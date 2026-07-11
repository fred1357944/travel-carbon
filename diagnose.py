#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
診斷腳本 - 檢查所有相依套件
"""

import sys
import os

print("=== 系統資訊 ===")
print(f"Python 版本: {sys.version}")
print(f"Python 執行檔: {sys.executable}")
print(f"當前目錄: {os.getcwd()}")
print()

print("=== 檢查必要套件 ===")

packages = {
    'tkinter': 'GUI 框架',
    'pandas': '資料處理',
    'numpy': '數值運算',
    'folium': '地圖產生',
    'selenium': '網頁自動化',
    'PIL': '圖片處理 (Pillow)',
    'geopy': '地理座標計算',
    'openpyxl': 'Excel 處理',
    'requests': 'HTTP 請求'
}

missing = []
installed = []

for package, description in packages.items():
    try:
        if package == 'PIL':
            from PIL import Image
        elif package == 'tkinter':
            import tkinter
        else:
            __import__(package)
        installed.append(f"✓ {package} ({description})")
    except ImportError:
        missing.append(f"✗ {package} ({description})")

print("\n已安裝的套件:")
for item in installed:
    print(f"  {item}")

if missing:
    print("\n缺少的套件:")
    for item in missing:
        print(f"  {item}")
    
    print("\n安裝指令:")
    print("pip install pandas folium selenium pillow geopy openpyxl requests")
    
    if 'tkinter' in str(missing):
        print("\n注意: tkinter 需要特別安裝")
        print("macOS: brew install python-tk")
        print("Ubuntu/Debian: sudo apt-get install python3-tk")
else:
    print("\n✓ 所有套件都已安裝！")

print("\n=== 測試主程式 ===")
main_script = "travel_distance_calculator_gui_cached_efficient.py"
if os.path.exists(main_script):
    print(f"✓ 找到主程式: {main_script}")
    
    # 檢查是否可以匯入主程式
    try:
        with open(main_script, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if first_line.startswith('#!'):
                print(f"✓ Shebang 行存在: {first_line}")
            else:
                print("✗ 缺少 Shebang 行")
    except Exception as e:
        print(f"✗ 無法讀取主程式: {e}")
else:
    print(f"✗ 找不到主程式: {main_script}")

print("\n如果所有檢查都通過，請執行:")
print(f"python3 {main_script}")
