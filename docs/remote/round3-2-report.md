# Round 3, list 2: report

Each Note was read in full, given new figures for its key ideas, laddered (plain idea and picture, then the standard term with its glossary ID, then the mechanism on the Note's numbers, then the formal version), and rebuilt with `tools/build.sh` ("Built"). Every new figure, frame grid and PDF page was looked at.

"Words per visual" and "figure share" use the measure of `docs/visual-audit/measure.py` (numbered sections only; Summary, Prerequisites, Sources and Key terms left out).

## 1054-keras-functional-api

- **Visuals added**
  - `images/graph_build.gif` (+ `_frames.png`), Plotly frames: the model of Figure 3 built one code line per frame. Each call adds a node and an edge, and the parameter count grows to the 8,898 of `model.summary()` (asserted). Illustrates "create a layer, then call it on its input" and the parameter count.
  - `images/naive_designs.tex`, TikZ: the naive designs of section 3 (two separate networks; three networks averaged), to compare with Figure 1b and 1c.
  - `images/concat_vs_add.tex`, TikZ: the Note's two example vectors joined by `Concatenate` (8 numbers) and by `Add` (4 numbers).
  - `images/loss_weights.py`, Plotly: the worked example of section 5.3 as stacked bars, with and without the 0.1 weight on age (totals 9.3 and 1.2, asserted).
- **Ladder:** section 3 now names regression, classification, multi-output and multi-input model where each idea appears, and explains with Figure 2 why the averaged design is weaker (no network sees the inputs together). Section 4.1 walks the animation before the parameter formula.
- **Words per visual:** 413 before, 246 after. **Figure share:** 3 of 4 sections before, 4 of 4 after.
- **Text fixed:** the Overview contents sentence became a list (§9). Glossary IDs added at first use: G-1776, G-818, G-1991, G-1655, G-395, G-1272, G-1269, G-772, G-1949, G-1374, G-1798, G-1065, G-583, G-71, G-1818, G-1681, G-2005, G-2088, G-788, G-1131, G-1194, G-304. Figures renumbered.
- **New Key terms:** none.

## 1055-why-rnn

- **Visuals added**
  - `images/padding_waste.gif` (+ `_frames.png`), Plotly frames: the 25,000 IMDB training reviews padded (grey) or cut (red) to one input length, from 100 to 2,494 words. Illustrates zero padding and truncation together; asserts 90% padding at 2,494 and 8.4% of reviews cut at 500.
  - `images/shift_accuracy.py`, Plotly: section 5.4's experiment (accuracy against shift, 67.9% down to 57.4%) as a chart against the 50% guessing line.
  - `images/weights_vs_length.py`, Plotly (log axes): weights of a dense layer on the padded input against a SimpleRNN layer as the review grows; asserts the Keras counts 10,000,010 and 100,110. Illustrates parameter sharing.
- **Ladder:** section 5.2 now shows the trade-off before listing the two costs; section 6 names the RNN's memory with its standard term, the hidden state.
- **Words per visual:** 494 before, 293 after. **Figure share:** 4 of 6 before, 4 of 6 after (the new figures went into subsections 5.2, 5.4 and section 6, which already counted).
- **Text fixed:** "an internal state" now carries the standard term **hidden state** (G-891). The 500-word cut is now given for the training reviews too (8.4%), so the figure and the text agree. Glossary IDs added: G-216, G-1270, G-1374, G-772, G-484, G-1647, G-1774, G-1340, G-1379, G-2093, G-811, G-923, G-1436, G-1447, G-891, G-1769, G-1123, G-1975, G-2007.
- **New Key terms:** none.

## 1056-rnn-forward-propagation

- **Visuals added**
  - `images/batch_tensor.tex`, TikZ: the three reviews as one-hot tables, padded with a grey zero row into one batch of shape (3, 4, 5). Illustrates time steps, features, padding and the batch tensor (section 3).
  - `images/worked_steps.gif` (+ `_frames.png`), Plotly frames: the worked example of section 5.3, one operation per frame (the word picks its row of W_i, the feedback h_(t-1) W_h, the sum, tanh), ending with the prediction 0.83. Hidden states asserted against `data/worked_example.csv`.
- **Ladder:** section 3.3 now names batch, tensor and padding with the picture before the code; section 5.3 points the reader through the animation before the hand computation.
- **Words per visual:** 450 before, 306 after. **Figure share:** 4 of 6 before, 6 of 6 after.
- **Text fixed:** glossary IDs added at first use: G-1647, G-1374, G-1949, G-2093, G-1379, G-772, G-1976, G-268, G-1957, G-1436, G-775, G-1646, G-891, G-2041, G-1947, G-1830, G-1447. Figures renumbered.
- **New Key terms:** none.

## 1057-rnn-sentiment-analysis

- **Visuals added**
  - `images/pad_truncate.py`, Plotly: `pad_sequences(maxlen=50)` on four real IMDB training reviews (218, 189, 141 and 11 words): the long ones lose their start and keep their last 50 words, the shortest gets 39 zeros in front. Lengths saved in `data/pad_examples.csv` from `keras.datasets.imdb.load_data()` and asserted.
  - `images/return_sequences.tex`, TikZ: the SimpleRNN unrolled over 50 inputs, with `return_sequences=False` (only h_50 goes on) and `True` (every hidden state leaves).
- **Ladder:** section 5.3 now shows the picture and names `return_sequences` before the two settings; the Overview's aims became a list with section links.
- **Words per visual:** 436 before, 316 after. **Figure share:** 4 of 6 before, 6 of 6 after.
- **Text fixed:** "With time, use full reviews" was vague; now "When training time allows, use full reviews". Glossary IDs added: G-1769, G-1374, G-1949, G-956, G-2093, G-1436, G-1984, G-1416, G-923, G-137, G-1300, G-1141, G-304, G-169, G-696, G-1845, G-2127, G-585, G-910, G-247, G-1429, G-851, G-1558.
- **New Key terms:** none.

## 1058-types-of-rnn

- **Visuals added**
  - `images/two_questions.tex`, TikZ: the Key point's two questions (is the input a sequence? is the output?) as a 2 x 2 grid, one type per cell.
  - `images/keras_shapes.tex`, TikZ: the Notebook's four RNN models layer by layer, with the shape each layer hands on (shapes from `data/shapes.csv`). Shows how `RepeatVector` creates the time-step axis and `return_sequences` keeps or removes it.
- **Ladder:** the Overview now shows the two questions as a picture before the table; section 7 walks the shapes before the rule "3D output means one prediction per time step".
- **Words per visual:** 293 before, 216 after. **Figure share:** 4 of 6 before, 6 of 6 after.
- **Text fixed:** glossary IDs added at first use: G-1769, G-246, G-1155, G-1266, G-1386, G-918, G-133, G-1154, G-1771, G-1721, G-1456, G-1305, G-1300, G-136, G-2072, G-1141, G-682, G-564, G-1387, G-1374. Figures renumbered.
- **New Key terms:** none.

## 1060-problems-with-rnn

- **Visuals added**
  - `images/slopes.py`, Plotly: the slope of tanh against the slope of ReLU. Illustrates fix 1 of section 5: each backward step multiplies the gradient by (slope) x w_h, and ReLU's slope is exactly 1 for positive inputs.
  - `images/power_steps.gif` (+ `_frames.png`), Plotly frames: the same factor multiplied once per step for 0.72, 1.0, 1.1 and 1.5, from 1 to 99 steps (log scale). Asserts the Note's 0.72^99 = 7.5e-15, 1.1^100 = 13,781 and 1.5^100 = 4e17. Illustrates vanishing and exploding as one process.
  - `images/clipping.py`, Plotly: clipping by norm on g = (3, 4) with threshold 1, giving (0.6, 0.8).
- **Ladder:** sections 5 and 6 now show the mechanism as a picture before the Keras code; section 4.3 points forward to the animation.
- **Words per visual:** 578 before, 341 after. **Figure share:** 3 of 5 before, 5 of 5 after.
- **Text fixed:** glossary IDs added at first use: G-1774, G-2070, G-2056, G-731, G-246, G-1126, G-1374, G-1949, G-1892, G-980, G-665, G-1407, G-1668, G-1064, G-915, G-914, G-1819, G-1123, G-826, G-861, G-1068.
- **New Key terms:** none.

## 1063-lstm-next-word-prediction

- **Visuals added**
  - `images/pad_split.tex`, TikZ: the first three training sequences (integers from section 4.2) padded in front to 51 integers and split into the input X (50 columns) and the output y (the last column).
  - `images/onehot_softmax.py`, Plotly: (a) a regression output of 2.7 falls between the indices of "the" and "and"; (b) for the prefix "but", the one-hot target against the trained model's softmax probabilities for its five most likely words (`data/typing.csv`, asserted).
  - `images/generate_loop.gif` (+ `_frames.png`), Plotly frames: the generation loop for "the wolf", one predicted word appended per frame (`data/generated.csv`, asserted).
- **Ladder:** sections 4.5, 5.1, 5.2 and 8.2 now show the mechanism on the Note's own data before the code.
- **Words per visual:** 500 before, 322 after. **Figure share:** 4 of 8 before, 6 of 8 after (section 6, the parameter count, and section 9, a short list of ideas, have no figure).
- **Text fixed:** glossary IDs added at first use: G-1322, G-1964, G-1919, G-1374, G-1949, G-1555, G-1287, G-1416, G-395, G-1266, G-1832, G-151, G-350, G-656, G-1429, G-909, G-2067. Figures renumbered.
- **New Key terms:** none. ("Bigram" and "Baseline" are already in the Note's Key terms table, but `merge_glossary.py --id` finds no ID for them; they may need merging on the other machine.)

## 1068-encoder-decoder

- **Visuals added**
  - `images/pair_lengths.py`, Plotly heatmap: the Notebook's 40,000 English-French training pairs counted by English length and French length. Only 30% lie on the same-length diagonal. Counts recomputed with the Notebook's own filtering and seeds (167,130 lines, 82,798 distinct sentences, 40,000 pairs, all matching its printed output) and saved as `data/pair_lengths.csv`. Illustrates "the two lengths are not tied".
  - `images/step_loss.py`, Plotly: the worked example of section 5.3, the probability of each correct word and its loss -ln p (total 5.52, mean 1.84, asserted).
  - `images/seq2seq_inference.tex`, TikZ: prediction with greedy decoding on the toy example, each output fed back as the next input, the wrong "jao" carried forward. Pairs with the training figure (teacher forcing).
  - `images/scale_compare.py`, Plotly: the Notebook's model against Sutskever et al. (2014): parameters, training pairs (log scales) and BLEU.
- **Ladder:** section 3 now shows the length mismatch on real data; section 6 contrasts prediction with training in a picture before the real results.
- **Words per visual:** 580 before, 331 after. **Figure share:** 5 of 8 before, 8 of 8 after.
- **Text fixed:** glossary IDs added at first use: G-1773, G-682, G-1981, G-564, G-461, G-1830, G-1442, G-1374, G-1949, G-1983, G-1955, G-350, G-870, G-315, G-1865, G-1492. Figures renumbered.
- **New Key terms:** none.

## 1069-attention-mechanism

- **Visuals added**
  - `images/static_context.tex`, TikZ: the plain encoder-decoder on "turn off the lights", one final state sent unchanged to every decoder step (section 3.2, "static").
  - `images/dynamic_context.tex`, TikZ: the same sentence with attention, each decoder step with its own context vector mixed from all encoder states. The line widths are drawn by hand to show the idea of section 3.2, and the caption says so.
  - `images/softmax_sum.gif` (+ `_frames.png`), Plotly frames: the worked examples of sections 6.2 and 5.2 as one process: scores, exponentials, weights, then the weighted states stacked into the context vector (all numbers asserted).
  - `images/bidirectional.tex`, TikZ: Bahdanau et al.'s bidirectional encoder, forward and backward RNNs joined at each position (section 9).
- **Ladder:** sections 3 and 4 now each show their idea as a picture before the notation; section 6.2 animates softmax before the full step list.
- **Words per visual:** 542 before, 278 after. **Figure share:** 4 of 8 before, 7 of 8 after.
- **Text fixed:** the attention weights alpha_ij now carry their own standard term, "attention weights", before the synonym "alignment scores". Glossary IDs added: G-226, G-326, G-461, G-225, G-190, G-775, G-189, G-1830, G-188, G-291, G-826. Figures renumbered (the cross-reference to Figure 3 of the Bahdanau vs Luong Note left as it is).
- **New Key terms:** none.

## 1072-what-is-self-attention

- **Visuals added**
  - `images/vectorization.tex`, TikZ: one-hot and bag of words on the vocabulary mat, cat, rat, with the Note's two example sentences.
  - `images/lookup_same.tex`, TikZ: the embedding layer as a lookup table; "bank" picks the same row in "money bank grows" and "river bank flows".
  - `images/bank_bars.py`, Plotly: section 6's similarity table as grouped bars (`data/bank_similarity.csv`, asserted).
- **Ladder:** section 3 shows the counting methods before naming their weakness; section 5 shows why a static embedding cannot change (a lookup) before the term "contextual embedding".
- **Words per visual:** 498 before, 251 after. **Figure share:** 3 of 5 before, 5 of 5 after.
- **Text fixed:** glossary IDs added at first use: G-1764, G-462, G-1305, G-1877, G-2084, G-1379, G-2093, G-250, G-2127, G-634, G-1813, G-1049, G-1544, G-1306, G-491. Figures renumbered.
- **New Key terms:** none. ("TF-IDF" is used in the text but has no glossary ID; it is not a Key term of this Note.)

## 1073-self-attention-step-by-step

- **Visuals added**
  - `images/bank_mix.py`, Plotly: the new "bank" in each phrase as stacked shares of the words of its phrase, with the real weights of the simple self-attention (`data/weights_simple.csv`, asserted). Illustrates section 3's "a word as a mix of its sentence".
  - `images/matrix_shapes.tex`, TikZ: X times X-transpose gives S, a row-wise softmax gives W, W times X gives Y, with the shapes for "money bank grows" (section 5).
  - `images/dog_query.py`, Plotly: section 7's invented "old brown dog" example: the query and the four keys as arrows, and the scores and softmax weights as bars (all numbers asserted).
- **Ladder:** sections 3, 5 and 7 now each show their idea before the formula.
- **Words per visual:** 484 before, 324 after. **Figure share:** 4 of 8 before, 7 of 8 after (section 6, an argument with no numbers, has no figure).
- **Text fixed:** in section 7, `\text` had become a tab character followed by "ext" in five formulas ($s_{\text{dog},j}$ and the q and k vectors), which broke them. Restored. Glossary IDs added: G-1764, G-1830, G-1011, G-2068, G-462, G-634, G-491, G-223, G-1528, G-836, G-1952, G-1097, G-915, G-1374, G-1949. Figures renumbered.
- **New Key terms:** none.

## 1074-scaled-dot-product-attention

- **Visuals added**
  - `images/example_weights.py`, Plotly: section 3's worked example, the softmax of the scores 4, 6, 2 with and without the division by the square root of 3 (asserted).
  - `images/variance_scale.py`, Plotly: section 6's example, 10 to 70 (variance 400) divided by 10 into 1 to 7 (variance 4).
  - `images/keras_check.py`, Plotly heatmap: section 7's attention matrix for "money bank grows", which the hand computation and Keras' `MultiHeadAttention` both return.
- **Ladder:** each of sections 3, 6 and 7 now shows its worked example or result as a picture.
- **Words per visual:** 315 before, 199 after. **Figure share:** 3 of 6 before, 6 of 6 after.
- **Text fixed:** glossary IDs added at first use: G-1745, G-1740, G-223, G-2078, G-2070, G-1747, G-121, G-1831. Figures renumbered.
- **New Key terms:** none.

## 1075-self-attention-geometric-intuition

- **Visuals added**
  - `images/word_arrows.py`, Plotly: the Note's hand-picked embeddings money (2, 7), bank (7, 3) and river (8, -2) as arrows with their angles (`data/vectors.csv`, asserted). Gives section 3, "words as arrows", its own picture and introduces the river vector used in section 7.2.
- **Ladder:** the Note already climbed from arrows to formulas in every section; only section 3 lacked its picture.
- **Words per visual:** 236 before, 206 after. **Figure share:** 5 of 6 before, 6 of 6 after.
- **Text fixed:** glossary IDs added at first use: G-677, G-611, G-1562, G-1097, G-1764, G-1011, G-2068, G-634, G-462, G-2119, G-477, G-1681, G-1054. Figures renumbered.
- **New Key terms:** none.

## 1076-why-self-attention

- **Visuals added**
  - `images/luong_step.tex`, TikZ: Luong's three equations for decoder step 2 ("la"): the decoder state compared with every encoder state, the softmax, the context vector.
  - `images/one_function.tex`, TikZ: the Notebook's one `attention` function called two ways, giving 3 x 4 weights between two sequences and 4 x 4 weights within one.
- **Ladder:** section 3 now draws the three equations before listing them in Luong's notation; section 5 shows the "one function" idea before the code. The untrained Luong weights (all close to 0.25) were not animated, because they would teach nothing.
- **Words per visual:** 383 before, 232 after. **Figure share:** 3 of 5 before, 5 of 5 after.
- **Text fixed:** glossary IDs added at first use: G-1763, G-1138, G-461, G-1123, G-1011, G-2068, G-103, G-958, G-507. Figures renumbered.
- **New Key terms:** none.

## 1078-positional-encoding

- **Visuals added**
  - `images/order_blind.tex`, TikZ: "Rahul killed the lion" and "the lion killed Rahul" through self-attention with no positions; the same four outputs come out in a different order, and "lion" gets the identical vector (section 3).
  - `images/count_problems.py`, Plotly: the two counting ideas of section 4: the raw count grows without limit, and count divided by length gives position 2 the value 1.0 in "thank you" but 0.5 in "Rahul killed the lion" (asserted).
  - `images/sine_collisions.py`, Plotly: section 5's repeats: positions 11 and 344 at the same height of sin(pos), and positions 15 and 725 on the same point of the (sin, cos) circle (`data/closest_pairs.csv`, asserted).
- **Ladder:** sections 3, 4 and 5 now show each failed idea as a picture before the next improvement, leading up to the formula of section 6.
- **Words per visual:** 483 before, 305 after. **Figure share:** 4 of 7 before, 7 of 7 after.
- **Text fixed:** the standard term "sinusoidal positional encoding" is now attached where the formula appears. Glossary IDs added at first use: G-1528, G-1764, G-462, G-158, G-1666, G-327, G-1489, G-806, G-1815, G-1066, G-1708. Figures renumbered.
- **New Key terms:** none.

## 1079-layer-normalization

- **Visuals added**
  - `images/where_norm.tex`, TikZ: the two places a network normalises, the inputs (data scaling) and the hidden activations (batch or layer normalisation) (section 3).
  - `images/bn_column.py`, Plotly: section 4's worked example, node 1's values 7, 2, 6, 3, 2 before and after batch normalisation on two number lines (mean 4, standard deviation 2.10, first value 1.43; asserted).
  - `images/add_norm.tex`, TikZ: one transformer encoder block with "add and norm" after each sub-layer (section 7.2).
- **Ladder:** section 3 now shows where normalisation happens before the list of benefits; section 7.2 names "add and norm" and draws it before pointing to the encoder Note.
- **Words per visual:** 481 before, 277 after. **Figure share:** 3 of 6 before, 6 of 6 after.
- **Text fixed:** glossary IDs added at first use: G-1054, G-266, G-1348, G-1874, G-1217, G-772, G-963, G-1374, G-1436, G-1681, G-172, G-1556, G-1696. Figures renumbered.
- **New Key terms:** none.

## 1081-masked-self-attention

- **Visuals added**
  - `images/autoregressive.tex`, TikZ: autoregressive generation of "comment ça va", each written word fed back as the next input (section 3).
  - `images/future_weight.py`, Plotly: section 5's leak as bars, the share of each word's unmasked weight taken from later words (0.866 down to 0; `data/weights_unmasked.csv`, asserted).
  - `images/masked_heads.tex`, TikZ: masked multi-head attention, every head with a lower-triangular weight matrix, then concatenation and W_O (section 8).
- **Ladder:** section 3 now draws the loop before naming the paper's quote; section 5 shows the size of the leak before naming it data leakage.
- **Words per visual:** 474 before, 318 after. **Figure share:** 4 of 7 before, 7 of 7 after.
- **Text fixed:** glossary IDs added at first use: G-1172, G-1171, G-234, G-1955, G-535, G-1169, G-358, G-154, G-564, G-1268. Figures renumbered.
- **New Key terms:** none.

## 1084-transformer-inference

- **Visuals added**
  - `images/runs_grid.tex`, TikZ: the decoder runs for "we're friends ." → "nous sommes amies .": one training run using every position, against five inference runs that each recompute every position so far and use only the last (section 3).
- **Ladder:** section 3 now shows the count of runs as a picture before the comparison table.
- **Words per visual:** 376 before, 315 after. **Figure share:** 5 of 6 before, 6 of 6 after.
- **Text fixed:** glossary IDs added at first use: G-358, G-1955, G-1331, G-235, G-639, G-1075, G-1429, G-315, G-507, G-870, G-1022, G-272. Figures renumbered.
- **New Key terms:** none.

## 1086-meaning-as-direction

- **Visuals added**
  - `images/tower_neighbours.py`, Plotly: the 8 GloVe words closest to "tower" by cosine (`data/tower_neighbours.csv`, asserted) (section 3).
  - `images/analogy_dots.py` → `analogy_glove.png` and `analogy_gpt2.png`, Plotly dot charts: each analogy question with the cosine of the closest word of all candidates and of the expected word, coloured by whether the expected word ranks first once the question words are removed, with the rank when it does not (`data/analogies.csv`, asserted). One chart for GloVe (section 5), one for GPT-2 (section 7), so the two can be compared.
- **Ladder:** sections 3, 5 and 7 now show the measured results as pictures before the tables.
- **Words per visual:** 581 before, 293 after. **Figure share:** 3 of 6 before, 6 of 6 after.
- **Text fixed:** glossary IDs added at first use: G-2127, G-613, G-634, G-851, G-1982, G-1981, G-491, G-404, G-196, G-1575, G-2048, G-1506. Figures renumbered.
- **New Key terms:** none.

## 1087-decoder-only-gpt

- **Visuals added**
  - `images/tokens.tex`, TikZ: GPT-2's tokens for the Note's two example texts, with rare words split into coloured pieces and the leading space marked (section 4).
  - `images/embed_lookup.tex`, TikZ: x_0 = row 19206 of W_E ("Steve") plus row 0 of W_P, in the Note's colour rule (learned weights blue, data grey) (section 5).
  - `images/every_position.py`, Plotly: section 7.2's table as bars, the probability of the true next token at each position with the top guess above, and " Apple" (0.69) at the last position (`data/every_position.csv`, asserted).
  - `images/context_cost.py`, Plotly (log scales): n² attention weights per head against context size, with GPT-1, GPT-2 and GPT-3 marked (section 8; the table's counts asserted).
- **Ladder:** sections 4, 5, 7.2 and 8 now each show their idea before the table or formula.
- **Words per visual:** 590 before, 331 after. **Figure share:** 4 of 8 before, 8 of 8 after.
- **Text fixed:** glossary IDs added at first use: G-855, G-565, G-1981, G-335, G-1980, G-1526, G-1683, G-834, G-1973, G-1492, G-870, G-1935, G-459. Figures renumbered.
- **New Key terms:** none.

## 1088-unembedding-and-sampling

- **Visuals added**
  - `images/last_vector.tex`, TikZ: one pass gives a final vector at every position, and generation unembeds only the last (section 4).
  - `images/two_logits.py`, Plotly: section 5.1's two-logit example at T = 0.5, 1 and 2 (0.88/0.12, 0.73/0.27, 0.62/0.38; asserted).
  - `images/sample_logprob.py`, Plotly: all 50 samples of section 6.2, the mean log-probability of each sample's chosen tokens and the mean per temperature (`data/samples.csv`; the five means asserted).
- **Ladder:** sections 4, 5 and 6 now each show their mechanism or result before the formula or table.
- **Words per visual:** 533 before, 306 after. **Figure share:** 3 of 6 before, 6 of 6 after.
- **Text fixed:** glossary IDs added at first use: G-2040, G-1122, G-1956, G-1739, G-1121, G-2039, G-691, G-1985, G-1360. Figures renumbered (the citations of Holtzman et al.'s own Figure 4 kept).
- **New Key terms:** none.

## 1090-superposition

- **Visuals added**
  - `images/interference.py`, Plotly: section 3's reading formula on an example of our own (two features of strength 1): perpendicular directions read exactly 1, directions 80 degrees apart read 1 + cos 80° = 1.17. Illustrates interference.
  - `images/spread_vs_d.py`, Plotly: section 4's table as two charts, measured angle spread against 57.3/√d, and the share of pairs within 5 degrees of perpendicular (`data/random_angles_summary.csv`, asserted).
  - `images/jl_growth.py`, Plotly: the Johnson–Lindenstrauss guarantee (ε = 0.1), directions against dimension on a log scale; the script recomputes the Note's four k values from the Dasgupta–Gupta bound and asserts them against `data/jl_table.csv`.
- **Ladder:** sections 3, 4 and 6 now each show their result as a picture before or beside the derivation.
- **Words per visual:** 489 before, 306 after. **Figure share:** 4 of 7 before, 7 of 7 after.
- **Text fixed:** glossary IDs added at first use: G-1916, G-962, G-1102, G-1307, G-984, G-862, G-772, G-1517, G-925. Figures renumbered.
- **New Key terms:** none.

## 109-random-forest-bias-variance

- **Visuals added**
  - `images/forest_flow.tex`, TikZ: the recipe of section 2, bootstrap samples growing fully grown trees whose average (or majority vote) is the forest, with "low bias, high variance" per tree and "low bias, low variance" for the forest.
- **Ladder:** section 2 now names bagging's bootstrap sample with its standard term and shows the recipe before the two experiments.
- **Words per visual:** 330 before, 250 after. **Figure share:** 3 of 4 before, 4 of 4 after.
- **Text fixed:** "its own random sample" now carries the standard term **bootstrap sample** (G-319). Glossary IDs added at first use: G-1611, G-288, G-287, G-2078, G-2154, G-1132, G-319, G-561, G-1374, G-772, G-1949, G-1429, G-1201. Figures renumbered.
- **New Key terms:** none.

## 11-tensors

- **Visuals added:** none. The Note already has 9 visuals (an animation of the tensor build-up and a diagram for every real data type); the one section without a figure, section 2, is a short definition that Figure 1 already pictures.
- **Ladder:** already in order (plain idea, picture, term, worked size and storage examples).
- **Words per visual:** 160 before, 160 after. **Figure share:** 5 of 6 before and after.
- **Text fixed:** glossary IDs added at first use: G-1957, G-1743, G-2081, G-1180, G-214, G-242, G-1629, G-1787, G-1816, G-772, G-1374, G-1949, G-2129, G-2084, G-1379, G-2093, G-1975, G-1501, G-375, G-801, G-433.
- **New Key terms:** none.

## 115-adaboost-intuition

- **Visuals added** (all on the Note's 10 students and three stumps; `images/adaboost_common.py` reruns the same AdaBoost as the animation and asserts the alphas 0.69, 0.97, 1.28)
  - `images/stagewise_growth.py`, Plotly: the vote of the first 1, 2 and 3 stumps, with 8, 8 and 10 students right (asserted). Illustrates "stage-wise additive" (section 3).
  - `images/vote_example.py`, Plotly waterfall: section 5's worked vote, -2 + 10 - 1 = +7, so "placed" (asserted).
  - `images/score_boxes.py`, Plotly: the weighted sum in every box made by the three cuts; the positive boxes form the L shape of section 6.
- **Ladder:** sections 3, 5 and 6 now each show their idea on the students before or beside the formula.
- **Words per visual:** 528 before, 273 after. **Figure share:** 3 of 6 before, 6 of 6 after.
- **Text fixed:** glossary IDs added at first use: G-167, G-318, G-2104, G-1904, G-559, G-946, G-1867, G-1374, G-772, G-1949, G-2063, G-192, G-912, G-1800. Figures renumbered.
- **New Key terms:** none.

## 119-bagging-vs-boosting

- **Visuals added**
  - `images/swap_bars.py`, Plotly: section 2's base-model swap (stump and fully grown tree; alone, bagged, boosted) as grouped bars, with a note that the axis starts at 0.5, the guessing level.
  - `images/vote_weights.tex`, TikZ: equal votes (bagging, 1 1 0 1 gives 1) against weighted votes (boosting, alphas 0.8, 1.5 and 5 on the answers 1, 1, 0 give 0).
- **Ladder:** section 4 now works one weighted vote through with the Note's three alphas (the answers 1, 1, 0 are stated as a supposition) and shows both votes side by side.
- **Words per visual:** 474 before, 244 after. **Figure share:** 2 of 4 before, 4 of 4 after.
- **Text fixed:** glossary IDs added at first use: G-2154, G-1132, G-1785, G-559, G-1443, G-1374, G-1775, G-1605, G-1146. Figures renumbered.
- **New Key terms:** none.

## 12-setup-anaconda-jupyter-colab

- **Visuals added**
  - `images/notebook_cells.tex`, TikZ: the two kinds of notebook cell, a Markdown cell as typed and after Shift+Enter, and a code cell (the Note's `read_csv` example) with its output (19158, 14) (section 3.2).
- **Ladder:** section 3.2 now shows what the cells look like before the Markdown syntax list.
- **Words per visual:** 436 before, 393 after. **Figure share:** 9 of 9 before and after.
- **Text fixed:** glossary IDs added at first use: G-439, G-195, G-1224, G-990, G-1353, G-362, G-991, G-1168, G-1009, G-999, G-2090, G-692, G-854. Figures renumbered.
- **New Key terms:** none.

## 127-stacking-blending

- **Visuals added**
  - `images/meta_row.tex`, TikZ: section 2.1's student (CGPA 7, IQ 75, package 3.5) turned into one training row for the meta-model (3.7, 4.1, 2.5 with the same target).
  - `images/leak_numbers.py`, Plotly: section 5's measurement, the random forest's and gradient boosting's error on seen against unseen patients (0.09 against 0.30, 0.07 against 0.25), and the in-sample meta-model weights 3.5, 3.8 and 1.0.
- **Ladder:** section 2.1 now shows the row transformation before the next section's recipe; section 5 shows the size of the leak before the two fixes.
- **Words per visual:** 426 before, 320 after. **Figure share:** 5 of 9 before, 7 of 9 after (sections 3 and 4, a recipe list and a comparison table, have no figure).
- **Text fixed:** section 2.1 said "section 8 shows the option that does pass them [the features]"; the `passthrough` option is in section 9, so the reference now says section 9. Glossary IDs added at first use: G-1866, G-1213, G-2096, G-1374, G-772, G-1949, G-314, G-901, G-2067, G-1415, G-1271, G-1461, G-1717. Figures renumbered.
- **New Key terms:** none.

## 128-kmeans-intuition

- **Visuals added**
  - `images/centroid_example.py`, Plotly: the worked example of sections 4.3 and 5.1, the centroid (2, 3) of (1, 2), (3, 2), (2, 5) and the squared distances 2, 2 and 4 that add up to WCSS 8 (asserted).
  - `images/faithful_k.py`, Plotly: k-means on the 272 Old Faithful eruptions (standardized, same settings as `elbow.py`) with k = 2 and k = 3. The WCSS values 80 and 56 are asserted against the elbow curve. Shows what the elbow means: k = 2 matches the dataset's short and long label for 99% of eruptions, and k = 3 cuts the long eruptions in two.
- **Ladder:** section 4.3 now draws the move step before section 5 reuses it for WCSS; section 5.4 shows the clusters on each side of the elbow.
- **Words per visual:** 508 before, 309 after. **Figure share:** 2 of 4 before, 3 of 4 after (section 3, a motivation in words, has no figure).
- **Text fixed:** the standard terms centroid initialization, convergence and elbow method are now attached where each idea appears. Glossary IDs added at first use: G-996, G-401, G-1374, G-2058, G-772, G-367, G-366, G-715, G-2102, G-671, G-670, G-672. Figures renumbered.
- **New Key terms:** none.

## 13-toy-project

- **Visuals added**
  - `images/xy_split.tex`, TikZ: the first 5 rows of `placement.csv` (real values), with the leftover row-number column crossed out (section 3) and the rest split into X and y (section 5).
  - `images/training_line.gif` (+ `_frames.png`), Plotly frames: what `fit` does. Gradient descent on logistic regression's own objective (log loss plus scikit-learn's default L2 penalty) on the 90 scaled training students, showing the 0.5 line and the 0.1/0.9 lines after 1 to 3,000 steps. The final weights are asserted to match scikit-learn's fitted model within 0.02.
- **Ladder:** section 8 now explains in plain words what `fit` does inside (start at zero, small steps that lower the error, named gradient descent) and shows it, instead of only calling it.
- **Words per visual:** 261 before, 207 after. **Figure share:** 6 of 10 before, 8 of 10 after.
- **Text fixed:** glossary IDs added at first use: G-1374, G-772, G-1949, G-395, G-513, G-1441, G-1235, G-1120, G-937, G-591, G-2002, G-1962, G-84, G-862. Figures renumbered.
- **New Key terms:** none.

## 131-hierarchical-clustering

- **Visuals added**
  - `images/two_kinds.tex`, TikZ: agglomerative (bottom-up) against divisive (top-down) on the Note's six points, one level per merge (sections 4 and 6).
  - `images/proximity.py`, Plotly: section 7's proximity matrix of the five points (distances asserted), the closest pair outlined, then the 4 x 4 matrix after the merge with question marks where a linkage rule is needed.
  - `images/memory.py`, Plotly (log scales): memory for the n × n matrix at 8 bytes per distance, from the 200 customers (320 KB) to a million points (8 TB), against 16 GB of RAM (section 11).
- **Ladder:** section 7 now shows the matrix and the open question that section 8 answers; section 11's limitation is drawn as a growth curve.
- **Words per visual:** 423 before, 285 after. **Figure share:** 5 of 10 before, 8 of 10 after (sections 5 and 6 point to Figures 1 and 3).
- **Text fixed:** glossary IDs added at first use: G-996, G-893, G-180, G-630, G-582, G-1585, G-715, G-1104, G-1811, G-427, G-236, G-2099. Figures renumbered.
- **New Key terms:** none.

## 132-dbscan

- **Visuals added**
  - `images/outlier_mean.py`, Plotly: section 3.2's example, nine points around (0, 0) (a 3 x 3 grid of our own) and one outlier at (20, 20) pulling the mean to (2, 2) (asserted).
  - `images/eps_count.py`, Plotly: section 5's example on the Note's 14 animation points with eps = 1 and MinPts = 3: 4 points within eps around (1, 1), dense; 2 around (2.7, 2.3), sparse (counts asserted; they match the numbers the text already used).
  - `images/chains.py`, Plotly: section 7's density-connected points on the same 14 points (eps = 1, min_samples = 4): chains of core points, dotted links to border points, two clusters and two noise points (scikit-learn's result asserted).
- **Ladder:** sections 3, 5 and 7 now each show their idea on points before or beside the definition.
- **Words per visual:** 362 before, 246 after. **Figure share:** 6 of 12 before, 9 of 12 after (section 4, a short definition, section 10, a list of strengths, and section 13, the instructions for the Dash app, have no figure).
- **Text fixed:** glossary IDs added at first use: G-548, G-1374, G-772, G-368, G-588, G-584, G-1396, G-697, G-698, G-1231, G-486, G-323, G-1329, G-589, G-994. Figures renumbered; the two citations of the hierarchical clustering Note's Figure 2 kept.
- **New Key terms:** none.

## 133-imbalanced-data

- **Visuals added** (the first three use the Note's own `make_classification` data through `images/imb.py`, with counts asserted)
  - `images/class_counts.py`, Plotly: observations per class, 299 and 21 in training, 73 and 7 in testing (section 2.1).
  - `images/confusion.py`, Plotly: the confusion matrices behind section 3.2's accuracy trap, logistic regression (92.5%, 1 of 7 found) and the always-class-1 model (91.25%, 0 of 7).
  - `images/resample_counts.py`, Plotly: the training set's class counts before and after random undersampling, random oversampling and SMOTE (21/21, 299/299, 21 real + 278 synthetic) (section 6).
  - `images/tradeoff.py`, Plotly: section 10's table as minority precision against minority recall, with an arrow from each model to its fixed version.
- **Ladder:** sections 2, 3.2, 6 and 10 now each show their numbers as a picture before the discussion.
- **Words per visual:** 523 before, 335 after. **Figure share:** 6 of 10 before, 9 of 10 after (section 4, a table of application areas, has no figure).
- **Text fixed:** glossary IDs added at first use: G-921, G-1374, G-772, G-1949, G-1145, G-1229, G-1619, G-1613, G-1825, G-964, G-1429, G-922, G-256, G-493, G-523, G-865, G-887. Figures renumbered.
- **New Key terms:** none.

## 14-framing-ml-problem

- **Visuals added:** none. The Note already has a figure in every one of its 11 sections (12 TikZ diagrams).
- **Words per visual:** 190 before and after. **Figure share:** 11 of 11 before and after.
- **Text fixed:** glossary IDs added at first use: G-802, G-387, G-386, G-1374, G-772, G-533, G-1378, G-1215, G-1547, G-1641, G-1655, G-1949, G-265, G-1391.
- **New Key terms:** none.

## 16-working-with-json-and-sql

- **Visuals added**
  - `images/json_anatomy.tex`, TikZ: the first record of `data/train.json` (id 10259, greek) labelled as an object of key-value pairs with an array value (section 2).
  - `images/world_tables.tex`, TikZ: the three tables of the `world` database with their row counts (from `data/world.db`) and the `CountryCode` links to `country.Code` (section 6).
- **Ladder:** section 2 now shows a real JSON object before the syntax list; section 6 shows the database's structure next to its table.
- **Words per visual:** 309 before, 234 after. **Figure share:** 5 of 8 before, 7 of 8 after (section 3, a two-paragraph definition, has no figure).
- **Text fixed:** glossary IDs added at first use: G-987, G-204, G-1857, G-544, G-543, G-2130, G-1493, G-1859, G-130. Figures renumbered.
- **New Key terms:** none.

## 17-fetching-data-from-api

- **Visuals added**
  - `images/normalize.tex`, TikZ: the first show of the saved TVmaze reply (`data/tvmaze_shows_page0.json`, "Under the Dome", rating 6.6) through `pd.DataFrame` (the rating dictionary stuck in one cell) and `pd.json_normalize` (a `rating.average` column holding 6.6) (section 6).
- **Ladder:** section 6 now shows the result of the code, not only the code.
- **Words per visual:** 298 before, 256 after. **Figure share:** 6 of 9 before, 7 of 9 after (section 2, a definition, and section 9, a list of resources, have no figure).
- **Text fixed:** glossary IDs added at first use: G-204, G-205, G-1674, G-1686, G-1886, G-99. Figures renumbered.
- **New Key terms:** none.

## 19-understanding-your-data

- **Visuals added**
  - `images/dtype_memory.py`, Plotly: section 5.2's four small-number Titanic columns as int64 and int8, measured with pandas on `data/titanic_train.csv` (28,512 against 3,564 bytes, asserted).
  - `images/duplicates.tex`, TikZ: section 8's example with the first two real passengers added again as rows 891 and 892, marked True by `duplicated()`.
- **Ladder:** sections 5.2 and 8 now show their result as a picture after the code.
- **Words per visual:** 413 before, 310 after. **Figure share:** 5 of 9 before, 7 of 9 after (section 2, the column table, and section 3, `df.shape`, have no figure).
- **Text fixed:** glossary IDs added at first use: G-1374, G-1949, G-772, G-540, G-1337, G-1871, G-1483, G-1602, G-648, G-490, G-1474. Figures renumbered.
- **New Key terms:** none.

## 20-univariate-analysis

- **Visuals added:** none. The Note already has 9 figures, one for every graph type it teaches, on the Titanic data.
- **Words per visual:** 271 before and after. **Figure share:** 8 of 9 before and after.
- **Text fixed:** glossary IDs added at first use: G-2050, G-310, G-1280, G-2071, G-1374, G-772, G-1949, G-494, G-1495, G-899, G-626, G-587, G-1569, G-329, G-787, G-1420, G-1817.
- **New Key terms:** none.

## 21-bivariate-multivariate-analysis

- **Visuals added:** none. The Note already has 13 figures, one for every plot type it teaches. Its figure numbers were also left unchanged on purpose: Notes 223 and 571 cite its Figures 1 and 6.
- **Words per visual:** 231 before and after. **Figure share:** 10 of 11 before and after.
- **Text fixed:** glossary IDs added at first use: G-1374, G-772, G-1949, G-1749, G-1095, G-258, G-1203, G-446, G-329, G-1005, G-886, G-511, G-402, G-582, G-1437, G-1088, G-1500.
- **New Key terms:** none.

## 210-statistics-roadmap

- **Visuals added**
  - `images/three_uses.tex`, TikZ: the three places statistics shows up in data work (understanding data, algorithms, decisions), with the Note's examples (section 2).
- **Ladder:** a roadmap Note; section 2 now shows its three-part list as a picture.
- **Words per visual:** 424 before, 284 after. **Figure share:** 2 of 4 before, 3 of 4 after (section 4, study advice, has no figure).
- **Text fixed:** glossary IDs added at first use: G-1884, G-596, G-1571, G-944, G-772, G-1374, G-1620, G-1525, G-1731, G-364, G-913. Figures renumbered.
- **New Key terms:** none.

## 22-pandas-profiling

- **Visuals added**
  - `images/build_flow.tex`, TikZ: section 2.2's three lines of code as a flow, CSV to DataFrame to report object to web page.
  - `images/report_to_tasks.tex`, TikZ: section 9's way of using the report, read in order, write down observations (the Note's two examples), turn them into tasks.
- **Ladder:** sections 2.2 and 9 now show their steps as a picture next to the numbered list.
- **Words per visual:** 309 before, 258 after. **Figure share:** 6 of 9 before, 8 of 9 after (section 8, the Sample tab, has no screenshot in the Notebook's set).
- **Text fixed:** "every figure from Figure 2 onwards is a screenshot" would have become wrong once diagrams were added; it now says Figures 3 to 11. Glossary IDs added at first use: G-1440, G-1593, G-904. Figures renumbered.
- **New Key terms:** none.

## 220-what-is-statistics

- **Visuals added**
  - `images/two_branches.tex`, TikZ: descriptive statistics (the 891 Titanic fares summarised) against inferential statistics (a sample to a statement about the population) (section 3).
  - `images/biased_sample.py`, Plotly: why a sample must be random, on the real Titanic fares. 1,000 random samples of 50 centre on the population mean 32.2; one sample of 50 first-class passengers has mean 72.6 (seed 0; asserted) (section 4.1).
- **Ladder:** section 3 now shows the two branches side by side before the population/sample idea; section 4.1's "random" requirement is demonstrated on data.
- **Words per visual:** 493 before, 298 after. **Figure share:** 3 of 6 before, 4 of 6 after (section 2, a definition with examples, and section 5, a list of later tools, have no figure).
- **Text fixed:** glossary IDs added at first use: G-1884, G-596, G-944, G-943, G-1525, G-1731, G-1737, G-1734, G-1738, G-1880, G-913, G-1883, G-446, G-203, G-381, G-772, G-1374, G-1330, G-1403, G-616, G-465. Figures renumbered. "Parameter" in the statistics sense was left without an ID: the glossary's "Parameter" (G-1448) is a function argument.
- **New Key terms:** none new in this Note, but see "Glossary notes" below.

## 221-measures-of-central-tendency

- **Visuals added**
  - `images/trim_example.py`, Plotly (log scale): section 7's worked example, the 10 class salaries with the two cut values marked, the trimmed mean 34.375 and the plain mean 230.3 (asserted with `scipy.stats.trim_mean`).
- **Ladder:** section 7's worked example is now drawn.
- **Words per visual:** 313 before, 262 after. **Figure share:** 5 of 8 before, 6 of 8 after (section 2, a definition, and section 8, the comparison table, have no figure).
- **Text fixed:** glossary IDs added at first use: G-1205, G-772, G-1374, G-1203, G-1524, G-1725, G-1209, G-1251, G-296, G-1275, G-2117, G-2111, G-2017, G-2018, G-844, G-880.
- **New Key terms:** none.


## Summary across the 43 Notes

- **Visuals:** 232 before, 328 after: 96 new figures and animations (7 of them animated GIFs with frame grids). Tools: Plotly for data and charts, Plotly frames for processes, TikZ for structure. No matplotlib, no Manim renders were needed.
- **Targets:** every Note now has at most 400 words per visual and a figure in at least 60% of its numbered sections. Before this round, 27 Notes were above 400 words per visual and 20 were below 60% figure share.
- **Data:** every new figure uses the Note's own data or numbers, and its script asserts them (against the Note's CSV files, the Notebook's printed values, or the worked example in the text). Two small CSV files were added: `1057-rnn-sentiment-analysis/data/pad_examples.csv` (review lengths from `keras.datasets.imdb.load_data`) and `1068-encoder-decoder/data/pair_lengths.csv` (pair lengths recomputed with the Notebook's own filtering and seeds). No Keras model was retrained.
- **Builds:** all 43 Notes rebuilt with `tools/build.sh` and printed "Built". Every new figure, frame grid and the PDF page where it sits was looked at; overlaps, clipped labels and figures that pandoc had made inline (a text line straight after the image) were fixed.

| Note | Visuals before | after | Words per visual before | after | Sections with a figure before | after |
|---|---|---|---|---|---|---|
| 1054-keras-functional-api | 5 | 9 | 413 | 246 | 3/4 | 4/4 |
| 1055-why-rnn | 4 | 7 | 494 | 293 | 4/6 | 4/6 |
| 1056-rnn-forward-propagation | 4 | 6 | 450 | 306 | 4/6 | 6/6 |
| 1057-rnn-sentiment-analysis | 5 | 7 | 436 | 316 | 4/6 | 6/6 |
| 1058-types-of-rnn | 5 | 7 | 293 | 216 | 4/6 | 6/6 |
| 1060-problems-with-rnn | 4 | 7 | 578 | 341 | 3/5 | 5/5 |
| 1063-lstm-next-word-prediction | 5 | 8 | 500 | 322 | 4/8 | 6/8 |
| 1068-encoder-decoder | 5 | 9 | 580 | 331 | 5/8 | 8/8 |
| 1069-attention-mechanism | 4 | 8 | 542 | 278 | 4/8 | 7/8 |
| 1072-what-is-self-attention | 3 | 6 | 498 | 251 | 3/5 | 5/5 |
| 1073-self-attention-step-by-step | 6 | 9 | 484 | 324 | 4/8 | 7/8 |
| 1074-scaled-dot-product-attention | 5 | 8 | 315 | 199 | 3/6 | 6/6 |
| 1075-self-attention-geometric-intuition | 6 | 7 | 236 | 206 | 5/6 | 6/6 |
| 1076-why-self-attention | 3 | 5 | 383 | 232 | 3/5 | 5/5 |
| 1078-positional-encoding | 5 | 8 | 483 | 305 | 4/7 | 7/7 |
| 1079-layer-normalization | 4 | 7 | 481 | 277 | 3/6 | 6/6 |
| 1081-masked-self-attention | 6 | 9 | 474 | 318 | 4/7 | 7/7 |
| 1084-transformer-inference | 5 | 6 | 376 | 315 | 5/6 | 6/6 |
| 1086-meaning-as-direction | 3 | 6 | 581 | 293 | 3/6 | 6/6 |
| 1087-decoder-only-gpt | 5 | 9 | 590 | 331 | 4/8 | 8/8 |
| 1088-unembedding-and-sampling | 4 | 7 | 533 | 306 | 3/6 | 6/6 |
| 109-random-forest-bias-variance | 3 | 4 | 330 | 250 | 3/4 | 4/4 |
| 1090-superposition | 5 | 8 | 489 | 306 | 4/7 | 7/7 |
| 11-tensors | 9 | 9 | 160 | 160 | 5/6 | 5/6 |
| 115-adaboost-intuition | 3 | 6 | 528 | 273 | 3/6 | 6/6 |
| 119-bagging-vs-boosting | 2 | 4 | 474 | 244 | 2/4 | 4/4 |
| 12-setup-anaconda-jupyter-colab | 9 | 10 | 436 | 393 | 9/9 | 9/9 |
| 127-stacking-blending | 6 | 8 | 426 | 320 | 5/9 | 7/9 |
| 128-kmeans-intuition | 3 | 5 | 508 | 309 | 2/4 | 3/4 |
| 13-toy-project | 6 | 8 | 261 | 207 | 6/10 | 8/10 |
| 131-hierarchical-clustering | 6 | 9 | 423 | 285 | 5/10 | 8/10 |
| 132-dbscan | 6 | 9 | 362 | 246 | 6/12 | 9/12 |
| 133-imbalanced-data | 7 | 11 | 523 | 335 | 6/10 | 9/10 |
| 14-framing-ml-problem | 12 | 12 | 190 | 190 | 11/11 | 11/11 |
| 16-working-with-json-and-sql | 6 | 8 | 309 | 234 | 5/8 | 7/8 |
| 17-fetching-data-from-api | 6 | 7 | 298 | 256 | 6/9 | 7/9 |
| 19-understanding-your-data | 6 | 8 | 413 | 310 | 5/9 | 7/9 |
| 20-univariate-analysis | 9 | 9 | 271 | 271 | 8/9 | 8/9 |
| 21-bivariate-multivariate-analysis | 12 | 12 | 231 | 231 | 10/11 | 10/11 |
| 210-statistics-roadmap | 2 | 3 | 424 | 284 | 2/4 | 3/4 |
| 22-pandas-profiling | 10 | 12 | 309 | 257 | 6/9 | 8/9 |
| 220-what-is-statistics | 3 | 5 | 493 | 298 | 3/6 | 4/6 |
| 221-measures-of-central-tendency | 5 | 6 | 313 | 262 | 5/8 | 6/8 |

## Glossary notes (for the merge on the other machine)

I did not run `tools/merge_glossary.py` or edit `glossary.md`. No Note gained a new Key term. These existing Key terms have no glossary ID, or share a name with an entry that means something else, so I left them without an ID in the text:

- **Query** (attention sense) in Notes 1073, 1075 and 1076: the glossary's "Query" (G-1606) is an SQL query. Key and Value have their attention meanings (G-1011, G-2068), so Query needs its own entry.
- **Inference** (using a trained model) in Notes 1081 and 1084: G-943 "Inference" is the statistical meaning (Note 220) and G-941 is "inference vs prediction".
- **Projection** (multiplying an embedding by W_Q, W_K or W_V) in Note 1075: G-1583 is the geometric projection onto a line.
- **Convergence (k-means)** in Note 128: G-472 is the convergence of the iterative imputer.
- **Parameter** (a number describing a population) in Note 220: G-1448 is a function argument.
- **Sparsity S** in Note 1090: G-1849 is "many coefficients exactly 0".
- **Lookup table** (the embedding layer) in Note 1072: G-1128 is Naive Bayes' stored probabilities.
- **Zero padding (text)** in Note 1055: G-2146 is zero padding of images; the text now points to "padding" (G-1436).
- **Bigram** and **Baseline** in Note 1063 have no glossary ID at all.

While auditing, I found that I had first attached ten IDs with the wrong meaning (G-472, G-808, G-1128, G-1448, G-1583, G-1606, G-1753, G-2146, G-1849, and G-943 in Note 1084). All were removed or replaced before the final build, and the entries above reflect the final state.

## Cross-references outside my list

- `1004-perceptron/note.md`, line 222, cites "the [toy project Note](../13-toy-project/note.md) (Figure 5)" for the decision-region plot. After this round that figure is **Figure 7** of Note 13. I did not edit Note 1004, since it is outside my list.
- Notes 223 and 571 cite Figures 1 and 6 of Note 21. Note 21's figures were not renumbered, so those citations still hold.
- Within my list, two citations in Note 132 of Note 131's Figure 2, and the citations of Holtzman et al.'s Figure 4 (Note 1088) and Vaswani et al.'s Figures 1 and 2 (Note 1081), were checked after renumbering and are correct.
