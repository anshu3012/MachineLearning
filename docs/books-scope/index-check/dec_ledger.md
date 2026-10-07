# dec ledger: index-based completeness check

Agent `dec`. Verdicts follow BRIEF.md. `taught` cites a Note whose robotics.md title/Teaches (or MA/ML/DL body) lists the concept;
rows marked [hand-checked] failed the literal script check only because of wording (British/US spelling, synonym, or a named part of a listed concept) and were confirmed by reading.
`mentioned-only` rows are treated as `add` (they are in dec_adds.json).

## Sutton & Barto, Reinforcement Learning: An Introduction, 2nd ed. (2020 PDF)

Source: http://incompleteideas.net/book/RLbook2020.pdf. Index: PDF pp. 541-546 (book pp. 519-524). Terms: 529. add 12, index-noise 41, out-of-scope 100, taught 376

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| k-armed bandits | 25–45 | taught | RL #2 Multi-armed bandits and epsilon-greedy |
| absorbing state | 57 | add | absorbing terminal state (one notation for episodic and continuing tasks) [RL] -> RL-02, short section in Note #8 Return and discounting. S&B §3.4 and DM appendix F use it; Note #8 lists episodes and continuing tasks but not the absorbing state that unifies them |
| access-control queuing example | 256 | out-of-scope | book-specific worked example (S&B §10.3); the concept, average-reward control, is RL #27 |
| action preferences | 322, 329, 336, 455 | taught | RL #5 Gradient bandits; RL #29 Parameterised policies |
| action preferences, in bandit problems | 37, 42 | taught | RL #5 Gradient bandits [hand-checked] |
| action-value function | see value function, action | index-noise | cross-reference to "value function, action" |
| action-value methods | 321 | taught | RL #2 (sample-average action values); RL #29 (value methods vs policy search) |
| action-value methods, for bandit problems | 27 | taught | RL #2 Multi-armed bandits and epsilon-greedy [hand-checked] |
| actor–critic | 21, 239, 321, 331–332, 338, 406 | taught | RL #32 Actor-critic |
| actor–critic, advantage, A2C | 338 | taught | RL #37 Parallel advantage actor-critic (A2C/A3C) |
| actor–critic, one-step (episodic) | 332 | taught | RL #32 Actor-critic |
| actor–critic, with eligibility traces (episodic) | 332 | taught | RL #32 Actor-critic (S&B §13.5 boxed algorithm, row SB13.7); traces from RL #24 [hand-checked] |
| actor–critic, with eligibility traces (continuing) | 333 | taught | RL #32 Actor-critic (continuing case, S&B §13.6, row SB13.8) |
| actor–critic, neural | 395–415 | out-of-scope | neuroscience (S&B ch.15); dropped in robotics.md §7 (SB15.x) |
| addiction | 409–410 | out-of-scope | neuroscience (S&B §15.11); dropped in robotics.md §7 (SB15.x) |
| afterstates | 137, 140, 181, 182, 191, 424, 430 | taught | RL #19 TD(0) prediction (afterstates) |
| agent–environment interface | 47–58, 466 | taught | RL #7 Markov decision processes |
| all-actions algorithm | 326 | out-of-scope | exercise-only variant of the policy-gradient update (S&B Ex. 13.x, p.326); REINFORCE itself is RL #30 |
| AlphaGo, AlphaGo Zero, AlphaZero | 441–450 | taught | RL #55 Self-play: from TD-Gammon to AlphaZero [hand-checked] |
| Andreae, John | 17, 21, 69, 89 | index-noise | person's name |
| ANN | see artificial neural networks | index-noise | cross-reference to "artificial neural networks" |
| applications and case studies | 421–457 | index-noise | chapter pointer (S&B ch.16) |
| approximate dynamic programming | 15 | taught | RL #25-#27 (DP-style updates with function approximation); RO #106 (DP with interpolation) |
| artificial intelligence | xvii, 1, 472, 478 | taught | ML-002 AI vs ML vs DL |
| artificial neural networks | 223–228, 238–240, 395–398, 423, 430, 436–450, 472 | taught | DL-010 forward propagation (whole network); recap in robotics.md §5 |
| associative reinforcement learning | 45, 418 | taught | RL #6 Contextual bandits (associative search) |
| associative search | 41 | taught | RL #6 Contextual bandits |
| asynchronous dynamic programming | 85, 88 | taught | RL #15 Asynchronous DP and generalized policy iteration |
| Atari video game play | 436–441 | taught | RL #35 Deep Q-networks (Atari) |
| auxiliary tasks | 460–461, 468, 474 | taught | RL #170 Auxiliary tasks and general value functions |
| average reward setting | 249–255, 258, 464 | taught | RL #27 Control with approximation and the average-reward setting |
| averagers | 264 | out-of-scope | convergence-theory condition (S&B §11.2 p.264: averagers are stable under DP); proof-level, no algorithm |
| backgammon | 11, 21, 182, 184, 421–426 | taught | RL #55 (TD-Gammon) |
| backpropagation | 21, 225–227, 239, 407, 424, 436, 439 | taught | DL-015/DL-016 backpropagation |
| backup diagram | 60, 139 | taught | RL #10 Bellman equations (backup diagrams) |
| backup diagram, for dynamic programming | 59, 61, 64, 172 | taught | RL #10, #12 (DP backups) [hand-checked] |
| backup diagram, for Monte Carlo methods | 94 | taught | RL #16 Monte Carlo prediction [hand-checked] |
| backup diagram, for Q-learning | 134 | taught | RL #21 Q-learning [hand-checked] |
| backup diagram, for TD(0) | 121 | taught | RL #19 TD(0) prediction [hand-checked] |
| backup diagram, for Sarsa | 129 | taught | RL #20 Sarsa and expected Sarsa [hand-checked] |
| backup diagram, for Expected Sarsa | 134 | taught | RL #20 Sarsa and expected Sarsa [hand-checked] |
| backup diagram, for Sarsa(λ) | 304 | taught | RL #24 Eligibility traces and TD(lambda) |
| backup diagram, for TD(λ) | 289 | taught | RL #24 Eligibility traces and TD(lambda) |
| backup diagram, for Q(λ) | 313 | taught | RL #24 (off-policy traces, Watkins's Q(λ)) [hand-checked] |
| backup diagram, for Tree Backup(λ) | 314 | taught | RL #24 (off-policy traces) |
| backup diagram, for Truncated TD(λ) | 296 | taught | RL #24 (truncated λ-return) [hand-checked] |
| backup diagram, for n-step Q(σ) | 155 | taught | RL #23 n-step bootstrapping (n-step Q(σ)) |
| backup diagram, for n-step Expected Sarsa | 146 | taught | RL #23 n-step bootstrapping [hand-checked] |
| backup diagram, for n-step Sarsa | 146 | taught | RL #23 n-step bootstrapping [hand-checked] |
| backup diagram, for n-step TD | 142 | taught | RL #23 n-step bootstrapping [hand-checked] |
| backup diagram, for n-step Tree Backup | 152 | taught | RL #23 n-step bootstrapping (tree-backup) |
| backup diagram, for Samuel’s Checker Player | 428 | taught | RL #55 (Samuel checkers) |
| backup diagram, compound | 288 | taught | RL #24 (λ-return as a compound update) [hand-checked] |
| backup diagram, half backups | 62 | taught | RL #10 Bellman equations (backup-diagram notation) [hand-checked] |
| backward view of eligibility traces | 288, 293 | taught | RL #24 (forward vs backward view) |
| Baird’s counterexample | 261–264, 280, 283, 285 | taught | RL #28 The deadly triad |
| bandit algorithm, simple | 32 | taught | RL #2 Multi-armed bandits and epsilon-greedy [hand-checked] |
| bandit problems | 25–45 | taught | RL #2 Multi-armed bandits and epsilon-greedy [hand-checked] |
| basal ganglia | 386 | out-of-scope | neuroscience (S&B ch.15); dropped in robotics.md §7 (SB15.x) |
| baseline | 37–40, 329, 330, 338 | taught | RL #5 Gradient bandits; RL #31 Baselines |
| behavior policy | 103, 110 | taught | RL #18 Off-policy learning with importance sampling [hand-checked] |
| Bellman equation | 14 | taught | RL #10 Bellman equations |
| Bellman equation, for v_π | 59 | taught | RL #10 Bellman equations [hand-checked] |
| Bellman equation, for q_π | 78 | taught | RL #10 Bellman equations [hand-checked] |
| Bellman equation, for optimal value functions: v_* and q_* | 63 | taught | RL #11 Optimal values and optimal policies |
| Bellman equation, differential | 250 | taught | RL #27 (differential values) |
| Bellman equation, for options | 463 | add | option models and planning with options (Bellman equation over options) [RL] -> RO-13, section in Note #184 Options: temporal abstraction. S&B §17.2; Note #184 lists only options as temporally extended actions |
| Bellman error | 268, 270, 272, 273 | taught | RL #52 Bellman error geometry and gradient-TD |
| Bellman error, learnability of | 274–278 | taught | RL #52 ("the Bellman error is not learnable") |
| Bellman error, vector | 267–269 | add | Bellman operator as a contraction: why value iteration converges [RL] -> RL-02, short section in Note #14 Value iteration. S&B §11.4 (Bellman operator) and DM §7.5 (contraction mapping); no Note lists either |
| Bellman operator | 267–269, 286 | add | Bellman operator as a contraction: why value iteration converges [RL] -> RL-02, short section in Note #14 Value iteration. S&B §11.4 (Bellman operator) and DM §7.5 (contraction mapping); no Note lists either |
| Bellman residual | 286 | index-noise | cross-reference to "Bellman error" |
| Bellman, Richard | 14, 71, 89, 241 | index-noise | person's name |
| binary features | 215, 222, 245, 304, 305 | taught | RL #26 Linear value functions and features (coarse/tile coding give binary features) [hand-checked] |
| bioreactor example | 51 | out-of-scope | book-specific worked example (S&B §3.1); MDP framing is RL #7 |
| blackjack example | 93–94, 99, 106 | out-of-scope | book-specific worked example (S&B §5.1); Monte Carlo prediction is RL #16 |
| blocking maze example | 166 | out-of-scope | book-specific worked example (S&B §8.3); Dyna-Q+ is RL #45 |
| bootstrapping | 89, 189, 308 | taught | RL #12 Policy evaluation (bootstrapping); RL #19 |
| bootstrapping, n-step | 141–158, 255 | taught | RL #23 n-step bootstrapping |
| bootstrapping, and dynamic programming | 89 | taught | RL #12 Policy evaluation [hand-checked] |
| bootstrapping, and function approximation | 208, 264–274 | taught | RL #28 The deadly triad [hand-checked] |
| bootstrapping, and Monte Carlo methods | 95 | taught | RL #19 TD(0) prediction (TD = sampling + bootstrapping) |
| bootstrapping, and stability | 263–265 | taught | RL #28 The deadly triad [hand-checked] |
| bootstrapping, and TD learning | 120 | taught | RL #19 TD(0) prediction |
| bootstrapping, assessment of | 124–128, 248, 264, 291, 318 | taught | RL #19, #23 (batch TD vs MC; choosing n) [hand-checked] |
| bootstrapping, in psychology | 345, 349, 354, 355 | out-of-scope | psychology (S&B ch.14); dropped in robotics.md §7 (SB14.x) |
| bootstrapping, parameter (λ or n) | 291, 307, 399 | taught | RL #23, #24 (n and λ) [hand-checked] |
| BOXES | 18, 71, 237 | out-of-scope | history: 1960s pole-balancing program (S&B §1.7) |
| branching factor | 173–177, 422 | taught | RL #46 (expected vs sample updates, branching factor b) [hand-checked] |
| breakfast example | 5, 22 | out-of-scope | book-specific illustration (S&B §1.2) |
| bucket-brigade algorithm | 19, 21, 139 | out-of-scope | history (S&B §1.7) |
| catastrophic interference | 472 | add | catastrophic forgetting (interference) [DL] -> RL-05 Note #36 Experience replay and target networks (short section). DM book indexes it too (catastrophic forgetting, p.345); it is the reason replay buffers exist, and it matters for fine-tuning robot policies |
| certainty-equivalence estimate | 128 | taught | RL #19 TD(0) prediction (certainty equivalence) |
| chess | 4, 20, 54, 182, 450 | out-of-scope | game example and history (S&B §1.7, §16) |
| classical conditioning | 20, 343–357 | out-of-scope | psychology (S&B ch.14); dropped in robotics.md §7 (SB14.x) |
| classical conditioning, blocking | 371 | out-of-scope | psychology (S&B ch.14); dropped in robotics.md §7 (SB14.x) |
| classical conditioning, blocking, and higher-order conditioning | 345–355 | out-of-scope | psychology (S&B ch.14); dropped in robotics.md §7 (SB14.x) |
| classical conditioning, delay and trace conditioning | 344 | out-of-scope | psychology (S&B ch.14); dropped in robotics.md §7 (SB14.x) |
| classical conditioning, Rescorla-Wagner model | 346–349 | out-of-scope | psychology (S&B ch.14); dropped in robotics.md §7 (SB14.x) |
| classical conditioning, TD model | 349–357 | out-of-scope | psychology (S&B ch.14); dropped in robotics.md §7 (SB14.x) |
| classifier systems | 19, 21 | out-of-scope | history (S&B §1.7) |
| cliff walking example | 132, 133 | out-of-scope | book-specific worked example (S&B §6.5); Sarsa vs Q-learning is RL #20-#21 |
| CMAC | see tile coding | index-noise | cross-reference to "tile coding" |
| coarse coding | 215–220, 238 | taught | RL #26 Linear value functions and features |
| cognitive maps | 363–364 | out-of-scope | psychology (S&B §14.5); dropped in robotics.md §7 (SB14.x) |
| collective reinforcement learning | 404–407 | out-of-scope | neuroscience (S&B §15.10); dropped in robotics.md §7 (SB15.x) |
| complex backups | see compound update | index-noise | cross-reference to "compound update" |
| compound stimulus | 345, 346–356, 371, 382 | out-of-scope | psychology (S&B ch.14); dropped in robotics.md §7 (SB14.x) |
| compound update/backup | 288, 319 | taught | RL #24 (λ-return as a compound update) [hand-checked] |
| conditioned/unconditioned stimulus, conditioned response (CS/US, CR) | 344 | out-of-scope | psychology (S&B ch.14); dropped in robotics.md §7 (SB14.x) |
| constant-α MC | 120 | taught | RL #19 TD(0) prediction (constant-α MC as the comparison) [hand-checked] |
| contextual bandits | 41 | taught | RL #6 Contextual bandits |
| continuing tasks | 54, 57, 70, 124, 249, 294 | taught | RL #8 Return and discounting |
| continuous action | 73, 244, 335–336 | taught | RL #33 Gaussian policies for continuous actions |
| continuous state | 73, 223, 238 | taught | RL #25 Value prediction as supervised learning [hand-checked] |
| continuous time | 11, 71 | taught | robotics.md §4 new MA "ODEs and vector fields"; RO #205 (Hamilton-Jacobi-Bellman) |
| control and prediction | 342 | taught | RL #12 (prediction) and RL #13 (control) [hand-checked] |
| control theory | 4, 71 | taught | RO-06 (#117-#125) and RO-15 (#201-#211) [hand-checked] |
| control variates | 150–152, 155, 281 | taught | RL #23, RL #31; robotics.md §4 "Control variates" |
| control variates, and eligibility traces | 309–312 | taught | RL #24 (off-policy traces with control variates) [hand-checked] |
| credit assignment | 11, 17, 19, 47, 294, 401 | taught | RL #8 Return and discounting (credit assignment) |
| credit assignment, in psychology | 346, 361 | out-of-scope | psychology (S&B ch.14); dropped in robotics.md §7 (SB14.x) |
| credit assignment, structural | 385, 405, 407 | out-of-scope | neuroscience (S&B §15.8-15.10); dropped in robotics.md §7 (SB15.x) |
| critic | 18, 239, 346, 417 | taught | RL #32 Actor-critic |
| cumulant | 459 | taught | RO #170 Auxiliary tasks and general value functions [hand-checked] |
| curiosity | 474 | taught | RO #182 Curiosity and intrinsic rewards |
| curse of dimensionality | 4, 14, 221, 231 | taught | ML-045 Curse of dimensionality; RL #15 |
| cybernetics | xvii, 477 | out-of-scope | history (S&B §1.7, p.477) |
| deadly triad | 264 | taught | RL #28 The deadly triad |
| deep learning | 12, 223, 441, 472–474, 479 | taught | DL-002 What is deep learning |
| deep reinforcement learning | 236 | taught | RL #35 Deep Q-networks (RL-05) [hand-checked] |
| deep residual learning | 227 | taught | DL-081 transformer encoder (residual connection, glossary G-1681); ResNet named in DL-051 |
| delayed reinforcement | 361–363 | out-of-scope | psychology (S&B §14.4); dropped in robotics.md §7 (SB14.x); delayed reward itself is RL #8 |
| delayed reward | 1, 47, 249 | taught | RL #8 Return and discounting |
| dimensions of reinforcement learning methods | 189–191 | index-noise | summary-section pointer (S&B §8.13) |
| direct and indirect RL | 162, 164, 192 | taught | RL #45 Models and Dyna (direct RL vs model learning) [hand-checked] |
| discounting | 55, 199, 243, 249, 282, 324, 328, 427, 459 | taught | RL #8 Return and discounting |
| discounting, in pole balancing | 56 | out-of-scope | book-specific worked example (S&B Ex. 3.x pole balancing) |
| discounting, state dependent | 307 | taught | RL #24 (variable λ and γ) |
| discounting, deprecated | 253, 256 | taught | RL #27 (why discounting breaks with approximation) |
| distribution models | 159, 185 | taught | RL #45 Models and Dyna |
| dopamine | 377, 381–387, 413–419 | out-of-scope | neuroscience (S&B ch.15); dropped in robotics.md §7 (SB15.x) |
| dopamine, and addiction | 409–410 | out-of-scope | neuroscience (S&B §15.11); dropped in robotics.md §7 (SB15.x) |
| double learning | 134–136, 140 | taught | RL #22 Double Q-learning |
| DP | see dynamic programming | index-noise | cross-reference to "dynamic programming" |
| driving-home example | 122–123 | out-of-scope | book-specific worked example (S&B §6.1); TD(0) is RL #19 |
| Dyna architecture | 164, 161–170 | taught | RL #45 Models and Dyna [hand-checked] |
| dynamic programming | 13–15, 73–90, 174, 262 | taught | RL-02 (#12-#15) [hand-checked] |
| dynamic programming, and artificial intelligence | 89 | out-of-scope | history (S&B §4.8 bibliographic remarks) |
| dynamic programming, and function approximation | 241 | taught | RO #106 (DP with interpolation); RL #25-#27 |
| dynamic programming, and options | 463 | add | option models and planning with options (Bellman equation over options) [RL] -> RO-13, section in Note #184 Options: temporal abstraction. S&B §17.2; Note #184 lists only options as temporally extended actions |
| dynamic programming, and the deadly triad | 264 | taught | RL #28 The deadly triad [hand-checked] |
| dynamic programming, computational efficiency of | 87 | taught | RL #15 (curse of dimensionality for DP) |
| eligibility traces | 287–320, 350, 362, 398–403 | taught | RL #24 Eligibility traces and TD(lambda) |
| eligibility traces, accumulating | 300, 306, 310 | taught | RL #24 Eligibility traces and TD(lambda) |
| eligibility traces, replacing | 301, 306 | taught | RL #24 Eligibility traces and TD(lambda) |
| eligibility traces, dutch | 300–303 | taught | RL #24 (true online TD(λ) uses dutch traces) |
| eligibility traces, contingent/non-contingent | 399–403, 411 | out-of-scope | neuroscience (S&B §15.8-15.9); dropped in robotics.md §7 (SB15.x) |
| eligibility traces, off-policy | 309–316 | taught | RL #24 (off-policy traces) |
| eligibility traces, with state-dependent λ and γ | 309–316 | taught | RL #24 (variable λ and γ) |
| Emphatic-TD methods | 234–235, 315 | taught | RL #52 (emphatic TD; optional) |
| Emphatic-TD methods, off-policy | 281–282 | taught | RL #52 (emphatic TD; optional) [hand-checked] |
| environment | 47–58 | taught | RL #7 Markov decision processes |
| episodes, episodic tasks | 11, 54–58, 91 | taught | RL #8 Return and discounting |
| error reduction property | 144, 288 | out-of-scope | proof device for n-step convergence (S&B §7.1, p.144) |
| evaluative feedback | 17, 25, 47 | add | evaluative vs instructive feedback [RL] -> RL-01, short section in Note #1 The reinforcement learning problem. S&B ch.2 opening; the core difference between RL and supervised learning; not in Note #1's list |
| evolution | 7, 359, 374, 471 | out-of-scope | biology context (S&B ch.14-15 and §1.6); evolutionary methods are a separate entry |
| evolutionary methods | 7, 8, 9, 11, 19 | taught | RL #1; RL #43 Black-box policy search |
| expected approximate value | 148, 155 | taught | RL #23 (expected approximate value in n-step expected Sarsa) [hand-checked] |
| Expected Sarsa | 133 | taught | RL #20 Sarsa and expected Sarsa |
| expected update | 75, 172–181, 189 | taught | RL #46 Prioritized sweeping (expected vs sample updates) |
| experience replay | 440–441 | taught | RL #36 Experience replay and target networks |
| explore/exploit dilemma | 3, 103, 472 | taught | RL #1 The reinforcement learning problem [hand-checked] |
| exploring starts | 96, 98–100, 178 | taught | RL #17 Monte Carlo control |
| feature construction | 210–223 | taught | RL #26 Linear value functions and features; ML-022 feature engineering |
| final time step (T ) | 54 | taught | RL #8 Return and discounting (episode end time T) [hand-checked] |
| Fourier basis | 211–215 | taught | RL #26; robotics.md §4 "Fourier basis features" |
| function approximation | 195–200 | taught | RL #25 Value prediction as supervised learning [hand-checked] |
| gambler’s example | 84 | out-of-scope | book-specific worked example (S&B §4.4); value iteration is RL #14 |
| game theory | 19 | taught | RL #54 Games: minimax, alpha-beta and equilibria (optional) [hand-checked] |
| gazelle calf example | 5 | out-of-scope | book-specific illustration (S&B §1.2) |
| general value functions (GVFs) | 459–463, 474 | taught | RO #170 Auxiliary tasks and general value functions |
| generalized policy iteration (GPI) | 86–87, 92, 97, 138, 189 | taught | RL #15 Asynchronous DP and generalized policy iteration |
| genetic algorithms | 19 | out-of-scope | history mention (S&B §1.7); population search is RL #43 |
| Gittins index | 43 | out-of-scope | Bayes-optimal bandit index; S&B §2.9 mentions it only and calls it intractable in general |
| gliding/soaring case study | 453–457 | out-of-scope | case study (S&B §16.8); dropped in robotics.md §7 (SB16.8) |
| goal | see reward signal | index-noise | cross-reference to "reward signal" |
| golf example | 61, 63, 66 | out-of-scope | book-specific worked example (S&B §3.5) |
| gradient | 201 | taught | MA-062 Partial derivatives and gradients |
| gradient descent | see stochastic gradient descent | index-noise | cross-reference to "stochastic gradient descent" |
| Gradient-TD methods | 278–281, 314–315 | taught | RL #52 Bellman error geometry and gradient-TD (optional) |
| greedy or ε-greedy |  | taught | RL #2 Multi-armed bandits and epsilon-greedy |
| greedy or ε-greedy, as exploiting | 26–28 | taught | RL #2 Multi-armed bandits and epsilon-greedy [hand-checked] |
| greedy or ε-greedy, as shortsighted | 64 | taught | RL #11 (greedy w.r.t. optimal values is optimal) |
| greedy or ε-greedy, ε-greedy policies | 100 | taught | RL #17 Monte Carlo control (epsilon-soft) |
| gridworld examples | 60, 65, 76, 147 | out-of-scope | book-specific worked examples (gridworlds, S&B §3.5) |
| gridworld examples, cliff walking | 132 | out-of-scope | book-specific worked example (S&B §6.5) |
| gridworld examples, Dyna blocking maze | 166 | out-of-scope | book-specific worked example (S&B §8.3) |
| gridworld examples, Dyna maze | 164 | out-of-scope | book-specific worked example (S&B §8.2) |
| gridworld examples, Dyna shortcut maze | 167 | out-of-scope | book-specific worked example (S&B §8.3) |
| gridworld examples, windy | 130, 131 | out-of-scope | book-specific worked example (S&B §6.4) |
| habitual and goal-directed control | 364–368 | taught | RL #45 (model-free habitual vs model-based goal-directed) |
| hedonistic neurons | 402–404 | out-of-scope | neuroscience (S&B §15.9); dropped in robotics.md §7 (SB15.x) |
| heuristic search | 181–183, 190 | taught | RL #47 Decision-time planning and rollouts |
| heuristic search, as sequences of backups | 183 | taught | RL #47 Decision-time planning and rollouts [hand-checked] |
| heuristic search, in Samuel’s checkers player | 426 | taught | RL #55 Self-play (Samuel checkers) |
| heuristic search, in TD-Gammon | 425 | taught | RL #55 Self-play (TD-Gammon) |
| history of reinforcement learning | 13–22 | index-noise | chapter pointer (S&B §1.7 history) |
| Holland, John | 19, 21, 44, 139, 241 | index-noise | person's name |
| Hull, Clark | 16, 359, 360, 362–363 | index-noise | person's name |
| importance sampling | 103–117, 151, 257 | taught | RL #18; robotics.md §4 new MA "Importance sampling" |
| importance sampling, ratio | 104, 148, 258 | taught | RL #18 Off-policy learning with importance sampling [hand-checked] |
| importance sampling, weighted and ordinary | 105, 106 | taught | RL #18 Off-policy learning with importance sampling [hand-checked] |
| importance sampling, and eligibility traces | 309–312 | taught | RL #24 (off-policy traces) |
| importance sampling, and infinite variance | 106 | taught | RL #18 Off-policy learning with importance sampling [hand-checked] |
| importance sampling, discounting aware | 112–113 | taught | RL #18 Off-policy learning with importance sampling |
| importance sampling, incremental implementation | 109 | taught | RL #18 (incremental weighted average) |
| importance sampling, per-decision | 114–115 | taught | RL #18 Off-policy learning with importance sampling |
| importance sampling, n-step | 148–156 | taught | RL #23 n-step bootstrapping |
| incremental implementation |  | taught | RL #3 Incremental updates and step sizes [hand-checked] |
| incremental implementation, of averages | 30–33 | taught | RL #3 Incremental updates and step sizes [hand-checked] |
| incremental implementation, of weighted averages | 109 | taught | RL #18 (incremental weighted average) |
| instrumental conditioning | 357–361 | out-of-scope | psychology (S&B §14.3); dropped in robotics.md §7 (SB14.x) |
| instrumental conditioning, and motivation | 360–361 | out-of-scope | psychology (S&B §14.3); dropped in robotics.md §7 (SB14.x) |
| instrumental conditioning, Thorndike’s puzzle boxes | 358 | out-of-scope | psychology (S&B §14.3); dropped in robotics.md §7 (SB14.x) |
| interest and emphasis | 234–235, 282, 316 | taught | RL #52 (interest and emphasis; optional) |
| inverse reinforcement learning | 470 | taught | RO #189 Inverse RL [hand-checked] |
| Jack’s car rental example | 81–82, 137, 210 | out-of-scope | book-specific worked example (S&B §4.3); policy iteration is RL #13 |
| kernel-based function approximation | 232–233 | taught | RL #51 Least-squares TD and nonparametric value functions (optional) |
| Klopf, A. Harry | xv, xvii, 19–21, 402–404, 411 | index-noise | person's name |
| latent learning | 192, 363, 366 | out-of-scope | psychology (S&B §14.5); dropped in robotics.md §7 (SB14.x) |
| Law of Effect | 15–16, 45, 343, 358–361, 417 | out-of-scope | psychology and history (S&B §1.7, §14.3); dropped in robotics.md §7 (SB14.x) |
| learning automata | 18 | out-of-scope | history (S&B §1.7) |
| Least Mean Square (LMS) algorithm | 279, 301 | taught | ML-058 Stochastic gradient descent (LMS = SGD on a linear model) |
| Least-Squares TD (LSTD) | 228–229 | taught | RL #51 Least-squares TD (optional) |
| linear function approx. | 204–209, 266–269 | taught | RL #26 Linear value functions and features [hand-checked] |
| linear programming | 87, 90 | taught | MA-068 Linear and quadratic programming; RL #54 |
| local and global optima | 200 | taught | MA-065 Convex and non-convex cost functions |
| Markov decision process (MDP) | 2, 14, 47–71 | taught | RL #7 Markov decision processes |
| Markov property | 49, 115, 465–468 | taught | RL #7; robotics.md §4 new MA "Markov chains" |
| Markov reward process (MRP) | 125 | add | Markov reward process (MRP) [RL] -> RL-02 Note #10 Bellman equations (short section: a fixed policy turns an MDP into an MRP; the linear Bellman system). S&B p.125 uses it for the random-walk example; standard first step in RL lectures before MDP control |
| maximization bias | 134–136 | taught | RL #22 Double Q-learning |
| maximum-likelihood estimate | 128 | taught | MA-070 Maximum likelihood estimation |
| MC | see Monte Carlo methods | index-noise | cross-reference to "Monte Carlo methods" |
| Mean Square |  | index-noise | heading only; sub-entries judged separately |
| Mean Square, Bellman Error, BE | 268 | taught | RL #52 Bellman error geometry [hand-checked] |
| Mean Square, Projected Bellman Error, PBE | 269 | taught | RL #52 Bellman error geometry [hand-checked] |
| Mean Square, Return Error, RE | 275 | taught | RL #52 Bellman error geometry (return error) [hand-checked] |
| Mean Square, TD Error, TDE | 270 | taught | RL #52 Bellman error geometry (TD error objective) [hand-checked] |
| Mean Square, Value Error, VE | 199–200 | taught | RL #25 (VE objective) |
| memory-based function approx. | 230–232 | taught | RL #51 (memory-based value approximation; optional) [hand-checked] |
| Michie, Donald | 17, 71, 117 | index-noise | person's name |
| Minsky, Marvin | 16, 17, 20, 89 | index-noise | person's name |
| model of the environment | 7, 159 | taught | RL #1 (four elements: model); RL #45 |
| model-based and model-free methods | 7, 159 | taught | RL #45 Models and Dyna [hand-checked] |
| model-based and model-free methods, in animal learning | 363–368 | out-of-scope | psychology (S&B §14.6); dropped in robotics.md §7 (SB14.x) |
| model-based reinforcement learning | 159–193 | taught | RL-06 (#45-#50) [hand-checked] |
| model-based reinforcement learning, in neuroscience | 407–409 | out-of-scope | neuroscience (S&B §15.11); dropped in robotics.md §7 (SB15.x) |
| Monte Carlo methods | 91–117 | taught | RL #16 Monte Carlo prediction [hand-checked] |
| Monte Carlo methods, first- and every-visit MC | 92 | taught | RL #16 Monte Carlo prediction |
| Monte Carlo methods, first-visit MC control | 101 | taught | RL #17 Monte Carlo control [hand-checked] |
| Monte Carlo methods, first-visit MC prediction | 92 | taught | RL #16 Monte Carlo prediction |
| Monte Carlo methods, gradient method for v_π | 202 | taught | RL #25 (gradient Monte Carlo) [hand-checked] |
| Monte Carlo methods, Monte Carlo ES (Exploring Starts) | 99 | taught | RL #17 Monte Carlo control |
| Monte Carlo methods, off-policy control | 111, 110–112 | taught | RL #18 Off-policy learning with importance sampling |
| Monte Carlo methods, off-policy prediction | 103–109, 110 | taught | RL #18 Off-policy learning with importance sampling [hand-checked] |
| Monte Carlo Tree Search (MCTS) | 185–188 | taught | RL #48 Monte Carlo tree search |
| motivation | 360–361 | out-of-scope | psychology (S&B §14.3); dropped in robotics.md §7 (SB14.x) |
| mountain car example | 244–248, 305, 306 | taught | RL #27 (episodic semi-gradient Sarsa on mountain car) |
| multi-armed bandits | 25–45 | taught | RL #2 Multi-armed bandits and epsilon-greedy |
| n-step methods | 141–158 | taught | RL #23 n-step bootstrapping [hand-checked] |
| n-step methods, Q(σ) | 156 | taught | RL #23 n-step bootstrapping (n-step Q(σ)) |
| n-step methods, Sarsa | 147, 247 | taught | RL #23 n-step bootstrapping [hand-checked] |
| n-step methods, Sarsa, differential | 255 | taught | RL #27 (differential semi-gradient n-step Sarsa) |
| n-step methods, Sarsa, off-policy | 149 | taught | RL #23 n-step bootstrapping (off-policy with IS) |
| n-step methods, TD | 144 | taught | RL #23 n-step bootstrapping [hand-checked] |
| n-step methods, Tree Backup | 154 | taught | RL #23 n-step bootstrapping (tree-backup) |
| n-step methods, truncated λ-return | 295 | taught | RL #24 (truncated λ-return) [hand-checked] |
| naughts and crosses | see tic-tac-toe | index-noise | cross-reference to "tic-tac-toe" |
| neural networks | see artificial neural networks | index-noise | cross-reference to "artificial neural networks" |
| neurodynamic programming | 15 | out-of-scope | alternative name in the history section (S&B §1.7); the method is approximate DP |
| neuroeconomics | 413, 419 | out-of-scope | neuroscience (S&B §15.12); dropped in robotics.md §7 (SB15.x) |
| neuroscience | 4, 21, 377–419 | out-of-scope | neuroscience chapter (S&B ch.15); dropped in robotics.md §7 (SB15.x) |
| nonstationarity | 30, 32–36, 44, 255 | taught | RL #3 (constant step size for nonstationary problems) [hand-checked] |
| nonstationarity, inherent | 91, 198 | taught | RL #25 (moving targets in value approximation) |
| notation | xiii, xix | index-noise | front-matter pointer (notation list) |
| observations | 464 | taught | RO #153 POMDPs and belief space |
| off-policy methods | 257–286 | taught | RL #18; RL #28 |
| off-policy methods, vs on-policy methods | 100, 103 | taught | RL #18 Off-policy learning with importance sampling [hand-checked] |
| off-policy methods, Monte Carlo | 103–115 | taught | RL #18 Off-policy learning with importance sampling [hand-checked] |
| off-policy methods, Q-learning | 131 | taught | RL #21 Q-learning |
| off-policy methods, Expected Sarsa | 133–134 | taught | RL #20 Sarsa and expected Sarsa |
| off-policy methods, n-step | 148–156 | taught | RL #23 n-step bootstrapping |
| off-policy methods, n-step Q(σ) | 156 | taught | RL #23 n-step bootstrapping |
| off-policy methods, n-step Sarsa | 149 | taught | RL #23 n-step bootstrapping |
| off-policy methods, n-step Tree Backup | 154 | taught | RL #23 n-step bootstrapping |
| off-policy methods, and eligibility traces | 309–316 | taught | RL #24 (off-policy traces) |
| off-policy methods, Emphatic-TD(λ) | 315 | taught | RL #52 (emphatic TD; optional) [hand-checked] |
| off-policy methods, GQ(λ) | 315 | taught | RL #52 (gradient-TD family; optional) [hand-checked] |
| off-policy methods, GTD(λ) | 314 | taught | RL #52 (gradient-TD family; optional) [hand-checked] |
| off-policy methods, HTD(λ) | 315 | taught | RL #52 (gradient-TD family; optional) [hand-checked] |
| off-policy methods, Q(λ) | 312–314 | taught | RL #24 (off-policy traces) |
| off-policy methods, Tree Backup(λ) | 312–314 | taught | RL #24 (off-policy traces) |
| off-policy methods, reducing variance | 283–284 | taught | RL #18 (per-decision IS); RL #24 |
| on-policy distribution | 175, 199, 208, 258, 262, 281, 282 | taught | RL #25 (VE weighted by state visits) |
| on-policy distribution, vs uniform distribution | 176 | taught | RL #46 (trajectory sampling) |
| on-policy methods | 100 | taught | RL #17 Monte Carlo control (on-policy) |
| on-policy methods, actor–critic | 332, 333 | taught | RL #32 Actor-critic |
| on-policy methods, approximate |  | index-noise | heading only; sub-entries judged separately |
| on-policy methods, approximate, control | 244, 247, 251, 255 | taught | RL #27 Control with approximation [hand-checked] |
| on-policy methods, approximate, prediction | 202, 203, 209 | taught | RL #25 Value prediction as supervised learning [hand-checked] |
| on-policy methods, Monte Carlo | 101, 100–103, 328, 330 | taught | RL #17 Monte Carlo control |
| on-policy methods, n-step | 144, 147 | taught | RL #23 n-step bootstrapping |
| on-policy methods, Sarsa | 130, 129–131 | taught | RL #20 Sarsa and expected Sarsa [hand-checked] |
| on-policy methods, TD(0) | 120, 119–128 | taught | RL #19 TD(0) prediction [hand-checked] |
| on-policy methods, with eligibility traces | 293, 300, 305, 307 | taught | RL #24 Eligibility traces and TD(lambda) |
| operant conditioning | see instrumental learning | index-noise | cross-reference to "instrumental learning" |
| optimal control | 2, 14–15, 21 | taught | RO #205 LQR (Hamilton-Jacobi-Bellman); RL #10 (principle of optimality) |
| optimistic initial values | 34–35, 192 | taught | RL #4 Exploring smartly: optimistic starts and UCB |
| optimizing memory control | 432–436 | out-of-scope | case study (S&B §16.4); dropped in robotics.md §7 (SB16.4) |
| options | 461–464 | taught | RO #184 Options: temporal abstraction |
| options, models of | 462 | add | option models and planning with options (Bellman equation over options) [RL] -> RO-13, section in Note #184 Options: temporal abstraction. S&B §17.2; Note #184 lists only options as temporally extended actions |
| pain and pleasure | 6, 16, 413 | out-of-scope | psychology (S&B ch.14-15); dropped in robotics.md §7 |
| Partially Observable MDPs (POMDPs) | 467 | taught | RO #153 POMDPs and belief space |
| Pavlov, Ivan | 16, 343–345, 362 | index-noise | person's name |
| Pavlovian |  | index-noise | heading only; sub-entries judged separately |
| Pavlovian, conditioning | see classical conditioning | index-noise | cross-reference to "classical conditioning" |
| Pavlovian, control | 343, 371, 373, 478 | out-of-scope | psychology (S&B §14.2); dropped in robotics.md §7 (SB14.x) |
| personalizing web services | 450–453 | taught | RL #6 Contextual bandits (personalized web services) |
| planning | 3, 5, 7, 11, 138, 159–193 | taught | RL #45 Models and Dyna; RL-06 |
| planning, in psychology | 363, 364, 366 | out-of-scope | psychology (S&B §14.5); dropped in robotics.md §7 (SB14.x) |
| planning, with learned models | 161–168, 473 | taught | RL #45 Models and Dyna; RL #49 [hand-checked] |
| planning, with options | 461, 463 | add | option models and planning with options (Bellman equation over options) [RL] -> RO-13, section in Note #184 Options: temporal abstraction. S&B §17.2; Note #184 lists only options as temporally extended actions |
| policy | 6, 41, 58 | taught | RL #9 Policies, plans and value functions |
| policy, hierarchical | 462 | taught | RO #184 Options (hierarchical RL) |
| policy, soft and ε-soft | 100–103, 110 | taught | RL #17 Monte Carlo control (epsilon-soft) |
| policy approximation | 321–324 | taught | RL #29 Parameterised policies [hand-checked] |
| policy evaluation | 74–76 | taught | RL #12 Policy evaluation |
| policy evaluation, iterative | 75 | taught | RL #12 Policy evaluation |
| policy gradient methods | 321–338 | taught | RL #30 The policy gradient theorem and REINFORCE [hand-checked] |
| policy gradient methods, REINFORCE | 328, 330 | taught | RL #30 The policy gradient theorem and REINFORCE [hand-checked] |
| policy gradient methods, actor–critic | 332, 333 | taught | RL #32 Actor-critic |
| policy gradient theorem | 324–326 | taught | RL #30 The policy gradient theorem and REINFORCE |
| policy gradient theorem, proof, episodic case | 325 | out-of-scope | proof (S&B §13.2 boxed proof); the theorem itself is RL #30 |
| policy gradient theorem, proof, continuing case | 334 | out-of-scope | proof (S&B §13.6 boxed proof); the theorem itself is RL #30 |
| policy improvement | 76–80 | taught | RL #13 Policy improvement and policy iteration |
| policy improvement, theorem | 78, 101 | taught | RL #13 Policy improvement and policy iteration |
| policy iteration | 14, 80, 80–82 | taught | RL #13 Policy improvement and policy iteration |
| polynomial basis | 210–211 | taught | ML-060 polynomial regression (recap in robotics.md §5, row SB9.5) [hand-checked] |
| prediction | 74–76 | taught | RL #12 Policy evaluation [hand-checked] |
| prediction, and control | 342 | taught | RL #12 (prediction) and RL #13 (control) [hand-checked] |
| prediction, Monte Carlo | 92–97 | taught | RL #16 Monte Carlo prediction |
| prediction, off-policy | 103–108 | taught | RL #18 Off-policy learning with importance sampling |
| prediction, TD | 119–126 | taught | RL #19 TD(0) prediction |
| prediction, with approximation | 197–242 | taught | RL #25 Value prediction as supervised learning |
| prior knowledge | 12, 34, 54, 137, 236, 324, 471 | taught | RO #132 Why robot RL is hard (using prior knowledge) |
| prioritized sweeping | 170, 168–171 | taught | RL #46 Prioritized sweeping |
| projected Bellman error | 285 | taught | RL #52 Bellman error geometry and gradient-TD |
| projected Bellman error, vector | 267, 269 | taught | RL #52 Bellman error geometry and gradient-TD [hand-checked] |
| proximal TD methods | 286 | out-of-scope | research method named in bibliographic remarks only (S&B §11.10, p.286) |
| pseudo termination | 282, 308 | taught | RL #24 (variable γ read as termination); RL #52 [hand-checked] |
| psychology | 4, 13, 19, 20, 341–376 | out-of-scope | psychology chapter (S&B ch.14); dropped in robotics.md §7 (SB14.x) |
| Q(λ), Watkins’s | 312–314 | taught | RL #24 (off-policy traces) |
| Q-function | see action-value function | index-noise | cross-reference to "action-value function" |
| Q-learning | 21, 131, 131–135 | taught | RL #21 Q-learning |
| Q-learning, double | 136 | taught | RL #22 Double Q-learning |
| Q-planning | 161 | taught | RL #45 Models and Dyna (random-sample one-step tabular Q-planning) |
| Q(σ) | 156, 154–156 | taught | RL #23 n-step bootstrapping (n-step Q(σ)) |
| queuing example | 252 | out-of-scope | book-specific worked example (S&B §10.3); average reward is RL #27 |
| R-learning | 256 | out-of-scope | 1993 algorithm named in bibliographic remarks only (S&B §10.6, p.256) |
| racetrack exercise | 111 | out-of-scope | book exercise (S&B Ex. 5.12) |
| radial basis functions (RBFs) | 221–222 | taught | RL #26 Linear value functions and features (RBF features) |
| random walk | 95 | out-of-scope | book-specific worked example (S&B §6.2) |
| random walk, 5-state | 125, 126, 127 | out-of-scope | book-specific worked example (S&B §6.2) |
| random walk, 19-state | 144, 291 | out-of-scope | book-specific worked example (S&B §7.1) |
| random walk, 19-state, TD(λ) results on | 294, 295, 299 | out-of-scope | book-specific worked example (S&B §12.1) |
| random walk, 1000-state | 203–209, 217, 218 | out-of-scope | book-specific worked example (S&B §9.2) |
| random walk, 1000-state, Fourier and polynomial bases | 214 | out-of-scope | book-specific worked example (S&B §9.5) |
| real-time dynamic programming | 177–180 | taught | RL #46 (trajectory sampling and real-time DP) |
| recycling robot example | 52 | out-of-scope | book-specific worked example (S&B §3.3) |
| REINFORCE | 328, 326–331 | taught | RL #30 The policy gradient theorem and REINFORCE |
| REINFORCE, with baseline | 330 | taught | RL #31 Baselines [hand-checked] |
| reinforcement learning | 1–22 | taught | RL #1 The reinforcement learning problem |
| reinforcement signal | 380 | out-of-scope | neuroscience (S&B §15.4); dropped in robotics.md §7 (SB15.x) |
| representation learning | 473 | taught | RO #353 Pretrained visual representations; DL-002 (learned features) |
| residual-gradient algorithm | 272–274, 277 | taught | RL #52 (residual-gradient methods; optional) [hand-checked] |
| residual-gradient algorithm, naive | 270, 271 | taught | RL #52 (residual-gradient methods; optional) [hand-checked] |
| return | 54–58 | taught | RL #8 Return and discounting |
| return, n-step | 143 | taught | RL #23 n-step bootstrapping |
| return, n-step, for Q(σ) | 155 | taught | RL #23 n-step bootstrapping |
| return, n-step, for action values | 146 | taught | RL #23 n-step bootstrapping [hand-checked] |
| return, n-step, for Expected Sarsa | 148 | taught | RL #23 n-step bootstrapping [hand-checked] |
| return, n-step, for Tree Backup | 153 | taught | RL #23 n-step bootstrapping |
| return, n-step, with control variates | 150, 151 | taught | RL #23 n-step bootstrapping (control variates) |
| return, n-step, with function approximation | 209 | taught | RL #27 (semi-gradient n-step Sarsa) |
| return, differential | 250, 255, 334 | taught | RL #27 (differential values) |
| return, flat partial | 113 | taught | RL #18 (discounting-aware IS uses flat partial returns) [hand-checked] |
| return, with state-dependent termination | 308 | taught | RL #24 (variable γ) |
| return, λ-return | 288–291 | taught | RL #24 Eligibility traces and TD(lambda) |
| return, λ-return, truncated | 296 | taught | RL #24 Eligibility traces and TD(lambda) |
| reward prediction error hypothesis | 381–383, 387–395 | out-of-scope | neuroscience (S&B §15.3-15.6); dropped in robotics.md §7 (SB15.x) |
| reward signal | 1, 6, 48, 53, 361, 380, 383, 397 | taught | RL #1; RO #146 Reward shaping and its risks |
| reward signal, and reinforcement | 373–375, 380–381 | out-of-scope | neuroscience (S&B §15.4); dropped in robotics.md §7 (SB15.x) |
| reward signal, design of | 469–472, 477 | taught | RO #146 Reward shaping and its risks (designing reward signals) |
| reward signal, intrinsic | 474 | taught | RO #182 Curiosity and intrinsic rewards [hand-checked] |
| reward signal, sparse | 469–470 | taught | RO #146; RO #150 Sparse rewards and hindsight relabelling |
| rod maneuvering example | 171 | out-of-scope | book-specific worked example (S&B §8.4) |
| rollout algorithms | 183–185 | taught | RL #47 Decision-time planning and rollouts |
| root mean square (RMS) error | 125 | taught | ML-051 Regression metrics (RMSE) |
| safety | 434, 478 | taught | RO-14 Safety and constraints (#192-#200) [hand-checked] |
| sample and expected updates | 121, 170–174 | taught | RL #46 (expected vs sample updates) |
| sample or simulation model | 115 | taught | RL #45 (distribution vs sample models) |
| sample-average method | 27 | taught | RL #2 (sample-average action values) |
| Samuel’s checkers player | 20, 241, 426–429 | taught | RL #55 Self-play (Samuel checkers) |
| Sarsa | 130, 129–131, 244 | taught | RL #20 Sarsa and expected Sarsa |
| Sarsa, vs Q-learning | 132 | taught | RL #20, RL #21 [hand-checked] |
| Sarsa, differential, one-step | 251 | taught | RL #27 (differential semi-gradient Sarsa) |
| Sarsa, Expected | 133–134, 140 | taught | RL #20 Sarsa and expected Sarsa |
| Sarsa, Expected, n-step | 148 | taught | RL #23 n-step bootstrapping [hand-checked] |
| Sarsa, Expected, n-step off-policy | 150 | taught | RL #23 n-step bootstrapping [hand-checked] |
| Sarsa, Expected, double | 136 | taught | RL #22 Double Q-learning (double expected Sarsa, S&B Ex. 6.13) [hand-checked] |
| Sarsa, n-step | 147, 145–148, 247 | taught | RL #23 n-step bootstrapping |
| Sarsa, n-step, differential | 255 | taught | RL #27 (differential semi-gradient n-step Sarsa) |
| Sarsa, n-step, off-policy | 149 | taught | RL #23 n-step bootstrapping |
| Sarsa(λ) | 305, 303–307 | taught | RL #24 Eligibility traces and TD(lambda) |
| Sarsa(λ), true online | 307 | taught | RL #24 Eligibility traces and TD(lambda) |
| Schultz, Wolfram | 387–395, 410 | index-noise | person's name |
| search control | 163 | taught | RL #45 Models and Dyna (search control) [hand-checked] |
| secondary reinforcement | 20, 346, 354, 369 | out-of-scope | psychology (S&B §14.2); dropped in robotics.md §7 (SB14.x) |
| selective bootstrap adaptation | 239 | out-of-scope | history (S&B §9.12, Widrow 1973) |
| semi-gradient methods | 202, 258–259 | taught | RL #25 Value prediction as supervised learning |
| SGD | see stochastic gradient descent | index-noise | cross-reference to "stochastic gradient descent" |
| Shannon, Claude | 16, 20, 71, 426 | index-noise | person's name |
| shaping | 360, 470 | taught | RO #146 Reward shaping and its risks |
| Skinner, B. F. | 359–360, 375, 470, 479 | index-noise | person's name |
| soap bubble example | 95 | out-of-scope | book-specific illustration (S&B §5.1) |
| soft and ε-soft policies | 100–103, 110 | taught | RL #17 Monte Carlo control (epsilon-soft) |
| soft-max | 322–323, 329, 336, 400, 445, 455 | taught | RL #5 Gradient bandits; RL #29 [hand-checked] |
| soft-max, for bandits | 37, 45 | taught | RL #5 Gradient bandits [hand-checked] |
| spike-timing-dependent plasticity (STDP) | 401 | out-of-scope | neuroscience (S&B §15.8); dropped in robotics.md §7 (SB15.x) |
| state | 7, 48, 49 | taught | RL #9; RO #63 (state) |
| state, kth-order history approach | 468 | taught | RO #162 History encoders (frame stacks) |
| state, and observations | 464–468 | taught | RO #153 POMDPs and belief space |
| state, and observations, Markov property | 465–468 | taught | RO #153 POMDPs and belief space [hand-checked] |
| state, belief | 467 | taught | RO #153 POMDPs and belief space |
| state, latent | 467 | taught | RO #153 POMDPs and belief space (hidden state) [hand-checked] |
| state, observable operator models (OOMs) | 467 | out-of-scope | research-only state representation, named in S&B §17.3 only |
| state, partially observable MDPs | 14, 467 | taught | RO #153 POMDPs and belief space |
| state, predictive state representations | 467 | out-of-scope | research-only state representation, named in S&B §17.3 only |
| state, state-update function | 465 | taught | RO #153 POMDPs and belief space (state-update function) |
| state aggregation | 203–204 | add | state aggregation [RL] -> RL-04 Note #26 Linear value functions and features (short section). S&B §9.3 opens function approximation with it (1000-state random walk); simplest feature map, one value per group of states |
| state-update function | 465 | taught | RO #153 POMDPs and belief space (state-update function) |
| step-size parameter | 10, 31–33, 120, 125, 126 | taught | RL #3 Incremental updates and step sizes [hand-checked] |
| step-size parameter, automatic adaptation | 238 | taught | DL-036 to DL-038 (AdaGrad, RMSprop, Adam adapt step sizes) |
| step-size parameter, in DQN | 439, 440 | taught | RL #35 Deep Q-networks [hand-checked] |
| step-size parameter, in psychological models | 347, 348 | out-of-scope | psychology (S&B ch.14); dropped in robotics.md §7 (SB14.x) |
| step-size parameter, selecting manually | 222–223 | taught | RL #26 (choosing the step size by hand) |
| step-size parameter, with coarse coding | 216 | taught | RL #26 (choosing the step size by hand) |
| step-size parameter, with Fourier features | 213 | taught | RL #26 (choosing the step size by hand) |
| step-size parameter, with tile coding | 217, 223 | taught | RL #26 (choosing the step size by hand) |
| stochastic approx. convergence conditions | 33 | taught | RL #3 (Robbins-Monro step-size conditions) |
| stochastic gradient descent (SGD) | 200–204 | taught | ML-058 Stochastic gradient descent |
| stochastic gradient descent (SGD), in the Bellman error | 269–278 | taught | RL #52 (residual-gradient: SGD in the Bellman error) [hand-checked] |
| strong and weak methods | 4 | out-of-scope | AI-history framing (S&B §1.1) |
| supervised learning | xvii, 2, 17–19, 198 | taught | ML-003 Types of ML |
| sweeps | 75, 160 | taught | RL #12 Policy evaluation (sweeps); RL #46 |
| synaptic plasticity | 379 | out-of-scope | neuroscience (S&B §15.1); dropped in robotics.md §7 (SB15.x) |
| synaptic plasticity, Hebbian | 400 | out-of-scope | neuroscience (S&B §15.8); dropped in robotics.md §7 (SB15.x) |
| synaptic plasticity, two-factor and three factor | 400 | out-of-scope | neuroscience (S&B §15.8); dropped in robotics.md §7 (SB15.x) |
| system identification | 364 | taught | RO #139 System identification and actuator models |
| tabular solution methods | 23 | taught | RL #11 (tabular vs approximate solutions) |
| target |  | index-noise | heading only; sub-entries judged separately |
| target, policy | 103, 110 | taught | RL #18 Off-policy learning with importance sampling |
| target, of update | 31, 143, 198 | taught | RL #3 (new = old + step x (target - old)) |
| TD | see temporal-difference learning | index-noise | cross-reference to "temporal-difference learning" |
| TD error | 121 | taught | RL #19 TD(0) prediction |
| TD error, n-step | 255 | taught | RL #27 (differential n-step TD error) |
| TD error, differential | 250 | taught | RL #27 (differential TD error) [hand-checked] |
| TD error, with function approximation | 270 | taught | RL #25 Value prediction as supervised learning [hand-checked] |
| TD(λ) | 293, 292–295 | taught | RL #24 Eligibility traces and TD(lambda) |
| TD(λ), truncated | 295–297 | taught | RL #24 Eligibility traces and TD(lambda) |
| TD(λ), true online | 300, 299–301 | taught | RL #24 Eligibility traces and TD(lambda) |
| TD-Gammon | 21, 421–426 | taught | RL #55 Self-play: from TD-Gammon to AlphaZero |
| temporal abstraction | 461–464 | taught | RO #184 Options: temporal abstraction |
| temporal-difference learning | 10, 119–140 | taught | RL #19 TD(0) prediction; RL-03 |
| temporal-difference learning, history of | 20–21 | out-of-scope | history (S&B §1.7) |
| temporal-difference learning, advantages of | 124–126 | taught | RL #19 TD(0) prediction [hand-checked] |
| temporal-difference learning, optimality of | 126–128 | taught | RL #19 (batch TD and certainty equivalence) |
| temporal-difference learning, TD(0) | 120, 203 | taught | RL #19 TD(0) prediction |
| temporal-difference learning, TD(1) | 294 | taught | RL #24 Eligibility traces and TD(lambda) |
| temporal-difference learning, TD(λ) | 293, 292–295 | taught | RL #24 Eligibility traces and TD(lambda) |
| temporal-difference learning, TD(λ), true online | 300, 299–301 | taught | RL #24 Eligibility traces and TD(lambda) |
| temporal-difference learning, λ-return methods |  | taught | RL #24 Eligibility traces and TD(lambda) |
| temporal-difference learning, λ-return methods, off-line | 290 | taught | RL #24 Eligibility traces and TD(lambda) |
| temporal-difference learning, λ-return methods, online | 297–299 | taught | RL #24 Eligibility traces and TD(lambda) |
| temporal-difference learning, n-step | 144, 141–158, 209 | taught | RL #23 n-step bootstrapping |
| termination function | 307, 459 | taught | RO #184 Options (termination function); RO #170 GVFs [hand-checked] |
| Thompson sampling | 43, 45 | add | Thompson sampling (posterior sampling) [RL] -> RL-01 Note #4 Exploring smartly: optimistic starts and UCB (section after UCB). S&B §2.9 names it as the Bayesian bandit method that works well in practice; DM ch.15 teaches it as posterior sampling; standard in bandit lectures beside UCB |
| Thorndike, Edward | see Law of Effect | index-noise | cross-reference to "Law of Effect" |
| tic-tac-toe | 8–13, 17, 137 | taught | RL #19 TD(0) prediction (tic-tac-toe value learning) |
| tile coding | 217–221, 223, 238, 246, 434, 435 | taught | RL #26 Linear value functions and features |
| Tolman, Edward | 364, 408 | index-noise | person's name |
| trace-decay parameter (λ) | 287, 289, 290, 292 | taught | RL #24 Eligibility traces and TD(lambda) |
| trace-decay parameter (λ), state dependent | 307 | taught | RL #24 (variable λ) |
| trajectory sampling | 174–177 | taught | RL #46 (trajectory sampling) |
| transition probabilities | 49 | taught | RL #7 Markov decision processes [hand-checked] |
| Tree Backup |  | taught | RL #23 n-step bootstrapping (tree-backup) |
| Tree Backup, n-step | 152–153, 154 | taught | RL #23 n-step bootstrapping |
| Tree Backup, Tree-Backup(λ) | 312–314 | taught | RL #24 (off-policy traces) |
| trial-and-error | 1, 7, 15–21, 403, 404 | taught | RL #1 The reinforcement learning problem [hand-checked] |
| true online TD(λ) | 300, 299–301 | taught | RL #24 Eligibility traces and TD(lambda) |
| Tsitsiklis and Van Roy’s Counterexample | 263 | out-of-scope | second divergence counterexample (S&B §11.2); the same lesson as Baird's counterexample, RL #28 |
| undiscounted continuing tasks | see average reward setting | index-noise | cross-reference to "average reward setting" |
| unsupervised learning | 2, 226 | taught | ML-003 Types of ML |
| value | 6, 26, 47 | taught | RL #1 The reinforcement learning problem |
| value function | 6, 58–67 | taught | RL #9 Policies, plans and value functions |
| value function, for a given policy: v_π and q_π | 58 | taught | RL #9 Policies, plans and value functions [hand-checked] |
| value function, for an optimal policy: v_* and q_* | 62 | taught | RL #11 Optimal values and optimal policies |
| value function, action | 58, 63, 65, 71, 129, 131 | taught | RL #9 Policies, plans and value functions |
| value function, approximate action values: q̂(s, a, w) | 243 | taught | RL #27 Control with approximation [hand-checked] |
| value function, approximate state values: v̂(s,w) | 197 | taught | RL #25 Value prediction as supervised learning [hand-checked] |
| value function, differential | 243 | taught | RL #27 (differential values) |
| value function, vs evolutionary methods | 11 | taught | RL #1 (evolutionary vs value-function methods) |
| value iteration | 83, 82–84 | taught | RL #14 Value iteration |
| value-function approximation | 198 | taught | RL #25 Value prediction as supervised learning [hand-checked] |
| Watkins, Chris | 15, 21, 89, 320 | index-noise | person's name |
| Watson (Jeopardy! player) | 429–432 | out-of-scope | case study (S&B §16.3); dropped in robotics.md §7 (SB16.3) |
| Werbos, Paul | 14, 21, 70, 89, 139, 239 | index-noise | person's name |
| Witten, Ian | 21, 70 | index-noise | person's name |

## Kochenderfer, Wheeler & Wray, Algorithms for Decision Making (MIT Press 2022)

Source: https://algorithmsbook.com/files/dm.pdf (redirects to the authors' Google Drive file 1drcYW3iJz4wnnCqjuVwQyc5a6eC7i6cu). Index: PDF pp. 693-700 (book pp. 671-678). Terms: 798. add 58, index-noise 91, mentioned-only 3, out-of-scope 245, taught 401

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| 2048 problem | 610 | out-of-scope | book's test problem (DM appendix F) |
| 3SAT | 577 | out-of-scope | complexity-theory example problem (DM §C.4); RO #103 names NP-hardness |
| A/B testing | 313 | taught | ML-009 (A/B testing, glossary) |
| absolutely homogeneous | 562 | out-of-scope | norm axiom (DM §A.3), proof-level property; norms themselves are MA-049 |
| absorbing | 599 | add | absorbing terminal state (one notation for episodic and continuing tasks) [RL] -> RL-02, short section in Note #8 Return and discounting. S&B §3.4 and DM appendix F use it; Note #8 lists episodes and continuing tasks but not the absorbing state that unifies them |
| abstract types | 638 | index-noise | Julia language feature (DM appendix G) |
| action distribution | 471 | out-of-scope | finite-state-controller parameter (DM §23.1); research-level POMDP controller |
| action node | 116 | out-of-scope | decision-network (influence-diagram) notation (DM §6.5); the plan models decisions with MDPs/POMDPs (RL #7, RO #153) |
| action profile | see joint action | index-noise | cross-reference to "joint action" |
| action space | 133, 599 | taught | RL #7; RO #134 Action spaces |
| action value function | 139 | taught | RL #9 Policies, plans and value functions |
| activation function | 582 | taught | DL-027 Activation functions |
| actor-critic methods | 267 | taught | RL #32 Actor-critic [hand-checked] |
| acyclic | 572 | add | graph basics: directed and undirected graphs, paths, cycles, DAGs, trees (parent, child) [maths] -> RO-05, short section in Note #103 Graphs and uninformed search. Note #103 lists 'graph as a model of a state space' only; Bayes nets, factor graphs (RO #263), roadmaps and search trees all need this vocabulary (DM appendix A, OPT §19) |
| adaptive injection | 394 | taught | RO #95 (augmented MCL injects random particles) [hand-checked] |
| ad hoc exploration | 301 | taught | RL #2 (epsilon-greedy and other simple rules) [hand-checked] |
| admissible | 606 | taught | RO #105 A* and heuristics |
| admissible heuristic | 197 | taught | RO #105 A* and heuristics |
| advantage | 245 | taught | RL #34 Advantage and GAE |
| advantage function | 139 | taught | RL #34 Advantage and GAE |
| adversarial analysis | 291 | add | falsification: searching for the disturbances that make a policy fail (adversarial stress testing) [robotics] -> RO-20, section in Note #249 Evaluating driving (scenario-based testing). DM ch.14; RO #248-#249 list scenario testing and safety cases but not the search for failures |
| adversarial learning | 369, 597 | taught | RB #318 Adversarial imitation: GAIL; robotics.md §4 new DL "Generative adversarial networks" [hand-checked] |
| adversary | 291 | taught | RO #141 Robust RL: training against an adversary |
| agent | 1 | taught | RL #1 The reinforcement learning problem [hand-checked] |
| aircraft collision avoidance problem | 614 | out-of-scope | book's test problem (DM appendix F) |
| almost-rock-paper-scissors | 515 | out-of-scope | book's test problem (DM appendix F) |
| AlphaGo Zero | 276 | taught | RL #55 Self-play: from TD-Gammon to AlphaZero [hand-checked] |
| alpha vector | 411 | taught | RO #268 Exact POMDP planning: alpha vectors |
| anonymous function | 640 | index-noise | Julia language feature (DM appendix G) |
| approximate dynamic programming | 161 | taught | RL #25-#27; RO #106 (DP with interpolation) |
| array comprehension | 630 | index-noise | Julia language feature (DM appendix G) |
| artificial intelligence | 2 | taught | ML-002 AI vs ML vs DL |
| asymptotic notation | 575 | taught | RO #103 (Big-O) |
| asynchronous value iteration | 145 | taught | RL #15 Asynchronous DP and generalized policy iteration [hand-checked] |
| autoencoder | 592 | taught | DL-003 (short paragraph); robotics.md §4 new DL "Variational autoencoder" |
| average return | 135 | taught | RL #8 Return and discounting |
| average reward | 135 | taught | RL #27 (average-reward setting) |
| axioms of probability | 20 | taught | MA-011 Empirical and theoretical probability (axioms, glossary) |
| backpropagation | 585 | taught | DL-015/DL-016 backpropagation |
| backup | 432 | taught | RL #10 (backups); RO #268 (belief-space backup) |
| backward induction value iteration | 145 | taught | RL #14 Value iteration (finite horizon); RO #205 (backward Riccati DP) [hand-checked] |
| Banach fixed-point theorem | see contraction mapping theorem | index-noise | cross-reference to "contraction mapping theorem" |
| bandwidth | 82 | taught | MA-023 Density estimation (KDE bandwidth, glossary) |
| baseline | 241 | taught | RL #31 Baselines |
| basis function | 172 | taught | RL #26 Linear value functions and features |
| batch | 345, 582 | taught | ML-057/ML-059 batch and mini-batch gradient descent |
| batch reinforcement learning | 299 | taught | RB #343 Offline RL and distribution shift [hand-checked] |
| Bayes’ rule | 30 | taught | MA-018 Bayes' theorem |
| Bayes-adaptive Markov decision process | 329 | out-of-scope | exact Bayes-optimal exploration, intractable beyond tiny problems (DM §16.6); absent from all 8 evidence docs |
| Bayesian learning | 509 | out-of-scope | game theory: belief-based learning in repeated games (DM §25.4 p.509) |
| Bayesian network | 32 | add | Bayesian networks (a joint distribution as a graph of conditional probabilities) [maths] -> MA 02-probability, new Note after MA-019 (before robotics.md §4 "Markov chains"). RO #77 teaches dynamic Bayes networks and RO #263 factor graphs; both assume the static Bayesian network; DM ch.2 makes it the base representation |
| Bayesian parameter learning | 75 | add | Bayesian parameter learning: Beta and Dirichlet priors, conjugate updates [maths] -> MA 08-likelihood, new Note after MA-072. Bayesian counterpart of MLE (MA-070); Thompson sampling needs the Beta posterior; DM §4.2 |
| Bayesian reinforcement learning | 326 | out-of-scope | exact Bayes-optimal exploration, intractable beyond tiny problems (DM §16.6); absent from all 8 evidence docs |
| Bayesian score | 98 | out-of-scope | Bayesian-network structure learning (DM ch.5); no plan Note or evidence-doc row learns graph structure |
| BDe | 104 | out-of-scope | Bayesian-network structure learning (DM §5.2); no plan Note or evidence-doc row learns graph structure |
| BDeu | 104 | out-of-scope | Bayesian-network structure learning (DM §5.2); no plan Note or evidence-doc row learns graph structure |
| behavioral cloning | 6, 355 | taught | RO #165 Behaviour cloning, compounding error and DAgger [hand-checked] |
| behavioral game theory | 504 | out-of-scope | game theory beyond Nash (DM §24.7); the plan's games Note RL #54 (optional) stops at Nash and minimax |
| behavioral policy | 530 | out-of-scope | game theory: history-dependent policies in Markov games (DM Ex. 25.3) |
| belief | 379 | taught | RO #77 Belief: what the robot knows |
| belief propagation | 53 | out-of-scope | exact inference by message passing on graphical models (DM §3.?); robot factor graphs in the plan (RO #263) are solved by least squares |
| belief simplex | 381 | taught | RO #268 (belief space as a simplex) [hand-checked] |
| belief space | 381 | taught | RO #153 POMDPs and belief space |
| belief state | 306 | taught | RO #153 POMDPs and belief space |
| belief-state Markov decision process | 407 | taught | RO #153 (planning in belief space); RO #268 |
| belief vector | 381 | taught | RO #268 Exact POMDP planning |
| Bellman backup | 141 | taught | RL #14 Value iteration (Bellman backup) [hand-checked] |
| Bellman expectation equation | 138 | taught | RL #10 Bellman equations |
| Bellman optimality equation | 142 | taught | RL #11 Optimal values and optimal policies |
| Bellman residual | 142 | taught | RL #52 (Bellman error); RL #14 |
| Bellman update | see Bellman backup | index-noise | cross-reference to "Bellman backup" |
| Bernoulli bandit | see binary bandit | index-noise | cross-reference to "binary bandit" |
| best-action best-state upper bound | 429 | out-of-scope | value-function bound for POMDP solvers (DM §21.?); research-level solver detail |
| best-action worst-state lower bound | 431 | out-of-scope | value-function bound for POMDP solvers (DM §21.?); research-level solver detail |
| best-first search | 604 | taught | RO #105 A* and heuristics (best-first search) |
| best response | 495 | taught | RL #54 (Nash equilibrium is mutual best response; optional) [hand-checked] |
| best response policy | 519 | out-of-scope | game theory: best-response dynamics in Markov games (DM ch.25); beyond RL #54 |
| beta distribution | 78 | mentioned-only | Bayesian parameter learning: Beta and Dirichlet priors, conjugate updates [maths] -> MA 08-likelihood, new Note after MA-072. MA-022 only mentions the Beta distribution; Beta posteriors drive Thompson sampling |
| bias | 239 | taught | ML-061 Bias-variance |
| big-Oh notation | 575 | taught | RO #103 (Big-O) |
| bilinear interpolation | 167 | add | linear, bilinear and multilinear interpolation on a grid [maths] -> RO-05, short section in Note #106 Grid path planning (which uses DP with interpolation). DM §8.5; also used for image undistortion (RO #89) and grid maps; no Note teaches interpolation |
| binary bandit | 299 | add | Thompson sampling (posterior sampling) [RL] -> RL-01 Note #4 Exploring smartly (section after UCB). the Bernoulli (binary) bandit with Beta posteriors is the standard worked case (DM §15.?) |
| binary variable | 20 | taught | MA-031 Bernoulli and binomial |
| binomial bandit | see binary bandit | index-noise | cross-reference to "binary bandit" |
| bit | 566 | taught | ML-091 Decision trees (entropy in bits) |
| blind lower bound | 431 | out-of-scope | value-function bound for POMDP solvers (DM §21.?); research-level solver detail |
| Boolean | 627 | index-noise | Julia language feature (DM appendix G) |
| Boolean satisfiability | 578 | out-of-scope | complexity theory (DM §C.4); RO #103 names NP-hardness |
| bottleneck | 592 | taught | DL-069 Attention mechanism (bottleneck, glossary) |
| bounded policy iteration | 475 | out-of-scope | POMDP controller search (DM §23.?); research-level |
| bowl-shaped | 564 | taught | MA-065 Convex and non-convex cost functions |
| box | 27 | add | multivariate uniform distribution (uniform over a box) [maths] -> MA 03-distributions, short section in MA-029. DM §2.3; sampling planners draw uniform samples over a box of C-space (RO #110, #111) |
| branch and bound | 185, 456, 601 | add | integer programming and branch and bound [maths] -> MA 07-optimisation, new Note after MA-068. DM uses it for planning (§9.4) and POMDPs; OPT book ch.19 teaches it; mixed-integer programs appear in footstep, TAMP and assignment problems |
| broadcasting | 633 | index-noise | Julia language feature (DM appendix G) |
| burn-in period | 61 | out-of-scope | MCMC detail (DM §3.?); no plan Note samples by Markov chains; particle methods (RO #82) cover robot sampling |
| callable | 641 | index-noise | Julia language feature (DM appendix G) |
| cart-pole problem | 611 | out-of-scope | book's test problem (DM appendix F) |
| cascading errors | 357 | taught | RO #165 (compounding error) |
| catastrophic forgetting | 345 | add | catastrophic forgetting (interference) [DL] -> RL-05 Note #36 Experience replay and target networks (short section). DM §17.? gives it as the reason for experience replay; also bears on fine-tuning robot policies (RB #345, #358) |
| catch problem | 619 | out-of-scope | book's test problem (DM appendix F) |
| causal networks | 33 | out-of-scope | causal inference, a different field (DM §2.?); not used by any plan Note |
| censored data | 92 | out-of-scope | survival statistics, a different field (DM §4.?) |
| certainty effect | 122 | out-of-scope | behavioural economics (DM §6.?); utility theory itself is RL #53 |
| certainty equivalence | 150, 419 | taught | RL #19 (certainty equivalence); RO #205 (LQR) |
| chain rule | 33 | taught | MA-015 Conditional probability (product rule) |
| chance node | 116 | out-of-scope | decision-network notation (DM §6.5) |
| Chebyshev norm | 563 | mentioned-only | vector norms L1, L2 and L-infinity (Manhattan, Euclidean, Chebyshev) [maths] -> MA 05-linear-algebra, short section in MA-049. grid planners use 4- and 8-connected distances (RO #104-#106); OPT book indexes Chebyshev distance and L1/L-infinity norms; MA only names Manhattan distance in ML-085 |
| chessboard norm | 563 | add | vector norms L1, L2 and L-infinity (Manhattan, Euclidean, Chebyshev) [maths] -> MA 05-linear-algebra, short section in MA-049. chessboard distance is the 8-connected grid distance |
| child | 572 | add | graph basics: directed and undirected graphs, paths, cycles, DAGs, trees (parent, child) [maths] -> RO-05, short section in Note #103 Graphs and uninformed search. Note #103 lists 'graph as a model of a state space' only; Bayes nets, factor graphs (RO #263), roadmaps and search trees all need this vocabulary (DM appendix A, OPT §19) |
| clamping | 257 | taught | RL #39 PPO (clipped surrogate) |
| class-conditional distribution | 48 | taught | ML-081 Naive Bayes |
| classification | 48 | taught | ML-003 Types of ML |
| clauses | 53 | out-of-scope | complexity theory (DM §C.4) |
| closed-loop planning | 200 | taught | RL #9 (open-loop vs feedback plan) |
| closed under complementation | 561 | out-of-scope | measure-theory property (DM §A.?), proof-level |
| closed under countable unions | 561 | out-of-scope | measure-theory property (DM §A.?), proof-level |
| collaborative predator-prey hex world | 625 | out-of-scope | book's test problem (DM appendix F) |
| colon notation | 20 | index-noise | notation (1:n ranges) |
| component policy | 361 | out-of-scope | research imitation variant SMILe (DM §18.?); behaviour cloning and DAgger are RO #165 |
| composite type | 638 | index-noise | Julia language feature (DM appendix G) |
| computational complexity | 575 | taught | RO #103 (algorithm cost) |
| computationally universal | 579 | out-of-scope | complexity theory (DM §C.?) |
| concave | 565 | taught | MA-067 Convex sets and functions |
| concrete types | 638 | index-noise | Julia language feature (DM appendix G) |
| conditional distribution | 29 | taught | MA-014 Joint, marginal and conditional probability |
| conditional edge | 118 | out-of-scope | decision-network notation (DM §6.5) |
| conditional Gaussian | 31 | taught | MA-073 Gaussian mixture models (Gaussian chosen by a discrete parent) |
| conditional independence | 35 | taught | MA-016; ML-082 (conditional independence, glossary) |
| conditional linear Gaussian | 31 | taught | RO #80 Kalman filter (linear Gaussian system) |
| conditional plan | 408 | taught | RO #268 (alpha vectors as conditional plans) [hand-checked] |
| conditional probability | 29 | taught | MA-015 Conditional probability |
| confidence interval | 285 | taught | MA-035 Confidence intervals |
| conjugate prior | 398 | add | Bayesian parameter learning: Beta and Dirichlet priors, conjugate updates [maths] -> MA 08-likelihood, new Note after MA-072. conjugate priors give closed-form posteriors (DM §4.2) |
| connectionism | 10 | out-of-scope | history (DM §1.?) |
| consistent | 606 | add | consistent (monotone) heuristics [robotics] -> RO-05 Note #105 A* and heuristics (short section). DM §E.? and LaValle use consistency for A* optimality without re-expansion; standard in planning courses |
| continuous entropy | see differential entropy | index-noise | cross-reference to "differential entropy" |
| continuous probability distribution | 21 | taught | MA-022 PDF and continuous CDF |
| contraction | see contraction mapping | index-noise | cross-reference to "contraction mapping" |
| contraction mapping | 136, 570 | add | Bellman operator as a contraction: why value iteration converges [RL] -> RL-02, short section in Note #14 Value iteration. S&B §11.4 (Bellman operator) and DM §7.5 (contraction mapping); no Note lists either |
| contraction mapping theorem | 570 | add | Bellman operator as a contraction: why value iteration converges [RL] -> RL-02, short section in Note #14 Value iteration. S&B §11.4 (Bellman operator) and DM §7.5 (contraction mapping); no Note lists either |
| contractor | see contraction mapping | index-noise | cross-reference to "contraction mapping" |
| controller | 471 | out-of-scope | POMDP policy representation (finite-state controller, DM ch.23); research-level |
| control theory | 2 | taught | RO-06 (#117-#125); RO-15 (#201-#211) [hand-checked] |
| convex combination | 564 | taught | MA-067 Convex sets and functions |
| convex function | 564 | taught | MA-067 Convex sets and functions |
| convex hull | 168 | taught | robotics.md §4 "Convex hull" (short section added to MA-067) |
| convex set | 564 | taught | MA-067 Convex sets and functions |
| convolutional layers | 587 | taught | DL-042 Convolution operation |
| coordination graph | 547 | out-of-scope | multiagent research: factored coordination (DM §27.?); RO #214 teaches CTDE and value factorisation |
| correlated equilibrium | 498, 501 | out-of-scope | game theory beyond Nash (DM §24.?); beyond RL #54 |
| correlated joint policy | 498 | out-of-scope | game theory beyond Nash (DM §24.?); beyond RL #54 |
| cost-sensitive classification | 373 | out-of-scope | research reduction of imitation to classification (DM §18.?) |
| countable additivity | 561 | taught | MA-011 (axioms of probability) |
| covariance matrix | 28 | taught | MA-009; MA-073 (multivariate normal) |
| Coxeter-Freudenthal-Kuhn triangulation | 168 | out-of-scope | interpolation-grid detail (DM §8.5) |
| cross entropy | 219, 566 | taught | ML-072 Log loss; DL-014 (cross-entropy loss) |
| cross entropy method | 218 | taught | RL #43 Black-box policy search (CEM) |
| crying baby problem | 382, 615 | out-of-scope | book's test problem (DM appendix F) |
| cumulative distribution function | 21 | taught | MA-021, MA-022 (CDF) |
| cycle | 572 | add | graph basics: directed and undirected graphs, paths, cycles, DAGs, trees (parent, child) [maths] -> RO-05, short section in Note #103 Graphs and uninformed search. Note #103 lists 'graph as a model of a state space' only; Bayes nets, factor graphs (RO #263), roadmaps and search trees all need this vocabulary (DM appendix A, OPT §19) |
| d-separation | 35 | out-of-scope | graph test for independence in Bayesian networks (DM §2.6); beyond the beginner Bayesian-network add |
| DAgger | see data set aggregation | index-noise | cross-reference to "data set aggregation" |
| data imputation | 84 | taught | ML-035 to ML-039 (imputation) |
| data set aggregation | 358 | taught | RO #165 (DAgger) |
| Dec-MDP | see decentralized Markov decision process | index-noise | cross-reference to "decentralized Markov decision process" |
| Dec-POMDP | see decentralized partially observable Markov decision process | index-noise | cross-reference to "decentralized partially observable Markov decision process" |
| decay factor | 567 | taught | RL #3 (decaying step sizes); DL-032 (learning-rate decay) [hand-checked] |
| decaying step factor | 567 | taught | RL #3 (decaying step sizes) [hand-checked] |
| decentralized Markov decision process | 546 | out-of-scope | multiagent research model (DM ch.27); RO #214 teaches CTDE |
| decentralized partially observable Markov decision process | 16, 545 | add | Dec-POMDP: the formal model of cooperative multi-robot RL [RL] -> RO-16 Note #214 Multi-agent RL: CTDE (short section). CTDE methods (MAPPO, value factorisation) are defined on a Dec-POMDP; DM ch.27 |
| decision network | 116 | out-of-scope | decision-network notation (DM §6.5) |
| decision networks | 14 | out-of-scope | decision-network notation (DM §6.5) |
| decision theory | 111 | taught | RL #53 Decisions against nature |
| decision tree | 25 | taught | ML-091 Decision trees |
| decoder | 593 | taught | DL-068 Encoder-decoder |
| deep learning | 581 | taught | DL-002 What is deep learning |
| deep neural network | 582 | taught | DL-002 What is deep learning |
| deep reinforcement learning | 344 | taught | RL #35 Deep Q-networks (RL-05) [hand-checked] |
| depth-first search | 183 | taught | RO #103 Graphs and uninformed search |
| depth of rationality | 504 | out-of-scope | game theory: level-k reasoning (DM §24.7) |
| descriptive theory | 122 | out-of-scope | behavioural economics (DM §6.?) |
| DESPOT | see Determinized Sparse Partially Observable Tree | index-noise | cross-reference to "Determinized Sparse Partially Observable Tree" |
| deterministic best response | 495 | out-of-scope | game theory beyond Nash (DM §24.?) |
| deterministic policy | 135 | taught | RL #9; RL #40 |
| deterministic policy gradient | 272 | taught | RL #40 Deterministic policy gradients: DDPG |
| deterministic variable | 32 | out-of-scope | Bayesian-network notation (DM §2.?) |
| determinized belief tree | 459 | out-of-scope | research online POMDP solver DESPOT (DM §22.6); online POMDP tree search is proposed as an add for RO #269 |
| Determinized Sparse Partially Observable Tree | 459 | out-of-scope | research online POMDP solver DESPOT (DM §22.6) |
| determinized sparse tree search | 459 | out-of-scope | research online POMDP solver DESPOT (DM §22.6) |
| determinizing matrix | 460 | out-of-scope | research online POMDP solver DESPOT (DM §22.6) |
| diagnostic test | 121 | out-of-scope | book example (DM §6.?); Bayes' theorem is MA-018 |
| dictionary | 637 | index-noise | Julia language feature (DM appendix G) |
| differential entropy | 566 | taught | ML-091 (differential entropy, glossary) |
| diminishing marginal utility | 115 | out-of-scope | economics (utility theory detail, DM §6.?) |
| directed acyclic graph | 32 | taught | RO #103 (graph vocabulary); DL-054 (DAG of layers) |
| directed acyclic graph pattern | 104 | out-of-scope | Bayesian-network structure learning (DM §5.?) |
| directed exploration | 303 | taught | RL #4 (UCB as directed exploration) [hand-checked] |
| directed graph | 572 | add | graph basics: directed and undirected graphs, paths, cycles, DAGs, trees (parent, child) [maths] -> RO-05, short section in Note #103 Graphs and uninformed search. Note #103 lists 'graph as a model of a state space' only; Bayes nets, factor graphs (RO #263), roadmaps and search trees all need this vocabulary (DM appendix A, OPT §19) |
| directed graph search | 99 | out-of-scope | Bayesian-network structure learning (DM §5.?) |
| directed path | 572 | add | graph basics: directed and undirected graphs, paths, cycles, DAGs, trees (parent, child) [maths] -> RO-05, short section in Note #103 Graphs and uninformed search. Note #103 lists 'graph as a model of a state space' only; Bayes nets, factor graphs (RO #263), roadmaps and search trees all need this vocabulary (DM appendix A, OPT §19) |
| direct sampling | 54 | out-of-scope | Bayesian-network sampling method (DM §3.?); no plan Note samples a Bayesian network |
| Dirichlet distribution | 80 | add | Bayesian parameter learning: Beta and Dirichlet priors, conjugate updates [maths] -> MA 08-likelihood, new Note after MA-072. Dirichlet is the prior for learned transition probabilities in model-based RL (DM §16.?) |
| discounted return | 135 | taught | RL #8 Return and discounting |
| discounted visitation distribution | 256 | taught | RL #38 (state distribution in the policy objective); RL #30 [hand-checked] |
| discount factor | 135 | taught | RL #8 Return and discounting |
| discrete probability distribution | 20 | taught | MA-021 PMF and discrete CDF |
| discrete state filter | 381 | taught | RO #79 Grid filters: histogram filter [hand-checked] |
| discrete-time Riccati equation | 150 | taught | RO #205 LQR; robotics.md §4 "Discrete Riccati recursion" |
| discriminator | 369, 597 | taught | RB #318 GAIL; robotics.md §4 new DL "Generative adversarial networks" |
| dispatch | 642 | index-noise | Julia language feature (DM appendix G) |
| distance metric | 163, 562 | taught | RO #108 (metric space) |
| dominant strategy | 497 | out-of-scope | game theory beyond Nash (DM §24.2); RL #54 teaches Nash and minimax only |
| dominant strategy equilibrium | 497 | out-of-scope | game theory beyond Nash (DM §24.2); RL #54 teaches Nash and minimax only |
| dominate | 291, 478 | taught | RL #53 (Pareto-optimal plans) |
| dominated | 412 | taught | RO #268 (pruning dominated alpha vectors) [hand-checked] |
| double progressive widening | 197 | out-of-scope | research extension of MCTS to continuous spaces (DM §9.6) |
| double Q-learning | 338 | taught | RL #22 Double Q-learning |
| Dyna | 318 | taught | RL #45 Models and Dyna |
| dynamic programming | 136, 549, 604 | taught | RL-02 (#12-#15) [hand-checked] |
| E-step | see expectation step | index-noise | cross-reference to "expectation step" |
| edge | 572 | add | graph basics: directed and undirected graphs, paths, cycles, DAGs, trees (parent, child) [maths] -> RO-05, short section in Note #103 Graphs and uninformed search. Note #103 lists 'graph as a model of a state space' only; Bayes nets, factor graphs (RO #263), roadmaps and search trees all need this vocabulary (DM appendix A, OPT §19) |
| e-greedy exploration | 303 | taught | RL #2 Multi-armed bandits and epsilon-greedy [hand-checked] |
| EKF | see extended Kalman filter | index-noise | cross-reference to "extended Kalman filter" |
| eligibility traces | 341 | taught | RL #24 Eligibility traces and TD(lambda) |
| elite sample | 218 | taught | RL #43 (cross-entropy method elite samples) [hand-checked] |
| EM | see expectation-maximization | index-noise | cross-reference to "expectation-maximization" |
| embedding | 592 | taught | DL-057 (embedding, glossary) |
| encoder | 593 | taught | DL-068 Encoder-decoder |
| entropy | 365, 566 | taught | ML-091 (entropy, glossary) |
| essential graph | 104 | out-of-scope | Bayesian-network structure learning (DM §5.?) |
| Euclidean norm | 563 | taught | MA-049 Magnitude and distance |
| evaluation model | 289 | out-of-scope | validation-chapter term (DM §14.1) |
| event space | 562 | taught | MA-010 Events and types of events |
| evidence | 29 | taught | MA-018 Bayes' theorem (evidence) |
| evidence variables | 43 | taught | MA-018 (evidence); RO #78 |
| expectation-maximization | 87 | taught | MA-074 Expectation maximization |
| expectation step | 87 | taught | MA-074 Expectation maximization |
| expected utility | 116 | taught | RL #53 (utility theory) |
| experience replay | 345 | taught | RL #36 Experience replay and target networks |
| explaining away | 36 | out-of-scope | Bayesian-network reasoning pattern (DM §2.6); beyond the beginner Bayesian-network add |
| exploding gradient | 590 | taught | DL-018 Vanishing and exploding gradients |
| exploitation | 299 | taught | RL #1 The reinforcement learning problem |
| exploration | 299 | taught | RL #1 The reinforcement learning problem |
| exploration bonus | 189 | taught | RL #45 (Dyna-Q+ bonus); RO #182 |
| exploratory belief expansion | 440 | out-of-scope | point-based POMDP solver detail (DM §21.?); research-level |
| explore-then-commit exploration | 303 | add | Thompson sampling (posterior sampling) [RL] -> RL-01 Note #4 Exploring smartly (section after UCB). explore-then-commit is the simplest baseline beside Thompson and UCB (DM §15.?); one line in the same section |
| exponential distribution | 38, 92 | taught | MA-071 MLE for common distributions (exponential) |
| exponentially weighted average | 270 | taught | DL-033 Exponentially weighted moving average |
| exponential utility | 115 | out-of-scope | economics (utility functions, DM §6.?) |
| extended Kalman filter | 385 | taught | RO #81 Extended Kalman filter |
| factor | 25 | taught | RO #263 Factor graphs |
| factor conditioning | 44 | out-of-scope | table operations for exact inference in discrete Bayesian networks (DM §3.1); marginalising and conditioning themselves are MA-014/MA-015 |
| factored Dec-POMDP | 546 | out-of-scope | multiagent research model (DM ch.27) |
| factor marginalization | 44 | out-of-scope | table operations for exact inference in discrete Bayesian networks (DM §3.1); marginalising itself is MA-014 |
| factor product | 44 | out-of-scope | table operations for exact inference in discrete Bayesian networks (DM §3.1) |
| fast informed bound | 429 | out-of-scope | value-function bound for POMDP solvers (DM §21.?); research-level |
| feature | 587 | taught | ML-022 Feature engineering |
| feature expectations | 364 | add | apprenticeship learning: max-margin IRL by matching feature expectations [RL] -> RO-13 Note #189 Inverse RL (section before max-entropy IRL). DM §18.? teaches it first; the classic robot IRL (helicopter aerobatics, Abbeel & Ng 2004) |
| features | 172 | taught | RL #26 Linear value functions and features |
| feedforward network | 582 | taught | DL-010 Forward propagation [hand-checked] |
| fictitious play | 505, 521 | out-of-scope | game theory learning dynamics (DM §25.?) |
| finite difference | 231 | taught | MA-061 (finite differences); RL #43 |
| finite horizon | 134 | taught | RL #8 (horizon) |
| finite state controller | 471 | out-of-scope | POMDP policy representation (DM ch.23); research-level; robot state machines are RO #130 |
| first fundamental theorem of calculus | 568 | add | integrals and the fundamental theorem of calculus [maths] -> MA 06-calculus, new Note after MA-062 (before the planned ODEs Note). MA has no Note on integration; dead reckoning (RO #84), probabilities from PDFs (MA-022), LQR and trajectory cost integrals (RO #205, #116) all integrate |
| Fisher information matrix | 254 | taught | RL #38 TRPO; robotics.md §4 "Natural gradient and Fisher information" [hand-checked] |
| fitting | see learning | index-noise | cross-reference to "learning" |
| forward difference | 234 | taught | MA-061 (finite differences) |
| forward search | 183, 600 | taught | RL #47 Decision-time planning and rollouts [hand-checked] |
| framing effect | 122, 124 | out-of-scope | behavioural economics (DM §6.?) |
| Freudenthal triangulation | 445 | out-of-scope | interpolation-grid detail (DM §8.5, §20.?) |
| function | 640 | index-noise | Julia language feature (DM appendix G) |
| functional edge | 118 | out-of-scope | decision-network notation (DM §6.5) |
| GAIL | see generative adversarial imitation learning | index-noise | cross-reference to "generative adversarial imitation learning" |
| game theory | 493 | taught | RL #54 Games: minimax, alpha-beta and equilibria (optional) [hand-checked] |
| gamma function | 78 | out-of-scope | special function used only in the Beta/Dirichlet normaliser (DM §4.2); proof-level |
| gap heuristic search | 460 | out-of-scope | research online POMDP solver (DM §22.?) |
| gated recurrent units | 592 | taught | DL-064 GRU |
| Gauss-Seidel value iteration | 145 | out-of-scope | value-iteration variant (DM §7.6); asynchronous DP is RL #15 |
| Gaussian distribution | 22 | taught | MA-024 Normal distribution |
| Gaussian kernel | 165 | taught | ML-089 Kernel trick (Gaussian/RBF kernel); RL #26 (RBF features) |
| Gaussian mixture model | 23 | taught | MA-073 Gaussian mixture models |
| generalized advantage estimation | 269 | taught | RL #34 Advantage and generalized advantage estimation |
| generalized infinitesimal gradient ascent | 509 | out-of-scope | game-theory learning dynamics (DM §25.?) |
| generations | 218 | add | genetic algorithms and population methods (selection, crossover, mutation) [maths] -> MA 07-optimisation, new Note after MA-068. DM §10.? and OPT ch.9 teach them; RL #43 lists ES/CMA-ES but not GAs; used for gait and morphology search |
| generative adversarial imitation learning | 369 | taught | RB #318 Adversarial imitation: GAIL [hand-checked] |
| generative model | 183, 593 | taught | robotics.md §4 new DL chapter "Generative models"; RL #45 (sample models) |
| generator | 597 | taught | robotics.md §4 new DL "Generative adversarial networks" |
| genetic algorithm | 103, 215 | add | genetic algorithms and population methods (selection, crossover, mutation) [maths] -> MA 07-optimisation, new Note after MA-068. DM §10.4 uses them for policy search |
| genetic local search | 103 | out-of-scope | hybrid of GA and local search (DM §10.4); research-level variant of the GA add |
| Gibbs sampling | 60 | out-of-scope | MCMC detail (DM §3.?); no plan Note samples by Markov chains |
| GIGA | see generalized infinitesimal gradient ascent | index-noise | cross-reference to "generalized infinitesimal gradient ascent" |
| Gittins allocation index | 309 | out-of-scope | Bayes-optimal bandit index (DM §15.?); intractable in general |
| global approximation | 163 | taught | RL #25 (global approximators such as linear and neural) [hand-checked] |
| gradient ascent | 249, 509, 526, 567 | taught | MA-062 (gradient); ML-056 Gradient descent |
| gradient clipping | 250 | taught | DL-018 (gradient clipping) |
| gradient scaling | 250 | out-of-scope | implementation detail of policy-gradient steps (DM §12.?) |
| graph | 572 | taught | RO #103 Graphs and uninformed search |
| greedy action | 301 | taught | RL #2 (greedy action) |
| greedy envelope | 200 | out-of-scope | research online-planning detail (DM §9.?) |
| greedy policy | 139 | taught | RL #11 (optimal policy is greedy w.r.t. q*) |
| GRU | see gated recurrent units | index-noise | cross-reference to "gated recurrent units" |
| hall problem | 610 | out-of-scope | book's test problem (DM appendix F) |
| halting problem | 579 | out-of-scope | computability theory (DM §C.?) |
| heuristic | 197 | taught | RO #105 A* and heuristics |
| heuristic search | 197, 550, 604 | taught | RL #47 (decision-time planning with heuristic search) |
| heuristic search value iteration | 442 | out-of-scope | research POMDP solver HSVI (DM §21.?) |
| hex world problem | 609 | out-of-scope | book's test problem (DM appendix F) |
| hidden variables | 43 | taught | MA-074 Expectation maximization (hidden/latent variables) |
| hierarchical softmax | 504 | out-of-scope | game-theory model of bounded rationality (DM §24.7) |
| hill climbing | 100 | add | local search: hill climbing, pattern search and simulated annealing [maths] -> MA 07-optimisation, new Note after MA-068. DM §10.2 starts policy search with it; OPT ch.7 teaches derivative-free direct methods; RL #43 lists only ES/CEM |
| hindsight optimization | 207 | out-of-scope | research planning variant (DM §9.?) |
| history | 135, 457 | taught | RO #77 (information state: history of actions and readings); RO #162 History encoders |
| history tree | 459 | out-of-scope | research online POMDP solver detail (DM §22.?) |
| Hooke-Jeeves method | 215 | add | local search: hill climbing, pattern search and simulated annealing [maths] -> MA 07-optimisation, new Note after MA-068. DM §10.2 policy search; OPT §7.4 |
| HSVI | see heuristic search value iteration | index-noise | cross-reference to "heuristic search value iteration" |
| hybrid planning | 185 | out-of-scope | research planning variant (DM §9.?) |
| I-POMDP | see Interactive POMDP | index-noise | cross-reference to "Interactive POMDP" |
| identity of indiscernibles | 562 | out-of-scope | metric axiom (DM §A.3); RO #108 teaches the rules a distance must follow |
| imitation learning | 355 | taught | RO #165 Behaviour cloning; RB-08 Imitation learning for manipulation [hand-checked] |
| immoral v-structures | 104 | out-of-scope | Bayesian-network structure learning (DM §5.?) |
| importance sampling | 256, 287, 570 | taught | RL #18; robotics.md §4 new MA "Importance sampling" |
| incomplete | 82 | out-of-scope | missing-data terminology (DM §4.4); imputation is ML-034 to ML-039 |
| incremental estimation | 335 | taught | RL #3 Incremental updates and step sizes [hand-checked] |
| independent | 25 | taught | MA-016 Independent events |
| independently and identically distributed | 71 | taught | MA-033 Sampling distribution and CLT (i.i.d., glossary G-933) [hand-checked] |
| independent parameter | 21 | out-of-scope | Bayesian-network parameter-count notation (DM §2.?) |
| inference | 43 | taught | MA-018 Bayes' theorem (inference from evidence) [hand-checked] |
| infinite horizon | 134 | taught | RL #8 (infinite horizon) |
| infinitesimal gradient ascent | 509 | out-of-scope | game-theory learning dynamics (DM §25.?) |
| influence diagram | see decision network | index-noise | cross-reference to "decision network" |
| informational edge | 118 | out-of-scope | decision-network notation (DM §6.5) |
| information content | 565 | taught | ML-091 (information, entropy) |
| information-gathering | 429 | taught | RO #180 Exploration by information gain [hand-checked] |
| informed search | 604 | taught | RO #105 A* and heuristics [hand-checked] |
| initial state distribution | 213, 282 | taught | RL #7 Markov decision processes [hand-checked] |
| interaction uncertainty | 2 | out-of-scope | chapter framing of uncertainty sources (DM §1.?) |
| Interactive POMDP | 534 | out-of-scope | research multiagent model (DM §26.?) |
| interval estimation | see quantile exploration | index-noise | cross-reference to "quantile exploration" |
| interval exploration | see quantile exploration | index-noise | cross-reference to "quantile exploration" |
| inverse cumulative distribution function | see quantile function | index-noise | cross-reference to "quantile function" |
| inverse reinforcement learning | 361 | taught | RO #189 Inverse RL [hand-checked] |
| isotropic Gaussian | 224 | taught | RL #43 (evolution strategies sample from an isotropic Gaussian) [hand-checked] |
| iterated ascent | 249 | out-of-scope | optimisation detail inside policy-gradient update (DM §12.?) |
| iterated best response | 503, 550 | out-of-scope | game theory (DM §24.?, §27.?) |
| JESP | see joint equilibrium-based search for policies | index-noise | cross-reference to "joint equilibrium-based search for policies" |
| joint action | 493 | taught | RO #214 Multi-agent RL (joint actions) [hand-checked] |
| joint action space | 493 | taught | RO #214 Multi-agent RL [hand-checked] |
| joint distribution | 24 | taught | MA-014 Joint, marginal and conditional probability |
| joint equilibrium-based search for policies | 550 | out-of-scope | research Dec-POMDP solver (DM §27.?) |
| joint full observability | 546 | out-of-scope | research multiagent model property (DM §27.?) |
| joint observation | 533 | taught | RO #214 Multi-agent RL (each agent's observation) [hand-checked] |
| joint observation space | 533 | taught | RO #214 Multi-agent RL [hand-checked] |
| joint policy | 494 | taught | RO #214 Multi-agent RL (shared policies) |
| joint reward | 493 | taught | RO #214 Multi-agent RL [hand-checked] |
| joint reward function | 493 | taught | RO #214 Multi-agent RL [hand-checked] |
| junction tree algorithm | 53 | out-of-scope | exact graphical-model inference (DM §3.?) |
| k-nearest neighbors | 163 | taught | ML-085 KNN |
| K2 | 100 | out-of-scope | Bayesian-network structure learning (DM §5.?) |
| Kalman filter | 383 | taught | RO #80 Kalman filter |
| Kalman gain | 385 | taught | RO #80 Kalman filter (Kalman gain) |
| kernel | 587 | taught | ML-089 Kernel trick; DL-042 (convolution kernel) |
| kernel density estimation | 82 | taught | MA-023 Density estimation (KDE) |
| kernel function | 82, 164 | taught | MA-023 Density estimation (KDE) |
| kernel smoothing | 164 | taught | MA-023 (kernel-weighted averaging); RL #51 (kernel-based value approximation) |
| keyword argument | 641 | index-noise | Julia language feature (DM appendix G) |
| Kolmorogov axioms | 562 | taught | MA-011 (axioms of probability) |
| Kronecker delta function | 329 | index-noise | notation (DM §16.?) |
| Kullback-Leibler divergence | 253 | taught | robotics.md §4 new MA "KL divergence"; DL-014 (KL) |
| labeled heuristic search | 197 | out-of-scope | research planning variant (DM §9.?) |
| landmark | 380 | taught | RO #71 Maps and landmarks |
| Laplace distribution | 91 | out-of-scope | distribution used only for a data example (DM §4.?) |
| latent space | 592 | taught | DL-068 (latent representation); robotics.md §4 new DL "Variational autoencoder" [hand-checked] |
| latent variables | 87 | taught | MA-074 Expectation maximization (latent variables) |
| law of total probability | 24 | taught | MA-019 (law of total probability, recap robotics.md §5) |
| learning | 71 | taught | ML-001 What is ML |
| learning curve | 337 | taught | DL-022 Early stopping (learning curves) |
| learning rate | 336, 567 | taught | ML-056 Gradient descent (learning rate) |
| likelihood ratio | 234 | taught | RL #30 (log-derivative / likelihood-ratio trick) [hand-checked] |
| likelihood weighted sampling | 57 | out-of-scope | Bayesian-network sampling method (DM §3.?) |
| linear combination | 575 | taught | MA-052 Linear combinations, span and basis |
| linear dynamics | 148 | taught | robotics.md §4 new MA "State-space models" (x_dot = Ax + Bu) |
| linear function approximation | 163 | taught | RL #26 Linear value functions and features [hand-checked] |
| linear Gaussian | 31 | taught | RO #80 Kalman filter (linear Gaussian system) |
| linear interpolation | 167 | add | linear, bilinear and multilinear interpolation on a grid [maths] -> RO-05, short section in Note #106 Grid path planning (which uses DP with interpolation). DM §8.5; also used for image undistortion (RO #89) and grid maps; no Note teaches interpolation |
| linearity of expectation | 242 | taught | MA-012 Expected value and variance |
| linearization | 386 | taught | RO #81 Extended Kalman filter (linearisation); MA-064 |
| linear program | 147 | taught | MA-068 Linear and quadratic programming |
| linear quadratic Gaussian | 419 | add | LQG: LQR plus a Kalman filter (separation principle) [control] -> RO-15, short section in Note #205 LQR (or #206). DM §7.8 and §19.? pair LQR with Kalman estimation; standard in control courses; plan has LQR (#205) and KF (#80) but never joins them |
| linear quadratic regulator | 148 | taught | RO #205 LQR: the linear-quadratic regulator |
| linear regression | 172, 234 | taught | ML-049, ML-052 Linear regression |
| line search | 254 | add | line search and one-dimensional minimisation (bracketing, golden section, backtracking, Wolfe conditions) [maths] -> MA 07-optimisation, new Note (MA-064 only says "usually shortened by a line search"). DM §12.? and OPT ch.4 use it; TRPO's step (RL #38) and SQP solvers (RO #208) do a backtracking line search |
| literals | 53 | out-of-scope | propositional logic notation (DM §C.4) |
| local approximation | 163 | taught | RL #51 (memory-based local approximation; optional) [hand-checked] |
| locally optimal | 250 | taught | MA-065 (local vs global minima) |
| local optima | 102 | taught | MA-065 (local vs global minima) |
| local search | 100, 215 | add | local search: hill climbing, pattern search and simulated annealing [maths] -> MA 07-optimisation, new Note after MA-068. DM §10.2; OPT ch.7 |
| logarithmic utility | 115 | out-of-scope | economics (utility functions, DM §6.?) |
| log derivative trick | 221 | taught | RL #30 (log-derivative trick) |
| logical conjunction | 53 | out-of-scope | propositional logic notation (DM §C.4) |
| logical disjunction | 53 | out-of-scope | propositional logic notation (DM §C.4) |
| logical negation | 53 | out-of-scope | propositional logic notation (DM §C.4) |
| logit-level-k | see hierarchical softmax | index-noise | cross-reference to "hierarchical softmax" |
| logit model | 32 | taught | ML-116 (log-odds); ML-071 Sigmoid |
| logit response | see softmax response | index-noise | cross-reference to "softmax response" |
| log-likelihood | 72 | taught | MA-070 Maximum likelihood estimation (log-likelihood) |
| long short-term memory | 592 | taught | DL-061 LSTM |
| lookahead | 136 | taught | RL #47 Decision-time planning [hand-checked] |
| loop | 644 | index-noise | Julia language feature (DM appendix G) |
| loopy belief propagation | 53 | out-of-scope | approximate graphical-model inference (DM §3.?) |
| loss function | 581 | taught | DL-014 Loss functions |
| lottery | 112 | out-of-scope | utility-theory construct (DM §6.1); utility theory is RL #53 |
| LQG | see linear quadratic Gaussian | index-noise | cross-reference to "linear quadratic Gaussian" |
| LQR | see linear quadratic regulator | index-noise | cross-reference to "linear quadratic regulator" |
| LSTM | see long short-term memory | index-noise | cross-reference to "long short-term memory" |
| M-step | see maximization step | index-noise | cross-reference to "maximization step" |
| machine learning | 71 | taught | ML-001 What is ML |
| machine replacement problem | 617 | out-of-scope | book's test problem (DM appendix F) |
| margin | 365 | taught | ML-086 SVM (margin) |
| marginal | 24 | taught | MA-014 (marginal probability) |
| marginalization | 44 | taught | MA-014 (marginalising) |
| marginal mode | 85 | out-of-scope | Bayesian-network learning detail (DM §4.?) |
| Markov assumption | 133 | taught | robotics.md §4 new MA "Markov chains" (Markov assumption) |
| Markov chain Monte Carlo | 60 | out-of-scope | MCMC (DM §3.?); no plan Note samples by Markov chains; particle methods (RO #82) cover robot sampling |
| Markov decision process | 14, 131, 133 | taught | RL #7 Markov decision processes |
| Markov equivalence class | 104 | out-of-scope | Bayesian-network structure learning (DM §5.?) |
| Markov equivalent | 104 | out-of-scope | Bayesian-network structure learning (DM §5.?) |
| Markov game | 16, 517 | add | Markov (stochastic) games [RL] -> RO-16, short section in Note #214 Multi-agent RL. the model behind multi-robot and self-play RL (DM ch.25); RL #54 covers sequential games on state spaces only by name |
| matrix | 633 | taught | MA-053 Linear transformations and matrices |
| matrix games | see normal form games | index-noise | cross-reference to "normal form games" |
| maximization step | 87 | taught | MA-074 Expectation maximization (M-step) |
| maximum a posteriori | 77 | add | maximum a posteriori (MAP) estimation [maths] -> MA 08-likelihood, short section after MA-070. DM §4.2; RO #260 uses "MAP estimate of a whole map" and RO #101 a negative log posterior without a Note that teaches MAP |
| maximum entropy inverse reinforcement learning | 365 | taught | RO #189 Inverse RL (max-entropy IRL) |
| maximum likelihood estimate | 71, 317 | taught | MA-070 Maximum likelihood estimation |
| maximum likelihood parameter learning | 71 | taught | MA-070 Maximum likelihood estimation |
| maximum margin inverse reinforcement learning | 361 | add | apprenticeship learning: max-margin IRL by matching feature expectations [RL] -> RO-13 Note #189 Inverse RL (section before max-entropy IRL). DM §18.?; Abbeel & Ng 2004 |
| max norm | 563 | add | vector norms L1, L2 and L-infinity (Manhattan, Euclidean, Chebyshev) [maths] -> MA 05-linear-algebra, short section in MA-049. max norm bounds the VI error (DM §A.3) |
| MBDP | see memory-bounded dynamic programming | index-noise | cross-reference to "memory-bounded dynamic programming" |
| MDP | see Markov decision process, see Markov decision process, see Markov decision process | index-noise | cross-reference to "Markov decision process" |
| mean vector | 28 | taught | MA-073 (multivariate normal: mean vector) |
| measurable set | 561 | out-of-scope | measure theory (DM §A.?), proof-level |
| measure | 561 | out-of-scope | measure theory (DM §A.?), proof-level |
| measure space | 561 | out-of-scope | measure theory (DM §A.?), proof-level |
| memetic algorithms | 103 | out-of-scope | research variant of genetic algorithms (DM §10.?) |
| memoization | 604 | taught | DL-019 MLP memoization |
| memory | 589 | taught | RO #162 History encoders (memory) |
| memory-bounded dynamic programming | 550 | out-of-scope | research Dec-POMDP solver (DM §27.?) |
| metric | 562 | taught | RO #108 (metric space) |
| metric space | 562 | taught | RO #108 (metric space) |
| MG | see Markov game | index-noise | cross-reference to "Markov game" |
| minimax | 204 | taught | RL #54 Games: minimax |
| mirrored sampling | 224 | out-of-scope | variance-reduction detail inside evolution strategies (DM §10.?) |
| missing | 82 | out-of-scope | missing-data terminology (DM §4.4); imputation is ML-034 to ML-039 |
| missing at random | 84 | taught | ML-037 Missing indicator (missing at random) |
| missingness mechanisms | 84 | taught | ML-034 Complete case analysis (missingness mechanisms) [hand-checked] |
| mixed strategy | 494 | taught | RL #54 (mixed strategies) |
| mixture model | 23 | taught | MA-073 Gaussian mixture models |
| MMA ∗ | see multiagent A ∗ | index-noise | cross-reference to "multiagent A*" |
| MMDP | see multiagent MDP | index-noise | cross-reference to "multiagent MDP" |
| mode | 77 | taught | MA-005 Measures of central tendency (mode) |
| model-free reinforcement learning | 335 | taught | RL-03 (#16-#24; model-free learning) [hand-checked] |
| model predictive control | 200 | taught | RO #207 Model predictive control |
| model uncertainty | 2 | out-of-scope | chapter framing of uncertainty sources (DM §1.?) |
| modified policy iteration | 141 | out-of-scope | DP variant (DM §7.?); policy iteration is RL #13 |
| Monte Carlo estimation | 569 | taught | robotics.md §4 new MA "Monte Carlo estimation" |
| Monte Carlo methods | 11, 54 | taught | RL #16 Monte Carlo prediction [hand-checked] |
| Monte Carlo policy evaluation | 214 | taught | RL #16 Monte Carlo prediction [hand-checked] |
| Monte Carlo tree search | 187, 457 | taught | RL #48 Monte Carlo tree search |
| Monte Carlo value iteration | 475 | out-of-scope | research POMDP solver (DM §23.?) |
| most likely failure | 293 | add | falsification: searching for the disturbances that make a policy fail (adversarial stress testing) [robotics] -> RO-20, section in Note #249 Evaluating driving (scenario-based testing). DM ch.14; RO #248-#249 list scenario testing and safety cases but not the search for failures |
| mountain car problem | 612 | taught | RL #27 (mountain car) |
| MPOMDP | see multiagent POMDP | index-noise | cross-reference to "multiagent POMDP" |
| multiagent A ∗ | 550 | out-of-scope | research multiagent planner (DM §27.?) |
| multiagent MDP | 548 | out-of-scope | research multiagent model (DM §27.?); RO #214 teaches CTDE |
| multiagent POMDP | 548 | out-of-scope | research multiagent model (DM §27.?) |
| multiarmed bandit problem | 299 | taught | RL #2 Multi-armed bandits [hand-checked] |
| multicaregiver crying baby problem | 624 | out-of-scope | book's test problem (DM appendix F) |
| multiforecast model predictive control | 207 | out-of-scope | research MPC variant (DM §9.9) |
| multilinear interpolation | 168 | add | linear, bilinear and multilinear interpolation on a grid [maths] -> RO-05, short section in Note #106 Grid path planning (which uses DP with interpolation). DM §8.5; also used for image undistortion (RO #89) and grid maps; no Note teaches interpolation |
| multimodal | 23 | taught | MA-073 Gaussian mixture models (multimodal) |
| multivariate | 573 | taught | MA-073 (multivariate normal) |
| multivariate distribution | 24 | taught | MA-073 (multivariate normal) |
| multivariate Gaussian distribution | 28 | taught | MA-073 (multivariate normal, recap robotics.md §5) |
| multivariate Gaussian mixture models | 28 | taught | MA-073 Gaussian mixture models |
| multivariate product distribution | 27 | out-of-scope | Bayesian-network notation (DM §2.?) |
| multivariate uniform distribution | 27 | add | multivariate uniform distribution (uniform over a box) [maths] -> MA 03-distributions, short section in MA-029. DM §2.3; sampling planners draw uniform samples over a box of C-space (RO #110, #111) |
| mutate | 631 | index-noise | Julia language feature (DM appendix G) |
| naive Bayes | 48 | taught | ML-081 Naive Bayes |
| named function | 640 | index-noise | Julia language feature (DM appendix G) |
| named tuple | 637 | index-noise | Julia language feature (DM appendix G) |
| Nash equilibrium | 498, 537 | taught | RL #54 (Nash equilibrium) |
| Nash Q-learning | 526 | out-of-scope | research multiagent RL algorithm (DM §25.?) |
| nat | 566 | out-of-scope | unit name (information in natural-log units, DM §A.?); entropy itself is ML-091 |
| natural | 566 | out-of-scope | unit name (information in natural-log units, DM §A.?); entropy itself is ML-091 |
| natural evolution strategies | 219 | out-of-scope | research variant of evolution strategies (DM §10.?); RL #43 teaches ES |
| natural gradient | 253 | taught | RL #38; robotics.md §4 "Natural gradient and Fisher information" |
| ND-POMDP | see network distributed partially observable Markov decision process | index-noise | cross-reference to "network distributed POMDP" |
| nearest neighbor | 163 | taught | ML-085 KNN |
| nearest-neighbor imputation | 85 | taught | ML-038 KNN imputer |
| neighbor | 572 | add | graph basics: directed and undirected graphs, paths, cycles, DAGs, trees (parent, child) [maths] -> RO-05, short section in Note #103 Graphs and uninformed search. Note #103 lists 'graph as a model of a state space' only; Bayes nets, factor graphs (RO #263), roadmaps and search trees all need this vocabulary (DM appendix A, OPT §19) |
| network distributed partially observable Markov decision process | 547 | out-of-scope | research multiagent model (DM §27.?) |
| neural network | 174, 581 | taught | DL-010 Forward propagation |
| neural network regression | 174 | taught | DL-013 graduate-admission ANN (regression) |
| NEXP-complete | 546 | out-of-scope | complexity class (DM §27.?) |
| NLP | see nonlinear programming | index-noise | cross-reference to "nonlinear programming" |
| node | 471, 572 | add | graph basics: directed and undirected graphs, paths, cycles, DAGs, trees (parent, child) [maths] -> RO-05, short section in Note #103 Graphs and uninformed search. Note #103 lists 'graph as a model of a state space' only; Bayes nets, factor graphs (RO #263), roadmaps and search trees all need this vocabulary (DM appendix A, OPT §19) |
| nonlinear programming | 478, 551 | taught | RO #208 (Newton-type solvers SQP, interior point); MA-066 |
| nonnegativity | 561 | taught | MA-011 (axioms of probability) |
| nonparametric | 82, 379 | taught | MA-023 (nonparametric density estimation); RO #82 (particles) |
| nonstationary Markov policy | 530 | out-of-scope | game theory: policy classes in Markov games (DM Ex. 25.3) |
| normal distribution | see Gaussian distribution | index-noise | cross-reference to "Gaussian distribution" |
| normal form games | 493 | taught | RL #54 (matrix games) [hand-checked] |
| normalization constant | 49 | taught | ML-082 (normalising constant, recap robotics.md §5) [hand-checked] |
| normalized utility function | 113 | out-of-scope | utility-theory detail (DM §6.?) |
| normative theory | 122 | out-of-scope | decision-theory philosophy (DM §6.?) |
| normed vector space | 562 | out-of-scope | abstract algebra (DM §A.?), proof-level |
| NP-complete | 577 | taught | RO #103 (NP-hard) |
| NP-hard | 52, 577 | taught | RO #103 (NP-hard) |
| NP | 577 | taught | RO #103 (complexity classes) |
| observation | 1, 379 | taught | RO #63 (state, controls and measurements) |
| observation independence | 547 | out-of-scope | research multiagent model property (DM §27.?) |
| observation space | 380 | taught | RO #153 POMDPs (observations) |
| observe-act cycle | 1 | taught | RL #7 (agent-environment interface per time step) |
| observe-act loop | see observe-act cycle | index-noise | cross-reference to "observe-act cycle" |
| off-policy | 340 | taught | RL #18 (on-policy vs off-policy) |
| on-policy | 340 | taught | RL #18 (on-policy vs off-policy) |
| one-armed bandit | 299 | taught | RL #2 Multi-armed bandits [hand-checked] |
| one-step lookahead | 412 | taught | RL #47 Decision-time planning [hand-checked] |
| online planning | 181 | taught | RL #47 Decision-time planning; RO #207 (receding horizon) |
| open-loop planning | 200 | taught | RL #9 (open-loop plan vs feedback plan) |
| operations research | 12 | out-of-scope | field label (DM §1.?) |
| opportunistic | 102 | out-of-scope | search-method nickname (DM §5.?) |
| optimal policy | 136 | taught | RL #11 Optimal values and optimal policies |
| optimal substructure | 604 | taught | RL #10 (principle of optimality) |
| optimal value function | 136 | taught | RL #11 Optimal values and optimal policies |
| optimism under uncertainty | 305 | taught | RL #4 (optimistic initial values; UCB) |
| order | 575 | taught | RO #103 (Big-O order) [hand-checked] |
| outcome uncertainty | 2 | out-of-scope | chapter framing of uncertainty sources (DM §1.?) |
| overfitting | 585 | taught | ML-061 Bias-variance (overfitting) |
| P | 577 | out-of-scope | complexity class (DM §C.?); RO #103 names NP-hard |
| package | 645 | index-noise | Julia language feature (DM appendix G) |
| parameter | 21, 161 | taught | ML-001 (model parameters); MA-020 (distribution parameters) |
| parameterized policy | 213 | taught | RL #29 Parameterised policies [hand-checked] |
| parameter regularization | 585 | taught | DL-026 Regularization in DL |
| parameter tuning | 581 | taught | ML-128 Optuna (hyperparameter tuning) |
| parametric | 379 | taught | MA-070 (parametric models) |
| parametric representation | 161 | taught | RL #26 (parametric value functions) [hand-checked] |
| parametric types | 639 | index-noise | Julia language feature (DM appendix G) |
| parent | 572 | add | graph basics: directed and undirected graphs, paths, cycles, DAGs, trees (parent, child) [maths] -> RO-05, short section in Note #103 Graphs and uninformed search. Note #103 lists 'graph as a model of a state space' only; Bayes nets, factor graphs (RO #263), roadmaps and search trees all need this vocabulary (DM appendix A, OPT §19) |
| Pareto curve | see Pareto frontier | index-noise | cross-reference to "Pareto frontier" |
| Pareto efficient | see Pareto optimal | index-noise | cross-reference to "Pareto optimal" |
| Pareto frontier | 291 | taught | RL #53 (multi-objective optimisation and Pareto-optimal plans) |
| Pareto optimal | 291 | taught | RL #53 (Pareto-optimal plans) |
| partially directed graph | 104 | out-of-scope | Bayesian-network structure learning (DM §5.?) |
| partially observable Markov decision process | 15, 377 | taught | RO #153 POMDPs and belief space |
| partially observable Markov game | 16, 533 | out-of-scope | game theory under partial observability (DM ch.26) |
| Partially Observable Monte Carlo Planning | 457 | add | online POMDP planning by tree search (POMCP) [robotics] -> RO-23, section in Note #269 Approximate POMDP planning. DM §22.5; the standard online POMDP solver used on robots; RO #269 teaches QMDP, augmented MDP and MC-POMDP only |
| partially observable stochastic game | 533 | out-of-scope | game theory under partial observability (DM ch.26) |
| particle | 390 | taught | RO #82 Particle filter |
| particle deprivation | 390 | taught | RO #82 Particle filter (particle deprivation) |
| particle filter | 390 | taught | RO #82 Particle filter |
| particle filter with rejection | 390 | out-of-scope | particle-filter variant for discrete observations (DM §19.?) |
| particle injection | 394 | taught | RO #95 (augmented MCL: random particles) |
| path | 572 | add | graph basics: directed and undirected graphs, paths, cycles, DAGs, trees (parent, child) [maths] -> RO-05, short section in Note #103 Graphs and uninformed search. Note #103 lists 'graph as a model of a state space' only; Bayes nets, factor graphs (RO #263), roadmaps and search trees all need this vocabulary (DM appendix A, OPT §19) |
| performance metric | 281 | taught | RO #161 Evaluating navigation; RL #44 Reporting RL results [hand-checked] |
| piecewise-uniform density | 24 | out-of-scope | density form used in one example (DM §2.?) |
| planning | 6 | taught | RL #45 Models and Dyna (planning) |
| planning model | 289 | out-of-scope | validation-model terminology (DM §14.?) |
| point-based value iteration | 432 | add | point-based value iteration (PBVI) [robotics] -> RO-23, section in Note #268 Exact POMDP planning. DM §21.?; the standard approximate offline POMDP solver; RO #268 stops at exact alpha-vector pruning |
| pole balancing problem | 611 | out-of-scope | book's test problem (DM appendix F); cart-pole style task |
| policy | 135 | taught | RL #9 Policies, plans and value functions |
| policy evaluation | 136 | taught | RL #12 Policy evaluation |
| policy iteration | 140 | taught | RL #13 Policy improvement and policy iteration |
| policy loss | 142 | out-of-scope | bound-analysis term (DM §7.?) |
| policy search | 213 | taught | RL #29 (value-function methods vs policy search); RL #43 |
| POMCP | see Partially Observable Monte Carlo Planning | index-noise | cross-reference to "Partially Observable Monte Carlo Planning" |
| POMDP | see partially observable Markov decision process | index-noise | cross-reference to "partially observable Markov decision process" |
| POMG | see partially observable Markov game | index-noise | cross-reference to "partially observable Markov game" |
| population | 215 | taught | RL #43 (population of perturbed parameters) [hand-checked] |
| POSG | see partially observable stochastic game | index-noise | cross-reference to "partially observable stochastic game" |
| positive affine transformation | 113 | out-of-scope | utility-theory detail (DM §6.?) |
| positive definite | 28, 564 | taught | MA-064; MA-068 (positive definite) |
| positive semidefinite | 564 | taught | MA-067; MA-068 (positive semidefinite) [hand-checked] |
| posterior distribution | 43 | taught | MA-018 Bayes' theorem (posterior) |
| posterior sampling | 306, 330 | add | Thompson sampling (posterior sampling) [RL] -> RL-01 Note #4 Exploring smartly (section after UCB). DM §15.? and §16.? (posterior sampling for bandits and model-based RL) |
| potential games | 503 | out-of-scope | game theory (DM §24.?) |
| power utility | 115 | out-of-scope | economics (utility functions, DM §6.?) |
| PPAD-complete | 498 | out-of-scope | complexity class (DM §24.?) |
| PPO | see proximal policy optimization | index-noise | cross-reference to "proximal policy optimization" |
| precision parameter | 305, 497 | out-of-scope | softmax temperature in game theory/exploration (DM §15.?); temperature itself is RL #42 |
| predator-prey hex world problem | 623 | out-of-scope | book's test problem (DM appendix F) |
| predict step | 383 | taught | RO #78 The Bayes filter: predict, then update |
| preference elicitation | 114 | out-of-scope | utility elicitation (DM §6.?), economics |
| principle of maximum entropy | 368 | taught | RO #189 Inverse RL (max-entropy IRL) |
| principle of maximum expected utility | 116 | taught | RL #53 (utility theory and rationality) |
| prior | 48 | taught | MA-018 Bayes' theorem (prior) |
| prioritized sweeping | 321 | taught | RL #46 Prioritized sweeping |
| prisoner’s dilemma | 494, 621 | out-of-scope | game-theory example (DM appendix F) |
| probability axioms | 562 | taught | MA-011 (axioms of probability) |
| probability density function | 21 | taught | MA-022 PDF |
| probability distribution | 20 | taught | MA-020 Random variables and distributions |
| probability mass function | 20 | taught | MA-021 PMF |
| probability measure | 562 | out-of-scope | measure theory (DM §A.?), proof-level |
| probability simplex | 381 | taught | RO #268 (belief space as a simplex) [hand-checked] |
| probability space | 562 | taught | MA-011 (sample space and probability); recap robotics.md §5 "Probability space" |
| progressive widening | 197 | out-of-scope | research extension of MCTS (DM §9.6) |
| proportional to | 49 | taught | ML-082 (Bayes without the evidence: proportional to) |
| proposal distribution | 287 | taught | robotics.md §4 new MA "Importance sampling" (proposal); RO #95 (better proposal distributions) |
| prospect theory | 122 | out-of-scope | behavioural economics (DM §6.?) |
| proximal policy optimization | 257 | taught | RL #39 Proximal policy optimisation [hand-checked] |
| prune | 185, 412 | taught | RL #54 (alpha-beta pruning); RO #268 (pruning) |
| pseudocounts | 79f | add | Bayesian parameter learning: Beta and Dirichlet priors, conjugate updates [maths] -> MA 08-likelihood, new Note after MA-072. pseudocounts are how conjugate priors are read (DM §4.2) |
| pseudoinverse | 174 | taught | MA-060 SVD in ML (pseudo-inverse) |
| PSPACE-complete | 427, 577 | out-of-scope | complexity class (DM §20.?, §C.?) |
| PSPACE-hard | 577 | taught | RO #103 (PSPACE-hard) |
| PSPACE | 577 | taught | RO #103 (PSPACE-hard) |
| pure strategy | 494 | taught | RL #54 (mixed vs pure strategies) [hand-checked] |
| Q-function | see action value function | index-noise | cross-reference to "action value function" |
| Q-learning | 336 | taught | RL #21 Q-learning |
| QCLP | see quadratically constrained linear program | index-noise | cross-reference to "quadratically constrained linear program" |
| QMDP | 427 | taught | RO #269 Approximate POMDP planning (QMDP) |
| quadratically constrained linear program | 481 | out-of-scope | POMDP controller optimisation (DM §23.?), research-level |
| quadratic reward | 148 | taught | RO #205 LQR (quadratic cost) [hand-checked] |
| quadratic utility | 115 | out-of-scope | economics (utility functions, DM §6.?) |
| quantal-level-k | see hierarchical softmax | index-noise | cross-reference to "hierarchical softmax" |
| quantal response | see softmax response | index-noise | cross-reference to "softmax response" |
| quantile | 305 | taught | MA-008 Percentiles and box plots |
| quantile exploration | 305 | taught | RL #4 (upper-confidence-bound selection) |
| quantile function | 21 | taught | MA-029 Uniform and log-normal (inverse CDF) |
| query variables | 43 | out-of-scope | Bayesian-network inference term (DM §3.?) |
| R-MAX | 323 | out-of-scope | PAC-exploration algorithm (DM §16.?); optimism bonuses are RL #4 and RL #45 |
| random belief expansion | 440 | out-of-scope | point-based POMDP solver detail (DM §21.?) |
| randomized point-based value iteration | 433 | out-of-scope | point-based POMDP solver variant (DM §21.?) |
| randomized probability matching | see posterior sampling | index-noise | cross-reference to "posterior sampling" |
| randomized restart | 102 | out-of-scope | local-search detail (DM §5.?) |
| rank shaping | 221 | out-of-scope | evolution-strategies detail (DM §10.?) |
| rational learning | 509 | out-of-scope | game-theory learning (DM §25.?) |
| rational preferences | 112 | taught | RL #53 (utility theory and rationality) |
| reachable state space | 181 | out-of-scope | online-planning detail (DM §9.?) |
| receding horizon planning | 181 | taught | RO #207 (receding horizon) |
| recurrent neural network | 589 | taught | DL-055 to DL-059 RNN |
| recursive Bayesian estimation | 381 | taught | RO #78 The Bayes filter [hand-checked] |
| REINFORCE | 245 | taught | RL #30 REINFORCE |
| reinforcement learning | 7, 15, 297 | taught | RL #1 The reinforcement learning problem |
| relative entropy | 567 | taught | robotics.md §4 new MA "KL divergence" [hand-checked] |
| relative standard error | 285 | out-of-scope | statistics detail of the validation chapter (DM §14.?) |
| repeated games | 493 | out-of-scope | game theory (DM ch.24) |
| replay memory | 345 | taught | RL #36 Experience replay [hand-checked] |
| representation learning | 592 | taught | RO #353 Pretrained visual representations; DL-002 |
| response | 494 | out-of-scope | game-theory term (DM §24.?) |
| restricted step | 251 | out-of-scope | optimisation detail inside policy-gradient update (DM §12.?) |
| return | 134, 599 | taught | RL #8 Return and discounting |
| reverse accumulation | 585 | taught | DL-015 Backpropagation [hand-checked] |
| reward function | 133 | taught | RL #7 Markov decision processes [hand-checked] |
| reward independence | 547 | out-of-scope | research multiagent model property (DM §27.?) |
| reward shaping | 343 | taught | RO #146 Reward shaping and its risks |
| reward-to-go | 240 | add | reward-to-go in policy gradients (each action credited only with later rewards) [RL] -> RL-04, section in Note #30 The policy gradient theorem and REINFORCE. DM §11.? and standard deep-RL courses; Note #30 lists REINFORCE but not this variance cut |
| robust dynamic programming | 289 | taught | RO #141 Robust RL (robust MDP) |
| robust model predictive control | 204 | add | robust MPC (constraints that hold for every disturbance in a set) [control] -> RO-15, section in Note #208 Nonlinear MPC. DM §9.?; RO #208 covers disturbances and offset-free MPC but not robust (tube/min-max) MPC |
| rock-paper-scissors | 495, 621 | out-of-scope | game-theory example (DM appendix F) |
| rollout policy | 183 | taught | RL #47 Rollout algorithms [hand-checked] |
| salvage values | 617 | out-of-scope | book's test problem detail (DM appendix F) |
| sample space | 562 | taught | MA-010 Events (sample space) |
| Sarsa | 338 | taught | RL #20 Sarsa |
| SARSOP | see Successive Approximations of the Reachable Space under Optimal Policies | index-noise | cross-reference to "SARSOP" |
| satisfiable | 578 | out-of-scope | complexity theory (DM §C.?) |
| sawtooth heuristic search | 442 | out-of-scope | research POMDP solver (DM §21.?) |
| sawtooth upper bound | 436 | out-of-scope | value-function bound for POMDP solvers (DM §21.?) |
| scenario | 459 | out-of-scope | online POMDP solver detail (DM §22.?) |
| score equivalent | 104 | out-of-scope | Bayesian-network structure learning (DM §5.?) |
| search distribution | 218 | taught | RL #43 (search distribution in CEM) [hand-checked] |
| search graph | 600 | taught | RO #103 (graph as a model of a state space) |
| search problem | 599 | taught | RO #103 Graphs and uninformed search [hand-checked] |
| search tree | 183, 600 | taught | RL #48 MCTS (search tree) |
| sensitivity | 253 | out-of-scope | optimisation detail inside policy-gradient update (DM §12.?) |
| sequential interactive demonstrations | 358 | out-of-scope | research imitation variant (DM §18.?) |
| Shannon information | 565 | taught | ML-091 (information content) [hand-checked] |
| shaping function | 343 | add | potential-based reward shaping (shaping that keeps the optimal policy) [RL] -> RO-09, section in Note #146 Reward shaping and its risks. DM §17.? (Ng et al. 1999); Note #146 lists shaping and hacking, not the safe form |
| sigma points | 387 | taught | RO #256 Unscented Kalman filter (sigma points) |
| sigmoid | 32 | taught | ML-071 Sigmoid function |
| simple decisions | 111 | out-of-scope | chapter title pointer (DM ch.6) |
| simple game | 493 | out-of-scope | game theory (DM ch.24) |
| simple regulator problem | 613 | out-of-scope | book's test problem (DM appendix F) |
| simplex | 168 | out-of-scope | interpolation-grid detail (DM §8.5) |
| simplex interpolation | 168 | out-of-scope | interpolation-grid detail (DM §8.5) |
| simulated annealing | 102 | mentioned-only | local search: hill climbing, pattern search and simulated annealing [maths] -> MA 07-optimisation, new Note after MA-068. DM §5.? and OPT ch.8 teach it; ML-058 only mentions the name |
| simultaneous perturbation stochastic approximation | 234 | add | gradient estimation by random perturbation (SPSA) [maths] -> MA 07-optimisation, short section with finite differences. DM §11.? and OPT §2.? teach it; same idea as ES gradients in RL #43 |
| singular value decomposition | 174 | taught | MA-057 SVD geometry |
| SMILe | see stochastic mixing iterative learning | index-noise | cross-reference to "stochastic mixing iterative learning" |
| smooth fictitious play | 509 | out-of-scope | game-theory learning (DM §25.?) |
| softmax | 583 | taught | DL-027 (softmax); ML-078 Softmax regression |
| softmax response | 497 | out-of-scope | game-theory model (DM §24.?) |
| softmax response policy | 520 | out-of-scope | game-theory model (DM §25.?) |
| softmax strategy | 303 | add | softmax (Boltzmann) exploration over action values [RL] -> RL-01 Note #4 Exploring smartly (one line beside UCB). DM §15.? ; RL #5 uses softmax over preferences, not over value estimates |
| soft threshold | 32 | out-of-scope | Bayesian-network CPD form (DM §2.?) |
| sparse reward | 341 | taught | RO #150 Sparse rewards and hindsight relabelling |
| sparse sampling | 187 | out-of-scope | theoretical precursor of MCTS (DM §9.5); absent from all 8 evidence docs |
| spherical Gaussian | see isotropic Gaussian | index-noise | cross-reference to "isotropic Gaussian" |
| splat | 642 | index-noise | Julia language feature (DM appendix G) |
| spread parameter | 388 | out-of-scope | UKF tuning detail (DM §19.?) |
| standard basis | 232 | taught | MA-052 (basis) |
| standard deviation | 22 | taught | MA-006 Measures of dispersion |
| standard error | 285 | taught | MA-033 (standard error) |
| standard form games | see normal form games | index-noise | cross-reference to "normal form games" |
| state space | 133, 599 | taught | RL #7 MDP; RO #72 (C-space) |
| state transition model | 133 | taught | RL #7 (MDP dynamics p(s', r  |
| state uncertainty | 2 | out-of-scope | chapter framing of uncertainty sources (DM §1.?) |
| stationary | 133, 520 | out-of-scope | stationarity of MDP models (DM §7.1); one-line definition inside RL #7 |
| stationary Markov perfect equilibrium | 520 | out-of-scope | game theory (DM ch.25) |
| stationary policies | 135 | out-of-scope | policy class term (DM §7.?) |
| step factor | 567 | taught | ML-056 (learning rate as step size) |
| stochastic game | see Markov game | index-noise | cross-reference to "Markov game" |
| stochastic mixing iterative learning | 358 | out-of-scope | research imitation variant SMILe (DM §18.?) |
| stochastic policy | 135 | taught | RL #9 (policy as a conditional distribution) |
| stress testing | 289 | add | falsification: searching for the disturbances that make a policy fail (adversarial stress testing) [robotics] -> RO-20, section in Note #249 Evaluating driving (scenario-based testing). DM ch.14; RO #248-#249 list scenario testing and safety cases but not the search for failures |
| strictly concave | 565 | out-of-scope | proof-level property (DM §A.?) |
| strictly convex | 565 | out-of-scope | proof-level property (DM §A.?) |
| stride | 587 | taught | DL-043 Padding and strides |
| string | 629 | index-noise | Julia language feature (DM appendix G) |
| Successive Approximations of the Reachable Space under Optimal Policies | 440 | out-of-scope | research POMDP solver SARSOP (DM §21.?) |
| successor distribution | 471 | out-of-scope | POMDP controller detail (DM §23.?) |
| sum-product algorithm | 53 | out-of-scope | exact graphical-model inference (DM §3.?) |
| sum-product variable elimination | 49 | out-of-scope | exact graphical-model inference (DM §3.?) |
| supervised learning | 6 | taught | ML-003 Types of ML |
| support | 22f | out-of-scope | probability notation (DM §2.?) |
| surrogate constraint | 256 | out-of-scope | TRPO derivation detail (DM §12.?) |
| surrogate objective | 256 | taught | RL #38 Trust regions: TRPO (surrogate objective) |
| symbol | 630 | index-noise | Julia language feature (DM appendix G) |
| symmetry | 562 | out-of-scope | metric axiom (DM §A.3); RO #108 lists the rules |
| tabu search | 103 | out-of-scope | research local-search variant (DM §5.?) |
| target parameterizations | 274 | out-of-scope | deep-RL detail (DM §17.?); target networks are RL #36 |
| taxicab norm | 563 | add | vector norms L1, L2 and L-infinity (Manhattan, Euclidean, Chebyshev) [maths] -> MA 05-linear-algebra, short section in MA-049. taxicab = L1 (DM §A.3) |
| Taylor approximation | 569 | taught | MA-064 Hessian and multivariate Taylor |
| Taylor expansion | 568 | taught | MA-064 Hessian and multivariate Taylor |
| Taylor series | 568 | taught | MA-061 (Taylor series) |
| temporal difference error | 336 | taught | RL #19 (TD error) |
| temporal difference residual | 268 | taught | RL #34 (GAE: TD residuals) [hand-checked] |
| temporal logic | 293 | add | temporal logic task specifications (LTL) [robotics] -> RO-14, section in Note #197 Shields, safety filters (which names only "Formal methods"). DM §14.? specifies failures with it; robot task specs and shields are written in LTL |
| terminal reward | 617 | out-of-scope | book's test problem detail (DM appendix F) |
| ternary operator | 643 | index-noise | Julia language feature (DM appendix G) |
| thin | 61 | out-of-scope | MCMC detail (DM §3.?) |
| Thompson sampling | see posterior sampling | index-noise | cross-reference to "posterior sampling" |
| topological sort | 55 | out-of-scope | graph algorithm used only for Bayesian-network sampling (DM §3.?) |
| trace trick | 159 | out-of-scope | algebra trick in a derivation (DM §7.8) |
| trade analysis | 291 | out-of-scope | validation-chapter term (DM §14.?) |
| trade-off curve | 291 | taught | RL #53 (Pareto-optimal plans) |
| training | 581 | taught | ML-001 (training) |
| trajectory | 213 | taught | RL #8 (episodes); RO #201 (trajectory) |
| trajectory reward | 214 | taught | RL #8 (return of an episode) |
| transition independence | 547 | out-of-scope | research multiagent model property (DM §27.?) |
| transitivity | 19 | out-of-scope | preference axiom (DM §6.1); utility theory is RL #53 |
| transposition table | 604 | out-of-scope | search implementation detail (DM appendix E) |
| traveler’s dilemma | 622 | out-of-scope | game-theory example (DM appendix F) |
| triangle inequality | 562 | taught | RO #108 (metric space: rules a distance must follow) |
| TRPO | see trust region policy optimization | index-noise | cross-reference to "trust region policy optimization" |
| truncated Gaussian distribution | 23 | out-of-scope | distribution used in one example (DM §2.?) |
| trust region | 254 | taught | RL #38 Trust regions: TRPO |
| trust region policy optimization | 254 | taught | RL #38 Trust regions: TRPO [hand-checked] |
| tuple | 636 | index-noise | Julia language feature (DM appendix G) |
| Turing complete | see computationally universal | index-noise | cross-reference to "computationally universal" |
| Turing machine | 575 | out-of-scope | computability theory (DM §C.?) |
| UCB1 exploration | 305 | taught | RL #4 (upper-confidence-bound selection) |
| UCB1 exploration heuristic | 187 | taught | RL #48 MCTS (UCB selection) [hand-checked] |
| UKF | see unscented Kalman filter | index-noise | cross-reference to "unscented Kalman filter" |
| uncertainty set | 204 | taught | RO #141 Robust RL (robust MDP) |
| undecidable | 579 | out-of-scope | computability theory (DM §C.?) |
| underdetermined | 585 | out-of-scope | linear-algebra detail of neural-network appendix (DM §D.?) |
| undirected exploration | 301 | taught | RL #2 (epsilon-greedy as undirected exploration) [hand-checked] |
| undirected path | 572 | add | graph basics: directed and undirected graphs, paths, cycles, DAGs, trees (parent, child) [maths] -> RO-05, short section in Note #103 Graphs and uninformed search. Note #103 lists 'graph as a model of a state space' only; Bayes nets, factor graphs (RO #263), roadmaps and search trees all need this vocabulary (DM appendix A, OPT §19) |
| uniform distribution | 21 | taught | MA-029 Uniform distribution |
| unimodal | 23 | taught | MA-073 (unimodal vs multimodal) [hand-checked] |
| univariate | 573 | taught | MA-020 (univariate distributions) [hand-checked] |
| univariate distribution | 24 | taught | MA-020 (univariate distributions) [hand-checked] |
| universal comparability | 19 | out-of-scope | preference axiom (DM §6.1) |
| unscented Kalman filter | 387 | taught | RO #256 Unscented Kalman filter |
| unscented transform | 387 | taught | RO #256 Unscented Kalman filter |
| unsupervised | 593 | taught | ML-003 Types of ML (unsupervised) |
| update step | 385 | taught | RO #78 The Bayes filter (update step) |
| upper confidence bound, probabilistic | 276 | out-of-scope | MCTS selection variant (DM §9.6) |
| upper confidence bound exploration | see quantile exploration | index-noise | cross-reference to "quantile exploration" |
| utility | 112 | taught | RL #53 (utility theory) |
| utility elicitation | 114 | out-of-scope | economics (DM §6.?) |
| utility node | 116 | out-of-scope | decision-network notation (DM §6.5) |
| utility theory | 14, 111 | taught | RL #53 (utility theory and rationality) |
| value function | 136 | taught | RL #9 (value functions) |
| value function approximation | 161 | taught | RL #25 Value prediction as supervised learning [hand-checked] |
| value iteration | 141, 416 | taught | RL #14 Value iteration |
| value of information | 119 | add | value of information [RL] -> RL-07, section in Note #53 Decisions against nature (Bayesian decision making with observations). DM §6.6; decides when a robot should sense before acting; links to information-gain exploration (RO #180) |
| vanishing gradient | 590 | taught | DL-018 Vanishing and exploding gradients |
| variance | 239 | taught | MA-006 Measures of dispersion; MA-012 |
| variational autoencoder | 593 | taught | robotics.md §4 new DL "Variational autoencoder" |
| vector | 630 | taught | MA-048 Vectors |
| vector space | 562 | taught | MA-047 Linear algebra roadmap (vector space) |
| vertex | see node | index-noise | cross-reference to "node" |
| von Neumann–Morgenstern axioms | 112 | out-of-scope | utility-theory axioms (DM §6.1) |
| weight regularization | 585 | taught | ML-062 Ridge regression (weight regularisation) |
| weights | 174 | taught | DL-008 MLP notation (weights) |
| zero-sum game | 494 | taught | RL #54 (zero-sum games) |

## Kochenderfer & Wheeler, Algorithms for Optimization, 2nd ed. draft (MIT Press) - replacement for Boyd & Vandenberghe

Source: https://algorithmsbook.com/optimization/files/optimization.pdf (redirects to the authors' Google Drive file 1Rx7MAekKZbyNVc5B2MNfR0HXXIEJCksp). Index: PDF pp. 627-634 (book pp. 607-614). Terms: 680. add 100, index-noise 59, mentioned-only 4, out-of-scope 301, taught 216

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| 0.632 bootstrap estimate | 381 | out-of-scope | model-validation estimator variant (OPT §14.?); bootstrap itself is MA-034/ML-099 |
| abstract types | 553 | index-noise | Julia language feature (OPT appendix A) |
| Ackley’s function | 561 | out-of-scope | benchmark test function (OPT appendix B) |
| active | 192 | taught | MA-068 (active constraints, KKT); recap robotics.md §5 |
| Adadelta | 84 | taught | DL-038 Adam (Adadelta named) |
| AdaGrad | see adaptive gradient | index-noise | cross-reference to "adaptive gradient" |
| Adam | see adaptive moment estimation | index-noise | cross-reference to "adaptive moment estimation" |
| adaptive gradient | 82 | taught | DL-036 AdaGrad |
| adaptive moment estimation | 86 | taught | DL-038 Adam |
| additive recurrence | 359 | out-of-scope | quasi-random sequence detail (OPT §13.?) |
| ADMM | see alternating direction method of multipliers | index-noise | cross-reference to "alternating direction method of multipliers" |
| affine subspace | 253 | out-of-scope | term used only inside the LP chapter's derivation (OPT §11.1) |
| aleatory uncertainty | see irreducible uncertainty | index-noise | cross-reference to "irreducible uncertainty" |
| algebra | 2 | out-of-scope | history of the word (OPT §1.1) |
| algorithm | 2 | out-of-scope | history of the word (OPT §1.1) |
| algorithms | 1 | out-of-scope | history of the word (OPT §1.1) |
| algoritmi | 2 | out-of-scope | history of the word (OPT §1.1) |
| alternating direction method of multipliers | 219 | add | augmented Lagrangian and ADMM [maths] -> MA 07-optimisation, new Note after MA-068 (or section of RO #208). OSQP, the QP solver behind many MPC stacks (RO #207-#208), is ADMM; OPT §10.? and §11.? |
| alternating projections | 227 | out-of-scope | research constraint-handling method (OPT §11.?) |
| anchoring point | 116 | out-of-scope | direct-method implementation detail (OPT §7.?) |
| anonymous function | 555 | index-noise | Julia language feature (OPT appendix A) |
| ant colony optimization | 477 | out-of-scope | metaheuristic family (OPT §9.?); the plan's population search is ES/CMA-ES (RL #43) |
| approximate line search | 65 | add | line search and one-dimensional minimisation (bracketing, golden section, backtracking, Wolfe conditions) [maths] -> MA 07-optimisation, new Note (MA-064 only says "usually shortened by a line search"). OPT ch.3-4 and DM §12.?; every Newton, quasi-Newton and SQP solver used in trajectory optimisation and MPC (RO #116, #208) uses it |
| Armijo condition | see sufficient decrease | index-noise | cross-reference to "sufficient decrease" |
| Armijo line search | see backtracking line search | index-noise | cross-reference to "backtracking line search" |
| array comprehension | 544 | index-noise | Julia language feature (OPT appendix A) |
| assignment | 516 | index-noise | Julia language feature (OPT appendix A) |
| associative array | 516 | index-noise | Julia language feature (OPT appendix A) |
| asymptotic notation | 571 | taught | RO #103 (Big-O) |
| atom library | 300 | out-of-scope | disciplined-convex-programming tool detail (OPT §12.?) |
| augmented Lagrange method | see method of multipliers | index-noise | cross-reference to "method of multipliers" |
| augmented system | 316 | out-of-scope | linear-algebra detail of constrained least squares (OPT §12.?) |
| automatic differentiation | 29 | add | automatic differentiation: forward and reverse mode [maths] -> MA 06-calculus, short section after MA-063 (DL-015 teaches reverse mode as backprop). OPT §2.4; differentiable simulators (RB #316), trajectory optimisation (RO #116) and MPC solvers get Jacobians this way; forward mode is not taught anywhere |
| auxiliary linear program | 262 | out-of-scope | simplex-algorithm initialisation detail (OPT §11.?) |
| backslash operator | 36, 274 | index-noise | Julia language feature (OPT appendix A) |
| backtracking line search | 65 | add | line search and one-dimensional minimisation (bracketing, golden section, backtracking, Wolfe conditions) [maths] -> MA 07-optimisation, new Note. OPT §4.2 backtracking line search |
| backward difference | 24 | taught | MA-061 (finite differences) |
| backward pass | 33 | taught | DL-015 Backpropagation (backward pass) |
| Baldwinian learning | 179 | out-of-scope | evolutionary-computation variant (OPT §9.?) |
| barrier methods | 199 | taught | RO #194 (log-barrier methods) |
| basic | 257 | out-of-scope | simplex-algorithm vocabulary (OPT §11.2) |
| basis functions | 367 | taught | RL #26 (basis functions); ML-060 |
| basis pursuit | 231 | out-of-scope | sparse-recovery problem (OPT §10.?), signal processing |
| batches | 135 | taught | ML-059 Mini-batch gradient descent |
| Bayes-Hermite Quadrature | 455 | out-of-scope | research quadrature method (OPT §18.?) |
| Bayesian Monte Carlo | 455 | out-of-scope | research quadrature method (OPT §18.?) |
| Bayesian optimization | 411 | taught | ML-128 Optuna (Bayesian optimisation, glossary G-270) |
| BFGS | see Broyden-Fletcher-Goldfarb-Shanno | index-noise | cross-reference to "Broyden-Fletcher-Goldfarb-Shanno" |
| big M method | 485 | out-of-scope | integer-programming modelling trick (OPT §19.?) |
| big-Oh notation | 571 | taught | RO #103 (Big-O) |
| Binet’s formula | 46 | out-of-scope | Fibonacci-number formula (OPT §3.?) |
| bisection method | 57 | add | line search and one-dimensional minimisation (bracketing, golden section, backtracking, Wolfe conditions) [maths] -> MA 07-optimisation, new Note. bisection is the 1-D root-finding base before Newton-Raphson (robotics.md §4) |
| black box | 113 | out-of-scope | general term (OPT §7.?) |
| Bland’s rule | 262 | out-of-scope | simplex-algorithm pivot rule (OPT §11.?) |
| block-diagonal | 316 | out-of-scope | linear-algebra detail (OPT §12.?) |
| Boolean | 541 | index-noise | Julia language feature (OPT appendix A) |
| Boolean satisfiability problem | 481 | out-of-scope | complexity theory (OPT §19.?) |
| Booth’s function | 561 | out-of-scope | benchmark test function (OPT appendix B) |
| bootstrap method | 379 | taught | MA-034 (bootstrap); robotics.md §4 "Bootstrap confidence intervals" |
| bootstrap sample | 379 | taught | ML-099 Bagging (bootstrap sample) |
| bound operation | 471 | add | integer programming and branch and bound [maths] -> MA 07-optimisation, new Note after MA-068. OPT §19.5 |
| bowl-shaped | 575 | taught | MA-065 (convex, bowl-shaped cost) |
| bowl | 11f | taught | MA-065 (convex, bowl-shaped cost) |
| box constraint | 183 | taught | MA-068 (bound constraints in LP/QP) |
| bracket | 43 | add | line search and one-dimensional minimisation (bracketing, golden section, backtracking, Wolfe conditions) [maths] -> MA 07-optimisation, new Note. OPT §3.1 bracketing |
| bracketing | 43 | add | line search and one-dimensional minimisation (bracketing, golden section, backtracking, Wolfe conditions) [maths] -> MA 07-optimisation, new Note. OPT §3.1 |
| bracketing phase | 68 | add | line search and one-dimensional minimisation (bracketing, golden section, backtracking, Wolfe conditions) [maths] -> MA 07-optimisation, new Note. OPT §4.4 strong backtracking |
| branch | 471 | add | integer programming and branch and bound [maths] -> MA 07-optimisation, new Note after MA-068. branch step of branch and bound (OPT §19.5) |
| branch and bound | 471 | add | integer programming and branch and bound [maths] -> MA 07-optimisation, new Note after MA-068. OPT §19.5; DM §9.4 uses it for planning |
| branch and cut | 466 | out-of-scope | advanced integer-programming method (OPT §19.?) |
| branch operation | 471 | add | integer programming and branch and bound [maths] -> MA 07-optimisation, new Note after MA-068. OPT §19.5 |
| Branin function | 564 | out-of-scope | benchmark test function (OPT appendix B) |
| Brent-Dekker | 57 | out-of-scope | 1-D root-finding variant (OPT §3.?) |
| broadcasting | 546 | index-noise | Julia language feature (OPT appendix A) |
| Broyden-Fletcher-Goldfarb-Shanno | 103 | add | quasi-Newton methods: BFGS and L-BFGS [maths] -> MA 07-optimisation, new Note after Newton's method (MA-064). OPT §6.3; the default solver for smooth unconstrained problems (trajectory optimisation RO #116, IK RB #279); robotics.md §4 covers only Gauss-Newton and LM |
| calculus | 3 | taught | MA-061 Derivatives of one variable |
| canonical form | 297 | out-of-scope | LP standard-form vocabulary (OPT §11.1); LP itself is MA-068 |
| canonicalization | 307 | out-of-scope | LP standard-form vocabulary (OPT §11.1) |
| Cauchy distribution | 164 | out-of-scope | distribution used in one stochastic method (OPT §8.?) |
| ceiling | 471 | index-noise | notation (ceiling function) |
| central difference | 24 | add | numerical derivatives: central differences and the complex-step method [maths] -> MA 06-calculus, short section in MA-061 (which has forward finite differences). OPT §2.3; checking analytic Jacobians in robot code |
| characteristic length-scale | 392 | taught | robotics.md §4 new ML "Gaussian processes" (kernel length-scale) [hand-checked] |
| Chebyshev distance | 577 | add | vector norms L1, L2 and L-infinity (Manhattan, Euclidean, Chebyshev) [maths] -> MA 05-linear-algebra, short section in MA-049. OPT appendix C.? |
| chessboard distance | 577 | add | vector norms L1, L2 and L-infinity (Manhattan, Euclidean, Chebyshev) [maths] -> MA 05-linear-algebra, short section in MA-049. OPT appendix C.? |
| Cholesky decomposition | 582 | taught | robotics.md §4 new MA "Cholesky factor" [hand-checked] |
| chromosome | 165 | add | genetic algorithms and population methods (selection, crossover, mutation) [maths] -> MA 07-optimisation, new Note after MA-068. OPT §9.2 |
| circle function | 569 | out-of-scope | benchmark test function (OPT appendix B) |
| CMA-ES | see covariance matrix adaptation | index-noise | cross-reference to "covariance matrix adaptation" |
| coherent risk measure | 436 | out-of-scope | risk-measure axioms (OPT §17.?); CVaR itself is RO #198 |
| collaborative optimization | 531 | out-of-scope | multidisciplinary design optimisation, a different field (OPT ch.21) |
| combinatorial optimization | 463 | add | integer programming and branch and bound [maths] -> MA 07-optimisation, new Note after MA-068. OPT ch.19 combinatorial optimisation |
| complete cross-validation | 379 | out-of-scope | cross-validation variant (OPT §14.?) |
| complex step method | 28 | add | numerical derivatives: central differences and the complex-step method [maths] -> MA 06-calculus, short section in MA-061. OPT §2.3.3 |
| composite type | 553 | index-noise | Julia language feature (OPT appendix A) |
| computational graph | 30 | taught | DL-015 Backpropagation (computational graph); DL-019 [hand-checked] |
| concave | 576 | taught | MA-067 Convex sets and functions |
| concrete types | 553 | index-noise | Julia language feature (OPT appendix A) |
| conditional distribution | 390 | taught | MA-014 (conditional distribution) |
| conditional value at risk | 436 | taught | RO #198 Risk-sensitive RL (CVaR); robotics.md §4 |
| cone | 185 | add | second-order cone programs (SOCP) [maths] -> MA 07-optimisation, short section after MA-068. the exact friction cone is a second-order cone (RB #288, robotics.md §4 "Friction pyramid" linearises it); OPT §10.? cone constraints |
| cone constraint | 185 | add | second-order cone programs (SOCP) [maths] -> MA 07-optimisation, short section after MA-068. cone constraints (OPT §10.?) |
| confidence region | 396 | out-of-scope | surrogate-model statistic (OPT §16.?) |
| conjugate gradient | 79 | taught | robotics.md §4 new MA "Sparse linear solves and conjugate gradient" |
| consensus | 234 | out-of-scope | distributed-optimisation term (OPT §10.?) |
| constraint | 6 | taught | MA-066 Lagrange multipliers (constraints); MA-068 |
| constraint method | 329 | add | scalarising several objectives: weighted sum and the constraint method [maths] -> RL-07, section in Note #53 Decisions against nature (which teaches multi-objective optimisation and Pareto-optimal plans). OPT §12.?; robot rewards are weighted sums of terms (RO #145) |
| context-free grammars | 489 | out-of-scope | expression optimisation, a different field (OPT ch.20) |
| contour plot | 13 | taught | MA-062 (contour plots) |
| contours | 13 | taught | MA-062 (contours) |
| convex combination | 574 | taught | MA-067 Convex sets and functions |
| convex function | 575 | taught | MA-067 Convex sets and functions |
| convex program | 297 | taught | MA-067 (convex programs); MA-068 |
| convex set | 575 | taught | MA-067 Convex sets and functions |
| coordinate descent | 77, 113 | add | local search: hill climbing, pattern search and simulated annealing [maths] -> MA 07-optimisation, new Note after MA-068. coordinate descent is the simplest derivative-free direct method (OPT §7.1) |
| coprime | 361 | out-of-scope | number theory (OPT §13.?) |
| corrector function | 407 | out-of-scope | surrogate-model detail (OPT §15.?) |
| coupling variables | 526 | out-of-scope | multidisciplinary design optimisation (OPT ch.21) |
| covariance function | 391 | taught | robotics.md §4 new ML "Gaussian processes" (covariance function) [hand-checked] |
| covariance matrix adaptation | 152 | taught | RL #43 (CMA-ES) |
| covariance matrix adaptation evolutionary strategy | see covariance matrix adaptation | index-noise | cross-reference to "covariance matrix adaptation" |
| covariant gradient | 97 | taught | RL #38 (natural gradient) |
| criterion space | 327 | out-of-scope | multiobjective vocabulary (OPT §12.?) |
| critical point | 191 | taught | MA-065 (stationary points) |
| cross-entropy | 144 | taught | ML-072 Log loss (cross-entropy) |
| cross-entropy method | 144 | taught | RL #43 (cross-entropy method) |
| crossover | 165 | add | genetic algorithms and population methods (selection, crossover, mutation) [maths] -> MA 07-optimisation, new Note after MA-068. OPT §9.2.? |
| crossover point | 168 | add | genetic algorithms and population methods (selection, crossover, mutation) [maths] -> MA 07-optimisation, new Note after MA-068. OPT §9.2.? |
| cuckoo search | 177 | out-of-scope | metaheuristic family (OPT §9.?) |
| cumulative distribution function | 436, 586 | taught | MA-021, MA-022 (CDF) |
| curvature | 299 | taught | MA-061 (second derivative as curvature); MA-064 |
| curvature condition | 68, 110 | add | line search and one-dimensional minimisation (bracketing, golden section, backtracking, Wolfe conditions) [maths] -> MA 07-optimisation, new Note. OPT §4.4 Wolfe curvature condition |
| cutting plane | 467 | out-of-scope | advanced integer-programming method (OPT §19.?) |
| cutting plane method | 466 | out-of-scope | advanced integer-programming method (OPT §19.?) |
| CVaR | see conditional value at risk | index-noise | cross-reference to "conditional value at risk" |
| cycles | 262 | out-of-scope | simplex-algorithm degeneracy detail (OPT §11.?) |
| cyclic coordinate search | 113 | add | local search: hill climbing, pattern search and simulated annealing [maths] -> MA 07-optimisation, new Note after MA-068. OPT §7.1 |
| Dantzig’s rule | 262 | out-of-scope | simplex-algorithm pivot rule (OPT §11.?) |
| Davidon-Fletcher-Powell | 103 | add | quasi-Newton methods: BFGS and L-BFGS [maths] -> MA 07-optimisation, new Note. DFP is the first quasi-Newton update (OPT §6.3) |
| DCP | see disciplined convex program | index-noise | cross-reference to "disciplined convex program" |
| decision quality improvement | 343 | out-of-scope | preference-elicitation detail (OPT §12.?) |
| deep learning | 7 | taught | DL-002 What is deep learning |
| Dempster-Shafer theory | 428 | out-of-scope | different field: evidence theory (OPT §17.?) |
| dependency cycle | 518 | out-of-scope | multidisciplinary design optimisation (OPT ch.21) |
| dependency graph | 518 | out-of-scope | multidisciplinary design optimisation (OPT ch.21) |
| dequeue | 471 | index-noise | data-structure operation name (OPT §19.?) |
| derivative-free | 113 | add | local search: hill climbing, pattern search and simulated annealing [maths] -> MA 07-optimisation, new Note after MA-068. derivative-free methods (OPT ch.7) |
| derivative | 23 | taught | MA-061 Derivatives of one variable |
| descent direction | 61 | taught | ML-056 Gradient descent |
| descent direction methods | 61 | taught | ML-056 Gradient descent |
| designer | 4 | out-of-scope | engineering-design vocabulary (OPT §1.?) |
| design matrix | 366 | taught | ML-053 (design matrix X in the normal equation) |
| design point | 5 | out-of-scope | engineering-design vocabulary (OPT §1.?) |
| design selection | 343 | out-of-scope | preference-elicitation detail (OPT §12.?) |
| design variables | 5 | out-of-scope | engineering-design vocabulary (OPT §1.?) |
| DFP | see Davidon-Fletcher-Powell | index-noise | cross-reference to "Davidon-Fletcher-Powell" |
| dictionary | 516, 552 | index-noise | Julia language feature (OPT appendix A) |
| differential evolution | 172 | out-of-scope | metaheuristic family (OPT §9.?) |
| DIRECT | see divided rectangles | index-noise | cross-reference to "divided rectangles" |
| directional derivative, Clarke | 577 | out-of-scope | nonsmooth-analysis detail (OPT appendix C) |
| directional derivative | 26 | taught | MA-062 (directional derivative) |
| direct methods | 113 | add | local search: hill climbing, pattern search and simulated annealing [maths] -> MA 07-optimisation, new Note after MA-068. direct (derivative-free) methods, OPT ch.7 |
| Dirichlet distribution | 502 | add | Bayesian parameter learning: Beta and Dirichlet priors, conjugate updates [maths] -> MA 08-likelihood, new Note after MA-072. OPT §20.? uses the Dirichlet for grammar weights; DM §4.2 |
| disciplinary analyses | 515 | out-of-scope | multidisciplinary design optimisation (OPT ch.21) |
| disciplined convex program | 297 | out-of-scope | convex-modelling tool rules (OPT §12.?) |
| discrepancy | 353 | out-of-scope | sampling-plan metric (OPT §13.?) |
| discrete factors | 349 | out-of-scope | sampling-plan detail (OPT §13.?) |
| discrete optimization | 463 | add | integer programming and branch and bound [maths] -> MA 07-optimisation, new Note after MA-068. OPT ch.19 discrete optimisation |
| dispatch | 557 | index-noise | Julia language feature (OPT appendix A) |
| distributed architecture | 532 | out-of-scope | multidisciplinary design optimisation (OPT ch.21) |
| distributionally robust optimization | 434 | out-of-scope | research robust-optimisation formulation (OPT §17.?) |
| divided rectangles | 124 | out-of-scope | global Lipschitz-based method (OPT §7.?), research-level |
| dominates | 326 | taught | RL #53 (Pareto-optimal plans) |
| dual ascent | 218 | out-of-scope | dual-decomposition detail (OPT §10.?) |
| dual certificates | 266 | out-of-scope | duality detail (OPT §10.?) |
| dual feasibility | 193 | taught | MA-068 (KKT conditions); recap robotics.md §5 |
| dual form | 210 | taught | MA-066 (Lagrangian duality) |
| dual function | 210 | taught | MA-066 (Lagrangian duality) |
| duality | 209 | taught | MA-066 (Lagrangian duality); MA-068 |
| duality gap | 210 | taught | MA-066 (weak and strong duality) |
| dual numbers | 32 | add | automatic differentiation: forward and reverse mode [maths] -> MA 06-calculus, short section after MA-063. dual numbers implement forward mode (OPT §2.4) |
| dual part | 32 | add | automatic differentiation: forward and reverse mode [maths] -> MA 06-calculus, short section after MA-063. OPT §2.4 |
| dual residual | 221 | out-of-scope | ADMM convergence detail (OPT §10.?) |
| dual value | 210 | taught | MA-066 (Lagrangian duality) |
| dual variable | 193, 209 | taught | MA-066 (multipliers as dual variables) |
| dynamic ordering | 119 | out-of-scope | direct-method detail (OPT §7.?) |
| dynamic programming | 474 | taught | RL-02 (dynamic programming); DL-019 memoization |
| elastic band | 243 | out-of-scope | research trajectory-optimisation method (OPT §10.?); RO #129 teaches the timed elastic band |
| elite samples | 144 | taught | RL #43 (cross-entropy method elite samples) [hand-checked] |
| elitism | 165 | add | genetic algorithms and population methods (selection, crossover, mutation) [maths] -> MA 07-optimisation, new Note after MA-068. OPT §9.2 |
| elitist selection | see elitism | index-noise | cross-reference to "elitism" |
| enqueue | 471 | index-noise | data-structure operation name (OPT §19.?) |
| entering index | 260 | out-of-scope | simplex-algorithm vocabulary (OPT §11.2) |
| entropic value at risk | 436 | out-of-scope | risk-measure variant (OPT §17.?); CVaR is RO #198 |
| epigraph | 313 | out-of-scope | convex-analysis term (OPT §12.?) |
| epistemic uncertainty | 427 | out-of-scope | uncertainty taxonomy (OPT §17.1) |
| equality form | 252 | out-of-scope | LP standard-form vocabulary (OPT §11.1) |
| equivalence class sharing | 339 | out-of-scope | multiobjective population detail (OPT §12.?) |
| error-based exploration | 412 | add | Bayesian optimisation acquisition functions: expected improvement, probability of improvement, confidence bounds [maths] -> ML-128 Optuna (section) or the new GP Note of robotics.md §4. ML-128 teaches Bayesian optimisation by name; OPT ch.16 gives the acquisition functions used for controller-gain tuning and SafeOpt (RO #200) |
| error function | 586 | out-of-scope | special function in the Gaussian CDF (OPT appendix C) |
| Euclidean norm | 577 | taught | MA-049 Magnitude and distance (Euclidean) |
| evolution path | 154 | out-of-scope | CMA-ES internal detail (OPT §8.?) |
| exchange subset selection | 357 | out-of-scope | surrogate-model subset selection (OPT §13.?) |
| expected improvement | 415 | add | Bayesian optimisation acquisition functions: expected improvement, probability of improvement, confidence bounds [maths] -> ML-128 Optuna (section). OPT §16.? |
| expected value | 434 | taught | MA-012 Expected value and variance |
| expert responses | 342 | out-of-scope | preference-elicitation detail (OPT §12.?) |
| exploitation | 413 | taught | RL #1 (exploration vs exploitation) |
| exploration | 413 | taught | RL #1 (exploration vs exploitation) |
| exponential annealing schedule | 141 | add | local search: hill climbing, pattern search and simulated annealing [maths] -> MA 07-optimisation, new Note after MA-068. annealing schedule (OPT §8.?) |
| exponential weighted criterion | 334 | out-of-scope | multiobjective scalarisation variant (OPT §12.?) |
| extended-valued function | 300 | out-of-scope | convex-analysis term (OPT §12.?) |
| extended real-valued function | 300 | out-of-scope | convex-analysis term (OPT §12.?) |
| factor of safety | 440 | out-of-scope | engineering-design term (OPT §17.?) |
| fast annealing | 141 | add | local search: hill climbing, pattern search and simulated annealing [maths] -> MA 07-optimisation, new Note after MA-068. annealing schedule (OPT §8.?) |
| feasibility problem | 299 | taught | MA-068 (feasible region) |
| feasible set | 5 | taught | MA-068 (feasible region); MA-066 |
| Fibonacci search | 45 | add | line search and one-dimensional minimisation (bracketing, golden section, backtracking, Wolfe conditions) [maths] -> MA 07-optimisation, new Note. Fibonacci search is the optimal bracketing rule (OPT §3.3) |
| fidelity | 383 | out-of-scope | multifidelity-model term (OPT §14.?) |
| finite difference methods | 27 | taught | MA-061 (finite differences) |
| firefly algorithm | 174 | out-of-scope | metaheuristic family (OPT §9.?) |
| first-order | 77 | taught | ML-056 Gradient descent (first-order method) |
| first-order necessary condition | 11 | taught | MA-065 (gradient zero at a minimum); MA-067 |
| first fundamental theorem of calculus | 573 | add | integrals and the fundamental theorem of calculus [maths] -> MA 06-calculus, new Note after MA-062. OPT appendix C.?; MA has no integration Note |
| Fisher information matrix | 149 | taught | RL #38; robotics.md §4 "Natural gradient and Fisher information" [hand-checked] |
| fitness proportionate selection | see roulette wheel selection | index-noise | cross-reference to "roulette wheel selection" |
| fitness sharing | 339 | out-of-scope | multiobjective population detail (OPT §12.?) |
| Fletcher-Reeves | 80 | out-of-scope | conjugate-gradient variant (OPT §5.?) |
| floor | 469 | index-noise | notation (floor function) |
| flower function | 565 | out-of-scope | benchmark test function (OPT appendix B) |
| forward accumulation | 31 | add | automatic differentiation: forward and reverse mode [maths] -> MA 06-calculus, short section after MA-063. forward accumulation (OPT §2.4) |
| forward difference | 24 | taught | MA-061 (finite differences) |
| forward pass | 33 | taught | DL-010 Forward propagation |
| Fourier series | 370 | add | Fourier series and the Fourier transform (frequency content of a signal) [maths] -> MA 06-calculus, new Note after the planned integrals Note. OPT §14.? uses sinusoidal bases; the owner found Fourier transform and frequency response missing; RL #26 uses Fourier features without a maths Note |
| fractional knapsack | 483 | out-of-scope | combinatorial example problem (OPT §19.?) |
| full factorial | 349 | out-of-scope | design-of-experiments plan (OPT §13.?) |
| function | 555 | index-noise | Julia language feature (OPT appendix A) |
| fuzzy-set theory | 428 | out-of-scope | different field: fuzzy logic (OPT §17.?) |
| gamma function | 392 | out-of-scope | special function in the Matérn kernel (OPT §16.?) |
| gap | 432 | out-of-scope | uncertainty-model detail (OPT §17.?) |
| Gauss-Seidel method | 518 | out-of-scope | multidisciplinary design iteration (OPT ch.21) |
| Gaussian distribution | 389 | taught | MA-024 Normal distribution |
| Gaussian process | 389, 391 | taught | robotics.md §4 new ML "Gaussian processes" |
| Gaussian quadrature | 586 | out-of-scope | numerical-integration rule (OPT appendix C.?); research-level for this plan |
| gene | 164 | add | genetic algorithms and population methods (selection, crossover, mutation) [maths] -> MA 07-optimisation, new Note after MA-068. OPT §9.2 |
| gene duplication | 497 | out-of-scope | genetic-programming detail (OPT ch.20) |
| general consensus optimization | 235 | out-of-scope | distributed-optimisation term (OPT §10.?) |
| general form | 251 | out-of-scope | LP standard-form vocabulary (OPT §11.1) |
| generalization error | 375 | taught | ML-061 Bias-variance (generalisation error) [hand-checked] |
| generalized gradient, Clarke | 577 | out-of-scope | nonsmooth-analysis detail (OPT appendix C) |
| generalized gradient | 577 | out-of-scope | nonsmooth-analysis detail (OPT appendix C) |
| generalized inequality constraint | 185 | out-of-scope | cone-programming notation (OPT §10.?) |
| generalized Lagrangian | 193, 209 | taught | MA-066 Lagrange multipliers (Lagrangian with inequality constraints); MA-068 |
| generalized pattern search | 117 | add | local search: hill climbing, pattern search and simulated annealing [maths] -> MA 07-optimisation, new Note after MA-068. OPT §7.? |
| generation | 163 | add | genetic algorithms and population methods (selection, crossover, mutation) [maths] -> MA 07-optimisation, new Note after MA-068. OPT §9.2 |
| genetic algorithms | 164 | add | genetic algorithms and population methods (selection, crossover, mutation) [maths] -> MA 07-optimisation, new Note after MA-068. OPT §9.2 |
| genetic local search | 179 | out-of-scope | research hybrid (OPT §9.?) |
| genetic programming | 493 | out-of-scope | expression optimisation, a different field (OPT ch.20) |
| geometric program | 247 | out-of-scope | circuit-design problem class (OPT §12.?) |
| global design variables | 524 | out-of-scope | multidisciplinary design optimisation (OPT ch.21) |
| global minimizer | 10 | taught | MA-065 (global minimum) |
| global optimization method | 53 | out-of-scope | global-optimisation family label (OPT §3.?) |
| goal programming | 332 | out-of-scope | multiobjective scalarisation variant (OPT §12.?) |
| golden ratio | 46 | add | line search and one-dimensional minimisation (bracketing, golden section, backtracking, Wolfe conditions) [maths] -> MA 07-optimisation, new Note. golden-ratio bracketing (OPT §3.4) |
| golden section search | 47 | add | line search and one-dimensional minimisation (bracketing, golden section, backtracking, Wolfe conditions) [maths] -> MA 07-optimisation, new Note. OPT §3.4 |
| gradient | 25 | taught | MA-062 Partial derivatives and gradients |
| gradient descent | 77 | taught | ML-056 Gradient descent |
| grammar | 489 | out-of-scope | expression optimisation, a different field (OPT ch.20) |
| grammatical evolution | 497 | out-of-scope | expression optimisation, a different field (OPT ch.20) |
| graph expansion | 314 | out-of-scope | convex-modelling tool detail (OPT §12.?) |
| graph implementation | 314 | out-of-scope | convex-modelling tool detail (OPT §12.?) |
| greedy heuristic | 261 | out-of-scope | simplex-algorithm pivot rule (OPT §11.?) |
| greedy subset selection | 357 | out-of-scope | sampling-plan subset selection (OPT §13.?) |
| grid search | 349 | taught | ML-128 Optuna (grid search vs smarter search) |
| half-space | 252 | taught | MA-051 Equation of a hyperplane (half-spaces); RO #71 (half-planes) |
| Halton sequence | 360 | out-of-scope | quasi-random sequence (OPT §13.?) |
| heavy ball | 91 | taught | DL-034 SGD with momentum (heavy ball) [hand-checked] |
| Hessian | 25 | taught | MA-064 Hessian and multivariate Taylor |
| hill | 12 | out-of-scope | landscape illustration word (OPT §1.?) |
| holdout method | 377 | taught | ML-012 (train/test holdout) [hand-checked] |
| Hooke-Jeeves method | 116 | add | local search: hill climbing, pattern search and simulated annealing [maths] -> MA 07-optimisation, new Note after MA-068. OPT §7.4 |
| Huber function | 230 | mentioned-only | robust loss functions (Huber) beside least squares [maths] -> MA 07-optimisation, robotics.md §4 short section "Levenberg-Marquardt and robust losses (IRLS)". DL-014 names the Huber loss only in passing; robust losses reject outliers in scan matching and pose graphs (RO #92, #102) |
| hybrid methods | 179 | out-of-scope | evolutionary-computation hybrid (OPT §9.?) |
| hypergradient | 86 | out-of-scope | research step-size method (OPT §5.?) |
| hypergradient descent | 86 | out-of-scope | research step-size method (OPT §5.?) |
| hyperparameter | 44 | taught | ML-128 Optuna (hyperparameter tuning) |
| hyperplane | 25 | taught | MA-051 Equation of a hyperplane |
| hypograph | 313 | out-of-scope | convex-analysis term (OPT §12.?) |
| image | 327 | out-of-scope | multiobjective vocabulary (OPT §12.?) |
| improvement | 413 | out-of-scope | surrogate-optimisation term (OPT §16.?) |
| inactive | 193 | out-of-scope | constraint vocabulary (OPT §10.?); active constraints are MA-068 |
| individual discipline feasible | 526 | out-of-scope | multidisciplinary design optimisation (OPT ch.21) |
| individuals | 163 | add | genetic algorithms and population methods (selection, crossover, mutation) [maths] -> MA 07-optimisation, new Note after MA-068. OPT §9.1 |
| information-gap decision theory | 432 | out-of-scope | different field: info-gap decision theory (OPT §17.?) |
| information-geometric optimization | 149 | out-of-scope | research stochastic method (OPT §8.?) |
| initialization phase | 258, 262 | out-of-scope | simplex-algorithm phase (OPT §11.?) |
| initial population | 163 | add | genetic algorithms and population methods (selection, crossover, mutation) [maths] -> MA 07-optimisation, new Note after MA-068. OPT §9.1 |
| integer linear programs | 464 | add | integer programming and branch and bound [maths] -> MA 07-optimisation, new Note after MA-068. OPT §19.1 |
| integer program | 464 | add | integer programming and branch and bound [maths] -> MA 07-optimisation, new Note after MA-068. OPT §19.1 |
| interdisciplinary compatibility | 517 | out-of-scope | multidisciplinary design optimisation (OPT ch.21) |
| interior point methods | 199 | taught | RO #208 (interior point) |
| intermediate value theorem | 57 | out-of-scope | proof-level theorem (OPT §3.?) |
| interpolation crossover | 168 | add | genetic algorithms and population methods (selection, crossover, mutation) [maths] -> MA 07-optimisation, new Note after MA-068. OPT §9.2 |
| inverse barrier | 199 | taught | RO #194 (log-barrier methods) |
| irreducible uncertainty | 427 | out-of-scope | uncertainty taxonomy (OPT §17.1) |
| iterates | 61 | taught | ML-056 Gradient descent (iterates) [hand-checked] |
| Kahn’s algorithm | 518 | out-of-scope | graph algorithm used for MDO ordering (OPT §21.?) |
| kernel | 391 | taught | robotics.md §4 new ML "Gaussian processes" (kernel); ML-089 |
| keyword argument | 556 | index-noise | Julia language feature (OPT appendix A) |
| k-fold cross-validation | 378 | taught | ML-012 (cross-validation, k-fold); MA-043 |
| KKT conditions | 194 | taught | MA-068 (KKT); recap robotics.md §5 |
| knapsack problem | 475 | out-of-scope | combinatorial example problem (OPT §19.?) |
| Kullback-Leibler divergence | 149 | taught | robotics.md §4 new MA "KL divergence"; DL-014 [hand-checked] |
| Kullback–Leibler divergence | 144 | taught | robotics.md §4 new MA "KL divergence"; DL-014 [hand-checked] |
| L-BFGS | see Limited-memory BFGS | index-noise | cross-reference to "Limited-memory BFGS" |
| L2 regularization | 372 | taught | ML-062 Ridge regression (L2 penalty) |
| Lagrange multiplier | 191 | taught | MA-066 Lagrange multipliers |
| Lagrange multipliers | 189 | taught | MA-066 Lagrange multipliers |
| Lagrangian | 191 | taught | MA-066 Lagrange multipliers |
| Lamarckian learning | 179 | out-of-scope | evolutionary-computation variant (OPT §9.?) |
| lasso | 233, 372 | taught | ML-066 Lasso regression |
| Latin-hypercube sampling | 351 | out-of-scope | sampling-plan method (OPT §13.?) |
| Latin squares | 351 | out-of-scope | sampling-plan method (OPT §13.?) |
| LDL decomposition | 583 | out-of-scope | matrix factorisation variant (OPT appendix C); Cholesky is robotics.md §4 |
| leaped Halton method | 361 | out-of-scope | quasi-random sequence detail (OPT §13.?) |
| learning rate | see step factor | index-noise | cross-reference to "step factor" |
| least-squares problem | 274 | taught | ML-053 Multiple linear regression maths (least squares) |
| least-squares problem with linear inequality constraints | 278 | out-of-scope | constrained least-squares variant (OPT §12.?) |
| least absolute deviation problem | 229 | out-of-scope | L1 regression variant (OPT §10.?) |
| least distance program | 281 | out-of-scope | least-squares variant (OPT §12.?) |
| leave-one-out bootstrap estimate | 381 | out-of-scope | model-validation estimator variant (OPT §14.?) |
| leave-one-out cross-validation | 379 | out-of-scope | cross-validation variant (OPT §14.?) |
| leaving index | 260 | out-of-scope | simplex-algorithm vocabulary (OPT §11.2) |
| Lebesgue measure | 353 | out-of-scope | measure theory (OPT §13.?) |
| Legendre polynomials | 588 | out-of-scope | orthogonal-polynomial family (OPT §18.?) |
| Levenberg-Marquardt algorithm | 100 | taught | robotics.md §4 "Levenberg-Marquardt and robust losses (IRLS)" |
| lexicographic method | 330 | out-of-scope | multiobjective scalarisation variant (OPT §12.?) |
| Limited-memory BFGS | 105 | add | quasi-Newton methods: BFGS and L-BFGS [maths] -> MA 07-optimisation, new Note. OPT §6.3; L-BFGS is the large-problem default |
| limit supremum | 577 | out-of-scope | real-analysis term (OPT appendix C) |
| linear combination | 571 | taught | MA-052 Linear combinations, span and basis |
| linear model | 366 | taught | ML-052 Multiple linear regression (linear model) |
| linear program | 249 | taught | MA-068 Linear and quadratic programming |
| linear regression | 35, 366 | taught | ML-049 Simple linear regression |
| line search | 64 | mentioned-only | line search and one-dimensional minimisation (bracketing, golden section, backtracking, Wolfe conditions) [maths] -> MA 07-optimisation, new Note. OPT §4.2; MA-064 only names it |
| Lipschitz continuous | 53 | out-of-scope | real-analysis condition used in a global method (OPT §3.?), proof-level |
| local design variables | 524 | out-of-scope | multidisciplinary design optimisation (OPT ch.21) |
| local minimum | 10 | taught | MA-065 (local minimum) |
| local models | 61 | out-of-scope | optimisation-method framing (OPT §4.1) |
| logarithmic annealing schedule | 141 | add | local search: hill climbing, pattern search and simulated annealing [maths] -> MA 07-optimisation, new Note after MA-068. annealing schedule (OPT §8.?) |
| log barrier | 199 | taught | RO #194 (log-barrier methods) |
| log likelihood | 401 | taught | MA-070 Maximum likelihood estimation (log-likelihood) |
| loop | 558 | index-noise | Julia language feature (OPT appendix A) |
| low-discrepancy sequences | 359 | out-of-scope | sampling-plan method (OPT §13.?) |
| lower confidence bound | 413 | add | Bayesian optimisation acquisition functions: expected improvement, probability of improvement, confidence bounds [maths] -> ML-128 Optuna (section). OPT §16.? |
| lower confidence bound exploration | 413 | add | Bayesian optimisation acquisition functions: expected improvement, probability of improvement, confidence bounds [maths] -> ML-128 Optuna (section). OPT §16.? |
| LQ decomposition | 584 | out-of-scope | matrix factorisation variant (OPT appendix C) |
| Lévy flights | 177 | out-of-scope | research metaheuristic detail (OPT §9.?) |
| marginal distribution | 390 | taught | MA-014 (marginal distribution) |
| Markowitz portfolio optimization | 438 | out-of-scope | finance example problem (OPT §17.?) |
| matrix | 548 | taught | MA-053 Linear transformations and matrices |
| matrix decomposition | 582 | taught | MA-057, MA-058 (SVD as a decomposition); robotics.md §4 Cholesky |
| matrix factorization | see matrix decomposition | index-noise | cross-reference to "matrix decomposition" |
| matrix norm | 110 | out-of-scope | linear-algebra detail (OPT §6.?) |
| Matérn kernel | 392 | out-of-scope | GP kernel family variant (OPT §16.?) |
| max-min inequality | 210 | out-of-scope | duality inequality used in a proof (OPT §10.?) |
| maximum likelihood estimate | 401 | taught | MA-070 Maximum likelihood estimation |
| max norm | 577 | add | vector norms L1, L2 and L-infinity (Manhattan, Euclidean, Chebyshev) [maths] -> MA 05-linear-algebra, short section in MA-049. max norm (OPT appendix C) |
| MDO | see multidisciplinary design optimization | index-noise | cross-reference to "multidisciplinary design optimization" |
| mean | 434 | taught | MA-005 Measures of central tendency (mean) |
| mean excess loss | 436 | out-of-scope | risk-measure variant (OPT §17.?); CVaR is RO #198 |
| mean function | 391 | taught | robotics.md §4 new ML "Gaussian processes" (mean function) [hand-checked] |
| mean shortfall | 436 | out-of-scope | risk-measure variant (OPT §17.?); CVaR is RO #198 |
| mean squared error | 375 | taught | ML-051 Regression metrics (MSE) |
| memetic algorithms | 179 | out-of-scope | evolutionary-computation hybrid (OPT §9.?) |
| memoization | 475 | taught | DL-019 MLP memoization |
| memory-efficient zeroth-order optimizer | 139 | out-of-scope | research zeroth-order optimiser (OPT §8.?) |
| mesh adaptive direct search | 136 | out-of-scope | research direct method (OPT §7.?) |
| method of multipliers | 197 | add | augmented Lagrangian and ADMM [maths] -> MA 07-optimisation, new Note after MA-068. method of multipliers = augmented Lagrangian (OPT §10.?) |
| Metropolis criterion | 141 | add | local search: hill climbing, pattern search and simulated annealing [maths] -> MA 07-optimisation, new Note after MA-068. Metropolis acceptance rule of simulated annealing (OPT §8.?) |
| MeZO | see memory-efficient zeroth-order optimizer | index-noise | cross-reference to "memory-efficient zeroth-order optimizer" |
| Michalewicz function | 566 | out-of-scope | benchmark test function (OPT appendix B) |
| minimax | 429 | taught | RL #54 (minimax); RO #141 (worst case) |
| minimax decision | 343 | taught | RL #53 (worst-case decisions) |
| minimax regret | 343 | out-of-scope | decision-rule variant (OPT §12.?) |
| minimizer | 5 | taught | MA-065 (minimiser of a cost) [hand-checked] |
| minimum ratio test | 260 | out-of-scope | simplex-algorithm step (OPT §11.?) |
| mixed-integer program | 464 | add | integer programming and branch and bound [maths] -> MA 07-optimisation, new Note after MA-068. mixed-integer programs (OPT §19.?) appear in footstep planning and TAMP (RB #293, #306) |
| modified Bessel function of the second kind | 392 | out-of-scope | special function in the Matérn kernel (OPT §16.?) |
| momentum | 81 | taught | DL-034 SGD with momentum |
| monomial | 247 | out-of-scope | geometric-programming term (OPT §12.?) |
| Monte Carlo integration | 359, 443 | taught | robotics.md §4 new MA "Monte Carlo estimation" [hand-checked] |
| Morris-Mitchell criterion | 355 | out-of-scope | sampling-plan metric (OPT §13.?) |
| multidisciplinary analysis | 517 | out-of-scope | multidisciplinary design optimisation (OPT ch.21) |
| multidisciplinary design feasible | 521 | out-of-scope | multidisciplinary design optimisation (OPT ch.21) |
| multidisciplinary design optimization | 515 | out-of-scope | multidisciplinary design optimisation (OPT ch.21) |
| multifidelity surrogate model | 383 | out-of-scope | multifidelity-model term (OPT §14.?) |
| multimodal function | 43 | taught | MA-065 (non-convex, many minima); MA-073 (multimodal) |
| multiobjective optimization | 325 | taught | RL #53 (multi-objective optimisation) |
| multivariate | 61 | taught | MA-062 (functions of several variables) |
| multivariate function | 10 | taught | MA-062 (functions of several variables) |
| mutate | 545 | index-noise | Julia language feature (OPT appendix A) |
| mutation | 165 | add | genetic algorithms and population methods (selection, crossover, mutation) [maths] -> MA 07-optimisation, new Note after MA-068. OPT §9.2 |
| mutation rate | 170 | add | genetic algorithms and population methods (selection, crossover, mutation) [maths] -> MA 07-optimisation, new Note after MA-068. OPT §9.2 |
| mutually conjugate | 79 | taught | robotics.md §4 new MA "Sparse linear solves and conjugate gradient" [hand-checked] |
| named function | 555 | index-noise | Julia language feature (OPT appendix A) |
| named tuple | 552 | index-noise | Julia language feature (OPT appendix A) |
| natural evolution strategies | 149 | out-of-scope | research variant of evolution strategies (OPT §8.?); RL #43 teaches ES |
| natural gradient | 97, 149 | taught | RL #38; robotics.md §4 "Natural gradient and Fisher information" |
| necessary | 11 | out-of-scope | logic vocabulary (OPT §1.?) |
| Nelder-Mead simplex method | 119 | add | local search: hill climbing, pattern search and simulated annealing [maths] -> MA 07-optimisation, new Note after MA-068. Nelder-Mead simplex is the common derivative-free method (OPT §7.5) |
| Nesterov momentum | 82 | taught | DL-035 Nesterov accelerated gradient |
| neural network kernel | 392 | out-of-scope | GP kernel family variant (OPT §16.?) |
| Newton’s method | 96 | taught | MA-064 (Newton's method, glossary G-1321) |
| niche | 339 | out-of-scope | multiobjective population detail (OPT §12.?) |
| niche techniques | 339 | out-of-scope | multiobjective population detail (OPT §12.?) |
| no free lunch theorems | 7 | out-of-scope | theory result (OPT §1.?) |
| non-basic | 257 | out-of-scope | simplex-algorithm vocabulary (OPT §11.2) |
| nondomination ranking | 336 | out-of-scope | multiobjective population detail (OPT §12.?) |
| nonnegative least-squares quadratic program | 282 | out-of-scope | least-squares variant (OPT §12.?) |
| nonparametric | 402 | taught | MA-023 (nonparametric density estimation) [hand-checked] |
| nonterminal | 489 | out-of-scope | expression optimisation, a different field (OPT ch.20) |
| nonterminal symbols | 489 | out-of-scope | expression optimisation, a different field (OPT ch.20) |
| norm | 577 | taught | MA-049 (magnitude/norm) |
| normal distribution | 389, 586 | taught | MA-024 Normal distribution |
| normal equation | 385 | taught | ML-053 Multiple linear regression maths (normal equation) |
| numerical differentiation | 26 | taught | MA-061 (finite differences) |
| objective function | 5 | taught | ML-056 Gradient descent (objective/cost function) [hand-checked] |
| operation overloading | 35 | index-noise | Julia language feature (OPT appendix A) |
| opportunistic | 119 | out-of-scope | direct-method detail (OPT §7.?) |
| optimal substructure | 474 | taught | RL #10 (principle of optimality) |
| optimization phase | 258, 262 | out-of-scope | simplex-algorithm phase (OPT §11.?) |
| order | 571 | taught | RO #103 (Big-O) |
| orthogonal | 447 | taught | MA-050 Dot product (orthogonal vectors) |
| orthogonal matrix | 584 | taught | MA-057 SVD geometry (orthogonal matrices) |
| orthonormal matrix | see orthogonal matrix | index-noise | cross-reference to "orthogonal matrix" |
| outer product approximation | 102 | out-of-scope | quasi-Newton detail (OPT §6.?) |
| outgoing neighbors | 478 | add | graph basics: directed and undirected graphs, paths, cycles, DAGs, trees (parent, child) [maths] -> RO-05, short section in Note #103 Graphs and uninformed search. Note #103 lists 'graph as a model of a state space' only; Bayes nets, factor graphs (RO #263), roadmaps and search trees all need this vocabulary (DM appendix A, OPT §19) |
| over-constrained | 252 | out-of-scope | linear-system vocabulary (OPT §11.?) |
| overfitting | 232, 375 | taught | ML-061 Bias-variance (overfitting) |
| overlapping subproblems | 474 | taught | RL-02 (dynamic programming); DL-019 |
| package | 560 | index-noise | Julia language feature (OPT appendix A) |
| paired query selection | 342 | out-of-scope | preference-elicitation detail (OPT §12.?) |
| pairwise distances | 353 | out-of-scope | sampling-plan metric (OPT §13.?) |
| parametric | 402 | taught | MA-070 (parametric models) |
| parametric types | 554 | index-noise | Julia language feature (OPT appendix A) |
| Pareto curve | 327 | taught | RL #53 (Pareto-optimal) |
| Pareto filter | 336 | out-of-scope | multiobjective population detail (OPT §12.?) |
| Pareto frontier | 327 | taught | RL #53 (Pareto-optimal) |
| Pareto optimality | 325, 327 | taught | RL #53 (Pareto-optimal) |
| parsimony | 493 | out-of-scope | expression optimisation, a different field (OPT ch.20) |
| partial derivative | 25 | taught | MA-062 Partial derivatives and gradients |
| partially observable Markov decision process | 411 | taught | RO #153 POMDPs and belief space |
| particle | 172 | out-of-scope | metaheuristic family (OPT §9.?) |
| particle swarm optimization | 172 | out-of-scope | metaheuristic family (OPT §9.?) |
| partitioned canonical form | 310 | out-of-scope | LP standard-form vocabulary (OPT §11.?) |
| pattern | 117 | add | local search: hill climbing, pattern search and simulated annealing [maths] -> MA 07-optimisation, new Note after MA-068. pattern search (OPT §7.4) |
| pattern search | 113 | add | local search: hill climbing, pattern search and simulated annealing [maths] -> MA 07-optimisation, new Note after MA-068. OPT §7.4 |
| penalty methods | 195 | taught | RO #194 (exact penalty methods) |
| pheromone | 477 | out-of-scope | metaheuristic detail (OPT §19.?) |
| pivoting | 260 | out-of-scope | simplex-algorithm step (OPT §11.?) |
| Polak-Ribière | 81 | out-of-scope | conjugate-gradient variant (OPT §5.?) |
| polyhedral method | 343 | out-of-scope | preference-elicitation detail (OPT §12.?) |
| polynomial basis functions | 369 | taught | ML-060 Polynomial regression (polynomial features) |
| polynomial chaos | 445 | out-of-scope | research uncertainty-propagation method (OPT §18.?) |
| polytopes | 256 | taught | MA-068 (feasible polytope of an LP) |
| population methods | 163 | add | genetic algorithms and population methods (selection, crossover, mutation) [maths] -> MA 07-optimisation, new Note after MA-068. OPT ch.9 |
| positive definite | 582 | taught | MA-064 (positive definite Hessian) |
| positive definiteness | 582 | taught | MA-064 (positive definite Hessian) |
| positive semidefinite | 582 | taught | MA-068 (positive semidefinite); MA-067 [hand-checked] |
| positive spanning set | 117 | out-of-scope | pattern-search theory detail (OPT §7.?) |
| possibility theory | 428 | out-of-scope | different field: possibility theory (OPT §17.?) |
| posterior distribution | 395 | taught | MA-018 Bayes' theorem (posterior) |
| Powell’s method | 115 | out-of-scope | direct-method variant (OPT §7.3) |
| prediction-based exploration | 411 | add | Bayesian optimisation acquisition functions: expected improvement, probability of improvement, confidence bounds [maths] -> ML-128 Optuna (section). OPT §16.? |
| preference elicitation | 340 | out-of-scope | preference elicitation (OPT §12.?) |
| primal-dual method | 213 | out-of-scope | interior-point variant (OPT §10.?); interior point named in RO #208 |
| primal | 193 | taught | MA-066 (primal and dual) |
| primal form | 210 | taught | MA-066 (primal and dual) |
| primal residual | 220 | out-of-scope | ADMM convergence detail (OPT §10.?) |
| primal value | 210 | taught | MA-066 (primal value) |
| prime analytic center | 342 | out-of-scope | preference-elicitation detail (OPT §12.?) |
| priority queue | 471 | taught | RO #104 Dijkstra's algorithm and priority queues |
| probabilistic grammar | 501 | out-of-scope | expression optimisation, a different field (OPT ch.20) |
| probabilistic prototype tree | 502 | out-of-scope | expression optimisation, a different field (OPT ch.20) |
| probabilistic uncertainty | 432 | out-of-scope | uncertainty taxonomy (OPT §17.?) |
| probability of improvement | 414 | add | Bayesian optimisation acquisition functions: expected improvement, probability of improvement, confidence bounds [maths] -> ML-128 Optuna (section). OPT §16.? |
| product-free expressions | 301 | out-of-scope | convex-modelling tool detail (OPT §12.?) |
| product correlation rule | 456 | out-of-scope | uncertainty-propagation detail (OPT §18.?) |
| production rules | 489 | out-of-scope | expression optimisation, a different field (OPT ch.20) |
| projected descent | 189 | out-of-scope | constrained-descent variant (OPT §10.?) |
| proposal distribution | 144 | taught | robotics.md §4 new MA "Importance sampling" (proposal); RL #43 (CEM) |
| proposal distribution descent | 148 | out-of-scope | stochastic-method variant (OPT §8.?) |
| proximal minimization | 224 | out-of-scope | proximal-operator detail (OPT §10.?) |
| pruning | 500 | taught | RL #54 (alpha-beta pruning) |
| pseudo-random | 135 | taught | plan §4 "Drawing samples from distributions" [hand-checked] |
| pseudoinverse | 277, 367 | taught | MA-060 SVD in ML (pseudo-inverse) |
| Q-Eval | 342 | out-of-scope | preference-elicitation detail (OPT §12.?) |
| QR decomposition | 584 | mentioned-only | QR decomposition for least squares [maths] -> MA 05-linear-algebra, short section after MA-058. MA-047 only names it; numerically stable least squares in calibration and SLAM solvers (OPT appendix C) |
| quadratic convergence | 96 | out-of-scope | convergence-rate term (OPT §6.?) |
| quadratic fit search | 51 | add | line search and one-dimensional minimisation (bracketing, golden section, backtracking, Wolfe conditions) [maths] -> MA 07-optimisation, new Note. quadratic fit search (OPT §3.5) |
| quadratic penalties | 196 | taught | RO #194 (exact penalty methods) |
| quadratic program | 273 | taught | MA-068 Linear and quadratic programming |
| quadrature rule | 586 | out-of-scope | numerical-integration rule (OPT appendix C) |
| quantile | 436 | taught | MA-008 Percentiles (quantiles) |
| quasi-Monte Carlo methods | 359 | out-of-scope | sampling-plan method (OPT §13.?) |
| quasi-Newton | 103 | add | quasi-Newton methods: BFGS and L-BFGS [maths] -> MA 07-optimisation, new Note. OPT ch.6 |
| quasi-random sequences | 359 | out-of-scope | sampling-plan method (OPT §13.?) |
| radial function | 371 | taught | RL #26 (RBF features) |
| randomized rounding | 465 | out-of-scope | integer-programming heuristic (OPT §19.?) |
| random restarts | 74 | out-of-scope | global-search restart detail (OPT §4.?) |
| random sampling | 350 | taught | plan §4 "Drawing samples from distributions" [hand-checked] |
| random subsampling | 377 | out-of-scope | model-validation method variant (OPT §14.?) |
| random uncertainty | see irreducible uncertainty | index-noise | cross-reference to "irreducible uncertainty" |
| real part | 32 | out-of-scope | complex-step detail (OPT §2.3) |
| reducible uncertainty | see epistemic uncertainty | index-noise | cross-reference to "epistemic uncertainty" |
| regression | 366 | taught | ML-049 Simple linear regression (regression) |
| regret | 343 | out-of-scope | decision-rule variant (OPT §12.?) |
| regularization | 232 | taught | ML-062 Ridge regression; DL-026 |
| regularization term | 372 | taught | ML-062 Ridge regression (penalty term) |
| relax | 465 | add | integer programming and branch and bound [maths] -> MA 07-optimisation, new Note after MA-068. LP relaxation of an integer program (OPT §19.?) |
| residual form | 534 | out-of-scope | multidisciplinary design optimisation (OPT ch.21) |
| response variables | 515 | out-of-scope | multidisciplinary design optimisation (OPT ch.21) |
| restricted step method | 71 | taught | RL #38 (trust region) |
| reverse accumulation | 31, 33 | taught | DL-015 Backpropagation (reverse mode) [hand-checked] |
| ridge regression | 372 | taught | ML-062 Ridge regression |
| risk measure | 436 | out-of-scope | risk-measure axioms (OPT §17.?); CVaR is RO #198 |
| RMSProp | 84 | taught | DL-037 RMSprop |
| robust | 436 | taught | RO #141 Robust RL |
| robust counterpart approach | see minimax | index-noise | cross-reference to "minimax" |
| robust regularization | see minimax | index-noise | cross-reference to "minimax" |
| root-finding methods | 57 | taught | robotics.md §4 "Newton-Raphson root finding" [hand-checked] |
| root mean squared error | 383 | taught | ML-051 Regression metrics (RMSE) |
| roots | 57 | taught | robotics.md §4 "Newton-Raphson root finding" |
| Rosenbrock function | 567 | out-of-scope | benchmark test function (OPT appendix B) |
| rotation estimation | 378 | out-of-scope | model-validation method variant (OPT §14.?) |
| roulette wheel selection | 165 | add | genetic algorithms and population methods (selection, crossover, mutation) [maths] -> MA 07-optimisation, new Note after MA-068. OPT §9.2 |
| rounding | 465 | out-of-scope | integer-programming heuristic (OPT §19.?) |
| saddle | 12 | taught | MA-064 (saddle points) |
| safe exploration | 416 | taught | RO #200 Safe exploration with an uncertainty model |
| SafeOpt | 416 | taught | RO #200 (SafeOpt) |
| sample mean | 443 | taught | MA-005 (mean) |
| sample variance | 443 | taught | MA-006 (variance) |
| sampling plans | 18, 349 | out-of-scope | sampling-plan method (OPT §13.?) |
| scaled dual variable | 223 | out-of-scope | ADMM detail (OPT §10.?) |
| scaled form | 222 | out-of-scope | ADMM detail (OPT §10.?) |
| secant equation | 110 | add | quasi-Newton methods: BFGS and L-BFGS [maths] -> MA 07-optimisation, new Note. secant equation behind quasi-Newton (OPT §6.?) |
| secant method | 97 | add | quasi-Newton methods: BFGS and L-BFGS [maths] -> MA 07-optimisation, new Note. secant method (OPT §6.2) |
| second-order | 95 | taught | MA-064 Hessian (second-order) |
| second-order necessary condition | 11 | taught | MA-065 (second-order conditions); MA-064 |
| second-order sufficient condition | 14 | taught | MA-064 (positive definite Hessian at a minimum) |
| second order cone program | 311 | add | second-order cone programs (SOCP) [maths] -> MA 07-optimisation, short section after MA-068. OPT §10.? |
| self-dual simplex algorithm | 267 | out-of-scope | simplex-algorithm variant (OPT §11.?) |
| semidefinite programming | 185 | out-of-scope | semidefinite programming (OPT §10.?); used in certifiable-SLAM research, no plan Note uses it |
| sensitive | 436 | out-of-scope | risk-measure term (OPT §17.?) |
| sequential optimization | 524 | out-of-scope | multidisciplinary design optimisation (OPT ch.21) |
| set-based uncertainty | 429 | out-of-scope | uncertainty taxonomy (OPT §17.?) |
| Shubert-Piyavskii method | 53 | out-of-scope | global Lipschitz method (OPT §3.?) |
| sign | 301 | index-noise | notation (sign function) |
| simplex | 119 | add | local search: hill climbing, pattern search and simulated annealing [maths] -> MA 07-optimisation, new Note after MA-068. Nelder-Mead simplex (OPT §7.5) |
| simplex algorithm | 255 | taught | MA-068 (simplex method) |
| simulated annealing | 140 | mentioned-only | local search: hill climbing, pattern search and simulated annealing [maths] -> MA 07-optimisation, new Note after MA-068. OPT §8.4; ML-058 only names it |
| simultaneous analysis and design | 534 | out-of-scope | multidisciplinary design optimisation (OPT ch.21) |
| simultaneous perturbation stochastic approximation | 35 | add | gradient estimation by random perturbation (SPSA) [maths] -> MA 07-optimisation, short section with finite differences. OPT §2.? |
| simultaneous perturbation stochastic gradient approximation | 37 | add | gradient estimation by random perturbation (SPSA) [maths] -> MA 07-optimisation, short section with finite differences. OPT §2.? |
| single-point crossover | 168 | add | genetic algorithms and population methods (selection, crossover, mutation) [maths] -> MA 07-optimisation, new Note after MA-068. OPT §9.2 |
| singular value decomposition | 276, 585 | taught | MA-057 SVD geometry |
| singular values | 585 | taught | MA-057 SVD geometry (singular values) |
| sinusoidal basis functions | 370 | add | Fourier series and the Fourier transform (frequency content of a signal) [maths] -> MA 06-calculus, new Note. sinusoidal basis functions (OPT §14.?) |
| six-sigma | 441 | out-of-scope | quality-engineering term (OPT §17.?) |
| slack | 194 | out-of-scope | LP vocabulary (OPT §10.?) |
| slack variable | 195 | out-of-scope | LP vocabulary (OPT §10.?) |
| Slater’s condition | 210 | out-of-scope | duality condition used in proofs (OPT §10.?) |
| Sobol sequences | 361 | out-of-scope | quasi-random sequence (OPT §13.?) |
| soft thresholding operator | 230 | out-of-scope | sparse-recovery operator (OPT §10.?) |
| solution | 5 | taught | ML-056 Gradient descent (solution of an optimisation) [hand-checked] |
| space-filling | 349 | out-of-scope | sampling-plan term (OPT §13.?) |
| space-filling metrics | 352 | out-of-scope | sampling-plan metric (OPT §13.?) |
| space-filling subsets | 356 | out-of-scope | sampling-plan term (OPT §13.?) |
| specification | 4 | out-of-scope | engineering-design vocabulary (OPT §1.?) |
| splat | 557 | index-noise | Julia language feature (OPT appendix A) |
| split Bregman method | 231 | out-of-scope | sparse-recovery method (OPT §10.?) |
| SPSA | see simultaneous perturbation stochastic gradient approximation | index-noise | cross-reference to SPSA |
| square-root-free Cholesky decomposition | see LDL decomposition | index-noise | cross-reference to "LDL decomposition" |
| squared exponential kernel | 392 | taught | ML-089 Kernel trick (RBF kernel); robotics.md §4 GPs |
| standard deviation | 396 | taught | MA-006 Measures of dispersion |
| standard form | 251 | out-of-scope | LP standard-form vocabulary (OPT §11.1) |
| standard normal cumulative distribution function | 414 | taught | MA-025 Standard normal and z-table |
| start type | 489 | out-of-scope | expression optimisation, a different field (OPT ch.20) |
| stationary point | 11, 78 | taught | MA-065 (stationary points) |
| statistical feasibility | 436 | out-of-scope | robust-design term (OPT §17.?) |
| steepest descent | 77 | taught | ML-056 Gradient descent [hand-checked] |
| step factor | 62 | taught | ML-056 (learning rate as step size) |
| step size | 62 | taught | ML-056 (learning rate as step size) |
| Stieltjes algorithm | 450 | out-of-scope | orthogonal-polynomial construction (OPT §18.?) |
| stochastic gradient descent | 135 | taught | ML-058 Stochastic gradient descent |
| stochastic methods | 135 | out-of-scope | chapter pointer (OPT ch.8) |
| stratified sampling | 352 | out-of-scope | sampling-plan method (OPT §13.?) |
| strict local minimizer | 10 | taught | MA-065 (local minimum) |
| strictly concave | 576 | out-of-scope | proof-level property (OPT appendix C) |
| strictly convex | 575 | out-of-scope | proof-level property (OPT appendix C) |
| string | 543 | index-noise | Julia language feature (OPT appendix A) |
| strong backtracking line search | 68 | add | line search and one-dimensional minimisation (bracketing, golden section, backtracking, Wolfe conditions) [maths] -> MA 07-optimisation, new Note. OPT §4.4 |
| strong curvature condition | 68 | add | line search and one-dimensional minimisation (bracketing, golden section, backtracking, Wolfe conditions) [maths] -> MA 07-optimisation, new Note. OPT §4.4 |
| strong duality | 210 | taught | MA-066 (strong duality) |
| strong local minima | 10 | taught | MA-065 (local minimum) |
| strong local minimizer | 10 | taught | MA-065 (local minimum) |
| strongly typed genetic programming | 493 | out-of-scope | expression optimisation, a different field (OPT ch.20) |
| strong Wolfe conditions | 68 | add | line search and one-dimensional minimisation (bracketing, golden section, backtracking, Wolfe conditions) [maths] -> MA 07-optimisation, new Note. OPT §4.4 |
| subdifferential, Clarke | 579 | out-of-scope | nonsmooth analysis (OPT appendix C) |
| subdifferential | 579 | out-of-scope | nonsmooth analysis (OPT appendix C) |
| subgradient | 579 | out-of-scope | nonsmooth analysis (OPT appendix C) |
| submatrix | 465 | out-of-scope | linear-algebra vocabulary (OPT §19.?) |
| suboptimizer | 521 | out-of-scope | multidisciplinary design optimisation (OPT ch.21) |
| subpopulations | 334 | out-of-scope | multiobjective population detail (OPT §12.?) |
| subproblem | 524 | out-of-scope | multidisciplinary design optimisation (OPT ch.21) |
| sufficient closeness | 97 | out-of-scope | Newton-convergence condition (OPT §6.?) |
| sufficient decrease | 65 | add | line search and one-dimensional minimisation (bracketing, golden section, backtracking, Wolfe conditions) [maths] -> MA 07-optimisation, new Note. Armijo sufficient-decrease rule (OPT §4.2) |
| supremum | 353 | out-of-scope | real-analysis term (OPT §13.?) |
| surrogate model | 349 | taught | robotics.md §4 new ML "Gaussian processes" (surrogate) [hand-checked] |
| surrogate models | 365 | taught | robotics.md §4 new ML "Gaussian processes" (surrogate) [hand-checked] |
| symbolic differentiation | 24 | out-of-scope | differentiation method (OPT §2.?); symbolic algebra is not used by any plan Note |
| symbols | 489 | out-of-scope | expression optimisation, a different field (OPT ch.20) |
| system-level optimizer | 524 | out-of-scope | multidisciplinary design optimisation (OPT ch.21) |
| tail value at risk | 436 | out-of-scope | risk-measure variant (OPT §17.?); CVaR is RO #198 |
| taxicab search | 113 | out-of-scope | direct-method variant (OPT §7.?) |
| Taylor approximation | 574 | taught | MA-064 Hessian and multivariate Taylor |
| Taylor expansion | 573 | taught | MA-064 Hessian and multivariate Taylor |
| Taylor series | 573 | taught | MA-061 (Taylor series) |
| Temperature | 140 | add | local search: hill climbing, pattern search and simulated annealing [maths] -> MA 07-optimisation, new Note after MA-068. annealing temperature (OPT §8.4) |
| terminal | 489 | out-of-scope | expression optimisation, a different field (OPT ch.20) |
| terminal symbols | 489 | out-of-scope | expression optimisation, a different field (OPT ch.20) |
| ternary operator | 558 | index-noise | Julia language feature (OPT appendix A) |
| test functions | 561 | out-of-scope | benchmark test functions (OPT appendix B) |
| test set | 377 | taught | ML-012 (train/test split) |
| tight | 194 | taught | MA-068 (tight/active constraints, KKT) |
| topological ordering | 518 | out-of-scope | graph algorithm used for MDO ordering (OPT §21.?) |
| totally unimodular | 466 | out-of-scope | integer-programming theory (OPT §19.?) |
| tournament selection | 165 | add | genetic algorithms and population methods (selection, crossover, mutation) [maths] -> MA 07-optimisation, new Note after MA-068. OPT §9.2 |
| trace | 401 | out-of-scope | matrix trace in a GP formula (OPT §16.?) |
| training error | 375 | taught | ML-061 (training error) |
| training set | 377 | taught | ML-012 (training set) |
| traveling salesman problem | 477 | out-of-scope | combinatorial example problem (OPT §19.?) |
| tree crossover | 493 | out-of-scope | expression optimisation, a different field (OPT ch.20) |
| tree mutation | 493 | out-of-scope | expression optimisation, a different field (OPT ch.20) |
| tree permutation | 495 | out-of-scope | expression optimisation, a different field (OPT ch.20) |
| triangle inequality | 577 | taught | RO #108 (metric space) |
| truncation selection | 165 | add | genetic algorithms and population methods (selection, crossover, mutation) [maths] -> MA 07-optimisation, new Note after MA-068. OPT §9.2 |
| trust region | 71 | taught | RL #38 (trust region) |
| tuple | 551 | index-noise | Julia language feature (OPT appendix A) |
| two-point crossover | 168 | add | genetic algorithms and population methods (selection, crossover, mutation) [maths] -> MA 07-optimisation, new Note after MA-068. OPT §9.2 |
| types | 489 | out-of-scope | expression optimisation, a different field (OPT ch.20) |
| uncertainty propagation | 443 | add | uncertainty propagation through a function (Monte Carlo, linearisation, sigma points) as one idea [maths] -> MA 04-inference, new Note after robotics.md §4 "Monte Carlo estimation". OPT ch.18; RO #81 and #256 each teach one way inside a filter, no Note compares them |
| uniform crossover | 168 | add | genetic algorithms and population methods (selection, crossover, mutation) [maths] -> MA 07-optimisation, new Note after MA-068. OPT §9.2 |
| uniform projection plan | 351 | out-of-scope | sampling-plan method (OPT §13.?) |
| unimodal function | 43 | out-of-scope | 1-D search assumption (OPT §3.?) |
| unimodality | 43 | out-of-scope | 1-D search assumption (OPT §3.?) |
| univariate function | 10 | taught | MA-061 Derivatives of one variable (univariate functions) [hand-checked] |
| univariate Gaussian | 586 | taught | MA-024 Normal distribution [hand-checked] |
| utopia point | 327 | out-of-scope | multiobjective vocabulary (OPT §12.?) |
| value at risk | 436 | add | value at risk (VaR), the quantile beside CVaR [maths] -> robotics.md §4 short section "Conditional value at risk" (RO #198). OPT §17.?; CVaR is defined from VaR |
| van der Corput sequences | 360 | out-of-scope | quasi-random sequence (OPT §13.?) |
| VaR | see value at risk | index-noise | cross-reference to "value at risk" |
| variance | 434 | taught | MA-006 (variance) |
| vector | 544 | taught | MA-048 Vectors |
| vector evaluated genetic algorithm | 334 | out-of-scope | multiobjective population variant (OPT §12.?) |
| vector optimization | 325 | taught | RL #53 (multi-objective optimisation) |
| verification | 298 | out-of-scope | engineering-design term (OPT §12.?) |
| vertices | 256 | taught | MA-068 (vertices of the feasible region) |
| warm start | 61 | add | warm-starting a solver from the last solution [control] -> RO-15, section in Note #208 Nonlinear MPC and solving it in real time. OPT §4.1; real-time MPC depends on it |
| weak duality | 210 | taught | MA-066 (weak duality) |
| weak local minima | 10 | out-of-scope | real-analysis term (OPT §1.?) |
| weakly Pareto-optimal | 327 | out-of-scope | multiobjective vocabulary (OPT §12.?) |
| weighted exponential sum | 332 | out-of-scope | multiobjective scalarisation variant (OPT §12.?) |
| weighted min-max method | 333 | out-of-scope | multiobjective scalarisation variant (OPT §12.?) |
| weighted sum method | 331 | add | scalarising several objectives: weighted sum and the constraint method [maths] -> RL-07, section in Note #53 Decisions against nature. OPT §12.?; rewards and MPC costs are weighted sums |
| weighted Tchebycheff method | 333 | out-of-scope | multiobjective scalarisation variant (OPT §12.?) |
| Wheeler’s ridge | 568 | out-of-scope | benchmark test function (OPT appendix B) |
| whitening | 445 | out-of-scope | uncertainty-propagation detail (OPT §18.?) |
| Wolfe conditions | 65 | add | line search and one-dimensional minimisation (bracketing, golden section, backtracking, Wolfe conditions) [maths] -> MA 07-optimisation, new Note. OPT §4.4 |
| zero-order | 113 | add | local search: hill climbing, pattern search and simulated annealing [maths] -> MA 07-optimisation, new Note after MA-068. zero-order (derivative-free) methods (OPT ch.7) |
| zero-order stochastic step | 139 | out-of-scope | research zeroth-order optimiser (OPT §8.?) |
| zoom phase | 70 | add | line search and one-dimensional minimisation (bracketing, golden section, backtracking, Wolfe conditions) [maths] -> MA 07-optimisation, new Note. zoom phase of strong Wolfe search (OPT §4.4) |
