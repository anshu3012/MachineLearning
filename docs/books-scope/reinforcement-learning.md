# Scope: Reinforcement Learning, from Sutton & Barto to the 2025 frontier

**Summary.** This is a scoping list only, not study Notes. Proposed: **about 108 concept Notes** (Section 7), 42 of them robotics. Parts:

- **A. Backbone book:** Sutton and Barto, *Reinforcement Learning: An Introduction*, 2nd ed., MIT Press 2018. Free from the authors at <http://incompleteideas.net/book/the-book-2nd.html>. The chapter and section list below comes from the contents pages of the authors' PDF (`RLbook2020.pdf`, linked on that page). 17 chapters in 3 parts: tabular methods (Ch. 2–8), approximate methods (Ch. 9–13), looking deeper (Ch. 14–17).
- **B–E. Concepts beyond the book:** classic and deep RL ideas, RL for robotics, and the frontier (RLHF, LLM reasoning, model-based, offline, robot foundation models). Rows are **concepts and skills**; papers are only the sources that teach and back them ("Taught with" column). Every source was checked on its arXiv abstract page, Crossref (by DOI) or the publisher page; see Section 3.
- **Robotics (Section 2D):** nine concept blocks R0–R8: foundations, sim-to-real, task design, partial observability and privileged information, safety and constraints, **autonomous navigation (primary, deepest)**, legged locomotion, humanoids, manipulation. A skills view for navigation is in 2D.10.
- **Lectures:** three DeepMind x UCL playlists, checked with `yt-dlp --flat-playlist` (Section 4). They are the primary lecture companion to the book. Robotics companions (CS285 2023, Abbeel's series, framework docs and code) are in Section 4.3.

This scope lists **308 concepts**: **3 covered**, **60 partial**, **245 new**
(maths: 65, RL: 153, robotics: 90). The robotics pass replaced the old 12-row robotics table with 118 concept rows (R0–R8), so robotics went from 20 to 90 concepts. Our Notes give almost all the *tools* (probability, expectation, MLE, gradients, SGD, optimizers, neural nets, CNN, LSTM, transformers). Almost all the *RL ideas* are new: Note 03 only names agent, environment, policy and reward, and Note 1067 describes RLHF in three sentences.

Status key:
- **covered**: we already have it; the Note folder is named.
- **partial**: we have the basics, but RL goes further; the new part is named.
- **new**: not in our Notes.

Kind key: **maths** (a general tool, useful outside RL), **RL** (an RL idea or algorithm), **robotics** (about robots or sim-to-real).

---

## 1. Sutton & Barto, chapter by chapter

### Ch. 1 Introduction

| Chapter | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|
| 1 Introduction | RL as learning from interaction: agent, environment, reward | RL | partial | 03 names agent, environment, policy, reward; new: the reward is a number to be maximised over time, and it can arrive late |
| 1 Introduction | Exploration vs exploitation trade-off | RL | partial | 134 shows a sampler exploring then settling; new: the trade-off as the central problem of acting |
| 1 Introduction | Four elements: policy, reward signal, value function, model | RL | partial | 03 has policy and reward; new: value function and model of the environment |
| 1 Introduction | Tic-tac-toe: learning state values from game outcomes | RL | new | First example of a temporal-difference update |
| 1 Introduction | Evolutionary (policy search) vs value-function methods | RL | new | Two families of solution |
| 1 Introduction | History: optimal control, trial-and-error, temporal differences | RL | new | Context only |

### Part I: Tabular solution methods

| Chapter | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|
| 2 Multi-armed Bandits | k-armed bandit problem; true action value q*(a) | RL | new | One state, many actions, noisy rewards |
| 2 Multi-armed Bandits | Sample-average action-value estimate | maths | partial | 221 mean; new: one running mean per action |
| 2 Multi-armed Bandits | Greedy and ε-greedy action selection | RL | new | Mostly pick the best, sometimes pick at random |
| 2 Multi-armed Bandits | 10-armed testbed (averaging over many runs) | RL | new | How RL methods are compared |
| 2 Multi-armed Bandits | Incremental update: new = old + step × (target − old) | maths | partial | 1033 EWMA; new: step 1/n gives the exact mean; this "error-correction" form is in every later RL update |
| 2 Multi-armed Bandits | Constant step size = exponential recency-weighted average | maths | covered | 1033 |
| 2 Multi-armed Bandits | Step-size conditions (Σα = ∞, Σα² < ∞) | maths | new | When a running estimate is sure to converge (Robbins–Monro) |
| 2 Multi-armed Bandits | Optimistic initial values | RL | new | Start high so every action gets tried |
| 2 Multi-armed Bandits | Upper-confidence-bound (UCB) selection | RL | partial | 280 confidence intervals; new: pick the action whose upper bound is highest |
| 2 Multi-armed Bandits | Gradient bandit: softmax over preferences, baseline | RL | partial | 79 softmax, 1074 softmax gradient; new: gradient ascent on expected reward, with a baseline |
| 2 Multi-armed Bandits | Contextual bandits (associative search) | RL | new | Bandit whose best arm depends on a situation |
| 3 Finite MDPs | Agent–environment interface: state, action, reward, time step | RL | partial | 03 loop figure; new: the formal per-step interface |
| 3 Finite MDPs | Markov property | maths | new | Next state and reward depend only on the current state and action |
| 3 Finite MDPs | Markov chain: transition matrix, stationary distribution | maths | new | Needed for the on-policy distribution (Ch. 9) and average reward (Ch. 10) |
| 3 Finite MDPs | MDP dynamics p(s', r given s, a) | maths | partial | 341 conditional probability; new: a joint distribution of next state and reward |
| 3 Finite MDPs | Reward hypothesis: goals as summed reward | RL | new | |
| 3 Finite MDPs | Return, episodes, episodic vs continuing tasks | RL | new | |
| 3 Finite MDPs | Discounted return and the geometric series | maths | new | γ < 1 keeps an infinite sum finite |
| 3 Finite MDPs | Policy π(a given s) as a conditional distribution | RL | partial | 03 policy as a rule book; new: probabilities over actions |
| 3 Finite MDPs | State-value v_π and action-value q_π | maths | partial | 332 expected value; new: expectation over all future steps |
| 3 Finite MDPs | Bellman expectation equation | maths | new | Builds on 332 expectation and 86 total probability |
| 3 Finite MDPs | Backup diagrams | RL | new | Picture of what an update averages over |
| 3 Finite MDPs | Optimal value functions v*, q*; Bellman optimality equation | maths | new | Expectation replaced by a max over actions |
| 3 Finite MDPs | Optimal policy = greedy with respect to q* | RL | new | |
| 3 Finite MDPs | Bellman equation as a linear system v = (I − γP)⁻¹r | maths | partial | 54 matrix inverse; new: solving for all state values at once |
| 3 Finite MDPs | Optimality vs approximation (tabular vs approximate) | RL | new | |
| 4 Dynamic Programming | Iterative policy evaluation | RL | new | Sweep the Bellman expectation update until values settle |
| 4 Dynamic Programming | Policy improvement theorem | maths | new | Acting greedily on v_π never makes the policy worse |
| 4 Dynamic Programming | Policy iteration | RL | new | Evaluate, improve, repeat |
| 4 Dynamic Programming | Value iteration | RL | new | Bellman optimality update in a loop |
| 4 Dynamic Programming | Asynchronous DP | RL | new | Update states in any order |
| 4 Dynamic Programming | Generalized policy iteration (GPI) | RL | new | The pattern behind every later control method |
| 4 Dynamic Programming | Bootstrapping (update a guess from a guess) | RL | new | |
| 4 Dynamic Programming | Efficiency of DP and the curse of dimensionality | maths | partial | 46 curse of dimensionality; new: state count grows exponentially with state variables |
| 5 Monte Carlo Methods | Monte Carlo estimation (average sampled returns) | maths | partial | 241/331 law of large numbers, 271 CLT; new: estimating an expectation by averaging random episodes |
| 5 Monte Carlo Methods | First-visit and every-visit MC prediction | RL | new | |
| 5 Monte Carlo Methods | MC estimation of action values | RL | new | |
| 5 Monte Carlo Methods | Exploring starts and MC control | RL | new | |
| 5 Monte Carlo Methods | ε-soft on-policy MC control | RL | new | |
| 5 Monte Carlo Methods | On-policy vs off-policy; target vs behaviour policy | RL | new | |
| 5 Monte Carlo Methods | Importance sampling ratio; ordinary vs weighted IS | maths | new | Reweight samples from one distribution to estimate another |
| 5 Monte Carlo Methods | Variance of IS estimators (can be infinite) | maths | partial | 332 variance; new: why weighted IS is preferred |
| 5 Monte Carlo Methods | Incremental weighted average | maths | partial | 1033; new: weights that change per sample |
| 5 Monte Carlo Methods | Off-policy MC control | RL | new | |
| 5 Monte Carlo Methods | Discounting-aware and per-decision IS (starred) | maths | new | Lower-variance IS for returns |
| 6 Temporal-Difference Learning | TD(0) prediction and the TD error δ | RL | new | The central idea of the book |
| 6 Temporal-Difference Learning | TD as sampling (MC) plus bootstrapping (DP) | RL | new | |
| 6 Temporal-Difference Learning | Batch TD vs batch MC; certainty-equivalence estimate | maths | partial | 631 MLE; new: batch TD(0) gives the answer of the maximum-likelihood Markov model |
| 6 Temporal-Difference Learning | Sarsa (on-policy TD control) | RL | new | |
| 6 Temporal-Difference Learning | Q-learning (off-policy TD control) | RL | new | |
| 6 Temporal-Difference Learning | Expected Sarsa | RL | new | |
| 6 Temporal-Difference Learning | Maximization bias and double Q-learning | RL | new | max of noisy estimates is biased upward |
| 6 Temporal-Difference Learning | Afterstates | RL | new | |
| 7 n-step Bootstrapping | n-step return and n-step TD | RL | new | Between TD (n = 1) and MC (n = ∞) |
| 7 n-step Bootstrapping | n-step Sarsa | RL | new | |
| 7 n-step Bootstrapping | n-step off-policy learning with IS | RL | new | |
| 7 n-step Bootstrapping | Control variates (starred) | maths | new | Subtract something with known mean to cut variance |
| 7 n-step Bootstrapping | Tree-backup algorithm | RL | new | Off-policy without IS |
| 7 n-step Bootstrapping | n-step Q(σ) | RL | new | Unifies sampling and expectation |
| 8 Planning and Learning | Distribution models vs sample models | RL | new | |
| 8 Planning and Learning | Dyna-Q: planning, acting and learning together | RL | new | |
| 8 Planning and Learning | Wrong models; Dyna-Q+ exploration bonus | RL | new | |
| 8 Planning and Learning | Prioritized sweeping | RL | new | Uses a priority queue (owned by Planning Algorithms scope, Ch. 2) |
| 8 Planning and Learning | Expected vs sample updates | RL | new | |
| 8 Planning and Learning | Trajectory sampling and real-time DP | RL | new | |
| 8 Planning and Learning | Decision-time planning and heuristic search | RL | new | A* and heuristics owned by Planning Algorithms scope; RL recaps |
| 8 Planning and Learning | Rollout algorithms | RL | new | |
| 8 Planning and Learning | Monte Carlo tree search (selection, expansion, simulation, backup) | RL | new | Core of AlphaGo |

### Part II: Approximate solution methods

| Chapter | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|
| 9 On-policy Prediction with Approximation | Value-function approximation as supervised learning | RL | partial | 50–55 regression, 1010 networks; new: the targets come from the agent itself and keep changing |
| 9 On-policy Prediction with Approximation | Prediction objective VE (MSE weighted by state-visit frequency μ) | maths | partial | 52 MSE; new: weights from the on-policy distribution |
| 9 On-policy Prediction with Approximation | Stochastic-gradient and semi-gradient methods | maths | partial | 59 SGD; new: the target uses the weights but is not differentiated |
| 9 On-policy Prediction with Approximation | Linear methods and the TD fixed point | maths | partial | 53 multiple regression; new: where linear TD converges and its error bound |
| 9 On-policy Prediction with Approximation | Polynomial features | maths | covered | 61 |
| 9 On-policy Prediction with Approximation | Fourier basis features | maths | new | |
| 9 On-policy Prediction with Approximation | Coarse coding | RL | new | |
| 9 On-policy Prediction with Approximation | Tile coding | RL | new | |
| 9 On-policy Prediction with Approximation | Radial basis function features | maths | partial | 95 RBF kernel; new: RBFs as state features |
| 9 On-policy Prediction with Approximation | Choosing the step size by hand | maths | partial | 1032 learning rate; new: α ≈ 1/(τ E[xᵀx]) |
| 9 On-policy Prediction with Approximation | Neural networks as approximators | maths | covered | 1010, 1015–1017, 1020 |
| 9 On-policy Prediction with Approximation | Least-squares TD (LSTD) | maths | partial | 54 normal equation; new: solve the TD fixed point directly |
| 9 On-policy Prediction with Approximation | Memory-based (nearest-neighbour) approximation | maths | partial | 91 KNN; new: used for values |
| 9 On-policy Prediction with Approximation | Kernel-based approximation | maths | partial | 95 kernel trick; new: used for values |
| 9 On-policy Prediction with Approximation | Interest and emphasis | RL | new | |
| 10 On-policy Control with Approximation | Episodic semi-gradient Sarsa (mountain car) | RL | new | |
| 10 On-policy Control with Approximation | Semi-gradient n-step Sarsa | RL | new | |
| 10 On-policy Control with Approximation | Average-reward setting, differential return and values | maths | new | Needs the Markov chain's stationary distribution |
| 10 On-policy Control with Approximation | Why discounting breaks with approximation | RL | new | |
| 10 On-policy Control with Approximation | Differential semi-gradient n-step Sarsa | RL | new | |
| 11 Off-policy Methods with Approximation | Off-policy semi-gradient methods | RL | new | |
| 11 Off-policy Methods with Approximation | Off-policy divergence (Baird's counterexample) | RL | new | |
| 11 Off-policy Methods with Approximation | The deadly triad (approximation + bootstrapping + off-policy) | RL | new | Why DQN needed tricks |
| 11 Off-policy Methods with Approximation | Linear value-function geometry: projection, Bellman operator, projected Bellman error | maths | partial | 520 projection; new: projection in a weighted norm |
| 11 Off-policy Methods with Approximation | Gradient descent in the Bellman error (residual gradient) | maths | new | |
| 11 Off-policy Methods with Approximation | The Bellman error is not learnable | RL | new | |
| 11 Off-policy Methods with Approximation | Gradient-TD methods (GTD2, TDC) | RL | new | |
| 11 Off-policy Methods with Approximation | Emphatic-TD methods | RL | new | |
| 12 Eligibility Traces | λ-return | RL | new | Average of all n-step returns, weights (1 − λ)λⁿ⁻¹ |
| 12 Eligibility Traces | Eligibility trace vector; TD(λ); forward vs backward view | RL | new | |
| 12 Eligibility Traces | Truncated λ-return, online λ-return, true online TD(λ), dutch traces | RL | new | |
| 12 Eligibility Traces | Sarsa(λ) | RL | new | |
| 12 Eligibility Traces | Variable λ and γ | RL | new | |
| 12 Eligibility Traces | Off-policy traces: Watkins's Q(λ), Tree-Backup(λ), GTD(λ), emphatic TD(λ) | RL | new | |
| 13 Policy Gradient Methods | Parameterized policy; softmax in action preferences | RL | partial | 79 softmax; new: the policy itself is the model being trained |
| 13 Policy Gradient Methods | Performance measure J(θ) | RL | new | |
| 13 Policy Gradient Methods | Policy gradient theorem | maths | new | Builds on 601 gradients, 332 expectation |
| 13 Policy Gradient Methods | Log-derivative trick ∇π / π = ∇ ln π | maths | partial | 73 log-likelihood, 74 derivative; new: gradient of an expectation through a log |
| 13 Policy Gradient Methods | REINFORCE (Monte Carlo policy gradient) | RL | new | |
| 13 Policy Gradient Methods | Baseline for variance reduction | maths | new | A control variate (Ch. 7) |
| 13 Policy Gradient Methods | One-step actor–critic | RL | new | |
| 13 Policy Gradient Methods | Policy gradient for continuing problems | RL | new | |
| 13 Policy Gradient Methods | Gaussian policy for continuous actions | maths | partial | 250 normal, 640 multivariate normal; new: gradient of the log-density in mean and σ |

### Part III: Looking deeper

| Chapter | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|
| 14 Psychology | Prediction vs control in animal learning | RL | new | |
| 14 Psychology | Classical conditioning; blocking; higher-order conditioning | RL | new | |
| 14 Psychology | Rescorla–Wagner model | RL | new | An error-correction rule like the incremental update |
| 14 Psychology | TD model of classical conditioning | RL | new | |
| 14 Psychology | Instrumental conditioning and the law of effect | RL | new | |
| 14 Psychology | Delayed reinforcement and credit assignment | RL | new | |
| 14 Psychology | Cognitive maps; habitual vs goal-directed (model-free vs model-based) | RL | new | |
| 15 Neuroscience | Reward signals vs reinforcement signals | RL | new | |
| 15 Neuroscience | Reward prediction error hypothesis and dopamine | RL | new | |
| 15 Neuroscience | TD error / dopamine correspondence | RL | new | |
| 15 Neuroscience | Neural actor–critic | RL | new | |
| 15 Neuroscience | Hedonistic neurons, collective RL, model-based methods in the brain, addiction | RL | new | |
| 16 Applications | TD-Gammon | RL | new | |
| 16 Applications | Samuel's checkers player | RL | new | |
| 16 Applications | Watson's Daily-Double wagering | RL | new | |
| 16 Applications | Optimizing memory control | RL | new | |
| 16 Applications | Human-level video game play (DQN) | RL | new | Details in Section 2C |
| 16 Applications | AlphaGo and AlphaGo Zero | RL | partial | 03 and 1003 name AlphaGo's 2016 win; new: how it works (Section 2C) |
| 16 Applications | Personalized web services (contextual bandits) | RL | new | |
| 16 Applications | Thermal soaring | RL | new | |
| 17 Frontiers | General value functions and auxiliary tasks | RL | new | |
| 17 Frontiers | Options (temporal abstraction) | RL | new | |
| 17 Frontiers | Observations and state; POMDP; state-update function | maths | new | POMDP owned by Probabilistic Robotics scope (Ch. 15); RL recaps |
| 17 Frontiers | Designing reward signals: sparse reward, shaping, imitation, inverse RL | RL | new | |
| 17 Frontiers | Remaining issues; RL and the future of AI (safety) | RL | new | |

---

## 2. Concepts beyond the book (papers are the teaching tools)

Rows are **ideas and skills**, not papers. The "Taught with" column names the sources used to teach and back each idea (all verified, Section 3). A paper may appear as a worked example inside a concept Note; it never gets a Note of its own.

### 2B. Foundations from the classic papers

| Concept | Kind | Status | Our Note / what is new | Taught with |
|---|---|---|---|---|
| Principle of optimality; the functional (Bellman) equation | maths | new | Origin of Ch. 3–4; recapped in the Bellman Note, no separate Note | Bellman 1957 |
| TD(λ) for multi-step prediction | RL | new | Origin of Ch. 6 and 12 | Sutton 1988 |
| Convergence of Q-learning (every pair visited forever, step-size conditions) | maths | new | | Watkins & Dayan 1992 |
| REINFORCE family of algorithms | RL | new | Origin of Ch. 13.3 | Williams 1992 |
| Policy gradient theorem with function approximation; compatible features | maths | new | | Sutton et al. 2000 |
| Two-timescale actor–critic (critic learns faster than actor) | maths | new | | Konda & Tsitsiklis 2000 |

### 2C. Deep RL

| Concept | Kind | Status | Our Note / what is new | Taught with |
|---|---|---|---|---|
| Deep Q-network on raw pixels | RL | partial | CNN 1040–1045; new: a CNN trained with Q-learning targets | Mnih et al. 2015 (DQN) |
| Experience replay | RL | new | Store transitions, train on random minibatches | Mnih et al. 2015 |
| Target network | RL | new | A slow copy of the network makes the target | Mnih et al. 2015 |
| Error clipping in the loss | maths | partial | 1014 Huber loss; new: used to keep TD errors bounded | Mnih et al. 2015 |
| Policy network + value network + tree search | RL | new | Supervised on human games, then self-play RL | Silver et al. 2016 (AlphaGo) |
| Self-play from scratch; MCTS as policy improvement | RL | new | One residual network, no human data | Silver et al. 2017 (AlphaGo Zero) |
| One algorithm for several board games | RL | new | | Silver et al. 2017 (AlphaZero, extra) |
| Advantage actor–critic with parallel workers; entropy bonus | RL | new | Standard stepping stone to PPO | Mnih et al. 2016 (A3C, extra) |
| Deterministic policy gradient for continuous actions | RL | new | | Lillicrap et al. 2016 (DDPG) |
| Soft (Polyak) target updates; exploration noise | RL | partial | 1033 EWMA; new: EWMA of network weights | Lillicrap et al. 2016 |
| KL divergence between policies | maths | partial | 1014 names KL; new: what it measures, how to compute it | Schulman et al. 2015 (TRPO) |
| Trust region and surrogate objective | maths | new | Limit how far one update moves the policy | Schulman et al. 2015 |
| Natural gradient, Fisher information, conjugate gradient | maths | new | Conjugate gradient also needed by Probabilistic Robotics Ch. 11 | Schulman et al. 2015 |
| Advantage function A = Q − V | RL | new | | Schulman et al. 2016 (GAE) |
| Generalized advantage estimation (λ-weighted TD errors) | RL | partial | 1033 EWMA; new: an exponentially weighted sum of TD errors | Schulman et al. 2016 |
| Clipped surrogate objective; several epochs per batch (PPO) | RL | new | The optimiser inside RLHF (1067) and inside almost every robot policy below | Schulman et al. 2017; Abbeel "Foundations of Deep RL" L4 |
| Maximum-entropy RL; soft Q; temperature | maths | partial | 97 entropy; new: entropy added to the reward | Haarnoja et al. 2018 (SAC) |
| Reparameterization trick; tanh-squashed Gaussian | maths | new | | Haarnoja et al. 2018 |
| Clipped double Q, delayed policy updates, target policy smoothing | RL | new | Builds on double Q-learning (Ch. 6.7) | Fujimoto et al. 2018 (TD3) |

### 2D. RL for robotics, by concept

The robotics part is organised as nine concept blocks, R0–R8, in learning order. Each row says what the skill is, why it matters, the RL idea underneath, what it builds on, and the sources that teach it. Row IDs (R0.1, N.4, …) are used by the skills view (2D.10) and the learning order (Section 7).

Kinds: **maths**, **RL**, **robotics** as before. "(added 2023–26)" marks recent work found during verification, beyond the minimum list.

#### R0. Robot RL foundations

| ID | Concept / skill | Kind | Status | What it is (what is new vs our Notes) | Why it matters | RL idea underneath | Builds on | Taught with |
|---|---|---|---|---|---|---|---|---|
| R0.1 | Why robot RL is hard | robotics | new | High-dimensional continuous states and actions, costly and risky real samples, model error, hard-to-write rewards | Explains every trick in R1–R8 | Sample cost and the exploration problem | S&B Ch. 1, 3 | Kober, Bagnell & Peters 2013; CS285 2023 L23 |
| R0.2 | Value-function vs policy-search methods on robots | robotics | new | Why continuous control favours policy search and actor–critic | Picks the algorithm family | Policy gradient vs value methods | S&B Ch. 9, 13 | Kober et al. 2013 |
| R0.3 | Using models, demonstrations and prior knowledge | robotics | new | Ways to cut real-robot samples | Motivates sim, imitation and residual RL | Prior knowledge as inductive bias | R0.1 | Kober et al. 2013 |
| R0.4 | The robot as an MDP: control rate, observation, action interface, episode and reset | robotics | new | Choosing the time step (e.g. physics at 200 Hz, policy at 50 Hz: legged_gym `dt = 0.005`, `decimation = 4`) and what counts as state and action | The formal MDP (Ch. 3) must be made concrete before any training | The agent–environment boundary is a design choice (S&B 3.1) | S&B Ch. 3 | S&B §3.1; legged_gym config |
| R0.5 | Joint position targets tracked by a PD controller | robotics | new | Policy outputs target angles q*; a fast PD loop applies torque τ = Kp(q* − q) − Kd q̇ (legged_gym `stiffness`, `damping`, `action_scale = 0.5`) | The standard action interface for legged robots and humanoids; smooths actions and eases sim-to-real | Action-space design changes how hard exploration is | R0.4, R0.7 | legged_gym; RMA (joint targets at 100 Hz); Hwangbo et al. 2019 |
| R0.6 | Choosing the action space: torques, PD targets, velocity commands | robotics | new | Same task learned with different action spaces gives very different results | Wrong choice can make learning fail | Policy parameterisation | R0.5 | Peng & van de Panne 2017; Chen et al. 2022 (direct torque); Tai et al. 2017 (velocity commands) |
| R0.7 | PD / PID feedback control | maths | new | Act on the error, its derivative and its integral | Needed by R0.5 and by PID Lagrangian (R4.4) | (control background) | 600 derivatives | legged_gym; Stooke et al. 2020 |
| R0.8 | Massively parallel on-policy training on one GPU | robotics | new | Thousands of simulated robots, short rollouts, very large batches for PPO | Cuts locomotion training to minutes | On-policy methods trade sample efficiency for wall-clock speed when samples are cheap | Block 10 PPO | Rudin et al. 2022; Isaac Gym (Makoviychuk et al. 2021) |
| R0.9 | Simulators and frameworks | robotics | new | Isaac Gym → Orbit → Isaac Lab (manager-based and direct workflows); MuJoCo, MJX, MuJoCo Playground; Gazebo + ROS; Habitat; Flightmare | Choosing the training environment | Environment as code | R0.8 | Isaac Lab docs and paper (2025); Orbit 2023; Todorov et al. 2012; MuJoCo Playground 2025; Koenig & Howard 2004 |
| R0.10 | Reading a reference training stack | robotics | new | legged_gym environment + rsl_rl PPO as the worked code base | Every Note's code examples can follow one stack | | R0.8, R0.9 | legged_gym, rsl_rl repositories |

#### R1. Sim-to-real transfer

| ID | Concept / skill | Kind | Status | What it is | Why it matters | RL idea underneath | Builds on | Taught with |
|---|---|---|---|---|---|---|---|---|
| R1.1 | The sim-to-real (reality) gap | robotics | new | Differences in dynamics, sensing, latency and appearance between sim and robot | Policies exploit simulator errors | Train-test distribution shift | R0.1 | Tobin et al. 2017; Tan et al. 2018 |
| R1.2 | Visual domain randomization | robotics | new | Randomise textures, lighting, camera so reality looks like one more variation | Vision policies trained only on rendered images | Robustness by training on a distribution of MDPs | R1.1 | Tobin et al. 2017; Sadeghi & Levine 2017 (CAD2RL) |
| R1.3 | Dynamics randomization | robotics | new | Randomise mass, friction, latency, motor strength, pushes (legged_gym `randomize_friction`, `added_mass_range`, `push_robots`); pair with a memory policy | The main sim-to-real tool for locomotion | Optimise expected return over a family of MDPs | R1.1, R3.2 | Peng et al. 2018; legged_gym |
| R1.4 | Automatic domain randomization (ADR) | robotics | new | Widen each randomisation range when the policy succeeds at its edge | Removes hand-tuning of ranges; acts as a curriculum | Curriculum over environments | R1.3, R2.10 | OpenAI et al. 2019 |
| R1.5 | System identification and actuator models | robotics | new | Measure or learn the real motor: an analytic actuator model, or an MLP fitted on the history of joint position errors and velocities (actuator network) | Motors are the largest gap on legged robots | Make the simulator's transition model closer to the real one | R1.1, 1010 MLP, 50–55 regression | Tan et al. 2018; Hwangbo et al. 2019 |
| R1.6 | Delta (residual) action model learned from real data *(added 2023–26)* | robotics | new | Deploy, collect real data, learn a correction to actions inside the simulator, fine-tune | Closes the gap without hand-tuning parameters | Model learning as residual | R1.5 | He et al. 2025 (ASAP) |
| R1.7 | Training on the real robot instead | robotics | new | Sample-efficient off-policy RL directly on hardware | The alternative when sim is poor | Off-policy sample efficiency (SAC) | Block 10 SAC | Haarnoja et al. 2019; SERL / HIL-SERL (Block 16) |
| R1.8 | Does sim performance predict real performance? | robotics | new | Measure the correlation of sim and real results; tune the simulator to raise it | Decides whether sim benchmarks mean anything | Evaluation under distribution shift | R1.1 | Kadian et al. 2020 (Sim2Real predictivity) |
| R1.9 | Sensor noise and latency modelling | robotics | new | Add noise to observations (legged_gym `noise_scale_vec`) and delays to actions | Real sensors are noisy and late | Robustness through training noise | R1.3 | legged_gym; Peng et al. 2018 |

#### R2. Designing the task: observations, rewards, curricula

| ID | Concept / skill | Kind | Status | What it is | Why it matters | RL idea underneath | Builds on | Taught with |
|---|---|---|---|---|---|---|---|---|
| R2.1 | Proprioceptive observation design | robotics | new | Base angular velocity, projected gravity, command, joint positions (minus default), joint velocities, last action, each scaled (legged_gym `compute_observations`) | The policy can only use what it sees | Choosing the state so the Markov property nearly holds | R0.4, 24 standardization | legged_gym; Rudin et al. 2022 |
| R2.2 | Projected gravity as an orientation feature | maths | partial | 500 rotation matrix; new: world gravity rotated into the body frame. Quaternions are owned by Planning Algorithms (Ch. 4) | A frame-independent tilt signal | | 500 | legged_gym |
| R2.3 | Exteroceptive inputs: height samples, scandots, depth, laser | robotics | new | Terrain heights around the robot (legged_gym `measure_heights`), sparse height points ("scandots"), depth images, laser ranges | Seeing terrain before touching it | Richer observations vs harder sim-to-real | R2.1 | legged_gym; Cheng et al. 2024; Miki et al. 2022 |
| R2.4 | Command- and goal-conditioned policies | RL | new | The command (velocity, target point) is part of the input, so one policy serves many goals | One policy for all speeds or targets | Goal-conditioned value functions and policies | S&B Ch. 3 | legged_gym; Andrychowicz et al. 2017 |
| R2.5 | Reward = task terms + regularisation terms | robotics | new | Task terms (velocity tracking) plus penalties (torques, joint acceleration, action rate, collisions); legged_gym weights e.g. `tracking_lin_vel = 1.0`, `torques = -1e-5`, `action_rate = -0.01`, `collision = -1` | Most locomotion behaviour is set by these weights | Reward hypothesis (S&B 3.2) in practice | S&B Ch. 3 | legged_gym; Kim et al. 2024 (why this tuning is laborious) |
| R2.6 | Exponential tracking kernel exp(−error²/σ) | maths | partial | 250 normal-curve shape; new: a bounded reward in (0, 1] (legged_gym `tracking_sigma = 0.25`) | Keeps tracking reward on a fixed scale | | 250 | legged_gym |
| R2.7 | Gait shaping: feet air time, foot clearance, energy | robotics | new | Reward long swing phases (legged_gym `feet_air_time`), set swing height as a behaviour parameter, or minimise energy so gaits emerge | Natural, efficient gaits | Shaping vs emergent behaviour | R2.5 | legged_gym; Margolis & Agrawal 2022; Fu et al. 2021 |
| R2.8 | Reward shaping and its risks | RL | new | Extra reward to guide learning; can change what is optimal (reward hacking) | Every robot reward is shaped | Shaping changes the MDP | S&B 17.4 row | S&B §17.4; Ma et al. 2024 (Eureka) |
| R2.9 | Terminations and the sign of rewards | RL | new | Ending an episode cuts all future reward; negative per-step reward plus termination teaches the robot to fall early (legged_gym `only_positive_rewards` clips the total at zero for this reason) | Silent cause of many failed trainings | Termination is part of the return | S&B Ch. 3 return | legged_gym; Chane-Sane et al. 2024 |
| R2.10 | Curricula: terrain and command | RL | new | Game-inspired terrain levels: move up if the robot walked far enough, down if it covered less than half the commanded distance (legged_gym `_update_terrain_curriculum`); grid-adaptive velocity-command curriculum | Hard tasks are learnable only after easy ones | Curriculum learning; non-stationary task distribution | R2.4 | Rudin et al. 2022; legged_gym; Margolis et al. 2022 |
| R2.11 | Sparse rewards and Hindsight Experience Replay | RL | new | Replay failed episodes as if the reached state had been the goal | Binary success rewards become learnable without shaping | Goal relabelling as an implicit curriculum; off-policy learning | Block 9 replay, R2.4 | Andrychowicz et al. 2017; SB3 HER docs |
| R2.12 | Symmetry: mirrored data augmentation and mirror loss | robotics | partial | 1050 data augmentation; new: mirror states and actions of a left–right symmetric robot, with on-policy correctness | Same gait forward and backward; faster training | Invariance by augmentation | R2.1, 1050 | Mittal et al. 2024; Su et al. 2024 |
| R2.13 | A family of behaviours in one policy | robotics | new | Gait parameters (frequency, foot swing height, posture) are policy inputs, chosen at deployment | Tune behaviour on the robot without retraining | Conditioning instead of retraining | R2.4, R2.7 | Margolis & Agrawal 2022 (Walk These Ways) |
| R2.14 | Style rewards learned from data | robotics | partial | 1003 names GANs; new: a discriminator's score of "looks like the motion data" used as reward | Replaces many hand-made style terms | Learned reward (link to inverse RL) | R2.5 | Peng et al. 2018 (DeepMimic); Peng et al. 2021 (AMP); Escontrela et al. 2022 |
| R2.15 | Reward code written by a language model *(added 2023–26)* | RL | new | An LLM proposes reward code; RL scores it; the LLM revises | Automates R2.5 | Search over reward functions | R2.5 | Ma et al. 2024 (Eureka); Ma et al. 2024 (DrEureka) |

#### R3. Partial observability and privileged information

| ID | Concept / skill | Kind | Status | What it is | Why it matters | RL idea underneath | Builds on | Taught with |
|---|---|---|---|---|---|---|---|---|
| R3.1 | Robot control as a POMDP | maths | new | Sensors miss friction, terrain, contacts, other agents' goals. POMDP owned by Probabilistic Robotics (Ch. 15); this row recaps | Explains why the policy needs memory or estimation | Partial observability | S&B 17.3 row | S&B §17.3; Lee et al. 2020 |
| R3.2 | History encoders: frame stacks, temporal convolution, GRU/LSTM, transformers | maths | partial | 1061–1064 LSTM/GRU, 1042 convolution, 1081 masked attention; new: 1D causal temporal convolution (TCN) over past observations and actions | Memory replaces the missing state | A history is a sufficient input when the state is hidden | R3.1 | Lee et al. 2020 (TCN); Peng et al. 2018 (recurrent); Radosavovic et al. 2024 (causal transformer) |
| R3.3 | Privileged information | robotics | new | The simulator knows the true state (terrain, friction, other cars); the real robot does not | Lets training use more than deployment can | Separate what training sees from what acting sees | R3.1 | Chen et al. 2019 (Learning by Cheating); Lee et al. 2020 |
| R3.4 | Asymmetric actor–critic | RL | new | Critic gets the full state, actor gets only the observations | Better value estimates, same deployable policy | The critic is only a training tool, so it may use any information | Block 8 actor–critic, R3.3 | Pinto et al. 2018; Nahrendra et al. 2023 (DreamWaQ) |
| R3.5 | Behaviour cloning and compounding error | RL | new | Supervised learning of expert actions; small errors lead to unseen states | Base of every distillation step | Distribution shift between expert and learner states | 50–55, 1014 | Ross et al. 2011; CS285 2023 L2 |
| R3.6 | DAgger | RL | new | Run the learner, have the expert label the states it visits, add to the dataset, repeat | Fixes compounding error; the distillation tool for teacher–student | Learning on the learner's own state distribution | R3.5 | Ross et al. 2011; Zhuang et al. 2023 (distil skills with DAgger) |
| R3.7 | Teacher–student (privileged) distillation | robotics | partial | 1071 names knowledge distillation; new: an RL teacher with privileged state, a student on sensors that imitates it on its own rollouts | The standard route to blind or vision policies | Two-stage RL then imitation | R3.3, R3.6 | Chen et al. 2019; Lee et al. 2020; Miki et al. 2022 |
| R3.8 | Online adaptation modules | robotics | new | A base policy uses a latent "extrinsics" vector encoded from environment factors; an adaptation module learns to predict it from recent state–action history (RMA: extrinsics at 10 Hz, actions at 100 Hz) | Adapts to new terrain or payload in a fraction of a second, no fine-tuning | Implicit system identification | R3.2, R3.7 | Kumar et al. 2021 (RMA); Qi et al. 2022 (in-hand) |
| R3.9 | Learned state estimation trained with the policy | robotics | new | An estimator network predicts base velocity, foot height and contact probability, trained at the same time as the policy and fed to it | Real robots lack a good velocity estimate | Explicit estimation instead of latent adaptation | R3.1; Kalman filter (PR scope) for contrast | Ji et al. 2022 |
| R3.10 | Variational autoencoder | maths | partial | 1003 names autoencoders; KL in Block 0; reparameterization in 2C; new: loss = reconstruction + β·KL to a prior | Needed for latent estimators (R3.11) | | 1003, Block 0 KL | Nahrendra et al. 2023 (β-VAE) |
| R3.11 | Latent context estimators | robotics | new | An encoder of history predicts velocity and a latent terrain code (β-VAE in DreamWaQ; contrastive learning in HIM) | Blind policies that still "imagine" terrain | Representation learning for POMDPs | R3.9, R3.10, R3.12 | Nahrendra et al. 2023; Long et al. 2023 (HIM, added 2023–26) |
| R3.12 | Contrastive learning objective | maths | new | Pull matching pairs together and push others apart in embedding space | Used by HIM | | 362 cosine similarity | Long et al. 2023 |
| R3.13 | In-context adaptation with a sequence model | RL | new | The policy adapts from its history without weight updates; memory policies show emergent meta-learning | One model adapts across many dynamics | Meta-learning through memory | R3.2 | Radosavovic et al. 2024; OpenAI et al. 2019 |
| R3.14 | Auxiliary tasks for representation | RL | partial | S&B 17.1 auxiliary tasks; new: predicting depth or loop closure alongside RL | Faster learning from pixels | Extra supervised losses shape features | S&B 17.1 row | Mirowski et al. 2017 |

#### R4. Safety and constraints

| ID | Concept / skill | Kind | Status | What it is | Why it matters | RL idea underneath | Builds on | Taught with |
|---|---|---|---|---|---|---|---|---|
| R4.1 | Constrained MDP (CMDP) | maths | new | Maximise expected return subject to expected discounted cost ≤ a limit, for each cost | Puts limits (torque, joint range, collisions) in physical units instead of reward weights | Rewards say what to do; constraints say what not to do | S&B Ch. 3; 620 constrained optimisation | Altman 1999; Achiam et al. 2017 |
| R4.2 | Cost signals and cost critics | RL | new | A second value function estimates expected cost | Every CMDP method needs it | Value estimation for any signal | R4.1, Block 8 | Achiam et al. 2017; Ray et al. 2019 (Safety Gym) |
| R4.3 | Lagrangian methods (PPO-Lagrangian) | maths | partial | 620 multipliers, duality, KKT; 621 saddle points; new: the multiplier λ is learned by gradient ascent on the constraint violation while PPO trains on reward − λ·cost | Simplest and most used constrained RL method | Primal–dual optimisation | R4.1, 620, 621 | Ray et al. 2019; Stooke et al. 2020 |
| R4.4 | PID Lagrangian | RL | new | Update λ with proportional and derivative terms, not just integral | Plain λ oscillates and overshoots the limit | Multiplier update as a feedback controller | R4.3, R0.7 | Stooke et al. 2020 |
| R4.5 | Trust-region constrained update (CPO) | RL | new | TRPO step with a linearised cost constraint | Near-constraint satisfaction at every update | Trust regions + constraints | 2C TRPO, R4.1 | Achiam et al. 2017 |
| R4.6 | Log-barrier methods (IPO) | maths | partial | 622 names interior-point methods; new: a logarithmic barrier on each constraint added to the PPO objective | First-order, easy to add to PPO | Interior-point idea | R4.1, 622 | Liu et al. 2020 (IPO) |
| R4.7 | Exact penalty methods (P3O) | maths | partial | 620 penalty view; new: a ReLU penalty with a finite factor, exact under conditions, inside PPO's clipped objective | No λ to tune online | Penalty = constraint when the factor is large enough | R4.1, 620 | Zhang et al. 2022 (P3O) |
| R4.8 | Constraint types for robots: probabilistic and average | robotics | new | Probabilistic: limit how often an event happens; average: limit a mean quantity. Task in the reward, everything else as constraints, one reward weight to tune | Cuts reward engineering on real legged robots | CMDP in practice | R4.1–R4.6 | Kim et al. 2024 (T-RO) |
| R4.9 | Choosing a constrained algorithm for hardware | robotics | new | Side-by-side comparison of constrained policy optimisation algorithms on a quadruped, with sim-to-real | Which method to use | Empirical comparison | R4.3–R4.7 | Lee et al. 2023 (IROS 2024) |
| R4.10 | Constraints as stochastic terminations | robotics | new | A violation sets a probability of ending the episode, so future reward is lost; works with plain PPO | Hard constraints with almost no code change | Termination as a soft, bounded penalty (links R2.9) | R2.9, R4.1 | Chane-Sane et al. 2024 (CaT) |
| R4.11 | Shields and safety filters | RL | new | A checker removes or corrects unsafe actions before or after the policy acts | Safety during learning and deployment | Restricting the action set | R4.1 | Alshiekh et al. 2018 |
| R4.12 | Recovery policies and reach-avoid values *(added 2023–26)* | robotics | new | An agile policy plus a recovery policy; a learned reach-avoid value decides when to switch | Fast and collision-free at once | Value function as a safety certificate | R4.11 | He et al. 2024 (ABS) |
| R4.13 | Safe-RL benchmarks and libraries | RL | new | Standard tasks and implementations of the methods above | For hands-on Notes | | R4.3–R4.7 | Ray et al. 2019; Safety-Gymnasium; OmniSafe; Gu et al. 2022 (review) |

#### R5. RL for autonomous navigation (primary block)

The deepest block. Classical planners are the comparison point throughout.

| ID | Concept / skill | Kind | Status | What it is | Why it matters | RL idea underneath | Builds on | Taught with |
|---|---|---|---|---|---|---|---|---|
| N.1 | Classical local planners: DWA, TEB, Nav2 controllers | robotics | new | DWA samples velocities inside the reachable window and scores short trajectories; TEB optimises a timed elastic band; Nav2 ships DWB and MPPI controllers on costmaps | The baseline every learned planner must beat | (background, no RL) | Occupancy grids (PR scope Ch. 9) | Fox, Burgard & Thrun 1997; Rösmann et al. 2017; Macenski et al. 2020; Nav2 docs |
| N.2 | Learned vs classical local planners | robotics | new | What RL buys (no map needed, learns from failure, uses dynamics) and what it costs (no guarantees, sample cost, sim-to-real) | Decides when to use RL at all | RL optimises the true objective; planners optimise a stand-in | N.1 | Xiao et al. 2022 (survey); Kahn et al. 2018; Song et al. 2023 |
| N.3 | Navigation as an MDP or POMDP | RL | new | Point-goal, object-goal and image-goal tasks; an episode ends at the goal, a collision or a time limit | The first step of every navigation project | Task formulation | S&B Ch. 3, R3.1 | Anderson et al. 2018; Savva et al. 2019 (Habitat) |
| N.4 | Mapless end-to-end navigation | robotics | new | Sparse laser ranges plus goal in the robot frame map straight to velocity commands, no map | Works without SLAM; transfers from sim | Continuous-action actor–critic | N.3, Block 10 DDPG | Tai, Paolo & Liu 2017; Zhu & Zhang 2021 (review) |
| N.5 | Observation design for a laser-scan navigation policy | robotics | new | Down-sampled ranges (10 in Tai et al.), goal distance and angle in the robot frame, previous velocity, stacked scans | Decides what the policy can react to | Making the observation close to Markov | N.4, R2.1 | Tai et al. 2017; Long et al. 2018 |
| N.6 | Observation design for visual and map-based navigation | robotics | partial | CNN 1040–1045; new: RGB or depth, target image, egocentric occupancy or costmap, learned state representations. Occupancy grids owned by Probabilistic Robotics | Cameras and maps give context lasers miss | Representation choice | N.5, R2.3 | Zhu et al. 2017; Chaplot et al. 2020; Hoeller et al. 2021 |
| N.7 | Action spaces for navigation | robotics | new | Continuous (v, ω); discrete moves (forward, turn); sub-goals or waypoints; velocity commands sent to a locomotion policy | Matches the robot's real controller | Action abstraction and hierarchy | R0.6 | Tai et al. 2017; Wijmans et al. 2020; Lee et al. 2024 |
| N.8 | Reward shaping for navigation | RL | new | Arrival bonus, progress (decrease in goal distance), collision penalty, time penalty, smoothness (rotation) penalty | The most common source of bad navigation behaviour | Dense shaping vs the true sparse goal | R2.5, R2.8 | Tai et al. 2017; Long et al. 2018 (arrival, progress, collision, rotation terms) |
| N.9 | Sparse, time-limited goal reward | RL | new | Reward only for being at the target at the end of a time budget; the robot chooses path and gait | Avoids over-shaping; unlocks new behaviours | Sparse reward + exploration | N.8, R2.11 | Rudin et al. 2022b |
| N.10 | Memory and auxiliary tasks for visual navigation | RL | new | Recurrent policy plus depth and loop-closure prediction | Learns to navigate mazes from pixels | Links R3.2 and R3.14 | R3.2, R3.14 | Mirowski et al. 2017; Zhu et al. 2017 |
| N.11 | Decentralised multi-agent collision avoidance | robotics | new | A value network over the joint configuration of the robot and its neighbours, learned offline, used online | Real-time avoidance without communication | Value function as an interaction model | Block 7, N.3 | Chen et al. 2017 (CADRL) |
| N.12 | Social norms in the reward | robotics | new | Penalise violations (e.g. passing on the wrong side) instead of specifying behaviour | Socially acceptable navigation | Specifying what not to do | N.11 | Chen et al. 2017 (SA-CADRL) |
| N.13 | Any number of neighbours: LSTM and attention pooling | robotics | partial | 1061 LSTM, 1072 self-attention; new: summarising a variable set of agents | Crowds of changing size | Permutation-tolerant inputs | N.11 | Everett et al. 2018 (GA3C-CADRL); Chen et al. 2019 (crowd–robot interaction) |
| N.14 | Shared-policy multi-robot training with PPO | robotics | new | One policy for every robot, raw sensor input, multi-scenario multi-stage training | Scales to many robots | Parameter sharing; curricula | N.11, Block 10 PPO | Long et al. 2018 |
| N.15 | Planner + RL hierarchies | robotics | partial | PRM owned by Planning Algorithms (Ch. 5); new: roadmap edges kept only if the RL local policy can actually drive them | Long-range navigation with short-range RL | Hierarchy of planning and learned control | N.4 | Faust et al. 2018 (PRM-RL); Francis et al. 2020 |
| N.16 | Searching rewards and networks automatically | RL | new | Evolutionary search over reward weights and network shape for navigation | Removes hand-tuning of N.8 | Outer-loop optimisation of the MDP | N.8 | Chiang et al. 2019 (AutoRL) |
| N.17 | Modular learned navigation vs end-to-end | robotics | new | Learned SLAM module + global and local policies + analytic planner | Lower sample cost, better exploration | Decomposition vs end-to-end | N.6 | Chaplot et al. 2020 (Active Neural SLAM) |
| N.18 | Embodied navigation at scale | RL | new | Fast photoreal simulators; decentralised synchronous distributed PPO to billions of frames | Shows what scale buys | Parallel on-policy RL (links R0.8) | R0.8 | Savva et al. 2019; Wijmans et al. 2020 (DD-PPO) |
| N.19 | Evaluation: success rate, SPL, collisions, time | robotics | new | SPL = (1/N) Σ Sᵢ ℓᵢ / max(pᵢ, ℓᵢ): success weighted by shortest-path length over the path taken | Fair comparison of planners and policies | Choosing the metric is part of the task | N.3 | Anderson et al. 2018; Wijmans et al. 2020 |
| N.20 | Self-supervised real-world navigation | robotics | new | Labels come from the robot's own events (collision, bumpiness); models between model-free and model-based | Learn on real terrain without sim or humans | Learning from the robot's own data; off-policy | Block 12, R1.7 | Kahn et al. 2018; Kahn et al. 2021 (BADGR); Gandhi et al. 2017 |
| N.21 | Sim-to-real for navigation | robotics | new | Randomised rendering, laser-only inputs that transfer well, measured sim–real agreement | Navigation policies are trained in sim | Links R1.1–R1.8 | R1.2, R1.8 | Sadeghi & Levine 2017; Tai et al. 2017; Kadian et al. 2020 |
| N.22 | Navigation with legged robots | robotics | new | Learned state representation + navigation policy; end-to-end locomotion and local navigation; a navigation policy that selects skills | Rough-terrain navigation | Hierarchical and end-to-end RL | N.9, R6 | Hoeller et al. 2021; Rudin et al. 2022b; Hoeller et al. 2024 |
| N.23 | Wheeled-legged urban navigation *(added 2023–26)* | robotics | new | Hierarchical RL: navigation policy over a privileged-trained locomotion policy that walks and drives | Long autonomous missions in cities | Hierarchy + privileged learning | N.22, R3.7 | Lee et al. 2024 (Science Robotics) |
| N.24 | Agile aerial navigation | robotics | new | Privileged expert imitated by a sensor policy for fast flight in the wild; RL in sim plus real-data correction for racing; RL vs optimal control | Shows the limits of learned navigation | Privileged learning; RL optimises the true objective | R3.7, R1.6 | Loquercio et al. 2021; Kaufmann et al. 2023; Song et al. 2023 |
| N.25 | Safety in navigation | robotics | new | Collision limits as constraints, shields, recovery policies | Needed before real deployment | Links R4 | R4.1, R4.11, R4.12 | He et al. 2024; Alshiekh et al. 2018 |
| N.26 | Navigation simulators and ROS tooling | robotics | new | Gazebo + ROS / Nav2, Isaac Lab, Habitat, Flightmare, CrowdNav | Setting up the training loop | | R0.9 | Koenig & Howard 2004; Savva et al. 2019; Song et al. 2020 (Flightmare); CrowdNav repo |
| N.27 | Navigation foundation models (context; imitation, not RL) | robotics | new | Goal-conditioned models trained on many robots' datasets (GNM, ViNT); a diffusion policy for goal-reaching and exploration (NoMaD) | Where the field is moving; a baseline for RL | Imitation at scale (contrast with RL) | N.3, Block 16 | Shah et al. 2023 (GNM); Shah et al. 2023 (ViNT); Sridhar et al. 2024 (NoMaD) |

#### R6. Legged locomotion

| ID | Concept / skill | Kind | Status | What it is | Why it matters | RL idea underneath | Builds on | Taught with |
|---|---|---|---|---|---|---|---|---|
| L.1 | The PPO locomotion recipe, end to end | robotics | new | Worked example joining R0–R3: PD targets, proprioceptive observations, tracking + penalty rewards, terrain curriculum, randomisation, teacher–student | The pattern behind most modern legged controllers | All of R0–R3 together | R0–R3 | Rudin et al. 2022; Lee et al. 2020; Hwangbo et al. 2019 |
| L.2 | Learning a gait from scratch with an improved simulator | robotics | new | Simple reward, optional open-loop reference, system identification + actuator model + randomisation | First quadruped sim-to-real with deep RL | | R1.5 | Tan et al. 2018 |
| L.3 | Perceptive locomotion | robotics | new | An attention-based recurrent encoder fuses proprioception with a noisy height map; trained teacher–student | Fast walking that still survives bad maps | Belief state from two noisy sources | R2.3, R3.7 | Miki et al. 2022 |
| L.4 | High-speed running | robotics | new | Adaptive curriculum on velocity commands + online system identification | Agility at the robot's limits | Curriculum + adaptation | R2.10, R3.8 | Margolis et al. 2022 |
| L.5 | Agility and parkour | robotics | new | First learn with soft (penetrable) obstacles, then hard ones; distil skills into one depth policy with DAgger; learn heading from scandots then depth | Climb, leap, crawl from a camera | Curriculum over dynamics constraints; distillation | R2.10, R3.6 | Zhuang et al. 2023; Cheng et al. 2024 |
| L.6 | Skill hierarchies for agile navigation | robotics | new | Several locomotion skills plus a navigation policy that selects and steers them; perception module rebuilds occluded obstacles | Long obstacle courses | Hierarchical RL | L.5, N.22 | Hoeller et al. 2024 |
| L.7 | RL tracking of model-based reference motions *(added 2023–26)* | robotics | new | A planner rolls out a reference during training; RL learns to track it robustly | Precise footholds where pure RL struggles | Hybrid model-based + RL | L.1 | Jenelten et al. 2024 (DTC) |
| L.8 | Gaits from energy minimisation | robotics | new | Minimising energy alone gives walk, trot and gallop at different speeds | Fewer reward terms | Simple reward, rich behaviour | R2.7 | Fu et al. 2021 |

#### R7. Humanoids

| ID | Concept / skill | Kind | Status | What it is | Why it matters | RL idea underneath | Builds on | Taught with |
|---|---|---|---|---|---|---|---|---|
| H.1 | Motion imitation reward | robotics | new | Reward for tracking a reference clip; start episodes at random reference states; terminate early on falls | Turns motion capture into physical skills | Imitation through a reward | R2.5, R2.9 | Peng et al. 2018 (DeepMimic) |
| H.2 | Adversarial motion priors | robotics | partial | 1003 GAN; new: discriminator reward for "looks like the dataset" plus a task reward | Natural style without per-clip tracking | Learned reward (R2.14) | H.1 | Peng et al. 2021 (AMP) |
| H.3 | Humanoid locomotion sim-to-real | robotics | new | A causal transformer over observation–action history, trained with large-scale RL on randomised sims, deployed zero-shot | Full-size humanoid walking outdoors | In-context adaptation (R3.13) | R1.3, R3.2 | Radosavovic et al. 2024 (Science Robotics) |
| H.4 | Skills, distillation and self-play | robotics | new | Train skills separately, distil into one agent, then self-play against past copies; high control rate, targeted randomisation and perturbations for transfer | Dynamic 1v1 soccer on small humanoids | Distillation + multi-agent self-play | R3.6, 2C self-play | Haarnoja et al. 2024 (Science Robotics) |
| H.5 | Whole-body tracking from human data | robotics | new | Retarget human motion, filter infeasible clips in sim ("sim-to-data"), train an RL tracker with privileged imitation, use it for teleoperation; high-level skills then come by imitation of teleoperated data | Human data at scale for humanoids. **RL** low-level tracker; **imitation** high-level | Privileged learning (R3.7) | H.1, R3.7 | He et al. 2024 (H2O); He et al. 2024 (OmniH2O); Fu et al. 2024 (HumanPlus) |
| H.6 | Split-body objectives | robotics | new | Upper body imitates the reference; legs only follow a velocity robustly | Expressive yet stable motion | Partial imitation reward | H.1 | Cheng et al. 2024 (Exbody) |
| H.7 | One controller for many command modes *(added 2023–26)* | robotics | new | Mask parts of a full-body command; distil many modes into one policy | Navigation, manipulation and teleop with one controller | Multi-task distillation | H.5 | He et al. 2025 (HOVER) |
| H.8 | Aligning sim with real via a delta action model | robotics | new | See R1.6, applied to agile humanoid skills | Agile humanoid motions transfer | Residual dynamics | R1.6 | He et al. 2025 (ASAP) |
| H.9 | Motion tracking plus guided diffusion *(added 2023–26)* | robotics | new | A general tracking policy; a diffusion model composes skills at test time. Diffusion has no Note yet (flag) | Versatile humanoid control | Tracking as a reusable skill layer | H.5 | Liao et al. 2025 (BeyondMimic) |
| H.10 | Perceptive humanoid locomotion *(added 2023–26)* | robotics | new | Parkour-style learning moved to humanoids | Humanoids on rough ground | Same as L.5 | L.5 | Zhuang et al. 2024 (Humanoid Parkour Learning) |

#### R8. Manipulation

| ID | Concept / skill | Kind | Status | What it is | Why it matters | RL idea underneath | Builds on | Taught with |
|---|---|---|---|---|---|---|---|---|
| M.1 | End-to-end visuomotor policies | robotics | partial | CNN 1040–1045; new: camera pixels straight to motor torques, trained by guided policy search | First deep policies on real arms | Supervised learning guided by trajectory optimisation | R0.3 | Levine et al. 2016 |
| M.2 | Large-scale real data for grasping (supervised, not RL) | robotics | partial | CNN; new: predict grasp success from images and servo continuously | The data-scale baseline for QT-Opt | Contrast: supervised success prediction | M.1 | Levine et al. 2018 (IJRR; arXiv 2016) |
| M.3 | Off-policy Q-learning at scale on real robots | robotics | new | Closed-loop vision grasping from over 580k real attempts with a large Q-function | Real-world RL at scale | Off-policy learning from logged data | Block 9 | Kalashnikov et al. 2018 (QT-Opt) |
| M.4 | Cross-entropy method for maximising Q | maths | new | Sample actions, keep the best, refit, repeat | Max over continuous actions without an actor | Derivative-free optimisation | M.3 | Kalashnikov et al. 2018 |
| M.5 | Goal-conditioned manipulation with sparse rewards | RL | new | Push, slide, pick-and-place from binary success + HER | Manipulation rewards are naturally sparse | Links R2.11 | R2.11 | Andrychowicz et al. 2017 |
| M.6 | Residual RL | RL | new | Learn a correction on top of a hand-designed controller | Fast learning on real contact-rich tasks | Policy = prior controller + learned residual | R0.3 | Johannink et al. 2019; Silver et al. 2018 |
| M.7 | Dexterous in-hand reorientation with randomisation and memory | robotics | new | Multi-finger hand trained only in sim with heavy randomisation, LSTM policy, vision pose estimator | Most-cited dexterous sim-to-real result | Links R1.3, R1.4, R3.13 | R1.3, R1.4 | OpenAI et al. 2018; OpenAI et al. 2019; Handa et al. 2023 (DeXtreme) |
| M.8 | Adaptive in-hand rotation from proprioception | robotics | new | RMA-style adaptation to object size, shape and weight from history | Generalises to many objects | Links R3.8 | R3.8 | Qi et al. 2022 |
| M.9 | Teacher–student for visual dexterity | robotics | new | Full-state RL teacher, vision (point-cloud) student by supervised imitation | Reorient new, complex shapes | Links R3.7 | R3.7 | Chen et al. 2023 (Science Robotics) |
| M.10 | Point-cloud policies and contact rewards | robotics | new | Point-cloud input, imagined hand points as extra input, contact-based reward | Generalise to new objects in the real world | Observation and reward design (R2) | R2.3, R2.5 | Qin et al. 2022 (DexPoint) |
| M.11 | Demonstrations from human videos | robotics | new | Extract hand and object poses from video, translate to robot demos, then imitation (+ RL) | Cheap demonstrations | Imitation; flagged as mostly imitation | R3.5 | Qin et al. 2022 (DexMV) |
| M.12 | Vision-based bimanual dexterity on humanoids *(added 2023–26)* | robotics | new | Sim-to-real RL recipe with automatic real-to-sim tuning for grasp, lift, handover | Dexterity on humanoid hands | Links R1, R2, R3 | M.7, M.9 | Lin et al. 2025 |

Real-world RL with human corrections (SERL, HIL-SERL) and VLA fine-tuning stay in 2E (Block 16), to avoid duplication.

#### 2D.10 Skills view: RL for autonomous navigation

What a learner should be able to do after Block 13.5, and the concepts that teach each skill.

| # | Skill | Taught by |
|---|---|---|
| 1 | Formulate a navigation task as an MDP or POMDP (state, goal, termination, time limit) | N.3, R0.4, R3.1 |
| 2 | Design observations: laser, depth, goal in robot frame, costmap, history | N.5, N.6, R2.3, R3.2 |
| 3 | Choose the action space: (v, ω), discrete moves, sub-goals, or commands to a locomotion policy | N.7, R0.6 |
| 4 | Design and debug the reward: progress, arrival, collision, time, smoothness; know when to go sparse | N.8, N.9, R2.8, R2.9 |
| 5 | Set up a sim training loop (Gazebo/ROS, Isaac Lab, Habitat) with PPO or SAC | N.26, R0.8, R0.9, N.18, Block 10 |
| 6 | Apply domain randomization and curricula | R1.2, R1.3, R1.4, R2.10, N.21 |
| 7 | Use privileged information and memory for partial observability | R3.3–R3.7, N.10, N.24 |
| 8 | Add safety constraints, shields and recovery | R4.1, R4.3, R4.10, R4.11, N.25 |
| 9 | Handle other agents and crowds | N.11–N.14 |
| 10 | Combine RL with planners or modular stacks | N.15, N.17, N.22, N.23 |
| 11 | Evaluate with success rate, SPL, collisions, time; check sim–real agreement | N.19, R1.8 |
| 12 | Compare against DWA / TEB / Nav2 controllers | N.1, N.2 |
| 13 | Transfer to a real robot (ROS) and learn from real data | N.21, N.20, R1.5–R1.7, N.26 |

### 2E. Frontier

| Concept | Kind | Status | Our Note / what is new | Taught with |
|---|---|---|---|---|
| Reward model learned from pairwise human preferences | RL | partial | 1067 describes a reward model; new: how it is trained | Christiano et al. 2017 |
| Bradley–Terry preference model | maths | new | P(A preferred) = sigmoid of the reward gap; links 72 sigmoid, 73 log loss | Christiano et al. 2017 |
| SFT → reward model → PPO with a KL penalty to the SFT model | RL | partial | 1067 three steps; new: the KL penalty and PPO details | Ouyang et al. 2022 (InstructGPT) |
| Closed-form optimal policy of KL-regularised reward; preference loss without RL | maths | new | | Rafailov et al. 2023 (DPO) |
| Group-relative advantage: no critic, compare answers to the same prompt | RL | new | | Shao et al. 2024 (GRPO) |
| RL with verifiable rule-based rewards (accuracy, format); R1-Zero without SFT | RL | new | | DeepSeek-AI 2025 (DeepSeek-R1) |
| The name and recipe "RL with verifiable rewards" (RLVR) | RL | new | | Lambert et al. 2024 (extra) |
| Decoupled clipping and dynamic sampling for large-scale GRPO-style RL | RL | new | | Yu et al. 2025 (DAPO, 2025 major) |
| Length bias in GRPO and an unbiased fix | RL | new | | Liu et al. 2025 (Dr. GRPO, 2025 major) |
| Learned latent model (representation, dynamics, prediction) + MCTS | RL | new | | Schrittwieser et al. 2020 (MuZero) |
| World model; learning by imagined rollouts; robustness tricks | RL | partial | 1064 GRU; new: a recurrent model of the world used for planning | Hafner et al. 2023/2025 (DreamerV3) |
| Offline RL setting; distribution shift; out-of-distribution actions | RL | new | | Levine et al. 2020 (tutorial) |
| Conservative Q-learning: push down Q on unseen actions | RL | new | | Kumar et al. 2020 (CQL) |
| RL as sequence modelling, conditioned on return-to-go | RL | partial | 1081 masked attention, 1085 GPT-style decoder; new: tokens are (return, state, action) | Chen et al. 2021 (Decision Transformer) |
| Vision-language-action (VLA) model; actions as text tokens; co-fine-tuning | robotics | partial | 1071 ViT, 1085 decoder, 1053 fine-tuning; new: robot actions as tokens | Brohan et al. 2023 (RT-2) |
| Fine-tuning an open VLA for a new robot | robotics | partial | 1053 fine-tuning; new: efficient fine-tuning of a 7B VLA | Kim et al. 2024 (OpenVLA) |
| Flow-matching action expert; action chunks | maths | new | Flow matching is a generative-model idea; no Note yet | Black et al. 2024 (π0) |
| VLA co-trained on varied data for open-world homes | robotics | new | | Physical Intelligence 2025 (π0.5, 2025 major) |
| RL fine-tuning of a VLA by advantage conditioning, with human corrections | robotics | new | The clearest "foundation model + RL" robot example | Physical Intelligence 2025 (π*0.6 / RECAP, 2025 major) |
| Generalist VLA for real robots (mostly imitation; context) | robotics | new | | Gemini Robotics Team 2025 (2025 major) |
| Open foundation model for humanoids (mostly imitation; context) | robotics | new | | NVIDIA 2025 (GR00T N1, 2025 major) |
| Sample-efficient off-policy real-robot RL: reward classifier, resets, demos | robotics | new | | Luo et al. 2024 (SERL) |
| Human corrections during real-world RL; 1–2.5 h training | robotics | new | | Luo et al. 2024/2025 (HIL-SERL) |

---

## 3. Verified sources

Checked on 2026-10-03. "arXiv" = title, first author and date read from the arXiv abstract page. "DOI" = read from Crossref. "Page" = publisher page loaded.

### 3.1 Book, classic, deep RL and frontier sources

| Paper | Authors | Year / venue | ID | Checked |
|---|---|---|---|---|
| Reinforcement Learning: An Introduction, 2nd ed. | Sutton, Barto | 2018, MIT Press | incompleteideas.net/book/the-book-2nd.html | Page + PDF contents |
| Dynamic Programming | Bellman | 1957, Princeton Univ. Press (2010 reprint page) | press.princeton.edu ISBN 9780691146683 | Page |
| Learning to predict by the methods of temporal differences | Sutton | 1988, Machine Learning 3 | DOI 10.1007/BF00115009 | DOI |
| Q-learning | Watkins, Dayan | 1992, Machine Learning 8 | DOI 10.1007/BF00992698 | DOI |
| Simple statistical gradient-following algorithms for connectionist RL | Williams | 1992, Machine Learning 8 | DOI 10.1007/BF00992696 | DOI |
| Policy Gradient Methods for RL with Function Approximation | Sutton, McAllester, Singh, Mansour | NIPS 12 (1999 meeting, 2000 proceedings) | papers.nips.cc 1999 hash 464d828b… | Page |
| Actor-Critic Algorithms | Konda, Tsitsiklis | NIPS 12 (2000 proceedings); journal version SIAM J. Control Optim. 2003 | papers.nips.cc 1999 hash 6449f44a…; DOI 10.1137/S0363012901385691 | Page + DOI |
| Human-level control through deep RL (DQN) | Mnih et al. | 2015, Nature | DOI 10.1038/nature14236 (preprint arXiv 1312.5602, 2013) | DOI + arXiv |
| Mastering the game of Go with deep neural networks and tree search | Silver et al. | 2016, Nature | DOI 10.1038/nature16961 | DOI |
| Mastering the game of Go without human knowledge | Silver et al. | 2017, Nature | DOI 10.1038/nature24270 | DOI |
| Mastering Chess and Shogi by Self-Play… (AlphaZero, extra) | Silver et al. | 2017, arXiv | 1712.01815 | arXiv |
| Asynchronous Methods for Deep RL (A3C, extra) | Mnih et al. | 2016, arXiv / ICML | 1602.01783 | arXiv |
| Continuous control with deep RL (DDPG) | Lillicrap et al. | 2015 arXiv, ICLR 2016 | 1509.02971 | arXiv |
| Trust Region Policy Optimization | Schulman et al. | 2015 | 1502.05477 | arXiv |
| High-Dimensional Continuous Control Using GAE | Schulman et al. | 2015 arXiv, ICLR 2016 | 1506.02438 | arXiv |
| Proximal Policy Optimization Algorithms | Schulman et al. | 2017 | 1707.06347 | arXiv |
| Soft Actor-Critic | Haarnoja et al. | 2018 | 1801.01290 | arXiv |
| Addressing Function Approximation Error in Actor-Critic Methods (TD3) | Fujimoto, van Hoof, Meger | 2018 | 1802.09477 | arXiv |
| Reinforcement learning in robotics: A survey | Kober, Bagnell, Peters | 2013, IJRR | DOI 10.1177/0278364913495721 | DOI |
| End-to-End Training of Deep Visuomotor Policies | Levine et al. | 2016, JMLR 17 (arXiv 2015) | jmlr.org/papers/v17/15-522; 1504.00702 | Page + arXiv |
| Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World | Tobin et al. | 2017 | 1703.06907 | arXiv |
| Learning agile and dynamic motor skills for legged robots | Hwangbo et al. | 2019, Science Robotics | DOI 10.1126/scirobotics.aau5872; 1901.08652 | DOI + arXiv |
| Learning quadrupedal locomotion over challenging terrain | Lee et al. | 2020, Science Robotics | DOI 10.1126/scirobotics.abc5986; 2010.11251 | DOI + arXiv |
| Solving Rubik's Cube with a Robot Hand | OpenAI et al. | 2019 | 1910.07113 | arXiv |
| Learning to Walk in Minutes Using Massively Parallel Deep RL | Rudin et al. | CoRL 2021, PMLR 164 (2022) | 2109.11978; proceedings.mlr.press/v164/rudin22a | arXiv + Page |
| Deep RL from human preferences | Christiano et al. | 2017 | 1706.03741 | arXiv |
| Training language models to follow instructions with human feedback | Ouyang et al. | 2022 | 2203.02155 | arXiv |
| Direct Preference Optimization | Rafailov et al. | 2023 | 2305.18290 | arXiv |
| DeepSeekMath (introduces GRPO) | Shao et al. | 2024 | 2402.03300 | arXiv |
| DeepSeek-R1 | DeepSeek-AI (Guo et al. in Nature) | 2025 arXiv; Nature 2025 | 2501.12948; DOI 10.1038/s41586-025-09422-z | arXiv + DOI |
| Tulu 3 (RLVR, extra) | Lambert et al. | 2024 | 2411.15124 | arXiv |
| DAPO (2025 major) | Yu et al. | 2025 | 2503.14476 | arXiv |
| Understanding R1-Zero-Like Training (Dr. GRPO, 2025 major) | Liu et al. | 2025 | 2503.20783 | arXiv |
| Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model (MuZero) | Schrittwieser et al. | 2019 arXiv; Nature 2020 | 1911.08265; DOI 10.1038/s41586-020-03051-4 | arXiv + DOI |
| Mastering Diverse Domains through World Models (DreamerV3) | Hafner et al. | 2023 arXiv; Nature 2025 ("Mastering diverse control tasks through world models") | 2301.04104; DOI 10.1038/s41586-025-08744-2 | arXiv + DOI |
| Offline RL: Tutorial, Review, and Perspectives on Open Problems | Levine, Kumar, Tucker, Fu | 2020 | 2005.01643 | arXiv |
| Conservative Q-Learning for Offline RL | Kumar et al. | 2020 | 2006.04779 | arXiv |
| Decision Transformer | Chen et al. | 2021 | 2106.01345 | arXiv |
| RT-2 | Brohan et al. | 2023 | 2307.15818 | arXiv |
| OpenVLA | Kim et al. | 2024 | 2406.09246 | arXiv |
| π0: A Vision-Language-Action Flow Model | Black et al. | 2024 | 2410.24164 | arXiv |
| π0.5 (2025 major) | Physical Intelligence | 2025 | 2504.16054 | arXiv |
| π*0.6: a VLA That Learns From Experience (2025 major) | Physical Intelligence | 2025 | 2511.14759 | arXiv |
| Gemini Robotics (2025 major) | Gemini Robotics Team | 2025 | 2503.20020 | arXiv |
| GR00T N1 (2025 major) | NVIDIA | 2025 | 2503.14734 | arXiv |
| SERL | Luo et al. | 2024 | 2401.16013 | arXiv |
| HIL-SERL | Luo, Xu, Wu, Levine | 2024 arXiv; Science Robotics 2025 | 2410.21845; DOI 10.1126/scirobotics.ads5033 | arXiv + DOI |

Nothing had to be dropped. Two notes: the Sutton et al. and Konda–Tsitsiklis papers are in NIPS volume 12, held in 1999 and printed in 2000. The arXiv API (export.arxiv.org) did not answer, so each abstract page was read one by one.


### 3.2 Robotics pass (checked 2026-10-03)

Same method: arXiv abstract page (title, authors, date, journal-ref, comments), Crossref by DOI, PMLR or publisher page. Where a claim in Section 2D quotes a method detail (TCN, extrinsics, β-VAE, probabilistic and average constraints, DAgger distillation, scandots, CEM, reward terms, SPL formula), it was read from the paper's PDF text. legged_gym details were read from `legged_robot_config.py` and `legged_robot.py` on GitHub (master).

| Paper | Authors | Year / venue | ID | Checked |
|---|---|---|---|---|
| **R0–R1 foundations, sim-to-real** | | | | |
| Learning Locomotion Skills Using DeepRL: Does the Choice of Action Space Matter? | Peng, van de Panne | 2017, SCA | 1611.01055; DOI 10.1145/3099564.3099567 | arXiv |
| Learning Torque Control for Quadrupedal Locomotion | Chen, Zhang, Mueller, Rai, Sreenath | 2022, arXiv | 2203.05194 | arXiv |
| Isaac Gym: High Performance GPU-Based Physics Simulation for Robot Learning | Makoviychuk et al. | 2021, arXiv | 2108.10470 | arXiv |
| Orbit: A Unified Simulation Framework for Interactive Robot Learning Environments | Mittal et al. | 2023, RA-L 8(6) | 2301.04195; DOI 10.1109/LRA.2023.3270034 | arXiv |
| Isaac Lab: A GPU-Accelerated Simulation Framework for Multi-Modal Robot Learning | NVIDIA: Mittal, Roth, Tigue, Richard et al. | 2025, arXiv | 2511.04831 | arXiv |
| MuJoCo: A physics engine for model-based control | Todorov, Erez, Tassa | 2012, IROS | DOI 10.1109/IROS.2012.6386109 | DOI |
| MuJoCo Playground | Zakka et al. | 2025, arXiv | 2502.08844 | arXiv |
| Design and use paradigms for Gazebo, an open-source multi-robot simulator | Koenig, Howard | 2004, IROS | DOI 10.1109/IROS.2004.1389727 | DOI |
| Sim-to-Real Transfer of Robotic Control with Dynamics Randomization | Peng, Andrychowicz, Zaremba, Abbeel | 2018, ICRA | 1710.06537; DOI 10.1109/ICRA.2018.8460528 | arXiv |
| Sim-to-Real: Learning Agile Locomotion For Quadruped Robots | Tan, Zhang, Coumans, Iscen, Bai, Hafner et al. | 2018, RSS XIV | 1804.10332; DOI 10.15607/RSS.2018.XIV.010 | arXiv + DOI |
| Learning to Walk via Deep Reinforcement Learning | Haarnoja, Ha, Zhou, Tan, Tucker, Levine | 2019, RSS XV | 1812.11103; DOI 10.15607/RSS.2019.XV.011 | arXiv + DOI |
| ASAP: Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills (added) | He, Gao, Xiao, Zhang et al. | 2025, RSS | 2502.01143 | arXiv |
| Sim2Real Predictivity: Does Evaluation in Simulation Predict Real-World Performance? | Kadian, Truong, Gokaslan, Clegg, Wijmans, Lee et al. | 2020, RA-L | 1912.06321; DOI 10.1109/LRA.2020.3013848 | arXiv |
| CAD2RL: Real Single-Image Flight without a Single Real Image | Sadeghi, Levine | 2017, RSS | 1611.04201 | arXiv |
| **R2 task design** | | | | |
| Rapid Locomotion via Reinforcement Learning | Margolis, Yang, Paigwar, Chen, Agrawal | 2022, RSS XVIII | 2205.02824; DOI 10.15607/RSS.2022.XVIII.022 | arXiv + DOI |
| Walk These Ways: Tuning Robot Control for Generalization with Multiplicity of Behavior | Margolis, Agrawal | CoRL 2022, PMLR 205 | 2212.03238; proceedings.mlr.press/v205/margolis23a | arXiv + Page |
| Minimizing Energy Consumption Leads to the Emergence of Gaits in Legged Robots | Fu, Kumar, Malik, Pathak | CoRL 2021, PMLR 164 | 2111.01674; proceedings.mlr.press/v164/fu22a | arXiv + Page |
| Hindsight Experience Replay | Andrychowicz, Wolski, Ray, Schneider, Fong, Welinder et al. | 2017, arXiv | 1707.01495 | arXiv |
| Symmetry Considerations for Learning Task Symmetric Robot Policies | Mittal, Rudin, Klemm, Allshire, Hutter | 2024, ICRA | 2403.04359; DOI 10.1109/ICRA57147.2024.10611493 | arXiv + DOI |
| Leveraging Symmetry in RL-based Legged Locomotion Control | Su, Huang, Ordoñez-Apraez, Li et al. | 2024, IROS | 2403.17320; DOI 10.1109/IROS58592.2024.10802439 | arXiv |
| DeepMimic: Example-Guided Deep RL of Physics-Based Character Skills | Peng, Abbeel, Levine, van de Panne | 2018, ACM TOG (SIGGRAPH) | 1804.02717; DOI 10.1145/3197517.3201311 | arXiv |
| AMP: Adversarial Motion Priors for Stylized Physics-Based Character Control | Peng, Ma, Abbeel, Levine, Kanazawa | 2021, ACM TOG (SIGGRAPH) | 2104.02180; DOI 10.1145/3450626.3459670 | arXiv |
| Adversarial Motion Priors Make Good Substitutes for Complex Reward Functions | Escontrela, Peng, Yu, Zhang, Iscen, Goldberg et al. | 2022, arXiv | 2203.15103 | arXiv |
| Eureka: Human-Level Reward Design via Coding LLMs (added) | Ma, Liang, Wang, Huang, Bastani, Jayaraman et al. | ICLR 2024 | 2310.12931 | arXiv |
| DrEureka: Language Model Guided Sim-To-Real Transfer (added) | Ma, Liang, Wang, Wang, Zhu, Fan et al. | RSS 2024 | 2406.01967 | arXiv |
| **R3 partial observability, privileged learning** | | | | |
| Asymmetric Actor Critic for Image-Based Robot Learning | Pinto, Andrychowicz, Welinder, Zaremba, Abbeel | 2018, RSS XIV (arXiv 2017) | 1710.06542; DOI 10.15607/RSS.2018.XIV.008 | arXiv + DOI |
| Learning by Cheating | Chen, Zhou, Koltun, Krähenbühl | CoRL 2019, PMLR 100 | 1912.12294; proceedings.mlr.press/v100/chen20a | arXiv + Page |
| A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning (DAgger) | Ross, Gordon, Bagnell | AISTATS 2011, PMLR 15 | 1011.0686; proceedings.mlr.press/v15/ross11a | arXiv + Page |
| RMA: Rapid Motor Adaptation for Legged Robots | Kumar, Fu, Pathak, Malik | 2021, RSS XVII | 2107.04034; DOI 10.15607/RSS.2021.XVII.011 | arXiv + DOI |
| Concurrent Training of a Control Policy and a State Estimator for Dynamic and Robust Legged Locomotion | Ji, Mun, Kim, Hwangbo | 2022, RA-L 7(2) | 2202.05481; DOI 10.1109/LRA.2022.3151396 | arXiv + DOI |
| DreamWaQ: Learning Robust Quadrupedal Locomotion With Implicit Terrain Imagination via Deep RL | Nahrendra, Yu, Myung | 2023, ICRA | 2301.10602; DOI 10.1109/ICRA48891.2023.10161144 | arXiv + DOI |
| Hybrid Internal Model: Learning Agile Legged Locomotion with Simulated Robot Response (added) | Long, Wang, Li, Gao, Cao, Pang et al. | 2023, arXiv | 2312.11460 | arXiv |
| Real-World Humanoid Locomotion with Reinforcement Learning | Radosavovic, Xiao, Zhang, Darrell, Malik, Sreenath | 2024, Science Robotics | 2303.03381; DOI 10.1126/scirobotics.adi9579 | arXiv + DOI |
| Learning to Navigate in Complex Environments | Mirowski, Pascanu, Viola, Soyer, Ballard, Banino et al. | ICLR 2017 (arXiv 2016) | 1611.03673 | arXiv |
| **R4 constraints** | | | | |
| Constrained Markov Decision Processes | Altman | 1999, Chapman & Hall/CRC (Crossref lists the 2021 Routledge re-issue) | DOI 10.1201/9781315140223 | DOI |
| Constrained Policy Optimization | Achiam, Held, Tamar, Abbeel | ICML 2017 | 1705.10528 | arXiv |
| Benchmarking Safe Exploration in Deep RL (Safety Gym; PPO-Lagrangian baseline) | Ray, Achiam, Amodei | 2019, OpenAI report | cdn.openai.com/safexp-short.pdf | Page (PDF title page read) |
| Responsive Safety in RL by PID Lagrangian Methods | Stooke, Achiam, Abbeel | ICML 2020 | 2007.03964 | arXiv |
| IPO: Interior-point Policy Optimization under Constraints | Liu, Ding, Liu | 2019 arXiv | 1910.09615 | arXiv |
| Penalized Proximal Policy Optimization for Safe RL (P3O) | Zhang, Shen, Yang, Chen, Yuan, Wang et al. | IJCAI 2022 | 2205.11814 | arXiv |
| Not Only Rewards But Also Constraints: Applications on Legged Robot Locomotion | Kim, Oh, Lee, Choi, Ji, Jung, Youm, Hwangbo | arXiv 2023; IEEE T-RO 2024 | 2308.12517; DOI 10.1109/TRO.2024.3400935 | arXiv + DOI |
| Evaluation of Constrained RL Algorithms for Legged Locomotion | Lee, Schroth, Klemm, Bjelonic, Reske, Hutter | arXiv 2023; published IROS 2024 under the title "Exploring Constrained RL Algorithms for Quadrupedal Locomotion" (same six authors) | 2309.15430; DOI 10.1109/IROS58592.2024.10801341 | arXiv + DOI |
| CaT: Constraints as Terminations for Legged Locomotion RL | Chane-Sane, Leziart, Flayols, Stasse, Souères, Mansard | 2024, IROS | 2403.18765; DOI 10.1109/IROS58592.2024.10802334 | arXiv + DOI |
| Safe RL via Shielding | Alshiekh, Bloem, Ehlers, Könighofer, Niekum, Topcu | 2017 arXiv | 1708.08611 | arXiv |
| Agile But Safe: Learning Collision-Free High-Speed Legged Locomotion (added) | He, Zhang, Xiao, He, Liu, Shi | RSS 2024 | 2401.17583 | arXiv |
| A Review of Safe RL: Methods, Theory and Applications | Gu, Yang, Du, Chen, Walter, Wang et al. | 2022, arXiv | 2205.10330 | arXiv |
| **R5 navigation** | | | | |
| The dynamic window approach to collision avoidance | Fox, Burgard, Thrun | 1997, IEEE Robotics & Automation Magazine | DOI 10.1109/100.580977 | DOI |
| Integrated online trajectory planning and optimization in distinctive topologies (TEB) | Rösmann, Hoffmann, Bertram | 2017, Robotics and Autonomous Systems | DOI 10.1016/j.robot.2016.11.007 | DOI |
| The Marathon 2: A Navigation System (Nav2) | Macenski, Martín, White, Clavero | 2020, IROS | 2003.00368; DOI 10.1109/IROS45743.2020.9341207 | arXiv (PDF names DWA, DWB, TEB) |
| Motion Planning and Control for Mobile Robot Navigation Using ML: a Survey | Xiao, Liu, Warnell, Stone | arXiv 2020; Autonomous Robots 2022 | 2011.13112; DOI 10.1007/s10514-022-10039-8 | arXiv + Crossref |
| Deep RL based mobile robot navigation: A review | Zhu, Zhang | 2021, Tsinghua Science and Technology | DOI 10.26599/TST.2021.9010012 | DOI |
| Virtual-to-real Deep RL: Continuous Control of Mobile Robots for Mapless Navigation | Tai, Paolo, Liu | 2017, arXiv (IROS 2017) | 1703.00420 | arXiv |
| Target-driven Visual Navigation in Indoor Scenes using Deep RL | Zhu, Mottaghi, Kolve, Lim, Gupta, Fei-Fei et al. | arXiv 2016 (ICRA 2017) | 1609.05143 | arXiv |
| Decentralized Non-communicating Multiagent Collision Avoidance with Deep RL (CADRL) | Chen, Liu, Everett, How | arXiv 2016 (ICRA 2017) | 1609.07845 | arXiv |
| Socially Aware Motion Planning with Deep RL (SA-CADRL) | Chen, Everett, Liu, How | 2017, arXiv (IROS 2017) | 1703.08862 | arXiv |
| Motion Planning Among Dynamic, Decision-Making Agents with Deep RL (GA3C-CADRL) | Everett, Chen, How | 2018, arXiv (IROS 2018) | 1805.01956 | arXiv |
| Towards Optimally Decentralized Multi-Robot Collision Avoidance via Deep RL | Long, Fan, Liao, Liu, Zhang, Pan | arXiv 2017 (ICRA 2018) | 1709.10082 | arXiv |
| Crowd-Robot Interaction: Crowd-aware Robot Navigation with Attention-based Deep RL (SARL) | Chen, Liu, Kreiss, Alahi | ICRA 2019 (arXiv 2018) | 1809.08835 | arXiv |
| PRM-RL: Long-range Robotic Navigation Tasks by Combining RL and Sampling-based Planning | Faust, Ramirez, Fiser, Oslund, Francis, Davidson et al. | ICRA 2018 (arXiv 2017) | 1710.03937 | arXiv |
| Learning Navigation Behaviors End-to-End with AutoRL | Chiang, Faust, Fiser, Francis | RA-L / ICRA 2019 | 1809.10124 | arXiv |
| Long-Range Indoor Navigation with PRM-RL | Francis, Faust, Chiang, Hsu, Kew, Fiser et al. | arXiv 2019, accepted to T-RO | 1902.09458 | arXiv |
| Habitat: A Platform for Embodied AI Research | Savva, Kadian, Maksymets, Zhao, Wijmans, Jain et al. | ICCV 2019 | 1904.01201 | arXiv |
| DD-PPO: Learning Near-Perfect PointGoal Navigators from 2.5 Billion Frames | Wijmans, Kadian, Morcos, Lee, Essa, Parikh et al. | arXiv 2019 (ICLR 2020) | 1911.00357 | arXiv |
| On Evaluation of Embodied Navigation Agents (SPL) | Anderson, Chang, Chaplot, Dosovitskiy, Gupta, Koltun et al. | 2018, arXiv | 1807.06757 | arXiv |
| Learning to Explore using Active Neural SLAM (added) | Chaplot, Gandhi, Gupta, Gupta, Salakhutdinov | ICLR 2020 | 2004.05155 | arXiv |
| Self-supervised Deep RL with Generalized Computation Graphs for Robot Navigation | Kahn, Villaflor, Ding, Abbeel, Levine | ICRA 2018 | 1709.10489 | arXiv |
| BADGR: An Autonomous Self-Supervised Learning-Based Navigation System | Kahn, Abbeel, Levine | arXiv 2020 (journal version 2021 not checked) | 2002.05700 | arXiv |
| Learning to Fly by Crashing (added) | Gandhi, Pinto, Gupta | 2017, arXiv | 1704.05588 | arXiv |
| Learning a State Representation and Navigation in Cluttered and Dynamic Environments | Hoeller, Wellhausen, Farshidian, Hutter | 2021, RA-L | 2103.04351 | arXiv |
| Advanced Skills by Learning Locomotion and Local Navigation End-to-End | Rudin, Hoeller, Bjelonic, Hutter | IROS 2022 | 2209.12827 | arXiv |
| Learning Robust Autonomous Navigation and Locomotion for Wheeled-Legged Robots | Lee, Bjelonic, Reske, Wellhausen, Miki, Hutter | 2024, Science Robotics 9(89) | 2405.01792; DOI 10.1126/scirobotics.adi9641 | arXiv |
| Learning High-Speed Flight in the Wild | Loquercio, Kaufmann, Ranftl, Müller, Koltun, Scaramuzza | 2021, Science Robotics 6(59) | 2110.05113; DOI 10.1126/scirobotics.abg5810 | arXiv |
| Champion-level drone racing using deep RL | Kaufmann, Bauersfeld, Loquercio, Müller et al. | 2023, Nature | DOI 10.1038/s41586-023-06419-4 | DOI + Page |
| Reaching the Limit in Autonomous Racing: Optimal Control versus RL (added) | Song, Romero, Mueller, Koltun, Scaramuzza | 2023, Science Robotics | 2310.10943; DOI 10.1126/scirobotics.adg1462 | arXiv |
| Flightmare: A Flexible Quadrotor Simulator | Song, Naji, Kaufmann, Loquercio, Scaramuzza | CoRL 2020 | 2009.00563 | arXiv |
| GNM: A General Navigation Model to Drive Any Robot (imitation) | Shah, Sridhar, Bhorkar, Hirose, Levine | ICRA 2023 | 2210.03370 | arXiv |
| ViNT: A Foundation Model for Visual Navigation (imitation) | Shah, Sridhar, Dashora, Stachowicz, Black, Hirose et al. | CoRL 2023 | 2306.14846 | arXiv |
| NoMaD: Goal Masked Diffusion Policies for Navigation and Exploration (imitation) | Sridhar, Shah, Glossop, Levine | 2023, arXiv | 2310.07896 | arXiv |
| **R6 legged locomotion** | | | | |
| Learning robust perceptive locomotion for quadrupedal robots in the wild | Miki, Lee, Hwangbo, Wellhausen, Koltun, Hutter | 2022, Science Robotics 7(62) | 2201.08117; DOI 10.1126/scirobotics.abk2822 | arXiv |
| Robot Parkour Learning | Zhuang, Fu, Wang, Atkeson, Schwertfeger, Finn et al. | CoRL 2023, PMLR 229 | 2309.05665; proceedings.mlr.press/v229/zhuang23a | arXiv + Page |
| Extreme Parkour with Legged Robots | Cheng, Shi, Agarwal, Pathak | arXiv 2023; ICRA 2024 | 2309.14341; DOI 10.1109/ICRA57147.2024.10610200 | arXiv + DOI |
| ANYmal parkour: Learning agile navigation for quadrupedal robots | Hoeller, Rudin, Sako, Hutter | arXiv 2023; Science Robotics 2024 | 2306.14874; DOI 10.1126/scirobotics.adi7566 | arXiv + DOI |
| DTC: Deep Tracking Control (added) | Jenelten, He, Farshidian, Hutter | 2024, Science Robotics | 2309.15462; DOI 10.1126/scirobotics.adh5401 | arXiv + DOI |
| Learning-based legged locomotion: state of the art and future perspectives (survey, reading) | Ha, Lee, van de Panne, Xie, Yu, Khadiv | 2024, arXiv | 2406.01152 | arXiv |
| **R7 humanoids** | | | | |
| Learning Agile Soccer Skills for a Bipedal Robot with Deep RL | Haarnoja, Moran, Lever, Huang, Tirumala, Humplik et al. (28 authors) | arXiv 2023; Science Robotics 2024 | 2304.13653; DOI 10.1126/scirobotics.adi8022 | arXiv + DOI |
| Learning Human-to-Humanoid Real-Time Whole-Body Teleoperation (H2O) | He, Luo, Xiao, Zhang, Kitani, Liu et al. | 2024, arXiv | 2403.04436 | arXiv |
| OmniH2O: Universal and Dexterous Human-to-Humanoid Whole-Body Teleoperation and Learning | He, Luo, He, Xiao, Zhang et al. | 2024, arXiv | 2406.08858 | arXiv |
| HumanPlus: Humanoid Shadowing and Imitation from Humans | Fu, Zhao, Wu, Wetzstein, Finn | 2024, arXiv | 2406.10454 | arXiv |
| Expressive Whole-Body Control for Humanoid Robots (Exbody) | Cheng, Ji, Chen, Yang, Yang, Wang | 2024, arXiv | 2402.16796 | arXiv |
| HOVER: Versatile Neural Whole-Body Controller for Humanoid Robots (added) | He, Xiao, Lin, Luo, Xu, Jiang et al. | ICRA 2025 | 2410.21229 | arXiv |
| BeyondMimic: From Motion Tracking to Versatile Humanoid Control via Guided Diffusion (added) | Liao, Truong, Huang, Gao, Tevet, Sreenath et al. | 2025, arXiv | 2508.08241 | arXiv |
| Humanoid Parkour Learning (added) | Zhuang, Yao, Zhao | CoRL 2024 | 2406.10759 | arXiv |
| **R8 manipulation** | | | | |
| Learning Hand-Eye Coordination for Robotic Grasping with Deep Learning and Large-Scale Data Collection | Levine, Pastor, Krizhevsky, Quillen et al. | arXiv 2016; IJRR (online 2017) | 1603.02199; DOI 10.1177/0278364917710318 | arXiv + DOI |
| QT-Opt: Scalable Deep RL for Vision-Based Robotic Manipulation | Kalashnikov, Irpan, Pastor, Ibarz, Herzog, Jang et al. | CoRL 2018, PMLR 87 | 1806.10293; proceedings.mlr.press/v87/kalashnikov18a | arXiv + Page |
| Residual RL for Robot Control | Johannink, Bahl, Nair, Luo, Kumar, Loskyll et al. | 2018, arXiv | 1812.03201 | arXiv |
| Residual Policy Learning | Silver, Allen, Tenenbaum, Kaelbling | 2018, arXiv | 1812.06298 | arXiv |
| Learning Dexterous In-Hand Manipulation | OpenAI: Andrychowicz, Baker, Chociej et al. | 2018, arXiv | 1808.00177 | arXiv |
| DeXtreme: Transfer of Agile In-hand Manipulation from Simulation to Reality | Handa, Allshire, Makoviychuk, Petrenko, Singh et al. | arXiv 2022; ICRA 2023 (short version) | 2210.13702 | arXiv |
| In-Hand Object Rotation via Rapid Motor Adaptation | Qi, Kumar, Calandra, Ma, Malik | CoRL 2022 | 2210.04887 | arXiv |
| Visual Dexterity: In-Hand Reorientation of Novel and Complex Object Shapes | Chen, Tippur, Wu, Kumar, Adelson, Agrawal | arXiv 2022; Science Robotics 2023 | 2211.11744; DOI 10.1126/scirobotics.adc9244 | arXiv + DOI |
| DexPoint: Generalizable Point Cloud RL for Sim-to-Real Dexterous Manipulation | Qin, Huang, Yin, Su, Wang | CoRL 2022 | 2211.09423 | arXiv |
| DexMV: Imitation Learning for Dexterous Manipulation from Human Videos | Qin, Wu, Liu, Jiang, Yang, Fu et al. | 2021, arXiv | 2108.05877 | arXiv |
| Sim-to-Real RL for Vision-Based Dexterous Manipulation on Humanoids (added) | Lin, Sachdev, Fan, Malik, Zhu | CoRL 2025 | 2502.20396 | arXiv |

**Robotics pass: 103 sources checked, none dropped.** Flags:
- Kim et al.: arXiv 2023, published IEEE T-RO 2024 (DOI checked). The user's "Kim et al." is this paper.
- Lee et al. 2023: published at IROS 2024 under a different title (same authors); both IDs recorded.
- Altman's CMDP book: original 1999 Chapman & Hall/CRC; Crossref lists the 2021 Routledge re-issue.
- PPO-Lagrangian has no single origin paper; it is taught with Safety Gym (Ray et al. 2019) and Stooke et al. 2020.
- Radosavovic et al.: Science Robotics 2024 (DOI checked); arXiv ID 2303.03381.
- Venues in brackets (e.g. "IROS 2017", "ICLR 2020") are from the arXiv comment field or common citation and were not checked on the publisher page; arXiv IDs and DOIs were.
- Not used: Ng et al. 1999 (potential-based shaping) could not be checked online; reward shaping is taught from S&B §17.4 instead. The original TEB paper (Rösmann et al. 2012) was not checked; the 2017 RAS paper is used.
- Mostly imitation, not RL (flagged in rows): GNM, ViNT, NoMaD, DexMV, Levine et al. 2018 grasping, the high-level parts of H2O / OmniH2O / HumanPlus.

---

## 4. Lecture companions (DeepMind x UCL)

All three checked with `yt-dlp --flat-playlist`. Lecturers come from each video's YouTube description. Not transcribed yet: English subtitles first, `transcripts/whisper_fetch.py` only if none.

| Playlist | Playlist ID | Lectures | Total length | Lecturer(s) |
|---|---|---|---|---|
| Introduction to Reinforcement Learning 2015 (David Silver, UCL) | `PLqYmG7hTraZDM-OYHWgPebj2MfCFzFObQ` | 10 | 16 h 24 m | David Silver (uploaded 2015-05-13) |
| RL Lecture Series 2021 (YouTube title of the playlist: "DeepMind x UCL \| Deep Learning Lecture Series 2021", but all 13 videos are the RL series) | `PLqYmG7hTraZDVH599EItlEWsUOsJbAodm` | 13 | 19 h 55 m | Hado van Hasselt, Diana Borsa, Matteo Hessel |
| Reinforcement Learning Course 2018 (the RL half of "Advanced Deep Learning & RL") | `PLqYmG7hTraZBKeNJ-JE_eyJHZ7XgBoAyb` | 10 | 16 h 57 m | Hado van Hasselt (1–8, from the descriptions read), Volodymyr Mnih (9), David Silver (10) |

The playlist ID often quoted for the 2018 course (`PLqYmG7hTraZDNJre23vqCGIVpfZ_K2RZs`) no longer exists on YouTube.

### 4.1 Lecture → book chapters → concepts

| Lecture (video ID, length) | S&B chapters | Concepts (Section 1/2 rows) | Status |
|---|---|---|---|
| **2015 L1** Introduction to RL (2pWv7GOvuf0, 1:28:13) | 1, 3.1–3.3 | agent–environment, reward hypothesis, elements of RL, exploration vs exploitation | partial (03) |
| **2015 L2** Markov Decision Process (lfHX2hHRMVQ, 1:42:05) | 3 | Markov property, Markov chain, return, discount, v and q, Bellman equations, Bellman as linear system | new |
| **2015 L3** Planning by Dynamic Programming (Nd1-UUMVfz4, 1:39:09) | 4 | policy evaluation, policy iteration, value iteration, asynchronous DP | new |
| **2015 L4** Model-Free Prediction (PnHCvfgC_ZA, 1:37:01) | 5.1, 6.1–6.3, 7, 12 | MC prediction, TD(0), batch MC vs TD, n-step, TD(λ) | new |
| **2015 L5** Model Free Control (0g4j2k_Ggc4, 1:36:31) | 5.3–5.7, 6.4–6.5, 12.7 | ε-greedy GPI, MC control, Sarsa, Sarsa(λ), Q-learning, importance sampling | new |
| **2015 L6** Value Function Approximation (UoPei5o4fps, 1:36:45) | 9, 10, 11 (parts) | semi-gradient, linear features, LSTD, experience replay, DQN | new / partial |
| **2015 L7** Policy Gradient Methods (KHZVXao4qXs, 1:33:58) | 13 | log-derivative trick, REINFORCE, actor–critic, advantage, compatible features | new / partial |
| **2015 L8** Integrating Learning and Planning (ItMutbeOHtc, 1:40:13) | 8 | models, Dyna, simulation-based search, MCTS | new |
| **2015 L9** Exploration and Exploitation (sGuiWX07sKw, 1:39:18) | 2 | ε-greedy, optimistic values, UCB, contextual bandits | new / partial |
| **2015 L10** Classic Games (kZ_AUmFcZtk, 1:51:24) | 8.11, 16.1, 16.6 | self-play, TD in games, game-tree search | new |
| **2021 L1** Introduction to RL (TCCjZe0y4Qc, 1:29:52) | 1, 3.1 | as 2015 L1 | partial (03) |
| **2021 L2** Exploration & Control (aQJP3Z2Ho8U, 2:10:14) | 2 | bandits, ε-greedy, UCB, gradient bandits (policy gradient on a bandit) | new / partial |
| **2021 L3** MDPs and Dynamic Programming (zSOMeug_i_M, 1:43:56) | 3, 4 | MDP, Bellman equations, policy and value iteration | new |
| **2021 L4** Theoretical Fund. of DP (XpbLq7rIJAA, 1:14:30) | 4 | Bellman operators as contraction mappings, convergence | new (maths) |
| **2021 L5** Model-free Prediction (eaWfWoVUTEw, 1:41:33) | 5, 6, 7 | MC, TD, n-step | new |
| **2021 L6** Model-free Control (t9uf9cuogBo, 1:40:41) | 5, 6 | Sarsa, Q-learning, double Q-learning | new |
| **2021 L7** Function Approximation (ook46h2Jfb4, 2:29:32) | 9, 10, 11 | linear and deep value approximation | new / partial |
| **2021 L8** Planning & Models (FKl8kM4finE, 57:41) | 8 | Dyna, MCTS | new |
| **2021 L9** Policy-Gradient and Actor-Critic (y3oqOjHilio, 1:38:50) | 13 | policy gradient theorem, REINFORCE, actor–critic | new / partial |
| **2021 L10** Approximate Dynamic Programming (AJejcug2brU, 1:42:03) | 11 | error bounds of approximate value / policy iteration | new (maths) |
| **2021 L11** Multi-step & Off Policy (u84MFu1nG4g, 1:32:30) | 7, 11, 12 | importance sampling, control variates, traces, tree backup | new |
| **2021 L12** Deep RL #1 (cVzvNZOBaJ4, 47:05) | 16.5 | practical deep RL, DQN, autodiff (JAX) | new |
| **2021 L13** Deep RL #2 (siDtNqlPoLk, 46:42) | 17.1 | general value functions, auxiliary tasks, scaling issues | new |
| **2018 L1** Introduction to RL (ISk80iLhdfU, 1:43:17) | 1 | as 2015 L1 | partial (03) |
| **2018 L2** Exploration and Exploitation (eM6IBYVqXEA, 1:48:24) | 2 | bandits | new |
| **2018 L3** MDPs and DP (hMbxmRyDw5M, 1:44:24) | 3, 4 | MDP, DP | new |
| **2018 L4** Model-Free Prediction and Control (nnxHlg-2WgA, 1:39:26) | 5, 6 | MC, TD, Sarsa, Q-learning | new |
| **2018 L5** Function Approximation and Deep RL (wAk1lxmiW4c, 1:44:56) | 9–11 | value approximation, DQN | new |
| **2018 L6** Policy Gradients and Actor Critics (bRfUxQs6xIM, 1:34:41) | 13 | policy gradient, actor–critic | new |
| **2018 L7** Planning and Models (Xrxrd8nl4YI, 1:46:51) | 8 | Dyna, MCTS | new |
| **2018 L8** Advanced Topics in Deep RL (L6xaQ501jEs, 1:28:34) | 17 | advanced topics | new |
| **2018 L9** A Brief Tour of Deep RL Agents (-mhBD8Frkc4, 1:37:31) | 16.5 | DQN family, A3C and later agents (Mnih) | new |
| **2018 L10** Classic Games Case Study (ld28AU7DDB4, 1:49:55) | 16.6 | AlphaGo, AlphaGo Zero, AlphaZero (Silver) | new / partial |

The lecture-to-chapter mapping is from the lecture titles and descriptions; it will be checked against the transcripts when they are fetched.

### 4.2 Best lecture per concept

| Concept group | Best lecture | Why |
|---|---|---|
| Bandits, UCB, gradient bandit | 2021 L2 | Longest bandit treatment; ties gradient bandits to policy gradients |
| MDP, return, Bellman equations | 2015 L2 | Silver's student-MDP worked example is the classic first picture |
| DP (policy / value iteration) | 2015 L3 for the pictures; 2021 L4 for why it converges | |
| MC vs TD, n-step, TD(λ) | 2015 L4 | Random-walk and driving-home comparisons |
| Sarsa, Q-learning, control | 2015 L5 | Cliff-walking comparison |
| Off-policy, IS, traces | 2021 L11 | Most recent and most complete |
| Function approximation, DQN | 2021 L7 | Covers both linear and deep |
| Approximate DP theory | 2021 L10 | Only lecture on it |
| Policy gradient, actor–critic | 2015 L7 for the derivation; 2021 L9 for the modern view | |
| Planning, Dyna, MCTS | 2015 L8 | |
| Deep RL agents (DQN family, A3C) | 2018 L9 (Mnih, DQN's first author) | |
| AlphaGo / AlphaZero | 2018 L10 (Silver) | Covers Zero; 2015 L10 predates AlphaGo |
| Deep RL in practice, GVFs | 2021 L12–13 | |

None of the three playlists covers robotics, RLHF, offline RL or VLAs. For those, use Section 4.3 and the sources in Section 8.

### 4.3 Robotics companions (lectures, docs, code)

Playlists checked with `yt-dlp --flat-playlist`; pages and repositories loaded (HTTP 200) on 2026-10-03.

| Companion | ID / URL | Use for (blocks) |
|---|---|---|
| CS 285 Deep RL, 2023 (Levine), 99 videos | `PL_iWQOsE6TfVYGEGiAOMaOzzv41Jfm_Ps` | L2 "Imitation Learning" parts 1–5 → behaviour cloning, DAgger (13.3); L22 "Transfer Learning & Meta-Learning" parts 1–5 → sim-to-real, adaptation (13.1, 13.3); L20 "Inverse RL" → learned rewards (13.2); L23 "Challenges & Open Problems" → 13.0 |
| Foundations of Deep RL (Abbeel), 6 lectures | `PLwRJQ4m4UJjNymuBM9RdmB3Z9N5-0IlY0` | L4 "TRPO and PPO" fills the PPO gap of the DeepMind playlists (Block 10); L3 policy gradients and advantage estimation |
| legged_gym | <https://github.com/leggedrobotics/legged_gym> | Reference env: observations, reward terms, terrain curriculum, randomisation (13.0–13.2, 13.6) |
| rsl_rl | <https://github.com/leggedrobotics/rsl_rl> | Reference PPO for robots (13.0) |
| Isaac Lab docs: task workflows (manager-based vs direct) | <https://isaac-sim.github.io/IsaacLab/main/source/overview/core-concepts/task_workflows.html> | Setting up a training env (13.0, 13.5) |
| MuJoCo XLA (MJX) docs; MuJoCo Playground | <https://mujoco.readthedocs.io/en/stable/mjx.html>, <https://playground.mujoco.org/> | GPU simulation in JAX (13.0) |
| Walk These Ways code | <https://github.com/Improbable-AI/walk-these-ways> | Behaviour families, sim-to-real deployment (13.2, 13.6) |
| Extreme Parkour code; Robot Parkour Learning code | <https://github.com/chengxuxin/extreme-parkour>, <https://github.com/ZiwenZhuang/parkour> | Parkour, distillation (13.6) |
| RMA project page; CaT project page | <https://ashish-kmr.github.io/rma-legged-robots/>, <https://constraints-as-terminations.github.io/> | Adaptation (13.3); constraints as terminations (13.4) |
| Safety-Gymnasium; OmniSafe | <https://github.com/PKU-Alignment/safety-gymnasium>, <https://github.com/PKU-Alignment/omnisafe> | Constrained RL exercises (13.4) |
| Nav2 docs (DWB and MPPI controllers) | <https://docs.nav2.org/> | Classical baseline for 13.5 |
| Gazebo | <https://gazebosim.org/> | ROS navigation training and testing (13.5) |
| Habitat (site and habitat-lab) | <https://aihabitat.org/>, <https://github.com/facebookresearch/habitat-lab> | Embodied navigation at scale, SPL (13.5) |
| CrowdNav | <https://github.com/vita-epfl/CrowdNav> | Crowd navigation environment (13.5) |
| MIT ACL `rl_collision_avoidance` | <https://github.com/mit-acl/rl_collision_avoidance> | Multi-agent collision avoidance code (13.5) |
| Flightmare | <https://github.com/uzh-rpg/flightmare> | Quadrotor simulation (13.5) |
| Stable-Baselines3 HER docs | <https://stable-baselines3.readthedocs.io/en/master/modules/her.html> | Hindsight Experience Replay in code (13.2, 13.8) |

---

## 5. Overlap with the robotics book scopes: who owns what

"Owner" writes the Note; the other scopes recap in a few lines and link. One concept, one Note.

| Shared concept | Probabilistic Robotics | Planning Algorithms | Owner |
|---|---|---|---|
| Markov property, Markov chain | Ch. 2 Markov assumption | — | **This RL scope** (Block 0). PR Ch. 2 recaps and adds the HMM / Bayes filter, which PR owns |
| MDP, discount, return | Ch. 14 | Ch. 10 | **This RL scope** (S&B Ch. 3) |
| Value function, Bellman equation | Ch. 14 | Ch. 2 cost-to-go, Ch. 10 | **This RL scope** |
| Value iteration, policy iteration | Ch. 14 | Ch. 2, Ch. 10 | **This RL scope** (S&B Ch. 4). PR keeps "value iteration for robot path planning on a grid" as an application Note |
| MC and TD evaluation, Q-learning | — | Ch. 10 | **This RL scope** |
| POMDP, belief space, alpha vectors, QMDP, AMDP, MC-POMDP | Ch. 15–16 | Ch. 11–12 | **Probabilistic Robotics**. S&B 17.3 recaps |
| Game against nature, minimax, alpha-beta, Nash | — | Ch. 9–10 | **Planning Algorithms** |
| MCTS, self-play, AlphaGo | — | — | **This RL scope** |
| Monte Carlo estimation, importance sampling | Ch. 4 | Ch. 11 | **This RL scope** (Block 0), since S&B Ch. 5 needs them first; PR Ch. 4 recaps and adds resampling and particle filters |
| KL divergence | Ch. 8 (KLD-sampling) | — | **This RL scope** (Block 0); TRPO, PPO, RLHF and DPO all need it |
| Multivariate normal | Ch. 2–3 | Ch. 11 | **Already covered by 640** (glossary lists it there); all three recap |
| Priority queue, A*, heuristic search | — | Ch. 2 | **Planning Algorithms**; S&B Ch. 8 recaps |
| Information-gain exploration | Ch. 17 | — | **Probabilistic Robotics**. Bandit exploration (ε-greedy, UCB) is owned here |
| HJB equation, LQR | — | Ch. 15 | **Planning Algorithms** |
| Conjugate gradient | Ch. 11 | — | **Probabilistic Robotics**; TRPO recaps |
| Sim-to-real, domain randomization, VLAs | — | — | **This RL scope** (no robotics book covers them) |
| Lagrange multipliers, duality, KKT, LP/QP | — | — | **Existing Maths Notes 620, 621, 622**. This scope owns only the new parts: primal–dual updates of λ, log-barrier and exact-penalty terms inside RL (Block 0) |
| Kalman filter, state estimation | Ch. 3 | — | **Probabilistic Robotics**. Learned estimators (R3.9) recap it as the classical contrast |
| Quaternions, 3D rotations | — | Ch. 4 | **Planning Algorithms**. Projected gravity (R2.2) recaps |
| Occupancy grids, costmaps | Ch. 9 | Ch. 3 (bitmaps) | **Probabilistic Robotics**. Navigation observation design (N.6) recaps |
| PRM | — | Ch. 5 | **Planning Algorithms**. PRM-RL (N.15) recaps |
| DWA, TEB, Nav2 local controllers | not listed | not listed | **Proposed: Planning Algorithms scope** (local / feedback planning). Neither book scope lists them yet, so this needs adding there; until then the "Classical local planners and what RL changes" Note (Block 13.5) carries a short background section |
| Behaviour cloning, DAgger, teacher–student | — | — | **This RL scope** (Block 13.3) |
| Variational autoencoder, contrastive loss | — | — | **This RL scope** (Block 0 bridge); no DL Note covers them (1003 only names autoencoders) |
| PD / PID control | — | — | **This RL scope** (Block 13.0), short; a control-theory scope would own it if one is added |
| Diffusion and flow matching | — | — | **Unowned, flagged**: needed by π0 (2E) and BeyondMimic / NoMaD (R7, R5); belongs in a generative-models scope |

---

### 5.1 Owners decided on 2026-10-03

- **Classical local planners (DWA, TEB, Nav2 controllers): owned by this scope**, as two background concept Notes at the start of block 13.5: "Classical local planning: DWA and TEB" and "The Nav2 navigation stack". Neither robotics book scope covers them. Autonomous navigation is the user's primary interest, and learned local planners are taught by contrast with them. If the Planning Algorithms scope later covers them, it links here.
- **Diffusion models and flow matching: owned by a new deep-learning block, "Generative models for control"** (about 3 Notes: VAE, which moves here from Block 0; diffusion models; flow matching). It sits after the transformer Notes and before block 13. It is needed by pi0, BeyondMimic, NoMaD and Diffusion Policy.

## 6. How RL builds on our existing Notes

- **MDP** ← conditional probability (341, 82), total probability (86). The Markov chain is the one missing piece.
- **Bellman equation** ← expected value (332): v(s) is an expectation of the return, split into "reward now + discounted value next".
- **Bellman as a linear system** ← matrix inverse (54).
- **Incremental and constant-step updates** ← EWMA (1033). The same formula, with a different name.
- **Monte Carlo** ← law of large numbers (241, 331), CLT (271).
- **Function approximation** ← regression (50–55), SGD (57–60, 1020), MSE (52), neural nets (1010–1017).
- **Policy gradient** ← gradients (601), log-likelihood and its derivative (73, 74), softmax (79). REINFORCE is "maximise log-likelihood of good actions, weighted by return".
- **Actor–critic, DQN** ← neural nets (1001–1031), CNN (1040–1045), Huber loss (1014), Adam (1038), gradient clipping (1018).
- **PPO and RLHF** ← RLHF in 1067 (reward model, three steps); PPO is the RL step there.
- **DPO, Bradley–Terry** ← sigmoid (72), log loss (73).
- **SAC** ← entropy (97). **TRPO** ← KL (named in 1014).
- **Recurrent policies, Dreamer** ← LSTM / GRU (1061–1064).
- **Decision Transformer** ← masked self-attention (1081), GPT-style decoder (1085).
- **VLAs (RT-2, OpenVLA, π0)** ← transformers (1071–1085), ViT (named in 1071), transfer learning and fine-tuning (1053).
- **Constrained RL (R4)** ← Lagrange multipliers, duality, KKT (620), convexity and saddle points (621), interior-point methods named in 622. The CMDP Lagrangian is the Ridge-as-constrained-least-squares idea of 620 with an expected cost in place of ‖w‖².
- **Teacher–student and DAgger (R3)** ← supervised regression (50–55), loss functions (1014), knowledge distillation named in 1071.
- **History encoders (R3.2)** ← LSTM / GRU (1061–1064), convolution (1042), masked attention (1081).
- **Symmetry augmentation (R2.12)** ← data augmentation (1050).
- **Style rewards (R2.14, H.2)** ← GAN generator and discriminator (named in 1003).
- **Observation scaling (R2.1)** ← standardization (24). **Tracking kernel (R2.6)** ← normal-curve shape (250). **Projected gravity (R2.2)** ← rotation matrices (500).
- **Contrastive loss (R3.12)** ← cosine similarity (362).

---

## 7. Suggested learning order

Each block needs the blocks above it. "Prereq" lists our existing Notes. "Lectures" are the primary companions (Section 4).

**Block 0: Maths bridge (about 8 Notes).**
Markov property and Markov chains (transition matrix, stationary distribution); geometric series and discounting; Monte Carlo estimation; importance sampling (ordinary, weighted, variance); KL divergence; step-size conditions (Robbins–Monro); log-derivative trick; control variates and baselines.
Added for robotics: **constrained optimisation inside learning** (recap 620–622, then primal–dual updates of λ by gradient ascent, log-barrier terms, exact ReLU penalties; R4.3, R4.6, R4.7) and **variational autoencoders and contrastive losses** (R3.10, R3.12). The cross-entropy method (M.4), temporal convolution (R3.2) and PID control (R0.7) are short sections inside the Notes that use them, not separate Notes.
Prereq: 241, 331, 332, 341, 86, 271, 73, 74, 601, 1033, 1014; for the additions 620, 621, 622, 1003, 362. Lectures: 2015 L2 (Markov chains), 2021 L11 (IS, control variates).

**Block 1: Bandits (S&B Ch. 2; about 3 Notes).**
k-armed bandit; sample averages and incremental update; ε-greedy; optimistic start; UCB; gradient bandit; contextual bandits.
Prereq: Block 0, 221, 280, 79, 1033. Lectures: 2021 L2, 2015 L9.

**Block 2: MDPs (S&B Ch. 1, 3; about 4 Notes).**
Agent–environment interface; return and discount; policy; v and q; Bellman expectation and optimality equations; linear-system solution; backup diagrams.
Prereq: Block 0, 03, 332, 54. Lectures: 2015 L1–L2, 2021 L1, L3.

**Block 3: Dynamic programming (S&B Ch. 4; about 3 Notes).**
Policy evaluation; policy improvement theorem; policy iteration; value iteration; asynchronous DP; GPI; contraction (2021 L4).
Prereq: Block 2. Lectures: 2015 L3, 2021 L3–L4.

**Block 4: Monte Carlo methods (S&B Ch. 5; about 3 Notes).**
MC prediction; MC control; exploring starts; ε-soft; off-policy by importance sampling.
Prereq: Block 3. Lectures: 2015 L4–L5, 2021 L5–L6.

**Block 5: TD learning (S&B Ch. 6–7; about 4 Notes).**
TD(0); batch TD vs MC; Sarsa; Q-learning; expected Sarsa; double Q-learning; n-step TD and Sarsa; tree backup.
Prereq: Block 4, 631. Lectures: 2015 L4–L5, 2021 L5–L6, L11.

**Block 6: Planning and learning (S&B Ch. 8; about 3 Notes).**
Models; Dyna-Q and Dyna-Q+; prioritized sweeping; trajectory sampling; rollouts; MCTS.
Prereq: Block 5; priority queue from the Planning Algorithms scope. Lectures: 2015 L8, 2021 L8.

**Block 7: Function approximation (S&B Ch. 9–12; about 5 Notes).**
VE objective; semi-gradient TD; linear features (polynomial, Fourier, tile coding, RBF); LSTD; neural approximators; average reward; deadly triad and Baird's example; projected Bellman error and gradient-TD; λ-return, eligibility traces, TD(λ), Sarsa(λ).
Prereq: Block 5, 52, 53, 54, 59, 61, 95, 520, 1010–1017. Lectures: 2015 L6, 2021 L7, L10, L11.

**Block 8: Policy gradient and actor–critic (S&B Ch. 13 + Williams 1992, Sutton et al. 2000, Konda & Tsitsiklis 2000; about 4 Notes).**
Parameterized policies; policy gradient theorem; REINFORCE; baseline; actor–critic; advantage; Gaussian policies.
Prereq: Block 7, 73, 74, 79, 250, 640, 601. Lectures: 2015 L7, 2021 L9.

**Block 9: Deep value-based RL (about 3 Notes).**
DQN: experience replay, target network, error clipping; double DQN; the DQN family.
Prereq: Block 7, 1040–1045, 1014, 1038. Lectures: 2021 L12, 2018 L9.

**Block 10: Deep policy methods (about 6 Notes).**
A3C/A2C; TRPO (KL trust region, natural gradient); GAE; PPO; DDPG; TD3; SAC (maximum entropy, reparameterization).
Prereq: Blocks 8–9, 97, 1033. Lectures: 2018 L9; no DeepMind lecture covers PPO, use Abbeel's "Foundations of Deep RL" L4 (Section 4.3) and Spinning Up.

**Block 11: Games and search (about 3 Notes).**
AlphaGo; AlphaGo Zero; AlphaZero; MuZero.
Prereq: Blocks 6, 9. Lectures: 2018 L10, 2015 L10.

**Block 12: Model-based deep RL (about 2 Notes).**
World models; DreamerV3.
Prereq: Block 11, 1064. Lectures: 2021 L8.

**Block 13: RL for robotics (nine sub-blocks, about 42 Notes).**
Concept Notes, never paper Notes; papers are worked examples inside them. Row IDs refer to Section 2D. Navigation (13.5) is the primary and deepest track; legged locomotion, humanoids and manipulation get equal weight after it. Each sub-block names the **RL lesson** it teaches, so the robotics blocks double as RL lessons.

| Sub-block | Proposed concept Notes | RL lesson it teaches | Prereq | Companions |
|---|---|---|---|---|
| **13.0 Robot RL foundations** (3) | Why robot RL is hard; The robot as an MDP: control rate and action interfaces (PD/PID, torques, velocity commands); Parallel simulation and the reference training stack | The MDP boundary is a design choice; action-space choice shapes exploration; on-policy RL when samples are cheap | Blocks 8, 10; 600 | CS285 L23; legged_gym; rsl_rl; Isaac Lab docs |
| **13.1 Sim-to-real** (3) | The reality gap and domain randomization (visual, dynamics, ADR); System identification, actuator networks and delta-action models; Real-robot training and sim–real agreement | Train on a distribution of MDPs; model learning; distribution shift between train and test | 13.0; 1010; 50–55 | CS285 L22; legged_gym randomisation config |
| **13.2 Designing the task** (5) | Observation design for robot policies; Reward design and shaping for robots; Terminations and curricula; Sparse rewards, goals and hindsight relabelling; Symmetry, behaviour families and learned style rewards | Reward hypothesis in practice; shaping changes the optimum; termination is part of the return; **sparse reward → shaping, curricula, HER**; goal-conditioned policies | 13.0; 24, 250, 500, 1050, 1003 | legged_gym rewards and curriculum code; SB3 HER docs; CS285 L20 |
| **13.3 Partial observability and privileged information** (5) | History encoders; Asymmetric actor–critic; Behaviour cloning and DAgger; Teacher–student distillation and adaptation modules; Learned estimators (concurrent, latent, contrastive) | **Partial observability → history encoders, POMDP beliefs**; **privileged information → asymmetric actor–critic, teacher–student**; imitation and distribution shift; meta-learning through memory | 13.2; Block 0 (VAE); 1061–1064, 1042, 1081 | CS285 L2 (imitation), L22; RMA page |
| **13.4 Safety and constraints** (4) | Constrained MDPs and cost critics; Lagrangian and PID-Lagrangian PPO; CPO, barriers and penalties; Constraints in practice (constraint types, constraints as terminations, shields, recovery) | **Safety → constrained MDPs**; primal–dual optimisation; termination as a penalty | 13.2; Block 0 (constrained optimisation); 620–622; Block 10 TRPO/PPO | Safety-Gymnasium; OmniSafe; CaT page |
| **13.5 RL for autonomous navigation** (10) | Classical local planners and what RL changes; Navigation as an MDP and mapless navigation; Observations and actions for navigation policies; Reward design for navigation; Visual navigation, memory and auxiliary tasks; Multi-agent and crowd navigation; Planners plus RL, and modular navigation; Navigation at scale and how to evaluate it (SPL); Self-supervised and sim-to-real navigation; Navigation on legged, wheeled-legged and aerial robots | Task formulation; dense shaping vs sparse goals; **exploration** in large spaces; auxiliary losses; multi-agent RL and parameter sharing; hierarchy; evaluation metrics; off-policy learning from real data | 13.1–13.4; PR occupancy grids; PA PRM | Nav2 docs; Gazebo; Habitat; CrowdNav; Flightmare; skills view 2D.10 |
| **13.6 Legged locomotion** (4) | The PPO locomotion recipe (worked example); Perceptive locomotion; Agility and parkour; Hybrid model-based + RL locomotion | Putting 13.0–13.4 together; curriculum over dynamics; distillation; hierarchy | 13.1–13.4 | legged_gym; Walk These Ways and parkour repos |
| **13.7 Humanoids** (4) | Motion imitation and adversarial motion priors; Humanoid locomotion sim-to-real; Whole-body tracking from human data (RL tracker vs imitation layer); Multi-skill humanoid controllers (distillation, self-play, multi-mode) | Imitation through a reward; learned rewards; in-context adaptation; self-play; multi-task distillation | 13.3, 13.6; 1003 | CS285 L20 (inverse RL) |
| **13.8 Manipulation** (4) | Grasping at scale with off-policy RL (QT-Opt, CEM); Goals, residual RL and demonstrations; Dexterous in-hand manipulation; Vision-based dexterity (teacher–student, point clouds, human video) | Off-policy learning from large logged data; **sparse reward → HER**; residual policies; randomisation + memory | 13.1–13.3; Block 9 | SB3 HER docs |

The navigation track (13.5) can start right after 13.2 for a learner in a hurry: 13.0 → 13.1 → 13.2 → 13.5, then 13.3 and 13.4 as needed.

**Block 14: Offline RL (about 3 Notes).**
Offline setting and distribution shift; CQL; Decision Transformer.
Prereq: Block 10, 1081, 1085.

**Block 15: RL for language models (about 5 Notes).**
Preference reward models and Bradley–Terry; InstructGPT RLHF with PPO and KL penalty; DPO; GRPO; RL with verifiable rewards (DeepSeek-R1, Tulu 3); 2025 fixes (DAPO, Dr. GRPO).
Prereq: Block 10, 1067, 1085, 72, 73.

**Block 16: Robot foundation models and real-world RL (about 4 Notes).**
VLAs (RT-2, OpenVLA); flow-matching action experts (π0, π0.5); RL fine-tuning of VLAs (π*0.6 / RECAP); real-world RL (SERL, HIL-SERL); context: Gemini Robotics, GR00T N1.
Prereq: Blocks 13–15, 1053, 1071.

**Block 17: Looking deeper (optional; about 3 Notes).**
Psychology (S&B Ch. 14); neuroscience and dopamine (Ch. 15); case studies (Ch. 16); frontiers: GVFs, options, reward design (Ch. 17).
Prereq: Block 8. Lectures: 2021 L13.

**Proposed total: about 108 Notes** (8 + 3 + 4 + 3 + 3 + 4 + 3 + 5 + 4 + 3 + 6 + 3 + 2 + 42 + 3 + 5 + 4 + 3 = 108). Block 13 alone: 3 + 3 + 5 + 5 + 4 + 10 + 4 + 4 + 4 = 42 (was 6). Block 0: 8 (was 6).

---

## 8. Visual and animation ideas

Library choices follow the project rule (no matplotlib). Manim for step-by-step processes; Plotly for interactive curves; seaborn only for static summary plots.

| Process | Animation idea | Library | Why this library |
|---|---|---|---|
| Bandit learning | 10 arms with true means; bars of estimates grow toward them; ε-greedy vs greedy reward curves | Manim + Plotly | Manim for the arms over time; Plotly for comparing curves |
| UCB | Each arm's estimate with a shrinking confidence bar; the chosen arm lights up | Manim | Bars must change step by step |
| Return and discount | Rewards along a path, each shrinking by γ; the sum appears | Manim | A step-by-step build-up |
| Value iteration on a gridworld | Grid cells change colour sweep by sweep; arrows (greedy policy) settle | Manim | The classic picture; frame-by-frame |
| Policy iteration | Alternating evaluate (colours) and improve (arrows) frames | Manim | Shows the two-phase loop |
| MC vs TD | Same random-walk episode; MC updates only at the end, TD updates every step | Manim | Side-by-side timing is the point |
| Q-learning agent exploring | Agent walks a cliff gridworld; Q-arrows grow; Sarsa vs Q-learning paths differ | Manim | Movement plus changing table |
| Eligibility traces | Trace bars decay behind the agent; one TD error updates them all | Manim | Decay over time |
| Tile coding | Several shifted grids over a 2D state; the active tiles light up | Manim | Geometric layering |
| MCTS | Tree grows: select, expand, simulate, back up, with visit counts | Manim | Tree drawing step by step |
| Policy gradient | Bar chart of action probabilities shifting toward rewarded actions; on a 2D Gaussian policy the mean drifts | Manim | Changing distribution |
| Actor–critic | Two networks: critic's TD error arrow feeds the actor update | Manim | Data-flow diagram that moves |
| PPO clipping | Plot of the clipped objective against the probability ratio, for positive and negative advantage | Plotly | Interactive slider on ε |
| KL divergence | Two distributions; slider moves one; KL value updates | Plotly | Interactive |
| DQN | Replay buffer filling; random minibatch drawn; target network copying every N steps | Manim | Process over time |
| Domain randomization | One robot scene with colours, masses and friction changing frame by frame | Manim | Many variations in sequence |
| RLHF / DPO | Pairwise preference → reward model → policy update pipeline; DPO skips the middle box | Manim | Pipeline with a removed step |
| GRPO | A group of answers to one prompt, scored, advantages = score minus group mean | Manim | Simple group bars |
| PD control of a joint (R0.5) | Step response of one joint to a target angle; sliders for Kp and Kd show overshoot vs sluggishness | Plotly | Interactive sliders on two gains |
| Terrain curriculum (R2.10) | Grid of terrain levels; each robot moves up after walking far, down after falling short | Manim | Many agents changing level step by step |
| Reward terms (R2.5, N.8) | Stacked contribution of each reward term along one episode; toggle terms on and off | Plotly | Interactive legend toggling |
| Asymmetric actor–critic and teacher–student (R3.4, R3.7) | Two networks: critic/teacher fed the full state, actor/student fed only sensors; the arrow that disappears at deployment | Manim | Data flow that changes between training and deployment |
| RMA adaptation (R3.8) | Phase 1: env factors → extrinsics → policy; Phase 2: history → predicted extrinsics; terrain changes and the estimate follows | Manim | Two-phase process over time |
| Lagrangian PPO vs PID Lagrangian (R4.3, R4.4) | Cost and λ over training iterations; plain λ oscillates around the limit, PID settles | Plotly | Comparing curves with hover |
| Constraints as terminations (R4.10) | Termination probability rising with constraint violation; slider for the maximum probability | Plotly | Interactive curve |
| Laser-scan observation (N.5) | Robot with range rays, goal shown as distance and angle in the robot frame, rays shortening near obstacles | Manim | Geometry that moves with the robot |
| DWA vs learned planner (N.1, N.2) | DWA samples a velocity window and scores arcs; the RL policy outputs one (v, ω) directly | Manim | Side-by-side process |
| Multi-agent collision avoidance (N.11) | Several agents crossing; value-network choice vs straight-line paths | Manim | Agents moving together |
| SPL (N.19) | Agent path vs shortest path; the SPL fraction fills in per episode | Manim | Build-up of the formula |
| Hindsight relabelling (R2.11) | Failed episode; the reached point becomes the new goal and the episode turns into a success | Manim | One clear before/after transformation |
| Symmetry augmentation (R2.12) | A trajectory and its left–right mirror added to the batch | Manim | Mirroring is a geometric transformation |

### Gold-standard visual and teaching sources (all checked, page loaded)

| Source | URL | Use for |
|---|---|---|
| David Silver's UCL course page (slides) | <https://www.davidsilver.uk/teaching/> | Slides for the 2015 lectures |
| DeepMind x UCL 2015 playlist | <https://www.youtube.com/playlist?list=PLqYmG7hTraZDM-OYHWgPebj2MfCFzFObQ> | Core lectures |
| DeepMind x UCL 2021 playlist | <https://www.youtube.com/playlist?list=PLqYmG7hTraZDVH599EItlEWsUOsJbAodm> | Core lectures |
| DeepMind x UCL 2018 RL playlist | <https://www.youtube.com/playlist?list=PLqYmG7hTraZBKeNJ-JE_eyJHZ7XgBoAyb> | Deep RL agents, AlphaZero |
| OpenAI Spinning Up | <https://spinningup.openai.com/en/latest/> | Policy-gradient derivation, PPO, DDPG, TD3, SAC |
| Hugging Face Deep RL Course | <https://huggingface.co/learn/deep-rl-course/unit0/introduction> | Hands-on units, Q-learning to PPO |
| Hugging Face blog: Illustrating RLHF | <https://huggingface.co/blog/rlhf> | RLHF pipeline pictures |
| Berkeley CS 285 (Levine) | <https://rail.eecs.berkeley.edu/deeprlcourse/> | Deep RL, offline RL, robotics |
| Karpathy REINFORCEjs gridworld (DP and TD demos) | <https://cs.stanford.edu/people/karpathy/reinforcejs/gridworld_dp.html>, <https://cs.stanford.edu/people/karpathy/reinforcejs/gridworld_td.html> | Live value iteration and TD in the browser |
| Karpathy, "Pong from Pixels" | <https://karpathy.github.io/2016/05/31/rl/> | Policy gradient explained with code |
| Lilian Weng, "Policy Gradient Algorithms" | <https://lilianweng.github.io/posts/2018-04-08-policy-gradient/> | One-page map of PG methods |
| Gymnasium | <https://gymnasium.farama.org/> | Standard environments for code examples |
| Isaac Lab | <https://isaac-sim.github.io/IsaacLab/main/index.html> | Parallel robot RL (successor setting of Rudin 2022) |
