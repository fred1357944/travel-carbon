#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import openpyxl
import os

# 建立測試資料
data = {
    '序號': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    '傳票編號': [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010],
    '出差地點': ['日本', '韓國', '新加坡', '泰國', '美國', '德國', '澳洲', '印度', '巴西', '南非'],
    '出差事由': ['國際會議'] * 10
}

# 建立 DataFrame
df = pd.DataFrame(data)

# 設定檔案路徑
file_path = os.path.expanduser('~/Downloads/差旅費/國際航線測試資料.xlsx')

# 寫入 Excel 檔案
with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='國際航線測試', index=False)
    
    # 取得工作表
    workbook = writer.book
    worksheet = writer.sheets['國際航線測試']
    
    # 調整欄寬
    worksheet.column_dimensions['A'].width = 10  # 序號
    worksheet.column_dimensions['B'].width = 15  # 傳票編號
    worksheet.column_dimensions['C'].width = 20  # 出差地點
    worksheet.column_dimensions['D'].width = 20  # 出差事由

print(f"Excel 檔案已成功建立：{file_path}")
print("\n檔案內容：")
print(df.to_string(index=False))
print("\n測試說明：")
print("1. 使用主程式載入此檔案")
print("2. 設定處理範圍 1-10")
print("3. 執行計算距離、產生地圖、匯出Excel")
print("\n預期結果：")
print("- 所有路線從桃園機場出發")
print("- 地圖顯示橘色弧形飛行路線")
print("- 根據距離自動調整地圖縮放級別")
