# Claims audit, group 7

Folders: 622 and 1001 to 1026 (27 Notes). Every edited Note was rebuilt with `tools/build.sh` and printed "Built". Experiments ran on CPU in the `campusx` env; each new experiment is a new cell in the Note's notebook.

## Findings

| Note | Quote (short) | Verdict | Action |
|---|---|---|---|
| 622 | "Strong duality holds, as it does for every linear program that has a finite best value" | WRONG FACT | sourced: Boyd and Vandenberghe, Convex Optimization (2004), Ch. 5, inequality-form LP (holds whenever the primal is feasible); reworded |
| 622 | "Real solvers (the simplex method, interior-point methods) handle thousands of variables" | UNSUPPORTED | sourced: Boyd and Vandenberghe (2004), Ch. 11; size claim dropped |
| 622 | dual sign constraints "which many solvers handle more easily" | UNSUPPORTED | derived: projection onto lambda >= 0 is max(v, 0), shown in the Note |
| 622 | "`QuantileRegressor` solves exactly this kind of linear program" | UNSUPPORTED | sourced: scikit-learn docs, QuantileRegressor (uses scipy linprog) |
| 622 | "`SVC` solves this dual" | UNSUPPORTED | sourced: scikit-learn User Guide, SVM, Mathematical formulation |
| 622 | Lasso constraint form "is a quadratic program once each weight is split" | UNSUPPORTED | sourced: Tibshirani (1996), Section 6 |
| 1001 | "Transformers replace recurrence with attention and power today's language models" | UNSUPPORTED | sourced: Vaswani et al. (2017); Brown et al. (2020) for GPT-3 |
| 1001 | "A single neuron is very close to logistic regression" | UNSUPPORTED | derived: sigmoid neuron computes sigma(w^T x + b), the logistic-regression formula |
| 1001 | "Deep learning libraries store every input, weight and output as a tensor" | UNSUPPORTED | sourced: TensorFlow guide, Introduction to Tensors; narrowed to TensorFlow |
| 1001 | "A neural network spends almost all its time multiplying matrices" | intuition (kept) | kept as an intuition that points the right way; transcript fact added (libraries are built on linear algebra) |
| 1001 | "Calculus is not on the usual list of prerequisites" | UNSUPPORTED | deleted (side remark); "training a network is calculus" kept as intuition |
| 1001 | "PyTorch: Meta's deep learning library" | WRONG FACT | reworded: first built at Meta, now run by the PyTorch Foundation (since 2022) |
| 1002 | AlphaGo "In 2016 ... beat Lee Sedol" | UNSUPPORTED (beyond transcript) | sourced: Silver et al., Nature 2017 |
| 1002 | Extra "CUDA was released in 2007; the switch ... 2009 and 2012" | UNSUPPORTED | sourced: NVIDIA "CUDA 1.0 released" (June 2007); Raina et al. ICML 2009; Krizhevsky et al. 2012 Sec. 3.2 |
| 1002 | Extra "Since Keras 3 (2023) ... TensorFlow, JAX or PyTorch" | UNSUPPORTED | sourced: keras.io, Introducing Keras 3.0 |
| 1002 | Extra SHAP/LIME "explain the model from outside" | UNSUPPORTED | sourced: Ribeiro et al. 2016 (LIME, Sec. 3), Lundberg and Lee 2017, Selvaraju et al. 2017 |
| 1002 | "on small or tabular data ... ML is the better tool" | UNSUPPORTED ("tabular") | sourced: Grinsztajn et al. (NeurIPS 2022) |
| 1003 | Extra: autoencoder output "rarely identical", "useful for removing noise and ... anomaly detection" | UNSUPPORTED | sourced: Goodfellow, Bengio and Courville, Deep Learning (2016) 14.1, 14.5; Sakurada and Yairi (2014) |
| 1003 | "GAN, introduced by Ian Goodfellow in 2014" | UNSUPPORTED (year beyond transcript) | sourced: Goodfellow et al., NeurIPS 2014 |
| 1003 | "In 1958 the psychologist Frank Rosenblatt" | UNSUPPORTED | sourced: Rosenblatt (1958), Psychological Review |
| 1003 | Extra: Perceptrons book, Lighthill report 1973 | UNSUPPORTED | sourced: Russell and Norvig, AIMA 4th ed., Sec. 1.3 |
| 1003 | "It was the first landmark result of neural networks in computer vision" | UNSUPPORTED | reworded: dropped the ranking; sourced LeCun et al. (1989) |
| 1003 | Extra: Turing Award 2018, Nobel 2024 | UNSUPPORTED | sourced: ACM Turing Award announcement; nobelprize.org |
| 1003 | Extra: Cybenko/Hornik; "deeper networks usually need far fewer"; "does not promise training will find it" | UNSUPPORTED | sourced: Cybenko (1989), Hornik (1991); Goodfellow et al. (2016) 6.4.1 |
| 1003 | "Go, a board game far more complex than chess" | UNSUPPORTED | sourced: Silver et al. (2016): about 250 moves per turn against 35 |
| 1003 | Extra: "15.3% ... against 26.2%"; Lee Sedol retired 2019 | UNSUPPORTED | sourced: Krizhevsky et al. (2012) abstract; Yonhap interview, Nov 2019 |
| 1003 | "DeepDream, a related Google technique" | WRONG FACT (not related to GANs) | reworded and sourced: Mordvintsev, Olah and Tyka (2015) |
| 1004 | Extra: z = 0 convention "so the choice almost never matters" | UNSUPPORTED | derived: the two rules differ only for z exactly 0, i.e. points on the line |
| 1004 | Extra: "steps whose size depends on the raw input values, so unscaled inputs make it settle on a poor line" | UNSUPPORTED (and misleading: both inputs are on the same 5 to 9.5 scale) | tested: raw 75%, scale-only 50%, centre-only 96%, standardized 97%, raw 1,000 epochs no early stop 92% (b = -673); explained with the update rule (bias moves by 1, weights by about 7) and scikit-learn's n_iter_no_change=5 (docs) |
| 1005 | Extra: scikit-learn "uses exactly this combination ... tol stops training early once the loss stops improving" | WRONG FACT | sourced: scikit-learn docs (tol, n_iter_no_change=5); reworded: the early stop is looser than convergence, tied to Note 1004's 75% after 7 epochs |
| 1005 | "some points are seen more than once in those 10 epochs and others not at all" | WRONG FACT (over 1,000 picks almost every point is seen) | derived: per 100 picks a point is missed with probability 0.99^100 = 0.37 |
| 1006 | Extra: "which is why a perceptron can end with a line that hugs one class" | UNSUPPORTED | derived: all-correct rows have zero gradient (Sec. 7.1), so updates stop at the first separating line |
| 1006 | Extra: subgradient 0 "is the standard choice and does no harm" | UNSUPPORTED | derived: any slope between 0 and -y x is a subgradient; the code uses 0; "no harm" removed |
| 1006 | "The `Perceptron` class is this same model with eta0=1" | UNSUPPORTED (no citation) | sourced: scikit-learn docs, Perceptron |
| 1007 | XOR: "every line it tries misclassifies some corner, so each update undoes an earlier one" | UNSUPPORTED | tested: weights are (0,0,0) after every epoch (new Notebook cell); derived: the four updates y_i(x_i,1) sum to zero |
| 1007 | Extra: Playground loss stays high "whatever the learning rate" | UNSUPPORTED (transcript only covers epochs) | reworded to the transcript: however many epochs |
| 1007 | Extra: "$x_1x_2$ ... makes XOR separable" | UNSUPPORTED | derived: x1 + x2 - 2x1x2 equals XOR on the four rows |
| 1008 | Extra: "Libraries such as Keras print this count for every layer" | UNSUPPORTED (no reference) | sourced: shown with model.summary() in Note 1011 (DATA) |
| 1008 | Extra: "Many write ... w_ji ... because that matches the rows of the weight matrix" | UNSUPPORTED | sourced: Nielsen, Neural Networks and Deep Learning (2015), Ch. 2 |
| 1009 | Extra: "Two hidden nodes are in fact enough for XOR: one weight setting separates it perfectly" | WRONG FACT (for this data) | tested: 2 hidden nodes over 30 seeds, best 87.5%, never 100%; 3 nodes 1/30, 4 nodes 7/30; panel seeds differ (4 nodes with seed 0: 86.5%) |
| 1009 | "an MLP can approximate any function ... with enough training time" | WRONG FACT | reworded: any continuous function; theorem says nothing about training (Goodfellow et al. 6.4.1 via Note 1003) |
| 1009 | Extra: solvers chosen "because each worked best on its data" | UNSUPPORTED | tested: 5 seeds each; lbfgs 81-100% vs adam 35-64% on XOR/circles; adam 80-99% vs lbfgs 79-85% on ReLU spirals |
| 1009 | "Changing only the activation function makes the deep network trainable" | UNSUPPORTED (one seed) | tested: adam, 5 seeds: sigmoid 50% every time, ReLU 80-99%; cause linked to Note 1018 |
| 1009 | Extra: softmax "in practice" | UNSUPPORTED (no reference) | sourced: Goodfellow et al. (2016) 6.2.2.3 |
| 1010 | Extra: raw inputs pin the sigmoid, "small changes to the weights hardly change the output, which makes training very slow" | UNSUPPORTED | derived: sigmoid slopes at the three sums are 1.9e-9, 1.1e-6, 3.7e-6, and backprop multiplies by them; "Real projects standardize" reworded to point at Note 1023 |
| 1010 | Extra: "This is why scikit-learn's MLPClassifier and Keras both store each layer's weights with shape (nodes in, nodes out)" | UNSUPPORTED (design rationale) | sourced: Keras docs, Dense computes dot(input, kernel) + bias; shapes checked in the Notebook; "This is why" removed |
| 1011 | Extra: "Keras 3 drops `input_dim`" | WRONG FACT | tested: Keras 3.15 still builds the model and prints a warning; reworded with the warning text |
| 1011 | Extra: Keras batch of 32 by default | UNSUPPORTED (no reference) | sourced: Keras docs, Model.fit (batch_size default 32) |
| 1011 | Extra: "`validation_split` takes the last 20% of the rows" | UNSUPPORTED (no reference) | sourced: Keras docs, Model.fit |
| 1011 | "ReLU ... usually train better than sigmoid ones" | UNSUPPORTED (transcript says "generally", no source) | sourced: Goodfellow et al. (2016) Sec. 6.3, plus Note 1009 data |
| 1011 | Extra: "another run can flag a few leavers and score slightly higher" | UNSUPPORTED | tested: seeds 0, 2, 3, 4 flag 35-128 leavers, 79.9-80.7%; seed 1 with 100 epochs 83.4% (new Notebook cell) |
| 1012 | "These pairs look alike when handwritten: a 2 with a straight base resembles a 7 ..." | intuition (kept) | kept as intuition; tested in an Extra: nearest-centroid confusions 9->4 rank 3, 7->1 rank 7, but 2->7 rank 36 of 90 |
| 1012 | "KNN ... took far longer to predict" | UNSUPPORTED (no timing of the network; different split) | derived: KNN compares with 33,600 stored images vs two matrix products; noted the different split |
| 1012 | Extra: "CNNs reach over 99% on MNIST" | UNSUPPORTED | sourced: LeCun et al. (1998), LeNet-5 test error 0.95% |
| 1012 | "ReLU ... usually works best in hidden layers" | UNSUPPORTED | sourced: Goodfellow et al. (2016) Sec. 6.3 |
| 1013 | Extra: "An older version, `Admission_Predict.csv`, has only the first 400 rows" | UNSUPPORTED (could not verify on Kaggle) | deleted (side remark) |
| 1013 | "The network simply has not finished learning" (cause of R2 = -0.06) | UNSUPPORTED | tested: one-layer network, 3 seeds: 10 epochs R2 -16.4 to 0.19, 100 epochs 0.42 to 0.78; two layers at 100 epochs 0.78 to 0.82 |
| 1013 | Extra: deep learning "not necessarily on small tables" | UNSUPPORTED | sourced: Grinsztajn et al. (2022) |
| 1014 | Extra: "Keras always reports the average over the batch, and calls it the loss" | UNSUPPORTED (no reference; "always" too strong) | sourced: Keras docs, Losses (default reduction sum_over_batch_size) |
| 1015 | Extra: large IQ input "would dominate the weighted sums and make training unstable, as ... shows for the sigmoid" | UNSUPPORTED (wrong reference: this network is linear) | derived: a weight's gradient is multiplied by its input (dO/dW = x, Sec. 6), so IQ weights get about 10x larger gradients |
| 1015 | Extra: "This automatic differentiation is how Keras computes the gradients" | UNSUPPORTED (no reference) | sourced: TensorFlow guide, automatic differentiation |
| 1015 | Extra: "Starting from different (random) values avoids this" | UNSUPPORTED (no reference) | sourced: Goodfellow et al. (2016) Sec. 8.4 |
| 1016 | cause of the stuck classifier: "Four rows: very little data to learn from" | UNSUPPORTED (the other two causes are tested/derived; 4 rows are linearly separable) | deleted |
| 1016 | Extra: "With eta = 0.5 the steps are too big and the loss ends higher" | UNSUPPORTED | tested: loss rises in 36 of 2,000 epochs, lowest 0.705 at epoch 194, ends 0.76 (new Notebook cell) |
| 1017 | "for any real network ... no formula for the solution" | UNSUPPORTED (no reference) | sourced: Goodfellow et al. (2016) Sec. 6.2 |
| 1018 | "ReLU networks usually train with smaller rates" (and spikes come from lr 0.5) | UNSUPPORTED | tested: ReLU network spikes 7 / 3 / 0 at lr 0.5 / 0.1 / 0.05 (new Notebook cell); "usually" claim replaced by the result |
| 1018 | Extra: under Adam "even tiny gradients produce visible weight changes" | UNSUPPORTED | sourced: Kingma and Ba (2015) Sec. 2.1 |
| 1018 | "It shows up most in recurrent neural networks" | UNSUPPORTED (transcript only, no reason) | sourced: Pascanu et al. (2013) |
| 1018 | Extra: Keras 3 computes BCE from the logit | UNSUPPORTED (no reference) | sourced: Keras 3 source, backend/tensorflow/nn.py binary_crossentropy (checked in the installed copy) |
| 1018 | "one of the main reasons neural networks failed in the 1980s and 1990s" | UNSUPPORTED (history beyond transcript wording) | sourced: Hochreiter (1991); Bengio et al. (1994) |
| 1019 | Extra: "The number of calls is 2 fib(n) - 1" | UNSUPPORTED (stated, not shown) | derived: C(n) = 1 + C(n-1) + C(n-2) gives C(n) + 1 = 2 fib(n) |
| 1019 | "the whole gradient costs about as much as one forward pass" | WRONG FACT (imprecise) | sourced: Baydin et al. (2018) Sec. 3: c < 6, typically 2 to 3 times |
| 1019 | Extra: training needs more memory because activations are stored | UNSUPPORTED | sourced: Chen et al. (2016); Baydin et al. (2018) Sec. 3 |
| 1019 | Extra: `functools.lru_cache` | UNSUPPORTED (no reference) | sourced: Python docs |
| 1020 | powers of 2 "can run slightly faster"; deep learning "almost always means mini-batch" | UNSUPPORTED (no reference in this Note) | sourced: Goodfellow et al. (2016) Sec. 8.1.3 |
| 1021 | Extras: Goyal et al. 2017 warm-up; Keras Dense defaults (Glorot uniform, zero bias) | UNSUPPORTED (no reference given) | sourced: Goyal et al. (2017); Keras docs, Dense |
| 1022 | Extra: "The decision boundary hardly changes ... what grows is the network's confidence ... That is why the validation loss rises by 70%" | UNSUPPORTED | tested (new Notebook cell): same class on 98% of the grid; mean distance of predictions from 0.5 grows 0.30 -> 0.42; mean loss of a misclassified validation point 1.25 -> 2.74 |
| 1023 | "nearly all the change during training goes into w2 ... the large steps on w2 overshoot back and forth" | WRONG FACT (the network uses Adam, whose steps do not scale with the gradient) | tested: in epoch 1 age and salary weights both moved about 0.004; standardizing salary alone gives 85-86%, age alone still jumps 35-85%, a 100x smaller learning rate gives 65% (all "did not buy"). Sourced: Kingma and Ba (2015) Sec. 2.1. Reworded: equal steps move z 2,000x further through salary |
| 1024 | dropout origin (2012/2014), "improved even strong networks by 1 to 2 points", ensemble behaviour, Keras per-step masks and inverted dropout | UNSUPPORTED (no references; transcript gives only "around 2%") | sourced: Hinton et al. (2012); Srivastava et al. (2014) Sec. 1, 6; Keras docs, Dropout |
| 1025 | Extras: Keras training loss computed with dropout on; original paper keep-probabilities 0.8/0.5 | UNSUPPORTED (no reference) | sourced: Keras FAQ; Srivastava et al. (2014) App. A.4 |
| 1026 | Extra (Sec. 6): "Adam rescales each weight's step ... Loshchilov and Hutter (2019) showed that true weight decay works better with Adam" | UNSUPPORTED (citation not specific) | sourced: Loshchilov and Hutter (ICLR 2019) abstract and Sec. 2, checked in the paper; Keras docs for `weight_decay` and AdamW, checked in Keras 3.15 |
| 1026 | Extra (Sec. 7.4): 92% of L2 first-layer weights < 0.001 because "Adam ... even the small pull of the penalty produces full-size steps towards 0" | UNSUPPORTED, and the result contradicts the textbook (L2 should not zero weights) | tested: only the optimizer changed: L2 weights below 0.001 = 7% with SGD vs 92% with Adam. Sourced: Kingma and Ba (2015) Sec. 2.1, Loshchilov and Hutter (2019) Sec. 2. Moved into a labelled Adam caveat in the new Sec. 7.6 Extra |
| 1026 | Extra (Sec. 7.5): "With Adam, L1 does not drive weights to exactly 0 ... hovers around it ... Exact zeros need a different optimizer or pruning" | UNSUPPORTED | tested: Adam L1: no exact zeros, 54% below 0.001, 94% below 0.01, 94% changed sign in the last 100 epochs. Sourced: Friedman et al. (2010) soft thresholding, Han et al. (2015) pruning. Moved into the Sec. 7.6 Extra |
| 1026 | Main result: L1 gives sparse weights and L2 does not (Sec. 5.2, Summary) was not shown by the Note's data | redesigned | new Sec. 7.6 and Figure 5: same moons data and network, plain SGD (learning rate 0.01), only the penalty changed, 3 seeds: L1(0.003) sets 56% of first-layer weights to 0 (to three decimals), L2(0.03) 3%; both have 90% validation accuracy. Sourced: ESL Sec. 3.4.3; Goodfellow et al. (2016) Sec. 7.1.2. Summary table cell changed from "many exactly 0" to "many pushed to 0" |

## Counts per Note

| Note | Findings |
|---|---|
| 622 | 6 |
| 1001 | 6 |
| 1002 | 5 |
| 1003 | 10 |
| 1004 | 2 |
| 1005 | 2 |
| 1006 | 3 |
| 1007 | 3 |
| 1008 | 2 |
| 1009 | 5 |
| 1010 | 2 |
| 1011 | 5 |
| 1012 | 4 |
| 1013 | 3 |
| 1014 | 1 |
| 1015 | 3 |
| 1016 | 2 |
| 1017 | 1 |
| 1018 | 5 |
| 1019 | 4 |
| 1020 | 1 |
| 1021 | 1 |
| 1022 | 1 |
| 1023 | 1 |
| 1024 | 1 |
| 1025 | 1 |
| 1026 | 4 |

Every Note had at least one finding. Notes with only one minor finding (a missing reference): 1014, 1017, 1020, 1021, 1024, 1025.

By verdict: UNSUPPORTED 71, WRONG FACT 10, WRONG CITATION 0; plus 2 intuitions checked and kept, and 1 redesigned experiment (1026).

## UNRESOLVED (removed from Note)

- 1001: "Calculus is not on the usual list of prerequisites".
- 1003: "It was the first landmark result of neural networks in computer vision" (LeCun 1989).
- 1013: "An older version, `Admission_Predict.csv`, has only the first 400 rows; we use the newer one." (could not verify on Kaggle).
- 1016: "Four rows: very little data to learn from" as a cause of the stuck classifier.
- 1001/1003 citation side remarks shortened under "Learning comes first"; no facts lost.

## Notes for the reviewer

- 1026: the main sparsity lesson now uses plain SGD (Sec. 7.6, Figure 5, new data files `sparsity.csv`, `sparsity_weights.csv`). Sections 7.1 to 7.5 still use Adam, as in the lecture. The Adam result (92% of L2 weights near 0) is now a labelled caveat with its tested cause.
- New notebook cells were added but notebooks were not re-executed end to end; the numbers come from scripts that run the same code (1004, 1007, 1009, 1011, 1012, 1013, 1016, 1018, 1022, 1023, 1026).
- Full references are in a new `## Sources` section before Key terms in each edited Note; the text uses short tags.
