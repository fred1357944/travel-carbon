import pandas as pd
import re
import os

def extract_locations(text):
    """從文字中提取出差地點"""
    if pd.isna(text):
        return ''
    
    # 清理亂碼
    text = re.sub(r'[䀭닌ꆟ㝤䀔鶿篸캄ꇀ㝤Ž⸽䀋纡鸐]', '', str(text))
    
    # 地點模式
    patterns = [
        # 國內城市
        r'赴?(台北|臺北|新北|台中|臺中|台南|臺南|高雄|基隆|新竹|苗栗|彰化|南投|雲林|嘉義|屏東|宜蘭|花蓮|台東|臺東|澎湖|金門|馬祖|桃園)',
        # 國外地點
        r'赴?(美國|日本|韓國|新加坡|馬來西亞|泰國|越南|印尼|菲律賓|香港|澳門|大陸|中國|英國|法國|德國|澳洲|紐西蘭|加拿大|義大利|西班牙|荷蘭|比利時|瑞士|奧地利|印度|巴西|墨西哥|俄羅斯|南非|埃及|以色列|土耳其|阿聯酋)'
    ]
    
    locations = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if match not in locations:
                locations.append(match)
    
    return '、'.join(locations)

# 取得當前資料夾路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, '113年度碳排放量純差旅4.xlsx')

# 檢查檔案是否存在
if not os.path.exists(file_path):
    print(f"找不到檔案：{file_path}")
    print(f"請確認檔案 '113年度碳排放量純差旅4.xlsx' 位於：{current_dir}")
    exit()

try:
    # 讀取Excel檔案
    print("正在讀取檔案...")
    df = pd.read_excel(file_path, sheet_name=0)
    print(f"成功讀取檔案，共有 {len(df)} 列資料")
    
    # 顯示欄位資訊
    print(f"欄位數量：{len(df.columns)}")
    print(f"欄位名稱：{list(df.columns)}")
    
    # 建立結果dataframe
    result_df = pd.DataFrame()
    
    # 處理資料
    if len(df.columns) >= 3:
        result_df['序號'] = df.iloc[:, 0]
        result_df['傳票編號'] = df.iloc[:, 1]
        
        # 提取出差地點
        print("正在分析出差地點...")
        result_df['出差地點'] = df.iloc[:, 2].apply(extract_locations)
    else:
        print("檔案格式不符預期，嘗試使用第一個欄位作為摘要")
        # 如果欄位結構不同，嘗試其他方式
        result_df['序號'] = range(1, len(df) + 1)
        result_df['傳票編號'] = df.iloc[:, 0] if len(df.columns) > 0 else ''
        result_df['出差地點'] = df.iloc[:, 1].apply(extract_locations) if len(df.columns) > 1 else ''
    
    # 輸出結果
    output_path = os.path.join(current_dir, '出差地點整理結果.xlsx')
    result_df.to_excel(output_path, index=False)
    
    print(f"\n處理完成！")
    print(f"共處理 {len(result_df)} 筆資料")
    print(f"有出差地點的資料：{(result_df['出差地點'] != '').sum()} 筆")
    print(f"無出差地點的資料：{(result_df['出差地點'] == '').sum()} 筆")
    print(f"\n結果已儲存至：{output_path}")
    
    # 顯示前10筆結果預覽
    print("\n前10筆資料預覽：")
    for idx, row in result_df.head(10).iterrows():
        location = row['出差地點'] if row['出差地點'] else '(無出差地點)'
        print(f"{row['序號']}: {row['傳票編號']} - {location}")
        
except Exception as e:
    print(f"處理過程中發生錯誤：{e}")
    print("\n請檢查：")
    print("1. Excel檔案是否正確")
    print("2. 檔案是否已損壞")
    print("3. 是否安裝了必要的套件（pandas, openpyxl）")