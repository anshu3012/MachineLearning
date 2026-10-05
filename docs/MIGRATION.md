# Migration: from a flat layout to Subjects and Chapters

Agreed with the user on 2026-10-03. Why: [ADR 0001](adr/0001-subject-prefixes-and-gap-free-numbers.md). Terms: `CONTEXT.md` (Subject, Chapter, Note number).

**When:** now (decided 2026-10-04): every MA/ML/DL Note is written and no agent is editing. RL becomes a new Subject (RO) later and shifts no MA/ML/DL numbers.

## Target layout

```
00-course-map/00-course-map.md
MA/<NN-chapter>/MA-001-<slug>/MA-001-<slug>.md     Mathematical foundations
ML/<NN-chapter>/ML-001-<slug>/ML-001-<slug>.md     Machine learning
DL/<NN-chapter>/DL-001-<slug>/DL-001-<slug>.md     Deep learning
RO/…                                               Robotics (later)
pdf/<same layout>/<Note>.pdf
tools/ docs/ transcripts/ reference/ course_map/ glossary.md CONTEXT.md   (stay at the top level)
```

## Rules

1. **Note number:** the Subject prefix plus three digits, in reading order, with no gaps. Numbers run on across Chapters. A Note's number never depends on its Chapter.
2. **File name = folder name**, e.g. `DL-038-adam/DL-038-adam.md`, and the notebook is `DL-038-adam.ipynb`. Obsidian then shows real names, and `[[DL-038-adam]]` links work.
3. **Chapters** match the mind maps (`course_map/mindmaps/`). Every Subject is split into Chapters.
4. **Moves:**
   - Today's ML Notes 82–86 (conditional probability, independent and mutually exclusive events, Bayes' theorem) move to MA's probability Chapter.
   - The ML intro Notes (1–14) become `ML/01-foundations/`.
   - The Course map becomes `00-course-map/`.
5. **Front matter:** `title`, `tags`, `video:` (the source video, so a script can find its transcript; transcripts stay keyed by video) and generated `prerequisites:` links. No `old_number` field (user, 2026-10-04).
6. **Loose files** (`app.py`, helper scripts, `models/`) stay inside their Note folder; empty per-Note `.logs/` folders are deleted and the three with files move to the root `.logs/`.
7. **Chapter index Notes:** each chapter folder gets a generated `<NN-chapter>.md` listing its Notes in reading order, one line each.
8. **No migration map is committed** and the README gets no pointer (user, 2026-10-04); the old → new table lives only in the migration commit's diff and in `git log --follow`.
9. **Renumbering later:** adding a Note shifts the numbers after it in its Subject. Rerun the migration script only at milestones, such as the end of a book.

## Chapters (agreed 2026-10-04; statistics first because the ML Notes need it first; the executed map is `tools/migrate.py` and the layout below)

| Subject | Chapter | Today's Notes |
|---|---|---|
| MA | 00-why-maths | 440, 580 |
| MA | 01-descriptive-stats | 210–231 |
| MA | 02-probability | 330–341, then ML 82–86 |
| MA | 03-distributions | 240–262, 270, 560 |
| MA | 04-inference | 271–302, 570–572 |
| MA | 05-linear-algebra | 350–363, 490–530, 610–613 |
| MA | 06-calculus | 600–603 |
| MA | 07-optimisation | 590, 620–622 |
| MA | 08-likelihood | 630–641 |
| ML | 01-foundations | 1–14 |
| ML | 02-getting-data | 15–22 |
| ML | 03-feature-engineering | 23–34 |
| ML | 04-missing-data-and-outliers | 35–44 |
| ML | 05-dimensionality | 45–49 |
| ML | 06-regression | 50–69 |
| ML | 07-classification | 70–81, 87–96 |
| ML | 08-trees-and-ensembles | 97–127 |
| ML | 09-clustering-and-more | 128–134 |
| DL | 01-basics | 1001–1019 |
| DL | 02-training | 1020–1031 |
| DL | 03-optimizers | 1032–1039 |
| DL | 04-cnn | 1040–1054 |
| DL | 05-rnn | 1055–1066 |
| DL | 06-transformers | 1067–1090: order 1067–1071, 1086 (meaning as direction), 1072–1085, then 1087–1090 (GPT, sampling, MLP facts, superposition) |

The reading order inside each Chapter is today's number order unless a Note's prerequisites say otherwise. The script checks that no Note comes before a Note it needs.

## Script steps (`tools/migrate.py`, one commit)

1. Build the old → new map from the table above. Write it to `docs/migration_map.csv`, which keeps old numbers findable.
2. Move the folders with `git mv`, and rename each `note.md` to `<folder>.md`.
3. Rewrite every link between Notes (about 4,900) and every `../../tools` path, which now depends on the folder depth.
4. Rewrite "Note N" mentions in the text, plus `concepts.yaml` (`notes:` and `videos:`), the glossary, `.logs/` names and the build tools (`build.sh`, `remote_run.sh`, `check_pdf.py`, `build_map.py`, `app.py`, `map_3d.py`).
5. **Front matter:** tags (as now), plus `prerequisites: ["[[MA-012-dot-product]]", …]` generated from the `needs` links in `concepts.yaml`.
6. Rebuild every PDF (all 292, about 2 hours with 4 in parallel) and the maps. Check that every link resolves, every PDF builds, and no Note precedes a prerequisite.
7. Commit as one change.

## Watch for during the migration
- **Figures that read other Notes' files:**
  - 210 `module_gallery`, 350 `module_thumbs` and 1001 `family_thumbs` read other Notes' PNGs.
  - 60's `gd_race.py` writes into 58 and 59.
  - 108 and 220 hold copies of other Notes' data.

  Rewrite these paths too, then rebuild with `FORCE=1`.
- **Stray `.logs/` folders inside Note folders** (git-ignored; about 80 of them from remote runs): move their contents to the root `.logs/` before moving the folders.
