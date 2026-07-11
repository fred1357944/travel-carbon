#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試 Tkinter 是否正常工作
"""

import sys

try:
    import tkinter as tk
    print("✓ tkinter 套件已成功匯入")
    
    # 建立簡單的測試視窗
    root = tk.Tk()
    root.title("Tkinter 測試")
    root.geometry("400x200")
    
    label = tk.Label(root, text="如果您看到這個視窗，表示 Tkinter 正常工作！", 
                     font=("Arial", 14), pady=20)
    label.pack()
    
    button = tk.Button(root, text="關閉", command=root.quit, 
                       bg="lightblue", padx=20, pady=10)
    button.pack()
    
    print("✓ 測試視窗已建立")
    print("✓ 正在啟動視窗...")
    
    root.mainloop()
    
    print("✓ Tkinter 測試完成")
    
except ImportError as e:
    print(f"✗ 無法匯入 tkinter: {e}")
    print("\n可能的解決方案：")
    print("1. 如果使用 macOS，請確保已安裝 python3-tk:")
    print("   brew install python-tk")
    print("2. 如果使用 Linux，請安裝:")
    print("   sudo apt-get install python3-tk")
    print("3. 確保使用正確的 Python 環境")
    
except Exception as e:
    print(f"✗ 發生錯誤: {e}")
    import traceback
    traceback.print_exc()
