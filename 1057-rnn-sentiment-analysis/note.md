---
title: "Sentiment Analysis with an RNN in Keras"
tags: [subject/deep-learning, area/dl-rnn, step/features, step/model, concept/rnn, concept/sequence-padding, concept/text-vectorization, concept/word-embedding]
---

## 1. Overview

> **Key point:** An RNN only reads numbers, so text must become numbers first. Two ways: integer encoding (each word becomes its index in the vocabulary) and a learned embedding (each word becomes a short, dense vector that the network learns). On IMDB movie reviews, the same SimpleRNN reaches about 0.80 test accuracy with an embedding, against 0.50 with raw integers.

**Sentiment analysis** is the task of predicting whether a text is positive or negative. The data is a set of texts, each with a label: 1 for positive, 0 for negative. This Note builds a sentiment analysis model with the RNN of the [RNN forward propagation Note](../1056-rnn-forward-propagation/note.md), in Keras, on real movie reviews.

The aim is the workflow, not the best accuracy: how text becomes numbers, how the numbers enter a `SimpleRNN`, and what changes when a learned embedding is added.

![IMDB reviews cut to their last 50 words. Dashed: training accuracy; solid: test accuracy; mean of 3 runs. Raw integer inputs stay near a coin toss; a learned 2-number embedding lifts the same SimpleRNN to about 0.80 on the test reviews](images/imdb_curves.png){width=95%}

Figure 1 is the result of the whole Note.

## 2. Prerequisites

- The [RNN forward propagation Note](../1056-rnn-forward-propagation/note.md): input shape (time steps, input features), the recurrent layer, counting its parameters.
- The [why RNNs Note](../1055-why-rnn/note.md): padding sequences to a common length, and its cost.
- The [MNIST ANN Note](../1012-mnist-ann/note.md): `compile`, `fit` and validation data in Keras.
- The [one-hot encoding Note](../27-one-hot-encoding/note.md): a category as a vector with a single 1.

## 3. Integer encoding

> **Key point:** Build the vocabulary, give each word an integer, replace every word by its integer, then pad the sequences to one length.

### 3.1 The three steps

> **Key point:** Vocabulary, replace, pad.

Each review is one **observation** (one record of the data), and its label is the **target** (the output we predict). Before an RNN can read the reviews, every word must become a number. **Integer encoding** does it in three steps.

![Integer encoding of two sentences: build the vocabulary and number its words, replace every word by its number, then pad the shorter sequence with 0](images/integer_encoding.png){width=100%}

1. **Vocabulary.** List the unique words of the whole document, the **vocabulary**, and give each one an integer: hi is 1, there is 2, how is 3, are is 4, you is 5.
2. **Replace.** Write every sentence as the integers of its words: "hi there" becomes $[1, 2]$ and "how are you" becomes $[3, 4, 5]$.
3. **Pad.** The sequences have different lengths, so add zeros at the start or the end of the shorter ones until all have the same length: $[1, 2, 0]$ and $[3, 4, 5]$. The integer 0 is kept for padding, so no word gets it.

Figure 2 shows the three steps.

### 3.2 Tokenizing in Keras

> **Key point:** Keras' `TextVectorization` layer lower-cases the text, strips punctuation, splits it into words, builds the vocabulary and replaces each word by its index, in one step.

Splitting a text into words is **tokenization**. Doing it by hand means lower-casing every word, removing punctuation and numbering the words; Keras does all of it.

Take a document of 10 short cheering slogans, such as "go india", "india india" and "jeetega bhai jeetega india jeetega". `adapt` reads the document and builds the vocabulary, most frequent word first. The Notebook prints 19 entries:

| Index | Entry |
|---|---|
| 0 | `""` (padding) |
| 1 | `[UNK]` (unknown word) |
| 2 | india |
| 3 | jeetega |
| ... | 15 more words |

"india" appears 4 times, more than any other word, so it gets the first free index, 2.

**Out-of-vocabulary words.** A word seen only at prediction time, never in training, has no index. The layer maps every such word to a special **out-of-vocabulary (OOV) token**, `[UNK]`, with index 1. In the Notebook, "go pakistan" becomes $[16, 1]$: "pakistan" is not in the vocabulary.

> **Python:** Integer encoding with `TextVectorization`; it also pads the sequences with 0 at the end.
>
> ```python
> import keras
> docs = ["go india", "india india", "hip hip hurray", ...]
> vectorizer = keras.layers.TextVectorization()
> vectorizer.adapt(docs)               # build the vocabulary
> print(vectorizer.get_vocabulary())   # ['', '[UNK]', 'india', ...]
> sequences = vectorizer(docs).numpy() # one padded row per sentence
> ```

For lists of integers of different lengths, `keras.utils.pad_sequences(sequences, padding="post")` pads at the end, and `padding="pre"` (the default) at the start (Keras documentation).

> **Extra:** Older Keras code uses `keras.preprocessing.text.Tokenizer` with `fit_on_texts`, `word_index`, `word_counts` and `texts_to_sequences`, and an `oov_token` argument. Keras 3 keeps that class only as a legacy API; `TextVectorization` is its replacement, and it reserves index 0 for padding and index 1 for `[UNK]` (Keras documentation, `TextVectorization`).

## 4. The IMDB dataset

> **Key point:** 50,000 movie reviews, half for training and half for testing, already integer encoded. We pad or cut every review to 50 words.

### 4.1 Loading the reviews

> **Key point:** `keras.datasets.imdb.load_data()` returns the reviews as lists of integers, one integer per word.

The **IMDB dataset** holds 50,000 movie reviews from the Internet Movie Database, labelled positive or negative: 25,000 for training and 25,000 for testing (Keras documentation, IMDB dataset). Keras ships it already tokenized and integer encoded, so the steps of section 3 are done. The first training review starts

$$[1, 14, 22, 16, 43, 530, 973, 1622, 1385, 65, \dots]$$

where 1 marks the start of a review and every other integer is a word. Decoded with the dataset's word index, it reads "this film was just brilliant casting location scenery story direction everyone's really suited the part they played and you ...".

> **Extra:** In `load_data`, a word's integer is its frequency rank plus 3: 0 is padding, 1 is the start marker and 2 is the out-of-vocabulary word. So the most frequent word, "the", is 4 (Keras source, `imdb.load_data`: `start_char=1`, `oov_char=2`, `index_from=3`).

### 4.2 Cutting every review to 50 words

> **Key point:** Reviews have different lengths (the first three have 218, 189 and 141 words). `pad_sequences(maxlen=50)` pads the short ones and cuts the long ones to 50 words, so training is fast.

Training on full reviews is slow, so we keep 50 words per review: `keras.utils.pad_sequences(X, maxlen=50)`. Shorter reviews get zeros in front; longer reviews are cut. The training data then has shape $(25000, 50)$. The cut throws information away: the median review has 178 words. With time, use full reviews.

**Which 50 words?** `pad_sequences` cuts from the start by default (`truncating="pre"`), so a long review keeps its **last** 50 words, not its first 50 (Keras documentation, `pad_sequences`). Passing `truncating="post"` keeps the first 50.

## 5. Approach 1: integer encoding into a SimpleRNN

> **Key point:** Feed each review as 50 time steps of 1 number each, into a SimpleRNN of 32 nodes and a sigmoid output node: 1,088 + 33 parameters.

### 5.1 The model

> **Key point:** Input shape $(50, 1)$: 50 time steps, 1 input feature, the word's integer.

> **Python:** The model for raw integer inputs.
>
> ```python
> model = keras.Sequential([
>     keras.Input(shape=(50, 1)),    # (time steps, input features)
>     keras.layers.SimpleRNN(32, return_sequences=False),
>     keras.layers.Dense(1, activation="sigmoid")])
> ```

Each review is 50 integers. At time step 1 the first integer enters the recurrent layer, at time step 2 the second, and so on, as in the [RNN forward propagation Note](../1056-rnn-forward-propagation/note.md). After the 50th, the last hidden state goes to the sigmoid node, which gives $\hat{y}$.

### 5.2 Counting the parameters

> **Key point:** $32 + 32 \times 32 + 32 = 1088$ in the recurrent layer and $32 + 1 = 33$ in the output layer.

| Part | Count |
|---|---|
| $W_i$: 1 input feature to 32 nodes | $1 \times 32 = 32$ |
| $W_h$: feedback, 32 nodes to 32 nodes | $32 \times 32 = 1024$ |
| $b_h$ | 32 |
| **SimpleRNN total** | **1,088** |
| $W_o$ and $b_o$ | $32 + 1 = 33$ |

`model.summary()` prints the same numbers.

### 5.3 `return_sequences`

> **Key point:** `return_sequences=False` (the default) returns only the last hidden state. `return_sequences=True` returns the hidden state of every time step.

The recurrent layer computes a hidden state at every time step. With `return_sequences=False`, only the last one leaves the layer; the others stay inside and only feed the next time step. Sentiment analysis needs one answer per review, after the last word, so `False` is right here.

Some tasks need an output at every word: named entity recognition labels each word (for example, is it a person's name?), and machine translation produces a sentence. Those use `return_sequences=True`. The [types of RNN Note](../1058-types-of-rnn/note.md) covers these cases.

### 5.4 Training

> **Key point:** Binary cross-entropy, Adam, 5 epochs, the test reviews as validation data. Raw integers give a test accuracy near a coin toss.

We compile with binary cross-entropy loss and the Adam optimizer, train for 5 epochs and pass the test reviews as `validation_data`. Averaged over 3 runs, the model reaches 0.50 training accuracy and 0.50 test accuracy after 5 epochs (grey lines in Figure 1). With two balanced classes, guessing gives 0.50.

Only 50 words per review and only 5 epochs make the task harder. But the embedding model of section 7 gets the same 50 words and the same 5 epochs and reaches 0.80. The main difference between the two models is how a word enters the RNN (the embedding model also keeps only the 10,000 most frequent words), so the representation of the words is what holds this model back.

## 6. Word embeddings

> **Key point:** An embedding turns each word into a short vector of real numbers, most of them non-zero, learned so that words used in similar ways get similar vectors.

### 6.1 Sparse and dense representations

> **Key point:** Padding and one-hot vectors are mostly zeros (sparse). An embedding is short and full of useful numbers (dense).

Two problems come with the earlier representations.

- **Sparse.** Take a 20-word review padded to the longest review of 2,000 words: 1,980 of its 2,000 numbers are padding zeros. A one-hot vector over a 10,000-word vocabulary is 9,999 zeros and one 1. A representation where most values are 0 is **sparse**.
- **No meaning.** Integers and one-hot vectors say nothing about meaning. In one-hot space every pair of words is the same distance apart, $\sqrt{2}$, so "good" is as far from "great" as from "awful" (Goodfellow §12.4.2).

A **word embedding** represents each word as a real-valued vector of a chosen, small size, such as 2 or 32 numbers, most of them non-zero: a **dense** representation. The vectors are learned so that words that appear in similar contexts are close to each other, which often puts words with similar meanings next to each other (Goodfellow §12.4.2).

### 6.2 Learning the embedding with the model

> **Key point:** Keras' `Embedding` layer learns the vectors during training, by backpropagation, together with the RNN.

Word2Vec and GloVe are well-known embedding methods trained on large text collections. In deep learning we can also learn an embedding as part of our own model: Keras' `Embedding` layer turns each integer into a dense vector of fixed size (Keras documentation, `Embedding`). Its input must be integer encoded.

`Embedding` takes two main arguments:

- `input_dim`: the vocabulary size;
- `output_dim`: the size of each word's vector, a hyperparameter (2, 32, 200, ...) to tune.

> **Extra:** Older code also passes `input_length`, the number of words per sequence. Keras 3 removed that argument; the sequence length comes from the input shape (`keras.Input(shape=(50,))`) instead (Keras documentation, `Embedding`).

### 6.3 What the layer computes

> **Key point:** The layer holds a weight matrix $E$ with one row per word. A word's vector is its row of $E$: a one-hot vector times $E$, done as a lookup.

1. **In words:** the layer is like a dense layer whose input is the word's one-hot vector, with no bias and no activation. Multiplying a one-hot vector by a matrix picks one row, so the layer simply looks up row $k$ for word $k$.
2. **Formula:** for a vocabulary of $V$ words and vectors of size $d$, $E$ is $V \times d$, and
   $$\text{embedding}(k) = \text{onehot}(k)\thinspace E = E_{k,:}$$
3. **Example:** the slogan document has $V = 19$ entries. With $d = 2$, $E$ is $19 \times 2$: 38 weights, which `model.summary()` confirms. The first word of the first slogan, "go", has index 16, and row 16 of $E$ is its 2-number vector: $[-0.039, -0.006]$ before training.

![The embedding layer as a lookup: the one-hot vector of "go" (index 16) times $E$ keeps row 16 of $E$, which becomes the word's dense vector](images/embedding_lookup.png){width=80%}

$E$ starts random and is trained with the rest of the network by backpropagation. Figure 3 shows the lookup. The Notebook checks that the one-hot product and the layer's output are the same numbers.

Applied to a padded sequence of 5 integers, the layer returns 5 rows of 2 numbers, one per word (the padding index 0 also gets a row). For the 10 slogans, padded to 5 words, the output has shape $(10, 5, 2)$: 100 numbers.

## 7. Approach 2: an embedding into the same SimpleRNN

> **Key point:** Keep the 10,000 most frequent words, embed each in 2 numbers, and feed the 50 vectors into the SimpleRNN. Test accuracy rises to about 0.80.

### 7.1 The model

> **Key point:** Embedding (20,000 parameters), SimpleRNN (1,120), Dense (33).

`load_data(num_words=10000)` keeps the 10,000 most frequent words; every rarer word becomes the out-of-vocabulary integer 2.

> **Python:** The embedding model.
>
> ```python
> model = keras.Sequential([
>     keras.Input(shape=(50,)),             # 50 integers per review
>     keras.layers.Embedding(10000, 2),     # each word -> 2 numbers
>     keras.layers.SimpleRNN(32),
>     keras.layers.Dense(1, activation="sigmoid")])
> ```

Now each time step carries 2 numbers instead of 1, so the RNN's input is (50 time steps, 2 input features).

| Layer | Parameters |
|---|---|
| Embedding: $E$ | $10000 \times 2 = 20000$ |
| SimpleRNN: $W_i$, $W_h$, $b_h$ | $2 \times 32 + 32 \times 32 + 32 = 1120$ |
| Dense: $W_o$, $b_o$ | $32 + 1 = 33$ |

### 7.2 Results

> **Key point:** Same RNN, same 50 words, same 5 epochs: the embedding lifts test accuracy from 0.50 to 0.80. Training accuracy climbs higher still, a sign of overfitting.

| After 5 epochs, mean of 3 runs | Integer encoding | Embedding |
|---|---|---|
| Training accuracy | 0.50 | 0.90 |
| Test accuracy | 0.50 | 0.80 |

The green lines of Figure 1 show the embedding model. Test accuracy peaks at epoch 2 (0.80) while training accuracy keeps rising to 0.90: the model is starting to memorise the training reviews, which is **overfitting**. The [regularization Note](../1026-regularization-in-dl/note.md) and the [early stopping Note](../1022-early-stopping/note.md) cover the remedies.

### 7.3 What the embedding learned

> **Key point:** After training, positive and negative words sit in different parts of the 2-number space.

![The learned 2-number vectors of a few IMDB words after training. Positive words (green) and negative words (red) end up on opposite sides; frequent neutral words (grey) sit between them](images/embedding_words.png){width=85%}

Figure 4 plots the learned vectors of 8 positive, 8 negative and 8 neutral words. Nobody told the network which words are positive. Goodfellow §12.4.2 explains the pattern: words that share features learned by the model end up close together. The only label this model learns from is the sentiment, and Figure 4 shows its embedding sorting the words by sentiment along one direction.

### 7.4 Learned or pre-trained embeddings

> **Key point:** We can learn the embedding with the model, as here, or load pre-trained vectors such as Word2Vec or GloVe.

A pre-trained embedding was learned on a large general text collection. An embedding learned with the model is fitted to our own data and task. Which works better depends on the dataset.

## 8. Summary

| | Integer encoding | Embedding |
|---|---|---|
| A word becomes | 1 number, its index | a learned vector of $d$ numbers |
| Representation | arbitrary numbers, sparse after padding | dense, similar words close |
| RNN input shape | (50, 1) | (50, $d$) |
| Extra parameters | none | vocabulary size $\times\ d$ |
| IMDB test accuracy, 5 epochs | 0.50 | 0.80 |

- Text must become numbers: build a vocabulary, replace words by integers, pad to one length.
- `TextVectorization` tokenizes and integer encodes; unknown words map to `[UNK]`; `pad_sequences` pads and cuts.
- IMDB comes integer encoded; `pad_sequences(maxlen=50)` keeps the last 50 words of each review.
- `SimpleRNN(32)` on 1 input feature has 1,088 parameters; `return_sequences=False` returns only the last hidden state.
- An `Embedding` layer is a lookup table $E$, trained with the model; it turned a coin toss into about 0.80 accuracy.

## 9. Sources

- Goodfellow, I., Bengio, Y. and Courville, A. (2016). *Deep Learning*. MIT Press. §12.4.2 (neural language models, word embeddings). deeplearningbook.org/contents/applications.html.
- Keras API documentation: `TextVectorization`, `pad_sequences`, `Embedding`, `SimpleRNN` layers, and the IMDB dataset (`keras.datasets.imdb.load_data`), keras.io/api/. Checked against the installed Keras 3.15 source.
- Maas, A. L. et al. (2011). Learning Word Vectors for Sentiment Analysis. ACL 2011. (The IMDB dataset.)

## 10. Key terms

| Term | Meaning |
|---|---|
| Sentiment analysis | Predicting whether a text is positive or negative |
| Observation | One record of the data, here one review |
| Target | The output we predict, here the sentiment label |
| Vocabulary | The set of unique words in the data, each with an integer index |
| Tokenization | Splitting a text into words (tokens) |
| Integer encoding | Replacing each word by its index in the vocabulary |
| Out-of-vocabulary (OOV) token | A placeholder, `[UNK]`, for words not in the vocabulary |
| Padding | Adding zeros to sequences so that all have the same length |
| Sparse representation | A representation where most values are 0 |
| Dense representation | A short representation where most values are non-zero |
| Word embedding | A learned real-valued vector for each word; words used in similar ways get nearby vectors |
| `Embedding` layer | The Keras layer holding the embedding matrix $E$; looks up one row per word |
| `return_sequences` | SimpleRNN argument: `False` returns the last hidden state, `True` returns every hidden state |
| IMDB dataset | 50,000 labelled movie reviews, shipped with Keras already integer encoded |
| Overfitting | Training accuracy rising while test accuracy stalls or falls |
