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
    return s


def fix(text):
    """Rewrite maths outside code; return the new text and the maths that still needs a person."""
    out, left, pos = [], [], 0
    for c in CODE.finditer(text):
        chunk = MATH.sub(fix_math, text[pos:c.start()])
        out += [chunk, c.group()]
        pos = c.end()
    out.append(MATH.sub(fix_math, text[pos:]))
    new = "".join(out)
    for c in CODE.split(new):
        left += [m.group() for m in MATH.finditer(c) if MANUAL.search(m.group())]
    return new, left


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
        for m in left:
            print(f"{path}: rewrite by hand (\\% \\_ \\& \\# break on GitHub): {m[:90]}")
            bad = True
    sys.exit(1 if check and bad else 0)
