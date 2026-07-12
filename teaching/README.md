# 教學包（Paper E）— 草稿

**原則**：不急投稿；下學期數堂課導入；合成資料 only。

## 與輔大制度對接

- 114 起日進學士：**永續素養領域（DT）** 2 學分（通識結構調整）  
- 學群：永續證照（D8）／永續多元（V8）  
- 校聞強調碳盤查與永續能力：https://www.fju.edu.tw/newsDetail.jsp?newsID=7757  
- 詳見 `paper/PAPER_E_curriculum_alignment.md`

## 建議嵌入方式

與**系主任／統計系老師**共授：**3 堂**導入（可調）：

| 堂 | 主題 | 學生產出 |
|----|------|----------|
| 1 | Scope 3 與假報帳歧義 | 歧義地名清單 |
| 2 | 上機 travel-carbon（合成 CSV） | 截圖＋screening vs cfp 對照 |
| 3 | 批判、採用、永續長 memo | 1 頁政策／改進建議 |

## 檔案

- `lesson_plan_3sessions.md` — 教案  
- 合成資料沿用 repo `examples/sample_travel_records.csv` 與 gold 集  

## 軟體

```bash
pip install -e ".[dev]"
python -m travel_carbon 台中
python -m travel_carbon.eval_batch --gold examples/sample_travel_gold_50.csv --out-dir /tmp/demo
```

GUI：`python travel_distance_calculator_gui_cached_efficient.py`
