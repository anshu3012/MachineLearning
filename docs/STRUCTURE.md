# Course structure: model and rollout (agreed 2026-10-05)

Terms are defined in `CONTEXT.md`; the decision is `docs/adr/0002-recorded-homes-and-generated-course-order.md`.

## Model
- **Concept** (`course_map/concepts.yaml`): `id`, `name`, `step`, `home: ML-023#<anchor>`, `videos: [every Note that teaches or uses it]`. Exactly one Home.
- **Glossary term** (`glossary.md`): ID, term, meaning, **Home** (Note#section), **Concept** id. Every term has one Concept (no natural one: the main Concept of its Home Note).
- **Link**: unchanged (needs, is a kind of, fixes, compared with, used in).
- **Builds on** (= `prerequisites:` front matter): direct only; the Homes of the Concepts this Note's Concepts need (needs, is a kind of, the problem side of fixes, the tool side of used in), when that Home is earlier in the Course order.
- **Preview**: such a Home that is later in the Course order (same Subject). Listed as "Used here, taught in full later"; the Note must explain it in one plain sentence where used.
- **Leads to**: the reverse of Builds on.
- **Compare with**: Homes of Concepts linked by *compared with*.
- **Pipeline step and tags**: from the Concepts whose Home is the Note, not mentions.
- **Course order**: ML then DL in Note order; each maths Note, with the maths it builds on, just before the first Note that needs it; maths nobody needs follows the maths Note numbered before it. Shown on the Learning path as Stages (one per ML or DL Chapter, split above 20 Notes).
- **Key terms table**: generated from the glossary: terms homed in this Note, then recap rows (terms it cites, homed elsewhere) linking to their Home.
- **Sidebar**: MA, ML, DL.

## Rollout (one commit per stage, pushed when checked)
1. Fields: add `home`/`uses` to concepts.yaml and Home/Concept to the glossary; agents propose, a script rejects Homes whose section is missing, does not name the term, or only points elsewhere.
2. Generators read the recorded Homes: Where this fits, Course map (with Course order and Stages), glossary links and site boxes, Key terms tables, tags, prerequisites, chapter pages, sidebar order.
3. `tools/check_structure.py` on every build (and in the site workflow): forward Builds on, missing Home, Leads to ≠ reverse, prerequisites ≠ box, term Home disagreeing with its records, Preview without its sentence, mind-map box numbers ≠ Homes.
4. Agents write the missing Preview sentences.
