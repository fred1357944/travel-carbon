# ADR-0001: 使用 OSRM 作為路由引擎

## 狀態

Accepted

## 日期

2024-01-01（回溯記錄）

## 決策者

專案開發者

## 背景

專案需要計算從輔仁大學到國內各地的實際開車距離，用於出差費用報銷計算。

主要需求：
- 計算實際道路距離（非直線距離）
- 支援台灣全島路網
- 無需付費或 API 金鑰
- 可承受批次處理（數百筆資料）

## 考慮的替代方案

### 選項 1: OSRM (Open Source Routing Machine)

**優點：**
- 免費公共 API，無需 API Key
- 使用 OpenStreetMap 資料，台灣道路覆蓋完整
- 回傳實際開車路線距離和時間
- 開源，可自架避免限速

**缺點：**
- 無即時路況資訊
- 公共服務無 SLA，可能被限速
- 無法自訂路由偏好（如避開高速公路）

### 選項 2: Google Maps Directions API

**優點：**
- 最完整的路網資料
- 即時路況
- 多種交通方式選項

**缺點：**
- 需要付費（超過免費額度）
- 需要 API Key 管理
- 有每日請求限制

### 選項 3: Geopy Geodesic（直線距離）

**優點：**
- 完全離線，無 API 依賴
- 計算速度最快
- 無任何限制

**缺點：**
- 只能計算直線距離，與實際道路差異大
- 無法產生路線地圖

### 選項 4: OpenRouteService

**優點：**
- 免費 API 額度充足
- 功能豐富（等時圈、優化路線）
- 可自訂路由偏好

**缺點：**
- 需要註冊取得 API Key
- 需要額外整合工作

## 決策

採用 **OSRM 公共 API** 作為主要路由引擎，以 **Geopy Geodesic** 作為備援。

## 理由

1. **零成本**：專案預算有限，OSRM 免費使用
2. **無需 API Key**：簡化部署和維護
3. **足夠準確**：台灣道路資料完整，距離誤差可接受
4. **備援機制**：OSRM 失敗時可用 Geopy 計算直線距離
5. **快取緩解限速**：透過快取機制減少 API 呼叫次數

## 後果

### 正面

- 專案可免費運作
- 部署簡單，無需管理 API 金鑰
- 快取機制使重複路線幾乎即時回應
- 程式碼簡潔，依賴少

### 負面

- 無即時路況，距離為理想狀態
- 公共服務可能在高峰期變慢
- 無法選擇特定路線（如避開收費道路）

### 風險與緩解

| 風險 | 緩解策略 |
|------|----------|
| OSRM 公共服務被限速 | 實作快取機制，避免重複請求 |
| OSRM 服務中斷 | 備援使用 Geopy 直線距離 |
| 距離與實際差異 | 可接受誤差，差旅費計算無需精確到公尺 |

## 實作細節

```python
# 主要路由：OSRM API
def get_driving_distance(start, end):
    url = f"http://router.project-osrm.org/route/v1/driving/{start[1]},{start[0]};{end[1]},{end[0]}"
    response = requests.get(url)
    return response.json()['routes'][0]['distance'] / 1000  # km

# 備援：Geopy 直線距離
from geopy.distance import geodesic
def get_geodesic_distance(start, end):
    return geodesic(start, end).kilometers
```

## 相關決策

- ADR-0002: 快取策略（計畫中）
- ADR-0003: 國際航線距離計算方式（計畫中）

## 參考資料

- [OSRM 官方文件](https://project-osrm.org/docs/v5.24.0/api/)
- [OpenStreetMap 台灣](https://www.openstreetmap.org/#map=7/23.5/121)
- [Geopy 文件](https://geopy.readthedocs.io/)
