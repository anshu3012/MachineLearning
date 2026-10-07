# Online term-list check of the robotics plan (agent `web`)

Checklists are curated Wikipedia term lists, all accessed 2026-10-07 (revision ids given). Each linked term on the page is one row; outlines include their sub-bullets.
Matched by `robo_match.py` (same matcher as agent robo; term lists, raw wikitext and verdict files in `web_work/`) against `docs/books-scope/robotics.md`, the evidence docs, MA/ML/DL Notes and `glossary.md`; then every row judged by hand.
Verdicts: **taught** (Note that teaches it; `plan§4 X` = new MA Note the plan already lists), **add** (concept in bold → target chapter), **out-of-scope** (checkable reason), **index-noise** (names, companies, fiction, generic words). No `mentioned-only` rows: those were folded into `add`.
The *Pages* column holds the page section the term sits in (web pages have no page numbers).
Totals: taught 198, add 95, out-of-scope 257, index-noise 578 (total 1128).


## Glossary of robotics

Source: https://en.wikipedia.org/wiki/Glossary_of_robotics (revision 1348593072), accessed 2026-10-07. Every linked term and every unlinked headword, from the A-Z body (References, See also and External links left out).

Counts: taught 27, add 19, out-of-scope 37, index-noise 28 (total 111).

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| Robotics | (lead) | index-noise | name of the whole field |
| technology | (lead) | index-noise | generic word |
| robot | (lead) | index-noise | generic word "robot" |
| science | (lead) | index-noise | generic word |
| electronics | (lead) | index-noise | generic field name |
| engineering | (lead) | index-noise | generic field name |
| mechanics | (lead) | taught | plan§4 Newtonian and rigid-body mechanics; N281 Lagrangian mechanics |
| computer software (software) | (lead) | index-noise | generic word |
| U.S. Marine Corps | (lead) | index-noise | organisation in a photo caption |
| improvised explosive device | (lead) | index-noise | photo caption |
| Camp Fallujah | (lead) | index-noise | place in a photo caption |
| Iraq | (lead) | index-noise | place in a photo caption |
| Actuator | A | taught | N283: motors and gearing as actuators; N139 actuator models |
| Engine (motor) | A | taught | N283: Motors, gears and the joint torque loop |
| Aerobot | A | out-of-scope | application category (planetary flying robot); no concept beyond aerial robots (RO-17) |
| Arduino | A | out-of-scope | a specific hardware product |
| physical computing | A | out-of-scope | hobby electronics practice, not a robotics concept |
| Artificial intelligence | A | taught | ML-002 AI vs ML vs DL |
| Aura (satellite) | A | index-noise | a named spacecraft |
| NASA | A | index-noise | organisation |
| Automaton | A | out-of-scope | history (early mechanical automata) |
| Autonomous vehicle | A | taught | N244: Driving automation levels and modular vs end-to-end stacks |
| Biomimetic | B | out-of-scope | design philosophy (copy nature); no teachable method behind the word |
| Bionics | B | out-of-scope | design philosophy; same as biomimetic |
| CAD/CAM (unlinked headword) | C | out-of-scope | different field: manufacturing software |
| computer-aided design | C | out-of-scope | different field: manufacturing software |
| computer-aided manufacturing | C | out-of-scope | different field: manufacturing |
| Karel Čapek (Čapek, Karel) | C | index-noise | person |
| Czechs (Czech) | C | index-noise | nationality |
| R.U.R. (Rossum's Universal Robots) | C | index-noise | a play (history of the word robot) |
| Chandra X-ray Observatory | C | index-noise | a named spacecraft |
| Cloud robotics | C | out-of-scope | deployment architecture (offloading compute to the cloud); research topic, no course concept |
| Robot combat (Combat, robot) | C | out-of-scope | hobby/sport event |
| Cruise missile | C | out-of-scope | weapon category |
| Cyborg | C | out-of-scope | fiction / biomedical concept |
| Degrees of freedom (mechanics) (Degrees of freedom) | D | taught | N72: Configuration space and degrees of freedom |
| Cartesian coordinates | D | taught | N65: Coordinate frames and the transform tree |
| Yaw (rotation) (yaw) | D | taught | plan§4 3D rotations: Euler angles and quaternions (yaw, pitch, roll) |
| Delta robot | D | add | **closed chains and parallel robots (delta robot, Stewart platform)** (robotics) → RB-01 (new Note); parallel mechanisms are a standard arm family; every RB Note assumes serial chains |
| Drive Power (unlinked headword) | D | add | **hydraulic and pneumatic actuators** (robotics) → RB-02 (new Note before N283); large legged robots and grippers use fluid power; N283 covers only electric motors [drive power = electric, hydraulic or pneumatic energy source; electric motors are in N283] |
| Emergent behaviour | E | add | **reactive control and behaviour-based robotics (Braitenberg, subsumption)** (robotics) → RO-07 (extend N126); classic architecture alternative to sense-plan-act; N126 lists only the layered stack [emergent behaviour from simple behaviours] |
| Envelope (unlinked headword) | E | taught | N276: Task space and workspace |
| Explosive ordnance disposal robot | E | out-of-scope | application category (bomb-disposal robots) |
| For Inspiration and Recognition of Science and Technology (FIRST) | F | out-of-scope | competition organisation |
| Forward chaining | F | out-of-scope | rule-based AI inference (expert systems); different field |
| Gynoid | G | out-of-scope | robot appearance category |
| Haptic technology (Haptic) | H | add | **haptic (force-feedback) teleoperation** (robotics) → RB-08 (extend N335); N335 teaches teleoperation devices but not feeding contact force back to the operator |
| Stewart platform (Hexapod) | H | add | **closed chains and parallel robots (delta robot, Stewart platform)** (robotics) → RB-01 (new Note); parallel mechanisms are a standard arm family; every RB Note assumes serial chains [Stewart platform] |
| flight simulator | H | index-noise | application example |
| fairground ride | H | index-noise | application example |
| Hexapod (robotics) (Hexapod) | H | out-of-scope | specific body plan (six legs); legged concepts are taught for quadrupeds and bipeds in RB-04/RB-05 |
| Hexapoda (insect-like) | H | index-noise | biology word (insects) |
| Human–computer interaction | H | taught | N341: Human-robot interaction: shared autonomy and physical HRI |
| Humanoid | H | taught | N321/N322: humanoid teleoperation and multi-skill humanoid controllers (RB-06 Humanoids) |
| Hydraulics | H | add | **hydraulic and pneumatic actuators** (robotics) → RB-02 (new Note before N283); large legged robots and grippers use fluid power; N283 covers only electric motors |
| Industrial robot | I | add | **robot arm types: Cartesian, SCARA, articulated, parallel** (robotics) → RB-01 (extend N276); the plan never names the standard arm geometries a course opens with [industrial robot as the standard arm category] |
| Insectoid robot (Insect robot) | I | out-of-scope | robot appearance category |
| Kalman filter | K | taught | N80: Kalman filter |
| Robot kinematics (Kinematics) | K | taught | N69: Kinematic chains and forward kinematics |
| Robot inversekinematics (Inverse Kinematics) | K | taught | N279: Inverse kinematics: analytic and numerical |
| Linear actuator | L | add | **electric motor types: DC, brushless, stepper, servo, AC** (robotics) → RB-02 (new Note before N283); actuators beyond the motor model in N283 are not covered [linear actuator] |
| linear | L | index-noise | generic maths word |
| Manipulator (device) | M | add | **gripper mechanisms: parallel jaw, linkages, suction, multi-finger** (robotics) → RB-03 (new Note before N290); grasping Notes assume a gripper the plan never describes [glossary defines manipulator as gripper; the arm itself is taught in N276-N280] |
| Mobile robot | M | taught | N64: Pose and wheeled-robot motion; N66 wheel types |
| Muting (unlinked headword) | M | out-of-scope | workplace-safety regulation vocabulary (OSHA technical manual, the glossary's source), not an engineering concept |
| Mecanum wheel | M | taught | N66: Omnidirectional (mecanum) base model and control |
| Ornithopter | O | out-of-scope | research body type (flapping-wing flight) |
| Parallel manipulator | P | add | **closed chains and parallel robots (delta robot, Stewart platform)** (robotics) → RB-01 (new Note); parallel mechanisms are a standard arm family; every RB Note assumes serial chains |
| Pendant (unlinked headword) | P | out-of-scope | operator hardware (teach pendant) from OSHA safety vocabulary; not a concept |
| Pneumatics | P | add | **hydraulic and pneumatic actuators** (robotics) → RB-02 (new Note before N283); large legged robots and grippers use fluid power; N283 covers only electric motors |
| Powered exoskeleton | P | out-of-scope | different field: wearable/rehabilitation robotics, outside the plan's navigation and bodies scope |
| Prosthetic | P | out-of-scope | different field: medical prosthetics |
| Remote manipulator | R | taught | N335: teleoperation (leader-follower arms) |
| Robonaut | R | index-noise | a named robot |
| Sensor fusion | S | taught | N86: Fusing IMU, wheels and GNSS |
| Serial manipulator | S | taught | N69: kinematic chains (serial chains) |
| Service robot | S | out-of-scope | application category |
| Servo motor (Servo) | S | add | **electric motor types: DC, brushless, stepper, servo, AC** (robotics) → RB-02 (new Note before N283); actuators beyond the motor model in N283 are not covered |
| Servomechanism | S | add | **electric motor types: DC, brushless, stepper, servo, AC** (robotics) → RB-02 (new Note before N283); actuators beyond the motor model in N283 are not covered [servomechanism] |
| Single Point of Control (unlinked headword) | S | out-of-scope | workplace-safety regulation vocabulary (OSHA) |
| Slow Speed Control (unlinked headword) | S | out-of-scope | workplace-safety regulation vocabulary (OSHA) |
| Snake robot (unlinked headword) | S | out-of-scope | specialised hyper-redundant body type; not in the surveys or curricula the plan was built from |
| tentacle | S | index-noise | biology analogy word |
| Elephant (elephant's trunk) | S | index-noise | biology analogy word |
| snake-arm robot | S | out-of-scope | specialised hyper-redundant body type (same as snake robot) |
| snakebot | S | out-of-scope | specialised hyper-redundant body type (same as snake robot) |
| Stepper motor | S | add | **electric motor types: DC, brushless, stepper, servo, AC** (robotics) → RB-02 (new Note before N283); actuators beyond the motor model in N283 are not covered |
| Subsumption architecture | S | add | **reactive control and behaviour-based robotics (Braitenberg, subsumption)** (robotics) → RO-07 (extend N126); classic architecture alternative to sense-plan-act; N126 lists only the layered stack |
| bottom-up design | S | add | **reactive control and behaviour-based robotics (Braitenberg, subsumption)** (robotics) → RO-07 (extend N126); classic architecture alternative to sense-plan-act; N126 lists only the layered stack [bottom-up behaviour design] |
| Robotic surgery (Surgical robot) | S | out-of-scope | different field: medical robotics |
| minimally invasive surgery (keyhole surgery) | S | out-of-scope | different field: medicine |
| Swarm robotics | S | add | **Consensus-based multi-robot coordination: rendezvous, formation control, swarms** (robotics) → RO-23, new Note after the consensus Note, before Note 271; many simple robots with local rules; plan has team RL (N213-214) but no swarm or consensus control |
| emergent behavior | S | add | **reactive control and behaviour-based robotics (Braitenberg, subsumption)** (robotics) → RO-07 (extend N126); classic architecture alternative to sense-plan-act; N126 lists only the layered stack |
| swarm intelligence | S | add | **Consensus-based multi-robot coordination: rendezvous, formation control, swarms** (robotics) → RO-23, new Note after the consensus Note, before Note 271; many simple robots with local rules; plan has team RL (N213-214) but no swarm or consensus control |
| Synchro | S | out-of-scope | obsolete angle transducer (rotary transformer); robots use encoders (encoder add from robo agent) |
| Teach Mode (unlinked headword) | T | taught | N335: kinesthetic teaching (moving the arm through the path to record it) |
| Three Laws of Robotics | T | out-of-scope | science fiction |
| Isaac Asimov | T | index-noise | person |
| ethics | T | out-of-scope | different field: ethics |
| psychology (robopsychological) | T | out-of-scope | different field: psychology |
| Tool Center Point (unlinked headword) | T | taught | N276: hand (tool) frame in forward kinematics |
| Uncanny valley | U | out-of-scope | HRI psychology hypothesis |
| Unimate | U | index-noise | a named robot (history) |
| Waldo (short story) (Waldo) | W | index-noise | a short story |
| Robert Heinlein | W | index-noise | person |
| Walking robot | W | taught | N295: Gaits, support polygons and the floating base; N312 biped walking |
| Motion (physics) (locomotion) | W | taught | N307: The PPO locomotion recipe (RB-05 Learned locomotion) |
| walking | W | taught | N295: gait vocabulary (walk, trot...); N312 biped walking |
| biped (two-legged walking) | W | taught | N312: Biped walking with RL |
| Zero Moment Point | Z | taught | N296: Zero-moment point and the linear inverted pendulum |
| ZMP (unlinked headword) | Z | taught | N296: zero-moment point (ZMP) |

## Outline of robotics

Source: https://en.wikipedia.org/wiki/Outline_of_robotics (revision 1379001530), accessed 2026-10-07. Every linked term in the whole outline, sub-bullets included, plus See also (References and External links left out).

Counts: taught 58, add 24, out-of-scope 94, index-noise 475 (total 651).

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| Outline (list) (outline) | (lead) | index-noise | page-type word |
| Robotics | (lead) | index-noise | name of the whole field |
| Karel Čapek | (lead) | index-noise | person |
| R.U.R. (Rossum's Universal Robots) | (lead) | index-noise | a play (history of the word robot) |
| Isaac Asimov | (lead) | index-noise | person |
| Liar! (short story) (Liar!) | (lead) | index-noise | fiction (short story) |
| applied science | Nature of robotics | index-noise | generic field name |
| computer science | Nature of robotics | index-noise | generic field name |
| electrical engineering | Nature of robotics | index-noise | generic field name |
| mechanical engineering | Nature of robotics | index-noise | generic field name |
| Research and development | Nature of robotics | index-noise | generic word |
| technology | Nature of robotics | index-noise | generic word |
| Adaptive control | Branches of robotics | out-of-scope | plan §7 dropped ME-069: adaptive control beyond beginner depth; learned adaptation is N167 |
| Unmanned aerial vehicle (Aerial robotics) | Branches of robotics | taught | N221: The quadrotor model (RO-17 Aerial robots) |
| Android science | Branches of robotics | out-of-scope | research field (androids for studying human cognition) |
| Anthrobotics | Branches of robotics | out-of-scope | research/philosophy field |
| Artificial intelligence | Branches of robotics | taught | ML-002 AI vs ML vs DL |
| intelligence | Branches of robotics | index-noise | generic word |
| Artificial neural network | Branches of robotics | taught | DL-009 MLP intuition (DL-008..DL-010) |
| Autonomous car | Branches of robotics | taught | N244: Driving automation levels (RO-20 Autonomous driving) |
| Autonomous research robot | Branches of robotics | out-of-scope | application (lab automation robots) |
| Bayesian network | Branches of robotics | taught | N77: hidden Markov model / dynamic Bayes network |
| BEAM robotics | Branches of robotics | out-of-scope | hobby analog-circuit robots |
| Behavior-based robotics | Branches of robotics | add | **reactive control and behaviour-based robotics (Braitenberg, subsumption)** (robotics) → RO-07 (extend N126); classic architecture alternative to sense-plan-act; N126 lists only the layered stack |
| behavior based AI | Branches of robotics | add | **reactive control and behaviour-based robotics (Braitenberg, subsumption)** (robotics) → RO-07 (extend N126); classic architecture alternative to sense-plan-act; N126 lists only the layered stack |
| Bio-inspired robotics | Branches of robotics | out-of-scope | design philosophy (copy nature); no teachable method behind the word |
| Biomimetic | Branches of robotics | out-of-scope | design philosophy |
| Bionics | Branches of robotics | out-of-scope | design philosophy |
| Biorobotics | Branches of robotics | out-of-scope | design philosophy / biology field |
| Cloud robotics | Branches of robotics | out-of-scope | deployment architecture (cloud offloading); research topic |
| Cognitive robotics | Branches of robotics | out-of-scope | research umbrella field |
| cognition | Branches of robotics | index-noise | generic word |
| Computer cluster (Clustering) | Branches of robotics | out-of-scope | computing hardware (link target is computer cluster, not ML clustering) |
| Computational neuroscience | Branches of robotics | out-of-scope | different field: neuroscience |
| Robot control | Branches of robotics | taught | N117: PD and PID control (RO-06 Feedback control) |
| Robotics conventions | Branches of robotics | out-of-scope | redirects to "Line representations in robotics" (Plücker coordinates), graduate screw-theory notation; the screw axis itself is N275 |
| Data mining | Branches of robotics | taught | ML-001 (glossary G-537 Data mining) |
| Degrees of freedom (mechanics) (Degrees of freedom) | Branches of robotics | taught | N72: Configuration space and degrees of freedom |
| Developmental robotics | Branches of robotics | out-of-scope | research field |
| Digital control | Branches of robotics | add | **Sampled-data control: A/D and D/A conversion, zero-order hold, aliasing** (control) → RO-08, extend Note 136 (Delays and control rate); every robot controller runs on a computer at a fixed rate; N136 covers delay but not sampling itself |
| Digital image processing | Branches of robotics | index-noise | umbrella field name; its methods are judged in the computer-vision table |
| Dimensionality reduction | Branches of robotics | taught | ML-046 PCA (ML-045..ML-048) |
| Distributed robotics | Branches of robotics | taught | N214: Multi-robot RL: decentralised agents |
| Electronic stability control | Branches of robotics | out-of-scope | vehicle safety product; car dynamics and slip are N250-N254 |
| Evolutionary computation | Branches of robotics | taught | N43: evolution strategies and CMA-ES |
| Evolutionary robotics | Branches of robotics | out-of-scope | research field (evolving robot bodies and controllers) |
| Extended Kalman filter | Branches of robotics | taught | N81: Extended Kalman filter |
| Cumulative distribution function (Distribution functions) | Branches of robotics | taught | MA-022 PDF and continuous CDF |
| Feedback control | Branches of robotics | taught | N117: PD / PID feedback control |
| Human–computer interaction | Branches of robotics | taught | N341: Human-robot interaction |
| Human robot interaction | Branches of robotics | taught | N341: Human-robot interaction: shared autonomy and physical HRI |
| Intelligent vehicle technologies | Branches of robotics | index-noise | umbrella term; driving is RO-20 |
| Computer vision | Branches of robotics | index-noise | name of a field |
| Machine vision | Branches of robotics | out-of-scope | industrial inspection field |
| Robot kinematics (Kinematics) | Branches of robotics | taught | N69: Kinematic chains and forward kinematics |
| Motion (physics) (motion) | Branches of robotics | index-noise | generic physics word |
| Laboratory robotics | Branches of robotics | out-of-scope | application (lab automation) |
| Robot learning | Branches of robotics | taught | N132: Why robot RL is hard (RO-08 Robot RL foundations) |
| Direct manipulation interface | Branches of robotics | out-of-scope | different field: HCI (GUI design) |
| Manifold learning | Branches of robotics | out-of-scope | ML family beyond PCA (Isomap, t-SNE); no robotics Note uses it |
| Microrobotics | Branches of robotics | out-of-scope | research field (micro-scale robots) |
| Motion planning | Branches of robotics | taught | N72: basic motion planning problem; RO-05 path planning |
| Motor control | Branches of robotics | out-of-scope | different field: neuroscience of movement |
| Nanorobotics | Branches of robotics | out-of-scope | research field (nano-scale robots) |
| Passive dynamics | Branches of robotics | taught | N299: Passive walkers, limit cycles and Poincaré maps |
| Programming by Demonstration | Branches of robotics | taught | N165: Behaviour cloning; N335 collecting demonstrations |
| Quantum robotics | Branches of robotics | out-of-scope | speculative research field |
| quantum computers | Branches of robotics | out-of-scope | different field: quantum computing |
| digital computers | Branches of robotics | index-noise | generic word |
| Rapid prototyping | Branches of robotics | out-of-scope | different field: manufacturing |
| Reinforcement learning | Branches of robotics | taught | N1: The reinforcement learning problem |
| Robot locomotion | Branches of robotics | taught | N295: gaits; N307 PPO locomotion recipe (RB-05 Learned locomotion) |
| Robot programming | Branches of robotics | out-of-scope | industrial arm programming (vendor languages, teach pendants); ROS programming is N127 |
| Robotic mapping | Branches of robotics | taught | N96: Occupancy grid mapping (RO-04 maps) |
| Robotic surgery | Branches of robotics | out-of-scope | different field: medical robotics |
| Robot-assisted heart surgery | Branches of robotics | out-of-scope | different field: medical robotics |
| Sensor | Branches of robotics | taught | RO-03 Robot sensors chapter (N83-N93) |
| Simultaneous localization and mapping | Branches of robotics | taught | N100: The SLAM problem |
| Software engineering | Branches of robotics | out-of-scope | different field: software engineering |
| Space robotics | Branches of robotics | out-of-scope | application domain (planetary rovers, orbital arms) |
| Speech processing | Branches of robotics | out-of-scope | different field: speech processing |
| Support vector machine | Branches of robotics | taught | ML-086 SVM intuition |
| Swarm robotics | Branches of robotics | add | **Consensus-based multi-robot coordination: rendezvous, formation control, swarms** (robotics) → RO-23, new Note after the consensus Note, before Note 271; many simple robots with local rules; plan has team RL (N213-214) but no swarm or consensus control |
| emergent behavior | Branches of robotics | add | **reactive control and behaviour-based robotics (Braitenberg, subsumption)** (robotics) → RO-07 (extend N126); classic architecture alternative to sense-plan-act; N126 lists only the layered stack |
| swarm intelligence | Branches of robotics | add | **Consensus-based multi-robot coordination: rendezvous, formation control, swarms** (robotics) → RO-23, new Note after the consensus Note, before Note 271; many simple robots with local rules; plan has team RL (N213-214) but no swarm or consensus control |
| Ant robotics | Branches of robotics | add | **Consensus-based multi-robot coordination: rendezvous, formation control, swarms** (robotics) → RO-23, new Note after the consensus Note, before Note 271; many simple robots with local rules; plan has team RL (N213-214) but no swarm or consensus control [ant robotics = swarm of simple robots] |
| Telepresence | Branches of robotics | out-of-scope | application (remote-presence robots for people); the teleoperation concept itself is N335 |
| Ubiquitous robotics | Branches of robotics | out-of-scope | research field |
| ubiquitous computing (ubiquitous and pervasive computing) | Branches of robotics | out-of-scope | different field: computing |
| sensor network | Branches of robotics | out-of-scope | different field: networking |
| ambient intelligence | Branches of robotics | out-of-scope | different field: computing |
| electronics | Contributing fields | index-noise | generic field name |
| engineering | Contributing fields | index-noise | generic field name |
| mechanics | Contributing fields | taught | plan§4 Newtonian and rigid-body mechanics; N281 Lagrangian mechanics |
| computer software (software) | Contributing fields | index-noise | generic word |
| arts | Contributing fields | index-noise | generic field name |
| Biology | Contributing fields | index-noise | generic field name |
| Biomechanics | Contributing fields | out-of-scope | different field: biomechanics |
| Bioinformatics | Contributing fields | out-of-scope | different field: bioinformatics |
| Machine learning | Contributing fields | taught | ML-001 what is ML |
| Deep learning | Contributing fields | taught | DL-002 what is deep learning |
| Computational linguistics | Contributing fields | out-of-scope | different field: linguistics |
| Cloud computing | Contributing fields | out-of-scope | different field: cloud computing |
| Cybernetics | Contributing fields | out-of-scope | history / umbrella field |
| Modal logic | Contributing fields | out-of-scope | different field: formal logic |
| Chemical engineering | Contributing fields | index-noise | engineering field name |
| Electronic engineering | Contributing fields | index-noise | engineering field name |
| Control engineering | Contributing fields | index-noise | engineering field name |
| Telecommunications engineering | Contributing fields | index-noise | engineering field name |
| Computer engineering | Contributing fields | index-noise | engineering field name |
| Internet of things | Contributing fields | index-noise | engineering field name |
| Aerospace engineering | Contributing fields | index-noise | engineering field name |
| Automotive engineering | Contributing fields | index-noise | engineering field name |
| Mechatronics engineering | Contributing fields | index-noise | engineering field name |
| Microelectromechanical systems (Microelectromechanical engineering) | Contributing fields | index-noise | engineering field name |
| Acoustical engineering | Contributing fields | index-noise | engineering field name |
| Nanoengineering | Contributing fields | index-noise | engineering field name |
| Optical engineering | Contributing fields | index-noise | engineering field name |
| Safety engineering | Contributing fields | taught | N248: System safety: monitoring, fail-safe stops and safety cases |
| Fiction | Contributing fields | index-noise | fiction, arts or humanities field |
| List of fictional robots and androids | Contributing fields | index-noise | fiction, arts or humanities field |
| Film | Contributing fields | index-noise | fiction, arts or humanities field |
| Robots in film | Contributing fields | index-noise | fiction, arts or humanities field |
| Literature | Contributing fields | index-noise | fiction, arts or humanities field |
| Robots in literature | Contributing fields | index-noise | fiction, arts or humanities field |
| The Three Laws of Robotics in popular culture | Contributing fields | index-noise | fiction, arts or humanities field |
| Military science | Contributing fields | index-noise | fiction, arts or humanities field |
| Psychology | Contributing fields | index-noise | fiction, arts or humanities field |
| Cognitive science | Contributing fields | index-noise | fiction, arts or humanities field |
| Behavioral science | Contributing fields | index-noise | fiction, arts or humanities field |
| Philosophy | Contributing fields | index-noise | fiction, arts or humanities field |
| Humanoid robot (Ethics) | Contributing fields | taught | N321/N322 (RB-06 Humanoids); link label reads "Ethics" but the target is Humanoid robot |
| Physics | Contributing fields | index-noise | generic field name |
| Dynamics (physics) (Dynamics) | Contributing fields | taught | N281: Lagrangian mechanics and the manipulator equation (RB-02 Dynamics) |
| Kinematics | Contributing fields | taught | N69: kinematic chains and forward kinematics |
| Building automation | Related fields | out-of-scope | different field: building automation |
| Home automation | Related fields | out-of-scope | different field: home automation |
| Assistive technology | Related fields | out-of-scope | different field: assistive technology |
| robot | Robots | index-noise | generic word "robot" |
| Autonomous robot | Types of robots | taught | N126: The autonomy stack |
| Aerobot | Types of robots | out-of-scope | application category (planetary flying robot) |
| Android (robot) (Android) | Types of robots | out-of-scope | robot appearance category |
| Automaton | Types of robots | out-of-scope | history (mechanical automata) |
| Animatronic | Types of robots | out-of-scope | entertainment application |
| Autonomous vehicle | Types of robots | taught | N244: Driving automation levels |
| Ballbot | Types of robots | out-of-scope | specific body type (ball-balancing); balance concepts are N296 |
| Cyborg | Types of robots | out-of-scope | fiction / biomedical concept |
| Explosive ordnance disposal robot | Types of robots | out-of-scope | application category |
| Gynoid | Types of robots | out-of-scope | robot appearance category |
| Hexapod (robotics) (Hexapod) | Types of robots | out-of-scope | specific body plan (six legs); legged concepts taught for quadrupeds and bipeds in RB-04/RB-05 |
| Hexapoda (insect-like) | Types of robots | index-noise | biology word (insects) |
| Industrial robot | Types of robots | add | **robot arm types: Cartesian, SCARA, articulated, parallel** (robotics) → RB-01 (extend N276); the plan never names the standard arm geometries a course opens with [industrial robot as the standard arm category] |
| 3D printer | Types of robots | out-of-scope | different field: manufacturing machine |
| Insect robot | Types of robots | out-of-scope | application category |
| Microbot | Types of robots | out-of-scope | research field (micro-scale robots) |
| Military robot | Types of robots | out-of-scope | application category |
| Mobile robot | Types of robots | taught | N64: Pose and wheeled-robot motion |
| Cruise missile | Types of robots | out-of-scope | weapon category |
| Nanobot | Types of robots | out-of-scope | speculative research field |
| nanometer | Types of robots | index-noise | unit of length |
| Prosthetic | Types of robots | out-of-scope | different field: medical prosthetics |
| Rover (space exploration) (Rover) | Types of robots | out-of-scope | application domain (planetary rovers); wheeled-robot models are N64-N66 |
| Service robot | Types of robots | out-of-scope | application category |
| Snakebot | Types of robots | out-of-scope | specialised hyper-redundant body type; not in the surveys or curricula the plan was built from |
| tentacle | Types of robots | index-noise | biology analogy word |
| Elephant (elephant's trunk) | Types of robots | index-noise | biology analogy word |
| snake-arm robot | Types of robots | out-of-scope | specialised hyper-redundant body type |
| Telerobotics (Teleoperated robot) | Types of robots | taught | N335: teleoperation |
| minimally invasive surgery (keyhole surgery) | Types of robots | out-of-scope | different field: medicine |
| Walking robot | Types of robots | taught | N295: Gaits, support polygons; N312 biped walking |
| walking | Types of robots | taught | N295: gait vocabulary |
| biped (two-legged walking) | Types of robots | taught | N312: Biped walking with RL |
| unmanned aerial vehicles | By mode of locomotion | taught | N221: The quadrotor model (RO-17 Aerial robots) |
| Autonomous Underwater Vehicle (autonomous underwater vehicles) | By mode of locomotion | out-of-scope | underwater domain (hydrodynamics, acoustic navigation) outside the plan's ground, aerial and arm robots |
| crevasse | By mode of locomotion | index-noise | terrain example word |
| Legged robot | By mode of locomotion | taught | N295: Gaits, support polygons and the floating base (RB-04 Legged robots) |
| human leg (human-like leg) | By mode of locomotion | index-noise | anatomy word |
| leg | By mode of locomotion | index-noise | anatomy word |
| Caterpillar track (Tracks) | By mode of locomotion | add | **steering mechanisms: turntable, Ackermann, skid steer (tracks)** (robotics) → RO-01 (extend N66); tracked and skid-steer bases are common field robots; N66 lists omni and unicycle bases only |
| Wheel | By mode of locomotion | taught | N66: Wheel types, omnidirectional bases and the unicycle model |
| Actuator | Robot components and design features | taught | N283: motors and gearing; N139 actuator models |
| Engine (motor) | Robot components and design features | taught | N283: Motors, gears and the joint torque loop |
| Linear actuator | Robot components and design features | add | **electric motor types: DC, brushless, stepper, servo, AC** (robotics) → RB-02 (new Note before N283); actuators beyond the motor model in N283 are not covered [linear actuator] |
| linear | Robot components and design features | index-noise | generic maths word |
| Delta robot | Robot components and design features | add | **closed chains and parallel robots (delta robot, Stewart platform)** (robotics) → RB-01 (new Note); parallel mechanisms are a standard arm family; every RB Note assumes serial chains |
| Robot end effector (End-effector) | Robot components and design features | taught | N276: hand (end-effector) pose by forward kinematics; N326 end-effector delta pose |
| Forward chaining | Robot components and design features | out-of-scope | rule-based AI inference (expert systems); different field |
| Haptic technology (Haptic) | Robot components and design features | add | **haptic (force-feedback) teleoperation** (robotics) → RB-08 (extend N335); N335 teaches teleoperation devices but not feeding contact force back to the operator |
| flight simulator | Robot components and design features | index-noise | application example |
| fairground ride | Robot components and design features | index-noise | application example |
| Hydraulics | Robot components and design features | add | **hydraulic and pneumatic actuators** (robotics) → RB-02 (new Note before N283); large legged robots and grippers use fluid power; N283 covers only electric motors |
| Kalman filter | Robot components and design features | taught | N80: Kalman filter |
| Klann linkage | Robot components and design features | out-of-scope | a specific walking linkage (mechanism design), not a general concept |
| Manipulator (device) | Robot components and design features | add | **gripper mechanisms: parallel jaw, linkages, suction, multi-finger** (robotics) → RB-03 (new Note before N290); grasping Notes assume a gripper the plan never describes [outline defines manipulator as gripper; the arm itself is taught in N276-N280] |
| Parallel manipulator | Robot components and design features | add | **closed chains and parallel robots (delta robot, Stewart platform)** (robotics) → RB-01 (new Note); parallel mechanisms are a standard arm family; every RB Note assumes serial chains |
| Remote manipulator | Robot components and design features | taught | N335: teleoperation (leader-follower arms) |
| Serial manipulator | Robot components and design features | taught | N69: kinematic chains (serial chains) |
| Pneumatics | Robot components and design features | add | **hydraulic and pneumatic actuators** (robotics) → RB-02 (new Note before N283); large legged robots and grippers use fluid power; N283 covers only electric motors |
| Servo motor (Servo) | Robot components and design features | add | **electric motor types: DC, brushless, stepper, servo, AC** (robotics) → RB-02 (new Note before N283); actuators beyond the motor model in N283 are not covered |
| Servomechanism | Robot components and design features | add | **electric motor types: DC, brushless, stepper, servo, AC** (robotics) → RB-02 (new Note before N283); actuators beyond the motor model in N283 are not covered [servomechanism] |
| Stepper motor | Robot components and design features | add | **electric motor types: DC, brushless, stepper, servo, AC** (robotics) → RB-02 (new Note before N283); actuators beyond the motor model in N283 are not covered |
| Stewart platform | Robot components and design features | add | **closed chains and parallel robots (delta robot, Stewart platform)** (robotics) → RB-01 (new Note); parallel mechanisms are a standard arm family; every RB Note assumes serial chains |
| Subsumption architecture | Robot components and design features | add | **reactive control and behaviour-based robotics (Braitenberg, subsumption)** (robotics) → RO-07 (extend N126); classic architecture alternative to sense-plan-act; N126 lists only the layered stack |
| bottom-up design | Robot components and design features | add | **reactive control and behaviour-based robotics (Braitenberg, subsumption)** (robotics) → RO-07 (extend N126); classic architecture alternative to sense-plan-act; N126 lists only the layered stack [bottom-up behaviour design] |
| Aura (satellite) | Specific robots | index-noise | a named spacecraft |
| NASA | Specific robots | index-noise | organisation |
| Chandra X-ray Observatory | Specific robots | index-noise | a named spacecraft |
| Justin (robot) (Justin) | Specific robots | index-noise | a named robot |
| Robonaut | Specific robots | index-noise | a named robot |
| Unimate | Specific robots | index-noise | a named robot (history) |
| GuRoo | Robots from Australia | index-noise | a named real robot |
| UWA Telerobot | Robots from Australia | index-noise | a named real robot |
| Boeing MQ-28 Ghost Bat | Robots from Australia | index-noise | a named real robot |
| Black Knight (vehicle) (Black Knight) | Robots from Britain | index-noise | a named real robot |
| eSTAR project (eSTAR) | Robots from Britain | index-noise | a named real robot |
| Freddy II | Robots from Britain | index-noise | a named real robot |
| George (robot) (George) | Robots from Britain | index-noise | a named real robot |
| Robop | Robots from Britain | index-noise | a named real robot |
| Shadow Hand | Robots from Britain | index-noise | a named real robot |
| Silver Swan (automaton) (Silver Swan) | Robots from Britain | index-noise | a named real robot |
| Talisman UUV | Robots from Britain | index-noise | a named real robot |
| Wheelbarrow (EOD) (Wheelbarrow) | Robots from Britain | index-noise | a named real robot |
| Ameca (robot) (Ameca) | Robots from Britain | index-noise | a named real robot |
| ANAT AMI-100 | Robots from Canada | index-noise | a named real robot |
| ANATROLLER ARE-100 | Robots from Canada | index-noise | a named real robot |
| ANATROLLER ARI-100 | Robots from Canada | index-noise | a named real robot |
| ANATROLLER ARI-50 | Robots from Canada | index-noise | a named real robot |
| ANATROLLER Dusty Duct Destroyer | Robots from Canada | index-noise | a named real robot |
| Canadarm2 | Robots from Canada | index-noise | a named real robot |
| Dextre | Robots from Canada | index-noise | a named real robot |
| hitchBOT | Robots from Canada | index-noise | a named real robot |
| FemiSapien | Robots from China | index-noise | a named real robot |
| Meinü robot | Robots from China | index-noise | a named real robot |
| RoboSapien | Robots from China | index-noise | a named real robot |
| Robosapien v2 | Robots from China | index-noise | a named real robot |
| RS Media | Robots from China | index-noise | a named real robot |
| Sanbot (robot) (Sanbot robot) | Robots from China | index-noise | a named real robot |
| Xianxingzhe | Robots from China | index-noise | a named real robot |
| Xiaoyi (Robot) | Robots from China | index-noise | a named real robot |
| DOK-ING | Robots from Croatia | index-noise | a named real robot |
| DOK-ING EOD (EOD) | Robots from Croatia | index-noise | a named real robot |
| Branimir Makanec (TIOSS) | Robots from Croatia | index-noise | person |
| SyRoTek | Robots from Czech Republic | index-noise | a named real robot |
| Air-Cobot | Robots from France | index-noise | a named real robot |
| Digesting Duck | Robots from France | index-noise | a named real robot |
| Jessiko | Robots from France | index-noise | a named real robot |
| Nabaztag | Robots from France | index-noise | a named real robot |
| Nao (robot) (Nao) | Robots from France | index-noise | a named real robot |
| BionicKangaroo | Robots from Germany | index-noise | a named real robot |
| Care-Providing Robot FRIEND | Robots from Germany | index-noise | a named real robot |
| LAURON | Robots from Germany | index-noise | a named real robot |
| Marvin (robot) (Marvin) | Robots from Germany | index-noise | a named real robot |
| iCub | Robots from Italy | index-noise | a named real robot |
| IsaacRobot | Robots from Italy | index-noise | a named real robot |
| WalkMan | Robots from Italy | index-noise | a named real robot |
| Leonardo's robot | Robots from Italy | index-noise | a named real robot |
| AIBO | Robots from Japan | index-noise | a named real robot |
| ASIMO | Robots from Japan | index-noise | a named real robot |
| EMIEW | Robots from Japan | index-noise | a named real robot |
| EMIEW 2 | Robots from Japan | index-noise | a named real robot |
| Enon (robot) (Enon) | Robots from Japan | index-noise | a named real robot |
| Evolta | Robots from Japan | index-noise | a named real robot |
| Gakutensoku | Robots from Japan | index-noise | a named real robot |
| HAL 5 | Robots from Japan | index-noise | a named real robot |
| HOAP | Robots from Japan | index-noise | a named real robot |
| Ibuki (robot) (Ibuki) | Robots from Japan | index-noise | a named real robot |
| KHR-1 | Robots from Japan | index-noise | a named real robot |
| Omnibot | Robots from Japan | index-noise | a named real robot |
| Plen | Robots from Japan | index-noise | a named real robot |
| QRIO | Robots from Japan | index-noise | a named real robot |
| R.O.B. | Robots from Japan | index-noise | a named real robot |
| SCARA | Robots from Japan | add | **robot arm types: Cartesian, SCARA, articulated, parallel** (robotics) → RB-01 (extend N276); the plan never names the standard arm geometries a course opens with [SCARA arm] |
| Toyota Partner Robot | Robots from Japan | index-noise | a named real robot |
| Wakamaru | Robots from Japan | index-noise | a named real robot |
| Don Cuco El Guapo | Robots from Mexico | index-noise | a named real robot |
| Adelbrecht | Robots from the Netherlands | index-noise | a named real robot |
| Flame (robot) (Flame) | Robots from the Netherlands | index-noise | a named real robot |
| Phobot | Robots from the Netherlands | index-noise | a named real robot |
| Senster | Robots from the Netherlands | index-noise | a named real robot |
| The Trons | Robots from New Zealand | index-noise | a named real robot |
| RAPOSA | Robots from Portugal | index-noise | a named real robot |
| Robot jockey | Robots from Qatar | index-noise | a named real robot |
| Lunokhod 1 | Robots from Russia (or former Soviet Union) | index-noise | a named real robot |
| Lunokhod 2 | Robots from Russia (or former Soviet Union) | index-noise | a named real robot |
| Teletank | Robots from Russia (or former Soviet Union) | index-noise | a named real robot |
| Albert Hubo | Robots from South Korea | index-noise | a named real robot |
| EveR-1 | Robots from South Korea | index-noise | a named real robot |
| HUBO | Robots from South Korea | index-noise | a named real robot |
| MAHRU | Robots from South Korea | index-noise | a named real robot |
| Musa (robot) (Musa) | Robots from South Korea | index-noise | a named real robot |
| AISoy1 | Robots from Spain | index-noise | a named real robot |
| Magie robot (Maggie) | Robots from Spain | index-noise | a named real robot |
| REEM | Robots from Spain | index-noise | a named real robot |
| Tico Robot (Tico) | Robots from Spain | index-noise | a named real robot |
| Alice mobile robot | Robots from Switzerland | index-noise | a named real robot |
| E-puck mobile robot | Robots from Switzerland | index-noise | a named real robot |
| Pocketdelta robot | Robots from Switzerland | index-noise | a named real robot |
| Shameer shami robot | Robots from Switzerland | index-noise | a named real robot |
| Albert One | Robots from the United States | index-noise | a named real robot |
| Allen (robot) (Allen) | Robots from the United States | index-noise | a named real robot |
| ATHLETE (robot) (ATHLETE) | Robots from the United States | index-noise | a named real robot |
| Atlas (robot) (Atlas) | Robots from the United States | index-noise | a named real robot |
| Baxter (robot) (Baxter) | Robots from the United States | index-noise | a named real robot |
| avbotz Baracuda XIV | Robots from the United States | index-noise | a named real robot |
| Berkeley Lower Extremity Exoskeleton | Robots from the United States | index-noise | a named real robot |
| BigDog | Robots from the United States | index-noise | a named real robot |
| Boe-Bot | Robots from the United States | index-noise | a named real robot |
| CISBOT | Robots from the United States | index-noise | a named real robot |
| Coco (robot) (Coco) | Robots from the United States | index-noise | a named real robot |
| Cog (project) (Cog) | Robots from the United States | index-noise | a named real robot |
| Crusher (robot) (Crusher) | Robots from the United States | index-noise | a named real robot |
| Dragon Runner | Robots from the United States | index-noise | a named real robot |
| Energetically Autonomous Tactical Robot (EATR) | Robots from the United States | index-noise | a named real robot |
| Elektro | Robots from the United States | index-noise | a named real robot |
| Entomopter | Robots from the United States | index-noise | a named real robot |
| Haile (robot) (Haile) | Robots from the United States | index-noise | a named real robot |
| Hardiman | Robots from the United States | index-noise | a named real robot |
| HERO (robot) (HERO) | Robots from the United States | index-noise | a named real robot |
| Johns Hopkins Beast | Robots from the United States | index-noise | a named real robot |
| Kismet (robot) (Kismet) | Robots from the United States | index-noise | a named real robot |
| Leonardo (robot) (Leonardo) | Robots from the United States | index-noise | a named real robot |
| LOPES (exoskeleton) (LOPES) | Robots from the United States | index-noise | a named real robot |
| LORAX (robot) (LORAX) | Robots from the United States | index-noise | a named real robot |
| Nomad 200 | Robots from the United States | index-noise | a named real robot |
| Nomad rover | Robots from the United States | index-noise | a named real robot |
| Octobot (robot) | Robots from the United States | index-noise | a named real robot |
| Opportunity rover | Robots from the United States | index-noise | a named real robot |
| Programmable Universal Machine for Assembly | Robots from the United States | index-noise | a named real robot |
| Push the Talking Trash Can | Robots from the United States | index-noise | a named real robot |
| RB5X | Robots from the United States | index-noise | a named real robot |
| Shakey the Robot | Robots from the United States | index-noise | a named real robot |
| Mars Pathfinder (Sojourner) | Robots from the United States | index-noise | a named real robot |
| Spirit rover | Robots from the United States | index-noise | a named real robot |
| Turtle (robot) (Turtle) | Robots from the United States | index-noise | a named real robot |
| Zoë (robot) (Zoë) | Robots from the United States | index-noise | a named real robot |
| Pleo | Robots from the United States | index-noise | a named real robot |
| TOPIO | Robots from Vietnam | index-noise | a named real robot |
| European Robotic Arm | International robots | index-noise | a named real robot |
| Curiosity Rover | International robots | index-noise | a named real robot |
| Mars Science Laboratory | International robots | index-noise | a named real robot |
| HAL 9000 | From British literature | index-noise | fiction: character, work or person |
| Arthur C. Clarke | From British literature | index-noise | fiction: character, work or person |
| Marvin the Paranoid Android | From British radio | index-noise | fiction: character, work or person |
| Douglas Adams | From British radio | index-noise | fiction: character, work or person |
| Kryten | From British television | index-noise | fiction: character, work or person |
| Rob Grant | From British television | index-noise | fiction: character, work or person |
| Doug Naylor | From British television | index-noise | fiction: character, work or person |
| David Ross (actor) (David Ross) | From British television | index-noise | fiction: character, work or person |
| Robert Llewellyn | From British television | index-noise | fiction: character, work or person |
| Red Dwarf | From British television | index-noise | fiction: character, work or person |
| Red Dwarf characters (Talkie Toaster) | From British television | index-noise | fiction: character, work or person |
| John Lenahan | From British television | index-noise | fiction: character, work or person |
| K-9 (Doctor Who) | From British television | index-noise | fiction: character, work or person |
| Bob Camp | From British television | index-noise | fiction: character, work or person |
| Robotboy | From British television | index-noise | fiction: character, work or person |
| Robert's Robots | From British television | index-noise | fiction: character, work or person |
| Coppélia | From French ballets | index-noise | fiction: character, work or person |
| Arthur Saint-Leon | From French ballets | index-noise | fiction: character, work or person |
| Léo Delibes | From French ballets | index-noise | fiction: character, work or person |
| The Future Eve (Hadaly) | From French literature | index-noise | fiction: character, work or person |
| Auguste Villiers de l'Isle-Adam | From French literature | index-noise | fiction: character, work or person |
| Maschinenmensch | From German film | index-noise | fiction: character, work or person |
| Fritz Lang | From German film | index-noise | fiction: character, work or person |
| Thea von Harbou | From German film | index-noise | fiction: character, work or person |
| Brigitte Helm | From German film | index-noise | fiction: character, work or person |
| Metropolis (1927 film) (Metropolis) | From German film | index-noise | fiction: character, work or person |
| The Sandman (short story) (Olimpia) | From German literature | index-noise | fiction: character, work or person |
| E. T. A. Hoffmann | From German literature | index-noise | fiction: character, work or person |
| Braiger | From anime | index-noise | fiction: character, work or person |
| Shigeo Tsubota | From anime | index-noise | fiction: character, work or person |
| Tokichi Aoki | From anime | index-noise | fiction: character, work or person |
| Chōdenji Robo Combattler V (Combattler V) | From anime | index-noise | fiction: character, work or person |
| Tadao Nagahama | From anime | index-noise | fiction: character, work or person |
| Saburo Yatsude | From anime | index-noise | fiction: character, work or person |
| Tōshō Daimos (Daimos) | From anime | index-noise | fiction: character, work or person |
| Groizer X | From anime | index-noise | fiction: character, work or person |
| Go Nagai | From anime | index-noise | fiction: character, work or person |
| Mechander Robo | From anime | index-noise | fiction: character, work or person |
| Jaruhiko Kaido | From anime | index-noise | fiction: character, work or person |
| Brave Raideen (Raideen) | From anime | index-noise | fiction: character, work or person |
| Yoshiyuki Tomino | From anime | index-noise | fiction: character, work or person |
| Trider G7 | From anime | index-noise | fiction: character, work or person |
| Hajime Yatate | From anime | index-noise | fiction: character, work or person |
| Chōdenji Machine Voltes V (Voltes V) | From anime | index-noise | fiction: character, work or person |
| Astro Boy (character) (Astro Boy) | From manga | index-noise | fiction: character, work or person |
| Osamu Tezuka | From manga | index-noise | fiction: character, work or person |
| Astro Boy | From manga | index-noise | fiction: character, work or person |
| Doraemon | From manga | index-noise | fiction: character, work or person |
| Fujiko Fujio | From manga | index-noise | fiction: character, work or person |
| Getter Robo | From manga | index-noise | fiction: character, work or person |
| Ken Ishikawa (manga artist) (Ken Ishikawa) | From manga | index-noise | fiction: character, work or person |
| Grendizer (mecha) (Grendizer) | From manga | index-noise | fiction: character, work or person |
| Grendizer (UFO Robo Grendizer) | From manga | index-noise | fiction: character, work or person |
| Mazinger Z (robot) (Mazinger Z) | From manga | index-noise | fiction: character, work or person |
| Mazinger Z | From manga | index-noise | fiction: character, work or person |
| Tetsujin 28-go (Tetsujin 28) | From manga | index-noise | fiction: character, work or person |
| Mitsuteru Yokoyama | From manga | index-noise | fiction: character, work or person |
| Amazo | From American comics | index-noise | fiction: character, work or person |
| Gardner Fox | From American comics | index-noise | fiction: character, work or person |
| DC Comics | From American comics | index-noise | fiction: character, work or person |
| Flash Gordon (Annihilants) | From American comics | index-noise | fiction: character, work or person |
| Alex Raymond | From American comics | index-noise | fiction: character, work or person |
| C-3PO | From American film | index-noise | fiction: character, work or person |
| George Lucas | From American film | index-noise | fiction: character, work or person |
| Anthony Daniels | From American film | index-noise | fiction: character, work or person |
| Star Wars | From American film | index-noise | fiction: character, work or person |
| Paul Verhoeven | From American film | index-noise | fiction: character, work or person |
| Craig Hayes | From American film | index-noise | fiction: character, work or person |
| Phil Tippett | From American film | index-noise | fiction: character, work or person |
| RoboCop | From American film | index-noise | fiction: character, work or person |
| Batteries Not Included (*batteries not included) | From American film | index-noise | fiction: character, work or person |
| Gort (The Day the Earth Stood Still) (Gort) | From American film | index-noise | fiction: character, work or person |
| Robert Wise | From American film | index-noise | fiction: character, work or person |
| Harry Bates (author) (Harry Bates) | From American film | index-noise | fiction: character, work or person |
| Edmund H. North | From American film | index-noise | fiction: character, work or person |
| Lock Martin | From American film | index-noise | fiction: character, work or person |
| The Day the Earth Stood Still (1951 film) (The Day the Earth Stood Still) | From American film | index-noise | fiction: character, work or person |
| Tim Blaney | From American film | index-noise | fiction: character, work or person |
| Syd Mead | From American film | index-noise | fiction: character, work or person |
| Short Circuit (1986 film) (Short Circuit) | From American film | index-noise | fiction: character, work or person |
| R2-D2 | From American film | index-noise | fiction: character, work or person |
| Kenny Baker (English actor) (Kenny Baker) | From American film | index-noise | fiction: character, work or person |
| Ben Burtt | From American film | index-noise | fiction: character, work or person |
| Robby the Robot | From American film | index-noise | fiction: character, work or person |
| Fred M. Wilcox (director) (Fred M. Wilcox) | From American film | index-noise | fiction: character, work or person |
| Robert Kinoshita | From American film | index-noise | fiction: character, work or person |
| Frankie Darro | From American film | index-noise | fiction: character, work or person |
| Marvin Miller (actor) (Marvin Miller) | From American film | index-noise | fiction: character, work or person |
| Forbidden Planet | From American film | index-noise | fiction: character, work or person |
| Terminator (character) (The Terminator) | From American film | index-noise | fiction: character, work or person |
| James Cameron | From American film | index-noise | fiction: character, work or person |
| Gale Anne Hurd | From American film | index-noise | fiction: character, work or person |
| Terminator (franchise) (The Terminator) | From American film | index-noise | fiction: character, work or person |
| Andrew Stanton | From American film | index-noise | fiction: character, work or person |
| Elissa Knight | From American film | index-noise | fiction: character, work or person |
| WALL-E | From American film | index-noise | fiction: character, work or person |
| Adam Link | From American literature | index-noise | fiction: character, work or person |
| Eando Binder | From American literature | index-noise | fiction: character, work or person |
| I, Robot (short story) (I, Robot) | From American literature | index-noise | fiction: character, work or person |
| Farewell to the Master | From American literature | index-noise | fiction: character, work or person |
| Robbie (short story) (Robbie) | From American literature | index-noise | fiction: character, work or person |
| I, Robot | From American literature | index-noise | fiction: character, work or person |
| The Steam Man of the Prairies | From American literature | index-noise | fiction: character, work or person |
| Edward S. Ellis | From American literature | index-noise | fiction: character, work or person |
| Tik-Tok (Oz) (Tik-Tok) | From American literature | index-noise | fiction: character, work or person |
| L. Frank Baum | From American literature | index-noise | fiction: character, work or person |
| Ozma of Oz | From American literature | index-noise | fiction: character, work or person |
| Bender (Futurama) (Bender Bending Rodriguez) | From American television | index-noise | fiction: character, work or person |
| Matt Groening | From American television | index-noise | fiction: character, work or person |
| David X. Cohen | From American television | index-noise | fiction: character, work or person |
| John DiMaggio | From American television | index-noise | fiction: character, work or person |
| Futurama | From American television | index-noise | fiction: character, work or person |
| Ben Bocquelet | From American television | index-noise | fiction: character, work or person |
| The Amazing World of Gumball | From American television | index-noise | fiction: character, work or person |
| Cambot | From American television | index-noise | fiction: character, work or person |
| Gypsy (Mystery Science Theater 3000) (Gypsy) | From American television | index-noise | fiction: character, work or person |
| Crow T. Robot | From American television | index-noise | fiction: character, work or person |
| Tom Servo | From American television | index-noise | fiction: character, work or person |
| Joel Hodgson | From American television | index-noise | fiction: character, work or person |
| Trace Beaulieu | From American television | index-noise | fiction: character, work or person |
| Bill Corbett | From American television | index-noise | fiction: character, work or person |
| Josh Weinstein | From American television | index-noise | fiction: character, work or person |
| Jim Mallon | From American television | index-noise | fiction: character, work or person |
| Patrick Brantseg | From American television | index-noise | fiction: character, work or person |
| Mystery Science Theater 3000 | From American television | index-noise | fiction: character, work or person |
| Data (Star Trek) (Data) | From American television | index-noise | fiction: character, work or person |
| Gene Roddenberry | From American television | index-noise | fiction: character, work or person |
| Brent Spiner | From American television | index-noise | fiction: character, work or person |
| Star Trek: The Next Generation | From American television | index-noise | fiction: character, work or person |
| Grounder | From American television | index-noise | fiction: character, work or person |
| Scratch (robot) (Scratch) | From American television | index-noise | fiction: character, work or person |
| Garry Chalk (actor) (Garry Chalk) | From American television | index-noise | fiction: character, work or person |
| Adventures of Sonic the Hedgehog | From American television | index-noise | fiction: character, work or person |
| Jhonen Vasquez | From American television | index-noise | fiction: character, work or person |
| Rosearik Rikki Simons | From American television | index-noise | fiction: character, work or person |
| Invader Zim | From American television | index-noise | fiction: character, work or person |
| Jenny Wakeman | From American television | index-noise | fiction: character, work or person |
| Rob Renzetti | From American television | index-noise | fiction: character, work or person |
| Janice Kawaye | From American television | index-noise | fiction: character, work or person |
| My Life as a Teenage Robot | From American television | index-noise | fiction: character, work or person |
| Lost in Space (Robot B-9) | From American television | index-noise | fiction: character, work or person |
| Irwin Allen | From American television | index-noise | fiction: character, work or person |
| Bob May (actor) (Bob May) | From American television | index-noise | fiction: character, work or person |
| Dick Tufeld | From American television | index-noise | fiction: character, work or person |
| Larry Miller (comedian) (Larry Miller) | From American television | index-noise | fiction: character, work or person |
| Buzz Lightyear of Star Command | From American television | index-noise | fiction: character, work or person |
| History of robots | History of robotics | out-of-scope | history |
| Artificial general intelligence | Future of robotics | out-of-scope | speculative AI topic |
| Soft robotics | Future of robotics | out-of-scope | research field (continuum mechanics of soft bodies); not in the plan's surveys |
| Arduino | Robotics development and development tools | out-of-scope | a specific hardware product |
| physical computing | Robotics development and development tools | out-of-scope | hobby electronics practice |
| computer-aided design | Robotics development and development tools | out-of-scope | different field: manufacturing software |
| computer-aided manufacturing | Robotics development and development tools | out-of-scope | different field: manufacturing |
| Cleanroom | Robotics development and development tools | out-of-scope | different field: manufacturing facility |
| Microsoft Robotics Developer Studio | Robotics development and development tools | index-noise | discontinued software product |
| Player Project | Robotics development and development tools | out-of-scope | legacy middleware superseded by ROS (N127) |
| Robot Operating System | Robotics development and development tools | taught | N127: ROS 2: nodes, topics, services and actions |
| Gazebo simulator (Gazebo) | Robotics development and development tools | taught | N128: choosing Gazebo vs MuJoCo vs Isaac vs Drake; N131 Gazebo + ROS |
| robotics simulator | Robotics development and development tools | taught | N128: Physics simulators |
| Cartesian coordinates | Robotics principles | taught | N65: Coordinate frames and the transform tree |
| Yaw (rotation) (yaw) | Robotics principles | taught | plan§4 3D rotations: Euler angles and quaternions (yaw, pitch, roll) |
| Emergent behaviour | Robotics principles | add | **reactive control and behaviour-based robotics (Braitenberg, subsumption)** (robotics) → RO-07 (extend N126); classic architecture alternative to sense-plan-act; N126 lists only the layered stack [emergent behaviour from simple behaviours] |
| Humanoid | Robotics principles | taught | N321/N322 (RB-06 Humanoids) |
| Roboethics | Robotics principles | out-of-scope | different field: ethics |
| Three Laws of Robotics | Robotics principles | out-of-scope | science fiction |
| ethics | Robotics principles | out-of-scope | different field: ethics |
| Uncanny valley | Robotics principles | out-of-scope | HRI psychology hypothesis |
| List of robotics companies | Robotics companies | index-noise | list page |
| 3D Robotics | Robotics companies | index-noise | company name |
| ABB Group | Robotics companies | index-noise | company name |
| Aethon Inc. | Robotics companies | index-noise | company name |
| Alphabet Inc. | Robotics companies | index-noise | company name |
| Amazon.com | Robotics companies | index-noise | company name |
| Anki (American company) (Anki Inc.) | Robotics companies | index-noise | company name |
| Autonomous Solutions | Robotics companies | index-noise | company name |
| Boston Dynamics | Robotics companies | index-noise | company name |
| Bot & Dolly | Robotics companies | index-noise | company name |
| CANVAS Technology | Robotics companies | index-noise | company name |
| Carbon Robotics | Robotics companies | index-noise | company name |
| Clearpath Robotics | Robotics companies | index-noise | company name |
| Cyberdyne, Inc. | Robotics companies | index-noise | company name |
| Delphi Automotive | Robotics companies | index-noise | company name |
| DJI (company) | Robotics companies | index-noise | company name |
| Ekso Bionics | Robotics companies | index-noise | company name |
| Energid Technologies | Robotics companies | index-noise | company name |
| Epson Robots | Robotics companies | index-noise | company name |
| FANUC Robotics | Robotics companies | index-noise | company name |
| Fetch Robotics | Robotics companies | index-noise | company name |
| Flexiv Robotics | Robotics companies | index-noise | company name |
| Foxconn | Robotics companies | index-noise | company name |
| Fujitsu | Robotics companies | index-noise | company name |
| Google DeepMind | Robotics companies | index-noise | company name |
| GreyOrange | Robotics companies | index-noise | company name |
| Holomini | Robotics companies | index-noise | company name |
| Honda | Robotics companies | index-noise | company name |
| IAM Robotics | Robotics companies | index-noise | company name |
| Industrial Perception | Robotics companies | index-noise | company name |
| Intuitive Surgical | Robotics companies | index-noise | company name |
| iRobot | Robotics companies | index-noise | company name |
| Jibo | Robotics companies | index-noise | company name |
| Kawasaki Heavy Industries | Robotics companies | index-noise | company name |
| Knightscope | Robotics companies | index-noise | company name |
| KUKA | Robotics companies | index-noise | company name |
| Lockheed Martin | Robotics companies | index-noise | company name |
| Locus Robotics | Robotics companies | index-noise | company name |
| Meka Robotics | Robotics companies | index-noise | company name |
| Omron Adept | Robotics companies | index-noise | company name |
| Open Bionics | Robotics companies | index-noise | company name |
| Rethink Robotics | Robotics companies | index-noise | company name |
| ReWalk Robotics | Robotics companies | index-noise | company name |
| RoboCV | Robotics companies | index-noise | company name |
| Robotiq | Robotics companies | index-noise | company name |
| Robotis | Robotics companies | index-noise | company name |
| Robotis Bioloid | Robotics companies | index-noise | company name |
| Samsung | Robotics companies | index-noise | company name |
| Savioke | Robotics companies | index-noise | company name |
| Schaft Inc | Robotics companies | index-noise | company name |
| Seegrid | Robotics companies | index-noise | company name |
| SIASUN Robot & Automation Co. Ltd. | Robotics companies | index-noise | company name |
| SIASUN UAV | Robotics companies | index-noise | company name |
| SoftBank Robotics | Robotics companies | index-noise | company name |
| Soil Machine Dynamics Ltd | Robotics companies | index-noise | company name |
| Swisslog | Robotics companies | index-noise | company name |
| Titan Medical Inc | Robotics companies | index-noise | company name |
| TOSY | Robotics companies | index-noise | company name |
| Toyota | Robotics companies | index-noise | company name |
| UBTECH | Robotics companies | index-noise | company name |
| ULC Robotics | Robotics companies | index-noise | company name |
| Universal Robotics | Robotics companies | index-noise | company name |
| Vecna Technologies | Robotics companies | index-noise | company name |
| Verb Surgical | Robotics companies | index-noise | company name |
| VEX Robotics | Robotics companies | index-noise | company name |
| Yamaha Corporation (Yamaha) | Robotics companies | index-noise | company name |
| Yaskawa | Robotics companies | index-noise | company name |
| List of robotics laboratories | Robotics organizations | index-noise | list page |
| For Inspiration and Recognition of Science and Technology (FIRST) | Robotics organizations | index-noise | organisation |
| IEEE Robotics and Automation Society | Robotics organizations | index-noise | organisation |
| Robotics Institute | Robotics organizations | index-noise | organisation |
| SRI International | Robotics organizations | index-noise | organisation |
| Robot competition | Robotics competitions | index-noise | competition or organiser name |
| National ElectroniX Olympiad | Robotics competitions | index-noise | competition or organiser name |
| ABU Robocon | Robotics competitions | index-noise | competition or organiser name |
| BEST Robotics | Robotics competitions | index-noise | competition or organiser name |
| Botball | Robotics competitions | index-noise | competition or organiser name |
| DARPA Grand Challenge | Robotics competitions | index-noise | competition or organiser name |
| vehicle automation (autonomous vehicles) | Robotics competitions | index-noise | umbrella term (vehicle automation); driving is RO-20 |
| Defense Advanced Research Projects Agency | Robotics competitions | index-noise | competition or organiser name |
| United States Department of Defense | Robotics competitions | index-noise | competition or organiser name |
| DARPA Grand Challenge (2004) | Robotics competitions | index-noise | competition or organiser name |
| DARPA Grand Challenge (2005) | Robotics competitions | index-noise | competition or organiser name |
| DARPA Grand Challenge (2007) | Robotics competitions | index-noise | competition or organiser name |
| DARPA Robotics Challenge | Robotics competitions | index-noise | competition or organiser name |
| Defcon Robot Contest | Robotics competitions | index-noise | competition or organiser name |
| Duke Annual Robo-Climb Competition | Robotics competitions | index-noise | competition or organiser name |
| Eurobot | Robotics competitions | index-noise | competition or organiser name |
| European Land-Robot Trial | Robotics competitions | index-noise | competition or organiser name |
| Junior FIRST Lego League (FIRST Junior Lego League) | Robotics competitions | index-noise | competition or organiser name |
| FIRST Lego League | Robotics competitions | index-noise | competition or organiser name |
| FIRST Robotics Competition | Robotics competitions | index-noise | competition or organiser name |
| FIRST Tech Challenge | Robotics competitions | index-noise | competition or organiser name |
| International Aerial Robotics Competition | Robotics competitions | index-noise | competition or organiser name |
| Micromouse | Robotics competitions | index-noise | competition or organiser name |
| RoboCup | Robotics competitions | index-noise | competition or organiser name |
| Robofest | Robotics competitions | index-noise | competition or organiser name |
| RoboGames | Robotics competitions | index-noise | competition or organiser name |
| RoboSub | Robotics competitions | index-noise | competition or organiser name |
| Student Robotics | Robotics competitions | index-noise | competition or organiser name |
| UAV Outback Challenge | Robotics competitions | index-noise | competition or organiser name |
| World Robot Olympiad | Robotics competitions | index-noise | competition or organiser name |
| List of roboticists | People influential in the field of robotics | index-noise | person or history pointer |
| Czechs (Czech) | People influential in the field of robotics | index-noise | person or history pointer |
| R.U.R. (Rossum's Universal Robots) | People influential in the field of robotics | index-noise | person or history pointer |
| George Devol (Devol, George) | People influential in the field of robotics | index-noise | person or history pointer |
| Joseph Engelberger (Engelberger, Joseph) | People influential in the field of robotics | index-noise | person or history pointer |
| Unimation | People influential in the field of robotics | index-noise | company name (history) |
| Marc Raibert (Raibert, Marc) | People influential in the field of robotics | index-noise | person or history pointer |
| Droid (Star Wars) (Droid) | Robotics in popular culture | index-noise | popular culture |
| Cyborgs in fiction (List of fictional cyborgs) | Robotics in popular culture | index-noise | popular culture |
| List of fictional gynoids | Robotics in popular culture | index-noise | popular culture |
| Real Robot | Robotics in popular culture | index-noise | popular culture |
| Super Robot | Robotics in popular culture | index-noise | popular culture |
| Robot Hall of Fame | Robotics in popular culture | index-noise | popular culture |
| Waldo (short story) (Waldo) | Robotics in popular culture | index-noise | popular culture |
| Robert Heinlein | Robotics in popular culture | index-noise | popular culture |
| Outline of automation | See also | index-noise | see-also pointer to another list page |
| Outline of machines | See also | index-noise | see-also pointer to another list page |
| Outline of technology | See also | index-noise | see-also pointer to another list page |
| :Category:Robots | See also | index-noise | category pointer |
| Automatic waste container | See also | out-of-scope | consumer product (smart bin) |
| Bina48 | See also | index-noise | a named robot |
| Cyberflora | See also | out-of-scope | art project |
| Educational robotics | See also | out-of-scope | different field: education |
| Electrointerpretation | See also | out-of-scope | art/research project |
| History of technology | See also | out-of-scope | history |
| List of emerging technologies (List of emerging robotic technologies) | See also | index-noise | list page |
| List of robotics journals | See also | index-noise | list page |
| List of robotics occupations | See also | index-noise | list page |
| Microsoft Robotics Studio | See also | index-noise | discontinued software product |
| Mobile manipulator | See also | taught | N334: Mobile manipulation |
| Mobile Robot Programming Toolkit | See also | index-noise | a specific software library |
| NASA robots | See also | index-noise | list page |
| Open-source robotics | See also | out-of-scope | community practice, not a concept |
| Open-source hardware | See also | out-of-scope | community practice, not a concept |
| Robotics suite | See also | out-of-scope | software category name |
| :Category:Robotics suites | See also | index-noise | category pointer |
| Whegs | See also | out-of-scope | a specific locomotion mechanism (wheel-legs), research |
| Vex Robotics Design System (VEX Robotics) | See also | index-noise | product name |
| Artificial Life | See also | out-of-scope | different field: artificial life |
| Control systems | See also | taught | N117: PD / PID feedback control |
| Mechatronics | See also | index-noise | engineering field name |
| :Category:Roboticists (Roboticists) | See also | index-noise | category pointer |

## Control theory (article topic lists)

Source: https://en.wikipedia.org/wiki/Control_theory (revision 1373944568), accessed 2026-10-07. Glossary of control theory and Outline of control theory do not exist on Wikipedia (API: missing). Used the Control theory article's topic sections instead: open/closed loop through Main control strategies, plus See also; History and People sections left out.

Counts: taught 56, add 40, out-of-scope 48, index-noise 24 (total 168).

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| Linear control theory | Linear and nonlinear control theory | index-noise | umbrella field heading; its members (LTI, Laplace, Bode, root locus...) are judged in their own rows |
| superposition principle | Linear and nonlinear control theory | add | **Response of linear time-invariant systems: linearity, superposition, impulse and step response** (control) → MA 06-calculus, new Note after the planned Matrix exponential Note; every transfer-function, Bode and convolution idea rests on linearity and the impulse response; no Note names them [superposition stated as the defining property of linear control] |
| linear differential equation | Linear and nonlinear control theory | add | **linear ODEs: homogeneous and particular solutions** (maths) → MA 06-calculus (planned ODEs Note); the planned ODEs Note lists vector fields only; solving a linear ODE is the base of step response |
| linear time invariant | Linear and nonlinear control theory | add | **Response of linear time-invariant systems: linearity, superposition, impulse and step response** (control) → MA 06-calculus, new Note after the planned Matrix exponential Note; every transfer-function, Bode and convolution idea rests on linearity and the impulse response; no Note names them |
| frequency domain | Linear and nonlinear control theory | add | **frequency response and Bode plots (gain, phase, bandwidth, resonance)** (control) → RO-06 (new Note after the Laplace/transfer-function Note); standard way to read a loop's speed and robustness; plan has none [frequency-domain analysis] |
| Laplace transform | Linear and nonlinear control theory | add | **Laplace transform and transfer functions** (control) → RO-06 (new Note after N118); classical control reads every loop as G(s); the plan has no Laplace or transfer-function Note |
| Fourier transform | Linear and nonlinear control theory | add | **Fourier transform, frequency spectrum and FFT** (maths) → MA 06-calculus; frequency content of signals and images (filtering, aliasing, vibration); absent from MA and the plan |
| Z transform | Linear and nonlinear control theory | add | **Z-transform and discrete-time transfer functions** (control) → RO-06 (section of the Laplace/transfer-function Note); robot controllers run in discrete time (N136); the discrete twin of the Laplace transform is not taught |
| Bode plot | Linear and nonlinear control theory | add | **frequency response and Bode plots (gain, phase, bandwidth, resonance)** (control) → RO-06 (new Note after the Laplace/transfer-function Note); standard way to read a loop's speed and robustness; plan has none |
| root locus | Linear and nonlinear control theory | add | **root locus** (control) → RO-06 (new Note after N118); how closed-loop poles move with one gain; core of an intro control course |
| Nyquist stability criterion | Linear and nonlinear control theory | add | **Loop transfer function and the Nyquist criterion (gain and phase margins)** (control) → RO-06, new Note after the frequency-response Note; stability margins of a feedback loop; plan has none |
| Bandwidth (signal processing) (bandwidth) | Linear and nonlinear control theory | add | **frequency response and Bode plots (gain, phase, bandwidth, resonance)** (control) → RO-06 (new Note after the Laplace/transfer-function Note); standard way to read a loop's speed and robustness; plan has none [bandwidth of a closed loop read from its frequency response] |
| frequency response | Linear and nonlinear control theory | add | **frequency response and Bode plots (gain, phase, bandwidth, resonance)** (control) → RO-06 (new Note after the Laplace/transfer-function Note); standard way to read a loop's speed and robustness; plan has none |
| eigenvalue | Linear and nonlinear control theory | taught | MA-056 eigenvectors and eigenvalues |
| gain (electronics) (gain) | Linear and nonlinear control theory | add | **frequency response and Bode plots (gain, phase, bandwidth, resonance)** (control) → RO-06 (new Note after the Laplace/transfer-function Note); standard way to read a loop's speed and robustness; plan has none [gain = output/input amplitude ratio (electronics sense); controller gains appear in N117 but the gain of a system is not taught] |
| resonant frequency (resonant frequencies) | Linear and nonlinear control theory | add | **frequency response and Bode plots (gain, phase, bandwidth, resonance)** (control) → RO-06 (new Note after the Laplace/transfer-function Note); standard way to read a loop's speed and robustness; plan has none [resonant peak in the frequency response; natural frequency itself is in plan§4 Second-order linear systems] |
| zeros and poles | Linear and nonlinear control theory | add | **poles and zeros of a transfer function; stable, marginally stable and BIBO stable** (control) → RO-06 (section of the Laplace/transfer-function Note); N204 places poles of A-BK but never says what poles and zeros of a system are or where stable ones lie |
| Nonlinear control theory | Linear and nonlinear control theory | index-noise | umbrella field heading; members (Lyapunov, feedback linearization, limit cycles) judged in own rows |
| nonlinear differential equation | Linear and nonlinear control theory | taught | plan§4 State-space models (nonlinear systems) and plan§4 ODEs and vector fields |
| limit cycle | Linear and nonlinear control theory | taught | N299: Passive walkers, limit cycles and Poincaré maps |
| Poincaré map | Linear and nonlinear control theory | taught | N299: Poincaré maps |
| Lyapunov function (Lyapunov stability theorem) | Linear and nonlinear control theory | taught | N199: Stability certificates with Lyapunov functions; plan§4 Lyapunov functions |
| describing function | Linear and nonlinear control theory | out-of-scope | graduate nonlinear-control approximation (harmonic balance for limit cycles); no plan Note or robot controller uses it |
| numerical method | Linear and nonlinear control theory | taught | plan§4 Numerical integration of ODEs (Euler, Runge-Kutta) |
| simulation (simulating) | Linear and nonlinear control theory | taught | N128: Physics simulators: time steps, contact and the main engines |
| simulation language | Linear and nonlinear control theory | out-of-scope | software category (Modelica/Simulink-style languages); tooling, not a concept; simulators taught in N128 |
| linearization (linearized) | Linear and nonlinear control theory | taught | N81: linearisation in the EKF; plan§5 recap Taylor linearisation of a system (MA-064) |
| perturbation theory | Linear and nonlinear control theory | out-of-scope | applied-maths asymptotic method from physics; no robotics or control course in scope uses it |
| state variable | Analysis techniques – frequency domain and time domain | taught | plan§4 State-space models |
| variable (mathematics) (variables) | Analysis techniques – frequency domain and time domain | index-noise | generic maths word "variable" |
| frequency | Analysis techniques – frequency domain and time domain | add | **frequency response and Bode plots (gain, phase, bandwidth, resonance)** (control) → RO-06 (new Note after the Laplace/transfer-function Note); standard way to read a loop's speed and robustness; plan has none [frequency of a sinusoid as used in frequency-domain analysis] |
| transfer function | Analysis techniques – frequency domain and time domain | add | **Laplace transform and transfer functions** (control) → RO-06 (new Note after N118); classical control reads every loop as G(s); the plan has no Laplace or transfer-function Note [glossary G-2004 "Transfer function" is the DL activation-function sense, not this one] |
| transform (mathematics) (transform) | Analysis techniques – frequency domain and time domain | index-noise | generic maths word "transform" |
| differential equation | Analysis techniques – frequency domain and time domain | taught | plan§4 ODEs and vector fields |
| algebraic equation | Analysis techniques – frequency domain and time domain | index-noise | generic maths term (algebraic vs differential equation) |
| Time-domain state space representation | Analysis techniques – frequency domain and time domain | taught | plan§4 State-space models (x_dot = Ax + Bu) |
| linear function (linear) | Analysis techniques – frequency domain and time domain | taught | MA-053 linear transformations and matrices |
| state space (controls) (state space) | Analysis techniques – frequency domain and time domain | taught | plan§4 State-space models |
| Single-input single-output system (Single-input single-output) | System interfacing | add | **SISO vs MIMO systems** (control) → RO-06 (section of the Laplace/transfer-function Note); tells when one transfer function suffices and when state space or LQR is needed |
| audio power amplifier | System interfacing | out-of-scope | different field: audio electronics example in the article |
| audio signal | System interfacing | out-of-scope | different field: audio electronics example |
| loudspeaker | System interfacing | out-of-scope | different field: audio electronics example |
| Multiple-input multiple-output system (Multiple-input multiple-output) | System interfacing | add | **SISO vs MIMO systems** (control) → RO-06 (section of the Laplace/transfer-function Note); tells when one transfer function suffices and when state space or LQR is needed |
| telescope | System interfacing | out-of-scope | different field: astronomy example |
| Keck telescopes (Keck) | System interfacing | out-of-scope | different field: a named observatory (astronomy) |
| MMT Observatory (MMT) | System interfacing | out-of-scope | different field: a named observatory (astronomy) |
| actuator | System interfacing | taught | N139: System identification and actuator models; N283 motors and gearing |
| active optics | System interfacing | out-of-scope | different field: telescope optics |
| wavefront | System interfacing | out-of-scope | optics wavefront (telescope example); not the grid wavefront planner of N106 |
| nuclear reactor | System interfacing | out-of-scope | different field: nuclear engineering example |
| cell (biology) (cells) | System interfacing | out-of-scope | different field: biology example |
| differential equations | Classical SISO system design | taught | plan§4 ODEs and vector fields |
| PID controller | Classical SISO system design | taught | N117: PD and PID control |
| state variables | Modern MIMO system design | taught | plan§4 State-space models |
| Nonlinear control (Nonlinear) | Modern MIMO system design | index-noise | umbrella heading, same as row "Nonlinear control theory" |
| multivariable control (multivariable) | Modern MIMO system design | add | **SISO vs MIMO systems** (control) → RO-06 (section of the Laplace/transfer-function Note); tells when one transfer function suffices and when state space or LQR is needed [multivariable = MIMO control] |
| adaptive control (adaptive) | Modern MIMO system design | out-of-scope | plan §7 dropped ME-069: robust and adaptive control beyond beginner depth; model error handled by system ID and domain randomization (N137, N139); learned adaptation is N167 |
| robust control | Modern MIMO system design | out-of-scope | plan §7 dropped ME-069 (robust and adaptive control beyond beginner depth); robustness margins are covered by the NYQUIST add |
| Rudolf E. Kálmán | Modern MIMO system design | index-noise | person |
| Aleksandr Lyapunov | Modern MIMO system design | index-noise | person |
| dynamical system | Stability | taught | plan§4 Stability of dynamical systems; plan§4 State-space models |
| Lyapunov stability | Stability | taught | N199: Stability certificates with Lyapunov functions; plan§4 Stability of dynamical systems |
| linear system | Stability | taught | plan§4 State-space models (x_dot = Ax + Bu) |
| BIBO stability (bounded-input bounded-output (BIBO) stable) | Stability | add | **poles and zeros of a transfer function; stable, marginally stable and BIBO stable** (control) → RO-06 (section of the Laplace/transfer-function Note); N204 places poles of A-BK but never says what poles and zeros of a system are or where stable ones lie |
| bounded function (bounded) | Stability | taught | DL-079 (glossary G-327 Bounded function) |
| nonlinear system | Stability | taught | plan§4 State-space models (nonlinear systems) |
| input-to-state stability | Stability | out-of-scope | graduate nonlinear-control notion (Sontag); no beginner course or plan Note needs it |
| Pole (complex analysis) (poles) | Stability | add | **poles and zeros of a transfer function; stable, marginally stable and BIBO stable** (control) → RO-06 (section of the Laplace/transfer-function Note); N204 places poles of A-BK but never says what poles and zeros of a system are or where stable ones lie |
| complex plane | Stability | add | **Complex numbers for engineers: real and imaginary parts, magnitude and phase, complex plane** (maths) → MA 06-calculus, new Note before the planned ODEs Note; poles, eigenvalues of oscillating systems and the Fourier transform are complex; MA has no complex-number Note |
| unit circle | Stability | add | **Stability of discrete-time linear systems: eigenvalues inside the unit circle** (maths) → MA 06-calculus, extend the planned Stability of dynamical systems Note; sampled robot loops (N136) are discrete; the planned stability Note covers only continuous time [unit circle as the discrete-time stability boundary] |
| Z-transform | Stability | add | **Z-transform and discrete-time transfer functions** (control) → RO-06 (section of the Laplace/transfer-function Note); robot controllers run in discrete time (N136); the discrete twin of the Laplace transform is not taught |
| Cartesian coordinates | Stability | taught | N65: Coordinate frames and the transform tree |
| circular coordinates | Stability | taught | N120: polar-coordinate controller (moving to a pose) |
| asymptotic stability (asymptotically stable) | Stability | add | **exponential vs asymptotic stability** (maths) → MA 06-calculus (extend Stability of dynamical systems); stability definitions used by N124 and N199 (Lyapunov) are not stated |
| Absolute value (modulus) | Stability | taught | ML-024 (glossary G-159 Absolute value) |
| marginal stability (marginally stable) | Stability | add | **poles and zeros of a transfer function; stable, marginally stable and BIBO stable** (control) → RO-06 (section of the Laplace/transfer-function Note); N204 places poles of A-BK but never says what poles and zeros of a system are or where stable ones lie [marginal stability] |
| impulse response | Stability | add | **Response of linear time-invariant systems: linearity, superposition, impulse and step response** (control) → MA 06-calculus, new Note after the planned Matrix exponential Note; every transfer-function, Bode and convolution idea rests on linearity and the impulse response; no Note names them |
| imaginary number (imaginary part) | Stability | add | **Complex numbers for engineers: real and imaginary parts, magnitude and phase, complex plane** (maths) → MA 06-calculus, new Note before the planned ODEs Note; poles, eigenvalues of oscillating systems and the Fourier transform are complex; MA has no complex-number Note |
| Nyquist plot | Stability | add | **Loop transfer function and the Nyquist criterion (gain and phase margins)** (control) → RO-06, new Note after the frequency-response Note; stability margins of a feedback loop; plan has none |
| Ship stability (antiroll fins) | Stability | out-of-scope | different field: naval architecture (ship roll fins example) |
| Controllability | Controllability and observability | taught | N204: Controllability (reachability) and the rank test |
| Observability | Controllability and observability | taught | N80: Kalman filter (Teaches lists Observability) |
| eigenvalues | Controllability and observability | taught | MA-056 eigenvectors and eigenvalues |
| robotics | Control specification | index-noise | name of the whole field |
| integrator | Control specification | taught | N119: integral action, integrator windup |
| rise time | Control specification | add | **Step-response specifications and steady state: rise time, steady-state error, first-order lag** (control) → RO-06, extend Note 118 (step response and second-order systems); N118 lists overshoot, settling time, damping only |
| overshoot (signal) (overshoot) | Control specification | taught | N118: step response (overshoot) |
| settling time | Control specification | taught | N118: step response (settling time) |
| system dynamics | Model identification and robustness | out-of-scope | different field: Forrester's stock-and-flow modelling of social/business systems, not mechanical dynamics |
| system identification | Model identification and robustness | taught | N139: System identification and actuator models |
| Mass-spring-damper model (mass-spring-damper) | Model identification and robustness | taught | plan§4 Second-order linear systems (mass-spring-damper) |
| Nyquist diagram (Nyquist) | Model identification and robustness | add | **Loop transfer function and the Nyquist criterion (gain and phase margins)** (control) → RO-06, new Note after the frequency-response Note; stability margins of a feedback loop; plan has none |
| Bode diagram | Model identification and robustness | add | **frequency response and Bode plots (gain, phase, bandwidth, resonance)** (control) → RO-06 (new Note after the Laplace/transfer-function Note); standard way to read a loop's speed and robustness; plan has none |
| model predictive control | Model identification and robustness | taught | N207: Model predictive control |
| anti-wind up system (control) (anti-wind up systems) | Model identification and robustness | taught | N119: Integrator windup and actuator saturation (anti-windup) |
| aerospace industry | Nonlinear systems control | out-of-scope | industry name |
| feedback linearization | Nonlinear systems control | taught | N124: Feedback linearisation |
| backstepping | Nonlinear systems control | out-of-scope | graduate nonlinear design method (Khalil ch. 14); plan §7 ME-069 drops robust/adaptive design; plan teaches PID, LQR, feedback linearisation, MPC instead |
| sliding mode control | Nonlinear systems control | out-of-scope | graduate robust nonlinear method; same reason as plan §7 ME-069 (robust control dropped) |
| Lyapunov's theory | Nonlinear systems control | taught | N199: Lyapunov functions |
| Differential geometry | Nonlinear systems control | out-of-scope | plan §7 dropped PA 8.5: differential geometry beyond beginner depth |
| Distributed control system | Decentralized systems control | out-of-scope | different field: industrial process-plant control architecture (DCS) |
| Stochastic control | Deterministic and stochastic systems control | add | **LQG control and the separation principle** (control) → RO-15 (extend N206); joins the Kalman filter (N80) with LQR (N205); the standard stochastic-control result [stochastic control at beginner level = LQG; MDPs (N7) are its discrete form] |
| Optimal control | Main control strategies | taught | N205: Hamilton-Jacobi-Bellman equation and LQR; N116 Trajectory optimisation |
| linear–quadratic–Gaussian control | Main control strategies | add | **LQG control and the separation principle** (control) → RO-15 (extend N206); joins the Kalman filter (N80) with LQR (N205); the standard stochastic-control result |
| process control | Main control strategies | out-of-scope | different field: chemical/industrial process control |
| Hendrik Wade Bode (Bode) | Main control strategies | index-noise | person |
| H-infinity loop-shaping | Main control strategies | out-of-scope | graduate robust control (H-infinity synthesis); plan §7 ME-069 dropped robust control |
| Keith Glover | Main control strategies | index-noise | person |
| Vadim Utkin | Main control strategies | index-noise | person |
| Stability theory (stability) | Main control strategies | taught | plan§4 Stability of dynamical systems |
| hierarchical control system | Main control strategies | taught | N126: autonomy stack layers mission → behaviour → motion → control |
| control system | Main control strategies | taught | N117: PD / PID feedback control |
| hierarchical | Main control strategies | index-noise | generic adjective |
| tree (data structure) (tree) | Main control strategies | taught | ML-091 decision trees (tree structure); N65 transform tree |
| computer network | Main control strategies | out-of-scope | different field: computer networking |
| networked control system | Main control strategies | out-of-scope | research field: control over communication networks |
| Intelligent control | Main control strategies | index-noise | umbrella heading; members (NN, Bayesian, ML, evolutionary) judged in own rows |
| artificial neural networks | Main control strategies | taught | DL-009 MLP intuition (DL-008..DL-010) |
| Bayesian probability | Main control strategies | taught | MA-018 Bayes' theorem |
| fuzzy logic | Main control strategies | out-of-scope | different method family (fuzzy sets); the plan and its surveys model uncertainty with probability |
| machine learning | Main control strategies | taught | ML-001 what is ML |
| evolutionary computation | Main control strategies | taught | N43: evolution strategies and CMA-ES |
| genetic algorithms | Main control strategies | add | **genetic algorithms (selection, crossover, mutation)** (RL) → RL-04 (extend N43); N43 teaches evolution strategies and CMA-ES; the genetic algorithm, the best-known evolutionary method, is not named |
| neuro-fuzzy | Main control strategies | out-of-scope | fuzzy-neural hybrid; same reason as fuzzy logic |
| dynamic system | Main control strategies | taught | plan§4 Stability of dynamical systems |
| Self-organized criticality control | Main control strategies | out-of-scope | physics research topic (self-organized criticality) |
| self-organized | Main control strategies | index-noise | generic adjective |
| Automation | See also | index-noise | umbrella word "automation"; driving automation levels are N244 |
| Deadbeat controller | See also | out-of-scope | digital-control-course design method; no robot controller in the plan or its surveys uses it |
| Distributed parameter systems | See also | out-of-scope | PDE-governed systems; graduate control |
| Fractional-order control | See also | out-of-scope | research topic (fractional calculus) |
| Servomechanism | See also | add | **electric motor types: DC, brushless, stepper, servo, AC** (robotics) → RB-02 (new Note before N283); actuators beyond the motor model in N283 are not covered [servomechanism = motor with position feedback] |
| Vector control (motor) | See also | out-of-scope | power-electronics drive technique (field-oriented control) inside motor drivers |
| Vector control | See also | index-noise | disambiguation page duplicate of the row above |
| Coefficient diagram method | See also | out-of-scope | niche research design method |
| Control reconfiguration | See also | out-of-scope | research topic: fault-tolerant reconfiguration |
| Feedback | See also | taught | N117: feedback control |
| H infinity | See also | out-of-scope | graduate robust control; plan §7 ME-069 |
| Hankel singular value | See also | out-of-scope | graduate model-reduction tool |
| Krener's theorem | See also | out-of-scope | graduate nonlinear-controllability theorem; plan §7 PA 15.5 drops controllability theory beyond the rank test |
| Lead-lag compensator | See also | add | **Loop-shaping design: lead and lag compensators** (control) → RO-06, new Note after the Nyquist/robustness Note; classical frequency-domain controller design; plan has none |
| Minor loop feedback | See also | taught | N119: cascaded loops |
| Multi-loop feedback | See also | taught | N119: cascaded loops |
| Positive systems | See also | out-of-scope | research topic |
| Radial basis function | See also | taught | N26: RBF features; ML-089 RBF kernel |
| Signal-flow graph | See also | out-of-scope | alternative notation to block diagrams (Mason's rule); not used by robotics courses |
| Stable polynomial | See also | add | **poles and zeros of a transfer function; stable, marginally stable and BIBO stable** (control) → RO-06 (section of the Laplace/transfer-function Note); N204 places poles of A-BK but never says what poles and zeros of a system are or where stable ones lie [stable (Hurwitz) polynomial] |
| State space representation | See also | taught | plan§4 State-space models |
| Steady state | See also | add | **Step-response specifications and steady state: rise time, steady-state error, first-order lag** (control) → RO-06, extend Note 118 (step response and second-order systems); N118 lists overshoot, settling time, damping only [steady state and steady-state error] |
| Transient response | See also | taught | N118: step response (transient: overshoot, settling) |
| Transient state | See also | taught | N118: step response (transient) |
| Underactuation | See also | taught | N221: underactuation: tilt to move |
| Youla–Kucera parametrization | See also | out-of-scope | graduate robust-control parametrization |
| Markov chain approximation method | See also | out-of-scope | research numerical method for stochastic control (Kushner) |
| Adaptive system | See also | index-noise | umbrella systems-theory term |
| Automation and remote control | See also | index-noise | journal name |
| Bond graph | See also | out-of-scope | specialist modelling notation (mechatronics) |
| Control engineering | See also | index-noise | umbrella field name |
| Control–feedback–abort loop | See also | out-of-scope | spaceflight operations term |
| Controller (control theory) | See also | taught | N117: PD and PID control |
| Cybernetics | See also | out-of-scope | history / umbrella field |
| Mathematical system theory | See also | index-noise | umbrella field name |
| Negative feedback amplifier | See also | out-of-scope | different field: electronics |
| Outline of management | See also | index-noise | unrelated outline page |
| People in systems and control | See also | index-noise | list of people |
| Perceptual control theory | See also | out-of-scope | different field: psychology |
| Systems theory | See also | index-noise | umbrella field name |

## Outline of computer vision

Source: https://en.wikipedia.org/wiki/Outline_of_computer_vision (revision 1349613121), accessed 2026-10-07. List of computer vision topics redirects here. Every linked term, sub-bullets and See also included.

Counts: taught 36, add 11, out-of-scope 71, index-noise 42 (total 160).

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| Outline (list) (outline) | (lead) | index-noise | page-type word |
| Computer vision | (lead) | index-noise | name of the whole field |
| Interdisciplinarity (interdisciplinary field) | (lead) | index-noise | generic word |
| digital image | (lead) | taught | DL-042 convolution operation (image as a grid of numbers; plan §5 recap) |
| video | (lead) | index-noise | generic medium |
| engineering | (lead) | index-noise | generic field name |
| image sensor | (lead) | add | **image sensors: CCD/CMOS, exposure, rolling vs global shutter** (vision) → RO-03 (extend N88); motion blur and rolling-shutter skew on a moving robot come from the sensor; N88 starts at the pinhole model |
| image processing | (lead) | index-noise | umbrella field name; its methods are judged in their own rows |
| image analysis | (lead) | index-noise | umbrella field name |
| Computer stereo vision | Branches of computer vision | taught | N90: Depth from stereo and depth cameras |
| Underwater computer vision | Branches of computer vision | out-of-scope | specialised domain (underwater imaging); the plan covers ground, aerial and arm robots |
| History of computer vision | History of computer vision | out-of-scope | history |
| Image denoising | Image enhancement | taught | N227: Image filtering: smoothing filters |
| Image histogram | Image enhancement | add | **image histograms and point operations: contrast, gamma, histogram equalization, thresholding, binary images and contours** (vision) → RO-18 (extend N227); first steps of every vision pipeline (and of colour-blob robot labs); the plan starts at gradient filters |
| Inpainting | Image enhancement | out-of-scope | image-editing application (fill missing regions) |
| Super-resolution imaging | Image enhancement | out-of-scope | imaging research topic; robots use the sensor resolution they have |
| Histogram equalization | Image enhancement | add | **image histograms and point operations: contrast, gamma, histogram equalization, thresholding, binary images and contours** (vision) → RO-18 (extend N227); first steps of every vision pipeline (and of colour-blob robot labs); the plan starts at gradient filters |
| Tone mapping | Image enhancement | out-of-scope | photography/HDR display technique |
| Retinex | Image enhancement | out-of-scope | colour-constancy research model |
| Gamma correction | Image enhancement | add | **image histograms and point operations: contrast, gamma, histogram equalization, thresholding, binary images and contours** (vision) → RO-18 (extend N227); first steps of every vision pipeline (and of colour-blob robot labs); the plan starts at gradient filters |
| Anisotropic diffusion | Image enhancement | out-of-scope | research edge-preserving smoothing (Perona-Malik); beyond beginner filtering |
| Affine transform | Transformations | add | **2D image transformations: translation, similarity, affine, projective; image warping** (vision) → RO-18 (extend N229); N229 teaches the homography alone; the affine family and how to warp an image are not taught |
| Homography (computer vision) | Transformations | taught | N229: RANSAC and homographies |
| Hough transform | Transformations | add | **Hough transform** (vision) → RO-18 (extend N229); standard line/circle finder (lane lines, scan lines); absent from the plan |
| Radon transform | Transformations | out-of-scope | different field: tomography (medical imaging) |
| Walsh–Hadamard transform | Transformations | out-of-scope | signal-processing transform not used in robot vision |
| Image compression | Filtering, Fourier and wavelet transforms and image compression | out-of-scope | different field: storage/coding |
| Filter bank | Filtering, Fourier and wavelet transforms and image compression | out-of-scope | signal-processing construction (texture, compression); not in beginner robot vision |
| Gabor filter | Filtering, Fourier and wavelet transforms and image compression | out-of-scope | texture-analysis filter; CNN filters (DL-042) took its role |
| JPEG 2000 | Filtering, Fourier and wavelet transforms and image compression | out-of-scope | file format |
| Adaptive filtering | Filtering, Fourier and wavelet transforms and image compression | out-of-scope | different field: DSP (LMS adaptive filters) |
| Visual perception | Color vision | out-of-scope | different field: psychology of perception |
| Human visual system model | Color vision | out-of-scope | different field: vision science |
| Color matching function | Color vision | out-of-scope | different field: colour science |
| Color space | Color vision | add | **colour spaces beyond RGB: grayscale conversion, HSV** (vision) → RO-18 (extend N227); colour segmentation under changing light uses HSV; DL-042 teaches only RGB channels |
| Color appearance model | Color vision | out-of-scope | different field: colour science |
| Color management system | Color vision | out-of-scope | different field: printing/display colour management |
| Color mapping | Color vision | out-of-scope | different field: colour science / graphics |
| Color model | Color vision | taught | DL-042 §3.2 Colour (RGB) images |
| Color profile | Color vision | out-of-scope | different field: printing/display colour management |
| Active contour | Feature extraction | out-of-scope | research-era segmentation (snakes); learned segmentation is N175 |
| Blob detection | Feature extraction | taught | N228: Scale-space blobs, descriptors and SIFT |
| Canny edge detector | Feature extraction | add | **edge detection and the Canny edge detector (non-max suppression, hysteresis, edge linking)** (vision) → RO-18 (extend N227); DL-042 shows edges as brightness change and N227 gradient filters; turning gradients into clean edges is not taught |
| Contour detection | Feature extraction | add | **image histograms and point operations: contrast, gamma, histogram equalization, thresholding, binary images and contours** (vision) → RO-18 (extend N227); first steps of every vision pipeline (and of colour-blob robot labs); the plan starts at gradient filters [contours of binary regions] |
| Edge detection | Feature extraction | taught | DL-042 (edges as brightness changes, plan §5 recap); N227 gradient filters |
| Edge linking | Feature extraction | add | **edge detection and the Canny edge detector (non-max suppression, hysteresis, edge linking)** (vision) → RO-18 (extend N227); DL-042 shows edges as brightness change and N227 gradient filters; turning gradients into clean edges is not taught [edge linking (hysteresis)] |
| Harris Corner Detector | Feature extraction | taught | N227: Harris and Shi-Tomasi corners |
| Histogram of oriented gradients | Feature extraction | out-of-scope | pre-deep-learning detector feature; replaced by the CNN detectors in N173-N174 |
| Random sample consensus | Feature extraction | taught | N229: RANSAC |
| Scale-invariant feature transform | Feature extraction | taught | N228: SIFT |
| Bundle adjustment | Pose estimation | taught | N235: Bundle adjustment |
| Articulated body pose estimation | Pose estimation | add | **human pose estimation: body keypoints from images** (vision) → RB-06 (extend N317); N317 and N337 use human poses from video but no Note says how a body pose is estimated from an image |
| Direct linear transformation | Pose estimation | taught | N89: Direct linear transform (DLT) |
| Epipolar geometry | Pose estimation | taught | N232: Epipolar geometry |
| Fundamental matrix (computer vision) (Fundamental matrix) | Pose estimation | taught | N232: Fundamental matrix F |
| Pinhole camera model | Pose estimation | taught | N88: Pinhole camera |
| Projective geometry | Pose estimation | taught | N88: Homogeneous coordinates; plan§4 Projective homogeneous coordinates |
| Trifocal tensor | Pose estimation | out-of-scope | three-view geometry beyond beginner depth (Hartley-Zisserman Part III); two-view geometry is N232 |
| Active appearance model | Registration | out-of-scope | face-modelling research method |
| Cross-correlation | Registration | taught | DL-042 (glossary G-508 Cross-correlation) |
| Geometric hashing | Registration | out-of-scope | research-era recognition method |
| Graph cut segmentation | Registration | out-of-scope | classic energy-minimisation segmentation; replaced by learned segmentation (N175) |
| Least squares (Least squares estimation) | Registration | taught | ML-053 multiple linear regression maths (least squares); N230 Lucas-Kanade by least squares |
| Pyramid (image processing) (Image pyramid) | Registration | taught | N227: Image pyramids |
| Image segmentation | Registration | taught | N175: Semantic segmentation |
| Level-set method | Registration | out-of-scope | research PDE segmentation method |
| Markov random field | Registration | out-of-scope | graphical-model labelling method; replaced by learned segmentation (N175) |
| Medial axis | Registration | taught | N270: maximum-clearance roadmap (generalized Voronoi diagram = medial axis) |
| Motion field | Registration | taught | N231: Image motion from camera motion (the image Jacobian) |
| Motion vector | Registration | out-of-scope | different field: video-compression block motion vectors |
| Multispectral imaging | Registration | out-of-scope | different field: remote sensing |
| Normalized cut segmentation | Registration | out-of-scope | classic graph-based segmentation; replaced by learned segmentation (N175) |
| Optical flow | Registration | taught | N230: Optical flow |
| Particle filter | Registration | taught | N82: Particle filter |
| Scale space | Registration | taught | N228: Scale-space blobs |
| Object recognition | Visual recognition | taught | DL-049 CNN image classification; N173 object detection |
| Gesture recognition | Visual recognition | out-of-scope | application (gesture interfaces) |
| Bag-of-words model in computer vision | Visual recognition | taught | N236: Visual place recognition with bag of words |
| Kadir–Brady saliency detector | Visual recognition | out-of-scope | research saliency detector |
| Eigenface | Visual recognition | out-of-scope | face-recognition application of PCA (PCA itself is ML-046) |
| 5DX | Commercial computer vision systems | index-noise | product name |
| Aphelion (software) | Commercial computer vision systems | index-noise | product name |
| Microsoft PixelSense | Commercial computer vision systems | index-noise | product name |
| Poseidon drowning detection system | Commercial computer vision systems | index-noise | product name |
| Roboflow | Commercial computer vision systems | index-noise | product/company name |
| Visage SDK | Commercial computer vision systems | index-noise | product name |
| 3D reconstruction from multiple images | Applications | taught | N235: Structure from motion |
| Audio-visual speech recognition | Applications | out-of-scope | different field: speech recognition |
| Augmented reality | Applications | out-of-scope | application (AR displays) |
| Augmented reality-assisted surgery | Applications | out-of-scope | different field: medicine |
| Automated optical inspection | Applications | out-of-scope | different field: industrial inspection |
| Automatic image annotation | Applications | out-of-scope | application (image tagging) |
| Automatic number plate recognition | Applications | out-of-scope | application (traffic enforcement) |
| Automatic target recognition | Applications | out-of-scope | military application |
| Check weigher | Applications | out-of-scope | different field: packaging machinery |
| Closed-circuit television | Applications | out-of-scope | different field: surveillance hardware |
| Contextual image classification | Applications | out-of-scope | research classification method |
| DARPA LAGR Program | Applications | index-noise | program name (DARPA learning off-road navigation; the concept is N177) |
| Digital video fingerprinting | Applications | out-of-scope | application (copy detection) |
| Document mosaicing | Applications | out-of-scope | application (document scanning) |
| Facial recognition system | Applications | out-of-scope | application (biometrics) |
| GazoPa | Applications | index-noise | product name |
| Geometric feature learning | Applications | out-of-scope | research method |
| Image collection exploration | Applications | out-of-scope | application (photo browsing) |
| Image retrieval | Applications | taught | N236: Visual place recognition with bag of words (image retrieval) |
| Content-based image retrieval | Applications | taught | N236: place recognition = content-based image retrieval with bag of words |
| Reverse image search | Applications | out-of-scope | web-search product feature |
| Image-based modeling and rendering | Applications | out-of-scope | different field: computer graphics |
| Integrated mail processing | Applications | out-of-scope | application (postal sorting) |
| Iris recognition | Applications | out-of-scope | application (biometrics) |
| Machine vision | Applications | out-of-scope | industrial inspection field |
| Mobile mapping | Applications | out-of-scope | surveying-industry practice; robot mapping is RO-04 and HD maps N245 |
| Autonomous car | Applications | taught | N244: driving automation levels (RO-20 Autonomous driving) |
| Mobile robot | Applications | taught | N64: Pose and wheeled-robot motion |
| Object detection | Applications | taught | N173: Object detection |
| Optical braille recognition | Applications | out-of-scope | application (document reading) |
| Optical character recognition | Applications | out-of-scope | application (document reading) |
| Intelligent character recognition | Applications | out-of-scope | application (document reading) |
| Pedestrian detection | Applications | taught | N173: Object detection (pedestrians as a detected class); N179 predicting where people go |
| People counter | Applications | out-of-scope | application |
| Physical computing | Applications | out-of-scope | hobby electronics practice |
| Red light camera | Applications | out-of-scope | application (traffic enforcement) |
| Remote sensing | Applications | out-of-scope | different field: remote sensing |
| Smart camera | Applications | out-of-scope | hardware product category |
| Traffic enforcement camera | Applications | out-of-scope | application (traffic enforcement) |
| Traffic sign recognition | Applications | taught | N173: traffic-light recognition as a detection task |
| Vehicle infrastructure integration | Applications | out-of-scope | vehicle-to-infrastructure communication; infrastructure policy, not robot perception |
| Velocity Moments | Applications | out-of-scope | research shape descriptor |
| Video content analysis | Applications | out-of-scope | application (video analytics) |
| View synthesis | Applications | out-of-scope | different field: graphics (novel view rendering) |
| Visual sensor network | Applications | out-of-scope | research field (camera networks) |
| Visual Word | Applications | taught | N236: bag of (visual) words |
| Water remote sensing | Applications | out-of-scope | different field: remote sensing |
| 3DFLOW | Computer vision companies | index-noise | company name |
| Automatix | Computer vision companies | index-noise | company name |
| Clarifai | Computer vision companies | index-noise | company name |
| Cognex Corporation | Computer vision companies | index-noise | company name |
| Datagen | Computer vision companies | index-noise | company name |
| Diffbot | Computer vision companies | index-noise | company name |
| IBM | Computer vision companies | index-noise | company name |
| InspecVision | Computer vision companies | index-noise | company name |
| Isra Vision | Computer vision companies | index-noise | company name |
| Kinesense | Computer vision companies | index-noise | company name |
| Mobileye | Computer vision companies | index-noise | company name |
| Scantron Corporation | Computer vision companies | index-noise | company name |
| Teledyne DALSA | Computer vision companies | index-noise | company name |
| VIEW Engineering | Computer vision companies | index-noise | company name |
| Warden Machinery | Computer vision companies | index-noise | company name |
| Zivid | Computer vision companies | index-noise | company name |
| Electronic Letters on Computer Vision and Image Analysis | Computer vision publications | index-noise | journal name |
| International Journal of Computer Vision | Computer vision publications | index-noise | journal name |
| Conference on Computer Vision and Pattern Recognition | Computer vision organizations | index-noise | conference name |
| European Conference on Computer Vision | Computer vision organizations | index-noise | conference name |
| International Conference on Computer Vision | Computer vision organizations | index-noise | conference name |
| International Conferences in Central Europe on Computer Graphics, Visualization and Computer Vision | Computer vision organizations | index-noise | conference name |
| Outline of artificial intelligence | See also | index-noise | see-also pointer to another list page |
| Outline of deep learning | See also | index-noise | see-also pointer to another list page |
| Outline of robotics | See also | index-noise | see-also pointer to another list page |
| List of computer graphics and descriptive geometry topics | See also | index-noise | see-also pointer to another list page |
| Virtual Design and Construction | See also | index-noise | see-also pointer to another list page |

## Self-driving car (Technology section)

Source: https://en.wikipedia.org/wiki/Self-driving_car (revision 1378736899), accessed 2026-10-07. Outline of autonomous vehicles and Glossary of autonomous vehicles do not exist (API: missing). Used the Self-driving car article's Technology section plus its Behavior prediction and Collision avoidance / Simulation subsections; history, incidents, regulation and business sections left out.

Counts: taught 15, add 1, out-of-scope 6, index-noise 9 (total 31).

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| Vehicular automation | Technology | index-noise | umbrella page name (vehicle automation) |
| control system | Architecture | taught | N117: PD / PID feedback control |
| Motional | Architecture | index-noise | company name |
| Hybrid navigation | Navigation | taught | N86: Fusing IMU, wheels and GNSS (hybrid navigation = INS + GNSS fusion) |
| navigation system | Navigation | taught | N126: The autonomy stack (navigation system layers); N131 Nav2 navigation stack |
| Lidar | Perception | taught | N91: How LiDAR works |
| radar | Perception | taught | N91: other range sensors: radar (range and Doppler) |
| ultrasound | Perception | add | **proximity and contact sensors (bumpers, infrared, ultrasonic)** (robotics) → RO-03 (new Note before N83); cheapest obstacle sensors on mobile robots and cars (parking sensors); RO-03 starts at IMU [ultrasonic ranging] |
| GPS | Perception | taught | N85: Satellite positioning: GNSS and RTK |
| Inertial measurement unit (inertial measurement) | Perception | taught | N83: Inertial sensors: gyroscope, accelerometer |
| Deep neural networks | Perception | taught | DL-009 MLP and DL chapters (deep networks) |
| Bayes' theorem (Bayesian) | Perception | taught | MA-018 Bayes' theorem; N78 Bayes filter |
| simultaneous localization and mapping | Perception | taught | N100: The SLAM problem |
| real-time locating system | Perception | out-of-scope | infrastructure asset-tracking systems (RFID/UWB tags); robot self-localization is taught in RO-04 |
| Motion planning (Path planning) | Path planning | taught | N72: basic motion planning problem; RO-05 path planning Notes N103-N116 |
| Voronoi diagram | Path planning | taught | N270: generalized Voronoi diagram |
| occupancy grid mapping | Path planning | taught | N96: Occupancy grid mapping |
| MIT Computer Science and Artificial Intelligence Laboratory (Computer Science and Artificial Intelligence Laboratory) | Maps | index-noise | organisation |
| OpenStreetMap | Maps | out-of-scope | a specific map dataset/service; road-graph route planning is N115 |
| sensor fusion (combine data from multiple sensors) | Sensors | taught | N86: EKF fusion of IMU, wheels and GNSS |
| Drive by wire | Drive by wire | out-of-scope | vehicle hardware (electronic actuation); the plan commands steering and throttle (N252) |
| Driver monitoring system | Driver monitoring | out-of-scope | in-cabin human monitoring for driver-assist cars; not robot perception |
| Vehicular communication systems | Vehicle communication | out-of-scope | V2X communication standards; infrastructure, not a robotics concept |
| International Organization for Standardization (ISO) | Vehicle communication | index-noise | organisation |
| Over-the-air programming | Software update | out-of-scope | software-deployment practice |
| United Nations Economic Commission for Europe (UNECE) | Software update | index-noise | organisation |
| National Institute of Informatics | Safety model | index-noise | organisation |
| Artificial intelligence | Artificial Intelligence | taught | ML-002 AI vs ML vs DL |
| Nissan | Collision avoidance | index-noise | company name |
| Waymo | Collision avoidance | index-noise | company name |
| Association for Standardisation of Automation and Measuring Systems (ASAM) | Simulation and validation | index-noise | standards organisation |

## Outline of machine learning (RL and paradigms only)

Source: https://en.wikipedia.org/wiki/Outline_of_machine_learning (revision 1378611610), accessed 2026-10-07. Only the Paradigms of machine learning and Reinforcement learning sections, as asked; no robotics section exists on the page.

Counts: taught 6, add 0, out-of-scope 1, index-noise 0 (total 7).

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| Supervised learning | Paradigms of machine learning | taught | ML-003 types of ML |
| Unsupervised learning | Paradigms of machine learning | taught | ML-003 types of ML (glossary G-2058) |
| Reinforcement learning | Paradigms of machine learning | taught | N1: The reinforcement learning problem |
| Q-learning | Reinforcement learning | taught | N21: Q-learning |
| State–action–reward–state–action | Reinforcement learning | taught | N20: Sarsa and expected Sarsa |
| Temporal difference learning | Reinforcement learning | taught | N19: TD(0) prediction |
| Learning Automata | Reinforcement learning | out-of-scope | history: early stochastic-automaton formulation of trial-and-error learning; bandit methods N2-N6 teach the same problem |
