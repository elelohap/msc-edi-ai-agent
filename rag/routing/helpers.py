# rag/routing/helpers.py
# sanitizer + chunk parsing + requirements extraction stay here
import re
from typing import Any, Optional

LEAK_PHRASES = [
    "not in the provided documents",
    "not in the documents",
    "not in the provided sources",
    "not in my sources",
]

POSITIONING_SIGNALS = [
    r"\bengineers?\b.*\bdesigners?\b.*\binnovators?\b",
    r"\binterdisciplin(ar|ary)\b",
    r"\bmulti[-\s]?disciplin(ar|ary)\b",
    r"\bvaried backgrounds?\b",
    r"\bopen to\b.*\bbackgrounds?\b",
]
HARD_REQUIREMENT_SIGNALS = [
    r"\bis required\b",
    r"\bmust have\b",
    r"\bminimum requirement\b",
    r"\bapplicants must\b",
]

def chunks_to_text(chunks: Any) -> str:
    if not chunks:
        return ""
    parts = []
    for c in chunks:
        if isinstance(c, str):
            parts.append(c)
        elif isinstance(c, dict):
            parts.append(str(c.get("text") or c.get("content") or c.get("page_content") or ""))
        else:
            parts.append(str(c))
    return "\n".join([p for p in parts if p]).lower()

def has_any_signal(text: str, patterns: list[str]) -> bool:
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)

def extract_requirement_thing(question: str) -> Optional[str]:
    q = question.strip()
    m = re.search(r"(?:is|are)\s+(.*?)\s+(?:required|mandatory|necessary)\??$", q, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    m = re.search(r"(?:do i need|must i have)\s+(.*?)\??$", q, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return None

def sanitize_answer(ans: str, fallback: str) -> str:
    if not ans:
        return fallback

    cleaned = ans

    # Remove any leak phrases (keep as you have it)
    for p in LEAK_PHRASES:
        cleaned = re.sub(re.escape(p), "", cleaned, flags=re.IGNORECASE)

    # Normalize line endings
    cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")

    # IMPORTANT: collapse spaces/tabs within lines, but preserve newlines
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)

    # Trim trailing spaces on each line (preserve structure)
    cleaned = "\n".join(line.rstrip() for line in cleaned.split("\n")).strip()

    # Fix weird spacing before punctuation (within a line)
    cleaned = re.sub(r"[ \t]+\.", ".", cleaned).strip()

    low = cleaned.lower().strip()

    # Keep your fallback guards
    if low in {"the answer is.", "the answer is .", "the answer is"}:
        return fallback
    if len(re.sub(r"[\W_]+", "", low)) < 15:
        return fallback

    return cleaned
