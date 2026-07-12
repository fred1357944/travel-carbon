# Zenodo DOI + JOSS 投稿手順

> Repo: https://github.com/fred1357944/travel-carbon  
> Release: https://github.com/fred1357944/travel-carbon/releases/tag/v0.1.0  
> Paper draft: `paper/paper.md`  
> 更新日期: 2026-07-12

本文件假設軟體本體已就緒（公開 repo、MIT、CI 綠燈、example、paper 草稿）。  
**Zenodo 與 JOSS 送出需要你在瀏覽器登入授權**；下列指令可在本機用 `gh` 輔助檢查。

---

## A. 掛 Zenodo DOI（約 10–15 分鐘）

### A1. 連結 GitHub ↔ Zenodo

1. 開啟 [Zenodo](https://zenodo.org/) → 用 **GitHub 帳號**登入（`fred1357944`）。
2. 右上角頭像 → **GitHub**（或 Settings → GitHub）。
3. 找到 **travel-carbon** → 打開 **ON**（啟用同步）。
4. 回到 GitHub release：  
   https://github.com/fred1357944/travel-carbon/releases/tag/v0.1.0  
5. 若 DOI 未自動出現：在 Zenodo 點 **Sync now** / 對該 release 按 **Publish**。

### A2. 取得 DOI 後寫回專案

DOI 形如 `10.5281/zenodo.xxxxxxx`。在本機執行（**把 DOI 換成真實值**）：

```bash
cd "/Users/laihongyi/Downloads/專案/程式專案/家誠差旅費程式"
# 例：export ZENODO_DOI=10.5281/zenodo.12345678
export ZENODO_DOI='10.5281/zenodo.XXXXXXX'

# paper front matter
python3 - <<'PY'
import os, re
from pathlib import Path
doi = os.environ["ZENODO_DOI"]
p = Path("paper/paper.md")
t = p.read_text(encoding="utf-8")
if "archive_doi:" in t:
    t = re.sub(r"archive_doi:.*", f'archive_doi: "{doi}"', t)
else:
    t = t.replace(
        "repository: https://github.com/fred1357944/travel-carbon\n",
        "repository: https://github.com/fred1357944/travel-carbon\n"
        f'archive_doi: "{doi}"\n',
    )
p.write_text(t, encoding="utf-8")
print("paper.md updated")
PY

# CITATION.cff
python3 - <<'PY'
import os
from pathlib import Path
doi = os.environ["ZENODO_DOI"]
p = Path("CITATION.cff")
t = p.read_text(encoding="utf-8")
block = f'identifiers:\n  - type: doi\n    value: "{doi}"\n'
if "identifiers:" not in t:
    t = t.rstrip() + "\n" + block
p.write_text(t if t.endswith("\n") else t + "\n", encoding="utf-8")
print("CITATION.cff updated")
PY

git add paper/paper.md CITATION.cff
git commit -m "docs: add Zenodo archive DOI"
git push origin main
```

### A3. （建議）打一個含 DOI 的 patch release

```bash
git tag -a v0.1.1 -m "v0.1.1: metadata with Zenodo DOI"
git push origin v0.1.1
gh release create v0.1.1 --title "v0.1.1" --notes "Metadata release with Zenodo DOI ${ZENODO_DOI}"
```

---

## B. JOSS 投稿前自檢（5 分鐘）

在 repo 根目錄：

```bash
python3 -m pip install -e ".[dev]"
pytest -q
python3 -m travel_carbon 台中
python3 -m travel_carbon.eval_batch \
  --gold examples/sample_travel_gold_50.csv \
  --out-dir /tmp/joss-eval
```

對照 `docs/JOSS_CHECKLIST.md`，確認：

- [x] 公開 repo + MIT  
- [x] 可安裝 + 自動化測試（CI）  
- [x] example / gold eval  
- [x] `paper/paper.md`  
- [ ] **ORCID** 填進 paper front matter（強烈建議）  
- [ ] **Zenodo DOI** 寫進 paper `archive_doi`  
- [ ] 單位署名定稿（目前：Fu Jen Catholic University）

### 填 ORCID（可選但建議）

編輯 `paper/paper.md` authors：

```yaml
authors:
  - name: Hung-Yi Lai
    orcid: 0000-XXXX-XXXX-XXXX
    corresponding: true
    affiliation: "1"
```

---

## C. 送 JOSS（你本人在瀏覽器完成）

1. 閱讀：https://joss.readthedocs.io/en/latest/submitting.html  
2. 投稿入口：https://joss.theoj.org/papers/new  
3. 表單重點：
   - **Software repository**: `https://github.com/fred1357944/travel-carbon`
   - **Software archive DOI**: Zenodo DOI  
   - **Paper**: 指向 repo 內 `paper/paper.md`（依當日 JOSS 表單欄位）  
   - 確認 software 有 **research utility** 敘事（已在 Statement of need）
4. 送出後：JOSS 會開 review issue；依 editor 意見修 paper / 軟體。

### 送出後可用 `gh` 追蹤（有 issue 連結時）

```bash
# 把 ISSUE 換成 JOSS review issue URL 或 openjournals/joss-reviews#NNNN
gh browse  # 或手動開 review issue
```

---

## D. 若暫時不送 JOSS

仍可引用：

```bibtex
@software{lai_travel_carbon_2026,
  title   = {travel-carbon: distance-based Scope 3 Category 6 helpers},
  author  = {Lai, Hung-Yi},
  year    = {2026},
  version = {0.1.0},
  url     = {https://github.com/fred1357944/travel-carbon},
  # doi   = {10.5281/zenodo.XXXXXXX}
}
```

中文技術報告／研討會可用 `docs/論文可行性與文獻研究_2026-07-11.md` 當相關工作骨架。

---

## E. 常見拒修／退件點（預先避開）

| 風險 | 我們的對策 |
|------|------------|
| 只是 script、無測試 | 48 tests + CI |
| 無 statement of need | `paper/paper.md` 已寫 |
| 宣稱 AI / 首創 | 已避免 |
| 係數宣稱法定合規 | `emission_factors_notes.md` 誠實表述 |
| 含真實差旅個資 | `.gitignore` 擋 xlsx/maps |

---

## F. 你回傳給我即可代做的下一步

貼上下列任一項，我可直接改檔 + commit + push：

1. `ZENODO_DOI=10.5281/zenodo.…`  
2. `ORCID=0000-…`  
3. 單位署名要改成「獨立開發者／某系所」的正確英文全名  
