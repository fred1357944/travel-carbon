#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
出差距離計算與地圖產生工具 (智能縮放版)
新功能：
1. 根據距離自動調整地圖縮放級別
2. 確保路線細節清晰可見
3. 短距離放大，長距離適當縮小
"""

import os
import sys
import time
import folium
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import requests
from geopy.distance import geodesic
import openpyxl
from openpyxl.drawing.image import Image as XLImage

# 座標資料庫（簡化版，用於示範）
COORDINATES = {
    '輔仁大學': {'lat': 25.0356, 'lon': 121.4320, 'name': '輔仁大學正門'},
    '台北': {'lat': 25.0330, 'lon': 121.5654, 'name': '台北市政府'},
    '臺北': {'lat': 25.0330, 'lon': 121.5654, 'name': '台北市政府'},
    '新北': {'lat': 25.0119, 'lon': 121.4653, 'name': '新北市政府'},
    '桃園': {'lat': 24.9936, 'lon': 121.3010, 'name': '桃園市政府'},
    '新竹': {'lat': 24.8138, 'lon': 120.9675, 'name': '新竹市政府'},
    '台中': {'lat': 24.1639, 'lon': 120.6478, 'name': '台中市政府'},
    '臺中': {'lat': 24.1639, 'lon': 120.6478, 'name': '台中市政府'},
    '台南': {'lat': 22.9997, 'lon': 120.2269, 'name': '台南市政府'},
    '臺南': {'lat': 22.9997, 'lon': 120.2269, 'name': '台南市政府'},
    '高雄': {'lat': 22.6273, 'lon': 120.3014, 'name': '高雄市政府'},
    '宜蘭': {'lat': 24.7021, 'lon': 121.7377, 'name': '宜蘭縣政府'},
    '花蓮': {'lat': 23.9871, 'lon': 121.6015, 'name': '花蓮縣政府'},
    '台東': {'lat': 22.7972, 'lon': 121.0713, 'name': '台東縣政府'},
    '臺東': {'lat': 22.7972, 'lon': 121.0713, 'name': '台東縣政府'},
    '桃園機場': {'lat': 25.0777, 'lon': 121.2325, 'name': '桃園國際機場'},
    '美國': {'lat': 33.9425, 'lon': -118.4081, 'name': '洛杉磯國際機場'},
    '日本': {'lat': 35.5494, 'lon': 139.7798, 'name': '成田國際機場'},
    '德國': {'lat': 50.0379, 'lon': 8.5622, 'name': '法蘭克福機場'},
}

def calculate_zoom_level(distance_km):
    """根據距離計算適當的地圖縮放級別"""
    if distance_km < 10:
        return 13  # 非常近的距離（如同區域）
    elif distance_km < 20:
        return 12  # 很近的距離（如新北）
    elif distance_km < 40:
        return 11  # 近距離（如台北）
    elif distance_km < 80:
        return 10  # 中等距離
    elif distance_km < 150:
        return 9   # 較遠距離（如台中）
    elif distance_km < 300:
        return 8   # 遠距離（如高雄）
    elif distance_km < 600:
        return 7   # 很遠距離
    elif distance_km < 1500:
        return 6   # 國際短程
    elif distance_km < 3000:
        return 5   # 國際中程
    elif distance_km < 6000:
        return 4   # 國際長程
    else:
        return 3   # 跨洲長程

def create_route_map(result, output_path):
    """創建路線地圖，根據距離自動調整縮放"""
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
            tiles='OpenStreetMap'
        )
        
        # 添加起點標記
        folium.Marker(
            [start_lat, start_lon],
            popup=f"<b>起點</b><br>{result['起點']['name']}<br>輔仁大學正門",
            icon=folium.Icon(color='green', icon='play', prefix='fa'),
            tooltip="起點"
        ).add_to(m)
        
        # 添加終點標記
        folium.Marker(
            [end_lat, end_lon],
            popup=f"<b>終點</b><br>{result['終點']['name']}",
            icon=folium.Icon(color='red', icon='stop', prefix='fa'),
            tooltip="終點"
        ).add_to(m)
        
        # 添加路線
        if result.get('類型') == '國內-開車' and result.get('route'):
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
            # 飛行路線（直線）
            folium.PolyLine(
                [[start_lat, start_lon], [end_lat, end_lon]],
                color='#CC0000',
                weight=4,
                opacity=0.8,
                dash_array='10, 5'
            ).add_to(m)
            
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
            
            folium.PolyLine(
                curve_coords,
                color='#FF6600',
                weight=3,
                opacity=0.6
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
        
        # 添加資訊框（固定在右上角）
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
                <tr><td style='padding: 3px;'><b>傳票編號:</b></td><td>{result.get('傳票編號', 'N/A')}</td></tr>
                <tr><td style='padding: 3px;'><b>起點:</b></td><td>{result['起點']['name']}</td></tr>
                <tr><td style='padding: 3px;'><b>終點:</b></td><td>{result['終點']['name']}</td></tr>
                <tr><td style='padding: 3px;'><b>距離:</b></td><td style='color: #0066CC; font-weight: bold;'>{distance} km</td></tr>
                <tr><td style='padding: 3px;'><b>時間:</b></td><td>{result.get('時間', 'N/A')}</td></tr>
                <tr><td style='padding: 3px;'><b>類型:</b></td><td>{result.get('類型', 'N/A')}</td></tr>
            </table>
        </div>
        """
        m.get_root().html.add_child(folium.Element(info_html))
        
        # 添加比例尺
        folium.plugins.MeasureControl(
            position='bottomleft',
            primary_length_unit='kilometers',
            secondary_length_unit='miles',
            primary_area_unit='sqkilometers',
            secondary_area_unit='acres'
        ).add_to(m)
        
        # 儲存地圖
        m.save(output_path)
        return True
        
    except Exception as e:
        print(f"創建地圖失敗: {e}")
        return False

# 示範用的簡單GUI
class MapDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("地圖縮放示範")
        self.root.geometry("600x400")
        
        # 建立示範資料
        self.demo_routes = [
            {
                '傳票編號': 'DEMO001',
                '起點': COORDINATES['輔仁大學'],
                '終點': COORDINATES['新北'],
                '距離(km)': 6,
                '時間': '15分鐘',
                '類型': '國內-開車',
                'route': None
            },
            {
                '傳票編號': 'DEMO002',
                '起點': COORDINATES['輔仁大學'],
                '終點': COORDINATES['台北'],
                '距離(km)': 20,
                '時間': '30分鐘',
                '類型': '國內-開車',
                'route': None
            },
            {
                '傳票編號': 'DEMO003',
                '起點': COORDINATES['輔仁大學'],
                '終點': COORDINATES['台中'],
                '距離(km)': 165,
                '時間': '2小時',
                '類型': '國內-開車',
                'route': None
            },
            {
                '傳票編號': 'DEMO004',
                '起點': COORDINATES['輔仁大學'],
                '終點': COORDINATES['高雄'],
                '距離(km)': 350,
                '時間': '4小時',
                '類型': '國內-開車',
                'route': None
            },
            {
                '傳票編號': 'DEMO005',
                '起點': COORDINATES['桃園機場'],
                '終點': COORDINATES['日本'],
                '距離(km)': 2150,
                '時間': '3.2小時',
                '類型': '國際-飛行',
                'route': None
            }
        ]
        
        self.setup_ui()
        
    def setup_ui(self):
        # 標題
        title = ttk.Label(self.root, text="智能地圖縮放示範", font=('Arial', 16, 'bold'))
        title.pack(pady=10)
        
        # 說明
        info = ttk.Label(self.root, text="根據不同距離，地圖會自動調整縮放級別以顯示最佳細節")
        info.pack(pady=5)
        
        # 路線列表
        frame = ttk.Frame(self.root)
        frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        columns = ('傳票編號', '終點', '距離', '縮放級別')
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        # 填充資料
        for route in self.demo_routes:
            zoom = calculate_zoom_level(route['距離(km)'])
            values = (
                route['傳票編號'],
                route['終點']['name'],
                f"{route['距離(km)']} km",
                f"Level {zoom}"
            )
            self.tree.insert('', 'end', values=values)
        
        self.tree.pack(fill='both', expand=True)
        
        # 按鈕
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="產生選定路線地圖", command=self.generate_map).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="產生所有地圖", command=self.generate_all_maps).pack(side='left', padx=5)
        
        # 狀態
        self.status = tk.StringVar(value="準備就緒")
        ttk.Label(self.root, textvariable=self.status).pack(pady=5)
        
    def generate_map(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("提示", "請先選擇一條路線")
            return
            
        idx = self.tree.index(selection[0])
        route = self.demo_routes[idx]
        
        output_dir = os.path.expanduser("~/Downloads/差旅費/maps_demo")
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"map_{route['傳票編號']}_{route['終點']['name']}.html"
        filepath = os.path.join(output_dir, filename)
        
        self.status.set(f"正在產生地圖: {route['終點']['name']}...")
        self.root.update()
        
        if create_route_map(route, filepath):
            self.status.set(f"地圖已產生: {filepath}")
            messagebox.showinfo("成功", f"地圖已儲存至:\n{filepath}")
        else:
            self.status.set("地圖產生失敗")
            messagebox.showerror("錯誤", "地圖產生失敗")
            
    def generate_all_maps(self):
        output_dir = os.path.expanduser("~/Downloads/差旅費/maps_demo")
        os.makedirs(output_dir, exist_ok=True)
        
        for i, route in enumerate(self.demo_routes):
            self.status.set(f"正在產生地圖 {i+1}/{len(self.demo_routes)}: {route['終點']['name']}...")
            self.root.update()
            
            filename = f"map_{route['傳票編號']}_{route['終點']['name']}.html"
            filepath = os.path.join(output_dir, filename)
            
            create_route_map(route, filepath)
            time.sleep(0.5)
            
        self.status.set("所有地圖產生完成")
        messagebox.showinfo("成功", f"所有地圖已儲存至:\n{output_dir}")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # 確保必要套件
    required = ['folium', 'pandas', 'geopy', 'requests', 'openpyxl']
    missing = []
    
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
            
    if missing:
        print(f"請先安裝套件: pip install {' '.join(missing)}")
        sys.exit(1)
        
    # 執行示範
    app = MapDemo()
    app.run()
