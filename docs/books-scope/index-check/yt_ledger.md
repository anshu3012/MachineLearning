# yt ledger: university lecture playlists as completeness checklists

Method: each playlist's titles listed with `yt-dlp --flat-playlist` (no cookies, no downloads; metadata saved in `yt/pl/`). Every title is a term; titles naming several topics are split (`yt_terms.py`). CS 285 and CS223A titles carry no topic, so the topic comes from the course page lecture list (CS 285) and each video's description (CS223A). Terms were script-matched against the plan, evidence docs, MA/ML/DL Notes and glossary (`robo_match.py`, results `yt/flat.json`), then judged by hand (`yt_build.py`). A `taught` verdict cites a Note whose title or Teaches column (MA/ML/DL: body; plan §4/§5: its row) names the concept.

Pages column = video numbers in the playlist (v1 = first video).

Substitutions: ETH Zurich has no official YouTube lecture playlist for Robot Dynamics or Autonomous Mobile Robots (the RSL channel's 'Lectures and Talks' playlist is research talks; AMR recordings are on the ETH video portal and edX). Replaced by Stanford CS223A (Khatib), the nearest official university lecture course on robot kinematics and dynamics. Brunton's Control Bootcamp (UW faculty, personal channel) and the MATLAB Tech Talks are kept as secondary sources, per the owner's preference for university playlists.

| Key | Playlist | Videos | Terms | URL | Course page |
|---|---|---|---|---|---|
| msr1 | Stachniss (Uni Bonn): Mobile Sensing and Robotics 1, Winter 2021/22 | 21 | 19 | https://www.youtube.com/playlist?list=PLgnQpQtFTOGQEn33QDVGJpiZLi-SlL7vA | https://www.ipb.uni-bonn.de/teaching/index.html |
| msr2 | Stachniss (Uni Bonn): Mobile Sensing and Robotics 2, Summer 2021 | 37 | 33 | https://www.youtube.com/playlist?list=PLgnQpQtFTOGQh_J16IMwDlji18SWQ2PZ6 | https://www.ipb.uni-bonn.de/teaching/index.html |
| slam | Stachniss (Uni Freiburg/Bonn): SLAM Course 2013/14 | 22 | 22 | https://www.youtube.com/playlist?list=PLgnQpQtFTOGQrZ4O5QzbIHgl3b1JHimN_ | http://ais.informatik.uni-freiburg.de/teaching/ws13/mapping/ |
| pg | Stachniss (Uni Bonn): Photogrammetry I & II, 2021 | 68 | 60 | https://www.youtube.com/playlist?list=PLgnQpQtFTOGRYjqjdZxTEQPZuFHQa7O7Y | https://www.ipb.uni-bonn.de/teaching/index.html |
| rc | Stachniss lab (Uni Bonn): Robot Control Lecture 2025 | 6 | 7 | https://www.youtube.com/playlist?list=PLgnQpQtFTOGT_BlLxVnsuI-7CEQCgNuk4 | https://www.ipb.uni-bonn.de/teaching/index.html |
| mr | Lynch (Northwestern): Modern Robotics, All Videos | 97 | 80 | https://www.youtube.com/playlist?list=PLggLP4f-rq02vX0OQQ5vrCxbJrzamYDfx | https://hades.mech.northwestern.edu/index.php/Modern_Robotics_Videos |
| ua | Tedrake (MIT): 6.8210 Underactuated Robotics, Spring 2024 | 24 | 31 | https://www.youtube.com/playlist?list=PLkx8KyIQkMfU5szP43GlE_S1QGSPQfL9s | https://underactuated.csail.mit.edu/Spring2024/index.html |
| cs285 | Levine (UC Berkeley): CS 285 Deep RL, Fall 2023 | 99 | 25 | https://www.youtube.com/playlist?list=PL_iWQOsE6TfVYGEGiAOMaOzzv41Jfm_Ps | https://rail.eecs.berkeley.edu/deeprlcourse-fa23/ |
| cs223a | Khatib (Stanford): CS223A Introduction to Robotics (replaces ETH Robot Dynamics) | 16 | 16 | https://www.youtube.com/playlist?list=PL65CC0384A1798ADF | https://see.stanford.edu/Course/CS223A |
| fpcv | Nayar (Columbia): First Principles of Computer Vision (12 module playlists) | 145 | 154 | https://www.youtube.com/playlist?list= (12 playlists, see table) | https://fpcv.cs.columbia.edu/ |
| cb | Brunton (Univ. Washington): Control Bootcamp [secondary] | 39 | 36 | https://www.youtube.com/playlist?list=PLMrJAkhIeNNR20Mz-VpzgfQs5zrYi085m | https://www.eigensteve.com/ |
| ucs | MATLAB Tech Talks (Douglas): Understanding Control Systems [secondary] | 6 | 6 | https://www.youtube.com/playlist?list=PLn8PRpmsu08q8CE0pbZ-cSrMm_WYJfVGd | https://www.mathworks.com/academia/courseware/understanding-control-systems-tech-talks.html |
| pid | MATLAB Tech Talks (Douglas): Understanding PID Control [secondary] | 7 | 7 | https://www.youtube.com/playlist?list=PLn8PRpmsu08pQBgjxYFXSsODEF3Jqmm-y | https://www.mathworks.com/academia/courseware/pid-control-tech-talks.html |
| csip | MATLAB Tech Talks (Douglas): Control Systems in Practice [secondary] | 15 | 17 | https://www.youtube.com/playlist?list=PLn8PRpmsu08pFBqgd_6Bi7msgkWFKL33b | https://www.mathworks.com/academia/courseware/control-systems-in-practice-tech-talks.html |

Counts per playlist: {"msr1": {"index-noise": 2, "taught": 17}, "msr2": {"index-noise": 1, "taught": 31, "out-of-scope": 1}, "slam": {"index-noise": 3, "taught": 17, "out-of-scope": 2}, "pg": {"index-noise": 5, "taught": 46, "add": 8, "out-of-scope": 1}, "rc": {"taught": 5, "add": 2}, "mr": {"index-noise": 3, "taught": 72, "out-of-scope": 4, "add": 1}, "ua": {"taught": 23, "add": 4, "out-of-scope": 3, "index-noise": 1}, "cs285": {"index-noise": 4, "taught": 19, "out-of-scope": 2}, "cs223a": {"index-noise": 2, "taught": 14}, "fpcv": {"index-noise": 29, "out-of-scope": 38, "taught": 54, "add": 33}, "cb": {"index-noise": 1, "taught": 13, "out-of-scope": 5, "add": 17}, "ucs": {"add": 6}, "pid": {"taught": 3, "add": 4}, "csip": {"index-noise": 2, "taught": 4, "add": 9, "out-of-scope": 2}}

## Stachniss (Uni Bonn): Mobile Sensing and Robotics 1, Winter 2021/22

Videos: 21. Course page: https://www.ipb.uni-bonn.de/teaching/index.html

- https://www.youtube.com/playlist?list=PLgnQpQtFTOGQEn33QDVGJpiZLi-SlL7vA

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| Course Intro for Mobile Sensing and Robotics I | v1 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Probability Primer for Probabilistic Robotics | v2 | taught | MA-014 (joint, marginal, conditional), MA-018 (Bayes' theorem), MA-024 (normal); plan §5 recaps |
| Bayes Filter | v3 | taught | Note 78 (The Bayes filter: predict, then update) |
| Occupancy grid maps | v4,v5 | taught | Note 96 (Occupancy grid mapping) |
| Robot Locomotion | v6 | taught | Note 66 (wheel types, omnidirectional bases, unicycle); Note 295 (gaits) |
| Motion Models | v7 | taught | Note 68 (velocity and odometry motion models) |
| Observation Models | v8 | taught | Note 74 (beam model, catalogue of sensor models); Note 76 (landmark model) |
| Kalman filter | v9,v10 | taught | Note 80 (Kalman filter) |
| Extended Kalman filter (EKF) | v10 | taught | Note 81 (Extended Kalman filter) |
| Robot Localization - An Overview | v11,v21 | taught | Note 94 (tracking, global and kidnapped-robot localization) |
| EKF Localization | v12 | taught | Note 258 (EKF localization with landmarks) |
| Particle filter | v13,v14 | taught | Note 82 (Particle filter) |
| Monte Carlo localization | v14 | taught | Note 95 (Monte Carlo localization) |
| Robot Control | v15 | taught | Note 284 (velocity inputs, PD plus gravity, computed torque) |
| Model predictive control (MPC) | v16 | taught | Note 207 (receding horizon, constraints, QP) |
| Numerical methods for MPC | v17 | taught | Note 208 (SQP and interior point overview, real-time MPC) |
| Robot Motion Planning using A* | v18 | taught | Note 105 (A* and heuristics) |
| Markov Decision Processes for Planning under Uncertainty | v19 | taught | Note 7 (Markov decision processes); Note 14 (value iteration) |
| Outlook: Further M.Sc. Courses from the Photogrammetry & Robotics Lab at Bonn University (2021) | v20 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |

## Stachniss (Uni Bonn): Mobile Sensing and Robotics 2, Summer 2021

Videos: 37. Course page: https://www.ipb.uni-bonn.de/teaching/index.html

- https://www.youtube.com/playlist?list=PLgnQpQtFTOGQh_J16IMwDlji18SWQ2PZ6

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| Welcome to the Mobile Sensing and Robotics 2 Course | v1 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Introduction to SLAM | v2,v3 | taught | Note 100 (The SLAM problem) |
| Least Squares | v4,v5 | taught | ML-053 (normal equation); plan §4 'Nonlinear least squares (Gauss-Newton)' |
| Iterative closest point (ICP), known data association | v6,v7 | taught | Note 92 (ICP; point-to-plane and Generalized-ICP; aligning two point sets by SVD/Kabsch); plan §4 Gauss-Newton |
| Point cloud registration via SVD | v7 | taught | Note 92 (ICP; point-to-plane and Generalized-ICP; aligning two point sets by SVD/Kabsch); plan §4 Gauss-Newton |
| ICP with unknown data association | v8 | taught | Note 92 (ICP; point-to-plane and Generalized-ICP; aligning two point sets by SVD/Kabsch); plan §4 Gauss-Newton |
| Point-to-Plane and Generalized ICP | v9 | taught | Note 92 (ICP; point-to-plane and Generalized-ICP; aligning two point sets by SVD/Kabsch); plan §4 Gauss-Newton |
| ICP as non-linear least squares | v10 | taught | Note 92 (ICP; point-to-plane and Generalized-ICP; aligning two point sets by SVD/Kabsch); plan §4 Gauss-Newton |
| Graph-based SLAM using Pose Graphs | v11 | taught | Note 101 (Pose graphs and GraphSLAM) |
| Graph-Based SLAM with Landmarks | v12 | taught | Note 101 (Pose graphs and GraphSLAM) |
| Bundle adjustment | v13 | taught | Note 235 (bundle adjustment, Schur complement, Levenberg-Marquardt) |
| Hierarchical Pose Graphs for SLAM | v14 | out-of-scope | speed-up for very large maps (implementation/research detail); the pose graph itself is Note 101 |
| Robust Least Squares for Graph-Based SLAM | v15 | taught | Note 102 (robust kernels, switchable constraints) |
| What Cameras Measure | v16 | taught | Note 88 (pinhole camera, camera matrix P = K[R\|t]) |
| Visual Feature Part 1: Computing Keypoints | v17 | taught | Note 227 (point features, Harris and Shi-Tomasi corners, FAST) |
| SIFT | v18 | taught | Note 228 (scale-space blobs, SIFT, ORB binary descriptors) |
| Binary Features | v19 | taught | Note 228 (scale-space blobs, SIFT, ORB binary descriptors) |
| Visual Features Part 2: Features Descriptors | v20 | taught | Note 228 (scale-space blobs, SIFT, ORB binary descriptors) |
| RANSAC | v21,v22 | taught | Note 229 (RANSAC) |
| Camera extrinsic parameters | v23,v24 | taught | Note 88 (intrinsics K, extrinsics) |
| Camera intrinsic parameters | v23,v24 | taught | Note 88 (intrinsics K, extrinsics) |
| Mapping the 3D world to an image | v25 | taught | Note 88 (pinhole camera, camera matrix P = K[R\|t]) |
| Direct linear transform (DLT) | v26,v27 | taught | Note 89 (checkerboard calibration, DLT; Zhang 2000) |
| Camera calibration | v27 | taught | Note 89 (checkerboard calibration, DLT; Zhang 2000) |
| Camera localization (pose from known points) | v27 | taught | Note 233 (PnP: camera pose from known 3D points) |
| Camera Calibration using Zhang's Method | v28,v29 | taught | Note 89 (checkerboard calibration, DLT; Zhang 2000) |
| Projective 3-point algorithm (P3P, Grunert) | v30,v31 | taught | Note 233 (PnP: camera pose from known 3D points) |
| Fundamental matrix | v32,v33 | taught | Note 232 (epipolar geometry, E and F, normalised 8-point) |
| Essential matrix | v32,v33 | taught | Note 232 (epipolar geometry, E and F, normalised 8-point) |
| Relative orientation | v33 | taught | Note 233 (recovering R and t from E); Note 235 (iterative refinement) |
| Stereo Normal Case | v34 | taught | Note 90 (stereo camera model, disparity, dense matching along rows) |
| Epipolar Geometry Basics | v35 | taught | Note 232 (epipolar geometry, E and F, normalised 8-point) |
| 8-point algorithm | v36,v37 | taught | Note 232 (epipolar geometry, E and F, normalised 8-point) |

## Stachniss (Uni Freiburg/Bonn): SLAM Course 2013/14

Videos: 22. Course page: http://ais.informatik.uni-freiburg.de/teaching/ws13/mapping/

- https://www.youtube.com/playlist?list=PLgnQpQtFTOGQrZ4O5QzbIHgl3b1JHimN_

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| Course Introduction | v1 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Introduction to Robot Mapping | v2 | taught | Note 71 (Maps and landmarks); Note 100 (SLAM problem) |
| Homogeneous Coordinates | v3 | taught | plan §4 'Rigid-body transforms and homogeneous coordinates' and 'Projective homogeneous coordinates'; Note 88 |
| Bayes Filter | v4 | taught | Note 78 (The Bayes filter: predict, then update) |
| Extended Kalman filter (EKF) | v5 | taught | Note 81 (Extended Kalman filter) |
| EKF SLAM | v6 | taught | Note 261 (EKF SLAM) |
| Unscented Kalman Filter | v7 | taught | Note 256 (Unscented Kalman filter) |
| Extended Information Filter | v8 | taught | Note 257 (information filter and extended information filter) |
| Sparse Extended Information Filter | v9,v10 | out-of-scope | plan §7 drops SEIF (PR 12.1-12.3): superseded by GraphSLAM and FastSLAM for a beginner |
| Short Kalman Filter Wrap-Up | v11 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Occupancy grid maps | v12 | taught | Note 96 (Occupancy grid mapping) |
| Particle filter | v13 | taught | Note 82 (Particle filter) |
| FastSLAM | v14 | taught | Note 266 (Rao-Blackwellization, FastSLAM, grid-based FastSLAM) |
| Grid-based SLAM | v15 | taught | Note 266 (Rao-Blackwellization, FastSLAM, grid-based FastSLAM) |
| Rao-Blackwellized particle filter | v15 | taught | Note 266 (Rao-Blackwellization, FastSLAM, grid-based FastSLAM) |
| Least Squares | v16 | taught | ML-053 (normal equation); plan §4 'Nonlinear least squares (Gauss-Newton)' |
| Least squares SLAM | v17,v18 | taught | Note 101 (Pose graphs and GraphSLAM) |
| Hierarchical Pose Graphs for SLAM | v18 | out-of-scope | speed-up for very large maps (implementation/research detail); the pose graph itself is Note 101 |
| Graph-Based SLAM with Landmarks | v19 | taught | Note 101 (Pose graphs and GraphSLAM) |
| Robust Least Squares for Graph-Based SLAM | v20 | taught | Note 102 (robust kernels, switchable constraints) |
| SLAM Frontends | v21 | taught | Note 236 (front-end vs back-end) |
| Short Summary | v22 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |

## Stachniss (Uni Bonn): Photogrammetry I & II, 2021

Videos: 68. Course page: https://www.ipb.uni-bonn.de/teaching/index.html

- https://www.youtube.com/playlist?list=PLgnQpQtFTOGRYjqjdZxTEQPZuFHQa7O7Y

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| Introduction to Photogrammetry | v1 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| What Cameras Measure | v2 | taught | Note 88 (pinhole camera, camera matrix P = K[R\|t]) |
| Camera basics | v3 | taught | Note 88 (pinhole camera, camera matrix P = K[R\|t]) |
| Propagation of light | v3 | add | **lens_basics**: RO-03, section of Note 88 |
| Image histogram | v4,v5 | add | **img_histogram**: RO-18, new first Note before Note 227 |
| Point operators | v5 | add | **img_histogram**: RO-18, new first Note before Note 227 |
| Histogram transformations (equalization) | v6 | add | **img_histogram**: RO-18, new first Note before Note 227 |
| Binary Images | v7 | add | **binary_images**: RO-18, new Note after the point-operators Note |
| Image convolution | v8 | taught | DL-042 (convolution operation) |
| Smoothing filters | v8 | taught | Note 227 (image filtering: smoothing and gradient filters) |
| Gradient filters | v9 | taught | Note 227 (image filtering: smoothing and gradient filters) |
| Geometric Transformation of Images | v10 | add | **image_warping**: RO-18, section of Note 229 (RANSAC and homographies) |
| Image Matching using Cross Correlation | v11 | add | **template_matching**: RO-18, new section before Note 228 (descriptors and matching) |
| Visual Feature Part 1: Computing Keypoints | v12 | taught | Note 227 (point features, Harris and Shi-Tomasi corners, FAST) |
| SIFT | v13 | taught | Note 228 (scale-space blobs, SIFT, ORB binary descriptors) |
| Binary Features | v14 | taught | Note 228 (scale-space blobs, SIFT, ORB binary descriptors) |
| Visual Features Part 2: Features Descriptors | v15 | taught | Note 228 (scale-space blobs, SIFT, ORB binary descriptors) |
| Image Segmentation using Mean Shift | v16 | add | **mean_shift**: ML clustering chapter, new Note after ML-126 (DBSCAN) |
| Introduction to Classification | v17 | taught | ML-003 (types of ML: classification); ML-085 (kNN); ML-091 (decision trees) |
| Classification - Ensemble Methods | v18 | taught | ML-095 (ensemble learning); ML-102 (random forest) |
| Neural networks | v19,v20 | taught | DL-008, DL-010 (multi-layer perceptron, forward propagation) |
| Gradient Descent | v21 | taught | ML-056 (gradient descent); DL-020 |
| Backpropagation | v22 | taught | DL-015 to DL-017 (backpropagation) |
| Training neural networks | v23 | taught | DL-020 (gradient descent in neural networks); DL-021 |
| Convolutional neural networks | v24,v25 | taught | DL-040 (CNN intuition), DL-042 |
| Least Squares | v26 | taught | ML-053 (normal equation); plan §4 'Nonlinear least squares (Gauss-Newton)' |
| Some Math Basics often used in Photogrammetry | v27 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Homogeneous Coordinates | v28,v29 | taught | plan §4 'Rigid-body transforms and homogeneous coordinates' and 'Projective homogeneous coordinates'; Note 88 |
| Camera extrinsic parameters | v30,v32 | taught | Note 88 (intrinsics K, extrinsics) |
| Camera intrinsic parameters | v30,v32 | taught | Note 88 (intrinsics K, extrinsics) |
| Mapping the 3D world to an image | v31 | taught | Note 88 (pinhole camera, camera matrix P = K[R\|t]) |
| Direct linear transform (DLT) | v33,v34 | taught | Note 89 (checkerboard calibration, DLT; Zhang 2000) |
| Camera calibration | v34 | taught | Note 89 (checkerboard calibration, DLT; Zhang 2000) |
| Camera localization (pose from known points) | v34 | taught | Note 233 (PnP: camera pose from known 3D points) |
| Camera Calibration using Zhang's Method | v35,v36 | taught | Note 89 (checkerboard calibration, DLT; Zhang 2000) |
| Projective 3-point algorithm (P3P, Grunert) | v37,v38 | taught | Note 233 (PnP: camera pose from known 3D points) |
| Photogrammetry I Course - Thank you for your Attention | v39 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Photogrammetry II Course - Welcome | v40 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Fundamental matrix | v41,v42 | taught | Note 232 (epipolar geometry, E and F, normalised 8-point) |
| Essential matrix | v41,v42 | taught | Note 232 (epipolar geometry, E and F, normalised 8-point) |
| Relative orientation | v42 | taught | Note 233 (recovering R and t from E); Note 235 (iterative refinement) |
| Epipolar Geometry Basics | v43 | taught | Note 232 (epipolar geometry, E and F, normalised 8-point) |
| 8-point algorithm | v44,v45 | taught | Note 232 (epipolar geometry, E and F, normalised 8-point) |
| Iterative Solution for Estimating the Relative Orientation | v46 | taught | Note 233 (recovering R and t from E); Note 235 (iterative refinement) |
| RANSAC | v47,v48 | taught | Note 229 (RANSAC) |
| Stereo Normal Case | v49 | taught | Note 90 (stereo camera model, disparity, dense matching along rows) |
| Triangulation for Image Pairs | v50 | taught | Note 233 (triangulation); Note 90 (depth from disparity) |
| Absolute orientation | v51,v52 | taught | Note 92 (aligning two 3D point sets by SVD/Kabsch; a scale factor is the only extra for a similarity) |
| Similarity transformation between point sets | v52 | taught | Note 92 (aligning two 3D point sets by SVD/Kabsch; a scale factor is the only extra for a similarity) |
| Bundle adjustment | v53,v54 | taught | Note 235 (bundle adjustment, Schur complement, Levenberg-Marquardt) |
| The Numerics of Bundle Adjustment | v55 | taught | Note 235 (bundle adjustment, Schur complement, Levenberg-Marquardt) |
| Orthophotos | v56,v57 | out-of-scope | aerial-mapping product of photogrammetry/surveying, a different field; no robot Note makes orthophotos |
| Bag of visual words | v58,v60 | taught | Note 236 (visual place recognition with bag of words) |
| k-means Clustering | v59 | taught | ML-122 (k-means) |
| Bayes Filter | v61,v62 | taught | Note 78 (The Bayes filter: predict, then update) |
| Kalman filter | v63,v64 | taught | Note 80 (Kalman filter) |
| Extended Kalman filter (EKF) | v64 | taught | Note 81 (Extended Kalman filter) |
| Introduction to SLAM | v65,v66 | taught | Note 100 (The SLAM problem) |
| EKF SLAM | v67 | taught | Note 261 (EKF SLAM) |
| Photogrammetry II Course - Thank You for Your Attention | v68 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |

## Stachniss lab (Uni Bonn): Robot Control Lecture 2025

Videos: 6. Course page: https://www.ipb.uni-bonn.de/teaching/index.html

- https://www.youtube.com/playlist?list=PLgnQpQtFTOGT_BlLxVnsuI-7CEQCgNuk4

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| Dynamic systems basics | v1 | taught | plan §4 'State-space models' and 'Stability of dynamical systems' |
| Control theory basics | v2 | add | **control_basics**: RO-06, new opening Note before Note 117 (PD and PID control) |
| Wheeled mobile robot kinematic models | v3 | taught | Note 64 (differential drive, simple car); Note 66 (unicycle, omnidirectional) |
| Wheeled mobile robot control problems | v3 | taught | Note 120 (point, line, pose); Note 121 (path following vs trajectory tracking) |
| PID Control | v4 | taught | Note 117 (PD and PID control) |
| Digital Control Systems | v5 | add | **digital_control**: RO-06, new Note after Note 119; z-transform as a short section in the Laplace MA Note |
| Model predictive control (MPC) | v6 | taught | Note 207 (receding horizon, constraints, QP) |

## Lynch (Northwestern): Modern Robotics, All Videos

Videos: 97. Course page: https://hades.mech.northwestern.edu/index.php/Modern_Robotics_Videos

- https://www.youtube.com/playlist?list=PLggLP4f-rq02vX0OQQ5vrCxbJrzamYDfx

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| Introduction to the Lightboard | v1 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Videos Acknowledgments (Kevin Lynch) | v2 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Foundations of Robot Motion | v3 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Degrees of Freedom of a Rigid Body | v4 | taught | Note 72 (C-space and degrees of freedom; C-space shapes in plain words) |
| Degrees of Freedom of a Robot | v5 | taught | Note 72 (C-space and degrees of freedom; C-space shapes in plain words) |
| Configuration Space Topology | v6 | taught | Note 72 (C-space and degrees of freedom; C-space shapes in plain words) |
| Configuration Space Representation | v7 | taught | Note 72 (C-space and degrees of freedom; C-space shapes in plain words) |
| Configuration and Velocity Constraints | v8 | taught | Note 64 (holonomic vs nonholonomic constraints) |
| Task Space and Workspace | v9 | taught | Note 276 (task space and workspace) |
| Introduction to Rigid-Body Motions | v10 | taught | plan §4 'Rigid-body transforms and homogeneous coordinates'; Note 65 (frames) |
| Rotation Matrices | v11,v12 | taught | Note 65 (rotation matrix read as a frame); plan §4 '3D rotations' |
| Angular Velocities | v13 | taught | Note 84 (angular velocity as a vector along the spin axis) |
| Exponential Coordinates of Rotation | v14,v15 | taught | plan §4 'Axis-angle, exponential and log maps of rotations' |
| Homogeneous Transformation Matrices | v16 | taught | plan §4 'Rigid-body transforms and homogeneous coordinates'; Note 65 (frames) |
| Twists | v17,v18 | taught | Note 275 (twists, screw axis and exponential coordinates, wrenches) |
| Exponential Coordinates of Rigid-Body Motion | v19 | taught | Note 275 (twists, screw axis and exponential coordinates, wrenches) |
| Wrenches | v20 | taught | Note 275 (twists, screw axis and exponential coordinates, wrenches) |
| Product of Exponentials Formula in the Space Frame | v21 | taught | Note 276 (product of exponentials, base and hand frame) |
| Product of Exponentials Formula in the End-Effector Frame | v22 | taught | Note 276 (product of exponentials, base and hand frame) |
| Forward Kinematics Example | v23 | taught | Note 276 (product of exponentials, base and hand frame) |
| Velocity Kinematics and Statics | v24 | taught | Note 277 (manipulator Jacobian, space and body forms; statics) |
| Space Jacobian | v25 | taught | Note 277 (manipulator Jacobian, space and body forms; statics) |
| Body Jacobian | v26 | taught | Note 277 (manipulator Jacobian, space and body forms; statics) |
| Statics of Open Chains | v27 | taught | Note 277 (manipulator Jacobian, space and body forms; statics) |
| Singularities | v28 | taught | Note 278 (singularities, manipulability) |
| Manipulability | v29 | taught | Note 278 (singularities, manipulability) |
| Inverse Kinematics of Open Chains | v30 | taught | Note 279 (analytic and numerical IK) |
| Numerical Inverse Kinematics | v31,v32 | taught | Note 279 (analytic and numerical IK) |
| Kinematics of Closed Chains | v33 | out-of-scope | plan §7 drops closed chains (ME-035): no navigation, legged, humanoid or RL Note uses them |
| Lagrangian Formulation of Dynamics | v34,v35 | taught | Note 281 (Lagrangian mechanics, manipulator equation, mass matrix) |
| Understanding the Mass Matrix | v36 | taught | Note 281 (Lagrangian mechanics, manipulator equation, mass matrix) |
| Dynamics of a Single Rigid Body | v37,v38 | taught | Note 220 (rigid-body dynamics in 3D) |
| Newton-Euler Inverse Dynamics | v39 | taught | Note 282 (inverse and forward dynamics) |
| Forward Dynamics of Open Chains | v40 | taught | Note 282 (inverse and forward dynamics) |
| Dynamics in the Task Space | v41 | taught | Note 285 (dynamics in task space) |
| Constrained Dynamics | v42 | taught | Note 289 (constrained dynamics) |
| Actuation | v43 | taught | Note 283 (motors, gearing, friction) |
| Gearing | v43 | taught | Note 283 (motors, gearing, friction) |
| Friction in actuators | v43 | taught | Note 283 (motors, gearing, friction) |
| Point-to-point trajectories | v44,v45 | taught | Note 201 (time scaling and polynomial trajectories) |
| Time scaling | v44,v45 | taught | Note 201 (time scaling and polynomial trajectories) |
| Polynomial Via Point Trajectories | v46 | taught | Note 202 (via points and splines) |
| Time-Optimal Time Scaling | v47,v48,v49 | taught | Note 203 (time-optimal time scaling) |
| Overview of Motion Planning | v50 | taught | Note 72 (basic motion planning problem) |
| C-Space Obstacles | v51 | taught | Note 73 (obstacles in C-space) |
| Graphs and Trees | v52 | taught | Note 103 (graphs) |
| Graph Search | v53 | taught | Notes 103-105 (BFS/DFS, Dijkstra, A*) |
| Complete Path Planners | v54 | taught | Note 270 (exact roadmaps); Note 111 (complete vs probabilistically complete) |
| Grid Methods for Motion Planning | v55 | taught | Note 106 (grid path planning) |
| Sampling Methods for Motion Planning | v56,v57 | taught | Note 110 (RRT); Note 111 (PRM) |
| Virtual Potential Fields | v58 | taught | Note 109 (potential fields) |
| Nonlinear Optimization | v59 | taught | Note 116 (trajectory optimisation) |
| Control System Overview | v60 | taught | Note 119 (motion vs force control, MR 11.1) |
| Error Response | v61 | taught | Note 118 (error dynamics, step response, second-order systems) |
| Linear Error Dynamics | v62 | taught | Note 118 (error dynamics, step response, second-order systems) |
| First-Order Error Dynamics | v63 | add | **first_order_systems**: RO-06, section of Note 118 (step response), before second-order systems |
| Second-Order Error Dynamics | v64 | taught | Note 118 (error dynamics, step response, second-order systems) |
| Motion Control with Velocity Inputs | v65,v66,v67 | taught | Note 284 (velocity inputs, PD plus gravity, computed torque) |
| Motion Control with Torque or Force Inputs | v68,v69,v70 | taught | Note 284 (velocity inputs, PD plus gravity, computed torque) |
| Force Control | v71 | taught | Note 286 (force control and hybrid motion-force control) |
| Hybrid Motion-Force Control | v72 | taught | Note 286 (force control and hybrid motion-force control) |
| Grasping and Manipulation | v73 | taught | Note 290 (form closure, force closure, grasp matrix) |
| First-Order Analysis of a Single Contact | v74 | taught | Note 288 (contact kinematics, contact types, friction cone) |
| Contact types: rolling, sliding, breaking | v75 | taught | Note 288 (contact kinematics, contact types, friction cone) |
| Multiple Contacts | v76 | taught | Note 290 (form closure, force closure, grasp matrix) |
| Planar Graphical Methods | v77,v78,v81 | out-of-scope | Modern Robotics' hand-drawing technique for planar contacts (book-specific method); closure is taught in Note 290 |
| Form Closure | v79 | taught | Note 290 (form closure, force closure, grasp matrix) |
| Friction | v80 | taught | Note 288 (contact kinematics, contact types, friction cone) |
| Force Closure | v82 | taught | Note 290 (form closure, force closure, grasp matrix) |
| Duality of Force and Motion Freedoms | v83 | taught | Note 286 (natural and artificial constraints) |
| Manipulation and the Meter-Stick Trick | v84 | out-of-scope | worked example / demonstration, no new concept (MR 12.3) |
| Transport of an Assembly | v85 | out-of-scope | worked example / demonstration, no new concept (MR 12.3) |
| Wheeled Mobile Robots | v86 | taught | Note 66 (wheel types, omnidirectional bases) |
| Omnidirectional Wheeled Mobile Robots | v87,v88 | taught | Note 66 (wheel types, omnidirectional bases) |
| Modeling of Nonholonomic Wheeled Mobile Robots | v89 | taught | Note 64 (nonholonomic constraint, differential drive, car) |
| Controllability of Wheeled Mobile Robots | v90,v91,v92,v93 | taught | Note 67 (controllability of a car in plain words) |
| Motion Planning for Nonholonomic Mobile Robots | v94 | taught | Note 112 (Dubins and Reeds-Shepp paths) |
| Feedback Control for Nonholonomic Mobile Robots | v95 | taught | Note 124 (Kanayama tracker) |
| Odometry | v96 | taught | Note 68 (odometry motion model, wheel odometry) |
| Mobile Manipulation | v97 | taught | Note 334 (mobile manipulation) |

## Tedrake (MIT): 6.8210 Underactuated Robotics, Spring 2024

Videos: 24. Course page: https://underactuated.csail.mit.edu/Spring2024/index.html

- https://www.youtube.com/playlist?list=PLkx8KyIQkMfU5szP43GlE_S1QGSPQfL9s

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| Robot dynamics | v1 | taught | Note 281 (Lagrangian mechanics, manipulator equation, mass matrix) |
| Model-based control | v1 | taught | Note 284 (velocity inputs, PD plus gravity, computed torque) |
| Nonlinear Dynamics | v2 | taught | plan §4 'State-space models' (nonlinear systems, phase space) and 'Stability of dynamical systems' |
| Dynamic Programming I | v3 | taught | Note 14 (value iteration); Note 106 (DP with interpolation on continuous spaces); Note 205 (HJB) |
| Dynamic Programming II | v4 | taught | Note 14 (value iteration); Note 106 (DP with interpolation on continuous spaces); Note 205 (HJB) |
| Acrobot | v5 | add | **underactuated_systems**: RO-15, new Note after Note 205 (LQR); the RL cart-pole benchmark can point to it |
| Cart-pole | v5 | add | **underactuated_systems**: RO-15, new Note after Note 205 (LQR); the RL cart-pole benchmark can point to it |
| Quadrotor | v5 | taught | Note 221 (the quadrotor model) |
| Dynamic Programming III | v6 | taught | Note 14 (value iteration); Note 106 (DP with interpolation on continuous spaces); Note 205 (HJB) |
| Lyapunov Analysis I | v7 | taught | Note 199 (stability certificates with Lyapunov functions); plan §4 'Stability of dynamical systems' |
| Computing Lyapunov Functions I | v8 | out-of-scope | sums-of-squares optimisation, research-level; Lyapunov functions themselves are Note 199 |
| Computing Lyapunov Functions II | v9 | out-of-scope | sums-of-squares optimisation, research-level; Lyapunov functions themselves are Note 199 |
| Trajectory Optimization I | v10 | taught | Note 116 (trajectory optimisation) |
| Trajectory Optimization II | v11 | taught | Note 116 (trajectory optimisation) |
| Trajectory Stabilization | v12 | taught | Note 206 (time-varying LQR to hold a robot on a planned trajectory) |
| Simple Models of Walking | v13 | taught | Note 299 (SLIP, passive walkers); Note 296 (linear inverted pendulum) |
| Hybrid Trajectory Optimization | v14 | taught | Note 289 (contact as a hybrid system; contact scheduling vs contact-implicit planning) |
| Planning through contact | v15 | taught | Note 289 (contact as a hybrid system; contact scheduling vs contact-implicit planning) |
| Control through contact | v15 | taught | Note 302 (convex MPC with foot forces) |
| Humanoid Robots | v16 | taught | Note 304 (whole-body motion generation and control for humanoids); RB-06 |
| Mixed-integer (combinatorial + continuous) optimization | v17 | add | **mixed_integer**: MA 07-optimisation, short section after MA-068; first user Note 306 (multi-contact planning) |
| Sampling-based (kinodynamic) motion planning | v18 | taught | Note 112 (kinodynamic planning, kinodynamic RRT) |
| Stochastic dynamics | v19 | taught | Note 68 (motion as a distribution); Note 77 (state transition probabilities) |
| Stochastic Control | v20 | taught | Note 14 (value iteration with nature: stochastic outcomes) |
| Robust control | v21 | out-of-scope | plan §7 drops robust (H-infinity) control (ME-069); worst-case training is taught as robust RL in Note 141 |
| Policy search | v21 | taught | Note 29 (value-function methods vs policy search); Note 43 (black-box policy search) |
| Output feedback | v22 | add | **observers_lqg**: RO-15, new Note after Note 205 (LQR) |
| Feedback motion planning | v23 | taught | Note 106 (feedback planning by DP); Note 9 (feedback plan as a policy) |
| Imitation learning | v24 | taught | Note 165 (behaviour cloning, compounding error, DAgger) |
| Foundation models for robotics | v24 | taught | Note 349 (vision-language-action models and generalist robot policies) |
| Course wrap-up | v24 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |

## Levine (UC Berkeley): CS 285 Deep RL, Fall 2023

Videos: 99. Course page: https://rail.eecs.berkeley.edu/deeprlcourse-fa23/

- https://www.youtube.com/playlist?list=PL_iWQOsE6TfVYGEGiAOMaOzzv41Jfm_Ps

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| Introduction and course overview | v1,v2,v3 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Imitation learning (supervised learning of behaviors) | v4,v5,v6,v7,v8 | taught | Note 165 (behaviour cloning, compounding error, DAgger) |
| Introduction to reinforcement learning | v9,v10,v11,v12,v13,v14 | taught | Note 1 (the RL problem); Note 7 (MDPs) |
| Policy gradients | v15,v16,v17,v18,v19,v20 | taught | Note 30 (policy gradient theorem and REINFORCE) |
| Actor-critic algorithms | v21,v22,v23,v24,v25 | taught | Note 32 (actor-critic) |
| Value function methods | v26,v27,v28,v29 | taught | Note 14 (value iteration); Note 21 (Q-learning); Note 25 (value prediction as supervised learning) |
| Deep RL with Q-functions | v30,v31,v32,v33,v34,v35 | taught | Note 35 (DQN); Note 36 (replay, target networks) |
| Advanced policy gradients | v36,v37,v38,v39 | taught | Note 38 (TRPO, natural gradient); Note 39 (PPO) |
| Optimal control and planning | v40,v41,v42,v43,v44 | taught | Note 116 (trajectory optimisation) |
| Model-based reinforcement learning | v45,v46,v47,v48,v49 | taught | Note 49 (model-based RL with learned dynamics) |
| Model-based policy learning | v50,v51,v52,v53 | taught | Note 45 (Dyna); Note 50 (world models and imagined rollouts) |
| Exploration (part 1) | v54,v55,v56,v57,v58,v59 | taught | Note 4 (optimistic starts, UCB); Note 182 (curiosity and intrinsic rewards) |
| Exploration (part 2) | v60,v61,v62,v63 | taught | Note 182 (intrinsic rewards); Note 315 (unsupervised skill discovery) |
| Offline reinforcement learning | v64,v65,v66,v67,v68,v69,v70 | taught | Note 343 (offline RL and distribution shift); Note 344 (CQL) |
| Reinforcement learning theory basics | v71,v72 | out-of-scope | sample-complexity and error-bound analysis (proof technique) |
| Variational inference and generative models | v73,v74,v75,v76 | taught | plan §4 'Variational autoencoder' (DL new chapter: reconstruction + KL, reparameterization) |
| Control as inference | v77,v78,v79,v80,v81 | out-of-scope | a probabilistic derivation of maximum-entropy RL (proof technique); the algorithm is taught in Note 42 (SAC) |
| Inverse reinforcement learning | v82,v83,v84,v85 | taught | Note 189 (inverse RL) |
| Eric Mitchell: Reinforcement Learning from Human Feedback: Algorithms & Applications | v86 | taught | Note 58 (RLHF with PPO and a KL penalty); guest talk |
| Andrea Zanette: Towards a Statistical Foundation for Reinforcement Learning | v87 | index-noise | guest research talk named after the speaker, not a course topic |
| RL with sequence models and language models | v88,v89,v90 | taught | Note 346 (Decision Transformer); Notes 57-62 (RL for language models) |
| Transfer learning and meta-learning | v91,v92,v93,v94,v95 | taught | Note 171 (multi-task and meta-RL); Note 137 (sim-to-real transfer) |
| Challenges and open problems | v96,v97 | taught | Note 132 (why robot RL is hard); its Sources cite CS285 2023 L23 |
| Guest Lecture: Aviral Kumar | v98 | index-noise | guest research talk named after the speaker, not a course topic |
| Guest Lecture: Dorsa Sadigh | v99 | index-noise | guest research talk named after the speaker, not a course topic |

## Khatib (Stanford): CS223A Introduction to Robotics (replaces ETH Robot Dynamics)

Videos: 16. Course page: https://see.stanford.edu/Course/CS223A

- https://www.youtube.com/playlist?list=PL65CC0384A1798ADF

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| Course overview | v1 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Kinematics | v2 | taught | Note 69 (kinematic chains, forward kinematics, Denavit-Hartenberg) |
| Spatial descriptions | v3 | taught | plan §4 'Rigid-body transforms and homogeneous coordinates'; Note 65 (frames) |
| Manipulator kinematics | v4 | taught | Note 69 (kinematic chains, forward kinematics, Denavit-Hartenberg) |
| Frame attachment | v5 | taught | Note 69 (kinematic chains, forward kinematics, Denavit-Hartenberg) |
| Instantaneous kinematics | v6 | taught | Note 277 (manipulator Jacobian, space and body forms; statics) |
| Jacobian | v6,v7,v8 | taught | Note 277 (manipulator Jacobian, space and body forms; statics) |
| Kinematic singularity | v8 | taught | Note 278 (singularities, manipulability) |
| Perception and sensing in robotic mobility and manipulation | v9 | index-noise | guest lecture survey (Hager); its topics are taught in RO-03 and RO-18 |
| Trajectory generation | v10 | taught | Note 201 (time scaling and polynomial trajectories) |
| Dynamics | v11,v12 | taught | Note 281 (Lagrangian mechanics, manipulator equation, mass matrix) |
| Robot control | v13 | taught | Note 284 (velocity inputs, PD plus gravity, computed torque) |
| Robot control of a one-degree-of-freedom system | v14 | taught | Note 117 (basic PD/PID on a single axis) |
| Control | v15 | taught | Note 284 (velocity inputs, PD plus gravity, computed torque) |
| Compliance / compliant motion | v16 | taught | Note 287 (impedance and admittance control) |
| Force control | v16 | taught | Note 286 (force control and hybrid motion-force control) |

## Nayar (Columbia): First Principles of Computer Vision (12 module playlists)

Videos: 145. Course page: https://fpcv.cs.columbia.edu/

- https://www.youtube.com/playlist?list=PL2zRqk16wsdoz4eycyq7EmeV2KpE6JN76
- https://www.youtube.com/playlist?list=PL2zRqk16wsdr9X5rgF-d0pkzPdkHZ4KiT
- https://www.youtube.com/playlist?list=PL2zRqk16wsdorCSZ5GWZQr1EMWXs2TDeu
- https://www.youtube.com/playlist?list=PL2zRqk16wsdqXEMpHrc4Qnb5rA1Cylrhx
- https://www.youtube.com/playlist?list=PL2zRqk16wsdp8KbDfHKvPYNGF2L-zQASc
- https://www.youtube.com/playlist?list=PL2zRqk16wsdoCCLpou-dGo7QQNks1Ppzo
- https://www.youtube.com/playlist?list=PL2zRqk16wsdpyQNZ6WFlGQtDICpzzQ925
- https://www.youtube.com/playlist?list=PL2zRqk16wsdowTcMVNhV0-7RjSOBS4rHO
- https://www.youtube.com/playlist?list=PL2zRqk16wsdoYzrWStffqBAoUY8XdvatV
- https://www.youtube.com/playlist?list=PL2zRqk16wsdop2EatuowXBX5C-r2FdyNt
- https://www.youtube.com/playlist?list=PL2zRqk16wsdoKHr5sfK1qqsJTDMl_MBs2
- https://www.youtube.com/playlist?list=PL2zRqk16wsdo3VJmrusPU6xXHk37RuKzi

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| Introduction: Overview | v1 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| What is Computer Vision? | v2 | index-noise | introductory lecture; its topics are separate rows |
| What is Vision Used For? | v3 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| How Do Humans Do It? | v4 | out-of-scope | biology / human perception, a different field |
| Topics Covered | v5 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| About the Lecture Series | v6 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| References and Credits | v7 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Image Formation: Overview | v8 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Pinhole camera | v9 | taught | Note 88 (pinhole camera, camera matrix P = K[R\|t]) |
| Perspective projection | v9 | taught | Note 88 (pinhole camera, camera matrix P = K[R\|t]) |
| Image Formation using Lenses | v10 | add | **lens_basics**: RO-03, section of Note 88 |
| Depth of Field | v11 | add | **lens_basics**: RO-03, section of Note 88 |
| Lens Related Issues | v12 | taught | Note 89 (lens distortion; fisheye and spherical models) |
| Wide Angle Cameras | v13 | taught | Note 89 (lens distortion; fisheye and spherical models) |
| Animal Eyes | v14 | out-of-scope | biology / human perception, a different field |
| Image Sensing: Overview | v15 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| A Brief History of Imaging | v16 | out-of-scope | history |
| Types of Image Sensors | v17 | add | **image_sensor**: RO-03, section of Note 88 (pinhole camera) or a short Note after it |
| Image sensor resolution | v18 | add | **image_sensor**: RO-03, section of Note 88 (pinhole camera) or a short Note after it |
| Image noise | v18 | add | **image_sensor**: RO-03, section of Note 88 (pinhole camera) or a short Note after it |
| Dynamic range | v18 | add | **image_sensor**: RO-03, section of Note 88 (pinhole camera) or a short Note after it |
| Sensing Color | v19 | add | **image_sensor**: RO-03, section of Note 88 (pinhole camera) or a short Note after it |
| Camera response function | v20 | add | **image_sensor**: RO-03, section of Note 88 (pinhole camera) or a short Note after it |
| HDR imaging | v20 | add | **image_sensor**: RO-03, section of Note 88 (pinhole camera) or a short Note after it |
| Nature's Image Sensors | v21 | out-of-scope | biology / human perception, a different field |
| Binary Images: Overview | v22 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Geometric Properties | v23 | add | **binary_images**: RO-18, new Note after the point-operators Note |
| Segmenting Binary Images | v24 | add | **binary_images**: RO-18, new Note after the point-operators Note |
| Iterative Modification | v25 | add | **binary_images**: RO-18, new Note after the point-operators Note |
| Image Processing I: Overview | v26 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Pixel Processing | v27 | add | **img_histogram**: RO-18, new first Note before Note 227 |
| Linear shift-invariant systems | v28 | add | **lti_systems**: new MA Note in 06-calculus, with the Fourier Note; DL-042 recaps it for images |
| Convolution | v28 | taught | DL-042 (convolution operation) |
| Linear Image Filters | v29 | taught | Note 227 (image filtering: smoothing and gradient filters) |
| Non-Linear Image Filters | v30 | add | **nonlinear_filters**: RO-18, section of Note 227 |
| Template Matching by Correlation | v31 | add | **template_matching**: RO-18, new section before Note 228 (descriptors and matching) |
| Image Processing II: Overview | v32 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Fourier Transform | v33 | add | **fourier**: new MA Note(s) in 06-calculus, before the frequency-response Note (RO-06) and before Note 227 (image filtering) |
| Convolution Theorem | v34 | add | **fourier**: new MA Note(s) in 06-calculus, before the frequency-response Note (RO-06) and before Note 227 (image filtering) |
| Image Filtering in Frequency Domain | v35 | add | **fourier**: new MA Note(s) in 06-calculus, before the frequency-response Note (RO-06) and before Note 227 (image filtering) |
| Deconvolution | v36 | out-of-scope | image restoration (deblurring), computational photography; no robot Note restores images |
| Sampling Theory and Aliasing | v37 | add | **fourier**: new MA Note(s) in 06-calculus, before the frequency-response Note (RO-06) and before Note 227 (image filtering) |
| Edge Detection: Overview | v38 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| What is an Edge? | v39 | taught | DL-042 (edges as brightness changes, plan §5 recap); Note 227 (gradient filters) |
| Edge detection using gradients | v40 | taught | DL-042 (edges as brightness changes, plan §5 recap); Note 227 (gradient filters) |
| Edge detection using the Laplacian (Laplacian of Gaussian) | v41 | add | **laplacian_log**: RO-18, section of Note 227 (image gradients), before SIFT in Note 228 |
| Canny Edge Detector | v42 | add | **canny**: RO-18, section of Note 227 |
| Corner Detection | v43 | taught | Note 227 (point features, Harris and Shi-Tomasi corners, FAST) |
| Boundary Detection: Overview | v44 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Fitting Lines and Curves | v45 | add | **line_fitting_hough**: RO-18, new Note after Note 227 (also usable on 2D laser scans in RO-03) |
| Active Contours | v46 | out-of-scope | interactive contour fitting (medical imaging, image editing); segmentation in the plan is learned (Note 175) |
| Hough Transform | v47 | add | **line_fitting_hough**: RO-18, new Note after Note 227 (also usable on 2D laser scans in RO-03) |
| Generalized Hough Transform | v48 | out-of-scope | detection of arbitrary template shapes, superseded by learned detectors (Notes 173-174) |
| SIFT Detector: Overview | v49 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| What is an Interest Point? | v50 | taught | Note 227 (point features, Harris and Shi-Tomasi corners, FAST) |
| Detecting Blobs | v51 | taught | Note 228 (scale-space blobs, SIFT, ORB binary descriptors) |
| SIFT Detector | v52 | taught | Note 228 (scale-space blobs, SIFT, ORB binary descriptors) |
| SIFT Descriptor | v53 | taught | Note 228 (scale-space blobs, SIFT, ORB binary descriptors) |
| Image Stitching: Overview | v54 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| 2x2 Image Transformations | v55 | taught | MA-053 (rotation, scaling and shear as matrices; plan §5 recap) |
| 3x3 Image Transformations | v56 | taught | Note 229 (homography between two views of a plane); Note 89 (DLT) |
| Computing Homography | v57 | taught | Note 229 (homography between two views of a plane); Note 89 (DLT) |
| RANSAC | v58 | taught | Note 229 (RANSAC) |
| Image warping | v59 | add | **image_warping**: RO-18, section of Note 229 (RANSAC and homographies) |
| Image blending | v59 | out-of-scope | panorama compositing (computational photography); no robot Note builds panoramas |
| Face Detection: Overview | v60 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Uses of Face Detection | v61 | out-of-scope | classical Viola-Jones face-detector pipeline, superseded by learned detectors (Notes 173-174) |
| Haar Features for Face Detection | v62 | out-of-scope | classical Viola-Jones face-detector pipeline, superseded by learned detectors (Notes 173-174) |
| Integral Image | v63 | out-of-scope | classical Viola-Jones face-detector pipeline, superseded by learned detectors (Notes 173-174) |
| Nearest Neighbor Classifier | v64 | taught | ML-085 (kNN) |
| Support Vector Machine | v65 | taught | ML-086 (SVM) |
| Camera Calibration: Overview | v66 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Linear Camera Model | v67 | taught | Note 88 (pinhole camera, camera matrix P = K[R\|t]) |
| Camera Calibration | v68 | taught | Note 89 (checkerboard calibration, DLT; Zhang 2000) |
| Intrinsic and Extrinsic Matrices | v69 | taught | Note 88 (intrinsics K, extrinsics) |
| Simple Stereo | v70 | taught | Note 90 (stereo camera model, disparity, dense matching along rows) |
| Uncalibrated Stereo: Overview | v71 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Uncalibrated Stereo: Problem of Uncalibrated Stereo | v72 | taught | Note 232 (epipolar geometry, E and F, normalised 8-point) |
| Epipolar Geometry | v73 | taught | Note 232 (epipolar geometry, E and F, normalised 8-point) |
| Stereo Vision in Nature | v74 | out-of-scope | biology / human perception, a different field |
| Estimating Fundamental Matrix | v75 | taught | Note 232 (epipolar geometry, E and F, normalised 8-point) |
| Finding Correspondences | v76 | taught | Note 90 (stereo camera model, disparity, dense matching along rows) |
| Computing Depth | v77 | taught | Note 233 (triangulation); Note 90 (depth from disparity) |
| Radiometry and Reflectance: Overview | v78 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Radiometric Concepts | v79 | add | **radiometry_basics**: RO-18, short section of Note 230 (brightness constancy) or Note 234 (direct methods) |
| Scene radiance | v80 | add | **radiometry_basics**: RO-18, short section of Note 230 (brightness constancy) or Note 234 (direct methods) |
| Image irradiance | v80 | add | **radiometry_basics**: RO-18, short section of Note 230 (brightness constancy) or Note 234 (direct methods) |
| BRDF: Bidirectional Reflectance Distribution Function | v81 | add | **radiometry_basics**: RO-18, short section of Note 230 (brightness constancy) or Note 234 (direct methods) |
| Reflectance Models | v82 | add | **radiometry_basics**: RO-18, short section of Note 230 (brightness constancy) or Note 234 (direct methods) |
| Reflection from Rough Surfaces | v83 | out-of-scope | physics-based reflectance models (graphics/physics-based vision); the plan needs only the Lambertian idea |
| Dichromatic Model | v84 | out-of-scope | physics-based reflectance models (graphics/physics-based vision); the plan needs only the Lambertian idea |
| Photometric Stereo: Overview | v85 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Gradient space | v86 | out-of-scope | shape from shading / photometric stereo need controlled lighting; robots get depth from stereo, structured light and ToF (Notes 90-91) |
| Reflectance map | v86 | out-of-scope | shape from shading / photometric stereo need controlled lighting; robots get depth from stereo, structured light and ToF (Notes 90-91) |
| Photometric Stereo | v87 | out-of-scope | shape from shading / photometric stereo need controlled lighting; robots get depth from stereo, structured light and ToF (Notes 90-91) |
| Lambertian Case | v88 | add | **radiometry_basics**: RO-18, short section of Note 230 (brightness constancy) or Note 234 (direct methods) |
| Calibration Based Photometric Stereo | v89 | out-of-scope | shape from shading / photometric stereo need controlled lighting; robots get depth from stereo, structured light and ToF (Notes 90-91) |
| Shape from Normals | v90 | out-of-scope | shape from shading / photometric stereo need controlled lighting; robots get depth from stereo, structured light and ToF (Notes 90-91) |
| Interreflections | v91 | out-of-scope | physics-based reflectance models (graphics/physics-based vision); the plan needs only the Lambertian idea |
| Shape from Shading: Overview | v92 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Human Perception of Shading | v93 | out-of-scope | biology / human perception, a different field |
| Stereographic Projection | v94 | out-of-scope | shape from shading / photometric stereo need controlled lighting; robots get depth from stereo, structured light and ToF (Notes 90-91) |
| Shape from Shading Algorithm | v95 | out-of-scope | shape from shading / photometric stereo need controlled lighting; robots get depth from stereo, structured light and ToF (Notes 90-91) |
| Shading Illusions | v96 | out-of-scope | biology / human perception, a different field |
| Depth from Defocus: Overview | v97 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Point Spread Function | v98 | out-of-scope | depth from lens blur, a passive cue no robot stack uses; depth sensing is Notes 90-91 |
| Depth from Focus | v99 | out-of-scope | depth from lens blur, a passive cue no robot stack uses; depth sensing is Notes 90-91 |
| Depth from Defocus | v100 | out-of-scope | depth from lens blur, a passive cue no robot stack uses; depth sensing is Notes 90-91 |
| Active Illumination Methods: Overview | v101 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Photometric Stereo Systems | v102 | out-of-scope | shape from shading / photometric stereo need controlled lighting; robots get depth from stereo, structured light and ToF (Notes 90-91) |
| Structured Light Range Finding | v103 | taught | Note 90 (depth cameras: structured light and time of flight) |
| Phase Shifting Method | v104 | taught | Note 90 (depth cameras: structured light and time of flight) |
| Structured Light Systems | v105 | taught | Note 90 (depth cameras: structured light and time of flight) |
| Time of Flight Method | v106 | taught | Note 90 (time of flight); Note 91 (how LiDAR works: time of flight) |
| Optical Flow: Overview | v107 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Motion field | v108 | taught | Note 231 (image motion from camera motion; ego-motion and time-to-contact) |
| Optical flow | v108 | taught | Note 230 (brightness constancy, optical-flow constraint, Lucas-Kanade) |
| Optical Flow Constraint Equation | v109 | taught | Note 230 (brightness constancy, optical-flow constraint, Lucas-Kanade) |
| Lucas-Kanade Method | v110 | taught | Note 230 (brightness constancy, optical-flow constraint, Lucas-Kanade) |
| Coarse-to-Fine Flow Estimation | v111 | taught | Note 230 (pyramidal KLT); Note 227 (image pyramids, coarse-to-fine) |
| Application of Optical Flow | v112 | taught | Note 231 (image motion from camera motion; ego-motion and time-to-contact) |
| Structure from Motion: Overview | v113 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Structure from Motion Problem | v114 | taught | Note 235 (structure from motion) |
| Observation Matrix | v115 | out-of-scope | affine-camera factorisation method; the plan teaches SfM by bundle adjustment (Note 235), which handles perspective cameras |
| Rank of the observation matrix | v116 | out-of-scope | affine-camera factorisation method; the plan teaches SfM by bundle adjustment (Note 235), which handles perspective cameras |
| Tomasi-Kanade Factorization | v117 | out-of-scope | affine-camera factorisation method; the plan teaches SfM by bundle adjustment (Note 235), which handles perspective cameras |
| Object Tracking: Overview | v118 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Change Detection | v119 | out-of-scope | background subtraction needs a static camera; a moving robot uses detection plus tracking (Note 178) |
| Gaussian Mixture Model | v120 | taught | MA-073 (Gaussian mixture models) |
| Object Tracking using Template Matching | v121 | add | **template_matching**: RO-18, new section before Note 228 (descriptors and matching) |
| Tracking by Feature Detection | v122 | taught | Note 230 (pyramidal KLT tracker); Note 178 (tracking by detection) |
| Image Segmentation: Overview | v123 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Segmentation by humans | v124 | out-of-scope | biology / human perception, a different field |
| Segmentation as Clustering | v125 | taught | ML-122 (k-means) |
| k-Means Segmentation | v126 | taught | ML-122 (k-means) |
| Mean-Shift Segmentation | v127 | add | **mean_shift**: ML clustering chapter, new Note after ML-126 (DBSCAN) |
| Graph Based Segmentation | v128 | out-of-scope | classical graph-cut / superpixel segmentation, superseded by learned segmentation (Note 175) |
| Appearance Matching: Overview | v129 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Shape vs. Appearance | v130 | out-of-scope | eigen-appearance object recognition (1990s), superseded by learned features and detectors (Notes 173, 353) |
| Learning Appearance | v131 | out-of-scope | eigen-appearance object recognition (1990s), superseded by learned features and detectors (Notes 173, 353) |
| Principal Component Analysis | v132 | taught | ML-046, ML-047 (PCA) |
| Finding Principal Components | v133 | taught | ML-046, ML-047 (PCA) |
| PCA via SVD | v134 | taught | MA-060 (SVD in machine learning: PCA) |
| Parametric Appearance Representation | v135 | out-of-scope | eigen-appearance object recognition (1990s), superseded by learned features and detectors (Notes 173, 353) |
| Appearance Matching | v136 | out-of-scope | eigen-appearance object recognition (1990s), superseded by learned features and detectors (Notes 173, 353) |
| Neural Networks: Overview | v137 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Perceptron | v138 | taught | DL-004 (perceptron) |
| Perceptron Network | v139 | taught | DL-008, DL-010 (multi-layer perceptron, forward propagation) |
| Activation Function | v140 | taught | DL-027 (activation functions) |
| Neural networks | v141 | taught | DL-008, DL-010 (multi-layer perceptron, forward propagation) |
| Gradient Descent | v142 | taught | ML-056 (gradient descent); DL-020 |
| Backpropagation | v143 | taught | DL-015 to DL-017 (backpropagation) |
| Example Applications | v144 | taught | DL-003 (NN types, history, applications) |
| When to Use Machine Learning? | v145 | taught | ML-001 (what is ML) |

## Brunton (Univ. Washington): Control Bootcamp [secondary]

Videos: 39. Course page: https://www.eigensteve.com/

- https://www.youtube.com/playlist?list=PLMrJAkhIeNNR20Mz-VpzgfQs5zrYi085m

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| Overview | v1 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Linear Systems | v2 | taught | plan §4 'State-space models' and 'Matrix exponential and logarithm' |
| Stability and Eigenvalues | v3 | taught | plan §4 'Stability of dynamical systems' (equilibria, eigenvalues) |
| Linearizing Around a Fixed Point | v4 | taught | Note 206 (linearising a model around an operating point) |
| Controllability | v5 | taught | Note 204 (state feedback, controllability rank test, pole placement) |
| Reachability | v6 | taught | Note 204 (state feedback, controllability rank test, pole placement) |
| Eigenvalue (pole) placement | v6 | taught | Note 204 (state feedback, controllability rank test, pole placement) |
| Controllability and the discrete-time impulse response | v7 | out-of-scope | proof tools for the controllability rank test taught in Note 204 (proof technique) |
| Controllability Gramian | v8 | out-of-scope | quantitative controllability measure (graduate control, model reduction); the rank test in Note 204 is the beginner tool |
| PBH test | v9 | out-of-scope | proof tools for the controllability rank test taught in Note 204 (proof technique) |
| Cayley-Hamilton Theorem | v10 | out-of-scope | proof tools for the controllability rank test taught in Note 204 (proof technique) |
| Reachability via Cayley-Hamilton | v11 | out-of-scope | proof tools for the controllability rank test taught in Note 204 (proof technique) |
| Inverted Pendulum on a Cart | v12 | add | **underactuated_systems**: RO-15, new Note after Note 205 (LQR); the RL cart-pole benchmark can point to it |
| Pole placement | v13 | taught | Note 204 (state feedback, controllability rank test, pole placement) |
| Linear quadratic regulator (LQR) | v14 | taught | Note 205 (LQR) |
| Motivation for Full-State Estimation | v15 | add | **observers_lqg**: RO-15, new Note after Note 205 (LQR) |
| Observability | v16,v19,v20 | taught | Note 80 (Observability, concept only) |
| Full-State Estimation | v17 | add | **observers_lqg**: RO-15, new Note after Note 205 (LQR) |
| Kalman filter | v18,v21 | taught | Note 80 (Kalman filter) |
| Linear quadratic Gaussian (LQG) | v22,v23 | add | **observers_lqg**: RO-15, new Note after Note 205 (LQR) |
| Introduction to Robust Control | v24 | add | **sensitivity_loopshaping**: RO-06, new Note after the frequency-response Note (optional depth) |
| Three representations of linear systems (state space, transfer function, impulse response) | v25 | add | **laplace_tf**: new MA Note in 06-calculus after the planned 'State-space models' Note; RO-06 Note 118 reads step responses from poles |
| Frequency response | v26 | add | **frequency_response**: RO-06, new Note after Note 118 |
| Bode plot | v26 | add | **frequency_response**: RO-06, new Note after Note 118 |
| Spring-mass-damper | v26 | taught | plan §4 'Second-order linear systems' (mass-spring-damper) |
| Laplace transform | v27 | add | **laplace_tf**: new MA Note in 06-calculus after the planned 'State-space models' Note; RO-06 Note 118 reads step responses from poles |
| Transfer function | v27 | add | **laplace_tf**: new MA Note in 06-calculus after the planned 'State-space models' Note; RO-06 Note 118 reads step responses from poles |
| Benefits of feedback (cruise control) | v28,v29 | add | **control_basics**: RO-06, new opening Note before Note 117 (PD and PID control) |
| PI control | v30 | taught | Note 117 (PD and PID control) |
| Sensitivity and complementary sensitivity | v31,v32 | add | **sensitivity_loopshaping**: RO-06, new Note after the frequency-response Note (optional depth) |
| Loop shaping | v33,v34 | add | **sensitivity_loopshaping**: RO-06, new Note after the frequency-response Note (optional depth) |
| Sensitivity and Robustness | v35 | add | **sensitivity_loopshaping**: RO-06, new Note after the frequency-response Note (optional depth) |
| Limitations on Robustness | v36 | add | **sensitivity_loopshaping**: RO-06, new Note after the frequency-response Note (optional depth) |
| Cautionary Tale About Inverting the Plant Dynamics | v37 | add | **nonminimum_phase**: RO-06, section of the frequency-response Note |
| Control systems with non-minimum phase dynamics | v38 | add | **nonminimum_phase**: RO-06, section of the frequency-response Note |
| Model predictive control (MPC) | v39 | taught | Note 207 (receding horizon, constraints, QP) |

## MATLAB Tech Talks (Douglas): Understanding Control Systems [secondary]

Videos: 6. Course page: https://www.mathworks.com/academia/courseware/understanding-control-systems-tech-talks.html

- https://www.youtube.com/playlist?list=PLn8PRpmsu08q8CE0pbZ-cSrMm_WYJfVGd

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| Introduction to Control Systems | v1 | add | **control_basics**: RO-06, new opening Note before Note 117 (PD and PID control) |
| Open-Loop Control Systems | v2 | add | **control_basics**: RO-06, new opening Note before Note 117 (PD and PID control) |
| Feedback Control Systems | v3 | add | **control_basics**: RO-06, new opening Note before Note 117 (PD and PID control) |
| Components of a Feedback Control System | v4 | add | **control_basics**: RO-06, new opening Note before Note 117 (PD and PID control) |
| Simulating Disturbance Rejection in Simulink | v5 | add | **control_basics**: RO-06, new opening Note before Note 117 (PD and PID control) |
| Simulating Robustness to System Variations in Simulink | v6 | add | **sensitivity_loopshaping**: RO-06, new Note after the frequency-response Note (optional depth) |

## MATLAB Tech Talks (Douglas): Understanding PID Control [secondary]

Videos: 7. Course page: https://www.mathworks.com/academia/courseware/pid-control-tech-talks.html

- https://www.youtube.com/playlist?list=PLn8PRpmsu08pQBgjxYFXSsODEF3Jqmm-y

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| What Is PID Control? | v1 | taught | Note 117 (PD and PID control) |
| Anti-windup for PID control | v2 | taught | Note 119 (integrator windup and actuator saturation) |
| Noise Filtering in PID Control | v3 | add | **control_filters**: RO-06, section of Note 119 (feedforward, integral action, cascaded loops) |
| A PID Tuning Guide | v4 | add | **pid_tuning**: RO-06, section of Note 117 (PD and PID control) |
| 3 Ways to Build a Model for Control System Design | v5 | taught | Note 139 (system identification); plan §4 'State-space models' |
| Manual and Automatic PID Tuning Methods | v6 | add | **pid_tuning**: RO-06, section of Note 117 (PD and PID control) |
| Important PID Concepts | v7 | add | **pid_tuning**: RO-06, section of Note 117 (PD and PID control) |

## MATLAB Tech Talks (Douglas): Control Systems in Practice [secondary]

Videos: 15. Course page: https://www.mathworks.com/academia/courseware/control-systems-in-practice-tech-talks.html

- https://www.youtube.com/playlist?list=PLn8PRpmsu08pFBqgd_6Bi7msgkWFKL33b

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| What Control Systems Engineers Do | v1 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| What Is Gain Scheduling? | v2 | taught | Note 255 (gain scheduling) |
| What Is Feedforward Control? | v3 | taught | Note 119 (feedforward plus feedback) |
| Why Time Delay Matters | v4 | taught | Note 136 (delays and control rate) |
| A Better Way to Think About a Notch Filter | v5 | add | **control_filters**: RO-06, section of Note 119 (feedforward, integral action, cascaded loops) |
| What Are Non-Minimum Phase Systems? | v6 | add | **nonminimum_phase**: RO-06, section of the frequency-response Note |
| 4 Ways to Implement a Transfer Function in Code | v7 | add | **digital_control**: RO-06, new Note after Note 119; z-transform as a short section in the Laplace MA Note |
| The Gang of Six in Control Theory | v8 | add | **sensitivity_loopshaping**: RO-06, new Note after the frequency-response Note (optional depth) |
| The Step Response | v9 | taught | Note 118 (error dynamics, step response, second-order systems) |
| Nichols chart | v10 | add | **frequency_response**: RO-06, new Note after Note 118 |
| Nyquist plot | v10 | add | **frequency_response**: RO-06, new Note after Note 118 |
| Bode plot | v10 | add | **frequency_response**: RO-06, new Note after Note 118 |
| Passivity-Based Control to Guarantee Stability | v11 | out-of-scope | energy-based nonlinear stability theory, graduate control; no plan Note builds on it |
| Why Padé Approximations Are Great! | v12 | out-of-scope | a modelling trick for delays inside transfer-function tools; delays are taught in Note 136 |
| What are Transfer Functions? | v13 | add | **laplace_tf**: new MA Note in 06-calculus after the planned 'State-space models' Note; RO-06 Note 118 reads step responses from poles |
| Everything You Need to Know About Control Theory | v14 | index-noise | course intro, outro, module overview or umbrella title; its topics are separate rows |
| Understanding the Z-Transform | v15 | add | **digital_control**: RO-06, new Note after Note 119; z-transform as a short section in the Laplace MA Note |
