# Completeness audit: what the RO scope still misses

> **Plan of record:** [robotics.md](robotics.md). This doc is evidence: its rows (IDs `AU-NNN`), sources and checks. "Note N" or "RO N" below means the earlier 188-Note draft (2026-10-07), not today's plan.


> **Plan of record:** [robotics.md](../../../../../campusx/docs/books-scope/robotics.md) (`docs/books-scope/robotics.md`, 25 chapters, 188 Notes). This audit lists only what is still missing **after** the three gap areas being scoped now. Those three are not re-scoped here:
> - **G-C**: mobile-robot control: path tracking, MPC, vehicle models, trajectory generation, quadrotors.
> - **G-P**: perception: cameras, features, optical flow, VO, SfM, LiDAR/ICP, IMU fusion, factor graphs.
> - **G-A**: arms and legged mechanics: kinematics, Jacobians, IK, dynamics, force/impedance, whole-body control, ZMP, capture point.

## 0. Summary

**Method.** I read five survey sources first, to see how the field splits itself up (§1). Then I checked 12 curricula: 8 university courses and 4 industry or nanodegree stacks (§2). I listed each one's topics from its official page and marked each topic in one of four ways: in robotics.md (RO Note number), in a gap area (G-C, G-P, G-A), already in MA/ML/DL, or **MISSING**. The missing topics are the rows in §3.

**How sources were checked.**
- arXiv papers: the arXiv abstract page (title and date).
- DOIs: Crossref (title and year).
- Course pages: fetched live.
- Nav2 and Autoware docs: these pages load through JavaScript redirects, so I read the source Markdown in their official GitHub doc repositories.
- No cookies, no members-only content.
- The MIT Press page for Siegwart (403) and the ISO 26262 page (403) blocked the fetch, so they are cited through other pages (see the rows).

**Counts (§3 table, 53 rows):**

| Status | Rows |
|---|---|
| new | 30 |
| partial (a related RO Note exists; the new part is named) | 23 |
| covered | 0 (covered topics appear only in the coverage table, §7) |

| Kind | Rows |
|---|---|
| robotics | 38 |
| vision | 5 |
| RL | 5 |
| software | 4 |
| control | 1 |
| maths | 0 (the 7 new maths items are listed in §6) |

**Largest holes**, by how many curricula teach them and the RO scope lacks:
1. **System architecture and software.** ROS 2, the TF frame tree, behaviour trees and state machines, layered costmaps, and the mission→behaviour→motion→control layering. Taught by 9 of the 12 sources.
2. **Planning for cars.** Behaviour planning, Hybrid A*, state lattices, route graphs, speed planning, path smoothing.
3. **Other agents.** Object detection, multi-object tracking and motion prediction. Taught by 6 sources, and every survey makes them a top-level block.
4. **GNSS and map-based localization.** GNSS, NDT, HD/vector maps.
5. **Robot learning beyond the RO list.** Diffusion policy, ACT, inverse RL/GAIL, statistically sound RL evaluation, curiosity-driven exploration, multi-agent RL.

## 1. Surveys read first: how the field divides itself

| # | Survey | Checked at | Top-level taxonomy (the column used in §7) |
|---|---|---|---|
| S1 | Siegwart, Nourbakhsh, Scaramuzza, *Introduction to Autonomous Mobile Robots*, 2nd ed., MIT Press 2011 (ISBN 9780262015356) | ETH AMR course page and 2021 programme PDF, which follow the book chapter by chapter ("to 4.3", "to 5.2", "to 6.2"): [AMR_Program_2021 V3.pdf](https://ethz.ch/content/dam/ethz/special-interest/mavt/robotics-n-intelligent-systems/asl-dam/documents/lectures/autonomous_mobile_robots/spring-2021/AMR_Program_2021%20V3.pdf); publisher listing [schweitzer-online](https://www.schweitzer-online.de/buch/Siegwart/Introduction-Autonomous-Mobile-Robots/9780262015356/A1374371/) (the MIT Press page returned 403) | **See–think–act**: locomotion and kinematics (act) · perception (see) · localization and map building · planning and navigation (think) |
| S2 | Paden et al. 2016, *A Survey of Motion Planning and Control Techniques for Self-driving Urban Vehicles* | [arXiv 1604.07446](https://arxiv.org/abs/1604.07446); the layer names were checked in the PDF's §II | **Decision hierarchy**: route planning → behavioural layer → motion planning → local feedback control |
| S3 | Badue et al. 2021, *Self-Driving Cars: A Survey* | [arXiv 1901.04407](https://arxiv.org/abs/1901.04407) | **Perception**: localization, static-obstacle mapping, moving-obstacle detection and tracking, road mapping, traffic-signal recognition. **Decision making**: route planning, path planning, behaviour selection, motion planning, control |
| S4 | Yurtsever et al. 2020, *A Survey of Autonomous Driving: Common Practices and Emerging Technologies* | [arXiv 1906.05113](https://arxiv.org/abs/1906.05113) | System architectures (modular vs end-to-end, ego-only vs connected) · localization · mapping · perception · assessment (risk) · planning · human-machine interface · datasets and tools |
| S5 | González et al. 2016, *A Review of Motion Planning Techniques for Automated Vehicles*, IEEE T-ITS | Crossref [10.1109/TITS.2015.2498841](https://doi.org/10.1109/TITS.2015.2498841) | Planner families: graph search, sampling, interpolating curves, numerical optimisation |
| (+) | Chen et al. 2023, *End-to-end Autonomous Driving: Challenges and Frontiers* | [arXiv 2306.16927](https://arxiv.org/abs/2306.16927) | Modular pipeline vs end-to-end; imitation vs RL; closed-loop vs open-loop evaluation |
| (+) | Rudenko et al. 2020, *Human Motion Trajectory Prediction: A Survey* | [arXiv 1905.06113](https://arxiv.org/abs/1905.06113) | Prediction methods: physics-based, pattern-based, planning-based |

**What the surveys show.** Every driving survey (S2, S3, S4) has three top-level blocks that the RO scope lacks:
- the **system architecture** itself;
- **moving-obstacle detection, tracking and prediction**;
- a **behaviour layer** between route and motion planning.

S1 (Siegwart) has no top-level block outside RO plus the three gap areas.

Surveys of RL for robots are left to the other agent.

## 2. The curricula and their topics

| Code | Curriculum | Official page (verified) |
|---|---|---|
| TOR | U. Toronto *Self-Driving Cars* Specialization (Coursera, 4 courses) | [specialization](https://www.coursera.org/specializations/self-driving-cars); module lists: [C1](https://www.coursera.org/learn/intro-self-driving-cars), [C2](https://www.coursera.org/learn/state-estimation-localization-self-driving-cars), [C4](https://www.coursera.org/learn/motion-planning-self-driving-cars); C3 topics from the specialization page |
| ETH | ETH Zurich *Autonomous Mobile Robots* 151-0854-00L (2021) | [course page](https://asl.ethz.ch/education/lectures/autonomous_mobile_robots/spring-2021.html), [programme PDF](https://ethz.ch/content/dam/ethz/special-interest/mavt/robotics-n-intelligent-systems/asl-dam/documents/lectures/autonomous_mobile_robots/spring-2021/AMR_Program_2021%20V3.pdf) |
| CMU | CMU 16-761 *Mobile Robots* (Kelly) | [course page](https://www.cs.cmu.edu/~alonzo/teaching/16-761/16-761.html) |
| FRE | Freiburg *Introduction to Mobile Robotics* SS24 | [course page](https://rl.uni-freiburg.de/teaching/ss24/mobile-robotics) |
| M42 | MIT 6.4210 *Robotic Manipulation* (Tedrake) | [online text, contents](https://manipulation.mit.edu/) |
| M832 | MIT 6.832 *Underactuated Robotics* (Tedrake) | [online text, contents](https://underactuated.mit.edu/) |
| S237B | Stanford AA274B/CS237B *Principles of Robot Autonomy II* | [course page](https://web.stanford.edu/class/cs237b/) |
| COR | Cornell CS 4756/5756 *Robot Learning* (2026) | [course page](https://www.cs.cornell.edu/courses/cs4756/) |
| UDS | Udacity *Self-Driving Car Engineer* nd0013 | [syllabus](https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd0013) |
| UDR | Udacity *Robotics Software Engineer* nd209 | [syllabus](https://www.udacity.com/course/robotics-software-engineer--nd209) |
| NAV2 | Nav2 docs (concepts + plugin list) | source repo [ros-navigation/docs.nav2.org](https://github.com/ros-navigation/docs.nav2.org) (`docs/getting_started/navigation_concepts/`, `docs/configuration_and_development/navigation_plugins.md`); site [docs.nav2.org](https://docs.nav2.org/) |
| AW | Autoware architecture v1 | source repo [autoware-documentation](https://github.com/autowarefoundation/autoware-documentation) (`docs/design/autoware-architecture-v1/`); site [docs.autoware.org](https://docs.autoware.org/) |

Other candidates I checked and did not use:
- Stanford AA274A: no public schedule page; only catalogue text.
- UPenn MicroMasters: the edX page returned 404, and the 2017 news gives course names only.
- CMU 16-831: no official page found.

### 2.1 Topics per curriculum, marked

Status codes:
- **RO n**: the RO Note number in robotics.md.
- **G-C**, **G-P**, **G-A**: one of the three gap areas.
- **MISSING**: see the §3 row named after the arrow.
- **MA/DL new**: a maths or deep-learning Note already planned.

**TOR, U. Toronto.**
- **C1, Introduction to Self-Driving Cars**
  - Taxonomy of driving (SAE levels, ODD): MISSING → row A1
  - Requirements for perception: MISSING → A1, D1–D4
  - Driving decisions and actions: MISSING → F1
  - Sensors and computing hardware, and hardware configuration design: G-P (sensors), MISSING (choosing and placing sensors) → A8
  - Software architecture: MISSING → A2
  - Environment representation: RO 68, plus MISSING HD maps → B3
  - Safety assurance, industry testing, safety frameworks: MISSING → A9
  - Kinematic and dynamic bicycle models, tyres, actuation: G-C
  - PID, longitudinal speed control, feedforward: RO 56, G-C
  - Lateral control (pure pursuit, Stanley, MPC): G-C
  - CARLA project: MISSING → J3
- **C2, State Estimation and Localization**
  - Least squares: ML-053; recursive least squares is new maths (§6)
  - KF / EKF / UKF: RO 63, 64, 158
  - Error-state EKF: G-P (IMU fusion)
  - GNSS/INS: MISSING (GNSS) → C1; G-P (INS)
  - LiDAR and ICP: G-P
  - Full vehicle state estimator: G-P
- **C3, Visual Perception**
  - Pinhole camera, calibration, features, VO: G-P
  - CNNs: DL-040
  - 2D object detection: MISSING → D1
  - Object tracking: MISSING → D3
  - Semantic segmentation of the drivable surface: MISSING → D2
- **C4, Motion Planning**
  - The planning problem as a hierarchy: MISSING → A2
  - Occupancy grids: RO 68
  - Mission planning with Dijkstra and A*: RO 14, 15, plus road-graph routing MISSING → B4
  - Dynamic object interactions (prediction, time to collision): MISSING → E1, E2
  - Behaviour planning with state machines: MISSING → A5, F1
  - Reactive planning (trajectory rollout, DWA): RO 106
  - Smooth local planning (parametric curves, velocity profiles): G-C, plus speed planning MISSING → F5

**ETH AMR.**
- Introduction: none needed.
- Locomotion and legged intro: G-A.
- Rigid-body kinematics: MA new (rigid-body transforms).
- Wheeled kinematics: RO 50.
- Sensors:
  - IMU: G-P
  - GPS: MISSING → C1
  - Motion capture: MISSING → H3
  - Laser: RO 57
  - RGB-D / ToF / sonar: G-P
- Image formation, calibration, stereo, SfM: G-P.
- Filtering, edges, points: G-P.
- Place recognition: G-P / RO 167.
- Error propagation law: MA new (linear transforms of a Gaussian).
- Line extraction: G-P.
- Markov and Kalman localization: RO 66, 160.
- SLAM (EKF, monocular): RO 69, 163, G-P.
- Planning:
  - C-space, graph search: RO 54, 13–15
  - Collision avoidance: RO 106
  - Sampling: RO 74, 75
  - Motion constraints: RO 76
- Dynamic window (exercise): RO 106.

**CMU 16-761.**
- Orthogonal transforms: MA new.
- Kinematics of mechanisms: G-A / RO 52.
- Kinematic models of sensors and actuators: RO 51, 57.
- Transform graphs and pose networks: MISSING → A4.
- Uncertainty, combining measurements, KF, Bayes, PF: RO 61–65.
- Ground-vehicle dynamics, linear systems: G-C, MA new (state-space models).
- Measurement physics, inertial navigation: G-P.
- Satellite navigation: MISSING → C1.
- Hierarchical control: MISSING → A2.
- WMR kinematics: RO 50.
- Trajectory generation: G-C.
- Obstacle avoidance: RO 106.
- Path following: G-C.
- Radiative sensors: RO 57, G-P.
- Visual tracking: G-P.
- Map representation: RO 53, 68.
- Localization: RO 66, 67.
- Motion planning: RO 74, 75.
- Real-time planning: RO 71.
- Nonholonomic planning: RO 76, plus Hybrid A* and lattices MISSING → F2, F3.

**FRE, Freiburg.**
- Probability: MA.
- Sensor and motion models: RO 51, 57.
- Particle filter and Kalman filter: RO 63, 65.
- Grid mapping: RO 68.
- SLAM, FastSLAM, graph SLAM: RO 69, 165, 166.
- 3D mapping: MISSING → B2.
- Motion and path planning: RO 13–15, 70, 74.
- Control systems: RO 56, G-C.

**M42, MIT 6.4210.**
- Ch2 robot description files: MISSING → J1.
- Ch2 arms and hands: G-A. Sensors: G-P.
- Ch3 spatial algebra: MA new.
- Ch3 FK, Jacobians, differential IK: G-A.
- Ch3 grasp poses: G-A.
- Ch4 cameras and depth sensors, ICP, outliers: G-P.
- Ch4 tracking: G-P.
- Ch5 static equilibrium with friction, contact simulation: G-A, plus MISSING how a simulator computes contact → J2.
- Ch5 model-based grasp selection, and grasps from point clouds: MISSING → K4.
- Ch5 task-level programming: MISSING → K3.
- Ch6 IK: G-A.
- Ch6 kinematic trajectory optimisation: RO 77.
- Ch6 sampling-based planning: RO 74, 75.
- Ch6 graphs of convex sets: research depth, left out.
- Ch6 time-optimal path parameterisation: G-C.
- Ch7 mobile manipulation: navigation RO 107.
- Ch8 force and stiffness control: G-A.
- Ch9 object detection and segmentation: MISSING → D1, D2.
- Ch9 self-supervised learning: DL-067 §7.
- Ch10 deep pose estimation, keypoints, dense correspondence: MISSING → D5.
- Ch11 RL: RO 36–48, 135.
- Ch12 soft robots and tactile sensing: MISSING (optional) → K5.

**M832, MIT 6.832.**
- Ch1–3 model systems (pendulum, acrobot, cart-pole, quadrotor): G-C.
- Ch4–5 walking and running, articulated legged robots: G-A.
- Ch6 stochastic models: RO 8.
- Ch7 DP: RO 18.
- Ch8 LQR: RO 174.
- Ch9 Lyapunov: MA new (stability).
- Ch10 trajectory optimisation: RO 77.
- Ch11 policy search: RO 36.
- Ch12 sampling-based planning: RO 74.
- Ch13 robust and stochastic control: research depth, left out.
- Ch14 feedback motion planning (funnels): dropped in PA 8.6 (kept dropped).
- Ch15 output feedback (pixels to torques): RO 152.
- Ch16 limit cycles: G-A.
- Ch17 planning through contact: G-A.
- Ch18 system identification: RO 83.
- Ch19 state estimation: RO 61–65.
- Ch20 model-free policy search: RO 36.
- Ch21 imitation learning: RO 100, plus MISSING → I1–I3.
- App. A Drake: MISSING → J2.

**S237B, Stanford.**
- ML for robotics: ML/DL.
- MDP and RL: RO 8–48.
- Model-based RL: RO 135, 142.
- Learning-based perception: MISSING → D1, D2.
- Grasping and manipulation: RO 151–156, G-A, MISSING → K4.
- Interactive perception: research depth, left out.
- Imitation learning I–II: RO 100, MISSING → I1–I3.
- Learning from human feedback: RO 183 (optional chapter), MISSING robot-side → I5.
- Interaction-aware planning: MISSING → E3.
- Shared autonomy: MISSING → I5.

**COR, Cornell.**
- Fundamentals of robotic control: RO 56.
- MDP: RO 8.
- Imitation learning: RO 100, MISSING → I1–I3.
- Value functions, Q-learning, policy gradient, actor-critic, deep RL: RO 16–48.
- MPC: G-C.
- Dynamics learning: RO 135, 142.
- Reward shaping and learning: RO 89, MISSING → I3.
- Simulation: RO 81, MISSING → J2.
- Camera models: G-P.
- 2D and 3D visual representations: MISSING → D2, D5.
- State estimation: RO 61–65.
- Visuomotor policies: RO 152.
- Transfer: RO 82.
- Multi-task: RO 178.
- Generative models: DL new.
- Sequence models: DL-064, DL-087.
- Hierarchical decision making: RO 119.
- Open-world robotics: RO 178.

**UDS, Udacity Self-Driving Car Engineer.**
- ML workflow: ML.
- Sensor and camera calibration: G-P (intrinsics), MISSING (extrinsics) → H1.
- CNN classification: DL-040.
- 2D object detection: MISSING → D1.
- LiDAR and 3D object detection: MISSING → D4.
- KF, EKF: RO 63, 64.
- Multi-target tracking: MISSING → D3.
- Markov localization: RO 66.
- Scan-matching localization: RO 58, G-P (ICP), MISSING (NDT) → C2.
- Behaviour planning: MISSING → F1.
- Trajectory generation: G-C.
- Motion planning: MISSING → F2.
- PID: RO 56.
- Trajectory tracking: G-C.
- UKF: RO 158.
- Prediction: MISSING → E1.
- Vehicle models and MPC: G-C.
- PCL: MISSING → D4.
- FCN and scene understanding: MISSING → D2.
- Functional safety: MISSING → A9.

**UDR, Udacity Robotics Software Engineer.**
- Gazebo world: MISSING → J1, J2.
- ROS essentials (packages, nodes): MISSING → A3.
- KF, MCL: RO 63, 67.
- Occupancy grid, grid FastSLAM, GraphSLAM: RO 68, 166, 165.
- Classic and sampling-based path planning: RO 13–15, 74, 75.
- Home service robot: RO 107.

**NAV2.**
- Concepts:
  - ROS 2: MISSING → A3
  - Behaviour trees: MISSING → A5
  - Navigation servers: RO 107 (partial) → A2
  - State estimation (REP-105 frames, robot_localization): MISSING → A4; RO 64
  - Environmental representation (costmaps and layers): MISSING → B1
- Navigators (to-pose, through-poses, coverage): RO 107, 173.
- Costmap layers (static, obstacle, inflation, voxel, range, semantic segmentation) and filters (keepout, speed): MISSING → B1.
- Controllers:
  - DWB, TEB: RO 106
  - Regulated pure pursuit, MPPI, graceful, vector pursuit, rotation shim: G-C
- Planners:
  - NavFn: RO 70
  - Smac 2D: RO 15
  - Smac Hybrid-A*: MISSING → F2
  - Smac Lattice: MISSING → F3
  - Theta*: RO 15 (a variant; too small for its own Note)
- Smoothers: MISSING → F6.
- Behaviours and recovery (spin, back up, wait, clear costmap, assisted teleop): MISSING → A6.
- Goal and progress checkers: MISSING → A6.
- Waypoint follower: MISSING → A6.
- Route server: MISSING → B4.
- GPS tutorial: MISSING → C1.
- Collision monitor: RO 127 (partial).
- Docking: left out (product feature).

**AW, Autoware.**
- Sensing data types (point cloud, image, GNSS/INS, radar, ultrasonic): G-P, MISSING (GNSS, radar) → C1, D4.
- Map (point-cloud map, vector map of lanes, crosswalks, stop lines, traffic lights): MISSING → B3.
- Localization:
  - LiDAR + point-cloud map: MISSING → C2
  - Camera or LiDAR + vector map: MISSING → B3
  - GNSS / RTK: MISSING → C1
  - VO / VSLAM: G-P
- Perception:
  - Object recognition (detection, tracking, prediction): MISSING → D1, D3, D4, E1
  - Obstacle segmentation: MISSING → D4
  - Occupancy grid (blind spots): RO 68
  - Traffic lights: MISSING → D1
- Planning:
  - Mission planning: MISSING → B4
  - Behaviour path and behaviour velocity planners: MISSING → F1, F5
  - Obstacle stop and adaptive cruise: MISSING → F5
  - Validation: MISSING → A7
- Control: G-C.
- Vehicle interface: G-C.
- System (fail-safe, diagnostics, operation modes): MISSING → A7.

## 3. Still missing: rows in the brief's format

Status key: **new** = not in robotics.md, not in MA/ML/DL and not in the three gap areas. **partial** = an RO Note touches it; the new part is named.

Kind key: robotics / vision / control / RL / software. "Software" is used for tools a learner must operate: ROS 2, description formats, simulators.

### A. System architecture and robot software

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| AU-001 | TOR C1 M1; SAE J3016 ([sae.org](https://www.sae.org/standards/content/j3016_202104/)); S3 | A1 Levels of driving automation and the operating domain (ODD) | robotics | new | What "level 2" and "level 4" mean; the ODD as the set of conditions a system is built for. Short section in A2 |
| AU-002 | TOR C1 M2 L3, C4 M2; CMU wk 10 "hierarchical control"; S1 ch.1; S2 §II; S3; AW architecture | A2 The autonomy stack: sense–plan–act and the layers mission → behaviour → motion → control | robotics | partial | RO 107 names the Nav2 servers. New: one picture of the whole loop, which layer runs how fast, and how Nav2 and Autoware map onto it. The anchor Note for this whole chapter |
| AU-003 | S4 §III; Chen et al. 2023 [arXiv 2306.16927](https://arxiv.org/abs/2306.16927) | A2b Modular vs end-to-end stacks for driving | robotics | partial | RO 121 compares modular and end-to-end for indoor navigation. New: the same trade-off for driving stacks, and where learned parts plug into a modular stack |
| AU-004 | NAV2 concepts "ROS 2"; UDR C3; Macenski et al. 2022, *Robot Operating System 2*, Sci. Robotics ([10.1126/scirobotics.abm6074](https://doi.org/10.1126/scirobotics.abm6074)); [ROS 2 concepts](https://docs.ros.org/en/jazzy/Concepts.html) | A3 ROS 2: nodes, topics, services, actions, parameters, launch, QoS, lifecycle nodes, bags, RViz | software | partial | RO 107 says "ROS tooling" with no concepts behind it. New: the publish/subscribe model and the action pattern every Nav2 server uses |
| AU-005 | CMU wk 3 "Transform graphs & pose networks"; M42 ch.3 "Monogram notation"; NAV2 concepts "State estimation"; [REP-105](https://www.ros.org/reps/rep-0105.html) | A4 Coordinate frames and the transform tree (map → odom → base_link → sensor) | robotics | new | Why odometry drifts smoothly while localization jumps, so there are two frames; looking up any pose through the tree. Builds on the new MA rigid-transforms Note |
| AU-006 | NAV2 concepts "Behavior Trees"; Colledanchise & Ögren, *Behavior Trees in Robotics and AI* ([arXiv 1709.00084](https://arxiv.org/abs/1709.00084)) | A5 Behaviour trees (sequence, fallback, decorator, tick) and finite state machines | robotics | new | How a robot picks what to do next; Nav2's navigate-to-pose tree; state machines as the older tool (TOR C4 M6). Also a natural action space for RL over skills |
| AU-007 | NAV2 plugins: Behaviors, Goal Checkers, Progress Checkers, Waypoint Task Executors | A6 Recovery behaviours, goal and progress checks, waypoint following | robotics | new | What happens when the robot is stuck: spin, back up, clear the costmap, retry. Section inside A5 |
| AU-008 | AW AD-API fail-safe / diagnostics / operation modes; AW planning "Validation" | A7 System monitoring, fail-safe and the minimal-risk manoeuvre | robotics | partial | RO 127 has safety filters for one policy. New: the system level: diagnostics, a trajectory validator, and a safe stop when a module fails |
| AU-009 | TOR C1 M2 L1–L2; ETH wk 4 | A8 Choosing and placing sensors: coverage, range, redundancy, compute budget | robotics | new | Section inside A2. Sensor physics stays in G-P |
| AU-010 | TOR C1 M3 (safety assurance, frameworks, testing); UDS C13 (functional safety, hazard analysis and risk assessment) | A9 Safety assurance: hazard analysis, functional safety (ISO 26262), scenario testing | robotics | new | Optional. How a team argues a robot is safe enough; differs from constrained RL (RO-17). ISO page blocked the fetch; cited through the TOR and UDS syllabi |

### B. Maps for planning

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| AU-011 | NAV2 concepts "Environmental representation", costmap layers and filters; Lu, Hershberger, Smart 2014, *Layered costmaps* ([10.1109/IROS.2014.6942636](https://doi.org/10.1109/IROS.2014.6942636)) | B1 Layered costmaps: static, obstacle and inflation layers, footprint, keep-out and speed zones | robotics | partial | RO 68 builds occupancy. New: turning occupancy into cost a planner uses, and inflating by the robot's size. Every Nav2 planner and controller reads it |
| AU-012 | FRE L10 "Techniques for 3D mapping"; NAV2 voxel layer; Hornung et al. 2013, *OctoMap* ([10.1007/s10514-012-9321-0](https://doi.org/10.1007/s10514-012-9321-0)) | B2 3D maps: voxel grids, octrees, elevation maps | robotics | partial | RO 86 uses height scans. New: how the 3D map is stored and updated (needed by drones and legged navigation) |
| AU-013 | AW map design (vector map: lanes, crosswalks, stop lines, traffic lights); S3 "road mapping"; Poggenhans et al. 2018, *Lanelet2* ([10.1109/ITSC.2018.8569929](https://doi.org/10.1109/ITSC.2018.8569929)) | B3 HD / vector maps: lanes as a graph with rules attached; point-cloud maps | robotics | new | What an HD map stores, and why a car localises and plans against it |
| AU-014 | TOR C4 M4; S2 §II-A; S3 "route planning"; NAV2 Route Server; AW mission planner | B4 Route (mission) planning on a road or route graph | robotics | partial | RO 14–15 teach Dijkstra and A*. New: the graph is a road network or a hand-made route graph, not a grid |

### C. Localization with GNSS and maps

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| AU-015 | TOR C2 M3; CMU wk 7–8 "satellite navigation"; ETH wk 4 GPS; AW localization (GNSS, RTK); NAV2 GPS tutorial | C1 GNSS: how a position is fixed from satellites, error sources, RTK, latitude/longitude to a local metric frame (ENU/UTM) | robotics | new | Fusing GNSS with an IMU belongs to G-P (IMU fusion, error-state EKF). This row is the GNSS sensor itself and its frames |
| AU-016 | AW localization "3D-LiDAR + point cloud map"; UDS C4 scan-matching localization; Biber & Straßer 2003, *The normal distributions transform* ([10.1109/IROS.2003.1249285](https://doi.org/10.1109/IROS.2003.1249285)) | C2 Localising against a prebuilt 3D map; the normal distributions transform (NDT) | robotics | partial | G-P owns ICP. New: NDT (the standard in Autoware) and the "localise in a prior map" setting. Confirm G-P does not already take NDT |

### D. Seeing other agents (outside the G-P list)

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| AU-017 | TOR C3; UDS C2; M42 ch.9; S237B wk 4; AW object recognition / traffic lights; Redmon et al. 2016 YOLO ([arXiv 1506.02640](https://arxiv.org/abs/1506.02640)) | D1 2D object detection: boxes, scores, non-max suppression, mAP | vision | new | No DL Note teaches detection (DL-040 to DL-054 cover classification and transfer). New DL Note |
| AU-018 | TOR C3 (drivable surface); UDS C12; M42 ch.9; NAV2 semantic-segmentation layer; Long et al. 2015 FCN ([arXiv 1411.4038](https://arxiv.org/abs/1411.4038)) | D2 Semantic segmentation | vision | new | Per-pixel classes; drivable-area masks feeding a costmap. New DL Note |
| AU-019 | UDS C3 multi-target tracking; TOR C3; S3 "moving obstacles tracking"; AW; Bewley et al. 2016 SORT ([arXiv 1602.00763](https://arxiv.org/abs/1602.00763)); Weng et al. 2020 AB3DMOT ([arXiv 1907.03961](https://arxiv.org/abs/1907.03961)) | D3 Multi-object tracking: one Kalman filter per object, association, track birth and death | robotics | partial | RO 161 (optional chapter) has data association. New: the full track-management loop. Every driving stack depends on it, so it should not sit only in optional RO-22 |
| AU-020 | UDS C3, C11 (PCL); AW obstacle segmentation, radar; NAV2 ground-consistency layer; Lang et al. 2019 PointPillars ([arXiv 1812.05784](https://arxiv.org/abs/1812.05784)) | D4 Point-cloud obstacles: ground removal, clustering, 3D boxes from LiDAR | vision | new | G-P teaches LiDAR geometry and ICP. New: finding objects in the cloud. Confirm with G-P |
| AU-021 | M42 ch.10 (pose estimation, keypoints, dense correspondence); COR "3D visual representations" | D5 Learned object pose and keypoints for manipulation | vision | new | Optional; manipulation side. Confirm with G-P/G-A |

### E. Prediction of other agents

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| AU-022 | TOR C4 M5; UDS C9; AW object recognition "predicts trajectories"; Rudenko et al. 2020 ([arXiv 1905.06113](https://arxiv.org/abs/1905.06113)); Salzmann et al. 2020 Trajectron++ ([arXiv 2001.03093](https://arxiv.org/abs/2001.03093)); Shi et al. 2022 MTR ([arXiv 2209.13508](https://arxiv.org/abs/2209.13508)) | E1 Motion prediction: constant velocity, manoeuvre-based, learned multi-modal forecasts; ADE/FDE | robotics | new | Where other cars and people will be in a few seconds. RO 128–129 avoid others but never forecast them |
| AU-023 | TOR C4 M5 "time to collision" | E2 Collision checks against moving obstacles; time to collision | robotics | partial | RO 72 checks static obstacles only. New: checking in space and time |
| AU-024 | S237B wk 9 "Interaction-aware learning, planning and control" | E3 Interaction-aware planning: my plan changes their behaviour | robotics | partial | RO 139 has games. New: coupling prediction and planning. Optional |

### F. Planning for cars and nonholonomic robots

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| AU-025 | TOR C4 M6; UDS C5; S2 §II-B; S3 "behavior selection"; AW behaviour path/velocity planners | F1 Behaviour planning: lane keep, lane change, yield, stop, using rules and state machines | robotics | new | The middle layer that chooses the manoeuvre before the motion planner computes it |
| AU-026 | Dolgov et al. 2010, *Path planning for autonomous vehicles in unknown semi-structured environments* ([10.1177/0278364909359210](https://doi.org/10.1177/0278364909359210)); NAV2 SmacPlannerHybrid; UDS C5; CMU wk 14–15 | F2 Hybrid A*: A* whose nodes carry heading and whose edges are drivable arcs | robotics | new | The standard planner for car-like robots and parking; builds on RO 15 and RO 76 (Dubins/Reeds-Shepp, PA 15.9) |
| AU-027 | Pivtoraiko & Kelly 2009, *state lattices* ([10.1002/rob.20285](https://doi.org/10.1002/rob.20285)); NAV2 SmacPlannerLattice; CMU wk 14–15 | F3 State-lattice planning with motion primitives | robotics | partial | RO 76 has LaValle's lattice search. New: a precomputed set of feasible primitives searched with A*. Primitive generation is G-C |
| AU-028 | Werling et al. 2010, *Optimal trajectory generation … in a Frenét frame* ([10.1109/ROBOT.2010.5509799](https://doi.org/10.1109/ROBOT.2010.5509799)); UDS C5; TOR C4 M8 | F4 Frenet-frame planning: sample lateral and longitudinal curves along the lane, then pick the cheapest | robotics | new | **Check G-C.** If its trajectory-generation scope already includes Frenet sampling, drop this row |
| AU-029 | TOR C4 M8 "velocity profile generation"; AW behaviour velocity planner, obstacle stop / adaptive cruise | F5 Speed planning: stop lines, following distance, comfort limits along a fixed path | control | new | **Check G-C.** Path–velocity split; often owned by trajectory generation |
| AU-030 | NAV2 Smoothers (simple, constrained, Savitzky-Golay) | F6 Path smoothing after a grid planner | robotics | new | Short section in F2. Grid paths are jagged; smooth them before tracking |

### G. Multi-robot coordination

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| AU-031 | Stern et al. 2019, *Multi-Agent Pathfinding* ([arXiv 1906.08291](https://arxiv.org/abs/1906.08291)); Sharon et al. 2015, *Conflict-based search* ([10.1016/j.artint.2014.11.006](https://doi.org/10.1016/j.artint.2014.11.006)) | G1 Multi-agent path finding: prioritised planning, conflict-based search | robotics | partial | RO 172 (optional) has decoupled planning for many robots. New: MAPF on graphs as used in warehouses |
| AU-032 | Gerkey & Matarić 2004, *Task allocation in multi-robot systems* ([10.1177/0278364904045564](https://doi.org/10.1177/0278364904045564)); Open-RMF ([docs](https://openrmf.readthedocs.io/en/latest/)) | G2 Task allocation and fleet management: auctions, assignment | robotics | new | Which robot does which job. Optional |
| AU-033 | Rashid et al. 2018 QMIX ([arXiv 1803.11485](https://arxiv.org/abs/1803.11485)); Yu et al. 2022 MAPPO ([arXiv 2103.01955](https://arxiv.org/abs/2103.01955)) | G3 Multi-agent RL: centralised training with decentralised execution, shared policies, value factorisation | RL | partial | RO 129 has shared policies for crowds. New: the CTDE idea and MAPPO, the default baseline for robot teams. **Check with the RL-surveys agent** |

### H. Calibration

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| AU-034 | UDS C2 "Sensor and camera calibration"; Tsai & Lenz 1989, *hand/eye calibration* ([10.1109/70.34770](https://doi.org/10.1109/70.34770)); Kalibr ([repo](https://github.com/ethz-asl/kalibr)) | H1 Extrinsic calibration: camera–LiDAR, camera–IMU, hand–eye; time offsets between sensors | vision | new | G-P has camera intrinsics (Zhang 2000, [10.1109/34.888718](https://doi.org/10.1109/34.888718)). New: where each sensor sits relative to the robot. **Confirm with G-P** |
| AU-035 | RO 83 | H2 Odometry and actuator calibration | robotics | partial | Covered in spirit by system identification (RO 83); no new Note |
| AU-036 | ETH wk 4 "Motion capture systems" | H3 Ground truth: motion capture and how pose error is measured | robotics | new | Short section in K1. How experiments get true poses |

### I. Imitation learning beyond BC and DAgger

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| AU-037 | Chi et al. 2023, *Diffusion Policy* ([arXiv 2303.04137](https://arxiv.org/abs/2303.04137)); M832 ch.21; COR "Generative models" | I1 Diffusion policy: a policy that generates a short action sequence by denoising; handles multi-modal demonstrations | robotics | partial | RO 180 (NoMaD) and RO 149 use diffusion inside other systems. New: diffusion as the general imitation policy. Needs the planned DL diffusion Note |
| AU-038 | Zhao et al. 2023, ACT / ALOHA ([arXiv 2304.13705](https://arxiv.org/abs/2304.13705)) | I2 Action chunking (ACT), temporal ensembling and low-cost teleoperation for collecting demonstrations | robotics | new | Why predicting chunks reduces compounding error (links to RO 100); how demonstration data is collected |
| AU-039 | Ho & Ermon 2016, GAIL ([arXiv 1606.03476](https://arxiv.org/abs/1606.03476)); COR "Reward shaping and learning"; S237B wk 7–8 | I3 Inverse RL and adversarial imitation (GAIL) | RL | partial | RO 89 names inverse RL; RO 148 uses a discriminator reward. New: recovering a reward from demonstrations as its own method |
| AU-040 | Open X-Embodiment ([arXiv 2310.08864](https://arxiv.org/abs/2310.08864)); Octo ([arXiv 2405.12213](https://arxiv.org/abs/2405.12213)) | I4 Large cross-robot demonstration datasets and generalist BC policies | robotics | partial | RO 178 covers VLAs. New: the dataset side (many robots, one action format). Section in RO 178 |
| AU-041 | S237B wk 8–9 "Learning from human feedback", "Shared autonomy" | I5 Human feedback for robots and shared autonomy | robotics | partial | RO 181 has human corrections; RO 183 has preferences for LLMs. New: preferences and shared control for robots. Optional |

### J. Simulation tools and robot description

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| AU-042 | M42 ch.2 "Robot description files"; UDR C2; URDF ([wiki.ros.org/urdf](https://wiki.ros.org/urdf)); MJCF ([MuJoCo XML reference](https://mujoco.readthedocs.io/en/stable/XMLreference.html)) | J1 Robot description formats: URDF/Xacro, SDF, MJCF: links, joints, inertias, collision vs visual shapes | software | new | Every simulator and ROS stack starts from one. Builds on RO 52 |
| AU-043 | M42 ch.5 "Contact simulation"; COR "Simulation"; M832 App. A (Drake, [drake.mit.edu](https://drake.mit.edu/)); [Gazebo docs](https://gazebosim.org/docs); [Isaac Sim docs](https://docs.isaacsim.omniverse.nvidia.com/latest/index.html); RL scope row R0.9 | J2 How a physics simulator steps: time step, contact and friction models; choosing Gazebo vs MuJoCo vs Isaac vs Drake | software | partial | RO 81 covers the Isaac training stack. New: what the simulator computes and where it lies to you (links to RO 82, the reality gap) |
| AU-044 | TOR C1 M7, C4 final project; Dosovitskiy et al. 2017 CARLA ([arXiv 1711.03938](https://arxiv.org/abs/1711.03938)) | J3 Driving simulators and scenario-based testing | software | new | Section in K3 |

### K. Evaluation, benchmarks and remaining robot-learning skills

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| AU-045 | Agarwal et al. 2021, *Deep RL at the Edge of the Statistical Precipice* ([arXiv 2108.13264](https://arxiv.org/abs/2108.13264)) | K1 Reporting RL results honestly: many seeds, interquartile mean, confidence intervals | RL | new | Every RL-for-navigation paper is judged on this. Builds on MA confidence intervals. **Check with the RL-surveys agent** |
| AU-046 | Perille et al. 2020, BARN ([arXiv 2008.13315](https://arxiv.org/abs/2008.13315)); Batra et al. 2020, ObjectNav ([arXiv 2006.13171](https://arxiv.org/abs/2006.13171)); Francis et al. 2023, social navigation evaluation ([arXiv 2306.16740](https://arxiv.org/abs/2306.16740)) | K2 Navigation benchmarks and protocols: BARN, Habitat challenges, social-navigation metrics | robotics | partial | RO 115 has success, SPL and collisions. New: the standard benchmark suites, and how to compare against classical planners fairly |
| AU-047 | Caesar et al. 2021, nuPlan ([arXiv 2106.11810](https://arxiv.org/abs/2106.11810)); CARLA leaderboard ([leaderboard.carla.org](https://leaderboard.carla.org/)); Chen et al. 2023 | K3 Open-loop vs closed-loop evaluation of driving planners | robotics | new | Why a planner that matches logged data can still crash when it drives itself |
| AU-048 | M42 ch.5 grasp selection; S237B wk 4–5 | K4 Grasp selection: antipodal grasps, friction cones, grasp quality, grasps from point clouds | robotics | new | **Confirm G-A.** RO 153 learns grasps; nothing teaches what makes a grasp good |
| AU-049 | M42 ch.5 "Programming the task level"; Garrett et al. 2021, TAMP ([arXiv 2010.01083](https://arxiv.org/abs/2010.01083)); Ahn et al. 2022, SayCan ([arXiv 2204.01691](https://arxiv.org/abs/2204.01691)) | K3b Task-level planning: task and motion planning, language models choosing skills | robotics | partial | RO 151 is motion only. New: deciding the sequence of skills (pick, then place). Optional |
| AU-050 | M42 ch.12 | K5 Tactile sensing | robotics | new | Optional; manipulation depth |
| AU-051 | Pathak et al. 2017, ICM ([arXiv 1705.05363](https://arxiv.org/abs/1705.05363)); Burda et al. 2018, RND ([arXiv 1810.12894](https://arxiv.org/abs/1810.12894)) | K6 Curiosity and intrinsic rewards for exploration | RL | new | Not in any scope doc (grep: no "curiosity", "intrinsic", "RND"). Sparse-reward navigation and exploration use it. **Check with the RL-surveys agent** |
| AU-052 | Anderson et al. 2018, VLN ([arXiv 1711.07280](https://arxiv.org/abs/1711.07280)) | K7 Vision-and-language navigation | robotics | new | Follow a spoken route instruction. RO 109 has point-, object- and image-goal tasks only |
| AU-053 | Laskin et al. 2020, CURL ([arXiv 2004.04136](https://arxiv.org/abs/2004.04136)); Kostrikov et al. 2020, DrQ ([arXiv 2004.13649](https://arxiv.org/abs/2004.13649)) | K8 RL from pixels: image augmentation and contrastive auxiliary losses | RL | partial | RO 105 has auxiliary tasks; DL-050 has augmentation. New: why augmentation stabilises pixel RL. **Check with the RL-surveys agent** |

## 4. Prerequisites between the new concepts

- A4 (frames) ← new MA rigid transforms. A3 (ROS 2) ← A4. A2 (stack) ← RO 107, A3.
- A5 (BTs/FSMs) ← A2. A6 ← A5. A7 ← A2, RO 127. A9 ← A7.
- B1 (costmaps) ← RO 68, RO 72. B2 ← RO 68. B4 ← RO 15. B3 ← B4, A4.
- C1 (GNSS) ← A4, RO 64 (fusion goes to G-P). C2 (NDT) ← RO 58, G-P ICP, B3.
- D1, D2 ← DL-040, DL-051. D4 ← D1, G-P LiDAR. D3 ← RO 63, RO 161, D1.
- E1 ← D3, DL-064/DL-087 (for learned forecasts). E2 ← E1, RO 72. E3 ← E1, RO 139.
- F1 ← A5, E1, B3. F2 ← RO 15, RO 76. F3 ← F2, G-C primitives. F4/F5 ← G-C. F6 ← F2.
- G1 ← RO 15, RO 172. G2 ← G1. G3 ← RO 45, RO 129.
- H1 ← G-P cameras, A4.
- I1 ← RO 100, DL diffusion (planned). I2 ← RO 100, DL-087. I3 ← RO 89, RO 148. I4, I5 ← RO 178, RO 181.
- J1 ← RO 52. J2 ← J1, RO 81.
- K1 ← MA confidence intervals. K2 ← RO 115, K1. K3 ← J3, E1. K6 ← RO 4, RO 93. K7 ← RO 109, DL-083. K8 ← RO 105, DL-050.

## 5. Suggested learning order

The primary interest is navigation with RL, so the software and stack Notes come early, beside RO-15. The car-specific planning Notes follow after it.

1. **Before RO 107 (the Nav2 Note):** A4 frames → A3 ROS 2 → J1 robot description → A2 the stack → B1 costmaps → A5 behaviour trees (+A6).
2. **With RO-15:** K2 benchmarks, K1 honest RL evaluation, J2 simulators.
3. **After RO-16:** K6 curiosity, K8 pixel RL, K7 VLN.
4. **New chapter "Driving and other agents"**, after RO-18:
   - D1 → D2 → D4 → D3 → E1 → E2;
   - then B4 → B3 → C1 → C2;
   - then F1 → F2 (+F6) → F3, with F4/F5 if G-C lacks them;
   - then A7 → K3/J3 → A9 (optional) → E3 (optional).
5. **Multi-robot (optional, beside RO-23):** G1 → G2 → G3.
6. **Into RO-24, after RO 100:** I3 → I1 → I2 → I4 → I5.
7. **Manipulation extras:** K4 (if G-A lacks it) → K3b → D5 → K5 (optional).
8. **Calibration:** H1 with G-P; H3 as a section in K2.

## 6. New maths these rows need that MA lacks

The rows rely on the MA Notes already planned in robotics.md §3 (rigid transforms, Gaussian transforms, stability). These are not yet planned anywhere:

| Concept | What | First needed by |
|---|---|---|
| Geodetic coordinates and map projections | Latitude/longitude → local east-north-up metres; UTM zones | C1 |
| Recursive least squares | Update a least-squares fit one measurement at a time (TOR C2 M1); a bridge to the Kalman filter | C1 (also helps RO 63) |
| Polynomial and spline curves | Cubic/quintic polynomials and splines as smooth paths | F4, F6 (check G-C, which may already add it) |
| Normal distributions on a grid cell (NDT) | Each cell's points summarised by a mean and covariance; score a scan against them | C2 (short section) |
| Assignment problem (Hungarian algorithm) | Match N tracks to M detections at least total cost | D3, G2 |
| Intersection over union and non-max suppression | Box overlap as a number; keep only the best box | D1 (short section) |
| Bootstrap confidence intervals and the interquartile mean | Error bars from resampling few seeds | K1 (check MA for bootstrap) |

## 7. Coverage table: curriculum × topic → status

A cell `x` means the curriculum (or survey taxonomy) teaches the topic. **Status** says where it lives in our plan.

Survey codes: S1 Siegwart see–think–act · S2 Paden layers · S3 Badue · S4 Yurtsever · S5 González planner families.

| Topic | TOR | ETH | CMU | FRE | M42 | M832 | S237B | COR | UDS | UDR | NAV2 | AW | Survey taxonomy | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Autonomy stack / layered architecture | x | | x | | | | | | | | x | x | S1 see–think–act; S2 all layers; S3; S4 architectures | **MISSING A2** (RO 107 partial) |
| Levels of automation, ODD | x | | | | | | | | | | | | S3 scope (SAE ≥3) | **MISSING A1** |
| ROS 2 middleware | | | | | | | | | | x | x | x | S4 tools | **MISSING A3** |
| Frames and transform tree | | | x | | x | | | | | | x | x | S1 kinematics | **MISSING A4** |
| Behaviour trees / state machines | x | | | | | | | | x | | x | | S2 behavioural layer | **MISSING A5** |
| Recovery, goal/progress checks | | | | | | | | | | | x | | none | **MISSING A6** |
| Fail-safe, diagnostics, validation | | | | | | | | | | | | x | S4 assessment | **MISSING A7** (RO 127 partial) |
| Safety assurance, functional safety | x | | | | | | | | x | | | | S4 assessment | **MISSING A9** |
| Sensor suite design | x | x | | | x | | | | | | | x | S3 perception; S4 sensors | G-P + **MISSING A8** |
| Rigid transforms, rotations | | x | x | | x | | | | | | | | S1 kinematics | MA new (planned) |
| Wheeled kinematics, pose | x | x | x | x | | | | | x | | | | S1 kinematics | RO 50 |
| Vehicle/bicycle dynamics, tyres | x | | x | | | | | | x | | | x | S2 control | G-C |
| PID | x | | | x | | | | x | x | | | x | S2 control | RO 56 |
| Pure pursuit, Stanley, MPC, path following | x | | x | | | | | x | x | | x | x | S2 control; S3 control | G-C |
| Trajectory generation, speed profiles | x | | x | | | | | | x | | | x | S2 motion planning; S5 curves | G-C; **F5 check** |
| Frenet-frame planning | x | | | | | | | | x | | | | S5 curves | **MISSING F4 (check G-C)** |
| Probability, Bayes | | x | x | x | | | | | | | | | S1 localization | MA |
| Kalman / EKF | x | x | x | x | | | | | x | x | | x | S1, S3 localization | RO 63, 64 |
| UKF | x | | | | | | | | x | | | | none | RO 158 |
| Particle filter, MCL | | | x | x | | | | | | x | x | | S1 localization | RO 65, 67 |
| Least squares / RLS | x | | | | | | | | | | | | none | ML-053 + new maths (RLS) |
| IMU, INS, error-state EKF | x | x | x | | | | | | | | | x | S3 localization | G-P |
| GNSS / RTK | x | x | x | | | | | | | | x | x | S3, S4 localization | **MISSING C1** |
| LiDAR model, scan matching, ICP | x | x | | | x | | | | x | | | x | S3 localization | RO 57–58, G-P |
| NDT, localising in a prior 3D map | | | | | | | | | x | | | x | S3, S4 localization | **MISSING C2** |
| Cameras, calibration (intrinsic), stereo | x | x | | | x | | | x | x | | | | S1 perception | G-P |
| Extrinsic / hand-eye calibration | | | | | | | | | x | | | | none | **MISSING H1** |
| Features, VO, SfM, place recognition | x | x | x | | | | | | | | | x | S1 perception | G-P |
| 2D object detection | x | | | | x | | x | | x | | | x | S3 moving obstacles; S4 perception | **MISSING D1** |
| Semantic segmentation | x | | | | x | | x | x | x | | x | | S4 perception | **MISSING D2** |
| LiDAR object detection, ground seg | | | | | | | | | x | | x | x | S3 static/moving obstacles | **MISSING D4** |
| Multi-object tracking | x | | | | | | | | x | | | x | S3 moving obstacle tracking | **MISSING D3** (RO 161 partial) |
| Traffic-light recognition | | | | | | | | | | | | x | S3 traffic signalization | **MISSING (inside D1)** |
| Learned pose / keypoints | | | | | x | | | x | | | | | none | **MISSING D5 (optional)** |
| Motion prediction | x | | | | | | | | x | | | x | S3 moving obstacles; S4 assessment | **MISSING E1** |
| Time to collision, dynamic collision | x | | | | | | | | | | | | S2 motion planning | **MISSING E2** |
| Interaction-aware planning | | | | | | | x | | | | | | none | **MISSING E3 (optional)** |
| Occupancy grid mapping | x | | | x | | | | | | x | x | x | S1 map building; S3 static mapping | RO 68 |
| Layered costmaps, inflation | | | | | | | | | | | x | | none | **MISSING B1** |
| 3D maps (voxel, octree, elevation) | | | | x | | | | | | | x | | S1 map building | **MISSING B2** |
| HD / vector maps | x | | | | | | | | | | | x | S3 road mapping; S4 mapping | **MISSING B3** |
| SLAM (EKF, graph, FastSLAM) | | x | | x | | | | | | x | x | | S1 map building; S4 mapping | RO 69, 163–167 |
| Route / mission planning on a road graph | x | | | | | | | | | | x | x | S2 route; S3 route | **MISSING B4** (RO 14–15 partial) |
| Graph search: Dijkstra, A* | x | x | | x | | | | | | x | x | | S5 graph search | RO 13–15 |
| Behaviour planning | x | | | | | | | | x | | | x | S2 behavioural; S3 behaviour selection | **MISSING F1** |
| DWA / trajectory rollout / TEB | x | x | x | | | | | | | | x | | S2 motion planning | RO 106 |
| Hybrid A* | | | x | | | | | | x | | x | | S5 graph search | **MISSING F2** |
| State lattice | | | x | | | | | | | | x | | S5 graph search | **MISSING F3** (RO 76 partial) |
| Path smoothing | | | | | | | | | | | x | | S5 curves | **MISSING F6** |
| Sampling planners RRT/PRM | | x | x | x | x | x | | | | x | | | S5 sampling | RO 74, 75 |
| Planning under motion constraints | | x | x | | | | | | | | | | S5 | RO 76 |
| Trajectory optimisation | | | | | x | x | | | | | | | S5 numerical optimisation | RO 77 |
| D* / replanning | | | x | | | | | | | | | | none | RO 71 |
| Coverage planning | | | | | | | | | | | x | | none | RO 173 |
| LQR, DP, Lyapunov | | | | | | x | | | | | | | none | RO 174, 18; MA new |
| Arms: FK, Jacobians, IK, force control | | | | | x | | | | | | | | none | G-A |
| Legged models, limit cycles, contact | | | | | | x | | | | | | | S1 locomotion | G-A |
| Grasp selection (model-based) | | | | | x | | x | | | | | | none | **MISSING K4 (confirm G-A)** |
| Task-level / TAMP | | | | | x | | | | | | | | none | **MISSING K3b** |
| Tactile sensing, soft robots | | | | | x | | | | | | | | none | **MISSING K5 (optional)** |
| Multi-agent path finding | | | | | | | | | | | | | none | **MISSING G1** (RO 172 partial) |
| Task allocation, fleets | | | | | | | | | | | | | S4 connected systems | **MISSING G2** |
| Multi-agent RL (CTDE) | | | | | | | | | | | | | none | **MISSING G3** (RO 129 partial) |
| MDPs and RL algorithms | | | | | x | x | x | x | | | | | S4 emerging methods | RO 1–48 |
| Model-based RL | | | | | x | | x | x | | | | | none | RO 135, 142 |
| System identification | | | | | | x | | | | | | | none | RO 83 |
| Imitation learning: BC, DAgger | | | | | | x | x | x | | | | | S4 end-to-end | RO 100 |
| Diffusion policy | | | | | | x | | x | | | | | none | **MISSING I1** (RO 180 partial) |
| Action chunking, teleop data | | | | | | | | | | | | | none | **MISSING I2** |
| Inverse RL / GAIL | | | | | | | x | x | | | | | none | **MISSING I3** (RO 89 partial) |
| Human feedback, shared autonomy | | | | | | | x | | | | | | S4 HMI | **MISSING I5 (optional)** |
| Visuomotor policies | | | | | | x | | x | | | | | S4 end-to-end | RO 152 |
| Transfer, multi-task, foundation models | | | | | | | | x | | | | | none | RO 82, 178 |
| Robot description (URDF/MJCF) | | | | | x | | | | | x | x | | none | **MISSING J1** |
| Physics simulators | x | x | | | x | x | | x | | x | | | S4 tools | RO 81 partial + **MISSING J2** |
| Driving simulators, scenario testing | x | | | | | | | | | | | | S4 datasets and tools | **MISSING J3** |
| Benchmarks and metrics | | | | | | | | | | | | | S4 datasets | RO 115 partial + **MISSING K2, K3** |
| Statistically sound RL evaluation | | | | | | | | | | | | | none | **MISSING K1** |
| Curiosity / intrinsic reward | | | | | | | | | | | | | none | **MISSING K6** |
| Vision-language navigation | | | | | | | | | | | | | none | **MISSING K7** |

Rows with no curriculum `x` (MAPF, MARL, K1, K6, K7) come from the brief's focus list and the cited papers, not from these 12 syllabi.
