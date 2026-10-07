# Verification of flagged `taught` verdicts

Rule: `taught` stands only if the cited Note's own title or Teaches text (plan §3/§4, or an MA/ML/DL Note body) covers the concept. `confirmed` quotes that phrase; "re-cite" means the concept is in a different Note than the one cited. `add` points to verify_adds.json.

Counts: ctrl_ledger add 10, ctrl_ledger confirmed 46, ctrl_ledger out-of-scope 1, robo_ledger add 16, robo_ledger confirmed 452, robo_ledger out-of-scope 5, vis_ledger add 8, vis_ledger confirmed 236. Total: confirmed 734, add 34, out-of-scope 6 (of which re-cited 17).

| ledger | term | old where | verdict | evidence / where |
|---|---|---|---|---|
| ctrl_ledger | anticipation, in controllers | Note 117 (derivative action as anticipation) | confirmed | N117: "act on error, its derivative and integral" (derivative action = anticipation, FBS 11-5) |
| ctrl_ledger | anti-windup compensation | Note 119 (integrator windup and anti-windup) | add | anti-windup: clamping the integrator or back-calculation when the actuator saturates [control] → RO-06, extend N119 |
| ctrl_ledger | architectures, for control systems | Note 126 (layered autonomy stack) | confirmed | N126: "the layers mission → behaviour → motion → control" |
| ctrl_ledger | automatic reset, in PID control | Note 119 (integral action = automatic reset) | confirmed | N117: "act on error, its derivative and integral" (automatic reset = integral action, FBS 11-4) |
| ctrl_ledger | balance systems | Note 296 (inverted-pendulum balance models) | add | cart-pole: inverted pendulum on a cart as a balance system (equations of motion, linearise at upright, stabilise by state feedback/LQR; also the classic RL benchmark) [control] → RO-15, worked example in N204/N205 |
| ctrl_ledger | block diagrams, PID controllers | Note 117 (PID block diagram) | add | transfer functions, poles and zeros, block-diagram algebra, pole/zero cancellation [control] → RO-06, new Note after N118 (merges existing ctrl_adds: Transfer functions (...)) |
| ctrl_ledger | block diagrams, two degree-of-freedom control | Note 119 (feedforward plus feedback = two degrees of freedom) | confirmed | N119: "Feedforward plus feedback" (= two-degree-of-freedom structure) |
| ctrl_ledger | cart-pendulum system | Note 296 (inverted pendulum); RL cart-pole benchmark | add | cart-pole: inverted pendulum on a cart as a balance system (equations of motion, linearise at upright, stabilise by state feedback/LQR; also the classic RL benchmark) [control] → RO-15, worked example in N204/N205 |
| ctrl_ledger | closed loop | Note 117 (closed-loop feedback vs open loop); Note 9 (open-loop vs feedback plans) | confirmed | N117: "PD / PID feedback control" (feedback control = closed loop) |
| ctrl_ledger | closed loop, versus open loop | Note 117 (closed-loop feedback vs open loop); Note 9 (open-loop vs feedback plans) | add | open-loop vs closed-loop (feedback) control: why feedback corrects disturbances and model error [control] → RO-06, extend N117 (PD and PID control) (merges existing robo_adds: open-loop vs closed-loop control) |
| ctrl_ledger | command signal | Note 117 (reference / command signal) | confirmed | N117: "act on error" (error = command/reference minus output) |
| ctrl_ledger | control, modeling for | plan §4 new maths: State-space models; Note 139 (models for control) | confirmed | plan §4 State-space models: "phase space, x_dot = Ax + Bu, nonlinear systems" |
| ctrl_ledger | Coriolis forces | Note 281 (manipulator equation: Coriolis terms) | add | centripetal and Coriolis terms of the manipulator equation [robotics] → RB-02, extend N281 (merges existing robo_adds: centripetal and Coriolis forces) |
| ctrl_ledger | cost function | Note 205 (quadratic cost) | confirmed | N205: "linear-quadratic regulator ...; Choosing the Q and R weights" |
| ctrl_ledger | covariance matrix | Note 80 (covariance matrix in the Kalman filter); MA-009 | confirmed | MA-009 (covariance and correlation): "a covariance matrix has the variances on its diagonal" |
| ctrl_ledger | cruise control, pole/zero cancellation | Note 252 (cruise control); FBS uses it as a running example | add | transfer functions, poles and zeros, block-diagram algebra, pole/zero cancellation [control] → RO-06, new Note after N118 (merges existing ctrl_adds: Transfer functions (...)) |
| ctrl_ledger | decision making, higher levels of | Note 126 (decision layers in the autonomy stack) | confirmed | N126: "the layers mission → behaviour → motion → control" |
| ctrl_ledger | differential equations, periodic solutions | Note 299 (limit cycles) | confirmed | N299: "limit cycles" (a limit cycle is an isolated periodic solution) |
| ctrl_ledger | differential equations, second-order | Note 118; plan §4 Second-order linear systems | confirmed | N118: "Error dynamics of a second-order system"; plan §4 "Second-order linear systems: mass-spring-damper" |
| ctrl_ledger | discrete-time systems, linear quadratic control for | Note 205 (discrete-time LQR) | confirmed | N205: "Discrete-time LQ problem solved by dynamic programming (Riccati recursion)" |
| ctrl_ledger | disturbances, random | Note 80 (random process disturbances in the Kalman filter) | confirmed | N80: "linear Gaussian system" (Gaussian process noise) |
| ctrl_ledger | dynamic inversion | Note 124 (feedback linearisation / dynamic inversion) | confirmed | N124: "Feedback linearisation" (FBS 6-34: also called dynamic inversion) |
| ctrl_ledger | dynamical systems, stochastic | Note 80 (stochastic linear system) | confirmed | N80: "linear Gaussian system" |
| ctrl_ledger | eigenvalue assignment | Note 204 (pole placement = eigenvalue assignment) | confirmed | N204: "pole placement" (= eigenvalue assignment) |
| ctrl_ledger | equilibrium points, for closed loop system | Note 204 (closed-loop equilibrium with state feedback) | confirmed | re-cite N206: "LQR for tracking a reference (error coordinates, steady-state target)" |
| ctrl_ledger | gain | Note 117 (controller gain) | confirmed | N117: "PD / PID feedback control" (controller gains); frequency-domain gain belongs to the ctrl_adds frequency-response Note |
| ctrl_ledger | Heaviside step function | Note 118 (step input) | confirmed | N118: "the step response" |
| ctrl_ledger | inverse model | Note 124 (inverting the model = feedback linearisation); Note 119 feedforward | confirmed | re-cite N284: "Computed torque (inverse dynamics control, feedback linearisation)"; N282 "inverse dynamics (torques for a wanted motion)" |
| ctrl_ledger | Jacobian linearization | plan §5 recap Taylor linearisation (MA-064); Note 206 | confirmed | N206: "Linearising a model around an operating point or a moving reference" |
| ctrl_ledger | linear quadratic control | Note 205 (LQR) | confirmed | N205: "linear-quadratic regulator and the Riccati equation" |
| ctrl_ledger | Lyapunov functions, design of controllers using | Note 124 (Kanayama controller proved stable with a Lyapunov function) | add | Lyapunov-based controller design: pick the control so a Lyapunov function decreases (control Lyapunov function) [control] → RO-06, extend N124 (after the planned Stability of dynamical systems Note) |
| ctrl_ledger | mechanical systems | plan §4 Newtonian and rigid-body mechanics; Note 281 | confirmed | plan §4 "Newtonian and rigid-body mechanics: F = ma, torque, inertia matrix"; N281 "Lagrangian mechanics" |
| ctrl_ledger | modeling | plan §4 State-space models; Note 139 | confirmed | plan §4 State-space models: "x_dot = Ax + Bu, nonlinear systems" |
| ctrl_ledger | modeling, from experiments | Note 139 (system identification) | confirmed | N139: "System identification" |
| ctrl_ledger | open loop | Note 9 (open-loop vs feedback plans) | add | open-loop vs closed-loop (feedback) control: why feedback corrects disturbances and model error [control] → RO-06, extend N117 (PD and PID control) (merges existing robo_adds: open-loop vs closed-loop control) |
| ctrl_ledger | optimal control | Note 205 (optimal control); Note 116 | confirmed | N205: "Hamilton-Jacobi-Bellman equation; linear-quadratic regulator"; N116 "Trajectory optimisation" |
| ctrl_ledger | PI control, first-order system | Note 117 (PI on a first-order plant) | confirmed | N117: "PD / PID feedback control" (PI is PID without D) |
| ctrl_ledger | prediction, in controllers | Note 117 (derivative action as prediction) | confirmed | N117: "act on error, its derivative" (derivative action = prediction, FBS 11-5) |
| ctrl_ledger | prediction time | Note 117 (derivative action as prediction) | add | PID ideal form with integral and derivative time constants (Td = prediction time) [control] → RO-06, extend N117 (merges existing ctrl_adds: PID tuning and implementation) |
| ctrl_ledger | reference signal | Note 117 (reference / setpoint) | confirmed | N117: "act on error" (error = reference minus output) |
| ctrl_ledger | reference signal, response to | Note 206 (tracking a reference) | confirmed | N206: "LQR for tracking a reference" |
| ctrl_ledger | reset, in PID control | Note 119 (reset = integral action) | confirmed | N117: "act on error, its derivative and integral" (reset = integral action) |
| ctrl_ledger | servo problem | Note 206 (tracking = servo problem) | confirmed | N206: "LQR for tracking a reference" (servo problem = tracking, FBS 2-17) |
| ctrl_ledger | setpoint | Note 117 (setpoint) | confirmed | N117: "act on error" (error = setpoint minus output) |
| ctrl_ledger | state, of a dynamical system | plan §4 State-space models; Note 63 | confirmed | N63: "state: pose, map, speeds; complete state"; plan §4 State-space models |
| ctrl_ledger | task description | Note 201 (trajectory generation as the task description) | out-of-scope | book-specific phrase (FBS 8-23: the input to trajectory generation); the concept itself, trajectory generation, is N201 "Path vs trajectory; time scaling" |
| ctrl_ledger | three-term controllers | Note 117 (three-term = PID) | confirmed | N117: "PD / PID" (three-term controller = PID, FBS 11-2) |
| ctrl_ledger | two degree-of-freedom control | Note 119 (feedforward plus feedback) | confirmed | N119: "Feedforward plus feedback" |
| ctrl_ledger | graph, edge set of | Note 103 (edges of a graph) | confirmed | N103: "graph as a model of a state space" (nodes and edges) |
| ctrl_ledger | graph, node set of | Note 103 | confirmed | N103: "graph as a model of a state space" (nodes and edges) |
| ctrl_ledger | system, linear | plan §4 new maths: State-space models (continuous and discrete time, x' = Ax + Bu); Note 204 | confirmed | plan §4 State-space models: "x_dot = Ax + Bu ...; discrete-time models x(k+1) = A x(k) + B u(k)" |
| ctrl_ledger | system, linear, continuous-time | plan §4 new maths: State-space models (continuous and discrete time, x' = Ax + Bu); Note 204 | confirmed | plan §4 State-space models: "x_dot = Ax + Bu" |
| ctrl_ledger | system, linear, discrete-time | plan §4 new maths: State-space models (continuous and discrete time, x' = Ax + Bu); Note 204 | confirmed | plan §4 State-space models: "discrete-time models x(k+1) = A x(k) + B u(k)" |
| ctrl_ledger | system, linear control | plan §4 new maths: State-space models (continuous and discrete time, x' = Ax + Bu); Note 204 | confirmed | plan §4 State-space models: "x_dot = Ax + Bu" |
| ctrl_ledger | weighted digraph | Note 104 (Dijkstra on a weighted directed graph) | confirmed | N104: "Dijkstra's shortest-path algorithm" (edge weights); Bullo's adjacency-matrix sense is in ctrl_adds Graph basics |
| ctrl_ledger | directed graphical model | Note 77 (dynamic Bayes network) | confirmed | N77: "hidden Markov model / dynamic Bayes network" (a directed graphical model) |
| ctrl_ledger | triangle inequality | Note 108 (rules a distance must follow) | confirmed | N108: "metric space: rules a distance must follow" (triangle inequality is one rule) |
| robo_ledger | actuator | N283: motors, gearing as actuators | confirmed | N283: "Motors, gearing" (motors are the actuators) |
| robo_ledger | collision–detection routine, sphere approximation | N108: bounding volumes (spheres) for collision checks | confirmed | N108: "bounding-volume hierarchies" (spheres as bounding volumes) |
| robo_ledger | condition number | MA-058: condition number (also used for manipulability in N278) | confirmed | MA-058: "condition number (G-441) ... σ1/σn" |
| robo_ledger | constraint, impenetrability | N288: impenetrability (no-penetration) contact constraint | confirmed | N288: "Contact kinematics: rolling, sliding, breaking free" (MR 12.1 impenetrability constraint) |
| robo_ledger | contact, roll–slide | N288: rolling and sliding contact | confirmed | N288: "Contact kinematics: rolling, sliding, breaking free" |
| robo_ledger | control, admittance-controlled robot | N287: admittance-controlled robot | confirmed | N287: "Admittance control" |
| robo_ledger | control, impedance-controlled robot | N287: impedance-controlled robot | confirmed | N287: "Impedance control: behave like a virtual spring and damper" |
| robo_ledger | damping, overdamped solution | N118: overdamped response | confirmed | N118: "overshoot, settling time, damping ratio" |
| robo_ledger | damping, underdamped solution | N118: underdamped response | confirmed | N118: "overshoot, settling time, damping ratio" |
| robo_ledger | diff-drive robot | N64: differential drive | confirmed | N64: "differential drive" |
| robo_ledger | distance-measurement algorithm | N108: distance computation between bodies | add | distance queries between bodies: minimum separation distance (GJK named) [robotics] → RO-05, extend N108 |
| robo_ledger | dynamics of open chains | N281: dynamics of open chains | confirmed | N281: "Manipulator equation M(q)q̈ + c(q,q̇) + g(q) = τ" |
| robo_ledger | dynamics of open chains, Lagrangian formulation | N281: Lagrangian formulation | confirmed | N281: "Lagrangian mechanics: L = kinetic − potential energy" |
| robo_ledger | dynamics of open chains, Newton–Euler recursive formulation with gearing | N283: Newton-Euler with gearing (reflected inertia) | confirmed | N282: "Recursive Newton–Euler inverse dynamics"; N283 "reflected inertia" |
| robo_ledger | elbow-down (righty) solution | N279: multiple IK solutions (elbow up/down) | confirmed | N279: "none, one, many or infinitely many answers; Analytic IK: 2-link planar arm" |
| robo_ledger | elbow-up (lefty) solution | N279: multiple IK solutions (elbow up/down) | confirmed | N279: "none, one, many or infinitely many answers; Analytic IK: 2-link planar arm" |
| robo_ledger | end-effector | N276: end-effector | confirmed | N276: "hand pose from screw axes" (hand = end-effector) |
| robo_ledger | generalized coordinates | N281: generalized coordinates | confirmed | N281: "Euler–Lagrange equation on a 2-link arm" (written in generalized coordinates q) |
| robo_ledger | generalized forces | N281: generalized forces | confirmed | N281: "Manipulator equation ... = τ" (τ = generalized forces) |
| robo_ledger | Grübler’s formula | N70: Grübler's formula | confirmed | N70: "Grübler's count of degrees of freedom" |
| robo_ledger | graph, weighted | N104: weighted graph (edge costs) | confirmed | N104: "Dijkstra's shortest-path algorithm" (weighted edges) |
| robo_ledger | inadmissible state | N203: inadmissible states in the phase plane (time-optimal scaling) | confirmed | N203: "Time-optimal time scaling under torque limits (phase plane)" |
| robo_ledger | Kalman rank condition | N204: Kalman rank condition for controllability | confirmed | N204: "Controllability (reachability) and the rank test" |
| robo_ledger | lefty solution | N279: lefty/righty IK branches | confirmed | N279: "none, one, many ... answers; Analytic IK: 2-link planar arm" |
| robo_ledger | Lie algebra | plan§4 Cross product and skew-symmetric matrix: so(3)/se(3) taught as skew-symmetric matrices and twists (N275) | confirmed | plan §4 "Cross product and skew-symmetric matrix" + "Axis-angle, exponential and log maps of rotations (SO(3) exp/log)"; N275 twists |
| robo_ledger | linearly controllable | N204: linear controllability | confirmed | N204: "Controllability (reachability) and the rank test" |
| robo_ledger | matrix logarithm, for rigid-body motion | N275: matrix log of a rigid motion | confirmed | N275: "Screw axis and exponential coordinates of a rigid motion"; plan §4 "Matrix exponential and logarithm" |
| robo_ledger | moment | N117: moment of force (torque) in the mechanics short section | confirmed | plan §4 Newtonian and rigid-body mechanics: "F = ma, torque" |
| robo_ledger | moment, pure | N275: pure moment as part of a wrench | confirmed | N275: "Wrench: force and torque as one 6-number vector" |
| robo_ledger | motion planning, anytime | N105: anytime planning (ARA*) | confirmed | N105: "anytime A* (ARA*)" |
| robo_ledger | motion planning, complete | N111: complete planners | confirmed | N111: "complete, resolution-complete and probabilistically complete planners" |
| robo_ledger | motion planning, computational complexity | N103: computational complexity of planning | confirmed | N103: "algorithm cost: Big-O ...; why exact planning is hard (NP-hard, PSPACE-hard)" |
| robo_ledger | motion planning, exact | N270: exact planning (exact roadmaps) | confirmed | N270: "Exact roadmaps" |
| robo_ledger | motion planning, nonlinear optimization | N116: planning by nonlinear optimisation | confirmed | N116: "gradient-based trajectory optimisation" |
| robo_ledger | motion planning, offline | N107: offline vs online planning | confirmed | N107: "D* fast replanning; bug algorithms in unknown spaces" (online vs offline planning) |
| robo_ledger | motion planning, online | N107: online planning (replanning) | confirmed | N107: "D* fast replanning" |
| robo_ledger | motion planning, optimal | N110: optimal planning (RRT*) | confirmed | N110: "RRT* and asymptotic optimality"; N9 "feasible vs optimal plan" |
| robo_ledger | motion planning, PRM algorithm | N111: PRM | confirmed | N111: "probabilistic and visibility roadmaps" |
| robo_ledger | motion planning, RDT algorithm | N110: RDT (rapidly exploring dense tree) | confirmed | N110: "rapidly-exploring random tree" (RDT is LaValle's name for the same tree) |
| robo_ledger | motion planning, resolution complete | N111: resolution completeness | confirmed | N111: "resolution-complete" |
| robo_ledger | motion planning, RRT algorithm | N110: RRT | confirmed | N110: "rapidly-exploring random tree" |
| robo_ledger | motion planning, RRT ∗ algorithm | N110: RRT* | confirmed | N110: "RRT*" |
| robo_ledger | motion planning, sampling methods | N110: sampling-based planning | confirmed | N110: "rapidly-exploring random tree"; N111 "probabilistic ... roadmaps" |
| robo_ledger | motion planning, satisficing | N9: satisficing (feasible) vs optimal | confirmed | N9: "feasible vs optimal plan" (satisficing = feasible) |
| robo_ledger | motion planning, smoothing | N113: path smoothing | confirmed | N113: "Path smoothing after a grid planner" |
| robo_ledger | motion planning, wheeled mobile robot | N112: planning for wheeled robots | confirmed | N112: "Dubins and Reeds-Shepp shortest car paths; Kinodynamic planning" |
| robo_ledger | omniwheel | N66: omniwheel | confirmed | N66: "Omnidirectional (mecanum) base model" |
| robo_ledger | open-chain mechanism | N69: open chain | confirmed | N69: "Forward kinematics of an open chain" |
| robo_ledger | parametrization, explicit | N72: explicit C-space parameterisation (plain words) | add | explicit vs implicit C-space representations: minimal coordinates (angles) vs a constrained embedding (rotation matrix with constraints) [robotics] → RO-01, extend N72 |
| robo_ledger | path | N104: path | confirmed | re-cite N201: "Path vs trajectory" |
| robo_ledger | polyhedral convex cone | MA-067: polyhedral convex cone (convex sets; friction pyramid N288) | confirmed | N288: "the friction cone (and its pyramid approximation)"; plan §4 Friction pyramid |
| robo_ledger | pseudoinverse | N279: pseudo-inverse in numerical IK | confirmed | N279: "Numerical IK: iterate with the Jacobian pseudo-inverse" |
| robo_ledger | redundant constraint | N70: redundant constraints in Grübler's count | out-of-scope | an exception case of Grübler's formula (MR p.14, closed chains); the formula itself is in N70 |
| robo_ledger | redundant robot | N278: redundant robot | confirmed | N278: "Redundancy and self-motion in the null space" |
| robo_ledger | Reeds–Shepp car | N64: Reeds-Shepp car | confirmed | N64: "Reeds-Shepp car models" |
| robo_ledger | representation, implicit | N72: implicit C-space representation (plain words) | add | explicit vs implicit C-space representations: minimal coordinates (angles) vs a constrained embedding (rotation matrix with constraints) [robotics] → RO-01, extend N72 |
| robo_ledger | righty solution | N279: righty IK branch | confirmed | N279: "none, one, many ... answers; Analytic IK: 2-link planar arm" |
| robo_ledger | rigid body, planar | N72: planar rigid body DOF | confirmed | N72: "Degrees of freedom of a body and of a robot" |
| robo_ledger | rigid body, spatial | N72: spatial rigid body DOF | confirmed | N72: "Degrees of freedom of a body and of a robot" |
| robo_ledger | Robot Operating System (ROS) | N127: ROS | confirmed | N127: "ROS 2: nodes, topics, services, actions" |
| robo_ledger | screw axis, body-frame | N276: body-frame screw axes | confirmed | N276: "hand pose from screw axes, in the base frame and the hand frame" |
| robo_ledger | screw axis, space-frame | N276: space-frame screw axes | confirmed | N276: "hand pose from screw axes, in the base frame and the hand frame" |
| robo_ledger | serial mechanism | N69: serial (open-chain) mechanism | confirmed | N69: "Forward kinematics of an open chain" (serial = open chain) |
| robo_ledger | singularity | N278: singularity | confirmed | N278: "Singularities: the Jacobian loses rank" |
| robo_ledger | singularity, kinematic | N278: kinematic singularity | confirmed | N278: "Singularities: the Jacobian loses rank" |
| robo_ledger | special orthogonal group (SO(3)) | N65: SO(3) | confirmed | N65: "Rotation matrix ... inverse = transpose" (SO(3) = the set of rotation matrices) |
| robo_ledger | standard second-order form | N118: standard second-order form | confirmed | N118: "natural frequency, damping ratio" |
| robo_ledger | tree | N103: tree (search tree) | confirmed | N110: "rapidly-exploring random tree"; N103 search trees of BFS/DFS |
| robo_ledger | tree, child node | N103: child node | confirmed | N103: "breadth-first and depth-first search" (search tree parent/child) |
| robo_ledger | tree, parent node | N103: parent node | confirmed | N103: "breadth-first and depth-first search" (search tree parent/child) |
| robo_ledger | velocity limit curve | N203: velocity limit curve in the phase plane | confirmed | N203: "Time-optimal time scaling under torque limits (phase plane)" |
| robo_ledger | wheeled mobile robot, diff-drive | N64: diff-drive robot | confirmed | N64: "differential drive" |
| robo_ledger | wheeled mobile robot, nonholonomic | N64: nonholonomic wheeled robot | confirmed | N64: "holonomic vs nonholonomic constraints" |
| robo_ledger | C 0 function | N202: continuity at the joins of a trajectory | confirmed | N202: "continuity at the joins" |
| robo_ledger | C k function | N202: continuity of derivatives at trajectory joins | confirmed | N202: "continuity at the joins" |
| robo_ledger | A ∗ algorithm | N105: A* search | confirmed | N105: "A* search with an admissible heuristic" |
| robo_ledger | acceleration vector | N117: short mechanics section (F = ma) | confirmed | plan §4 Newtonian and rigid-body mechanics: "F = ma" |
| robo_ledger | acceleration-based control | N106: navigation function used as feedback; acceleration form is a variant | out-of-scope | LaValle §8.4 extension of navigation-function feedback to second-order (acceleration-input) systems; research-level, kinodynamic planning itself is N112 |
| robo_ledger | actuators | N283: motors and actuators | confirmed | N283: "Motors, gearing" |
| robo_ledger | admissible conﬁgurations | N292: manipulation planning (transit and transfer) | confirmed | N292: "transit and transfer moves" (admissible configurations are their state space, LaValle 7.3.2) |
| robo_ledger | approximate optimal motion planning | N110: asymptotic optimality (RRT*) | confirmed | N110: "RRT* and asymptotic optimality"; N106 "DP with interpolation on continuous spaces" |
| robo_ledger | asymptotic convergence to a goal | N106: navigation function converges to the goal | confirmed | N106: "navigation function with one minimum at the goal" |
| robo_ledger | asymptotic solution plan | N106: feedback plan that reaches the goal in the limit | confirmed | N106: "feedback planning by DP with interpolation" |
| robo_ledger | average cost-per-stage model | N27: average-reward setting | confirmed | N8: "infinite horizon: discounted and average cost"; N27 "average-reward setting" |
| robo_ledger | axis-aligned bounding box | N108: bounding-volume hierarchies | confirmed | N108: "bounding-volume hierarchies" (axis-aligned boxes are one bounding volume) |
| robo_ledger | backprojection | N292: preimage planning | confirmed | re-cite N7: "forward projections and backprojections" |
| robo_ledger | backward action space | N105: backward search | confirmed | N105: "backward and bidirectional search" |
| robo_ledger | backward reachable set | N197: reach-avoid / backward reachable values | confirmed | N197: "recovery policies and reach-avoid values"; N112 "reachable sets" |
| robo_ledger | backward search, with backprojections | N292: preimage planning with backprojections | confirmed | N105: "backward and bidirectional search" + N7 "backprojections" |
| robo_ledger | backward state transition equation | N105: backward search | confirmed | N105: "backward and bidirectional search" |
| robo_ledger | backward value iteration, for reinforcement learning | N14: value iteration, RL link | confirmed | N14: "value iteration" |
| robo_ledger | backward value iteration, for sequential games | N54: sequential games on state spaces | confirmed | N54: "sequential games on state spaces" |
| robo_ledger | backward value iteration, on a probabilistic I-space | N268: value iteration in belief space | confirmed | N268: "value iteration in belief space" |
| robo_ledger | backward value iteration, path-constrained | N203: time scaling along a fixed path (phase plane) | confirmed | N203: "Time-optimal time scaling under torque limits (phase plane)" |
| robo_ledger | backward value iteration, running time | N103: algorithm cost, Big-O | confirmed | N103: "algorithm cost: Big-O"; N14 "value iteration" |
| robo_ledger | backward value iteration, under diﬀerential constraints | N112: lattice search under motion limits | confirmed | re-cite N106: "DP with interpolation on continuous spaces" |
| robo_ledger | backward value iteration, with average cost-per-stage | N27: average-reward setting | confirmed | N27: "average-reward setting"; N8 "average cost" |
| robo_ledger | backward value iteration, with discounted cost | N14: discounted value iteration | confirmed | N14: "value iteration"; N8 "discount factor" |
| robo_ledger | backward value iteration, with nondeterministic uncertainty | N14: value iteration with nature | confirmed | N14: "value iteration with nature"; N53 "worst-case vs expected-cost decisions" |
| robo_ledger | backward value iteration, with probabilistic uncertainty | N14: value iteration with stochastic outcomes | confirmed | N14: "value iteration with nature (stochastic outcomes)" |
| robo_ledger | bang-bang approach | N203: time-optimal (bang-bang) time scaling | add | bang-bang (time-optimal) control: full acceleration then full braking; the double-integrator case [control] → RO-15, extend N203 (merges existing robo_adds: bang-bang (time-optimal) trajectory) |
| robo_ledger | best-ﬁrst search | N105: best-first search | confirmed | N105: "best-first search" |
| robo_ledger | bitangent line | N270: visibility graph (bitangent edges) | confirmed | N270: "shortest-path roadmap (visibility graph)" (bitangent lines are its edges) |
| robo_ledger | boundary representation | N71: polygons described by their boundary edges | confirmed | N71: "obstacles as polygons built from half-planes; triangle meshes and bitmaps" |
| robo_ledger | bounded-acceleration model | N112: planning with motion limits (speed/acceleration bounds) | confirmed | N112: "kinodynamic planning and phase-space obstacles" |
| robo_ledger | bounded-velocity model | N112: planning with motion limits (speed/acceleration bounds) | confirmed | N112: "kinodynamic planning and phase-space obstacles" |
| robo_ledger | Boustrophedon decomposition | N273: coverage planning (boustrophedon cells) | add | boustrophedon (lawnmower) cell decomposition for coverage [robotics] → RO-23, extend N273 |
| robo_ledger | breadth-ﬁrst search | N103: breadth-first search | confirmed | N103: "breadth-first and depth-first search" |
| robo_ledger | calculus of variations | N202: beginner calculus of variations (minimum jerk), plan§4 | confirmed | plan §4: "Cubic splines and minimum jerk (beginner calculus of variations)" |
| robo_ledger | closed-loop, control law | N117: feedback control law | confirmed | N117: "PD / PID feedback control" |
| robo_ledger | collision-detection | N108: collision detection | confirmed | N108: "collision detection: broad and narrow phase" |
| robo_ledger | combinatorial motion planning | N270: exact (combinatorial) roadmaps | confirmed | N270: "Exact roadmaps; vertical cell decomposition" |
| robo_ledger | combinatorial motion planning, cell decompositions | N270: vertical cell decomposition | confirmed | N270: "vertical cell decomposition" |
| robo_ledger | combinatorial motion planning, introductory concepts | N270: exact roadmaps | confirmed | N270: "Exact roadmaps" |
| robo_ledger | combinatorial motion planning, polygonal case (see Canny’s roadmap algorithm see also cylindrical algebraic decomposition) | N270: polygonal exact planning | confirmed | N270: "vertical cell decomposition; ... visibility graph" (polygonal case) |
| robo_ledger | commutator motion | N67: parallel-parking intuition for car controllability, in plain words | confirmed | N67: "Controllability of a car in plain words (parallel parking)" (the parking wiggle is the commutator motion) |
| robo_ledger | completely integrable | N64: holonomic = integrable constraint | confirmed | N64: "holonomic vs nonholonomic constraints" (holonomic = integrable) |
| robo_ledger | completeness | N111: complete, resolution-complete, probabilistically complete | confirmed | N111: "complete, resolution-complete and probabilistically complete planners" |
| robo_ledger | completeness, overview (see probabilistic completeness see also resolution completeness) | N111: completeness notions | confirmed | N111: "complete, resolution-complete and probabilistically complete planners" |
| robo_ledger | complexity class | N103: NP-hard, PSPACE-hard | confirmed | N103: "why exact planning is hard (NP-hard, PSPACE-hard)" |
| robo_ledger | complexity of motion planning | N103: why exact planning is hard | confirmed | N103: "why exact planning is hard (NP-hard, PSPACE-hard)" |
| robo_ledger | complexity of motion planning, lower bounds | N103: hardness of planning | confirmed | N103: "why exact planning is hard (NP-hard, PSPACE-hard)" |
| robo_ledger | compliant motions | N292: compliant motions in preimage planning | confirmed | N292: "preimage planning"; N287 "Impedance control" |
| robo_ledger | conditional Bayes’ risk | N53: Bayesian decision making with observations | confirmed | N53: "Bayesian decision making with observations" |
| robo_ledger | conditional Bayes’ rule | N78: Bayes' theorem conditioned on past data | confirmed | N78: "Bayes' theorem conditioned on past data" |
| robo_ledger | conﬁguration space | N72: configuration space | confirmed | N72: "configuration space (C-space)" |
| robo_ledger | conﬁguration space, of 2D rigid bodies | N72: C-space of a 2D rigid body | confirmed | N72: "Degrees of freedom of a body"; "C-space shapes in plain words" |
| robo_ledger | conﬁguration space, of 3D rigid bodies | N72: C-space of a 3D rigid body | confirmed | N72: "Degrees of freedom of a body"; "C-space shapes in plain words" |
| robo_ledger | conﬁguration space, of chains of bodies | N72: C-space of chains | confirmed | N72: "Degrees of freedom of a body and of a robot" |
| robo_ledger | conﬁguration space, of trees of bodies | N69: kinematic trees | confirmed | N69: "kinematic trees (branching bodies such as humanoids)" |
| robo_ledger | conﬁguration space, velocity constraints on | N64: velocity (nonholonomic) constraints | confirmed | N64: "Nonholonomic constraint: a wheel cannot slide sideways" |
| robo_ledger | conservative system | N281: energy-conserving systems in Lagrangian mechanics | confirmed | N281: "L = kinetic − potential energy" (conservative forces come from a potential) |
| robo_ledger | controllability of a system, linear case | N204: controllability of linear systems | confirmed | N204: "Controllability (reachability) and the rank test" |
| robo_ledger | controlled Markov process | N7: Markov decision process | confirmed | N7: "Markov decision processes" |
| robo_ledger | convolution | DL-042: convolution (Minkowski sum as convolution, N73) | confirmed | DL-042 (convolution operation); N73 "Minkowski sum" |
| robo_ledger | coordination space | N271: decoupled multi-robot planning (coordination space) | confirmed | N271: "decoupled planning: path first, then timing" |
| robo_ledger | cost functional | N116: trajectory-optimisation cost | confirmed | N116: "gradient-based trajectory optimisation" |
| robo_ledger | cost functional, approximating | N106: cost approximated by interpolation in DP | confirmed | N106: "DP with interpolation on continuous spaces" |
| robo_ledger | cost functional, quadratic | N205: quadratic cost (LQR) | confirmed | N205: "linear-quadratic regulator" |
| robo_ledger | cost-to-come | N104: cost-to-come in Dijkstra | confirmed | N104: "Dijkstra's shortest-path algorithm" (its distance label is the cost-to-come) |
| robo_ledger | decision problem | N103: complexity of decision problems | confirmed | N103: "NP-hard, PSPACE-hard" |
| robo_ledger | decision vertex (in a game tree) | N54: game trees | confirmed | N54: "game trees and alpha-beta pruning" |
| robo_ledger | depth-ﬁrst search | N103: depth-first search | confirmed | N103: "breadth-first and depth-first search" |
| robo_ledger | depth-mapping sensors | N90: depth cameras and depth sensing | confirmed | N90: "Depth cameras: structured light and time of flight" |
| robo_ledger | diﬀerential models, conversion from implicit to parametric | N64: from velocity constraints to a velocity model | add | velocity constraints in implicit (Pfaffian) form A(q)q̇ = 0 and converting them to a parametric model q̇ = G(q)u [robotics] → RO-01, extend N64 (merges existing robo_adds: Pfaffian velocity constraints A(q)q̇ = 0) |
| robo_ledger | diﬀerential models, implicit representation | N64: implicit (constraint) form | add | velocity constraints in implicit (Pfaffian) form A(q)q̇ = 0 and converting them to a parametric model q̇ = G(q)u [robotics] → RO-01, extend N64 (merges existing robo_adds: Pfaffian velocity constraints A(q)q̇ = 0) |
| robo_ledger | diﬀerentially ﬂat systems | N223: differential flatness | confirmed | N223: "Differential flatness" |
| robo_ledger | Dijkstra’s algorithm, extension of to continuous spaces | N106: Dijkstra-like DP on continuous spaces with interpolation | confirmed | N106: "DP with interpolation on continuous spaces" |
| robo_ledger | Dijkstra’s algorithm, with probabilistic uncertainty | N14: value iteration with stochastic outcomes | confirmed | N14: "value iteration with nature (stochastic outcomes)" |
| robo_ledger | discrete feasible planning | N103: discrete feasible planning as graph search | confirmed | N103: "graph as a model of a state space"; N9 "feasible vs optimal plan" |
| robo_ledger | discretization of C | N106: grids over C-space | confirmed | N106: "value iteration on a robot grid map"; N79 "static and adaptive cell decomposition" |
| robo_ledger | distance between sets | N108: distance between robot and obstacles | add | distance queries between bodies: minimum separation distance (GJK named) [robotics] → RO-05, extend N108 |
| robo_ledger | dominated action | N53: dominated actions (Pareto) | confirmed | N53: "multi-objective optimisation and Pareto-optimal plans" |
| robo_ledger | double integrator, lattice | N114: state lattice | confirmed | N114: "State-lattice planning with motion primitives" |
| robo_ledger | double integrator, optimal planning for | N203: time-optimal (bang-bang) motion | add | bang-bang (time-optimal) control: full acceleration then full braking; the double-integrator case [control] → RO-15, extend N203 (merges existing robo_adds: bang-bang (time-optimal) trajectory) |
| robo_ledger | dynamic constraints | N112: kinodynamic planning | confirmed | N112: "kinodynamic planning" |
| robo_ledger | dynamic programming | N14: dynamic programming | confirmed | N14: "value iteration"; N10 "principle of optimality" |
| robo_ledger | dynamics, of a set of particles | N220: centre of mass of many particles | confirmed | plan §4 Newtonian and rigid-body mechanics: "F = ma"; N220 "F = ma plus Euler's equation" |
| robo_ledger | dynamics, of a two-link manipulator | N281: 2-link arm dynamics | confirmed | N281: "Euler–Lagrange equation on a 2-link arm" |
| robo_ledger | dynamics, of chains of bodies | N282: dynamics of chains | confirmed | N282: "Recursive Newton–Euler inverse dynamics"; N281 "Manipulator equation" |
| robo_ledger | dynamics, with nonconservative forces | N281: torques/forces outside the potential | confirmed | N281: "Manipulator equation ... = τ" (τ = non-conservative input forces) |
| robo_ledger | Euclidean shortest paths | N270: shortest-path roadmap (visibility graph) | confirmed | N270: "shortest-path roadmap (visibility graph)" |
| robo_ledger | Euler-Lagrange equation, with conservative forces | N281: Euler-Lagrange equation | confirmed | N281: "Euler–Lagrange equation" |
| robo_ledger | expected-case analysis | N53: expected-case vs worst-case decisions | confirmed | N53: "worst-case vs expected-cost decisions" |
| robo_ledger | feasible planning, discrete | N103: discrete feasible planning | confirmed | N9: "feasible vs optimal plan"; N103 graph search |
| robo_ledger | feedback motion planning, complete, optimal | N106: optimal navigation functions / wavefront on continuous spaces | confirmed | N106: "feedback planning by DP with interpolation; navigation function" |
| robo_ledger | feedback motion planning, complete, some dynamics | N106: navigation functions | confirmed | N106: "navigation function with one minimum at the goal" |
| robo_ledger | feedback plan, cost of | N14: cost of a feedback plan (value) | confirmed | N14: "cost-to-go as the planning name for value" |
| robo_ledger | feedback plan, information feedback | N153: policies over information/belief space | confirmed | N153: "planning in belief / information space" |
| robo_ledger | feedback plan, sensor feedback | N153: sensor-feedback policies | confirmed | N153: "planning in belief / information space" |
| robo_ledger | ﬁxed-path coordination | N271: decoupled multi-robot coordination | confirmed | N271: "decoupled planning: path first, then timing" |
| robo_ledger | ﬁxed-roadmap coordination | N271: decoupled multi-robot coordination | confirmed | N271: "centralized vs decoupled (prioritized) multi-robot planning" |
| robo_ledger | ﬂat cylinder | N72: C-space shapes in plain words | confirmed | N72: "C-space shapes in plain words: circle, torus (manifolds)" |
| robo_ledger | ﬂat outputs | N223: flat outputs | confirmed | N223: "state and inputs from position, yaw and derivatives" (flat outputs) |
| robo_ledger | force | N117: force (short mechanics section) | confirmed | plan §4 Newtonian and rigid-body mechanics: "F = ma" |
| robo_ledger | force, resultant | N117: net force | confirmed | plan §4 Newtonian and rigid-body mechanics: "F = ma" |
| robo_ledger | forward projection | N78: prediction step (forward projection of belief) | confirmed | re-cite N7: "forward projections and backprojections" |
| robo_ledger | forward projection, diﬀerential | N112: reachable sets | confirmed | N112: "reachable sets" |
| robo_ledger | forward projection, nondeterministic | N112: reachable sets | confirmed | N7: "forward projections"; N112 "reachable sets" |
| robo_ledger | forward projection, probabilistic | N78: prediction step | confirmed | re-cite N7: "forward projections"; N78 "predict" |
| robo_ledger | forward projection, under a ﬁxed plan | N78: prediction step | confirmed | re-cite N7: "forward projections" |
| robo_ledger | forward search, A ∗ algorithm | N105: A* search | confirmed | N105: "A* search with an admissible heuristic" |
| robo_ledger | forward search, best ﬁrst | N105: best-first search | confirmed | N105: "best-first search" |
| robo_ledger | forward search, breadth-ﬁrst | N103: breadth-first search | confirmed | N103: "breadth-first and depth-first search" |
| robo_ledger | forward search, depth-ﬁrst | N103: depth-first search | confirmed | N103: "breadth-first and depth-first search" |
| robo_ledger | forward search, general, discrete | N103: general forward search | confirmed | N103: "graph as a model of a state space; breadth-first and depth-first search" |
| robo_ledger | frontier set | N104: search frontier (priority queue) | confirmed | N104: "priority queue; Dijkstra's" (the queue holds the frontier) |
| robo_ledger | fully actuated system | N221: fully actuated vs underactuated | add | under-, fully and over-actuated systems [robotics] → RO-01, extend N66 (merges existing robo_adds: under-, fully and over-actuated robots) |
| robo_ledger | functional | N116: cost over a whole trajectory | confirmed | plan §4: "beginner calculus of variations"; N116 trajectory cost |
| robo_ledger | gain constant | N117: feedback gains | confirmed | N117: "PD / PID feedback control" |
| robo_ledger | game, alternating-play model | N54: sequential games | confirmed | N54: "sequential games on state spaces" |
| robo_ledger | game, extensive form | N54: game trees (extensive form) | confirmed | N54: "game trees and alpha-beta pruning" |
| robo_ledger | game, normal form | N54: matrix games (normal form) | confirmed | N54: "zero-sum games, minimax ...; mixed strategies solved by linear programming" (matrix = normal form) |
| robo_ledger | game against nature, sequential | N14: value iteration with nature | confirmed | N53: "game against nature"; N14 "value iteration with nature" |
| robo_ledger | generalized coordinates | N281: generalized coordinates q in L(q, q_dot) | confirmed | N281: "Euler–Lagrange equation" (in generalized coordinates q) |
| robo_ledger | generalized forces | N281: generalized forces in the Euler-Lagrange equation | confirmed | N281: "Manipulator equation ... = τ" (τ = generalized forces) |
| robo_ledger | geometric modeling | N71: geometric representations of obstacles | confirmed | N71: "obstacles as polygons built from half-planes; triangle meshes and bitmaps" |
| robo_ledger | globally asymptotically stable | N199: global asymptotic stability via Lyapunov functions | add | local vs global (asymptotic) stability and the region of attraction [control] → MA 06-calculus, extend the planned Stability of dynamical systems Note (plan §4) (merges existing ctrl_adds: Phase-plane types of equilibria (...local vs global stability and the region of attraction); robo_adds: region of attraction) |
| robo_ledger | globally positive deﬁnite | N199: positive definite Lyapunov function | confirmed | N199: "Stability certificates with Lyapunov functions" (a Lyapunov function is positive definite by definition) |
| robo_ledger | Grübler’s formula | N70: Grübler's count of degrees of freedom | confirmed | N70: "Grübler's count of degrees of freedom" |
| robo_ledger | grasped conﬁgurations | N292: grasped configurations in manipulation planning (transit/transfer) | confirmed | N292: "transit and transfer moves" |
| robo_ledger | great circle | plan§4: 3D rotations: Euler angles and quaternions: distances on rotations/directions; also N108 | confirmed | N108: "distances on angles; uniform random samples of rotations and directions" |
| robo_ledger | grid, resolution issues | N106: grid resolution and its effect on planning | confirmed | N111: "resolution-complete"; N106 "value iteration on a robot grid map" |
| robo_ledger | half-space | N71: half-spaces (3D version of half-planes) | confirmed | N71: "obstacles as polygons built from half-planes" |
| robo_ledger | hierarchical planning | N126: layers mission > behaviour > motion > control | confirmed | N126: "the layers mission → behaviour → motion → control" |
| robo_ledger | implicit velocity constraints | N64: velocity constraints (holonomic/nonholonomic) | add | velocity constraints in implicit (Pfaffian) form A(q)q̇ = 0 and converting them to a parametric model q̇ = G(q)u [robotics] → RO-01, extend N64 (merges existing robo_adds: Pfaffian velocity constraints A(q)q̇ = 0) |
| robo_ledger | incremental sampling and searching, adapting search algorithms | N110: sampling-based planners adapting search | confirmed | N110: "rapidly-exploring random tree" |
| robo_ledger | incremental sampling and searching, general framework | N110: incremental sampling-and-searching framework | confirmed | N110: "rapidly-exploring random tree"; N111 "probabilistic roadmaps" |
| robo_ledger | incremental sampling and searching, under diﬀerential constraints | N112: kinodynamic sampling-based planning | confirmed | N112: "kinodynamic RRT; lattice search" |
| robo_ledger | information space, in continuous state spaces | N80: continuous-state information spaces (Kalman/particle) | confirmed | N78: "belief as the probabilistic information state"; N80 "Kalman filter" |
| robo_ledger | information space, sensor feedback (see history information space see also nondeterministic information space see also probabilistic information space) | N77: history information space | confirmed | N77: "information state: the history of actions and readings" |
| robo_ledger | information transition equation | N78: information/belief transition (Bayes filter) | confirmed | N78: "Bayes filter predict and update steps; belief as the probabilistic information state" |
| robo_ledger | information transition function | N78: belief transition function | confirmed | N78: "Bayes filter predict and update steps" |
| robo_ledger | information-feedback plan | N153: information-feedback plan (policy over beliefs) | confirmed | N153: "planning in belief / information space" |
| robo_ledger | intractable problem | N103: intractable / NP-hard planning | confirmed | N103: "why exact planning is hard (NP-hard, PSPACE-hard)" |
| robo_ledger | jerk (third time derivative) | N202: jerk and minimum-jerk | confirmed | N202: "Minimum-jerk trajectories" |
| robo_ledger | junction of links | N69: kinematic trees: links joined at junctions | confirmed | N69: "kinematic trees (branching bodies)" |
| robo_ledger | Kalman rank condition | N204: controllability rank test | confirmed | N204: "Controllability (reachability) and the rank test" |
| robo_ledger | kinematics for wheeled systems | N64: wheeled-robot kinematics (also N66, N67) | confirmed | N64: "Differential drive: wheel speeds to (v, ω)"; N66, N67 |
| robo_ledger | Kutzbach criterion | N70: Grübler/Kutzbach DOF count | confirmed | N70: "Grübler's count of degrees of freedom" (Kutzbach criterion = Grübler's formula) |
| robo_ledger | lattice, for unconstrained mechanical systems | N114: lattice for mechanical systems (motion primitives) | confirmed | N114: "State-lattice planning with motion primitives" |
| robo_ledger | linear complementarity problem | N289: complementarity contact model | confirmed | N289: "Complementarity contact model" |
| robo_ledger | linear momentum | N220: linear momentum (F = ma) | confirmed | N220: "F = ma"; N301 "momentum" |
| robo_ledger | linear sensing models | N80: linear measurement model | confirmed | N80: "linear Gaussian system" |
| robo_ledger | linear system, time-varying | N206: time-varying linear systems (time-varying LQR) | confirmed | N206: "Time-varying LQR to hold a robot on a planned trajectory" |
| robo_ledger | link | N70: link | confirmed | N70: "links, joints" |
| robo_ledger | local operator | N106: local operator of value iteration | confirmed | N106: "DP with interpolation on continuous spaces" (the local operator is its one-step min) |
| robo_ledger | local planning method | N111: local planner in sampling-based roadmaps | confirmed | N111: "probabilistic and visibility roadmaps" (the local planner connects roadmap nodes) |
| robo_ledger | local planning method, under diﬀerential constraints | N112: steering/local planning under motion limits | confirmed | N112: "motion primitives and a system simulator" |
| robo_ledger | locally positive deﬁnite | N199: positive definite functions (Lyapunov) | confirmed | N199: "Stability certificates with Lyapunov functions" |
| robo_ledger | lower pairs | N70: lower pairs = basic joint types | confirmed | N70: "Joint types (revolute, prismatic, spherical...)" (= lower pairs) |
| robo_ledger | lower value of a game | N54: minimax value of a game | confirmed | N54: "zero-sum games, minimax and saddle points" |
| robo_ledger | maneuver | N114: maneuvers = motion primitives | confirmed | N114: "State-lattice planning with motion primitives" (maneuver = motion primitive) |
| robo_ledger | maneuver automaton | N114: maneuver automaton = motion-primitive library | confirmed | N114: "motion primitives"; N112 "motion primitives and a system simulator" |
| robo_ledger | maze searching | N107: searching an unknown maze (bug/exploration strategies) | confirmed | N107: "bug algorithms in unknown spaces" |
| robo_ledger | mechanics, Newton-Euler (see dynamics) | N220: Newton-Euler rigid-body mechanics | confirmed | N220: "F = ma plus Euler's equation" |
| robo_ledger | moment of momentum | N220: angular momentum (behind Euler's equation) | confirmed | N301: "only contact forces and gravity change the whole body's momentum"; N220 Euler's equation |
| robo_ledger | moment-based approximations | N80: approximating a belief by its mean and covariance | confirmed | N80: "Kalman filter" (Gaussian belief by mean and covariance); N269 "augmented MDP (mean + entropy summary)" |
| robo_ledger | multiobjective optimization | N53: multi-objective optimisation and Pareto optimality | confirmed | N53: "multi-objective optimisation and Pareto-optimal plans" |
| robo_ledger | multiple query | N111: multiple-query roadmaps (PRM) | add | single-query vs multiple-query planners [robotics] → RO-05, extend N111 (merges existing robo_adds: single-query vs multi-query planners) |
| robo_ledger | multiple-robot motion planning | N271: multi-robot motion planning | confirmed | N271: "centralized vs decoupled (prioritized) multi-robot planning" |
| robo_ledger | nature action space | N53: nature's actions | confirmed | N53: "game against nature" |
| robo_ledger | navigation function, stochastic | N14: value function with stochastic outcomes | confirmed | N14: "value iteration with nature"; N106 "navigation function" |
| robo_ledger | navigation problem | N107: navigating in unknown environments | confirmed | N107: "bug algorithms in unknown spaces" |
| robo_ledger | Newton’s laws | plan§4: Newtonian and rigid-body mechanics: short section in N117 | confirmed | plan §4 Newtonian and rigid-body mechanics: "F = ma, torque, inertia matrix" |
| robo_ledger | next-best-view problem | N180: choosing the next best view by information gain | confirmed | N180: "expected information gain of an action; greedy and multi-step exploration" |
| robo_ledger | nonconservative forces | N281: nonconservative forces enter as generalized forces (torques, friction) | confirmed | N281: "Manipulator equation ... = τ" |
| robo_ledger | nonconvex, polyhedron | N71: nonconvex polyhedra | confirmed | N71: "obstacles as polygons built from half-planes; triangle meshes" |
| robo_ledger | nondeterministic uncertainty | N53: worst-case (nondeterministic) decisions against nature | confirmed | N53: "worst-case vs expected-cost decisions" |
| robo_ledger | nonzero-sum game, with more than two players | N54: nonzero-sum games with several players | confirmed | N54: "nonzero-sum games and Nash equilibrium" |
| robo_ledger | OBB | N108: oriented bounding boxes in bounding-volume hierarchies | confirmed | N108: "bounding-volume hierarchies" |
| robo_ledger | obstacle region, in the state space | N112: obstacles in phase/state space | confirmed | N112: "kinodynamic planning and phase-space obstacles" |
| robo_ledger | obstacle region, in the world | N71: obstacles in the world | confirmed | re-cite N73: "obstacle region and free space" |
| robo_ledger | obstacle region, polygonal case | N270: planning among polygonal obstacles (exact roadmaps) | confirmed | N270: "vertical cell decomposition; ... visibility graph" |
| robo_ledger | odometric coordinates | N68: odometry coordinates | confirmed | N68: "odometry motion model; Wheel odometry" |
| robo_ledger | open-loop, control law | N9: open-loop control | add | open-loop vs closed-loop (feedback) control: why feedback corrects disturbances and model error [control] → RO-06, extend N117 (PD and PID control) (merges existing robo_adds: open-loop vs closed-loop control) |
| robo_ledger | optimal motion planning | N110: optimal motion planning (RRT*, asymptotic optimality) | confirmed | N110: "RRT* and asymptotic optimality" |
| robo_ledger | optimal planning, discrete | N104: optimal discrete planning (shortest paths) | confirmed | N104: "Dijkstra's shortest-path algorithm" |
| robo_ledger | optimal planning, ﬁxed-length plans | N14: fixed-length optimal plans by value iteration | confirmed | N14: "value iteration" |
| robo_ledger | optimal planning, unspeciﬁed length | N14: optimal plans of unspecified length by value iteration | confirmed | N14: "value iteration" |
| robo_ledger | optimization | N53: optimisation in decision making | confirmed | N53: "Bayesian decision making ...; utility theory" |
| robo_ledger | oriented bounding box | N108: oriented bounding box | confirmed | N108: "bounding-volume hierarchies" |
| robo_ledger | parallel-jaw gripper | N291: parallel-jaw (antipodal) grasps | confirmed | N291: "antipodal grasps" (the parallel-jaw grasp) |
| robo_ledger | Pareto optimal | N53: Pareto optimal | confirmed | N53: "Pareto-optimal plans" |
| robo_ledger | part conﬁguration space | N292: part (object) configuration space in manipulation planning | confirmed | N292: "transit and transfer moves" |
| robo_ledger | path | N72: path as a continuous curve in C-space | confirmed | re-cite N201: "Path vs trajectory"; N72 "basic motion planning problem" |
| robo_ledger | path-constrained phase space | N203: path-constrained phase plane | confirmed | N203: "Time-optimal time scaling under torque limits (phase plane)" |
| robo_ledger | peg-in-hole problem | N327: peg-in-hole insertion | confirmed | N327: "insertion and assembly" |
| robo_ledger | phase constraints | N112: phase-space (state) constraints | confirmed | N112: "kinodynamic planning and phase-space obstacles" |
| robo_ledger | phase space | N112: phase space | confirmed | plan §4 State-space models: "phase space"; N112 "phase-space obstacles" |
| robo_ledger | phase space, obstacles | N112: phase-space obstacles | confirmed | N112: "phase-space obstacles" |
| robo_ledger | phase space, path-constrained | N203: path-constrained phase space (time scaling) | confirmed | N203: "(phase plane)" |
| robo_ledger | piecewise-linear obstacle motion | N271: moving obstacles | confirmed | N271: "time-varying obstacles and velocity tuning" |
| robo_ledger | planner | N9: planner / plan | confirmed | N9: "feasible vs optimal plan" |
| robo_ledger | planning under sensing uncertainty | N153: planning under sensing uncertainty | confirmed | N153: "planning in belief / information space" |
| robo_ledger | planning under sensing uncertainty, general methods | N153: general methods (belief/information space) | confirmed | N153: "planning in belief / information space" |
| robo_ledger | planning under sensing uncertainty, manipulation | N292: manipulation under uncertainty (preimage planning) | confirmed | N292: "preimage planning" |
| robo_ledger | policy iteration, with average cost-per-stage | N27: average-cost setting | confirmed | N27: "average-reward setting"; N13 "policy iteration" |
| robo_ledger | polygonal model | N71: polygonal obstacle models | confirmed | N71: "obstacles as polygons built from half-planes" |
| robo_ledger | polygonal model, representation | N71: obstacles as polygons | confirmed | N71: "obstacles as polygons built from half-planes" |
| robo_ledger | polyhedral model | N71: polyhedra from half-spaces | confirmed | N71: "obstacles as polygons built from half-planes; triangle meshes" |
| robo_ledger | position sensor | N63: position as a measured state | confirmed | re-cite N85: "GNSS/GPS basics"; N63 "measurements" |
| robo_ledger | positive deﬁnite function | N199: positive definite function in Lyapunov certificates (plan§4 Lyapunov functions) | confirmed | N199: "Lyapunov functions"; plan §4 Lyapunov functions |
| robo_ledger | potential function, discrete | N106: discrete navigation function / wavefront | confirmed | N106: "navigation function ...; grid wavefront propagation" |
| robo_ledger | preimage of a motion command | N292: preimage planning | confirmed | N292: "preimage planning" |
| robo_ledger | probabilistic information space, approximations | N269: approximate belief representations | confirmed | N269: "QMDP; augmented MDP; Monte Carlo POMDP with particle beliefs" |
| robo_ledger | projective geometry | N88: projective homogeneous coordinates (plan§4) | confirmed | plan §4 "Projective homogeneous coordinates"; N88 "Homogeneous coordinates" |
| robo_ledger | PSPACE | N103: PSPACE-hard named | confirmed | N103: "PSPACE-hard" |
| robo_ledger | pure strategy | N54: pure vs mixed strategies | confirmed | N54: "mixed strategies" (pure strategy is the non-mixed case) |
| robo_ledger | Q-factor | N21: Q-factor = action value | confirmed | N21: "Q-learning" (Q-factor = action value, N9 "action-value functions") |
| robo_ledger | quadratic cost functional | N205: quadratic cost (LQR) | confirmed | N205: "linear-quadratic regulator" |
| robo_ledger | quaternion | N65: quaternions (plan§4 3D rotations) | confirmed | plan §4 "3D rotations: Euler angles and quaternions" |
| robo_ledger | randomized algorithm | N110: randomized algorithms (RRT, PRM) | confirmed | N110: "rapidly-exploring random tree"; N111 "probabilistically complete" |
| robo_ledger | randomized plan | N54: randomized (mixed) strategy | confirmed | N54: "mixed strategies" |
| robo_ledger | randomized strategy | N54: mixed strategy | confirmed | N54: "mixed strategies" |
| robo_ledger | randomized value | N54: value of a zero-sum game | confirmed | N54: "mixed strategies solved by linear programming" |
| robo_ledger | rapidly exploring dense tree | N110: RRT/RDT | confirmed | N110: "rapidly-exploring random tree" |
| robo_ledger | rapidly exploring dense tree, exploration | N110: RRT exploration | confirmed | N110: "rapidly-exploring random tree" |
| robo_ledger | rapidly exploring dense tree, ﬁnding nearest points | N108: nearest-point search for RRT | confirmed | N108: "kd-tree nearest-neighbour search" |
| robo_ledger | rapidly exploring dense tree, making planners | N110: RRT-based planners | confirmed | N110: "rapidly-exploring random tree" |
| robo_ledger | rapidly exploring dense tree, under diﬀerential constraints | N112: kinodynamic RRT | confirmed | N112: "kinodynamic RRT" |
| robo_ledger | rational decision maker | N53: utility and rationality | confirmed | N53: "utility theory and rationality" |
| robo_ledger | reachability graph | N112: reachability graph / lattice | confirmed | N112: "reachable sets; ... lattice search" |
| robo_ledger | reachability tree | N112: reachability tree of motion primitives | confirmed | N112: "reachable sets; motion primitives" |
| robo_ledger | reﬂex vertex | N270: reflex vertices define the visibility graph | confirmed | N270: "shortest-path roadmap (visibility graph)" |
| robo_ledger | resolution | N111: resolution of a grid or sample set | confirmed | N111: "resolution-complete" |
| robo_ledger | resolution completeness | N111: resolution completeness | confirmed | N111: "resolution-complete" |
| robo_ledger | resultant, force | N220: net (resultant) force on a rigid body | confirmed | plan §4 Newtonian mechanics "F = ma"; N220 |
| robo_ledger | resultant, moment | N220: net moment (torque) on a rigid body | confirmed | plan §4 Newtonian mechanics "torque"; N220 "Euler's equation" |
| robo_ledger | reward space | N53: multi-objective reward spaces and Pareto optimality | confirmed | N53: "multi-objective optimisation and Pareto-optimal plans" |
| robo_ledger | risk, conditional Bayes’ | N53: Bayes risk = expected cost under the posterior | confirmed | N53: "Bayesian decision making with observations" |
| robo_ledger | roadmap, general requirements | N111: roadmap requirements (accessibility, connectivity) | add | roadmap requirements: accessibility and connectivity [robotics] → RO-05, extend N111 (merges existing robo_adds: roadmap properties: accessibility and connectivity) |
| robo_ledger | robot displacement metric | N108: distance between robot configurations | confirmed | N108: "metric space: rules a distance must follow; distances on angles" |
| robo_ledger | robot-robot collisions | N271: robot-robot collisions in multi-robot planning | confirmed | N271: "multi-robot planning" |
| robo_ledger | sample point of a cell | N270: sample point of a cell in cell decomposition | confirmed | N270: "vertical cell decomposition" |
| robo_ledger | sample sequence | N111: sample sequence for sampling-based planners | confirmed | N108: "uniform random samples of rotations and directions"; N111 |
| robo_ledger | sample set | N111: sample set | confirmed | N108: "uniform random samples"; N111 |
| robo_ledger | sampling-based planning, philosophy | N111: why sample instead of build the obstacle region exactly | confirmed | N111: "probabilistic ... roadmaps; probabilistically complete planners" |
| robo_ledger | sampling-based planning, under diﬀerential constraints | N112: kinodynamic sampling-based planning | confirmed | N112: "kinodynamic RRT" |
| robo_ledger | sampling-based roadmap, basic method | N111: basic PRM | confirmed | N111: "probabilistic ... roadmaps" |
| robo_ledger | sampling-based roadmap, preprocessing phase | N111: PRM preprocessing (build) phase | confirmed | N111: "probabilistic ... roadmaps" |
| robo_ledger | sampling-based roadmap, query phase | N111: PRM query phase | confirmed | N111: "probabilistic ... roadmaps" |
| robo_ledger | sampling-based roadmaps, under diﬀerential constraints | N185: roadmap edges checked against a controller (PRM-RL) / kinodynamic roadmaps | confirmed | N185: "roadmap edges kept only if the RL policy can drive them (PRM-RL)" |
| robo_ledger | scalarization | N53: scalarization of multi-objective costs | confirmed | N53: "multi-objective optimisation" |
| robo_ledger | search algorithms, adaptation to continuous spaces | N106: grid search over continuous C-space | confirmed | N106: "DP with interpolation on continuous spaces" |
| robo_ledger | search algorithms, under diﬀerential constraints | N113: search with motion primitives (hybrid A*, lattices N114) | confirmed | N113: "Hybrid A*"; N114 "State-lattice planning" |
| robo_ledger | search algorithms, uniﬁed view (see backward search see also bidirectional search see also forward search) | N105: unified view of forward, backward and bidirectional search | confirmed | N105: "backward and bidirectional search" |
| robo_ledger | searching an environment | N181: searching/exploring an environment | confirmed | re-cite N107: "bug algorithms in unknown spaces"; N181 exploration |
| robo_ledger | second-order diﬀerential drive | N67: kinematic vs dynamic (acceleration-input) vehicle models | confirmed | N67: "Kinematic vs dynamic model" |
| robo_ledger | second-order unicycle | N67: kinematic vs dynamic (acceleration-input) vehicle models | confirmed | N67: "Kinematic vs dynamic model" |
| robo_ledger | security plan | N54: security (minimax) plan | confirmed | N54: "minimax and saddle points" |
| robo_ledger | security strategy | N54: security strategy = minimax | confirmed | N54: "minimax" |
| robo_ledger | security strategy, randomized | N54: randomized security strategy = mixed minimax | confirmed | N54: "mixed strategies" |
| robo_ledger | sensor feedback | N77: feedback from sensor readings via information state | confirmed | N77: "information state: the history of actions and readings" |
| robo_ledger | sensor observation | N63: measurement/observation | confirmed | N63: "measurements and controls" |
| robo_ledger | sensors, discrete | N77: discrete sensor models | confirmed | N77: "state transition and measurement probabilities; set-valued (nondeterministic) information state" |
| robo_ledger | sequential game, Markov assumption | N7: Markov assumption | confirmed | N7: "MDP dynamics"; plan §4 "Markov property / Markov assumption" |
| robo_ledger | sequential game, more than two players | N54: nonzero-sum games with many players | confirmed | N54: "nonzero-sum games and Nash equilibrium" |
| robo_ledger | simple-car model, with nature | N68: car motion with noise | confirmed | N68: "velocity motion model" |
| robo_ledger | simulation-based methods | N16: simulation-based (Monte Carlo) evaluation | confirmed | N16: "evaluating a plan by simulation" |
| robo_ledger | simultaneous localization and mapping (see SLAM, 656) | N100: SLAM | confirmed | N100: "online SLAM vs full SLAM" |
| robo_ledger | smooth diﬀerential drive | N67: kinematic vs dynamic vehicle models | confirmed | N67: "Kinematic vs dynamic model" |
| robo_ledger | solid representation | N71: solid models from half-planes and meshes | confirmed | N71: "obstacles as polygons built from half-planes" |
| robo_ledger | solution trajectory | N112: solution trajectory of an ODE (plan§4 ODEs and vector fields) | confirmed | plan §4 "ODEs and vector fields" |
| robo_ledger | special Euclidean group | N64: SE(2)/SE(3) as rigid-body transforms (plan§4) | confirmed | plan §4 Rigid-body transforms: "SE(2)/SE(3)" |
| robo_ledger | special orthogonal group | N65: rotation matrices SO(2)/SO(3) (plan§4 rigid-body transforms) | confirmed | N65: "Rotation matrix ... inverse = transpose" |
| robo_ledger | speedometer | N86: wheel speed sensing / odometry | confirmed | N86: "Wheel odometry from encoders" |
| robo_ledger | spherical coordinates | N91: range-azimuth-elevation (spherical) coordinates | confirmed | N91: "Range-azimuth-elevation sensor model" |
| robo_ledger | spherical linear interpolation | N202: slerp | confirmed | N202: "Interpolating orientation (slerp)" |
| robo_ledger | stability of a system | N117: stability of dynamical systems (plan§4) | confirmed | plan §4 "Stability of dynamical systems" |
| robo_ledger | stable conﬁguration space | N292: stable configurations in manipulation planning (transit/transfer) | confirmed | N292: "transit and transfer moves" |
| robo_ledger | star algorithm | N73: computing C-obstacles of polygons (Minkowski sum) | confirmed | N73: "Minkowski sum: growing obstacles by the robot's shape" |
| robo_ledger | state trajectory | N112: state trajectory | confirmed | plan §4 "ODEs and vector fields" |
| robo_ledger | state transition matrix | N7: transition matrix (plan§4 Markov chains) | confirmed | plan §4 Markov chains: "transition matrix" |
| robo_ledger | state-space discretization | N114: state-space discretization / lattices | confirmed | N114: "State-lattice planning" |
| robo_ledger | stationary cost-to-go function | N11: stationary optimal value / cost-to-go | confirmed | N11: "optimal value functions"; N14 "cost-to-go" |
| robo_ledger | stationary diﬀerential equations | N112: autonomous ODEs (plan§4 ODEs and vector fields) | confirmed | plan §4 "ODEs and vector fields" |
| robo_ledger | steering problem | N112: steering problem solved by Dubins/Reeds-Shepp curves | confirmed | N112: "Dubins and Reeds-Shepp shortest car paths" |
| robo_ledger | sticking | N288: sticking vs sliding contact | confirmed | N288: "rolling, sliding, breaking free; Coulomb friction and the friction cone" |
| robo_ledger | stochastic iterative algorithm | N3: stochastic approximation (Robbins-Monro) | confirmed | N3: "step-size conditions (Robbins-Monro)" |
| robo_ledger | stochastic shortest-path problem | N8: episodic shortest-path MDP | confirmed | N8: "episodic vs continuing tasks" |
| robo_ledger | strategy | N54: strategy | confirmed | N54: "mixed strategies" |
| robo_ledger | suﬃcient information mapping | N78: belief as a sufficient summary of history | confirmed | N78: "belief as the probabilistic information state" |
| robo_ledger | suﬃcient statistic | N78: belief as a sufficient statistic | confirmed | N78: "belief as the probabilistic information state" (a sufficient summary of the history) |
| robo_ledger | switching boundary | N203: bang-bang switching in time-optimal scaling | out-of-scope | LaValle §8.3.1 (p.388): switching boundaries of piecewise-smooth vector fields under Filippov's condition; existence theory for discontinuous ODEs, proof-level |
| robo_ledger | TangentBug | N107: bug algorithms | confirmed | N107: "bug algorithms in unknown spaces" (TangentBug is one bug algorithm) |
| robo_ledger | temporal diﬀerence | N19: temporal difference | confirmed | N19: "TD(0) and the TD error" |
| robo_ledger | temporal logic | N197: formal methods named | confirmed | N197: "Formal methods and shields" |
| robo_ledger | termination action | N8: terminating episodes | out-of-scope | LaValle §2.3.2 book-specific device: an extra action u_T that ends a plan of unspecified length; the idea is the terminal state of N8 "episodes" |
| robo_ledger | time-invariant | N64: time-invariant systems (plan§4 State-space models) | add | linear time-invariant (LTI) systems: time-invariance, linearity and superposition [control] → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4) (merges existing ctrl_adds: Response of linear time-invariant systems) |
| robo_ledger | time-varying motion planning, bounded speed | N271: velocity tuning with bounded speed | confirmed | N271: "time-varying obstacles and velocity tuning" |
| robo_ledger | time-varying motion planning, unbounded speed | N271: time-varying planning with unbounded speed | confirmed | N271: "time-varying obstacles and velocity tuning" |
| robo_ledger | tire skidding | N251: tyre skidding / friction limit | confirmed | N251: "Tyre force saturation and friction limit" |
| robo_ledger | trajectory planning, path-constrained | N203: path-constrained (time-scaling) trajectory planning | confirmed | N203: "Time-optimal time scaling under torque limits (phase plane)" |
| robo_ledger | transcription | N116: direct transcription / collocation | confirmed | N116: "Direct methods: single shooting, multiple shooting, collocation" |
| robo_ledger | transformations, 2D rigid body | N64: 2D rigid transforms (plan§4 rigid-body transforms) | confirmed | plan §4 Rigid-body transforms: "rotate + translate, homogeneous matrix, SE(2)/SE(3)" |
| robo_ledger | transformations, 3D rigid body | N65: 3D rigid transforms (plan§4 rigid-body transforms) | confirmed | plan §4 Rigid-body transforms: "SE(2)/SE(3)" |
| robo_ledger | transition conﬁgurations (mode change) | N292: mode changes between transit and transfer | confirmed | N292: "transit and transfer moves" |
| robo_ledger | triangle inequality | N108: triangle inequality in metric rules | confirmed | N108: "metric space: rules a distance must follow" |
| robo_ledger | tricycle | N67: car-like (tricycle/bicycle) kinematics | confirmed | N67: "Kinematic bicycle model (front wheel steers, rear wheel follows)" |
| robo_ledger | two-point boundary value problem | N116: two-point boundary value problem solved by shooting | confirmed | N116: "single shooting, multiple shooting, collocation"; N112 "Dubins and Reeds-Shepp shortest car paths" |
| robo_ledger | uncertainty, brief overview | N63: sources of uncertainty | confirmed | N63: "sources of uncertainty in robots" |
| robo_ledger | uncertainty, due to partial predictability | N63: uncertainty in actions | confirmed | N63: "uncertainty in actions vs in perception" |
| robo_ledger | uncertainty, due to sensing | N63: uncertainty in perception | confirmed | N63: "uncertainty in actions vs in perception" |
| robo_ledger | underactuated system | N221: underactuation | confirmed | N221: "underactuation: tilt to move" |
| robo_ledger | unit quaternions | plan§4 3D rotations: unit quaternions | confirmed | plan §4 "3D rotations: Euler angles and quaternions" |
| robo_ledger | upper value of a game | N54: upper value of a game | confirmed | N54: "minimax and saddle points" |
| robo_ledger | vector ﬁeld | N112: vector fields (plan§4 ODEs and vector fields) | confirmed | plan §4 "ODEs and vector fields: following the arrows" |
| robo_ledger | vector ﬁeld, equilibrium point | N117: equilibrium points (plan§4 Stability of dynamical systems) | confirmed | plan §4 Stability of dynamical systems: "equilibria" |
| robo_ledger | velocity ﬁeld | N112: velocity field (plan§4 ODEs and vector fields) | confirmed | plan §4 "ODEs and vector fields" |
| robo_ledger | velocity-tuning method | N271: velocity tuning | confirmed | N271: "velocity tuning" |
| robo_ledger | VisBug | N107: bug algorithms | confirmed | N107: "bug algorithms in unknown spaces" |
| robo_ledger | wall following | N107: wall following in bug algorithms | confirmed | N107: "bug algorithms in unknown spaces" (bugs follow walls) |
| robo_ledger | way point | N130: waypoints | confirmed | N130: "waypoint following" |
| robo_ledger | weighted-region problem | N98: region-dependent travel costs via costmaps | confirmed | N98: "keep-out and speed zones" (region-dependent cost) |
| robo_ledger | world | N63: world / environment | confirmed | N72: "basic motion planning problem (piano mover's)" (the world the robot moves in) |
| robo_ledger | End-effector | N276: end-effector | confirmed | N276: "hand pose" (hand = end-effector) |
| robo_ledger | Dynamics | N281: dynamics | confirmed | N281: "Manipulator equation" |
| robo_ledger | Compliance | N287: compliance | confirmed | N287: "Impedance control: behave like a virtual spring and damper" |
| robo_ledger | Mapping from one frame to another [subsection] | N65: mapping between frames | confirmed | N65: "using it to change frames" |
| robo_ledger | Singularity | N278: singularity (and gimbal lock in plan§4 3D rotations) | confirmed | N278: "Singularities" |
| robo_ledger | Differential Kinematics | N277: differential kinematics | confirmed | N277: "Manipulator Jacobian ...: joint speeds to hand twist" |
| robo_ledger | Generalized Position | N72: generalized position (configuration) | confirmed | N72: "configuration space (C-space)" |
| robo_ledger | Forward Kinematics of a simple robot arm [subsection] | N69: FK of a simple arm | confirmed | N69: "Forward kinematics of an open chain" |
| robo_ledger | Solvability [subsection] | N279: IK solvability | confirmed | N279: "none, one, many or infinitely many answers" |
| robo_ledger | Differential Kinematics [section] | N277: differential kinematics | confirmed | N277: "Manipulator Jacobian"; N280 "Differential (inverse velocity) IK" |
| robo_ledger | Forward Differential Kinematics [subsection] | N277: forward differential kinematics | confirmed | N277: "joint speeds to hand twist" |
| robo_ledger | Forward Kinematics of a Differential Wheeled Robot [subsection] | N64: diff-drive forward kinematics | confirmed | N64: "Differential drive: wheel speeds to (v, ω)" |
| robo_ledger | Non-holonomic | N64: nonholonomic | confirmed | N64: "Nonholonomic constraint" |
| robo_ledger | From Forward Kinematics to Odometry [subsubsection] | N68: odometry from forward kinematics | confirmed | N68: "Wheel odometry"; N86 "Wheel odometry from encoders" |
| robo_ledger | Inverse Kinematics using Feedback Control [subsection] | N280: IK by feedback on the error | confirmed | N280: "Jacobian-transpose IK; Differential (inverse velocity) IK ... tracking a moving target" |
| robo_ledger | Damped Least-Squares Method | N280: damped least squares | confirmed | N280: "Damped least squares IK" |
| robo_ledger | Inverse Kinematics of Mobile Robots [subsection] | N66: inverse kinematics of mobile bases | confirmed | re-cite N64: "wheel speeds to (v, ω) and back"; N66 mecanum model |
| robo_ledger | Feedback Control for Mobile Robots [subsection] | N120: feedback control for mobile robots (drive to a pose) | confirmed | N120: "Moving to a point; ... Moving to a pose" |
| robo_ledger | Generalized Force | N281: generalized force | confirmed | N281: "Manipulator equation ... = τ" |
| robo_ledger | Kineto-Statics Duality [section] | N277: kineto-statics duality (τ = Jᵀ F) | confirmed | N277: "Statics: joint torques that hold a hand force, τ = Jᵀ F" |
| robo_ledger | Kineto-Statics Duality | N277: kineto-statics duality | confirmed | N277: "τ = Jᵀ F" |
| robo_ledger | Force interactions and compliance [section] | N287: force interaction and compliance | confirmed | N286: "Force control"; N287 "Impedance control" |
| robo_ledger | Dynamics [section] | N281: dynamics | confirmed | N281: "Manipulator equation" |
| robo_ledger | Grasping | N290: grasping | confirmed | N290: "Form closure; Force closure; Grasp matrix" |
| robo_ledger | The theory of grasping [section] | N290: grasping theory | confirmed | N290: "Form closure; Force closure; Grasp matrix" |
| robo_ledger | Grasping wrench space | N291: grasp wrench space | confirmed | N291: "Grasp quality: the largest push a grasp can resist" |
| robo_ledger | Actuators | N283: actuators | confirmed | N283: "Motors, gearing" |
| robo_ledger | Proprioception vs. Exteroception [subsection] | N142: proprioception vs exteroception | confirmed | N142: "proprioceptive observation design"; N143 exteroceptive |
| robo_ledger | Proprioception | N142: proprioception | confirmed | N142: "proprioceptive observation design" |
| robo_ledger | Exteroception | N143: exteroception | confirmed | N143: "height samples, scandots, depth and laser inputs" |
| robo_ledger | Measuring pressure or touch [subsection] | N294: pressure and touch sensing | confirmed | N294: "Tactile sensing on hands, feet and body" |
| robo_ledger | Artificial skin | N294: artificial skin (tactile) | confirmed | N294: "Tactile sensing on hands, feet and body" |
| robo_ledger | Artificial skins for robotics [subsection] | N294: artificial skins | confirmed | N294: "Tactile sensing on hands, feet and body" |
| robo_ledger | Laser range finder | N91: laser range finder | confirmed | N91: "How LiDAR works: time of flight" |
| robo_ledger | Laser Range Scanners | N91: laser range scanners | confirmed | N91: "How LiDAR works: time of flight, spinning vs solid-state" |
| robo_ledger | Time-of-flight [subsection] | N91: time of flight | confirmed | N91: "time of flight"; N90 "time of flight" |
| robo_ledger | Sensors to sense global pose [section] | N85: global pose sensors (GNSS) | confirmed | N85: "GNSS/GPS basics" |
| robo_ledger | Edge detection [subsubsection] | N227: edge detection (gradient filters) | confirmed | N227: "smoothing and gradient filters"; §5 DL-042 "edges as brightness changes" |
| robo_ledger | Difference of Gaussians [subsubsection] | N228: difference of Gaussians (scale space) | confirmed | N228: "Scale-space blobs, descriptors and SIFT" (DoG finds the blobs) |
| robo_ledger | Difference of Gaussians (DoG) | N228: difference of Gaussians | confirmed | N228: "Scale-space blobs, descriptors and SIFT" |
| robo_ledger | RANSAC: Random Sample and Consensus [subsection] | N229: RANSAC | confirmed | N229: "RANSAC" |
| robo_ledger | Random Sample and Consensus | N229: random sample consensus | confirmed | N229: "RANSAC" |
| robo_ledger | Scale-invariant feature transforms [section] | N228: scale-invariant features | confirmed | N228: "SIFT" |
| robo_ledger | SURF | N228: SURF named as a faster SIFT variant | out-of-scope | SURF is a speed variant of SIFT (Correll p.170 names it only); the concept is N228 SIFT, and robotics uses ORB (N228, ORB-SLAM N236) |
| robo_ledger | Object Recognition using scale-invariant features [subsection] | N228: object recognition by feature matching | confirmed | N228: "Matching descriptors (nearest neighbour, ratio test, mutual check)" |
| robo_ledger | Convolutional Networks beyond 2D image data [subsection] | N162: 1D (temporal) convolution | confirmed | N162: "temporal convolution" |
| robo_ledger | FSM | N130: FSM | confirmed | N130: "finite state machines" |
| robo_ledger | Inter-process communication | N127: inter-process communication (topics, services) | confirmed | N127: "nodes, topics, services, actions" |
| robo_ledger | IPC | N127: IPC | confirmed | N127: "nodes, topics, services, actions" |
| robo_ledger | Robot Operating System | N127: ROS | confirmed | N127: "ROS 2" |
| robo_ledger | Node Definition and Status [subsection] | N130: BT node status | confirmed | N130: "Behaviour trees (sequence, fallback, decorator, tick)" |
| robo_ledger | Node Types [subsection] | N130: BT node types | confirmed | N130: "sequence, fallback, decorator" |
| robo_ledger | Behavior Tree Execution [subsection] | N130: BT execution (tick) | confirmed | N130: "tick" |
| robo_ledger | RGB-D mapping: dense mapping of surfaces [section] | N97: dense surface mapping (TSDF/surfels named) | confirmed | N97: "Signed-distance (TSDF) maps; surfel maps named" |
| robo_ledger | Path | N104: path | confirmed | N104: "Dijkstra's shortest-path algorithm" |
| robo_ledger | A* Shortest Path Algorithm | N105: A* | confirmed | N105: "A* search" |
| robo_ledger | Sampling-based path planning [section] | N110: sampling-based planning | confirmed | N110: "rapidly-exploring random tree" |
| robo_ledger | Planning at different length scales [section] | N126: planning at different scales (layers) | confirmed | re-cite N131: "Classical stack: global planner + local planner" |
| robo_ledger | Choosing the right grasp [section] | N291: choosing a grasp | confirmed | N291: "Grasp selection" |
| robo_ledger | Finding good grasps for simple grippers [subsection] | N291: grasps for simple grippers (antipodal) | confirmed | N291: "antipodal grasps" |
| robo_ledger | Finding good grasps for multi-fingered hands [subsection] | N291: grasps for multi-fingered hands | confirmed | N291: "Analytic vs data-driven grasp synthesis"; N290 "Force closure" |
| robo_ledger | Pick and place [section] | N292: pick and place (transit and transfer) | confirmed | N292: "transit and transfer moves" |
| robo_ledger | TAMP | N293: TAMP | confirmed | N293: "task and motion planning" |
| robo_ledger | Peg-in-hole problems [section] | N327: peg-in-hole | confirmed | N327: "insertion and assembly" |
| robo_ledger | Peg-in-hole | N327: peg-in-hole | confirmed | N327: "insertion and assembly" |
| robo_ledger | Uncertainty in Robotics as Random Variable [section] | N63: uncertainty as random variables | confirmed | N63: "keep a full distribution"; §5 MA-020 random variables |
| robo_ledger | Error Propagation [section] | plan§4 Linear transforms of a Gaussian: error propagation (A Σ Aᵀ; N81 for the Jacobian form) | confirmed | plan §4 Linear transforms of a Gaussian: "covariance A Sigma A^T" |
| robo_ledger | Optimal Sensor Fusion [section] | N80: optimal sensor fusion | confirmed | N80: "Kalman filter and the Kalman gain"; plan §4 "Product of two Gaussians" |
| robo_ledger | Innovation | N80: innovation (measurement residual) | confirmed | N80: "Kalman filter and the Kalman gain" (innovation = measurement minus prediction) |
| robo_ledger | Perception step (Kalman filter) | N80: update step | confirmed | N80: "Kalman filter"; N78 "predict and update steps" |
| robo_ledger | Prediction step (Kalman filter) | N80: prediction step | confirmed | N80: "Kalman filter"; N78 "predict and update steps" |
| robo_ledger | Perception Update (Markov Localization) | N94: perception update | confirmed | N94: "Markov localization" |
| robo_ledger | Action Update (Markov Localization) | N94: action update | confirmed | N94: "Markov localization" |
| robo_ledger | The Covariance Matrix [section] | N261: SLAM covariance matrix | confirmed | N261: "EKF SLAM with known correspondence" |
| robo_ledger | Algorithm [subsection] | N261: EKF SLAM algorithm | confirmed | N261: "EKF SLAM" |
| robo_ledger | Update [subsubsection] | N261: EKF SLAM update | confirmed | N261: "EKF SLAM" |
| robo_ledger | Multiple Sensors [subsection] | N86: multiple sensors in one filter | confirmed | N86: "EKF fusion of IMU, wheels and GNSS" |
| vis_ledger | arrowhead matrix | RO 235 (sparsity and Schur complement in bundle adjustment) | confirmed | N235: "Sparsity and the Schur complement in bundle adjustment" (arrowhead = that sparsity pattern) |
| vis_ledger | Bayesian inference | MA-018; RO 78 | confirmed | MA-018 (Bayes' theorem); N78 "Bayes filter predict and update steps" |
| vis_ledger | global positioning system | RO 85 | confirmed | N85: "GNSS/GPS basics" |
| vis_ledger | Hermite basis function | RO 201 | confirmed | N201: "Cubic and quintic polynomials from boundary conditions" (Hermite basis = cubic from end positions and slopes) |
| vis_ledger | interoceptive | RO 142 (proprioceptive = interoceptive sensing) | confirmed | N142: "proprioceptive observation design" (interoceptive = proprioceptive) |
| vis_ledger | linear-Gaussian | RO 80 | confirmed | N80: "linear Gaussian system" |
| vis_ledger | M-estimation | RO 235 (robust cost functions, M-estimators) | confirmed | N235: "Robust cost functions (Huber, Cauchy)"; plan §4 "robust losses (IRLS)" |
| vis_ledger | maximum a posteriori | MA-072 (MAP estimate, G-1189); RO 260 | confirmed | N260: "MAP estimate of a whole map"; MA-072 |
| vis_ledger | outlier | ML-040; RO 235 | confirmed | N229: "RANSAC: fit a model despite wrong matches"; N235 robust costs |
| vis_ledger | point-cloud alignment | RO 92 | confirmed | N92: "ICP: iterative closest point; Aligning two 3D point sets" |
| vis_ledger | point-clouds | RO 91 | confirmed | N91: "Point clouds: storage and basic operations" |
| vis_ledger | Poisson’s equation | RO 84 (Poisson's kinematic equation = integrating angular velocity into orientation) | confirmed | N84: "Integrating angular velocity into orientation" (Poisson's kinematic equation) |
| vis_ledger | pose-graph relaxation | RO 101 | confirmed | N101: "pose (constraint) graph; negative log posterior as a sum of quadratic terms" |
| vis_ledger | random sample consensus | RO 229 | confirmed | N229: "RANSAC" |
| vis_ledger | sigmapoint | RO 256 | confirmed | N256: "unscented transform and sigma points" |
| vis_ledger | sigmapoint transformation | RO 256 (unscented transform) | confirmed | N256: "unscented transform and sigma points" |
| vis_ledger | simultaneous localization and mapping | RO 100 | confirmed | N100: "online SLAM vs full SLAM" |
| vis_ledger | sliding-window filter | RO 263 | confirmed | N263: "Filtering vs optimisation (sliding window)" |
| vis_ledger | Chi-squared distribution and Mahalanobis distance (2nd-ed contents) | MA-045 (chi-square distribution); new MA: Mahalanobis distance (gating); RO 178 | confirmed | plan §4 "Mahalanobis distance"; N178 "Mahalanobis gating"; MA-045 (chi-square) |
| vis_ledger | Fisher information matrix for a multivariate Gaussian (2nd-ed contents) | RL 38 (Fisher information) | confirmed | N38: "natural gradient and Fisher information" |
| vis_ledger | 3D reconstruction | RO 233 (triangulation); RO 235 (structure from motion) | confirmed | N233: "Triangulation"; N235 "Structure from motion" |
| vis_ledger | 3D reconstruction, pipeline | RO 235 | confirmed | N235: "Structure from motion: cameras and points from many photos" |
| vis_ledger | alignment of shapes | RO 92 (point-set alignment by SVD / Procrustes) | confirmed | N92: "Aligning two 3D point sets (SVD / Kabsch solution)" |
| vis_ledger | approximate inference | RO 82 (sampling-based approximate inference) | confirmed | N82: "belief as a cloud of weighted samples" |
| vis_ledger | articulated models | RO 69 (kinematic chains and trees) | confirmed | N69: "kinematic trees (branching bodies such as humanoids)" |
| vis_ledger | body pose estimation | RB 317; RB 337 (human pose from video) | confirmed | N317: "Human motion data: motion capture, video, body models (SMPL)"; N337 "hand and object poses from video" |
| vis_ledger | Brownian motion | RO 83 (bias random walk); add white-noise-psd for the continuous form | add | white noise, random walks and Brownian motion (continuous noise intensity to a discrete Q) [robotics] → RO-03, section in N83 (merges existing vis_adds: White noise and its power spectral density; random walks) |
| vis_ledger | calibration target, planar | RO 89 | confirmed | N89: "Camera calibration with a checkerboard" |
| vis_ledger | chain model, directed | RO 77 | confirmed | N77: "hidden Markov model / dynamic Bayes network" |
| vis_ledger | Chapman-Kolmogorov equation | RO 78 (prediction step) | confirmed | N78: "Bayes filter predict" (the predict step is the Chapman-Kolmogorov equation) |
| vis_ledger | condensation algorithm | RO 82 (CONDENSATION = particle filter) | confirmed | N82: "particle filter" (CONDENSATION = particle filter) |
| vis_ledger | corner detection, SIFT | RO 228 | confirmed | N228: "SIFT" |
| vis_ledger | directed graphical model, chain | RO 77 | confirmed | N77: "hidden Markov model / dynamic Bayes network" |
| vis_ledger | essential matrix, decomposition | RO 233 (recovering R and t from E) | confirmed | N233: "Recovering R and t from E; the four-solution check" |
| vis_ledger | Euclidean transformation, learning | RO 92 (fitting a rigid transform to matched points) | confirmed | N92: "Aligning two 3D point sets (SVD / Kabsch solution)" |
| vis_ledger | exterior orientation problem | RO 233 (PnP) | confirmed | N233: "PnP: camera pose from known 3D points" |
| vis_ledger | exterior orientation problem, 3D scene | RO 233 | confirmed | N233: "PnP: camera pose from known 3D points" |
| vis_ledger | exterior orientation problem, planar scene | RO 233; RO 229 (pose from a plane) | confirmed | N233: "PnP"; N229 "Homography: the map between two views of a plane" |
| vis_ledger | extrinsic parameters, estimation | RO 233 | confirmed | N233: "PnP: camera pose from known 3D points" |
| vis_ledger | extrinsic parameters, learning | RO 233 | confirmed | N233: "PnP: camera pose from known 3D points" |
| vis_ledger | extrinsic parameters, learning, 3D scene | RO 233 | confirmed | N233: "PnP: camera pose from known 3D points" |
| vis_ledger | extrinsic parameters, learning, planar scene | RO 233 | confirmed | N233: "PnP"; N229 "Homography" |
| vis_ledger | feature, tracking | RO 230 (KLT tracking) | confirmed | N230: "Pyramidal KLT tracker" |
| vis_ledger | feature descriptor, histogram | RO 228 | confirmed | N228: "descriptors and SIFT" |
| vis_ledger | feature detector, SIFT detector | RO 228 | confirmed | N228: "Scale-space blobs, descriptors and SIFT" |
| vis_ledger | graphical model, chain | RO 77 | confirmed | N77: "hidden Markov model / dynamic Bayes network" |
| vis_ledger | HMM | RO 77 | confirmed | N77: "hidden Markov model" |
| vis_ledger | inference, marginal posterior distribution | MA-014; RO 78 | confirmed | MA-014 (joint, marginal, conditional); N78 |
| vis_ledger | inference, sampling from posterior | RO 82 | confirmed | N82: "belief as a cloud of weighted samples" |
| vis_ledger | interest point detection | RO 227 | confirmed | N227: "Point features (keypoints)" |
| vis_ledger | interest point detection, SIFT | RO 228 | confirmed | N228: "SIFT" |
| vis_ledger | intrinsic parameters, learning | RO 89 | confirmed | N89: "Camera calibration with a checkerboard" |
| vis_ledger | intrinsic parameters, learning, from 3D object | RO 89 | confirmed | N89: "Camera calibration"; "Direct linear transform (DLT)" |
| vis_ledger | intrinsic parameters, learning, from a plane | RO 89 | confirmed | N89: "Camera calibration with a checkerboard" |
| vis_ledger | Kalman filter, temporal and measurement models | RO 80 | confirmed | N80: "linear Gaussian system; Kalman filter" |
| vis_ledger | linear algebra, common problems | MA-060; RO 89; RO 92 | confirmed | MA-060 (SVD); N89 "Solving A x = 0 with the SVD"; N92 "SVD / Kabsch" |
| vis_ledger | M-estimator | RO 235 (robust costs, M-estimators) | confirmed | N235: "Robust cost functions (Huber, Cauchy)" |
| vis_ledger | marginal posterior distribution | MA-014; RO 78 | confirmed | MA-014; N78 "Bayes filter" |
| vis_ledger | measurement incorporation step | RO 78 (update step) | confirmed | N78: "Bayes filter predict and update steps" |
| vis_ledger | minimum direction problem | new short section: Least-squares solution of Ax = 0 by the SVD (RO 89) | confirmed | N89: "Solving A x = 0 with the SVD (last right singular vector)" |
| vis_ledger | MonoSLAM | RO 261 (EKF SLAM); RO 236 (visual SLAM) | confirmed | N261: "EKF SLAM"; N236 "VO vs visual SLAM" (MonoSLAM = EKF visual SLAM) |
| vis_ledger | multi-view reconstruction | RO 235 | confirmed | N235: "Structure from motion; Bundle adjustment" |
| vis_ledger | multiple view geometry | RO 232 | confirmed | N232: "Epipolar geometry" |
| vis_ledger | nonlinear optimization, trust-region methods | RL 38 (trust region); new MA short section: Levenberg-Marquardt | confirmed | N38: "trust region"; N235 "Levenberg-Marquardt" |
| vis_ledger | offset parameter | RO 88 (principal-point offset) | confirmed | N88: "Intrinsics K: focal length, principal point" |
| vis_ledger | optimization, trust-region methods | RL 38; new MA short section: Levenberg-Marquardt | confirmed | N38: "trust region"; N235 "Levenberg-Marquardt" |
| vis_ledger | orthogonal Procrustes problem | RO 92 (Kabsch / orthogonal Procrustes) | confirmed | N92: "Aligning two 3D point sets (SVD / Kabsch solution)" |
| vis_ledger | outlier | ML-040; RO 229 | confirmed | N229: "RANSAC: fit a model despite wrong matches" |
| vis_ledger | perspective-n-point problem | RO 233 | confirmed | N233: "PnP" |
| vis_ledger | photoreceptor spacing | RO 88 (focal length in pixels from pixel size) | confirmed | N88: "Intrinsics K: focal length, principal point, pixel size" |
| vis_ledger | preprocessing | RO 227 | confirmed | N227: "Image filtering: smoothing and gradient filters" |
| vis_ledger | Prewitt operators | RO 227 (gradient filters) | confirmed | N227: "gradient filters" |
| vis_ledger | Procrustes analysis | RO 92 | confirmed | N92: "SVD / Kabsch solution" |
| vis_ledger | Procrustes problem | RO 92 | confirmed | N92: "SVD / Kabsch solution" |
| vis_ledger | projective transformation | RO 229 | confirmed | N229: "Homography" |
| vis_ledger | projective transformation, fitting | RO 229; RO 89 (DLT) | confirmed | N229: "Homography"; N89 "Direct linear transform (DLT)" |
| vis_ledger | projective transformation, properties | RO 229 | confirmed | N229: "Homography: the map between two views of a plane" |
| vis_ledger | random sample consensus | RO 229 | confirmed | N229: "RANSAC" |
| vis_ledger | reconstruction | RO 233; RO 235 | confirmed | N233: "Triangulation"; N235 "Structure from motion" |
| vis_ledger | reconstruction, multi-view | RO 235 | confirmed | N235: "Structure from motion" |
| vis_ledger | reconstruction, two view | RO 233 | confirmed | N233: "Recovering R and t from E; Triangulation" |
| vis_ledger | reconstruction pipeline | RO 235 | confirmed | N235: "Structure from motion; Bundle adjustment" |
| vis_ledger | region descriptor, histogram | RO 228 | confirmed | N228: "descriptors and SIFT" |
| vis_ledger | robust learning, RANSAC | RO 229 | confirmed | N229: "RANSAC" |
| vis_ledger | sampling from posterior | RO 82 | confirmed | N82: "belief as a cloud of weighted samples" |
| vis_ledger | scale invariant feature transform | RO 228 | confirmed | N228: "SIFT" |
| vis_ledger | simultaneous localization and mapping | RO 100 | confirmed | N100: "online SLAM vs full SLAM" |
| vis_ledger | Sobel operator | RO 227 (gradient filters) | confirmed | N227: "gradient filters" (Sobel is one) |
| vis_ledger | sparse stereo vision | RO 233 (triangulating matched features) | confirmed | N233: "Triangulation" |
| vis_ledger | stereo vision, dynamic programming | RO 90 (matching along rows) | add | stereo matching costs and optimisation along a scanline (SSD/SAD/NCC, cost volume, dynamic programming / semi-global matching) [vision] → RO-03, section in N90 (merges existing vis_adds: Stereo and patch matching (extend with scanline DP/SGM)) |
| vis_ledger | stereo vision, sparse | RO 233 | confirmed | N233: "Triangulation" |
| vis_ledger | tracking, condensation algorithm | RO 82 | confirmed | N82: "particle filter" |
| vis_ledger | tracking, features | RO 230 | confirmed | N230: "Pyramidal KLT tracker" |
| vis_ledger | tracking, particle filtering | RO 82 | confirmed | N82: "particle filter" |
| vis_ledger | tracking, through clutter | RO 259 (data association in clutter) | confirmed | N259: "maximum-likelihood data association with gating; multi-hypothesis tracking" |
| vis_ledger | transformation, between images | RO 229 | confirmed | N229: "Homography" |
| vis_ledger | transformation, learning, Euclidean | RO 92 | confirmed | N92: "Aligning two 3D point sets" |
| vis_ledger | transformation, learning, homography | RO 229 | confirmed | N229: "Homography" |
| vis_ledger | transformation, learning, projective | RO 229 | confirmed | N229: "Homography" |
| vis_ledger | transformation, projective | RO 229 | confirmed | N229: "Homography" |
| vis_ledger | transformation, robust learning | RO 229 | confirmed | N229: "RANSAC" |
| vis_ledger | trust-region methods | RL 38; new MA short section: Levenberg-Marquardt | confirmed | N38: "trust region"; N235 "Levenberg-Marquardt" |
| vis_ledger | 3D alignment | RO 92 (aligning 3D point sets, Kabsch / Procrustes) | confirmed | N92: "Aligning two 3D point sets (SVD / Kabsch solution)" |
| vis_ledger | 3D alignment, absolute orientation | RO 92 (aligning 3D point sets, Kabsch / Procrustes) | confirmed | N92: "Aligning two 3D point sets" |
| vis_ledger | 3D alignment, orthogonal Procrustes | RO 92 (aligning 3D point sets, Kabsch / Procrustes) | confirmed | N92: "SVD / Kabsch solution" |
| vis_ledger | Absolute orientation | RO 92 | confirmed | N92: "Aligning two 3D point sets" |
| vis_ledger | Active illumination | RO 90; RO 91 (structured light, time of flight, LiDAR) | confirmed | N90: "structured light and time of flight"; N91 LiDAR |
| vis_ledger | Active rangefinding | RO 90; RO 91 (structured light, time of flight, LiDAR) | confirmed | N90: "structured light and time of flight"; N91 LiDAR |
| vis_ledger | Arc length parameterization of a curve | RO 121 (distance along the path s) | confirmed | N121: "distance along the path s" |
| vis_ledger | Aspect ratio | RO 88 (pixel aspect ratio in K) | confirmed | N88: "Intrinsics K: focal length, principal point, pixel size" |
| vis_ledger | Bayesian modeling, uncertainty | MA-018; RO 63 | confirmed | MA-018; N63 "keep a full distribution" |
| vis_ledger | Category-level recognition, segmentation | RO 175 | confirmed | N175: "Semantic segmentation" |
| vis_ledger | Chained transformations | MA-054; RO 65 (chaining transforms) | confirmed | §5 MA-054 "Chaining transforms by matrix multiplication"; N65 "transform tree" |
| vis_ledger | Chirality | RO 233 (point in front of both cameras: four-solution check) | confirmed | N233: "the four-solution check" (chirality = point in front of both cameras) |
| vis_ledger | Collineation | RO 229 (collineation = homography) | confirmed | N229: "Homography" |
| vis_ledger | CONDENSATION | RO 82 | confirmed | N82: "particle filter" |
| vis_ledger | Contour, arc length parameterization | RO 121 | confirmed | N121: "distance along the path s" |
| vis_ledger | Correspondence map | RO 231 (dense flow field) | confirmed | re-cite N231: "Horn-Schunck: dense flow" |
| vis_ledger | Curve, arc length parameterization | RO 121 | confirmed | N121: "distance along the path s" |
| vis_ledger | Decimation | RO 227 (pyramids: downsampling) | confirmed | N227: "Image pyramids" |
| vis_ledger | Displaced frame difference (DFD) | RO 230; RO 234 (brightness difference = photometric error) | confirmed | N234: "photometric error"; N230 "Brightness constancy" |
| vis_ledger | Displacement field | RO 231 (dense flow field) | confirmed | re-cite N231: "dense flow" |
| vis_ledger | Edge detection, scale selection | RO 228 (scale space) | add | edge detection with scale selection (gradient magnitude, non-max suppression, hysteresis, Canny) [vision] → RO-18, section in N227 (merges existing vis_adds: Edge detection (Canny); robo_adds: Canny edge detector) |
| vis_ledger | Errors-in-variable model | RO 92 (plane fitting by the smallest eigenvector = total least squares) | add | total least squares (errors-in-variables): fit a line or plane with errors in all coordinates by the smallest eigenvector / last singular vector [maths] → MA 07-optimisation, section in the planned Nonlinear least squares Note; used by N92 plane fitting |
| vis_ledger | Essential matrix, twisted pair | RO 233 (four-solution check) | confirmed | N233: "the four-solution check" |
| vis_ledger | Estimation theory | MA-070; RO 78 | confirmed | MA-070 (maximum likelihood estimation); N78 |
| vis_ledger | Fast marching method (FMM) | RO 106 (wavefront propagation) | add | fast marching method: solve the Eikonal equation on a grid to get geodesic distance-to-goal (continuous wavefront; planner in modular ObjectNav) [robotics] → RO-05, extend N106 |
| vis_ledger | Feature descriptor, quantization | RO 236 (visual words) | confirmed | N236: "Visual place recognition with bag of words" |
| vis_ledger | Feature detection, auto-correlation | RO 227 (Harris from the auto-correlation surface) | confirmed | N227: "Harris and Shi-Tomasi corners and the structure tensor" |
| vis_ledger | Feature detection, repeatability | RO 227 (corners are easy to find again) | confirmed | N227: "why corners are easy to find again" |
| vis_ledger | Feature detection, rotation invariance | RO 228 | confirmed | N228: "SIFT" |
| vis_ledger | Feature detection, scale invariance | RO 228 | confirmed | N228: "Scale-space blobs, descriptors and SIFT" |
| vis_ledger | Feature matching, efficiency | RO 92; RO 108 (k-d trees) | confirmed | N92: "k-d tree for nearest-neighbour search" |
| vis_ledger | Feature matching, indexing structure | RO 92; RO 108 (k-d trees) | confirmed | N92: "k-d tree" |
| vis_ledger | Feature matching, strategy | RO 228 (nearest neighbour, ratio test) | confirmed | N228: "Matching descriptors (nearest neighbour, ratio test, mutual check)" |
| vis_ledger | Feature matching, verification | RO 229 (RANSAC verification) | confirmed | N229: "RANSAC" |
| vis_ledger | Feature tracking | RO 230 | confirmed | N230: "Pyramidal KLT tracker" |
| vis_ledger | Feature tracks | RO 234; RO 235 | confirmed | N234: "chaining frame-to-frame motions"; N236 tracking thread |
| vis_ledger | Feature-based alignment | RO 229 | confirmed | N229: "Homography"; "RANSAC" |
| vis_ledger | Feature-based alignment, 2D | RO 229 | confirmed | N229: "Homography" |
| vis_ledger | Feature-based alignment, 3D | RO 92 | confirmed | N92: "Aligning two 3D point sets" |
| vis_ledger | Feature-based alignment, match verification | RO 229 | confirmed | N229: "RANSAC" |
| vis_ledger | Feature-based alignment, RANSAC | RO 229 | confirmed | N229: "RANSAC" |
| vis_ledger | Feature-based alignment, robust | RO 229; RO 235 | confirmed | N229: "RANSAC"; N235 "Robust cost functions" |
| vis_ledger | Filter, directional derivative | RO 227 | confirmed | N227: "gradient filters" |
| vis_ledger | Focus of expansion (FOE) | RO 231 (ego-motion from flow: focus of expansion) | confirmed | N231: "Ego-motion and time-to-contact from flow" (the focus of expansion) |
| vis_ledger | Geometric image formation | RO 88 | confirmed | N88: "Pinhole camera" |
| vis_ledger | Geometric lens aberrations | RO 89 (lens distortion) | confirmed | N89: "Lens distortion: radial and tangential" |
| vis_ledger | Geometric primitives, normal vector | MA-051 (normal of a hyperplane); RO 92 (normals) | confirmed | MA-051 (hyperplane normal); N92 "Normals and plane fitting" |
| vis_ledger | Geometric primitives, normal vectors | MA-051 (normal of a hyperplane); RO 92 (normals) | confirmed | MA-051; N92 "Normals and plane fitting" |
| vis_ledger | Geometric primitives, planes | MA-051; RO 92 (plane fitting) | confirmed | MA-051; N92 "plane fitting" |
| vis_ledger | Geometric transformations, calibration matrix | RO 88 | confirmed | N88: "Intrinsics K" |
| vis_ledger | Geometric transformations, collineation | RO 229 | confirmed | N229: "Homography" |
| vis_ledger | Geometric transformations, homography | RO 229 | confirmed | N229: "Homography" |
| vis_ledger | Geometric transformations, perspective | RO 229 | confirmed | N229: "Homography" |
| vis_ledger | Geometric transformations, projections | RO 88 | confirmed | N88: "Camera matrix P = K [R \| t]" |
| vis_ledger | Geometric transformations, projective | RO 229 | confirmed | N229: "Homography" |
| vis_ledger | Ground control points | RO 233 (pose from known 3D points) | confirmed | N233: "PnP: camera pose from known 3D points" |
| vis_ledger | Hessian, image | RO 230 (Lucas-Kanade normal equations / structure tensor) | confirmed | N230: "Lucas-Kanade: local flow by least squares"; plan §4 "Structure tensor" |
| vis_ledger | Hessian, reduced motion | RO 235 (sparsity, Schur complement) | confirmed | N235: "Sparsity and the Schur complement" |
| vis_ledger | Hessian, sparse | RO 235 (sparsity, Schur complement) | confirmed | N235: "Sparsity and the Schur complement" |
| vis_ledger | Hierarchical motion estimation | RO 230 (pyramidal KLT) | confirmed | N230: "Pyramidal KLT tracker" |
| vis_ledger | Human motion tracking, kinematic models | RO 69 (kinematic chains) | confirmed | N69: "kinematic trees"; N317 "body models (SMPL)" |
| vis_ledger | Human motion tracking, particle filtering | RO 82 | confirmed | N82: "particle filter" |
| vis_ledger | Image alignment, feature-based | RO 229 | confirmed | N229: "Homography" |
| vis_ledger | Image alignment, intensity-based | RO 230; RO 234 (direct vs feature-based) | confirmed | N234: "Direct vs feature-based (indirect) methods: photometric error" |
| vis_ledger | Image formation, geometric | RO 88 | confirmed | N88: "Pinhole camera" |
| vis_ledger | Image stitching, homography | RO 229 | confirmed | N229: "Homography" |
| vis_ledger | Image stitching, planar perspective motion | RO 229 | confirmed | N229: "Homography" |
| vis_ledger | Implicit surface | RO 97 (signed-distance maps) | confirmed | N97: "Signed-distance (TSDF) maps" |
| vis_ledger | Incremental refinement, motion estimation | RO 230 (iterative Lucas-Kanade) | confirmed | N230: "Lucas-Kanade" |
| vis_ledger | Indexing structure | RO 92; RO 108 (k-d trees) | confirmed | N92: "k-d tree" |
| vis_ledger | Instance recognition, algorithm | RO 236 (recognising places by bag of words) | confirmed | N236: "Visual place recognition with bag of words" |
| vis_ledger | Instance recognition, geometric alignment | RO 229 | confirmed | N229: "RANSAC" |
| vis_ledger | Instance recognition, match verification | RO 229 | confirmed | N229: "RANSAC" |
| vis_ledger | Jacobian, sparse | RO 235 | confirmed | N235: "Sparsity and the Schur complement" |
| vis_ledger | Kanade–Lucas–Tomasi (KLT) tracker | RO 230 | confirmed | N230: "Pyramidal KLT tracker" |
| vis_ledger | Kernel, Sobel operator | RO 227 | confirmed | N227: "gradient filters" |
| vis_ledger | Least squares, total | RO 92 (plane fitting by the smallest eigenvector) | add | total least squares (errors-in-variables): fit a line or plane with errors in all coordinates by the smallest eigenvector / last singular vector [maths] → MA 07-optimisation, section in the planned Nonlinear least squares Note; used by N92 plane fitting |
| vis_ledger | Level sets, fast marching method | RO 106 (wavefront propagation) | add | fast marching method: solve the Eikonal equation on a grid to get geodesic distance-to-goal (continuous wavefront; planner in modular ObjectNav) [robotics] → RO-05, extend N106 |
| vis_ledger | Levenberg–Marquardt | RO 235 | confirmed | N235: "Levenberg-Marquardt" |
| vis_ledger | Line detection, RANSAC | RO 229 (RANSAC line fit) | confirmed | N229: "RANSAC" |
| vis_ledger | M-estimator | RO 235 | confirmed | N235: "Robust cost functions (Huber, Cauchy)" |
| vis_ledger | Medial axis transform (MAT) | RO 270 (maximum-clearance roadmap = medial axis) | confirmed | N270: "maximum-clearance roadmap (generalized Voronoi diagram)" |
| vis_ledger | Motion estimation, hierarchical | RO 230 (pyramidal, iterative Lucas-Kanade) | confirmed | N230: "Pyramidal KLT tracker" |
| vis_ledger | Motion estimation, incremental refinement | RO 230 (pyramidal, iterative Lucas-Kanade) | confirmed | N230: "Lucas-Kanade" |
| vis_ledger | Motion estimation, learning | RO 231 (learned optical flow) | confirmed | N231: "Learned optical flow" |
| vis_ledger | Motion estimation, patch-based | RO 230 | confirmed | N230: "Lucas-Kanade: local flow by least squares in a window" |
| vis_ledger | Motion estimation, translational | RO 230 | confirmed | N230: "Lucas-Kanade" |
| vis_ledger | Motion stereo | RO 233 (stereo from a moving camera) | confirmed | N233: "Triangulation"; N234 "Monocular vs stereo VO" |
| vis_ledger | Multiple hypothesis tracking | RO 259 | confirmed | N259: "multi-hypothesis tracking" |
| vis_ledger | Multiresolution representation | RO 227 | confirmed | N227: "Image pyramids (coarse-to-fine)" |
| vis_ledger | Noise | RO 63 (noise in sensing) | confirmed | N63: "sources of uncertainty"; N83 "reading = truth + bias + noise" |
| vis_ledger | Omnidirectional vision systems | RO 89 (wide-angle and omnidirectional cameras) | confirmed | N89: "Wide-angle cameras: fisheye and spherical models" |
| vis_ledger | Optical triangulation | RO 90 (structured light / laser triangulation) | confirmed | N90: "Depth cameras: structured light" |
| vis_ledger | Optimal motion estimation | RO 235 (bundle adjustment as the statistically optimal estimate) | confirmed | N235: "Bundle adjustment" |
| vis_ledger | Orthogonal Procrustes | RO 92 | confirmed | N92: "SVD / Kabsch solution" |
| vis_ledger | Osculating circle | RO 67; RO 121 (curvature = 1 / radius) | confirmed | N67: "turning radius; curvature" (osculating circle has radius 1/curvature) |
| vis_ledger | Patch-based motion estimation | RO 230 | confirmed | N230: "Lucas-Kanade" |
| vis_ledger | Perspective n-point problem (PnP) | RO 233 | confirmed | N233: "PnP" |
| vis_ledger | Perspective transform (2D) | RO 229 | confirmed | N229: "Homography" |
| vis_ledger | Planar pattern tracking | RO 229 (tracking a plane by homography) | confirmed | N229: "Homography" |
| vis_ledger | Point-based representations | RO 91 (point clouds) | confirmed | N91: "Point clouds"; N97 "surfel maps named" |
| vis_ledger | Polar coordinates | RO 120 (polar-coordinate controller); MA-063 | confirmed | N120: "polar-coordinate controller" |
| vis_ledger | Pose estimation, iterative | RO 233 (refine pose by reprojection error) | confirmed | N233: "Reprojection error" |
| vis_ledger | Pyramid, motion estimation | RO 230 (pyramidal KLT) | confirmed | N230: "Pyramidal KLT tracker" |
| vis_ledger | Range scan, alignment | RO 92 | confirmed | N92: "ICP" |
| vis_ledger | Range scan, merging | RO 97 (fusing scans into a volumetric map) | confirmed | N97: "Signed-distance (TSDF) maps" |
| vis_ledger | Range scan, registration | RO 92 | confirmed | N92: "ICP" |
| vis_ledger | Range scan, segmentation | RO 176 (ground removal, clustering) | confirmed | N176: "ground removal, clustering" |
| vis_ledger | Range scan, volumetric | RO 97 (fusing scans into a volumetric map) | confirmed | N97: "Signed-distance (TSDF) maps" |
| vis_ledger | Range sensing (rangefinding), coded pattern | RO 90 (structured light) | confirmed | N90: "structured light" |
| vis_ledger | Range sensing (rangefinding), light stripe | RO 90 (structured light) | confirmed | N90: "structured light" |
| vis_ledger | Range sensing (rangefinding), stereo | RO 90 | confirmed | N90: "Stereo camera model: disparity and depth" |
| vis_ledger | Range sensing (rangefinding), texture pattern (checkerboard) | RO 90 (structured light) | confirmed | N90: "structured light" |
| vis_ledger | Rectification, standard rectified geometry | RO 90 | confirmed | N90: "Image rectification" |
| vis_ledger | Registration, feature-based | RO 229 | confirmed | N229: "Homography"; "RANSAC" |
| vis_ledger | Registration, intensity-based | RO 230; RO 234 | confirmed | N234: "Direct vs feature-based (indirect) methods" |
| vis_ledger | Robust least squares | RO 235 | confirmed | N235: "Robust cost functions"; plan §4 "robust losses (IRLS)" |
| vis_ledger | Robust statistics, inliers | RO 229 | confirmed | N229: "RANSAC" |
| vis_ledger | Robust statistics, M-estimator | RO 235 | confirmed | N235: "Robust cost functions" |
| vis_ledger | Rotations, interpolation | RO 202 (slerp) | confirmed | N202: "Interpolating orientation (slerp)" |
| vis_ledger | Scale invariant feature transform (SIFT) | RO 228 | confirmed | N228: "SIFT" |
| vis_ledger | Simultaneous localization and mapping (SLAM) | RO 100 | confirmed | N100: "online SLAM vs full SLAM" |
| vis_ledger | Skeleton | RO 270 (medial axis / generalised Voronoi) | confirmed | N270: "maximum-clearance roadmap (generalized Voronoi diagram)" (= medial axis / skeleton) |
| vis_ledger | Spherical coordinates | RO 91 (range-azimuth-elevation) | confirmed | N91: "Range-azimuth-elevation sensor model" |
| vis_ledger | Spherical linear interpolation | RO 202 (slerp) | confirmed | N202: "slerp" |
| vis_ledger | Stereo, feature-based | RO 233 | confirmed | N233: "Triangulation" |
| vis_ledger | Stereo, sparse correspondence | RO 233 | confirmed | N233: "Triangulation" |
| vis_ledger | Structure from motion, two-frame | RO 233 | confirmed | N233: "Recovering R and t from E; Triangulation" |
| vis_ledger | Sum of squared differences (SSD), surface | RO 227 (Harris from the SSD surface) | confirmed | N227: "Harris and Shi-Tomasi corners and the structure tensor" |
| vis_ledger | Surface representations | RO 97 (choosing a map type) | confirmed | N97: "Choosing a map type: landmarks, point clouds, voxels, elevation, meshes" |
| vis_ledger | Surface representations, triangle mesh | RO 71; RO 97 (triangle meshes) | confirmed | N71: "triangle meshes"; N97 "meshes" |
| vis_ledger | Temporal derivative | RO 230 (brightness constancy: time derivative) | confirmed | N230: "Brightness constancy and the optical-flow constraint" |
| vis_ledger | Total least squares (TLS) | RO 92 (total least squares by the smallest eigenvector) | add | total least squares (errors-in-variables): fit a line or plane with errors in all coordinates by the smallest eigenvector / last singular vector [maths] → MA 07-optimisation, section in the planned Nonlinear least squares Note; used by N92 plane fitting |
| vis_ledger | Tracking, feature | RO 230 | confirmed | N230: "Pyramidal KLT tracker" |
| vis_ledger | Tracking, multiple hypothesis | RO 259 | confirmed | N259: "multi-hypothesis tracking" |
| vis_ledger | Tracking, planar pattern | RO 229 | confirmed | N229: "Homography" |
| vis_ledger | Translational motion estimation | RO 230 | confirmed | N230: "Lucas-Kanade" |
| vis_ledger | Variable state dimension filter (VSDF) | RO 263 (sliding-window filter) | confirmed | N263: "Filtering vs optimisation (sliding window)" |
| vis_ledger | Variational method | RO 202 (beginner calculus of variations) | confirmed | re-cite N231: "Horn-Schunck: dense flow with a smoothness term"; plan §4 calculus of variations |
| vis_ledger | Volumetric 3D reconstruction | RO 97 (volumetric / signed-distance fusion) | confirmed | N97: "Signed-distance (TSDF) maps" |
| vis_ledger | Volumetric range image processing (VRIP) | RO 97 (volumetric / signed-distance fusion) | confirmed | N97: "Signed-distance (TSDF) maps" |
| vis_ledger | Volumetric representations | RO 97 (volumetric / signed-distance fusion) | confirmed | N97: "voxel grids; Signed-distance (TSDF) maps" |
