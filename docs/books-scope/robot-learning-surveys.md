# Gap scope: learning-based robotics, mapped from survey papers

> **Plan of record:** [robotics.md](robotics.md). This doc is evidence: its rows (IDs `RS-NNN`), sources and checks. "Note N" or "RO N" below means the earlier 188-Note draft (2026-10-07), not today's plan.


> **Plan of record:** the 188-Note draft of [robotics.md](robotics.md) (2026-10-07). This doc maps the field from review papers, then checks each method family against that plan. RO numbers below are robotics.md Note numbers.

## Summary

**Sources.** 26 surveys across 8 sub-areas. Each was checked on arXiv (title, first author, PDF), and the published version on Crossref or the publisher (DOI, journal, volume, pages). Section structure was read from each survey's own PDF (pdftotext of the arXiv or open-access copy), not from memory. Two surveys had no open full text that loaded: Sun et al. (ObjectNav) and Zhu & Zhang; their method groups come from the published abstracts. Singamaneni, Duan, Hu and Ma were read for structure only.

| Sub-area | Survey | Checked at |
|---|---|---|
| RL for robots | Kober, Bagnell & Peters 2013, *Reinforcement learning in robotics: a survey*, IJRR 32(11):1238-1274 | [Crossref 10.1177/0278364913495721](https://doi.org/10.1177/0278364913495721); free PDF [TU Darmstadt](https://www.ias.informatik.tu-darmstadt.de/uploads/Publications/Kober_IJRR_2013.pdf) |
| RL for robots | Ibarz et al. 2021, *How to train your robot with deep RL: lessons we have learned*, IJRR 40:698-721 | [arXiv 2102.02915](https://arxiv.org/abs/2102.02915); [Crossref 10.1177/0278364920987859](https://doi.org/10.1177/0278364920987859) |
| RL for robots | Tang, Abbatematteo, Hu, Chandra, Martín-Martín, Stone 2025, *Deep RL for robotics: a survey of real-world successes*, Annu. Rev. Control Robot. Auton. Syst. 8:153-188 | [arXiv 2408.03539](https://arxiv.org/abs/2408.03539); [Crossref 10.1146/annurev-control-030323-022510](https://doi.org/10.1146/annurev-control-030323-022510) |
| Navigation | Xiao, Liu, Warnell, Stone 2022, *Motion planning and control for mobile robot navigation using machine learning: a survey*, Autonomous Robots 46:569-597 | [arXiv 2011.13112](https://arxiv.org/abs/2011.13112); [Crossref 10.1007/s10514-022-10039-8](https://doi.org/10.1007/s10514-022-10039-8) |
| Navigation | Zhu & Zhang 2021, *Deep RL based mobile robot navigation: a review*, Tsinghua Sci. Technol. 26(5):674-691 | [Crossref 10.26599/TST.2021.9010012](https://doi.org/10.26599/TST.2021.9010012); [SciOpen page](https://www.sciopen.com/article/10.26599/TST.2021.9010012) (abstract only) |
| Navigation (embodied) | Duan et al. 2022, *A survey of embodied AI: from simulators to research tasks*, IEEE TETCI | [arXiv 2103.04918](https://arxiv.org/abs/2103.04918) |
| Navigation (object goal) | Sun, Wu, Ji, Lai 2025, *A survey of object goal navigation*, IEEE T-ASE 22:2292-2308 | [Crossref 10.1109/TASE.2024.3378010](https://doi.org/10.1109/TASE.2024.3378010) (abstract only) |
| Navigation (language) | Gu, Stefani, Wu, Thomason, Wang 2022, *Vision-and-language navigation: a survey of tasks, methods, and future directions*, ACL 2022 | [arXiv 2203.12667](https://arxiv.org/abs/2203.12667); [DOI 10.18653/v1/2022.acl-long.524](https://doi.org/10.18653/v1/2022.acl-long.524) |
| Navigation (social) | Mavrogiannis et al. 2023, *Core challenges of social robot navigation: a survey*, ACM THRI 12:1-39 | [arXiv 2103.05668](https://arxiv.org/abs/2103.05668); [Crossref 10.1145/3583741](https://doi.org/10.1145/3583741) |
| Navigation (social) | Singamaneni et al. 2024, *A survey on socially aware robot navigation: taxonomy and future challenges*, IJRR | [arXiv 2311.06922](https://arxiv.org/abs/2311.06922); [DOI 10.1177/02783649241230562](https://doi.org/10.1177/02783649241230562) |
| Legged | Ha, Lee, van de Panne, Xie, Yu, Khadiv 2025, *Learning-based legged locomotion: state of the art and future perspectives*, IJRR 44:1396-1427 | [arXiv 2406.01152](https://arxiv.org/abs/2406.01152); [Crossref 10.1177/02783649241312698](https://doi.org/10.1177/02783649241312698) |
| Manipulation / IL | Ravichandar, Polydoros, Chernova, Billard 2020, *Recent advances in robot learning from demonstration*, Annu. Rev. CRAS 3:297-330 | [Crossref 10.1146/annurev-control-100819-063206](https://doi.org/10.1146/annurev-control-100819-063206); accepted PDF on [EPFL Infoscience](https://infoscience.epfl.ch/entities/publication/fb601853-11db-40a8-9c47-b0a6470d662d) |
| Manipulation / IL | Kroemer, Niekum, Konidaris 2021, *A review of robot learning for manipulation*, JMLR 22(30) | [arXiv 1907.03146](https://arxiv.org/abs/1907.03146); [JMLR page](https://jmlr.org/papers/v22/19-804.html) |
| Manipulation / IL | Zare, Kebria, Khosravi, Nahavandi 2023, *A survey of imitation learning: algorithms, recent developments, and challenges* (IEEE T-Cybernetics) | [arXiv 2309.02473](https://arxiv.org/abs/2309.02473) |
| Manipulation / IL | Wolf, Shi, Liu, Rayyes 2025, *Diffusion models for robotic manipulation: a survey*, Frontiers in Robotics and AI | [arXiv 2504.08438](https://arxiv.org/abs/2504.08438); [Crossref 10.3389/frobt.2025.1606247](https://doi.org/10.3389/frobt.2025.1606247) |
| Humanoid | Gu et al. 2025, *Humanoid locomotion and manipulation: current progress and challenges in control, planning, and learning* | [arXiv 2501.02116](https://arxiv.org/abs/2501.02116) |
| Humanoid | Yuan et al. 2025, *A survey of behavior foundation model: next-generation whole-body control system of humanoid robots*, IEEE TPAMI | [arXiv 2506.20487](https://arxiv.org/abs/2506.20487) |
| Sim-to-real | Zhao, Peña Queralta, Westerlund 2020, *Sim-to-real transfer in deep RL for robotics: a survey*, IEEE SSCI 2020:737-744 | [arXiv 2009.13303](https://arxiv.org/abs/2009.13303); [DOI 10.1109/SSCI47803.2020.9308468](https://doi.org/10.1109/SSCI47803.2020.9308468) |
| Sim-to-real | Muratore, Ramos, Turk, Yu, Gienger, Peters 2022, *Robot learning from randomized simulations: a review*, Front. Robot. AI 9 | [arXiv 2111.00956](https://arxiv.org/abs/2111.00956); [Crossref 10.3389/frobt.2022.799893](https://doi.org/10.3389/frobt.2022.799893) |
| Safe RL | García & Fernández 2015, *A comprehensive survey on safe reinforcement learning*, JMLR 16:1437-1480 | [JMLR page](https://jmlr.org/papers/v16/garcia15a.html) |
| Safe RL | Brunke et al. 2022, *Safe learning in robotics: from learning-based control to safe RL*, Annu. Rev. CRAS 5:411-444 | [arXiv 2108.06266](https://arxiv.org/abs/2108.06266); [Crossref 10.1146/annurev-control-042920-020211](https://doi.org/10.1146/annurev-control-042920-020211) |
| Safe RL | Gu et al. 2024, *A review of safe RL: methods, theories and applications*, IEEE TPAMI 46:11216-11235 | [arXiv 2205.10330](https://arxiv.org/abs/2205.10330); [Crossref 10.1109/TPAMI.2024.3457538](https://doi.org/10.1109/TPAMI.2024.3457538) |
| Foundation models | Firoozi et al. 2025, *Foundation models in robotics: applications, challenges, and the future*, IJRR 44:701-739 | [arXiv 2312.07843](https://arxiv.org/abs/2312.07843); [Crossref 10.1177/02783649241281508](https://doi.org/10.1177/02783649241281508) |
| Foundation models | Hu et al. 2023, *Toward general-purpose robots via foundation models: a survey and meta-analysis* | [arXiv 2312.08782](https://arxiv.org/abs/2312.08782) |
| Foundation models | Ma et al. 2025, *A survey on vision-language-action models for embodied AI*, IEEE TNNLS | [arXiv 2405.14093](https://arxiv.org/abs/2405.14093); [DOI 10.1109/TNNLS.2025.3650584](https://doi.org/10.1109/TNNLS.2025.3650584) |
| Foundation models | Kawaharazuka, Oh, Yamada, Posner, Zhu 2025, *Vision-language-action models for robotics: a review towards real-world applications*, IEEE Access | [arXiv 2510.07077](https://arxiv.org/abs/2510.07077); [DOI 10.1109/ACCESS.2025.3609980](https://doi.org/10.1109/ACCESS.2025.3609980) |

**Row counts** (table in §2): **120 rows**: **39 covered**, **37 partial**, **44 new**. By kind: robotics 104, control 11, vision 5, maths 0 (the maths sits in §6: 7 new maths/DL prerequisites). Control rows (MPC, whole-body control, action spaces, safety certificates) overlap the classical-control gap scope; merge them there.

**Main finding.** robotics.md is strong where the surveys say deep RL has worked best: legged locomotion, sim-to-real, privileged learning, mapless navigation. It is thin in four places the surveys treat as major: **imitation learning for manipulation** (diffusion policy, action chunking, demonstration collection, inverse RL), **embodied and semantic navigation** (object-goal, language, open-vocabulary maps), **social navigation beyond RL crowds** (trajectory prediction, social norms), and **mobile manipulation / loco-manipulation and whole-body control**. Several Sutton & Barto and LaValle topics (games, gradient-TD, LSTD) get no mention at all in the robotics surveys (§3).

Status key: **covered** = a robotics.md Note teaches it; **partial** = the Note has the basics, the new part is named; **new** = not in robotics.md or MA/ML/DL.

## 1. Domain map per sub-area (from the surveys' own taxonomies)

**A. RL for robots in general.**
- Families (Kober §2): value-function methods vs policy search; model-free vs model-based. Policy search splits into gradient methods, EM-style reward-weighted updates, path-integral methods, and black-box search (Kober §2.2.2).
- Making it tractable (Kober §4-6): good state/action representations, pre-structured policies (movement primitives), prior knowledge (demonstrations, task structure), models (simulation, learned dynamics).
- Practical lessons (Ibarz §4): stable learning, sample efficiency (model-based, off-policy, demos), simulation and domain adaptation, model exploitation, running at scale (resets, changing environments), delays ("thinking while moving"), reward specification, multi-task and meta-learning, safe learning, persistence.
- Tang's three axes (§3): competency (locomotion, navigation, stationary manipulation, mobile manipulation, human-robot interaction, multi-robot), problem formulation (action level, observation type, reward density), solution approach (sim use, model learning, expert data, policy optimiser, network type).
- Open problems (Tang §5): sample-efficient and stable RL, real-world learning (safe data collection, resets), long-horizon tasks via skills, principled system design, real-world benchmarks, using foundation models.

**B. Learning-based navigation.**
- Xiao's scope axis: learn the whole stack (fixed-goal, moving-goal), learn a subsystem (global planner, local planner), or learn a component (world representation/costmap, planner parameters). Beyond classical: terrain-based and social navigation. Best practice found: learning at the component or subsystem level, with classical parts for safety and explainability (Xiao §6.2).
- Zhu & Zhang scenarios: local obstacle avoidance, indoor navigation, multi-robot, social.
- Embodied tasks (Duan §III, Sun): visual exploration, PointNav/ObjectNav/ImageNav, embodied question answering; ObjectNav methods are end-to-end, modular (semantic map + policy + planner) or zero-shot.
- Language (Gu VLN §2-4): instruction, oracle and dialogue tasks; methods by representation learning, action strategy (RL, exploration, planning, asking for help), data-centric learning, prior exploration.
- Social (Mavrogiannis §3-5): decoupled prediction-then-planning vs coupled; behaviour (proxemics, intentions, groups); evaluation metrics and methods.
- Benchmarks: Habitat, Gibson/Matterport scenes, R2R (VLN), SPL/success metrics, CrowdNav-style crowd simulators.

**C. Learned legged locomotion (Ha §2-8).**
- Algorithms: deep RL, behaviour cloning/imitation, combined with model-based control.
- MDP parts: dynamics (sim or real), observations (proprioception, exteroception), rewards, actions (joint targets or structured, e.g. CPG).
- Training frameworks: end-to-end, curriculum, hierarchical, privileged.
- Sim-to-real: system design, system identification, domain randomization, domain adaptation.
- Control + learning: model inside the policy structure, or a learned high-level policy over a model-based controller.
- Open problems: unsupervised skill discovery, differentiable simulators, hard terrain, safety, wheeled-legged, loco-manipulation, foundation models.

**D. Manipulation and imitation learning.**
- Demonstration source (Ravichandar §2): kinesthetic teaching, teleoperation, passive observation.
- Learning outcome (Ravichandar §3): policies (input, output space, policy class), cost/reward (trajectory optimisation, inverse RL), plans.
- Algorithm families (Zare §II-V): behaviour cloning, inverse RL, adversarial imitation, imitation from observation; challenges: imperfect demos, domain gaps.
- Manipulation structure (Kroemer §4-8): object representations, transition models, skill policies (action spaces, RL, IL, transfer, safety), pre/postconditions, hierarchical task structure.
- Generative policies (Wolf §4): diffusion for trajectory generation (IL and offline RL), grasp generation, visual data augmentation; benchmarks RLBench, CALVIN, Meta-World, LIBERO.
- Tang §4.3 competencies: grasping, pick-and-place, contact-rich (assembly, articulated, deformable), in-hand, non-prehensile.

**E. Humanoids.**
- Gu §III-VIII: tactile sensing, multi-contact planning, MPC (simplified, whole-body, mixed models), whole-body control (closed form, optimisation), learned loco-manipulation skills (RL from scratch, imitation from robot data, imitation from human data, hybrid), humanoid foundation models.
- Yuan §III: behaviour foundation models pre-trained by goal-conditioned tracking, intrinsic rewards or forward-backward representations, then adapted.

**F. Sim-to-real.**
- Zhao §III: zero-shot transfer, system identification, domain randomization, domain adaptation, learning with disturbances, simulators; related ideas: distillation, meta-RL, robust RL.
- Muratore §3-6: building stochastic simulators, measuring the reality gap, curriculum, meta-learning, transfer, distillation, distributional robustness, system identification, adaptive control, simulation-based inference; DR as static, adaptive or adversarial.

**G. Safe RL.**
- García §3-4: change the optimisation goal (worst-case, risk-sensitive, constrained) or change exploration (external knowledge, risk-directed exploration).
- Brunke §3: learn uncertain dynamics to improve safely (adaptive, robust, learning MPC, safe model-based RL), encourage safety in RL (safe exploration, risk-averse, constrained, robust MDPs), certify learned control (Lyapunov stability, control barrier functions, safety filters).
- Gu §3, §6: policy-optimisation, control-theory, formal-methods and Gaussian-process families; safe multi-agent RL; benchmarks Safety Gym, Safety-Gymnasium, safe-control-gym.

**H. Robot foundation models.**
- Firoozi §III-IV: robot policies (transformers), language-image goal-conditioned value learning, LLM task planning, in-context learning, open-vocabulary navigation/manipulation; perception (open-vocabulary detection, segmentation, 3D scene representations, affordances, predictive models).
- Ma §III-V: VLA components, low-level control policies, task planners (monolithic vs modular), datasets and benchmarks.
- Kawaharazuka §IV-VI: architectures (sensorimotor, world model, affordance-based), training (supervised, self-supervised, RL, stages, inference), data collection and datasets.
- Open problems: data scarcity, real-time inference, embodiment transfer, uncertainty, safety, evaluation.

## 2. Topic-by-topic table

### A. RL for robots in general

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| RS-001 | Kober §3; Ibarz §1 | Why robot RL is hard: high dimensions, costly real samples, model errors, goal specification | robotics | covered | 78 |
| RS-002 | Kober §2.2 | Value-function methods vs policy search | robotics | covered | 10, 35-38 |
| RS-003 | Kober §2.2.2 | Black-box policy search: perturb parameters, keep what scores well (finite differences, evolution strategies, CMA-ES, reward-weighted averaging) | robotics | partial | 153 has the cross-entropy method as a maths aside; new: searching policy parameters with no gradient, a standard robot baseline |
| RS-004 | Kober §4.3; Ravichandar §3.1.3 | Movement primitives: a trajectory as a spring-damper system plus a learned shape (DMP, ProMP) | robotics | new | A compact policy class learned from one demo, then tuned by RL |
| RS-005 | Kober §6; Ibarz §4.2.1, §4.6 | Model-based RL for robots: learn the dynamics, plan with it (random shooting / CEM with a learned model), guard against the policy exploiting model errors | robotics | partial | 135 Dyna, 142 world models; new: learned dynamics plus sampling-based planning, model ensembles, model exploitation |
| RS-006 | Ibarz §4.3.3; Zhao §III-D | Visual domain adaptation: make sim and real images look alike, or share features | vision | partial | 82 randomizes; new: translate real images toward sim (or the reverse) with an image-to-image network |
| RS-007 | Ibarz §4.4 | Bootstrapping RL with demonstrations: demos in the replay buffer, BC term in the loss | robotics | partial | 181 uses demos; new: the general recipe (e.g. DDPG from demonstrations) |
| RS-008 | Ibarz §4.7, §4.12; Tang §5 | Learning on real robots for days: automatic resets, reset-free learning, a changing world | robotics | new | How to keep a real robot collecting data without a human resetting it |
| RS-009 | Ibarz §4.8 | Delays and control rate: the robot keeps moving while the policy thinks | robotics | new | Observation and action latency, how to model it in sim and in the state |
| RS-010 | Ibarz §4.9 | Rewards from success classifiers and goal images | robotics | partial | 183 learns rewards from preferences (optional chapter); new: a classifier that says "task done" from camera images |
| RS-011 | Ibarz §4.10; Zhao §II-E; Muratore §4.2 | Multi-task and meta-RL: learn to adapt fast to a new task | robotics | new | Train over many tasks so a few trials suffice on a new one |
| RS-012 | Tang §3.1 | Map of robot competencies: locomotion, navigation, manipulation, mobile manipulation, HRI, multi-robot | robotics | partial | 78; new: the competency map as an orientation section |
| RS-013 | Tang §3.2-3.3 | Formulation and solution axes: action level, observation type, reward density; sim use, expert data, on/off-policy/offline optimiser | robotics | covered | 80, 85-88, 112, 81-84, 100, 45-48, 175 |
| RS-014 | Tang §3.4, §5 | Judging real-world success: lab vs diverse real settings; reproducible real benchmarks | robotics | partial | 115 for navigation; new: a general real-world evaluation ladder |
| RS-015 | Tang §4.4 | Mobile manipulation: arm on a moving base; whole-body control by RL | robotics | new | One policy for base and arm; short- vs long-horizon tasks |
| RS-016 | Tang §4.5 | Human-robot interaction: shared autonomy and physical HRI | robotics | new | Robot blends its action with a human's; robot works in contact with people |
| RS-017 | Tang §4.6; Gu safe §3.3 | Multi-robot RL: decentralised agents, centralised training (CTDE, MAPPO) | robotics | partial | 128-129 shared crowd policies; new: centralised critic, decentralised actors |
| RS-018 | Tang §5; Kroemer §8 | Long-horizon tasks by composing skills (hierarchical RL) | robotics | partial | 119 options; new: a high-level policy choosing among learned low-level skills |
| RS-019 | Ha §8.1; Tang §5 | Unsupervised skill discovery: learn many distinct skills with no task reward (DIAYN) | robotics | new | Reward = how well the skill can be told apart from its states |
| RS-020 | Tang §5 | Offline pretraining, then online fine-tuning | robotics | partial | 175-176, 181; new: why fine-tuning a value-based offline policy can collapse |
| RS-021 | Tang §4.1.3 | RL for quadrotor flight control | robotics | partial | 134 agile flight; new: low-level thrust/attitude control by RL |
| RS-022 | Tang §4.3.2 | Contact-rich manipulation: insertion and assembly with force and impedance control | control | new | Policy outputs stiffness or force, not just positions |
| RS-023 | Tang §4.3.2-4.3.4 | Object types: articulated (doors, drawers), deformable (cloth), non-prehensile (pushing) | robotics | new | Short overview of what changes for each object type |

### B. Learning-based navigation

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| RS-024 | Xiao §2 | Classical stack: global planner + local planner | robotics | covered | 106, 107, 15 |
| RS-025 | Xiao §3.1; Zhu & Zhang | Learning the whole stack end to end (mapless) | robotics | covered | 110 |
| RS-026 | Xiao §3.2.2 | Learning only the local planner | robotics | covered | 108 |
| RS-027 | Xiao §3.2.1 | Learning the global planner: learned heuristics, planning as a network (value iteration networks, neural A*) | robotics | new | A differentiable planner trained from data |
| RS-028 | Xiao §3.3.1 | Learned costmaps from demonstrations (inverse RL for navigation) | robotics | new | Learn what the robot should avoid from how people drive it; needs D-row inverse RL |
| RS-029 | Xiao §3.3.2, §6.2 | Learning planner parameters (tune DWA/TEB settings from demos or RL) | robotics | new | Xiao's "best current practice": keep the classical planner, learn its knobs |
| RS-030 | Xiao §6.2 | Hybrid learned-plus-classical systems for safety and explainability | robotics | covered | 108, 121 |
| RS-031 | Xiao §4.2.1; Tang §4.2.1 | Terrain-aware and off-road navigation: learn traversability from experience | robotics | partial | 131 self-supervised (BADGR), 86; new: traversability costmaps for wheeled off-road |
| RS-032 | Zhu & Zhang; Tang §4.6.1 | Multi-robot and crowd navigation with RL | robotics | covered | 128, 129 |
| RS-033 | Mavrogiannis §3.1 | Human trajectory prediction for planning: constant velocity, social force model, learned predictors | robotics | new | Predict where people go, then plan around the prediction |
| RS-034 | Mavrogiannis §3.2 | Coupled prediction and planning (the robot's move changes theirs) | robotics | partial | 128 learns this implicitly; new: the decoupled-vs-coupled distinction and the "freezing robot" problem |
| RS-035 | Mavrogiannis §4; Singamaneni | Social norms: personal space (proxemics), legibility, groups | robotics | new | What "polite" motion means and how to encode it |
| RS-036 | Mavrogiannis §5 | Evaluating social navigation: metrics and protocols | robotics | partial | 115; new: comfort and disturbance metrics, human studies |
| RS-037 | Duan §III-A | Visual exploration: cover a new house fast (coverage, curiosity, novelty rewards) | robotics | partial | 116-117 info gain; new: learned exploration policies with intrinsic rewards |
| RS-038 | Duan §III-B; Tang §4.2.1 | Embodied goal types: PointNav, ImageNav, ObjectNav | robotics | partial | 109, 115 (PointNav); new: image and object goals |
| RS-039 | Sun (ObjectNav) | Object-goal navigation by a semantic map + exploration policy (modular) | robotics | new | Build a map of object categories, choose where to look next |
| RS-040 | Sun (ObjectNav); Firoozi §III-F | Zero-shot, open-vocabulary navigation with vision-language models | robotics | new | "Find the red chair" with no task-specific training |
| RS-041 | Gu VLN §2-3 | Vision-and-language navigation: task, R2R dataset, metrics | robotics | new | Follow a spoken route through a building |
| RS-042 | Gu VLN §4 | VLN methods: cross-modal attention, graph memory, data augmentation (speaker-follower) | robotics | new | How instruction and view are matched step by step |
| RS-043 | Gu VLN §4.1.3; Firoozi §III-F | Topological maps: navigate over a graph of places | robotics | partial | 180 (ViNT) uses one; new: the graph map itself |
| RS-044 | Duan §II | Embodied AI simulators: Habitat, iGibson, AI2-THOR | robotics | covered | 107, 130 |
| RS-045 | Tang §4.2.2-4.2.3 | Legged and aerial navigation | robotics | covered | 147, 134 |

### C. Learned legged locomotion

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| RS-046 | Ha §2.2 | Deep RL for locomotion (PPO recipe) | robotics | covered | 143 |
| RS-047 | Ha §3.1-3.4 | Locomotion MDP parts: sim or real dynamics, proprio/extero observations, reward terms, PD joint targets | robotics | covered | 81, 84, 85, 86, 88, 90, 80 |
| RS-048 | Ha §3.4 | Structured action spaces: central pattern generators, foot-trajectory generators | robotics | partial | 80; new: policy modulates a rhythmic oscillator |
| RS-049 | Ha §4 | Curriculum, hierarchical, privileged training | robotics | covered | 92, 147, 98-101 |
| RS-050 | Ha §5.2-5.4 | System ID, domain randomization, domain adaptation | robotics | covered | 83, 82, 102 |
| RS-051 | Ha §2.3 | Imitation for locomotion (animal or human motion) | robotics | covered | 148 |
| RS-052 | Ha §6.1 | Learning inside a model-based controller (learned corrections to MPC) | control | partial | 146, 154; new: learned residual on an MPC output |
| RS-053 | Ha §6.2 | Learned high-level policy over a model-based low level (choose footholds or gait, MPC executes) | control | new | Needs MPC (shared with the classical-control gap scope) |
| RS-054 | Ha §7; Tang §4.1.2 | From quadrupeds to bipeds: gait clocks, periodic rewards, biped sim-to-real | robotics | partial | 149-150 start from imitation; new: plain-RL biped walking |
| RS-055 | Ha §8.2 | Differentiable simulators: gradients through physics | robotics | new | Optional; open problem, beginner overview only |
| RS-056 | Ha §8.3 | Hard terrain and parkour | robotics | covered | 144, 145 |
| RS-057 | Ha §8.4 | Safe locomotion and safety filters | robotics | covered | 127, 133 |
| RS-058 | Ha §8.5 | Wheeled-legged robots | robotics | covered | 147 |
| RS-059 | Ha §8.6; Gu hum §VII-F | Loco-manipulation: walk and use arms (or a leg) together | robotics | new | Whole-body policies for legged robots that also manipulate |

### D. Manipulation and imitation learning

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| RS-060 | Ravichandar §2 | Collecting demonstrations: kinesthetic teaching, teleoperation (VR, leader-follower arms), passive observation | robotics | new | Where demo data comes from and how its quality limits the policy |
| RS-061 | Zare §II | Behaviour cloning and compounding error | robotics | covered | 100 |
| RS-062 | Ravichandar §3.1.2; Kroemer §6.1 | Manipulation action spaces: joint, end-effector delta pose, impedance | control | new | Needs Jacobians/inverse kinematics (shared with classical-control gap scope) |
| RS-063 | Wolf §2.3, §4.1.1 | Why plain BC fails on multimodal demos (averaging two good paths gives a bad one) | robotics | new | The problem that diffusion and chunking policies solve |
| RS-064 | Wolf §4.1.1; Ma §III-B | Diffusion policy: denoise a short action sequence step by step | robotics | new | Chi et al. 2023 style policy; needs new DL diffusion |
| RS-065 | Kawaharazuka §IV-A; Ma §III-B | Action chunking (ACT): predict k actions at once, blend overlapping chunks | robotics | new | Fewer decisions per task, smoother motion; uses a conditional VAE |
| RS-066 | Ravichandar §3.2.2; Zare §III | Inverse RL: recover the reward from demos (max-entropy IRL) | robotics | new | Mentioned only as a word in 89; needs its own Note |
| RS-067 | Zare §IV | Adversarial imitation (GAIL): a discriminator gives the reward | robotics | partial | 148 AMP uses a discriminator for style; new: GAIL as the general method |
| RS-068 | Zare §V | Imitation from observation: learn from state-only or video demos | robotics | partial | 157 human videos; new: inferring missing actions (inverse dynamics) |
| RS-069 | Zare §VI-B; Kawaharazuka §II-B | Embodiment gap: human hand vs robot gripper, retargeting | robotics | partial | 157, 149; new: general cross-embodiment problem |
| RS-070 | Ravichandar §3.1.3 | Gaussian mixture regression as a policy | robotics | new | Optional; builds directly on MA-073 |
| RS-071 | Ravichandar §3.3; Kroemer §7-8 | Learning task structure: segment demos into skills, pre- and postconditions | robotics | new | Optional; link to hierarchical skills |
| RS-072 | Tang §4.3.1.1; Wolf §4.2 | 6-DoF grasp pose prediction from point clouds | vision | partial | 153 learns grasps from images; new: grasp poses in 3D, generated or scored |
| RS-073 | Kroemer §5 | Learned transition models for manipulation (predict object motion) | robotics | partial | 142; new: object-centric forward models for pushing |
| RS-074 | Tang §4.3.3 | In-hand dexterity | robotics | covered | 155, 156 |
| RS-075 | Ibarz §3.2; Tang §4.3.1 | Grasping at scale with RL | robotics | covered | 153 |
| RS-076 | Tang §4.3, §5 | Residual RL on a base controller; goal relabelling for sparse rewards | robotics | covered | 154, 93 |
| RS-077 | Wolf §5; Ma §V | Manipulation benchmarks and datasets: robosuite, RLBench, Meta-World, CALVIN, LIBERO, robomimic | robotics | new | One reference Note: what each tests |

### E. Humanoids

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| RS-078 | Gu hum §VII-A | RL from scratch for humanoid skills | robotics | covered | 143, 150 |
| RS-079 | Gu hum §VII-C | Imitation from human motion data | robotics | covered | 148, 149 |
| RS-080 | Gu hum §VII-C | Motion retargeting: map human mocap onto a robot skeleton | robotics | new | The step before any human-motion tracking; uses IK |
| RS-081 | Gu hum §VII-B | Imitation from robot teleoperation data | robotics | partial | 149 (teleop systems); new: whole-body teleop data for policy learning |
| RS-082 | Gu hum §V | MPC with simplified models (inverted pendulum, centroidal) | control | new | Classical baseline the surveys compare against; shared with control gap scope |
| RS-083 | Gu hum §VI | Whole-body control as a QP with task priorities | control | new | Builds on MA-068; shared with control gap scope |
| RS-084 | Gu hum §IX-A | Model-based vs learning-based control: when each wins | control | partial | 78, 108; new: humanoid-specific comparison |
| RS-085 | Gu hum §III | Tactile sensing on hands, feet and body | robotics | new | Optional overview |
| RS-086 | Gu hum §IV | Multi-contact planning (where to place hands and feet) | control | new | Optional overview |
| RS-087 | Yuan §III | Behaviour foundation models: one controller for any motion or goal, prompted at run time | robotics | partial | 150 multi-skill (HOVER); new: pre-train once, adapt by prompt |
| RS-088 | Gu hum §VIII | Humanoid foundation models | robotics | covered | 178 |

### F. Sim-to-real

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| RS-089 | Zhao §III-A, §III-C, §III-E; Muratore §5.1 | Zero-shot transfer with domain randomization and pushes | robotics | covered | 82 |
| RS-090 | Zhao §III-B; Muratore §4.6 | System identification | robotics | covered | 83 |
| RS-091 | Muratore §5.2 | Adaptive domain randomization (tune ranges from results) | robotics | covered | 92 |
| RS-092 | Muratore §5.3; García §3.1; Brunke §3.2.4 | Robust RL: train against the worst case or an adversary (robust MDP, RARL, adversarial DR) | robotics | new | One Note for worst-case training, used by sim-to-real and safety |
| RS-093 | Muratore §3.4 | Measuring the reality gap | robotics | partial | 84; new: estimating how far sim results predict real ones |
| RS-094 | Muratore §4.8 | Simulation-based inference: fit a distribution over sim parameters to real data | robotics | new | Optional; builds on 83 |
| RS-095 | Zhao §II-D | Distillation into a deployable student | robotics | covered | 101 |
| RS-096 | Muratore §4.7; Ha §5.4 | Online adaptation | robotics | covered | 102, 104 |
| RS-097 | Zhao §III-F | Simulators for robot learning | robotics | covered | 81 |

### G. Safe RL

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| RS-098 | García §3.3; Gu safe §3.1.1 | Constrained MDPs, Lagrangian and CPO | robotics | covered | 122-124 |
| RS-099 | García §3.2; Brunke §3.2.2 | Risk-sensitive RL: care about bad outcomes, not just the average (variance, CVaR) | robotics | new | Needs the spread of returns; builds on MA-008 percentiles |
| RS-100 | García §4.1 | Safe exploration with outside knowledge: demos, teacher advice | robotics | partial | 127 recovery, 181 human corrections; new: advice-taking as a family |
| RS-101 | Brunke §3.1, §3.2.1; Gu safe §3.1.4 | Safe exploration with an uncertainty model (Gaussian process, SafeOpt, learning MPC) | control | new | Optional; explore only where the model is confident it is safe |
| RS-102 | Brunke §3.3.1 | Stability certificates with Lyapunov functions | control | partial | New MA "Stability of dynamical systems" is planned; new: using it to certify a learned controller |
| RS-103 | Brunke §3.3.2; Gu safe §3.1.2 | Control barrier functions and safety filters (QP that minimally edits the action) | control | partial | 124 barriers, 127 filters; new: the CBF-QP filter step by step, reach-avoid sets |
| RS-104 | Gu safe §3.1.3 | Formal methods and shields | robotics | covered | 127 |
| RS-105 | Gu safe §6; Brunke §4 | Safe RL benchmarks: Safety Gym, Safety-Gymnasium, safe-control-gym | robotics | covered | 125 |

### H. Robot foundation models

| ID | Source section | Concept | Kind | Status | Our Note / what is new |
|---|---|---|---|---|---|
| RS-106 | Firoozi §III-A, §III-E; Ma §III | Robot transformers and VLAs | robotics | covered | 178 |
| RS-107 | Kawaharazuka §IV-A | Action heads: discrete action tokens vs diffusion/flow heads | robotics | partial | 178, 179; new: how continuous actions become tokens (binning, compression) |
| RS-108 | Kawaharazuka §VI; Ma §V-A | Cross-embodiment datasets (Open X-Embodiment, DROID, BridgeData) and training across robots | robotics | partial | 178; new: aligning different action spaces and data mixing |
| RS-109 | Firoozi §II-D | Vision-language models (CLIP-style image-text matching) | vision | partial | DL-071 transformers, planned new DL contrastive Note; new: image-text contrastive pretraining |
| RS-110 | Firoozi §III-B | Pretrained visual representations for robots (from human video, goal-conditioned values) | vision | new | Frozen image encoders trained for control |
| RS-111 | Firoozi §III-C; Ma §IV | LLM task planning: monolithic vs modular (affordance-scored plans, code as policies) | robotics | new | A language model breaks a task into skills the robot can run |
| RS-112 | Firoozi §IV-C | Open-vocabulary 3D semantic maps (language-queryable maps) | vision | new | Shared by ObjectNav and manipulation |
| RS-113 | Firoozi §IV-D; Kawaharazuka §IV-C | Affordance-based models: where and how to act on an object | robotics | new | Value maps from VLMs that a planner then uses |
| RS-114 | Firoozi §IV-E; Kawaharazuka §IV-B | Video and world models as policies (predict the future frame, then act) | robotics | partial | 142; new: video-prediction policies |
| RS-115 | Firoozi §III-D | In-context learning for decisions | robotics | covered | 104 |
| RS-116 | Ma §IV; Kawaharazuka §V-D | Hierarchical VLA: slow planner + fast controller | robotics | partial | 178; new: the two-speed split |
| RS-117 | Kawaharazuka §V-C, §IX-D | RL fine-tuning of generalist policies | robotics | covered | 182 |
| RS-118 | Firoozi §III-C | LLM-written rewards | robotics | covered | 95 |
| RS-119 | Firoozi §VI-D | Uncertainty and asking for help (conformal prediction) | robotics | new | Optional; robot knows when it does not know |
| RS-120 | Tang §5 | Navigation foundation models | robotics | covered | 180 |

## 3. Over-representation: robotics.md Notes on topics the surveys treat as minor

Counts are mentions in the 17 survey texts read in full (Tang, Ibarz, Kober, Xiao, Ha, Gu humanoid, Zhao, Muratore, Brunke, Gu safe, Kroemer, Ravichandar, Zare, Firoozi, Kawaharazuka, Mavrogiannis, Gu VLN), by text search.

| Note(s) | Topic | Survey evidence | Suggestion |
|---|---|---|---|
| 139 | Games: minimax, alpha-beta, equilibria | 0 mentions in 16 of 17 surveys; Gu safe RL uses "minimax" only for sample-complexity bounds | Move to optional |
| 140, 141 | Self-play, AlphaZero, MuZero | 0 in 16 of 17; Gu safe RL names MuZero once, for video compression | Merge into one optional Note |
| 138 | Monte Carlo tree search | 1 mention each in Gu humanoid and Gu safe RL | Keep short or optional |
| 31, 34 | LSTD, nonparametric values, Bellman error geometry, gradient-TD | 0 mentions of LSTD/GTD in all 17 | Move to optional |
| 28 | Eligibility traces and TD(lambda) | 1 mention (Kober); robot RL uses GAE (Note 40) instead | Shorten; keep what GAE needs |
| 32 | Average-reward setting | 7 mentions in Kober (2013), 1 in Ibarz, 0 in Tang and Ha | Keep as a short section |
| 177 | Decision Transformer | 1 mention (Tang) | Shorten or optional |
| 7 | Decisions against nature (LaValle) | not a survey family; LaValle framing only | Fold into Note 8 |
| 183-188 | RL for language models | not a robotics topic in any survey | Already optional; keep so |

The surveys give the opposite weight to imitation learning: Zare uses "inverse RL" 84 times, Ravichandar 26, Kroemer 36; diffusion appears 89 times in Wolf. robotics.md has no Note for inverse RL or diffusion policy.

## 4. Prerequisites between the new concepts

- Collecting demonstrations → multimodal demos problem → diffusion policy; → action chunking (ACT).
- Inverse RL → learned costmaps for navigation; → GAIL (adversarial imitation).
- Black-box policy search → movement primitives (tuned by black-box search) → Gaussian mixture regression (optional).
- Model-based RL with learned dynamics → bootstrapping RL with demos → real-world learning with resets → contact-rich manipulation.
- Robust RL → risk-sensitive RL → safe exploration with uncertainty models (optional).
- Lyapunov certificates → control barrier functions and safety filters (completes 124, 127).
- Human trajectory prediction → coupled prediction and planning → social norms → social evaluation.
- Embodied goal types → semantic-map ObjectNav → open-vocabulary 3D maps → zero-shot ObjectNav; VLN task → VLN methods; topological maps feed VLN and 180.
- Vision-language models → pretrained visual representations → LLM task planning → affordance models → hierarchical VLA.
- Manipulation action spaces → contact-rich manipulation; → mobile manipulation → loco-manipulation.
- MPC with simplified models → learned high-level policy over MPC; whole-body control QP → loco-manipulation.
- Motion retargeting → behaviour foundation models.
- Multi-task/meta-RL → (links to 102, 104 adaptation).
- Hierarchical skills → unsupervised skill discovery.

## 5. Suggested learning order (where new Notes slot into robotics.md)

1. After RO-07: black-box policy search; model-based RL with learned dynamics.
2. RO-12/13: competency map (into 78), delays and control rate, robust RL, multi-task/meta-RL, rewards from success classifiers.
3. RO-14, right after 100 (BC): collecting demonstrations, multimodal demos, inverse RL, GAIL. This gives the primary-interest navigation chapters inverse RL before RO-15.
4. RO-15/16 (navigation): learned costmaps, planner-parameter learning, learned global planners, terrain traversability, visual exploration with intrinsic rewards, embodied goal types, semantic-map ObjectNav, topological maps.
5. RO-17 (safety): risk-sensitive RL, Lyapunov certificates, CBF safety filters, advice-taking.
6. RO-18 (navigation III): trajectory prediction, coupled planning, social norms, social evaluation, multi-robot CTDE.
7. RO-20 (legged/humanoid): structured action spaces (CPG), biped RL, MPC baselines and learned high-level over MPC, WBC QP, motion retargeting, loco-manipulation, behaviour foundation models.
8. RO-21 (manipulation): manipulation action spaces, diffusion policy, ACT, contact-rich, object types, 6-DoF grasps, movement primitives, benchmarks; mobile manipulation and HRI at the end.
9. RO-24 (foundation models): VLMs, pretrained visual representations, open-vocabulary 3D maps, zero-shot ObjectNav, VLN, LLM planning, affordances, action heads, cross-embodiment data, hierarchical VLA, video policies.
10. Optional depth: differentiable simulators, simulation-based inference, GMR, task structure learning, tactile sensing, contact planning, safe exploration with GPs, uncertainty/asking for help, real-world reset-free learning.

## 6. New maths and DL the area needs that MA/ML/DL lack

| Concept | Why | Home | First needed by |
|---|---|---|---|
| Generative adversarial networks | GAIL; image translation for visual domain adaptation | new DL "Generative models for control" chapter (already planned for VAE, diffusion, flow) | GAIL |
| Conditional VAE | ACT encodes the style of a demo | extend planned DL VAE Note | Action chunking (ACT) |
| Mutual information | Skill discovery rewards; VLA/representation objectives | MA 08-likelihood, after the planned KL divergence Note | Unsupervised skill discovery |
| Gaussian processes (regression with uncertainty) | Safe exploration, sim-based inference, PILCO-style model-based RL | ML new Note (none exists; MA-073 has mixtures only) | Safe exploration with an uncertainty model |
| Spring-damper (second-order) systems | Movement primitives and impedance control | short section in the movement-primitives Note (physics, like the mechanics aside in Note 56) | Movement primitives |
| Conditional value at risk (tail average) | Risk-sensitive RL | short section; builds on MA-008 percentiles | Risk-sensitive RL |
| Image-text contrastive pretraining (CLIP) | VLMs, open-vocabulary maps, zero-shot navigation | extends the planned DL contrastive-loss Note | Vision-language models |

Already planned in robotics.md §3 and reused here: KL divergence, diffusion, flow matching, VAE, contrastive loss, stability of dynamical systems (Lyapunov). Quadratic programming (for CBF filters and WBC) is MA-068; Gaussian mixtures are MA-073.
