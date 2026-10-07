# Index check of the robotics plan: MPC (Rawlings et al.), MLS (Murray, Li, Sastry), Underactuated Robotics (Tedrake)

Agent `adv`. Every term of each book, judged against `docs/books-scope/robotics.md` (Notes 1-359, §4 planned MA/DL Notes, §5 recap), the eight evidence docs, the MA/ML/DL Notes and `glossary.md`.

Verdicts: **taught** (where = the Note whose title/Teaches, or MA/ML/DL body, contains the concept; 'plan §4 new MA: X' = a planned Note listed in the plan), **mentioned-only** (none here), **add** (concept in bold, kind, target chapter), **out-of-scope** (checkable reason), **index-noise**.
Matching: `robo_match.py` (case-insensitive, light stemming, synonyms) gave candidate hits; every row was then judged by reading the term, the plan Note list and, where unclear, the book text.

## Rawlings, Mayne & Diehl, *Model Predictive Control: Theory, Computation, and Design*, 2nd ed. (6th printing, 2024)

Free official PDF from the Rawlings group page (Rawlings moved from UW-Madison to UC Santa Barbara; the page is the group's book site): https://sites.engineering.ucsb.edu/~jbraw/mpc/MPC-book-2nd-edition-6th-printing.pdf . Subject Index pp. 613-623 (PDF pp. 664-673), parsed from `pdftotext -bbox`. The Citation (author) Index before it is names only and was not used.

Counts: taught 246, mentioned-only 0, add 105, out-of-scope 295, index-noise 117 (total 763).

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| A-stable integration methods | 501 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Accumulation point (see Sequence) |  | index-noise | cross-reference to "Sequence" |
| Active |  | index-noise | grouping header for the sub-entries below |
| Active, constraint | 743 | taught | MA-066 (active constraint, G-166) |
| Active, set | 552, 743 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| AD | 514, 516, 561, 580 | taught | MA-063 (automatic differentiation, G-232) |
| AD, forward mode | 520 | taught | MA-063 (forward mode AD) |
| AD, reverse mode | 522 | taught | MA-063 (reverse mode AD); DL-015 backpropagation |
| Adaptive stepsize | 507 | add | **ODE solving basics: initial- vs boundary-value problems, explicit vs implicit integrators, stiff equations, step size, local and global error** (maths) -> MA 06-calculus (extend the planned 'Numerical integration of ODEs' Note) |
| Adjoint operator | 676 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Admissible | 97 | taught | Note 207 (input and state constraints: admissible = satisfies the constraints) |
| Admissible, control | 464, 465, 469 | taught | Note 207 (input constraints) |
| Admissible, control sequence | 108, 210, 732 | taught | Note 207 (input constraints over the horizon) |
| Admissible, disconnected region | 161 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Admissible, disturbance sequence | 198, 204, 215, 227 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Admissible, policy | 197, 198 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Admissible, set | 137, 166, 168 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Affine | 446, 447, 488 | taught | MA-053 (affine transformation, G-178) |
| Affine, function | 447 | taught | MA-053 (affine map) |
| Affine, hull | 450, 632 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Affine, invariance | 513 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Affine, piecewise | 104, 448, 450, 452, 458, 462, 468, 763 | add | **Explicit MPC: the MPC law precomputed offline as a piecewise-affine lookup table** (control) -> RO-15 (extend Note 207) |
| Affine, set | 632 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Algebraic states | 506 | out-of-scope | differential-algebraic equations: numerical-analysis topic (RMD 8.4); constrained robot dynamics are taught via Lagrange multipliers (Note 289) |
| Algorithmic (or automatic) differentiation (see AD) |  | index-noise | cross-reference to "AD" |
| Arrival cost | 33, 70, 79, 80 | add | **Arrival cost in moving-horizon (sliding-window) estimation: a prior that summarises dropped measurements; forward DP view of estimation** (robotics) -> RO-22 (extend Note 263) |
| Arrival cost, full information | 296 | add | **Arrival cost in moving-horizon (sliding-window) estimation: a prior that summarises dropped measurements; forward DP view of estimation** (robotics) -> RO-22 (extend Note 263) |
| AS | 112, 423, 698 | add | **Stability definitions: equilibrium, Lyapunov stable, asymptotically and exponentially stable, local vs global, region of attraction; stability from the linearisation (Lyapunov's indirect method)** (maths) -> MA 06-calculus (extend the planned 'Stability of dynamical systems' Note) |
| Asymptotically stable (see AS) |  | index-noise | cross-reference to "AS" |
| Attraction |  | index-noise | grouping header for the sub-entries below |
| Attraction, domain of | 700 | add | **Stability definitions: equilibrium, Lyapunov stable, asymptotically and exponentially stable, local vs global, region of attraction; stability from the linearisation (Lyapunov's indirect method)** (maths) -> MA 06-calculus (extend the planned 'Stability of dynamical systems' Note) |
| Attraction, global | 697 | add | **Stability definitions: equilibrium, Lyapunov stable, asymptotically and exponentially stable, local vs global, region of attraction; stability from the linearisation (Lyapunov's indirect method)** (maths) -> MA 06-calculus (extend the planned 'Stability of dynamical systems' Note) |
| Attraction, region of | 113, 700 | add | **Stability definitions: equilibrium, Lyapunov stable, asymptotically and exponentially stable, local vs global, region of attraction; stability from the linearisation (Lyapunov's indirect method)** (maths) -> MA 06-calculus (extend the planned 'Stability of dynamical systems' Note) |
| Attractivity | 710 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Back propagation algorithm | 524 | taught | DL-015 (backpropagation = reverse-mode AD) |
| Bar quantities | 518 | index-noise | book notation (bar quantities in the AD chapter) |
| Bayes’s theorem | 672, 674 | taught | MA-018 (Bayes' theorem) |
| Bellman-Gronwall lemma | 651 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| BFGS | 550 | taught | MA-064 (BFGS, G-283) |
| Bolzano-Weierstrass theorem | 111, 632 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Boundary-value problem (see BVP) |  | index-noise | cross-reference to "BVP" |
| Bounded |  | index-noise | grouping header for the sub-entries below |
| Bounded, locally | 209, 693, 696, 710, 711 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Bounded estimate error | 313 | out-of-scope | estimator convergence and stability theory (RMD ch.4), research depth |
| Broyden-Fletcher-Goldfarb-Shanno (see BFGS) |  | index-noise | cross-reference to "BFGS" |
| Butcher tableau | 498 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| BVP | 493, 582 | add | **ODE solving basics: initial- vs boundary-value problems, explicit vs implicit integrators, stiff equations, step size, local and global error** (maths) -> MA 06-calculus (extend the planned 'Numerical integration of ODEs' Note) |
| C-set | 338 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Caratheodory conditions | 651 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| CasADi | vii, xii, xiii, 527, 580, 585, 586, 591 | out-of-scope | software or tool name, not a concept |
| Cayley-Hamilton theorem | 22, 64 | out-of-scope | proof technique or derivation route (a lemma used inside a derivation) |
| Central limit theorem | 657 | taught | MA-033 (central limit theorem) |
| Centralized control | 363, 376 | taught | Note 284 (decentralised vs centralised control) |
| Certainty equivalence | 194 | taught | Note 19 (certainty equivalence) |
| Chain rule | 61, 638 | taught | MA-061 (chain rule) |
| Cholesky factorization | 508, 561 | taught | plan §4 new MA: Cholesky factor (first needed by Note 256) |
| CIA | 577, 594 | out-of-scope | mixed-integer solution heuristic (RMD 8.x), research depth beyond the mixed-integer add |
| CLF | 131, 134, 714–716 | add | **Control Lyapunov functions (CLF) and the CLF-CBF quadratic program** (control) -> RO-14 (extend Note 199) |
| CLF, constrained | 716 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| CLF, global | 714 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Closed-loop control | 92 | taught | Note 9 (open-loop plan vs feedback plan) |
| Code generation | 569 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Collocation | 502 | taught | Note 116 (collocation) |
| Collocation, direct | 540 | taught | Note 116 (collocation) |
| Collocation, methods | 502 | taught | Note 116 (collocation) |
| Collocation, points | 502 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Combinatorial integral approximation (see CIA) |  | index-noise | cross-reference to "CIA" |
| Combining MHE and MPC | 312 | add | **State observer (Luenberger), output feedback and the separation principle; LQG; output-feedback MPC (estimator + controller)** (control) -> RO-15 (new Note after Note 204) |
| Combining MHE and MPC, stability | 314 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Complementarity condition | 543 | taught | MA-066 (complementary slackness in the KKT conditions) |
| Complementarity condition, strict | 544 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Concave function | 647 | taught | MA-067 (concave function, G-438) |
| Condensing | 491, 560 | taught | Note 207 (condensed vs sparse QP) |
| Cone |  | index-noise | grouping header for the sub-entries below |
| Cone, convex | 644 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Cone, normal | 439, 737, 743, 746, 748 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Cone, polar | 453, 455, 644, 740 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Cone, tangent | 737, 743, 746, 748 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Constrained Gauss-Newton method | 549 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Constraint qualification | 479, 750, 751 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Constraints | 6 | taught | Note 207 (input and state constraints) |
| Constraints, active | 543, 743 | taught | MA-066 (active constraint) |
| Constraints, coupled input | 405 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Constraints, hard | 7, 94 | add | **Hard vs soft constraints: soft constraints with slack variables** (control) -> RO-15 (extend Note 207) |
| Constraints, input | 6, 94 | taught | Note 207 (input constraints) |
| Constraints, integrality | 8 | add | **Mixed-integer programming (MILP/MIQP): optimisation with on/off decisions, e.g. footstep and contact-sequence planning** (maths) -> MA 07-optimisation (new short section after MA-068); used by Note 306 |
| Constraints, output | 6 | taught | Note 207 (state constraints include output limits) |
| Constraints, polyhedral | 743 | taught | MA-068 (linear inequality constraints of an LP/QP) |
| Constraints, probabilistic | 254 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Constraints, soft | 7, 132 | add | **Hard vs soft constraints: soft constraints with slack variables** (control) -> RO-15 (extend Note 207) |
| Constraints, state | 6, 94 | taught | Note 207 (state constraints) |
| Constraints, terminal | 96, 144–147, 212 | taught | Note 207 (terminal cost and terminal set) |
| Constraints, tightened | 202, 223, 230, 242, 346, 357 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Constraints, trust region | 514 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Constraints, uncoupled input | 402 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Continuation methods | 571 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Continuity | 633 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Continuity, lower semicontinuous | 634 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Continuity, uniform | 634 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Continuity, upper semicontinuous | 634 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Control law | 90, 200, 445 | taught | Note 204 (state feedback u = -Kx) |
| Control law, continuity | 104 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Control law, discontinuity | 104 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Control law, explicit | 446 | add | **Explicit MPC: the MPC law precomputed offline as a piecewise-affine lookup table** (control) -> RO-15 (extend Note 207) |
| Control law, implicit | 100, 210, 446 | taught | Note 207 (receding horizon: the law is the solution of an online QP) |
| Control law, offline | 89, 236 | add | **Explicit MPC: the MPC law precomputed offline as a piecewise-affine lookup table** (control) -> RO-15 (extend Note 207) |
| Control law, online | 89 | add | **Explicit MPC: the MPC law precomputed offline as a piecewise-affine lookup table** (control) -> RO-15 (extend Note 207) |
| Control law, time-invariant | 100 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Control Lyapunov function (see CLF) |  | index-noise | cross-reference to "CLF" |
| Control vector parameterization | 532 | taught | Note 116 (single shooting: parameterise the inputs) |
| Controllability | 23 | taught | Note 204 (controllability and the rank test) |
| Controllability, canonical form | 68 | out-of-scope | derivation device (canonical form) for pole placement; Note 204 teaches pole placement directly |
| Controllability, duality with observability | 291 | add | **Observability rank test, stabilizability and detectability; duality of control and estimation** (control) -> RO-15 (new Note after Note 204, together with observers) |
| Controllability, matrix | 23 | taught | Note 204 (controllability rank test) |
| Controllability, weak | 116 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Controllable | 23 | taught | Note 204 (controllability) |
| Converse theorem |  | index-noise | grouping header for the sub-entries below |
| Converse theorem, asymptotic stability | 705 | out-of-scope | proof technique or derivation route (a lemma used inside a derivation) |
| Converse theorem, exponential stability | 374, 725 | out-of-scope | proof technique or derivation route (a lemma used inside a derivation) |
| Convex | 646 | taught | MA-067 (convex sets and functions) |
| Convex, cone | 644 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Convex, function | 488, 583, 646 | taught | MA-067 (convex function) |
| Convex, hull | 641 | taught | plan §4 new MA: Convex hull (first needed by Note 290) |
| Convex, optimization problem | 487, 741 | taught | MA-067 (convex optimisation problem, G-478) |
| Convex, optimization problem, optimality condition | 453 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Convex, set | 338, 583, 641 | taught | MA-067 (convex set) |
| Cooperative control | 363, 386 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Cooperative control, algorithm | 421 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Cooperative control, distributed nonlinear | 419 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Correlation | 668 | taught | MA-009 (correlation) |
| Cost function | 11, 95, 369 | taught | MA-065 (cost function) |
| DAE | 505 | out-of-scope | differential-algebraic equations: numerical-analysis topic (RMD 8.4); constrained robot dynamics are taught via Lagrange multipliers (Note 289) |
| DAE, semiexplicit DAE of index one | 506 | out-of-scope | differential-algebraic equations: numerical-analysis topic (RMD 8.4); constrained robot dynamics are taught via Lagrange multipliers (Note 289) |
| Damping | 514 | taught | plan §4 new MA: Levenberg-Marquardt (damped Gauss-Newton) (first needed by Note 235) |
| DARE | 25, 69, 136 | taught | Note 205 (infinite-horizon LQR and the steady Riccati equation) |
| DDP | 564 | taught | Note 116 (DDP/iLQR) |
| DDP, exact Hessian | 565 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| DDP, Gauss-Newton Hessian | 565 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Decentralized control | 363, 377 | taught | Note 284 (decentralised control) |
| Decreasing (see Sequence) |  | index-noise | cross-reference to "Sequence" |
| Derivatives | 636 | taught | MA-061 (derivatives) |
| Detectability | 50, 120, 275, 319, 321, 322, 719 | add | **Observability rank test, stabilizability and detectability; duality of control and estimation** (control) -> RO-15 (new Note after Note 204, together with observers) |
| Detectability, duality with stabilizability | 291 | add | **Observability rank test, stabilizability and detectability; duality of control and estimation** (control) -> RO-15 (new Note after Note 204, together with observers) |
| Detectability, exponential | 285 | out-of-scope | estimator convergence and stability theory (RMD ch.4), research depth |
| Detectable | 26, 68, 72, 73, 325 | add | **Observability rank test, stabilizability and detectability; duality of control and estimation** (control) -> RO-15 (new Note after Note 204, together with observers) |
| Determinant | 27, 628, 659, 666 | taught | MA-056 (determinant, G-598) |
| Deterministic problem | 91 | taught | plan §4 new MA: State-space models (deterministic x' = Ax + Bu) |
| Difference equation | 5 | taught | plan §4 new MA: State-space models (discrete-time model x(k+1) = Ax(k) + Bu(k)) |
| Difference equation, linear | 5 | taught | plan §4 new MA: State-space models (discrete-time linear model) |
| Difference equation, nonlinear | 93, 237 | taught | plan §4 new MA: State-space models (nonlinear systems) |
| Difference equation, uncertain systems | 203, 211 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Difference inclusion | 203, 711 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Difference inclusion, asymptotic stability | 150 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Difference inclusion, discontinuous systems | 206 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Difference inclusion, uncertain systems | 203 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Differential algebraic equation (see DAE) |  | index-noise | cross-reference to "DAE" |
| Differential dynamic programming (see DDP) |  | index-noise | cross-reference to "DDP" |
| Differential equation | 91 | taught | plan §4 new MA: ODEs and vector fields |
| Differential equations | 648 | taught | plan §4 new MA: ODEs and vector fields |
| Differential states | 506 | out-of-scope | differential-algebraic equations: numerical-analysis topic (RMD 8.4); constrained robot dynamics are taught via Lagrange multipliers (Note 289) |
| Differentiation |  | index-noise | grouping header for the sub-entries below |
| Differentiation, algorithmic | 516 | taught | MA-063 (automatic differentiation) |
| Differentiation, numerical | 515 | taught | MA-062 (finite-difference estimate of a derivative) |
| Differentiation, symbolic | 514 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Direct collocation | 540, 588 | taught | Note 116 (collocation) |
| Direct methods | 493 | taught | Note 116 (direct vs indirect methods) |
| Direct multiple shooting | 534, 586, 589 | taught | Note 116 (multiple shooting) |
| Direct single shooting | 532, 586 | taught | Note 116 (single shooting) |
| Direct transcription methods | 538 | taught | Note 116 (direct methods: transcribe the OCP into an NLP) |
| Directional derivatives | 639 | taught | MA-062 (directional derivative, G-614) |
| Directional derivatives, forward | 518 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Directional derivatives, reverse | 518 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Discrete actuators | 8, 160 | add | **Mixed-integer programming (MILP/MIQP): optimisation with on/off decisions, e.g. footstep and contact-sequence planning** (maths) -> MA 07-optimisation (new short section after MA-068); used by Note 306 |
| Discrete algebraic Riccati equation (see DARE) |  | index-noise | cross-reference to "DARE" |
| Discretization | 531 | taught | plan §4 new MA: State-space models (discrete-time models by zero-order hold) |
| Dissipativity (see Economic MPC) |  | index-noise | cross-reference to "Economic MPC" |
| Distance |  | index-noise | grouping header for the sub-entries below |
| Distance, Hausdorff, set to set | 224, 339 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Distance, point to set | 207, 208, 224 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Distributed |  | index-noise | grouping header for the sub-entries below |
| Distributed, gradient algorithm | 417 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Distributed, nonconvex optimization | 417 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Distributed, nonlinear cooperative control | 419 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Distributed, nonlinear cooperative control, stability | 422 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Distributed, optimization | 426 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Distributed, state estimation | 399 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Distributed, target problem | 410 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Distributed MPC | 363 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Distributed MPC, disturbance models | 408 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Distributed MPC, nonlinear | 414, 422 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Distributed MPC, state estimation | 399 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Distributed MPC, target problem | 410 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Distributed MPC, zero offset | 411 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Disturbances | 49 | taught | Note 208 (disturbances and offset-free MPC) |
| Disturbances, additive | 193, 224, 228 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Disturbances, bounded | 336 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Disturbances, integrating | 50 | taught | Note 208 (disturbance model for offset-free MPC) |
| Disturbances, measurement | 269 | taught | Note 80 (linear Gaussian system: measurement noise) |
| Disturbances, process | 269 | taught | Note 80 (linear Gaussian system: process noise) |
| Disturbances, random | 198 | taught | Note 80 (linear Gaussian system: random disturbances) |
| Disturbances, stability | 712 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Dot quantities | 518 | index-noise | book notation (dot quantities in the AD chapter) |
| DP | 14, 107, 195, 364, 367, 469, 729 | taught | Note 10 (Bellman equations, principle of optimality); Note 14 (value iteration) |
| DP, backward | 14, 18 | taught | Note 205 (discrete-time LQ problem solved by dynamic programming, Riccati recursion) |
| DP, forward | 14, 33, 296 | add | **Arrival cost in moving-horizon (sliding-window) estimation: a prior that summarises dropped measurements; forward DP view of estimation** (robotics) -> RO-22 (extend Note 263) |
| DP, robust control | 214 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Dual dynamic system | 677 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Duality |  | index-noise | grouping header for the sub-entries below |
| Duality, of linear estimation and regulation | 290 | add | **Observability rank test, stabilizability and detectability; duality of control and estimation** (control) -> RO-15 (new Note after Note 204, together with observers) |
| Duality, strong | 184, 769 | taught | MA-067 (strong duality, Slater's condition) |
| Duality, weak | 184, 769 | taught | MA-066 (weak duality) |
| Dynamic programming (see DP) |  | index-noise | cross-reference to "DP" |
| Economic MPC | 153 | out-of-scope | economic MPC: process-industry profit objective and dissipativity theory (RMD 2.8), research depth |
| Economic MPC, asymptotic average performance | 155 | out-of-scope | economic MPC: process-industry profit objective and dissipativity theory (RMD 2.8), research depth |
| Economic MPC, asymptotic stability | 156 | out-of-scope | economic MPC: process-industry profit objective and dissipativity theory (RMD 2.8), research depth |
| Economic MPC, comparison with tracking MPC | 158 | out-of-scope | economic MPC: process-industry profit objective and dissipativity theory (RMD 2.8), research depth |
| Economic MPC, dissipativity | 156 | out-of-scope | economic MPC: process-industry profit objective and dissipativity theory (RMD 2.8), research depth |
| Economic MPC, strict dissipativity | 157, 160 | out-of-scope | economic MPC: process-industry profit objective and dissipativity theory (RMD 2.8), research depth |
| EKF | 302–304 | taught | Note 81 (extended Kalman filter) |
| END | 525 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Epigraph | 647 | taught | MA-067 (epigraph, G-695) |
| Equilibrium point | 694 | taught | plan §4 new MA: Stability of dynamical systems (equilibria) |
| Estimation | 26, 269, 349 | taught | Note 78 (Bayes filter); Note 80 (Kalman filter) |
| Estimation, convergence | 43 | out-of-scope | estimator convergence and stability theory (RMD ch.4), research depth |
| Estimation, distributed | 399 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Estimation, duality with regulation | 290 | add | **Observability rank test, stabilizability and detectability; duality of control and estimation** (control) -> RO-15 (new Note after Note 204, together with observers) |
| Estimation, full information (see FIE) |  | index-noise | cross-reference to "FIE" |
| Estimation, least squares | 33 | taught | ML-053 (least squares); plan §4 new MA: Recursive least squares |
| Estimation, linear optimal | 29 | taught | Note 80 (Kalman filter as the linear optimal estimator) |
| Estimation, moving horizon (see MHE) |  | index-noise | cross-reference to "MHE" |
| Estimation, stability | 288 | out-of-scope | estimator convergence and stability theory (RMD ch.4), research depth |
| Euler integration method | 494, 497 | taught | plan §4 new MA: Numerical integration of ODEs (Euler and Runge-Kutta steps) |
| Expectation | 655 | taught | MA-012 (expected value) |
| Explicit MPC | 445 | add | **Explicit MPC: the MPC law precomputed offline as a piecewise-affine lookup table** (control) -> RO-15 (extend Note 207) |
| Exponential stability (see Stability) |  | index-noise | cross-reference to "Stability" |
| Extended Kalman filter (see EKF) |  | index-noise | cross-reference to "EKF" |
| External numerical differentiation (see END) |  | index-noise | cross-reference to "END" |
| Farkas’s lemma | 453 | out-of-scope | proof technique or derivation route (a lemma used inside a derivation) |
| Feasibility |  | index-noise | grouping header for the sub-entries below |
| Feasibility, recursive | 112, 132, 356 | add | **Invariant sets (positively invariant, control invariant) and recursive feasibility of MPC** (control) -> RO-15 (extend Note 207) |
| Feasible set | 487 | taught | MA-068 (feasible region of an LP/QP) |
| Feedback control | 49, 195, 340 | taught | Note 117 (PD/PID feedback control) |
| Feedback MPC | 200 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Feedback particle filtering | 302 | out-of-scope | research-level estimator (feedback particle filter, RMD 4.7) |
| Feedforward control | 341 | taught | Note 119 (feedforward plus feedback) |
| FIE | 269 | taught | Note 101 (full SLAM: estimate the whole trajectory from all data = full information estimation) |
| Final-state observability (see FSO) |  | index-noise | cross-reference to "FSO" |
| Finite horizon | 21, 89 | taught | Note 207 (plan N steps: finite horizon) |
| Floating point operation (see FLOP) |  | index-noise | cross-reference to "FLOP" |
| FLOP | 367, 508, 560, 561 | taught | DL-086 (FLOP, G-790) |
| Forward mode (see AD) |  | index-noise | cross-reference to "AD" |
| Fritz-John necessary conditions | 753 | out-of-scope | proof technique or derivation route (a lemma used inside a derivation) |
| FSO | 294 | out-of-scope | estimator convergence and stability theory (RMD ch.4), research depth |
| Full information estimation (see FIE) |  | index-noise | cross-reference to "FIE" |
| Fundamental theorem of linear algebra | 23, 42, 625 | add | **Solving linear systems Ax = b: Gaussian elimination, existence and uniqueness of solutions (range and null space)** (maths) -> MA 05-linear-algebra (new Note) |
| Fundamental theorem of linear algebra, existence | 23, 625 | add | **Solving linear systems Ax = b: Gaussian elimination, existence and uniqueness of solutions (range and null space)** (maths) -> MA 05-linear-algebra (new Note) |
| Fundamental theorem of linear algebra, uniqueness | 42, 625 | add | **Solving linear systems Ax = b: Gaussian elimination, existence and uniqueness of solutions (range and null space)** (maths) -> MA 05-linear-algebra (new Note) |
| Game |  | taught | Note 54 (games: zero-sum, Nash equilibrium) |
| Game, M-player game | 412 | out-of-scope | game formulations used only to analyse distributed MPC (RMD ch.6) |
| Game, constrained two-player | 400 | out-of-scope | game formulations used only to analyse distributed MPC (RMD ch.6) |
| Game, cooperative | 386 | out-of-scope | game formulations used only to analyse distributed MPC (RMD ch.6) |
| Game, noncooperative | 378 | out-of-scope | game formulations used only to analyse distributed MPC (RMD ch.6) |
| Game, theory | 426 | taught | Note 54 (games and equilibria) |
| Game, two-player nonconvex | 418 | out-of-scope | game formulations used only to analyse distributed MPC (RMD ch.6) |
| Game, unconstrained two-player | 374 | out-of-scope | game formulations used only to analyse distributed MPC (RMD ch.6) |
| GAS | 112, 408, 433, 698 | add | **Stability definitions: equilibrium, Lyapunov stable, asymptotically and exponentially stable, local vs global, region of attraction; stability from the linearisation (Lyapunov's indirect method)** (maths) -> MA 06-calculus (extend the planned 'Stability of dynamical systems' Note) |
| Gauss divergence theorem | 61 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Gauss-Jacobi iteration | 380 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Gauss-Legendre methods (see GL) |  | index-noise | cross-reference to "GL" |
| Gauss-Newton Hessian | 548, 589 | taught | plan §4 new MA: Nonlinear least squares (Gauss-Newton) |
| Gaussian distribution (see Normal density) |  | index-noise | cross-reference to "Normal density" |
| Gaussian elimination | 508 | add | **Solving linear systems Ax = b: Gaussian elimination, existence and uniqueness of solutions (range and null space)** (maths) -> MA 05-linear-algebra (new Note) |
| Generalized Gauss-Newton method | 549 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Generalized predictive control (see GPC) |  | index-noise | cross-reference to "GPC" |
| Generalized tangential predictors | 552, 570 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| GES | 698 | add | **Stability definitions: equilibrium, Lyapunov stable, asymptotically and exponentially stable, local vs global, region of attraction; stability from the linearisation (Lyapunov's indirect method)** (maths) -> MA 06-calculus (extend the planned 'Stability of dynamical systems' Note) |
| GL | 505 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Global error | 496 | add | **ODE solving basics: initial- vs boundary-value problems, explicit vs implicit integrators, stiff equations, step size, local and global error** (maths) -> MA 06-calculus (extend the planned 'Numerical integration of ODEs' Note) |
| Global solutions | 741 | taught | MA-065 (convex vs non-convex: local vs global minimum) |
| Globalization techniques | 514 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Globally asymptotically stable (see GAS) |  | index-noise | cross-reference to "GAS" |
| Globally exponentially stable (see GES) |  | index-noise | cross-reference to "GES" |
| GPC | 167 | out-of-scope | history of the field |
| Gramian |  | index-noise | grouping header for the sub-entries below |
| Gramian, observability | 684 | out-of-scope | Gramian energy tests: an alternative to the rank test (RMD App. A), beyond beginner depth |
| Gramian, reachability | 683 | out-of-scope | Gramian energy tests: an alternative to the rank test (RMD App. A), beyond beginner depth |
| Hamilton-Jacobi-Bellman equation (see HJB) |  | index-noise | cross-reference to "HJB" |
| Hausdorff metric (see Distance Hausdorff) |  | index-noise | cross-reference to "Distance Hausdorff" |
| Hautus lemma |  | index-noise | grouping header for the sub-entries below |
| Hautus lemma, controllability | 24 | out-of-scope | Hautus (PBH) eigenvector test: an alternative to the rank test used in proofs; Note 204's rank test suffices at beginner depth |
| Hautus lemma, detectability | 72, 437, 441 | out-of-scope | Hautus (PBH) eigenvector test: an alternative to the rank test used in proofs; Note 204's rank test suffices at beginner depth |
| Hautus lemma, observability | 42 | out-of-scope | Hautus (PBH) eigenvector test: an alternative to the rank test used in proofs; Note 204's rank test suffices at beginner depth |
| Hautus lemma, stabilizability | 68 | out-of-scope | Hautus (PBH) eigenvector test: an alternative to the rank test used in proofs; Note 204's rank test suffices at beginner depth |
| Hessian approximations | 547 | taught | MA-064 (Newton and quasi-Newton: approximating the Hessian, BFGS) |
| Hessian approximations, BFGS | 550 | taught | MA-064 (BFGS) |
| Hessian approximations, Gauss-Newton | 548 | taught | plan §4 new MA: Nonlinear least squares (Gauss-Newton) |
| Hessian approximations, secant condition | 550 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Hessian approximations, update methods | 549 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| HJB | 493 | taught | Note 205 (Hamilton-Jacobi-Bellman equation) |
| Hurwitz matrix | 220, 706 | taught | plan §4 new MA: Stability of dynamical systems (stable iff all eigenvalues have negative real part) |
| Hyperplane | 472, 642, 643 | taught | MA-051 (equation of a hyperplane) |
| Hyperplane, support | 644 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Hyperstate | 194, 333, 334 | taught | Note 77 (information state: the history summarised) |
| i-IOSS | 275, 285, 321, 323, 722 | out-of-scope | estimator convergence and stability theory (RMD ch.4), research depth |
| Implicit integrators | 500 | add | **ODE solving basics: initial- vs boundary-value problems, explicit vs implicit integrators, stiff equations, step size, local and global error** (maths) -> MA 06-calculus (extend the planned 'Numerical integration of ODEs' Note) |
| Increasing (see Sequence) |  | index-noise | cross-reference to "Sequence" |
| Incrementally, uniformly input/output-to-state-stable (see i-UIOSS) |  | index-noise | cross-reference to "i-UIOSS" |
| IND | 526 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Independent (see Random variable) |  | index-noise | cross-reference to "Random variable" |
| Indirect methods | 493 | taught | Note 116 (direct vs indirect methods) |
| Infinite horizon | 21, 89 | taught | Note 205 (infinite-horizon LQR); Note 8 (infinite horizon) |
| Initial-value embedding | 534 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Initial-value problem | 495 | add | **ODE solving basics: initial- vs boundary-value problems, explicit vs implicit integrators, stiff equations, step size, local and global error** (maths) -> MA 06-calculus (extend the planned 'Numerical integration of ODEs' Note) |
| Innovation | 194, 305, 334 | add | **Innovation (measurement residual) in the Kalman filter** (robotics) -> RO-02 (extend Note 80) |
| Input-to-state-stability (see ISS) |  | index-noise | cross-reference to "ISS" |
| Input/output-to-state-stability (see IOSS) |  | index-noise | cross-reference to "IOSS" |
| Integral control (see Offset-free control) |  | index-noise | cross-reference to "Offset-free control" |
| Interior point methods (see IP) |  | index-noise | cross-reference to "IP" |
| Internal model principle | 49 | add | **Internal model principle: to cancel a constant disturbance the controller must contain an integrator (a model of the disturbance)** (control) -> RO-06 (extend Note 119) |
| Internal numerical differentiation (see IND) |  | index-noise | cross-reference to "IND" |
| Invariance |  | index-noise | grouping header for the sub-entries below |
| Invariance, control | 110 | add | **Invariant sets (positively invariant, control invariant) and recursive feasibility of MPC** (control) -> RO-15 (extend Note 207) |
| Invariance, positive | 110, 339, 694, 712 | add | **Invariant sets (positively invariant, control invariant) and recursive feasibility of MPC** (control) -> RO-15 (extend Note 207) |
| Invariance, robust control | 217 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Invariance, robust positive | 212, 217, 313, 339, 350 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Invariance, sequential control | 125 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Invariance, sequential positive | 125, 707 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| IOSS | 121, 322, 323, 721 | out-of-scope | nonlinear robust-stability notions (ISS/IOSS, comparison functions K/KL; RMD App. B), graduate-level theory |
| IP | 552, 580 | taught | Note 208 (interior point, overview) |
| IPOPT | 528, 554, 580 | out-of-scope | software or tool name, not a concept |
| ISS | 718 | out-of-scope | nonlinear robust-stability notions (ISS/IOSS, comparison functions K/KL; RMD App. B), graduate-level theory |
| i-UIOSS | 312, 325 | out-of-scope | nonlinear robust-stability notions (ISS/IOSS, comparison functions K/KL; RMD App. B), graduate-level theory |
| K functions | 112, 275, 285, 694 | out-of-scope | nonlinear robust-stability notions (ISS/IOSS, comparison functions K/KL; RMD App. B), graduate-level theory |
| K functions, upper bounding | 709 | out-of-scope | nonlinear robust-stability notions (ISS/IOSS, comparison functions K/KL; RMD App. B), graduate-level theory |
| K ∞ functions | 112, 694 | out-of-scope | nonlinear robust-stability notions (ISS/IOSS, comparison functions K/KL; RMD App. B), graduate-level theory |
| KL functions | 112, 275, 285, 694 | out-of-scope | nonlinear robust-stability notions (ISS/IOSS, comparison functions K/KL; RMD App. B), graduate-level theory |
| Kalman filter (see KF) |  | index-noise | cross-reference to "KF" |
| Karush-Khun-Tucker conditions (see KKT) |  | index-noise | cross-reference to "KKT" |
| KF | 26, 33, 43, 51, 78, 79, 334 | taught | Note 80 (Kalman filter) |
| KF, extended | 306–311 | taught | Note 81 (extended Kalman filter) |
| KF, unscented | 304–311 | taught | Note 256 (unscented Kalman filter) |
| KKT | 543, 755 | taught | MA-066 (KKT conditions); plan §5 recap QP and KKT |
| KKT, matrix | 546 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| KKT, strongly regular | 545 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| L-stable integration methods | 505 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Lagrange basis polynomials | 503 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Lagrange multipliers | 66, 67, 365, 369, 430 | taught | MA-066 (Lagrange multipliers) |
| Laplace transform | 3 | add | **Laplace transform** (maths) -> MA 06-calculus (new Note) |
| LAR | 179, 475–476 | out-of-scope | regulator variant with a 1-norm cost, an RMD exercise topic |
| LDLT-factorization | 508 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| LDLT-factorization, plain banded | 560 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Least squares estimation (see Estimation) |  | index-noise | cross-reference to "Estimation" |
| Leibniz formula | 61 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Level set | 16, 137, 648 | taught | MA-067 (level sets of a convex function) |
| LICQ | 543, 755 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Limit (see Sequence) |  | index-noise | cross-reference to "Sequence" |
| Line search | 417, 514 | taught | MA-064 (line search: try a shorter step until the function drops enough) |
| Linear |  | index-noise | grouping header for the sub-entries below |
| Linear, MPC | 131–139, 488 | taught | Note 207 (linear MPC as a QP) |
| Linear, quadratic MPC | 11, 99, 461–470 | taught | Note 207 (linear MPC with quadratic cost as a QP) |
| Linear, space | 624 | taught | MA-047 (vector space) |
| Linear, subspace | 624 | taught | MA-058 (subspaces of a matrix: column space, null space) |
| Linear, system | 27, 131–139 | taught | plan §4 new MA: State-space models (x' = Ax + Bu) |
| Linear absolute regulator (see LAR) |  | index-noise | cross-reference to "LAR" |
| Linear independence constraint qualification (see LICQ) |  | index-noise | cross-reference to "LICQ" |
| Linear multistep methods | 580 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Linear optimal state estimation (see KF) |  | index-noise | cross-reference to "KF" |
| Linear program (see LP) |  | index-noise | cross-reference to "LP" |
| Linear quadratic Gaussian (see LQG) |  | index-noise | cross-reference to "LQG" |
| Linear quadratic problems (see LQP) |  | index-noise | cross-reference to "LQP" |
| Linear quadratic regulator (see LQR) |  | index-noise | cross-reference to "LQR" |
| Lipschitz continuous | 374, 406, 461, 495, 637, 761, 766 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Local error | 496 | add | **ODE solving basics: initial- vs boundary-value problems, explicit vs implicit integrators, stiff equations, step size, local and global error** (maths) -> MA 06-calculus (extend the planned 'Numerical integration of ODEs' Note) |
| Local solutions | 489, 741 | taught | MA-065 (local minima of non-convex costs) |
| Look-up table | 90 | add | **Explicit MPC: the MPC law precomputed offline as a piecewise-affine lookup table** (control) -> RO-15 (extend Note 207) |
| LP | 448, 451 | taught | MA-068 (linear programming) |
| LP, parametric | 470 | out-of-scope | parametric-programming detail of explicit MPC (RMD ch.7), research depth beyond the explicit-MPC add |
| LQG | 194, 335 | add | **State observer (Luenberger), output feedback and the separation principle; LQG; output-feedback MPC (estimator + controller)** (control) -> RO-15 (new Note after Note 204) |
| LQP | 429, 430, 558 | taught | Note 205 (discrete-time LQ problem) |
| LQP, condensing | 560 | taught | Note 207 (condensed QP) |
| LQP, Riccati recursion | 558 | taught | Note 205 (Riccati recursion) |
| LQR | 11, 24, 364, 429, 430, 565, 736 | taught | Note 205 (LQR and the Riccati equation) |
| LQR, constrained | 461–470 | taught | Note 207 (constrained LQ problem = linear MPC; unconstrained MPC equals LQR) |
| LQR, convergence | 24 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| LQR, DP solution for constrained | 469 | out-of-scope | parametric-programming detail of explicit MPC (RMD ch.7), research depth beyond the explicit-MPC add |
| LQR, infinite horizon | 21 | taught | Note 205 (infinite-horizon LQR) |
| LQR, unconstrained | 132 | taught | Note 207 (unconstrained MPC equals LQR) |
| LU-factorization | 508 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Luenberger observer | 338 | add | **State observer (Luenberger), output feedback and the separation principle; LQG; output-feedback MPC (estimator + controller)** (control) -> RO-15 (new Note after Note 204) |
| Lyapunov equation | 137, 706 | add | **Quadratic Lyapunov functions V = x'Px and the Lyapunov equation for linear systems** (maths) -> MA 06-calculus (extend the planned Stability Note) |
| Lyapunov function | 113, 701 | taught | Note 199 (stability certificates with Lyapunov functions); plan §4 Lyapunov functions |
| Lyapunov function, control (see CLF) |  | index-noise | cross-reference to "CLF" |
| Lyapunov function, global | 208 | taught | Note 199 (Lyapunov functions) |
| Lyapunov function, IOSS | 721 | out-of-scope | nonlinear robust-stability notions (ISS/IOSS, comparison functions K/KL; RMD App. B), graduate-level theory |
| Lyapunov function, ISS | 314, 718 | out-of-scope | nonlinear robust-stability notions (ISS/IOSS, comparison functions K/KL; RMD App. B), graduate-level theory |
| Lyapunov function, local | 239 | taught | Note 199 (Lyapunov functions) |
| Lyapunov function, OSS | 720 | out-of-scope | nonlinear robust-stability notions (ISS/IOSS, comparison functions K/KL; RMD App. B), graduate-level theory |
| Lyapunov stability | 370, 432 | taught | Note 199 (Lyapunov stability certificates) |
| Lyapunov stability, uniform | 371 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Lyapunov stability constraint | 404 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Lyapunov stability theorem | 113, 700 | taught | Note 199 (Lyapunov stability certificates) |
| Lyapunov stability theorem, KL version | 703 | out-of-scope | nonlinear robust-stability notions (ISS/IOSS, comparison functions K/KL; RMD App. B), graduate-level theory |
| M-player game |  | index-noise | grouping header for the sub-entries below |
| M-player game, constrained | 412 | out-of-scope | game formulations used only to analyse distributed MPC (RMD ch.6) |
| MATLAB | 22, 64, 65, 68, 508, 528 | out-of-scope | software or tool name, not a concept |
| Mean value theorem | 638 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Merit function | 514 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| MHE | 39, 292 | taught | Note 263 (filtering vs optimisation over a sliding window = moving-horizon estimation) |
| MHE, as conditional density | 40 | out-of-scope | estimator convergence and stability theory (RMD ch.4), research depth |
| MHE, as least squares | 40 | taught | Note 263 (sliding-window least squares) |
| MHE, combining with MPC | 312 | add | **State observer (Luenberger), output feedback and the separation principle; LQG; output-feedback MPC (estimator + controller)** (control) -> RO-15 (new Note after Note 204) |
| MHE, comparison with EKF and UKF | 306 | out-of-scope | estimator convergence and stability theory (RMD ch.4), research depth |
| MHE, convergence | 296 | out-of-scope | estimator convergence and stability theory (RMD ch.4), research depth |
| MHE, existence | 293 | out-of-scope | estimator convergence and stability theory (RMD ch.4), research depth |
| MHE, nonzero prior weighting | 296 | out-of-scope | estimator convergence and stability theory (RMD ch.4), research depth |
| MHE, zero prior weighting | 293 | out-of-scope | estimator convergence and stability theory (RMD ch.4), research depth |
| MILP | 575, 594 | add | **Mixed-integer programming (MILP/MIQP): optimisation with on/off decisions, e.g. footstep and contact-sequence planning** (maths) -> MA 07-optimisation (new short section after MA-068); used by Note 306 |
| Min-max optimal control | 214 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Minimum theorem | 760 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Minkowski set subtraction (see Set algebra) |  | index-noise | cross-reference to "Set algebra" |
| MINLP | 575 | add | **Mixed-integer programming (MILP/MIQP): optimisation with on/off decisions, e.g. footstep and contact-sequence planning** (maths) -> MA 07-optimisation (new short section after MA-068); used by Note 306 |
| MIQP | 575 | add | **Mixed-integer programming (MILP/MIQP): optimisation with on/off decisions, e.g. footstep and contact-sequence planning** (maths) -> MA 07-optimisation (new short section after MA-068); used by Note 306 |
| Mixed continuous/discrete actuators | 162 | add | **Mixed-integer programming (MILP/MIQP): optimisation with on/off decisions, e.g. footstep and contact-sequence planning** (maths) -> MA 07-optimisation (new short section after MA-068); used by Note 306 |
| Mixed-integer optimization | 161 | add | **Mixed-integer programming (MILP/MIQP): optimisation with on/off decisions, e.g. footstep and contact-sequence planning** (maths) -> MA 07-optimisation (new short section after MA-068); used by Note 306 |
| Models | 1 | index-noise | grouping header for the sub-entries below |
| Models, continuous time | 492 | taught | plan §4 new MA: State-space models (x' = Ax + Bu) |
| Models, deterministic | 2, 9 | taught | plan §4 new MA: State-space models |
| Models, discrete time | 5, 486 | taught | plan §4 new MA: State-space models (discrete-time models) |
| Models, distributed | 4 | out-of-scope | distributed-parameter (PDE) models of process plants: a different field |
| Models, disturbance | 49, 408 | taught | Note 208 (disturbance model for offset-free MPC) |
| Models, input-output | 3 | add | **Transfer functions (input-output models of linear systems)** (control) -> RO-06 (new Note) |
| Models, linear dynamic | 2 | taught | plan §4 new MA: State-space models (linear) |
| Models, stochastic | 9 | taught | Note 80 (linear Gaussian system) |
| Models, time-invariant | 2, 10 | add | **Linear time-invariant (LTI) vs time-varying systems** (maths) -> MA 06-calculus (extend the planned State-space models Note) |
| Models, time-varying | 2 | add | **Linear time-invariant (LTI) vs time-varying systems** (maths) -> MA 06-calculus (extend the planned State-space models Note) |
| Monotonicity | 118, 435 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Monte Carlo optimization | 223 | out-of-scope | sampling-based solution method for stochastic MPC (RMD 3.6), research depth |
| Move blocking | 568 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Moving horizon estimation (see MHE) |  | index-noise | cross-reference to "MHE" |
| MPCTools | vii, xii | out-of-scope | software or tool name, not a concept |
| Multipliers | 543 | taught | MA-066 (Lagrange multipliers) |
| Multistage optimization | 12 | taught | Note 205 (DP over stages); Note 10 (principle of optimality) |
| Nash equilibrium | 382–386 | taught | Note 54 (Nash equilibrium) |
| Newton-Lagrange method | 546 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Newton-Raphson method | 509 | taught | plan §4 new MA: Newton-Raphson root finding (first needed by Note 279) |
| Newton-type methods | 507, 510 | taught | MA-064 (Newton's method) |
| Newton-type methods, local convergence | 511 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Newton-type optimization with inequalities | 550 | taught | Note 208 (SQP and interior point, overview) |
| NLP | 534, 542 | taught | Note 208 (nonlinear MPC solved as an NLP) |
| Noise | 10 | index-noise | grouping header for the sub-entries below |
| Noise, Gaussian | 287 | taught | MA-072 (Gaussian noise, G-831) |
| Noise, measurement | 10, 26, 269 | taught | Note 80 (linear Gaussian system: measurement noise) |
| Noise, process | 26, 269 | taught | Note 80 (linear Gaussian system: process noise) |
| Nominal stability (see Stability) |  | index-noise | cross-reference to "Stability" |
| Nonconvex |  | index-noise | grouping header for the sub-entries below |
| Nonconvex, optimization problem | 487 | taught | MA-065 (non-convex cost functions) |
| Nonconvex optimization problem | 745 | taught | MA-065 (non-convex cost functions) |
| Nonconvexity | 166, 415 | taught | MA-065 (non-convexity: many local minima) |
| Noncooperative control | 363, 378 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Nonlinear |  | index-noise | grouping header for the sub-entries below |
| Nonlinear, MPC | 139–144, 488 | taught | Note 208 (nonlinear MPC) |
| Nonlinear interior point methods (see IP) |  | index-noise | cross-reference to "IP" |
| Nonlinear optimization | 542 | taught | Note 208 (nonlinear MPC: SQP, interior point); MA-064 |
| Nonlinear program (see NLP) |  | index-noise | cross-reference to "NLP" |
| Nonlinear root-finding problems | 508 | taught | plan §4 new MA: Newton-Raphson root finding |
| Norm | 631, 690, 696, 717 | taught | MA-049 (magnitude = norm of a vector) |
| Normal cone (see Cone) |  | index-noise | cross-reference to "Cone" |
| Normal density | 27, 656 | taught | MA-024 (normal distribution) |
| Normal density, conditional | 28, 674, 675 | add | **Conditioning a joint Gaussian: conditional mean and covariance** (maths) -> MA 08-likelihood (with the planned 'Linear transforms of a Gaussian' Note) |
| Normal density, degenerate | 661 | out-of-scope | probability-theory detail (degenerate densities, characteristic functions, non-invertible transforms; RMD App. A) |
| Normal density, Fourier transform of | 658 | out-of-scope | probability-theory detail (degenerate densities, characteristic functions, non-invertible transforms; RMD App. A) |
| Normal density, linear transformation | 28, 75 | taught | plan §4 new MA: Linear transforms of a Gaussian (first needed by Note 80) |
| Normal density, multivariate | 659 | taught | MA-073 (multivariate normal) |
| Normal density, singular | 661 | out-of-scope | probability-theory detail (degenerate densities, characteristic functions, non-invertible transforms; RMD App. A) |
| Normal distribution (see Normal density) |  | index-noise | cross-reference to "Normal density" |
| Nullspace | 53, 624 | taught | MA-058 (null space) |
| Numerical differentiation | 515 | taught | MA-062 (finite-difference derivative) |
| Numerical differentiation, forward difference | 515 | taught | MA-062 (finite-difference derivative) |
| Numerical integration | 495 | taught | plan §4 new MA: Numerical integration of ODEs |
| Numerical optimal control | 485 | taught | Note 116 (trajectory optimisation: direct methods) |
| Observability | 41, 293, 722 | taught | Note 80 (observability, concept) |
| Observability, canonical form | 72 | out-of-scope | derivation device (canonical form) for pole placement; Note 204 teaches pole placement directly |
| Observability, duality with controllability | 291 | add | **Observability rank test, stabilizability and detectability; duality of control and estimation** (control) -> RO-15 (new Note after Note 204, together with observers) |
| Observability, Gramian | 684 | out-of-scope | Gramian energy tests: an alternative to the rank test (RMD App. A), beyond beginner depth |
| Observability, matrix | 42 | add | **Observability rank test, stabilizability and detectability; duality of control and estimation** (control) -> RO-15 (new Note after Note 204, together with observers) |
| Observable | 41, 293 | taught | Note 80 (observability) |
| OCP | 490, 585, 586, 589, 592, 731 | taught | Note 116 (trajectory optimisation = optimal control problem) |
| OCP, continuous time | 492 | taught | Note 116 (continuous-time OCP; Pontryagin named) |
| OCP, discrete time | 486, 555 | taught | Note 205 (discrete-time LQ problem); Note 116 |
| Octave | 22, 64, 65, 68, 528 | out-of-scope | software or tool name, not a concept |
| ODE | 495–507, 528 | taught | plan §4 new MA: ODEs and vector fields |
| Offset-free control | 48–59 | taught | Note 208 (disturbances and offset-free MPC); Note 119 (integral action) |
| Offset-free MPC | 347 | taught | Note 208 (offset-free MPC) |
| One-step integration methods | 497 | taught | plan §4 new MA: Numerical integration of ODEs (Euler and Runge-Kutta are one-step methods) |
| Online optimization algorithms | 567 | taught | Note 208 (real-time MPC) |
| Open-loop control | 195 | taught | Note 9 (open-loop plan vs feedback plan) |
| Optimal control problem (see OCP) |  | index-noise | cross-reference to "OCP" |
| Optimality conditions | 543, 737 | taught | MA-066 (KKT optimality conditions) |
| Optimality conditions, convex program | 453 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Optimality conditions, KKT | 543 | taught | MA-066 (KKT conditions) |
| Optimality conditions, linear inequalities | 744 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Optimality conditions, nonconvex problems | 752 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Optimality conditions, normal cone | 742 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Optimality conditions, parametric LP | 472 | out-of-scope | parametric-programming detail of explicit MPC (RMD ch.7), research depth beyond the explicit-MPC add |
| Optimality conditions, tangent cone | 743 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Ordinary differential equation (see ODE) |  | index-noise | cross-reference to "ODE" |
| OSS | 321, 323, 719 | out-of-scope | nonlinear robust-stability notions (ISS/IOSS, comparison functions K/KL; RMD App. B), graduate-level theory |
| Outer-bounding tube (see Tube) |  | index-noise | cross-reference to "Tube" |
| Output MPC | 312–318, 333 | add | **State observer (Luenberger), output feedback and the separation principle; LQG; output-feedback MPC (estimator + controller)** (control) -> RO-15 (new Note after Note 204) |
| Output MPC, stability | 314, 345 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Output-to-state-stability (see OSS) |  | index-noise | cross-reference to "OSS" |
| Parameter | 97, 446 | index-noise | generic word (parameter of a parametric program) |
| Parametric optimization | 97 | out-of-scope | parametric-programming detail of explicit MPC (RMD ch.7), research depth beyond the explicit-MPC add |
| Parametric programming | 97, 446 | out-of-scope | parametric-programming detail of explicit MPC (RMD ch.7), research depth beyond the explicit-MPC add |
| Parametric programming, computation | 476 | out-of-scope | parametric-programming detail of explicit MPC (RMD ch.7), research depth beyond the explicit-MPC add |
| Parametric programming, continuity of V 0 (·) and u 0 (·) | 460 | out-of-scope | parametric-programming detail of explicit MPC (RMD ch.7), research depth beyond the explicit-MPC add |
| Parametric programming, linear | 470, 472, 473 | out-of-scope | parametric-programming detail of explicit MPC (RMD ch.7), research depth beyond the explicit-MPC add |
| Parametric programming, piecewise quadratic | 463 | out-of-scope | parametric-programming detail of explicit MPC (RMD ch.7), research depth beyond the explicit-MPC add |
| Parametric programming, quadratic | 451, 456, 458 | out-of-scope | parametric-programming detail of explicit MPC (RMD ch.7), research depth beyond the explicit-MPC add |
| Partial condensing | 562 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Partial separability | 556 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Particle filtering | 302 | taught | Note 82 (particle filter) |
| Particle filtering, feedback | 302 | out-of-scope | research-level estimator (feedback particle filter, RMD 4.7) |
| Partitioned matrix inversion theorem | 16, 65, 628 | taught | plan §4 new MA: Schur complement (block-matrix inverse) |
| Peano’s existence theorem | 651 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Picard-Lindelöf theorem | 495 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| PID control | 49, 84 | taught | Note 117 (PD and PID control) |
| Pivoting | 508 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Plantwide control | 363, 409, 418 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Plantwide control, optimal | 376, 421 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Plantwide control, subsystems | 364, 374, 414 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Polyhedral | 446, 447, 450, 743, 761 | taught | MA-068 (polytope feasible region) |
| Polytope | 203, 450, 461, 462, 464–466, 468, 761, 765, 766 | taught | MA-068 (polytope, G-1518) |
| Pontryagin set subtraction (see Set algebra) |  | index-noise | cross-reference to "Set algebra" |
| Positive definite | 121, 629, 695 | taught | MA-064 (positive definite: all eigenvalues positive) |
| Positive semidefinite | 121, 629 | taught | MA-068 (positive semidefinite matrix in a convex QP) |
| Principle of optimality | 734 | taught | Note 10 (principle of optimality) |
| Probability |  | index-noise | grouping header for the sub-entries below |
| Probability, conditional density | 27, 672 | taught | MA-015 (conditional probability); MA-014 |
| Probability, density | 27, 654 | taught | MA-022 (PDF) |
| Probability, distribution | 27, 654 | taught | MA-020 (random variables and distributions) |
| Probability, marginal density | 27, 659 | taught | MA-014 (joint, marginal, conditional probability) |
| Probability, moments | 655 | taught | MA-012 (expected value and variance) |
| Probability, multivariate density | 27, 659 | taught | MA-073 (multivariate normal) |
| Probability, noninvertible transformations | 666 | out-of-scope | probability-theory detail (degenerate densities, characteristic functions, non-invertible transforms; RMD App. A) |
| Projection | 97, 111, 447, 731, 756, 763, 765, 767 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Proportional-integral-derivative (see PID control) |  | index-noise | cross-reference to "PID control" |
| Pseudo-inverse | 625 | taught | MA-060 (pseudo-inverse) |
| Pseudospectral method | 541 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Python | 528 | out-of-scope | software or tool name, not a concept |
| Q-convergence |  | index-noise | grouping header for the sub-entries below |
| Q-convergence, q-linearly | 511 | out-of-scope | convergence-rate classes of Newton-type methods (RMD 8.3): numerical-analysis detail |
| Q-convergence, q-quadratically | 511 | out-of-scope | convergence-rate classes of Newton-type methods (RMD 8.3): numerical-analysis detail |
| Q-convergence, q-superlinearly | 511 | out-of-scope | convergence-rate classes of Newton-type methods (RMD 8.3): numerical-analysis detail |
| Q-function | 279, 281–283 | out-of-scope | estimator convergence and stability theory (RMD ch.4), research depth |
| QP | 100, 364, 437, 449, 451, 547 | taught | MA-068 (quadratic programming); Note 207 |
| QP, parametric | 451 | out-of-scope | parametric-programming detail of explicit MPC (RMD ch.7), research depth beyond the explicit-MPC add |
| QP, parametric piecewise | 463 | out-of-scope | parametric-programming detail of explicit MPC (RMD ch.7), research depth beyond the explicit-MPC add |
| Quadratic |  | index-noise | grouping header for the sub-entries below |
| Quadratic, piecewise | 104, 450, 452, 458, 463, 464, 468, 761 | add | **Explicit MPC: the MPC law precomputed offline as a piecewise-affine lookup table** (control) -> RO-15 (extend Note 207) |
| Quadratic program (see QP) |  | index-noise | cross-reference to "QP" |
| Quadrature state | 532 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Radau IIA collocation methods | 505, 540 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Random variable | 654 | taught | MA-020 (random variables) |
| Random variable, independent | 27 | taught | MA-016 (independent events); MA-033 |
| Range | 624 | taught | MA-047 (column space of a matrix) |
| RAS | 229, 313 | out-of-scope | nonlinear robust-stability notions (ISS/IOSS, comparison functions K/KL; RMD App. B), graduate-level theory |
| Reachability Gramian | 683 | out-of-scope | Gramian energy tests: an alternative to the rank test (RMD App. A), beyond beginner depth |
| Real-time iterations | 573 | taught | Note 208 (real-time iteration) |
| Receding horizon control (see RHC) |  | index-noise | cross-reference to "RHC" |
| Recursive feasibility (see Feasibility) |  | index-noise | cross-reference to "Feasibility" |
| Recursive least squares | 38, 75 | taught | plan §4 new MA: Recursive least squares (first needed by Note 80) |
| Reduced Hessian | 547 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Region of attraction (see Attraction) |  | index-noise | cross-reference to "Attraction" |
| Regularization | 206–209 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Regulation | 89, 350 | taught | Note 204 (state feedback regulation to the origin); Note 205 (LQR = regulator) |
| Regulation, combining with MHE | 312 | add | **State observer (Luenberger), output feedback and the separation principle; LQG; output-feedback MPC (estimator + controller)** (control) -> RO-15 (new Note after Note 204) |
| Regulation, duality with estimation | 290 | add | **Observability rank test, stabilizability and detectability; duality of control and estimation** (control) -> RO-15 (new Note after Note 204, together with observers) |
| Relative gain array (see RGA) |  | index-noise | cross-reference to "RGA" |
| Reverse mode (see AD) |  | index-noise | cross-reference to "AD" |
| RGA | 385 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| RGAS | 207, 272, 710 | out-of-scope | nonlinear robust-stability notions (ISS/IOSS, comparison functions K/KL; RMD App. B), graduate-level theory |
| RGAS, convolution maximization form | 273 | out-of-scope | nonlinear robust-stability notions (ISS/IOSS, comparison functions K/KL; RMD App. B), graduate-level theory |
| RGES | 285 | out-of-scope | nonlinear robust-stability notions (ISS/IOSS, comparison functions K/KL; RMD App. B), graduate-level theory |
| RHC | 108, 109, 135, 163, 217 | taught | Note 207 (receding horizon) |
| Riccati equation | 20, 68, 69, 71, 136, 291, 369 | taught | Note 205 (Riccati equation) |
| Riccati recursion | 558 | taught | Note 205 (Riccati recursion) |
| RK | 498 | taught | plan §4 new MA: Numerical integration of ODEs (Runge-Kutta steps) |
| RK, classical (RK4) | 497 | taught | plan §4 new MA: Numerical integration of ODEs (Runge-Kutta) |
| RK, explicit | 496 | taught | plan §4 new MA: Numerical integration of ODEs (Runge-Kutta) |
| RK, implicit | 501 | add | **ODE solving basics: initial- vs boundary-value problems, explicit vs implicit integrators, stiff equations, step size, local and global error** (maths) -> MA 06-calculus (extend the planned 'Numerical integration of ODEs' Note) |
| Robust min-max MPC | 220 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Robust MPC | 193, 200 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Robust MPC, min-max | 220 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Robust MPC, tube-based | 223 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Robustly asymptotically stable (see RAS) |  | index-noise | cross-reference to "RAS" |
| Robustly globally asymptotically stable (see RGAS) |  | index-noise | cross-reference to "RGAS" |
| Robustly globally exponentially stable (see RGES) |  | index-noise | cross-reference to "RGES" |
| Robustness |  | index-noise | grouping header for the sub-entries below |
| Robustness, inherent | 204 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Robustness, nominal | 204, 709 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Robustness, of nominal MPC | 209 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Runge-Kutta method (see RK) |  | index-noise | cross-reference to "RK" |
| Scenario optimization | 254 | out-of-scope | sampling-based solution method for stochastic MPC (RMD 3.6), research depth |
| Schur decomposition | 629 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Schur decomposition, real | 401, 630 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Semicontinuity |  | index-noise | grouping header for the sub-entries below |
| Semicontinuity, inner | 757 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Semicontinuity, outer | 757 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Sequence | 632 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Sequence, accumulation point | 632, 759 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Sequence, convergence | 632 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Sequence, limit | 632, 679, 680, 759 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Sequence, monotone | 632 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Sequence, nondecreasing | 44 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Sequence, nonincreasing | 25 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Sequence, subsequence | 632 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Sequential optimal control | 491, 562 | taught | Note 116 (single shooting = sequential approach) |
| Sequential optimal control, plain dense | 563 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Sequential optimal control, sparsity-exploiting | 563 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Sequential quadratic programming (see SQP) |  | index-noise | cross-reference to "SQP" |
| Set |  | index-noise | grouping header for the sub-entries below |
| Set, affine | 632 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Set, algebra | 224 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Set, boundary | 631 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Set, bounded | 631 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Set, closed | 631 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Set, compact | 631 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Set, complement | 631 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Set, interior | 631 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Set, level | 16, 137 | taught | MA-067 (level sets) |
| Set, open | 631 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Set, quasiregular | 751 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Set, regular | 749 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Set, relative interior | 632 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Set, sublevel | 137 | taught | MA-067 (level/sublevel sets of a convex function) |
| Set-valued function | 99, 472, 755–757 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Setpoint |  | index-noise | grouping header for the sub-entries below |
| Setpoint, nonzero | 46, 349 | taught | Note 206 (tracking a reference: steady-state target) |
| Shift initialization | 571 | taught | Note 208 (warm starts) |
| Short horizon syndrome | 311 | out-of-scope | estimator convergence and stability theory (RMD ch.4), research depth |
| Sigma points | 305 | taught | Note 256 (sigma points) |
| Simultaneous optimal control | 490 | taught | Note 116 (multiple shooting and collocation = simultaneous approach) |
| Singular-value decomposition (see SVD) |  | index-noise | cross-reference to "SVD" |
| Space |  | index-noise | grouping header for the sub-entries below |
| Space, linear | 624 | taught | MA-047 (vector space) |
| Space, vector | 624 | taught | MA-047 (vector space) |
| Sparsity | 491 | taught | Note 207 (condensed vs sparse QP) |
| SQP | 551, 589 | taught | Note 208 (SQP, overview) |
| SQP, feasibility perturbed | 566 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| SQP, local convergence | 552 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Stability | 112 | taught | plan §4 new MA: Stability of dynamical systems |
| Stability, asymptotic | 112, 423, 698 | add | **Stability definitions: equilibrium, Lyapunov stable, asymptotically and exponentially stable, local vs global, region of attraction; stability from the linearisation (Lyapunov's indirect method)** (maths) -> MA 06-calculus (extend the planned 'Stability of dynamical systems' Note) |
| Stability, constrained | 699 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Stability, exponential | 120, 698 | add | **Stability definitions: equilibrium, Lyapunov stable, asymptotically and exponentially stable, local vs global, region of attraction; stability from the linearisation (Lyapunov's indirect method)** (maths) -> MA 06-calculus (extend the planned 'Stability of dynamical systems' Note) |
| Stability, global | 112, 698 | add | **Stability definitions: equilibrium, Lyapunov stable, asymptotically and exponentially stable, local vs global, region of attraction; stability from the linearisation (Lyapunov's indirect method)** (maths) -> MA 06-calculus (extend the planned 'Stability of dynamical systems' Note) |
| Stability, global asymptotic | 112, 126, 408, 433, 698 | add | **Stability definitions: equilibrium, Lyapunov stable, asymptotically and exponentially stable, local vs global, region of attraction; stability from the linearisation (Lyapunov's indirect method)** (maths) -> MA 06-calculus (extend the planned 'Stability of dynamical systems' Note) |
| Stability, global asymptotic (KL version) | 699 | out-of-scope | nonlinear robust-stability notions (ISS/IOSS, comparison functions K/KL; RMD App. B), graduate-level theory |
| Stability, global attractive | 112 | add | **Stability definitions: equilibrium, Lyapunov stable, asymptotically and exponentially stable, local vs global, region of attraction; stability from the linearisation (Lyapunov's indirect method)** (maths) -> MA 06-calculus (extend the planned 'Stability of dynamical systems' Note) |
| Stability, global exponential | 120, 698 | add | **Stability definitions: equilibrium, Lyapunov stable, asymptotically and exponentially stable, local vs global, region of attraction; stability from the linearisation (Lyapunov's indirect method)** (maths) -> MA 06-calculus (extend the planned 'Stability of dynamical systems' Note) |
| Stability, inherent | 91 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Stability, local | 112, 698 | add | **Stability definitions: equilibrium, Lyapunov stable, asymptotically and exponentially stable, local vs global, region of attraction; stability from the linearisation (Lyapunov's indirect method)** (maths) -> MA 06-calculus (extend the planned 'Stability of dynamical systems' Note) |
| Stability, nominal | 91 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Stability, robust asymptotic (see RAS) |  | index-noise | cross-reference to "RAS" |
| Stability, robust exponential | 235 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Stability, robust global asymptotic (see RGAS) |  | index-noise | cross-reference to "RGAS" |
| Stability, time-varying systems | 125 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Stability, with disturbances | 712 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Stabilizability | 68, 120 | add | **Observability rank test, stabilizability and detectability; duality of control and estimation** (control) -> RO-15 (new Note after Note 204, together with observers) |
| Stabilizability, duality with detectability | 291 | add | **Observability rank test, stabilizability and detectability; duality of control and estimation** (control) -> RO-15 (new Note after Note 204, together with observers) |
| Stabilizable | 26, 46, 68, 73, 136, 140, 714 | add | **Observability rank test, stabilizability and detectability; duality of control and estimation** (control) -> RO-15 (new Note after Note 204, together with observers) |
| Stage cost | 18, 153 | add | **Optimal-control problem anatomy: stage (running) cost, additive cost over the horizon, terminal cost, cost-to-go / time to go** (control) -> RO-15 (extend Note 205) |
| Stage cost, economic | 153 | out-of-scope | economic MPC: process-industry profit objective and dissipativity theory (RMD 2.8), research depth |
| State estimation (see Estimation) |  | index-noise | cross-reference to "Estimation" |
| Statistical independence | 668 | taught | MA-016 (independent events) |
| Steady-state target | 48, 352 | taught | Note 206 (steady-state target) |
| Steady-state target, distributed | 410 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Stiff equations | 500 | add | **ODE solving basics: initial- vs boundary-value problems, explicit vs implicit integrators, stiff equations, step size, local and global error** (maths) -> MA 06-calculus (extend the planned 'Numerical integration of ODEs' Note) |
| Stochastic MPC | 193, 200, 246 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Stochastic MPC, stabilizing conditions | 248 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Stochastic MPC, tightened constraints | 253 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Stochastic MPC, tube-based | 250 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Storage function | 156 | out-of-scope | economic MPC: process-industry profit objective and dissipativity theory (RMD 2.8), research depth |
| Strong duality (see Duality) |  | index-noise | cross-reference to "Duality" |
| Subgradient | 640 | taught | DL-006 (subgradient, G-1910) |
| Subgradient, convex function | 762 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Sublevel set | 137, 648 | taught | MA-067 (sublevel sets) |
| Suboptimal MPC | 147, 369 | taught | Note 208 (stopping early: suboptimal real-time MPC) |
| Suboptimal MPC, asymptotic stability | 151 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Suboptimal MPC, distributed | 369 | out-of-scope | distributed / plantwide MPC for chemical plants (RMD ch.6); multi-robot coordination is covered by Notes 212-214 and 271-274 |
| Suboptimal MPC, exponential stability | 372 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Subspace |  | index-noise | grouping header for the sub-entries below |
| Subspace, linear | 624 | taught | MA-058 (subspaces: column space and null space) |
| Supply rate | 156 | out-of-scope | economic MPC: process-industry profit objective and dissipativity theory (RMD 2.8), research depth |
| Support function | 648 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| SVD | 627 | taught | MA-057 (SVD geometry); MA-058 |
| System |  | index-noise | grouping header for the sub-entries below |
| System, composite | 343, 345 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| System, deterministic | 9, 196, 333 | taught | plan §4 new MA: State-space models |
| System, discontinuous | 206 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| System, linear | 2, 133, 224, 228, 338 | taught | plan §4 new MA: State-space models (linear) |
| System, noisy | 269 | taught | Note 80 (linear Gaussian system) |
| System, nominal | 238 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| System, nonlinear | 2, 93, 123, 139, 236 | taught | plan §4 new MA: State-space models (nonlinear systems) |
| System, periodic | 133 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| System, time-invariant | 3, 5, 10, 93, 338 | add | **Linear time-invariant (LTI) vs time-varying systems** (maths) -> MA 06-calculus (extend the planned State-space models Note) |
| System, time-varying | 2, 123, 141, 347, 437 | add | **Linear time-invariant (LTI) vs time-varying systems** (maths) -> MA 06-calculus (extend the planned State-space models Note) |
| System, uncertain | 193, 195, 196, 333, 334, 338 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Tangent cone (see Cone) |  | index-noise | cross-reference to "Cone" |
| Taylor series | 3, 64 | taught | MA-061 (Taylor series) |
| Taylor’s theorem | 143 | taught | MA-064 (multivariate Taylor) |
| Terminal constraint (see Constraints) |  | index-noise | cross-reference to "Constraints" |
| Terminal region | 93 | taught | Note 207 (terminal set) |
| Time to go | 108, 109, 196, 217, 469 | add | **Optimal-control problem anatomy: stage (running) cost, additive cost over the horizon, terminal cost, cost-to-go / time to go** (control) -> RO-15 (extend Note 205) |
| Trace | 73, 681 | add | **Trace of a matrix** (maths) -> MA 05-linear-algebra (short section) |
| Tracking | 46 | taught | Note 206 (LQR for tracking a reference) |
| Tracking, periodic target | 142 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Transfer function | 4, 6, 179, 383 | add | **Transfer functions (input-output models of linear systems)** (control) -> RO-06 (new Note) |
| Trust region | 514 | taught | Note 38 (trust region); MA-064 |
| Tube | 202, 335 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Tube, bounding | 226 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Tube, outer-bounding | 224 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Tube-based robust MPC | 223 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Tube-based robust MPC, feedback controller | 228 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Tube-based robust MPC, improved | 234 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Tube-based robust MPC, linear systems | 228 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Tube-based robust MPC, model predictive controller | 238 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Tube-based robust MPC, nominal controller | 228 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Tube-based robust MPC, nominal trajectory | 238 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Tube-based robust MPC, nonlinear systems | 236 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Tube-based robust MPC, tightened constraints | 230, 242 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Two-player game |  | index-noise | grouping header for the sub-entries below |
| Two-player game, constrained | 400 | out-of-scope | game formulations used only to analyse distributed MPC (RMD ch.6) |
| Two-player game, coupled input constraints | 405 | out-of-scope | game formulations used only to analyse distributed MPC (RMD ch.6) |
| Two-player game, unconstrained | 374 | out-of-scope | game formulations used only to analyse distributed MPC (RMD ch.6) |
| Two-player game, uncoupled input constraints | 402 | out-of-scope | game formulations used only to analyse distributed MPC (RMD ch.6) |
| UKF | 304–306 | taught | Note 256 (unscented Kalman filter) |
| Uncertainty | 193 | taught | Note 63 (sources of uncertainty) |
| Uncertainty, parametric | 194 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Uncontrollable | 22 | taught | Note 204 (controllability rank test: uncontrollable when rank deficient) |
| Unit ball | 631 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Unscented Kalman filter (see UKF) |  | index-noise | cross-reference to "UKF" |
| Value function | 13, 92, 204, 240 | taught | Note 9 (value functions); Note 14 (cost-to-go) |
| Value function, continuity | 104, 208, 759 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Value function, discontinuity | 104 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Value function, Lipschitz continuity | 760 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Variable |  | index-noise | grouping header for the sub-entries below |
| Variable, controlled | 47 | taught | plan §4 new MA: State-space models (outputs to control) |
| Variable, disturbance | 49 | taught | Note 208 (disturbances) |
| Variable, dual | 543 | taught | MA-068 (dual problem and dual variables) |
| Variable, input | 2 | taught | plan §4 new MA: State-space models (input u) |
| Variable, output | 2 | taught | plan §4 new MA: State-space models (outputs) |
| Variable, primal | 543 | taught | MA-068 (primal and dual problems) |
| Variable, random | 27, 654 | taught | MA-020 (random variables) |
| Variable, random, independent | 27, 654 | taught | MA-016 (independence) |
| Variable, state | 2 | taught | plan §4 new MA: State-space models (state x) |
| Vertex | 471 | taught | MA-068 (vertex of the feasible polytope, simplex) |
| Warm start | 148, 183, 221, 370, 391, 404, 413, 433, 555 | taught | Note 208 (warm starts) |
| Warm start, shift initialization | 571 | taught | Note 208 (warm starts by shifting the last solution) |
| Weak controllability (see Controllability) |  | index-noise | cross-reference to "Controllability" |
| Weak duality (see Duality) |  | index-noise | cross-reference to "Duality" |
| Weierstrass theorem | 97, 99, 294, 372, 636 | out-of-scope | real-analysis / convex-analysis background used for proofs (RMD App. A, C), not a robotics skill |
| Z-transform | 5 | add | **Z-transform and discrete-time transfer functions** (maths) -> MA 06-calculus (new Note after the Laplace transform) |

## Murray, Li & Sastry, *A Mathematical Introduction to Robotic Manipulation* (1994) -- replacement term list

**No official free copy now.** The authors' site (http://www.cds.caltech.edu/~murray/mlswiki/) states: '20 Jan 2020: The publisher has decided that the PDF for this book can no longer be made available online' and 'Those links are now broken'. A stale copy still sits on the server, but it is no longer offered with permission, so it was not used. Closest free official replacement: the same book's official sources -- (1) the full section-level table of contents on the publisher's page (Routledge/CRC, https://www.routledge.com/A-Mathematical-Introduction-to-Robotic-Manipulation/Murray-Li-Sastry/p/book/9781138440166), and (2) the authors' official chapter pages on MLSwiki, whose 'Chapter Summary' lists each chapter's key concepts in italics (fetched as wiki source with `action=raw`). Reason: it keeps the requested book and its own vocabulary; Modern Robotics (Lynch & Park), the nearest free book, is already checked by agent `robo`. Limitation: 151 terms instead of a full back index (no page numbers; 'Pages' gives the chapter).

Counts: taught 70, mentioned-only 0, add 23, out-of-scope 55, index-noise 3 (total 151).

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| Introduction | Ch1 | index-noise | chapter title (Introduction) |
| Brief History | Ch1 | out-of-scope | history of the field |
| Multifingered Hands and Dextrous Manipulation | Ch1 | taught | Note 331 (dexterous in-hand manipulation with a multi-finger hand) |
| Outline of the Book | Ch1 | index-noise | book outline heading |
| Rigid Body Motion | Ch2 | taught | Note 275 (twists, screws); plan §4 new MA: Rigid-body transforms and homogeneous coordinates |
| Rigid Body Transformations | Ch2 | taught | plan §4 new MA: Rigid-body transforms and homogeneous coordinates |
| Rotational Motion in R3 | Ch2 | taught | plan §4 new MA: 3D rotations: Euler angles and quaternions; plan §4 Axis-angle, exponential and log maps |
| Rigid Motion in R3 | Ch2 | taught | plan §4 new MA: Rigid-body transforms (SE(3)); Note 275 (screw motion) |
| Velocity of a Rigid Body | Ch2 | taught | Note 275 (twist: angular and linear velocity as one vector) |
| Wrenches and Reciprocal Screws | Ch2 | taught | Note 275 (wrench; moving it between frames) |
| Manipulator Kinematics | Ch3 | taught | Note 69 (kinematic chains and forward kinematics); Note 276 |
| Forward Kinematics | Ch3 | taught | Note 276 (product of exponentials forward kinematics) |
| Inverse Kinematics | Ch3 | taught | Note 279 (inverse kinematics) |
| The Manipulator Jacobian | Ch3 | taught | Note 277 (manipulator Jacobian) |
| Redundant and Parallel Manipulators | Ch3 | add | **Closed chains and parallel robots: loop-closure (structure) equations** (robotics) -> RB-01 (new Note) |
| Robot Dynamics And Control | Ch4 | taught | Note 281 (manipulator equation); Note 284 (joint-space control) |
| Lagrange's Equations | Ch4 | taught | Note 281 (Lagrangian mechanics, Euler-Lagrange equation) |
| Dynamics of Open-Chain Manipulators | Ch4 | taught | Note 281 (manipulator equation) |
| Lyapunov Stability Theory | Ch4 | taught | Note 199 (Lyapunov stability certificates); plan §4 Lyapunov functions |
| Position Control and Trajectory Tracking | Ch4 | taught | Note 284 (PD plus gravity, computed torque) |
| Control of Constrained Manipulators | Ch4 | taught | Note 286 (hybrid motion-force control; natural and artificial constraints) |
| Multifingered Hand Kinematics | Ch5 | taught | Note 288 (contact kinematics); Note 290 (grasp matrix) |
| Introduction to Grasping | Ch5 | taught | Note 290 (form closure, force closure, grasp matrix) |
| Grasp Statics | Ch5 | taught | Note 290 (grasp matrix: contact forces to object wrench) |
| Force-Closure | Ch5 | taught | Note 290 (force closure) |
| Grasp Planning | Ch5 | taught | Note 291 (grasp quality and grasp selection) |
| Grasp Constraints | Ch5 | add | **Hand Jacobian and the grasp constraint: finger joint velocities to object twist; manipulable grasps** (robotics) -> RB-03 (extend Note 290) |
| Rolling Contact Kinematics | Ch5 | taught | Note 288 (contact kinematics: rolling) |
| Hand Dynamics And Control | Ch6 | out-of-scope | model-based multifingered-hand dynamics and control (MLS ch.6): graduate depth; the plan teaches dexterous hands by learning (Notes 331-332) |
| Lagrange's Equations with Constraints | Ch6 | taught | Note 289 (constrained dynamics: contact forces as Lagrange multipliers) |
| Robot Hand Dynamics | Ch6 | out-of-scope | model-based multifingered-hand dynamics and control (MLS ch.6): graduate depth; the plan teaches dexterous hands by learning (Notes 331-332) |
| Redundant and Nonmanipulable Robot Systems | Ch6 | out-of-scope | model-based multifingered-hand dynamics and control (MLS ch.6): graduate depth; the plan teaches dexterous hands by learning (Notes 331-332) |
| Kinematics and Statics of Tendon Actuation | Ch6 | out-of-scope | tendon-routing kinematics for hand design (MLS 6.4): specialist hand design; no plan Note models tendons |
| Control of Robot Hands | Ch6 | out-of-scope | model-based multifingered-hand dynamics and control (MLS ch.6): graduate depth; the plan teaches dexterous hands by learning (Notes 331-332) |
| Nonholonomic Behavior In Robotic Systems | Ch7 | taught | Note 64 (holonomic vs nonholonomic constraints) |
| Controllability and Frobenius' Theorem | Ch7 | out-of-scope | differential-geometric nonholonomic / Lie-group theory (MLS ch.7, App. A); plan dropped PA 15.10-15.11 and PA 4.6; car controllability in plain words is Note 67 |
| Examples of Nonholonomic Systems | Ch7 | taught | Note 64 (differential drive, simple car); Note 66; Note 67 |
| Structure of Nonholonomic Systems | Ch7 | out-of-scope | differential-geometric nonholonomic / Lie-group theory (MLS ch.7, App. A); plan dropped PA 15.10-15.11 and PA 4.6; car controllability in plain words is Note 67 |
| Nonholonomic Motion Planning | Ch8 | taught | Note 112 (planning with motion limits: Dubins and Reeds-Shepp car paths) |
| Steering Model Control Systems Using Sinusoids | Ch8 | out-of-scope | nonholonomic steering by sinusoids / chained form (MLS ch.8); plan dropped PA 15.12; car planning uses Dubins/Reeds-Shepp and Hybrid A* (Notes 112-113) |
| General Methods for Steering | Ch8 | out-of-scope | nonholonomic steering by sinusoids / chained form (MLS ch.8); plan dropped PA 15.12; car planning uses Dubins/Reeds-Shepp and Hybrid A* (Notes 112-113) |
| Dynamic Finger Repositioning | Ch8 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Future Prospects | Ch9 | out-of-scope | application-survey chapter of 1994 prospects (MLS ch.9), no teachable concept |
| Robots in Hazardous Environments | Ch9 | out-of-scope | application-survey chapter of 1994 prospects (MLS ch.9), no teachable concept |
| Medical Applications for Multifingered Hands | Ch9 | out-of-scope | application-survey chapter of 1994 prospects (MLS ch.9), no teachable concept |
| Robots on a Small Scale: Microrobotics | Ch9 | out-of-scope | application-survey chapter of 1994 prospects (MLS ch.9), no teachable concept |
| Appendices | AppA | index-noise | appendices heading |
| Lie Groups and Robot Kinematics | AppA | out-of-scope | differential-geometric nonholonomic / Lie-group theory (MLS ch.7, App. A); plan dropped PA 15.10-15.11 and PA 4.6; car controllability in plain words is Note 67 |
| A Mathematica Package for Screw Calculus | AppA | out-of-scope | software or tool name, not a concept |
| special orthogonal group SO(3) | Ch2 | taught | Note 65 (rotation matrix: columns are axes, inverse = transpose) |
| Euler angles (fixed and Euler angle sets) | Ch2 | taught | plan §4 new MA: 3D rotations: Euler angles and quaternions |
| unit quaternions | Ch2 | taught | plan §4 new MA: 3D rotations: Euler angles and quaternions |
| configuration (SE(3), homogeneous coordinates) | Ch2 | taught | plan §4 new MA: Rigid-body transforms and homogeneous coordinates (SE(3)) |
| rigid body transformation as exponential of a twist | Ch2 | taught | Note 275 (exponential coordinates of a rigid motion) |
| twist coordinates | Ch2 | taught | Note 275 (twist as a 6-number vector) |
| screw (pitch, axis, magnitude) | Ch2 | taught | Note 275 (screw axis) |
| pure rotation | Ch2 | taught | Note 275 (screw motion; zero pitch = pure rotation) |
| pure translation | Ch2 | taught | Note 275 (screw motion; infinite pitch = pure translation) |
| spatial velocity | Ch2 | add | **Spatial (space-frame) vs body-frame twists and wrenches** (robotics) -> RB-01 (extend Note 275) |
| body velocity | Ch2 | add | **Spatial (space-frame) vs body-frame twists and wrenches** (robotics) -> RB-01 (extend Note 275) |
| adjoint transformation | Ch2 | taught | Note 275 (the adjoint map moves a twist between frames) |
| wrench (force, moment pair) | Ch2 | taught | Note 275 (wrench: force and torque as one vector) |
| equivalent wrench | Ch2 | taught | Note 275 (moving a wrench between frames) |
| spatial wrench | Ch2 | add | **Spatial (space-frame) vs body-frame twists and wrenches** (robotics) -> RB-01 (extend Note 275) |
| body wrench | Ch2 | add | **Spatial (space-frame) vs body-frame twists and wrenches** (robotics) -> RB-01 (extend Note 275) |
| reciprocal twist and wrench | Ch2 | out-of-scope | screw-theory reciprocity machinery (MLS 2.5); contact kinematics is taught in Note 288 at beginner level |
| reciprocal product | Ch2 | out-of-scope | screw-theory reciprocity machinery (MLS 2.5); contact kinematics is taught in Note 288 at beginner level |
| system of screws | Ch2 | out-of-scope | screw-theory reciprocity machinery (MLS 2.5); contact kinematics is taught in Note 288 at beginner level |
| reciprocal screw system | Ch2 | out-of-scope | screw-theory reciprocity machinery (MLS 2.5); contact kinematics is taught in Note 288 at beginner level |
| Lie subgroups of SE(3) for joints | Ch2 | out-of-scope | differential-geometric nonholonomic / Lie-group theory (MLS ch.7, App. A); plan dropped PA 15.10-15.11 and PA 4.6; car controllability in plain words is Note 67 |
| forward kinematics | Ch3 | taught | Note 69 (forward kinematics); Note 276 |
| product of exponentials formula | Ch3 | taught | Note 276 (product of exponentials) |
| workspace (complete) | Ch3 | taught | Note 276 (workspace) |
| reachable workspace | Ch3 | add | **Reachable vs dexterous workspace** (robotics) -> RB-01 (extend Note 276) |
| dextrous workspace | Ch3 | add | **Reachable vs dexterous workspace** (robotics) -> RB-01 (extend Note 276) |
| inverse kinematics | Ch3 | taught | Note 279 (inverse kinematics) |
| Paden-Kahan subproblems | Ch3 | add | **Paden-Kahan subproblems for analytic inverse kinematics** (robotics) -> RB-01 (extend Note 279) |
| manipulator Jacobian (spatial and body) | Ch3 | taught | Note 277 (manipulator Jacobian, space and body forms) |
| singular configuration | Ch3 | taught | Note 278 (singularities) |
| manipulability | Ch3 | taught | Note 278 (manipulability) |
| kinematically redundant | Ch3 | taught | Note 278 (redundancy) |
| self-motion manifold | Ch3 | taught | Note 278 (self-motion in the null space) |
| internal motions | Ch3 | taught | Note 278 (self-motion in the null space) |
| parallel manipulator | Ch3 | add | **Closed chains and parallel robots: loop-closure (structure) equations** (robotics) -> RB-01 (new Note) |
| structure equation | Ch3 | add | **Closed chains and parallel robots: loop-closure (structure) equations** (robotics) -> RB-01 (new Note) |
| Lagrange's equations | Ch4 | taught | Note 281 (Euler-Lagrange equation) |
| generalized coordinates | Ch4 | add | **Generalized coordinates and generalized forces** (robotics) -> RB-02 (extend Note 281) |
| generalized forces | Ch4 | add | **Generalized coordinates and generalized forces** (robotics) -> RB-02 (extend Note 281) |
| Newton-Euler equations | Ch4 | taught | Note 220 (F = ma plus Euler's equation); Note 282 (recursive Newton-Euler) |
| inertia tensor | Ch4 | taught | Note 220 (the 3x3 inertia matrix) |
| manipulator equations of motion M(q) C N | Ch4 | taught | Note 281 (manipulator equation) |
| mass matrix symmetric positive definite | Ch4 | taught | Note 281 (what the mass matrix means) |
| skew-symmetry of Mdot-2C | Ch4 | out-of-scope | passivity property (skew-symmetric Mdot - 2C), a stability-proof property (MLS 4.2) |
| equilibrium point | Ch4 | taught | plan §4 new MA: Stability of dynamical systems (equilibria) |
| locally asymptotically stable | Ch4 | add | **Stability definitions: equilibrium, Lyapunov stable, asymptotically and exponentially stable, local vs global, region of attraction; stability from the linearisation (Lyapunov's indirect method)** (maths) -> MA 06-calculus (extend the planned 'Stability of dynamical systems' Note) |
| direct method of Lyapunov | Ch4 | taught | Note 199 (Lyapunov stability certificates) |
| LaSalle's invariance principle | Ch4 | add | **LaSalle's invariance principle** (maths) -> MA 06-calculus (short section in the planned Stability Note) |
| indirect method of Lyapunov (linearization) | Ch4 | add | **Stability definitions: equilibrium, Lyapunov stable, asymptotically and exponentially stable, local vs global, region of attraction; stability from the linearisation (Lyapunov's indirect method)** (maths) -> MA 06-calculus (extend the planned 'Stability of dynamical systems' Note) |
| exponential stability | Ch4 | add | **Stability definitions: equilibrium, Lyapunov stable, asymptotically and exponentially stable, local vs global, region of attraction; stability from the linearisation (Lyapunov's indirect method)** (maths) -> MA 06-calculus (extend the planned 'Stability of dynamical systems' Note) |
| computed torque control law | Ch4 | taught | Note 284 (computed torque) |
| augmented PD control law | Ch4 | out-of-scope | variant tracking law (augmented PD, MLS 4.5); Note 284 teaches PD plus gravity and computed torque, the two standard forms |
| exponential trajectory tracking | Ch4 | add | **Stability definitions: equilibrium, Lyapunov stable, asymptotically and exponentially stable, local vs global, region of attraction; stability from the linearisation (Lyapunov's indirect method)** (maths) -> MA 06-calculus (extend the planned 'Stability of dynamical systems' Note) |
| workspace control | Ch4 | taught | Note 285 (task-space motion control) |
| contact (contact basis) | Ch5 | taught | Note 288 (contact types) |
| friction cone | Ch5 | taught | Note 288 (friction cone) |
| contact with friction (soft finger, point contact) | Ch5 | taught | Note 288 (point with friction, soft finger) |
| grasp | Ch5 | taught | Note 290 (grasp) |
| grasp map | Ch5 | taught | Note 290 (grasp matrix) |
| force-closure | Ch5 | taught | Note 290 (force closure) |
| internal force | Ch5 | add | **Internal (squeezing) forces in a grasp: null space of the grasp matrix** (robotics) -> RB-03 (extend Note 290) |
| fundamental grasp constraint | Ch5 | add | **Hand Jacobian and the grasp constraint: finger joint velocities to object twist; manipulable grasps** (robotics) -> RB-03 (extend Note 290) |
| hand Jacobian | Ch5 | add | **Hand Jacobian and the grasp constraint: finger joint velocities to object twist; manipulable grasps** (robotics) -> RB-03 (extend Note 290) |
| manipulable grasp | Ch5 | add | **Hand Jacobian and the grasp constraint: finger joint velocities to object twist; manipulable grasps** (robotics) -> RB-03 (extend Note 290) |
| contact kinematics | Ch5 | taught | Note 288 (contact kinematics) |
| rolling contact | Ch5 | taught | Note 288 (rolling contact) |
| Pfaffian constraints | Ch6 | add | **Pfaffian velocity constraints A(q) q-dot = 0** (robotics) -> RO-01 (extend Note 64) |
| Lagrange multipliers | Ch6 | taught | MA-066 (Lagrange multipliers); Note 289 |
| Lagrange-d'Alembert formulation | Ch6 | out-of-scope | analytical-mechanics formulation (d'Alembert, stationary action, Hamiltonian; MLS 6.2, UA App. B.3); the plan derives dynamics by Lagrange (Note 281) and multipliers (Note 289); Hamiltonian dropped in plan §7 |
| multifingered robot hand dynamics | Ch6 | out-of-scope | model-based multifingered-hand dynamics and control (MLS ch.6): graduate depth; the plan teaches dexterous hands by learning (Notes 331-332) |
| redundant robot systems | Ch6 | out-of-scope | model-based multifingered-hand dynamics and control (MLS ch.6): graduate depth; the plan teaches dexterous hands by learning (Notes 331-332) |
| nonmanipulable robot systems | Ch6 | out-of-scope | model-based multifingered-hand dynamics and control (MLS ch.6): graduate depth; the plan teaches dexterous hands by learning (Notes 331-332) |
| internal motions | Ch6 | taught | Note 278 (self-motion in the null space) |
| tendon-driven systems | Ch6 | out-of-scope | tendon-routing kinematics for hand design (MLS 6.4): specialist hand design; no plan Note models tendons |
| extension functions | Ch6 | out-of-scope | tendon-routing kinematics for hand design (MLS 6.4): specialist hand design; no plan Note models tendons |
| coupling matrix | Ch6 | out-of-scope | tendon-routing kinematics for hand design (MLS 6.4): specialist hand design; no plan Note models tendons |
| tendon force-closure | Ch6 | out-of-scope | tendon-routing kinematics for hand design (MLS 6.4): specialist hand design; no plan Note models tendons |
| nonholonomic constraints | Ch7 | taught | Note 64 (nonholonomic constraints) |
| nonholonomic motion planning | Ch7 | taught | Note 112 (Dubins and Reeds-Shepp paths for car-like robots); Note 113 |
| Lie bracket | Ch7 | out-of-scope | differential-geometric nonholonomic / Lie-group theory (MLS ch.7, App. A); plan dropped PA 15.10-15.11 and PA 4.6; car controllability in plain words is Note 67 |
| distribution | Ch7 | out-of-scope | differential-geometric nonholonomic / Lie-group theory (MLS ch.7, App. A); plan dropped PA 15.10-15.11 and PA 4.6; car controllability in plain words is Note 67 |
| regular distribution | Ch7 | out-of-scope | differential-geometric nonholonomic / Lie-group theory (MLS ch.7, App. A); plan dropped PA 15.10-15.11 and PA 4.6; car controllability in plain words is Note 67 |
| involutive distribution | Ch7 | out-of-scope | differential-geometric nonholonomic / Lie-group theory (MLS ch.7, App. A); plan dropped PA 15.10-15.11 and PA 4.6; car controllability in plain words is Note 67 |
| integrable distribution | Ch7 | out-of-scope | differential-geometric nonholonomic / Lie-group theory (MLS ch.7, App. A); plan dropped PA 15.10-15.11 and PA 4.6; car controllability in plain words is Note 67 |
| Frobenius' theorem | Ch7 | out-of-scope | differential-geometric nonholonomic / Lie-group theory (MLS ch.7, App. A); plan dropped PA 15.10-15.11 and PA 4.6; car controllability in plain words is Note 67 |
| completely nonholonomic | Ch7 | out-of-scope | differential-geometric nonholonomic / Lie-group theory (MLS ch.7, App. A); plan dropped PA 15.10-15.11 and PA 4.6; car controllability in plain words is Note 67 |
| controllability Lie algebra | Ch7 | out-of-scope | differential-geometric nonholonomic / Lie-group theory (MLS ch.7, App. A); plan dropped PA 15.10-15.11 and PA 4.6; car controllability in plain words is Note 67 |
| Chow's theorem | Ch7 | out-of-scope | differential-geometric nonholonomic / Lie-group theory (MLS ch.7, App. A); plan dropped PA 15.10-15.11 and PA 4.6; car controllability in plain words is Note 67 |
| filtration | Ch7 | out-of-scope | differential-geometric nonholonomic / Lie-group theory (MLS ch.7, App. A); plan dropped PA 15.10-15.11 and PA 4.6; car controllability in plain words is Note 67 |
| degree of nonholonomy | Ch7 | out-of-scope | differential-geometric nonholonomic / Lie-group theory (MLS ch.7, App. A); plan dropped PA 15.10-15.11 and PA 4.6; car controllability in plain words is Note 67 |
| growth vector | Ch7 | out-of-scope | differential-geometric nonholonomic / Lie-group theory (MLS ch.7, App. A); plan dropped PA 15.10-15.11 and PA 4.6; car controllability in plain words is Note 67 |
| relative growth vector | Ch7 | out-of-scope | differential-geometric nonholonomic / Lie-group theory (MLS ch.7, App. A); plan dropped PA 15.10-15.11 and PA 4.6; car controllability in plain words is Note 67 |
| Lie product | Ch7 | out-of-scope | differential-geometric nonholonomic / Lie-group theory (MLS ch.7, App. A); plan dropped PA 15.10-15.11 and PA 4.6; car controllability in plain words is Note 67 |
| nilpotent Lie algebra | Ch7 | out-of-scope | differential-geometric nonholonomic / Lie-group theory (MLS ch.7, App. A); plan dropped PA 15.10-15.11 and PA 4.6; car controllability in plain words is Note 67 |
| Philip Hall basis | Ch7 | out-of-scope | differential-geometric nonholonomic / Lie-group theory (MLS ch.7, App. A); plan dropped PA 15.10-15.11 and PA 4.6; car controllability in plain words is Note 67 |
| optimal steering with sinusoids | Ch8 | out-of-scope | nonholonomic steering by sinusoids / chained form (MLS ch.8); plan dropped PA 15.12; car planning uses Dubins/Reeds-Shepp and Hybrid A* (Notes 112-113) |
| chained form | Ch8 | out-of-scope | nonholonomic steering by sinusoids / chained form (MLS ch.8); plan dropped PA 15.12; car planning uses Dubins/Reeds-Shepp and Hybrid A* (Notes 112-113) |
| integrally related sinusoids | Ch8 | out-of-scope | nonholonomic steering by sinusoids / chained form (MLS ch.8); plan dropped PA 15.12; car planning uses Dubins/Reeds-Shepp and Hybrid A* (Notes 112-113) |
| least squares steering problem | Ch8 | out-of-scope | nonholonomic steering by sinusoids / chained form (MLS ch.8); plan dropped PA 15.12; car planning uses Dubins/Reeds-Shepp and Hybrid A* (Notes 112-113) |
| Ritz approximation algorithm | Ch8 | out-of-scope | nonholonomic steering by sinusoids / chained form (MLS ch.8); plan dropped PA 15.12; car planning uses Dubins/Reeds-Shepp and Hybrid A* (Notes 112-113) |
| piecewise constant inputs | Ch8 | out-of-scope | nonholonomic steering by sinusoids / chained form (MLS ch.8); plan dropped PA 15.12; car planning uses Dubins/Reeds-Shepp and Hybrid A* (Notes 112-113) |
| Gauss-Bonnet theorem (finger repositioning) | Ch8 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |

## Tedrake, *Underactuated Robotics* (MIT 6.832 course notes, 2024 version)

Official free HTML: https://underactuated.csail.mit.edu/ (© Russ Tedrake, 2024). No back index, so every chapter, section and subsection heading of the official table of contents (index.html) is a term. 'Pages' gives the chapter or appendix.

Counts: taught 215, mentioned-only 0, add 54, out-of-scope 173, index-noise 43 (total 485).

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| Preface | Preface | index-noise | front matter (preface) |
| Fully-actuated vs Underactuated Systems | Ch 1 | taught | Note 221 (underactuation: tilt to move) |
| Motivation | Ch 1 | index-noise | motivation heading; sub-entries judged |
| Honda's ASIMO vs. passive dynamic walkers | Ch 1 | taught | Note 299 (passive walkers) |
| Birds vs. modern aircraft | Ch 1 | index-noise | motivation anecdote (birds vs aircraft), no separate concept |
| Manipulation | Ch 1 | index-noise | motivation heading (manipulation as an underactuated problem) |
| The common theme | Ch 1 | index-noise | motivation summary heading |
| Definitions | Ch 1 | taught | Note 221 (underactuation) |
| Feedback Equivalence | Ch 1 | taught | Note 124 (feedback linearisation) |
| Input and State Constraints | Ch 1 | taught | Note 207 (input and state constraints) |
| Nonholonomic constraints | Ch 1 | taught | Note 64 (nonholonomic constraints) |
| Underactuated robotics | Ch 1 | taught | Note 221 (underactuation) |
| Goals for the course | Ch 1 | index-noise | course-logistics heading |
| Exercises | Ch 1 | index-noise | exercises heading |
| The Simple Pendulum | Ch 2 | add | **The simple pendulum as the first nonlinear system: phase portrait, damped vs undamped, equilibria (stable bottom, unstable top), orbits, torque limits** (control) -> MA 06-calculus (worked example in the planned ODEs and Stability Notes) |
| Introduction | Ch 2 | index-noise | chapter introduction heading |
| Nonlinear dynamics with a constant torque | Ch 2 | add | **The simple pendulum as the first nonlinear system: phase portrait, damped vs undamped, equilibria (stable bottom, unstable top), orbits, torque limits** (control) -> MA 06-calculus (worked example in the planned ODEs and Stability Notes) |
| The overdamped pendulum | Ch 2 | add | **The simple pendulum as the first nonlinear system: phase portrait, damped vs undamped, equilibria (stable bottom, unstable top), orbits, torque limits** (control) -> MA 06-calculus (worked example in the planned ODEs and Stability Notes) |
| The undamped pendulum with zero torque | Ch 2 | add | **The simple pendulum as the first nonlinear system: phase portrait, damped vs undamped, equilibria (stable bottom, unstable top), orbits, torque limits** (control) -> MA 06-calculus (worked example in the planned ODEs and Stability Notes) |
| Orbit calculations | Ch 2 | add | **The simple pendulum as the first nonlinear system: phase portrait, damped vs undamped, equilibria (stable bottom, unstable top), orbits, torque limits** (control) -> MA 06-calculus (worked example in the planned ODEs and Stability Notes) |
| The undamped pendulum with a constant torque | Ch 2 | add | **The simple pendulum as the first nonlinear system: phase portrait, damped vs undamped, equilibria (stable bottom, unstable top), orbits, torque limits** (control) -> MA 06-calculus (worked example in the planned ODEs and Stability Notes) |
| The torque-limited simple pendulum | Ch 2 | add | **Canonical underactuated systems: acrobot and cart-pole equations of motion; balancing by LQR; swing-up by energy shaping** (robotics) -> RB-04 (new Note before Note 295) |
| Energy-shaping control | Ch 2 | add | **Canonical underactuated systems: acrobot and cart-pole equations of motion; balancing by LQR; swing-up by energy shaping** (robotics) -> RB-04 (new Note before Note 295) |
| Exercises | Ch 2 | index-noise | exercises heading |
| Acrobots, Cart-Poles, and Quadrotors | Ch 3 | add | **Canonical underactuated systems: acrobot and cart-pole equations of motion; balancing by LQR; swing-up by energy shaping** (robotics) -> RB-04 (new Note before Note 295) |
| The Acrobot | Ch 3 | add | **Canonical underactuated systems: acrobot and cart-pole equations of motion; balancing by LQR; swing-up by energy shaping** (robotics) -> RB-04 (new Note before Note 295) |
| Equations of motion | Ch 3 | add | **Canonical underactuated systems: acrobot and cart-pole equations of motion; balancing by LQR; swing-up by energy shaping** (robotics) -> RB-04 (new Note before Note 295) |
| The Cart-Pole system | Ch 3 | add | **Canonical underactuated systems: acrobot and cart-pole equations of motion; balancing by LQR; swing-up by energy shaping** (robotics) -> RB-04 (new Note before Note 295) |
| Equations of motion | Ch 3 | add | **Canonical underactuated systems: acrobot and cart-pole equations of motion; balancing by LQR; swing-up by energy shaping** (robotics) -> RB-04 (new Note before Note 295) |
| Quadrotors | Ch 3 | taught | Note 221 (the quadrotor model) |
| The Planar Quadrotor | Ch 3 | taught | Note 221 (quadrotor model; planar case) |
| The Full 3D Quadrotor | Ch 3 | taught | Note 221 (3D quadrotor dynamics) |
| Balancing | Ch 3 | taught | Note 222 (linearise at hover, LQR); Note 206 |
| Linearizing the manipulator equations | Ch 3 | taught | Note 206 (linearising a model around an operating point) |
| Controllability of linear systems | Ch 3 | taught | Note 204 (controllability rank test) |
| The special case of non-repeated eigenvalues | Ch 3 | out-of-scope | proof technique or derivation route (a lemma used inside a derivation) |
| A general solution | Ch 3 | taught | Note 204 (controllability rank test) |
| Controllability vs. underactuated | Ch 3 | taught | Note 204 (controllability); Note 221 (underactuation) |
| Stabilizability of a linear system | Ch 3 | add | **Observability rank test, stabilizability and detectability; duality of control and estimation** (control) -> RO-15 (new Note after Note 204, together with observers) |
| LQR feedback | Ch 3 | taught | Note 205 (LQR); Note 222 (LQR at hover) |
| Partial feedback linearization | Ch 3 | out-of-scope | partial feedback linearisation: a technique specific to underactuated-systems research (UA 3.5); full feedback linearisation is Note 124 |
| PFL for the Cart-Pole System | Ch 3 | out-of-scope | partial feedback linearisation: a technique specific to underactuated-systems research (UA 3.5); full feedback linearisation is Note 124 |
| Collocated | Ch 3 | out-of-scope | partial feedback linearisation: a technique specific to underactuated-systems research (UA 3.5); full feedback linearisation is Note 124 |
| Non-collocated | Ch 3 | out-of-scope | partial feedback linearisation: a technique specific to underactuated-systems research (UA 3.5); full feedback linearisation is Note 124 |
| General form | Ch 3 | out-of-scope | partial feedback linearisation: a technique specific to underactuated-systems research (UA 3.5); full feedback linearisation is Note 124 |
| Collocated linearization | Ch 3 | out-of-scope | partial feedback linearisation: a technique specific to underactuated-systems research (UA 3.5); full feedback linearisation is Note 124 |
| Non-collocated linearization | Ch 3 | out-of-scope | partial feedback linearisation: a technique specific to underactuated-systems research (UA 3.5); full feedback linearisation is Note 124 |
| Task-space partial feedback linearization | Ch 3 | out-of-scope | partial feedback linearisation: a technique specific to underactuated-systems research (UA 3.5); full feedback linearisation is Note 124 |
| Swing-up control | Ch 3 | add | **Canonical underactuated systems: acrobot and cart-pole equations of motion; balancing by LQR; swing-up by energy shaping** (robotics) -> RB-04 (new Note before Note 295) |
| Energy shaping | Ch 3 | add | **Canonical underactuated systems: acrobot and cart-pole equations of motion; balancing by LQR; swing-up by energy shaping** (robotics) -> RB-04 (new Note before Note 295) |
| Cart-Pole | Ch 3 | add | **Canonical underactuated systems: acrobot and cart-pole equations of motion; balancing by LQR; swing-up by energy shaping** (robotics) -> RB-04 (new Note before Note 295) |
| Acrobot | Ch 3 | add | **Canonical underactuated systems: acrobot and cart-pole equations of motion; balancing by LQR; swing-up by energy shaping** (robotics) -> RB-04 (new Note before Note 295) |
| Discussion | Ch 3 | index-noise | discussion heading |
| Other model systems | Ch 3 | index-noise | pointer section to other model systems |
| Exercises | Ch 3 | index-noise | exercises heading |
| Simple Models of Walking and Running | Ch 4 | taught | Note 299 (hopping and running: SLIP, passive walkers) |
| Limit Cycles | Ch 4 | taught | Note 299 (limit cycles) |
| Poincaré Maps | Ch 4 | taught | Note 299 (Poincaré maps) |
| Simple Models of Walking | Ch 4 | taught | Note 299 (passive walkers) |
| The Rimless Wheel | Ch 4 | taught | Note 299 (rimless wheel as a passive walker) |
| Stance Dynamics | Ch 4 | taught | Note 299 (passive walker dynamics) |
| Foot Collision | Ch 4 | taught | Note 289 (impacts at touch-down) |
| Forward simulation | Ch 4 | taught | plan §4 new MA: Numerical integration of ODEs; Note 289 (hybrid simulation) |
| Poincaré Map | Ch 4 | taught | Note 299 (Poincaré maps) |
| Fixed Points and Stability | Ch 4 | taught | Note 299 (fixed point of the Poincaré map = stable limit cycle) |
| Stability of standing still | Ch 4 | taught | Note 299 (passive walker stability) |
| The Compass Gait | Ch 4 | taught | Note 299 (compass gait as a passive walker) |
| The Kneed Walker | Ch 4 | out-of-scope | model or formulation variant shown as an extension in the book; the base idea is taught in the cited Note |
| Curved feet | Ch 4 | out-of-scope | model or formulation variant shown as an extension in the book; the base idea is taught in the cited Note |
| And beyond... | Ch 4 | index-noise | pointer heading ("and beyond") |
| Simple Models of Running | Ch 4 | taught | Note 299 (running models: SLIP) |
| The Spring-Loaded Inverted Pendulum (SLIP) | Ch 4 | taught | Note 299 (SLIP) |
| Analysis on the apex-to-apex map | Ch 4 | taught | Note 299 (Poincaré map: apex-to-apex) |
| SLIP Control | Ch 4 | taught | Note 299 (Raibert controller: foot placement for speed) |
| SLIP extensions | Ch 4 | out-of-scope | model or formulation variant shown as an extension in the book; the base idea is taught in the cited Note |
| Hopping robots from the MIT Leg Laboratory | Ch 4 | taught | Note 299 (Raibert hopping controller) |
| The 2D Hopper | Ch 4 | taught | Note 299 (Raibert hopper) |
| Running on four legs as though they were one | Ch 4 | taught | Note 299 (Raibert controller applied to quadrupeds) |
| Towards human-like running | Ch 4 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| A simple model that can walk and run | Ch 4 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Juggling | Ch 4 | out-of-scope | worked example system used only for illustration in the book (no new concept) |
| Exercises | Ch 4 | index-noise | exercises heading |
| Highly-articulated Legged Robots | Ch 5 | taught | Note 295 (floating base); Note 303-304 (whole-body control) |
| A thought experiment | Ch 5 | taught | Note 295 (floating base: unpowered degrees of freedom) |
| A spacecraft model | Ch 5 | taught | Note 295 (floating base without contact) |
| Robots with (massless) legs | Ch 5 | taught | Note 295 (floating base moved only through contact forces) |
| Center of pressure (CoP) and Zero-moment point (ZMP) | Ch 5 | taught | Note 296 (centre of pressure and ZMP) |
| The special case of flat terrain | Ch 5 | taught | Note 296 (ZMP on flat ground) |
| An aside: Zero-moment point derivation | Ch 5 | taught | Note 296 (ZMP) |
| A note about impact dynamics | Ch 5 | taught | Note 289 (impacts) |
| ZMP-based planning | Ch 5 | taught | Note 297 (ZMP walking) |
| Heuristic footstep planning | Ch 5 | taught | Note 297 (footsteps, then ZMP path) |
| Planning trajectories for the center of mass | Ch 5 | taught | Note 297 (CoM path by preview control) |
| The ZMP "Stability" Metric | Ch 5 | taught | Note 295 (static vs dynamic balance); Note 296 |
| From a CoM plan to a whole-body plan | Ch 5 | taught | Note 304 (WBC tracks a plan from a simpler model) |
| Centroidal dynamics | Ch 5 | taught | Note 301 (centroidal dynamics) |
| Spatial momentum | Ch 5 | taught | Note 301 (centroidal momentum) |
| Generalization to multibody | Ch 5 | taught | Note 301 (centroidal momentum matrix) |
| Whole-Body Control | Ch 5 | taught | Note 303 (whole-body control); Note 304 |
| Footstep planning and push recovery | Ch 5 | taught | Note 298 (capture point and push recovery) |
| Beyond ZMP planning | Ch 5 | taught | Note 302 (MPC with simplified and whole-body models) |
| Exercises | Ch 5 | index-noise | exercises heading |
| Model Systems with Stochasticity | Ch 6 | out-of-scope | chapter on stochastic model systems (UA ch.6); its parts are judged separately |
| The Master Equation | Ch 6 | out-of-scope | continuous-time Markov-chain (master) equation (UA 6.1); discrete Markov chains are planned in §4 |
| Stationary Distributions | Ch 6 | taught | plan §4 new MA: Markov chains (stationary distribution) |
| Finite Markov Decision Processes | Ch 6 | taught | Note 7 (Markov decision processes) |
| Dynamics of a Markov chain | Ch 6 | taught | plan §4 new MA: Markov chains (transition matrix) |
| Extended Example: The Rimless Wheel on Rough Terrain | Ch 6 | out-of-scope | worked example system used only for illustration in the book (no new concept) |
| Randomized smoothing of contact dynamics | Ch 6 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Noise models for real robots/systems. | Ch 6 | taught | Note 137 (sensor noise and latency modelling); Note 83 (IMU noise) |
| Dynamic Programming | Ch 7 | taught | Note 10 (Bellman equations); Note 14 (value iteration); Note 205 |
| Formulating control design as an optimization | Ch 7 | taught | Note 205 (LQ problem: control as cost minimisation) |
| Additive cost | Ch 7 | add | **Optimal-control problem anatomy: stage (running) cost, additive cost over the horizon, terminal cost, cost-to-go / time to go** (control) -> RO-15 (extend Note 205) |
| Optimal control as graph search | Ch 7 | taught | Note 14 (value iteration = cost-to-go); Note 104 |
| Continuous dynamic programming | Ch 7 | taught | Note 205 (HJB equation) |
| The Hamilton-Jacobi-Bellman Equation | Ch 7 | taught | Note 205 (Hamilton-Jacobi-Bellman equation) |
| Solving for the minimizing control | Ch 7 | taught | Note 205 (HJB equation) |
| Numerical solutions for $J^*$ | Ch 7 | taught | Note 106 (DP with interpolation on continuous spaces) |
| Value iteration with function approximation | Ch 7 | taught | Note 25 (value approximation); Note 26 |
| Linear function approximators | Ch 7 | taught | Note 26 (linear value functions) |
| Value iteration on a mesh | Ch 7 | taught | Note 106 (DP with interpolation) |
| Neural fitted value iteration | Ch 7 | taught | Note 35 (neural network fitted to TD/Bellman targets); Note 25 |
| Continuous-time systems | Ch 7 | taught | Note 205 (HJB, continuous time) |
| Extensions | Ch 7 | index-noise | grouping heading |
| Discounted and average cost formulations | Ch 7 | taught | Note 8 (discounted and average cost) |
| Stochastic control for finite MDPs | Ch 7 | taught | Note 14 (value iteration with nature); Note 7 |
| Stochastic interpretation of deterministic, continuous-state value iteration | Ch 7 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Linear Programming Dynamic Programming | Ch 7 | out-of-scope | linear-programming formulation of dynamic programming (UA 7.4): theory and research depth |
| Sums-of-Squares Dynamic Programming | Ch 7 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Exercises | Ch 7 | index-noise | exercises heading |
| Linear Quadratic Regulators | Ch 8 | taught | Note 205 (LQR) |
| Basic Derivation | Ch 8 | taught | Note 205 (LQR and the Riccati equation) |
| Local stabilization of nonlinear systems | Ch 8 | taught | Note 206 (linearising around an operating point); Note 222 |
| Finite-horizon formulations | Ch 8 | taught | Note 205 (discrete-time finite-horizon LQ problem) |
| Finite-horizon LQR | Ch 8 | taught | Note 205 (finite-horizon LQ by Riccati recursion) |
| Time-varying LQR | Ch 8 | taught | Note 206 (time-varying LQR) |
| Local trajectory stabilization for nonlinear systems | Ch 8 | taught | Note 206 (time-varying LQR on a planned trajectory) |
| Linear Quadratic Optimal Tracking | Ch 8 | taught | Note 206 (LQR for tracking) |
| Linear Final Boundary Value Problems | Ch 8 | out-of-scope | model or formulation variant shown as an extension in the book; the base idea is taught in the cited Note |
| Variations and extensions | Ch 8 | index-noise | grouping heading |
| Discrete-time Riccati Equations | Ch 8 | taught | Note 205 (discrete-time Riccati recursion) |
| LQR with input and state constraints | Ch 8 | taught | Note 207 (constrained LQ = linear MPC) |
| LQR on a manifold | Ch 8 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| LQR for linear systems in implicit form | Ch 8 | out-of-scope | model or formulation variant shown as an extension in the book; the base idea is taught in the cited Note |
| LQR as a convex optimization | Ch 8 | out-of-scope | semidefinite programming / LMI formulations (UA App. C): graduate convex-optimisation topic |
| Finite-horizon LQR via least squares | Ch 8 | taught | Note 207 (stack the predictions: condensed QP) |
| Minimum-time LQR | Ch 8 | out-of-scope | model or formulation variant shown as an extension in the book; the base idea is taught in the cited Note |
| Parameterized Riccati Equations | Ch 8 | out-of-scope | model or formulation variant shown as an extension in the book; the base idea is taught in the cited Note |
| Exercises | Ch 8 | index-noise | exercises heading |
| Notes | Ch 8 | index-noise | notes heading |
| Finite-horizon LQR derivation (general form) | Ch 8 | taught | Note 205 (LQR derivation) |
| Lyapunov Analysis | Ch 9 | taught | Note 199 (Lyapunov certificates) |
| Lyapunov Functions | Ch 9 | taught | Note 199 (Lyapunov functions) |
| Global Stability | Ch 9 | add | **Stability definitions: equilibrium, Lyapunov stable, asymptotically and exponentially stable, local vs global, region of attraction; stability from the linearisation (Lyapunov's indirect method)** (maths) -> MA 06-calculus (extend the planned 'Stability of dynamical systems' Note) |
| LaSalle's Invariance Principle | Ch 9 | add | **LaSalle's invariance principle** (maths) -> MA 06-calculus (short section in the planned Stability Note) |
| Relationship to the Hamilton-Jacobi-Bellman equations | Ch 9 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Lyapunov functions for estimating regions of attraction | Ch 9 | add | **Stability definitions: equilibrium, Lyapunov stable, asymptotically and exponentially stable, local vs global, region of attraction; stability from the linearisation (Lyapunov's indirect method)** (maths) -> MA 06-calculus (extend the planned 'Stability of dynamical systems' Note) |
| Robustness analysis using "common Lyapunov functions" | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Barrier functions | Ch 9 | taught | Note 199 (control barrier functions) |
| Lyapunov analysis with convex optimization | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Linear systems | Ch 9 | add | **Quadratic Lyapunov functions V = x'Px and the Lyapunov equation for linear systems** (maths) -> MA 06-calculus (extend the planned Stability Note) |
| Global analysis for polynomial systems | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Region of attraction estimation for polynomial systems | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| The S-procedure | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Basic region of attraction formulation | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| The equality-constrained formulation | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Searching for $V(\bx)$ | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Convex outer approximations | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Regions of attraction codes in Drake | Ch 9 | out-of-scope | software or tool name, not a concept |
| Robustness analysis using the S-procedure | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Piecewise-polynomial systems | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Rigid-body dynamics are (rational) polynomial | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Linear feedback and quadratic forms | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Alternatives for obtaining polynomial equations | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Verifying dynamics in implicit form | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Finite-time Reachability | Ch 9 | out-of-scope | funnels, finite-time reachability and feedback motion planning (UA ch.9, ch.14); plan dropped funnel composition (PA 8.6) as advanced theory |
| Time-varying dynamics and Lyapunov functions | Ch 9 | out-of-scope | funnels, finite-time reachability and feedback motion planning (UA ch.9, ch.14); plan dropped funnel composition (PA 8.6) as advanced theory |
| Finite-time reachability | Ch 9 | out-of-scope | funnels, finite-time reachability and feedback motion planning (UA ch.9, ch.14); plan dropped funnel composition (PA 8.6) as advanced theory |
| Reachability via Lyapunov functions | Ch 9 | out-of-scope | funnels, finite-time reachability and feedback motion planning (UA ch.9, ch.14); plan dropped funnel composition (PA 8.6) as advanced theory |
| Control design | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Control design via alternations | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Global stability | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Maximizing the region of attraction | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| State feedback for linear systems | Ch 9 | taught | Note 204 (state feedback for linear systems) |
| Control-Lyapunov Functions | Ch 9 | add | **Control Lyapunov functions (CLF) and the CLF-CBF quadratic program** (control) -> RO-14 (extend Note 199) |
| Approximate dynamic programming with SOS | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Upper and lower bounds on cost-to-go | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Linear Programming Dynamic Programming | Ch 9 | out-of-scope | linear-programming formulation of dynamic programming (UA 7.4): theory and research depth |
| Sums-of-Squares Dynamic Programming | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Alternative computational approaches | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Sampling Quotient-Ring Sum-of-Squares | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| "Satisfiability modulo theories" (SMT) | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Mixed-integer programming (MIP) formulations | Ch 9 | add | **Mixed-integer programming (MILP/MIQP): optimisation with on/off decisions, e.g. footstep and contact-sequence planning** (maths) -> MA 07-optimisation (new short section after MA-068); used by Note 306 |
| Continuation methods | Ch 9 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Neural Lyapunov functions | Ch 9 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Contraction metrics | Ch 9 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Other variations and extensions | Ch 9 | index-noise | pointer heading |
| Exercises | Ch 9 | index-noise | exercises heading |
| Trajectory Optimization | Ch 10 | taught | Note 116 (trajectory optimisation) |
| Problem Formulation | Ch 10 | taught | Note 116 (trajectory optimisation) |
| Convex Formulations for Linear Systems | Ch 10 | taught | Note 207 (linear MPC as a QP); Note 116 |
| Direct Transcription | Ch 10 | taught | Note 116 (direct methods: transcription) |
| Direct Shooting | Ch 10 | taught | Note 116 (shooting) |
| Computational Considerations | Ch 10 | taught | Note 207 (condensed vs sparse) |
| Continuous Time | Ch 10 | taught | Note 116 (direct methods) |
| Nonconvex Trajectory Optimization | Ch 10 | taught | Note 116 (gradient-based trajectory optimisation) |
| Direct Transcription and Direct Shooting | Ch 10 | taught | Note 116 (single and multiple shooting) |
| Direct Collocation | Ch 10 | taught | Note 116 (collocation) |
| Pseudo-spectral Methods | Ch 10 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Dynamic constraints in implicit form | Ch 10 | out-of-scope | specialist numerical-methods detail (RMD ch.8, App. A); the plan teaches solvers at overview level (Notes 116, 208) |
| Solution techniques | Ch 10 | taught | Note 208 (SQP, interior point overview) |
| Efficiently computing gradients | Ch 10 | taught | MA-063 (automatic differentiation) |
| The special case of direct shooting without state constraints | Ch 10 | taught | Note 116 (gradient-based shooting) |
| Penalty methods and the Augmented Lagrangian | Ch 10 | taught | Note 194 (penalty methods) |
| Zero-order optimization | Ch 10 | taught | Note 43 (black-box search: CEM, evolution strategies) |
| Getting good solutions... in practice. | Ch 10 | index-noise | practical-tips heading |
| Local Trajectory Feedback Design | Ch 10 | taught | Note 206 (time-varying LQR around a trajectory) |
| Finite-horizon LQR | Ch 10 | taught | Note 205 (finite-horizon LQR) |
| Model-Predictive Control | Ch 10 | taught | Note 207 (model predictive control) |
| Receding-horizon MPC | Ch 10 | taught | Note 207 (receding horizon) |
| Recursive feasibility | Ch 10 | add | **Invariant sets (positively invariant, control invariant) and recursive feasibility of MPC** (control) -> RO-15 (extend Note 207) |
| MPC and Lyapunov functions | Ch 10 | out-of-scope | stability or optimality proof machinery (RMD ch.2-3 theorems; UA proofs), research depth |
| Case Study: A glider that can land on a perch like a bird | Ch 10 | out-of-scope | worked example system used only for illustration in the book (no new concept) |
| The Flat-Plate Glider Model | Ch 10 | out-of-scope | worked example system used only for illustration in the book (no new concept) |
| Trajectory optimization | Ch 10 | taught | Note 116 (trajectory optimisation) |
| Trajectory stabilization | Ch 10 | taught | Note 206 (time-varying LQR to hold a trajectory) |
| Trajectory funnels | Ch 10 | out-of-scope | funnels, finite-time reachability and feedback motion planning (UA ch.9, ch.14); plan dropped funnel composition (PA 8.6) as advanced theory |
| Beyond a single trajectory | Ch 10 | index-noise | pointer heading |
| Pontryagin's Minimum Principle | Ch 10 | taught | Note 116 (Pontryagin's principle, named only) |
| Lagrange multiplier derivation of the adjoint equations | Ch 10 | out-of-scope | Pontryagin costate (adjoint) machinery; plan names Pontryagin only (Note 116), PA 15.8 dropped |
| Necessary conditions for optimality in continuous time | Ch 10 | out-of-scope | Pontryagin costate (adjoint) machinery; plan names Pontryagin only (Note 116), PA 15.8 dropped |
| Variations and Extensions | Ch 10 | index-noise | grouping heading |
| Differential Flatness | Ch 10 | taught | Note 223 (differential flatness) |
| Iterative LQR and Differential Dynamic Programming | Ch 10 | taught | Note 116 (DDP/iLQR) |
| Leveraging combinatorial optimization | Ch 10 | add | **Mixed-integer programming (MILP/MIQP): optimisation with on/off decisions, e.g. footstep and contact-sequence planning** (maths) -> MA 07-optimisation (new short section after MA-068); used by Note 306 |
| Explicit model-predictive control | Ch 10 | add | **Explicit MPC: the MPC law precomputed offline as a piecewise-affine lookup table** (control) -> RO-15 (extend Note 207) |
| Exercises | Ch 10 | index-noise | exercises heading |
| Policy Search | Ch 11 | taught | Note 29 (parameterised policies); Note 43 (policy search) |
| Problem formulation | Ch 11 | taught | Note 29 (performance measure J(theta)) |
| Linear Quadratic Regulator | Ch 11 | out-of-scope | convergence theory of policy gradient on LQR (UA 11.2-11.3, Fazel et al.): research results |
| Policy Evaluation | Ch 11 | out-of-scope | convergence theory of policy gradient on LQR (UA 11.2-11.3, Fazel et al.): research results |
| A nonconvex objective in ${\bf K}$ | Ch 11 | out-of-scope | convergence theory of policy gradient on LQR (UA 11.2-11.3, Fazel et al.): research results |
| No local minima | Ch 11 | out-of-scope | convergence theory of policy gradient on LQR (UA 11.2-11.3, Fazel et al.): research results |
| True gradient descent | Ch 11 | out-of-scope | convergence theory of policy gradient on LQR (UA 11.2-11.3, Fazel et al.): research results |
| More convergence results and counter-examples | Ch 11 | out-of-scope | convergence theory of policy gradient on LQR (UA 11.2-11.3, Fazel et al.): research results |
| Trajectory-based policy search | Ch 11 | taught | Note 43 (black-box policy search over rollouts) |
| Infinite-horizon objectives | Ch 11 | taught | Note 8 (infinite horizon) |
| Search strategies for global optimization | Ch 11 | taught | Note 43 (CMA-ES, cross-entropy method) |
| Policy Iteration | Ch 11 | taught | Note 13 (policy iteration) |
| Sampling-based motion planning | Ch 12 | taught | Note 110 (RRT); Note 111 (PRM) |
| Large-scale Incremental Search | Ch 12 | taught | Note 105 (A*); Note 104 |
| Probabilistic RoadMaps (PRMs) | Ch 12 | taught | Note 111 (probabilistic roadmaps) |
| Getting smooth trajectories | Ch 12 | taught | Note 113 (path smoothing) |
| Rapidly-exploring Random Trees (RRTs) | Ch 12 | taught | Note 110 (RRT) |
| RRTs for robots with dynamics | Ch 12 | taught | Note 112 (kinodynamic RRT) |
| Variations and extensions | Ch 12 | taught | Note 110 (RRT*, PRM*, FMT*, SST* named) |
| Decomposition methods | Ch 12 | taught | Note 270 (cell decomposition) |
| Exercises | Ch 12 | index-noise | exercises heading |
| Robust and Stochastic Control | Ch 13 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Stochastic models | Ch 13 | taught | Note 80 (linear Gaussian system); Note 68 (motion as a distribution) |
| Costs and constraints for stochastic systems | Ch 13 | taught | Note 195 (probabilistic and average constraints) |
| Finite Markov Decision Processes | Ch 13 | taught | Note 7 (Markov decision processes) |
| Linear optimal control | Ch 13 | taught | Note 205 (LQR) |
| Stochastic LQR | Ch 13 | add | **State observer (Luenberger), output feedback and the separation principle; LQG; output-feedback MPC (estimator + controller)** (control) -> RO-15 (new Note after Note 204) |
| Non-i.i.d. disturbances | Ch 13 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Stochastic linear MPC | Ch 13 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Worst-case control w/ bounded uncertainty | Ch 13 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Common Lyapunov functions | Ch 13 | out-of-scope | robust-control theory (H-infinity, L2 gain, small-gain, polytopic uncertainty; UA 13.4): graduate depth; robustness is handled by domain randomization (Note 137) |
| Polytope dynamics | Ch 13 | out-of-scope | robust-control theory (H-infinity, L2 gain, small-gain, polytopic uncertainty; UA 13.4): graduate depth; robustness is handled by domain randomization (Note 137) |
| Robust MPC | Ch 13 | add | **Robust and stochastic MPC: bounded disturbances, min-max idea, tube MPC with constraint tightening; stochastic MPC with chance constraints** (control) -> RO-15 (extend Note 208) |
| Polytopic containment | Ch 13 | out-of-scope | robust-control theory (H-infinity, L2 gain, small-gain, polytopic uncertainty; UA 13.4): graduate depth; robustness is handled by domain randomization (Note 137) |
| Robust constrained LQR | Ch 13 | out-of-scope | robust-control theory (H-infinity, L2 gain, small-gain, polytopic uncertainty; UA 13.4): graduate depth; robustness is handled by domain randomization (Note 137) |
| Disturbance-based feedback parameterizations | Ch 13 | out-of-scope | robust-control theory (H-infinity, L2 gain, small-gain, polytopic uncertainty; UA 13.4): graduate depth; robustness is handled by domain randomization (Note 137) |
| $L_2$ gain | Ch 13 | out-of-scope | robust-control theory (H-infinity, L2 gain, small-gain, polytopic uncertainty; UA 13.4): graduate depth; robustness is handled by domain randomization (Note 137) |
| Dissipation inequalities | Ch 13 | out-of-scope | robust-control theory (H-infinity, L2 gain, small-gain, polytopic uncertainty; UA 13.4): graduate depth; robustness is handled by domain randomization (Note 137) |
| Small-gain theorem | Ch 13 | out-of-scope | robust-control theory (H-infinity, L2 gain, small-gain, polytopic uncertainty; UA 13.4): graduate depth; robustness is handled by domain randomization (Note 137) |
| Model uncertainty as a special case. | Ch 13 | out-of-scope | robust-control theory (H-infinity, L2 gain, small-gain, polytopic uncertainty; UA 13.4): graduate depth; robustness is handled by domain randomization (Note 137) |
| Robust LQR as $\mathcal{H}_\infty$ | Ch 13 | out-of-scope | robust-control theory (H-infinity, L2 gain, small-gain, polytopic uncertainty; UA 13.4): graduate depth; robustness is handled by domain randomization (Note 137) |
| Linear Exponential-Quadratic Gaussian (LEQG) | Ch 13 | out-of-scope | robust-control theory (H-infinity, L2 gain, small-gain, polytopic uncertainty; UA 13.4): graduate depth; robustness is handled by domain randomization (Note 137) |
| Adaptive control | Ch 13 | out-of-scope | adaptive control: plan dropped it (ME-069) as beyond beginner depth; model error handled by system identification and domain randomization |
| Structured uncertainty | Ch 13 | out-of-scope | robust-control theory (H-infinity, L2 gain, small-gain, polytopic uncertainty; UA 13.4): graduate depth; robustness is handled by domain randomization (Note 137) |
| Linear parameter-varying (LPV) control | Ch 13 | taught | Note 255 (linear parameter-varying control, named) |
| Trajectory optimization | Ch 13 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Monte-carlo trajectory optimization | Ch 13 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Iterative $\mathcal{H}_2$/iLQG | Ch 13 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Nonlinear analysis and control | Ch 13 | out-of-scope | robust-control theory (H-infinity, L2 gain, small-gain, polytopic uncertainty; UA 13.4): graduate depth; robustness is handled by domain randomization (Note 137) |
| Domain randomization | Ch 13 | taught | Note 137 (domain randomization) |
| Extensions | Ch 13 | index-noise | grouping heading |
| Alternative risk/robustness metrics | Ch 13 | taught | Note 198 (risk-sensitive RL: variance, CVaR) |
| Feedback Motion Planning | Ch 14 | out-of-scope | funnels, finite-time reachability and feedback motion planning (UA ch.9, ch.14); plan dropped funnel composition (PA 8.6) as advanced theory |
| Parameterized feedback policies as "skills" | Ch 14 | out-of-scope | funnels, finite-time reachability and feedback motion planning (UA ch.9, ch.14); plan dropped funnel composition (PA 8.6) as advanced theory |
| The rules of composition | Ch 14 | out-of-scope | funnels, finite-time reachability and feedback motion planning (UA ch.9, ch.14); plan dropped funnel composition (PA 8.6) as advanced theory |
| Parameterized controllers and Lyapunov functions | Ch 14 | out-of-scope | funnels, finite-time reachability and feedback motion planning (UA ch.9, ch.14); plan dropped funnel composition (PA 8.6) as advanced theory |
| Probabilistic feedback coverage | Ch 14 | out-of-scope | funnels, finite-time reachability and feedback motion planning (UA ch.9, ch.14); plan dropped funnel composition (PA 8.6) as advanced theory |
| Online planning | Ch 14 | out-of-scope | funnels, finite-time reachability and feedback motion planning (UA ch.9, ch.14); plan dropped funnel composition (PA 8.6) as advanced theory |
| Output Feedback (aka Pixels-to-Torques) | Ch 15 | add | **State observer (Luenberger), output feedback and the separation principle; LQG; output-feedback MPC (estimator + controller)** (control) -> RO-15 (new Note after Note 204) |
| Background | Ch 15 | add | **State observer (Luenberger), output feedback and the separation principle; LQG; output-feedback MPC (estimator + controller)** (control) -> RO-15 (new Note after Note 204) |
| The classical perspective | Ch 15 | add | **State observer (Luenberger), output feedback and the separation principle; LQG; output-feedback MPC (estimator + controller)** (control) -> RO-15 (new Note after Note 204) |
| From pixels to torques | Ch 15 | taught | Note 323 (end-to-end visuomotor policies) |
| Static Output Feedback | Ch 15 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| A hardness result | Ch 15 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Perhaps a history of observations? | Ch 15 | taught | Note 162 (history encoders) |
| Partially-observable Markov Decision Processes (POMDPs) | Ch 15 | taught | Note 153 (POMDPs) |
| Linear systems w/ Gaussian noise | Ch 15 | taught | Note 80 (linear Gaussian system) |
| Linear Quadratic Regulator w/ Gaussian Noise (LQG) | Ch 15 | add | **State observer (Luenberger), output feedback and the separation principle; LQG; output-feedback MPC (estimator + controller)** (control) -> RO-15 (new Note after Note 204) |
| Trajectory optimization with Iterative LQG | Ch 15 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Observer-based Feedback | Ch 15 | add | **State observer (Luenberger), output feedback and the separation principle; LQG; output-feedback MPC (estimator + controller)** (control) -> RO-15 (new Note after Note 204) |
| Luenberger Observer | Ch 15 | add | **State observer (Luenberger), output feedback and the separation principle; LQG; output-feedback MPC (estimator + controller)** (control) -> RO-15 (new Note after Note 204) |
| Disturbance-based feedback | Ch 15 | out-of-scope | robust-control theory (H-infinity, L2 gain, small-gain, polytopic uncertainty; UA 13.4): graduate depth; robustness is handled by domain randomization (Note 137) |
| Optimizing dynamic policies | Ch 15 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Convex reparameterizations of $H_2$, $H_\infty$, and LQG | Ch 15 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Policy gradient for LQG | Ch 15 | out-of-scope | convergence theory of policy gradient on LQR (UA 11.2-11.3, Fazel et al.): research results |
| Sums-of-squares alternations | Ch 15 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Teacher-student learning | Ch 15 | taught | Note 166 (teacher-student distillation) |
| Feedback from pixels | Ch 15 | taught | Note 323 (camera pixels to torques) |
| Algorithms for Limit Cycles | Ch 16 | out-of-scope | limit-cycle stabilisation algorithms (transverse coordinates, orbital stabilisation; UA ch.16): research depth; limit cycles themselves are Note 299 |
| Trajectory optimization | Ch 16 | out-of-scope | limit-cycle stabilisation algorithms (transverse coordinates, orbital stabilisation; UA ch.16): research depth; limit cycles themselves are Note 299 |
| Lyapunov analysis | Ch 16 | out-of-scope | limit-cycle stabilisation algorithms (transverse coordinates, orbital stabilisation; UA ch.16): research depth; limit cycles themselves are Note 299 |
| Transverse coordinates | Ch 16 | out-of-scope | limit-cycle stabilisation algorithms (transverse coordinates, orbital stabilisation; UA ch.16): research depth; limit cycles themselves are Note 299 |
| Transverse linearization | Ch 16 | out-of-scope | limit-cycle stabilisation algorithms (transverse coordinates, orbital stabilisation; UA ch.16): research depth; limit cycles themselves are Note 299 |
| Region of attraction estimation using sums-of-squares | Ch 16 | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Feedback design | Ch 16 | out-of-scope | limit-cycle stabilisation algorithms (transverse coordinates, orbital stabilisation; UA ch.16): research depth; limit cycles themselves are Note 299 |
| For underactuation degree one. | Ch 16 | out-of-scope | limit-cycle stabilisation algorithms (transverse coordinates, orbital stabilisation; UA ch.16): research depth; limit cycles themselves are Note 299 |
| Transverse LQR | Ch 16 | out-of-scope | limit-cycle stabilisation algorithms (transverse coordinates, orbital stabilisation; UA ch.16): research depth; limit cycles themselves are Note 299 |
| Orbital stabilization for non-periodic trajectories | Ch 16 | out-of-scope | limit-cycle stabilisation algorithms (transverse coordinates, orbital stabilisation; UA ch.16): research depth; limit cycles themselves are Note 299 |
| Planning and Control through Contact | Ch 17 | taught | Note 289 (contact as a hybrid system); Note 302 |
| (Autonomous) Hybrid Systems | Ch 17 | taught | Note 289 (contact as a hybrid system) |
| Hybrid trajectory optimization | Ch 17 | taught | Note 289 (contact scheduling: fixed gait sequence vs contact-implicit planning) |
| Given a fixed mode sequence | Ch 17 | taught | Note 289 (fixed gait sequence) |
| Direct shooting | Ch 17 | taught | Note 116 (shooting); Note 289 |
| Deriving hybrid models: minimal vs floating-base coordinates | Ch 17 | taught | Note 295 (floating base) |
| Discrete control (between events) | Ch 17 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Hybrid LQR | Ch 17 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Hybrid Lyapunov analysis | Ch 17 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Contact-implicit trajectory optimization | Ch 17 | taught | Note 289 (contact-implicit planning) |
| Leveraging combinatorial optimization | Ch 17 | add | **Mixed-integer programming (MILP/MIQP): optimisation with on/off decisions, e.g. footstep and contact-sequence planning** (maths) -> MA 07-optimisation (new short section after MA-068); used by Note 306 |
| Exercises | Ch 17 | index-noise | exercises heading |
| System Identification | Ch 18 | taught | Note 139 (system identification) |
| Problem formulation | Ch 18 | taught | Note 139 (system identification) |
| Equation error vs simulation error | Ch 18 | add | **Equation error vs simulation error: one-step vs multi-step fitting of dynamics models** (robotics) -> RO-08 (extend Note 139) |
| Online optimization | Ch 18 | taught | plan §4 new MA: Recursive least squares |
| Learning models for control | Ch 18 | taught | Note 49 (learn the dynamics, plan with it) |
| Parameter Identification for Mechanical Systems | Ch 18 | taught | Note 139 (system identification) |
| Kinematic parameters and calibration | Ch 18 | taught | Note 139 (odometry and actuator calibration) |
| Estimating inertial parameters (and friction) | Ch 18 | add | **Inertial-parameter identification: dynamics linear in the parameters (regressor form), least squares, exciting trajectories, friction** (robotics) -> RB-02 (extend Note 282) or RO-08 (Note 139) |
| Simultaneous kinematic and inertial identification via lumped parameters. | Ch 18 | add | **Inertial-parameter identification: dynamics linear in the parameters (regressor form), least squares, exciting trajectories, friction** (robotics) -> RB-02 (extend Note 282) or RO-08 (Note 139) |
| Identification using energy instead of inverse dynamics. | Ch 18 | out-of-scope | model or formulation variant shown as an extension in the book; the base idea is taught in the cited Note |
| Residual physics models with linear function approximators | Ch 18 | taught | Note 139 (delta / residual model learned from real data) |
| Experiment design as a trajectory optimization | Ch 18 | add | **Inertial-parameter identification: dynamics linear in the parameters (regressor form), least squares, exciting trajectories, friction** (robotics) -> RB-02 (extend Note 282) or RO-08 (Note 139) |
| Online estimation and adaptive control | Ch 18 | out-of-scope | adaptive control: plan dropped it (ME-069) as beyond beginner depth; model error handled by system identification and domain randomization |
| Identification with contact | Ch 18 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Identifying (time-domain) linear dynamical systems | Ch 18 | add | **Fitting linear dynamical models from data: least-squares fit of A and B, ARX / autoregressive input-output models** (control) -> RO-08 (extend Note 139) |
| From state observations | Ch 18 | add | **Fitting linear dynamical models from data: least-squares fit of A and B, ARX / autoregressive input-output models** (control) -> RO-08 (extend Note 139) |
| Model-based Iterative Learning Control (ILC) | Ch 18 | out-of-scope | iterative learning control: specialised repetitive-task control (UA 18.3), no plan Note uses it |
| Compression using the dominant eigenmodes | Ch 18 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Linear dynamics in a nonlinear basis | Ch 18 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| From input-output data (the state-realization problem) | Ch 18 | out-of-scope | state-realization (subspace) identification from input-output data (UA 18.4): graduate system-identification theory |
| Adding stability constraints | Ch 18 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Autoregressive models | Ch 18 | add | **Fitting linear dynamical models from data: least-squares fit of A and B, ARX / autoregressive input-output models** (control) -> RO-08 (extend Note 139) |
| Statistical analysis of learning linear models | Ch 18 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Identification of finite (PO)MDPs | Ch 18 | taught | Note 45 (learned models); Note 139 |
| From state observations | Ch 18 | taught | Note 45 (learning a model from experience) |
| Identifying Hidden Markov Models (HMMs) | Ch 18 | taught | Note 77 (hidden Markov model); MA-074 (EM) |
| Neural network models | Ch 18 | taught | Note 49 (learned dynamics with neural networks) |
| Generating training data | Ch 18 | taught | Note 49 (collecting data to learn dynamics) |
| From state observations | Ch 18 | taught | Note 49 (learned dynamics) |
| State-space models from input-output data (recurrent networks) | Ch 18 | taught | Note 50 (recurrent world model) |
| Input-output (autoregressive) models | Ch 18 | add | **Fitting linear dynamical models from data: least-squares fit of A and B, ARX / autoregressive input-output models** (control) -> RO-08 (extend Note 139) |
| Particle-based models | Ch 18 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Object-centric models | Ch 18 | taught | Note 333 (learned object-motion models) |
| Modeling stochasticity | Ch 18 | taught | Note 49 (ensembles for model uncertainty) |
| Control design for neural network models | Ch 18 | taught | Note 49 (sampling planners with a learned model) |
| Alternatives for nonlinear system identification | Ch 18 | index-noise | survey heading |
| Identification of hybrid systems | Ch 18 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Task-relevant models | Ch 18 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Exercises | Ch 18 | index-noise | exercises heading |
| State Estimation | Ch 19 | taught | Note 78 (Bayes filter); Note 80 |
| Observers and the Kalman Filter | Ch 19 | taught | Note 80 (Kalman filter) |
| Recursive Bayesian Filters | Ch 19 | taught | Note 78 (Bayes filter) |
| Smoothing | Ch 19 | taught | Note 263 (filtering vs optimisation; incremental smoothing named) |
| Model-Free Policy Search | Ch 20 | taught | Note 30 (policy gradient); Note 43 |
| Policy Gradient Methods | Ch 20 | taught | Note 30 (policy gradient theorem and REINFORCE) |
| The Likelihood Ratio Method (aka REINFORCE) | Ch 20 | taught | Note 30 (REINFORCE, log-derivative trick) |
| Sample efficiency | Ch 20 | taught | Note 132 (costly real samples) |
| Stochastic Gradient Descent | Ch 20 | taught | ML-058 (stochastic gradient descent) |
| The Weight Pertubation Algorithm | Ch 20 | taught | Note 43 (finite-difference parameter perturbation) |
| Weight Perturbation with an Estimated Baseline | Ch 20 | taught | Note 31 (baselines); Note 43 |
| REINFORCE w/ additive Gaussian noise | Ch 20 | taught | Note 33 (Gaussian policies) |
| Summary | Ch 20 | index-noise | summary heading |
| Sample performance via the signal-to-noise ratio. | Ch 20 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Performance of Weight Perturbation | Ch 20 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Imitation Learning | Ch 21 | taught | Note 165 (behaviour cloning) |
| Behavior cloning | Ch 21 | taught | Note 165 (behaviour cloning) |
| Visuomotor policies (aka control from pixels) | Ch 21 | taught | Note 323 (visuomotor policies) |
| Behavior cloning as sequence modeling | Ch 21 | taught | Note 339 (action chunking: predict an action sequence) |
| Supervised learning in a feedback loop: dealing with distribution shift | Ch 21 | taught | Note 165 (compounding error and DAgger) |
| Dealing with suboptimal and multimodal demonstrations | Ch 21 | taught | Note 338 (multimodal demonstrations) |
| Architectures for visuomotor policies | Ch 21 | taught | Note 350 (action heads); Note 353 |
| Desiderata | Ch 21 | index-noise | design-wishlist heading |
| Output/action decoders | Ch 21 | taught | Note 350 (action heads) |
| (Multi-modal) input encoders | Ch 21 | taught | Note 353 (pretrained visual representations); Note 157 |
| Diffusion Policy | Ch 21 | taught | Note 338 (diffusion policy) |
| Denoising Diffusion models | Ch 21 | taught | plan §4 new DL: Diffusion models |
| Diffusion Policy | Ch 21 | taught | Note 338 (diffusion policy) |
| Diffusion Policy for Linear Policies | Ch 21 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| State-feedback | Ch 21 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Output-feedback | Ch 21 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Action sequence prediction | Ch 21 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Inverse reinforcement learning | Ch 21 | taught | Note 189 (inverse RL) |
| Vistas | Ch 21 | index-noise | outlook heading |
| Multitask / foundation models for control | Ch 21 | taught | Note 349 (generalist robot policies) |
| Distributed decentralized learning (aka "fleet learning") | Ch 21 | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Be rigorous | Ch 21 | taught | Note 44 (reporting results honestly); Note 342 |
| Drake | Ap A | out-of-scope | software or tool name, not a concept |
| Pydrake | Ap A | out-of-scope | software or tool name, not a concept |
| Online Jupyter Notebooks | Ap A | out-of-scope | software or tool name, not a concept |
| Running on Google Colab | Ap A | out-of-scope | software or tool name, not a concept |
| Enabling licensed solvers | Ap A | out-of-scope | software or tool name, not a concept |
| Running on your own machine | Ap A | out-of-scope | software or tool name, not a concept |
| Getting help | Ap A | out-of-scope | software or tool name, not a concept |
| Multi-Body Dynamics | Ap B | taught | Note 281 (manipulator equation); Note 282 |
| Deriving the equations of motion | Ap B | taught | Note 281 (Lagrangian mechanics) |
| The Manipulator Equations | Ap B | taught | Note 281 (manipulator equation) |
| Recursive Dynamics Algorithms | Ap B | taught | Note 282 (recursive Newton-Euler) |
| Bilateral Position Constraints | Ap B | taught | Note 289 (constrained dynamics: contact forces as Lagrange multipliers) |
| Bilateral Velocity Constraints | Ap B | add | **Pfaffian velocity constraints A(q) q-dot = 0** (robotics) -> RO-01 (extend Note 64) |
| Hybrid models via constraint forces | Ap B | taught | Note 289 (constraint forces; hybrid modes) |
| The Dynamics of Contact | Ap B | taught | Note 289 (contact forces); Note 128 |
| Compliant Contact Models | Ap B | taught | Note 128 (contact and friction models) |
| Rigid Contact with Event Detection | Ap B | taught | Note 289 (modes switch on touch-down) |
| Impulsive Collisions | Ap B | taught | Note 289 (impacts) |
| Putting it all together | Ap B | index-noise | summary heading |
| Time-stepping Approximations for Rigid Contact | Ap B | taught | Note 128 (how a simulator steps contact) |
| Complementarity formulations | Ap B | taught | Note 289 (complementarity contact model) |
| Anitescu's convex formulation | Ap B | out-of-scope | simulator-internal contact solver (UA App. B.2): research detail; Note 128 teaches how a simulator steps contact |
| Todorov's regularization | Ap B | out-of-scope | simulator-internal contact solver (UA App. B.2): research detail; Note 128 teaches how a simulator steps contact |
| The Semi-Analytic Primal (SAP) solver | Ap B | out-of-scope | simulator-internal contact solver (UA App. B.2): research detail; Note 128 teaches how a simulator steps contact |
| Beyond Point Contact | Ap B | out-of-scope | simulator-internal contact solver (UA App. B.2): research detail; Note 128 teaches how a simulator steps contact |
| Variational mechanics | Ap B | out-of-scope | analytical-mechanics formulation (d'Alembert, stationary action, Hamiltonian; MLS 6.2, UA App. B.3); the plan derives dynamics by Lagrange (Note 281) and multipliers (Note 289); Hamiltonian dropped in plan §7 |
| Virtual work | Ap B | add | **Principle of virtual work (why tau = J' F)** (robotics) -> RB-01 (extend Note 277) |
| D'Alembert's principle and the force of inertia | Ap B | out-of-scope | analytical-mechanics formulation (d'Alembert, stationary action, Hamiltonian; MLS 6.2, UA App. B.3); the plan derives dynamics by Lagrange (Note 281) and multipliers (Note 289); Hamiltonian dropped in plan §7 |
| Principle of Stationary Action | Ap B | out-of-scope | analytical-mechanics formulation (d'Alembert, stationary action, Hamiltonian; MLS 6.2, UA App. B.3); the plan derives dynamics by Lagrange (Note 281) and multipliers (Note 289); Hamiltonian dropped in plan §7 |
| Hamiltonian Mechanics | Ap B | out-of-scope | analytical-mechanics formulation (d'Alembert, stationary action, Hamiltonian; MLS 6.2, UA App. B.3); the plan derives dynamics by Lagrange (Note 281) and multipliers (Note 289); Hamiltonian dropped in plan §7 |
| Exercises | Ap B | index-noise | exercises heading |
| Optimization and Mathematical Programming | Ap C | taught | MA-065 (convex and non-convex costs); MA-067; MA-068 |
| Optimization software | Ap C | out-of-scope | software or tool name, not a concept |
| General concepts | Ap C | index-noise | grouping heading |
| Convex vs nonconvex optimization | Ap C | taught | MA-065 (convex vs non-convex cost functions) |
| Constrained optimization with Lagrange multipliers | Ap C | taught | MA-066 (Lagrange multipliers) |
| Convex optimization | Ap C | taught | MA-067 (convex sets and functions) |
| Linear Programs/Quadratic Programs/Second-Order Cones | Ap C | taught | MA-068 (linear and quadratic programming) |
| Semidefinite Programming and Linear Matrix Inequalities | Ap C | out-of-scope | semidefinite programming / LMI formulations (UA App. C): graduate convex-optimisation topic |
| Semidefinite programming relaxation of general quadratic optimization | Ap C | out-of-scope | semidefinite programming / LMI formulations (UA App. C): graduate convex-optimisation topic |
| Sums-of-squares optimization | Ap C | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Sums of squares on a Semi-Algebraic Set | Ap C | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Sums of squares optimization on an Algebraic Variety | Ap C | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| DSOS and SDSOS | Ap C | out-of-scope | sums-of-squares / polynomial optimisation for verification (UA ch.9, App. C): research-level method |
| Solution techniques | Ap C | taught | MA-068 (simplex and solution of LP/QP) |
| Nonlinear programming | Ap C | taught | Note 208 (nonlinear MPC solvers); MA-064 |
| Second-order methods (SQP / Interior-Point) | Ap C | taught | Note 208 (SQP and interior point, overview) |
| First-order methods (SGD / ADMM) | Ap C | taught | ML-058 (stochastic gradient descent) |
| Penalty methods | Ap C | taught | Note 194 (penalty methods) |
| Projected Gradient Descent | Ap C | add | **Projected gradient descent: gradient step, then project back onto the feasible set** (maths) -> MA 07-optimisation (short section after MA-068) |
| Zero-order methods (CMA) | Ap C | taught | Note 43 (CMA-ES) |
| Example: Inverse Kinematics | Ap C | taught | Note 279 (numerical IK) |
| Mixed-discrete (combinatorial) and continuous optimization | Ap C | add | **Mixed-integer programming (MILP/MIQP): optimisation with on/off decisions, e.g. footstep and contact-sequence planning** (maths) -> MA 07-optimisation (new short section after MA-068); used by Note 306 |
| Search, SAT, First order logic, SMT solvers, LP interpretation | Ap C | out-of-scope | logic and SAT/SMT solvers: a different field (computer-science verification) |
| Mixed-integer convex optimization | Ap C | add | **Mixed-integer programming (MILP/MIQP): optimisation with on/off decisions, e.g. footstep and contact-sequence planning** (maths) -> MA 07-optimisation (new short section after MA-068); used by Note 306 |
| Graphs of Convex Sets | Ap C | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Shortest path problems | Ap C | out-of-scope | research-level topic (current-literature method or open question in the book's own words) |
| Applications | Ap C | index-noise | applications heading |
| "Black-box" optimization | Ap C | taught | Note 43 (black-box search) |
| An Optimization Playbook | Ap D | out-of-scope | solver-formulation tricks for convex programs (UA App. D): solver-level detail |
| Matrices | Ap D | out-of-scope | solver-formulation tricks for convex programs (UA App. D): solver-level detail |
| Ellipsoids | Ap D | out-of-scope | solver-formulation tricks for convex programs (UA App. D): solver-level detail |
| Polytopes | Ap D | out-of-scope | solver-formulation tricks for convex programs (UA App. D): solver-level detail |
| Perspective functions | Ap D | out-of-scope | solver-formulation tricks for convex programs (UA App. D): solver-level detail |
| (Mixed-)Integer Programming | Ap D | add | **Mixed-integer programming (MILP/MIQP): optimisation with on/off decisions, e.g. footstep and contact-sequence planning** (maths) -> MA 07-optimisation (new short section after MA-068); used by Note 306 |
| Bilinear Matrix Inequalities (BMIs) | Ap D | out-of-scope | solver-formulation tricks for convex programs (UA App. D): solver-level detail |
| Geometry (SE(3), Penetration, and Contact) | Ap D | out-of-scope | solver-formulation tricks for convex programs (UA App. D): solver-level detail |
| Miscellaneous | Ap E | index-noise | appendix of course logistics |
| How to cite these notes | Ap E | index-noise | citation instructions |
| Annotation tool etiquette | Ap E | index-noise | course logistics |
| Some great final projects | Ap E | index-noise | course logistics |
| Please give me feedback! | Ap E | index-noise | course logistics |
