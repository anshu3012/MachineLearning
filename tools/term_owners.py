"""Where each glossary term is explained (NOTE-RULES §17, §20 addendum).

  python tools/term_owners.py            write docs/term-owners.tsv: G-id, term, owner Note, section anchor, link
  python tools/term_owners.py G-1874     print one row
The owner Note comes from glossary.md's last column; the section is the heading above the first line of that Note
that cites the ID "(G-N)". A row with an empty anchor means the owner Note never cites its own ID: fix the Note.
A Note that uses a term it does not own links its first use to the link column, with a one-line recap.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from section_links import slug  # noqa: E402

ROW = re.compile(r'^\| <span id="(G-\d+)">G-\d+</span> \| (.*?) \| .*\| \[Note [^\]]*\]\(([^)]+\.md)\) \|\s*$')


def owner_section(note, gid):
    """The section where the Note defines the term: the line with the term in bold right before "(G-N" wins over
    a plain citation of the ID (a passing mention); the Key terms table at the end never counts."""
    cite = re.compile(rf"\({gid}[;,)]|\({gid}\b")
    found = {}
    heading = ""
    for line in open(note, encoding="utf-8"):
        m = re.match(r"^#{2,6}\s+(.*?)\s*$", line)
        if m:
            heading = m.group(1)
            if re.match(r"[\d.]+ (key terms|sources)", heading.lower()):
                break
        elif cite.search(line) and heading and "$" not in heading:
            kind = "bold" if re.search(rf"\*\*[^*]+\*\*\s*\({gid}\b", line) else "plain"
            found.setdefault(kind, slug(heading))
    return found.get("bold") or found.get("plain", "")


def rows():
    for line in open("glossary.md", encoding="utf-8"):
        m = ROW.match(line)
        if m:
            gid, term, note = m.groups()
            anchor = owner_section(note, gid) if os.path.exists(note) else ""
            yield gid, term, note, anchor, f"{note}#{anchor}" if anchor else note


if __name__ == "__main__":
    out = list(rows())
    assert len(out) > 2000, len(out)                      # self-check: the glossary parsed
    if sys.argv[1:]:
        for r in out:
            if r[0] in sys.argv[1:]:
                print("\t".join(r))
    else:
        with open("docs/term-owners.tsv", "w", encoding="utf-8") as f:
            f.write("id\tterm\towner\tanchor\tlink\n")
            f.writelines("\t".join(r) + "\n" for r in out)
        missing = sum(1 for r in out if not r[3])
        print(f"{len(out)} terms, {missing} with no section found (owner Note does not cite its own ID)")
