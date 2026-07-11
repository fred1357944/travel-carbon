#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試地理智能對應功能
"""

# 從主程式匯入必要的常數和函數
import sys
sys.path.append('/Users/laihongyi/Downloads/差旅費')

from travel_distance_calculator_gui_cached_efficient import COORDINATES, REGION_MAPPING, CHINA_KEYWORDS

def test_smart_destination():
    """測試智能地名處理"""
    
    print("=== 測試地理智能對應功能 ===\n")
    
    # 測試案例
    test_cases = [
        # 台灣地區測試
        ("南港", "預期對應到台北"),
        ("台北市南港區", "預期對應到南港，然後對應到台北"),
        ("新北市板橋區", "預期對應到板橋，然後對應到新北"),
        ("台北市信義區", "預期對應到信義，然後對應到台北"),
        
        # 中國城市測試
        ("杭州", "預期對應到杭州機場"),
        ("浙江省杭州市", "預期對應到杭州機場"),
        ("蘇州", "預期對應到上海機場（最近）"),
        ("江蘇省蘇州市", "預期對應到上海機場"),
        ("無錫", "預期對應到上海機場"),
        ("佛山", "預期對應到廣州機場"),
        ("廣東省佛山市", "預期對應到廣州機場"),
        
        # 國際城市測試
        ("東京", "預期對應到日本（成田機場）"),
        ("首爾", "預期對應到韓國（仁川機場）"),
        ("紐約", "預期無對應（需要新增）"),
    ]
    
    # 執行測試
    for destination, expected in test_cases:
        print(f"測試地點: {destination}")
        print(f"期望結果: {expected}")
        
        # 檢查是否在 COORDINATES 中
        if destination in COORDINATES:
            coord = COORDINATES[destination]
            print(f"✓ 直接找到座標: {coord['name']}")
        elif destination in REGION_MAPPING:
            mapped = REGION_MAPPING[destination]
            print(f"✓ 找到對應關係: {destination} -> {mapped}")
            if mapped in COORDINATES:
                coord = COORDINATES[mapped]
                print(f"  對應座標: {coord['name']}")
        else:
            print(f"✗ 找不到對應")
            
            # 嘗試智能處理
            processed = smart_destination_handler(destination)
            if processed != destination:
                print(f"  智能處理後: {destination} -> {processed}")
                if processed in COORDINATES:
                    coord = COORDINATES[processed]
                    print(f"  ✓ 找到座標: {coord['name']}")
                elif processed in REGION_MAPPING:
                    mapped = REGION_MAPPING[processed]
                    print(f"  ✓ 找到對應關係: {processed} -> {mapped}")
        
        print("-" * 50)

def smart_destination_handler(destination):
    """智能處理目的地名稱（簡化版）"""
    # 移除常見的地名後綴
    suffixes_to_remove = ['市', '縣', '區', '鎮', '鄉', '街', '路', '段']
    for suffix in suffixes_to_remove:
        if destination.endswith(suffix):
            destination = destination[:-len(suffix)]
            
    # 處理特殊情況
    # 例如："台北市南港區" -> "南港"
    for region, parent in REGION_MAPPING.items():
        if region in destination and parent in destination:
            return region
            
    # 處理中國城市的省份問題
    china_provinces = ['浙江', '江蘇', '廣東', '福建', '山東', '河北', '河南', 
                      '湖北', '湖南', '四川', '陕西', '山西', '遼寧', '吉林', 
                      '黑龍江', '安徽', '江西', '雲南', '貴州', '甘肅', '青海']
    
    for province in china_provinces:
        if province in destination:
            # 找出省份後的城市名
            for city in CHINA_KEYWORDS:
                if city in destination:
                    return city
                    
    return destination

def show_statistics():
    """顯示資料庫統計"""
    print("\n=== 資料庫統計 ===")
    
    # 統計各類型座標
    domestic_count = sum(1 for coord in COORDINATES.values() if coord['type'] == 'domestic')
    international_count = sum(1 for coord in COORDINATES.values() if coord['type'] == 'international')
    airport_count = sum(1 for coord in COORDINATES.values() if coord['type'] == 'airport')
    
    print(f"國內地點: {domestic_count} 個")
    print(f"國際機場: {international_count} 個")
    print(f"機場轉運站: {airport_count} 個")
    print(f"總計: {len(COORDINATES)} 個座標點")
    
    print(f"\n地區對應關係: {len(REGION_MAPPING)} 個")
    print(f"中國城市關鍵字: {len(CHINA_KEYWORDS)} 個")
    
    # 顯示部分對應關係
    print("\n=== 地區對應範例 ===")
    count = 0
    for region, parent in REGION_MAPPING.items():
        if count < 10:
            print(f"{region} -> {parent}")
            count += 1
        else:
            print(f"... 還有 {len(REGION_MAPPING) - 10} 個對應關係")
            break

def test_is_domestic(destination):
    """測試國內外判斷邏輯"""
    # 台灣縣市列表
    taiwan_cities = ['台北', '臺北', '新北', '桃園', '新竹', '苗栗', '台中', '臺中', 
                    '彰化', '南投', '雲林', '嘉義', '台南', '臺南', '高雄', '屏東',
                    '宜蘭', '花蓮', '台東', '臺東', '基隆', '澎湖', '金門', '馬祖']
    
    # 台灣地區關鍵字
    taiwan_regions = list(REGION_MAPPING.keys())
    
    # 檢查是否為台灣地點
    is_taiwan = any(city in destination for city in taiwan_cities) or \
               any(region in destination for region in taiwan_regions)
    
    # 檢查是否為中國城市
    is_china = any(city in destination for city in CHINA_KEYWORDS)
    
    # 如果是中國城市，視為國際
    if is_china:
        return False
        
    return is_taiwan

def test_destination_types():
    """測試各種目的地類型的判斷"""
    print("\n=== 測試目的地類型判斷 ===")
    
    test_destinations = [
        "台北",
        "南港",
        "台北市南港區",
        "杭州",
        "浙江省杭州市",
        "東京",
        "紐約",
        "板橋",
        "新北市板橋區",
        "蘇州工業園區",
    ]
    
    for dest in test_destinations:
        is_domestic = test_is_domestic(dest)
        print(f"{dest:20} -> {'國內' if is_domestic else '國際'}")

if __name__ == "__main__":
    # 執行測試
    test_smart_destination()
    show_statistics()
    test_destination_types()
    
    print("\n測試完成！")
