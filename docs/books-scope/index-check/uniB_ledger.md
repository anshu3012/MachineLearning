# uniB ledger: university course schedules as checklists

Each table is one course's official lecture-by-lecture schedule (lecture titles plus topics listed under them; CS223A also lists two core concepts from its course description). Raw pages are saved in `uniB_work/raw/`. Every topic got a script match (`robo_match.py`, results in `uniB_work/terms.json`) and then a hand verdict (`uniB_work/verdicts.tsv`). A `taught` verdict cites a plan Note whose title or Teaches column names the concept, a plan §4 new-Note row, or an MA/ML/DL Note. For `add` rows the bold key is the merged concept in `uniB_adds.json`; keys shared with `ctrl_adds.json` / `vis_adds.json` are the same concept.

"Lecture" column: L = lecture, W = week, S/R = section or review session, desc = course description, F26 = MIT 6.4210 Fall 2026 tentative titles.

## Coverage summary

| Course | Term | Topics | taught | add | out-of-scope | index-noise |
|---|---|---|---|---|---|---|
| MIT 2.004 Dynamics and Control II (Rowell) | Spring 2008 (MIT OCW) | 32 | 4 | 18 | 9 | 1 |
| MIT 16.30 Feedback Control Systems (How, Frazzoli) | Fall 2010 (MIT OCW) | 27 | 12 | 11 | 3 | 1 |
| Caltech CDS 110/ChE 105 Analysis and Design of Feedback Control Systems (Murray) | Spring 2024 | 34 | 18 | 13 | 3 | 0 |
| Stanford CS223A / ME320 Introduction to Robotics (Khatib) | Winter 2026 | 16 | 13 | 1 | 0 | 2 |
| Berkeley EECS C106A/206A Introduction to Robotics (Horowitz, Tennant) | Fall 2025 | 30 | 26 | 2 | 2 | 0 |
| MIT 6.4210/6.4212 Robotic Manipulation (Tedrake) | Fall 2025 (plus new Fall 2026 tentative titles) | 31 | 26 | 1 | 3 | 1 |
| MIT 6.8210 (formerly 6.832) Underactuated Robotics (Tedrake) | Spring 2024 | 27 | 20 | 5 | 2 | 0 |
| CMU 16-745 Optimal Control and Reinforcement Learning (Manchester) | Spring 2025 | 32 | 24 | 3 | 5 | 0 |
| CMU 16-385 Computer Vision (Gkioulekas) | Spring 2020 (latest offering with a public schedule on the course site) | 25 | 17 | 4 | 4 | 0 |
| Stanford CS231A Computer Vision: From 3D Perception to 3D Reconstruction and beyond (Savarese, Bohg) | Spring 2025 | 18 | 11 | 4 | 3 | 0 |
| Berkeley CS 185/285 Deep Reinforcement Learning (Levine) | Spring 2026 | 21 | 16 | 3 | 1 | 1 |
| Cornell CS 4756/5756 Robot Learning (Fang) | Spring 2026 | 25 | 23 | 0 | 0 | 2 |
| **All** | | 318 | 210 | 65 | 35 | 8 |

## MIT 2.004 Dynamics and Control II (Rowell), Spring 2008 (MIT OCW)

Source: https://ocw.mit.edu/courses/2-004-dynamics-and-control-ii-spring-2008/pages/calendar/

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| Introduction | L1 | index-noise | course overview lecture, no single concept |
| Example: cruise control | L2 | taught | Note 252 (Longitudinal dynamics and cruise control) |
| Laplace transform definition, properties | L3 | add | **laplace** → MA 06-calculus, new Note after the planned ODEs and State-space models Notes (plan §4). Laplace transform |
| Block diagram algebra | L4 | add | **tf** → RO-06 Feedback control, new Note after Note 118. block-diagram algebra |
| Impedance of electrical components | L5 | out-of-scope | electrical circuit analysis (impedance of R, L, C), a different field; motor electrics are covered in Note 283 |
| Kirchhoff's laws, circuit equations | L6 | out-of-scope | electrical circuit analysis, a different field |
| Transfer functions | L7 | add | **tf** → RO-06 Feedback control, new Note after Note 118. transfer functions |
| Loop/mesh currents | L7 | out-of-scope | electrical circuit analysis (mesh-current method), a different field |
| Thevenin and Norton sources | L8 | out-of-scope | electrical circuit analysis (source equivalents), a different field |
| One-dimensional mechanical components (mass, spring, damper) | L9 | taught | plan §4 Second-order linear systems (mass-spring-damper), a short section in Note 118 |
| Impedance of mechanical components | L10 | out-of-scope | impedance/network method for modelling mechanical systems by circuit analogy (2.004 lumped-network modelling); the plan models mechanics by F = ma (plan §4 Newtonian mechanics) |
| Transfer functions in MATLAB and Maple | L11 | out-of-scope | software-tool lecture (MATLAB/Maple); the concept itself is the tf add |
| Operational amplifiers | L12 | out-of-scope | electronics (op-amp circuits), a different field |
| Generalized system modeling | L13 | out-of-scope | cross-domain lumped-element analogies (electrical, mechanical, fluid, thermal; bond-graph style), system-dynamics modelling method outside robotics |
| Modeling rotational systems | L14 | taught | plan §4 Newtonian and rigid-body mechanics (torque, inertia) in Note 117; Note 283 (motors, gears and the joint torque loop) |
| Two-port components | L16 | out-of-scope | two-port network elements (transformers, gyrators) in lumped-network modelling, electrical-engineering method |
| LTI system response | L17 | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). response of linear time-invariant systems |
| Standard input functions: delta, step, ramp, sinusoid | L18 | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). impulse, step, ramp and sinusoid test inputs |
| Poles and zeros | L19 | add | **tf** → RO-06 Feedback control, new Note after Note 118. poles and zeros of a transfer function |
| Standard first- and second-order system responses | L20 | add | **ssresp** → RO-06, extend Note 118 (step response and second-order systems). first-order response and time constant (second-order is Note 118) |
| Higher-order systems, LTI system properties | L21 | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). higher-order responses as sums of modes, dominant poles |
| Effects of poles and zeros | L23 | add | **tf** → RO-06 Feedback control, new Note after Note 118. how pole and zero positions shape the response |
| Closed-loop systems | L24 | add | **feedback** → RO-06, opening section of Note 117 (PD and PID control). open vs closed loop and the closed-loop transfer function; Note 117 lists only PD/PID |
| Steady-state errors | L24 | add | **ssresp** → RO-06, extend Note 118 (step response and second-order systems). steady-state error and system type |
| System stability | L25 | taught | plan §4 Stability of dynamical systems (equilibria, eigenvalues) |
| Routh-Hurwitz criterion | L25 | add | **tf** → RO-06 Feedback control, new Note after Note 118. Routh-Hurwitz test (named) |
| Stability of closed-loop systems | L26 | add | **tf** → RO-06 Feedback control, new Note after Note 118. closed-loop stability from the characteristic equation 1 + KG = 0 |
| Root locus plots | L26-29 | add | **rootlocus** → RO-06 Feedback control, short section in the transfer-function Note. root locus |
| Sinusoidal system response | L30 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. steady-state sinusoidal response |
| Frequency response and pole-zero plots | L31 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. frequency response read from a pole-zero plot |
| Bode plots | L32-34 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. Bode plots |
| Poles and zeros on Bode plots | L33 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. asymptotic Bode sketching from poles and zeros |

## MIT 16.30 Feedback Control Systems (How, Frazzoli), Fall 2010 (MIT OCW)

Source: https://ocw.mit.edu/courses/16-30-feedback-control-systems-fall-2010/pages/lecture-notes/

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| Introduction | L1 | index-noise | course overview lecture |
| Root locus: analysis and examples | L2 | add | **rootlocus** → RO-06 Feedback control, short section in the transfer-function Note. root locus |
| Frequency response methods | L3 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. frequency response |
| Control design using Bode plots | L4 | add | **loopshape** → RO-06 Feedback control, new Note after the sensitivity Note. lead/lag compensator design on Bode plots |
| State-space models | L5 | taught | plan §4 State-space models (x_dot = Ax + Bu) |
| Signals and systems | L5 | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). signals and LTI systems: impulse, convolution, transforms |
| State-space models from transfer functions | L6 | add | **tf** → RO-06 Feedback control, new Note after Note 118. converting between transfer functions and state-space models |
| State-space models: basic properties | L7 | taught | plan §4 State-space models; plan §4 Matrix exponential (e^(At) solves x' = Ax) |
| System zeros | L8 | out-of-scope | invariant (transmission) zeros of multi-input multi-output state-space systems, linear-systems structure theory; single-input zeros are the tf add |
| Transfer function matrices | L8 | out-of-scope | multi-input multi-output transfer-function matrices, multivariable frequency-domain theory beyond the single-loop controllers the plan uses |
| State-space model features (modes) | L9 | add | **modes** → MA 06-calculus, inside the planned Matrix exponential Note (plan §4). modes of a linear system |
| Controllability | L10 | taught | Note 204 (controllability and the rank test) |
| Full-state feedback control | L11 | taught | Note 204 (state feedback u = -Kx) |
| Pole placement | L12 | taught | Note 204 (pole placement) |
| LQ servo | L13 | taught | Note 119 (integral action in state feedback); Note 206 (LQR for tracking a reference) |
| Open-loop and closed-loop estimators | L14 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). observers (closed-loop estimators) vs open-loop simulation of the model |
| Combined estimators and regulators | L15 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). observer-based output feedback, separation principle |
| Adding reference inputs | L16 | taught | Note 206 (LQR for tracking a reference: error coordinates, steady-state target) |
| LQ servo: improving transient performance | L17 | taught | Note 206 (LQR for tracking, with feedforward); Note 119 (integral action) |
| Deterministic linear quadratic regulator (LQR) | L18 | taught | Note 205 (LQR) |
| Linear quadratic Gaussian (LQG) | L19 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). LQG: LQR plus Kalman filter |
| Digital control basics | L20 | add | **sampling** → RO-08, extend Note 136 (Delays and control rate), or RO-06 after the PID Notes. sampled-data (digital) control: sampling, zero-order hold, discretising a controller |
| Systems with nonlinear functions (describing functions) | L21 | out-of-scope | describing functions: nonlinear analysis beyond course level (same verdict as the FBS index in ctrl_ledger) |
| Analysis of nonlinear systems (Lyapunov) | L22 | taught | plan §4 Stability of dynamical systems (Lyapunov functions); Note 199 (Lyapunov certificates) |
| Nonlinear control synthesis | L22 | taught | Note 124 (feedback linearisation) |
| Anti-windup | L23 | taught | Note 119 (integrator windup and actuator saturation) |
| Closed-loop system analysis | L24 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. closed-loop robustness analysis with sensitivity functions |

## Caltech CDS 110/ChE 105 Analysis and Design of Feedback Control Systems (Murray), Spring 2024

Source: https://murray.cds.caltech.edu/Cds110

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| Introduction to feedback and control | W1 | add | **feedback** → RO-06, opening section of Note 117 (PD and PID control). what feedback does: open vs closed loop, robustness to disturbances and model error; Note 117 lists only PD/PID |
| Introduction to python-control | W1 | out-of-scope | software-library tutorial; the concepts are the tf / freqresp adds |
| State space models | W2 | taught | plan §4 State-space models |
| Continuous and discrete time systems | W2 | taught | plan §4 State-space models (discrete-time models x(k+1) = A x(k) + B u(k) by zero-order hold) |
| Phase portraits | W2 | taught | plan §4 State-space models (phase space); plan §4 ODEs and vector fields |
| Stability | W2 | taught | plan §4 Stability of dynamical systems |
| Input/output response of LTI systems | W3 | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). input/output response of LTI systems |
| Matrix exponential | W3 | taught | plan §4 Matrix exponential and logarithm |
| Convolution equation | W3 | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). convolution equation (output = impulse response convolved with input) |
| Linearization around an equilibrium point | W3 | taught | Note 206 (linearising a model around an operating point); plan §5 Taylor linearisation (MA-064) |
| State feedback | W4 | taught | Note 204 (state feedback) |
| Eigenvalue placement | W4 | taught | Note 204 (pole placement) |
| Integral action | W4 | taught | Note 119 (integral action in state feedback) |
| Linear quadratic regulators (LQR) | W4 | taught | Note 205 (LQR) |
| Observers | W5 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). state observers |
| Observability | W5 | taught | Note 80 (observability, concept); the rank test is the observer add |
| Control using estimated state | W5 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). output feedback with an observer, separation principle |
| Kalman filtering | W5 | taught | Note 80 (Kalman filter) |
| Trajectory generation and tracking | W6 | taught | Notes 201-202 (trajectory generation); Note 206 (LQR tracking with feedforward) |
| Two degree of freedom design | W6 | taught | Note 119 (feedforward plus feedback = two degrees of freedom) |
| Gain scheduling | W6 | taught | Note 255 (gain scheduling) |
| Receding horizon / model predictive control | W6 | taught | Note 207 (model predictive control: receding horizon) |
| Frequency domain analysis | W7 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. frequency-domain analysis |
| Bode plots | W7 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. Bode plots |
| Nyquist plots | W7 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. Nyquist plot and criterion |
| Stability margins | W7 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. gain and phase margins |
| Robustness and fundamental tradeoffs | W8 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. robustness to model error and disturbances |
| Sensitivity functions | W8 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. sensitivity and complementary sensitivity |
| Performance specifications | W8 | add | **ssresp** → RO-06, extend Note 118 (step response and second-order systems). rise time, overshoot, settling, steady-state error, bandwidth as specs |
| Bode integral formula | W8 | out-of-scope | fundamental-limits theory (waterbed effect, complex-analysis result); ctrl_ledger gives RHP limits the same verdict |
| Limits due to RHP poles and zeros | W8 | out-of-scope | fundamental-limits theory via maximum modulus (complex analysis); same verdict as ctrl_ledger "pole/zero pair, right half-plane" |
| PID control | W9 | taught | Note 117 (PD and PID control) |
| Frequency domain design | W9 | add | **loopshape** → RO-06 Feedback control, new Note after the sensitivity Note. frequency-domain (loop-shaping) design |
| Windup and anti-windup | W9 | taught | Note 119 (integrator windup and actuator saturation) |

## Stanford CS223A / ME320 Introduction to Robotics (Khatib), Winter 2026

Source: https://cs.stanford.edu/groups/manips/teaching/cs223a/

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| Spatial descriptions | L2 | taught | Note 65 (coordinate frames and the transform tree); plan §4 Rigid-body transforms and homogeneous coordinates |
| Essential math review | R1 | index-noise | review section, no single concept |
| Articulated body systems | L3 | taught | Note 69 (kinematic chains, Denavit-Hartenberg parameters) |
| Forward kinematics | L4 | taught | Note 69 (forward kinematics of an open chain); Note 276 (product of exponentials) |
| Jacobians | L5-7 | taught | Note 277 (manipulator Jacobian) |
| Inverse kinematics | L8 | taught | Note 279 (inverse kinematics: analytic and numerical) |
| Workspace | L8 | taught | Note 276 (task space and workspace) |
| Trajectory generation | L9 | taught | Note 201 (time scaling and polynomial trajectories); Note 202 (via points, splines) |
| Essential physics review | R2 | index-noise | review section, no single concept |
| Dynamics: acceleration and inertia | L10 | taught | Note 220 (rigid-body dynamics in 3D: the inertia matrix); Note 281 (what the mass matrix means) |
| Dynamics: Newton-Euler | L11 | taught | Note 282 (recursive Newton-Euler inverse dynamics) |
| Dynamics: explicit form | L12 | taught | Note 281 (manipulator equation M(q)q'' + c + g = tau) |
| Joint space control | L13 | taught | Note 284 (joint-space control: PD plus gravity, computed torque) |
| Operational space control | L14 | taught | Note 285 (task-space and operational space control) |
| Force control | desc | taught | Note 286 (force control and hybrid motion-force control) |
| Vision-based control | desc | add | **visualservo** → RB-02, new Note after Note 285 (task-space control); uses Note 231 (image Jacobian). visual servoing (image-based and position-based); Note 231 has only the image Jacobian |

## Berkeley EECS C106A/206A Introduction to Robotics (Horowitz, Tennant), Fall 2025

Source: https://pages.github.berkeley.edu/EECS-106/fa25-site/

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| History of robotics | L1 | out-of-scope | history |
| SO(3) group / rigid transformations | L2 | taught | plan §4 Axis-angle, exponential and log maps of rotations (SO(3)); plan §4 Rigid-body transforms (SE(2)/SE(3)) |
| Exponential map | L3 | taught | plan §4 Axis-angle, exponential and log maps of rotations |
| Rodrigues' formula | L3 | taught | plan §4 Matrix exponential and logarithm (gives Rodrigues' formula for rotations) |
| Euler angles | L3 | taught | plan §4 3D rotations: Euler angles and quaternions |
| Quaternions | L4 | taught | plan §4 3D rotations: Euler angles and quaternions |
| SE(3) | L4 | taught | plan §4 Rigid-body transforms and homogeneous coordinates (SE(2)/SE(3)) |
| Twists | L4 | taught | Note 275 (twists, wrenches and screw motion) |
| se(3) exponential map | L5 | taught | Note 275 (screw axis and exponential coordinates of a rigid motion) |
| Screws | L5 | taught | Note 275 (screw motion, screw axis) |
| Chasles' theorem | L6 | add | **chasles** → RB-01, extend Note 275 (twists, wrenches and screw motion). Chasles' theorem named: every rigid motion is a screw motion; Note 275 teaches screw coordinates without the theorem (robo_adds lists the same: extend N275) |
| Joint space and forward kinematics | L7 | taught | Note 69 (forward kinematics); Note 276 (product of exponentials) |
| Product of exponentials | L8 | taught | Note 276 (forward kinematics by the product of exponentials) |
| Manipulator workspace | L9 | taught | Note 276 (task space and workspace) |
| Inverse kinematics: Paden-Kahan subproblems | L9-10 | out-of-scope | book-specific analytic-IK method (Murray-Li-Sastry Ch. 3); Note 279 teaches analytic IK by geometry and wrist splitting plus numerical IK |
| Image formation | L11 | taught | Note 88 (the pinhole camera: projection, intrinsics, extrinsics) |
| Image features | L11 | taught | Note 227 (corner features); Note 228 (descriptors) |
| Image primitives and correspondence | L12 | taught | Note 227 (image filtering, corners); Note 228 (matching descriptors) |
| Two-view geometry | L13 | taught | Note 232 (epipolar geometry); Note 233 (relative pose, triangulation) |
| Spatial and body velocities | L15 | add | **twist-frames** → RB-01, extend Note 275 (twists, wrenches and screw motion). spatial vs body twist of a moving frame (Note 275 gives the twist and adjoint, Note 277 the two Jacobian forms, but no Note teaches the two velocity forms; robo_adds lists 'angular velocity, body/spatial' as extend N275) |
| Generalized velocities | L15 | taught | Note 277 (joint speeds to hand twist) |
| Spatial Jacobian | L16 | taught | Note 277 (manipulator Jacobian, space and body forms) |
| Jacobians | L17 | taught | Note 277 (manipulator Jacobian) |
| Singular value decomposition (SVD) | L18 | taught | MA-057 (SVD geometry), MA-058 (computing the SVD) |
| Singularities | L18 | taught | Note 278 (singularities) |
| Manipulability | L18 | taught | Note 278 (manipulability ellipsoid and measure) |
| Redundant manipulators | L18 | taught | Note 278 (redundancy and self-motion in the null space) |
| Motion planning with Jacobians | L18 | taught | Note 280 (differential IK; straight-line hand motion) |
| Lagrangian dynamics | L19-21 | taught | Note 281 (Lagrangian mechanics and the manipulator equation) |
| Robot control (Controls I-IV) | L22-25 | taught | Note 284 (joint-space control); Note 285 (task-space control); Note 286 (force control) |

## MIT 6.4210/6.4212 Robotic Manipulation (Tedrake), Fall 2025 (plus new Fall 2026 tentative titles)

Source: https://manipulation.csail.mit.edu/Fall2025/schedule.html ; https://manipulation.csail.mit.edu/Fall2026/schedule.html

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| Anatomy of a manipulation system | L1 | index-noise | course overview lecture, no single concept |
| Model-based design and simulation (Drake) | L2 | taught | Note 128 (physics simulators: time steps, contact, Gazebo vs MuJoCo vs Isaac vs Drake) |
| Frames (spatial algebra) | L3 | taught | Note 65 (coordinate frames and the transform tree); plan §4 Rigid-body transforms |
| Kinematics | L4 | taught | Note 69 (forward kinematics); Note 276 (product of exponentials) |
| Differential kinematics via optimization | L5 | add | **diffikqp** → RB-01, extend Note 280 (damped, transpose and differential IK). differential IK as a constrained QP (joint and velocity limits); Note 280 teaches only pseudo-inverse, damped and transpose IK |
| Cameras and point clouds | L6 | taught | Note 88 (pinhole camera); Note 91 (point clouds from depth images) |
| Point cloud registration | L6 | taught | Note 92 (aligning scans: ICP, SVD/Kabsch) |
| Statics and contact | L7 | taught | Note 277 (statics: tau = J^T F); Note 288 (contact types and the friction cone) |
| Grasping | L8 | taught | Note 290 (form and force closure); Note 291 (grasp quality and grasp selection) |
| Motion planning: sampling-based | L9 | taught | Note 110 (RRT); Note 111 (PRM) |
| Motion planning: local optimization | L10 | taught | Note 116 (trajectory optimisation) |
| Motion planning: global optimization | L11 | out-of-scope | research method from the instructor's lab (Graphs of Convex Sets, Marcucci et al. 2023, mixed-integer convex planning); not a standard course topic elsewhere |
| Position control | L12 | taught | Note 284 (joint-space control: PD plus gravity) |
| Force control | L13 | taught | Note 286 (force control) |
| Manipulator control | L14 | taught | Note 284 (computed torque); Note 285 (operational space); Note 287 (impedance control) |
| Programming behaviors: scripts and state machines | L15 | taught | Note 130 (behaviour trees and finite state machines) |
| Behavior trees | L15 | taught | Note 130 (behaviour trees: sequence, fallback, decorator, tick) |
| Object recognition and segmentation | L16 | taught | Note 173 (object detection; using pretrained detectors and segmenters); Note 175 (semantic segmentation) |
| Affordances | L17 | taught | Note 355 (affordance models: where and how to act) |
| Reinforcement learning overview | L18 | taught | Note 1 (the reinforcement learning problem); Note 133 (the robot as an MDP) |
| Policy gradients and PPO | L19 | taught | Note 30 (policy gradient theorem and REINFORCE); Note 39 (PPO) |
| Visuomotor policies: behavior cloning | L20 | taught | Note 165 (behaviour cloning); Note 323 (end-to-end visuomotor policies) |
| Task and motion planning | L21 | taught | Note 293 (task and motion planning) |
| Planning through contact | L22 | taught | Note 306 (multi-contact planning); Note 289 (contact as a hybrid system) |
| Overview of robot learning for manipulation | F26 | taught | Note 323 (end-to-end visuomotor policies); RB-07 chapter |
| Model-based learning | F26 | taught | Note 49 (model-based RL with learned dynamics); Note 333 (learned models for manipulation) |
| Task planning | F26 | taught | Note 293 (task-level planning); Note 354 (language models as task planners) |
| Generative simulation / real-to-sim | F26 | out-of-scope | tentative Fall 2026 research-frontier lecture (generated scenes); the dynamics side of real-to-sim is Note 139 (system identification) |
| World models | F26 | taught | Note 50 (world models and imagined rollouts); Note 356 (video and world models as policies) |
| Post-training (RL) | F26 | taught | Note 358 (RL fine-tuning of a VLA) |
| Learning from low-quality data | F26 | out-of-scope | tentative Fall 2026 research-frontier lecture with no fixed method; offline RL from mixed data is Note 343 |

## MIT 6.8210 (formerly 6.832) Underactuated Robotics (Tedrake), Spring 2024

Source: https://underactuated.csail.mit.edu/Spring2024/schedule.html

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| Robot dynamics and model-based control | L1 | taught | Note 281 (manipulator equation); Note 284 (computed torque) |
| Nonlinear dynamics | L2 | taught | plan §4 ODEs and vector fields; plan §4 Stability of dynamical systems (equilibria) |
| Dynamic programming (continuous state, action, time) | L3-4 | taught | Note 106 (DP with interpolation on continuous spaces); Note 205 (Hamilton-Jacobi-Bellman equation) |
| Acrobots, cart-poles and quadrotors | L5 | add | **underact** → RO-15, new Note after Note 205 (LQR). underactuated systems: cart-pole and acrobot, energy-shaping swing-up, partial feedback linearisation, LQR balance (quadrotor part is Note 221) |
| Neural fitted value iteration | L6 | taught | Note 25 (value prediction as supervised learning); Note 35 (deep Q-networks) |
| Lyapunov analysis | L7 | taught | plan §4 Stability of dynamical systems (Lyapunov functions); Note 199 |
| Computing Lyapunov functions (sums of squares) | L8-9 | out-of-scope | sums-of-squares programming (semidefinite optimisation), research and graduate method |
| Lyapunov / sums-of-squares for control design | L10 | out-of-scope | sums-of-squares control synthesis, research and graduate method |
| Trajectory optimization | L11-12 | taught | Note 116 (trajectory optimisation: shooting, collocation, DDP/iLQR) |
| Trajectory stabilization | L13 | taught | Note 206 (time-varying LQR to hold a robot on a planned trajectory) |
| System identification | L14 | taught | Note 139 (system identification and actuator models) |
| Multibody parameter estimation | L15 | add | **inertialid** → RB-02, new section in Note 282 (inverse and forward dynamics) or Note 139. identifying inertial parameters: dynamics linear in mass/inertia parameters, least-squares fit |
| Learning linear models and deep models | L16 | taught | Note 49 (learned dynamics); Note 139 (system identification) |
| Simple models of walking | L17 | taught | Note 299 (passive walkers, limit cycles); Note 296 (linear inverted pendulum) |
| Hybrid trajectory optimization | L18 | taught | Note 289 (contact as a hybrid system); Note 116 (trajectory optimisation); Note 306 (multi-contact planning by optimisation) |
| Planning and control through contact | L19 | taught | Note 306 (multi-contact planning); Note 289 (contact forces and hybrid systems); Note 302 (convex MPC) |
| Humanoid robots | L20 | taught | RB-04 Notes 295-304 (ZMP, capture point, whole-body control); RB-06 Notes 317-322 |
| Mixed-discrete (combinatorial) and continuous optimization | L21 | add | **miqp** → MA 07-optimisation, extend MA-068 (linear and quadratic programming). mixed-integer programming (binary choice variables, e.g. which foothold or region) |
| Sampling-based kinodynamic motion planning | L22 | taught | Note 112 (kinodynamic RRT) |
| Stochastic dynamics | L23 | taught | Note 68 (probabilistic motion models); Note 7 (MDPs, stochastic transitions) |
| Stochastic control | L24 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). stochastic optimal control of continuous systems: LQG, certainty equivalence (the MDP side is Note 11) |
| Robust control | L25 | taught | Note 141 (robust RL: worst case, robust MDP) |
| Policy search | L25 | taught | Note 43 (black-box policy search); Note 30 (policy gradients) |
| Output feedback | L26 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). output feedback through an observer |
| Feedback motion planning | L27 | taught | Note 106 (feedback planning by DP with interpolation; navigation functions) |
| Imitation learning | L28 | taught | Note 165 (behaviour cloning, DAgger); RB-08 chapter |
| Foundation models | L28 | taught | Note 349 (vision-language-action models and generalist robot policies) |

## CMU 16-745 Optimal Control and Reinforcement Learning (Manchester), Spring 2025

Source: https://optimalcontrol.ri.cmu.edu/

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| Dynamics intro | W1 | taught | plan §4 State-space models |
| Stability | W1 | taught | plan §4 Stability of dynamical systems |
| Discrete-time dynamics | W1 | taught | plan §4 State-space models (discrete-time models); plan §4 Numerical integration of ODEs |
| Optimization intro | W2 | taught | MA-065 (convex and non-convex cost functions); ML-056 (gradient descent) |
| Numerical optimization | W2-3 | taught | MA-064 (Hessian, Newton's method); ML-056 (gradient descent); MA-066 (Lagrange multipliers) |
| Optimal control intro | W3 | taught | Note 205 (LQR, HJB); Note 116 (trajectory optimisation) |
| Regularization and merit functions | W3 | out-of-scope | solver-implementation detail (Hessian regularisation, merit functions in constrained Newton solvers); the plan treats solvers at overview depth (plan §4 Newton-type solvers, Note 208) |
| Pontryagin's minimum principle | W4 | out-of-scope | plan §7 drops PA 15.8 Pontryagin's principle as advanced theory; its practical use (shooting) is Note 116 |
| Shooting methods | W4 | taught | Note 116 (single and multiple shooting) |
| LQR in three ways | W4 | taught | Note 205 (LQR: DP/Riccati recursion, steady Riccati equation) |
| Dynamic programming | W5 | taught | Notes 12-14 (DP); Note 205 (discrete LQ problem by DP) |
| Convexity | W5 | taught | MA-065 (convex and non-convex cost functions); MA-067 (convex sets and functions) |
| Convex model-predictive control | W5 | taught | Note 207 (linear MPC as a quadratic program); Note 302 (convex MPC for legged robots) |
| Nonlinear trajectory optimization | W6 | taught | Note 116 (trajectory optimisation) |
| Differential dynamic programming and iLQR | W6 | taught | Note 116 (trajectory optimisation methods: multiple shooting, collocation, DDP/iLQR) |
| Direct trajectory optimization, collocation | W7 | taught | Note 116 (direct methods: collocation) |
| Sequential quadratic programming (SQP) | W7 | taught | Note 208 (Newton-type solvers: SQP and interior point, overview) |
| SO(3) and quaternions (attitude) | W9 | taught | plan §4 3D rotations: Euler angles and quaternions; plan §4 Axis-angle, exponential and log maps |
| Optimizing with attitude | W9 | out-of-scope | research method (quaternion differential calculus for optimisation, Jackson & Manchester 2021); quadrotor attitude control is Note 225 |
| LQR with attitude, quadrotors | W10 | taught | Note 222 (linearise at hover, LQR or PID) |
| Contact intro | W10 | taught | Note 288 (contact kinematics and types); Note 289 (contact forces) |
| Trajectory optimization for hybrid systems | W10 | taught | Note 289 (contact as a hybrid system); Note 116; Note 306 |
| Data-driven methods | W11 | taught | Note 139 (system identification); Note 49 (learned dynamics) |
| Iterative learning control | W11 | add | **ilc** → RO-15, short section after Note 206 (LQR for tracking with feedforward). iterative learning control: correct a repeated trajectory's feedforward from the last trial's error |
| Stochastic optimal control | W11 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). stochastic optimal control with noisy measurements: certainty equivalence and the separation principle (MDP side is Note 11) |
| LQG | W11 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). LQG |
| Robust control | W12 | taught | Note 141 (robust RL: worst case) |
| Minimax DDP | W12 | out-of-scope | research method (minimax differential dynamic programming, Morimoto et al. 2003) |
| RL from an optimal-control perspective | W13 | taught | Note 211 (MPC and RL: comparing and combining) |
| Case study: driving a car | W13 | taught | RO-21 Notes 250-253 (car dynamics, LQR steering); Note 209 (MPC for path following) |
| Case study: landing a rocket | W14 | out-of-scope | aerospace application (powered-descent guidance), a different field |
| Case study: walking | W14 | taught | RB-04 Notes 296-302 (ZMP, LIPM, convex MPC) |

## CMU 16-385 Computer Vision (Gkioulekas), Spring 2020 (latest offering with a public schedule on the course site)

Source: https://www.cs.cmu.edu/~16385/

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| Image filtering | L2 | taught | Note 227 (image filtering: smoothing and gradient filters) |
| Image pyramids | L3 | taught | Note 227 (image pyramids) |
| Fourier transform | L3 | add | **fourier-transform** → MA 06-calculus (new Note); used in RO-18 (227) and RO-03 sensor signals. Fourier transform of signals and images |
| Hough transform | L4 | add | **hough-transform** → RO-18 (section in 229, next to RANSAC). Hough transform |
| Feature and corner detection | L5 | taught | Note 227 (Harris and Shi-Tomasi corners, FAST) |
| Feature descriptors and matching | L6 | taught | Note 228 (SIFT, ORB, matching) |
| 2D transformations | L7-8 | add | **2d-transform-hierarchy** → RO-18 (section in 229). 2D transform hierarchy (translation, rigid, similarity, affine, projective) |
| Image homographies | L9 | taught | Note 229 (homography) |
| Camera models | L10-11 | taught | Note 88 (pinhole camera); Note 89 (lens distortion) |
| Two-view geometry | L12 | taught | Note 232 (epipolar geometry); Note 233 (relative pose, triangulation) |
| Stereo | L13 | taught | Note 90 (depth from stereo) |
| Radiometry and reflectance | L14-15 | out-of-scope | photometric image formation (radiometry, BRDF), graphics/optics; same verdict as vis_ledger |
| Photometric stereo | L16 | out-of-scope | cv-special: photometric stereo; same verdict as vis_ledger |
| Shape from shading | L16 | out-of-scope | cv-special: shape from a single shaded image under known lighting (reflectance-map method), no robot perception stack uses it |
| Image processing pipeline | L17 | add | **camera-sensor-pipeline** → RO-03 (new Note after 88). camera sensor pipeline: exposure, demosaicing, white balance, gamma, rolling shutter |
| Image classification | L18 | taught | DL-040 (CNN intuition); DL-049 (cat vs dog CNN) |
| Bag of words | L19 | taught | Note 236 (visual place recognition with bag of words) |
| Neural networks | L20-21 | taught | DL-008 to DL-020 (MLP, forward propagation, backpropagation) |
| Convolutional neural networks | L22-23 | taught | DL-040 to DL-053 (CNNs) |
| Optical flow | L24 | taught | Note 230 (optical flow, Lucas-Kanade); Note 231 (dense flow) |
| Alignment (image alignment, Lucas-Kanade) | L25 | taught | Note 230 (Lucas-Kanade: local flow by least squares; pyramidal KLT) |
| Tracking | L26 | taught | Note 230 (KLT tracker); Note 178 (multi-object tracking) |
| Segmentation and graph-based techniques | L27 | out-of-scope | cv-special: graph-cut and normalised-cut segmentation; the plan uses learned segmentation (Note 175); same verdict as vis_ledger |
| Segmentation | L28 | taught | Note 175 (semantic segmentation) |
| Structure from motion | L29 | taught | Note 235 (structure from motion and bundle adjustment) |

## Stanford CS231A Computer Vision: From 3D Perception to 3D Reconstruction and beyond (Savarese, Bohg), Spring 2025

Source: https://web.stanford.edu/class/cs231a/syllabus.html

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| Camera models | L2-3 | taught | Note 88 (pinhole camera) |
| Camera calibration | L3 | taught | Note 89 (camera calibration with a checkerboard, DLT) |
| Single view metrology | L4 | out-of-scope | cv-special: single-view metrology; same verdict as vis_ledger (the vanishing-point basics are vis add projective-points-lines) |
| Epipolar geometry | L5 | taught | Note 232 (epipolar geometry) |
| Stereo systems | L6 | taught | Note 90 (depth from stereo, rectification) |
| Structure from motion | L7 | taught | Note 235 (structure from motion and bundle adjustment) |
| Active stereo | L8 | taught | Note 90 (depth cameras: structured light and time of flight) |
| Volumetric stereo | L8 | out-of-scope | offline multi-view reconstruction (space carving, voxel colouring); vis_ledger gives volumetric graph cuts the same verdict; robots fuse depth into voxel/TSDF maps (Note 97) |
| Fitting and matching | L9 | taught | Note 229 (RANSAC); Note 228 (matching descriptors) |
| Representations and representation learning | L10 | taught | Note 353 (pretrained visual representations for control); plan §4 Contrastive learning objective |
| Monocular depth estimation | L11-12 | add | **learned-depth** → RO-18, new Note after Note 234 (visual odometry), or RO-03 after Note 90. learned depth from a single image (scale ambiguity, foundation depth models) |
| Learning-based stereo | L11-12 | add | **learned-depth** → RO-18, new Note after Note 234 (visual odometry), or RO-03 after Note 90. learned stereo matching |
| Feature tracking | L11-12 | taught | Note 230 (pyramidal KLT tracker) |
| Optical flow | L13 | taught | Note 230 (optical flow); Note 231 (learned optical flow) |
| Scene flow | L13 | out-of-scope | research-only: scene flow; same verdict as vis_ledger |
| Optimal estimation | L14-15 | taught | Note 78 (Bayes filter); Note 80 (Kalman filter); Note 81 (EKF) |
| Neural radiance fields (NeRF) | L16 | add | **neural-scenes** → RO-19, new Note before Note 239 (open-vocabulary 3D semantic maps). neural radiance fields as a 3D scene representation |
| Gaussian splatting | L17 | add | **neural-scenes** → RO-19, new Note before Note 239 (open-vocabulary 3D semantic maps). 3D Gaussian splatting as a 3D scene representation |

## Berkeley CS 185/285 Deep Reinforcement Learning (Levine), Spring 2026

Source: https://rail.eecs.berkeley.edu/deeprlcourse/

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| Behavioral cloning | L2-3 | taught | Note 165 (behaviour cloning) |
| Distributional shift in behavioral cloning | S2 | taught | Note 165 (compounding error and DAgger) |
| RL basics | L4 | taught | Note 1 (the RL problem); Note 7 (MDPs) |
| Policy gradients | L5 | taught | Note 30 (policy gradient theorem and REINFORCE) |
| Actor-critic | L6 | taught | Note 32 (actor-critic) |
| Value-based RL | L7 | taught | Note 21 (Q-learning); Note 14 (value iteration) |
| Q-learning in practice | L8 | taught | Note 35 (DQN); Note 36 (experience replay and target networks); Note 22 (double Q-learning) |
| DQN and SAC | S4 | taught | Note 35 (deep Q-networks); Note 42 (soft actor-critic) |
| Advanced policy gradients | L9-10 | taught | Note 38 (TRPO); Note 39 (PPO); plan §4 Natural gradient and Fisher information |
| Variational inference | L11 | add | **variational-inference** → DL new chapter "Generative models" (section in the planned VAE Note). variational inference and the ELBO |
| Variational inference in RL | L12 | add | **controlinf** → RL-05, short section in Note 42 (soft actor-critic). control as inference: maximum-entropy RL derived as probabilistic inference |
| Control as inference | L13 | add | **controlinf** → RL-05, short section in Note 42 (soft actor-critic). control as inference / soft optimality; Note 42 teaches SAC's entropy bonus but not the inference view |
| Inverse reinforcement learning | S7 | taught | Note 189 (inverse RL, max-entropy IRL) |
| RL for LLMs | L14 | taught | RL-08 Notes 57-62 (RLHF, DPO, GRPO) |
| Model-based RL | L15-16 | taught | Note 45 (models and Dyna); Note 49 (model-based RL with learned dynamics) |
| Offline RL | L17-18 | taught | Note 343 (offline RL and distribution shift); Note 344 (CQL) |
| Exploration | L19 | taught | Note 4 (UCB); Note 182 (curiosity and intrinsic rewards) |
| RL theory | L20 | out-of-scope | proof technique: sample-complexity and error-propagation bounds for fitted Q-iteration |
| Advanced exploration | L23 | taught | Note 182 (curiosity and intrinsic rewards for exploration) |
| Multi-task RL | L24 | taught | Note 171 (multi-task and meta-RL) |
| Challenges and open problems | L25 | index-noise | discussion lecture, no single concept |

## Cornell CS 4756/5756 Robot Learning (Fang), Spring 2026

Source: https://www.cs.cornell.edu/courses/cs4756/2026sp/

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| Introduction to robot learning | L1 | index-noise | course overview lecture |
| Fundamentals of robotic control | L2 | taught | Note 72 (configuration space and degrees of freedom; reading is MR Ch. 2); Note 117 (PD and PID control) |
| Markov decision processes | L3 | taught | Note 7 (Markov decision processes) |
| Deep learning tutorial | L4 | taught | DL-008 to DL-038 (MLPs, backpropagation, optimisers) |
| Imitation learning | L5 | taught | Note 165 (behaviour cloning, DAgger) |
| Value function and dynamic programming | L6 | taught | Note 9 (value functions); Notes 12-14 (DP) |
| Q-learning | L7 | taught | Note 21 (Q-learning) |
| Policy gradients | L8 | taught | Note 30 (policy gradient theorem and REINFORCE) |
| Actor-critic methods | L9 | taught | Note 32 (actor-critic) |
| Deep RL algorithms | L10 | taught | RL-05 Notes 35-42 (DQN, A2C, TRPO, PPO, DDPG, TD3, SAC) |
| Model predictive control | L11 | taught | Note 207 (model predictive control) |
| Dynamics learning | L12 | taught | Note 49 (model-based RL with learned dynamics) |
| Reward shaping and learning | L13 | taught | Note 146 (reward shaping and its risks); Note 57 (reward models from human preferences); Note 189 (inverse RL) |
| Simulation | L14 | taught | Note 128 (physics simulators); Note 135 (parallel simulation) |
| Camera models | L15 | taught | Note 88 (pinhole camera) |
| 2D visual representations | L16 | taught | Note 353 (pretrained visual representations); DL-051 (pretrained models) |
| 3D visual representations | L17 | taught | Note 91 (point clouds); Note 97 (voxels, octrees, signed distance) |
| State estimation | L18 | taught | Note 78 (Bayes filter); Notes 80-82 (Kalman, EKF, particle filter) |
| End-to-end visuomotor policy learning | L19 | taught | Note 323 (end-to-end visuomotor policies) |
| Transfer learning | L20 | taught | DL-053 (transfer learning) |
| Multi-task learning | L21 | taught | Note 171 (multi-task and meta-RL) |
| Generative models | L22 | taught | plan §4 DL new chapter "Generative models" (VAE, diffusion, flow matching, GANs) |
| Sequence models: RNN, Transformer, Transformer policy | L23 | taught | DL-055 (why RNN); DL-071 (transformers); Note 346 (Decision Transformer); Note 349 (VLA) |
| Hierarchical decision making | L24 | taught | Note 184 (options, hierarchical RL); Note 357 (hierarchical VLAs) |
| Open-world robotics | L25 | index-noise | frontier survey lecture, no single concept |
