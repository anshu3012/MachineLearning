# Course structure: model and rollout (agreed 2026-10-05)

Terms are defined in `CONTEXT.md`; the decision is `docs/adr/0002-recorded-homes-and-generated-course-order.md`.

## Model
- **Concept** (`course_map/concepts.yaml`): `id`, `name`, `step`, `home: ML-023#<anchor>`, `videos: [every Note that teaches or uses it]`. Exactly one Home.
- **Glossary term** (`glossary.md`): ID, term, meaning, **Home** (Note#section), **Concept** id. Every term has one Concept (no natural one: the main Concept of its Home Note).
- **Link**: unchanged (needs, is a kind of, fixes, compared with, used in).
- **Builds on** (= `prerequisites:` front matter): direct only; the Homes of the Concepts this Note's Concepts need, when earlier in the Course order. *needs* and *fixes* are requirements (the fix needs the problem). *is a kind of* and *used in* only say which idea comes first: the one taught earlier is the building block (a general idea taught after a special case, or a tool taught after the method, leads on from it). A Note that is Home to no Concept (a practice Note) builds on the Homes of the Concepts it uses.
- **Preview**: a required Home (*needs*, *fixes*) that is later in the Course order. Listed as "Used here, taught in full later"; the Note must name, link or cite (a glossary term of) the idea where used.
- **Leads to**: the reverse of Builds on.
- **Compare with**: Homes of Concepts linked by *compared with*.
- **Pipeline step and tags**: from the Concepts whose Home is the Note, not mentions.
- **Course order**: the 30 Stages in `course_map/course_stages.json`, chosen by two independent reviews (2026-10-07): ML and DL in Note order; each maths topic sits just before the first Note that needs it, whole (not one Note at a time). The structure check fails on any Builds on that comes later. A *used in* / *is a kind of* link only gives reading order, so it must not pull maths in front of a Note whose text never uses it (5 such links were removed).
- **Key terms table**: generated from the glossary: terms homed in this Note, then recap rows (terms it cites, homed elsewhere) linking to their Home.
- **Sidebar**: "Course order" (the Stages, open by default; inside the ☰ menu on a phone) above the MA, ML, DL folders. Data: `course_map/course_order.json`, written by build_map.

## Rollout (one commit per stage, pushed when checked)
1. Fields: add `home`/`uses` to concepts.yaml and Home/Concept to the glossary; agents propose, a script rejects Homes whose section is missing, does not name the term, or only points elsewhere.
2. Generators read the recorded Homes: Where this fits, Course map (with Course order and Stages), glossary links and site boxes, Key terms tables, tags, prerequisites, chapter pages, sidebar order.
3. `tools/check_structure.py` on every build (and in the site workflow): forward Builds on, missing Home, Leads to ≠ reverse, prerequisites ≠ box, term Home disagreeing with its records, Preview without its sentence, mind-map box numbers ≠ Homes.
4. Agents write the missing Preview sentences.
