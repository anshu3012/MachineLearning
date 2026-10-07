# vis ledger: index check of the robotics plan

Verdicts: taught (cited Note lists the concept), mentioned-only (treated as add), add, out-of-scope, index-noise. "app:" = application area outside robotics; "cv-special" = specialised computer-vision method beyond beginner robotics depth; "ml-zoo" = ML model variant no robotics Note uses. Add keys point to vis_adds.json.

## Barfoot, State Estimation for Robotics (index of the free 1st ed. PDF, plus the "(2ed new)" sections of the free 2nd ed. contents)

Source: Index of Barfoot, State Estimation for Robotics, 1st ed. (2017), official free PDF asrl.utias.utoronto.ca/~tdb/bib/barfoot_ser17.pdf, book pp. 375-378. The 2nd ed. free PDF (barfoot_ser24.pdf) has no index; its "(2ed new)" table-of-contents sections are appended with source "2ed-ToC" and 2nd-ed page numbers.

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| adaptive estimation | 166 | add | `kf-noise-tuning`: Choosing and estimating the noise covariances Q and R (robotics; RO-02 (section in 80) or RO-22) |
| adjoint | 226, 227 | taught | RB 275 (adjoint map) |
| affine transformation | 203 | taught | MA-053 §7.3 (affine transformation, G-178) |
| algebra | 217 | add | `lie-groups`: Matrix Lie groups SO(3)/SE(3) for estimation (maths; MA 05-linear-algebra (new Note after the planned axis-angle Note); used by RO 87, RO 101, RO 235) |
| Apianus, Petrus | xv | index-noise | person (historical figure) |
| arrowhead matrix | 345, 346 | taught | RO 235 (sparsity and Schur complement in bundle adjustment) |
| axiom of total probability | 9 | taught | MA-020 (a PDF integrates to 1) |
| BA [see bundle adjustment] |  | index-noise | cross-reference to bundle adjustment |
| Baker, Henry Frederick | 231 | index-noise | person |
| Baker-Campbell-Hausdorff | 231, 232, 234, 237, 247, 248, 274, 281, 326, 331, 360, 393 | out-of-scope | derivation identity for compounding Lie-algebra perturbations; beginner pose updates use the first-order form (see add lie-groups) |
| Bayes filter | xv, 3, 68, 91, 97–103, 107, 115, 116, 127, 142 | taught | RO 78 |
| Bayes’ rule | 3, 10, 33, 40, 50, 94, 98 | taught | MA-018 |
| Bayes, Thomas | 11 | index-noise | person |
| Bayesian | 9 | taught | MA-018 (Bayesian view: prior to posterior) |
| Bayesian inference | 11, 24, 39, 44, 46, 68–70, 91, 92, 135, 137, 143, 146 | taught | MA-018; RO 78 |
| BCH [see Baker-Campbell-Hausdorff] |  | index-noise | cross-reference |
| belief function | 97 | taught | RO 77 (belief) |
| Bernoulli numbers | 232 | out-of-scope | series coefficients used inside the book's SO(3) Jacobian derivation (proof technique) |
| Bernoulli, Jakob | 232, 243 | index-noise | person |
| Bessel’s correction | 12 | taught | MA-006 |
| Bessel, Friedrich Wilhelm | 12 | index-noise | person |
| best linear unbiased estimate | 70 | out-of-scope | optimality property proved for the Kalman filter (proof technique); the filter itself is RO 80 |
| biased | 103, 139 | taught | MA-071 (biased MLE of variance) |
| BLUE [see best linear unbiased estimate] |  | index-noise | cross-reference |
| bundle adjustment | 337, 348, 351, 352, 354, 355 | taught | RO 235 |
| camera | 199 | taught | RO 88 |
| Campbell, John Edward | 231 | index-noise | person |
| Cauchy cost function | 164 | taught | RO 235 (robust cost functions: Huber, Cauchy) |
| Cauchy product | 243 | out-of-scope | series-product identity used in a derivation (proof technique) |
| Cauchy, Baron Augustin-Louis | 243 | index-noise | person |
| causal | 58 | add | `rts-smoother`: Batch estimation and smoothing (robotics; RO-22 (new Note after 257)). causal = filter uses only past data, smoother uses all |
| Cayley-Hamilton theorem | 49 | out-of-scope | proof tool behind the rank test (proof technique); the rank test itself is listed under add observability-rank-test |
| Cayley-Rodrigues parameters | 182 | out-of-scope | rotation parametrisation not used by robot software or the plan (Euler angles, quaternions, axis-angle cover it); book-specific |
| Cholesky decomposition | 52–55, 87, 90, 110, 111, 119, 120, 124, 129, 276, 289, 334, 335, 345, 347, 354, 355, 365 | taught | new MA: Cholesky factor (robotics.md §4) |
| Cholesky smoother | 53 | add | `rts-smoother`: Batch estimation and smoothing (robotics; RO-22 (new Note after 257)) |
| Cholesky, André-Louis | 52 | index-noise | person |
| consistent | 71, 152 | add | `estimator-consistency`: Is the filter honest? innovation and its covariance, bias, consistency, NEES and NIS tests (robotics; RO-02 (section in 81) or RO-22) |
| continuous time | xvi, 4, 9, 32, 33, 37, 74, 88, 91, 96, 143, 147, 320, 321, 357, 358, 362, 363, 365–368 | taught | new MA: State-space models (continuous vs discrete time) |
| covariance estimation | 166 | add | `kf-noise-tuning`: Choosing and estimating the noise covariances Q and R (robotics; RO-02 (section in 80) or RO-22) |
| covariance matrix | 12 | taught | MA-009; ML-047 (covariance matrix) |
| Cramér, Harold | 14 | index-noise | person |
| Cramér-Rao lower bound | 14, 15, 31, 32, 70, 72, 118 | out-of-scope | estimation-theory lower bound taught in graduate estimation courses, not in robotics or control courses at beginner depth |
| CRLB [see Cramér-Rao lower bound] |  | index-noise | cross-reference |
| cross product | 175, 176 | taught | new MA: Cross product and skew-symmetric matrix |
| cubic Hermite polynomial | 86 | taught | RO 201 (cubic polynomials from boundary conditions) |
| curvature | 196 | taught | RO 67; RO 121 (curvature) |
| DARCES [see data-aligned rigidity-constrained exhaustive search] |  | index-noise | cross-reference |
| data association | 151, 159 | taught | RO 178; RO 259 |
| data-aligned rigidity-constrained exhaustive search | 161 | out-of-scope | named research algorithm for point-cloud registration (research-only) |
| Dirac, Paul Adrien Maurice | 33 | index-noise | person |
| directional derivative | 247, 393 | taught | MA-062 (directional derivative) |
| discrete time | 28, 32, 37, 51, 58, 74, 80, 87, 88, 96, 97, 127, 143, 147, 149, 277, 319–322, 325, 357, 363, 365 | taught | new MA: State-space models (discrete-time models by zero-order hold) |
| disparity | 208 | taught | RO 90 |
| dot product | 175, 177 | taught | MA-050 |
| early estimation milestones | 3 | out-of-scope | history |
| EKF [see extended Kalman filter] |  | index-noise | cross-reference |
| epipolar constraint | 203 | taught | RO 232 |
| epipolar line | 203 | taught | RO 232 |
| essential matrix (of computer vision) | 201 | taught | RO 232 |
| estimate | 38 | taught | MA-034 (estimate of a parameter) |
| estimation [see state estimation] |  | index-noise | cross-reference |
| Euler parameters [see unit-length quaternions] |  | index-noise | cross-reference |
| Euler’s rotation theorem | 180, 216 | taught | new MA: Axis-angle, exponential and log maps of rotations (any rotation is one turn about one axis) |
| Euler, Leonhard | 178 | index-noise | person |
| exponential map | 219 | taught | new MA: Axis-angle, exponential and log maps of rotations |
| extended Kalman filter | 70, 91, 100, 101, 103, 104, 106, 107, 109, 115, 118, 121, 122, 124–127, 134, 142, 143, 149, 297, 319, 321–324 | taught | RO 81 |
| exteroceptive | 3 | taught | RO 143 |
| extrinsic sensor parameters | 199 | taught | RO 88; RO 93 |
| factor graph | 355 | taught | RO 263 |
| Faulhaber’s formula | 243 | out-of-scope | series identity used in a derivation (proof technique) |
| Faulhaber, Johann | 243 | index-noise | person |
| filter | 59 | taught | RO 78 |
| Fisher, Sir Ronald Aylmer | 15 | index-noise | person |
| fixed-internal smoother | 43, 51 | add | `rts-smoother`: Batch estimation and smoothing (robotics; RO-22 (new Note after 257)) |
| focal length | 200 | taught | RO 88 (intrinsics) |
| Frenet, Jean Frédéric | 196 | index-noise | person |
| Frenet-Serret frame | 196, 198, 212 | taught | RO 121 (Frenet path frame, 2D) |
| frequentist | 9 | taught | MA-036 (frequentist reading of probability) |
| Frobenius norm | 279, 291 | taught | MA-059 |
| frontal projection model | 199 | out-of-scope | book's drawing convention for the pinhole model (image plane in front of the lens); RO 88 teaches the pinhole model |
| fundamental matrix (of computer vision) | 203 | taught | RO 232 |
| fundamental matrix (of control theory) | 145, 264 | taught | new MA: Matrix exponential and logarithm (e^(At) is the transition matrix of x' = Ax) |
| Gauss, Carl Friedrich | 2, 3 | index-noise | person |
| Gauss-Newton optimization | 129–134, 138, 139, 142, 249, 250, 254, 282, 283, 318, 319, 326–329, 333, 342, 343, 345 | taught | new MA: Nonlinear least squares (Gauss-Newton) |
| Gaussian estimator | 50, 63, 107 | taught | RO 80 |
| Gaussian filter | 115 | taught | RO 80; RO 81 (Gaussian filters) |
| Gaussian inference | 19 | add | `gaussian-conditioning`: Marginal and conditional of a joint Gaussian (maths; MA 08-likelihood (with the planned linear-transforms Note)) |
| Gaussian noise | 1, 2, 70, 88, 92, 100, 101, 151, 152, 155, 321, 339 | taught | MA-072 (Gaussian noise model) |
| Gaussian probability density function | 9, 13–16, 18–20, 22, 24, 26, 28–31, 33, 60, 63, 93, 99–102, 104, 105, 107–113, 115, 119, 120, 124, 126, 136, 146, 268, 288, 330 | taught | MA-024; MA-073 (multivariate normal) |
| Gaussian process | xvi, 4, 9, 32, 33, 74–77, 81, 85, 87, 143, 145–148, 357, 358, 363, 366 | taught | new ML: Gaussian processes (robotics.md §4); RO 200 |
| Gaussian random variable | 9, 16, 20, 24, 37, 266, 267, 270 | taught | MA-024 |
| Geman-McClure cost function | 164 | out-of-scope | one more robust loss beyond the Huber and Cauchy losses that RO 235 lists (variant) |
| generalized mass matrix | 318 | taught | RB 281 (mass matrix) |
| generalized velocity | 258 | taught | RB 275 (twist) |
| Gibbs vector | 182 | out-of-scope | same rotation parametrisation as Cayley-Rodrigues; book-specific |
| Gibbs, Josiah Willard | 182 | index-noise | person |
| global positioning system | 4, 159–161 | taught | RO 85 |
| GP [see Gaussian process] |  | index-noise | cross-reference |
| GPS [see global positioning system] |  | index-noise | cross-reference |
| group | 216 | add | `lie-groups`: Matrix Lie groups SO(3)/SE(3) for estimation (maths; MA 05-linear-algebra (new Note after the planned axis-angle Note); used by RO 87, RO 101, RO 235) |
| Hamilton, Sir William Rowan | 181 | index-noise | person |
| Hausdorff, Felix | 231 | index-noise | person |
| Heaviside step function | 79 | taught | DL-004 (step function) |
| Heaviside, Oliver | 182 | index-noise | person |
| Hermite basis function | 87 | taught | RO 201 |
| Hermite, Charles | 86 | index-noise | person |
| homogeneous coordinates | 193, 246, 285 | taught | RO 88; new MA: Projective homogeneous coordinates |
| homography matrix | 205 | taught | RO 229 |
| ICP [see iterative closest point] |  | index-noise | cross-reference |
| identity matrix | 175 | taught | MA-053; ML-053 |
| IEKF [see iterated extended Kalman filter] |  | index-noise | cross-reference |
| improper rotation | 216 | add | `rotation-matrix-properties`: Rotation representations (maths; MA 05-linear-algebra (section in the planned 3D rotations Note)) |
| IMU [see inertial measurement unit] |  | index-noise | cross-reference |
| inconsistent | 103 | add | `estimator-consistency`: Is the filter honest? innovation and its covariance, bias, consistency, NEES and NIS tests (robotics; RO-02 (section in 81) or RO-22) |
| inertial measurement unit | 209, 211, 213 | taught | RO 83 |
| information form | 56, 57, 67 | taught | RO 257; new MA: Canonical (information) form of a Gaussian |
| information matrix | 53 | taught | RO 257 |
| information vector | 50 | taught | RO 257 |
| injection | 268 | out-of-scope | set-theory word used in the book's proof about the exponential map (proof technique) |
| injective | 20 | out-of-scope | set-theory condition in a proof about transforming densities (proof technique); the change of variables itself is MA-063 §Extra |
| inner product [see dot product] |  | index-noise | cross-reference |
| interoceptive | 3 | taught | RO 142 (proprioceptive = interoceptive sensing) |
| interpolation matrix | 351 | out-of-scope | matrix of the book's continuous-time GP trajectory method (research-only) |
| intrinsic parameter matrix | 202 | taught | RO 88 |
| inverse covariance form [see information form] |  | index-noise | cross-reference |
| inverse-Wishart distribution | 166 | out-of-scope | multivariate conjugate prior used by a research-level adaptive estimator; beyond beginner depth |
| IRLS [see iterated reweighted least squares] |  | index-noise | cross-reference |
| ISPKF [see iterated sigmapoint Kalman filter] |  | index-noise | cross-reference |
| Isserlis’ theorem | 16, 288 | out-of-scope | Gaussian moment identity used in derivations (proof technique) |
| Isserlis, Leon | 16 | index-noise | person |
| Itō calculus | 77 | out-of-scope | stochastic calculus, a graduate maths field; the beginner part is in add white-noise-psd |
| Itō, Kiyoshi | 77 | index-noise | person |
| iterated extended Kalman filter | 105–107, 109, 124–127, 136, 137, 142, 146, 148 | add | `iterated-ekf`: Iterated EKF (robotics; RO-22 (section in 258)) |
| iterated sigmapoint Kalman filter | 123, 125–127 | out-of-scope | book's own iterated sigma-point variant (research-only) |
| iterative closest point | 297, 298 | taught | RO 92 |
| iteratively reweighted least squares | 165 | taught | new MA short section: Levenberg-Marquardt and robust losses (IRLS) |
| Jacobi’s formula | 222 | out-of-scope | determinant identity used in a proof (proof technique) |
| Jacobi, Gustav Jacob | 218 | index-noise | person |
| Jacobian | 224, 233, 234, 248 | taught | MA-063 |
| John Harrison | 2 | index-noise | person |
| joint probability density function | 10 | taught | MA-014 |
| Kálmán, Rudolf Emil | 2 | index-noise | person |
| Kōwa, Seki | 232 | index-noise | person |
| Kalman filter | xv, 2, 3, 37, 58, 63, 68–70, 72, 153, 154, 159 | taught | RO 80 |
| Kalman gain | 67 | taught | RO 80 |
| kernel matrix | 75, 80 | add | `gp-kernel-matrix`: Kernel (covariance) function and kernel matrix of a Gaussian process (maths; the planned new ML Note "Gaussian processes") |
| KF [see Kalman filter] |  | index-noise | cross-reference |
| kinematics | 184, 197, 198, 255, 256, 258, 259, 261–263, 265, 266, 274, 320, 321, 323 | taught | RO 69; RO 84 |
| kurtosis | 12, 115 | taught | MA-028 |
| law of large numbers | 108 | taught | MA-021 (law of large numbers, G-1052) |
| Levenberg-Marquardt | 132, 254 | taught | RO 235 |
| LG [see linear-Gaussian] |  | index-noise | cross-reference |
| Lie algebra | 217 | add | `lie-groups`: Matrix Lie groups SO(3)/SE(3) for estimation (maths; MA 05-linear-algebra (new Note after the planned axis-angle Note); used by RO 87, RO 101, RO 235) |
| Lie derivative | 248 | out-of-scope | differential-geometry tool for nonlinear observability analysis (graduate) |
| Lie group [see matrix Lie group] |  | index-noise | cross-reference |
| Lie product formula | 232 | out-of-scope | identity used in a derivation (proof technique) |
| Lie, Marius Sophus | 215 | index-noise | person |
| lifted form | 39, 44, 78 | add | `rts-smoother`: Batch estimation and smoothing (robotics; RO-22 (new Note after 257)). lifted form = whole trajectory stacked into one batch problem |
| line search | 132, 254 | mentioned-only | `line-search`: Line search and step-size rules (backtracking) in optimisation (maths; MA 07-optimisation (section in the planned nonlinear least squares Note)). MA-064 names it in one parenthesis only |
| linear time-invariant | 83, 359 | taught | new MA: State-space models (x' = Ax + Bu) |
| linear time-varying | 77, 81, 144, 264, 266 | taught | new MA: State-space models; RO 206 (time-varying LQR) |
| linear, time-varying | 37 | taught | RO 206 (time-varying LQR on a time-varying linear model) |
| linear-Gaussian | 38, 39, 43, 44, 46, 59, 61, 64, 73, 98, 159 | taught | RO 80 |
| Lovelace, Ada | 232 | index-noise | person |
| LTI [see linear time-invariant] |  | index-noise | cross-reference |
| LTV [see linear time-varying] |  | index-noise | cross-reference |
| M-estimation | 163 | taught | RO 235 (robust cost functions, M-estimators) |
| Möbius, Augustus Ferdinand | 193 | index-noise | person |
| Mahalanobis | 282 | taught | new MA: Mahalanobis distance |
| Mahalanobis distance | 28, 41 | taught | new MA: Mahalanobis distance |
| Mahalanobis, Prasanta Chandra | 28 | index-noise | person |
| many-to-one | 220 | out-of-scope | set-theory word used in the book's proof about the exponential map (proof technique) |
| MAP [see maximum a posteriori] |  | index-noise | cross-reference |
| marginalization | 11 | taught | MA-014 |
| Markov property | 64, 97 | taught | new MA: Markov chains |
| matrix inversion lemma [see Sherman-Morrison-Woodbury] |  | index-noise | cross-reference |
| matrix Lie group | 215, 216 | add | `lie-groups`: Matrix Lie groups SO(3)/SE(3) for estimation (maths; MA 05-linear-algebra (new Note after the planned axis-angle Note); used by RO 87, RO 101, RO 235) |
| maximum a posteriori | 39, 40, 63, 64, 69, 88, 89, 91, 94, 95, 106, 107, 125–128, 137, 138, 148, 151, 321, 322, 325, 326, 352, 364, 368 | taught | MA-072 (MAP estimate, G-1189); RO 260 |
| maximum likelihood | 137, 138, 149, 151, 330, 331, 339, 342, 351 | taught | MA-070 |
| mean | 11, 15 | taught | MA-005; MA-012 |
| mean rotation | 269 | out-of-scope | averaging rotations needs Lie-group machinery beyond beginner depth (used in research-level filters on SO(3)) |
| ML [see maximum likelihood] |  | index-noise | cross-reference |
| Monte Carlo | 100, 108, 279, 290 | taught | new MA: Monte Carlo estimation |
| Moore-Penrose pseudoinverse [see pseudoinverse] |  | index-noise | cross-reference |
| mutual information | 14, 30 | taught | new MA: Mutual information |
| NASA [see National Aeronautics and Space Administration] |  | index-noise | cross-reference |
| National Aeronautics and Space Administration | 3, 100 | index-noise | organisation name |
| Newton’s method | 129 | taught | MA-064 |
| NLNG [see nonlinear, non-Gaussian] |  | index-noise | cross-reference |
| non-commutative group | 182, 188, 215 | add | `rotation-matrix-properties`: Rotation representations (maths; MA 05-linear-algebra (section in the planned 3D rotations Note)). rotations do not commute |
| nonlinear, non-Gaussian | 91, 96, 97 | out-of-scope | book-specific category label (nonlinear, non-Gaussian problems); the particle filter itself is RO 82 |
| normalized image coordinates | 200 | add | `pinhole-geometry-terms`: Pinhole geometry terms (vision; RO-03 (section in 88)). normalised image coordinates |
| normalized product | 13, 22 | taught | new MA: Product of two Gaussians |
| observability | 2, 49, 156 | taught | RO 80 |
| observability matrix | 49 | add | `observability-rank-test`: Observability matrix and rank test (dual of controllability) (control; RO-15 (section in 204)) |
| onto | 220 | out-of-scope | set-theory word used in the book's proof about the exponential map (proof technique) |
| optical axis | 199 | add | `pinhole-geometry-terms`: Pinhole geometry terms (vision; RO-03 (section in 88)). optical axis |
| outlier | 151, 161, 162 | taught | ML-040; RO 235 |
| particle filter | 91, 115–118 | taught | RO 82 |
| PDF [see probability density function] |  | index-noise | cross-reference |
| point-cloud alignment | 297 | taught | RO 92 |
| point-clouds | 297 | taught | RO 91 |
| Poisson’s equation | 186 | taught | RO 84 (Poisson's kinematic equation = integrating angular velocity into orientation) |
| Poisson, Siméon Denis | 186 | index-noise | person |
| pose-graph relaxation | 329 | taught | RO 101 |
| poses | 173, 192, 216, 218, 222, 234, 239, 245, 251, 258, 265, 270, 273, 280 | taught | RO 64; RO 65 |
| posterior | 11, 38 | taught | MA-018 |
| power spectral density martrix | 77 | add | `white-noise-psd`: White noise and its power spectral density; random walks; turning continuous noise intensity into a discrete Q (IMU noise density) (robotics; RO-03 (section in 83)) |
| power spectral density matrix | 33 | add | `white-noise-psd`: White noise and its power spectral density; random walks; turning continuous noise intensity into a discrete Q (IMU noise density) (robotics; RO-03 (section in 83)) |
| prior | 11, 38 | taught | MA-018 |
| probability | 9 | taught | MA-011 |
| probability density function | 9–12, 14–16, 19, 22–26, 28–30, 34, 95, 97–99, 101, 104, 107–113, 115, 116, 148, 268, 269, 276, 282 | taught | MA-022 |
| probability distributions | 10 | taught | MA-020 |
| proper rotation | 216 | add | `rotation-matrix-properties`: Rotation representations (maths; MA 05-linear-algebra (section in the planned 3D rotations Note)) |
| pseudoinverse | 43 | taught | MA-060 (Moore-Penrose pseudo-inverse, G-1262) |
| quaternion | 298 | taught | new MA: 3D rotations: Euler angles and quaternions |
| RAE [see range-azimuth-elevation] |  | index-noise | cross-reference |
| random sample consensus | 162, 168, 169, 297, 305 | taught | RO 229 |
| random variable | 9 | taught | MA-020 |
| range-azimuth-elevation | 208, 209 | taught | RO 91 |
| RANSAC [see random sample consensus] |  | index-noise | cross-reference |
| Rao, Calyampudi Radhakrishna | 14 | index-noise | person |
| Rauch, Herbert E. | 55 | index-noise | person |
| Rauch-Tung-Striebel smoother | 3, 51, 55, 58 | add | `rts-smoother`: Batch estimation and smoothing (robotics; RO-22 (new Note after 257)) |
| realization | 12, 14, 38 | taught | MA-020 (a realisation = one drawn value) |
| reference frame | 174 | taught | RO 65 |
| robust cost | 164 | taught | RO 235 |
| rotary reflection | 216 | out-of-scope | classification of orthogonal maps (geometry); robots use only proper rotations |
| rotation matrix [see also rotations] | 176 | taught | RO 65 |
| rotations | 173, 215, 220, 232, 237, 240, 242, 247, 255, 261, 267 | taught | new MA: 3D rotations: Euler angles and quaternions; RO 65 |
| RTS [see Rauch-Tung-Striebel] |  | index-noise | cross-reference |
| sample covariance | 12 | taught | MA-009 |
| sample mean | 12 | taught | MA-005 |
| Schmidt, Stanley F. | 100 | index-noise | person |
| Schur complement | 19, 65, 345, 346, 348, 354, 355, 365, 366 | taught | new MA: Schur complement |
| Schur, Issai | 19 | index-noise | person |
| SDE [see stochastic differential equation] |  | index-noise | cross-reference |
| Serret, Joseph Alfred | 196 | index-noise | person |
| Shannon information | 14, 28, 29, 33 | taught | ML-091 (entropy) |
| Shannon, Claude Elwood | 14 | index-noise | person |
| Sherman-Morrison-Woodbury | 23, 45, 55–57, 75, 123, 136, 137, 147 | taught | new MA: Woodbury identity |
| sigmapoint | 110, 115, 120 | taught | RO 256 |
| sigmapoint Kalman filter | 91, 118, 121, 122, 124–127 | taught | RO 256 |
| sigmapoint transformation | 110, 113, 114, 119, 120, 148, 272, 276, 279, 285, 288 | taught | RO 256 (unscented transform) |
| simultaneous localization and mapping | 342, 352, 355, 363–365 | taught | RO 100 |
| simultaneous trajectory estimation and mapping | 362 | out-of-scope | the author's continuous-time GP trajectory method (research-only) |
| singular-value decomposition | 305 | taught | MA-057; MA-058 |
| skewness | 12, 115 | taught | MA-026 |
| SLAM [see simultaneous localization and mapping] |  | index-noise | cross-reference |
| sliding-window filter | 142 | taught | RO 263 |
| smoother | 59 | add | `rts-smoother`: Batch estimation and smoothing (robotics; RO-22 (new Note after 257)) |
| SMW [see Sherman-Morrison-Woodbury] |  | index-noise | cross-reference |
| SP [see sigmapoint] |  | index-noise | cross-reference |
| sparse bundle adjustment | 345 | taught | RO 235 |
| special Euclidean group, see also poses | 216 | taught | new MA: Rigid-body transforms and homogeneous coordinates (SE(2)/SE(3)) |
| special orthogonal group, see also rotations | 215 | taught | new MA: Rigid-body transforms and homogeneous coordinates (SO(3) rotations) |
| SPKF [see sigmapoint Kalman filter] |  | index-noise | cross-reference |
| state | 1, 38 | taught | RO 63 |
| state estimation | 1, 4, 38 | taught | RO 63; RO 78 |
| state transition matrix | 264 | taught | new MA: Matrix exponential and logarithm |
| statistical moments | 11 | taught | MA-028 (moments) |
| statistically independent | 10, 12, 20, 30 | taught | MA-016 |
| STEAM [see simultaneous trajectory estimation and mapping] |  | index-noise | cross-reference |
| stereo baseline | 206 | taught | RO 90 |
| stereo camera | 92 | taught | RO 90 |
| stochastic differential equation | 144, 266, 358, 360, 366, 368 | out-of-scope | stochastic calculus (graduate); the beginner part is in add white-noise-psd |
| Striebel, Charlotte T. | 55 | index-noise | person |
| surjective-only | 220 | out-of-scope | set-theory word used in the book's proof about the exponential map (proof technique) |
| SWF [see sliding-window filter] |  | index-noise | cross-reference |
| Sylvester’s determinant theorem | 30 | out-of-scope | determinant identity used in a proof (proof technique) |
| Sylvester, James Joseph | 30 | index-noise | person |
| tangent space | 218 | add | `lie-groups`: Matrix Lie groups SO(3)/SE(3) for estimation (maths; MA 05-linear-algebra (new Note after the planned axis-angle Note); used by RO 87, RO 101, RO 235) |
| taxonomy of filtering methods | 127 | index-noise | pointer to the book's comparison table of filters (chapter pointer) |
| torsion | 196 | out-of-scope | 3D curve geometry (differential geometry); the plan's path frame is 2D (RO 121) |
| transformation matrix [see also poses] | 193 | taught | new MA: Rigid-body transforms and homogeneous coordinates |
| transition function | 77 | taught | new MA: Matrix exponential and logarithm (transition matrix) |
| transition matrix | 38, 78 | taught | new MA: State-space models (x(k+1) = A x(k) + B u(k)) |
| Tung, Frank F. | 55 | index-noise | person |
| UKF [see sigmapoint Kalman filter] |  | index-noise | cross-reference |
| unbiased | 14, 71, 152 | taught | MA-071 |
| uncertainty ellipsoid | 29 | taught | MA-073 (Gaussian contour ellipses) |
| uncorrelated | 12, 20 | taught | MA-009 |
| unimodular | 238 | out-of-scope | determinant property used in derivations (proof technique) |
| unit-length quaternions | 180 | taught | new MA: 3D rotations: Euler angles and quaternions |
| unscented Kalman filter [see sigmapoint Kalman filter] |  | index-noise | cross-reference |
| variance | 15 | taught | MA-012 |
| vector | 174 | taught | MA-048 |
| vectrix | 174 | out-of-scope | book-specific notation (Hughes' vectrix) |
| white noise | 33 | add | `white-noise-psd`: White noise and its power spectral density; random walks; turning continuous noise intensity into a discrete Q (IMU noise density) (robotics; RO-03 (section in 83)) |
| Quantifying the difference between PDFs (KL divergence) (2nd-ed contents) | 13 | taught | new MA: KL divergence |
| Random sampling (2nd-ed contents) | 14 | taught | new MA: Drawing samples from distributions |
| Information form of a Gaussian (2nd-ed contents) | 20 | taught | RO 257 |
| Marginals of a joint Gaussian (2nd-ed contents) | 20 | add | `gaussian-conditioning`: Marginal and conditional of a joint Gaussian (maths; MA 08-likelihood (with the planned linear-transforms Note)) |
| Chi-squared distribution and Mahalanobis distance (2nd-ed contents) | 28 | taught | MA-045 (chi-square distribution); new MA: Mahalanobis distance (gating); RO 178 |
| Quantifying the difference between Gaussians (2nd-ed contents) | 31 | taught | new MA: KL divergence |
| Randomly sampling a Gaussian (2nd-ed contents) | 31 | taught | new MA: Cholesky factor (matrix square root); new MA: Drawing samples from distributions |
| Stein's lemma (2nd-ed contents) | 34, 206, 520 | out-of-scope | Gaussian expectation identity used in research-level variational estimation (proof technique) |
| Posterior covariance in the Cholesky smoother (2nd-ed contents) | 61 | add | `rts-smoother`: Batch estimation and smoothing (robotics; RO-22 (new Note after 257)) |
| Recursive continuous-time smoothing and filtering (2nd-ed contents) | 96 | out-of-scope | continuous-time GP smoothing (research-only) |
| Turning batch estimation into a smoother/filter (2nd-ed contents) | 96 | add | `rts-smoother`: Batch estimation and smoothing (robotics; RO-22 (new Note after 257)) |
| Kalman-Bucy filter (2nd-ed contents) | 97 | out-of-scope | continuous-time filter; robots run discrete-time filters, which the plan teaches (RO 80) |
| Estimator performance (2nd-ed contents) | 172 | add | `estimator-consistency`: Is the filter honest? innovation and its covariance, bias, consistency, NEES and NIS tests (robotics; RO-02 (section in 81) or RO-22) |
| Unbiased and consistent (2nd-ed contents) | 172 | add | `estimator-consistency`: Is the filter honest? innovation and its covariance, bias, consistency, NEES and NIS tests (robotics; RO-02 (section in 81) or RO-22) |
| NEES and NIS (2nd-ed contents) | 174 | add | `estimator-consistency`: Is the filter honest? innovation and its covariance, bias, consistency, NEES and NIS tests (robotics; RO-02 (section in 81) or RO-22) |
| Covariance estimation (2nd-ed contents) | 191 | add | `kf-noise-tuning`: Choosing and estimating the noise covariances Q and R (robotics; RO-02 (section in 80) or RO-22) |
| Supervised covariance estimation (2nd-ed contents) | 192 | add | `kf-noise-tuning`: Choosing and estimating the noise covariances Q and R (robotics; RO-02 (section in 80) or RO-22) |
| Adaptive covariance estimation (2nd-ed contents) | 193 | add | `kf-noise-tuning`: Choosing and estimating the noise covariances Q and R (robotics; RO-02 (section in 80) or RO-22) |
| Variational inference (2nd-ed contents) | 199 | add | `variational-inference`: Variational inference and the evidence lower bound (ELBO) (maths; DL new chapter "Generative models" (section in the planned VAE Note)) |
| Gaussian variational inference (2nd-ed contents) | 201 | out-of-scope | research-level estimator (Barfoot's exactly sparse Gaussian variational inference) |
| Natural gradient descent (2nd-ed contents) | 205 | taught | RL 38 (natural gradient and Fisher information) |
| Exact sparsity (factored joint likelihood) (2nd-ed contents) | 207 | out-of-scope | research-level property of the book's variational estimator |
| Optimization on Riemannian manifolds (2nd-ed contents) | 318 | add | `lie-groups`: Matrix Lie groups SO(3)/SE(3) for estimation (maths; MA 05-linear-algebra (new Note after the planned axis-angle Note); used by RO 87, RO 101, RO 235). optimise a rotation by small rotation-vector updates |
| Inverse pose (2nd-ed contents) | 352 | add | `pose-inverse-composition`: Inverse and composition of poses with homogeneous matrices (maths; MA 05-linear-algebra (section in the planned rigid-body Note)) |
| Compounding and differencing correlated poses (2nd-ed contents) | 353 | add | `lie-groups`: Matrix Lie groups SO(3)/SE(3) for estimation (maths; MA 05-linear-algebra (new Note after the planned axis-angle Note); used by RO 87, RO 101, RO 235). uncertainty of composed poses |
| Symmetry, invariance, and equivariance (2nd-ed contents) | 366 | out-of-scope | research-level theory of invariant filters |
| Inertial navigation (2nd-ed contents) | 418 | taught | RO 84 |
| Extended poses (2nd-ed contents) | 419 | out-of-scope | research-level state representation for the invariant EKF (SE_2(3)) |
| Matrix primer (2nd-ed contents) | 475 | taught | MA-047 to MA-060 (linear algebra chapter) |
| Vectorization and Kronecker product (2nd-ed contents) | 493 | out-of-scope | matrix-calculus derivation tool (proof technique) |
| Matrix calculus (2nd-ed contents) | 496 | taught | MA-063 |
| Rotation and pose extras (SO(3)/SE(3) Jacobian identities, decompositions) (2nd-ed contents) | 501 | out-of-scope | derivation identities for SO(3)/SE(3) Jacobians (proof technique) |
| Fisher information matrix for a multivariate Gaussian (2nd-ed contents) | 515 | taught | RL 38 (Fisher information) |
| Temporally discretizing motion models (2nd-ed contents) | 522 | taught | new MA: State-space models (discretisation); add white-noise-psd for the noise part |
| Invariant EKF (2nd-ed contents) | 525 | out-of-scope | research-level filter (invariant EKF, 2017 onward) |

## Prince, Computer Vision: Models, Learning, and Inference (free PDF, CUP 2012)

Source: Index of Prince, Computer Vision: Models, Learning, and Inference (CUP 2012), official free PDF linked from computervisionmodels.com (github.com/udlbook/cvbook/raw/main/book.pdf), book pp. 655-665.

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| 3D body model | 496–497 | taught | RB 317 (body models, SMPL) |
| 3D morphable model | 494–496, 500 | out-of-scope | app: face and body modelling for graphics (different field) |
| 3D reconstruction | 359, 369–370, 376–377, 453 | taught | RO 233 (triangulation); RO 235 (structure from motion) |
| 3D reconstruction, from structured light | 378–380 | taught | RO 90 (structured light depth cameras) |
| 3D reconstruction, pipeline | 447–449 | taught | RO 235 |
| 3D reconstruction, volumetric graph cuts | 450–452 | out-of-scope | cv-special: multi-view stereo by graph cuts, beyond beginner robotics depth |
| action recognition | 592–593, 595 | out-of-scope | app: video action recognition (different field) |
| activation | 172 | taught | DL-027 |
| active appearance model | 482–487, 499 | out-of-scope | app: face fitting (biometrics, different field) |
| active contour model | 463–468, 499 | out-of-scope | cv-special: snakes (active contours) for segmentation, not used by any robotics Note |
| active shape model | 462, 471–482, 499 | out-of-scope | app: face and organ shape fitting (different field) |
| active shape model, 3D | 482 | out-of-scope | app: face and organ shape fitting (different field) |
| adaboost [see also boosting] | 200, 202, 209 | taught | ML-109 |
| affine transformation | 393–394 | taught | MA-053 §7.3 |
| affine transformation, learning | 399–400 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)). fit an affine map to point matches by least squares |
| alignment of shapes | 472–473 | taught | RO 92 (point-set alignment by SVD / Procrustes) |
| alpha-beta swap | 316, 319 | out-of-scope | cv-special: graph-cut move-making algorithm (MRF energy minimisation) |
| alpha-expansion algorithm | 298–300, 316 | out-of-scope | cv-special: graph-cut move-making algorithm (MRF energy minimisation) |
| ancestral sampling | 232 | add | `bayes-networks`: Probabilistic graphical models (maths; MA 02-probability (new Note after MA-019)). ancestral sampling of a directed model |
| application |  | index-noise | heading for the book's list of application pointers |
| application, 3D reconstruction | 359, 447–453 | index-noise | application pointer; the method is judged under its own entry |
| application, action recognition | 592–593, 595 | index-noise | application pointer; the method is judged under its own entry |
| application, animation synthesis | 531–532 | index-noise | application pointer; the method is judged under its own entry |
| application, augmented reality tracking | 390, 416–417, 420 | index-noise | application pointer; the method is judged under its own entry |
| application, background subtraction | 94, 97, 305 | index-noise | application pointer; the method is judged under its own entry |
| application, body pose estimation | 143, 166, 207–208, 271–272 | index-noise | application pointer; the method is judged under its own entry |
| application, body tracking | 500 | index-noise | application pointer; the method is judged under its own entry |
| application, changing face pose | 137 | index-noise | application pointer; the method is judged under its own entry |
| application, contour tracking | 537, 565 | index-noise | application pointer; the method is judged under its own entry |
| application, denoising | 279, 282–284, 291, 300 | index-noise | application pointer; the method is judged under its own entry |
| application, depth from structured light | 378–380 | index-noise | application pointer; the method is judged under its own entry |
| application, face detection | 101, 133–134, 140, 202–203, 210 | index-noise | application pointer; the method is judged under its own entry |
| application, face recognition | 136, 503, 510–514, 517, 528–530, 533 | index-noise | application pointer; the method is judged under its own entry |
| application, face synthesis | 314–315 | index-noise | application pointer; the method is judged under its own entry |
| application, finding facial features | 271, 274 | index-noise | application pointer; the method is judged under its own entry |
| application, fitting 3D body model | 496–497 | index-noise | application pointer; the method is judged under its own entry |
| application, fitting 3D shape model | 494–496 | index-noise | application pointer; the method is judged under its own entry |
| application, gender classification | 171, 201, 209 | index-noise | application pointer; the method is judged under its own entry |
| application, gesture tracking | 243, 267 | index-noise | application pointer; the method is judged under its own entry |
| application, image retargeting | 308–309 | index-noise | application pointer; the method is judged under its own entry |
| application, interactive segmentation | 305–307, 317 | index-noise | application pointer; the method is judged under its own entry |
| application, multi-view reconstruction | 450–453 | index-noise | application pointer; the method is judged under its own entry |
| application, object recognition | 134–135, 140, 571–592 | index-noise | application pointer; the method is judged under its own entry |
| application, panorama | 417, 420 | index-noise | application pointer; the method is judged under its own entry |
| application, pedestrian detection | 202–203 | index-noise | application pointer; the method is judged under its own entry |
| application, pedestrian tracking | 563–564 | index-noise | application pointer; the method is judged under its own entry |
| application, Photo-tourism | 449–450 | index-noise | application pointer; the method is judged under its own entry |
| application, scene recognition | 571, 590 | index-noise | application pointer; the method is judged under its own entry |
| application, segmentation | 135–136, 272–273, 463–468 | index-noise | application pointer; the method is judged under its own entry |
| application, semantic segmentation | 203–205, 210 | index-noise | application pointer; the method is judged under its own entry |
| application, shape from silhouette | 380–383 | index-noise | application pointer; the method is judged under its own entry |
| application, sign language interpretation | 243, 246, 267 | index-noise | application pointer; the method is judged under its own entry |
| application, skin detection | 93–94, 97 | index-noise | application pointer; the method is judged under its own entry |
| application, SLAM | 564, 567 | index-noise | application pointer; the method is judged under its own entry |
| application, stereo vision | 267–270, 274, 307–308, 317 | index-noise | application pointer; the method is judged under its own entry |
| application, super-resolution | 310–311 | index-noise | application pointer; the method is judged under its own entry |
| application, surface layout recovery | 205–206 | index-noise | application pointer; the method is judged under its own entry |
| application, TensorTextures | 530–531 | index-noise | application pointer; the method is judged under its own entry |
| application, texture synthesis | 311–314, 317 | index-noise | application pointer; the method is judged under its own entry |
| application, tracking head position | 167 | index-noise | application pointer; the method is judged under its own entry |
| application, Video Google | 591–592 | index-noise | application pointer; the method is judged under its own entry |
| approximate inference | 231 | taught | RO 82 (sampling-based approximate inference) |
| AR Toolkit | 420 | index-noise | software product name |
| argmax function | 600 | index-noise | entry in the book's notation appendix (symbol) |
| argmin function | 600 | index-noise | entry in the book's notation appendix (symbol) |
| articulated models | 492–493 | taught | RO 69 (kinematic chains and trees) |
| articulated models, pictorial structures | 271 | out-of-scope | cv-special: part-based body model for 2000s pose detection, superseded by learned pose (RB 317) |
| asymmetric bilinear model | 518–524 | out-of-scope | app: face style/identity model (biometrics, different field) |
| augmented reality | 390, 416–417, 420 | out-of-scope | app: augmented reality graphics (different field); its pose step is PnP, RO 233 |
| augmenting paths algorithm | 286, 316 | out-of-scope | graph algorithm used only inside graph cuts (cv-special) |
| author-topic model | 582–585, 595 | out-of-scope | ml-zoo: text topic model, no robotics Note uses it |
| auto-calibration | 444 | out-of-scope | cv-special: self-calibration from uncalibrated views, beyond beginner depth; robots calibrate with targets (RO 89) |
| back propagation | 200 | taught | DL-015 |
| background subtraction | 94, 97, 305 | out-of-scope | app: fixed-camera surveillance (different field) |
| bag of words | 344, 573–576, 595 | taught | RO 236 |
| Baum-Welch algorithm | 263 | out-of-scope | learning HMM parameters by EM; the plan's HMMs use known models (RO 77-79) |
| Bayes’ Rule | 30 | taught | MA-018 |
| Bayesian approach to fitting | 50–51 | add | `bayesian-fitting`: Bayesian fitting (maths; MA 08-likelihood (new Note after MA-072)) |
| Bayesian belief propagation | 257–262, 275 | out-of-scope | message passing on loopy graphs; robot factor graphs are solved by least squares (RO 263) |
| Bayesian belief propagation, loopy | 266 | out-of-scope | message passing on loopy graphs; robot factor graphs are solved by least squares (RO 263) |
| Bayesian belief propagation, sum-product algorithm | 258–259 | add | `hmm-inference`: HMM inference (robotics; RO-02 (section after 79)). sum-product on a chain = forward-backward |
| Bayesian linear regression | 147–150 | add | `bayesian-fitting`: Bayesian fitting (maths; MA 08-likelihood (new Note after MA-072)) |
| Bayesian logistic regression | 176–180 | out-of-scope | ml-zoo: classifier variant no robotics Note uses |
| Bayesian model selection | 66, 511 | out-of-scope | ml-zoo: evidence-based model comparison, no robotics Note uses it |
| Bayesian network | 219–222 | add | `bayes-networks`: Probabilistic graphical models (maths; MA 02-probability (new Note after MA-019)) |
| Bayesian network, comparison to undirected | 225 | add | `bayes-networks`: Probabilistic graphical models (maths; MA 02-probability (new Note after MA-019)) |
| Bayesian network, learning | 234–235 | out-of-scope | ml-zoo: structure and parameter learning of Bayes nets, no robotics Note uses it |
| Bayesian network, sampling | 232 | add | `bayes-networks`: Probabilistic graphical models (maths; MA 02-probability (new Note after MA-019)) |
| Bayesian nonlinear regression | 153 | add | `bayesian-fitting`: Bayesian fitting (maths; MA 08-likelihood (new Note after MA-072)) |
| belief propagation | 257–262, 275 | out-of-scope | message passing on loopy graphs; robot factor graphs are solved by least squares (RO 263) |
| belief propagation, loopy | 266 | out-of-scope | message passing on loopy graphs; robot factor graphs are solved by least squares (RO 263) |
| belief propagation, sum-product algorithm | 258–259 | add | `hmm-inference`: HMM inference (robotics; RO-02 (section after 79)) |
| Bernoulli distribution | 35–37 | taught | MA-031 |
| Bernoulli distribution, conjugate prior | 42, 46 | add | `bayesian-fitting`: Bayesian fitting (maths; MA 08-likelihood (new Note after MA-072)) |
| Bernoulli distribution, relation to binomial | 45 | taught | MA-031 |
| beta distribution | 35, 37–38 | add | `bayesian-fitting`: Bayesian fitting (maths; MA 08-likelihood (new Note after MA-072)). beta as the conjugate prior of the Bernoulli |
| between-individual variation | 507 | out-of-scope | app: face recognition (biometrics) |
| BFGS | 608 | taught | MA-064 (BFGS) |
| bilateral filter | 353 | add | `nonlinear-image-filters`: Nonlinear image filters (vision; RO-18 (section in 227) or RO 90 depth-map cleanup) |
| bilinear model | 534 | out-of-scope | app: face style/identity model (biometrics) |
| bilinear model, asymmetric | 518–524 | out-of-scope | app: face style/identity model (biometrics) |
| bilinear model, symmetric | 524–528 | out-of-scope | app: face style/identity model (biometrics) |
| binary classification | 88–91, 171–196 | taught | ML-073; ML-078 (binary classification) |
| binomial distribution | 45 | taught | MA-031 |
| bivariate distribution | 69 | taught | MA-014; MA-073 |
| block diagonal matrix | 626 | taught | new MA: Schur complement (block-matrix algebra) |
| blurring | 328 | taught | DL-042 §4.2 (blur) |
| body pose estimation | 143, 166, 207–208, 271–272 | taught | RB 317; RB 337 (human pose from video) |
| body tracking | 500 | taught | RB 320 |
| boosting | 209 | taught | ML-113 |
| boosting, adaboost | 202 | taught | ML-109 |
| boosting, jointboost | 203 | out-of-scope | ml-zoo: boosting variant for face detection |
| boosting, logitboost | 193–194 | out-of-scope | ml-zoo: boosting variant |
| bottom-up approach | 461 | out-of-scope | book's taxonomy of segmentation strategies (book-specific) |
| branching logistic regression | 194–196 | out-of-scope | ml-zoo: classifier variant |
| Brownian motion | 548 | taught | RO 83 (bias random walk); add white-noise-psd for the continuous form |
| Broyden Fletcher Goldfarb Shanno | 608 | taught | MA-064 (BFGS) |
| bundle adjustment | 445–448, 453 | taught | RO 235 |
| calibration |  | taught | RO 89 |
| calibration, from 3D object | 368, 375–376 | taught | RO 89 (DLT) |
| calibration, from a plane | 405–406, 420 | taught | RO 89 (checkerboard calibration) |
| calibration target | 375, 405 | taught | RO 89 |
| calibration target, 3D | 368 | taught | RO 89 |
| calibration target, planar | 405 | taught | RO 89 |
| camera |  | taught | RO 88 |
| camera, geometry | 385 | taught | RO 88 |
| camera, orthographic | 387 | out-of-scope | camera model for very distant scenes; robot cameras use the pinhole model (RO 88) |
| camera, other camera models | 385 | taught | RO 89 (wide-angle and fisheye models) |
| camera, othographic | 455 | out-of-scope | camera model for very distant scenes; robot cameras use the pinhole model (RO 88) |
| camera, parameters | 365 | taught | RO 88 |
| camera, pinhole | 359–366 | taught | RO 88 |
| camera, pinhole, in Cartesian coordinates | 364–365 | taught | RO 88 |
| camera, pinhole, in homogeneous coordinates | 372–373 | taught | RO 88 |
| camera, projective | 359 | taught | RO 88 |
| camera, weak perspective | 387 | out-of-scope | camera model for very distant scenes; robot cameras use the pinhole model (RO 88) |
| camera calibration |  | taught | RO 89 |
| camera calibration, from 3D object | 368, 375–376 | taught | RO 89 |
| camera calibration, from a plane | 405–406, 420 | taught | RO 89 |
| Canny edge detector | 336–338, 464 | add | `edge-detection`: Edge detection (vision; RO-18 (section in 227)) |
| canonical correlation analysis | 519 | out-of-scope | ml-zoo: canonical correlation analysis, no robotics Note uses it |
| capacity | 285 | out-of-scope | edge capacity in a graph cut (cv-special) |
| cascade structured classifier | 203 | out-of-scope | app: Viola-Jones face detection (cv-special, superseded by RO 173-174) |
| categorical distribution | 35, 38 | taught | MA-031; MA-072 (categorical distribution) |
| categorical distribution, Bayesian fitting | 62–63 | add | `bayesian-fitting`: Bayesian fitting (maths; MA 08-likelihood (new Note after MA-072)) |
| categorical distribution, conjugate prior | 42, 46 | add | `bayesian-fitting`: Bayesian fitting (maths; MA 08-likelihood (new Note after MA-072)) |
| categorical distribution, fitting | 60–63 | taught | MA-072 (MLE for the categorical) |
| categorical distribution, MAP fitting | 61 | add | `bayesian-fitting`: Bayesian fitting (maths; MA 08-likelihood (new Note after MA-072)) |
| categorical distribution, ML fitting | 60–61 | taught | MA-072 |
| categorical distribution, relation to multinomial | 45 | taught | MA-031 (multinomial as the many-category binomial) |
| chain model | 243–251, 254–262, 537 | taught | RO 77 (hidden Markov model) |
| chain model, directed | 244–245 | taught | RO 77 |
| chain model, learning | 262 | out-of-scope | learning HMM parameters by EM; the plan's HMMs use known models (RO 77-79) |
| chain model, MAP inference | 246 | add | `hmm-inference`: HMM inference (robotics; RO-02 (section after 79)). MAP path = Viterbi |
| chain model, marginal posterior inference | 254 | add | `hmm-inference`: HMM inference (robotics; RO-02 (section after 79)). marginals = forward-backward smoothing |
| chain model, sum product algorithm in | 259 | add | `hmm-inference`: HMM inference (robotics; RO-02 (section after 79)) |
| chain model, undirected | 245 | out-of-scope | cv-special: undirected chain models (CRFs) |
| changing face pose | 137 | out-of-scope | app: face synthesis (graphics) |
| Chapman-Kolmogorov equation | 539 | taught | RO 78 (prediction step) |
| checkerboard | 405 | taught | RO 89 |
| class conditional density function | 91, 102 | taught | ML-082 (class-conditional likelihood in naive Bayes) |
| classification | 83, 171–201, 209 | taught | ML-003 |
| classification, adaboost | 200 | taught | ML-109 |
| classification, applications of | 201–209 | index-noise | pointer to the book's list of applications |
| classification, Bayesian logistic regression | 176–180 | out-of-scope | ml-zoo: classifier variant |
| classification, binary | 88–91, 171–196 | taught | ML-071 |
| classification, boosting | 193–194 | taught | ML-116 |
| classification, cascade structure | 203 | out-of-scope | cv-special: detector cascade (Viola-Jones) |
| classification, dual logistic regression | 183–185 | out-of-scope | ml-zoo: classifier variant |
| classification, fern | 199 | out-of-scope | ml-zoo: classifier variant (ferns) |
| classification, gender | 201 | out-of-scope | app: gender classification (biometrics) |
| classification, kernel logistic regression | 185–186 | out-of-scope | ml-zoo: classifier variant |
| classification, logistic regression | 89, 171–175 | taught | ML-071 to ML-074 |
| classification, multi-class | 197–198 | taught | ML-078 |
| classification, multi-layer perceptron | 200 | taught | DL-008 |
| classification, non-probabilistic models | 200–201 | taught | ML-086 |
| classification, nonlinear logistic regression | 181 | taught | ML-079 (polynomial logistic regression) |
| classification, one-against-all | 197 | taught | ML-078 (one-vs-rest) |
| classification, random classification tree | 198–200 | taught | ML-091; ML-102 |
| classification, random forest | 200 | taught | ML-102 |
| classification, relevance vector | 186–190 | out-of-scope | ml-zoo: relevance vector machine |
| classification, support vector machine | 200 | taught | ML-086 |
| classification, tree | 194–196, 209 | taught | ML-091 |
| classification, weak classifier | 194 | taught | ML-109 (weak learners) |
| clique | 223, 281 | out-of-scope | cv-special: cliques of undirected models (MRFs) |
| clique, maximal | 224 | out-of-scope | cv-special: cliques of undirected models (MRFs) |
| closed set face identification | 512 | out-of-scope | app: face identification (biometrics) |
| clustering | 113, 349–351 | taught | ML-122 |
| coarse-to-fine approach | 309, 480 | taught | RO 227 (pyramids, coarse-to-fine) |
| collinearity [see homography] | 395 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)). what each transform keeps (straight lines) |
| color model | 93, 95, 305 | out-of-scope | app: skin-colour detection (biometrics) |
| combining variables | 265 | out-of-scope | cv-special: graphical-model inference trick |
| concave function | 176 | taught | MA-067 |
| condensation algorithm | 558–562 | taught | RO 82 (CONDENSATION = particle filter) |
| condensation algorithm, for tracking contour | 565 | out-of-scope | app: contour tracking (cv-special) |
| condition number | 620 | taught | MA-058 |
| conditional independence | 217 | taught | ML-081 |
| conditional independence, in a directed model | 220 | add | `bayes-networks`: Probabilistic graphical models (maths; MA 02-probability (new Note after MA-019)) |
| conditional independence, in an undirected model | 224 | out-of-scope | cv-special: independence in undirected models (MRFs) |
| conditional probability distribution | 28 | taught | MA-015 |
| conditional probability distribution, of multivariate normal | 73 | add | `gaussian-conditioning`: Marginal and conditional of a joint Gaussian (maths; MA 08-likelihood (with the planned linear-transforms Note)) |
| conditional random field | 316 | out-of-scope | cv-special: conditional random fields for image labelling |
| conditional random field, 1D | 263 | out-of-scope | cv-special: conditional random fields for image labelling |
| conditional random field, 2D | 300–302 | out-of-scope | cv-special: conditional random fields for image labelling |
| conic | 387, 421, 462 | out-of-scope | cv-special: projective geometry of conics |
| conjugacy | 42 | add | `bayesian-fitting`: Bayesian fitting (maths; MA 08-likelihood (new Note after MA-072)) |
| conjugacy, Bernoulli/beta | 46 | add | `bayesian-fitting`: Bayesian fitting (maths; MA 08-likelihood (new Note after MA-072)) |
| conjugacy, categorical/Dirichlet distribution | 46 | add | `bayesian-fitting`: Bayesian fitting (maths; MA 08-likelihood (new Note after MA-072)) |
| conjugacy, normal/normal inverse Wishart | 47 | out-of-scope | multivariate conjugate prior beyond beginner depth |
| conjugacy, normal/normal-scaled inverse gamma | 47 | out-of-scope | conjugate prior beyond beginner depth |
| conjugacy, self-conjugacy of normal | 75 | taught | new MA: Product of two Gaussians |
| conjugate gradient method | 608 | taught | new MA: Sparse linear solves and conjugate gradient |
| constellation model | 585–588 | out-of-scope | cv-special: 2000s part-based object recognition (research-only now) |
| constraint edge | 294, 316, 319 | out-of-scope | cv-special: graph-cut construction detail |
| continuous random variable | 25 | taught | MA-020 |
| contour model | 463–468 | out-of-scope | cv-special: snakes (active contours) |
| contour tracking | 537, 565 | out-of-scope | cv-special: contour tracking |
| contrastive divergence | 236–237 | out-of-scope | ml-zoo: training restricted Boltzmann machines |
| contrastive divergence, persistent | 237 | out-of-scope | ml-zoo: training restricted Boltzmann machines |
| convex function | 176, 602 | taught | MA-065; MA-067 |
| convex potentials | 296, 297 | out-of-scope | cv-special: MRF potentials |
| corner detection | 336, 339–341, 352 | taught | RO 227 |
| corner detection, Harris corner detector | 339 | taught | RO 227 |
| corner detection, SIFT | 339–341 | taught | RO 228 |
| cost function | 601 | taught | MA-065 |
| covariance | 32 | taught | MA-009 |
| covariance matrix | 41, 69 | taught | MA-009; ML-047 |
| covariance matrix, diagonal | 69 | taught | MA-073 (diagonal/spherical/full covariance) |
| covariance matrix, full | 69 | taught | MA-073 |
| covariance matrix, spherical | 69 | taught | MA-073 |
| CRF | 316 | out-of-scope | cv-special: conditional random fields for image labelling |
| CRF, 1D | 263 | out-of-scope | cv-special: conditional random fields for image labelling |
| CRF, 2D | 300–302 | out-of-scope | cv-special: conditional random fields for image labelling |
| cross product | 614 | taught | new MA: Cross product and skew-symmetric matrix |
| cross-ratio | 422 | out-of-scope | cv-special: projective invariant |
| cut on a graph | 285 | out-of-scope | cv-special: graph cuts |
| cut on a graph, cost | 285 | out-of-scope | cv-special: graph cuts |
| cut on a graph, minimum | 286 | out-of-scope | cv-special: graph cuts |
| damped Newton | 608 | taught | new MA short section: Levenberg-Marquardt (damped Gauss-Newton) |
| data association | 470, 560 | taught | RO 178 |
| decision boundary | 98, 172 | taught | ML-070; ML-086 |
| Delaunay triangulation | 443 | out-of-scope | mesh-building geometry; the plan's exact roadmaps use the Voronoi diagram (RO 270) |
| delta function | 600 | index-noise | entry in the book's notation appendix (symbol) |
| denoising | 279, 282–284 | out-of-scope | cv-special: MRF image denoising |
| denoising, binary | 291 | out-of-scope | cv-special: MRF image denoising |
| denoising, multi-label | 297, 300 | out-of-scope | cv-special: MRF image denoising |
| dense stereo vision | 267–270, 307–308, 443 | taught | RO 90 |
| depth from structured light | 378–380 | taught | RO 90 |
| derivative filter | 329 | taught | RO 227 (gradient filters) |
| descriptor | 341–345, 352 | taught | RO 228 |
| descriptor, bag of words | 344–345 | taught | RO 236 |
| descriptor, histogram | 341–342 | taught | RO 228 |
| descriptor, HOG | 343–344 | out-of-scope | hand-designed detector feature; the plan's detectors are learned (RO 173-174) |
| descriptor, SIFT | 342–343 | taught | RO 228 |
| determinant of matrix | 615 | taught | MA-056 (determinant, G-598); MA-063 §5 |
| diagonal covariance matrix | 69 | taught | MA-073 |
| diagonal matrix | 614 | taught | MA-056 |
| diagonal matrix, inverting | 626 | out-of-scope | trivial arithmetic (invert each diagonal entry); diagonal matrices are MA-056 |
| dictionary of visual words | 344, 571 | taught | RO 236 |
| difference of Gaussians | 331 | add | `image-laplacian-log`: Second-derivative image filters (vision; RO-18 (section in 227, before SIFT in 228)). DoG approximates the Laplacian of Gaussian |
| digits |  | index-noise | heading (dataset pointer) |
| digits, modeling | 138 | out-of-scope | app: handwritten digit modelling |
| dimensionality reduction | 345–352 | taught | ML-045 |
| dimensionality reduction, dual PCA | 349 | out-of-scope | ml-zoo: dual PCA |
| dimensionality reduction, K-means | 349–351 | taught | ML-122 |
| dimensionality reduction, PCA | 348 | taught | ML-047 |
| direct linear transformation algorithm | 400–402 | taught | RO 89 |
| direct search method | 609 | taught | RL 43 (derivative-free search) |
| directed graphical model | 219–222 | add | `bayes-networks`: Probabilistic graphical models (maths; MA 02-probability (new Note after MA-019)) |
| directed graphical model, chain | 244–245 | taught | RO 77 |
| directed graphical model, comparison to undirected | 225 | add | `bayes-networks`: Probabilistic graphical models (maths; MA 02-probability (new Note after MA-019)) |
| directed graphical model, establishing conditional independence relations in | 220 | add | `bayes-networks`: Probabilistic graphical models (maths; MA 02-probability (new Note after MA-019)) |
| directed graphical model, for grids | 304 | out-of-scope | cv-special: directed grid models |
| directed graphical model, learning | 234–235 | out-of-scope | ml-zoo: learning Bayes nets |
| directed graphical model, Markov blanket | 220 | add | `bayes-networks`: Probabilistic graphical models (maths; MA 02-probability (new Note after MA-019)) |
| directed graphical model, sampling | 232 | add | `bayes-networks`: Probabilistic graphical models (maths; MA 02-probability (new Note after MA-019)) |
| Dirichlet distribution | 35, 39 | out-of-scope | ml-zoo: Dirichlet prior, used by topic models |
| discrete random variable | 25 | taught | MA-020 |
| discriminative model | 84–85 | add | `generative-vs-discriminative`: Generative vs discriminative models (maths; ML 07-classification (section in ML-081)) |
| discriminative model, classification | 171–201 | add | `generative-vs-discriminative`: Generative vs discriminative models (maths; ML 07-classification (section in ML-081)) |
| discriminative model, regression | 143–169 | add | `generative-vs-discriminative`: Generative vs discriminative models (maths; ML 07-classification (section in ML-081)) |
| disparity | 268, 307 | taught | RO 90 |
| displacement expert | 167 | out-of-scope | app: head tracking regressor |
| distance transform | 464 | add | `distance-transform`: Distance transform of a grid (robotics; RO-04 (section in 98, inflation layer)) |
| distribution |  | index-noise | heading |
| distribution, Bernoulli | 35–37 | taught | MA-031 |
| distribution, beta | 35, 37–38 | add | `bayesian-fitting`: Bayesian fitting (maths; MA 08-likelihood (new Note after MA-072)) |
| distribution, binomial | 45 | taught | MA-031 |
| distribution, categorical | 35, 38 | taught | MA-031 |
| distribution, conjugate | 42 | add | `bayesian-fitting`: Bayesian fitting (maths; MA 08-likelihood (new Note after MA-072)) |
| distribution, Dirichlet | 35, 39 | out-of-scope | ml-zoo: Dirichlet prior, used by topic models |
| distribution, gamma | 117 | out-of-scope | used only as a latent prior in the book's t-distribution model |
| distribution, multinomial | 45 | taught | MA-031 |
| distribution, multivariate normal | 41–42, 69–76 | taught | MA-073 |
| distribution, normal | 35 | taught | MA-024 |
| distribution, normal inverse Wishart | 35, 42 | out-of-scope | multivariate conjugate prior beyond beginner depth |
| distribution, normal-scaled inverse gamma | 35, 40 | out-of-scope | conjugate prior beyond beginner depth |
| distribution, probability | 35–45 | taught | MA-020 |
| distribution, t-distribution | 115–120 | taught | MA-037 (t distribution) |
| distribution, univariate normal | 40 | taught | MA-024 |
| DLT algorithm | 400–402 | taught | RO 89 |
| dolly zoom | 385 | out-of-scope | app: cinematography effect (different field); the perspective it shows is RO 88 |
| domain of a random variable | 35 | taught | MA-020 |
| dot product | 613 | taught | MA-050 |
| dual |  | index-noise | heading |
| dual, linear regression | 161–163 | out-of-scope | ml-zoo: dual form of regression (kernel-method breadth) |
| dual, logistic regression | 183–185 | out-of-scope | ml-zoo: dual logistic regression |
| dual, parameterization | 161, 184 | out-of-scope | ml-zoo: dual parameterisation of kernel models |
| dual, PCA | 349 | out-of-scope | ml-zoo: dual PCA |
| dynamic programming | 248, 274 | taught | RL 12 to RL 14 (dynamic programming); RO 205 |
| dynamic programming, for stereo vision | 274 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90). dynamic programming along scanlines |
| dynamic programming, in a chain | 248–251 | add | `hmm-inference`: HMM inference (robotics; RO-02 (section after 79)). DP on a chain = Viterbi |
| dynamic programming, in a loop | 278 | out-of-scope | cv-special: DP on loopy grids |
| dynamic programming, in a tree | 251–254 | out-of-scope | cv-special: DP on tree-structured part models |
| E-step | 106, 128, 130–132 | taught | MA-074 |
| edge detection | 336, 352 | add | `edge-detection`: Edge detection (vision; RO-18 (section in 227)). DL-042 §5 shows edge kernels only, not a detector |
| edge detection, Canny | 336–338, 464 | add | `edge-detection`: Edge detection (vision; RO-18 (section in 227)) |
| edge filter | 329 | taught | DL-042 §4.2, §6.4 (edge kernels) |
| eight-point algorithm | 433–435 | taught | RO 232 (normalised 8-point algorithm) |
| EKF | 550–554 | taught | RO 81 |
| EM algorithm | 106–108, 127–132 | taught | MA-074 |
| EM algorithm, E-step | 107, 128, 130–132 | taught | MA-074 |
| EM algorithm, for factor analyzer | 124–126 | out-of-scope | ml-zoo: factor analysis |
| EM algorithm, for mixture of Gaussians | 110–115 | taught | MA-074 (EM for Gaussian mixtures) |
| EM algorithm, for t distribution | 117–120 | out-of-scope | ml-zoo: EM for t-distributions |
| EM algorithm, lower bound | 129 | taught | MA-074 (lower bound via Jensen) |
| EM algorithm, M-step | 107, 132 | taught | MA-074 |
| empirical max-marginals | 231 | out-of-scope | cv-special: sampling-based max-marginals |
| energy minimization | 223 | out-of-scope | cv-special: MRF energy minimisation |
| epipolar constraint | 424 | taught | RO 232 |
| epipolar geometry | 424 | taught | RO 232 |
| epipolar line | 424 | taught | RO 232 |
| epipolar line, computing | 429 | taught | RO 232 |
| epipole | 425–426 | taught | RO 232 |
| epipole, computing | 429 | taught | RO 232 |
| essential matrix | 427–429, 453 | taught | RO 232 |
| essential matrix, decomposition | 430–431 | taught | RO 233 (recovering R and t from E) |
| essential matrix, properties | 428–429 | taught | RO 232 |
| estimating parameters | 49–65 | taught | MA-070 |
| Euclidean transformation | 389–392 | taught | new MA: Rigid-body transforms and homogeneous coordinates |
| Euclidean transformation, learning | 398 | taught | RO 92 (fitting a rigid transform to matched points) |
| evidence | 30, 65 | taught | MA-018; ML-082 |
| evidence, framework | 66 | out-of-scope | ml-zoo: evidence framework for model selection |
| expectation | 31–32 | taught | MA-012 |
| expectation maximization | 106–108, 127–132, 140 | taught | MA-074 |
| expectation maximization, E-step | 107, 128, 130–132 | taught | MA-074 |
| expectation maximization, for factor analyzer | 124–126 | out-of-scope | ml-zoo: factor analysis |
| expectation maximization, for mixture of Gaussians | 110–115 | taught | MA-074 |
| expectation maximization, for t-distribution | 117–120 | out-of-scope | ml-zoo: EM for t-distributions |
| expectation maximization, lower bound | 129 | taught | MA-074 |
| expectation maximization, M-step | 107, 132 | taught | MA-074 |
| expectation step | 106, 107, 128, 130–132 | taught | MA-074 |
| expert | 195 | out-of-scope | ml-zoo: mixture of experts |
| exponential family | 45 | out-of-scope | ml-zoo: exponential-family theory, no robotics Note uses it |
| extended Kalman filter | 550–554 | taught | RO 81 |
| exterior orientation problem | 373, 385 | taught | RO 233 (PnP) |
| exterior orientation problem, 3D scene | 367, 373–375 | taught | RO 233 |
| exterior orientation problem, planar scene | 403–405 | taught | RO 233; RO 229 (pose from a plane) |
| extrinsic parameters | 365 | taught | RO 88 |
| extrinsic parameters, estimation | 385 | taught | RO 233 |
| extrinsic parameters, learning |  | taught | RO 233 |
| extrinsic parameters, learning, 3D scene | 367, 373–375 | taught | RO 233 |
| extrinsic parameters, learning, planar scene | 403–405 | taught | RO 233 |
| face |  | index-noise | heading |
| face, clustering | 512, 529 | out-of-scope | app: face recognition (biometrics) |
| face, detection | 101, 102, 133–134, 140, 202–203, 210 | out-of-scope | app: face detection (biometrics); generic detection is RO 173 |
| face, recognition | 136, 503, 517, 528–530, 533 | out-of-scope | app: face recognition (biometrics) |
| face, recognition, across pose | 137 | out-of-scope | app: face recognition (biometrics) |
| face, recognition, as model comparison | 510–514 | out-of-scope | app: face recognition (biometrics) |
| face, recognition, closed set identification | 512 | out-of-scope | app: face recognition (biometrics) |
| face, recognition, open set identification | 512 | out-of-scope | app: face recognition (biometrics) |
| face, synthesis | 314–315 | out-of-scope | app: face synthesis (graphics) |
| face, verification | 503 | out-of-scope | app: face verification (biometrics) |
| face model |  | index-noise | heading |
| face model, 3D morphable | 494–496 | out-of-scope | app: face modelling (graphics) |
| facial features |  | index-noise | heading |
| facial features, aligning | 533 | out-of-scope | app: facial landmarks (biometrics) |
| facial features, finding | 271, 274 | out-of-scope | app: facial landmarks (biometrics) |
| factor analysis | 120, 140, 503 | out-of-scope | ml-zoo: factor analysis |
| factor analysis, as a marginalization | 122 | out-of-scope | ml-zoo: factor analysis |
| factor analysis, learning | 124–126 | out-of-scope | ml-zoo: factor analysis |
| factor analysis, mixture of factor analyzers | 126 | out-of-scope | ml-zoo: factor analysis |
| factor analysis, probability density function | 121 | out-of-scope | ml-zoo: factor analysis |
| factor graph | 240, 257, 275 | taught | RO 263 |
| factorization | 445 | out-of-scope | cv-special: factorisation SfM for affine cameras |
| factorization, of a probability distribution | 219, 223 | add | `bayes-networks`: Probabilistic graphical models (maths; MA 02-probability (new Note after MA-019)). factorising a joint distribution by a graph |
| factorization, Tomasi-Kanade | 453, 455 | out-of-scope | cv-special: Tomasi-Kanade factorisation (affine cameras) |
| feature | 453 | taught | RO 227 |
| feature, tracking | 453 | taught | RO 230 (KLT tracking) |
| feature descriptor | 341–345 | taught | RO 228 |
| feature descriptor, bag of words | 344–345 | taught | RO 236 |
| feature descriptor, histogram | 341–342 | taught | RO 228 |
| feature descriptor, HOG | 343–344 | out-of-scope | hand-designed detector feature; the plan's detectors are learned (RO 173-174) |
| feature descriptor, SIFT | 342–343 | taught | RO 228 |
| feature detector | 336 | taught | RO 227 |
| feature detector, Canny edge detector | 336–338 | add | `edge-detection`: Edge detection (vision; RO-18 (section in 227)) |
| feature detector, Harris corner detector | 339 | taught | RO 227 |
| feature detector, SIFT detector | 339–341 | taught | RO 228 |
| fern | 199 | out-of-scope | ml-zoo: random ferns |
| field of view | 363 | add | `pinhole-geometry-terms`: Pinhole geometry terms (vision; RO-03 (section in 88)). field of view from focal length |
| filter | 327 | taught | DL-042; RO 227 |
| filter, bilateral | 353 | add | `nonlinear-image-filters`: Nonlinear image filters (vision; RO-18 (section in 227) or RO 90 depth-map cleanup) |
| filter, derivative | 329 | taught | RO 227 |
| filter, different of Gaussian | 331 | add | `image-laplacian-log`: Second-derivative image filters (vision; RO-18 (section in 227, before SIFT in 228)) |
| filter, edge | 329 | taught | DL-042 |
| filter, Gabor | 331 | out-of-scope | cv-special: texture filter bank, no robotics Note uses it |
| filter, Haar | 331 | out-of-scope | cv-special: Haar features for Viola-Jones |
| filter, Laplacian | 329 | add | `image-laplacian-log`: Second-derivative image filters (vision; RO-18 (section in 227, before SIFT in 228)) |
| filter, Laplacian of Gaussian | 329 | add | `image-laplacian-log`: Second-derivative image filters (vision; RO-18 (section in 227, before SIFT in 228)) |
| filter, Prewitt | 329 | taught | RO 227 (gradient filters) |
| filter, Sobel | 329 | taught | RO 227 (gradient filters) |
| fitting probability models | 49–65 | taught | MA-070 |
| fixed interval smoothing | 547–548 | add | `rts-smoother`: Batch estimation and smoothing (robotics; RO-22 (new Note after 257)) |
| fixed lag smoothing | 546–547 | add | `rts-smoother`: Batch estimation and smoothing (robotics; RO-22 (new Note after 257)) |
| flow |  | index-noise | heading |
| flow, optical | 308 | taught | RO 230 |
| flow, through graph | 285 | out-of-scope | max-flow in a graph cut (cv-special) |
| focal length | 360 | taught | RO 88 |
| focal length, parameter | 362 | taught | RO 88 |
| forest | 200, 207 | taught | ML-102 |
| forward-backward algorithm | 255–257 | add | `hmm-inference`: HMM inference (robotics; RO-02 (section after 79)) |
| Frobenius norm | 625 | taught | MA-059 |
| frustum | 416 | out-of-scope | graphics term for the visible volume of a camera |
| full covariance matrix | 69 | taught | MA-073 |
| fundamental matrix | 432, 453 | taught | RO 232 |
| fundamental matrix, decomposition | 441 | out-of-scope | cv-special: projective reconstruction from F (uncalibrated cameras) |
| fundamental matrix, estimation | 432–435 | taught | RO 232 |
| fundamental matrix, relation to essential matrix | 432 | taught | RO 232 |
| Gabor energy | 331 | out-of-scope | cv-special: texture filter bank |
| Gabor filter | 331 | out-of-scope | cv-special: texture filter bank |
| gallery face | 512 | out-of-scope | app: face recognition (biometrics) |
| gamma distribution | 117 | out-of-scope | used only as a latent prior in the book's t-distribution model |
| gamma function | 37 | out-of-scope | special function used only inside normalising constants |
| gating function | 195 | out-of-scope | ml-zoo: mixture of experts |
| Gauss-Newton method | 606–607 | taught | new MA: Nonlinear least squares (Gauss-Newton) |
| Gaussian distribution [see normal distribution] |  | index-noise | cross-reference |
| Gaussian Markov random field | 318 | out-of-scope | cv-special: Gaussian MRF |
| Gaussian process |  | taught | new ML: Gaussian processes |
| Gaussian process, classification | 186 | out-of-scope | ml-zoo: GP classification |
| Gaussian process, latent variable model | 487–491, 518 | out-of-scope | ml-zoo: GP latent variable model |
| Gaussian process, latent variable model, multi-factor | 531–532 | out-of-scope | ml-zoo: GP latent variable model |
| Gaussian process, regression | 156, 169 | taught | new ML: Gaussian processes |
| gender classification | 171, 201, 209 | out-of-scope | app: gender classification (biometrics) |
| generalized Procrustes analysis | 472–473 | out-of-scope | app: shape-model alignment (biometrics, medical) |
| generative model | 84, 85 | add | `generative-vs-discriminative`: Generative vs discriminative models (maths; ML 07-classification (section in ML-081)) |
| generative model, comparison to discriminative model | 91 | add | `generative-vs-discriminative`: Generative vs discriminative models (maths; ML 07-classification (section in ML-081)) |
| geodesic distance | 307 | out-of-scope | cv-special: geodesic segmentation |
| geometric invariants | 422 | out-of-scope | cv-special: projective invariants |
| geometric transformation model | 389–415 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)) |
| geometric transformation model, 2D | 389–396 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)) |
| geometric transformation model, application | 415–418 | index-noise | application pointer |
| geometric transformation model, learning | 396 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)) |
| gesture tracking | 243, 267 | out-of-scope | app: gesture tracking |
| Gibbs distribution | 223, 280 | out-of-scope | cv-special: Gibbs distribution of an MRF |
| Gibbs sampling | 233 | out-of-scope | MCMC for undirected models; the plan samples with particle filters and importance sampling (RO 82) |
| GPLVM | 487–491, 518 | out-of-scope | ml-zoo: GP latent variable model |
| GPLVM, multi-factor | 531–532 | out-of-scope | ml-zoo: GP latent variable model |
| GrabCut | 305–307 | out-of-scope | app: interactive photo segmentation |
| gradient vector | 175, 604 | taught | MA-062 |
| graph cuts | 284–300, 316 | out-of-scope | cv-special: graph cuts |
| graph cuts, alpha-expansion | 298–300 | out-of-scope | cv-special: graph cuts |
| graph cuts, applications of | 304–309 | out-of-scope | cv-special: graph cuts |
| graph cuts, binary variables | 286–291 | out-of-scope | cv-special: graph cuts |
| graph cuts, efficient reuse of solution | 316 | out-of-scope | cv-special: graph cuts |
| graph cuts, multi-label | 293–300 | out-of-scope | cv-special: graph cuts |
| graph cuts, reparameterization | 290–291 | out-of-scope | cv-special: graph cuts |
| graph cuts, volumetric | 450–452 | out-of-scope | cv-special: graph cuts |
| graphical model | 217–239 | add | `bayes-networks`: Probabilistic graphical models (maths; MA 02-probability (new Note after MA-019)) |
| graphical model, applications in computer vision | 227 | index-noise | application pointer |
| graphical model, chain | 243, 537 | taught | RO 77 |
| graphical model, directed | 219–222 | add | `bayes-networks`: Probabilistic graphical models (maths; MA 02-probability (new Note after MA-019)) |
| graphical model, directed, learning | 234–235 | out-of-scope | ml-zoo: learning Bayes nets |
| graphical model, directed, sampling | 232 | add | `bayes-networks`: Probabilistic graphical models (maths; MA 02-probability (new Note after MA-019)) |
| graphical model, directed vs. undirected | 225 | add | `bayes-networks`: Probabilistic graphical models (maths; MA 02-probability (new Note after MA-019)) |
| graphical model, factor graph | 240 | taught | RO 263 |
| graphical model, grid-based | 263 | out-of-scope | cv-special: grid MRFs |
| graphical model, plate notation | 222 | out-of-scope | diagram notation (book-specific) |
| graphical model, tree | 243 | out-of-scope | cv-special: tree-structured part models |
| graphical model, undirected | 223 | out-of-scope | cv-special: undirected models (MRFs) |
| graphical model, undirected, learning | 235–238 | out-of-scope | cv-special: learning MRFs |
| graphical model, undirected, sampling | 233 | out-of-scope | cv-special: sampling MRFs |
| Gray codes | 380 | out-of-scope | detail of one structured-light coding scheme; structured light itself is RO 90 |
| grid-based model | 263, 279–318 | out-of-scope | cv-special: grid MRFs |
| grid-based model, applications | 316 | out-of-scope | cv-special: grid MRFs |
| grid-based model, directed | 304 | out-of-scope | cv-special: grid MRFs |
| Haar-like filter | 203, 331 | out-of-scope | cv-special: Haar features for Viola-Jones |
| hand model | 492, 493, 500 | out-of-scope | app: hand modelling (graphics) |
| Harris corner detector | 339 | taught | RO 227 |
| head position |  | index-noise | heading |
| head position, tracking | 167 | out-of-scope | app: head tracking |
| Heaviside step function | 181, 193, 600 | taught | DL-004 (step function) |
| Hessian matrix | 175, 602 | taught | MA-064 |
| hidden layer | 200 | taught | DL-008 |
| hidden Markov model | 227, 245, 246, 267, 274 | taught | RO 77 |
| hidden variable | 104, 105 | taught | MA-073 (latent variable) |
| hidden variable, representing transformations | 138 | out-of-scope | ml-zoo: transformations as hidden variables |
| higher order cliques | 303, 317 | out-of-scope | cv-special: MRF cliques |
| Hinton diagram | 25 | out-of-scope | plotting convention (book-specific) |
| histogram equalization | 326 | add | `point-operators`: Point operators (vision; RO-18 (section in 227)) |
| histogram of oriented gradients | 343–344, 352 | out-of-scope | hand-designed detector feature; the plan's detectors are learned (RO 173-174) |
| histogram, RGB | 341 | taught | ML-019 (histogram); DL-042 §3.2 (RGB channels) |
| HMM | 227, 245, 246, 274 | taught | RO 77 |
| HOG descriptor | 343–344, 352 | out-of-scope | hand-designed detector feature; the plan's detectors are learned (RO 173-174) |
| homogeneous coordinates | 371 | taught | RO 88; new MA: Projective homogeneous coordinates |
| homography | 395–396 | taught | RO 229 |
| homography, learning | 400–402 | taught | RO 229; RO 89 (DLT) |
| homography, properties | 407–409 | taught | RO 229 |
| human part identification | 207–208 | out-of-scope | app: body-part labelling (Kinect) |
| human performance capture | 382, 385 | out-of-scope | app: performance capture (graphics) |
| human pose estimation | 271–272 | taught | RB 317; RB 337 |
| hyperparameter | 36 | taught | DL-039 |
| hysteresis thresholding | 338 | add | `edge-detection`: Edge detection (vision; RO-18 (section in 227)) |
| ICP | 470 | taught | RO 92 |
| ideal point | 370 | add | `projective-points-lines`: Points and lines in homogeneous coordinates (vision; RO-03 (section in 88)). ideal point = point at infinity |
| identity | 503 | out-of-scope | app: face identity (biometrics) |
| identity / style model | 503 | out-of-scope | app: face identity models (biometrics) |
| identity / style model, asymmetric bilinear | 518–524 | out-of-scope | app: face identity models (biometrics) |
| identity / style model, multi-factor GPLVM | 531–532 | out-of-scope | app: face identity models (biometrics) |
| identity / style model, multi-linear | 528 | out-of-scope | app: face identity models (biometrics) |
| identity / style model, nonlinear | 517–518 | out-of-scope | app: face identity models (biometrics) |
| identity / style model, PLDA | 514–517 | out-of-scope | app: face identity models (biometrics) |
| identity / style model, subspace identity model | 506–514 | out-of-scope | app: face identity models (biometrics) |
| identity / style model, symmetric bilinear | 524–528 | out-of-scope | app: face identity models (biometrics) |
| identity matrix | 614 | taught | MA-056 |
| image denoising | 279, 282–284 | out-of-scope | cv-special: MRF image denoising |
| image denoising, binary | 291 | out-of-scope | cv-special: MRF image denoising |
| image denoising, multi-label | 300 | out-of-scope | cv-special: MRF image denoising |
| image descriptor | 352 | taught | RO 228 |
| image plane | 359, 360 | add | `pinhole-geometry-terms`: Pinhole geometry terms (vision; RO-03 (section in 88)). image plane |
| image processing | 325–345, 352 | taught | RO 227 |
| image quilting | 311–314 | out-of-scope | app: texture synthesis (graphics) |
| image retargeting | 308–309 | out-of-scope | app: image editing (graphics) |
| image structure tensor | 339 | taught | new short section: Structure tensor (RO 227) |
| importance sampling | 562 | taught | new MA: Importance sampling |
| incremental fitting |  | index-noise | heading |
| incremental fitting, of logistic regression | 190–193 | out-of-scope | ml-zoo: boosting-style logistic regression |
| independence | 31 | taught | MA-016 |
| independence, conditional | 217 | taught | ML-081 |
| inference | 84 | taught | MA-018 |
| inference, algorithm | 84 | taught | MA-018 |
| inference, empirical max-marginals | 231 | out-of-scope | cv-special: sampling-based max-marginals |
| inference, in graphical models with loops | 265 | out-of-scope | cv-special: inference on loopy graphs |
| inference, MAP solution | 230 | taught | MA-072 |
| inference, marginal posterior distribution | 230 | taught | MA-014; RO 78 |
| inference, maximum marginals | 231 | out-of-scope | cv-special: max-marginals |
| inference, sampling from posterior | 231 | taught | RO 82 |
| innovation | 543 | add | `estimator-consistency`: Is the filter honest? innovation and its covariance, bias, consistency, NEES and NIS tests (robotics; RO-02 (section in 81) or RO-22). innovation (measurement residual) and its covariance |
| integral image | 332 | out-of-scope | cv-special: integral images for Viola-Jones |
| intensity normalization | 325 | add | `point-operators`: Point operators (vision; RO-18 (section in 227)) |
| interactive segmentation | 305–307, 317 | out-of-scope | app: interactive photo segmentation |
| interest point detection | 336, 352 | taught | RO 227 |
| interest point detection, Harris corner detector | 339 | taught | RO 227 |
| interest point detection, SIFT | 339–341 | taught | RO 228 |
| intersection of two lines | 387 | add | `projective-points-lines`: Points and lines in homogeneous coordinates (vision; RO-03 (section in 88)) |
| intrinsic matrix | 365 | taught | RO 88 |
| intrinsic parameters | 365 | taught | RO 88 |
| intrinsic parameters, learning |  | taught | RO 89 |
| intrinsic parameters, learning, from 3D object | 368, 375–376 | taught | RO 89 |
| intrinsic parameters, learning, from a plane | 405–406 | taught | RO 89 |
| invariant |  | index-noise | heading |
| invariant, geometric | 422 | out-of-scope | cv-special: projective invariants |
| inverse of a matrix | 615, 620–621 | taught | ML-053 |
| inverse of a matrix, computing for large matrices | 626 | taught | new MA: Sparse linear solves and conjugate gradient |
| Ishikawa construction | 316 | out-of-scope | cv-special: graph-cut construction |
| iterated extended Kalman filter | 552 | add | `iterated-ekf`: Iterated EKF (robotics; RO-22 (section in 258)) |
| iterative closest point | 470 | taught | RO 92 |
| Jensen’s inequality | 130 | taught | MA-067; MA-074 |
| joint probability | 26 | taught | MA-014 |
| jointboost | 203 | out-of-scope | ml-zoo: boosting variant |
| junction tree algorithm | 265, 266 | out-of-scope | ml-zoo: exact inference on loopy graphs |
| K-means algorithm | 113, 349–351 | taught | ML-122 |
| Kalman filter | 229, 540–548 | taught | RO 80 |
| Kalman filter, temporal and measurement models | 548 | taught | RO 80 |
| Kalman filter, derivation | 541 | taught | RO 80 |
| Kalman filter, extended | 550–554 | taught | RO 81 |
| Kalman filter, iterated extended | 552 | add | `iterated-ekf`: Iterated EKF (robotics; RO-22 (section in 258)) |
| Kalman filter, recursions | 543–544 | taught | RO 80 |
| Kalman filter, smoothing | 546–548 | add | `rts-smoother`: Batch estimation and smoothing (robotics; RO-22 (new Note after 257)) |
| Kalman filter, unscented | 554–558 | taught | RO 256 |
| Kalman gain | 542 | taught | RO 80 |
| Kalman smoothing | 546–548 | add | `rts-smoother`: Batch estimation and smoothing (robotics; RO-22 (new Note after 257)) |
| kernel function | 155–156, 185 | taught | ML-089; ML-090 |
| kernel logistic regression | 185–186 | out-of-scope | ml-zoo: classifier variant |
| kernel PCA | 349, 352 | out-of-scope | ml-zoo: kernel PCA |
| kernel trick | 155 | taught | ML-089 |
| Kinect | 207 | index-noise | product name |
| kinematic chain | 492 | taught | RO 69 |
| Kullback-Leibler divergence | 131 | taught | new MA: KL divergence |
| landmark point | 463 | out-of-scope | app: shape-model landmarks (biometrics) |
| landscape matrix | 614 | out-of-scope | book-specific word for a wide matrix |
| Laplace approximation | 178, 179, 188 | taught | MA-064 §Extra (Laplace approximation, G-1043) |
| Laplacian filter | 329 | add | `image-laplacian-log`: Second-derivative image filters (vision; RO-18 (section in 227, before SIFT in 228)) |
| Laplacian of Gaussian filter | 329 | add | `image-laplacian-log`: Second-derivative image filters (vision; RO-18 (section in 227, before SIFT in 228)) |
| latent Dirichlet allocation | 576–581, 595 | out-of-scope | ml-zoo: text topic model |
| latent Dirichlet allocation, learning | 578–581 | out-of-scope | ml-zoo: text topic model |
| latent variable | 104, 105 | taught | MA-073 |
| LDA (latent Dirichlet allocation) | 576–581, 595 | out-of-scope | ml-zoo: text topic model |
| LDA (latent Dirichlet allocation), learning | 578–581 | out-of-scope | ml-zoo: text topic model |
| LDA (linear discriminant analysis) | 533 | out-of-scope | ml-zoo: no robotics Note needs it; ML-022 names it (G-1059) |
| learning | 49, 84 | taught | ML-001 |
| learning, Bayesian approach | 50–51 | add | `bayesian-fitting`: Bayesian fitting (maths; MA 08-likelihood (new Note after MA-072)) |
| learning, in chains and trees | 262 | out-of-scope | learning HMM parameters; the plan's HMMs use known models |
| learning, in directed models | 234–235 | out-of-scope | ml-zoo: learning Bayes nets |
| learning, in undirected models | 235–238 | out-of-scope | cv-special: learning MRFs |
| learning, least squares | 54 | taught | ML-050 |
| learning, maximum a posteriori | 50 | taught | MA-072 |
| learning, maximum likelihood | 49 | taught | MA-070 |
| learning algorithm | 84 | taught | ML-001 |
| least median of squares regression | 420 | out-of-scope | robust-regression variant; the plan uses RANSAC and robust losses (RO 229, RO 235) |
| least squares | 54 | taught | ML-050; MA-060 |
| least squares, solving least squares problems | 623 | taught | MA-060; ML-053 |
| likelihood | 30 | taught | MA-069 |
| line | 387, 421 | add | `projective-points-lines`: Points and lines in homogeneous coordinates (vision; RO-03 (section in 88)) |
| line, epipolar | 424 | taught | RO 232 |
| line, joining two points | 387 | add | `projective-points-lines`: Points and lines in homogeneous coordinates (vision; RO-03 (section in 88)) |
| line search | 608 | mentioned-only | `line-search`: Line search and step-size rules (backtracking) in optimisation (maths; MA 07-optimisation (section in the planned nonlinear least squares Note)). MA-064 names it in one parenthesis only |
| linear algebra | 613–628 | taught | MA-047 |
| linear algebra, common problems | 623–626 | taught | MA-060; RO 89; RO 92 |
| linear discriminant analysis | 533 | out-of-scope | ml-zoo: no robotics Note needs it; ML-022 names it (G-1059) |
| linear regression | 143–145 | taught | ML-049 |
| linear regression, Bayesian approach | 147–150 | add | `bayesian-fitting`: Bayesian fitting (maths; MA 08-likelihood (new Note after MA-072)) |
| linear regression, limitations of | 145–146 | taught | ML-055; ML-060 |
| linear subspace | 121 | taught | MA-058 (subspaces) |
| linear transform | 617 | taught | MA-053 |
| local binary pattern | 333, 352 | out-of-scope | cv-special: texture descriptor (local binary patterns) |
| local maximum / minimum | 176, 602 | taught | MA-065 |
| log likelihood | 53 | taught | MA-070 |
| logistic classification tree | 194–196 | out-of-scope | ml-zoo: classifier variant |
| logistic regression | 89, 171–175 | taught | ML-071 |
| logistic regression, Bayesian approach | 176–180 | out-of-scope | ml-zoo: classifier variant |
| logistic regression, branching | 194–196 | out-of-scope | ml-zoo: classifier variant |
| logistic regression, dual | 183–185 | out-of-scope | ml-zoo: dual logistic regression |
| logistic regression, kernel | 185–186 | out-of-scope | ml-zoo: kernel logistic regression |
| logistic regression, multi-class | 197–198 | taught | ML-078 |
| logistic regression, nonlinear | 181 | taught | ML-079 |
| logistic sigmoid function | 171 | taught | ML-071 |
| logitboost | 193–194 | out-of-scope | ml-zoo: boosting variant |
| loopy belief propagation | 266 | out-of-scope | message passing on loopy graphs; robot factor graphs are solved by least squares (RO 263) |
| loopy belief propagation, applications | 275 | out-of-scope | message passing on loopy graphs; robot factor graphs are solved by least squares (RO 263) |
| M-estimator | 420 | taught | RO 235 (robust costs, M-estimators) |
| M-step | 106, 129, 132 | taught | MA-074 |
| magnitude of vector | 613 | taught | MA-049 |
| manifold | 346 | taught | RO 72 (C-space manifolds) |
| MAP estimation | 50 | taught | MA-072 |
| marginal distribution | 27 | taught | MA-014 |
| marginal distribution, of multivariate normal | 72 | add | `gaussian-conditioning`: Marginal and conditional of a joint Gaussian (maths; MA 08-likelihood (with the planned linear-transforms Note)) |
| marginal posterior distribution | 230 | taught | MA-014; RO 78 |
| marginalization | 27 | taught | MA-014 |
| Markov assumption | 244, 537 | taught | new MA: Markov chains (Markov assumption) |
| Markov blanket | 220, 224 | add | `bayes-networks`: Probabilistic graphical models (maths; MA 02-probability (new Note after MA-019)) |
| Markov blanket, in a directed model | 220 | add | `bayes-networks`: Probabilistic graphical models (maths; MA 02-probability (new Note after MA-019)) |
| Markov blanket, in an undirected model | 224 | out-of-scope | cv-special: Markov blanket in undirected models |
| Markov chain Monte Carlo | 233 | out-of-scope | MCMC; the plan samples with particle filters and importance sampling (RO 82) |
| Markov network |  | out-of-scope | cv-special: undirected models (MRFs) |
| Markov network, learning | 235–238 | out-of-scope | cv-special: learning MRFs |
| Markov network, sampling | 233 | out-of-scope | cv-special: sampling MRFs |
| Markov random field | 224, 227, 279, 280, 316 | out-of-scope | cv-special: MRFs for image labelling |
| Markov random field, Gaussian | 318 | out-of-scope | cv-special: MRFs for image labelling |
| Markov random field, applications | 304–309, 316 | out-of-scope | cv-special: MRFs for image labelling |
| Markov random field, higher order | 303, 317 | out-of-scope | cv-special: MRFs for image labelling |
| Markov random field, pairwise | 281 | out-of-scope | cv-special: MRFs for image labelling |
| Markov tree | 227 | out-of-scope | cv-special: tree models |
| matrix | 614 | taught | MA-053 |
| matrix, block diagonal | 626 | taught | new MA: Schur complement (block matrices) |
| matrix, calculus | 621–623 | taught | MA-063 |
| matrix, condition number | 620 | taught | MA-058 |
| matrix, determinant | 615 | taught | MA-056; MA-063 §5 |
| matrix, diagonal | 614 | taught | MA-056 |
| matrix, Frobenious norm | 625 | taught | MA-059 |
| matrix, identity | 614 | taught | MA-053 |
| matrix, inverse | 615, 620–621 | taught | ML-053 |
| matrix, inverting large | 626 | taught | new MA: Sparse linear solves and conjugate gradient |
| matrix, landscape | 614 | out-of-scope | book-specific word for a wide matrix |
| matrix, multiplication | 614 | taught | MA-054 |
| matrix, null space | 616, 620 | taught | MA-058 |
| matrix, orthogonal | 616 | taught | MA-057 |
| matrix, portrait | 614 | out-of-scope | book-specific word for a tall matrix |
| matrix, positive definite | 616 | taught | MA-068 |
| matrix, rank | 620 | taught | MA-052; MA-058 |
| matrix, rotation | 616 | taught | RO 65 |
| matrix, singular | 615 | taught | MA-056 (determinant 0) |
| matrix, square | 614 | taught | MA-053 |
| matrix, trace | 615 | add | `matrix-trace`: Trace of a matrix (maths; MA 05-linear-algebra (section in MA-056)) |
| matrix, transpose | 615 | taught | MA-054 |
| matrix determinant lemma | 628 | out-of-scope | determinant identity used in derivations (proof technique) |
| matrix inversion lemma | 148, 628 | taught | new MA: Woodbury identity |
| max flow | 285 | out-of-scope | max-flow algorithm used only inside graph cuts (cv-special) |
| max flow, algorithms | 316 | out-of-scope | max-flow algorithm used only inside graph cuts (cv-special) |
| max flow, augmenting paths algorithm | 286 | out-of-scope | max-flow algorithm used only inside graph cuts (cv-special) |
| max function | 600 | index-noise | entry in the book's notation appendix (symbol) |
| maximal clique | 224 | out-of-scope | cv-special: MRF cliques |
| maximization step | 106, 107, 129, 132 | taught | MA-074 |
| maximum a posteriori estimation | 50 | taught | MA-072 |
| maximum likelihood estimation | 49 | taught | MA-070 |
| maximum marginals | 231 | out-of-scope | cv-special: max-marginals |
| MCMC | 233 | out-of-scope | MCMC; the plan samples with particle filters and importance sampling (RO 82) |
| measurement incorporation step | 539 | taught | RO 78 (update step) |
| measurement model | 537 | taught | RO 74; RO 76 |
| Mercer’s theorem | 155 | out-of-scope | kernel-theory theorem (proof technique) |
| min cut | 285 | out-of-scope | cv-special: graph cuts |
| min function | 600 | index-noise | entry in the book's notation appendix (symbol) |
| minimum direction problem | 374, 624 | taught | new short section: Least-squares solution of Ax = 0 by the SVD (RO 89) |
| mixture model |  | taught | MA-073 |
| mixture model, mixture of experts | 211 | out-of-scope | ml-zoo: mixture of experts |
| mixture model, mixture of factor analyzers | 126, 140 | out-of-scope | ml-zoo: mixture of factor analysers |
| mixture model, mixture of Gaussians | 108–115, 140 | taught | MA-073 |
| mixture model, mixture of PLDAs | 518 | out-of-scope | app: face recognition (biometrics) |
| mixture model, mixture of t-distributions | 126, 140 | out-of-scope | ml-zoo: mixture of t-distributions |
| mixture model, robust | 126 | out-of-scope | ml-zoo: robust mixtures |
| ML estimation | 49 | taught | MA-070 |
| model | 84 | taught | ML-001; ML-006 |
| model, discriminative | 84–85 | add | `generative-vs-discriminative`: Generative vs discriminative models (maths; ML 07-classification (section in ML-081)) |
| model, generative | 84, 85 | add | `generative-vs-discriminative`: Generative vs discriminative models (maths; ML 07-classification (section in ML-081)) |
| model comparison | 66 | out-of-scope | ml-zoo: Bayesian model comparison |
| model selection | 511 | taught | ML-009 |
| moment | 31–32 | taught | MA-028 |
| moment, about mean | 32 | add | `statistical-moments`: Raw and central moments (maths; MA 03-distributions (section in MA-028)) |
| moment, about zero | 32 | add | `statistical-moments`: Raw and central moments (maths; MA 03-distributions (section in MA-028)) |
| MonoSLAM | 564 | taught | RO 261 (EKF SLAM); RO 236 (visual SLAM) |
| morphable model | 494–496 | out-of-scope | app: face modelling (graphics) |
| mosaic | 417, 420 | out-of-scope | app: photo mosaics (photography) |
| MRF | 224, 227, 279, 280, 316 | out-of-scope | cv-special: MRFs for image labelling |
| MRF, applications | 304–309, 316 | out-of-scope | cv-special: MRFs for image labelling |
| MRF, Gaussian | 318 | out-of-scope | cv-special: MRFs for image labelling |
| MRF, higher order | 303, 317 | out-of-scope | cv-special: MRFs for image labelling |
| MRF, pairwise | 281 | out-of-scope | cv-special: MRFs for image labelling |
| multi-class classification | 197–198 | taught | ML-078 |
| multi-class classification, multi-class logistic regression | 197–198 | taught | ML-078 |
| multi-class classification, random classification tree | 198–200 | taught | ML-102 |
| multi-factor GPLVM | 531–532 | out-of-scope | ml-zoo: GP latent variable model |
| multi-factor model | 528 | out-of-scope | app: multi-factor face models |
| multi-layer perceptron | 200, 209 | taught | DL-008 |
| multi-linear model | 528, 534 | out-of-scope | app: multi-linear face models |
| multi-view geometry | 453 | taught | RO 232 to RO 235 |
| multi-view reconstruction | 369–370, 376–377, 443, 450–453 | taught | RO 235 |
| multinomial distribution | 45 | taught | MA-031 |
| multiple view geometry | 423 | taught | RO 232 |
| multivariate normal distribution | 35, 69–76 | taught | MA-073 |
| naı̈ve Bayes | 94 | taught | ML-081 |
| neural network | 200 | taught | DL-008 |
| Newton method | 176, 605–606 | taught | MA-064 |
| non-convex potentials | 297 | out-of-scope | cv-special: MRF potentials |
| non-stationary model | 545 | out-of-scope | book-specific label for a time-varying temporal model |
| nonlinear identity model | 517–518 | out-of-scope | app: face identity models |
| nonlinear logistic regression | 181 | taught | ML-079 |
| nonlinear optimization | 601–611 | taught | MA-064; ML-056; new MA: Nonlinear least squares |
| nonlinear optimization, BFGS | 608 | taught | MA-064 |
| nonlinear optimization, Broyden Fletcher Goldfarb Shanno | 608 | taught | MA-064 |
| nonlinear optimization, conjugate gradient method | 608 | taught | new MA: Sparse linear solves and conjugate gradient |
| nonlinear optimization, Gauss-Newton method | 606–607 | taught | new MA: Nonlinear least squares (Gauss-Newton) |
| nonlinear optimization, line search | 608 | mentioned-only | `line-search`: Line search and step-size rules (backtracking) in optimisation (maths; MA 07-optimisation (section in the planned nonlinear least squares Note)). MA-064 names it in one parenthesis only |
| nonlinear optimization, Newton method | 605–606 | taught | MA-064 |
| nonlinear optimization, over positive definite matrices | 611 | out-of-scope | parameterisation trick (optimise a Cholesky factor) beyond beginner depth |
| nonlinear optimization, over rotation matrices | 610 | add | `lie-groups`: Matrix Lie groups SO(3)/SE(3) for estimation (maths; MA 05-linear-algebra (new Note after the planned axis-angle Note); used by RO 87, RO 101, RO 235). optimise over rotations by small rotation-vector updates |
| nonlinear optimization, quasi-Newton methods | 608 | taught | MA-064 |
| nonlinear optimization, reparameterization | 609 | out-of-scope | parameterisation trick beyond beginner depth |
| nonlinear optimization, steepest descent | 603–604 | taught | ML-056 (gradient descent) |
| nonlinear optimization, trust-region methods | 608 | taught | RL 38 (trust region); new MA short section: Levenberg-Marquardt |
| nonlinear regression | 150 | taught | ML-060 |
| nonlinear regression, Bayesian | 153 | add | `bayesian-fitting`: Bayesian fitting (maths; MA 08-likelihood (new Note after MA-072)) |
| norm of vector | 613 | taught | MA-049 |
| normal distribution | 35, 69–76 | taught | MA-024 |
| normal distribution, Bayesian fitting | 56 | add | `bayesian-fitting`: Bayesian fitting (maths; MA 08-likelihood (new Note after MA-072)) |
| normal distribution, change of variable | 75 | taught | MA-063 §Extra (density under a change of variables) |
| normal distribution, conditional distribution | 73 | add | `gaussian-conditioning`: Marginal and conditional of a joint Gaussian (maths; MA 08-likelihood (with the planned linear-transforms Note)) |
| normal distribution, covariance decomposition | 71 | taught | MA-073; ML-047 (covariance axes by eigenvectors) |
| normal distribution, MAP fitting | 54 | add | `bayesian-fitting`: Bayesian fitting (maths; MA 08-likelihood (new Note after MA-072)) |
| normal distribution, marginal distribution | 72 | add | `gaussian-conditioning`: Marginal and conditional of a joint Gaussian (maths; MA 08-likelihood (with the planned linear-transforms Note)) |
| normal distribution, ML fitting | 51 | taught | MA-071 |
| normal distribution, multivariate | 35, 41–42 | taught | MA-073 |
| normal distribution, product of two normals | 74, 78 | taught | new MA: Product of two Gaussians |
| normal distribution, self-conjugacy | 75 | taught | new MA: Product of two Gaussians |
| normal distribution, transformation of variable | 72 | taught | new MA: Linear transforms of a Gaussian |
| normal distribution, univariate | 35, 40 | taught | MA-024 |
| normal inverse Wishart distribution | 35, 42 | out-of-scope | multivariate conjugate prior beyond beginner depth |
| normal-scaled inverse gamma distribution | 35, 40 | out-of-scope | conjugate prior beyond beginner depth |
| normalized camera | 361 | add | `pinhole-geometry-terms`: Pinhole geometry terms (vision; RO-03 (section in 88)). normalised camera |
| normalized image coordinates | 373 | add | `pinhole-geometry-terms`: Pinhole geometry terms (vision; RO-03 (section in 88)). normalised image coordinates |
| null space | 616, 620 | taught | MA-058 |
| object recognition | 134–135, 140, 571–592 | taught | RO 173 |
| object recognition, unsupervised | 581 | out-of-scope | research-only: unsupervised object discovery |
| objective function | 601 | taught | MA-065 |
| offset parameter | 363 | taught | RO 88 (principal-point offset) |
| one-against-all classifier | 197 | taught | ML-078 |
| open-set face identification | 512 | out-of-scope | app: face identification (biometrics) |
| optical axis | 360 | add | `pinhole-geometry-terms`: Pinhole geometry terms (vision; RO-03 (section in 88)). optical axis |
| optical center | 359 | add | `pinhole-geometry-terms`: Pinhole geometry terms (vision; RO-03 (section in 88)). optical centre |
| optical flow | 308 | taught | RO 230 |
| optimization | 601–611 | taught | MA-065 to MA-068 |
| optimization, BFGS | 608 | taught | MA-064 |
| optimization, Broyden Fletcher Goldfarb Shanno | 608 | taught | MA-064 |
| optimization, conjugate gradient method | 608 | taught | new MA: Sparse linear solves and conjugate gradient |
| optimization, Gauss-Newton method | 606–607 | taught | new MA: Nonlinear least squares (Gauss-Newton) |
| optimization, line search | 608 | mentioned-only | `line-search`: Line search and step-size rules (backtracking) in optimisation (maths; MA 07-optimisation (section in the planned nonlinear least squares Note)). MA-064 names it in one parenthesis only |
| optimization, Newton method | 605–606 | taught | MA-064 |
| optimization, over positive definite matrix | 611 | out-of-scope | parameterisation trick beyond beginner depth |
| optimization, over rotation matrix | 610 | add | `lie-groups`: Matrix Lie groups SO(3)/SE(3) for estimation (maths; MA 05-linear-algebra (new Note after the planned axis-angle Note); used by RO 87, RO 101, RO 235) |
| optimization, quasi-Newton methods | 608 | taught | MA-064 |
| optimization, reparameterization | 609 | out-of-scope | parameterisation trick beyond beginner depth |
| optimization, steepest descent | 603–604 | taught | ML-056 |
| optimization, trust-region methods | 608 | taught | RL 38; new MA short section: Levenberg-Marquardt |
| orthogonal matrix | 616 | taught | MA-057 |
| orthogonal Procrustes problem | 374, 398, 625 | taught | RO 92 (Kabsch / orthogonal Procrustes) |
| orthogonal vectors | 613 | taught | MA-050 |
| orthographic camera | 387, 455 | out-of-scope | camera model for very distant scenes; robot cameras use the pinhole model (RO 88) |
| outlier | 115, 411 | taught | ML-040; RO 229 |
| pairwise MRF | 281 | out-of-scope | cv-special: pairwise MRFs |
| pairwise term | 248, 284 | out-of-scope | cv-special: pairwise MRF terms |
| panorama | 417, 420 | out-of-scope | app: panoramas (photography) |
| parametric contour model | 463–468 | out-of-scope | cv-special: snakes (active contours) |
| part of object | 577 | out-of-scope | research-only: part-based object models |
| particle filtering | 558–562 | taught | RO 82 |
| partition function | 223 | out-of-scope | cv-special: normaliser of an undirected model |
| PCA | 348 | taught | ML-047 |
| PCA, dual | 349 | out-of-scope | ml-zoo: dual PCA |
| PCA, kernel | 349, 352 | out-of-scope | ml-zoo: kernel PCA |
| PCA, probabilistic | 122, 476–479 | out-of-scope | ml-zoo: probabilistic PCA |
| PDF | 25 | taught | MA-020 |
| PEaRL algorithm | 415, 420 | out-of-scope | research-only: the book's robust-fitting algorithm |
| pedestrian detection | 202–203 | taught | RO 173 (object detection) |
| pedestrian tracking | 563–564 | taught | RO 178 |
| per-pixel image processing | 325 | add | `point-operators`: Point operators (vision; RO-18 (section in 227)) |
| persistent contrastive divergence | 237 | out-of-scope | ml-zoo: training restricted Boltzmann machines |
| perspective projection | 361 | taught | RO 88 |
| perspective-n-point problem | 367, 385 | taught | RO 233 |
| Phong shading model | 494 | out-of-scope | app: graphics shading model |
| Photo-tourism | 449–450 | out-of-scope | named photo-collection system (product); its SfM method is RO 235 |
| photoreceptor spacing | 362 | taught | RO 88 (focal length in pixels from pixel size) |
| pictorial structure | 270, 274 | out-of-scope | cv-special: part-based body model |
| pinhole | 359 | taught | RO 88 |
| pinhole camera | 359–366, 423 | taught | RO 88 |
| pinhole camera, in Cartesian coordinates | 364–365 | taught | RO 88 |
| pinhole camera, in homogeneous coordinates | 372–373 | taught | RO 88 |
| plate | 222 | out-of-scope | diagram notation (book-specific) |
| PLDA | 514–517 | out-of-scope | app: face recognition (biometrics) |
| PnP problem | 367, 385 | taught | RO 233 |
| point distribution model | 471–482 | out-of-scope | app: shape models (biometrics, medical) |
| point estimate | 50 | taught | MA-034 |
| point operator | 325 | add | `point-operators`: Point operators (vision; RO-18 (section in 227)) |
| polar rectification | 443 | out-of-scope | cv-special: rectification variant; rectification is RO 90 |
| portrait matrix | 614 | out-of-scope | book-specific word for a tall matrix |
| pose estimation | 420 | taught | RO 233 |
| positive definite matrix | 616 | taught | MA-068 |
| positive definite matrix, optimization over | 611 | out-of-scope | parameterisation trick beyond beginner depth |
| posterior distribution | 30 | taught | MA-018 |
| potential function | 223 | out-of-scope | cv-special: MRF potential (not the gradient potential of MA-062) |
| potentials |  | out-of-scope | cv-special: MRF potentials |
| potentials, convex | 296 | out-of-scope | cv-special: MRF potentials |
| potentials, non-convex | 297 | out-of-scope | cv-special: MRF potentials |
| Potts model | 298, 319 | out-of-scope | cv-special: MRF smoothness prior |
| PPCA | 476–479 | out-of-scope | ml-zoo: probabilistic PCA |
| PPCA, learning parameters | 477 | out-of-scope | ml-zoo: probabilistic PCA |
| prediction step | 539 | taught | RO 78 |
| predictive distribution | 49 | add | `bayesian-fitting`: Bayesian fitting (maths; MA 08-likelihood (new Note after MA-072)) |
| preprocessing | 133, 325–351 | taught | RO 227 |
| Prewitt operators | 329 | taught | RO 227 (gradient filters) |
| principal component analysis | 348 | taught | ML-047 |
| principal component analysis, dual PCA | 349 | out-of-scope | ml-zoo: dual PCA |
| principal component analysis, probabilistic | 122, 476–479 | out-of-scope | ml-zoo: probabilistic PCA |
| principal direction problem | 624 | taught | ML-047 (direction of largest spread) |
| principal point | 360 | taught | RO 88 |
| prior | 30 | taught | MA-018 |
| probabilistic latent semantic analysis | 595 | out-of-scope | ml-zoo: text topic model |
| probabilistic linear discriminant analysis | 514–517 | out-of-scope | app: face recognition (biometrics) |
| probabilistic principal component analysis | 122, 140, 476–479 | out-of-scope | ml-zoo: probabilistic PCA |
| probabilistic principal component analysis, learning parameters | 477 | out-of-scope | ml-zoo: probabilistic PCA |
| probability |  | taught | MA-011 |
| probability, conditional | 28 | taught | MA-015 |
| probability, joint | 26 | taught | MA-014 |
| probability, marginal | 27 | taught | MA-014 |
| probability density function | 25 | taught | MA-022 |
| probability distribution | 35–45 | taught | MA-020 |
| probability distribution, fitting | 49–65 | taught | MA-070 |
| probe face | 512 | out-of-scope | app: face recognition (biometrics) |
| Procrustes analysis |  | taught | RO 92 |
| Procrustes analysis, generalized | 472–473 | out-of-scope | app: shape-model alignment (biometrics, medical) |
| Procrustes problem | 374, 625 | taught | RO 92 |
| product of experts | 223 | out-of-scope | ml-zoo: product of experts |
| projective camera | 359 | taught | RO 88 |
| projective pinhole camera | 359 | taught | RO 88 |
| projective reconstruction | 377 | out-of-scope | cv-special: projective reconstruction (uncalibrated cameras) |
| projective transformation | 395–396 | taught | RO 229 |
| projective transformation, fitting | 400–402 | taught | RO 229; RO 89 (DLT) |
| projective transformation, properties | 407–409 | taught | RO 229 |
| propose, expand and re-learn | 415, 420 | out-of-scope | research-only: the book's robust-fitting algorithm |
| prototype vector | 349 | taught | ML-122 (cluster centre) |
| pruning graphical models | 265, 270 | out-of-scope | cv-special: pruning graphical models |
| quadri-focal tensor | 444 | out-of-scope | cv-special: four-view tensor |
| quadric | 492 | out-of-scope | app: body-shape primitives (graphics) |
| quadric, truncated | 493 | out-of-scope | app: body-shape primitives (graphics) |
| Quasi-Newton methods | 608 | taught | MA-064 |
| quaternion | 610 | taught | new MA: 3D rotations: Euler angles and quaternions |
| radial basis function | 151, 191 | taught | ML-089 |
| radial distortion | 365 | taught | RO 89 |
| random classification tree | 198–200 | taught | ML-102 |
| random forest | 200 | taught | ML-102 |
| random sample consensus | 411–413, 420 | taught | RO 229 |
| random sample consensus, sequential | 413–414 | out-of-scope | variant of a taught method (RANSAC, RO 229) beyond beginner depth |
| random variable | 25 | taught | MA-020 |
| random variable, continuous | 25 | taught | MA-020 |
| random variable, discrete | 25 | taught | MA-020 |
| random variable, domain of | 35 | taught | MA-020 |
| rank of matrix | 620 | taught | MA-052; MA-058 |
| RANSAC | 411–413, 420 | taught | RO 229 |
| RANSAC, sequential | 413–414 | out-of-scope | variant of a taught method (RANSAC, RO 229) beyond beginner depth |
| Rao-Blackwellization | 562 | taught | RO 266 |
| reconstruction | 359, 369–370, 376–377 | taught | RO 233; RO 235 |
| reconstruction, from structured light | 378–380 | taught | RO 90 |
| reconstruction, multi-view | 443, 453 | taught | RO 235 |
| reconstruction, projective | 377 | out-of-scope | cv-special: projective reconstruction (uncalibrated cameras) |
| reconstruction, two view | 435 | taught | RO 233 |
| reconstruction error | 346 | out-of-scope | ml-zoo: the reconstruction-error view of PCA; no robotics Note needs it (PCA itself is ML-047) |
| reconstruction pipeline | 447–449, 453 | taught | RO 235 |
| rectification | 267, 439, 453 | taught | RO 90 |
| rectification, planar | 439 | taught | RO 90 |
| rectification, polar | 443 | out-of-scope | cv-special: rectification variant; rectification is RO 90 |
| region descriptor | 341–344 | taught | RO 228 |
| region descriptor, bag of words | 344–345 | taught | RO 236 |
| region descriptor, histogram | 341–342 | taught | RO 228 |
| region descriptor, HOG | 343–344 | out-of-scope | hand-designed detector feature; the plan's detectors are learned (RO 173-174) |
| region descriptor, SIFT | 342–343 | taught | RO 228 |
| regression | 83, 143–169 | taught | ML-003 |
| regression, Bayesian linear | 147–150 | add | `bayesian-fitting`: Bayesian fitting (maths; MA 08-likelihood (new Note after MA-072)) |
| regression, dual | 161–163 | out-of-scope | ml-zoo: dual regression |
| regression, Gaussian process | 156, 169 | taught | new ML: Gaussian processes |
| regression, linear | 86, 143–145 | taught | ML-049 |
| regression, linear, limitations of | 145–146 | taught | ML-055 |
| regression, nonlinear | 150 | taught | ML-060 |
| regression, nonlinear, Bayesian | 153 | add | `bayesian-fitting`: Bayesian fitting (maths; MA 08-likelihood (new Note after MA-072)) |
| regression, polynomial | 150 | taught | ML-060 |
| regression, relevance vector | 163–165 | out-of-scope | ml-zoo: relevance vector machine |
| regression, sparse | 157 | taught | ML-067 (sparsity) |
| regression, to multivariate data | 165 | out-of-scope | ml-zoo: multi-output regression detail |
| relative orientation | 431, 453 | taught | RO 233 (relative pose) |
| relevance vector |  | index-noise | heading |
| relevance vector, classification | 186–190 | out-of-scope | ml-zoo: relevance vector machine |
| relevance vector, regression | 163–165 | out-of-scope | ml-zoo: relevance vector machine |
| reparameterization |  | index-noise | heading |
| reparameterization, for optimization | 609 | out-of-scope | parameterisation trick beyond beginner depth |
| reparameterization, in graph cuts | 290–291 | out-of-scope | cv-special: graph cuts |
| reparameterization, multi-label case | 296 | out-of-scope | cv-special: graph cuts |
| reprojection error | 424 | taught | RO 233 |
| resection-intersection | 446 | out-of-scope | cv-special: alternating SfM scheme; the plan teaches bundle adjustment (RO 235) |
| responsibility | 111 | taught | MA-073 |
| robust density modeling | 115–120 | out-of-scope | ml-zoo: t-distribution density models |
| robust learning | 410, 420 | taught | RO 229; RO 235 |
| robust learning, PEaRL | 415 | out-of-scope | research-only: the book's robust-fitting algorithm |
| robust learning, RANSAC | 411–413 | taught | RO 229 |
| robust learning, sequential RANSAC | 413–414 | out-of-scope | variant of a taught method (RANSAC, RO 229) beyond beginner depth |
| robust mixture model | 126 | out-of-scope | ml-zoo: robust mixtures |
| robust subspace model | 126 | out-of-scope | ml-zoo: robust subspace models |
| rotation matrix | 616 | taught | RO 65 |
| rotation matrix, optimization over | 610 | add | `lie-groups`: Matrix Lie groups SO(3)/SE(3) for estimation (maths; MA 05-linear-algebra (new Note after the planned axis-angle Note); used by RO 87, RO 101, RO 235) |
| rotation of camera | 408 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)). a rotating camera gives a homography |
| sampling |  | taught | new MA: Drawing samples from distributions |
| sampling, ancestral | 232 | add | `bayes-networks`: Probabilistic graphical models (maths; MA 02-probability (new Note after MA-019)) |
| sampling, directed models | 232 | add | `bayes-networks`: Probabilistic graphical models (maths; MA 02-probability (new Note after MA-019)) |
| sampling, Gibbs | 233 | out-of-scope | MCMC; the plan samples with particle filters and importance sampling (RO 82) |
| sampling, undirected models | 233 | out-of-scope | cv-special: sampling MRFs |
| sampling from posterior | 231 | taught | RO 82 |
| scalar product | 613 | taught | MA-050 |
| scale invariant feature transform | 339–343 | taught | RO 228 |
| SCAPE | 496–497 | out-of-scope | app: human body shape model (graphics) |
| scene model | 590 | out-of-scope | app: scene classification |
| scene recognition | 571 | out-of-scope | app: scene classification; place recognition is RO 236 |
| Schur complement | 627 | taught | new MA: Schur complement |
| segmentation | 135–136, 140, 272, 461, 463–468 | taught | RO 175 |
| segmentation, supervised | 305–307 | out-of-scope | app: interactive photo segmentation |
| semantic segmentation | 203–205, 210 | taught | RO 175 |
| sequential RANSAC | 413–414 | out-of-scope | variant of a taught method (RANSAC, RO 229) beyond beginner depth |
| seven point algorithm | 436 | out-of-scope | cv-special: minimal solver for F; the plan teaches the 8-point algorithm (RO 232) |
| shape | 461 | index-noise | heading |
| shape, alignment | 472–473 | out-of-scope | app: statistical shape models (biometrics, medical) |
| shape, definition | 462 | out-of-scope | app: statistical shape models (biometrics, medical) |
| shape, statistical model | 471–482 | out-of-scope | app: statistical shape models (biometrics, medical) |
| shape and appearance models | 482–487 | out-of-scope | app: shape and appearance models (biometrics, medical) |
| shape context descriptor | 166, 345 | out-of-scope | cv-special: shape-matching descriptor |
| shape from silhouette | 380–383, 385 | out-of-scope | cv-special: visual hull reconstruction |
| shape model |  | index-noise | heading |
| shape model, 3D | 482 | out-of-scope | app: statistical shape models |
| shape model, articulated | 492–493 | out-of-scope | app: articulated shape models |
| shape model, non-Gaussian | 487–491 | out-of-scope | app: statistical shape models |
| shape model, subspace | 475 | out-of-scope | app: statistical shape models |
| shape template | 468, 469 | out-of-scope | cv-special: template matching of shapes |
| Sherman-Morrison-Woodbury relation | 148, 628 | taught | new MA: Woodbury identity |
| shift map image editing | 308–309 | out-of-scope | app: image editing |
| SIFT | 416 | taught | RO 228 |
| SIFT, descriptor | 342–343, 352 | taught | RO 228 |
| SIFT, detector | 339–341 | taught | RO 228 |
| sign language interpretation | 243, 246, 267 | out-of-scope | app: sign-language recognition |
| silhouette |  | index-noise | heading |
| silhouette, shape from | 380–383 | out-of-scope | cv-special: visual hull reconstruction |
| similarity transformation | 392 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)) |
| similarity transformation, learning | 399 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)) |
| simultaneous localization and mapping | 564, 567 | taught | RO 100 |
| single author-topic model | 582–585 | out-of-scope | ml-zoo: text topic model |
| singular matrix | 615 | taught | MA-056 |
| singular value decomposition | 618–620 | taught | MA-057; MA-058 |
| singular values | 619 | taught | MA-057 |
| skew (camera parameter) | 364 | add | `pinhole-geometry-terms`: Pinhole geometry terms (vision; RO-03 (section in 88)). skew in K |
| skew (moment) | 32 | taught | MA-026 |
| skin detection | 93–94, 97 | out-of-scope | app: skin-colour detection (biometrics) |
| SLAM | 564, 567 | taught | RO 100 |
| smoothing | 546–548 | add | `rts-smoother`: Batch estimation and smoothing (robotics; RO-22 (new Note after 257)) |
| smoothing, fixed interval | 547–548 | add | `rts-smoother`: Batch estimation and smoothing (robotics; RO-22 (new Note after 257)) |
| smoothing, fixed lag | 546–547 | add | `rts-smoother`: Batch estimation and smoothing (robotics; RO-22 (new Note after 257)) |
| snake | 272–273, 275, 463–468, 499 | out-of-scope | cv-special: snakes (active contours) |
| Sobel operator | 329 | taught | RO 227 (gradient filters) |
| softmax function | 197 | taught | ML-078 |
| sparse classification model | 186–190 | out-of-scope | ml-zoo: relevance vector machine |
| sparse linear regression | 157 | taught | ML-067 |
| sparse stereo vision | 359 | taught | RO 233 (triangulating matched features) |
| sparsity | 157, 164, 187, 190 | taught | ML-067 |
| spherical covariance matrix | 69 | taught | MA-073 |
| square matrix | 614 | taught | MA-053 |
| squared reprojection error | 424 | taught | RO 233 |
| statistical shape model | 471–482 | out-of-scope | app: statistical shape models |
| steepest descent | 603–604 | taught | ML-056 |
| step function | 193 | taught | DL-004 |
| stereo reconstruction | 369–370, 376–377 | taught | RO 90; RO 233 |
| stereo vision | 267–270, 274, 307–308, 317 | taught | RO 90 |
| stereo vision, dense | 267–270 | taught | RO 90 |
| stereo vision, dynamic programming | 274 | taught | RO 90 (matching along rows) |
| stereo vision, graph cuts formulation | 307–308 | out-of-scope | cv-special: stereo by graph cuts |
| stereo vision, sparse | 359 | taught | RO 233 |
| strong classifier | 194 | taught | ML-109 |
| structure from motion | 423, 444 | taught | RO 235 |
| structured light | 379, 385 | taught | RO 90 |
| Student t-distribution | 115–120 | taught | MA-037 |
| style | 503 | out-of-scope | app: face style models |
| style / identity model | 503 | out-of-scope | app: face identity/style models |
| style / identity model, asymmetric bilinear | 518–524 | out-of-scope | app: face identity/style models |
| style / identity model, multi-factor GPLVM | 531–532 | out-of-scope | app: face identity/style models |
| style / identity model, multi-linear | 528 | out-of-scope | app: face identity/style models |
| style / identity model, nonlinear | 517–518 | out-of-scope | app: face identity/style models |
| style / identity model, PLDA | 514–517 | out-of-scope | app: face identity/style models |
| style / identity model, subspace identity model | 506–514 | out-of-scope | app: face identity/style models |
| style / identity model, symmetric bilinear | 524–528 | out-of-scope | app: face identity/style models |
| style translation | 524 | out-of-scope | app: style translation (graphics) |
| submodularity | 291, 296 | out-of-scope | cv-special: graph-cut theory |
| submodularity, multi-label case | 296 | out-of-scope | cv-special: graph-cut theory |
| subspace | 121 | taught | MA-058 (subspaces) |
| subspace identity model | 506–514 | out-of-scope | app: face identity models |
| subspace model | 120, 140, 475, 499, 503 | out-of-scope | ml-zoo: subspace density models (factor analysis family) |
| subspace model, bilinear asymmetric | 518–524 | out-of-scope | app: face identity models |
| subspace model, bilinear symmetric | 524–528 | out-of-scope | app: face identity models |
| subspace model, dual PCA | 349 | out-of-scope | ml-zoo: dual PCA |
| subspace model, factor analysis | 503 | out-of-scope | ml-zoo: factor analysis |
| subspace model, for face recognition | 533 | out-of-scope | app: face recognition |
| subspace model, multi-factor GPLVM | 531–532 | out-of-scope | ml-zoo: GP latent variable model |
| subspace model, multi-linear model | 528 | out-of-scope | app: multi-linear face models |
| subspace model, PLDA | 514–517 | out-of-scope | app: face recognition |
| subspace model, principal component analysis | 348 | taught | ML-047 |
| subspace model, subspace identity model | 506–514 | out-of-scope | app: face identity models |
| subspace model, subspace shape model | 475 | out-of-scope | app: statistical shape models |
| sum-product algorithm | 257–259, 275 | out-of-scope | message passing on loopy graphs; robot factor graphs are solved by least squares (RO 263) |
| sum-product algorithm, for chain model | 259 | add | `hmm-inference`: HMM inference (robotics; RO-02 (section after 79)) |
| sum-product algorithm, for tree model | 262 | out-of-scope | cv-special: inference on tree models |
| super-resolution | 310–311 | out-of-scope | app: image super-resolution |
| superpixel | 205 | out-of-scope | cv-special: superpixels |
| supervised segmentation | 305–307 | out-of-scope | app: interactive photo segmentation |
| support vector machine | 200, 209 | taught | ML-086 |
| surface layout recovery | 205–206 | out-of-scope | research-only: single-image surface layout |
| SVD | 618–620 | taught | MA-057 |
| SVM | 200 | taught | ML-086 |
| symmetric bilinear model | 524–528 | out-of-scope | app: face identity models |
| symmetric epipolar distance | 433 | out-of-scope | error-measure detail of fundamental-matrix fitting (cv-special) |
| t-distribution | 115–120, 140 | taught | MA-037 |
| t-distribution, mixture of | 126 | out-of-scope | ml-zoo: mixture of t-distributions |
| t-distribution, multivariate | 116 | out-of-scope | ml-zoo: multivariate t density models |
| t-distribution, univariate | 116 | taught | MA-037 |
| t-test | 66 | taught | MA-042 |
| temporal model | 537–568 | taught | RO 77 to RO 82 (temporal models) |
| tensor | 617 | taught | ML-010 |
| tensor, multiplication | 617 | out-of-scope | multi-linear algebra beyond beginner depth |
| TensorTextures | 530–531 | out-of-scope | app: graphics texture model |
| texton | 204, 334 | out-of-scope | cv-special: texture descriptor |
| textonboost | 203–205 | out-of-scope | cv-special: texture-based segmentation |
| texture synthesis | 311–314, 317 | out-of-scope | app: texture synthesis (graphics) |
| tied factor analysis | 519 | out-of-scope | app: face identity models |
| Tomasi-Kanade factorization | 445, 453, 455 | out-of-scope | cv-special: Tomasi-Kanade factorisation (affine cameras) |
| top-down approach | 461 | out-of-scope | book's taxonomy of segmentation strategies (book-specific) |
| topic | 576 | out-of-scope | ml-zoo: text topic model |
| trace of matrix | 615 | add | `matrix-trace`: Trace of a matrix (maths; MA 05-linear-algebra (section in MA-056)) |
| tracking | 537–568 | taught | RO 178 |
| tracking, pedestrian | 563–564 | taught | RO 178 |
| tracking, applications | 567 | index-noise | application pointer |
| tracking, condensation algorithm | 558–562 | taught | RO 82 |
| tracking, displacement expert | 167 | out-of-scope | app: head tracking regressor |
| tracking, features | 453 | taught | RO 230 |
| tracking, for augmented reality | 416–417 | out-of-scope | app: augmented reality |
| tracking, head position | 167 | out-of-scope | app: head tracking |
| tracking, particle filtering | 558–562 | taught | RO 82 |
| tracking, through clutter | 565 | taught | RO 259 (data association in clutter) |
| transformation | 389–415, 420 | taught | MA-053 |
| transformation, 2D | 389–396 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)) |
| transformation, affine | 393–394 | taught | MA-053 |
| transformation, application | 415–418 | index-noise | application pointer |
| transformation, between images | 407 | taught | RO 229 |
| transformation, Euclidean | 389–392 | taught | new MA: Rigid-body transforms and homogeneous coordinates |
| transformation, homography | 395–396 | taught | RO 229 |
| transformation, indexed by hidden variable | 138 | out-of-scope | ml-zoo: transformations as hidden variables |
| transformation, inference | 401 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)). applying and inverting a transform |
| transformation, inverting | 401 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)). inverting a transform |
| transformation, learning | 396 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)) |
| transformation, learning, affine | 399–400 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)) |
| transformation, learning, Euclidean | 398 | taught | RO 92 |
| transformation, learning, homography | 400–402 | taught | RO 229 |
| transformation, learning, projective | 400–402 | taught | RO 229 |
| transformation, learning, similarity | 399 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)) |
| transformation, linear | 617 | taught | MA-053 |
| transformation, projective | 395–396 | taught | RO 229 |
| transformation, robust learning | 410 | taught | RO 229 |
| transformation, similarity | 392 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)) |
| transpose | 615 | taught | MA-054 |
| tree model | 243 | out-of-scope | cv-special: tree-structured graphical models |
| tree model, learning | 262 | out-of-scope | cv-special: tree-structured graphical models |
| tree model, MAP inference | 251–254 | out-of-scope | cv-special: tree-structured graphical models |
| tree model, marginal posterior inference | 262 | out-of-scope | cv-special: tree-structured graphical models |
| tri-focal tensor | 444 | out-of-scope | cv-special: three-view tensor |
| triangulation | 370 | taught | RO 233 |
| truncating potentials | 300 | out-of-scope | cv-special: MRF potentials |
| trust-region methods | 608 | taught | RL 38; new MA short section: Levenberg-Marquardt |
| two-view geometry | 424 | taught | RO 232 |
| UKF | 554–558 | taught | RO 256 |
| unary term | 284, 304 | out-of-scope | cv-special: MRF unary terms |
| undirected graphical model | 223 | out-of-scope | cv-special: undirected models (MRFs) |
| undirected graphical model, chain | 245 | out-of-scope | cv-special: undirected chain models |
| undirected graphical model, conditional independence relations in | 224 | out-of-scope | cv-special: undirected models (MRFs) |
| undirected graphical model, learning | 235–238 | out-of-scope | cv-special: learning MRFs |
| undirected graphical model, Markov blanket | 224 | out-of-scope | cv-special: undirected models (MRFs) |
| undirected graphical model, sampling | 233 | out-of-scope | cv-special: sampling MRFs |
| univariate normal distribution | 35 | taught | MA-024 |
| unscented Kalman filter | 554–558 | taught | RO 256 |
| unsupervised object discovery | 581 | out-of-scope | research-only: unsupervised object discovery |
| variable elimination | 255 | out-of-scope | exact inference for discrete graphical models; robot factor graphs are solved by sparse least squares (RO 263) |
| variance | 32 | taught | MA-012 |
| vector | 613 | taught | MA-048 |
| vector, norm | 613 | taught | MA-049 |
| vector, product | 614 | taught | MA-050; new MA: Cross product and skew-symmetric matrix |
| Vertigo | 385 | out-of-scope | app: cinematography effect |
| Video Google | 591–592 | out-of-scope | named retrieval system; bag of words is RO 236 |
| virtual image | 359 | add | `pinhole-geometry-terms`: Pinhole geometry terms (vision; RO-03 (section in 88)). virtual image plane |
| visual hull | 381 | out-of-scope | cv-special: visual hull reconstruction |
| visual word | 344, 571 | taught | RO 236 |
| Viterbi algorithm | 248–251 | add | `hmm-inference`: HMM inference (robotics; RO-02 (section after 79)) |
| volumetric graph cuts | 450–452 | out-of-scope | cv-special: multi-view stereo by graph cuts |
| weak classifier | 194 | taught | ML-109 |
| weak perspective camera | 387 | out-of-scope | camera model for very distant scenes; robot cameras use the pinhole model (RO 88) |
| whitening | 325 | add | `point-operators`: Point operators (vision; RO-18 (section in 227)) |
| whitening transform | 77 | add | `whitening`: Whitening transform (maths; MA 05-linear-algebra (section in the planned Mahalanobis Note)) |
| within-individual variation | 507, 514 | out-of-scope | app: face recognition |
| Woodbury inversion identity | 148, 628 | taught | new MA: Woodbury identity |
| word | 344, 571 | taught | RO 236 |
| world state | 83 | taught | RO 63 (state) |

## Szeliski, Computer Vision: Algorithms and Applications, 1st ed. (free 2010 draft PDF from szeliski.org)

Source: Index of Szeliski, Computer Vision: Algorithms and Applications, 1st ed. (Sept 3 2010 draft), official free PDF szeliski.org/Book/drafts/SzeliskiBook_20100903_draft.pdf, book pp. 933-957. Replaces Szeliski 2nd ed (download form) and Torralba-Isola-Freeman online edition (no back index).

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| 3D Rotations [see Rotations] |  | index-noise | cross-reference |
| 3D alignment | 320 | taught | RO 92 (aligning 3D point sets, Kabsch / Procrustes) |
| 3D alignment, absolute orientation | 320, 588 | taught | RO 92 (aligning 3D point sets, Kabsch / Procrustes) |
| 3D alignment, orthogonal Procrustes | 320 | taught | RO 92 (aligning 3D point sets, Kabsch / Procrustes) |
| 3D photography | 613 | out-of-scope | app: 3D photography and video (graphics) |
| 3D video | 643 | out-of-scope | app: 3D photography and video (graphics) |
| Absolute orientation | 320, 588 | taught | RO 92 |
| Active appearance model (AAM) | 680 | out-of-scope | app: face fitting (biometrics) |
| Active contours | 270 | out-of-scope | cv-special: snakes (active contours), not used by any robotics Note |
| Active illumination | 585 | taught | RO 90; RO 91 (structured light, time of flight, LiDAR) |
| Active rangefinding | 585 | taught | RO 90; RO 91 (structured light, time of flight, LiDAR) |
| Active shape model (ASM) | 276, 680 | out-of-scope | app: face and organ shape fitting |
| Activity recognition | 610 | out-of-scope | app: video activity recognition |
| Adaptive smoothing | 127 | out-of-scope | cv-special: PDE-based edge-preserving smoothing beyond beginner depth |
| Affine transforms | 37, 40 | taught | MA-053 §7.3 (affine); the full 2D hierarchy is add 2d-transform-hierarchy |
| Affinities (segmentation) | 296 | out-of-scope | cv-special: affinity-based (normalised-cut) segmentation |
| Affinities (segmentation), normalizing | 297 | out-of-scope | cv-special: affinity-based (normalised-cut) segmentation |
| Algebraic multigrid | 288 | out-of-scope | advanced numerical solver (multigrid) beyond beginner depth |
| Algorithms |  | index-noise | heading |
| Algorithms, testing | viii | index-noise | pointer to the preface |
| Aliasing | 77, 476 | add | `sampling-aliasing`: Sampling theorem (Nyquist rate) and aliasing; anti-alias low-pass before downsampling (maths; MA 06-calculus (Note after the Fourier Note); used in RO 227 pyramids and RO-03 sensor rates) |
| Alignment [see Image alignment] |  | index-noise | cross-reference |
| Alpha |  | index-noise | heading |
| Alpha, opacity | 106 | out-of-scope | app: alpha matting and compositing (graphics) |
| Alpha, pre-multiplied | 106 | out-of-scope | app: alpha matting and compositing (graphics) |
| Alpha matte | 105 | out-of-scope | app: alpha matting and compositing (graphics) |
| Ambient illumination | 65 | out-of-scope | photometric image formation (graphics/optics); robots rely on brightness constancy (RO 230) |
| Analog to digital conversion (ADC) | 77 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)) |
| Anisotropic diffusion | 127 | out-of-scope | cv-special: PDE-based edge-preserving smoothing beyond beginner depth |
| Anisotropic filtering | 168 | out-of-scope | app: texture filtering for rendering (graphics) |
| Anti-aliasing filter | 78, 476 | add | `sampling-aliasing`: Sampling theorem (Nyquist rate) and aliasing; anti-alias low-pass before downsampling (maths; MA 06-calculus (Note after the Fourier Note); used in RO 227 pyramids and RO-03 sensor rates) |
| Aperture | 69 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)) |
| Aperture problem | 394 | add | `aperture-problem`: The aperture problem and normal flow (vision; RO 230 (section)) |
| Applications | 5 | index-noise | heading for the book's list of application pointers |
| Applications, 3D model reconstruction | 362, 371 | index-noise | application pointer; the method is judged under its own entry |
| Applications, 3D photography | 613 | index-noise | application pointer; the method is judged under its own entry |
| Applications, augmented reality | 326, 368 | index-noise | application pointer; the method is judged under its own entry |
| Applications, automotive safety | 5 | index-noise | application pointer; the method is judged under its own entry |
| Applications, background replacement | 558 | index-noise | application pointer; the method is judged under its own entry |
| Applications, biometrics | 668 | index-noise | application pointer; the method is judged under its own entry |
| Applications, colorization | 504 | index-noise | application pointer; the method is judged under its own entry |
| Applications, de-interlacing | 415 | index-noise | application pointer; the method is judged under its own entry |
| Applications, digital heritage | 590 | index-noise | application pointer; the method is judged under its own entry |
| Applications, document scanning | 432 | index-noise | application pointer; the method is judged under its own entry |
| Applications, edge editing | 249 | index-noise | application pointer; the method is judged under its own entry |
| Applications, facial animation | 603 | index-noise | application pointer; the method is judged under its own entry |
| Applications, flash photography | 494 | index-noise | application pointer; the method is judged under its own entry |
| Applications, frame interpolation | 418 | index-noise | application pointer; the method is judged under its own entry |
| Applications, gaze correction | 552 | index-noise | application pointer; the method is judged under its own entry |
| Applications, head tracking | 551 | index-noise | application pointer; the method is judged under its own entry |
| Applications, hole filling | 521 | index-noise | application pointer; the method is judged under its own entry |
| Applications, image restoration | 192 | index-noise | application pointer; the method is judged under its own entry |
| Applications, image search | 717 | index-noise | application pointer; the method is judged under its own entry |
| Applications, industrial | 7 | index-noise | application pointer; the method is judged under its own entry |
| Applications, intelligent photo editing | 709 | index-noise | application pointer; the method is judged under its own entry |
| Applications, Internet photos | 371 | index-noise | application pointer; the method is judged under its own entry |
| Applications, location recognition | 693 | index-noise | application pointer; the method is judged under its own entry |
| Applications, machine inspection | 5 | index-noise | application pointer; the method is judged under its own entry |
| Applications, match move | 368 | index-noise | application pointer; the method is judged under its own entry |
| Applications, medical imaging | 5, 304, 408 | index-noise | application pointer; the method is judged under its own entry |
| Applications, morphing | 173 | index-noise | application pointer; the method is judged under its own entry |
| Applications, mosaic-based video compression | 436 | index-noise | application pointer; the method is judged under its own entry |
| Applications, non-photorealistic rendering | 522 | index-noise | application pointer; the method is judged under its own entry |
| Applications, Optical character recognition (OCR) | 5 | index-noise | application pointer; the method is judged under its own entry |
| Applications, panography | 314 | index-noise | application pointer; the method is judged under its own entry |
| Applications, performance-driven animation | 237 | index-noise | application pointer; the method is judged under its own entry |
| Applications, photo pop-up | 710 | index-noise | application pointer; the method is judged under its own entry |
| Applications, Photo Tourism | 624 | index-noise | application pointer; the method is judged under its own entry |
| Applications, Photomontage | 459 | index-noise | application pointer; the method is judged under its own entry |
| Applications, planar pattern tracking | 326 | index-noise | application pointer; the method is judged under its own entry |
| Applications, rotoscoping | 282 | index-noise | application pointer; the method is judged under its own entry |
| Applications, scene completion | 709 | index-noise | application pointer; the method is judged under its own entry |
| Applications, scratch removal | 521 | index-noise | application pointer; the method is judged under its own entry |
| Applications, single view reconstruction | 331 | index-noise | application pointer; the method is judged under its own entry |
| Applications, tonal adjustment | 111 | index-noise | application pointer; the method is judged under its own entry |
| Applications, video denoising | 414 | index-noise | application pointer; the method is judged under its own entry |
| Applications, video stabilization | 401 | index-noise | application pointer; the method is judged under its own entry |
| Applications, video summarization | 436 | index-noise | application pointer; the method is judged under its own entry |
| Applications, video-based walkthroughs | 645 | index-noise | application pointer; the method is judged under its own entry |
| Applications, VideoMouse | 326 | index-noise | application pointer; the method is judged under its own entry |
| Applications, view morphing | 357 | index-noise | application pointer; the method is judged under its own entry |
| Applications, visual effects | 5 | index-noise | application pointer; the method is judged under its own entry |
| Applications, whiteboard scanning | 432 | index-noise | application pointer; the method is judged under its own entry |
| Applications, z-keying | 558 | index-noise | application pointer; the method is judged under its own entry |
| Arc length parameterization of a curve | 246 | taught | RO 121 (distance along the path s) |
| Architectural reconstruction | 598 | out-of-scope | app: architectural reconstruction |
| Area statistics | 132 | add | `binary-image-ops`: Binary image processing (vision; RO-18 (new Note after 227)). region (blob) statistics |
| Area statistics, mean (centroid) | 132 | add | `binary-image-ops`: Binary image processing (vision; RO-18 (new Note after 227)). region (blob) statistics |
| Area statistics, perimeter | 132 | add | `binary-image-ops`: Binary image processing (vision; RO-18 (new Note after 227)). region (blob) statistics |
| Area statistics, second moment (inertia) | 132 | add | `binary-image-ops`: Binary image processing (vision; RO-18 (new Note after 227)). region (blob) statistics |
| Aspect ratio | 52, 53 | taught | RO 88 (pixel aspect ratio in K) |
| Augmented reality | 326, 338, 368 | out-of-scope | app: augmented reality |
| Auto-calibration | 355 | out-of-scope | cv-special: self-calibration from uncalibrated views; robots calibrate with targets (RO 89) |
| Automatic gain control (AGC) | 76 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)) |
| Axis/angle representation of rotations | 41 | taught | new MA: Axis-angle, exponential and log maps of rotations |
| B-snake | 273 | out-of-scope | cv-special: spline snakes |
| B-spline | 171, 172, 250, 273, 279, 408 | add | `b-splines`: B-splines (robotics; RO-15 (section in 202)) |
| B-spline, cubic | 146 | add | `b-splines`: B-splines (robotics; RO-15 (section in 202)) |
| B-spline, multilevel | 592 | out-of-scope | cv-special: multilevel spline fitting for surfaces |
| B-spline, octree | 597 | out-of-scope | cv-special: multilevel spline fitting for surfaces |
| Background plate | 518 | out-of-scope | app: fixed-camera background modelling (surveillance) |
| Background subtraction (maintenance) | 606 | out-of-scope | app: fixed-camera background modelling (surveillance) |
| Bag of words (keypoints) | 697, 727 | taught | RO 236 |
| Bag of words (keypoints), distance metrics | 698 | add | `bow-retrieval`: Bag-of-words retrieval (vision; RO 236 (section)) |
| Band-pass filter | 118 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals). band-pass = keep a band of frequencies |
| Bartlett filter [see Bilinear kernel] |  | index-noise | cross-reference |
| Bayer pattern (RGB sensor mosaic) | 85 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)) |
| Bayer pattern (RGB sensor mosaic), demosaicing | 86, 502 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)) |
| Bayes’ rule | 141, 180, 762 | taught | MA-018 |
| Bayes’ rule, MAP (maximum a posteriori) estimate | 763 | taught | MA-072 |
| Bayes’ rule, posterior distribution | 762 | taught | MA-018 |
| Bayesian modeling | 180, 762 | taught | MA-018 |
| Bayesian modeling, MAP estimate | 180, 763 | taught | MA-072 |
| Bayesian modeling, matting | 510 | out-of-scope | app: matting (graphics) |
| Bayesian modeling, posterior distribution | 180, 762 | taught | MA-018 |
| Bayesian modeling, prior distribution | 180, 762 | taught | MA-018 |
| Bayesian modeling, uncertainty | 180 | taught | MA-018; RO 63 |
| Belief propagation (BP) | 185, 768 | out-of-scope | message passing on loopy graphs for image labelling (cv-special); robot factor graphs are solved by least squares (RO 263) |
| Belief propagation (BP), update rule | 769 | out-of-scope | message passing on loopy graphs for image labelling (cv-special); robot factor graphs are solved by least squares (RO 263) |
| Bias | 104, 386 | add | `point-operators`: Point operators (vision; RO-18 (section in 227)). gain and bias |
| Bidirectional Reflectance Distribution Func-tion [see BRDF] |  | index-noise | cross-reference |
| Bilateral filter | 125 | add | `nonlinear-image-filters`: Nonlinear image filters (vision; RO-18 (section in 227) or RO 90 depth-map cleanup) |
| Bilateral filter, joint | 496 | out-of-scope | cv-special: joint bilateral filtering |
| Bilateral filter, range kernel | 125 | add | `nonlinear-image-filters`: Nonlinear image filters (vision; RO-18 (section in 227) or RO 90 depth-map cleanup) |
| Bilateral filter, tone mapping | 489 | out-of-scope | app: tone mapping (computational photography) |
| Bilinear blending | 110 | add | `image-interpolation`: Image interpolation and warping (vision; RO-18 (section in 229) or RO 89 undistortion) |
| Bilinear kernel | 117 | add | `image-interpolation`: Image interpolation and warping (vision; RO-18 (section in 229) or RO 89 undistortion) |
| Biometrics | 668 | out-of-scope | app: biometrics |
| Bipartite problem | 364 | out-of-scope | cv-special: projective SfM detail |
| Blind image deconvolution | 498 | out-of-scope | cv-special: blind deconvolution |
| Block-based motion estimation |  | index-noise | heading |
| Block-based motion estimation, (block matching) | 387 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90) |
| Blocks world | 11 | out-of-scope | history |
| Blue screen matting | 106, 195, 507 | out-of-scope | app: matting (graphics) |
| Blur kernel | 69 | taught | DL-042 §4.2 (blur kernels) |
| Blur kernel, estimation | 476, 528 | out-of-scope | cv-special: blur-kernel estimation |
| Blur removal | 144, 197 | out-of-scope | cv-special: deblurring by deconvolution |
| Body color | 63 | out-of-scope | photometric image formation (graphics/optics) |
| Boltzmann distribution | 181, 763 | out-of-scope | cv-special: Gibbs distribution of an MRF |
| Boosting | 663 | taught | ML-113 |
| Boosting, AdaBoost algorithm | 665 | taught | ML-109 |
| Boosting, decision stump | 663 | taught | ML-109 (decision stumps) |
| Boosting, weak learner | 663 | taught | ML-109 |
| Border (boundary) effects | 114, 196 | taught | DL-043 (padding and border pixels) |
| Boundary detection | 244 | add | `edge-detection`: Edge detection (vision; RO-18 (section in 227)). boundary detection |
| Box filter | 117 | taught | DL-042 §4.2 (box blur) |
| Boxlet | 121 | out-of-scope | cv-special: fast filtering trick |
| BRDF | 62 | out-of-scope | photometric image formation: reflectance models (graphics/optics) |
| BRDF, anisotropic | 62 | out-of-scope | photometric image formation: reflectance models (graphics/optics) |
| BRDF, isotropic | 62 | out-of-scope | photometric image formation: reflectance models (graphics/optics) |
| BRDF, recovery | 612 | out-of-scope | photometric image formation: reflectance models (graphics/optics) |
| BRDF, spatially varying (SVBRDF) | 612 | out-of-scope | photometric image formation: reflectance models (graphics/optics) |
| Brightness | 104 | add | `point-operators`: Point operators (vision; RO-18 (section in 227)). brightness adjustment |
| Brightness constancy | 3, 384 | taught | RO 230 |
| Brightness constancy constraint | 384, 393, 410 | taught | RO 230 |
| Bundle adjustment | 363 | taught | RO 235 |
| Calibration [see Camera calibration] |  | index-noise | cross-reference |
| Calibration matrix | 51 | taught | RO 88 |
| Camera calibration | 50, 97 | taught | RO 89 |
| Camera calibration, accuracy | 340 | out-of-scope | calibration evaluation detail beyond beginner depth |
| Camera calibration, aliasing | 476 | out-of-scope | cv-special: optical-blur calibration |
| Camera calibration, extrinsic | 51, 321 | taught | RO 89; RO 93 |
| Camera calibration, intrinsic | 50, 327 | taught | RO 89 |
| Camera calibration, optical blur | 476, 528 | out-of-scope | cv-special: optical-blur calibration |
| Camera calibration, patterns | 327 | taught | RO 89 (calibration targets) |
| Camera calibration, photometric | 470 | out-of-scope | cv-special: radiometric calibration |
| Camera calibration, plumb-line method | 335, 341 | out-of-scope | alternative distortion-calibration method; the plan teaches target calibration (RO 89) |
| Camera calibration, point spread function | 476, 528 | out-of-scope | cv-special: point-spread-function calibration |
| Camera calibration, radial distortion | 334 | taught | RO 89 |
| Camera calibration, radiometric | 470, 481, 526 | out-of-scope | cv-special: radiometric calibration |
| Camera calibration, rotational motion | 332, 339 | out-of-scope | cv-special: calibration from a rotating camera |
| Camera calibration, slant edge | 476 | out-of-scope | cv-special: slanted-edge blur calibration |
| Camera calibration, vanishing points | 329 | add | `projective-points-lines`: Points and lines in homogeneous coordinates (vision; RO-03 (section in 88)). vanishing points |
| Camera calibration, vignetting | 474 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)). vignetting |
| Camera matrix | 51, 54 | taught | RO 88 |
| Catadioptric optics | 71 | out-of-scope | mirror-lens cameras; RO 89 teaches fisheye and spherical models |
| Category-level recognition | 696 | taught | RO 173; DL-049 |
| Category-level recognition, bag of words | 697, 727 | taught | RO 236 |
| Category-level recognition, data sets | 718 | index-noise | pointer to data sets |
| Category-level recognition, part-based | 701 | out-of-scope | research-only: part-based recognition |
| Category-level recognition, segmentation | 704 | taught | RO 175 |
| Category-level recognition, surveys | 723 | index-noise | pointer to surveys |
| CCD | 74 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)) |
| CCD, blooming | 74 | out-of-scope | sensor artefact detail (blooming) |
| Central difference | 118 | taught | MA-061 (central difference) |
| Chained transformations | 325, 364 | taught | MA-054; RO 65 (chaining transforms) |
| Chamfer matching | 129 | out-of-scope | cv-special: chamfer matching |
| Characteristic function | 131, 281, 590, 596 | index-noise | notation (indicator function) |
| Characteristic polynomial | 740 | taught | MA-056 |
| Chirality | 347, 351 | taught | RO 233 (point in front of both cameras: four-solution check) |
| Cholesky factorization | 741 | taught | new MA: Cholesky factor |
| Cholesky factorization, algorithm | 741 | taught | new MA: Cholesky factor |
| Cholesky factorization, incomplete | 752 | out-of-scope | numerical preconditioner (incomplete Cholesky) beyond beginner depth |
| Cholesky factorization, sparse | 749 | taught | new MA: Sparse linear solves and conjugate gradient |
| Chromatic aberration | 71, 342 | out-of-scope | lens optics detail (chromatic aberration) |
| Chromaticity coordinates | 83 | add | `color-spaces`: Colour spaces (vision; RO-18 (section in 227)) |
| CIE L*a*b* [see Color] |  | index-noise | cross-reference |
| CIE L*u*v* [see Color] |  | index-noise | cross-reference |
| CIE XYZ [see Color] |  | index-noise | cross-reference |
| Circle of confusion | 69 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)). depth of field |
| CLAHE [see Histogram equalization] |  | index-noise | cross-reference |
| Clustering |  | taught | ML-122 |
| Clustering, agglomerative | 286 | taught | ML-125 |
| Clustering, cluster analysis | 269, 305 | taught | ML-122 |
| Clustering, divisive | 286 | taught | ML-125 |
| CMOS | 74 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)) |
| Co-vector | 37 | taught | MA-055 (duality) |
| Coefficient matrix | 177 | taught | ML-053 |
| Collineation | 40 | taught | RO 229 (collineation = homography) |
| Color | 80 | add | `color-spaces`: Colour spaces (vision; RO-18 (section in 227)) |
| Color, balance | 86, 97, 194 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)) |
| Color, camera | 84 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)) |
| Color, demosaicing | 86, 502 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)) |
| Color, fringing | 504 | out-of-scope | sensor artefact detail (colour fringing) |
| Color, hue, saturation, value (HSV) | 90 | add | `color-spaces`: Colour spaces (vision; RO-18 (section in 227)) |
| Color, L*a*b* | 83 | add | `color-spaces`: Colour spaces (vision; RO-18 (section in 227)) |
| Color, L*u*v* | 84, 289 | add | `color-spaces`: Colour spaces (vision; RO-18 (section in 227)) |
| Color, primaries | 81 | out-of-scope | colour science (different field) |
| Color, profile | 473 | out-of-scope | colour management (different field) |
| Color, ratios | 90 | out-of-scope | cv-special: colour ratios |
| Color, RGB | 81 | taught | DL-042 §3.2 (RGB images) |
| Color, transform | 104 | add | `color-spaces`: Colour spaces (vision; RO-18 (section in 227)) |
| Color, twist | 86, 105 | out-of-scope | colour science (different field) |
| Color, XYZ | 81 | out-of-scope | colour science (different field) |
| Color, YIQ | 88 | out-of-scope | video-broadcast colour format (different field) |
| Color, YUV | 88 | add | `color-spaces`: Colour spaces (vision; RO-18 (section in 227)). YUV is the format many robot cameras stream |
| Color filter array (CFA) | 85, 502 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)) |
| Color line model | 513 | out-of-scope | cv-special: matting colour model |
| ColorChecker chart | 473 | out-of-scope | app: colour calibration chart (photography) |
| Colorization | 504 | out-of-scope | app: colorisation (graphics) |
| Compositing | 105, 192, 195 | out-of-scope | app: compositing (graphics) |
| Compositing, image stitching | 450 | out-of-scope | app: compositing (graphics) |
| Compositing, opacity | 106 | out-of-scope | app: compositing (graphics) |
| Compositing, over operator | 106 | out-of-scope | app: compositing (graphics) |
| Compositing, surface | 451 | out-of-scope | app: compositing (graphics) |
| Compositing, transparency | 106 | out-of-scope | app: compositing (graphics) |
| Compression | 90 | out-of-scope | app: image compression |
| Computational photography | 467 | out-of-scope | app: computational photography |
| Computational photography, active illumination | 496 | out-of-scope | app: computational photography |
| Computational photography, flash and non-flash | 494 | out-of-scope | app: computational photography |
| Computational photography, high dynamic range | 479 | out-of-scope | app: computational photography |
| Computational photography, references | 469, 524 | out-of-scope | app: computational photography |
| Computational photography, tone mapping | 487 | out-of-scope | app: computational photography |
| Concentric mosaic | 437, 634 | out-of-scope | app: concentric mosaics (graphics) |
| CONDENSATION | 279 | taught | RO 82 |
| Condition number | 750 | taught | MA-058 |
| Conditional random field (CRF) | 188, 553, 708 | out-of-scope | cv-special: conditional random fields for image labelling |
| Confusion matrix (table) | 226 | taught | ML-075 |
| Conic section | 33 | out-of-scope | cv-special: projective geometry of conics |
| Conjugate gradient descent (CG) | 749 | taught | new MA: Sparse linear solves and conjugate gradient |
| Conjugate gradient descent (CG), algorithm | 751 | taught | new MA: Sparse linear solves and conjugate gradient |
| Conjugate gradient descent (CG), non-linear | 750 | out-of-scope | numerical-optimisation variant beyond beginner depth |
| Conjugate gradient descent (CG), preconditioned | 751 | out-of-scope | numerical-optimisation variant beyond beginner depth |
| Connected components | 131, 198 | add | `binary-image-ops`: Binary image processing (vision; RO-18 (new Note after 227)). connected components |
| Constellation model | 704 | out-of-scope | research-only: part-based recognition |
| Content based image retrieval (CBIR) | 717 | out-of-scope | app: image search; place recognition is RO 236 |
| Continuation method | 179 | out-of-scope | numerical continuation method beyond beginner depth |
| Contour |  | index-noise | heading |
| Contour, arc length parameterization | 246 | taught | RO 121 |
| Contour, chain code | 246 | out-of-scope | cv-special: contour coding, matching and smoothing |
| Contour, matching | 248, 263 | out-of-scope | cv-special: contour coding, matching and smoothing |
| Contour, smoothing | 248 | out-of-scope | cv-special: contour coding, matching and smoothing |
| Contrast | 104 | add | `point-operators`: Point operators (vision; RO-18 (section in 227)). contrast adjustment |
| Controlled-continuity spline | 175 | out-of-scope | cv-special: controlled-continuity splines |
| Convolution | 112 | taught | DL-042 |
| Convolution, kernel | 111 | taught | DL-042 |
| Convolution, mask | 111 | taught | DL-042 |
| Convolution, superposition | 112 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals). superposition = linearity of filtering |
| Coring | 153, 201 | out-of-scope | cv-special: wavelet coring |
| Correlation | 111, 386 | taught | DL-042 §Extra (cross-correlation, G-508) |
| Correlation, windowed | 390 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90) |
| Correspondence map | 398 | taught | RO 231 (dense flow field) |
| Cramer–Rao lower bound | 320, 397, 775 | out-of-scope | estimation-theory lower bound taught in graduate estimation courses, not in robotics or control courses at beginner depth |
| Cube map |  | index-noise | heading |
| Cube map, Hough transform | 253 | out-of-scope | cv-special: Hough-space parameterisation detail |
| Cube map, image stitching | 451 | out-of-scope | app: panorama projection (graphics) |
| Curve |  | index-noise | heading |
| Curve, arc length parameterization | 246 | taught | RO 121 |
| Curve, evolution | 248 | out-of-scope | cv-special: curve evolution and matching |
| Curve, matching | 248 | out-of-scope | cv-special: curve evolution and matching |
| Curve, smoothing | 248 | out-of-scope | cv-special: curve evolution and matching |
| Cylindrical coordinates | 438 | out-of-scope | app: cylindrical panoramas (graphics) |
| Data energy (term) | 181, 763 | out-of-scope | cv-special: data term of an MRF energy |
| Data sets and test databases | 778 | index-noise | pointer to data sets |
| Data sets and test databases, recognition | 718 | index-noise | pointer to data sets |
| De-interlacing | 415 | out-of-scope | app: video de-interlacing |
| Decimation | 148 | taught | RO 227 (pyramids: downsampling) |
| Decimation kernels |  | index-noise | heading |
| Decimation kernels, bicubic | 150 | out-of-scope | choice-of-kernel detail for downsampling beyond beginner depth |
| Decimation kernels, binomial | 148, 150 | out-of-scope | choice-of-kernel detail for downsampling beyond beginner depth |
| Decimation kernels, QMF | 150 | out-of-scope | choice-of-kernel detail for downsampling beyond beginner depth |
| Decimation kernels, windowed sinc | 148 | out-of-scope | choice-of-kernel detail for downsampling beyond beginner depth |
| Demosaicing (Bayer) | 86, 502 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)) |
| Depth from defocus | 584 | out-of-scope | cv-special: depth from defocus |
| Depth map [see Disparity map] |  | index-noise | cross-reference |
| Depth of field | 69, 95 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)). depth of field |
| Di-chromatic reflection model | 67 | out-of-scope | photometric image formation: reflectance models (graphics/optics) |
| Difference matting (keying) | 106, 195, 508, 606 | out-of-scope | app: matting (graphics) |
| Difference of Gaussians (DoG) | 152 | add | `image-laplacian-log`: Second-derivative image filters (vision; RO-18 (section in 227, before SIFT in 228)). DoG approximates the Laplacian of Gaussian |
| Difference of low-pass (DOLP) | 152 | add | `image-laplacian-log`: Second-derivative image filters (vision; RO-18 (section in 227, before SIFT in 228)). difference of low-pass = Laplacian pyramid band |
| Diffuse reflection | 63 | out-of-scope | photometric image formation: reflectance models (graphics/optics) |
| Diffusion |  | index-noise | heading |
| Diffusion, anisotropic | 127 | out-of-scope | cv-special: PDE-based edge-preserving smoothing beyond beginner depth |
| Digital camera | 73 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)) |
| Digital camera, color | 84 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)) |
| Digital camera, color filter array (CFA) | 85 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)) |
| Digital camera, compression | 90 | out-of-scope | app: image compression |
| Direct current (DC) | 92 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals). DC = zero frequency |
| Direct linear transform (DLT) | 322 | taught | RO 89 |
| Direct sparse matrix techniques | 747 | taught | new MA: Sparse linear solves and conjugate gradient |
| Directional derivative | 119 | taught | MA-062 |
| Directional derivative, selectivity | 120 | out-of-scope | cv-special: steerable filters |
| Discrete cosine transform (DCT) | 91, 142 | out-of-scope | app: image compression (DCT) |
| Discrete Fourier transform (DFT) | 134 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals) |
| Discriminative random field (DRF) | 190 | out-of-scope | cv-special: discriminative random fields |
| Disparity | 49, 539 | taught | RO 90 |
| Disparity map | 540, 562 | taught | RO 90 |
| Disparity map, multiple | 561 | out-of-scope | cv-special: multi-view disparity maps |
| Disparity space image (DSI) | 540 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90) |
| Disparity space image (DSI), generalized | 542 | out-of-scope | cv-special: generalised disparity space |
| Displaced frame difference (DFD) | 384 | taught | RO 230; RO 234 (brightness difference = photometric error) |
| Displacement field | 170 | taught | RO 231 (dense flow field) |
| Distance from face space (DFFS) | 672 | out-of-scope | app: face recognition (biometrics) |
| Distance in face space (DIFS) | 672 | out-of-scope | app: face recognition (biometrics) |
| Distance map [see Distance transform] |  | index-noise | cross-reference |
| Distance transform | 129, 198 | add | `distance-transform`: Distance transform of a grid (robotics; RO-04 (section in 98, inflation layer)) |
| Distance transform, Euclidean | 129 | add | `distance-transform`: Distance transform of a grid (robotics; RO-04 (section in 98, inflation layer)) |
| Distance transform, image stitching | 455 | out-of-scope | app: image stitching seams |
| Distance transform, Manhattan (city block) | 129 | add | `distance-transform`: Distance transform of a grid (robotics; RO-04 (section in 98, inflation layer)) |
| Distance transform, signed | 130 | add | `distance-transform`: Distance transform of a grid (robotics; RO-04 (section in 98, inflation layer)) |
| Domain (of a function) | 103 | taught | MA-061 (domain of a function) |
| Domain scaling law | 167 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals). scaling a signal shrinks its spectrum |
| Downsampling [see Decimation] |  | index-noise | cross-reference |
| Dynamic programming (DP) | 554, 766 | taught | RL 12 to RL 14; RO 205 |
| Dynamic programming (DP), monotonicity | 556 | out-of-scope | stereo-matching constraint detail beyond beginner depth |
| Dynamic programming (DP), ordering constraint | 556 | out-of-scope | stereo-matching constraint detail beyond beginner depth |
| Dynamic programming (DP), scanline optimization | 556 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90) |
| Dynamic snake | 276 | out-of-scope | cv-special: dynamic snakes |
| Dynamic texture | 642 | out-of-scope | app: dynamic texture (graphics) |
| Earth mover’s distance (EMD) | 698 | out-of-scope | cv-special: earth mover's distance for histograms |
| Edge detection | 238, 261 | add | `edge-detection`: Edge detection (vision; RO-18 (section in 227)) |
| Edge detection, boundary detection | 244 | add | `edge-detection`: Edge detection (vision; RO-18 (section in 227)) |
| Edge detection, Canny | 239 | add | `edge-detection`: Edge detection (vision; RO-18 (section in 227)) |
| Edge detection, chain code | 246 | out-of-scope | cv-special: chain-code contour coding |
| Edge detection, color | 243 | out-of-scope | colour-edge detail beyond beginner depth |
| Edge detection, Difference of Gaussian | 240 | add | `image-laplacian-log`: Second-derivative image filters (vision; RO-18 (section in 227, before SIFT in 228)) |
| Edge detection, edgel (edge element) | 241 | add | `edge-detection`: Edge detection (vision; RO-18 (section in 227)) |
| Edge detection, hysteresis | 246 | add | `edge-detection`: Edge detection (vision; RO-18 (section in 227)) |
| Edge detection, Laplacian of Gaussian | 240 | add | `image-laplacian-log`: Second-derivative image filters (vision; RO-18 (section in 227, before SIFT in 228)) |
| Edge detection, linking | 244, 262 | add | `edge-detection`: Edge detection (vision; RO-18 (section in 227)). edge linking |
| Edge detection, marching cubes | 241 | out-of-scope | app: surface extraction (graphics) |
| Edge detection, scale selection | 242 | taught | RO 228 (scale space) |
| Edge detection, steerable filter | 241 | out-of-scope | cv-special: steerable filters |
| Edge detection, zero crossing | 241 | add | `image-laplacian-log`: Second-derivative image filters (vision; RO-18 (section in 227, before SIFT in 228)). edges at zero crossings of the LoG |
| Eigenface | 671 | out-of-scope | app: face recognition (biometrics) |
| Eigenvalue decomposition | 275, 671, 737 | taught | MA-056 |
| Eigenvector | 737 | taught | MA-056 |
| Elastic deformations | 408 | out-of-scope | cv-special: elastic image registration |
| Elastic deformations, image registration | 408 | out-of-scope | cv-special: elastic image registration |
| Elastic nets | 272 | out-of-scope | cv-special: elastic-net contour model (not the regression of ML-068) |
| Elliptical weighted average (EWA) | 168 | out-of-scope | app: texture filtering for rendering (graphics) |
| Environment map | 61, 633 | out-of-scope | app: environment mapping (graphics) |
| Environment matte | 634 | out-of-scope | app: environment mapping (graphics) |
| Epanechnikov kernel | 294 | out-of-scope | cv-special: mean-shift kernel |
| Epipolar constraint | 348 | taught | RO 232 |
| Epipolar geometry | 348, 537 | taught | RO 232 |
| Epipolar geometry, pure rotation | 353 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)). a purely rotating camera gives a homography |
| Epipolar geometry, pure translation | 352 | out-of-scope | special-case epipolar geometry detail beyond beginner depth |
| Epipolar line | 537 | taught | RO 232 |
| Epipolar plane | 537, 544 | taught | RO 232 |
| Epipolar plane, image (EPI) | 559, 629 | out-of-scope | cv-special: epipolar-plane images (light fields) |
| Epipolar volume | 629 | out-of-scope | cv-special: epipolar-plane images (light fields) |
| Epipole | 348, 537 | taught | RO 232 |
| Error rates |  | index-noise | heading |
| Error rates, accuracy (ACC) | 229 | taught | ML-075 |
| Error rates, false negative (FN) | 226 | taught | ML-075 |
| Error rates, false positive (FP) | 226 | taught | ML-075 |
| Error rates, positive predictive value (PPV) | 229 | taught | ML-076 |
| Error rates, precision | 229 | taught | ML-076 |
| Error rates, recall | 229 | taught | ML-076 |
| Error rates, ROC curve | 229 | taught | ML-077 |
| Error rates, true negative (TN) | 226 | taught | ML-075 |
| Error rates, true positive (TP) | 226 | taught | ML-075 |
| Errors-in-variable model | 442, 744 | taught | RO 92 (plane fitting by the smallest eigenvector = total least squares) |
| Errors-in-variable model, heteroscedastic | 746 | out-of-scope | noise-model detail (heteroscedastic) beyond beginner depth |
| Essential matrix | 348 | taught | RO 232 |
| Essential matrix, 5-point algorithm | 352 | taught | RO 232 (5-point, concept only) |
| Essential matrix, eight-point algorithm | 349 | taught | RO 232 |
| Essential matrix, re-normalization | 350 | out-of-scope | numerical-conditioning detail of E estimation |
| Essential matrix, seven-point algorithm | 350 | out-of-scope | cv-special: minimal solver for F; the plan teaches the 8-point algorithm (RO 232) |
| Essential matrix, twisted pair | 351 | taught | RO 233 (four-solution check) |
| Estimation theory | 757 | taught | MA-070; RO 78 |
| Euclidean transformation | 36, 40 | taught | new MA: Rigid-body transforms and homogeneous coordinates |
| Euler angles | 41 | taught | new MA: 3D rotations: Euler angles and quaternions |
| Expectation maximization (EM) | 291 | taught | MA-074 |
| Exponential twist | 43 | taught | RB 275 (exponential coordinates of a rigid motion) |
| Exposure bracketing | 480 | out-of-scope | app: HDR photography |
| Exposure value (EV) | 70, 470 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)) |
| F-number (stop) | 69, 95 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)) |
| Face detection | 658 | out-of-scope | app: face detection, recognition and animation (biometrics, graphics) |
| Face detection, boosting | 663 | out-of-scope | app: face detection, recognition and animation (biometrics, graphics) |
| Face detection, cascade of classifiers | 664 | out-of-scope | app: face detection, recognition and animation (biometrics, graphics) |
| Face detection, clustering and PCA | 660 | out-of-scope | app: face detection, recognition and animation (biometrics, graphics) |
| Face detection, data sets | 718 | out-of-scope | app: face detection, recognition and animation (biometrics, graphics) |
| Face detection, neural networks | 661 | out-of-scope | app: face detection, recognition and animation (biometrics, graphics) |
| Face detection, support vector machines | 662 | out-of-scope | app: face detection, recognition and animation (biometrics, graphics) |
| Face modeling | 601 | out-of-scope | app: face detection, recognition and animation (biometrics, graphics) |
| Face recognition | 668 | out-of-scope | app: face detection, recognition and animation (biometrics, graphics) |
| Face recognition, active appearance model | 680 | out-of-scope | app: face detection, recognition and animation (biometrics, graphics) |
| Face recognition, data sets | 718 | out-of-scope | app: face detection, recognition and animation (biometrics, graphics) |
| Face recognition, eigenface | 671 | out-of-scope | app: face detection, recognition and animation (biometrics, graphics) |
| Face recognition, elastic bunch graph matching | 679 | out-of-scope | app: face detection, recognition and animation (biometrics, graphics) |
| Face recognition, local binary patterns (LBP) | 722 | out-of-scope | app: face detection, recognition and animation (biometrics, graphics) |
| Face recognition, local feature analysis | 679 | out-of-scope | app: face detection, recognition and animation (biometrics, graphics) |
| Face transfer | 639 | out-of-scope | app: face detection, recognition and animation (biometrics, graphics) |
| Facial motion capture | 603, 605, 639 | out-of-scope | app: face detection, recognition and animation (biometrics, graphics) |
| Factor graph | 181, 764, 768 | taught | RO 263 |
| Factorization | 15, 357 | out-of-scope | cv-special: factorisation SfM |
| Factorization, missing data | 360 | out-of-scope | cv-special: factorisation SfM |
| Factorization, projective | 360 | out-of-scope | cv-special: factorisation SfM |
| Fast Fourier transform (FFT) | 134 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals) |
| Fast marching method (FMM) | 282 | taught | RO 106 (wavefront propagation) |
| Feature descriptor | 222, 260 | taught | RO 228 |
| Feature descriptor, bias and gain normalization | 222 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90) |
| Feature descriptor, GLOH | 223 | out-of-scope | cv-special: descriptor variant (GLOH) |
| Feature descriptor, patch | 222 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90) |
| Feature descriptor, PCA-SIFT | 223 | out-of-scope | cv-special: descriptor variant (PCA-SIFT) |
| Feature descriptor, performance (evaluation) | 224 | out-of-scope | benchmarking detail |
| Feature descriptor, quantization | 234, 691, 698 | taught | RO 236 (visual words) |
| Feature descriptor, SIFT | 223 | taught | RO 228 |
| Feature descriptor, steerable filter | 224 | out-of-scope | cv-special: steerable filters |
| Feature detection | 207, 209, 259 | taught | RO 227 |
| Feature detection, Adaptive non-maximal suppression | 215 | out-of-scope | detector detail (adaptive non-maximal suppression) |
| Feature detection, affine invariance | 219 | out-of-scope | cv-special: affine-invariant detectors |
| Feature detection, auto-correlation | 210 | taught | RO 227 (Harris from the auto-correlation surface) |
| Feature detection, Förstner | 212 | out-of-scope | cv-special: Förstner operator |
| Feature detection, Harris | 212 | taught | RO 227 |
| Feature detection, Laplacian of Gaussian | 217 | add | `image-laplacian-log`: Second-derivative image filters (vision; RO-18 (section in 227, before SIFT in 228)) |
| Feature detection, MSER | 220 | out-of-scope | cv-special: MSER regions |
| Feature detection, region | 221 | out-of-scope | cv-special: region detectors |
| Feature detection, repeatability | 215 | taught | RO 227 (corners are easy to find again) |
| Feature detection, rotation invariance | 218 | taught | RO 228 |
| Feature detection, scale invariance | 216 | taught | RO 228 |
| Feature matching | 207, 225, 261 | taught | RO 228 |
| Feature matching, densification | 234 | out-of-scope | cv-special: match densification |
| Feature matching, efficiency | 232 | taught | RO 92; RO 108 (k-d trees) |
| Feature matching, error rates | 226 | taught | ML-075 (TP/FP counts) |
| Feature matching, hashing | 232 | out-of-scope | cv-special: hashing for matching |
| Feature matching, indexing structure | 232 | taught | RO 92; RO 108 (k-d trees) |
| Feature matching, k-d trees | 233 | taught | RO 92; RO 108 (k-d trees) |
| Feature matching, locality sensitive hashing | 233 | out-of-scope | cv-special: locality-sensitive hashing |
| Feature matching, nearest neighbor | 229 | taught | RO 228 (nearest neighbour, ratio test) |
| Feature matching, strategy | 226 | taught | RO 228 (nearest neighbour, ratio test) |
| Feature matching, verification | 234 | taught | RO 229 (RANSAC verification) |
| Feature tracking | 235, 261 | taught | RO 230 |
| Feature tracking, affine | 235 | out-of-scope | tracker detail (affine patch check) |
| Feature tracking, learning | 236 | out-of-scope | research-only: learned trackers |
| Feature tracks | 357, 371 | taught | RO 234; RO 235 |
| Feature-based alignment | 311 | taught | RO 229 |
| Feature-based alignment, 2D | 311 | taught | RO 229 |
| Feature-based alignment, 3D | 320 | taught | RO 92 |
| Feature-based alignment, iterative | 315 | taught | new MA: Nonlinear least squares (Gauss-Newton) |
| Feature-based alignment, Jacobian | 312 | taught | MA-063 |
| Feature-based alignment, least squares | 312 | taught | ML-050 |
| Feature-based alignment, match verification | 686 | taught | RO 229 |
| Feature-based alignment, RANSAC | 318 | taught | RO 229 |
| Feature-based alignment, robust | 318 | taught | RO 229; RO 235 |
| Field of Experts (FoE) | 186 | out-of-scope | research-only: learned image priors |
| Fill factor | 75 | out-of-scope | sensor detail (fill factor) |
| Fill-in | 366, 748 | out-of-scope | numerical detail of sparse factorisation |
| Filter |  | taught | DL-042 |
| Filter, adaptive | 127 | out-of-scope | cv-special: adaptive smoothing |
| Filter, band-pass | 118 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals) |
| Filter, bilateral | 125 | add | `nonlinear-image-filters`: Nonlinear image filters (vision; RO-18 (section in 227) or RO 90 depth-map cleanup) |
| Filter, directional derivative | 119 | taught | RO 227 |
| Filter, edge-preserving | 124, 127 | add | `nonlinear-image-filters`: Nonlinear image filters (vision; RO-18 (section in 227) or RO 90 depth-map cleanup) |
| Filter, Laplacian of Gaussian | 119 | add | `image-laplacian-log`: Second-derivative image filters (vision; RO-18 (section in 227, before SIFT in 228)) |
| Filter, median | 124 | add | `nonlinear-image-filters`: Nonlinear image filters (vision; RO-18 (section in 227) or RO 90 depth-map cleanup) |
| Filter, moving average | 117 | taught | DL-042 §4.1 (moving average) |
| Filter, non-linear | 122 | add | `nonlinear-image-filters`: Nonlinear image filters (vision; RO-18 (section in 227) or RO 90 depth-map cleanup) |
| Filter, separable | 115, 197 | add | `separable-filters`: Separable filters (vision; RO-18 (section in 227)) |
| Filter, steerable | 119, 198 | out-of-scope | cv-special: steerable filters |
| Filter coefficients | 111 | taught | DL-042 |
| Filter kernel [see Kernel] |  | index-noise | cross-reference |
| Finding faces [see Face detection] |  | index-noise | cross-reference |
| Finite element analysis | 176 | out-of-scope | different field: finite-element mechanics |
| Finite element analysis, stiffness matrix | 177 | out-of-scope | different field: finite-element mechanics |
| Finite impulse response (FIR) filter | 111, 122 | add | `digital-filters`: Discrete-time signal filters (control; RO-03 (section in 83 or 86)) |
| Fisher information matrix | 313, 320, 758, 775 | taught | RL 38 (Fisher information) |
| Fisher’s linear discriminant (FLD) | 676 | out-of-scope | ml-zoo: Fisher's linear discriminant, no robotics Note needs it |
| Fisheye lens | 59 | taught | RO 89 (fisheye) |
| Flash and non-flash merging | 494 | out-of-scope | app: computational photography and animation |
| Flash matting | 517 | out-of-scope | app: computational photography and animation |
| Flip-book animation | 336 | out-of-scope | app: computational photography and animation |
| Flying spot scanner | 587 | out-of-scope | hardware history (flying-spot scanner) |
| Focal length | 52, 53, 69 | taught | RO 88 |
| Focus | 69 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)). focus |
| Focus, shape-from | 584, 616 | out-of-scope | cv-special: shape from focus |
| Focus of expansion (FOE) | 352 | taught | RO 231 (ego-motion from flow: focus of expansion) |
| Form factor | 68 | out-of-scope | graphics: radiosity form factor |
| Forward mapping [see Forward warping] |  | index-noise | cross-reference |
| Forward warping | 164, 202 | add | `image-interpolation`: Image interpolation and warping (vision; RO-18 (section in 229) or RO 89 undistortion). forward warping |
| Fourier transform | 132, 198 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals) |
| Fourier transform, discrete | 134 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals) |
| Fourier transform, examples | 136 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals) |
| Fourier transform, magnitude (gain) | 133 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals) |
| Fourier transform, pairs | 136 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals) |
| Fourier transform, Parseval’s Theorem | 136 | out-of-scope | property used in derivations (proof technique) |
| Fourier transform, phase (shift) | 133 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals) |
| Fourier transform, power spectrum | 140 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals) |
| Fourier transform, properties | 134 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals) |
| Fourier transform, two-dimensional | 140 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals) |
| Fourier-based motion estimation | 388 | out-of-scope | cv-special: phase-correlation motion estimation |
| Fourier-based motion estimation, rotations and scale | 391 | out-of-scope | cv-special: phase-correlation motion estimation |
| Frame interpolation | 418 | out-of-scope | app: video interpolation and free-viewpoint video |
| Free-viewpoint video | 644 | out-of-scope | app: video interpolation and free-viewpoint video |
| Fundamental matrix | 353 | taught | RO 232 |
| Fundamental matrix, estimation [see Essential matrix] |  | index-noise | cross-reference |
| Fundamental radiometric relation | 73 | out-of-scope | photometric image formation (optics) |
| Gain | 104, 386 | add | `point-operators`: Point operators (vision; RO-18 (section in 227)). gain |
| Gamma | 104 | add | `point-operators`: Point operators (vision; RO-18 (section in 227)). gamma correction |
| Gamma correction | 87, 96 | add | `point-operators`: Point operators (vision; RO-18 (section in 227)). gamma correction |
| Gap closing (image stitching) | 435 | out-of-scope | app: stitching and matting |
| Garbage matte | 518 | out-of-scope | app: stitching and matting |
| Gaussian kernel | 117 | taught | DL-042 §4.2 (Gaussian blur); MA-023 (Gaussian kernel) |
| Gaussian Markov random field (GMRF) | 184, 191, 499 | out-of-scope | cv-special: Gaussian MRF |
| Gaussian mixtures [see Mixture of Gaussians] |  | index-noise | cross-reference (Gaussian mixtures are MA-073) |
| Geometry image | 594 | out-of-scope | app: geometry images (graphics) |
| Gaussian pyramid | 150 | taught | RO 227 |
| Gaussian scale mixtures (GSM) | 186 | out-of-scope | research-only: image-prior model |
| Gaze correction | 552 | out-of-scope | app: gaze correction |
| Geman–McClure function | 385 | out-of-scope | one more robust loss beyond the Huber and Cauchy losses that RO 235 lists (variant) |
| Generalized cylinders | 12, 588, 593 | out-of-scope | history: early shape representation |
| Geodesic active contour | 282 | out-of-scope | cv-special: geodesic segmentation |
| Geodesic distance (segmentation) | 304 | out-of-scope | cv-special: geodesic segmentation |
| Geometric image formation | 31 | taught | RO 88 |
| Geometric lens aberrations | 70 | taught | RO 89 (lens distortion) |
| Geometric primitives | 32 | index-noise | heading |
| Geometric primitives, homogeneous coordinates | 32 | taught | new MA: Rigid-body transforms and homogeneous coordinates; RO 88 |
| Geometric primitives, lines | 32, 34 | add | `projective-points-lines`: Points and lines in homogeneous coordinates (vision; RO-03 (section in 88)) |
| Geometric primitives, normal vector | 32 | taught | MA-051 (normal of a hyperplane); RO 92 (normals) |
| Geometric primitives, normal vectors | 34 | taught | MA-051 (normal of a hyperplane); RO 92 (normals) |
| Geometric primitives, planes | 33 | taught | MA-051; RO 92 (plane fitting) |
| Geometric primitives, points | 32, 33 | taught | new MA short section: Projective homogeneous coordinates |
| Geometric transformations |  | index-noise | heading |
| Geometric transformations, 2D | 35, 163 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)) |
| Geometric transformations, 3D | 39 | taught | new MA: Rigid-body transforms and homogeneous coordinates |
| Geometric transformations, 3D perspective | 40 | out-of-scope | cv-special: 3D projective transforms |
| Geometric transformations, 3D rotations | 41 | taught | new MA: 3D rotations: Euler angles and quaternions |
| Geometric transformations, affine | 37, 40 | taught | MA-053 §7.3 |
| Geometric transformations, bilinear | 39 | out-of-scope | cv-special: bilinear warp |
| Geometric transformations, calibration matrix | 51 | taught | RO 88 |
| Geometric transformations, collineation | 40 | taught | RO 229 |
| Geometric transformations, Euclidean | 36, 40 | taught | new MA: Rigid-body transforms and homogeneous coordinates |
| Geometric transformations, forward warping | 164, 202 | add | `image-interpolation`: Image interpolation and warping (vision; RO-18 (section in 229) or RO 89 undistortion). forward warping |
| Geometric transformations, hierarchy | 37 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)) |
| Geometric transformations, homography | 37, 40, 56, 431 | taught | RO 229 |
| Geometric transformations, inverse warping | 165 | add | `image-interpolation`: Image interpolation and warping (vision; RO-18 (section in 229) or RO 89 undistortion). inverse warping |
| Geometric transformations, perspective | 37 | taught | RO 229 |
| Geometric transformations, projections | 46 | taught | RO 88 |
| Geometric transformations, projective | 37 | taught | RO 229 |
| Geometric transformations, rigid body | 36, 40 | taught | new MA: Rigid-body transforms and homogeneous coordinates |
| Geometric transformations, scaled rotation | 36, 40 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)) |
| Geometric transformations, similarity | 36, 40 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)) |
| Geometric transformations, translation | 36, 39 | taught | new MA: Rigid-body transforms and homogeneous coordinates |
| Gesture recognition | 605 | out-of-scope | app: gesture recognition |
| Gibbs distribution | 181, 763 | out-of-scope | cv-special: Gibbs distribution of an MRF |
| Gibbs sampler | 765 | out-of-scope | MCMC; the plan samples with particle filters and importance sampling (RO 82) |
| Gimbal lock | 41 | add | `rotation-matrix-properties`: Rotation representations (maths; MA 05-linear-algebra (section in the planned 3D rotations Note)). gimbal lock of Euler angles |
| Gist (of a scene) | 709, 714 | out-of-scope | app: scene gist |
| Global illumination | 67 | out-of-scope | graphics: global illumination |
| Global optimization | 174 | out-of-scope | cv-special: regularisation-based global energy methods |
| GPU algorithms | 789 | index-noise | pointer to GPU implementations |
| Gradient location-orientation histogram (GLOH) | 223 | out-of-scope | cv-special: descriptor variant (GLOH) |
| Graduated non-convexity (GNC) | 179 | out-of-scope | research-level optimisation strategy (graduated non-convexity) |
| Graph cuts |  | index-noise | heading |
| Graph cuts, MRF inference | 183, 770 | out-of-scope | cv-special: graph-cut and graph-based segmentation |
| Graph cuts, normalized cuts | 296 | out-of-scope | cv-special: graph-cut and graph-based segmentation |
| Graph-based segmentation | 286 | out-of-scope | cv-special: graph-cut and graph-based segmentation |
| Grassfire transform | 130, 248, 455 | add | `distance-transform`: Distance transform of a grid (robotics; RO-04 (section in 98, inflation layer)). grassfire = distance transform |
| Ground control points | 350, 429 | taught | RO 233 (pose from known 3D points) |
| Hammersley–Clifford theorem | 181, 763 | out-of-scope | theorem used in proofs about MRFs (proof technique) |
| Hann window | 138 | out-of-scope | windowing detail of spectral analysis |
| Harris corner detector [see Feature detection] |  | index-noise | cross-reference |
| Head tracking | 551 | out-of-scope | app: head tracking |
| Head tracking, active appearance model (AAM) | 680 | out-of-scope | app: head tracking |
| Helmholtz reciprocity | 62 | out-of-scope | optics: Helmholtz reciprocity |
| Hessian | 177, 213, 313, 315, 320, 394, 399, 743 | taught | MA-064 |
| Hessian, eigenvalues | 397 | taught | MA-064 |
| Hessian, image | 394, 411 | taught | RO 230 (Lucas-Kanade normal equations / structure tensor) |
| Hessian, inverse | 320, 397, 401 | taught | MA-064 §Extra (covariance from the inverse Hessian, Laplace approximation) |
| Hessian, local | 410 | out-of-scope | alignment detail beyond beginner depth |
| Hessian, patch-based | 400 | out-of-scope | alignment detail beyond beginner depth |
| Hessian, rank-deficient | 370 | out-of-scope | cv-special: gauge freedom in SfM |
| Hessian, reduced motion | 366 | taught | RO 235 (sparsity, Schur complement) |
| Hessian, sparse | 366, 379, 747 | taught | RO 235 (sparsity, Schur complement) |
| Heteroscedastic | 313, 746 | out-of-scope | noise-model detail (heteroscedastic) beyond beginner depth |
| Hidden Markov model (HMM) | 642 | taught | RO 77 |
| Hierarchical motion estimation | 387 | taught | RO 230 (pyramidal KLT) |
| High dynamic range (HDR) imaging | 479 | out-of-scope | app: HDR photography |
| High dynamic range (HDR) imaging, formats | 486 | out-of-scope | app: HDR photography |
| High dynamic range (HDR) imaging, tone mapping | 487 | out-of-scope | app: HDR photography |
| Highest confidence first | 765 | out-of-scope | cv-special: MRF inference heuristic |
| Highest confidence first (HCF) | 182 | out-of-scope | cv-special: MRF inference heuristic |
| Hilbert transform pair | 120 | out-of-scope | cv-special: quadrature filter pairs |
| Histogram equalization | 107, 196 | add | `point-operators`: Point operators (vision; RO-18 (section in 227)). histogram equalisation |
| Histogram equalization, locally adaptive | 109, 196 | add | `point-operators`: Point operators (vision; RO-18 (section in 227)). histogram equalisation |
| Histogram intersection | 698 | out-of-scope | cv-special: histogram distance for retrieval |
| Histogram of oriented gradients (HOG) | 666 | out-of-scope | hand-designed detector feature; the plan's detectors are learned (RO 173-174) |
| History of computer vision | 10 | out-of-scope | history |
| Hole filling | 521 | out-of-scope | app: hole filling (image editing) |
| Homogeneous coordinates | 32, 347 | taught | RO 88; new MA short section: Projective homogeneous coordinates |
| Homography | 37, 56, 431 | taught | RO 229 |
| Hough transform | 251, 264 | add | `hough-transform`: Hough transform for lines (and circles) (vision; RO-18 (section in 229, next to RANSAC)) |
| Hough transform, cascaded | 253 | out-of-scope | Hough-transform implementation detail |
| Hough transform, cube map | 253 | out-of-scope | Hough-transform implementation detail |
| Hough transform, generalized | 251 | out-of-scope | cv-special: generalised Hough transform |
| Human body shape modeling | 609 | out-of-scope | app: human body shape modelling (graphics) |
| Human motion tracking | 605 | taught | RB 317 (human motion data) |
| Human motion tracking, activity recognition | 610 | out-of-scope | app: video-based human tracking details |
| Human motion tracking, adaptive shape modeling | 609 | out-of-scope | app: video-based human tracking details |
| Human motion tracking, background subtraction | 606 | out-of-scope | app: video-based human tracking details |
| Human motion tracking, flow-based | 607 | out-of-scope | app: video-based human tracking details |
| Human motion tracking, initialization | 607 | out-of-scope | app: video-based human tracking details |
| Human motion tracking, kinematic models | 607 | taught | RO 69 (kinematic chains) |
| Human motion tracking, particle filtering | 608 | taught | RO 82 |
| Human motion tracking, probabilistic models | 608 | out-of-scope | app: video-based human tracking details |
| Hyper-Laplacian | 179, 184, 186 | out-of-scope | research-only: image priors |
| Ideal points | 32 | add | `projective-points-lines`: Points and lines in homogeneous coordinates (vision; RO-03 (section in 88)). ideal point = point at infinity |
| Ill-posed (ill-conditioned) problems | 175 | taught | MA-058 (condition number); ML-062 (regularisation) |
| Illusions | 3 | out-of-scope | perception psychology (different field) |
| Image alignment |  | index-noise | heading |
| Image alignment, feature-based | 311, 543 | taught | RO 229 |
| Image alignment, intensity-based | 384 | taught | RO 230; RO 234 (direct vs feature-based) |
| Image alignment, intensity-based vs. feature-based | 450 | taught | RO 230; RO 234 (direct vs feature-based) |
| Image analogies | 522 | out-of-scope | app: image analogies (graphics) |
| Image blending |  | index-noise | heading |
| Image blending, feathering | 455 | out-of-scope | app: image blending (graphics) |
| Image blending, GIST | 461 | out-of-scope | app: image blending (graphics) |
| Image blending, gradient domain | 459 | out-of-scope | app: image blending (graphics) |
| Image blending, image stitching | 453 | out-of-scope | app: image blending (graphics) |
| Image blending, Poisson | 460 | out-of-scope | app: image blending (graphics) |
| Image blending, pyramid | 160, 459 | out-of-scope | app: image blending (graphics) |
| Image compositing [see Compositing] |  | index-noise | cross-reference |
| Image compression | 90 | out-of-scope | app: image compression |
| Image decimation | 148 | taught | RO 227 (pyramid downsampling) |
| Image deconvolution [see Blur removal] |  | index-noise | cross-reference |
| Image filtering | 111 | taught | RO 227 |
| Image formation |  | index-noise | heading |
| Image formation, geometric | 31 | taught | RO 88 |
| Image formation, photometric | 60 | out-of-scope | photometric image formation (graphics/optics); robots rely on brightness constancy (RO 230) |
| Image gradient | 119, 127, 392 | taught | RO 227 |
| Image gradient, constraint | 177 | out-of-scope | regularisation detail of variational methods (cv-special) |
| Image interpolation | 145 | add | `image-interpolation`: Image interpolation and warping (vision; RO-18 (section in 229) or RO 89 undistortion) |
| Image matting | 505, 529 | out-of-scope | app: matting (graphics) |
| Image processing | 101 | taught | RO 227 |
| Image processing, textbooks | 101, 192 | index-noise | pointer to textbooks |
| Image pyramid | 144, 200 | taught | RO 227 |
| Image resampling | 163, 199 | add | `image-interpolation`: Image interpolation and warping (vision; RO-18 (section in 229) or RO 89 undistortion). resampling |
| Image resampling, test images | 200 | index-noise | pointer to test images |
| Image restoration | 144, 192 | out-of-scope | cv-special: image restoration (deblurring, deblocking) |
| Image restoration, blur removal | 144, 197, 199 | out-of-scope | cv-special: image restoration (deblurring, deblocking) |
| Image restoration, deblocking | 204 | out-of-scope | cv-special: image restoration (deblurring, deblocking) |
| Image restoration, inpainting | 192 | out-of-scope | app: inpainting (image editing) |
| Image restoration, noise removal | 144, 197, 203 | add | `nonlinear-image-filters`: Nonlinear image filters (vision; RO-18 (section in 227) or RO 90 depth-map cleanup). noise removal |
| Image restoration, using MRFs | 192 | out-of-scope | cv-special: MRF image restoration |
| Image search | 717 | out-of-scope | app: image search |
| Image segmentation [see Segmentation] |  | index-noise | cross-reference |
| Image sensing [see Sensing] |  | index-noise | cross-reference |
| Image statistics | 132 | add | `binary-image-ops`: Binary image processing (vision; RO-18 (new Note after 227)). region statistics |
| Image stitching | 427 | out-of-scope | app: panorama stitching (photography) |
| Image stitching, automatic | 446 | out-of-scope | app: panorama stitching (photography) |
| Image stitching, bundle adjustment | 441 | taught | RO 235 |
| Image stitching, compositing | 450 | out-of-scope | app: panorama stitching (photography) |
| Image stitching, coordinate transformations | 452 | out-of-scope | app: panorama stitching (photography) |
| Image stitching, cube map | 451 | out-of-scope | app: panorama stitching (photography) |
| Image stitching, cylindrical | 438, 463 | out-of-scope | app: panorama stitching (photography) |
| Image stitching, de-ghosting | 446, 456, 464 | out-of-scope | app: panorama stitching (photography) |
| Image stitching, direct vs. feature-based | 450 | taught | RO 234 (direct vs feature-based) |
| Image stitching, exposure compensation | 462 | out-of-scope | app: panorama stitching (photography) |
| Image stitching, feathering | 455 | out-of-scope | app: panorama stitching (photography) |
| Image stitching, gap closing | 435 | out-of-scope | app: panorama stitching (photography) |
| Image stitching, global alignment | 441 | out-of-scope | app: panorama stitching (photography) |
| Image stitching, homography | 431 | taught | RO 229 |
| Image stitching, motion models | 430 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)). choice of motion model |
| Image stitching, panography | 314 | out-of-scope | app: panorama stitching (photography) |
| Image stitching, parallax removal | 445 | out-of-scope | app: panorama stitching (photography) |
| Image stitching, photogrammetry | 429 | out-of-scope | app: panorama stitching (photography) |
| Image stitching, pixel selection | 453 | out-of-scope | app: panorama stitching (photography) |
| Image stitching, planar perspective motion | 431 | taught | RO 229 |
| Image stitching, recognizing panoramas | 446 | out-of-scope | app: panorama stitching (photography) |
| Image stitching, rotational motion | 433 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)). a rotating camera gives a homography |
| Image stitching, seam selection | 456 | out-of-scope | app: panorama stitching (photography) |
| Image stitching, spherical | 439 | out-of-scope | app: panorama stitching (photography) |
| Image stitching, up vector selection | 444 | out-of-scope | app: panorama stitching (photography) |
| Image warping | 163, 201, 388 | add | `image-interpolation`: Image interpolation and warping (vision; RO-18 (section in 229) or RO 89 undistortion). warping |
| Image-based modeling | 623 | out-of-scope | app: image-based modelling and rendering (graphics) |
| Image-based rendering | 619 | out-of-scope | app: image-based modelling and rendering (graphics) |
| Image-based rendering, concentric mosaic | 634 | out-of-scope | app: image-based modelling and rendering (graphics) |
| Image-based rendering, environment matte | 634 | out-of-scope | app: image-based modelling and rendering (graphics) |
| Image-based rendering, impostors | 626 | out-of-scope | app: image-based modelling and rendering (graphics) |
| Image-based rendering, layered depth image | 626 | out-of-scope | app: image-based modelling and rendering (graphics) |
| Image-based rendering, layers | 626 | out-of-scope | app: image-based modelling and rendering (graphics) |
| Image-based rendering, light field | 628 | out-of-scope | app: image-based modelling and rendering (graphics) |
| Image-based rendering, Lumigraph | 628 | out-of-scope | app: image-based modelling and rendering (graphics) |
| Image-based rendering, modeling vs. rendering continuum | 637 | out-of-scope | app: image-based modelling and rendering (graphics) |
| Image-based rendering, sprites | 626 | out-of-scope | app: image-based modelling and rendering (graphics) |
| Image-based rendering, surface light field | 632 | out-of-scope | app: image-based modelling and rendering (graphics) |
| Image-based rendering, unstructured Lumigraph | 632 | out-of-scope | app: image-based modelling and rendering (graphics) |
| Image-based rendering, view interpolation | 621 | out-of-scope | app: image-based modelling and rendering (graphics) |
| Image-based rendering, view-dependent texture maps | 623 | out-of-scope | app: image-based modelling and rendering (graphics) |
| Image-based visual hull | 569 | out-of-scope | app: image-based modelling and rendering (graphics) |
| ImageNet | 716 | taught | DL-051 |
| Implicit surface | 596 | taught | RO 97 (signed-distance maps) |
| Impostors [see Sprites] |  | index-noise | cross-reference |
| Impulse response | 112 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals). impulse response of a linear shift-invariant filter |
| Incremental refinement |  | index-noise | heading |
| Incremental refinement, motion estimation | 388, 392 | taught | RO 230 (iterative Lucas-Kanade) |
| Incremental rotation | 45 | add | `lie-groups`: Matrix Lie groups SO(3)/SE(3) for estimation (maths; MA 05-linear-algebra (new Note after the planned axis-angle Note); used by RO 87, RO 101, RO 235). small (incremental) rotation updates |
| Indexing structure | 232 | taught | RO 92; RO 108 (k-d trees) |
| Indicator function | 596 | index-noise | notation (indicator function) |
| Industrial applications | 7 | index-noise | application pointer |
| Infinite impulse response (IIR) filter | 122 | add | `digital-filters`: Discrete-time signal filters (control; RO-03 (section in 83 or 86)) |
| Influence function | 179, 318, 761 | taught | new MA short section: Levenberg-Marquardt and robust losses (IRLS weights) |
| Information matrix | 313, 320, 370, 758, 775 | taught | RO 257 |
| Inpainting | 521 | out-of-scope | app: inpainting (image editing) |
| Instance recognition | 685 | taught | RO 236 (recognising places by bag of words) |
| Instance recognition, algorithm | 690 | taught | RO 236 (recognising places by bag of words) |
| Instance recognition, data sets | 718 | index-noise | pointer to data sets |
| Instance recognition, geometric alignment | 686 | taught | RO 229 |
| Instance recognition, inverted index | 687 | add | `bow-retrieval`: Bag-of-words retrieval (vision; RO 236 (section)). inverted index |
| Instance recognition, large scale | 687 | out-of-scope | retrieval scaling detail |
| Instance recognition, match verification | 686 | taught | RO 229 |
| Instance recognition, query expansion | 692 | out-of-scope | retrieval detail (query expansion, stop lists) |
| Instance recognition, stop list | 689 | out-of-scope | retrieval detail (query expansion, stop lists) |
| Instance recognition, visual words | 688 | taught | RO 236 (visual words, vocabulary tree) |
| Instance recognition, vocabulary tree | 691 | add | `bow-retrieval`: Bag-of-words retrieval (vision; RO 236 (section)). vocabulary tree |
| Integrability constraint | 581 | out-of-scope | cv-special: shape from shading |
| Integral image | 120 | out-of-scope | cv-special: integral images for fast box sums |
| Integrating sphere | 472 | out-of-scope | optics lab equipment |
| Intelligent scissors | 280 | out-of-scope | app: interactive image cut-out |
| Interaction potential | 181, 763, 768 | out-of-scope | cv-special: MRF potentials |
| Interactive computer vision | 614 | out-of-scope | app: interactive vision |
| International Color Consortium (ICC) | 473 | out-of-scope | colour management (different field) |
| Internet photos | 371 | out-of-scope | app: internet photo collections |
| Interpolation | 145 | add | `image-interpolation`: Image interpolation and warping (vision; RO-18 (section in 229) or RO 89 undistortion) |
| Interpolation kernels |  | index-noise | heading |
| Interpolation kernels, bicubic | 146 | add | `image-interpolation`: Image interpolation and warping (vision; RO-18 (section in 229) or RO 89 undistortion) |
| Interpolation kernels, bilinear | 145 | add | `image-interpolation`: Image interpolation and warping (vision; RO-18 (section in 229) or RO 89 undistortion) |
| Interpolation kernels, binomial | 145 | out-of-scope | choice-of-kernel detail for interpolation beyond beginner depth |
| Interpolation kernels, sinc | 148 | out-of-scope | choice-of-kernel detail for interpolation beyond beginner depth |
| Interpolation kernels, spline | 148 | out-of-scope | choice-of-kernel detail for interpolation beyond beginner depth |
| Intrinsic camera calibration | 327 | taught | RO 89 |
| Intrinsic images | 12 | out-of-scope | cv-special: intrinsic images |
| Inverse kinematics (IK) | 607 | taught | RB 279 |
| Inverse mapping [see Inverse warping] |  | index-noise | cross-reference |
| Inverse problems | 3, 175 | out-of-scope | framing term from the book's introduction (book-specific) |
| Inverse warping | 165 | add | `image-interpolation`: Image interpolation and warping (vision; RO-18 (section in 229) or RO 89 undistortion). inverse warping |
| ISO setting | 76 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)). ISO gain |
| Iterated closest point (ICP) | 272, 321, 588 | taught | RO 92 |
| Iterated conditional modes (ICM) | 182, 765 | out-of-scope | cv-special: MRF inference heuristic |
| Iterative back projection (IBP) | 499 | out-of-scope | cv-special: super-resolution method |
| Iterative feature-based alignment | 315 | taught | new MA: Nonlinear least squares (Gauss-Newton) |
| Iterative sparse matrix techniques | 748 | taught | new MA: Sparse linear solves and conjugate gradient |
| Iterative sparse matrix techniques, conjugate gradient | 749 | taught | new MA: Sparse linear solves and conjugate gradient |
| Iteratively reweighted least squares |  | index-noise | heading |
| Iteratively reweighted least squares, (IRLS) | 318, 324, 398, 761 | taught | new MA short section: Levenberg-Marquardt and robust losses (IRLS) |
| Jacobian | 312, 325, 364, 392, 746 | taught | MA-063 |
| Jacobian, image | 394 | taught | RO 231 (image Jacobian) |
| Jacobian, motion | 399 | taught | RO 230 (warp Jacobian in Lucas-Kanade) |
| Jacobian, sparse | 366, 379, 747 | taught | RO 235 |
| Joint bilateral filter | 496 | out-of-scope | cv-special: joint bilateral filter, mean-shift feature space |
| Joint domain (feature space) | 294 | out-of-scope | cv-special: joint bilateral filter, mean-shift feature space |
| K-d trees | 233 | taught | RO 92 |
| K-means | 289 | taught | ML-122 |
| Kalman snakes | 276 | out-of-scope | cv-special: Kalman snakes |
| Kanade–Lucas–Tomasi (KLT) tracker | 235 | taught | RO 230 |
| Karhunen–Loève transform | 143, 671 | taught | ML-047 (KL transform = PCA) |
| Kernel | 117 | taught | DL-042 |
| Kernel, bilinear | 117 | add | `image-interpolation`: Image interpolation and warping (vision; RO-18 (section in 229) or RO 89 undistortion). bilinear (tent) kernel |
| Kernel, Gaussian | 117 | taught | DL-042 §4.2 |
| Kernel, low-pass | 117 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals). low-pass = keeps slow changes |
| Kernel, Sobel operator | 118 | taught | RO 227 |
| Kernel, unsharp mask | 117 | add | `image-laplacian-log`: Second-derivative image filters (vision; RO-18 (section in 227, before SIFT in 228)). unsharp masking sharpens by adding back the high-pass part |
| Kernel basis function | 176 | out-of-scope | cv-special: spline basis detail |
| Kernel density estimation | 292 | taught | MA-023 |
| Keypoint detection [see Feature detection] |  | index-noise | cross-reference |
| Kinematic model (chain) | 607 | taught | RO 69 |
| Kruppa equations | 356 | out-of-scope | cv-special: self-calibration equations |
| L*a*b* [see Color] |  | index-noise | cross-reference |
| L*u*v* [see Color] |  | index-noise | cross-reference |
| L 1 norm | 179, 385, 411, 597 | taught | ML-066 (L1 penalty) |
| L ∞ norm | 367 | out-of-scope | norm used only in the book's minimax SfM formulation |
| Lambertian reflection | 63 | out-of-scope | photometric image formation: reflectance models (graphics/optics) |
| Laplacian matting | 515 | out-of-scope | app: matting (graphics) |
| Laplacian of Gaussian (LoG) filter | 119 | add | `image-laplacian-log`: Second-derivative image filters (vision; RO-18 (section in 227, before SIFT in 228)) |
| Laplacian pyramid | 151 | add | `image-laplacian-log`: Second-derivative image filters (vision; RO-18 (section in 227, before SIFT in 228)). Laplacian pyramid = band-pass stack |
| Laplacian pyramid, blending | 160, 200, 459 | out-of-scope | app: image blending (graphics) |
| Laplacian pyramid, perfect reconstruction | 151 | add | `image-laplacian-log`: Second-derivative image filters (vision; RO-18 (section in 227, before SIFT in 228)) |
| Latent Dirichlet process (LDP) | 713 | out-of-scope | ml-zoo: topic model |
| Layered depth image (LDI) | 626 | out-of-scope | app: layered depth images (graphics) |
| Layered depth panorama | 634 | out-of-scope | app: layered depth images (graphics) |
| Layered motion estimation | 415 | out-of-scope | cv-special: layered motion |
| Layered motion estimation, transparent | 419 | out-of-scope | cv-special: layered motion |
| Layers |  | index-noise | heading |
| Layers, image-based rendering | 626 | out-of-scope | app: image-based rendering (graphics) |
| Layout consistent random field | 708 | out-of-scope | cv-special: random-field variant |
| Learning in computer vision | 714 | taught | DL-040; DL-051 |
| Least median of squares (LMS) | 318 | out-of-scope | robust-regression variant; the plan uses RANSAC and robust losses (RO 229, RO 235) |
| Least squares |  | taught | ML-050 |
| Least squares, iterative solvers | 324, 748 | taught | new MA: Sparse linear solves and conjugate gradient |
| Least squares, linear | 94, 312, 320, 384, 738, 742, 756, 760, 786 | taught | ML-050; ML-053 |
| Least squares, non-linear | 315, 324, 347, 746, 760, 787 | taught | new MA: Nonlinear least squares (Gauss-Newton) |
| Least squares, robust [see Robust least squares] |  | index-noise | cross-reference |
| Least squares, sparse | 364, 748, 787 | taught | new MA: Sparse linear solves and conjugate gradient |
| Least squares, total | 744 | taught | RO 92 (plane fitting by the smallest eigenvector) |
| Least squares, weighted | 313, 494, 498, 505 | mentioned-only | `weighted-least-squares`: Weighted least squares (maths; MA 07-optimisation (section in the planned nonlinear least squares Note)). MA-063 names it once |
| Lens |  | taught | RO 88; RO 89 |
| Lens, compound | 71 | out-of-scope | lens optics detail |
| Lens, nodal point | 71 | out-of-scope | lens optics detail |
| Lens, thin | 69 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)). thin lens and focus |
| Lens distortions | 58 | taught | RO 89 |
| Lens distortions, calibration | 334 | taught | RO 89 |
| Lens distortions, decentering | 59 | taught | RO 89 |
| Lens distortions, radial | 58 | taught | RO 89 |
| Lens distortions, spline-based | 59 | out-of-scope | cv-special: spline distortion models |
| Lens distortions, tangential | 59 | taught | RO 89 |
| Lens law | 69 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)). lens law |
| Level of detail (LOD) | 594 | out-of-scope | graphics: level of detail |
| Level sets | 281, 282 | out-of-scope | cv-special: level sets |
| Level sets, fast marching method | 282 | taught | RO 106 (wavefront propagation) |
| Level sets, geodesic active contour | 282 | out-of-scope | cv-special: geodesic active contours |
| Levenberg–Marquardt | 316, 371, 379, 747, 783 | taught | RO 235 |
| Lifting [see Wavelets] |  | index-noise | cross-reference |
| Light field |  | index-noise | heading |
| Light field, higher dimensional | 636 | out-of-scope | app: light fields (graphics) |
| Light field, light slab | 629 | out-of-scope | app: light fields (graphics) |
| Light field, ray space | 631 | out-of-scope | app: light fields (graphics) |
| Light field, rendering | 628 | out-of-scope | app: light fields (graphics) |
| Light field, surface | 632 | out-of-scope | app: light fields (graphics) |
| Lightness | 84 | add | `color-spaces`: Colour spaces (vision; RO-18 (section in 227)) |
| Line at infinity | 32 | add | `projective-points-lines`: Points and lines in homogeneous coordinates (vision; RO-03 (section in 88)). line at infinity |
| Line detection | 250 | add | `hough-transform`: Hough transform for lines (and circles) (vision; RO-18 (section in 229, next to RANSAC)) |
| Line detection, Hough transform | 251, 264 | add | `hough-transform`: Hough transform for lines (and circles) (vision; RO-18 (section in 229, next to RANSAC)) |
| Line detection, RANSAC | 254 | taught | RO 229 (RANSAC line fit) |
| Line detection, simplification | 250, 264 | add | `line-fitting-extraction`: Line extraction from points (robotics; RO-03 (section in 92)) |
| Line detection, successive approximation | 251, 264 | add | `line-fitting-extraction`: Line extraction from points (robotics; RO-03 (section in 92)) |
| Line equation | 32, 34 | taught | MA-051 (equation of a line/hyperplane) |
| Line fitting | 94, 264 | taught | ML-049; RO 92 |
| Line fitting, uncertainty | 265 | out-of-scope | uncertainty detail of line fitting beyond beginner depth |
| Line hull [see Visual hull] |  | index-noise | cross-reference |
| Line labeling | 11 | out-of-scope | history: line labelling (blocks world) |
| Line process | 194, 553, 764 | out-of-scope | cv-special: MRF line process |
| Line spread function (LSF) | 476 | out-of-scope | optics: line spread function |
| Line-based structure from motion | 374 | out-of-scope | cv-special: line-based SfM |
| Linear algebra | 735 | taught | MA-047 |
| Linear algebra, least squares | 742 | taught | MA-060 |
| Linear algebra, matrix decompositions | 736 | taught | MA-056; MA-057 |
| Linear algebra, references | 736 | index-noise | pointer to references |
| Linear blend | 104 | add | `point-operators`: Point operators (vision; RO-18 (section in 227)). linear blend |
| Linear discriminant analysis (LDA) | 676 | out-of-scope | ml-zoo: no robotics Note needs it; ML-022 names it (G-1059) |
| Linear filtering | 111 | taught | DL-042; RO 227 |
| Linear operator | 104 | taught | MA-053 |
| Linear operator, superposition | 104 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals). linear shift-invariant systems |
| Linear shift invariant (LSI) filter | 112 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals). linear shift-invariant systems |
| Live-wire | 280 | out-of-scope | app: interactive image cut-out |
| Local distance functions | 679 | out-of-scope | app: face recognition |
| Local operator | 111 | taught | DL-042 |
| Locality sensitive hashing (LSH) | 233 | out-of-scope | cv-special: locality-sensitive hashing |
| Locally adaptive histogram equalization | 109 | add | `point-operators`: Point operators (vision; RO-18 (section in 227)). histogram equalisation |
| Location recognition | 693 | taught | RO 236 (place recognition) |
| Loopy belief propagation (LBP) | 185, 769 | out-of-scope | message passing on loopy graphs for image labelling (cv-special) |
| Low-pass filter | 117 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals). low-pass filter |
| Low-pass filter, sinc | 117 | out-of-scope | ideal-filter detail (sinc) beyond beginner depth |
| Lumigraph | 628 | out-of-scope | app: light fields (graphics) |
| Lumigraph, unstructured | 632 | out-of-scope | app: light fields (graphics) |
| Luminance | 82 | add | `color-spaces`: Colour spaces (vision; RO-18 (section in 227)) |
| Lumisphere | 633 | out-of-scope | app: light fields (graphics) |
| M-estimator | 318, 384, 761 | taught | RO 235 |
| Mahalanobis distance | 291, 673, 677, 758 | taught | new MA: Mahalanobis distance |
| Manifold mosaic | 455, 649 | out-of-scope | app: manifold mosaics |
| Markov chain Monte Carlo (MCMC) | 760, 765 | out-of-scope | MCMC; the plan samples with particle filters and importance sampling (RO 82) |
| Markov random field | 180, 763 | out-of-scope | cv-special: MRFs for image labelling |
| Markov random field, cliques | 181, 764 | out-of-scope | cv-special: MRFs for image labelling |
| Markov random field, directed edges | 302 | out-of-scope | cv-special: MRFs for image labelling |
| Markov random field, dynamic | 772 | out-of-scope | cv-special: MRFs for image labelling |
| Markov random field, flux | 302 | out-of-scope | cv-special: MRFs for image labelling |
| Markov random field, inference [see MRF inference] |  | out-of-scope | cv-special: MRFs for image labelling |
| Markov random field, layout consistent | 708 | out-of-scope | cv-special: MRFs for image labelling |
| Markov random field, learning parameters | 180 | out-of-scope | cv-special: MRFs for image labelling |
| Markov random field, line process | 194, 553, 764 | out-of-scope | cv-special: MRFs for image labelling |
| Markov random field, neighborhood | 181, 763 | out-of-scope | cv-special: MRFs for image labelling |
| Markov random field, order | 181, 765 | out-of-scope | cv-special: MRFs for image labelling |
| Markov random field, random walker | 303 | out-of-scope | cv-special: MRFs for image labelling |
| Markov random field, stereo matching | 553 | out-of-scope | cv-special: MRFs for image labelling |
| Marr’s framework | 13 | out-of-scope | history: Marr's framework |
| Marr’s framework, computational theory | 13 | out-of-scope | history: Marr's framework |
| Marr’s framework, hardware implementation | 13 | out-of-scope | history: Marr's framework |
| Marr’s framework, representations and algorithms | 13 | out-of-scope | history: Marr's framework |
| Match move | 368 | out-of-scope | app: match moving (film) |
| Matrix decompositions | 736 | taught | MA-056; MA-057 |
| Matrix decompositions, Cholesky | 741 | taught | new MA: Cholesky factor |
| Matrix decompositions, eigenvalue (ED) | 737 | taught | MA-056 |
| Matrix decompositions, QR | 740 | mentioned-only | `qr-decomposition`: QR decomposition (Gram-Schmidt) and solving least squares with it (maths; MA 05-linear-algebra (new Note)). MA-047 roadmap names it only |
| Matrix decompositions, singular value (SVD) | 736 | taught | MA-057 |
| Matrix decompositions, square root | 741 | taught | new MA: Cholesky factor (matrix square root) |
| Matte reflection | 63 | out-of-scope | photometric image formation: reflectance models (graphics/optics) |
| Matting | 105, 106, 505, 529 | out-of-scope | app: matting (graphics) |
| Matting, alpha matte | 105 | out-of-scope | app: matting (graphics) |
| Matting, Bayesian | 510 | out-of-scope | app: matting (graphics) |
| Matting, blue screen | 106, 195, 507 | out-of-scope | app: matting (graphics) |
| Matting, difference | 106, 195, 508, 606 | out-of-scope | app: matting (graphics) |
| Matting, flash | 517 | out-of-scope | app: matting (graphics) |
| Matting, GrabCut | 513 | out-of-scope | app: matting (graphics) |
| Matting, Laplacian | 514 | out-of-scope | app: matting (graphics) |
| Matting, natural | 509 | out-of-scope | app: matting (graphics) |
| Matting, optimization-based | 513 | out-of-scope | app: matting (graphics) |
| Matting, Poisson | 513 | out-of-scope | app: matting (graphics) |
| Matting, shadow | 517 | out-of-scope | app: matting (graphics) |
| Matting, smoke | 516 | out-of-scope | app: matting (graphics) |
| Matting, triangulation | 507, 518 | out-of-scope | app: matting (graphics) |
| Matting, trimap | 509 | out-of-scope | app: matting (graphics) |
| Matting, two screen | 507 | out-of-scope | app: matting (graphics) |
| Matting, video | 518 | out-of-scope | app: matting (graphics) |
| Maximally stable extremal region (MSER) | 220 | out-of-scope | cv-special: MSER regions |
| Maximum a posteriori (MAP) estimate | 180, 763 | taught | MA-072 |
| Mean absolute difference (MAD) | 547 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90) |
| Mean average precision | 229 | taught | RO 173 |
| Mean shift | 289, 292 | out-of-scope | cv-special: mean-shift segmentation and tracking |
| Mean shift, bandwidth selection | 295 | out-of-scope | cv-special: mean-shift segmentation and tracking |
| Mean square error (MSE) | 92, 547 | taught | ML-051 |
| Measurement equation (model) | 346, 757 | taught | RO 74; RO 76 (measurement model) |
| Measurement matrix | 359 | out-of-scope | cv-special: factorisation SfM |
| Measurement model [see Bayesian model] |  | index-noise | cross-reference |
| Medial axis transform (MAT) | 130 | taught | RO 270 (maximum-clearance roadmap = medial axis) |
| Median absolute deviation (MAD) | 385 | taught | MA-006 §Extra (median absolute deviation, G-1207) |
| Median filter | 124 | add | `nonlinear-image-filters`: Nonlinear image filters (vision; RO-18 (section in 227) or RO 90 depth-map cleanup) |
| Median filter, weighted | 124 | out-of-scope | filter variant detail |
| Medical image registration | 408 | out-of-scope | app: medical imaging |
| Medical image segmentation | 304 | out-of-scope | app: medical imaging |
| Membrane | 175 | out-of-scope | cv-special: membrane spline energy |
| Mesh-based warping | 170, 201 | out-of-scope | app: mesh warping (graphics) |
| Metamer | 82 | out-of-scope | colour science (different field) |
| Metric learning | 679 | out-of-scope | ml-zoo: metric learning |
| Metric tree | 234 | out-of-scope | search-structure detail |
| MIP-mapping | 167 | out-of-scope | graphics: MIP-mapping |
| MIP-mapping, trilinear | 168 | out-of-scope | graphics: MIP-mapping |
| Mixture of Gaussians | 272, 279, 289 | taught | MA-073 |
| Mixture of Gaussians, color model | 509 | out-of-scope | app: matting colour model |
| Mixture of Gaussians, expectation maximization (EM) | 291 | taught | MA-074 |
| Mixture of Gaussians, mixing coefficient | 291 | taught | MA-073 |
| Mixture of Gaussians, soft assignment | 291 | taught | MA-073 |
| Model selection | 430, 763 | taught | ML-009 |
| Model-based reconstruction | 598 | out-of-scope | app: model-based reconstruction (graphics, faces) |
| Model-based reconstruction, architecture | 598 | out-of-scope | app: model-based reconstruction (graphics, faces) |
| Model-based reconstruction, heads and faces | 601 | out-of-scope | app: model-based reconstruction (graphics, faces) |
| Model-based reconstruction, human body | 605 | out-of-scope | app: model-based reconstruction (graphics, faces) |
| Model-based stereo | 599, 624 | out-of-scope | app: model-based reconstruction (graphics, faces) |
| Models |  | index-noise | heading |
| Models, Bayesian | 180, 762 | taught | MA-018 |
| Models, forward | 3 | taught | RO 74; RO 260 (forward sensor models) |
| Models, physically based | 14 | out-of-scope | framing term from the book's introduction (book-specific) |
| Models, physics-based | 3 | out-of-scope | framing term from the book's introduction (book-specific) |
| Models, probabilistic | 3 | taught | MA-072 |
| Modular eigenspace | 678 | out-of-scope | app: face recognition |
| Modulation transfer function (MTF) | 79, 476 | out-of-scope | optics: modulation transfer function |
| Morphable model |  | index-noise | heading |
| Morphable model, body | 609 | out-of-scope | app: morphing (graphics) |
| Morphable model, face | 603, 639 | out-of-scope | app: morphing (graphics) |
| Morphable model, multidimensional | 639 | out-of-scope | app: morphing (graphics) |
| Morphing | 173, 202, 622, 623 | out-of-scope | app: morphing (graphics) |
| Morphing, 3D body | 609 | out-of-scope | app: morphing (graphics) |
| Morphing, 3D face | 603 | out-of-scope | app: morphing (graphics) |
| Morphing, automated | 424 | out-of-scope | app: morphing (graphics) |
| Morphing, facial feature | 639 | out-of-scope | app: morphing (graphics) |
| Morphing, feature-based | 173, 202 | out-of-scope | app: morphing (graphics) |
| Morphing, flow-based | 424 | out-of-scope | app: morphing (graphics) |
| Morphing, video textures | 642 | out-of-scope | app: morphing (graphics) |
| Morphing, view morphing | 623, 650 | out-of-scope | app: morphing (graphics) |
| Morphological operator | 127 | add | `binary-image-ops`: Binary image processing (vision; RO-18 (new Note after 227)). morphology |
| Morphological operator, closing | 128 | add | `binary-image-ops`: Binary image processing (vision; RO-18 (new Note after 227)). morphology |
| Morphological operator, dilation | 128 | add | `binary-image-ops`: Binary image processing (vision; RO-18 (new Note after 227)). morphology |
| Morphological operator, erosion | 128 | add | `binary-image-ops`: Binary image processing (vision; RO-18 (new Note after 227)). morphology |
| Morphological operator, opening | 128 | add | `binary-image-ops`: Binary image processing (vision; RO-18 (new Note after 227)). morphology |
| Morphology | 127 | add | `binary-image-ops`: Binary image processing (vision; RO-18 (new Note after 227)). morphology |
| Mosaic [see Image stitching] |  | index-noise | cross-reference |
| Mosaics |  | index-noise | heading |
| Mosaics, motion models | 430 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)). choice of motion model |
| Mosaics, video compression | 436 | out-of-scope | app: mosaics and video compression |
| Mosaics, whiteboard and document scanning | 432 | out-of-scope | app: mosaics and video compression |
| Motion compensated video compression | 387, 421 | out-of-scope | app: mosaics and video compression |
| Motion compensation | 92 | out-of-scope | app: mosaics and video compression |
| Motion estimation | 383 | taught | RO 230 |
| Motion estimation, affine | 398 | out-of-scope | variant of Lucas-Kanade (affine patch motion) beyond beginner depth |
| Motion estimation, aperture problem | 394 | add | `aperture-problem`: The aperture problem and normal flow (vision; RO 230 (section)) |
| Motion estimation, compositional | 400 | out-of-scope | alignment-algorithm variant beyond beginner depth |
| Motion estimation, Fourier-based | 388 | out-of-scope | cv-special: Fourier-based motion estimation |
| Motion estimation, frame interpolation | 418 | out-of-scope | app: frame interpolation |
| Motion estimation, hierarchical | 387 | taught | RO 230 (pyramidal, iterative Lucas-Kanade) |
| Motion estimation, incremental refinement | 392 | taught | RO 230 (pyramidal, iterative Lucas-Kanade) |
| Motion estimation, layered | 415 | out-of-scope | cv-special: layered motion |
| Motion estimation, learning | 403, 411 | taught | RO 231 (learned optical flow) |
| Motion estimation, linear appearance variation | 397 | out-of-scope | alignment-algorithm variant beyond beginner depth |
| Motion estimation, optical flow | 409 | taught | RO 230 |
| Motion estimation, parametric | 398 | out-of-scope | variant of Lucas-Kanade (parametric motion) beyond beginner depth |
| Motion estimation, patch-based | 384, 399 | taught | RO 230 |
| Motion estimation, phase correlation | 390 | out-of-scope | cv-special: phase correlation |
| Motion estimation, quadtree spline-based | 407 | out-of-scope | cv-special: spline-based and reflection-aware motion estimation |
| Motion estimation, reflections | 419 | out-of-scope | cv-special: spline-based and reflection-aware motion estimation |
| Motion estimation, spline-based | 404 | out-of-scope | cv-special: spline-based and reflection-aware motion estimation |
| Motion estimation, translational | 384 | taught | RO 230 |
| Motion estimation, transparent | 419 | out-of-scope | cv-special: transparent motion |
| Motion estimation, uncertainty modeling | 395 | out-of-scope | uncertainty detail of flow estimates beyond beginner depth |
| Motion field | 398 | taught | RO 231 (image motion from camera motion) |
| Motion models |  | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)). 2D motion models |
| Motion models, learned | 403 | out-of-scope | cv-special: learned motion models |
| Motion segmentation | 425 | out-of-scope | cv-special: motion segmentation |
| Motion stereo | 561 | taught | RO 233 (stereo from a moving camera) |
| Motion-based user interaction | 425 | out-of-scope | app: motion-based interaction |
| Moving least squares (MLS) | 596 | out-of-scope | cv-special: moving-least-squares surfaces |
| MRF inference | 182, 765 | out-of-scope | cv-special: MRF inference algorithms for image labelling |
| MRF inference, alpha expansion | 185, 772 | out-of-scope | cv-special: MRF inference algorithms for image labelling |
| MRF inference, belief propagation | 185, 768 | out-of-scope | cv-special: MRF inference algorithms for image labelling |
| MRF inference, dynamic programming | 766 | out-of-scope | cv-special: MRF inference algorithms for image labelling |
| MRF inference, expansion move | 185, 772 | out-of-scope | cv-special: MRF inference algorithms for image labelling |
| MRF inference, gradient descent | 765 | out-of-scope | cv-special: MRF inference algorithms for image labelling |
| MRF inference, graph cuts | 183, 770 | out-of-scope | cv-special: MRF inference algorithms for image labelling |
| MRF inference, highest confidence first | 182 | out-of-scope | cv-special: MRF inference algorithms for image labelling |
| MRF inference, highest confidence first (HCF) | 765 | out-of-scope | cv-special: MRF inference algorithms for image labelling |
| MRF inference, iterated conditional modes | 182, 765 | out-of-scope | cv-special: MRF inference algorithms for image labelling |
| MRF inference, linear programming (LP) | 773 | out-of-scope | cv-special: MRF inference algorithms for image labelling |
| MRF inference, loopy belief propagation | 185, 769 | out-of-scope | cv-special: MRF inference algorithms for image labelling |
| MRF inference, Markov chain Monte Carlo | 765 | out-of-scope | cv-special: MRF inference algorithms for image labelling |
| MRF inference, simulated annealing | 182, 766 | out-of-scope | cv-special: MRF inference algorithms for image labelling |
| MRF inference, stochastic gradient descent | 182, 765 | out-of-scope | cv-special: MRF inference algorithms for image labelling |
| MRF inference, swap move (alpha-beta) | 185, 772 | out-of-scope | cv-special: MRF inference algorithms for image labelling |
| MRF inference, Swendsen–Wang | 766 | out-of-scope | cv-special: MRF inference algorithms for image labelling |
| Multi-frame motion estimation | 413 | out-of-scope | cv-special: multi-frame motion estimation |
| Multi-pass transforms | 169 | out-of-scope | app: panorama rendering |
| Multi-perspective panoramas | 437 | out-of-scope | app: panorama rendering |
| Multi-perspective plane sweep (MPPS) | 445 | out-of-scope | app: panorama rendering |
| Multi-view stereo | 558 | out-of-scope | cv-special: dense multi-view stereo; the plan's dense depth comes from stereo and depth cameras (RO 90) |
| Multi-view stereo, epipolar plane image | 559 | out-of-scope | cv-special: dense multi-view stereo; the plan's dense depth comes from stereo and depth cameras (RO 90) |
| Multi-view stereo, evaluation | 567 | out-of-scope | cv-special: dense multi-view stereo; the plan's dense depth comes from stereo and depth cameras (RO 90) |
| Multi-view stereo, initialization requirements | 566 | out-of-scope | cv-special: dense multi-view stereo; the plan's dense depth comes from stereo and depth cameras (RO 90) |
| Multi-view stereo, reconstruction algorithm | 565 | out-of-scope | cv-special: dense multi-view stereo; the plan's dense depth comes from stereo and depth cameras (RO 90) |
| Multi-view stereo, scene representation | 563 | out-of-scope | cv-special: dense multi-view stereo; the plan's dense depth comes from stereo and depth cameras (RO 90) |
| Multi-view stereo, shape priors | 565 | out-of-scope | cv-special: dense multi-view stereo; the plan's dense depth comes from stereo and depth cameras (RO 90) |
| Multi-view stereo, silhouettes | 567 | out-of-scope | cv-special: dense multi-view stereo; the plan's dense depth comes from stereo and depth cameras (RO 90) |
| Multi-view stereo, space carving | 566 | out-of-scope | cv-special: dense multi-view stereo; the plan's dense depth comes from stereo and depth cameras (RO 90) |
| Multi-view stereo, spatio-temporally shiftable window | 560 | out-of-scope | cv-special: dense multi-view stereo; the plan's dense depth comes from stereo and depth cameras (RO 90) |
| Multi-view stereo, taxonomy | 563 | out-of-scope | cv-special: dense multi-view stereo; the plan's dense depth comes from stereo and depth cameras (RO 90) |
| Multi-view stereo, visibility | 565 | out-of-scope | cv-special: dense multi-view stereo; the plan's dense depth comes from stereo and depth cameras (RO 90) |
| Multi-view stereo, volumetric | 562 | out-of-scope | cv-special: dense multi-view stereo; the plan's dense depth comes from stereo and depth cameras (RO 90) |
| Multi-view stereo, voxel coloring | 566 | out-of-scope | cv-special: dense multi-view stereo; the plan's dense depth comes from stereo and depth cameras (RO 90) |
| Multigrid | 753 | out-of-scope | advanced numerical solver (multigrid) beyond beginner depth |
| Multigrid, algebraic (AMG) | 288, 753 | out-of-scope | advanced numerical solver (multigrid) beyond beginner depth |
| Multiple hypothesis tracking | 279 | taught | RO 259 |
| Multiple-center-of-projection images | 437, 649 | out-of-scope | app: multi-perspective images |
| Multiresolution representation | 150 | taught | RO 227 |
| Mutual information | 386, 408 | taught | new MA: Mutual information |
| Natural image matting | 509 | out-of-scope | app: matting |
| Nearest neighbor |  | taught | ML-085 |
| Nearest neighbor, distance ratio (NNDR) | 230 | taught | RO 228 (ratio test) |
| Nearest neighbor, matching [see Feature matching] |  | index-noise | cross-reference |
| Negative posterior log likelihood | 180, 758, 762 | taught | RO 101 (negative log posterior) |
| Neighborhood operator | 111, 122 | taught | DL-042 |
| Neural networks | 661 | taught | DL-008 |
| Nintendo Wii | 326 | index-noise | product name |
| Nodal point | 71 | out-of-scope | lens optics detail |
| Noise |  | taught | RO 63 (noise in sensing) |
| Noise, sensor | 76, 473 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)). sensor noise |
| Noise level function (NLF) | 76, 96, 473, 527 | out-of-scope | sensor-noise calibration detail |
| Noise removal | 144, 197, 203 | add | `nonlinear-image-filters`: Nonlinear image filters (vision; RO-18 (section in 227) or RO 90 depth-map cleanup). noise removal |
| Non-linear filter | 122, 193 | add | `nonlinear-image-filters`: Nonlinear image filters (vision; RO-18 (section in 227) or RO 90 depth-map cleanup) |
| Non-linear least squares |  | index-noise | heading |
| Non-linear least squares, seeLeast squares | 315 | taught | new MA: Nonlinear least squares (Gauss-Newton) |
| Non-maximal suppression [see Feature detec-tion] |  | index-noise | cross-reference |
| Non-parametric density modeling | 292 | taught | MA-023 |
| Non-photorealistic rendering (NPR) | 522 | out-of-scope | app: non-photorealistic rendering |
| Non-rigid motion | 377 | out-of-scope | cv-special: non-rigid motion |
| Normal equations | 313, 393, 743, 746 | taught | ML-053 |
| Normal map (geometry image) | 594 | out-of-scope | graphics: normal maps |
| Normal vector | 34 | taught | MA-051 |
| Normalized cross-correlation (NCC) | 386, 422, 547 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90) |
| Normalized cuts | 296 | out-of-scope | cv-special: normalised-cut segmentation |
| Normalized cuts, intervening contour | 298 | out-of-scope | cv-special: normalised-cut segmentation |
| Normalized device coordinates (NDC) | 49, 54 | out-of-scope | graphics: normalised device coordinates |
| Normalized sum of squared differences |  | index-noise | heading |
| Normalized sum of squared differences, (NSSD) | 387 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90) |
| Norms |  | taught | MA-049 |
| Norms, L 1 | 179, 385, 411, 597 | taught | ML-066 |
| Norms, L ∞ | 367 | out-of-scope | norm used only in the book's minimax SfM formulation |
| Nyquist rate / frequency | 78 | add | `sampling-aliasing`: Sampling theorem (Nyquist rate) and aliasing; anti-alias low-pass before downsampling (maths; MA 06-calculus (Note after the Fourier Note); used in RO 227 pyramids and RO-03 sensor rates). Nyquist rate |
| Object detection | 658 | taught | RO 173 |
| Object detection, car | 666, 722 | taught | RO 173 |
| Object detection, face | 658 | out-of-scope | app: face detection |
| Object detection, part-based | 667 | out-of-scope | research-only: part-based detectors |
| Object detection, pedestrian | 666, 684 | taught | RO 173 |
| Object-centered projection | 57 | out-of-scope | projection-model detail beyond beginner depth |
| Occluding contours | 543 | out-of-scope | cv-special: occluding contours |
| Octree reconstruction | 569 | out-of-scope | cv-special: silhouette-based octree reconstruction |
| Octree spline | 409 | out-of-scope | cv-special: octree splines |
| Omnidirectional vision systems | 646 | taught | RO 89 (wide-angle and omnidirectional cameras) |
| Opacity | 106 | out-of-scope | app: compositing |
| Operator |  | index-noise | heading |
| Operator, linearity | 104 | taught | MA-053 (linearity) |
| Optic flow [see Optical flow] |  | index-noise | cross-reference |
| Optical center | 52 | add | `pinhole-geometry-terms`: Pinhole geometry terms (vision; RO-03 (section in 88)). optical centre |
| Optical flow | 409 | taught | RO 230 |
| Optical flow, anisotropic smoothness | 411 | out-of-scope | cv-special: flow regulariser variant |
| Optical flow, evaluation | 413 | out-of-scope | benchmarking detail |
| Optical flow, fusion move | 413 | out-of-scope | cv-special: fusion moves |
| Optical flow, global and local | 410 | taught | RO 231 (Horn-Schunck global vs Lucas-Kanade local) |
| Optical flow, Markov random field | 411 | out-of-scope | cv-special: MRF optical flow |
| Optical flow, multi-frame | 413 | out-of-scope | cv-special: multi-frame flow |
| Optical flow, normal flow | 394 | add | `aperture-problem`: The aperture problem and normal flow (vision; RO 230 (section)). normal flow |
| Optical flow, patch-based | 409 | taught | RO 230 |
| Optical flow, region-based | 417 | out-of-scope | cv-special: region-based flow |
| Optical flow, regularization | 410 | taught | RO 231 (smoothness term) |
| Optical flow, robust regularization | 411 | out-of-scope | cv-special: robust flow regulariser |
| Optical flow, smoothness | 410 | taught | RO 231 (smoothness term) |
| Optical flow, total variation | 411 | out-of-scope | cv-special: total-variation flow |
| Optical flow constraint equation | 393 | taught | RO 230 |
| Optical illusions | 3 | out-of-scope | perception psychology (different field) |
| Optical transfer function (OTF) | 79, 476 | out-of-scope | optics: optical transfer function |
| Optical triangulation | 586 | taught | RO 90 (structured light / laser triangulation) |
| Optics | 68 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)). lens optics basics |
| Optics, chromatic aberration | 71 | out-of-scope | lens optics detail (aberrations) |
| Optics, Seidel aberrations | 70 | out-of-scope | lens optics detail (aberrations) |
| Optics, vignetting | 72, 527 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)). vignetting |
| Optimal motion estimation | 363 | taught | RO 235 (bundle adjustment as the statistically optimal estimate) |
| Oriented particles (points) | 595 | out-of-scope | graphics: oriented particles |
| Orthogonal Procrustes | 320 | taught | RO 92 |
| Orthographic projection | 46 | out-of-scope | camera model for very distant scenes; robot cameras use the pinhole model (RO 88) |
| Osculating circle | 544 | taught | RO 67; RO 121 (curvature = 1 / radius) |
| Over operator | 106 | out-of-scope | app: compositing |
| Overview | 19 | index-noise | pointer to the book overview |
| Padding | 114, 196 | taught | DL-043 |
| Panography | 314, 337 | out-of-scope | app: panography |
| Panorama [see Image stitching] |  | index-noise | cross-reference |
| Panorama with depth | 438, 542, 634 | out-of-scope | app: panoramas with depth |
| Para-perspective projection | 48 | out-of-scope | camera model for very distant scenes; robot cameras use the pinhole model (RO 88) |
| Parallel tracking and mapping (PTAM) | 369 | taught | RO 236 (keyframe visual SLAM with tracking and mapping threads) |
| Parameter sensitive hashing | 233 | out-of-scope | cv-special: hashing |
| Parametric motion estimation | 398 | out-of-scope | variant of Lucas-Kanade (parametric motion) beyond beginner depth |
| Parametric surface | 593 | out-of-scope | graphics: parametric surfaces |
| Parametric transformation | 163, 201 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)) |
| Parseval’s Theorem [see Fourier transform] |  | index-noise | cross-reference |
| Part-based recognition | 701 | out-of-scope | research-only: part-based recognition |
| Part-based recognition, constellation model | 704 | out-of-scope | research-only: part-based recognition |
| Particle filtering | 279, 608, 760 | taught | RO 82 |
| Parzen window | 292 | taught | MA-023 (Parzen window = KDE) |
| PASCAL Visual Object Classes Challenge (VOC) | 718 | index-noise | data-set name |
| Patch-based motion estimation | 384 | taught | RO 230 |
| Peak signal-to-noise Ratio (PSNR) | 92, 144 | out-of-scope | app: image-quality metric (PSNR) |
| Pedestrian detection | 666 | taught | RO 173 |
| Penumbra | 60 | out-of-scope | photometric image formation (shadows) |
| Performance-driven animation | 237, 605, 639 | out-of-scope | app: performance-driven animation |
| Perspective n-point problem (PnP) | 322 | taught | RO 233 |
| Perspective projection | 48 | taught | RO 88 |
| Perspective transform (2D) | 37 | taught | RO 229 |
| Phase correlation | 390, 422 | out-of-scope | cv-special: phase correlation |
| Phong shading | 65 | out-of-scope | graphics: Phong shading |
| Photo pop-up | 710 | out-of-scope | app: photo collections and mosaics |
| Photo Tourism | 624 | out-of-scope | app: photo collections and mosaics |
| Photo-mosaic | 429 | out-of-scope | app: photo collections and mosaics |
| Photoconsistency | 540, 565 | out-of-scope | cv-special: photo-consistency in multi-view stereo |
| Photometric image formation | 60 | out-of-scope | photometric image formation (graphics/optics); robots rely on brightness constancy (RO 230) |
| Photometric image formation, calibration | 470 | out-of-scope | photometric image formation (graphics/optics); robots rely on brightness constancy (RO 230) |
| Photometric image formation, global illumination | 67 | out-of-scope | photometric image formation (graphics/optics); robots rely on brightness constancy (RO 230) |
| Photometric image formation, lighting | 60 | out-of-scope | photometric image formation (graphics/optics); robots rely on brightness constancy (RO 230) |
| Photometric image formation, optics | 68 | out-of-scope | photometric image formation (graphics/optics); robots rely on brightness constancy (RO 230) |
| Photometric image formation, radiosity | 67 | out-of-scope | photometric image formation (graphics/optics); robots rely on brightness constancy (RO 230) |
| Photometric image formation, reflectance | 62 | out-of-scope | photometric image formation (graphics/optics); robots rely on brightness constancy (RO 230) |
| Photometric image formation, shading | 65 | out-of-scope | photometric image formation (graphics/optics); robots rely on brightness constancy (RO 230) |
| Photometric stereo | 582 | out-of-scope | cv-special: photometric stereo |
| Photometry | 60 | out-of-scope | photometry (optics) |
| Photomontage | 459 | out-of-scope | app: photomontage |
| Physically based models | 14 | out-of-scope | framing term from the book's introduction (book-specific) |
| Physics-based vision | 16 | out-of-scope | framing term from the book's introduction (book-specific) |
| Pictorial structures | 12, 19, 701 | out-of-scope | cv-special: pictorial structures |
| Pixel transform | 103 | add | `point-operators`: Point operators (vision; RO-18 (section in 227)). pixel transform |
| Plücker coordinates | 35 | out-of-scope | 3D-line coordinates beyond beginner depth; screw axes are RB 275 |
| Planar pattern tracking | 326 | taught | RO 229 (tracking a plane by homography) |
| Plane at infinity | 34 | out-of-scope | cv-special: plane at infinity |
| Plane equation | 33 | taught | MA-051 |
| Plane plus parallax | 55, 405, 417, 540, 626 | out-of-scope | cv-special: plane-plus-parallax, plane sweep, plane-based SfM |
| Plane sweep | 540, 572 | out-of-scope | cv-special: plane-plus-parallax, plane sweep, plane-based SfM |
| Plane-based structure from motion | 376 | out-of-scope | cv-special: plane-plus-parallax, plane sweep, plane-based SfM |
| Plenoptic function | 628 | out-of-scope | graphics: plenoptic modelling |
| Plenoptic modeling | 623 | out-of-scope | graphics: plenoptic modelling |
| Plumb-line calibration method | 335, 341 | out-of-scope | alternative distortion-calibration method; the plan teaches target calibration (RO 89) |
| Point distribution model | 275 | out-of-scope | app: shape models |
| Point operator | 101 | add | `point-operators`: Point operators (vision; RO-18 (section in 227)) |
| Point process | 101 | add | `point-operators`: Point operators (vision; RO-18 (section in 227)) |
| Point spread function (PSF) | 78 | out-of-scope | optics: point spread function |
| Point spread function (PSF), estimation | 476, 528 | out-of-scope | optics: point spread function |
| Point-based representations | 595 | taught | RO 91 (point clouds) |
| Points at infinity | 32 | add | `projective-points-lines`: Points and lines in homogeneous coordinates (vision; RO-03 (section in 88)). points at infinity |
| Poisson |  | index-noise | heading |
| Poisson, blending | 460 | out-of-scope | app: Poisson image blending (graphics) |
| Poisson, equations | 597 | add | `laplace-poisson-equation`: Laplace's and Poisson's equations (maths; MA 06-calculus (new Note); used in RO 109 potential fields) |
| Poisson, matting | 513 | out-of-scope | app: Poisson matting (graphics) |
| Poisson, noise | 76 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)). shot (Poisson) noise |
| Poisson, surface reconstruction | 597 | out-of-scope | meshing method; the plan's maps use voxels and signed distance (RO 97) |
| Polar coordinates | 33 | taught | RO 120 (polar-coordinate controller); MA-063 |
| Polar projection | 59, 440 | out-of-scope | app: panorama projections |
| Polyphase filter | 145 | out-of-scope | filter-design detail |
| Pop-out effect | 4 | out-of-scope | perception psychology (different field) |
| Pose estimation | 321 | taught | RO 233 |
| Pose estimation, iterative | 324 | taught | RO 233 (refine pose by reprojection error) |
| Power spectrum | 140 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals). power spectrum |
| Precision [see Error rates] |  | index-noise | cross-reference |
| Precision, mean average | 229 | taught | RO 173 |
| Preconditioning | 751 | out-of-scope | numerical preconditioning beyond beginner depth |
| Principal component analysis (PCA) | 275, 660, 671, 738, 758 | taught | ML-047 |
| Principal component analysis (PCA), face modeling | 601 | out-of-scope | app: face modelling |
| Principal component analysis (PCA), generalized | 740 | out-of-scope | ml-zoo: PCA variants |
| Principal component analysis (PCA), missing data | 360, 740 | out-of-scope | ml-zoo: PCA variants |
| Prior energy (term) | 181, 763 | out-of-scope | cv-special: MRF prior term |
| Prior model [see Bayesian model] |  | index-noise | cross-reference |
| Profile curves | 543 | out-of-scope | cv-special: profile curves |
| Progressive mesh (PM) | 594 | out-of-scope | graphics: progressive meshes |
| Projections |  | index-noise | heading |
| Projections, object-centered | 57 | out-of-scope | projection-model detail beyond beginner depth |
| Projections, orthographic | 46 | out-of-scope | camera model for very distant scenes; robot cameras use the pinhole model (RO 88) |
| Projections, para-perspective | 48 | out-of-scope | camera model for very distant scenes; robot cameras use the pinhole model (RO 88) |
| Projections, perspective | 48 | taught | RO 88 |
| Projective (uncalibrated) reconstruction | 353 | out-of-scope | cv-special: projective reconstruction (uncalibrated cameras) |
| Projective depth | 55, 540 | out-of-scope | cv-special: projective reconstruction (uncalibrated cameras) |
| Projective disparity | 55, 540 | out-of-scope | cv-special: projective reconstruction (uncalibrated cameras) |
| Projective space | 32 | taught | new MA short section: Projective homogeneous coordinates |
| PROSAC (PROgressive SAmple Consensus) | 319 | out-of-scope | variant of a taught method (RANSAC, RO 229) beyond beginner depth |
| PSNR [see Peak signal-to-noise ratio] |  | index-noise | cross-reference |
| Pyramid | 144, 200 | taught | RO 227 |
| Pyramid, blending | 160, 200 | out-of-scope | app: pyramid blending |
| Pyramid, Gaussian | 150 | taught | RO 227 |
| Pyramid, half-octave | 152 | out-of-scope | pyramid-design detail |
| Pyramid, Laplacian | 151 | add | `image-laplacian-log`: Second-derivative image filters (vision; RO-18 (section in 227, before SIFT in 228)). Laplacian pyramid |
| Pyramid, motion estimation | 387 | taught | RO 230 (pyramidal KLT) |
| Pyramid, octave | 150 | taught | RO 227 |
| Pyramid, radial frequency implementation | 159 | out-of-scope | cv-special: steerable pyramids |
| Pyramid, steerable | 159 | out-of-scope | cv-special: steerable pyramids |
| Pyramid match kernel | 698 | out-of-scope | cv-special: pyramid match kernel |
| QR factorization | 740 | mentioned-only | `qr-decomposition`: QR decomposition (Gram-Schmidt) and solving least squares with it (maths; MA 05-linear-algebra (new Note)). MA-047 roadmap names it only |
| Quadratic form | 177 | taught | MA-068 |
| Quadrature mirror filter (QMF) | 150 | out-of-scope | filter-design detail (QMF) |
| Quadric equation | 33, 35 | out-of-scope | cv-special: quadrics |
| Quadtree spline |  | index-noise | heading |
| Quadtree spline, motion estimation | 407 | out-of-scope | cv-special: quadtree splines |
| Quadtree spline, restricted | 407 | out-of-scope | cv-special: quadtree splines |
| Quaternions | 43 | taught | new MA: 3D rotations: Euler angles and quaternions |
| Quaternions, antipodal | 43 | add | `rotation-matrix-properties`: Rotation representations (maths; MA 05-linear-algebra (section in the planned 3D rotations Note)). q and -q give the same rotation |
| Quaternions, multiplication | 44 | taught | new MA: 3D rotations: Euler angles and quaternions |
| Query by image content (QBIC) | 717 | out-of-scope | app: image retrieval |
| Query expansion | 692 | out-of-scope | app: image retrieval |
| Quincunx sampling | 152 | out-of-scope | sampling-pattern detail |
| Radial basis function | 171, 176, 592 | taught | ML-089 |
| Radial distortion | 58 | taught | RO 89 |
| Radial distortion, barrel | 58 | taught | RO 89 |
| Radial distortion, calibration | 334 | taught | RO 89 |
| Radial distortion, parameters | 58 | taught | RO 89 |
| Radial distortion, pincushion | 58 | taught | RO 89 |
| Radiance map | 483 | out-of-scope | app: HDR radiance maps |
| Radiometric image formation | 60 | out-of-scope | photometric image formation (graphics/optics) |
| Radiometric response function | 470 | out-of-scope | cv-special: radiometric response calibration |
| Radiometry | 60 | out-of-scope | photometric image formation (graphics/optics) |
| Radiosity | 68 | out-of-scope | photometric image formation (graphics/optics) |
| Random walker | 303, 771 | out-of-scope | cv-special: random-walker segmentation |
| Range (of a function) | 103 | taught | MA-061 |
| Range data [see Range scan] |  | index-noise | cross-reference |
| Range image [see Range scan] |  | index-noise | cross-reference |
| Range scan |  | taught | RO 91 |
| Range scan, alignment | 588, 617 | taught | RO 92 |
| Range scan, large scenes | 590 | out-of-scope | large-scale scanning detail |
| Range scan, merging | 589 | taught | RO 97 (fusing scans into a volumetric map) |
| Range scan, registration | 588, 617 | taught | RO 92 |
| Range scan, segmentation | 588 | taught | RO 176 (ground removal, clustering) |
| Range scan, volumetric | 590 | taught | RO 97 (fusing scans into a volumetric map) |
| Range sensing (rangefinding) | 585 | taught | RO 90; RO 91 |
| Range sensing (rangefinding), coded pattern | 587 | taught | RO 90 (structured light) |
| Range sensing (rangefinding), light stripe | 586 | taught | RO 90 (structured light) |
| Range sensing (rangefinding), shadow stripe | 586, 616 | out-of-scope | cv-special: shadow-stripe and spacetime stereo |
| Range sensing (rangefinding), spacetime stereo | 587 | out-of-scope | cv-special: shadow-stripe and spacetime stereo |
| Range sensing (rangefinding), stereo | 587 | taught | RO 90 |
| Range sensing (rangefinding), texture pattern (checkerboard) | 587 | taught | RO 90 (structured light) |
| Range sensing (rangefinding), time of flight | 587 | taught | RO 90; RO 91 (time of flight) |
| RANSAC |  | taught | RO 229 |
| RANSAC, (RAndom SAmple Consensus) | 318 | taught | RO 229 |
| RANSAC, inliers | 319 | taught | RO 229 |
| RANSAC, preemptive | 319 | out-of-scope | variant of a taught method (RANSAC, RO 229) beyond beginner depth |
| RANSAC, progressive (PROSAC) | 319 | out-of-scope | variant of a taught method (RANSAC, RO 229) beyond beginner depth |
| RAW image format | 77 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)). RAW images |
| Ray space (light field) | 631 | out-of-scope | app: light fields (graphics) |
| Ray tracing | 68 | out-of-scope | graphics: ray tracing |
| Rayleigh quotient | 297 | out-of-scope | linear-algebra identity used in a derivation (proof technique) |
| Recall [see Error rates] |  | index-noise | cross-reference |
| Receiver Operating Characteristic |  | taught | ML-077 |
| Receiver Operating Characteristic, area under the curve (AUC) | 229 | taught | ML-077 |
| Receiver Operating Characteristic, mean average precision | 229 | taught | RO 173 |
| Receiver Operating Characteristic, ROC curve | 229, 260 | taught | ML-077 |
| Recognition | 655 | taught | RO 173 |
| Recognition, 3D models | 725 | out-of-scope | cv-special: recognition from 3D models |
| Recognition, category (class) | 696 | taught | RO 173; DL-049 |
| Recognition, color similarity | 717 | out-of-scope | app: colour-based image retrieval |
| Recognition, context | 712 | out-of-scope | cv-special: context in recognition |
| Recognition, contour-based | 724 | out-of-scope | cv-special: contour-based recognition |
| Recognition, data sets | 718 | index-noise | pointer to data sets |
| Recognition, face | 668 | out-of-scope | app: face recognition |
| Recognition, instance | 685 | taught | RO 236 |
| Recognition, large scale | 715 | out-of-scope | large-scale recognition detail |
| Recognition, learning | 714 | taught | DL-040 |
| Recognition, part-based | 701 | out-of-scope | research-only: part-based recognition |
| Recognition, scene understanding | 712 | out-of-scope | app: scene understanding |
| Recognition, segmentation | 704 | taught | RO 175 |
| Recognition, shape context | 724 | out-of-scope | cv-special: shape context |
| Rectangle detection | 257 | out-of-scope | cv-special: rectangle detection |
| Rectification | 538, 571 | taught | RO 90 |
| Rectification, standard rectified geometry | 539 | taught | RO 90 |
| Recursive filter | 122 | add | `digital-filters`: Discrete-time signal filters (control; RO-03 (section in 83 or 86)). recursive (IIR) filter |
| Reference plane | 55 | out-of-scope | cv-special: reference plane (plane plus parallax) |
| Reflectance | 62 | out-of-scope | photometric image formation: reflectance models (graphics/optics) |
| Reflectance map | 580 | out-of-scope | photometric image formation: reflectance models (graphics/optics) |
| Reflectance modeling | 611 | out-of-scope | photometric image formation: reflectance models (graphics/optics) |
| Reflection |  | index-noise | heading |
| Reflection, di-chromatic | 67 | out-of-scope | photometric image formation: reflectance models (graphics/optics) |
| Reflection, diffuse | 63 | out-of-scope | photometric image formation: reflectance models (graphics/optics) |
| Reflection, specular | 64 | out-of-scope | photometric image formation: reflectance models (graphics/optics) |
| Region |  | index-noise | heading |
| Region, merging | 286 | out-of-scope | cv-special: region split-and-merge segmentation |
| Region, splitting | 286 | out-of-scope | cv-special: region split-and-merge segmentation |
| Region segmentation [see Segmentation] |  | index-noise | cross-reference |
| Registration [see Image Alignment] |  | index-noise | cross-reference |
| Registration, feature-based | 311 | taught | RO 229 |
| Registration, intensity-based | 384 | taught | RO 230; RO 234 |
| Registration, medical image | 408 | out-of-scope | app: medical image registration |
| Regularization | 174, 407 | taught | ML-062; DL-026 |
| Regularization, robust | 178 | out-of-scope | cv-special: robust regularisers |
| Regularization parameter | 176 | taught | ML-062 (regularisation strength) |
| Residual error | 312, 318, 346, 363, 384, 393, 399, 410, 411, 742, 750 | taught | ML-055 (residuals) |
| RGB (red green blue) [see Color] |  | index-noise | cross-reference |
| Rigid body transformation | 36, 40 | taught | new MA: Rigid-body transforms and homogeneous coordinates |
| Robust error metric [see Robust penalty func-tion] |  | index-noise | cross-reference |
| Robust least squares | 255, 256, 318, 384, 761 | taught | RO 235 |
| Robust least squares, iteratively reweighted | 318, 324, 398, 761 | taught | new MA short section: Levenberg-Marquardt and robust losses (IRLS) |
| Robust penalty function | 178, 384, 397, 499, 542, 547, 548, 553, 761 | taught | RO 235 |
| Robust regularization | 178 | out-of-scope | cv-special: robust regularisers |
| Robust statistics | 385, 760 | taught | RO 235 |
| Robust statistics, inliers | 319 | taught | RO 229 |
| Robust statistics, M-estimator | 318, 384, 761 | taught | RO 235 |
| Rodriguez’s formula | 42 | taught | new MA: Matrix exponential and logarithm (gives Rodrigues' formula) |
| Root mean square error (RMS) | 92, 385 | taught | ML-051 (RMSE) |
| Rotations | 41 | taught | new MA: 3D rotations: Euler angles and quaternions; RO 65 |
| Rotations, Euler angles | 41 | taught | new MA: 3D rotations: Euler angles and quaternions |
| Rotations, axis/angle | 41 | taught | new MA: Axis-angle, exponential and log maps of rotations |
| Rotations, exponential twist | 43 | taught | RB 275 |
| Rotations, incremental | 45 | add | `lie-groups`: Matrix Lie groups SO(3)/SE(3) for estimation (maths; MA 05-linear-algebra (new Note after the planned axis-angle Note); used by RO 87, RO 101, RO 235). small (incremental) rotation updates |
| Rotations, interpolation | 45 | taught | RO 202 (slerp) |
| Rotations, quaternions | 43 | taught | new MA: 3D rotations: Euler angles and quaternions |
| Rotations, Rodriguez’s formula | 42 | taught | new MA: Matrix exponential and logarithm (Rodrigues' formula) |
| Sampling | 77 | add | `sampling-aliasing`: Sampling theorem (Nyquist rate) and aliasing; anti-alias low-pass before downsampling (maths; MA 06-calculus (Note after the Fourier Note); used in RO 227 pyramids and RO-03 sensor rates) |
| Scale invariant feature transform (SIFT) | 223 | taught | RO 228 |
| Scale-space | 13, 119, 152, 282 | taught | RO 228 |
| Scatter matrix | 671 | taught | ML-047 (covariance / scatter matrix) |
| Scatter matrix, between-class | 675 | out-of-scope | ml-zoo: scatter matrices of linear discriminant analysis |
| Scatter matrix, within-class | 674 | out-of-scope | ml-zoo: scatter matrices of linear discriminant analysis |
| Scattered data interpolation | 171, 592 | out-of-scope | cv-special: scattered-data interpolation |
| Scene completion | 709 | out-of-scope | app: scene completion |
| Scene flow | 562, 644 | out-of-scope | research-only: scene flow |
| Scene understanding | 712 | out-of-scope | app: scene understanding |
| Scene understanding, gist | 709, 714 | out-of-scope | app: scene understanding |
| Scene understanding, scene alignment | 715 | out-of-scope | app: scene understanding |
| Schur complement | 366, 748 | taught | new MA: Schur complement |
| Scratch removal | 521 | out-of-scope | app: scratch removal |
| Seam selection |  | index-noise | heading |
| Seam selection, image stitching | 456 | out-of-scope | app: stitching seams |
| Second-order cone programming (SOCP) | 367 | out-of-scope | convex-program class beyond the plan's QPs (RO 207, RO 288) |
| Seed and grow |  | index-noise | heading |
| Seed and grow, stereo | 543 | out-of-scope | cv-special: seed-and-grow matching |
| Seed and grow, structure from motion | 371 | out-of-scope | cv-special: seed-and-grow matching |
| Segmentation | 267 | taught | RO 175 |
| Segmentation, active contours | 270 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, affinities | 296 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, binary MRF | 182, 300 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, CONDENSATION | 279 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, connected components | 131, 198 | add | `binary-image-ops`: Binary image processing (vision; RO-18 (new Note after 227)). connected components |
| Segmentation, energy-based | 300 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, for recognition | 704 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, geodesic active contour | 282 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, geodesic distance | 304 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, GrabCut | 301, 513 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, graph cuts | 300 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, graph-based | 286 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, hierarchical | 285, 288 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, intelligent scissors | 280 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, joint feature space | 294 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, k-means | 289 | taught | ML-122 |
| Segmentation, level sets | 281 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, mean shift | 289, 292 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, medical image | 304 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, merging | 286 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, minimum description length (MDL) | 300 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, mixture of Gaussians | 289 | taught | MA-073 |
| Segmentation, Mumford–Shah | 300 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, non-parametric | 292 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, normalized cuts | 296 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, probabilistic aggregation | 288 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, random walker | 303 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, snakes | 270 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, splitting | 286 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, stereo matching | 556 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, thresholding | 127 | add | `binary-image-ops`: Binary image processing (vision; RO-18 (new Note after 227)). thresholding |
| Segmentation, tobogganing | 281, 285 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, watershed | 284 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Segmentation, weighted aggregation (SWA) | 300 | out-of-scope | cv-special: classical segmentation algorithm; the plan uses learned segmentation (RO 175) |
| Seidel aberrations | 70 | out-of-scope | lens optics detail (aberrations) |
| Self-calibration | 355 | out-of-scope | cv-special: self-calibration; robots calibrate with targets (RO 89) |
| Self-calibration, bundle adjustment | 357 | out-of-scope | cv-special: self-calibration; robots calibrate with targets (RO 89) |
| Self-calibration, Kruppa equations | 356 | out-of-scope | cv-special: self-calibration; robots calibrate with targets (RO 89) |
| Sensing | 73 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)) |
| Sensing, aliasing | 77, 476 | add | `sampling-aliasing`: Sampling theorem (Nyquist rate) and aliasing; anti-alias low-pass before downsampling (maths; MA 06-calculus (Note after the Fourier Note); used in RO 227 pyramids and RO-03 sensor rates) |
| Sensing, color | 80 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)) |
| Sensing, color balance | 86 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)) |
| Sensing, gamma | 87 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)) |
| Sensing, pipeline | 74, 471 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)) |
| Sensing, sampling | 77 | add | `sampling-aliasing`: Sampling theorem (Nyquist rate) and aliasing; anti-alias low-pass before downsampling (maths; MA 06-calculus (Note after the Fourier Note); used in RO 227 pyramids and RO-03 sensor rates) |
| Sensing, sampling pitch | 75 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)). pixel pitch |
| Sensor noise | 76, 473 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)). sensor noise |
| Sensor noise, amplifier | 76 | out-of-scope | sensor-noise source detail |
| Sensor noise, dark current | 76 | out-of-scope | sensor-noise source detail |
| Sensor noise, fixed pattern | 76 | out-of-scope | sensor-noise source detail |
| Sensor noise, shot noise | 76 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)). shot noise |
| Separable filtering | 115, 197 | add | `separable-filters`: Separable filters (vision; RO-18 (section in 227)) |
| Shading | 65 | out-of-scope | photometric image formation and shading (graphics/optics) |
| Shading, equation | 64 | out-of-scope | photometric image formation and shading (graphics/optics) |
| Shading, shape-from | 580 | out-of-scope | photometric image formation and shading (graphics/optics) |
| Shadow matting | 517 | out-of-scope | photometric image formation and shading (graphics/optics) |
| Shape context | 249, 724 | out-of-scope | cv-special: shape context |
| Shape from |  | index-noise | heading |
| Shape from, focus | 584, 616 | out-of-scope | cv-special: shape-from-X methods |
| Shape from, photometric stereo | 582 | out-of-scope | cv-special: shape-from-X methods |
| Shape from, profiles | 543 | out-of-scope | cv-special: shape-from-X methods |
| Shape from, shading | 580 | out-of-scope | cv-special: shape-from-X methods |
| Shape from, silhouettes | 567 | out-of-scope | cv-special: shape-from-X methods |
| Shape from, specularities | 584 | out-of-scope | cv-special: shape-from-X methods |
| Shape from, stereo | 533 | taught | RO 90 |
| Shape from, texture | 583 | out-of-scope | cv-special: shape from texture |
| Shape parameters | 275, 681 | out-of-scope | app: shape-model parameters |
| Shape-from-X | 14 | out-of-scope | cv-special: shape-from-X methods |
| Shape-from-X, focus | 14 | out-of-scope | cv-special: shape-from-X methods |
| Shape-from-X, photometric stereo | 14 | out-of-scope | cv-special: shape-from-X methods |
| Shape-from-X, shading | 14 | out-of-scope | cv-special: shape-from-X methods |
| Shape-from-X, texture | 14 | out-of-scope | cv-special: shape-from-X methods |
| Shift invariance | 112 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals). shift invariance |
| Shiftable multi-scale transform | 159 | out-of-scope | cv-special: shiftable multi-scale transforms |
| Shutter speed | 75 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)). shutter speed |
| Signed distance function | 281, 589, 595, 597 | taught | RO 97 (signed distance) |
| Silhouette-based reconstruction | 567 | out-of-scope | cv-special: silhouette-based reconstruction |
| Silhouette-based reconstruction, octree | 569 | out-of-scope | cv-special: silhouette-based reconstruction |
| Silhouette-based reconstruction, visual hull | 567 | out-of-scope | cv-special: silhouette-based reconstruction |
| Similarity transform | 36, 40 | add | `2d-transform-hierarchy`: The 2D transform hierarchy (vision; RO-18 (section in 229)) |
| Simulated annealing | 182, 766 | out-of-scope | stochastic global optimiser; the plan's samplers are CEM and MPPI (RL 43, RO 210) |
| Simultaneous localization and mapping (SLAM) | 368 | taught | RO 100 |
| Sinc filter |  | index-noise | heading |
| Sinc filter, interpolation | 148 | out-of-scope | ideal-filter detail (sinc) beyond beginner depth |
| Sinc filter, low-pass | 117 | out-of-scope | ideal-filter detail (sinc) beyond beginner depth |
| Sinc filter, windowed | 148 | out-of-scope | ideal-filter detail (sinc) beyond beginner depth |
| Single view metrology | 331, 340 | out-of-scope | cv-special: single-view metrology |
| Singular value decomposition (SVD) | 736 | taught | MA-057 |
| Skeletal set | 367, 372 | out-of-scope | cv-special: skeletal sets for SfM |
| Skeleton | 130, 248 | taught | RO 270 (medial axis / generalised Voronoi) |
| Skew | 50, 52 | add | `pinhole-geometry-terms`: Pinhole geometry terms (vision; RO-03 (section in 88)). skew in K |
| Skin color detection | 96 | out-of-scope | app: skin detection, slanted edge, matting |
| Slant edge calibration | 476 | out-of-scope | app: skin detection, slanted edge, matting |
| Slippery spring | 273 | out-of-scope | app: skin detection, slanted edge, matting |
| Smoke matting | 516 | out-of-scope | app: skin detection, slanted edge, matting |
| Smoothness constraint | 176 | taught | RO 231 (smoothness term) |
| Smoothness penalty | 176 | taught | RO 231 (smoothness term) |
| Snakes | 270 | out-of-scope | cv-special: snakes (active contours) |
| Snakes, ballooning | 271 | out-of-scope | cv-special: snakes (active contours) |
| Snakes, dynamic | 276 | out-of-scope | cv-special: snakes (active contours) |
| Snakes, internal energy | 270 | out-of-scope | cv-special: snakes (active contours) |
| Snakes, Kalman | 276 | out-of-scope | cv-special: snakes (active contours) |
| Snakes, shape priors | 274 | out-of-scope | cv-special: snakes (active contours) |
| Snakes, slippery spring | 273 | out-of-scope | cv-special: snakes (active contours) |
| Soft assignment | 291 | taught | MA-073 (soft assignment / responsibility) |
| Software | 780 | index-noise | pointer to software |
| Space carving |  | index-noise | heading |
| Space carving, multi-view stereo | 566 | out-of-scope | cv-special: space carving and spacetime stereo |
| Spacetime stereo | 587 | out-of-scope | cv-special: space carving and spacetime stereo |
| Sparse flexible model | 703 | out-of-scope | research-only: sparse flexible models |
| Sparse matrices | 747, 787 | taught | new MA: Sparse linear solves and conjugate gradient |
| Sparse matrices, compressed sparse row (CSR) | 747 | out-of-scope | sparse-storage format detail |
| Sparse matrices, skyline storage | 747 | out-of-scope | sparse-storage format detail |
| Sparse methods |  | index-noise | heading |
| Sparse methods, direct | 747, 787 | taught | new MA: Sparse linear solves and conjugate gradient |
| Sparse methods, iterative | 748, 787 | taught | new MA: Sparse linear solves and conjugate gradient |
| Spatial pyramid matching | 699 | out-of-scope | cv-special: spatial pyramid matching |
| Spectral response function | 85 | out-of-scope | colour science (different field) |
| Spectral sensitivity | 85 | out-of-scope | colour science (different field) |
| Specular flow | 584 | out-of-scope | cv-special: specular flow |
| Specular reflection | 64 | out-of-scope | photometric image formation: reflectance models (graphics/optics) |
| Spherical coordinates | 34, 253, 256, 439 | taught | RO 91 (range-azimuth-elevation) |
| Spherical linear interpolation | 45 | taught | RO 202 (slerp) |
| Spin image | 589 | out-of-scope | cv-special: spin-image 3D descriptor |
| Splatting [see Forward warping] |  | index-noise | cross-reference |
| Splatting, volumetric | 595 | out-of-scope | graphics: volumetric splatting |
| Spline |  | taught | RO 202 |
| Spline, controlled continuity | 175 | out-of-scope | cv-special: spline variants for images |
| Spline, octree | 409 | out-of-scope | cv-special: spline variants for images |
| Spline, quadtree | 407 | out-of-scope | cv-special: spline variants for images |
| Spline, thin plate | 175 | out-of-scope | cv-special: spline variants for images |
| Spline-based motion estimation | 404 | out-of-scope | cv-special: spline variants for images |
| Splining images [see Laplacian pyramid blending] |  | index-noise | cross-reference |
| Sprites |  | index-noise | heading |
| Sprites, image-based rendering | 626 | out-of-scope | app: sprites (graphics, video coding) |
| Sprites, motion estimation | 415 | out-of-scope | app: sprites (graphics, video coding) |
| Sprites, video | 642 | out-of-scope | app: sprites (graphics, video coding) |
| Sprites, video compression | 436 | out-of-scope | app: sprites (graphics, video coding) |
| Sprites, with depth | 627 | out-of-scope | app: sprites (graphics, video coding) |
| Statistical decision theory | 757, 760 | taught | RL 53 (Bayesian decision making) |
| Steerable filter | 119, 198 | out-of-scope | cv-special: steerable filters |
| Steerable pyramid | 159 | out-of-scope | cv-special: steerable filters |
| Steerable random field | 184 | out-of-scope | cv-special: steerable filters |
| Stereo | 533 | taught | RO 90 |
| Stereo, aggregation methods | 549, 573 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90) |
| Stereo, coarse-to-fine | 554 | out-of-scope | stereo-algorithm variant beyond beginner depth |
| Stereo, cooperative algorithms | 554 | out-of-scope | stereo-algorithm variant beyond beginner depth |
| Stereo, correspondence | 535 | taught | RO 90 |
| Stereo, curve-based | 543 | out-of-scope | stereo-algorithm variant beyond beginner depth |
| Stereo, dense correspondence | 545 | taught | RO 90 |
| Stereo, depth map | 535 | taught | RO 90 |
| Stereo, dynamic programming | 554 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90) |
| Stereo, edge-based | 543 | out-of-scope | stereo-algorithm variant beyond beginner depth |
| Stereo, epipolar geometry | 537 | taught | RO 232; RO 90 |
| Stereo, feature-based | 543 | taught | RO 233 |
| Stereo, global optimization | 552, 573 | out-of-scope | cv-special: global and layered stereo |
| Stereo, graph cut | 553 | out-of-scope | cv-special: global and layered stereo |
| Stereo, layers | 558 | out-of-scope | cv-special: global and layered stereo |
| Stereo, local methods | 548 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90) |
| Stereo, model-based | 599, 624 | out-of-scope | cv-special: model-based and multi-view stereo |
| Stereo, multi-view | 558 | out-of-scope | cv-special: model-based and multi-view stereo |
| Stereo, non-parametric similarity measures | 547 | out-of-scope | matching-cost variant (census) beyond beginner depth |
| Stereo, photoconsistency | 540 | out-of-scope | cv-special: photo-consistency and plane sweep |
| Stereo, plane sweep | 540, 572 | out-of-scope | cv-special: photo-consistency and plane sweep |
| Stereo, rectification | 538, 571 | taught | RO 90 |
| Stereo, region-based | 548 | out-of-scope | stereo-algorithm variant beyond beginner depth |
| Stereo, scanline optimization | 556 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90) |
| Stereo, seed and grow | 543 | out-of-scope | stereo-algorithm variant beyond beginner depth |
| Stereo, segmentation-based | 548, 556 | out-of-scope | stereo-algorithm variant beyond beginner depth |
| Stereo, semi-global optimization | 556 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90) |
| Stereo, shiftable window | 560 | out-of-scope | stereo-algorithm variant beyond beginner depth |
| Stereo, similarity measure | 546 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90) |
| Stereo, spacetime | 587 | out-of-scope | cv-special: spacetime stereo |
| Stereo, sparse correspondence | 543 | taught | RO 233 |
| Stereo, sub-pixel refinement | 550 | out-of-scope | sub-pixel refinement detail |
| Stereo, support region | 548 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90) |
| Stereo, taxonomy | 535, 545 | index-noise | pointer to the book's taxonomy |
| Stereo, uncertainty | 551 | taught | RO 90 (depth error grows with distance) |
| Stereo, window-based | 548, 573 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90) |
| Stereo, winner-take-all (WTA) | 550 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90) |
| Stereo-based head tracking | 551 | out-of-scope | app: head tracking |
| Stiffness matrix | 177 | out-of-scope | different field: finite-element mechanics |
| Stitching [see Image stitching] |  | index-noise | cross-reference |
| Stochastic gradient descent | 182 | taught | ML-058 |
| Structural Similarity (SSIM) index | 144 | out-of-scope | app: image-quality metric (SSIM) |
| Structure from motion | 345 | taught | RO 235 |
| Structure from motion, affine | 359 | out-of-scope | cv-special: affine SfM, bas-relief ambiguity |
| Structure from motion, bas-relief ambiguity | 370 | out-of-scope | cv-special: affine SfM, bas-relief ambiguity |
| Structure from motion, bundle adjustment | 363 | taught | RO 235 |
| Structure from motion, constrained | 374 | out-of-scope | cv-special: constrained and factorisation SfM |
| Structure from motion, factorization | 357 | out-of-scope | cv-special: constrained and factorisation SfM |
| Structure from motion, feature tracks | 371 | taught | RO 234; RO 235 |
| Structure from motion, iterative factorization | 360 | out-of-scope | cv-special: factorisation and line-based SfM |
| Structure from motion, line-based | 374 | out-of-scope | cv-special: factorisation and line-based SfM |
| Structure from motion, multi-frame | 357 | taught | RO 235 |
| Structure from motion, non-rigid | 377 | out-of-scope | cv-special: non-rigid, orthographic, plane-based, projective SfM |
| Structure from motion, orthographic | 357 | out-of-scope | cv-special: non-rigid, orthographic, plane-based, projective SfM |
| Structure from motion, plane-based | 362, 376 | out-of-scope | cv-special: non-rigid, orthographic, plane-based, projective SfM |
| Structure from motion, projective factorization | 360 | out-of-scope | cv-special: non-rigid, orthographic, plane-based, projective SfM |
| Structure from motion, seed and grow | 371 | taught | RO 235 (incremental SfM) |
| Structure from motion, self-calibration | 355 | out-of-scope | cv-special: self-calibration, skeletal sets |
| Structure from motion, skeletal set | 367, 372 | out-of-scope | cv-special: self-calibration, skeletal sets |
| Structure from motion, two-frame | 347 | taught | RO 233 |
| Structure from motion, uncertainty | 370 | out-of-scope | uncertainty detail of SfM beyond beginner depth |
| Subdivision surface | 593 | out-of-scope | graphics: subdivision surfaces |
| Subdivision surface, subdivision connectivity | 594 | out-of-scope | graphics: subdivision surfaces |
| Subspace learning | 679 | out-of-scope | ml-zoo: subspace learning for faces |
| Sum of absolute differences (SAD) | 384, 422, 547 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90) |
| Sum of squared differences (SSD) | 384, 422, 547 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90) |
| Sum of squared differences (SSD), bias and gain | 386 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90) |
| Sum of squared differences (SSD), Fourier-based computation | 389 | out-of-scope | cv-special: Fourier-based SSD |
| Sum of squared differences (SSD), normalized | 387 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90) |
| Sum of squared differences (SSD), surface | 210, 396 | taught | RO 227 (Harris from the SSD surface) |
| Sum of squared differences (SSD), weighted | 385 | out-of-scope | matching-cost variant beyond beginner depth |
| Sum of squared differences (SSD), windowed | 385 | add | `stereo-patch-matching`: Stereo and patch matching (vision; RO 90 (section) or new Note after 90) |
| Sum of sum of squared differences (SSSD) | 559 | out-of-scope | cv-special: multi-baseline stereo cost |
| Summed area table | 120 | out-of-scope | cv-special: integral images for fast box sums |
| Super-resolution | 497, 529 | out-of-scope | app: super-resolution |
| Super-resolution, example-based | 499 | out-of-scope | app: super-resolution |
| Super-resolution, faces | 501 | out-of-scope | app: super-resolution |
| Super-resolution, hallucination | 499 | out-of-scope | app: super-resolution |
| Super-resolution, prior | 499 | out-of-scope | app: super-resolution |
| Superposition principle | 104 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals). superposition principle |
| Superquadric | 597 | out-of-scope | cv-special: superquadrics |
| Support vector machine (SVM) | 662, 667 | taught | ML-086 |
| Surface element (surfel) | 595 | out-of-scope | map-representation variant (surfels); RO 97 compares the main map types |
| Surface interpolation | 592 | out-of-scope | graphics: surface interpolation and light fields |
| Surface light field | 632 | out-of-scope | graphics: surface interpolation and light fields |
| Surface representations | 591 | taught | RO 97 (choosing a map type) |
| Surface representations, non-parametric | 593 | out-of-scope | graphics: surface-representation variants |
| Surface representations, parametric | 593 | out-of-scope | graphics: surface-representation variants |
| Surface representations, point-based | 595 | out-of-scope | graphics: surface-representation variants |
| Surface representations, simplification | 594 | out-of-scope | graphics: surface-representation variants |
| Surface representations, splines | 593 | out-of-scope | graphics: surface-representation variants |
| Surface representations, subdivision surface | 593 | out-of-scope | graphics: surface-representation variants |
| Surface representations, symmetry-seeking | 593 | out-of-scope | graphics: surface-representation variants |
| Surface representations, triangle mesh | 593 | taught | RO 71; RO 97 (triangle meshes) |
| Surface simplification | 594 | out-of-scope | graphics: surface simplification |
| Swendsen–Wang algorithm | 766 | out-of-scope | cv-special: MRF sampler |
| Telecentric lens | 48, 585 | out-of-scope | optics: telecentric lenses |
| Temporal derivative | 393, 410 | taught | RO 230 (brightness constancy: time derivative) |
| Temporal texture | 642 | out-of-scope | app: temporal textures |
| Term frequency-inverse document frequency (TF-IDF) | 689 | add | `bow-retrieval`: Bag-of-words retrieval (vision; RO 236 (section)). TF-IDF weighting |
| Testing algorithms | viii | index-noise | pointer to the preface |
| TextonBoost | 706 | out-of-scope | cv-special: TextonBoost |
| Texture |  | index-noise | heading |
| Texture, shape-from | 583 | out-of-scope | cv-special: shape from texture |
| Texture addressing mode | 115 | out-of-scope | border-mode detail beyond the zero padding of DL-043 |
| Texture map |  | index-noise | heading |
| Texture map, recovery | 610 | out-of-scope | graphics: texture maps |
| Texture map, view-dependent | 611, 623 | out-of-scope | graphics: texture maps |
| Texture mapping |  | index-noise | heading |
| Texture mapping, anisotropic filtering | 168 | out-of-scope | graphics: texture mapping |
| Texture mapping, MIP-mapping | 167 | out-of-scope | graphics: texture mapping |
| Texture mapping, multi-pass | 169 | out-of-scope | graphics: texture mapping |
| Texture mapping, trilinear interpolation | 168 | out-of-scope | graphics: texture mapping |
| Texture synthesis | 518, 531 | out-of-scope | app: texture synthesis (graphics) |
| Texture synthesis, by numbers | 523 | out-of-scope | app: texture synthesis (graphics) |
| Texture synthesis, hole filling | 521 | out-of-scope | app: texture synthesis (graphics) |
| Texture synthesis, image quilting | 519 | out-of-scope | app: texture synthesis (graphics) |
| Texture synthesis, non-parametric | 519 | out-of-scope | app: texture synthesis (graphics) |
| Texture synthesis, transfer | 522 | out-of-scope | app: texture synthesis (graphics) |
| Thin lens | 69 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)). thin lens |
| Thin-plate spline | 175 | out-of-scope | cv-special: thin-plate splines |
| Thresholding | 127 | add | `binary-image-ops`: Binary image processing (vision; RO-18 (new Note after 227)). thresholding |
| Through-the-lens camera control | 326, 368 | out-of-scope | app/cv-special: camera control, tobogganing |
| Tobogganing | 281, 285 | out-of-scope | app/cv-special: camera control, tobogganing |
| Tonal adjustment | 111, 196 | add | `point-operators`: Point operators (vision; RO-18 (section in 227)). tonal adjustment |
| Tone mapping | 487 | out-of-scope | app: tone mapping (computational photography) |
| Tone mapping, adaptive | 488 | out-of-scope | app: tone mapping (computational photography) |
| Tone mapping, bilateral filter | 489 | out-of-scope | app: tone mapping (computational photography) |
| Tone mapping, global | 487 | out-of-scope | app: tone mapping (computational photography) |
| Tone mapping, gradient domain | 489 | out-of-scope | app: tone mapping (computational photography) |
| Tone mapping, halos | 489 | out-of-scope | app: tone mapping (computational photography) |
| Tone mapping, interactive | 493 | out-of-scope | app: tone mapping (computational photography) |
| Tone mapping, local | 488 | out-of-scope | app: tone mapping (computational photography) |
| Tone mapping, scale selection | 492 | out-of-scope | app: tone mapping (computational photography) |
| Total least squares (TLS) | 265, 398, 744 | taught | RO 92 (total least squares by the smallest eigenvector) |
| Total variation | 179, 411, 597 | out-of-scope | cv-special: total-variation regularisation |
| Tracking |  | taught | RO 178 |
| Tracking, feature | 235 | taught | RO 230 |
| Tracking, head | 551 | out-of-scope | app: head tracking |
| Tracking, human motion | 605 | taught | RB 317 (human motion data) |
| Tracking, multiple hypothesis | 279 | taught | RO 259 |
| Tracking, planar pattern | 326 | taught | RO 229 |
| Tracking, PTAM | 369 | taught | RO 236 |
| Translational motion estimation | 384 | taught | RO 230 |
| Translational motion estimation, bias and gain | 386 | out-of-scope | photometric-alignment detail beyond beginner depth |
| Transparency | 106 | out-of-scope | app: compositing |
| Travelling salesman problem (TSP) | 272 | add | `tsp`: Travelling salesman problem (robotics; RO-23 (section in 273 or 274)) |
| Tri-chromatic sensing | 81 | out-of-scope | colour science (different field) |
| Tri-stimulus values | 81, 85 | out-of-scope | colour science (different field) |
| Triangulation | 345 | taught | RO 233 |
| Trilinear interpolation [see MIP-mapping] |  | index-noise | cross-reference |
| Trimap (matting) | 509 | out-of-scope | app: matting |
| Trust region method | 747 | taught | RL 38; new MA short section: Levenberg-Marquardt |
| Two-dimensional Fourier transform | 140 | add | `fourier-transform`: Linear shift-invariant systems and the Fourier transform (maths; MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals) |
| Uncanny valley | 3 | out-of-scope | HRI psychology (different field) |
| Uncertainty |  | taught | RO 63 |
| Uncertainty, correspondence | 313 | out-of-scope | uncertainty detail of matching beyond beginner depth |
| Uncertainty, modeling | 319, 775 | taught | RO 63; MA-073 |
| Uncertainty, weighting | 313 | add | `weighted-least-squares`: Weighted least squares (maths; MA 07-optimisation (section in the planned nonlinear least squares Note)). weight residuals by their uncertainty |
| Unsharp mask | 117 | add | `image-laplacian-log`: Second-derivative image filters (vision; RO-18 (section in 227, before SIFT in 228)). unsharp masking |
| Upsampling [see Interpolation] |  | index-noise | cross-reference |
| Vanishing point |  | add | `projective-points-lines`: Points and lines in homogeneous coordinates (vision; RO-03 (section in 88)). vanishing points |
| Vanishing point, detection | 254, 266 | out-of-scope | cv-special: vanishing-point detection and estimation |
| Vanishing point, Hough | 255 | out-of-scope | cv-special: vanishing-point detection and estimation |
| Vanishing point, least squares | 256 | out-of-scope | cv-special: vanishing-point detection and estimation |
| Vanishing point, modeling | 599 | out-of-scope | cv-special: vanishing-point detection and estimation |
| Vanishing point, uncertainty | 266 | out-of-scope | cv-special: vanishing-point detection and estimation |
| Variable reordering | 748 | out-of-scope | sparse-factorisation ordering detail |
| Variable reordering, minimum degree | 748 | out-of-scope | sparse-factorisation ordering detail |
| Variable reordering, multi-frontal | 748 | out-of-scope | sparse-factorisation ordering detail |
| Variable reordering, nested dissection | 748 | out-of-scope | sparse-factorisation ordering detail |
| Variable state dimension filter (VSDF) | 367 | taught | RO 263 (sliding-window filter) |
| Variational method | 175 | taught | RO 202 (beginner calculus of variations) |
| Video compression |  | out-of-scope | app: video coding, editing and rendering (graphics) |
| Video compression, motion compensated | 387 | out-of-scope | app: video coding, editing and rendering (graphics) |
| Video compression (coding) | 421 | out-of-scope | app: video coding, editing and rendering (graphics) |
| Video denoising | 414 | out-of-scope | app: video coding, editing and rendering (graphics) |
| Video matting | 518 | out-of-scope | app: video coding, editing and rendering (graphics) |
| Video objects (coding) | 415 | out-of-scope | app: video coding, editing and rendering (graphics) |
| Video sprites | 642 | out-of-scope | app: video coding, editing and rendering (graphics) |
| Video stabilization | 401, 423 | out-of-scope | app: video coding, editing and rendering (graphics) |
| Video texture | 640 | out-of-scope | app: video coding, editing and rendering (graphics) |
| Video-based animation | 639 | out-of-scope | app: video coding, editing and rendering (graphics) |
| Video-based rendering | 638 | out-of-scope | app: video coding, editing and rendering (graphics) |
| Video-based rendering, 3D video | 643 | out-of-scope | app: video coding, editing and rendering (graphics) |
| Video-based rendering, animating pictures | 643 | out-of-scope | app: video coding, editing and rendering (graphics) |
| Video-based rendering, sprites | 642 | out-of-scope | app: video coding, editing and rendering (graphics) |
| Video-based rendering, video texture | 640 | out-of-scope | app: video coding, editing and rendering (graphics) |
| Video-based rendering, virtual viewpoint video | 644 | out-of-scope | app: video coding, editing and rendering (graphics) |
| Video-based rendering, walkthroughs | 645 | out-of-scope | app: video coding, editing and rendering (graphics) |
| VideoMouse | 326 | out-of-scope | app: video coding, editing and rendering (graphics) |
| View correlation | 368 | out-of-scope | app: video coding, editing and rendering (graphics) |
| View interpolation | 357, 621, 650 | out-of-scope | app: video coding, editing and rendering (graphics) |
| View morphing | 357, 623, 642 | out-of-scope | app: video coding, editing and rendering (graphics) |
| View-based eigenspace | 678 | out-of-scope | app: video coding, editing and rendering (graphics) |
| View-dependent texture maps | 623 | out-of-scope | app: video coding, editing and rendering (graphics) |
| Vignetting | 72, 386, 474, 527 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)). vignetting |
| Vignetting, mechanical | 73 | out-of-scope | vignetting source detail |
| Vignetting, natural | 72 | out-of-scope | vignetting source detail |
| Virtual viewpoint video | 644 | out-of-scope | app: virtual viewpoint video |
| Visual hull | 567 | out-of-scope | cv-special: visual hull |
| Visual hull, image-based | 569 | out-of-scope | cv-special: visual hull |
| Visual illusions | 3 | out-of-scope | perception psychology (different field) |
| Visual odometry | 368 | taught | RO 234 |
| Visual words | 234, 688, 697 | taught | RO 236 |
| Vocabulary tree | 234, 691 | add | `bow-retrieval`: Bag-of-words retrieval (vision; RO 236 (section)). vocabulary tree |
| Volumetric 3D reconstruction | 562 | taught | RO 97 (volumetric / signed-distance fusion) |
| Volumetric range image processing (VRIP) | 589 | taught | RO 97 (volumetric / signed-distance fusion) |
| Volumetric representations | 596 | taught | RO 97 (volumetric / signed-distance fusion) |
| Voronoi diagram | 455 | taught | RO 270 |
| Voxel coloring |  | index-noise | heading |
| Voxel coloring, multi-view stereo | 566 | out-of-scope | cv-special: voxel colouring |
| Watershed | 284, 292 | out-of-scope | cv-special: watershed segmentation |
| Watershed, basins | 284, 292 | out-of-scope | cv-special: watershed segmentation |
| Watershed, oriented | 285 | out-of-scope | cv-special: watershed segmentation |
| Wavelets | 154, 201 | out-of-scope | cv-special: wavelets (mainly compression) |
| Wavelets, compression | 201 | out-of-scope | cv-special: wavelets (mainly compression) |
| Wavelets, lifting | 156 | out-of-scope | cv-special: wavelets (mainly compression) |
| Wavelets, overcomplete | 155, 159 | out-of-scope | cv-special: wavelets (mainly compression) |
| Wavelets, second generation | 158 | out-of-scope | cv-special: wavelets (mainly compression) |
| Wavelets, self-inverting | 159 | out-of-scope | cv-special: wavelets (mainly compression) |
| Wavelets, tight frame | 155 | out-of-scope | cv-special: wavelets (mainly compression) |
| Wavelets, weighted | 158 | out-of-scope | cv-special: wavelets (mainly compression) |
| Weaving wall | 544 | out-of-scope | cv-special: weaving wall |
| Weighted least squares (WLS) | 493, 505 | mentioned-only | `weighted-least-squares`: Weighted least squares (maths; MA 07-optimisation (section in the planned nonlinear least squares Note)). MA-063 names it once |
| Weighted prediction (bias and gain) | 386 | out-of-scope | photometric-alignment detail |
| White balance | 86, 97 | add | `camera-sensor-pipeline`: Digital camera sensing (vision; RO-03 (new Note after 88)). white balance |
| Whitening transform | 673 | add | `whitening`: Whitening transform (maths; MA 05-linear-algebra (section in the planned Mahalanobis Note)) |
| Wiener filter | 140, 142, 198 | out-of-scope | frequency-domain restoration filter beyond beginner depth |
| Wire removal | 521 | out-of-scope | app: wire removal |
| Wrapping mode | 115 | out-of-scope | border-mode detail beyond the zero padding of DL-043 |
| XYZ [see Color] |  | index-noise | cross-reference |
| Zippering | 589 | out-of-scope | cv-special: mesh zippering |
