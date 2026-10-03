# Claims audit, group 2 (Notes 63–94)

32 Notes checked. 85 findings: 70 UNSUPPORTED, 14 WRONG FACT, 1 WRONG CITATION. No item is left UNRESOLVED; nothing was removed without a replacement.

Every edited folder was rebuilt with `tools/build.sh` and printed "Built". In-text citations use short tags; each Note has a `Sources` list before Key terms.

## Findings

Note | quote (short) | verdict | action
---|---|---|---
| 63 | "The intercept b is not penalised: it only shifts the line" | UNSUPPORTED | sourced: ISL 2e (James et al. 2021) §6.2.1 p.238 |
| 63 | "On new data drawn from the same source, the flatter line is indeed better" | UNSUPPORTED | reworded: test points were generated from a slope-0.9 pattern, so the figure cannot test the claim; now called an illustration, grounding moved to ISL cite + diabetes data |
| 63 | "Ridge gives up a little accuracy ... bias-variance trade-off" | UNSUPPORTED | sourced: ISL 2e §6.2.1 p.240 |
| 63 | "every coefficient moves towards 0 as alpha grows" | WRONG FACT | tested: age and s6 first grow, s3 flips sign; reworded |
| 63 | "s1 and s5, signs of multicollinearity, first to be tamed" | UNSUPPORTED | tested: s1 is correlated with s2 (r=0.90, coefs -971/+574), s1 shrinks fastest; sourced: ESL 2e §3.4.1 p.63 |
| 63 | Extra: "inputs are standardised before Ridge (diabetes already are)" | UNSUPPORTED | sourced: ISL 2e §6.2.1 p.239; scikit-learn load_diabetes docs |
| 63 | summary "small alpha: often better on new data" | UNSUPPORTED | reworded: "here slightly better test R²" (data: 0.519 to 0.523) |
| 64 | Extra: "scikit-learn centres X and y ... cholesky solves the same equation" | UNSUPPORTED | sourced: scikit-learn 1.9 `_preprocess_data` docstring and `Ridge` solver docs |
| 64 | Extra: "+λI always makes it invertible" | UNSUPPORTED | sourced: ESL 2e §3.4.1 p.64 (Hoerl and Kennard 1970); maths added (vᵀ(XᵀX+λI)v > 0) |
| 65 | "This is why the L2 penalty is also called weight decay, the name used in deep learning" | UNSUPPORTED | sourced: ESL 2e §3.4.1 p.63 (update-rule maths already in Note) |
| 65 | "The penalty also makes the bowl rounder, so the path heads more directly" | WRONG FACT | tested: curvature ratio rises 1.2 to 1.9 with λ=100; replaced with second-derivative maths (87 to 187 along m) |
| 65 | "That is why the learning rate must be tiny ... 0.006 overshoots" | UNSUPPORTED | maths added: η < 2/h_max; tested: h_max = 353, limit 0.0057, between 0.005 and 0.006 |
| 65 | "inputs strongly correlated (s1 and s5) ... acts like extra regularisation and here happened to help" | WRONG FACT | tested: flattest eigenvector is s1/s2 (not s1/s5), eigenvalue 0.0083, ~24,000 steps; 1,146 of the gap lies on it; sourced: Goodfellow et al. 2016 §7.8; tested (new notebook cell): gain holds on average over 30 splits (0.461 vs 0.459); tied to ISL §6.2.1 |
| 65 | Extra: early stopping "widely used for neural networks" | UNSUPPORTED | sourced: Goodfellow et al. 2016 §7.8 |
| 65 | "iterative solvers choose their own step sizes" | UNSUPPORTED | reworded to the fact: Ridge has no learning-rate setting (sklearn docs) |
| 65 | Extra: "SGDRegressor alpha = Ridge alpha / n" | UNSUPPORTED | sourced: sklearn user guide §1.5.8 (maths shown); tested: SGD within 3 of Ridge(0.353), 840 from Ridge(0.001) |
| 66 | "every coefficient gets closer to 0. None becomes exactly 0" | WRONG FACT | reworded; sourced: ISL 2e §6.2.2 p.241; data: s1, s2 and age do not shrink steadily, s1/s2 pass through 0 |
| 66 | "each tenfold increase makes the coefficients ten times smaller" (no meaning given) | UNSUPPORTED | maths added: λ ≫ largest eigenvalue (3.2) gives w ≈ Xᵀy/λ |
| 66 | Extra: "s1, s2, s5 strongly correlated, so ... effect moves to other inputs" | UNSUPPORTED | tested: dropping s1, s2, s5 moves age from −9.2 to +34.3 (42 at alpha 1); correlation wording corrected (s1–s2 r=0.90, s5 weaker) |
| 66 | Extra: "wild curves at tiny alpha move the average curve ... edge effect" | UNSUPPORTED | tested: excess bias² at alpha 0.01 comes almost all from the test point at x=2.81, at the edge of the training range (24.3 vs 1.9) |
| 66 | Extra: "the name comes from ... a ridge along the diagonal" | WRONG FACT | sourced: Hoerl and Kennard 1970, Technometrics, §2 (named after Hoerl's ridge analysis of response surfaces) |
| 66 | Point 5 "especially correlated ones" | UNSUPPORTED | sourced: ESL 2e §3.4.1 p.63, tied to s1/s2 pair |
| 67 | "LASSO stands for least absolute shrinkage and selection operator" | UNSUPPORTED | sourced: Tibshirani 1996, JRSS-B, §1 |
| 67 | Extra: sklearn Lasso minimises 1/(2n)·RSS + α·Σ abs(β) | UNSUPPORTED | sourced: scikit-learn `Lasso` docs |
| 67 | "bmi, bp and s5, the three most useful inputs here" | UNSUPPORTED | tested: best of all 120 triples by 5-fold CV R² (0.485) |
| 67 | Extra: "preferred when many columns ... faster to use and easier to explain" | UNSUPPORTED | sourced: ISL 2e §6.2.2 pp.242, 246; "faster to use" removed |
| 67 | Key point "Small ones go first; the strongest inputs survive longest" | WRONG FACT | reworded: s2 (561) goes second; data in the Note's own table |
| 67 | "cut back hard at first, which removes most of the overfitting" | WRONG FACT | tested: test R² 0.440 → 0.441 → 0.433, overfitting not removed; reworded |
| 67 | "s1 and s2 had huge coefficients only because they are correlated" | UNSUPPORTED | sourced: ESL 2e §3.4.1 p.63; data r=0.90 |
| 67 | Extra: Ridge vs Lasso push near 0 (compared penalty values, called it force) | UNSUPPORTED | maths: slopes 2λm vs λ |
| 67 | Ridge-or-Lasso table (best when, closed form, correlated) | UNSUPPORTED | sourced: ISL 2e p.246; ESL 2e §3.4.2 p.68; Zou and Hastie 2005 §1 |
| 68 | Extra: soft thresholding; "scikit-learn applies this same soft-threshold step" | UNSUPPORTED | sourced: ESL 2e §3.8.6 p.93; scikit-learn `Lasso` docs (coordinate descent) |
| 69 | Extra: "0.9 means 90% Lasso" (lecture said 90% Ridge) | UNSUPPORTED (corrects lecture) | sourced: scikit-learn `ElasticNet` docs |
| 69 | Extra: sklearn ElasticNet objective | UNSUPPORTED | sourced: scikit-learn `ElasticNet` docs |
| 69 | "rounded, but still with corners ... can still produce exact zeros" | UNSUPPORTED | sourced: Zou and Hastie 2005 §2.1, Fig. 1 |
| 69 | "Linear regression gives the three copies wild values" (no meaning) | UNSUPPORTED | sourced: ESL 2e §3.4.1 p.63 |
| 69 | "Which copy it drops is close to arbitrary" | UNSUPPORTED | sourced: Zou and Hastie 2005 §1 |
| 69 | "grouping effect" | UNSUPPORTED | sourced: Zou and Hastie 2005 §2.3 (Lemma 2) |
| 69 | Extra: "ElasticNet usually the better choice; SGD when data too large for memory" | UNSUPPORTED | sourced: scikit-learn user guide §1.5.2 (>10,000 samples); memory claim removed |
| 69 | "When to use which" table | UNSUPPORTED | sourced: ISL 2e p.246; Zou and Hastie 2005 |
| 72 | "it settles where the pushes balance, in the middle of the gap" | WRONG FACT | contradicted by the Note's own Section 7 data (gaps 3.07 vs 1.21); reworded to point at that data |
| 72 | "sigma is the Greek letter for s" (name origin) | UNSUPPORTED | sourced: Online Etymology Dictionary, "sigmoid" |
| 72 | "something is still missing. The missing piece is a proper loss function" (why sigmoid line is off-centre) | WRONG FACT | tested (new notebook cell): with more loops the line moves to logistic regression's; with sklearn's default L2 penalty it matches (2.18/2.00 vs 2.20/1.97); sourced: Bishop 2006 §4.3.2 (update = log-loss gradient; separable data needs a penalty) |
| 73 | "The reason is deeper ... nothing in that procedure says which line is best, so no guarantee it ends up there" | WRONG FACT | reworded; the sigmoid update is the log-loss gradient step (Bishop §4.3.2; test in Note 72) |
| 73 | "That second effect is what keeps pushing the line into the middle of the gap" | UNSUPPORTED | sourced: Soudry et al. 2018, JMLR (GD on separable data turns to max-margin direction) |
| 73 | "no closed-form solution, because w sits inside the sigmoid" | UNSUPPORTED | sourced: Bishop §4.3.3 |
| 74 | Extra: vanishing gradient; "one reason deep networks mostly use ReLU" | UNSUPPORTED | sourced: Goodfellow et al. 2016 §6.1, §6.3.2 |
| 75 | Extra: "same form as linear regression gradient" | UNSUPPORTED | sourced: Bishop §4.3.2 (maths also in Note) |
| 75 | "The line's position settles while its weights grow" | WRONG FACT | own table: slope −w1/w2 goes −30 → −23 → −18; reworded; sourced: Soudry et al. 2018; Bishop §4.3.2 |
| 75 | "one reason scikit-learn uses a penalty by default" | UNSUPPORTED | reworded: regularisation is the standard fix (Bishop §4.3.2); motive claim removed |
| 76 | Extra: "Some books draw the matrix the other way round" | UNSUPPORTED | sourced: Fawcett 2006, Fig. 1 (scikit-learn layout is in the Note's own output) |
| 77 | Extra: "Recall is also called sensitivity or true positive rate, names common in medicine" | UNSUPPORTED | sourced: Fawcett 2006 §2 |
| 77 | "Precision and recall usually pull against each other" | UNSUPPORTED | sourced: scikit-learn "Precision-Recall" example |
| 77 | Extra: "positive class is usually the one we care about, so class 1 is the default" | UNSUPPORTED | reworded to the fact: default `pos_label=1` (scikit-learn docs) |
| 78 | "roc_curve tries every distinct probability as a threshold (54 here)" | WRONG FACT | tested: 154 distinct probabilities, 54 returned after `drop_intermediate=True`; sourced: scikit-learn docs |
| 78 | Extra: Youden's J | UNSUPPORTED | sourced: Youden 1950, Cancer 3:32–35; tested: 0.287 |
| 78 | AUC table "0.5 random; below 0.5 classes the wrong way round" | UNSUPPORTED | sourced: Fawcett 2006 §3, §7 |
| 78 | Extra: AUC = P(random positive ranked above random negative) | UNSUPPORTED | sourced: Fawcett 2006 §7; tested: pair count 0.823 |
| 79 | "standard output layer of neural networks that classify" | UNSUPPORTED | sourced: Goodfellow et al. 2016 §6.2.2.3 |
| 79 | Extra: "Recent versions removed multi_class ... default uses softmax" | UNSUPPORTED | sourced: scikit-learn 1.9 `LogisticRegression` docs/source (no `multi_class` parameter; softmax for multiclass) |
| 80 | "without the scaler ... the solver struggles to converge" | UNSUPPORTED | tested (new notebook cell): degree 10 converges either way, 279 vs 182 steps; reworded to the data |
| 80 | Extra: "default C=1 overfits less ... one more reason to use the default" | UNSUPPORTED | tested: high degrees CV 0.900/0.905 → 0.910/0.915, but degree 4 drops 0.935 → 0.910; advice replaced with "tune C" |
| 81 | solver table "liblinear: one-vs-rest for several classes" | WRONG FACT | tested: liblinear raises an error on 3 classes in 1.9; sourced: scikit-learn docs |
| 81 | "`n_jobs`: CPU cores to use; only helps in a few cases" | WRONG FACT | sourced: scikit-learn 1.9 docs ("Does not have any effect", deprecated 1.8) |
| 81 | "solver struggles to converge" without penalty | UNSUPPORTED | tested: stops at max_iter=100 with ConvergenceWarning; reworded |
| 82 | "one of the simplest and fastest ... widely used for text such as spam filtering" | UNSUPPORTED | sourced: scikit-learn user guide §1.9 |
| 71 | "the perceptron can reach zero training error and still do worse on new data" | UNSUPPORTED | tested (new notebook cell, real iris data, setosa vs versicolor, 100 random 20-flower training sets × 5 seeds): perceptron 5.5% vs logistic 1.2% test error; sourced: ISL §9.1.3 |
| 71 | Extra: "default C=1 ... misclassifies one point by a hair" | UNSUPPORTED | sourced: scikit-learn `LogisticRegression` docs; tested: 1 point, 0.009 from the line |
| 83 | "the simplification works surprisingly well" | UNSUPPORTED | sourced: ISL 2e §4.4.4 p.155 (bias–variance reason added) |
| 85 | "published after Thomas Bayes's death in the 1760s" | UNSUPPORTED | sourced: Bayes 1763, Phil. Trans. R. Soc. 53:370–418 (made precise: 1763) |
| 88 | "often still picks the right class ... probabilities tend to be too extreme" | UNSUPPORTED | sourced: Domingos and Pazzani 1997; scikit-learn user guide §1.9 (the Note's own copies-of-toss figure shows the extreme probabilities) |
| 89 | Laplace (add-one) smoothing and the zero-frequency problem (not in transcript) | UNSUPPORTED | sourced: Manning, Raghavan and Schütze 2008, §13.2; scikit-learn `CategoricalNB` docs |
| 90 | Python note: GaussianNB divides by n and adds a tiny amount | UNSUPPORTED | sourced: scikit-learn `GaussianNB` docs (var_smoothing); numbers already in notebook (99.2%) |
| 90 | Variant table (multinomial, Bernoulli, categorical) | UNSUPPORTED | sourced: scikit-learn user guide §1.9 |
| 91 | Extra: "Minkowski with p=2 by default" | UNSUPPORTED | sourced: scikit-learn `KNeighborsClassifier` docs |
| 91 | Extra: on a tie "picks the class that comes first in its sorted list" | UNSUPPORTED | tested (new notebook cell): 2–2 tie returns label 0 either way round |
| 91 | Extra: KD-tree/ball tree "helps little with many columns" | UNSUPPORTED | sourced: scikit-learn user guide §1.6.4 (D < ~20) |
| 92 | Extra history: "Vapnik and Chervonenkis in the 1960s ... 1992 ... 1995" | WRONG CITATION (no source; V–C attribution not in the cited history) | sourced: Cortes and Vapnik 1995 §1 (optimal hyperplanes 1965, Boser et al. 1992); reworded to "Vapnik's work in the 1960s" |
| 92 | "strong, widely used algorithm that works in many situations" | UNSUPPORTED | sourced: ISL 2e ch. 9 intro p.367 |
| 92 | "The hope is that such a line generalises better" | UNSUPPORTED | sourced: ISL 2e §9.1.3; linked to the Note 71 test |
| 92 | Extra: deleting non-support vectors gives the same line | UNSUPPORTED | sourced: ISL 2e §9.1.3 |
| 92 | Extra: hard margin sensitive to outliers | UNSUPPORTED | sourced: ISL 2e §9.2.1 |
| 94 | Extra: "in scikit-learn the term is written ½‖w‖²" | UNSUPPORTED | sourced: scikit-learn user guide §1.4.7 |
| 94 | "C is inversely proportional to λ" | UNSUPPORTED | sourced: ESL 2e §12.3.2 p.426 (λ = 1/C) |
| 94 | "The convention comes from SVM" (why LogisticRegression uses C) | UNSUPPORTED | reworded: "follows the same convention as SVM" (scikit-learn `LogisticRegression` docs: "Like in support vector machines") |

## Counts per Note

| Note | Findings | Note | Findings |
|---|---|---|---|
| 63 ridge intuition | 7 | 79 softmax | 2 |
| 64 ridge maths | 2 | 80 polynomial logistic | 2 |
| 65 ridge gradient descent | 7 | 81 logistic hyperparameters | 3 |
| 66 ridge key points | 6 | 82 conditional probability | 1 |
| 67 lasso | 9 | 83 independent events | 1 |
| 68 lasso sparsity | 1 | 84 mutually exclusive | 0 |
| 69 elastic net | 8 | 85 Bayes theorem | 1 |
| 70 perceptron trick | 0 | 86 Bayes problem | 0 |
| 71 perceptron code | 2 | 87 naive Bayes intuition | 0 |
| 72 sigmoid | 3 | 88 naive Bayes maths | 1 |
| 73 log loss | 3 | 89 naive Bayes code | 1 |
| 74 sigmoid derivative | 1 | 90 Gaussian naive Bayes | 2 |
| 75 logistic gradient descent | 3 | 91 KNN | 3 |
| 76 accuracy, confusion matrix | 1 | 92 SVM intuition | 5 |
| 77 precision, recall, F1 | 3 | 93 SVM maths | 0 |
| 78 ROC-AUC | 4 | 94 SVM soft margin | 3 |

## New notebook experiments

- 71: perceptron vs logistic regression on real iris data (setosa vs versicolor), 100 random training draws × 5 seeds: test error 5.5% vs 1.2%.
- 72: sigmoid perceptron run longer and with scikit-learn's default penalty: it lands on scikit-learn's line (gaps 2.18/2.00 vs 2.20/1.97).
- 65: early stopping vs exact Ridge over 30 splits (mean test R² 0.461 vs 0.459).
- 80: scaler on/off (solver steps) and C=1 vs weak penalty across degrees.
- 91: KNN tie-breaking.

## UNRESOLVED (removed from Note)

None.
