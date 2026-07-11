#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用新進程啟動 GUI - 解決視窗不顯示問題
"""

import subprocess
import sys
import os

def main():
    print("使用新進程啟動 GUI...")
    
    # 確保在正確的目錄
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 選擇要啟動的腳本
    scripts = [
        "travel_distance_calculator_gui_cached.py",
        "travel_distance_calculator_gui_cached_efficient.py"
    ]
    
    # 找到存在的腳本
    script_to_run = None
    for script in scripts:
        if os.path.exists(script):
            script_to_run = script
            break
    
    if not script_to_run:
        print("錯誤：找不到主程式檔案")
        return
    
    print(f"正在啟動: {script_to_run}")
    
    # 使用 subprocess 在新的進程中啟動
    try:
        # 在 macOS 上，使用 pythonw 可以更好地顯示 GUI
        if sys.platform == 'darwin':
            # 嘗試使用 pythonw
            try:
                subprocess.run(['pythonw', script_to_run], check=True)
            except FileNotFoundError:
                # 如果沒有 pythonw，使用普通 python
                subprocess.run([sys.executable, script_to_run], check=True)
        else:
            # 其他平台使用普通 python
            subprocess.run([sys.executable, script_to_run], check=True)
            
    except subprocess.CalledProcessError as e:
        print(f"程式執行失敗: {e}")
    except KeyboardInterrupt:
        print("\n程式已被使用者中斷")
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    main()
