# Final pass: summary of finished groups

| Group | Notes | Experiments redesigned | Main fixes |
|---|---|---|---|
| 0 | 01–34 | 32 binarization (+ KNN row in 24, tip-share cell in 21) | blogs → papers (Sahami 1998, conda docs, Zheng and Casari); about 250 vague-pronoun fixes |
| 2 | 63–94 | 63, 66, 67 (bias–variance now matches ISL), 69, 80, 81 (real data) | about 30 analogies; Gelman, Altman and Bland, Bishop added |
| 3 | 95–122 | 98, 103, 104, 107, 110 (Spambase), 111, 112 (nested CV: tuning does not beat defaults, Probst 2019), 113, 118, 120, 122 — all seed- or split-averaged | about 35 citations added (ESL sections, Breiman 1996, Dietterich 2000); about 30 unsupported claims removed; about 140 vague-pronoun fixes |
| 4 | 123–134, 210–261 | 123 timing and GPU, 128 elbow (Old Faithful), 131 dendrogram, 133 (mammography, real data) | Wikipedia, LibreTexts and blogs replaced; 10 unsupported claims removed |
| 5 | 262–362 | 301, 302 (real data, adequate power) | Sources numbered in 18 Notes; Gosset sentence restored afterwards (see KEEP.md) |
| 6 | 363–641 | 571 (expected-count rule), 641 (local maxima on Iris) | Strang lecture → textbook; OpenIntro → NIST; StatQuest and 3Blue1Brown cited by author and site |

## Open items for the user
- **25:** "min-max is used about 90% of the time" and "standardization gives better results in most cases" rest only on the transcript. Cut them, or find a book source.
- **12:** the conda environment is named `campusx` in the commands (from environment.yml).
- **05, 08, 11:** YouTube appears as a product example (recommendations, bit rates), not as a source.
- **570:** still uses a simulated `people.csv`, though no result contradicts its lesson.
- Group 3: 112, 103–108 keep saved notebook outputs; the other Notes store notebooks without outputs. Pick one convention at the end.
- Group 3: 106 says the grid search takes "about 12 minutes"; on the loaded laptop it took 29.
