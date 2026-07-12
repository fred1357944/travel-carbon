# Source: GitHub Copilot CLI adversarial review (read-only)

# Adversarial Peer Review — `travel-carbon` (JOSS / SoftwareX track)

**方法**：實際執行 `pytest`（48 passed）、`travel_carbon.eval_batch`、`git log`/`git show`、GitHub API（`gh api repos/fred1357944/travel-carbon`）、比對 JOSS 官方 `submitting.html` / `review_criteria.html` / `paper.html`（現行版本，2026 年）。以下每項均附檔案路徑與可重現指令。

---

## 1. Fatal risks（會擋 accept / 逼 major revision，甚至 desk reject）

**這是最嚴重的一項：本專案在目前狀態下，依 JOSS 現行 pre-review screening gates，會被自動 desk reject，連 review 都不會開始。**

- `gh api repos/fred1357944/travel-carbon` 回報 `created_at: 2026-07-11T15:13:32Z`，`git log --oneline --all` 只有 **8 個 commit**，全部落在 2026-07-11～07-12 兩天內。JOSS `submitting.html` 明文：「*The repository must have been public for more than six months prior to submission... A repository made public immediately before submission, or one showing development concentrated into a few days or weeks, will [receive desk rejection]... We run automated checks on commit distribution — a repo dump is not a history.*」— 這個 repo 就是官方範例裡描述的「反例」本身。
- `docs/PATH_A_PROGRESS_2026-07-11.md` 自己承認：全部 library、48 tests、paper、CI、GitHub repo 都是「Loop 1–9」在同一場 session 內生出來的（"not git-committed" 反覆出現）。這份文件如果被 reviewer 看到，等於作者自證「rapid, recent code generation」——JOSS review criteria 對 Development timeline 的 *Not acceptable* 定義。
- Repo 現況：0 stars、0 forks、0 watchers、0 open issues（`gh api` 實測）。JOSS gate 2「Demonstrated research impact」要求至少作者自己有使用證據，「Aspirational statements about future use are not sufficient」——而 `paper.md` 唯一的「未來使用」敘述就是 aspirational（"remain recommended future work"）。
- 沒有 `CONTRIBUTING.md`、`SUPPORT`、issue template（`find . -iname "CONTRIBUT*"` 無結果，`.github/` 只有 `workflows/`）。JOSS review checklist 明確要求「Community guidelines」；review_criteria.html 對單作者專案的最低門檻是「a meaningful public commit history over time, tagged releases..., a CONTRIBUTING file, and stated support expectations」——本專案一項都沒有。
- **AI usage disclosure 完全缺失**，但這是 JOSS **required section**（`paper.html`：「AI usage disclosure: ... If no AI tools were used, state this explicitly」）。本 repo 到處是 AI-agent 開發痕跡（`CLAUDE.md`、`docs/多AI審議_論文定位_PROMPT.md` 直接寫「複製貼上給 Claude / GPT / Gemini / Perplexity」、`PATH_A_PROGRESS` 的 Loop 結構）。若不揭露，依現行政策「may be considered an ethical breach」，後果可到「notify the authors' institutions」。這不是 nice-to-have，是投稿前必須補的合規項。
- `paper.md` 只有 648 字（見第 6 節精算），JOSS 現行要求 **750–1750 words**，且缺 4/6 required sections（State of the field / Software design / Research impact statement / AI usage disclosure）。這代表論文格式本身就不合規，不是內容深淺問題。
- 單作者、無共同作者，但主題涉及 GHG Protocol / ISO 14064-1 專業判斷。JOSS checklist 明講：「If the author list seems unexpectedly short given the scope of the work, it is appropriate to raise this.」

**結論：現在送出 = 100% 會被 editor 用上述任一條 desk reject，連審稿人都看不到論文。**

---

## 2. Methodological honesty gaps（emission factors / OSRM / geodesic / mode heuristics）

- `docs/emission_factors_notes.md` 與 `src/travel_carbon/data/factors.yaml` **誠實揭露**了自家 screening 係數與台灣官方對不上（自用車 0.21 vs CFP 0.115/0.133；國內航班 0.133「數字上等於營業小客車，不是航空」）。這是本專案最誠實的部分，值得肯定——**但**：這些誠實揭露只活在 `docs/` 和 YAML 註解裡；`paper.md` Summary/Functionality 段落用「screening」一詞把問題包裝成方法學選擇，而不是「預設值本身就是錯的、只是我們知道它錯」。Reviewer 會問：既然知道 CFP 數字更準，為何不把 CFP 設為預設、screening 設為 opt-in？現在是相反。
- **靜默零排放 bug（critical, previously undisclosed）**：實測
  ```python
  estimate_trip('完全虛構地名QQQ')  # -> kind=international, 類型=國際-未知, 距離(km)=0
  estimate_trip('asdkfjaslkdfj')     # -> 同上
  ```
  任何無法解析的地名（誤字、OCR 殘留、未收錄小地名）會落到 `src/travel_carbon/locations/resolve.py:225` 的 `return "international" if not is_domestic(d) else "mainland"`，再進 `compute_flight_distance()`（`src/travel_carbon/distance/compute.py:290-302`），因 `dest_key not in COORDINATES` 回傳 `距離(km)=0`。**碳排放量因此靜默記為 0，而不是拋錯或標記低信心**。對一個宣稱做 Scope 3 Category 6 盤查稽核的工具，這是系統性低估風險（under-reporting），而且沒有任何警告機制曝露在彙總報表層級。這比係數誤差更嚴重，因為係數誤差是「知道方向」，這個 bug 是「不知道發生了」。
- **OSRM 路徑零測試**：`grep -rn "use_osrm" tests/` 顯示全部測試呼叫都是 `use_osrm=False`；`src/travel_carbon/distance/osrm.py` 的 `get_osrm_route()` 沒有任何 mock 測試。CI（`.github/workflows/ci.yml`）跑 `eval_batch` 也沒加 `--osrm`。論文賣點之一「optional OSRM road routing」是**唯一沒被驗證過的核心能力**，而且 `osrm.py:44` 用 `except Exception: return None` 吞掉所有錯誤——同一天對同一目的地跑兩次，可能因為公共 OSRM 忙碌而悄悄切換成 geodesic×1.4，兩次結果不同，且無 log 紀錄用了哪條路徑。這直接衝擊 reproducibility。
- Geodesic×1.4 的 road factor（`src/travel_carbon/distance/geodesic.py:10`）是硬編碼常數，`ADRs/0001-use-osrm-for-routing.md` 只說「可接受誤差，差旅費計算無需精確到公尺」，沒有任何來源或驗證支持 1.4 這個倍數在台灣路網下的準確性。
- Mode heuristics（`determine_transport_mode`, `src/travel_carbon/carbon.py:182-211`）純粹是距離門檻猜測（>300km→高鐵，>500km→國內航班），`docs/emission_factors_notes.md` 已誠實寫「Not observed booking modes」，但論文正文只用一句話帶過，沒有量化這個猜測對總排放量的敏感度範圍。

---

## 3. Evaluation weakness（gold set 是合成的——敵意審稿人會怎麼講）

一個敵意審稿人的第一個問題會是：**「這個 52 筆的 gold set，label 是誰標的？跟寫 classifier 的人是不是同一個人？在同一次 session 裡嗎？」** 答案全部是「是」。

- `examples/sample_travel_gold_50.csv` 第 51 列：`完全虛構地名QQQ,international,,junk`。這是**循環驗證（circular evaluation）**的鐵證：expected_kind=international 剛好等於 classifier 對「無法解析字串」的 catch-all fallback（見第 2 節）。這不是測試「系統能不能正確辨識國際地名」，是測試「fallback 分支有沒有被改動」。`outputs/eval/report50.md` 的 `international: 20` 這個桶子裡，混了「真正解析成功的國際城市」跟「解析失敗、距離=0 的垃圾輸入」，但 kind_accuracy 把兩者算成同樣的「正確」。
- `docs/PATH_A_PROGRESS_2026-07-11.md` Loop 5 自己寫：「empty dest → unknown (fixed, was misclassified international)」——即開發者用 gold set 發現 bug 後**直接改 code 讓它符合 gold**，而不是獨立驗證。這代表 kind_accuracy=1.0 / mode_accuracy=1.0 不是「外部驗證分數」，本質是「單元測試通過率」，卻被包裝成「offline evaluation」用語（`paper.md` 第 55 行：「Offline evaluation reports kind accuracy 1.0 and mode-heuristic accuracy 1.0」），措辭上刻意模糊了兩者差異。
- 完全沒有：地名抽取的 precision/recall（README/CLAUDE.md 都強調專案核心痛點是「free-text destination extraction」，卻沒有一個測試量化抽取準確率）；沒有距離 MAPE 對照真實里程／報帳憑證；沒有跟任何真實機構帳冊做過驗證（`paper.md` 第 55 行自己承認「This is not a substitute for labelled extraction precision/recall or MAPE against independent mileages on real institutional ledgers, which remain recommended future work」）。對一個以「distance-based 優於 spend-based」為核心賣點的工具，**距離準確度從未被驗證過**，這是方法學的心臟地帶留白。
- n=52 對 22 個縣市 + 3 個離島 + ~20 個國際城市的排列組合來說覆蓋率極低，且每個 kind 只有 1-2 個代表城市（如「德國」只測「德國」本身，沒測「法蘭克福」「慕尼黑」這些在 `INTERNATIONAL_CITY_MAPPING` 裡列出的實際次級城市）。

---

## 4. Statement of need / related work（GES 1point5、CO2UNV、Auger）—— overclaim 還是 underclaim？

整體語氣刻意 hedge 得很重（"not a claim of global first inventorship"、"complementary"、"sub-pipeline"），這個誠實方向是對的，比多數 AI 輔助生成的論文負責——但敵意審稿人仍會挑出：

- **比較是敘述性的，不是實證的（no empirical benchmark）**。`paper.md` 第 37 行說 GES1point5/CO2UNV/Auger「typically with structured activity inputs」「do not target Traditional Chinese free-text... in one lightweight desktop package」——這句話沒有任何引用支持「這些工具真的處理不了中文自由文本」，作者顯然沒有實際跑過這三個工具去測試。JOSS 現行 `paper.html` 要求的 **State of the field** section 明確要求「build vs. contribute justification explaining your unique scholarly contribution and why existing alternatives are insufficient」——目前的寫法只是斷言，沒有 justification。
- 差異化利基被縮得極窄（「Traditional Chinese free-text + Taiwan island flight rules + map-backed audit trail + lightweight desktop」四個條件疊在一起才成立獨特性）——這種「疊加式利基」常被審稿人視為 gerrymandered novelty claim：只要拆開任一條件，市面上就有工具能做（例如任何 geocoding + GHG factor 的組合都能達成前三項）。
- 支撐「Taiwanese HEI 需要這個」的證據只有 `@tsai2025`（泛論 ISO 14064-1 在台灣大學的應用），**沒有任何文獻或調查支持「人工查地圖很慢很難稽核」這個核心痛點陳述**（`paper.md` 第 35 行「Manual map look-ups are slow and hard to audit」是斷言，無引用、無時間量測、無使用者訪談）。
- Underclaim 的部分（值得稱讚但也是弱點）：完全沒有量化「用這個工具比人工查表快多少 / 準多少」，導致 Statement of need 停留在「這個問題存在」層級，沒有到「這個軟體解決了多少」層級——而後者才是 JOSS 真正想看的 impact 論證。

---

## 5. Software engineering for research software（packaging、reproducibility、public OSRM）

- **兩套並行程式碼、測試覆蓋不對稱**：`src/travel_carbon/`（有 48 tests）是「JOSS packaging core」，但 README（`README.md` 第 118 行）自己承認「GUI remains the operational batch entry point」——真正被機構使用者操作的是根目錄 2469 行的 `travel_distance_calculator_gui_cached_efficient.py`、`calculate_distances.py`、`map_utils.py`、`process_travel_data_AI.py`，**這些檔案 0% 被 pytest 覆蓋**。也就是「被測試的東西」和「被使用的東西」是兩套系統，只靠 import 關係鬆散耦合，沒有整合測試證明 GUI 真的呼叫到 package 邏輯而不是自己內部複製一份。
- **`data/factors.yaml`（repo root）與 `src/travel_carbon/data/factors.yaml` 是兩份獨立檔案**（`diff` 結果：目前 byte-identical，但沒有 symlink、沒有 build-time sync 機制），未來只要改一份忘了改另一份，`_factors_yaml_candidates()`（`src/travel_carbon/carbon.py:34-40`）的搜尋順序會決定用哪一份，維護風險高。
- **`src/travel_carbon/data/mappings.py:137-139` 的 `CHINA_KEYWORDS`混入亂碼／錯字**：`烏魭木齊`（應為烏魯木齊/Urumqi）、`廚州`（無意義）、`莵田`（無意義）、`濰州`（應為濰坊/Weifang）。這極度諷刺：`geo_text.py` 的 `_GARBLED_RE` 專門用來清洗「legacy Excel exports 的亂碼字元」，但工具自己的權威資料表就含有同類缺陷。低成本、高羞辱風險的 bug，應立即修。
- **公共 OSRM 依賴無 SLA、無 backoff/retry、錯誤全吞**（`osrm.py:44` `except Exception: return None`）。`ADRs/0001-use-osrm-for-routing.md` 自己列出風險「公共服務可能在高峰期變慢」「無即時路況」，但程式碼沒有 timeout 分級重試、沒有 circuit breaker、沒有把「本次用了 OSRM 還是 fallback」記錄進最終輸出的顯著欄位（雖然 `route` 欄位技術上能看出來，但一般使用者不會去檢查）。
- **ADR-0001 標註「2024-01-01（回溯記錄）」**——即承認是 2026-07 補寫、假裝是 2024 年決策的回溯文件。這種「provenance theater」在 JOSS 現行政策下是反效果：官方明講會做「automated checks on commit distribution」，一份日期造假、實際 commit 只在最近兩天出現的 ADR，只會讓 reviewer 更懷疑整個文件體系的可信度。
- 座標資料（`src/travel_carbon/data/coordinates.py`，50KB Python literal dict）沒有來源欄位（source、retrieved-date、precision），無法稽核任一座標的正確性，也沒有對應的資料驗證測試（除了個別 spot check，如 `test_locations.py::test_coordinates_core_keys`）。
- 檔名 `process_travel_data_AI.py` 明明是 rule-based（README 第 80 行自己澄清「Rule-based location extraction CLI (*not* ML)」），卻取名帶 "AI"——這正是 `docs/JOSS_CHECKLIST.md` 自己列的「Do not claim」風險項之一（"AI / LLM extraction"），但檔名本身就製造了這個誤解，文件澄清不能完全抵銷這個訊號。
- Repo 工作目錄殘留大量真實機構產出的巨型 Excel（`出差距離計算結果_20250612_171859.xlsx` 195MB、`112出差距離計算結果_20250617_092950.xlsx` 307MB），雖然 `.gitignore` 目前擋住未追蹤，但這代表真實使用場景會產生數百 MB 的輸出檔，論文和文件完全沒討論這個規模下的效能／記憶體/瀏覽器渲染 Folium 地圖的可行性。

---

## 6. Paper writing（summary length、JOSS 要求缺漏章節）

實測（`python3` 對 `paper/paper.md` 逐節計字）：

| Section | 字數 | 狀態 |
|---|---|---|
| Summary | 214 | 存在 |
| Statement of need | 129 | 存在，但夾帶 State of the field 內容 |
| Functionality | 173 | **存在，但整節是 API 文件表格——JOSS 明文禁止**（"paper should not include software documentation such as API functionality"） |
| Quality assurance | 91 | 存在（非 required 標題，等同 Software design 但未達要求深度） |
| Acknowledgements | 34 | 存在 |
| **State of the field** | 0 | **缺（required）** |
| **Software design** | 0 | **缺（required）** |
| **Research impact statement** | 0 | **缺（required）** |
| **AI usage disclosure** | 0 | **缺（required，且有揭露義務風險，見第1節）** |
| **總字數** | **648** | **低於 JOSS 現行下限 750（上限 1750）** |

四個 required section 全缺，字數又低於下限——這不是「寫得不夠好」，是格式上不合規，editor 在 pre-review checklist 就會退回要求補件，不需要進入同儕審查。

---

## 7. Concrete paper.md rewrites（BEFORE → AFTER，5 個最高 ROI 修改）

**#1 — 補 AI usage disclosure（避免被判定 ethical breach）**

BEFORE（現況：完全沒有這一節）

AFTER（插入於 Acknowledgements 之前）：
```markdown
# AI usage disclosure

Generative AI assistants (GitHub Copilot CLI / Claude, GPT, and Gemini via
manual multi-model review, see `docs/多AI審議_論文定位_PROMPT.md`) were used
for code scaffolding, test generation, documentation drafting, and paper
copy-editing during package extraction (July 2026). The corresponding author
reviewed, ran, and validated all generated code against the test suite and
made all emission-factor, architecture, and scope decisions. No AI tool was
used for reviewer/editor correspondence.
```

**#2 — 拆出獨立 State of the field，加 build-vs-contribute 論證**

BEFORE（`paper.md` 第 37 行，混在 Statement of need 裡）：
> "Open tools such as the campus estimator of @auger2021, **CO2UNV** [@vallsval2022], and **GES 1point5** [@mariette2022] serve important laboratory- and multi-scope use cases... They do not target **Traditional Chinese free-text administrative ledgers**..."

AFTER（獨立成 `# State of the field`，補上實測依據或明確標記為未驗證的推論）：
```markdown
# State of the field

@auger2021's estimator, CO2UNV [@vallsval2022], and GES 1point5
[@mariette2022] assume structured activity inputs (booking exports, survey
forms) and, to our knowledge, none ship a Traditional Chinese free-text
normalisation layer or Taiwan-specific island/mainland routing policy. We
have not benchmarked `travel-carbon` against these tools on a shared dataset;
this claim rests on reading their public documentation, not head-to-head
testing. A build-vs-contribute assessment: contributing free-text Chinese
support upstream to GES 1point5 was considered but rejected because its
activity model assumes per-mode structured records, not raw ledger rows —
see `ADRs/` for the rejected alternatives.
```

**#3 — 加 Software design 章節，取代違規的 API 文件表**

BEFORE（`paper.md` 第 39-51 行「# Functionality」整節是模組對照表——JOSS 明文禁止把 API 文件放進論文）

AFTER（把表格移到 README/docs，論文改寫設計取捨）：
```markdown
# Software design

We chose a hybrid OSRM/geodesic distance policy over a single geocoding API
to avoid vendor lock-in and per-request cost at institutional batch scale
(hundreds of rows/year); the trade-off is that public OSRM has no SLA and
our fallback (geodesic × 1.4) is unvalidated for Taiwan road networks. We
chose a hardcoded gazetteer over live geocoding to keep the offline test
suite deterministic and avoid transmitting employee travel destinations to
third-party geocoders (privacy). The cost is a growing, hand-maintained
coordinate table (`src/travel_carbon/data/coordinates.py`) with no
provenance metadata — a known limitation, not a design virtue.
```

**#4 — Research impact statement：誠實承認目前沒有，而不是留白**

BEFORE：無此章節。

AFTER：
```markdown
# Research impact statement

`travel-carbon` has not yet been used in a published inventory or cited by
external researchers; the public repository was created in July 2026. Its
near-term significance rests on reproducible artefacts available today: an
installable package, a deterministic offline evaluation harness
(`python -m travel_carbon.eval_batch`), and CI-verified examples. We commit
to reporting real (anonymised) institutional evaluation results in a future
release once ethics/data-sharing review at the originating institution is
complete.
```

**#5 — Quality assurance：拆穿自我循環驗證，補上已知 bug**

BEFORE（第 55 行）：
> "Offline evaluation reports kind accuracy 1.0 and mode-heuristic accuracy 1.0 on that set (geodesic fallback; no public OSRM required)."

AFTER：
```markdown
Offline evaluation reports kind accuracy 1.0 and mode-heuristic accuracy 1.0
on that set. This figure should be read as a regression-test pass rate, not
an independent validation: the same author authored both the gold labels and
the classifier in the same development session, and one row intentionally
exercises the classifier's catch-all fallback (unresolved destinations are
labelled `international` with 0 km / 0 kg CO2e rather than flagged as
low-confidence — see Known limitations). This silent-zero behaviour is a
known undercount risk on real, messier ledgers and is tracked as an open
issue.
```

---

## 8. Concrete software todos（P0/P1/P2，7 天內可完成）

**P0（不修就不該考慮投稿）**
1. 修「未解析地名 → 靜默 international/0km」bug：`classify_trip_kind()`（`src/travel_carbon/locations/resolve.py:225`）改成明確回傳 `unknown`，並讓 `estimate_trip()` 在輸出加 `resolved: bool` 欄位，GUI/Excel 匯出時對 `resolved=False` 的列要顯著標紅或另列清單，不能悄悄記 0。
2. 修 `mappings.py:137-139` 亂碼字：`烏魭木齊→烏魯木齊`、`廚州`（刪除或訂正）、`莵田`（刪除或訂正）、`濰州→濰坊`。
3. 補 `paper.md` 四個 required sections（見第 7 節）並把總字數拉到 750+。
4. 補 `paper.md` 的 `authors` block 加 ORCID（`docs/JOSS_SUBMISSION.md` 已列步驟，只是沒執行）。
5. 新增 `CONTRIBUTING.md` + GitHub issue template + 一句支援管道說明——即使暫時不投 JOSS，這是「六個月開放開發」期間必須先擺出來的基本訊號。
6. **停止規劃「現在投稿」**：先接受 JOSS 現行政策要求的六個月公開迭代期，把這份 review 的 P1/P2 排進這六個月的 roadmap，而不是趕在明天投出去。

**P1（7 天內，強化誠實性與可驗證性）**
7. 幫 `get_osrm_route()`（`src/travel_carbon/distance/osrm.py`）加 mocked 單元測試（成功／逾時／非 200／格式錯誤四種情境），目前 0 覆蓋。
8. 移除 `data/factors.yaml`（root）與 `src/travel_carbon/data/factors.yaml` 的重複，改成單一來源（package 內）+ root 用 symlink 或直接刪除。
9. 重建 gold set：找非本人（或至少非同一次 session）標註至少一批新的 label，並把「測 fallback 行為」與「測真實解析」的列分開標記，避免循環驗證。
10. 為根目錄 GUI/CLI 腳本（`calculate_distances.py`、`map_utils.py`）補至少涵蓋純邏輯函式的測試，讓「真正被使用者執行的程式碼」不再是 0% 覆蓋。
11. 加 OSRM 呼叫的 timeout 分級重試 + 明確 log（哪次用 OSRM、哪次 fallback），而不是靜默 `except Exception: return None`。

**P2（可排後，但要寫進 roadmap 讓審稿人看到誠意）**
12. 把 `coordinates.py` 改成有 `source`/`retrieved_at` provenance 欄位的 CSV/YAML，而不是無來源的 Python literal。
13. 用小規模、去識別化、經倫理/資料治理審查同意的真實帳冊做一次距離 MAPE + 抽取 precision/recall 驗證，這是整個專案科學可信度最大的缺口。
14. 考慮把預設係數換成 `docs/emission_factors_notes.md` 建議的誠實 CFP 數值，把目前的 `screening` 數值改為需要顯式 opt-in 的 legacy 模式。
15. 評估自架 OSRM instance 或制定明確的公共服務速率限制應對政策（ADR-0002，目前只是「計畫中」）。

---

## 9. Accept/Reject 預測

**預測：Reject（現行狀態下極可能是 desk rejection，連不進審稿流程）。**

**信心：9/10。**

理由：JOSS 現行 `submitting.html` 的 pre-review screening gate #1（六個月公開開發歷史）是**客觀、可自動檢測**的門檻（"We run automated checks on commit distribution"），而本 repo 的 `created_at` 與 commit 分布完全落在門檻定義的「反例」裡（1-2 天內全部完成）。這一項單獨就足以在人工審查介入前被系統/editor 擋下，不需要評估論文品質或程式碼品質。即使假設審稿人跳過這個 gate 進入實質審查，論文格式本身也不合規（648 字 < 750 下限，缺 4/6 required sections），且存在未揭露的 AI usage（政策明訂的合規風險）與至少一個影響方法學可信度的靜默零排放 bug——三者疊加，即使在沒有「六個月」門檻的假設情境下，我仍會給 reject / major revision，而不是 minor revision。剩下的 1/10 不確定性來自：如果作者願意花六個月按 P0→P2 清單真實迭代、公開累積 commit 歷史、引入至少一位協作者或機構背書，這個工具本身的誠實文件（`docs/emission_factors_notes.md`）品質其實優於多數同類專案，屆時是有機會通過的。
