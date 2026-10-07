# Gap scope: robot perception and state estimation from sensors

> **Plan of record:** [robotics.md](robotics.md). This doc is evidence: its rows (IDs `PE-NNN`), sources and checks. "Note N" or "RO N" below means the earlier 188-Note draft (2026-10-07), not today's plan.


> **Plan of record:** the RO chapters and Notes are in `docs/books-scope/robotics.md`. This doc lists what that plan is missing in perception: cameras, image geometry, visual motion, depth and LiDAR, inertial sensing and sensor fusion. "RO n" below means planned RO Note n in robotics.md. "new MA (planned)" means a maths Note already listed in robotics.md §3.

**Summary.** This is a scoping list only, not study Notes. Following the owner's change of method, the area was first divided using **nine surveys and tutorials**: SLAM, visual odometry (two parts), visual-inertial odometry, LiDAR odometry, optical flow, deep learning for localization and mapping, object detection, and image segmentation. Their section structure gives the domain map (§0). Rows were then filled from **four textbooks** for teaching depth, plus the original method papers.

How the sources were checked:
- **Surveys.** Each was checked on arXiv (abs page title) or Crossref (DOI lookup). Section headings were read from the arXiv PDF, the authors' official PDF, or the journal PDF on the authors' site.
- **Hartley & Zisserman** (HZ). Section-level contents are from the official contents PDF on the authors' book page.
- **Barfoot**, *State Estimation for Robotics*, 2nd ed. The contents come from the author's free official PDF.
- **Corke**, *Robotics, Vision and Control*, 3rd ed. (RVC3). Chapter titles come from Crossref chapter DOIs. Section titles come from the author's official chapter notebooks on GitHub. Those notebooks only carry the sections that have code, so a few section numbers may be missing.
- **Szeliski**, 2nd ed. Cited at **chapter level only**: chapter titles come from Crossref chapter DOIs. The free PDF sits behind a sign-up form, and the Springer page needs cookies. Neither was used, and no library scan of the 2nd-edition contents could be reached.
- **Not used:** Siegwart et al. The MIT Press page returned 403, and no official contents could be checked.
- **Papers.** Every paper was checked on Crossref or arXiv.

Row counts. There are **117 rows**:
- **covered: 7**
- **partial: 27**
- **new: 83**

By kind:
- **maths: 19**
- **vision: 53**
- **robotics: 43**
- **control: 2**

Almost all of camera geometry, visual motion, LiDAR registration and IMU modelling is new. Most of the estimation side is partial, because RO-09 and RO-22 already plan the filters, pose graphs and SLAM. The DL Notes have CNNs but say outright that detection and segmentation are not covered (DL-001 §"Extra"), so the learned-perception rows are new.

Status key:
- **covered**: already taught or planned. The Note is named.
- **partial**: the basics are there. The new part is named.
- **new**: not in any Note or in robotics.md.

## 0. Domain map from surveys

How the surveys split the area. Every row in §1 names the family it belongs to as its first "Source section" entry, or a textbook section.

| Survey (checked) | How it divides the area | Families used for rows |
|---|---|---|
| Cadena et al. 2016, *Past, Present, and Future of SLAM*, IEEE T-RO, [doi:10.1109/TRO.2016.2624754](https://doi.org/10.1109/TRO.2016.2624754), [arXiv:1606.05830](https://arxiv.org/abs/1606.05830) | §II anatomy: **front-end** (features, data association, loop closure) and **back-end** (MAP estimate over a factor graph). §V metric maps: landmark-based sparse; raw dense (point clouds); boundary and spatial-partitioning (voxels, octrees). §VI semantic maps. §IX new sensors and deep learning | SLAM front-end; SLAM back-end; map representations; semantic maps |
| Scaramuzza & Fraundorfer 2011, *Visual Odometry, Part I*, IEEE RAM, [doi:10.1109/MRA.2011.943233](https://doi.org/10.1109/MRA.2011.943233) ([author PDF](https://rpg.ifi.uzh.ch/docs/VO_Part_I_Scaramuzza.pdf)) | Stereo VO vs monocular VO; VO vs V-SLAM; formulation; camera modelling (perspective, omnidirectional) and calibration; motion estimation from feature matches: 2D-to-2D, 3D-to-3D, 3D-to-2D; triangulation and keyframes | VO-I: camera model, motion estimation, mono vs stereo |
| Fraundorfer & Scaramuzza 2012, *Visual Odometry, Part II*, IEEE RAM, [doi:10.1109/MRA.2012.2182810](https://doi.org/10.1109/MRA.2012.2182810) ([author PDF](https://rpg.ifi.uzh.ch/docs/VO_Part_II_Scaramuzza.pdf)) | Feature detection (corners: Harris, Shi-Tomasi, FAST; blobs: SIFT, SURF); description; matching vs tracking; dense and correspondence-free methods; outlier removal (RANSAC); error propagation; pose-graph and windowed bundle adjustment; loop constraints | VO-II: features, matching, robustness, optimisation |
| Huang 2019, *Visual-Inertial Navigation: A Concise Review*, ICRA, [arXiv:1906.02650](https://arxiv.org/abs/1906.02650) | §2.1 IMU kinematic model; §2.2 camera measurement model; §3.1 filtering vs optimisation; §3.2 tight vs loose coupling; §3.3 VIO vs SLAM; §3.4 direct vs indirect; §3.5 preintegration; §3.6 initialisation; §4 calibration; §5 observability | VIO families |
| Lee et al. 2023, *LiDAR Odometry Survey*, [arXiv:2312.17487](https://arxiv.org/abs/2312.17487) | §2 how LiDAR works; §3 LiDAR-only odometry: **direct matching** (ICP, NDT), **feature-based** (edges and planes), **learned**; §4 LiDAR-inertial, loose vs tight; §6 fusion with other sensors (incl. GNSS); §7 degenerate scenes; §8 datasets and evaluation | LiDAR families |
| Baker et al. 2011, *A Database and Evaluation Methodology for Optical Flow*, IJCV, [doi:10.1007/s11263-010-0390-2](https://doi.org/10.1007/s11263-010-0390-2) ([official PDF](https://vision.middlebury.edu/flow/floweval-ijcv2011.pdf)) | §2 taxonomy: **data term** (brightness constancy, penalty), **prior term** (smoothness), **optimisation** (gradient/variational, coarse-to-fine), discrete methods, learning, occlusion; §4 evaluation (endpoint error) | Optical-flow families |
| Chen et al. 2020, *A Survey on Deep Learning for Localization and Mapping*, [arXiv:2006.12567](https://arxiv.org/abs/2006.12567) | §3 learned odometry (visual, visual-inertial, inertial, LiDAR); §4 mapping (geometric, semantic, general); §5 global localization; §6 SLAM (local/global optimisation, keyframes and loop closure, uncertainty) | Learned localization and mapping |
| Zou et al. 2023, *Object Detection in 20 Years: A Survey*, Proc. IEEE, [arXiv:1905.05055](https://arxiv.org/abs/1905.05055); Minaee et al. 2021, *Image Segmentation Using Deep Learning: A Survey*, [arXiv:2001.05566](https://arxiv.org/abs/2001.05566) | Detection: road map from hand-made detectors to two-stage and one-stage CNN detectors; datasets and metrics; NMS. Segmentation: fully convolutional, encoder-decoder, and more | Learned perception |

The resulting map has four layers:
1. **Sensors and their models:** camera, depth and stereo, LiDAR, IMU, wheels, GNSS.
2. **Front-end:** features and matching, optical flow, two-view geometry, scan registration.
3. **Back-end:** filters (EKF, UKF, complementary), and optimisation (bundle adjustment, factor graphs).
4. **Maps:** sparse landmarks, point clouds, voxels and octrees, elevation maps, semantic maps.

## 1. Topic-by-topic table

### A. Cameras and image formation

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| PE-001 | VO-I camera modelling; HZ 6.1; RVC3 13.1 | Pinhole camera: a 3D point maps to a pixel through a small hole | vision | new | Similar triangles: pixel = focal length × X / Z |
| PE-002 | HZ 2.2, 3.1 | Homogeneous coordinates for points in an image and in 3D | maths | partial | new MA (planned): rigid-body transforms and homogeneous coordinates teaches the extra 1 for poses. New: the projective use, where any multiple of the vector is the same point, and divide-by-last-entry |
| PE-003 | HZ 6.1; RVC3 13.1.4; Barfoot 7.4.1 | Camera matrix P = K [R \| t] | vision | new | One matrix sends a world point to a pixel |
| PE-004 | HZ 6.1; RVC3 13.1.3 | Intrinsics K: focal length, principal point, pixel size | vision | new | What is fixed inside the camera |
| PE-005 | HZ 6.1; RVC3 13.1.2 | Extrinsics: camera pose in the world | vision | partial | RO 50 pose; new: the camera frame convention (z forward) |
| PE-006 | HZ 7.4; RVC3 13.1.6 | Lens distortion: radial and tangential | vision | new | Straight lines bend near the image edge; how to undo it |
| PE-007 | VO-I calibration; RVC3 13.2.2; Zhang 2000 [doi:10.1109/34.888718](https://doi.org/10.1109/34.888718) | Camera calibration with a checkerboard | vision | new | Find K and distortion from photos of a known pattern |
| PE-008 | HZ 4.1, 7.1 | Direct linear transform (DLT): estimate a matrix from point pairs | maths | new | Stack the equations, solve A x = 0 |
| PE-009 | HZ 4.1; MA-058 §6 | Solving A x = 0 with the SVD (last right singular vector) | maths | partial | MA-058 has the null space; new: the least-squares answer when there is noise |
| PE-010 | VO-I omnidirectional; RVC3 13.3 | Wide-angle cameras: fisheye and spherical models | vision | new | Robots often use fisheye lenses; a sphere replaces the flat image |
| PE-011 | RVC3 13.6.1 | Fiducial markers (AprilTag-style) | vision | new | Printed tags that give an exact pose; used for ground truth and docking |
| PE-012 | DL-042 §3, §5 | Image as a grid of numbers; edges as changes in brightness | vision | covered | DL-042 §3, §5 |
| PE-013 | RVC3 11.5.1; DL-042 §6 | Image filtering: smoothing and gradient filters | vision | partial | DL-042 convolution and edge filters; new: Gaussian blur and the x/y image gradient used by features and flow |
| PE-014 | RVC3 11.7.3; Baker 2.3.4 | Image pyramids (coarse-to-fine) | vision | new | The same image at halving sizes; lets features and flow handle large motion |
| PE-015 | Furgale et al. 2013 [doi:10.1109/IROS.2013.6696514](https://doi.org/10.1109/IROS.2013.6696514); Huang §4 | Extrinsic and time calibration between sensors (camera-IMU, camera-LiDAR) | robotics | new | Where each sensor sits on the robot and how their clocks line up |

### B. Features and matching

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| PE-016 | VO-II feature detection; RVC3 12.3 | Point features (keypoints): why corners are easy to find again | vision | new | Flat areas and edges slide; corners do not |
| PE-017 | VO-II; Harris & Stephens 1988 [doi:10.5244/C.2.23](https://doi.org/10.5244/C.2.23) | Harris and Shi-Tomasi corners and the structure tensor | vision | new | A 2×2 matrix of gradients; both eigenvalues large means a corner (MA-056); Shi-Tomasi scores by the smaller one (Shi & Tomasi 1994 [doi:10.1109/CVPR.1994.323794](https://doi.org/10.1109/CVPR.1994.323794)) |
| PE-018 | VO-II; Rosten et al. 2010 [doi:10.1109/TPAMI.2008.275](https://doi.org/10.1109/TPAMI.2008.275) | FAST corner detector | vision | new | A ring-of-pixels test, fast enough for real-time VO |
| PE-019 | VO-II; RVC3 12.3.2; Lowe 2004 [doi:10.1023/B:VISI.0000029664.99615.94](https://doi.org/10.1023/B:VISI.0000029664.99615.94) | Scale-space blobs, descriptors and SIFT | vision | new | Find features at any zoom; a descriptor is a short vector describing the patch; SIFT uses gradient histograms |
| PE-020 | VO-II; Rublee et al. 2011 [doi:10.1109/ICCV.2011.6126544](https://doi.org/10.1109/ICCV.2011.6126544) | ORB: binary descriptors and Hamming distance | vision | new | Bits instead of floats; compared by counting differing bits |
| PE-021 | VO-II feature matching; ML-085 | Matching descriptors (nearest neighbour, ratio test, mutual check) vs tracking | vision | partial | ML-085 nearest neighbours; new: the ratio test, the left-right check, and tracking (search near the old spot) vs matching (search everywhere) |
| PE-022 | VO-II outlier removal; Fischler & Bolles 1981 [doi:10.1145/358669.358692](https://doi.org/10.1145/358669.358692); Barfoot 5.4.1 | RANSAC: fit a model despite wrong matches | maths | new | Try minimal random samples, keep the model most points agree with; number of tries N = log(1-p) / log(1-w^s), from MA-031 (HZ 4.7) |
| PE-023 | HZ 4.1, 4.8, 13; RVC3 13.6.2 | Homography: the map between two views of a plane | vision | new | 3×3 matrix, 4 point pairs, used for floors, walls and image stitching |

### C. Optical flow and image motion

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| PE-024 | Szeliski ch.9; Baker 2.1.1 | Optical flow: the apparent motion of each pixel | vision | new | A 2D arrow per pixel between two frames |
| PE-025 | Baker 2.1.1; Horn & Schunck 1981 [doi:10.1016/0004-3702(81)90024-2](https://doi.org/10.1016/0004-3702(81)90024-2) | Brightness constancy and the optical-flow constraint | vision | new | I_x u + I_y v + I_t = 0: one equation, two unknowns, so through a small window only motion across an edge shows (the aperture problem) |
| PE-026 | Lucas & Kanade 1981 ([IJCAI PDF](https://www.ijcai.org/Proceedings/81-2/Papers/017.pdf)); ML-053 | Lucas-Kanade: local flow by least squares in a window | vision | partial | ML-053 normal equation; new: the 2×2 system, the same structure tensor as Harris |
| PE-027 | Baker 2.3.4; Shi & Tomasi 1994 | Pyramidal KLT tracker | vision | new | LK on a pyramid; the standard sparse tracker in VO |
| PE-028 | Horn & Schunck 1981; Baker 2.2 | Horn-Schunck: dense flow with a smoothness term | vision | new | Data term + smoothness prior, solved for every pixel |
| PE-029 | Chen §3.1; Teed & Deng 2020, RAFT [arXiv:2003.12039](https://arxiv.org/abs/2003.12039) | Learned optical flow | vision | new | A network predicts flow; one overview row, no architecture detail |
| PE-030 | RVC3 15.2.1 | Image motion from camera motion (the image Jacobian) | vision | new | How pixels move when the camera moves and turns; links flow to ego-motion |
| PE-031 | Szeliski ch.9; RVC3 15.2.3 | Ego-motion and time-to-contact from flow | robotics | new | The flow field's centre shows heading; its growth rate warns of collision |

### D. Two-view geometry

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| PE-032 | HZ 9.1; RVC3 14.2 | Epipolar geometry: epipoles, epipolar lines | vision | new | A point in one image must lie on a line in the other |
| PE-033 | MA-050 (named only) | Cross product and its matrix form [t]× | maths | new | MA-050 names the cross product but teaches only the dot product; needed for E = [t]× R and for angular velocity |
| PE-034 | HZ 9.6; RVC3 14.2.2 | Essential matrix E (calibrated cameras) | vision | new | Holds the relative rotation and the direction of travel |
| PE-035 | HZ 9.2; RVC3 14.2.1 | Fundamental matrix F (uncalibrated cameras) | vision | new | F = K'^-T E K^-1; the constraint written in pixels |
| PE-036 | HZ 11.2; RVC3 14.2.3 | Normalised 8-point algorithm | vision | new | Normalise the points (HZ 4.4), solve linearly for F from 8 matches, then force rank 2 with the SVD (MA-059) |
| PE-037 | VO-I 2D-to-2D; Nistér 2004 [doi:10.1109/TPAMI.2004.17](https://doi.org/10.1109/TPAMI.2004.17) | 5-point algorithm (concept only) | vision | new | The fewest matches for calibrated cameras, so RANSAC needs fewer tries; the polynomial solve is left to libraries |
| PE-038 | HZ 9.6.2; VO-I | Recovering R and t from E; the four-solution check | vision | new | Keep the one solution that puts points in front of both cameras |
| PE-039 | VO-I monocular | Scale ambiguity of a single camera | vision | new | One camera cannot tell a small near scene from a big far one |
| PE-040 | HZ 12.2; RVC3 14.3.1; VO-I triangulation | Triangulation | vision | new | Two rays from two cameras meet at the 3D point |
| PE-041 | VO-I 3D-to-2D; RVC3 13.2.4; Lepetit et al. 2009 [doi:10.1007/s11263-008-0152-6](https://doi.org/10.1007/s11263-008-0152-6) | PnP: camera pose from known 3D points (EPnP) | vision | new | Locate the camera against a map |
| PE-042 | HZ 4.2-4.3, 12.3 | Reprojection error | vision | new | Pixel distance between seen and predicted point; the cost everything later minimises |
| PE-043 | VO-I 3D-to-3D; Barfoot 9.1; RVC3 14.7.2 | Aligning two 3D point sets (SVD / Kabsch solution) | maths | new | Best rotation and translation between matched 3D points; shared by stereo VO and ICP |
| PE-044 | HZ 11.12; RVC3 14.4.3 | Image rectification | vision | new | Warp a stereo pair so matches lie on the same row |

### E. Visual odometry, structure from motion and visual SLAM

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| PE-045 | VO-I formulation | Visual odometry: chaining frame-to-frame motions | robotics | new | Pose_k = pose_{k-1} × T_k; keep only keyframes that moved enough |
| PE-046 | VO-I; RO 51 | Drift: why odometry error grows | robotics | partial | RO 51 shows growing uncertainty for wheel odometry; new: drift in VO, and scale drift in monocular VO |
| PE-047 | VO-I mono vs stereo | Monocular vs stereo VO | robotics | new | Stereo gives metric scale at each step; mono needs another cue |
| PE-048 | VO-II dense methods; Huang §3.4; Engel et al. 2018 DSO [doi:10.1109/TPAMI.2017.2658577](https://doi.org/10.1109/TPAMI.2017.2658577) | Direct vs feature-based (indirect) methods: photometric error | vision | new | Compare pixel brightness directly instead of matched features |
| PE-049 | VO-I/II; Szeliski ch.11; RVC3 14.3 | Structure from motion: cameras and points from many photos | vision | new | Offline, unordered images; VO is the online, ordered case |
| PE-050 | HZ 18.1; Barfoot 10.1; VO-II windowed BA | Bundle adjustment | vision | new | Move all cameras and points to cut total reprojection error |
| PE-051 | Barfoot 10.1; RO 165 | Sparsity and the Schur complement in bundle adjustment | maths | partial | new MA (planned): Schur complement; new: the camera-point block structure that makes BA fast |
| PE-052 | HZ 4.5; Barfoot 4.3 | Levenberg-Marquardt | maths | partial | new MA (planned): Gauss-Newton; new: the damping term that blends it with gradient descent (ML-056) |
| PE-053 | Barfoot 5.4; Cadena §III | Robust cost functions (Huber, Cauchy) | maths | partial | ML-051 MAE vs RMSE under outliers; new: losses that grow slowly for big errors inside least squares |
| PE-054 | Cadena §II; VO-I VO vs V-SLAM | VO vs visual SLAM; front-end vs back-end | robotics | partial | RO 69 SLAM problem; new: the front-end/back-end split for cameras |
| PE-055 | Cadena §II; Gálvez-López & Tardós 2012 [doi:10.1109/TRO.2012.2197158](https://doi.org/10.1109/TRO.2012.2197158) | Visual place recognition with bag of words | vision | new | Recognise a revisited place from its word histogram; the trigger for a loop closure |
| PE-056 | VO-II loop constraints; RO 167 | Loop closure for a visual map | robotics | partial | RO 167 loop closure; new: closing visual loops and the scale fix for mono |
| PE-057 | Mur-Artal et al. 2015 [doi:10.1109/TRO.2015.2463671](https://doi.org/10.1109/TRO.2015.2463671); Campos et al. 2021 ORB-SLAM3 [doi:10.1109/TRO.2021.3075644](https://doi.org/10.1109/TRO.2021.3075644) | ORB-SLAM as a worked system: tracking, local mapping, loop closing threads | robotics | new | One complete visual SLAM system, read part by part |
| PE-058 | Cadena §III; Lee §8.2; Geiger et al. 2012 KITTI [doi:10.1109/CVPR.2012.6248074](https://doi.org/10.1109/CVPR.2012.6248074) | Evaluating odometry and SLAM: trajectory error, drift %, benchmarks | robotics | new | ATE/RPE-style error against ground truth |
| PE-059 | Chen §3, §6 | Learned odometry (visual, inertial) and learned SLAM parts | vision | new | One overview row: networks for depth, pose, velocity from IMU windows, or loop detection (Chen §3, §3.3, §6) |

### F. Depth: stereo and depth cameras

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| PE-060 | Barfoot 7.4.2; RVC3 14.4 | Stereo camera model: disparity and depth | vision | new | Depth = focal length × baseline / disparity |
| PE-061 | RVC3 14.4; Szeliski ch.12 | Dense stereo matching along rows | vision | new | Find each pixel's partner on the same row; cost by patch similarity; semi-global matching (Hirschmüller 2008 [doi:10.1109/TPAMI.2007.1166](https://doi.org/10.1109/TPAMI.2007.1166)) smooths it, and most stereo cameras run it |
| PE-062 | RVC3 14.4.2 | Stereo failure modes and depth error growing with distance | vision | new | Blank walls, repeats, and error ∝ depth² |
| PE-063 | Szeliski ch.13; Newcombe et al. 2011 [doi:10.1109/ISMAR.2011.6092378](https://doi.org/10.1109/ISMAR.2011.6092378) | Depth cameras: structured light and time of flight | robotics | new | How RGB-D cameras measure depth, and where they fail (sunlight, glass) |
| PE-064 | RVC3 14.7 | Depth image to point cloud | vision | new | Back-project each pixel with K |
| PE-065 | Chen §4.1; Eigen et al. 2014 [arXiv:1406.2283](https://arxiv.org/abs/1406.2283) | Learned depth from one image (concept) | vision | new | A network guesses depth; useful but scale is uncertain |

### G. LiDAR, point clouds and 3D maps

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| PE-066 | Lee §2; RVC3 6.8 | How LiDAR works: time of flight, spinning vs solid-state, rings | robotics | new | A 3D scan as rings of range points |
| PE-067 | Barfoot 7.4.3; RO 57 | Range-azimuth-elevation sensor model | robotics | partial | RO 57 beam model is 2D; new: 3D range-bearing to x, y, z |
| PE-068 | Cadena §V; Rusu & Cousins 2011 [doi:10.1109/ICRA.2011.5980567](https://doi.org/10.1109/ICRA.2011.5980567) | Point clouds: storage and basic operations | robotics | new | A list of x, y, z points; cropping and transforming |
| PE-069 | Rusu & Cousins 2011 | Voxel-grid downsampling | robotics | new | One point per small cube; cuts millions of points to thousands |
| PE-070 | RVC3 14.7.1 | Normals and plane fitting (incl. ground removal) | maths | partial | MA-060 PCA via SVD; new: the smallest principal direction of a local patch is its normal |
| PE-071 | Lee §3.1 | k-d tree for nearest-neighbour search | maths | partial | ML-085 nearest neighbours by brute force; new: a tree that finds them fast |
| PE-072 | Lee §3.1; Besl & McKay 1992 [doi:10.1109/34.121791](https://doi.org/10.1109/34.121791); Barfoot 9.1 | ICP: iterative closest point | robotics | partial | RO 58 scan matching with likelihood fields; new: match closest points, align with the SVD, repeat |
| PE-073 | Chen & Medioni 1992 [doi:10.1016/0262-8856(92)90066-C](https://doi.org/10.1016/0262-8856(92)90066-C); Segal et al. 2009 [doi:10.15607/RSS.2009.V.021](https://doi.org/10.15607/RSS.2009.V.021) | Point-to-plane ICP and Generalized-ICP | robotics | new | Slide along flat surfaces; faster and more accurate than point-to-point |
| PE-074 | Lee §3.1; Biber & Strasser 2003 [doi:10.1109/IROS.2003.1249285](https://doi.org/10.1109/IROS.2003.1249285) | NDT scan matching | robotics | new | Turn the map into small Gaussians and match a scan to them |
| PE-075 | Lee §3.2; Zhang & Singh 2014 LOAM [doi:10.15607/RSS.2014.X.007](https://doi.org/10.15607/RSS.2014.X.007) | Feature-based LiDAR odometry: edge and plane points | robotics | new | The standard LiDAR odometry design |
| PE-076 | Lee §7.3 | Degenerate scenes: long corridors and open fields | robotics | new | When a scan cannot fix motion in one direction |
| PE-077 | Cadena §V; Hornung et al. 2013 [doi:10.1007/s10514-012-9321-0](https://doi.org/10.1007/s10514-012-9321-0) | 3D occupancy with octrees (OctoMap) | robotics | partial | RO 68 occupancy grid in 2D; new: 3D voxels in a tree so free space costs little |
| PE-078 | Fankhauser et al. 2018 [doi:10.1109/LRA.2018.2849506](https://doi.org/10.1109/LRA.2018.2849506) | Elevation maps for legged robots | robotics | partial | RO 86 and RO 144 use height samples from a map; new: building the robot-centred height map with per-cell variance from depth/LiDAR |
| PE-079 | Newcombe et al. 2011; Cadena §V | Signed-distance (TSDF) maps (concept) | robotics | new | Store distance to the nearest surface per voxel; smooth surfaces from depth cameras |
| PE-080 | Cadena §V | Choosing a map type: landmarks, point clouds, voxels, elevation, meshes | robotics | partial | RO 53 maps and landmarks; new: the 3D options and what each costs |

### H. Inertial, wheel and satellite sensing

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| PE-081 | RVC3 3.4.1; Woodman 2007 ([UCAM-CL-TR-696](https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-696.html)) | Gyroscope: measures turn rate | robotics | new | What a MEMS gyro reads |
| PE-082 | RVC3 3.4; Woodman 2007 | Accelerometer: measures specific force (gravity included) | robotics | new | Why a still IMU reads 9.8 m/s² upward |
| PE-083 | Huang §2.1; Woodman 2007 gyro/accel errors | IMU measurement model: reading = truth + bias + noise | robotics | new | The two error terms every IMU filter models |
| PE-084 | Woodman 2007; Barfoot 5.2 | Bias random walk and bias estimation | robotics | partial | RO 63 Kalman filter; new: bias as a slowly drifting state added to the filter |
| PE-085 | Woodman 2007 | Integration drift: angle error grows with t, position error with t³ for a gyro bias | robotics | new | Why an IMU alone is useless for position after seconds |
| PE-086 | RVC3 3.4.1.2; Barfoot 7.2.4 | Integrating angular velocity into orientation | maths | partial | new MA (planned): 3D rotations and numerical ODE integration; new: the rotation update R_{k+1} = R_k exp([ω dt]×) |
| PE-087 | Barfoot 8.1 | Small rotations: exponential and log maps of SO(3) (beginner level) | maths | new | A rotation vector ↔ rotation matrix; how errors on rotations are written |
| PE-088 | Barfoot 9.4; Woodman 2007 strapdown | Strapdown inertial navigation | robotics | new | Rotate, remove gravity, integrate twice |
| PE-089 | RVC3 6.1; Thrun ch.5 via RO 51 | Wheel odometry from encoders, and wheel slip | robotics | partial | RO 51 odometry motion model; new: detecting slip by checking wheels against the IMU |
| PE-090 | Lee §6; [GPS.gov accuracy page](https://archive.gps.gov/systems/gps/performance/accuracy/) | GNSS/GPS basics: ranging to satellites, ~5 m phone accuracy, multipath and blockage | robotics | new | Global position with no drift but noisy and often missing; RTK and dual-frequency receivers reach centimetres |

### I. Sensor fusion and estimation back-ends

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| PE-091 | RO 63 | Kalman filter | maths | covered | RO 63 |
| PE-092 | RO 64 | Extended Kalman filter | maths | covered | RO 64 |
| PE-093 | RO 158 | Unscented Kalman filter | maths | covered | RO 158 |
| PE-094 | RVC3 3.4.4; Mahony et al. 2008 [doi:10.1109/TAC.2008.923738](https://doi.org/10.1109/TAC.2008.923738) | Complementary filter for attitude | control | new | Trust the gyro for fast changes and the accelerometer for the slow tilt; the simplest fusion |
| PE-095 | Huang §2.1, §3.1 | EKF fusion of IMU, wheels and GNSS (loosely coupled) | robotics | partial | RO 64 EKF; new: IMU as the predict step, other sensors as updates at their own rates |
| PE-096 | Huang §3.2 | Loose vs tight coupling | robotics | new | Fuse finished poses vs fuse raw measurements |
| PE-097 | Barfoot 7.2.5, 8.3 | Error-state (indirect) Kalman filter for rotations | control | new | Filter the small error, not the rotation itself |
| PE-098 | Huang §3.1 | Filtering vs optimisation (sliding window) | robotics | partial | RO 61 and RO 165; new: the trade-off for real-time odometry |
| PE-099 | Dellaert & Kaess 2017 [doi:10.1561/2300000043](https://doi.org/10.1561/2300000043); Cadena §II | Factor graphs (beginner level) | maths | partial | RO 165 pose graphs; new: general factors (IMU, camera, GNSS) as boxes on a graph, MAP = least squares (MA-070) |
| PE-100 | Huang §3.5; Forster et al. 2017 [arXiv:1512.02363](https://arxiv.org/abs/1512.02363) | IMU preintegration | robotics | new | Sum many IMU readings into one factor between keyframes |
| PE-101 | Huang §3.1; Mourikis & Roumeliotis 2007 [doi:10.1109/ROBOT.2007.364024](https://doi.org/10.1109/ROBOT.2007.364024) | Filter-based VIO (MSCKF, concept) | robotics | new | EKF that keeps a window of past camera poses |
| PE-102 | Huang §3.2; Qin et al. 2018 VINS-Mono [doi:10.1109/TRO.2018.2853729](https://doi.org/10.1109/TRO.2018.2853729) | Optimisation-based VIO (VINS-Mono as worked system) | robotics | new | Sliding-window factor graph with preintegrated IMU factors |
| PE-103 | Huang §3.6 | VIO initialisation: gravity, scale and biases | robotics | new | The IMU fixes the monocular scale |
| PE-104 | Huang §5 | Observability (concept only) | maths | new | Which states the sensors can pin down; with VIO, global position and yaw cannot be |
| PE-105 | Lee §4 | LiDAR-inertial odometry (loose and tight) | robotics | new | IMU predicts motion and undistorts each scan (a spinning scan takes about 0.1 s while the robot moves) |
| PE-106 | RO 161 | Data association and Mahalanobis gating | maths | covered | RO 161 with new MA (planned) Mahalanobis distance |
| PE-107 | Barfoot 5.3–5.4; Cadena §III | Outliers in the back-end: robust kernels, switchable constraints (concept) | robotics | partial | Robust losses row in §E; new: rejecting wrong loop closures |
| PE-108 | RO 103 | Learned state estimators for legged robots | robotics | covered | RO 103 |

### J. Learned perception for navigation

DL-001 says detection and segmentation are not covered, and DL-040 and DL-044 only name them. So these rows are new.

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| PE-109 | Zou §II.A road map; RVC3 12.1.4 | Object detection: boxes and class labels | vision | new | The task, and how it differs from classification (DL-040) |
| PE-110 | Zou §II.B | Intersection over union (IoU) and mean average precision (mAP) | vision | partial | ML-076 precision and recall; new: IoU matching and averaging over recall |
| PE-111 | Zou §II.C | Non-maximum suppression | vision | new | Keep the best box, drop overlapping duplicates |
| PE-112 | Zou §II.A; Ren et al. 2015 [arXiv:1506.01497](https://arxiv.org/abs/1506.01497) | Two-stage detectors (Faster R-CNN) | vision | new | Propose regions, then classify them |
| PE-113 | Zou §II.A; Redmon et al. 2016 [arXiv:1506.02640](https://arxiv.org/abs/1506.02640); Liu et al. 2016 SSD [arXiv:1512.02325](https://arxiv.org/abs/1512.02325) | One-stage detectors (YOLO, SSD) | vision | new | One pass over a grid; the real-time choice on robots |
| PE-114 | Minaee §3; Long et al. 2015 [arXiv:1411.4038](https://arxiv.org/abs/1411.4038); RVC3 12.1.1 | Semantic segmentation: a class per pixel (FCN) | vision | new | Road, grass and person masks for where to drive; instance segmentation (Mask R-CNN, He et al. 2017 [arXiv:1703.06870](https://arxiv.org/abs/1703.06870)) gives one mask per object |
| PE-115 | Minaee §3.3; Ronneberger et al. 2015 [arXiv:1505.04597](https://arxiv.org/abs/1505.04597) | Encoder-decoder segmentation (U-Net) | vision | new | Shrink then grow back with skip links; DL-002 names U-Net only |
| PE-116 | Cadena §VI; Chen §4.2 | Semantic maps: putting labels into the 3D map | robotics | new | Project pixel labels onto voxels or grid cells; feeds costmaps and object-goal navigation (RO 111, RO 121) |
| PE-117 | Chen §4.2; Fankhauser 2018 | Traversability from geometry and semantics | robotics | new | Turn slope, step height and class into a drive cost |
| PE-118 | DL-053 | Using pretrained detectors and segmenters | vision | covered | DL-053 transfer learning |

## 2. Prerequisites between the new concepts

```
homogeneous coords (projective) ─┬─> pinhole + K, R, t ─> distortion ─> calibration
rigid-body transforms (planned)  ┘        │
                                          ├─> PnP ───────────────────────────┐
image gradients + pyramids ─> Harris/Shi-Tomasi/FAST ─> descriptors (SIFT, ORB) ─> matching ─> RANSAC
       │                                                                                         │
       └─> brightness constancy ─> Lucas-Kanade ─> KLT tracker                                   │
                     └─> Horn-Schunck                                                            v
cross product [t]x ─> epipolar geometry ─> E, F ─> 8-point / 5-point ─> R,t from E ─> triangulation
                                                                         │
3D point-set alignment (SVD) ─> ICP ─> point-to-plane, NDT, LOAM         v
k-d tree ──────────────────────┘                     visual odometry (mono/stereo, feature/direct)
                                                                         │
reprojection error + Gauss-Newton (planned) ─> Levenberg-Marquardt ─> bundle adjustment ─> visual SLAM (ORB-SLAM)
robust losses ──────────────────────────────────────────┘     place recognition ─┘
stereo disparity ─> depth image ─> point cloud ─> voxel grid ─> OctoMap / elevation map / semantic map
IMU model (bias, noise) ─> integration + SO(3) exp ─> strapdown ─> complementary filter
                                       └─> error-state EKF ─> loose fusion (IMU+wheels+GNSS)
                                       └─> preintegration ─> factor graphs ─> VIO, LiDAR-inertial
```

## 3. Suggested learning order

Navigation starts at RO 106, so a **lean sensing core** should sit just before it. The heavy visual geometry goes into an **optional depth chapter** next to RO-22, matching how robotics.md handles SLAM depth.

1. **Core, after RO-09 (filters) and before RO-15.** Seven to eight Notes:
   - IMU model, bias and integration drift.
   - Complementary filter.
   - EKF fusion of IMU, wheels and GNSS.
   - Pinhole camera, intrinsics, distortion and calibration.
   - Depth cameras and stereo disparity.
   - Depth image to point cloud and voxel grid.
   - LiDAR and ICP.
   - Elevation and 3D occupancy maps.

   RO 86, 111 and 144 then build on real sensor Notes, not just named inputs.
2. **Before RO 144 (perceptive locomotion):** elevation maps and traversability.
3. **Before the visual-navigation and VLA Notes (RO 118, 152, 178):** semantic segmentation, detection, IoU/NMS and semantic maps.
4. **Optional chapter "Visual geometry and odometry", next to RO-22:**
   - Features, then matching and RANSAC, then homography.
   - Optical flow (LK, KLT, Horn-Schunck).
   - Epipolar geometry, then E and F, then triangulation and PnP.
   - Visual odometry (mono and stereo, direct and feature-based).
   - Bundle adjustment.
   - Visual SLAM (ORB-SLAM), place recognition and evaluation.
5. **Optional, after RO 165 (pose graphs):**
   - Factor graphs.
   - IMU preintegration.
   - VIO (MSCKF, VINS-Mono).
   - LiDAR-inertial odometry and deskewing.
   - Degenerate scenes.

## 4. New maths the area needs that MA lacks

Already planned in robotics.md §3, and needed here too:
- rigid-body transforms and homogeneous coordinates
- 3D rotations and quaternions
- nonlinear least squares (Gauss-Newton)
- Schur complement
- Mahalanobis distance
- Cholesky factor
- numerical ODE integration

Not yet planned:

| Concept | What | Where | First needed by |
|---|---|---|---|
| Projective use of homogeneous coordinates | A point is the same under any scaling; divide by the last entry | short section in the planned MA rigid-body transforms Note | Pinhole camera |
| Cross product and its skew-symmetric matrix | a × b as a matrix times b | MA 05-linear-algebra (new Note after MA-050) | Epipolar geometry; angular velocity |
| Least-squares solution of A x = 0 by SVD | Last right singular vector; unit-norm constraint | short section after MA-058 §6, or inside the DLT Note | DLT, 8-point algorithm |
| Point-set alignment by SVD (Kabsch) | Best rotation between matched point sets | MA 05-linear-algebra (new Note) or inside ICP Note | Stereo VO, ICP |
| Levenberg-Marquardt | Damped Gauss-Newton | MA 07-optimisation, section of the planned Gauss-Newton Note | Bundle adjustment |
| Robust loss functions (Huber, Cauchy) and iteratively reweighted least squares | Big errors count less | MA 07-optimisation (new Note) | Bundle adjustment, ICP, SLAM back-end |
| SO(3) exponential and log maps (beginner level) | Rotation vector to and from rotation matrix | MA 05-linear-algebra, after the planned 3D rotations Note | IMU integration, error-state EKF, preintegration |
| k-d trees | Fast nearest-neighbour search | short section inside the ICP Note | ICP |
| Structure tensor | 2×2 matrix of image gradients, read through its eigenvalues (MA-056) | short section inside the Harris Note | Harris, Lucas-Kanade |
