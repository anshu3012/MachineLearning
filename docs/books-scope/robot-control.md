# Gap scope: mobile robot motion and control

> **Plan of record:** [robotics.md](robotics.md). This doc is evidence: its rows (IDs `CT-NNN`), sources and checks. "Note N" or "RO N" below means the earlier 188-Note draft (2026-10-07), not today's plan.


**Summary.** This is a scoping list only, not study Notes. It finds what the RO plan (`docs/books-scope/robotics.md`, 188 Notes) is missing on how a mobile robot is *modelled* and *steered*: wheeled and car models, tyres, path tracking, state feedback, LQR, MPC, trajectory generation and quadrotors.

The method was survey-first. Five surveys and comparison papers were read first to split the area into families (§0). Textbooks then gave the teaching depth and the section numbers. Every row cites a survey family or a textbook section.

**How the sources were checked.** Every source below was opened on an official page; no cookies and no members-only content were used.

| Short name | Source | How it was checked |
|---|---|---|
| **PA16** | Paden, Čáp, Yong, Yershov, Frazzoli 2016, *A survey of motion planning and control techniques for self-driving urban vehicles* | arXiv [1604.07446](https://arxiv.org/abs/1604.07446); section list read from the arXiv PDF |
| **WE22** | Wensing, Posa, Hu, Escande, Mansard, Del Prete 2022, *Optimization-based control for dynamic legged robots* | arXiv [2211.11644](https://arxiv.org/abs/2211.11644); section list read from the PDF |
| **AR24** | Artuñedo, Moreno-Gonzalez, Villagra 2024, *Lateral control for autonomous vehicles: a comparative evaluation*, Annual Reviews in Control 57:100910 | arXiv [2311.07987](https://arxiv.org/abs/2311.07987); section list read from the PDF |
| **NG20** | Nguyen, Kamel, Alexis, Siegwart 2020, *Model predictive control for micro aerial vehicles: a survey* | arXiv [2011.11104](https://arxiv.org/abs/2011.11104); section list read from the PDF |
| **SU22** | Sun, Romero, Foehn, Kaufmann, Scaramuzza 2022, *A comparative study of nonlinear MPC and differential-flatness-based control for quadrotor agile flight*, IEEE T-RO | arXiv [2109.01365](https://arxiv.org/abs/2109.01365); section list read from the PDF |
| **MR** | Lynch & Park, *Modern Robotics* (Cambridge 2017) | free official preprint [MR-v2.pdf](https://hades.mech.northwestern.edu/images/2/25/MR-v2.pdf) from the [authors' page](https://hades.mech.northwestern.edu/index.php/Modern_Robotics); contents pages read (ch.8, 9, 11, 13) |
| **RVC3** | Corke, *Robotics, Vision and Control*, 3rd ed., Python (Springer 2023) | chapter list from the author's page [petercorke.com/rvc3p](https://petercorke.com/rvc3p/home/); section numbers from the author's official code companion [RVC3-python notebooks](https://github.com/petercorke/RVC3-python/tree/main/notebooks) (chap3, chap4, chap9). Springer pages sit behind a sign-in challenge and were not used |
| **MPC** | Rawlings, Mayne, Diehl, *Model Predictive Control: Theory, Computation, and Design*, 2nd ed. (Nob Hill 2017, 3rd printing 2020) | free official PDF from the authors' site, [MPC-book-2nd-edition-3rd-printing.pdf](https://sites.engineering.ucsb.edu/~jbraw/mpc/MPC-book-2nd-edition-3rd-printing.pdf); contents pages read |
| **FBS** | Åström & Murray, *Feedback Systems*, 2nd ed. (Princeton 2021) | free official PDF [fbs-public_24Jul2020.pdf](http://www.cds.caltech.edu/~murray/books/AM08/pdf/fbs-public_24Jul2020.pdf); section list from the [authors' wiki](https://fbswiki.org/wiki/index.php/Feedback_Systems:_An_Introduction_for_Scientists_and_Engineers) |
| **UR** | Tedrake, *Underactuated Robotics*, MIT course notes (2024 version) | official course site [underactuated.mit.edu](https://underactuated.mit.edu/); chapter list read there |
| **RAJ** | Rajamani, *Vehicle Dynamics and Control*, 2nd ed. (Springer 2012) | contents pages (ch.1–5) from the publisher's reading sample, [e-bookshelf PDF](https://content.e-bookshelf.de/media/reading/L-614337-f1649bd9f8.pdf). Later chapters (tyre models, stability control) were not visible, so no row cites them |
| **SN09** | Snider 2009, *Automatic steering methods for autonomous automobile path tracking*, CMU-RI-TR-09-08 | [CMU RI page](https://publications.ri.cmu.edu/automatic-steering-methods-for-autonomous-automobile-path-tracking/) and its [PDF](https://publications.ri.cmu.edu/storage/publications/pub_files/2009/2/Automatic_Steering_Methods_for_Autonomous_Automobile_Path_Tracking.pdf); contents read |

Papers, each checked on Crossref (DOI) or the CMU RI page:

| Paper | Check |
|---|---|
| Coulter 1992, *Implementation of the pure pursuit path tracking algorithm*, CMU-RI-TR-92-01 | [CMU RI page](https://publications.ri.cmu.edu/implementation-of-the-pure-pursuit-path-tracking-algorithm) |
| Kanayama, Kimura, Miyazaki, Noguchi 1990, "A stable tracking control method for an autonomous mobile robot", ICRA | [10.1109/ROBOT.1990.126006](https://doi.org/10.1109/ROBOT.1990.126006) |
| Thrun et al. 2006, "Stanley: the robot that won the DARPA Grand Challenge", J. Field Robotics | [10.1002/rob.20147](https://doi.org/10.1002/rob.20147) |
| Hoffmann, Tomlin, Montemerlo, Thrun 2007, "Autonomous automobile trajectory tracking for off-road driving", ACC (the Stanley steering law in detail) | [10.1109/ACC.2007.4282788](https://doi.org/10.1109/ACC.2007.4282788) |
| Kong, Pfeiffer, Schildbach, Borrelli 2015, "Kinematic and dynamic vehicle models for autonomous driving control design", IV | [10.1109/IVS.2015.7225830](https://doi.org/10.1109/IVS.2015.7225830) |
| Williams, Drews, Goldfain, Rehg, Theodorou 2016, "Aggressive driving with model predictive path integral control", ICRA | [10.1109/ICRA.2016.7487277](https://doi.org/10.1109/ICRA.2016.7487277) |
| Di Carlo, Wensing, Katz, Bledt, Kim 2018, "Dynamic locomotion in the MIT Cheetah 3 through convex model-predictive control", IROS | [10.1109/IROS.2018.8594448](https://doi.org/10.1109/IROS.2018.8594448) |
| Flash & Hogan 1985, "The coordination of arm movements: an experimentally confirmed mathematical model" (minimum jerk), J. Neuroscience | [10.1523/JNEUROSCI.05-07-01688.1985](https://doi.org/10.1523/JNEUROSCI.05-07-01688.1985) |
| Mellinger & Kumar 2011, "Minimum snap trajectory generation and control for quadrotors", ICRA | [10.1109/ICRA.2011.5980409](https://doi.org/10.1109/ICRA.2011.5980409) |
| Richter, Bry, Roy 2016, "Polynomial trajectory planning for aggressive quadrotor flight in dense indoor environments", ISRR (Springer STAR) | [10.1007/978-3-319-28872-7_37](https://doi.org/10.1007/978-3-319-28872-7_37) |
| Mahony, Kumar, Corke 2012, "Multirotor aerial vehicles: modeling, estimation, and control of quadrotor", IEEE RAM 19(3) | [10.1109/MRA.2012.2206474](https://doi.org/10.1109/MRA.2012.2206474) (metadata only; full text is paywalled, so it is cited as a source, not used for the map) |
| Lee, Leok, McClamroch 2010, "Geometric tracking control of a quadrotor UAV on SE(3)", CDC | [10.1109/CDC.2010.5717652](https://doi.org/10.1109/CDC.2010.5717652) |

**Checked but not used:**
- Siegwart, Nourbakhsh & Scaramuzza, *Introduction to Autonomous Mobile Robots*, 2nd ed. (MIT Press 2011). The MIT Press page returned 403 or an empty page, and no official section-level contents could be found (only full-book copies on third-party sites, which were not used). Its kinematics chapter covers the same ground as MR ch.13 and RVC3 ch.4, so nothing is lost.
- Schwenzer et al. 2021, "Review on model predictive control: an engineering perspective" (Int. J. Adv. Manuf. Technol. 117, CC BY), [10.1007/s00170-021-07682-3](https://doi.org/10.1007/s00170-021-07682-3). It is confirmed on Crossref, but the full text sits behind Springer's sign-in redirect. MPC (the book) and NG20 give the MPC map instead.

**Row counts.** **112 rows**: **18 covered**, **19 partial**, **75 new**. By kind: **maths 19**, **robotics 7**, **control 86** (control = steering laws, controllers and models of motion); vision 0. Five new rows are marked optional, and Block 7 (car dynamics) is optional as a whole.

**Main findings.**
1. **Path tracking is missing entirely.** No pure pursuit, Stanley, Kanayama, cross-track error or "drive to a point / line / pose". The plan goes from PID (Note 56) straight to DWA/TEB (Note 106), with nothing on following a path that has already been planned.
2. **MPC is missing.** It shows up only as one Nav2 controller name (MPPI, in row N.1). Linear MPC as a QP, nonlinear MPC, convex MPC for legs and sampling MPC (MPPI) are all new.
3. **LQR sits in the optional chapter** (Note 174, continuous-time, RO-23). MPC, LQR steering and convex MPC all need discrete-time LQR, so it should move into the core.
4. **Controllability was dropped** (PA 15.5, together with STLC). The simple linear rank test is beginner level, and LQR and MPC need it. Drop only STLC.
5. **Car and tyre models stop at the "simple car"** (Note 50). The bicycle model, Ackermann steering, slip angle and cornering stiffness are new.
6. **Trajectory generation** (polynomials, splines, minimum jerk and snap, time scaling) and **quadrotor dynamics and control** are new. Note 134 (agile flight) assumes them.

**Out of this area (left to other gap files):** manipulator control (computed torque, impedance, force control; MR 11.4–11.8, RVC3 9.4–9.6), state estimation (MPC ch.4 moving-horizon estimation), visual servoing (RVC3 ch.15–16), and global planning (PA16 §IV).

Status key:
- **covered**: already in robotics.md or an MA/ML/DL Note (named), or already planned as a new MA Note there.
- **partial**: the basics are planned or written; the new part is named.
- **new**: in neither.

---

## 0. Domain map from surveys

The families of this area, and which survey gave each one. **Bold** marks the standard baselines that every comparison uses.

| Family | Sub-families / standard methods | Survey that gave it | Teaching depth from |
|---|---|---|---|
| A. Vehicle models | **kinematic single-track (bicycle)** model; inertial effects: dynamic bicycle, tyre slip; unicycle / differential drive; omnidirectional | PA16 §III.A–B; AR24 §3; SU22 §III.B (quadrotor model); NG20 §II (MAV model) | MR 13; RVC3 4.1; RAJ 2, 4; SN09 3.1, 4.1; Kong 2015 |
| B. Path stabilisation (geometric, kinematic) | **pure pursuit**; rear-wheel feedback; **front-wheel feedback (Stanley)** | PA16 §V.A.1–3; SN09 §2 | RVC3 4.1.1.1–4.1.1.4; Coulter 1992; Hoffmann 2007 |
| C. Trajectory tracking (timed reference) | control-Lyapunov design (**Kanayama**); output feedback linearisation | PA16 §V.B.1–2 | MR 13.3.4; Kanayama 1990; UR 3 |
| D. Linear optimal and classical control | **PID**; **LQR**; LQR with feedforward; preview control | AR24 §4.1, 4.4; SN09 §4.2–4.4; PA16 §V.D (linear parameter-varying) | FBS 5–7, 11; MPC 1.3; UR 8; RAJ 3 |
| E. Predictive control | **linear MPC**; **nonlinear MPC**; linear vs nonlinear trade-off; sampling MPC (MPPI); robust / fault-tolerant (left out) | PA16 §V.C; AR24 §4.5; NG20 §III.A–D; SU22 §IV.A | MPC ch.1, 2, 8; Williams 2016 |
| F. Legged optimisation-based control | contact models and contact schedules; simplified models (**single rigid body**, LIP, centroidal); OCP solvers (multiple shooting); whole-body control | WE22 §II–VI | Di Carlo 2018; UR 4–5 |
| G. Trajectory generation | path vs trajectory, time scaling; polynomials; via points; **minimum snap**; variational / collocation methods | PA16 §IV.B–C; SU22 §VI.A–D | MR 9; RVC3 3.3; Mellinger & Kumar 2011; Richter 2016; Flash & Hogan 1985 |
| H. Quadrotor control | **differential flatness + geometric (non-predictive) control**; **NMPC**; INDI (left out); cascaded attitude and position loops | SU22 §II.A–B, §IV.A–C; NG20 §III | RVC3 4.2; Mellinger & Kumar 2011; Lee 2010; Mahony 2012; UR 3 |
| I. Learning + control | deep RL vs MPC; RL tracking of model-based plans | NG20 §III.E; WE22 §VII; SU22 §VIII | links to RO Notes 134, 146 |

**What the map adds over the starting brief:** omnidirectional bases, path coordinates (Frenet), rear-wheel feedback, preview and feedforward steering, cascaded loops, sampling MPC (MPPI), offset-free MPC, real-time MPC solvers, simplified legged models (LIP and ZMP), whole-body control, time scaling, via points, and tracker evaluation metrics.

---

## 1. Topic-by-topic table

### 1.1 Wheeled and vehicle kinematic models (family A)

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| CT-001 | MR 13.1 | Types of wheeled robots: omnidirectional vs nonholonomic | robotics | partial | Note 50 has holonomic vs nonholonomic. New: which wheel types (omni, mecanum, fixed, steered) give which |
| CT-002 | MR 13.2.1, 13.2.3 | Omnidirectional (mecanum) base model and control | control | new | Wheel speeds from a wanted body velocity; such a base can drive sideways, so control is simple |
| CT-003 | MR 13.3.1, PA16 III.A | Unicycle model (forward speed v, turn rate ω) | control | partial | Note 50 has differential drive. New: the unicycle as the shared simple model that most trackers are written for |
| CT-004 | MR 13.3.1 | Differential drive: wheel speeds to (v, ω) and back | control | covered | Note 50 (PA 13.3) |
| CT-005 | MR 13.3.1, PA16 III.A, RVC3 4.1.1 | Nonholonomic constraint: a wheel cannot slide sideways | control | covered | Note 50 |
| CT-006 | MR 13.4 | Wheel odometry | robotics | covered | Note 51 |
| CT-007 | SN09 3.1, PA16 III.A, RAJ 2.2 | Kinematic bicycle model (front wheel steers, rear wheel follows) | control | partial | Note 50 has the "simple car". New: the bicycle form, the choice of reference point (rear axle or centre of mass) and the body slip angle β |
| CT-008 | SN09 2.1, RVC3 4.1.1 | Steering angle, wheelbase and turning radius (tan δ = L / R); curvature | control | partial | Note 50. New: curvature as the quantity every tracker sets |
| CT-009 | RAJ 2.2 | Ackermann steering geometry (inner wheel turns more than outer) | robotics | new | Why a real car has two different front-wheel angles, and why the bicycle model can lump them into one |
| CT-010 | RVC3 4.1.1, MR 13.3.1 | Speed and steering limits (maximum steer, minimum turning radius) | control | partial | Note 76 (Dubins, motion limits). New: limits as input bounds a controller must respect |
| CT-011 | SN09 3.1.1, RAJ 2.5, PA16 V | Path coordinates (Frenet frame): distance along the path s, sideways offset, heading error | control | new | The coordinates every path tracker and path-following MPC uses |
| CT-012 | MR 13.3.2 | Controllability of a car in plain words (parallel parking) | control | new | A car can reach any pose even though it cannot slide sideways. Lie brackets stay dropped (PA 15.11) |
| CT-013 | Kong 2015 | Kinematic vs dynamic model: when the kinematic model is enough | control | new | At low speed tyres barely slip, so the kinematic model works; at high speed it does not |

### 1.2 Vehicle dynamics and tyre slip (family A, inertial effects)

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| CT-014 | MR 8.2, RVC3 3.2.1 | Rigid-body dynamics (F = ma, torque, inertia) | maths | covered | Planned short section inside Note 56 ("Newtonian and rigid-body mechanics") |
| CT-015 | RAJ 2.3, PA16 III.B, SN09 4.1 | Dynamic bicycle model (sideways force, yaw rate, yaw inertia) | control | new | Adds forces and mass to the bicycle model |
| CT-016 | RAJ 2.3, SN09 4.1 | Tyre slip angle | control | new | The angle between where a tyre points and where it actually moves |
| CT-017 | SN09 4.1, RAJ 2.3 | Cornering stiffness: the linear tyre model | control | new | Sideways tyre force ≈ stiffness × slip angle, valid for small slip |
| CT-018 | SN09 4.1 (tyre data figures), PA16 III.B | Tyre force saturation and friction limit | control | new | The force stops growing once the tyre slides; why cars skid. Name the Pacejka "magic formula" only |
| CT-019 | RAJ 4.1.2, 4.1.3 | Longitudinal slip ratio: why driving and braking force depends on slip | control | new | Wheel spins faster or slower than the ground goes past |
| CT-020 | RAJ 4.1.1, 4.1.4 | Longitudinal dynamics: aerodynamic drag and rolling resistance | control | new | Forces that set the throttle needed for a speed |
| CT-021 | RAJ 2.5, 2.6 | Error dynamics with respect to the road (lateral and yaw error states) | control | new | The linear model used by LQR steering |
| CT-022 | RAJ 3.3 | Steady-state cornering and understeer | control | new | Why a car needs more steering at speed than geometry says |
| CT-023 | RAJ 5.3–5.5 | Cruise control: upper level (wanted acceleration) and lower level (throttle, brake) | control | new | Speed tracking, the longitudinal half of a vehicle controller |
| CT-024 | WE22 III.A, UR 5 | Contact forces and the friction cone | control | new | A foot can push but not pull, and cannot push too far sideways; needed by convex MPC |

### 1.3 State feedback, stability and controllability (family D)

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| CT-025 | FBS 6.1, MPC 1.2.1 | Linear state-space model ẋ = Ax + Bu | maths | covered | Planned new MA "State-space models" |
| CT-026 | FBS 5.3, MPC 2.4 | Equilibria and stability; eigenvalues with negative real part | maths | covered | Planned new MA "Stability of dynamical systems" (with MA-056) |
| CT-027 | FBS 5.4, UR 9 | Lyapunov functions | maths | covered | Planned new MA "Stability of dynamical systems" |
| CT-028 | FBS 6.2 | Matrix exponential: the solution of ẋ = Ax | maths | new | Needed to turn a continuous model into a discrete one |
| CT-029 | MPC 1.2.4 | Discrete-time models x(k+1) = A x(k) + B u(k); discretising a continuous model | maths | partial | Planned MA "Numerical integration of ODEs" has Euler steps. New: zero-order hold, and the discrete A and B |
| CT-030 | FBS 6.4, PA16 V | Linearising a model around an operating point or a moving reference | maths | partial | MA-063, MA-064 (Jacobian, Taylor). New: linearising around a trajectory, giving time-varying A and B |
| CT-031 | FBS 7.1, MPC 1.3.5, 2.4.4 | Controllability (reachability) and the rank test | maths | new | Robotics.md dropped PA 15.5 (with STLC). Bring back only the linear rank test: LQR and MPC need it |
| CT-032 | MPC 1.4.5 | Observability | maths | partial | Kalman filter Note 63. New: can the sensors reveal the whole state at all; the twin of controllability |
| CT-033 | FBS 7.2, 7.3, RAJ 3.1 | State feedback u = −Kx and pole placement | control | new | Choose K so the closed loop's eigenvalues are stable and fast enough |
| CT-034 | MR 11.2 | Error dynamics and the step response (overshoot, settling time, damping) | control | new | Words to judge any controller from a plot |
| CT-035 | FBS 7.4 | Integral action in state feedback | control | partial | Note 56 has the I term of PID. New: adding an integral state to remove steady error |
| CT-036 | FBS 11.4, 11.5 | Integrator windup and actuator saturation | control | new | What goes wrong when the motor maxes out |
| CT-037 | MR 11.3, RVC3 9.4.1 | Feedforward plus feedback | control | new | Feedforward does what the model says is needed; feedback fixes the rest |
| CT-038 | RVC3 9.1.6, 9.1.7, RAJ 5.4–5.5, SU22 II.A | Cascaded control loops (fast inner loop, slower outer loop) | control | new | Velocity loop inside position loop; attitude loop inside position loop on a drone |
| CT-039 | UR 3, PA16 V.B.2 | Feedback linearisation | control | new | Cancel the nonlinear part with the input, then use a linear controller. Beginner example: a point just ahead of a unicycle |

### 1.4 Moving to a point, line or pose, and path tracking (families B and C)

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| CT-040 | RVC3 4.1.1.1 | Moving to a point | control | new | Steer toward the goal and set speed from distance |
| CT-041 | RVC3 4.1.1.2 | Following a line | control | new | Steer on distance-from-line and on heading |
| CT-042 | RVC3 4.1.1.4 | Moving to a pose (position and heading), polar-coordinate controller | control | new | Arrive at a spot facing the right way |
| CT-043 | PA16 V (Problems V.1, V.2) | Path following vs trajectory tracking | control | new | A path has no clock; a trajectory says where to be at each time |
| CT-044 | SN09 2, AR24 5.1.3, PA16 V | Cross-track error and heading error | control | new | The two numbers every tracker drives to zero |
| CT-045 | Coulter 1992, SN09 2.2, PA16 V.A.1, RVC3 4.1.1.3 | Pure pursuit | control | new | Aim at a point a fixed distance ahead on the path; fit the arc that reaches it |
| CT-046 | SN09 2.2.1 | Look-ahead distance and its tuning (look-ahead grows with speed) | control | new | Short: tight but wobbly; long: smooth but cuts corners |
| CT-047 | Thrun 2006, Hoffmann 2007, SN09 2.3, PA16 V.A.3 | Stanley controller (front-wheel feedback) | control | new | Steer = heading error + arctan(gain × cross-track error / speed); won the 2005 DARPA Grand Challenge |
| CT-048 | SN09 2.3.1 | Tuning the Stanley controller | control | new | Effect of the gain and of low-speed softening |
| CT-049 | PA16 V.A.2 | Rear-wheel feedback path controller | control | new | Third baseline in PA16. Optional |
| CT-050 | Kanayama 1990, PA16 V.B.1, MR 13.3.4 | Kanayama tracker: error in the robot's own frame, virtual reference robot, Lyapunov-proved stable | control | new | Track a timed trajectory: feedforward from the reference speeds plus error feedback |
| CT-051 | RAJ 3.11, SN09 4.4 | Preview (look-ahead) control | control | new | Use the road ahead, not only the current error. Optional |
| CT-052 | SN09 4.3, RAJ 3.2 | Feedforward steering from path curvature | control | new | Removes the steady error that pure feedback leaves on curves |
| CT-053 | SN09 5, AR24 6 | Comparing trackers: speed, curvature, tuning effort | control | new | No tracker wins everywhere (SN09 §5–6) |
| CT-054 | AR24 5.1.3 | Tracker metrics: RMS and peak lateral error, steering effort | control | new | How to score a tracker; links to Note 115 (navigation metrics) |
| CT-055 | robotics.md (RL N.1) | Local planners as controllers (DWA, TEB) | control | covered | Note 106 |
| CT-056 | PA16 V.D | Gain scheduling / linear parameter-varying control | control | new | Different gains at different speeds. Optional, one section |

### 1.5 LQR (family D)

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| CT-057 | MPC 1.3.1–1.3.3 | Discrete-time LQ problem solved by dynamic programming (Riccati recursion) | maths | partial | Note 174 (optional, continuous-time HJB and LQR). New: discrete time, solved backward like value iteration (Note 18) |
| CT-058 | MPC 1.3.4, 1.3.6, UR 8 | Infinite-horizon LQR and the steady Riccati equation | maths | partial | Note 174. New: discrete form; K computed once. Move into the core |
| CT-059 | SN09 4.2.1 | Choosing the Q and R weights | control | new | Q prices error, R prices effort |
| CT-060 | MPC 1.5.1 | LQR for tracking a reference (error coordinates, steady-state target) | control | new | Regulate the error, not the state |
| CT-061 | SN09 4.2, RAJ 3.1, AR24 4.1 | LQR steering on the dynamic bicycle model | control | new | The standard optimal lane-keeping baseline |
| CT-062 | UR 8 | Time-varying LQR to hold a robot on a planned trajectory | control | new | Linearise along the trajectory, one gain per time step |
| CT-063 | SN09 4.3, MR 11.3 | LQR with feedforward | control | new | Same idea as §1.3 feedforward, applied to LQR steering |

### 1.6 Model predictive control (family E)

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| CT-064 | MPC 1.3, NG20 III | Receding horizon: plan N steps, apply the first, re-plan | control | new | The core MPC loop |
| CT-065 | MPC 1.2.5, 2.5.4 | Input and state constraints (steering limits, speed limits, keep-out zones) | control | new | What MPC can handle and LQR cannot |
| CT-066 | MPC 1.3.1, 8.8, NG20 III.A | Linear MPC as a quadratic program (stack the predictions, condensed vs sparse) | control | partial | MA-068 has the QP and KKT. New: building the QP from A, B, Q, R |
| CT-067 | MPC 2.4.2, 2.6 | Terminal cost and terminal set; why a short horizon can fail | control | new | Use the LQR cost-to-go at the end of the horizon |
| CT-068 | MPC 2.5.1 | Unconstrained MPC equals LQR | control | new | The bridge between §1.5 and §1.6 |
| CT-069 | MPC 1.5.2, 5.5 | Disturbances and offset-free MPC | control | new | Estimate a constant disturbance so the error goes to zero. Optional |
| CT-070 | MPC 2.5.5, NG20 III.B, SU22 IV.A | Nonlinear MPC | control | new | Keep the full nonlinear model; solve a nonlinear program each step |
| CT-071 | NG20 III.C | Linear vs nonlinear MPC: accuracy against compute | control | new | Quadrotor evidence |
| CT-072 | MPC 8.5, WE22 V.A, PA16 IV.C | Direct methods: single shooting, multiple shooting, collocation | maths | partial | Note 77 (trajectory optimisation, shooting). New: multiple shooting and collocation |
| CT-073 | MPC 8.6, 8.7 | Newton-type solvers: SQP and interior point (overview only) | maths | partial | MA-064 mentions Newton's method. New: Newton with constraints, at "what the solver does" depth |
| CT-074 | MPC 8.9, 2.7 | Real-time MPC: warm starts, real-time iteration, stopping early | control | new | How MPC runs at 50–1000 Hz |
| CT-075 | PA16 V.C, Kong 2015 | MPC for path following on the bicycle model | control | new | Frenet errors as the state, steering and acceleration as inputs |
| CT-076 | Williams 2016 | Sampling-based MPC: model predictive path integral (MPPI) | control | partial | Note 106/107 name MPPI as a Nav2 controller. New: sample many control sequences, weight by cost, average. Link to the cross-entropy method (Note 153) |
| CT-077 | Di Carlo 2018, WE22 IV | Convex MPC for legged robots (single rigid body, ground reaction forces, QP) | control | new | How MIT Cheetah 3 picks foot forces |
| CT-078 | NG20 III, SU22 IV.A | MPC for quadrotors | control | new | Same NMPC with the quadrotor model; links to §1.8 |
| CT-079 | NG20 III.E, WE22 VII, SU22 VIII | MPC vs RL, and combining them | control | partial | Notes 134 and 146. New: a side-by-side view from the control side |

### 1.7 Legged models for control (family F)

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| CT-080 | WE22 IV, UR 4, UR 5 | Simplified models: linear inverted pendulum (LIP), single rigid body, centroidal dynamics | control | new | Why a 12-joint robot can be planned as one box or one pendulum |
| CT-081 | UR 5 | Zero-moment point (ZMP) and ZMP walking | control | new | The classic humanoid balance rule |
| CT-082 | WE22 III.B, Di Carlo 2018 | Contact schedule (gait timing) as a fixed input to MPC | control | new | MPC chooses forces; a timer chooses which feet are down |
| CT-083 | WE22 II.D, VI, UR 5 | Whole-body control: a QP that turns wanted forces and motions into joint torques | control | new | The fast layer under convex MPC |

### 1.8 Trajectory generation (family G)

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| CT-084 | MR 9.1 | Path vs trajectory; time scaling s(t) | control | new | Separate the shape from the timing |
| CT-085 | MR 9.2, RVC3 3.3.1 | Cubic and quintic polynomials from boundary conditions | maths | partial | ML-060 fits polynomials to data. New: solving for the coefficients from start and end position, speed and acceleration |
| CT-086 | MR 9.2, RVC3 3.3.1 | Trapezoidal velocity profile | control | new | Speed up, cruise, slow down |
| CT-087 | MR 9.3, RVC3 3.3.2, 3.3.3 | Via points and multi-segment trajectories; continuity at the joins | control | new | Smooth through many waypoints |
| CT-088 | MR 9.3, RVC3 3.3.3 | Cubic splines | maths | new | Piecewise cubics with matching slope and curvature |
| CT-089 | Flash & Hogan 1985 | Minimum-jerk trajectories | control | new | The smoothest motion: the quintic that minimises jerk |
| CT-090 | Mellinger & Kumar 2011, Richter 2016 | Minimum-snap trajectories as a QP | control | new | Piecewise polynomials for quadrotors; Richter gives the closed form |
| CT-091 | Richter 2016 | Time allocation between segments | control | new | How long each piece takes changes the result |
| CT-092 | MR 9.4 | Time-optimal time scaling under speed and acceleration limits | control | partial | Note 172 (optional, path-constrained timing, PA 14.8). New: the beginner case, a speed profile along a fixed path |
| CT-093 | RVC3 3.3.4 | Interpolating orientation (slerp) | maths | partial | Planned MA "3D rotations: Euler angles and quaternions". New: smooth blends between orientations |
| CT-094 | SU22 VI.C–D | Dynamically feasible vs infeasible references | control | new | A tracker cannot follow what the robot physically cannot do |
| CT-095 | robotics.md (PA 15.9) | Dubins and Reeds-Shepp curves | control | covered | Note 76 |
| CT-096 | robotics.md (PA 14.1–14.6) | Kinodynamic planning | control | covered | Note 76 |
| CT-097 | robotics.md (PA 14.9) | Trajectory optimisation (gradient-based, shooting) | control | covered | Note 77 |

### 1.9 Quadrotor dynamics and control (family H)

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| CT-098 | SU22 III.B, NG20 II, Mahony 2012 | Quadrotor model: four rotor thrusts give total thrust and three torques (the mixer) | control | new | How four propellers steer a drone |
| CT-099 | SU22 III.B, RVC3 4.2 | Quadrotor rigid-body dynamics in 3D | control | new | Needs the planned MA rotation and rigid-body Notes |
| CT-100 | RVC3 4.2, Mahony 2012 | Underactuation: tilt to move sideways | robotics | new | Four inputs, six degrees of freedom |
| CT-101 | SU22 II.A, RVC3 4.2 | Cascaded quadrotor control: attitude loop inside position loop | control | new | Uses §1.3 cascades |
| CT-102 | UR 3 | Linearise at hover; LQR or PID at hover | control | new | The beginner drone controller |
| CT-103 | Mellinger & Kumar 2011, SU22 IV.B | Differential flatness: full state and inputs from position, yaw and their derivatives | control | new | Why polynomials in x, y, z, yaw are enough to plan a drone flight |
| CT-104 | Lee 2010, SU22 IV.B | Geometric tracking controller | control | new | Large-angle attitude control without Euler-angle trouble. Optional, as a named tool |
| CT-105 | robotics.md (RL R0.7) | Basic PD/PID on a single axis | control | covered | Note 56 |
| CT-106 | robotics.md (RL N.24) | RL for agile flight | control | covered | Note 134 |

### 1.10 Other covered or recap rows

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| CT-107 | MPC 1.3.1, NG20 III.A | QP, KKT conditions | maths | covered | MA-066, MA-068 |
| CT-108 | FBS 6.4 | Jacobian | maths | covered | MA-063 |
| CT-109 | robotics.md (PA 15.6) | HJB equation | maths | covered | Note 174 |
| CT-110 | robotics.md (PR 3.1) | Kalman filter for the state that feedback needs | robotics | covered | Note 63 |
| CT-111 | robotics.md (RL R0.5) | PD joint targets under an RL policy | robotics | covered | Note 80 |
| CT-112 | MR 13.5 | Mobile manipulation | robotics | new | Out of this area; listed so the manipulation gap file can claim it |

---

## 2. Prerequisites between the new concepts

Arrows mean "needed before". "MA:" marks planned or new maths.

- MA: state-space models → matrix exponential → discrete-time models → linearising around a trajectory
- MA: stability (eigenvalues, Lyapunov) → state feedback and pole placement → integral action, windup
- Discrete-time models → controllability rank test → LQR (Riccati recursion) → infinite-horizon LQR → LQR tracking → time-varying LQR
- Unicycle model → move to a point → follow a line → move to a pose
- Kinematic bicycle model → path (Frenet) coordinates → cross-track and heading error → pure pursuit → Stanley → rear-wheel feedback
- Unicycle model + Lyapunov → Kanayama tracker
- Feedback linearisation needs state feedback and the unicycle model
- Dynamic bicycle model needs slip angle and cornering stiffness; it feeds road-error dynamics → LQR steering → LQR with feedforward, preview
- LQR + MA-068 QP + constraints → receding horizon → linear MPC as a QP → terminal cost → nonlinear MPC → shooting and collocation → SQP overview → real-time MPC
- Linear MPC + path coordinates → MPC path following
- Sampling MPC (MPPI) needs the receding horizon and Monte Carlo estimation (planned MA)
- Friction cone + single rigid body model + linear MPC → convex MPC → whole-body control; LIP → ZMP
- Polynomials from boundary conditions → trapezoid profile → via points → cubic splines → minimum jerk → minimum snap QP → time allocation
- MA 3D rotations + rigid-body dynamics → quadrotor model → hover LQR → cascaded attitude and position control → differential flatness (+ minimum snap) → geometric controller → quadrotor NMPC

---

## 3. Suggested learning order

Each block needs the blocks above it. The RO Note numbers say where each block plugs into robotics.md.

**Block 1: Feedback basics (just after Note 56 PID).** Step response words → feedforward plus feedback → cascaded loops → windup.

**Block 2: Wheeled models in depth (extends Note 50).** Unicycle → kinematic bicycle and Ackermann → curvature and limits → path coordinates → omnidirectional base → kinematic vs dynamic.

**Block 3: Driving to a goal and tracking a path (after Note 77, before Note 106).** Move to a point, a line, a pose → path following vs trajectory tracking → cross-track error → pure pursuit → Stanley → Kanayama → feedforward on curves → comparing trackers and metrics. **This block is the most urgent: navigation (RO-15) needs a path follower.**

**Block 4: Trajectory generation (beside Block 3).** Time scaling → polynomials → trapezoid → via points and splines → minimum jerk.

**Block 5: State feedback and LQR (core; pull LQR out of optional Note 174).** Matrix exponential and discretising → linearising around a trajectory → controllability → pole placement → discrete LQR → LQR tracking → time-varying LQR → feedback linearisation.

**Block 6: MPC (after Block 5).** Receding horizon → constraints → linear MPC as QP → unconstrained MPC = LQR → terminal cost → nonlinear MPC → shooting and collocation → solvers in outline → real-time MPC → MPC path following → MPPI → MPC vs RL.

**Block 7: Car dynamics (optional for navigation, needed for fast cars).** Dynamic bicycle → slip angle and cornering stiffness → tyre saturation → longitudinal slip and resistance → road-error dynamics → LQR steering → understeer → cruise control → preview and gain scheduling.

**Block 8: Legged control (before RO-20 Note 146, "Tracking model-based reference motions").** Friction cone → LIP and ZMP → single rigid body → contact schedule → convex MPC → whole-body control.

**Block 9: Quadrotors (before Note 134, agile aerial navigation).** Model and mixer → underactuation → hover LQR → cascaded control → differential flatness → minimum snap and time allocation → geometric controller → quadrotor NMPC.

---

## 4. New maths the area needs that MA lacks

Not yet in MA, nor in the planned new MA Notes of robotics.md §3:

| Concept | What | Suggested home | First needed by |
|---|---|---|---|
| Matrix exponential | e^(At) solves ẋ = Ax; series definition; eigenvalues set growth or decay | MA 06-calculus, with the planned "State-space models" Note | Discrete-time models |
| Discretising a continuous model | zero-order hold: A_d = e^(AΔt), and the matching B_d; compare with an Euler step | Short section in the "State-space models" Note | Linear MPC, discrete LQR |
| Controllability rank test | rank of [B, AB, …, A^(n−1)B]; the linear case only | MA 05-linear-algebra or short section in the LQR Note | LQR |
| Pole placement (eigenvalues of A − BK) | choose K to move the eigenvalues | Short section in the state-feedback Note | State feedback |
| Discrete Riccati recursion | the backward update of the cost matrix P | Short section in the LQR Note (it is DP, Note 18, on quadratic costs) | LQR |
| Polynomials from boundary conditions | solve a small linear system for the coefficients | Short section in the trajectory Note (uses MA-054 matrix inverse) | Cubic and quintic trajectories |
| Cubic splines | piecewise cubics with matching slope and curvature; a banded linear system | MA 06-calculus (new Note) or short RO section | Via-point trajectories, minimum snap |
| Calculus of variations, beginner form | minimise an integral of squared jerk or snap; result is a polynomial | Short section in the minimum-jerk Note (robotics.md dropped PA 13.9 as full theory; keep it dropped) | Minimum jerk and snap |
| Second-order cone and its linear pyramid approximation | the friction cone as linear inequalities so the problem stays a QP | Short section in the convex MPC Note (uses MA-067 convex sets) | Convex MPC |
| Newton's method with constraints (SQP, interior point), overview | what the solver does each iteration | MA 07-optimisation (extend MA-064 / MA-068) or short RO section | Nonlinear MPC |

Already planned in robotics.md §3 and used here: state-space models, stability and Lyapunov functions, ODEs and numerical integration, rigid-body transforms, 3D rotations and quaternions, Newtonian and rigid-body mechanics, Monte Carlo estimation (for MPPI).

---

## 5. Left out (beyond beginner depth or another area)

| Item | Source | Why |
|---|---|---|
| Chained form and time-varying feedback for cars | SN09 3.2.1–3.2.2 | Nonholonomic control theory; robotics.md already dropped its parent (PA 15.10–15.12) |
| Robust, tube and stochastic MPC | MPC ch.3 | Research depth |
| Economic, distributed and explicit MPC | MPC 2.8, ch.6, ch.7 | Research depth; not used by navigation or legged Notes |
| Fault-tolerant MPC, load transport, physical interaction | NG20 III.D, F, G | Specialist drone topics |
| Incremental nonlinear dynamic inversion (INDI) | SU22 IV.C | Specialist; one mention in the quadrotor Note is enough |
| Partial feedback linearisation, swing-up | UR 3 | Underactuated-systems depth |
| Model-free control (MFC, SAMFC) | AR24 4.2, 4.3 | Niche lateral-control methods |
| Manipulator control: computed torque, force, impedance | MR 11.4–11.8, RVC3 9.4–9.6 | Manipulation area |
| Moving-horizon estimation | MPC ch.4 | Estimation area |
