"""Section links between Notes (NOTE-RULES §17).

  python tools/section_links.py --headings <Note.md>   list the Note's sections with their anchors
  python tools/section_links.py --check [Note.md ...]  check every [text](other-Note.md#anchor) points at a real
                                                         section; also lists links with no anchor, and link texts
                                                         that contain the word "Note" (no arguments = all Notes)
Anchors follow GitHub's rule, which the site (rehype-slug) and the PDFs (pandoc gfm_auto_identifiers) share:
lower-case, drop punctuation except "-" and "_", spaces to "-". "## 4.1 Two tiny steps" -> "41-two-tiny-steps".
A heading with maths in it has an unreliable anchor: link the nearest heading without maths instead.
"""
import glob
import os
import re
import sys

LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]*?[A-Z]{2}-\d{3}-[^)\s#]*\.md)(#[^)\s]*)?\)")


def slug(text):
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)          # [x](y) -> x
    text = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"\1", text)        # _emphasis_ -> emphasis; snake_case keeps "_"
    text = re.sub(r"[*`]", "", text).strip().lower()
    return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")


def headings(path):
    out = []
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^(#{1,6})\s+(.*?)\s*$", line)
        if m:
            out.append((len(m.group(1)), m.group(2), slug(m.group(2)), "$" in m.group(2)))
    return out


def check(files):
    bad = unanchored = noteword = 0
    for f in files:
        for n, line in enumerate(open(f, encoding="utf-8"), 1):
            for text, url, anchor in LINK.findall(line):
                target = os.path.normpath(os.path.join(os.path.dirname(f), url))
                if re.search(r"\bNote\b", text):
                    noteword += 1
                    print(f"{f}:{n}: 'Note' in link text: [{text}]")
                if not anchor:
                    unanchored += 1
                    continue
                if not os.path.exists(target):
                    bad += 1
                    print(f"{f}:{n}: missing file {url}")
                elif anchor[1:] not in {h[2] for h in headings(target)}:
                    bad += 1
                    print(f"{f}:{n}: no section {anchor} in {os.path.basename(target)}")
    print(f"{bad} broken, {unanchored} without a section, {noteword} with 'Note' in the text")


if __name__ == "__main__":
    assert slug("4.1 Two tiny steps give the two columns") == "41-two-tiny-steps-give-the-two-columns"
    assert slug("2. Why **one** curve isn't enough") == "2-why-one-curve-isnt-enough"
    if sys.argv[1:2] == ["--headings"]:
        for level, text, s, maths in headings(sys.argv[2]):
            print(f"{'  ' * (level - 2)}#{s}{'   (has maths: avoid)' if maths else ''}   <- {text}")
    else:
        check(sys.argv[2:] or sorted(glob.glob("*/*/*-[0-9][0-9][0-9]-*/*.md")))
