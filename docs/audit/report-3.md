# Claims audit, group 3 (Notes 95–122)

28 Notes checked. Every edited Note was rebuilt with `tools/build.sh` and printed "Built".
Final rules applied: grounding order (source, maths, test), nothing unresolved left in a Note, "Learning comes first" (short tags in text, `## Sources` before Key terms, experiments in Extra boxes or the notebook), "Intuitions are welcome", and STYLE-naming for new or rewritten text.

## Findings

| Note | quote (short) | verdict | action |
|---|---|---|---|
| 95 | "name comes from neural networks… used much less than RBF" | UNSUPPORTED | sourced: Lin & Lin 2003, sigmoid kernels for SVM |
| 95 | "The three that come with SVM in scikit-learn" | WRONG FACT | reworded: SVC also has a linear kernel |
| 95 | "for RBF the higher-dimensional space is even infinite" | UNSUPPORTED | sourced: MML §12.4 |
| 96 | "weighted sum of bumps, one per support vector" | UNSUPPORTED | sourced: sklearn UG §1.4.7 |
| 96 | poly kernel formula, coef0 = 0 by default | UNSUPPORTED | sourced: sklearn UG §1.4.6, SVC reference |
| 96 | "coef0=1 with degree 3 would also fit the circles" | UNSUPPORTED | tested: accuracy 1.00, 8 support vectors |
| 96 | "few support vectors, as the SVM intuition Note predicted" | WRONG CITATION | sourced: ESL §12.2.1; tested: the 76 support vectors are exactly the 76 points inside the margin or misclassified |
| 96 | "SVM only needs dot products; RBF space infinite" | UNSUPPORTED | sourced: MML §12.4 |
| 96 | gamma Extra | UNSUPPORTED | sourced: sklearn "RBF SVM parameters" example, SVC reference |
| 97 | "This is rare among ML models" (interpretability) | UNSUPPORTED | sourced: sklearn UG §1.10 ("white box") |
| 97 | "training costs much more than using it" | UNSUPPORTED | sourced: sklearn UG §1.10 |
| 97 | imbalanced data: "rare class gets few leaves" | UNSUPPORTED | sourced: sklearn UG §1.10 |
| 97 | "After a dozen questions" (Akinator) | UNSUPPORTED | kept as intuition: "after about a dozen questions" |
| 97 | differential entropy formula | UNSUPPORTED | sourced: Cover & Thomas 2006, Ex. 8.1.2 |
| 97 | "every common tree algorithm is greedy" | UNSUPPORTED | sourced: sklearn UG §1.10 |
| 97 | "entropy and log_loss are the same criterion" | UNSUPPORTED | sourced: sklearn UG §1.10.7.1 |
| 97 | "Gini and entropy give very similar trees" | WRONG FACT | tested: accuracy within 0.02 on 3 datasets, different root on 2; reworded |
| 97 | thresholds are midpoints | UNSUPPORTED | sourced: sklearn `tree/_splitter.pyx` |
| 97 | numerical features / 255 bins | WRONG FACT | sourced: sklearn UG §1.10, §1.10.4; HistGB and LightGBM default 255 |
| 98 | "CV prefers the simplest tree that captures the pattern" | UNSUPPORTED | tested: CV accuracy falls after depth 2; sourced: ISLR §5.1 |
| 98 | "usually give very similar trees" | WRONG FACT | reworded to "similar accuracy" |
| 98 | random_state Extra | UNSUPPORTED | sourced: sklearn DecisionTreeClassifier reference |
| 98 | max_leaf_nodes grows best-first | UNSUPPORTED | sourced: sklearn reference |
| 98 | impurity-decrease formula | UNSUPPORTED | sourced: sklearn reference |
| 99 | absolute_error: outliers pull less, much slower | UNSUPPORTED | sourced: ESL §10.6; tested: about 2.4 times slower |
| 99 | poisson "for counts" | UNSUPPORTED | sourced: sklearn UG §1.10.7.2 |
| 99 | friedman_mse "always gave the same trees" | UNSUPPORTED | sourced: sklearn 1.9 deprecation |
| 99 | "often called variance reduction" | UNSUPPORTED | sourced: sklearn DecisionTreeRegressor reference |
| 99 | load_boston removed because of column B | UNSUPPORTED | sourced: sklearn 1.0/1.1 deprecation notice |
| 99 | "0.725 can be trusted because it comes from CV" | WRONG FACT | tested: on fresh folds 0.663 vs 0.662 untuned; explained as selection bias (Cawley & Talbot 2010) |
| 99 | "the split happened to favour the first tree" | WRONG FACT | tested: over 30 splits the first tree is better (0.749 vs 0.728) |
| 99 | "more values can improve it further" | UNSUPPORTED | deleted (test shows no gain) |
| 99 | "a single tree's importances change a lot" | UNSUPPORTED | sourced: ESL §9.2.4; tested: std 0.20 (tree) vs 0.12 (forest) |
| 100 | dtreeviz supports XGBoost, LightGBM, Spark | UNSUPPORTED | sourced: dtreeviz README |
| 100 | plot_tree `feature_names`, `class_names`, `filled` | UNSUPPORTED | sourced: sklearn plot_tree reference |
| 100 | dtreeviz 2.0 API, instance_feature_importance | UNSUPPORTED | sourced: dtreeviz README |
| 100 | "a different split can rank the minor columns differently" | UNSUPPORTED | tested: over 20 splits the last two swap 10 vs 10 |
| 101 | Galton's ox, 1,207 lb vs 1,198 lb | UNSUPPORTED | sourced: Galton 1907, *Nature* |
| 101 | "tree ensembles beat deep learning on small tables" | UNSUPPORTED | sourced: Grinsztajn et al., NeurIPS 2022 |
| 101 | "bagging with trees = random forest" | WRONG FACT | sourced: Breiman 2001; link to Note 110 |
| 102 | "Condorcet's jury theorem (1785)" | UNSUPPORTED | sourced: Condorcet 1785 |
| 102 | models "tend to fail on the same hard rows… why ensembles make models different" | UNSUPPORTED | sourced: ESL §15.2, Dietterich 2000 §1; tied to Fig. 2b numbers |
| 103 | "LR, SVM … voting 0.77" | WRONG FACT | fixed to 0.76 |
| 103 | "soft voting often better: a probability carries more information" | UNSUPPORTED | tested: on the 30 disputed points soft voting is right on 28 and follows the confident forest each time; reworded |
| 103 | "smoothing is often why it does better" | UNSUPPORTED | reworded to "sometimes", as in the lecture |
| 104 | "rows stored grouped by town… folds test on unseen towns" | UNSUPPORTED | sourced: Gilley & Pace 1996 corrected data; tested: 453 of 506 test rows from unseen towns in order vs 19 shuffled; GroupKFold in between |
| 104 | "`n_jobs=-1` saves time on big data" | UNSUPPORTED | tested: 15 times slower here (1.6 s vs 0.11 s); sourced: sklearn UG §10.3.1 |
| 105 | "both classes always appear in every sample" | UNSUPPORTED | replaced with data: trees on 100 rows reach depth 3 to 6 |
| 105 | "bias stays tiny (0.009 and 0.004)" | WRONG FACT | fixed: these are squared bias |
| 106 | "bagging usually beats pasting… more varied, lower variance" | UNSUPPORTED | sourced: ESL §15.2; tested: correlation 0.82 vs 0.84, variance 0.041 vs 0.055, squared bias 0.0019 vs 0.0013 |
| 106 | "480 fits, about 5 minutes" | WRONG FACT | fixed: about 12 minutes measured |
| 106 | "`base_estimator` removed in 1.4" | UNSUPPORTED | sourced: sklearn 1.2 release notes |
| 107 | "102 rows is a small, noisy test" | UNSUPPORTED | tested: 100 splits give 0.63 to 0.94 (mean 0.857); tuned beats default on 79 of 100 |
| 108 | Breiman 2001, bagging 1996, Ho 1995 | UNSUPPORTED | sourced: Breiman 1996, 2001; Ho 1995 |
| 108 | "fresh random columns at every node adds more variety" | UNSUPPORTED | sourced: Breiman 2001 §4, ESL §15.2 |
| 109 | "trees that did see it outvote the rest" | UNSUPPORTED | sourced: ESL §7.11 (63%); tested: every point seen by ≥57% of trees, which are always right on it |
| 109 | "On noisier data the forest's training accuracy can fall below 1" | WRONG FACT | tested: noise 0.35 to 1.0 all give 1.00; replaced with the result |
| 110 | variance formula "from Breiman's random forest paper and ESL" | WRONG CITATION | sourced: ESL §15.2, eq. 15.1 (not in Breiman 2001) |
| 110 | "That confirms node-level sampling is the whole difference" | UNSUPPORTED | sourced: sklearn UG §1.11; data: 0.917 = 0.917 |
| 111 | `max_features="auto"` removed in 1.3, defaults changed in 1.1 | UNSUPPORTED (uncited) | sourced: sklearn API docs (1.1, current) |
| 111 | `bootstrap=False, max_features=None`: only tie-breaking randomness | UNSUPPORTED | sourced: sklearn DecisionTreeClassifier `random_state` |
| 111 | `monotonic_cst` added 1.4, regression and two-class | UNSUPPORTED (uncited) | sourced: sklearn API docs; added "not multi-class or multi-output" |
| 111 | mse/mae removed 1.2, friedman_mse deprecated 1.9, min_impurity_split removed 1.0 | UNSUPPORTED (uncited) | sourced: sklearn API docs 0.24, 1.1, 1.9 |
| 112 | "A random forest needs no scaling" (causal) | UNSUPPORTED | sourced: ESL §10.7 Table 10.1; tested: scaler leaves 0.836 / 0.835 |
| 112 | "The cross-validated gain is small but real" (max_samples=0.75) | WRONG FACT | tested: over 10 seeds mean gain 0.0003 (−0.010 to +0.017); reworded as noise |
| 112 | "randomized search over a wide grid, then grid search narrow" | UNSUPPORTED | deleted (no authoritative source found) |
| 113 | "OOB pessimistic: each OOB prediction comes from a third of the forest" | UNSUPPORTED | replaced with the sourced mechanism: Janitza & Hornung 2018 (balanced classes, few rows), tied to the Note's 0.818 vs 0.836 |
| 113 | "hard votes and soft votes give the same score" | UNSUPPORTED | tested: both 0.835 (new notebook cell) |
| 114 | "forest's mean much more stable" | UNSUPPORTED | tested: importance std 0.035–0.076 (tree) vs 0.012–0.014 (forest) over 20 resamples |
| 114 | high-cardinality column gets credit from chance deep splits | UNSUPPORTED | sourced: Strobl et al. 2007, sklearn UG §5.2; tested: raising min_samples_leaf 1→50 cuts random_id from 0.100 to 0.021 |
| 114 | correlated features both look unimportant under permutation | UNSUPPORTED | sourced: sklearn UG §5.2.3 |
| 114 | "cannot be fooled by splits that only fit the training set" | UNSUPPORTED | sourced: sklearn UG §5.2 |
| 114 | single-node trees dropped from the mean, renormalized | UNSUPPORTED | sourced: sklearn `ensemble/_forest.py` |
| 115 | Freund & Schapire 1995; Viola-Jones face detection 2001 | UNSUPPORTED (uncited) | sourced: Freund & Schapire 1997, Viola & Jones 2001 |
| 115 | "libraries pick one class… almost never happens" | UNSUPPORTED | sourced: sklearn `_weight_boosting.py` (tie gives first class); "almost never" removed |
| 116 | "stops adding stumps when error reaches 0.5" | UNSUPPORTED | sourced: sklearn `_weight_boosting.py` |
| 116 | "mistakes end up with exactly half the weight… forced to learn something new" | UNSUPPORTED | maths: both totals √(err(1−err)) = 0.4899, old stump gets α = 0 |
| 116 | "scikit-learn's AdaBoost works this way, no random draws" | UNSUPPORTED | sourced: sklearn source (`sample_weight`) |
| 117 | "ties broken by shuffling columns; seed 0 gives X2" | UNSUPPORTED | sourced: sklearn DecisionTreeClassifier docs; tested: seeds 0–9 give X2 six times |
| 117 | "error meaninglessly high (0.7), alpha negative" | UNSUPPORTED | tested: error 0.7, α = −0.42 |
| 117 | "scikit-learn stops early for a perfect stump" | UNSUPPORTED | sourced: sklearn source |
| 118 | "stops earlier only if a stump is perfect" | WRONG FACT | reworded: also stops at error ≥ 0.5 (sklearn source) |
| 118 | "SAMME.R often converged faster" | UNSUPPORTED | sourced: sklearn 1.5 docs |
| 118 | "deprecated in 1.4 and later removed" | UNSUPPORTED | sourced: sklearn 1.5 docs |
| 118 | "0.812 rather than the 0.786 older versions gave" | UNSUPPORTED | deleted |
| 118 | "each extra stage focuses on noise" | UNSUPPORTED | sourced: Dietterich 2000 |
| 118 | "more columns or deeper trees: stronger effect" | UNSUPPORTED | reworded to the Note's result (depth-8 trees: train 1.00) |
| 118 | "large n_estimators with small learning_rate is the usual recipe" | UNSUPPORTED | sourced: ESL §10.12.1 |
| 119 | "the variance stays low" | WRONG FACT | reworded "fairly low", with Note 118 numbers |
| 120 | "XGBoost has won many Kaggle competitions" | UNSUPPORTED | sourced: Chen & Guestrin 2016 |
| 120 | "4 to 8 leaves work well" (full title mid-sentence) | WRONG CITATION | sourced: ESL §10.11, short tag |
| 121 | "Runge's phenomenon" | UNSUPPORTED | sourced: Runge 1901 |
| 121 | "accepts any differentiable loss" | UNSUPPORTED | sourced: Friedman 2001 |
| 121 | "gradient descent in function space" | UNSUPPORTED | sourced: Friedman 2001 |
| 121 | "each tree moves the sum closer to the true function" | WRONG FACT | maths: "closer to the training data"; training loss cannot rise |
| 122 | "step 1 gives exactly this log-odds" | UNSUPPORTED | maths: σ(γ) = 5/8 gives γ = ln(5/3) |
| 122 | "one Newton step; scikit-learn uses the same formula" | UNSUPPORTED | sourced: Friedman 2001, sklearn `_gb.py` |
| 122 | "gap is a sign more trees would overfit" | UNSUPPORTED | tested: test accuracy peaks at 0.939 after 92 trees, 0.917 by 300 |

## Counts per Note

| Note | Findings | Note | Findings |
|---|---|---|---|
| 95 | 3 | 109 | 2 |
| 96 | 6 | 110 | 2 |
| 97 | 10 | 111 | 4 |
| 98 | 5 | 112 | 3 |
| 99 | 9 | 113 | 2 |
| 100 | 4 | 114 | 5 |
| 101 | 3 | 115 | 2 |
| 102 | 2 | 116 | 3 |
| 103 | 3 | 117 | 3 |
| 104 | 2 | 118 | 7 |
| 105 | 2 | 119 | 1 |
| 106 | 3 | 120 | 2 |
| 107 | 1 | 121 | 4 |
| 108 | 2 | 122 | 3 |

Total: 98 findings (80 UNSUPPORTED, 15 WRONG FACT, 3 WRONG CITATION). No Note was free of findings.

## UNRESOLVED (removed from Note)

- 99, §7.2: "Adding more values and more hyperparameters can improve it further." (the Notebook test shows no gain)
- 112, §7.3: "A common approach combines the two: a randomized search over a wide grid finds the promising region, then a grid search over a narrow grid around it."
- 118: "This is also why the default model here scores 0.812 rather than the 0.786 that older versions gave with SAMME.R (section 3)."

## Notes

- Friedman 2001 is cited without section numbers (no readable full copy found); secondary sources confirm the Newton-step claim.
- New experiment cells were added to the notebooks of 96, 97, 98, 99, 100, 103, 104, 106, 107, 109, 112, 113, 114, 117 and 122. They are saved without outputs.
- New data file: `104-voting-regressor/data/boston_corrected.txt` (Gilley & Pace corrected Boston data, with town names).
