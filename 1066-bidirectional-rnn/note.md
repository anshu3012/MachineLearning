---
title: "Bidirectional RNNs"
---

## 1. Overview

> **Key point:** A bidirectional RNN runs two RNNs over the same sequence, one from left to right and one from right to left, and joins their hidden states at every time step. Each output can then use both the past and the future of the sequence.

A **bidirectional RNN** (Schuster and Paliwal 1997) combines an RNN that moves forward through time, from the start of the sequence, with another that moves backward through time, from the end (Goodfellow §10.3). The RNNs of the earlier Notes read only from left to right, so the output at a time step can depend only on the inputs up to that step. A bidirectional RNN removes that limit.

![A bidirectional RNN on "Amazon is a website". The forward RNN (blue) reads left to right; the backward RNN (green) reads right to left. At every time step their two hidden states are joined to give the output, so $\hat{y}_1$, the output for "Amazon", already depends on "website"](images/birnn_unrolled.png){width=100%}

Figure 1 shows the structure. The idea works with any recurrent layer: with LSTM layers it is called a **BiLSTM**, with GRU layers a **BiGRU**.

## 2. Prerequisites

- The [RNN forward propagation Note](../1056-rnn-forward-propagation/note.md): $h_t = \tanh(x_t W_i + h_{t-1} W_h + b_h)$ and counting parameters.
- The [RNN sentiment analysis Note](../1057-rnn-sentiment-analysis/note.md): IMDB and the `Embedding` layer.
- The [types of RNN Note](../1058-types-of-rnn/note.md): many-to-many models and `return_sequences=True`; part-of-speech tagging and named entity recognition.
- The [LSTM architecture Note](../1062-lstm-architecture/note.md) and the [GRU Note](../1064-gru/note.md): the gated layers that can be made bidirectional.
- The [deep RNNs Note](../1065-deep-rnns/note.md): stacking recurrent layers.

## 3. Why read a sequence in both directions

> **Key point:** In a unidirectional RNN the output at time $t$ depends only on the inputs up to $t$. Some tasks need later inputs to decide an earlier output.

### 3.1 The limit of a unidirectional RNN

> **Key point:** Information flows only forward, so the past can affect an output but the future cannot.

Every RNN so far is **unidirectional**: it reads $x_1$, then $x_2$, then $x_3$. The output at the last step depends on $x_3$, $x_2$ and $x_1$: on all the past inputs. Goodfellow §10.3 calls this a "causal" structure: the state at time $t$ captures only information from the past and the present input.

Now suppose the correct output at an early time step depends on an input that comes later. A unidirectional RNN, whether simple, LSTM or GRU, has not yet read that input when it must give the output, so it fails.

### 3.2 An example: named entity recognition

> **Key point:** In "I love Amazon. It's a great website" the word Amazon is an organisation; in "I love Amazon. It's a beautiful river" it is a location. Reading left to right, the words that decide come after Amazon.

**Named entity recognition** (NER) is the task of labelling the names in a sentence with their type: a person, a location, an organisation (see the [types of RNN Note](../1058-types-of-rnn/note.md)). Chatbots use it to pick names and places out of messages. Take two sentences:

- "I love Amazon. It's a great website." Here Amazon is an **organisation**.
- "I love Amazon. It's a beautiful river." Here Amazon is a **location**.

A tagger reading left to right reaches Amazon with exactly the same context, "I love", in both sentences. Until it reads the next sentence, it cannot tell the organisation from the river. The next inputs decide the output at an earlier step: that is the situation a bidirectional RNN is built for. Machine translation has the same need: a word of the output may depend on parts of the input that come later.

Goodfellow §10.3 gives a speech example: the correct interpretation of the current sound may depend on the next few sounds, and even on the next few words.

## 4. How a bidirectional RNN works

> **Key point:** Two separate RNNs read the sequence in opposite directions. At every time step their hidden states are concatenated, and the output layer reads the joined vector.

### 4.1 Two RNNs, opposite directions

> **Key point:** The forward RNN starts at $x_1$ from a vector of zeros; the backward RNN starts at $x_T$ from a vector of zeros.

Take the four words "Amazon is a website" as $x_1, x_2, x_3, x_4$.

1. **The forward RNN** (blue in Figure 1) is the RNN we know. It starts from $\overrightarrow{h}_0$, zeros or random numbers, reads Amazon, is, a, website, and produces $\overrightarrow{h}_1, \dots, \overrightarrow{h}_4$.
2. **The backward RNN** (green) is a second, separate RNN with its own weights. It starts from zeros at the other end, reads website, a, is, Amazon, and produces $\overleftarrow{h}_4, \dots, \overleftarrow{h}_1$.
3. **At every time step**, the two hidden states are **concatenated** (placed one after the other in a single vector), and the output layer turns the joined vector into $\hat{y}_t$.

The two RNNs do not feed each other: the outputs of the forward states are not connected to the inputs of the backward states, and the other way round (Schuster and Paliwal 1997). They meet only at the output.

### 4.2 Why the output now sees the future

> **Key point:** $\overleftarrow{h}_1$ is the backward RNN's last state: it has read every word. So $\hat{y}_1$ depends on the whole sentence.

Look at the output for Amazon, $\hat{y}_1$, in Figure 1.

- Its forward part, $\overrightarrow{h}_1$, has read only Amazon.
- Its backward part, $\overleftarrow{h}_1$, has read website, a, is and Amazon: it is the last state of the backward RNN.

So every word, including "website", contributes to the label of Amazon. "Website" points to an organisation, not a location. In general, the output at each step gets a summary of the past from the forward RNN and a summary of the future from the backward RNN, while staying most sensitive to the inputs around time $t$ (Goodfellow §10.3).

### 4.3 The equations

> **Key point:** The forward equation uses $\overrightarrow{h}_{t-1}$, the backward equation uses $\overleftarrow{h}_{t+1}$, and the output uses both, joined.

1. **In words:** the forward state at $t$ comes from the input and the forward state at $t - 1$. The backward state at $t$ comes from the input and the backward state at $t + 1$, the step it read just before. The output applies its activation to the joined pair.
2. **Formula:** each RNN has its own weights and bias:
   $$\overrightarrow{h}_t = \tanh\big(x_t \overrightarrow{W}_i + \overrightarrow{h}_{t-1} \overrightarrow{W}_h + \overrightarrow{b}\big), \qquad \overrightarrow{h}_0 = 0$$
   $$\overleftarrow{h}_t = \tanh\big(x_t \overleftarrow{W}_i + \overleftarrow{h}_{t+1} \overleftarrow{W}_h + \overleftarrow{b}\big), \qquad \overleftarrow{h}_{T+1} = 0$$
   $$\hat{y}_t = g\big([\overrightarrow{h}_t, \overleftarrow{h}_t]\, W_y + b_y\big)$$
   where $[\,\cdot\,,\,\cdot\,]$ joins two row vectors into one and $g$ is the output activation, a sigmoid or a softmax.
3. **Example:** with 2 nodes in each direction, suppose $\overrightarrow{h}_1 = [0.3, -0.1]$ and $\overleftarrow{h}_1 = [0.6, 0.2]$. The output layer receives the 4 numbers
   $$[\overrightarrow{h}_1, \overleftarrow{h}_1] = [0.3, -0.1, 0.6, 0.2]$$
   so $W_y$ has 4 rows: twice as many as for one direction.

The Notebook builds a Keras bidirectional layer, runs the forward and backward equations by hand with its weights, and gets exactly its output at every time step.

## 5. Bidirectional RNNs in Keras

> **Key point:** Wrap any recurrent layer in `keras.layers.Bidirectional`. The wrapper makes a second copy for the backward direction, so the layer's parameters double.

### 5.1 The wrapper

> **Key point:** One line changes: `SimpleRNN(5)` becomes `Bidirectional(SimpleRNN(5))`.

> **Python:** The IMDB model of the [RNN sentiment analysis Note](../1057-rnn-sentiment-analysis/note.md), made bidirectional.
>
> ```python
> model = keras.Sequential([
>     keras.Input(shape=(100,)),
>     keras.layers.Embedding(10000, 32),
>     keras.layers.Bidirectional(keras.layers.SimpleRNN(5)),
>     keras.layers.Dense(1, activation="sigmoid")])
> ```

By default the wrapper concatenates the two directions (`merge_mode="concat"`); it can also add, average or multiply them (Keras documentation, `Bidirectional`). Without `return_sequences=True`, as here, it returns the forward RNN's last state joined with the backward RNN's last state, which is $\overleftarrow{h}_1$.

### 5.2 Counting the parameters

> **Key point:** Two RNNs instead of one: 190 becomes 380 for `SimpleRNN(5)`. The layer after it also gets twice as many inputs.

| Recurrent layer (5 nodes, input 32) | Unidirectional | Bidirectional |
|---|---|---|
| `SimpleRNN` | 190 | 380 |
| `LSTM` | 760 | 1,520 |
| `GRU` | 585 | 1,170 |

The `Dense(1)` output layer grows too, from $5 + 1 = 6$ to $10 + 1 = 11$ parameters, because it reads 10 joined numbers instead of 5.

Wrapping an `LSTM` gives a BiLSTM and wrapping a `GRU` gives a BiGRU. The bidirectional simple RNN is rarely used; BiLSTMs and BiGRUs are the common choices in practice, for the reasons of the [problems with RNNs Note](../1060-problems-with-rnn/note.md).

## 6. Experiment: tagging the parts of speech

> **Key point:** On real Wall Street Journal sentences, a BiLSTM tags parts of speech more accurately than a unidirectional LSTM, also when the unidirectional one gets the same number of parameters. Most of the gain is on words whose tag depends on what follows.

RESULTS_PLACEHOLDER

## 7. Applications

> **Key point:** Use a bidirectional RNN when the whole sequence is available and an output may depend on later inputs: tagging, named entity recognition, translation, and often sentiment analysis.

1. **Named entity recognition**, as in section 3.2.
2. **Part-of-speech tagging**, as in section 6: each word gets its grammatical class.
3. **Machine translation.** Google's neural machine translation system made the first layer of its encoder bidirectional, to have the best possible context at each point (Wu et al. 2016).
4. **Sentiment analysis.** Bidirectional RNNs are worth trying here too; the whole review is available before the prediction.

Bidirectional RNNs have been extremely successful in handwriting recognition, speech recognition and bioinformatics (Goodfellow §10.3).

## 8. Disadvantages

> **Key point:** Twice the parameters, so more training time and more overfitting risk; and the whole sequence must be available before any output, which adds latency in real-time tasks.

1. **Complexity.** The recurrent layer has twice the parameters, so training takes longer and the network can overfit more easily. The usual remedies apply: [dropout](../1024-dropout/note.md) and [regularisation](../1026-regularization-in-dl/note.md).
2. **The whole sequence must be available.** The backward RNN starts at the last input. In **real-time speech recognition**, the words arrive one by one while the person speaks, so the backward RNN cannot start until the sentence is finished. The reply is delayed: a **latency** problem that a unidirectional RNN does not have. The same constraint limits parallel computation: Google's translation system kept only its bottom encoder layer bidirectional, because a layer above a bidirectional one must wait for both directions to finish (Wu et al. 2016).

## 9. Summary

| | Unidirectional RNN | Bidirectional RNN |
|---|---|---|
| Reads | left to right | left to right and right to left |
| Output at time $t$ depends on | $x_1, \dots, x_t$ | the whole sequence $x_1, \dots, x_T$ |
| Recurrent layers | 1 | 2 separate ones, joined at every step |
| Parameters | $P$ | $2P$ (and a wider next layer) |
| Keras | `LSTM(64)` | `Bidirectional(LSTM(64))` |
| Needs the full sequence first | no | yes: latency in real-time tasks |

- A bidirectional RNN joins a forward RNN and a backward RNN at every time step: $\hat{y}_t = g([\overrightarrow{h}_t, \overleftarrow{h}_t] W_y + b_y)$.
- The backward state at $t$ comes from $\overleftarrow{h}_{t+1}$, so every output sees the future of the sequence.
- It helps when an output depends on later inputs: tagging, NER, translation.
- It doubles the parameters and needs the whole sequence before any output.

## 10. Sources

- Goodfellow, I., Bengio, Y. and Courville, A. (2016). *Deep Learning*. MIT Press. Chapter 10, §10.3 (bidirectional RNNs). deeplearningbook.org/contents/rnn.html.
- Schuster, M. and Paliwal, K. K. (1997). Bidirectional Recurrent Neural Networks. *IEEE Transactions on Signal Processing* 45(11), 2673–2681.
- Tjong Kim Sang, E. F. and Buchholz, S. (2000). Introduction to the CoNLL-2000 Shared Task: Chunking. CoNLL 2000. (The tagged Wall Street Journal sentences.)
- Wu, Y., Schuster, M., Chen, Z., Le, Q. V., Norouzi, M. et al. (2016). Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation. arXiv:1609.08144.
- Keras API documentation: `Bidirectional` layer (`merge_mode`, default `"concat"`), keras.io/api/layers/recurrent_layers/bidirectional.

## 11. Key terms

| Term | Meaning |
|---|---|
| Bidirectional RNN | Two RNNs reading a sequence in opposite directions, their hidden states joined at every time step |
| Unidirectional RNN | An RNN that reads in one direction only, so its output at $t$ depends only on inputs up to $t$ |
| Forward and backward RNN | The left-to-right and the right-to-left halves of a bidirectional RNN |
| BiLSTM, BiGRU | A bidirectional RNN made of LSTM or GRU layers |
| Concatenation | Placing two vectors one after the other to form one longer vector |
| Named entity recognition (NER) | Labelling the names in a text with their type, such as person, location or organisation |
| Part-of-speech tagging | Labelling every word of a sentence with its grammatical class, such as noun or verb |
| Observation | One record of the data, here one sentence |
| Target | The output we predict, here the tag of each word |
| Latency | The delay between an input and the system's reply |
| `Bidirectional` | The Keras wrapper that makes any recurrent layer bidirectional |
