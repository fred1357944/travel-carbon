import openpyxl
import re
import os

def extract_locations(text):
    """從文字中提取出差地點"""
    if not text:
        return ''
    
    # 轉換為字串並清理亂碼
    text = str(text)
    text = re.sub(r'[䀭닌ꆟ㝤䀔鶿篸캄ꇀ㝤Ž⸽䀋纡鸐]', '', text)
    
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
    # 使用openpyxl讀取Excel檔案
    print("正在讀取Excel檔案...")
    workbook = openpyxl.load_workbook(file_path, data_only=True)
    
    # 取得第一個工作表
    sheet = workbook.active
    print(f"工作表名稱：{sheet.title}")
    
    # 取得所有資料
    all_data = list(sheet.values)
    print(f"總共有 {len(all_data)} 列資料")
    
    # 創建新的工作簿
    new_workbook = openpyxl.Workbook()
    new_sheet = new_workbook.active
    new_sheet.title = "出差地點整理"
    
    # 寫入標題
    new_sheet.append(['序號', '傳票編號', '出差地點'])
    
    # 處理資料（跳過標題列）
    location_count = 0
    no_location_count = 0
    
    for idx, row in enumerate(all_data[1:], start=1):
        if row and len(row) >= 3:
            seq_num = row[0] or idx
            voucher_no = row[1] or ''
            summary = row[2] or ''
            
            # 提取出差地點
            locations = extract_locations(summary)
            
            if locations:
                location_count += 1
            else:
                no_location_count += 1
            
            # 寫入新工作表
            new_sheet.append([seq_num, voucher_no, locations])
            
            # 顯示進度
            if idx % 100 == 0:
                print(f"已處理 {idx} 筆資料...")
    
    # 調整欄寬
    new_sheet.column_dimensions['A'].width = 10
    new_sheet.column_dimensions['B'].width = 20
    new_sheet.column_dimensions['C'].width = 40
    
    # 儲存檔案
    output_path = os.path.join(current_dir, '出差地點整理結果.xlsx')
    new_workbook.save(output_path)
    
    print(f"\n處理完成！")
    print(f"共處理 {idx} 筆資料")
    print(f"有出差地點的資料：{location_count} 筆")
    print(f"無出差地點的資料：{no_location_count} 筆")
    print(f"\n結果已儲存至：{output_path}")
    
    # 關閉工作簿
    workbook.close()
    new_workbook.close()
    
except Exception as e:
    print(f"處理過程中發生錯誤：{e}")
    print("\n可能的原因：")
    print("1. Excel檔案損壞或格式不正確")
    print("2. 缺少必要的套件（請執行：pip install openpyxl）")
    print("3. 檔案正在被其他程式使用")