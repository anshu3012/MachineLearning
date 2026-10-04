---
title: "Deep (Stacked) RNNs"
---

## 1. Overview

> **Key point:** A deep RNN stacks several recurrent layers on top of each other. At every time step, each layer passes its hidden state up to the next layer and along to its own next time step. More layers give the network more representation power for complex patterns.

A **deep RNN**, also called a **stacked RNN**, is an RNN with more than one recurrent layer. The idea is the same one that turns a perceptron into a multi-layer perceptron: when one hidden layer cannot capture the pattern in the data, we add more layers. In an RNN, the extra layers are recurrent layers, and the whole stack is unfolded through time.

![A deep RNN with two recurrent layers on the review "cat mat rat". Layer 1 (3 nodes) reads the words; layer 2 (2 nodes) reads layer 1's hidden state at the same time step. Each layer also passes its own hidden state to its next time step (red). The last hidden state of the top layer gives the prediction](images/stacked_unrolled.png){width=100%}

Figure 1 shows a deep RNN with two layers. The same stacking works with LSTM and GRU layers, which give deep LSTMs and deep GRUs.

## 2. Prerequisites

- The [RNN forward propagation Note](../1056-rnn-forward-propagation/note.md): one recurrent layer, $h_t = \tanh(x_t W_i + h_{t-1} W_h + b_h)$, and counting its parameters.
- The [RNN sentiment analysis Note](../1057-rnn-sentiment-analysis/note.md): the IMDB reviews, the `Embedding` layer and `return_sequences`.
- The [types of RNN Note](../1058-types-of-rnn/note.md): many-to-one and many-to-many, and what `return_sequences=True` returns.
- The [LSTM Note](../1061-lstm/note.md), the [LSTM architecture Note](../1062-lstm-architecture/note.md) and the [GRU Note](../1064-gru/note.md): the two gated layers that can replace the simple recurrent layer.
- The [MLP intuition Note](../1009-mlp-intuition/note.md): why more layers and more nodes let a network fit more complex patterns.

## 3. Why stack recurrent layers

> **Key point:** In an ANN, a network that underfits gets better when we add nodes or hidden layers, because its representation power grows. A deep RNN applies the same idea to recurrent layers.

Take a spiral-shaped dataset, a classic non-linear problem, and a small ANN with one hidden layer of 4 nodes. After hundreds of epochs it still labels most of the plane wrongly: the network is too simple for the pattern.

- **Add nodes** to the hidden layer, and the fit improves.
- **Add a second hidden layer**, and the fit improves again.

Each change increases the **representation power** of the network: the variety of patterns it can express (see the [MLP intuition Note](../1009-mlp-intuition/note.md)).

An RNN has the same handle. A simple RNN for sentiment analysis has one recurrent layer, unfolded over the words of a review. If its accuracy is too low, we can add a second recurrent layer above the first, and a third above that. There is no limit to the stacking. Each added layer is unfolded over the same time steps. Stacking recurrent layers and unfolding them all through time is the whole idea of a deep RNN.

## 4. The architecture of a deep RNN

> **Key point:** Layer 1 reads the input at each time step. Every higher layer reads the hidden state of the layer below at the same time step, plus its own hidden state from the previous time step.

### 4.1 One recurrent layer, as a reminder

> **Key point:** One layer: the word goes in through $W_i$, the previous hidden state through $W_h$, and the last hidden state goes to the output.

Take three toy reviews of three words each, with a sentiment of 1 (positive) or 0 (negative). Each review is one **observation** (one record of the data), and its sentiment is the **target** (the output we predict).

| Review | Sentiment |
|---|---|
| cat mat rat | 1 |
| rat rat mat | 1 |
| mat mat cat | 0 |

With one-hot encoding, each word is 3 numbers: cat $= [1, 0, 0]$, mat $= [0, 1, 0]$, rat $= [0, 0, 1]$. Each of the 3 positions is one input **feature** (one input variable). A single recurrent layer of 3 nodes reads cat at $t = 1$, mat at $t = 2$ and rat at $t = 3$, starting from $h_0 = 0$. Its input weights are $3 \times 3$, its feedback weights $3 \times 3$, and after the last word its hidden state goes to a sigmoid output node (see the [forward propagation Note](../1056-rnn-forward-propagation/note.md)).

### 4.2 Two recurrent layers

> **Key point:** Layer 1 now hands its hidden state up at **every** time step, not only at the last one. Layer 2 treats that sequence of hidden states as its input sequence.

Now we use two recurrent layers: layer 1 with 3 nodes and layer 2 with 2 nodes. The two layers can have the same or a different number of nodes.

1. **Layer 1** reads the words, exactly as before. But instead of keeping its output until the end, it sends its hidden state $h^{(1)}_t$ up to layer 2 at every time step.
2. **Layer 2** receives $h^{(1)}_t$ as its input at time $t$, plus its own previous hidden state $h^{(2)}_{t-1}$. Both layers start from a vector of zeros (or random numbers).
3. After the last time step, the hidden state of the **top** layer, $h^{(2)}_3$, goes to the sigmoid output node.

The connections of the stack are:

| Connection | Shape |
|---|---|
| input to layer 1, $W^{(1)}_i$ | $3 \times 3$ |
| layer 1 to itself (feedback), $W^{(1)}_h$ | $3 \times 3$ |
| layer 1 to layer 2, $W^{(2)}_i$ | $3 \times 2$ |
| layer 2 to itself (feedback), $W^{(2)}_h$ | $2 \times 2$ |
| layer 2 to output, $W_y$ | $2 \times 1$ |

Figure 1 shows the stack unfolded over the three time steps. Each layer has its own weights, shared across all time steps, as in a single RNN. The information flows in two directions: along the time axis inside each layer, and up the layers at each time step.

## 5. Notation: time axis and depth axis

> **Key point:** An unfolded deep RNN is a grid. $h^{(l)}_t$ is the hidden state of layer $l$ at time step $t$; it is computed from the cell below, $h^{(l-1)}_t$, and the cell to its left, $h^{(l)}_{t-1}$.

![An unfolded deep RNN with 3 layers and 4 time steps is a grid with two axes. The highlighted cell $h^{(2)}_3$ receives $h^{(1)}_3$ from the layer below and $h^{(2)}_2$ from the previous time step](images/deep_grid.png){width=75%}

Figure 2 has two axes:

- the **time axis**, indexed by $t$: which word we are at;
- the **depth axis**, indexed by $l$: which layer we are in.

Each cell of the grid gets a name with both indices: $h^{(l)}_t$, the hidden state of layer $l$ at time $t$. The highlighted cell is $h^{(2)}_3$. Its two inputs are named the same way:

- from below: $h^{(l-1)}_t$, the same time step, the previous layer;
- from the left: $h^{(l)}_{t-1}$, the same layer, the previous time step.

Its output also goes two ways: up, as the input of layer $l + 1$, and right, as the previous hidden state of the next time step.

1. **In words:** each cell is an ordinary recurrent layer whose "input" is the hidden state of the layer below. Every layer $l$ has its own input weights $W^{(l)}_i$, feedback weights $W^{(l)}_h$ and bias $b^{(l)}$. For the first layer, the "layer below" is the input itself.
2. **Formula:**
   $$h^{(l)}_t = \tanh\big(h^{(l-1)}_t W^{(l)}_i + h^{(l)}_{t-1} W^{(l)}_h + b^{(l)}\big), \qquad h^{(0)}_t = x_t, \qquad h^{(l)}_0 = 0$$
   With $L$ layers and $T$ time steps, the prediction is $\hat{y} = g\big(h^{(L)}_T W_y + b_y\big)$.
3. **Example:** layer 2 with 2 nodes, at time $t$. The layer below gives $h^{(1)}_t = [0.5, -0.2, 0.1]$; layer 2's previous state is $h^{(2)}_{t-1} = [0.3, 0.0]$; the bias is 0, and
   $$W^{(2)}_i = \begin{bmatrix} 0.4 & 0.1 \\ 0.0 & 0.5 \\ -0.2 & 0.3 \end{bmatrix}, \qquad W^{(2)}_h = \begin{bmatrix} 0.6 & 0.0 \\ 0.1 & 0.2 \end{bmatrix}$$
   $$h^{(1)}_t W^{(2)}_i = [0.5 \times 0.4 + 0 - 0.1 \times 0.2,\ 0.5 \times 0.1 - 0.2 \times 0.5 + 0.1 \times 0.3] = [0.18, -0.02]$$
   $$h^{(2)}_{t-1} W^{(2)}_h = [0.3 \times 0.6 + 0,\ 0.3 \times 0 + 0] = [0.18, 0.00]$$
   $$h^{(2)}_t = \tanh([0.36, -0.02]) = [0.345, -0.020]$$

The Notebook runs this two-layer forward pass by hand on the three toy reviews and gets the same predictions as Keras.

## 6. Deep RNNs in Keras

> **Key point:** Stack recurrent layers in a `Sequential` model. Every recurrent layer except the last one needs `return_sequences=True`, so the next layer receives a sequence.

### 6.1 The model

> **Key point:** An `Embedding` layer, two `SimpleRNN` layers of 5 nodes, one sigmoid node.

The IMDB reviews of the [RNN sentiment analysis Note](../1057-rnn-sentiment-analysis/note.md) are loaded with a vocabulary capped at 10,000 words and padded or cut to 100 words. Each word becomes a vector of 32 numbers through an `Embedding` layer.

> **Python:** A deep RNN with two recurrent layers.
>
> ```python
> model = keras.Sequential([
>     keras.Input(shape=(100,)),
>     keras.layers.Embedding(10000, 32),
>     # layer 1 hands up its hidden state at every step
>     keras.layers.SimpleRNN(5, return_sequences=True),
>     # layer 2: only its last hidden state
>     keras.layers.SimpleRNN(5),
>     keras.layers.Dense(1, activation="sigmoid")])
> ```

### 6.2 Counting the parameters

> **Key point:** Embedding 320,000; layer 1: $32 \times 5 + 5 \times 5 + 5 = 190$; layer 2: $5 \times 5 + 5 \times 5 + 5 = 55$; output 6. The second layer's input size is the first layer's number of nodes.

| Layer | Computation | Parameters |
|---|---|---|
| `Embedding(10000, 32)` | $10{,}000 \times 32$ | 320,000 |
| `SimpleRNN(5)`, layer 1 | $W^{(1)}_i$: $32 \times 5$, $W^{(1)}_h$: $5 \times 5$, bias 5 | 190 |
| `SimpleRNN(5)`, layer 2 | $W^{(2)}_i$: $5 \times 5$, $W^{(2)}_h$: $5 \times 5$, bias 5 | 55 |
| `Dense(1)` | 5 weights, 1 bias | 6 |
| **Total** | | **320,251** |

`model.summary()` in the Notebook gives the same numbers. For the toy stack of section 4.2 the counts are $9 + 9 + 3 = 21$ for layer 1, $6 + 4 + 2 = 12$ for layer 2 and $2 + 1 = 3$ for the output.

### 6.3 Why `return_sequences=True`

> **Key point:** Without it, the lower layer outputs only its last hidden state, so the upper layer has no sequence to read, and Keras refuses to build the model.

By default a Keras recurrent layer returns only its last hidden state, one vector per review (see the [types of RNN Note](../1058-types-of-rnn/note.md)). The layer above needs one vector **per time step**: the upward arrows of Figure 1. `return_sequences=True` makes the lower layer return all of them, a tensor of shape (batch size, time steps, nodes), here (batch size, 100, 5).

- **Every recurrent layer except the last** needs `return_sequences=True`. Without it the upward connections break: Keras raises an error, because the upper layer expects a 3D input and gets a 2D one (Notebook).
- **The last recurrent layer** keeps the default for a many-to-one task such as sentiment analysis, because the output layer needs only the last time step. For a many-to-many task, where the output layer needs a prediction at every time step, the last recurrent layer also returns sequences.

## 7. Why use a deep RNN

> **Key point:** Two reasons: stacked layers can learn a hierarchy, from simple features low down to more abstract ones higher up; and complex architectures, such as encoder-decoder translation systems, are built from deep RNNs.

### 7.1 Hierarchical representation

> **Key point:** Lower layers turn the raw input into simpler features; higher layers build more abstract features from them.

Text has a hierarchy: words make sentences, sentences make a review. A stack of recurrent layers can follow it. In a product review such as "The audio is bad. The display is great. Overall I am happy.":

- **lower layers** can pick up word-level features: words such as love, hate, amazing, terrible;
- **middle layers** can combine them at the level of a phrase or sentence: "the audio is bad";
- **higher layers** can combine the sentences into the overall sentiment of the review: happy, despite the bad audio.

This picture is an intuition about what each layer specialises in. Goodfellow §10.5 states the general idea: the lower layers of the hierarchy can be thought of as transforming the raw input into a representation that is more appropriate for the higher levels of the hidden state. Graves et al. (2013) were the first to show a significant benefit from splitting the state of an RNN into several layers this way (Goodfellow §10.5).

### 7.2 Building blocks for advanced architectures

> **Key point:** Encoder-decoder systems for machine translation use deep recurrent layers in both the encoder and the decoder.

Deep RNNs also serve as parts of larger architectures. An encoder-decoder model for machine translation, with an attention mechanism, can use a deep RNN as its encoder and another as its decoder. Google's neural machine translation system used a deep LSTM network with 8 encoder and 8 decoder layers, with attention; its authors found that both had to be deep enough to reach good accuracy (Wu et al. 2016). Encoder-decoder models and attention have their own Notes later.

## 8. When to use a deep RNN

> **Key point:** Try a deep RNN for complex tasks, with a lot of data, when the computing power is there and a single-layer model is not good enough.

1. **Complex tasks.** Speech recognition and machine translation are the standard examples (Graves et al. 2013 in Goodfellow §10.5; Wu et al. 2016).
2. **Large datasets.** A deep RNN has more parameters. On a small dataset it is likely to overfit, so deep RNNs need a lot of data (see the [improving a neural network Note](../1021-improving-a-neural-network/note.md)).
3. **Enough computing resources.** More layers mean more parameters and longer training; on a weak machine, training can take too long.
4. **A single layer is not good enough.** Start with a single-layer RNN as a baseline. If its results are not satisfactory, a deep RNN is a natural next step.

RESULTS_PLACEHOLDER

## 9. Deep LSTMs and deep GRUs

> **Key point:** Stacking works with any recurrent layer. In practice deep RNNs are built from LSTM or GRU layers, because simple recurrent layers still suffer from vanishing and exploding gradients.

Replacing `SimpleRNN` by `LSTM` in the model of section 6 gives a **deep LSTM**; replacing it by `GRU` gives a **deep GRU**. Nothing else changes: the same `return_sequences=True` on every layer but the last.

| Model (5 nodes per layer) | Layer 1 | Layer 2 | Total with embedding and output |
|---|---|---|---|
| deep SimpleRNN | 190 | 55 | PARAMS_RNN |
| deep LSTM | 760 | 220 | PARAMS_LSTM |
| deep GRU | 585 | 180 | PARAMS_GRU |

The LSTM layer has four times the weights of a simple recurrent layer, one set per gate and one for the candidate cell state (see the [LSTM architecture Note](../1062-lstm-architecture/note.md)); the GRU layer has three (see the [GRU Note](../1064-gru/note.md)). In practice, deep RNNs are mostly built from LSTM or GRU layers: a stack of simple recurrent layers still has the vanishing and exploding gradient problems of the [problems with RNNs Note](../1060-problems-with-rnn/note.md).

Training works as before. Backpropagation through time (see the [BPTT Note](../1059-backpropagation-through-time/note.md)) now runs over a grid instead of a chain: a gradient can travel back along the time axis, down the depth axis, or both. The bookkeeping is harder by hand, but Keras builds the computation graph and computes every gradient automatically. Dropout and the other techniques of earlier Notes apply unchanged.

## 10. Disadvantages

> **Key point:** More layers mean more parameters: a higher risk of overfitting and a longer training time.

1. **Overfitting.** A more complex network overfits more easily. Design it carefully: use [dropout](../1024-dropout/note.md), [regularisation](../1026-regularization-in-dl/note.md), a carefully chosen learning rate and a good [weight initialisation](../1030-xavier-he-initialization/note.md).
2. **Training time.** More parameters mean more derivatives to compute and more weights to update at every step, so training takes longer, especially on a large dataset.

## 11. Summary

| | Single-layer RNN | Deep (stacked) RNN |
|---|---|---|
| Recurrent layers | 1 | 2 or more, stacked |
| Input of a recurrent layer at time $t$ | $x_t$ | $x_t$ for layer 1; $h^{(l-1)}_t$ for layer $l$ |
| Unfolded shape | a chain (time axis) | a grid (time axis and depth axis) |
| Keras | one recurrent layer | `return_sequences=True` on every recurrent layer but the last |
| Strength | simple, fast | more representation power: hierarchical features |
| Cost | | more parameters, more overfitting risk, longer training |

- A deep RNN stacks recurrent layers; each is unfolded through time.
- $h^{(l)}_t = \tanh\big(h^{(l-1)}_t W^{(l)}_i + h^{(l)}_{t-1} W^{(l)}_h + b^{(l)}\big)$, with $h^{(0)}_t = x_t$.
- Each layer has its own weights; the second layer's input size is the first layer's number of nodes.
- Use it for complex tasks with a lot of data, after a single-layer baseline.
- In practice, stack LSTM or GRU layers: deep LSTMs and deep GRUs.

## 12. Sources

- Goodfellow, I., Bengio, Y. and Courville, A. (2016). *Deep Learning*. MIT Press. Chapter 10, §10.5 (deep recurrent networks). deeplearningbook.org/contents/rnn.html.
- Graves, A., Mohamed, A. and Hinton, G. (2013). Speech Recognition with Deep Recurrent Neural Networks. ICASSP 2013. Cited through Goodfellow §10.5.
- Wu, Y., Schuster, M., Chen, Z., Le, Q. V., Norouzi, M. et al. (2016). Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation. arXiv:1609.08144.
- Keras API documentation: `SimpleRNN`, `LSTM` and `GRU` layers (`return_sequences`), keras.io/api/layers/recurrent_layers/.

## 13. Key terms

| Term | Meaning |
|---|---|
| Deep RNN (stacked RNN) | An RNN with two or more recurrent layers stacked on top of each other, all unfolded through time |
| Deep LSTM, deep GRU | A deep RNN whose recurrent layers are LSTM or GRU layers |
| Observation | One record of the data, here one review |
| Feature | An input variable; here one of the numbers that represent a word |
| Target | The output we predict, here the sentiment |
| Representation power | The variety of patterns a network can express; grows with more nodes and layers |
| Time axis and depth axis | The two directions of an unfolded deep RNN: time steps and layers |
| $h^{(l)}_t$ | The hidden state of layer $l$ at time step $t$ |
| Hierarchical representation | Features built in levels: simple ones in lower layers, more abstract ones in higher layers |
| `return_sequences=True` | Makes a Keras recurrent layer return its hidden state at every time step; needed on every stacked layer but the last |
