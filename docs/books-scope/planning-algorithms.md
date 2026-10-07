# Scope: *Planning Algorithms* (LaValle, 2006)

> **Plan of record:** the RO chapters and Notes are in [robotics.md](robotics.md), which merges this doc with the other two book scopes. This doc stays as the evidence: its rows, sources and checks. Where its own plan (Note counts, blocks, order) differs, robotics.md wins.

**Summary.** Source: the author's free official copy at <https://lavalle.pl/planning/> (home page chapter list, plus the section and sub-section list of the HTML edition, `book.html` and its `nodeNNN.html` pages). The book has 15 chapters in 4 parts: discrete search, motion planning in continuous space, planning under uncertainty, and planning with motion limits (cars, dynamics, control). This scope lists **149 concepts**: **8 covered**, **24 partial**, **117 new**. Of these, 84 are maths and 65 are robotics/planning. Our Notes cover the probability, linear-algebra and optimisation basics the book leans on. Almost everything about robots, search, topology, games, filters, motion and control is new.

Status key:
- **covered**: we already have it (Note folder or glossary term named).
- **partial**: we have the basics; the column says what the book adds.
- **new**: not in our Notes.

---

## Chapter-by-chapter table

### Part I: Introductory material

| Chapter | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|
| 1 Introduction | State, action, state transition (the basic parts of a planning problem) | robotics | partial | Note 03 names agent and policy. New: a formal state space, an action set, and a rule that gives the next state. |
| 1 Introduction | Feasible plan vs optimal plan | robotics | partial | "Feasible region" in Maths Note 620/622. New: "any plan that reaches the goal" vs "the cheapest one". |
| 1 Introduction | Open-loop plan vs feedback plan | robotics | new | A fixed list of actions vs a rule that picks an action from the current state. |
| 2 Discrete Planning | Graph (nodes and edges) as a model of a state space | maths | new | No graph-theory Note yet. |
| 2 Discrete Planning | Breadth-first and depth-first search | robotics | new | Visit states level by level, or go deep first. |
| 2 Discrete Planning | Priority queue | maths | new | A list that always hands out the smallest item first; core of Dijkstra and A*. |
| 2 Discrete Planning | Dijkstra's algorithm (shortest path) | robotics | new | Cheapest path in a graph with costs. |
| 2 Discrete Planning | A* search and heuristics | robotics | new | Dijkstra plus a guess of the remaining cost; needs an "admissible" (never too high) guess. |
| 2 Discrete Planning | Best-first search and iterative deepening | robotics | new | "Greedy search" in Note 97 is a different idea (tree splits). |
| 2 Discrete Planning | Backward and bidirectional search | robotics | new | Search from the goal, or from both ends. |
| 2 Discrete Planning | Cost-to-go and value iteration (dynamic programming) | maths | partial | Dynamic programming / memoization in DL Note 1019. New: the cost-to-go function and the Bellman-style update over states. |
| 2 Discrete Planning | Algorithm cost (Big-O, exponential time) | maths | partial | "Exponential time" in DL Note 1019; O(n) used loosely. New: formal Big-O. |
| 2 Discrete Planning | Propositional logic (true/false statements, AND/OR/NOT) | maths | partial | AND, OR, XOR in DL Note 1007. New: predicates, literals, logical formulas. |
| 2 Discrete Planning | STRIPS representation (planning with logic statements) | robotics | new | |
| 2 Discrete Planning | Plan-space search and planning graphs | robotics | new | |
| 2 Discrete Planning | Planning as satisfiability (SAT) | maths | new | Turn a planning problem into "can these logic statements all be true?". |

### Part II: Motion planning

| Chapter | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|
| 3 Geometric Representations | Shapes from half-planes (convex polygons and polyhedra) | maths | partial | Hyperplane sides in Maths Note 363, convex sets in Maths Note 621. New: build any polygon from them. |
| 3 Geometric Representations | Semi-algebraic models (shapes from polynomial inequalities) | maths | new | |
| 3 Geometric Representations | Triangle meshes and bitmaps (occupancy grids) | robotics | new | |
| 3 Geometric Representations | 2D rotation matrix | maths | covered | Maths Note 500 (glossary: Rotation matrix). |
| 3 Geometric Representations | Chaining transforms by matrix multiplication | maths | covered | Maths Note 510 (composition). |
| 3 Geometric Representations | Scaling and shear (non-rigid transforms) | maths | covered | Maths Note 500 (glossary: Shear, Scaling). |
| 3 Geometric Representations | Rigid-body transform (rotate + translate, keeps distances) | maths | partial | Affine transformation in Maths Note 500. New: the rigid-body rule and its use for moving robots. |
| 3 Geometric Representations | Homogeneous transformation matrix | maths | new | Put rotation and translation in one bigger matrix by adding a 1 to each point. |
| 3 Geometric Representations | 3D rotations: yaw, pitch, roll, and reading them back from a matrix | maths | new | Needs atan2 and trigonometry. |
| 3 Geometric Representations | Kinematic chains and forward kinematics | robotics | new | Linked arm parts; find where the hand is from the joint angles. |
| 3 Geometric Representations | Denavit-Hartenberg parameters | robotics | new | A standard 4-number recipe per joint. |
| 3 Geometric Representations | Kinematic trees | robotics | new | Bodies that branch (like a humanoid). |
| 4 Configuration Space | Topological space, open and closed sets | maths | new | |
| 4 Configuration Space | Continuous function and homeomorphism | maths | new | "Same shape up to stretching" (donut = coffee cup). |
| 4 Configuration Space | Manifold | maths | new | A space that looks flat when you zoom in. |
| 4 Configuration Space | Cartesian product of spaces and identification (circle, torus, Möbius strip) | maths | new | Make new spaces by pairing old ones or gluing edges. |
| 4 Configuration Space | Paths, connectedness, simply connected | maths | new | |
| 4 Configuration Space | Groups (basic group theory) | maths | new | A set with an operation that can be undone, like rotations. |
| 4 Configuration Space | Fundamental group | maths | new | Counts the kinds of loops in a space. |
| 4 Configuration Space | Configuration space (C-space) and degrees of freedom | robotics | new | Every possible pose of the robot as one point. |
| 4 Configuration Space | Rotations as complex numbers (SO(2)) | maths | partial | Complex numbers appear only briefly in Maths Note 530. New: a unit complex number as a 2D rotation. |
| 4 Configuration Space | Quaternions and the projective space RP³ | maths | new | Four numbers that describe a 3D rotation. |
| 4 Configuration Space | Special Euclidean groups SE(2), SE(3) | maths | new | All rigid-body poses in 2D or 3D. |
| 4 Configuration Space | Obstacle region and free space in C-space | robotics | new | |
| 4 Configuration Space | Minkowski sum (growing obstacles by the robot's shape) | maths | new | "Minkowski distance" in Note 91 is a different idea. |
| 4 Configuration Space | Basic motion planning problem (piano mover's problem) | robotics | new | |
| 4 Configuration Space | Closed kinematic chains and algebraic varieties | maths | new | Solution sets of polynomial equations (loops in a linkage). |
| 5 Sampling-Based Planning | Metric space (rules a distance must follow) | maths | partial | Distances in Maths Note 361 and Note 91. New: the axioms, and distances on circles and rotations. |
| 5 Sampling-Based Planning | Measure (a general idea of length, area, volume) | maths | new | Includes the "right" volume for rotations (Haar measure). |
| 5 Sampling-Based Planning | Uniform random samples of rotations and directions | maths | partial | Uniform distribution in Maths Note 261. New: sampling evenly on a circle, sphere, or rotation group. |
| 5 Sampling-Based Planning | Pseudorandom numbers and testing randomness | maths | partial | Pseudorandom and random seed in Maths Note 261 and Note 38. New: how they are made and tested. |
| 5 Sampling-Based Planning | Dispersion, grids and lattices | maths | new | How big the largest empty gap between samples is. |
| 5 Sampling-Based Planning | Discrepancy and low-discrepancy sequences (van der Corput, Halton, Hammersley) | maths | new | Samples spread more evenly than random ones. |
| 5 Sampling-Based Planning | Collision detection (distance between sets, broad and narrow phase) | robotics | new | |
| 5 Sampling-Based Planning | Bounding-volume hierarchies | robotics | new | Wrap parts in simple boxes or spheres to rule out collisions fast. |
| 5 Sampling-Based Planning | Nearest-neighbour search with kd-trees | robotics | partial | kd-tree and ball tree named in Note 91. New: on C-space with wrap-around angles, and approximate search. |
| 5 Sampling-Based Planning | Gradient of a potential function | maths | covered | Gradient in Maths Note 601. |
| 5 Sampling-Based Planning | Randomized potential fields | robotics | new | Roll downhill to the goal, take random walks to escape local minima. |
| 5 Sampling-Based Planning | Rapidly-exploring random trees (RRT) | robotics | new | |
| 5 Sampling-Based Planning | Probabilistic roadmaps (PRM) and visibility roadmaps | robotics | new | |
| 5 Sampling-Based Planning | Completeness: complete, resolution complete, probabilistically complete | robotics | new | What it means for a planner to always find a path when one exists. |
| 6 Combinatorial Planning | Vertical cell decomposition | robotics | new | Cut free space into simple pieces, then search the pieces. |
| 6 Combinatorial Planning | Maximum-clearance roadmap (generalized Voronoi diagram) | robotics | new | Paths that stay as far from obstacles as possible. |
| 6 Combinatorial Planning | Shortest-path roadmap (visibility graph) | robotics | new | |
| 6 Combinatorial Planning | Cell complexes | maths | new | |
| 6 Combinatorial Planning | Tarski sentences and quantifier elimination | maths | new | |
| 6 Combinatorial Planning | Cylindrical algebraic decomposition | maths | new | |
| 6 Combinatorial Planning | Canny's roadmap algorithm | robotics | new | |
| 6 Combinatorial Planning | Complexity classes (NP-hard, PSPACE-hard) and lower bounds | maths | new | |
| 6 Combinatorial Planning | Davenport-Schinzel sequences | maths | new | |
| 7 Extensions | Time-varying problems and velocity tuning | robotics | new | Moving obstacles; fix the path, then choose the speed. |
| 7 Extensions | Multiple robots: centralized vs decoupled (prioritized) planning | robotics | new | |
| 7 Extensions | Hybrid systems (discrete modes + continuous motion) | robotics | new | |
| 7 Extensions | Manipulation planning (transit and transfer moves) | robotics | new | |
| 7 Extensions | Closed-chain planning (active-passive links, random loop generator) | robotics | new | |
| 7 Extensions | Folding problems (protein folding, unknotting) | robotics | new | |
| 7 Extensions | Coverage planning | robotics | new | Visit every part of an area (like a vacuum robot). |
| 7 Extensions | Pareto-optimal plans | maths | new | "Pareto distribution" in Maths Note 262 is a different idea. A plan nobody can improve without making another worse. |
| 8 Feedback Planning | Feedback plan as a policy | robotics | partial | Policy in Note 03. New: a policy defined over a whole state space. |
| 8 Feedback Planning | Navigation functions and grid wavefront propagation | robotics | new | A cost map with one minimum at the goal; follow it downhill. |
| 8 Feedback Planning | Ordinary differential equations (ODEs) | maths | new | An equation linking a quantity to how fast it changes. |
| 8 Feedback Planning | Vector fields and integral curves | maths | new | An arrow at every point, and the path you get by following the arrows. |
| 8 Feedback Planning | Smooth manifolds and tangent spaces | maths | new | |
| 8 Feedback Planning | Composition of funnels | robotics | new | Chain simple controllers so each one hands off to the next. |
| 8 Feedback Planning | Dynamic programming with interpolation on continuous spaces | robotics | partial | Linear interpolation (glossary). New: value iteration on a grid with in-between values. |

### Part III: Decision-theoretic planning

| Chapter | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|
| 9 Basic Decision Theory | Optimisation review (single and multi-objective) | maths | partial | Maths Notes 620–622, Note 57. New: many objectives at once. |
| 9 Basic Decision Theory | Probability space, conditional probability, marginalising | maths | covered | Maths Notes 330, 331, 341. |
| 9 Basic Decision Theory | Random variables and expectation | maths | covered | Maths Notes 240, 332. |
| 9 Basic Decision Theory | Game against nature: worst-case vs expected-cost decisions | maths | new | Nature picks an outcome; plan for the worst one, or for the average. |
| 9 Basic Decision Theory | Bayesian decision making with observations | maths | partial | Bayes' theorem (Maths Note 85), Naive Bayes (Notes 87–90). New: choose the action with least expected loss. |
| 9 Basic Decision Theory | Zero-sum games, minimax and saddle points | maths | partial | Saddle point (Note 57), minimax inequality (Maths Note 620). New: game matrices and security strategies. |
| 9 Basic Decision Theory | Mixed (randomized) strategies, solved with linear programming | maths | partial | Linear programming in Maths Note 622. New: pick actions at random with set chances. |
| 9 Basic Decision Theory | Nonzero-sum games and Nash equilibrium | maths | new | |
| 9 Basic Decision Theory | Utility theory and rationality | maths | new | |
| 10 Sequential Decision Theory | Markov decision process (MDP) | maths | new | Next state depends only on the current state and action. |
| 10 Sequential Decision Theory | Forward projections and backprojections | robotics | new | Where can I end up / where could I have come from. |
| 10 Sequential Decision Theory | Value iteration and the Bellman equation (with nature) | maths | new | Builds on Chapter 2 cost-to-go. |
| 10 Sequential Decision Theory | Policy iteration | maths | new | |
| 10 Sequential Decision Theory | Infinite horizon: discounted cost and average cost | maths | new | |
| 10 Sequential Decision Theory | Reinforcement learning: evaluating a plan by simulation (Monte Carlo, temporal difference) | robotics | partial | RL overview in Note 03. New: the actual algorithms. |
| 10 Sequential Decision Theory | Q-learning | robotics | new | |
| 10 Sequential Decision Theory | Game trees and alpha-beta pruning | robotics | new | |
| 10 Sequential Decision Theory | Sequential games on state spaces | maths | new | |
| 11 Sensors and Information Spaces | Sensor models (landmark, range/depth, odometry, boundary) | robotics | new | |
| 11 Sensors and Information Spaces | Information space and information state (history of actions and readings) | robotics | new | Plan on what you know, not on the true state. |
| 11 Sensors and Information Spaces | Nondeterministic information state (set of possible states) | robotics | new | |
| 11 Sensors and Information Spaces | Probabilistic information state (belief) and the Bayes filter | maths | partial | Bayes' theorem in Maths Note 85. New: update the belief step after step over time. |
| 11 Sensors and Information Spaces | Nondeterministic finite automata | maths | new | |
| 11 Sensors and Information Spaces | POMDP (MDP where the state is hidden) | maths | new | |
| 11 Sensors and Information Spaces | Multivariate Gaussian | maths | partial | Normal distribution (Maths Note 250), covariance matrix (Maths Note 231). New: the full many-variable bell curve. GMM Note 640 is still in progress. |
| 11 Sensors and Information Spaces | Kalman filter | maths | new | Best guess of a moving state from noisy readings, for linear systems with Gaussian noise. |
| 11 Sensors and Information Spaces | Monte Carlo methods and importance sampling | maths | new | Estimate things by drawing many random samples. |
| 11 Sensors and Information Spaces | Particle filter | robotics | new | Belief as a cloud of weighted samples. |
| 12 Planning Under Sensing Uncertainty | Planning in belief / information space | robotics | new | |
| 12 Planning Under Sensing Uncertainty | Robot localization (discrete, geometric, Monte Carlo) | robotics | new | Work out where the robot is. |
| 12 Planning Under Sensing Uncertainty | Mapping and SLAM (build a map while finding yourself in it) | robotics | new | |
| 12 Planning Under Sensing Uncertainty | D* (fast replanning when the map changes) | robotics | new | |
| 12 Planning Under Sensing Uncertainty | Bug algorithms and navigating unknown spaces | robotics | new | |
| 12 Planning Under Sensing Uncertainty | Visibility-based pursuit-evasion | robotics | new | |
| 12 Planning Under Sensing Uncertainty | Preimage planning and nonprehensile manipulation | robotics | new | Plans that work despite position error; pushing instead of grasping. |

### Part IV: Planning under differential constraints

| Chapter | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|
| 13 Differential Models | Velocity constraints: holonomic vs nonholonomic | robotics | new | E.g. a car cannot slide sideways. |
| 13 Differential Models | Jacobian / partial derivatives for velocity relations | maths | covered | Maths Notes 601, 602. |
| 13 Differential Models | Wheeled robot models: simple car, Dubins car, Reeds-Shepp car, differential drive, trailers | robotics | new | |
| 13 Differential Models | Phase (state) space: turn a higher-order ODE into first-order ones | maths | new | Add velocity to the state. |
| 13 Differential Models | Linear systems ẋ = Ax + Bu | maths | partial | Matrices in Maths Note 500. New: matrices that describe change over time. |
| 13 Differential Models | Nonlinear systems and adding integrators | maths | new | |
| 13 Differential Models | Newtonian mechanics (force, mass, F = ma, particles) | maths | new | Basic physics. |
| 13 Differential Models | Rigid-body dynamics (angular velocity, inertia matrix, torque) | maths | new | |
| 13 Differential Models | Calculus of variations | maths | new | Find the best whole function (path), not just the best number. |
| 13 Differential Models | Lagrangian mechanics and the Euler-Lagrange equation | maths | new | Same word "Lagrangian" as Maths Note 620, but a different idea (kinetic minus potential energy). |
| 13 Differential Models | Hamiltonian mechanics | maths | new | |
| 13 Differential Models | Differential games | maths | new | |
| 14 Sampling-Based Under Constraints | Kinodynamic planning and phase-space obstacles | robotics | new | |
| 14 Sampling-Based Under Constraints | Reachable sets | robotics | new | |
| 14 Sampling-Based Under Constraints | Numerical integration of ODEs (Euler, Runge-Kutta) | maths | new | |
| 14 Sampling-Based Under Constraints | Motion primitives, system simulator, local planning | robotics | new | |
| 14 Sampling-Based Under Constraints | Lattice search and the Barraquand-Latombe planner | robotics | new | |
| 14 Sampling-Based Under Constraints | RRT under motion limits (kinodynamic RRT) | robotics | new | Needs RRT from Chapter 5. |
| 14 Sampling-Based Under Constraints | Feedback planning with dynamic programming and interpolation | robotics | new | |
| 14 Sampling-Based Under Constraints | Decoupled planning: plan-and-transform, path-constrained timing | robotics | new | |
| 14 Sampling-Based Under Constraints | Gradient-based trajectory optimization | maths | partial | Gradient descent in Note 57. New: optimise a whole path at once (shooting methods). |
| 15 System Theory | Taylor linearisation of a system around a point | maths | covered | Maths Note 603 (and Linearisation in Maths Note 600). |
| 15 System Theory | Eigenvalues to judge stability of linear systems | maths | partial | Eigenvalues in Maths Note 530. New: negative real parts mean the system settles. |
| 15 System Theory | Equilibrium points, Lyapunov and asymptotic stability, limit cycles | maths | new | |
| 15 System Theory | Lyapunov functions | maths | new | An "energy" that always goes down proves stability. |
| 15 System Theory | Controllability and small-time local controllability (STLC) | maths | new | |
| 15 System Theory | Hamilton-Jacobi-Bellman (HJB) equation | maths | new | Value iteration in continuous time. |
| 15 System Theory | Linear-quadratic regulator (LQR) and the Riccati equation | maths | new | |
| 15 System Theory | Pontryagin's minimum principle | maths | new | Uses multipliers much like Maths Note 620, but along a whole path. |
| 15 System Theory | Dubins, Reeds-Shepp and Balkcom-Mason curves (shortest car paths) | robotics | new | |
| 15 System Theory | Control-affine systems and distributions | maths | new | |
| 15 System Theory | Lie brackets, Lie algebra, Frobenius and Chow-Rashevskii theorems | maths | new | Tell whether wiggling the controls can reach any nearby state. |
| 15 System Theory | Steering methods (P. Hall basis, sinusoids, piecewise-constant inputs) | robotics | new | |

---

## Suggested learning order for the new concepts

Each block needs the blocks above it. Within a block, go top to bottom.

**Block A: Graphs and search (needs nothing new).**
Graph → breadth-first and depth-first search → priority queue → Dijkstra → A* and heuristics → best-first, iterative deepening, backward and bidirectional search → Big-O and complexity classes.

**Block B: Logic-based planning (needs A).**
Propositional logic → STRIPS → plan-space search and planning graphs → planning as SAT.

**Block C: Robot geometry (needs Maths Notes 500, 510).**
Shapes from half-planes and semi-algebraic models → rigid-body transform → homogeneous matrix → yaw, pitch, roll → kinematic chains and forward kinematics → Denavit-Hartenberg → kinematic trees.

**Block D: Shape of spaces (needs C).**
Topological space → continuous maps and homeomorphism → Cartesian products and gluing (circle, torus) → paths and connectedness → groups → fundamental group → manifolds → complex numbers as rotations → quaternions → SE(2), SE(3).

**Block E: Configuration space (needs C, D).**
C-space and degrees of freedom → obstacle region and free space → Minkowski sum → basic motion planning problem → closed chains and algebraic varieties.

**Block F: Sampling-based planning (needs A, E).**
Metric space → measure → uniform samples of rotations → pseudorandom numbers → dispersion and grids → low-discrepancy sequences → collision detection and bounding volumes → kd-tree search on C-space → randomized potential fields → RRT → PRM → completeness ideas.

**Block G: Exact (combinatorial) planning (needs E, F; optional, heavy).**
Vertical cell decomposition → visibility graph → generalized Voronoi roadmap → cell complexes → Tarski sentences → cylindrical algebraic decomposition → Canny's algorithm → Davenport-Schinzel sequences.

**Block H: Extensions (needs F).**
Time-varying problems → multiple robots → hybrid systems → manipulation planning → closed-chain planning → coverage planning → Pareto-optimal plans → folding problems.

**Block I: Feedback and continuous change (needs F, Maths Note 601).**
ODEs → vector fields and integral curves → smooth manifolds and tangent spaces → navigation functions and wavefronts → composition of funnels.

**Block J: Decisions and games (needs Maths Notes 85, 332, 622).**
Game against nature → utility theory → zero-sum games and mixed strategies → Nash equilibrium.

**Block K: Sequential decisions and RL (needs A, J).**
MDP → forward projections and backprojections → value iteration and Bellman equation → policy iteration → discounted and average cost → Monte Carlo methods → RL evaluation (Monte Carlo, temporal difference) → Q-learning → game trees and alpha-beta → sequential games.

**Block L: Sensing and estimation (needs K, Maths Notes 231, 250).**
Sensor models → information states (history, set of possible states) → nondeterministic finite automata → belief and Bayes filter → POMDP → multivariate Gaussian → Kalman filter → importance sampling → particle filter.

**Block M: Planning with uncertainty (needs L, F).**
Belief-space planning → localization → mapping and SLAM → D* → bug algorithms → pursuit-evasion → preimage planning and nonprehensile manipulation.

**Block N: Motion with physics (needs I, Maths Notes 530, 603).**
Holonomic vs nonholonomic → wheeled models (car, Dubins, Reeds-Shepp, differential drive) → phase space → linear systems ẋ = Ax + Bu → nonlinear systems → Newtonian mechanics → rigid-body dynamics → calculus of variations → Euler-Lagrange → Hamiltonian mechanics.

**Block O: Planning under motion limits (needs F, N).**
Numerical integration (Euler, Runge-Kutta) → reachable sets → motion primitives and simulators → kinodynamic planning → lattice search → kinodynamic RRT → feedback planning with interpolation → decoupled planning → trajectory optimization.

**Block P: Control theory (needs N, O, K).**
Equilibrium and stability → Lyapunov functions → controllability and STLC → HJB equation → LQR and Riccati → Pontryagin's principle → Dubins and Reeds-Shepp curves → control-affine systems → Lie brackets and Chow-Rashevskii → steering methods → differential games.
