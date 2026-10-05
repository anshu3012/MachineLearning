"""List maths that breaks NOTE-RULES §15 on a phone: calculations inside sentences, and display lines too wide.

Usage: python tools/find_inline_calc.py [Note.md ...]   (no arguments = every Note)
Prints file:line: kind: snippet, then a count. A clean Note prints nothing but "0 found".
- prose: an inline $...$ in a sentence that contains '=', a digit and an operation (a sum, product, division):
  move it to display lines, one step per line. Naming one value ("$h = 0.6$") is fine and not listed.
- wide: a one-line $$...$$ whose visible maths is over 40 characters: split it, one operation per line.
"""
import glob
import re
import sys

OP = re.compile(r"[\d)}]\s*[-+*/×]\s*[\d(\\{]|\\times|\\cdot|\\frac|\\sqrt")
INLINE = re.compile(r"(?<!\$)\$([^$]+)\$(?!\$)")


def visible(tex):
    """Rough count of characters a reader sees: drop commands, braces and spaces."""
    tex = re.sub(r"\\(text|mathrm|operatorname)\{([^}]*)\}", r"\2", tex)
    return len(re.sub(r"\\[a-zA-Z]+|[{}\\ ^_&]|\\,", "", tex))


def scan(path):
    out = []
    block = None                          # (start line, body lines) inside a multi-line "$$ / body / $$" display
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        s = line.strip().lstrip("> ").strip()
        if s == "$$":                     # github_math.py writes some displays (e.g. inside lists) over three lines
            if block is None:
                block = (n, [])
            else:
                body = " ".join(block[1])
                if visible(body) > 40 and "\\begin{" not in body:
                    out.append((block[0], "wide", body[:90]))
                block = None
            continue
        if block is not None:
            block[1].append(s)
            continue
        if s.startswith("$$") and s.endswith("$$") and len(s) > 4:
            if visible(s[2:-2]) > 40:
                out.append((n, "wide", s[:90]))
            elif re.search(r"\\qquad\s*[^,\s]", s) and s.count("=") >= 2:
                out.append((n, "side-by-side", s[:90]))     # two results on one line (§15)
        elif s and not s.startswith(("|", "!", "<", "#", "```")):
            for m in INLINE.findall(s):
                if "=" in m and re.search(r"\d", m) and OP.search(m):
                    out.append((n, "prose", m[:90]))
    return out


if __name__ == "__main__":
    assert visible(r"\frac{a}{b} = 2") == 4                          # self-check: "ab=2"
    assert OP.search("0.524 + 0.6 = 1.124") and not OP.search("h = 0.6")
    files = sys.argv[1:] or sorted(f for f in glob.glob("*/*/*-[0-9][0-9][0-9]-*/*.md"))
    total = 0
    for f in files:
        for n, kind, snip in scan(f):
            print(f"{f}:{n}: {kind}: {snip}")
            total += 1
    print(f"{total} found")
