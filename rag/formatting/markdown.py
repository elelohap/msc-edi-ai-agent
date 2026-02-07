# rag/formatting/markdown.py
import re

# Structural detectors
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")
_BULLET_RE = re.compile(r"^\s*(?:[-*]|\d+\.)\s+")
_CODE_FENCE_RE = re.compile(r"^\s*```")

# Common bad pattern: "### Heading The paragraph starts..."
# We split after a short heading title.
# This is intentionally conservative and only triggers for ### headings.
_INLINE_H3_RE = re.compile(r"^(###\s+)(.+)$")


def format_markdown_safe(text: str) -> str:
    """
    Minimal, deterministic Markdown normalizer.
    Only changes whitespace/newlines; does NOT paraphrase or reorder content.

    Fixes:
    - Inline headings: "### Title The ..." -> "### Title\n\nThe ..."
    - Reflow paragraphs: removes accidental hard wraps inside paragraphs
    - Tight bullets: removes blank lines between bullet items
    - Ensures one blank line after headings and around list blocks
    - Preserves code fences exactly
    """
      
    if not isinstance(text, str) or not text.strip():
        return text

    t = _normalize_newlines(text)
    t = _strip_trailing_spaces(t)

    t = _rejoin_split_headings(t)
    t = _split_inline_h3_headings(t)
    t = _reflow_paragraphs_preserve_blocks(t)

    # Join accidental blank-line breaks in the middle of a sentence/paragraph
    t = re.sub(r"\n\n(?=[a-z0-9])", " ", t)
    # blank line before lowercase continuation
    t = re.sub(r"\b(in|to|of|be|is|are|was|were)\n\n(?=\w)", r"\1 ", t, flags=re.IGNORECASE)

    # ADD THE re.sub FIX HERE
    t = re.sub(
    r"\n\n(\d+(?:\s+and\s+\d+)?\s+[A-Za-z]+[A-Za-z\s]*[,.;:]?)\n\n",
    r" \1 ",
    t
    )

    t = _tighten_bullets(t)
    t = _ensure_blank_line_after_headings(t)
    t = _ensure_blank_lines_around_lists(t)

    # Cap excessive blank lines (keep max 2 consecutive)
    t = re.sub(r"\n{4,}", "\n\n\n", t).strip() + "\n"
    return t

def _rejoin_split_headings(t: str) -> str:
    """
    Rejoin headings split across lines (even with blank lines).
    Example:
      ### Why the EDI
      programme?
    -> ### Why the EDI programme?
    """
    lines = t.split("\n")
    out = []
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()

        if stripped.startswith("###"):
            # find next non-empty line
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1

            if j < len(lines):
                nxt = lines[j].strip()

                # Merge only if nxt looks like heading continuation
                if (
                    nxt
                    and len(nxt.split()) <= 7
                    and not nxt.startswith(("#", "-", "*"))
                    and not _BULLET_RE.match(nxt)
                    and not re.search(r"[.!]$", nxt)  # allow '?'
                ):
                    out.append(f"{stripped} {nxt}")
                    i = j + 1
                    continue

        out.append(line)
        i += 1

    return "\n".join(out)





def _normalize_newlines(t: str) -> str:
    return t.replace("\r\n", "\n").replace("\r", "\n")


def _strip_trailing_spaces(t: str) -> str:
    return "\n".join(line.rstrip() for line in t.split("\n"))

def _split_inline_h3_headings(t: str) -> str:
    """
    Split inline H3 headings like:
      "### Programme overview The MSc..." ->
      "### Programme overview\n\nThe MSc..."

    Prefer splitting before 'The' (common pattern), otherwise fall back to a short-title split.
    """
    out = []
    for line in t.split("\n"):
        m = _INLINE_H3_RE.match(line.strip())
        if not m:
            out.append(line)
            continue

        prefix, rest = m.group(1), m.group(2).strip()

        # If it's already a short heading, keep it.
        if len(rest.split()) <= 5:
            out.append(f"{prefix}{rest}")
            continue

        # Prefer splitting right before "The " if present (case-insensitive)
        lower = rest.lower()
        the_idx = lower.find(" the ")
        if the_idx != -1:
            title = rest[:the_idx].strip()
            cont = rest[the_idx + 1 :].strip()  # keep "The ..." (remove leading space only)
            if title and cont:
                out.append(f"{prefix}{title}")
                out.append("")
                out.append(cont)
                continue

        # Fallback: first 3 words as title
        words = rest.split()
        title = " ".join(words[:3])
        cont = " ".join(words[3:]).strip()

        out.append(f"{prefix}{title}")
        out.append("")
        out.append(cont)

    return "\n".join(out)





def _reflow_paragraphs_preserve_blocks(t: str) -> str:
    """
    Joins lines inside paragraphs (hard wraps) into a single line.
    Preserves headings, bullet/numbered lines, blank lines, and code fences.
    """
    lines = t.split("\n")
    out = []
    buf = []
    in_code = False

    def flush_buf():
        nonlocal buf
        if not buf:
            return
        # Join wrapped lines with spaces (do not change words)
        out.append(" ".join(s.strip() for s in buf if s.strip()))
        buf = []

    for line in lines:
        if _CODE_FENCE_RE.match(line):
            flush_buf()
            out.append(line)
            in_code = not in_code
            continue

        if in_code:
            out.append(line)
            continue

        stripped = line.strip()

        if stripped == "":
            flush_buf()
            out.append("")
            continue

        if _HEADING_RE.match(stripped) or _BULLET_RE.match(stripped):
            flush_buf()
            out.append(line)
            continue

        # Otherwise paragraph text
        buf.append(line)

    flush_buf()
    return "\n".join(out)



def _tighten_bullets(t: str) -> str:
    """
    Remove blank lines between consecutive bullet items.
    Keeps blank lines before/after list blocks (handled separately).
    """
    lines = t.split("\n")
    out = []
    for i, line in enumerate(lines):
        if (
            line.strip() == ""
            and i > 0
            and i + 1 < len(lines)
            and _BULLET_RE.match(lines[i - 1].strip())
            and _BULLET_RE.match(lines[i + 1].strip())
        ):
            # skip blank line between bullets
            continue
        out.append(line)
    return "\n".join(out)


def _ensure_blank_line_after_headings(t: str) -> str:
    lines = t.split("\n")
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        if _HEADING_RE.match(line.strip()):
            # Ensure exactly one blank line after heading
            if i + 1 < len(lines) and lines[i + 1].strip() != "":
                out.append("")
        i += 1
    return "\n".join(out)


def _ensure_blank_lines_around_lists(t: str) -> str:
    """
    Ensure:
    - blank line before a list block (if preceding line is text)
    - blank line after a list block (if following line is text)
    """
    lines = t.split("\n")
    out = []
    for i, line in enumerate(lines):
        cur_is_bullet = bool(_BULLET_RE.match(line.strip()))
        prev = lines[i - 1] if i > 0 else ""
        nxt = lines[i + 1] if i + 1 < len(lines) else ""

        if cur_is_bullet and prev.strip() != "" and not _BULLET_RE.match(prev.strip()) and not _HEADING_RE.match(prev.strip()):
            out.append("")

        out.append(line)

        if cur_is_bullet and nxt.strip() != "" and not _BULLET_RE.match(nxt.strip()):
            out.append("")

    return "\n".join(out)
