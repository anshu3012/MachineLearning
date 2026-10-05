# Task: glossary meanings in plain words first, standard terms in brackets after (NOTE-RULES §10, §23)

User's choice (2026-10-05), style **B**, for PCA:
> A way to replace many columns with a few new ones that keep most of the spread in the data (feature extraction for dimensionality reduction). Each new column, a principal component, follows one direction of greatest variance. Used to cut the number of features and to plot data with many columns.

The old meaning opened with jargon: "an unsupervised feature extraction technique for dimensionality reduction that builds new columns along the directions of greatest variance".

For each row in your G-ID list (read `glossary.md`):
1. Does the meaning open with, or lean on, words a beginner meeting this term would not know yet (other technical terms, "technique for…", "estimator", "variance", "hyperparameter", symbols)? If it already reads in plain words (or the jargon is the term's own simple name), leave it.
2. If not, rewrite in style B: plain words first saying what it is and what it does; the standard terms kept, in brackets or a short second clause, after the plain words; then what it is used for. Keep every fact and number; add no claim (the old meaning and the Note it links to are the source; check the Note if unsure). Keep `$...$` valid, no `|`, no newline, two or three short sentences at most.
3. Code names (`fit_transform`, `GridSearchCV`) and symbols: say in plain words what the thing does; the name stays as the term.

Output: JSON mapping only rewritten G-IDs to `{"meaning": "..."}`, validated with `python3 -m json.tool`. Edit no other file; no git. Report: rows checked, rows rewritten.
