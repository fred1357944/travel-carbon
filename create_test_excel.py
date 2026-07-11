#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os

# 建立測試資料
test_data = {
    '序號': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    '傳票編號': [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010],
    '出差地點': [
        '日本',
        '韓國', 
        '新加坡',
        '泰國',
        '美國',
        '德國',
        '澳洲',
        '印度',
        '巴西',
        '南非'
    ],
    '出差事由': ['國際會議'] * 10
}

# 建立 DataFrame
df = pd.DataFrame(test_data)

# 儲存為 Excel 檔案
output_file = '國際航線測試資料.xlsx'
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"Excel 檔案已建立：{output_file}")
