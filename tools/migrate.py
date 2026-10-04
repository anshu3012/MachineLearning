"""One-shot migration from the flat Note folders to Subjects and Chapters (docs/MIGRATION.md, ADR 0001).

Usage: python tools/migrate.py [--dry-run] <migration_map.csv>
The CSV has two columns, old,new:  50-simple-linear-regression,ML/06-regression/ML-049-simple-linear-regression
The Course map is not in the CSV: 01-course-map becomes 00-course-map/00-course-map.md.

Every text rewrite is computed first (from the files where they are now) and checked against the planned
layout, so --dry-run validates every link without touching the repo. Without --dry-run the folders are moved
with git mv, the rewritten texts are written, and the checks run again on disk (plus three sample PDF builds)."""
import csv
import posixpath
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DRY = "--dry-run" in sys.argv
COURSE_OLD, COURSE_NEW = "01-course-map", "00-course-map"
PY = sys.executable

MAP = {}                      # old folder -> new folder path (relative to ROOT), Course map included
NUM = {}                      # old Note number -> old folder (1 is 01-what-is-ml; the Course map has no number)
PENDING = {}                  # new path -> text to write after the move (also what --dry-run checks)
COUNT = Counter()
UNRESOLVED = []               # links, mentions or paths the script could not map
LOOSE = []                    # files inside Note folders that are not note.md/notebook/images/data/...
PATCHED = []                  # tool files changed

# the old number ranges behind the Concept map areas (build_map.py today); the new build_map.py works by Chapter
OLD_MATHS_TOPICS = {"descriptive": [(200, 263), (270, 271), (560, 561)], "probability": [(330, 342)],
                    "inference": [(271, 303), (570, 573)],
                    "linear_algebra": [(350, 364), (440, 441), (490, 531), (580, 581)],
                    "calculus": [(590, 630)], "likelihood": [(630, 650)]}
OLD_DL_AREAS = {"dl_basics": [(1000, 1020)], "dl_training": [(1020, 1032)], "dl_optimizers": [(1032, 1040)],
                "dl_cnn": [(1040, 1055)], "dl_rnn": [(1055, 1067)], "dl_transformers": [(1067, 2000)]}


# ---------------------------------------------------------------- helpers

def name_of(new):
    return Path(new).name


def label(old):
    """'ML-049' for a Note, 'Course map' for the Course map."""
    return "Course map" if old == COURSE_OLD else name_of(MAP[old])[:6]


def note_md(new):
    return f"{new}/{name_of(new)}.md"


def rel(target, start_dir):
    return posixpath.relpath(target, start_dir)


def read(path):
    return (ROOT / path).read_text()


def stage(new_path, text, before):
    """Queue a rewritten file under the path it will have after the move."""
    if text != before:
        COUNT["files rewritten"] += 1
    PENDING[new_path] = text


def patch(path, replacements, new_path=None):
    """Exact-string edits to a tool; every anchor must occur exactly once (fails loudly otherwise)."""
    before = read(path)
    text = PENDING.get(new_path or path, before)              # build on an earlier rewrite of the same file
    for old, new, *every in replacements:                      # (old, new, True) replaces every occurrence
        n = text.count(old)
        if n != 1 and not (every and n):
            raise SystemExit(f"{path}: anchor found {n} times, expected once:\n{old}")
        text = text.replace(old, new)
    PATCHED.append(path)
    stage(new_path or path, text, before)
    return text


def old_number(old):
    return int(old.split("-")[0])


# ---------------------------------------------------------------- 1. the map

def read_map(csv_path):
    pat = re.compile(r"^(MA|ML|DL)/\d\d-[a-z0-9-]+/(MA|ML|DL)-\d{3}-[a-z0-9-]+$")
    errors, seen = [], set()
    for row in csv.DictReader(open(csv_path)):
        old, new = row["old"].strip().strip("/"), row["new"].strip().strip("/")
        if not (ROOT / old / "note.md").is_file():
            errors.append(f"old folder missing or has no note.md: {old}")
        m = pat.match(new)
        if not m or m.group(1) != m.group(2):
            errors.append(f"new path does not fit <S>/<NN-chapter>/<S>-NNN-slug: {new}")
        if new in seen:
            errors.append(f"new path used twice: {new}")
        seen.add(new)
        MAP[old] = new
        NUM[old_number(old)] = old
    MAP[COURSE_OLD] = COURSE_NEW
    for d in ROOT.iterdir():                                  # every Note folder on disk must be in the map
        if d.is_dir() and re.match(r"\d+-", d.name) and d.name not in MAP:
            errors.append(f"Note folder not in the CSV: {d.name}")
    for subject in ("MA", "ML", "DL"):                        # gap-free numbers per Subject
        nums = sorted(int(name_of(n)[3:6]) for n in MAP.values() if n.startswith(subject + "/"))
        if nums != list(range(1, len(nums) + 1)):
            errors.append(f"{subject} numbers are not 1..{len(nums)} without gaps")
    if errors:
        raise SystemExit("migration map errors:\n" + "\n".join(errors))
    print(f"map: {len(MAP) - 1} Notes + Course map, "
          + ", ".join(f"{s} {sum(n.startswith(s) for n in MAP.values())}" for s in ("MA", "ML", "DL")))


def reverse(new_path):
    """Where a planned path lives today (for --dry-run checks)."""
    parts = new_path.split("/")
    for k in (3, 1):
        head = "/".join(parts[:k])
        old = next((o for o, n in MAP.items() if n == head), None)
        if old:
            return "/".join([old] + parts[k:])
    return new_path


def exists(new_path):
    if new_path in PENDING:
        return True
    return (ROOT / (reverse(new_path) if DRY else new_path)).exists()


# ---------------------------------------------------------------- 3 + 4. links and "Note N" mentions

NOTE_LINK = re.compile(r"\]\(((?:\.\./)*)(\d+-[a-z0-9-]+)/note\.md")
COURSE_LINK = re.compile(r"\[(?:Maths |DL )?Note 1\]\(((?:\.\./)*)01-course-map/note\.md\)")
SEP = r"(?:,| and| or| to|–| &) ?"
MENTION = re.compile(r"\b(?:Maths |DL )?(Notes?) (\d{1,4})((?:" + SEP + r"\d{1,4})*)(?![-x]|\.\d|\d)")


def rewrite_links(text, new_dir, where):
    """`](../<old>/note.md` -> the path from new_dir to the Note's new file; `](../glossary.md` likewise."""
    def sub(m):
        old = m.group(2)
        if old not in MAP:
            UNRESOLVED.append(f"{where}: link to {old}")
            return m.group(0)
        COUNT["links rewritten"] += 1
        return "](" + rel(note_md(MAP[old]), new_dir)

    text = NOTE_LINK.sub(sub, text)
    n = text.count("](../glossary.md")
    if n:
        COUNT["glossary links rewritten"] += n
        text = text.replace("](../glossary.md", "](" + rel("glossary.md", new_dir))
    return text


def rewrite_mentions(text, where):
    """'Note 50', 'Maths Note 280', 'DL Note 1038', 'Notes 6, 57 and 70' -> 'Note ML-049' style. Never 'Video N'."""
    text = COURSE_LINK.sub(r"[Course map](\g<1>01-course-map/note.md)", text)

    def one(m):
        n = int(m.group())
        if n in NUM:
            COUNT["Note mentions rewritten"] += 1
            return label(NUM[n])
        UNRESOLVED.append(f"{where}: Note {n}")
        return m.group()

    return MENTION.sub(lambda m: f"{m.group(1)} " + re.sub(r"\d{1,4}", one, m.group(2) + m.group(3)), text)


# ---------------------------------------------------------------- 6b. front matter

DATA = yaml.safe_load(open(ROOT / "course_map" / "concepts.yaml"))
CONCEPTS = {c["id"]: c for c in DATA["concepts"]}
NOTES = DATA["notes"]


def first_note(c):                                            # same rule as build_map.first_note
    maths = [v for v in c["videos"] if 200 <= v < 1000]
    return min(maths) if c["step"] == 0 and maths else min(c["videos"])


def prerequisites(n):
    """Obsidian links to the Notes that teach what this Note's Concepts need (concepts.yaml `needs` links)."""
    own = {cid for cid, c in CONCEPTS.items() if n in c["videos"]}
    vids = {first_note(CONCEPTS[b]) for a, t, b, _ in DATA["links"] if t == "needs" and a in own and b not in own}
    return sorted(f"[[{name_of(MAP[NOTES[v]])}]]" for v in vids if v in NOTES and v != n)


def video_id(n):
    """1-134 -> '12'; 1001-1090 -> 'D001'; maths 210-450 -> 'M02' when transcripts/M02.* exists; else None."""
    if n < 200:
        return str(n)
    if n >= 1000:
        return f"D{n % 1000:03d}"
    if 210 <= n <= 450:                                       # Note ID = 200 + 10 x session + part (docs/maths-plan.md)
        session = f"M{(n - 200) // 10:02d}"
        if list((ROOT / "transcripts").glob(f"{session}.*")):
            return session
    return None


def front_matter(text, old):
    if old == COURSE_OLD or not text.startswith("---\n"):
        return text
    end = text.index("\n---\n", 4)
    lines = text[4:end].split("\n")
    keep = {k: [l for l in lines if l.startswith(k + ":")] for k in ("title", "tags")}
    other = [l for l in lines if not l.startswith(("title:", "tags:", "video:", "prerequisites:"))]
    n = old_number(old)
    video, pre = video_id(n), prerequisites(n)
    COUNT["front matter: video set"] += bool(video)
    COUNT["front matter: prerequisites set"] += bool(pre)
    new = (keep["title"] + ([f"video: {video}"] if video else []) + keep["tags"]
           + ([f"prerequisites: [{', '.join(repr(p) for p in pre)}]".replace("'", '"')] if pre else []) + other)
    return "---\n" + "\n".join(new) + text[end:]


# ---------------------------------------------------------------- Notes, glossary, docs

def rewrite_notes():
    known = {"note.md", "notebook.ipynb", "images", "data", "experiments", "models", "app.py",
             ".logs", "__pycache__", ".ipynb_checkpoints"}
    for old, new in MAP.items():
        where = f"{old}/note.md"
        text = before = read(where)
        text = rewrite_links(text, new, where)
        text = rewrite_mentions(text, where)
        text = front_matter(text, old)
        stage(note_md(new), text, before)
        LOOSE.extend(f"{old}/{p.name}" for p in (ROOT / old).iterdir() if p.name not in known)


def rewrite_glossary():
    text = before = read("glossary.md")
    text = rewrite_mentions(text, "glossary.md")
    text = rewrite_links(text, ".", "glossary.md")            # its links have no ../ : (<old>/note.md)
    stage("glossary.md", text, before)


def rewrite_docs():
    skip = {"MIGRATION.md", "migration-table-draft.md"}       # these talk about the old numbers on purpose
    for p in sorted(ROOT.glob("docs/*.md")):
        if p.name in skip:
            continue
        where = f"docs/{p.name}"
        text = before = read(where)
        text = rewrite_links(text, "docs", where)
        stage(where, rewrite_mentions(text, where), before)
    text = before = read("CONTEXT.md")
    text = text.replace("It is also Note 1.", "It lives in `00-course-map/`, outside the Subjects.")
    stage("CONTEXT.md", rewrite_mentions(text, "CONTEXT.md"), before)


# ---------------------------------------------------------------- 5. images/*.tex, images/*.py, notebooks

UPS_TOOLS = re.compile(r"((?:\.\./)+)tools/")
UPS_NOTE = re.compile(r"((?:\.\./)+)(\d+-[a-z0-9-]+)/")
TOKEN = re.compile(r"(?<![\w/.-])(\d+-[a-z0-9-]+)(?![\w-])")   # a bare old folder name in text


def rewrite_tokens(text):
    """Bare old folder names (in usage lines, docstrings, .gitignore) -> new paths; `<old>/note.md` -> new file."""
    def file_sub(m):
        return note_md(MAP[m.group(1)]) if m.group(1) in MAP else m.group(0)

    def tok_sub(m):
        if m.group(1) in MAP:
            COUNT["folder names rewritten"] += 1
            return MAP[m.group(1)]
        return m.group(0)

    text = re.sub(r"(\d+-[a-z0-9-]+)/note\.md", file_sub, text)
    text = re.sub(r"pdf/(\d+-[a-z0-9-]+)\.pdf", lambda m: f"pdf/{MAP.get(m.group(1), m.group(1))}.pdf", text)
    return TOKEN.sub(tok_sub, text)


def rewrite_images():
    for old, new in MAP.items():
        for p in sorted((ROOT / old / "images").glob("*")):
            if p.suffix not in (".tex", ".py"):
                continue
            where = f"{old}/images/{p.name}"
            text = before = read(where)
            if old != COURSE_OLD:                             # Note images sit two levels deeper than before
                text, n = UPS_TOOLS.subn(lambda m: m.group(1) + "../../tools/", text)
                COUNT["tools paths rewritten"] += n
                if p.suffix == ".py":
                    text = text.replace("HERE.parent.parent", "HERE.parents[3]")

            def sub(m):
                k, other = m.group(1).count("../"), m.group(2)
                if other not in MAP:
                    UNRESOLVED.append(f"{where}: path to {other}")
                    return m.group(0)
                # k ups reached the root: from images/ when k == 2, from the Note folder when k == 1
                anchor = new if k == 1 else new + "/images"
                COUNT["cross-Note paths rewritten"] += 1
                return "../" * max(k - 2, 0) + rel(MAP[other], anchor) + "/"

            text = UPS_NOTE.sub(sub, text)
            if p.suffix == ".tex":                            # folder names in a \foreach list: 350 module_thumbs.tex
                text = re.sub(r"(?<=/)(\d+-[a-z0-9-]+)(?=/)",
                              lambda m: rel(MAP[m.group(1)], new + "/images") if m.group(1) in MAP else m.group(0), text)
                text = text.replace("{../../\\d/images/", "{\\d/images/")
            if p.suffix == ".py":
                text = rewrite_tokens(text)
            text = rewrite_mentions(text, where)
            stage(f"{new}/images/{p.name}", text, before)


def rewrite_notebooks():
    for old, new in MAP.items():
        where = f"{old}/notebook.ipynb"
        if not (ROOT / where).is_file():
            continue
        text = before = read(where)                           # raw JSON text: keeps the notebook's formatting

        def sub(m):
            if m.group(1) not in MAP:
                UNRESOLVED.append(f"{where}: path to {m.group(1)}")
                return m.group(0)
            COUNT["cross-Note paths rewritten"] += 1
            return rel(MAP[m.group(1)], new) + "/"

        text = re.sub(r"\.\./(\d+-[a-z0-9-]+)/", sub, text)
        text, n = re.subn(r'(ROOT|Path\.cwd\(\))\.parent / \\"tools\\"', r'\1.parents[2] / \\"tools\\"', text)
        COUNT["tools paths rewritten"] += n
        text = rewrite_mentions(text, where)
        stage(f"{new}/{name_of(new)}.ipynb", text, before)


# ---------------------------------------------------------------- 6. tools and course_map

def chapters_by_topic(old_ranges, subject):
    """topic -> Chapter folders, each Chapter voting with its old numbers (how build_map.py grouped them)."""
    votes = defaultdict(Counter)
    for old, new in MAP.items():
        if old == COURSE_OLD or not new.startswith(subject + "/"):
            continue
        n, chapter = old_number(old), new.split("/")[1]
        for topic, ranges in old_ranges.items():
            if any(a <= n < b for a, b in ranges):
                votes[chapter][topic] += 1
    out = defaultdict(list)
    for chapter, c in votes.items():
        out[c.most_common(1)[0][0]].append(chapter)
    return {t: sorted(chs) for t, chs in out.items()}


def update_build_map():
    maths = chapters_by_topic(OLD_MATHS_TOPICS, "MA")
    dl = chapters_by_topic(OLD_DL_AREAS, "DL")
    quoted = lambda items: "(" + ", ".join(f'"{i}"' for i in items) + ("," if len(items) == 1 else "") + ")"
    topics = ",\n                ".join(f'"{t}": {quoted(chs)}' for t, chs in maths.items())
    old_topics = '''# Maths and statistics Notes interleave topics in their numbering, so each topic lists its Note ranges.
MATHS_TOPICS = {"descriptive": [(200, 263), (270, 271), (560, 561)], "probability": [(330, 342)],
                "inference": [(271, 303), (570, 573)],
                "linear_algebra": [(350, 364), (440, 441), (490, 531), (580, 581)],
                "calculus": [(590, 630)], "likelihood": [(630, 650)]}


def maths_topic(c):
    v = first_note(c)
    return next((t for t, ranges in MATHS_TOPICS.items() if any(a <= v < b for a, b in ranges)), None)
'''
    new_topics = f'''# Maths Chapters by Concept map topic (a topic can span several Chapters).
MATHS_TOPICS = {{{topics}}}


def maths_topic(c):
    v = first_note(c)
    return next((t for t, chapters in MATHS_TOPICS.items() if subject(v) == "MA" and chapter(v) in chapters), None)


def dl_chapter(c):
    v = first_note(c)
    return chapter(v) if subject(v) == "DL" else None
'''
    dl_lambdas = [(f"lambda c: {a} <= first_note(c) < {b})" if b < 2000 else f"lambda c: first_note(c) >= {a})",
                   f"lambda c: dl_chapter(c) in {quoted(dl[area])})")
                  for area, [(a, b)] in OLD_DL_AREAS.items()]
    reps = [
        ("  01-course-map/note.md and its images", "  00-course-map/00-course-map.md and its images"),
        ('NOTES = DATA["notes"]\n', '''NOTES = DATA["notes"]


def subject(video):
    """'MA', 'ML' or 'DL': the Subject prefix of the Note's folder."""
    return NOTES[video].split("/")[0]


def chapter(video):
    return NOTES[video].split("/")[1]


def label(video):
    """'ML-049': the Note number shown in text."""
    return Path(NOTES[video]).name[:6]


def note_file(video):
    return ROOT / NOTES[video] / f"{Path(NOTES[video]).name}.md"
'''),
        ("that uses it; its home is the maths or statistics Note (200 to 999).",
         "that uses it; its home is the maths or statistics Note (Subject MA)."),
        ('maths = [v for v in c["videos"] if 200 <= v < 1000]', 'maths = [v for v in c["videos"] if subject(v) == "MA"]'),
        ("    return first_note(c) < 200\n", '    return subject(first_note(c)) == "ML"\n'),
        (old_topics, new_topics),
        *dl_lambdas,
        ('    """\'Note 7\' with a link if written, else \'Video 7 (coming)\'."""\n    if video in NOTES:\n'
         '        return f"[Note {video}]({md_dir}{NOTES[video]}/note.md)"',
         '    """A link \'Note ML-007\' if written, else the bare video number, marked coming."""\n    if video in NOTES:\n'
         '        return f"[Note {label(video)}]({md_dir}{NOTES[video]}/{Path(NOTES[video]).name}.md)"'),
        ('"\\\\documentclass[tikz,border=4pt]{standalone}\\n\\\\input{../../tools/tikz-style.tex}\\n"',
         '"\\\\documentclass[tikz,border=4pt]{standalone}\\n\\\\input{../../../../tools/tikz-style.tex}\\n"'),
        ("See the [Course map](../01-course-map/note.md).", "See the [Course map](../../../00-course-map/00-course-map.md)."),
        ("concept_list(items, '../')", "concept_list(items, '../../../')"),
        ('''    subject = ("deep-learning" if video >= 1000 else "ml" if video < 200
               else "statistics" if maths_topic({"videos": [video], "step": 0}) in ("descriptive", "probability", "inference")
               else "maths")
    return ([f"subject/{subject}"]''',
         '''    subj = {"DL": "deep-learning", "ML": "ml"}.get(subject(video)) or (
        "statistics" if maths_topic({"videos": [video], "step": 0}) in ("descriptive", "probability", "inference")
        else "maths")
    return ([f"subject/{subj}"]'''),
        ('    note = folder / "note.md"\n', '    note = note_file(video)\n'),
        ('(ROOT / NOTES[video] / "note.md").read_text()', "note_file(video).read_text()"),
        ('    return f"{video}. " + (m.group(1) if m else NOTES[video])',
         '    return f"{label(video)} " + (m.group(1) if m else Path(NOTES[video]).name)'),
        ('        rows.append(f"| {v} | {names} | {reads} | {status} |")',
         '        rows.append(f"| {label(v) if v in NOTES else v} | {names} | {reads} | {status} |")'),
        ('    out = ROOT / "01-course-map" / "images"', '    out = ROOT / "00-course-map" / "images"'),
        ('    (ROOT / "01-course-map" / "note.md").write_text(text)',
         '    (ROOT / "00-course-map" / "00-course-map.md").write_text(text)'),
        ("the perceptron Note (1004)", f"the perceptron Note ({label(NUM[1004])})"),
    ]
    text = patch("course_map/build_map.py", reps)
    # the Course map's prose names Notes by number: rewrite only inside its f-string template
    start, end = text.index('    text = f"""'), text.index('    (ROOT / "00-course-map"')
    PENDING["course_map/build_map.py"] = (text[:start] + rewrite_mentions(text[start:end], "course_map/build_map.py")
                                          + text[end:])


def update_tools():
    update_build_map()
    patch("course_map/concepts.yaml", [("(Video 1 also has 01-course-map)", "(Video 1 also has 00-course-map)")])
    text = PENDING["course_map/concepts.yaml"]
    text, n = re.subn(r"^(  \d+: )(\d+-[a-z0-9-]+)$", lambda m: m.group(1) + MAP[m.group(2)], text, flags=re.M)
    COUNT["concepts.yaml notes: rewritten"] += n
    PENDING["course_map/concepts.yaml"] = text

    patch(f"{COURSE_OLD}/images/learning_path.py", [
        ('(ROOT / bm.NOTES[v] / "note.md").read_text()', "bm.note_file(v).read_text()"),
        ("the perceptron Note (1004)", f"the perceptron Note ({label(NUM[1004])})", True),
        ('"Round 1: the Notes that 1004 builds on"', f'"Round 1: the Notes that {label(NUM[1004])} builds on"'),
    ], new_path=f"{COURSE_NEW}/images/learning_path.py")

    patch("tools/build.sh", [
        ("Usage: tools/build.sh 02-ai-vs-ml-vs-dl", f"Usage: tools/build.sh {MAP['02-ai-vs-ml-vs-dl']}"),
        ("note=${1%/}\n", 'note=${1%/}                                         # ML/01-foundations/ML-002-ai-vs-ml-vs-dl\n'
                          'name=$(basename "$note")                            # ML-002-ai-vs-ml-vs-dl: its file name\n'),
        ('github_math.py" note.md ', 'github_math.py" "$name.md" '),
        ('"$ENV/bin/pandoc" note.md -o "$root/pdf/$note.pdf"',
         'mkdir -p "$root/pdf/$(dirname "$note")"\n"$ENV/bin/pandoc" "$name.md" -o "$root/pdf/$note.pdf"'),
        ('check_pdf.py" note.md "$root/pdf/$note.pdf"', 'check_pdf.py" "$name.md" "$root/pdf/$note.pdf"'),
    ])
    patch("tools/remote_run.sh", [
        ("default command: execute notebook.ipynb into .logs/", "default command: execute the Note's notebook into .logs/"),
        ("DIR=${1%/}; shift || true\n", 'DIR=${1%/}; shift || true\nNAME=$(basename "$DIR")\n'),
        ("--output notebook notebook.ipynb}", "--output notebook $NAME.ipynb}"),
        ('"mkdir -p $RROOT" 2>/dev/null', '"mkdir -p $RROOT/$DIR" 2>/dev/null'),
        ("project-root .logs/<ID>-notebook.ipynb", "project-root .logs/<Note>-notebook.ipynb"),
        ('"$ROOT/.logs/${DIR%%-*}-notebook.ipynb"', '"$ROOT/.logs/$NAME-notebook.ipynb"'),
    ])
    patch("tools/merge_glossary.py", [
        ("Usage: python tools/merge_glossary.py 46-curse-of-dimensionality",
         f"Usage: python tools/merge_glossary.py {MAP['46-curse-of-dimensionality']}"),
        ('video = int(folder.split("-")[0])\nnote = (root / folder / "note.md").read_text()',
         'name = Path(folder).name                            # ML-045-curse-of-dimensionality\n'
         'note = (root / folder / f"{name}.md").read_text()'),
        ('kind = "Note" if video < 200 else "Maths Note" if video < 1000 else "DL Note"\n', ""),
        ("[{kind} {video}]({folder}/note.md)", "[Note {name[:6]}]({folder}/{name}.md)"),
    ])
    patch("tools/check_pdf.py", [
        ("Usage: python tools/check_pdf.py 02-ai-vs-ml-vs-dl/note.md pdf/02-ai-vs-ml-vs-dl.pdf",
         f"Usage: python tools/check_pdf.py {note_md(MAP['02-ai-vs-ml-vs-dl'])} pdf/{MAP['02-ai-vs-ml-vs-dl']}.pdf"),
    ])
    new251 = MAP[NUM[251]]
    patch("tools/test_check_pdf.py", [
        ("](../251-standard-normal/note.md)", f"](../../../{note_md(new251)})"),
    ])
    patch("tools/gpt2_small.py", [("the 1077 Notebook", f"the {label(NUM[1077])} Notebook")])


def chapter_indexes():
    """ML/06-regression/06-regression.md: the Chapter's Notes in reading order, one line each."""
    chapters = defaultdict(list)
    for old, new in MAP.items():
        if old != COURSE_OLD:
            chapters[tuple(new.split("/")[:2])].append((old, new))
    for (subject, chapter), notes in sorted(chapters.items()):
        lines = []
        for old, new in sorted(notes, key=lambda on: on[1]):
            m = re.search(r'^title:\s*"(.*)"', read(f"{old}/note.md"), re.M)
            lines.append(f"- [{name_of(new)[:6]} {m.group(1) if m else name_of(new)}]({name_of(new)}/{name_of(new)}.md)")
        title = chapter[3:].replace("-", " ").capitalize()
        text = f"# {title}\n\n{subject} chapter {chapter[:2]}. Notes in reading order:\n\n" + "\n".join(lines) + "\n"
        stage(f"{subject}/{chapter}/{chapter}.md", text, None)
        COUNT["chapter index Notes"] += 1


# ---------------------------------------------------------------- 8. README and .gitignore

def update_readme_gitignore():
    text = before = read("README.md")
    tree = """```
campusx/
  00-course-map/00-course-map.md                       the Course map (also its images/)
  MA/<NN-chapter>/MA-001-<slug>/MA-001-<slug>.md       Mathematical foundations
  ML/<NN-chapter>/ML-001-<slug>/ML-001-<slug>.md       Machine learning: each Note folder holds its .md, images/,
  DL/<NN-chapter>/DL-001-<slug>/DL-001-<slug>.md       Deep learning      data/ and <Note>.ipynb when it has code
  ML/06-regression/06-regression.md                    chapter index: the Chapter's Notes in reading order
  pdf/<same layout>/<Note>.pdf                         generated PDFs
  transcripts/                                         subtitles for every Video
  glossary.md
```"""
    text, n = re.subn(r"```\ncampusx/\n.*?```", lambda _: tree, text, count=1, flags=re.S)
    if n != 1:
        raise SystemExit("README.md: folder layout block not found")
    text = rewrite_tokens(text)
    text = rewrite_mentions(text, "README.md")
    stage("README.md", text, before)
    text = before = read(".gitignore")
    stage(".gitignore", rewrite_tokens(text), before)


# ---------------------------------------------------------------- 2. the move

def git(*args):
    subprocess.run(["git", *args], cwd=ROOT, check=True)


def git_mv(old, new):
    (ROOT / new).parent.mkdir(parents=True, exist_ok=True)
    if subprocess.run(["git", "ls-files", "--error-unmatch", old], cwd=ROOT, capture_output=True).returncode == 0:
        git("mv", old, new)
    else:                                                     # untracked (git-ignored) file: a plain rename
        (ROOT / old).rename(ROOT / new)


def move_folders():
    for old, new in MAP.items():                              # per-Note .logs: files to the root .logs, folder gone
        logs = ROOT / old / ".logs"
        if logs.is_dir():
            files = [f for f in logs.rglob("*") if f.is_file()]
            for f in files:
                print(f"  .logs: {old}/.logs/{f.name} -> .logs/{name_of(new)}-{f.name}")
                COUNT[".logs files moved to root .logs"] += 1
                if not DRY:
                    (ROOT / ".logs").mkdir(exist_ok=True)
                    shutil.move(str(f), ROOT / ".logs" / f"{name_of(new)}-{f.name}")
            COUNT[".logs folders deleted"] += 1
            if not DRY:
                shutil.rmtree(logs)
    for old, new in MAP.items():
        moves = [(old, new), (f"{new}/note.md", note_md(new)), (f"pdf/{old}.pdf", f"pdf/{new}.pdf")]
        if (ROOT / old / "notebook.ipynb").is_file():
            moves.insert(2, (f"{new}/notebook.ipynb", f"{new}/{name_of(new)}.ipynb"))
            COUNT["notebooks renamed"] += 1
        COUNT["folders moved"] += 1
        COUNT["pdfs moved"] += 1
        print(f"  git mv {old} -> {new}  (+ {name_of(new)}.md" + (", .ipynb" if len(moves) == 4 else "") + ", pdf)")
        if not DRY:
            for a, b in moves:
                git_mv(a, b)


def write_pending():
    for path, text in PENDING.items():
        p = ROOT / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    git("add", "--", *PENDING)


# ---------------------------------------------------------------- 7. verification

LINK = re.compile(r"\]\(([^)\s]+)\)")


def verify():
    problems = []
    # every .md the migration wrote (Notes, chapter indexes, glossary, README, CONTEXT, docs/*.md): staged text
    # in a dry run, the file on disk after the move otherwise
    md_files = {p: (t if DRY else (ROOT / p).read_text()) for p, t in PENDING.items() if p.endswith(".md")}
    for path, text in md_files.items():
        for m in LINK.finditer(text):
            target = m.group(1).split("#")[0]
            if not re.match(r"[\w./-]+$", target) or target.startswith(("http://", "https://", "mailto:")):
                continue                                      # not a path: a URL, or code such as (x=1)
            full = posixpath.normpath(posixpath.join(posixpath.dirname(path), target))
            if not exists(full):
                problems.append(f"{path}: broken link {m.group(1)}")
        if re.search(r"\]\(\.\./(?!00-course-map)\d+-", text):
            problems.append(f"{path}: old-style ](../N- link left")
    for path, text in PENDING.items():
        for m in re.finditer(r"\bNote \d{1,4}(?![-x]|\.\d|\d)", text):
            problems.append(f"{path}: 'Note N' left: {text[m.start():m.start() + 12]!r}")
    print(f"verify: {len(md_files)} .md files, {sum(len(LINK.findall(t)) for t in md_files.values())} links checked, "
          f"{len(problems)} problems")
    for p in problems[:40]:
        print("  " + p)
    if not DRY:
        for old in ("440-role-of-maths-in-ml", "02-ai-vs-ml-vs-dl", "1004-perceptron"):
            r = subprocess.run(["tools/build.sh", MAP[old]], cwd=ROOT)
            print(f"build {MAP[old]}: {'ok' if r.returncode == 0 else 'FAILED'}")
            if r.returncode:
                problems.append(f"build failed: {MAP[old]}")
    return problems


# ---------------------------------------------------------------- main

def main():
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    if len(args) != 1:
        raise SystemExit(__doc__)
    read_map(args[0])
    rewrite_notes()
    rewrite_glossary()
    rewrite_docs()
    rewrite_images()
    rewrite_notebooks()
    update_tools()
    chapter_indexes()
    update_readme_gitignore()
    print(("DRY RUN: would " if DRY else "") + "move:")
    move_folders()
    if not DRY:
        write_pending()
    problems = verify()
    print("\nsummary" + (" (dry run, nothing changed)" if DRY else ""))
    for k, v in sorted(COUNT.items()):
        print(f"  {k}: {v}")
    print(f"  tool files patched: {len(PATCHED)}: {', '.join(PATCHED)}")
    print(f"  unresolved (left as they were): {len(UNRESOLVED)}")
    for u in UNRESOLVED[:40]:
        print("    " + u)
    print(f"  loose files that stay inside their Note folder: {len(LOOSE)}")
    for f in LOOSE:
        print("    " + f)
    if problems:
        raise SystemExit(f"{len(problems)} verification problems")


if __name__ == "__main__":
    main()
