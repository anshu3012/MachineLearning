# Task: record each Concept's Home (docs/STRUCTURE.md, CONTEXT.md "Home")

Input: a JSON list of Concepts, each with `id`, `name` and `notes` (every Note that currently lists it; mentions and teaching are mixed).

For each Concept, find its **Home**: the one section of one Note that teaches it, meaning it explains what it is and how it works or why it is used, as its own topic (a heading named for it, or a section built around it). Not a passing mention, a preview in an overview Note, a recap, a code line, or a Sources/Key terms entry. Usually one of `notes`; if the real teaching section is in a Note not listed, use it (grep the Notes for the name). If two Notes teach it properly, prefer the one earlier in the course (MA before ML before DL, then Note number), unless the earlier one is only a short first look and the later one is the dedicated Note: then the dedicated Note.

Anchor = `slug(heading)` from `tools/section_links.py` (check it exists in the Note).

Output JSON: `{ "<id>": {"home": "<Note path from repo root>#<anchor>", "quote": "<a line from that section that shows it teaches the Concept, max 150 chars>"} }` for every Concept in your list. Validate with `python3 -m json.tool`. Edit no other file; no git. Report: count, and any Concept with no teaching section anywhere (list them).
