# 多 AI 審議 Prompt：差旅碳排工具能否／如何寫成論文

> 用法：整份「給外部 AI 的 Prompt」區塊複製貼上給 Claude / GPT / Gemini / Perplexity 等。  
> 回傳後：把各模型完整回覆貼回主對話，一起交叉討論。  
> 配套背景檔：`docs/論文可行性與文獻研究_2026-07-11.md`

---

## 給外部 AI 的 Prompt（由此複製）

```markdown
# Role

你是一位同時熟悉以下領域的資深學術顧問（請明確標示你較強與較弱的面向）：
1. 高等教育機構（HEI）溫室氣體盤查與 Scope 3 / ISO 14064-1
2. GHG Protocol Scope 3 Category 6（Business Travel）方法論
3. 永續／環境管理／圖資應用類期刊的投稿與審稿慣例
4. 開源科研軟體論文（JOSS、SoftwareX 等）的門檻
5. 台灣大專校院行政差旅與碳盤查實務（若你不熟，請明確說「不確定」而非猜測）

請用**繁體中文**回答。先給結論，再給論證。區分：
- **[事證]** 有文獻／標準依據
- **[推論]** 合理但未驗證
- **[風險]** 審稿或方法誠實性風險
- **[不知道]** 需要查原文或實測

不要為了討好使用者而誇大 novelty。若你認為「不夠格寫 peer-reviewed 論文」，請直接說，並說明還差什麼。

---

# Project snapshot（請當作唯一事實來源；勿發明專案沒有的功能）

## What it is
台灣輔仁大學場景的 **Python 桌面工具**：讀取差旅 Excel 帳冊 → 從中文自由文本抽目的地 → 算距離 → 產 Folium 地圖 → 匯出含距離／碳排／地圖的 Excel。支援約數百～千筆年度資料批次處理與快取。

## Pipeline
Excel → 地名抽取／正規化（規則＋辭典；台/臺變體）→ 座標（硬編碼 COORDINATES + ALIASES + 區→市、城→機場）→ 距離：
- 本島：輔仁大學 → 目的地，**OSRM 開車距離**
- 離島：松山 → 離島，**大地線飛行**
- 國際：桃園 → 機場，**大地線**
→ 地圖（唯一路線去重、cache）→ Excel（碳排係數 × 距離、碳排放總覽 sheet）

## Claimed domain hooks
- GHG Protocol Scope 3 **Category 6 distance-based** 取向（非 spend-based）
- 簡化運具係數（註解寫「台灣環保署 2023」）：自用車 0.21、國內航 0.133、國際航 0.101、高鐵 0.034、巴士 0.065 kg CO₂e/km
- 運具啟發式：例如「開車且 >300 km → 當高鐵」
- 地圖作為**稽核軌跡**
- README 已有 SDG 3/12 與 BibTeX 草稿

## What it is NOT
- 不是 ML/LLM NER（雖檔名有 AI）
- 不是 ICAO 機型／載客率級飛行碳排
- 沒有正式 gold-label 評估（抽取 P/R、距離 MAPE、與官方盤查對帳）
- 未處理航空 RFI / radiative forcing
- 未確認係數是否等於環境部「113年公告溫室氣體排放係數」逐項
- 主程式巨型單檔、座標硬編碼、缺 CI 測試

## Preliminary gap claim（請你攻擊或改寫）
「歐美大學多用結構化訂票資料算學術航空碳排；台灣 HEI 盤查報告有列差旅但少公開方法。少有公開系統同時做到：中文 free-text 帳冊抽取 + 混合 OSRM 公路／大地線飛行 + 距離法係數 + 地圖稽核。」

## Literature already on the table（請補充／刪修，勿假裝都讀過全文）
- GHG Protocol Cat.6 Technical Guidance (WRI/WBCSD)
- ISO 14064-1:2018
- 環境部 113 年排放係數公告；盤查作業指引
- ICAO Carbon Emissions Calculator methodology
- DEFRA/DESNZ conversion factors（對照用）
- Ciers et al. 2019 (EPFL academic air travel, Sustainability)
- Valls-Val & Bovea 2021 (HEI carbon footprint review)
- Kiehle et al. 2023 (University of Oulu)
- Lee et al. 2021 (aviation climate forcing)
- Tsai et al. 2025 (Taiwan HEI ISO 14064-1, Sustainability)
- Tseng et al. 2022 (academic flying practices) / Schmidt 2022 (HEI air travel policy gaps)
- Huber & Rust 2016 (OSRM in research)
- Auger et al. 2021 (open-source university CF estimator)
- Wynes & Donner 2018 (UBC); Allamraju et al. 2025 (UofT Scope 3) 等

---

# Your tasks（請依序完成，用標題分段）

## Task 1 — Verdict matrix
用表格回答「值不值得寫成論文」：
| 投稿類型 | 現況可投稿？(Yes/Borderline/No) | 最小還要補什麼 | 預估接受難度(1–5) | 理由 |
包含至少：  
(a) JOSS / SoftwareX 類軟體論文  
(b) IJSHE / Sustainability / Cleaner Environmental Systems 等應用期刊  
(c) 環境工程／碳盤查方法期刊  
(d) GIS / 地理資訊期刊  
(e) 中文期刊或研討會  
(f) 碩士論文／技術報告（若相關）

## Task 2 — Novelty stress test
1. 用**審稿人最兇的 5 個問題**挑戰本專案。  
2. 對每個問題給：可回應策略 / 若答不出該砍掉的 claim。  
3. 改寫一版 **safe contribution statement**（中英各 1 段，≤120 字英文）。  
4. 標出哪些 claim 屬於 overclaim（例如「AI」「符合環保署係數」「首創」）。

## Task 3 — Method honesty audit
對下列每一項，判定：可寫成 methods 主敘述 / 只能當 limitation / 必須先修程式再寫：
1. 係數來源「環保署 2023」vs 環境部 113 公告  
2. >300 km → 高鐵的運具推估  
3. 國際僅機場大地線、無艙等／RFI  
4. OSRM 公共 API 可重現性  
5. 規則式地名抽取稱為 extraction pipeline  
6. 地圖嵌入作為 audit trail 的學術分量  
7. ISO 14064 vs GHG Protocol 類別對照  
請給「論文 Methods 應如何措辭」的範例句（可直接用）。

## Task 4 — Reference upgrade
1. 指出上述文獻清單的 **缺漏類型**（不是只再塞同質論文）。  
2. 建議 **最多 15 篇**「若只能引這些」的核心書目，分：Standards / HEI cases / Method uncertainty / Tools。  
3. 若你能提供更精確書目（作者、年、期刊、DOI），請給；不確定就標 [需核對]。  
4. 特別檢查：是否有**更接近**的競品（開源差旅碳排工具、中文報帳地理正規化、台灣大學差旅碳方法論文）——有的話必須點名。

## Task 5 — Minimum viable paper (MVP)
假設目標是 **12 個月內**可投稿的最小論文，給：
1. 建議 title（3 個備選，中英）  
2. Research questions（2–4 個，可驗證）  
3. 必做實驗與樣本設計（抽取評估、距離驗證、碳排敏感度——請給可操作的 n、指標、基線）  
4. 論文大綱（IMRaD 或 tool-paper 結構）  
5. 明確的 **out-of-scope**（這版不做什麼）  
6. 成功標準：什麼結果叫「夠投」、什麼叫「再等一年」

## Task 6 — Venue & strategy
1. 首選／次選／保底 venue 各 1–2，附：契合度、OA 與否（若知）、常見拒稿理由。  
2. 若走「工具論文 + 應用短文」雙產出，如何切資料避免 salami slicing。  
3. 作者貢獻與倫理：真實帳冊個資、機構同意、開源授權注意點。

## Task 7 — Decision memo（給決策者的一頁）
用以下格式收尾（務必填）：

**GO / CONDITIONAL GO / NO-GO：**  
**條件（若 CONDITIONAL）：**  
**最大學術賣點（1 句）：**  
**最大致命傷（1 句）：**  
**未來 30 天只做這 3 件事：**  
**不該花時間做的 3 件事：**  
**你對自己這份建議的信心（1–10）與為何不是 10：**

---

# Output rules
- 總長建議 1500–3000 中文字；可用表格壓縮。  
- 禁止空話（「很有潛力」「值得深入研究」）除非附具體條件。  
- 禁止發明專案沒有的模組或已完成的評估數字。  
- 若需要假設，標 **[假設]**。  
- 最後附：你希望使用者補充的 **5 個事實問題**（用來提高建議品質）。
```

---

## 使用建議（給你自己）

1. **同一份 prompt** 至少丟 2–3 個模型（例如 Claude Opus、GPT、Gemini），要求都用繁中。  
2. 可選加一句：`請特別從 [審稿人 / 碳盤查實務者 / 軟體論文編輯] 視角偏重。` 做角色變體。  
3. 回傳貼回時，請標明模型名稱與日期。  
4. 若某模型給了大量「新文獻」，回來後應要求核 DOI，勿直接寫進稿。  
5. 討論時我們會做：共識提取 → 分歧表 → 更新 `論文可行性與文獻研究_2026-07-11.md` 的決策記錄。

---

## 貼回格式建議（給主對話）

```text
## 模型：xxx
## 日期：
## 完整回覆：
（貼上）

## 我自己的初步判斷（可選）：
- 同意：
- 不同意：
- 想追問：
```
