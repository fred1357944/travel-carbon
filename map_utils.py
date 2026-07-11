# 地圖縮放級別計算函數
def calculate_zoom_level(distance_km):
    """根據距離計算適當的地圖縮放級別
    
    縮放級別說明：
    - 13-14: 街道級別，適合 <10km 的距離
    - 11-12: 區域級別，適合 10-40km 的距離  
    - 9-10: 城市級別，適合 40-150km 的距離
    - 7-8: 區域級別，適合 150-600km 的距離
    - 5-6: 國家級別，適合 600-3000km 的距離
    - 3-4: 洲際級別，適合 >3000km 的距離
    """
    if distance_km < 10:
        return 13  # 街道細節（如新北市內）
    elif distance_km < 20:
        return 12  # 區域細節（如台北市）
    elif distance_km < 40:
        return 11  # 城市邊界
    elif distance_km < 80:
        return 10  # 大城市範圍
    elif distance_km < 150:
        return 9   # 縣市範圍（如台中）
    elif distance_km < 300:
        return 8   # 跨縣市（如高雄）
    elif distance_km < 600:
        return 7   # 半島範圍
    elif distance_km < 1500:
        return 6   # 區域國家
    elif distance_km < 3000:
        return 5   # 東亞範圍
    elif distance_km < 6000:
        return 4   # 半球範圍
    else:
        return 3   # 全球範圍

# 改進的地圖創建函數
def create_enhanced_map(result, output_path):
    """創建增強版地圖，包含智能縮放和路線細節"""
    import folium
    from folium import plugins
    
    try:
        # 取得座標
        start_lat = result['起點']['lat']
        start_lon = result['起點']['lon']
        end_lat = result['終點']['lat'] 
        end_lon = result['終點']['lon']
        
        # 計算中心點和距離
        center_lat = (start_lat + end_lat) / 2
        center_lon = (start_lon + end_lon) / 2
        distance = result.get('距離(km)', 0)
        
        # 智能縮放
        zoom_level = calculate_zoom_level(distance)
        
        # 創建地圖，使用更清晰的圖層
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=zoom_level,
            tiles='OpenStreetMap',
            prefer_canvas=True
        )
        
        # 添加額外的圖層選項
        folium.TileLayer('CartoDB positron', name='簡潔地圖').add_to(m)
        folium.TileLayer('CartoDB dark_matter', name='深色地圖').add_to(m)
        
        # 起點標記（更詳細的資訊）
        start_popup = f"""
        <div style='width: 200px;'>
            <h4>起點</h4>
            <p><b>{result['起點']['name']}</b></p>
            <p>座標: {start_lat:.4f}, {start_lon:.4f}</p>
        </div>
        """
        folium.Marker(
            [start_lat, start_lon],
            popup=folium.Popup(start_popup, max_width=250),
            tooltip="起點 - 點擊查看詳情",
            icon=folium.Icon(color='green', icon='play', prefix='fa')
        ).add_to(m)
        
        # 終點標記
        end_popup = f"""
        <div style='width: 200px;'>
            <h4>終點</h4>
            <p><b>{result['終點']['name']}</b></p>
            <p>座標: {end_lat:.4f}, {end_lon:.4f}</p>
            <p>距離: {distance} km</p>
        </div>
        """
        folium.Marker(
            [end_lat, end_lon],
            popup=folium.Popup(end_popup, max_width=250),
            tooltip="終點 - 點擊查看詳情",
            icon=folium.Icon(color='red', icon='stop', prefix='fa')
        ).add_to(m)
        
        # 繪製路線
        if result.get('類型') == '國內-開車' and result.get('route'):
            # 實際開車路線
            route_coords = [[coord[1], coord[0]] for coord in result['route']['coordinates']]
            
            # 主路線（藍色）
            folium.PolyLine(
                route_coords,
                color='#0066CC',
                weight=6,
                opacity=0.8
            ).add_to(m)
            
            # 路線陰影效果
            folium.PolyLine(
                route_coords,
                color='#000033',
                weight=8,
                opacity=0.3
            ).add_to(m)
            
            # 自動調整視野以顯示完整路線
            if len(route_coords) > 0:
                bounds = [[min(c[0] for c in route_coords), min(c[1] for c in route_coords)],
                         [max(c[0] for c in route_coords), max(c[1] for c in route_coords)]]
                
                # 根據距離調整padding
                padding_ratio = 0.1 if distance > 100 else 0.15 if distance > 50 else 0.2
                m.fit_bounds(bounds, padding=(padding_ratio, padding_ratio))
                
        else:
            # 飛行路線（曲線）
            import numpy as np
            
            # 創建曲線路徑
            num_points = 50
            t = np.linspace(0, 1, num_points)
            
            # 控制點（創建弧形）
            control_height = min(distance / 1000, 10)  # 根據距離調整弧度
            control_lat = center_lat + control_height
            control_lon = center_lon
            
            # 二次貝茲曲線
            curve_lats = (1-t)**2 * start_lat + 2*(1-t)*t * control_lat + t**2 * end_lat
            curve_lons = (1-t)**2 * start_lon + 2*(1-t)*t * control_lon + t**2 * end_lon
            curve_coords = list(zip(curve_lats, curve_lons))
            
            # 繪製飛行路線
            folium.PolyLine(
                curve_coords,
                color='#FF3333',
                weight=4,
                opacity=0.8,
                dash_array='10, 5'
            ).add_to(m)
            
            # 飛機圖標（在路線中點）
            mid_idx = len(curve_coords) // 2
            folium.Marker(
                curve_coords[mid_idx],
                icon=folium.Icon(color='blue', icon='plane', prefix='fa')
            ).add_to(m)
            
            # 調整視野
            bounds = [[min(start_lat, end_lat), min(start_lon, end_lon)],
                     [max(start_lat, end_lat), max(start_lon, end_lon)]]
            padding_ratio = 0.15 if distance > 1000 else 0.2
            m.fit_bounds(bounds, padding=(padding_ratio, padding_ratio))
        
        # 添加距離標籤
        distance_popup = f"""
        <div style='background: white; 
                    padding: 8px; 
                    border: 2px solid #333;
                    border-radius: 5px;
                    font-weight: bold;'>
            {distance} km<br>
            {result.get('時間', '')}
        </div>
        """
        folium.Marker(
            [center_lat, center_lon],
            icon=folium.DivIcon(html=distance_popup)
        ).add_to(m)
        
        # 資訊面板（響應式設計）
        info_html = f"""
        <div style='position: fixed; 
                    top: 10px; 
                    right: 10px; 
                    background: rgba(255,255,255,0.95);
                    padding: 15px;
                    border: 2px solid #333;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    font-family: "Microsoft JhengHei", Arial;
                    z-index: 1000;
                    max-width: 320px;'>
            <h3 style='margin: 0 0 10px 0; color: #0066CC;'>路線資訊</h3>
            <table style='width: 100%; font-size: 14px;'>
                <tr>
                    <td style='padding: 4px; color: #666;'><b>傳票編號:</b></td>
                    <td style='padding: 4px;'>{result.get('傳票編號', 'N/A')}</td>
                </tr>
                <tr>
                    <td style='padding: 4px; color: #666;'><b>起點:</b></td>
                    <td style='padding: 4px;'>{result['起點']['name']}</td>
                </tr>
                <tr>
                    <td style='padding: 4px; color: #666;'><b>終點:</b></td>
                    <td style='padding: 4px;'>{result['終點']['name']}</td>
                </tr>
                <tr>
                    <td style='padding: 4px; color: #666;'><b>距離:</b></td>
                    <td style='padding: 4px; color: #FF6600; font-weight: bold;'>{distance} km</td>
                </tr>
                <tr>
                    <td style='padding: 4px; color: #666;'><b>時間:</b></td>
                    <td style='padding: 4px;'>{result.get('時間', 'N/A')}</td>
                </tr>
                <tr>
                    <td style='padding: 4px; color: #666;'><b>類型:</b></td>
                    <td style='padding: 4px;'>{result.get('類型', 'N/A')}</td>
                </tr>
                <tr>
                    <td style='padding: 4px; color: #666;'><b>縮放級別:</b></td>
                    <td style='padding: 4px;'>Level {zoom_level}</td>
                </tr>
            </table>
        </div>
        """
        m.get_root().html.add_child(folium.Element(info_html))
        
        # 添加測量工具
        plugins.MeasureControl(position='bottomleft').add_to(m)
        
        # 添加全螢幕按鈕
        plugins.Fullscreen(position='topright').add_to(m)
        
        # 添加圖層控制
        folium.LayerControl(position='topleft').add_to(m)
        
        # 儲存地圖
        m.save(output_path)
        return True
        
    except Exception as e:
        print(f"創建地圖錯誤: {e}")
        return False
