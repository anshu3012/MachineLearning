"""Make the maths in Notes render on GitHub as well as in the PDF and Obsidian.

GitHub applies Markdown backslash escapes before rendering maths, so \\, \\; \\! \\{ \\} \\| and the row break \\\\
lose their backslash there. Inside $...$ and $$...$$ (never in code), this rewrites them to the spelled-out
commands that LaTeX, GitHub (MathJax) and Obsidian (MathJax) all accept. \\% \\_ \\& \\# have no such command:
they are reported for a manual rewrite (move them out of the maths or use words).

Usage: python tools/github_math.py <note.md>...        rewrites in place, prints what is left for a person
       python tools/github_math.py --check <note.md>... only reports; exit 1 if anything needs fixing"""
import re
import sys

SWAP = [(r"\\[^]]*]", r"\cr "),                    # row break with extra space: the space is dropped
        ("\\\\", r"\cr "), (r"\,", r"\thinspace "), (r"\;", r"\thickspace "), (r"\:", r"\medspace "),
        (r"\!", r"\negthinspace "), (r"\{", r"\lbrace "), (r"\}", r"\rbrace "), (r"\|", r"\Vert ")]
MANUAL = re.compile(r"\\[%_&#$]")
CODE = re.compile(r"```.*?```|`[^`\n]*`", re.S)
MATH = re.compile(r"(?<!\\)\$\$.*?\$\$|(?<![\\$])\$(?!\$)[^$\n]+?(?<!\\)\$", re.S)


def fix_math(m):
    s = m.group()
    s = re.sub(r"\\\\\[[^\]]*\]", r"\\cr ", s)
    for old, new in SWAP[1:]:
        s = s.replace(old, new)
    # GitHub reads "_" after "}" as the start of italics: put a subscript before a superscript, and drop the
    # braces of a one-letter argument (\hat{y}_i -> \hat y_i); both print the same
    s = re.sub(r"\^(\{[^{}]*\}|[^{\\])_(\{[^{}]*\}|\\[A-Za-z]+|[^{\\])", r"_\2^\1", s)
    s = re.sub(r"(\\[A-Za-z]+)\{([A-Za-z0-9])\}(?=_)", r"\1 \2", s)
    s = re.sub(r"(?<!\\)\*", r"\\ast ", s).replace(r"\ast }", r"\ast}")       # GitHub reads * as italics
    # the space after a spelled-out command is needed only before a letter; GitHub ignores "$x $" as maths
    return re.sub(r"(\\(?:thinspace|thickspace|medspace|negthinspace|lbrace|rbrace|Vert|cr|ast)) +(?![A-Za-z])", r"\1", s)


def blank_around_display(text):
    """GitHub mixes a $$ line into the paragraph above it unless an empty line separates them."""
    lines, out = text.split("\n"), []
    plain = lambda l: l.strip() and not l.startswith((" ", "\t", "$$", "|", "#", ">", "-", "*", "!", "<")) \
        and not re.match(r"\d+\. ", l)
    item = None                                       # indent of the list item we are inside, if any
    for i, line in enumerate(lines):
        m = re.match(r"( *)(\d+\.|[-*]) ", line)
        if m:
            item = " " * len(m.group())
        elif not line.strip() and i + 1 < len(lines) and not lines[i + 1].startswith((" ", "$$")):
            item = None
        if line.startswith("$$") and out and item is not None and out[-1].strip() and not out[-1].startswith("$$"):
            out.append("")                            # a formula under a list item: indented, its own paragraph
        if line.startswith("$$") and item is not None:
            if line.rstrip().endswith("$$") and len(line.strip()) > 4:
                # GitHub renders a one-line $$...$$ inside a list only when $$ stands on its own lines
                line = f"{item}$$\n{item}{line.strip()[2:-2].strip()}\n{item}$$"
            else:
                line = item + line
            if i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].startswith("$$"):
                out.append(line)
                out.append("")
                continue
        if line.startswith("$$") and out and plain(out[-1]):
            out.append("")
        out.append(line)
        if line.rstrip().endswith("$$") and line.startswith("$$") and i + 1 < len(lines) and plain(lines[i + 1]):
            out.append("")
    return "\n".join(out)


GLUED = re.compile(r"(?<=[A-Za-z0-9])-(?=\$[^$\s])")       # rank-$k$ -> rank $k$
GLUED_NUM = re.compile(r"(?<![\w$])(\d+(?:\.\d+)?)/\$(?=[^$\s])")  # 2/$x$ -> $2/x$


def unglue(text):
    return GLUED_NUM.sub(r"$\1/", GLUED.sub(" ", text))


def fix(text):
    """Rewrite maths outside code; return the new text and the maths that still needs a person."""
    out, left, pos = [], [], 0
    for c in CODE.finditer(text):
        chunk = blank_around_display(MATH.sub(fix_math, unglue(text[pos:c.start()])))
        out += [chunk, c.group()]
        pos = c.end()
    out.append(blank_around_display(MATH.sub(fix_math, unglue(text[pos:]))))
    new = "".join(out)
    for c in CODE.split(new):
        left += [m.group() for m in MATH.finditer(c) if MANUAL.search(m.group())]
    return new, left


def risks(text):
    """Maths GitHub fails to render, by rules found through its API (2026-10-03)."""
    found = []
    for chunk in CODE.split(text):
        for m in MATH.finditer(chunk):
            s, inline = m.group(), not m.group().startswith("$$")
            before = chunk[m.start() - 1] if m.start() else "\n"
            after = chunk[m.end()] if m.end() < len(chunk) else "\n"
            if inline and not (before.isspace() or before in "([{>|*_"):
                found.append(("inline maths glued to the character before it", chunk[m.start() - 8:m.end()]))
            if inline and after.isalnum():
                found.append(("inline maths glued to the letter after it", chunk[m.start():m.end() + 8]))
            if re.search(r"[})\]]_", s):
                found.append(('"_" right after a brace (GitHub may read italics)', s[:70]))
    return found


if __name__ == "__main__":
    check = sys.argv[1] == "--check"
    bad = False
    for path in sys.argv[2 if check else 1:]:
        text = open(path).read()
        new, left = fix(text)
        if check and new != text:
            print(f"{path}: maths that GitHub breaks (run tools/github_math.py on it)")
            bad = True
        elif not check and new != text:
            open(path, "w").write(new)
        for why, m in risks(new):
            print(f"{path}: {why}: {m}")
            bad = True
        for m in left:
            print(f"{path}: rewrite by hand (\\% \\_ \\& \\# break on GitHub): {m[:90]}")
            bad = True
    sys.exit(1 if check and bad else 0)
