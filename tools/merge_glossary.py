"""Add a Note's Key terms to glossary.md (terms already there are kept as they are).
Usage: python tools/merge_glossary.py 46-curse-of-dimensionality"""
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
folder = sys.argv[1].rstrip("/")
video = int(folder.split("-")[0])
note = (root / folder / "note.md").read_text()
terms = note.split("Key terms", )[-1]
new = [r for r in re.findall(r"^\| (.+?) \| (.+?) \|$", terms, re.M) if r[0] not in ("Term", "---")]
gloss = root / "glossary.md"
head, table = gloss.read_text().split("|---|---|---|\n")
rows = [r for r in table.splitlines() if r.startswith("| ")]
have = {r.split(" | ")[0][2:].lower() for r in rows}
added = [f"| {t} | {m.rstrip('.')}. | [{"Video" if int(video) < 200 else "Maths Note"} {video}]({folder}/note.md) |" for t, m in new if t.lower() not in have]
rows = sorted(rows + added, key=lambda r: r[2:].lower())
gloss.write_text(head + "|---|---|---|\n" + "\n".join(rows) + "\n")
print(f"added {len(added)} of {len(new)} terms")
