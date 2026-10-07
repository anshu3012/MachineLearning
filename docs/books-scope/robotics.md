# Scope: Robotics and reinforcement learning, one plan

**Summary.** This is the plan for all robotics and reinforcement learning Notes: **382 Notes in two Subjects: Reinforcement Learning (RL) and Robotics (RO), with Robotics in four submodules: Perception, Localization, Control, and Navigation and planning**, plus **49 new Maths/Machine Learning/Deep Learning prerequisite Notes** (§4) and new sections for 11 existing Maths/Machine Learning Notes (§5). It is a scoping list only, not study Notes.

The first draft (188 Notes, 2026-10-07) came from three books and left whole areas out: path tracking, MPC, cameras and optical flow, visual odometry, arm kinematics and dynamics, legged models, the system architecture, tracking other agents, and imitation learning. This plan was rebuilt from **survey papers first**, then textbooks and university courses.

**Evidence docs.** Each one keeps its rows, sources and checks. This plan cites their rows by ID.

| Doc | Area | Row IDs |
|---|---|---|
| [reinforcement-learning.md](reinforcement-learning.md) | Sutton & Barto, deep reinforcement learning, robot reinforcement learning, frontier | `SB2.7`, `C.18`, `R3.10`, `N.1` … |
| [probabilistic-robotics.md](probabilistic-robotics.md) | Thrun, Burgard & Fox | `PR 4.2` … |
| [planning-algorithms.md](planning-algorithms.md) | LaValle | `PA 8.7` … |
| [robot-control.md](robot-control.md) | Path tracking, vehicle models, LQR, MPC, trajectories, quadrotors | `CT-001` … |
| [robot-perception.md](robot-perception.md) | Cameras, features, optical flow, two-view geometry, VO, SfM, LiDAR, IMU, fusion, detection | `PE-001` … |
| [robot-mechanics.md](robot-mechanics.md) | Rigid-body motion, kinematics, dynamics, arm control, grasping, legged models, whole-body control | `ME-001` … |
| [robotics-curricula-audit.md](robotics-curricula-audit.md) | What 12 university courses and the Nav2 and Autoware stacks teach that the rest lacked | `AU-001` … |
| [robot-learning-surveys.md](robot-learning-surveys.md) | Learning-based robotics, mapped from 26 surveys | `RS-001` … |
| [index-check/](index-check/) | The term-by-term completeness check (see "Completeness check" below) | `idx:<concept>` |

Every row is placed exactly once. That covers the 589 book rows, the 518 rows of the five new docs, and all 188 Notes of the first draft. Each row is in one of four places:
- in a Note;
- recapped from an Maths/Machine Learning/Deep Learning Note (§7);
- in new maths: a prerequisite Note (§4), a section of an existing Note (§5) or a short section (§6);
- dropped with a reason (§9).

Source keys such as `PA16`, `SN09`, `RVC3` and `MR` are defined in the evidence doc that the row ID points to.

**How it was chosen.** The steps:
1. **Two merged plans.** A put robotics foundations first (409 Notes). B interleaved robotics and reinforcement learning by first use (356 Notes).
2. **Two critics.** Both rejected A, which reaches learned navigation only at Note 310. Both rebuilt from B, checked the plans by script and argued for two rounds.
3. **Ruling.** Where they still differed, the orchestrator ruled: LSTD and gradient-TD are optional, because no robotics survey uses them; imitation learning and offline reinforcement learning get separate chapters, because the surveys treat them as separate families.
4. **Final check.** The plan was checked against 85 method families taken from five surveys (Paden 2016, Cadena 2016, Xiao et al. 2022, Ha et al. 2024, Yurtsever 2020). All 85 are present.

## Completeness check

The second draft (359 Notes) still missed fundamentals. Missing in every sense: the Laplacian (image Laplacian, Laplace's equation, graph Laplacian, Laplace transform), transfer functions, Bode plots, open vs closed loop, and PID tuning. Survey papers assume these, so a survey-built plan misses them.

So every term in these sources was checked one by one. Each term got a written verdict: **taught** (the Note that lists it), **add** (where it goes), **out of scope** (a reason that can be checked), or **noise** (names, symbols, pointers).

**Book indexes (free official copies):**
- Lynch & Park, *Modern Robotics*
- LaValle, *Planning Algorithms*
- Correll et al., *Introduction to Autonomous Robots*: authors' source index, since the free PDF has none
- Åström & Murray, *Feedback Systems*
- Bullo, *Lectures on Network Systems*
- Deisenroth et al., *Mathematics for Machine Learning*
- Barfoot, *State Estimation for Robotics*
- Szeliski, *Computer Vision* (2010 draft)
- Prince, *Computer Vision: Models, Learning, and Inference*
- Sutton & Barto
- Kochenderfer et al., *Algorithms for Decision Making*
- Kochenderfer & Wheeler, *Algorithms for Optimization*
- Rawlings, Mayne & Diehl, *Model Predictive Control*

**Read from contents (no free index):** Murray, Li & Sastry; Tedrake, *Underactuated Robotics*.

**University course schedules (24 courses):** UCSD, CMU, Stanford, Michigan, ETH, Bonn, Freiburg, MIT, Georgia Tech, Berkeley, Caltech and Cornell.

**Lecture playlists (14):** Stachniss (Bonn), Lynch, Tedrake, Levine, Nayar, Khatib, Brunton and MATLAB.

**Online reference pages:** robotics, control, computer vision and machine learning outlines and glossaries.

**Totals:** 13,470 terms. 5,696 taught, 1,698 add, 4,163 out of scope, 1,896 noise, 17 mentioned only.

**Checking the verdicts.**
- A script tested every "taught" verdict against the cited Note's own concept list. 774 failures were judged by hand: 734 confirmed and 34 turned into adds.
- The adds merged into 234 unique concepts. Each was searched for in the existing Notes: 10 were already taught and were dropped, and 224 are placed in this plan.
- The ledgers are in [index-check/](index-check/). Search any term there to see where it is taught, or why it was left out.

**Limit.** The check proves completeness against these sources, not against everything.

## 1. Structure

| Subject | Title | Submodules (Notes) | Chapters | Notes | Optional | Why |
|---|---|---|---|---|---|---|
| RL | Reinforcement Learning | Core (62), Reinforcement Learning for Robots (92) | 18 | 154 | 12 | All reinforcement learning. Core: the algorithms on their own, with no robot needed. Reinforcement Learning for Robots: sim-to-real, task design, privileged learning and safety; then learned locomotion, humanoids and manipulation, imitation, offline reinforcement learning and foundation models. These build on the Robotics models and controllers, which they replace or combine with. |
| RO | Robotics | Perception (38), Localization (34), Control (80), Navigation and planning (76) | 24 | 228 | 28 | Classical robotics in four submodules: Perception, Localization, Control, and Navigation and planning. Navigation also holds the learned navigation policy (the primary track), which builds on Reinforcement Learning for Robots. |

## 2. Reading order, and why

Subjects and submodules are folders: they group Notes by what they teach. The **reading order** (the Course order) interleaves them, the same way Maths Notes sit between Machine Learning Notes, so each Note comes just before its first user. Every "#" in §3 is the Note's place in the reading order, and every "Builds on" points to a smaller number.

1. **Reinforcement learning core first (Notes 1–50).** Its only robotics needs are a priority queue and a heuristic, and each Note builds its own (S&B §8.4, §8.9). Reinforcement learning theory and games (RL-07) and reinforcement learning for language models (RL-08) are optional, because the robotics surveys treat them as minor.
2. **The classical robotics stack next.** Navigation is the primary track:
   - robot models (Robotics / Control);
   - uncertainty and Bayes filters (Robotics / Localization);
   - sensors (Robotics / Perception);
   - localization, maps and pose-graph SLAM;
   - C-space and planning (Robotics / Navigation and planning);
   - classical feedback control, then path tracking (Robotics / Control);
   - the navigation stack: ROS 2, behaviour trees, Nav2 (Note 140).
3. **Reinforcement learning for robots, then learned navigation:** sim-to-real, task design and partial observability (Reinforcement Learning / Reinforcement Learning for Robots), then Navigation I from Note 162.
4. **Each later block sits just before the chapter that first uses it:**
   - objects and people (Perception) before Navigation II and III;
   - LQR and MPC before aerial robots;
   - visual odometry before navigation with language and foundation models.
5. **Arms and legs come after navigation.**
   - Model-based first: kinematics, dynamics, contact and grasping, legged balance (Robotics / Control).
   - Then the learned versions: learned locomotion, humanoids, learned manipulation, imitation, offline reinforcement learning, foundation models (Reinforcement Learning / Reinforcement Learning for Robots).
   - Legged robots, manipulation and humanoids rank equal second.
6. **Optional depth comes last.** Nothing outside an optional chapter builds on it:
   - car dynamics;
   - SLAM and estimation in depth;
   - planning in depth;
   - reinforcement learning theory and games;
   - reinforcement learning for language models.

## 3. The Notes

"Builds on" gives a number for an earlier Note in this plan, a label for an Maths/Machine Learning/Deep Learning Note, or "new Maths Note"/"new Deep Learning Note" for a Note still to be written (§4).

## Reinforcement Learning (RL)


### Reinforcement Learning / Core


#### RL-01 Learning by trial: bandits

Act, get a number back, learn which action pays: explore vs exploit in one state.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 1 | The reinforcement learning problem | reward as a number to maximise over time, possibly delayed; exploration vs exploitation; four elements: policy, reward, value function, model; evolutionary (policy search) vs value-function methods; formal RL definitions in robotics; Evaluative vs instructive feedback | ML-003 | SB1.1, SB1.2, SB1.3, SB1.5, PR 14.2, idx:evaluative_feedback | Sutton&Barto 2018 ch.1; Thrun et al. 2005 ch.14; Sutton & Barto, RL |
| 2 | Multi-armed bandits and epsilon-greedy | k-armed bandit and true action value; sample-average action values; greedy and epsilon-greedy selection; 10-armed testbed | 1, MA-005 | SB2.1, SB2.2, SB2.3, SB2.4 | Sutton&Barto 2018 ch.2; DeepMind x UCL 2021 L2 |
| 3 | Incremental updates and step sizes | incremental update new = old + step x (target - old); step-size conditions (Robbins-Monro) | 2, DL-033 | SB2.5, SB2.7 | Sutton&Barto 2018 ch.2 |
| 4 | Exploring smartly: optimistic starts and UCB | optimistic initial values; upper-confidence-bound selection; Thompson sampling (posterior sampling); Softmax (Boltzmann) exploration over action values; Regret of an exploration strategy | 3, MA-035, new Maths Note: Bayesian estimation: posteriors and conjugate priors, ML-078 | SB2.8, SB2.9, idx:thompson_sampling, idx:boltzmann_exploration, idx:regret | Sutton&Barto 2018 ch.2; Kochenderfer et al., Algorithms for Decision Making; Sutton & Barto, RL; LaValle, Planning Algorithms |
| 5 | Gradient bandits | softmax over action preferences with a baseline | 2, ML-078 | SB2.10 | Sutton&Barto 2018 ch.2 |
| 6 | Contextual bandits | contextual bandits (associative search); personalized web services example | 2 | SB2.11, SB16.7 | Sutton&Barto 2018 ch.2; Sutton&Barto 2018 ch.16 |

#### RL-02 Markov decision processes and dynamic programming

Many states: the formal model, returns, policies, value functions and Bellman equations.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 7 | Markov decision processes | agent-environment interface per time step; MDP dynamics p(s', r \| s, a); reward hypothesis; forward projections and backprojections | 1, new Maths Note: Markov chains, MA-014 | SB3.1, SB3.4, SB3.5, PR 14.3, PA 10.1, PA 10.2 | Sutton&Barto 2018 ch.3; Thrun et al. 2005 ch.14; LaValle 2006 ch.10; DeepMind x UCL 2015 L2 |
| 8 | Return and discounting | return, episodes, episodic vs continuing tasks; discount factor and horizon; infinite horizon: discounted and average cost; delayed reward and the credit-assignment problem; Absorbing terminal state | 7, new Maths Note: Geometric series | SB3.6, PR 14.4, PA 10.5, SB14.6, idx:absorbing_state | Sutton&Barto 2018 ch.3; Thrun et al. 2005 ch.14; LaValle 2006 ch.10; Kochenderfer et al., Algorithms for Decision Making; Sutton & Barto, RL |
| 9 | Policies, plans and value functions | policy as a conditional distribution over actions; state-value and action-value functions; state, action and state transition of a planning problem; feasible vs optimal plan; open-loop plan vs feedback plan; feedback plan as a policy over the whole state space | 8, MA-012, ML-003, MA-066 | SB3.8, SB3.9, PA 1.1, PA 1.2, PA 1.3, PA 8.1 | Sutton&Barto 2018 ch.3; LaValle 2006 ch.1; LaValle 2006 ch.8 |
| 10 | Bellman equations | Bellman expectation equation; backup diagrams; Bellman equation as a linear system; principle of optimality; Markov reward process | 9, MA-019, ML-053, new Maths Note: Markov chains | SB3.10, SB3.11, SB3.14, B.1, PR 14.5, idx:mrp | Sutton&Barto 2018 ch.3; Thrun et al. 2005 ch.14; Bellman 1957; Sutton & Barto, RL |
| 11 | Optimal values and optimal policies | optimal value functions and the Bellman optimality equation; optimal policy is greedy w.r.t. q*; tabular vs approximate solutions | 10 | SB3.12, SB3.13, SB3.15 | Sutton&Barto 2018 ch.3 |
| 12 | Policy evaluation | iterative policy evaluation; bootstrapping: update a guess from a guess | 10 | SB4.1, SB4.7 | Sutton&Barto 2018 ch.4; DeepMind x UCL 2015 L3 |
| 13 | Policy improvement and policy iteration | policy improvement theorem; policy iteration | 12, 11 | SB4.2, SB4.3, PA 10.4 | Sutton&Barto 2018 ch.4; LaValle 2006 ch.10 |
| 14 | Value iteration | value iteration; cost-to-go as the planning name for value; value iteration with nature (stochastic outcomes); Bellman operator as a contraction: why value iteration converges | 13, MA-049 | SB4.4, PA 2.8, PA 10.3, PR 14.6, idx:bellman_contraction | Sutton&Barto 2018 ch.4; LaValle 2006 ch.2; LaValle 2006 ch.10; Thrun et al. 2005 ch.14; Kochenderfer et al., Algorithms for Decision Making; Sutton & Barto, RL |
| 15 | Asynchronous DP and generalized policy iteration | asynchronous DP; generalized policy iteration (GPI); curse of dimensionality for DP | 14, ML-045 | SB4.5, SB4.6, SB4.8 | Sutton&Barto 2018 ch.4 |

#### RL-03 Learning values from experience: Monte Carlo and TD

No model: learn from sampled episodes and from one-step bootstrapping.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 16 | Monte Carlo prediction | first-visit and every-visit MC prediction; MC estimation of action values; evaluating a plan by simulation | 12, new Maths Note: Monte Carlo estimation | SB5.2, SB5.3, PA 10.6 | Sutton&Barto 2018 ch.5; LaValle 2006 ch.10; DeepMind x UCL 2015 L4 |
| 17 | Monte Carlo control | exploring starts; epsilon-soft on-policy MC control | 16, 15 | SB5.4, SB5.5 | Sutton&Barto 2018 ch.5 |
| 18 | Off-policy learning with importance sampling | on-policy vs off-policy; target vs behaviour policy; incremental weighted average; off-policy MC control; discounting-aware and per-decision IS | 17, new Maths Note: Importance sampling | SB5.6, SB5.9, SB5.10, SB5.11 | Sutton&Barto 2018 ch.5 |
| 19 | TD(0) prediction | TD(0) and the TD error; TD = sampling + bootstrapping; batch TD vs batch MC; certainty equivalence; tic-tac-toe value learning; afterstates | 16, 12, MA-070 | SB6.1, SB6.2, SB6.3, SB1.4, SB6.8 | Sutton&Barto 2018 ch.6; Sutton&Barto 2018 ch.1; Sutton 1988 |
| 20 | Sarsa and expected Sarsa | Sarsa (on-policy TD control); expected Sarsa | 19, 17 | SB6.4, SB6.6 | Sutton&Barto 2018 ch.6; DeepMind x UCL 2015 L5 |
| 21 | Q-learning | Q-learning (off-policy TD control); convergence of Q-learning | 20, 18, 3 | SB6.5, PA 10.7, B.3 | Sutton&Barto 2018 ch.6; LaValle 2006 ch.10; Watkins & Dayan 1992 |
| 22 | Double Q-learning | maximization bias and double Q-learning | 21 | SB6.7 | Sutton&Barto 2018 ch.6 |
| 23 | n-step bootstrapping | n-step return and n-step TD; n-step Sarsa; n-step off-policy learning with IS; control variates; tree-backup algorithm; n-step Q(sigma) | 19, 18 | SB7.1, SB7.2, SB7.3, SB7.4, SB7.5, SB7.6 | Sutton&Barto 2018 ch.7; DeepMind x UCL 2021 L11 |
| 24 | Eligibility traces and TD(lambda) | lambda-return; eligibility traces; forward vs backward view; online and true online TD(lambda); Sarsa(lambda); variable lambda and gamma; off-policy traces | 23 | SB12.1, SB12.2, SB12.3, SB12.4, SB12.5, SB12.6, B.2 | Sutton&Barto 2018 ch.12; Sutton 1988 |

#### RL-04 Approximate values and policy gradients

Too many states for a table: features and linear values, why off-policy approximation diverges, then training the policy itself.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 25 | Value prediction as supervised learning | value approximation with moving targets; VE objective weighted by state visits; semi-gradient methods | 19, ML-051, ML-058 | SB9.1, SB9.2, SB9.3 | Sutton&Barto 2018 ch.9; DeepMind x UCL 2021 L7 |
| 26 | Linear value functions and features | linear TD and the TD fixed point; Fourier basis features; coarse coding; tile coding; RBF features; choosing the step size by hand; State aggregation | 25, ML-052, ML-089, ML-060 | SB9.4, SB9.6, SB9.7, SB9.8, SB9.9, SB9.10, idx:state_aggregation | Sutton&Barto 2018 ch.9; Sutton & Barto, RL |
| 27 | Control with approximation and the average-reward setting | episodic semi-gradient Sarsa (mountain car); semi-gradient n-step Sarsa; average-reward setting and differential values; why discounting breaks with approximation; differential semi-gradient n-step Sarsa | 26, 23, new Maths Note: Markov chains | SB10.1, SB10.2, SB10.3, SB10.4, SB10.5 | Sutton&Barto 2018 ch.10 |
| 28 | The deadly triad | off-policy semi-gradient methods; Baird's counterexample; deadly triad: approximation + bootstrapping + off-policy | 27, 18 | SB11.1, SB11.2, SB11.3 | Sutton&Barto 2018 ch.11 |
| 29 | Parameterised policies | policy as the trained model; softmax in action preferences; performance measure J(theta); Value-function methods vs policy search | 5, 9 | SB13.1, SB13.2, RS-002 | Sutton&Barto 2018 ch.13; DeepMind x UCL 2015 L7; Kober §2.2 |
| 30 | The policy gradient theorem and REINFORCE | policy gradient theorem; log-derivative trick; compatible features; Monte Carlo policy gradient (REINFORCE family); Reward-to-go in policy gradients | 29, MA-062, ML-072, 16 | SB13.3, SB13.4, B.5, SB13.5, B.4, idx:reward_to_go | Sutton&Barto 2018 ch.13; Sutton et al. 2000; Williams 1992; Kochenderfer et al., Algorithms for Decision Making |
| 31 | Baselines | baseline as a control variate for variance reduction | 30, 23 | SB13.6 | Sutton&Barto 2018 ch.13 |
| 32 | Actor-critic | one-step actor-critic; policy gradient for continuing problems; two-timescale actor-critic | 31, 19, 27 | SB13.7, SB13.8, B.6 | Sutton&Barto 2018 ch.13; Konda & Tsitsiklis 2000 |
| 33 | Gaussian policies for continuous actions | Gaussian policy and the gradient of its log-density | 29, MA-024, MA-073 | SB13.9 | Sutton&Barto 2018 ch.13 |
| 34 | Advantage and generalized advantage estimation | advantage function A = Q - V; GAE: lambda-weighted TD errors | 32, 24, DL-033 | C.14, C.15 | Schulman et al. 2016 (GAE) |

#### RL-05 Deep RL algorithms

The algorithms robots are trained with, a gradient-free baseline, and how to report results honestly.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 35 | Deep Q-networks | CNN trained with Q-learning targets on raw pixels; error clipping in the TD loss; human-level Atari play | 21, 25, DL-040, DL-014 | C.1, C.4, SB16.5 | Sutton&Barto 2018 ch.16; Mnih et al. 2015 |
| 36 | Experience replay and target networks | experience replay; target network; Catastrophic forgetting (interference) | 35, 28 | C.2, C.3, idx:catastrophic_forgetting | Mnih et al. 2015; Kochenderfer et al., Algorithms for Decision Making; Sutton & Barto, RL |
| 37 | Parallel advantage actor-critic (A2C/A3C) | parallel workers; entropy bonus | 34, ML-091, DL-020 | C.8 | Mnih et al. 2016 |
| 38 | Trust regions: TRPO | trust region and surrogate objective; natural gradient and Fisher information | 37, new Maths Note: KL divergence, new Maths Note: Sparse linear solves and conjugate gradient, MA-064 | C.12, C.13 | Schulman et al. 2015 |
| 39 | Proximal policy optimisation (PPO) | clipped surrogate objective; several epochs per batch | 38 | C.16 | Schulman et al. 2017; Abbeel Foundations of Deep RL L4 |
| 40 | Deterministic policy gradients: DDPG | deterministic policy gradient for continuous actions; soft (Polyak) target updates and exploration noise | 36, 33, DL-033 | C.9, C.10 | Lillicrap et al. 2016 |
| 41 | TD3 | clipped double Q, delayed policy updates, target policy smoothing | 40, 22 | C.19 | Fujimoto et al. 2018 |
| 42 | Soft actor-critic (SAC) | maximum-entropy RL, soft Q and temperature; tanh-squashed Gaussian policy (reparameterization); Control as probabilistic inference; max-entropy RL as variational inference | 41, ML-091, new Deep Learning Note: Variational autoencoder | C.17, C.18, idx:control_as_inference | Haarnoja et al. 2018; Berkeley CS 185/285 Deep Reinforcement Learning |
| 43 | Black-box policy search: evolution strategies and the cross-entropy method | Black-box policy search: perturb parameters, keep what scores well (finite differences, evolution strategies, CMA-ES, reward-weighted averaging); short section: derivative-free optimisation, the family ES and CEM belong to (local search, simulated annealing, genetic algorithms named) | 29, new Maths Note: Monte Carlo estimation | RS-003, idx:local_search_sa, idx:genetic_algorithms, idx:spsa | Kober §2.2.2 |
| 44 | Reporting RL results honestly: seeds, interquartile mean and confidence intervals | K1 Reporting RL results honestly: many seeds, interquartile mean, confidence intervals | 39, MA-035, new Maths Note: Bootstrap confidence intervals and the interquartile mean | AU-045 | Agarwal et al. 2021, *Deep RL at the Edge of the Statistical Precipice* ([arXiv 2108.13264](https://arxiv.org/abs/2108.13264)) |

#### RL-06 Planning with models

Use a model to plan: Dyna, rollouts, MCTS, learned dynamics and world models.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 45 | Models and Dyna | distribution vs sample models; Dyna-Q: planning, acting and learning together; wrong models and the Dyna-Q+ bonus; model-free (habitual) vs model-based (goal-directed) control | 21 | SB8.1, SB8.2, SB8.3, SB14.7 | Sutton&Barto 2018 ch.8; DeepMind x UCL 2015 L8 |
| 46 | Prioritized sweeping and where to spend updates | prioritized sweeping; expected vs sample updates; trajectory sampling and real-time DP | 45 | SB8.4, SB8.5, SB8.6 | Sutton&Barto 2018 ch.8 |
| 47 | Decision-time planning and rollouts | decision-time planning with heuristic search; rollout algorithms | 45 | SB8.7, SB8.8 | Sutton&Barto 2018 ch.8 |
| 48 | Monte Carlo tree search | MCTS: selection, expansion, simulation, backup | 47, 4 | SB8.9 | Sutton&Barto 2018 ch.8 |
| 49 | Model-based RL with learned dynamics: sampling planners, ensembles and model exploitation | Model-based RL for robots: learn the dynamics, plan with it (random shooting / CEM with a learned model), guard against the policy exploiting model errors | 45, 47, 43, DL-010 | RS-005 | Kober §6; Ibarz §4.2.1, §4.6 |
| 50 | World models and imagined rollouts | recurrent world model; learning in imagination (Dreamer) | 48, 42, DL-064, 49 | E.11 | Hafner et al. 2023 |

#### RL-07 RL theory, games and self-play (minor in the robotics surveys) *(optional)*

Optional: LSTD and gradient-TD (in no robotics survey), games, self-play and MuZero (minor: about one mention each), Decision Transformer, and RL for language models.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 51 | Least-squares TD and nonparametric value functions | LSTD: solve the TD fixed point directly; memory-based value approximation; kernel-based value approximation | 26, ML-053, 25, ML-085, ML-089 | SB9.12, SB9.13, SB9.14 | Sutton&Barto 2018 ch.9 |
| 52 | Bellman error geometry and gradient-TD | projected Bellman error in a weighted norm; residual-gradient methods; the Bellman error is not learnable; gradient-TD (GTD2, TDC); emphatic TD; interest and emphasis | 28, MA-055 | SB11.4, SB11.5, SB11.6, SB11.7, SB11.8, SB9.15 | Sutton&Barto 2018 ch.11; Sutton&Barto 2018 ch.9; DeepMind x UCL 2021 L10 |
| 53 | Decisions against nature | game against nature: worst-case vs expected-cost decisions; Bayesian decision making with observations; utility theory and rationality; multi-objective optimisation and Pareto-optimal plans; Scalarising several objectives: weighted sum and the constraint method; Value of information | MA-012, MA-018, MA-066 | PA 9.4, PA 9.5, PA 9.9, PA 9.1, PA 7.8, idx:scalarisation, idx:value_of_information | LaValle 2006 ch.9; LaValle 2006 ch.7; Kochenderfer & Wheeler, Algorithms for Optimization; Kochenderfer et al., Algorithms for Decision Making |
| 54 | Games: minimax, alpha-beta and equilibria | zero-sum games, minimax and saddle points; mixed strategies solved by linear programming; nonzero-sum games and Nash equilibrium; game trees and alpha-beta pruning; sequential games on state spaces | 53, MA-068, MA-066 | PA 9.6, PA 9.7, PA 9.8, PA 10.8, PA 10.9 | LaValle 2006 ch.9; LaValle 2006 ch.10; DeepMind x UCL 2015 L10 |
| 55 | Self-play: from TD-Gammon to AlphaZero | self-play TD learning (TD-Gammon, Samuel checkers); policy network + value network + tree search; self-play from scratch; MCTS as policy improvement; one algorithm for several board games | 48, 54, 35, 30 | SB16.1, SB16.2, SB16.6, C.5, C.6, C.7 | Sutton&Barto 2018 ch.16; Silver et al. 2016; Silver et al. 2017; DeepMind x UCL 2018 L10 |
| 56 | Planning with a learned model: MuZero | learned latent model (representation, dynamics, prediction) + MCTS | 55 | E.10 | Schrittwieser et al. 2020 |

#### RL-08 RL for language models *(optional)*

reward models, RLHF, DPO, GRPO, RLVR

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 57 | Reward models from human preferences | reward model trained on pairwise preferences; Bradley-Terry preference model | DL-067, ML-071, ML-072 | E.1, E.2 | Christiano et al. 2017 |
| 58 | RLHF with PPO and a KL penalty | SFT, reward model, PPO with a KL penalty to the SFT model | 57, 39, new Maths Note: KL divergence | E.3 | Ouyang et al. 2022 |
| 59 | Direct preference optimisation | closed-form optimal policy of KL-regularised reward; preference loss without RL | 58 | E.4 | Rafailov et al. 2023 |
| 60 | Group-relative advantages: GRPO | no critic: compare answers to the same prompt | 58, 31 | E.5 | Shao et al. 2024 |
| 61 | RL with verifiable rewards | rule-based rewards (accuracy, format); R1-Zero without SFT; the RLVR recipe | 60 | E.6, E.7 | DeepSeek-AI 2025; Lambert et al. 2024 |
| 62 | Fixing GRPO at scale | decoupled clipping and dynamic sampling (DAPO); length bias and the Dr. GRPO fix | 61 | E.8, E.9 | Yu et al. 2025; Liu et al. 2025 |

### Reinforcement Learning / Reinforcement Learning for Robots


#### RL-09 Robot RL foundations and sim-to-real

Turning a robot into an MDP and getting a simulator-trained policy onto hardware.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 141 | Why robot RL is hard | why robot RL is hard; value-function vs policy-search methods on robots; using models, demonstrations and prior knowledge; Why robot RL is hard: high dimensions, costly real samples, model errors, goal specification; Map of robot competencies: locomotion, navigation, manipulation, mobile manipulation, HRI, multi-robot | 39, 42 | R0.1, R0.2, R0.3, RS-001, RS-012 | Kober, Bagnell & Peters 2013; CS285 2023 L23; Kober §3; Ibarz §1; Tang §3.1 |
| 142 | The robot as an MDP | control rate, observation, action interface, episode and reset; Formulation and solution axes: action level, observation type, reward density; sim use, expert data, on/off-policy/offline optimiser | 141, 7 | R0.4, RS-013 | legged_gym config; Tang §3.2-3.3 |
| 143 | Action spaces: torques, PD targets, velocity commands | joint position targets tracked by a PD controller; choosing the action space; PD joint targets under an RL policy | 142, 120 | R0.5, R0.6, CT-111 | legged_gym; Hwangbo et al. 2019; Peng & van de Panne 2017; Chen et al. 2022; Tai et al. 2017; robotics.md (RL R0.5) |
| 144 | Parallel simulation and the reference training stack | massively parallel on-policy training on one GPU; simulators and frameworks (Isaac Lab, MuJoCo, Gazebo, Habitat); reading legged_gym + rsl_rl; Simulators for robot learning | 143, 39 | R0.8, R0.9, R0.10, RS-097 | Rudin et al. 2022; Makoviychuk et al. 2021; Isaac Lab 2025; Todorov et al. 2012; Zhao §III-F |
| 145 | Delays and control rate: acting while the robot keeps moving | Delays and control rate: the robot keeps moving while the policy thinks | 143, 144 | RS-009 | Ibarz §4.8 |
| 146 | The reality gap and domain randomization | sim-to-real gap; visual domain randomization; dynamics randomization; sensor noise and latency modelling; Zero-shot transfer with domain randomization and pushes; System ID, domain randomization, domain adaptation | 144, DL-050 | R1.1, R1.2, R1.3, R1.9, RS-089, RS-050 | Tobin et al. 2017; Peng et al. 2018; Sadeghi & Levine 2017; Zhao §III-A, §III-C, §III-E; Muratore §5.1; Ha §5.2-5.4 |
| 147 | Visual domain adaptation: making sim and real images look alike | Visual domain adaptation: make sim and real images look alike, or share features | 146, DL-050, new Deep Learning Note: Generative adversarial networks | RS-006 | Ibarz §4.3.3; Zhao §III-D |
| 148 | System identification and actuator models | system identification and actuator networks; delta (residual) action model learned from real data; delta action model for agile humanoid skills; first quadruped sim-to-real: simple reward + actuator model + randomisation; System identification; H2 Odometry and actuator calibration; Simulation-based inference: fit a distribution over sim parameters to real data; Fitting linear dynamical models from data: least-squares A and B, ARX; equation vs simulation error | 146, DL-010, ML-049, ML-053 | R1.5, R1.6, H.8, L.2, RS-090, AU-035, RS-094, idx:linear_sysid | Tan et al. 2018; Hwangbo et al. 2019; He et al. 2025 (ASAP); Zhao §III-B; Muratore §4.6; RO 83; Muratore §4.8; Tedrake, Underactuated Robotics (book + course + lectures) |
| 149 | Real-robot training and sim-real agreement | training on the real robot instead; does sim performance predict real performance?; Measuring the reality gap; Learning on real robots for days: automatic resets, reset-free learning, a changing world | 148, 42 | R1.7, R1.8, RS-093, RS-008 | Haarnoja et al. 2019; Kadian et al. 2020; Muratore §3.4; Ibarz §4.7, §4.12; Tang §5 |
| 150 | Robust RL: training against the worst case or an adversary | Robust RL: train against the worst case or an adversary (robust MDP, RARL, adversarial DR) | 146, 39 | RS-092 | Muratore §5.3; García §3.1; Brunke §3.2.4 |

#### RL-10 Designing the robot task: observations, rewards, curricula

What the policy sees, what it is paid for, when episodes end, how training gets harder.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 151 | Proprioceptive observations | proprioceptive observation design; projected gravity as an orientation feature | 142, ML-023, new Maths Note: 3D rotations: Euler angles and quaternions | R2.1, R2.2 | legged_gym; Rudin et al. 2022 |
| 152 | Seeing the terrain: exteroceptive inputs | height samples, scandots, depth and laser inputs | 151, 98 | R2.3 | Miki et al. 2022; Cheng et al. 2024 |
| 153 | Goal- and command-conditioned policies | command- and goal-conditioned policies | 151, 9 | R2.4 | Andrychowicz et al. 2017 |
| 154 | Reward = task terms + regularisation terms | task terms plus penalty terms; exponential tracking kernel | 153, MA-024 | R2.5, R2.6 | legged_gym; Kim et al. 2024 |
| 155 | Reward shaping and its risks | reward shaping and reward hacking; designing reward signals: sparse, shaped, imitation, inverse RL; Potential-based reward shaping (keeps the optimal policy) | 154 | R2.8, SB17.4, idx:potential_shaping | Sutton&Barto 2018 ch.17; Ma et al. 2024 (Eureka); Kochenderfer et al., Algorithms for Decision Making |
| 156 | Gaits from rewards and behaviour families | gait shaping: feet air time, clearance, energy; gaits emerging from energy minimisation; a family of behaviours in one policy | 155 | R2.7, L.8, R2.13 | Margolis & Agrawal 2022; Fu et al. 2021 |
| 157 | Terminations and the sign of rewards | terminations cut future reward; negative rewards teach early falls | 154, 8 | R2.9 | legged_gym; Chane-Sane et al. 2024 |
| 158 | Curricula: terrain, commands and automatic domain randomization | game-inspired terrain curriculum; grid-adaptive command curriculum; widen randomisation ranges when the policy succeeds at the edge; Adaptive domain randomization (tune ranges from results) | 153, 146 | R2.10, R1.4, RS-091 | Rudin et al. 2022; Margolis et al. 2022; OpenAI et al. 2019; Muratore §5.2 |
| 159 | Sparse rewards and hindsight relabelling | Hindsight Experience Replay; goal-conditioned manipulation with sparse rewards | 153, 36, 40 | R2.11, M.5 | Andrychowicz et al. 2017; SB3 HER docs |
| 160 | Symmetry augmentation | mirrored data augmentation and mirror loss | 151, DL-050 | R2.12 | Mittal et al. 2024; Su et al. 2024 |
| 161 | Searching for rewards automatically | evolutionary search over reward weights and network shape (AutoRL); reward code written by a language model; Rewards from success classifiers and goal images; LLM-written rewards | 155 | N.16, R2.15, RS-010, RS-118 | Chiang et al. 2019; Ma et al. 2024 (Eureka, DrEureka); Ibarz §4.9; Firoozi §III-C |

#### RL-11 Partial observability, privileged learning and adaptation

The robot cannot see the full state: memory, privileged critics and teachers, adaptation, learned estimators, pixel RL.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 171 | History encoders: memory for a hidden state | frame stacks, temporal convolution, GRU/LSTM and transformer history encoders | 162, DL-061, DL-064, DL-042, DL-082 | R3.2 | Lee et al. 2020; Radosavovic et al. 2024 |
| 172 | Privileged information | privileged information: what sim knows and the robot does not; Curriculum, hierarchical, privileged training | 171 | R3.3, RS-049 | Chen et al. 2019 (Learning by Cheating); Ha §4 |
| 173 | Asymmetric actor-critic | critic sees the full state, actor sees observations | 172, 32 | R3.4 | Pinto et al. 2018; Nahrendra et al. 2023 |
| 174 | Behaviour cloning, compounding error and DAgger | behaviour cloning and compounding error; DAgger: label the states the learner visits | 172, ML-049, DL-014 | R3.5, R3.6, RS-061 | Ross et al. 2011; CS285 2023 L2; Zare §II |
| 175 | Teacher-student distillation | privileged RL teacher, sensor student trained on its own rollouts; Distillation into a deployable student | 174, 173, DL-071 | R3.7, RS-095 | Chen et al. 2019; Lee et al. 2020; Miki et al. 2022; Zhao §II-D |
| 176 | Online adaptation modules (RMA) | extrinsics latent and an adaptation module from history; Online adaptation | 175, 171 | R3.8, RS-096 | Kumar et al. 2021 (RMA); Muratore §4.7; Ha §5.4 |
| 177 | Learned state estimators: explicit and latent | estimator network trained with the policy (velocity, foot height, contact); history encoder predicting velocity and a latent terrain code; Learned state estimators for legged robots | 176, 80, new Deep Learning Note: Variational autoencoder, new Deep Learning Note: Contrastive learning objective | R3.9, R3.11, PE-108 | Ji et al. 2022; Nahrendra et al. 2023; Long et al. 2023; RO 103 |
| 178 | In-context adaptation with sequence models | adaptation from history without weight updates; humanoid walking sim-to-real with a causal transformer, zero-shot; In-context learning for decisions | 171, 146, DL-087 | R3.13, H.3, RS-115 | Radosavovic et al. 2024; OpenAI et al. 2019; Firoozi §III-D |
| 179 | Auxiliary tasks and general value functions | general value functions; auxiliary losses (depth, loop closure) for representation | 171, 25 | R3.14, SB17.1 | Sutton&Barto 2018 ch.17; Mirowski et al. 2017; DeepMind x UCL 2021 L13 |
| 180 | Multi-task and meta-RL: learning to adapt to a new task fast | Multi-task and meta-RL: learn to adapt fast to a new task | 178, 176 | RS-011 | Ibarz §4.10; Zhao §II-E; Muratore §4.2 |
| 181 | RL from pixels: image augmentation and contrastive auxiliary losses | K8 RL from pixels: image augmentation and contrastive auxiliary losses | 179, DL-050, new Deep Learning Note: Contrastive learning objective | AU-053 | Laskin et al. 2020, CURL ([arXiv 2004.04136](https://arxiv.org/abs/2004.04136)); Kostrikov et al. 2020, DrQ ([arXiv 2004.13649](https://arxiv.org/abs/2004.13649)) |

#### RL-12 Safety and constraints

Say what not to do: constrained MDPs, Lagrangian/CPO/barrier methods, risk, shields, barrier-function filters, safe exploration.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 201 | Constrained MDPs and cost critics | constrained MDP; cost signals and cost critics; Constrained MDPs, Lagrangian and CPO | 7, 32, MA-066 | R4.1, R4.2, RS-098 | Altman 1999; Achiam et al. 2017; García §3.3; Gu safe §3.1.1 |
| 202 | Lagrangian and PID-Lagrangian PPO | learned multiplier by gradient ascent on violation (PPO-Lagrangian); multiplier update as a PID controller | 201, 39, MA-067, 120 | R4.3, R4.4 | Ray et al. 2019; Stooke et al. 2020 |
| 203 | CPO, barriers and penalties | trust-region constrained update (CPO); log-barrier methods (IPO); exact penalty methods (P3O) | 202, 38, MA-068 | R4.5, R4.6, R4.7 | Achiam et al. 2017; Liu et al. 2020; Zhang et al. 2022 |
| 204 | Not only rewards but also constraints: constraint types for real robots | probabilistic and average constraints; task in reward, rest as constraints; side-by-side comparison on a quadruped; safe-RL benchmarks and libraries; Safe RL benchmarks: Safety Gym, Safety-Gymnasium, safe-control-gym | 203 | R4.8, R4.9, R4.13, RS-105 | Kim et al. 2024 (T-RO); Lee et al. 2023; Safety-Gymnasium; OmniSafe; Gu et al. 2022; Gu safe §6; Brunke §4 |
| 205 | Constraints as terminations | violation sets a termination probability | 204, 157 | R4.10 | Chane-Sane et al. 2024 (CaT) |
| 206 | Shields, safety filters and recovery policies | shields and safety filters; recovery policies and reach-avoid values; Safe exploration with outside knowledge: demos, teacher advice; Formal methods and shields; Temporal logic task specifications (LTL) | 201 | R4.11, R4.12, RS-100, RS-104, idx:temporal_logic | Alshiekh et al. 2018; He et al. 2024 (ABS); García §4.1; Gu safe §3.1.3; Kochenderfer et al., Algorithms for Decision Making |
| 207 | Risk-sensitive RL: caring about bad outcomes | Risk-sensitive RL: care about bad outcomes, not just the average (variance, CVaR); Value at risk (the quantile) beside CVaR | 201, MA-008 | RS-099, idx:var_risk | García §3.2; Brunke §3.2.2; Kochenderfer & Wheeler, Algorithms for Optimization |
| 208 | Lyapunov certificates and control barrier function filters | Control barrier functions and safety filters (QP that minimally edits the action); Stability certificates with Lyapunov functions; Control Lyapunov functions and the CLF-CBF QP | 206, 203, MA-068, new Maths Note: Stability of dynamical systems | RS-103, RS-102, idx:clf | Brunke §3.3.2; Gu safe §3.1.2; Brunke §3.3.1; Rawlings, Mayne & Diehl, MPC; Tedrake, Underactuated Robotics (book + course + lectures); Åström & Murray, Feedback Systems |
| 209 | Safe exploration with an uncertainty model | Safe exploration with an uncertainty model (Gaussian process, SafeOpt, learning MPC) | 208, ML-new: Gaussian processes | RS-101 | Brunke §3.1, §3.2.1; Gu safe §3.1.4 |

#### RL-13 Learned locomotion

The PPO locomotion recipe and its extensions, model-based plus learned control, bipeds, legged navigation, loco-manipulation.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 330 | The PPO locomotion recipe, end to end | PD targets + proprioception + tracking/penalty rewards + terrain curriculum + randomisation + teacher-student; Deep RL for locomotion (PPO recipe); Locomotion MDP parts: sim or real dynamics, proprio/extero observations, reward terms, PD joint targets | 158, 175, 205 | L.1, RS-046, RS-047 | Rudin et al. 2022; Lee et al. 2020; Hwangbo et al. 2019; Ha §2.2; Ha §3.1-3.4 |
| 331 | Perceptive locomotion | attention-based recurrent fusion of proprioception and a noisy height map | 330, 152 | L.3 | Miki et al. 2022 |
| 332 | Agility: high speed and parkour | adaptive velocity curriculum + online system identification for running; soft-then-hard obstacle curriculum; distil skills into one depth policy with DAgger; parkour-style learning on humanoids; Hard terrain and parkour | 331, 176, 174 | L.4, L.5, H.10, RS-056 | Margolis et al. 2022; Zhuang et al. 2023; Cheng et al. 2024; Zhuang et al. 2024; Ha §8.3 |
| 333 | Tracking model-based reference motions | RL learns to track a planner reference (DTC) | 330, 118, 325 | L.7 | Jenelten et al. 2024 |
| 334 | Model-based and learned legged control: comparing and combining | Model-based vs learned legged control: what each does well; Combining control and learning: learn controller parameters, learn a high-level policy over MPC/WBC, use MPC to guide RL; Learning inside a model-based controller (learned corrections to MPC); Learned high-level policy over a model-based low level (choose footholds or gait, MPC executes); Model-based vs learning-based control: when each wins | 333, 325, 327, 221 | ME-105, ME-106, RS-052, RS-053, RS-084 | Ha §6; Gu IX-A; Ha 6.1–6.4; Gu VII-D; Ha §6.1; Ha §6.2; Gu hum §IX-A |
| 335 | Biped walking with RL: gait clocks and periodic rewards | From quadrupeds to bipeds: gait clocks, periodic rewards, biped sim-to-real | 330, 320 | RS-054 | Ha §7; Tang §4.1.2 |
| 336 | Navigation on legged and wheeled-legged robots | learned navigation over a locomotion policy; end-to-end locomotion + local navigation; skill hierarchies for agile navigation (parkour); hierarchical RL for wheeled-legged urban missions; Wheeled-legged robots | 332, 169, 193, 175 | N.22, L.6, N.23, RS-058 | Hoeller et al. 2021; Rudin et al. 2022b; Hoeller et al. 2024; Lee et al. 2024; Ha §8.5 |
| 337 | Loco-manipulation: walking and using arms together | Loco-manipulation: walk and use arms (or a leg) together; Loco-manipulation in WBC: the held object as an external wrench | 336, 327, 305 | RS-059, ME-076 | Ha §8.6; Gu hum §VII-F; Gu VI-D1 |
| 338 | Unsupervised skill discovery | Unsupervised skill discovery: learn many distinct skills with no task reward (DIAYN) | 193, 330, new Maths Note: Mutual information | RS-019 | Ha §8.1; Tang §5 |
| 339 | Differentiable simulators | Differentiable simulators: gradients through physics | 137, 118, 301 | RS-055 | Ha §8.2 |

#### RL-14 Humanoids: learning motion from humans

Human motion data and retargeting, adversarial and tracking imitation, teleoperation, multi-skill controllers.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 340 | Human motion data and kinematic retargeting | Human motion data: motion capture, video, body models (SMPL); Kinematic retargeting: scale, map joints, solve IK to match key points under joint limits; Motion retargeting: map human mocap onto a robot skeleton; Human pose estimation: body keypoints from images | 298, 182 | ME-108, ME-109, RS-080, idx:human_pose | Gu VII-C1; Loper et al. 2015; Gleicher 1998; Gu VII-C3; Gu hum §VII-C; Wikipedia (glossary/outline pages) |
| 341 | Adversarial imitation: GAIL | Adversarial imitation (GAIL): a discriminator gives the reward | 198, new Deep Learning Note: Generative adversarial networks | RS-067 | Zare §IV |
| 342 | Motion imitation and adversarial motion priors | motion imitation reward with reference-state starts; discriminator style reward (AMP) plus task reward; Imitation for locomotion (animal or human motion) | 154, 157, DL-003, 341 | H.1, H.2, R2.14, RS-051 | Peng et al. 2018 (DeepMimic); Peng et al. 2021 (AMP); Escontrela et al. 2022; Ha §2.3 |
| 343 | Whole-body tracking from human data | retargeting, sim-to-data filtering, RL tracker with privileged imitation; imitation for high-level skills; split-body objectives: upper body imitates, legs follow a velocity; general tracking policy composed by a diffusion model at test time; Filtering retargeted motions that the robot cannot follow; Imitation from human motion data | 342, 175, 69, new Deep Learning Note: Diffusion models, 340 | H.5, H.6, H.9, ME-110, RS-079 | He et al. 2024 (H2O, OmniH2O); Fu et al. 2024 (HumanPlus); Cheng et al. 2024 (Exbody); Liao et al. 2025 (BeyondMimic); He et al. 2024 (H2O); Gu hum §VII-C |
| 344 | Teleoperating humanoids: live retargeting with differential IK | Teleoperation of humanoids: live retargeting with differential IK; Imitation from robot teleoperation data | 298, 340, 343 | ME-111, RS-081 | Darvish et al. 2023; Gu hum §VII-B |
| 345 | Multi-skill humanoid controllers and behaviour foundation models | separate skills distilled into one agent, then self-play (soccer); masked full-body commands distilled into one policy; RL from scratch for humanoid skills; Behaviour foundation models: one controller for any motion or goal, prompted at run time | 343, 175 | H.4, H.7, RS-078, RS-087 | Haarnoja et al. 2024; He et al. 2025 (HOVER); Gu hum §VII-A; Yuan §III |

#### RL-15 Manipulation with learning

Visuomotor policies, grasping at scale, residual RL, action spaces, contact-rich tasks, dexterity, mobile manipulation.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 346 | End-to-end visuomotor policies | camera pixels to torques by guided policy search | 141, 118, DL-040 | M.1 | Levine et al. 2016 |
| 347 | Grasping from large real datasets | supervised grasp-success prediction with continuous servoing; closed-loop off-policy Q-learning from logged real data (QT-Opt); cross-entropy method to maximise Q; Grasping at scale with RL | 346, 36 | M.2, M.3, M.4, RS-075 | Levine et al. 2018; Kalashnikov et al. 2018; Ibarz §3.2; Tang §4.3.1 |
| 348 | Residual RL | learned correction on top of a hand-designed controller; Residual RL on a base controller; goal relabelling for sparse rewards | 141, 120 | M.6, RS-076 | Johannink et al. 2019; Silver et al. 2018; Tang §4.3, §5 |
| 349 | Manipulation action spaces: joints, end-effector deltas and impedance targets | Manipulation action spaces: joint, end-effector delta pose, impedance; Impedance targets as an RL action space | 143, 298, 307 | RS-062, ME-068 | Ravichandar §3.1.2; Kroemer §6.1; Martín-Martín et al. 2019 |
| 350 | Contact-rich manipulation: insertion and assembly | Contact-rich manipulation: insertion and assembly with force and impedance control; Jamming and wedging in peg-in-hole | 349, 306 | RS-022, idx:jamming_wedging | Tang §4.3.2; Lynch & Park, Modern Robotics (book + lectures) |
| 351 | Articulated, deformable and non-prehensile objects | Object types: articulated (doors, drawers), deformable (cloth), non-prehensile (pushing) | 350, 313 | RS-023 | Tang §4.3.2-4.3.4 |
| 354 | Dexterous in-hand manipulation | multi-finger hand in sim with heavy randomisation and an LSTM policy; RMA-style adaptation to object size, shape and weight; In-hand dexterity | 158, 178, 176 | M.7, M.8, RS-074 | OpenAI et al. 2018; OpenAI et al. 2019; Handa et al. 2023; Qi et al. 2022; Tang §4.3.3 |
| 355 | Vision-based dexterity | full-state RL teacher, point-cloud student; point-cloud input, imagined hand points, contact-based reward; bimanual sim-to-real recipe with automatic real-to-sim tuning | 354, 175, 154, 148 | M.9, M.10, M.12 | Chen et al. 2023; Qin et al. 2022 (DexPoint); Lin et al. 2025 |
| 356 | Predicting object motion: learned models for manipulation | Learned transition models for manipulation (predict object motion) | 50, 351 | RS-073 | Kroemer §5 |
| 357 | Mobile manipulation | Mobile manipulation: one Jacobian for base and arm together; Mobile manipulation; Mobile manipulation: arm on a moving base; whole-body control by RL | 295, 140, 327 | ME-112, CT-112, RS-015 | MR 13.5; Tang §4.4 |

#### RL-16 Imitation learning for manipulation

Where demonstrations come from and the policies that learn from them: diffusion policy, action chunking, demos inside RL, human feedback.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 358 | Collecting demonstrations: teleoperation and kinesthetic teaching | Collecting demonstrations: kinesthetic teaching, teleoperation (VR, leader-follower arms), passive observation; Haptic (force-feedback) teleoperation | 174, 344 | RS-060, idx:haptic_teleop | Ravichandar §2; Wikipedia (glossary/outline pages) |
| 359 | Movement primitives and Gaussian mixture regression | Movement primitives: a trajectory as a spring-damper system plus a learned shape (DMP, ProMP); Gaussian mixture regression as a policy | 43, 121, 174, MA-073 | RS-004, RS-070 | Kober §4.3; Ravichandar §3.1.3 |
| 360 | Demonstrations from human videos | hand and object poses from video turned into robot demos; Imitation from observation: learn from state-only or video demos; Embodiment gap: human hand vs robot gripper, retargeting | 174 | M.11, RS-068, RS-069 | Qin et al. 2022 (DexMV); Zare §V; Zare §VI-B; Kawaharazuka §II-B |
| 361 | Diffusion policy and multimodal demonstrations | Why plain BC fails on multimodal demos (averaging two good paths gives a bad one); Diffusion policy: denoise a short action sequence step by step; I1 Diffusion policy: a policy that generates a short action sequence by denoising; handles multi-modal demonstrations | 358, new Deep Learning Note: Diffusion models | RS-063, RS-064, AU-037 | Wolf §2.3, §4.1.1; Wolf §4.1.1; Ma §III-B; Chi et al. 2023, *Diffusion Policy* ([arXiv 2303.04137](https://arxiv.org/abs/2303.04137)); M832 ch.21; COR "Generative models" |
| 362 | Action chunking (ACT) | Action chunking (ACT): predict k actions at once, blend overlapping chunks; I2 Action chunking (ACT), temporal ensembling and low-cost teleoperation for collecting demonstrations | 361, DL-087, new Deep Learning Note: Variational autoencoder | RS-065, AU-038 | Kawaharazuka §IV-A; Ma §III-B; Zhao et al. 2023, ACT / ALOHA ([arXiv 2304.13705](https://arxiv.org/abs/2304.13705)) |
| 363 | Learning task structure from demonstrations | Learning task structure: segment demos into skills, pre- and postconditions | 358, 193 | RS-071 | Ravichandar §3.3; Kroemer §7-8 |
| 364 | Human feedback and shared autonomy for robots | I5 Human feedback for robots and shared autonomy; Human-robot interaction: shared autonomy and physical HRI | 358, 206 | AU-041, RS-016 | S237B wk 8–9 "Learning from human feedback", "Shared autonomy"; Tang §4.5 |
| 365 | Manipulation benchmarks and datasets | Manipulation benchmarks and datasets: robosuite, RLBench, Meta-World, CALVIN, LIBERO, robomimic | 361, 44 | RS-077 | Wolf §5; Ma §V |

#### RL-17 Offline RL and RL from demonstrations

Learning a policy from logged data and demos, then improving it on the robot

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 366 | Offline RL and distribution shift | offline setting, distribution shift, out-of-distribution actions | 347, 174 | E.12 | Levine et al. 2020 |
| 367 | Conservative Q-learning | push down Q on unseen actions | 366 | E.13 | Kumar et al. 2020 |
| 368 | Offline pretraining, then online fine-tuning | Offline pretraining, then online fine-tuning | 367, 149 | RS-020 | Tang §5 |
| 369 | RL as sequence modelling: Decision Transformer | tokens are (return-to-go, state, action) | 366, DL-087 | E.14 | Chen et al. 2021 |
| 370 | Bootstrapping RL with demonstrations | Bootstrapping RL with demonstrations: demos in the replay buffer, BC term in the loss | 358, 42 | RS-007 | Ibarz §4.4 |
| 371 | Real-world RL with human corrections | sample-efficient off-policy real-robot RL: reward classifier, resets, demos; human corrections during real-world RL | 149, 42 | E.22, E.23 | Luo et al. 2024 (SERL); Luo et al. 2024 (HIL-SERL) |

#### RL-18 Robot foundation models

Learning from fixed data and pretrained models: offline RL, VLAs, action heads, cross-robot data, language planning, real-world fine-tuning.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 372 | Vision-language-action models and generalist robot policies | robot actions as text tokens; co-fine-tuning; fine-tuning an open VLA for a new robot; generalist VLA for real robots (mostly imitation); open foundation model for humanoids (mostly imitation); Robot transformers and VLAs; Humanoid foundation models | 174, DL-071, DL-053 | E.15, E.16, E.20, E.21, RS-106, RS-088 | Brohan et al. 2023 (RT-2); Kim et al. 2024 (OpenVLA); Gemini Robotics Team 2025; NVIDIA 2025 (GR00T N1); Firoozi §III-A, §III-E; Ma §III; Gu hum §VIII |
| 373 | Action heads: tokens, diffusion and flow | Action heads: discrete action tokens vs diffusion/flow heads | 372 | RS-107 | Kawaharazuka §IV-A |
| 374 | Cross-embodiment datasets and generalist policies | Cross-embodiment datasets (Open X-Embodiment, DROID, BridgeData) and training across robots; I4 Large cross-robot demonstration datasets and generalist BC policies | 372, 362 | RS-108, AU-040 | Kawaharazuka §VI; Ma §V-A; Open X-Embodiment ([arXiv 2310.08864](https://arxiv.org/abs/2310.08864)); Octo ([arXiv 2405.12213](https://arxiv.org/abs/2405.12213)) |
| 375 | Flow-matching action experts | action chunks from a flow-matching expert; co-training on varied data for open-world homes | 372, new Deep Learning Note: Flow matching | E.17, E.18 | Black et al. 2024 (pi0); Physical Intelligence 2025 (pi0.5) |
| 376 | Pretrained visual representations for control | Pretrained visual representations for robots (from human video, goal-conditioned values) | 252, 346 | RS-110 | Firoozi §III-B |
| 377 | Language models as task planners | LLM task planning: monolithic vs modular (affordance-scored plans, code as policies) | 372, 315, 252 | RS-111 | Firoozi §III-C; Ma §IV |
| 378 | Affordance models: where and how to act | Affordance-based models: where and how to act on an object | 377 | RS-113 | Firoozi §IV-D; Kawaharazuka §IV-C |
| 379 | Video and world models as policies | Video and world models as policies (predict the future frame, then act) | 50, 372, new Deep Learning Note: Diffusion models | RS-114 | Firoozi §IV-E; Kawaharazuka §IV-B |
| 380 | Hierarchical VLAs: slow planner, fast controller | Hierarchical VLA: slow planner + fast controller | 375, 377 | RS-116 | Ma §IV; Kawaharazuka §V-D |
| 381 | RL fine-tuning of a VLA | advantage-conditioned RL fine-tuning with human corrections; RL fine-tuning of generalist policies | 375, 371, 34 | E.19, RS-117 | Physical Intelligence 2025 (pi*0.6 / RECAP); Kawaharazuka §V-C, §IX-D |
| 382 | Uncertainty and asking for help | Uncertainty and asking for help (conformal prediction) | 372 | RS-119 | Firoozi §VI-D |

## Robotics (RO)


### Robotics / Perception


#### RO-01 Robot sensors: IMU, GNSS, cameras, depth and LiDAR

What each sensor measures and how it errs, the first fusion filters, and turning depth and LiDAR into aligned point clouds.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 83 | Sensor basics and simple sensors: specifications, contact and proximity sensors | Sensor terms: active/passive, range, resolution, accuracy vs precision, bandwidth, systematic vs random error; Decibels; Proximity and contact sensors: bumpers, infrared, ultrasonic (sonar) | 63, MA-061 | idx:sensor_terms, idx:decibels, idx:proximity_sensors | CMU 16-761; Correll et al., Intro to Autonomous Robots; ETH AMR; LaValle, Planning Algorithms; Wikipedia (glossary/outline pages) |
| 84 | Inertial sensors: gyroscope, accelerometer and their errors | Gyroscope: measures turn rate; Accelerometer: measures specific force (gravity included); IMU measurement model: reading = truth + bias + noise; Bias random walk and bias estimation; Integration drift: angle error grows with t, position error with t³ for a gyro bias; Magnetometer (compass) for heading | 63, new Maths Note: 3D rotations: Euler angles and quaternions, MA-024, new Maths Note: Random processes: white noise, random walks and noise density | PE-081, PE-082, PE-083, PE-084, PE-085, idx:magnetometer | RVC3 3.4.1; Woodman 2007 ([UCAM-CL-TR-696](https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-696.html)); RVC3 3.4; Woodman 2007; Huang §2.1; Woodman 2007 gyro/accel errors; Barfoot 5.2; LaValle, Planning Algorithms |
| 85 | Integrating rotation rates and strapdown inertial navigation | Integrating angular velocity into orientation; Strapdown inertial navigation; Angular velocity as a vector along the spin axis | 84, new Maths Note: Axis-angle, exponential and log maps of rotations, new Maths Note: Numerical integration of ODEs, new Maths Note: Cross product and skew-symmetric matrix | PE-086, PE-088, ME-005 | RVC3 3.4.1.2; Barfoot 7.2.4; Barfoot 9.4; Woodman 2007 strapdown; MR 3.2.2 |
| 86 | Satellite positioning: GNSS and RTK | GNSS/GPS basics: ranging to satellites, ~5 m phone accuracy, multipath and blockage; C1 GNSS: how a position is fixed from satellites, error sources, RTK, latitude/longitude to a local metric frame (ENU/UTM) | 65 | PE-090, AU-015 | Lee §6; [GPS.gov accuracy page](https://archive.gps.gov/systems/gps/performance/accuracy/); TOR C2 M3; CMU wk 7–8 "satellite navigation"; ETH wk 4 GPS; AW localization (GNSS, RTK); NAV2 GPS tutorial |
| 87 | Fusing IMU, wheels and GNSS: complementary filter and EKF | Complementary filter for attitude; EKF fusion of IMU, wheels and GNSS (loosely coupled); Loose vs tight coupling; Wheel odometry from encoders, and wheel slip; Encoders: incremental (quadrature) and absolute | 85, 86, 81, 68 | PE-094, PE-095, PE-096, PE-089, idx:encoders | RVC3 3.4.4; Mahony et al. 2008 [doi:10.1109/TAC.2008.923738](https://doi.org/10.1109/TAC.2008.923738); Huang §2.1, §3.1; Huang §3.2; RVC3 6.1; Thrun ch.5 via RO 51; Correll et al., Intro to Autonomous Robots |
| 88 | Error-state Kalman filter for orientation | Error-state (indirect) Kalman filter for rotations | 87, new Maths Note: Axis-angle, exponential and log maps of rotations | PE-097 | Barfoot 7.2.5, 8.3 |
| 89 | The pinhole camera: projection, intrinsics and extrinsics | Pinhole camera: a 3D point maps to a pixel through a small hole; Homogeneous coordinates for points in an image and in 3D; Camera matrix P = K [R \| t]; Intrinsics K: focal length, principal point, pixel size; Extrinsics: camera pose in the world; Pinhole terms: optical axis and centre, image plane, normalised coordinates, field of view, skew; Points and lines in homogeneous coordinates: cross products, points/line at infinity, vanishing points | 65, new Maths Note: Cross product and skew-symmetric matrix | PE-001, PE-002, PE-003, PE-004, PE-005, idx:pinhole_terms, idx:homogeneous_lines | VO-I camera modelling; HZ 6.1; RVC3 13.1; HZ 2.2, 3.1; RVC3 13.1.4; Barfoot 7.4.1; RVC3 13.1.3; RVC3 13.1.2; Barfoot, State Estimation for Robotics; Prince, Computer Vision: Models, Learning, Inference; Szeliski, Computer Vision |
| 90 | Camera hardware: lenses, exposure and image sensors | Camera hardware: lens law, focus, aperture, depth of field, exposure, global vs rolling shutter, CCD/CMOS, noise, Bayer filter, dynamic range | 89 | idx:camera_sensing | CMU 16-385 Computer Vision; Nayar, First Principles of CV; Stachniss lectures (Bonn); Szeliski, Computer Vision; Wikipedia (glossary/outline pages) |
| 91 | Lens distortion, wide-angle cameras and camera calibration | Lens distortion: radial and tangential; Camera calibration with a checkerboard; Direct linear transform (DLT): estimate a matrix from point pairs; Solving A x = 0 with the SVD (last right singular vector); Wide-angle cameras: fisheye and spherical models; Fiducial markers (AprilTag-style); Bilinear and multilinear interpolation on a grid; Image warping and resampling: forward vs inverse warping, nearest/bilinear/bicubic | 89, MA-058, ML-053, ML-043 | PE-006, PE-007, PE-008, PE-009, PE-010, PE-011, idx:grid_interpolation, idx:image_warping | HZ 7.4; RVC3 13.1.6; VO-I calibration; RVC3 13.2.2; Zhang 2000 [doi:10.1109/34.888718](https://doi.org/10.1109/34.888718); HZ 4.1, 7.1; HZ 4.1; MA-058 §6; VO-I omnidirectional; RVC3 13.3; RVC3 13.6.1; Kochenderfer et al., Algorithms for Decision Making; Nayar, First Principles of CV; Stachniss lectures (Bonn); Szeliski, Computer Vision |
| 92 | Depth from stereo and depth cameras | Stereo camera model: disparity and depth; Dense stereo matching along rows; Stereo failure modes and depth error growing with distance; Depth cameras: structured light and time of flight; Image rectification; Stereo matching costs: SSD, SAD, NCC, cost volume, scanline DP, semi-global matching | 89 | PE-060, PE-061, PE-062, PE-063, PE-044, idx:stereo_matching | Barfoot 7.4.2; RVC3 14.4; Szeliski ch.12; RVC3 14.4.2; Szeliski ch.13; Newcombe et al. 2011 [doi:10.1109/ISMAR.2011.6092378](https://doi.org/10.1109/ISMAR.2011.6092378); HZ 11.12; RVC3 14.4.3; Prince, Computer Vision: Models, Learning, Inference; Szeliski, Computer Vision |
| 93 | Point clouds from depth images and LiDAR | Depth image to point cloud; How LiDAR works: time of flight, spinning vs solid-state, rings; Range-azimuth-elevation sensor model; Point clouds: storage and basic operations; Voxel-grid downsampling; other range sensors: radar (range and Doppler) and event cameras, named; Range measurement: time of flight vs phase shift | 92, 74 | PE-064, PE-066, PE-067, PE-068, PE-069, idx:tof_phase | RVC3 14.7; Lee §2; RVC3 6.8; Barfoot 7.4.3; RO 57; Cadena §V; Rusu & Cousins 2011 [doi:10.1109/ICRA.2011.5980567](https://doi.org/10.1109/ICRA.2011.5980567); Rusu & Cousins 2011; Correll et al., Intro to Autonomous Robots |
| 94 | Aligning scans: normals, k-d trees and ICP | Normals and plane fitting (incl. ground removal); k-d tree for nearest-neighbour search; ICP: iterative closest point; Point-to-plane ICP and Generalized-ICP; Aligning two 3D point sets (SVD / Kabsch solution); Line extraction from 2D scans and points: split-and-merge, line fitting | 93, 75, MA-060, ML-085 | PE-070, PE-071, PE-072, PE-073, PE-043, idx:line_extraction | RVC3 14.7.1; Lee §3.1; Besl & McKay 1992 [doi:10.1109/34.121791](https://doi.org/10.1109/34.121791); Barfoot 9.1; Chen & Medioni 1992 [doi:10.1016/0262-8856(92)90066-C](https://doi.org/10.1016/0262-8856(92)90066-C); Segal et al. 2009 [doi:10.15607/RSS.2009.V.021](https://doi.org/10.15607/RSS.2009.V.021); VO-I 3D-to-3D; RVC3 14.7.2; Correll et al., Intro to Autonomous Robots; ETH AMR; Szeliski, Computer Vision |
| 95 | Extrinsic and time calibration between sensors | Extrinsic and time calibration between sensors (camera-IMU, camera-LiDAR); H1 Extrinsic calibration: camera–LiDAR, camera–IMU, hand–eye; time offsets between sensors | 91, 93, 84 | PE-015, AU-034 | Furgale et al. 2013 [doi:10.1109/IROS.2013.6696514](https://doi.org/10.1109/IROS.2013.6696514); Huang §4; UDS C2 "Sensor and camera calibration"; Tsai & Lenz 1989, *hand/eye calibration* ([10.1109/70.34770](https://doi.org/10.1109/70.34770)); Kalibr ([repo](https://github.com/ethz-asl/kalibr)) |

#### RO-02 Objects, people and grasps: detection, segmentation, tracking, pose and touch



| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 182 | Object detection: boxes, IoU, non-max suppression and mAP | Object detection: boxes and class labels; Intersection over union (IoU) and mean average precision (mAP); Non-maximum suppression; Using pretrained detectors and segmenters; D1 2D object detection: boxes, scores, non-max suppression, mAP; traffic-light recognition as a detection task | DL-040, DL-051, ML-076, 89 | PE-109, PE-110, PE-111, PE-118, AU-017 | Zou §II.A road map; RVC3 12.1.4; Zou §II.B; Zou §II.C; DL-053; TOR C3; UDS C2; M42 ch.9; S237B wk 4; AW object recognition / traffic lights; Redmon et al. 2016 YOLO ([arXiv 1506.02640](https://arxiv.org/abs/1506.02640)) |
| 183 | Detector families: two-stage and one-stage | Two-stage detectors (Faster R-CNN); One-stage detectors (YOLO, SSD) | 182 | PE-112, PE-113 | Zou §II.A; Ren et al. 2015 [arXiv:1506.01497](https://arxiv.org/abs/1506.01497); Redmon et al. 2016 [arXiv:1506.02640](https://arxiv.org/abs/1506.02640); Liu et al. 2016 SSD [arXiv:1512.02325](https://arxiv.org/abs/1512.02325) |
| 184 | Semantic segmentation | Semantic segmentation: a class per pixel (FCN); Encoder-decoder segmentation (U-Net); D2 Semantic segmentation; road and lane detection as segmentation | 182, DL-042 | PE-114, PE-115, AU-018 | Minaee §3; Long et al. 2015 [arXiv:1411.4038](https://arxiv.org/abs/1411.4038); RVC3 12.1.1; Minaee §3.3; Ronneberger et al. 2015 [arXiv:1505.04597](https://arxiv.org/abs/1505.04597); TOR C3 (drivable surface); UDS C12; M42 ch.9; NAV2 semantic-segmentation layer; Long et al. 2015 FCN ([arXiv 1411.4038](https://arxiv.org/abs/1411.4038)) |
| 185 | Obstacles in point clouds: ground removal, clustering and 3D boxes | D4 Point-cloud obstacles: ground removal, clustering, 3D boxes from LiDAR | 93, 182 | AU-020 | UDS C3, C11 (PCL); AW obstacle segmentation, radar; NAV2 ground-consistency layer; Lang et al. 2019 PointPillars ([arXiv 1812.05784](https://arxiv.org/abs/1812.05784)) |
| 186 | Semantic maps and traversability costs | Semantic maps: putting labels into the 3D map; Traversability from geometry and semantics; Terrain-aware and off-road navigation: learn traversability from experience | 184, 99, 100 | PE-116, PE-117, RS-031 | Cadena §VI; Chen §4.2; Fankhauser 2018; Xiao §4.2.1; Tang §4.2.1 |
| 187 | Multi-object tracking | D3 Multi-object tracking: one Kalman filter per object, association, track birth and death; Data association and Mahalanobis gating | 182, 80, new Maths Note: Mahalanobis distance, new Maths Note: Assignment problem (Hungarian algorithm) | AU-019, PE-106 | UDS C3 multi-target tracking; TOR C3; S3 "moving obstacles tracking"; AW; Bewley et al. 2016 SORT ([arXiv 1602.00763](https://arxiv.org/abs/1602.00763)); Weng et al. 2020 AB3DMOT ([arXiv 1907.03961](https://arxiv.org/abs/1907.03961)); RO 161 |
| 188 | Predicting where people and vehicles go, and collision checks in time | E1 Motion prediction: constant velocity, manoeuvre-based, learned multi-modal forecasts; ADE/FDE; Human trajectory prediction for planning: constant velocity, social force model, learned predictors; E2 Collision checks against moving obstacles; time to collision; risk assessment and driving style named | 187, 110, DL-064 | AU-022, RS-033, AU-023 | TOR C4 M5; UDS C9; AW object recognition "predicts trajectories"; Rudenko et al. 2020 ([arXiv 1905.06113](https://arxiv.org/abs/1905.06113)); Salzmann et al. 2020 Trajectron++ ([arXiv 2001.03093](https://arxiv.org/abs/2001.03093)); Shi et al. 2022 MTR ([arXiv 2209.13508](https://arxiv.org/abs/2209.13508)); Mavrogiannis §3.1; TOR C4 M5 "time to collision" |
| 316 | Tactile sensing | K5 Tactile sensing; Tactile sensing on hands, feet and body | 308 | AU-050, RS-085 | M42 ch.12; Gu hum §III |
| 352 | 6-DoF grasp poses from point clouds | 6-DoF grasp pose prediction from point clouds | 312, 347, 93 | RS-072 | Tang §4.3.1.1; Wolf §4.2 |
| 353 | Learned object pose and keypoints | D5 Learned object pose and keypoints for manipulation | 182, 247 | AU-021 | M42 ch.10 (pose estimation, keypoints, dense correspondence); COR "3D visual representations" |

#### RO-03 Vision for motion: features, optical flow and visual odometry

How a camera alone measures motion: calibration between sensors, features, matching, optical flow, two-view geometry, VO and bundle adjustment.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 237 | Pixels, point operators and colour spaces | Pixels and point operators: histogram, brightness/contrast, gamma, histogram equalisation (CLAHE), blending; Colour spaces: RGB, HSV, Lab, YUV; luminance and chromaticity | 89, ML-019, DL-042 | idx:point_ops, idx:colour_spaces | Nayar, First Principles of CV; Prince, Computer Vision: Models, Learning, Inference; Stachniss lectures (Bonn); Szeliski, Computer Vision; Wikipedia (glossary/outline pages) |
| 238 | Binary images: thresholds, morphology and blobs | Binary images: thresholding, morphology, connected components, blob moments | 237, new Maths Note: Graphs and their matrices: adjacency, degree, paths and connectivity, MA-028 | idx:binary_images | Correll et al., Intro to Autonomous Robots; Nayar, First Principles of CV; Stachniss lectures (Bonn); Szeliski, Computer Vision; Wikipedia (glossary/outline pages) |
| 239 | Image gradients, pyramids and corner features | Image filtering: smoothing and gradient filters; Image pyramids (coarse-to-fine); Point features (keypoints): why corners are easy to find again; Harris and Shi-Tomasi corners and the structure tensor; FAST corner detector; Separable filters; Nonlinear image filters: median, bilateral | 89, DL-042, MA-056 | PE-013, PE-014, PE-016, PE-017, PE-018, idx:separable_filters, idx:nonlinear_filters | RVC3 11.5.1; DL-042 §6; RVC3 11.7.3; Baker 2.3.4; VO-II feature detection; RVC3 12.3; VO-II; Harris & Stephens 1988 [doi:10.5244/C.2.23](https://doi.org/10.5244/C.2.23); Rosten et al. 2010 [doi:10.1109/TPAMI.2008.275](https://doi.org/10.1109/TPAMI.2008.275); Szeliski, Computer Vision; Nayar, First Principles of CV; Prince, Computer Vision: Models, Learning, Inference |
| 240 | Edges: Canny, the image Laplacian and Laplacian of Gaussian | Edge detection: gradient magnitude, non-maximum suppression, hysteresis, Canny; Image Laplacian, Laplacian of Gaussian, difference of Gaussians, zero crossings, Laplacian pyramid | 239, new Maths Note: The Laplacian and Laplace's equation | idx:canny, idx:image_laplacian | Correll et al., Intro to Autonomous Robots; ETH AMR; Nayar, First Principles of CV; Prince, Computer Vision: Models, Learning, Inference; Szeliski, Computer Vision; Wikipedia (glossary/outline pages) |
| 241 | Descriptors and matching: SIFT and ORB | Scale-space blobs, descriptors and SIFT; ORB: binary descriptors and Hamming distance; Matching descriptors (nearest neighbour, ratio test, mutual check) vs tracking; Template matching by (normalised) cross-correlation | 239, ML-085, DL-042, 92 | PE-019, PE-020, PE-021, idx:template_matching | VO-II; RVC3 12.3.2; Lowe 2004 [doi:10.1023/B:VISI.0000029664.99615.94](https://doi.org/10.1023/B:VISI.0000029664.99615.94); Rublee et al. 2011 [doi:10.1109/ICCV.2011.6126544](https://doi.org/10.1109/ICCV.2011.6126544); VO-II feature matching; ML-085; Nayar, First Principles of CV; Stachniss lectures (Bonn) |
| 242 | RANSAC and homographies | RANSAC: fit a model despite wrong matches; Homography: the map between two views of a plane; 2D transform hierarchy: translation, Euclidean, similarity, affine, projective; Hough transform for lines and circles | 241, 91, MA-031, MA-053 | PE-022, PE-023, idx:transform_hierarchy, idx:hough | VO-II outlier removal; Fischler & Bolles 1981 [doi:10.1145/358669.358692](https://doi.org/10.1145/358669.358692); Barfoot 5.4.1; HZ 4.1, 4.8, 13; RVC3 13.6.2; CMU 16-385 Computer Vision; Prince, Computer Vision: Models, Learning, Inference; Szeliski, Computer Vision; Wikipedia (glossary/outline pages); Correll et al., Intro to Autonomous Robots; ETH AMR; Nayar, First Principles of CV |
| 243 | Optical flow: brightness constancy, Lucas-Kanade and KLT | Optical flow: the apparent motion of each pixel; Brightness constancy and the optical-flow constraint; Lucas-Kanade: local flow by least squares in a window; Pyramidal KLT tracker; Aperture problem and normal flow; Light and surfaces: radiance, irradiance, Lambertian vs specular, BRDF named | 239, ML-053 | PE-024, PE-025, PE-026, PE-027, idx:aperture_problem, idx:light_surfaces | Szeliski ch.9; Baker 2.1.1; Horn & Schunck 1981 [doi:10.1016/0004-3702(81)90024-2](https://doi.org/10.1016/0004-3702(81)90024-2); Lucas & Kanade 1981 ([IJCAI PDF](https://www.ijcai.org/Proceedings/81-2/Papers/017.pdf)); ML-053; Baker 2.3.4; Shi & Tomasi 1994; Szeliski, Computer Vision; Nayar, First Principles of CV |
| 244 | Dense and learned flow, and ego-motion from flow | Horn-Schunck: dense flow with a smoothness term; Learned optical flow; Image motion from camera motion (the image Jacobian); Ego-motion and time-to-contact from flow | 243, DL-040 | PE-028, PE-029, PE-030, PE-031 | Horn & Schunck 1981; Baker 2.2; Chen §3.1; Teed & Deng 2020, RAFT [arXiv:2003.12039](https://arxiv.org/abs/2003.12039); RVC3 15.2.1; Szeliski ch.9; RVC3 15.2.3 |
| 245 | Visual servoing | Visual servoing: IBVS, PBVS, interaction matrix in a control law | 244, 120 | idx:visual_servoing | CMU 16-761; Stanford CS223A / ME320 Introduction to Robotics |
| 246 | Epipolar geometry: essential and fundamental matrices | Epipolar geometry: epipoles, epipolar lines; Essential matrix E (calibrated cameras); Fundamental matrix F (uncalibrated cameras); Normalised 8-point algorithm; 5-point algorithm (concept only) | 242, new Maths Note: Cross product and skew-symmetric matrix, MA-058 | PE-032, PE-034, PE-035, PE-036, PE-037 | HZ 9.1; RVC3 14.2; HZ 9.6; RVC3 14.2.2; HZ 9.2; RVC3 14.2.1; HZ 11.2; RVC3 14.2.3; VO-I 2D-to-2D; Nistér 2004 [doi:10.1109/TPAMI.2004.17](https://doi.org/10.1109/TPAMI.2004.17) |
| 247 | Relative pose, triangulation and PnP | Recovering R and t from E; the four-solution check; Scale ambiguity of a single camera; Triangulation; PnP: camera pose from known 3D points (EPnP); Reprojection error | 246 | PE-038, PE-039, PE-040, PE-041, PE-042 | HZ 9.6.2; VO-I; VO-I monocular; HZ 12.2; RVC3 14.3.1; VO-I triangulation; VO-I 3D-to-2D; RVC3 13.2.4; Lepetit et al. 2009 [doi:10.1007/s11263-008-0152-6](https://doi.org/10.1007/s11263-008-0152-6); HZ 4.2-4.3, 12.3 |
| 248 | Visual odometry: mono and stereo, feature-based and direct | Visual odometry: chaining frame-to-frame motions; Drift: why odometry error grows; Monocular vs stereo VO; Direct vs feature-based (indirect) methods: photometric error; Learned odometry (visual, inertial) and learned SLAM parts; Learned depth from one image (concept); Depth from one image with a network: scale ambiguity, relative vs metric depth, foundation depth models; learned stereo | 247, 243, 92, 68 | PE-045, PE-046, PE-047, PE-048, PE-059, PE-065, idx:mono_depth_nets | VO-I formulation; VO-I; RO 51; VO-I mono vs stereo; VO-II dense methods; Huang §3.4; Engel et al. 2018 DSO [doi:10.1109/TPAMI.2017.2658577](https://doi.org/10.1109/TPAMI.2017.2658577); Chen §3, §6; Chen §4.1; Eigen et al. 2014 [arXiv:1406.2283](https://arxiv.org/abs/1406.2283); Stanford CS231A Computer Vision |
| 249 | Structure from motion and bundle adjustment | Structure from motion: cameras and points from many photos; Bundle adjustment; Sparsity and the Schur complement in bundle adjustment; Levenberg-Marquardt; Robust cost functions (Huber, Cauchy) | 248, new Maths Note: Nonlinear least squares (Gauss-Newton), new Maths Note: Schur complement | PE-049, PE-050, PE-051, PE-052, PE-053 | VO-I/II; Szeliski ch.11; RVC3 14.3; HZ 18.1; Barfoot 10.1; VO-II windowed BA; RO 165; HZ 4.5; Barfoot 4.3; Barfoot 5.4; Cadena §III |
| 250 | Visual SLAM: place recognition and ORB-SLAM | VO vs visual SLAM; front-end vs back-end; Visual place recognition with bag of words; ORB-SLAM as a worked system: tracking, local mapping, loop closing threads; Bag-of-words retrieval: TF-IDF, inverted index, vocabulary tree | 249, 102, 104, MA-048 | PE-054, PE-055, PE-057, idx:bow_tfidf | Cadena §II; VO-I VO vs V-SLAM; Gálvez-López & Tardós 2012 [doi:10.1109/TRO.2012.2197158](https://doi.org/10.1109/TRO.2012.2197158); VO-II loop constraints; RO 167; Mur-Artal et al. 2015 [doi:10.1109/TRO.2015.2463671](https://doi.org/10.1109/TRO.2015.2463671); Campos et al. 2021 ORB-SLAM3 [doi:10.1109/TRO.2021.3075644](https://doi.org/10.1109/TRO.2021.3075644); Szeliski, Computer Vision |
| 251 | Evaluating odometry and SLAM | Evaluating odometry and SLAM: trajectory error, drift %, benchmarks | 248, 170 | PE-058 | Cadena §III; Lee §8.2; Geiger et al. 2012 KITTI [doi:10.1109/CVPR.2012.6248074](https://doi.org/10.1109/CVPR.2012.6248074) |

### Robotics / Localization


#### RO-04 Uncertainty, motion models and Bayes filters



| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 63 | Why a robot is never sure: state, controls and measurements | sources of uncertainty in robots; keep a full distribution, not one best guess; state: pose, map, speeds; complete state; measurements and controls; uncertainty in actions vs in perception | ML-003, MA-020, MA-014 | PR 1.1, PR 1.2, PR 2.12, PR 2.13, PR 14.1 | Thrun et al. 2005 ch.1; Thrun et al. 2005 ch.2; Thrun et al. 2005 ch.14 |
| 68 | Probabilistic motion models: velocity and odometry | motion as a distribution p(x_t \| u_t, x_t-1); velocity motion model; odometry motion model; sampling next poses from a motion model; ruling out poses inside walls; Wheel odometry | 64, new Maths Note: Drawing samples from distributions, MA-024 | PR 5.3, PR 5.4, PR 5.5, PR 5.7, PR 5.8, CT-006 | Thrun et al. 2005 ch.5; MR 13.4 |
| 71 | Maps and landmarks | feature-based vs grid maps; obstacles as polygons built from half-planes; triangle meshes and bitmaps; feature extraction: landmarks with range, bearing, signature | MA-051, 63 | PR 6.1, PR 6.8, PA 3.1, PA 3.3 | Thrun et al. 2005 ch.6; LaValle 2006 ch.3 |
| 74 | Range sensors: the beam model | beam model: one reading as a mix of four error types; mixture density of different shapes; learning sensor-model parameters by MLE and EM; catalogue of sensor models (landmark, range, odometry, boundary) | 71, MA-071, MA-073, MA-074 | PR 6.2, PR 6.4, PR 6.5, PA 11.1 | Thrun et al. 2005 ch.6; LaValle 2006 ch.11 |
| 75 | Likelihood fields and scan matching | likelihood field model; correlation-based map matching | 74, MA-009 | PR 6.6, PR 6.7 | Thrun et al. 2005 ch.6 |
| 76 | Landmark measurement model | landmark sensor model with known correspondence; sampling poses from a landmark reading | 71, 68 | PR 6.9, PR 6.10 | Thrun et al. 2005 ch.6 |
| 77 | Belief: what the robot knows | state transition and measurement probabilities; hidden Markov model / dynamic Bayes network; belief and predicted belief; information state: the history of actions and readings; set-valued (nondeterministic) information state | new Maths Note: Markov chains, 68, 74, new Maths Note: Bayesian networks | PR 2.14, PR 2.15, PR 2.17, PA 11.2, PA 11.3 | Thrun et al. 2005 ch.2; LaValle 2006 ch.11 |
| 78 | The Bayes filter: predict, then update | Bayes' theorem conditioned on past data; Bayes filter predict and update steps; belief as the probabilistic information state | 77, MA-018, MA-019 | PR 2.7, PR 2.18, PA 11.4 | Thrun et al. 2005 ch.2; LaValle 2006 ch.11 |
| 79 | Grid filters: histogram filter and binary Bayes filter | histogram (discrete Bayes) filter; static and adaptive cell decomposition; binary Bayes filter in log-odds form; HMM inference: forward-backward smoothing and Viterbi | 78, ML-019, ML-031, ML-116, 77 | PR 4.2, PR 4.3, PR 4.5, idx:hmm_inference | Thrun et al. 2005 ch.4; Prince, Computer Vision: Models, Learning, Inference |
| 80 | Kalman filter | linear Gaussian system; Kalman filter and the Kalman gain; Kalman filter for the state that feedback needs; Kalman filter; Observability; Observability (concept only); Choosing and estimating Q and R | 78, MA-073, new Maths Note: Linear transforms of a Gaussian | PR 3.1, PR 3.6, PA 11.8, CT-110, PE-091, CT-032, PE-104, idx:noise_cov_estimation | Thrun et al. 2005 ch.3; LaValle 2006 ch.11; robotics.md (PR 3.1); RO 63; MPC 1.4.5; Huang §5; Barfoot, State Estimation for Robotics |
| 81 | Extended Kalman filter | pushing a Gaussian through a curved function by linearisation; extended Kalman filter (EKF); Extended Kalman filter; Filter honesty: innovation and its covariance, NEES and NIS tests | 80, MA-063, MA-064, MA-045, new Maths Note: Propagating uncertainty through a function | PR 3.7, PR 3.8, PE-092, idx:filter_consistency | Thrun et al. 2005 ch.3; RO 64; Barfoot, State Estimation for Robotics; Prince, Computer Vision: Models, Learning, Inference; Rawlings, Mayne & Diehl, MPC |
| 82 | Particle filter | resampling and the low-variance sampler; particle filter; particle deprivation; belief as a cloud of weighted samples | 78, new Maths Note: Monte Carlo estimation, new Maths Note: Importance sampling, ML-102 | PR 4.8, PR 4.9, PR 4.10, PA 11.10 | Thrun et al. 2005 ch.4; LaValle 2006 ch.11 |

#### RO-05 Localization and maps for navigation

Where am I on a known 2D or 3D map, what is around me, and the cost map every planner reads.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 96 | Markov localization on a known map | tracking, global and kidnapped-robot localization; Markov localization; discrete, geometric and Monte Carlo localization compared; grid localization (histogram filter over poses) | 78, 71, 79 | PR 7.1, PR 7.2, PA 12.2, PR 8.1 | Thrun et al. 2005 ch.7; LaValle 2006 ch.12; Thrun et al. 2005 ch.8 |
| 97 | Monte Carlo localization and adaptive particle counts | Monte Carlo localization (MCL); augmented MCL: random particles to recover when lost; rejecting readings the map cannot explain; better proposal distributions; chi-square quantile to set a sample size; KLD-sampling | 82, 75, new Maths Note: KL divergence, MA-045 | PR 8.2, PR 8.3, PR 8.8, PR 8.4, PR 8.6, PR 8.7 | Thrun et al. 2005 ch.8 |
| 98 | Occupancy grid mapping | occupancy grid map; inverse sensor model and log-odds cell update; fusing several sensors in one map | 79, 74 | PR 9.1, PR 9.2, PR 9.3 | Thrun et al. 2005 ch.9 |
| 99 | 3D maps: voxels, octrees, elevation maps and signed distance | B2 3D maps: voxel grids, octrees, elevation maps; 3D occupancy with octrees (OctoMap); Elevation maps for legged robots; Signed-distance (TSDF) maps (concept); Choosing a map type: landmarks, point clouds, voxels, elevation, meshes; surfel maps named; Quadtrees and multi-resolution grids | 98, 93 | AU-012, PE-077, PE-078, PE-079, PE-080, idx:quadtrees | FRE L10 "Techniques for 3D mapping"; NAV2 voxel layer; Hornung et al. 2013, *OctoMap* ([10.1007/s10514-012-9321-0](https://doi.org/10.1007/s10514-012-9321-0)); Cadena §V; Hornung et al. 2013 [doi:10.1007/s10514-012-9321-0](https://doi.org/10.1007/s10514-012-9321-0); Fankhauser et al. 2018 [doi:10.1109/LRA.2018.2849506](https://doi.org/10.1109/LRA.2018.2849506); Newcombe et al. 2011; LaValle, Planning Algorithms; Lynch & Park, Modern Robotics (book + lectures) |
| 100 | Layered costmaps: obstacles, inflation and keep-out zones | B1 Layered costmaps: static, obstacle and inflation layers, footprint, keep-out and speed zones; Distance transform of a grid (grassfire, Euclidean, signed) | 98, 73, MA-049 | AU-011, idx:distance_transform | NAV2 concepts "Environmental representation", costmap layers and filters; Lu, Hershberger, Smart 2014, *Layered costmaps* ([10.1109/IROS.2014.6942636](https://doi.org/10.1109/IROS.2014.6942636)); Prince, Computer Vision: Models, Learning, Inference; Szeliski, Computer Vision |
| 101 | Localizing in a prior 3D map: the normal distributions transform | C2 Localising against a prebuilt 3D map; the normal distributions transform (NDT); NDT scan matching | 94, 97, 99 | AU-016, PE-074 | AW localization "3D-LiDAR + point cloud map"; UDS C4 scan-matching localization; Biber & Straßer 2003, *The normal distributions transform* ([10.1109/IROS.2003.1249285](https://doi.org/10.1109/IROS.2003.1249285)); Lee §3.1; Biber & Strasser 2003 [doi:10.1109/IROS.2003.1249285](https://doi.org/10.1109/IROS.2003.1249285) |
| 102 | The SLAM problem | online SLAM vs full SLAM | 98, 96 | PR 10.1, PA 12.3 | Thrun et al. 2005 ch.10; LaValle 2006 ch.12 |
| 103 | Pose graphs and GraphSLAM | pose (constraint) graph; negative log posterior as a sum of quadratic terms; information form of a large SLAM problem; correspondence test in GraphSLAM; information form as a short section (full information filter stays optional) | 81, 102, new Maths Note: Nonlinear least squares (Gauss-Newton), new Maths Note: Schur complement, new Maths Note: Sparse linear solves and conjugate gradient, MA-070 | PR 11.1, PR 11.2, PR 11.4, PR 11.7 | Thrun et al. 2005 ch.11 |
| 104 | Loop closure and map merging | loop closure; multi-robot map integration and alignment; Outliers in the back-end: robust kernels, switchable constraints (concept); Loop closure for a visual map (was PE-056) | 103, 75 | PR 13.6, PR 12.7, PE-107, PE-056 | Thrun et al. 2005 ch.13; Thrun et al. 2005 ch.12; Barfoot 5.3–5.4; Cadena §III |

#### RO-06 State estimation and SLAM in depth *(optional)*

Optional: UKF and information filters, landmark SLAM, GraphSLAM, FastSLAM, factor graphs, visual-inertial and LiDAR-inertial odometry.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 271 | Unscented Kalman filter | unscented transform and sigma points; unscented Kalman filter (UKF); Unscented Kalman filter | 81, new Maths Note: Cholesky factor | PR 3.11, PR 3.12, PE-093 | Thrun et al. 2005 ch.3; RO 158 |
| 272 | Information filter | canonical form: information matrix and vector; information filter and extended information filter | 80, new Maths Note: Woodbury identity | PR 3.13, PR 3.14 | Thrun et al. 2005 ch.3 |
| 273 | Batch estimation and smoothing | Batch estimation and smoothing: lifted form, Cholesky/RTS smoother, fixed-interval and fixed-lag | 80, new Maths Note: Cholesky factor | idx:batch_smoothing | Barfoot, State Estimation for Robotics; Prince, Computer Vision: Models, Learning, Inference |
| 274 | EKF and UKF localization | EKF localization with landmarks; UKF localization; Iterated EKF | 96, 81, 271, 76, new Maths Note: Nonlinear least squares (Gauss-Newton) | PR 7.3, PR 7.8, idx:iekf | Thrun et al. 2005 ch.7; Barfoot, State Estimation for Robotics; Prince, Computer Vision: Models, Learning, Inference |
| 275 | Data association and multi-hypothesis tracking | the correspondence problem; maximum-likelihood data association with gating; mixture-of-Gaussians belief; multi-hypothesis tracking | 274, new Maths Note: Mahalanobis distance, MA-070, MA-073 | PR 7.4, PR 7.5, PR 3.9, PR 7.7 | Thrun et al. 2005 ch.7; Thrun et al. 2005 ch.3 |
| 276 | Learned sensor models and MAP mapping | learning the inverse sensor model from simulated data; MAP estimate of a whole map; MAP occupancy mapping with forward models | 98, MA-072, DL-014 | PR 9.4, PR 9.5, PR 9.6 | Thrun et al. 2005 ch.9 |
| 277 | EKF SLAM | EKF SLAM with known correspondence; landmark initialization | 102, 274 | PR 10.2, PR 10.3 | Thrun et al. 2005 ch.10 |
| 278 | EKF SLAM with unknown landmarks | provisional landmarks; feature selection and map management; incremental data association; equivalence constraints between landmarks | 277, 275 | PR 10.4, PR 10.5, PR 12.4, PR 12.6 | Thrun et al. 2005 ch.10; Thrun et al. 2005 ch.12 |
| 279 | Factor graphs, sliding windows and IMU preintegration | Filtering vs optimisation (sliding window); Factor graphs (beginner level); IMU preintegration; incremental smoothing (iSAM), named; Arrival cost in moving-horizon estimation | 103, 85, 273, new Maths Note: Lie groups for robot poses: perturbations and uncertainty on SO(3) and SE(3) | PE-098, PE-099, PE-100, idx:arrival_cost | Huang §3.1; Dellaert & Kaess 2017 [doi:10.1561/2300000043](https://doi.org/10.1561/2300000043); Cadena §II; Huang §3.5; Forster et al. 2017 [arXiv:1512.02363](https://arxiv.org/abs/1512.02363); Rawlings, Mayne & Diehl, MPC |
| 280 | Visual-inertial odometry: MSCKF, VINS and initialisation | Filter-based VIO (MSCKF, concept); Optimisation-based VIO (VINS-Mono as worked system); VIO initialisation: gravity, scale and biases | 279, 248, 88 | PE-101, PE-102, PE-103 | Huang §3.1; Mourikis & Roumeliotis 2007 [doi:10.1109/ROBOT.2007.364024](https://doi.org/10.1109/ROBOT.2007.364024); Huang §3.2; Qin et al. 2018 VINS-Mono [doi:10.1109/TRO.2018.2853729](https://doi.org/10.1109/TRO.2018.2853729); Huang §3.6 |
| 281 | LiDAR odometry and LiDAR-inertial odometry | Feature-based LiDAR odometry: edge and plane points; Degenerate scenes: long corridors and open fields; LiDAR-inertial odometry (loose and tight) | 279, 94, 101 | PE-075, PE-076, PE-105 | Lee §3.2; Zhang & Singh 2014 LOAM [doi:10.15607/RSS.2014.X.007](https://doi.org/10.15607/RSS.2014.X.007); Lee §7.3; Lee §4 |
| 282 | FastSLAM: particles over paths | Rao-Blackwellization: sample the path, landmarks become independent; FastSLAM 1.0; FastSLAM 2.0 improved proposal; per-particle data association; grid-based FastSLAM; entropy decomposition in SLAM; exploring with FastSLAM | 82, 277 | PR 13.1, PR 13.2, PR 13.3, PR 13.4, PR 13.7, PR 17.7 | Thrun et al. 2005 ch.13 |
| 283 | Multi-robot exploration | coordinating several exploring robots | 190, 104 | PR 17.6 | Thrun et al. 2005 ch.17 |

### Robotics / Control


#### RO-07 Robot models: pose, frames, wheeled and car-like kinematics



| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 64 | Pose and wheeled-robot motion | pose (x, y, heading); holonomic vs nonholonomic constraints; differential drive, simple car, Dubins and Reeds-Shepp car models; Differential drive: wheel speeds to (v, ω) and back; Nonholonomic constraint: a wheel cannot slide sideways; Holonomic and nonholonomic constraints; Pfaffian velocity constraints A(q)q' = 0 and the form q' = G(q)u; Car with trailers | new Maths Note: Rigid-body transforms and homogeneous coordinates, new Maths Note: State-space models, MA-063, MA-053 | PR 5.1, PA 13.1, PA 13.3, CT-004, CT-005, ME-014, idx:pfaffian, idx:trailers | Thrun et al. 2005 ch.5; LaValle 2006 ch.13; MR 13.3.1; MR 13.3.1, PA16 III.A, RVC3 4.1.1; MR 2.4; LaValle, Planning Algorithms; Lynch & Park, Modern Robotics (book + lectures); Murray, Li & Sastry, Robotic Manipulation; Tedrake, Underactuated Robotics (book + course + lectures) |
| 65 | Coordinate frames and the transform tree | A4 Coordinate frames and the transform tree (map → odom → base_link → sensor); Rotation matrix read as a frame: its columns are the new axes; inverse = transpose; using it to change frames | 64, new Maths Note: Rigid-body transforms and homogeneous coordinates, new Maths Note: 3D rotations: Euler angles and quaternions | AU-005, ME-004 | CMU wk 3 "Transform graphs & pose networks"; M42 ch.3 "Monogram notation"; NAV2 concepts "State estimation"; [REP-105](https://www.ros.org/reps/rep-0105.html); MR 3.2.1 |
| 66 | Wheel types, omnidirectional bases and the unicycle model | Types of wheeled robots: omnidirectional vs nonholonomic; Omnidirectional (mecanum) base model and control; Unicycle model (forward speed v, turn rate ω); Instantaneous centre of rotation; Steering mechanisms: turntable, Ackermann, skid steer, tracks; Under-, fully and over-actuated robots | 64, MA-063 | CT-001, CT-002, CT-003, idx:icr, idx:steering_mechanisms, idx:actuation_levels | MR 13.1; MR 13.2.1, 13.2.3; MR 13.3.1, PA16 III.A; Lynch & Park, Modern Robotics (book + lectures); Correll et al., Intro to Autonomous Robots; Wikipedia (glossary/outline pages); LaValle, Planning Algorithms |
| 67 | Car-like robots: the kinematic bicycle model and Ackermann steering | Kinematic bicycle model (front wheel steers, rear wheel follows); Steering angle, wheelbase and turning radius (tan δ = L / R); curvature; Ackermann steering geometry (inner wheel turns more than outer); Speed and steering limits (maximum steer, minimum turning radius); Controllability of a car in plain words (parallel parking); Kinematic vs dynamic model: when the kinematic model is enough | 66 | CT-007, CT-008, CT-009, CT-010, CT-012, CT-013 | SN09 3.1, PA16 III.A, RAJ 2.2; SN09 2.1, RVC3 4.1.1; RAJ 2.2; RVC3 4.1.1, MR 13.3.1; MR 13.3.2; Kong 2015 |
| 69 | Kinematic chains: where the hand and foot are | kinematic chains and forward kinematics; Denavit-Hartenberg parameters; kinematic trees (branching bodies such as humanoids); Forward kinematics of an open chain | new Maths Note: Rigid-body transforms and homogeneous coordinates, new Maths Note: 3D rotations: Euler angles and quaternions | PA 3.10, PA 3.11, PA 3.12, ME-018, ME-019, ME-020 | LaValle 2006 ch.3; MR ch.4 intro; MR App. C; PA ch.3 |
| 70 | Robot description files: URDF, SDF and MJCF | J1 Robot description formats: URDF/Xacro, SDF, MJCF: links, joints, inertias, collision vs visual shapes; Robot description files (URDF): links, joints, masses and inertias; Joint types (revolute, prismatic, spherical...) and Grübler's count of degrees of freedom | 69, 65 | AU-042, ME-016, ME-013 | M42 ch.2 "Robot description files"; UDR C2; URDF ([wiki.ros.org/urdf](https://wiki.ros.org/urdf)); MJCF ([MuJoCo XML reference](https://mujoco.readthedocs.io/en/stable/XMLreference.html)); MR 4.2, 8.8; MR 2.2.1–2.2.2 |

#### RO-08 Classical feedback control

Feedback on one loop: block diagrams, PID, step response, transfer functions, Bode and Nyquist, robustness, tuning and digital control.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 119 | Feedback basics: open and closed loop and the block diagram | Control-system basics: open vs closed loop; plant, reference, error, sensor, actuator, disturbance, noise in one block diagram; why feedback helps; Setpoint regulation vs trajectory tracking | 63, new Maths Note: State-space models | idx:control_basics, idx:regulation_vs_tracking | Brunton, Control Bootcamp; Caltech CDS 110/ChE 105 Analysis and Design of Feedback Control Systems; LaValle, Planning Algorithms; Lynch & Park, Modern Robotics (book + lectures); MATLAB Tech Talks; MIT 2.004 Dynamics and Control II; Stachniss lectures (Bonn); Åström & Murray, Feedback Systems |
| 120 | PD and PID control | PD / PID feedback control: act on error, its derivative and integral; short section: Newtonian and rigid-body mechanics (F = ma, torque, inertia); Rigid-body dynamics (F = ma, torque, inertia); Basic PD/PID on a single axis | MA-061, new Maths Note: Stability of dynamical systems | R0.7, CT-014, CT-105 | legged_gym; Stooke et al. 2020; MR 8.2, RVC3 3.2.1; robotics.md (RL R0.7) |
| 121 | Reading a controller's response: step response and second-order systems | Error dynamics and the step response (overshoot, settling time, damping); Error dynamics of a second-order system: overshoot, settling time, damping ratio, natural frequency; First-order systems and step-response specs: time constant, rise time, DC gain, steady-state error, damped natural frequency | 120, new Maths Note: Stability of dynamical systems, new Maths Note: ODEs and vector fields | CT-034, ME-056, idx:step_specs_first_order | MR 11.2; Caltech CDS 110/ChE 105 Analysis and Design of Feedback Control Systems; Lynch & Park, Modern Robotics (book + lectures); MIT 2.004 Dynamics and Control II; Wikipedia (glossary/outline pages); Åström & Murray, Feedback Systems |
| 122 | Transfer functions, poles and zeros | Transfer functions: G(s) from the ODE or from state space; poles and zeros; BIBO stability; block-diagram algebra; pole-zero cancellation; non-minimum phase; time delay; SISO vs MIMO; Routh-Hurwitz named; Root locus | new Maths Note: The Laplace transform, 121, new Maths Note: State-space models | idx:transfer_functions, idx:root_locus | Brunton, Control Bootcamp; Lynch & Park, Modern Robotics (book + lectures); MATLAB Tech Talks; MIT 16.30 Feedback Control Systems; MIT 2.004 Dynamics and Control II; Rawlings, Mayne & Diehl, MPC; Wikipedia (glossary/outline pages); Åström & Murray, Feedback Systems |
| 123 | Frequency response and Bode plots | Frequency response and Bode plots: gain and phase, asymptotes, bandwidth, resonance | 122, new Maths Note: Fourier series and the Fourier transform, 83 | idx:frequency_response | Brunton, Control Bootcamp; Caltech CDS 110/ChE 105 Analysis and Design of Feedback Control Systems; Correll et al., Intro to Autonomous Robots; Lynch & Park, Modern Robotics (book + lectures); MATLAB Tech Talks; MIT 16.30 Feedback Control Systems; MIT 2.004 Dynamics and Control II; Wikipedia (glossary/outline pages); Åström & Murray, Feedback Systems |
| 124 | The Nyquist criterion and stability margins | Loop transfer function, Nyquist criterion, gain/phase/delay margins | 123, new Maths Note: Complex numbers and Euler's formula | idx:nyquist_margins | Brunton, Control Bootcamp; Caltech CDS 110/ChE 105 Analysis and Design of Feedback Control Systems; MATLAB Tech Talks; Wikipedia (glossary/outline pages); Åström & Murray, Feedback Systems |
| 125 | Sensitivity, robustness and loop shaping | Sensitivity functions (S, T, gang of four), disturbance attenuation, robustness to model error and its limits; Loop shaping; lead, lag and lead-lag compensators | 124 | idx:sensitivity_robustness, idx:loop_shaping | Brunton, Control Bootcamp; Caltech CDS 110/ChE 105 Analysis and Design of Feedback Control Systems; MATLAB Tech Talks; MIT 16.30 Feedback Control Systems; Åström & Murray, Feedback Systems; Wikipedia (glossary/outline pages) |
| 126 | Feedforward, integral action, cascaded loops and windup | Feedforward plus feedback; Feedforward plus feedback; motion vs force control; Integral action in state feedback; Integrator windup and actuator saturation; Cascaded control loops (fast inner loop, slower outer loop); Anti-windup: clamping and back-calculation; Internal model principle | 121, 122 | CT-037, ME-055, CT-035, CT-036, CT-038, idx:anti_windup, idx:internal_model_principle | MR 11.3, RVC3 9.4.1; MR 11.1; FBS 7.4; FBS 11.4, 11.5; RVC3 9.1.6, 9.1.7, RAJ 5.4–5.5, SU22 II.A; Åström & Murray, Feedback Systems; Rawlings, Mayne & Diehl, MPC |
| 127 | PID tuning in practice | PID tuning and practice: ideal form, Ziegler-Nichols, model-based tuning, derivative kick, set-point weighting; Filters inside control loops: derivative low-pass, notch | 120, 126, 123, new Maths Note: Digital filters: moving average, low-pass, FIR and IIR | idx:pid_tuning, idx:control_loop_filters | MATLAB Tech Talks; Åström & Murray, Feedback Systems |
| 128 | Digital control: sampling a continuous controller | Digital control: A/D and D/A, zero-order hold, sample-rate choice, discretising a controller, z-transform and difference equations | new Maths Note: The z-transform and discrete-time systems, new Maths Note: Sampling and aliasing, 127 | idx:digital_control | MATLAB Tech Talks; MIT 16.30 Feedback Control Systems; Stachniss lectures (Bonn); Wikipedia (glossary/outline pages); Åström & Murray, Feedback Systems |

#### RO-09 Path tracking

From a planned path to wheel commands: driving to a goal, path vs trajectory tracking, pure pursuit, Stanley, Kanayama.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 129 | Driving to a point, a line and a pose | Moving to a point; Following a line; Moving to a pose (position and heading), polar-coordinate controller | 66, 120 | CT-040, CT-041, CT-042 | RVC3 4.1.1.1; RVC3 4.1.1.2; RVC3 4.1.1.4 |
| 130 | Path following vs trajectory tracking: path coordinates and tracking errors | Path following vs trajectory tracking; Path coordinates (Frenet frame): distance along the path s, sideways offset, heading error; Cross-track error and heading error | 129, 67 | CT-043, CT-011, CT-044 | PA16 V (Problems V.1, V.2); SN09 3.1.1, RAJ 2.5, PA16 V; SN09 2, AR24 5.1.3, PA16 V |
| 131 | Pure pursuit | Pure pursuit; Look-ahead distance and its tuning (look-ahead grows with speed) | 130 | CT-045, CT-046 | Coulter 1992, SN09 2.2, PA16 V.A.1, RVC3 4.1.1.3; SN09 2.2.1 |
| 132 | The Stanley controller and rear-wheel feedback | Stanley controller (front-wheel feedback); Tuning the Stanley controller; Rear-wheel feedback path controller | 131 | CT-047, CT-048, CT-049 | Thrun 2006, Hoffmann 2007, SN09 2.3, PA16 V.A.3; SN09 2.3.1; PA16 V.A.2 |
| 133 | Tracking a timed trajectory: Kanayama and feedback linearisation | Kanayama tracker: error in the robot's own frame, virtual reference robot, Lyapunov-proved stable; Feedback linearisation | 130, 126, new Maths Note: Stability of dynamical systems | CT-050, CT-039 | Kanayama 1990, PA16 V.B.1, MR 13.3.4; UR 3, PA16 V.B.2 |
| 134 | Feedforward on curves, tracker metrics and choosing a tracker | Feedforward steering from path curvature; Comparing trackers: speed, curvature, tuning effort; Tracker metrics: RMS and peak lateral error, steering effort | 132, 133 | CT-052, CT-053, CT-054 | SN09 4.3, RAJ 3.2; SN09 5, AR24 6; AR24 5.1.3 |

#### RO-10 Trajectories, LQR and MPC

Timed references, then optimal feedback: polynomial and spline trajectories, speed profiles, LQR, linear and nonlinear MPC, MPPI.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 210 | Time scaling and polynomial trajectories | Path vs trajectory; time scaling s(t); Path vs trajectory; time scaling; Cubic and quintic polynomials from boundary conditions; Cubic and quintic polynomial time scaling; Trapezoidal velocity profile; Trapezoidal velocity profile and S-curve | 130, ML-060, ML-053 | CT-084, ME-048, CT-085, ME-050, CT-086, ME-051 | MR 9.1; MR 9.2, RVC3 3.3.1; MR 9.2.2 |
| 211 | Via points, splines and minimum-jerk trajectories | Via points and multi-segment trajectories; continuity at the joins; Via points and spline trajectories; Cubic splines; Minimum-jerk trajectories; Interpolating orientation (slerp); Dynamically feasible vs infeasible references; B-splines: smooth curves from control points with local control | 210, new Maths Note: 3D rotations: Euler angles and quaternions | CT-087, ME-052, CT-088, CT-089, CT-093, CT-094, idx:bsplines | MR 9.3, RVC3 3.3.2, 3.3.3; MR 9.3; MR 9.3, RVC3 3.3.3; Flash & Hogan 1985; RVC3 3.3.4; SU22 VI.C–D; LaValle, Planning Algorithms; Szeliski, Computer Vision |
| 212 | Speed profiles along a fixed path | Time-optimal time scaling under speed and acceleration limits; Time-optimal time scaling under torque limits (phase plane); F5 Speed planning: stop lines, following distance, comfort limits along a fixed path; Bang-bang (time-optimal) control of the double integrator | 210, 67, new Maths Note: State-space models | CT-092, ME-053, AU-029, idx:bang_bang | MR 9.4; TOR C4 M8 "velocity profile generation"; AW behaviour velocity planner, obstacle stop / adaptive cruise; LaValle, Planning Algorithms; Lynch & Park, Modern Robotics (book + lectures) |
| 213 | State feedback, controllability and pole placement | State feedback u = −Kx and pole placement; Controllability (reachability) and the rank test | 121, new Maths Note: State-space models, new Maths Note: Matrix exponential and logarithm, MA-056 | CT-033, CT-031 | FBS 7.2, 7.3, RAJ 3.1; FBS 7.1, MPC 1.3.5, 2.4.4 |
| 214 | LQR: the linear-quadratic regulator | Hamilton-Jacobi-Bellman equation; linear-quadratic regulator and the Riccati equation; Discrete-time LQ problem solved by dynamic programming (Riccati recursion); Infinite-horizon LQR and the steady Riccati equation; Choosing the Q and R weights; HJB equation; Optimal-control problem anatomy: stage cost, terminal cost, cost-to-go | 213, 14 | PA 15.6, PA 15.7, CT-057, CT-058, CT-059, CT-109, idx:optimal_control_anatomy | LaValle 2006 ch.15; MPC 1.3.1–1.3.3; MPC 1.3.4, 1.3.6, UR 8; SN09 4.2.1; robotics.md (PA 15.6); Rawlings, Mayne & Diehl, MPC; Tedrake, Underactuated Robotics (book + course + lectures) |
| 215 | Observers and output feedback: Luenberger observer, separation principle, LQG | State observers and output feedback: observability matrix and rank test, Luenberger observer, stabilisability and detectability, duality; LQG: LQR plus a Kalman filter (separation principle); output-feedback MPC | 213, 214, 80 | idx:observers, idx:lqg | Barfoot, State Estimation for Robotics; Brunton, Control Bootcamp; CMU 16-745 Optimal Control and Reinforcement Learning; Caltech CDS 110/ChE 105 Analysis and Design of Feedback Control Systems; MIT 16.30 Feedback Control Systems; Rawlings, Mayne & Diehl, MPC; Tedrake, Underactuated Robotics (book + course + lectures); Åström & Murray, Feedback Systems; Kochenderfer et al., Algorithms for Decision Making; LaValle, Planning Algorithms; Wikipedia (glossary/outline pages) |
| 216 | LQR for tracking: references, feedforward and time-varying gains | LQR for tracking a reference (error coordinates, steady-state target); Time-varying LQR to hold a robot on a planned trajectory; LQR with feedforward; Linearising a model around an operating point or a moving reference; Iterative learning control | 214, 126, 118, MA-064 | CT-060, CT-062, CT-063, CT-030, idx:ilc | MPC 1.5.1; UR 8; SN09 4.3, MR 11.3; FBS 6.4, PA16 V; CMU 16-745 Optimal Control and Reinforcement Learning |
| 217 | Model predictive control: receding horizon, constraints and the QP | Receding horizon: plan N steps, apply the first, re-plan; Input and state constraints (steering limits, speed limits, keep-out zones); Linear MPC as a quadratic program (stack the predictions, condensed vs sparse); Terminal cost and terminal set; why a short horizon can fail; Unconstrained MPC equals LQR; Explicit MPC: the law precomputed as a piecewise-affine table; Hard vs soft constraints with slack variables; Invariant sets and recursive feasibility of MPC | 214, MA-068, new Maths Note: Stability of dynamical systems | CT-064, CT-065, CT-066, CT-067, CT-068, idx:explicit_mpc, idx:soft_constraints, idx:invariant_sets_mpc | MPC 1.3, NG20 III; MPC 1.2.5, 2.5.4; MPC 1.3.1, 8.8, NG20 III.A; MPC 2.4.2, 2.6; MPC 2.5.1; Rawlings, Mayne & Diehl, MPC; Tedrake, Underactuated Robotics (book + course + lectures) |
| 218 | Nonlinear MPC and solving it in real time | Disturbances and offset-free MPC; Nonlinear MPC; Linear vs nonlinear MPC: accuracy against compute; Newton-type solvers: SQP and interior point (overview only); Real-time MPC: warm starts, real-time iteration, stopping early; Robust and stochastic MPC: tube MPC with tightened constraints, min-max, chance constraints | 217, 118, MA-064 | CT-069, CT-070, CT-071, CT-073, CT-074, idx:robust_mpc | MPC 1.5.2, 5.5; MPC 2.5.5, NG20 III.B, SU22 IV.A; NG20 III.C; MPC 8.6, 8.7; MPC 8.9, 2.7; Kochenderfer et al., Algorithms for Decision Making; Rawlings, Mayne & Diehl, MPC; Tedrake, Underactuated Robotics (book + course + lectures) |
| 219 | MPC for path following | MPC for path following on the bicycle model | 217, 130, 67 | CT-075 | PA16 V.C, Kong 2015 |
| 220 | Sampling-based MPC: MPPI | Sampling-based MPC: model predictive path integral (MPPI) | 217, new Maths Note: Monte Carlo estimation, 43, 140 | CT-076 | Williams 2016 |
| 221 | MPC and RL: comparing and combining | MPC vs RL, and combining them | 220, 163, 39 | CT-079 | NG20 III.E, WE22 VII, SU22 VIII |

#### RO-11 Aerial robots: quadrotors and agile flight

3D rigid-body dynamics, quadrotor model and control, flat trajectories, learned agile flight

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 230 | Rigid-body dynamics in 3D: Euler's equation and the inertia matrix | One rigid body in 3D: F = ma plus Euler's equation; the 3×3 inertia matrix; Inertial reference frame; Parallel-axis theorem; Principal axes of inertia; Static equilibrium: forces and torques sum to zero | new Maths Note: 3D rotations: Euler angles and quaternions, 85, MA-056 | ME-036, idx:inertial_frame, idx:parallel_axis, idx:principal_axes, idx:static_equilibrium | MR 8.2.1; LaValle, Planning Algorithms; Lynch & Park, Modern Robotics (book + lectures); Correll et al., Intro to Autonomous Robots |
| 231 | The quadrotor model | mixer: four thrusts to thrust and three torques; 3D dynamics; underactuation: tilt to move | 230, 85 | CT-098, CT-099, CT-100 | Mahony et al. 2012; Corke 2023 (RVC3) 4.2; Sun et al. 2022 §III.B |
| 232 | Hovering and cascaded quadrotor control | linearise at hover, LQR or PID; attitude loop inside position loop | 231, 126, 214 | CT-101, CT-102 | Tedrake, Underactuated Robotics ch.3; Sun et al. 2022 §II.A |
| 233 | Differential flatness | state and inputs from position, yaw and derivatives | 232 | CT-103 | Mellinger & Kumar 2011 |
| 234 | Minimum-snap trajectories and time allocation | piecewise polynomials as a QP; time per segment | 233, 211, MA-068 | CT-090, CT-091 | Mellinger & Kumar 2011; Richter et al. 2016 |
| 235 | Geometric control and MPC for quadrotors | large-angle control on SE(3); quadrotor NMPC; INDI named | 234, 218 | CT-104, CT-078 | Lee et al. 2010; Sun et al. 2022 §IV |
| 236 | Agile aerial navigation | privileged expert imitated by a sensor policy; RL for drone racing; RL vs optimal control; RL for agile flight; RL for quadrotor flight control; Legged and aerial navigation | 175, 148, 118, 235 | N.24, CT-106, RS-021, RS-045 | Loquercio et al. 2021; Kaufmann et al. 2023; Song et al. 2023; robotics.md (RL N.24); Tang §4.1.3; Tang §4.2.2-4.2.3 |

#### RO-12 Rigid-body motion and arm kinematics

Twists and screws, product of exponentials, Jacobians, singularities, inverse kinematics.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 293 | Twists, wrenches and screw motion | Twist: angular and linear velocity of a body as one 6-number vector; the adjoint map that moves it between frames; Screw axis and exponential coordinates of a rigid motion; Wrench: force and torque as one 6-number vector; moving it between frames; Fixed (space) frame vs body frame; Body vs spatial angular velocity and twist (and wrench); Chasles-Mozzi theorem: every rigid motion is a screw motion | 85, 69, new Maths Note: Matrix exponential and logarithm, new Maths Note: Cross product and skew-symmetric matrix | ME-009, ME-010, ME-011, idx:space_body_frames, idx:body_spatial_velocity, idx:chasles | MR 3.3.2; MR 3.3.3; MR 3.4; Lynch & Park, Modern Robotics (book + lectures); Berkeley EECS C106A/206A Introduction to Robotics; Murray, Li & Sastry, Robotic Manipulation |
| 294 | Forward kinematics by the product of exponentials; workspace | Product of exponentials: hand pose from screw axes, in the base frame and the hand frame; how it compares with DH; Task space and workspace: where the hand can reach; Robot arm types: Cartesian, SCARA, articulated, parallel; Reachable vs dexterous workspace | 293, 69 | ME-021, ME-015, idx:arm_types, idx:workspace_types | MR 4.1.1–4.1.3, C.5; MR 2.5; Lynch & Park, Modern Robotics (book + lectures); Wikipedia (glossary/outline pages); Murray, Li & Sastry, Robotic Manipulation |
| 295 | The manipulator Jacobian and statics | Manipulator Jacobian (space and body forms): joint speeds to hand twist; Analytic Jacobian (rates of Euler angles) vs geometric Jacobian; Statics: joint torques that hold a hand force, τ = Jᵀ F; Principle of virtual work (why tau = J^T F) | 294, MA-063 | ME-022, ME-023, ME-024, idx:virtual_work | MR 5.1.1–5.1.4; MR 5.1.5; MR 5.2; Tedrake, Underactuated Robotics (book + course + lectures) |
| 296 | Singularities, manipulability and redundancy | Singularities: the Jacobian loses rank and the hand cannot move in some direction; Manipulability ellipsoid and measure; Redundancy and self-motion in the null space; Force and acceleration ellipsoids | 295, MA-057, MA-058, new Maths Note: Null-space projector and weighted pseudo-inverse | ME-025, ME-026, ME-027, idx:force_ellipsoids | MR 5.3; MR 5.4; Yoshikawa 1985; MR 6.3; Siciliano ch.3; Correll et al., Intro to Autonomous Robots; Lynch & Park, Modern Robotics (book + lectures) |
| 297 | Inverse kinematics: analytic and numerical | The IK problem: none, one, many or infinitely many answers; Analytic IK: 2-link planar arm, wrist-splitting for 6-joint arms; Newton–Raphson for solving equations (root finding); Numerical IK: iterate with the Jacobian pseudo-inverse; Paden-Kahan subproblems for analytic IK | 295, MA-064, MA-060 | ME-028, ME-029, ME-030, ME-031, idx:paden_kahan | MR ch.6 intro; MR 6.1, 6.1.1–6.1.2; MR 6.2.1; MR 6.2.2; Murray, Li & Sastry, Robotic Manipulation |
| 298 | Damped, transpose and differential IK; straight-line hand motion | Damped least squares IK; Jacobian-transpose IK; Differential (inverse velocity) IK: q̇ = J⁺ V, and its use for tracking a moving target; Straight-line paths in joint space and in task space (including SE(3)); Differential IK as a QP with joint, velocity and collision limits | 297, 296, ML-063, 210, MA-068 | ME-032, ME-033, ME-034, ME-049, idx:diff_ik_qp | Wampler 1986; Nakamura & Hanafusa 1986; Siciliano ch.3; MR 6.3; MR 9.2.1; MIT 6.4210/6.4212 Robotic Manipulation |
| 299 | Closed chains and parallel robots | Closed chains and parallel robots: loop-closure equations, delta, Stewart | 297, 298 | idx:parallel_robots | LaValle, Planning Algorithms; Lynch & Park, Modern Robotics (book + lectures); Murray, Li & Sastry, Robotic Manipulation; Wikipedia (glossary/outline pages) |

#### RO-13 Dynamics, arm control, contact and grasping



| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 300 | Lagrangian mechanics and the manipulator equation | Lagrangian mechanics: L = kinetic − potential energy; Euler–Lagrange equation on a 2-link arm; Manipulator equation M(q)q̈ + c(q,q̇) + g(q) = τ; what the mass matrix means; Centripetal and Coriolis terms; Generalized coordinates and generalized forces | 230, MA-066 | ME-037, ME-038, idx:coriolis, idx:generalized_coords | MR 8.1.1; Tedrake App. B; MR 8.1.2–8.1.3; Lynch & Park, Modern Robotics (book + lectures); Åström & Murray, Feedback Systems; Murray, Li & Sastry, Robotic Manipulation |
| 301 | Inverse and forward dynamics | Recursive Newton–Euler inverse dynamics (torques for a wanted motion); Forward dynamics: solve for accelerations, then integrate; Inertial-parameter identification: dynamics linear in the parameters, least squares, exciting trajectories; Twist-wrench (spatial) form of rigid-body dynamics | 300, 137, ML-053, 293 | ME-039, ME-040, idx:dynamic_param_id, idx:spatial_dynamics | MR 8.1.4, 8.3; MR 8.5; Tedrake, Underactuated Robotics (book + course + lectures); Lynch & Park, Modern Robotics (book + lectures) |
| 302 | Actuators: electric motors, drivers, fluid power and elastic actuators | Electric motor types: brushed, brushless, stepper, servo, AC; DC motor model: torque constant and back-EMF; Motor drivers: PWM and H-bridge; Hydraulic and pneumatic actuators | 301 | idx:electric_motor_types, idx:dc_motor_model, idx:motor_drivers_pwm, idx:fluid_actuators | Correll et al., Intro to Autonomous Robots; Lynch & Park, Modern Robotics (book + lectures); Wikipedia (glossary/outline pages) |
| 303 | Motors, gears and the joint torque loop | Motors, gearing, reflected inertia, friction, flexible joints; Low-level joint torque control loop; Series elastic actuators; Gear ratio choice: direct drive vs geared, inertia matching; Backlash and gear transmission errors; Friction models: Stribeck effect | 301, 148 | ME-043, ME-067, idx:sea, idx:gear_ratio_direct_drive, idx:backlash, idx:stribeck | MR 8.9.1–8.9.5; MR 11.8; Correll et al., Intro to Autonomous Robots; Lynch & Park, Modern Robotics (book + lectures) |
| 304 | Joint-space control: velocity inputs, PD plus gravity, computed torque | Control with velocity inputs, in joint space and task space; PD plus gravity compensation; Independent-joint (decentralised) control vs centralised control; Computed torque (inverse dynamics control, feedback linearisation) | 300, 121, 126 | ME-057, ME-058, ME-059, ME-060 | MR 11.3.1–11.3.3; MR 11.4.1; Siciliano ch.8; MR 11.4.2 |
| 305 | Task-space and operational space control | Task-space motion control with torque inputs; Operational space control: task-space inertia, Jᵀ F, dynamically consistent null space; Dynamics in task space: the hand's apparent mass Λ = (J M⁻¹ Jᵀ)⁻¹ | 304, 295, 296 | ME-061, ME-062, ME-041 | MR 11.4.3; Khatib 1987; MR 8.6 |
| 306 | Force control and hybrid motion-force control | Force control; Hybrid motion–force control; natural and artificial constraints; Force/torque sensors (strain gauges) | 305 | ME-063, ME-064, idx:ft_sensors | MR 11.5; MR 11.6.1–11.6.2; Correll et al., Intro to Autonomous Robots; LaValle, Planning Algorithms; Lynch & Park, Modern Robotics (book + lectures) |
| 307 | Impedance and admittance control | Impedance control: behave like a virtual spring and damper; Admittance control; Collaborative robots and physical safety | 306 | ME-065, ME-066, idx:cobots | MR 11.7.1; Hogan 1985; MR 11.7.2; Correll et al., Intro to Autonomous Robots |
| 308 | Contact kinematics, contact types and the friction cone | Contact kinematics: rolling, sliding, breaking free; Contact types: point without friction, point with friction, soft finger; Coulomb friction and the friction cone (and its pyramid approximation); Contact forces and the friction cone; Soft and deformable contacts | 293, MA-067 | ME-078, ME-079, ME-080, CT-024, idx:soft_contacts | MR 12.1.1–12.1.2; MR 12.1.5; Sahbani 2012; MR 12.2.1; WE22 III.A, UR 5; Correll et al., Intro to Autonomous Robots |
| 309 | Contact forces and contact as a hybrid system | Constrained dynamics: contact forces as Lagrange multipliers; Contact as a hybrid system: modes switch on touch-down and lift-off; impacts; Complementarity contact model: force only when touching, touching only when force; Contact scheduling: fixed gait sequence vs contact-implicit planning | 308, 300 | ME-042, ME-044, ME-045, ME-046 | MR 8.7; Wensing III-A1; Tedrake ch.17; Wensing III-A2; Wensing III-B |
| 310 | Grippers and end effectors | Gripper mechanisms: parallel jaw, linkages, suction, multi-finger | 308 | idx:grippers | Correll et al., Intro to Autonomous Robots; Wikipedia (glossary/outline pages) |
| 311 | Form closure, force closure and the grasp matrix | Form closure; Force closure; Grasp matrix: contact forces to object wrench; Linear, positive and convex span (cones of contact wrenches); Hand Jacobian and the grasp constraint; Internal (squeezing) forces: null space of the grasp matrix | 308, new Maths Note: Convex hull, MA-052, 295 | ME-081, ME-082, ME-083, idx:spans_cones, idx:hand_jacobian_grasp, idx:internal_forces_grasp | MR 12.1.6–12.1.7; MR 12.2.3; MR 12.2; Sahbani 2012; Lynch & Park, Modern Robotics (book + lectures); Murray, Li & Sastry, Robotic Manipulation |
| 312 | Grasp quality and grasp selection | Grasp quality: the largest push a grasp can resist; Analytic vs data-driven grasp synthesis; known, familiar and unknown objects; K4 Grasp selection: antipodal grasps, friction cones, grasp quality, grasps from point clouds | 311, 93 | ME-084, ME-085, AU-048 | Ferrari & Canny 1992; Bohg et al. 2014; Sahbani 2012; M42 ch.5 grasp selection; S237B wk 4–5 |

#### RO-14 Legged robots: balance and model-based control

Gaits, ZMP and the inverted pendulum, capture point, centroidal dynamics, convex MPC and whole-body control.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 317 | Underactuated systems: cart-pole, acrobot and swing-up | Underactuated systems: cart-pole, acrobot, energy-shaping swing-up, LQR balance, partial feedback linearisation | 214, new Maths Note: ODEs and vector fields, 120, 300 | idx:underactuated | Brunton, Control Bootcamp; Tedrake, Underactuated Robotics (book + course + lectures); Åström & Murray, Feedback Systems |
| 318 | Gaits, support polygons and the floating base | Gait vocabulary: walk, trot, pace, bound, gallop; stance and swing; duty factor; Centre of mass, support polygon, static vs dynamic balance; Floating base: a legged robot's body is 6 extra unpowered degrees of freedom | 309, 230, new Maths Note: Convex hull | ME-088, ME-089, ME-017 | Raibert 1986; Tedrake ch.4; Kajita ch.3; Tedrake 5; Wensing II-B; Tedrake App. B |
| 319 | Zero-moment point and the linear inverted pendulum | Centre of pressure and zero-moment point (ZMP); Linear inverted pendulum model (LIPM); Simplified models: linear inverted pendulum (LIP), single rigid body, centroidal dynamics; Zero-moment point (ZMP) and ZMP walking | 318, new Maths Note: State-space models | ME-090, ME-091, CT-080, CT-081 | Tedrake 5 (CoP and ZMP); Vukobratović & Borovac 2004; Kajita 2001; Kajita ch.4; WE22 IV, UR 4, UR 5; UR 5 |
| 320 | ZMP walking with preview control | ZMP walking: footsteps, then ZMP path, then CoM path by preview control | 319, 216 | ME-092 | Tedrake 5 (ZMP planning); Kajita 2003 |
| 321 | Capture point and push recovery | Capture point: where to step to stop; Divergent component of motion (3D capture point) control | 319 | ME-093, ME-094 | Pratt et al. 2006; Tedrake 5 (push recovery); Englsberger et al. 2015 |
| 322 | Hopping and running: SLIP, Raibert's controller and passive walkers | Spring-loaded inverted pendulum (SLIP) for running; Passive walkers, limit cycles and Poincaré maps; Raibert hopping controller: foot placement for speed, thrust for height, hip torque for posture | 319, 120 | ME-095, ME-096, ME-097 | Tedrake 4 (SLIP); Tedrake 4 (rimless wheel, compass gait); Raibert 1986; Tedrake 4 (MIT Leg Lab hoppers) |
| 323 | Central pattern generators | Central pattern generators (CPGs); Structured action spaces: central pattern generators, foot-trajectory generators | 318, 143 | ME-098, RS-048 | Ijspeert 2008; Ha 1.3; Ha §3.4 |
| 324 | Centroidal dynamics and the single rigid body model | Centroidal dynamics: only contact forces and gravity change the whole body's momentum; centroidal momentum matrix; Single rigid body model of a quadruped | 318, 293 | ME-099, ME-100 | Orin et al. 2013; Tedrake 5 (centroidal dynamics); Wensing IV-A; Di Carlo et al. 2018; Wensing IV-B |
| 325 | Convex MPC for legged robots | Convex MPC for legged robots: choose foot forces by a QP over a short horizon; Convex MPC for legged robots (single rigid body, ground reaction forces, QP); Contact schedule (gait timing) as a fixed input to MPC; MPC with simplified models (inverted pendulum, centroidal); Whole-body and mixed-fidelity MPC | 324, 308, 217, 309 | ME-101, CT-077, CT-082, RS-082, ME-102 | Di Carlo et al. 2018; Gu V-A; Di Carlo 2018, WE22 IV; WE22 III.B, Di Carlo 2018; Gu hum §V; Gu V-B–V-C |
| 326 | Whole-body control: tasks and null-space priority | Tasks and task Jacobians: any quantity to control (hand pose, CoM, posture) is a "task"; Strict task priority by null-space projection; Whole-body control in closed form (prioritised operational space control) | 305, 296 | ME-070, ME-071, ME-072 | Wensing VI-A1–VI-A2; Gu VI-A; Siciliano & Slotine 1991; Moro & Sentis; Sentis & Khatib 2005; Gu VI-B |
| 327 | QP-based whole-body control | QP-based whole-body control: one quadratic program with weighted tasks, dynamics, contact and torque limits; Hierarchical QP (stack of tasks): strict priorities with inequalities; Inequality tasks: joint limits, torque limits, collision avoidance; WBC as the layer that tracks a plan from a simpler model; Whole-body control: a QP that turns wanted forces and motions into joint torques; Whole-body control as a QP with task priorities; Whole-body motion generation and control for humanoids | 326, 325, MA-068 | ME-073, ME-074, ME-075, ME-077, CT-083, RS-083, ME-107 | Gu VI-C; Wensing VI-B; Escande et al. 2014; Wensing VI-B2; Wensing VI-A4; Wensing II-D; WE22 II.D, VI, UR 5; Gu hum §VI; Kajita ch.5; Gu VI |
| 328 | Legged state estimation: leg kinematics fused with the IMU | Legged state estimation: fuse leg kinematics with the IMU | 87, 295, 81 | ME-104 | Bloesch et al. 2013 |
| 329 | Multi-contact planning | Multi-contact planning (search, optimisation, learning); Multi-contact planning (where to place hands and feet) | 325 | ME-103, RS-086 | Gu IV; Gu hum §IV |

#### RO-15 Car dynamics and steering control *(optional)*

Optional: tyres, forces and LQR steering for fast cars.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 265 | The dynamic bicycle model, slip angle and cornering stiffness | Dynamic bicycle model (sideways force, yaw rate, yaw inertia); Tyre slip angle; Cornering stiffness: the linear tyre model | 67, 120 | CT-015, CT-016, CT-017 | RAJ 2.3, PA16 III.B, SN09 4.1; RAJ 2.3, SN09 4.1; SN09 4.1, RAJ 2.3 |
| 266 | Tyre limits: saturation and longitudinal slip | Tyre force saturation and friction limit; Longitudinal slip ratio: why driving and braking force depends on slip | 265 | CT-018, CT-019 | SN09 4.1 (tyre data figures), PA16 III.B; RAJ 4.1.2, 4.1.3 |
| 267 | Longitudinal dynamics and cruise control | Longitudinal dynamics: aerodynamic drag and rolling resistance; Cruise control: upper level (wanted acceleration) and lower level (throttle, brake) | 266, 126 | CT-020, CT-023 | RAJ 4.1.1, 4.1.4; RAJ 5.3–5.5 |
| 268 | Road error dynamics and LQR steering | Error dynamics with respect to the road (lateral and yaw error states); LQR steering on the dynamic bicycle model | 265, 216 | CT-021, CT-061 | RAJ 2.5, 2.6; SN09 4.2, RAJ 3.1, AR24 4.1 |
| 269 | Steady cornering and understeer | Steady-state cornering and understeer | 265 | CT-022 | RAJ 3.3 |
| 270 | Preview control and gain scheduling | Preview (look-ahead) control; Gain scheduling / linear parameter-varying control; linear parameter-varying (LPV) control, named | 268 | CT-051, CT-056 | RAJ 3.11, SN09 4.4; PA16 V.D |

### Robotics / Navigation and planning


#### RO-16 Configuration space and graph search



| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 72 | Configuration space and degrees of freedom | configuration space (C-space) and degrees of freedom; C-space shapes in plain words: circle, torus (manifolds); basic motion planning problem (piano mover's); Degrees of freedom of a body and of a robot; Cartesian product of spaces; Explicit vs implicit C-space representations | new Maths Note: Rigid-body transforms and homogeneous coordinates, 69 | PA 4.8, PA 4.3, PA 4.4, PA 4.14, ME-012, idx:cartesian_product, idx:explicit_implicit_cspace | LaValle 2006 ch.4; MR 2.1–2.2; Correll et al., Intro to Autonomous Robots; LaValle, Planning Algorithms; Lynch & Park, Modern Robotics (book + lectures) |
| 73 | Obstacles in C-space | obstacle region and free space; Minkowski sum: growing obstacles by the robot's shape | 72, 71 | PA 4.12, PA 4.13 | LaValle 2006 ch.4 |
| 105 | Graphs and uninformed search | graph as a model of a state space; breadth-first and depth-first search; algorithm cost: Big-O and exponential time; why exact planning is hard (NP-hard, PSPACE-hard); Explicit vs implicit graphs; choosing a Markov search state |  | PA 2.1, PA 2.2, PA 2.9, PA 6.8, idx:implicit_graphs | LaValle 2006 ch.2; LaValle 2006 ch.6; CMU 16-350 |
| 106 | Dijkstra's algorithm and priority queues | priority queue; Dijkstra's shortest-path algorithm | 105 | PA 2.3, PA 2.4 | LaValle 2006 ch.2 |
| 107 | A* and heuristics | A* search with an admissible heuristic; best-first search and iterative deepening; backward and bidirectional search; weighted A*, anytime A* (ARA*) and any-angle search (Theta*) named as variants; Consistent (monotone) heuristics; Multi-goal A* (virtual goal; moving targets); Jump point search | 106 | PA 2.5, PA 2.6, PA 2.7, idx:consistent_heuristics, idx:multigoal_astar, idx:jps | LaValle 2006 ch.2; Kochenderfer et al., Algorithms for Decision Making; CMU 16-350; UCSD ECE276B |
| 108 | Grid path planning: wavefronts, navigation functions and value iteration | value iteration on a robot grid map; DP with interpolation on continuous spaces; feedback planning by DP with interpolation; navigation function with one minimum at the goal; grid wavefront propagation; Grid connectivity: 4- and 8-connected; Fast marching method and the Eikonal equation | 14, 98, ML-043, 106 | PR 14.7, PA 8.7, PA 14.7, PA 8.2, idx:grid_connectivity, idx:fast_marching | Thrun et al. 2005 ch.14; LaValle 2006 ch.8; LaValle 2006 ch.14; LaValle, Planning Algorithms; Lynch & Park, Modern Robotics (book + lectures); Szeliski, Computer Vision |
| 109 | Moving through unknown maps: D* replanning and bug algorithms | D* fast replanning; bug algorithms in unknown spaces; D* Lite, named; Real-time heuristic search (LRTA*, RTAA*) | 107, 98, 9 | PA 12.4, PA 12.5, idx:rt_heuristic_search | LaValle 2006 ch.12; CMU 16-350; UCSD ECE276B |
| 110 | Collision checking and nearest neighbours in C-space | collision detection: broad and narrow phase; bounding-volume hierarchies; metric space: rules a distance must follow; distances on angles; kd-tree nearest-neighbour search with wrap-around angles; uniform random samples of rotations and directions; Distance queries between bodies (GJK named); Checking a path segment for collision (edge resolution); Self-collision checking | 73, 72, ML-085, MA-049, MA-029 | PA 5.7, PA 5.8, PA 5.1, PA 5.9, PA 5.3, idx:distance_queries, idx:edge_collision, idx:self_collision | LaValle 2006 ch.5; LaValle, Planning Algorithms; Lynch & Park, Modern Robotics (book + lectures) |

#### RO-17 Sampling-based, car-like and manipulation planning



| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 111 | Potential fields | randomized potential fields: roll downhill, random-walk out of local minima; Artificial potential fields: attractive and repulsive terms; Harmonic potential fields from Laplace's equation (no local minima); Navigation functions (Rimon-Koditschek) | 73, MA-062, new Maths Note: The Laplacian and Laplace's equation, 108 | PA 5.11, idx:artificial_potential_fields, idx:harmonic_potential, idx:navigation_functions | LaValle 2006 ch.5; LaValle, Planning Algorithms; Lynch & Park, Modern Robotics (book + lectures); Szeliski, Computer Vision |
| 112 | Rapidly-exploring random trees (RRT) | rapidly-exploring random tree; RRT* and asymptotic optimality; PRM*, FMT* and SST* named; Bidirectional RRT (RRT-Connect) | 110 | PA 5.12, idx:rrt_connect | LaValle 2006 ch.5; CMU 16-350; LaValle, Planning Algorithms; Lynch & Park, Modern Robotics (book + lectures) |
| 113 | Probabilistic roadmaps (PRM) | probabilistic and visibility roadmaps; complete, resolution-complete and probabilistically complete planners; Single-query vs multi-query planners; Roadmap requirements: accessibility and connectivity; Narrow passages and PRM sampling strategies; Lazy collision checking | 112, 105 | PA 5.13, PA 5.14, idx:single_multi_query, idx:roadmap_props, idx:narrow_passages, idx:lazy_collision | LaValle 2006 ch.5; Correll et al., Intro to Autonomous Robots; LaValle, Planning Algorithms; Lynch & Park, Modern Robotics (book + lectures) |
| 114 | Planning with motion limits | kinodynamic planning and phase-space obstacles; reachable sets; motion primitives and a system simulator; lattice search; kinodynamic RRT; Dubins and Reeds-Shepp shortest car paths; Dubins and Reeds-Shepp curves; Kinodynamic planning; Inevitable collision states | 112, 64, new Maths Note: Numerical integration of ODEs, new Maths Note: ODEs and vector fields | PA 14.1, PA 14.2, PA 14.4, PA 14.5, PA 14.6, PA 15.9, CT-095, CT-096, idx:ics | LaValle 2006 ch.14; LaValle 2006 ch.15; robotics.md (PA 15.9); robotics.md (PA 14.1–14.6); LaValle, Planning Algorithms |
| 115 | Hybrid A* and path smoothing | F2 Hybrid A*: A* whose nodes carry heading and whose edges are drivable arcs; F6 Path smoothing after a grid planner | 107, 114, 67, 100 | AU-026, AU-030 | Dolgov et al. 2010, *Path planning for autonomous vehicles in unknown semi-structured environments* ([10.1177/0278364909359210](https://doi.org/10.1177/0278364909359210)); NAV2 SmacPlannerHybrid; UDS C5; CMU wk 14–15; NAV2 Smoothers (simple, constrained, Savitzky-Golay) |
| 116 | State lattices and motion primitives | F3 State-lattice planning with motion primitives | 115 | AU-027 | Pivtoraiko & Kelly 2009, *state lattices* ([10.1002/rob.20285](https://doi.org/10.1002/rob.20285)); NAV2 SmacPlannerLattice; CMU wk 14–15 |
| 117 | Route planning on road and route graphs | B4 Route (mission) planning on a road or route graph; lane graphs as the road-network graph | 107, 65 | AU-014 | TOR C4 M4; S2 §II-A; S3 "route planning"; NAV2 Route Server; AW mission planner |
| 118 | Trajectory optimisation | gradient-based trajectory optimisation (shooting); Trajectory optimisation (gradient-based, shooting); Direct methods: single shooting, multiple shooting, collocation; Trajectory optimisation methods: multiple shooting, collocation, DDP/iLQR; direct vs indirect methods; Pontryagin's principle named only | 114, ML-056 | PA 14.9, CT-097, CT-072, ME-054 | LaValle 2006 ch.14; robotics.md (PA 14.9); MPC 8.5, WE22 V.A, PA16 IV.C; PA 14.9; Wensing V-A–V-C |
| 313 | Manipulation planning | transit and transfer moves; preimage planning and nonprehensile manipulation (pushing); Manipulation beyond grasping: pushing, nonprehensile; Manipulation planning (transit and transfer); Quasistatic assumption; Motion-planning libraries: MoveIt and OMPL | 113, 69 | PA 7.4, PA 12.7, ME-086, ME-087, idx:quasistatic, idx:moveit_ompl | LaValle 2006 ch.7; LaValle 2006 ch.12; MR 12.3; PA 7.4; LaValle, Planning Algorithms; Lynch & Park, Modern Robotics (book + lectures) |
| 314 | Symbolic task planning: STRIPS and PDDL | Symbolic task planning: STRIPS/PDDL, forward search | 105, 107 | idx:strips_pddl | CMU 16-350; Correll et al., Intro to Autonomous Robots; LaValle, Planning Algorithms; MIT 16.410 |
| 315 | Task and motion planning | K3b Task-level planning: task and motion planning, language models choosing skills | 313, 139 | AU-049 | M42 ch.5 "Programming the task level"; Garrett et al. 2021, TAMP ([arXiv 2010.01083](https://arxiv.org/abs/2010.01083)); Ahn et al. 2022, SayCan ([arXiv 2204.01691](https://arxiv.org/abs/2204.01691)) |

#### RO-18 The classical navigation stack

Putting the parts together: the layered stack, ROS 2, simulators, DWA/TEB, behaviour trees and Nav2.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 135 | The autonomy stack: layers, rates and sensor choice | A2 The autonomy stack: sense–plan–act and the layers mission → behaviour → motion → control; A8 Choosing and placing sensors: coverage, range, redundancy, compute budget; Reactive control and behaviour-based robotics (Braitenberg, subsumption) | 97, 108, 134 | AU-002, AU-009, idx:reactive_behaviour | TOR C1 M2 L3, C4 M2; CMU wk 10 "hierarchical control"; S1 ch.1; S2 §II; S3; AW architecture; TOR C1 M2 L1–L2; ETH wk 4; Correll et al., Intro to Autonomous Robots; Wikipedia (glossary/outline pages) |
| 136 | ROS 2: nodes, topics, services and actions | A3 ROS 2: nodes, topics, services, actions, parameters, launch, QoS, lifecycle nodes, bags, RViz | 135, 65 | AU-004 | NAV2 concepts "ROS 2"; UDR C3; Macenski et al. 2022, *Robot Operating System 2*, Sci. Robotics ([10.1126/scirobotics.abm6074](https://doi.org/10.1126/scirobotics.abm6074)); [ROS 2 concepts](https://docs.ros.org/en/jazzy/Concepts.html) |
| 137 | Physics simulators: time steps, contact and the main engines | J2 How a physics simulator steps: time step, contact and friction models; choosing Gazebo vs MuJoCo vs Isaac vs Drake | 70, new Maths Note: Numerical integration of ODEs | AU-043 | M42 ch.5 "Contact simulation"; COR "Simulation"; M832 App. A (Drake, [drake.mit.edu](https://drake.mit.edu/)); [Gazebo docs](https://gazebosim.org/docs); [Isaac Sim docs](https://docs.isaacsim.omniverse.nvidia.com/latest/index.html); RL scope row R0.9 |
| 138 | Classical local planning: DWA and TEB | dynamic window approach: sample reachable velocities, score short trajectories; timed elastic band: optimise a timed path; Local planners as controllers (DWA, TEB) | 118, 98, 64, 100 | N.1, CT-055 | Fox, Burgard & Thrun 1997; Rosmann et al. 2017; robotics.md (RL N.1) |
| 139 | Behaviour trees, state machines and recovery behaviours | A5 Behaviour trees (sequence, fallback, decorator, tick) and finite state machines; A6 Recovery behaviours, goal and progress checks, waypoint following | 135, 136 | AU-006, AU-007 | NAV2 concepts "Behavior Trees"; Colledanchise & Ögren, *Behavior Trees in Robotics and AI* ([arXiv 1709.00084](https://arxiv.org/abs/1709.00084)); NAV2 plugins: Behaviors, Goal Checkers, Progress Checkers, Waypoint Task Executors |
| 140 | The Nav2 navigation stack and ROS tooling | Nav2: global planner, costmaps, AMCL localization, DWB and MPPI controllers; navigation simulators and tooling: Gazebo + ROS, Isaac Lab, Habitat, Flightmare, CrowdNav; Classical stack: global planner + local planner; MPPI and regulated pure pursuit named as Nav2 controllers | 138, 97, 107, 136, 139, 100, 131, 137 | N.26, RL §5.1 decision 2026-10-03 'The Nav2 navigation stack' (second background Note), RS-024 | Macenski et al. 2020; Nav2 docs; Koenig & Howard 2004; Savva et al. 2019; Song et al. 2020 (Flightmare); CrowdNav repo; Xiao §2 |

#### RO-19 Navigation I: the learned navigation policy

Replace the local planner with a learned policy: task, observations, actions, rewards, evaluation.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 162 | POMDPs and belief space | partially observable MDP; planning in belief / information space; observations, state and the state-update function; robot control as a POMDP | 11, 78 | PR 15.1, PA 11.6, PA 12.1, SB17.3, R3.1 | Thrun et al. 2005 ch.15; LaValle 2006 ch.11; LaValle 2006 ch.12; Sutton&Barto 2018 ch.17; Lee et al. 2020 |
| 163 | Learned vs classical local planners | what RL buys and costs vs DWA/TEB; Learning only the local planner; Hybrid learned-plus-classical systems for safety and explainability; learning that duplicates, replaces or improves a classical part | 138, 141 | N.2, RS-026, RS-030 | Xiao et al. 2022; Kahn et al. 2018; Song et al. 2023; Xiao §3.2.2; Xiao §6.2 |
| 164 | Navigation as an MDP or POMDP | point-goal, object-goal and image-goal tasks; termination and time limit; fixed vs moving goals; geometric vs non-geometric sensing | 163, 162, 142 | N.3 | Anderson et al. 2018; Savva et al. 2019 |
| 165 | Mapless end-to-end navigation | laser ranges + goal to velocity commands, no map; Learning the whole stack end to end (mapless) | 164, 40 | N.4, RS-025 | Tai, Paolo & Liu 2017; Zhu & Zhang 2021; Xiao §3.1; Zhu & Zhang |
| 166 | Observations for navigation: laser, vision and maps | down-sampled ranges, goal in robot frame, stacked scans; RGB/depth, target image, egocentric occupancy or costmap | 165, 151, 152, DL-040 | N.5, N.6 | Tai et al. 2017; Long et al. 2018; Zhu et al. 2017; Chaplot et al. 2020; Hoeller et al. 2021 |
| 167 | Action spaces for navigation | (v, omega), discrete moves, waypoints, commands to a locomotion policy | 165, 143 | N.7 | Tai et al. 2017; Wijmans et al. 2020; Lee et al. 2024 |
| 168 | Reward design for navigation | arrival, progress, collision, time and smoothness terms | 167, 155 | N.8 | Tai et al. 2017; Long et al. 2018 |
| 169 | Sparse, time-limited goal rewards | reward only for being at the target at the end of a time budget | 168, 159 | N.9 | Rudin et al. 2022b |
| 170 | Evaluating navigation: success, SPL, collisions | success rate, SPL, collisions and time; K2 Navigation benchmarks and protocols: BARN, Habitat challenges, social-navigation metrics; H3 Ground truth: motion capture and how pose error is measured; Judging real-world success: lab vs diverse real settings; reproducible real benchmarks | 164 | N.19, AU-046, AU-036, RS-014 | Anderson et al. 2018; Wijmans et al. 2020; Perille et al. 2020, BARN ([arXiv 2008.13315](https://arxiv.org/abs/2008.13315)); Batra et al. 2020, ObjectNav ([arXiv 2006.13171](https://arxiv.org/abs/2006.13171)); Francis et al. 2023, social navigation evaluation ([arXiv 2306.16740](https://arxiv.org/abs/2306.16740)); ETH wk 4 "Motion capture systems"; Tang §3.4, §5 |

#### RO-20 Navigation II: exploring, remembering and learning parts of the stack

Long-range navigation: exploration, memory, options, object goals, topological maps, and learned costmaps, planner parameters and planners.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 189 | Exploration by information gain and active localization | expected information gain of an action; greedy and multi-step exploration; Monte Carlo exploration; moving to become sure of the pose; active SLAM: choosing motions that improve the map | 162, 82, ML-091, 97 | PR 17.1, PR 17.2, PR 17.3, PR 17.4 | Thrun et al. 2005 ch.17 |
| 190 | Exploring to build a map | exploration for occupancy grids (cell entropy, gain spread by value iteration); Frontier-based exploration | 189, 108 | PR 17.5, idx:frontier_exploration | Thrun et al. 2005 ch.17; Stanford AA274A |
| 191 | Curiosity and intrinsic rewards for exploration | K6 Curiosity and intrinsic rewards for exploration; Visual exploration: cover a new house fast (coverage, curiosity, novelty rewards) | 190, 39, 4 | AU-051, RS-037 | Pathak et al. 2017, ICM ([arXiv 1705.05363](https://arxiv.org/abs/1705.05363)); Burda et al. 2018, RND ([arXiv 1810.12894](https://arxiv.org/abs/1810.12894)); Duan §III-A |
| 192 | Memory and auxiliary tasks for visual navigation | recurrent navigation policy with depth and loop-closure prediction | 166, 179 | N.10 | Mirowski et al. 2017; Zhu et al. 2017 |
| 193 | Options: temporal abstraction | options as temporally extended actions; Long-horizon tasks by composing skills (hierarchical RL); Option models and planning with options | 167, 7, 10 | SB17.2, RS-018, idx:option_models | Sutton&Barto 2018 ch.17; Tang §5; Kroemer §8; Sutton & Barto, RL |
| 194 | Planners plus RL | roadmap edges kept only if the RL policy can drive them (PRM-RL) | 113, 165, 193 | N.15 | Faust et al. 2018; Francis et al. 2020 |
| 195 | Modular learned navigation vs end-to-end | learned SLAM + global and local policies + analytic planner | 194, 98, 190 | N.17 | Chaplot et al. 2020 |
| 196 | Object-goal navigation with a semantic map | Embodied goal types: PointNav, ImageNav, ObjectNav; Object-goal navigation by a semantic map + exploration policy (modular) | 195, 186, 164 | RS-038, RS-039 | Duan §III-B; Tang §4.2.1; Sun (ObjectNav) |
| 197 | Topological maps: navigating over a graph of places | Topological maps: navigate over a graph of places | 195, 105 | RS-043 | Gu VLN §4.1.3; Firoozi §III-F |
| 198 | Inverse RL: recovering a reward from demonstrations | Inverse RL: recover the reward from demos (max-entropy IRL); I3 Inverse RL and adversarial imitation (GAIL); Apprenticeship learning by matching feature expectations | 174, 155, 14, ML-091 | RS-066, AU-039, idx:apprenticeship_learning | Ravichandar §3.2.2; Zare §III; Ho & Ermon 2016, GAIL ([arXiv 1606.03476](https://arxiv.org/abs/1606.03476)); COR "Reward shaping and learning"; S237B wk 7–8; Kochenderfer et al., Algorithms for Decision Making |
| 199 | Learned costmaps and learned planner parameters | Learned costmaps from demonstrations (inverse RL for navigation); Learning planner parameters (tune DWA/TEB settings from demos or RL) | 198, 138, 100 | RS-028, RS-029 | Xiao §3.3.1; Xiao §3.3.2, §6.2 |
| 200 | Learned global planners: value iteration networks and neural A* | Learning the global planner: learned heuristics, planning as a network (value iteration networks, neural A*) | 108, 14, DL-040 | RS-027 | Xiao §3.2.1 |

#### RO-21 Navigation III: people, crowds and the real world

Many agents and people, billions of frames, real-robot data, sim-to-real, safety, and fast flight from quadrotor control to learned agile flight.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 222 | Multi-agent collision avoidance and social norms | value network over joint configuration (CADRL); social norms in the reward; Multi-robot and crowd navigation with RL | 164, 25 | N.11, N.12, RS-032 | Chen et al. 2017 (CADRL, SA-CADRL); Zhu & Zhang; Tang §4.6.1 |
| 223 | Crowds and robot teams: attention pooling and shared policies | summarising a variable set of neighbours; one PPO policy for every robot; multi-stage training | 222, DL-061, DL-073, 39 | N.13, N.14 | Everett et al. 2018; Chen et al. 2019 (SARL); Long et al. 2018 |
| 224 | Multi-agent RL: centralised training, decentralised execution | G3 Multi-agent RL: centralised training with decentralised execution, shared policies, value factorisation; Multi-robot RL: decentralised agents, centralised training (CTDE, MAPPO); Dec-POMDP; Markov (stochastic) games | 223, 39, 173, 162 | AU-033, RS-017, idx:dec_pomdp, idx:markov_games | Rashid et al. 2018 QMIX ([arXiv 1803.11485](https://arxiv.org/abs/1803.11485)); Yu et al. 2022 MAPPO ([arXiv 2103.01955](https://arxiv.org/abs/2103.01955)); Tang §4.6; Gu safe §3.3; Kochenderfer et al., Algorithms for Decision Making |
| 225 | Social navigation: norms, coupled prediction and planning, evaluation | Coupled prediction and planning (the robot's move changes theirs); Social norms: personal space (proxemics), legibility, groups; Evaluating social navigation: metrics and protocols; E3 Interaction-aware planning: my plan changes their behaviour | 222, 188 | RS-034, RS-035, RS-036, AU-024 | Mavrogiannis §3.2; Mavrogiannis §4; Singamaneni; Mavrogiannis §5; S237B wk 9 "Interaction-aware learning, planning and control" |
| 226 | Navigation at scale | photoreal simulators and distributed PPO to billions of frames (DD-PPO); Embodied AI simulators: Habitat, iGibson, AI2-THOR | 140, 144 | N.18, RS-044 | Savva et al. 2019; Wijmans et al. 2020; Duan §II |
| 227 | Self-supervised real-world navigation | labels from the robot's own events (collision, bumpiness) | 149, 164 | N.20 | Kahn et al. 2018; Kahn et al. 2021 (BADGR); Gandhi et al. 2017 |
| 228 | Sim-to-real for navigation | randomised rendering, laser-only inputs, measured sim-real agreement | 146, 149, 166 | N.21 | Sadeghi & Levine 2017; Tai et al. 2017; Kadian et al. 2020 |
| 229 | Safety in navigation | collision limits as constraints, shields and recovery for navigation; Safe locomotion and safety filters | 206, 205, 168 | N.25, RS-057 | He et al. 2024; Alshiekh et al. 2018; Ha §8.4 |

#### RO-22 Navigation with language and foundation models

Open-vocabulary goals and spoken routes: vision-language models, language-queryable maps, zero-shot ObjectNav, VLN, navigation foundation models.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 252 | Vision-language models for robots | Vision-language models (CLIP-style image-text matching) | DL-071, new Deep Learning Note: Contrastive learning objective, DL-053 | RS-109 | Firoozi §II-D |
| 253 | Neural radiance fields and Gaussian splatting for robot maps | Neural radiance fields and 3D Gaussian splatting | 247, DL-010 | idx:nerf_gs | Stanford CS231A Computer Vision |
| 254 | Open-vocabulary 3D semantic maps | Open-vocabulary 3D semantic maps (language-queryable maps) | 252, 186 | RS-112 | Firoozi §IV-C |
| 255 | Zero-shot object navigation with vision-language models | Zero-shot, open-vocabulary navigation with vision-language models | 254, 196 | RS-040 | Sun (ObjectNav); Firoozi §III-F |
| 256 | Vision-and-language navigation: task, datasets and metrics | K7 Vision-and-language navigation; Vision-and-language navigation: task, R2R dataset, metrics | 164, 252, DL-083 | AU-052, RS-041 | Anderson et al. 2018, VLN ([arXiv 1711.07280](https://arxiv.org/abs/1711.07280)); Gu VLN §2-3 |
| 257 | Vision-and-language navigation methods | VLN methods: cross-modal attention, graph memory, data augmentation (speaker-follower) | 256, 197 | RS-042 | Gu VLN §4 |
| 258 | Navigation foundation models | goal-conditioned navigation models from many robots (GNM, ViNT); diffusion policy (NoMaD); Navigation foundation models | 164, 197, 252, 174, new Deep Learning Note: Diffusion models | N.27, RS-120 | Shah et al. 2023 (GNM, ViNT); Sridhar et al. 2024 (NoMaD); Tang §5 |

#### RO-23 Autonomous driving

Navigation for cars: automation levels, HD maps, behaviour planning, Frenet planning, system safety, open- vs closed-loop evaluation.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 259 | Driving automation levels and modular vs end-to-end stacks | A1 Levels of driving automation and the operating domain (ODD); A2b Modular vs end-to-end stacks for driving | 135, 195 | AU-001, AU-003 | TOR C1 M1; SAE J3016 ([sae.org](https://www.sae.org/standards/content/j3016_202104/)); S3; S4 §III; Chen et al. 2023 [arXiv 2306.16927](https://arxiv.org/abs/2306.16927) |
| 260 | HD and vector maps | B3 HD / vector maps: lanes as a graph with rules attached; point-cloud maps | 117, 65 | AU-013 | AW map design (vector map: lanes, crosswalks, stop lines, traffic lights); S3 "road mapping"; Poggenhans et al. 2018, *Lanelet2* ([10.1109/ITSC.2018.8569929](https://doi.org/10.1109/ITSC.2018.8569929)) |
| 261 | Behaviour planning for driving | F1 Behaviour planning: lane keep, lane change, yield, stop, using rules and state machines | 139, 260, 188 | AU-025 | TOR C4 M6; UDS C5; S2 §II-B; S3 "behavior selection"; AW behaviour path/velocity planners |
| 262 | Frenet-frame trajectory planning | F4 Frenet-frame planning: sample lateral and longitudinal curves along the lane, then pick the cheapest | 130, 211, 212, 261 | AU-028 | Werling et al. 2010, *Optimal trajectory generation … in a Frenét frame* ([10.1109/ROBOT.2010.5509799](https://doi.org/10.1109/ROBOT.2010.5509799)); UDS C5; TOR C4 M8 |
| 263 | System safety: monitoring, fail-safe stops and safety cases | A7 System monitoring, fail-safe and the minimal-risk manoeuvre; A9 Safety assurance: hazard analysis, functional safety (ISO 26262), scenario testing | 206, 135 | AU-008, AU-010 | AW AD-API fail-safe / diagnostics / operation modes; AW planning "Validation"; TOR C1 M3 (safety assurance, frameworks, testing); UDS C13 (functional safety, hazard analysis and risk assessment) |
| 264 | Evaluating driving: open vs closed loop, simulators and scenarios | J3 Driving simulators and scenario-based testing; K3 Open-loop vs closed-loop evaluation of driving planners; Falsification: searching for disturbances that make a policy fail | 188, 137, 170 | AU-044, AU-047, idx:falsification | TOR C1 M7, C4 final project; Dosovitskiy et al. 2017 CARLA ([arXiv 1711.03938](https://arxiv.org/abs/1711.03938)); Caesar et al. 2021, nuPlan ([arXiv 2106.11810](https://arxiv.org/abs/2106.11810)); CARLA leaderboard ([leaderboard.carla.org](https://leaderboard.carla.org/)); Chen et al. 2023; Kochenderfer et al., Algorithms for Decision Making |

#### RO-24 Planning in depth *(optional)*

Optional: exact POMDP planning, exact roadmaps, time and many robots, coverage, task allocation.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 284 | Exact POMDP planning: alpha vectors | piecewise-linear convex value function (alpha vectors); value iteration in belief space; pruning value-function pieces; Point-based value iteration | 162, 14 | PR 15.2, PR 15.3, PR 15.4, idx:pbvi | Thrun et al. 2005 ch.15; Kochenderfer et al., Algorithms for Decision Making |
| 285 | Approximate POMDP planning | QMDP; augmented MDP (mean + entropy summary); Monte Carlo POMDP with particle beliefs; Online POMDP planning by tree search (POMCP) | 284, 82, 48 | PR 16.1, PR 16.2, PR 16.3, idx:pomcp | Thrun et al. 2005 ch.16; Kochenderfer et al., Algorithms for Decision Making |
| 286 | Exact roadmaps | vertical cell decomposition; maximum-clearance roadmap (generalized Voronoi diagram); shortest-path roadmap (visibility graph) | 73, 107 | PA 6.1, PA 6.2, PA 6.3 | LaValle 2006 ch.6 |
| 287 | Consensus: agreement over a graph | Consensus (agreement) dynamics: x' = -Lx and averaging x(k+1) = A x(k) | new Maths Note: The graph Laplacian, new Maths Note: Stability of dynamical systems | idx:consensus | Bullo, Lectures on Network Systems; Åström & Murray, Feedback Systems |
| 288 | Formation control and swarms | Multi-robot coordination by consensus: rendezvous, formation control, cyclic pursuit, deployment, swarms | 287 | idx:multirobot_formation | Bullo, Lectures on Network Systems; Wikipedia (glossary/outline pages) |
| 289 | Planning with time and many robots | time-varying obstacles and velocity tuning; centralized vs decoupled (prioritized) multi-robot planning; decoupled planning: path first, then timing | 113, 114 | PA 7.1, PA 7.2, PA 14.8 | LaValle 2006 ch.7; LaValle 2006 ch.14 |
| 290 | Multi-agent path finding | G1 Multi-agent path finding: prioritised planning, conflict-based search | 289, 107 | AU-031 | Stern et al. 2019, *Multi-Agent Pathfinding* ([arXiv 1906.08291](https://arxiv.org/abs/1906.08291)); Sharon et al. 2015, *Conflict-based search* ([10.1016/j.artint.2014.11.006](https://doi.org/10.1016/j.artint.2014.11.006)) |
| 291 | Coverage planning | coverage planning: visit every part of an area; Spanning-tree coverage; Boustrophedon (lawnmower) coverage | 286, new Maths Note: Graphs and their matrices: adjacency, degree, paths and connectivity | PA 7.7, idx:spanning_tree_coverage, idx:boustrophedon | LaValle 2006 ch.7; LaValle, Planning Algorithms |
| 292 | Task allocation and fleet management | G2 Task allocation and fleet management: auctions, assignment; Travelling salesman problem | 290, new Maths Note: Assignment problem (Hungarian algorithm), new Maths Note: Mixed-integer programming and branch and bound | AU-032, idx:tsp | Gerkey & Matarić 2004, *Task allocation in multi-robot systems* ([10.1177/0278364904045564](https://doi.org/10.1177/0278364904045564)); Open-RMF ([docs](https://openrmf.readthedocs.io/en/latest/)); Correll et al., Intro to Autonomous Robots; LaValle, Planning Algorithms; Szeliski, Computer Vision |

## 4. New prerequisite Notes (49)

These are new Maths/Machine Learning/Deep Learning Notes. Each must be written before its first user. They include a new Maths chapter, **Maths (MA) 09 Signals and systems** (LTI systems and convolution → Fourier → sampling and aliasing → Laplace → z-transform → digital filters → random processes).

**A new Deep Learning chapter, "Generative models for control",** is needed: VAE, contrastive loss, diffusion, flow matching, GANs and CLIP-style image–text pretraining. No Deep Learning Note teaches them: DL-001 says generative networks are not covered, and DL-003 gives GANs and autoencoders only a short paragraph. The reparameterization trick lives in the VAE Note, where it first appeared (Kingma & Welling 2014, arXiv 1312.6114); SAC recaps it.

| Chapter | Note | Teaches | Builds on | First user (Note) | Sources |
|---|---|---|---|---|---|
| Maths 02-probability | Markov chains | Markov property / Markov assumption, transition matrix, stationary distribution; Irreducible and aperiodic Markov chains converge to one stationary distribution | MA-019 | 7 | Sutton&Barto 2018; Thrun et al. 2005; Bullo, Lectures on Network Systems |
| Maths 02-probability | Bayesian networks | Bayesian networks: a joint distribution as a product of local conditionals; conditional independence, Markov blanket, ancestral sampling | MA-014, MA-016, MA-019, new Maths Note: Markov chains | 77 | Georgia Tech CS 3630; Kochenderfer et al., Algorithms for Decision Making; Prince, Computer Vision: Models, Learning, Inference |
| Maths 03-distributions | Drawing samples from distributions | sampling recipes, triangular distribution |  | 68 | Thrun et al. 2005 |
| Maths 04-inference | Monte Carlo estimation | estimate an expectation by averaging random samples; a sample set stands for a distribution | MA-034 | 16 | Sutton&Barto 2018; Thrun et al. 2005 |
| Maths 04-inference | Importance sampling | target, proposal, weights; ordinary vs weighted; variance | new Maths Note: Monte Carlo estimation | 18 | LaValle 2006; Sutton&Barto 2018; Thrun et al. 2005 |
| Maths 04-inference | Bootstrap confidence intervals and the interquartile mean | error bars from resampling a few seeds; a mean robust to outlier runs | MA-035 | 44 | plan §4 (new maths) |
| Maths 05-linear-algebra | Cross product and skew-symmetric matrix | a x b written as [a]x b; Right-handed frames and the right-hand rule | MA-050 | 85 | robotics.md rows PE-033, ME-006; Lynch & Park, Modern Robotics (book + lectures) |
| Maths 05-linear-algebra | Rigid-body transforms and homogeneous coordinates | rotate + translate, homogeneous matrix, SE(2)/SE(3), heading angles kept in -pi..pi; 2D rotation by any angle (cos, sin), headings kept in -pi..pi (MA-053 shows only the 90-degree case); Inverse and composition of poses with homogeneous matrices; atan2, the two-argument arctangent; Trigonometry basics: right triangles, sin/cos/tan, identities, inverse functions | MA-054, MA-049 | 64 | LaValle 2006; Thrun et al. 2005; Barfoot, State Estimation for Robotics; LaValle, Planning Algorithms; Lynch & Park, Modern Robotics (book + lectures); Correll et al., Intro to Autonomous Robots |
| Maths 05-linear-algebra | 3D rotations: Euler angles and quaternions | yaw, pitch, roll; quaternions; Quaternion algebra: conjugate, product, rotating a vector; Rotation facts: det +1 (proper vs improper), rotations do not commute, gimbal lock, q and -q are the same rotation; Fixed-axis vs moving-axis (extrinsic vs intrinsic) rotation order | new Maths Note: Rigid-body transforms and homogeneous coordinates | 65 | LaValle 2006; Correll et al., Intro to Autonomous Robots; Barfoot, State Estimation for Robotics; Szeliski, Computer Vision |
| Maths 05-linear-algebra | Axis-angle, exponential and log maps of rotations | any rotation as one turn about one axis; rotation vector to and from rotation matrix (SO(3) exp/log, beginner level) | new Maths Note: 3D rotations: Euler angles and quaternions | 85 | robotics.md rows ME-007, PE-087 |
| Maths 05-linear-algebra | Graphs and their matrices: adjacency, degree, paths and connectivity | Graph basics: directed/undirected and weighted graphs, degree, neighbours, paths, cycles, trees, connectivity and connected components, adjacency matrix | MA-053, MA-056 | 238 | Bullo, Lectures on Network Systems; Kochenderfer & Wheeler, Algorithms for Optimization; Kochenderfer et al., Algorithms for Decision Making; Lynch & Park, Modern Robotics (book + lectures); Åström & Murray, Feedback Systems |
| Maths 05-linear-algebra | The graph Laplacian | Graph Laplacian L = D - A: incidence matrix, quadratic form x^T L x, eigenvalues, algebraic connectivity; Non-negative and row-stochastic matrices: eigenvalue 1, left eigenvector, Perron-Frobenius statement | new Maths Note: Graphs and their matrices: adjacency, degree, paths and connectivity, MA-056, new Maths Note: Markov chains | 287 | Bullo, Lectures on Network Systems; Åström & Murray, Feedback Systems |
| Maths 05-linear-algebra | Null-space projector and weighted pseudo-inverse | N = I - J+J; pseudo-inverse weighted by a mass matrix | MA-060 | 296 | plan §4 (new maths) |
| Maths 05-linear-algebra | Cholesky factor | matrix square root, needed for sigma points | MA-060 | 38 | Thrun et al. 2005 |
| Maths 05-linear-algebra | Mahalanobis distance | distance scaled by a covariance; gating; Whitening transform: decorrelate data with the covariance | new Maths Note: Cholesky factor | 187 | Thrun et al. 2005; Prince, Computer Vision: Models, Learning, Inference; Szeliski, Computer Vision |
| Maths 05-linear-algebra | Woodbury identity | inverse of matrix plus low-rank change | MA-060 | 272 | Thrun et al. 2005 |
| Maths 05-linear-algebra | Schur complement | marginalising variables out of a block matrix | MA-060 | 80 | Thrun et al. 2005 |
| Maths 05-linear-algebra | Sparse linear solves and conjugate gradient | sparse systems, relaxation, conjugate gradient; also used by TRPO | new Maths Note: Cholesky factor | 38 | Thrun et al. 2005 |
| Maths 06-calculus | Geometric series | sum of r^k = 1/(1-r) for \|r\|<1; Neumann series (I - A)^-1 = sum of A^k | MA-056 | 8 | Sutton&Barto 2018; Bullo, Lectures on Network Systems |
| Maths 06-calculus | The Laplacian and Laplace's equation | The Laplacian operator and Laplace's equation: sum of second derivatives, harmonic functions, solving on a grid | MA-064, MA-056 | 111 | LaValle, Planning Algorithms; Szeliski, Computer Vision |
| Maths 06-calculus | Integrals and the fundamental theorem of calculus | Integrals and the fundamental theorem of calculus | MA-061, MA-022 | 64 | Kochenderfer & Wheeler, Algorithms for Optimization; Kochenderfer et al., Algorithms for Decision Making |
| Maths 06-calculus | Complex numbers and Euler's formula | Complex numbers: real and imaginary parts, magnitude and angle, polar form, Euler's formula, the complex plane | MA-049, new Maths Note: Rigid-body transforms and homogeneous coordinates | 84 | Wikipedia (glossary/outline pages); Åström & Murray, Feedback Systems |
| Maths 06-calculus | ODEs and vector fields | an equation for change; following the arrows; Linear ODEs: homogeneous and particular solutions; The simple pendulum as the first nonlinear system: phase portrait, equilibria, damping, torque limits | new Maths Note: Integrals and the fundamental theorem of calculus | 64 | LaValle 2006; Lynch & Park, Modern Robotics (book + lectures); Wikipedia (glossary/outline pages); Tedrake, Underactuated Robotics (book + course + lectures) |
| Maths 06-calculus | Numerical integration of ODEs | Euler and Runge-Kutta steps; ODE solving basics: initial vs boundary value, explicit vs implicit integrators, stiffness, step size, local and global error | new Maths Note: ODEs and vector fields | 85 | LaValle 2006; Rawlings, Mayne & Diehl, MPC |
| Maths 06-calculus | State-space models | phase space, x_dot = Ax + Bu, nonlinear systems; discrete-time models x(k+1) = A x(k) + B u(k) by zero-order hold (CT-029); Control-affine systems: drift and control vector fields; The double integrator x'' = u (chain of integrators) | new Maths Note: ODEs and vector fields | 64 | LaValle 2006; LaValle, Planning Algorithms; Lynch & Park, Modern Robotics (book + lectures); Åström & Murray, Feedback Systems |
| Maths 06-calculus | Matrix exponential and logarithm | e^(At) solves x' = Ax; series definition; log as the inverse; gives Rodrigues' formula for rotations; Modes of a linear system: x' = Ax as a sum of eigenvector modes e^(lambda t) v | new Maths Note: ODEs and vector fields, MA-056, new Maths Note: Complex numbers and Euler's formula | 84 | robotics.md rows CT-028, ME-008; Bullo, Lectures on Network Systems; MIT 16.30 Feedback Control Systems; Åström & Murray, Feedback Systems |
| Maths 06-calculus | Stability of dynamical systems | equilibria, eigenvalues, Lyapunov functions; Stability definitions: equilibrium, Lyapunov, asymptotic and exponential stability, local vs global, region of attraction, stability by linearisation; Phase-plane equilibria: node, saddle, focus, centre from the eigenvalues of a planar system; Quadratic Lyapunov functions V = x^T P x and the Lyapunov equation A^T P + P A = -Q; LaSalle's invariance principle and invariant sets; Stability of x(k+1) = A x(k): all eigenvalues inside the unit circle | new Maths Note: State-space models, new Maths Note: Matrix exponential and logarithm, new Maths Note: Complex numbers and Euler's formula, MA-056, MA-064 | 84 | LaValle 2006; LaValle, Planning Algorithms; Murray, Li & Sastry, Robotic Manipulation; Rawlings, Mayne & Diehl, MPC; Tedrake, Underactuated Robotics (book + course + lectures); Wikipedia (glossary/outline pages); Åström & Murray, Feedback Systems; Bullo, Lectures on Network Systems |
| Maths 07-optimisation | Mixed-integer programming and branch and bound | Mixed-integer programming (MILP/MIQP): integer choices inside an LP/QP, why harder, branch and bound; use for footholds, contacts, routing | MA-068 | 292 | Kochenderfer & Wheeler, Algorithms for Optimization; Kochenderfer et al., Algorithms for Decision Making; MIT 16.410; Rawlings, Mayne & Diehl, MPC; Tedrake, Underactuated Robotics (book + course + lectures) |
| Maths 07-optimisation | Nonlinear least squares (Gauss-Newton) | re-linearise and re-solve in a loop; Weighted least squares: weight residuals by inverse noise covariance | MA-064, ML-053 | 103 | Thrun et al. 2005; Szeliski, Computer Vision |
| Maths 07-optimisation | Assignment problem (Hungarian algorithm) | match N tracks to M detections at least total cost | MA-068 | 187 | plan §4 (new maths) |
| Maths 08-likelihood | Bayesian estimation: posteriors and conjugate priors | Bayesian parameter learning: posterior over parameters, conjugate priors (Beta-Bernoulli, Dirichlet, normal-normal), predictive distribution, Bayesian linear regression | MA-072, MA-031 | 4 | Kochenderfer & Wheeler, Algorithms for Optimization; Kochenderfer et al., Algorithms for Decision Making; Prince, Computer Vision: Models, Learning, Inference |
| Maths 08-likelihood | KL divergence | what it measures, how to compute it | MA-072 | 38 | Sutton&Barto 2018; Thrun et al. 2005 |
| Maths 08-likelihood | Mutual information | how much knowing one variable tells about another; KL between joint and product | new Maths Note: KL divergence | 338 | plan §4 (new maths) |
| Maths 08-likelihood | Linear transforms of a Gaussian | mean A mu, covariance A Sigma A^T; Product of two Gaussians: completing the square; Conditioning a joint Gaussian: marginal, conditional mean and covariance from the block covariance | MA-073, new Maths Note: Schur complement | 80 | Thrun et al. 2005; Barfoot, State Estimation for Robotics; Deisenroth et al., Mathematics for ML; Prince, Computer Vision: Models, Learning, Inference; Rawlings, Mayne & Diehl, MPC |
| Maths 08-likelihood | Propagating uncertainty through a function | Uncertainty propagation through a function: Monte Carlo, linearisation, sigma points as one idea | new Maths Note: Monte Carlo estimation, new Maths Note: Linear transforms of a Gaussian, MA-063 | 81 | Kochenderfer & Wheeler, Algorithms for Optimization |
| Maths 08-likelihood | Lie groups for robot poses: perturbations and uncertainty on SO(3) and SE(3) | Matrix Lie groups SO(3)/SE(3) for estimation: group, Lie algebra, tangent-space perturbations, pose uncertainty | new Maths Note: Axis-angle, exponential and log maps of rotations, new Maths Note: Rigid-body transforms and homogeneous coordinates, MA-073 | 279 | Barfoot, State Estimation for Robotics; Michigan ROB 530; Prince, Computer Vision: Models, Learning, Inference; Szeliski, Computer Vision; UCSD ECE276A |
| Maths 09-signals-and-systems | Linear time-invariant systems: impulse response and convolution | Linear time-invariant systems: linearity, superposition, time invariance, impulse response, output = input convolved with the impulse response (1D and 2D) | new Maths Note: Stability of dynamical systems, new Maths Note: State-space models, new Maths Note: Matrix exponential and logarithm, new Maths Note: Integrals and the fundamental theorem of calculus, DL-042 | 84 | CMU 16-385 Computer Vision; Caltech CDS 110/ChE 105 Analysis and Design of Feedback Control Systems; LaValle, Planning Algorithms; MIT 16.30 Feedback Control Systems; MIT 2.004 Dynamics and Control II; Nayar, First Principles of CV; Rawlings, Mayne & Diehl, MPC; Szeliski, Computer Vision; Wikipedia (glossary/outline pages); Åström & Murray, Feedback Systems |
| Maths 09-signals-and-systems | Fourier series and the Fourier transform | Fourier series and the Fourier transform: frequency, magnitude and phase, convolution theorem, low/high/band-pass, power spectrum, DFT/FFT, 2D Fourier of images | new Maths Note: Complex numbers and Euler's formula, new Maths Note: Integrals and the fundamental theorem of calculus, new Maths Note: Linear time-invariant systems: impulse response and convolution | 84 | CMU 16-385 Computer Vision; Correll et al., Intro to Autonomous Robots; Kochenderfer & Wheeler, Algorithms for Optimization; LaValle, Planning Algorithms; Nayar, First Principles of CV; Szeliski, Computer Vision; Wikipedia (glossary/outline pages) |
| Maths 09-signals-and-systems | Sampling and aliasing | Sampling theorem (Nyquist rate) and aliasing; anti-alias filtering | new Maths Note: Fourier series and the Fourier transform | 127 | Nayar, First Principles of CV; Szeliski, Computer Vision |
| Maths 09-signals-and-systems | The Laplace transform | Laplace transform: transforms of step, impulse, exponential; derivative = multiply by s; transfer function as the transform of the impulse response; initial and final value theorems | new Maths Note: Integrals and the fundamental theorem of calculus, new Maths Note: Complex numbers and Euler's formula, new Maths Note: ODEs and vector fields, new Maths Note: Linear time-invariant systems: impulse response and convolution | 122 | Brunton, Control Bootcamp; Lynch & Park, Modern Robotics (book + lectures); MATLAB Tech Talks; MIT 2.004 Dynamics and Control II; Rawlings, Mayne & Diehl, MPC; Wikipedia (glossary/outline pages); Åström & Murray, Feedback Systems |
| Maths 09-signals-and-systems | The z-transform and discrete-time systems | Z-transform and discrete-time transfer functions | new Maths Note: The Laplace transform, new Maths Note: Sampling and aliasing | 127 | Brunton, Control Bootcamp; MATLAB Tech Talks; Rawlings, Mayne & Diehl, MPC; Stachniss lectures (Bonn); Wikipedia (glossary/outline pages) |
| Maths 09-signals-and-systems | Digital filters: moving average, low-pass, FIR and IIR | Discrete-time filters: moving average, first-order low-pass (IIR), FIR vs IIR, cutoff frequency | new Maths Note: Fourier series and the Fourier transform, DL-033, new Maths Note: The z-transform and discrete-time systems | 127 | Szeliski, Computer Vision |
| Maths 09-signals-and-systems | Random processes: white noise, random walks and noise density | Random processes: white noise and its power spectral density, random walk, Gauss-Markov process, continuous noise density to a discrete Q | new Maths Note: Fourier series and the Fourier transform, MA-024, new Maths Note: State-space models | 84 | Barfoot, State Estimation for Robotics; CMU 16-761; Prince, Computer Vision: Models, Learning, Inference |
| Machine Learning 07-classification | Gaussian processes | regression with a mean and an uncertainty at every input; Kernel (covariance) function and kernel matrix of a Gaussian process | ML-089, MA-073 | 209 | plan §4 (new maths); Barfoot, State Estimation for Robotics |
| Deep Learning Generative models (new chapter) | Variational autoencoder | reconstruction + beta KL; reparameterization; Conditional VAE: a VAE whose encoder and decoder see a condition (the observation); Variational inference and the ELBO | new Maths Note: KL divergence | 42 | Sutton&Barto 2018; Barfoot, State Estimation for Robotics; Berkeley CS 185/285 Deep Reinforcement Learning |
| Deep Learning Generative models (new chapter) | Contrastive learning objective | pull matching pairs together, push others apart |  | 177 | Sutton&Barto 2018 |
| Deep Learning Generative models (new chapter) | Generative adversarial networks | generator vs discriminator; the discriminator as a learned reward |  | 147 | plan §4 (new maths) |
| Deep Learning Generative models (new chapter) | Diffusion models | flagged unowned in RL scope 5 |  | 258 | plan §4 (new maths) |
| Deep Learning Generative models (new chapter) | Flow matching | flagged unowned in RL scope 5 |  | 375 | plan §4 (new maths) |

## 5. New sections in existing Maths/Machine Learning Notes (11)

| Note | Add | Sources |
|---|---|---|
| MA-056 | Repeated eigenvalues: algebraic vs geometric multiplicity, defective matrices, when a matrix is diagonalisable; Jordan form named; Trace of a matrix: sum of the diagonal = sum of the eigenvalues | Bullo, Lectures on Network Systems; Deisenroth et al., Mathematics for ML; Åström & Murray, Feedback Systems; Prince, Computer Vision: Models, Learning, Inference; Rawlings, Mayne & Diehl, MPC |
| MA-051 | Lines and planes in parametric form p = p0 + t d (affine subspace) | Deisenroth et al., Mathematics for ML |
| MA-049 | Vector norms L1, L2 and L-infinity; Manhattan, Euclidean and Chebyshev distance | Kochenderfer & Wheeler, Algorithms for Optimization; Kochenderfer et al., Algorithms for Decision Making; LaValle, Planning Algorithms |
| MA-060 | Left and right pseudo-inverse (tall vs wide matrices); Total least squares: fit a line or plane with errors in all coordinates by the last singular vector | Lynch & Park, Modern Robotics (book + lectures); Nayar, First Principles of CV; Szeliski, Computer Vision |
| MA-061 | Continuity of a function | LaValle, Planning Algorithms |
| MA-063 | Implicit function theorem; Automatic differentiation: forward and reverse mode | LaValle, Planning Algorithms; Kochenderfer & Wheeler, Algorithms for Optimization |
| MA-019 | Conditional expectation (law of total expectation) | LaValle, Planning Algorithms |
| MA-029 | Multivariate uniform distribution (uniform over a box) | Kochenderfer et al., Algorithms for Decision Making |
| ML-081 | Generative vs discriminative models | Prince, Computer Vision: Models, Learning, Inference |
| MA-068 | Second-order cone programs | Kochenderfer & Wheeler, Algorithms for Optimization |
| MA-064 | Line search and step-size rules: backtracking, Wolfe conditions, golden section | Barfoot, State Estimation for Robotics; Kochenderfer & Wheeler, Algorithms for Optimization; Kochenderfer et al., Algorithms for Decision Making; Prince, Computer Vision: Models, Learning, Inference |

## 6. Short maths sections inside Reinforcement Learning/Robotics Notes (29)

Each goes inside the Note that first needs it.

| Concept | What | Where | First needed by (Note) |
|---|---|---|---|
| Newtonian and rigid-body mechanics | F = ma, torque, inertia matrix, angular velocity | short RO section inside "PD and PID control" (mechanics is physics; CONTEXT.md defines MA as linear algebra, calculus, optimisation, probability, statistics) | 120 |
| Robbins-Monro step-size conditions |  | new maths: short section inside the RO Note that first uses it | 3 |
| Control variates (why a baseline cuts variance) |  | new maths: short section inside the RO Note that first uses it | 31 |
| Log-derivative trick |  | new maths: short section inside the RO Note that first uses it | 30 |
| Fourier basis features |  | new maths: short section inside the RO Note that first uses it | 26 |
| Natural gradient and Fisher information |  | new maths: short section inside the RO Note that first uses it | 38 |
| Priority queue and Big-O cost |  | new maths: short section inside the RO Note that first uses it | 106 |
| Canonical (information) form of a Gaussian |  | new maths: short section inside the RO Note that first uses it | 272 |
| Lyapunov functions |  | new maths: short section inside the RO Note that first uses it | 120 |
| Bradley-Terry preference model |  | new maths: short section inside the RO Note that first uses it | 57 |
| Cross-entropy method (derivative-free max over actions) |  | new maths: short section inside the RO Note that first uses it | 43 |
| Convex hull | smallest convex set around a set of points | MA 07-optimisation (short section added to MA-067) | 311 |
| Geodetic coordinates and map projections | latitude/longitude to local east-north-up metres; UTM | short section inside the RO Note that first uses it | 86 |
| Recursive least squares | update a least-squares fit one measurement at a time; a bridge to the Kalman filter | short section inside the RO Note that first uses it | 80 |
| Projective homogeneous coordinates | any multiple is the same point; divide by the last entry (PE-002) | short section inside the RO Note that first uses it | 89 |
| Least-squares solution of Ax = 0 by the SVD | last right singular vector (PE-009) | short section inside the RO Note that first uses it | 91 |
| k-d trees and point-set alignment by SVD (Kabsch) | fast nearest neighbours; best rotation between matched points (PE-071, PE-043) | short section inside the RO Note that first uses it | 94 |
| Polynomials from boundary conditions | solve a small linear system for cubic/quintic coefficients (CT-085, ME-050) | short section inside the RO Note that first uses it | 210 |
| Cubic splines and minimum jerk (beginner calculus of variations) | piecewise cubics; the quintic that minimises jerk (CT-088, CT-089) | short section inside the RO Note that first uses it | 211 |
| Controllability rank test and pole placement | rank of [B, AB, ...]; eigenvalues of A - BK (CT-031, CT-033) | short section inside the RO Note that first uses it | 213 |
| Discrete Riccati recursion | backward update of the cost matrix; DP on quadratic costs | short section inside the RO Note that first uses it | 214 |
| Newton-type solvers with constraints (SQP, interior point), overview | what the solver does each iteration (CT-073) | short section inside the RO Note that first uses it | 218 |
| Second-order linear systems | mass-spring-damper; natural frequency and damping ratio (ME-056) | short section inside the RO Note that first uses it | 121 |
| Conditional value at risk | the average of the worst outcomes; builds on MA-008 percentiles | short section inside the RO Note that first uses it | 207 |
| Structure tensor | 2x2 matrix of image gradients read through its eigenvalues | short section inside the RO Note that first uses it | 239 |
| Levenberg-Marquardt and robust losses (IRLS) | damped Gauss-Newton; losses that grow slowly for big errors (PE-052, PE-053) | short section inside the RO Note that first uses it | 249 |
| Newton-Raphson root finding | solve f(x) = 0 by repeated linearisation; non-square Jacobian via the pseudo-inverse (ME-030) | short section inside the RO Note that first uses it | 297 |
| Lagrangian mechanics (worked-example depth) | L = T - V gives M(q)q'' + c + g = tau (ME-037); physics, so a short RO section | short section inside the RO Note that first uses it | 300 |
| Friction pyramid | the friction cone as linear inequalities so problems stay QPs (ME-080) | short section inside the RO Note that first uses it | 308 |

## 7. Recap only: already taught in Maths/Machine Learning/Deep Learning (29)

| Concept | Home | Rows |
|---|---|---|
| Constant step size = EWMA | DL-033#1-overview | RL doc SB2.6 'Constant step size = exponential recency-weighted average' |
| Polynomial features | ML-060#3-adding-powers-as-new-features | RL doc SB9.5 'Polynomial features' |
| Neural networks as function approximators | DL-010#6-the-whole-network-in-one-formula | RL doc SB9.11 'Neural networks as approximators' |
| Random variables, PMF and PDF | MA-020#2-random-variables | PR doc 2.1 'Random variables, PMF and PDF' |
| Joint, marginal and conditional probability | MA-014#2-joint-probability | PR doc 2.2 'Joint, marginal and conditional probability' |
| Independence | MA-016#2-the-definition | PR doc 2.3 'Independence and conditional independence' |
| Law of total probability | MA-019#1-overview | PR doc 2.4 'Law of total probability' |
| Bayes' theorem, prior, posterior | MA-018#4-the-formula-and-its-proof | PR doc 2.5 'Bayes' theorem, prior, posterior' |
| Normalising constant (Bayes without the evidence) | ML-082#3-step-1-bayes-theorem-without-the-evidence | PR doc 2.6 'Normalising constant (Bayes without the evidence term)' |
| Expected value, variance, covariance | MA-012#3-expected-value | PR doc 2.8 'Expected value, variance, covariance' |
| Entropy of a distribution | ML-091#61-disorder-and-uncertainty | PR doc 2.9 'Entropy of a distribution' |
| Normal distribution | MA-024#5-the-pdf-of-the-normal-distribution | PR doc 2.10 'Normal distribution (one variable)' |
| Multivariate normal distribution | MA-073#71-the-multivariate-normal | PR doc 2.11 'Multivariate normal distribution' |
| Matrix inverse | ML-053#6-the-normal-equation | PR doc 3.4 'Matrix inverse' |
| Histogram | ML-019#6-histogram | PR doc 4.1 'Histogram' |
| Log-odds | ML-116#4-stage-1-the-log-odds-of-class-1 | PR doc 4.4 'Log-odds' |
| Exponential distribution | MA-071#31-the-distribution-of-waiting-times | PR doc 6.3 'Exponential distribution (for "too short" readings)' |
| Rotation as a linear map (MA-053 shows the 90-degree case; any angle theta is new, see new_maths rigid-body transforms) | MA-053#6-reading-a-matrix-as-a-picture | PA doc 3.4 '2D rotation matrix' |
| Chaining transforms by matrix multiplication | MA-054#22-following-the-basis-vectors | PA doc 3.5 'Chaining transforms by matrix multiplication' |
| Scaling and shear | MA-053#6-reading-a-matrix-as-a-picture | PA doc 3.6 'Scaling and shear (non-rigid transforms)' |
| Gradient of a potential function | MA-062#4-the-gradient | PA doc 5.10 'Gradient of a potential function' |
| Probability space, conditional probability, marginalising | MA-015#2-the-definition | PA doc 9.2 'Probability space, conditional probability, marginalising' |
| Random variables and expectation | MA-012#3-expected-value | PA doc 9.3 'Random variables and expectation' |
| Multivariate Gaussian | MA-073#71-the-multivariate-normal | PA doc 11.7 'Multivariate Gaussian' |
| Jacobian for velocity relations | MA-063#42-the-formula-every-partial-derivative-in-one-grid | PA doc 13.2 'Jacobian / partial derivatives for velocity relations' |
| Taylor linearisation of a system | MA-064#7-where-ml-uses-second-order-approximations | PA doc 15.1 'Taylor linearisation of a system around a point' |
| QP and KKT conditions | MA-066, MA-068 | CT-107 |
| Jacobian | MA-063 | CT-108 |
| Image as a grid of numbers; edges as brightness changes | DL-042 | PE-012 |

## 8. Overlaps merged (155)

The same concept named in more than one doc, kept as one Note.

| Concept | Rows | Kept as (Note) |
|---|---|---|
| pose (x, y, heading), holonomic vs nonholonomic constraints | PR doc 5.1 'Pose (x, y, heading) and kinematic configuration', PA doc 13.1 'Velocity constraints: holonomic vs nonholonomic', PA doc 13.3 'Wheeled robot models: simple car, Dubins car, Reeds-Shepp car, differential drive, trailers' | 64 |
| feature-based vs grid maps, obstacles as polygons built from half-planes | PR doc 6.1 'Maps: feature-based and location-based (grid)', PR doc 6.8 'Feature extraction and landmarks (range, bearing, signature)', PA doc 3.1 'Shapes from half-planes (convex polygons and polyhedra)', PA doc 3.3 'Triangle meshes and bitmaps (occupancy grids)' | 71 |
| beam model: one reading as a mix of four error types, mixture density of different shapes | PR doc 6.2 'Beam model of range finders', PR doc 6.4 'Mixture density of four parts', PR doc 6.5 'Learning sensor-model parameters by MLE / EM', PA doc 11.1 'Sensor models (landmark, range/depth, odometry, boundary)' | 74 |
| state transition and measurement probabilities, hidden Markov model / dynamic Bayes network | PR doc 2.14 'State transition probability and measurement probability', PR doc 2.15 'Hidden Markov model / dynamic Bayes network', PR doc 2.17 'Belief and predicted belief', PA doc 11.2 'Information space and information state (history of actions and readings)', PA doc 11.3 'Nondeterministic information state (set of possible states)' | 77 |
| Bayes' theorem conditioned on past data, Bayes filter predict and update steps | PR doc 2.7 'Bayes' theorem conditioned on extra known facts', PR doc 2.18 'Bayes filter (predict step, update step)', PA doc 11.4 'Probabilistic information state (belief) and the Bayes filter' | 78 |
| linear Gaussian system, Kalman filter and the Kalman gain | PR doc 3.1 'Linear Gaussian system', PR doc 3.6 'Kalman filter and the Kalman gain', PA doc 11.8 'Kalman filter' | 80 |
| resampling and the low-variance sampler, particle filter | PR doc 4.8 'Resampling, low-variance sampler', PR doc 4.9 'Particle filter', PR doc 4.10 'Particle deprivation and sample variance', PA doc 11.10 'Particle filter' | 82 |
| tracking, global and kidnapped-robot localization, Markov localization | PR doc 7.1 'Kinds of localization: tracking, global, kidnapped robot; static/dynamic world; passive/active; one/many robots', PR doc 7.2 'Markov localization', PA doc 12.2 'Robot localization (discrete, geometric, Monte Carlo)' | 96 |
| online SLAM vs full SLAM | PR doc 10.1 'SLAM problem: online SLAM vs full SLAM', PA doc 12.3 'Mapping and SLAM (build a map while finding yourself in it)' | 102 |
| reward as a number to maximise over time, possibly delayed, exploration vs exploitation | RL doc SB1.1 'RL as learning from interaction: agent, environment, reward', RL doc SB1.2 'Exploration vs exploitation trade-off', RL doc SB1.3 'Four elements: policy, reward signal, value function, model', RL doc SB1.5 'Evolutionary (policy search) vs value-function methods', PR doc 14.2 'Reinforcement learning, reward, policy' | 1 |
| agent-environment interface per time step, MDP dynamics p(s', r \| s, a) | RL doc SB3.1 'Agent–environment interface: state, action, reward, time step', RL doc SB3.4 'MDP dynamics p(s', r given s, a)', RL doc SB3.5 'Reward hypothesis: goals as summed reward', PR doc 14.3 'Markov decision process (states, actions, transition probabilities, payoff)', PA doc 10.1 'Markov decision process (MDP)', PA doc 10.2 'Forward projections and backprojections' | 7 |
| return, episodes, episodic vs continuing tasks, discount factor and horizon | RL doc SB3.6 'Return, episodes, episodic vs continuing tasks', PR doc 14.4 'Discount factor, horizon, cumulative payoff', PA doc 10.5 'Infinite horizon: discounted cost and average cost' | 8 |
| Bellman expectation equation, backup diagrams | RL doc SB3.10 'Bellman expectation equation', RL doc SB3.11 'Backup diagrams', RL doc SB3.14 'Bellman equation as a linear system v = (I − γP)⁻¹r', RL doc B.1 'Principle of optimality; the functional (Bellman) equation', PR doc 14.5 'Value function and Bellman equation' | 10 |
| policy improvement theorem, policy iteration | RL doc SB4.2 'Policy improvement theorem', RL doc SB4.3 'Policy iteration', PA doc 10.4 'Policy iteration' | 13 |
| value iteration, cost-to-go as the planning name for value | RL doc SB4.4 'Value iteration', PA doc 2.8 'Cost-to-go and value iteration (dynamic programming)', PA doc 10.3 'Value iteration and the Bellman equation (with nature)', PR doc 14.6 'Value iteration' | 14 |
| value iteration on a robot grid map, DP with interpolation on continuous spaces | PR doc 14.7 'Value iteration for robot path planning on a grid', PA doc 8.7 'Dynamic programming with interpolation on continuous spaces', PA doc 14.7 'Feedback planning with dynamic programming and interpolation' | 108 |
| first-visit and every-visit MC prediction, MC estimation of action values | RL doc SB5.2 'First-visit and every-visit MC prediction', RL doc SB5.3 'MC estimation of action values', PA doc 10.6 'Reinforcement learning: evaluating a plan by simulation (Monte Carlo, temporal difference)' | 16 |
| Q-learning (off-policy TD control), convergence of Q-learning | RL doc SB6.5 'Q-learning (off-policy TD control)', PA doc 10.7 'Q-learning', RL doc B.3 'Convergence of Q-learning (every pair visited forever, step-size conditions)' | 21 |
| lambda-return, eligibility traces; forward vs backward view | RL doc SB12.1 'λ-return', RL doc SB12.2 'Eligibility trace vector; TD(λ); forward vs backward view', RL doc SB12.3 'Truncated λ-return, online λ-return, true online TD(λ), dutch traces', RL doc SB12.4 'Sarsa(λ)', RL doc SB12.5 'Variable λ and γ', RL doc SB12.6 'Off-policy traces: Watkins's Q(λ), Tree-Backup(λ), GTD(λ), emphatic TD(λ)', RL doc B.2 'TD(λ) for multi-step prediction' | 24 |
| policy gradient theorem, log-derivative trick | RL doc SB13.3 'Policy gradient theorem', RL doc SB13.4 'Log-derivative trick ∇π / π = ∇ ln π', RL doc B.5 'Policy gradient theorem with function approximation; compatible features' | 30 |
| Monte Carlo policy gradient (REINFORCE family) | RL doc SB13.5 'REINFORCE (Monte Carlo policy gradient)', RL doc B.4 'REINFORCE family of algorithms' | 30 |
| one-step actor-critic, policy gradient for continuing problems | RL doc SB13.7 'One-step actor–critic', RL doc SB13.8 'Policy gradient for continuing problems', RL doc B.6 'Two-timescale actor–critic (critic learns faster than actor)' | 32 |
| CNN trained with Q-learning targets on raw pixels, error clipping in the TD loss | RL doc C.1 'Deep Q-network on raw pixels', RL doc C.4 'Error clipping in the loss', RL doc SB16.5 'Human-level video game play (DQN)' | 35 |
| self-play TD learning (TD-Gammon, Samuel checkers), policy network + value network + tree search | RL doc SB16.1 'TD-Gammon', RL doc SB16.2 'Samuel's checkers player', RL doc SB16.6 'AlphaGo and AlphaGo Zero', RL doc C.5 'Policy network + value network + tree search', RL doc C.6 'Self-play from scratch; MCTS as policy improvement', RL doc C.7 'One algorithm for several board games' | 55 |
| partially observable MDP, planning in belief / information space | PR doc 15.1 'Partially observable MDP and belief space', PA doc 11.6 'POMDP (MDP where the state is hidden)', PA doc 12.1 'Planning in belief / information space', RL doc SB17.3 'Observations and state; POMDP; state-update function', RL doc R3.1 'Robot control as a POMDP' | 162 |
| system identification and actuator networks, delta (residual) action model learned from real data | RL doc R1.5 'System identification and actuator models', RL doc R1.6 'Delta (residual) action model learned from real data *(added 2023–26)*', RL doc H.8 'Aligning sim with real via a delta action model', RL doc L.2 'Learning a gait from scratch with an improved simulator' | 148 |
| reward shaping and reward hacking, designing reward signals: sparse, shaped, imitation, inverse RL | RL doc R2.8 'Reward shaping and its risks', RL doc SB17.4 'Designing reward signals: sparse reward, shaping, imitation, inverse RL' | 155 |
| gait shaping: feet air time, clearance, energy, gaits emerging from energy minimisation | RL doc R2.7 'Gait shaping: feet air time, foot clearance, energy', RL doc L.8 'Gaits from energy minimisation', RL doc R2.13 'A family of behaviours in one policy' | 156 |
| Hindsight Experience Replay, goal-conditioned manipulation with sparse rewards | RL doc R2.11 'Sparse rewards and Hindsight Experience Replay', RL doc M.5 'Goal-conditioned manipulation with sparse rewards' | 159 |
| evolutionary search over reward weights and network shape (AutoRL), reward code written by a language model | RL doc N.16 'Searching rewards and networks automatically', RL doc R2.15 'Reward code written by a language model *(added 2023–26)*' | 161 |
| adaptation from history without weight updates, humanoid walking sim-to-real with a causal transformer, zero-shot | RL doc R3.13 'In-context adaptation with a sequence model', RL doc H.3 'Humanoid locomotion sim-to-real' | 178 |
| general value functions, auxiliary losses (depth, loop closure) for representation | RL doc R3.14 'Auxiliary tasks for representation', RL doc SB17.1 'General value functions and auxiliary tasks' | 179 |
| adaptive velocity curriculum + online system identification for running, soft-then-hard obstacle curriculum; distil skills into one depth policy with DAgger | RL doc L.4 'High-speed running', RL doc L.5 'Agility and parkour', RL doc H.10 'Perceptive humanoid locomotion *(added 2023–26)*' | 332 |
| motion imitation reward with reference-state starts, discriminator style reward (AMP) plus task reward | RL doc H.1 'Motion imitation reward', RL doc H.2 'Adversarial motion priors', RL doc R2.14 'Style rewards learned from data' | 342 |
| learned navigation over a locomotion policy; end-to-end locomotion + local navigation, skill hierarchies for agile navigation (parkour) | RL doc N.22 'Navigation with legged robots', RL doc L.6 'Skill hierarchies for agile navigation', RL doc N.23 'Wheeled-legged urban navigation *(added 2023–26)*' | 336 |
| Markov chains | RL doc SB3.2 'Markov property', RL doc SB3.3 'Markov chain: transition matrix, stationary distribution', PR doc 2.16 'Markov assumption' | new maths: Markov chains |
| Monte Carlo estimation | RL doc SB5.1 'Monte Carlo estimation (average sampled returns)', PR doc 4.6 'Monte Carlo approximation (a set of samples stands for a distribution)' | new maths: Monte Carlo estimation |
| Importance sampling | RL doc SB5.7 'Importance sampling ratio; ordinary vs weighted IS', RL doc SB5.8 'Variance of IS estimators (can be infinite)', PR doc 4.7 'Importance sampling (target, proposal, weights)', PA doc 11.9 'Monte Carlo methods and importance sampling' | new maths: Importance sampling |
| KL divergence | RL doc C.11 'KL divergence between policies', PR doc 8.5 'KL divergence' | new maths: KL divergence |
| Rigid-body transforms and homogeneous coordinates | PA doc 3.7 'Rigid-body transform (rotate + translate, keeps distances)', PA doc 3.8 'Homogeneous transformation matrix', PA doc 4.11 'Special Euclidean groups SE(2), SE(3)', PR doc 5.2 '2D rotation and heading angles' | new maths: Rigid-body transforms and homogeneous coordinates |
| Policies, plans and value functions | RL doc SB3.8 'Policy π(a given s) as a conditional distribution', RL doc SB3.9 'State-value v_π and action-value q_π', PA doc 1.1 'State, action, state transition (the basic parts of a planning problem)', PA doc 1.2 'Feasible plan vs optimal plan', PA doc 1.3 'Open-loop plan vs feedback plan', PA doc 8.1 'Feedback plan as a policy' | 9 |
| Least-squares TD and nonparametric value functions | RL doc SB9.12 'Least-squares TD (LSTD)', RL doc SB9.13 'Memory-based (nearest-neighbour) approximation', RL doc SB9.14 'Kernel-based approximation' | 51 |
| Control with approximation and the average-reward setting | RL doc SB10.1 'Episodic semi-gradient Sarsa (mountain car)', RL doc SB10.2 'Semi-gradient n-step Sarsa', RL doc SB10.3 'Average-reward setting, differential return and values', RL doc SB10.4 'Why discounting breaks with approximation', RL doc SB10.5 'Differential semi-gradient n-step Sarsa' | 27 |
| The policy gradient theorem and REINFORCE | RL doc SB13.3 'Policy gradient theorem', RL doc SB13.4 'Log-derivative trick ∇π / π = ∇ ln π', RL doc B.5 'Policy gradient theorem with function approximation; compatible features', RL doc SB13.5 'REINFORCE (Monte Carlo policy gradient)', RL doc B.4 'REINFORCE family of algorithms' | 30 |
| Markov localization on a known map | PR doc 7.1 'Kinds of localization: tracking, global, kidnapped robot; static/dynamic world; passive/active; one/many robots', PR doc 7.2 'Markov localization', PA doc 12.2 'Robot localization (discrete, geometric, Monte Carlo)', PR doc 8.1 'Grid localization' | 96 |
| Monte Carlo localization and adaptive particle counts | PR doc 8.2 'Monte Carlo localization (MCL)', PR doc 8.3 'Random-particle / augmented MCL (recovery from failure)', PR doc 8.8 'Localization in changing environments (people, outlier readings)', PR doc 8.4 'Choosing a better proposal distribution', PR doc 8.6 'Chi-square distribution (used to bound KL)', PR doc 8.7 'KLD-sampling (adaptive number of particles)' | 97 |
| Grid path planning: wavefronts, navigation functions and value iteration | PR doc 14.7 'Value iteration for robot path planning on a grid', PA doc 8.7 'Dynamic programming with interpolation on continuous spaces', PA doc 14.7 'Feedback planning with dynamic programming and interpolation', PA doc 8.2 'Navigation functions and grid wavefront propagation' | 108 |
| Moving through unknown maps: D* replanning and bug algorithms | PA doc 12.4 'D* (fast replanning when the map changes)', PA doc 12.5 'Bug algorithms and navigating unknown spaces' | 109 |
| Collision checking and nearest neighbours in C-space | PA doc 5.7 'Collision detection (distance between sets, broad and narrow phase)', PA doc 5.8 'Bounding-volume hierarchies', PA doc 5.1 'Metric space (rules a distance must follow)', PA doc 5.9 'Nearest-neighbour search with kd-trees', PA doc 5.3 'Uniform random samples of rotations and directions' | 110 |
| Curricula: terrain, commands and automatic domain randomization | RL doc R2.10 'Curricula: terrain and command', RL doc R1.4 'Automatic domain randomization (ADR)' | 158 |
| Behaviour cloning, compounding error and DAgger | RL doc R3.5 'Behaviour cloning and compounding error', RL doc R3.6 'DAgger' | 174 |
| Learned state estimators: explicit and latent | RL doc R3.9 'Learned state estimation trained with the policy', RL doc R3.11 'Latent context estimators' | 177 |
| Lagrangian and PID-Lagrangian PPO | RL doc R4.3 'Lagrangian methods (PPO-Lagrangian)', RL doc R4.4 'PID Lagrangian' | 202 |
| Not only rewards but also constraints: constraint types for real robots | RL doc R4.8 'Constraint types for robots: probabilistic and average', RL doc R4.9 'Choosing a constrained algorithm for hardware', RL doc R4.13 'Safe-RL benchmarks and libraries' | 204 |
| Observations for navigation: laser, vision and maps | RL doc N.5 'Observation design for a laser-scan navigation policy', RL doc N.6 'Observation design for visual and map-based navigation' | 166 |
| Exploration by information gain and active localization | PR doc 17.1 'Information gain and entropy as a goal', PR doc 17.2 'Greedy and multi-step exploration', PR doc 17.3 'Monte Carlo exploration', PR doc 17.4 'Active localization' | 189 |
| Crowds and robot teams: attention pooling and shared policies | RL doc N.13 'Any number of neighbours: LSTM and attention pooling', RL doc N.14 'Shared-policy multi-robot training with PPO' | 223 |
| Vision-language-action models and generalist robot policies | RL doc E.15 'Vision-language-action (VLA) model; actions as text tokens; co-fine-tuning', RL doc E.16 'Fine-tuning an open VLA for a new robot', RL doc E.20 'Generalist VLA for real robots (mostly imitation; context)', RL doc E.21 'Open foundation model for humanoids (mostly imitation; context)' | 372 |
| Data association and multi-hypothesis tracking | PR doc 7.4 'Data association (correspondence) problem', PR doc 7.5 'Maximum-likelihood data association', PR doc 3.9 'Mixture-of-Gaussians belief (multi-hypothesis, 3.3.5)', PR doc 7.7 'Multi-hypothesis tracking' | 275 |
| Games: minimax, alpha-beta and equilibria | PA doc 9.6 'Zero-sum games, minimax and saddle points', PA doc 9.7 'Mixed (randomized) strategies, solved with linear programming', PA doc 9.8 'Nonzero-sum games and Nash equilibrium', PA doc 10.8 'Game trees and alpha-beta pruning', PA doc 10.9 'Sequential games on state spaces' | 54 |
| Parameterised policies | SB13.1, SB13.2, RS-002 | 29 |
| Pose and wheeled-robot motion | PR 5.1, PA 13.1, PA 13.3, CT-004, CT-005, ME-014 | 64 |
| Coordinate frames and the transform tree | AU-005, ME-004 | 65 |
| Probabilistic motion models: velocity and odometry | PR 5.3, PR 5.4, PR 5.5, PR 5.7, PR 5.8, CT-006 | 68 |
| Kinematic chains: where the hand and foot are | PA 3.10, PA 3.11, PA 3.12, ME-018, ME-019, ME-020 | 69 |
| Robot description files: URDF, SDF and MJCF | AU-042, ME-016, ME-013 | 70 |
| Configuration space and degrees of freedom | PA 4.8, PA 4.3, PA 4.4, PA 4.14, ME-012 | 72 |
| PD and PID control | R0.7, CT-014, CT-105 | 120 |
| Kalman filter | PR 3.1, PR 3.6, PA 11.8, CT-110, PE-091, CT-032, PE-104 | 80 |
| Extended Kalman filter | PR 3.7, PR 3.8, PE-092 | 81 |
| Integrating rotation rates and strapdown inertial navigation | PE-086, PE-088, ME-005 | 85 |
| Satellite positioning: GNSS and RTK | PE-090, AU-015 | 86 |
| 3D maps: voxels, octrees, elevation maps and signed distance | AU-012, PE-077, PE-078, PE-079, PE-080 | 99 |
| Localizing in a prior 3D map: the normal distributions transform | AU-016, PE-074 | 101 |
| Planning with motion limits | PA 14.1, PA 14.2, PA 14.4, PA 14.5, PA 14.6, PA 15.9, CT-095, CT-096 | 114 |
| Trajectory optimisation | PA 14.9, CT-097, CT-072, ME-054 | 118 |
| Reading a controller's response: step response and second-order systems | CT-034, ME-056 | 121 |
| Feedforward, integral action, cascaded loops and windup | CT-037, ME-055, CT-035, CT-036, CT-038 | 126 |
| Classical local planning: DWA and TEB | N.1, CT-055 | 138 |
| The Nav2 navigation stack and ROS tooling | N.26, RL §5.1 decision 2026-10-03 'The Nav2 navigation stack' (second background Note), RS-024 | 140 |
| Why robot RL is hard | R0.1, R0.2, R0.3, RS-001, RS-012 | 141 |
| The robot as an MDP | R0.4, RS-013 | 142 |
| Action spaces: torques, PD targets, velocity commands | R0.5, R0.6, CT-111 | 143 |
| Parallel simulation and the reference training stack | R0.8, R0.9, R0.10, RS-097 | 144 |
| The reality gap and domain randomization | R1.1, R1.2, R1.3, R1.9, RS-089, RS-050 | 146 |
| System identification and actuator models | R1.5, R1.6, H.8, L.2, RS-090, AU-035, RS-094 | 148 |
| Real-robot training and sim-real agreement | R1.7, R1.8, RS-093, RS-008 | 149 |
| Curricula: terrain, commands and automatic domain randomization | R2.10, R1.4, RS-091 | 158 |
| Searching for rewards automatically | N.16, R2.15, RS-010, RS-118 | 161 |
| Learned vs classical local planners | N.2, RS-026, RS-030 | 163 |
| Mapless end-to-end navigation | N.4, RS-025 | 165 |
| Evaluating navigation: success, SPL, collisions | N.19, AU-046, AU-036, RS-014 | 170 |
| Privileged information | R3.3, RS-049 | 172 |
| Behaviour cloning, compounding error and DAgger | R3.5, R3.6, RS-061 | 174 |
| Teacher-student distillation | R3.7, RS-095 | 175 |
| Online adaptation modules (RMA) | R3.8, RS-096 | 176 |
| Learned state estimators: explicit and latent | R3.9, R3.11, PE-108 | 177 |
| In-context adaptation with sequence models | R3.13, H.3, RS-115 | 178 |
| Object detection: boxes, IoU, non-max suppression and mAP | PE-109, PE-110, PE-111, PE-118, AU-017 | 182 |
| Semantic segmentation | PE-114, PE-115, AU-018 | 184 |
| Semantic maps and traversability costs | PE-116, PE-117, RS-031 | 186 |
| Multi-object tracking | AU-019, PE-106 | 187 |
| Predicting where people and vehicles go, and collision checks in time | AU-022, RS-033, AU-023 | 188 |
| Curiosity and intrinsic rewards for exploration | AU-051, RS-037 | 191 |
| Options: temporal abstraction | SB17.2, RS-018 | 193 |
| Inverse RL: recovering a reward from demonstrations | RS-066, AU-039 | 198 |
| Constrained MDPs and cost critics | R4.1, R4.2, RS-098 | 201 |
| Not only rewards but also constraints: constraint types for real robots | R4.8, R4.9, R4.13, RS-105 | 204 |
| Shields, safety filters and recovery policies | R4.11, R4.12, RS-100, RS-104 | 206 |
| Time scaling and polynomial trajectories | CT-084, ME-048, CT-085, ME-050, CT-086, ME-051 | 210 |
| Via points, splines and minimum-jerk trajectories | CT-087, ME-052, CT-088, CT-089, CT-093, CT-094 | 211 |
| Speed profiles along a fixed path | CT-092, ME-053, AU-029 | 212 |
| LQR: the linear-quadratic regulator | PA 15.6, PA 15.7, CT-057, CT-058, CT-059, CT-109 | 214 |
| Multi-agent collision avoidance and social norms | N.11, N.12, RS-032 | 222 |
| Multi-agent RL: centralised training, decentralised execution | AU-033, RS-017 | 224 |
| Social navigation: norms, coupled prediction and planning, evaluation | RS-034, RS-035, RS-036, AU-024 | 225 |
| Navigation at scale | N.18, RS-044 | 226 |
| Safety in navigation | N.25, RS-057 | 229 |
| Agile aerial navigation | N.24, CT-106, RS-021, RS-045 | 236 |
| Extrinsic and time calibration between sensors | PE-015, AU-034 | 95 |
| Vision-and-language navigation: task, datasets and metrics | AU-052, RS-041 | 256 |
| Navigation foundation models | N.27, RS-120 | 258 |
| Unscented Kalman filter | PR 3.11, PR 3.12, PE-093 | 271 |
| Loop closure and map merging | PR 13.6, PR 12.7, PE-107 | 104 |
| Contact kinematics, contact types and the friction cone | ME-078, ME-079, ME-080, CT-024 | 308 |
| Grasp quality and grasp selection | ME-084, ME-085, AU-048 | 312 |
| Manipulation planning | PA 7.4, PA 12.7, ME-086, ME-087 | 313 |
| Tactile sensing | AU-050, RS-085 | 316 |
| Zero-moment point and the linear inverted pendulum | ME-090, ME-091, CT-080, CT-081 | 319 |
| Central pattern generators | ME-098, RS-048 | 323 |
| Convex MPC for legged robots | ME-101, CT-077, CT-082, RS-082, ME-102 | 325 |
| QP-based whole-body control | ME-073, ME-074, ME-075, ME-077, CT-083, RS-083, ME-107 | 327 |
| Multi-contact planning | ME-103, RS-086 | 329 |
| The PPO locomotion recipe, end to end | L.1, RS-046, RS-047 | 330 |
| Agility: high speed and parkour | L.4, L.5, H.10, RS-056 | 332 |
| Model-based and learned legged control: comparing and combining | ME-105, ME-106, RS-052, RS-053, RS-084 | 334 |
| Navigation on legged and wheeled-legged robots | N.22, L.6, N.23, RS-058 | 336 |
| Loco-manipulation: walking and using arms together | RS-059, ME-076 | 337 |
| Human motion data and kinematic retargeting | ME-108, ME-109, RS-080 | 340 |
| Motion imitation and adversarial motion priors | H.1, H.2, R2.14, RS-051 | 342 |
| Whole-body tracking from human data | H.5, H.6, H.9, ME-110, RS-079 | 343 |
| Teleoperating humanoids: live retargeting with differential IK | ME-111, RS-081 | 344 |
| Multi-skill humanoid controllers and behaviour foundation models | H.4, H.7, RS-078, RS-087 | 345 |
| Grasping from large real datasets | M.2, M.3, M.4, RS-075 | 347 |
| Residual RL | M.6, RS-076 | 348 |
| Manipulation action spaces: joints, end-effector deltas and impedance targets | RS-062, ME-068 | 349 |
| Dexterous in-hand manipulation | M.7, M.8, RS-074 | 354 |
| Mobile manipulation | ME-112, CT-112, RS-015 | 357 |
| Demonstrations from human videos | M.11, RS-068, RS-069 | 360 |
| Diffusion policy and multimodal demonstrations | RS-063, RS-064, AU-037 | 361 |
| Action chunking (ACT) | RS-065, AU-038 | 362 |
| Human feedback and shared autonomy for robots | AU-041, RS-016 | 364 |
| Vision-language-action models and generalist robot policies | E.15, E.16, E.20, E.21, RS-106, RS-088 | 372 |
| Cross-embodiment datasets and generalist policies | RS-108, AU-040 | 374 |
| RL fine-tuning of a VLA | E.19, RS-117 | 381 |

## 9. Dropped (68)

| Row | Why |
|---|---|
| SB1.6 | history, context only; one line in the RL-problem Note is enough |
| SB16.3 | case study only (S&B ch.16); teaches no new concept |
| SB16.4 | case study only (S&B ch.16); teaches no new concept |
| SB16.8 | case study only (S&B ch.16); teaches no new concept |
| SB17.5 | open-issues essay, no concept; safety is taught in the safety chapter |
| PR 12.1 | SEIF SLAM is superseded by GraphSLAM and FastSLAM for a beginner; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PR 12.2 | part of SEIF; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PR 12.3 | part of SEIF; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PR 12.5 | search technique for data association; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PR 13.5 | implementation detail (tree storage) of FastSLAM |
| PA 2.10 | logic-based (symbolic) planning; no robot RL or navigation Note uses it |
| PA 2.11 | logic-based (symbolic) planning; no robot RL or navigation Note uses it |
| PA 2.12 | logic-based (symbolic) planning; no robot RL or navigation Note uses it |
| PA 2.13 | logic-based (symbolic) planning; no robot RL or navigation Note uses it |
| PA 3.2 | semi-algebraic models; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 4.1 | topology; C-space is taught in plain words instead; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 4.2 | topology; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 4.5 | topology; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 4.6 | group theory; SE(2)/SE(3) are taught as matrices in the new rigid-body MA Note |
| PA 4.7 | topology; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 4.9 | a second way to write 2D rotations; the rotation matrix is enough |
| PA 4.15 | closed chains and algebraic varieties; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 5.2 | measure theory; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 5.4 | how random-number generators are built and tested; trivia for this course (seeds are in ML-111) |
| PA 5.5 | dispersion theory of samples; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 5.6 | low-discrepancy sequences; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 6.4 | exact algebraic planning (LaValle Block G, marked optional and heavy) |
| PA 6.5 | exact algebraic planning (LaValle Block G, marked optional and heavy) |
| PA 6.6 | exact algebraic planning (LaValle Block G, marked optional and heavy) |
| PA 6.7 | exact algebraic planning (LaValle Block G, marked optional and heavy) |
| PA 6.9 | exact algebraic planning (LaValle Block G, marked optional and heavy) |
| PA 7.3 | hybrid systems; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 7.5 | closed-chain planning; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 7.6 | protein folding and unknotting are outside robotics |
| PA 8.5 | differential geometry; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 8.6 | funnel composition; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 11.5 | automata theory; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 12.6 | pursuit-evasion; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 13.9 | calculus of variations; simulators give the dynamics, advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 13.10 | Lagrangian mechanics; simulators give the dynamics, advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 13.11 | Hamiltonian mechanics; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 13.12 | differential games; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 15.5 | controllability theory; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 15.8 | Pontryagin's principle; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 15.10 | nonholonomic control theory; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 15.11 | Lie brackets; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 15.12 | steering methods; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| SB14.1 | psychology/neuroscience context (S&B ch.14-15, optional Block 17 of the RL scope); no robot or navigation Note needs it; beginner depth (no trivia) |
| SB14.2 | psychology/neuroscience context (S&B ch.14-15, optional Block 17 of the RL scope); no robot or navigation Note needs it; beginner depth (no trivia) |
| SB14.3 | psychology/neuroscience context (S&B ch.14-15, optional Block 17 of the RL scope); no robot or navigation Note needs it; beginner depth (no trivia) |
| SB14.4 | psychology/neuroscience context (S&B ch.14-15, optional Block 17 of the RL scope); no robot or navigation Note needs it; beginner depth (no trivia) |
| SB14.5 | psychology/neuroscience context (S&B ch.14-15, optional Block 17 of the RL scope); no robot or navigation Note needs it; beginner depth (no trivia) |
| SB15.1 | psychology/neuroscience context (S&B ch.14-15, optional Block 17 of the RL scope); no robot or navigation Note needs it; beginner depth (no trivia) |
| SB15.2 | psychology/neuroscience context (S&B ch.14-15, optional Block 17 of the RL scope); no robot or navigation Note needs it; beginner depth (no trivia) |
| SB15.3 | psychology/neuroscience context (S&B ch.14-15, optional Block 17 of the RL scope); no robot or navigation Note needs it; beginner depth (no trivia) |
| SB15.4 | psychology/neuroscience context (S&B ch.14-15, optional Block 17 of the RL scope); no robot or navigation Note needs it; beginner depth (no trivia) |
| SB15.5 | psychology/neuroscience context (S&B ch.14-15, optional Block 17 of the RL scope); no robot or navigation Note needs it; beginner depth (no trivia) |
| ME-035 | closed chains and parallel mechanisms: the old plan already drops closed chains (PA 4.15, 7.5); no navigation, legged, humanoid or RL Note uses them |
| ME-047 | articulated-body algorithms are implementation detail inside simulators and dynamics libraries |
| ME-069 | robust and adaptive control: only named in MR's 'other topics'; beyond beginner depth; model error is handled the RL way (system identification, domain randomization) |
| ME-113 | contact pathologies and hybrid differentiability: research-level theory (Wensing III-A3-A4) |
| ME-114 | contact-implicit numerical methods: research level; the idea is named in 'Contact forces and contact as a hybrid system' |
| ME-115 | speed-ups for nonlinear MPC: implementation detail |
| MA Note: Solving linear systems: Gaussian elimination | no Note in the plan solves a linear system by hand; ML-053 inverts its matrix without it |
| MA Note: QR decomposition and least squares | no Note in the plan uses it |
| MA Note: Constrained optimisation algorithms: projected gradient, augmented Lagrangian and ADMM | the MPC solver Note (218) gives only an overview of solvers; nothing needs ADMM itself |
| MA Note: Derivative-free optimisation: local search, annealing and genetic algorithms | folded into Note 43, its only user: evolution strategies and the cross-entropy method are derivative-free methods |
| ML Note: Mean-shift clustering | no Note in the plan uses it; segmentation in the plan is learned |

## 10. Decisions taken (2026-10-07)

1. **Subjects:** Reinforcement Learning (RL) and Robotics (RO). The old third Subject was dropped: it grouped Notes by robot type, not by what they teach. Its model-based Notes went to Robotics / Control, Perception or Navigation and planning; its learning Notes went to Reinforcement Learning for Robots.
2. **Detection and segmentation** (Notes 182–184) stay in Robotics / Perception.
3. **Lagrangian mechanics** (Note 300) stays, as a worked 2-link arm.
4. **Humanoids:** 6 Notes of their own (RL-14) is enough.
5. **Maths Notes with no user were dropped:** Gaussian elimination, QR, constrained optimisation algorithms and mean shift. Derivative-free optimisation became a section of Note 43, its only user. Lie groups stays, linked to its user (Note 279). The reasons are in §9.
6. **Maths (MA) 09 Signals and systems** comes before the sensors chapter.
7. **Robotics / Navigation** is renamed **Navigation and planning**, since it also holds manipulation and task planning (Notes 313–315).
8. **Full names everywhere:** Maths (MA), Machine Learning (ML), Deep Learning (DL), Reinforcement Learning (RL), Robotics (RO).

