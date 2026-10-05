"""Make every glossary code in the site copy of the Notes ("(G-2040)") a tap target that opens its definition.

Each code becomes <button class="gloss">G-2040</button>; after the closing ")" of its bracket comes a hidden
<span class="gloss-def"> holding the glossary's term and definition (plain Markdown, so maths still renders)
and a link to the Note that teaches it ("Explained in this Note" inside that Note). site/GlossaryTerms.tsx
opens and closes the box. Headings, code, maths and HTML are left alone. Runs on the Quartz content copy only;
the repo's Notes are not touched.
Usage: python3 site/glossary_terms.py <repo> <quartz>/content
"""
import os
import re
import sys

ROW = re.compile(r'^\| <span id="(G-\d+)">G-\d+</span> \| (.*?) \| (.*?) \| (.*?) \|(?: [^|]* \|)?\s*$')  # ..., Home, Concept
CODE = re.compile(r"\bG-\d+\b")
PROTECT = re.compile(r"(`[^`]*`|\$[^$]+\$|<[^>]+>)")  # inline code, inline maths, HTML tags
NOTE_LINK = re.compile(r"\]\(([^)]*?)([A-Z]{2}-\d{3}-[^/)#]+)\.md(?:#([^)]*))?\)")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from section_links import slug  # noqa: E402  same anchors as the site


def load(repo):
    entries = {}
    for line in open(os.path.join(repo, "glossary.md"), encoding="utf-8"):
        m = ROW.match(line)
        if not m:
            continue
        code, term, definition, where = m.groups()
        note = NOTE_LINK.search(where)
        if note:
            path, anchor = os.path.join(repo, note.group(1), note.group(2) + ".md"), note.group(3)  # the recorded Home
            text = open(path, encoding="utf-8").read()
            title = re.search(r'^title: "?(.*?)"?\s*$', text[:2000], re.M)
            name = os.path.basename(path)[:-3]
            title = title.group(1) if title else name
            heads = {slug(h): h for h in re.findall(r"^#{2,6}\s+(.*?)\s*$", text, re.M)}
            target = (name, title, anchor, re.sub(r"[*`$]", "", heads[anchor]) if anchor else None,
                      os.path.relpath(path, repo))
        else:
            target = ("/", "Course map", None, None, None)
        entries[code] = (term, definition, target)
    return entries


def box(code, entries, page):
    term, definition, (note, title, anchor, section, _) = entries[code]
    if anchor:
        where = f"Explained in [§{section}](#{anchor})." if note == page else f"Explained in: [{title}, §{section}]({note}#{anchor})"
    else:
        where = "Explained in this Note." if note == page else f"Explained in: [{title}]({note})"
    return f'<span class="gloss-def" data-g="{code}" hidden>**{term}:** {definition} {where}</span>'


def fix_text(text, entries, page):
    """Buttons for the codes in plain text; each code's box goes after the ")" that closes its bracket."""
    out, pending, depth = [], [], 0
    pos = 0
    for m in re.finditer(r"\bG-\d+\b|[()]", text):
        out.append(text[pos:m.start()])
        tok = m.group(0)
        pos = m.end()
        if tok == "(":
            depth += 1
            out.append(tok)
        elif tok == ")":
            depth = max(depth - 1, 0)
            out.append(tok)
            if depth == 0 and pending:
                out.extend(box(c, entries, page) for c in pending)
                pending = []
        elif tok in entries:
            out.append(f'<button type="button" class="gloss" data-g="{tok}" aria-expanded="false">{tok}</button>')
            if depth:
                pending.append(tok)
            else:
                out.append(box(tok, entries, page))
        else:
            out.append(tok)
    out.append(text[pos:])
    out.extend(box(c, entries, page) for c in pending)  # an unclosed bracket: boxes at the end of the text
    return "".join(out)


def fix_line(line, entries, page):
    parts = PROTECT.split(line)
    # parts alternate: text, protected, text, ...; brackets may span a protected part, so join the text parts
    # with placeholders, fix them together, then put the protected parts back.
    marks = [f"\x00{i}\x00" for i in range(len(parts) // 2)]
    joined = "".join(p if i % 2 == 0 else marks[i // 2] for i, p in enumerate(parts))
    fixed = fix_text(joined, entries, page)
    for i, mark in enumerate(marks):
        fixed = fixed.replace(mark, parts[2 * i + 1], 1)
    return fixed


def fix_file(path, entries):
    page = os.path.basename(path)[:-3]
    lines, out = open(path, encoding="utf-8").read().split("\n"), []
    fence = math = front = False
    for n, line in enumerate(lines):
        bare = line.lstrip("> ").strip()
        if n == 0 and line == "---":
            front = True
        elif front:
            front = line != "---"
        elif bare.startswith("```"):
            fence = not fence
        elif bare == "$$":
            math = not math
        elif not (fence or math or line.startswith("#")) and CODE.search(line):
            line = fix_line(line, entries, page)
        out.append(line)
    open(path, "w", encoding="utf-8").write("\n".join(out))


def main(repo, content):
    entries = load(repo)
    n = 0
    for root, _, files in os.walk(content):
        for name in files:
            if name.endswith(".md") and name != "glossary.md":
                fix_file(os.path.join(root, name), entries)
                n += 1
    print(f"glossary_terms: {len(entries)} terms, {n} pages")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
