#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
強制顯示 GUI 視窗的啟動腳本
"""

import sys
import os
import time

def force_show_gui():
    """強制顯示 GUI 視窗"""
    print("正在強制啟動 GUI...")
    
    # 確保我們在正確的目錄
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 使用較為激進的方式啟動 tkinter
    import tkinter as tk
    
    # 建立一個臨時視窗來「喚醒」GUI系統
    print("初始化 GUI 系統...")
    temp_root = tk.Tk()
    temp_root.withdraw()  # 隱藏臨時視窗
    temp_root.update()
    temp_root.destroy()
    
    print("GUI 系統已就緒")
    time.sleep(0.5)
    
    # 現在啟動真正的應用程式
    print("\n正在啟動主程式...")
    
    # 匯入並執行主程式
    try:
        # 重新匯入以確保最新版本
        if 'travel_distance_calculator_gui_cached' in sys.modules:
            del sys.modules['travel_distance_calculator_gui_cached']
            
        from travel_distance_calculator_gui_cached import TravelDistanceCalculator
        
        # 創建應用程式實例
        app = TravelDistanceCalculator()
        
        # 強制顯示主視窗
        app.root.update()
        app.root.deiconify()
        app.root.lift()
        app.root.focus_force()
        
        # 在 macOS 上特別處理
        if sys.platform == 'darwin':
            app.root.attributes('-topmost', True)
            app.root.update()
            time.sleep(0.1)
            app.root.attributes('-topmost', False)
            
            # 嘗試將應用程式帶到前台
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
        
        print("✓ 視窗應該已經顯示")
        print("\n如果還是看不到視窗：")
        print("- 檢查 Dock (macOS) 或工作列 (Windows)")
        print("- 使用 Cmd+Tab (macOS) 或 Alt+Tab (Windows) 切換")
        print("- 檢查是否有對話框需要回應")
        
        # 執行主循環
        app.run()
        
    except Exception as e:
        print(f"\n錯誤：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    force_show_gui()
