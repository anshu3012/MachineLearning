# Scope: *Probabilistic Robotics* (Thrun, Burgard, Fox, MIT Press 2005)

> **Plan of record:** the RO chapters and Notes are in [robotics.md](robotics.md), which merges this doc with seven other scope docs. This doc is evidence: its rows, sources and checks. Where its own plan (Note counts, blocks, order) differs, robotics.md wins.

**Summary.** This is a scoping list only, not study Notes. The section-level table of contents comes from the book's own
contents pages, as scanned and hosted by the German library network GBV
([481815236.PDF](http://www.gbv.de/dms/ilmenau/toc/481815236.PDF), linked from the
[UTB library catalogue record](https://vufind.katalog.k.utb.cz/Record/34143/Details)). The authors' official book page
([robots.stanford.edu/probabilistic-robotics](https://robots.stanford.edu/probabilistic-robotics/)) confirms the book's aim
and offers the authors' slides and figures. probabilistic-robotics.org and the MIT Press page did not load. No book PDF was used.
The book has 17 chapters in four parts (Basics, Localization, Mapping, Planning and Control). We list
**132 concepts**: **12 covered**, **24 partial** and **96 new**
(maths: 73, robotics: 59). Almost all the robotics is new; most of the new maths is about
*tracking a changing quantity over time* (filters), *sampling*, and *planning under uncertainty*.

Status key:
- **covered**: we already have it; the Note folder is named.
- **partial**: we have the basics, but the book goes further; the new part is named.
- **new**: not in our Notes.

Notes marked "(in progress)" are 630–633 (MLE) and 640–641 (GMM, EM).

## 1. Chapter-by-chapter table

### Part I: Basics

| Chapter | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|
| 1 Introduction | Sources of uncertainty in robots (world, sensors, motors, models, rounding) | robotics | new | Why a robot can never be sure where it is or what it sees |
| 1 Introduction | Probabilistic robotics: keep a full distribution, not one best guess | robotics | new | The core idea of the whole book |
| 2 Recursive State Estimation | Random variables, PMF and PDF | maths | covered | 240, 241, 242 |
| 2 Recursive State Estimation | Joint, marginal and conditional probability | maths | covered | 341, 82 |
| 2 Recursive State Estimation | Independence and conditional independence | maths | covered | 83, 88 |
| 2 Recursive State Estimation | Law of total probability | maths | covered | 86 |
| 2 Recursive State Estimation | Bayes' theorem, prior, posterior | maths | covered | 85, 86 |
| 2 Recursive State Estimation | Normalising constant (Bayes without the evidence term) | maths | covered | 88 |
| 2 Recursive State Estimation | Bayes' theorem conditioned on extra known facts | maths | partial | 85 has plain Bayes; new: every term also conditioned on past data, which the filter relies on |
| 2 Recursive State Estimation | Expected value, variance, covariance | maths | covered | 332, 231 |
| 2 Recursive State Estimation | Entropy of a distribution | maths | covered | 97 (entropy, differential entropy) |
| 2 Recursive State Estimation | Normal distribution (one variable) | maths | covered | 250 |
| 2 Recursive State Estimation | Multivariate normal distribution | maths | partial | 250 is one variable, 48 and 231 have the covariance matrix; new: the many-variable density formula and its ellipse-shaped contours |
| 2 Recursive State Estimation | State: pose, map, speeds; complete state | robotics | new | What the robot needs to know about itself and the world |
| 2 Recursive State Estimation | Measurements and controls (what the robot senses and does) | robotics | new | The two kinds of data a robot gets each step |
| 2 Recursive State Estimation | State transition probability and measurement probability | robotics | new | The "motion model" and "sensor model" used in every later chapter |
| 2 Recursive State Estimation | Hidden Markov model / dynamic Bayes network | maths | new | A chain of hidden states, each giving one visible measurement |
| 2 Recursive State Estimation | Markov assumption | maths | new | The future depends only on the present state, not the full past |
| 2 Recursive State Estimation | Belief and predicted belief | robotics | new | The robot's distribution over states, before and after a measurement |
| 2 Recursive State Estimation | Bayes filter (predict step, update step) | maths | new | Bayes' theorem applied again and again over time; parent of every filter in the book |
| 3 Gaussian Filters | Linear Gaussian system | maths | new | Next state = matrix x state + Gaussian noise |
| 3 Gaussian Filters | Passing a Gaussian through a matrix (mean A mu, covariance A Sigma A^T) | maths | partial | 231 covariance, 500 linear maps; new: how the covariance changes under the map |
| 3 Gaussian Filters | Product of two Gaussians / completing the square | maths | new | Combining two bell curves gives a narrower bell curve |
| 3 Gaussian Filters | Matrix inverse | maths | covered | 54 |
| 3 Gaussian Filters | Matrix inversion lemma (Woodbury identity) | maths | new | A shortcut for the inverse of "matrix + low-rank change" |
| 3 Gaussian Filters | Kalman filter and the Kalman gain | maths | new | The exact Bayes filter for linear Gaussian systems |
| 3 Gaussian Filters | Linearisation by first-order Taylor expansion | maths | partial | 600, 603 Taylor, 602 Jacobian; new: using it to push a Gaussian through a curved function |
| 3 Gaussian Filters | Extended Kalman filter (EKF) | maths | new | Kalman filter on a linearised model |
| 3 Gaussian Filters | Mixture-of-Gaussians belief (multi-hypothesis, 3.3.5) | maths | partial | 640 GMM (in progress); new: a mixture used as a moving belief |
| 3 Gaussian Filters | Matrix square root (Cholesky factor) | maths | partial | 64 names the Cholesky solver; new: the factor itself, needed for sigma points |
| 3 Gaussian Filters | Unscented transform and sigma points | maths | new | Push a few chosen points through the function instead of using a Jacobian |
| 3 Gaussian Filters | Unscented Kalman filter (UKF) | maths | new | Kalman filter built on the unscented transform |
| 3 Gaussian Filters | Canonical form: information matrix (inverse covariance) and information vector | maths | new | A second way to write a Gaussian |
| 3 Gaussian Filters | Information filter and extended information filter | maths | new | The Kalman filter written in canonical form |
| 4 Nonparametric Filters | Histogram | maths | covered | 20 |
| 4 Nonparametric Filters | Histogram filter / discrete Bayes filter | maths | new | Bayes filter over a grid of cells |
| 4 Nonparametric Filters | Splitting a continuous space into cells (static and dynamic decomposition, density trees) | maths | partial | 32 binning; new: cells that adapt to where the probability is |
| 4 Nonparametric Filters | Log-odds | maths | covered | 122 |
| 4 Nonparametric Filters | Binary Bayes filter in log-odds form | maths | partial | 122 log-odds; new: updating a yes/no belief by adding log-odds |
| 4 Nonparametric Filters | Monte Carlo approximation (a set of samples stands for a distribution) | maths | new | Represent any shape of distribution by random samples |
| 4 Nonparametric Filters | Importance sampling (target, proposal, weights) | maths | new | Sample from an easy distribution, weight to fix the difference |
| 4 Nonparametric Filters | Resampling, low-variance sampler | maths | partial | 105, 108 bootstrap sampling; new: resampling by weight inside a filter, the low-variance method |
| 4 Nonparametric Filters | Particle filter | maths | new | Bayes filter run on weighted samples |
| 4 Nonparametric Filters | Particle deprivation and sample variance | maths | new | Why a particle filter can lose the true state |

### Part I (continued): motion and sensing

| Chapter | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|
| 5 Robot Motion | Pose (x, y, heading) and kinematic configuration | robotics | new | Position plus direction of a robot on a plane |
| 5 Robot Motion | 2D rotation and heading angles | maths | partial | 500 rotation matrix; new: sin/cos of heading, keeping angles in -pi..pi |
| 5 Robot Motion | Probabilistic kinematics p(x_t given u_t, x_t-1) | robotics | new | Motion with noise, as a distribution |
| 5 Robot Motion | Velocity motion model | robotics | new | Motion from forward and turning speed |
| 5 Robot Motion | Odometry motion model | robotics | new | Motion from wheel-count readings |
| 5 Robot Motion | Drawing random samples from a normal or triangular distribution | maths | partial | 250, 261, 271 (simulated samples); new: the sampling recipes and the triangular distribution |
| 5 Robot Motion | Sampling from a motion model | robotics | new | Generate possible next poses, used by particle filters |
| 5 Robot Motion | Motion and maps (ruling out poses inside walls) | robotics | new | Combining a motion model with a map |
| 6 Robot Perception | Maps: feature-based and location-based (grid) | robotics | new | Two ways to store the world |
| 6 Robot Perception | Beam model of range finders | robotics | new | One laser/sonar reading as a mix of four error types |
| 6 Robot Perception | Exponential distribution (for "too short" readings) | maths | new | Not in our Notes yet (632 may touch it, in progress) |
| 6 Robot Perception | Mixture density of four parts | maths | partial | 640 GMM (in progress); new: mixing different shapes, not only Gaussians |
| 6 Robot Perception | Learning sensor-model parameters by MLE / EM | maths | partial | 631 MLE, 641 EM (in progress); new: applied to sensor data |
| 6 Robot Perception | Likelihood field model | robotics | new | Score a reading by distance to the nearest obstacle |
| 6 Robot Perception | Correlation-based measurement model (map matching) | robotics | partial | 231 correlation; new: correlating a local scan with a map |
| 6 Robot Perception | Feature extraction and landmarks (range, bearing, signature) | robotics | new | Turning raw sensor data into a few landmark readings |
| 6 Robot Perception | Landmark sensor model with known correspondence | robotics | new | Probability of a landmark reading given the pose |
| 6 Robot Perception | Sampling poses from a landmark reading | robotics | new | Working backward from a reading to possible poses |

### Part II: Localization

| Chapter | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|
| 7 Localization: Markov and Gaussian | Kinds of localization: tracking, global, kidnapped robot; static/dynamic world; passive/active; one/many robots | robotics | new | The map of problem types |
| 7 Localization: Markov and Gaussian | Markov localization | robotics | new | The Bayes filter used to find the robot's pose on a known map |
| 7 Localization: Markov and Gaussian | EKF localization | robotics | new | Markov localization with an EKF |
| 7 Localization: Markov and Gaussian | Data association (correspondence) problem | robotics | new | Which landmark did I just see? |
| 7 Localization: Markov and Gaussian | Maximum-likelihood data association | maths | partial | 631 MLE (in progress); new: choosing the most likely match |
| 7 Localization: Markov and Gaussian | Mahalanobis distance and gating | maths | new | Distance that takes the covariance into account |
| 7 Localization: Markov and Gaussian | Multi-hypothesis tracking | robotics | new | Keep several Gaussians, one per possible match |
| 7 Localization: Markov and Gaussian | UKF localization | robotics | new | Localization with the UKF |
| 8 Localization: Grid and Monte Carlo | Grid localization | robotics | new | Histogram filter over poses |
| 8 Localization: Grid and Monte Carlo | Monte Carlo localization (MCL) | robotics | new | Particle filter over poses |
| 8 Localization: Grid and Monte Carlo | Random-particle / augmented MCL (recovery from failure) | robotics | new | Inject random particles to recover when lost |
| 8 Localization: Grid and Monte Carlo | Choosing a better proposal distribution | maths | new | Builds on importance sampling |
| 8 Localization: Grid and Monte Carlo | KL divergence | maths | partial | 1014 only names it; new: what it measures and how to compute it |
| 8 Localization: Grid and Monte Carlo | Chi-square distribution (used to bound KL) | maths | partial | 571 chi-square tests; new: using its quantile to set a sample size |
| 8 Localization: Grid and Monte Carlo | KLD-sampling (adaptive number of particles) | maths | new | Use fewer particles when the belief is focused |
| 8 Localization: Grid and Monte Carlo | Localization in changing environments (people, outlier readings) | robotics | new | Reject readings that the map cannot explain |

### Part III: Mapping

| Chapter | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|
| 9 Occupancy Grid Mapping | Occupancy grid map | robotics | new | A grid of cells, each with a probability of being blocked |
| 9 Occupancy Grid Mapping | Inverse sensor model and log-odds cell update | robotics | new | Uses the binary Bayes filter of Chapter 4 |
| 9 Occupancy Grid Mapping | Fusing several sensors in one map | robotics | new | Combining maps from different sensors |
| 9 Occupancy Grid Mapping | Learning the inverse sensor model from simulated data (with an error function) | maths | partial | Supervised learning, loss functions, neural nets (1014+); new: data made by simulating the forward model |
| 9 Occupancy Grid Mapping | Maximum a posteriori (MAP) estimation | maths | partial | 88 MAP rule; 633 MAP (in progress); new: MAP for a whole map |
| 9 Occupancy Grid Mapping | MAP occupancy mapping with forward models | robotics | new | Treat the map as one unknown and search for the best one |
| 10 SLAM | SLAM problem: online SLAM vs full SLAM | robotics | new | Build the map and find yourself in it at once |
| 10 SLAM | EKF SLAM with known correspondence | robotics | new | One big Gaussian over pose and all landmarks |
| 10 SLAM | Landmark initialization | robotics | new | Adding a newly seen landmark to the state |
| 10 SLAM | EKF SLAM with unknown correspondence (provisional landmarks) | robotics | new | Adds data association to EKF SLAM |
| 10 SLAM | Feature selection and map management | robotics | new | Which landmarks to keep or drop |
| 11 GraphSLAM | Pose graph (constraint graph) | robotics | new | Poses and landmarks as nodes, measurements as soft links |
| 11 GraphSLAM | Negative log posterior as a sum of quadratic terms | maths | partial | 631 negative log-likelihood, 350 quadratic form; new: the full posterior over path and map |
| 11 GraphSLAM | Nonlinear least squares with repeated linearisation | maths | partial | 51 least squares, 603 Taylor and Newton's method; new: re-linearise and re-solve in a loop (Gauss-Newton style) |
| 11 GraphSLAM | Information form of a large problem (Omega, xi) | maths | new | Builds on the canonical form of Chapter 3 |
| 11 GraphSLAM | Marginalising variables out of the information form (Schur complement) | maths | new | Removing landmarks to leave a smaller system |
| 11 GraphSLAM | Sparse matrices and sparse linear solves | maths | partial | 27 sparse matrix (storage only); new: solving large sparse systems fast |
| 11 GraphSLAM | Correspondence test in GraphSLAM | robotics | new | Deciding if two landmarks are the same one |
| 11 GraphSLAM | Other solvers: relaxation, conjugate gradient | maths | new | Iterative ways to solve big linear systems |
| 12 Sparse Extended Information Filter | SEIF SLAM | robotics | new | Online SLAM in information form |
| 12 Sparse Extended Information Filter | Sparsification of the information matrix | maths | new | Drop weak links to keep the matrix sparse |
| 12 Sparse Extended Information Filter | Amortized approximate map recovery | maths | new | Recover the mean a little at each step |
| 12 Sparse Extended Information Filter | Incremental data association | robotics | new | Matching as data arrives |
| 12 Sparse Extended Information Filter | Branch-and-bound search | maths | new | Search over many match choices with pruning |
| 12 Sparse Extended Information Filter | Equivalence constraints in data association | robotics | new | Saying "these two landmarks are one" |
| 12 Sparse Extended Information Filter | Multi-robot SLAM: map integration and alignment | robotics | new | Merging maps by finding a rotation and shift |
| 13 FastSLAM | Factoring the SLAM posterior (Rao-Blackwellization) | maths | new | Sample the path; given the path, landmarks are independent |
| 13 FastSLAM | FastSLAM 1.0 (particles with small per-landmark EKFs) | robotics | new | Combines particle filter and EKF |
| 13 FastSLAM | FastSLAM 2.0 (improved proposal) | robotics | new | Uses the latest measurement when sampling the pose |
| 13 FastSLAM | Per-particle data association | robotics | new | Each particle makes its own matches |
| 13 FastSLAM | Tree-based landmark storage (log-time updates) | maths | new | Balanced binary trees shared between particles |
| 13 FastSLAM | Loop closure | robotics | new | Recognising a place seen before |
| 13 FastSLAM | Grid-based FastSLAM | robotics | new | FastSLAM with an occupancy grid per particle |

### Part IV: Planning and Control

| Chapter | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|
| 14 Markov Decision Processes | Uncertainty in actions vs in perception | robotics | new | Four cases: sure/unsure motion x full/partial view |
| 14 Markov Decision Processes | Reinforcement learning, reward, policy | maths | partial | 03 (one-paragraph idea); new: formal definitions |
| 14 Markov Decision Processes | Markov decision process (states, actions, transition probabilities, payoff) | maths | new | The formal planning model |
| 14 Markov Decision Processes | Discount factor, horizon, cumulative payoff | maths | new | How future rewards are counted |
| 14 Markov Decision Processes | Value function and Bellman equation | maths | new | Value of a state = best reward now + value of what comes next |
| 14 Markov Decision Processes | Value iteration | maths | new | Repeat the Bellman update until values settle |
| 14 Markov Decision Processes | Value iteration for robot path planning on a grid | robotics | new | Planning a path that avoids risky areas |
| 15 POMDPs | Partially observable MDP and belief space | maths | new | Planning when you only have a belief, not the true state |
| 15 POMDPs | Piecewise-linear convex value function (alpha vectors) | maths | new | How a POMDP value function is stored |
| 15 POMDPs | Value iteration in belief space, finite-world POMDP algorithm | maths | new | Exact POMDP planning |
| 15 POMDPs | Pruning of value-function pieces | maths | new | Throw away pieces that are never best |
| 16 Approximate POMDPs | QMDP | maths | new | Pretend the state becomes known after one step |
| 16 Approximate POMDPs | Augmented MDP (belief summed up as mean + entropy) | robotics | new | Plan over a small summary of the belief |
| 16 Approximate POMDPs | Monte Carlo POMDP (beliefs as particle sets) | robotics | new | POMDP planning with particle filters |
| 17 Exploration | Information gain and entropy as a goal | maths | partial | 97 entropy, information gain (for tree splits); new: expected gain of a future action |
| 17 Exploration | Greedy and multi-step exploration | robotics | new | Go where you expect to learn most |
| 17 Exploration | Monte Carlo exploration | robotics | new | Estimate gain with sampled outcomes |
| 17 Exploration | Active localization | robotics | new | Move to become sure of your pose |
| 17 Exploration | Exploration for occupancy grids (cell entropy, gain spread by value iteration) | robotics | new | Choosing where to map next |
| 17 Exploration | Multi-robot exploration coordination | robotics | new | Sending several robots to different areas |
| 17 Exploration | Entropy decomposition in SLAM, exploration in FastSLAM | robotics | new | Balance learning the map and keeping the pose sure |

## 2. Prerequisites between the new concepts

Arrows mean "learn this first". Our existing Notes are in brackets.

- Bayes' theorem [85], conditional independence [88], total probability [86] -> **Markov assumption** -> **Bayes filter**.
- Normal [250] + covariance matrix [48, 231] -> **multivariate normal** -> **Gaussian through a matrix**, **product of Gaussians** -> **Kalman filter**.
- Kalman filter + Jacobian [602] + Taylor [603] -> **EKF** -> EKF localization -> **EKF SLAM**.
- Kalman filter + Cholesky factor -> **unscented transform** -> **UKF** -> UKF localization.
- Multivariate normal + matrix inverse [54] -> **canonical (information) form** -> **information filter** -> GraphSLAM -> SEIF.
- Bayes filter + histogram [20] -> **histogram filter** -> grid localization.
- Bayes filter + log-odds [122] -> **binary Bayes filter** -> **occupancy grid mapping**.
- Sampling from distributions -> **Monte Carlo approximation** -> **importance sampling** -> **resampling** -> **particle filter** -> MCL -> KLD-sampling, FastSLAM, MC-POMDP.
- Motion and sensor models -> every localization and SLAM algorithm.
- Multivariate normal -> **Mahalanobis distance** -> **ML data association** -> EKF SLAM with unknown correspondence.
- Negative log-likelihood [631] + least squares [51] + Newton [603] -> **nonlinear least squares** -> GraphSLAM. **Schur complement** -> GraphSLAM reduction.
- EKF SLAM + particle filter -> **Rao-Blackwellization** -> FastSLAM.
- Reinforcement learning idea [03] -> **MDP** -> **Bellman equation** -> **value iteration** -> **POMDP** -> QMDP, AMDP, MC-POMDP.
- Entropy and information gain [97] + belief -> **exploration**.

## 3. Suggested learning order for the new concepts

**Block A: maths bridge (after 641 EM).**
Multivariate normal; Gaussian through a matrix; product of Gaussians; Mahalanobis distance; exponential and triangular
distributions; drawing samples; KL divergence (full); Woodbury identity; Cholesky factor; Schur complement.

**Block B: the Bayes filter.**
Markov assumption; hidden Markov model / dynamic Bayes network; state, controls, measurements; belief;
Bayes filter (predict and update); Bayes' theorem with extra conditions.

**Block C: Gaussian filters.**
Linear Gaussian system; Kalman filter and gain; linearisation; EKF; unscented transform; UKF; canonical form;
information filter; mixture-of-Gaussians belief.

**Block D: sample-based and grid filters.**
Histogram filter; adaptive cells; binary Bayes filter in log-odds; Monte Carlo approximation; importance sampling;
resampling and low-variance sampler; particle filter; particle deprivation.

**Block E: robot models.**
Pose and heading angles; velocity and odometry motion models; sampling motion; maps (feature vs grid); beam model;
likelihood field; map matching; landmarks and the landmark sensor model.

**Block F: localization.**
Kinds of localization; Markov, grid, EKF, UKF localization; data association and multi-hypothesis tracking;
MCL; augmented MCL; better proposals; KLD-sampling; changing environments.

**Block G: mapping and SLAM.**
Occupancy grids and inverse sensor models; MAP mapping; SLAM (online vs full); EKF SLAM; nonlinear least squares;
pose graphs and GraphSLAM; sparse solvers and conjugate gradient; SEIF and sparsification; branch-and-bound
data association; Rao-Blackwellization; FastSLAM 1.0 and 2.0; loop closure; grid FastSLAM; multi-robot map merging.

**Block H: planning and exploration.**
MDP; discount and horizon; value function and Bellman equation; value iteration; path planning on a grid;
POMDP and belief space; alpha vectors and pruning; QMDP; augmented MDP; MC-POMDP; information-gain exploration;
active localization; grid and SLAM exploration; multi-robot exploration.

Blocks A to D are mostly maths and also serve other fields (tracking, time series, reinforcement learning).
Block H only needs Block B, so it could follow Block B directly if planning is the goal.
