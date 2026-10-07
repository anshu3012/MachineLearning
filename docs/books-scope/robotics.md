# Scope: Robotics and reinforcement learning (RO), one consolidated plan

**Summary.** This is the one plan for the RO Subject: **25 chapters, 188 Notes**. It is a scoping list only, not study Notes. It merges three book scopes into one list in which each concept appears once:

- [reinforcement-learning.md](reinforcement-learning.md): Sutton & Barto, plus deep RL, RL for robots and the frontier (308 rows).
- [probabilistic-robotics.md](probabilistic-robotics.md): Thrun, Burgard, Fox (132 rows).
- [planning-algorithms.md](planning-algorithms.md): LaValle (149 rows).

The three docs stay as the evidence: their rows hold the book sections, papers and checks. Rows are cited here as `RL SB3.2`, `PR 4.2` and `PA 8.7`. All 589 rows are placed: each is in exactly one Note, recapped from an MA/ML/DL Note, listed as new maths, or dropped with a reason. The one exception is row N.1, which is in two Notes on purpose. RL §5.1 asks for separate "DWA and TEB" and "Nav2" Notes.

**How it was chosen.** Two proposals were written: A put RL first (185 Notes), B put robotics first (209 Notes). Two critics checked both by script (rows placed, no forward links, labels exist) and argued over two rounds. This plan is critic 2's round-1 scope, with critic 2's round-2 maths fixes added.

## 1. Order, and why

1. **RL first (RO-01 to RO-07).** The RL core needs nothing from classical robotics except graph search. Graph search sits in RO-03, next to dynamic programming, as in LaValle ch.2 (row PA 2.8 puts value iteration inside discrete planning).
2. **A lean classical core (RO-08 to RO-11, 29 Notes):** robot models, Bayes filters, localization, occupancy grids, grid and sampling planners. This is only what the robot-RL chapters build on.
3. **Robot RL (RO-12 to RO-14):** sim-to-real, task design, and partial observability with privileged learning.
4. **Navigation, the primary interest (RO-15, RO-16, RO-18; 23 Notes plus Note 147 on legged navigation).** It starts at Note 106, against 133 in A and 158 in B. Safety (RO-17) sits between navigation II and III, because "Safety in navigation" (Note 133) builds on it.
5. **Then planning and games, legged robots and humanoids, manipulation, offline RL and foundation models.**
6. **Optional depth, last:** RO-22 (state estimation and SLAM in depth), RO-23 (planning and control in depth) and RO-25 (RL for language models). No Note outside them builds on them, so a learner can skip them.

**RL for language models stays in RO.** Its Notes build on PPO, baselines and KL, which live in RO. DL comes before RO, so a DL home would need links forward into RO. Its RLHF Note recaps DL-067 §7.

## 2. Chapters and Notes

"Builds on" gives a number for an earlier RO Note, a label for an MA/ML/DL Note, or "new MA"/"new DL" for a Note still to be written (§3).

### RO-01 Learning by trial: bandits

Act, get a number back, learn which action pays: the explore-exploit problem in one state.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 1 | The reinforcement learning problem | ML-003 | RL SB1.1, RL SB1.2, RL SB1.3, RL SB1.5, PR 14.2 | Sutton&Barto 2018 ch.1; Thrun et al. 2005 ch.14 |
| 2 | Multi-armed bandits and epsilon-greedy | 1, MA-005 | RL SB2.1, RL SB2.2, RL SB2.3, RL SB2.4 | Sutton&Barto 2018 ch.2; DeepMind x UCL 2021 L2 |
| 3 | Incremental updates and step sizes | 2, DL-033 | RL SB2.5, RL SB2.7 | Sutton&Barto 2018 ch.2 |
| 4 | Exploring smartly: optimistic starts and UCB | 3, MA-035 | RL SB2.8, RL SB2.9 | Sutton&Barto 2018 ch.2 |
| 5 | Gradient bandits | 2, ML-078 | RL SB2.10 | Sutton&Barto 2018 ch.2 |
| 6 | Contextual bandits | 2 | RL SB2.11, RL SB16.7 | Sutton&Barto 2018 ch.2; Sutton&Barto 2018 ch.16 |

### RO-02 Markov decision processes

Many states: the formal model, returns, policies, value functions and Bellman equations.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 7 | Decisions against nature | MA-012, MA-018, MA-066 | PA 9.4, PA 9.5, PA 9.9, PA 9.1, PA 7.8 | LaValle 2006 ch.9; LaValle 2006 ch.7 |
| 8 | Markov decision processes | 1, new MA: Markov chains, MA-014 | RL SB3.1, RL SB3.4, RL SB3.5, PR 14.3, PA 10.1, PA 10.2 | Sutton&Barto 2018 ch.3; Thrun et al. 2005 ch.14; LaValle 2006 ch.10; DeepMind x UCL 2015 L2 |
| 9 | Return and discounting | 8, new MA: Geometric series | RL SB3.6, PR 14.4, PA 10.5, RL SB14.6 | Sutton&Barto 2018 ch.3; Thrun et al. 2005 ch.14; LaValle 2006 ch.10 |
| 10 | Policies, plans and value functions | 9, MA-012, ML-003, MA-066 | RL SB3.8, RL SB3.9, PA 1.1, PA 1.2, PA 1.3, PA 8.1 | Sutton&Barto 2018 ch.3; LaValle 2006 ch.1; LaValle 2006 ch.8 |
| 11 | Bellman equations | 10, MA-019, ML-053 | RL SB3.10, RL SB3.11, RL SB3.14, RL B.1, PR 14.5 | Sutton&Barto 2018 ch.3; Thrun et al. 2005 ch.14; Bellman 1957 |
| 12 | Optimal values and optimal policies | 11 | RL SB3.12, RL SB3.13, RL SB3.15 | Sutton&Barto 2018 ch.3 |

### RO-03 Planning with a known model: graph search and dynamic programming

When the model is known: shortest paths on graphs (BFS, Dijkstra, A*) and DP on MDPs.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 13 | Graphs and uninformed search | 10 | PA 2.1, PA 2.2, PA 2.9, PA 6.8 | LaValle 2006 ch.2; LaValle 2006 ch.6 |
| 14 | Dijkstra's algorithm and priority queues | 13 | PA 2.3, PA 2.4 | LaValle 2006 ch.2 |
| 15 | A* and heuristics | 14 | PA 2.5, PA 2.6, PA 2.7 | LaValle 2006 ch.2 |
| 16 | Policy evaluation | 11 | RL SB4.1, RL SB4.7 | Sutton&Barto 2018 ch.4; DeepMind x UCL 2015 L3 |
| 17 | Policy improvement and policy iteration | 16, 12 | RL SB4.2, RL SB4.3, PA 10.4 | Sutton&Barto 2018 ch.4; LaValle 2006 ch.10 |
| 18 | Value iteration | 17 | RL SB4.4, PA 2.8, PA 10.3, PR 14.6 | Sutton&Barto 2018 ch.4; LaValle 2006 ch.2; LaValle 2006 ch.10; Thrun et al. 2005 ch.14 |
| 19 | Asynchronous DP and generalized policy iteration | 18, ML-045 | RL SB4.5, RL SB4.6, RL SB4.8 | Sutton&Barto 2018 ch.4 |

### RO-04 Learning values from experience: Monte Carlo and TD

No model: learn values and control from sampled episodes and from one-step bootstrapping.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 20 | Monte Carlo prediction | 16, new MA: Monte Carlo estimation | RL SB5.2, RL SB5.3, PA 10.6 | Sutton&Barto 2018 ch.5; LaValle 2006 ch.10; DeepMind x UCL 2015 L4 |
| 21 | Monte Carlo control | 20, 19 | RL SB5.4, RL SB5.5 | Sutton&Barto 2018 ch.5 |
| 22 | Off-policy learning with importance sampling | 21, new MA: Importance sampling | RL SB5.6, RL SB5.9, RL SB5.10, RL SB5.11 | Sutton&Barto 2018 ch.5 |
| 23 | TD(0) prediction | 20, 16, MA-070 | RL SB6.1, RL SB6.2, RL SB6.3, RL SB1.4, RL SB6.8 | Sutton&Barto 2018 ch.6; Sutton&Barto 2018 ch.1; Sutton 1988 |
| 24 | Sarsa and expected Sarsa | 23, 21 | RL SB6.4, RL SB6.6 | Sutton&Barto 2018 ch.6; DeepMind x UCL 2015 L5 |
| 25 | Q-learning | 24, 22, 3 | RL SB6.5, PA 10.7, RL B.3 | Sutton&Barto 2018 ch.6; LaValle 2006 ch.10; Watkins & Dayan 1992 |
| 26 | Double Q-learning | 25 | RL SB6.7 | Sutton&Barto 2018 ch.6 |
| 27 | n-step bootstrapping | 23, 22 | RL SB7.1, RL SB7.2, RL SB7.3, RL SB7.4, RL SB7.5, RL SB7.6 | Sutton&Barto 2018 ch.7; DeepMind x UCL 2021 L11 |
| 28 | Eligibility traces and TD(lambda) | 27 | RL SB12.1, RL SB12.2, RL SB12.3, RL SB12.4, RL SB12.5, RL SB12.6, RL B.2 | Sutton&Barto 2018 ch.12; Sutton 1988 |

### RO-05 Value functions that generalise

Too many states for a table: features, linear and nonparametric values, and why off-policy approximation can diverge.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 29 | Value prediction as supervised learning | 23, ML-051, ML-058 | RL SB9.1, RL SB9.2, RL SB9.3 | Sutton&Barto 2018 ch.9; DeepMind x UCL 2021 L7 |
| 30 | Linear value functions and features | 29, ML-052, ML-089, ML-060 | RL SB9.4, RL SB9.6, RL SB9.7, RL SB9.8, RL SB9.9, RL SB9.10 | Sutton&Barto 2018 ch.9 |
| 31 | Least-squares TD and nonparametric value functions | 30, ML-053, 29, ML-085, ML-089 | RL SB9.12, RL SB9.13, RL SB9.14 | Sutton&Barto 2018 ch.9 |
| 32 | Control with approximation and the average-reward setting | 30, 27, new MA: Markov chains | RL SB10.1, RL SB10.2, RL SB10.3, RL SB10.4, RL SB10.5 | Sutton&Barto 2018 ch.10 |
| 33 | The deadly triad | 32, 22 | RL SB11.1, RL SB11.2, RL SB11.3 | Sutton&Barto 2018 ch.11 |
| 34 | Bellman error geometry and gradient-TD | 33, MA-055 | RL SB11.4, RL SB11.5, RL SB11.6, RL SB11.7, RL SB11.8, RL SB9.15 | Sutton&Barto 2018 ch.11; Sutton&Barto 2018 ch.9; DeepMind x UCL 2021 L10 |

### RO-06 Policy gradients and actor-critic

Train the policy itself: gradient theorem, REINFORCE, baselines, critics, Gaussian policies, GAE.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 35 | Parameterised policies | 5, 10 | RL SB13.1, RL SB13.2 | Sutton&Barto 2018 ch.13; DeepMind x UCL 2015 L7 |
| 36 | The policy gradient theorem and REINFORCE | 35, MA-062, ML-072, 20 | RL SB13.3, RL SB13.4, RL B.5, RL SB13.5, RL B.4 | Sutton&Barto 2018 ch.13; Sutton et al. 2000; Williams 1992 |
| 37 | Baselines | 36, 27 | RL SB13.6 | Sutton&Barto 2018 ch.13 |
| 38 | Actor-critic | 37, 23, 32 | RL SB13.7, RL SB13.8, RL B.6 | Sutton&Barto 2018 ch.13; Konda & Tsitsiklis 2000 |
| 39 | Gaussian policies for continuous actions | 35, MA-024, MA-073 | RL SB13.9 | Sutton&Barto 2018 ch.13 |
| 40 | Advantage and generalized advantage estimation | 38, 28, DL-033 | RL C.14, RL C.15 | Schulman et al. 2016 (GAE) |

### RO-07 Deep RL algorithms

The algorithms robots are trained with: DQN, A2C, TRPO, PPO, DDPG, TD3, SAC.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 41 | Deep Q-networks | 25, 29, DL-040, DL-014 | RL C.1, RL C.4, RL SB16.5 | Sutton&Barto 2018 ch.16; Mnih et al. 2015 |
| 42 | Experience replay and target networks | 41, 33 | RL C.2, RL C.3 | Mnih et al. 2015 |
| 43 | Parallel advantage actor-critic (A2C/A3C) | 40, ML-091, DL-020 | RL C.8 | Mnih et al. 2016 |
| 44 | Trust regions: TRPO | 43, new MA: KL divergence, new MA: Sparse linear solves and conjugate gradient, MA-064 | RL C.12, RL C.13 | Schulman et al. 2015 |
| 45 | Proximal policy optimisation (PPO) | 44 | RL C.16 | Schulman et al. 2017; Abbeel Foundations of Deep RL L4 |
| 46 | Deterministic policy gradients: DDPG | 42, 39, DL-033 | RL C.9, RL C.10 | Lillicrap et al. 2016 |
| 47 | TD3 | 46, 26 | RL C.19 | Fujimoto et al. 2018 |
| 48 | Soft actor-critic (SAC) | 47, ML-091, new DL: Variational autoencoder | RL C.17, RL C.18 | Haarnoja et al. 2018 |

### RO-08 Robot models: pose, motion, maps and feedback control

How a robot and its world are described: uncertainty, pose, wheeled and noisy motion, kinematic chains, maps, C-space, PID.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 49 | Why a robot is never sure: state, controls and measurements | ML-003, MA-020, MA-014 | PR 1.1, PR 1.2, PR 2.12, PR 2.13, PR 14.1 | Thrun et al. 2005 ch.1; Thrun et al. 2005 ch.2; Thrun et al. 2005 ch.14 |
| 50 | Pose and wheeled-robot motion | new MA: Rigid-body transforms and homogeneous coordinates, new MA: State-space models, MA-063 | PR 5.1, PA 13.1, PA 13.3 | Thrun et al. 2005 ch.5; LaValle 2006 ch.13 |
| 51 | Probabilistic motion models: velocity and odometry | 50, new MA: Drawing samples from distributions, MA-024 | PR 5.3, PR 5.4, PR 5.5, PR 5.7, PR 5.8 | Thrun et al. 2005 ch.5 |
| 52 | Kinematic chains: where the hand and foot are | new MA: Rigid-body transforms and homogeneous coordinates, new MA: 3D rotations: Euler angles and quaternions | PA 3.10, PA 3.11, PA 3.12 | LaValle 2006 ch.3 |
| 53 | Maps and landmarks | MA-051, 49 | PR 6.1, PR 6.8, PA 3.1, PA 3.3 | Thrun et al. 2005 ch.6; LaValle 2006 ch.3 |
| 54 | Configuration space and degrees of freedom | new MA: Rigid-body transforms and homogeneous coordinates, 52 | PA 4.8, PA 4.3, PA 4.4, PA 4.14 | LaValle 2006 ch.4 |
| 55 | Obstacles in C-space | 54, 53 | PA 4.12, PA 4.13 | LaValle 2006 ch.4 |
| 56 | PD and PID control | MA-061, new MA: Stability of dynamical systems | RL R0.7 | legged_gym; Stooke et al. 2020 |

### RO-09 Sensing and Bayes filters

How a robot reads noisy sensors and tracks a hidden state: range and landmark sensor models, belief, Bayes, histogram, Kalman, EKF and particle filters.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 57 | Range sensors: the beam model | 53, MA-071, MA-073, MA-074 | PR 6.2, PR 6.4, PR 6.5, PA 11.1 | Thrun et al. 2005 ch.6; LaValle 2006 ch.11 |
| 58 | Likelihood fields and scan matching | 57, MA-009 | PR 6.6, PR 6.7 | Thrun et al. 2005 ch.6 |
| 59 | Landmark measurement model | 53, 51 | PR 6.9, PR 6.10 | Thrun et al. 2005 ch.6 |
| 60 | Belief: what the robot knows | new MA: Markov chains, 51, 57 | PR 2.14, PR 2.15, PR 2.17, PA 11.2, PA 11.3 | Thrun et al. 2005 ch.2; LaValle 2006 ch.11 |
| 61 | The Bayes filter: predict, then update | 60, MA-018, MA-019 | PR 2.7, PR 2.18, PA 11.4 | Thrun et al. 2005 ch.2; LaValle 2006 ch.11 |
| 62 | Grid filters: histogram filter and binary Bayes filter | 61, ML-019, ML-031, ML-116 | PR 4.2, PR 4.3, PR 4.5 | Thrun et al. 2005 ch.4 |
| 63 | Kalman filter | 61, MA-073, new MA: Linear transforms of a Gaussian, new MA: Product of two Gaussians | PR 3.1, PR 3.6, PA 11.8 | Thrun et al. 2005 ch.3; LaValle 2006 ch.11 |
| 64 | Extended Kalman filter | 63, MA-063, MA-064 | PR 3.7, PR 3.8 | Thrun et al. 2005 ch.3 |
| 65 | Particle filter | 61, new MA: Monte Carlo estimation, new MA: Importance sampling, ML-102 | PR 4.8, PR 4.9, PR 4.10, PA 11.10 | Thrun et al. 2005 ch.4; LaValle 2006 ch.11 |

### RO-10 Localization, occupancy maps and grid path planning

Where am I, what is around me, how do I get there on a grid: the parts a navigation stack is built from.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 66 | Markov localization on a known map | 61, 53, 62 | PR 7.1, PR 7.2, PA 12.2, PR 8.1 | Thrun et al. 2005 ch.7; LaValle 2006 ch.12; Thrun et al. 2005 ch.8 |
| 67 | Monte Carlo localization and adaptive particle counts | 65, 58, new MA: KL divergence, MA-045 | PR 8.2, PR 8.3, PR 8.8, PR 8.4, PR 8.6, PR 8.7 | Thrun et al. 2005 ch.8 |
| 68 | Occupancy grid mapping | 62, 57 | PR 9.1, PR 9.2, PR 9.3 | Thrun et al. 2005 ch.9 |
| 69 | The SLAM problem | 68, 66 | PR 10.1, PA 12.3 | Thrun et al. 2005 ch.10; LaValle 2006 ch.12 |
| 70 | Grid path planning: wavefronts, navigation functions and value iteration | 18, 68, ML-043, 14 | PR 14.7, PA 8.7, PA 14.7, PA 8.2 | Thrun et al. 2005 ch.14; LaValle 2006 ch.8; LaValle 2006 ch.14 |
| 71 | Moving through unknown maps: D* replanning and bug algorithms | 15, 68, 10 | PA 12.4, PA 12.5 | LaValle 2006 ch.12 |

### RO-11 Motion planning in continuous space

Paths for real robot shapes and real motion limits: collision checks, potential fields, RRT, PRM, kinodynamic planning, trajectory optimisation.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 72 | Collision checking and nearest neighbours in C-space | 55, 54, ML-085, MA-049, MA-029 | PA 5.7, PA 5.8, PA 5.1, PA 5.9, PA 5.3 | LaValle 2006 ch.5 |
| 73 | Potential fields | 55, MA-062 | PA 5.11 | LaValle 2006 ch.5 |
| 74 | Rapidly-exploring random trees (RRT) | 72 | PA 5.12 | LaValle 2006 ch.5 |
| 75 | Probabilistic roadmaps (PRM) | 74, 13 | PA 5.13, PA 5.14 | LaValle 2006 ch.5 |
| 76 | Planning with motion limits | 74, 50, new MA: Numerical integration of ODEs, new MA: ODEs and vector fields | PA 14.1, PA 14.2, PA 14.4, PA 14.5, PA 14.6, PA 15.9 | LaValle 2006 ch.14; LaValle 2006 ch.15 |
| 77 | Trajectory optimisation | 76, ML-056 | PA 14.9 | LaValle 2006 ch.14 |

### RO-12 Robot RL foundations and sim-to-real

Turning a robot into an MDP and getting a simulator-trained policy onto hardware.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 78 | Why robot RL is hard | 45, 48 | RL R0.1, RL R0.2, RL R0.3 | Kober, Bagnell & Peters 2013; CS285 2023 L23 |
| 79 | The robot as an MDP | 78, 8 | RL R0.4 | legged_gym config |
| 80 | Action spaces: torques, PD targets, velocity commands | 79, 56 | RL R0.5, RL R0.6 | legged_gym; Hwangbo et al. 2019; Peng & van de Panne 2017; Chen et al. 2022; Tai et al. 2017 |
| 81 | Parallel simulation and the reference training stack | 80, 45 | RL R0.8, RL R0.9, RL R0.10 | Rudin et al. 2022; Makoviychuk et al. 2021; Isaac Lab 2025; Todorov et al. 2012 |
| 82 | The reality gap and domain randomization | 81, DL-050 | RL R1.1, RL R1.2, RL R1.3, RL R1.9 | Tobin et al. 2017; Peng et al. 2018; Sadeghi & Levine 2017 |
| 83 | System identification and actuator models | 82, DL-010, ML-049 | RL R1.5, RL R1.6, RL H.8, RL L.2 | Tan et al. 2018; Hwangbo et al. 2019; He et al. 2025 (ASAP) |
| 84 | Real-robot training and sim-real agreement | 83, 48 | RL R1.7, RL R1.8 | Haarnoja et al. 2019; Kadian et al. 2020 |

### RO-13 Designing the robot task: observations, rewards, curricula

What the policy sees, what it is paid for, when episodes end, and how training gets harder.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 85 | Proprioceptive observations | 79, ML-023, new MA: 3D rotations: Euler angles and quaternions | RL R2.1, RL R2.2 | legged_gym; Rudin et al. 2022 |
| 86 | Seeing the terrain: exteroceptive inputs | 85, 68 | RL R2.3 | Miki et al. 2022; Cheng et al. 2024 |
| 87 | Goal- and command-conditioned policies | 85, 10 | RL R2.4 | Andrychowicz et al. 2017 |
| 88 | Reward = task terms + regularisation terms | 87, MA-024 | RL R2.5, RL R2.6 | legged_gym; Kim et al. 2024 |
| 89 | Reward shaping and its risks | 88 | RL R2.8, RL SB17.4 | Sutton&Barto 2018 ch.17; Ma et al. 2024 (Eureka) |
| 90 | Gaits from rewards and behaviour families | 89 | RL R2.7, RL L.8, RL R2.13 | Margolis & Agrawal 2022; Fu et al. 2021 |
| 91 | Terminations and the sign of rewards | 88, 9 | RL R2.9 | legged_gym; Chane-Sane et al. 2024 |
| 92 | Curricula: terrain, commands and automatic domain randomization | 87, 82 | RL R2.10, RL R1.4 | Rudin et al. 2022; Margolis et al. 2022; OpenAI et al. 2019 |
| 93 | Sparse rewards and hindsight relabelling | 87, 42, 46 | RL R2.11, RL M.5 | Andrychowicz et al. 2017; SB3 HER docs |
| 94 | Symmetry augmentation | 85, DL-050 | RL R2.12 | Mittal et al. 2024; Su et al. 2024 |
| 95 | Searching for rewards automatically | 89 | RL N.16, RL R2.15 | Chiang et al. 2019; Ma et al. 2024 (Eureka, DrEureka) |

### RO-14 Partial observability and privileged learning

The robot cannot see the full state: memory, privileged critics and teachers, adaptation, learned estimators.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 96 | POMDPs and belief space | 12, 61 | PR 15.1, PA 11.6, PA 12.1, RL SB17.3, RL R3.1 | Thrun et al. 2005 ch.15; LaValle 2006 ch.11; LaValle 2006 ch.12; Sutton&Barto 2018 ch.17; Lee et al. 2020 |
| 97 | History encoders: memory for a hidden state | 96, DL-061, DL-064, DL-042, DL-082 | RL R3.2 | Lee et al. 2020; Radosavovic et al. 2024 |
| 98 | Privileged information | 97 | RL R3.3 | Chen et al. 2019 (Learning by Cheating) |
| 99 | Asymmetric actor-critic | 98, 38 | RL R3.4 | Pinto et al. 2018; Nahrendra et al. 2023 |
| 100 | Behaviour cloning, compounding error and DAgger | 98, ML-049, DL-014 | RL R3.5, RL R3.6 | Ross et al. 2011; CS285 2023 L2 |
| 101 | Teacher-student distillation | 100, 99, DL-071 | RL R3.7 | Chen et al. 2019; Lee et al. 2020; Miki et al. 2022 |
| 102 | Online adaptation modules (RMA) | 101, 97 | RL R3.8 | Kumar et al. 2021 (RMA) |
| 103 | Learned state estimators: explicit and latent | 102, 63, new DL: Variational autoencoder, new DL: Contrastive learning objective | RL R3.9, RL R3.11 | Ji et al. 2022; Nahrendra et al. 2023; Long et al. 2023 |
| 104 | In-context adaptation with sequence models | 97, 82, DL-087 | RL R3.13, RL H.3 | Radosavovic et al. 2024; OpenAI et al. 2019 |
| 105 | Auxiliary tasks and general value functions | 97, 29 | RL R3.14, RL SB17.1 | Sutton&Barto 2018 ch.17; Mirowski et al. 2017; DeepMind x UCL 2021 L13 |

### RO-15 Autonomous navigation I: the navigation policy

Classical baselines, then a learned navigation policy end to end: task, observations, actions, rewards, evaluation.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 106 | Classical local planning: DWA and TEB | 77, 68, 50 | RL N.1 | Fox, Burgard & Thrun 1997; Rosmann et al. 2017 |
| 107 | The Nav2 navigation stack and ROS tooling | 106, 67, 15, 81 | RL N.26, RL §5.1 decision 2026-10-03 'The Nav2 navigation stack' (second background Note) | Macenski et al. 2020; Nav2 docs; Koenig & Howard 2004; Savva et al. 2019; Song et al. 2020 (Flightmare); CrowdNav repo |
| 108 | Learned vs classical local planners | 106, 78 | RL N.2 | Xiao et al. 2022; Kahn et al. 2018; Song et al. 2023 |
| 109 | Navigation as an MDP or POMDP | 108, 96, 79 | RL N.3 | Anderson et al. 2018; Savva et al. 2019 |
| 110 | Mapless end-to-end navigation | 109, 46 | RL N.4 | Tai, Paolo & Liu 2017; Zhu & Zhang 2021 |
| 111 | Observations for navigation: laser, vision and maps | 110, 85, 86, DL-040 | RL N.5, RL N.6 | Tai et al. 2017; Long et al. 2018; Zhu et al. 2017; Chaplot et al. 2020; Hoeller et al. 2021 |
| 112 | Action spaces for navigation | 110, 80 | RL N.7 | Tai et al. 2017; Wijmans et al. 2020; Lee et al. 2024 |
| 113 | Reward design for navigation | 112, 89 | RL N.8 | Tai et al. 2017; Long et al. 2018 |
| 114 | Sparse, time-limited goal rewards | 113, 93 | RL N.9 | Rudin et al. 2022b |
| 115 | Evaluating navigation: success, SPL, collisions | 109 | RL N.19 | Anderson et al. 2018; Wijmans et al. 2020 |

### RO-16 Autonomous navigation II: exploring, remembering and planning ahead

Long-range navigation: information-gain exploration, memory, options, planners plus RL, modular stacks.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 116 | Exploration by information gain and active localization | 96, 65, ML-091, 67 | PR 17.1, PR 17.2, PR 17.3, PR 17.4 | Thrun et al. 2005 ch.17 |
| 117 | Exploring to build a map | 116, 70 | PR 17.5 | Thrun et al. 2005 ch.17 |
| 118 | Memory and auxiliary tasks for visual navigation | 111, 105 | RL N.10 | Mirowski et al. 2017; Zhu et al. 2017 |
| 119 | Options: temporal abstraction | 112, 8 | RL SB17.2 | Sutton&Barto 2018 ch.17 |
| 120 | Planners plus RL | 75, 110, 119 | RL N.15 | Faust et al. 2018; Francis et al. 2020 |
| 121 | Modular learned navigation vs end-to-end | 120, 68, 117 | RL N.17 | Chaplot et al. 2020 |

### RO-17 Safety and constraints

Say what not to do: constrained MDPs, Lagrangian/CPO/barrier methods, Kim et al. constraint types, CaT, shields.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 122 | Constrained MDPs and cost critics | 8, 38, MA-066 | RL R4.1, RL R4.2 | Altman 1999; Achiam et al. 2017 |
| 123 | Lagrangian and PID-Lagrangian PPO | 122, 45, MA-067, 56 | RL R4.3, RL R4.4 | Ray et al. 2019; Stooke et al. 2020 |
| 124 | CPO, barriers and penalties | 123, 44, MA-068 | RL R4.5, RL R4.6, RL R4.7 | Achiam et al. 2017; Liu et al. 2020; Zhang et al. 2022 |
| 125 | Not only rewards but also constraints: constraint types for real robots | 124 | RL R4.8, RL R4.9, RL R4.13 | Kim et al. 2024 (T-RO); Lee et al. 2023; Safety-Gymnasium; OmniSafe; Gu et al. 2022 |
| 126 | Constraints as terminations | 125, 91 | RL R4.10 | Chane-Sane et al. 2024 (CaT) |
| 127 | Shields, safety filters and recovery policies | 122 | RL R4.11, RL R4.12 | Alshiekh et al. 2018; He et al. 2024 (ABS) |

### RO-18 Autonomous navigation III: crowds, scale and the real world

Many agents, billions of frames, real-robot data, sim-to-real, safety and fast flight.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 128 | Multi-agent collision avoidance and social norms | 109, 29 | RL N.11, RL N.12 | Chen et al. 2017 (CADRL, SA-CADRL) |
| 129 | Crowds and robot teams: attention pooling and shared policies | 128, DL-061, DL-073, 45 | RL N.13, RL N.14 | Everett et al. 2018; Chen et al. 2019 (SARL); Long et al. 2018 |
| 130 | Navigation at scale | 107, 81 | RL N.18 | Savva et al. 2019; Wijmans et al. 2020 |
| 131 | Self-supervised real-world navigation | 84, 109 | RL N.20 | Kahn et al. 2018; Kahn et al. 2021 (BADGR); Gandhi et al. 2017 |
| 132 | Sim-to-real for navigation | 82, 84, 111 | RL N.21 | Sadeghi & Levine 2017; Tai et al. 2017; Kadian et al. 2020 |
| 133 | Safety in navigation | 127, 126, 113 | RL N.25 | He et al. 2024; Alshiekh et al. 2018 |
| 134 | Agile aerial navigation | 101, 83, 77 | RL N.24 | Loquercio et al. 2021; Kaufmann et al. 2023; Song et al. 2023 |

### RO-19 Planning with models, search and games

Use a model to plan: Dyna, prioritized sweeping, rollouts, MCTS, games and self-play, MuZero, world models.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 135 | Models and Dyna | 25 | RL SB8.1, RL SB8.2, RL SB8.3, RL SB14.7 | Sutton&Barto 2018 ch.8; DeepMind x UCL 2015 L8 |
| 136 | Prioritized sweeping and where to spend updates | 135, 14 | RL SB8.4, RL SB8.5, RL SB8.6 | Sutton&Barto 2018 ch.8 |
| 137 | Decision-time planning and rollouts | 135, 15 | RL SB8.7, RL SB8.8 | Sutton&Barto 2018 ch.8 |
| 138 | Monte Carlo tree search | 137, 4 | RL SB8.9 | Sutton&Barto 2018 ch.8 |
| 139 | Games: minimax, alpha-beta and equilibria | 7, MA-068, MA-066, 13 | PA 9.6, PA 9.7, PA 9.8, PA 10.8, PA 10.9 | LaValle 2006 ch.9; LaValle 2006 ch.10; DeepMind x UCL 2015 L10 |
| 140 | Self-play: from TD-Gammon to AlphaZero | 138, 139, 41, 36 | RL SB16.1, RL SB16.2, RL SB16.6, RL C.5, RL C.6, RL C.7 | Sutton&Barto 2018 ch.16; Silver et al. 2016; Silver et al. 2017; DeepMind x UCL 2018 L10 |
| 141 | Planning with a learned model: MuZero | 140 | RL E.10 | Schrittwieser et al. 2020 |
| 142 | World models and imagined rollouts | 141, 48, DL-064 | RL E.11 | Hafner et al. 2023 |

### RO-20 Legged robots: quadrupeds and humanoids

The PPO locomotion recipe and its extensions, legged navigation, then humanoid imitation and whole-body control.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 143 | The PPO locomotion recipe, end to end | 92, 101, 126 | RL L.1 | Rudin et al. 2022; Lee et al. 2020; Hwangbo et al. 2019 |
| 144 | Perceptive locomotion | 143, 86 | RL L.3 | Miki et al. 2022 |
| 145 | Agility: high speed and parkour | 144, 102, 100 | RL L.4, RL L.5, RL H.10 | Margolis et al. 2022; Zhuang et al. 2023; Cheng et al. 2024; Zhuang et al. 2024 |
| 146 | Tracking model-based reference motions | 143, 77 | RL L.7 | Jenelten et al. 2024 |
| 147 | Navigation on legged and wheeled-legged robots | 145, 114, 119, 101 | RL N.22, RL L.6, RL N.23 | Hoeller et al. 2021; Rudin et al. 2022b; Hoeller et al. 2024; Lee et al. 2024 |
| 148 | Motion imitation and adversarial motion priors | 88, 91, DL-003 | RL H.1, RL H.2, RL R2.14 | Peng et al. 2018 (DeepMimic); Peng et al. 2021 (AMP); Escontrela et al. 2022 |
| 149 | Whole-body tracking from human data | 148, 101, 52, new DL: Diffusion models | RL H.5, RL H.6, RL H.9 | He et al. 2024 (H2O, OmniH2O); Fu et al. 2024 (HumanPlus); Cheng et al. 2024 (Exbody); Liao et al. 2025 (BeyondMimic) |
| 150 | Multi-skill humanoid controllers | 149, 140 | RL H.4, RL H.7 | Haarnoja et al. 2024; He et al. 2025 (HOVER) |

### RO-21 Manipulation

Arms and hands: planning, visuomotor policies, grasping at scale, residual RL, dexterity, demonstrations.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 151 | Manipulation planning | 75, 52 | PA 7.4, PA 12.7 | LaValle 2006 ch.7; LaValle 2006 ch.12 |
| 152 | End-to-end visuomotor policies | 78, 77, DL-040 | RL M.1 | Levine et al. 2016 |
| 153 | Grasping from large real datasets | 152, 42 | RL M.2, RL M.3, RL M.4 | Levine et al. 2018; Kalashnikov et al. 2018 |
| 154 | Residual RL | 78, 56 | RL M.6 | Johannink et al. 2019; Silver et al. 2018 |
| 155 | Dexterous in-hand manipulation | 92, 104, 102 | RL M.7, RL M.8 | OpenAI et al. 2018; OpenAI et al. 2019; Handa et al. 2023; Qi et al. 2022 |
| 156 | Vision-based dexterity | 155, 101, 88, 83 | RL M.9, RL M.10, RL M.12 | Chen et al. 2023; Qin et al. 2022 (DexPoint); Lin et al. 2025 |
| 157 | Demonstrations from human videos | 100 | RL M.11 | Qin et al. 2022 (DexMV) |

### RO-22 State estimation and SLAM in depth *(optional)*

Optional classical depth: UKF and information filters, landmark localization, data association, MAP mapping, EKF SLAM, GraphSLAM, FastSLAM, map merging and multi-robot exploration.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 158 | Unscented Kalman filter | 64, new MA: Cholesky factor | PR 3.11, PR 3.12 | Thrun et al. 2005 ch.3 |
| 159 | Information filter | 63, new MA: Woodbury identity | PR 3.13, PR 3.14 | Thrun et al. 2005 ch.3 |
| 160 | EKF and UKF localization | 66, 64, 158, 59 | PR 7.3, PR 7.8 | Thrun et al. 2005 ch.7 |
| 161 | Data association and multi-hypothesis tracking | 160, new MA: Mahalanobis distance, MA-070, MA-073 | PR 7.4, PR 7.5, PR 3.9, PR 7.7 | Thrun et al. 2005 ch.7; Thrun et al. 2005 ch.3 |
| 162 | Learned sensor models and MAP mapping | 68, MA-072, DL-014 | PR 9.4, PR 9.5, PR 9.6 | Thrun et al. 2005 ch.9 |
| 163 | EKF SLAM | 69, 160 | PR 10.2, PR 10.3 | Thrun et al. 2005 ch.10 |
| 164 | EKF SLAM with unknown landmarks | 163, 161 | PR 10.4, PR 10.5, PR 12.4, PR 12.6 | Thrun et al. 2005 ch.10; Thrun et al. 2005 ch.12 |
| 165 | Pose graphs and GraphSLAM | 159, 69, new MA: Nonlinear least squares (Gauss-Newton), new MA: Schur complement, new MA: Sparse linear solves and conjugate gradient, MA-070 | PR 11.1, PR 11.2, PR 11.4, PR 11.7 | Thrun et al. 2005 ch.11 |
| 166 | FastSLAM: particles over paths | 65, 163 | PR 13.1, PR 13.2, PR 13.3, PR 13.4, PR 13.7, PR 17.7 | Thrun et al. 2005 ch.13 |
| 167 | Loop closure and map merging | 165, 166 | PR 13.6, PR 12.7 | Thrun et al. 2005 ch.13; Thrun et al. 2005 ch.12 |
| 168 | Multi-robot exploration | 117, 167 | PR 17.6 | Thrun et al. 2005 ch.17 |

### RO-23 Planning and control in depth *(optional)*

Optional classical depth: exact POMDP planning, exact roadmaps, time and many robots, coverage, HJB and LQR.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 169 | Exact POMDP planning: alpha vectors | 96, 18 | PR 15.2, PR 15.3, PR 15.4 | Thrun et al. 2005 ch.15 |
| 170 | Approximate POMDP planning | 169, 65 | PR 16.1, PR 16.2, PR 16.3 | Thrun et al. 2005 ch.16 |
| 171 | Exact roadmaps | 55, 15 | PA 6.1, PA 6.2, PA 6.3 | LaValle 2006 ch.6 |
| 172 | Planning with time and many robots | 75, 76 | PA 7.1, PA 7.2, PA 14.8 | LaValle 2006 ch.7; LaValle 2006 ch.14 |
| 173 | Coverage planning | 171 | PA 7.7 | LaValle 2006 ch.7 |
| 174 | Continuous-time optimal control: HJB and LQR | 18, new MA: State-space models, 56 | PA 15.6, PA 15.7 | LaValle 2006 ch.15 |

### RO-24 Offline RL and robot foundation models

Learning from fixed data and pretrained models: offline RL, CQL, Decision Transformer, VLAs, flow-matching experts, real-world RL fine-tuning.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 175 | Offline RL and distribution shift | 153, 100 | RL E.12 | Levine et al. 2020 |
| 176 | Conservative Q-learning | 175 | RL E.13 | Kumar et al. 2020 |
| 177 | RL as sequence modelling: Decision Transformer | 175, DL-087 | RL E.14 | Chen et al. 2021 |
| 178 | Vision-language-action models and generalist robot policies | 100, DL-071, DL-053 | RL E.15, RL E.16, RL E.20, RL E.21 | Brohan et al. 2023 (RT-2); Kim et al. 2024 (OpenVLA); Gemini Robotics Team 2025; NVIDIA 2025 (GR00T N1) |
| 179 | Flow-matching action experts | 178, new DL: Flow matching | RL E.17, RL E.18 | Black et al. 2024 (pi0); Physical Intelligence 2025 (pi0.5) |
| 180 | Navigation foundation models | 178, 109, new DL: Diffusion models | RL N.27 | Shah et al. 2023 (GNM, ViNT); Sridhar et al. 2024 (NoMaD) |
| 181 | Real-world RL with human corrections | 84, 48 | RL E.22, RL E.23 | Luo et al. 2024 (SERL); Luo et al. 2024 (HIL-SERL) |
| 182 | RL fine-tuning of a VLA | 179, 181, 40 | RL E.19 | Physical Intelligence 2025 (pi*0.6 / RECAP) |

### RO-25 RL for language models *(optional)*

Optional: the same policy-gradient machinery applied to LLMs: preference reward models, RLHF, DPO, GRPO, RLVR.

| # | Note | Builds on | Doc rows | Sources |
|---|---|---|---|---|
| 183 | Reward models from human preferences | DL-067, ML-071, ML-072 | RL E.1, RL E.2 | Christiano et al. 2017 |
| 184 | RLHF with PPO and a KL penalty | 183, 45, new MA: KL divergence | RL E.3 | Ouyang et al. 2022 |
| 185 | Direct preference optimisation | 184 | RL E.4 | Rafailov et al. 2023 |
| 186 | Group-relative advantages: GRPO | 184, 37 | RL E.5 | Shao et al. 2024 |
| 187 | RL with verifiable rewards | 186 | RL E.6, RL E.7 | DeepSeek-AI 2025; Lambert et al. 2024 |
| 188 | Fixing GRPO at scale | 187 | RL E.8, RL E.9 | Yu et al. 2025; Liu et al. 2025 |

## 3. New maths and deep-learning Notes (34)

These Notes must be written before the RO Note that first needs them. Pieces marked "short section" go inside that RO Note.

**Gap: a new DL chapter, "Generative models for control".** It needs Notes on the VAE, the contrastive loss, diffusion and flow matching. No DL Note covers them; RL scope §5 lists diffusion and flow matching as unowned. The doc rows that need it:

| Model | Rows |
|---|---|
| VAE | R3.10, C.18 |
| Contrastive loss | R3.12 |
| Diffusion | H.9, N.27 |
| Flow matching | E.17 |

**The reparameterization trick** lives in the DL VAE Note, where it first appeared (Kingma & Welling 2014, *Auto-Encoding Variational Bayes*, arXiv 1312.6114). SAC (Note 48) recaps it.

| Concept | What | Where | First needed by |
|---|---|---|---|
| Markov chains | Markov property / Markov assumption, transition matrix, stationary distribution | MA 02-probability (new Note after MA-019) | 8 Markov decision processes |
| Geometric series | sum of r^k = 1/(1-r) for \|r\|<1 | MA 06-calculus (new Note) | 9 Return and discounting |
| Monte Carlo estimation | estimate an expectation by averaging random samples; a sample set stands for a distribution | MA 04-inference (new Note after MA-034) | 20 Monte Carlo prediction |
| Importance sampling | target, proposal, weights; ordinary vs weighted; variance | MA 04-inference (new Note after Monte Carlo estimation) | 22 Off-policy learning with importance sampling |
| KL divergence | what it measures, how to compute it | MA 08-likelihood (new Note after MA-072) | 44 Trust regions: TRPO |
| Linear transforms of a Gaussian | mean A mu, covariance A Sigma A^T | MA 08-likelihood (new Note after MA-073) | 63 Kalman filter |
| Product of two Gaussians | completing the square | MA 08-likelihood (same new Note as linear transforms) | 63 Kalman filter |
| Mahalanobis distance | distance scaled by a covariance; gating | MA 05-linear-algebra (new Note) | 161 Data association and multi-hypothesis tracking |
| Woodbury identity | inverse of matrix plus low-rank change | MA 05-linear-algebra (new Note) | 159 Information filter |
| Cholesky factor | matrix square root, needed for sigma points | MA 05-linear-algebra (new Note) | 158 Unscented Kalman filter |
| Schur complement | marginalising variables out of a block matrix | MA 05-linear-algebra (new Note) | 165 Pose graphs and GraphSLAM |
| Sparse linear solves and conjugate gradient | sparse systems, relaxation, conjugate gradient; also used by TRPO | MA 05-linear-algebra (new Note) | 44 Trust regions: TRPO |
| Nonlinear least squares (Gauss-Newton) | re-linearise and re-solve in a loop | MA 07-optimisation (new Note) | 165 Pose graphs and GraphSLAM |
| Drawing samples from distributions | sampling recipes, triangular distribution | MA 03-distributions (new Note) | 51 Probabilistic motion models: velocity and odometry |
| Rigid-body transforms and homogeneous coordinates | rotate + translate, homogeneous matrix, SE(2)/SE(3), heading angles kept in -pi..pi; 2D rotation by any angle (cos, sin), headings kept in -pi..pi (MA-053 shows only the 90-degree case) | MA 05-linear-algebra (new Note after MA-054) | 50 Pose and wheeled-robot motion |
| 3D rotations: Euler angles and quaternions | yaw, pitch, roll; quaternions | MA 05-linear-algebra (new Note) | 52 Kinematic chains: where the hand and foot are |
| ODEs and vector fields | an equation for change; following the arrows | MA 06-calculus (new Note) | 76 Planning with motion limits |
| State-space models | phase space, x_dot = Ax + Bu, nonlinear systems | MA 06-calculus (new Note) | 50 Pose and wheeled-robot motion |
| Numerical integration of ODEs | Euler and Runge-Kutta steps | MA 06-calculus (new Note) | 76 Planning with motion limits |
| Stability of dynamical systems | equilibria, eigenvalues, Lyapunov functions | MA 06-calculus (new Note) | 56 PD and PID control |
| Newtonian and rigid-body mechanics | F = ma, torque, inertia matrix, angular velocity | short RO section inside "PD and PID control" (mechanics is physics; CONTEXT.md defines MA as linear algebra, calculus, optimisation, probability, statistics) | 56 PD and PID control |
| Variational autoencoder | reconstruction + beta KL; reparameterization | DL new chapter "Generative models" (RL scope 5.1 decision) | 48 Soft actor-critic (SAC) |
| Contrastive learning objective | pull matching pairs together, push others apart | DL new chapter "Generative models" | 103 Learned state estimators: explicit and latent |
| Diffusion models | flagged unowned in RL scope 5 | DL new chapter "Generative models" (added: prerequisite of humanoid diffusion tracking and navigation foundation models) | 149 Whole-body tracking from human data |
| Flow matching | flagged unowned in RL scope 5 | DL new chapter "Generative models" (added: prerequisite of flow-matching action experts) | 179 Flow-matching action experts |
| Robbins-Monro step-size conditions |  | new maths: short section inside the RO Note that first uses it | 3 Incremental updates and step sizes |
| Control variates (why a baseline cuts variance) |  | new maths: short section inside the RO Note that first uses it | 37 Baselines |
| Log-derivative trick |  | new maths: short section inside the RO Note that first uses it | 36 The policy gradient theorem and REINFORCE |
| Fourier basis features |  | new maths: short section inside the RO Note that first uses it | 30 Linear value functions and features |
| Natural gradient and Fisher information |  | new maths: short section inside the RO Note that first uses it | 44 Trust regions: TRPO |
| Priority queue and Big-O cost |  | new maths: short section inside the RO Note that first uses it | 14 Dijkstra's algorithm and priority queues |
| Canonical (information) form of a Gaussian |  | new maths: short section inside the RO Note that first uses it | 159 Information filter |
| Bradley-Terry preference model |  | new maths: short section inside the RO Note that first uses it | 183 Reward models from human preferences |
| Cross-entropy method (derivative-free max over actions) |  | new maths: short section inside the RO Note that first uses it | 153 Grasping from large real datasets |

## 4. Recap only: already taught in MA/ML/DL (26)

| Concept | Home | Doc row |
|---|---|---|
| Constant step size = EWMA | DL-033#1-overview | RL SB2.6 |
| Polynomial features | ML-060#3-adding-powers-as-new-features | RL SB9.5 |
| Neural networks as function approximators | DL-010#6-the-whole-network-in-one-formula | RL SB9.11 |
| Random variables, PMF and PDF | MA-020#2-random-variables | PR 2.1 |
| Joint, marginal and conditional probability | MA-014#2-joint-probability | PR 2.2 |
| Independence | MA-016#2-the-definition | PR 2.3 |
| Law of total probability | MA-019#1-overview | PR 2.4 |
| Bayes' theorem, prior, posterior | MA-018#4-the-formula-and-its-proof | PR 2.5 |
| Normalising constant (Bayes without the evidence) | ML-082#3-step-1-bayes-theorem-without-the-evidence | PR 2.6 |
| Expected value, variance, covariance | MA-012#3-expected-value | PR 2.8 |
| Entropy of a distribution | ML-091#61-disorder-and-uncertainty | PR 2.9 |
| Normal distribution | MA-024#5-the-pdf-of-the-normal-distribution | PR 2.10 |
| Multivariate normal distribution | MA-073#71-the-multivariate-normal | PR 2.11 |
| Matrix inverse | ML-053#6-the-normal-equation | PR 3.4 |
| Histogram | ML-019#6-histogram | PR 4.1 |
| Log-odds | ML-116#4-stage-1-the-log-odds-of-class-1 | PR 4.4 |
| Exponential distribution | MA-071#31-the-distribution-of-waiting-times | PR 6.3 |
| Rotation as a linear map (MA-053 shows the 90-degree case; any angle theta is new, see new_maths rigid-body transforms) | MA-053#6-reading-a-matrix-as-a-picture | PA 3.4 |
| Chaining transforms by matrix multiplication | MA-054#22-following-the-basis-vectors | PA 3.5 |
| Scaling and shear | MA-053#6-reading-a-matrix-as-a-picture | PA 3.6 |
| Gradient of a potential function | MA-062#4-the-gradient | PA 5.10 |
| Probability space, conditional probability, marginalising | MA-015#2-the-definition | PA 9.2 |
| Random variables and expectation | MA-012#3-expected-value | PA 9.3 |
| Multivariate Gaussian | MA-073#71-the-multivariate-normal | PA 11.7 |
| Jacobian for velocity relations | MA-063#42-the-formula-every-partial-derivative-in-one-grid | PA 13.2 |
| Taylor linearisation of a system | MA-064#7-where-ml-uses-second-order-approximations | PA 15.1 |

## 5. Overlaps merged (60)

One concept named in more than one doc (or twice in one doc), kept as one Note.

| Concept | Rows | Kept as |
|---|---|---|
| pose (x, y, heading), holonomic vs nonholonomic constraints | PR 5.1, PA 13.1, PA 13.3 | Pose and wheeled-robot motion |
| feature-based vs grid maps, obstacles as polygons built from half-planes | PR 6.1, PR 6.8, PA 3.1, PA 3.3 | Maps and landmarks |
| beam model: one reading as a mix of four error types, mixture density of different shapes | PR 6.2, PR 6.4, PR 6.5, PA 11.1 | Range sensors: the beam model |
| state transition and measurement probabilities, hidden Markov model / dynamic Bayes network | PR 2.14, PR 2.15, PR 2.17, PA 11.2, PA 11.3 | Belief: what the robot knows |
| Bayes' theorem conditioned on past data, Bayes filter predict and update steps | PR 2.7, PR 2.18, PA 11.4 | The Bayes filter: predict, then update |
| linear Gaussian system, Kalman filter and the Kalman gain | PR 3.1, PR 3.6, PA 11.8 | Kalman filter |
| resampling and the low-variance sampler, particle filter | PR 4.8, PR 4.9, PR 4.10, PA 11.10 | Particle filter |
| tracking, global and kidnapped-robot localization, Markov localization | PR 7.1, PR 7.2, PA 12.2 | Markov localization on a known map |
| online SLAM vs full SLAM | PR 10.1, PA 12.3 | The SLAM problem |
| reward as a number to maximise over time, possibly delayed, exploration vs exploitation | RL SB1.1, RL SB1.2, RL SB1.3, RL SB1.5, PR 14.2 | The reinforcement learning problem |
| agent-environment interface per time step, MDP dynamics p(s', r | s, a) | RL SB3.1, RL SB3.4, RL SB3.5, PR 14.3, PA 10.1, PA 10.2 | Markov decision processes |
| return, episodes, episodic vs continuing tasks, discount factor and horizon | RL SB3.6, PR 14.4, PA 10.5 | Return and discounting |
| Bellman expectation equation, backup diagrams | RL SB3.10, RL SB3.11, RL SB3.14, RL B.1, PR 14.5 | Bellman equations |
| policy improvement theorem, policy iteration | RL SB4.2, RL SB4.3, PA 10.4 | Policy improvement and policy iteration |
| value iteration, cost-to-go as the planning name for value | RL SB4.4, PA 2.8, PA 10.3, PR 14.6 | Value iteration |
| value iteration on a robot grid map, DP with interpolation on continuous spaces | PR 14.7, PA 8.7, PA 14.7 | Grid path planning: wavefronts, navigation functions and value iteration |
| first-visit and every-visit MC prediction, MC estimation of action values | RL SB5.2, RL SB5.3, PA 10.6 | Monte Carlo prediction |
| Q-learning (off-policy TD control), convergence of Q-learning | RL SB6.5, PA 10.7, RL B.3 | Q-learning |
| lambda-return, eligibility traces; forward vs backward view | RL SB12.1, RL SB12.2, RL SB12.3, RL SB12.4, RL SB12.5, RL SB12.6, RL B.2 | Eligibility traces and TD(lambda) |
| policy gradient theorem, log-derivative trick | RL SB13.3, RL SB13.4, RL B.5 | The policy gradient theorem and REINFORCE |
| Monte Carlo policy gradient (REINFORCE family) | RL SB13.5, RL B.4 | The policy gradient theorem and REINFORCE |
| one-step actor-critic, policy gradient for continuing problems | RL SB13.7, RL SB13.8, RL B.6 | Actor-critic |
| CNN trained with Q-learning targets on raw pixels, error clipping in the TD loss | RL C.1, RL C.4, RL SB16.5 | Deep Q-networks |
| self-play TD learning (TD-Gammon, Samuel checkers), policy network + value network + tree search | RL SB16.1, RL SB16.2, RL SB16.6, RL C.5, RL C.6, RL C.7 | Self-play: from TD-Gammon to AlphaZero |
| partially observable MDP, planning in belief / information space | PR 15.1, PA 11.6, PA 12.1, RL SB17.3, RL R3.1 | POMDPs and belief space |
| system identification and actuator networks, delta (residual) action model learned from real data | RL R1.5, RL R1.6, RL H.8, RL L.2 | System identification and actuator models |
| reward shaping and reward hacking, designing reward signals: sparse, shaped, imitation, inverse RL | RL R2.8, RL SB17.4 | Reward shaping and its risks |
| gait shaping: feet air time, clearance, energy, gaits emerging from energy minimisation | RL R2.7, RL L.8, RL R2.13 | Gaits from rewards and behaviour families |
| Hindsight Experience Replay, goal-conditioned manipulation with sparse rewards | RL R2.11, RL M.5 | Sparse rewards and hindsight relabelling |
| evolutionary search over reward weights and network shape (AutoRL), reward code written by a language model | RL N.16, RL R2.15 | Searching for rewards automatically |
| adaptation from history without weight updates, humanoid walking sim-to-real with a causal transformer, zero-shot | RL R3.13, RL H.3 | In-context adaptation with sequence models |
| general value functions, auxiliary losses (depth, loop closure) for representation | RL R3.14, RL SB17.1 | Auxiliary tasks and general value functions |
| adaptive velocity curriculum + online system identification for running, soft-then-hard obstacle curriculum; distil skills into one depth policy with DAgger | RL L.4, RL L.5, RL H.10 | Agility: high speed and parkour |
| motion imitation reward with reference-state starts, discriminator style reward (AMP) plus task reward | RL H.1, RL H.2, RL R2.14 | Motion imitation and adversarial motion priors |
| learned navigation over a locomotion policy; end-to-end locomotion + local navigation, skill hierarchies for agile navigation (parkour) | RL N.22, RL L.6, RL N.23 | Navigation on legged and wheeled-legged robots |
| Markov chains | RL SB3.2, RL SB3.3, PR 2.16 | new maths: Markov chains |
| Monte Carlo estimation | RL SB5.1, PR 4.6 | new maths: Monte Carlo estimation |
| Importance sampling | RL SB5.7, RL SB5.8, PR 4.7, PA 11.9 | new maths: Importance sampling |
| KL divergence | RL C.11, PR 8.5 | new maths: KL divergence |
| Rigid-body transforms and homogeneous coordinates | PA 3.7, PA 3.8, PA 4.11, PR 5.2 | new maths: Rigid-body transforms and homogeneous coordinates |
| Policies, plans and value functions | RL SB3.8, RL SB3.9, PA 1.1, PA 1.2, PA 1.3, PA 8.1, PA 1.1, PA 1.2 | Policies, plans and value functions |
| Least-squares TD and nonparametric value functions | RL SB9.12, RL SB9.13, RL SB9.14, RL SB9.13, RL SB9.14 | Least-squares TD and nonparametric value functions |
| Control with approximation and the average-reward setting | RL SB10.1, RL SB10.2, RL SB10.3, RL SB10.4, RL SB10.5, RL SB10.3, RL SB10.4, RL SB10.5 | Control with approximation and the average-reward setting |
| The policy gradient theorem and REINFORCE | RL SB13.3, RL SB13.4, RL B.5, RL SB13.5, RL B.4, RL SB13.5, RL B.4 | The policy gradient theorem and REINFORCE |
| Markov localization on a known map | PR 7.1, PR 7.2, PA 12.2, PR 8.1, PR 8.1 | Markov localization on a known map |
| Monte Carlo localization and adaptive particle counts | PR 8.2, PR 8.3, PR 8.8, PR 8.4, PR 8.6, PR 8.7, PR 8.4, PR 8.6 | Monte Carlo localization and adaptive particle counts |
| Grid path planning: wavefronts, navigation functions and value iteration | PR 14.7, PA 8.7, PA 14.7, PA 8.2, PA 8.2 | Grid path planning: wavefronts, navigation functions and value iteration |
| Moving through unknown maps: D* replanning and bug algorithms | PA 12.4, PA 12.5, PA 12.5 | Moving through unknown maps: D* replanning and bug algorithms |
| Collision checking and nearest neighbours in C-space | PA 5.7, PA 5.8, PA 5.1, PA 5.9, PA 5.3, PA 5.1, PA 5.9, PA 5.3 | Collision checking and nearest neighbours in C-space |
| Curricula: terrain, commands and automatic domain randomization | RL R2.10, RL R1.4, RL R1.4 | Curricula: terrain, commands and automatic domain randomization |
| Behaviour cloning, compounding error and DAgger | RL R3.5, RL R3.6, RL R3.6 | Behaviour cloning, compounding error and DAgger |
| Learned state estimators: explicit and latent | RL R3.9, RL R3.11, RL R3.11 | Learned state estimators: explicit and latent |
| Lagrangian and PID-Lagrangian PPO | RL R4.3, RL R4.4, RL R4.4 | Lagrangian and PID-Lagrangian PPO |
| Not only rewards but also constraints: constraint types for real robots | RL R4.8, RL R4.9, RL R4.13, RL R4.9, RL R4.13 | Not only rewards but also constraints: constraint types for real robots |
| Observations for navigation: laser, vision and maps | RL N.5, RL N.6, RL N.6 | Observations for navigation: laser, vision and maps |
| Exploration by information gain and active localization | PR 17.1, PR 17.2, PR 17.3, PR 17.4, PR 17.4 | Exploration by information gain and active localization |
| Crowds and robot teams: attention pooling and shared policies | RL N.13, RL N.14, RL N.14 | Crowds and robot teams: attention pooling and shared policies |
| Vision-language-action models and generalist robot policies | RL E.15, RL E.16, RL E.20, RL E.21, RL E.20, RL E.21 | Vision-language-action models and generalist robot policies |
| Data association and multi-hypothesis tracking | PR 7.4, PR 7.5, PR 3.9, PR 7.7, PR 3.9, PR 7.7 | Data association and multi-hypothesis tracking |
| Games: minimax, alpha-beta and equilibria | PA 9.6, PA 9.7, PA 9.8, PA 10.8, PA 10.9, PA 10.8, PA 10.9 | Games: minimax, alpha-beta and equilibria |

## 6. Dropped (57)

| Row | Topic | Why |
|---|---|---|
| RL SB1.6 | History: optimal control, trial-and-error, temporal differences | history, context only; one line in the RL-problem Note is enough |
| RL SB16.3 | Watson's Daily-Double wagering | case study only (S&B ch.16); teaches no new concept |
| RL SB16.4 | Optimizing memory control | case study only (S&B ch.16); teaches no new concept |
| RL SB16.8 | Thermal soaring | case study only (S&B ch.16); teaches no new concept |
| RL SB17.5 | Remaining issues; RL and the future of AI (safety) | open-issues essay, no concept; safety is taught in the safety chapter |
| PR 12.1 | SEIF SLAM | no Note builds on it; GraphSLAM and FastSLAM already teach SLAM; past beginner depth |
| PR 12.2 | Sparsification of the information matrix | part of SEIF; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PR 12.3 | Amortized approximate map recovery | part of SEIF; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PR 12.5 | Branch-and-bound search | search technique for data association; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PR 13.5 | Tree-based landmark storage (log-time updates) | implementation detail (tree storage) of FastSLAM |
| PA 2.10 | Propositional logic (true/false statements, AND/OR/NOT) | logic-based (symbolic) planning; no robot RL or navigation Note uses it |
| PA 2.11 | STRIPS representation (planning with logic statements) | logic-based (symbolic) planning; no robot RL or navigation Note uses it |
| PA 2.12 | Plan-space search and planning graphs | logic-based (symbolic) planning; no robot RL or navigation Note uses it |
| PA 2.13 | Planning as satisfiability (SAT) | logic-based (symbolic) planning; no robot RL or navigation Note uses it |
| PA 3.2 | Semi-algebraic models (shapes from polynomial inequalities) | semi-algebraic models; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 4.1 | Topological space, open and closed sets | topology; C-space is taught in plain words instead; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 4.2 | Continuous function and homeomorphism | topology; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 4.5 | Paths, connectedness, simply connected | topology; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 4.6 | Groups (basic group theory) | group theory; SE(2)/SE(3) are taught as matrices in the new rigid-body MA Note |
| PA 4.7 | Fundamental group | topology; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 4.9 | Rotations as complex numbers (SO(2)) | a second way to write 2D rotations; the rotation matrix is enough |
| PA 4.15 | Closed kinematic chains and algebraic varieties | closed chains and algebraic varieties; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 5.2 | Measure (a general idea of length, area, volume) | measure theory; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 5.4 | Pseudorandom numbers and testing randomness | how random-number generators are built and tested; trivia for this course (seeds are in ML-111) |
| PA 5.5 | Dispersion, grids and lattices | dispersion theory of samples; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 5.6 | Discrepancy and low-discrepancy sequences (van der Corput, Halton, Hammersley) | low-discrepancy sequences; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 6.4 | Cell complexes | exact algebraic planning (LaValle Block G, marked optional and heavy) |
| PA 6.5 | Tarski sentences and quantifier elimination | exact algebraic planning (LaValle Block G, marked optional and heavy) |
| PA 6.6 | Cylindrical algebraic decomposition | exact algebraic planning (LaValle Block G, marked optional and heavy) |
| PA 6.7 | Canny's roadmap algorithm | exact algebraic planning (LaValle Block G, marked optional and heavy) |
| PA 6.9 | Davenport-Schinzel sequences | exact algebraic planning (LaValle Block G, marked optional and heavy) |
| PA 7.3 | Hybrid systems (discrete modes + continuous motion) | hybrid systems; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 7.5 | Closed-chain planning (active-passive links, random loop generator) | closed-chain planning; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 7.6 | Folding problems (protein folding, unknotting) | protein folding and unknotting are outside robotics |
| PA 8.5 | Smooth manifolds and tangent spaces | differential geometry; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 8.6 | Composition of funnels | funnel composition; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 11.5 | Nondeterministic finite automata | automata theory; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 12.6 | Visibility-based pursuit-evasion | pursuit-evasion; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 13.9 | Calculus of variations | calculus of variations; simulators give the dynamics, advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 13.10 | Lagrangian mechanics and the Euler-Lagrange equation | Lagrangian mechanics; simulators give the dynamics, advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 13.11 | Hamiltonian mechanics | Hamiltonian mechanics; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 13.12 | Differential games | differential games; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 15.5 | Controllability and small-time local controllability (STLC) | controllability theory; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 15.8 | Pontryagin's minimum principle | Pontryagin's principle; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 15.10 | Control-affine systems and distributions | nonholonomic control theory; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 15.11 | Lie brackets, Lie algebra, Frobenius and Chow-Rashevskii theorems | Lie brackets; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| PA 15.12 | Steering methods (P. Hall basis, sinusoids, piecewise-constant inputs) | steering methods; advanced theory beyond beginner depth; no navigation, locomotion, manipulation or RL Note needs it |
| RL SB14.1 | Prediction vs control in animal learning | psychology/neuroscience context (S&B ch.14-15, optional Block 17 of the RL scope); no robot or navigation Note needs it; beginner depth (no trivia) |
| RL SB14.2 | Classical conditioning; blocking; higher-order conditioning | psychology/neuroscience context (S&B ch.14-15, optional Block 17 of the RL scope); no robot or navigation Note needs it; beginner depth (no trivia) |
| RL SB14.3 | Rescorla–Wagner model | psychology/neuroscience context (S&B ch.14-15, optional Block 17 of the RL scope); no robot or navigation Note needs it; beginner depth (no trivia) |
| RL SB14.4 | TD model of classical conditioning | psychology/neuroscience context (S&B ch.14-15, optional Block 17 of the RL scope); no robot or navigation Note needs it; beginner depth (no trivia) |
| RL SB14.5 | Instrumental conditioning and the law of effect | psychology/neuroscience context (S&B ch.14-15, optional Block 17 of the RL scope); no robot or navigation Note needs it; beginner depth (no trivia) |
| RL SB15.1 | Reward signals vs reinforcement signals | psychology/neuroscience context (S&B ch.14-15, optional Block 17 of the RL scope); no robot or navigation Note needs it; beginner depth (no trivia) |
| RL SB15.2 | Reward prediction error hypothesis and dopamine | psychology/neuroscience context (S&B ch.14-15, optional Block 17 of the RL scope); no robot or navigation Note needs it; beginner depth (no trivia) |
| RL SB15.3 | TD error / dopamine correspondence | psychology/neuroscience context (S&B ch.14-15, optional Block 17 of the RL scope); no robot or navigation Note needs it; beginner depth (no trivia) |
| RL SB15.4 | Neural actor–critic | psychology/neuroscience context (S&B ch.14-15, optional Block 17 of the RL scope); no robot or navigation Note needs it; beginner depth (no trivia) |
| RL SB15.5 | Hedonistic neurons, collective RL, model-based methods in the brain, addiction | psychology/neuroscience context (S&B ch.14-15, optional Block 17 of the RL scope); no robot or navigation Note needs it; beginner depth (no trivia) |

## 7. Open questions for the owner

1. **Size.** 188 Notes is more than ML (128). Keep one RO Subject, or split it into two (classical robotics and RL)?
2. **Humanoids** get 3 Notes (148–150), legged robots 5 and manipulation 7. Is that the "equal weight" wanted?
3. **New maths placement.** The new MA Notes go just before their first user in the Course order. Some fill gaps in existing MA chapters, such as Markov chains next to MA-019, so the MA chapters will grow.

