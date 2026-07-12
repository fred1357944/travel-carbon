#!/usr/bin/env bash
# Render application draft with bibliography via pandoc.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="${ROOT}/build"
mkdir -p "$OUT"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "pandoc not found. Install: brew install pandoc"
  exit 1
fi

# Prefer application draft; fall back to JOSS short paper
SRC="${ROOT}/application_draft.md"
BIB="${ROOT}/references.bib"
if [[ ! -f "$SRC" ]]; then
  SRC="${ROOT}/paper.md"
  BIB="${ROOT}/paper.bib"
fi

echo "Building from $SRC"

# HTML with references (citeproc)
pandoc "$SRC" \
  --citeproc \
  --bibliography="$BIB" \
  --metadata link-citations=true \
  -o "$OUT/application_draft.html"

echo "Wrote $OUT/application_draft.html"

# PDF if engine available
if command -v xelatex >/dev/null 2>&1 || command -v pdflatex >/dev/null 2>&1; then
  pandoc "$SRC" \
    --citeproc \
    --bibliography="$BIB" \
    -V geometry:margin=1in \
    -o "$OUT/application_draft.pdf" 2>/dev/null \
    && echo "Wrote $OUT/application_draft.pdf" \
    || echo "PDF engine failed; HTML still available"
else
  echo "No LaTeX engine; skip PDF (HTML has rendered references)"
fi

# Also render JOSS short paper for dual-track
pandoc "${ROOT}/paper.md" \
  --citeproc \
  --bibliography="${ROOT}/paper.bib" \
  -o "$OUT/joss_paper.html" 2>/dev/null \
  && echo "Wrote $OUT/joss_paper.html" || true

echo "Done. Open: $OUT/application_draft.html"
