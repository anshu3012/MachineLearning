"""Check the course structure (docs/STRUCTURE.md): one recorded Home per Concept and term, Builds on only earlier
in the Course order, boxes and prerequisites in step with the data, mind maps naming each Concept's Home.
Errors exit 1. Previews whose Note never explains or links the idea are warnings until every Note has its sentence.
Usage: python3 tools/check_structure.py            (run by site/build-content.sh and course_map/build_map.py)"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "course_map"))
sys.path.insert(0, str(ROOT / "tools"))
import build_map as b  # noqa: E402
from section_links import slug  # noqa: E402

errors, warnings = [], []


def heads(path):
    return {slug(h) for h in re.findall(r"^#{2,6}\s+(.*?)\s*$", path.read_text(encoding="utf-8"), re.M)}


# 1. every Concept has a Home whose section exists
for c in b.CONCEPTS.values():
    v = b.first_note(c)
    if c["home"].split("#", 1)[1] not in heads(b.note_file(v)):
        errors.append(f"{c['id']}: Home section {c['home']} does not exist")

# 2. Builds on only earlier; the box and the prerequisites line match the data
for v in b.NOTES:
    _, before, _, _, _ = b.neighbours(v)
    for cid, m in before.items():
        if b.position(m) >= b.position(v):
            errors.append(f"{b.label(v)}: builds on {b.label(m)}, which is not earlier in the Course order")
    text = b.note_file(v).read_text(encoding="utf-8")
    block, _ = b.where_block(v)
    if block not in text:
        errors.append(f"{b.label(v)}: Where this fits box is stale (run course_map/build_map.py)")
    want = sorted({b.label(m) for m in before.values()})
    got = sorted(re.findall(r"\[\[([A-Z]{2}-\d{3})", (re.search(r"(?m)^prerequisites: (.*)$", text) or [None, ""])[1]))
    if want != got:
        errors.append(f"{b.label(v)}: prerequisites {got} differ from Builds on {want}")

# 3. glossary: every term's Home section exists; its Concept (when recorded) is a known Concept
ROW = re.compile(r'^\| <span id="(G-\d+)">G-\d+</span> \| (.*?) \| (.*?) \| (.*)$')
for line in (ROOT / "glossary.md").read_text(encoding="utf-8").split("\n"):
    m = ROW.match(line)
    if not m:
        continue
    link = re.search(r"\]\(([^)#]+\.md)#([^)]+)\)", m.group(4))
    if not link:
        errors.append(f"{m.group(1)}: no Home section in its glossary link")
    elif not (ROOT / link.group(1)).exists() or link.group(2) not in heads(ROOT / link.group(1)):
        errors.append(f"{m.group(1)}: Home {link.group(1)}#{link.group(2)} does not exist")
    concept = line.rstrip().rstrip("|").rsplit("|", 1)[-1].strip()
    if "Course map](" not in line and concept.lower() not in {c["name"].lower() for c in b.CONCEPTS.values()}:
        errors.append(f"{m.group(1)}: Concept '{concept}' is missing or unknown")

# 4. Previews: the Note names the idea or links its Home outside the box (the one plain sentence)
for v in b.NOTES:
    body = b.note_file(v).read_text(encoding="utf-8").split(b.END)[-1]
    body = body.split("## ")[0] + "## ".join(s for s in body.split("## ")[1:] if not re.match(r"\d+\. (Sources|Key terms)", s))
    for cid, m in b.neighbours(v)[4].items():
        c = b.CONCEPTS[cid]
        target = f"{Path(b.NOTES[m]).name}.md"
        if target not in body and c["name"].lower() not in body.lower():
            warnings.append(f"{b.label(v)}: Preview of '{c['name']}' ({b.label(m)}) is neither explained nor linked")

# 5. mind maps: a box named for a Concept lists the Concept's Home Note
names = {c["name"].lower(): c for c in b.CONCEPTS.values()}
for tex in sorted((ROOT / "course_map" / "mindmaps").glob("*.tex")):
    for name, notes in re.findall(r"\{([^{}\\]+?)\\nt\{([^}]*)\}\}", tex.read_text(encoding="utf-8")):
        c = names.get(name.strip().lower())
        if c and b.label(b.first_note(c)) not in notes:
            errors.append(f"mind map {tex.stem}: '{name.strip()}' shows {notes}, but its Home is "
                          f"{b.label(b.first_note(c))}")

for w in warnings:
    print("warning:", w)
for e in errors:
    print("error:", e)
print(f"check_structure: {len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
