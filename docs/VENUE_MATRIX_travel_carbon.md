# Venue 矩陣 — travel-carbon / 大學差旅 Scope 3 工具稿

**日期**：2026-07-12  
**稿件**：`paper/paper.md`（短稿／軟體說明）＋規劃中 `paper/application_draft.md`（應用期刊長稿）  
**軟體**：https://github.com/fred1357944/travel-carbon  
**署名預設**：輔仁大學（與全域規則一致，除非另拍板）  
**狀態**：**AMBER — 待使用者拍板首投 venue**；下列為 2026-07-12 盤點，**非正式 GREEN 送件授權**。

---

## 0. 稿件類型判定

| 維度 | 現況 | 對 venue 的含義 |
|------|------|----------------|
| 實證 | 合成 gold n≈52；真實帳冊未公開驗證 | 純工具短文可先走 JOSS；**IJSHE/Sustainability 需要案例結果** |
| 長度 | ~1.2k words（JOSS 短稿） | 應用期刊通常需 **5–10k+ words** 級方法＋結果 |
| 貢獻 | 繁中 free-text 帳冊→距離法 Cat.6 管線 | HEI 永續實務／工具案例，非純 GIS 算法 |
| 風險 | 係數為 screening；模式啟發式 | Methods 必須誠實；避免「符合盤查法規」 |

---

## 1. 候選矩陣

| Venue | Scope 契合 | 近期前例／訊號 | APC／費用（約） | 字數／格式 | 判決 | 備註 |
|-------|------------|----------------|-----------------|------------|------|------|
| **IJSHE** (Emerald) | **高** — HEI 永續、差旅減碳、政策與實務 | 多篇 academic air travel / business travel GHG；e.g. 部門差旅 GHG 核算、UK 大學 sustainable travel 政策回顧 | 訂閱制為主；OA 另計（需 live 查最新） | 研究論文結構；倫理／同意聲明要求嚴格 | **AMBER→條件 GREEN** | **首選應用軌**。需：真實或充分去識別案例、字數、倫理敘述。**不可用現 JOSS 短稿直接投** |
| **Sustainability** (MDPI) | **高** — HEI 永續、校園碳、數位工具 | 大量 HEI CF／ISO 14064 個案（含 Tsai et al. 2025 台灣）；Special Issues: Higher Education for Sustainability | **Gold OA，APC 高**（需 live 查當期） | Article；審稿快 | **AMBER** | 速度快、scope 寬；代價是 APC 與「MDPI 觀感」。有案例後可投 section *Sustainable Education and Approaches* |
| **International Journal of Life Cycle Assessment** | 中高 — CF 方法整合 | Deda et al. 2025 HEI CF + GHG Protocol/ISO | 訂閱/OA 混合 | 方法＋個案 | **AMBER** | 要更「LCA／盤查方法」味；工具 GUI 敘事要下調 |
| **Journal of Cleaner Production** | 中 — 減碳與行為 | Wynes et al. 學術飛行與產出 | APC 高 | 長文、證據門檻高 | **RED（現階段）** | 實證不足時易 desk；日後有 MAPE／政策結果再評 |
| **Cleaner Environmental Systems** | 中高 — 系統性 CF 工具 | Valls-Val 綜述／工具線 | 視出版社 | 方法工具 | **AMBER** | 可作 Sustainability 備案 |
| **SoftwareX** | 中 — 科研軟體 | 工具論文 | APC（曾約 USD 量級，需 live） | software paper | **AMBER** | 與 JOSS 同族；若不要 MDPI 又要比 JOSS 長可選 |
| **JOSS** | 中 — 開源研究軟體 | 短 paper + repo 審查 | 免費 | 750–1750 words 量級 | **AMBER（工程可、歷史短）** | **軟體軌保底**；不取代應用期刊故事 |
| **台灣／區域：大學永續、Talloires、校園永續研討會** | 高（實務） | 各校永續報告書、國內研討會 | 通常低／無 | 中英皆可 | **GREEN（跳板）** | 先發表實務案例、累積證據，再投 IJSHE |
| **輔大／台灣高教永續社群報告、USR、SDGs 專刊** | 高 | 機構導向 | 低 | 中文可 | **GREEN（對內／實務）** | 不計國際影響因子，但服務機構 |

### 判決圖例
- **GREEN**：scope＋前例＋費用可接受，可開打包  
- **AMBER**：可行但有條件（實證／APC／字數）  
- **RED**：現階段不建議  

---

## 2. 建議策略（2026-07-12）

```text
軌 A（應用期刊主線）— 使用者本次指定方向
  1) 擴成長稿 application_draft（方法＋合成評估＋誠實限制）
  2) 補文獻 25–40 條 + CITATIONS_VERIFIED
  3) 取得去識別真實案例 OR 明確標「工具＋合成驗證」投 Sustainability 工具向
  4) 首投候選：IJSHE（訂閱友善）或 Sustainability（快、付 APC）
  5) 未拍板前禁止雙投

軌 B（軟體保底，已公開）
  JOSS / SoftwareX — 維持短 paper.md + repo

軌 C（永續大學實務跳板）
  校園永續／高教 SDG 研討會或中文實務專刊 → 累積引用與使用者故事
```

### 條件式推薦（尚未使用者最終拍板）

| 優先 | Venue | 條件 |
|------|--------|------|
| 1 | **IJSHE** | 有機構去識別案例 **或** 願意寫成 “tool + workflow case with synthetic validation” 並接受較嚴的 limitation |
| 2 | **Sustainability** | 接受 APC；強調 HEI 數位工具／ISO 14064 實務 |
| 3 | **校園永續研討會／中文專刊** | 要速度與機構能見度 |
| 4 | **JOSS** | 並行軟體短文，不與期刊主文 salami 重複「同一結果表」 |

**紅線（記取 E&B / CAD scope-reject）**  
- 勿投 Energy and Buildings 類「能源系統」刊（domain 近≠scope 合）  
- 勿在無 GREEN 帳本紀錄時中途換刊  
- 同資料集勿拆成兩篇僅改標題  

---

## 3. 投稿前還差什麼（對應用期刊）

| 缺口 | IJSHE | Sustainability | 研討會 |
|------|-------|----------------|--------|
| 真實／去識別年度結果表 | 幾乎必須 | 強烈建議 | 可較鬆 |
| 字數 5k+ 級 | 是 | 是 | 視 CFP |
| 倫理／資料治理句 | 必須 | 必須 | 建議 |
| 文獻 30+ | 建議 | 建議 | 15–25 可 |
| 軟體可用性 | 加分 | 加分 | 加分 |

---

## 4. 決策日誌（本專案）

- 2026-07-12｜travel-carbon｜使用者要求 1–3 轉向**應用期刊**（IJSHE / Sustainability／大學永續相關），不再只鎖 JOSS｜本矩陣寫入；VENUE_LEDGER 登記；長稿＋文獻＋pandoc 包啟動。**首投尚未拍板**→狀態 AMBER。
