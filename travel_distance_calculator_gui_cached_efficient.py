#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
出差距離計算與地圖產生工具 (GUI版本 - 效率優化版)
主要優化：
1. 先找出所有唯一路線（最大公因數概念）
2. 只為唯一路線產生地圖，避免重複處理
3. 改進的進度顯示
"""

import os
import re
import sys
import time
import json
import pickle
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from collections import defaultdict
try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None
import folium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl
from openpyxl.drawing.image import Image as XLImage
from geopy.distance import geodesic
import warnings
warnings.filterwarnings('ignore')

# 座標資料庫
# ========== 地名資料：套件 gazetteer（可測試）==========
from pathlib import Path as _Path
import sys as _sys
_SRC = _Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in _sys.path:
    _sys.path.insert(0, str(_SRC))

from travel_carbon.data import (  # noqa: E402
    COORDINATES,
    ALIASES,
    TAIWAN_REGION_MAPPING,
    INTERNATIONAL_CITY_MAPPING,
    CHINA_KEYWORDS,
)
from travel_carbon.locations import (  # noqa: E402
    smart_destination_handler as _pkg_smart_destination_handler,
    is_domestic as _pkg_is_domestic,
    resolve_coordinates as _pkg_resolve_coordinates,
)
from travel_carbon.distance import (  # noqa: E402
    compute_driving_distance as _pkg_compute_driving,
    compute_island_flight_distance as _pkg_compute_island,
    compute_flight_distance as _pkg_compute_flight,
)
# ========== 地名資料結束 ==========


# ========== 碳排放 / 縮放：優先使用可測試套件 ==========
try:
    from travel_carbon.carbon import (  # type: ignore
        CARBON_EMISSION_FACTORS,
        determine_transport_mode,
        calculate_carbon_emission,
    )
    from travel_carbon.zoom import calculate_zoom_level  # type: ignore
except ImportError:
    # Fallback when package not installed (python path = repo root only)
    # 簡化係數 (kg CO2e/km)；正式盤查請對照環境部公告，見 docs/emission_factors_notes.md
    CARBON_EMISSION_FACTORS = {
        '自用車/計程車': 0.21,
        '國內航班': 0.133,
        '國際航班': 0.101,
        '火車/高鐵': 0.034,
        '巴士': 0.065,
    }

    def determine_transport_mode(travel_type, distance_km):
        if distance_km <= 0:
            return ('N/A', 0)
        if '國際' in travel_type:
            return ('國際航班', CARBON_EMISSION_FACTORS['國際航班'])
        elif '離島' in travel_type or '航班' in travel_type:
            return ('國內航班', CARBON_EMISSION_FACTORS['國內航班'])
        elif '開車' in travel_type:
            if distance_km > 300:
                return ('火車/高鐵', CARBON_EMISSION_FACTORS['火車/高鐵'])
            else:
                return ('自用車/計程車', CARBON_EMISSION_FACTORS['自用車/計程車'])
        else:
            if distance_km > 500:
                return ('國內航班', CARBON_EMISSION_FACTORS['國內航班'])
            elif distance_km > 300:
                return ('火車/高鐵', CARBON_EMISSION_FACTORS['火車/高鐵'])
            else:
                return ('自用車/計程車', CARBON_EMISSION_FACTORS['自用車/計程車'])

    def calculate_carbon_emission(travel_type, distance_km):
        transport_mode, factor = determine_transport_mode(travel_type, distance_km)
        emission = round(distance_km * factor, 3) if distance_km > 0 else 0
        return {
            '交通方式': transport_mode,
            '碳排係數': factor,
            '碳排放量(kg CO2e)': emission,
        }

    def calculate_zoom_level(distance_km):
        if distance_km < 10:
            return 13
        elif distance_km < 20:
            return 12
        elif distance_km < 40:
            return 11
        elif distance_km < 80:
            return 10
        elif distance_km < 150:
            return 9
        elif distance_km < 300:
            return 8
        elif distance_km < 600:
            return 7
        elif distance_km < 1500:
            return 6
        elif distance_km < 3000:
            return 5
        elif distance_km < 6000:
            return 4
        else:
            return 3
# ========== 碳排放 / 縮放結束 ==========

class TravelDistanceCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("出差距離計算與地圖產生工具 (效率優化版)")
        self.root.geometry("1200x800")
        
        # 確保視窗在最前面
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        
        # 設定樣式
        style = ttk.Style()
        style.theme_use('clam')
        
        # 變數
        self.input_file = tk.StringVar()
        self.output_dir = tk.StringVar(value=os.path.expanduser("~/Downloads/差旅費"))
        self.start_row = tk.IntVar(value=1)
        self.end_row = tk.IntVar(value=10000)  # 預設處理到第10000列
        self.progress = tk.DoubleVar()
        self.status_text = tk.StringVar(value="準備就緒")
        
        # 資料存儲
        self.df_locations = None
        self.results = []
        self.unique_routes = {}  # 儲存唯一路線資訊
        
        # 快取機制
        self.route_cache = {}  # 儲存已計算的路線
        self.map_cache = {}    # 儲存已產生的地圖檔案
        self.load_cache()      # 載入既有快取
        
        self.setup_ui()
        
    def load_cache(self):
        """載入快取檔案"""
        cache_dir = os.path.expanduser("~/Downloads/差旅費/.cache")
        os.makedirs(cache_dir, exist_ok=True)
        
        # 載入路線快取
        route_cache_file = os.path.join(cache_dir, 'route_cache.pkl')
        if os.path.exists(route_cache_file):
            try:
                with open(route_cache_file, 'rb') as f:
                    self.route_cache = pickle.load(f)
                print(f"載入 {len(self.route_cache)} 條快取路線")
            except:
                self.route_cache = {}
                
        # 載入地圖快取
        map_cache_file = os.path.join(cache_dir, 'map_cache.json')
        if os.path.exists(map_cache_file):
            try:
                with open(map_cache_file, 'r', encoding='utf-8') as f:
                    self.map_cache = json.load(f)
                # 檢查快取的地圖檔案是否仍存在
                valid_cache = {}
                for key, path in self.map_cache.items():
                    if os.path.exists(path):
                        valid_cache[key] = path
                self.map_cache = valid_cache
                print(f"載入 {len(self.map_cache)} 個有效快取地圖")
            except:
                self.map_cache = {}
                
    def save_cache(self):
        """儲存快取檔案"""
        cache_dir = os.path.expanduser("~/Downloads/差旅費/.cache")
        
        # 儲存路線快取
        route_cache_file = os.path.join(cache_dir, 'route_cache.pkl')
        with open(route_cache_file, 'wb') as f:
            pickle.dump(self.route_cache, f)
            
        # 儲存地圖快取
        map_cache_file = os.path.join(cache_dir, 'map_cache.json')
        with open(map_cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.map_cache, f, ensure_ascii=False, indent=2)
        
    def setup_ui(self):
        """設置UI介面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 檔案選擇區
        file_frame = ttk.LabelFrame(main_frame, text="檔案設定", padding="10")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(file_frame, text="輸入檔案:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(file_frame, textvariable=self.input_file, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(file_frame, text="瀏覽", command=self.browse_input_file).grid(row=0, column=2)
        
        ttk.Label(file_frame, text="輸出目錄:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(file_frame, textvariable=self.output_dir, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(file_frame, text="瀏覽", command=self.browse_output_dir).grid(row=1, column=2)
        
        # 處理範圍設定
        range_frame = ttk.LabelFrame(main_frame, text="處理範圍", padding="10")
        range_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(range_frame, text="起始列:").grid(row=0, column=0, sticky=tk.W)
        ttk.Spinbox(range_frame, from_=1, to=10000, textvariable=self.start_row, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(range_frame, text="結束列:").grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        ttk.Spinbox(range_frame, from_=1, to=10000, textvariable=self.end_row, width=10).grid(row=0, column=3, padx=5)
        
        # 快取資訊
        self.cache_info_label = ttk.Label(range_frame, text=f"快取: {len(self.route_cache)} 條路線, {len(self.map_cache)} 個地圖")
        self.cache_info_label.grid(row=0, column=4, padx=(20, 0))
        
        # 效率資訊
        self.efficiency_label = ttk.Label(range_frame, text="")
        self.efficiency_label.grid(row=1, column=0, columnspan=5, pady=5)
        
        # 控制按鈕
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="載入資料", command=self.load_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="計算距離", command=self.calculate_distances).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="產生地圖", command=self.generate_maps).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="匯出Excel", command=self.export_excel).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清除快取", command=self.clear_cache).pack(side=tk.LEFT, padx=5)
        
        # 新增一鍵處理全部按鈕
        ttk.Separator(button_frame, orient='vertical').pack(side=tk.LEFT, fill='y', padx=10)
        self.process_all_btn = ttk.Button(button_frame, text="一鍵處理全部", 
                                         command=self.process_all_data, 
                                         style='Accent.TButton')
        self.process_all_btn.pack(side=tk.LEFT, padx=5)
        
        # 進度條
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress, maximum=100)
        self.progress_bar.pack(fill=tk.X, expand=True)
        
        # 狀態列
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Label(status_frame, textvariable=self.status_text).pack(side=tk.LEFT)
        
        # 結果顯示區
        result_frame = ttk.LabelFrame(main_frame, text="處理結果", padding="10")
        result_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 建立Treeview
        columns = ('序號', '傳票編號', '目的地', '類型', '距離(km)', '時間', '地圖', '快取')
        self.tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=15)
        
        # 設定欄位
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100 if col != '快取' else 60)
        
        # 捲軸
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 配置grid權重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
    def update_cache_info(self):
        """更新快取資訊顯示"""
        self.cache_info_label.config(text=f"快取: {len(self.route_cache)} 條路線, {len(self.map_cache)} 個地圖")
        
    def process_all_data(self):
        """一鍵處理所有資料"""
        if self.df_locations is None:
            messagebox.showerror("錯誤", "請先載入資料")
            return
            
        # 確認處理所有資料
        total_rows = len(self.df_locations)
        if messagebox.askyesno("確認", f"確定要處理所有 {total_rows} 筆資料嗎？\n\n這可能需要一些時間。"):
            # 設定處理範圍為全部
            self.start_row.set(1)
            self.end_row.set(total_rows)
            
            # 依序執行：計算距離 -> 產生地圖 -> 匯出Excel
            self.status_text.set("開始一鍵處理...")
            
            # 在新執行緒中執行
            thread = threading.Thread(target=self._process_all_thread)
            thread.start()
            
    def _process_all_thread(self):
        """一鍵處理的執行緒函數"""
        try:
            # 步驟1: 計算距離
            self.root.after(0, lambda: self.status_text.set("步驟 1/3: 計算距離..."))
            self._calculate_distances_thread()
            
            # 等待計算完成
            while self.progress.get() < 100:
                time.sleep(0.1)
            
            # 步驟2: 產生地圖
            self.root.after(0, lambda: self.status_text.set("步驟 2/3: 產生地圖..."))
            self.progress.set(0)  # 重置進度條
            self._generate_maps_thread()
            
            # 等待地圖產生完成
            while self.progress.get() < 100:
                time.sleep(0.1)
            
            # 步驟3: 匯出Excel
            self.root.after(0, lambda: self.status_text.set("步驟 3/3: 匯出Excel..."))
            self.root.after(0, self.export_excel)
            
            # 完成
            self.root.after(0, lambda: messagebox.showinfo("完成", 
                f"一鍵處理完成！\n\n" +
                f"已處理 {len(self.results)} 筆資料\n" +
                f"產生 {len(self.unique_routes)} 個唯一路線地圖\n" +
                f"結果已匯出至 Excel 檔案"))
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("錯誤", f"一鍵處理失敗: {str(e)}"))
            self.root.after(0, lambda: self.status_text.set("一鍵處理失敗"))
        
    def clear_cache(self):
        """清除快取"""
        if messagebox.askyesno("確認", "確定要清除所有快取嗎？"):
            self.route_cache = {}
            self.map_cache = {}
            self.save_cache()
            self.update_cache_info()
            messagebox.showinfo("成功", "快取已清除")
            self.status_text.set("快取已清除")
        
    def browse_input_file(self):
        """選擇輸入檔案"""
        filename = filedialog.askopenfilename(
            title="選擇Excel檔案",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if filename:
            self.input_file.set(filename)
            
    def browse_output_dir(self):
        """選擇輸出目錄"""
        directory = filedialog.askdirectory(title="選擇輸出目錄")
        if directory:
            self.output_dir.set(directory)
            
    def load_data(self):
        """載入Excel資料"""
        if not self.input_file.get():
            messagebox.showerror("錯誤", "請先選擇輸入檔案")
            return
            
        try:
            self.status_text.set("正在載入資料...")
            self.df_locations = pd.read_excel(self.input_file.get())
            
            # 顯示資料資訊
            total_rows = len(self.df_locations)
            
            # 分析資料內容
            destinations_col = '出差地點' if '出差地點' in self.df_locations.columns else None
            if destinations_col:
                # 計算有出差地點的資料筆數
                has_destination = self.df_locations[destinations_col].notna().sum()
                no_destination = total_rows - has_destination
                info_msg = f"成功載入 {total_rows} 筆資料\n\n" + \
                          f"- 有出差地點: {has_destination} 筆\n" + \
                          f"- 無出差地點: {no_destination} 筆"
            else:
                info_msg = f"成功載入 {total_rows} 筆資料\n\n注意：找不到'出差地點'欄位"
                
            messagebox.showinfo("載入成功", info_msg)
            self.status_text.set(f"已載入 {total_rows} 筆資料")
            
            # 更新範圍設定為全部資料
            self.end_row.set(total_rows)  # 預設處理所有資料
            
        except Exception as e:
            messagebox.showerror("錯誤", f"載入資料失敗: {str(e)}")
            self.status_text.set("載入失敗")
            
    def calculate_distances(self):
        """計算距離"""
        if self.df_locations is None:
            messagebox.showerror("錯誤", "請先載入資料")
            return
            
        # 在新執行緒中執行計算
        thread = threading.Thread(target=self._calculate_distances_thread)
        thread.start()
        
    def _calculate_distances_thread(self):
        """計算距離的執行緒函數"""
        try:
            start_idx = self.start_row.get() - 1
            end_idx = self.end_row.get()
            
            # 清空結果
            self.results = []
            self.unique_routes = {}
            self.tree.delete(*self.tree.get_children())
            
            # 處理選定範圍的資料
            subset = self.df_locations.iloc[start_idx:end_idx]
            total = len(subset)
            
            # 先分析所有唯一的目的地
            destinations_count = defaultdict(int)
            for _, row in subset.iterrows():
                dests = str(row.get('出差地點', '')).split('、') if pd.notna(row.get('出差地點', '')) else []
                if dests and dests[0]:
                    destinations_count[dests[0]] += 1
                    
            # 顯示效率資訊
            unique_count = len(destinations_count)
            self.root.after(0, lambda: self.efficiency_label.config(
                text=f"發現 {unique_count} 個不同目的地，共 {total} 筆資料"
            ))
            
            cache_hit = 0
            api_calls = 0
            skipped = 0  # 記錄跳過的筆數
            
            for idx, (_, row) in enumerate(subset.iterrows()):
                self.status_text.set(f"正在處理第 {idx+1}/{total} 筆...")
                self.progress.set((idx + 1) / total * 100)
                
                # 取得目的地
                destinations = str(row.get('出差地點', '')).split('、') if pd.notna(row.get('出差地點', '')) else []
                
                # 處理特殊情況
                if destinations and destinations[0] and destinations[0].strip() not in ['無地點資訊', '無', '']:
                    destination = destinations[0].strip()  # 取第一個目的地並去除空白
                    
                    # 智能處理目的地
                    destination = self._smart_destination_handler(destination)
                    
                    # 特殊處理離島（使用飛機）
                    if destination in ['澎湖', '金門', '馬祖'] or (destination in COORDINATES and COORDINATES[destination].get('type') == 'island'):
                        # 台灣離島：使用飛機
                        result = self._calculate_island_flight_distance(row, destination)
                        if result and result.get('cached'):
                            cache_hit += 1
                    elif self._is_domestic(destination):
                        # 台灣本島：統一從輔大出發開車
                        result = self._calculate_driving_distance(row, destination)
                        if result and result.get('cached'):
                            cache_hit += 1
                        else:
                            api_calls += 1
                    else:
                        # 國外：計算飛行距離（從桃園機場出發）
                        result = self._calculate_flight_distance(row, destination)
                        if result and result.get('cached'):
                            cache_hit += 1
                    
                    if result:
                        self.results.append(result)
                        # 更新UI
                        self.root.after(0, self._add_result_to_tree, result)
                        
                        # 收集唯一路線資訊
                        route_key = result.get('route_key')
                        if route_key and route_key not in self.unique_routes:
                            self.unique_routes[route_key] = {
                                '起點': result['起點'],
                                '終點': result['終點'],
                                '類型': result['類型'],
                                '距離(km)': result['距離(km)'],
                                '時間': result['時間'],
                                'route': result.get('route'),
                                'results': []
                            }
                        if route_key:
                            self.unique_routes[route_key]['results'].append(result)
                else:
                    # 如果沒有出差地點，仍然保留這筆記錄
                    # 檢查原始資料內容
                    original_location = str(row.get('出差地點', ''))
                    if original_location in ['無地點資訊', '無']:
                        display_text = original_location
                    else:
                        display_text = '無出差地點'
                        
                    empty_result = {
                        '序號': row['序號'],
                        '傳票編號': row['傳票編號'],
                        '目的地': display_text,
                        '類型': 'N/A',
                        '距離(km)': 0,
                        '時間': 'N/A',
                        '起點': {'name': '輔仁大學', 'lat': 25.0356, 'lon': 121.4320},
                        '終點': {'name': '無', 'lat': 0, 'lon': 0},
                        'route': None,
                        'route_key': 'no-destination',
                        'cached': False
                    }
                    self.results.append(empty_result)
                    self.root.after(0, self._add_result_to_tree, empty_result)
                
                # 減少API請求頻率
                if api_calls > 0 and (api_calls % 5 == 0):
                    time.sleep(1)
                    
            # 儲存快取
            self.save_cache()
            self.update_cache_info()
            
            # 統計處理結果
            processed = len([r for r in self.results if r.get('距離(km)', 0) > 0])
            no_destination = len([r for r in self.results if r.get('目的地') == '無出差地點'])
            unknown = len([r for r in self.results if '未知' in r.get('類型', '')])
            
            self.status_text.set(
                f"計算完成！共 {len(self.results)} 筆 "
                f"(成功處理 {processed} 筆，無目的地 {no_destination} 筆，未知地點 {unknown} 筆)，"
                f"{len(self.unique_routes)} 條唯一路線，"
                f"快取命中 {cache_hit} 筆，新計算 {api_calls} 筆"
            )
            self.progress.set(100)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("錯誤", f"計算失敗: {str(e)}"))
            self.status_text.set("計算失敗")
            
    def _smart_destination_handler(self, destination):
        """智能處理目的地名稱（委派套件）"""
        return _pkg_smart_destination_handler(destination)
            
    def _is_domestic(self, destination):
        """判斷是否為國內本島地點（委派套件）"""
        return _pkg_is_domestic(destination)
        
    def _calculate_driving_distance(self, row, destination):
        """計算開車距離（委派 travel_carbon.distance）"""
        return _pkg_compute_driving(
            destination,
            row=row,
            route_cache=self.route_cache,
            use_osrm=True,
        )

    def _calculate_island_flight_distance(self, row, destination):
        """計算台灣離島航班距離（委派套件）"""
        return _pkg_compute_island(
            destination,
            row=row,
            route_cache=self.route_cache,
        )

    def _calculate_flight_distance(self, row, destination):
        """計算國際飛行距離（委派套件）"""
        return _pkg_compute_flight(
            destination,
            row=row,
            route_cache=self.route_cache,
        )

    def _add_result_to_tree(self, result):
        """添加結果到Treeview"""
        values = (
            result['序號'],
            result['傳票編號'],
            result['目的地'],
            result['類型'],
            result['距離(km)'],
            result['時間'],
            '待產生',
            '✓' if result.get('cached') else ''
        )
        self.tree.insert('', 'end', values=values)
        
    def generate_maps(self):
        """產生地圖"""
        if not self.results:
            messagebox.showerror("錯誤", "請先計算距離")
            return
            
        # 在新執行緒中執行
        thread = threading.Thread(target=self._generate_maps_thread)
        thread.start()
        
    def _generate_maps_thread(self):
        """產生地圖的執行緒函數 - 優化版本"""
        try:
            # 確保輸出目錄存在
            map_dir = os.path.join(self.output_dir.get(), 'maps')
            os.makedirs(map_dir, exist_ok=True)
            
            # 只處理唯一路線，不是每個結果
            total_unique_routes = len(self.unique_routes)
            cache_hit = 0
            new_maps = 0
            
            self.status_text.set(f"準備產生 {total_unique_routes} 個唯一路線的地圖...")
            
            # 只為每個唯一路線產生一次地圖
            for idx, (route_key, route_info) in enumerate(self.unique_routes.items()):
                self.status_text.set(f"正在處理唯一路線 {idx+1}/{total_unique_routes}...")
                self.progress.set((idx + 1) / total_unique_routes * 100)
                
                # 檢查是否已有快取的地圖
                if route_key in self.map_cache and os.path.exists(self.map_cache[route_key]):
                    # 使用已存在的地圖檔案
                    map_file = self.map_cache[route_key]
                    cache_hit += 1
                    self.status_text.set(f"使用快取地圖: {route_key}")
                else:
                    # 產生新地圖（使用第一個結果作為範本）
                    sample_result = route_info['results'][0]
                    map_file = self._create_map(sample_result, map_dir, route_key)
                    
                    if map_file:
                        # 截圖
                        screenshot = self._capture_map_screenshot(map_file)
                        if screenshot:
                            map_file = screenshot
                            
                        # 儲存到快取
                        self.map_cache[route_key] = map_file
                        new_maps += 1
                        self.status_text.set(f"已產生新地圖: {route_key}")
                
                # 將地圖檔案分配給所有使用此路線的結果
                if map_file:
                    for result in route_info['results']:
                        result['地圖檔案'] = map_file
                        # 更新UI顯示
                        self._update_tree_for_result(result)
                    
            # 儲存快取
            self.save_cache()
            self.update_cache_info()
            
            # 計算效率提升
            total_results = len(self.results)
            efficiency_ratio = round((1 - total_unique_routes / total_results) * 100, 1) if total_results > 0 else 0
            
            self.status_text.set(
                f"地圖產生完成！共 {total_results} 筆資料，"
                f"僅需產生 {total_unique_routes} 個地圖，"
                f"效率提升 {efficiency_ratio}%，"
                f"快取 {cache_hit} 個，新建 {new_maps} 個"
            )
            self.progress.set(100)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("錯誤", f"產生地圖失敗: {str(e)}"))
            self.status_text.set("產生地圖失敗")
            
    def _update_tree_for_result(self, result):
        """更新特定結果在 TreeView 中的顯示"""
        items = self.tree.get_children()
        for item in items:
            values = list(self.tree.item(item)['values'])
            if values[0] == result['序號'] and values[1] == result['傳票編號']:
                values[-2] = '已產生'  # 更新地圖狀態
                self.tree.item(item, values=values)
                break
                
    def _create_map(self, result, output_dir, name):
        """創建地圖（包含智能縮放）"""
        try:
            # 取得起終點座標
            start_lat = result['起點']['lat']
            start_lon = result['起點']['lon']
            end_lat = result['終點']['lat']
            end_lon = result['終點']['lon']
            
            # 計算中心點
            center_lat = (start_lat + end_lat) / 2
            center_lon = (start_lon + end_lon) / 2
            
            # 根據距離決定縮放級別
            distance = result.get('距離(km)', 0)
            zoom_level = calculate_zoom_level(distance)
            
            # 創建地圖
            m = folium.Map(
                location=[center_lat, center_lon], 
                zoom_start=zoom_level,
                tiles='OpenStreetMap',
                prefer_canvas=True
            )
            
            # 添加起點標記（綠色）
            folium.Marker(
                [start_lat, start_lon],
                popup=f"<b>起點</b><br>{result['起點']['name']}",
                icon=folium.Icon(color='green', icon='play', prefix='fa'),
                tooltip="起點"
            ).add_to(m)
            
            # 添加終點標記（紅色）
            folium.Marker(
                [end_lat, end_lon],
                popup=f"<b>終點</b><br>{result['終點']['name']}",
                icon=folium.Icon(color='red', icon='stop', prefix='fa'),
                tooltip="終點"
            ).add_to(m)
            
            # 添加路線
            if result['類型'] == '國內-開車' and result.get('route'):
                # 開車路線（詳細路徑）
                route_coords = [[coord[1], coord[0]] for coord in result['route']['coordinates']]
                
                # 主路線
                folium.PolyLine(
                    route_coords,
                    color='#0066CC',
                    weight=6,
                    opacity=0.8,
                    smooth_factor=1
                ).add_to(m)
                
                # 路線邊框（讓路線更明顯）
                folium.PolyLine(
                    route_coords,
                    color='#000033',
                    weight=8,
                    opacity=0.4,
                    smooth_factor=1
                ).add_to(m)
                
                # 使用路線邊界來調整地圖視野
                if len(route_coords) > 0:
                    lats = [coord[0] for coord in route_coords]
                    lons = [coord[1] for coord in route_coords]
                    sw = [min(lats), min(lons)]
                    ne = [max(lats), max(lons)]
                    
                    # 根據距離調整padding
                    if distance < 20:
                        padding = 0.02  # 短距離用較小的padding
                    elif distance < 50:
                        padding = 0.05
                    else:
                        padding = 0.1
                        
                    m.fit_bounds([sw, ne], padding=(padding, padding))
                    
            else:
                # 飛行路線（曲線）
                # 添加飛行路線的曲線效果（貝茲曲線）
                import numpy as np
                t = np.linspace(0, 1, 50)
                
                # 計算控制點（讓路線呈現弧形）
                control_lat = center_lat + (distance / 10000) * 5  # 根據距離調整弧度
                control_lon = center_lon
                
                # 二次貝茲曲線
                curve_lats = (1-t)**2 * start_lat + 2*(1-t)*t * control_lat + t**2 * end_lat
                curve_lons = (1-t)**2 * start_lon + 2*(1-t)*t * control_lon + t**2 * end_lon
                
                curve_coords = [[lat, lon] for lat, lon in zip(curve_lats, curve_lons)]
                
                # 飛行路線（橘色曲線）
                folium.PolyLine(
                    curve_coords,
                    color='#FF6600',
                    weight=4,
                    opacity=0.8
                ).add_to(m)
                
                # 虛線直線（參考用）
                folium.PolyLine(
                    [[start_lat, start_lon], [end_lat, end_lon]],
                    color='#CC0000',
                    weight=2,
                    opacity=0.4,
                    dash_array='10, 5'
                ).add_to(m)
                
                # 確保兩個機場都在視野內
                sw = [min(start_lat, end_lat), min(start_lon, end_lon)]
                ne = [max(start_lat, end_lat), max(start_lon, end_lon)]
                
                # 國際航線需要更大的padding
                padding = 0.2 if distance > 1000 else 0.1
                m.fit_bounds([sw, ne], padding=(padding, padding))
            
            # 添加距離標記（在路線中點）
            folium.Marker(
                [center_lat, center_lon],
                icon=folium.DivIcon(
                    html=f"""
                    <div style="background-color: white; 
                                border: 2px solid black; 
                                border-radius: 5px; 
                                padding: 5px;
                                font-weight: bold;
                                font-size: 12px;">
                        {distance} km
                    </div>
                    """
                )
            ).add_to(m)
            
            # 添加資訊框（固定在右上角）- 不顯示特定傳票編號
            info_html = f"""
            <div style='position: fixed; 
                        top: 10px; right: 10px; 
                        background: rgba(255,255,255,0.95); 
                        padding: 15px;
                        border: 2px solid #333;
                        border-radius: 8px;
                        font-family: "Microsoft JhengHei", Arial;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
                        z-index: 9999;
                        max-width: 300px;'>
                <h3 style='margin: 0 0 10px 0; color: #333;'>路線資訊</h3>
                <table style='font-size: 14px;'>
                    <tr><td style='padding: 3px;'><b>起點:</b></td><td>{result['起點']['name']}</td></tr>
                    <tr><td style='padding: 3px;'><b>終點:</b></td><td>{result['終點']['name']}</td></tr>
                    <tr><td style='padding: 3px;'><b>距離:</b></td><td style='color: #0066CC; font-weight: bold;'>{distance} km</td></tr>
                    <tr><td style='padding: 3px;'><b>時間:</b></td><td>{result.get('時間', 'N/A')}</td></tr>
                    <tr><td style='padding: 3px;'><b>類型:</b></td><td>{result.get('類型', 'N/A')}</td></tr>
                </table>
            </div>
            """
            m.get_root().html.add_child(folium.Element(info_html))
            
            # 儲存地圖
            filename = f"map_{name}.html"
            filepath = os.path.join(output_dir, filename)
            m.save(filepath)
            
            return filepath
            
        except Exception as e:
            print(f"創建地圖失敗: {e}")
            return None
            
    def _capture_map_screenshot(self, html_file):
        """截取地圖截圖"""
        try:
            # 設置Chrome選項
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--window-size=1200,800')
            
            # 創建瀏覽器實例
            driver = webdriver.Chrome(options=options)
            
            # 載入地圖
            driver.get(f"file://{html_file}")
            
            # 等待地圖載入
            time.sleep(3)
            
            # 截圖
            screenshot_path = html_file.replace('.html', '.png')
            driver.save_screenshot(screenshot_path)
            
            driver.quit()
            
            return screenshot_path
            
        except Exception as e:
            print(f"截圖失敗: {e}")
            # 如果Chrome截圖失敗，返回None
            return None
            
    def _update_tree_item(self, index, status):
        """更新Treeview項目"""
        items = self.tree.get_children()
        if index < len(items):
            item = items[index]
            values = list(self.tree.item(item)['values'])
            values[-2] = status  # 地圖狀態
            self.tree.item(item, values=values)
            
    def export_excel(self):
        """匯出Excel"""
        if not self.results:
            messagebox.showerror("錯誤", "沒有可匯出的資料")
            return
            
        try:
            self.status_text.set("正在匯出Excel...")
            
            # 建立DataFrame
            export_data = []
            for result in self.results:
                carbon = calculate_carbon_emission(result['類型'], result['距離(km)'])
                export_data.append({
                    '序號': result['序號'],
                    '傳票編號': result['傳票編號'],
                    '目的地': result['目的地'],
                    '類型': result['類型'],
                    '距離(km)': result['距離(km)'],
                    '時間': result['時間'],
                    '起點': result['起點']['name'],
                    '終點': result['終點']['name'],
                    '交通方式': carbon['交通方式'],
                    '碳排係數': carbon['碳排係數'],
                    '碳排放量(kg CO2e)': carbon['碳排放量(kg CO2e)'],
                })
                
            df = pd.DataFrame(export_data)
            
            # 儲存Excel
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.output_dir.get(), f'出差距離計算結果_{timestamp}.xlsx')
            
            # 使用ExcelWriter來插入圖片
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='距離計算結果', index=False)
                
                # 取得工作表
                workbook = writer.book
                worksheet = writer.sheets['距離計算結果']
                
                # 調整欄寬
                column_widths = {'A': 10, 'B': 15, 'C': 30, 'D': 15, 'E': 12, 'F': 12, 'G': 20, 'H': 20,
                                 'I': 18, 'J': 12, 'K': 20}
                for column, width in column_widths.items():
                    worksheet.column_dimensions[column].width = width
                    
                # 插入地圖截圖（如果有的話）
                if any('地圖檔案' in r for r in self.results):
                    # 新增一個工作表放地圖
                    ws_maps = workbook.create_sheet('地圖')
                    
                    # 使用已經整理好的唯一路線資訊
                    row = 1
                    for route_key, route_info in self.unique_routes.items():
                        results = route_info['results']
                        result = results[0]  # 取第一個結果作為範本
                        
                        if '地圖檔案' in result and result['地圖檔案'] and os.path.exists(result['地圖檔案']):
                            # 添加標題
                            ws_maps.cell(row=row, column=1, value=f"路線: {result['起點']['name']} → {result['終點']['name']}")
                            ws_maps.cell(row=row, column=1).font = openpyxl.styles.Font(bold=True, size=14)
                            row += 1
                            
                            # 列出使用此路線的所有傳票
                            vouchers = [str(r['傳票編號']) for r in results]  # 確保轉換為字串
                            ws_maps.cell(row=row, column=1, value=f"傳票編號: {', '.join(vouchers)}")
                            ws_maps.cell(row=row, column=2, value=f"(共 {len(vouchers)} 筆)")
                            row += 1
                            
                            # 列出距離和時間
                            ws_maps.cell(row=row, column=1, value=f"距離: {result['距離(km)']} km | 時間: {result['時間']}")
                            row += 1
                            
                            # 插入圖片
                            try:
                                if result['地圖檔案'].endswith('.png'):
                                    img = XLImage(result['地圖檔案'])
                                    img.width = 600
                                    img.height = 400
                                    ws_maps.add_image(img, f'A{row}')
                                    row += 25  # 預留圖片空間
                                else:
                                    ws_maps.cell(row=row, column=1, value=f"地圖檔案: {result['地圖檔案']}")
                                    row += 2
                            except Exception as e:
                                print(f"插入圖片失敗: {e}")
                                ws_maps.cell(row=row, column=1, value=f"地圖檔案: {result['地圖檔案']}")
                                row += 2
                            
                            # 添加分隔線
                            row += 2

                # ========== 碳排放總覽工作表 ==========
                ws_carbon = workbook.create_sheet('碳排放總覽')

                # 標題樣式
                title_font = openpyxl.styles.Font(bold=True, size=14)
                header_font = openpyxl.styles.Font(bold=True, size=11)
                header_fill = openpyxl.styles.PatternFill(start_color='D9E1F2', end_color='D9E1F2', fill_type='solid')

                # 計算碳排放資料
                carbon_by_mode = defaultdict(lambda: {'trips': 0, 'distance': 0, 'emission': 0})
                total_emission = 0
                total_trips = 0
                for r in self.results:
                    dist = r.get('距離(km)', 0)
                    if dist <= 0:
                        continue
                    c = calculate_carbon_emission(r['類型'], dist)
                    mode = c['交通方式']
                    if mode == 'N/A':
                        continue
                    carbon_by_mode[mode]['trips'] += 1
                    carbon_by_mode[mode]['distance'] += dist
                    carbon_by_mode[mode]['emission'] += c['碳排放量(kg CO2e)']
                    total_emission += c['碳排放量(kg CO2e)']
                    total_trips += 1

                # 總覽標題
                ws_carbon.cell(row=1, column=1, value='碳排放總覽').font = title_font
                ws_carbon.cell(row=2, column=1, value=f'產生日期：{datetime.now().strftime("%Y-%m-%d %H:%M")}')

                # 總計區塊
                ws_carbon.cell(row=4, column=1, value='總碳排放量(kg CO2e)').font = header_font
                ws_carbon.cell(row=4, column=2, value=round(total_emission, 3))
                ws_carbon.cell(row=5, column=1, value='有效出差筆數').font = header_font
                ws_carbon.cell(row=5, column=2, value=total_trips)
                ws_carbon.cell(row=6, column=1, value='平均每趟碳排(kg CO2e)').font = header_font
                ws_carbon.cell(row=6, column=2, value=round(total_emission / total_trips, 3) if total_trips > 0 else 0)

                # 各交通方式明細表
                ws_carbon.cell(row=8, column=1, value='各交通方式碳排明細').font = title_font
                detail_headers = ['交通方式', '出差筆數', '總距離(km)', '碳排係數(kg/km)', '碳排放量(kg CO2e)', '佔比(%)']
                for col_idx, h in enumerate(detail_headers, 1):
                    cell = ws_carbon.cell(row=9, column=col_idx, value=h)
                    cell.font = header_font
                    cell.fill = header_fill

                detail_row = 10
                for mode, data in sorted(carbon_by_mode.items(), key=lambda x: x[1]['emission'], reverse=True):
                    factor = CARBON_EMISSION_FACTORS.get(mode, 0)
                    pct = round(data['emission'] / total_emission * 100, 1) if total_emission > 0 else 0
                    ws_carbon.cell(row=detail_row, column=1, value=mode)
                    ws_carbon.cell(row=detail_row, column=2, value=data['trips'])
                    ws_carbon.cell(row=detail_row, column=3, value=round(data['distance'], 1))
                    ws_carbon.cell(row=detail_row, column=4, value=factor)
                    ws_carbon.cell(row=detail_row, column=5, value=round(data['emission'], 3))
                    ws_carbon.cell(row=detail_row, column=6, value=pct)
                    detail_row += 1

                # 合計列
                ws_carbon.cell(row=detail_row, column=1, value='合計').font = header_font
                ws_carbon.cell(row=detail_row, column=2, value=total_trips).font = header_font
                total_dist = sum(d['distance'] for d in carbon_by_mode.values())
                ws_carbon.cell(row=detail_row, column=3, value=round(total_dist, 1)).font = header_font
                ws_carbon.cell(row=detail_row, column=5, value=round(total_emission, 3)).font = header_font
                ws_carbon.cell(row=detail_row, column=6, value=100.0).font = header_font

                # 調整碳排放工作表欄寬
                carbon_col_widths = {'A': 20, 'B': 15, 'C': 15, 'D': 18, 'E': 22, 'F': 12}
                for col, w in carbon_col_widths.items():
                    ws_carbon.column_dimensions[col].width = w
                # ========== 碳排放總覽結束 ==========

            messagebox.showinfo("成功", f"Excel已匯出至:\n{output_file}")
            self.status_text.set("匯出完成")
            
        except Exception as e:
            messagebox.showerror("錯誤", f"匯出失敗: {str(e)}")
            self.status_text.set("匯出失敗")
            
    def run(self):
        """執行GUI"""
        # 確保視窗顯示
        self.root.update()
        self.root.deiconify()
        print("GUI視窗已啟動...")
        self.root.mainloop()


# 主程式
if __name__ == "__main__":
    # 確保必要的套件已安裝
    required_packages = {
        'pandas': 'pandas',
        'folium': 'folium',
        'selenium': 'selenium',
        'PIL': 'pillow',
        'geopy': 'geopy',
        'openpyxl': 'openpyxl',
        'requests': 'requests'
    }
    
    missing_packages = []
    for import_name, install_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(install_name)
            
    if missing_packages:
        print("請先安裝以下套件:")
        print(f"pip install {' '.join(missing_packages)}")
        sys.exit(1)
    
    print("正在啟動出差距離計算與地圖產生工具...")
    
    try:
        # 啟動應用程式
        app = TravelDistanceCalculator()
        app.run()
    except Exception as e:
        print(f"啟動失敗: {e}")
        import traceback
        traceback.print_exc()
