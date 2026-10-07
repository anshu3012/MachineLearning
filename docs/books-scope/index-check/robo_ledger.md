# Index check of the robotics plan: Modern Robotics, Planning Algorithms, Introduction to Autonomous Robots

Agent `robo`. Every index term of each book, with a verdict against `docs/books-scope/robotics.md` (Notes N1-N359 and its §4 planned MA/DL Notes), the eight evidence docs, the MA/ML/DL Notes and `glossary.md`.

Verdicts: **taught** (where = the Note; `plan§4 X` = a new MA Note the plan already lists), **mentioned-only** (counted as add), **add** (where = target chapter; concept in bold), **out-of-scope** (checkable reason), **index-noise**.
Matching: `robo_match.py` (case-insensitive, light stemming, British/American spelling, a few synonyms); every row was then judged by reading the term, the plan Note list and, where unclear, the book text.

## Lynch & Park, *Modern Robotics* (2017 preprint)

Free official PDF: http://hades.mech.northwestern.edu/images/7/7f/MR.pdf (linked from modernrobotics.org). Index pp. 617-624.

Counts: taught 299, mentioned-only 1, add 101, out-of-scope 36, index-noise 34 (total 471).

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| S n | 24 | index-noise | symbol: S^n, n-sphere notation (C-space topology shorthand) |
| R n | 24 | index-noise | symbol: R^n notation |
| acceleration ellipsoid | 280 | add | **acceleration and force ellipsoids** (robotics) → RB-01 (extend N278); MR 8.4 reads arm dynamics/manipulability as ellipsoids; companion of the manipulability ellipsoid already in N278 |
| Ackermann steering | 524 | taught | N67: Ackermann steering geometry |
| actuator | 11, 303 | taught | N283: motors, gearing as actuators |
| Ad | 100 | index-noise | symbol: Ad (adjoint map notation) |
| adjoint map | 100 | taught | N275: adjoint map moves twists between frames |
| admittance | 442 | taught | N287: admittance control |
| ambiguity | 495 | out-of-scope | MR 12.2 grasp 'ambiguity' is a book-specific contact-mode term; unrelated to the camera scale ambiguity (N233) |
| angular velocity | 76 | taught | N84: angular velocity as a vector (also N220) |
| angular velocity, body | 78 | add | **body vs spatial angular velocity** (robotics) → RB-01 (extend N275); MR 3.2.2 expresses angular velocity in body or fixed frame; needed for IMU readings (body frame) and twists |
| angular velocity, spatial | 77 | add | **body vs spatial angular velocity** (robotics) → RB-01 (extend N275); same concept as body angular velocity (MR p.77) |
| apparent inertia | 310 | taught | N285: apparent (task-space) mass Λ = (J M⁻¹ Jᵀ)⁻¹ |
| associativity | 70 | taught | MA-054: matrix product associativity |
| atan2 | 219 | add | **atan2 (two-argument arctangent)** (maths) → MA 05-linear-algebra (new rigid-body Note); MR 6.1 analytic IK and every heading angle need the quadrant-correct angle; not named in any Note |
| atlas | 27 | out-of-scope | manifold atlas is differential-geometry machinery (MR 2.3.3); C-space is taught in plain words in N72 |
| axis-angle representation | 79 | taught | plan§4 Axis-angle, exponential and log maps: axis-angle (planned MA Note) |
| back-emf | 308 | add | **DC motor model: torque constant and back-EMF** (control) → RB-02 (extend N283); MR 8.9.1: motor torque = k_t·i and back-EMF = k_e·ω set the speed-torque curve every joint actuator obeys |
| backlash | 2, 446 | add | **backlash and gear transmission errors** (robotics) → RB-02 (extend N283); MR 8.9 and 11.9 list backlash as a main cause of joint tracking error with gears |
| bang-bang trajectory | 340 | add | **bang-bang (time-optimal) trajectory** (control) → RO-15 (extend N203); MR 9.4: max acceleration then max deceleration is the time-optimal profile; trapezoid limit case |
| Barrett Technology’s WAM | 150 | index-noise | robot product name (Barrett WAM) used as an example |
| bifurcation point | 257 | out-of-scope | bifurcation points of closed-chain configuration spaces (MR 7.4) are closed-chain research detail |
| body frame | 61 | add | **fixed (space) frame vs body frame** (robotics) → RB-01 (extend N275); MR 3.1: every twist, Jacobian and IMU reading is stated in either the fixed frame or the body frame |
| C-space | 12 | taught | N72: C-space |
| C-space, free | 353 | taught | N73: free space |
| C-space, obstacle | 358 | taught | N73: C-space obstacle |
| C-space, representation | 25 | taught | N72: C-space representation (explicit vs implicit, plain words) |
| C-space, topologically equivalent | 24 | out-of-scope | topological equivalence (homeomorphism) is topology machinery; C-space shape taught in plain words in N72 |
| C-space, topology | 23 | taught | N72: C-space topology in plain words (circle, torus) |
| Cartesian product | 25 | add | **Cartesian product of spaces** (maths) → RO-01 (extend N72); MR 2.3.1: C-space of a chain is a product of joint spaces (torus = S1 × S1) |
| Cartesian robot | 431 | add | **robot arm types: Cartesian, SCARA, articulated, parallel** (robotics) → RB-01 (extend N276); MR 11.1/4: arm geometry names a course expects; sets workspace shape |
| Cayley–Rodrigues parameters | 68, 582 | out-of-scope | Cayley–Rodrigues parameters are an alternative rotation parameterisation (MR App. B); Euler angles, quaternions and exponential coordinates already cover rotation representations |
| center of mass | 283 | taught | N295: centre of mass |
| center of rotation (CoR) | 473 | add | **instantaneous centre of rotation (ICR)** (robotics) → RO-01 (extend N66); MR 12/13: every wheeled base turns about one point; explains Ackermann and diff-drive turning |
| centripetal force | 276 | add | **centripetal and Coriolis forces** (control) → RB-02 (extend N281); MR 8.1: the velocity term c(q,q̇) of the manipulator equation is made of these |
| Chasles–Mozzi theorem | 105 | add | **Chasles–Mozzi theorem (every rigid motion is a screw motion)** (robotics) → RB-01 (extend N275); MR 3.3.2: the reason a twist/screw describes every rigid-body motion |
| chassis | 513 | index-noise | body-part word (chassis) in wheeled-robot section |
| Christoffel symbols of the first kind | 278 | add | **centripetal and Coriolis forces** (control) → RB-02 (extend N281); Christoffel symbols compute the c(q,q̇) term (MR 8.1.2); taught via the Coriolis-force concept |
| closed-chain mechanism | 18, 245 | add | **closed chains and parallel robots** (robotics) → RB-01 (new Note); MR ch.7: Stewart platform, Delta robot; a robotics course expects the open vs closed chain distinction and loop-closure constraints |
| collision–detection routine | 362 | taught | N108: collision detection |
| collision–detection routine, sphere approximation | 363 | taught | N108: bounding volumes (spheres) for collision checks |
| commutation | 306 | add | **DC motor commutation (brushed vs brushless)** (control) → RB-02 (extend N283); MR 8.9.1: why brushless motors need electronic commutation; every robot joint uses one |
| commutativity | 71 | index-noise | group property; covered by matrix multiplication non-commutativity (MA-054) |
| condition number | 199 | taught | MA-058: condition number (also used for manipulability in N278) |
| configuration | 12 | taught | N72: configuration |
| configuration space (see C-space) |  | index-noise | cross-reference to C-space |
| connected component | 358 | add | **connected components of a graph or free space** (maths) → RO-05 (extend N103); MR 10.2: planning succeeds only if start and goal are in the same component |
| connectivity | 368 | add | **grid connectivity (4- and 8-connected)** (robotics) → RO-05 (extend N106); MR 10.4: grid planners choose 4- or 8-neighbours; changes path shape and cost |
| constrained dynamics | 301 | taught | N289: constrained dynamics with contact forces |
| constraint |  | index-noise | group heading; sub-entries judged separately |
| constraint, active | 466 | taught | MA-066: active constraint (KKT) |
| constraint, artificial | 439 | taught | N286: natural and artificial constraints |
| constraint, holonomic | 30 | taught | N64: holonomic constraint |
| constraint, homogeneous | 469 | out-of-scope | homogeneous contact constraint (MR 12.1) is contact-mode book notation; contact kinematics taught N288 |
| constraint, impenetrability | 465 | taught | N288: impenetrability (no-penetration) contact constraint |
| constraint, integrable | 31 | taught | N64: integrable (holonomic) constraint |
| constraint, natural | 438 | taught | N286: natural constraints |
| constraint, nonholonomic | 32 | taught | N64: nonholonomic constraint |
| constraint, Pfaffian | 31, 439 | add | **Pfaffian velocity constraints A(q)q̇ = 0** (robotics) → RO-01 (extend N64); MR 2.4: the standard form of wheel and contact constraints used later in dynamics and control |
| constraint, rolling | 466 | taught | N288: rolling constraint |
| contact |  | index-noise | group heading; sub-entries judged separately |
| contact, frictionless point | 472 | taught | N288: frictionless point contact |
| contact, kinematics | 463 | taught | N288: contact kinematics |
| contact, point with friction | 472 | taught | N288: point contact with friction |
| contact, roll–slide | 465, 466 | taught | N288: rolling and sliding contact |
| contact, rolling | 466 | taught | N288: rolling contact |
| contact, sliding | 466 | taught | N288: sliding contact |
| contact, soft | 472 | taught | N288: soft-finger contact |
| contact label | 466 | out-of-scope | contact label is MR book notation for contact modes (MR 12.1.2) |
| contact mode | 469 | taught | N289: contact modes switching (hybrid system) |
| contact normal | 464 | taught | N288: contact normal and friction cone |
| control |  | index-noise | group heading; sub-entries judged separately |
| control, proportional (P) | 414 | taught | N117: proportional control |
| control, adaptive | 448 | out-of-scope | adaptive control: MR 11.9 names it only in 'other topics'; beyond the book's own taught depth |
| control, admittance-controlled robot | 443 | taught | N287: admittance-controlled robot |
| control, centralized | 432 | taught | N284: centralized control |
| control, compliance | 442 | taught | N287: compliance (impedance) control |
| control, computed torque | 429 | taught | N284: computed torque |
| control, decentralized | 431 | taught | N284: decentralized (independent-joint) control |
| control, feedback | 414 | taught | N117: feedback control |
| control, feedforward | 414 | taught | N119: feedforward control |
| control, feedforward–feedback | 418 | taught | N119: feedforward plus feedback |
| control, force | 403, 434 | taught | N286: force control |
| control, gain | 414 | taught | N117: control gains |
| control, hybrid motion–force | 403, 437 | taught | N286: hybrid motion-force control |
| control, impedance | 403, 441 | taught | N287: impedance control |
| control, impedance-controlled robot | 443 | taught | N287: impedance-controlled robot |
| control, inverse dynamics | 429 | taught | N284: inverse dynamics control |
| control, iterative learning | 448 | out-of-scope | iterative learning control is named only in MR 11.9 'other topics'; not taught in the book |
| control, linear | 414 | taught | plan§4 State-space models: linear control of linear error dynamics (MR 11.2); state-space models planned in plan §4 |
| control, motion | 403 | taught | N284: motion control |
| control, motion, with torque or force inputs | 420 | taught | N284: motion control with torque inputs (PD plus gravity, computed torque) |
| control, motion, with velocity inputs | 413 | taught | N284: motion control with velocity inputs |
| control, open-loop | 414 | add | **open-loop vs closed-loop control** (control) → RO-06 (extend N117); MR 11.1: the basic split of control; N117 teaches feedback only |
| control, proportional-derivative (PD) | 423 | taught | N117: PD control |
| control, proportional-integral (PI) | 415 | taught | N117: PI control |
| control, proportional-integral-derivative (PID) | 422 | taught | N117: PID control |
| control, robust | 448 | out-of-scope | robust control named only in MR 11.9 'other topics' |
| control, setpoint | 414 | add | **setpoint regulation vs trajectory tracking** (control) → RO-06 (extend N117); MR 11.1: regulation to a constant target vs tracking a moving one |
| control, stiffness | 442 | taught | N287: stiffness control |
| control, task-space motion control | 433 | taught | N285: task-space motion control |
| control vector field | 522 | add | **control-affine systems (drift and control vector fields)** (control) → MA 06-calculus (extend planned State-space models Note); MR 13.3.2: x' = f(x) + G(x)u, the form wheeled-robot and CBF analysis use |
| control-affine system | 531 | add | **control-affine systems (drift and control vector fields)** (control) → MA 06-calculus (extend planned State-space models Note); MR 13.3.2 control-affine system |
| controllable robot | 529 | taught | N67: controllability of a car (plain words) |
| coordinate chart | 27 | out-of-scope | coordinate chart is differential-geometry machinery (MR 2.3.3) |
| coordinate free | 60 | index-noise | phrase about notation style (coordinate-free) |
| Coriolis force | 276 | add | **centripetal and Coriolis forces** (control) → RB-02 (extend N281); Coriolis force in c(q,q̇) (MR 8.1) |
| Coriolis matrix | 279 | add | **centripetal and Coriolis forces** (control) → RB-02 (extend N281); Coriolis matrix, used for the skew-symmetry property in PD stability (MR 8.1.2) |
| D–H parameters | 140, 585 | taught | N69: Denavit-Hartenberg parameters |
| D–H parameters and product of exponentials |  | index-noise | group heading; sub-entry judged |
| D–H parameters and product of exponentials, comparison | 595 | taught | N276: DH vs product of exponentials comparison |
| da Vinci S Surgical System | 238 | index-noise | robot product name (example) |
| damped natural frequency | 411 | add | **damped natural frequency** (control) → RO-06 (extend N118); MR 11.2.2: oscillation frequency of an underdamped second-order response |
| damping |  | index-noise | group heading; sub-entries judged |
| damping, critical | 411 | taught | N118: critical damping |
| damping, overdamped solution | 411 | taught | N118: overdamped response |
| damping, underdamped solution | 411 | taught | N118: underdamped response |
| damping ratio | 410 | taught | N118: damping ratio |
| DC motor | 305 | add | **DC motor model: torque constant and back-EMF** (control) → RB-02 (extend N283); MR 8.9.1 DC motor model |
| DC motor, brushed | 306 | add | **DC motor commutation (brushed vs brushless)** (control) → RB-02 (extend N283); MR 8.9.1 |
| DC motor, brushless | 306 | add | **DC motor commutation (brushed vs brushless)** (control) → RB-02 (extend N283); MR 8.9.1 |
| degrees of freedom (dof) | 12 | taught | N72: degrees of freedom |
| Delta robot | 22, 245 | add | **closed chains and parallel robots** (robotics) → RB-01 (new Note); Delta robot is MR's parallel-robot example (MR 2.2, 7) |
| Denavit–Hartenberg parameters (see D–H parameters) |  | index-noise | cross-reference to D–H parameters |
| diff-drive robot | 523 | taught | N64: differential drive |
| differential equation |  | index-noise | group heading; sub-entries judged |
| differential equation, homogeneous | 407 | add | **linear ODEs: homogeneous and particular solutions** (maths) → MA 06-calculus (planned ODEs Note); MR 11.2 solves error dynamics as linear ODEs; the step response is built from these |
| differential equation, nonhomogeneous | 407 | add | **linear ODEs: homogeneous and particular solutions** (maths) → MA 06-calculus (planned ODEs Note); MR 11.2 nonhomogeneous ODE |
| direct-drive robot | 313 | add | **direct drive vs geared joints** (robotics) → RB-02 (extend N283); MR 8.9.3: trade-off of gear ratio vs backdrivability and reflected inertia |
| distance-measurement algorithm | 362 | taught | N108: distance computation between bodies |
| dof | 12 | index-noise | abbreviation of degrees of freedom |
| Dubins car | 537 | taught | N64: Dubins car |
| dynamic grasp | 496 | out-of-scope | dynamic grasp (MR 12.3) is a book-specific case study of manipulation with dynamics |
| dynamics of a rigid body | 283 | taught | N220: rigid-body dynamics |
| dynamics of a rigid body, classical formulation | 283 | taught | N220: Newton-Euler rigid-body dynamics |
| dynamics of a rigid body, twist–wrench formulation | 288 | add | **twist-wrench (spatial) form of rigid-body dynamics** (robotics) → RB-02 (extend N282); MR 8.2.2: the 6-D form F = G V̇ − [ad_V]ᵀ G V that recursive Newton-Euler uses |
| dynamics of open chains | 271 | taught | N281: dynamics of open chains |
| dynamics of open chains, Lagrangian formulation | 272 | taught | N281: Lagrangian formulation |
| dynamics of open chains, Newton–Euler recursive formulation | 291 | taught | N282: recursive Newton-Euler |
| dynamics of open chains, Newton–Euler recursive formulation with gearing | 312 | taught | N283: Newton-Euler with gearing (reflected inertia) |
| Eclipse mechanism | 267 | index-noise | mechanism example name |
| elbow-down (righty) solution | 219 | taught | N279: multiple IK solutions (elbow up/down) |
| elbow-up (lefty) solution | 219 | taught | N279: multiple IK solutions (elbow up/down) |
| electrical constant | 308 | add | **DC motor model: torque constant and back-EMF** (control) → RB-02 (extend N283); electrical constant k_e (MR 8.9.1) |
| end-effector | 11 | taught | N276: end-effector |
| equations of motion | 271 | taught | N281: equations of motion |
| error dynamics | 406 | taught | N118: error dynamics |
| error response | 406 | taught | N118: error response |
| Euclidean space | 24 | add | **Euclidean space R^n** (maths) → MA 05-linear-algebra (new rigid-body Note); MR 2.3: base space for C-space and task space; plain naming |
| Euler angles | 68, 575 | taught | plan§4 3D rotations Note: Euler angles (planned MA Note) |
| Euler’s equation for a rotating body | 284 | taught | N220: Euler's equation for a rotating body |
| Euler–Lagrange equations | 273 | taught | N281: Euler-Lagrange equations |
| exceptional objects | 479 | out-of-scope | exceptional objects (MR 12.2) is a book-specific grasp-closure term |
| exponential coordinates |  | taught | N275: exponential coordinates |
| exponential coordinates, for rigid-body motion | 104 | taught | N275: exponential coordinates of rigid motion |
| exponential coordinates, for rotation | 79, 82 | taught | plan§4 Axis-angle, exponential and log maps: axis-angle (planned MA Note) |
| five-bar linkage | 20 | add | **closed chains and parallel robots** (robotics) → RB-01 (new Note); five-bar linkage is the planar closed-chain example (MR 2.2, 7) |
| fixed frame | 61 | add | **fixed (space) frame vs body frame** (robotics) → RB-01 (extend N275); MR 3.1 fixed frame |
| force closure | 489 | taught | N290: force closure |
| force ellipsoid | 176, 199 | add | **acceleration and force ellipsoids** (robotics) → RB-01 (extend N278); MR 5.4 force ellipsoid is the dual of the manipulability ellipsoid |
| form closure | 469, 478 | taught | N290: form closure |
| forward dynamics | 271 | taught | N282: forward dynamics |
| forward kinematics | 137 | taught | N69: forward kinematics |
| forward kinematics, parallel mechanisms | 247 | add | **closed chains and parallel robots** (robotics) → RB-01 (new Note); MR 7.1: forward kinematics of parallel mechanisms is the hard direction (opposite of serial arms) |
| four-bar linkage | 18 | add | **closed chains and parallel robots** (robotics) → RB-01 (new Note); four-bar linkage is the basic closed chain (MR 2.2) |
| free vector | 60 | out-of-scope | 'free vector' is the book's coordinate-free notation remark (MR 3.1) |
| friction | 484 | taught | N288: friction |
| friction, Coulomb | 484 | taught | N288: Coulomb friction |
| friction, static | 314 | taught | N283: static friction in joints and motors |
| friction, viscous | 314 | taught | N283: viscous friction in joints and motors |
| friction angle | 484 | taught | N288: friction angle = half-angle of the friction cone |
| friction coefficient | 484 | taught | N288: friction coefficient |
| friction cone | 484 | taught | N288: friction cone |
| gantry robot | 431 | add | **robot arm types: Cartesian, SCARA, articulated, parallel** (robotics) → RB-01 (extend N276); gantry = Cartesian robot (MR 11.1) |
| gearing | 310 | taught | N283: gearing |
| gearing, harmonic drive | 314 | add | **backlash and gear transmission errors** (robotics) → RB-02 (extend N283); harmonic drive: zero-backlash gearhead used in most robot joints (MR 8.9.3) |
| generalized coordinates | 272 | taught | N281: generalized coordinates |
| generalized forces | 272 | taught | N281: generalized forces |
| GJK algorithm | 362 | out-of-scope | GJK is an algorithm inside collision libraries (MR 10.3 names it only); N108 teaches collision checking at usage level |
| Grübler’s formula | 17 | taught | N70: Grübler's formula |
| graph | 364 | taught | N103: graph |
| graph, directed | 364 | taught | N103: directed graph |
| graph, undirected | 364 | taught | N103: undirected graph |
| graph, unweighted | 364 | taught | N103: unweighted graph |
| graph, visibility | 368 | taught | N270: visibility graph |
| graph, weighted | 364 | taught | N104: weighted graph (edge costs) |
| graph edge | 364 | taught | N103: graph edge |
| graph node | 364 | taught | N103: graph node |
| grasp metric | 482 | taught | N291: grasp quality metric |
| group closure | 70 | out-of-scope | group closure axiom is group theory (MR 3.2.1); rotations are taught as matrices |
| homogeneous coordinates | 90 | taught | plan§4 Rigid-body transforms: homogeneous coordinates (planned MA Note) |
| homogeneous transformation matrix | 89 | taught | plan§4 Rigid-body transforms: homogeneous transformation matrix (planned MA Note) |
| homotopic path | 398 | out-of-scope | homotopy classes of paths are topology (MR 10.1 aside) |
| impedance | 441 | taught | N287: impedance |
| inadmissible state | 339 | taught | N203: inadmissible states in the phase plane (time-optimal scaling) |
| inconsistent problem | 495 | out-of-scope | 'inconsistent problem' is MR 12.2 book terminology for contact-mode analysis |
| inertia matching | 323 | add | **gear ratio choice: direct drive vs geared, inertia matching** (robotics) → RB-02 (extend N283); MR 8.9.2: choosing a gear ratio to match motor and load inertia |
| inertia matrix |  | taught | N220: inertia matrix |
| inertia matrix, rotational | 284 | taught | N220: rotational inertia matrix |
| inertia matrix, spatial | 288 | add | **twist-wrench (spatial) form of rigid-body dynamics** (robotics) → RB-02 (extend N282); spatial inertia matrix G (MR 8.2.2) |
| inertial measurement unit (IMU) | 560 | taught | N83: IMU |
| integrator anti-windup | 425 | taught | N119: integrator anti-windup |
| inverse dynamics | 271 | taught | N282: inverse dynamics |
| inverse kinematics | 219 | taught | N279: inverse kinematics |
| inverse kinematics, analytic | 221 | taught | N279: analytic IK |
| inverse kinematics, numerical | 226 | taught | N279: numerical IK |
| inverse kinematics, parallel mechanisms | 247 | add | **closed chains and parallel robots** (robotics) → RB-01 (new Note); IK of parallel mechanisms is the easy direction (MR 7.1) |
| inverse velocity kinematics | 232 | taught | N280: inverse velocity kinematics |
| isotropic manipulability ellipsoid | 198 | taught | N278: isotropic manipulability |
| Jacobi identity | 322 | out-of-scope | Jacobi identity is a Lie-algebra proof identity (MR 8.2 exercise) |
| Jacobian | 171 | taught | N277: Jacobian |
| Jacobian, analytic | 188 | taught | N277: analytic Jacobian |
| Jacobian, body | 178, 185 | taught | N277: body Jacobian |
| Jacobian, constraint | 252 | add | **closed chains and parallel robots** (robotics) → RB-01 (new Note); constraint Jacobian of loop-closure equations (MR 7.2) |
| Jacobian, geometric | 188 | taught | N277: geometric Jacobian |
| Jacobian, space | 178, 180 | taught | N277: space Jacobian |
| jamming | 500 | add | **jamming and wedging in peg-in-hole insertion** (robotics) → RB-07 (extend N327); MR 12.3: the classic failure modes of insertion; why compliance is needed |
| joint | 11 | taught | N70: joint |
| joint, cylindrical | 16 | taught | N70: cylindrical joint (joint types) |
| joint, helical | 16 | taught | N70: helical joint |
| joint, prismatic | 16 | taught | N70: prismatic joint |
| joint, revolute | 16 | taught | N70: revolute joint |
| joint, screw | 16 | taught | N70: screw joint |
| joint, spherical | 16 | taught | N70: spherical joint |
| joint, universal | 16 | taught | N70: universal joint |
| Kalman rank condition | 528 | taught | N204: Kalman rank condition for controllability |
| kinetic energy | 272 | taught | N281: kinetic energy |
| Krasovskii–LaSalle invariance principle | 458 | out-of-scope | Krasovskii-LaSalle invariance principle is a stability-proof technique (MR 11.4 proof) |
| Lagrange multiplier | 234, 302, 440, 598 | taught | MA-066: Lagrange multipliers |
| Lagrangian function | 272 | taught | N281: Lagrangian function |
| law of cosines | 220 | add | **law of cosines for analytic IK** (maths) → RB-01 (extend N279); MR 6.1: the 2-link analytic IK is solved with the law of cosines and atan2 |
| lefty solution | 219 | taught | N279: lefty/righty IK branches |
| Lie algebra | 77, 98 | taught | plan§4 Cross product and skew-symmetric matrix: so(3)/se(3) taught as skew-symmetric matrices and twists (N275) |
| Lie algebra, of vector fields | 534 | out-of-scope | Lie algebra of vector fields is nonlinear geometric control (MR 13.3.2) |
| Lie bracket |  | index-noise | group heading; sub-entries judged |
| Lie bracket, of twists | 289 | add | **twist-wrench (spatial) form of rigid-body dynamics** (robotics) → RB-02 (extend N282); Lie bracket of twists (ad_V) appears in the spatial dynamics equation (MR 8.2.2) |
| Lie bracket, of vector fields | 532 | out-of-scope | Lie bracket of vector fields is differential-geometric controllability (MR 13.3.2); the plain-words car controllability is N67 |
| Lie product | 533 | out-of-scope | Lie product: same geometric-control machinery (MR 13.3.2) |
| linear program | 480 | taught | MA-068: linear program |
| linear system | 406 | taught | plan§4 State-space models: linear system x' = Ax + Bu (planned MA Note) |
| linearly controllable | 528 | taught | N204: linear controllability |
| link | 11 | taught | N70: link |
| loop-closure equation | 28, 29 | add | **closed chains and parallel robots** (robotics) → RB-01 (new Note); loop-closure equations (MR 2.3, 7) |
| Manhattan distance | 370 | taught | ML-085: Manhattan distance (Minkowski family) |
| manipulability ellipsoid | 173, 197 | taught | N278: manipulability ellipsoid |
| mass ellipsoid | 280 | add | **acceleration and force ellipsoids** (robotics) → RB-01 (extend N278); mass ellipsoid visualises the mass matrix (MR 8.1.4) |
| mass matrix | 271, 275, 277, 279 | taught | N281: mass matrix |
| matrix |  | index-noise | group heading; sub-entries judged |
| matrix, rotation | 28 | taught | N65: rotation matrix |
| matrix exponential | 80 | taught | plan§4 Matrix exponential and logarithm: matrix exponential (planned MA Note) |
| matrix exponential, for rigid-body motion | 105 | taught | N275: matrix exponential of a twist |
| matrix exponential, for rotations | 84 | taught | plan§4 Axis-angle, exponential and log maps: exponential of rotations (planned MA Note) |
| matrix Lie group | 70 | out-of-scope | 'matrix Lie group' is group-theory naming; SE(3)/SO(3) taught as matrices (plan §7 PA 4.6) |
| matrix logarithm |  | index-noise | group heading; sub-entries judged |
| matrix logarithm, for rigid-body motion | 106 | taught | N275: matrix log of a rigid motion |
| matrix logarithm, for rotation | 85 | taught | plan§4 Axis-angle, exponential and log maps: log of a rotation (planned MA Note) |
| mecanum wheel | 514 | taught | N66: mecanum wheel |
| meter-stick trick | 498 | index-noise | demonstration example (meter-stick trick) |
| mobile manipulation | 548 | taught | N334: mobile manipulation |
| moment | 108 | taught | N117: moment of force (torque) in the mechanics short section |
| moment, pure | 109 | taught | N275: pure moment as part of a wrench |
| moment labeling | 488 | out-of-scope | moment labeling is MR 12.2's graphical method for planar force closure, book-specific |
| motion planning | 353 | taught | N72: motion planning problem |
| motion planning, anytime | 356 | taught | N105: anytime planning (ARA*) |
| motion planning, approximate | 355 | add | **quadtrees and multi-resolution grids** (robotics) → RO-04 (extend N97); MR 10.4.2: approximate cell decomposition with adaptive cells for planning |
| motion planning, complete | 356 | taught | N111: complete planners |
| motion planning, complete planners | 368 | taught | N111: complete planners |
| motion planning, computational complexity | 356 | taught | N103: computational complexity of planning |
| motion planning, exact | 355 | taught | N270: exact planning (exact roadmaps) |
| motion planning, grid methods | 369 | taught | N106: grid methods |
| motion planning, multiple query | 356 | add | **single-query vs multi-query planners** (robotics) → RO-05 (extend N111); MR 10.1: why PRM (multi-query) and RRT (single-query) suit different uses |
| motion planning, nonlinear optimization | 392 | taught | N116: planning by nonlinear optimisation |
| motion planning, offline | 355 | taught | N107: offline vs online planning |
| motion planning, online | 355 | taught | N107: online planning (replanning) |
| motion planning, optimal | 355 | taught | N110: optimal planning (RRT*) |
| motion planning, path planning | 355 | taught | N106: path planning |
| motion planning, piano mover’s problem | 355 | taught | N72: piano mover's problem |
| motion planning, PRM algorithm | 384 | taught | N111: PRM |
| motion planning, probabilistically complete | 356 | taught | N111: probabilistic completeness |
| motion planning, RDT algorithm | 380 | taught | N110: RDT (rapidly exploring dense tree) |
| motion planning, resolution complete | 356 | taught | N111: resolution completeness |
| motion planning, RRT algorithm | 379 | taught | N110: RRT |
| motion planning, RRT algorithm, bidirectional | 382 | add | **bidirectional RRT (RRT-Connect)** (robotics) → RO-05 (extend N110); MR 10.5.1: grow trees from start and goal; the default RRT variant in libraries |
| motion planning, RRT ∗ algorithm | 383 | taught | N110: RRT* |
| motion planning, sampling methods | 378 | taught | N110: sampling-based planning |
| motion planning, satisficing | 355 | taught | N9: satisficing (feasible) vs optimal |
| motion planning, single query | 356 | add | **single-query vs multi-query planners** (robotics) → RO-05 (extend N111); MR 10.1 single-query |
| motion planning, smoothing | 394 | taught | N113: path smoothing |
| motion planning, virtual potential fields | 386 | mentioned-only | **artificial potential fields (attractive and repulsive)** (robotics) → RO-05 (extend N109); MR 10.6: the basic attractive/repulsive field and its local minima; N109 only teaches the randomized variant |
| motion planning, wavefront planner | 370 | taught | N106: wavefront planner |
| motion planning, wheeled mobile robot | 374 | taught | N112: planning for wheeled robots |
| MoveIt | 353 | add | **motion-planning libraries: MoveIt and OMPL** (robotics) → RB-03 (new section); MR 10: the standard tools that run these planners on real arms, like Nav2 for bases (N131) |
| multi-resolution grid | 372 | add | **quadtrees and multi-resolution grids** (robotics) → RO-04 (extend N97); MR 10.4.2 multi-resolution grid |
| natural frequency | 410 | taught | N118: natural frequency |
| navigation function | 389 | taught | N106: navigation function |
| neighborhood | 529 | out-of-scope | neighborhood is the topological notion in small-time local controllability (MR 13.4) |
| neighbors |  | index-noise | group heading; sub-entries judged |
| neighbors, 4-connected | 369 | add | **grid connectivity (4- and 8-connected)** (robotics) → RO-05 (extend N106); MR 10.4.1 |
| neighbors, 8-connected | 369 | add | **grid connectivity (4- and 8-connected)** (robotics) → RO-05 (extend N106); MR 10.4.1 |
| Newton–Raphson root finding | 227 | taught | plan§4 Newton-Raphson root finding: Newton-Raphson (planned short section, N279) |
| no-load speed | 308 | add | **DC motor model: torque constant and back-EMF** (control) → RB-02 (extend N283); no-load speed is one end of the speed-torque curve (MR 8.9.1) |
| octree | 373 | taught | N97: octree |
| odometry | 546 | taught | N68: odometry |
| omniwheel | 514 | taught | N66: omniwheel |
| Open Motion Planning Library | 398 | add | **motion-planning libraries: MoveIt and OMPL** (robotics) → RB-03 (new section); OMPL (MR 10.9) |
| open-chain mechanism | 18 | taught | N69: open chain |
| overshoot | 406 | taught | N118: overshoot |
| parallel mechanisms | 245 | add | **closed chains and parallel robots** (robotics) → RB-01 (new Note); parallel mechanisms (MR ch.7) |
| parallel-axis theorem | 287 | add | **parallel-axis theorem** (robotics) → RO-17 (extend N220); MR 8.2.1: inertia about a point other than the centre of mass; needed to build link inertias for URDF/simulators |
| parametrization |  | index-noise | group heading; sub-entry judged |
| parametrization, explicit | 27 | taught | N72: explicit C-space parameterisation (plain words) |
| passivity property | 279 | out-of-scope | passivity (Ṁ − 2C skew-symmetric) is a stability-proof property (MR 8.1.2) |
| path | 325 | taught | N104: path |
| peg insertion | 500 | taught | N327: peg insertion |
| phase plane | 339 | taught | N203: phase plane |
| polyhedral convex cone | 469 | taught | MA-067: polyhedral convex cone (convex sets; friction pyramid N288) |
| polyhedral convex set | 469 | taught | MA-067: polyhedral convex set |
| polytope | 469 | taught | MA-068: polytope |
| potential energy | 272 | taught | N281: potential energy |
| principal axes of inertia | 285 | add | **principal axes of inertia** (robotics) → RO-17 (extend N220); MR 8.2.1: the inertia matrix is diagonal in its eigen-axes; ties MA-056 eigenvectors to a body |
| principal moments of inertia | 285 | add | **principal axes of inertia** (robotics) → RO-17 (extend N220); principal moments = eigenvalues of the inertia matrix (MR 8.2.1) |
| product of exponentials | 140 | taught | N276: product of exponentials |
| product of exponentials, body form | 149 | taught | N276: PoE body form |
| product of exponentials, space form | 142 | taught | N276: PoE space form |
| product of exponentials and D–H parameters |  | index-noise | group heading; sub-entry judged |
| product of exponentials and D–H parameters, comparison | 595 | taught | N276: PoE vs DH comparison |
| pseudoinverse | 229 | taught | N279: pseudo-inverse in numerical IK |
| pseudoinverse, left | 229 | add | **left and right pseudo-inverse** (maths) → MA 05-linear-algebra (extend MA-060); MR 6.2.1: tall vs wide Jacobians need the left (least-squares) or right (minimum-norm) pseudo-inverse |
| pseudoinverse, right | 229 | add | **left and right pseudo-inverse** (maths) → MA 05-linear-algebra (extend MA-060); right pseudo-inverse = minimum-norm solution for redundant arms (MR 6.2.1) |
| PUMA-type arm | 221 | index-noise | arm example name (PUMA) |
| quadtree | 373 | add | **quadtrees and multi-resolution grids** (robotics) → RO-04 (extend N97); MR 10.4.2: the 2D version of the octree; adaptive grid for planning and maps |
| quasistatic | 496 | add | **quasistatic assumption** (robotics) → RB-03 (extend N292); MR 12.3: manipulation analysed with negligible inertia; the standard simplifying assumption for pushing and assembly |
| quaternion, unit | 581 | taught | plan§4 3D rotations: unit quaternion (planned MA Note) |
| reachability | 368 | taught | N204: reachability |
| reachable set | 529 | taught | N112: reachable set |
| reciprocal wrench and twist | 466 | out-of-scope | reciprocal wrench/twist (MR 12.1) is screw-theory machinery for contact analysis; contact kinematics taught in N288 at beginner level |
| redundant actuation | 246 | add | **closed chains and parallel robots** (robotics) → RB-01 (new Note); redundant actuation in parallel mechanisms (MR 7.3) |
| redundant constraint | 14 | taught | N70: redundant constraints in Grübler's count |
| redundant robot | 190, 234 | taught | N278: redundant robot |
| Reeds–Shepp car | 538 | taught | N64: Reeds-Shepp car |
| reflected inertia | 310 | taught | N283: reflected inertia |
| repelling wrench and twist | 466 | out-of-scope | repelling wrench/twist is MR 12.1 screw-theory contact notation |
| representation |  | index-noise | group heading; sub-entry judged |
| representation, implicit | 28 | taught | N72: implicit C-space representation (plain words) |
| right-handed reference frame | 62 | add | **right-handed frames and the right-hand rule** (maths) → RO-01 (extend N65); MR 3.1: all frames are right-handed; sign of every cross product and rotation |
| righty solution | 219 | taught | N279: righty IK branch |
| rigid body |  | index-noise | group heading; sub-entries judged |
| rigid body, planar | 15 | taught | N72: planar rigid body DOF |
| rigid body, spatial | 15 | taught | N72: spatial rigid body DOF |
| rigid-body motion | 89 | taught | plan§4 Rigid-body transforms: rigid-body motion (planned MA Note, N275) |
| roadmap | 368 | taught | N111: roadmap |
| Robot Operating System (ROS) | 152, 354 | taught | N127: ROS |
| Rodrigues’ formula | 84 | taught | plan§4 Matrix exponential and logarithm: Rodrigues' formula |
| roll–pitch–yaw angles | 68, 580 | taught | plan§4 3D rotations: roll-pitch-yaw angles (planned MA Note) |
| root locus | 416 | add | **root locus** (control) → RO-06 (new Note after N118); MR 11.2.2.2: how closed-loop poles move as a gain grows; the standard tool for choosing PD/PID gains |
| rotation | 68 | taught | N65: rotation |
| rotation matrix | 68 | taught | N65: rotation matrix |
| rotor | 305 | add | **DC motor model: torque constant and back-EMF** (control) → RB-02 (extend N283); rotor/stator: motor anatomy behind the motor model (MR 8.9.1) |
| rviz | 354 | taught | N127: RViz |
| SCARA | 34 | add | **robot arm types: Cartesian, SCARA, articulated, parallel** (robotics) → RB-01 (extend N276); SCARA arm (MR 4) |
| screw axis | 102 | taught | N275: screw axis |
| screw axis, body-frame | 149 | taught | N276: body-frame screw axes |
| screw axis, space-frame | 142 | taught | N276: space-frame screw axes |
| screw pitch | 103 | taught | N275: screw pitch |
| SE(3) | 89 | taught | plan§4 Rigid-body transforms: SE(3) as homogeneous matrices |
| se(3) | 98 | taught | N275: se(3) twists in matrix form |
| search |  | index-noise | group heading; sub-entries judged |
| search, A ∗ | 365 | taught | N105: A* search |
| search, breadth-first | 367 | taught | N103: breadth-first search |
| search, Dijkstra’s algorithm | 367 | taught | N104: Dijkstra's algorithm |
| search, suboptimal A ∗ | 367 | taught | N105: suboptimal (weighted) A* |
| serial mechanism | 18 | taught | N69: serial (open-chain) mechanism |
| series elastic actuator | 446, 459 | add | **series elastic actuators** (robotics) → RB-02 (extend N283); MR 11.6/11.9: a spring between motor and load lets the robot measure and control force; common in legged robots and cobots |
| settling time | 406 | taught | N118: settling time |
| shortest paths, car with reverse gear | 538 | taught | N112: Reeds-Shepp shortest paths |
| shortest paths, forward-only car | 537 | taught | N112: Dubins shortest paths |
| singularity | 21, 27, 172 | taught | N278: singularity |
| singularity, actuator | 256 | add | **closed chains and parallel robots** (robotics) → RB-01 (new Note); actuator singularities are a parallel-mechanism concept (MR 7.3) |
| singularity, actuator, degenerate | 259 | add | **closed chains and parallel robots** (robotics) → RB-01 (new Note); degenerate actuator singularity (MR 7.3) |
| singularity, actuator, nondegenerate | 259 | add | **closed chains and parallel robots** (robotics) → RB-01 (new Note); nondegenerate actuator singularity (MR 7.3) |
| singularity, C-space | 256, 258 | out-of-scope | C-space singularities of closed chains (MR 7.3) are topology of solution sets; beyond beginner closed-chain coverage |
| singularity, end-effector | 256, 261 | add | **closed chains and parallel robots** (robotics) → RB-01 (new Note); end-effector singularity of parallel mechanisms (MR 7.3) |
| singularity, kinematic | 191 | taught | N278: kinematic singularity |
| skew-symmetric matrix | 77 | taught | plan§4 Cross product and skew-symmetric matrix: skew-symmetric matrix |
| slider–crank mechanism | 18 | add | **closed chains and parallel robots** (robotics) → RB-01 (new Note); slider-crank is a closed-chain example (MR 2.2) |
| small-time locally accessible (STLA) | 529 | out-of-scope | small-time local accessibility is nonlinear controllability theory (MR 13.4) |
| small-time locally controllable (STLC) | 529 | out-of-scope | small-time local controllability is nonlinear controllability theory (MR 13.4); plain-words car controllability in N67 |
| so(3) | 77 | taught | plan§4 Cross product and skew-symmetric matrix: so(3) = 3x3 skew-symmetric matrices |
| SO(2) | 70 | taught | plan§4 Rigid-body transforms: SO(2) 2D rotation matrices |
| SO(3) | 70 | taught | N65: SO(3) rotation matrices |
| space frame | 61 | add | **fixed (space) frame vs body frame** (robotics) → RB-01 (extend N275); space frame (MR 3.1) |
| span |  | index-noise | group heading; sub-entries judged |
| span, conical | 462 | add | **linear, positive and convex span (cones of contact wrenches)** (maths) → RB-03 (extend N290); MR 12.1.6: force closure asks whether contact wrenches positively span the wrench space |
| span, convex | 462 | taught | plan§4 Convex hull: convex span = convex hull |
| span, linear | 462 | taught | MA-052: linear span |
| span, positive | 462 | add | **linear, positive and convex span (cones of contact wrenches)** (maths) → RB-03 (extend N290); positive span (MR 12.1.6) |
| spatial force | 109 | taught | N275: spatial force = wrench |
| spatial momentum | 289 | add | **twist-wrench (spatial) form of rigid-body dynamics** (robotics) → RB-02 (extend N282); spatial momentum (MR 8.2.2) |
| spatial velocity |  | index-noise | group heading; sub-entries judged |
| spatial velocity, in body frame | 97 | taught | N275: body twist |
| spatial velocity, in space frame | 99 | taught | N275: spatial twist |
| special Euclidean group (SE(3)) | 89 | taught | plan§4 Rigid-body transforms: SE(3) |
| special orthogonal group (SO(3)) | 70 | taught | N65: SO(3) |
| speed–torque curve | 308 | add | **DC motor model: torque constant and back-EMF** (control) → RB-02 (extend N283); speed-torque curve (MR 8.9.1) |
| stability of an assembly | 499 | out-of-scope | stability of an assembly (MR 12.3) is a book-specific case study |
| stable dynamics | 408 | taught | plan§4 Stability of dynamical systems: stable dynamics (planned MA Note) |
| stall torque | 308 | add | **DC motor model: torque constant and back-EMF** (control) → RB-02 (extend N283); stall torque (MR 8.9.1) |
| standard second-order form | 410 | taught | N118: standard second-order form |
| Stanford-type arm | 225 | index-noise | arm example name (Stanford arm) |
| state | 354 | taught | N63: state |
| stator | 305 | add | **DC motor model: torque constant and back-EMF** (control) → RB-02 (extend N283); stator (MR 8.9.1) |
| steady-state error | 406 | add | **steady-state error** (control) → RO-06 (extend N118); MR 11.2.1: the error left after the transient; why P control alone leaves an offset and I action removes it |
| steady-state response | 406 | add | **steady-state error** (control) → RO-06 (extend N118); steady-state response (MR 11.2.1) |
| Steiner’s theorem | 287 | add | **parallel-axis theorem** (robotics) → RO-17 (extend N220); Steiner's theorem = parallel-axis theorem (MR 8.2.1) |
| Stephenson six-bar linkage | 20 | add | **closed chains and parallel robots** (robotics) → RB-01 (new Note); six-bar linkage example (MR 2.2) |
| Stewart–Gough platform | 22, 245 | add | **closed chains and parallel robots** (robotics) → RB-01 (new Note); Stewart-Gough platform, the standard 6-DOF parallel robot (MR 7.1) |
| strain gauge | 405, 435, 446 | add | **force/torque sensors (strain gauges)** (robotics) → RB-02 (new section in N286); MR 11.5: force control needs a wrist force-torque sensor built from strain gauges |
| Stribeck effect | 314 | add | **friction models: Stribeck effect** (robotics) → RB-02 (extend N283); MR 8.9.4: friction drops just after motion starts; explains stick-slip in joints |
| Swedish wheel | 514 | taught | N66: Swedish (mecanum) wheel |
| T n | 25 | index-noise | symbol: T^n torus notation |
| tangent vector | 522 | out-of-scope | tangent vectors/vector fields as differential geometry (MR 13.3.2); velocity vector fields taught in the planned ODEs Note |
| tangent vector field | 522 | taught | plan§4 ODEs and vector fields: vector field (planned MA Note) |
| task space | 32 | taught | N276: task space |
| task-space dynamics | 300 | taught | N285: task-space dynamics |
| Taylor expansion | 227, 531 | taught | MA-064: Taylor expansion |
| time constant | 409 | add | **first-order systems and the time constant** (control) → RO-06 (extend N118); MR 11.2.2.1: exponential decay rate of first-order error dynamics; how fast a loop settles |
| time scaling | 326 | taught | N201: time scaling |
| time scaling, cubic | 329 | taught | N201: cubic time scaling |
| time scaling, quintic | 330 | taught | N201: quintic time scaling |
| time scaling, S-curve | 333 | taught | N201: S-curve |
| time scaling, time-optimal | 336 | taught | N203: time-optimal time scaling |
| time scaling, trapezoidal | 330 | taught | N201: trapezoidal profile |
| time-optimal trajectories, diff-drive | 540 | out-of-scope | time-optimal diff-drive trajectories (MR 13.3.3) is a specialised optimal-control result |
| torque | 108 | taught | N117: torque |
| torque constant | 306 | add | **DC motor model: torque constant and back-EMF** (control) → RB-02 (extend N283); torque constant (MR 8.9.1) |
| trajectory | 326 | taught | N201: trajectory |
| trajectory, point-to-point | 326 | taught | N201: point-to-point trajectory |
| trajectory, through via points | 334 | taught | N202: via points |
| trajectory tracking, nonholonomic mobile robot | 543 | taught | N124: trajectory tracking for nonholonomic robots (Kanayama) |
| transformation matrix | 89 | taught | plan§4 Rigid-body transforms: transformation matrix |
| transient response | 406 | taught | N118: transient response |
| tree | 364 | taught | N103: tree (search tree) |
| tree, child node | 364 | taught | N103: child node |
| tree, leaf node | 364 | taught | ML-091: leaf node |
| tree, parent node | 364 | taught | N103: parent node |
| tree, root node | 364 | taught | ML-091: root node |
| twist | 97 | taught | N275: twist |
| twist, body | 98 | taught | N275: body twist |
| twist, spatial | 99 | taught | N275: spatial twist |
| unit quaternions | 68 | taught | plan§4 3D rotations: unit quaternions |
| Universal Robot Description Format (URDF) | 152, 303 | taught | N70: URDF |
| Universal Robots’ UR5 | 147 | index-noise | robot product name (UR5) |
| unstable dynamics | 408 | taught | plan§4 Stability of dynamical systems: unstable dynamics |
| variable-impedance actuator | 449 | add | **series elastic actuators** (robotics) → RB-02 (extend N283); variable-impedance actuators (MR 11.9) extend the SEA idea |
| variable-stiffness actuator | 449 | add | **series elastic actuators** (robotics) → RB-02 (extend N283); variable-stiffness actuators (MR 11.9) |
| vector field | 522 | taught | plan§4 ODEs and vector fields: vector field |
| velocity limit curve | 339 | taught | N203: velocity limit curve in the phase plane |
| Watt six-bar linkage | 20 | add | **closed chains and parallel robots** (robotics) → RB-01 (new Note); Watt six-bar linkage example (MR 2.2) |
| wedging | 501 | add | **jamming and wedging in peg-in-hole insertion** (robotics) → RB-07 (extend N327); wedging (MR 12.3) |
| wheeled mobile robot | 513 | taught | N66: wheeled mobile robots |
| wheeled mobile robot, canonical | 526 | taught | N66: canonical wheeled model (unicycle) |
| wheeled mobile robot, car-like | 524 | taught | N67: car-like robot |
| wheeled mobile robot, diff-drive | 523 | taught | N64: diff-drive robot |
| wheeled mobile robot, nonholonomic | 514 | taught | N64: nonholonomic wheeled robot |
| wheeled mobile robot, omnidirectional | 514 | taught | N66: omnidirectional robot |
| wheeled mobile robot, unicycle | 521 | taught | N66: unicycle |
| workspace | 33 | taught | N276: workspace |
| wrench | 108 | taught | N275: wrench |
| wrench, body | 110 | taught | N275: body wrench |
| wrench, spatial | 110 | taught | N275: spatial wrench |
| zero-inertia point | 338, 344 | out-of-scope | zero-inertia point is a technical detail of the time-optimal phase-plane algorithm (MR 9.4) |

## LaValle, *Planning Algorithms* (2006)

Free official PDF: https://lavalle.pl/planning/book.pdf (from lavalle.pl/planning). Index pp. 985-1007.

Counts: taught 773, mentioned-only 1, add 77, out-of-scope 627, index-noise 291 (total 1769).

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| C 0 function | 385 | taught | N202: continuity at the joins of a trajectory |
| C ∞ function | 385 | out-of-scope | smooth-manifold machinery (C-infinity); PA 4.1/8.5 topology dropped |
| C ∞ manifold (see smooth manifold) |  | index-noise | cross-reference to smooth manifold |
| C ∞ structure (see smooth structure) |  | index-noise | cross-reference to smooth structure |
| C k function | 385 | taught | N202: continuity of derivatives at trajectory joins |
| GL(n) | 145 | out-of-scope | group theory (general linear group); PA 4.6 dropped, matrices taught instead |
| K-step information-feedback plan | 568 | out-of-scope | research-level information-space construct (LaValle ch.11 notation) |
| L 1 metric (see Manhattan metric) |  | index-noise | cross-reference to Manhattan metric |
| L 2 metric (see Euclidean metric) |  | index-noise | cross-reference to Euclidean metric |
| L ∞ metric | 187 | add | **Lp norms and metrics (L1, L2, L-infinity)** (maths) → MA 05-linear-algebra; distances between configurations and in grid planners use L1/L2/L-inf |
| L p metric | 187–188 | add | **Lp norms and metrics (L1, L2, L-infinity)** (maths) → MA 05-linear-algebra; distances between configurations and in grid planners use L1/L2/L-inf |
| L p norm | 188 | add | **Lp norms and metrics (L1, L2, L-infinity)** (maths) → MA 05-linear-algebra; distances between configurations and in grid planners use L1/L2/L-inf |
| SE(n) (see special Euclidean group) |  | index-noise | cross-reference to special Euclidean group |
| C (see conﬁguration space) |  | index-noise | cross-reference to configuration space |
| C obs (see obstacle region, in the C-space) |  | index-noise | cross-reference to obstacle region |
| X obs (see obstacle region, in the state space) |  | index-noise | cross-reference to obstacle region |
| X ric (see obstacle region, in the state space) |  | index-noise | cross-reference to obstacle region |
| ǫ-goodness | 240 | out-of-scope | proof technique (visibility-roadmap coverage analysis) |
| I hist (see history information space) |  | index-noise | cross-reference to history information space |
| I ndet (see nondeterministic information space) |  | index-noise | cross-reference to nondeterministic information space |
| I prob (see probabilistic information space) |  | index-noise | cross-reference to probabilistic information space |
| k-cell | 267 | out-of-scope | cell-complex topology (singular complexes); PA 6.x exact algebraic planning dropped |
| k-neighborhood | 221 | add | **grid connectivity (4- and 8-connected)** (robotics) → RO-05 (extend N106); every grid planner must choose which neighbour cells are reachable |
| (t,m,s)-nets | 208 | out-of-scope | low-discrepancy sampling theory; PA 5.6 dropped |
| (t,s)-sequences | 208 | out-of-scope | low-discrepancy sampling theory; PA 5.6 dropped |
| 1-complex | 133 | out-of-scope | algebraic topology (simplicial complexes) |
| 1-neighborhood | 221, 380 | add | **grid connectivity (4- and 8-connected)** (robotics) → RO-05 (extend N106); every grid planner must choose which neighbour cells are reachable |
| 2-neighborhood | 221 | add | **grid connectivity (4- and 8-connected)** (robotics) → RO-05 (extend N106); every grid planner must choose which neighbour cells are reachable |
| 3D triangles | 90–91 | taught | N71: triangle meshes |
| A ∗ algorithm | 37, 223, 811 | taught | N105: A* search |
| Abelian group (see commutative group) |  | index-noise | cross-reference to commutative group |
| acceleration vector | 408 | taught | N117: short mechanics section (F = ma) |
| acceleration-based control | 408 | taught | N106: navigation function used as feedback; acceleration form is a variant |
| accelerometer | 601 | taught | N83: accelerometer |
| accessibility (of a roadmap) | 251 | add | **roadmap properties: accessibility and connectivity** (robotics) → RO-05 (extend N111); defines what makes a roadmap usable for any start and goal |
| accessible system | 870, 909 | out-of-scope | nonlinear controllability theory; PA 15.5 dropped |
| accumulation point | 129 | out-of-scope | point-set topology |
| Ackerman function | 303, 304 | out-of-scope | complexity-theory function (inverse Ackermann bound) |
| action history | 400, 566 | taught | N77: information state = history of actions and readings |
| action sequence | 802 | taught | N9: open-loop plan as an action sequence |
| action trajectory | 400, 788 | taught | N9: open-loop plan in continuous time |
| active localization problem | 642 | taught | N180: active localization |
| active-passive decomposition | 343 | out-of-scope | closed-chain planning; PA 7.5 dropped |
| actuators | 793 | taught | N283: motors and actuators |
| Adams methods | 815 | out-of-scope | numerical-analysis detail beyond Euler and Runge-Kutta (plan§4 Numerical integration of ODEs) |
| adding integrators to a model | 742–744 | add | **double integrator and adding integrators** (control) → MA 06-calculus (extend State-space models); the standard first control model (position, velocity, acceleration input) |
| adjoint transition equation | 877 | out-of-scope | Pontryagin costate machinery; PA 15.8 dropped, Pontryagin named only in N116 |
| adjoint variables | 779, 875 | out-of-scope | Pontryagin costate machinery; PA 15.8 dropped, Pontryagin named only in N116 |
| admissible conﬁgurations | 334 | taught | N292: manipulation planning (transit and transfer) |
| aﬃne space | 170 | out-of-scope | algebraic-geometry machinery for closed chains; PA 4.15 dropped |
| aﬃne-in-control system (see aﬃne nonlinear control system) |  | index-noise | cross-reference to affine nonlinear control system |
| AGVs (see automated guided vehicles) |  | index-noise | cross-reference to automated guided vehicles |
| airport terminal | 376 | index-noise | example name |
| algebraic primitive | 87, 88, 130, 164–166 | out-of-scope | semi-algebraic models; PA 3.2 dropped |
| algebraic Riccati equation | 874 | taught | N205: steady (infinite-horizon) Riccati equation |
| algebraic set | 87 | out-of-scope | algebraic geometry; PA 3.2 dropped |
| algebraic variety (see variety) |  | index-noise | cross-reference to variety |
| alive states | 33, 55, 56, 427 | taught | N103: graph search bookkeeping (unvisited, alive, dead states) |
| Allen wrench | 701 | index-noise | example name |
| Alpha Puzzle | 6 | index-noise | puzzle name |
| alphabet | 586 | out-of-scope | automata theory; PA 11.5 dropped |
| Amato | 6 | index-noise | person name |
| ambient isotopy | 350 | out-of-scope | knot theory; PA 7.6 dropped |
| ambient space | 350 | out-of-scope | knot theory; PA 7.6 dropped |
| analytic function | 383 | taught | MA-061: analytic function (glossary G-197) |
| angular momentum (see moment of momentum) |  | index-noise | cross-reference to moment of momentum |
| angular velocity | 601, 727, 729, 756, 757, 760, 761 | taught | N84: angular velocity |
| annihilator | 897 | out-of-scope | differential geometry (codistributions); PA 15.11 dropped |
| antipodal points | 138 | out-of-scope | topology of RP3 (identifying antipodal points); PA 4.1/4.2 dropped |
| approximate cell decomposition | 246 | add | **quadtrees and multi-resolution grids** (robotics) → RO-05 (extend N106); standard way to grid a continuous space at varying resolution |
| approximate cover | 413–414 | out-of-scope | feedback-planning theory on cell covers; PA 8.6 dropped |
| approximate optimal motion planning | 359–360 | taught | N110: asymptotic optimality (RRT*) |
| approximation algorithm | 826–827 | out-of-scope | complexity theory (approximation algorithms) |
| Ariadne’s Clew algorithm | 227 | out-of-scope | research-only planner |
| arrangement | 307 | out-of-scope | computational geometry theory (arrangements) |
| Asimo | 14 | index-noise | robot name |
| assembly planning | 321–322 | out-of-scope | assembly sequencing by partitioning; computational-geometry research |
| asteroids game | 137 | index-noise | example name |
| asymptotic convergence to a goal | 399 | taught | N106: navigation function converges to the goal |
| asymptotic solution plan | 400 | taught | N106: feedback plan that reaches the goal in the limit |
| asymptotic stability | 863–864 | taught | plan§4 Stability of dynamical systems: new MA Note in the plan (equilibria, eigenvalues, Lyapunov) |
| atan2 | 99 | add | **atan2 (two-argument arctangent)** (maths) → MA 05-linear-algebra (extend Rigid-body transforms Note); every heading and IK computation needs the four-quadrant arctangent |
| atlas (see smooth structure) |  | index-noise | cross-reference to smooth structure |
| automated farming | 354 | index-noise | application name |
| automated guided vehicles | 325 | index-noise | application name |
| automotive assembly | 6 | index-noise | application name |
| autonomous diﬀerential equations | 387 | taught | plan§4 ODEs and vector fields: new MA Note in the plan |
| average cost-per-stage model | 522, 524 | taught | N27: average-reward setting |
| average dispersion | 246 | out-of-scope | dispersion theory; PA 5.5 dropped |
| averaging methods | 921 | out-of-scope | nonholonomic steering theory; PA 15.12 dropped |
| axioms of rationality | 481–482 | taught | N53: utility theory and rationality |
| axis-aligned bounding box | 211 | taught | N108: bounding-volume hierarchies |
| B-splines | 91 | add | **B-splines** (maths) → RO-15 (extend N202); standard smooth-path representation in planners and trajectory code |
| backprojection | 427, 503–505, 840–841, 852 | taught | N292: preimage planning |
| backprojection, in preimage planning | 696–700 | taught | N292: preimage planning |
| backward action space | 40 | taught | N105: backward search |
| backward P. Hall coordinates | 914, 916 | out-of-scope | Lie-algebra coordinates; PA 15.11 dropped |
| backward reachable set | 801 | taught | N197: reach-avoid / backward reachable values |
| backward search | 39–40, 219, 377, 696, 699, 703 | taught | N105: backward search |
| backward search, with backprojections | 518–519 | taught | N292: preimage planning with backprojections |
| backward state transition equation | 40, 50, 53 | taught | N105: backward search |
| backward system simulator | 816 | taught | N112: system simulator |
| backward value iteration | 45–48 | taught | N14: value iteration (cost-to-go) |
| backward value iteration, for reinforcement learning | 534–535 | taught | N14: value iteration, RL link |
| backward value iteration, for sequential games | 546–548 | taught | N54: sequential games on state spaces |
| backward value iteration, on a nondeterministic I-space | 637–638 | out-of-scope | worst-case set-valued information-space planning (PA 12.1); plan uses probabilistic belief (N268) |
| backward value iteration, on a probabilistic I-space | 638–639 | taught | N268: value iteration in belief space |
| backward value iteration, path-constrained | 852–853 | taught | N203: time scaling along a fixed path (phase plane) |
| backward value iteration, running time | 46 | taught | N103: algorithm cost, Big-O |
| backward value iteration, under diﬀerential constraints | 839–841 | taught | N112: lattice search under motion limits |
| backward value iteration, with average cost-per-stage | 527 | taught | N27: average-reward setting |
| backward value iteration, with discounted cost | 525–526 | taught | N14: discounted value iteration |
| backward value iteration, with nature and continuous spaces | 551–552 | taught | N106: DP with interpolation on continuous spaces |
| backward value iteration, with nondeterministic uncertainty | 508–514 | taught | N14: value iteration with nature |
| backward value iteration, with probabilistic uncertainty | 510–514 | taught | N14: value iteration with stochastic outcomes |
| bad bracket | 910 | out-of-scope | Lie-algebra machinery; PA 15.11 dropped |
| Balkcom-Mason curves | 886–888 | out-of-scope | research-only result (time-optimal differential-drive curves) |
| Balkcom-Mason drive | 887 | out-of-scope | research-only result (Balkcom-Mason drive) |
| Balkcom-Mason metric | 888 | out-of-scope | research-only result (Balkcom-Mason metric) |
| bang-bang approach | 853–855 | taught | N203: time-optimal (bang-bang) time scaling |
| Barraquand-Latombe nonholonomic planner | 828–832 | out-of-scope | research-only planner; modern successor Hybrid A* taught in N113 |
| base point (on a manifold) | 895 | out-of-scope | differential geometry (tangent spaces) |
| base point of a path | 142 | out-of-scope | algebraic topology (fundamental group) |
| basis | 382 | taught | MA-052: basis of a vector space |
| basis, of open sets | 130 | out-of-scope | point-set topology |
| Basu-Pollack-Roy roadmap algorithm | 298 | out-of-scope | exact algebraic planning; PA 6.4-6.9 dropped |
| Battle of the Sexes | 471 | index-noise | example name (game) |
| Battleship game | 626–627 | index-noise | example name (game) |
| Bayes’ rule | 443, 458, 578, 653 | taught | MA-018: Bayes' theorem |
| Bayesian classiﬁer | 456–458 | taught | ML-081: naive Bayes classifier |
| Bayesian classiﬁer, naive | 457 | taught | ML-081: naive Bayes classifier |
| behavioral strategies | 622 | out-of-scope | game theory for imperfect-information sequential games (beyond N54) |
| behaviors (see motion primitives) |  | index-noise | cross-reference to motion primitives |
| best-ﬁrst search | 38–39 | taught | N105: best-first search |
| bidirectional search | 40–41, 71, 227, 367, 638, 801, 819, 820, 827, 831, 835 | taught | N105: bidirectional search |
| bidirectional search, balanced | 235–236 | add | **bidirectional RRT (RRT-Connect)** (robotics) → RO-05 (extend N110); the default sampling planner in MoveIt/OMPL grows two trees |
| bidirectional search, for sampling-based planning | 220 | add | **bidirectional RRT (RRT-Connect)** (robotics) → RO-05 (extend N110); the default sampling planner in MoveIt/OMPL grows two trees |
| bijective sensor | 562 | out-of-scope | book-specific sensor-mapping taxonomy (LaValle ch.11) |
| bilinear programming | 473 | out-of-scope | game-theory solution method (nonzero-sum games) beyond N54 |
| binding constraints | 63 | out-of-scope | logic-based planning; PA 2.10-2.13 dropped |
| bitangent line | 262 | taught | N270: visibility graph (bitangent edges) |
| bitangent ray | 675 | out-of-scope | visibility pursuit-evasion; PA 12.6 dropped |
| bitmap | 91–92 | taught | N71: bitmaps as maps |
| black-box simulators | 815–816 | taught | N112: system simulator |
| Blum and Furst | 64 | index-noise | person names |
| Blum and Kozen | 660, 662 | index-noise | person names |
| body density | 753 | taught | N220: inertia of a rigid body |
| body frame | 94, 176, 178, 352, 366, 754, 758–760 | taught | N65: frames attached to a body |
| bond angle | 111 | out-of-scope | molecular biology (protein geometry); PA 7.6 dropped |
| bond length | 111 | out-of-scope | molecular biology (protein geometry); PA 7.6 dropped |
| Borel sets | 192 | out-of-scope | measure theory; PA 5.2 dropped |
| boundary grid point | 221 | out-of-scope | book-specific grid notation (neighbourhood bookkeeping) |
| boundary of a set | 129 | out-of-scope | point-set topology |
| boundary point | 129 | out-of-scope | point-set topology |
| boundary representation | 81 | taught | N71: polygons described by their boundary edges |
| boundary sensors | 601–602 | taught | N74: catalogue of sensor models (boundary) |
| bounded set | 132 | out-of-scope | point-set topology |
| bounded-acceleration model | 409 | taught | N112: planning with motion limits (speed/acceleration bounds) |
| bounded-velocity model | 409 | taught | N112: planning with motion limits (speed/acceleration bounds) |
| Boustrophedon decomposition | 354–357 | taught | N273: coverage planning (boustrophedon cells) |
| Brachistochrone curve | 762 | index-noise | historical example (calculus of variations) |
| bracket | 904 | out-of-scope | Lie brackets; PA 15.11 dropped |
| breadth-ﬁrst search | 35 | taught | N103: breadth-first search |
| bridge-test sampling | 243–244 | add | **narrow passages and PRM sampling strategies** (robotics) → RO-05 (extend N111); LaValle 5.6.2: uniform sampling misses narrow passages; bridge/Gaussian sampling fix it |
| broad-phase collision detection | 210 | taught | N108: broad and narrow phase |
| Brockett | 741, 917, 919 | index-noise | person name |
| Brockett’s condition | 864 | out-of-scope | nonlinear stabilisation theory; PA 15.5 dropped |
| Brockett’s system (see nonholonomic integrator) |  | index-noise | cross-reference to nonholonomic integrator |
| bug algorithms | 667–673 | taught | N107: bug algorithms |
| bug trap | 219 | index-noise | example name (bug-trap obstacle) |
| Bug1 strategy | 668–669 | taught | N107: bug algorithms |
| Bug2 strategy | 669–670 | taught | N107: bug algorithms |
| BVP (see two-point boundary value problem) |  | index-noise | cross-reference to two-point boundary value problem |
| C-space (see conﬁguration space) |  | index-noise | cross-reference to configuration space |
| caﬀeine | 17 | index-noise | example name (molecule) |
| calculus of variations | 440, 762–769, 922 | taught | N202: beginner calculus of variations (minimum jerk), plan§4 |
| Campbell-Baker-Hausdorﬀ-Dynkin formula | 913 | out-of-scope | Lie-algebra series; PA 15.11 dropped |
| candidate Lyapunov function | 866 | taught | N199: Lyapunov functions (plan§4 short section) |
| Candorcet paradox | 482 | out-of-scope | social-choice theory (different field) |
| Canny | 293 | index-noise | person name |
| Canny’s roadmap algorithm | 293–298, 307, 315, 324, 339 | out-of-scope | exact algebraic planning; PA 6.4-6.9 dropped |
| car pulling trailers | 13, 730–731 | add | **car with trailers (kinematic model)** (robotics) → RO-01 (extend N64); LaValle 13.1.2: truck-trailer kinematics used by tractor-trailer and tow robots |
| Caratheodory, solution sense of | 387 | out-of-scope | ODE existence theory (Caratheodory solutions) |
| card-counting strategies | 630 | index-noise | example name (card games) |
| Carnot-Caratheodory metric | 811 | out-of-scope | sub-Riemannian geometry |
| Cartesian product | 135 | add | **Cartesian product of spaces** (maths) → MA 02-probability (extend MA-010 sets); C-spaces of several bodies are products (circle x circle = torus) |
| carton folding | 347–350 | index-noise | example name (carton folding) |
| causal links | 63 | out-of-scope | logic-based planning; PA 2.10-2.13 dropped |
| CBHD formula | 913 | out-of-scope | Lie-algebra series; PA 15.11 dropped |
| cell decomposition | 251, 264–280, 650, 690 | taught | N270: vertical cell decomposition |
| cell decomposition, under diﬀerential constraints | 828 | out-of-scope | research-level planning under differential constraints |
| center of mass | 753 | taught | N295: centre of mass |
| Central Limit Theorem | 199 | taught | MA-033: central limit theorem |
| chain of integrators | 738–739 | add | **double integrator and adding integrators** (control) → MA 06-calculus (extend State-space models); the standard first control model (position, velocity, acceleration input) |
| chained-form system | 906, 920 | out-of-scope | chained-form steering; PA 15.12 dropped |
| change of coordinates | 391–393 | out-of-scope | manifold coordinate changes (differential geometry); frame changes taught in N65 |
| chart (see coordinate neighborhood) |  | index-noise | cross-reference to coordinate neighborhood |
| chasing a gap | 677 | out-of-scope | visibility pursuit-evasion; PA 12.6 dropped |
| Chazelle | 250 | index-noise | person name |
| Chen-Fliess series | 913–914 | out-of-scope | Lie-algebra series; PA 15.11 dropped |
| Chen-Fliess-Sussman equation | 914–916 | out-of-scope | Lie-algebra series; PA 15.11 dropped |
| chi-square test | 200 | taught | MA-045: chi-square distribution (used by KLD-sampling N95) |
| Chow-Rashevskii theorem | 908 | out-of-scope | nonlinear controllability theorem; PA 15.11 dropped, car controllability in plain words in N67 |
| Christoﬀel symbol | 770, 771 | out-of-scope | tensor form of Coriolis terms; N281 teaches c(q, qdot) directly |
| Church-Turing thesis | 19 | out-of-scope | computability theory (different field) |
| classiﬁcation rule | 456 | taught | ML-081: classification rule (Bayes classifier) |
| classiﬁer | 455–458 | taught | ML-081: classifier |
| cleared region | 688 | out-of-scope | visibility pursuit-evasion; PA 12.6 dropped |
| closed kinematic chains | 118, 167–180 | add | **closed chains and parallel robots** (robotics) → RB-01 (new Note); LaValle 4.4: loop-closure constraints of closed chains |
| closed kinematic chains, motion planning for | 337–347 | out-of-scope | closed-chain planning; PA 7.5 dropped |
| closed set | 128 | out-of-scope | point-set topology |
| closed system (in mechanics) | 746–747 | out-of-scope | physics definition for momentum conservation proofs; PA 13.10-13.11 dropped |
| closed-loop |  | index-noise | group heading; sub-entries judged separately |
| closed-loop, control law | 793 | taught | N117: feedback control law |
| closed-loop, plan (see feedback plan) | 370 | taught | N9: feedback (closed-loop) plan |
| closure of a set | 129, 195 | out-of-scope | point-set topology |
| closure space | 339 | out-of-scope | closed-chain planning; PA 7.5 dropped |
| codistribution | 897 | out-of-scope | differential geometry; PA 15.11 dropped |
| coherent models | 212 | out-of-scope | book-specific model property (collision-detection coherence) |
| Collins decomposition (see cylindrical algebraic decomposition) |  | index-noise | cross-reference to cylindrical algebraic decomposition |
| collision detection | 209–217 | taught | N108: collision detection |
| collision detection, broad-phase | 210 | taught | N108: broad phase |
| collision detection, checking a path segment | 214–217 | add | **checking a path segment for collision (edge resolution)** (robotics) → RO-05 (extend N108); every sampling planner must check whole edges, not only points |
| collision detection, hierarchical methods | 210–212 | taught | N108: bounding-volume hierarchies |
| collision detection, incremental methods | 212–214 | out-of-scope | incremental closest-feature algorithms; implementation detail inside collision libraries |
| collision detection, narrow-phase | 210 | taught | N108: narrow phase |
| collision detection, two-phase | 210 | taught | N108: broad and narrow phase |
| collision pairs | 156 | add | **self-collision checking (collision pairs)** (robotics) → RO-05 (extend N108); arms and humanoids must skip adjacent links and check the rest |
| collision-detection | 812–813 | taught | N108: collision detection |
| collocation | 857 | taught | N116: collocation |
| combinatorial motion planning | 249–307 | taught | N270: exact (combinatorial) roadmaps |
| combinatorial motion planning, cell decompositions | 264–280 | taught | N270: vertical cell decomposition |
| combinatorial motion planning, introductory concepts | 249–251 | taught | N270: exact roadmaps |
| combinatorial motion planning, polygonal case (see Canny’s roadmap algorithm see also cylindrical algebraic decomposition) | 251–264 | taught | N270: polygonal exact planning |
| combinatorial roadmaps | 237 | taught | N270: exact roadmaps |
| commutative group | 142, 898 | out-of-scope | group theory; PA 4.6 dropped |
| commutative ring | 170 | out-of-scope | abstract algebra (rings) |
| commutator | 898 | out-of-scope | Lie brackets; PA 15.11 dropped |
| commutator motion | 897–900, 911 | taught | N67: parallel-parking intuition for car controllability, in plain words |
| compass | 600, 647 | add | **magnetometer (compass) for heading** (robotics) → RO-03 (extend N83); IMUs and AHRS fuse a magnetometer for absolute heading |
| compatible coordinate neighborhoods | 393 | out-of-scope | differential geometry (atlases) |
| competitive ratio | 602, 672–673 | out-of-scope | online-algorithm analysis (proof technique) |
| complementary pair | 59 | out-of-scope | logic-based planning; PA 2.10-2.13 dropped |
| complete exclusion axiom | 70 | out-of-scope | logic-based planning; PA 2.10-2.13 dropped |
| completely integrable | 734, 893–894 | taught | N64: holonomic = integrable constraint |
| completeness |  | taught | N111: complete, resolution-complete, probabilistically complete |
| completeness, overview (see probabilistic completeness see also resolution completeness) | 185–186 | taught | N111: completeness notions |
| complex | 265–268 | out-of-scope | cell-complex topology |
| complexity class | 299 | taught | N103: NP-hard, PSPACE-hard |
| complexity of motion planning | 298–307 | taught | N103: why exact planning is hard |
| complexity of motion planning, lower bounds | 298–302 | taught | N103: hardness of planning |
| complexity of motion planning, upper bounds | 304–307 | out-of-scope | algorithm upper-bound proofs (Canny's algorithm) |
| compliant motions | 692–693, 697 | taught | N292: compliant motions in preimage planning |
| composition of funnels | 412–418, 702, 865 | out-of-scope | funnel composition; PA 8.6 dropped |
| compressed mode | 330 | out-of-scope | hybrid-systems example; PA 7.3 dropped |
| computational algebraic geometry | 280–298 | out-of-scope | computational algebraic geometry; PA 6.4-6.9 dropped |
| Conchoid of Nicomedes | 277, 308 | index-noise | example name (curve) |
| conditional Bayes’ risk | 453 | taught | N53: Bayesian decision making with observations |
| conditional Bayes’ rule | 443 | taught | N78: Bayes' theorem conditioned on past data |
| conditional expectation | 444 | add | **conditional expectation** (maths) → MA 02-probability; value functions and Bayes estimates are conditional expectations |
| conditional independence | 443 | taught | ML-082: conditional independence (glossary G-443) |
| conditional plan (see feedback plan) |  | index-noise | cross-reference to feedback plan |
| conditional probability | 443 | taught | MA-015: conditional probability |
| conﬁguration space | 127–180 | taught | N72: configuration space |
| conﬁguration space, obstacle (see obstacle region, C-space) |  | index-noise | cross-reference to obstacle region |
| conﬁguration space, of 2D rigid bodies | 145–148 | taught | N72: C-space of a 2D rigid body |
| conﬁguration space, of 3D rigid bodies | 148–154 | taught | N72: C-space of a 3D rigid body |
| conﬁguration space, of chains of bodies | 154–155 | taught | N72: C-space of chains |
| conﬁguration space, of trees of bodies | 155 | taught | N69: kinematic trees |
| conﬁguration space, velocity constraints on | 716–735 | taught | N64: velocity (nonholonomic) constraints |
| conformations | 110, 351 | out-of-scope | molecular biology; PA 7.6 dropped |
| connected space | 139 | out-of-scope | point-set topology |
| connectivity-preserving roadmap | 251 | add | **roadmap properties: accessibility and connectivity** (robotics) → RO-05 (extend N111); defines what makes a roadmap usable for any start and goal |
| connector in a roadmap | 241 | taught | N111: connecting samples in a roadmap |
| conservative approximations | 593–595 | out-of-scope | approximations of nondeterministic information spaces (research-level) |
| conservative system | 766 | taught | N281: energy-conserving systems in Lagrangian mechanics |
| constant vector ﬁeld | 384 | taught | plan§4 ODEs and vector fields: new MA Note in the plan |
| constant-sum game | 492 | taught | N54: zero-sum (constant-sum) games |
| contaminated region | 688 | out-of-scope | visibility pursuit-evasion; PA 12.6 dropped |
| continuous Dijkstra paradigm | 357 | out-of-scope | exact shortest-path computational geometry |
| continuous function | 131 | add | **continuity of a function** (maths) → MA 06-calculus; paths, C-space and trajectory smoothness rest on continuity |
| continuous-steering car | 743–744 | add | **double integrator and adding integrators** (control) → MA 06-calculus (extend State-space models); the standard first control model (position, velocity, acceleration input) |
| contractible space | 144 | out-of-scope | algebraic topology |
| control system | 715, 793 | taught | plan§4 State-space models: new MA Note in the plan |
| control-aﬃne system | 741, 890–892 | add | **control-affine systems (drift and control vector fields)** (control) → RO-06 (extend N124); the form x' = f(x) + g(x)u that feedback linearisation and CBFs assume |
| controllability matrix | 868 | taught | N204: controllability rank test |
| controllability of a system | 867–870 | taught | N204: controllability |
| controllability of a system, linear case | 868 | taught | N204: controllability of linear systems |
| controllability of a system, small-time local (see small-time local controllability) |  | index-noise | cross-reference to small-time local controllability |
| controlled Markov process | 498 | taught | N7: Markov decision process |
| convex hull | 211, 388 | taught | plan§4 Convex hull: short section added to MA-067 |
| convex polygon | 82–84 | taught | N71: convex polygons from half-planes |
| convex set | 82 | taught | MA-067: convex sets |
| convolution | 158 | taught | DL-042: convolution (Minkowski sum as convolution, N73) |
| cooperative game theory | 490 | out-of-scope | cooperative game theory (different field) |
| coordinate neighborhood | 391 | out-of-scope | differential geometry (charts) |
| coordinates | 391 | out-of-scope | manifold coordinates (differential geometry) |
| coordination space | 323 | taught | N271: decoupled multi-robot planning (coordination space) |
| Coriolis matrix | 770 | taught | N281: Coriolis terms in the manipulator equation |
| cost functional | 44, 359, 363, 501, 523, 625, 839 | taught | N116: trajectory-optimisation cost |
| cost functional, approximating | 424 | taught | N106: cost approximated by interpolation in DP |
| cost functional, quadratic | 874 | taught | N205: quadratic cost (LQR) |
| cost-based learning (see reinforcement learning) |  | index-noise | cross-reference to reinforcement learning |
| cost-to-come | 36, 48–50, 799 | taught | N104: cost-to-come in Dijkstra |
| cost-to-come iteration (see forward value iteration) |  | index-noise | cross-reference to forward value iteration |
| cost-to-go (see stationary cost-to-go function) | 37, 45–46, 361, 373, 375–377, 379, 380, 401, 405–407, 412, 419, 420, 422, 424–429, 551, 811, 835, 836, 839, 840, 852, 853 | taught | N14: cost-to-go |
| cost-to-go iteration (see backward value iteration) |  | index-noise | cross-reference to backward value iteration |
| Coulomb friction | 693 | taught | N288: Coulomb friction |
| counting measure | 193 | out-of-scope | measure theory; PA 5.2 dropped |
| covariance matrix | 596 | taught | MA-073: covariance matrix of a multivariate normal |
| cover of a set | 413 | out-of-scope | funnel/cover theory for feedback planning; PA 8.6 dropped |
| cover of a set, approximate | 414 | out-of-scope | funnel/cover theory for feedback planning; PA 8.6 dropped |
| coverage planning | 354–357 | taught | N273: coverage planning |
| Coxeter-Freudenthal-Kuhn triangulation | 421 | out-of-scope | simplex-interpolation implementation detail; DP with interpolation taught in N106 |
| critical curves | 276 | out-of-scope | exact algebraic planning (Canny); PA 6.x dropped |
| critical gap events | 674–675 | out-of-scope | visibility pursuit-evasion; PA 12.6 dropped |
| critical point of a function | 295, 410 | taught | MA-065: critical (stationary) points of a function |
| cube complex | 325–327 | out-of-scope | cube-complex topology for multi-robot coordination (research-level) |
| cubical partition | 828 | out-of-scope | research-level cell decompositions under differential constraints |
| CW-complex | 265 | out-of-scope | algebraic topology (CW complexes) |
| cycloid function | 762 | index-noise | example name (curve) |
| cylinder over a cell | 270, 276, 290 | out-of-scope | cylindrical algebraic decomposition; PA 6.x dropped |
| cylindrical algebraic decomposition | 286–293, 315, 324 | out-of-scope | cylindrical algebraic decomposition; PA 6.x dropped |
| cylindrical algebraic decomposition, for motion planning | 292–293 | out-of-scope | cylindrical algebraic decomposition; PA 6.x dropped |
| cylindrical decomposition | 269–270 | out-of-scope | generalisation of vertical decomposition for exact algebraic planning; PA 6.x dropped |
| cylindrical joint | 105 | taught | N70: joint types |
| D ∗ algorithm (see Stentz’s algorithm) |  | index-noise | cross-reference to Stentz's algorithm |
| D’Alembert | 776 | out-of-scope | analytical-mechanics principle (d'Alembert); PA 13.10 dropped |
| Davenport-Schinzel sequence | 302–304 | out-of-scope | combinatorics used for complexity bounds (proof technique) |
| Davis-Putnam procedure | 69 | out-of-scope | SAT solving / logic-based planning; PA 2.10-2.13 dropped |
| dead states | 33, 34, 37, 427 | taught | N103: graph search bookkeeping (dead states) |
| decision maker | 4, 437 | taught | N53: decision maker in decision theory |
| decision problem | 283 | taught | N103: complexity of decision problems |
| decision theory | 437 | taught | N53: decision theory |
| decision vertex (in a game tree) | 536 | taught | N54: game trees |
| decision-theoretic learning (see reinforcement learning) |  | index-noise | cross-reference to reinforcement learning |
| decoupled planning | 320, 841–855 | taught | N271: decoupled planning: path first, then timing |
| decoupling vector ﬁelds | 849, 921 | out-of-scope | research-level trajectory method (decoupling vector fields) |
| deformation retract | 260 | out-of-scope | algebraic topology (deformation retract) |
| degrees of freedom | 95 | taught | N72: degrees of freedom |
| delayed-observation sensor | 564 | out-of-scope | book-specific sensor taxonomy; delays taught in N136 |
| Denavit-Hartenberg parameters | 103–106, 110, 149, 154, 167, 179 | taught | N69: Denavit-Hartenberg parameters |
| dense sequence | 195, 798 | out-of-scope | dense-sampling theory; PA 5.5-5.6 dropped |
| dense set | 195 | out-of-scope | point-set topology (dense sets) |
| dependent events | 443 | taught | MA-016: dependent events |
| depth-ﬁrst search | 36 | taught | N103: depth-first search |
| depth-mapping sensors | 603–605 | taught | N90: depth cameras and depth sensing |
| derivation (on a manifold) | 396 | out-of-scope | differential geometry (derivations) |
| derived information space | 571–581, 592–598 | out-of-scope | book-specific framework for compressing histories; plan uses belief (N77) |
| derived information space, for continuous time | 597–598 | out-of-scope | book-specific framework for compressing histories; plan uses belief (N77) |
| derived information transition equation | 573 | out-of-scope | book-specific framework for compressing histories; plan uses belief (N77) |
| determining the environment | 656–660 | out-of-scope | sensorless environment identification (research-level, PA 12.3) |
| deterministic ﬁnite automaton | 31, 585 | out-of-scope | automata theory; PA 11.5 dropped |
| deterministic ﬁnite automaton, language | 31 | out-of-scope | automata theory; PA 11.5 dropped |
| deterministic plan | 538, 545, 621 | taught | N9: plan without randomisation |
| DFA (see deterministic ﬁnite automaton) |  | index-noise | cross-reference to deterministic finite automaton |
| DH parameters (see Denavit-Hartenberg parameters) |  | index-noise | cross-reference to Denavit-Hartenberg parameters |
| Dial’s algorithm | 380 | out-of-scope | bucket-queue variant of Dijkstra (implementation detail) |
| diameter function | 702 | out-of-scope | parts-orienting research (diameter function) |
| dielectric constant | 352 | out-of-scope | molecular physics (drug design) |
| diﬀeomorphic spaces | 385 | out-of-scope | differential geometry (diffeomorphisms) |
| diﬀeomorphism | 385 | out-of-scope | differential geometry (diffeomorphisms) |
| diﬀerentiable manifold (see smooth manifold) |  | index-noise | cross-reference to smooth manifold |
| diﬀerentiable structure (see smooth structure) |  | index-noise | cross-reference to smooth structure |
| diﬀerential constraints (see diﬀerential models) |  | index-noise | cross-reference to differential models |
| diﬀerential drive | 908 | taught | N64: differential drive |
| diﬀerential drive, Balkcom-Mason (see Balkcom-Mason drive) |  | index-noise | cross-reference to Balkcom-Mason drive |
| diﬀerential drive, model | 726–729 | taught | N64: differential-drive model |
| diﬀerential drive, second-order | 744 | add | **double integrator and adding integrators** (control) → MA 06-calculus (extend State-space models); the standard first control model (position, velocity, acceleration input) |
| diﬀerential drive, showing it is nonholonomic | 902 | out-of-scope | Lie-bracket proof; plain-words nonholonomy taught in N64 |
| diﬀerential game | 782–783 | out-of-scope | differential games; PA 13.12 dropped |
| diﬀerential game, against nature | 780 | out-of-scope | differential games; PA 13.12 dropped |
| diﬀerential game, pursuit-evasion | 782 | out-of-scope | differential pursuit-evasion games; PA 13.12 dropped |
| diﬀerential inclusion | 388, 780 | out-of-scope | differential inclusions (advanced ODE theory) |
| diﬀerential models | 715–783 | taught | N64: velocity constraints and motion models |
| diﬀerential models, conversion from implicit to parametric | 720–722 | taught | N64: from velocity constraints to a velocity model |
| diﬀerential models, implicit representation | 716–718 | taught | N64: implicit (constraint) form |
| diﬀerential models, parametric representation | 718–720 | taught | plan§4 State-space models: x' = f(x, u) |
| diﬀerential rotations | 755–756 | taught | N84: small rotations / angular velocity |
| diﬀerentially ﬂat systems | 921 | taught | N223: differential flatness |
| digital actor | 12 | index-noise | application name (animation) |
| Dijkstra’s algorithm | 27, 36–37, 55–57, 377, 378, 380, 403, 405, 407, 426, 428, 552, 663, 666, 823, 840, 852 | taught | N104: Dijkstra's algorithm |
| Dijkstra’s algorithm, extension of to continuous spaces | 426–429 | taught | N106: Dijkstra-like DP on continuous spaces with interpolation |
| Dijkstra’s algorithm, with nondeterministic uncertainty | 519–521 | out-of-scope | worst-case set-valued planning (PA 12.1); plan uses probabilistic outcomes (N14) |
| Dijkstra’s algorithm, with probabilistic uncertainty | 521 | taught | N14: value iteration with stochastic outcomes |
| dimension |  | index-noise | group heading; sub-entries judged separately |
| dimension, of a manifold | 134 | taught | N72: dimension of C-space = degrees of freedom |
| dimension, of a vector space | 383 | taught | MA-052: dimension of a vector space (basis) |
| directed roadmap | 315 | out-of-scope | research-level roadmap for time-varying problems |
| Dirichlet boundary condition | 412 | add | **harmonic potential fields and Laplace's equation** (robotics) → RO-05 (extend N109); potential fields with no local minima come from solving Laplace's equation with fixed boundary values |
| disconnection proof | 246 | out-of-scope | proof technique |
| discount factor | 523 | taught | N8: discount factor |
| discounted cost model | 522–524 | taught | N8: discounted cost |
| discrepancy | 205–209, 811–812 | out-of-scope | low-discrepancy theory; PA 5.6 dropped |
| discrepancy, range space | 206 | out-of-scope | low-discrepancy theory; PA 5.6 dropped |
| discrepancy, relation to dispersion | 207 | out-of-scope | low-discrepancy theory; PA 5.6 dropped |
| discrete feasible planning | 29 | taught | N103: discrete feasible planning as graph search |
| discrete-time model | 801–808 | taught | plan§4 State-space models: discrete-time models by zero-order hold |
| discretization of C | 221 | taught | N106: grids over C-space |
| dispersion | 201–205, 419, 811–812 | out-of-scope | dispersion theory; PA 5.5 dropped |
| dispersion, relation to discrepancy | 207 | out-of-scope | dispersion theory; PA 5.5 dropped |
| distance between sets | 209–210 | taught | N108: distance between robot and obstacles |
| distance function | 209 | taught | N108: distance computation in collision checking |
| distribution (of vector ﬁelds) | 894–897 | out-of-scope | distributions of vector fields; PA 15.11 dropped |
| distribution (of vector ﬁelds), regular | 895 | out-of-scope | distributions of vector fields; PA 15.11 dropped |
| distribution (of vector ﬁelds), singular | 895–896 | out-of-scope | distributions of vector fields; PA 15.11 dropped |
| disturbed odd/even sensor | 564 | out-of-scope | book-specific sensor taxonomy |
| disturbed sign sensor | 564 | out-of-scope | book-specific sensor taxonomy |
| DM (see decision maker) |  | index-noise | cross-reference to decision maker |
| domain of attraction | 864–865 | add | **region of attraction** (control) → MA 06-calculus (extend Stability of dynamical systems); tells from which states a controller still reaches its goal |
| dominated action | 440 | taught | N53: dominated actions (Pareto) |
| dominated plan | 364 | taught | N53: Pareto-optimal plans |
| Donald | 627, 697 | index-noise | person name |
| double integrator | 737–738, 744, 747, 755, 790, 792, 796 | add | **double integrator and adding integrators** (control) → MA 06-calculus (extend State-space models); the standard first control model (position, velocity, acceleration input) |
| double integrator, lattice | 820–828 | taught | N114: state lattice |
| double integrator, optimal planning for | 877–878 | taught | N203: time-optimal (bang-bang) motion |
| doubly connected edge list | 86, 252, 253, 258 | out-of-scope | computational-geometry data structure |
| drift | 739, 741, 793, 891 | add | **control-affine systems (drift and control vector fields)** (control) → RO-06 (extend N124); drift vs control vector fields; the form feedback linearisation and CBFs assume |
| driftless | 741, 793 | add | **control-affine systems (drift and control vector fields)** (control) → RO-06 (extend N124); drift vs control vector fields; the form feedback linearisation and CBFs assume |
| driftless system | 739, 891 | add | **control-affine systems (drift and control vector fields)** (control) → RO-06 (extend N124); drift vs control vector fields; the form feedback linearisation and CBFs assume |
| driftless system, controllability | 908–909 | out-of-scope | nonlinear controllability theory; PA 15.5 dropped |
| drug design | 15, 350–353 | out-of-scope | drug design (different field) |
| Dubins car | 725, 782, 794, 796, 800, 803, 806, 811, 817, 828, 829, 831, 832, 835, 838, 842, 844, 845, 848 | taught | N64: Dubins car |
| Dubins car, plan-and-transform approach | 843–844 | out-of-scope | research-level planning method |
| Dubins car, reachability tree of | 803–804 | taught | N112: reachable sets |
| Dubins curves | 880–883 | taught | N112: Dubins curves |
| Dubins metric | 883 | out-of-scope | research-level metric |
| dynamic constraints | 891 | taught | N112: kinodynamic planning |
| dynamic game (see diﬀerential game) |  | index-noise | cross-reference to differential game |
| dynamic programming | 27 | taught | N14: dynamic programming |
| dynamic programming, applied to steering | 922 | out-of-scope | nonholonomic steering by DP; PA 15.12 dropped |
| dynamic programming, continuous-time (see Dijkstra’s algorithm see also Hamilton-Jacobi-Bellman equation see also value iteration) | 870–879 | taught | N205: HJB (continuous-time DP) |
| dynamics |  | index-noise | group heading; sub-entries judged separately |
| dynamics, of a particle | 747–752 | taught | N117: short mechanics section (F = ma) |
| dynamics, of a rigid body | 753–762 | taught | N220: rigid-body dynamics in 3D |
| dynamics, of a set of particles | 752–753 | taught | N220: centre of mass of many particles |
| dynamics, of a two-link manipulator | 771–773 | taught | N281: 2-link arm dynamics |
| dynamics, of chains of bodies | 769–773 | taught | N282: dynamics of chains |
| dynamics, of constrained bodies | 774–777 | taught | N289: constraint forces as Lagrange multipliers |
| dynamics, with nonconservative forces | 777 | taught | N281: torques/forces outside the potential |
| eﬃcient algorithm | 299, 302, 304 | taught | N103: polynomial-time algorithms |
| elongated mode | 330 | out-of-scope | hybrid-systems example; PA 7.3 dropped |
| EM algorithm | 682–684 | taught | MA-074: expectation-maximization |
| embedding of a manifold | 134 | out-of-scope | differential geometry (embeddings) |
| energy function | 347, 350, 352 | out-of-scope | molecular energy (different field) |
| equilibrium point of a vector ﬁeld | 862 | taught | plan§4 Stability of dynamical systems: equilibria |
| Erdmann | 696, 699 | index-noise | person name |
| error detection and recovery (EDR) | 697 | out-of-scope | research-level manipulation planning (EDR) |
| Euclidean metric | 187 | taught | MA-049: Euclidean distance |
| Euclidean motion model | 361–362 | taught | N64: robot that can move in any direction (holonomic) |
| Euclidean norm | 188 | taught | MA-049: Euclidean norm (magnitude) |
| Euclidean shortest paths | 357–358 | taught | N270: shortest-path roadmap (visibility graph) |
| Euler angles | 122 | taught | plan§4 3D rotations: Euler angles and quaternions: new MA Note in the plan |
| Euler approximation | 423 | taught | plan§4 Numerical integration of ODEs: Euler step |
| Euler integration (see numerical integration, Euler) |  | index-noise | cross-reference to numerical integration |
| Euler-Lagrange equation | 765–770, 879, 891, 918, 922 | taught | N281: Euler-Lagrange equation |
| Euler-Lagrange equation, with conservative forces | 777 | taught | N281: Euler-Lagrange equation |
| event space | 442 | taught | MA-010: events and sample space |
| exact motion planning (see combinatorial motion planning) |  | index-noise | cross-reference to combinatorial motion planning |
| exit face | 403 | out-of-scope | cell-complex feedback-planning detail; PA 8.6 dropped |
| exotic R 4 | 393 | out-of-scope | differential topology |
| expansive-space planner | 227–228 | out-of-scope | research-only planner (expansive spaces) |
| expectation of a random variable | 444 | taught | MA-012: expected value |
| expected-case analysis | 449, 508, 570 | taught | N53: expected-case vs worst-case decisions |
| exploration vs. exploitation | 530 | taught | N1: exploration vs exploitation |
| exponential map | 912–913 | taught | plan§4 Axis-angle, exponential and log maps of rotations: exponential map at beginner level; Lie-algebra form out of scope |
| exponentially stable system | 864 | add | **exponential vs asymptotic stability** (control) → MA 06-calculus (extend Stability of dynamical systems); how fast errors die out is how controllers are compared |
| EXPTIME | 299 | out-of-scope | complexity theory (EXPTIME) |
| extended Kalman ﬁlter | 617, 655 | taught | N81: extended Kalman filter |
| extended system | 910 | out-of-scope | nonholonomic steering construct; PA 15.12 dropped |
| exterior point | 129 | out-of-scope | point-set topology |
| extremal function | 764 | out-of-scope | calculus-of-variations formalism beyond beginner minimum jerk (N202); PA 13.9 dropped |
| falling particle | 767–768 | index-noise | example name |
| fast Fourier transforms | 424 | add | **Fourier transform, frequency spectrum and FFT** (maths) → MA 06-calculus; signals, sensor noise spectra and frequency response are read in the frequency domain |
| Faure sequence | 208 | out-of-scope | low-discrepancy theory; PA 5.6 dropped |
| feasible planning |  | index-noise | group heading; sub-entries judged separately |
| feasible planning, discrete | 29 | taught | N103: discrete feasible planning |
| feasible planning, with feedback | 373–374 | taught | N9: feedback plan that reaches the goal |
| feasible space (for closure constraints) | 339 | out-of-scope | closed-chain planning; PA 7.5 dropped |
| feature space | 456 | taught | ML-089: feature space |
| feature vector | 456, 457 | taught | MA-048: feature vector |
| feedback control law (see feedback plan) |  | index-noise | cross-reference to feedback plan |
| feedback motion planning |  | index-noise | group heading; sub-entries judged separately |
| feedback motion planning, complete, optimal | 405–407 | taught | N106: optimal navigation functions / wavefront on continuous spaces |
| feedback motion planning, complete, some dynamics | 407–412 | taught | N106: navigation functions |
| feedback motion planning, deﬁnitions | 398–402 | taught | N106: feedback motion planning |
| feedback motion planning, motivation | 369–371 | taught | N106: feedback motion planning |
| feedback motion planning, sampling-based | 412–429 | out-of-scope | sampling-based funnel composition; PA 8.6 dropped |
| feedback motion planning, under diﬀerential constraints | 837–841 | out-of-scope | research-level feedback planning under differential constraints |
| feedback plan | 372–373, 505–508 | taught | N9: feedback plan |
| feedback plan, cost of | 507–508 | taught | N14: cost of a feedback plan (value) |
| feedback plan, graph representation of | 507 | taught | N9: feedback plan over a state graph |
| feedback plan, information feedback | 568–569 | taught | N153: policies over information/belief space |
| feedback plan, over a cover | 414–416 | out-of-scope | funnel composition; PA 8.6 dropped |
| feedback plan, sensor feedback | 581 | taught | N153: sensor-feedback policies |
| feedback planning |  | index-noise | group heading; sub-entries judged separately |
| feedback planning, continuous (see feedback motion planning) |  | index-noise | cross-reference to feedback motion planning |
| feedback planning, discrete | 371–381 | taught | N106: discrete feedback planning (wavefront, value iteration) |
| feedback policy (see feedback plan) |  | index-noise | cross-reference to feedback plan |
| feedback stabilization | 862 | taught | N204: stabilising state feedback |
| ﬁber over a base | 895 | out-of-scope | differential geometry (fibre bundles) |
| ﬁctitious action variable | 911 | out-of-scope | nonholonomic steering construct; PA 15.12 dropped |
| ﬁeld | 168–169 | out-of-scope | abstract algebra (fields) |
| ﬁeld, algebraically closed | 287 | out-of-scope | abstract algebra (fields) |
| Filipov, solution sense of | 388, 398 | out-of-scope | ODE solution theory (Filippov) |
| ﬁne motion planning (see manipulation planning) |  | index-noise | cross-reference to manipulation planning |
| ﬁnite state machine | 31 | taught | N130: finite state machines |
| ﬁretruck | 731 | index-noise | example name (vehicle model) |
| ﬁrst-order controllable systems | 919–920 | out-of-scope | nonholonomic control theory; PA 15.10 dropped |
| ﬁrst-order theory of the reals | 283 | out-of-scope | mathematical logic (Tarski) |
| ﬁxed point of a vector ﬁeld | 862 | taught | plan§4 Stability of dynamical systems: equilibria |
| ﬁxed-path coordination | 323–325 | taught | N271: decoupled multi-robot coordination |
| ﬁxed-roadmap coordination | 325–327 | taught | N271: decoupled multi-robot coordination |
| ﬂashlight example | 59–61 | index-noise | example name |
| ﬂashlight example, Boolean expression for | 70 | index-noise | example name |
| ﬂashlight example, planning graph of | 67 | index-noise | example name |
| ﬂashlight sensor | 691 | out-of-scope | book-specific sensor model |
| ﬂat cylinder | 136 | taught | N72: C-space shapes in plain words |
| ﬂat outputs | 921 | taught | N223: flat outputs |
| ﬂat torus | 137 | taught | N72: torus as a C-space |
| ﬂexible materials | 121 | out-of-scope | deformable-object geometric modelling (research-level) |
| ﬂying an airplane | 732–733 | index-noise | example name |
| folding problems | 347–354 | out-of-scope | protein folding; PA 7.6 dropped |
| foliation | 799, 893 | out-of-scope | differential geometry (foliations) |
| force | 747, 748, 751–755, 760, 761, 766, 767 | taught | N117: force (short mechanics section) |
| force, resultant | 748, 752 | taught | N117: net force |
| force sensor | 601 | add | **force/torque sensors (strain gauges)** (robotics) → RB-02 (extend N286); force control and contact-rich tasks read a wrist force-torque sensor |
| formal Lie algebra | 912–913 | out-of-scope | Lie algebra; PA 15.11 dropped |
| forward projection | 501, 799 | taught | N78: prediction step (forward projection of belief) |
| forward projection, diﬀerential | 781 | taught | N112: reachable sets |
| forward projection, nondeterministic | 501–502 | taught | N112: reachable sets |
| forward projection, probabilistic | 502–503 | taught | N78: prediction step |
| forward projection, under a ﬁxed plan | 506 | taught | N78: prediction step |
| forward search | 33–39 | taught | N103: forward search |
| forward search, A ∗ algorithm | 37–38 | taught | N105: A* search |
| forward search, best ﬁrst | 38–39 | taught | N105: best-first search |
| forward search, breadth-ﬁrst | 35 | taught | N103: breadth-first search |
| forward search, depth-ﬁrst | 36 | taught | N103: depth-first search |
| forward search, Dijkstra’s algorithm | 36–37 | taught | N104: Dijkstra's algorithm |
| forward search, general, discrete | 33–35 | taught | N103: general forward search |
| forward search, iterative deepening | 39 | taught | N105: iterative deepening |
| forward value iteration | 48–50 | taught | N14: value iteration (forward form) |
| four-bar mechanism | 175 | add | **closed chains and parallel robots** (robotics) → RB-01 (new Note); four-bar mechanism, the basic closed chain (LaValle 4.4) |
| frame axiom | 70 | out-of-scope | logic-based planning; PA 2.10-2.13 dropped |
| Fraunhofer Chalmers Centre | 8 | index-noise | organisation name |
| Frazzoli | 809 | index-noise | person name |
| free space | 156 | taught | N73: free space |
| free variables | 282 | out-of-scope | mathematical logic |
| frequentist | 483–484 | taught | MA-036: frequentist interpretation |
| frequentist risk | 484 | out-of-scope | statistical decision theory detail (frequentist risk) beyond N53 |
| friction cone | 693 | taught | N288: friction cone |
| Frobenius theorem | 901–902 | out-of-scope | Frobenius theorem; PA 15.11 dropped |
| frontier set | 427, 520, 840 | taught | N104: search frontier (priority queue) |
| fully actuated system | 793 | taught | N221: fully actuated vs underactuated |
| function space | 383, 590, 763 | out-of-scope | functional analysis |
| functional | 763 | taught | N116: cost over a whole trajectory |
| functional, shortest-path | 764 | out-of-scope | calculus-of-variations formalism; PA 13.9 dropped |
| fundamental group | 142–144 | out-of-scope | algebraic topology (fundamental group); PA 4.x topology dropped |
| fundamental group, higher order | 144 | out-of-scope | algebraic topology (fundamental group); PA 4.x topology dropped |
| fundamental group, of a simply connected space | 142 | out-of-scope | algebraic topology (fundamental group); PA 4.x topology dropped |
| fundamental group, of RP 2 | 143–144 | out-of-scope | algebraic topology (fundamental group); PA 4.x topology dropped |
| fundamental group, of S 1 | 142–143 | out-of-scope | algebraic topology (fundamental group); PA 4.x topology dropped |
| fundamental group, of T n | 143 | out-of-scope | algebraic topology (fundamental group); PA 4.x topology dropped |
| Fundamental Lemma of the Calculus of Variations | 765 | out-of-scope | proof lemma (calculus of variations) |
| Gabriely and Rimon | 355 | index-noise | person names |
| gain constant | 408 | taught | N117: feedback gains |
| game |  | index-noise | group heading; sub-entries judged separately |
| game, alternating-play model | 538, 621 | taught | N54: sequential games |
| game, extensive form | 536 | taught | N54: game trees (extensive form) |
| game, ladder-nested | 623 | out-of-scope | game information-model variant beyond N54 |
| game, normal form | 536 | taught | N54: matrix games (normal form) |
| game, open-loop model | 539, 621 | out-of-scope | game information-model variant beyond N54 |
| game, sequential (see sequential game) |  | index-noise | cross-reference to sequential game |
| game, stage-by-stage model | 538, 621 | out-of-scope | game information-model variant beyond N54 |
| game, unusual information model (see game theory) | 621 | index-noise | cross-reference to game theory |
| game against nature | 446–459 | taught | N53: game against nature |
| game against nature, sequential | 496–508, 551–556 | taught | N14: value iteration with nature |
| game graph | 544 | taught | N54: game graph |
| game theory | 437, 459–476, 489–490, 536–551, 619–627 | taught | N54: game theory |
| game theory, information spaces in | 619–627 | out-of-scope | information spaces in games (research-level) |
| game theory, nonzero-sum (see nonzero-sum game) |  | index-noise | cross-reference to nonzero-sum game |
| game theory, sequential (see sequential game) |  | index-noise | cross-reference to sequential game |
| game theory, zero-sum (see zero-sum game) |  | index-noise | cross-reference to zero-sum game |
| game tree | 536–544 | taught | N54: game trees |
| game tree, information space over | 619–623 | out-of-scope | information spaces in games (research-level) |
| gap navigation tree | 673–679 | out-of-scope | research-level sensor-based navigation (gap navigation trees, PA 12.3) |
| gap sensor | 604 | out-of-scope | book-specific sensor model |
| gap theorems | 287 | out-of-scope | algebra (gap theorems) |
| garage conﬁguration | 325 | index-noise | example name |
| Gaussian sampling | 243 | add | **narrow passages and PRM sampling strategies** (robotics) → RO-05 (extend N111); LaValle 5.6.2: uniform sampling misses narrow passages; bridge/Gaussian sampling fix it |
| Geiger counter sensor | 602 | index-noise | example sensor name (Geiger counter) |
| general linear group | 145 | out-of-scope | group theory notation GL(n); plan dropped PA 4.6 (SE(2)/SE(3) taught as matrices) |
| general position | 255, 675 | out-of-scope | computational-geometry proof assumption |
| generalized coordinates | 767 | taught | N281: generalized coordinates q in L(q, q_dot) |
| generalized cylinder | 92 | out-of-scope | geometric-modeling primitive used only in CAD/graphics |
| generalized damper model | 693 | out-of-scope | research model from compliant-motion preimage planning (LaValle ch.12) |
| generalized forces | 768, 769, 776 | taught | N281: generalized forces in the Euler-Lagrange equation |
| generalized momentum | 779 | out-of-scope | Hamiltonian mechanics; plan dropped PA 13.11 |
| generalized Voronoi diagram (see maximumclearance roadmap) |  | index-noise | cross-reference to maximum-clearance roadmap |
| generator of a lattice | 204 | out-of-scope | lattice sampling theory (dropped PA 5.6, low-discrepancy) |
| geodesics | 766, 810 | out-of-scope | differential-geometry term (sub-Riemannian geodesics) |
| geometric modeling | 81–92 | taught | N71: geometric representations of obstacles |
| Gilbert-Johnson-Keerthi algorithm | 244 | out-of-scope | GJK is an algorithm inside collision libraries (LaValle 5.3 names it); N108 teaches collision checking at usage level |
| gingerbread face | 87, 284, 291 | index-noise | example shape name |
| globally asymptotically stable | 865 | taught | N199: global asymptotic stability via Lyapunov functions |
| globally positive deﬁnite | 866 | taught | N199: positive definite Lyapunov function |
| globally randomized plan | 622 | out-of-scope | randomized plans in sensing games; research-only |
| GNT (see gap navigation tree) |  | index-noise | cross-reference to gap navigation tree |
| goal recognizability | 582, 696 | out-of-scope | preimage-planning theory (LaValle ch.12); research-only |
| goal sensor | 667 | index-noise | example virtual sensor |
| Goldberg and Mason | 701 | index-noise | person names |
| golden ratio | 209 | out-of-scope | number trivia used in a low-discrepancy sequence |
| Goursat normal form | 920 | out-of-scope | nonholonomic control theory normal form; plan dropped PA 15.10 |
| Grübler’s formula | 180 | taught | N70: Grübler's count of degrees of freedom |
| gradient descent | 375, 401, 410 | taught | ML-056: gradient descent |
| graph search |  | index-noise | group heading; sub-entries judged separately |
| graph search, on an information space | 638 | taught | N153: planning in belief/information space |
| grasped conﬁgurations | 334 | taught | N292: grasped configurations in manipulation planning (transit/transfer) |
| gray-scale map | 92, 665 | taught | N97: gray-scale/elevation-style maps |
| great circle | 190 | taught | plan§4: 3D rotations: Euler angles and quaternions: distances on rotations/directions; also N108 |
| grid | 318 | taught | N106: grid planning |
| grid, 2D planning on | 29 | taught | N106: 2D grid planning |
| grid, feedback plan on | 374 | taught | N106: feedback plan on a grid |
| grid, inﬁnite sequence | 204–205 | out-of-scope | sampling-theory detail (infinite grid sequences, dropped PA 5.6) |
| grid, localization on (see localization, discrete) |  | index-noise | cross-reference to localization, discrete |
| grid, multi-resolution | 205 | add | **quadtrees and multi-resolution grids** (robotics) → RO-04 (extend N97); quadtrees/octrees and multi-resolution maps are standard map representations |
| grid, navigation function on | 376–381 | taught | N106: navigation function on a grid |
| grid, neighborhoods | 221 | add | **grid connectivity (4- and 8-connected)** (robotics) → RO-05 (extend N106); every grid planner must choose 4- or 8-connected moves |
| grid, partial | 205 | out-of-scope | sampling-theory detail (partial grids) |
| grid, resolution issues | 223–224 | taught | N106: grid resolution and its effect on planning |
| grid, set of environments | 655–662 | out-of-scope | sensing-uncertainty example (set of environments), research-only |
| grid, standard (see standard grid) |  | index-noise | cross-reference to standard grid |
| grid, Sukharev (see Sukharev grid see also lattice) |  | index-noise | cross-reference to Sukharev grid |
| grid point | 221 | taught | N106: grid points of a grid |
| grid resolution | 201 | taught | N106: grid resolution |
| group (see fundamental group see also matrix groups) | 141 | index-noise | cross-reference to fundamental group / matrix groups |
| group axioms | 141 | out-of-scope | group axioms; plan dropped PA 4.6 (group theory) |
| group of n-dimensional rotation matrices | 146 | taught | plan§4: Rigid-body transforms and homogeneous coordinates: rotation matrices as SO(n) |
| guaranteed reachable | 512 | out-of-scope | nondeterministic planning theory term |
| guard in a roadmap | 241 | taught | N111: visibility roadmap guards |
| gyroscope | 601 | taught | N83: gyroscope |
| Haar measure | 193–195 | out-of-scope | measure theory; plan dropped PA 5.2 |
| hairy ball theorem | 400 | out-of-scope | topology theorem (proof result) |
| half-edge | 86, 253 | out-of-scope | computational-geometry data structure (doubly connected edge list) |
| half-plane | 83 | taught | N71: half-planes |
| half-space | 87 | taught | N71: half-spaces (3D version of half-planes) |
| Halton sequence | 207–208 | out-of-scope | low-discrepancy sequences; plan dropped PA 5.6 |
| Hamilton’s equations | 779, 879, 891, 922 | out-of-scope | Hamiltonian mechanics; plan dropped PA 13.11 |
| Hamilton’s principle of least action | 766–768 | out-of-scope | variational principle; plan dropped PA 13.9 |
| Hamilton-Jacobi-Bellman equation | 515, 870–873 | taught | N205: HJB equation |
| Hamilton-Jacobi-Isaacs equation | 873 | out-of-scope | differential games; plan dropped PA 13.12 |
| Hamiltonian function | 778, 779, 875 | out-of-scope | Hamiltonian mechanics; plan dropped PA 13.11 (Pontryagin named only in N116) |
| Hamiltonian mechanics (see mechanics, Hamiltonian) |  | index-noise | cross-reference to mechanics, Hamiltonian |
| Hammersley point set | 207–208 | out-of-scope | low-discrepancy sequences; plan dropped PA 5.6 |
| harmonic potential function | 411–412 | add | **harmonic potential fields and Laplace's equation** (robotics) → RO-05 (extend N109); potential fields with no local minima come from solutions of Laplace's equation |
| Hausdorﬀ axiom | 131 | out-of-scope | point-set topology axiom |
| Hausdorﬀ space | 131 | out-of-scope | point-set topology |
| Heisenberg system (see nonholonomic integrator) |  | index-noise | cross-reference to nonholonomic integrator |
| helicopter ﬂight | 809 | index-noise | application example |
| Hessian | 410 | taught | MA-064: Hessian |
| hide and seek | 11 | index-noise | example game name |
| hide-and-seek (see pursuit-evasion game) |  | index-noise | cross-reference to pursuit-evasion game |
| hierarchical inclusion of a plan | 23, 693 | out-of-scope | book-specific formalism (hierarchical inclusion) |
| hierarchical planning | 23, 336 | taught | N126: layers mission > behaviour > motion > control |
| higher order controllability | 920 | out-of-scope | nonholonomic control theory; plan dropped PA 15.5 |
| Hilbert space | 383 | out-of-scope | functional analysis |
| hill function | 866 | out-of-scope | control-theory proof device (hill functions) |
| history | 566 | taught | N77: action/observation history |
| history information space | 565–567, 591–592 | taught | N77: history information space |
| history information space, at stage k | 567 | taught | N77: history at stage k |
| history information space, at time t | 591 | out-of-scope | continuous-time information spaces; advanced theory |
| history information state | 566 | taught | N77: history information state |
| history-based sensor mapping | 590, 591 | out-of-scope | book-specific formalism of sensor mappings |
| hitch length | 730 | index-noise | parameter of an example (trailer hitch) |
| holonomic | 735, 893 | taught | N64: holonomic |
| homeomorphic spaces | 132 | out-of-scope | topology; plan teaches C-space in plain words (N72) |
| homeomorphism | 132–134, 385, 391 | out-of-scope | topology; plan dropped PA 4.1 |
| homicidal chauﬀeur | 782–783 | index-noise | example differential game name |
| homing sensor | 602 | index-noise | example sensor name |
| homogeneous transformation matrix | 96, 97, 100–103, 105–108, 110, 121, 124, 145, 165–167 | taught | plan§4: Rigid-body transforms and homogeneous coordinates: planned new MA Note |
| homology | 144 | out-of-scope | algebraic topology |
| homotopic paths | 140 | out-of-scope | algebraic topology (homotopy); plan dropped PA 4.5 |
| homotopy group (see fundamental group) |  | index-noise | cross-reference to fundamental group |
| humanoid | 13, 14, 114 | taught | N69: humanoid kinematic trees |
| hybrid state space | 328 | out-of-scope | hybrid systems; plan dropped PA 7.3 |
| hybrid system | 327–332, 388 | taught | N289: contact as a hybrid system |
| hybrid system, motion planning | 327 | out-of-scope | hybrid-system motion planning; plan dropped PA 7.3 |
| hybrid system, with nature | 552–556 | out-of-scope | hybrid systems with nature; advanced theory |
| I-map (see information mapping) |  | index-noise | cross-reference to information mapping |
| I-space (see information space) |  | index-noise | cross-reference to information space |
| I-state (see information state) |  | index-noise | cross-reference to information state |
| ibuprofen | 17 | index-noise | example molecule name |
| ideal distance function | 811 | out-of-scope | sub-Riemannian metric theory |
| identiﬁcation of points | 136 | out-of-scope | topology (quotient spaces) |
| identity sensor | 562, 598 | out-of-scope | book-specific virtual sensor formalism |
| implicit function theorem | 722 | add | **Implicit function theorem** (maths) → MA 06-calculus; linearising constraints g(q)=0 and closed-chain/IK velocity relations |
| implicit velocity constraints | 718 | taught | N64: velocity constraints (holonomic/nonholonomic) |
| improper prior | 485 | out-of-scope | Bayesian statistics detail |
| incomparable actions | 440 | out-of-scope | multi-objective decision theory detail |
| incremental distance computation | 212 | out-of-scope | incremental distance computation is an implementation detail inside collision libraries (LaValle 5.3) |
| incremental sampling and searching |  | index-noise | group heading; sub-entries judged separately |
| incremental sampling and searching, adapting search algorithms | 220–224 | taught | N110: sampling-based planners adapting search |
| incremental sampling and searching, general framework | 217–220 | taught | N110: incremental sampling-and-searching framework |
| incremental sampling and searching, under diﬀerential constraints | 820–837 | taught | N112: kinodynamic sampling-based planning |
| independent events | 443 | taught | MA-016: independent events |
| independent-joint motion model | 361 | out-of-scope | book-specific coordinated-motion model |
| inertia matrix | 756–759, 766 | taught | N220: inertia matrix |
| inertia operator (see inertia matrix) |  | index-noise | cross-reference to inertia matrix |
| inertia tensor (see inertia matrix) |  | index-noise | cross-reference to inertia matrix |
| inertial coordinate frame | 746–747, 754, 755, 762, 767 | add | **Inertial reference frame** (robotics) → RO-17 (extend N220); Newton's laws and IMU readings only hold in an inertial frame |
| inﬁmum | 439 | out-of-scope | real-analysis notation (infimum) |
| inﬁnite reﬂection (in a game) | 489 | out-of-scope | game-theory philosophy |
| inﬁnite-horizon problem | 522–527 | taught | N8: infinite-horizon problems |
| inﬂection ray | 674 | out-of-scope | gap-navigation research detail |
| information mapping | 571–574 | out-of-scope | book-specific information-mapping formalism |
| information mapping, suﬃcient | 573–574 | out-of-scope | book-specific information-mapping formalism |
| information space | 559–627 | taught | N153: information/belief space |
| information space, continuous examples | 598–614 | index-noise | pointer to example section |
| information space, continuous time | 591–592 | out-of-scope | continuous-time information spaces; advanced theory |
| information space, conversion to a state space | 570–571, 634–637 | taught | N153: belief space as a new state space |
| information space, discrete examples | 581–589 | index-noise | pointer to example section |
| information space, for game theory | 619–627 | out-of-scope | information spaces in games; advanced theory |
| information space, in continuous state spaces | 589–614 | taught | N80: continuous-state information spaces (Kalman/particle) |
| information space, limited memory | 580–581 | out-of-scope | book-specific formalism |
| information space, sensor feedback (see history information space see also nondeterministic information space see also probabilistic information space) | 580–581 | taught | N77: history information space |
| information state | 560 | taught | N77: information state |
| information transition equation | 570–571 | taught | N78: information/belief transition (Bayes filter) |
| information transition equation, derived | 573–574 | out-of-scope | derived I-space formalism; book-specific |
| information transition function | 570 | taught | N78: belief transition function |
| information-conservative property | 688 | out-of-scope | book-specific formalism |
| information-feedback plan | 568 | taught | N153: information-feedback plan (policy over beliefs) |
| initial condition space | 566–567, 590 | out-of-scope | book-specific formalism |
| input string | 585 | out-of-scope | automata theory; plan dropped PA 11.5 |
| integrable system | 734 | out-of-scope | nonholonomic system theory (integrability); plan dropped PA 15.10 |
| integral curve | 387–388 | taught | plan§4: ODEs and vector fields: integral curve = following the arrows |
| integral manifold | 893 | out-of-scope | differential geometry (Frobenius); plan dropped PA 15.11 |
| integration (see numerical integration) |  | index-noise | cross-reference to numerical integration |
| interior of a set | 129 | out-of-scope | point-set topology |
| interior point | 129 | out-of-scope | point-set topology (interior of a set), not the solver |
| interpolation neighbors | 420 | taught | N106: DP with interpolation |
| interpolation region (for value iteration) | 422, 551 | taught | N106: interpolation in DP over continuous spaces |
| interval homeomorphisms | 132 | out-of-scope | topology (homeomorphisms of intervals) |
| intractable problem | 299 | taught | N103: intractable / NP-hard planning |
| inverse Ackerman function | 304 | out-of-scope | complexity-theory function (Davenport-Schinzel bounds) |
| inverse control problem | 816 | out-of-scope | book-specific formalism (inverse of the system simulator) |
| inverse kinematics problem | 120 | taught | N279: inverse kinematics problem |
| involutive distribution | 901 | out-of-scope | differential geometry (Frobenius); plan dropped PA 15.11 |
| Isaacs | 782 | index-noise | person name |
| isomorphic graphs | 133 | out-of-scope | graph/topology theory (isomorphism) |
| isomorphic groups | 149 | out-of-scope | group theory; plan dropped PA 4.6 |
| isomorphism | 132 | out-of-scope | abstract algebra/topology term |
| iterative deepening | 39 | taught | N105: iterative deepening |
| Jacobi identity | 904, 907, 920 | out-of-scope | Lie algebra identity; plan dropped PA 15.11 |
| Jacobian | 294 | taught | MA-063: Jacobian |
| jerk (third time derivative) | 738, 853 | taught | N202: jerk and minimum-jerk |
| joint encoder | 601 | taught | N86: encoders |
| junction of links | 114 | taught | N69: kinematic trees: links joined at junctions |
| Kagami | 13 | index-noise | person name |
| Kalman ﬁlter | 615–617 | taught | N80: Kalman filter |
| Kalman rank condition | 868 | taught | N204: controllability rank test |
| Kd-tree | 233–234, 417, 831 | taught | N108: kd-tree |
| Khalil-Kleinﬁnger parameterization | 115 | out-of-scope | book-specific variant of DH notation (modified DH) |
| Khatib | 401 | index-noise | person name |
| kidnapped-robot problem | 640 | taught | N94: kidnapped-robot problem |
| kinematic chain | 100 | taught | N69: kinematic chain |
| kinematic constraints | 791, 891 | taught | N64: kinematic (velocity) constraints |
| kinematic singularities | 346 | taught | N278: kinematic singularities |
| kinematically controllable | 921 | out-of-scope | nonholonomic control theory; plan dropped PA 15.5 |
| kinematics for wheeled systems | 722–731 | taught | N64: wheeled-robot kinematics (also N66, N67) |
| Kineo CAM | 7, 16 | index-noise | company/product name |
| kinetic energy | 752, 760, 766–769, 772, 776 | taught | N281: kinetic energy in Lagrangian mechanics |
| kinodynamic planning | 792, 820–828 | taught | N112: kinodynamic planning |
| Klein bottle | 138 | index-noise | topology example surface |
| knot | 350 | out-of-scope | knot theory (a different field) |
| knot simpliﬁcation | 350 | out-of-scope | knot theory (a different field) |
| knot vector | 91 | add | **B-splines** (maths) → RO-15 (extend N202); B-splines (knots, control points) are the common way to represent smooth robot paths and trajectories |
| Koditschek | 375, 409 | index-noise | person name |
| Kolmogorov complexity | 61, 301 | out-of-scope | theoretical computer science |
| Kuﬀner | 6, 219 | index-noise | person name |
| Kuhn | 622, 627 | index-noise | person name |
| Kutzbach criterion | 180 | taught | N70: Grübler/Kutzbach DOF count |
| L-shaped corridor example | 582–585 | index-noise | worked example name |
| label-correcting algorithms | 56–57 | taught | N104: label-correcting = Dijkstra-family shortest paths |
| ladder robot (see line-segment robot) |  | index-noise | cross-reference to line-segment robot |
| Laﬀerriere and Sussmann | 910 | index-noise | person names |
| Lagrange multiplier | 774 | taught | MA-066: Lagrange multipliers |
| Lagrangian function | 767, 769, 772, 776, 779 | taught | N281: Lagrangian L = T - V |
| Lagrangian mechanics (see mechanics, Lagrangian, 127) |  | index-noise | cross-reference to mechanics, Lagrangian |
| landmark region detector | 602 | out-of-scope | book-specific virtual sensor |
| landmark sensors | 602–603 | taught | N76: landmark sensors |
| language | 31, 588 | out-of-scope | formal-language/automata theory; plan dropped PA 11.5 |
| LARC (see Lie algebra rank condition) |  | index-noise | cross-reference to Lie algebra rank condition |
| latitude in a grid | 661 | index-noise | example detail |
| Latombe | 127 | index-noise | person name |
| lattice | 204, 208 | taught | N114: state lattice |
| lattice, for unconstrained mechanical systems | 825–826 | taught | N114: lattice for mechanical systems (motion primitives) |
| lattice, from double integrator (see doubleintegrator lattice) |  | index-noise | cross-reference to double-integrator lattice |
| lattice, grid (see grid) |  | index-noise | cross-reference to grid |
| Laumond | 16, 791 | index-noise | person name |
| lawn mowing | 354 | index-noise | example application of coverage (N273) |
| layered graph | 65 | out-of-scope | logic-based planning graphs; plan dropped PA 2.10-2.13 |
| layered plan | 68 | out-of-scope | logic-based planning graphs; plan dropped PA 2.10-2.13 |
| learning phase | 529 | taught | N1: learning phase of reinforcement learning |
| leaves of a foliation | 799, 893 | out-of-scope | differential geometry (foliations) |
| Lebesgue integral | 193 | out-of-scope | measure theory; plan dropped PA 5.2 |
| Lebesgue measure | 193 | out-of-scope | measure theory; plan dropped PA 5.2 |
| left translation | 905 | out-of-scope | Lie group theory |
| left-invariant vector ﬁeld | 905 | out-of-scope | Lie group theory |
| left-turn predicate | 263 | out-of-scope | computational-geometry predicate (orientation test) |
| Legendre transformation | 778 | out-of-scope | Hamiltonian mechanics; plan dropped PA 13.11 |
| Legendre-Clebsch condition | 879 | out-of-scope | optimal-control second-order condition (proof) |
| Leibniz rule | 396 | out-of-scope | calculus identity used inside a derivation |
| Lennard-Jones radii | 352 | out-of-scope | molecular chemistry (a different field) |
| Lens spaces | 138 | out-of-scope | topology examples |
| level-set method | 429 | out-of-scope | numerical PDE method (research-level) |
| LG (see linear Gaussian system) |  | index-noise | cross-reference to linear Gaussian system |
| Lie | 892 | index-noise | person name |
| Lie algebra | 904–906 | out-of-scope | Lie algebra; plan dropped PA 15.11 |
| Lie algebra, cross product example | 904–905 | out-of-scope | Lie algebra; plan dropped PA 15.11 |
| Lie algebra, of the system distribution | 905–906 | out-of-scope | Lie algebra; plan dropped PA 15.11 |
| Lie algebra, on Lie groups (see Philip Hall basis) | 905 | out-of-scope | Lie algebra; plan dropped PA 15.11 |
| Lie algebra rank condition | 908 | out-of-scope | nonholonomic controllability theory; plan dropped PA 15.5 |
| Lie bracket | 897–901, 904 | out-of-scope | Lie brackets; plan dropped PA 15.11 |
| Lie bracket, Taylor series approximation of | 899–900 | out-of-scope | Lie brackets; plan dropped PA 15.11 |
| Lie derivative | 866 | out-of-scope | differential-geometry notation; dV/dt along f is taught with Lyapunov functions (N199) |
| Lie group | 145, 905 | out-of-scope | Lie group theory; plan dropped PA 4.6 (SE(3) taught as matrices) |
| ligand | 350 | index-noise | molecular-biology example |
| limit curve | 853 | taught | N203: phase-plane limit curve in time-optimal time scaling |
| limit cycle | 865 | taught | N299: limit cycle |
| limit point of a set | 129 | out-of-scope | point-set topology |
| Lin-Canny | 245 | out-of-scope | research collision algorithm (Lin-Canny) |
| line-segment robot | 273–280 | index-noise | example robot |
| line-sweep principle (see plane-sweep principle) |  | index-noise | cross-reference to plane-sweep principle |
| linear combination | 382 | taught | MA-052: linear combination |
| linear complementarity problem | 473 | taught | N289: complementarity contact model |
| linear diﬀerential game | 782 | out-of-scope | differential games; plan dropped PA 13.12 |
| linear interpolation | 420 | taught | ML-043: linear interpolation |
| linear momentum | 751 | taught | N220: linear momentum (F = ma) |
| linear programming | 440, 467, 855 | taught | MA-068: linear programming |
| linear sensing models | 598–600 | taught | N80: linear measurement model |
| linear space | 382 | taught | MA-052: vector (linear) space |
| linear system | 739–741 | taught | plan§4: State-space models: x' = Ax + Bu |
| linear system, observability | 740 | taught | N80: observability |
| linear system, time-varying | 741 | taught | N206: time-varying linear systems (time-varying LQR) |
| linear transformations | 120 | taught | MA-053: linear transformations |
| linear-Gaussian system | 615, 616, 655 | taught | N80: linear-Gaussian system |
| linear-quadratic problems | 874–875 | taught | N205: linear-quadratic problems (LQR) |
| linear-quadratic-Gaussian (LQG) system | 617, 875 | add | **LQG control and the separation principle** (control) → RO-15 (extend N206); Kalman filter + LQR together is the standard output-feedback controller |
| link | 100 | taught | N69: links of a chain |
| linkage | 100 | add | **closed chains and parallel robots** (robotics) → RB-01 (new Note); linkages as closed chains (LaValle 4.4) |
| linkage graph | 177 | out-of-scope | closed-chain linkages; plan dropped PA 4.15 and ME-035 |
| Lipschitz condition | 216, 387–388, 806, 819, 831, 840, 856 | out-of-scope | existence/uniqueness proof condition for ODEs and planner convergence proofs |
| Lipschitz constant | 216, 388 | out-of-scope | existence/uniqueness proof condition for ODEs and planner convergence proofs |
| LMT framework (see preimage planning, 692) |  | index-noise | cross-reference to preimage planning |
| local operator | 375, 377, 378, 401, 403, 410, 514, 839 | taught | N106: local operator of value iteration |
| local operator, continuous space | 401 | taught | N106: local operator in continuous spaces (interpolation) |
| local planning method | 217–220, 226–228, 231, 238, 240, 241, 327, 855, 862, 869, 880, 883, 886, 888, 908, 910, 921 | taught | N111: local planner in sampling-based roadmaps |
| local planning method, in plan-and-transform | 843, 845 | out-of-scope | plan-and-transform method; research-level nonholonomic planning |
| local planning method, under diﬀerential constraints | 816–818, 833, 834, 836 | taught | N112: steering/local planning under motion limits |
| local visibility sensor | 667 | out-of-scope | book-specific virtual sensor |
| localization | 640–684 | taught | N94: localization |
| localization, active | 640, 644–646 | taught | N180: active localization |
| localization, combinatorial | 647–651 | out-of-scope | combinatorial localization; research-level |
| localization, discrete | 640–647 | taught | N94: discrete (grid) localization |
| localization, passive | 640, 642–644 | taught | N94: passive localization |
| localization, probabilistic | 651–655 | taught | N94: probabilistic localization |
| localization, symmetries | 643–644 | taught | N94: symmetric maps make global localization ambiguous |
| locally positive deﬁnite | 866 | taught | N199: positive definite functions (Lyapunov) |
| locally randomized plan | 622 | out-of-scope | randomized plans in games; research-only |
| Logabex LX4 robot | 348 | index-noise | robot product name |
| logic-based planning | 57–71 | add | **symbolic task planning (STRIPS/PDDL)** (robotics) → RB-03 (extend N293); task and motion planning needs operators with preconditions and effects |
| logic-based planning, as satisﬁability | 69–71 | out-of-scope | planning as SAT; AI-planning research technique |
| logic-based planning, converting to state space | 61–62 | add | **symbolic task planning (STRIPS/PDDL)** (robotics) → RB-03 (extend N293); symbolic plans map to a state space search |
| logic-based planning, in plan space | 63–64 | out-of-scope | plan-space (partial-order) planning; AI-planning technique beyond beginner robotics |
| logic-based planning, operator | 58 | add | **symbolic task planning (STRIPS/PDDL)** (robotics) → RB-03 (extend N293); operators with preconditions and effects |
| logic-based planning, via a planning graph | 64–69 | out-of-scope | planning graphs (Graphplan); AI-planning technique |
| logical predicate (see predicate) |  | index-noise | cross-reference to predicate |
| loop path | 142 | out-of-scope | algebraic topology (loops for the fundamental group) |
| lost-cow problem | 672, 707 | out-of-scope | competitive search theory; research-only |
| low-discrepancy sampling | 205–209 | out-of-scope | low-discrepancy sampling; plan dropped PA 5.6 |
| low-dispersion sampling | 201–205 | out-of-scope | dispersion theory; plan dropped PA 5.5 |
| lower envelope | 302–304, 467 | out-of-scope | computational geometry (lower envelopes) |
| lower pairs | 105 | taught | N70: lower pairs = basic joint types |
| lower value of a game | 461, 540, 546 | taught | N54: minimax value of a game |
| Lozano-Pérez | 127 | index-noise | person name |
| Lozano-Pérez, Mason, and Taylor | 692 | index-noise | person names |
| LPM (see local planning method) |  | index-noise | cross-reference to local planning method |
| lunar lander | 748–750 | index-noise | worked example name |
| Lyapunov function | 412, 865–867 | taught | N199: Lyapunov function |
| Lyapunov function, in planning | 867 | taught | N199: Lyapunov functions used for planning/feedback |
| Lyapunov stability | 862–863 | taught | N199: Lyapunov stability |
| Lyapunov stability, uniform | 863 | out-of-scope | uniform stability for time-varying systems; proof-level control theory |
| Lynch and Mason | 732 | index-noise | person names |
| Möbius band | 136, 138, 144, 183 | index-noise | topology example surface |
| Mahalanobis metric | 811 | taught | plan§4: Mahalanobis distance: planned new MA Note |
| maneuver | 809 | taught | N114: maneuvers = motion primitives |
| maneuver automaton | 809 | taught | N114: maneuver automaton = motion-primitive library |
| Manhattan metric | 187 | taught | ML-085: Manhattan distance |
| Manhattan motion model | 360–361 | out-of-scope | book-specific coordinated-motion model |
| manifold | 134–139 | taught | N72: manifold in plain words |
| manifold, embedding | 134 | out-of-scope | topology (embeddings of manifolds); plan teaches C-space shapes in plain words (N72) |
| manifold, higher dimensional | 138–139 | out-of-scope | topology of higher-dimensional manifolds; beyond N72 plain-words level |
| manifold, one-dimensional | 135–136 | taught | N72: one-dimensional manifolds: line and circle |
| manifold, two-dimensional | 136–138 | taught | N72: two-dimensional manifolds: plane, sphere, torus |
| manifold, with boundary (see smooth manifold) | 134 | out-of-scope | topology (manifolds with boundary) |
| manipulation graph | 335–336 | taught | N292: manipulation planning graph (transit and transfer modes) |
| manipulation planning | 332–337 | taught | N292: manipulation planning |
| manipulation planning, nonprehensile (see nonprehensile manipulation) |  | index-noise | cross-reference to nonprehensile manipulation |
| manipulation planning, under uncertainty | 691–704 | taught | N292: preimage planning under uncertainty |
| manipulator | 107, 118, 122, 332–339, 348, 771–773, 846, 851 | taught | N277: manipulators |
| map building | 655–684 | taught | N96: map building |
| marginalization | 443–444, 502, 503, 578, 652 | taught | MA-014: marginal probability |
| Markov chain | 498 | taught | plan§4: Markov chains: planned new MA Note |
| Markov decision process | 498 | taught | N7: Markov decision process |
| Markov game | 550 | taught | N54: Markov (stochastic) games: sequential games on state spaces |
| Markov process | 498, 499 | taught | plan§4: Markov chains: Markov process |
| mass matrix | 766 | taught | N281: mass matrix |
| matching pennies | 446 | index-noise | example game name |
| Matlab | 856 | index-noise | software name |
| matrix game | 460 | taught | N54: matrix games, mixed strategies by LP |
| matrix groups | 145–148 | out-of-scope | group theory; plan dropped PA 4.6 |
| matrix subgroup | 146 | out-of-scope | group theory; plan dropped PA 4.6 |
| maximal ball | 244 | out-of-scope | medial-axis sampling detail; research sampler |
| maximum-clearance navigation function | 379–380 | out-of-scope | book-specific navigation-function variant (NF2); base ideas in N106 and N270 |
| maximum-clearance roadmap | 260–261 | taught | N270: maximum-clearance roadmap |
| maze searching | 660–662 | taught | N107: searching an unknown maze (bug/exploration strategies) |
| MDP (see Markov decision process) |  | index-noise | cross-reference to Markov decision process |
| Mealy/Moore machines | 31 | out-of-scope | automata-theory variants; finite state machines taught in N130 |
| means-end analysis | 71 | out-of-scope | history of AI planning |
| measurable function | 193 | out-of-scope | measure theory; plan dropped PA 5.2 |
| measurable sets | 192 | out-of-scope | measure theory; plan dropped PA 5.2 |
| measure axioms | 192 | out-of-scope | measure theory; plan dropped PA 5.2 |
| measure space | 186 | out-of-scope | measure theory; plan dropped PA 5.2 |
| measure theory (see Haar measure) | 191–195, 811 | out-of-scope | measure theory; plan dropped PA 5.2 |
| measure zero | 193 | out-of-scope | measure theory; plan dropped PA 5.2 |
| mechanics | 745–780 | index-noise | group heading; sub-entries judged separately |
| mechanics, Hamiltonian | 778–780 | out-of-scope | Hamiltonian mechanics; plan dropped PA 13.11 |
| mechanics, Lagrangian | 762–777 | taught | N281: Lagrangian mechanics |
| mechanics, Newton-Euler (see dynamics) | 745–762 | taught | N220: Newton-Euler rigid-body mechanics |
| medial-axis sampling | 244 | out-of-scope | research sampler variant (medial-axis PRM) |
| Mersenne twister | 200 | out-of-scope | random-number generator internals; plan dropped PA 5.4 |
| metric space | 186–188 | taught | N108: metric space |
| metric space, Cartesian products of | 188 | taught | N108: distances on product C-spaces |
| metric space, deﬁnition | 187 | taught | N108: metric axioms |
| metric space, for motion planning | 188–191 | taught | N108: metrics for motion planning |
| metric space, from SE(2) | 189 | taught | N108: distances on SE(2) |
| metric space, from SE(3) | 191 | taught | N108: distances on SE(3) |
| metric space, from SO(2) | 188–189 | taught | N108: distances on angles (SO(2)) |
| metric space, from SO(3) | 189–190 | taught | N108: distances on rotations (SO(3)) |
| metric space, from T n | 190–191 | taught | N108: distances on the torus (wrap-around angles) |
| metric space, nonpositively curved | 857 | out-of-scope | differential geometry (curvature of metric spaces) |
| metric space, Riemannian manifold | 810–811 | out-of-scope | differential geometry (Riemannian metrics) |
| metric space, robot displacement metric | 190 | taught | N108: robot displacement as a C-space distance |
| metric space, subspaces of | 188 | taught | N108: metric restricted to a subspace |
| metric tensor | 810 | out-of-scope | differential geometry (Riemannian metrics) |
| metrics (see metric space) |  | index-noise | cross-reference to metric space |
| metrizable | 187 | out-of-scope | point-set topology |
| mine sweeping | 354 | index-noise | example application of coverage (N273) |
| minimalism | 700 | out-of-scope | philosophy of minimal sensing (research viewpoint) |
| minimax | 448 | taught | N54: minimax |
| minimum turning radius | 725 | taught | N67: minimum turning radius |
| Minkowski diﬀerence | 158, 252, 305 | taught | N73: Minkowski difference forms the C-space obstacle |
| Minkowski sum | 158 | taught | N73: Minkowski sum |
| mixed Nash equilibrium (see Nash equilibrium, randomized) |  | index-noise | cross-reference to Nash equilibrium, randomized |
| mixed strategy (see randomized strategy) |  | index-noise | cross-reference to randomized strategy |
| mod sensor | 562 | out-of-scope | book-specific virtual sensor |
| mode space | 327 | out-of-scope | hybrid systems; plan dropped PA 7.3 |
| mode transition function | 328 | out-of-scope | hybrid systems; plan dropped PA 7.3 |
| mode-dependent dynamics | 327 | out-of-scope | hybrid systems; plan dropped PA 7.3 |
| moment of a density | 597 | taught | MA-012: moments of a distribution (mean, variance) |
| moment of force (see torque, 753) |  | index-noise | cross-reference to torque |
| moment of inertia | 758 | taught | N220: moment of inertia |
| moment of momentum | 751–753, 755, 761 | taught | N220: angular momentum (behind Euler's equation) |
| moment-based approximations | 595–597 | taught | N80: approximating a belief by its mean and covariance |
| momentum | 751 | taught | N301: momentum |
| monomial | 169 | out-of-scope | semi-algebraic models; plan dropped PA 3.2 |
| monotone polygon | 269 | out-of-scope | computational geometry (monotone polygons) |
| Monte-Carlo localization (see localization, probabilistic) |  | index-noise | cross-reference to localization, probabilistic |
| morphing a path | 140 | out-of-scope | algebraic topology (homotopy of paths) |
| Morse function | 411 | out-of-scope | differential topology (Morse theory) |
| Morse theory | 410 | out-of-scope | differential topology (Morse theory) |
| motion capture | 858 | taught | N317: motion capture |
| motion command | 694–695 | out-of-scope | compliant-motion preimage planning detail; research-level |
| motion library (see motion primitives) |  | index-noise | cross-reference to motion primitives |
| motion planning | 793 | taught | N72: motion planning problem |
| motion primitive | 808–810, 836 | taught | N114: motion primitives |
| multi-body dynamics (see dynamics, of multiple bodies) |  | index-noise | cross-reference to dynamics, of multiple bodies |
| multi-chained-form systems | 920 | out-of-scope | nonholonomic control theory normal forms; plan dropped PA 15.10 |
| multi-level approach | 845 | out-of-scope | plan-and-transform multi-level method; research-level nonholonomic planning |
| multi-linear interpolation | 421 | taught | N106: multilinear interpolation of values on a grid |
| multi-resolution grid | 204 | add | **quadtrees and multi-resolution grids** (robotics) → RO-04 (extend N97); quadtrees/octrees and multi-resolution maps are standard map representations |
| multiobjective optimization | 440–441 | taught | N53: multi-objective optimisation and Pareto optimality |
| multiple observations | 454 | taught | N53: Bayesian decisions with several observations |
| multiple query | 186, 237 | taught | N111: multiple-query roadmaps (PRM) |
| multiple shooting | 857 | taught | N116: multiple shooting |
| multiple-robot motion planning | 318–327 | taught | N271: multi-robot motion planning |
| multiple-robot optimality | 362–364 | out-of-scope | Pareto-optimal multi-robot plans; research-level |
| multiply connected | 141 | out-of-scope | algebraic topology |
| Murphy’s Law | 448 | index-noise | joke/saying |
| Murray and Sastry | 917 | index-noise | person names |
| mutex condition | 66–67 | out-of-scope | logic-based planning graphs; plan dropped PA 2.10-2.13 |
| mutex relation | 66 | out-of-scope | logic-based planning graphs; plan dropped PA 2.10-2.13 |
| NAG Fortran Library | 856 | index-noise | software name |
| naive Bayes | 454 | taught | ML-081: naive Bayes |
| narrow-phase collision detection | 210 | taught | N108: narrow-phase collision detection |
| NASA/Lockheed Martin X-33 | 795 | index-noise | vehicle name (example) |
| Nash equilibrium | 468–475, 490, 619, 626 | taught | N54: Nash equilibrium |
| Nash equilibrium, admissible | 471 | taught | N54: admissible Nash equilibria |
| Nash equilibrium, in a sequential game | 548–549 | taught | N54: equilibria in sequential games |
| Nash equilibrium, nonuniqueness | 470–472 | taught | N54: several Nash equilibria |
| Nash equilibrium, randomized | 472–474, 476, 622 | taught | N54: mixed (randomized) Nash equilibrium |
| nature | 437, 447 | taught | N53: nature as an adversary/random source |
| nature action space | 447 | taught | N53: nature's actions |
| nature observation action | 453 | taught | N53: nature's observation actions (decisions with observations) |
| nature sensing action | 563, 564, 590, 598–599, 609–612 | out-of-scope | book-specific notation: sensor noise written as nature's action |
| nature sensing actions | 561 | out-of-scope | book-specific notation: sensor noise written as nature's action |
| navigation function | 35, 52, 375–381 | taught | N106: navigation function |
| navigation function, continuous space | 401 | taught | N106: navigation function on continuous spaces |
| navigation function, in the sense of Rimon-Koditschek | 409–411 | add | **Navigation functions (Rimon-Koditschek)** (robotics) → RO-05 (extend N109); potential function with a single minimum gives provably convergent feedback motion |
| navigation function, stochastic | 553 | taught | N14: value function with stochastic outcomes |
| navigation problem | 657, 660 | taught | N107: navigating in unknown environments |
| negative literal | 58 | out-of-scope | logic notation for STRIPS-style planning detail |
| neighborhood function | 241 | out-of-scope | research sampler detail (visibility roadmap) |
| neighborhood of a cover | 414 | out-of-scope | covering theory for approximate DP; research-level |
| Neumann boundary condition | 412 | add | **harmonic potential fields and Laplace's equation** (robotics) → RO-05 (extend N109); boundary conditions (Dirichlet/Neumann) set obstacles and goal in harmonic potentials |
| neuro-dynamic programming (see reinforcement learning) |  | index-noise | cross-reference to reinforcement learning |
| Newton’s laws | 747–752, 755, 757, 766, 768 | taught | plan§4: Newtonian and rigid-body mechanics: short section in N117 |
| Newton-Euler mechanics (see mechanics, Newton-Euler) |  | index-noise | cross-reference to mechanics, Newton-Euler |
| next-best-view problem | 680 | taught | N180: choosing the next best view by information gain |
| NF2 (a navigation function) | 379 | index-noise | book-specific function name |
| NFA (see nondeterministic ﬁnite automaton) |  | index-noise | cross-reference to nondeterministic finite automaton |
| nicotine | 17 | index-noise | example molecule name |
| nilpotent | 910 | out-of-scope | nilpotent Lie algebras; plan dropped PA 15.11 |
| nilpotent system | 908 | out-of-scope | nonholonomic control theory; plan dropped PA 15.10 |
| nilpotentizable | 910 | out-of-scope | nonholonomic control theory; plan dropped PA 15.10 |
| Nilsson | 72 | index-noise | person name |
| Nixederreiter-Xing sequence | 208 | out-of-scope | low-discrepancy sequences; plan dropped PA 5.6 |
| nonconservative forces | 777 | taught | N281: nonconservative forces enter as generalized forces (torques, friction) |
| nonconvex |  | index-noise | group heading; sub-entries judged separately |
| nonconvex, polygon | 84–85, 90 | taught | N71: nonconvex polygons from convex pieces |
| nonconvex, polyhedron | 90 | taught | N71: nonconvex polyhedra |
| nonconvex, set | 82 | taught | MA-067: convex vs nonconvex sets |
| noncooperative game | 438 | taught | N54: noncooperative games |
| noncritical regions | 277 | out-of-scope | cylindrical decomposition detail; plan dropped PA 6.4-6.7 |
| nondeterministic ﬁnite automaton | 585–589 | out-of-scope | automata theory; plan dropped PA 11.5 |
| nondeterministic information space | 574–577 | taught | N77: set-valued (nondeterministic) information space |
| nondeterministic information space, approximations | 593–595 | out-of-scope | approximations of nondeterministic I-spaces; research-level |
| nondeterministic information space, examples | 581–589 | index-noise | pointer to example section |
| nondeterministic information space, planning on | 637–638 | out-of-scope | planning on set-valued information spaces; research-level |
| nondeterministic Turing machine | 299 | out-of-scope | complexity theory (nondeterministic Turing machine) |
| nondeterministic uncertainty | 448–450 | taught | N53: worst-case (nondeterministic) decisions against nature |
| nondeterministic uncertainty, criticisms of | 487–489 | out-of-scope | philosophy of decision theory (criticisms) |
| nondirectional backprojections | 696 | out-of-scope | preimage-planning detail; research-level |
| nondominated (see Pareto optimal) |  | index-noise | cross-reference to Pareto optimal |
| nonholonomic | 735, 791, 888, 893 | taught | N64: nonholonomic |
| nonholonomic constraints | 722 | taught | N64: nonholonomic constraints |
| nonholonomic integrator | 741–742, 901, 908, 911, 915 | out-of-scope | nonholonomic control theory (Brockett integrator); plan dropped PA 15.10 |
| nonholonomic integrator, showing it is nonholonomic | 902 | out-of-scope | nonholonomic control theory; plan dropped PA 15.10 |
| nonholonomic integrator, steering | 917–918 | out-of-scope | steering methods; plan dropped PA 15.12 |
| nonholonomic metric | 811 | out-of-scope | sub-Riemannian metric theory |
| nonholonomic planning | 13, 791–792 | taught | N112: planning for nonholonomic (car-like) robots |
| nonholonomic system | 827–828 | taught | N64: nonholonomic systems |
| nonholonomic system theory | 888–910 | out-of-scope | nonholonomic system theory; plan dropped PA 15.10 |
| noninformative prior | 485–487 | out-of-scope | Bayesian statistics detail (noninformative priors) |
| nonintegrable | 893 | out-of-scope | integrability theory (Frobenius); plan dropped PA 15.11 |
| nonlinear optimization | 855 | taught | N208: nonlinear optimisation solvers (overview) |
| nonlinear programming | 855–857 | taught | N208: nonlinear programming (SQP, interior point) |
| nonlinear system | 741–742 | taught | plan§4: State-space models: nonlinear systems |
| nonlinear system, aﬃne in control | 890–892 | add | **control-affine systems (drift and control vector fields)** (control) → MA 06-calculus (extend planned State-space models Note); x' = f(x) + g(x)u is the form used by feedback linearisation (N124) and barrier-function filters (N199) |
| nonlinear system, aﬃne-in-control | 741 | add | **control-affine systems (drift and control vector fields)** (control) → MA 06-calculus (extend planned State-space models Note); x' = f(x) + g(x)u is the form used by feedback linearisation (N124) and barrier-function filters (N199) |
| nonparametric methods | 487 | taught | ML-085: nonparametric methods (nearest neighbours) |
| nonpositively curved space | 857 | out-of-scope | differential geometry (curvature) |
| nonprehensile manipulation | 700–704 | taught | N292: nonprehensile manipulation |
| nonrigid transformations | 120 | taught | MA-053: scaling and shear (plan §5 recap) |
| nonzero-sum game | 468–476 | taught | N54: nonzero-sum games |
| nonzero-sum game, with more than two players | 475–476 | taught | N54: nonzero-sum games with several players |
| nonzero-sum game, with two players (see Nash equilibrium) | 469–475 | taught | N54: two-player nonzero-sum games |
| NP (complexity class) | 299 | taught | N103: NP-hardness in plain words |
| null sensor | 563 | out-of-scope | book-specific virtual sensor |
| numerical continuation | 341 | out-of-scope | numerical algebraic-geometry technique (homotopy continuation); research-level |
| numerical integration |  | taught | plan§4: Numerical integration of ODEs: planned new MA Note |
| numerical integration, Euler | 813–814 | taught | plan§4: Numerical integration of ODEs: Euler method |
| numerical integration, multistep methods | 815 | out-of-scope | multistep (Adams) integrators; numerical-analysis detail beyond Euler and Runge-Kutta |
| numerical integration, Runge-Kutta | 424, 814–815 | taught | plan§4: Numerical integration of ODEs: Runge-Kutta |
| numerical integration, single-step methods | 815 | taught | plan§4: Numerical integration of ODEs: single-step methods (Euler, Runge-Kutta) |
| NURBS | 91 | out-of-scope | CAD geometric modeling (NURBS) |
| OBB | 211 | taught | N108: oriented bounding boxes in bounding-volume hierarchies |
| observability | 740 | taught | N80: observability |
| observation space | 451, 561 | taught | N153: observation space |
| observations | 451–454 | taught | N153: observations |
| obstacle region | 92, 155 | taught | N73: obstacle region |
| obstacle region, in the C-space | 155–167 | taught | N73: C-space obstacle region |
| obstacle region, in the C-space, 1D case | 158 | taught | N73: 1D C-obstacle |
| obstacle region, in the C-space, general case | 164–167 | out-of-scope | general semi-algebraic C-obstacles; plan dropped PA 3.2 |
| obstacle region, in the C-space, polygonal case | 159–163 | taught | N73: polygonal C-obstacles by Minkowski sum |
| obstacle region, in the C-space, polyhedral case | 163–164 | taught | N73: polyhedral C-obstacles |
| obstacle region, in the state space | 794–797 | taught | N112: obstacles in phase/state space |
| obstacle region, in the world | 82–92 | taught | N71: obstacles in the world |
| obstacle region, polygonal case | 251–264 | taught | N270: planning among polygonal obstacles (exact roadmaps) |
| obstacle region, time-varying | 312–318 | taught | N271: time-varying obstacles |
| obstacles | 82 | taught | N71: obstacles |
| occupancy grid | 92, 684 | taught | N96: occupancy grid |
| Ochiai unknot benchmark | 351 | index-noise | benchmark name (knot theory) |
| octane transformations | 110–112 | index-noise | molecule example |
| odd/even sensor | 561–562 | out-of-scope | book-specific virtual sensor |
| odometric coordinates | 645, 660 | taught | N68: odometry coordinates |
| odometry sensors | 605 | taught | N86: odometry sensors (wheel encoders) |
| on-line algorithm | 20, 672–673 | taught | N107: planning on-line in unknown environments |
| open ball | 130 | out-of-scope | point-set topology |
| open set | 89, 128 | out-of-scope | point-set topology |
| open-loop |  | index-noise | group heading; sub-entries judged separately |
| open-loop, control law | 793 | taught | N9: open-loop control |
| open-loop, plan | 370 | taught | N9: open-loop plan |
| operator | 58 | add | **symbolic task planning (STRIPS/PDDL)** (robotics) → RB-03 (extend N293); operators with preconditions and effects |
| optical character recognition | 456–458 | index-noise | application example |
| optimal motion planning | 357–364 | taught | N110: optimal motion planning (RRT*, asymptotic optimality) |
| optimal planning |  | index-noise | group heading; sub-entries judged separately |
| optimal planning, discrete | 43–57 | taught | N104: optimal discrete planning (shortest paths) |
| optimal planning, ﬁxed-length plans | 45–50 | taught | N14: fixed-length optimal plans by value iteration |
| optimal planning, unspeciﬁed length | 50–53 | taught | N14: optimal plans of unspecified length by value iteration |
| optimization | 438–441 | taught | N53: optimisation in decision making |
| orientation sensor | 600 | taught | N84: orientation from inertial sensors |
| oriented bounding box | 211 | taught | N108: oriented bounding box |
| orienteering problem | 365 | out-of-scope | operations-research routing problem |
| origami | 347 | index-noise | application example |
| orthogonal group | 146 | out-of-scope | group theory; plan dropped PA 4.6 |
| outdoor navigation | 362 | index-noise | application example |
| painting | 354 | index-noise | application example of coverage |
| parallel manipulator | 338 | add | **closed chains and parallel robots** (robotics) → RB-01 (new Note); parallel manipulators (LaValle 4.4) |
| parallel-jaw gripper | 701 | taught | N291: parallel-jaw (antipodal) grasps |
| parameter estimation | 458–459 | taught | MA-070: parameter estimation (MLE) |
| parameterization | 136, 391 | out-of-scope | topology (parametrizing manifolds and paths) |
| Pareto optimal | 362–364, 440–441, 470, 471, 476, 484 | taught | N53: Pareto optimal |
| parking a car | 13, 726, 744, 800, 860, 868, 898 | index-noise | example (car parking; covered in N67) |
| part conﬁguration space | 332 | taught | N292: part (object) configuration space in manipulation planning |
| partial grid | 205 | out-of-scope | sampling-theory detail |
| partial plan | 63 | out-of-scope | plan-space (partial-order) planning; AI-planning technique |
| partially observable Markov decision process (see POMDP) |  | index-noise | cross-reference to POMDP |
| particle | 747 | taught | plan§4: Newtonian and rigid-body mechanics: point particle |
| particle, dynamics | 747–752 | taught | plan§4: Newtonian and rigid-body mechanics: F = ma for a particle |
| particle, falling | 767–768 | index-noise | worked example |
| particle, on a sphere | 776–777 | index-noise | worked example |
| particle ﬁltering | 618–619, 655 | taught | N82: particle filter |
| path | 139 | taught | N72: path as a continuous curve in C-space |
| path connected | 139 | out-of-scope | point-set topology |
| path tuning | 319 | taught | N271: velocity (path) tuning |
| path-constrained phase space | 849 | taught | N203: path-constrained phase plane |
| path-directed subdivision tree | 837 | out-of-scope | research planner (subdivision tree) |
| pattern classiﬁcation | 455–458 | taught | ML-003: classification |
| pebble | 602 | index-noise | example sensor (pebble) |
| peg-in-hole problem | 692, 696–698 | taught | N327: peg-in-hole insertion |
| pendulum | 750–751 | taught | N296: pendulum models |
| pendulum, double | 785 | index-noise | worked example |
| Pennsylvania Turnpike | 441 | index-noise | example place name |
| perfect recall | 622 | out-of-scope | game-theory detail (extensive-form information) |
| permissible action trajectories | 790 | out-of-scope | book-specific formalism |
| Pfaﬃan constraints | 720–721, 724, 734, 742, 775–777, 891–894, 897, 903, 920 | add | **Pfaffian velocity constraints A(q)q̇ = 0** (robotics) → RO-01 (extend N64); the standard matrix form of wheel and contact constraints |
| pharmacophore | 351 | index-noise | molecular-biology example |
| phase constraints | 795 | taught | N112: phase-space (state) constraints |
| phase space | 735–744 | taught | N112: phase space |
| phase space, obstacles | 794–797 | taught | N112: phase-space obstacles |
| phase space, path-constrained | 849–850 | taught | N203: path-constrained phase space (time scaling) |
| phase transition equation | 737, 738 | taught | plan§4: State-space models: x' = f(x, u) |
| phase vector | 736 | taught | plan§4: State-space models: state vector of position and velocity |
| Philip Hall basis | 907–908, 910–914, 917 | out-of-scope | Lie algebra basis; plan dropped PA 15.11 |
| Piano Mover’s Problem | 157–158, 789, 790, 817, 818, 832–835, 838, 841, 855 | taught | N72: piano mover's problem |
| piecewise-linear obstacle motion | 313–314, 317 | taught | N271: moving obstacles |
| pitch rotation | 98 | taught | plan§4: 3D rotations: Euler angles and quaternions: pitch |
| plan-and-transform method | 842–846 | out-of-scope | plan-and-transform method; research-level nonholonomic planning |
| plan-based state transition graph | 507 | out-of-scope | book-specific formalism |
| plan-space planning | 65 | out-of-scope | plan-space (partial-order) planning; AI-planning technique |
| planar joint | 105 | taught | N70: joint types |
| plane-sweep principle | 257–258 | out-of-scope | computational-geometry sweep technique; the resulting decomposition is taught in N270 |
| plane-sweep principle, radial sweep | 263, 406 | out-of-scope | computational-geometry sweep technique; the resulting visibility graph is taught in N270 |
| planetary navigation | 362 | index-noise | application example |
| planner | 21 | taught | N9: planner / plan |
| planning graph | 64–69 | out-of-scope | logic-based planning graphs; plan dropped PA 2.10-2.13 |
| planning under sensing uncertainty | 633–704 | taught | N153: planning under sensing uncertainty |
| planning under sensing uncertainty, general methods | 634–640 | taught | N153: general methods (belief/information space) |
| planning under sensing uncertainty, manipulation | 691–704 | taught | N292: manipulation under uncertainty (preimage planning) |
| planning under sensing uncertainty, pursuit-evasion (see visibility-based pursuit-evasion see also SLAM see also localization) |  | index-noise | cross-reference to visibility-based pursuit-evasion, SLAM, localization |
| Poinsot | 754, 760 | out-of-scope | classical-mechanics construction (Poinsot ellipsoid for free rotation); body rotation is taught via Euler's equation N220 |
| point robot | 252 | taught | N73: point robot as the simplest C-space obstacle case |
| point-location problem | 421, 830 | out-of-scope | computational-geometry data-structure problem (point location); used inside exact planners only |
| policy iteration | 514–518 | taught | N13: policy iteration |
| policy iteration, for reinforcement learning | 535 | taught | N13: policy iteration in RL setting |
| policy iteration, on an information space | 638 | out-of-scope | policy iteration on information spaces: advanced POMDP theory; plan uses value iteration in belief space N268 |
| policy iteration, with average cost-per-stage | 527 | taught | N27: average-cost setting |
| policy iteration, with discounted cost | 526–527 | taught | N13: discounted policy iteration |
| polygonal model | 82–85, 251–264 | taught | N71: polygonal obstacle models |
| polygonal model, face | 253 | out-of-scope | computational-geometry data structure detail (face of a doubly connected edge list) |
| polygonal model, half-edge | 253 | out-of-scope | computational-geometry data structure detail (half-edge list) |
| polygonal model, representation | 251–253 | taught | N71: obstacles as polygons |
| polyhedral model | 85–87 | taught | N71: polyhedra from half-spaces |
| polynomial | 169–170 | taught | N201: polynomials (cubic/quintic) |
| polynomial, coeﬃcient | 169 | taught | ML-060: polynomial coefficients |
| polynomial, in formal Lie algebra | 912 | out-of-scope | formal Lie algebra polynomials: nonholonomic control theory proof machinery (plan dropped PA 15.11) |
| polynomial, term | 169 | taught | ML-060: polynomial term |
| polynomial, total degree | 169 | out-of-scope | algebraic-geometry detail of semi-algebraic models (plan dropped PA 3.2) |
| polynomial-time reducible | 300 | out-of-scope | complexity-theory proof technique (reductions); plan names hardness only in N103 |
| POMDP | 589, 638–640 | taught | N153: POMDP |
| Pontryagin’s minimum principle | 515, 856, 875–879, 922 | taught | N116: Pontryagin named in trajectory optimisation Note |
| Pontryagin’s minimum principle, time-optimality case | 879 | out-of-scope | time-optimal Pontryagin case: optimal control theory beyond beginner depth (plan dropped PA 15.8) |
| portiernia | 329–330 | index-noise | example name (Portiernia doorman example) |
| position sensor | 600 | taught | N63: position as a measured state |
| positive deﬁnite function | 866 | taught | N199: positive definite function in Lyapunov certificates (plan§4 Lyapunov functions) |
| positive literal | 58 | out-of-scope | logic-based symbolic planning (plan dropped PA 2.10-2.13) |
| possibilistic uncertainty (see nondeterministic uncertainty) |  | index-noise | cross-reference to nondeterministic uncertainty |
| posterior | 443 | taught | MA-018: posterior |
| potential energy | 766, 767, 769, 772 | taught | N281: potential energy in the Lagrangian |
| potential function | 191, 225, 766 | taught | N109: potential function for planning |
| potential function, attractive term | 225 | add | **artificial potential fields (attractive and repulsive)** (robotics) → RO-05 (extend N109); classic reactive planner every intro robotics course teaches: attractive pull to goal, repulsive push from obstacles, local minima |
| potential function, continuous state space | 401 | add | **artificial potential fields (attractive and repulsive)** (robotics) → RO-05 (extend N109); potential as a feedback plan over a continuous state space |
| potential function, discrete | 375 | taught | N106: discrete navigation function / wavefront |
| potential function, repulsive term (see navigation function) | 225 | add | **artificial potential fields (attractive and repulsive)** (robotics) → RO-05 (extend N109); repulsive term pushes away from obstacles; see navigation function |
| PQP (Proximity Query Package) | 245 | index-noise | software package name (PQP) |
| predicate | 58 | out-of-scope | logic-based symbolic planning (plan dropped PA 2.10-2.13) |
| predicate, for geometric models | 85 | out-of-scope | semi-algebraic primitives: algebraic-geometry machinery (plan dropped PA 3.2) |
| preimage of a function | 131 | out-of-scope | set-theory notation used in topology definitions (plan dropped PA 4.1) |
| preimage of a motion command | 695 | taught | N292: preimage planning |
| preimage of an observation | 563 | out-of-scope | information-space theory detail (preimage of an observation); belief taught N77 |
| preimage planning | 692–700 | taught | N292: preimage planning |
| Princess and the Monster | 627 | index-noise | example name (Princess and the Monster game) |
| principle of least action (see Hamilton’s principle of least action) |  | index-noise | cross-reference to Hamilton's principle of least action |
| principle of optimality (see dynamic programming) |  | index-noise | cross-reference to dynamic programming (principle of optimality taught N10) |
| principle of virtual work | 776 | out-of-scope | analytical-mechanics principle (virtual work) for deriving constraint forces; plan teaches statics via J^T F (N277) |
| principle subresultant coeﬃcients | 290 | out-of-scope | algebraic-geometry machinery for exact planning (plan dropped PA 6.4-6.9) |
| prior distribution | 443, 484–487 | taught | MA-018: prior distribution |
| prioritized planning | 322 | taught | N271: prioritized multi-robot planning |
| prismatic joint | 100, 101, 103, 105, 107 | taught | N70: prismatic joint |
| Prisoner’s Dilemma | 472, 490 | index-noise | example name (Prisoner's Dilemma) illustrating Nash equilibrium N54 |
| PRM (see sampling-based roadmap) |  | index-noise | cross-reference to sampling-based roadmap |
| probabilistic completeness | 186 | taught | N111: probabilistic completeness |
| probabilistic information space | 577–581 | taught | N78: probabilistic information state = belief |
| probabilistic information space, approximations | 595–597 | taught | N269: approximate belief representations |
| probabilistic information space, examples | 589 | index-noise | examples heading; concept taught N78 |
| probabilistic information space, planning on | 638–640 | taught | N268: planning in belief space |
| probabilistic information state |  | taught | N78: probabilistic information state |
| probabilistic information state, computation of | 614–619 | taught | N78: Bayes filter computation of belief |
| probabilistic roadmap (see sampling-based roadmap) |  | index-noise | cross-reference to sampling-based roadmap |
| probabilistic uncertainty | 448–450 | taught | N63: probabilistic uncertainty |
| probabilistic uncertainty, criticisms of | 483–487 | out-of-scope | philosophical critique of probability models in decision theory |
| probability function | 442 | taught | MA-020: probability function |
| probability measure | 193 | out-of-scope | measure theory (plan dropped PA 5.2) |
| probability space | 441–442 | taught | MA-015: probability space recap (plan§5) |
| probability theory | 441–444 | taught | MA-011: probability theory basics |
| problem solving | 27 | index-noise | general phrase (problem solving), not a concept |
| product of inertia | 758 | taught | N220: products of inertia are entries of the inertia matrix |
| projection sensors | 600–601, 605–608 | out-of-scope | book-specific abstract sensor classification (projection sensors); concrete sensors taught N83-N91 |
| projective geometry | 97 | taught | N88: projective homogeneous coordinates (plan§4) |
| projective space | 138 | out-of-scope | topology of rotation spaces (RP^3); plan dropped PA 4.1-4.7 |
| protein cavity | 113 | out-of-scope | molecular biology application (plan dropped PA 7.6) |
| protein folding | 15, 353–354 | out-of-scope | molecular biology application (plan dropped PA 7.6) |
| proximity sensor | 601 | add | **proximity and contact sensors (bumpers, infrared, ultrasonic)** (robotics) → RO-03; cheap sensors on almost every mobile robot; intro courses list them |
| pseudometric | 191, 314 | out-of-scope | metric-space theory detail (pseudometric) |
| pseudorandom number generation | 199–200 | out-of-scope | how random-number generators are built (plan dropped PA 5.4) |
| pseudorandom number generation, linear congruential | 200 | out-of-scope | how random-number generators are built (plan dropped PA 5.4) |
| PSPACE | 299 | taught | N103: PSPACE-hard named |
| Puma 560 robot | 107 | index-noise | robot product name (Puma 560) |
| pure strategy | 445 | taught | N54: pure vs mixed strategies |
| pursuit-evasion game | 627, 782, 783 | out-of-scope | pursuit-evasion games (plan dropped PA 12.6) |
| pursuit-evasion game, visibility-based (see visibility-based pursuit-evasion) |  | index-noise | cross-reference to visibility-based pursuit-evasion |
| pushing a box | 731–732 | taught | N292: pushing (nonprehensile manipulation) |
| Q-factor | 534 | taught | N21: Q-factor = action value |
| Q-learning | 534–535 | taught | N21: Q-learning |
| quadratic cost functional | 874 | taught | N205: quadratic cost (LQR) |
| quadratic potential function | 402 | add | **artificial potential fields (attractive and repulsive)** (robotics) → RO-05 (extend N109); quadratic attractive potential |
| quantiﬁed variables | 282 | out-of-scope | logic/quantifier elimination for exact algebraic planning (plan dropped PA 6.4-6.9) |
| quantiﬁer | 282 | out-of-scope | logic/quantifier elimination for exact algebraic planning (plan dropped PA 6.4-6.9) |
| quantiﬁer-elimination problem | 283 | out-of-scope | quantifier elimination: algebraic-geometry machinery (plan dropped PA 6.4-6.9) |
| quantiﬁer-free formula | 282 | out-of-scope | logic formula detail for exact algebraic planning (plan dropped PA 6.4-6.9) |
| quasi-static | 731 | add | **quasistatic assumption** (robotics) → RB-03 (extend N292); pushing and grasp analysis assume inertia is negligible; standard in manipulation courses |
| quaternion | 150–153 | taught | N65: quaternions (plan§4 3D rotations) |
| quaternion, from a rotation matrix | 153 | taught | N65: quaternion from rotation matrix (plan§4 3D rotations) |
| quotient topology | 136 | out-of-scope | point-set topology (quotient topology; plan dropped PA 4.1) |
| radar map | 275–276 | out-of-scope | exact cell decomposition detail for a rotating segment (research-level combinatorial planning) |
| radial sweep | 263, 406 | out-of-scope | computational-geometry sweep algorithm used inside exact roadmaps |
| random loop generator | 343, 345 | out-of-scope | closed-chain planning (plan dropped PA 7.5) |
| random sampling | 198–201 | taught | N108: uniform random samples for planners |
| random sampling, of SO(3) | 198–199 | taught | N108: uniform random rotations |
| random sampling, of directions | 199 | taught | N108: random directions |
| random sampling, tests | 200–201 | out-of-scope | statistical tests for random-number generators (plan dropped PA 5.4) |
| random variable | 444 | taught | MA-020: random variable |
| random-walk planner | 228 | taught | N109: random walk escape in randomized potential fields |
| randomized algorithm | 305 | taught | N110: randomized algorithms (RRT, PRM) |
| randomized lower value | 466, 542, 547 | out-of-scope | game-theory detail (randomized lower value); minimax taught N54 |
| randomized plan | 538, 545 | taught | N54: randomized (mixed) strategy |
| randomized potential ﬁeld | 224–227, 402 | taught | N109: randomized potential field |
| randomized potential ﬁeld, under diﬀerential constraints | 837 | out-of-scope | randomized potential field with differential constraints: research variant |
| randomized saddle point | 466 | taught | N54: saddle point in mixed strategies |
| randomized security plan | 542 | out-of-scope | game-theory detail (security plans in sequential games); minimax N54 |
| randomized strategy | 445–446 | taught | N54: mixed strategy |
| randomized upper value | 465 | out-of-scope | game-theory detail (randomized upper value) |
| randomized value | 466, 542 | taught | N54: value of a zero-sum game |
| range scanner | 604 | taught | N91: range scanner / LiDAR |
| range space (for discrepancy) | 206 | out-of-scope | discrepancy theory of samples (plan dropped PA 5.5) |
| rapidly exploring dense tree | 228–237, 314, 325, 340, 348 | taught | N110: RRT/RDT |
| rapidly exploring dense tree, exploration | 228–232 | taught | N110: RRT exploration |
| rapidly exploring dense tree, ﬁnding nearest points | 232–234 | taught | N108: nearest-point search for RRT |
| rapidly exploring dense tree, making planners | 235–237 | taught | N110: RRT-based planners |
| rapidly exploring dense tree, under diﬀerential constraints | 832–836 | taught | N112: kinodynamic RRT |
| rapidly exploring random tree (see rapidly exploring dense tree) |  | index-noise | cross-reference to rapidly exploring dense tree |
| Rapoport | 490 | index-noise | person name |
| rational decision maker | 460, 479, 481 | taught | N53: utility and rationality |
| RDT (see rapidly exploring dense tree) |  | index-noise | cross-reference (abbreviation RDT) |
| reachability graph | 804–805 | taught | N112: reachability graph / lattice |
| reachability tree | 802–804 | taught | N112: reachability tree of motion primitives |
| reachable set | 798–801 | taught | N112: reachable sets |
| reachable set, backward | 865 | out-of-scope | backward reachable sets in control theory proofs; recovery reach-avoid values named N197 |
| reachable set, for simple car models | 800 | taught | N112: reachable sets for cars |
| reactive plan (see feedback plan) |  | index-noise | cross-reference to feedback plan |
| real algebraic numbers | 286–287 | out-of-scope | algebraic number theory for exact planning (plan dropped PA 6.4-6.9) |
| reality television | 478–479 | index-noise | example name |
| reckless driving | 13 | index-noise | example name |
| recognizability | 582, 696 | out-of-scope | information-space theory detail (recognizability in preimage planning) |
| reconﬁgurable robot | 330 | out-of-scope | reconfigurable modular robots: research topic, no plan Note uses them |
| recontamination | 688 | out-of-scope | pursuit-evasion detail (plan dropped PA 12.6) |
| reduced visibility graph (see shortest-path roadmap) |  | index-noise | cross-reference to shortest-path roadmap |
| Reeds-Shepp car | 725, 794, 800, 845 | taught | N64: Reeds-Shepp car |
| Reeds-Shepp curves | 884–886 | taught | N112: Reeds-Shepp curves |
| reﬁnement of a plan | 22, 841 | out-of-scope | book-specific terminology (plan refinement in hierarchical planning) |
| reﬂex vertex | 261 | taught | N270: reflex vertices define the visibility graph |
| region of inevitable collision | 796–797 | add | **Inevitable collision states** (robotics) → RO-05 (extend N112); states from which a moving robot cannot stop in time; basis of safe kinodynamic planning |
| regret | 450–451, 462 | add | **Regret** (RL) → RL-01 (extend N4); standard measure of bandit/decision performance (loss vs best choice) |
| regret matrix | 450, 451 | add | **Regret** (RL) → RL-01 (extend N4); regret table in decision making |
| reinforcement learning | 527–535 | taught | N1: reinforcement learning |
| reinforcement learning, evaluating a plan | 530–534 | taught | N16: evaluating a plan by simulation |
| reinforcement learning, general framework | 528–530 | taught | N1: RL framework |
| reinforcement learning, terminology | 528 | taught | N1: RL terminology |
| reinforcement planning (see reinforcement learning) |  | index-noise | cross-reference to reinforcement learning |
| relative value iteration | 527 | out-of-scope | average-cost DP algorithm variant; the average-reward setting is taught in N27 |
| repulsive vertex | 404 | out-of-scope | navigation-function construction detail on cell complexes (book-specific) |
| reroute path | 646 | out-of-scope | pursuit-evasion detail (plan dropped PA 12.6) |
| resolution | 201 | taught | N111: resolution of a grid or sample set |
| resolution completeness | 186, 201, 224, 325, 805, 831, 836 | taught | N111: resolution completeness |
| resolution completeness, under diﬀerential constraints | 805–808 | out-of-scope | completeness proofs under differential constraints: research-level analysis |
| resultant |  | index-noise | group heading; sub-entries judged separately |
| resultant, force | 754 | taught | N220: net (resultant) force on a rigid body |
| resultant, moment | 754 | taught | N220: net moment (torque) on a rigid body |
| retraction method (see maximum-clearance roadmap) |  | index-noise | cross-reference to maximum-clearance roadmap |
| reverse-time system simulation | 816 | out-of-scope | backward-in-time simulation for bidirectional kinodynamic search: research-level implementation detail |
| revolute joint | 100, 101, 103, 105–108, 113, 114, 121, 124 | taught | N70: revolute joint |
| reward | 528 | taught | N1: reward |
| reward function | 439 | taught | N1: reward function |
| reward functional | 528 | taught | N8: return as a reward functional |
| reward space | 480 | taught | N53: multi-objective reward spaces and Pareto optimality |
| Riemannian manifold | 766 | out-of-scope | differential geometry (Riemannian manifolds; plan dropped PA 8.5) |
| Riemannian metric | 810–811 | out-of-scope | differential geometry (sub-Riemannian metrics for nonholonomic systems; plan dropped PA 15.10) |
| Riemannian tensor | 810 | out-of-scope | differential geometry (Riemannian tensor) |
| rigid-body dynamics (see dynamics, of a rigid body) |  | index-noise | cross-reference to dynamics of a rigid body |
| rigid-body transformations (see transformations, rigid body) |  | index-noise | cross-reference to rigid-body transformations |
| Rimon | 375, 409 | index-noise | person name |
| risk |  | index-noise | group heading; sub-entries judged separately |
| risk, conditional Bayes’ | 453 | taught | N53: Bayes risk = expected cost under the posterior |
| risk, frequentist | 484 | out-of-scope | statistical decision-theory detail (frequentist risk); expected-cost decisions taught N53 |
| RLG (see random loop generator) |  | index-noise | cross-reference (abbreviation RLG) |
| roadmap |  | taught | N111: roadmap |
| roadmap, directed | 315 | out-of-scope | directed roadmaps for time-varying problems: book-specific variant |
| roadmap, general requirements | 250–251 | taught | N111: roadmap requirements (accessibility, connectivity) |
| roadmap, maximum-clearance (see maximumclearance roadmap) |  | index-noise | cross-reference to maximum-clearance roadmap |
| roadmap, sampling-based (see sampling-based roadmap) |  | index-noise | cross-reference to sampling-based roadmap |
| roadmap, shortest-path (see shortest-path roadmap) |  | index-noise | cross-reference to shortest-path roadmap |
| Robbins-Monro algorithm (see stochastic iterative algorithm) |  | index-noise | cross-reference to stochastic iterative algorithm (Robbins-Monro taught N3) |
| robot displacement metric | 190 | taught | N108: distance between robot configurations |
| robot-robot collisions | 319 | taught | N271: robot-robot collisions in multi-robot planning |
| Rock-Paper-Scissors | 490, 493 | index-noise | example name (Rock-Paper-Scissors) illustrating mixed strategies N54 |
| roll rotation | 98 | taught | N65: roll angle (plan§4 3D rotations) |
| rolling a ball | 733–734 | index-noise | example name (rolling ball) illustrating nonholonomic constraints N64 |
| rotation |  | index-noise | group heading; sub-entries judged separately |
| rotation, 2D | 95–97 | taught | N65: 2D rotation (plan§4 rigid-body transforms) |
| rotation, 3D with quaternions | 150–152 | taught | N65: quaternions (plan§4 3D rotations) |
| rotation, 3D with yaw-pitch-roll | 98–100 | taught | N65: yaw-pitch-roll (plan§4 3D rotations) |
| RRT (see rapidly exploring dense tree) |  | index-noise | cross-reference to rapidly exploring dense tree |
| Rubik’s cube | 4, 5, 17, 30 | index-noise | example name (Rubik's cube) |
| Runge-Kutta (see numerical integration, Runge-Kutta, 424) |  | index-noise | cross-reference to numerical integration (Runge-Kutta in plan§4 Numerical integration of ODEs) |
| Russell and Norvig | 27 | index-noise | person names (textbook authors) |
| saddle point (see sequential game, saddle point, and zero-sum game, saddle point) |  | index-noise | cross-reference to game saddle points |
| sample point of a cell | 255 | taught | N270: sample point of a cell in cell decomposition |
| sample sequence | 195 | taught | N111: sample sequence for sampling-based planners |
| sample set | 195 | taught | N111: sample set |
| sample space (of a probability space) | 442 | taught | MA-010: sample space |
| sampling-based neighborhood graph | 416 | out-of-scope | book-specific feedback-planning construction (sampling-based neighborhood graph) |
| sampling-based planning |  | index-noise | group heading; sub-entries judged separately |
| sampling-based planning, for closed chains | 340–347 | out-of-scope | closed-chain planning (plan dropped PA 7.5) |
| sampling-based planning, philosophy | 185 | taught | N111: why sample instead of build the obstacle region exactly |
| sampling-based planning, time-varying | 314–315 | taught | N271: sampling-based planning with time-varying obstacles |
| sampling-based planning, under diﬀerential constraints | 810–837 | taught | N112: kinodynamic sampling-based planning |
| sampling-based planning, with feedback | 412–429, 837–841 | out-of-scope | sampling-based feedback planning: research-level construction (plan keeps grid DP feedback in N106) |
| sampling-based roadmap |  | index-noise | group heading; sub-entries judged separately |
| sampling-based roadmap, ǫ-goodness | 240 | out-of-scope | analysis/proof technique for PRM (epsilon-goodness) |
| sampling-based roadmap, analysis | 240–241 | out-of-scope | analysis/proof technique for PRM |
| sampling-based roadmap, basic method | 237–241 | taught | N111: basic PRM |
| sampling-based roadmap, boundary sampling | 243 | add | **Narrow passages and PRM sampling strategies** (robotics) → RO-05 (extend N111); uniform sampling misses narrow corridors; Gaussian, bridge-test and boundary sampling are standard course material |
| sampling-based roadmap, bridge-test sampling | 243–244 | add | **Narrow passages and PRM sampling strategies** (robotics) → RO-05 (extend N111); bridge-test sampling for narrow passages |
| sampling-based roadmap, Guassian sampling | 243 | add | **Narrow passages and PRM sampling strategies** (robotics) → RO-05 (extend N111); Gaussian sampling near obstacle boundaries |
| sampling-based roadmap, medial-axis sampling | 244 | add | **Narrow passages and PRM sampling strategies** (robotics) → RO-05 (extend N111); medial-axis sampling keeps samples away from obstacles |
| sampling-based roadmap, preprocessing phase | 238–239 | taught | N111: PRM preprocessing (build) phase |
| sampling-based roadmap, query phase | 240 | taught | N111: PRM query phase |
| sampling-based roadmap, vertex enhancement | 242–243 | add | **Narrow passages and PRM sampling strategies** (robotics) → RO-05 (extend N111); vertex enhancement adds samples where the roadmap is weak |
| sampling-based roadmap, visibility roadmap | 241–242 | taught | N111: visibility roadmap |
| sampling-based roadmaps | 237–244 | taught | N111: sampling-based roadmaps |
| sampling-based roadmaps, under diﬀerential constraints | 837 | taught | N185: roadmap edges checked against a controller (PRM-RL) / kinodynamic roadmaps |
| Sard’s Theorem | 411 | out-of-scope | proof technique (Sard's theorem, measure theory) |
| SB (see strong backprojection) |  | index-noise | cross-reference (abbreviation SB) |
| scalarization | 364 | taught | N53: scalarization of multi-objective costs |
| scaling an object | 121 | taught | MA-053: scaling as a linear map (plan§5 recap) |
| screw joint | 105 | taught | N70: screw joint among joint types |
| screw transformation | 106 | taught | N275: screw motion |
| sealing cracks | 7 | index-noise | example/application name |
| search algorithms | 318 | taught | N103: search algorithms |
| search algorithms, adaptation to continuous spaces | 220–224 | taught | N106: grid search over continuous C-space |
| search algorithms, under diﬀerential constraints | 818–820, 828–830 | taught | N113: search with motion primitives (hybrid A*, lattices N114) |
| search algorithms, uniﬁed view (see backward search see also bidirectional search see also forward search) | 41–43 | taught | N105: unified view of forward, backward and bidirectional search |
| search graph | 41, 217, 818 | taught | N103: search graph |
| searching an environment | 657 | taught | N181: searching/exploring an environment |
| second-order controllable systems | 919 | out-of-scope | nonholonomic controllability theory (plan dropped PA 15.5) |
| second-order diﬀerential drive | 744 | taught | N67: kinematic vs dynamic (acceleration-input) vehicle models |
| second-order unicycle | 743 | taught | N67: kinematic vs dynamic (acceleration-input) vehicle models |
| section (of a cylinder) | 290 | out-of-scope | cylindrical algebraic decomposition detail (plan dropped PA 6.4-6.9) |
| sector (of a cylinder) | 290 | out-of-scope | cylindrical algebraic decomposition detail (plan dropped PA 6.4-6.9) |
| security plan | 539–541, 546 | taught | N54: security (minimax) plan |
| security strategy | 461 | taught | N54: security strategy = minimax |
| security strategy, randomized | 465 | taught | N54: randomized security strategy = mixed minimax |
| selective sensor | 562 | out-of-scope | book-specific abstract sensor classification |
| semi-algebraic decomposition | 284 | out-of-scope | algebraic-geometry machinery (plan dropped PA 6.4-6.9) |
| semi-algebraic model | 87–89 | out-of-scope | semi-algebraic models (plan dropped PA 3.2) |
| semi-algebraic set | 87 | out-of-scope | semi-algebraic sets (plan dropped PA 3.2) |
| sensing history | 566 | taught | N77: history of actions and readings |
| sensor feedback | 581 | taught | N77: feedback from sensor readings via information state |
| sensor mapping | 561, 591 | taught | N74: sensor model |
| sensor observation | 560 | taught | N63: measurement/observation |
| sensor-based planning (see planning under sensing uncertainty) |  | index-noise | cross-reference to planning under sensing uncertainty |
| sensorless manipulation | 701 | out-of-scope | research topic (sensorless part orienting); plan teaches preimage planning N292 |
| sensorless planning | 582–585, 612–614 | out-of-scope | research topic (planning with no sensors) on nondeterministic I-spaces |
| sensors |  | index-noise | group heading; sub-entries judged separately |
| sensors, continuous | 598–605 | taught | N74: continuous sensor models |
| sensors, discrete | 561–564 | taught | N77: discrete sensor models |
| sequential game | 536–551 | taught | N54: sequential games |
| sequential game, against nature (see game against nature, sequential) |  | index-noise | cross-reference to game against nature |
| sequential game, information space of | 619–627 | out-of-scope | information spaces of games: advanced game theory |
| sequential game, Markov assumption | 496–497 | taught | N7: Markov assumption |
| sequential game, more than two players | 550–551 | taught | N54: nonzero-sum games with many players |
| sequential game, on state spaces | 544–551 | taught | N54: sequential games on state spaces |
| sequential game, saddle point | 542–544, 546, 619, 621–623, 626 | taught | N54: saddle point |
| sequential game, zero-sum with nature | 549–550 | taught | N54: zero-sum game against nature |
| shadow component | 674 | out-of-scope | pursuit-evasion detail (plan dropped PA 12.6) |
| shadow region | 674 | out-of-scope | pursuit-evasion detail (plan dropped PA 12.6) |
| shearing transformation | 121 | taught | MA-053: shear as a linear map (plan§5 recap) |
| shooting methods | 856 | taught | N116: shooting methods |
| shortest-path functional | 764 | out-of-scope | calculus of variations (plan dropped PA 13.9) |
| shortest-path roadmap | 261–264, 679 | taught | N270: shortest-path (visibility) roadmap |
| SICK LMS-200 | 604 | index-noise | product name (SICK laser scanner) |
| sigma algebra | 192 | out-of-scope | measure theory (plan dropped PA 5.2) |
| sign assignment | 284 | out-of-scope | cylindrical algebraic decomposition detail |
| sign sensor | 562 | out-of-scope | book-specific abstract sensor classification |
| sign-invariant region | 284 | out-of-scope | cylindrical algebraic decomposition detail |
| silhouette curves | 293, 296 | out-of-scope | Canny's roadmap algorithm detail (plan dropped PA 6.4-6.9) |
| silhouette method (see Canny’s roadmap algorithm) |  | index-noise | cross-reference to Canny's roadmap algorithm |
| simple polygon | 90 | taught | N71: polygonal obstacles |
| simple-car model | 722–726 | taught | N64: simple car model |
| simple-car model, two-car game | 783 | out-of-scope | differential games (plan dropped PA 13.12) |
| simple-car model, with nature | 781 | taught | N68: car motion with noise |
| simple-unicycle model | 729–730 | taught | N66: unicycle model |
| simplicial complex | 265–268 | out-of-scope | algebraic topology (plan dropped PA 4.1-4.7) |
| simply connected space | 141 | out-of-scope | algebraic topology (plan dropped PA 4.1-4.7) |
| Simpson paradox | 482 | out-of-scope | statistics paradox used in a decision-theory aside; different field (statistics), no robotics Note uses it |
| simulation-based dynamic programming (see reinforcement learning) |  | index-noise | cross-reference to reinforcement learning |
| simulation-based methods | 528 | taught | N16: simulation-based (Monte Carlo) evaluation |
| simulation-based planning (see reinforcement learning) |  | index-noise | cross-reference to reinforcement learning |
| simultaneous localization and mapping (see SLAM, 656) |  | taught | N100: SLAM |
| single query | 186, 217 | add | **single-query vs multi-query planners** (robotics) → RO-05 (extend N111); why RRT suits one query and PRM suits many; standard planner choice |
| single shooting | 857 | taught | N116: single shooting |
| singular 0-simplex | 267 | out-of-scope | algebraic topology (singular simplices) |
| singular 1-simplex | 266 | out-of-scope | algebraic topology (singular simplices) |
| singular k-simplex | 267 | out-of-scope | algebraic topology (singular simplices) |
| singular arcs | 878 | out-of-scope | optimal control theory detail (singular arcs; plan dropped PA 15.8) |
| singular complex | 265–267 | out-of-scope | algebraic topology (singular complex) |
| singular distribution | 895 | out-of-scope | differential geometry of distributions (plan dropped PA 15.11) |
| singular matrix | 295 | taught | MA-056: singular matrix = determinant 0 |
| singular point of a distribution | 895 | out-of-scope | differential geometry of distributions (plan dropped PA 15.11) |
| singular simplex | 266 | out-of-scope | algebraic topology (singular simplex) |
| singular value decomposition (SVD) | 516 | taught | MA-057: SVD |
| situation calculus | 69 | out-of-scope | logic-based symbolic planning (plan dropped PA 2.10-2.13) |
| skew symmetry | 904, 907 | out-of-scope | Lie-algebra identity in nonholonomic control theory (plan dropped PA 15.11) |
| SLAM | 655–684 | taught | N100: SLAM |
| SLAM, probabilistic | 679–684 | taught | N101: probabilistic SLAM |
| sliding-mode control | 389 | out-of-scope | graduate nonlinear robust control; plan handles model error by system ID and randomisation (plan dropped ME-069) |
| sliding-tile puzzle | 4, 5, 30 | index-noise | example/puzzle name (sliding-tile puzzle) |
| small-time local controllability | 722, 726, 845, 868–870, 883, 886, 888, 892, 903, 908–910, 921 | out-of-scope | nonholonomic controllability theory (plan dropped PA 15.5) |
| smooth diﬀerential drive | 744 | taught | N67: kinematic vs dynamic vehicle models |
| smooth distribution | 895 | out-of-scope | differential geometry of distributions (plan dropped PA 15.11) |
| smooth function | 385 | taught | MA-061: smooth (differentiable) function |
| smooth manifold | 134, 390–398, 895 | out-of-scope | differential geometry (smooth manifolds; plan dropped PA 8.5) |
| smooth manifold, RP n | 394–395 | out-of-scope | projective spaces: topology (plan dropped PA 4.1-4.7) |
| smooth manifold, R n | 393 | taught | MA-048: R^n as vectors |
| smooth manifold, S n | 393–394 | taught | N72: circle/sphere C-spaces in plain words |
| smooth manifold, Riemannian | 810–811 | out-of-scope | differential geometry (Riemannian manifolds) |
| smooth structure | 392 | out-of-scope | differential geometry (smooth structure) |
| smoothness of a function | 385 | taught | MA-061: smoothness/differentiability |
| Sobol sequence | 208 | out-of-scope | low-discrepancy sequences (plan dropped PA 5.6) |
| Sod’s Law | 448 | index-noise | joke/aside (Sod's Law) |
| Sokoban | 301 | index-noise | puzzle name (Sokoban) |
| solid representation | 81 | taught | N71: solid models from half-planes and meshes |
| solution in the sense of Filipov | 388 | out-of-scope | nonsmooth ODE solution theory (Filippov) beyond beginner depth |
| solution trajectory | 387, 398 | taught | N112: solution trajectory of an ODE (plan§4 ODEs and vector fields) |
| span of vector ﬁelds | 895 | out-of-scope | differential geometry of distributions (plan dropped PA 15.11) |
| spanning tree | 355 | add | **Spanning-tree coverage** (robotics) → RO-23 (extend N273); classic coverage planner: cover a grid by circling a spanning tree |
| spanning-tree covering | 355–357 | add | **Spanning-tree coverage** (robotics) → RO-23 (extend N273); spanning-tree covering of a grid |
| spatial constraints | 351 | out-of-scope | molecular-biology application (plan dropped PA 7.6) |
| special Euclidean group | 147–148, 154 | taught | N64: SE(2)/SE(3) as rigid-body transforms (plan§4) |
| special orthogonal group | 146 | taught | N65: rotation matrices SO(2)/SO(3) (plan§4 rigid-body transforms) |
| speedometer | 601 | taught | N86: wheel speed sensing / odometry |
| spherical coordinates | 397 | taught | N91: range-azimuth-elevation (spherical) coordinates |
| spherical joint | 105, 107, 113 | taught | N70: spherical joint |
| spherical linear interpolation | 189 | taught | N202: slerp |
| spine curve | 92 | out-of-scope | geometric-modelling detail (generalized cylinders) |
| spiral search | 673 | out-of-scope | online search competitive analysis: research-level |
| squeeze function | 702 | out-of-scope | sensorless part orienting research (squeeze function) |
| squeezing parts | 701–704 | out-of-scope | sensorless part orienting research (squeezing parts) |
| SSM (see swath-point selection method) |  | index-noise | cross-reference (abbreviation SSM) |
| stability of a system | 862–866 | taught | N117: stability of dynamical systems (plan§4) |
| stability of a system, asymptotic (see asymptotic stability) |  | index-noise | cross-reference to asymptotic stability |
| stability of a system, Lyapunov (see Lyapunov stability) |  | index-noise | cross-reference to Lyapunov stability |
| stability of a system, time-varying case | 864 | out-of-scope | nonlinear-control theory detail (time-varying stability) |
| stability of a system, uniform | 863 | out-of-scope | nonlinear-control theory detail (uniform stability) |
| stable conﬁguration space | 334 | taught | N292: stable configurations in manipulation planning (transit/transfer) |
| stage-dependent plan | 505 | taught | N9: time-dependent (nonstationary) plans |
| standard grid | 203 | taught | N106: grid over C-space |
| star algorithm | 159–161 | taught | N73: computing C-obstacles of polygons (Minkowski sum) |
| star-shaped regions | 411 | out-of-scope | research navigation-function construction (star-shaped worlds) |
| state estimation | 572–573 | taught | N78: state estimation by Bayes filtering |
| state history | 400 | taught | N77: state history |
| state mapping | 590 | out-of-scope | book-specific notation (state mapping) |
| state space | 28 | taught | N103: state space |
| state trajectory | 372, 400, 788 | taught | N112: state trajectory |
| state transition equation | 28, 29, 737, 738 | taught | N9: state transition equation |
| state transition function | 28, 29 | taught | N9: state transition function |
| state transition graph | 29 | taught | N103: state transition graph |
| state transition matrix | 502 | taught | N7: transition matrix (plan§4 Markov chains) |
| state-nature mapping | 590, 591 | out-of-scope | book-specific notation (state-nature mapping) |
| state-sensor mapping | 591 | out-of-scope | book-specific notation (state-sensor mapping) |
| state-space discretization | 828–832 | taught | N114: state-space discretization / lattices |
| stationary cost-to-go function | 51, 511, 512, 514 | taught | N11: stationary optimal value / cost-to-go |
| stationary diﬀerential equations | 387 | taught | N112: autonomous ODEs (plan§4 ODEs and vector fields) |
| statistical decision theory | 455 | taught | N53: decision theory with observations |
| steering methods | 817, 910–922 | out-of-scope | nonholonomic steering methods (plan dropped PA 15.12) |
| steering methods, piecewise-constant actions | 910–916 | out-of-scope | nonholonomic steering methods (plan dropped PA 15.12) |
| steering methods, sinusoidal action trajectories | 917–920 | out-of-scope | nonholonomic steering methods (plan dropped PA 15.12) |
| steering problem | 792 | taught | N112: steering problem solved by Dubins/Reeds-Shepp curves |
| Stentz’s algorithm | 362, 662–667 | taught | N107: D* (Stentz) |
| stereographic projection | 293, 394 | out-of-scope | topology (stereographic projection charts) |
| sticking | 693, 697, 699, 700 | taught | N288: sticking vs sliding contact |
| STLC (see small-time local controllability) |  | index-noise | cross-reference (abbreviation STLC) |
| stochastic control theory (see game against nature, sequential, 495) |  | index-noise | cross-reference to game against nature |
| stochastic diﬀerential equation | 781 | out-of-scope | stochastic calculus beyond beginner depth |
| stochastic fractal | 231 | out-of-scope | research aside (stochastic fractal nature of RRTs) |
| stochastic iterative algorithm | 533, 534 | taught | N3: stochastic approximation (Robbins-Monro) |
| stochastic shortest-path problem | 556 | taught | N8: episodic shortest-path MDP |
| strange topology | 131 | index-noise | example of a pathological topology |
| strategy | 452 | taught | N54: strategy |
| STRIPS | 27, 58–63 | add | **symbolic task planning (STRIPS/PDDL)** (robotics) → RB-03 (extend N293); LaValle 2.4: STRIPS states and operators, the task layer of TAMP |
| strong backprojection | 504, 696 | out-of-scope | preimage-planning detail beyond N292's beginner treatment |
| structure problem | 353 | out-of-scope | molecular-biology application (plan dropped PA 7.6) |
| sub-Riemannian metric | 811 | out-of-scope | differential geometry (sub-Riemannian) |
| subgroup | 146 | out-of-scope | group theory (plan dropped PA 4.6) |
| subjective probabilities | 485 | out-of-scope | philosophy of probability (subjective probabilities) |
| subspace topology | 130–131 | out-of-scope | point-set topology (plan dropped PA 4.1) |
| suﬃcient information mapping | 573 | taught | N78: belief as a sufficient summary of history |
| suﬃcient statistic | 573 | taught | N78: belief as a sufficient statistic |
| Sukharev grid | 203 | out-of-scope | dispersion theory of grids (plan dropped PA 5.5) |
| superquadric | 92 | out-of-scope | geometric-modelling detail (superquadrics) |
| supremum | 201, 439 | out-of-scope | analysis notation (supremum); max is enough at beginner level |
| Sussmann and Tang | 887 | index-noise | person names |
| swath | 229, 231, 803, 804, 809, 818 | out-of-scope | book-specific RDT construction detail (swath) |
| swath-point selection method | 231, 818 | out-of-scope | book-specific RDT construction detail |
| Swiss cheese | 141 | index-noise | example name |
| switching boundary | 388 | taught | N203: bang-bang switching in time-optimal scaling |
| switching time | 878 | taught | N203: switching time of bang-bang control |
| symmetric systems | 793–794 | out-of-scope | nonholonomic system theory (plan dropped PA 15.5) |
| symmetric Turing machine | 300 | out-of-scope | complexity theory |
| symmetry class | 644 | out-of-scope | book-specific combinatorial localization detail (symmetry classes) |
| symplectic manifold | 778 | out-of-scope | Hamiltonian mechanics (plan dropped PA 13.11) |
| system | 715, 793 | index-noise | group heading; sub-entries judged separately |
| system, determining whether controllable | 903–910 | out-of-scope | nonholonomic controllability theory (plan dropped PA 15.5) |
| system, determining whether nonholonomic | 892–903 | out-of-scope | nonholonomic system theory (plan dropped PA 15.10) |
| system, distribution | 895 | out-of-scope | differential geometry of distributions (plan dropped PA 15.11) |
| system, linear (see linear system) |  | index-noise | cross-reference to linear system |
| system, nonholonomic (see nonholonomic system theory) |  | index-noise | cross-reference to nonholonomic system theory |
| system, nonlinear (see nonlinear system) |  | index-noise | cross-reference to nonlinear system |
| system, simulator (see diﬀerential models) | 813–816 | taught | N112: system simulator |
| system vector ﬁelds | 891 | out-of-scope | nonholonomic system theory (plan dropped PA 15.10) |
| systematic search | 32–33 | taught | N103: systematic search |
| tangent bundle | 384, 738, 895 | out-of-scope | differential geometry (tangent bundle; plan dropped PA 8.5) |
| tangent point | 854 | out-of-scope | time-optimal phase-plane construction detail |
| tangent space | 384, 390, 396 | out-of-scope | differential geometry (tangent spaces; plan dropped PA 8.5) |
| tangent space, on a manifold | 395–397 | out-of-scope | differential geometry (tangent spaces; plan dropped PA 8.5) |
| TangentBug | 670 | taught | N107: bug algorithms |
| Tarski sentence | 282 | out-of-scope | logic/algebraic geometry (plan dropped PA 6.4-6.9) |
| Tarski-Seidenberg Theorem | 286 | out-of-scope | logic/algebraic geometry theorem (plan dropped PA 6.4-6.9) |
| Taylor series | 872, 873, 898, 899 | taught | MA-064: Taylor series |
| TD (see temporal diﬀerence) |  | index-noise | cross-reference (abbreviation TD) |
| team theory | 626 | out-of-scope | team theory: advanced game theory |
| temporal diﬀerence | 531–534 | taught | N19: temporal difference |
| temporal logic | 364 | taught | N197: formal methods named |
| termination action | 51, 568 | taught | N8: terminating episodes |
| THC | 17 | index-noise | example name (THC molecule) |
| theory of computation | 298 | out-of-scope | theory of computation |
| time scaling | 317, 792 | taught | N201: time scaling |
| time-invariant | 741 | taught | N64: time-invariant systems (plan§4 State-space models) |
| time-limited reachable set | 799 | taught | N112: reachable set |
| time-monotonic path | 313, 315–317 | taught | N271: time-monotonic paths in time-varying planning |
| time-optimal trajectory planning | 853–855 | taught | N203: time-optimal trajectory planning |
| time-varying motion planning | 311–318 | taught | N271: time-varying motion planning |
| time-varying motion planning, algebraic obstacle motion | 315 | out-of-scope | algebraic obstacle motion: exact algebraic planning (plan dropped PA 6.4-6.9) |
| time-varying motion planning, bounded speed | 315–316 | taught | N271: velocity tuning with bounded speed |
| time-varying motion planning, unbounded speed | 312–315 | taught | N271: time-varying planning with unbounded speed |
| timing function | 317 | taught | N271: timing function (path first, then timing) |
| tire skidding | 761 | taught | N251: tyre skidding / friction limit |
| Tit-for-Tat | 490 | index-noise | strategy name example (Tit-for-Tat) |
| topological complexity | 429 | out-of-scope | topology (plan dropped PA 4.1) |
| topological graph | 132–134, 803 | out-of-scope | topology (plan dropped PA 4.1) |
| topological manifold (see manifold) |  | index-noise | cross-reference to manifold |
| topological property | 845, 909 | out-of-scope | topology (plan dropped PA 4.1) |
| topological space | 128–134 | out-of-scope | point-set topology (plan dropped PA 4.1) |
| topological space, connected | 139, 140 | out-of-scope | formal topology (connectedness); plan teaches roadmap connectivity N111 |
| topological space, identiﬁcation | 136 | out-of-scope | topology (identification spaces; plan dropped PA 4.1) |
| topological space, metrizable | 187 | out-of-scope | topology (plan dropped PA 4.1) |
| topological space, path connected | 139 | out-of-scope | formal topology (path connectedness); plan teaches roadmap connectivity N111 |
| topological space, simply connected | 141 | out-of-scope | algebraic topology (plan dropped PA 4.1-4.7) |
| topologist’s sine curve | 139 | index-noise | example of a pathological space |
| topology |  | index-noise | group heading; sub-entries judged separately |
| topology, manifold (see manifold) |  | index-noise | cross-reference to manifold |
| topology, topological space (see topological space) |  | index-noise | cross-reference to topological space |
| torque | 751, 753, 771 | taught | N117: torque (short mechanics section) |
| torus | 137, 138, 143, 171, 172, 175 | taught | N72: torus C-space |
| total diﬀerential | 778, 779 | out-of-scope | Hamiltonian mechanics calculus (plan dropped PA 13.11) |
| tower exponentiation | 304 | out-of-scope | complexity-theory notation (tower exponentiation) |
| Towers of Hanoi | 368 | index-noise | puzzle name (Towers of Hanoi) |
| trailers | 730–731 | mentioned-only | **car with trailers (kinematic model)** (robotics) → RO-01 (extend N64); PA 13.3 row merged into N64 names trailers but N64 does not teach them; tractor-trailer is the standard hard nonholonomic case |
| trajectory | 387 | taught | N201: trajectory vs path |
| trajectory optimization | 855–857 | taught | N116: trajectory optimisation |
| trajectory planning | 792 | taught | N201: trajectory planning |
| trajectory planning, path-constrained | 846–855 | taught | N203: path-constrained (time-scaling) trajectory planning |
| transcription | 857 | taught | N116: direct transcription / collocation |
| transfer mode | 334 | taught | N292: transfer mode in manipulation planning |
| transfer path | 335 | taught | N292: transfer path |
| transformations |  | index-noise | group heading; sub-entries judged separately |
| transformations, 2D chain | 100–103 | taught | N69: 2D kinematic chains |
| transformations, 2D rigid body | 94–97 | taught | N64: 2D rigid transforms (plan§4 rigid-body transforms) |
| transformations, 3D chain | 103–112 | taught | N69: 3D kinematic chains |
| transformations, 3D rigid body | 97–100 | taught | N65: 3D rigid transforms (plan§4 rigid-body transforms) |
| transformations, general concepts | 92–94 | taught | MA-053: transformations as maps |
| transformations, kinematic tree | 112–120 | taught | N69: kinematic trees |
| transformations, nonrigid | 120–122 | taught | MA-053: nonrigid (scale, shear) transforms (plan§5 recap) |
| transit path | 335 | taught | N292: transit path |
| transition conﬁgurations (mode change) | 334 | taught | N292: mode changes between transit and transfer |
| translating a disc | 94 | index-noise | example name |
| trapezoidal decomposition (see vertical decomposition) |  | index-noise | cross-reference to vertical decomposition |
| trapped on a surface | 734–735 | index-noise | example name illustrating holonomic constraints |
| Traveling Salesman Problem | 354 | add | **travelling salesman problem (visiting many goals)** (robotics) → RO-23 (extend N274); ordering many goals (inspection, delivery, coverage) reduces to TSP; planning courses expect the name and hardness |
| tray tilting | 612–614, 701 | out-of-scope | sensorless part orienting research (tray tilting) |
| triangle fan | 91 | out-of-scope | computer-graphics storage detail (triangle fan) |
| triangle inequality | 187 | taught | N108: triangle inequality in metric rules |
| triangle model | 90–91 | taught | N71: triangle meshes |
| triangle strip | 91 | out-of-scope | computer-graphics storage detail (triangle strip) |
| triangular enumeration | 807 | out-of-scope | book-specific enumeration detail for resolution-complete search |
| triangulation | 250, 266, 268–269, 307, 403 | out-of-scope | computational-geometry polygon triangulation; cell decomposition taught N270 via vertical decomposition |
| tricycle | 725 | taught | N67: car-like (tricycle/bicycle) kinematics |
| trim trajectory | 809 | out-of-scope | research maneuver-automaton concept (trim trajectories) |
| trivial operator | 66 | out-of-scope | book-specific logic notation (trivial operator) |
| trivial topology | 131 | out-of-scope | point-set topology |
| Turing machine | 19, 299 | out-of-scope | theory of computation |
| two-point boundary value problem | 788, 792, 798, 805, 810, 816–820, 823, 830–832, 834, 835, 837, 855–857, 861, 862, 867, 910 | taught | N116: two-point boundary value problem solved by shooting |
| Type A contact (see Type EV contact) |  | index-noise | cross-reference to Type EV contact |
| Type B contact (see Type VE contact) |  | index-noise | cross-reference to Type VE contact |
| Type EE contact | 164, 167 | out-of-scope | exact polyhedral C-obstacle construction detail; Minkowski sum taught N73 |
| Type EV contact | 161, 162, 164–166, 184 | out-of-scope | exact polygon C-obstacle construction detail; Minkowski sum taught N73 |
| Type FV contact | 163, 167 | out-of-scope | exact polyhedral C-obstacle construction detail; Minkowski sum taught N73 |
| Type VE contact | 161, 162, 164–166, 182, 184 | out-of-scope | exact polygon C-obstacle construction detail; Minkowski sum taught N73 |
| Type VF contact | 164, 167 | out-of-scope | exact polyhedral C-obstacle construction detail; Minkowski sum taught N73 |
| Udupa | 127 | index-noise | person name |
| uncertainty |  | index-noise | group heading; sub-entries judged separately |
| uncertainty, brief overview | 435–436 | taught | N63: sources of uncertainty |
| uncertainty, due to partial predictability | 435, 496–535 | taught | N63: uncertainty in actions |
| uncertainty, due to sensing | 435, 559–627, 633–704 | taught | N63: uncertainty in perception |
| underactuated system | 722, 793, 804, 827–828 | taught | N221: underactuation |
| unicycle | 729–730, 743–744 | taught | N66: unicycle model |
| uniform random | 198 | taught | N108: uniform random samples |
| union-ﬁnd algorithm | 224, 239 | out-of-scope | data-structure implementation detail (union-find) inside PRM |
| unique point | 662 | out-of-scope | book-specific bug-algorithm detail |
| unit complex number | 149 | out-of-scope | second way to write 2D rotations (plan dropped PA 4.9) |
| unit quaternions | 150 | taught | N65: unit quaternions (plan§4 3D rotations) |
| unknot | 350 | out-of-scope | knot theory (plan dropped PA 7.6) |
| unsupervised classiﬁcation | 455 | taught | ML-122: clustering |
| unvisited states | 33 | taught | N103: unvisited states in search |
| upper envelope | 467 | out-of-scope | game-theory computation detail (upper envelope) |
| upper value of a game | 461, 539, 546 | taught | N54: upper value of a game |
| utility function | 482–483 | taught | N53: utility function |
| utility of money | 483 | index-noise | economics example (utility of money) |
| utility theory | 477–483 | taught | N53: utility theory |
| vacuum cleaning | 354 | index-noise | application example (vacuum cleaning) |
| value iteration | 45 | taught | N14: value iteration |
| value iteration, backward (see backward value iteration, 45–48) |  | index-noise | cross-reference to backward value iteration |
| value iteration, convergence issues | 511–514 | out-of-scope | convergence proofs of value iteration (proof technique) |
| value iteration, forward | 48–50 | out-of-scope | book-specific variant (forward value iteration) |
| value iteration, relative | 527 | out-of-scope | average-cost DP variant; average-reward setting taught N27 |
| value iteration, with interpolation | 418–422 | taught | N106: DP with interpolation |
| van der Corput sequence | 196–197, 204, 205, 207, 217, 238 | out-of-scope | low-discrepancy sequences (plan dropped PA 5.6) |
| variation of a function | 763 | out-of-scope | calculus of variations (plan dropped PA 13.9) |
| variety | 168, 170–171 | out-of-scope | algebraic varieties for closed chains (plan dropped PA 4.15) |
| variety, for 2D chains | 171–176 | out-of-scope | algebraic varieties for closed chains (plan dropped PA 4.15) |
| variety, for general linkages | 176–180 | out-of-scope | algebraic varieties for closed chains (plan dropped PA 4.15) |
| vector ﬁeld | 381–390, 398, 719 | taught | N112: vector fields (plan§4 ODEs and vector fields) |
| vector ﬁeld, equilibrium point | 862 | taught | N117: equilibrium points (plan§4 Stability of dynamical systems) |
| vector ﬁeld, normalized | 400 | out-of-scope | book-specific feedback-planning construction (normalized vector field) |
| vector ﬁeld, over a cell complex | 402–404 | out-of-scope | book-specific feedback-planning construction over cell complexes |
| vector ﬁeld, piecewise-smooth | 388–390 | out-of-scope | nonsmooth ODE theory beyond beginner depth |
| vector space | 382–383 | taught | MA-052: vector space, span and basis |
| vector space, R n over R | 383 | taught | MA-048: R^n |
| vector space, of functions | 383 | out-of-scope | functional analysis (function spaces) |
| velocity ﬁeld | 386–387 | taught | N112: velocity field (plan§4 ODEs and vector fields) |
| velocity-tuning method | 317–318 | taught | N271: velocity tuning |
| vertex selection method | 217–220, 226–228, 231 | out-of-scope | book-specific RDT/sampling framework detail |
| vertical decomposition | 253–258, 267–268, 319 | taught | N270: vertical cell decomposition |
| vertical decomposition, 3D | 270–273 | out-of-scope | exact 3D cell decomposition (plan dropped PA 6.4-6.9) |
| violation-free state | 796 | add | **Inevitable collision states** (robotics) → RO-05 (extend N112); violation-free states are those from which collision can still be avoided |
| virtual human | 11 | index-noise | application example (virtual humans) |
| VisBug | 670 | taught | N107: bug algorithms |
| visibility graph (see shortest-path roadmap) |  | index-noise | cross-reference to shortest-path roadmap |
| visibility polygon | 648 | out-of-scope | computational geometry for pursuit-evasion (plan dropped PA 12.6) |
| visibility region | 674 | out-of-scope | computational geometry for pursuit-evasion (plan dropped PA 12.6) |
| visibility roadmap | 241 | taught | N111: visibility roadmap |
| visibility sensor | 604, 647 | out-of-scope | book-specific abstract sensor classification |
| visibility skeleton | 649 | out-of-scope | computational geometry (visibility skeleton) |
| visibility-based pursuit-evasion | 684–691 | out-of-scope | pursuit-evasion (plan dropped PA 12.6) |
| visibility-based pursuit-evasion, a sequence of hard problems | 686 | out-of-scope | pursuit-evasion (plan dropped PA 12.6) |
| visibility-based pursuit-evasion, complete algorithm | 687–690 | out-of-scope | pursuit-evasion (plan dropped PA 12.6) |
| visibility-based pursuit-evasion, problem formulation | 684–687 | out-of-scope | pursuit-evasion (plan dropped PA 12.6) |
| visibility-based pursuit-evasion, variations | 690–691 | out-of-scope | pursuit-evasion (plan dropped PA 12.6) |
| Voronoi diagram | 200 | taught | N270: generalized Voronoi diagram |
| Voronoi region | 200, 208, 212–214, 618 | taught | N270: Voronoi regions |
| Voronoi vertex | 202 | taught | N270: Voronoi vertices |
| VSM (see vertex selection method) |  | index-noise | cross-reference (abbreviation VSM) |
| wall clock | 605 | out-of-scope | book-specific abstract sensor (wall clock) |
| wall following | 662 | taught | N107: wall following in bug algorithms |
| warping a path | 140 | out-of-scope | homotopy (algebraic topology) |
| wavefront | 357 | taught | N106: wavefront |
| wavefront propagation | 378–379, 428 | taught | N106: wavefront propagation |
| wavelet | 358 | out-of-scope | signal-processing aside in coverage discussion |
| way point | 406 | taught | N130: waypoints |
| WB (see weak backprojection) |  | index-noise | cross-reference (abbreviation WB) |
| weak backprojection | 504, 552, 696, 697 | out-of-scope | preimage-planning detail beyond N292's beginner treatment |
| weighted-region problem | 362 | taught | N98: region-dependent travel costs via costmaps |
| Weiner process | 781 | out-of-scope | stochastic calculus; discrete random walk taught N83 |
| Whitney’s embedding theorem | 134, 136 | out-of-scope | differential topology theorem |
| with probability one | 196 | out-of-scope | measure-theory phrasing; probabilistic completeness taught N111 |
| word (sequence of motion primitives) | 881 | out-of-scope | formal-language view of motion primitives (Lie algebra steering) |
| world | 81, 745 | taught | N63: world / environment |
| world frame | 94 | taught | N65: world frame |
| worst-case analysis | 448, 507, 570 | taught | N53: worst-case decisions |
| wrench (from mechanics) | 754 | taught | N275: wrench |
| yaw rotation | 98 | taught | N65: yaw angle (plan§4 3D rotations) |
| zero-sum game | 459–468 | taught | N54: zero-sum game |
| zero-sum game, matrix representation of | 460 | taught | N54: matrix games |
| zero-sum game, randomized saddle point | 466–468 | taught | N54: randomized saddle point |
| zero-sum game, randomized value of | 466 | taught | N54: value of a mixed-strategy game |
| zero-sum game, regret in | 462 | out-of-scope | game-theory detail; regret is added under RL-01 |
| zero-sum game, saddle point | 462–464 | taught | N54: saddle point |
| zero-sum game, value of | 462 | taught | N54: value of a game |

## Correll, Hayes, Heckman & Roncone, *Introduction to Autonomous Robots*

No free official copy has an index (MIT Press edition is not open access; the authors' free v3.0 PDF has no index). Term list = the authors' own \index{} entries in the official CC-licensed LaTeX source (github.com/Introduction-to-Autonomous-Robots/Introduction-to-Autonomous-Robots, commit cb5918c), plus every section heading (marked [section]/[subsection]); pages = printed pages of the authors' v3.0 release PDF (releases/download/v3.0/book.pdf).

Counts: taught 329, mentioned-only 0, add 87, out-of-scope 13, index-noise 49 (total 478).

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| Intelligence and embodiment [section] | 20 | index-noise | chapter section title (intro essay) |
| A roboticists' problem [section] | 21 | index-noise | chapter section title (intro essay) |
| Ratslife: an example of autonomous mobile robotics [section] | 5 | index-noise | example name (Ratslife robot game) |
| Autonomous mobile robots: some core challenges [section] | 5 | index-noise | chapter section title (overview) |
| Autonomous manipulation: some core challenges [section] | 24 | index-noise | chapter section title (overview) |
| End-effector | 25 | taught | N276: end-effector |
| The first industrial robot ``Unimate" [section] |  | out-of-scope | history (first industrial robot) |
| Take-home lessons [section] | 25, 82, 51, 106, 121, 139, 173, 197, 216, 231, 246, 260, 278, 315 | index-noise | chapter pointer (take-home lessons) |
| Exercises [section] | 25, 83, 51, 106, 122, 139, 160, 173, 198, 231, 246, 261, 278, 300, 316 | index-noise | chapter pointer (exercises) |
| Locomotion | 34 | taught | N295: locomotion (gaits; N307) |
| Manipulation | 34, 252 | taught | N292: manipulation |
| Locomotion and manipulation examples [section] | 35 | index-noise | chapter section title (examples) |
| Kinematics | 34, 56 | taught | N69: kinematics |
| Dynamics | 34 | taught | N281: dynamics |
| Compliance | 36, 120 | taught | N287: compliance |
| Static and dynamic stability [section] | 36 | taught | N295: static vs dynamic stability |
| Static stability | 36 | taught | N295: static stability |
| Dynamic Stability | 36 | taught | N295: dynamic stability |
| Degrees of freedom [section] | 37 | taught | N72: degrees of freedom |
| Degree of Freedom | 37 | taught | N72: degree of freedom |
| Cartesian | 37 | add | **Cartesian product of spaces** (maths) → RO-01 (extend N72); Correll 2.3: Cartesian degrees of freedom (x, y, z) as the product of independent axes |
| Cartesian Degree of Freedom |  | taught | N72: Cartesian DOF of a rigid body |
| Kinematic constraints | 40, 70 | taught | N64: kinematic constraints |
| Coordinate Systems and Frames of Reference [section] | 42 | index-noise | chapter section title |
| Pose | 42 | taught | N64: pose |
| Pitch | 42 | taught | plan§4 3D rotations: pitch |
| Yaw | 42 | taught | plan§4 3D rotations: yaw |
| Roll | 42 | taught | plan§4 3D rotations: roll |
| Bank | 42 | taught | plan§4 3D rotations: bank = roll (aviation name) |
| Attitude | 42 | taught | N86: attitude |
| Heading | 42 | taught | N64: heading |
| Frame of Reference | 47 | taught | N65: frame of reference |
| Matrix notation [subsection] | 43 | taught | plan§4 Rigid-body transforms: matrix notation for frames |
| Frame | 42 | taught | N65: frame |
| Mapping from one frame to another [subsection] | 47 | taught | N65: mapping between frames |
| Homogeneous Transform | 48 | taught | plan§4 Rigid-body transforms: homogeneous transform |
| Concatenation of Transformations [subsection] | 48 | taught | MA-054: concatenating transforms = matrix product |
| Other representations for orientation [subsection] | 48 | index-noise | section title; sub-entries judged |
| Euler Angles [subsubsection] | 49 | taught | plan§4 3D rotations: Euler angles |
| Fixed angle notation | 49 | add | **fixed-axis vs moving-axis (extrinsic vs intrinsic) rotation order** (maths) → MA 05-linear-algebra (planned 3D rotations Note); Correll 2.4.4: the same three angles give different rotations depending on fixed or moving axes; a common source of bugs |
| Euler angles | 49 | taught | plan§4 3D rotations: Euler angles |
| Singularity | 49, 76 | taught | N278: singularity (and gimbal lock in plan§4 3D rotations) |
| Quaternions [subsubsection] | 49 | taught | plan§4 3D rotations: quaternions |
| Quaternion | 50 | taught | plan§4 3D rotations: quaternion |
| Conjugate (Quaternion) | 50 | add | **quaternion algebra: conjugate, product, rotating a vector** (maths) → MA 05-linear-algebra (planned 3D rotations Note); Correll 2.4.4: rotating a vector with q v q* needs the conjugate and product |
| Euler axis | 50 | taught | plan§4 Axis-angle, exponential and log maps: Euler axis = rotation axis |
| Euler parameters | 50 | taught | plan§4 3D rotations: Euler parameters = unit quaternion |
| unit quaternion | 50 | taught | plan§4 3D rotations: unit quaternion |
| Dual quaternion | 50 | out-of-scope | dual quaternions are an advanced alternative pose representation (Correll names them in one paragraph); homogeneous matrices cover the need |
| Forward Kinematics | 56 | taught | N69: forward kinematics |
| Odometry | 73 | taught | N68: odometry |
| Inverse Kinematics | 56 | taught | N279: inverse kinematics |
| Differential Kinematics | 66, 56 | taught | N277: differential kinematics |
| Generalized Position | 56 | taught | N72: generalized position (configuration) |
| Generalized Configuration | 56 | taught | N72: generalized configuration |
| Forward Kinematics [section] | 56 | taught | N69: forward kinematics |
| Forward Kinematics of a simple robot arm [subsection] | 57 | taught | N69: FK of a simple arm |
| Configuration space | 58, 234 | taught | N72: configuration space |
| C-Space (Configuration space) | 58 | taught | N72: C-space |
| Workspace | 58 | taught | N276: workspace |
| The Denavit-Hartenberg notation [subsection] | 59 | taught | N69: DH notation |
| Denavit-Hartenberg parameters | 59 | taught | N69: DH parameters |
| Inverse Kinematics [section] | 62 | taught | N279: inverse kinematics |
| Solvability [subsection] | 63 | taught | N279: IK solvability |
| Inverse Kinematics of a Simple Manipulator Arm [subsection] | 63 | taught | N279: IK of a 2-link arm |
| Differential Kinematics [section] | 66 | taught | N277: differential kinematics |
| Forward Differential Kinematics [subsection] | 66 | taught | N277: forward differential kinematics |
| Twist (velocity) | 67 | taught | N275: twist |
| Velocity Twist | 67 | taught | N275: velocity twist |
| Jacobian Matrix | 67 | taught | N277: Jacobian matrix |
| Forward Kinematics of a Differential Wheeled Robot [subsection] | 67 | taught | N64: diff-drive forward kinematics |
| Non-holonomic | 68 | taught | N64: nonholonomic |
| Holonomic | 68 | taught | N64: holonomic |
| From Forward Kinematics to Odometry [subsubsection] | 73 | taught | N68: odometry from forward kinematics |
| Forward kinematics of Car-like steering [subsection] | 74 | taught | N67: car-like steering kinematics |
| Ackermann steering | 74 | taught | N67: Ackermann steering |
| Turntable steering | 74 | add | **steering mechanisms: turntable, Ackermann, skid steer** (robotics) → RO-01 (extend N66); Correll 3.3.3: turntable (articulated) steering is the other car-like layout; field and toy robots use it |
| Inverse Differential Kinematics [section] | 75 | taught | N280: inverse differential kinematics |
| Inverse Kinematics using Feedback Control [subsection] |  | taught | N280: IK by feedback on the error |
| Gradient Descent | 181 | taught | ML-056: gradient descent |
| Feedback Control | 76 | taught | N117: feedback control |
| Inverse Jacobian | 84 | taught | N280: inverse Jacobian |
| Inverse Differential Kinematics | 75 | taught | N280: inverse differential kinematics |
| Damped Least-Squares Method | 77 | taught | N280: damped least squares |
| Inverse Kinematics of Mobile Robots [subsection] | 77 | taught | N66: inverse kinematics of mobile bases |
| Inverse kinematics of an omnidirectional robot [subsubsection] | 78 | taught | N66: omnidirectional base kinematics |
| Swedish Wheel | 78 | taught | N66: Swedish wheel |
| Meccano Wheel | 78 | taught | N66: mecanum wheel |
| Feedback Control for Mobile Robots [subsection] | 80 | taught | N120: feedback control for mobile robots (drive to a pose) |
| Under-actuation and Over-actuation [subsection] | 80 | add | **under-, fully and over-actuated robots** (robotics) → RO-01 (extend N66); Correll 3.4.3: counts actuators vs DOF; explains why a car or quadrotor cannot move sideways directly |
| Fully actuated | 80 | add | **under-, fully and over-actuated robots** (robotics) → RO-01 (extend N66); fully actuated (Correll 3.4.3) |
| Under actuated | 81 | add | **under-, fully and over-actuated robots** (robotics) → RO-01 (extend N66); under-actuated (Correll 3.4.3); N221 names it only for quadrotors |
| Over actuation | 81 | add | **under-, fully and over-actuated robots** (robotics) → RO-01 (extend N66); over-actuated (Correll 3.4.3) |
| Kinematic deficiency | 81 | add | **under-, fully and over-actuated robots** (robotics) → RO-01 (extend N66); kinematic deficiency (Correll 3.4.3) |
| Kinematic redundancy | 82 | taught | N278: kinematic redundancy |
| Coordinate systems [subsection] | 58 | index-noise | exercise-section title |
| Forward and inverse kinematics [subsection] | 82 | index-noise | exercise-section title |
| Statics | 88 | taught | N277: statics |
| Statics [section] | 88 | taught | N277: statics |
| Mechanical Equilibrium | 88 | add | **static equilibrium: forces and torques sum to zero** (robotics) → RO-17 (extend N220); Correll 4.1: the base of statics, grasp analysis and support polygons |
| Static Equilibrium |  | add | **static equilibrium: forces and torques sum to zero** (robotics) → RO-17 (extend N220); static equilibrium (Correll 4.1) |
| Generalized Force | 89 | taught | N281: generalized force |
| Wrench | 89, 100 | taught | N275: wrench |
| Spatial Force | 89 | taught | N275: spatial force = wrench |
| Force Control | 90 | taught | N286: force control |
| Kineto-Statics Duality [section] | 90 | taught | N277: kineto-statics duality (τ = Jᵀ F) |
| Kineto-Statics Duality | 88 | taught | N277: kineto-statics duality |
| Manipulability [section] | 91 | taught | N278: manipulability |
| Manipulability Ellipsoid in Velocity space [subsection] | 91 | taught | N278: velocity manipulability ellipsoid |
| Velocity Manipulability Ellipsoid | 92 | taught | N278: velocity manipulability ellipsoid |
| Manipulability Ellipsoid in Force space [subsection] | 92 | add | **acceleration and force ellipsoids** (robotics) → RB-01 (extend N278); force manipulability ellipsoid (Correll 4.3.2) |
| Force Manipulability Ellipsoid | 92 | add | **acceleration and force ellipsoids** (robotics) → RB-01 (extend N278); force manipulability ellipsoid (Correll 4.3.2) |
| Manipulability Considerations [subsection] | 94 | taught | N278: manipulability considerations |
| Force interactions and compliance [section] |  | taught | N287: force interaction and compliance |
| Dynamics [section] | 51 | taught | N281: dynamics |
| Grasping | 98 | taught | N290: grasping |
| The theory of grasping [section] | 99 | taught | N290: grasping theory |
| Friction [subsection] | 98 | taught | N288: friction |
| Friction | 98 | taught | N288: friction |
| Coloumb Friction | 98 | taught | N288: Coulomb friction |
| Grasping wrench space | 100 | taught | N291: grasp wrench space |
| Multiple contacts and deformation [subsection] | 100 | add | **soft and deformable contacts** (robotics) → RB-03 (extend N288); Correll 5.1.2: real fingertips deform, which spreads contact into an area and adds torsional friction |
| Suction [subsection] | 101 | add | **suction grippers** (robotics) → RB-03 (new section in N291); Correll 5.1.3: the most common industrial pick tool; needs its own contact model |
| Simple grasping mechanisms [section] | 102 | add | **gripper mechanisms: parallel jaw, linkages, suction, multi-finger** (robotics) → RB-03 (new Note before N290); Correll 5.2: what the hardware can grasp decides every later grasp-planning step |
| 1-DoF scissor-like gripper [subsection] | 102 | add | **gripper mechanisms: parallel jaw, linkages, suction, multi-finger** (robotics) → RB-03 (new Note before N290); scissor gripper (Correll 5.2.1) |
| Parallel jaw [subsection] | 103 | add | **gripper mechanisms: parallel jaw, linkages, suction, multi-finger** (robotics) → RB-03 (new Note before N290); parallel-jaw gripper (Correll 5.2.2) |
| 4-bar linkage parallel gripper [subsection] | 105 | add | **gripper mechanisms: parallel jaw, linkages, suction, multi-finger** (robotics) → RB-03 (new Note before N290); four-bar linkage gripper (Correll 5.2.3) |
| Multi-fingered hands [subsection] | 105 | taught | N331: multi-fingered hands |
| Actuators | 114 | taught | N283: actuators |
| Electric motors [section] | 114 | taught | N283: electric motors |
| Dynamic | 114 | index-noise | stray index tag 'Dynamic' (no concept of its own) |
| AC and DC motors [subsection] | 114 | add | **electric motor types: DC, brushless, stepper, servo, AC** (robotics) → RB-02 (new Note before N283); Correll 6.1: choosing an actuator is the first hardware decision; N283 covers gearing but not motor types |
| Magnetomotive force | 114 | out-of-scope | magnetomotive force is electromagnetics (Correll 6.1.1 physics background) |
| MMF---magnetomotive force | 114 | out-of-scope | magnetomotive force is electromagnetics |
| AC motors [subsubsection] | 114 | add | **electric motor types: DC, brushless, stepper, servo, AC** (robotics) → RB-02 (new Note before N283); AC motors (Correll 6.1.1) |
| Rotor | 114 | add | **DC motor model: torque constant and back-EMF** (control) → RB-02 (extend N283); rotor (Correll 6.1.1) |
| Stator | 114 | add | **DC motor model: torque constant and back-EMF** (control) → RB-02 (extend N283); stator (Correll 6.1.1) |
| Alternating Current | 114 | out-of-scope | alternating current is electrical-engineering background |
| Alternating Current (AC) | 114 | out-of-scope | alternating current is electrical-engineering background |
| DC motors [subsubsection] | 114 | add | **electric motor types: DC, brushless, stepper, servo, AC** (robotics) → RB-02 (new Note before N283); DC motors (Correll 6.1.1) |
| commutator | 115 | add | **DC motor commutation (brushed vs brushless)** (control) → RB-02 (extend N283); commutator (Correll 6.1.1) |
| Direct Current | 115 | out-of-scope | direct current is electrical-engineering background |
| Direct Current (DC) | 115 | out-of-scope | direct current is electrical-engineering background |
| Stepper motor [subsection] | 116 | add | **electric motor types: DC, brushless, stepper, servo, AC** (robotics) → RB-02 (new Note before N283); stepper motor (Correll 6.1.2) |
| Rotations per minute | 116 | index-noise | unit (rotations per minute) |
| Rotations per minute (RPM) | 116 | index-noise | unit (RPM) |
| Stepper motor | 116 | add | **electric motor types: DC, brushless, stepper, servo, AC** (robotics) → RB-02 (new Note before N283); stepper motor (Correll 6.1.2) |
| Brushless DC motor [subsection] | 117 | add | **electric motor types: DC, brushless, stepper, servo, AC** (robotics) → RB-02 (new Note before N283); brushless DC motor (Correll 6.1.3) |
| brushless DC motor | 117 | add | **electric motor types: DC, brushless, stepper, servo, AC** (robotics) → RB-02 (new Note before N283); brushless DC motor |
| Servo motor [subsection] | 114 | add | **electric motor types: DC, brushless, stepper, servo, AC** (robotics) → RB-02 (new Note before N283); servo motor (Correll 6.1.4) |
| servo motors | 117 | add | **electric motor types: DC, brushless, stepper, servo, AC** (robotics) → RB-02 (new Note before N283); servo motors |
| linear actuator | 118 | add | **electric motor types: DC, brushless, stepper, servo, AC** (robotics) → RB-02 (new Note before N283); linear actuators (Correll 6.1) |
| Motor controllers [subsection] | 118 | add | **motor drivers: PWM and H-bridge** (control) → RB-02 (extend N283); Correll 6.1.5: how a controller's command becomes motor current; every robot uses one |
| Hydraulic and pneumatic actuators [section] | 119 | add | **hydraulic and pneumatic actuators** (robotics) → RB-02 (new Note before N283); Correll 6.2: actuators behind heavy legged robots and soft grippers |
| Hydraulic actuators [subsection] | 119 | add | **hydraulic and pneumatic actuators** (robotics) → RB-02 (new Note before N283); hydraulic actuators (Correll 6.2.1) |
| Pneumatic actuators and soft robotics [subsection] | 119 | add | **hydraulic and pneumatic actuators** (robotics) → RB-02 (new Note before N283); pneumatic actuators and soft robotics (Correll 6.2.2) |
| Other actuators [section] | 120 | add | **electric motor types: DC, brushless, stepper, servo, AC** (robotics) → RB-02 (new Note before N283); other actuators (Correll 6.2) |
| Safety considerations [section] | 120 | add | **collaborative robots and physical safety** (robotics) → RB-02 (extend N287); Correll 6.3: force limits, compliance and power failure behaviour that let robots work beside people |
| Collaborative robot | 120 | add | **collaborative robots and physical safety** (robotics) → RB-02 (extend N287); collaborative robot (Correll 6.3) |
| Cobot |  | add | **collaborative robots and physical safety** (robotics) → RB-02 (extend N287); cobot (Correll 6.3) |
| Series Elastic Actuators | 121 | add | **series elastic actuators** (robotics) → RB-02 (extend N283); series elastic actuators (Correll 6.3) |
| Power failure | 121 | add | **collaborative robots and physical safety** (robotics) → RB-02 (extend N287); power failure: brakes and back-drivability (Correll 6.3) |
| Robotic Sensors [section] |  | index-noise | chapter title |
| Terminology [section] | 127 | index-noise | section title; sub-entries judged |
| Active sensor | 127 | add | **sensor terminology: active/passive, range, resolution, accuracy, precision, bandwidth** (robotics) → RO-03 (new Note before N83); Correll 7.1: the words used to compare and choose every sensor |
| Passive sensor | 127 | add | **sensor terminology: active/passive, range, resolution, accuracy, precision, bandwidth** (robotics) → RO-03 (new Note before N83); passive sensor (Correll 7.1) |
| Range (sensor) | 127 | add | **sensor terminology: active/passive, range, resolution, accuracy, precision, bandwidth** (robotics) → RO-03 (new Note before N83); sensor range (Correll 7.1) |
| Dynamic Range (sensor) | 127 | add | **sensor terminology: active/passive, range, resolution, accuracy, precision, bandwidth** (robotics) → RO-03 (new Note before N83); dynamic range (Correll 7.1) |
| Decibel | 127 | add | **decibels (logarithmic ratio scale)** (maths) → RO-03 (new Note before N83); Correll 7.1: dynamic range and signal-to-noise are given in dB |
| Resolution (sensor) | 127 | add | **sensor terminology: active/passive, range, resolution, accuracy, precision, bandwidth** (robotics) → RO-03 (new Note before N83); resolution (Correll 7.1) |
| Accuracy (sensor) | 127 | add | **sensor terminology: active/passive, range, resolution, accuracy, precision, bandwidth** (robotics) → RO-03 (new Note before N83); accuracy (Correll 7.1) |
| Precision (sensor) | 126 | add | **sensor terminology: active/passive, range, resolution, accuracy, precision, bandwidth** (robotics) → RO-03 (new Note before N83); precision vs accuracy (Correll 7.1) |
| Bandwidth (sensor) | 128 | add | **sensor terminology: active/passive, range, resolution, accuracy, precision, bandwidth** (robotics) → RO-03 (new Note before N83); bandwidth (Correll 7.1); ties to frequency response |
| Proprioception vs. Exteroception [subsection] | 128 | taught | N142: proprioception vs exteroception |
| Proprioception | 128 | taught | N142: proprioception |
| Exteroception of the physical interaction with the environment [section] |  | index-noise | section title |
| Exteroception | 128 | taught | N143: exteroception |
| Proprioception of the internal state of the robot [section] |  | index-noise | section title |
| Sensors that measure the robot's joint configuration [section] | 129 | index-noise | section title; sub-entries judged |
| Encoder | 126 | add | **encoders: incremental (quadrature) and absolute** (robotics) → RO-03 (extend N86); Correll 7.2: how joint angles and wheel turns are measured; N86 uses encoders without teaching them |
| Quadrature encoder | 129 | add | **encoders: incremental (quadrature) and absolute** (robotics) → RO-03 (extend N86); quadrature encoder gives direction from two phase-shifted channels (Correll 7.2) |
| Gray code | 130 | add | **encoders: incremental (quadrature) and absolute** (robotics) → RO-03 (extend N86); Gray code in absolute encoders (Correll 7.2) |
| Sensors that measure ego-motion [section] | 130 | index-noise | section title; sub-entries judged |
| Inertia | 130 | taught | N220: inertia |
| Accelerometers [subsection] | 126 | taught | N83: accelerometers |
| Accelerometer | 126 | taught | N83: accelerometer |
| Hooke's law | 130 | add | **springs and dampers (Hooke's law)** (robotics) → plan§4 Newtonian and rigid-body mechanics (short section in N117); Correll 7.3.1: spring force = stiffness x stretch; base of accelerometers, impedance control and series elastic actuators |
| Gyroscopes [subsection] | 130 | taught | N83: gyroscopes |
| Rate gyro | 131 | taught | N83: rate gyro |
| Gyroscope | 130 | taught | N83: gyroscope |
| Inertial Measurement Unit | 131 | taught | N83: IMU |
| IMU | 131 | taught | N83: IMU |
| Measuring force [section] | 132 | index-noise | section title; sub-entries judged |
| Series Elastic Actuator | 132 | add | **series elastic actuators** (robotics) → RB-02 (extend N283); SEA as a force sensor (Correll 7.4) |
| Force/Torque sensor | 133 | add | **force/torque sensors (strain gauges)** (robotics) → RB-02 (new section in N286); Correll 7.4: wrist F/T sensors measure the wrench used by force control |
| Measuring pressure or touch [subsection] | 133 | taught | N294: pressure and touch sensing |
| Artificial skin | 134 | taught | N294: artificial skin (tactile) |
| Artificial skins for robotics [subsection] |  | taught | N294: artificial skins |
| Sensors to measure distance [section] | 135 | index-noise | section title; sub-entries judged |
| Light-based distance sensors [subsection] | 134 | add | **proximity and contact sensors (bumpers, infrared, ultrasonic)** (robotics) → RO-03 (new Note before N83); Correll 7.5: light-based distance sensors |
| Reflection [subsection] | 127 | add | **proximity and contact sensors (bumpers, infrared, ultrasonic)** (robotics) → RO-03 (new Note before N83); reflection (intensity) ranging (Correll 7.5.1) |
| Phase shift [subsection] | 131 | add | **range measurement principles: time of flight vs phase shift** (robotics) → RO-03 (extend N91); Correll 7.5.2: phase-shift ranging is how many lidars and ToF cameras measure distance |
| Laser range finder | 136 | taught | N91: laser range finder |
| Laser Range Scanners | 137 | taught | N91: laser range scanners |
| Lidar | 137 | taught | N91: lidar |
| Time-of-flight [subsection] | 135 | taught | N91: time of flight |
| Ultrasound distance sensors [subsubsection] | 137 | add | **proximity and contact sensors (bumpers, infrared, ultrasonic)** (robotics) → RO-03 (new Note before N83); ultrasound distance sensors (Correll 7.5.3) |
| Sensors to sense global pose [section] | 138 | taught | N85: global pose sensors (GNSS) |
| Images as two-dimensional signals [section] |  | add | **Fourier transform, frequency spectrum and FFT** (maths) → MA 06-calculus (new Note); Correll 8.1: an image (or any signal) as a sum of frequencies; base of low-pass and band-pass filters |
| From signals to information [section] | 149 | index-noise | section title (essay) |
| Basic image operations [section] | 152 | index-noise | section title; sub-entries judged |
| Threshold-based operations [subsection] | 152 | add | **image thresholding and binary images** (vision) → RO-18 (extend N227); Correll 8.3.1: simplest segmentation; colour thresholds are used in many robot demos |
| Convolution-based filters [subsection] | 152 | taught | N227: convolution-based image filters |
| Convolution | 152, 336 | taught | DL-042: convolution |
| Filter | 152 | taught | N227: image filter |
| Gaussian smoothing [subsubsection] | 153 | taught | N227: Gaussian smoothing |
| Gaussian filter | 153 | taught | N227: Gaussian filter |
| Low-pass filter | 148 | add | **frequency view of filters: low-pass, high-pass, band-pass** (vision) → RO-18 (extend N227); Correll 8.3.2: smoothing is a low-pass filter; LoG/DoG are band-pass; same idea filters IMU and encoder signals |
| Edge detection [subsubsection] | 154 | taught | N227: edge detection (gradient filters) |
| Sobel filter | 154 | taught | N227: Sobel gradient filter |
| Canny edge detector | 155 | add | **Canny edge detector** (vision) → RO-18 (extend N227); Correll 8.3.2: the standard edge detector (smooth, gradient, non-max suppression, hysteresis) |
| Difference of Gaussians [subsubsection] | 155 | taught | N228: difference of Gaussians (scale space) |
| Difference of Gaussians (DoG) | 155 | taught | N228: difference of Gaussians |
| Band-pass filter | 155 | add | **frequency view of filters: low-pass, high-pass, band-pass** (vision) → RO-18 (extend N227); band-pass filter (Correll 8.3.2) |
| Laplacian of Gaussian | 155 | add | **image Laplacian and Laplacian of Gaussian** (vision) → RO-18 (extend N227); Correll 8.3.2: second-derivative edge/blob detector; DoG approximates it (SIFT) |
| Morphological Operations [subsection] | 155 | add | **morphological operations: erosion and dilation** (vision) → RO-18 (extend N227); Correll 8.3.3: clean binary masks and grow obstacles in grid maps |
| Erosion | 155 | add | **morphological operations: erosion and dilation** (vision) → RO-18 (extend N227); erosion (Correll 8.3.3) |
| Dilation | 155 | add | **morphological operations: erosion and dilation** (vision) → RO-18 (extend N227); dilation (Correll 8.3.3); costmap inflation is a dilation |
| Extracting Structure from Vision [section] | 156 | index-noise | section title; sub-entries judged |
| Stereo Vision | 156 | taught | N90: stereo vision |
| Structure From Motion | 156 | taught | N235: structure from motion |
| Epipolar Line | 158 | taught | N232: epipolar line |
| Structured light | 158 | taught | N90: structured light |
| Depth from Focus |  | out-of-scope | depth from focus is a camera/microscopy technique; robot depth sensing is taught via stereo, structured light and ToF (N90) |
| Depth from Stereo |  | taught | N90: depth from stereo |
| Computer Vision and Machine Learning [section] |  | index-noise | section title |
| Features | 164 | taught | N227: image features |
| Feature detection as an information-reduction problem [section] |  | index-noise | section title |
| Features [section] | 164 | taught | N227: features |
| Harris Corner Detector | 164 | taught | N227: Harris corner detector |
| SIFT features | 164 | taught | N228: SIFT features |
| Line recognition [section] | 165 | add | **line extraction from 2D scans (split-and-merge)** (robotics) → RO-03 (extend N92); Correll 9.2: turning laser points into wall lines for maps and localisation |
| Line fitting using least squares [subsection] | 166 | taught | ML-050: least-squares line fitting |
| Least-Squares Method (Line fitting) | 167 | taught | ML-050: least-squares method |
| Split-and-merge algorithm [subsection] | 167 | add | **line extraction from 2D scans (split-and-merge)** (robotics) → RO-03 (extend N92); split-and-merge (Correll 9.2.2) |
| RANSAC: Random Sample and Consensus [subsection] | 168 | taught | N229: RANSAC |
| RANSAC | 168 | taught | N229: RANSAC |
| Random Sample and Consensus | 168 | taught | N229: random sample consensus |
| The Hough transform [subsection] | 169 | add | **Hough transform** (vision) → RO-18 (extend N229); Correll 9.2.4: voting method for lines and circles; classic lane and wall detector |
| Hough transform | 169 | add | **Hough transform** (vision) → RO-18 (extend N229); Hough transform |
| Scale-invariant feature transforms [section] | 170 | taught | N228: scale-invariant features |
| SIFT | 170 | taught | N228: SIFT |
| SURF | 170 | taught | N228: SURF named as a faster SIFT variant |
| Overview [subsection] | 170, 358 | index-noise | generic subsection title 'Overview' |
| Object Recognition using scale-invariant features [subsection] | 172 | taught | N228: object recognition by feature matching |
| Feature detection and machine learning [section] | 173 | taught | DL-040: feature detection with machine learning (CNNs) |
| Artificial Neural Networks | 178 | taught | DL-002: artificial neural networks |
| Deep Learning | 178 | taught | DL-002: deep learning |
| Classification (neural networks) | 178 | taught | ML-003: classification |
| Regression (neural networks) | 178 | taught | ML-003: regression |
| The simple Perceptron [section] | 178 | taught | DL-004: perceptron |
| Perceptron | 178 | taught | DL-004: perceptron |
| Heaviside step function | 179 | taught | DL-004: Heaviside step activation |
| Geometric interpretation of the simple perceptron [subsection] | 179 | taught | DL-005: geometric view of the perceptron |
| Training the simple perceptron [subsection] | 180 | taught | DL-005: training the perceptron |
| Learning Rate | 181 | taught | ML-056: learning rate |
| Activation Functions [section] | 181 | taught | DL-027: activation functions |
| Sigmoid function | 182 | taught | ML-071: sigmoid |
| Rectified Linear Unit (ReLU) | 182 | taught | DL-028: ReLU |
| From the simple perceptron to Multi-layer neural networks [section] | 178 | taught | DL-008: multi-layer networks |
| Input Layer | 183 | taught | DL-008: input layer |
| Hidden Layer | 183 | taught | DL-008: hidden layer |
| Output Layer | 183 | taught | DL-008: output layer |
| Formal description of Artificial Neural Networks [subsection] | 184 | taught | DL-010: formal description of an ANN |
| Inputs and outputs [subsubsection] | 184 | taught | DL-010: inputs and outputs |
| Activation (neural network) | 184 | taught | DL-010: activation |
| Training a multi-layer neural network [subsection] | 185 | taught | DL-016: training a multi-layer network (backprop) |
| Loss function [subsubsection] | 186 | taught | DL-014: loss function |
| Training set | 186 | taught | ML-001: training set |
| From single outputs to higher dimensional data [section] | 186 | index-noise | section title |
| One-Hot Encoding [subsubsection] | 187 | taught | ML-026: one-hot encoding |
| Softmax output [subsubsection] | 187 | taught | ML-078: softmax output |
| Softmax (neural network) | 187 | taught | ML-078: softmax |
| Objective functions and optimization [section] | 188 | taught | DL-014: objective functions |
| Loss functions for regression tasks [subsection] | 188 | taught | DL-014: regression losses |
| Regression | 188 | taught | ML-049: regression |
| Huber Loss (neural networks) | 189 | taught | DL-014: Huber loss |
| Loss functions for classification tasks [subsection] | 189 | taught | DL-014: classification losses |
| Entropy (neural networks) | 189 | taught | ML-091: entropy |
| Kullback-Leibler Divergence | 190 | taught | plan§4 KL divergence: KL divergence (planned MA Note) |
| Binary and Categorical cross-entropy [subsection] | 190 | taught | DL-014: binary and categorical cross-entropy |
| Convolutional Neural Networks [section] | 178 | taught | DL-040: CNNs |
| Kernel (neural networks) | 191 | taught | DL-042: kernel |
| From convolutions to 2D neural networks [subsection] | 193 | taught | DL-042: 2D convolution in networks |
| Feature Map (neural networks) | 193 | taught | DL-042: feature map |
| Convolutional Layer (neural networks) | 193 | taught | DL-042: convolutional layer |
| Padding and striding [subsection] | 193 | taught | DL-043: padding and stride |
| Pooling [subsection] | 194 | taught | DL-044: pooling |
| Pooling (neural networks) | 194 | taught | DL-044: pooling |
| Max Pooling (neural networks) | 194 | taught | DL-044: max pooling |
| Flattening [subsection] | 195 | taught | DL-045: flattening |
| A sample CNN [subsection] | 195 | taught | DL-045: sample CNN (LeNet) |
| Convolutional Networks beyond 2D image data [subsection] | 195 | taught | N162: 1D (temporal) convolution |
| Recurrent Neural Networks [section] | 178 | taught | DL-055: RNNs |
| Recurrent neural network | 197 | taught | DL-055: recurrent neural network |
| RNN | 197 | taught | DL-055: RNN |
| Reactive control [section] | 203 | add | **reactive control and behaviour-based robotics (Braitenberg, subsumption)** (robotics) → RO-07 (extend N126); Correll 11.1: sensor-to-motor rules with no model; the classic first robot controller and the root of behaviour trees |
| Phototaxis | 202 | add | **reactive control and behaviour-based robotics (Braitenberg, subsumption)** (robotics) → RO-07 (extend N126); phototaxis is the standard reactive behaviour (Correll 11.1) |
| Limitations of reactive control [subsection] | 204 | add | **reactive control and behaviour-based robotics (Braitenberg, subsumption)** (robotics) → RO-07 (extend N126); limits of reactive control (Correll 11.1) |
| Finite State Machines [section] | 204 | taught | N130: finite state machines |
| Finite State Machine | 204 | taught | N130: finite state machine |
| FSM | 204 | taught | N130: FSM |
| state transition | 206 | taught | N9: state transition |
| transition (state) | 206 | taught | N9: state transition |
| Implementation [subsection] | 204 | index-noise | generic subsection title 'Implementation' |
| Hierarchical Finite State Machines [section] | 208 | taught | N130: hierarchical state machines |
| Inter-process communication | 209 | taught | N127: inter-process communication (topics, services) |
| IPC | 209 | taught | N127: IPC |
| Robot Operating System | 209 | taught | N127: ROS |
| ROS | 209 | taught | N127: ROS |
| Behavior Trees [section] | 209 | taught | N130: behaviour trees |
| Node Definition and Status [subsection] | 210 | taught | N130: BT node status |
| Node Types [subsection] | 211 | taught | N130: BT node types |
| Behavior Tree Execution [subsection] | 212 | taught | N130: BT execution (tick) |
| Mission Planning [section] | 214 | taught | N115: mission planning |
| The General Problem Solver and STRIPS [subsection] | 214 | add | **symbolic task planning (STRIPS/PDDL)** (robotics) → RB-03 (extend N293); Correll 11.5: STRIPS states, actions with pre/post-conditions; the task layer of task-and-motion planning |
| Map representations [section] | 223 | taught | N71: map representations |
| Topological map | 223, 286 | taught | N188: topological map |
| Graph-based map | 223 | taught | N188: graph-based (topological) map |
| Iterative Closest Point for Sparse Mapping [section] | 224 | taught | N92: ICP |
| Iterative Closest Point | 223 | taught | N92: iterative closest point |
| ICP | 223 | taught | N92: ICP |
| Octomap: dense mapping of voxels [section] | 227 | taught | N97: OctoMap |
| Occupancy grid map | 227 | taught | N96: occupancy grid map |
| k-d tree (data structure) | 227 | taught | N92: k-d tree |
| Octree | 227 | taught | N97: octree |
| RGB-D mapping: dense mapping of surfaces [section] | 228 | taught | N97: dense surface mapping (TSDF/surfels named) |
| Path | 234 | taught | N104: path |
| Trajectory | 242 | taught | N201: trajectory |
| The configuration space [section] | 234 | taught | N72: configuration space |
| Graph-based planning algorithms [section] | 234 | taught | N103: graph-based planning |
| Dijkstra's algorithm [subsection] | 235 | taught | N104: Dijkstra |
| Dijkstra's Shortest Path Algorithm |  | taught | N104: Dijkstra |
| Complete (algorithm) | 236 | taught | N111: complete algorithm |
| A* [subsection] | 234 | taught | N105: A* |
| A* Shortest Path Algorithm |  | taught | N105: A* |
| Heuristic function | 237 | taught | N105: heuristic function |
| Manhattan distance | 237 | taught | ML-085: Manhattan distance |
| D* | 234 | taught | N107: D* |
| Sampling-based path planning [section] | 238 | taught | N110: sampling-based planning |
| Resolution complete | 238 | taught | N111: resolution complete |
| Probabilistic complete | 238 | taught | N111: probabilistically complete |
| Rapidly-exploring Random Tree | 238 | taught | N110: RRT |
| RRT | 238 | taught | N110: RRT |
| Probabilistic Roadmaps | 238 | taught | N111: PRM |
| PRM | 238 | taught | N111: PRM |
| Multi-query (path planning) | 239 | add | **single-query vs multi-query planners** (robotics) → RO-05 (extend N111); Correll 12.3: PRM answers many queries on one map, RRT one query |
| Single-query (path planning) | 239 | add | **single-query vs multi-query planners** (robotics) → RO-05 (extend N111); single-query planning (Correll 12.3) |
| Rapidly Exploring Random Trees [subsection] | 238 | taught | N110: RRT |
| Anytime algorithm | 240 | taught | N105: anytime algorithm (ARA*) |
| RRT* | 241 | taught | N110: RRT* |
| Lazy collision avoidance | 242 | add | **lazy collision checking** (robotics) → RO-05 (extend N111); Correll 12.3: check edges only when a path uses them; why sampling planners are fast |
| Model-predictive control | 243 | taught | N207: model predictive control |
| Planning at different length scales [section] | 243 | taught | N126: planning at different scales (layers) |
| Coverage path planning [section] | 245 | taught | N273: coverage path planning |
| Coverage Path Planning | 245 | taught | N273: coverage path planning |
| Hamiltonian Path | 245 | add | **travelling salesman problem (visiting many goals)** (maths) → RO-23 (extend N274); Hamiltonian path (Correll 12.5): visit every node once; coverage and multi-goal tours |
| Traveling Salesman Problem | 245 | add | **travelling salesman problem (visiting many goals)** (maths) → RO-23 (extend N274); Correll 12.5: best order to visit many goals; inspection and delivery routes |
| Summary and Outlook [section] | 245 | index-noise | section title |
| Non-Prehensile Manipulation [section] | 252 | taught | N328: non-prehensile manipulation |
| Non-prehensile Manipulation | 252 | taught | N328: non-prehensile manipulation |
| In-hand manipulation | 252 | taught | N331: in-hand manipulation |
| Choosing the right grasp [section] | 252 | taught | N291: choosing a grasp |
| Finding good grasps for simple grippers [subsection] | 253 | taught | N291: grasps for simple grippers (antipodal) |
| Finding good grasps for multi-fingered hands [subsection] | 256 | taught | N291: grasps for multi-fingered hands |
| Pick and place [section] | 257 | taught | N292: pick and place (transit and transfer) |
| Task and motion planning | 258 | taught | N293: task and motion planning |
| TAMP | 258 | taught | N293: TAMP |
| Peg-in-hole problems [section] | 258 | taught | N327: peg-in-hole |
| Peg-in-hole | 258 | taught | N327: peg-in-hole |
| Uncertainty in Robotics as Random Variable [section] | 270 | taught | N63: uncertainty as random variables |
| Random Variable | 270 | taught | MA-020: random variable |
| Error Propagation [section] | 270 | taught | plan§4 Linear transforms of a Gaussian: error propagation (A Σ Aᵀ; N81 for the Jacobian form) |
| Error Propagation Law | 271 | taught | plan§4 Linear transforms of a Gaussian: error propagation law |
| Covariance Matrix | 273, 335 | taught | MA-009: covariance matrix (also MA-073) |
| Example: Line Fitting [subsection] | 273 | index-noise | worked example name |
| Example: Odometry [subsection] | 274 | index-noise | worked example name |
| Optimal Sensor Fusion [section] | 276 | taught | N80: optimal sensor fusion |
| The Kalman Filter [subsection] | 277, 295 | taught | N80: Kalman filter |
| Innovation | 277 | taught | N80: innovation (measurement residual) |
| Kalman filter | 277 | taught | N80: Kalman filter |
| Perception step (Kalman filter) | 277 | taught | N80: update step |
| Kalman gain | 277 | taught | N80: Kalman gain |
| Prediction step (Kalman filter) | 277 | taught | N80: prediction step |
| Motivating Example [section] | 282 | index-noise | section title (example) |
| Markov Localization [section] | 283 | taught | N94: Markov localization |
| Bayes' rule | 283, 335 | taught | MA-018: Bayes' rule |
| Perception Update [subsection] | 283 | taught | N78: perception update |
| Perception Update (Markov Localization) | 283 | taught | N94: perception update |
| Belief Model | 285 | taught | N77: belief model |
| Action Update [subsection] | 285 | taught | N78: action update |
| Action Update (Markov Localization) | 286 | taught | N94: action update |
| Example: Markov Localization on a Topological Map [subsection] | 286 | index-noise | worked example name |
| Markov Localization | 286 | taught | N94: Markov localization |
| The Bayes Filter [section] | 289 | taught | N78: Bayes filter |
| Bayes Filter | 289 | taught | N78: Bayes filter |
| Belief | 289 | taught | N77: belief |
| Example: Bayes filter on a grid [subsection] | 291 | taught | N79: grid Bayes filter |
| Central Limit Theorem |  | taught | MA-033: central limit theorem |
| Particle Filter [section] | 293 | taught | N82: particle filter |
| Extended Kalman Filter [section] | 296 | taught | N81: EKF |
| Odometry using the Kalman Filter [subsection] | 297 | taught | N86: odometry fusion with a Kalman filter |
| Summary: Probabilistic Map based localization [section] | 299 | index-noise | summary section title |
| Take home lessons [section] | 300 | index-noise | chapter pointer (take-home lessons) |
| Introduction [section] | 304 | index-noise | generic section title |
| Landmarks [subsection] | 304 | taught | N71: landmarks |
| Landmark | 304 | taught | N71: landmark |
| Special Case I: one landmark [subsection] | 304 | index-noise | worked example name (one landmark) |
| Special Case II: two landmarks [subsection] | 305 | index-noise | worked example name (two landmarks) |
| The Covariance Matrix [section] | 306 | taught | N261: SLAM covariance matrix |
| EKF SLAM [section] | 307 | taught | N261: EKF SLAM |
| Algorithm [subsection] | 304 | taught | N261: EKF SLAM algorithm |
| Initialization [subsubsection] | 307 | taught | N261: landmark initialization |
| Update [subsubsection] | 307 | taught | N261: EKF SLAM update |
| data association | 309 | taught | N259: data association |
| Multiple Sensors [subsection] | 309 | taught | N86: multiple sensors in one filter |
| Graph-based SLAM [section] | 310 | taught | N101: graph-based SLAM |
| Graph-based SLAM | 310 | taught | N101: graph-based SLAM |
| SLAM as a Maximum-Likelihood Estimation Problem [subsection] | 311 | taught | N101: SLAM as maximum likelihood |
| Maximum Likelihood Estimation | 311 | taught | MA-070: maximum likelihood estimation |
| Numerical Techniques for Graph-based SLAM [subsection] | 314 | taught | plan§4 Nonlinear least squares (Gauss-Newton): numerical solution of graph SLAM |
| Further reading [subsection] | 353 | index-noise | further-reading pointer |
| Hypothenuse | 324 | add | **trigonometry basics: right triangles, identities, inverse functions** (maths) → MA 05-linear-algebra (new rigid-body Note); Correll App. A: kinematics, odometry and IK all use sin, cos, tan and their inverses; no MA Note teaches trigonometry |
| Law of Cosines | 324 | add | **law of cosines for analytic IK** (maths) → RB-01 (extend N279); Correll App. A law of cosines |
| Inverse trigonometry [section] | 10 | add | **trigonometry basics: right triangles, identities, inverse functions** (maths) → MA 05-linear-algebra (new rigid-body Note); inverse trigonometry (Correll App. A) |
| Trigonometric identities [section] | 324 | add | **trigonometry basics: right triangles, identities, inverse functions** (maths) → MA 05-linear-algebra (new rigid-body Note); trigonometric identities (Correll App. A) |
| Dot product [section] | 11 | taught | MA-050: dot product |
| Dot product | 11 | taught | MA-050: dot product |
| Scalar product | 328 | taught | MA-050: scalar product |
| Cross product [section] | 11 | taught | plan§4 Cross product and skew-symmetric matrix: cross product |
| Matrix product [section] | 328 | taught | MA-054: matrix product |
| Matrix inversion [section] | 328 | taught | ML-053: matrix inversion |
| Identify matrix | 328 | taught | MA-053: identity matrix |
| Orthonormal matrix | 328 | taught | N65: orthonormal (rotation) matrix, inverse = transpose |
| Pseudo-inverse | 329 | taught | N279: pseudo-inverse |
| Principal Component Analysis [section] | 329 | taught | ML-046: PCA |
| Principal Component Analysis | 11 | taught | ML-046: PCA |
| PCA | 11 | taught | ML-046: PCA |
| Random Variables and Probability Distributions [section] |  | taught | MA-020: random variables and distributions |
| Variate (Random variable) | 334 | taught | MA-020: random variable |
| Probability Distribution | 334 | taught | MA-020: probability distribution |
| Uniform Distribution |  | taught | MA-029: uniform distribution |
| The Normal Distribution [subsection] | 334 | taught | MA-024: normal distribution |
| Normal Distribution | 334 | taught | MA-024: normal distribution |
| Gaussian Distribution | 334 | taught | MA-024: Gaussian distribution |
| Normal distribution in two dimensions [subsection] | 335 | taught | MA-073: 2D normal distribution |
| Conditional Probabilities and Bayes Rule [section] | 335 | taught | MA-018: conditional probability and Bayes' rule |
| Conditional Probability | 335 | taught | MA-015: conditional probability |
| Sum of two random processes [section] | 334 | taught | plan§4 Linear transforms of a Gaussian: sum of random variables |
| Linear Combinations of Independent Gaussian Random Variables [section] | 336 | taught | plan§4 Linear transforms of a Gaussian: linear combinations of independent Gaussians |
| Testing Statistical Significance [section] | 337 | taught | MA-038: statistical significance testing |
| Null Hypothesis on Distributions [subsection] | 337 | taught | MA-038: null hypothesis |
| Testing whether two distributions are independent [subsection] | 338 | taught | MA-045: chi-square test of independence |
| Statistical Significance of True-False Tests [subsection] | 339 | taught | MA-040: significance of true/false tests (error types) |
| Summary [subsection] | 340 | index-noise | summary section title |
| Backpropagation | 344 | taught | DL-015: backpropagation |
| Backward propagation of error [section] | 345 | taught | DL-016: backward propagation of error |
| Backpropagation algorithm [section] | 347 | taught | DL-016: backpropagation algorithm |
| Original [section] | 350 | out-of-scope | research-paper writing appendix (Correll App. E), a different skill than robotics content |
| Hypothesis: Or, what do we learn from this work? [section] | 351 | out-of-scope | research-paper writing appendix (Correll App. E) |
| Survey and Tutorial [section] | 352 | out-of-scope | research-paper writing appendix (Correll App. E) |
| Writing it up! [section] | 352 | out-of-scope | research-paper writing appendix (Correll App. E) |
| An introduction to autonomous emph{mobile} robots [section] |  | index-noise | sample-curriculum appendix (course outline) |
| Content [subsection] | 356, 359, 361 | index-noise | sample-curriculum appendix |
| Implementation suggestions [subsection] | 357, 359 | index-noise | sample-curriculum appendix |
| An introduction to robotic manipulation [section] | 358 | index-noise | sample-curriculum appendix |
| An introduction to robotic systems [section] | 360 | index-noise | sample-curriculum appendix |
| Class debates [section] | 361 | index-noise | sample-curriculum appendix |

## Adds found in body text (not in any index)

- **Laplace transform and transfer functions** (control) → RO-06 (new Note after N118): MR 11.7 defines impedance as the transfer function Z(s) = Ms^2 + Bs + K via the Laplace transform; the standard language of PID tuning, stability margins and filters, and no Note teaches it. Source: MR §11.7 body text p.441-442 (impedance defined as a transfer function; footnote 4).
- **frequency response and Bode plots** (control) → RO-06 (new Note after the Laplace/transfer-function Note): MR 11.7 describes impedance by its low- and high-frequency response; Correll 8.3 describes filters by which frequencies pass; sensor bandwidth (Correll 7.1) is a frequency-response number. Source: MR §11.7 body text p.442; Correll §8.2-8.3 body text pp.150-155.
