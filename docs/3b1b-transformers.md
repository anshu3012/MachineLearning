# 3Blue1Brown on transformers: what to take for Notes DL-067–DL-086

**Key point:** 3Blue1Brown's 4 transformer videos (plus 1 on cross-entropy) teach about 15 ideas that no Note owns. The four biggest gaps:
1. The **decoder-only GPT** model itself (no Note walks through it).
2. The **unembedding / logits / temperature** step that turns the last vector into a sampled token.
3. **Meaning as direction** in embedding space (king − man + woman, the plural direction).
4. The **MLP as a fact store**, plus **superposition**.

His best visual idea is to draw attention as an **adjustment Δe added to a word's vector**. Our Notes draw it as "replace the word by a weighted mix". His version is clearer and fits the residual stream.

Everything below was checked against the transcripts in `transcripts/3b1b/`. Video IDs, titles, lengths and lesson URLs were checked with yt-dlp and curl on 2026-10-03.

> **Caveat on visuals:** the descriptions of his animations come from his narration and the chapter timestamps. We did not inspect the video frames. Before recreating an animation, watch that timestamp once.

---

## 1. Videos found

Playlist "Neural networks" (PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi), listed with `yt-dlp --flat-playlist`. It has 10 videos; the 5 that matter here:

| # | ID | Title (exact) | Length | Uploaded | Lesson page (HTTP 200) | Transcript |
|---|---|---|---|---|---|---|
| B | LPZh9BOjkQs | Large Language Models explained briefly | 7:58 | 2024-11-20 | 3blue1brown.com/lessons/mini-llm | `transcripts/3b1b/llms-explained-briefly.txt` |
| 5 | wjZofJX0v4M | Transformers, the tech behind LLMs \| Deep Learning Chapter 5 | 27:14 | 2024-04-01 | 3blue1brown.com/lessons/gpt | `transcripts/3b1b/ch5-gpt.txt` |
| 6 | eMlx5fFNoYc | Attention in transformers, step-by-step \| Deep Learning Chapter 6 | 26:10 | 2024-04-07 | 3blue1brown.com/lessons/attention | `transcripts/3b1b/ch6-attention.txt` |
| 7 | 9-Jl0dxWQs8 | How might LLMs store facts \| Deep Learning Chapter 7 | 22:43 | 2024-08-31 | 3blue1brown.com/lessons/mlp | `transcripts/3b1b/ch7-mlp-facts.txt` |
| CE | GlYgs6v2YfU | But what is cross-entropy? \| Compression is Intelligence Part 2 | 33:51 | 2026-07-16 | 3blue1brown.com/lessons/cross-entropy | `transcripts/3b1b/cross-entropy.txt` |

- **Titles:** the current YouTube titles are "…step-by-step" (Ch 6) and "Transformers, the tech behind LLMs" (Ch 5). The older names "Attention in transformers, visually explained" and "But what is a GPT?" are no longer used, so cite the current ones.
- **Not taken:** chapters 1–4 (basic networks and backprop, already covered); "AI images and videos" (a Welch Labs guest video on diffusion); "Reinventing Entropy | Compression is Intelligence Part 1" (l6DKRf-fAAM, 32:19, lessons/entropy). Part 1 is background for CE and is not in the playlist. No transcript was fetched for it.
- **Transcripts:** all five come from the official English subtitles (`--write-subs --sub-langs en`), so Whisper was not needed. Each `.txt` has a `[m:ss]` marker about every 30 s. The `.desc` files hold each video's description with its official chapter list.
- **Tool note:** the yt-dlp in `~/.local/bin` (2024.10.22, Python 3.8) can no longer read YouTube playlists ("0 items of 10"). Use the campusx env one: `/media/anshu/z/miniforge3/envs/campusx/bin/yt-dlp` (2026.08.19).

### Citation form (for Sources sections)
- Sanderson, G. (3Blue1Brown), "Large Language Models explained briefly", 2024, 3blue1brown.com/lessons/mini-llm
- Sanderson, G. (3Blue1Brown), "Transformers, the tech behind LLMs | Deep Learning Chapter 5", 2024, 3blue1brown.com/lessons/gpt
- Sanderson, G. (3Blue1Brown), "Attention in transformers, step-by-step | Deep Learning Chapter 6", 2024, 3blue1brown.com/lessons/attention
- Sanderson, G. (3Blue1Brown), "How might LLMs store facts | Deep Learning Chapter 7", 2024, 3blue1brown.com/lessons/mlp
- Sanderson, G. (3Blue1Brown), "But what is cross-entropy? | Compression is Intelligence Part 2", **2026**, 3blue1brown.com/lessons/cross-entropy

There is already a precedent for crediting him, in the maths Notes: an Extra box saying "The geometric pictures in this Note … follow Sanderson's *Essence of Linear Algebra* (3Blue1Brown)", plus a Sources entry. Use the same pattern here. In the text, the short tag is "(Sanderson 2024, Ch 6)". NOTE-RULES' ban on "mentioning a video" is about the CampusX lecture. 3b1b is cited as a source, never narrated.

---

## 2. What each video teaches, in its order (a)

### B. Large Language Models explained briefly (7:58)
| Time | Idea |
|---|---|
| 0:01 | A chatbot is a torn movie script plus a next-word machine, run again and again |
| 0:33 | An LLM gives a **probability to every possible next word**. Chatbot = setup text + user text + repeated prediction |
| 1:07 | Picking less likely words at random reads more naturally, so the same prompt gives different answers (**sampling**) |
| 1:39 | Scale of GPT-3's training data: 2,600 years of non-stop reading |
| 1:39 | Parameters are dials; "large" means hundreds of billions of them |
| 2:10 | Training: random start; feed all but the last word; nudge the weights by backprop so the true last word becomes more likely |
| 3:13 | Scale of compute: over 100 million years at 10⁹ operations per second, for the largest models |
| 3:45 | Pre-training is different from being an assistant, hence RLHF |
| 4:18 | GPUs; models before 2017 read one word at a time; a transformer "soaks it all in at once" |
| 4:49 | Words become lists of numbers (embeddings) |
| 4:49 | Attention lets the vectors "talk" and refine meaning: "bank" becomes riverbank |
| 5:21 | The feed-forward network adds capacity to store patterns |
| 5:53 | Many rounds of both; the **last vector** gives the next-word distribution |
| 6:28 | The behaviour emerges from training, so it is hard to interpret |

### Ch 5. Transformers, the tech behind LLMs (27:14)
| Time | Idea |
|---|---|
| 0:00 | GPT = Generative Pre-trained Transformer |
| 0:31 | Transformers for speech, text-to-speech, text-to-image and translation (2017) |
| 1:31 | **Predict → sample → append → repeat.** GPT-2 writes nonsense stories; GPT-3, the same design but bigger, writes coherent ones |
| 3:06 | Tokens: words, pieces of words, image patches, chunks of sound |
| 3:37 | Each token gets a vector; similar meanings sit close together |
| 3:37 | Attention block: "model" in "machine learning model" vs "fashion model" |
| 4:38 | MLP block: every vector goes through the same operation in parallel, "like asking a long list of questions" |
| 5:10 | Repeat the blocks; the last vector gives a distribution over tokens |
| 5:42 | Chatbot = **system prompt** + user prompt + continuation |
| 7:16 | The premise of ML: tunable parameters (shown with linear regression) |
| 8:52 | The deep-learning format: data as arrays (tensors); weights touch data only through **weighted sums** (matrix–vector products); non-linearities in between |
| 10:58 | GPT-3: 175B weights in just under 28,000 matrices of 8 kinds; a **running parameter tally** follows |
| 12:01 | Colour rule: **weights in blue/red, data in grey** |
| 12:31 | Embedding matrix W_E, one column per token |
| 13:33 | 12,288 dimensions; a 3-D slice shows the space; directions carry meaning; nearest neighbours of "tower" |
| 15:09 | woman − man ≈ queen − king (only roughly; family relations work better); Italy − Germany + Hitler ≈ Mussolini; Germany − Japan + sushi ≈ bratwurst |
| 16:44 | **Dot product = alignment.** cats − cat as a "plural direction": plurals score higher, and one, two, three, … score higher and higher |
| 17:44 | W_E = 50,257 × 12,288 ≈ 617M weights |
| 18:14 | Vectors "soak in context": "king" ends as "a Scottish king who murdered his predecessor, in Shakespearean language". The first lookup ignores context |
| 19:49 | **Context size** 2,048 tokens; early ChatGPT "lost the thread" in long chats |
| 20:22 | **Unembedding W_U** maps the last vector to 50k logits (the Harry Potter → "Snape" example). In training, every position predicts its next token |
| 22:31 | Softmax |
| 24:04 | **Temperature T**: high T flattens the distribution, low T sharpens it, T = 0 is argmax. GPT-3 stories at different T; the API caps T at 2 |
| 25:42 | The raw outputs are called **logits** |

### Ch 6. Attention in transformers, step-by-step (26:10)
| Time | Idea |
|---|---|
| 0:00 | Recap: directions carry meaning (gender) |
| 1:32 | "mole" ×3 (animal, chemistry unit, skin): the same first vector; attention computes **what to add** to move it to the right meaning |
| 2:38 | tower → Eiffel tower → miniature Eiffel tower. Information can move over long distances |
| 3:43 | "…therefore the murderer was": the last vector must hold everything needed to predict |
| 4:16 | Toy: "a fluffy blue creature roamed the verdant forest"; one head where adjectives update nouns |
| 4:47 | Embeddings encode position as well |
| 6:22 | **Query** = "are there adjectives in front of me?", made by W_Q, in 128 dimensions |
| 7:27 | **Key** = "I'm an adjective, here"; keys match queries when they align |
| 8:30 | **Grid of dots**, dot size = query·key; scores range over −∞…∞ |
| 9:32 | Softmax **per column** gives the "attention pattern"; then the paper's formula softmax(QKᵀ/√d_k)V |
| 10:35 | √d_k "for numerical stability" |
| 11:05 | Training predicts every next token at once, so later tokens must not leak. **Masking**: set them to −∞ *before* the softmax so the columns still sum to 1. GPT always masks |
| 12:42 | The pattern has context² entries, a bottleneck for long contexts |
| 13:12 | **Value vector** = "what should be added to the other word if I am relevant to it" |
| 14:45 | Weighted sum of values in each column = **Δe**, *added* to the original embedding |
| 15:49 | Tally: W_Q and W_K are 128 × 12,288, about 1.5M each |
| 16:20 | A full value map would be 12,288² ≈ 150M; it is factored as **value-down × value-up** (low rank) |
| 17:55 | 6.3M parameters per head |
| 18:27 | **Cross-attention**: keys and queries come from different data; no mask |
| 19:28 | Many kinds of context update ("they crashed the car"; Harry + wizard vs Harry + Queen/Sussex/William), so many heads |
| 20:31 | Multi-head: 96 heads; **each head proposes a Δe; the proposals are summed** and added |
| 22:03 | About 600M parameters per attention block |
| 22:34 | **W_O = all value-up matrices stapled together**; papers' "value matrix" is only the value-down part |
| 23:39 | Deeper layers can hold more abstract ideas (sentiment, tone, "is it a poem") |
| 24:11 | 96 layers: about 58B parameters in attention, roughly a third of 175B |
| 24:41 | The real win is **parallelism**, because scale pays |

### Ch 7. How might LLMs store facts (22:43)
| Time | Idea |
|---|---|
| 0:00 | "Michael Jordan plays the sport of ___": where do facts live? |
| 0:35 | Google DeepMind's work on athletes and sports: facts seem to live in the MLPs |
| 3:16 | uncle + (woman − man) ≈ aunt; vectors also take in the model's knowledge |
| 4:18 | Most parameters are in the MLPs |
| 4:49 | Toy assumptions: nearly perpendicular directions for *first name Michael*, *last name Jordan* and *basketball*; a dot product of 1 means "has the feature" |
| 5:53 | Attention has already moved "Michael" into the "Jordan" token |
| 6:26 | The MLP acts on each vector separately, in parallel; its output is **added** to its input |
| 7:30 | **Rows of W_up are questions**: a row equal to M + J gives a dot product of 2 for "Michael Jordan" |
| 9:02 | A bias of −1 makes the value positive only for the full name |
| 9:33 | About 50,000 rows = **4 × d_model** |
| 10:09 | A linear layer also fires for Michael Phelps and Alexis Jordan. **ReLU** turns the row into an **AND gate** |
| 11:12 | GELU is a smooth ReLU. "Neurons" are these hidden values; a neuron is active when its value is positive |
| 12:12 | **Columns of W_down are directions**: column 1 = basketball, added when neuron 1 fires (the column view of matrix multiplication) |
| 13:49 | b_down; the result is added back to the stream |
| 15:38 | Tally: 604M per matrix, 1.2B per MLP, 116B in total (about 2/3); everything sums to 175B |
| 16:59 | Real neurons rarely stand for one clean feature |
| 17:30 | **Superposition**: only n directions can be exactly perpendicular, but far more fit at 89–91° |
| 18:34 | Experiment: 10,000 random 100-d vectors; angle histogram; after optimisation every angle lies in 89–91° |
| 19:37 | **Johnson–Lindenstrauss**: the number of nearly perpendicular vectors grows exponentially with the dimension |
| 20:11 | This applies to the embedding space and to the neuron space. Features are combinations of neurons; sparse autoencoders try to find them |

### CE. But what is cross-entropy? (33:51; side topic, the training loss)
| Time | Idea |
|---|---|
| 0:00 | "Language trees and zipping": gzip distance recovers language families |
| 3:02 | Optimal code length = −log₂ p (information content) |
| 5:20 | **Cross-entropy** H(P, Q) = Σ pᵢ(−log₂ qᵢ). Bar diagram: width pᵢ, height −log₂ qᵢ |
| 8:26 | Asymmetric (1 bit vs about 1.74 bits). Fix P and vary Q: the minimum is at Q = P and equals H(P); the minima trace out the entropy curve |
| 14:55 | LLM pre-training loss = the **average information per token** from the model's point of view |
| 20:38 | **Why the log?** A loss minimised exactly when the model matches the data's statistics must be a log (Lagrange-multiplier argument) |
| 26:13 | **Distillation**: cross-entropy against a big model's full distribution, a "softer tug" than one true token |
| 31:35 | KL = cross-entropy − entropy: the wasted bits; asymmetric |

---

## 3. 3b1b's animations, ranked by teaching value (for our Manim versions)

**Rules for every recreation:**
- Recreate the *idea*. Never his frames, code or assets.
- Use our own data where possible: real GPT-2 small weights, real word vectors.
- Credit the intuition in an Extra box and in Sources.
- Manim **Community** 0.20.1 (installed in the campusx env). His style library is ManimGL, which is a different API.
- Output: `<name>.gif` + `<name>_frames.png`, a 2×2 grid of key frames, as in `603-hessian-and-multivariate-taylor/images/optimizer_race.py`. Render Manim to a PNG sequence (`--format png`), make the GIF with ffmpeg palettegen, and build the grid with PIL from 4 key frames.
- Plotly frames are fine where the picture is a chart, not geometry.

**Effort:**
- **simple:** under half a day; toy data, no model.
- **medium:** half a day to 1.5 days; needs the GPT-2 NumPy forward pass or GloVe.
- **hard:** over 1.5 days; needs an interpretability search or a fragile result.

| Rank | 3b1b animation (time) | What it shows, and why it works | Our recreation and data | Target Note | Effort |
|---|---|---|---|---|---|
| 1 | Value vectors scaled and **added as Δe** to "creature" (Ch 6, 13:12–15:44); mole/tower moving (1:32–3:43) | A generic word arrow gets nudged into a specific region. Attention reads as *editing* a vector, not replacing it, and the picture carries on into residual connections and multi-head sums | Manim 2-D/3-D: the arrow e_creature; weighted value arrows from "fluffy" and "blue" placed tip to tail; Δe; e + Δe lands near "furry/fuzzy" words. Data: GloVe 100-d (or GPT-2 wte) projected onto a plane fitted to the word set; nearest neighbours before and after shown as labels | 1075 §6–7 (new final frame), 1080 §5.2 | medium |
| 2 | **Grid of dots** (size = score), softmax per column, then **mask to −∞** (Ch 6, 8:30–12:42) | Every pair is visible at once; dot size reads faster than heatmap colour; the mask visibly blanks one triangle | Manim grid of circles sized by **real GPT-2 small** attention on a real sentence: raw scores → scaled → masked → softmax rows. Our row convention (rows = queries) | 1081 §6.3 (today's figure uses random weights), 1073 Fig 2 | medium |
| 3 | **Directions carry meaning**: woman − man moved onto king; plural direction; a 3-D slice of embedding space (Ch 5, 13:33–17:44) | Turns "embedding" from a list of numbers into geometry you can do arithmetic with; sets up dot product = alignment | Manim ThreeDScene: GloVe vectors projected onto 3 directions we choose (gender, plurality, royalty); arrows for the analogy; honest failure case (queen not exactly hit, as he says). Plotly bars: plural-direction score for singular vs plural nouns and for one…ten | new Note "meaning as direction" (§4.c) | medium |
| 4 | **MLP as an AND gate**: row M + J, bias −1, ReLU, column = basketball (Ch 7, 7:30–14:19) | The first readable story of what an MLP *does* inside a transformer: rows ask, ReLU decides, columns write | Manim toy with 3 hand-built orthogonal directions (the toy is the point), fed Michael Jordan / Michael Phelps / Alexis Jordan; numbers on screen. Then a real check in Plotly: per-layer MLP contribution to the "basketball" logit in GPT-2 small | new Note "how the FFN stores facts" | toy simple; GPT-2 part medium–hard |
| 5 | **Angle histogram squeezed into 89–91°** (Ch 7, 18:34–20:11) | A shocking fact about high dimensions in one moving chart; motivates superposition | Plotly frames → GIF: 10,000 random vectors in 100-d (NumPy), histogram over optimisation steps. Plus a static Plotly histogram of real angles between GPT-2 wte rows (768-d) | new Note "superposition" | simple |
| 6 | **Softmax temperature** reshaping a distribution; stories at T = 0 vs high T (Ch 5, 22:22–25:11) | Shows sampling as a dial, not magic; explains why chatbots vary | Manim bar chart driven by a ValueTracker T, using **real GPT-2 small logits** for "Once upon a time there was a"; side text: GPT-2 continuations at T = 0, 0.7, 1.5 | new Note "unembedding, logits, temperature" | simple, once the forward pass exists |
| 7 | **Running parameter tally** to 175B (Ch 5–7) | Every matrix gets a size and a share; shows that attention is only about 1/3 | Plotly animated stacked bar: GPT-2 small (exact, from the safetensors header: 124,412,160 parameters) and GPT-3 (from Brown 2020 Table 2.1 dimensions) | new Note "GPT, decoder-only" | simple |
| 8 | **Value map factored**: a 12,288² square split into value-down/value-up; W_O as the value-ups stapled together (Ch 6, 16:20–18:21, 22:34) | Explains why W_O exists and why each head's value map is low rank | Manim matrix-shape blocks; then Plotly: singular values of W_V^h W_O^h from BERT layer 1 (weights already downloaded the 1077 way): 64 non-zero, then a cliff | 1077 §5.3 / §6 | simple |
| 9 | **Predict–sample–repeat**, showing the distribution at every step (Ch 5, 1:31–2:35) | Makes "an LLM is a next-token distribution" concrete | Reuse the 1084 `decode_anim.gif` design, with GPT-2 small sampling instead of translation | new Note "GPT, decoder-only" | simple, once the forward pass exists |
| 10 | **Cross-entropy bars**; fix P, vary Q, the minimum traces H(P) (CE, 5:20–12:59) | A geometric reason why the log loss is minimised at Q = P | Plotly frames → GIF for the two-outcome case | 1014 §9 (owner), linked from 1083 §9 | simple |
| 11 | **Colour rule**: weights blue/red, data grey (Ch 5, 12:01) | A reader can tell learned from computed at a glance | Make it a figure-style rule for all transformer figures (one token: weights = one hue, activations = grey) | all transformer figures | simple |

He shows two views of a matrix–vector product: rows as dot products (Ch 7, 7:30) and the product as a sum of scaled columns (12:12). Both are already owned by 500/510 (the "column by column" section of 510 §4), so link to them and do not redraw.

**Shared infrastructure, built once:** `gpt2_numpy.py`, a GPT-2 small loader plus forward pass in NumPy. Reuse the byte-range safetensors reader already in the 1077 notebook: the `Range` header plus the JSON header parse; no torch, no transformers, neither is installed. Use the `tokenizers` library (0.23.2, installed) with GPT-2's `tokenizer.json`. Checked on 2026-10-03:
- `openai-community/gpt2/model.safetensors` has 160 tensors;
- config: 12 layers, 12 heads, d = 768, n_ctx = 1024, `gelu_new`;
- learned positions `wpe` (1024 × 768);
- the causal mask is stored as a `h.N.attn.bias` buffer (1, 1, 1024, 1024);
- there is **no separate output matrix**, so the unembedding is `wte` itself (tied).

GPT-2 small runs on CPU; topgro is not needed.

---

## 4. Mapping: 3b1b idea → our Note (b)

Grades:
- **same:** we teach it about as well.
- **ours stronger:** measured or sourced better.
- **ours weaker:** we have it, but thinner or less clear.
- **missing:** no Note owns it.

| 3b1b idea | Where | Our Note | Grade |
|---|---|---|---|
| LLM = probability for every next token | B 0:33, Ch 5 1:31 | 1067 §7–8, 1083 §8 | same |
| Chatbot = system prompt + repeated prediction | B 0:01, Ch 5 5:42 | 1067 §9 (SFT/RLHF only) | ours weaker (prompt format missing) |
| Sampling makes outputs vary | B 1:07, Ch 5 1:31 | 1063 §8, 1084 §5 (greedy only; beam in Extra) | missing |
| Training-data and compute scale | B 1:39, 3:13 | 1067 §8 (data, GPUs, days, energy, all sourced) | ours stronger; "years of compute" framing missing |
| Pre-training vs RLHF | B 3:45 | 1067 §9 (InstructGPT 3 steps) | ours stronger |
| Parallelism is the transformer's win | B 4:18, Ch 6 24:41 | 1071 §5 (measured on GPU) | ours stronger |
| Tokens are word pieces / patches | Ch 5 3:06 | 1080 §4 (BPE, one line), 1071 §6.3 (ViT) | ours weaker (no tokenizer demo) |
| High-level GPT flow (embed → [attn, MLP]×L → last vector → distribution) | Ch 5 3:06–5:10 | 1085 (encoder–decoder flow only) | missing for decoder-only |
| Weights vs data; everything is weighted sums | Ch 5 8:52–12:01 | 1010 forward propagation; 500/510 | same (owned earlier) |
| Embedding matrix as lookup | Ch 5 12:31 | 1072 §5, 1080 §4 | same |
| Nearest neighbours of a word | Ch 5 14:37 | 1072 §4.2 (real PPMI-SVD table) | same (ours on real data) |
| **Directions carry meaning; vector arithmetic** | Ch 5 15:09; Ch 7 3:16 | 1072 §3 (per-coordinate picture with caveat) | missing (ours slightly points the wrong way: coordinates, not directions) |
| Dot product = alignment | Ch 5 16:44 | 362 §5 | same (owned by 362) |
| Plural direction as a probe | Ch 5 17:14 | none | missing |
| Vectors soak in context | Ch 5 18:14; Ch 6 1:32 | 1072 §5–6 ("bank", real numbers) | ours stronger |
| **Context size** | Ch 5 19:49 | none (1071 §5 only on cost) | missing |
| **Unembedding W_U, logits** | Ch 5 20:22, 25:42 | 1083 §8 (linear + softmax, "logits"); 1084 last position | ours weaker (not called unembedding; no geometric "dot with every token vector" view; no tying in GPT) |
| Every position predicts in training | Ch 5 21:28; Ch 6 11:05 | 1081 §4.3 and Extra, 1083 §9 | same |
| Softmax | Ch 5 22:31 | 79 (owner), 1073 §4.2 | same |
| **Temperature** | Ch 5 24:04 | none | missing |
| "Murderer was": the last vector must hold all context | Ch 6 3:43 | 1084 §6 (only the last row is used) | ours weaker (mechanics, no meaning) |
| Q/K as question and answer (adjective→noun toy) | Ch 6 6:22–8:30 | 1073 §7 (dictionary + matrimonial analogies) | ours weaker in clarity, same in content |
| Smaller key–query space (128) | Ch 6 6:22 | 1077 §6 (64 per head) | same |
| Attention pattern grid, softmax | Ch 6 8:30–10:03 | 1073 §4–5 (real weights), 1075 | same |
| √d_k | Ch 6 10:35 | 1074 (derivation + measurement) | ours stronger |
| Masking with −∞ | Ch 6 11:05 | 1081 | ours stronger |
| context² cost | Ch 6 12:42 | 1071 §5, §9 | ours stronger |
| **Value = what to add; Δe added to e** | Ch 6 13:12–15:44 | 1073 §8 (y = Σ w v), 1075 §6–7, 1080 §5.2 (residual stream) | ours weaker: the link "attention output is an *added* change" is never drawn |
| **Low-rank value map (value-down/up)** | Ch 6 16:20 | 1077 §6 (W_V^i is 512 × 64; W_O 512 × 512) | missing as an idea |
| **W_O = value-ups stapled; heads' Δe summed** | Ch 6 20:31–23:08 | 1077 §5.3 ("editor" mixes concatenation) | ours weaker |
| Cross-attention | Ch 6 18:27 | 1082 | ours stronger |
| Many heads, many kinds of update | Ch 6 19:28 | 1077 §4, §8 (BERT heads, real) | ours stronger |
| Deeper layers are more abstract | Ch 6 23:39 | 1080 §7.3 ("depth", BLEU vs N) | ours weaker (no layer-wise evidence) |
| Parameter counting by matrix | Ch 5–7 | 1077 §6.1, 1080 §6, 1083 §7 (Vaswani base, exact via Keras) | ours stronger for Vaswani; **GPT-3 / GPT-2 tally missing** |
| **Facts live in MLPs** | Ch 7 0:00–0:35 | 1080 §7.2 (one paragraph: Geva 2021, SLP3) | ours weaker |
| MLP per token, added back | Ch 7 6:26 | 1080 §5.3 (measured "separately, identically") | ours stronger |
| **Rows of W_up = questions; ReLU = AND gate; columns of W_down = directions written** | Ch 7 7:30–13:16 | none | missing |
| d_ff = 4 × d_model | Ch 7 9:33 | 1080 §5.3 (2048 vs 512; ratio not named) | same |
| GELU | Ch 7 11:12 | 1080 §7.2 Extra (SwiGLU only) | missing |
| MLP holds about 2/3 of the parameters | Ch 7 15:38 | 1080 §6 (66.6%, Geva quote) | same |
| **Superposition; nearly orthogonal; JL** | Ch 7 16:59–21:14 | none (46 curse of dimensionality is about sparsity, not angles) | missing |
| Cross-entropy as information; why log; distillation; KL | CE | 1014 §9 (CE formula; KL named only), 1085 §7.4 (perplexity), 1071 §10 (distillation, one line) | ours weaker |
| Decoder-only GPT vs encoder–decoder | Ch 5 1:01, Ch 6 18:27 | 1067 §8, 1071 §8, 1081 Extra, 1085 §9 (one line each) | missing as a taught architecture |

---

## 5. Missing concepts, with proposals (c)

Order is by how much a beginner loses without the concept. "New Note" means one concept per Note. Numbers 1086+ are placeholders; where each Note goes is the coordinator's call.

| # | Concept | Proposal | Experiment / figure on real data |
|---|---|---|---|
| 1 | **Decoder-only GPT** (no encoder, no cross-attention; causal LM on every position; learned positions; pre-LN; GELU; tied unembedding) | **New Note "GPT: the decoder-only transformer"** (e.g. 1086), straight after 1085. 1081's Extra and 1085 §9 recap it and link | Load GPT-2 small via `gpt2_numpy.py`. Check the shapes against the header; reproduce the HF model's top next token for 3 prompts. Count parameters exactly (124,412,160). Plotly tally animation (rank 7). Sources: Radford 2018, 2019 §2.3 (pre-LN, extra final LN), Brown 2020 §2.1 and Table 2.1 |
| 2 | **Context size** | Fold into the new GPT Note (one section); 1071 §9 links to it | GPT-2 n_ctx = 1024 (config). Plot memory of the n_ctx² attention pattern per head/layer vs context length (arithmetic, Plotly). Show the `attn.bias` mask buffer is 1024 × 1024 |
| 3 | **GPT-3 parameter count by matrix** | Fold into the new GPT Note | From Brown 2020 Table 2.1 (d = 12,288, L = 96, 96 heads of 128, n_ctx = 2,048, vocab 50,257): attention 57.98B, MLP 115.96B, W_E 0.618B, positions 25.2M. That is **174.59B with a tied unembedding, 175.21B untied** (computed here). Both round to "175B"; see §7.2 |
| 4 | **Unembedding matrix and logits** (last vector · every token's vector) | **New Note "From the last vector to a token: unembedding, logits and temperature"** (e.g. 1087). 1083 §8 keeps the Vaswani output layer and links forward | GPT-2 small: the final vector after ln_f, dotted with all 50,257 rows of wte; top-10 logits for "The capital of France is". Show the logit lens: unembed the residual after each layer and watch the right token rise (Plotly line per layer) |
| 5 | **Softmax temperature and sampling** (greedy = T → 0) | Same new Note as #4 (one concept: turning logits into a choice). 1063 §8.2 and 1084 §5 recap. Beam search stays in 1084 | Rank-6 Manim animation on real GPT-2 logits. Measure the entropy of the next-token distribution vs T (Plotly). Measure the share of distinct continuations over 20 samples at T = 0.3/0.7/1.0/1.5 |
| 6 | **Meaning as direction; vector arithmetic; dot-product probes** | **New Note "Meaning as direction in embedding space"**, placed before 1072. 1072 §3 replaces its per-coordinate example with a recap and link. Fallback: fold into 1057 §7.3 | GloVe 6B 100-d (Pennington et al. 2014; download URL to confirm at build time). king − man + woman → nearest, with its rank and cosine (honest about "queen" being imperfect); uncle/aunt, nephew/niece pairs; plural direction (mean of plural − singular pairs) dotted with held-out nouns and with one…ten. Repeat on GPT-2 wte to show the same structure inside a transformer. Rank-3 animation |
| 7 | **Attention output as an added adjustment Δe** (residual-stream view) | Fold: 1075 new §7.3 "Adding the change back"; 1080 §5.2 adds one sentence plus a link | Rank-1 animation. In GPT-2 small, measure ‖Δe‖/‖e‖ per layer for one token (the edits are small next to the stream) and the cosine between e before and after each attention block |
| 8 | **Low-rank value map; W_O as per-head value-ups; head outputs summed** | Fold into 1077: new §5.4 "W_O split per head: every head adds its own change" | Check numerically that Concat(Z₁…Z_h)W_O = Σ_h Z_h W_O^(h) (rows h·64…). Singular values of W_V^(h) W_O^(h) on BERT layer 1 (download W_O too): exactly 64 non-zero. Rank-8 animation |
| 9 | **MLP as key–value fact store** (rows = questions, ReLU = AND, columns = written directions; neurons) | **New Note "How the feed-forward network stores facts"** (e.g. 1088). 1080 §7.2 keeps its paragraph and links | (a) Toy Manim AND gate (rank 4). (b) GPT-2 small, "Michael Jordan plays the sport of": the prob of " basketball", then zero each layer's MLP output in turn and record the drop (Plotly bars). Direct logit attribution: mlp_out_ℓ · wte[" basketball"]. (c) Geva-style: for the top neuron, project its W_down column through wte and list the top tokens. Risk: GPT-2 small may not know the fact strongly. Check first; fall back to a fact it does know (e.g. "The Eiffel Tower is in the city of") |
| 10 | **GELU** | Fold into the new FFN Note (one paragraph plus a Plotly curve vs ReLU); 1027 activation-functions recaps | Plot GELU vs ReLU; confirm GPT-2 config `gelu_new` |
| 11 | **Superposition; nearly orthogonal directions; JL lemma; polysemantic neurons** | **New Note "Superposition: more features than dimensions"** (e.g. 1089), after the FFN Note | (a) Rank-5 histogram GIF (NumPy: 10,000 × 100-d; penalise squared cosines; about 5,000 vectors if memory is tight). (b) Real angles between GPT-2 wte rows. (c) Elhage et al. 2022 toy model: 5 sparse features → 2-d hidden, ReLU output, train in NumPy at several sparsities; the pentagon appears only when features are sparse (their Fig. 2). Sources: Elhage 2022; JL as stated in Dasgupta & Gupta 2003 (open it before citing) |
| 12 | **Decoder-only vs encoder–decoder** (which parts each keeps, and why GPT needs no cross-attention) | In the new GPT Note (#1), a comparison table vs 1080/1083 | Side-by-side block diagrams (TikZ): Vaswani decoder block (3 sub-layers) vs GPT-2 block (2 sub-layers, pre-LN) |
| 13 | Cross-entropy as information; why the log; distillation; KL | Fold into **1014 §9** (owner of categorical CE) as an Extra; 1083 §9 recaps "average information per token" | Rank-10 GIF. Distillation demo: a small Keras model on MNIST trained on hard labels vs soft labels from a bigger model, at small data sizes (Hinton et al. 2015) |
| 14 | Chatbot = system prompt + continuation | One paragraph in 1067 §9 | GPT-2 small given a "User: … Assistant:" frame: show it continues the format but is not a good assistant, which motivates SFT/RLHF (already in 1067 §9) |
| 15 | Compute as "years at 10⁹ ops/s" | One sentence in 1067 §8 | GPT-3 training FLOPs from Brown 2020 (Table D.1, about 3.14 × 10²³; open it to confirm) ÷ 10⁹ /s ≈ 10 million years. 3b1b's "100 million years" refers to *larger* models, not GPT-3 |

---

## 6. Better intuitions: where his picture is clearer (d)

The top 5 are first.

1. **Attention adds a change, it does not replace (1075 §6–7, 1073 §8, 1080 §5.2).** Ours: y = weighted average of values, and 1075 §7.1 stresses that the output "cannot leave the convex hull of the values". His: values are "what to add"; Δe goes on top of e (Ch 6, 13:12–15:44). The fix keeps our maths:
   - add a frame or subsection where the output is added to the original vector, and say "this addition is the residual connection of 1080";
   - for post-LN, say the LayerNorm follows the addition.

   Figure: rank-1 Manim.
2. **W_O as a sum of per-head changes (1077 §5.3).** Our "editor mixes the concatenation" is right but opaque. His view, every head proposes a Δe and they are summed (Ch 6, 20:31–23:08), is the same algebra, because [Z₁ Z₂]W_O = Z₁W_O¹ + Z₂W_O². It also explains why W_O exists: it holds each head's "value-up". Add the identity with the worked numbers already in §5.3 (the 2-head example) and one Manim block animation.
3. **Embeddings: directions, not coordinates (1072 §3).** Ours gives king = [0.6, 0.2, 1, 0, 0.9] with "first number = royalty". The caveat is there, but the picture points toward per-axis meaning. His picture: meaning lives in *directions* (gender = woman − man), and a dot product reads how much of it a vector has (Ch 5, 15:09–17:44). Replace the per-coordinate example with a 2-arrow picture (royalty and gender directions) and link the new direction Note. Figure: Plotly 2-D projection of real GloVe vectors with the analogy arrows.
4. **Query/key as a question and an answer (1073 §7).** Our dictionary and matrimonial analogies are good for *why three roles*. His adjective→noun toy (Ch 6, 6:22–9:32) is better for *what Q and K compute*: a noun's query asks "adjectives before me?", an adjective's key answers, and a big dot means a match. Add a short toy paragraph after the analogy, and redraw the 1073 Fig 2 weights as a **dot-size grid** (Plotly scatter, marker size = weight). That is a 15-minute change that reads faster than a heatmap.
5. **The MLP block as questions and answers (1080 §5.3, §7.2).** Ours explains the FFN by shapes and "non-linearity per word". His reading:
   - each row of W₁ is a feature detector (dot product + bias);
   - ReLU gates it;
   - each column of W₂ is what gets written when it fires (Ch 7, 7:30–13:16).

   This matches Geva 2021's keys and values, which 1080 already cites. Add a 3-line "how to read W₁ and W₂" box with a link to the new FFN Note.

Smaller upgrades:
- **1084 §5–6:** add the "…therefore the murderer was" framing. The last vector must already hold the whole relevant context, which is why only it is unembedded (Ch 6, 3:43).
- **1081 §6.3:** swap the random-weight matrices for a real GPT-2 small head (rank-2 animation). The real pattern (previous-token head, etc.) teaches more than random weights.
- **1080 §7.3:** "deeper = more abstract" needs data. Use a logit-lens or probing plot on GPT-2 small, or keep it out (rule: claims need evidence).
- **All transformer figures:** adopt his colour rule. Weights in one hue, data in grey (Ch 5, 12:01).
- **1074:** no change. Ours is stronger than his one-line "numerical stability".

---

## 7. Where 3b1b and our Notes disagree, and who is right (e)

1. **Why divide by √d_k.**
   - 3b1b: "for numerical stability" (Ch 6, 10:35).
   - Vaswani 2017 §3.2.1: large dot products push the softmax "into regions where it has extremely small gradients". SLP3 (eq. 7.11) gives both reasons: numerical issues and loss of gradients.

   **Our 1074 matches the paper.** His remark is incomplete, not wrong. Keep 1074 as it is.
2. **Is the unembedding a separate 617M matrix?**
   - 3b1b counts W_U separately (Ch 5, 21:59).
   - Vaswani 2017 §3.4 ties the embeddings and the pre-softmax matrix (our 1083/1085 say so).
   - GPT-2 also ties them: the released weights (`openai-community/gpt2/model.safetensors`, 160 tensors) contain only `wte` and no separate output matrix. Checked here.
   - Brown 2020 says GPT-3 uses "the same model and architecture as GPT-2" with alternating sparse attention, but does not state the tying explicitly.

   **Unresolved for GPT-3:** the tally is 174.59B tied vs 175.21B untied, and both round to "175B". In the new GPT Note, present W_U as tied for GPT-2 (verified) and do not claim either way for GPT-3.
3. **Rows vs columns.** He puts queries as columns and applies the softmax per column (Ch 6, 9:32). Vaswani's QKᵀ and all our Notes put queries as rows, softmax per row. Same maths, transposed. **Keep the row convention** in our recreations and say so in captions.
4. **Name of the "value matrix".** His value-down is the paper's W_V^i; his value-up is a slice of W_O. He flags this himself (Ch 6, 22:34). Our 1077 uses the paper's names, which is correct per Vaswani §3.2.2. When we add the per-head-W_O view, use the paper's names and mention his only once, as an intuition.
5. **"Attention output stays inside the values" (1075 §7.1) vs "attention adds Δe" (Ch 6).** Both are right at different levels:
   - 1075 describes a single head's attention output;
   - his Δe is the block output after W_O and the residual addition.

   Not a contradiction. Add the bridging sentence (§6 item 1).
6. **Normalisation placement.**
   - 3b1b: normalisation "in between", not specified.
   - Our Notes: post-LN, correct for Vaswani §3.1.
   - GPT-2 moved LayerNorm to the *input* of each sub-block and added one after the last block (Radford 2019 §2.3; matches `ln_1`/`ln_2`/`ln_f` in the weights).

   His clean "add Δe to the stream" picture is exact for pre-LN, so the new GPT Note should teach pre-LN. 1085 §7.3 already mentions Pre-LN via Xiong 2020.
7. **Activation in the MLP.** 3b1b uses ReLU and mentions GELU. Vaswani §3.3 uses ReLU (our 1080 is right for the paper). GPT uses GELU (Radford 2018 §4.1; GPT-2 config `gelu_new`). No conflict; it is a gap for the GPT Note.
8. **Facts live in MLPs.** 3b1b cites Google DeepMind's athletes→sports work (Ch 7, 0:35; it is the DeepMind "Fact Finding" posts by Nanda et al., Dec 2023, which we have not opened yet; open before citing). Geva et al. 2021 support the key–value reading: keys detect input patterns, and values promote output tokens. Our 1080 §7.2 cites Geva correctly. **Agreement**, with the caveat both he and Geva give: a full mechanism is not solved.
9. **Superposition and JL.** His claim: the number of nearly orthogonal vectors grows exponentially with dimension (a consequence of the JL lemma). That is standard. Elhage et al. 2022 present superposition as a *hypothesis* with toy-model evidence, which matches his wording ("a hypothesis"). Our Notes are silent, so there is no conflict. The new Note must keep the word "hypothesis".
10. **GPT model sizes (1067 §8).** 1067 gives GPT-1 = 117M, quoting Radford 2019 Table 2's smallest size. The released GPT-2 small weights hold **124,412,160** parameters (counted from the header here). A known gap: the 117M figure does not match the released file. No 3b1b conflict, but the new GPT Note should give the counted number and explain the gap only if a source explains it.
11. **Cross-attention wording.** 3b1b says "the key and query maps act on different data sets" (Ch 6, 18:27). Precisely: queries come from the decoder; keys *and values* come from the encoder (Vaswani §3.2.3). Our 1082 is precise. Keep it.

No case was found where 3b1b is right and our Notes are wrong. Our gaps are omissions, not errors. The one wording risk is 1072 §3's per-coordinate example (§6 item 3).

---

## 8. Build order (suggested)

1. `gpt2_numpy.py` (loader + forward pass + tokenizer). It unblocks ranks 2, 4b, 6, 7, 9 and Notes #1, #4, #5, #9.
2. Quick wins with no model: rank 5 (superposition histogram), rank 8 (W_O split, BERT weights), rank 10 (cross-entropy bars), the 1073 dot-grid redraw, the 1077 §5.4 identity.
3. New GPT Note, then the unembedding/temperature Note, then the "meaning as direction" Note (needs GloVe), then the FFN Note, then the superposition Note.
4. Rank-1 Manim (Δe) for 1075/1080 once the direction Note's GloVe set-up exists.
