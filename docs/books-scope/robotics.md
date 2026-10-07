# Scope: Robotics and reinforcement learning, one plan

**Summary.** This is the plan for all robotics and RL Notes: **359 Notes in three Subjects**. It is a scoping list only, not study Notes.

The first draft (188 Notes, 2026-10-07) came from three books and left whole areas out: path tracking, MPC, cameras and optical flow, visual odometry, arm kinematics and dynamics, legged models, the system architecture, tracking other agents, and imitation learning. This plan was rebuilt from **survey papers first**, then textbooks and university courses.

**Evidence docs.** Each one keeps its rows, sources and checks. This plan cites their rows by ID.

| Doc | Area | Row IDs |
|---|---|---|
| [reinforcement-learning.md](reinforcement-learning.md) | Sutton & Barto, deep RL, robot RL, frontier | `SB2.7`, `C.18`, `R3.10`, `N.1` … |
| [probabilistic-robotics.md](probabilistic-robotics.md) | Thrun, Burgard & Fox | `PR 4.2` … |
| [planning-algorithms.md](planning-algorithms.md) | LaValle | `PA 8.7` … |
| [robot-control.md](robot-control.md) | Path tracking, vehicle models, LQR, MPC, trajectories, quadrotors | `CT-001` … |
| [robot-perception.md](robot-perception.md) | Cameras, features, optical flow, two-view geometry, VO, SfM, LiDAR, IMU, fusion, detection | `PE-001` … |
| [robot-mechanics.md](robot-mechanics.md) | Rigid-body motion, kinematics, dynamics, arm control, grasping, legged models, whole-body control | `ME-001` … |
| [robotics-curricula-audit.md](robotics-curricula-audit.md) | What 12 university courses and the Nav2 and Autoware stacks teach that the rest lacked | `AU-001` … |
| [robot-learning-surveys.md](robot-learning-surveys.md) | Learning-based robotics, mapped from 26 surveys | `RS-001` … |

Every row is placed exactly once. That covers the 589 book rows, the 518 rows of the five new docs, and all 188 Notes of the first draft. Each row is in one of four places:
- in a Note;
- recapped from an MA/ML/DL Note (§4);
- in new maths (§3);
- dropped with a reason (§6).

Source keys such as `PA16`, `SN09`, `RVC3` and `MR` are defined in the evidence doc that the row ID points to.

**How it was chosen.** The steps:
1. **Two merged plans.** A put robotics foundations first (409 Notes). B interleaved robotics and RL by first use (356 Notes).
2. **Two critics.** Both rejected A, which reaches learned navigation only at Note 310. Both rebuilt from B, checked the plans by script and argued for two rounds.
3. **Ruling.** Where they still differed, the orchestrator ruled: LSTD and gradient-TD are optional, because no robotics survey uses them; imitation learning and offline RL get separate chapters, because the surveys treat them as separate families.
4. **Final check.** The plan was checked against 85 method families taken from five surveys (Paden 2016, Cadena 2016, Xiao et al. 2022, Ha et al. 2024, Yurtsever 2020). All 85 are present.

## 1. Structure

| Subject | Title | Chapters | Notes | Optional | Why |
|---|---|---|---|---|---|
| RL | Reinforcement learning | 8 | 62 | 12 | The learning algorithms on their own, with no robot needed. 50 core Notes (plus 12 optional) that both robot Subjects use; keeping them apart gives RO and RB one clean base and lets RO open straight on robots. |
| RO | Robot navigation | 23 | 212 | 25 | The primary interest and the deepest track. Classical robotics is interleaved with robot RL: each classical block sits just before the chapter that first uses it, so the learner builds a classical stack (sense, localise, plan, track), then replaces and extends parts of it with learned policies. |
| RB | Robot bodies: legs, humanoids and arms | 10 | 85 | 0 | The equal-second interests. Mechanics, arm and legged control, then learned locomotion, humanoids, manipulation, imitation and foundation models. It needs RO's robot-RL chapters (sim-to-real, task design, privileged learning), so it comes after RO and never links forward. |

## 2. Order, and why

1. **RL core first (RL-01 to RL-06).** Its only robotics needs are a priority queue and a heuristic, and each Note builds its own (S&B §8.4, §8.9). RL theory and games (RL-07) and RL for language models (RL-08) are optional, because the robotics surveys treat them as minor.
2. **Robot navigation (RO) is the primary track.** It builds a classical stack first:
   - robot models;
   - Bayes filters;
   - sensors: IMU, GNSS, cameras, depth, LiDAR;
   - localization, maps and pose-graph SLAM;
   - path planning: graph search, sampling, Hybrid A\*, lattices;
   - path tracking: pure pursuit, Stanley, Kanayama;
   - the stack itself: ROS 2, behaviour trees, Nav2 (Note 131).

   Robot RL and task design come next, then Navigation I (from Note 153).
3. **Each later classical block sits just before the chapter that first uses it:**
   - perception of objects and people before Navigation II and III;
   - LQR and MPC before aerial robots;
   - visual odometry before navigation with language and foundation models.
4. **Robot bodies (RB) comes after navigation:** kinematics, dynamics, grasping, model-based legged control, learned locomotion, humanoids, manipulation, imitation, offline RL and foundation models. Legged robots, manipulation and humanoids rank equal second.
5. **Optional depth comes last in its Subject.** Nothing outside an optional chapter builds on it:
   - car dynamics;
   - SLAM and estimation in depth, including visual-inertial and LiDAR odometry;
   - planning in depth.

## 3. The Notes

"Builds on" gives a number for an earlier Note in this plan, a label for an MA/ML/DL Note, or "new MA"/"new DL" for a Note still to be written (§4).

## RL: Reinforcement learning


### RL-01 Learning by trial: bandits

Act, get a number back, learn which action pays: explore vs exploit in one state.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 1 | The reinforcement learning problem | reward as a number to maximise over time, possibly delayed; exploration vs exploitation; four elements: policy, reward, value function, model; evolutionary (policy search) vs value-function methods; formal RL definitions in robotics | ML-003 | SB1.1, SB1.2, SB1.3, SB1.5, PR 14.2 | Sutton&Barto 2018 ch.1; Thrun et al. 2005 ch.14 |
| 2 | Multi-armed bandits and epsilon-greedy | k-armed bandit and true action value; sample-average action values; greedy and epsilon-greedy selection; 10-armed testbed | 1, MA-005 | SB2.1, SB2.2, SB2.3, SB2.4 | Sutton&Barto 2018 ch.2; DeepMind x UCL 2021 L2 |
| 3 | Incremental updates and step sizes | incremental update new = old + step x (target - old); step-size conditions (Robbins-Monro) | 2, DL-033 | SB2.5, SB2.7 | Sutton&Barto 2018 ch.2 |
| 4 | Exploring smartly: optimistic starts and UCB | optimistic initial values; upper-confidence-bound selection | 3, MA-035 | SB2.8, SB2.9 | Sutton&Barto 2018 ch.2 |
| 5 | Gradient bandits | softmax over action preferences with a baseline | 2, ML-078 | SB2.10 | Sutton&Barto 2018 ch.2 |
| 6 | Contextual bandits | contextual bandits (associative search); personalized web services example | 2 | SB2.11, SB16.7 | Sutton&Barto 2018 ch.2; Sutton&Barto 2018 ch.16 |

### RL-02 Markov decision processes and dynamic programming

Many states: the formal model, returns, policies, value functions and Bellman equations.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 7 | Markov decision processes | agent-environment interface per time step; MDP dynamics p(s', r \| s, a); reward hypothesis; forward projections and backprojections | 1, new MA: Markov chains, MA-014 | SB3.1, SB3.4, SB3.5, PR 14.3, PA 10.1, PA 10.2 | Sutton&Barto 2018 ch.3; Thrun et al. 2005 ch.14; LaValle 2006 ch.10; DeepMind x UCL 2015 L2 |
| 8 | Return and discounting | return, episodes, episodic vs continuing tasks; discount factor and horizon; infinite horizon: discounted and average cost; delayed reward and the credit-assignment problem | 7, new MA: Geometric series | SB3.6, PR 14.4, PA 10.5, SB14.6 | Sutton&Barto 2018 ch.3; Thrun et al. 2005 ch.14; LaValle 2006 ch.10 |
| 9 | Policies, plans and value functions | policy as a conditional distribution over actions; state-value and action-value functions; state, action and state transition of a planning problem; feasible vs optimal plan; open-loop plan vs feedback plan; feedback plan as a policy over the whole state space | 8, MA-012, ML-003, MA-066 | SB3.8, SB3.9, PA 1.1, PA 1.2, PA 1.3, PA 8.1 | Sutton&Barto 2018 ch.3; LaValle 2006 ch.1; LaValle 2006 ch.8 |
| 10 | Bellman equations | Bellman expectation equation; backup diagrams; Bellman equation as a linear system; principle of optimality | 9, MA-019, ML-053 | SB3.10, SB3.11, SB3.14, B.1, PR 14.5 | Sutton&Barto 2018 ch.3; Thrun et al. 2005 ch.14; Bellman 1957 |
| 11 | Optimal values and optimal policies | optimal value functions and the Bellman optimality equation; optimal policy is greedy w.r.t. q*; tabular vs approximate solutions | 10 | SB3.12, SB3.13, SB3.15 | Sutton&Barto 2018 ch.3 |
| 12 | Policy evaluation | iterative policy evaluation; bootstrapping: update a guess from a guess | 10 | SB4.1, SB4.7 | Sutton&Barto 2018 ch.4; DeepMind x UCL 2015 L3 |
| 13 | Policy improvement and policy iteration | policy improvement theorem; policy iteration | 12, 11 | SB4.2, SB4.3, PA 10.4 | Sutton&Barto 2018 ch.4; LaValle 2006 ch.10 |
| 14 | Value iteration | value iteration; cost-to-go as the planning name for value; value iteration with nature (stochastic outcomes) | 13 | SB4.4, PA 2.8, PA 10.3, PR 14.6 | Sutton&Barto 2018 ch.4; LaValle 2006 ch.2; LaValle 2006 ch.10; Thrun et al. 2005 ch.14 |
| 15 | Asynchronous DP and generalized policy iteration | asynchronous DP; generalized policy iteration (GPI); curse of dimensionality for DP | 14, ML-045 | SB4.5, SB4.6, SB4.8 | Sutton&Barto 2018 ch.4 |

### RL-03 Learning values from experience: Monte Carlo and TD

No model: learn from sampled episodes and from one-step bootstrapping.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 16 | Monte Carlo prediction | first-visit and every-visit MC prediction; MC estimation of action values; evaluating a plan by simulation | 12, new MA: Monte Carlo estimation | SB5.2, SB5.3, PA 10.6 | Sutton&Barto 2018 ch.5; LaValle 2006 ch.10; DeepMind x UCL 2015 L4 |
| 17 | Monte Carlo control | exploring starts; epsilon-soft on-policy MC control | 16, 15 | SB5.4, SB5.5 | Sutton&Barto 2018 ch.5 |
| 18 | Off-policy learning with importance sampling | on-policy vs off-policy; target vs behaviour policy; incremental weighted average; off-policy MC control; discounting-aware and per-decision IS | 17, new MA: Importance sampling | SB5.6, SB5.9, SB5.10, SB5.11 | Sutton&Barto 2018 ch.5 |
| 19 | TD(0) prediction | TD(0) and the TD error; TD = sampling + bootstrapping; batch TD vs batch MC; certainty equivalence; tic-tac-toe value learning; afterstates | 16, 12, MA-070 | SB6.1, SB6.2, SB6.3, SB1.4, SB6.8 | Sutton&Barto 2018 ch.6; Sutton&Barto 2018 ch.1; Sutton 1988 |
| 20 | Sarsa and expected Sarsa | Sarsa (on-policy TD control); expected Sarsa | 19, 17 | SB6.4, SB6.6 | Sutton&Barto 2018 ch.6; DeepMind x UCL 2015 L5 |
| 21 | Q-learning | Q-learning (off-policy TD control); convergence of Q-learning | 20, 18, 3 | SB6.5, PA 10.7, B.3 | Sutton&Barto 2018 ch.6; LaValle 2006 ch.10; Watkins & Dayan 1992 |
| 22 | Double Q-learning | maximization bias and double Q-learning | 21 | SB6.7 | Sutton&Barto 2018 ch.6 |
| 23 | n-step bootstrapping | n-step return and n-step TD; n-step Sarsa; n-step off-policy learning with IS; control variates; tree-backup algorithm; n-step Q(sigma) | 19, 18 | SB7.1, SB7.2, SB7.3, SB7.4, SB7.5, SB7.6 | Sutton&Barto 2018 ch.7; DeepMind x UCL 2021 L11 |
| 24 | Eligibility traces and TD(lambda) | lambda-return; eligibility traces; forward vs backward view; online and true online TD(lambda); Sarsa(lambda); variable lambda and gamma; off-policy traces | 23 | SB12.1, SB12.2, SB12.3, SB12.4, SB12.5, SB12.6, B.2 | Sutton&Barto 2018 ch.12; Sutton 1988 |

### RL-04 Approximate values and policy gradients

Too many states for a table: features and linear values, why off-policy approximation diverges, then training the policy itself.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 25 | Value prediction as supervised learning | value approximation with moving targets; VE objective weighted by state visits; semi-gradient methods | 19, ML-051, ML-058 | SB9.1, SB9.2, SB9.3 | Sutton&Barto 2018 ch.9; DeepMind x UCL 2021 L7 |
| 26 | Linear value functions and features | linear TD and the TD fixed point; Fourier basis features; coarse coding; tile coding; RBF features; choosing the step size by hand | 25, ML-052, ML-089, ML-060 | SB9.4, SB9.6, SB9.7, SB9.8, SB9.9, SB9.10 | Sutton&Barto 2018 ch.9 |
| 27 | Control with approximation and the average-reward setting | episodic semi-gradient Sarsa (mountain car); semi-gradient n-step Sarsa; average-reward setting and differential values; why discounting breaks with approximation; differential semi-gradient n-step Sarsa | 26, 23, new MA: Markov chains | SB10.1, SB10.2, SB10.3, SB10.4, SB10.5 | Sutton&Barto 2018 ch.10 |
| 28 | The deadly triad | off-policy semi-gradient methods; Baird's counterexample; deadly triad: approximation + bootstrapping + off-policy | 27, 18 | SB11.1, SB11.2, SB11.3 | Sutton&Barto 2018 ch.11 |
| 29 | Parameterised policies | policy as the trained model; softmax in action preferences; performance measure J(theta); Value-function methods vs policy search | 5, 9 | SB13.1, SB13.2, RS-002 | Sutton&Barto 2018 ch.13; DeepMind x UCL 2015 L7; Kober §2.2 |
| 30 | The policy gradient theorem and REINFORCE | policy gradient theorem; log-derivative trick; compatible features; Monte Carlo policy gradient (REINFORCE family) | 29, MA-062, ML-072, 16 | SB13.3, SB13.4, B.5, SB13.5, B.4 | Sutton&Barto 2018 ch.13; Sutton et al. 2000; Williams 1992 |
| 31 | Baselines | baseline as a control variate for variance reduction | 30, 23 | SB13.6 | Sutton&Barto 2018 ch.13 |
| 32 | Actor-critic | one-step actor-critic; policy gradient for continuing problems; two-timescale actor-critic | 31, 19, 27 | SB13.7, SB13.8, B.6 | Sutton&Barto 2018 ch.13; Konda & Tsitsiklis 2000 |
| 33 | Gaussian policies for continuous actions | Gaussian policy and the gradient of its log-density | 29, MA-024, MA-073 | SB13.9 | Sutton&Barto 2018 ch.13 |
| 34 | Advantage and generalized advantage estimation | advantage function A = Q - V; GAE: lambda-weighted TD errors | 32, 24, DL-033 | C.14, C.15 | Schulman et al. 2016 (GAE) |

### RL-05 Deep RL algorithms

The algorithms robots are trained with, a gradient-free baseline, and how to report results honestly.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 35 | Deep Q-networks | CNN trained with Q-learning targets on raw pixels; error clipping in the TD loss; human-level Atari play | 21, 25, DL-040, DL-014 | C.1, C.4, SB16.5 | Sutton&Barto 2018 ch.16; Mnih et al. 2015 |
| 36 | Experience replay and target networks | experience replay; target network | 35, 28 | C.2, C.3 | Mnih et al. 2015 |
| 37 | Parallel advantage actor-critic (A2C/A3C) | parallel workers; entropy bonus | 34, ML-091, DL-020 | C.8 | Mnih et al. 2016 |
| 38 | Trust regions: TRPO | trust region and surrogate objective; natural gradient and Fisher information | 37, new MA: KL divergence, new MA: Sparse linear solves and conjugate gradient, MA-064 | C.12, C.13 | Schulman et al. 2015 |
| 39 | Proximal policy optimisation (PPO) | clipped surrogate objective; several epochs per batch | 38 | C.16 | Schulman et al. 2017; Abbeel Foundations of Deep RL L4 |
| 40 | Deterministic policy gradients: DDPG | deterministic policy gradient for continuous actions; soft (Polyak) target updates and exploration noise | 36, 33, DL-033 | C.9, C.10 | Lillicrap et al. 2016 |
| 41 | TD3 | clipped double Q, delayed policy updates, target policy smoothing | 40, 22 | C.19 | Fujimoto et al. 2018 |
| 42 | Soft actor-critic (SAC) | maximum-entropy RL, soft Q and temperature; tanh-squashed Gaussian policy (reparameterization) | 41, ML-091, new DL: Variational autoencoder | C.17, C.18 | Haarnoja et al. 2018 |
| 43 | Black-box policy search: evolution strategies and the cross-entropy method | Black-box policy search: perturb parameters, keep what scores well (finite differences, evolution strategies, CMA-ES, reward-weighted averaging) | 29, new MA: Monte Carlo estimation | RS-003 | Kober §2.2.2 |
| 44 | Reporting RL results honestly: seeds, interquartile mean and confidence intervals | K1 Reporting RL results honestly: many seeds, interquartile mean, confidence intervals | 39, MA-035, new MA: Bootstrap confidence intervals and the interquartile mean | AU-045 | Agarwal et al. 2021, *Deep RL at the Edge of the Statistical Precipice* ([arXiv 2108.13264](https://arxiv.org/abs/2108.13264)) |

### RL-06 Planning with models

Use a model to plan: Dyna, rollouts, MCTS, learned dynamics and world models.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 45 | Models and Dyna | distribution vs sample models; Dyna-Q: planning, acting and learning together; wrong models and the Dyna-Q+ bonus; model-free (habitual) vs model-based (goal-directed) control | 21 | SB8.1, SB8.2, SB8.3, SB14.7 | Sutton&Barto 2018 ch.8; DeepMind x UCL 2015 L8 |
| 46 | Prioritized sweeping and where to spend updates | prioritized sweeping; expected vs sample updates; trajectory sampling and real-time DP | 45 | SB8.4, SB8.5, SB8.6 | Sutton&Barto 2018 ch.8 |
| 47 | Decision-time planning and rollouts | decision-time planning with heuristic search; rollout algorithms | 45 | SB8.7, SB8.8 | Sutton&Barto 2018 ch.8 |
| 48 | Monte Carlo tree search | MCTS: selection, expansion, simulation, backup | 47, 4 | SB8.9 | Sutton&Barto 2018 ch.8 |
| 49 | Model-based RL with learned dynamics: sampling planners, ensembles and model exploitation | Model-based RL for robots: learn the dynamics, plan with it (random shooting / CEM with a learned model), guard against the policy exploiting model errors | 45, 47, 43, DL-010 | RS-005 | Kober §6; Ibarz §4.2.1, §4.6 |
| 50 | World models and imagined rollouts | recurrent world model; learning in imagination (Dreamer) | 48, 42, DL-064, 49 | E.11 | Hafner et al. 2023 |

### RL-07 RL theory, games and self-play (minor in the robotics surveys) *(optional)*

Optional: LSTD and gradient-TD (in no robotics survey), games, self-play and MuZero (minor: about one mention each), Decision Transformer, and RL for language models.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 51 | Least-squares TD and nonparametric value functions | LSTD: solve the TD fixed point directly; memory-based value approximation; kernel-based value approximation | 26, ML-053, 25, ML-085, ML-089 | SB9.12, SB9.13, SB9.14 | Sutton&Barto 2018 ch.9 |
| 52 | Bellman error geometry and gradient-TD | projected Bellman error in a weighted norm; residual-gradient methods; the Bellman error is not learnable; gradient-TD (GTD2, TDC); emphatic TD; interest and emphasis | 28, MA-055 | SB11.4, SB11.5, SB11.6, SB11.7, SB11.8, SB9.15 | Sutton&Barto 2018 ch.11; Sutton&Barto 2018 ch.9; DeepMind x UCL 2021 L10 |
| 53 | Decisions against nature | game against nature: worst-case vs expected-cost decisions; Bayesian decision making with observations; utility theory and rationality; multi-objective optimisation and Pareto-optimal plans | MA-012, MA-018, MA-066 | PA 9.4, PA 9.5, PA 9.9, PA 9.1, PA 7.8 | LaValle 2006 ch.9; LaValle 2006 ch.7 |
| 54 | Games: minimax, alpha-beta and equilibria | zero-sum games, minimax and saddle points; mixed strategies solved by linear programming; nonzero-sum games and Nash equilibrium; game trees and alpha-beta pruning; sequential games on state spaces | 53, MA-068, MA-066 | PA 9.6, PA 9.7, PA 9.8, PA 10.8, PA 10.9 | LaValle 2006 ch.9; LaValle 2006 ch.10; DeepMind x UCL 2015 L10 |
| 55 | Self-play: from TD-Gammon to AlphaZero | self-play TD learning (TD-Gammon, Samuel checkers); policy network + value network + tree search; self-play from scratch; MCTS as policy improvement; one algorithm for several board games | 48, 54, 35, 30 | SB16.1, SB16.2, SB16.6, C.5, C.6, C.7 | Sutton&Barto 2018 ch.16; Silver et al. 2016; Silver et al. 2017; DeepMind x UCL 2018 L10 |
| 56 | Planning with a learned model: MuZero | learned latent model (representation, dynamics, prediction) + MCTS | 55 | E.10 | Schrittwieser et al. 2020 |

### RL-08 RL for language models *(optional)*

reward models, RLHF, DPO, GRPO, RLVR

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 57 | Reward models from human preferences | reward model trained on pairwise preferences; Bradley-Terry preference model | DL-067, ML-071, ML-072 | E.1, E.2 | Christiano et al. 2017 |
| 58 | RLHF with PPO and a KL penalty | SFT, reward model, PPO with a KL penalty to the SFT model | 57, 39, new MA: KL divergence | E.3 | Ouyang et al. 2022 |
| 59 | Direct preference optimisation | closed-form optimal policy of KL-regularised reward; preference loss without RL | 58 | E.4 | Rafailov et al. 2023 |
| 60 | Group-relative advantages: GRPO | no critic: compare answers to the same prompt | 58, 31 | E.5 | Shao et al. 2024 |
| 61 | RL with verifiable rewards | rule-based rewards (accuracy, format); R1-Zero without SFT; the RLVR recipe | 60 | E.6, E.7 | DeepSeek-AI 2025; Lambert et al. 2024 |
| 62 | Fixing GRPO at scale | decoupled clipping and dynamic sampling (DAPO); length bias and the Dr. GRPO fix | 61 | E.8, E.9 | Yu et al. 2025; Liu et al. 2025 |

## RO: Robot navigation


### RO-01 Robot models: pose, frames, kinematic chains and C-space

How a robot and its world are described: uncertainty, pose and frames, wheeled and car-like motion, chains, description files, maps, C-space, PID.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 63 | Why a robot is never sure: state, controls and measurements | sources of uncertainty in robots; keep a full distribution, not one best guess; state: pose, map, speeds; complete state; measurements and controls; uncertainty in actions vs in perception | ML-003, MA-020, MA-014 | PR 1.1, PR 1.2, PR 2.12, PR 2.13, PR 14.1 | Thrun et al. 2005 ch.1; Thrun et al. 2005 ch.2; Thrun et al. 2005 ch.14 |
| 64 | Pose and wheeled-robot motion | pose (x, y, heading); holonomic vs nonholonomic constraints; differential drive, simple car, Dubins and Reeds-Shepp car models; Differential drive: wheel speeds to (v, ω) and back; Nonholonomic constraint: a wheel cannot slide sideways; Holonomic and nonholonomic constraints | new MA: Rigid-body transforms and homogeneous coordinates, new MA: State-space models, MA-063 | PR 5.1, PA 13.1, PA 13.3, CT-004, CT-005, ME-014 | Thrun et al. 2005 ch.5; LaValle 2006 ch.13; MR 13.3.1; MR 13.3.1, PA16 III.A, RVC3 4.1.1; MR 2.4 |
| 65 | Coordinate frames and the transform tree | A4 Coordinate frames and the transform tree (map → odom → base_link → sensor); Rotation matrix read as a frame: its columns are the new axes; inverse = transpose; using it to change frames | 64, new MA: Rigid-body transforms and homogeneous coordinates, new MA: 3D rotations: Euler angles and quaternions | AU-005, ME-004 | CMU wk 3 "Transform graphs & pose networks"; M42 ch.3 "Monogram notation"; NAV2 concepts "State estimation"; [REP-105](https://www.ros.org/reps/rep-0105.html); MR 3.2.1 |
| 66 | Wheel types, omnidirectional bases and the unicycle model | Types of wheeled robots: omnidirectional vs nonholonomic; Omnidirectional (mecanum) base model and control; Unicycle model (forward speed v, turn rate ω) | 64, MA-063 | CT-001, CT-002, CT-003 | MR 13.1; MR 13.2.1, 13.2.3; MR 13.3.1, PA16 III.A |
| 67 | Car-like robots: the kinematic bicycle model and Ackermann steering | Kinematic bicycle model (front wheel steers, rear wheel follows); Steering angle, wheelbase and turning radius (tan δ = L / R); curvature; Ackermann steering geometry (inner wheel turns more than outer); Speed and steering limits (maximum steer, minimum turning radius); Controllability of a car in plain words (parallel parking); Kinematic vs dynamic model: when the kinematic model is enough | 66 | CT-007, CT-008, CT-009, CT-010, CT-012, CT-013 | SN09 3.1, PA16 III.A, RAJ 2.2; SN09 2.1, RVC3 4.1.1; RAJ 2.2; RVC3 4.1.1, MR 13.3.1; MR 13.3.2; Kong 2015 |
| 68 | Probabilistic motion models: velocity and odometry | motion as a distribution p(x_t \| u_t, x_t-1); velocity motion model; odometry motion model; sampling next poses from a motion model; ruling out poses inside walls; Wheel odometry | 64, new MA: Drawing samples from distributions, MA-024 | PR 5.3, PR 5.4, PR 5.5, PR 5.7, PR 5.8, CT-006 | Thrun et al. 2005 ch.5; MR 13.4 |
| 69 | Kinematic chains: where the hand and foot are | kinematic chains and forward kinematics; Denavit-Hartenberg parameters; kinematic trees (branching bodies such as humanoids); Forward kinematics of an open chain | new MA: Rigid-body transforms and homogeneous coordinates, new MA: 3D rotations: Euler angles and quaternions | PA 3.10, PA 3.11, PA 3.12, ME-018, ME-019, ME-020 | LaValle 2006 ch.3; MR ch.4 intro; MR App. C; PA ch.3 |
| 70 | Robot description files: URDF, SDF and MJCF | J1 Robot description formats: URDF/Xacro, SDF, MJCF: links, joints, inertias, collision vs visual shapes; Robot description files (URDF): links, joints, masses and inertias; Joint types (revolute, prismatic, spherical...) and Grübler's count of degrees of freedom | 69, 65 | AU-042, ME-016, ME-013 | M42 ch.2 "Robot description files"; UDR C2; URDF ([wiki.ros.org/urdf](https://wiki.ros.org/urdf)); MJCF ([MuJoCo XML reference](https://mujoco.readthedocs.io/en/stable/XMLreference.html)); MR 4.2, 8.8; MR 2.2.1–2.2.2 |
| 71 | Maps and landmarks | feature-based vs grid maps; obstacles as polygons built from half-planes; triangle meshes and bitmaps; feature extraction: landmarks with range, bearing, signature | MA-051, 63 | PR 6.1, PR 6.8, PA 3.1, PA 3.3 | Thrun et al. 2005 ch.6; LaValle 2006 ch.3 |
| 72 | Configuration space and degrees of freedom | configuration space (C-space) and degrees of freedom; C-space shapes in plain words: circle, torus (manifolds); basic motion planning problem (piano mover's); Degrees of freedom of a body and of a robot | new MA: Rigid-body transforms and homogeneous coordinates, 69 | PA 4.8, PA 4.3, PA 4.4, PA 4.14, ME-012 | LaValle 2006 ch.4; MR 2.1–2.2 |
| 73 | Obstacles in C-space | obstacle region and free space; Minkowski sum: growing obstacles by the robot's shape | 72, 71 | PA 4.12, PA 4.13 | LaValle 2006 ch.4 |

### RO-02 Sensing and Bayes filters

Range and landmark sensor models, belief, Bayes, histogram, Kalman, EKF and particle filters.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 74 | Range sensors: the beam model | beam model: one reading as a mix of four error types; mixture density of different shapes; learning sensor-model parameters by MLE and EM; catalogue of sensor models (landmark, range, odometry, boundary) | 71, MA-071, MA-073, MA-074 | PR 6.2, PR 6.4, PR 6.5, PA 11.1 | Thrun et al. 2005 ch.6; LaValle 2006 ch.11 |
| 75 | Likelihood fields and scan matching | likelihood field model; correlation-based map matching | 74, MA-009 | PR 6.6, PR 6.7 | Thrun et al. 2005 ch.6 |
| 76 | Landmark measurement model | landmark sensor model with known correspondence; sampling poses from a landmark reading | 71, 68 | PR 6.9, PR 6.10 | Thrun et al. 2005 ch.6 |
| 77 | Belief: what the robot knows | state transition and measurement probabilities; hidden Markov model / dynamic Bayes network; belief and predicted belief; information state: the history of actions and readings; set-valued (nondeterministic) information state | new MA: Markov chains, 68, 74 | PR 2.14, PR 2.15, PR 2.17, PA 11.2, PA 11.3 | Thrun et al. 2005 ch.2; LaValle 2006 ch.11 |
| 78 | The Bayes filter: predict, then update | Bayes' theorem conditioned on past data; Bayes filter predict and update steps; belief as the probabilistic information state | 77, MA-018, MA-019 | PR 2.7, PR 2.18, PA 11.4 | Thrun et al. 2005 ch.2; LaValle 2006 ch.11 |
| 79 | Grid filters: histogram filter and binary Bayes filter | histogram (discrete Bayes) filter; static and adaptive cell decomposition; binary Bayes filter in log-odds form | 78, ML-019, ML-031, ML-116 | PR 4.2, PR 4.3, PR 4.5 | Thrun et al. 2005 ch.4 |
| 80 | Kalman filter | linear Gaussian system; Kalman filter and the Kalman gain; Kalman filter for the state that feedback needs; Kalman filter; Observability; Observability (concept only) | 78, MA-073, new MA: Linear transforms of a Gaussian, new MA: Product of two Gaussians | PR 3.1, PR 3.6, PA 11.8, CT-110, PE-091, CT-032, PE-104 | Thrun et al. 2005 ch.3; LaValle 2006 ch.11; robotics.md (PR 3.1); RO 63; MPC 1.4.5; Huang §5 |
| 81 | Extended Kalman filter | pushing a Gaussian through a curved function by linearisation; extended Kalman filter (EKF); Extended Kalman filter | 80, MA-063, MA-064 | PR 3.7, PR 3.8, PE-092 | Thrun et al. 2005 ch.3; RO 64 |
| 82 | Particle filter | resampling and the low-variance sampler; particle filter; particle deprivation; belief as a cloud of weighted samples | 78, new MA: Monte Carlo estimation, new MA: Importance sampling, ML-102 | PR 4.8, PR 4.9, PR 4.10, PA 11.10 | Thrun et al. 2005 ch.4; LaValle 2006 ch.11 |

### RO-03 Robot sensors: IMU, GNSS, cameras, depth and LiDAR

What each sensor measures and how it errs, the first fusion filters, and turning depth and LiDAR into aligned point clouds.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 83 | Inertial sensors: gyroscope, accelerometer and their errors | Gyroscope: measures turn rate; Accelerometer: measures specific force (gravity included); IMU measurement model: reading = truth + bias + noise; Bias random walk and bias estimation; Integration drift: angle error grows with t, position error with t³ for a gyro bias | 63, new MA: 3D rotations: Euler angles and quaternions, MA-024 | PE-081, PE-082, PE-083, PE-084, PE-085 | RVC3 3.4.1; Woodman 2007 ([UCAM-CL-TR-696](https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-696.html)); RVC3 3.4; Woodman 2007; Huang §2.1; Woodman 2007 gyro/accel errors; Barfoot 5.2 |
| 84 | Integrating rotation rates and strapdown inertial navigation | Integrating angular velocity into orientation; Strapdown inertial navigation; Angular velocity as a vector along the spin axis | 83, new MA: Axis-angle, exponential and log maps of rotations, new MA: Numerical integration of ODEs, new MA: Cross product and skew-symmetric matrix | PE-086, PE-088, ME-005 | RVC3 3.4.1.2; Barfoot 7.2.4; Barfoot 9.4; Woodman 2007 strapdown; MR 3.2.2 |
| 85 | Satellite positioning: GNSS and RTK | GNSS/GPS basics: ranging to satellites, ~5 m phone accuracy, multipath and blockage; C1 GNSS: how a position is fixed from satellites, error sources, RTK, latitude/longitude to a local metric frame (ENU/UTM) | 65 | PE-090, AU-015 | Lee §6; [GPS.gov accuracy page](https://archive.gps.gov/systems/gps/performance/accuracy/); TOR C2 M3; CMU wk 7–8 "satellite navigation"; ETH wk 4 GPS; AW localization (GNSS, RTK); NAV2 GPS tutorial |
| 86 | Fusing IMU, wheels and GNSS: complementary filter and EKF | Complementary filter for attitude; EKF fusion of IMU, wheels and GNSS (loosely coupled); Loose vs tight coupling; Wheel odometry from encoders, and wheel slip | 84, 85, 81, 68 | PE-094, PE-095, PE-096, PE-089 | RVC3 3.4.4; Mahony et al. 2008 [doi:10.1109/TAC.2008.923738](https://doi.org/10.1109/TAC.2008.923738); Huang §2.1, §3.1; Huang §3.2; RVC3 6.1; Thrun ch.5 via RO 51 |
| 87 | Error-state Kalman filter for orientation | Error-state (indirect) Kalman filter for rotations | 86, new MA: Axis-angle, exponential and log maps of rotations | PE-097 | Barfoot 7.2.5, 8.3 |
| 88 | The pinhole camera: projection, intrinsics and extrinsics | Pinhole camera: a 3D point maps to a pixel through a small hole; Homogeneous coordinates for points in an image and in 3D; Camera matrix P = K [R \| t]; Intrinsics K: focal length, principal point, pixel size; Extrinsics: camera pose in the world | 65 | PE-001, PE-002, PE-003, PE-004, PE-005 | VO-I camera modelling; HZ 6.1; RVC3 13.1; HZ 2.2, 3.1; RVC3 13.1.4; Barfoot 7.4.1; RVC3 13.1.3; RVC3 13.1.2 |
| 89 | Lens distortion, wide-angle cameras and camera calibration | Lens distortion: radial and tangential; Camera calibration with a checkerboard; Direct linear transform (DLT): estimate a matrix from point pairs; Solving A x = 0 with the SVD (last right singular vector); Wide-angle cameras: fisheye and spherical models; Fiducial markers (AprilTag-style) | 88, MA-058, ML-053 | PE-006, PE-007, PE-008, PE-009, PE-010, PE-011 | HZ 7.4; RVC3 13.1.6; VO-I calibration; RVC3 13.2.2; Zhang 2000 [doi:10.1109/34.888718](https://doi.org/10.1109/34.888718); HZ 4.1, 7.1; HZ 4.1; MA-058 §6; VO-I omnidirectional; RVC3 13.3; RVC3 13.6.1 |
| 90 | Depth from stereo and depth cameras | Stereo camera model: disparity and depth; Dense stereo matching along rows; Stereo failure modes and depth error growing with distance; Depth cameras: structured light and time of flight; Image rectification | 88 | PE-060, PE-061, PE-062, PE-063, PE-044 | Barfoot 7.4.2; RVC3 14.4; Szeliski ch.12; RVC3 14.4.2; Szeliski ch.13; Newcombe et al. 2011 [doi:10.1109/ISMAR.2011.6092378](https://doi.org/10.1109/ISMAR.2011.6092378); HZ 11.12; RVC3 14.4.3 |
| 91 | Point clouds from depth images and LiDAR | Depth image to point cloud; How LiDAR works: time of flight, spinning vs solid-state, rings; Range-azimuth-elevation sensor model; Point clouds: storage and basic operations; Voxel-grid downsampling; other range sensors: radar (range and Doppler) and event cameras, named | 90, 74 | PE-064, PE-066, PE-067, PE-068, PE-069 | RVC3 14.7; Lee §2; RVC3 6.8; Barfoot 7.4.3; RO 57; Cadena §V; Rusu & Cousins 2011 [doi:10.1109/ICRA.2011.5980567](https://doi.org/10.1109/ICRA.2011.5980567); Rusu & Cousins 2011 |
| 92 | Aligning scans: normals, k-d trees and ICP | Normals and plane fitting (incl. ground removal); k-d tree for nearest-neighbour search; ICP: iterative closest point; Point-to-plane ICP and Generalized-ICP; Aligning two 3D point sets (SVD / Kabsch solution) | 91, 75, MA-060, ML-085 | PE-070, PE-071, PE-072, PE-073, PE-043 | RVC3 14.7.1; Lee §3.1; Besl & McKay 1992 [doi:10.1109/34.121791](https://doi.org/10.1109/34.121791); Barfoot 9.1; Chen & Medioni 1992 [doi:10.1016/0262-8856(92)90066-C](https://doi.org/10.1016/0262-8856(92)90066-C); Segal et al. 2009 [doi:10.15607/RSS.2009.V.021](https://doi.org/10.15607/RSS.2009.V.021); VO-I 3D-to-3D; RVC3 14.7.2 |
| 93 | Extrinsic and time calibration between sensors | Extrinsic and time calibration between sensors (camera-IMU, camera-LiDAR); H1 Extrinsic calibration: camera–LiDAR, camera–IMU, hand–eye; time offsets between sensors | 89, 91, 83 | PE-015, AU-034 | Furgale et al. 2013 [doi:10.1109/IROS.2013.6696514](https://doi.org/10.1109/IROS.2013.6696514); Huang §4; UDS C2 "Sensor and camera calibration"; Tsai & Lenz 1989, *hand/eye calibration* ([10.1109/70.34770](https://doi.org/10.1109/70.34770)); Kalibr ([repo](https://github.com/ethz-asl/kalibr)) |

### RO-04 Localization and maps for navigation

Where am I on a known 2D or 3D map, what is around me, and the cost map every planner reads.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 94 | Markov localization on a known map | tracking, global and kidnapped-robot localization; Markov localization; discrete, geometric and Monte Carlo localization compared; grid localization (histogram filter over poses) | 78, 71, 79 | PR 7.1, PR 7.2, PA 12.2, PR 8.1 | Thrun et al. 2005 ch.7; LaValle 2006 ch.12; Thrun et al. 2005 ch.8 |
| 95 | Monte Carlo localization and adaptive particle counts | Monte Carlo localization (MCL); augmented MCL: random particles to recover when lost; rejecting readings the map cannot explain; better proposal distributions; chi-square quantile to set a sample size; KLD-sampling | 82, 75, new MA: KL divergence, MA-045 | PR 8.2, PR 8.3, PR 8.8, PR 8.4, PR 8.6, PR 8.7 | Thrun et al. 2005 ch.8 |
| 96 | Occupancy grid mapping | occupancy grid map; inverse sensor model and log-odds cell update; fusing several sensors in one map | 79, 74 | PR 9.1, PR 9.2, PR 9.3 | Thrun et al. 2005 ch.9 |
| 97 | 3D maps: voxels, octrees, elevation maps and signed distance | B2 3D maps: voxel grids, octrees, elevation maps; 3D occupancy with octrees (OctoMap); Elevation maps for legged robots; Signed-distance (TSDF) maps (concept); Choosing a map type: landmarks, point clouds, voxels, elevation, meshes; surfel maps named | 96, 91 | AU-012, PE-077, PE-078, PE-079, PE-080 | FRE L10 "Techniques for 3D mapping"; NAV2 voxel layer; Hornung et al. 2013, *OctoMap* ([10.1007/s10514-012-9321-0](https://doi.org/10.1007/s10514-012-9321-0)); Cadena §V; Hornung et al. 2013 [doi:10.1007/s10514-012-9321-0](https://doi.org/10.1007/s10514-012-9321-0); Fankhauser et al. 2018 [doi:10.1109/LRA.2018.2849506](https://doi.org/10.1109/LRA.2018.2849506); Newcombe et al. 2011 |
| 98 | Layered costmaps: obstacles, inflation and keep-out zones | B1 Layered costmaps: static, obstacle and inflation layers, footprint, keep-out and speed zones | 96, 73 | AU-011 | NAV2 concepts "Environmental representation", costmap layers and filters; Lu, Hershberger, Smart 2014, *Layered costmaps* ([10.1109/IROS.2014.6942636](https://doi.org/10.1109/IROS.2014.6942636)) |
| 99 | Localizing in a prior 3D map: the normal distributions transform | C2 Localising against a prebuilt 3D map; the normal distributions transform (NDT); NDT scan matching | 92, 95, 97 | AU-016, PE-074 | AW localization "3D-LiDAR + point cloud map"; UDS C4 scan-matching localization; Biber & Straßer 2003, *The normal distributions transform* ([10.1109/IROS.2003.1249285](https://doi.org/10.1109/IROS.2003.1249285)); Lee §3.1; Biber & Strasser 2003 [doi:10.1109/IROS.2003.1249285](https://doi.org/10.1109/IROS.2003.1249285) |
| 100 | The SLAM problem | online SLAM vs full SLAM | 96, 94 | PR 10.1, PA 12.3 | Thrun et al. 2005 ch.10; LaValle 2006 ch.12 |
| 101 | Pose graphs and GraphSLAM | pose (constraint) graph; negative log posterior as a sum of quadratic terms; information form of a large SLAM problem; correspondence test in GraphSLAM; information form as a short section (full information filter stays optional) | 81, 100, new MA: Nonlinear least squares (Gauss-Newton), new MA: Schur complement, new MA: Sparse linear solves and conjugate gradient, MA-070 | PR 11.1, PR 11.2, PR 11.4, PR 11.7 | Thrun et al. 2005 ch.11 |
| 102 | Loop closure and map merging | loop closure; multi-robot map integration and alignment; Outliers in the back-end: robust kernels, switchable constraints (concept); Loop closure for a visual map (was PE-056) | 101, 75 | PR 13.6, PR 12.7, PE-107, PE-056 | Thrun et al. 2005 ch.13; Thrun et al. 2005 ch.12; Barfoot 5.3–5.4; Cadena §III |

### RO-05 Path planning: graph search, grids, samples and car-like robots

Global paths for real robot shapes and motion limits: grid search, sampling planners, Hybrid A*, lattices, route graphs, trajectory optimisation.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 103 | Graphs and uninformed search | graph as a model of a state space; breadth-first and depth-first search; algorithm cost: Big-O and exponential time; why exact planning is hard (NP-hard, PSPACE-hard) |  | PA 2.1, PA 2.2, PA 2.9, PA 6.8 | LaValle 2006 ch.2; LaValle 2006 ch.6 |
| 104 | Dijkstra's algorithm and priority queues | priority queue; Dijkstra's shortest-path algorithm | 103 | PA 2.3, PA 2.4 | LaValle 2006 ch.2 |
| 105 | A* and heuristics | A* search with an admissible heuristic; best-first search and iterative deepening; backward and bidirectional search; weighted A*, anytime A* (ARA*) and any-angle search (Theta*) named as variants | 104 | PA 2.5, PA 2.6, PA 2.7 | LaValle 2006 ch.2 |
| 106 | Grid path planning: wavefronts, navigation functions and value iteration | value iteration on a robot grid map; DP with interpolation on continuous spaces; feedback planning by DP with interpolation; navigation function with one minimum at the goal; grid wavefront propagation | 14, 96, ML-043, 104 | PR 14.7, PA 8.7, PA 14.7, PA 8.2 | Thrun et al. 2005 ch.14; LaValle 2006 ch.8; LaValle 2006 ch.14 |
| 107 | Moving through unknown maps: D* replanning and bug algorithms | D* fast replanning; bug algorithms in unknown spaces; D* Lite, named | 105, 96, 9 | PA 12.4, PA 12.5 | LaValle 2006 ch.12 |
| 108 | Collision checking and nearest neighbours in C-space | collision detection: broad and narrow phase; bounding-volume hierarchies; metric space: rules a distance must follow; distances on angles; kd-tree nearest-neighbour search with wrap-around angles; uniform random samples of rotations and directions | 73, 72, ML-085, MA-049, MA-029 | PA 5.7, PA 5.8, PA 5.1, PA 5.9, PA 5.3 | LaValle 2006 ch.5 |
| 109 | Potential fields | randomized potential fields: roll downhill, random-walk out of local minima | 73, MA-062 | PA 5.11 | LaValle 2006 ch.5 |
| 110 | Rapidly-exploring random trees (RRT) | rapidly-exploring random tree; RRT* and asymptotic optimality; PRM*, FMT* and SST* named | 108 | PA 5.12 | LaValle 2006 ch.5 |
| 111 | Probabilistic roadmaps (PRM) | probabilistic and visibility roadmaps; complete, resolution-complete and probabilistically complete planners | 110, 103 | PA 5.13, PA 5.14 | LaValle 2006 ch.5 |
| 112 | Planning with motion limits | kinodynamic planning and phase-space obstacles; reachable sets; motion primitives and a system simulator; lattice search; kinodynamic RRT; Dubins and Reeds-Shepp shortest car paths; Dubins and Reeds-Shepp curves; Kinodynamic planning | 110, 64, new MA: Numerical integration of ODEs, new MA: ODEs and vector fields | PA 14.1, PA 14.2, PA 14.4, PA 14.5, PA 14.6, PA 15.9, CT-095, CT-096 | LaValle 2006 ch.14; LaValle 2006 ch.15; robotics.md (PA 15.9); robotics.md (PA 14.1–14.6) |
| 113 | Hybrid A* and path smoothing | F2 Hybrid A*: A* whose nodes carry heading and whose edges are drivable arcs; F6 Path smoothing after a grid planner | 105, 112, 67, 98 | AU-026, AU-030 | Dolgov et al. 2010, *Path planning for autonomous vehicles in unknown semi-structured environments* ([10.1177/0278364909359210](https://doi.org/10.1177/0278364909359210)); NAV2 SmacPlannerHybrid; UDS C5; CMU wk 14–15; NAV2 Smoothers (simple, constrained, Savitzky-Golay) |
| 114 | State lattices and motion primitives | F3 State-lattice planning with motion primitives | 113 | AU-027 | Pivtoraiko & Kelly 2009, *state lattices* ([10.1002/rob.20285](https://doi.org/10.1002/rob.20285)); NAV2 SmacPlannerLattice; CMU wk 14–15 |
| 115 | Route planning on road and route graphs | B4 Route (mission) planning on a road or route graph; lane graphs as the road-network graph | 105, 65 | AU-014 | TOR C4 M4; S2 §II-A; S3 "route planning"; NAV2 Route Server; AW mission planner |
| 116 | Trajectory optimisation | gradient-based trajectory optimisation (shooting); Trajectory optimisation (gradient-based, shooting); Direct methods: single shooting, multiple shooting, collocation; Trajectory optimisation methods: multiple shooting, collocation, DDP/iLQR; direct vs indirect methods; Pontryagin's principle named only | 112, ML-056 | PA 14.9, CT-097, CT-072, ME-054 | LaValle 2006 ch.14; robotics.md (PA 14.9); MPC 8.5, WE22 V.A, PA16 IV.C; PA 14.9; Wensing V-A–V-C |

### RO-06 Feedback control and path tracking

From a planned path to wheel commands: judging a response, feedforward and cascades, driving to a goal, pure pursuit, Stanley, Kanayama.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 117 | PD and PID control | PD / PID feedback control: act on error, its derivative and integral; short section: Newtonian and rigid-body mechanics (F = ma, torque, inertia); Rigid-body dynamics (F = ma, torque, inertia); Basic PD/PID on a single axis | MA-061, new MA: Stability of dynamical systems | R0.7, CT-014, CT-105 | legged_gym; Stooke et al. 2020; MR 8.2, RVC3 3.2.1; robotics.md (RL R0.7) |
| 118 | Reading a controller's response: step response and second-order systems | Error dynamics and the step response (overshoot, settling time, damping); Error dynamics of a second-order system: overshoot, settling time, damping ratio, natural frequency | 117, new MA: Stability of dynamical systems | CT-034, ME-056 | MR 11.2 |
| 119 | Feedforward, integral action, cascaded loops and windup | Feedforward plus feedback; Feedforward plus feedback; motion vs force control; Integral action in state feedback; Integrator windup and actuator saturation; Cascaded control loops (fast inner loop, slower outer loop) | 118 | CT-037, ME-055, CT-035, CT-036, CT-038 | MR 11.3, RVC3 9.4.1; MR 11.1; FBS 7.4; FBS 11.4, 11.5; RVC3 9.1.6, 9.1.7, RAJ 5.4–5.5, SU22 II.A |
| 120 | Driving to a point, a line and a pose | Moving to a point; Following a line; Moving to a pose (position and heading), polar-coordinate controller | 66, 117 | CT-040, CT-041, CT-042 | RVC3 4.1.1.1; RVC3 4.1.1.2; RVC3 4.1.1.4 |
| 121 | Path following vs trajectory tracking: path coordinates and tracking errors | Path following vs trajectory tracking; Path coordinates (Frenet frame): distance along the path s, sideways offset, heading error; Cross-track error and heading error | 120, 67 | CT-043, CT-011, CT-044 | PA16 V (Problems V.1, V.2); SN09 3.1.1, RAJ 2.5, PA16 V; SN09 2, AR24 5.1.3, PA16 V |
| 122 | Pure pursuit | Pure pursuit; Look-ahead distance and its tuning (look-ahead grows with speed) | 121 | CT-045, CT-046 | Coulter 1992, SN09 2.2, PA16 V.A.1, RVC3 4.1.1.3; SN09 2.2.1 |
| 123 | The Stanley controller and rear-wheel feedback | Stanley controller (front-wheel feedback); Tuning the Stanley controller; Rear-wheel feedback path controller | 122 | CT-047, CT-048, CT-049 | Thrun 2006, Hoffmann 2007, SN09 2.3, PA16 V.A.3; SN09 2.3.1; PA16 V.A.2 |
| 124 | Tracking a timed trajectory: Kanayama and feedback linearisation | Kanayama tracker: error in the robot's own frame, virtual reference robot, Lyapunov-proved stable; Feedback linearisation | 121, 119, new MA: Stability of dynamical systems | CT-050, CT-039 | Kanayama 1990, PA16 V.B.1, MR 13.3.4; UR 3, PA16 V.B.2 |
| 125 | Feedforward on curves, tracker metrics and choosing a tracker | Feedforward steering from path curvature; Comparing trackers: speed, curvature, tuning effort; Tracker metrics: RMS and peak lateral error, steering effort | 123, 124 | CT-052, CT-053, CT-054 | SN09 4.3, RAJ 3.2; SN09 5, AR24 6; AR24 5.1.3 |

### RO-07 The classical navigation stack

Putting the parts together: the layered stack, ROS 2, simulators, DWA/TEB, behaviour trees and Nav2.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 126 | The autonomy stack: layers, rates and sensor choice | A2 The autonomy stack: sense–plan–act and the layers mission → behaviour → motion → control; A8 Choosing and placing sensors: coverage, range, redundancy, compute budget | 95, 106, 125 | AU-002, AU-009 | TOR C1 M2 L3, C4 M2; CMU wk 10 "hierarchical control"; S1 ch.1; S2 §II; S3; AW architecture; TOR C1 M2 L1–L2; ETH wk 4 |
| 127 | ROS 2: nodes, topics, services and actions | A3 ROS 2: nodes, topics, services, actions, parameters, launch, QoS, lifecycle nodes, bags, RViz | 126, 65 | AU-004 | NAV2 concepts "ROS 2"; UDR C3; Macenski et al. 2022, *Robot Operating System 2*, Sci. Robotics ([10.1126/scirobotics.abm6074](https://doi.org/10.1126/scirobotics.abm6074)); [ROS 2 concepts](https://docs.ros.org/en/jazzy/Concepts.html) |
| 128 | Physics simulators: time steps, contact and the main engines | J2 How a physics simulator steps: time step, contact and friction models; choosing Gazebo vs MuJoCo vs Isaac vs Drake | 70, new MA: Numerical integration of ODEs | AU-043 | M42 ch.5 "Contact simulation"; COR "Simulation"; M832 App. A (Drake, [drake.mit.edu](https://drake.mit.edu/)); [Gazebo docs](https://gazebosim.org/docs); [Isaac Sim docs](https://docs.isaacsim.omniverse.nvidia.com/latest/index.html); RL scope row R0.9 |
| 129 | Classical local planning: DWA and TEB | dynamic window approach: sample reachable velocities, score short trajectories; timed elastic band: optimise a timed path; Local planners as controllers (DWA, TEB) | 116, 96, 64, 98 | N.1, CT-055 | Fox, Burgard & Thrun 1997; Rosmann et al. 2017; robotics.md (RL N.1) |
| 130 | Behaviour trees, state machines and recovery behaviours | A5 Behaviour trees (sequence, fallback, decorator, tick) and finite state machines; A6 Recovery behaviours, goal and progress checks, waypoint following | 126, 127 | AU-006, AU-007 | NAV2 concepts "Behavior Trees"; Colledanchise & Ögren, *Behavior Trees in Robotics and AI* ([arXiv 1709.00084](https://arxiv.org/abs/1709.00084)); NAV2 plugins: Behaviors, Goal Checkers, Progress Checkers, Waypoint Task Executors |
| 131 | The Nav2 navigation stack and ROS tooling | Nav2: global planner, costmaps, AMCL localization, DWB and MPPI controllers; navigation simulators and tooling: Gazebo + ROS, Isaac Lab, Habitat, Flightmare, CrowdNav; Classical stack: global planner + local planner; MPPI and regulated pure pursuit named as Nav2 controllers | 129, 95, 105, 127, 130, 98, 122, 128 | N.26, RL §5.1 decision 2026-10-03 'The Nav2 navigation stack' (second background Note), RS-024 | Macenski et al. 2020; Nav2 docs; Koenig & Howard 2004; Savva et al. 2019; Song et al. 2020 (Flightmare); CrowdNav repo; Xiao §2 |

### RO-08 Robot RL foundations and sim-to-real

Turning a robot into an MDP and getting a simulator-trained policy onto hardware.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 132 | Why robot RL is hard | why robot RL is hard; value-function vs policy-search methods on robots; using models, demonstrations and prior knowledge; Why robot RL is hard: high dimensions, costly real samples, model errors, goal specification; Map of robot competencies: locomotion, navigation, manipulation, mobile manipulation, HRI, multi-robot | 39, 42 | R0.1, R0.2, R0.3, RS-001, RS-012 | Kober, Bagnell & Peters 2013; CS285 2023 L23; Kober §3; Ibarz §1; Tang §3.1 |
| 133 | The robot as an MDP | control rate, observation, action interface, episode and reset; Formulation and solution axes: action level, observation type, reward density; sim use, expert data, on/off-policy/offline optimiser | 132, 7 | R0.4, RS-013 | legged_gym config; Tang §3.2-3.3 |
| 134 | Action spaces: torques, PD targets, velocity commands | joint position targets tracked by a PD controller; choosing the action space; PD joint targets under an RL policy | 133, 117 | R0.5, R0.6, CT-111 | legged_gym; Hwangbo et al. 2019; Peng & van de Panne 2017; Chen et al. 2022; Tai et al. 2017; robotics.md (RL R0.5) |
| 135 | Parallel simulation and the reference training stack | massively parallel on-policy training on one GPU; simulators and frameworks (Isaac Lab, MuJoCo, Gazebo, Habitat); reading legged_gym + rsl_rl; Simulators for robot learning | 134, 39 | R0.8, R0.9, R0.10, RS-097 | Rudin et al. 2022; Makoviychuk et al. 2021; Isaac Lab 2025; Todorov et al. 2012; Zhao §III-F |
| 136 | Delays and control rate: acting while the robot keeps moving | Delays and control rate: the robot keeps moving while the policy thinks | 134, 135 | RS-009 | Ibarz §4.8 |
| 137 | The reality gap and domain randomization | sim-to-real gap; visual domain randomization; dynamics randomization; sensor noise and latency modelling; Zero-shot transfer with domain randomization and pushes; System ID, domain randomization, domain adaptation | 135, DL-050 | R1.1, R1.2, R1.3, R1.9, RS-089, RS-050 | Tobin et al. 2017; Peng et al. 2018; Sadeghi & Levine 2017; Zhao §III-A, §III-C, §III-E; Muratore §5.1; Ha §5.2-5.4 |
| 138 | Visual domain adaptation: making sim and real images look alike | Visual domain adaptation: make sim and real images look alike, or share features | 137, DL-050, new DL: Generative adversarial networks | RS-006 | Ibarz §4.3.3; Zhao §III-D |
| 139 | System identification and actuator models | system identification and actuator networks; delta (residual) action model learned from real data; delta action model for agile humanoid skills; first quadruped sim-to-real: simple reward + actuator model + randomisation; System identification; H2 Odometry and actuator calibration; Simulation-based inference: fit a distribution over sim parameters to real data | 137, DL-010, ML-049 | R1.5, R1.6, H.8, L.2, RS-090, AU-035, RS-094 | Tan et al. 2018; Hwangbo et al. 2019; He et al. 2025 (ASAP); Zhao §III-B; Muratore §4.6; RO 83; Muratore §4.8 |
| 140 | Real-robot training and sim-real agreement | training on the real robot instead; does sim performance predict real performance?; Measuring the reality gap; Learning on real robots for days: automatic resets, reset-free learning, a changing world | 139, 42 | R1.7, R1.8, RS-093, RS-008 | Haarnoja et al. 2019; Kadian et al. 2020; Muratore §3.4; Ibarz §4.7, §4.12; Tang §5 |
| 141 | Robust RL: training against the worst case or an adversary | Robust RL: train against the worst case or an adversary (robust MDP, RARL, adversarial DR) | 137, 39 | RS-092 | Muratore §5.3; García §3.1; Brunke §3.2.4 |

### RO-09 Designing the robot task: observations, rewards, curricula

What the policy sees, what it is paid for, when episodes end, how training gets harder.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 142 | Proprioceptive observations | proprioceptive observation design; projected gravity as an orientation feature | 133, ML-023, new MA: 3D rotations: Euler angles and quaternions | R2.1, R2.2 | legged_gym; Rudin et al. 2022 |
| 143 | Seeing the terrain: exteroceptive inputs | height samples, scandots, depth and laser inputs | 142, 96 | R2.3 | Miki et al. 2022; Cheng et al. 2024 |
| 144 | Goal- and command-conditioned policies | command- and goal-conditioned policies | 142, 9 | R2.4 | Andrychowicz et al. 2017 |
| 145 | Reward = task terms + regularisation terms | task terms plus penalty terms; exponential tracking kernel | 144, MA-024 | R2.5, R2.6 | legged_gym; Kim et al. 2024 |
| 146 | Reward shaping and its risks | reward shaping and reward hacking; designing reward signals: sparse, shaped, imitation, inverse RL | 145 | R2.8, SB17.4 | Sutton&Barto 2018 ch.17; Ma et al. 2024 (Eureka) |
| 147 | Gaits from rewards and behaviour families | gait shaping: feet air time, clearance, energy; gaits emerging from energy minimisation; a family of behaviours in one policy | 146 | R2.7, L.8, R2.13 | Margolis & Agrawal 2022; Fu et al. 2021 |
| 148 | Terminations and the sign of rewards | terminations cut future reward; negative rewards teach early falls | 145, 8 | R2.9 | legged_gym; Chane-Sane et al. 2024 |
| 149 | Curricula: terrain, commands and automatic domain randomization | game-inspired terrain curriculum; grid-adaptive command curriculum; widen randomisation ranges when the policy succeeds at the edge; Adaptive domain randomization (tune ranges from results) | 144, 137 | R2.10, R1.4, RS-091 | Rudin et al. 2022; Margolis et al. 2022; OpenAI et al. 2019; Muratore §5.2 |
| 150 | Sparse rewards and hindsight relabelling | Hindsight Experience Replay; goal-conditioned manipulation with sparse rewards | 144, 36, 40 | R2.11, M.5 | Andrychowicz et al. 2017; SB3 HER docs |
| 151 | Symmetry augmentation | mirrored data augmentation and mirror loss | 142, DL-050 | R2.12 | Mittal et al. 2024; Su et al. 2024 |
| 152 | Searching for rewards automatically | evolutionary search over reward weights and network shape (AutoRL); reward code written by a language model; Rewards from success classifiers and goal images; LLM-written rewards | 146 | N.16, R2.15, RS-010, RS-118 | Chiang et al. 2019; Ma et al. 2024 (Eureka, DrEureka); Ibarz §4.9; Firoozi §III-C |

### RO-10 Navigation I: the learned navigation policy

Replace the local planner with a learned policy: task, observations, actions, rewards, evaluation.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 153 | POMDPs and belief space | partially observable MDP; planning in belief / information space; observations, state and the state-update function; robot control as a POMDP | 11, 78 | PR 15.1, PA 11.6, PA 12.1, SB17.3, R3.1 | Thrun et al. 2005 ch.15; LaValle 2006 ch.11; LaValle 2006 ch.12; Sutton&Barto 2018 ch.17; Lee et al. 2020 |
| 154 | Learned vs classical local planners | what RL buys and costs vs DWA/TEB; Learning only the local planner; Hybrid learned-plus-classical systems for safety and explainability; learning that duplicates, replaces or improves a classical part | 129, 132 | N.2, RS-026, RS-030 | Xiao et al. 2022; Kahn et al. 2018; Song et al. 2023; Xiao §3.2.2; Xiao §6.2 |
| 155 | Navigation as an MDP or POMDP | point-goal, object-goal and image-goal tasks; termination and time limit; fixed vs moving goals; geometric vs non-geometric sensing | 154, 153, 133 | N.3 | Anderson et al. 2018; Savva et al. 2019 |
| 156 | Mapless end-to-end navigation | laser ranges + goal to velocity commands, no map; Learning the whole stack end to end (mapless) | 155, 40 | N.4, RS-025 | Tai, Paolo & Liu 2017; Zhu & Zhang 2021; Xiao §3.1; Zhu & Zhang |
| 157 | Observations for navigation: laser, vision and maps | down-sampled ranges, goal in robot frame, stacked scans; RGB/depth, target image, egocentric occupancy or costmap | 156, 142, 143, DL-040 | N.5, N.6 | Tai et al. 2017; Long et al. 2018; Zhu et al. 2017; Chaplot et al. 2020; Hoeller et al. 2021 |
| 158 | Action spaces for navigation | (v, omega), discrete moves, waypoints, commands to a locomotion policy | 156, 134 | N.7 | Tai et al. 2017; Wijmans et al. 2020; Lee et al. 2024 |
| 159 | Reward design for navigation | arrival, progress, collision, time and smoothness terms | 158, 146 | N.8 | Tai et al. 2017; Long et al. 2018 |
| 160 | Sparse, time-limited goal rewards | reward only for being at the target at the end of a time budget | 159, 150 | N.9 | Rudin et al. 2022b |
| 161 | Evaluating navigation: success, SPL, collisions | success rate, SPL, collisions and time; K2 Navigation benchmarks and protocols: BARN, Habitat challenges, social-navigation metrics; H3 Ground truth: motion capture and how pose error is measured; Judging real-world success: lab vs diverse real settings; reproducible real benchmarks | 155 | N.19, AU-046, AU-036, RS-014 | Anderson et al. 2018; Wijmans et al. 2020; Perille et al. 2020, BARN ([arXiv 2008.13315](https://arxiv.org/abs/2008.13315)); Batra et al. 2020, ObjectNav ([arXiv 2006.13171](https://arxiv.org/abs/2006.13171)); Francis et al. 2023, social navigation evaluation ([arXiv 2306.16740](https://arxiv.org/abs/2306.16740)); ETH wk 4 "Motion capture systems"; Tang §3.4, §5 |

### RO-11 Partial observability, privileged learning and adaptation

The robot cannot see the full state: memory, privileged critics and teachers, adaptation, learned estimators, pixel RL.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 162 | History encoders: memory for a hidden state | frame stacks, temporal convolution, GRU/LSTM and transformer history encoders | 153, DL-061, DL-064, DL-042, DL-082 | R3.2 | Lee et al. 2020; Radosavovic et al. 2024 |
| 163 | Privileged information | privileged information: what sim knows and the robot does not; Curriculum, hierarchical, privileged training | 162 | R3.3, RS-049 | Chen et al. 2019 (Learning by Cheating); Ha §4 |
| 164 | Asymmetric actor-critic | critic sees the full state, actor sees observations | 163, 32 | R3.4 | Pinto et al. 2018; Nahrendra et al. 2023 |
| 165 | Behaviour cloning, compounding error and DAgger | behaviour cloning and compounding error; DAgger: label the states the learner visits | 163, ML-049, DL-014 | R3.5, R3.6, RS-061 | Ross et al. 2011; CS285 2023 L2; Zare §II |
| 166 | Teacher-student distillation | privileged RL teacher, sensor student trained on its own rollouts; Distillation into a deployable student | 165, 164, DL-071 | R3.7, RS-095 | Chen et al. 2019; Lee et al. 2020; Miki et al. 2022; Zhao §II-D |
| 167 | Online adaptation modules (RMA) | extrinsics latent and an adaptation module from history; Online adaptation | 166, 162 | R3.8, RS-096 | Kumar et al. 2021 (RMA); Muratore §4.7; Ha §5.4 |
| 168 | Learned state estimators: explicit and latent | estimator network trained with the policy (velocity, foot height, contact); history encoder predicting velocity and a latent terrain code; Learned state estimators for legged robots | 167, 80, new DL: Variational autoencoder, new DL: Contrastive learning objective | R3.9, R3.11, PE-108 | Ji et al. 2022; Nahrendra et al. 2023; Long et al. 2023; RO 103 |
| 169 | In-context adaptation with sequence models | adaptation from history without weight updates; humanoid walking sim-to-real with a causal transformer, zero-shot; In-context learning for decisions | 162, 137, DL-087 | R3.13, H.3, RS-115 | Radosavovic et al. 2024; OpenAI et al. 2019; Firoozi §III-D |
| 170 | Auxiliary tasks and general value functions | general value functions; auxiliary losses (depth, loop closure) for representation | 162, 25 | R3.14, SB17.1 | Sutton&Barto 2018 ch.17; Mirowski et al. 2017; DeepMind x UCL 2021 L13 |
| 171 | Multi-task and meta-RL: learning to adapt to a new task fast | Multi-task and meta-RL: learn to adapt fast to a new task | 169, 167 | RS-011 | Ibarz §4.10; Zhao §II-E; Muratore §4.2 |
| 172 | RL from pixels: image augmentation and contrastive auxiliary losses | K8 RL from pixels: image augmentation and contrastive auxiliary losses | 170, DL-050, new DL: Contrastive learning objective | AU-053 | Laskin et al. 2020, CURL ([arXiv 2004.04136](https://arxiv.org/abs/2004.04136)); Kostrikov et al. 2020, DrQ ([arXiv 2004.13649](https://arxiv.org/abs/2004.13649)) |

### RO-12 Seeing objects and people

Learned perception a navigating robot needs: detection, segmentation, LiDAR obstacles, semantic maps, tracking and prediction.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 173 | Object detection: boxes, IoU, non-max suppression and mAP | Object detection: boxes and class labels; Intersection over union (IoU) and mean average precision (mAP); Non-maximum suppression; Using pretrained detectors and segmenters; D1 2D object detection: boxes, scores, non-max suppression, mAP; traffic-light recognition as a detection task | DL-040, DL-051, ML-076, 88 | PE-109, PE-110, PE-111, PE-118, AU-017 | Zou §II.A road map; RVC3 12.1.4; Zou §II.B; Zou §II.C; DL-053; TOR C3; UDS C2; M42 ch.9; S237B wk 4; AW object recognition / traffic lights; Redmon et al. 2016 YOLO ([arXiv 1506.02640](https://arxiv.org/abs/1506.02640)) |
| 174 | Detector families: two-stage and one-stage | Two-stage detectors (Faster R-CNN); One-stage detectors (YOLO, SSD) | 173 | PE-112, PE-113 | Zou §II.A; Ren et al. 2015 [arXiv:1506.01497](https://arxiv.org/abs/1506.01497); Redmon et al. 2016 [arXiv:1506.02640](https://arxiv.org/abs/1506.02640); Liu et al. 2016 SSD [arXiv:1512.02325](https://arxiv.org/abs/1512.02325) |
| 175 | Semantic segmentation | Semantic segmentation: a class per pixel (FCN); Encoder-decoder segmentation (U-Net); D2 Semantic segmentation; road and lane detection as segmentation | 173, DL-042 | PE-114, PE-115, AU-018 | Minaee §3; Long et al. 2015 [arXiv:1411.4038](https://arxiv.org/abs/1411.4038); RVC3 12.1.1; Minaee §3.3; Ronneberger et al. 2015 [arXiv:1505.04597](https://arxiv.org/abs/1505.04597); TOR C3 (drivable surface); UDS C12; M42 ch.9; NAV2 semantic-segmentation layer; Long et al. 2015 FCN ([arXiv 1411.4038](https://arxiv.org/abs/1411.4038)) |
| 176 | Obstacles in point clouds: ground removal, clustering and 3D boxes | D4 Point-cloud obstacles: ground removal, clustering, 3D boxes from LiDAR | 91, 173 | AU-020 | UDS C3, C11 (PCL); AW obstacle segmentation, radar; NAV2 ground-consistency layer; Lang et al. 2019 PointPillars ([arXiv 1812.05784](https://arxiv.org/abs/1812.05784)) |
| 177 | Semantic maps and traversability costs | Semantic maps: putting labels into the 3D map; Traversability from geometry and semantics; Terrain-aware and off-road navigation: learn traversability from experience | 175, 97, 98 | PE-116, PE-117, RS-031 | Cadena §VI; Chen §4.2; Fankhauser 2018; Xiao §4.2.1; Tang §4.2.1 |
| 178 | Multi-object tracking | D3 Multi-object tracking: one Kalman filter per object, association, track birth and death; Data association and Mahalanobis gating | 173, 80, new MA: Mahalanobis distance, new MA: Assignment problem (Hungarian algorithm) | AU-019, PE-106 | UDS C3 multi-target tracking; TOR C3; S3 "moving obstacles tracking"; AW; Bewley et al. 2016 SORT ([arXiv 1602.00763](https://arxiv.org/abs/1602.00763)); Weng et al. 2020 AB3DMOT ([arXiv 1907.03961](https://arxiv.org/abs/1907.03961)); RO 161 |
| 179 | Predicting where people and vehicles go, and collision checks in time | E1 Motion prediction: constant velocity, manoeuvre-based, learned multi-modal forecasts; ADE/FDE; Human trajectory prediction for planning: constant velocity, social force model, learned predictors; E2 Collision checks against moving obstacles; time to collision; risk assessment and driving style named | 178, 108, DL-064 | AU-022, RS-033, AU-023 | TOR C4 M5; UDS C9; AW object recognition "predicts trajectories"; Rudenko et al. 2020 ([arXiv 1905.06113](https://arxiv.org/abs/1905.06113)); Salzmann et al. 2020 Trajectron++ ([arXiv 2001.03093](https://arxiv.org/abs/2001.03093)); Shi et al. 2022 MTR ([arXiv 2209.13508](https://arxiv.org/abs/2209.13508)); Mavrogiannis §3.1; TOR C4 M5 "time to collision" |

### RO-13 Navigation II: exploring, remembering and learning parts of the stack

Long-range navigation: exploration, memory, options, object goals, topological maps, and learned costmaps, planner parameters and planners.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 180 | Exploration by information gain and active localization | expected information gain of an action; greedy and multi-step exploration; Monte Carlo exploration; moving to become sure of the pose; active SLAM: choosing motions that improve the map | 153, 82, ML-091, 95 | PR 17.1, PR 17.2, PR 17.3, PR 17.4 | Thrun et al. 2005 ch.17 |
| 181 | Exploring to build a map | exploration for occupancy grids (cell entropy, gain spread by value iteration) | 180, 106 | PR 17.5 | Thrun et al. 2005 ch.17 |
| 182 | Curiosity and intrinsic rewards for exploration | K6 Curiosity and intrinsic rewards for exploration; Visual exploration: cover a new house fast (coverage, curiosity, novelty rewards) | 181, 39, 4 | AU-051, RS-037 | Pathak et al. 2017, ICM ([arXiv 1705.05363](https://arxiv.org/abs/1705.05363)); Burda et al. 2018, RND ([arXiv 1810.12894](https://arxiv.org/abs/1810.12894)); Duan §III-A |
| 183 | Memory and auxiliary tasks for visual navigation | recurrent navigation policy with depth and loop-closure prediction | 157, 170 | N.10 | Mirowski et al. 2017; Zhu et al. 2017 |
| 184 | Options: temporal abstraction | options as temporally extended actions; Long-horizon tasks by composing skills (hierarchical RL) | 158, 7 | SB17.2, RS-018 | Sutton&Barto 2018 ch.17; Tang §5; Kroemer §8 |
| 185 | Planners plus RL | roadmap edges kept only if the RL policy can drive them (PRM-RL) | 111, 156, 184 | N.15 | Faust et al. 2018; Francis et al. 2020 |
| 186 | Modular learned navigation vs end-to-end | learned SLAM + global and local policies + analytic planner | 185, 96, 181 | N.17 | Chaplot et al. 2020 |
| 187 | Object-goal navigation with a semantic map | Embodied goal types: PointNav, ImageNav, ObjectNav; Object-goal navigation by a semantic map + exploration policy (modular) | 186, 177, 155 | RS-038, RS-039 | Duan §III-B; Tang §4.2.1; Sun (ObjectNav) |
| 188 | Topological maps: navigating over a graph of places | Topological maps: navigate over a graph of places | 186, 103 | RS-043 | Gu VLN §4.1.3; Firoozi §III-F |
| 189 | Inverse RL: recovering a reward from demonstrations | Inverse RL: recover the reward from demos (max-entropy IRL); I3 Inverse RL and adversarial imitation (GAIL) | 165, 146, 14, ML-091 | RS-066, AU-039 | Ravichandar §3.2.2; Zare §III; Ho & Ermon 2016, GAIL ([arXiv 1606.03476](https://arxiv.org/abs/1606.03476)); COR "Reward shaping and learning"; S237B wk 7–8 |
| 190 | Learned costmaps and learned planner parameters | Learned costmaps from demonstrations (inverse RL for navigation); Learning planner parameters (tune DWA/TEB settings from demos or RL) | 189, 129, 98 | RS-028, RS-029 | Xiao §3.3.1; Xiao §3.3.2, §6.2 |
| 191 | Learned global planners: value iteration networks and neural A* | Learning the global planner: learned heuristics, planning as a network (value iteration networks, neural A*) | 106, 14, DL-040 | RS-027 | Xiao §3.2.1 |

### RO-14 Safety and constraints

Say what not to do: constrained MDPs, Lagrangian/CPO/barrier methods, risk, shields, barrier-function filters, safe exploration.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 192 | Constrained MDPs and cost critics | constrained MDP; cost signals and cost critics; Constrained MDPs, Lagrangian and CPO | 7, 32, MA-066 | R4.1, R4.2, RS-098 | Altman 1999; Achiam et al. 2017; García §3.3; Gu safe §3.1.1 |
| 193 | Lagrangian and PID-Lagrangian PPO | learned multiplier by gradient ascent on violation (PPO-Lagrangian); multiplier update as a PID controller | 192, 39, MA-067, 117 | R4.3, R4.4 | Ray et al. 2019; Stooke et al. 2020 |
| 194 | CPO, barriers and penalties | trust-region constrained update (CPO); log-barrier methods (IPO); exact penalty methods (P3O) | 193, 38, MA-068 | R4.5, R4.6, R4.7 | Achiam et al. 2017; Liu et al. 2020; Zhang et al. 2022 |
| 195 | Not only rewards but also constraints: constraint types for real robots | probabilistic and average constraints; task in reward, rest as constraints; side-by-side comparison on a quadruped; safe-RL benchmarks and libraries; Safe RL benchmarks: Safety Gym, Safety-Gymnasium, safe-control-gym | 194 | R4.8, R4.9, R4.13, RS-105 | Kim et al. 2024 (T-RO); Lee et al. 2023; Safety-Gymnasium; OmniSafe; Gu et al. 2022; Gu safe §6; Brunke §4 |
| 196 | Constraints as terminations | violation sets a termination probability | 195, 148 | R4.10 | Chane-Sane et al. 2024 (CaT) |
| 197 | Shields, safety filters and recovery policies | shields and safety filters; recovery policies and reach-avoid values; Safe exploration with outside knowledge: demos, teacher advice; Formal methods and shields | 192 | R4.11, R4.12, RS-100, RS-104 | Alshiekh et al. 2018; He et al. 2024 (ABS); García §4.1; Gu safe §3.1.3 |
| 198 | Risk-sensitive RL: caring about bad outcomes | Risk-sensitive RL: care about bad outcomes, not just the average (variance, CVaR) | 192, MA-008 | RS-099 | García §3.2; Brunke §3.2.2 |
| 199 | Lyapunov certificates and control barrier function filters | Control barrier functions and safety filters (QP that minimally edits the action); Stability certificates with Lyapunov functions | 197, 194, MA-068, new MA: Stability of dynamical systems | RS-103, RS-102 | Brunke §3.3.2; Gu safe §3.1.2; Brunke §3.3.1 |
| 200 | Safe exploration with an uncertainty model | Safe exploration with an uncertainty model (Gaussian process, SafeOpt, learning MPC) | 199, ML-new: Gaussian processes | RS-101 | Brunke §3.1, §3.2.1; Gu safe §3.1.4 |

### RO-15 Trajectories, LQR and MPC

Timed references, then optimal feedback: polynomial and spline trajectories, speed profiles, LQR, linear and nonlinear MPC, MPPI.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 201 | Time scaling and polynomial trajectories | Path vs trajectory; time scaling s(t); Path vs trajectory; time scaling; Cubic and quintic polynomials from boundary conditions; Cubic and quintic polynomial time scaling; Trapezoidal velocity profile; Trapezoidal velocity profile and S-curve | 121, ML-060, ML-053 | CT-084, ME-048, CT-085, ME-050, CT-086, ME-051 | MR 9.1; MR 9.2, RVC3 3.3.1; MR 9.2.2 |
| 202 | Via points, splines and minimum-jerk trajectories | Via points and multi-segment trajectories; continuity at the joins; Via points and spline trajectories; Cubic splines; Minimum-jerk trajectories; Interpolating orientation (slerp); Dynamically feasible vs infeasible references | 201, new MA: 3D rotations: Euler angles and quaternions | CT-087, ME-052, CT-088, CT-089, CT-093, CT-094 | MR 9.3, RVC3 3.3.2, 3.3.3; MR 9.3; MR 9.3, RVC3 3.3.3; Flash & Hogan 1985; RVC3 3.3.4; SU22 VI.C–D |
| 203 | Speed profiles along a fixed path | Time-optimal time scaling under speed and acceleration limits; Time-optimal time scaling under torque limits (phase plane); F5 Speed planning: stop lines, following distance, comfort limits along a fixed path | 201, 67 | CT-092, ME-053, AU-029 | MR 9.4; TOR C4 M8 "velocity profile generation"; AW behaviour velocity planner, obstacle stop / adaptive cruise |
| 204 | State feedback, controllability and pole placement | State feedback u = −Kx and pole placement; Controllability (reachability) and the rank test | 118, new MA: State-space models, new MA: Matrix exponential and logarithm, MA-056 | CT-033, CT-031 | FBS 7.2, 7.3, RAJ 3.1; FBS 7.1, MPC 1.3.5, 2.4.4 |
| 205 | LQR: the linear-quadratic regulator | Hamilton-Jacobi-Bellman equation; linear-quadratic regulator and the Riccati equation; Discrete-time LQ problem solved by dynamic programming (Riccati recursion); Infinite-horizon LQR and the steady Riccati equation; Choosing the Q and R weights; HJB equation | 204, 14 | PA 15.6, PA 15.7, CT-057, CT-058, CT-059, CT-109 | LaValle 2006 ch.15; MPC 1.3.1–1.3.3; MPC 1.3.4, 1.3.6, UR 8; SN09 4.2.1; robotics.md (PA 15.6) |
| 206 | LQR for tracking: references, feedforward and time-varying gains | LQR for tracking a reference (error coordinates, steady-state target); Time-varying LQR to hold a robot on a planned trajectory; LQR with feedforward; Linearising a model around an operating point or a moving reference | 205, 119, 116, MA-064 | CT-060, CT-062, CT-063, CT-030 | MPC 1.5.1; UR 8; SN09 4.3, MR 11.3; FBS 6.4, PA16 V |
| 207 | Model predictive control: receding horizon, constraints and the QP | Receding horizon: plan N steps, apply the first, re-plan; Input and state constraints (steering limits, speed limits, keep-out zones); Linear MPC as a quadratic program (stack the predictions, condensed vs sparse); Terminal cost and terminal set; why a short horizon can fail; Unconstrained MPC equals LQR | 205, MA-068 | CT-064, CT-065, CT-066, CT-067, CT-068 | MPC 1.3, NG20 III; MPC 1.2.5, 2.5.4; MPC 1.3.1, 8.8, NG20 III.A; MPC 2.4.2, 2.6; MPC 2.5.1 |
| 208 | Nonlinear MPC and solving it in real time | Disturbances and offset-free MPC; Nonlinear MPC; Linear vs nonlinear MPC: accuracy against compute; Newton-type solvers: SQP and interior point (overview only); Real-time MPC: warm starts, real-time iteration, stopping early | 207, 116, MA-064 | CT-069, CT-070, CT-071, CT-073, CT-074 | MPC 1.5.2, 5.5; MPC 2.5.5, NG20 III.B, SU22 IV.A; NG20 III.C; MPC 8.6, 8.7; MPC 8.9, 2.7 |
| 209 | MPC for path following | MPC for path following on the bicycle model | 207, 121, 67 | CT-075 | PA16 V.C, Kong 2015 |
| 210 | Sampling-based MPC: MPPI | Sampling-based MPC: model predictive path integral (MPPI) | 207, new MA: Monte Carlo estimation, 43, 131 | CT-076 | Williams 2016 |
| 211 | MPC and RL: comparing and combining | MPC vs RL, and combining them | 210, 154, 39 | CT-079 | NG20 III.E, WE22 VII, SU22 VIII |

### RO-16 Navigation III: people, crowds and the real world

Many agents and people, billions of frames, real-robot data, sim-to-real, safety, and fast flight from quadrotor control to learned agile flight.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 212 | Multi-agent collision avoidance and social norms | value network over joint configuration (CADRL); social norms in the reward; Multi-robot and crowd navigation with RL | 155, 25 | N.11, N.12, RS-032 | Chen et al. 2017 (CADRL, SA-CADRL); Zhu & Zhang; Tang §4.6.1 |
| 213 | Crowds and robot teams: attention pooling and shared policies | summarising a variable set of neighbours; one PPO policy for every robot; multi-stage training | 212, DL-061, DL-073, 39 | N.13, N.14 | Everett et al. 2018; Chen et al. 2019 (SARL); Long et al. 2018 |
| 214 | Multi-agent RL: centralised training, decentralised execution | G3 Multi-agent RL: centralised training with decentralised execution, shared policies, value factorisation; Multi-robot RL: decentralised agents, centralised training (CTDE, MAPPO) | 213, 39, 164 | AU-033, RS-017 | Rashid et al. 2018 QMIX ([arXiv 1803.11485](https://arxiv.org/abs/1803.11485)); Yu et al. 2022 MAPPO ([arXiv 2103.01955](https://arxiv.org/abs/2103.01955)); Tang §4.6; Gu safe §3.3 |
| 215 | Social navigation: norms, coupled prediction and planning, evaluation | Coupled prediction and planning (the robot's move changes theirs); Social norms: personal space (proxemics), legibility, groups; Evaluating social navigation: metrics and protocols; E3 Interaction-aware planning: my plan changes their behaviour | 212, 179 | RS-034, RS-035, RS-036, AU-024 | Mavrogiannis §3.2; Mavrogiannis §4; Singamaneni; Mavrogiannis §5; S237B wk 9 "Interaction-aware learning, planning and control" |
| 216 | Navigation at scale | photoreal simulators and distributed PPO to billions of frames (DD-PPO); Embodied AI simulators: Habitat, iGibson, AI2-THOR | 131, 135 | N.18, RS-044 | Savva et al. 2019; Wijmans et al. 2020; Duan §II |
| 217 | Self-supervised real-world navigation | labels from the robot's own events (collision, bumpiness) | 140, 155 | N.20 | Kahn et al. 2018; Kahn et al. 2021 (BADGR); Gandhi et al. 2017 |
| 218 | Sim-to-real for navigation | randomised rendering, laser-only inputs, measured sim-real agreement | 137, 140, 157 | N.21 | Sadeghi & Levine 2017; Tai et al. 2017; Kadian et al. 2020 |
| 219 | Safety in navigation | collision limits as constraints, shields and recovery for navigation; Safe locomotion and safety filters | 197, 196, 159 | N.25, RS-057 | He et al. 2024; Alshiekh et al. 2018; Ha §8.4 |

### RO-17 Aerial robots: quadrotors and agile flight

3D rigid-body dynamics, quadrotor model and control, flat trajectories, learned agile flight

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 220 | Rigid-body dynamics in 3D: Euler's equation and the inertia matrix | One rigid body in 3D: F = ma plus Euler's equation; the 3×3 inertia matrix | new MA: 3D rotations: Euler angles and quaternions, 84 | ME-036 | MR 8.2.1 |
| 221 | The quadrotor model | mixer: four thrusts to thrust and three torques; 3D dynamics; underactuation: tilt to move | 220, 84 | CT-098, CT-099, CT-100 | Mahony et al. 2012; Corke 2023 (RVC3) 4.2; Sun et al. 2022 §III.B |
| 222 | Hovering and cascaded quadrotor control | linearise at hover, LQR or PID; attitude loop inside position loop | 221, 119, 205 | CT-101, CT-102 | Tedrake, Underactuated Robotics ch.3; Sun et al. 2022 §II.A |
| 223 | Differential flatness | state and inputs from position, yaw and derivatives | 222 | CT-103 | Mellinger & Kumar 2011 |
| 224 | Minimum-snap trajectories and time allocation | piecewise polynomials as a QP; time per segment | 223, 202, MA-068 | CT-090, CT-091 | Mellinger & Kumar 2011; Richter et al. 2016 |
| 225 | Geometric control and MPC for quadrotors | large-angle control on SE(3); quadrotor NMPC; INDI named | 224, 208 | CT-104, CT-078 | Lee et al. 2010; Sun et al. 2022 §IV |
| 226 | Agile aerial navigation | privileged expert imitated by a sensor policy; RL for drone racing; RL vs optimal control; RL for agile flight; RL for quadrotor flight control; Legged and aerial navigation | 166, 139, 116, 225 | N.24, CT-106, RS-021, RS-045 | Loquercio et al. 2021; Kaufmann et al. 2023; Song et al. 2023; robotics.md (RL N.24); Tang §4.1.3; Tang §4.2.2-4.2.3 |

### RO-18 Vision for motion: features, optical flow and visual odometry

How a camera alone measures motion: calibration between sensors, features, matching, optical flow, two-view geometry, VO and bundle adjustment.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 227 | Image gradients, pyramids and corner features | Image filtering: smoothing and gradient filters; Image pyramids (coarse-to-fine); Point features (keypoints): why corners are easy to find again; Harris and Shi-Tomasi corners and the structure tensor; FAST corner detector | 88, DL-042, MA-056 | PE-013, PE-014, PE-016, PE-017, PE-018 | RVC3 11.5.1; DL-042 §6; RVC3 11.7.3; Baker 2.3.4; VO-II feature detection; RVC3 12.3; VO-II; Harris & Stephens 1988 [doi:10.5244/C.2.23](https://doi.org/10.5244/C.2.23); Rosten et al. 2010 [doi:10.1109/TPAMI.2008.275](https://doi.org/10.1109/TPAMI.2008.275) |
| 228 | Descriptors and matching: SIFT and ORB | Scale-space blobs, descriptors and SIFT; ORB: binary descriptors and Hamming distance; Matching descriptors (nearest neighbour, ratio test, mutual check) vs tracking | 227, ML-085 | PE-019, PE-020, PE-021 | VO-II; RVC3 12.3.2; Lowe 2004 [doi:10.1023/B:VISI.0000029664.99615.94](https://doi.org/10.1023/B:VISI.0000029664.99615.94); Rublee et al. 2011 [doi:10.1109/ICCV.2011.6126544](https://doi.org/10.1109/ICCV.2011.6126544); VO-II feature matching; ML-085 |
| 229 | RANSAC and homographies | RANSAC: fit a model despite wrong matches; Homography: the map between two views of a plane | 228, 89, MA-031 | PE-022, PE-023 | VO-II outlier removal; Fischler & Bolles 1981 [doi:10.1145/358669.358692](https://doi.org/10.1145/358669.358692); Barfoot 5.4.1; HZ 4.1, 4.8, 13; RVC3 13.6.2 |
| 230 | Optical flow: brightness constancy, Lucas-Kanade and KLT | Optical flow: the apparent motion of each pixel; Brightness constancy and the optical-flow constraint; Lucas-Kanade: local flow by least squares in a window; Pyramidal KLT tracker | 227, ML-053 | PE-024, PE-025, PE-026, PE-027 | Szeliski ch.9; Baker 2.1.1; Horn & Schunck 1981 [doi:10.1016/0004-3702(81)90024-2](https://doi.org/10.1016/0004-3702(81)90024-2); Lucas & Kanade 1981 ([IJCAI PDF](https://www.ijcai.org/Proceedings/81-2/Papers/017.pdf)); ML-053; Baker 2.3.4; Shi & Tomasi 1994 |
| 231 | Dense and learned flow, and ego-motion from flow | Horn-Schunck: dense flow with a smoothness term; Learned optical flow; Image motion from camera motion (the image Jacobian); Ego-motion and time-to-contact from flow | 230, DL-040 | PE-028, PE-029, PE-030, PE-031 | Horn & Schunck 1981; Baker 2.2; Chen §3.1; Teed & Deng 2020, RAFT [arXiv:2003.12039](https://arxiv.org/abs/2003.12039); RVC3 15.2.1; Szeliski ch.9; RVC3 15.2.3 |
| 232 | Epipolar geometry: essential and fundamental matrices | Epipolar geometry: epipoles, epipolar lines; Essential matrix E (calibrated cameras); Fundamental matrix F (uncalibrated cameras); Normalised 8-point algorithm; 5-point algorithm (concept only) | 229, new MA: Cross product and skew-symmetric matrix, MA-058 | PE-032, PE-034, PE-035, PE-036, PE-037 | HZ 9.1; RVC3 14.2; HZ 9.6; RVC3 14.2.2; HZ 9.2; RVC3 14.2.1; HZ 11.2; RVC3 14.2.3; VO-I 2D-to-2D; Nistér 2004 [doi:10.1109/TPAMI.2004.17](https://doi.org/10.1109/TPAMI.2004.17) |
| 233 | Relative pose, triangulation and PnP | Recovering R and t from E; the four-solution check; Scale ambiguity of a single camera; Triangulation; PnP: camera pose from known 3D points (EPnP); Reprojection error | 232 | PE-038, PE-039, PE-040, PE-041, PE-042 | HZ 9.6.2; VO-I; VO-I monocular; HZ 12.2; RVC3 14.3.1; VO-I triangulation; VO-I 3D-to-2D; RVC3 13.2.4; Lepetit et al. 2009 [doi:10.1007/s11263-008-0152-6](https://doi.org/10.1007/s11263-008-0152-6); HZ 4.2-4.3, 12.3 |
| 234 | Visual odometry: mono and stereo, feature-based and direct | Visual odometry: chaining frame-to-frame motions; Drift: why odometry error grows; Monocular vs stereo VO; Direct vs feature-based (indirect) methods: photometric error; Learned odometry (visual, inertial) and learned SLAM parts; Learned depth from one image (concept) | 233, 230, 90, 68 | PE-045, PE-046, PE-047, PE-048, PE-059, PE-065 | VO-I formulation; VO-I; RO 51; VO-I mono vs stereo; VO-II dense methods; Huang §3.4; Engel et al. 2018 DSO [doi:10.1109/TPAMI.2017.2658577](https://doi.org/10.1109/TPAMI.2017.2658577); Chen §3, §6; Chen §4.1; Eigen et al. 2014 [arXiv:1406.2283](https://arxiv.org/abs/1406.2283) |
| 235 | Structure from motion and bundle adjustment | Structure from motion: cameras and points from many photos; Bundle adjustment; Sparsity and the Schur complement in bundle adjustment; Levenberg-Marquardt; Robust cost functions (Huber, Cauchy) | 234, new MA: Nonlinear least squares (Gauss-Newton), new MA: Schur complement | PE-049, PE-050, PE-051, PE-052, PE-053 | VO-I/II; Szeliski ch.11; RVC3 14.3; HZ 18.1; Barfoot 10.1; VO-II windowed BA; RO 165; HZ 4.5; Barfoot 4.3; Barfoot 5.4; Cadena §III |
| 236 | Visual SLAM: place recognition and ORB-SLAM | VO vs visual SLAM; front-end vs back-end; Visual place recognition with bag of words; ORB-SLAM as a worked system: tracking, local mapping, loop closing threads | 235, 100, 102 | PE-054, PE-055, PE-057 | Cadena §II; VO-I VO vs V-SLAM; Gálvez-López & Tardós 2012 [doi:10.1109/TRO.2012.2197158](https://doi.org/10.1109/TRO.2012.2197158); VO-II loop constraints; RO 167; Mur-Artal et al. 2015 [doi:10.1109/TRO.2015.2463671](https://doi.org/10.1109/TRO.2015.2463671); Campos et al. 2021 ORB-SLAM3 [doi:10.1109/TRO.2021.3075644](https://doi.org/10.1109/TRO.2021.3075644) |
| 237 | Evaluating odometry and SLAM | Evaluating odometry and SLAM: trajectory error, drift %, benchmarks | 234, 161 | PE-058 | Cadena §III; Lee §8.2; Geiger et al. 2012 KITTI [doi:10.1109/CVPR.2012.6248074](https://doi.org/10.1109/CVPR.2012.6248074) |

### RO-19 Navigation with language and foundation models

Open-vocabulary goals and spoken routes: vision-language models, language-queryable maps, zero-shot ObjectNav, VLN, navigation foundation models.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 238 | Vision-language models for robots | Vision-language models (CLIP-style image-text matching) | DL-071, new DL: Contrastive learning objective, DL-053 | RS-109 | Firoozi §II-D |
| 239 | Open-vocabulary 3D semantic maps | Open-vocabulary 3D semantic maps (language-queryable maps) | 238, 177 | RS-112 | Firoozi §IV-C |
| 240 | Zero-shot object navigation with vision-language models | Zero-shot, open-vocabulary navigation with vision-language models | 239, 187 | RS-040 | Sun (ObjectNav); Firoozi §III-F |
| 241 | Vision-and-language navigation: task, datasets and metrics | K7 Vision-and-language navigation; Vision-and-language navigation: task, R2R dataset, metrics | 155, 238, DL-083 | AU-052, RS-041 | Anderson et al. 2018, VLN ([arXiv 1711.07280](https://arxiv.org/abs/1711.07280)); Gu VLN §2-3 |
| 242 | Vision-and-language navigation methods | VLN methods: cross-modal attention, graph memory, data augmentation (speaker-follower) | 241, 188 | RS-042 | Gu VLN §4 |
| 243 | Navigation foundation models | goal-conditioned navigation models from many robots (GNM, ViNT); diffusion policy (NoMaD); Navigation foundation models | 155, 188, 238, 165, new DL: Diffusion models | N.27, RS-120 | Shah et al. 2023 (GNM, ViNT); Sridhar et al. 2024 (NoMaD); Tang §5 |

### RO-20 Autonomous driving

Navigation for cars: automation levels, HD maps, behaviour planning, Frenet planning, system safety, open- vs closed-loop evaluation.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 244 | Driving automation levels and modular vs end-to-end stacks | A1 Levels of driving automation and the operating domain (ODD); A2b Modular vs end-to-end stacks for driving | 126, 186 | AU-001, AU-003 | TOR C1 M1; SAE J3016 ([sae.org](https://www.sae.org/standards/content/j3016_202104/)); S3; S4 §III; Chen et al. 2023 [arXiv 2306.16927](https://arxiv.org/abs/2306.16927) |
| 245 | HD and vector maps | B3 HD / vector maps: lanes as a graph with rules attached; point-cloud maps | 115, 65 | AU-013 | AW map design (vector map: lanes, crosswalks, stop lines, traffic lights); S3 "road mapping"; Poggenhans et al. 2018, *Lanelet2* ([10.1109/ITSC.2018.8569929](https://doi.org/10.1109/ITSC.2018.8569929)) |
| 246 | Behaviour planning for driving | F1 Behaviour planning: lane keep, lane change, yield, stop, using rules and state machines | 130, 245, 179 | AU-025 | TOR C4 M6; UDS C5; S2 §II-B; S3 "behavior selection"; AW behaviour path/velocity planners |
| 247 | Frenet-frame trajectory planning | F4 Frenet-frame planning: sample lateral and longitudinal curves along the lane, then pick the cheapest | 121, 202, 203, 246 | AU-028 | Werling et al. 2010, *Optimal trajectory generation … in a Frenét frame* ([10.1109/ROBOT.2010.5509799](https://doi.org/10.1109/ROBOT.2010.5509799)); UDS C5; TOR C4 M8 |
| 248 | System safety: monitoring, fail-safe stops and safety cases | A7 System monitoring, fail-safe and the minimal-risk manoeuvre; A9 Safety assurance: hazard analysis, functional safety (ISO 26262), scenario testing | 197, 126 | AU-008, AU-010 | AW AD-API fail-safe / diagnostics / operation modes; AW planning "Validation"; TOR C1 M3 (safety assurance, frameworks, testing); UDS C13 (functional safety, hazard analysis and risk assessment) |
| 249 | Evaluating driving: open vs closed loop, simulators and scenarios | J3 Driving simulators and scenario-based testing; K3 Open-loop vs closed-loop evaluation of driving planners | 179, 128, 161 | AU-044, AU-047 | TOR C1 M7, C4 final project; Dosovitskiy et al. 2017 CARLA ([arXiv 1711.03938](https://arxiv.org/abs/1711.03938)); Caesar et al. 2021, nuPlan ([arXiv 2106.11810](https://arxiv.org/abs/2106.11810)); CARLA leaderboard ([leaderboard.carla.org](https://leaderboard.carla.org/)); Chen et al. 2023 |

### RO-21 Car dynamics and steering control *(optional)*

Optional: tyres, forces and LQR steering for fast cars.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 250 | The dynamic bicycle model, slip angle and cornering stiffness | Dynamic bicycle model (sideways force, yaw rate, yaw inertia); Tyre slip angle; Cornering stiffness: the linear tyre model | 67, 117 | CT-015, CT-016, CT-017 | RAJ 2.3, PA16 III.B, SN09 4.1; RAJ 2.3, SN09 4.1; SN09 4.1, RAJ 2.3 |
| 251 | Tyre limits: saturation and longitudinal slip | Tyre force saturation and friction limit; Longitudinal slip ratio: why driving and braking force depends on slip | 250 | CT-018, CT-019 | SN09 4.1 (tyre data figures), PA16 III.B; RAJ 4.1.2, 4.1.3 |
| 252 | Longitudinal dynamics and cruise control | Longitudinal dynamics: aerodynamic drag and rolling resistance; Cruise control: upper level (wanted acceleration) and lower level (throttle, brake) | 251, 119 | CT-020, CT-023 | RAJ 4.1.1, 4.1.4; RAJ 5.3–5.5 |
| 253 | Road error dynamics and LQR steering | Error dynamics with respect to the road (lateral and yaw error states); LQR steering on the dynamic bicycle model | 250, 206 | CT-021, CT-061 | RAJ 2.5, 2.6; SN09 4.2, RAJ 3.1, AR24 4.1 |
| 254 | Steady cornering and understeer | Steady-state cornering and understeer | 250 | CT-022 | RAJ 3.3 |
| 255 | Preview control and gain scheduling | Preview (look-ahead) control; Gain scheduling / linear parameter-varying control; linear parameter-varying (LPV) control, named | 253 | CT-051, CT-056 | RAJ 3.11, SN09 4.4; PA16 V.D |

### RO-22 State estimation and SLAM in depth *(optional)*

Optional: UKF and information filters, landmark SLAM, GraphSLAM, FastSLAM, factor graphs, visual-inertial and LiDAR-inertial odometry.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 256 | Unscented Kalman filter | unscented transform and sigma points; unscented Kalman filter (UKF); Unscented Kalman filter | 81, new MA: Cholesky factor | PR 3.11, PR 3.12, PE-093 | Thrun et al. 2005 ch.3; RO 158 |
| 257 | Information filter | canonical form: information matrix and vector; information filter and extended information filter | 80, new MA: Woodbury identity | PR 3.13, PR 3.14 | Thrun et al. 2005 ch.3 |
| 258 | EKF and UKF localization | EKF localization with landmarks; UKF localization | 94, 81, 256, 76 | PR 7.3, PR 7.8 | Thrun et al. 2005 ch.7 |
| 259 | Data association and multi-hypothesis tracking | the correspondence problem; maximum-likelihood data association with gating; mixture-of-Gaussians belief; multi-hypothesis tracking | 258, new MA: Mahalanobis distance, MA-070, MA-073 | PR 7.4, PR 7.5, PR 3.9, PR 7.7 | Thrun et al. 2005 ch.7; Thrun et al. 2005 ch.3 |
| 260 | Learned sensor models and MAP mapping | learning the inverse sensor model from simulated data; MAP estimate of a whole map; MAP occupancy mapping with forward models | 96, MA-072, DL-014 | PR 9.4, PR 9.5, PR 9.6 | Thrun et al. 2005 ch.9 |
| 261 | EKF SLAM | EKF SLAM with known correspondence; landmark initialization | 100, 258 | PR 10.2, PR 10.3 | Thrun et al. 2005 ch.10 |
| 262 | EKF SLAM with unknown landmarks | provisional landmarks; feature selection and map management; incremental data association; equivalence constraints between landmarks | 261, 259 | PR 10.4, PR 10.5, PR 12.4, PR 12.6 | Thrun et al. 2005 ch.10; Thrun et al. 2005 ch.12 |
| 263 | Factor graphs, sliding windows and IMU preintegration | Filtering vs optimisation (sliding window); Factor graphs (beginner level); IMU preintegration; incremental smoothing (iSAM), named | 101, 84 | PE-098, PE-099, PE-100 | Huang §3.1; Dellaert & Kaess 2017 [doi:10.1561/2300000043](https://doi.org/10.1561/2300000043); Cadena §II; Huang §3.5; Forster et al. 2017 [arXiv:1512.02363](https://arxiv.org/abs/1512.02363) |
| 264 | Visual-inertial odometry: MSCKF, VINS and initialisation | Filter-based VIO (MSCKF, concept); Optimisation-based VIO (VINS-Mono as worked system); VIO initialisation: gravity, scale and biases | 263, 234, 87 | PE-101, PE-102, PE-103 | Huang §3.1; Mourikis & Roumeliotis 2007 [doi:10.1109/ROBOT.2007.364024](https://doi.org/10.1109/ROBOT.2007.364024); Huang §3.2; Qin et al. 2018 VINS-Mono [doi:10.1109/TRO.2018.2853729](https://doi.org/10.1109/TRO.2018.2853729); Huang §3.6 |
| 265 | LiDAR odometry and LiDAR-inertial odometry | Feature-based LiDAR odometry: edge and plane points; Degenerate scenes: long corridors and open fields; LiDAR-inertial odometry (loose and tight) | 263, 92, 99 | PE-075, PE-076, PE-105 | Lee §3.2; Zhang & Singh 2014 LOAM [doi:10.15607/RSS.2014.X.007](https://doi.org/10.15607/RSS.2014.X.007); Lee §7.3; Lee §4 |
| 266 | FastSLAM: particles over paths | Rao-Blackwellization: sample the path, landmarks become independent; FastSLAM 1.0; FastSLAM 2.0 improved proposal; per-particle data association; grid-based FastSLAM; entropy decomposition in SLAM; exploring with FastSLAM | 82, 261 | PR 13.1, PR 13.2, PR 13.3, PR 13.4, PR 13.7, PR 17.7 | Thrun et al. 2005 ch.13 |
| 267 | Multi-robot exploration | coordinating several exploring robots | 181, 102 | PR 17.6 | Thrun et al. 2005 ch.17 |

### RO-23 Planning in depth *(optional)*

Optional: exact POMDP planning, exact roadmaps, time and many robots, coverage, task allocation.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 268 | Exact POMDP planning: alpha vectors | piecewise-linear convex value function (alpha vectors); value iteration in belief space; pruning value-function pieces | 153, 14 | PR 15.2, PR 15.3, PR 15.4 | Thrun et al. 2005 ch.15 |
| 269 | Approximate POMDP planning | QMDP; augmented MDP (mean + entropy summary); Monte Carlo POMDP with particle beliefs | 268, 82 | PR 16.1, PR 16.2, PR 16.3 | Thrun et al. 2005 ch.16 |
| 270 | Exact roadmaps | vertical cell decomposition; maximum-clearance roadmap (generalized Voronoi diagram); shortest-path roadmap (visibility graph) | 73, 105 | PA 6.1, PA 6.2, PA 6.3 | LaValle 2006 ch.6 |
| 271 | Planning with time and many robots | time-varying obstacles and velocity tuning; centralized vs decoupled (prioritized) multi-robot planning; decoupled planning: path first, then timing | 111, 112 | PA 7.1, PA 7.2, PA 14.8 | LaValle 2006 ch.7; LaValle 2006 ch.14 |
| 272 | Multi-agent path finding | G1 Multi-agent path finding: prioritised planning, conflict-based search | 271, 105 | AU-031 | Stern et al. 2019, *Multi-Agent Pathfinding* ([arXiv 1906.08291](https://arxiv.org/abs/1906.08291)); Sharon et al. 2015, *Conflict-based search* ([10.1016/j.artint.2014.11.006](https://doi.org/10.1016/j.artint.2014.11.006)) |
| 273 | Coverage planning | coverage planning: visit every part of an area | 270 | PA 7.7 | LaValle 2006 ch.7 |
| 274 | Task allocation and fleet management | G2 Task allocation and fleet management: auctions, assignment | 272, new MA: Assignment problem (Hungarian algorithm) | AU-032 | Gerkey & Matarić 2004, *Task allocation in multi-robot systems* ([10.1177/0278364904045564](https://doi.org/10.1177/0278364904045564)); Open-RMF ([docs](https://openrmf.readthedocs.io/en/latest/)) |

## RB: Robot bodies: legs, humanoids and arms


### RB-01 Rigid-body motion and arm kinematics

Twists and screws, product of exponentials, Jacobians, singularities, inverse kinematics.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 275 | Twists, wrenches and screw motion | Twist: angular and linear velocity of a body as one 6-number vector; the adjoint map that moves it between frames; Screw axis and exponential coordinates of a rigid motion; Wrench: force and torque as one 6-number vector; moving it between frames | 84, 69, new MA: Matrix exponential and logarithm, new MA: Cross product and skew-symmetric matrix | ME-009, ME-010, ME-011 | MR 3.3.2; MR 3.3.3; MR 3.4 |
| 276 | Forward kinematics by the product of exponentials; workspace | Product of exponentials: hand pose from screw axes, in the base frame and the hand frame; how it compares with DH; Task space and workspace: where the hand can reach | 275, 69 | ME-021, ME-015 | MR 4.1.1–4.1.3, C.5; MR 2.5 |
| 277 | The manipulator Jacobian and statics | Manipulator Jacobian (space and body forms): joint speeds to hand twist; Analytic Jacobian (rates of Euler angles) vs geometric Jacobian; Statics: joint torques that hold a hand force, τ = Jᵀ F | 276, MA-063 | ME-022, ME-023, ME-024 | MR 5.1.1–5.1.4; MR 5.1.5; MR 5.2 |
| 278 | Singularities, manipulability and redundancy | Singularities: the Jacobian loses rank and the hand cannot move in some direction; Manipulability ellipsoid and measure; Redundancy and self-motion in the null space | 277, MA-057, MA-058, new MA: Null-space projector and weighted pseudo-inverse | ME-025, ME-026, ME-027 | MR 5.3; MR 5.4; Yoshikawa 1985; MR 6.3; Siciliano ch.3 |
| 279 | Inverse kinematics: analytic and numerical | The IK problem: none, one, many or infinitely many answers; Analytic IK: 2-link planar arm, wrist-splitting for 6-joint arms; Newton–Raphson for solving equations (root finding); Numerical IK: iterate with the Jacobian pseudo-inverse | 277, MA-064, MA-060 | ME-028, ME-029, ME-030, ME-031 | MR ch.6 intro; MR 6.1, 6.1.1–6.1.2; MR 6.2.1; MR 6.2.2 |
| 280 | Damped, transpose and differential IK; straight-line hand motion | Damped least squares IK; Jacobian-transpose IK; Differential (inverse velocity) IK: q̇ = J⁺ V, and its use for tracking a moving target; Straight-line paths in joint space and in task space (including SE(3)) | 279, 278, ML-063, 201 | ME-032, ME-033, ME-034, ME-049 | Wampler 1986; Nakamura & Hanafusa 1986; Siciliano ch.3; MR 6.3; MR 9.2.1 |

### RB-02 Dynamics and arm control

The manipulator equation and the controllers built on it: computed torque, operational space, force, impedance.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 281 | Lagrangian mechanics and the manipulator equation | Lagrangian mechanics: L = kinetic − potential energy; Euler–Lagrange equation on a 2-link arm; Manipulator equation M(q)q̈ + c(q,q̇) + g(q) = τ; what the mass matrix means | 220, MA-066 | ME-037, ME-038 | MR 8.1.1; Tedrake App. B; MR 8.1.2–8.1.3 |
| 282 | Inverse and forward dynamics | Recursive Newton–Euler inverse dynamics (torques for a wanted motion); Forward dynamics: solve for accelerations, then integrate | 281, 128 | ME-039, ME-040 | MR 8.1.4, 8.3; MR 8.5 |
| 283 | Motors, gears and the joint torque loop | Motors, gearing, reflected inertia, friction, flexible joints; Low-level joint torque control loop | 282, 139 | ME-043, ME-067 | MR 8.9.1–8.9.5; MR 11.8 |
| 284 | Joint-space control: velocity inputs, PD plus gravity, computed torque | Control with velocity inputs, in joint space and task space; PD plus gravity compensation; Independent-joint (decentralised) control vs centralised control; Computed torque (inverse dynamics control, feedback linearisation) | 281, 118, 119 | ME-057, ME-058, ME-059, ME-060 | MR 11.3.1–11.3.3; MR 11.4.1; Siciliano ch.8; MR 11.4.2 |
| 285 | Task-space and operational space control | Task-space motion control with torque inputs; Operational space control: task-space inertia, Jᵀ F, dynamically consistent null space; Dynamics in task space: the hand's apparent mass Λ = (J M⁻¹ Jᵀ)⁻¹ | 284, 277, 278 | ME-061, ME-062, ME-041 | MR 11.4.3; Khatib 1987; MR 8.6 |
| 286 | Force control and hybrid motion-force control | Force control; Hybrid motion–force control; natural and artificial constraints | 285 | ME-063, ME-064 | MR 11.5; MR 11.6.1–11.6.2 |
| 287 | Impedance and admittance control | Impedance control: behave like a virtual spring and damper; Admittance control | 286 | ME-065, ME-066 | MR 11.7.1; Hogan 1985; MR 11.7.2 |

### RB-03 Contact, grasping and manipulation planning

What a touch allows, when a grasp holds, contact as switching dynamics, and planning pick-and-place.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 288 | Contact kinematics, contact types and the friction cone | Contact kinematics: rolling, sliding, breaking free; Contact types: point without friction, point with friction, soft finger; Coulomb friction and the friction cone (and its pyramid approximation); Contact forces and the friction cone | 275, MA-067 | ME-078, ME-079, ME-080, CT-024 | MR 12.1.1–12.1.2; MR 12.1.5; Sahbani 2012; MR 12.2.1; WE22 III.A, UR 5 |
| 289 | Contact forces and contact as a hybrid system | Constrained dynamics: contact forces as Lagrange multipliers; Contact as a hybrid system: modes switch on touch-down and lift-off; impacts; Complementarity contact model: force only when touching, touching only when force; Contact scheduling: fixed gait sequence vs contact-implicit planning | 288, 281 | ME-042, ME-044, ME-045, ME-046 | MR 8.7; Wensing III-A1; Tedrake ch.17; Wensing III-A2; Wensing III-B |
| 290 | Form closure, force closure and the grasp matrix | Form closure; Force closure; Grasp matrix: contact forces to object wrench | 288, new MA: Convex hull | ME-081, ME-082, ME-083 | MR 12.1.6–12.1.7; MR 12.2.3; MR 12.2; Sahbani 2012 |
| 291 | Grasp quality and grasp selection | Grasp quality: the largest push a grasp can resist; Analytic vs data-driven grasp synthesis; known, familiar and unknown objects; K4 Grasp selection: antipodal grasps, friction cones, grasp quality, grasps from point clouds | 290, 91 | ME-084, ME-085, AU-048 | Ferrari & Canny 1992; Bohg et al. 2014; Sahbani 2012; M42 ch.5 grasp selection; S237B wk 4–5 |
| 292 | Manipulation planning | transit and transfer moves; preimage planning and nonprehensile manipulation (pushing); Manipulation beyond grasping: pushing, nonprehensile; Manipulation planning (transit and transfer) | 111, 69 | PA 7.4, PA 12.7, ME-086, ME-087 | LaValle 2006 ch.7; LaValle 2006 ch.12; MR 12.3; PA 7.4 |
| 293 | Task and motion planning | K3b Task-level planning: task and motion planning, language models choosing skills | 292, 130 | AU-049 | M42 ch.5 "Programming the task level"; Garrett et al. 2021, TAMP ([arXiv 2010.01083](https://arxiv.org/abs/2010.01083)); Ahn et al. 2022, SayCan ([arXiv 2204.01691](https://arxiv.org/abs/2204.01691)) |
| 294 | Tactile sensing | K5 Tactile sensing; Tactile sensing on hands, feet and body | 288 | AU-050, RS-085 | M42 ch.12; Gu hum §III |

### RB-04 Legged robots: balance and model-based control

Gaits, ZMP and the inverted pendulum, capture point, centroidal dynamics, convex MPC and whole-body control.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 295 | Gaits, support polygons and the floating base | Gait vocabulary: walk, trot, pace, bound, gallop; stance and swing; duty factor; Centre of mass, support polygon, static vs dynamic balance; Floating base: a legged robot's body is 6 extra unpowered degrees of freedom | 289, 220, new MA: Convex hull | ME-088, ME-089, ME-017 | Raibert 1986; Tedrake ch.4; Kajita ch.3; Tedrake 5; Wensing II-B; Tedrake App. B |
| 296 | Zero-moment point and the linear inverted pendulum | Centre of pressure and zero-moment point (ZMP); Linear inverted pendulum model (LIPM); Simplified models: linear inverted pendulum (LIP), single rigid body, centroidal dynamics; Zero-moment point (ZMP) and ZMP walking | 295, new MA: State-space models | ME-090, ME-091, CT-080, CT-081 | Tedrake 5 (CoP and ZMP); Vukobratović & Borovac 2004; Kajita 2001; Kajita ch.4; WE22 IV, UR 4, UR 5; UR 5 |
| 297 | ZMP walking with preview control | ZMP walking: footsteps, then ZMP path, then CoM path by preview control | 296, 206 | ME-092 | Tedrake 5 (ZMP planning); Kajita 2003 |
| 298 | Capture point and push recovery | Capture point: where to step to stop; Divergent component of motion (3D capture point) control | 296 | ME-093, ME-094 | Pratt et al. 2006; Tedrake 5 (push recovery); Englsberger et al. 2015 |
| 299 | Hopping and running: SLIP, Raibert's controller and passive walkers | Spring-loaded inverted pendulum (SLIP) for running; Passive walkers, limit cycles and Poincaré maps; Raibert hopping controller: foot placement for speed, thrust for height, hip torque for posture | 296, 117 | ME-095, ME-096, ME-097 | Tedrake 4 (SLIP); Tedrake 4 (rimless wheel, compass gait); Raibert 1986; Tedrake 4 (MIT Leg Lab hoppers) |
| 300 | Central pattern generators | Central pattern generators (CPGs); Structured action spaces: central pattern generators, foot-trajectory generators | 295, 134 | ME-098, RS-048 | Ijspeert 2008; Ha 1.3; Ha §3.4 |
| 301 | Centroidal dynamics and the single rigid body model | Centroidal dynamics: only contact forces and gravity change the whole body's momentum; centroidal momentum matrix; Single rigid body model of a quadruped | 295, 275 | ME-099, ME-100 | Orin et al. 2013; Tedrake 5 (centroidal dynamics); Wensing IV-A; Di Carlo et al. 2018; Wensing IV-B |
| 302 | Convex MPC for legged robots | Convex MPC for legged robots: choose foot forces by a QP over a short horizon; Convex MPC for legged robots (single rigid body, ground reaction forces, QP); Contact schedule (gait timing) as a fixed input to MPC; MPC with simplified models (inverted pendulum, centroidal); Whole-body and mixed-fidelity MPC | 301, 288, 207, 289 | ME-101, CT-077, CT-082, RS-082, ME-102 | Di Carlo et al. 2018; Gu V-A; Di Carlo 2018, WE22 IV; WE22 III.B, Di Carlo 2018; Gu hum §V; Gu V-B–V-C |
| 303 | Whole-body control: tasks and null-space priority | Tasks and task Jacobians: any quantity to control (hand pose, CoM, posture) is a "task"; Strict task priority by null-space projection; Whole-body control in closed form (prioritised operational space control) | 285, 278 | ME-070, ME-071, ME-072 | Wensing VI-A1–VI-A2; Gu VI-A; Siciliano & Slotine 1991; Moro & Sentis; Sentis & Khatib 2005; Gu VI-B |
| 304 | QP-based whole-body control | QP-based whole-body control: one quadratic program with weighted tasks, dynamics, contact and torque limits; Hierarchical QP (stack of tasks): strict priorities with inequalities; Inequality tasks: joint limits, torque limits, collision avoidance; WBC as the layer that tracks a plan from a simpler model; Whole-body control: a QP that turns wanted forces and motions into joint torques; Whole-body control as a QP with task priorities; Whole-body motion generation and control for humanoids | 303, 302, MA-068 | ME-073, ME-074, ME-075, ME-077, CT-083, RS-083, ME-107 | Gu VI-C; Wensing VI-B; Escande et al. 2014; Wensing VI-B2; Wensing VI-A4; Wensing II-D; WE22 II.D, VI, UR 5; Gu hum §VI; Kajita ch.5; Gu VI |
| 305 | Legged state estimation: leg kinematics fused with the IMU | Legged state estimation: fuse leg kinematics with the IMU | 86, 277, 81 | ME-104 | Bloesch et al. 2013 |
| 306 | Multi-contact planning | Multi-contact planning (search, optimisation, learning); Multi-contact planning (where to place hands and feet) | 302 | ME-103, RS-086 | Gu IV; Gu hum §IV |

### RB-05 Learned locomotion

The PPO locomotion recipe and its extensions, model-based plus learned control, bipeds, legged navigation, loco-manipulation.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 307 | The PPO locomotion recipe, end to end | PD targets + proprioception + tracking/penalty rewards + terrain curriculum + randomisation + teacher-student; Deep RL for locomotion (PPO recipe); Locomotion MDP parts: sim or real dynamics, proprio/extero observations, reward terms, PD joint targets | 149, 166, 196 | L.1, RS-046, RS-047 | Rudin et al. 2022; Lee et al. 2020; Hwangbo et al. 2019; Ha §2.2; Ha §3.1-3.4 |
| 308 | Perceptive locomotion | attention-based recurrent fusion of proprioception and a noisy height map | 307, 143 | L.3 | Miki et al. 2022 |
| 309 | Agility: high speed and parkour | adaptive velocity curriculum + online system identification for running; soft-then-hard obstacle curriculum; distil skills into one depth policy with DAgger; parkour-style learning on humanoids; Hard terrain and parkour | 308, 167, 165 | L.4, L.5, H.10, RS-056 | Margolis et al. 2022; Zhuang et al. 2023; Cheng et al. 2024; Zhuang et al. 2024; Ha §8.3 |
| 310 | Tracking model-based reference motions | RL learns to track a planner reference (DTC) | 307, 116, 302 | L.7 | Jenelten et al. 2024 |
| 311 | Model-based and learned legged control: comparing and combining | Model-based vs learned legged control: what each does well; Combining control and learning: learn controller parameters, learn a high-level policy over MPC/WBC, use MPC to guide RL; Learning inside a model-based controller (learned corrections to MPC); Learned high-level policy over a model-based low level (choose footholds or gait, MPC executes); Model-based vs learning-based control: when each wins | 310, 302, 304, 211 | ME-105, ME-106, RS-052, RS-053, RS-084 | Ha §6; Gu IX-A; Ha 6.1–6.4; Gu VII-D; Ha §6.1; Ha §6.2; Gu hum §IX-A |
| 312 | Biped walking with RL: gait clocks and periodic rewards | From quadrupeds to bipeds: gait clocks, periodic rewards, biped sim-to-real | 307, 297 | RS-054 | Ha §7; Tang §4.1.2 |
| 313 | Navigation on legged and wheeled-legged robots | learned navigation over a locomotion policy; end-to-end locomotion + local navigation; skill hierarchies for agile navigation (parkour); hierarchical RL for wheeled-legged urban missions; Wheeled-legged robots | 309, 160, 184, 166 | N.22, L.6, N.23, RS-058 | Hoeller et al. 2021; Rudin et al. 2022b; Hoeller et al. 2024; Lee et al. 2024; Ha §8.5 |
| 314 | Loco-manipulation: walking and using arms together | Loco-manipulation: walk and use arms (or a leg) together; Loco-manipulation in WBC: the held object as an external wrench | 313, 304, 285 | RS-059, ME-076 | Ha §8.6; Gu hum §VII-F; Gu VI-D1 |
| 315 | Unsupervised skill discovery | Unsupervised skill discovery: learn many distinct skills with no task reward (DIAYN) | 184, 307, new MA: Mutual information | RS-019 | Ha §8.1; Tang §5 |
| 316 | Differentiable simulators | Differentiable simulators: gradients through physics | 128, 116, 282 | RS-055 | Ha §8.2 |

### RB-06 Humanoids: learning motion from humans

Human motion data and retargeting, adversarial and tracking imitation, teleoperation, multi-skill controllers.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 317 | Human motion data and kinematic retargeting | Human motion data: motion capture, video, body models (SMPL); Kinematic retargeting: scale, map joints, solve IK to match key points under joint limits; Motion retargeting: map human mocap onto a robot skeleton | 280 | ME-108, ME-109, RS-080 | Gu VII-C1; Loper et al. 2015; Gleicher 1998; Gu VII-C3; Gu hum §VII-C |
| 318 | Adversarial imitation: GAIL | Adversarial imitation (GAIL): a discriminator gives the reward | 189, new DL: Generative adversarial networks | RS-067 | Zare §IV |
| 319 | Motion imitation and adversarial motion priors | motion imitation reward with reference-state starts; discriminator style reward (AMP) plus task reward; Imitation for locomotion (animal or human motion) | 145, 148, DL-003, 318 | H.1, H.2, R2.14, RS-051 | Peng et al. 2018 (DeepMimic); Peng et al. 2021 (AMP); Escontrela et al. 2022; Ha §2.3 |
| 320 | Whole-body tracking from human data | retargeting, sim-to-data filtering, RL tracker with privileged imitation; imitation for high-level skills; split-body objectives: upper body imitates, legs follow a velocity; general tracking policy composed by a diffusion model at test time; Filtering retargeted motions that the robot cannot follow; Imitation from human motion data | 319, 166, 69, new DL: Diffusion models, 317 | H.5, H.6, H.9, ME-110, RS-079 | He et al. 2024 (H2O, OmniH2O); Fu et al. 2024 (HumanPlus); Cheng et al. 2024 (Exbody); Liao et al. 2025 (BeyondMimic); He et al. 2024 (H2O); Gu hum §VII-C |
| 321 | Teleoperating humanoids: live retargeting with differential IK | Teleoperation of humanoids: live retargeting with differential IK; Imitation from robot teleoperation data | 280, 317, 320 | ME-111, RS-081 | Darvish et al. 2023; Gu hum §VII-B |
| 322 | Multi-skill humanoid controllers and behaviour foundation models | separate skills distilled into one agent, then self-play (soccer); masked full-body commands distilled into one policy; RL from scratch for humanoid skills; Behaviour foundation models: one controller for any motion or goal, prompted at run time | 320, 166 | H.4, H.7, RS-078, RS-087 | Haarnoja et al. 2024; He et al. 2025 (HOVER); Gu hum §VII-A; Yuan §III |

### RB-07 Manipulation with learning

Visuomotor policies, grasping at scale, residual RL, action spaces, contact-rich tasks, dexterity, mobile manipulation.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 323 | End-to-end visuomotor policies | camera pixels to torques by guided policy search | 132, 116, DL-040 | M.1 | Levine et al. 2016 |
| 324 | Grasping from large real datasets | supervised grasp-success prediction with continuous servoing; closed-loop off-policy Q-learning from logged real data (QT-Opt); cross-entropy method to maximise Q; Grasping at scale with RL | 323, 36 | M.2, M.3, M.4, RS-075 | Levine et al. 2018; Kalashnikov et al. 2018; Ibarz §3.2; Tang §4.3.1 |
| 325 | Residual RL | learned correction on top of a hand-designed controller; Residual RL on a base controller; goal relabelling for sparse rewards | 132, 117 | M.6, RS-076 | Johannink et al. 2019; Silver et al. 2018; Tang §4.3, §5 |
| 326 | Manipulation action spaces: joints, end-effector deltas and impedance targets | Manipulation action spaces: joint, end-effector delta pose, impedance; Impedance targets as an RL action space | 134, 280, 287 | RS-062, ME-068 | Ravichandar §3.1.2; Kroemer §6.1; Martín-Martín et al. 2019 |
| 327 | Contact-rich manipulation: insertion and assembly | Contact-rich manipulation: insertion and assembly with force and impedance control | 326, 286 | RS-022 | Tang §4.3.2 |
| 328 | Articulated, deformable and non-prehensile objects | Object types: articulated (doors, drawers), deformable (cloth), non-prehensile (pushing) | 327, 292 | RS-023 | Tang §4.3.2-4.3.4 |
| 329 | 6-DoF grasp poses from point clouds | 6-DoF grasp pose prediction from point clouds | 291, 324, 91 | RS-072 | Tang §4.3.1.1; Wolf §4.2 |
| 330 | Learned object pose and keypoints | D5 Learned object pose and keypoints for manipulation | 173, 233 | AU-021 | M42 ch.10 (pose estimation, keypoints, dense correspondence); COR "3D visual representations" |
| 331 | Dexterous in-hand manipulation | multi-finger hand in sim with heavy randomisation and an LSTM policy; RMA-style adaptation to object size, shape and weight; In-hand dexterity | 149, 169, 167 | M.7, M.8, RS-074 | OpenAI et al. 2018; OpenAI et al. 2019; Handa et al. 2023; Qi et al. 2022; Tang §4.3.3 |
| 332 | Vision-based dexterity | full-state RL teacher, point-cloud student; point-cloud input, imagined hand points, contact-based reward; bimanual sim-to-real recipe with automatic real-to-sim tuning | 331, 166, 145, 139 | M.9, M.10, M.12 | Chen et al. 2023; Qin et al. 2022 (DexPoint); Lin et al. 2025 |
| 333 | Predicting object motion: learned models for manipulation | Learned transition models for manipulation (predict object motion) | 50, 328 | RS-073 | Kroemer §5 |
| 334 | Mobile manipulation | Mobile manipulation: one Jacobian for base and arm together; Mobile manipulation; Mobile manipulation: arm on a moving base; whole-body control by RL | 277, 131, 304 | ME-112, CT-112, RS-015 | MR 13.5; Tang §4.4 |

### RB-08 Imitation learning for manipulation

Where demonstrations come from and the policies that learn from them: diffusion policy, action chunking, demos inside RL, human feedback.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 335 | Collecting demonstrations: teleoperation and kinesthetic teaching | Collecting demonstrations: kinesthetic teaching, teleoperation (VR, leader-follower arms), passive observation | 165, 321 | RS-060 | Ravichandar §2 |
| 336 | Movement primitives and Gaussian mixture regression | Movement primitives: a trajectory as a spring-damper system plus a learned shape (DMP, ProMP); Gaussian mixture regression as a policy | 43, 118, 165, MA-073 | RS-004, RS-070 | Kober §4.3; Ravichandar §3.1.3 |
| 337 | Demonstrations from human videos | hand and object poses from video turned into robot demos; Imitation from observation: learn from state-only or video demos; Embodiment gap: human hand vs robot gripper, retargeting | 165 | M.11, RS-068, RS-069 | Qin et al. 2022 (DexMV); Zare §V; Zare §VI-B; Kawaharazuka §II-B |
| 338 | Diffusion policy and multimodal demonstrations | Why plain BC fails on multimodal demos (averaging two good paths gives a bad one); Diffusion policy: denoise a short action sequence step by step; I1 Diffusion policy: a policy that generates a short action sequence by denoising; handles multi-modal demonstrations | 335, new DL: Diffusion models | RS-063, RS-064, AU-037 | Wolf §2.3, §4.1.1; Wolf §4.1.1; Ma §III-B; Chi et al. 2023, *Diffusion Policy* ([arXiv 2303.04137](https://arxiv.org/abs/2303.04137)); M832 ch.21; COR "Generative models" |
| 339 | Action chunking (ACT) | Action chunking (ACT): predict k actions at once, blend overlapping chunks; I2 Action chunking (ACT), temporal ensembling and low-cost teleoperation for collecting demonstrations | 338, DL-087, new DL: Conditional VAE | RS-065, AU-038 | Kawaharazuka §IV-A; Ma §III-B; Zhao et al. 2023, ACT / ALOHA ([arXiv 2304.13705](https://arxiv.org/abs/2304.13705)) |
| 340 | Learning task structure from demonstrations | Learning task structure: segment demos into skills, pre- and postconditions | 335, 184 | RS-071 | Ravichandar §3.3; Kroemer §7-8 |
| 341 | Human feedback and shared autonomy for robots | I5 Human feedback for robots and shared autonomy; Human-robot interaction: shared autonomy and physical HRI | 335, 197 | AU-041, RS-016 | S237B wk 8–9 "Learning from human feedback", "Shared autonomy"; Tang §4.5 |
| 342 | Manipulation benchmarks and datasets | Manipulation benchmarks and datasets: robosuite, RLBench, Meta-World, CALVIN, LIBERO, robomimic | 338, 44 | RS-077 | Wolf §5; Ma §V |

### RB-09 Offline RL and RL from demonstrations

Learning a policy from logged data and demos, then improving it on the robot

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 343 | Offline RL and distribution shift | offline setting, distribution shift, out-of-distribution actions | 324, 165 | E.12 | Levine et al. 2020 |
| 344 | Conservative Q-learning | push down Q on unseen actions | 343 | E.13 | Kumar et al. 2020 |
| 345 | Offline pretraining, then online fine-tuning | Offline pretraining, then online fine-tuning | 344, 140 | RS-020 | Tang §5 |
| 346 | RL as sequence modelling: Decision Transformer | tokens are (return-to-go, state, action) | 343, DL-087 | E.14 | Chen et al. 2021 |
| 347 | Bootstrapping RL with demonstrations | Bootstrapping RL with demonstrations: demos in the replay buffer, BC term in the loss | 335, 42 | RS-007 | Ibarz §4.4 |
| 348 | Real-world RL with human corrections | sample-efficient off-policy real-robot RL: reward classifier, resets, demos; human corrections during real-world RL | 140, 42 | E.22, E.23 | Luo et al. 2024 (SERL); Luo et al. 2024 (HIL-SERL) |

### RB-10 Robot foundation models

Learning from fixed data and pretrained models: offline RL, VLAs, action heads, cross-robot data, language planning, real-world fine-tuning.

| # | Note | Teaches | Builds on | Rows | Sources |
|---|---|---|---|---|---|
| 349 | Vision-language-action models and generalist robot policies | robot actions as text tokens; co-fine-tuning; fine-tuning an open VLA for a new robot; generalist VLA for real robots (mostly imitation); open foundation model for humanoids (mostly imitation); Robot transformers and VLAs; Humanoid foundation models | 165, DL-071, DL-053 | E.15, E.16, E.20, E.21, RS-106, RS-088 | Brohan et al. 2023 (RT-2); Kim et al. 2024 (OpenVLA); Gemini Robotics Team 2025; NVIDIA 2025 (GR00T N1); Firoozi §III-A, §III-E; Ma §III; Gu hum §VIII |
| 350 | Action heads: tokens, diffusion and flow | Action heads: discrete action tokens vs diffusion/flow heads | 349 | RS-107 | Kawaharazuka §IV-A |
| 351 | Cross-embodiment datasets and generalist policies | Cross-embodiment datasets (Open X-Embodiment, DROID, BridgeData) and training across robots; I4 Large cross-robot demonstration datasets and generalist BC policies | 349, 339 | RS-108, AU-040 | Kawaharazuka §VI; Ma §V-A; Open X-Embodiment ([arXiv 2310.08864](https://arxiv.org/abs/2310.08864)); Octo ([arXiv 2405.12213](https://arxiv.org/abs/2405.12213)) |
| 352 | Flow-matching action experts | action chunks from a flow-matching expert; co-training on varied data for open-world homes | 349, new DL: Flow matching | E.17, E.18 | Black et al. 2024 (pi0); Physical Intelligence 2025 (pi0.5) |
| 353 | Pretrained visual representations for control | Pretrained visual representations for robots (from human video, goal-conditioned values) | 238, 323 | RS-110 | Firoozi §III-B |
| 354 | Language models as task planners | LLM task planning: monolithic vs modular (affordance-scored plans, code as policies) | 349, 293, 238 | RS-111 | Firoozi §III-C; Ma §IV |
| 355 | Affordance models: where and how to act | Affordance-based models: where and how to act on an object | 354 | RS-113 | Firoozi §IV-D; Kawaharazuka §IV-C |
| 356 | Video and world models as policies | Video and world models as policies (predict the future frame, then act) | 50, 349, new DL: Diffusion models | RS-114 | Firoozi §IV-E; Kawaharazuka §IV-B |
| 357 | Hierarchical VLAs: slow planner, fast controller | Hierarchical VLA: slow planner + fast controller | 352, 354 | RS-116 | Ma §IV; Kawaharazuka §V-D |
| 358 | RL fine-tuning of a VLA | advantage-conditioned RL fine-tuning with human corrections; RL fine-tuning of generalist policies | 352, 348, 34 | E.19, RS-117 | Physical Intelligence 2025 (pi*0.6 / RECAP); Kawaharazuka §V-C, §IX-D |
| 359 | Uncertainty and asking for help | Uncertainty and asking for help (conformal prediction) | 349 | RS-119 | Firoozi §VI-D |

## 4. New maths and deep-learning Notes (63)

These must be written before the Note that first needs them. Pieces marked "short section" go inside that Note.

**A new DL chapter, "Generative models for control",** is needed: VAE, contrastive loss, diffusion, flow matching, GANs and CLIP-style image–text pretraining. No DL Note teaches them: DL-001 says generative networks are not covered, and DL-003 gives GANs and autoencoders only a short paragraph. The reparameterization trick lives in the VAE Note, where it first appeared (Kingma & Welling 2014, arXiv 1312.6114); SAC recaps it.

| Concept | What | Where | First needed by (Note) |
|---|---|---|---|
| Markov chains | Markov property / Markov assumption, transition matrix, stationary distribution | MA 02-probability (new Note after MA-019) | 7 |
| Geometric series | sum of r^k = 1/(1-r) for \|r\|<1 | MA 06-calculus (new Note) | 8 |
| Monte Carlo estimation | estimate an expectation by averaging random samples; a sample set stands for a distribution | MA 04-inference (new Note after MA-034) | 16 |
| Importance sampling | target, proposal, weights; ordinary vs weighted; variance | MA 04-inference (new Note after Monte Carlo estimation) | 18 |
| KL divergence | what it measures, how to compute it | MA 08-likelihood (new Note after MA-072) | 38 |
| Linear transforms of a Gaussian | mean A mu, covariance A Sigma A^T | MA 08-likelihood (new Note after MA-073) | 80 |
| Product of two Gaussians | completing the square | MA 08-likelihood (same new Note as linear transforms) | 80 |
| Mahalanobis distance | distance scaled by a covariance; gating | MA 05-linear-algebra (new Note) | 178 |
| Woodbury identity | inverse of matrix plus low-rank change | MA 05-linear-algebra (new Note) | 257 |
| Cholesky factor | matrix square root, needed for sigma points | MA 05-linear-algebra (new Note) | 256 |
| Schur complement | marginalising variables out of a block matrix | MA 05-linear-algebra (new Note) | 101 |
| Sparse linear solves and conjugate gradient | sparse systems, relaxation, conjugate gradient; also used by TRPO | MA 05-linear-algebra (new Note) | 38 |
| Nonlinear least squares (Gauss-Newton) | re-linearise and re-solve in a loop | MA 07-optimisation (new Note) | 101 |
| Drawing samples from distributions | sampling recipes, triangular distribution | MA 03-distributions (new Note) | 68 |
| Rigid-body transforms and homogeneous coordinates | rotate + translate, homogeneous matrix, SE(2)/SE(3), heading angles kept in -pi..pi; 2D rotation by any angle (cos, sin), headings kept in -pi..pi (MA-053 shows only the 90-degree case) | MA 05-linear-algebra (new Note after MA-054) | 64 |
| 3D rotations: Euler angles and quaternions | yaw, pitch, roll; quaternions | MA 05-linear-algebra (new Note) | 65 |
| ODEs and vector fields | an equation for change; following the arrows | MA 06-calculus (new Note) | 112 |
| State-space models | phase space, x_dot = Ax + Bu, nonlinear systems; discrete-time models x(k+1) = A x(k) + B u(k) by zero-order hold (CT-029) | MA 06-calculus (new Note) | 64 |
| Numerical integration of ODEs | Euler and Runge-Kutta steps | MA 06-calculus (new Note) | 84 |
| Stability of dynamical systems | equilibria, eigenvalues, Lyapunov functions | MA 06-calculus (new Note) | 117 |
| Newtonian and rigid-body mechanics | F = ma, torque, inertia matrix, angular velocity | short RO section inside "PD and PID control" (mechanics is physics; CONTEXT.md defines MA as linear algebra, calculus, optimisation, probability, statistics) | 117 |
| Variational autoencoder | reconstruction + beta KL; reparameterization | DL new chapter "Generative models" (RL scope 5.1 decision) | 42 |
| Contrastive learning objective | pull matching pairs together, push others apart | DL new chapter "Generative models" | 168 |
| Diffusion models | flagged unowned in RL scope 5 | DL new chapter "Generative models" (added: prerequisite of humanoid diffusion tracking and navigation foundation models) | 243 |
| Flow matching | flagged unowned in RL scope 5 | DL new chapter "Generative models" (added: prerequisite of flow-matching action experts) | 352 |
| Robbins-Monro step-size conditions |  | new maths: short section inside the RO Note that first uses it | 3 |
| Control variates (why a baseline cuts variance) |  | new maths: short section inside the RO Note that first uses it | 31 |
| Log-derivative trick |  | new maths: short section inside the RO Note that first uses it | 30 |
| Fourier basis features |  | new maths: short section inside the RO Note that first uses it | 26 |
| Natural gradient and Fisher information |  | new maths: short section inside the RO Note that first uses it | 38 |
| Priority queue and Big-O cost |  | new maths: short section inside the RO Note that first uses it | 104 |
| Canonical (information) form of a Gaussian |  | new maths: short section inside the RO Note that first uses it | 257 |
| Lyapunov functions |  | new maths: short section inside the RO Note that first uses it | 117 |
| Bradley-Terry preference model |  | new maths: short section inside the RO Note that first uses it | 57 |
| Cross-entropy method (derivative-free max over actions) |  | new maths: short section inside the RO Note that first uses it | 43 |
| Matrix exponential and logarithm | e^(At) solves x' = Ax; series definition; log as the inverse; gives Rodrigues' formula for rotations | MA 06-calculus (new Note after the planned ODEs Note) | 204 |
| Cross product and skew-symmetric matrix | a x b written as [a]x b | MA 05-linear-algebra (new Note after MA-050) | 84 |
| Axis-angle, exponential and log maps of rotations | any rotation as one turn about one axis; rotation vector to and from rotation matrix (SO(3) exp/log, beginner level) | MA 05-linear-algebra (new Note after the planned 3D rotations Note) | 84 |
| Assignment problem (Hungarian algorithm) | match N tracks to M detections at least total cost | MA 07-optimisation (new Note) | 178 |
| Bootstrap confidence intervals and the interquartile mean | error bars from resampling a few seeds; a mean robust to outlier runs | MA 04-inference (new Note after MA-035) | 44 |
| Null-space projector and weighted pseudo-inverse | N = I - J+J; pseudo-inverse weighted by a mass matrix | MA 05-linear-algebra (new Note after MA-060) | 278 |
| Convex hull | smallest convex set around a set of points | MA 07-optimisation (short section added to MA-067) | 290 |
| Mutual information | how much knowing one variable tells about another; KL between joint and product | MA 08-likelihood (new Note after KL divergence) | 315 |
| Generative adversarial networks | generator vs discriminator; the discriminator as a learned reward | DL new chapter 'Generative models' | 138 |
| Conditional VAE | a VAE whose encoder and decoder see a condition (the observation) | DL new chapter 'Generative models' (section of the VAE Note) | 339 |
| Gaussian processes | regression with a mean and an uncertainty at every input | ML new Note (no ML Note has GPs) | 200 |
| Geodetic coordinates and map projections | latitude/longitude to local east-north-up metres; UTM | short section inside the RO Note that first uses it | 85 |
| Recursive least squares | update a least-squares fit one measurement at a time; a bridge to the Kalman filter | short section inside the RO Note that first uses it | 80 |
| Projective homogeneous coordinates | any multiple is the same point; divide by the last entry (PE-002) | short section inside the RO Note that first uses it | 88 |
| Least-squares solution of Ax = 0 by the SVD | last right singular vector (PE-009) | short section inside the RO Note that first uses it | 89 |
| k-d trees and point-set alignment by SVD (Kabsch) | fast nearest neighbours; best rotation between matched points (PE-071, PE-043) | short section inside the RO Note that first uses it | 92 |
| Polynomials from boundary conditions | solve a small linear system for cubic/quintic coefficients (CT-085, ME-050) | short section inside the RO Note that first uses it | 201 |
| Cubic splines and minimum jerk (beginner calculus of variations) | piecewise cubics; the quintic that minimises jerk (CT-088, CT-089) | short section inside the RO Note that first uses it | 202 |
| Controllability rank test and pole placement | rank of [B, AB, ...]; eigenvalues of A - BK (CT-031, CT-033) | short section inside the RO Note that first uses it | 204 |
| Discrete Riccati recursion | backward update of the cost matrix; DP on quadratic costs | short section inside the RO Note that first uses it | 205 |
| Newton-type solvers with constraints (SQP, interior point), overview | what the solver does each iteration (CT-073) | short section inside the RO Note that first uses it | 208 |
| Second-order linear systems | mass-spring-damper; natural frequency and damping ratio (ME-056) | short section inside the RO Note that first uses it | 118 |
| Conditional value at risk | the average of the worst outcomes; builds on MA-008 percentiles | short section inside the RO Note that first uses it | 198 |
| Structure tensor | 2x2 matrix of image gradients read through its eigenvalues | short section inside the RO Note that first uses it | 227 |
| Levenberg-Marquardt and robust losses (IRLS) | damped Gauss-Newton; losses that grow slowly for big errors (PE-052, PE-053) | short section inside the RO Note that first uses it | 235 |
| Newton-Raphson root finding | solve f(x) = 0 by repeated linearisation; non-square Jacobian via the pseudo-inverse (ME-030) | short section inside the RO Note that first uses it | 279 |
| Lagrangian mechanics (worked-example depth) | L = T - V gives M(q)q'' + c + g = tau (ME-037); physics, so a short RO section | short section inside the RO Note that first uses it | 281 |
| Friction pyramid | the friction cone as linear inequalities so problems stay QPs (ME-080) | short section inside the RO Note that first uses it | 288 |

## 5. Recap only: already taught in MA/ML/DL (29)

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

## 6. Overlaps merged (155)

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
| tracking, global and kidnapped-robot localization, Markov localization | PR doc 7.1 'Kinds of localization: tracking, global, kidnapped robot; static/dynamic world; passive/active; one/many robots', PR doc 7.2 'Markov localization', PA doc 12.2 'Robot localization (discrete, geometric, Monte Carlo)' | 94 |
| online SLAM vs full SLAM | PR doc 10.1 'SLAM problem: online SLAM vs full SLAM', PA doc 12.3 'Mapping and SLAM (build a map while finding yourself in it)' | 100 |
| reward as a number to maximise over time, possibly delayed, exploration vs exploitation | RL doc SB1.1 'RL as learning from interaction: agent, environment, reward', RL doc SB1.2 'Exploration vs exploitation trade-off', RL doc SB1.3 'Four elements: policy, reward signal, value function, model', RL doc SB1.5 'Evolutionary (policy search) vs value-function methods', PR doc 14.2 'Reinforcement learning, reward, policy' | 1 |
| agent-environment interface per time step, MDP dynamics p(s', r \| s, a) | RL doc SB3.1 'Agent–environment interface: state, action, reward, time step', RL doc SB3.4 'MDP dynamics p(s', r given s, a)', RL doc SB3.5 'Reward hypothesis: goals as summed reward', PR doc 14.3 'Markov decision process (states, actions, transition probabilities, payoff)', PA doc 10.1 'Markov decision process (MDP)', PA doc 10.2 'Forward projections and backprojections' | 7 |
| return, episodes, episodic vs continuing tasks, discount factor and horizon | RL doc SB3.6 'Return, episodes, episodic vs continuing tasks', PR doc 14.4 'Discount factor, horizon, cumulative payoff', PA doc 10.5 'Infinite horizon: discounted cost and average cost' | 8 |
| Bellman expectation equation, backup diagrams | RL doc SB3.10 'Bellman expectation equation', RL doc SB3.11 'Backup diagrams', RL doc SB3.14 'Bellman equation as a linear system v = (I − γP)⁻¹r', RL doc B.1 'Principle of optimality; the functional (Bellman) equation', PR doc 14.5 'Value function and Bellman equation' | 10 |
| policy improvement theorem, policy iteration | RL doc SB4.2 'Policy improvement theorem', RL doc SB4.3 'Policy iteration', PA doc 10.4 'Policy iteration' | 13 |
| value iteration, cost-to-go as the planning name for value | RL doc SB4.4 'Value iteration', PA doc 2.8 'Cost-to-go and value iteration (dynamic programming)', PA doc 10.3 'Value iteration and the Bellman equation (with nature)', PR doc 14.6 'Value iteration' | 14 |
| value iteration on a robot grid map, DP with interpolation on continuous spaces | PR doc 14.7 'Value iteration for robot path planning on a grid', PA doc 8.7 'Dynamic programming with interpolation on continuous spaces', PA doc 14.7 'Feedback planning with dynamic programming and interpolation' | 106 |
| first-visit and every-visit MC prediction, MC estimation of action values | RL doc SB5.2 'First-visit and every-visit MC prediction', RL doc SB5.3 'MC estimation of action values', PA doc 10.6 'Reinforcement learning: evaluating a plan by simulation (Monte Carlo, temporal difference)' | 16 |
| Q-learning (off-policy TD control), convergence of Q-learning | RL doc SB6.5 'Q-learning (off-policy TD control)', PA doc 10.7 'Q-learning', RL doc B.3 'Convergence of Q-learning (every pair visited forever, step-size conditions)' | 21 |
| lambda-return, eligibility traces; forward vs backward view | RL doc SB12.1 'λ-return', RL doc SB12.2 'Eligibility trace vector; TD(λ); forward vs backward view', RL doc SB12.3 'Truncated λ-return, online λ-return, true online TD(λ), dutch traces', RL doc SB12.4 'Sarsa(λ)', RL doc SB12.5 'Variable λ and γ', RL doc SB12.6 'Off-policy traces: Watkins's Q(λ), Tree-Backup(λ), GTD(λ), emphatic TD(λ)', RL doc B.2 'TD(λ) for multi-step prediction' | 24 |
| policy gradient theorem, log-derivative trick | RL doc SB13.3 'Policy gradient theorem', RL doc SB13.4 'Log-derivative trick ∇π / π = ∇ ln π', RL doc B.5 'Policy gradient theorem with function approximation; compatible features' | 30 |
| Monte Carlo policy gradient (REINFORCE family) | RL doc SB13.5 'REINFORCE (Monte Carlo policy gradient)', RL doc B.4 'REINFORCE family of algorithms' | 30 |
| one-step actor-critic, policy gradient for continuing problems | RL doc SB13.7 'One-step actor–critic', RL doc SB13.8 'Policy gradient for continuing problems', RL doc B.6 'Two-timescale actor–critic (critic learns faster than actor)' | 32 |
| CNN trained with Q-learning targets on raw pixels, error clipping in the TD loss | RL doc C.1 'Deep Q-network on raw pixels', RL doc C.4 'Error clipping in the loss', RL doc SB16.5 'Human-level video game play (DQN)' | 35 |
| self-play TD learning (TD-Gammon, Samuel checkers), policy network + value network + tree search | RL doc SB16.1 'TD-Gammon', RL doc SB16.2 'Samuel's checkers player', RL doc SB16.6 'AlphaGo and AlphaGo Zero', RL doc C.5 'Policy network + value network + tree search', RL doc C.6 'Self-play from scratch; MCTS as policy improvement', RL doc C.7 'One algorithm for several board games' | 55 |
| partially observable MDP, planning in belief / information space | PR doc 15.1 'Partially observable MDP and belief space', PA doc 11.6 'POMDP (MDP where the state is hidden)', PA doc 12.1 'Planning in belief / information space', RL doc SB17.3 'Observations and state; POMDP; state-update function', RL doc R3.1 'Robot control as a POMDP' | 153 |
| system identification and actuator networks, delta (residual) action model learned from real data | RL doc R1.5 'System identification and actuator models', RL doc R1.6 'Delta (residual) action model learned from real data *(added 2023–26)*', RL doc H.8 'Aligning sim with real via a delta action model', RL doc L.2 'Learning a gait from scratch with an improved simulator' | 139 |
| reward shaping and reward hacking, designing reward signals: sparse, shaped, imitation, inverse RL | RL doc R2.8 'Reward shaping and its risks', RL doc SB17.4 'Designing reward signals: sparse reward, shaping, imitation, inverse RL' | 146 |
| gait shaping: feet air time, clearance, energy, gaits emerging from energy minimisation | RL doc R2.7 'Gait shaping: feet air time, foot clearance, energy', RL doc L.8 'Gaits from energy minimisation', RL doc R2.13 'A family of behaviours in one policy' | 147 |
| Hindsight Experience Replay, goal-conditioned manipulation with sparse rewards | RL doc R2.11 'Sparse rewards and Hindsight Experience Replay', RL doc M.5 'Goal-conditioned manipulation with sparse rewards' | 150 |
| evolutionary search over reward weights and network shape (AutoRL), reward code written by a language model | RL doc N.16 'Searching rewards and networks automatically', RL doc R2.15 'Reward code written by a language model *(added 2023–26)*' | 152 |
| adaptation from history without weight updates, humanoid walking sim-to-real with a causal transformer, zero-shot | RL doc R3.13 'In-context adaptation with a sequence model', RL doc H.3 'Humanoid locomotion sim-to-real' | 169 |
| general value functions, auxiliary losses (depth, loop closure) for representation | RL doc R3.14 'Auxiliary tasks for representation', RL doc SB17.1 'General value functions and auxiliary tasks' | 170 |
| adaptive velocity curriculum + online system identification for running, soft-then-hard obstacle curriculum; distil skills into one depth policy with DAgger | RL doc L.4 'High-speed running', RL doc L.5 'Agility and parkour', RL doc H.10 'Perceptive humanoid locomotion *(added 2023–26)*' | 309 |
| motion imitation reward with reference-state starts, discriminator style reward (AMP) plus task reward | RL doc H.1 'Motion imitation reward', RL doc H.2 'Adversarial motion priors', RL doc R2.14 'Style rewards learned from data' | 319 |
| learned navigation over a locomotion policy; end-to-end locomotion + local navigation, skill hierarchies for agile navigation (parkour) | RL doc N.22 'Navigation with legged robots', RL doc L.6 'Skill hierarchies for agile navigation', RL doc N.23 'Wheeled-legged urban navigation *(added 2023–26)*' | 313 |
| Markov chains | RL doc SB3.2 'Markov property', RL doc SB3.3 'Markov chain: transition matrix, stationary distribution', PR doc 2.16 'Markov assumption' | new maths: Markov chains |
| Monte Carlo estimation | RL doc SB5.1 'Monte Carlo estimation (average sampled returns)', PR doc 4.6 'Monte Carlo approximation (a set of samples stands for a distribution)' | new maths: Monte Carlo estimation |
| Importance sampling | RL doc SB5.7 'Importance sampling ratio; ordinary vs weighted IS', RL doc SB5.8 'Variance of IS estimators (can be infinite)', PR doc 4.7 'Importance sampling (target, proposal, weights)', PA doc 11.9 'Monte Carlo methods and importance sampling' | new maths: Importance sampling |
| KL divergence | RL doc C.11 'KL divergence between policies', PR doc 8.5 'KL divergence' | new maths: KL divergence |
| Rigid-body transforms and homogeneous coordinates | PA doc 3.7 'Rigid-body transform (rotate + translate, keeps distances)', PA doc 3.8 'Homogeneous transformation matrix', PA doc 4.11 'Special Euclidean groups SE(2), SE(3)', PR doc 5.2 '2D rotation and heading angles' | new maths: Rigid-body transforms and homogeneous coordinates |
| Policies, plans and value functions | RL doc SB3.8 'Policy π(a given s) as a conditional distribution', RL doc SB3.9 'State-value v_π and action-value q_π', PA doc 1.1 'State, action, state transition (the basic parts of a planning problem)', PA doc 1.2 'Feasible plan vs optimal plan', PA doc 1.3 'Open-loop plan vs feedback plan', PA doc 8.1 'Feedback plan as a policy' | 9 |
| Least-squares TD and nonparametric value functions | RL doc SB9.12 'Least-squares TD (LSTD)', RL doc SB9.13 'Memory-based (nearest-neighbour) approximation', RL doc SB9.14 'Kernel-based approximation' | 51 |
| Control with approximation and the average-reward setting | RL doc SB10.1 'Episodic semi-gradient Sarsa (mountain car)', RL doc SB10.2 'Semi-gradient n-step Sarsa', RL doc SB10.3 'Average-reward setting, differential return and values', RL doc SB10.4 'Why discounting breaks with approximation', RL doc SB10.5 'Differential semi-gradient n-step Sarsa' | 27 |
| The policy gradient theorem and REINFORCE | RL doc SB13.3 'Policy gradient theorem', RL doc SB13.4 'Log-derivative trick ∇π / π = ∇ ln π', RL doc B.5 'Policy gradient theorem with function approximation; compatible features', RL doc SB13.5 'REINFORCE (Monte Carlo policy gradient)', RL doc B.4 'REINFORCE family of algorithms' | 30 |
| Markov localization on a known map | PR doc 7.1 'Kinds of localization: tracking, global, kidnapped robot; static/dynamic world; passive/active; one/many robots', PR doc 7.2 'Markov localization', PA doc 12.2 'Robot localization (discrete, geometric, Monte Carlo)', PR doc 8.1 'Grid localization' | 94 |
| Monte Carlo localization and adaptive particle counts | PR doc 8.2 'Monte Carlo localization (MCL)', PR doc 8.3 'Random-particle / augmented MCL (recovery from failure)', PR doc 8.8 'Localization in changing environments (people, outlier readings)', PR doc 8.4 'Choosing a better proposal distribution', PR doc 8.6 'Chi-square distribution (used to bound KL)', PR doc 8.7 'KLD-sampling (adaptive number of particles)' | 95 |
| Grid path planning: wavefronts, navigation functions and value iteration | PR doc 14.7 'Value iteration for robot path planning on a grid', PA doc 8.7 'Dynamic programming with interpolation on continuous spaces', PA doc 14.7 'Feedback planning with dynamic programming and interpolation', PA doc 8.2 'Navigation functions and grid wavefront propagation' | 106 |
| Moving through unknown maps: D* replanning and bug algorithms | PA doc 12.4 'D* (fast replanning when the map changes)', PA doc 12.5 'Bug algorithms and navigating unknown spaces' | 107 |
| Collision checking and nearest neighbours in C-space | PA doc 5.7 'Collision detection (distance between sets, broad and narrow phase)', PA doc 5.8 'Bounding-volume hierarchies', PA doc 5.1 'Metric space (rules a distance must follow)', PA doc 5.9 'Nearest-neighbour search with kd-trees', PA doc 5.3 'Uniform random samples of rotations and directions' | 108 |
| Curricula: terrain, commands and automatic domain randomization | RL doc R2.10 'Curricula: terrain and command', RL doc R1.4 'Automatic domain randomization (ADR)' | 149 |
| Behaviour cloning, compounding error and DAgger | RL doc R3.5 'Behaviour cloning and compounding error', RL doc R3.6 'DAgger' | 165 |
| Learned state estimators: explicit and latent | RL doc R3.9 'Learned state estimation trained with the policy', RL doc R3.11 'Latent context estimators' | 168 |
| Lagrangian and PID-Lagrangian PPO | RL doc R4.3 'Lagrangian methods (PPO-Lagrangian)', RL doc R4.4 'PID Lagrangian' | 193 |
| Not only rewards but also constraints: constraint types for real robots | RL doc R4.8 'Constraint types for robots: probabilistic and average', RL doc R4.9 'Choosing a constrained algorithm for hardware', RL doc R4.13 'Safe-RL benchmarks and libraries' | 195 |
| Observations for navigation: laser, vision and maps | RL doc N.5 'Observation design for a laser-scan navigation policy', RL doc N.6 'Observation design for visual and map-based navigation' | 157 |
| Exploration by information gain and active localization | PR doc 17.1 'Information gain and entropy as a goal', PR doc 17.2 'Greedy and multi-step exploration', PR doc 17.3 'Monte Carlo exploration', PR doc 17.4 'Active localization' | 180 |
| Crowds and robot teams: attention pooling and shared policies | RL doc N.13 'Any number of neighbours: LSTM and attention pooling', RL doc N.14 'Shared-policy multi-robot training with PPO' | 213 |
| Vision-language-action models and generalist robot policies | RL doc E.15 'Vision-language-action (VLA) model; actions as text tokens; co-fine-tuning', RL doc E.16 'Fine-tuning an open VLA for a new robot', RL doc E.20 'Generalist VLA for real robots (mostly imitation; context)', RL doc E.21 'Open foundation model for humanoids (mostly imitation; context)' | 349 |
| Data association and multi-hypothesis tracking | PR doc 7.4 'Data association (correspondence) problem', PR doc 7.5 'Maximum-likelihood data association', PR doc 3.9 'Mixture-of-Gaussians belief (multi-hypothesis, 3.3.5)', PR doc 7.7 'Multi-hypothesis tracking' | 259 |
| Games: minimax, alpha-beta and equilibria | PA doc 9.6 'Zero-sum games, minimax and saddle points', PA doc 9.7 'Mixed (randomized) strategies, solved with linear programming', PA doc 9.8 'Nonzero-sum games and Nash equilibrium', PA doc 10.8 'Game trees and alpha-beta pruning', PA doc 10.9 'Sequential games on state spaces' | 54 |
| Parameterised policies | SB13.1, SB13.2, RS-002 | 29 |
| Pose and wheeled-robot motion | PR 5.1, PA 13.1, PA 13.3, CT-004, CT-005, ME-014 | 64 |
| Coordinate frames and the transform tree | AU-005, ME-004 | 65 |
| Probabilistic motion models: velocity and odometry | PR 5.3, PR 5.4, PR 5.5, PR 5.7, PR 5.8, CT-006 | 68 |
| Kinematic chains: where the hand and foot are | PA 3.10, PA 3.11, PA 3.12, ME-018, ME-019, ME-020 | 69 |
| Robot description files: URDF, SDF and MJCF | AU-042, ME-016, ME-013 | 70 |
| Configuration space and degrees of freedom | PA 4.8, PA 4.3, PA 4.4, PA 4.14, ME-012 | 72 |
| PD and PID control | R0.7, CT-014, CT-105 | 117 |
| Kalman filter | PR 3.1, PR 3.6, PA 11.8, CT-110, PE-091, CT-032, PE-104 | 80 |
| Extended Kalman filter | PR 3.7, PR 3.8, PE-092 | 81 |
| Integrating rotation rates and strapdown inertial navigation | PE-086, PE-088, ME-005 | 84 |
| Satellite positioning: GNSS and RTK | PE-090, AU-015 | 85 |
| 3D maps: voxels, octrees, elevation maps and signed distance | AU-012, PE-077, PE-078, PE-079, PE-080 | 97 |
| Localizing in a prior 3D map: the normal distributions transform | AU-016, PE-074 | 99 |
| Planning with motion limits | PA 14.1, PA 14.2, PA 14.4, PA 14.5, PA 14.6, PA 15.9, CT-095, CT-096 | 112 |
| Trajectory optimisation | PA 14.9, CT-097, CT-072, ME-054 | 116 |
| Reading a controller's response: step response and second-order systems | CT-034, ME-056 | 118 |
| Feedforward, integral action, cascaded loops and windup | CT-037, ME-055, CT-035, CT-036, CT-038 | 119 |
| Classical local planning: DWA and TEB | N.1, CT-055 | 129 |
| The Nav2 navigation stack and ROS tooling | N.26, RL §5.1 decision 2026-10-03 'The Nav2 navigation stack' (second background Note), RS-024 | 131 |
| Why robot RL is hard | R0.1, R0.2, R0.3, RS-001, RS-012 | 132 |
| The robot as an MDP | R0.4, RS-013 | 133 |
| Action spaces: torques, PD targets, velocity commands | R0.5, R0.6, CT-111 | 134 |
| Parallel simulation and the reference training stack | R0.8, R0.9, R0.10, RS-097 | 135 |
| The reality gap and domain randomization | R1.1, R1.2, R1.3, R1.9, RS-089, RS-050 | 137 |
| System identification and actuator models | R1.5, R1.6, H.8, L.2, RS-090, AU-035, RS-094 | 139 |
| Real-robot training and sim-real agreement | R1.7, R1.8, RS-093, RS-008 | 140 |
| Curricula: terrain, commands and automatic domain randomization | R2.10, R1.4, RS-091 | 149 |
| Searching for rewards automatically | N.16, R2.15, RS-010, RS-118 | 152 |
| Learned vs classical local planners | N.2, RS-026, RS-030 | 154 |
| Mapless end-to-end navigation | N.4, RS-025 | 156 |
| Evaluating navigation: success, SPL, collisions | N.19, AU-046, AU-036, RS-014 | 161 |
| Privileged information | R3.3, RS-049 | 163 |
| Behaviour cloning, compounding error and DAgger | R3.5, R3.6, RS-061 | 165 |
| Teacher-student distillation | R3.7, RS-095 | 166 |
| Online adaptation modules (RMA) | R3.8, RS-096 | 167 |
| Learned state estimators: explicit and latent | R3.9, R3.11, PE-108 | 168 |
| In-context adaptation with sequence models | R3.13, H.3, RS-115 | 169 |
| Object detection: boxes, IoU, non-max suppression and mAP | PE-109, PE-110, PE-111, PE-118, AU-017 | 173 |
| Semantic segmentation | PE-114, PE-115, AU-018 | 175 |
| Semantic maps and traversability costs | PE-116, PE-117, RS-031 | 177 |
| Multi-object tracking | AU-019, PE-106 | 178 |
| Predicting where people and vehicles go, and collision checks in time | AU-022, RS-033, AU-023 | 179 |
| Curiosity and intrinsic rewards for exploration | AU-051, RS-037 | 182 |
| Options: temporal abstraction | SB17.2, RS-018 | 184 |
| Inverse RL: recovering a reward from demonstrations | RS-066, AU-039 | 189 |
| Constrained MDPs and cost critics | R4.1, R4.2, RS-098 | 192 |
| Not only rewards but also constraints: constraint types for real robots | R4.8, R4.9, R4.13, RS-105 | 195 |
| Shields, safety filters and recovery policies | R4.11, R4.12, RS-100, RS-104 | 197 |
| Time scaling and polynomial trajectories | CT-084, ME-048, CT-085, ME-050, CT-086, ME-051 | 201 |
| Via points, splines and minimum-jerk trajectories | CT-087, ME-052, CT-088, CT-089, CT-093, CT-094 | 202 |
| Speed profiles along a fixed path | CT-092, ME-053, AU-029 | 203 |
| LQR: the linear-quadratic regulator | PA 15.6, PA 15.7, CT-057, CT-058, CT-059, CT-109 | 205 |
| Multi-agent collision avoidance and social norms | N.11, N.12, RS-032 | 212 |
| Multi-agent RL: centralised training, decentralised execution | AU-033, RS-017 | 214 |
| Social navigation: norms, coupled prediction and planning, evaluation | RS-034, RS-035, RS-036, AU-024 | 215 |
| Navigation at scale | N.18, RS-044 | 216 |
| Safety in navigation | N.25, RS-057 | 219 |
| Agile aerial navigation | N.24, CT-106, RS-021, RS-045 | 226 |
| Extrinsic and time calibration between sensors | PE-015, AU-034 | 93 |
| Vision-and-language navigation: task, datasets and metrics | AU-052, RS-041 | 241 |
| Navigation foundation models | N.27, RS-120 | 243 |
| Unscented Kalman filter | PR 3.11, PR 3.12, PE-093 | 256 |
| Loop closure and map merging | PR 13.6, PR 12.7, PE-107 | 102 |
| Contact kinematics, contact types and the friction cone | ME-078, ME-079, ME-080, CT-024 | 288 |
| Grasp quality and grasp selection | ME-084, ME-085, AU-048 | 291 |
| Manipulation planning | PA 7.4, PA 12.7, ME-086, ME-087 | 292 |
| Tactile sensing | AU-050, RS-085 | 294 |
| Zero-moment point and the linear inverted pendulum | ME-090, ME-091, CT-080, CT-081 | 296 |
| Central pattern generators | ME-098, RS-048 | 300 |
| Convex MPC for legged robots | ME-101, CT-077, CT-082, RS-082, ME-102 | 302 |
| QP-based whole-body control | ME-073, ME-074, ME-075, ME-077, CT-083, RS-083, ME-107 | 304 |
| Multi-contact planning | ME-103, RS-086 | 306 |
| The PPO locomotion recipe, end to end | L.1, RS-046, RS-047 | 307 |
| Agility: high speed and parkour | L.4, L.5, H.10, RS-056 | 309 |
| Model-based and learned legged control: comparing and combining | ME-105, ME-106, RS-052, RS-053, RS-084 | 311 |
| Navigation on legged and wheeled-legged robots | N.22, L.6, N.23, RS-058 | 313 |
| Loco-manipulation: walking and using arms together | RS-059, ME-076 | 314 |
| Human motion data and kinematic retargeting | ME-108, ME-109, RS-080 | 317 |
| Motion imitation and adversarial motion priors | H.1, H.2, R2.14, RS-051 | 319 |
| Whole-body tracking from human data | H.5, H.6, H.9, ME-110, RS-079 | 320 |
| Teleoperating humanoids: live retargeting with differential IK | ME-111, RS-081 | 321 |
| Multi-skill humanoid controllers and behaviour foundation models | H.4, H.7, RS-078, RS-087 | 322 |
| Grasping from large real datasets | M.2, M.3, M.4, RS-075 | 324 |
| Residual RL | M.6, RS-076 | 325 |
| Manipulation action spaces: joints, end-effector deltas and impedance targets | RS-062, ME-068 | 326 |
| Dexterous in-hand manipulation | M.7, M.8, RS-074 | 331 |
| Mobile manipulation | ME-112, CT-112, RS-015 | 334 |
| Demonstrations from human videos | M.11, RS-068, RS-069 | 337 |
| Diffusion policy and multimodal demonstrations | RS-063, RS-064, AU-037 | 338 |
| Action chunking (ACT) | RS-065, AU-038 | 339 |
| Human feedback and shared autonomy for robots | AU-041, RS-016 | 341 |
| Vision-language-action models and generalist robot policies | E.15, E.16, E.20, E.21, RS-106, RS-088 | 349 |
| Cross-embodiment datasets and generalist policies | RS-108, AU-040 | 351 |
| RL fine-tuning of a VLA | E.19, RS-117 | 358 |

## 7. Dropped (63)

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

## 8. Open decisions for the owner

1. **Three Subjects.** RL (reinforcement learning), RO (robot navigation) and RB (robot bodies), or another split? RO now means robot navigation, not all of robotics.
2. **Detection and segmentation** (Notes 173–175) are in RO. Should they be DL Notes instead?
3. **Lagrangian mechanics** (Note 281) is back, as a worked 2-link arm. It had been dropped, but computed torque, operational-space control and whole-body control build on its result.
4. **Humanoids** get 6 Notes of their own (RB-06), plus whole-body control and biped walking elsewhere. Is that equal weight with legged robots and manipulation?
5. **New MA Notes (63 entries, some only short sections)** will grow the MA chapters. Each goes just before its first user in the Course order.

