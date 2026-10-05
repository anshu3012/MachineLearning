# Task: give every glossary term its Concept (CONTEXT.md "Glossary term")

Inputs: your term list (JSON: `g`, `term`, `meaning`, `home` = the term's Home section) and `/home/anshu/.claude/jobs/8c1c0992/tmp/concepts_list.json` (335 Concepts: `id`, `name`, `home`).

For each term pick the **one** Concept it belongs to: the idea it is part of or a tool/setting/symbol of (e.g. "learning rate" → gradient descent; `n_init` → k-means; "dendrites" → perceptron or neural network, whichever its Home teaches). A term that is itself a Concept belongs to that Concept. If no Concept fits naturally, use the main Concept of the term's Home Note: the Concept whose `home` is in that Note (if several, the one whose section is closest to the term's Home section; read the Note if unsure).

Output JSON `{ "G-123": "concept_id", ... }` for every term in your list; every value must be an `id` from concepts_list.json. Validate with `python3 -m json.tool`. Edit no other file; no git. Report: count, and how many used the fallback rule.
