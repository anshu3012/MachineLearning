"""Generate every Note's Key terms table from the glossary (docs/STRUCTURE.md, CONTEXT.md "Key terms").
Rows: the terms whose Home is this Note, then recaps (terms the Note cites or names, taught elsewhere) linked to
their Home. The meaning always comes from the glossary, so the two never drift apart.
Usage: python3 tools/key_terms.py [--check]      (run by course_map/build_map.py; --check: exit 1 if stale)"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROW = re.compile(r'^\| <span id="(G-\d+)">G-\d+</span> \| (.*?) \| (.*?) \| \[[^\]]*\]\(([^)#]+)(?:#([^)]*))?\) \|')
INTRO = "Terms taught in this Note come first; linked terms are recaps, taught in the Note the link opens."


def glossary():
    out = {}
    for line in (ROOT / "glossary.md").read_text(encoding="utf-8").split("\n"):
        m = ROW.match(line)
        if m:
            out[m.group(1)] = dict(term=m.group(2), meaning=m.group(3), path=m.group(4), anchor=m.group(5) or "")
    return out


def table(note, g, by_name):
    rel = note.relative_to(ROOT).as_posix()
    text = note.read_text(encoding="utf-8")
    parts = re.split(r"(?m)^(## \d+\. Key terms[ \t]*\n)", text, maxsplit=1)
    if len(parts) < 3:
        return None
    body, old = parts[0], parts[2].lstrip("\n")
    first = {}
    for m in re.finditer(r"\bG-\d+\b", body.split("<!-- /where-this-fits -->")[-1]):
        first.setdefault(m.group(0), m.start())
    named = []
    for t, _ in re.findall(r"^\| (.+?) \| (.+?) \|$", old, re.M):
        code = re.search(r"G-\d+", t) or None
        key = re.sub(r"\s*\(G-\d+\)|\[|\]\([^)]*\)", "", t).strip().lower()
        c = code.group(0) if code else by_name.get(key)
        if c in g:
            named.append(c)
    homed = [c for c, e in g.items() if e["path"] == rel]
    recap = [c for c in dict.fromkeys(list(first) + named) if c in g and c not in homed]
    end = len(body) + 1
    homed.sort(key=lambda c: first.get(c, end))
    recap.sort(key=lambda c: first.get(c, end))
    up = os.path.relpath(ROOT, note.parent)
    rows = [f"| {g[c]['term']} ({c}) | {g[c]['meaning']} |" for c in homed]
    rows += [f"| [{g[c]['term']}]({up}/{g[c]['path']}{'#' + g[c]['anchor'] if g[c]['anchor'] else ''}) ({c}) "
             f"| {g[c]['meaning']} |" for c in recap]
    if not rows:
        return None
    tail = re.split(r"(?m)^## ", old, maxsplit=1)
    rest = "## " + tail[1] if len(tail) > 1 else ""
    new = f"{INTRO}\n\n| Term | Meaning |\n|---|---|\n" + "\n".join(rows) + "\n" + ("\n" + rest if rest else "")
    return parts[0] + parts[1] + "\n" + new.rstrip("\n") + "\n"


def main(check=False):
    g = glossary()
    by_name = {re.sub(r"\s*\(G-\d+\)", "", e["term"]).strip().lower(): c for c, e in g.items()}
    stale = []
    for note in sorted(ROOT.glob("[MD][AL]/**/[A-Z][A-Z]-[0-9][0-9][0-9]-*.md")):
        if note.stem != note.parent.name:
            continue
        new = table(note, g, by_name)
        if new and new != note.read_text(encoding="utf-8"):
            stale.append(note.relative_to(ROOT).as_posix())
            if not check:
                note.write_text(new, encoding="utf-8")
    print(f"key_terms: {len(stale)} {'stale' if check else 'rewritten'}")
    if check and stale:
        print("\n".join(stale[:20]))
        sys.exit(1)


if __name__ == "__main__":
    main("--check" in sys.argv)
