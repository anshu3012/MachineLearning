"""Make every glossary code in the site copy of the Notes ("(G-2040)") a tap target that opens its definition.

Each code becomes <button class="gloss">G-2040</button>; after the closing ")" of its bracket comes a hidden
<span class="gloss-def"> holding the glossary's term and definition (plain Markdown, so maths still renders)
and a link to the Note that teaches it ("Explained in this Note" inside that Note). site/GlossaryTerms.tsx
opens and closes the box. Headings, code, maths and HTML are left alone. Runs on the Quartz content copy only;
the repo's Notes are not touched.
Usage: python3 site/glossary_terms.py <repo> <quartz>/content
       python3 site/glossary_terms.py --fix-glossary <repo>   (point glossary.md links at the teaching section)
"""
import os
import re
import sys

ROW = re.compile(r'^\| <span id="(G-\d+)">G-\d+</span> \| (.*?) \| (.*?) \| (.*?) \|\s*$')
CODE = re.compile(r"\bG-\d+\b")
PROTECT = re.compile(r"(`[^`]*`|\$[^$]+\$|<[^>]+>)")  # inline code, inline maths, HTML tags
NOTE_LINK = re.compile(r"\]\(([^)]*?)([A-Z]{2}-\d{3}-[^/)#]+)\.md(?:#([^)]*))?\)")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from section_links import slug  # noqa: E402  same anchors as the site


HEAD = re.compile(r"^#{2,6}\s+(.*?)\s*$", re.M)
# A Note that only mentions a term points to the Note that teaches it, right after the code:
# "(G-1469), taught in [what PCA is](...ML-046-...md#1-what-pca-is)", "(G-996; see [the five steps](...))".
POINTER = re.compile(r"^[^*\n]{0,40}?\b(?:see|taught in|covered(?: in detail)? in|explained in)\s+(?:the\s+)?"
                     r"\[[^\]]*\]\(([^)#]*?[A-Z]{2}-\d{3}-[^/)#]+\.md)#([^)]+)\)")


def named(term, heading):
    """True when a section anchor names the term (by the term's first word of 4+ letters)."""
    words = re.findall(r"[a-z]{4,}", re.sub(r"\(.*?\)|\$.*?\$|`", "", term.lower()))
    return bool(words) and words[0] in (heading or "")


def owner(path, anchor, code, term="", seen=()):
    """The Note and section that teach `code`. Starts at the glossary's link; when that Note only mentions the
    term and points elsewhere (POINTER), follows the pointer. Without a section, uses the first section citing it."""
    text = open(path, encoding="utf-8").read()
    heads = {slug(h) for h in HEAD.findall("\n".join(l for l in text.split("\n") if l.startswith("#")))}
    cur, first = None, None
    for line in text.split("\n"):
        h = HEAD.match(line)
        if h:
            cur = slug(h.group(1))
            continue
        m = re.search(rf"\b{code}\b", line)
        if not m or line.startswith("|"):
            continue
        after = line[m.end():]
        nxt = CODE.search(after)
        ptr = POINTER.search(after[: nxt.start()] if nxt else after)
        # a section named for the term teaches it, unless the pointer goes to a section named for it too
        if ptr and path not in seen and (not named(term, cur) or named(term, ptr.group(2))):
            target = os.path.normpath(os.path.join(os.path.dirname(path), ptr.group(1)))
            if os.path.exists(target) and target != path:
                return owner(target, ptr.group(2), code, term, seen + (path,))
        first = first or cur
        if anchor in heads:
            break
    return path, anchor if anchor in heads else first


def load(repo):
    entries = {}
    for line in open(os.path.join(repo, "glossary.md"), encoding="utf-8"):
        m = ROW.match(line)
        if not m:
            continue
        code, term, definition, where = m.groups()
        note = NOTE_LINK.search(where)
        if note:
            path, anchor = owner(os.path.join(repo, note.group(1), note.group(2) + ".md"), note.group(3), code, term)
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


def fix_glossary(repo):
    """Rewrite glossary.md's links to the Note and section owner() finds, so the glossary page agrees with the boxes."""
    entries, p = load(repo), os.path.join(repo, "glossary.md")
    out, n = [], 0
    for line in open(p, encoding="utf-8").read().split("\n"):
        m = ROW.match(line)
        if m and entries[m.group(1)][2][4]:
            _, _, (name, _, anchor, _, rel) = entries[m.group(1)]
            link = f"[Note {name[:6]}]({rel}{'#' + anchor if anchor else ''})"
            new = line[: line.rindex("| [")] + f"| {link} |"
            n += new != line
            line = new
        out.append(line)
    open(p, "w", encoding="utf-8").write("\n".join(out))
    print(f"glossary links changed: {n}")


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
    if sys.argv[1] == "--fix-glossary":
        fix_glossary(sys.argv[2])
    else:
        main(sys.argv[1], sys.argv[2])
