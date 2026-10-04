"""Add a Note's Key terms to glossary.md (terms already there are kept as they are).
Every glossary row has a fixed ID (G-118) that Notes cite after a term; new terms take the next free number.
Usage: python tools/merge_glossary.py ML/05-dimensionality/ML-045-curse-of-dimensionality
       python tools/merge_glossary.py --id "learning rate"     prints the term's ID"""
import fcntl
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
gloss = root / "glossary.md"
lock = open(root / ".glossary.lock", "w")
fcntl.flock(lock, fcntl.LOCK_EX)          # several agents merge at once: one at a time, so IDs never collide
head, table = gloss.read_text().split("|---|---|---|---|\n")
rows = [r for r in table.splitlines() if r.startswith("| ")]
ROW = re.compile(r'^\| <span id="G-(\d+)">G-\d+</span> \| (.+?) \| ')
ids = {ROW.match(r).group(2).lower(): int(ROW.match(r).group(1)) for r in rows}

if sys.argv[1] == "--id":
    q = sys.argv[2].lower()
    hits = [(t, i) for t, i in ids.items() if t == q] or [(t, i) for t, i in ids.items() if q in t]
    print("\n".join(f"G-{i}  {t}" for t, i in hits[:10]) or "not found")
    sys.exit()

folder = sys.argv[1].rstrip("/")
name = Path(folder).name                            # ML-045-curse-of-dimensionality
note = (root / folder / f"{name}.md").read_text()
terms = note.split("Key terms")[-1]
new = [r for r in re.findall(r"^\| (.+?) \| (.+?) \|$", terms, re.M) if r[0] not in ("Term", "---")]
nxt = max(ids.values(), default=0) + 1
added = []
for t, m in new:
    if t.lower() in ids or re.search(r"G-\d+", t + m[:12]):     # known term, or the row already cites its ID
        continue
    added.append(f'| <span id="G-{nxt}">G-{nxt}</span> | {t} | {m.rstrip(".")}. | [Note {name[:6]}]({folder}/{name}.md) |')
    ids[t.lower()] = nxt
    nxt += 1
rows = sorted(rows + added, key=lambda r: ROW.match(r).group(2).lower())
gloss.write_text(head + "|---|---|---|---|\n" + "\n".join(rows) + "\n")
print(f"added {len(added)} of {len(new)} terms")
