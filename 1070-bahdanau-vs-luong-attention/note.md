---
title: "Bahdanau Attention and Luong Attention"
---

## 1. Overview

> **Key point:** Both attentions build a context vector $c_i = \sum_j \alpha_{ij} h_j$; they differ in how they score each encoder state and where the context enters the decoder. **Bahdanau** (additive) attention scores the previous decoder state $s_{i-1}$ against $h_j$ with a small neural network, and feeds $c_i$ *into* the LSTM step. **Luong** (multiplicative) attention scores the current state $s_i$ against $h_j$ with a dot product, and joins $c_i$ to the LSTM's *output*.

The [attention Note](../1069-attention-mechanism/note.md) introduced attention in the encoder–decoder: at every decoder step, a weighted sum of all the encoder's hidden states, with weights from a softmax over scores $e_{ij}$. It left open how the scores are computed. This Note opens the two best-known answers: Bahdanau et al. (2015) and Luong et al. (2015). The second one introduced the dot-product score that the transformer's self-attention builds on.

![Where attention sits in the two designs. (a) Bahdanau: the previous state $s_{i-1}$ is scored, and $c_i$ is an input of the LSTM step. (b) Luong: the LSTM step runs first, its new state $s_i$ is scored, and $c_i$ is combined with $s_i$ before the output layer](images/two_paths.png){width=78%}

## 2. Prerequisites

- [Attention Note](../1069-attention-mechanism/note.md): context vectors, alignment scores, softmax over the input positions.
- [Encoder–decoder Note](../1068-encoder-decoder/note.md): encoder, decoder, teacher forcing.
- [Dot product and cosine similarity Note](../362-dot-product-and-cosine-similarity/note.md): the dot product as a measure of similarity.
- [Forward propagation Note](../1010-forward-propagation/note.md): a dense layer as a matrix product.

## 3. Recap: what both must compute

> **Key point:** Scores $e_{ij}$, weights $\alpha_{ij} = \text{softmax}_j(e_{ij})$, context $c_i = \sum_j \alpha_{ij} h_j$. Only the score function and the wiring differ.

For "turn off the lights" → "light band karo", decoder step 1 needs $c_1 = \alpha_{11}h_1 + \alpha_{12}h_2 + \alpha_{13}h_3 + \alpha_{14}h_4$, step 2 needs $c_2$ with new weights, and so on: (number of input words) × (number of output words) weights in all. Each weight is a word-to-word similarity: $\alpha_{11}$ says how much "turn" counts when writing "light". The question of this Note is how to get the raw scores $e_{ij}$.

## 4. Bahdanau attention

> **Key point:** A feed-forward network with one hidden layer scores the pair $(s_{i-1}, h_j)$: $e_{ij} = v^\top \tanh(W[s_{i-1}; h_j])$. The context vector is then an input of decoder step $i$.

### 4.1 What the score depends on

> **Key point:** On the encoder state $h_j$ and on the decoder's *previous* state $s_{i-1}$, which holds what has been translated so far.

As the [attention Note](../1069-attention-mechanism/note.md) (section 6) explains, $\alpha_{ij}$ must depend on $h_j$, the input word being judged, and on what the decoder has already written, which is stored in $s_{i-1}$. To compute $\alpha_{11}$, the weight of "turn" for the first output word, we need $h_1$ and $s_0$; for $\alpha_{21}$ we need $h_1$ and $s_1$. Bahdanau et al. (2015) do not choose a formula for the score; they let a small feed-forward network learn it, the **alignment model**.

### 4.2 The alignment network, step by step

> **Key point:** Concatenate $s_{i-1}$ with every $h_j$, pass the rows through a hidden layer with tanh, then through one output unit: one score per input word. Softmax gives the weights.

Take hidden states of size 4 and an alignment network with 3 hidden units and 1 output unit. At decoder step 1:

1. **Concatenate.** Join $s_0$ (4 numbers) with each of $h_1, \dots, h_4$ (4 numbers each). Stacked, the four rows form a $4 \times 8$ matrix $X$, one row per input word.
2. **Hidden layer.** Multiply by the $8 \times 3$ weight matrix $W$ and apply tanh: a $4 \times 3$ matrix. A bias can be added before the tanh.
3. **Output unit.** Multiply by the $3 \times 1$ vector $v$: 4 numbers, the scores $e_{11}, \dots, e_{14}$.
4. **Softmax** over the 4 scores gives $\alpha_{11}, \dots, \alpha_{14}$, and the weighted sum gives $c_1$.
5. **Decoder step.** $c_1$, $s_0$ and the input $y_0$ (`<start>`) go into the LSTM, which outputs the first word, "light", and the new state $s_1$.

At step 2 the same network runs again with $s_1$ in place of $s_0$. In the $4 \times 8$ matrix only the left half changes; the encoder states on the right stay the same. The changing decoder state is why every step gets different weights. The network's weights are shared across all decoder steps, like a time-distributed dense layer, and are updated by backpropagation together with the two LSTMs.

1. **In words:** concatenate the two states, apply one tanh hidden layer, then one output unit; softmax over the input positions.
2. **Formula** (Bahdanau et al. 2015, appendix A.1.2):
   $$e_{ij} = v^\top \tanh\left(W [s_{i-1}; h_j]\right) = v^\top \tanh\left(W_a s_{i-1} + U_a h_j\right), \qquad \alpha_{ij} = \frac{\exp(e_{ij})}{\sum_k \exp(e_{ik})}, \qquad c_i = \sum_j \alpha_{ij} h_j$$
   The two forms are the same: multiplying the joined vector $[s; h]$ by $W$ equals multiplying $s$ by the left half of $W$ and $h$ by the right half, and adding.
3. **Example:** the decoder state $s = [0.5, -0.2, 0.8, 0.1]$ and four encoder states, the first being $h_1 = [0.3, -0.5, -0.9, -1.0]$ (the Notebook lists all four and the weights $W$ and $v = [0.1, -0.4, 0.2]$). For $j = 1$, the joined row is $[0.5, -0.2, 0.8, 0.1, 0.3, -0.5, -0.9, -1.0]$. Times $W$ it gives $[-0.06, 0.47, 0.44]$; tanh gives $[-0.060, 0.438, 0.414]$; times $v$:
   $$e_1 = 0.1(-0.060) - 0.4(0.438) + 0.2(0.414) = -0.099$$
   The four scores are $(-0.099, -0.011, 0.449, -0.116)$, and softmax turns them into the weights $(0.208, 0.227, 0.360, 0.205)$. The score function has $8 \times 3 + 3 = 27$ learned numbers.

Because the score adds a term from $s_{i-1}$ to a term from $h_j$ inside the tanh, Bahdanau attention is also called **additive attention** (Vaswani et al. 2017, section 3.2.1). Since $U_a h_j$ does not depend on $i$, it can be computed once per sentence (Bahdanau et al. 2015, appendix A.1.2).

## 5. Luong attention

> **Key point:** Two changes. The score uses the *current* decoder state $s_i$, and it is a simple product: $e_{ij} = s_i^\top h_j$ (dot) or $s_i^\top W_a h_j$ (general). The context vector is joined to $s_i$ after the LSTM step, not fed into it.

Luong, Pham and Manning (2015) kept the goal and changed the means.

### 5.1 A simpler score

> **Key point:** Two similar vectors have a large dot product. Using the dot product as the score needs no network at all.

The aim of the score is not to approximate some exact function; it is to find which encoder states are useful now. A similarity measure does that job, and the simplest one is the dot product (the [dot product Note](../362-dot-product-and-cosine-similarity/note.md)): large when two vectors point the same way, small or negative when they do not. Luong et al. (2015, section 3.1) proposed three content-based scores:

| Name | Score $e_{ij}$ | Learned parameters |
|---|---|---|
| dot | $s_i^\top h_j$ | none |
| general | $s_i^\top W_a h_j$ | one matrix $W_a$ |
| concat | $v_a^\top \tanh(W_a [s_i; h_j])$ | $W_a$ and $v_a$, as in Bahdanau |

The dot score requires $s_i$ and $h_j$ to have the same size; the general score lifts that requirement and lets the model learn which directions of similarity matter (SLP3 §14.8). Because the score multiplies the two states, this family is called **multiplicative attention** (Vaswani et al. 2017, section 3.2.1).

1. **In words:** multiply the decoder state and each encoder state element by element and add up (dot), or first transform the encoder state by a learned matrix (general).
2. **Formula:**
   $$e_{ij} = s_i^\top h_j \ \ \text{(dot)}, \qquad e_{ij} = s_i^\top W_a h_j \ \ \text{(general)}$$
3. **Example:** the same $s = [0.5, -0.2, 0.8, 0.1]$ and $h_1 = [0.3, -0.5, -0.9, -1.0]$:
   $$e_1 = 0.5(0.3) + (-0.2)(-0.5) + 0.8(-0.9) + 0.1(-1.0) = 0.15 + 0.10 - 0.72 - 0.10 = -0.57$$
   The four dot scores are $(-0.57, 0.35, 0.25, 0.87)$, with weights $(0.100, 0.251, 0.227, 0.422)$: no learned numbers at all. With a $4 \times 4$ matrix $W_a$ (16 learned numbers, in the Notebook) the general scores are $(0.477, -0.254, 0.975, -0.887)$, with weights $(0.296, 0.142, 0.486, 0.076)$. The three functions rank the four states differently. Here the states and the weights are random numbers; in a trained model, training sets them so that the useful encoder states get the high scores, whichever function is used.

### 5.2 The current state, and the context on the output side

> **Key point:** The LSTM step runs first. Its new state $s_i$ is scored against the encoder states, and $\tilde{h}_i = \tanh(W_c[c_i; s_i])$ feeds the softmax.

Bahdanau's decoder goes $s_{i-1} \to \alpha_i \to c_i \to s_i$: the context must be ready before the LSTM step. Luong's goes $s_i \to \alpha_i \to c_i \to \tilde{h}_i$ (Luong et al. 2015, section 3.1):

1. The decoder LSTM takes $y_{i-1}$ and $s_{i-1}$ and produces $s_i$, with no context vector.
2. $s_i$ is scored against every $h_j$; softmax gives $\alpha_{ij}$; the weighted sum gives $c_i$.
3. $c_i$ and $s_i$ are joined and passed through a dense layer with tanh: the **attentional hidden state** $\tilde{h}_i = \tanh(W_c[c_i; s_i])$.
4. A softmax layer on $\tilde{h}_i$ gives the next word: $p(y_i) = \text{softmax}(W_s \tilde{h}_i)$.
5. $s_i$ (not $\tilde{h}_i$) and the word $y_i$ go on to step $i+1$.

Scoring with $s_i$ uses the most recent state, which already includes the latest word written. Figure 1 shows the two wirings side by side.

> **Extra:** Luong et al. (2015, section 3.3) also propose **input feeding**: $\tilde{h}_{i-1}$ is joined to the next input, so that the model remembers its past alignment choices. With input feeding the LSTM again needs the previous step's attention before it can run. The Notebook leaves it out, as in Luong's basic global model of section 3.1.

## 6. The two compared

XX

## 7. Summary

## 8. Sources

## 9. Key terms
