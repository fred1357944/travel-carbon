#!/bin/bash
# 安裝出差距離計算工具所需套件

echo "==================================="
echo "出差距離計算工具 - 套件安裝腳本"
echo "==================================="
echo ""

# 檢查是否有Python
if ! command -v python3 &> /dev/null; then
    echo "錯誤：找不到 Python 3，請先安裝 Python"
    exit 1
fi

echo "正在安裝必要套件..."
echo ""

# 基本套件
pip3 install pandas openpyxl xlsxwriter

# 地圖和距離計算套件
pip3 install folium geopy requests

# GUI套件
pip3 install pillow

# 網頁截圖套件 (需要Chrome)
pip3 install selenium

echo ""
echo "套件安裝完成！"
echo ""
echo "注意事項："
echo "1. 地圖截圖功能需要安裝 Chrome 瀏覽器和 ChromeDriver"
echo "   - Mac: brew install chromedriver"
echo "   - 或從 https://chromedriver.chromium.org/ 下載"
echo ""
echo "2. 使用方式："
echo "   - GUI版本: python3 travel_distance_calculator_gui.py"
echo "   - 命令列版本: python3 process_travel_data_AI.py --with-distance 1 10"
echo ""
echo "==================================="
