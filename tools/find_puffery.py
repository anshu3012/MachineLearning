"""List puffery and filler in Notes (NOTE-RULES §18). Usage: python tools/find_puffery.py [Note.md ...]
Prints file:line: [phrase] sentence. A hit is a prompt to look, not proof: cut it only if the sentence says less
without it being missed. Code blocks, maths, tables and Sources are skipped."""
import glob
import re
import sys

PATTERNS = [  # puffery
    r"\bpowerful\b", r"\brobust\b", r"\belegant(ly)?\b", r"\bbeautiful(ly)?\b", r"\bremarkabl[ey]\b",
    r"\bcrucial\b", r"\bvital\b", r"\bkey (role|insight|idea)\b", r"\bpivotal\b", r"\btestament\b",
    r"\bmagic(al)?\b", r"\bseamless(ly)?\b", r"\bcornerstone\b", r"\bgame[- ]changer\b", r"\bat its (core|heart)\b",
    r"\bthe heart of\b", r"\bbackbone of\b", r"\bunlock(s|ing)?\b", r"\bdelve\b", r"\bharness(es|ing)?\b",
    r"\blandscape\b", r"\brealm\b", r"\bjourney\b", r"\bstunning\b", r"\bincredibl[ey]\b",
    # filler
    r"\bit is (important|worth|crucial) to (note|remember|mention)\b", r"\bit('s| is) worth noting\b",
    r"\bnote that\b", r"\bin other words\b", r"\bessentially\b", r"\bbasically\b", r"\bsimply put\b",
    r"\bin fact\b", r"\bactually\b", r"\bindeed\b", r"\bof course\b", r"\bclearly\b", r"\bobviously\b",
    r"\bit turns out( that)?\b", r"\bas we (can )?see\b", r"\blet us\b", r"\blet's\b", r"\bin summary\b",
    r", (highlighting|underscoring|ensuring|showcasing|reflecting|emphasi[sz]ing)\b",
    # vague sources
    r"\b(experts|researchers|studies|many people) (say|believe|suggest|show)\b", r"\bit is (widely|often|commonly) (said|believed|known)\b",
]
RX = re.compile("|".join(PATTERNS), re.I)


def scan(path):
    out, code, sources = [], False, False
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        if line.startswith("```"):
            code = not code
        if re.match(r"^## \d+\. Sources", line):
            sources = True
        elif re.match(r"^## ", line):
            sources = False
        s = line.strip()
        if code or sources or not s or s.startswith(("$$", "|", "!", "<", "#")):
            continue
        prose = re.sub(r"\$[^$]*\$|`[^`]*`|\]\([^)]*\)", " ", s)
        for m in RX.finditer(prose):
            out.append((n, m.group(0), s[:110]))
    return out


if __name__ == "__main__":
    assert RX.search("This is a powerful idea") and RX.search("Note that x") and not RX.search("the Note shows")
    files = sys.argv[1:] or sorted(glob.glob("*/*/*-[0-9][0-9][0-9]-*/*.md"))
    total = 0
    for f in files:
        for n, phrase, s in scan(f):
            print(f"{f}:{n}: [{phrase}] {s}")
            total += 1
    print(f"{total} found")
