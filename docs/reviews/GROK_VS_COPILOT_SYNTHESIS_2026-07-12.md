# Grok × Copilot 對抗式討論綜述（論文優化）

日期：2026-07-12  
Copilot 全文：`docs/reviews/COPILOT_ADVERSARIAL_JOSS_2026-07-12.md`  
觸發：`copilot -p`（adversarial JOSS reviewer，read-only）

---

## 共識（雙方都同意、應採納）

| 點 | 行動 |
|----|------|
| 未解析地名不可靜默當國際 0 km | **已修** `classify_trip_kind` → `unknown` + `resolved` flag |
| CHINA_KEYWORDS 亂碼 | **已修**（烏魯木齊、濰坊；刪無意義項） |
| paper 缺 JOSS required sections / 字數 | **已擴寫** State of the field / Software design / Research impact / AI disclosure |
| 合成 gold ≠ 外部驗證 | paper QA 改寫為 regression pass rate |
| 缺 CONTRIBUTING / support | **已加** CONTRIBUTING.md + issue template |
| OSRM 無 mock 測試 | 仍為 P1 |
| 預設係數誠實但宜考慮 CFP 預設 | 仍為 P2 政策選擇 |
| 真實帳冊 MAPE / P-R | 仍為科學主缺口 |
| 公開歷史短 | Copilot 強調 JOSS 可能 desk-reject；**需對照當日 JOSS 政策**，不盲信單一模型 |

## 分歧與 Grok 註記

| Copilot 主張 | Grok 註記 |
|--------------|-----------|
| JOSS「六個月公開開發」必 desk-reject | 政策會改；以官方 submitting 頁為準。短歷史是風險但非永遠絕對 |
| Functionality 表格絕對禁止 | JOSS 不喜 API 文件化；已改為設計取捨為主、功能簡述 |
| ADR 回溯日期= provenance theater | 同意弱；可不強調 ADR 日期或標明 retrospective |
| 必須馬上停投稿 | 同意「先修 P0 再送」；不一定等滿六個月若政策允許 + 持續迭代 |

## 已落地（本輪）

1. unresolved → unknown + `resolved`  
2. mappings 亂碼清理  
3. paper.md 合規擴寫  
4. CONTRIBUTING + bug issue template  
5. 存檔 Copilot 審查全文  

## 尚未做（P1）

- OSRM mock tests  
- factors.yaml 單一來源  
- 外部/二次標註 gold  
- GUI 整合測試  

## 投稿策略建議（合流）

1. **現在**：繼續公開迭代（本輪已 push 級改善）  
2. **本週**：Zenodo DOI + ORCID  
3. **送 JOSS 前**：再跑一次 adversarial checklist；確認官方 length/sections  
4. **並行**：中文研討會／技術報告不依賴 JOSS 時程  
