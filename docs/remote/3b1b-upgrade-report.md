# Report: 3Blue1Brown upgrades for Notes 1067–1085

All 19 Notes from 1067 to 1085 build: `CAMPUSX_ENV=~/miniforge3/envs/campusx tools/build.sh <folder>` printed "Built" for each, in a final pass over all of them. I looked at every new `_frames.png` grid and at the PDF page where each new figure sits, and fixed overlaps and clipped labels before moving on. Every new GIF is under 3 MB (the largest is the 1085 capstone, 2.7 MB). Every `data/` folder stays under 80 KB.

## Things to know first

- **Chrome.** Plotly's image export found no Chrome here, so I set `BROWSER_PATH` to the existing Puppeteer copy (`~/.cache/puppeteer/chrome/linux-147.0.7727.57/chrome-linux64/chrome`), as the earlier session did. I installed nothing. The build machine needs Chrome or the same variable.
- **The GPT-2 parameter count in `docs/3b1b-transformers.md` is wrong.** It gives 124,412,160. That number leaves out the 12 `h.N.attn.c_attn.bias` tensors (27,648 numbers), because a filter on names ending in `attn.bias` also catches them. The correct count of learned parameters is **124,439,808**, with only the 12 mask buffers `h.N.attn.bias` left out. The 1067 Notebook counts it from the file header and checks it with an assert.
- **The W₁/W₂ wording in the task is transposed for our Notes.** The task says "W₁ rows are questions, W₂ columns are what gets written". That holds for 3Blue1Brown's convention, where the matrix multiplies a column vector. Our Notes follow the paper and write the vector as a row, $xW_1$. In that form the questions are the *columns* of $W_1$ and the written directions are the *rows* of $W_2$. The 1080 box states our version and explains that his is the same thing transposed.
- **Retraining the 1084 model.** The trained model of 1084 was never saved, so I appended a section 8 to its Notebook. It trains the same model again from seed 0 and exports the data for the 1081 grid and the 1085 capstone. GPU training does not repeat to the last bit: this run scored test BLEU 40.6, against 41.4 in the original run. Its translation of "we're friends ." is the same. I ran only the new cells, after the set-up cells, so the stored outputs and numbers of sections 1 to 7 are unchanged and still match the Note.
- **An existing 1077 Notebook cell fails on this GPU.** Section 2's check against Keras fails with a difference of 1e-3, because TF32 is enabled on the GPU. I ran 1077 on the CPU (`CUDA_VISIBLE_DEVICES=""`), where it passes as before. This was already the case before my change. I did not edit that cell.
- **Two links point to Notes that do not exist yet.** They are `../1086-meaning-as-direction/note.md` (from 1072) and `../1089-mlp-stores-facts/note.md` (from 1080), as the task asked. They will stay broken until those Notes land.
- **Large downloads.** The new cells in the 1075 and 1067 Notebooks download the GPT-2 small weights (523 MB) and its tokenizer from Hugging Face on their first run, cached through `keras.utils.get_file`. The 1067 parameter count and the 1077 BERT matrices use byte-range downloads (a few KB and 4.7 MB).
- **How the new data was made.** All new Notebook cells were appended at the end and executed. Their stored outputs have stderr and download progress bars removed.

## Sources opened for this work

- 3Blue1Brown transcripts in `transcripts/3b1b/`. I read Ch 6 from 1:32 to the end; Ch 7 from 7:30 to 13:49; Ch 5 around 15:09 and 16:44; and "LLMs explained briefly" at 0:01 and 3:13.
- Radford et al. 2019 (GPT-2 paper, PDF from cdn.openai.com): Table 2 (117M), §2.3 ("The smallest model is equivalent to the original GPT"; vocabulary 50,257; context 1,024).
- Radford et al. 2018 (GPT-1 paper, PDF): §4.1 (12 layers, 768 dimensions, 12 heads, 40,000 BPE merges; no parameter count).
- Brown et al. 2020 (arXiv:2005.14165): Appendix D, Table D.1 (GPT-3 175B: 3.14E+23 training FLOPs).
- The Hugging Face model card of `openai-community/gpt2` ("the smallest version of GPT-2, with 124M parameters"), plus the safetensors header and weights.
- The BERT-base `model.safetensors` (value and output matrices of layer 0).

## Per Note

### 1067 History of LLMs
- **What changed:**
  - §8 has a new paragraph on the GPT-1 size. The GPT-1 paper gives no count. The 117M figure comes from the GPT-2 paper's smallest model, which that paper calls equivalent to the original GPT. The released weights of that model count 124.4M (124,439,808). Both numbers are given with sources, and the Note says that no source explains the gap.
  - §8, item 3, now gives compute in years: 3.14 × 10²³ FLOPs at 10⁹ operations per second is about 10 million years. It also gives the arithmetic for about 2.5 trillion operations per second per GPU.
  - §9 opens with "A chatbot is a next-word predictor in a script". It shows the prompt format, and the Notebook gives the same chat script to GPT-2 small. GPT-2 answers "Assistant: I'm a French citizen." and then writes the user's next turn itself, which motivates the SFT/RLHF steps.
  - New sources: Brown et al. Table D.1, the GPT-2 model card, and two Sanderson entries. The Radford 2018 and 2019 entries now name their sections.
- **Visuals:** the timeline (TikZ) now has a small architecture sketch above each stage: an LSTM chain into a context vector, attention fan-in, an all-to-all transformer, pre-train then fine-tune, and a block stack with a chat bubble. The caption was updated.
- **Animations:** none. The audit asked for a TikZ still.
- **Removed:** nothing.

### 1068 Encoder–decoder
- **What changed:** a new Figure 2 in §4.1 with one sentence of text before it. The later figure numbers were shifted.
- **Animation:** `context_squeeze.gif` (Manim). Two real test sentences (5 and 8 tokens, from `data/translations.csv`) pass word by word into a fixed-size context vector drawn as coloured slices. Watch the slices get thinner as more words share the same space. The decoder sees only that vector. The caption says it is a picture of the idea, not the LSTM's numbers.
- **Note:** the file is named `context_squeeze.py` because a file called `bottleneck.py` shadows the optional pandas dependency of the same name and breaks `import pandas`.
- **Removed:** nothing.

### 1069 Attention mechanism
- **What changed:** a new Figure 2 at the end of §5.2, with two sentences of text. Later numbers were shifted. The cross-reference to 1070 now says Figure 3, because 1070's numbering moved.
- **Animation:** `attention_fill.gif` (Plotly frames). The trained model's real weights (`data/attention_weights.csv`). The grid fills one French word per frame. On the right are the current word's weights and its context vector written out (for example, "c₅ ≈ 0.88 h_about + …"). Watch the large weight move along the English sentence.
- **Removed:** nothing.

### 1070 Bahdanau vs Luong
- **What changed:** a new Figure 2 in §5.2, with one sentence before it.
- **Animation:** `two_orders.gif` (Manim). One decoder step in each design, built up operation by operation from the bottom. Watch where the green context box lands: below the LSTM step for Bahdanau, above it for Luong. The equations come from the Note's sections 4 and 5.
- **Removed:** nothing.

### 1071 Introduction to transformers
- **What changed:** a new Figure 2 in §5, with one sentence. Later numbers were shifted.
- **Animation:** `race.gif` (Manim). An LSTM lights 6 cells one step at a time; self-attention lights all 6 in one step, with all-to-all links. Then the measured times at 256 words grow as bars (6.28 ms against 1.19 ms, from `data/timing.csv`), followed by the 1,024-word catch-up.
- **Removed:** nothing.

### 1072 What is self-attention
- **What changed:** §3's per-coordinate example ("king = [0.6, 0.2, 1, 0, 0.9]; first number = royalty") was replaced by the direction picture. Each direction is one aspect of meaning; man → woman is roughly king → queen; the dot product reads how much of a direction a word has. The new text links `../1086-meaning-as-direction/note.md` and adds a Sanderson Ch 5 source.
- **Animations:** none. That concept belongs to Note 1086.
- **Removed:** the per-coordinate example, because it pointed the wrong way.

### 1073 Self-attention step by step
- **What changed:**
  - §7 has a new "invented example": the noun "dog" asks for adjectives before it, and "old" and "brown" answer. The worked numbers are $q = (3, 0)$, scores 0, 9, 8.4, 0.6, and weights 0.646 and 0.354 on the two adjectives. It is clearly labelled as invented, following Sanderson's own framing, and points to §9.3 for a real learned pattern.
  - Figure 2 was redrawn as a dot grid.
  - A new Figure 3 was added in §8.1. Later numbers were shifted.
- **Visuals:**
  - `weights_dots.png` (Plotly): the same data as before (`data/weights_simple.csv`), with each dot's area showing the weight.
  - `qkv_arrows.gif` (Manim): e = (1, 2) becomes q, k and v under the Note's three 2 × 2 matrices. The Note says that k and v coincide for this e.
- **Removed:** `weights_simple.png` is no longer linked from the Note. `heatmaps.py` still makes it, and I did not delete the file.

### 1074 Scaled dot-product attention
- **What changed:** a new Figure 4 in §5, with two sentences. The heatmap became Figure 5.
- **Animation:** `saturation_anim.gif` (Plotly frames). One seeded random query and 10 keys, using their first d numbers, for d = 1 to 1,024. The unscaled softmax collapses onto one key while the scaled one stays spread. Under each panel are the Notebook's averages over 2,000 draws (`data/saturation.csv`), so the single draw is not the evidence.
- **Removed:** nothing.

### 1075 Self-attention, geometrically (upgrade 1)
- **What changed:**
  - A new §7.3, "Adding the change back". It covers e + Δe, the link to the residual connection of 1080 §5.2, and the bridge to §7.1 (the change itself still lies between the value vectors). Worked numbers: (7, 3) + (4.97, 4.67) = (11.97, 7.67), turning from 23° to 33° in "money bank"; and (13.68, 6.03) at 24° in "river bank".
  - A GPT-2 small measurement: in blocks 2 to 11, the change is 9 to 25 percent of the vector's length, with cosine at least 0.97.
  - An Extra box crediting Sanderson, a summary bullet, two sources and one key term.
  - Stills inside §4–6 (the audit's proposal).
- **Animations and figures:**
  - `residual_nudge.gif` (Manim): the Note's own numbers. The weighted value vectors are placed tip to tail at the tip of e_bank, giving Δe, then e + Δe, for both sentences. Watch the same grey arrow receive a different purple change.
  - `gpt2_delta.png` (Plotly): real GPT-2 small (`data/gpt2_delta.csv`) on "He sat on the river bank" and "She works at the money bank".
  - `stills_projections.png`, `stills_scores.png`, `stills_sum.png` (Plotly): three frames of the existing animation, made by the same code.
- **Removed:** nothing. The sentence "The embeddings themselves are not used again" now ends "…inside the attention computation", since §7.3 reuses them.

### 1076 Why self-attention
- **What changed:** a new Figure 2 in §4, with one sentence. The weights figure became Figure 3.
- **Visual:** `three_equations.png` (TikZ). Luong's three equations and self-attention's, row by row. Only the query (blue), key (orange) and value (green) symbols are coloured.
- **Removed:** nothing.

### 1077 Multi-head attention (upgrade 2)
- **What changed:**
  - §5.3 gained the identity [Z₁ Z₂]W_O = Z₁W_O¹ + Z₂W_O², with the Notebook's numbers: head 1's change for "money" is (1.66, 1.19, 1.27, −0.92), head 2's is (1.00, 0.50, 0.50, 2.50), and their sum is the output (2.66, 1.69, 1.77, 1.58). It is linked to 1075 §7.3.
  - A new §5.4, "Each head's value map is low rank". W_V^i (value down) times head i's rows of W_O (value up) has rank at most d_v. In BERT-base layer 1, all 12 heads have exactly 64 non-zero singular values, and the 65th is below 10⁻⁷. The section compares 98,304 numbers against 589,824, uses the paper's names and mentions Sanderson's names once.
  - A summary bullet and a source were added. Later figure numbers were shifted.
- **Visuals:**
  - `heads_wo.gif` (Manim): the 2-head "money bank" example. Each head's weights and output, the concatenation times W_O, then the same result as one change per head, added up. This covers the audit's "heads in parallel, then concat" proposal.
  - `value_rank.png` (Plotly): the singular values of the 12 BERT heads (`data/bert_value_svals.csv`).
- **New data:** `data/wo_split.csv`, `data/bert_value_svals.csv`.
- **Removed:** nothing.

### 1078 Positional encoding
- No change. There was no task item and no audit proposal. It was rebuilt only as a check.

### 1079 Layer normalisation
- **What changed:** a new Figure 4 at the end of §6.1, with one sentence.
- **Animation:** `norm_axes.gif` (Manim). The Note's padded batch from §5.1. Batch normalisation sweeps the columns, with means 3.99, 4.28 and 3.50 against 5.32, 5.70 and 4.67 over the real words. Layer normalisation sweeps the rows, and the padding rows stay 0. The values are computed as Keras does (ε = 0.001).
- **Removed:** nothing.

### 1080 Transformer encoder (upgrades 1 and 5)
- **What changed:**
  - §5.2 has a new paragraph, "Attention as a change", linking 1075 §7.3.
  - §5.3 ends with an Extra box on how to read $W_1$ and $W_2$ (Sanderson 2024 Ch 7; Geva et al. 2021). It explains the convention (see "Things to know first") and links `../1089-mlp-stores-facts/note.md`.
  - A new Figure 3 was added in §5.4, and the collapse figure became Figure 4.
  - Two Sanderson sources were added.
- **Animation:** `block_values.gif` (Manim). The Note's tiny-block numbers for "how": x plus the attention change z, LayerNorm, the hidden layer with the 2 ReLU zeros outlined, plus the network's change y, then LayerNorm.
- **Removed:** nothing.

### 1081 Masked self-attention (section 2 animation)
- **What changed:** a new Figure 2 in §4.3 and a new Figure 5 in §6.3, each with text saying what to watch. There is an Extra box on Sanderson's columns against our rows, and a source. Later numbers were shifted.
- **Animations:**
  - `trained_grid.gif` (Manim): head 1 of the first decoder block of the retrained 1084 model, on `<start> comment ça va ?` (`data/trained_grid.csv`, exported by the 1084 Notebook, section 8). It goes from raw q·k dots, to division by √32, to the −∞ mask, to the softmax of each row. Watch every dot shrink by the same factor, then the upper triangle blank out.
  - `train_infer_anim.gif` (Plotly frames): the same weights. Training fills every row at once; inference adds one row per step, with the same numbers. This was the audit's §4 proposal.
- **Head choice:** I fixed head 1 in advance and did not pick it for looks. The script names the head.
- **Removed:** nothing.

### 1082 Cross-attention
- **What changed:** a new Figure 2 before §7, with one sentence. The heatmap became Figure 3.
- **Animation:** `cross_fill.gif` (Plotly frames). This Note's own trained model (1 + 1 blocks, `data/cross_weights.csv`). The grid fills one French position per frame, with that query's weights over the English words.
- **Removed:** nothing.

### 1083 Transformer decoder
- **What changed:** a new Figure 3 at the start of §6, with a paragraph saying what to watch.
- **Animation:** `decoder_flow_anim.gif` (Manim). The position "sommes" goes through the last decoder block of the trained 1084 model: masked self-attention over the French words so far (0.66, 0.20, 0.14), cross-attention (0.85 on "friends"), the feed-forward network, then the output ("amies", 0.987).
- **New data:** `data/decoder_step.json`, copied from 1085's `capstone.json` with its source named.
- **Removed:** nothing.

### 1084 Transformer inference
- **What changed:** three stills with captions and a sentence each: §4 (Figure 2), §5 (Figure 3) and §7 (Figure 5). The decode GIF became Figure 4.
  - The §4 text says plainly that the validation loss stops improving after about 10 epochs and then creeps up slightly.
- **Visuals:** `training_curve.png`, `step1.png` and `mask_bleu.png` (Plotly), from the Note's existing data. This answers the audit's request for "frames in sections 3–7". §3 is a comparison table and kept no figure.
- **Notebook:** a new section 8, the retrain and export described above.
- **Removed:** nothing.

### 1085 Transformer end to end (section 2 capstone)
- **What changed:** at the start of §4, a paragraph saying what to watch and a new Figure 3, plus a Sanderson Ch 5 source.
- **Animation:** `capstone.gif` (Manim). "we're friends ." through the retrained 1084 model (`data/capstone.json`):
  - each English word as a strip of 128 numbers after the embedding, then after each encoder block, with the blocks' self-attention as dots;
  - then 5 decoder runs, each showing the masked self-attention of the newest word, cross-attention lines to the English strips, the top 5 next words, and the chosen word appended;
  - the result is "nous sommes amies .".
- **A choice to know about:** the capstone uses the small trained model, not the base model of §4, because only a trained model gives meaningful weights. The paragraph says so.
- **Removed:** nothing.

## Not done
- The smaller suggestions in `docs/3b1b-transformers.md` §6 that are not on the task list were left out: the "murderer was" framing for 1084, the layer-wise "deeper means more abstract" evidence for 1080 §7.3, and the colour rule across all figures.
- 1085 §9 still says "GPT grew from 117 million parameters". That number is what the GPT-2 paper reports, and 1067 now explains it, so I left 1085 as it was.
