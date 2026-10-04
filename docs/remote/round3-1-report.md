# Round 3 report, list 1 (docs/visual-audit/round3_1.txt)

Words per visual (wpv) and figure share (sections with a figure / numbered sections) are measured with `docs/visual-audit/measure.py`, which counts table words as text.

## Summary

- **All 43 Notes of the list were handled.** 35 got new visuals: 53 new figures from 52 new scripts, 27 of them animations (GIF plus a PDF frame or grid). 8 were already strong and are left unchanged, each with a reason below. Every touched Note was rebuilt with `tools/build.sh` and printed "Built"; I looked at every new figure and at its PDF page, and fixed overlaps, clipping, faint lines and wrong axes before moving on.
- **Target ("strong": at most about 400 words per visual and at least 60% of sections with a figure):** 18 of the 43 Notes met both parts before this round; 36 do now. The 7 that do not all meet the figure share but not the word limit:
  - 01-course-map (553): its words are generated tables;
  - 1011 (435);
  - 1027 (421), 1024 (414), 1019 (404), 1002 (403) and 1028 (402), each within about 5% of the limit.
- **Experiments.** Every number drawn is asserted in its script. Keras runs that must match a Note's existing numbers ran on CPU with the Notebook's seeds, and all of them reproduce the Note exactly (1011, 1013, 1028, 1029). New experiments ran on topgro's GPU (the CPU-vs-GPU timing of 1002, and 1021, 1031, 1050); the other new training runs (1002's hidden layers, 1024) ran on CPU with fixed seeds. Training runs live in each Note's new `experiments/` folder and save small results to `data/`, so the build only plots.
- **Experiments run but not used, because the data did not show the principle cleanly:** 02 (ML vs DL by data size on MNIST: the CNN won at every size), 105 (tree vs KNN instability on the iris subset: no clear difference; replaced by a variance measurement on the Note's own setup that does show it), 1021 (deep-narrow vs wide-shallow at equal parameter budgets: a tie on MNIST). Each is described under its Note.
- **Text errors found by the figures and fixed:** 1049 (cat and dog counts added up to 23,412, not 23,410: `Thumbs.db` files), 1038 (Adam "swings around once"; it swings several times), 1042 (a stale figure reference in Sources), 02 (a grammar slip), 01-course-map ("Figure 8" for what is Figure 21).
- **New Key terms for glossary.md** (I did not run `merge_glossary.py` or edit `glossary.md`): Parameter, Gradient descent, Label, Test set, Accuracy (01-what-is-ml); Label propagation (03-types-of-ml, no ID yet); Parameter (05-online-learning); Logistic regression, Loss function, Gradient descent (06-instance-vs-model-based); Logistic regression (08-applications-of-ml); Epoch (1002-what-is-deep-learning). All except Label propagation already have IDs.
- **New datasets added to Notes' data/ folders (all under 1 MB):** UCI SMS Spam Collection (01), ELEC2 electricity market (04, 05), Kaggle Titanic train (07, copied from Note 32), German credit (08), the ascent photo (1043, copied from 1042), photo sizes and one batch from PetImages (1049).
- **Process notes.** I did not start any background agents. Two long runs (the 1050 experiment and a wait loop) ran as background shell commands. No git commands were used. Outside my Notes I changed only the template text in `course_map/build_map.py` (`course_map_note()`), as the task allows.

### Metrics, all 43 Notes

| Note | wpv before | wpv after | figure share before | after |
|---|---|---|---|---|
| 01-course-map | 572 | 553 | 3/5 | 4/5 |
| 01-what-is-ml | 432 | 352 | 4/6 | 6/6 |
| 02-ai-vs-ml-vs-dl | 191 | 191 | 5/6 | 5/6 |
| 03-types-of-ml | 152 | 151 | 5/5 | 5/5 |
| 04-batch-learning | 194 | 201 | 4/5 | 4/5 |
| 05-online-learning | 278 | 212 | 4/8 | 7/8 |
| 06-instance-vs-model-based | 259 | 214 | 3/5 | 4/5 |
| 07-challenges-in-ml | 188 | 181 | 8/10 | 8/10 |
| 08-applications-of-ml | 358 | 334 | 6/7 | 6/7 |
| 100-dtreeviz | 264 | 246 | 5/7 | 5/7 |
| 105-bagging-intuition | 481 | 336 | 3/6 | 5/6 |
| 1001-dl-scope-and-prerequisites | 330 | 330 | 3/3 | 3/3 |
| 1002-what-is-deep-learning | 518 | 403 | 5/5 | 5/5 |
| 1004-perceptron | 440 | 326 | 4/7 | 6/7 |
| 1007-problem-with-perceptron | 293 | 254 | 3/5 | 4/5 |
| 1008-mlp-notation | 205 | 205 | 5/5 | 5/5 |
| 1009-mlp-intuition | 421 | 327 | 3/5 | 4/5 |
| 1011-customer-churn-ann | 599 | 435 | 4/8 | 6/8 |
| 1013-graduate-admission-ann | 431 | 286 | 3/6 | 4/6 |
| 1019-mlp-memoization | 496 | 404 | 3/5 | 4/5 |
| 1021-improving-a-neural-network | 581 | 391 | 3/3 | 3/3 |
| 1022-early-stopping | 451 | 358 | 3/4 | 4/4 |
| 1024-dropout | 502 | 414 | 3/5 | 4/5 |
| 1025-dropout-code | 360 | 360 | 4/6 | 4/6 |
| 1027-activation-functions | 584 | 421 | 4/7 | 6/7 |
| 1028-relu-variants | 471 | 402 | 3/5 | 3/5 |
| 1029-weight-initialization | 419 | 362 | 4/6 | 5/6 |
| 1030-xavier-he-initialization | 576 | 372 | 3/5 | 5/5 |
| 1031-batch-normalization | 434 | 384 | 5/6 | 6/6 |
| 1032-optimizers-in-deep-learning | 306 | 306 | 5/5 | 5/5 |
| 1033-exponentially-weighted-moving-average | 283 | 247 | 4/6 | 5/6 |
| 1034-sgd-with-momentum | 350 | 279 | 5/8 | 7/8 |
| 1035-nesterov-accelerated-gradient | 276 | 276 | 5/8 | 5/8 |
| 1036-adagrad | 341 | 341 | 5/8 | 5/8 |
| 1037-rmsprop | 316 | 316 | 4/6 | 4/6 |
| 1038-adam | 366 | 307 | 4/8 | 5/8 |
| 1040-cnn-intuition | 313 | 270 | 3/5 | 3/5 |
| 1041-cnn-vs-visual-cortex | 502 | 392 | 3/5 | 4/5 |
| 1042-convolution-operation | 395 | 296 | 5/9 | 7/9 |
| 1043-padding-and-strides | 456 | 291 | 3/5 | 5/5 |
| 1049-cat-vs-dog-cnn | 437 | 304 | 4/8 | 6/8 |
| 1050-data-augmentation | 426 | 344 | 3/5 | 4/5 |
| 1052-visualizing-cnn | 422 | 359 | 5/7 | 6/7 |

## 01-course-map
- **Visual added:** `images/learning_path.py` -> `learning_path.gif` (Plotly frames to GIF; the PDF shows the final frame). It grows the reading order for the perceptron Note (1004) backwards: round 1 adds Notes 71, 363 and 520, round 2 adds the Notes those build on. The data comes from `concepts.yaml` through `build_map.neighbours()`, read only, with the same "last four earlier Notes" rule as the Learning path table. The script asserts round 1 and the layer sizes.
- **Ladder changes (section 4):** plain idea (read the ideas a Note uses first), the term **prerequisite**, the figure, then the mechanism as four numbered steps on Note 1004, then the exact rule behind each table row (which Link types count, and the four-Note cap).
- **Text fixed:**
  - Changed only in the template, `course_map_note()` in `course_map/build_map.py`, then regenerated with that one function (not the whole script, so no other Note's block was rewritten).
  - The note.md on disk had a hand edit (the MLDLC list, G-1240) that the template did not have; I moved it into the template so regeneration keeps it.
  - "Figure 8" for the Algorithm chooser was wrong (it is Figure 21 now); the template now computes the number.
  - Regeneration deletes stale `concept_map_models_1/2` copies in `images/`; I put them back to leave nothing else changed. They are not referenced and could be removed.
- **Metrics:** wpv 572 -> 553, figure share 3/5 -> 4/5. The words are almost all generated tables (step lists and the Learning path), so wpv cannot reach 400 without removing those tables.

## 01-what-is-ml
- **Visuals added:**
  - `images/spam_experience.py` -> `spam_experience.gif` (Plotly frames to GIF). Mitchell's T, E and P on real data: a Naive Bayes spam filter's accuracy on 1,000 held-out messages as it learns from 10 up to 4,574 labelled messages (UCI SMS Spam Collection, stored as `data/sms_spam.tsv.gz`, 202 KB; mean of 20 random training sets). 86.9 percent at 10 messages (the "always not spam" level is 86.6), 93.8 at 100, 98.1 at 4,574; all asserted.
  - `images/learn_addition.py` -> `learn_addition.gif` (Plotly frames to GIF). Training as a process: a model sum = w1 a + w2 b + c starts at (0.20, -0.30, 3.00) and gradient descent on 20 pairs (the table's two pairs plus 18 random ones) moves it to (1.00, 1.00, 0.04); the answer for 7 + 8 goes from 2.00 to 14.99. Asserted.
- **Ladder changes:**
  - Section 2 opened with "The formal definition". It now climbs: plain words, the standard definition with its terms and IDs, the measured picture as four numbered steps, then Mitchell's definition (moved out of the Extra into the body, as the formal version) mapped onto the figure's axes. The Samuel history stays in the Extra.
  - Section 3.3 gains the worked example of training, with the terms **parameter** (G-1448) and **gradient descent** (G-862).
- **Text fixed:** figure numbers after section 3 shifted by two. New terms in the body with IDs: label (G-1032), test set (G-1962), Naive Bayes (G-1298), accuracy (G-162). New source: Almeida et al. 2011 (the dataset).
- **New Key terms (for glossary.md):** Parameter, Gradient descent, Label, Test set, Accuracy. All already have glossary IDs.
- **Metrics:** wpv 432 -> 352, figure share 4/6 -> 6/6.

## 02-ai-vs-ml-vs-dl
- **Visuals added:** none. The Note was already strong (wpv 191, 5/6 sections with a figure; only the short "Choosing between ML and DL" section has none, and it points to Figure 8).
- **Experiment run, not used:** I tried to replace the Figure 8 sketch ("ML levels off, DL keeps improving; ML wins on small data") with a measurement: logistic regression vs a small CNN on MNIST, 50 to 60,000 training images (3 seeds below 10,000). The CNN won at every size (75.5 vs 63.8 percent at 50 images; 99.2 vs 92.6 at 60,000). On images the measurement does not show the small-data region where ML wins, so it would contradict the sketch's shading instead of illustrating it. Showing that region needs small tabular data (Grinsztajn et al. 2022 is the usual reference), which I did not have time to set up. The sketch stays, still labelled as a sketch.
- **Text fixed:** "rules work ... and fails" -> "and fail" (section 3 Key point).
- **Metrics:** unchanged, wpv 191, figure share 5/6.

## 03-types-of-ml
- **Visual added:** `images/label_spreading.py` -> `label_spreading.gif` (Plotly frames to GIF; the PDF shows the start and step 2). Semi-supervised learning as a process: one student per group is labelled by hand and the labels hop along a 5-nearest-neighbour graph of the Note's own 90 example students (the clustering figure's data). 3 -> 24 -> 68 -> 89 -> 90 labelled after 4 steps, every one correct; asserted.
- **Ladder changes (section 4):** after the Google Photos picture, a bridging question ("How does one label reach a whole group?"), the term **nearest neighbours** (G-1306), the animation, the mechanism in four numbered steps with the counts, then the method's name, **label propagation** (Zhu and Ghahramani 2002, opened), and the condition it needs.
- **Text fixed:** later figure numbers shifted by one.
- **New Key term (for glossary.md):** Label propagation (no glossary ID yet).
- **Not changed, but worth knowing:** `clustering.py` and a few other older scripts in this Note draw with seaborn (matplotlib), which the house rules forbid. They were outside this round's scope, so I left them.
- **Metrics:** wpv 152 -> 151, figure share 5/5 -> 5/5.

## 04-batch-learning
- **Visual added:** `images/stale_measured.py` -> `stale_measured.gif` (Plotly frames to GIF; the PDF shows the final frame). A batch model going stale, measured instead of sketched: logistic regression on the Electricity (ELEC2) market data, 45,312 half-hour records, 1996 to 1998 (`data/elec2.csv.gz`, 517 KB). One copy trained on the first 4 weeks and never retrained, one retrained from scratch every 4 weeks; weekly accuracy, 8-week average, drawn over time. Frozen 68.0 percent vs retrained 73.3 percent on average; the script asserts that accuracy rises with retraining frequency (never 68.0 < 13 weeks 72.4 < 4 weeks 73.3 < weekly 73.7).
- **Ladder changes:** section 4.1 now goes from the plain sketch (Figure 3, kept and still labelled as a sketch) to the measured picture, with the mechanism in five numbered steps. Section 4.2 gains a small table of accuracy by retraining schedule and one sentence on the trade-off it shows (accuracy against training cost).
- **Text fixed:** later figure numbers shifted by one. **Logistic regression** (G-1120) gets its ID at first use. New source: Harries 1999, via OpenML dataset 151 (description opened).
- **Metrics:** wpv 194 -> 201 (the new worked example adds words), figure share 4/5 -> 4/5. Only the Overview has no figure.

## 05-online-learning
- **Visuals added:**
  - `images/elec_online.py` -> `elec_online.gif` (Plotly frames to GIF). Online vs frozen batch on the Electricity market data (copied to `data/elec2.csv.gz`): scikit-learn's default `SGDClassifier` (log loss) predicts each day, then learns from it with `partial_fit`. 71.7 percent vs 68.0 over 130 weeks; asserted.
  - the same script -> `elec_cost.png` (Plotly). The batch vs online trade-off as two bar charts: accuracy (68.0, 73.3, 71.7) and records fed to training (1,344; 754 thousand; 72 thousand). Asserted.
  - `images/partial_fit_stream.py` -> `partial_fit_stream.gif` (Plotly frames to GIF). What each `partial_fit` call does: an `SGDRegressor` line moving from y = 0.67x + 0.25 after call 1 to y = 1.81x + 0.51 after call 50, on the Notebook's own stream (true y = 2x). Asserted.
- **Ladder changes:** section 3's first reason now has a measured example with four numbered steps. Section 4.1 shows what the code does, step by step, and names the **parameters** (G-1448) that each call moves. Section 8's comparison table is followed by the measured trade-off as a picture and three bullets.
- **Text fixed:** later figure numbers shifted. New source: Harries 1999 / OpenML 151.
- **New Key term (for glossary.md):** Parameter (already G-1448).
- **Metrics:** wpv 278 -> 211, figure share 4/8 -> 7/8.

## 06-instance-vs-model-based
- **Visuals added:**
  - `images/model_training.py` -> `model_training.gif` (Plotly frames to GIF; PDF: start and final frames). Model-based learning as a process: logistic regression finds its decision boundary on the Note's 60 placement students by gradient descent (same loss and penalty as scikit-learn's default, asserted equal to it), then the training points disappear and only w1 = 1.36, w2 = 2.72, b = -0.53 remain to classify the new student (placed, probability 0.57).
  - `images/cost_compare.py` -> `cost_compare.png` (Plotly). The comparison table's storage and prediction rows, measured: numbers kept (3n for KNN, 3 for logistic regression; asserted) and time to answer 10,000 new students, for 1,000 to 1,000,000 training students from the Note's own data generator.
- **Ladder changes:** section 4.1 now has a bridging question ("How does the algorithm find that line?"), the terms **logistic regression** (G-1120), **loss function** (G-1130) and **gradient descent** (G-862), and the mechanism in four numbered steps with the measured losses. Section 5's table is followed by the measured picture and two bullets.
- **Text fixed:** later figure numbers shifted by one.
- **New Key terms (for glossary.md):** Logistic regression, Loss function, Gradient descent (all have IDs).
- **Metrics:** wpv 259 -> 216, figure share 3/5 -> 4/5.

## 07-challenges-in-ml
- **Visual added:** `images/sampling_survey.py` -> `sampling_survey.gif` (Plotly frames to GIF; the PDF shows the final frame). Sampling noise vs sampling bias on real data: 40 surveys at each size (5 to 200 passengers) estimate the Titanic survival share (true 38.4 percent, `data/titanic_train.csv` copied from Note 32). Random surveys range from 0 to 100 percent at size 5 and gather around 38 at size 200; first-class-only surveys gather around 63 percent at any size. Asserted.
- **Ladder changes (section 4.2):** after the plain survey example and its terms, the measured picture with three numbered steps (noise, more data, bias). The existing closing sentence ("a large sample does not protect against bias") now follows the evidence.
- **Text fixed:** later figure numbers shifted by one. New source: the Kaggle Titanic training set.
- **Not done:** Figure 2 (the unreasonable effectiveness of data) remains an illustration, as its caption says.
- **Metrics:** wpv 188 -> 181, figure share 8/10 -> 8/10 (the figure joins a section that had one).

## 08-applications-of-ml
- **Visual added:** `images/loan_threshold.py` -> `loan_threshold.gif` (Plotly frames to GIF; the PDF shows the cut-off 50 frame). The ML stage of loan screening on real loans: German credit data (1,000 borrowers, 300 did not repay; `data/credit_g.csv`, 136 KB). A logistic regression trained on 700 scores the other 300; the cut-off slides from 90 to 20 and the title counts who is rejected. Cut-off 80 rejects 9 defaulters and 3 good customers; 50 rejects 38 and 20; 20 rejects 72 and 82. Asserted.
- **Ladder changes (section 4.1):** after the plain two-stage description, a bridging question ("Where should the bank draw the line?"), the figure, and five numbered steps from training to the trade-off, with the dataset's own cost matrix as the reason the cut-off is a business decision.
- **Text fixed:** later figure numbers shifted by one. New source: Hofmann 1994 (OpenML 31 description and cost matrix opened).
- **New Key term (for glossary.md):** Logistic regression (G-1120).
- **Metrics:** wpv 358 -> 334, figure share 6/7 -> 6/7 (only the short B2C/B2B section has no figure; nothing there is worth a picture).

## 100-dtreeviz
- **Visual added:** `images/path_region.py` -> `path_region.gif` (Plotly frames to GIF; PDF: the frames after questions 1 and 3). The prediction path of section 6.2 as a region of the petal plane that shrinks with each question, with the training flowers still on the path counted: 150 -> 100 -> 46 -> 3 -> 1. Uses the Note's fully grown tree (`random_state=0`); the path, thresholds and counts are asserted.
- **Ladder changes (section 6.2):** after the numbered path, the same path as cuts on the data, in five steps. The figure exposed a fact the text did not state: after three questions the 3 remaining flowers sit at exactly the same petal point (4.8, 1.8), one versicolor and two virginica, which is why the tree must ask about sepal width. The text now says so.
- **Text fixed:** later figure numbers (and the Summary table's figure references) shifted by one.
- **Metrics:** wpv 264 -> 246, figure share 5/7 -> 5/7 (the two sections without a figure are the install/call code and the top of section 6, whose subsections carry figures).

## 105-bagging-intuition
- **Visuals added:**
  - `images/unstable.py` -> `unstable.png` (Plotly). "When to use bagging", measured on the Note's own Figure 3 setup (20 sine training sets, same seed): bagging cuts a fully grown tree's variance by 52 percent (0.160 -> 0.076) but a 5-nearest-neighbour model's by only 24 percent (0.034 -> 0.025). Asserted. A first design (decision regions of a tree vs KNN over bootstrap samples on the iris subset) did not show the tree as clearly less stable than KNN on that data, so I dropped it rather than pick a lucky setup.
  - `images/hand_vote.py` -> `hand_vote.gif` (Plotly frames to GIF; PDF: the final frame). Bagging by hand, drawn: the Notebook's exact 10 flowers and three bootstrap samples (repeats shown as bigger dots, undrawn rows hollow), each tree's cut (5.20, 4.90, 4.95) and the votes 1, 2, 2. Asserted.
- **Ladder changes:** section 4 now follows the plain claim ("bagging helps unstable models") with the measurement, the term **k-nearest neighbours** (G-998), and two bullets that explain the gap (KNN already averages 5 points). Section 5.3 points to the drawn example.
- **Text fixed:** the types figure is now Figure 6.
- **Metrics:** wpv 481 -> 336, figure share 3/6 -> 5/6.

## 1001-dl-scope-and-prerequisites
- **No change.** Already strong (wpv 330, 3/3 sections with a figure). Its remaining ideas (a layer as a matrix product, training by derivatives) are previews whose owner Notes (500, 600, 57) already animate them; a new picture here would duplicate them, against the one-owner rule. I spent the time on weaker Notes instead.

## 1002-what-is-deep-learning
- **Visuals added:**
  - `images/hidden_rep.py` -> `hidden_rep.gif` (Plotly frames to GIF; PDF: raw pixels next to the hidden layer after 10 epochs). Representation learning, watched: an MLP (784-64-32-10) learns MNIST on CPU (seeded); the 432 test 3s, 5s and 8s are shown as raw pixels and as the last hidden layer after 0, 1, 2, 5 and 10 epochs, each squeezed to 2D by PCA. The share of digits whose 2D nearest neighbour is the same digit: pixels 56, then 48, 64, 69, 78, 87 percent; test accuracy 96.9 percent. Asserted. The training run is `experiments/hidden_rep.py` (writes `data/hidden_rep.npz`, 69 KB), so the build only plots. Ten digits at once did not separate in a 2D PCA view, so the figure uses three easily confused digits.
  - `images/cpu_vs_gpu.py` -> `cpu_vs_gpu.png` (Plotly). Section 4.2's hardware claim, measured on topgro: TensorFlow matrix multiplication, n = 256 to 8192, CPU (i9-13900HK) vs GPU (RTX 4060 Laptop). The GPU is 2.7 times faster at 256 and 12.5 times at 8192. From `experiments/cpu_vs_gpu.py` (writes `data/cpu_vs_gpu.json`). A first try, one epoch of a small CNN, gave only 1.6 times because feeding the data, not the maths, limited it; it did not test the claim, so I measured the operation the text names.
- **Ladder changes:** section 2.4 goes from the plain three-layer story to the measured picture, five numbered steps with the term **epoch** (G-696), and one closing sentence on what "learned representation" means. Section 4.2 gets the measured picture and two bullets.
- **Text fixed:** later figure numbers shifted. New source: LeCun et al. 1998 (MNIST).
- **New Key term (for glossary.md):** Epoch (G-696).
- **Metrics:** wpv 518 -> 403, figure share 5/5 -> 5/5.

## 1004-perceptron
- **Visuals added:**
  - `images/weight_turn.py` -> `weight_turn.gif` (Plotly frames to GIF; PDF: w2 = 0, 1.48 and 5.82). Weights as feature importance: the trained perceptron of section 8 (standardized; w1 = 5.82, b = 1 fixed) with the resume-score weight swept from 0 to 8; the line z = 0 turns from vertical to diagonal and training accuracy goes 97 (w2 = 0), 97 (1.48, trained), 81 (5.82). Asserted.
  - `images/z_plane.py` -> `z_plane.gif` (Plotly 3D frames to GIF). The geometry of section 7: z as a tilted plane over the 100 students, its zero line (the decision boundary), and the step function turning it into two terraces.
- **Ladder changes:** section 6 now follows the plain claim (bigger weight, more say) with the picture and three numbered cases, ending in the mechanism (the line turns towards the heavier input). Section 7 now shows where the line z = 0 comes from, in three steps, before the formal statement about decision regions and hyperplanes.
- **Text fixed:** the scikit-learn figure is now Figure 6. The sweep also shows that w2 = 0 already gives 97 percent: the resume score adds almost nothing on this data, which the new text states.
- **Metrics:** wpv 440 -> 326, figure share 4/7 -> 6/7.

## 1007-problem-with-perceptron
- **Visual added:** `images/xor_remap.py` -> `xor_remap.gif` (Plotly frames to GIF; PDF: input space and hidden space). Why a hidden layer solves XOR: the two hidden perceptrons of section 6 (the OR and AND lines) slide the four corners to (h1, h2), where (0,1) and (1,0) land on the same spot and one line, h1 - h2 = 0.5, separates the classes. The script asserts the hidden values and that the output is XOR.
- **Ladder changes (section 6):** after the existing two-line idea, the picture and four numbered steps, then the term **representation learning** (G-1670) as the formal name for what the hidden layer did.
- **Metrics:** wpv 293 -> 254, figure share 3/5 -> 4/5.

## 1008-mlp-notation
- **No change.** Already strong (wpv 205, 5/5 sections with a figure). The Note is about still structure (names and counts), which its five TikZ diagrams already draw; it has no process to animate.

## 1009-mlp-intuition
- **Visuals added:**
  - `images/sigmoid_map.py` -> `sigmoid_map.png` (Plotly). Section 2's probability map of one sigmoid perceptron (the first perceptron of the combination figure), with contours every 0.1 and the 0.5 hyperplane.
  - `images/xor_training.py` -> `xor_training.gif` (Plotly frames to GIF; PDF: steps 1,000, 1,650 and 5,000). Section 5.1's training, replayed with exactly the Notebook's `TwoNodeNet` (same seed, asserted equal at the end). It reveals a long plateau: the log loss sits at 0.693 until about step 1,500, then falls to 0.178 by step 1,750 (accuracy 54 -> 74 -> 92 -> 100 percent) and to 0.003 by step 5,000. Asserted.
- **Ladder changes:** section 2 now has its picture, three bullets reading it, and one sentence on why the contours are parallel. Section 5.1 gains the training replay in three numbered stages; the plateau is explained from the update formula itself (each hidden update is multiplied by the output weights, which start near 0.01).
- **Text fixed:** all figure numbers shifted (the new map is Figure 1, the replay Figure 6).
- **Metrics:** wpv 421 -> 327, figure share 3/5 -> 4/5.

## 1011-customer-churn-ann
- **Visuals added:**
  - `images/scales.py` -> `scales.png` (Plotly). Why we standardize: box plots of the 11 features of the 8,000 training customers, raw (Balance reaches 250,899; nine features squashed against zero) and after `StandardScaler`.
  - `images/prob_epochs.py` -> `prob_epochs.gif` (Plotly frames to GIF; PDF: after epoch 10). The first network's predicted probability of leaving for all 2,000 test customers, before training and after each epoch, split by what really happened. From `experiments/prob_epochs.py` (CPU, the Notebook's seed and steps; it reproduces the Note's losses and the 0.069 to 0.498 range exactly, asserted). Before training 1,965 customers sit above 0.5; the average then falls to 0.21 (near the share of leavers), the spread opens, and after epoch 10 nobody crosses 0.5.
- **Ladder changes:** section 3.2 gets the picture and two bullets. Section 5.2 now asks "what does the falling loss change?" and answers it in four numbered steps that lead straight into section 6.2's "predicts stays for everyone". The base-rate step is explained by a maths fact (a constant prediction has the lowest log loss at the class share), not by a guess.
- **Not used:** I also retrained the second network; it scored 86.50 percent instead of the Note's 86.45 (one test customer), so I did not put it in a figure that would disagree with the Note.
- **Text fixed:** figure numbers shifted.
- **Metrics:** wpv 599 -> 435, figure share 4/8 -> 6/8.

## 1013-graduate-admission-ann
- **Visuals added:**
  - `images/scales.py` -> `scales.png` (Plotly). Min-max scaling: the 7 features of the 400 training students raw (GRE 290 to 340, TOEFL 92 to 120, the rest below 10) and after `MinMaxScaler` (all 0 to 1). Asserted.
  - `images/pred_epochs.py` -> `pred_epochs.gif` (Plotly frames to GIF; PDF: epochs 5, 20, 100). The second network's predicted vs actual chance for the 100 test students after 0 to 100 epochs, with the test R² of each: -6.13, -3.27, -1.58, -1.00, -0.94, -0.34, 0.23, 0.73, 0.80. From `experiments/pred_epochs.py` (CPU, the Notebook's seed and order; it reproduces both of the Note's R² values exactly, -0.0552 and 0.8004).
- **Ladder changes:** section 3 now goes plain idea -> picture -> the min-max formula -> a worked example (GRE 316 -> 0.52). Section 6 shows R² rising through 0 in five numbered steps, with the "always predict the average" line drawn as the R² = 0 reference.
- **Text fixed:** figure numbers shifted (the churn Note's "Figure 1" reference left alone).
- **Metrics:** wpv 431 -> 286, figure share 3/6 -> 4/6.

## 1019-mlp-memoization
- **Visual added:** `images/backward_memo.py` -> `backward_memo.gif` (Plotly frames to GIF; PDF: the final frame). The memoized backward pass on the Note's own 3-3-2-1 network (the Notebook's weights and observation): each node turns orange as its dL/dO is computed once and stored (-2.387; 0.874, 0.650; -0.163, -0.120, -0.089), the links used in each step are highlighted, and the last frame reads dL/dW^1_11 = -0.0138 off the stored value. Asserted against the Note's numbers.
- **Ladder changes (section 5.2):** the plain rule and formula are now followed by the worked backward pass in four numbered steps, showing where the two paths of section 4.4 are added (once, inside dL/dO11).
- **Metrics:** wpv 496 -> 404, figure share 3/5 -> 4/5.

## 1021-improving-a-neural-network
- **Visuals added:**
  - `images/shapes.py` -> `shapes.png` (Plotly). Section 3.2's two claims measured on MNIST (3 seeds, 10 epochs): a 64-32-16 pyramid and three equal layers of 58 at the same parameter count both score 97.2 percent; a first hidden layer of 1, 2 or 32 neurons (then 32-32) scores 42.8, 70.6 and 96.3 percent. From `experiments/shapes.py` (writes `data/shapes.json`).
  - `images/batch_size.py` -> `batch_size.png` (Plotly). Section 3.4's table measured: seconds per epoch (5.9 at batch 8, about 0.4 from 512 up) and test accuracy after 10 epochs (about 96 percent for 8 to 512, 94.2 at 2,048, 89.6 at 8,192). From `experiments/batch_size.py`. The text names the counting part of the drop (80 updates in 10 epochs at 8,192 against 75,000 at 8).
- **Experiment run, not used (section 3.1, deep and narrow vs one wide layer):** with unequal sizes, one layer of 512 (407,050 weights) beat 32-32-32 (27,562). At equal parameter budgets the two tie on MNIST (35 units: 96.4 percent vs 32-32-32: 96.3; 66 units: 97.3 vs 64-32-16: 97.2). So MNIST with an MLP cannot illustrate the depth claim; I left section 3.1's text (sourced to Goodfellow et al. §6.4.1) and added no figure there. A compositional task would be needed to show it.
- **Ladder changes:** sections 3.2 and 3.4 now follow their rules of thumb with measured pictures and bullets that read them.
- **Text fixed:** the fix-list figure is now Figure 5.
- **Metrics:** wpv 581 -> 391, figure share 3/3 -> 3/3.

## 1022-early-stopping
- **Visual added:** `images/patience.py` -> `patience.png` (Plotly). Section 5.2's patience example drawn from the Note's own 3,500-epoch history: Keras' rule (min_delta 0.00001) replayed in the script gives stop epochs 21 for patience 20 and 503 for patience 50, both asserted against the Note.
- **Ladder changes (section 5.2):** the picture plus one paragraph with the mechanism the text lacked: at epoch 21 the best loss so far is still epoch 1's (0.6892), because the early bump is not beaten until epoch 25, so patience 20 runs out just as learning starts.
- **Metrics:** wpv 451 -> 358, figure share 3/4 -> 4/4.

## 1024-dropout
- **Visual added:** `images/subnet_average.py` -> `subnet_average.gif` (Plotly frames to GIF; PDF: the final frame). The ensemble view of section 5.3, measured: a 2-128-128-1 network with p = 0.5, trained on make_moons (CPU, seeded; `experiments/subnet_average.py`, data 405 KB). Grey lines are single sub-networks (one fixed mask per hidden layer, applied to the trained weights); green is their average; dashed is the full network. With 20 or more sub-networks the average agrees with the full network on 99.8 percent of the plane. The script checks that the hand-computed full network equals Keras `predict()`.
  - A first version used `model(x, training=True)` on the grid; that draws a new mask for every grid point, so it is not one sub-network. I replaced it with explicit masks.
- **Ladder changes (section 5.3):** after the counting argument (2^n sub-networks), the measured picture and three bullets, ending with a pointer to section 6 for the scaling.
- **Text fixed:** the train-vs-predict figure is now Figure 4.
- **Metrics:** wpv 502 -> 414, figure share 3/5 -> 4/5.

## 1025-dropout-code
- **No change.** Already strong (wpv 360, 4/6 sections with a figure, including an animated dropout-rate sweep). The two sections without a figure are short lists of tips and drawbacks; I spent the time on weaker Notes.

## 1027-activation-functions
- **Visuals added:**
  - `images/zigzag.py` -> `zigzag.gif` (Plotly frames to GIF; PDF: the final frame). Section 5.4's claim as a worked illustration: one linear node, two weights, stochastic gradient descent towards w = (1, -1), with all-positive inputs (like sigmoid outputs) vs the same inputs centred on 0 (like tanh). With positive inputs every step moves both weights the same way (asserted for all steps) and the path zig-zags across a narrow valley; after 20 steps it is 1.01 from the target against 0.10 for centred inputs (asserted). At a small learning rate (0.5) the two ended equally close; the difference appears because positive inputs make the valley narrow and limit the usable step size, which is LeCun et al.'s §4.3 argument. The figure says it is an illustration, not the Note's data.
  - `images/layer_outputs.py` -> `layer_outputs.png` (Plotly). The Notebook's zero-centred check drawn: histograms of a fresh 128-node layer's outputs on the 300 circles observations for sigmoid (mean 0.50, all positive), tanh (mean 0.00, half positive) and ReLU (never negative). Asserted.
- **Ladder changes:** section 5.4 now goes from the plain property to the picture and three numbered steps with the gradient formula; section 7.2's zero-centred advantage gets its picture and a reading of it.
- **Text fixed:** later figure numbers shifted.
- **Metrics:** wpv 584 -> 421, figure share 4/7 -> 6/7.

## 1028-relu-variants
- **Visual added:** `images/dead_over_time.py` -> `dead_over_time.gif` (Plotly frames to GIF; PDF: the final frame). The dead-node shares of Figure 3 followed through training, on a log time axis: learning rate 10 kills 41 percent of the first layer within 8 of the first 16 batches and nothing changes after; ReLU with bias -1 is flat at 72 and 100 percent; Leaky ReLU and ELU with the same bias recover (Leaky's second layer from 100 to 38 percent by epoch 27). From `experiments/dead_over_time.py` (CPU, the Notebook's exact runs; all final shares equal the Note's table, asserted).
- **Ladder changes (section 3.4):** the static end-of-training bars are now followed by the process in four numbered steps.
- **Text fixed:** the SELU figure is now Figure 5.
- **Metrics:** wpv 471 -> 402, figure share 3/5 -> 3/5 (the figure joins section 3; sections 4 and 5 are short and use Figure 1's curves).

## 1029-weight-initialization
- **Visual added:** `images/twins.py` -> `twins.gif` (Plotly frames to GIF; PDF: the final frame). Section 5's symmetry followed through training: the weights from x1 into the 3 ReLU hidden nodes over 100 epochs, started at 0.5 (one line, ending at 0.312 for all three) vs Keras' random start (three lines ending at -2.27, -0.13, 0.19). From `experiments/twins.py` (CPU, the Notebook's exact run; it reproduces the table's 0.312 and -0.842, asserted).
- **Ladder changes (section 5):** the table is now followed by the process picture and two bullets that give the mechanism (identical gradients at every step).
- **Text fixed:** later figure numbers shifted.
- **Metrics:** wpv 419 -> 362, figure share 4/6 -> 5/6.

## 1030-xavier-he-initialization
- **Visuals added:**
  - `images/xavier_shapes.py` -> `xavier_shapes.png` (Plotly). Section 4.2: the 62,500 starting weights of a 250 x 250 layer under Xavier normal (sigma 0.063) and Xavier uniform (from -0.110 to 0.110); both have variance 0.0040. Asserted.
  - `images/relu_half.py` -> `relu_half.png` (Plotly). Section 5.1's "why the 2": 100,000 symmetric weighted sums (mean square 1.00) and the same values after ReLU (half are 0, mean square 0.50). Asserted.
- **Ladder changes:** section 4.2 gets its picture and a reading of it. Section 5.1 now explains the factor 2 in plain bullets with the picture before the existing formal Extra, instead of only inside the Extra.
- **Text fixed:** the decision-region figure is now Figure 5.
- **Metrics:** wpv 576 -> 372, figure share 3/5 -> 5/5.

## 1031-batch-normalization
- **Visual added:** `images/lr_range.py` -> `lr_range.png` (Plotly). Section 6's first two advantages measured on the Note's circles networks: plain SGD at learning rates 0.01 to 3, 100 epochs, 5 seeds each. Without batch normalisation the best mean is 0.80 (at 0.3); with it the mean stays above 0.9 from 0.03 to 1.0; both degrade at 3. From `experiments/lr_range.py` (writes `data/lr_range.json`).
- **Ladder changes (section 6):** the list of advantages is now followed by the measurement and three bullets, including the limit (batch normalisation widens the safe range but does not remove it).
- **Text fixed:** the Keras comparison figure is now Figure 7.
- **Metrics:** wpv 434 -> 384, figure share 5/6 -> 6/6.

## 1032-optimizers-in-deep-learning
- **No change.** Already strong (wpv 306, 5/5 sections with a figure). It is the map for the optimizer Notes that follow, each of which animates its own optimizer.

## 1033-exponentially-weighted-moving-average
- **Visual added:** `images/ewma_steps.py` -> `ewma_steps.gif` (Plotly frames to GIF; PDF: day 21). The EWMA update, day by day, on Delhi's first 21 days of 2013: each frame shows the gap between yesterday's average and today's temperature and the one-tenth move (beta = 0.9, V0 = theta1). The script asserts its values equal pandas' `ewm(alpha=0.1, adjust=False)` and the Note's 10.00, 9.74, 9.48, 9.40, 9.06.
- **Ladder changes (section 3):** the two plain rules now have their picture and three numbered steps, then one paragraph tying each rule to the picture, before the formula of section 4.
- **Text fixed:** later figure numbers shifted.
- **Metrics:** wpv 283 -> 247, figure share 4/6 -> 5/6.

## 1034-sgd-with-momentum
- **Visuals added:**
  - `images/loss_views.py` -> `loss_views.png` (Plotly). Section 3's three ways to draw a loss, on the Note's own functions: L = w²/2 as a curve, the narrow valley of Figure 1 as a 3D surface, and its contour plot.
  - `images/obstacles.py` -> `obstacles.png` (Plotly). Section 4's three obstacles with plain gradient descent: the Note's dip curve (stops at w = -1.83, asserted), a saddle (step length falls from 0.30 to 0.008 near the centre, asserted) and the valley at learning rate 0.019 (zigzag).
- **Ladder changes:** sections 3 and 4 now each have their picture; section 3 adds one sentence on reading the stretched axis, section 4 three bullets with the measured numbers.
- **Text fixed:** later figure numbers shifted (the Goh 2017 citation's figure reference updated with them).
- **Metrics:** wpv 350 -> 279, figure share 5/8 -> 7/8.

## 1035-nesterov-accelerated-gradient
- **No change.** Already strong (wpv 276, 5/8 sections with a figure, two animations). The sections without their own figure (momentum's oscillation, NAG's weakness, Keras code) are each shown by figures in neighbouring sections.

## 1036-adagrad
- **No change.** Already strong (wpv 341, 5/8 sections with a figure, two animations).

## 1037-rmsprop
- **No change.** Already strong (wpv 316, 4/6 sections with a figure, two animations).

## 1038-adam
- **Visual added:** `images/loss_gap.py` -> `loss_gap.png` (Plotly). Section 6's table drawn: the loss above its minimum, step by step, for the five runs of Figure 1 (the Note's `shared.py` runs; the first-crossing step counts 61, 64, 44, 48, 42 are asserted).
- **Text fixed:** the picture showed that the table's "steps" are the first time a run gets within 0.01, and that Adam and momentum then swing back above the line several times before settling (Adam reaches 0.2 again around step 52). The text said Adam "swings around once"; it now says "a few times, each swing smaller", and a new paragraph explains what the step counts mean and that RMSProp jumps back up near step 105.
- **Ladder changes (section 6):** table, then picture, then the reading of it, then the existing interpretation.
- **Text fixed:** the MNIST figure is now Figure 5.
- **Metrics:** wpv 366 -> 307, figure share 4/8 -> 5/8.

## 1040-cnn-intuition
- **Visual added:** `images/weights_growth.py` -> `weights_growth.png` (Plotly). Section 4.2's weight count drawn: first-layer weights and biases for a Dense layer of 100 nodes as a greyscale image grows from 28 x 28 to 1000 x 1000 (78,500 to 100,000,100), against a convolution layer of 32 filters of 3 x 3 (always 320). The formulas are checked against Keras' `count_params()`.
- **Ladder changes (section 4.2):** the worked formula is now followed by the picture and one paragraph that names the mechanism (a filter is reused at every position) with a link to the Note that teaches it.
- **Text fixed:** later figure numbers shifted.
- **Metrics:** wpv 313 -> 270, figure share 3/5 -> 3/5.

## 1041-cnn-vs-visual-cortex
- **Visual added:** `images/hubel_wiesel.py` -> `hubel_wiesel.gif` (Plotly frames to GIF; PDF: the 90° frame). The Hubel and Wiesel experiment replayed with the Note's model simple cell: a bar rotates on a 41 x 41 screen while the cell's response is traced (0 near horizontal, 1 around vertical). The responses are recomputed from the Notebook's filter and checked against `data/tuning.csv`.
- **Ladder changes (section 4.2):** the plain description of the recordings now has its picture and four numbered stages with the model's numbers, before the generalisation to other orientations; section 5.3 then gives the formal model.
- **Text fixed:** the cell-model figure is now Figure 4.
- **Metrics:** wpv 502 -> 392, figure share 3/5 -> 4/5.

## 1042-convolution-operation
- **Visuals added:**
  - `images/rgb_channels.py` -> `rgb_channels.png` (Plotly). Section 3.2: a colour photo (scikit-learn's `flower.jpg`, CC BY 2.0, credited in Sources) split into its red, green and blue channels, with the numbers of one 4 x 4 patch in each.
  - `images/fit_positions.py` -> `fit_positions.png` (Plotly). Section 6: the four starting columns of a 3 x 3 filter on a 6 x 6 image, and the fifth that does not fit: n - f + 1 drawn.
- **Ladder changes:** sections 3.2 and 6 now go plain idea -> picture -> a sentence reading it -> the existing formula and table.
- **Text fixed:** figure numbers shifted (the edges photo is now Figure 3, and its later reference was updated). New source: the sample photo.
- **Metrics:** wpv 395 -> 296, figure share 5/9 -> 7/9.
- Also fixed in 1042 afterwards: its Sources line for the ascent photo said "used for Figure 2"; it is Figure 3 after renumbering.

## 1043-padding-and-strides
- **Visuals added:**
  - `images/layer_sizes.py` -> `layer_sizes.png` (Plotly). Feature-map width after each of 13 stacked 3 x 3 convolution layers on a 28 x 28 input: `valid` loses 2 pixels per layer (28 ... 2), `same` keeps 28. Sizes from Keras, asserted.
  - `images/stride_photo.py` -> `stride_photo.png` (Plotly). Section 6's two reasons on a real photo (the ascent image, copied from Note 1042's data): one vertical-edge filter at strides 1, 2 and 3 (256, 128 and 86 pixels wide), the railings blurring as the stride grows, and the multiplications falling from 589,824 to 147,456 to 66,564. Computed with Keras `Conv2D`, asserted.
- **Ladder changes:** section 4 now shows the stacking effect before the formula; section 6's two reasons get their picture and a bullet each.
- **Text fixed:** the stride animation is now Figure 4. New source line for the photo.
- **Metrics:** wpv 456 -> 291, figure share 3/5 -> 5/5.

## 1049-cat-vs-dog-cnn
- **Visuals added** (both from `experiments/peek.py`, run on the full PetImages folder at `~/datasets/PetImages` on topgro; it writes `data/sizes.csv.gz`, 52 KB, and `data/batch.npz`, 524 KB):
  - `images/sizes.py` -> `sizes.png` (Plotly). Width against height for all 23,410 photos: 6,559 different sizes, the most common 500 x 375 (a quarter of the photos), none above 500 pixels; the 256 x 256 target marked. Asserted.
  - `images/batch.py` -> `batch.png` (Plotly). The first training batch exactly as the Note's `image_dataset_from_directory` call serves it (seed 1337): 32 resized photos with their folder labels (16 cats, 16 dogs).
- **Text fixed:** the Note said "23,410: 11,742 cats and 11,670 dogs", which adds up to 23,412. Each folder also holds a `Thumbs.db` file; the photos are 11,741 cats and 11,669 dogs. The text now gives both counts and the reason.
- **Ladder changes:** sections 3 and 4 now each show the data they describe, with a short reading (including that the square resize stretches non-square photos).
- **Text fixed:** later figure numbers shifted.
- **Metrics:** wpv 437 -> 304, figure share 4/8 -> 6/8.

## 1052-visualizing-cnn
- **Visual added:** `images/receptive_field.py` -> `receptive_field.gif` (Plotly frames to GIF; PDF: block 3, 4 and 5 ends). Section 8.2's receptive-field recursion drawn on the Note's kitten photo: a square centred on the left eye grows through VGG16's 13 convolution layers (3, 5, 10, ... 196 pixels). The script recomputes the Note's 40, 92 and 196 and asserts them.
- **Ladder changes (section 8.2):** after the formula and worked recursion, the picture and one paragraph saying what each block's square covers, tied to the patch sizes of section 8.3.
- **Metrics:** wpv 422 -> 359, figure share 5/7 -> 6/7.

## 1050-data-augmentation
- **Visuals added:**
  - `images/data_size.py` -> `data_size.png` (Plotly). Section 3.1's claim measured: the Note's section 6 network trained on 500, 1,000 and 2,000 cat-and-dog photos (taken from the Notebook's small subset), with and without its three random layers, 60 epochs, 4 seeds each, tested on the same 1,000 photos. Mean test accuracy without / with augmentation: 63.0 / 69.3, 67.6 / 76.3, 73.1 / 79.3 percent. Augmentation on 1,000 photos beats no augmentation on 2,000. From `experiments/data_size.py` (GPU; writes `data/data_size.json`). A first run with 2 seeds had one augmented run at 66 percent, so I reran everything with 4 seeds rather than drop it; the figure and text use the 4-seed run. The text says GPU runs do not repeat exactly, and that the 2,000-photo numbers differ slightly from section 6's separate runs.
  - `images/train_vs_infer.py` -> `train_vs_infer.png` (Plotly). Section 5.2: the section 6 augmentation pipeline called three times with `training=True` (three different images) and three times with `training=False` (the photo unchanged, asserted).
- **Ladder changes:** section 3.1 gains a bridging question ("How much more?"), the measurement and two bullets; section 5.2's statement now has its picture.
- **Text fixed:** later figure numbers shifted.
- **Metrics:** wpv 426 -> 303, figure share 3/5 -> 5/5.

## Noticed, not changed
- Leftover temporary frame folders from an earlier round (dated 2026-10-03 17:10, before this session): `1035-nesterov-accelerated-gradient/images/.nag_frames`, `1037-rmsprop/images/.race_frames`, `1038-adam/images/.race_frames`. Safe to delete.
- `03-types-of-ml/images/clustering.py` and some other older scripts draw with seaborn (matplotlib), against the house rule.
