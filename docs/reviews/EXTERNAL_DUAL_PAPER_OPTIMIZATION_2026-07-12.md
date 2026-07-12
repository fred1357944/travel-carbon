# External dual-paper optimization review (archived)

以下審查基於逐字讀完 14 份指定本機檔案（含兩份對抗審查全文；`build/application_draft.html` 與 `application_draft.md` 同源故以 md 為準；114.05.06 簡報未另開，制度事實以 `PAPER_E_curriculum_alignment.md` 已整理版為據）。

---

# 0. 一句總評

- **Paper E 成熟度：4 / 10** — 研究設計文件（大綱、教案、問卷、訪談稿、合成帳冊）完備度高，但**實證資料為零、倫理路徑未定、理論框架未收斂**。是「設計已好、田野未開」的典型。
- **Paper S 成熟度：5 / 10** — 草稿結構完整、方法誠實度優於同類（**共識**：Copilot 也如此評價 `emission_factors_notes.md`），但**無明確 RQ、無真實機構案例**，而後者是 IJSHE 的近乎硬門檻（你自己的 VENUE_MATRIX §3 也這樣寫）。
- **雙軌 salami 風險：低–中** — 設計層是低（VENUE_MATRIX §4 的切割表在多數投稿者連想都沒想時就寫好了）；但執行層有三個具體撞車點（見 §1），若不處理會升到中。

---

# 1. 雙軌邊界體檢

| #   | 撞車點                                                                                                                                                                                                            | 歸屬判定                                    | 具體改法                                                                                                                                                                                                                                                               |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **系統／pipeline 描述**：E 大綱 §8 第 3 章「The tool as boundary object」 vs S 草稿 §3 Methods 五步驟                                                                                                             | 技術細節歸 **S**；E 僅保「可共用一段」      | E 的系統節壓到 **≤1.5 頁**，只寫「與教學/採用相關的可視特徵」（`resolved=false` 旗標、screening vs `taiwan_cfp` 雙係數、開源可檢查），技術方法一律 cite S（或先 cite repo/JOSS 短文）。**[風險]** 兩篇各自完整描述 pipeline 是審稿人認定 salami 的第一訊號。           |
| 2   | **合成 gold set 結果**（kind/mode accuracy 1.0、~8.9×10⁴ km、係數敏感度）：現在只在 S §4，但 E 教案第 2 堂正好在課堂重演 screening vs taiwan_cfp                                                                  | 數字結果歸 **S**；E 只能當「教材事件」      | E 中禁止出現任何 aggregate CO₂e 對照表當 findings；可以寫「學生觀察到兩種係數表產生不同總量並討論之」（質性），不引用 S 的表格數字。                                                                                                                                   |
| 3   | **訪談資料**：`interview_guide_v0.1.md` 第 1 節（Q1–5 現況資料流、痛點）與第 4 節（Q15–16 與 ISO 盤查關係）的答案，正好能補 S 草稿被 Copilot 抓到的無證據斷言（"Manual map look-ups are slow and hard to audit"） | 訪談**整批歸 E**。這是最誘人的撞車點        | S 的痛點陳述改用文獻＋公開文件（盤查報告書、tsai2025）支撐，或降級為 "practitioner accounts reported in a companion study [cite E]" 一句帶過、**不引 quote、不做主題分析**。若 S 日後真需要 practitioner 驗證，另做一輪獨立 walkthrough（不同 protocol、不同同意書）。 |
| 4   | **學生設計回饋**（問卷 D4、第 3 堂 GitHub issue 活動） vs S §5.4 future work「user study with sustainability officers」                                                                                           | 歸 **E**（RQ3）                             | S 的 future work 該句改寫為 "usability evaluation"，勿寫成好像 S 已規劃 user study——那是 E 的資料。                                                                                                                                                                    |
| 5   | **輔大 114 永續素養（DT）制度敘事**                                                                                                                                                                               | 歸 **E** 當 Introduction 主軸；S 可共用一句 | S 的 Introduction 只留「台灣 HEI 在 ISO 14064 與淨零政策下的盤查需求」，不展開通識改革——展開了兩篇 Intro 就長得像雙胞胎。                                                                                                                                              |
| 6   |  的 0.21 vs 0.115 等）                                                                                                                                                 | 歸 **S** Methods                            | E 只能寫一句「工具明示其係數為篩檢預設而非法定係數，此透明性成為教學素材」。                                                                                                                                                                                           |
| 7   | **共同文獻**（ghgprotocol_cat6、tsai2025、mariette2022 等）                                                                                                                                                       | 見 §4 末的「不可重複當主論述」清單          | 兩篇可引同一篇，但**論證角色必須不同**（S 用它立方法、E 用它一句帶背景）。                                                                                                                                                                                             |

**[推論]** 一個好用的自我檢核：想像兩篇同時擺在同一位審稿人桌上（IJSHE 與 10639 的審稿池在「HEI sustainability」有交集），任何一張表格、一段 quote、一組數字不得同時出現在兩篇。

---

# 2. Paper E 如何再優化（Education and Information Technologies）

## 2.1 問題表

| 優先級 | 問題                                                                       | 為何傷 10639                                                                                                         | 具體改法（可執行）                                                                                                                                                                                                                                                                                                    | 預估工作量                                                                       |
| ------ | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **P0** | 訪談 n=2–3 卻扛 RQ1（採用）半壁江山                                        | 10639 收質性研究，但「2–3 位受訪者支撐一個 adoption RQ」會被寫進 major revision；adoption 文獻的質性個案通常 5–15 人 | 兩選一：(a) 把訪談擴到 **5–8 人**（永續、環安、總務出納、資訊中心、院系助理各 1–2，用大綱 Q21 滾雪球）；(b) 把 RQ1 降級為 "contextual staff perspectives"，課堂升為主體。建議 (a)——訪談比再開一班便宜                                                                                                                 | 中（每人 45 分＋逐字稿）                                                         |
| **P0** | 倫理路徑只有一行「依輔大規定」                                             | 10639 對 IRB/consent 敘述要求明確；「對自己學生施測」是 dependent relationship，需說明自願性如何不影響成績           | 開學前確定輔大研究倫理審查（或免審）管道並取得文號；問卷改由**非授課者**回收或匿名箱；教案評量表已寫「必交」但研究使用須另行同意（目前 survey A2 有做，好），補「不同意研究使用仍可交作業計分」一句                                                                                                                   | 中（行政流程，時間風險大）**[不知道]** 輔大 REC 對課堂問卷有無免審管道——需作者查 |
| **P0** | 理論框架 4 個並列未收斂（sociotechnical＋UTAUT/TAM＋boundary object＋ESD） | 10639 審稿人最常見批評之一就是 framework 大雜燴；且 n=1 班＋幾位訪談根本撐不起 UTAUT 量表                            | **主：boundary object**（Star & Griesemer）——它同時解釋「同一工具連接行政與課堂兩個社會世界」，是你設計的獨特處；**輔：carbon/sustainability literacy**（接課堂結果）。UTAUT/TAM **整個降級**為訪談編碼的 sensitizing concepts（績效預期、促成條件當 code，不當框架）；sociotechnical 併入 boundary object 的敘述即可 | 小（決策）＋中（Related work 重寫）                                              |
| **P1** | 前後測 n 小、自願填答，卻規劃「配對檢定」                                  | 一班自願樣本做 paired test 幾乎必被打「overclaim」；10639 對 quantitative rigor 敏感                                 | 定位為 **mixed-methods exploratory**：量化只做描述統計＋逐題變化圖，主證據改押「不確定性三句」「永續長 memo」「角色扮演記錄」的質性分析（教案裡本來就有這些必交產物——它們才是金礦）                                                                                                                                   | 小（分析計畫改寫）                                                               |
| **P1** | 問卷知識題天花板效應風險（見 2.3 題號級意見）                              | 課前就答對 4/5，前後測無變化空間 → RQ2「知識變化」開天窗                                                             | 見 2.3                                                                                                                                                                                                                                                                                                                | 小                                                                               |
| **P1** | 「數堂課嵌入既有課」與「永續素養學程（DT）」的對接寫法可能 overclaim       | 若課程實際不掛 DT 標籤（113 前入學生不計），寫成「素養學程內的部署」會被在地審稿人（台灣人審 10639 不少）抓          | 論文精確寫 "a module embedded in an existing course, positioned within the university's new sustainability-literacy general-education framework (DT, effective AY 114)"；投稿前把課名、掛哪個學群（V8 多元 vs 嵌入）釘死（大綱 §11 第一項未完成）                                                                     | 小                                                                               |
| **P2** | 系統 log（大綱 §6「可選」）沒有落地方案                                    | 「三角驗證：課堂×單位×系統行為」寫了卻沒資料會被問                                                                   | 最低成本版：第 2 堂操作表加「你跑了幾個目的地、幾個 unknown」自報欄；或工具端加一個匿名 session 計數。做不到就把「系統 log」從設計中刪掉，別留空頭支票                                                                                                                                                                | 小–中                                                                            |
| **P2** | 教學 ledger 缺「金額」欄                                                   | 第 1 堂要討論 spend-based 的問題，但 `teaching_ledger_40.csv` 沒有金額欄，學生無從對比                               | 加一欄合成「核銷金額」（刻意讓兩筆同目的地不同金額），distance vs spend 的討論才有素材                                                                                                                                                                                                                                | 小（1 小時）                                                                     |

## 2.2 RQ 改寫句（3 個，供定稿選 2–3）

1. **RQ1（採用）**：「在台灣一所綜合大學通識『永續素養』改革啟動初期，永續與行政人員如何評估一個開源差旅碳行政工具的可採用性？資料實踐、信任與治理安排如何形塑其判斷？」（英：*How do sustainability and administrative staff at a Taiwanese comprehensive university appraise the adoptability of an open-source travel-carbon tool, and how do data practices, trust, and governance arrangements shape these appraisals?*）——比原句好在把「條件」具體化為三個可編碼構念，且嵌入制度時間點。
2. **RQ2（教學）**：「在三堂嵌入式模組中，學生對 Scope 3 差旅碳的概念理解，以及對工具輸出的批判性評估（辨識不確定性來源、判斷可用場合），呈現何種變化與樣態？」——把原本模糊的「知識與態度如何變化」拆成「概念理解」＋「批判性評估」，後者正對 C6 反向題與「不確定性三句」的資料。
3. **RQ3（設計）**：「行政與課堂兩側的使用回饋，收斂出哪些『使假設可被檢查』（inspectable-assumption）的永續行政 ICT 設計原則？」——把大綱裡的括號舉例（解析失敗可見性、係數透明、隱私）留到 Findings 再歸納，RQ 本身不預載答案。

## 2.3 問卷 v0.1 題號級增刪

**改**：
- **B1**：選項 c「（如差旅、通勤等…）」把答案寫在選項裡，天花板主因之一。改為只寫「價值鏈上其他間接排放」，把例子拿掉；干擾項 d 換成「凡是外包出去的排放都不用算」這類似是而非句。
- **B2**：題幹已說「出差」，選項 c 又寫「業務差旅相關」＝送分。干擾項改成「a) Scope 1，因為是學校付錢 b) Scope 2，因為是外購服務 c) Scope 3 d) 視有無過夜而定」。
- **B3**：c、d 都帶「一定」，考試老手秒殺。至少一個干擾項要有真實迷惑性，如「spend-based 需要每筆的距離資料」。
- **C5** 保留但明確定位為「自評回饋」，不得寫成學習成效證據。

**增**：
- **B7（新，僅課後，開放）**：「請列出本工具輸出的**兩個**不確定性來源。」——這是學習目標 3 的直測題，現在全卷竟沒有；也直接產生可編碼資料。
- **B8（新，情境題）**：「某列目的地顯示 unknown、距離 0 km。若直接加總全校排放，總量會偏高還是偏低？為什麼？」——比 B4 難一階，防天花板，且正對工具的核心設計論點。
- **C7（新，與 C6 成對）**：「工具輸出需要人工檢核後才能放進正式報告」（Likert）——單靠 C6 一題撐「批判素養」太薄，兩題才勉強成一個微構念。
- **A6（新，背景）**：「是否修過統計／程式相關課程」——上機表現的明顯混淆變數，不問就無法在 Findings 排除。
- **A7（新，課後）**：「你實際完成幾個目的地的計算？」——劑量（dose）自報，替代做不出的系統 log。

**刪／降**：無題需刪；D 區保留（D4 是 RQ3 主資料源，好設計）。

**程序**：配對用「自產代碼」（母親生日＋學號末兩碼之類）取代學號雜湊——雜湊仍屬可還原個資爭議區，10639 審稿人有人會挑。**[推論]**

## 2.4 訪談大綱要補的 3 問

1. **反事實（插在 Q5 後）**：「如果明年就被要求交差旅碳數字、而不用這類工具，您實際上會怎麼做？要花多少人力？」——沒有這題，「工具 vs 現狀」的採用論證缺基準線。
2. **採用決策鏈（插在 Q15 後）**：「假設要正式導入，需要誰核准、走什麼程序、大約多久？過去有沒有類似（免費/開源）工具走完這流程的前例？」——sociotechnical/boundary-object 分析需要制度程序的實料，現有 Q15 只問「誰主導」，問不到程序。
3. **資料治理具體化（插在 Q16 後）**：「若把真實報帳資料餵給這個工具跑，需要什麼授權？您最擔心的是哪些**欄位**（姓名、事由、金額…）？工具輸出您願意放進永續報告書的哪一層——附錄參考、正式數字、還是不放？」——這題同時服務 E 的信任構念，且其答案可當 Paper S 資料治理節的**設計需求**（注意：只能以「E 的發現」被 S 引用，不能雙報）。

## 2.5 理論：保留／替換裁定

- **保留並升為主**：boundary object。
- **保留為輔**：carbon literacy / sustainability literacy（對接 DT 語言與 RQ2）。
- **降級**：UTAUT/TAM → 只取 2–3 個構念當訪談 code book 條目，正文不稱其為 framework。
- **併入**：sociotechnical 不單列，用一段話併進 boundary object 的理論節。
- **[風險]** 若四個都留，10639 最可能的審稿意見原話會是 "the theoretical framing is underdeveloped relative to the number of frameworks invoked"——這類意見幾乎必然伴隨 major revision。

---

# 3. Paper S 如何再優化（IJSHE 主攻）

## 3.1 問題表

| 優先級 | 問題                                                                                                                                      | 為何傷 IJSHE                                                                                                                           | 具體改法（可執行）                                                                                                                                                                                                                                                                                                 | 預估工作量                                                                      |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| **P0** | **全文沒有明確 RQ／Purpose 問句**                                                                                                         | IJSHE 是研究期刊，結構化摘要有 Purpose 但正文 Introduction 收尾沒有研究問題，會被判 "descriptive tool report"                          | Introduction 末加：*RQ1: What technical and organisational steps are required to turn free-text Traditional Chinese reimbursement ledgers into auditable distance-based Category 6 activity data? RQ2: How sensitive are resulting screening totals to factor-profile choice and unresolved-destination handling?* | 小                                                                              |
| **P0** | **無真實機構案例**（草稿 status 自己寫 "institutional de-identified case TBD"）                                                           | 你的 VENUE_MATRIX §3 已判「IJSHE 幾乎必須」；沒有它，本稿是方法＋軟體說明，desk reject 或轉投建議機率高                                | 走「**中間路徑**」（見 3.2）：申請資料治理核可，發布**一個去識別年度的過程統計**——解析成功率、unknown 率、trip-kind 分布、模式分布、係數敏感度區間——**可以不公布絕對 CO₂e 總量**。這已足構成 "institutional case"，而不必等完整盤查年度                                                                            | 大（核心缺口；行政審批時程不可控）**[不知道]** 誰有權核可去識別使用——需作者確認 |
| **P0** | §4.1 把 kind/mode accuracy **1.0 放在 Findings**                                                                                          | 即使已標 "regression metrics"，把作者自標 gold 的 1.0 當結果呈現，就是把脖子伸給循環驗證攻擊（**共識**：Copilot §3 全節；Grok 亦同意） | 整段搬進 §3.3 Quality assurance，Findings 改由三支柱撐：(i) 係數敏感度全帳冊表、(ii) failure-mode 分類與 unresolved 處理、(iii)（日後）真實年度過程統計                                                                                                                                                            | 小（搬動）＋中（敏感度擴充）                                                    |
| **P1** | 敏感度分析只有「100 km 單腿示例」                                                                                                         | "factor-dominated" 是全文最有力的論點，卻只給一個玩具例子                                                                              | 對合成 52 筆全帳冊跑 screening vs taiwan_cfp vs（航空）ICAO 式情境，加 **RFI ×1.9 情境列**（cite lee2021/jungbluth2019），出一張 tornado 或分模式對照表——這張表是本稿現階段唯一能自產的「像結果的結果」                                                                                                            | 中（1–2 天，工具已有 `sensitivity_compare`）                                    |
| **P1** | 痛點斷言無證據："operational data path… less attention"、痛點敘述繼承自 JOSS 稿的 "manual look-ups slow"（**共識**：Copilot §4 抓過同款） | IJSHE 審稿人會問 "says who?"                                                                                                           | 用兩條腿補：台灣大學公開盤查/永續報告書中差旅資料方法的**文件分析**（幾間學校、用什麼法、有無揭露資料來源）＋ tsai2025 的 data-constrained 陳述。**不要**用 E 的訪談 quote 來補（見 §1 撞車點 3）                                                                                                                  | 中（文件掃描半天–1 天）                                                         |
| **P1** | CHECK 級引用 5 筆未核（schmidt2022、schreuer2023、sunley2025、deda2025、goerlinger2023——goerlinger 連 DOI 都沒有）                        | 其中三筆是 IJSHE 自家論文，引錯自家期刊的作者名單特別難看                                                                              | 投稿前逐筆開 publisher 頁核對（CITATIONS_VERIFIED 已有此紀律，執行即可）；goerlinger2023 補齊 DOI 或降級不引                                                                                                                                                                                                       | 小                                                                              |
| **P2** | 「unresolved → unknown 已修」的宣稱與對抗審查時序                                                                                         | 草稿 §4.3 說 "no longer collapse to silent 0 km"——這是修復後狀態。**[風險]** 若審稿人跑舊版或文件殘留舊行為描述，會抓到不一致          | 在 §3.3 加一句版本釘選（"as of v0.1.x"）並確認 repo、README、docs 全部同步新行為（宣告層≠執行層——投稿前實測一次 `estimate_trip('亂字串 附輸出）                                                                                                                                                                 | 小                                                                              |
| **P2** | 與 JOSS 短文的 salami 防線                                                                                                                | 同一合成評估表若同時是 JOSS 主結果與 IJSHE 結果，違反你自己 VENUE_MATRIX 紅線「不與期刊主文重複同一結果表」                            | IJSHE 稿的合成評估只放 QA 節並 cite JOSS/repo；IJSHE 的「結果」必須是 JOSS 稿沒有的（敏感度全表＋真實年度過程統計）                                                                                                                                                                                                | 小（紀律）                                                                      |

## 3.2 「尚無完整真實年度公開結果」時的誠實 framing

**IJSHE 可接受**（[推論]，依據其近年刊登的 workflow/policy 類文章型態與你 VENUE_MATRIX 的前例欄）：
- 定位為 **"workflow development and screening-level evaluation study"**：明說本文貢獻是「從帳冊到活動數據的可稽核路徑＋係數敏感度界定＋失效模式治理」，明說不宣稱盤查結果。
- 有一個**真實年度的過程統計**（解析率、unknown 率、模式分布、距離分布），即使不公布 CO₂e 絕對值——這是「有機構、有真資料、有治理故事」與「純合成」的分水嶺。
- Discussion 落在**機構治理意涵**：誰該擁有這條資料路徑、unknown 率該成為報告書的品質指標、係數版本該如何隨盤查年度釘選。

**會被當工具廣告**：
- 功能清單＋GitHub 連結＋合成 accuracy 1.0＋「歡迎使用」；
- 用 "validated" 描述作者自標的 gold set；
- 通篇主詞是 "the tool can…" 而不是 "the institution needs… / the workflow reveals…"。
- **[風險]** 現稿約 40% 內容重心仍在軟體本身；改寫方向是把每一節的問句從「工具做什麼」轉成「機構要什麼、這條路徑暴露了什麼」。

## 3.3 現在文獻還缺的 5 類（可查主題，不編 DOI）

1. **Distance-based vs spend-based 的實證誤差比較**（企業或機構 Scope 3 方法選擇對總量的影響；搜尋 "spend-based versus activity-based scope 3 accuracy"）——CITATIONS_VERIFIED 自己已列此缺口，仍未補。
2. **Scope 3 資料品質與不確定性框架**（data quality scoring、pedigree matrix、corporate Scope 3 uncertainty；如 Klaaßen & Stoll 一系的企業 Scope 3 透明度研究）——支撐 unresolved-rate 作為品質指標的主張。
3. **東亞／非西方 HEI 碳盤查案例**（中日韓大學 carbon footprint 英文文獻）——現在的機構文獻幾乎全歐洲＋一篇台灣，「東亞行政文件情境」的 gap 主張需要對照組。
4. **中文地名解析／geoparsing 評估**（kuai2020 之外的 toponym resolution、geocoding accuracy 文獻）——目前單篇支撐整個 NLP 面向，太薄。
5. **台灣高教永續治理灰色文獻**（大學永續報告書差旅方法節、教育部淨零/USR 政策文件、SDGs 報告）——以 grey citation＋URL＋擷取日期格式進場，直接服務 3.1 P1 的痛點證據。

---

# 4. 文獻

## 4.1 Paper E 核心應讀 12–15 篇（bib 現況幾乎全是 S 向，E 要新開一條線）

| #   | 主題／代表作                                                                                          | 狀態   |
| --- | ----------------------------------------------------------------------------------------------------- | ------ |
| 1   | Star & Griesemer (1989) boundary objects 原典                                                         | 需新找 |
| 2   | Star (2010) "This is not a boundary object" 回顧（防止概念濫用被抓）                                  | 需新找 |
| 3   | Whitmarsh, Seyfang & O'Neill (2011) carbon capability, *Global Environmental Change*                  | 需新找 |
| 4   | UNESCO (2017) ESD Learning Objectives                                                                 | 需新找 |
| 5   | Wiek et al. (2011) sustainability key competencies                                                    | 需新找 |
| 6   | Venkatesh et al. (2003) UTAUT（僅作 sensitizing concepts 引用）                                       | 需新找 |
| 7   | Orlikowski (2000) technology-in-practice（sociotechnical 一段用）                                     | 需新找 |
| 8   | Selwyn 批判取向 EdTech（防「工具樂觀主義」指控）                                                      | 需新找 |
| 9   | 近 3 年 **10639 自家**的 sustainability × EdTech／tool adoption 論文 2–3 篇（投其所好＋證明對話對象） | 需新找 |
| 10  | 高教行政資訊系統採用研究（ERP/administrative IS in HE adoption）                                      | 需新找 |
| 11  | Critical data literacy 教學研究                                                                       | 需新找 |
| 12  | 台灣通識教育改革／永續通識文獻（中文可，證明在地制度脈絡）                                            | 需新找 |
| 13  | mariette2022（GES 1point5，一句背景）                                                                 | 已有   |
| 14  | tsai2025（台灣 HEI ISO 14064，一句背景）                                                              | 已有   |
| 15  | schmidt2022 或 schreuer2023 擇一（學術差旅政策，一句背景）                                            | 已有   |

## 4.2 Paper S 核心 12–15 篇

| #   | Key                                        | 狀態                       |
| --- | ------------------------------------------ | -------------------------- |
| 1–2 | ghgprotocol_cat6、ghgprotocol_scope3       | 已有                       |
| 3   | iso14064_1_2018                            | 已有                       |
| 4   | vallsval2021（HEI CF 綜述）                | 已有                       |
| 5   | vallsval2022（CO2UNV）                     | 已有                       |
| 6   | mariette2022（GES 1point5）                | 已有                       |
| 7   | kiehle2023 或 helmers2021（機構 CF 實證）  | 已有                       |
| 8   | tsai2025（台灣錨點）                       | 已有                       |
| 9   | ciers2019＋tseng2022（學術飛行）           | 已有                       |
| 10  | lee2021＋jungbluth2019（航空 non-CO₂/RFI） | 已有                       |
| 11  | deda2025（核對後用）                       | 已有（CHECK）              |
| 12  | kuai2020＋新增 geoparsing 評估 1–2 篇      | 已有＋需新找               |
| 13  | distance vs spend 實證比較                 | 需新找                     |
| 14  | Scope 3 資料品質／不確定性                 | 需新找                     |
| 15  | 台灣灰色文獻（MOENV 係數、大學盤查報告）   | 已有（GREY，補大學報告書） |

## 4.3 不可兩篇重複當主論述的 cite

- **boundary object、UTAUT、ESD/素養文獻** → E 專屬。
- **ghgprotocol_cat6、iso14064、moenv 兩筆、icao、defra、係數與 RFI 文獻** → S 專屬（E 至多在系統節出現 ghgprotocol_cat6 一次）。
- **GES 1point5 / CO2UNV / auger2021 的「工具比較」論證** → S 專屬；E 提工具背景時不做比較。
- **學術飛行減量文獻**（wynes、tseng、schreuer、schmidt、sunley）→ S 主用；E 全文至多 1 個 contextual cite。
- 兩篇 Introduction 若引用集合重疊率 >30%，就是邊界失守的量化警訊。**[推論]**

---

# 5. 寫作與結構

## 5.1 Paper E（10639，目標 8,000–9,000 字）

| 章節                                                                     | 占比 | 備註                               |
| ------------------------------------------------------------------------ | ---- | ---------------------------------- |
| 1 Introduction（制度窗口＋缺口）                                         | 12%  | DT 改革敘事在此，一頁內講完        |
| 2 Related work（EdTech×永續素養；HE 行政 IS 採用；boundary object）      | 18%  | 三線收斂到一個 g                 |
| 3 Context & the tool（≤1.5 頁）                                          | 8%   | 只寫教學/採用相關特徵，cite repo/S |
| 4 Methods（模組設計、參與者、訪談、倫理、分析）                          | 22%  | 倫理獨立小節                       |
| 5 Findings（5.1 staff appraisals／5.2 classroom／5.3 design principles） | 27%  | 質性為主幹                         |
| 6 Discussion                                                             | 10%  | 回扣 boundary object＋10639 對話   |
| 7 Limitations & conclusion                                               | 3%   | 單校、單班、自願樣本全認           |

**英文 title 3 選項**：
1. *From ledgers to literacy: adopting an open travel-carbon tool across a university's sustainability office and classroom*
2. *Making Scope 3 inspectable: an administrative carbon tool as a boundary object in sustainability-literacy teaching*
3. *Staff appraisals and classroom deployment of an open travel-carbon workflow during a sustainability-literacy curriculum reform in Taiwan*

**中文 title**：開源差旅碳工具的行政採用與永續素養教學：台灣一所綜合大學通識改革初期的課堂導入研究

## 5.2 Paper S（IJSHE，目標 7,000–8,000 字）

| 章節                                                     | 占比 | 備註                                                              |
| -------------------------------------------------------- | ---- | ----------------------------------------------------------------- |
| 1 Introduction＋RQ                                       | 12%  | 加明確 RQ（§3.1 P0）                                              |
| 2 Literature（HEI CF；Cat.6 方法；工具；資料品質）       | 18%  | 補 §3.3 的 5 類                                                   |
| 3 Institutional context & data governance                | 10%  | 新增節：台灣 HEI 報帳資料路徑、去識別程序——這節是「案例感」的來源 |
| 4 Workflow & methods（含 QA、regression 說明、係數誠實） | 25%  | accuracy 1.0 收進這裡                                             |
| 5 Results（敏感度全表；failure modes；真實年度過程統計） | 20%  |                                                                   |
| 6 Discussion & implications for HEI practice             | 12%  | unknown 率＝品質指標；係數版本治理                                |
| 7 Limitations & conclusion                               | 3%   |                                                                   |

**英文 title 3 選項**：
1. 現題保留（已相當好）：*From free-text reimbursement ledgers to Scope 3 Category 6 distances: an open workflow for Taiwanese higher-education business-travel carbon accounting*
2. *Auditable by design: distance-based screening of business-travel emissions from Traditional Chinese free-text ledgers in higher education*
3. *Turning messy travel ledgers into Category 6 activity data: workflow, factor sensitivity, and governance implications for Taiwanese universities*

**中文 title**：從自由文本報帳帳冊到 Scope 3 類別六：台灣高教差旅碳距離法的開源工作流、係數敏感度與治理意涵

---

# 6. 資料與倫理紅線 checklist

**課堂（5 條）**
1. 真實報帳資料與任何可識別個資**永不**進課堂與 repo（教案已載明——維持並每堂投影）。
2. 研究參與（問卷）與課程成績**完全脫鉤**，不同意研究使用者作業照常計分（survey A2 已有，正文須寫明操作方式）。
3. 授課者不得在成績確定前接觸可識別的同意名單（用自產代碼＋第三方或密封回收）。
4. 未取得倫理審查（或免審）文號前，**不得**開始蒐集任何進論文的資料——試教可先跑，但那批資料只能算 pilot、不進 Findings。
5. 學生開 GitHub issue 屬**公開發言**：須告知其公開性、允許匿名帳號、且論文引用 issue 內容前取得該生同意。

**訪談（5 條）**
1. 逐字稿去識別到「角色層」（永續承辦 A），單位小到角色即可識人時，連角色都要模糊化。
2. 錄音須逐次明示同意；拒錄改筆記（大綱已有——執行時不得「先錄再問」）。
3. 受訪者可撤回至指定期限（寫進同意書，如分析定稿前）。
4. 訪談中若出現對特定同仁／主管的負評，引用時一律去脈絡化處理，不得可回溯。
5. walkthrough 一律用合成 CSV；受訪者若主動打開真實檔案，研究者當場停止記錄該段。

**行政資料（Paper S，5 條）**
1. 真實帳冊的去識別使用需**書面**治理核可（誰核可、範圍、年度）留檔，論文倫理節引用之。
2. 去識別最低標準：移除姓名、工號、單位到院級以下、事由自由文字（只留解析後地名與模式）；**金額欄一併考慮移除**（可回推個人）。
3. 原始檔不離開校方控制環境；repo 與論文附檔只出現聚合統計。工作目錄現存的大型真實輸出 xlsx（Copilot 審查提及 195MB/307MB 級檔案）**[風險]** ——確認永不入 git 之外，投稿附 repo 前做一次 `git ls-files` 全掃。
4. 公布層級分級：解析率／分布統計（低敏）→ CO₂e 總量（中敏，需核可）→ 任何單位別明細（不公布）。
5. 「已修 bug 後重跑」不得覆蓋治理核可的資料版本——分析用資料集釘版本＋雜湊，確保可重現且可稽核。

---

# 7. 12 個月「好文章」時程（2026Q3–2027Q2）

| 季                        | Paper E                                                                                                                | Paper S                                                                                                                  | 共同                                                                                                                   |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| **2026 Q3**（現在–開學）  | 釘課名/學期/學群歸屬；倫理送件；問卷 v0.2（納 §2.3 修改）＋找 3–5 人 pilot 填答修題；訪談對象名單擴到 5–8、先試訪 1 人 | 向校方提出去識別年度資料的治理申請（時程最不可控，**現在就送**）；合成全帳冊敏感度表＋RFI 情境做出來；核 5 筆 CHECK 引用 | teaching ledger 加金額欄；repo 個資全掃                                                                                |
| **2026 Q4**（115-1 學期） | 試教 3 堂＋前後測＋質性產物蒐集；訪談 5–8 人完成                                                                       | 若核可下來：跑真實年度，產出解析率/分布/敏感度過程統計                                                                   | （可選）JOSS：2027-01 起滿六個月公開史（**共識**：Copilot 的 desk-reject 判斷；Grok 註記以當日官方政策為準——投前重查） |
| **2027 Q1**               | 編碼與分析；E 全文初稿；內部對抗審查一輪                                                                               | S 依真實過程統計改寫 Results/Discussion；文件分析補痛點證據                                                              | 兩稿並排掃引用重疊與句式指紋                                                                                           |
| **2027 Q2**               | 修訂→**投 10639**                                                                                                      | E 送出後 4–6 週內**投 IJSHE**（時間差＋內容差雙保險）                                                                    | cover letter 各自聲明 companion paper 的存在與分工（主動揭露是最好的 salami 防禦）                                     |

**最早可認真投的前提條件（非日期）**：
- **E**：① 倫理核可文號在手；② ≥1 班完整試教且前後測配對可用；③ ≥5 位不同角色訪談完成編碼；④ 理論收斂為 boundary object＋literacy 且 Related work 有 2–3 篇 10639 自家對話文獻。四者缺一不投。
- **S**：① 至少一個去識別真實年度的過程統計獲准發表；② 全帳冊係數敏感度＋RFI 情境表完成；③ 5 筆 CHECK 引用全數核畢；④ Findings 中不再有作者自標 accuracy 當結果。四者缺一不投（缺 ① 而想早投 → 只剩 Sustainability 工具向路線，需你明示接受 APC 與定位降級）。

---

# 8. 給作者的 7 個澄清問題

1. **課的實體**：下學期嵌入的是哪門課、修課人數約多少、你本人是否為授課者之一？（授課者身分直接改變倫理設計與問卷回收方式）
2. **倫理管道**：輔大對「課堂匿名問卷＋職員訪談」這類低風險研究，有免審/簡審機制嗎？你或主任走過一次嗎？預估時程？
3. **行政資料治理**：真實帳冊的資料擁有者是誰（總務？出納？）？「去識別後發表過程統計（不含 CO₂e 總量）」這個層級，你判斷拿得到核可嗎？
4. **訪談可及性**：可約的永續／行政對象實際名單有幾人、涵蓋哪些角色？擴到 5–8 人現實嗎？
5. **E 的方法重心**：你想把 E 寫成質性為主（boundary object 敘事，前後測僅輔助），還是堅持混合方法有量化成分？這決定問卷還要投資多少。
6. **署名**：主任／統計系老師的參與會到共同作者層級嗎？（依你的 AUTHORSHIP 預設是獨作；但共同設計課程＋共同施測若不掛名，反而有貢獻歸屬疑慮——需早定，也影響兩篇的作者列是否相同、進而影響 salami 觀感）
7. **S 的時程底線**：若治理核可拖過 2027 Q1，你要 (a) S 順延等真實資料（維持 IJSHE 定位），還是 (b) 轉投 Sustainability 接受「工具＋合成驗證」定位＋APC？現在給傾向，我後續建議會照這條路徑收斂。

---

**與 Copilot 敵意審查的對照**：靜默零排放 bug、合成 gold 循環性、公開歷史短、係數誠實值得肯定——四項**共識**且本文沿用；「六個月必 desk reject」僅適用 JOSS，**不適用** 10639/IJSHE（期刊無此 gate），此處**反對**將其外推到期刊軌；「CFP 應設為預設」我持保留（**部分反對**：對論文而言關鍵是揭露＋敏感度，預設值選擇是軟體政策，可在 S 的 Discussion 承認為 open policy question 而非投稿前必改）。
