# Moved from RO-013 (Belief: What the Robot Knows) on 2026-10-10: Markov chains and the transition matrix

Text from RO-013 §5.1 (the hallway robot: 10 cells in a loop, the command "move 2" moves it 1, 2 or 3 cells with probability 0.1, 0.8, 0.1). RO-013 keeps only the one-sentence definition of a Markov chain.

**A small piece of maths: Markov chains.** A sequence of states where the next state depends only on the current one is a **Markov chain** (G-2437) (CS188 §8.1). Our robot repeating "move 2" without looking is one. Its transition probabilities fit in a table with one row per "from" cell and one column per "to" cell, the **transition matrix** (G-2438). Row 1 of our 10 × 10 transition matrix, with columns for cells 0 to 9, is:

$$(0,\ 0,\ 0.1,\ 0.8,\ 0.1,\ 0,\ 0,\ 0,\ 0,\ 0)$$

Every row has the same three numbers, shifted to start at its own cell. Every row adds to 1, because from any cell the robot ends somewhere.

Glossary row to restore:

| <span id="G-2438">G-2438</span> | Transition matrix | A table of a Markov chain's transition probabilities, one row per "from" state and one column per "to" state, each row adding to 1; it stores in one place how the state moves. | [Note RO-013](RO/localization/02-bayes-filters/RO-013-belief/RO-013-belief.md#51-how-a-command-moves-the-robot-the-state-transition-probability) | Hidden Markov model |

Also removed from RO-013 with the hidden-Markov-model name table (restore where hidden Markov models are taught):

| <span id="G-2440">G-2440</span> | Emission probability | The HMM name for the measurement probability: the probability of each observation given each hidden state, stored as a table with one row per state and one column per observation; it links what is seen to what is hidden. | [Note RO-013](RO/localization/02-bayes-filters/RO-013-belief/RO-013-belief.md#63-hidden-markov-model) | Hidden Markov model |
