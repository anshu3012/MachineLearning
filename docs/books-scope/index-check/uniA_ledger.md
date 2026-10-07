# University course schedules vs the robotics plan (agent uniA)

Checklist = lecture-by-lecture schedules of 12 university courses (mobile robotics, estimation/SLAM, planning, robot software), from their official course pages, fetched 2026-10-07. Every listed lecture topic is a term; a lecture listing several topics gives one term each.
Matching: `robo_match.py` against `docs/books-scope/robotics.md`, the evidence docs, MA/ML/DL Notes and `glossary.md`; then every row judged by hand against the cited Note's title and Teaches column (MA/ML/DL: body text). `plan §4 X` = a new MA Note the plan already lists.
Not used (no public lecture schedule found): Penn MEAM 620 (alliance.seas.upenn.edu page is 2007), Toronto AER1513/ROB521 (Quercus only), CMU 16-833 (Fall 2024 page has no schedule), CMU 16-362 (404), MIT 16.412 (not checked: 16.410 is the planning twin). Stanford AA274B (Winter 2025) skipped: its schedule is learning/manipulation, outside this agent's areas.

## Coverage summary

| Course | Term | Topics | taught | add | out-of-scope | index-noise |
|---|---|---|---|---|---|---|
| UCSD ECE276A: Sensing & Estimation in Robotics | Winter 2026 | 18 | 17 | 1 | 0 | 0 |
| UCSD ECE276B: Planning & Learning in Robotics | Spring 2026 | 17 | 15 | 2 | 0 | 0 |
| CMU 16-350: Planning Techniques for Robotics (undergrad twin of 16-782) | Spring 2026 | 28 | 21 | 7 | 0 | 0 |
| CMU 16-761: Mobile Robotics (Kelly) | course calendar dated 31 Oct 2016 (latest public) | 38 | 34 | 3 | 0 | 1 |
| Stanford AA274A: Principles of Robot Autonomy I | Fall 2025 | 52 | 50 | 1 | 1 | 0 |
| Michigan ROB 530: Mobile Robotics: Methods and Algorithms (NA/EECS 568) | Winter 2022 (latest public slides) | 17 | 14 | 1 | 2 | 0 |
| ETH AMR: Autonomous Mobile Robots 151-0854-00L | Spring 2021 (latest public agenda) | 41 | 37 | 4 | 0 | 0 |
| Bonn MSR1: Mobile Sensing and Robotics 1 (Stachniss part) | Winter 2021/22 | 17 | 17 | 0 | 0 | 0 |
| Bonn MSR2: Mobile Sensing and Robotics 2 | Summer 2021 | 25 | 24 | 0 | 1 | 0 |
| Freiburg IMR: Introduction to Mobile Robotics | Summer 2024 | 12 | 12 | 0 | 0 | 0 |
| MIT 16.410: Principles of Autonomy and Decision Making (OCW) | Fall 2010 (latest OCW) | 25 | 13 | 2 | 10 | 0 |
| Georgia Tech CS 3630: Introduction to Perception and Robotics | Fall 2026 | 26 | 25 | 1 | 0 | 0 |
| **All 12** | | 316 | 279 | 22 | 14 | 1 |

## UCSD ECE276A: Sensing & Estimation in Robotics (Winter 2026)

Source: https://natanaso.github.io/ece276a/schedule.html

Counts: taught 17, add 1, out-of-scope 0, index-noise 0 (total 18).

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| Matrix calculus | L1 Introduction | taught | ML-053 (three rules of matrix calculus); MA-063 |
| Unconstrained optimization | L2-3 Unconstrained Optimization | taught | ML-056 gradient descent; MA-064 Newton's method; MA-065 cost functions |
| Rotations (rotation representations) | L4-5 Rotations | taught | plan §4 '3D rotations: Euler angles and quaternions' and 'Axis-angle, exp/log maps' |
| Robot motion models | L6 Robot Motion and Observation Models | taught | N68 probabilistic motion models |
| Observation models | L6 Robot Motion and Observation Models | taught | N74 beam model; N76 landmark measurement model |
| Factor graph SLAM | L7 Factor Graph SLAM | taught | N263 factor graphs; N101 pose graphs |
| Localization from point features | L8-9 Localization and Odometry from Point Features | taught | N233 PnP and relative pose from E |
| Odometry from point features | L8-9 Localization and Odometry from Point Features | taught | N234 feature-based visual odometry |
| Bayes filter | L10-11 Bayes Filter | taught | N78 |
| Particle filter | L12-13 Particle Filter SLAM | taught | N82 |
| Particle filter SLAM | L12-13 Particle Filter SLAM | taught | N266 FastSLAM (Rao-Blackwellised PF, grid-based FastSLAM) |
| Kalman filter | L14 Kalman Filter | taught | N80 |
| Extended Kalman filter (EKF) | L15-16 EKF, UKF | taught | N81 |
| Unscented Kalman filter (UKF) | L15-16 EKF, UKF | taught | N256 |
| Matrix Lie groups | L17 Matrix Lie Groups | add | **Matrix Lie groups for estimation: SO(3)/SE(3) as groups, tangent-space (Lie algebra) perturbations, uncertainty on poses** (maths) → RO-22 new Note before N263 (builds on plan §4 'Axis-angle, exponential and log maps of rotations') |
| Visual-inertial SLAM | L18 Visual-Inertial SLAM | taught | N264 visual-inertial odometry (MSCKF, VINS) |
| Visual features | L19 Visual Features | taught | N227 corners; N228 descriptors |
| Dense mapping | L20 Dense Mapping | taught | N97 signed-distance (TSDF) maps |

## UCSD ECE276B: Planning & Learning in Robotics (Spring 2026)

Source: https://natanaso.github.io/ece276b/schedule.html

Counts: taught 15, add 2, out-of-scope 0, index-noise 0 (total 17).

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| Markov chains | L2 Markov Chains | taught | plan §4 'Markov chains' (new MA Note) |
| Markov decision processes | L4 Markov Decision Processes | taught | N7 |
| Dynamic programming | L5 Dynamic Programming | taught | N12-N15 policy evaluation, PI, VI, asynchronous DP |
| Deterministic shortest path | L6 Deterministic Shortest Path | taught | N104 Dijkstra's shortest-path algorithm |
| Configuration space | L7 Configuration Space | taught | N72 |
| Search-based planning | L8 Search-based Planning (LaValle 2.1-2.3, JPS) | taught | N103-N105 |
| Jump point search (JPS) | L8 Search-based Planning (LaValle 2.1-2.3, JPS) | add | **Jump point search on uniform grids** (robotics) → named variant in N105 |
| Anytime search (ARA*) | L10 Anytime Incremental Search (RTAA*, ARA*, AD*) | taught | N105 (ARA* named as a variant) |
| Incremental search (AD*) | L10 Anytime Incremental Search (RTAA*, ARA*, AD*) | taught | N107 D* replanning, D* Lite |
| Real-time search (RTAA*) | L10 Anytime Incremental Search (RTAA*, ARA*, AD*) | add | **Real-time heuristic search (LRTA*, RTAA*): plan a few steps, move, update the heuristic** (robotics) → RO-05 after N107 |
| Sampling-based planning | L11 Sampling-based Planning | taught | N110 RRT; N111 PRM |
| Infinite-horizon optimal control | L12-13 Infinite-Horizon Optimal Control | taught | N8 infinite horizon: discounted and average cost; N205 infinite-horizon LQR |
| Model-free prediction (MC and TD) | L15 Model-Free Prediction | taught | N16 MC prediction; N19 TD(0) |
| Model-free control (SARSA, Q-learning) | L16 Model-Free Control | taught | N20 Sarsa; N21 Q-learning |
| Value function approximation | L17 Value Function Approximation | taught | N25, N26 |
| Linear quadratic control (LQR) | L18 Linear Quadratic Control | taught | N205 |
| Continuous-time optimal control | L19 Continuous-Time Optimal Control | taught | N205 Hamilton-Jacobi-Bellman equation |

## CMU 16-350: Planning Techniques for Robotics (undergrad twin of 16-782) (Spring 2026)

Source: https://www.cs.cmu.edu/~maxim/classes/robotplanning/

Counts: taught 21, add 7, out-of-scope 0, index-noise 0 (total 28).

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| Robot planning problem | 1/12 Introduction, What is Robot Planning? | taught | N72 basic motion planning problem; N9 plans |
| Skeleton-based graphs (visibility graph, Voronoi) | 1/14 Planning Representations | taught | N270 exact roadmaps (visibility graph, generalized Voronoi) |
| Grid-based graphs | 1/14 Planning Representations | taught | N106 grid path planning |
| Lattice-based graphs (state lattice) | 1/14 Planning Representations | taught | N114 state lattices |
| Explicit vs implicit graphs | 1/14 Planning Representations | add | **Explicit vs implicit graphs; choosing a Markov search state (drop dependent variables)** (robotics) → short section in N103 |
| Uninformed search (BFS, Dijkstra) | 1/21 Search Algorithms: Uninformed A* Search | taught | N103 BFS/DFS; N104 Dijkstra |
| A* search | 1/26 A* Search, Multi-goal A* | taught | N105 |
| Multi-goal A* | 1/26 A* Search, Multi-goal A* | add | **Multi-goal A* (one virtual goal joined to all goals; moving targets)** (robotics) → short section in N105 |
| Heuristics (admissible, consistent) | 1/28 Heuristics, Backward A*, Weighted A* | taught | N105 admissible heuristic |
| Backward A* | 1/28 Heuristics, Backward A*, Weighted A* | taught | N105 backward and bidirectional search |
| Weighted A* | 1/28 Heuristics, Backward A*, Weighted A* | taught | N105 weighted A* |
| Anytime heuristic search | 2/2 Anytime Heuristic Search | taught | N105 anytime A* (ARA*) |
| Incremental heuristic search (D* Lite) | 2/4 Incremental Heuristic Search | taught | N107 |
| Real-time heuristic search | 2/9 Real-time Heuristic Search | add | **Real-time heuristic search (LRTA*, RTAA*): plan a few steps, move, update the heuristic** (robotics) → RO-05 after N107 |
| Planning for autonomous driving | 2/11 Case Study: Planning for Autonomous Driving | taught | N113 Hybrid A*; N246 behaviour planning; N247 Frenet planning |
| Probabilistic roadmap (PRM) | 2/16 Probabilistic Roadmaps | taught | N111 |
| RRT | 2/18-23 RRT, RRT-Connect, RRT* | taught | N110 |
| RRT-Connect | 2/18-23 RRT, RRT-Connect, RRT* | add | **Bidirectional RRT (RRT-Connect)** (robotics) → section in N110 |
| RRT* | 2/18-23 RRT, RRT-Connect, RRT* | taught | N110 |
| Planning for mobile manipulators and arms | 2/25 Case Study: Mobile Manipulators and Articulated Robots | taught | N292 manipulation planning; N72 C-space |
| Markov property in search state design (independent vs dependent variables) | 3/9 Markov property, independent vs dependent variables | add | **Explicit vs implicit graphs; choosing a Markov search state (drop dependent variables)** (robotics) → short section in N103 |
| Coverage planning | 3/11 Case Study: Coverage, Mapping and Surveyal | taught | N273 |
| Symbolic task planning representation (STRIPS/PDDL) | 3/16 Symbolic Representation for Task Planning | add | **Symbolic task planning: STRIPS/PDDL states, actions with pre/postconditions, forward search over them** (robotics) → RB-03 new Note before N293 (reverses plan §7 drop of PA 2.10-2.13) |
| Search over symbolic representations | 3/23-25 Planning on Symbolic Representations | add | **Symbolic task planning: STRIPS/PDDL states, actions with pre/postconditions, forward search over them** (robotics) → RB-03 new Note before N293 (reverses plan §7 drop of PA 2.10-2.13) |
| Minimax planning under uncertainty | 3/30 Planning under Uncertainty: Minimax | taught | N53 worst-case vs expected-cost decisions |
| Expected-value planning under uncertainty | 4/1 Expected Value Formulation | taught | N53 |
| Solving MDPs | 4/6 Solving MDPs | taught | N13 policy iteration; N14 value iteration |
| Multi-robot planning | 4/13-15 Multi-Robot Planning | taught | N271 centralized vs decoupled multi-robot planning; N272 MAPF |

## CMU 16-761: Mobile Robotics (Kelly) (course calendar dated 31 Oct 2016 (latest public))

Source: https://www.cs.cmu.edu/~alonzo/teaching/16-761/16-761.html

Counts: taught 34, add 3, out-of-scope 0, index-noise 1 (total 38).

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| Introduction to mobile robots | Intro 1 | index-noise | course introduction lecture, no concept |
| Orthogonal transforms (rotations, homogeneous transforms) | Kin 1 Orthogonal Transforms | taught | plan §4 'Rigid-body transforms and homogeneous coordinates'; N65 |
| Kinematics of mechanisms | Kin 2 Kinematics of Mechanisms | taught | N69 kinematic chains and forward kinematics |
| Kinematic models of sensors and actuators | Kin 3 Kinematic Models of Sensors and Actuators | taught | N65 transform tree (base_link to sensor) |
| Transform graphs and pose networks | Kin 4 Transform Graphs & Pose Networks | taught | N65 coordinate frames and the transform tree |
| Fundamentals of uncertainty (random variables, covariance) | Unc 1 Fundamentals of Uncertainty | taught | MA-020 random variables; MA-012; MA-009 covariance |
| Combining uncertain measurements (covariance propagation, fusion) | Unc 2 Combining Uncertain Measurements | taught | plan §4 'Linear transforms of a Gaussian' and 'Product of two Gaussians' |
| Kalman filters | Unc 3 Kalman Filters | taught | N80 |
| Bayes rule applications | Unc 4 Applications of Bayes Rule | taught | MA-018, MA-019 |
| Particle filters | Unc 5 Particle Filters | taught | N82 |
| Ground vehicle dynamics | Dyn 1 Ground Vehicle Dynamics | taught | N250-N252 (RO-21) |
| Linear systems theory | Dyn 2 Linear Systems Theory and Stochastic Calculus | taught | plan §4 'State-space models'; N204 controllability |
| Stochastic calculus (random processes, noise integration) | Dyn 2 Linear Systems Theory and Stochastic Calculus | add | **Random processes for estimation: white noise, random walk, Gauss-Markov process, discretising process noise Q** (maths) → short section in RO-02 before N80 (or MA 03-distributions new Note) |
| Physics of measurement | Pos 1 Physics of Measurement | add | **Sensor characteristics and error types: range, resolution, bandwidth, accuracy vs precision, systematic vs random error** (robotics) → short opening section of RO-03 (before N83) |
| Mathematics of position estimation (dead reckoning, triangulation) | Pos 2 Mathematics of Position Estimation | taught | N68 odometry (dead reckoning); N85 ranging to satellites |
| Sensors for position estimation (odometry, encoders) | Pos 3 Sensors for Position Estimation | taught | N86 wheel odometry from encoders |
| Inertial navigation systems | Pos 4 Inertial Navigation Systems | taught | N84 strapdown inertial navigation |
| Satellite navigation (GNSS) | Pos 5 Satellite Navigation Systems | taught | N85 |
| Stability estimation (vehicle tip-over) | Pos 6 Stability Estimation | taught | N295 centre of mass, support polygon, static balance |
| Hierarchical control | Ctr 1 Hierarchical Control / Motion Autonomy | taught | N126 autonomy-stack layers; N119 cascaded loops |
| Wheeled mobile robot kinematics | Ctr 2 Kinematics of WMRs | taught | N64, N66 |
| Trajectory generation | Ctr 3 Trajectory Generation | taught | N201, N202 polynomial and spline trajectories |
| Obstacle avoidance | Ctr 4 Obstacle Avoidance | taught | N129 DWA/TEB; N109 potential fields; N107 bug algorithms |
| Path and trajectory following | Ctr 5 Path and Trajectory Following | taught | N121 |
| Mathematics for perception (projection, image geometry) | Per 1 Mathematics for Perception | taught | N88 pinhole projection |
| Physics of radiative sensors | Per 2 Physics of Radiative Sensors | taught | N91 how LiDAR works (time of flight); radar named |
| Sensors for perception (lidar, radar, cameras) | Per 3 Sensors for Perception | taught | N88-N91 |
| Perception algorithms (obstacle detection, terrain) | Per 4 Perception Algorithms | taught | N176 point-cloud obstacles; N177 traversability |
| Visual tracking | Per 5 Visual Tracking & Servoing | taught | N230 pyramidal KLT tracker |
| Visual servoing | Per 5 Visual Tracking & Servoing | add | **Visual servoing: image-based and position-based, control law from the image Jacobian** (control) → RO-18 after N231 |
| Map representations | Map 1 Intro to Maps and Representation | taught | N71 feature vs grid maps; N97 3D maps |
| Perception-based localization | Map 2 Perception Based Localization | taught | N75 scan matching; N99 NDT localization |
| Globally consistent mapping (loop closure) | Map 3 Globally Consistent Mapping | taught | N102 loop closure |
| SLAM | Map 4 SLAM | taught | N100 |
| Motion planning | Pln 1 Introduction to Motion Planning | taught | N72 |
| Motion planning algorithms | Pln 2 Algorithms for Motion Planning | taught | N103-N111 |
| Real-time planning in dynamic environments (replanning) | Pln 3 Real-Time Planning & Dynamic Environments | taught | N107 D* replanning; N271 time-varying obstacles |
| Nonholonomic motion planning | Pln 4 Nonholonomic Motion Planning | taught | N112 kinodynamic planning, Dubins/Reeds-Shepp |

## Stanford AA274A: Principles of Robot Autonomy I (Fall 2025)

Source: https://stanfordasl.github.io/PoRA-I/aa274a_aut2526/

Counts: taught 50, add 1, out-of-scope 1, index-noise 0 (total 52).

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| Perception-action loop | 09/23 Course overview, perception-action loop, maps | taught | N126 sense-plan-act |
| Maps | 09/23 Course overview, perception-action loop, maps | taught | N71 maps and landmarks |
| Coordinate frames | 09/25 Maps, robot geometry, coordinate frames, SE(2)/SE(3) | taught | N65 |
| SE(2)/SE(3) transforms | 09/25 Maps, robot geometry, coordinate frames, SE(2)/SE(3) | taught | plan §4 'Rigid-body transforms' (SE(2)/SE(3)) |
| Collision checking | 09/30 Collision, C-space, motion models, A* | taught | N108 |
| Configuration space (C-space) | 09/30 Collision, C-space, motion models, A* | taught | N72, N73 |
| Motion models | 09/30 Collision, C-space, motion models, A* | taught | N68 |
| A* path planning | 09/30 Collision, C-space, motion models, A* | taught | N105 |
| RRT | 10/02 Path planning II: RRT, RRT* | taught | N110 |
| RRT* | 10/02 Path planning II: RRT, RRT* | taught | N110 |
| Trajectory optimization | 10/07 Trajectory optimization | taught | N116 |
| Trajectory following | 10/09 Trajectory following: PID, LQR, gain-scheduled LQR | taught | N121 path following vs trajectory tracking; N124 |
| PID control | 10/09 Trajectory following: PID, LQR, gain-scheduled LQR | taught | N117 |
| LQR | 10/09 Trajectory following: PID, LQR, gain-scheduled LQR | taught | N205 |
| Gain-scheduled LQR | 10/09 Trajectory following: PID, LQR, gain-scheduled LQR | taught | N255 gain scheduling; N206 time-varying LQR |
| IMU | 10/14 Sensors: IMU, lidar, cameras, RGB-D; point clouds & ICP | taught | N83 |
| Lidar | 10/14 Sensors: IMU, lidar, cameras, RGB-D; point clouds & ICP | taught | N91 |
| Cameras | 10/14 Sensors: IMU, lidar, cameras, RGB-D; point clouds & ICP | taught | N88 |
| RGB-D sensors | 10/14 Sensors: IMU, lidar, cameras, RGB-D; point clouds & ICP | taught | N90 depth cameras |
| Point clouds | 10/14 Sensors: IMU, lidar, cameras, RGB-D; point clouds & ICP | taught | N91 |
| ICP | 10/14 Sensors: IMU, lidar, cameras, RGB-D; point clouds & ICP | taught | N92 |
| Pinhole camera model | 10/16 Pinhole camera models, camera calibration | taught | N88 |
| Camera calibration | 10/16 Pinhole camera models, camera calibration | taught | N89 |
| Structure from motion | 10/21 Structure from Motion, features, RANSAC | taught | N235 |
| Image features | 10/21 Structure from Motion, features, RANSAC | taught | N227, N228 |
| RANSAC | 10/21 Structure from Motion, features, RANSAC | taught | N229 |
| Learning-based perception | 10/23 Learning-based perception, semantic perception | taught | N173-N175 detection and segmentation |
| Semantic perception | 10/23 Learning-based perception, semantic perception | taught | N175 semantic segmentation; N177 semantic maps |
| SLAM | 10/28 SLAM intro, factor graphs, PGO | taught | N100 |
| Factor graphs | 10/28 SLAM intro, factor graphs, PGO | taught | N263 |
| Pose graph optimization | 10/28 SLAM intro, factor graphs, PGO | taught | N101 pose graphs and GraphSLAM |
| Bundle adjustment | 10/30 Pose graph opt, bundle adjustment | taught | N235 |
| Bayes rule | 11/06 Bayes rule, RVs, occupancy mapping | taught | MA-018 |
| Random variables | 11/06 Bayes rule, RVs, occupancy mapping | taught | MA-020 |
| Occupancy grid mapping | 11/06 Bayes rule, RVs, occupancy mapping | taught | N96 |
| Frontier exploration | 11/11 Occupancy mapping, frontier exploration | add | **Frontier-based exploration: drive to the boundary between known-free and unknown cells** (robotics) → section in N181 |
| Gaussian random variables | 11/13 Gaussian RVs, Kalman filtering, EKF, UKF | taught | MA-024; MA-073 multivariate normal |
| Kalman filter | 11/13 Gaussian RVs, Kalman filtering, EKF, UKF | taught | N80 |
| EKF | 11/13 Gaussian RVs, Kalman filtering, EKF, UKF | taught | N81 |
| UKF | 11/13 Gaussian RVs, Kalman filtering, EKF, UKF | taught | N256 |
| Particle filter | 11/18 Particle filtering, Monte Carlo localization | taught | N82 |
| Monte Carlo localization | 11/18 Particle filtering, Monte Carlo localization | taught | N95 |
| EKF localization | 12/02 EKF localization, object tracking | taught | N258 |
| Object tracking | 12/02 EKF localization, object tracking | taught | N178 multi-object tracking |
| Imitation learning | 12/04 Advanced topics | taught | N165 behaviour cloning, DAgger; RB-08 |
| Vision-language-action models (VLAs) | 12/04 Advanced topics | taught | N349 |
| 3D Gaussian splatting for sim2real | 12/04 Advanced topics | out-of-scope | research-only: listed under the course's 'Advanced Topics' lecture (12/04); a 2023 scene-reconstruction method |
| World models | 12/04 Advanced topics | taught | N50; N356 |
| ROS (Robot Operating System) | Labs (ROS) | taught | N127 ROS 2 |
| RViz visualisation | Labs (ROS) | taught | N127 (RViz listed) |
| Heading controller | Labs (ROS) | taught | N120 moving to a pose (heading) |
| Navigation to goal | Labs (ROS) | taught | N120; N131 Nav2 stack |

## Michigan ROB 530: Mobile Robotics: Methods and Algorithms (NA/EECS 568) (Winter 2022 (latest public slides))

Source: https://github.com/UMich-CURLY-teaching/UMich-ROB-530-public (linked from curly.engin.umich.edu/teaching)

Counts: taught 14, add 1, out-of-scope 2, index-noise 0 (total 17).

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| Probability review | Notes 01 Probability | taught | MA-014, MA-015, MA-018 |
| Estimation (least squares, MAP, MLE) | Notes 02 Estimation | taught | ML-053 OLS; MA-070 MLE; MA-072 MAP |
| Kalman filtering | 02 Kalman Filtering | taught | N80 |
| Nonlinear Kalman filtering (EKF, UKF) | 03 Nonlinear Kalman Filtering | taught | N81 EKF; N256 UKF |
| Particle filtering | 04 Particle Filtering | taught | N82 |
| Rigid body motion | 05 Rigid Body Motion | taught | plan §4 'Rigid-body transforms'; N275 twists and screw motion |
| Matrix Lie groups | 06-07 Matrix Lie Groups | add | **Matrix Lie groups for estimation: SO(3)/SE(3) as groups, tangent-space (Lie algebra) perturbations, uncertainty on poses** (maths) → RO-22 new Note before N263 (builds on plan §4 'Axis-angle, exponential and log maps of rotations') |
| Uncertainty propagation in robot motion | 08 Robot Motion and Uncertainty Propagation | taught | N68 motion as a distribution; plan §4 'Linear transforms of a Gaussian'; N81 |
| Invariant EKF | 09-10 Invariant EKF | out-of-scope | research-only: Barrau-Bonnabel invariant filtering (2017), the instructor's research area; needs Lie groups beyond beginner depth |
| Localization | 11 Localization | taught | N94, N95 |
| Occupancy grid mapping | 12 OGM | taught | N96 |
| Robotic mapping (semantic, continuous maps) | 13 Robotic Mapping | taught | N177 semantic maps |
| Nonlinear least squares optimization (Gauss-Newton, LM) | 14-15 Optimization I-II | taught | plan §4 'Nonlinear least squares (Gauss-Newton)' and 'Levenberg-Marquardt' |
| Point cloud registration (ICP) | 16 Pointcloud Registration I | taught | N92 |
| RKHS (kernel) registration | 17 RKHS Registration | out-of-scope | research-only: the instructor's own registration method (continuous visual odometry in an RKHS) |
| RGB-D visual odometry | 18 RGB-D VO | taught | N234 visual odometry (direct vs feature-based); N90 depth cameras |
| Graph SLAM | 19-20 Graph SLAM I-II | taught | N101 |

## ETH AMR: Autonomous Mobile Robots 151-0854-00L (Spring 2021 (latest public agenda))

Source: https://asl.ethz.ch/education/lectures/autonomous_mobile_robots/spring-2021.html (agenda PDF AMR_Program_2021 V3)

Counts: taught 37, add 4, out-of-scope 0, index-noise 0 (total 41).

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| Legged robotics introduction | W2 Locomotion Concepts | taught | N295 gaits, support polygon |
| Rigid body kinematics | W2 Locomotion Concepts | taught | plan §4 'Rigid-body transforms'; N275 |
| Wheeled, legged and flying robots | W2 Locomotion Concepts | taught | N66 wheel types; N295 legs; N221 quadrotor |
| Wheeled locomotion | W3 Mobile Robot Kinematics | taught | N66 |
| Differential kinematics | W3 Mobile Robot Kinematics | taught | N64 wheel speeds to (v, w) |
| Wheeled kinematics | W3 Mobile Robot Kinematics | taught | N64, N66, N67 |
| Sensors (classification, characteristics) | W4 Perception I | add | **Sensor characteristics and error types: range, resolution, bandwidth, accuracy vs precision, systematic vs random error** (robotics) → short opening section of RO-03 (before N83) |
| IMU | W4 Perception I | taught | N83 |
| GPS | W4 Perception I | taught | N85 |
| Motion capture systems | W4 Perception I | taught | N161 ground truth: motion capture |
| Laser range finder | W4 Perception I | taught | N91 LiDAR; N74 beam model |
| RGB-D / time-of-flight cameras | W4 Perception I | taught | N90 structured light and time of flight |
| Sonar (ultrasonic range sensors) | W4 Perception I | add | **Ultrasonic (sonar) range sensors: time of flight of sound, wide beam, specular reflection** (robotics) → named in N91 (range sensors) |
| Camera image formation, perspective projection | W5 Perception II | taught | N88 |
| Introduction to computer vision | W5 Perception II | taught | N227; DL-042 image as a grid |
| Omnidirectional projection | W5 Perception II | taught | N89 fisheye and spherical models |
| Camera calibration | W5 Perception II | taught | N89 |
| Stereo vision | W5 Perception II | taught | N90 |
| Structure from motion | W5 Perception II | taught | N235 |
| Correlation and convolution | W6 Perception III: Image Saliency | taught | DL-042 (convolution vs cross-correlation) |
| Edge detection | W6 Perception III: Image Saliency | add | **Edge detection: image gradients, Canny, Laplacian of Gaussian** (vision) → section in N227 |
| Point (corner) detection | W6 Perception III: Image Saliency | taught | N227 Harris, Shi-Tomasi, FAST |
| Image filtering | W6 Perception III: Image Saliency | taught | N227 |
| Place recognition | W7 Perception IV | taught | N236 |
| Error propagation law | W7 Perception IV | taught | plan §4 'Linear transforms of a Gaussian' (A Sigma A^T); N81 linearisation |
| Line extraction | W7 Perception IV | add | **Line extraction from 2D laser scans: split-and-merge, line fitting with uncertainty, Hough transform** (robotics) → RO-04 near N75 (or with N71 features) |
| Map-based localization | W8 Localization I | taught | N94 |
| Probability theory refresher | W8 Localization I | taught | MA-014, MA-018 |
| Markov localization | W9 Localization II | taught | N94 |
| Kalman filter localization | W9 Localization II | taught | N258 EKF localization |
| The SLAM problem | W10 SLAM I | taught | N100 |
| Monocular SLAM | W11 SLAM II | taught | N236 visual SLAM; N233 scale ambiguity |
| EKF SLAM | W11 SLAM II | taught | N261 |
| Motion planning | W12 Planning I | taught | N72 |
| Representations and configuration space | W12 Planning I | taught | N72, N73 |
| Graph search methods | W12 Planning I | taught | N103-N105 |
| Collision avoidance | W12 Planning I | taught | N129 DWA; N109 potential fields; N107 bug algorithms |
| Sampling-based planning | W13 Planning II | taught | N110, N111 |
| Planning under motion constraints | W13 Planning II | taught | N112 planning with motion limits |
| Dijkstra's algorithm | Ex6 | taught | N104 |
| Dynamic window approach | Ex6 | taught | N129 |

## Bonn MSR1: Mobile Sensing and Robotics 1 (Stachniss part) (Winter 2021/22)

Source: https://www.ipb.uni-bonn.de/msr1-2021/index.html

Counts: taught 17, add 0, out-of-scope 0, index-noise 0 (total 17).

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| Probability primer | W1 Probability primer | taught | MA-014, MA-018 |
| Bayes filter | W2 Bayes filter | taught | N78 |
| Occupancy grid maps | W3 Occupancy grid maps | taught | N96 |
| Robot locomotion | W4 Robot locomotion | taught | N64, N66 |
| Probabilistic motion models | W5 Motion models | taught | N68 |
| Observation models for range sensors | W6 Observation models | taught | N74, N75 |
| Kalman filter | W7 Kalman filter & EKF | taught | N80 |
| Extended Kalman filter | W7 Kalman filter & EKF | taught | N81 |
| Robot localization overview | W8 Robot localization, EKF localization | taught | N94 |
| EKF localization | W8 Robot localization, EKF localization | taught | N258 |
| Particle filter | W9 Particle filter and MCL | taught | N82 |
| Monte Carlo localization | W9 Particle filter and MCL | taught | N95 |
| Robot control | W10 Robot control | taught | N117 PID; N120 driving to a point/pose |
| Model predictive control | W11 MPC part 1 | taught | N207 |
| Numerical methods for MPC | W12 MPC part 2: numerical methods | taught | N208 SQP/interior point overview, real-time MPC |
| A* motion planning | W13 Motion planning using A* | taught | N105 |
| MDPs for planning under uncertainty | W14 MDPs for planning under uncertainty | taught | N7; N106 value iteration on a robot grid |

## Bonn MSR2: Mobile Sensing and Robotics 2 (Summer 2021)

Source: https://www.ipb.uni-bonn.de/msr2-2021/index.html

Counts: taught 24, add 0, out-of-scope 1, index-noise 0 (total 25).

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| SLAM problem | W1 Introduction to SLAM | taught | N100 |
| Least squares | W2 Least squares; ICP part 1 (known data association, SVD) | taught | ML-053 ordinary least squares |
| Point cloud registration with known correspondences (SVD) | W2 Least squares; ICP part 1 (known data association, SVD) | taught | N92 aligning two point sets (SVD/Kabsch) |
| Iterative closest point (unknown data association) | W3 ICP parts 2-3 | taught | N92 |
| Robust nonlinear least squares ICP (Gauss-Newton) | W3 ICP parts 2-3 | taught | plan §4 'Nonlinear least squares (Gauss-Newton)' and 'robust losses'; N92 |
| Pose-graph SLAM | W4 Graph-based SLAM using pose graphs | taught | N101 |
| Hierarchical pose graphs | W5 Hierarchical pose graphs; graph SLAM with landmarks; bundle adjustment | out-of-scope | research-only: a specific speed-up method (hierarchical optimisation, HOG-Man 2010), not a core concept |
| Graph SLAM with landmarks | W5 Hierarchical pose graphs; graph SLAM with landmarks; bundle adjustment | taught | N101 GraphSLAM |
| Bundle adjustment | W5 Hierarchical pose graphs; graph SLAM with landmarks; bundle adjustment | taught | N235 |
| Robust least squares (robust kernels) | W6 Robust least squares for graph SLAM | taught | N102 robust kernels; N235 robust cost functions |
| What cameras measure | W7 What cameras measure; keypoints | taught | N88 pinhole camera |
| Keypoint detection | W7 What cameras measure; keypoints | taught | N227 |
| SIFT | W8 SIFT, binary features, descriptors | taught | N228 |
| Binary features (BRIEF/ORB) | W8 SIFT, binary features, descriptors | taught | N228 ORB binary descriptors |
| Feature descriptors | W8 SIFT, binary features, descriptors | taught | N228 |
| RANSAC | W9 RANSAC | taught | N229 |
| Camera intrinsics and extrinsics | W10 Camera intrinsics and extrinsics | taught | N88 |
| Projection of 3D points to pixels | W11 Mapping 3D to image; DLT; Zhang calibration | taught | N88 camera matrix P = K[R|t] |
| Direct linear transform (DLT) | W11 Mapping 3D to image; DLT; Zhang calibration | taught | N89 |
| Zhang's camera calibration | W11 Mapping 3D to image; DLT; Zhang calibration | taught | N89 calibration with a checkerboard |
| Perspective-3-point (P3P) / spatial resection | W12 P3P (Grunert) | taught | N233 PnP |
| Relative orientation | W13 Relative orientation, fundamental/essential matrix, epipolar geometry | taught | N233 recovering R and t from E |
| Fundamental and essential matrix | W13 Relative orientation, fundamental/essential matrix, epipolar geometry | taught | N232 |
| Epipolar geometry | W13 Relative orientation, fundamental/essential matrix, epipolar geometry | taught | N232 |
| 8-point algorithm | W14 8-point algorithm | taught | N232 |

## Freiburg IMR: Introduction to Mobile Robotics (Summer 2024)

Source: https://rl.uni-freiburg.de/teaching/ss24/mobile-robotics

Counts: taught 12, add 0, out-of-scope 0, index-noise 0 (total 12).

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| Probability theory | 02 Probability Theory | taught | MA-014, MA-018 |
| Sensor models | 03 Sensor Models | taught | N74, N75, N76 |
| Motion models | 04 Motion Models | taught | N68 |
| Particle filter | 05 Particle Filter | taught | N82 |
| Kalman filter | 06 Kalman Filter | taught | N80 |
| Grid mapping | 07 Grid Mapping | taught | N96 |
| SLAM | 08 SLAM | taught | N100 |
| FastSLAM | 09 FastSLAM and Graph-based SLAM | taught | N266 |
| Graph-based SLAM | 09 FastSLAM and Graph-based SLAM | taught | N101 |
| 3D mapping techniques (octrees, elevation maps) | 10 Techniques for 3D Mapping | taught | N97 |
| Motion and path planning | 11 Motion and Path Planning | taught | N105, N110 |
| Control systems | 12 Control Systems | taught | N117 |

## MIT 16.410: Principles of Autonomy and Decision Making (OCW) (Fall 2010 (latest OCW))

Source: https://ocw.mit.edu/courses/16-410-principles-of-autonomy-and-decision-making-fall-2010/pages/lecture-notes/

Counts: taught 13, add 2, out-of-scope 10, index-noise 0 (total 25).

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| State space search | L2 State space search | taught | N103 graph as a model of a state space |
| Complexity of search | L3 Complexity of state space search | taught | N103 Big-O and exponential time |
| Soundness and completeness of search | L4 Soundness and completeness of search | taught | N111 complete / resolution-complete / probabilistically complete |
| Constraint programming | L5 Constraint programming | out-of-scope | different field: symbolic AI / logic programming; no other of the 12 courses teaches it and no plan Note uses CSPs |
| Constraint satisfaction | L6 Constraint satisfaction | out-of-scope | different field: symbolic AI (CSPs); same reason as constraint programming |
| Conflict-directed backjumping | L7 Conflict-directed backjumping; activity planning | out-of-scope | different field: CSP-solver algorithm detail |
| Activity planning | L7 Conflict-directed backjumping; activity planning | add | **Symbolic task planning: STRIPS/PDDL states, actions with pre/postconditions, forward search over them** (robotics) → RB-03 new Note before N293 (reverses plan §7 drop of PA 2.10-2.13) |
| Graphplan | L8 Graph plan | out-of-scope | different field: a specific classical-AI planner (1995); the beginner idea is forward search in the symbolic-planning add |
| Plan execution | L9 Plan termination and execution | taught | N130 behaviour trees, progress checks, recovery |
| Propositional logic and SAT | L10 Propositional logic and satisfiability | out-of-scope | different field: logic / computer-science theory |
| Encoding planning as SAT | L11 Planning as SAT | out-of-scope | different field: logic-based AI planning |
| Model-based diagnosis and mode estimation | L12 Diagnosis and mode estimation | out-of-scope | research-only: MIT model-based autonomy (Livingstone-style) research line |
| Optimal satisfiability / conflict-directed A* | L13 OpSat and conflict-directed A* | out-of-scope | research-only: the lecturers' own OpSat method |
| Informed search (A*) | L14 Global path planning I: informed search | taught | N105 |
| Sampling-based motion planning | L15 Sampling-based motion planning | taught | N110, N111 |
| Mathematical programming | L16 Mathematical programming I | taught | MA-068 linear and quadratic programming |
| Simplex method | L17 Simplex method | taught | MA-068 (simplex algorithm, G-2259) |
| Mixed-integer linear programming for routing and planning | L18 MILP for vehicle routing and motion planning | add | **Mixed-integer linear programs (MILP): integer choices in LP, why they are harder, use for routing and obstacle-side choices** (maths) → short section in MA-068 |
| Probabilistic reasoning | L19 Reasoning in an uncertain world | taught | MA-014, MA-018 |
| Hidden Markov models | L20 Hidden Markov models | taught | N77 |
| Baum-Welch algorithm | L21 Baum-Welch | out-of-scope | different field: HMM parameter learning (speech/sequence ML); no plan Note fits HMM parameters; EM itself is MA-074 |
| Markov decision processes | L22-23 MDPs, policy iteration | taught | N7 |
| Policy iteration | L22-23 MDPs, policy iteration | taught | N13 |
| Sequential games | L24 Sequential games | taught | N54 sequential games on state spaces |
| Differential games | L25 Differential games | out-of-scope | research-only: plan §7 drops PA 13.12 (differential games, advanced theory); pursuit-evasion |

## Georgia Tech CS 3630: Introduction to Perception and Robotics (Fall 2026)

Source: https://dellaert.github.io/26F-3630/schedule.html (official course site of GT CS 3630)

Counts: taught 25, add 1, out-of-scope 0, index-noise 0 (total 26).

| Term | Lecture | Verdict | Where / why |
|---|---|---|---|
| Robot system components (sense, think, act) | L2 Six aspects of robotics systems | taught | N126 sense-plan-act |
| Bayesian thinking | L3 Bayesian thinking | taught | MA-018 |
| Discrete state and actions | L4 State, probability, and actions | taught | N63 state, controls, measurements; N7 |
| Sensor models | L5 Sensor models | taught | N74, N76 |
| Perception and planning (decision from posterior) | L6 Perception and planning | taught | N53 Bayesian decision making with observations |
| Probabilistic actions | L7 Probabilistic actions | taught | N7 MDP dynamics p(s'|s,a); N68 |
| Controlled Markov chains | L8 Controlled Markov chains | taught | N7; plan §4 'Markov chains' |
| Bayes nets | L9 Sensors and Bayes nets | add | **Bayesian networks: a joint distribution as a product of local conditionals drawn as a graph** (maths) → MA 02-probability new Note (before N77; factor graphs N263 build on it) |
| Inference in HMMs | L10 Inference in HMMs | taught | N77 HMM; N78 Bayes filter (forward filtering) |
| Markov decision processes | L11 MDPs | taught | N7 |
| Continuous state and action | L12 Continuous state and action | taught | N68 continuous motion models; N80 linear Gaussian system |
| Continuous motion and sensing models | Oct 8 Continuous motion and sensing | taught | N68, N74 |
| Markov localization | Oct 13-15 Markov localization and MCL | taught | N94 |
| Monte Carlo localization | Oct 13-15 Markov localization and MCL | taught | N95 |
| System identification | Oct 20 System identification | taught | N139 |
| Differential drive | Oct 22 Differential drive | taught | N64 |
| Cameras | Oct 27 Cameras and image processing | taught | N88 |
| Image processing | Oct 27 Cameras and image processing | taught | N227 image filtering |
| Computer vision basics | Oct 29 Computer vision 101 | taught | N227; DL-042 |
| Deep learning for perception | Nov 3-5 Inference with deep nets | taught | DL-040-DL-053 CNNs; N173 |
| SE(2) | Nov 10 Autonomous vehicles and SE(2) | taught | plan §4 'Rigid-body transforms' (SE(2)) |
| Ackermann steering | Nov 12 Ackermann steering | taught | N67 |
| Lidar sensors | Nov 17 LIDAR sensors | taught | N91 |
| ICP | Nov 19 ICP and pose SLAM | taught | N92 |
| Pose SLAM | Nov 19 ICP and pose SLAM | taught | N101 pose graphs |
| Planning for driving | Nov 24 Planning for driving | taught | N246, N247 |
