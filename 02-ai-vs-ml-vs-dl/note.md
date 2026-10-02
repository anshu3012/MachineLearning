---
title: "Video 2: AI vs ML vs DL"
subtitle: "100 Days of Machine Learning, CampusX"
---

**Video:** [AI Vs ML Vs DL for Beginners](https://www.youtube.com/watch?v=1v3_AQ26jZ0)

## In one picture

![](images/big_picture.png)

Three circles, one inside the other. **Deep Learning** is a kind of **Machine Learning**, and Machine Learning is a kind of **Artificial Intelligence**.

Almost everyone draws this picture, and it is correct. This Note explains *why* it looks like this: what each circle means, why the inner circles appeared, and when to use which.

## Before you start

Nothing. This is the first teaching Video of the course.

## The Teacher's flow

### 1. The question

"What is the difference between AI, ML and DL?" is one of the most common beginner and interview questions. The usual answer is the picture above. But a picture is not an explanation, so he goes through them one by one, starting from the outside.

### 2. Artificial Intelligence (AI)

**AI** is the idea of putting *intelligence* into a machine. People have dreamed of this for a very long time: a machine that is smart the way we are.

But what is **intelligence**? It is the reason humans are ahead of every other living species. When you look into it, intelligence turns out to be not one thing but many abilities mixed together:

![](images/intelligence.png)

We use some of these abilities to write code, others to solve a puzzle, and others to be creative or to understand someone's feelings.

The big dream is **general AI**: one machine with *all* of these abilities, exactly like a human. We are not there. Some of these abilities, like creativity or love, we cannot even define properly ourselves, so how would we build them?

So in practice, almost everything called "AI" today copies **one narrow ability** at a time: recognising faces, translating text, playing chess.

> **Extra (not in the video):** You will see these called **narrow AI** (one task) and **AGI**, *artificial general intelligence* (all tasks, like a human). Every AI product you have used so far is narrow AI.

### 3. How AI started: rules written by humans

![](images/timeline.png)

The idea of a thinking machine took off in the **1950s**. The first serious attempt was **symbolic AI**: if we want a machine to be smart, let's *write down* the knowledge it needs as rules.

The most famous result was the **expert system**. As a child you may have played chess against a computer. That kind of program is an expert system:

![](images/expert_system.png)

1. Sit down with a **human expert** (a doctor, a chess master) and get all their knowledge out of them.
2. Turn that knowledge into rules (the **knowledge base**).
3. A program (the **inference engine**) uses those rules to answer your question.

For a while everyone thought expert systems were the future of AI.

**Where they broke.** Expert systems only work on problems with **clear, fixed rules**: chess, logic puzzles, some medical checks. Now take a problem whose rules are fuzzy:

> *Is there a dog in this photo?*

Try writing the rules. There are hundreds of dog breeds. Each has a different size, colour, ear shape and tail. The photo can be taken from any angle, in any light. You cannot write rules for all of that. The same happened with recognising speech and many other everyday tasks.

So expert systems fell behind, and a new approach came along that could handle these problems: **Machine Learning**.

> **Extra (not in the video):** The "1950s" start is usually traced to Alan Turing's 1950 paper asking *"Can machines think?"*. The decades on the middle two boxes of the timeline are rough guides that I added, not dates from the video.

### 4. Machine Learning (ML)

**Machine Learning** is a branch of computer science that uses **statistics** to find **patterns in data**.

The most important difference from what came before: in ML **you never write the rules yourself** (no *explicit programming*). Instead, you give the computer data together with the right answers, and the computer works out the rules.

![](images/rules_vs_data.png)

**Back to the dog photo.**

- *Symbolic AI way:* write rules for every breed, every colour, every ear shape. Impossible.
- *ML way:* show the system thousands of photos, each labelled "dog" or "not dog". It slowly figures out on its own what makes a dog a dog. This figuring-out is what we call **learning**. After enough photos, show it a new photo it has never seen, and it can tell you whether there is a dog in it.

Your job changes from *writing rules* to *giving good data*.

This is exactly how you learned as a child. Nobody gave you a rulebook for dogs. Someone pointed and said "that's a dog, that's not a dog", and after enough examples you just knew. ML is inspired by that.

**Why ML is everywhere now.** ML ideas are old, but they really took over industry in the last 20 to 30 years, for two reasons:

1. **Lots of data**, because the internet and phones produce huge amounts of it.
2. **Better hardware**, because computers became fast and cheap enough to learn from that data.

ML leans heavily on statistics, but day to day it is a very practical, engineering kind of work.

### 5. Deep Learning (DL)

If ML is so good, why do we need Deep Learning at all? He answers in two parts: what DL is, then why it is needed.

#### What DL is

DL is **a part of ML**. The work started long ago, but it only really took off after about 2010.

The overall process is the same as ML: give data to an algorithm, **train** it (let it learn, and keep reducing its mistakes), then use it to **predict** on new data.

What is different is the *kind* of algorithm. DL uses **neural networks**, which are inspired by the **neurons** in our brain.

Be careful, though: *inspired by* does not mean *works like*. We still don't fully understand how the brain works, so we cannot copy it. A neural network is a mathematical model that borrowed the brain's basic idea. Its smallest building block is called a **perceptron** (an artificial neuron). You will meet it properly later in the course.

#### Why DL is needed: features

The biggest limitation of ML is **features**.

A **feature** is one piece of information about each example that you hand to the model. In ML, **you** have to decide which features to give it.

**His example: will a student get placed?** Suppose you want to predict whether a student will get a job in campus placements.

- In ML, you sit down and decide the features yourself: CGPA, IQ, number of certifications... Then you reason about them: *more than two certifications $\rightarrow$ better chance; CGPA in some range $\rightarrow$ maybe 50% chance*.
- To pick good features, you must **understand the data well**. Choosing the right features is hard, and if you miss a useful one, the model can never use it.

**In DL, the network finds the features by itself.** You give it the raw data, and it works out which pieces of information matter.

![](images/features_ml_vs_dl.png)

This is the key difference: **in ML you build the features; in DL you don't need to worry about them.** That makes DL useful for problems where *nobody knows* what the right features are, like "what makes a photo a dog photo?".

#### Layers: why "deep"?

A neural network is built in **layers** of neurons, one after another. The more layers you add, the more hidden patterns the network can pull out of the data, and the better it gets at its task. Many layers stacked up is what makes it *deep*.

His example is recognising a handwritten digit:

![](images/layers_digit.gif)

1. The **first layer** finds tiny **edges**: short straight bits.
2. The **next layer** joins edges into **shapes**: a long bar, a slanted line.
3. The **next layer** joins shapes into an answer: *this is a 7*.

Each layer builds on the one before it. Small, simple pieces become bigger, more meaningful ideas.

> **Extra (not in the video):** Real networks do not label their layers "edges" or "shapes". Researchers looked inside trained networks and found that early layers *happen* to react to edges and later layers to bigger parts. The picture above is a simplified version of what they saw.

#### Data vs performance

The second big reason for DL is how it behaves as you give it **more data**.

![](images/data_vs_performance.png)

- An **ML** model improves as you add data, but only up to a point. Then it levels off: more data stops helping.
- A **DL** model keeps improving as you keep adding data.

That is why DL beats ML at tasks where huge amounts of data exist: **recognising images, finding objects in photos, and working with text and speech**. On these, DL left 20 years of ML work behind.

### 6. So should we always use DL? No.

DL needs **a lot of data**. Without it, it does worse than ML (the grey area on the left of the chart).

When you work in industry, you will find that many companies, like **banks and insurance companies**, simply do not have that much data. For them, ML is still the better choice, and it is used heavily.

**Rule of thumb:**

- Small or medium data, especially tables of numbers $\rightarrow$ **ML**
- Huge data, especially images, text or speech $\rightarrow$ **DL**

### 7. The big picture

The final goal of the field is still **general AI**. We are not there yet, and nobody knows how long it will take. Along the way, we have found two very effective ways to solve real problems: **ML** and **DL**. Today, both are widely used.

## Cheat sheet

| | **AI** | **ML** | **DL** |
|---|---|---|---|
| What it is | Any way of making a machine act smart | Machine learns the rules from data | ML using neural networks with many layers |
| Who writes the rules? | Humans (symbolic AI / expert systems) | The machine | The machine |
| Who picks the features? | (no learning) | **You** | **The network** |
| Needs lots of data? | No | Some | **A lot** |
| Good at | Problems with clear rules (chess) | Tables of data (banking, insurance) | Images, text, speech |

- AI $\supset$ ML $\supset$ DL: every DL system is ML, and every ML system is AI.
- Expert systems failed on fuzzy problems, because nobody can write rules for "dog".
- ML: give **data + answers**, get **rules**. No explicit programming.
- DL removes the hardest part of ML, which is picking features.
- More data $\rightarrow$ DL keeps improving; ML levels off.
- Little data $\rightarrow$ use ML.

**New terms in this Note:** see the [glossary](../glossary.md).
