# Maths Notes: plan and numbering

Source playlists (see `transcripts/maths_playlist.txt`):
- "Maths for Machine Learning" (CampusX), sessions M01–M23.
- "Machine Learning Mathematics" (CampusX), M24–M25. M25 is the same video as ML Video 11, so Note 11 covers it.
- Videos from 3Blue1Brown or StatQuest in CampusX's other maths playlists, when they teach a concept the CampusX sessions do not.

## Numbering

A session is often 2 hours and becomes several Notes, so maths Notes are numbered by Note, not by Video:

    Note ID = 200 + 10 × session + part        (part 0–9)

M01 → 210; M02 → 220, 221, …; M03 → 230, …; M25 → 450. Folders are `<ID>-<topic>/`, e.g. `220-measures-of-central-tendency/`.
In `course_map/concepts.yaml`, the `notes:` map and every Concept's `videos:` list use these IDs, so the map tools work unchanged.

## No duplication

The ML Notes already teach much of this (descriptive statistics 19, univariate/bivariate analysis 20–21, outliers 41–44,
PCA 47–48, gradient descent 57–60, probability and Bayes 82–90, tensors 11). A maths Note recaps those in one line with a
link and teaches only what is new: more depth, proofs, new concepts.

## Members-only sessions

M11, M12, M17–M23 are CampusX channel-member videos and cannot be downloaded without the user's login. Until then, their
topics are covered from free videos in the other maths playlists where possible.

## Supplementary videos (M26–M37)

Chosen to cover concepts the free CampusX sessions lack (see `transcripts/maths_playlist.txt`). English videos are read from their YouTube captions (`transcripts/Mnn.captions-en.txt`); Hindi ones go through Whisper.

| Session | Source | Note IDs | Fills |
|---|---|---|---|
| M26 | CampusX free linear algebra session | 460+ | linear algebra basics |
| M27 | Equation of a hyperplane | 470 (if new) | compare with 363 |
| M28–M33 | 3Blue1Brown, Essence of Linear Algebra ch. 1, 2, 3, 4, 9, 14 | 480–530 | span and basis, matrices as transformations, composition, duality, eigenvectors |
| M34–M36 | 365 Data Science: binomial, Bernoulli, Poisson | 540–560 | Poisson (binomial and Bernoulli only if new) |
| M37 | p-value, t-test, chi-square, ANOVA tutorial | 570+ | chi-square tests, ANOVA |
