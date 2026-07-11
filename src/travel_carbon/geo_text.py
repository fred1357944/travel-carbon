"""Lightweight Traditional Chinese place-text normalization helpers."""

from __future__ import annotations

import re
from typing import Optional

# Common administrative suffixes stripped before gazetteer lookup
_ADMIN_SUFFIX_RE = re.compile(
    r"(市|縣|區|鎮|鄉|村|里|街|路|段|巷|弄|號)+$"
)

# Characters often garbled in legacy Excel exports (subset used by extractor)
_GARBLED_RE = re.compile(r"[䀭닌ꆟ㝤䀔鶿篸캄ꇀ㝤Ž⸽䀋纡鸐]")


def normalize_place_text(text: Optional[str]) -> str:
    """Normalize free-text place strings for matching.

    - Coerce to str, strip
    - Remove a small set of known garbled OCR/export characters
    - Unify 台/臺 to 台 for matching (dictionary may still store both)
    """
    if text is None:
        return ""
    s = str(text).strip()
    if not s or s.lower() == "nan":
        return ""
    s = _GARBLED_RE.sub("", s)
    s = s.replace("臺", "台")
    s = re.sub(r"\s+", "", s)
    return s


def strip_admin_suffix(text: str) -> str:
    """Strip trailing Taiwan administrative suffixes (市/縣/區/…)."""
    if not text:
        return ""
    s = normalize_place_text(text)
    prev = None
    while prev != s:
        prev = s
        s = _ADMIN_SUFFIX_RE.sub("", s)
    return s
