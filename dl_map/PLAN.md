# Deep Learning playlist plan

**Key point:** 84 Videos (52 hours), 10 parts. Same teacher, same Note rules as the ML course. No new pipeline steps needed. Everything here is a draft from titles.

- Playlist: [100 Days of Deep Learning](https://youtube.com/playlist?list=PLKnIA16_RmvYuZauWaPlRTC54KxSNLtNn)
- Files: `playlist.txt` (`NNN|id|title`), `playlist_durations.txt` (same plus seconds), `concepts.yaml` (draft map), `check.py` (validates it), `transcripts/` (downloading)
- Check: `/home/anshu/miniforge3/envs/campusx/bin/python dl_map/check.py`

## 1. Parts

| Part | Videos | Purpose | Written by |
|---|---|---|---|
| A. Foundations | 1-3 | What DL is, types of networks, history | Claude (1 and 3 maybe deferred) |
| B. Perceptron to MLP | 4-10 | One neuron, its limits, many layers, forward pass | Claude |
| C. First ANNs in Keras | 11-13 | Three small projects: churn, MNIST, admissions | subagents |
| D. Training a network | 14-20 | Loss, backpropagation, gradient problems, GD variants | Claude |
| E. Improving a network | 21-31 | Early stopping, scaling, dropout, L1/L2, activations, init, batch norm | Claude (25 is code: subagent) |
| F. Optimizers and tuning | 32-39 | EWMA to Adam, then Keras Tuner | Claude (39 is code: subagent) |
| G. CNN theory | 40-48 | Convolution, padding, pooling, LeNet, CNN backprop | Claude |
| H. CNN in practice | 49-54 | Cat vs dog, augmentation, pretrained models, transfer learning, functional API | subagents |
| I. RNN family | 55-66 | RNN, BPTT, LSTM, GRU, stacked and bidirectional | Claude (57, 63 are code: subagents) |
| J. Attention and transformers | 67-84 | Seq2seq, attention, self-attention, full transformer | Claude (67 is history: subagent) |

- Subagent load: 3 + 1 + 1 + 6 + 2 + 1 = **14 Videos**. Claude: **70 Videos**.
- Order: A, B first (they lock the DL style). Subagents can start C while Claude writes B.

## 2. Pipeline steps

**Same 14 steps as the ML map. No new ones.** DL Videos only use 5 of them:

| Step | DL Concepts there |
|---|---|
| 0 Foundations | DL intro, history, biological neuron, chain rule, sequential data |
| 5 Engineer features | input scaling, data augmentation, word embeddings |
| 8 Model | almost everything: architectures, backprop, activations, optimizers |
| 9 Evaluate | visualising what a CNN sees |
| 10 Tune | improving a network, early stopping, Keras Tuner, fine-tuning |

Why no "Train" step: the ML map already puts gradient descent and regularisation under 8 Model. A separate step would break that and the shared numbering. Same numbers also mean the two maps can be merged later.

Instead, step 8 needs **Concept map areas** (as the ML map splits Model in two): ANN and training (B-F), CNN (G-H), RNN (I), attention and transformers (J).

Steps 1-4, 7, 11-13 stay empty: the playlist has no data-gathering, splitting or deployment Videos.

## 3. Deferred or Skipped (suggestions only)

| Video | Suggest | Why |
|---|---|---|
| 1 Course announcement | Deferred | Like ML Video 1: becomes the DL Course map. Its curriculum (GANs, autoencoders, object detection) was never made. |
| 3 Types, history, applications | Deferred (partly) | Like ML Video 8. Keep "types of networks", defer history/applications. |
| 41 CNN vs visual cortex | Deferred | History of CNNs, no method. |
| 67 History of LLMs | Deferred | 87 min history, no method; nothing later needs it. |

**Overlap with the ML course** (not duplicates within this playlist; keep, but Notes can be shorter and link back):

| DL Video | Overlaps ML Videos |
|---|---|
| 5 Perceptron trick | 70-71 (Logistic regression: perceptron trick) |
| 6 Perceptron loss, BCE, sigmoid | 72-74 (sigmoid, binary cross-entropy) |
| 20 Batch vs SGD vs mini-batch | 57-60 (gradient descent family) |

No setup or job-role Videos, so nothing obvious to skip.

## 4. ML Notes to read first

From Video 1: Python basics, how to train a model and prepare data (the ML course), and basic linear algebra (vectors, matrices, dot product).

| Needed for | ML Videos |
|---|---|
| Everything | 2 AI vs ML vs DL, 3 Types of ML, 11 Tensors |
| C Keras projects | 13 Toy project, 24-25 Scaling, 26-27 Encoding |
| B Perceptron | 70-75 Logistic regression, sigmoid, cross-entropy |
| D Training | 57-60 Gradient descent family, 52 Regression metrics |
| E Improving | 7 and 62 Overfitting, bias-variance; 63-68 Ridge/Lasso |
| C, I classification | 79 Softmax, 76 Accuracy |
| F Tuning | 111-112 Hyperparameters, grid search |

## 5. Unusual

- **Title says 100 days, playlist has 84.** It ends at Transformer inference (84).
- **Very long Videos:** 67 (87 min), 64 (86), 73 (83), 68 (74), 78 (73), 62 (70). Plan for big Notes (Notes are never split).
- **Title slips:** 31 says "Batch Learning in Keras" but means Batch Normalization. 37 and 38 are both "Part 5". 30 spells Glorot as "Glorat".
- **Linked pairs:** 24/25 (dropout theory/code), 61-63 (LSTM what/how/code), 72-76 (five self-attention Videos). Write each pair in order.
- **Video 3 reuses older footage** from an earlier DL course he abandoned (he says so at the start). Quality may differ.
- **Transcripts checked so far:** 1-3 match their titles. Video 1 lists prerequisites (section 4).
- **No live sessions** in titles. Upload order not checked: it would need 84 extra YouTube requests while transcripts download.
- **Transcripts:** auto-Hindi (`hi-orig`) so far, same messy quality as the ML ones. About 90 s per Video, so the full set takes about 2 hours. Videos with no subtitles are listed in `transcripts/fetch.err` as `NNN NO SUBS`.
- yt-dlp warns "No supported JavaScript runtime". Captions still download; if many come back NO SUBS, install `deno` and rerun `transcripts/fetch.sh` (it skips finished Videos).
