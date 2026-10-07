# Scope gap: robot arms, legged and humanoid mechanics, and model-based control

> **Plan of record:** [robotics.md](robotics.md). This doc is evidence: its rows (IDs `ME-NNN`), sources and checks. "Note N" or "RO N" below means the earlier 188-Note draft (2026-10-07), not today's plan.


> **Plan of record:** `docs/books-scope/robotics.md` (25 chapters, 188 Notes). This doc lists what that plan is missing in one area: how arms, legs and humanoid bodies move, and the classical (model-based) controllers for them. It is a scoping list only, not study Notes.

**Summary.**

- **Method.** Surveys first, to see how the field divides itself. Then the textbooks give the section list and the teaching depth. Every row points to a survey family (§0) or a textbook section.
- **Surveys used (5):** Wensing et al. 2024 (legged optimal control), Gu et al. 2026 (humanoid locomotion and manipulation), Ha et al. 2025 (learning-based legged locomotion, with its model-based baselines), Moro & Sentis 2017 (whole-body control), Bohg et al. 2014 (grasp synthesis). Sahbani et al. 2012 adds the analytic grasping side.
- **Main textbook:** Lynch & Park, *Modern Robotics* (MR). Its section list was read from the contents pages of the free official PDF ([hades.mech.northwestern.edu/images/7/7f/MR.pdf](https://hades.mech.northwestern.edu/images/7/7f/MR.pdf), linked from the [book page](https://hades.mech.northwestern.edu/index.php/Modern_Robotics), which also links the four-course Coursera series). Tedrake, *Underactuated Robotics*: chapter and section headings read from [underactuated.mit.edu](https://underactuated.mit.edu/) and its chapter pages ([simple_legs.html](https://underactuated.mit.edu/simple_legs.html), [humanoids.html](https://underactuated.mit.edu/humanoids.html)).
- **Checked at chapter level only** (Springer pages need cookies, so chapter titles came from Crossref): Siciliano et al. 2009 *Robotics: Modelling, Planning and Control* (doi [10.1007/978-1-84628-642-1](https://doi.org/10.1007/978-1-84628-642-1)), Corke 2023 *Robotics, Vision and Control* 3rd ed. (doi [10.1007/978-3-031-06469-2](https://doi.org/10.1007/978-3-031-06469-2)), Kajita et al. 2014 *Introduction to Humanoid Robotics* (doi [10.1007/978-3-642-54536-8](https://doi.org/10.1007/978-3-642-54536-8)). These are cited by chapter only.
- **Not used:** Craig, *Introduction to Robotics*. No official contents page could be reached; Crossref has only book reviews. MR covers the same ground.
- **Papers:** each was checked on Crossref or arXiv. The DOI is given in §6.
- **Row counts:** **115 rows**: **12 covered**, **30 partial**, **67 new**, **6 dropped**. By kind: robotics 62, control 34, maths 19 (counted by script over the §1 tables).

Status key: **covered** = already in robotics.md (RO Note number) or an MA/ML/DL Note; **partial** = the basics exist, the new part is named; **new** = nowhere in our plan; **dropped** = left out, with a reason.

## 0. Domain map from surveys

The five surveys split the area the same way. Each family below is a block of rows in §1.

| Family (survey section) | Sub-families | Standard baselines | Rows |
|---|---|---|---|
| **Describing the body** (MR ch.2–4; Wensing II-B) | rigid-body pose, rotations, twists and wrenches; joints and degrees of freedom; forward kinematics; robot description files; floating base | product of exponentials, DH, URDF | A, B, C |
| **Velocity, force and inverse kinematics** (MR ch.5–6) | Jacobian, statics, singularities, redundancy; analytic and numerical IK | Newton–Raphson IK, damped least squares | D, E |
| **Dynamics** (MR ch.8; Wensing II-B; Tedrake App. B) | Newton–Euler, Lagrange, the manipulator equation, inverse and forward dynamics, task-space dynamics, contact | recursive Newton–Euler, manipulator equation | G |
| **Contact** (Wensing III; MR ch.12) | contact models (hybrid, complementarity), contact scheduling, friction | friction cone, rigid contact | G, K |
| **Trajectories** (MR ch.9; Wensing V) | time scaling, via points, time-optimal scaling; trajectory optimisation methods | quintic polynomial, trapezoid profile; collocation, multiple shooting, DDP | H |
| **Arm control** (MR ch.11; Siciliano ch.8–9) | joint-space and task-space motion control; force, hybrid, impedance and admittance control | PD + gravity compensation, computed torque, operational space control | I |
| **Whole-body control** (Wensing VI; Gu VI; Moro & Sentis) | tasks and task Jacobians; closed-form (null-space) vs optimisation (QP); strict vs weighted priorities; loco-manipulation | null-space projection, weighted QP, hierarchical QP | J |
| **Grasping** (Bohg 2014; Sahbani 2012; MR ch.12) | analytic (contact models, form and force closure, quality) vs data-driven (known, familiar, unknown objects) | force closure, Ferrari–Canny quality | K |
| **Simplified models of legged robots** (Wensing IV; Tedrake ch.4–5; Gu V-A) | ZMP and support polygon, LIPM, capture point, SLIP, centroidal dynamics, single rigid body | ZMP preview control, capture point, Raibert hopper | L |
| **Model-based legged control** (Wensing V; Gu V; Ha 1.3) | MPC with simple models, whole-body MPC, contact planning; heuristics and CPGs | convex MPC (MIT Cheetah 3), Raibert foot placement, CPG | L |
| **Control + learning** (Ha §6; Gu VII-D, IX-A) | learn controller parameters, learn a high-level policy over a model-based controller, model-based control guiding RL | model-based baselines RL is compared against | L |
| **Humanoid motion from humans** (Gu VII-C; Darvish 2023) | human motion data, kinematic retargeting, teleoperation | IK-based retargeting | M |

**Out of this area** (noted so it is not lost): wheeled-robot models and odometry (MR ch.13; RO Note 50), general MPC, LQR, pure pursuit and path tracking (control and navigation docs), visual servoing (Siciliano ch.10, Corke ch.15–16; vision doc), tactile sensing (Gu III).

## 1. Topic-by-topic table

"Our Note" uses RO Note numbers from robotics.md and MA/ML/DL labels. "new MA: X" is a maths Note already planned in robotics.md §3.

### A. Rigid-body motion

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| ME-001 | MR 3.1 | Moving a body in the plane: rotate, then translate | maths | covered | new MA: Rigid-body transforms and homogeneous coordinates |
| ME-002 | MR 3.3.1 | Homogeneous transformation matrix; its inverse; chaining frames | maths | covered | new MA: Rigid-body transforms; MA-054 |
| ME-003 | MR App. B.1–B.3 | Euler angles, roll-pitch-yaw, unit quaternions | maths | covered | new MA: 3D rotations: Euler angles and quaternions |
| ME-004 | MR 3.2.1 | Rotation matrix read as a frame: its columns are the new axes; inverse = transpose; using it to change frames | maths | partial | MA-053, MA-054 show rotation as a linear map; new: columns as axes, R⁻¹ = Rᵀ, "move a vector" vs "re-describe it in another frame" |
| ME-005 | MR 3.2.2 | Angular velocity as a vector along the spin axis | maths | partial | RO Note 56 short mechanics section names angular velocity; new: the vector form and how it changes between frames |
| ME-006 | MR 3.2.2 | Skew-symmetric matrix: the cross product written as a matrix | maths | new | MA-050 only names the cross product; needed for every velocity formula below |
| ME-007 | MR 3.2.3 | Axis-angle and exponential coordinates of a rotation; Rodrigues' formula | maths | new | Any rotation = one turn by some angle about one axis |
| ME-008 | MR 3.2.3 | Matrix exponential and matrix logarithm | maths | new | e^(At) solves x' = Ax; it turns an axis and an angle into a rotation matrix and back |
| ME-009 | MR 3.3.2 | Twist: angular and linear velocity of a body as one 6-number vector; the adjoint map that moves it between frames | maths | new | The velocity language of MR ch.4–11 |
| ME-010 | MR 3.3.3 | Screw axis and exponential coordinates of a rigid motion | maths | new | Every rigid motion is a turn about a line plus a slide along it |
| ME-011 | MR 3.4 | Wrench: force and torque as one 6-number vector; moving it between frames | maths | partial | Torque is in RO Note 56 section; new: the paired force-torque vector and its frame change |

### B. Configuration and robot description

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| ME-012 | MR 2.1–2.2 | Degrees of freedom of a body and of a robot | robotics | covered | RO Note 54 |
| ME-013 | MR 2.2.1–2.2.2 | Joint types (revolute, prismatic, spherical...) and Grübler's count of degrees of freedom | robotics | partial | RO Note 54 has DOF; new: the joint catalogue and counting DOF of a mechanism |
| ME-014 | MR 2.4 | Holonomic and nonholonomic constraints | robotics | covered | RO Note 50 |
| ME-015 | MR 2.5 | Task space and workspace: where the hand can reach | robotics | new | The reachable set, and why it differs from C-space |
| ME-016 | MR 4.2, 8.8 | Robot description files (URDF): links, joints, masses and inertias | robotics | new | The file every simulator (Isaac, MuJoCo) and every controller loads |
| ME-017 | Wensing II-B; Tedrake App. B | Floating base: a legged robot's body is 6 extra unpowered degrees of freedom | robotics | new | Why a walking robot can push only through its feet |

### C. Forward kinematics

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| ME-018 | MR ch.4 intro | Forward kinematics of an open chain | robotics | covered | RO Note 52 |
| ME-019 | MR App. C | Denavit–Hartenberg parameters | robotics | covered | RO Note 52 (PA row "Denavit-Hartenberg parameters") |
| ME-020 | PA ch.3 | Kinematic trees (branching bodies such as humanoids) | robotics | covered | RO Note 52 |
| ME-021 | MR 4.1.1–4.1.3, C.5 | Product of exponentials: hand pose from screw axes, in the base frame and the hand frame; how it compares with DH | robotics | new | The DH alternative MR uses for everything after ch.4 |

### D. Velocity kinematics and statics

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| ME-022 | MR 5.1.1–5.1.4 | Manipulator Jacobian (space and body forms): joint speeds to hand twist | robotics | partial | MA-063 Jacobian; new: the arm Jacobian, built column by column from the screw axes |
| ME-023 | MR 5.1.5 | Analytic Jacobian (rates of Euler angles) vs geometric Jacobian | robotics | new | Short section: why two Jacobians exist |
| ME-024 | MR 5.2 | Statics: joint torques that hold a hand force, τ = Jᵀ F | robotics | new | The same Jacobian maps forces backwards |
| ME-025 | MR 5.3 | Singularities: the Jacobian loses rank and the hand cannot move in some direction | robotics | partial | MA-058 rank and null space; new: what it looks like on an arm (stretched-out elbow, aligned wrist axes) |
| ME-026 | MR 5.4; Yoshikawa 1985 | Manipulability ellipsoid and measure | robotics | partial | MA-057 SVD geometry (circle to ellipse); new: velocity and force ellipsoids of an arm, and a single score |
| ME-027 | MR 6.3; Siciliano ch.3 | Redundancy and self-motion in the null space | robotics | new | More joints than the task needs: the arm can move without moving the hand |

### E. Inverse kinematics

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| ME-028 | MR ch.6 intro | The IK problem: none, one, many or infinitely many answers | robotics | new | Working backwards from hand pose to joint angles |
| ME-029 | MR 6.1, 6.1.1–6.1.2 | Analytic IK: 2-link planar arm, wrist-splitting for 6-joint arms | robotics | new | Closed-form answers with geometry and atan2 |
| ME-030 | MR 6.2.1 | Newton–Raphson for solving equations (root finding) | maths | partial | MA-064 has Newton for minimising; new: the root-finding form with a non-square Jacobian |
| ME-031 | MR 6.2.2 | Numerical IK: iterate with the Jacobian pseudo-inverse | robotics | partial | MA-060 pseudo-inverse; new: the IK loop, start guesses, stopping rules |
| ME-032 | Wampler 1986; Nakamura & Hanafusa 1986 | Damped least squares IK | robotics | partial | ML-063 ridge has the same (JᵀJ + λI)⁻¹ form; new: why damping keeps steps sane near singularities |
| ME-033 | Siciliano ch.3 | Jacobian-transpose IK | robotics | new | Gradient descent on hand error; no inverse needed |
| ME-034 | MR 6.3 | Differential (inverse velocity) IK: q̇ = J⁺ V, and its use for tracking a moving target | robotics | new | The workhorse of teleoperation and retargeting |

### F. Closed chains

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| ME-035 | MR ch.7 | Closed chains and parallel mechanisms (Stewart–Gough platform) | robotics | dropped | robotics.md already drops closed-chain rows (PA 4.15, 7.5); no navigation, legged, humanoid or RL Note needs it |

### G. Dynamics and contact

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| ME-036 | MR 8.2.1 | One rigid body in 3D: F = ma plus Euler's equation; the 3×3 inertia matrix | maths | partial | RO Note 56 short mechanics section; new: rotational equation and the inertia matrix in 3D |
| ME-037 | MR 8.1.1; Tedrake App. B | Lagrangian mechanics: L = kinetic − potential energy; Euler–Lagrange equation on a 2-link arm | maths | new | robotics.md dropped PA 13.10 ("simulators give the dynamics"); it is needed now, at worked-example depth only, for the mass matrix, computed torque and operational space control |
| ME-038 | MR 8.1.2–8.1.3; Tedrake App. B | Manipulator equation M(q)q̈ + c(q,q̇) + g(q) = τ; what the mass matrix means | robotics | new | The one equation behind every controller in I and J |
| ME-039 | MR 8.1.4, 8.3 | Recursive Newton–Euler inverse dynamics (torques for a wanted motion) | robotics | new | Outward pass for speeds, inward pass for forces |
| ME-040 | MR 8.5 | Forward dynamics: solve for accelerations, then integrate | robotics | new | What a simulator does each step; builds on new MA: numerical integration of ODEs |
| ME-041 | MR 8.6 | Dynamics in task space: the hand's apparent mass Λ = (J M⁻¹ Jᵀ)⁻¹ | robotics | new | Needed by operational space control |
| ME-042 | MR 8.7 | Constrained dynamics: contact forces as Lagrange multipliers | robotics | partial | MA-066 Lagrange multipliers; new: the multiplier is the constraint force |
| ME-043 | MR 8.9.1–8.9.5 | Motors, gearing, reflected inertia, friction, flexible joints | robotics | partial | RO Note 83 actuator models; new: gear ratio, reflected inertia, friction models |
| ME-044 | Wensing III-A1; Tedrake ch.17 | Contact as a hybrid system: modes switch on touch-down and lift-off; impacts | robotics | new | Why legged control is hard to optimise |
| ME-045 | Wensing III-A2 | Complementarity contact model: force only when touching, touching only when force | maths | new | Optional short section |
| ME-046 | Wensing III-B | Contact scheduling: fixed gait sequence vs contact-implicit planning | robotics | new | Optional; names the two families |
| ME-047 | Featherstone 2008 | Articulated-body and other fast recursive algorithms | robotics | dropped | Implementation detail inside simulators and libraries (Pinocchio, MuJoCo) |

### H. Trajectory generation

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| ME-048 | MR 9.1 | Path vs trajectory; time scaling | robotics | new | Separate "where" from "when" |
| ME-049 | MR 9.2.1 | Straight-line paths in joint space and in task space (including SE(3)) | robotics | new | Joint lines are easy; hand lines need IK on the way |
| ME-050 | MR 9.2.2 | Cubic and quintic polynomial time scaling | maths | partial | ML-060 polynomials; new: picking the coefficients from start and end speed and acceleration |
| ME-051 | MR 9.2.2 | Trapezoidal velocity profile and S-curve | robotics | new | The profile industrial arms use |
| ME-052 | MR 9.3 | Via points and spline trajectories | robotics | new | Smooth curves through several waypoints |
| ME-053 | MR 9.4 | Time-optimal time scaling under torque limits (phase plane) | robotics | new | Optional depth |
| ME-054 | PA 14.9; Wensing V-A–V-C | Trajectory optimisation methods: multiple shooting, collocation, DDP/iLQR | control | partial | RO Note 77; new: the three solution families named in Wensing V |

### I. Arm control

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| ME-055 | MR 11.1 | Feedforward plus feedback; motion vs force control | control | partial | RO Note 56; new: the feedforward + feedback split |
| ME-056 | MR 11.2 | Error dynamics of a second-order system: overshoot, settling time, damping ratio, natural frequency | control | partial | new MA: Stability of dynamical systems; new: reading and choosing PD gains from the error response |
| ME-057 | MR 11.3.1–11.3.3 | Control with velocity inputs, in joint space and task space | control | new | Kinematic control, as used by most commercial arms and by RL with velocity actions |
| ME-058 | MR 11.4.1 | PD plus gravity compensation | control | partial | RO Note 56 PD; new: the gravity term g(q) |
| ME-059 | Siciliano ch.8 | Independent-joint (decentralised) control vs centralised control | control | partial | RO Note 56; new: one PID per joint vs a controller that uses the whole model |
| ME-060 | MR 11.4.2 | Computed torque (inverse dynamics control, feedback linearisation) | control | new | Cancel the dynamics, then PD on the error |
| ME-061 | MR 11.4.3 | Task-space motion control with torque inputs | control | new | Control the hand directly |
| ME-062 | Khatib 1987 | Operational space control: task-space inertia, Jᵀ F, dynamically consistent null space | control | new | The basis of whole-body control |
| ME-063 | MR 11.5 | Force control | control | new | Press with a set force |
| ME-064 | MR 11.6.1–11.6.2 | Hybrid motion–force control; natural and artificial constraints | control | new | Move along a surface while pressing into it |
| ME-065 | MR 11.7.1; Hogan 1985 | Impedance control: behave like a virtual spring and damper | control | new | Measure motion, command force |
| ME-066 | MR 11.7.2 | Admittance control | control | new | Measure force, command motion; for stiff, position-controlled arms |
| ME-067 | MR 11.8 | Low-level joint torque control loop | control | partial | RO Notes 80, 83; new: the inner torque loop under a PD target |
| ME-068 | Martín-Martín et al. 2019 | Impedance targets as an RL action space | control | partial | RO Note 80 action spaces; new: the policy outputs a target pose and stiffness |
| ME-069 | MR 11.9 | Robust and adaptive control | control | dropped | Named in MR's "other topics" only; beyond beginner depth; RO Notes 82–83 handle model error the RL way |

### J. Whole-body control and task priorities

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| ME-070 | Wensing VI-A1–VI-A2; Gu VI-A | Tasks and task Jacobians: any quantity to control (hand pose, CoM, posture) is a "task" | control | new | The common language of WBC |
| ME-071 | Siciliano & Slotine 1991; Moro & Sentis | Strict task priority by null-space projection | control | partial | MA-058 null space; new: the projector N = I − J⁺J and stacking tasks |
| ME-072 | Sentis & Khatib 2005; Gu VI-B | Whole-body control in closed form (prioritised operational space control) | control | new | Khatib's method extended to a floating-base humanoid |
| ME-073 | Gu VI-C; Wensing VI-B | QP-based whole-body control: one quadratic program with weighted tasks, dynamics, contact and torque limits | control | partial | MA-068 quadratic programming; new: the variables (accelerations, contact forces, torques), costs and constraints |
| ME-074 | Escande et al. 2014; Wensing VI-B2 | Hierarchical QP (stack of tasks): strict priorities with inequalities | control | new | Solve QPs in priority order |
| ME-075 | Wensing VI-A4 | Inequality tasks: joint limits, torque limits, collision avoidance | control | new | Short section inside the QP Note |
| ME-076 | Gu VI-D1 | Loco-manipulation in WBC: the held object as an external wrench | control | new | Optional |
| ME-077 | Wensing II-D | WBC as the layer that tracks a plan from a simpler model | control | new | Where WBC sits in the stack: plan, MPC, WBC, joint PD |

### K. Contact and grasping

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| ME-078 | MR 12.1.1–12.1.2 | Contact kinematics: rolling, sliding, breaking free | robotics | new | What a single touch allows |
| ME-079 | MR 12.1.5; Sahbani 2012 | Contact types: point without friction, point with friction, soft finger | robotics | new | |
| ME-080 | MR 12.2.1 | Coulomb friction and the friction cone (and its pyramid approximation) | maths | new | Also used by every WBC and legged MPC (J, L) |
| ME-081 | MR 12.1.6–12.1.7 | Form closure | robotics | new | Held by shape alone |
| ME-082 | MR 12.2.3 | Force closure | robotics | new | Held by friction against any push |
| ME-083 | MR 12.2; Sahbani 2012 | Grasp matrix: contact forces to object wrench | robotics | new | |
| ME-084 | Ferrari & Canny 1992 | Grasp quality: the largest push a grasp can resist | robotics | new | The standard analytic score |
| ME-085 | Bohg et al. 2014; Sahbani 2012 | Analytic vs data-driven grasp synthesis; known, familiar and unknown objects | robotics | partial | RO Note 153 (grasping from data); new: the map of methods and the analytic side |
| ME-086 | MR 12.3 | Manipulation beyond grasping: pushing, nonprehensile | robotics | covered | RO Note 151 (PA 12.7) |
| ME-087 | PA 7.4 | Manipulation planning (transit and transfer) | robotics | covered | RO Note 151 |

### L. Legged robots: balance, simple models and model-based control

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| ME-088 | Raibert 1986; Tedrake ch.4 | Gait vocabulary: walk, trot, pace, bound, gallop; stance and swing; duty factor | robotics | partial | RO Note 90 (gaits from rewards); new: the names and timing diagrams |
| ME-089 | Kajita ch.3; Tedrake 5 | Centre of mass, support polygon, static vs dynamic balance | robotics | new | Static balance: CoM stays over the feet |
| ME-090 | Tedrake 5 (CoP and ZMP); Vukobratović & Borovac 2004 | Centre of pressure and zero-moment point (ZMP) | robotics | new | Where the ground's push acts; must stay inside the support polygon |
| ME-091 | Kajita 2001; Kajita ch.4 | Linear inverted pendulum model (LIPM) | robotics | new | CoM at fixed height on a massless leg: one linear equation |
| ME-092 | Tedrake 5 (ZMP planning); Kajita 2003 | ZMP walking: footsteps, then ZMP path, then CoM path by preview control | control | new | The classic humanoid walking pipeline; uses RO Note 174 (LQR) |
| ME-093 | Pratt et al. 2006; Tedrake 5 (push recovery) | Capture point: where to step to stop | robotics | new | Push recovery from the LIPM |
| ME-094 | Englsberger et al. 2015 | Divergent component of motion (3D capture point) control | control | new | Optional; the capture point used as a walking controller |
| ME-095 | Tedrake 4 (SLIP) | Spring-loaded inverted pendulum (SLIP) for running | robotics | new | The template model of running and hopping |
| ME-096 | Tedrake 4 (rimless wheel, compass gait) | Passive walkers, limit cycles and Poincaré maps | maths | new | Optional; stable walking as a repeating loop |
| ME-097 | Raibert 1986; Tedrake 4 (MIT Leg Lab hoppers) | Raibert hopping controller: foot placement for speed, thrust for height, hip torque for posture | control | new | The heuristic still used in legged MPC and RL (Ha 1.3) |
| ME-098 | Ijspeert 2008; Ha 1.3 | Central pattern generators (CPGs) | control | new | Coupled oscillators make rhythm; still used as RL action parameterisations |
| ME-099 | Orin et al. 2013; Tedrake 5 (centroidal dynamics); Wensing IV-A | Centroidal dynamics: only contact forces and gravity change the whole body's momentum; centroidal momentum matrix | robotics | new | The key simple model of modern legged control |
| ME-100 | Di Carlo et al. 2018; Wensing IV-B | Single rigid body model of a quadruped | robotics | new | Treat the body as one block pushed by the feet |
| ME-101 | Di Carlo et al. 2018; Gu V-A | Convex MPC for legged robots: choose foot forces by a QP over a short horizon | control | new | The main model-based baseline for quadrupeds; needs MPC from the control doc |
| ME-102 | Gu V-B–V-C | Whole-body and mixed-fidelity MPC | control | new | Optional; names the step up from simple models |
| ME-103 | Gu IV | Multi-contact planning (search, optimisation, learning) | robotics | new | Optional; choosing which hands and feet touch where |
| ME-104 | Bloesch et al. 2013 | Legged state estimation: fuse leg kinematics with the IMU | robotics | partial | RO Note 64 EKF; new: feet in contact as velocity measurements |
| ME-105 | Ha §6; Gu IX-A | Model-based vs learned legged control: what each does well | robotics | partial | RO Note 108 does this for navigation; new: the legged comparison against ZMP, MPC and WBC baselines |
| ME-106 | Ha 6.1–6.4; Gu VII-D | Combining control and learning: learn controller parameters, learn a high-level policy over MPC/WBC, use MPC to guide RL | control | partial | RO Notes 146, 154; new: the four combination families |

### M. Humanoids: motion from humans

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| ME-107 | Kajita ch.5; Gu VI | Whole-body motion generation and control for humanoids | control | covered | Rows in block J and L (this doc) |
| ME-108 | Gu VII-C1; Loper et al. 2015 | Human motion data: motion capture, video, body models (SMPL) | robotics | new | What the input to retargeting looks like |
| ME-109 | Gleicher 1998; Gu VII-C3 | Kinematic retargeting: scale, map joints, solve IK to match key points under joint limits | robotics | partial | RO Note 149 uses retargeted data; new: how retargeting itself works |
| ME-110 | He et al. 2024 (H2O) | Filtering retargeted motions that the robot cannot follow | robotics | covered | RO Note 149 (RL H.5) |
| ME-111 | Darvish et al. 2023 | Teleoperation of humanoids: live retargeting with differential IK | robotics | partial | RO Note 149 (teleop use); new: the real-time IK loop and feedback to the operator |
| ME-112 | MR 13.5 | Mobile manipulation: one Jacobian for base and arm together | robotics | new | Optional; links arms to the navigation chapters |

### N. Dropped (beyond beginner depth or outside this area)

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| ME-113 | Wensing III-A3–A4 | Contact pathologies and hybrid differentiability | maths | dropped | Research-level theory |
| ME-114 | Wensing V-D | Contact-implicit numerical methods | control | dropped | Research-level; row G "contact scheduling" names the idea |
| ME-115 | Gu V-D | Speed-ups for nonlinear MPC | control | dropped | Implementation detail |

## 2. Prerequisites between the new concepts

Arrows mean "learn this first". Existing Notes are in brackets.

- [new MA: Rigid-body transforms] + [new MA: 3D rotations] -> rotation matrix as a frame -> **skew-symmetric matrix** -> **angular velocity**.
- [new MA: ODEs] + skew matrix -> **matrix exponential** -> **axis-angle / Rodrigues** -> **twist** -> **screw motion** -> **product of exponentials** [RO 52 for DH].
- Twist + [MA-063 Jacobian] -> **manipulator Jacobian** -> **statics (Jᵀ F)**, **singularities** [MA-058], **manipulability** [MA-057], **redundancy**.
- Jacobian + [MA-064 Newton] + [MA-060 pseudo-inverse] -> **numerical IK** -> **damped least squares** [ML-063] -> **differential IK** -> **kinematic retargeting**, **teleoperation**.
- [RO 56 mechanics section] + Lagrangian -> **manipulator equation** -> **inverse dynamics (RNEA)**, **forward dynamics** [new MA: numerical integration] -> **task-space dynamics**.
- Manipulator equation + [RO 56 PD] + second-order error dynamics -> **PD + gravity compensation** -> **computed torque** -> **task-space control** -> **operational space control** -> **null-space priority** -> **closed-form WBC**.
- Operational space control + [MA-068 QP] + **friction cone** -> **QP-based WBC** -> **hierarchical QP**.
- Task-space control + wrench -> **force control** -> **hybrid motion–force**; **impedance** and **admittance** control -> impedance as RL action.
- Wrench + friction cone + **convex hull** -> **form / force closure** -> **grasp quality** -> analytic vs data-driven grasping [RO 153].
- Centre of mass + convex hull -> **support polygon** -> **ZMP** -> **LIPM** -> **ZMP preview control** [RO 174 LQR] and **capture point** -> DCM control.
- Floating base + wrench -> **centroidal dynamics** -> **single rigid body model** -> **convex MPC** (needs MPC from the control doc) -> **WBC tracks the MPC plan**.
- Path vs trajectory -> **polynomial time scaling** -> via points -> time-optimal scaling.
- All baselines (ZMP, capture point, Raibert, convex MPC, WBC) -> **model-based vs learned** -> **combining control and learning** [RO 146, 154].

## 3. Suggested learning order

The RL-first order of robotics.md stays. These blocks slot into the classical core and in front of the legged, humanoid and manipulation chapters.

**Block 1: rigid-body motion (just before RO Note 52).** Rotation matrix as a frame; skew matrix; angular velocity; matrix exponential; axis-angle; twists and wrenches; screws.

**Block 2: arm kinematics (extends RO-08 after Note 52).** Joint types; workspace; URDF; product of exponentials; Jacobian; statics; singularities and manipulability; redundancy; IK (analytic, Newton, damped least squares, Jacobian transpose, differential IK).

**Block 3: dynamics and trajectories (after RO Note 56).** One rigid body in 3D; Lagrangian; manipulator equation; inverse and forward dynamics; task-space dynamics; motors and gearing; path vs trajectory, time scaling, via points.

**Block 4: arm control (before RO-21 Manipulation).** Feedforward + feedback; second-order error dynamics; velocity-input control; PD + gravity; computed torque; task-space control; operational space control; force, hybrid, impedance and admittance control; impedance as an RL action.

**Block 5: contact and grasping (inside RO-21, before Note 152).** Contact types; friction cone; convex hull; form and force closure; grasp matrix; grasp quality; analytic vs data-driven grasping.

**Block 6: legged models and baselines (before RO-20).** Gaits; support polygon; ZMP; LIPM; ZMP preview control; capture point; SLIP; Raibert hopper; CPGs; floating base; centroidal dynamics; single rigid body; convex MPC; legged state estimation; model-based vs learned; combining them.

**Block 7: whole-body control and humanoid motion (inside RO-20, before Note 149).** Tasks; null-space priority; closed-form WBC; QP-based WBC; hierarchical QP; human motion data; kinematic retargeting; teleoperation.

**Optional depth (with RO-23):** time-optimal scaling; analytic Jacobian; complementarity contact; contact scheduling; DCM control; passive walkers; whole-body MPC; multi-contact planning; mobile manipulation; loco-manipulation WBC.

## 4. New maths the area needs that MA lacks

Not repeated from robotics.md §3, which already plans: rigid-body transforms and homogeneous coordinates; 3D rotations (Euler angles, quaternions); ODEs and vector fields; state-space models; numerical integration; stability of dynamical systems; the Newtonian mechanics short section in RO Note 56. Those are prerequisites here and are only extended where noted.

| Concept | What | Where | First needed by |
|---|---|---|---|
| Skew-symmetric matrix | the cross product ω × v written as a matrix [ω]v | MA 05-linear-algebra (new Note, or a section of the planned rigid-body transforms Note) | Angular velocity (block A) |
| Matrix exponential and logarithm | e^(At) as the solution of x' = Ax; series definition; for rotations it gives Rodrigues' formula | MA 06-calculus (new Note after the planned ODEs Note) | Axis-angle and exponential coordinates |
| Axis-angle and exponential coordinates | one axis and one angle for any rotation | extend the planned MA Note "3D rotations: Euler angles and quaternions" | Product of exponentials |
| Twists, wrenches and the adjoint | 6-vectors for velocity and force; how they change frame | short RO section in the first kinematics Note (MR treats it as robotics, ch.3) | Manipulator Jacobian |
| Newton–Raphson root finding | solve f(x) = 0 by repeated linearisation; non-square Jacobian uses the pseudo-inverse | extend MA-064 (it has Newton for minimising) | Numerical IK |
| Damped least squares | (JᵀJ + λI)⁻¹Jᵀ: ridge applied to a Jacobian | short section in the IK Note, recapping ML-063 | Damped least squares IK |
| Null-space projector and weighted pseudo-inverse | N = I − J⁺J; pseudo-inverse with a weight (mass) matrix | MA 05-linear-algebra (new Note after MA-060) | Redundancy; task priority; operational space control |
| Convex hull | smallest convex shape around a set of points | MA 07-optimisation (short section in MA-067 convex sets) | Support polygon; force closure |
| Second-order linear systems | mass-spring-damper; natural frequency, damping ratio; under-, over-, critically damped | extend the planned MA Note "Stability of dynamical systems" | Error dynamics and PD gain choice |
| Lagrangian mechanics (worked-example depth) | L = T − V; Euler–Lagrange gives M(q)q̈ + c + g = τ | short RO section, next to the Newtonian mechanics section (physics, not MA, per CONTEXT.md) | Manipulator equation |
| 3D rigid-body rotation dynamics | inertia matrix, Euler's equation | extend the RO Note 56 mechanics short section | One rigid body in 3D; centroidal dynamics |
| Coulomb friction cone and pyramid | force must lie inside a cone; linear pyramid makes it QP-friendly | short RO section in the contact Note | Force closure; QP-based WBC; convex MPC |
| Polynomial boundary-value fitting | find cubic/quintic coefficients from start and end conditions (a small linear solve) | short RO section in the time-scaling Note | Polynomial time scaling |

## 5. Notes on this doc

- **One reversal of a robotics.md drop.** PA 13.10 (Lagrangian mechanics) was dropped because "simulators give the dynamics". The manipulator equation it produces is used by computed torque, operational space control, WBC and centroidal dynamics, so it returns at worked-example depth (2-link arm only).
- **MPC.** Convex MPC (block L) needs general MPC, which robotics.md lacks. That belongs to the control doc; this doc only lists the legged use.
- **Humanoid weight.** With blocks J, L and M, humanoids gain model-based context (about 20 rows) before RO Notes 148–150.

## 6. Sources checked

| Source | Checked on |
|---|---|
| Lynch & Park 2017, *Modern Robotics* (preprint of the Cambridge UP book) | official free PDF contents pages, [hades.mech.northwestern.edu/images/7/7f/MR.pdf](https://hades.mech.northwestern.edu/images/7/7f/MR.pdf); book page with Coursera links [hades.mech.northwestern.edu/index.php/Modern_Robotics](https://hades.mech.northwestern.edu/index.php/Modern_Robotics) |
| Tedrake, *Underactuated Robotics* (MIT course notes) | [underactuated.mit.edu](https://underactuated.mit.edu/), [simple_legs.html](https://underactuated.mit.edu/simple_legs.html), [humanoids.html](https://underactuated.mit.edu/humanoids.html) |
| Siciliano et al. 2009 | Crossref chapter records, doi 10.1007/978-1-84628-642-1 (chapters 1–12) |
| Corke 2023, 3rd ed. | Crossref chapter records, doi 10.1007/978-3-031-06469-2 (chapters 1–16) |
| Kajita et al. 2014 | Crossref chapter records, doi 10.1007/978-3-642-54536-8 (chapters 1–6) |
| Wensing et al. 2024, "Optimization-Based Control for Dynamic Legged Robots", IEEE T-RO | doi [10.1109/TRO.2023.3324580](https://doi.org/10.1109/TRO.2023.3324580); sections from [arXiv 2211.11644](https://arxiv.org/html/2211.11644) |
| Gu et al. 2026, "Humanoid Locomotion and Manipulation: Current Progress and Challenges in Control, Planning, and Learning", IEEE/ASME T-Mech | doi [10.1109/TMECH.2025.3579247](https://doi.org/10.1109/TMECH.2025.3579247); sections from [arXiv 2501.02116](https://arxiv.org/html/2501.02116) |
| Ha et al. 2025, "Learning-based legged locomotion: State of the art and future perspectives", IJRR | doi [10.1177/02783649241312698](https://doi.org/10.1177/02783649241312698); sections from [arXiv 2406.01152](https://arxiv.org/html/2406.01152) |
| Moro & Sentis 2017, "Whole-Body Control of Humanoid Robots", in *Humanoid Robotics: A Reference* | doi [10.1007/978-94-007-7194-9_51-1](https://doi.org/10.1007/978-94-007-7194-9_51-1) (Crossref; record only) |
| Bohg et al. 2014, "Data-Driven Grasp Synthesis—A Survey", IEEE T-RO | doi [10.1109/TRO.2013.2289018](https://doi.org/10.1109/TRO.2013.2289018); abstract on [arXiv 1309.2660](https://arxiv.org/abs/1309.2660) |
| Sahbani et al. 2012, "An overview of 3D object grasp synthesis algorithms", RAS | doi [10.1016/j.robot.2011.07.016](https://doi.org/10.1016/j.robot.2011.07.016) |
| Darvish et al. 2023, "Teleoperation of Humanoid Robots: A Survey", IEEE T-RO | doi [10.1109/TRO.2023.3236952](https://doi.org/10.1109/TRO.2023.3236952) |
| Khatib 1987, operational space formulation | doi [10.1109/JRA.1987.1087068](https://doi.org/10.1109/JRA.1987.1087068) |
| Hogan 1985, impedance control part I | doi [10.1115/1.3140702](https://doi.org/10.1115/1.3140702) |
| Pratt et al. 2006, capture point | doi [10.1109/ICHR.2006.321385](https://doi.org/10.1109/ICHR.2006.321385) |
| Kajita et al. 2001, 3D LIPM | doi [10.1109/IROS.2001.973365](https://doi.org/10.1109/IROS.2001.973365) |
| Kajita et al. 2003, ZMP preview control | doi [10.1109/ROBOT.2003.1241826](https://doi.org/10.1109/ROBOT.2003.1241826) |
| Vukobratović & Borovac 2004, ZMP | doi [10.1142/S0219843604000083](https://doi.org/10.1142/S0219843604000083) |
| Englsberger et al. 2015, DCM | doi [10.1109/TRO.2015.2405592](https://doi.org/10.1109/TRO.2015.2405592) |
| Orin, Goswami & Lee 2013, centroidal dynamics | doi [10.1007/s10514-013-9341-4](https://doi.org/10.1007/s10514-013-9341-4) |
| Di Carlo et al. 2018, MIT Cheetah 3 convex MPC | doi [10.1109/IROS.2018.8594448](https://doi.org/10.1109/IROS.2018.8594448) |
| Raibert 1986, "Legged robots", CACM (and the book *Legged Robots That Balance*, MIT Press 1986) | doi [10.1145/5948.5950](https://doi.org/10.1145/5948.5950); book confirmed by its 1986 IEEE Expert review, doi 10.1109/MEX.1986.4307016 (MIT Press page returned 403) |
| Ijspeert 2008, CPG review | doi [10.1016/j.neunet.2008.03.014](https://doi.org/10.1016/j.neunet.2008.03.014) |
| Bloesch et al. 2013, legged state estimation | doi [10.7551/mitpress/9816.003.0008](https://doi.org/10.7551/mitpress/9816.003.0008) |
| Siciliano & Slotine 1991, multiple tasks in redundant robots | doi [10.1109/ICAR.1991.240390](https://doi.org/10.1109/ICAR.1991.240390) |
| Sentis & Khatib 2005, whole-body behaviours | doi [10.1142/S0219843605000594](https://doi.org/10.1142/S0219843605000594) |
| Escande, Mansard & Wieber 2014, hierarchical QP | doi [10.1177/0278364914521306](https://doi.org/10.1177/0278364914521306) |
| Wampler 1986, damped least squares IK | doi [10.1109/TSMC.1986.289285](https://doi.org/10.1109/TSMC.1986.289285) |
| Nakamura & Hanafusa 1986, singularity-robust IK | doi [10.1115/1.3143764](https://doi.org/10.1115/1.3143764) |
| Yoshikawa 1985, manipulability | doi [10.1177/027836498500400201](https://doi.org/10.1177/027836498500400201) |
| Ferrari & Canny 1992, grasp quality | doi [10.1109/ROBOT.1992.219918](https://doi.org/10.1109/ROBOT.1992.219918) |
| Martín-Martín et al. 2019, impedance as RL action space | doi [10.1109/IROS40897.2019.8968201](https://doi.org/10.1109/IROS40897.2019.8968201) |
| Gleicher 1998, retargeting | doi [10.1145/280814.280820](https://doi.org/10.1145/280814.280820) |
| Loper et al. 2015, SMPL | doi [10.1145/2816795.2818013](https://doi.org/10.1145/2816795.2818013) |
| Featherstone 2008, *Rigid Body Dynamics Algorithms* | doi [10.1007/978-1-4899-7560-7](https://doi.org/10.1007/978-1-4899-7560-7) |
| Wieber, Tedrake & Kuindersma 2016, "Modeling and Control of Legged Robots" | doi [10.1007/978-3-319-32552-1_48](https://doi.org/10.1007/978-3-319-32552-1_48) (record only; superseded here by Wensing 2024) |
| He et al. 2024 (H2O) | already verified in reinforcement-learning.md (row H.5) |
