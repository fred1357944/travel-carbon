import re
import pandas as pd
import os
import requests
import folium
from geopy.distance import geodesic
import time

# 座標資料庫（簡化版）
COORDINATES = {
    # 起點
    '輔仁大學': {'lat': 25.0356, 'lon': 121.4320, 'name': '輔仁大學正門'},
    # 台灣主要城市
    '台北': {'lat': 25.0330, 'lon': 121.5654, 'name': '台北市政府'},
    '臺北': {'lat': 25.0330, 'lon': 121.5654, 'name': '台北市政府'},
    '新北': {'lat': 25.0119, 'lon': 121.4653, 'name': '新北市政府'},
    '桃園': {'lat': 24.9936, 'lon': 121.3010, 'name': '桃園市政府'},
    '新竹': {'lat': 24.8138, 'lon': 120.9675, 'name': '新竹市政府'},
    '台中': {'lat': 24.1639, 'lon': 120.6478, 'name': '台中市政府'},
    '臺中': {'lat': 24.1639, 'lon': 120.6478, 'name': '台中市政府'},
    '台南': {'lat': 22.9997, 'lon': 120.2269, 'name': '台南市政府'},
    '臺南': {'lat': 22.9997, 'lon': 120.2269, 'name': '台南市政府'},
    '高雄': {'lat': 22.6273, 'lon': 120.3014, 'name': '高雄市政府'},
    '宜蘭': {'lat': 24.7021, 'lon': 121.7377, 'name': '宜蘭縣政府'},
    '花蓮': {'lat': 23.9871, 'lon': 121.6015, 'name': '花蓮縣政府'},
    '台東': {'lat': 22.7972, 'lon': 121.0713, 'name': '台東縣政府'},
    '臺東': {'lat': 22.7972, 'lon': 121.0713, 'name': '台東縣政府'},
    # 機場
    '桃園機場': {'lat': 25.0777, 'lon': 121.2325, 'name': '桃園國際機場'},
    # 國際主要機場
    '日本': {'lat': 35.5494, 'lon': 139.7798, 'name': '成田國際機場'},
    '韓國': {'lat': 37.4602, 'lon': 126.4407, 'name': '仁川國際機場'},
    '美國': {'lat': 33.9425, 'lon': -118.4081, 'name': '洛杉磯國際機場'},
    '德國': {'lat': 50.0379, 'lon': 8.5622, 'name': '法蘭克福機場'},
    '迦納': {'lat': 5.6052, 'lon': -0.1668, 'name': '科托卡國際機場'},
    '澳洲': {'lat': -33.9399, 'lon': 151.1753, 'name': '雪梨機場'},
    '泰國': {'lat': 13.6900, 'lon': 100.7501, 'name': '素萬那普機場'},
    '印尼': {'lat': -6.1256, 'lon': 106.6559, 'name': '蘇加諾哈達機場'},
}

def calculate_distance(origin, destination, travel_type='driving'):
    """計算兩點間的距離"""
    if travel_type == 'driving':
        # 嘗試使用OSRM API獲取實際路線
        try:
            url = f"http://router.project-osrm.org/route/v1/driving/{origin['lon']},{origin['lat']};{destination['lon']},{destination['lat']}"
            response = requests.get(url, params={'overview': 'false'}, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data['code'] == 'Ok':
                    distance_km = round(data['routes'][0]['distance'] / 1000, 1)
                    duration_min = round(data['routes'][0]['duration'] / 60)
                    return distance_km, f"{duration_min}分鐘"
        except:
            pass
        
        # 如果API失敗，使用直線距離估算
        coords_1 = (origin['lat'], origin['lon'])
        coords_2 = (destination['lat'], destination['lon'])
        distance_km = round(geodesic(coords_1, coords_2).kilometers * 1.4, 1)
        duration_min = round(distance_km * 1.5)
        return distance_km, f"{duration_min}分鐘"
    
    else:  # flying
        coords_1 = (origin['lat'], origin['lon'])
        coords_2 = (destination['lat'], destination['lon'])
        distance_km = round(geodesic(coords_1, coords_2).kilometers, 1)
        flight_hours = distance_km / 800 + 0.5
        return distance_km, f"{flight_hours:.1f}小時"

def extract_locations_ai(text):
    """使用AI級別的地點識別"""
    if not text or pd.isna(text):
        return ''
    
    # 清理亂碼
    text = str(text)
    text = re.sub(r'[䀭닌ꆟ㝤䀔鶿篸캄ꇀ㝤Ž⸽䀋纡鸐]', '', text)
    
    locations = []
    
    # 超完整的地點清單
    all_locations = [
        # === 台灣地區 ===
        '台北', '臺北', '新北', '台中', '臺中', '台南', '臺南', '高雄', '基隆', 
        '新竹', '苗栗', '彰化', '南投', '雲林', '嘉義', '屏東', '宜蘭', '花蓮', 
        '台東', '臺東', '澎湖', '金門', '馬祖', '桃園', '竹北', '板橋', '中壢',
        '三重', '永和', '新店', '土城', '蘆洲', '汐止', '樹林', '三峽', '淡水',
        
        # === 亞洲國家/城市 ===
        # 東亞
        '日本', '東京', '大阪', '京都', '名古屋', '福岡', '札幌', '仙台', '橫濱', '神戶', '奈良',
        '韓國', '首爾', '釜山', '大邱', '仁川', '光州', '大田', '蔚山', '濟州',
        '中國', '大陸', '北京', '上海', '廣州', '深圳', '成都', '杭州', '南京', '西安', '武漢', '重慶',
        '香港', '澳門', '蒙古', '烏蘭巴托',
        
        # 東南亞
        '新加坡', '馬來西亞', '吉隆坡', '檳城', '新山', '馬六甲',
        '泰國', '曼谷', '清邁', '普吉島', '芭達雅', '蘇梅島',
        '越南', '河內', '胡志明市', '峴港', '芽莊', '大叻',
        '印尼', '雅加達', '峇里島', '泗水', '萬隆', '棉蘭',
        '菲律賓', '馬尼拉', '宿霧', '長灘島', '達沃', '碧瑤',
        '柬埔寨', '金邊', '暹粒', '吳哥窟',
        '寮國', '永珍', '龍坡邦',
        '緬甸', '仰光', '曼德勒', '蒲甘',
        '汶萊', '斯里巴加灣市',
        '東帝汶', '帝力',
        
        # 南亞
        '印度', '新德里', '孟買', '加爾各答', '清奈', '班加羅爾',
        '巴基斯坦', '伊斯蘭堡', '卡拉奇', '拉合爾',
        '孟加拉', '達卡', '吉大港',
        '斯里蘭卡', '可倫坡', '康提',
        '尼泊爾', '加德滿都', '博克拉',
        '不丹', '廷布',
        '馬爾地夫', '馬列',
        
        # 中亞
        '哈薩克', '阿斯塔納', '阿拉木圖',
        '烏茲別克', '塔什干', '撒馬爾罕',
        '土庫曼', '阿什哈巴德',
        '吉爾吉斯', '比什凱克',
        '塔吉克', '杜尚別',
        '阿富汗', '喀布爾',
        
        # === 歐洲國家/城市 ===
        '英國', '倫敦', '曼徹斯特', '愛丁堡', '伯明罕', '利物浦', '格拉斯哥',
        '法國', '巴黎', '馬賽', '里昂', '尼斯', '波爾多',
        '德國', '柏林', '慕尼黑', '漢堡', '科隆', '法蘭克福',
        '義大利', '羅馬', '米蘭', '威尼斯', '佛羅倫斯', '那不勒斯',
        '西班牙', '馬德里', '巴塞隆納', '瓦倫西亞', '塞維亞',
        '葡萄牙', '里斯本', '波爾圖',
        '荷蘭', '阿姆斯特丹', '鹿特丹', '海牙',
        '比利時', '布魯塞爾', '安特衛普',
        '瑞士', '蘇黎世', '日內瓦', '伯恩', '巴塞爾',
        '奧地利', '維也納', '薩爾茨堡', '因斯布魯克',
        '瑞典', '斯德哥爾摩', '哥德堡', '馬爾默',
        '挪威', '奧斯陸', '卑爾根',
        '丹麥', '哥本哈根', '奧胡斯',
        '芬蘭', '赫爾辛基', '圖爾庫',
        '冰島', '雷克雅維克',
        '愛爾蘭', '都柏林', '科克',
        '波蘭', '華沙', '克拉科夫',
        '捷克', '布拉格', '布爾諾',
        '匈牙利', '布達佩斯',
        '羅馬尼亞', '布加勒斯特',
        '保加利亞', '索菲亞',
        '希臘', '雅典', '塞薩洛尼基',
        '克羅埃西亞', '札格雷布', '杜布羅夫尼克',
        '塞爾維亞', '貝爾格勒',
        '斯洛伐克', '布拉提斯拉瓦',
        '斯洛維尼亞', '盧比安納',
        '愛沙尼亞', '塔林',
        '拉脫維亞', '里加',
        '立陶宛', '維爾紐斯',
        '烏克蘭', '基輔', '哈爾科夫',
        '俄羅斯', '莫斯科', '聖彼得堡',
        
        # === 美洲國家/城市 ===
        # 北美
        '美國', '紐約', '洛杉磯', '芝加哥', '休士頓', '費城', '鳳凰城', 
        '聖安東尼奧', '聖地牙哥', '達拉斯', '聖荷西', '奧斯汀', '舊金山', 
        '西雅圖', '波士頓', '華盛頓', '邁阿密', '亞特蘭大', '拉斯維加斯', 
        '丹佛', '底特律', '波特蘭', '夏威夷', '檀香山',
        '加拿大', '多倫多', '溫哥華', '蒙特婁', '卡加利', '渥太華', '愛民頓',
        '墨西哥', '墨西哥城', '瓜達拉哈拉', '蒙特雷', '坎昆', '提華納',
        
        # 中美洲
        '瓜地馬拉', '貝里斯', '薩爾瓦多', '宏都拉斯', '尼加拉瓜', '哥斯大黎加', '巴拿馬',
        
        # 加勒比海
        '古巴', '哈瓦那', '牙買加', '金斯敦', '海地', '多明尼加', '聖多明哥',
        '波多黎各', '聖胡安', '巴哈馬', '拿騷', '巴貝多', '千里達',
        
        # 南美洲
        '巴西', '聖保羅', '里約', '巴西利亞', '薩爾瓦多',
        '阿根廷', '布宜諾斯艾利斯', '科爾多瓦',
        '智利', '聖地牙哥', '瓦爾帕萊索',
        '秘魯', '利馬', '庫斯科',
        '哥倫比亞', '波哥大', '麥德林',
        '委內瑞拉', '卡拉卡斯',
        '厄瓜多', '基多', '瓜亞基爾',
        '玻利維亞', '拉巴斯', '蘇克雷',
        '巴拉圭', '亞松森',
        '烏拉圭', '蒙得維的亞',
        '蘇利南', '帕拉馬里博',
        '蓋亞那', '喬治敦',
        '法屬圭亞那', '開雲',
        
        # === 非洲國家/城市 ===
        # 北非
        '埃及', '開羅', '亞歷山大', '路克索', '亞斯文',
        '利比亞', '的黎波里', '班加西',
        '突尼西亞', '突尼斯',
        '阿爾及利亞', '阿爾及爾',
        '摩洛哥', '拉巴特', '卡薩布蘭卡', '馬拉喀什',
        
        # 西非
        '奈及利亞', '拉哥斯', '阿布賈',
        '迦納', '阿克拉', '庫馬西',
        '塞內加爾', '達喀爾',
        '象牙海岸', '阿必尚', '雅穆索戈',
        '布吉納法索', '瓦加杜古',
        '馬利', '巴馬科',
        '尼日', '尼阿美',
        '幾內亞', '柯那克里',
        '獅子山', '自由城',
        '賴比瑞亞', '蒙羅維亞',
        '多哥', '洛美',
        '貝南', '波多諾伏',
        '甘比亞', '班竹',
        '幾內亞比索', '比紹',
        '茅利塔尼亞', '諾克少',
        '維德角', '培亞',
        
        # 東非
        '衣索比亞', '阿迪斯阿貝巴',
        '肯亞', '奈洛比', '蒙巴薩',
        '坦尚尼亞', '三蘭港', '杜篤瑪',
        '烏干達', '坎帕拉',
        '盧安達', '吉佳利',
        '蒲隆地', '布松布拉',
        '索馬利亞', '摩加迪休',
        '吉布地', '吉布地市',
        '厄利垂亞', '阿斯馬拉',
        '南蘇丹', '朱巴',
        '蘇丹', '喀土穆',
        
        # 中非
        '剛果民主共和國', '金夏沙',
        '剛果共和國', '布拉薩',
        '中非共和國', '班基',
        '查德', '恩將納',
        '喀麥隆', '雅溫德', '杜阿拉',
        '加彭', '利伯維爾',
        '赤道幾內亞', '馬拉博',
        '聖多美普林西比', '聖多美',
        
        # 南非
        '南非', '約翰尼斯堡', '開普敦', '德班', '普利托利亞',
        '辛巴威', '哈拉雷',
        '尚比亞', '路沙卡',
        '波札那', '嘉柏隆里',
        '納米比亞', '溫得和克',
        '莫三比克', '馬布多',
        '馬拉威', '里朗威',
        '安哥拉', '羅安達',
        '史瓦帝尼', '墨巴本',
        '賴索托', '馬塞魯',
        '馬達加斯加', '安塔那那利佛',
        '模里西斯', '路易港',
        '塞席爾', '維多利亞',
        '葛摩', '莫洛尼',
        
        # === 大洋洲國家/城市 ===
        '澳洲', '雪梨', '墨爾本', '布里斯本', '伯斯', '阿德萊德', '坎培拉', '達爾文',
        '紐西蘭', '奧克蘭', '威靈頓', '基督城', '皇后鎮',
        '斐濟', '蘇瓦',
        '巴布亞紐幾內亞', '莫士比港',
        '索羅門群島', '荷尼阿拉',
        '萬那杜', '維拉港',
        '薩摩亞', '阿庇亞',
        '東加', '努瓜婁發',
        '帛琉', '恩吉魯穆德',
        '馬紹爾群島', '馬朱羅',
        '密克羅尼西亞', '帕利基爾',
        '諾魯', '亞倫',
        '吉里巴斯', '南塔拉瓦',
        '吐瓦魯', '富納富提',
        
        # === 中東國家/城市 ===
        '以色列', '耶路撒冷', '特拉維夫', '海法',
        '土耳其', '伊斯坦堡', '安卡拉', '伊茲密爾',
        '阿聯酋', '杜拜', '阿布達比', '沙迦',
        '沙烏地阿拉伯', '利雅德', '吉達', '麥加',
        '卡達', '多哈',
        '科威特', '科威特市',
        '巴林', '麥納瑪',
        '阿曼', '馬斯喀特',
        '約旦', '安曼',
        '黎巴嫩', '貝魯特',
        '敘利亞', '大馬士革',
        '伊拉克', '巴格達',
        '伊朗', '德黑蘭',
        '葉門', '沙那',
        '亞美尼亞', '葉里溫',
        '喬治亞', '提比里斯',
        '亞塞拜然', '巴庫'
    ]
    
    # 搜尋所有可能的地點
    for location in all_locations:
        if location in text:
            if location not in locations:
                locations.append(location)
    
    # 特殊模式匹配
    patterns = [
        r'[至赴往去到前飛]([^\s，。、,\.]{2,6})[參出會議務學習招考察訪問交流洽談]',
        r'前往([^\s，。、,\.]{2,6})',
        r'飛[往至]([^\s，。、,\.]{2,6})',
        r'([^\s，。、,\.]{2,6})[分公司|辦事處|分校|校區|大學|學院]',
        r'在([^\s，。、,\.]{2,6})[舉辦行參出席]',
        r'([^\s，。、,\.]{2,6})出差',
        r'出差[到至]([^\s，。、,\.]{2,6})'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            # 檢查是否為中文地名
            if match and re.search(r'[\u4e00-\u9fa5]', match) and len(match) >= 2:
                # 過濾掉明顯不是地名的詞
                if not any(word in match for word in ['會議', '計畫', '活動', '研討', '論壇', '展覽', '招生', '學習']):
                    if match not in locations:
                        locations.append(match)
    
    return '、'.join(locations)

def is_domestic(location):
    """判斷是否為國內地點"""
    taiwan_cities = ['台北', '臺北', '新北', '桃園', '新竹', '苗栗', '台中', '臺中', 
                    '彰化', '南投', '雲林', '嘉義', '台南', '臺南', '高雄', '屏東',
                    '宜蘭', '花蓮', '台東', '臺東', '基隆', '澎湖', '金門', '馬祖']
    return any(city in location for city in taiwan_cities)

# 主程式
def process_travel_data(calculate_distances=False, start_row=1, end_row=None):
    # 取得當前資料夾路徑
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '113年度碳排放量純差旅4.xlsx')
    
    # 檢查檔案是否存在
    if not os.path.exists(file_path):
        print(f"找不到檔案：{file_path}")
        return
    
    try:
        # 讀取Excel檔案
        print("正在使用AI分析出差地點...")
        df = pd.read_excel(file_path, sheet_name=0)
        
        # 建立結果dataframe
        result_df = pd.DataFrame()
        
        # 處理資料
        if len(df.columns) >= 3:
            result_df['序號'] = df.iloc[:, 0]
            result_df['傳票編號'] = df.iloc[:, 1]
            
            # 使用AI提取出差地點
            result_df['出差地點'] = df.iloc[:, 2].apply(extract_locations_ai)
            
            # 如果需要計算距離
            if calculate_distances:
                print("\n正在計算距離...")
                distances = []
                times = []
                types = []
                
                # 選擇處理範圍
                if end_row:
                    process_df = result_df.iloc[start_row-1:end_row]
                else:
                    process_df = result_df
                
                for idx, row in process_df.iterrows():
                    if row['出差地點']:
                        destinations = row['出差地點'].split('、')
                        destination = destinations[0]  # 取第一個目的地
                        
                        if is_domestic(destination) and destination in COORDINATES:
                            # 國內：從輔大開車
                            origin = COORDINATES['輔仁大學']
                            dest = COORDINATES[destination]
                            dist, dur = calculate_distance(origin, dest, 'driving')
                            distances.append(dist)
                            times.append(dur)
                            types.append('國內-開車')
                        elif not is_domestic(destination) and destination in COORDINATES:
                            # 國外：從桃園機場飛行
                            origin = COORDINATES['桃園機場']
                            dest = COORDINATES[destination]
                            dist, dur = calculate_distance(origin, dest, 'flying')
                            distances.append(dist)
                            times.append(dur)
                            types.append('國際-飛行')
                        else:
                            distances.append('')
                            times.append('')
                            types.append('')
                    else:
                        distances.append('')
                        times.append('')
                        types.append('')
                    
                    # 顯示進度
                    if (idx + 1) % 10 == 0:
                        print(f"  已處理 {idx + 1} 筆...")
                        time.sleep(0.5)  # 避免過度請求
                
                # 添加距離資訊到結果
                if end_row:
                    result_df.loc[start_row-1:end_row-1, '距離(km)'] = distances
                    result_df.loc[start_row-1:end_row-1, '時間'] = times
                    result_df.loc[start_row-1:end_row-1, '類型'] = types
                else:
                    result_df['距離(km)'] = distances
                    result_df['時間'] = times
                    result_df['類型'] = types
        else:
            print("檔案格式不符預期")
            return
        
        # 輸出結果
        output_path = os.path.join(current_dir, '出差地點整理結果_AI版.xlsx')
        result_df.to_excel(output_path, index=False)
        
        # 統計資訊
        total_count = len(result_df)
        has_location = (result_df['出差地點'] != '').sum()
        no_location = (result_df['出差地點'] == '').sum()
        
        print(f"\n✅ AI分析完成！")
        print(f"📊 總共處理：{total_count} 筆資料")
        print(f"✈️  有出差地點：{has_location} 筆 ({has_location/total_count*100:.1f}%)")
        print(f"❌ 無出差地點：{no_location} 筆 ({no_location/total_count*100:.1f}%)")
        print(f"\n💾 結果已儲存至：{output_path}")
        
        # 顯示特殊地點範例
        special_locations = result_df[result_df['出差地點'].str.contains('迦納|肯亞|衣索比亞|非洲', na=False)]
        if not special_locations.empty:
            print("\n🌍 包含非洲地點的資料範例：")
            for idx, row in special_locations.head(5).iterrows():
                print(f"   {row['序號']}: {row['傳票編號']} - {row['出差地點']}")
        
        # 顯示前20筆預覽
        print("\n📋 前20筆資料預覽：")
        for idx, row in result_df.head(20).iterrows():
            location = row['出差地點'] if row['出差地點'] else '(無出差地點)'
            print(f"   {row['序號']}: {row['傳票編號']} - {location}")
            
    except Exception as e:
        print(f"處理過程中發生錯誤：{e}")

if __name__ == "__main__":
    import sys
    
    # 檢查命令列參數
    if len(sys.argv) > 1:
        if sys.argv[1] == '--with-distance':
            # 計算距離模式
            start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
            end = int(sys.argv[3]) if len(sys.argv) > 3 else 10
            print(f"將計算第 {start} 到第 {end} 筆的距離")
            process_travel_data(calculate_distances=True, start_row=start, end_row=end)
        else:
            print("使用方式:")
            print("  python process_travel_data_AI.py              # 只提取地點")
            print("  python process_travel_data_AI.py --with-distance [起始列] [結束列]  # 計算距離")
    else:
        # 預設模式：只提取地點
        process_travel_data()
