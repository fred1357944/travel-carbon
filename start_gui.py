#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI 啟動腳本
"""

import os
import sys
import subprocess

def main():
    print("正在啟動出差距離計算與地圖產生工具...")
    
    # 確保在正確的目錄
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    
    # 啟動主程式
    script_path = os.path.join(current_dir, "travel_distance_calculator_gui_cached_efficient.py")
    
    if not os.path.exists(script_path):
        print(f"錯誤：找不到主程式檔案 {script_path}")
        return
    
    # 執行程式
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"程式執行失敗: {e}")
    except KeyboardInterrupt:
        print("\n程式已被使用者中斷")
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    main()
