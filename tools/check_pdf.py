"""Fail if any paragraph of a Note is missing from its PDF (LaTeX can silently push text off a page).
Usage: python tools/check_pdf.py 02-ai-vs-ml-vs-dl/note.md pdf/02-ai-vs-ml-vs-dl.pdf"""
import re
import subprocess
import sys
import unicodedata


def words(text):
    # NFKC turns PDF ligatures (the single character "ﬁ") back into plain letters.
    return re.findall(r"[a-z0-9]+", unicodedata.normalize("NFKC", text).lower())


def probes(md):
    """First 5 plain words of every prose line (skips images, tables, front matter and maths)."""
    out = []
    in_code = False
    for line in md.split("\n"):
        line = re.sub(r"^\s*(>\s*)*", "", line)          # drop block-quote markers
        if line.startswith("```"):
            in_code = not in_code                          # skip code blocks: not prose
            continue
        if in_code:
            continue
        if line.strip().startswith("<!--"):
            continue                                       # HTML comments never reach the PDF
        line = re.sub(r"^\s*([-*]|\d+\.|#+)\s*", "", line.strip())
        line = line.split("$")[0]                          # stop at maths: the PDF renders it differently
        line = re.sub(r"\*\*?|`", "", line)
        if not line or line.startswith(("![", "|", "---", "title:")):
            continue
        w = words(line)
        if len(w) >= 5:
            out.append(" ".join(w[:5]))
    return out


def missing(md, pdf_text):
    flat = " ".join(words(pdf_text))
    return [p for p in probes(md) if p not in flat]


if __name__ == "__main__":
    md = open(sys.argv[1]).read()
    pdf_text = subprocess.run(["pdftotext", sys.argv[2], "-"], capture_output=True, text=True).stdout
    lost = missing(md, pdf_text)
    for p in lost:
        print("MISSING from PDF:", p)
    sys.exit(1 if lost else 0)
