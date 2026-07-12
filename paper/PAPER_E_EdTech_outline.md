# Paper E — Education and Information Technologies 大綱

**工作標題（英）**  
*Adopting administrative carbon tools in university sustainability work and teaching: A classroom-and-office deployment of an open travel-carbon workflow*

**工作標題（中）**  
行政差旅碳工具的採用與教學：開源工作流於大學永續單位與永續素養課堂的部署研究

**目標刊**：Education and Information Technologies (Springer, journal 10639)  
**狀態**：大綱（2026-07-12）— 待試教／訪談數據  
**軟體**：https://github.com/fred1357944/travel-carbon  
**與 Paper S 邊界**：見 `docs/VENUE_MATRIX_travel_carbon.md` §4

---

## 1. 為什麼這篇「很 10639」

本刊關心 **ICT 與教育／高教實踐的關係**，不是 GHG 方法專刊。

我們的雙錨：

1. **組織採用（adoption）**  
   永續中心／環安／總務如何把行政數位工具嵌進差旅碳資料工作？促成／阻礙因素？
2. **教學使用（teaching & learning）**  
   永續素養學程課堂中，工具作為 **boundary object（邊界物件）**，如何支持 Scope 3 識讀與批判性使用（含不確定性）？

輔大推動**永續素養學程**＝ curriculum window：不是「又多一個系統」，而是學程需要**可操作的碳識讀教具**。

---

## 2. 研究問題（建議定稿用 2–3 個）

- **RQ1（採用）**  
  大學永續相關單位在何種條件下採用（或拒用）開源差旅碳行政工具？資料、技能、制度、信任如何作用？
- **RQ2（教學）**  
  在永續素養取向的課堂設計中，學生使用該工具後，碳／Scope 3 相關知識與態度如何變化？如何談論工具假設與風險？
- **RQ3（設計回饋，可選）**  
  課堂與單位使用者的回饋，如何回推資訊系統的設計原則（解析失敗可見性、係數透明、隱私）？

---

## 3. 概念框架（選 1 主＋1 輔，勿堆）

| 層 | 建議 | 用途 |
|----|------|------|
| 主 | **Sociotechnical systems / 工作實踐中的工具** | 行政採用不是「上線就用」 |
| 輔 A | **Technology acceptance**（精簡 UTAUT／TAM：績效預期、努力預期、促成條件） | 問卷可操作 |
| 輔 B | **Boundary object**（Star & Griesemer 傳統） | 同一工具連接行政世界與課堂 |
| 輔 C | **Education for Sustainable Development (ESD) / 碳素養** | 對接學程語言 |

論文一句話：  
> 我們檢視開源行政碳工具如何在永續治理實踐與素養教育之間被**採用、教學化與重新詮釋**。

---

## 4. 教學設計（可寫進 Methods）

### 4.1 課程窗口

- 載體：輔大**永續素養學程**相關課程／工作坊（正式課名投稿前填）  
- 時數：建議 **6–9 小時**（三週單元）或一日工作坊＋作業  
- 對象：修素養課之大學部／研究生（說明抽樣）

### 4.2 三節結構

| 節 | 目標 | 活動 | 數位工具 |
|----|------|------|----------|
| 1 識讀 | Scope 1/2/3、Cat.6、distance vs spend | 假報帳閱讀；標歧義地名 | 尚未計算 |
| 2 操作 | 會跑通、會讀輸出 | 合成 ledger 上機；screening vs taiwan_cfp | travel-carbon GUI/CLI |
| 3 批判與採用 | 不確定性、倫理、若你是永續長 | memo／改進建議；可選對 GitHub 開 issue | 輸出＋反思 |

### 4.3 原則

- **只用合成或學生虛構行程**；真報帳個資不上課  
- 強調 **resolved=false / unknown** 必須被討論（反黑箱）  
- 對接學程：可對應 SDG 12/13、校園淨零敘事（依學程文件微調）

---

## 5. 永續單位採用研究（可與課堂同季）

### 5.1 對象（示意）

- 永續發展中心／委員會幕僚  
- 環安衛、總務／出納、碳盤查承辦（1–5 人深度即可）

### 5.2 問題焦點

- 現在差旅碳資料怎麼來？痛點？  
- 願不願意用開源桌面工具？怕什麼（資安、正確性、維運）？  
- 與正式 ISO 盤查／顧問報表的關係？  
- 課堂產出能否回饋行政（例如未解析地名清單）？

### 5.3 資料

- 半結構訪談 30–45 分  
- 可選：讓對方在合成資料上 walkthrough（螢幕＋放聲思考）  
- 文件：校內永續素養學程公開說明、差旅／盤查公開政策（若有）

---

## 6. 資料與分析（論文可重現）

| 資料 | 分析 |
|------|------|
| 課前–課後短問卷 | 描述統計；配對檢定（樣本夠才做） |
| 開放題／反思 | 主題分析 |
| 系統 log（可選） | 解析成功／失敗、操作步驟時間 |
| 訪談 | 主題編碼：促成條件、阻力、意義建構 |
| 三角 | 課堂 × 單位 × 系統行為 |

**倫理**：IRB／校內研究倫理或免除審查依輔大規定；知情同意；可撤回；資料去識別。

---

## 7. 預期貢獻（對 10639 審稿人）

1. **實證**：高教情境下，永續**行政工具**進入**素養課**的部署案例  
2. **設計知識**：開源、可檢查假設的碳工具作為 ESD 教具的設計原則  
3. **採用知識**：永續單位對行政數位工具的信任、技能、制度條件  
4. **在地**：繁中 free-text 行政文件＋台灣大學素養學程時間點  

**非宣稱**：全國代表性；係數法定最優；取代正式盤查軟體。

---

## 8. 論文結構（建議章節）

1. Introduction（學程窗口＋行政數位化＋研究缺口）  
2. Related work（EdTech in HE；ESD／碳素養；IS adoption in universities；HEI carbon tools 簡述）  
3. The tool as boundary object（系統一節，引用 GitHub）  
4. Study design（課＋單位；倫理）  
5. Findings（採用條件；學習與回饋；設計意涵）  
6. Discussion（對 10639：ICT–education；對實務：學程與永續治理）  
7. Limitations & conclusion  

---

## 9. 時程（配合 A+C）

| 階段 | 內容 |
|------|------|
| 4 週內 | 定課名／時段；合成教材包；問卷 v0.1；倫理路徑 |
| 一學期內 | 至少 **1 班試教**＋ **2–3 位**永續／行政訪談 |
| 課後 6–8 週 | 分析＋ Paper E 初稿 |
| 並行 | Paper S 蒐集去識別行政案例（不同證據） |

---

## 10. 標題與關鍵詞草案

**Keywords**: higher education; educational technology; sustainability literacy; technology adoption; carbon literacy; open-source software; Scope 3; Taiwan  

**Abstract 骨架（80 字英）**  
We report a dual deployment of an open travel-carbon workflow as (i) an administrative digital tool for university sustainability offices and (ii) a teaching artefact in a sustainability literacy programme. Drawing on classroom use and staff perspectives, we analyse adoption conditions, learning opportunities, and design implications for ICT that makes Scope 3 assumptions inspectable rather than black-boxed.

---

## 11. 下一步實作清單（給作者）

- [ ] 確認可掛課的**實際課名與學期**  
- [ ] 永續素養學程公開文件連結／能力指標對照表  
- [ ] 合成教學 ledger（10–30 列）教材化  
- [ ] 問卷中英 v0.1  
- [ ] 訪談大綱 v0.1  
- [ ] 倫理／同意書草稿  
