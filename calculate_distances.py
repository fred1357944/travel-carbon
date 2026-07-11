import json
import os
import time

import folium
import pandas as pd
import requests
from folium import plugins
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 各地點座標（台灣主要城市政府位置）
COORDINATES = {
    "輔仁大學": {"lat": 25.0356, "lon": 121.4320, "name": "輔仁大學正門"},
    "台北": {"lat": 25.0330, "lon": 121.5654, "name": "台北市政府"},
    "臺北": {"lat": 25.0330, "lon": 121.5654, "name": "台北市政府"},  # 統一處理
    "新北": {"lat": 25.0119, "lon": 121.4653, "name": "新北市政府"},
    "台中": {"lat": 24.1639, "lon": 120.6478, "name": "台中市政府"},
    "臺中": {"lat": 24.1639, "lon": 120.6478, "name": "台中市政府"},
    "高雄": {"lat": 22.6273, "lon": 120.3014, "name": "高雄市政府"},
    "新竹": {"lat": 24.8138, "lon": 120.9675, "name": "新竹市政府"},
    "桃園": {"lat": 24.9936, "lon": 121.3010, "name": "桃園市政府"},
    "台南": {"lat": 22.9997, "lon": 120.2269, "name": "台南市政府"},
    "臺南": {"lat": 22.9997, "lon": 120.2269, "name": "台南市政府"},
    "基隆": {"lat": 25.1324, "lon": 121.7391, "name": "基隆市政府"},
    "嘉義": {"lat": 23.4801, "lon": 120.4538, "name": "嘉義市政府"},
    "彰化": {"lat": 24.0757, "lon": 120.5442, "name": "彰化縣政府"},
    "屏東": {"lat": 22.6821, "lon": 120.4871, "name": "屏東縣政府"},
    "宜蘭": {"lat": 24.7021, "lon": 121.7377, "name": "宜蘭縣政府"},
    "花蓮": {"lat": 23.9871, "lon": 121.6015, "name": "花蓮縣政府"},
    "台東": {"lat": 22.7972, "lon": 121.0713, "name": "台東縣政府"},
    "臺東": {"lat": 22.7972, "lon": 121.0713, "name": "台東縣政府"},
    "澎湖": {"lat": 23.5711, "lon": 119.5793, "name": "澎湖縣政府"},
    "金門": {"lat": 24.4493, "lon": 118.3766, "name": "金門縣政府"},
    "馬祖": {"lat": 26.1505, "lon": 119.9498, "name": "連江縣政府"},
}


def get_osrm_route(start_lat, start_lon, end_lat, end_lon):
    """使用OSRM API獲取實際行車路線"""
    try:
        # OSRM API endpoint
        url = f"http://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}"
        params = {"overview": "full", "geometries": "geojson", "steps": "true"}

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data["code"] == "Ok":
                route = data["routes"][0]
                distance_km = route["distance"] / 1000
                duration_min = route["duration"] / 60
                geometry = route["geometry"]

                return {
                    "distance_km": round(distance_km, 1),
                    "duration_min": round(duration_min),
                    "geometry": geometry,
                }
    except Exception as e:
        print(f"OSRM API錯誤: {e}")

    return None


def create_route_map(start_name, end_name, route_data, filename):
    """創建路線地圖"""
    start = COORDINATES[start_name]
    end = COORDINATES[end_name]

    # 創建地圖
    center_lat = (start["lat"] + end["lat"]) / 2
    center_lon = (start["lon"] + end["lon"]) / 2

    m = folium.Map(
        location=[center_lat, center_lon], zoom_start=10, tiles="OpenStreetMap"
    )

    # 添加起點標記
    folium.Marker(
        [start["lat"], start["lon"]],
        popup=f"<b>起點</b><br>{start['name']}",
        icon=folium.Icon(color="green", icon="play"),
    ).add_to(m)

    # 添加終點標記
    folium.Marker(
        [end["lat"], end["lon"]],
        popup=f"<b>終點</b><br>{end['name']}",
        icon=folium.Icon(color="red", icon="stop"),
    ).add_to(m)

    # 添加路線
    if route_data and "geometry" in route_data:
        route_coords = [
            [coord[1], coord[0]] for coord in route_data["geometry"]["coordinates"]
        ]
        folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.8).add_to(m)

        # 添加距離和時間資訊
        info_html = f"""
        <div style='position: fixed;
                    top: 10px; right: 10px;
                    background: white;
                    padding: 10px;
                    border: 2px solid grey;
                    border-radius: 5px;
                    z-index: 9999;'>
            <b>路線資訊</b><br>
            起點: {start['name']}<br>
            終點: {end['name']}<br>
            距離: {route_data['distance_km']} 公里<br>
            時間: {route_data['duration_min']} 分鐘
        </div>
        """
        m.get_root().html.add_child(folium.Element(info_html))

    # 儲存地圖
    m.save(filename)
    return m


def process_travel_distances():
    """處理前10筆出差資料的距離計算"""

    # 讀取處理後的Excel檔案
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(current_dir, "出差地點整理結果_AI版.xlsx")

    if not os.path.exists(input_file):
        print(f"找不到檔案: {input_file}")
        return

    # 讀取資料
    df = pd.read_excel(input_file)

    # 只處理前10筆有出差地點的資料
    results = []
    map_count = 0

    print("正在計算前10筆出差資料的實際行車距離...\n")
    print(
        f"{'序號':<6} {'傳票編號':<15} {'目的地':<10} {'距離(km)':<10} {'時間(分)':<10}"
    )
    print("-" * 60)

    for idx, row in df.head(10).iterrows():
        if row["出差地點"]:
            # 取第一個目的地
            destination = row["出差地點"].split("、")[0]

            # 統一處理台北
            if destination == "臺北":
                destination = "台北"

            if destination in COORDINATES:
                # 獲取路線資訊
                route_data = get_osrm_route(
                    COORDINATES["輔仁大學"]["lat"],
                    COORDINATES["輔仁大學"]["lon"],
                    COORDINATES[destination]["lat"],
                    COORDINATES[destination]["lon"],
                )

                if route_data:
                    results.append(
                        {
                            "序號": row["序號"],
                            "傳票編號": row["傳票編號"],
                            "目的地": destination,
                            "實際距離(km)": route_data["distance_km"],
                            "行車時間(分)": route_data["duration_min"],
                        }
                    )

                    print(
                        f"{row['序號']:<6} {row['傳票編號']:<15} {destination:<10} "
                        f"{route_data['distance_km']:<10} {route_data['duration_min']:<10}"
                    )

                    # 為前3筆創建地圖
                    if map_count < 3:
                        map_filename = os.path.join(
                            current_dir, f"route_map_{map_count+1}_{destination}.html"
                        )
                        create_route_map(
                            "輔仁大學", destination, route_data, map_filename
                        )
                        print(f"   → 地圖已儲存: {map_filename}")
                        map_count += 1

                    # 避免過度請求
                    time.sleep(0.5)

    # 儲存結果
    if results:
        results_df = pd.DataFrame(results)
        output_file = os.path.join(current_dir, "出差距離計算結果.xlsx")
        results_df.to_excel(output_file, index=False)
        print(f"\n✅ 距離計算結果已儲存至: {output_file}")

        # 顯示統計
        print(f"\n📊 統計資訊:")
        print(f"   平均距離: {results_df['實際距離(km)'].mean():.1f} 公里")
        print(
            f"   最短距離: {results_df['實際距離(km)'].min():.1f} 公里 ({results_df.loc[results_df['實際距離(km)'].idxmin(), '目的地']})"
        )
        print(
            f"   最長距離: {results_df['實際距離(km)'].max():.1f} 公里 ({results_df.loc[results_df['實際距離(km)'].idxmax(), '目的地']})"
        )


if __name__ == "__main__":
    process_travel_distances()
