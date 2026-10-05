# Task: give each Preview its one plain sentence (CONTEXT.md "Preview", NOTE-RULES §19)

Each line of your list: `<Note> | <Concept> | home: <Home Note>#<section>`. The Note uses (or the data says it needs) an idea the course teaches only later, in the Home section.

For each line:
1. Read the Note and find where it relies on the idea (the term, its symbol, or what it does).
2. If it does rely on it: at its first use, add one plain sentence (or clause) saying what the idea is, enough to follow this Note, with a link to the Home section whose link text is the idea (§17), e.g. "…updated by **backpropagation**, a way to work out how much each weight should change ([taught in full later](../../01-basics/DL-015-…md#…))". Use the idea's name in the sentence. Plain words first (§10, §11). No new facts beyond what the Home section says.
3. If the Note does not actually use the idea, change nothing and list it in your report as "not used" (the link data is wrong).

Keep headings, figures, code and numbers unchanged. Checks per edited Note: `python3 tools/github_math.py --check`, `python3 tools/section_links.py --check`, `python3 tools/find_inline_calc.py` (0). Do not touch git, glossary.md, course_map/, tools/, docs/, or Notes not on your list. Report: per line, "added" or "not used".
