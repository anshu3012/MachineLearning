# Moved from RO-013 (Belief: What the Robot Knows) on 2026-10-10: Bayesian networks

Text from RO-013 §6.1. RO-013 keeps a two-sentence recap before drawing the robot as a dynamic Bayes network.

### 6.1 A small piece of maths: Bayesian networks

Many probability models are easiest to read as a drawing. Each variable is a circle. Arrows go into a variable from the variables its probability depends on directly; in robot models they usually run from cause to effect. Each variable then needs only one table: its probability given the variables with arrows into it, its **parents**. Such a drawing is a **Bayesian network** (G-2442) (CS188 §6.3). The probability of all variables together is the product of these tables, one per circle.

Why a product? The [chain rule of probability](../../../ML/07-classification/ML-082-naive-bayes-maths/ML-082-naive-bayes-maths.md#4-step-2-the-chain-rule) (G-369) always writes a joint probability as a product of conditional probabilities. The missing arrows say which conditions can be dropped, so each factor shrinks to "given my parents" (CS188 §6.3).

From RO-013 §6.4 (deleted): for the robot's dynamic Bayes network, the joint probability of one whole run (the hidden cells together with the commands and readings) is the starting belief times one factor per arrow: the state transition probability for each move and the measurement probability for each reading. So a joint probability over many variables is a product of small local tables.

Glossary row to restore:

| <span id="G-2442">G-2442</span> | Bayesian network | A drawing of random variables as circles with arrows into each from the variables it depends on directly (its parents), plus one table per variable giving its probability given its parents; the probability of all variables together is the product of those tables. | [Note RO-013](RO/localization/02-bayes-filters/RO-013-belief/RO-013-belief.md#61-a-small-piece-of-maths-bayesian-networks) | Hidden Markov model |
