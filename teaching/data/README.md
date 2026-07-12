# 教學用合成資料

| 檔案 | 說明 |
|------|------|
| `teaching_ledger_40.csv` | 40 筆虛構差旅列（學員代號亦虛構） |
| `teaching_ledger_40_key.csv` | 教師用：系統離線預測 kind／距離／碳（`use_osrm=False`） |

**禁止**放入真實報帳、姓名、工號。  
重新產生 key：

```bash
# 見 repo 根目錄；或重跑生成腳本邏輯
python3 -c "from travel_carbon.pipeline import estimate_trip; ..."
```
