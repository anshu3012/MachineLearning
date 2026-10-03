"""Check dl_map/concepts.yaml: unique ids, link ends exist, five link types, steps valid, names with commas quoted,
every Video covered, ml_links point at real ids in course_map/concepts.yaml. Exits 1 on any error."""
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TEXT = (HERE / "concepts.yaml").read_text()
DATA = yaml.safe_load(TEXT)
ML_IDS = {c["id"] for c in yaml.safe_load(open(HERE.parent / "course_map" / "concepts.yaml"))["concepts"]}
TYPES = ("needs", "is a kind of", "fixes", "compared with", "used in")
N_VIDEOS = sum(1 for _ in open(HERE / "playlist.txt"))
steps = DATA["steps"]
errors = []

ids = [c["id"] for c in DATA["concepts"]]
errors += [f"duplicate id {i}" for i in {i for i in ids if ids.count(i) > 1}]
errors += [f"id {i} clashes with an ML id" for i in set(ids) & ML_IDS]
for c in DATA["concepts"]:
    if set(c) != {"id", "name", "step", "videos", "status"}:
        errors.append(f"bad keys in {c['id']}: {sorted(c)} (a name with a comma must be quoted)")
    if not isinstance(c["step"], int) or c["step"] not in steps:
        errors.append(f"bad step in {c['id']}")
    if c["status"] not in ("draft", "confirmed"):
        errors.append(f"bad status in {c['id']}")
# Comma check on the raw text too: yaml would split an unquoted "a, b" name into an extra key (caught above),
# but this names the line.
for n, line in enumerate(TEXT.splitlines(), 1):
    m = re.search(r"name: ([^\"][^:]*?), step:", line)
    if m and "," in m.group(1):
        errors.append(f"line {n}: name with a comma must be quoted")

for key, right in (("links", set(ids)), ("ml_links", ML_IDS)):
    for link in DATA[key]:
        a, t, b, s = link
        if a not in ids:
            errors.append(f"{key}: unknown id {a!r} in {link}")
        if b not in right:
            errors.append(f"{key}: unknown id {b!r} in {link}")
        if t not in TYPES:
            errors.append(f"{key}: bad type in {link}")
        if s not in ("draft", "confirmed"):
            errors.append(f"{key}: bad status in {link}")

covered = {v for c in DATA["concepts"] for v in c["videos"]}
errors += [f"Video {v} has no Concept" for v in range(1, N_VIDEOS + 1) if v not in covered]
errors += [f"Video {v} is not in the playlist" for v in covered if not 1 <= v <= N_VIDEOS]

print("\n".join(errors) or f"OK: {len(ids)} Concepts, {len(DATA['links'])} links, "
      f"{len(DATA['ml_links'])} ML cross-links, {N_VIDEOS} Videos covered")
sys.exit(1 if errors else 0)
