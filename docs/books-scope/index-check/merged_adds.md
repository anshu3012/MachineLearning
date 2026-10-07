# Merged adds for the robotics plan

**234 unique concepts** merged from 390 entries in ten ledgers (ctrl, dec, robo, uniA, uniB, verify, vis, web, yt, adv).

- `new`: 137
- `partial`: 87
- `already-taught` (dropped from the adds): 10
- core (3 or more independent sources): 59

**How sources are counted.** One source = one book, course, lecture playlist or glossary. The same author's book, course and lectures count once (Lynch & Park book + Lynch lectures; Tedrake's book, MIT 6.8210 and lectures). All Wikipedia pages count once.

**How status was set.** Each concept was searched by regex in every MA/ML/DL Note body, `glossary.md`, and the robotics.md Note titles, "Teaches" column and §4 table (`merge_work/search.py`, hits in `merge_work/hits.txt`). Every hit was then read. A concept is `already-taught` only when the cited Note's body (MA/ML/DL) or Teaches (RO/RL/RB, §4) states it.

## 1. Proposed new chapters

1. **MA 09 Signals and systems** (new MA chapter, after MA 08; needs MA 06's planned ODE, state-space and matrix-exponential Notes). In order:
   1. Linear time-invariant systems: impulse response and convolution
   2. Fourier series and the Fourier transform
   3. Sampling and aliasing
   4. The Laplace transform
   5. The z-transform and discrete-time systems
   6. Digital filters: moving average, low-pass, FIR and IIR
   7. Random processes: white noise, random walks and noise density
2. **RO-06 Classical feedback control** (the old RO-06 split in two). In order:
   1. *new* Feedback basics: open and closed loop and the block diagram
   2. 117 PD and PID control
   3. 118 Step response and second-order systems (+ first-order systems and step-response specs)
   4. *new* Transfer functions, poles and zeros (+ root locus)
   5. *new* Frequency response and Bode plots
   6. *new* The Nyquist criterion and stability margins
   7. *new* Sensitivity, robustness and loop shaping (+ lead/lag)
   8. 119 Feedforward, integral action, cascades and windup (+ anti-windup, internal model principle)
   9. *new* PID tuning in practice (+ filters inside the loop)
   10. *new* Digital control: sampling a continuous controller

   Notes 120 to 125 become **RO-06b Path tracking**, unchanged.

## 2. Proposed new Notes, in reading order

**MA 05 linear algebra**
- after MA-053: Solving linear systems: Gaussian elimination
- after MA-056: Graphs and their matrices: adjacency, degree, paths and connectivity
- after that: The graph Laplacian (+ stochastic matrices)
- after MA-060: QR decomposition and least squares
- after the planned "Axis-angle, exponential and log maps" Note: Lie groups for robot poses

**MA 06 calculus**
- after MA-064: The Laplacian and Laplace's equation
- after that: Integrals and the fundamental theorem of calculus
- after that, before the planned ODEs Note: Complex numbers and Euler's formula

**MA 02 / MA 07 / MA 08, ML**
- MA 02, after the planned Markov chains Note: Bayesian networks
- MA 07, after MA-068: Mixed-integer programming and branch and bound; then Derivative-free optimisation (local search, annealing, genetic algorithms, SPSA); then Constrained optimisation algorithms (projected gradient, augmented Lagrangian, ADMM)
- MA 08, after MA-072: Bayesian estimation: posteriors and conjugate priors
- MA 08, after the planned "Linear transforms of a Gaussian": Propagating uncertainty through a function
- ML 09, after ML-126: Mean-shift clustering

**MA 09 Signals and systems**: 7 Notes, listed in §1.

**RO**
- RO-03, after 82 (opens the chapter): Sensor basics and simple sensors (specs, decibels, bumpers, infrared, ultrasonic)
- RO-03, after 88: Camera hardware: lenses, exposure and image sensors
- RO-06: 6 Notes, listed in §1
- RO-15, after 205: Observers and output feedback: Luenberger observer, separation principle, LQG
- RO-15, after that: Underactuated systems: cart-pole, acrobot and swing-up
- RO-18, before 227: Pixels, point operators and colour spaces; then Binary images: thresholds, morphology and blobs
- RO-18, after 227: Edges: Canny, the image Laplacian and Laplacian of Gaussian (before SIFT in 228)
- RO-18, after 231: Visual servoing
- RO-19, after 238: Neural radiance fields and Gaussian splatting for robot maps
- RO-22, after 257: Batch estimation and smoothing
- RO-23, after 270: Consensus: agreement over a graph; then Formation control and swarms (both before 271)

**RB**
- RB-01, after 280: Closed chains and parallel robots
- RB-02, after 282 (before 283): Actuators: electric motors, drivers, fluid power and elastic actuators
- RB-03, after 289: Grippers and end effectors
- RB-03, after 292 (before 293): Symbolic task planning: STRIPS and PDDL

All other `new` and `partial` concepts are sections added to existing or planned Notes (table below).

Total: 45 new Notes (rows with `new_note`), one new MA chapter, one rebuilt RO chapter.

## 3. The 20 most-cited concepts

| # | Concept | Sources | Status | Placement |
|---|---|---|---|---|
| 1 | Linear time-invariant systems | 10 | partial | MA 09-signals-and-systems (new): new Note (chapter start, after MA 06 planned Stability Note) |
| 2 | Frequency response and Bode plots | 9 | new | RO-06: new Note after new RO: Transfer functions, poles and zeros |
| 3 | Control-system basics | 8 | partial | RO-06: new Note (before 117) |
| 4 | State observers and output feedback | 8 | partial | RO-15: new Note after 205 |
| 5 | Transfer functions | 8 | new | RO-06: new Note after 118 |
| 6 | Fourier series and the Fourier transform | 7 | new | MA 09-signals-and-systems (new): new Note after new MA: Linear time-invariant systems |
| 7 | Laplace transform | 7 | new | MA 09-signals-and-systems (new): new Note after new MA: Sampling and aliasing |
| 8 | Edge detection | 6 | partial | RO-18: new Note after 227 |
| 9 | Hough transform for lines and circles | 6 | new | RO-18: extend 229 |
| 10 | Loop shaping; lead, lag and lead-lag compensators | 6 | new | RO-06: extend new RO: Sensitivity, robustness and loop shaping |
| 11 | LQG | 6 | new | RO-15: extend new RO: Observers and output feedback |
| 12 | Binary images | 5 | new | RO-18: new Note after new RO: Pixels, point operators and colour spaces |
| 13 | Camera hardware | 5 | new | RO-03: new Note after 88 |
| 14 | Digital control | 5 | partial | RO-06: new Note after new RO: PID tuning in practice |
| 15 | Graph basics | 5 | new | MA 05-linear-algebra: new Note after MA-056 |
| 16 | Image Laplacian, Laplacian of Gaussian, difference of Gaussians, zero crossings, Laplacian pyramid | 5 | new | RO-18: extend new RO: Edges: Canny, the image Laplacian and LoG |
| 17 | Matrix Lie groups SO(3)/SE(3) for estimation | 5 | partial | MA 05-linear-algebra: new Note after new MA: Axis-angle, exponential and log maps of rotations |
| 18 | Mixed-integer programming (MILP/MIQP) | 5 | new | MA 07-optimisation: new Note after MA-068 |
| 19 | Loop transfer function, Nyquist criterion, gain/phase/delay margins | 5 | new | RO-06: new Note after new RO: Frequency response and Bode plots |
| 20 | Pixels and point operators | 5 | new | RO-18: new Note (before 227) |

## 4. Already taught (dropped from the adds)

| Concept | Where it is taught |
|---|---|
| Euclidean space R^n | MA-048 §2: "a vector in an n-dimensional space has n components" (G-610 dimension) |
| Numerical derivatives: central differences (complex step) | MA-061: "the central difference (G-363) ... Its error shrinks like h^2"; the complex-step method is beyond beginner depth |
| Maximum a posteriori (MAP) estimation | MA-072 §7 'MAP estimation: maximum likelihood plus a prior' (G-1189) |
| Raw and central moments | MA-028 §2.1 'Statistical moments' (G-1882) |
| Quasi-Newton methods BFGS and L-BFGS | MA-064: "Quasi-Newton methods (G-1603): BFGS (G-283) and L-BFGS (G-1023)", with the secant equation |
| Robust loss functions (Huber) | DL-014 §7 Huber loss (G-8, Huber loss); Note 235 lists "Robust cost functions (Huber, Cauchy)" |
| Bayesian optimisation acquisition functions | ML-128: "Expected improvement, step by step"; Acquisition function (G-163), Expected improvement (G-724) |
| Warm-starting a solver | Note 208: "Real-time MPC: warm starts, real-time iteration, stopping early" |
| Law of cosines | MA-050 §5.1: "The three vectors a, b and a - b form a triangle. The law of cosines gives:"; its IK use is Note 279 (2-link planar arm) |
| Springs and dampers (Hooke's law) | plan §4 'Second-order linear systems: mass-spring-damper; natural frequency and damping ratio' (short section in Note 118) |

## 5. All concepts

Placement: **new** = new Note after the named Note; **ext** = section added to the named Note. "new MA:/new RO:" names a Note that is planned (§4) or proposed here.

| Concept | Status | Src | Core | Placement | Missing / note | Ledgers |
|---|---|---|---|---|---|---|
| Bayesian networks: a joint distribution as a product of local conditionals; conditional independence, Markov blanket, ancestral sampling | partial | 3 | yes | MA 02-probability: **new** after new MA: Markov chains — *Bayesian networks* | Note 77 teaches "hidden Markov model / dynamic Bayes network" for one filter; general Bayes networks are missing | dec, uniA, vis |
| Conditional expectation (law of total expectation) | new | 1 |  | MA 02-probability: **ext** MA-019 | everything: nothing | robo |
| Irreducible and aperiodic Markov chains converge to one stationary distribution | new | 1 |  | MA 02-probability: **ext** new MA: Markov chains | everything: plan §4 'Markov chains' lists the stationary distribution, not when it exists or is reached | ctrl |
| Multivariate uniform distribution (uniform over a box) | new | 1 |  | MA 03-distributions: **ext** MA-029 | everything: MA-029 teaches the one-variable uniform | dec |
| atan2, the two-argument arctangent | new | 2 |  | MA 05-linear-algebra: **ext** new MA: Rigid-body transforms and homogeneous coordinates | everything: nothing | robo |
| Fixed-axis vs moving-axis (extrinsic vs intrinsic) rotation order | new | 1 |  | MA 05-linear-algebra: **ext** new MA: 3D rotations: Euler angles and quaternions | everything: nothing | robo |
| Solving Ax = b: Gaussian elimination, row-echelon form, pivots, free variables; existence and uniqueness of solutions | new | 2 |  | MA 05-linear-algebra: **new** after MA-053 — *Solving linear systems: Gaussian elimination* | everything: nothing (ML-053 inverts a matrix but never eliminates) | adv, ctrl |
| Graph basics: directed/undirected and weighted graphs, degree, neighbours, paths, cycles, trees, connectivity and connected components, adjacency matrix | new | 5 | yes | MA 05-linear-algebra: **new** after MA-056 — *Graphs and their matrices: adjacency, degree, paths and connectivity* | everything: Note 103 uses a graph only as a search space; no Note teaches adjacency matrix, degree or connectivity | ctrl, dec, robo |
| Graph Laplacian L = D - A: incidence matrix, quadratic form x^T L x, eigenvalues, algebraic connectivity | new | 2 |  | MA 05-linear-algebra: **new** after new MA: Graphs and their matrices — *The graph Laplacian* | everything: nothing | ctrl |
| Left and right pseudo-inverse (tall vs wide matrices) | partial | 1 |  | MA 05-linear-algebra: **ext** MA-060 | MA-060 teaches the Moore-Penrose pseudo-inverse (G-1261) through the SVD; the left (A^T A)^-1 A^T and right A^T (A A^T)^-1 forms are missing | robo |
| Matrix Lie groups SO(3)/SE(3) for estimation: group, Lie algebra, tangent-space perturbations, pose uncertainty | partial | 5 | yes | MA 05-linear-algebra: **new** after new MA: Axis-angle, exponential and log maps of rotations — *Lie groups for robot poses: perturbations and uncertainty on SO(3) and SE(3)* | plan §4 'Axis-angle, exponential and log maps of rotations' teaches exp/log of SO(3) only; group view, perturbations and pose uncertainty are missing | uniA, vis |
| Lines and planes in parametric form p = p0 + t d (affine subspace) | new | 1 |  | MA 05-linear-algebra: **ext** MA-051 | everything: MA-051 teaches only the implicit form w.x + b = 0 | ctrl |
| Inverse and composition of poses with homogeneous matrices | new | 1 |  | MA 05-linear-algebra: **ext** new MA: Rigid-body transforms and homogeneous coordinates | everything: plan §4 rigid-body Note lists 'homogeneous matrix' but not inverting or chaining poses | vis |
| QR decomposition (Gram-Schmidt) and least squares by QR | new | 2 |  | MA 05-linear-algebra: **new** after MA-060 — *QR decomposition and least squares* | everything: MA-047 only names QR in a list ("LU, QR, eigen-decomposition and SVD"); mentioned only | dec, vis |
| Quaternion algebra: conjugate, product, rotating a vector | partial | 1 |  | MA 05-linear-algebra: **ext** new MA: 3D rotations: Euler angles and quaternions | plan §4 '3D rotations: Euler angles and quaternions' names quaternions; the operations are not listed | robo |
| Repeated eigenvalues: algebraic vs geometric multiplicity, defective matrices, when a matrix is diagonalisable; Jordan form named | partial | 3 | yes | MA 05-linear-algebra: **ext** MA-056 | MA-056 §5 shows the shear has too few eigenvectors to be diagonalised (G-602); multiplicities, 'defective' and Jordan form are missing | ctrl |
| Right-handed frames and the right-hand rule | new | 1 |  | MA 05-linear-algebra: **ext** new MA: Cross product and skew-symmetric matrix | everything: nothing | robo |
| Rotation facts: det +1 (proper vs improper), rotations do not commute, gimbal lock, q and -q are the same rotation | new | 2 |  | MA 05-linear-algebra: **ext** new MA: 3D rotations: Euler angles and quaternions | everything: nothing | vis |
| Non-negative and row-stochastic matrices: eigenvalue 1, left eigenvector, Perron-Frobenius statement | new | 1 |  | MA 05-linear-algebra: **ext** new MA: The graph Laplacian | everything: nothing | ctrl |
| Total least squares: fit a line or plane with errors in all coordinates by the last singular vector | new | 2 |  | MA 05-linear-algebra: **ext** MA-060 | everything: nothing; plan §4 has only "Ax = 0 by the SVD" (short section in Note 89) | verify, yt |
| Trace of a matrix: sum of the diagonal = sum of the eigenvalues | new | 3 | yes | MA 05-linear-algebra: **ext** MA-056 | everything: nothing | adv, ctrl, vis |
| Trigonometry basics: right triangles, sin/cos/tan, identities, inverse functions | partial | 1 |  | MA 05-linear-algebra: **ext** new MA: Rigid-body transforms and homogeneous coordinates | MA-049 §1 teaches Pythagoras; sin, cos, tan, identities and inverse functions are used (MA-063 polar map) but never taught | robo |
| Vector norms L1, L2 and L-infinity; Manhattan, Euclidean and Chebyshev distance | partial | 3 | yes | MA 05-linear-algebra: **ext** MA-049 | MA-049 §2 teaches L2 and names L1 (G-1025, G-1028); L-infinity and the Chebyshev/Manhattan distance names are missing | dec, robo |
| Whitening transform: decorrelate data with the covariance | new | 2 |  | MA 05-linear-algebra: **ext** new MA: Mahalanobis distance | everything: nothing | vis |
| Automatic differentiation: forward and reverse mode | partial | 1 |  | MA 06-calculus: **ext** MA-063 | MA-063 §10 teaches reverse mode as backpropagation (G-232); forward mode is missing | dec |
| Complex numbers: real and imaginary parts, magnitude and angle, polar form, Euler's formula, the complex plane | new | 2 |  | MA 06-calculus: **new** after new MA: Integrals and the fundamental theorem of calculus — *Complex numbers and Euler's formula* | everything: MA-056 only says NumPy reports complex eigenvalues | ctrl, web |
| Continuity of a function | new | 1 |  | MA 06-calculus: **ext** MA-061 | everything: nothing | robo |
| Control-affine systems: drift and control vector fields | new | 2 |  | MA 06-calculus: **ext** new MA: State-space models | everything: nothing | robo |
| Stability of x(k+1) = A x(k): all eigenvalues inside the unit circle | partial | 3 | yes | MA 06-calculus: **ext** new MA: Stability of dynamical systems | plan §4 Stability Note uses eigenvalues for continuous time only | ctrl, web |
| The double integrator x'' = u (chain of integrators) | new | 2 |  | MA 06-calculus: **ext** new MA: State-space models | everything: nothing | ctrl, robo |
| The Laplacian operator and Laplace's equation: sum of second derivatives, harmonic functions, solving on a grid | new | 2 |  | MA 06-calculus: **new** after MA-064 — *The Laplacian and Laplace's equation* | everything: nothing | robo, vis |
| Implicit function theorem | new | 1 |  | MA 06-calculus: **ext** MA-063 | everything: nothing | robo |
| Integrals and the fundamental theorem of calculus | partial | 2 |  | MA 06-calculus: **new** after new MA: The Laplacian and Laplace's equation — *Integrals and the fundamental theorem of calculus* | MA-022 §3 teaches the integral as area under a PDF (G-13); antiderivatives, the fundamental theorem and computing integrals are missing | dec |
| LaSalle's invariance principle and invariant sets | new | 4 | yes | MA 06-calculus: **ext** new MA: Stability of dynamical systems | everything: nothing | adv, ctrl |
| Linear ODEs: homogeneous and particular solutions | partial | 2 |  | MA 06-calculus: **ext** new MA: ODEs and vector fields | plan §4 'ODEs and vector fields' teaches "an equation for change"; homogeneous and particular solutions are missing | robo, web |
| Quadratic Lyapunov functions V = x^T P x and the Lyapunov equation A^T P + P A = -Q | partial | 4 | yes | MA 06-calculus: **ext** new MA: Stability of dynamical systems | plan §4 Stability Note lists "Lyapunov functions"; the quadratic form and the Lyapunov equation are missing | adv, ctrl |
| Modes of a linear system: x' = Ax as a sum of eigenvector modes e^(lambda t) v | partial | 3 | yes | MA 06-calculus: **ext** new MA: Matrix exponential and logarithm | plan §4 'Matrix exponential' teaches e^(At); the eigenvector-mode reading is missing | ctrl, uniB |
| Neumann series (I - A)^-1 = sum of A^k | new | 1 |  | MA 06-calculus: **ext** new MA: Geometric series | everything: nothing | ctrl |
| ODE solving basics: initial vs boundary value, explicit vs implicit integrators, stiffness, step size, local and global error | new | 1 |  | MA 06-calculus: **ext** new MA: Numerical integration of ODEs | everything: plan §4 'Numerical integration of ODEs' lists only Euler and Runge-Kutta | adv |
| Phase-plane equilibria: node, saddle, focus, centre from the eigenvalues of a planar system | partial | 1 |  | MA 06-calculus: **ext** new MA: Stability of dynamical systems | plan §4 Stability Note lists "equilibria, eigenvalues"; the types are missing | ctrl |
| The simple pendulum as the first nonlinear system: phase portrait, equilibria, damping, torque limits | new | 1 |  | MA 06-calculus: **ext** new MA: ODEs and vector fields | everything: nothing (Notes 296/299 use inverted-pendulum models of walking) | adv |
| Stability definitions: equilibrium, Lyapunov, asymptotic and exponential stability, local vs global, region of attraction, stability by linearisation | partial | 5 | yes | MA 06-calculus: **ext** new MA: Stability of dynamical systems | plan §4 'Stability of dynamical systems' lists "equilibria, eigenvalues, Lyapunov functions"; the kinds of stability and the region of attraction are missing | adv, robo, verify, web |
| Augmented Lagrangian and ADMM | new | 1 |  | MA 07-optimisation: **ext** new MA: Constrained optimisation algorithms | everything: nothing | dec |
| Genetic algorithms and population methods: selection, crossover, mutation | new | 3 | yes | MA 07-optimisation: **ext** new MA: Derivative-free optimisation | everything: nothing (Note 43 teaches ES and CMA-ES, not GAs) | dec, web |
| Line search and step-size rules: backtracking, Wolfe conditions, golden section | partial | 4 | yes | MA 07-optimisation: **ext** MA-064 | MA-064 says only "usually shortened by a line search (trying a shorter step until the function drops enough)" | dec, vis |
| Local search: hill climbing, pattern search, simulated annealing | partial | 2 |  | MA 07-optimisation: **new** after new MA: Mixed-integer programming — *Derivative-free optimisation: local search, annealing and genetic algorithms* | ML-058 names simulated annealing only as an analogy for a learning schedule (G-1810); the methods are not taught | dec |
| Mixed-integer programming (MILP/MIQP): integer choices inside an LP/QP, why harder, branch and bound; use for footholds, contacts, routing | new | 5 | yes | MA 07-optimisation: **new** after MA-068 — *Mixed-integer programming and branch and bound* | everything: nothing | adv, dec, uniA, uniB, yt |
| Projected gradient descent | new | 1 |  | MA 07-optimisation: **new** after new MA: Derivative-free optimisation — *Constrained optimisation algorithms: projected gradient, augmented Lagrangian and ADMM* | everything: nothing | adv |
| Second-order cone programs | new | 1 |  | MA 07-optimisation: **ext** MA-068 | everything: nothing | dec |
| Gradient estimation by random perturbation (SPSA) | new | 2 |  | MA 07-optimisation: **ext** new MA: Derivative-free optimisation | everything: nothing | dec |
| Weighted least squares: weight residuals by inverse noise covariance | new | 1 |  | MA 07-optimisation: **ext** new MA: Nonlinear least squares (Gauss-Newton) | everything: nothing | vis |
| Bayesian parameter learning: posterior over parameters, conjugate priors (Beta-Bernoulli, Dirichlet, normal-normal), predictive distribution, Bayesian linear regression | partial | 3 | yes | MA 08-likelihood: **new** after MA-072 — *Bayesian estimation: posteriors and conjugate priors* | MA-072 §7 teaches the posterior's peak (MAP, G-1189); the full posterior, conjugate updates and prediction are missing | dec, vis |
| Conditioning a joint Gaussian: marginal, conditional mean and covariance from the block covariance | new | 4 | yes | MA 08-likelihood: **ext** new MA: Linear transforms of a Gaussian | everything: nothing | adv, ctrl, vis |
| Uncertainty propagation through a function: Monte Carlo, linearisation, sigma points as one idea | new | 1 |  | MA 08-likelihood: **new** after new MA: Linear transforms of a Gaussian — *Propagating uncertainty through a function* | everything: Notes 81 and 256 each push a Gaussian one way; the common idea is not taught | dec |
| Discrete-time filters: moving average, first-order low-pass (IIR), FIR vs IIR, cutoff frequency | partial | 1 |  | MA 09-signals-and-systems (new): **new** after new MA: The z-transform — *Digital filters: moving average, low-pass, FIR and IIR* | DL-033 teaches the EWMA (G-735), which is a first-order IIR low-pass, and DL-042 §4.1 a moving average; the filter view (cutoff, FIR vs IIR) is missing | vis |
| Fourier series and the Fourier transform: frequency, magnitude and phase, convolution theorem, low/high/band-pass, power spectrum, DFT/FFT, 2D Fourier of images | new | 7 | yes | MA 09-signals-and-systems (new): **new** after new MA: Linear time-invariant systems — *Fourier series and the Fourier transform* | everything: Note 26 teaches only Fourier basis features; no Note teaches the transform | dec, robo, uniB, vis, web, yt |
| Laplace transform: transforms of step, impulse, exponential; derivative = multiply by s; transfer function as the transform of the impulse response; initial and final value theorems | new | 7 | yes | MA 09-signals-and-systems (new): **new** after new MA: Sampling and aliasing — *The Laplace transform* | everything: nothing | adv, ctrl, robo, uniB, web, yt |
| Linear time-invariant systems: linearity, superposition, time invariance, impulse response, output = input convolved with the impulse response (1D and 2D) | partial | 10 | yes | MA 09-signals-and-systems (new): **new** (chapter start, after MA 06 planned Stability Note) — *Linear time-invariant systems: impulse response and convolution* | DL-042 §4 and §6 teach the sliding-window convolution of an image; time invariance, superposition and the impulse response are missing | adv, ctrl, uniB, verify, vis, web, yt |
| Random processes: white noise and its power spectral density, random walk, Gauss-Markov process, continuous noise density to a discrete Q | partial | 3 | yes | MA 09-signals-and-systems (new): **new** after new MA: Digital filters — *Random processes: white noise, random walks and noise density* | Note 83 teaches 'Bias random walk'; white noise, PSD, Gauss-Markov and discretising Q are missing | uniA, verify, vis |
| Sampling theorem (Nyquist rate) and aliasing; anti-alias filtering | new | 2 |  | MA 09-signals-and-systems (new): **new** after new MA: Fourier series and the Fourier transform — *Sampling and aliasing* | everything: nothing | vis, yt |
| Z-transform and discrete-time transfer functions | new | 5 | yes | MA 09-signals-and-systems (new): **new** after new MA: The Laplace transform — *The z-transform and discrete-time systems* | everything: nothing | adv, web, yt |
| Kernel (covariance) function and kernel matrix of a Gaussian process | partial | 1 |  | ML (new GP Note, plan §4): **ext** new ML: Gaussian processes | ML-128 names a Gaussian process (G-832) as a surrogate; the planned GP Note lists "mean and uncertainty", not the kernel | vis |
| Generative vs discriminative models | new | 1 |  | ML 07-classification: **ext** ML-081 | everything: nothing | vis |
| Mean-shift: mode seeking on a density; clustering and segmentation | new | 2 |  | ML 09-clustering-and-more: **new** after ML-126 — *Mean-shift clustering* | everything: nothing | yt |
| Variational inference and the ELBO | partial | 2 |  | DL Generative models (new chapter, plan §4): **ext** new DL: Variational autoencoder | plan §4 VAE Note lists "reconstruction + beta KL"; the ELBO derivation is missing | uniB, vis |
| Softmax (Boltzmann) exploration over action values | new | 1 |  | RL-01: **ext** 4 | everything: Note 5 uses softmax over preferences, not over action values | dec |
| Evaluative vs instructive feedback | new | 1 |  | RL-01: **ext** 1 | everything: nothing | dec |
| Regret of an exploration strategy | new | 1 |  | RL-01: **ext** 4 | everything: nothing | robo |
| Thompson sampling (posterior sampling) | new | 2 |  | RL-01: **ext** 4 | everything: nothing | dec |
| Absorbing terminal state | new | 2 |  | RL-02: **ext** 8 | everything: nothing | dec |
| Bellman operator as a contraction: why value iteration converges | new | 2 |  | RL-02: **ext** 14 | everything: nothing | dec |
| Markov reward process | new | 1 |  | RL-02: **ext** 10 | everything: nothing | dec |
| Reward-to-go in policy gradients | new | 1 |  | RL-04: **ext** 30 | everything: nothing | dec |
| State aggregation | new | 1 |  | RL-04: **ext** 26 | everything: nothing | dec |
| Catastrophic forgetting (interference) | new | 2 |  | RL-05: **ext** 36 | everything: nothing | dec |
| Control as probabilistic inference; max-entropy RL as variational inference | new | 1 |  | RL-05: **ext** 42 | everything: nothing | uniB |
| Scalarising several objectives: weighted sum and the constraint method | new | 1 |  | RL-07: **ext** 53 | everything: Note 53 teaches Pareto-optimal plans, not how to scalarise | dec |
| Value of information | new | 1 |  | RL-07: **ext** 53 | everything: nothing | dec |
| Under-, fully and over-actuated robots | partial | 2 |  | RO-01: **ext** 66 | Note 221 names quadrotor underactuation; the general classes are missing | robo, verify |
| Cartesian product of spaces | new | 3 | yes | RO-01: **ext** 72 | everything: nothing | robo |
| Explicit vs implicit C-space representations | new | 1 |  | RO-01: **ext** 72 | everything: nothing | verify |
| Instantaneous centre of rotation | new | 1 |  | RO-01: **ext** 66 | everything: nothing | robo |
| Pfaffian velocity constraints A(q)q' = 0 and the form q' = G(q)u | partial | 4 | yes | RO-01: **ext** 64 | Note 64 teaches holonomic vs nonholonomic constraints; the Pfaffian matrix form is missing | adv, robo, verify |
| Steering mechanisms: turntable, Ackermann, skid steer, tracks | partial | 2 |  | RO-01: **ext** 66 | Note 67 teaches Ackermann; turntable and skid-steer/tracks are missing | robo, web |
| Car with trailers | new | 1 |  | RO-01: **ext** 64 | everything: nothing | robo |
| Filter honesty: innovation and its covariance, NEES and NIS tests | new | 3 | yes | RO-02: **ext** 81 | everything: nothing | adv, vis |
| HMM inference: forward-backward smoothing and Viterbi | partial | 1 |  | RO-02: **ext** 79 | Note 77 names the hidden Markov model; forward-backward and Viterbi are missing | vis |
| Choosing and estimating Q and R | new | 1 |  | RO-02: **ext** 80 | everything: nothing | vis |
| Camera hardware: lens law, focus, aperture, depth of field, exposure, global vs rolling shutter, CCD/CMOS, noise, Bayer filter, dynamic range | new | 5 | yes | RO-03: **new** after 88 — *Camera hardware: lenses, exposure and image sensors* | everything: nothing | uniB, vis, web, yt |
| Decibels | new | 1 |  | RO-03: **ext** new RO: Sensor basics and simple sensors | everything: nothing | robo |
| Encoders: incremental (quadrature) and absolute | partial | 1 |  | RO-03: **ext** 86 | Note 86 teaches 'Wheel odometry from encoders'; how encoders work is missing | robo |
| Bilinear and multilinear interpolation on a grid | partial | 1 |  | RO-03: **ext** 89 | ML-043 teaches 1D linear interpolation for percentiles (G-1092); bilinear/multilinear on a grid is missing | dec |
| Points and lines in homogeneous coordinates: cross products, points/line at infinity, vanishing points | partial | 2 |  | RO-03: **ext** 88 | Note 88 teaches homogeneous coordinates of points only | vis |
| Image warping and resampling: forward vs inverse warping, nearest/bilinear/bicubic | new | 3 | yes | RO-03: **ext** 89 | everything: nothing | vis, yt |
| Line extraction from 2D scans and points: split-and-merge, line fitting | new | 3 | yes | RO-03: **ext** 92 | everything: nothing | robo, uniA, vis |
| Magnetometer (compass) for heading | new | 1 |  | RO-03: **ext** 83 | everything: nothing | robo |
| Pinhole terms: optical axis and centre, image plane, normalised coordinates, field of view, skew | partial | 3 | yes | RO-03: **ext** 88 | Note 88 teaches focal length and principal point; the rest is missing | vis |
| Proximity and contact sensors: bumpers, infrared, ultrasonic (sonar) | new | 4 | yes | RO-03: **ext** new RO: Sensor basics and simple sensors | everything: Note 91 names only radar and event cameras | robo, uniA, web |
| Sensor terms: active/passive, range, resolution, accuracy vs precision, bandwidth, systematic vs random error | new | 3 | yes | RO-03: **new** after 82 — *Sensor basics and simple sensors: specifications, contact and proximity sensors* | everything: nothing (ML-076 precision is a classification metric) | robo, uniA |
| Stereo matching costs: SSD, SAD, NCC, cost volume, scanline DP, semi-global matching | partial | 2 |  | RO-03: **ext** 90 | Note 90 teaches 'Dense stereo matching along rows'; the costs and SGM are missing | verify, vis |
| Range measurement: time of flight vs phase shift | partial | 1 |  | RO-03: **ext** 91 | Notes 90-91 teach time of flight; phase shift is missing | robo |
| Distance transform of a grid (grassfire, Euclidean, signed) | partial | 2 |  | RO-04: **ext** 98 | Note 97 names signed-distance (TSDF) maps; the grid distance transform for inflation is missing | vis |
| Quadtrees and multi-resolution grids | partial | 2 |  | RO-04: **ext** 97 | Note 97 teaches octrees in 3D; 2D quadtrees are missing | robo |
| Artificial potential fields: attractive and repulsive terms | partial | 2 |  | RO-05: **ext** 109 | Note 109 teaches randomized potential fields; the attractive/repulsive field is not named | robo |
| Consistent (monotone) heuristics | partial | 1 |  | RO-05: **ext** 105 | Note 105 teaches admissible heuristics only | dec |
| Distance queries between bodies (GJK named) | partial | 2 |  | RO-05: **ext** 108 | Note 108 teaches collision detection (yes/no); distance between bodies is missing | verify |
| Checking a path segment for collision (edge resolution) | new | 1 |  | RO-05: **ext** 108 | everything: nothing | robo |
| Fast marching method and the Eikonal equation | new | 1 |  | RO-05: **ext** 106 | everything: nothing | verify |
| Grid connectivity: 4- and 8-connected | new | 2 |  | RO-05: **ext** 106 | everything: nothing | robo |
| Harmonic potential fields from Laplace's equation (no local minima) | new | 2 |  | RO-05: **ext** 109 | everything: nothing | robo, vis |
| Inevitable collision states | new | 1 |  | RO-05: **ext** 112 | everything: nothing | robo |
| Explicit vs implicit graphs; choosing a Markov search state | partial | 1 |  | RO-05: **ext** 103 | Note 103 teaches 'graph as a model of a state space'; implicit graphs are missing | uniA |
| Jump point search | new | 1 |  | RO-05: **ext** 105 | everything: nothing | uniA |
| Lazy collision checking | new | 1 |  | RO-05: **ext** 111 | everything: nothing | robo |
| Multi-goal A* (virtual goal; moving targets) | new | 1 |  | RO-05: **ext** 105 | everything: nothing | uniA |
| Narrow passages and PRM sampling strategies | new | 1 |  | RO-05: **ext** 111 | everything: nothing | robo |
| Navigation functions (Rimon-Koditschek) | partial | 1 |  | RO-05: **ext** 109 | Note 106 teaches the grid navigation function; the continuous Rimon-Koditschek form is missing | robo |
| Roadmap requirements: accessibility and connectivity | new | 1 |  | RO-05: **ext** 111 | everything: nothing | robo, verify |
| Bidirectional RRT (RRT-Connect) | new | 3 | yes | RO-05: **ext** 110 | everything: Note 105 has bidirectional graph search; RRT-Connect is missing | robo, uniA |
| Real-time heuristic search (LRTA*, RTAA*) | new | 2 |  | RO-05: **ext** 107 | everything: nothing | uniA |
| Self-collision checking | new | 1 |  | RO-05: **ext** 108 | everything: nothing | robo |
| Single-query vs multi-query planners | new | 3 | yes | RO-05: **ext** 111 | everything: nothing | robo, verify |
| Anti-windup: clamping and back-calculation | partial | 1 |  | RO-06: **ext** 119 | Note 119 teaches 'Integrator windup and actuator saturation'; the fixes are missing | verify |
| Control-system basics: open vs closed loop; plant, reference, error, sensor, actuator, disturbance, noise in one block diagram; why feedback helps | partial | 8 | yes | RO-06: **new** (before 117) — *Feedback basics: open and closed loop and the block diagram* | Note 9 teaches open-loop plan vs feedback plan (planning sense); the control block diagram and disturbance rejection are missing | robo, uniB, verify, yt |
| Filters inside control loops: derivative low-pass, notch | new | 1 |  | RO-06: **ext** new RO: PID tuning in practice | everything: nothing | yt |
| Digital control: A/D and D/A, zero-order hold, sample-rate choice, discretising a controller, z-transform and difference equations | partial | 5 | yes | RO-06: **new** after new RO: PID tuning in practice — *Digital control: sampling a continuous controller* | plan §4 'State-space models' has discrete-time models by zero-order hold (CT-029); controller discretisation and rate choice are missing | ctrl, uniB, web, yt |
| Frequency response and Bode plots: gain and phase, asymptotes, bandwidth, resonance | new | 9 | yes | RO-06: **new** after new RO: Transfer functions, poles and zeros — *Frequency response and Bode plots* | everything: nothing | ctrl, robo, uniB, web, yt |
| Internal model principle | new | 1 |  | RO-06: **ext** 119 | everything: nothing | adv |
| Loop shaping; lead, lag and lead-lag compensators | new | 6 | yes | RO-06: **ext** new RO: Sensitivity, robustness and loop shaping | everything: nothing | ctrl, uniB, web, yt |
| Loop transfer function, Nyquist criterion, gain/phase/delay margins | new | 5 | yes | RO-06: **new** after new RO: Frequency response and Bode plots — *The Nyquist criterion and stability margins* | everything: nothing | ctrl, uniB, web, yt |
| PID tuning and practice: ideal form, Ziegler-Nichols, model-based tuning, derivative kick, set-point weighting | new | 2 |  | RO-06: **new** after 119 — *PID tuning in practice* | everything: Note 117 teaches the PID law only | ctrl, verify, yt |
| Setpoint regulation vs trajectory tracking | partial | 1 |  | RO-06: **ext** new RO: Feedback basics | Note 121 teaches path following vs trajectory tracking; regulation is missing | robo |
| Root locus | new | 5 | yes | RO-06: **ext** new RO: Transfer functions, poles and zeros | everything: nothing | ctrl, robo, uniB, web |
| Sensitivity functions (S, T, gang of four), disturbance attenuation, robustness to model error and its limits | new | 5 | yes | RO-06: **new** after new RO: The Nyquist criterion and stability margins — *Sensitivity, robustness and loop shaping* | everything: nothing | ctrl, uniB, yt |
| First-order systems and step-response specs: time constant, rise time, DC gain, steady-state error, damped natural frequency | partial | 5 | yes | RO-06: **ext** 118 | Note 118 teaches overshoot, settling time, damping ratio, natural frequency of second-order systems; first-order systems and the other specs are missing | ctrl, robo, uniB, web, yt |
| Transfer functions: G(s) from the ODE or from state space; poles and zeros; BIBO stability; block-diagram algebra; pole-zero cancellation; non-minimum phase; time delay; SISO vs MIMO; Routh-Hurwitz named | new | 8 | yes | RO-06: **new** after 118 — *Transfer functions, poles and zeros* | everything: DL-027's "transfer function" means an activation function | adv, ctrl, robo, uniB, verify, web, yt |
| Reactive control and behaviour-based robotics (Braitenberg, subsumption) | new | 2 |  | RO-07: **ext** 126 | everything: nothing | robo, web |
| Fitting linear dynamical models from data: least-squares A and B, ARX; equation vs simulation error | partial | 1 |  | RO-08: **ext** 139 | Note 139 teaches system identification with actuator networks; linear least-squares and ARX fits are missing | adv |
| Potential-based reward shaping (keeps the optimal policy) | partial | 1 |  | RO-09: **ext** 146 | Note 146 teaches reward shaping and its risks; the potential-based form is missing | dec |
| Apprenticeship learning by matching feature expectations | new | 1 |  | RO-13: **ext** 189 | everything: nothing (Note 189 teaches max-entropy IRL) | dec |
| Frontier-based exploration | partial | 1 |  | RO-13: **ext** 181 | Note 181 teaches exploration by cell entropy; frontiers are missing | uniA |
| Option models and planning with options | partial | 1 |  | RO-13: **ext** 184 | Note 184 teaches options as temporally extended actions; option models and planning with them are missing | dec |
| Control Lyapunov functions and the CLF-CBF QP | partial | 3 | yes | RO-14: **ext** 199 | Note 199 teaches 'Stability certificates with Lyapunov functions'; designing u by a CLF is missing | adv, verify |
| Temporal logic task specifications (LTL) | partial | 1 |  | RO-14: **ext** 197 | Note 197 names only "Formal methods and shields" | dec |
| Value at risk (the quantile) beside CVaR | partial | 1 |  | RO-14: **ext** 198 | plan §4 'Conditional value at risk' (short section in Note 198) builds on MA-008 percentiles; VaR is not named | dec |
| Bang-bang (time-optimal) control of the double integrator | partial | 2 |  | RO-15: **ext** 203 | Note 203 teaches time-optimal time scaling; bang-bang control is not named | robo, verify |
| B-splines: smooth curves from control points with local control | partial | 2 |  | RO-15: **ext** 202 | Note 202 teaches cubic splines; B-splines are missing | robo, vis |
| Explicit MPC: the law precomputed as a piecewise-affine table | new | 2 |  | RO-15: **ext** 207 | everything: nothing | adv |
| Iterative learning control | new | 1 |  | RO-15: **ext** 206 | everything: nothing | uniB |
| Invariant sets and recursive feasibility of MPC | partial | 2 |  | RO-15: **ext** 207 | Note 207 teaches 'Terminal cost and terminal set'; invariance and recursive feasibility are missing | adv |
| LQG: LQR plus a Kalman filter (separation principle); output-feedback MPC | new | 6 | yes | RO-15: **ext** new RO: Observers and output feedback | everything: nothing | adv, dec, robo, web, yt |
| State observers and output feedback: observability matrix and rank test, Luenberger observer, stabilisability and detectability, duality | partial | 8 | yes | RO-15: **new** after 205 — *Observers and output feedback: Luenberger observer, separation principle, LQG* | Note 80 teaches 'Observability (concept only)'; the rank test, observer design and detectability are missing | adv, ctrl, uniB, vis, yt |
| Optimal-control problem anatomy: stage cost, terminal cost, cost-to-go | partial | 2 |  | RO-15: **ext** 205 | Note 14 names cost-to-go and Note 207 the terminal cost; stage cost and the general structure are missing | adv |
| Robust and stochastic MPC: tube MPC with tightened constraints, min-max, chance constraints | new | 3 | yes | RO-15: **ext** 208 | everything: nothing | adv, dec |
| Hard vs soft constraints with slack variables | new | 1 |  | RO-15: **ext** 207 | everything: nothing | adv |
| Underactuated systems: cart-pole, acrobot, energy-shaping swing-up, LQR balance, partial feedback linearisation | partial | 3 | yes | RO-15: **new** after new RO: Observers and output feedback — *Underactuated systems: cart-pole, acrobot and swing-up* | Note 221 names underactuation of the quadrotor; Notes 296/299 use inverted-pendulum walking models; cart-pole and acrobot are missing | adv, uniB, verify, yt |
| Dec-POMDP | new | 1 |  | RO-16: **ext** 214 | everything: nothing | dec |
| Markov (stochastic) games | new | 1 |  | RO-16: **ext** 214 | everything: nothing | dec |
| Inertial reference frame | new | 1 |  | RO-17: **ext** 220 | everything: nothing | robo |
| Parallel-axis theorem | new | 1 |  | RO-17: **ext** 220 | everything: Note 220 teaches the inertia matrix only | robo |
| Principal axes of inertia | new | 1 |  | RO-17: **ext** 220 | everything: nothing | robo |
| Static equilibrium: forces and torques sum to zero | partial | 1 |  | RO-17: **ext** 220 | Note 277 teaches arm statics tau = J^T F; equilibrium of a body is missing | robo |
| Aperture problem and normal flow | new | 1 |  | RO-18: **ext** 230 | everything: nothing | vis |
| Binary images: thresholding, morphology, connected components, blob moments | new | 5 | yes | RO-18: **new** after new RO: Pixels, point operators and colour spaces — *Binary images: thresholds, morphology and blobs* | everything: DL-049's "binary" means two classes | robo, vis, web, yt |
| Bag-of-words retrieval: TF-IDF, inverted index, vocabulary tree | partial | 1 |  | RO-18: **ext** 236 | Note 236 teaches 'Visual place recognition with bag of words'; TF-IDF and the inverted index are missing | vis |
| Edge detection: gradient magnitude, non-maximum suppression, hysteresis, Canny | partial | 6 | yes | RO-18: **new** after 227 — *Edges: Canny, the image Laplacian and Laplacian of Gaussian* | DL-042 §5 'Edges are changes in intensity' and Note 227 gradient filters; non-max suppression, hysteresis and Canny are missing | robo, uniA, verify, vis, web, yt |
| Colour spaces: RGB, HSV, Lab, YUV; luminance and chromaticity | partial | 2 |  | RO-18: **ext** new RO: Pixels, point operators and colour spaces | DL-042 §3.2 teaches RGB channels; other colour spaces are missing | vis, web |
| Hough transform for lines and circles | new | 6 | yes | RO-18: **ext** 229 | everything: nothing | robo, uniA, uniB, vis, web, yt |
| Image Laplacian, Laplacian of Gaussian, difference of Gaussians, zero crossings, Laplacian pyramid | new | 5 | yes | RO-18: **ext** new RO: Edges: Canny, the image Laplacian and LoG | everything: nothing | robo, uniA, vis, yt |
| Light and surfaces: radiance, irradiance, Lambertian vs specular, BRDF named | new | 1 |  | RO-18: **ext** 230 | everything: nothing | yt |
| Depth from one image with a network: scale ambiguity, relative vs metric depth, foundation depth models; learned stereo | partial | 1 |  | RO-18: **ext** 234 | Note 234 lists 'Learned depth from one image (concept)'; relative vs metric depth and foundation models are missing | uniB |
| Nonlinear image filters: median, bilateral | new | 3 | yes | RO-18: **ext** 227 | everything: nothing | vis, yt |
| Pixels and point operators: histogram, brightness/contrast, gamma, histogram equalisation (CLAHE), blending | new | 5 | yes | RO-18: **new** (before 227) — *Pixels, point operators and colour spaces* | everything: nothing | vis, web, yt |
| Separable filters | new | 1 |  | RO-18: **ext** 227 | everything: nothing | vis |
| Template matching by (normalised) cross-correlation | partial | 2 |  | RO-18: **ext** 228 | DL-042 defines cross-correlation; template matching and NCC are missing | yt |
| 2D transform hierarchy: translation, Euclidean, similarity, affine, projective | partial | 4 | yes | RO-18: **ext** 229 | MA-053 defines the affine transformation (G-178); the hierarchy and what each keeps are missing | uniB, vis, web |
| Visual servoing: IBVS, PBVS, interaction matrix in a control law | partial | 2 |  | RO-18: **new** after 231 — *Visual servoing* | Note 231 teaches the image Jacobian; using it in a control law is missing | uniA, uniB |
| Neural radiance fields and 3D Gaussian splatting | new | 1 |  | RO-19: **new** after 238 — *Neural radiance fields and Gaussian splatting for robot maps* | everything: nothing | uniB |
| Falsification: searching for disturbances that make a policy fail | new | 1 |  | RO-20: **ext** 249 | everything: nothing | dec |
| Arrival cost in moving-horizon estimation | new | 1 |  | RO-22: **ext** 263 | everything: nothing | adv |
| Batch estimation and smoothing: lifted form, Cholesky/RTS smoother, fixed-interval and fixed-lag | new | 2 |  | RO-22: **new** after 257 — *Batch estimation and smoothing* | everything: Note 263 teaches filtering vs optimisation (sliding window), not smoothing | vis |
| Iterated EKF | new | 2 |  | RO-22: **ext** 258 | everything: nothing | vis |
| Boustrophedon (lawnmower) coverage | new | 1 |  | RO-23: **ext** 273 | everything: nothing (Note 273 teaches coverage planning in general) | verify |
| Consensus (agreement) dynamics: x' = -Lx and averaging x(k+1) = A x(k) | new | 2 |  | RO-23: **new** after 270 — *Consensus: agreement over a graph* | everything: nothing | ctrl |
| Multi-robot coordination by consensus: rendezvous, formation control, cyclic pursuit, deployment, swarms | new | 2 |  | RO-23: **new** after new RO: Consensus — *Formation control and swarms* | everything: nothing | ctrl, web |
| Point-based value iteration | new | 1 |  | RO-23: **ext** 268 | everything: nothing | dec |
| Online POMDP planning by tree search (POMCP) | new | 1 |  | RO-23: **ext** 269 | everything: nothing | dec |
| Spanning-tree coverage | new | 1 |  | RO-23: **ext** 273 | everything: nothing | robo |
| Travelling salesman problem | new | 3 | yes | RO-23: **ext** 274 | everything: nothing | robo, vis |
| Robot arm types: Cartesian, SCARA, articulated, parallel | new | 2 |  | RB-01: **ext** 276 | everything: nothing | robo, web |
| Body vs spatial angular velocity and twist (and wrench) | partial | 3 | yes | RB-01: **ext** 275 | Note 275 teaches twists and the adjoint; body vs spatial forms are not named | adv, robo, uniB |
| Chasles-Mozzi theorem: every rigid motion is a screw motion | partial | 2 |  | RB-01: **ext** 275 | Note 275 teaches the screw axis; the theorem is not stated | robo, uniB |
| Differential IK as a QP with joint, velocity and collision limits | partial | 1 |  | RB-01: **ext** 280 | Note 280 teaches differential IK; the QP form with limits is missing | uniB |
| Force and acceleration ellipsoids | partial | 2 |  | RB-01: **ext** 278 | Note 278 teaches the manipulability ellipsoid | robo |
| Paden-Kahan subproblems for analytic IK | new | 1 |  | RB-01: **ext** 279 | everything: nothing | adv |
| Closed chains and parallel robots: loop-closure equations, delta, Stewart | new | 4 | yes | RB-01: **new** after 280 — *Closed chains and parallel robots* | everything: nothing | adv, robo, web |
| Fixed (space) frame vs body frame | partial | 1 |  | RB-01: **ext** 275 | Notes 276-277 use space and body forms; the two frames are not introduced | robo |
| Principle of virtual work (why tau = J^T F) | partial | 1 |  | RB-01: **ext** 277 | Note 277 teaches tau = J^T F without the reason | adv |
| Reachable vs dexterous workspace | partial | 1 |  | RB-01: **ext** 276 | Note 276 teaches workspace | adv |
| Backlash and gear transmission errors | new | 1 |  | RB-02: **ext** 283 | everything: nothing | robo |
| Collaborative robots and physical safety | new | 1 |  | RB-02: **ext** 287 | everything: nothing | robo |
| Centripetal and Coriolis terms | partial | 2 |  | RB-02: **ext** 281 | Note 281 teaches c(q, q') in the manipulator equation; the terms are not named | robo, verify |
| DC motor model: torque constant and back-EMF | partial | 2 |  | RB-02: **ext** new RB: Actuators | Note 283 teaches 'Motors'; the model is missing | robo |
| Inertial-parameter identification: dynamics linear in the parameters, least squares, exciting trajectories | partial | 1 |  | RB-02: **ext** 282 | Note 139 teaches system identification in general; the regressor form is missing | adv, uniB |
| Electric motor types: brushed, brushless, stepper, servo, AC | partial | 3 | yes | RB-02: **new** after 282 — *Actuators: electric motors, drivers, fluid power and elastic actuators* | Note 283 teaches 'Motors'; types are missing | robo, web |
| Hydraulic and pneumatic actuators | new | 2 |  | RB-02: **ext** new RB: Actuators | everything: nothing | robo, web |
| Force/torque sensors (strain gauges) | new | 3 | yes | RB-02: **ext** 286 | everything: nothing | robo |
| Gear ratio choice: direct drive vs geared, inertia matching | partial | 1 |  | RB-02: **ext** 283 | Note 283 teaches gearing and reflected inertia; the choice and direct drive are missing | robo |
| Generalized coordinates and generalized forces | partial | 1 |  | RB-02: **ext** 281 | Note 281 teaches Lagrangian mechanics without these names | adv |
| Motor drivers: PWM and H-bridge | new | 1 |  | RB-02: **ext** new RB: Actuators | everything: nothing | robo |
| Series elastic actuators | partial | 2 |  | RB-02: **ext** new RB: Actuators | Note 283 names flexible joints; SEAs are missing | robo |
| Twist-wrench (spatial) form of rigid-body dynamics | partial | 1 |  | RB-02: **ext** 282 | Note 282 teaches recursive Newton-Euler; the spatial form is missing | robo |
| Friction models: Stribeck effect | partial | 1 |  | RB-02: **ext** 283 | Note 283 teaches friction | robo |
| Gripper mechanisms: parallel jaw, linkages, suction, multi-finger | new | 2 |  | RB-03: **new** after 289 — *Grippers and end effectors* | everything: nothing | robo, web |
| Hand Jacobian and the grasp constraint | partial | 1 |  | RB-03: **ext** 290 | Note 290 teaches the grasp matrix | adv |
| Internal (squeezing) forces: null space of the grasp matrix | partial | 1 |  | RB-03: **ext** 290 | Note 290 teaches the grasp matrix | adv |
| Motion-planning libraries: MoveIt and OMPL | new | 1 |  | RB-03: **ext** 292 | everything: nothing | robo |
| Quasistatic assumption | new | 2 |  | RB-03: **ext** 292 | everything: nothing | robo |
| Soft and deformable contacts | partial | 1 |  | RB-03: **ext** 288 | Note 288 teaches the soft-finger contact type | robo |
| Linear, positive and convex span (cones of contact wrenches) | new | 1 |  | RB-03: **ext** 290 | everything: nothing | robo |
| Symbolic task planning: STRIPS/PDDL, forward search | partial | 4 | yes | RB-03: **new** after 292 — *Symbolic task planning: STRIPS and PDDL* | Note 293 teaches task and motion planning and Note 354 LLM task planning; symbolic planning is missing | robo, uniA |
| Human pose estimation: body keypoints from images | partial | 1 |  | RB-06: **ext** 317 | Note 317 teaches motion capture, video and SMPL; keypoint detection from images is missing | web |
| Jamming and wedging in peg-in-hole | new | 1 |  | RB-07: **ext** 327 | everything: nothing | robo |
| Haptic (force-feedback) teleoperation | new | 1 |  | RB-08: **ext** 335 | everything: nothing | web |
