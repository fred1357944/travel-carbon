# Architecture Decision Records (ADRs)

本目錄包含專案的架構決策記錄。

## 索引

| ADR | 標題 | 狀態 | 日期 |
|-----|------|------|------|
| [0001](0001-use-osrm-for-routing.md) | 使用 OSRM 作為路由引擎 | Accepted | 2024-01-01 |

## 建立新的 ADR

1. 複製 `template.md` 為 `XXXX-title-with-dashes.md`
2. 編號遞增（如 `0002-...`）
3. 填寫範本內容
4. 更新此索引

## ADR 狀態說明

| 狀態 | 說明 |
|------|------|
| **Proposed** | 提案中，尚未決定 |
| **Accepted** | 已接受，實施中 |
| **Deprecated** | 已廢棄，不再適用 |
| **Superseded** | 被新 ADR 取代 |
| **Rejected** | 被拒絕，未採用 |

## 何時需要 ADR

✅ **需要 ADR：**
- 選擇新的框架或函式庫
- 資料庫或儲存技術選型
- API 設計模式決策
- 重大架構變更
- 有多個可行方案需要權衡

❌ **不需要 ADR：**
- 小版本升級
- Bug 修復
- 程式碼重構
- 設定變更

## 參考資源

- [Michael Nygard - Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [ADR GitHub Organization](https://adr.github.io/)
