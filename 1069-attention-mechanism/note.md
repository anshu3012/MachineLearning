---
title: "The Attention Mechanism"
---

## 1. Overview

> **Key point:** In the plain encoder–decoder, the decoder sees one fixed summary of the whole input. With **attention**, the decoder gets a fresh **context vector** $c_i$ at every step: a weighted sum of all the encoder's hidden states, $c_i = \sum_j \alpha_{ij} h_j$. A small neural network, trained with the rest, decides the weights $\alpha_{ij}$, so each output word can focus on the input words it needs.

The [encoder–decoder Note](../1068-encoder-decoder/note.md) built a translator from two LSTMs joined by a single context vector. This Note explains why that single vector fails on long sentences, and how Bahdanau, Cho and Bengio (2015) fixed it. The fix, attention, is also the central idea of the transformer.

![Attention weights of a trained model translating a real English sentence into French. Row $i$ shows how much each English word counted when the model wrote French word $i$](images/attention_heatmap.png){width=95%}

## 2. Prerequisites

- [Encoder–decoder Note](../1068-encoder-decoder/note.md): encoder, context vector, decoder, teacher forcing, greedy decoding.
- [the LSTM Note](../1061-lstm/note.md): hidden states $h_t$ and how an LSTM reads a sequence.
- [Softmax regression Note](../79-softmax-regression/note.md): softmax turns scores into probabilities.
- [MLP intuition Note](../1009-mlp-intuition/note.md): a small feed-forward network with a hidden layer.

## 3. The problem with one context vector

> **Key point:** Two problems. The encoder must squeeze a whole sentence into one fixed vector, which fails for long sentences. And the decoder gets the same vector at every step, although each output word needs only a few input words.

### 3.1 The encoder side: too much in one vector

> **Key point:** However long the sentence, its summary has the same fixed size.

Read a sentence of 50 words once, close your eyes, and translate it. Few people can: the sentence is too long to hold in memory at once. The plain encoder–decoder is asked to do exactly this. The encoder reads the whole input and must pack it into one vector of fixed size, and the decoder must translate from that vector alone. For a short sentence the vector is enough; for a long one it is a **bottleneck**, and information from the start of the sentence is the most likely to be lost (SLP3 §14.8). Measurements show the effect: in Bahdanau et al. (2015, Figure 2) the translation quality of the plain encoder–decoder "dramatically drops as the length of the sentences increases" (see also the [history of LLMs Note](../1067-history-of-llms/note.md), section 4).

### 3.2 The decoder side: the same summary at every step

> **Key point:** Each output word depends on a few input words, but the decoder always receives the whole sentence as one static summary.

Translate "turn off the lights" into Hindi, "light band karo". To write "light", only "lights" is needed. To write "band" (off), only "turn off" is needed. At no step does the decoder need the whole sentence; it needs a particular word or group of words. Yet the plain decoder receives the same context vector at every step and must work out by itself which part of it matters now. The representation is **static**. A better design would let the decoder look at the useful part of the input at each step.

## 4. The idea: look back at the input while writing

> **Key point:** Keep all the encoder's hidden states, and at each decoder step give the decoder a weighted mix of them, with high weights on the input words that matter for the word being written.

People translate a long text piece by piece. While reading, our eyes and mind keep a small region of focus: the words around the current position are sharp, the rest is blurry, and the focus moves along as we go. Attention brings this into the network. When the decoder writes "light", it should be told that encoder step 4 ("lights") matters most; when it writes "band", that steps 1 and 2 ("turn off") matter most. This information must be computed anew at every decoder step.

## 5. The context vector at each step

> **Key point:** $c_i = \sum_j \alpha_{ij} h_j$. The weights are non-negative and sum to 1; $c_i$ has the same size as each $h_j$.

### 5.1 Notation

> **Key point:** $h_j$: encoder hidden states. $s_i$: decoder hidden states. $y_i$: decoder outputs. $c_i$: context vector for decoder step $i$.

Following Bahdanau et al. (2015):

- $h_1, \dots, h_n$ are the encoder's hidden states, one per input word ($n$ words). Each is a vector.
- $s_0, s_1, \dots$ are the decoder's hidden states.
- $y_{i-1}$ is the decoder's input at step $i$: the previous word (the gold word under teacher forcing).
- $c_i$ is the new **context vector** for decoder step $i$.

Without attention, decoder step $i$ uses two inputs: $y_{i-1}$ and $s_{i-1}$. With attention it uses three: $y_{i-1}$, $s_{i-1}$ and $c_i$ (Bahdanau et al. 2015, section 3.1: $s_i = f(s_{i-1}, y_{i-1}, c_i)$).

### 5.2 What $c_i$ is

> **Key point:** A vector of the same size as $h_j$: the weighted sum of all encoder states.

$c_i$ has to carry the useful encoder states into decoder step $i$. Sometimes one state is useful, sometimes several. A sum of several states would change the size, unless we add them up: the weighted sum of all states has the same size as a single state, and the weights decide how much each state counts.

1. **In words:** give each encoder state a weight, then add the states up, each multiplied by its weight.
2. **Formula:**
   $$c_i = \sum_{j=1}^{n} \alpha_{ij}\, h_j, \qquad \alpha_{ij} \ge 0, \qquad \sum_{j=1}^{n} \alpha_{ij} = 1$$
3. **Example:** three encoder states of size 4 and the weights $\alpha_{i1} = 0.185$, $\alpha_{i2} = 0.137$, $\alpha_{i3} = 0.678$ (section 6.2 shows where they come from):
   $$c_i = 0.185\,[1.0, 0.5, 0.6, 0.3] + 0.137\,[0.2, 0.9, 0.1, 0.4] + 0.678\,[0.7, 0.1, 0.8, 0.5] = [0.687, 0.284, 0.667, 0.449]$$
   The result is dominated by $h_3$, the state with the largest weight.

Every decoder step has its own weights. With $n$ input words and $m$ output words there are $m \times n$ weights per sentence pair: $4 \times 4 = 16$ for "turn off the lights" → "light band karo `<end>`". The weight $\alpha_{21}$, for example, says how much "turn" ($h_1$) counts when the decoder writes its second word, "band". The weights are also called **alignment scores**: they say which input word each output word lines up with.

## 6. Computing the weights

> **Key point:** $\alpha_{ij}$ depends on the encoder state $h_j$ and on the decoder's previous state $s_{i-1}$. A small feed-forward network scores each pair, and softmax turns the scores into weights.

### 6.1 What the weight depends on

> **Key point:** On $h_j$, the input word being judged, and on $s_{i-1}$, everything the decoder has written so far.

$\alpha_{21}$ measures how useful "turn" is for writing the second output word, so it must depend on $h_1$. It must also depend on the decoder's state before the step, $s_1$. The question is not only "which input word matches the next output word?", but "given everything translated so far, which input word is needed next?". What has been translated so far is stored in the decoder's previous state. So, in general,

$$e_{ij} = a(s_{i-1}, h_j)$$

where $e_{ij}$ is a raw score and $a$ is some function (Bahdanau et al. 2015, eq. 6).

### 6.2 Let a neural network find the function

> **Key point:** Instead of choosing a formula for $a$, use a small feed-forward network, the **alignment model**, and train it together with the encoder and decoder.

Which mathematical function should $a$ be? We could try many and keep the best. Bahdanau et al. took another route: a feed-forward neural network can approximate a very wide range of functions, so they let a small network be $a$ and trained it jointly with everything else (Bahdanau et al. 2015, section 3.1). The network takes $s_{i-1}$ and $h_j$ as inputs and outputs one number, $e_{ij}$. Its weights are learned by the same backpropagation that trains the two LSTMs.

The raw scores can be any real numbers. A **softmax** over the input positions turns them into weights that are positive and sum to 1:

1. **In words:** exponentiate each score and divide by the sum of all exponentials for that decoder step.
2. **Formula:**
   $$\alpha_{ij} = \frac{\exp(e_{ij})}{\sum_{k=1}^{n} \exp(e_{ik})}$$
3. **Example:** scores $e = (0.5, 0.2, 1.8)$ give $\exp(e) = (1.65, 1.22, 6.05)$ with sum $8.92$, so
   $$\alpha = (0.185, 0.137, 0.678)$$
   The Notebook gets the same numbers. The largest score takes most of the weight.

The full step, for decoder step 2 of "turn off the lights" (Figure 2):

1. Feed $(s_1, h_1)$, $(s_1, h_2)$, $(s_1, h_3)$, $(s_1, h_4)$ through the alignment model: scores $e_{21}, \dots, e_{24}$.
2. Softmax: weights $\alpha_{21}, \dots, \alpha_{24}$.
3. Weighted sum: $c_2 = \sum_j \alpha_{2j} h_j$.
4. The decoder LSTM takes $c_2$, $s_1$ and $y_1$ ("light"), outputs "band" and the new state $s_2$.
5. Repeat for step 3, with $s_2$ in place of $s_1$.

![One decoder step with attention. The same small network scores every pair $(s_1, h_j)$; softmax turns the scores into weights; the weighted sum $c_2$ joins the decoder's input](images/attention_step.png){width=100%}

The exact form of the alignment model, Bahdanau's additive score, and the alternative proposed by Luong et al. (2015) are the subject of the [Bahdanau vs Luong attention Note](../1070-bahdanau-vs-luong-attention/note.md).

> **Extra:** Bahdanau et al. (2015, section 3.1) read $\alpha_{ij}$ as a probability: the probability that output word $i$ is aligned to, or translated from, input word $j$. The context vector $c_i$ is then the expected encoder state under that distribution. Because the weights are a smooth function of the scores, the whole model stays differentiable and is trained with ordinary backpropagation.

## 7. Attention against no attention, by sentence length

> **Key point:** XX

XX

## 8. Seeing the alignment

> **Key point:** The weights can be drawn as a grid, output words against input words. A trained model puts its weight on the input words that a human would pair with each output word.

XX

## 9. Notes on the original model

> **Key point:** Bahdanau et al. used a bidirectional encoder, so each $h_j$ also knows the words after position $j$. The attention part is unchanged.

Two details of Bahdanau et al. (2015) differ from the simple picture above:

- **A bidirectional encoder** (section 3.2). One RNN reads the sentence forwards and a second reads it backwards; $h_j$ joins the two states at position $j$. Each $h_j$ then summarises the words before and after word $j$, with a focus on the words around it. Attention itself is computed exactly as above.
- **A gated unit, not an LSTM** (appendix A.1.1). Their encoder and decoder use the gated hidden unit of Cho et al. (2014), which the paper describes as similar to an LSTM unit and, like it, able to learn long-term dependencies.

The model was trained on English–French translation, with a vocabulary of the 30,000 most frequent words in each language and 1,000 hidden units in each direction of the encoder and in the decoder (section 4.2).

## 10. Summary

## 11. Sources

## 12. Key terms
