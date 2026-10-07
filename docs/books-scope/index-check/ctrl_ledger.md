# ctrl ledger: index-based completeness check

Sources (official free PDFs, no sign-in; saved in `pdf/`):

- FBS: Åström & Murray, *Feedback Systems*, 2nd ed., v3.1.5 (2020-07-24). http://www.cds.caltech.edu/~murray/books/AM08/pdf/fbs-public_24Jul2020.pdf, linked from the authors' wiki https://fbswiki.org/wiki/index.php/Main_Page. Index pp. I-1 to I-16 (PDF pp. 558-573).
- LNS: Bullo, *Lectures on Network Systems*, ed. 1.7 (Apr 2024). Author page https://fbullo.github.io/lns/ links the PDF on UCSB Box https://ucsb.box.com/v/LecturesNetworkSystems. Subject index pp. 317-320 (PDF pp. 329-332).
- MML: Deisenroth, Faisal & Ong, *Mathematics for Machine Learning* (CUP 2020). https://mml-book.github.io/book/mml-book.pdf. Index pp. 407-411 (PDF pp. 413-417).

Method: `pdftotext -bbox-layout` per index page, split into columns by x-position, sub-entries joined to parents by indent (`ctrl/scripts/lines.py`, `parse.py`); every term matched by script against robotics.md, the eight evidence docs, MA/ML/DL Note bodies and glossary.md (`ctrl/scripts/match.py`, results in `ctrl/<book>_matches.json`); verdicts written by hand per term (`ctrl/v/<book>.tsv`) and assembled by `ctrl/scripts/build.py`, which fails if any term lacks a verdict.

Verdicts: taught / mentioned-only (treated as add) / add / out-of-scope / index-noise. For add rows the bold key names the merged concept in `ctrl_adds.json`.

Counts: {"fbs": {"out-of-scope": 348, "index-noise": 180, "taught": 251, "add": 294}, "lns": {"add": 100, "index-noise": 27, "out-of-scope": 126, "taught": 47}, "mml": {"taught": 341, "out-of-scope": 89, "add": 28, "index-noise": 2}}

## Åström & Murray, Feedback Systems, 2nd ed. (v3.1.5, 2020-07-24)

Index pages parsed: 1073 terms. Pages are the book's own page labels.

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| acausal modeling | 3-7 | out-of-scope | modelling-software paradigm (acausal / equation-based tools), FBS §3.1 |
| access control |  (see admission control) | index-noise | cross-reference |
| acknowledgment (ack) packet | 4-14–4-16 | out-of-scope | application example from another field (networking / biology) |
| activator | 1-13, 3-41 (see also biological circuits) | out-of-scope | application example from another field (networking / biology) |
| active filter | 6-23 (see also operational amplifier) | out-of-scope | electronics (op-amp filter circuits), different field |
| actuator |  | taught | Note 119 (actuator saturation), Note 139 (actuator models) |
| actuator, saturation | 15-3 | taught | Note 119 (saturation), Note 139 (actuator models) |
| actuators | 1-5, 1-6, 3-6, 3-30, 4-1, 4-17, 8-30, 10-20, 11-22, 12-11, 14-4, 14-7, 14-13, 14-15 | taught | Note 119 (saturation), Note 139 (actuator models) |
| actuators, effect on zeros | 10-20, 14-4 | out-of-scope | design insight on actuator placement and zeros (FBS §14.1), advanced |
| actuators, in computing systems | 4-11 | out-of-scope | application example from computing systems |
| actuators, saturation | 3-9, 8-31, 11-9, 11-15–11-17, 11-22, 12-11, 14-26–14-28 | taught | Note 119 (actuator saturation and windup) |
| A/D converters |  (see analog-to-digital converters) | index-noise | cross-reference |
| adaptation | 11-6, 15-29 | out-of-scope | adaptation in biology/adaptive control (FBS §15.4 overview); RL adaptation is Notes 167-171 |
| adaptive control | 13-28 | out-of-scope | adaptive control: plan §7 drops ME-069 with a reason |
| additive uncertainty | 13-3, 13-9, 13-12, 13-13 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. additive uncertainty |
| adjacency matrix | 3-38 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. adjacency matrix (FBS §3.4 consensus example) |
| admission control | 3-35, 3-47, 4-14, 4-15, 10-8 | out-of-scope | application example from computing systems (admission control) |
| aerospace systems | 1-8, 1-15, 14-7, 15-38 (see also vectored thrust aircraft; X-29 aircraft) | out-of-scope | application domain (aerospace) pointer |
| AFM |  (see atomic force microscopes) | index-noise | cross-reference |
| air-fuel ratio control | 1-23 | out-of-scope | application example (engine control) |
| aircraft |  (see flight control) | index-noise | cross-reference |
| alcohol, metabolism of | 4-30 | out-of-scope | application example from biology |
| algebraic loops | 3-26, 9-22–9-23 | out-of-scope | simulation artefact in block diagrams (algebraic loops), modelling-software detail |
| aliasing | 8-31 | add | **sampling** → RO-08, extend Note 136 (Delays and control rate), or RO-06 after the PID Notes. aliasing |
| all-pass transfer function | 14-10 | out-of-scope | all-pass transfer functions: fundamental-limits theory (FBS §14.2) |
| alternating current (AC) | 6-25 | out-of-scope | electrical engineering (AC circuits), different field |
| amplifier |  (see operational amplifier) | index-noise | cross-reference |
| amplitude ratio |  (see gain) | index-noise | cross-reference |
| analog computing | 3-9, 3-26, 4-8, 9-23, 11-20 | out-of-scope | history (analog computers) |
| analog implementation, of controllers | 4-10, 9-41, 11-20–11-22 | out-of-scope | electronics implementation of controllers (op amps) |
| analog-to-digital converters | 1-5, 1-6, 4-18, 8-30, 8-31, 11-22 | add | **sampling** → RO-08, extend Note 136 (Delays and control rate), or RO-06 after the PID Notes. analog-to-digital converters |
| angle, of frequency response |  (see phase) | index-noise | cross-reference |
| anticipation, in controllers | 1-20, 11-5 (see also derivative action) | taught | Note 117 (derivative action as anticipation) |
| antiresonance | 6-26 | out-of-scope | detail of a mechanical example (FBS p.6-26) |
| anti-windup compensation | 1-19, 11-16–11-18, 11-22, 11-23, 11-26 | taught | Note 119 (integrator windup and anti-windup) |
| anti-windup compensation, stability analysis | 11-26 | out-of-scope | stability proof of anti-windup schemes, advanced |
| Apache web server | 4-12 (see also web server control) | out-of-scope | application example from computing systems |
| Arbib, M. A. | 7-1 | index-noise | person |
| architectures, for control systems | 1-16, 1-23–1-27, 2-19, 8-23–8-24, 13-14, 15-39, 15-42 | taught | Note 126 (layered autonomy stack) |
| architectures, for control systems, bottom up | 15-17–15-24 | out-of-scope | systems-engineering design processes (FBS ch.15) |
| architectures, for control systems, top down | 15-6–15-17 | out-of-scope | systems-engineering design processes (FBS ch.15) |
| argument, of a complex number | 9-29 | add | **complex** → MA 06-calculus, new Note before the planned ODEs and State-space models Notes (plan §4). argument (angle) of a complex number |
| arrival rate (queuing systems) | 3-36 | out-of-scope | queuing systems, different field |
| artifical neural network (ANN) | 15-34 | taught | DL-002 (artificial neural networks) |
| artificial pancreas | 4-25 | out-of-scope | application example from medicine |
| asymptotes, in Bode plot | 9-32 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. Bode-plot asymptotes |
| asymptotic stability | 3-21, 5-8, 5-10, 5-12, 5-13, 5-18, 5-19, 5-22, 5-26, 5-27, 5-29, 6-10 | taught | plan §4 new maths: Stability of dynamical systems |
| asymptotic stability, discrete-time systems | 6-37 | add | **dtstab** → MA 06-calculus, extend the planned Stability of dynamical systems Note (plan §4). asymptotic stability of discrete-time systems |
| atmospheric dynamics |  (see environmental science) | index-noise | cross-reference |
| atomic force microscopes | 1-3, 3-30, 4-17–4-21 | out-of-scope | application example: atomic force microscope (FBS running example) |
| atomic force microscopes, contact mode | 4-17, 6-25 | out-of-scope | application example: atomic force microscope (FBS running example) |
| atomic force microscopes, horizontal positioning | 10-17–10-18, 13-19–13-21 | out-of-scope | application example: atomic force microscope (FBS running example) |
| atomic force microscopes, system identification | 9-38–9-39 | out-of-scope | application example: atomic force microscope (FBS running example) |
| atomic force microscopes, tapping mode | 4-17, 10-28, 11-8, 11-13–11-14, 12-16 | out-of-scope | application example: atomic force microscope (FBS running example) |
| atomic force microscopes, with preloading | 4-30 | out-of-scope | application example: atomic force microscope (FBS running example) |
| attractor (equilibrium point) | 5-10 | add | **eqtypes** → MA 06-calculus, extend the planned Stability of dynamical systems Note (plan §4). attractor |
| automatic reset, in PID control | 11-4, 11-5 | taught | Note 119 (integral action = automatic reset) |
| automatic tuning | 11-15, 13-28 | add | **pidtune** → RO-06, extend Note 117 (PD and PID control) or a new Note after Note 119. automatic tuning |
| automotive control systems | 1-18, 3-30, 4-5, 15-38–15-39 (see also cruise control; vehicle steering) | out-of-scope | application domain pointer (automotive) |
| autonomous differential equation | 3-3 (see also time-invariant systems) | taught | plan §4 new maths: ODEs and vector fields (time-invariant ODE) |
| autonomous vehicles | 1-9, 1-10, 1-27, 15-8–15-10, 15-29, 15-35, 15-38, 15-39 (see also robotics) | index-noise | pointer to application examples |
| autopilot | 1-15, 1-16 | out-of-scope | history (autopilots) |
| AUTOSAR | 15-39 | out-of-scope | automotive software standard, different field |
| average residence time | 11-7, 11-25 | out-of-scope | process-control measure used in tuning (FBS §11.2) |
| balance systems | 3-12–3-14, 3-29, 7-4–7-6, 7-23–7-24, 9-25–9-26, 14-14–14-15 (see also cart-pendulum system; inverted pendulum) | taught | Note 296 (inverted-pendulum balance models) |
| band-pass filter | 6-23–6-25, 9-35 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. band-pass filter |
| bandwidth | 2-18, 6-25, 12-6, 12-7, 12-32, 14-13 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. bandwidth |
| bandwidth, for second-order systems | 7-20 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. bandwidth |
| behavioral modeling | 3-7 | out-of-scope | modelling-software paradigm |
| Bell Labs | 1-15, 10-27, 12-30 | index-noise | organisation / person |
| Bennett, S. | 1-27, 10-27, 11-24 | index-noise | organisation / person |
| Bertram, J. | 7-33 | index-noise | organisation / person |
| bicycle dynamics | 4-5–4-8, 4-28, 5-31–5-32, 14-1, 14-19–14-20 | taught | Note 67 (bicycle model); Note 253 |
| bicycle dynamics, Whipple model | 4-7 | out-of-scope | detailed bicycle model (Whipple), beyond course level |
| bicycle model, for vehicle steering | 3-30–3-31 | taught | Note 67 (kinematic bicycle model) |
| bifurcations | 5-30–5-32 (see also root locus plots) | out-of-scope | bifurcation theory (FBS §5.4), nonlinear-dynamics topic beyond course level |
| biological circuits | 1-13, 3-24, 3-40–3-41, 5-38, 6-38, 9-36–9-37 | out-of-scope | application examples from biology |
| biological circuits, genetic switch | 3-47, 5-23 | out-of-scope | application examples from biology |
| biological circuits, repressilator | 3-41 | out-of-scope | application examples from biology |
| biological systems | 1-1, 1-3, 1-9, 1-12, 1-28, 3-40–3-44, 5-34, 11-2, 11-6 (see also biological circuits; drug administration; neural systems; population dynamics) | out-of-scope | application examples from biology |
| bistability | 5-25 | out-of-scope | application examples from biology |
| Black, H. S. | 1-8, 1-15, 4-8, 4-10, 6-2, 10-1, 10-27, 13-1 | index-noise | person |
| block diagonal form | 5-38 | add | **modes** → MA 06-calculus, inside the planned Matrix exponential Note (plan §4). block-diagonal (modal) form |
| block diagonal systems | 5-12, 5-13, 5-38, 6-9, 6-15, 6-19, 8-12 | add | **modes** → MA 06-calculus, inside the planned Matrix exponential Note (plan §4). block-diagonal (modal) form |
| block diagram algebra | 2-11, 9-17, 9-19, 13-12 | add | **tf** → RO-06 Feedback control, new Note after Note 118. block-diagram algebra |
| block diagrams | 1-1, 2-10, 3-23–3-26, 9-8, 9-17–9-23 | add | **tf** → RO-06 Feedback control, new Note after Note 118. block diagrams |
| block diagrams, control system | 1-6, 2-13, 2-21, 2-26, 9-1, 9-2, 9-18 | add | **tf** → RO-06 Feedback control, new Note after Note 118. block diagrams |
| block diagrams, Kalman decomposition | 8-16 | out-of-scope | Kalman decomposition: linear-systems structure theory (FBS §8.3) |
| block diagrams, observable canonical form | 8-5 | out-of-scope | observable canonical form: derivation device (FBS §8.1) |
| block diagrams, observer | 8-2, 8-9 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). observer block diagrams |
| block diagrams, observer-based control system | 8-14 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). observer block diagrams |
| block diagrams, PID controllers | 11-2, 11-5, 11-22 | taught | Note 117 (PID block diagram) |
| block diagrams, reachable canonical form | 7-7 | out-of-scope | reachable canonical form: derivation device for pole placement (FBS §7.1) |
| block diagrams, two degree-of-freedom control | 8-23, 12-2, 13-16 | taught | Note 119 (feedforward plus feedback = two degrees of freedom) |
| block diagrams, Youla parameterization | 13-14 | out-of-scope | Youla parameterization: advanced robust-control synthesis |
| Bode, H. | 1-8, 9-1, 10-27, 13-28, 14-30 | index-noise | person |
| Bode plots | 9-29–9-37, 10-18 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. Bode plots |
| Bode plots, asymptotic approximation | 9-32 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. Bode plots |
| Bode plots, low-, band-, high-pass filters | 9-35 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. Bode plots |
| Bode plots, of rational function | 9-29 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. Bode plots |
| Bode plots, sketching | 9-32 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. Bode plots |
| Bode’s ideal loop transfer function | 13-13, 13-30 | out-of-scope | Bode's ideal loop transfer function: advanced design result |
| Bode’s integral formula | 14-5–14-10, 14-31 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. Bode's integral formula (waterbed), named |
| Bode’s phase area formula | 12-16 | out-of-scope | Bode's gain-phase relations: frequency-domain theory (FBS §10.4) |
| Bode’s relations | 10-18, 10-19, 12-14 | out-of-scope | Bode's gain-phase relations: frequency-domain theory (FBS §10.4) |
| BOXES | 15-33 | out-of-scope | history (BOXES, an early learning controller) |
| Brahe, T. | 3-2 | index-noise | person |
| breakpoint | 9-32, 10-8 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. breakpoint (corner) frequency |
| Bristol’s RGA | 15-25 | out-of-scope | relative gain array: process-control MIMO design |
| Brockett, R. W. | xii, 6-34 | index-noise | person |
| Bryson, A. E. | 7-36 | index-noise | person |
| bump test | 11-11, 11-13 | add | **pidtune** → RO-06, extend Note 117 (PD and PID control) or a new Note after Note 119. bump test |
| bumpless transfer | 13-27 | add | **pidtune** → RO-06, extend Note 117 (PD and PID control) or a new Note after Note 119. bumpless transfer |
| Bush, V. | 11-24 | index-noise | person |
| calibration, versus feedback | 1-8, 7-14, 7-24, 7-26 | out-of-scope | motivating comparison (calibration vs feedback), FBS ch.1 |
| cancellation |  (see pole/zero cancellations) | index-noise | cross-reference |
| Cannon, R. H. | 3-44, 6-1 | index-noise | person |
| capacitor, transfer function for | 9-9 | out-of-scope | electrical circuit example |
| car |  (see automotive control systems; cruise control; vehicle steering) | index-noise | cross-reference |
| carrying capacity, in population models | 4-26, 4-27 | out-of-scope | population models, biology |
| cart-pendulum system | 3-12, 3-13, 7-5, 7-6, 14-28–14-30, 15-33 (see also balance systems) | taught | Note 296 (inverted pendulum); RL cart-pole benchmark |
| cascade control | 15-18–15-19 | taught | Note 119 (cascaded control loops) |
| causal reasoning | 1-1, 4-7 | out-of-scope | philosophy of modelling (FBS ch.1) |
| Cayley-Hamilton theorem | 7-33, 8-3 | out-of-scope | Cayley-Hamilton theorem: proof tool for the rank tests |
| center (equilibrium point) | 5-10 | add | **eqtypes** → MA 06-calculus, extend the planned Stability of dynamical systems Note (plan §4). center |
| centrifugal governor | 1-2, 1-3, 1-14 | out-of-scope | history (centrifugal governor) |
| certainty equivalence principle | 15-30 | out-of-scope | adaptive-control theory (FBS §15.4 overview) |
| chain of integrators (normal form) | 3-44, 7-7 | add | **dblint** → MA 06-calculus, worked example in the planned State-space models Note (plan §4). chain of integrators |
| characteristic polynomial | 2-6, 2-9, 5-12, 7-33, 9-8, 9-24 | taught | MA-056 (characteristic polynomial) |
| characteristic polynomial, for closed loop transfer function | 10-2 | add | **tf** → RO-06 Feedback control, new Note after Note 118. closed-loop characteristic polynomial |
| characteristic polynomial, observable canonical form | 8-5 | out-of-scope | observable canonical form (derivation device) |
| characteristic polynomial, output feedback controller | 8-12, 8-13 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). characteristic polynomial with output feedback |
| characteristic polynomial, reachable canonical form | 7-7, 7-9, 7-13, 7-34 | out-of-scope | reachable canonical form (derivation device) |
| chemical systems | 1-8, 11-1 (see also process control; compartment models) | out-of-scope | application domain (chemical/process) |
| chordal metric | 13-6 | out-of-scope | chordal metric: advanced robust-control theory (Vinnicombe) |
| circle criterion | 10-24–10-25, 10-30, 11-17, 11-18, 13-13, 14-27 | out-of-scope | circle criterion: nonlinear feedback analysis beyond course level |
| circuits |  (see biological circuits; electrical circuits) | index-noise | cross-reference |
| class of signals E |  (see exponential signals) | index-noise | cross-reference |
| classical control | xi, 13-28 | out-of-scope | history of control (FBS ch.1) |
| closed loop | 1-1, 1-2, 1-5, 6-33, 7-10, 7-17, 10-2, 10-24, 12-1 | taught | Note 117 (closed-loop feedback vs open loop); Note 9 (open-loop vs feedback plans) |
| closed loop, versus open loop | 1-1, 10-4, 12-1 | taught | Note 117 (closed-loop feedback vs open loop); Note 9 (open-loop vs feedback plans) |
| co-design | 15-1 | out-of-scope | systems-engineering process (co-design) |
| command signal | 1-4, 1-5, 2-1, 7-9, 8-23, 11-2 (see also reference signal; setpoint) | taught | Note 117 (reference / command signal) |
| communication systems | 15-41 | out-of-scope | application domain (communication) |
| compartment models | 4-21–4-26, 5-13–5-14, 6-21, 6-37, 7-20, 8-3–8-4, 8-8–8-9 | out-of-scope | compartment models: pharmacokinetics, different field |
| compensator |  (see control law) | index-noise | cross-reference |
| complementary filtering | 15-23, 15-24 | taught | Note 86 (complementary filter) |
| complementary sensitivity function | 12-3, 13-11, 13-14, 13-17, 13-22, 13-29, 14-7, 14-25, 14-32 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. complementary sensitivity function |
| complexity, of control systems | 1-8, 1-18, 11-7 | out-of-scope | systems-engineering discussion |
| computed torque | 6-34 | taught | Note 284 (computed torque) |
| computer implementation, of controllers | 3-17, 8-30–8-31, 11-22–11-23 | add | **sampling** → RO-08, extend Note 136 (Delays and control rate), or RO-06 after the PID Notes. computer implementation of controllers |
| computer science, relationship to control | 1-6 | out-of-scope | application domain (computing) |
| computer systems, control of | 1-10–1-11, 1-22, 1-28, 3-16, 3-37, 3-38, 4-11–4-17, 6-28 (see also queuing systems) | out-of-scope | application domain (computing) |
| conditional stability | 10-14 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. conditional stability |
| configuration variables | 3-13 | taught | Note 72 (configuration variables) |
| congestion control | 1-10, 4-14–4-17, 5-10–5-11, 10-8–10-9, 10-28 (see also queuing systems) | out-of-scope | congestion control: networking, different field |
| congestion control, router dynamics | 4-29 | out-of-scope | congestion control: networking, different field |
| consensus | 3-38 | add | **consensus** → RO-23 Planning in depth, new Note before Note 271 (Planning with time and many robots). consensus (FBS §3.4 example) |
| contracts (specifications) | 15-14 | out-of-scope | formal-methods design contracts (FBS ch.15) |
| control |  | taught | Note 117 (feedback control) |
| control, definition of | 1-5–1-6 | out-of-scope | history of control (FBS ch.1) |
| control, early examples | 1-2, 1-7, 1-8, 1-14, 1-18, 1-27, 11-4 | out-of-scope | history of control (FBS ch.1) |
| control, fundamental limits | 13-27–13-28, 14-1–14-30, 14-32 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. fundamental limits (named) |
| control, history of | 1-28, 11-24 | out-of-scope | history of control (FBS ch.1) |
| control, modeling for | 1-6, 3-5–3-6, 3-44, 13-1 | taught | plan §4 new maths: State-space models; Note 139 (models for control) |
| control, successes of | 1-8, 1-27 | out-of-scope | history of control (FBS ch.1) |
| control, system | 1-5, 7-9, 8-14, 8-23, 8-30, 9-1, 12-2, 12-6, 13-16 | taught | Note 117 (control system) |
| control, using estimated state | 8-11–8-14, 13-23 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). control using the estimated state |
| control error | 1-18, 9-18, 11-2 | taught | Note 117 (control error) |
| control law | 1-5, 1-18, 1-19, 6-33, 7-10, 7-13, 9-18 | taught | Note 117 (control law) |
| control Lyapunov function | 5-33 | out-of-scope | control Lyapunov functions: named only (FBS §5.5); Note 199 uses Lyapunov certificates |
| control matrix | 3-10, 3-14 | taught | plan §4 new maths: State-space models (B matrix) |
| control protocol | 15-12 | out-of-scope | networking protocol design (FBS ch.15) |
| control signal | 1-4, 1-19, 2-2, 2-18, 2-25, 3-6, 3-10, 3-27, 6-27, 7-1, 7-22, 8-30, 9-2, 11-2, 11-4, 11-15, 11-18–11-20, 11-22, 12-2, 12-5–12-8, 12-11, 12-22, 13-24, 14-26, 14-28, 15-19–15-21, 15-32 | taught | plan §4 new maths: State-space models (input u) |
| controllability | 7-33 (see also reachability) | taught | Note 204 (controllability / reachability) |
| controlled differential equation | 3-3, 3-11, 9-8 | taught | plan §4 new maths: State-space models (x' = f(x, u)) |
| convolution equation | 6-15–6-17, 6-19, 6-20, 6-22, 6-35, 7-4, 9-16 | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). convolution equation |
| convolution equation, discrete-time | 6-36 | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). convolution equation |
| convolutional neural network | 15-37 | taught | DL-040 (CNNs) |
| convolutional neural network (CNN) | 15-35 | taught | DL-040 (CNNs) |
| convolutional neural networks | 15-35 | taught | DL-040 (CNNs) |
| coordinate transformations | 5-12, 6-17–6-19, 7-8, 8-32, 9-12 | taught | MA-056 (change of basis); Note 65 (frames) |
| coordinate transformations, to Jordan form | 6-9 | add | **eigmult** → MA 05-linear-algebra, extend MA-056 (eigenvectors and eigenvalues). Jordan form |
| coordinate transformations, to observable canonical form | 8-6 | out-of-scope | canonical forms: derivation devices |
| coordinate transformations, to reachable canonical form | 7-8, 7-9 | out-of-scope | canonical forms: derivation devices |
| Coriolis forces | 3-12, 6-34 | taught | Note 281 (manipulator equation: Coriolis terms) |
| corner frequency | 9-32 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. corner frequency |
| correct-by-construction | 15-16 | out-of-scope | formal-methods design (FBS ch.15) |
| cost function | 7-28 | taught | Note 205 (quadratic cost) |
| coupled spring-mass system | 6-12, 6-14–6-15, 6-18–6-19 | out-of-scope | worked mechanical example (coupled spring-mass) |
| covariance matrix | 8-17, 8-18 | taught | Note 80 (covariance matrix in the Kalman filter); MA-009 |
| critical gain | 11-12, 11-14 | add | **pidtune** → RO-06, extend Note 117 (PD and PID control) or a new Note after Note 119. critical gain and period |
| critical period | 11-12, 11-14 | add | **pidtune** → RO-06, extend Note 117 (PD and PID control) or a new Note after Note 119. critical gain and period |
| critical point | 10-3, 10-6, 10-7, 10-15, 10-16, 10-26, 10-27, 11-12, 13-9, 13-10 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. critical point -1 |
| critically damped oscillator | 7-18 | taught | plan §4 new maths: Second-order linear systems (critically damped) |
| crossover frequency |  (see gain crossover frequency; phase crossover frequency) | index-noise | cross-reference |
| crossover frequency inequality |  (see gain crossover frequency inequality) | index-noise | cross-reference |
| cruise control | 1-14, 1-21, 4-1–4-5 | taught | Note 252 (cruise control) |
| cruise control, control design | 7-25–7-26, 11-9–11-10, 11-20 | taught | Note 252 (cruise control); FBS uses it as a running example |
| cruise control, electric car | 15-27–15-29 | taught | Note 252 (cruise control); FBS uses it as a running example |
| cruise control, feedback linearization | 6-33 | taught | Note 252 (cruise control); FBS uses it as a running example |
| cruise control, integrator windup | 11-15–11-17 | taught | Note 252 (cruise control); FBS uses it as a running example |
| cruise control, linearization | 6-29, 6-31 | taught | Note 252 (cruise control); FBS uses it as a running example |
| cruise control, pole/zero cancellation | 9-27–9-28 | taught | Note 252 (cruise control); FBS uses it as a running example |
| cruise control, robustness | 1-14, 13-2–13-3, 13-11–13-12 | taught | Note 252 (cruise control); FBS uses it as a running example |
| Curtiss seaplane | 1-16 | out-of-scope | history of control (FBS ch.1) |
| cybernetics | 1-9 (see also robotics) | index-noise | history pointer (cybernetics) |
| cyberphysical system | 3-8 (see also hybrid system) | taught | Note 289 (hybrid systems) |
| D contour |  (see Nyquist contour) | index-noise | cross-reference |
| D/A converters |  (see digital-to-analog converters) | index-noise | cross-reference |
| damped frequency | 2-15, 7-18 | taught | Note 118 (damping ratio, natural and damped frequency); plan §4 Second-order linear systems |
| damping | 3-3, 3-12, 3-19, 5-2 | taught | Note 118 (damping ratio, natural and damped frequency); plan §4 Second-order linear systems |
| damping ratio | 2-15, 7-18, 7-19, 7-21, 11-9 | taught | Note 118 (damping ratio, natural and damped frequency); plan §4 Second-order linear systems |
| DARPA Grand Challenge | 1-27, 15-10 | out-of-scope | history; the Stanley controller from it is Note 123 |
| DC gain | 6-25 (see also zero frequency gain) | add | **ssresp** → RO-06, extend Note 118 (step response and second-order systems). DC gain |
| dead zone | 1-18, 1-19 | out-of-scope | on-off control detail (dead zone), FBS §1.5 motivating example |
| decision making, higher levels of | 1-9, 15-9 | taught | Note 126 (decision layers in the autonomy stack) |
| deep learning | 15-35 | taught | DL-002 (deep learning) |
| delay |  (see time delay) | index-noise | cross-reference |
| delay margin | 10-17 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. delay margin |
| delay-dominated dynamics | 11-14 | add | **pidtune** → RO-06, extend Note 117 (PD and PID control) or a new Note after Note 119. delay-dominated dynamics (FOTD classes) |
| delta function |  (see impulse function) | index-noise | cross-reference |
| derivative action | 1-20, 11-2, 11-5–11-7, 11-21 | taught | Note 117 (derivative action) |
| derivative action, filtering | 11-6, 11-19–11-20, 11-22, 11-23, 12-11 | add | **pidtune** → RO-06, extend Note 117 (PD and PID control) or a new Note after Note 119. derivative filtering, setpoint weighting, derivative time constant |
| derivative action, setpoint weighting | 11-20, 11-23 | add | **pidtune** → RO-06, extend Note 117 (PD and PID control) or a new Note after Note 119. derivative filtering, setpoint weighting, derivative time constant |
| derivative action, time constant | 11-3 | add | **pidtune** → RO-06, extend Note 117 (PD and PID control) or a new Note after Note 119. derivative filtering, setpoint weighting, derivative time constant |
| derivative gain | 11-2 | taught | Note 117 (derivative gain) |
| derivative time constant | 11-5 | add | **pidtune** → RO-06, extend Note 117 (PD and PID control) or a new Note after Note 119. derivative time constant |
| describing functions | 10-25–10-27, 10-31, 14-28, 14-29 | out-of-scope | describing functions: nonlinear analysis beyond course level |
| design of dynamics | 1-15–1-16, 5-16, 5-32–5-34, 6-1, 7-1, 7-11, 7-17 | out-of-scope | design discussion (FBS ch.1, ch.5) |
| design V | 15-2 | out-of-scope | systems-engineering V-process |
| diabetes |  (see insulin-glucose dynamics) | index-noise | cross-reference |
| diagonal systems | 5-12, 6-9 (see also block diagonal systems) | add | **modes** → MA 06-calculus, inside the planned Matrix exponential Note (plan §4). diagonal (modal) systems |
| diagonal systems, Kalman decomposition for | 8-15 | out-of-scope | Kalman decomposition (structure theory) |
| diagonal systems, transforming to | 5-12, 5-38, 6-8 | add | **modes** → MA 06-calculus, inside the planned Matrix exponential Note (plan §4). transforming to diagonal form |
| difference equations | 3-10, 3-14–3-17, 3-20, 3-44, 6-27, 8-30, 11-23 | taught | plan §4 new maths: State-space models (discrete-time models) |
| differential algebraic equations | 3-7 (see also algebraic loops) | out-of-scope | differential-algebraic equations: modelling-software detail |
| differential equations | 2-5, 3-2, 3-10–3-14, 5-1–5-4 | taught | plan §4 new maths: ODEs and vector fields |
| differential equations, controlled | 3-3, 6-3, 9-8 | taught | plan §4 new maths: State-space models |
| differential equations, equilibrium points | 5-6–5-7 | taught | plan §4 new maths: Stability of dynamical systems (equilibria) |
| differential equations, existence and uniqueness of solutions | 5-2–5-4 | out-of-scope | ODE existence and uniqueness: proof conditions |
| differential equations, first-order | 3-6, 11-7 | add | **ssresp** → RO-06, extend Note 118 (step response and second-order systems). first-order systems |
| differential equations, periodic solutions | 5-7, 5-17 | taught | Note 299 (limit cycles) |
| differential equations, qualitative analysis | 5-4–5-7 | taught | plan §4 new maths: ODEs and vector fields (following the arrows) |
| differential equations, second-order | 5-5, 7-17, 11-7 | taught | Note 118; plan §4 Second-order linear systems |
| differential equations, solutions | 2-8, 5-2, 6-3, 6-7, 6-15, 9-44 | taught | plan §4 new maths: ODEs and vector fields; Numerical integration |
| differential equations, stability |  (see stability) | index-noise | cross-reference |
| differential equations, transfer functions for | 9-11 | add | **tf** → RO-06 Feedback control, new Note after Note 118. transfer functions from ODEs |
| differential flatness | 8-25, 8-26, 15-11 | taught | Note 223 (differential flatness) |
| digital control systems |  (see computer implementation, controllers) | index-noise | cross-reference |
| digital-to-analog converters | 1-5, 1-6, 4-18, 8-30, 8-31, 11-22 | add | **sampling** → RO-08, extend Note 136 (Delays and control rate), or RO-06 after the PID Notes. digital-to-analog converters |
| dimension-free variables | 3-28, 3-44 | out-of-scope | modelling technique (non-dimensional variables) |
| direct connection | 3-26 | taught | plan §4 new maths: State-space models (D matrix / direct term) |
| direct term | 3-10, 3-14, 3-26, 6-17, 8-11, 9-22 | taught | plan §4 new maths: State-space models (D matrix / direct term) |
| discrete control | 3-37 | out-of-scope | discrete-event (logic) control models (FBS §3.4, ch.15) |
| discrete transition system | 15-12 | out-of-scope | discrete-event (logic) control models (FBS §3.4, ch.15) |
| discrete-time systems | 3-14, 3-44, 5-37, 6-27, 6-36, 11-22 | taught | plan §4 new maths: State-space models (discrete-time) |
| discrete-time systems, Kalman filter for | 8-17 | taught | Note 80 (discrete-time Kalman filter) |
| discrete-time systems, linear quadratic control for | 7-30 | taught | Note 205 (discrete-time LQR) |
| distributed control system (DCS) | 1-25, 11-2, 15-9, 15-39–15-40 | out-of-scope | industrial process-control systems (DCS) |
| disturbance attenuation | 1-5, 2-4–2-5, 2-12–2-16, 7-10, 12-9–12-10, 13-16 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. disturbance attenuation |
| disturbance attenuation, design of controllers for | 12-14, 12-19, 12-33, 13-23, 14-6 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. disturbance attenuation |
| disturbance attenuation, in biological systems | 9-37, 11-6 | out-of-scope | application example from biology |
| disturbance attenuation, integral gain as a measure of | 11-5, 13-16 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. disturbance attenuation and the sensitivity function |
| disturbance attenuation, relationship to sensitivity function | 12-9, 12-32, 13-16, 14-6 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. disturbance attenuation and the sensitivity function |
| disturbance modeling | 8-19, 8-27 | taught | Note 208 (disturbance models, offset-free MPC) |
| disturbance weighting | 13-26 (see H ∞ control) | out-of-scope | H-infinity disturbance weighting: advanced robust control |
| disturbances | 1-5, 3-3, 3-6, 9-18, 9-27, 12-2, 12-5 | taught | Note 208 (disturbances) |
| disturbances, generalized | 13-24 | out-of-scope | generalized disturbances (H-infinity setting), advanced |
| disturbances, random | 8-17 | taught | Note 80 (random process disturbances in the Kalman filter) |
| Dodson, B. | 1-1 | index-noise | person |
| dominant eigenvalues (poles) | 7-21, 11-9, 11-10 | add | **tf** → RO-06 Feedback control, new Note after Note 118. dominant poles |
| double integrator | 6-7, 7-2, 9-11, 9-36 | add | **dblint** → MA 06-calculus, worked example in the planned State-space models Note (plan §4). double integrator |
| Doyle, J. C. | xii, 12-30, 13-28 | index-noise | person |
| drag | 4-3 | taught | Note 252 (aerodynamic drag) |
| drug administration | 4-21–4-26, 4-30, 6-21, 7-20–7-21 (see also compartment models) | out-of-scope | application examples (drug dosing, boiler) |
| drum boiler | 3-34 | out-of-scope | application examples (drug dosing, boiler) |
| dual control | 15-32 | out-of-scope | dual control: adaptive-control theory (FBS §15.4 overview) |
| duality | 8-7, 8-11 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). duality of reachability and observability |
| Dubins car model | 3-31, 3-46 | taught | Note 112 (Dubins car) |
| dynamic compensator | 7-25, 8-13 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). dynamic compensator (observer-based controller) |
| dynamic inversion | 6-34 | taught | Note 124 (feedback linearisation / dynamic inversion) |
| dynamic voltage frequency scaling | 11-25 | out-of-scope | application example from computing systems |
| dynamical systems | 1-1, 3-1, 5-1, 5-4, 5-34 | taught | plan §4 new maths: ODEs and vector fields; State-space models |
| dynamical systems, linear | 5-11, 6-1 | taught | plan §4 new maths: State-space models (linear) |
| dynamical systems, observer as a | 8-1 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). observer as a dynamical system |
| dynamical systems, state of | 7-9 | taught | plan §4 new maths: State-space models (state) |
| dynamical systems, stochastic | 8-17 (see also differential equations) | taught | Note 80 (stochastic linear system) |
| dynamics matrix | 3-10, 3-14, 5-11, 6-13 | taught | plan §4 new maths: State-space models (A matrix) |
| Dyson, F. | 3-1 | index-noise | person |
| E |  (see exponential signals) | index-noise | cross-reference |
| e-commerce | 1-10 | out-of-scope | application domains (economics, ecosystems, computing) |
| e-mail server, control of | 3-16, 6-28 | out-of-scope | application domains (economics, ecosystems, computing) |
| economic systems | 1-4, 1-11, 3-45 | out-of-scope | application domains (economics, ecosystems, computing) |
| ecosystems | 1-12, 4-26, 7-15 (see also predatorprey system) | out-of-scope | application domains (economics, ecosystems, computing) |
| eigenvalue assignment | 7-11, 7-13–7-17, 7-22, 11-8, 14-20–14-25 | taught | Note 204 (pole placement = eigenvalue assignment) |
| eigenvalue assignment, by output feedback | 8-13 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). eigenvalue assignment by output feedback |
| eigenvalue assignment, for observer design | 8-7 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). observer design by eigenvalue assignment |
| eigenvalues | 5-11, 5-22, 5-31, 6-12, 9-5 | taught | MA-056; plan §4 Stability of dynamical systems |
| eigenvalues, and Jordan form | 6-9–6-11, 6-36 | add | **eigmult** → MA 05-linear-algebra, extend MA-056 (eigenvectors and eigenvalues). Jordan form |
| eigenvalues, distinct | 6-8, 6-14, 8-15 | add | **eigmult** → MA 05-linear-algebra, extend MA-056 (eigenvectors and eigenvalues). distinct eigenvalues (diagonalizable case) |
| eigenvalues, dominant | 7-21 | add | **tf** → RO-06 Feedback control, new Note after Note 118. dominant eigenvalues (poles) |
| eigenvalues, effect on dynamic behavior | 7-17–7-19, 7-21, 9-4, 9-5 | add | **modes** → MA 06-calculus, inside the planned Matrix exponential Note (plan §4). effect of eigenvalues on behaviour |
| eigenvalues, for discrete-time systems | 6-37 | add | **dtstab** → MA 06-calculus, extend the planned Stability of dynamical systems Note (plan §4). eigenvalues for discrete-time systems |
| eigenvalues, invariance under coordinate transformation | 5-13 | taught | MA-056 (similar matrices, P^-1 A P) |
| eigenvalues, relationship to modes | 6-12–6-15 | add | **modes** → MA 06-calculus, inside the planned Matrix exponential Note (plan §4). eigenvalues and modes |
| eigenvalues, relationship to poles | 9-24 | add | **tf** → RO-06 Feedback control, new Note after Note 118. eigenvalues are the poles |
| eigenvalues, relationship to stability | 5-26, 6-10, 6-11 | taught | plan §4 new maths: Stability of dynamical systems (eigenvalue test) |
| eigenvalues, repeated | 6-9 | add | **eigmult** → MA 05-linear-algebra, extend MA-056 (eigenvectors and eigenvalues). repeated eigenvalues |
| eigenvectors | 5-13, 6-12, 6-13 | taught | MA-056 (eigenvectors) |
| eigenvectors, relationship to mode shape | 6-13 | add | **modes** → MA 06-calculus, inside the planned Matrix exponential Note (plan §4). mode shapes |
| electric car | 15-27 | out-of-scope | application example (electric car) |
| electric power |  (see power systems (electric)) | index-noise | cross-reference |
| electrical circuits | 3-7, 3-24, 4-10, 6-1, 9-9 (see also operational amplifier) | out-of-scope | electrical engineering, different field |
| electrical engineering | 1-7–1-8, 3-4–3-5, 6-25, 10-13 | out-of-scope | electrical engineering, different field |
| elephant, modeling of an | 3-1 | out-of-scope | modelling anecdote (FBS ch.3 quote) |
| Elowitz, M. B. | 3-41 | index-noise | person |
| encirclement | 10-6 (see also Nyquist criterion) | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. encirclement |
| environmental science | 1-3, 1-8 | out-of-scope | application domain / modelling-software paradigm |
| equation-based modeling | 3-7 | out-of-scope | application domain / modelling-software paradigm |
| equilibrium points | 3-39, 4-27, 5-6, 5-12, 6-2, 6-30, 7-2 | taught | plan §4 new maths: Stability of dynamical systems (equilibria) |
| equilibrium points, bifurcations of | 5-30 | out-of-scope | bifurcation theory, beyond course level |
| equilibrium points, discrete time | 3-39, 3-44 | taught | plan §4 new maths: State-space models (discrete-time equilibria) |
| equilibrium points, for closed loop system | 7-11, 7-25 | taught | Note 204 (closed-loop equilibrium with state feedback) |
| equilibrium points, for planar systems | 5-10 | add | **eqtypes** → MA 06-calculus, extend the planned Stability of dynamical systems Note (plan §4). equilibria of planar systems |
| equilibrium points, region of attraction | 5-28–5-30 | add | **eqtypes** → MA 06-calculus, extend the planned Stability of dynamical systems Note (plan §4). region of attraction |
| equilibrium points, stability | 5-8 | taught | plan §4 new maths: Stability of dynamical systems |
| equipment protection | 15-20 | out-of-scope | process-control logic (equipment protection) |
| error coefficients | 12-7 | add | **ssresp** → RO-06, extend Note 118 (step response and second-order systems). error coefficients |
| error feedback | 2-18, 11-2, 11-20, 12-4 | taught | Note 117 (feedback on the error) |
| estimators |  (see observers) | index-noise | cross-reference |
| Euler integration | 3-20, 3-21 | taught | plan §4 new maths: Numerical integration of ODEs (Euler) |
| exponential growth, in population models | 2-24, 4-26 | out-of-scope | population models, biology |
| exponential response | 9-4, 9-5 (see also transfer functions) | add | **tf** → RO-06 Feedback control, new Note after Note 118. exponential signals and response (FBS derives transfer functions from them) |
| exponential signals | 2-7, 9-2–9-12, 9-24, 9-29 | add | **tf** → RO-06 Feedback control, new Note after Note 118. exponential signals and response (FBS derives transfer functions from them) |
| extended Kalman filter | 8-30 | taught | Note 81 (EKF) |
| extremum seeking | 15-24 | out-of-scope | extremum seeking: adaptive optimisation, research-level |
| Falb, P. L. | 7-1 | index-noise | person |
| feedback | 1-1–1-3, 2-1 | taught | Note 117 (feedback) |
| feedback, as technology enabler | 1-3 | out-of-scope | motivating discussion (FBS ch.1-2) |
| feedback, drawbacks of | 1-3, 1-17–1-18, 2-4, 11-19, 13-9, 13-16 | out-of-scope | motivating discussion (FBS ch.1-2) |
| feedback, generation of discrete behavior | 2-27 | out-of-scope | logic from feedback (oscillators), FBS ch.2 example |
| feedback, in biological systems | 1-1, 1-3, 1-12, 1-28, 11-6 (see also biological circuits) | out-of-scope | application domain (biology) |
| feedback, in engineered systems |  (see control) | index-noise | cross-reference |
| feedback, in financial systems | 1-3 | out-of-scope | application domains (finance, nature) |
| feedback, in nature | 1-3, 1-11–1-13, 4-26 | out-of-scope | application domains (finance, nature) |
| feedback, positive |  (see positive feedback) | index-noise | cross-reference |
| feedback, properties | 1-2, 1-6, 1-13–1-18, 13-1 | out-of-scope | motivating discussion of feedback (FBS ch.1) |
| feedback, robustness through | 1-14 | out-of-scope | motivating discussion of feedback (FBS ch.1) |
| feedback, versus feedforward | 1-4, 11-4, 12-19 | taught | Note 119 (feedforward plus feedback) |
| feedback amplifier | 1-7 | out-of-scope | history (feedback amplifier) |
| feedback connection | 2-10, 2-11, 9-17, 9-18, 10-24, 10-25 | add | **tf** → RO-06 Feedback control, new Note after Note 118. feedback connection of transfer functions |
| feedback controller | 9-18, 12-2 | taught | Note 117 (feedback controller) |
| feedback linearization | 6-33–6-34 | taught | Note 124 (feedback linearisation) |
| feedback loop | 1-5, 10-1 | taught | Note 117 (feedback loop) |
| feedback uncertainty | 13-3, 13-4, 13-13 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. feedback uncertainty |
| feedforward | 1-4, 3-6, 8-24, 8-28, 9-18, 11-17, 12-2, 12-18 (see also two degree-of-freedom control) | taught | Note 119 (feedforward) |
| feedforward, design | 12-18–12-23 | taught | Note 206 (feedforward design for tracking); Note 119 |
| feedforward, difficulties with | 12-20–12-23 | out-of-scope | feedforward limitations (FBS §12.4 detail) |
| feedforward, sensitivity to process variations | 13-30 | out-of-scope | sensitivity of feedforward to model error (FBS exercise-level detail) |
| Fermi, E. | 3-1 | index-noise | person |
| filters |  | taught | Notes 78-82 (Bayes, Kalman and particle filters); for signal filters see freqresp |
| filters, active | 6-23 | out-of-scope | electronics (active filters) |
| filters, complementary filtering | 15-23 | taught | Note 86 (complementary filter) |
| filters, for measurement signals | 1-17, 8-31, 13-17 (see also band-pass filters; high-pass filters; low-pass filters) | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. filtering measurement signals |
| final value theorem | 9-16 | add | **laplace** → MA 06-calculus, new Note after the planned ODEs and State-space models Notes (plan §4). final value theorem |
| financial systems |  (see economic systems) | index-noise | cross-reference |
| finite escape time | 5-3 | out-of-scope | finite escape time: ODE theory |
| finite state machine | 1-21, 3-8, 3-17–3-19, 4-5, 4-12 | taught | Note 130 (state machines) |
| first-order and time-delay (FOTD) model | 11-12–11-14 | add | **pidtune** → RO-06, extend Note 117 (PD and PID control) or a new Note after Note 119. FOTD model |
| first-order systems | 6-3, 6-36, 9-11, 9-30, 9-31 | add | **ssresp** → RO-06, extend Note 118 (step response and second-order systems). first-order systems |
| fisheries management | 4-31 | out-of-scope | application example (fisheries) |
| FitzHugh-Nagumo equations | 3-43, 3-47, 3-48 (see also Hodgkin-Huxley equations) | out-of-scope | neuroscience models, different field |
| flatness |  (see differential flatness) | index-noise | cross-reference |
| flight control | 1-8, 1-15, 3-31, 6-34 | taught | Note 226 (aerial vehicles); RO-17 |
| flight control, X-29 aircraft | 14-7 (see also vectored thrust aircraft) | out-of-scope | application example (X-29 aircraft) |
| flow, of a vector field | 3-3, 5-5 | taught | plan §4 new maths: ODEs and vector fields (flow) |
| flow in a tank | 5-35 | out-of-scope | worked example (tank flow) |
| flow model (queuing systems) | 3-36, 10-28 | out-of-scope | queuing systems, different field |
| flyball governor |  (see centrifugal governor) | index-noise | cross-reference |
| flying home mode | 15-17 | out-of-scope | application example (aircraft modes) |
| force feedback | 1-8 | taught | Note 286 (force control) |
| forced response | 6-3, 9-3 | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). forced response |
| Forrester, J. W. | 1-12 | index-noise | person |
| Fourier, J. B. J. | 3-44, 9-40 | index-noise | person (FBS indexes no Fourier transform entry) |
| fractional transfer functions | 13-28 | out-of-scope | fractional transfer functions: advanced |
| frequency domain | 9-1–9-3, 10-1, 10-22, 12-1 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. frequency domain |
| frequency response | 2-8, 2-9, 3-5, 3-22, 3-23, 6-21–6-27, 9-1, 9-2, 10-27 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. frequency response and Bode plot |
| frequency response, relationship to Bode plot | 9-29 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. frequency response and Bode plot |
| frequency response, relationship to Nyquist plot | 10-5, 10-7 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. frequency response and the Nyquist plot |
| frequency response, relationship to step response | 10-21, 12-8, 12-9, 12-12, 12-32 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. frequency response vs step response; second-order case |
| frequency response, second-order systems | 7-19, 9-35 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. frequency response vs step response; second-order case |
| frequency response, system identification using | 9-38 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. system identification from a frequency response |
| frequency response analyzer | 9-40 | out-of-scope | lab instrument (frequency response analyzer) |
| friction | 3-12, 3-13, 3-20, 4-3, 14-28–14-30 | taught | Note 288 (friction); Note 283 (motor friction) |
| fully actuated systems | 9-24 | out-of-scope | FBS-specific system class (fully actuated) |
| fundamental limits |  (see control: fundamental limits) | index-noise | cross-reference |
| gain | 1-19, 2-2, 2-8, 3-22, 3-27, 4-8, 6-23, 6-24, 7-21, 9-3, 9-6, 9-23, 9-29, 10-15, 10-22–10-25, 13-1 | taught | Note 117 (controller gain) |
| gain, feedback | 7-25 | taught | Note 204 (feedback gain) |
| gain, generalized | 10-22 | out-of-scope | system gains and norms (FBS §10.6), beyond course level |
| gain, H ∞ | 10-23 | out-of-scope | system gains and norms (FBS §10.6), beyond course level |
| gain, observer |  (see observer gain) | index-noise | cross-reference |
| gain, state feedback | 7-11, 7-15, 7-25, 7-33 | taught | Note 204 (state-feedback gain) |
| gain, zero frequency |  (see zero frequency gain; see also integral gain) | index-noise | cross-reference |
| gain crossover frequency | 10-15, 10-16, 12-6, 12-14, 12-34, 14-11, 14-25 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. gain crossover frequency |
| gain crossover frequency inequality | 14-10–14-15 | out-of-scope | fundamental-limits inequality, advanced (FBS §14.3) |
| gain curve (Bode plot) | 9-29–9-33, 10-18, 12-13 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. Bode gain curve |
| gain margin | 10-15–10-17 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. gain margin |
| gain margin, from Bode plot | 10-16 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. gain margin |
| gain margin, reasonable values | 10-17 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. gain margin |
| gain scheduling | 8-27–8-29, 13-27 | taught | Note 255 (gain scheduling) |
| gain-bandwidth product | 4-10, 9-7, 13-18 | out-of-scope | electronics (op-amp gain-bandwidth) |
| Gang of Four | 12-3, 12-31, 13-15 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. Gang of Four / Six |
| Gang of Six | 12-3 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. Gang of Four / Six |
| gene regulation | 1-12, 3-40, 6-38, 9-36 | out-of-scope | biology (gene regulation) |
| generalized impedance | 9-9 | out-of-scope | electrical impedance, different field |
| genetic switch | 3-47, 5-23–5-25 | out-of-scope | biology (genetic switch) |
| global behavior | 5-10, 5-29–5-32 | add | **eqtypes** → MA 06-calculus, extend the planned Stability of dynamical systems Note (plan §4). global behaviour / region of attraction |
| Glover, K. | 12-30, 13-28 | index-noise | person |
| glucose regulation |  (see insulin-glucose dynamics) | index-noise | cross-reference |
| Golomb, S. | 4-1 | index-noise | person |
| governor |  (see centrifugal governor) | index-noise | cross-reference |
| H ∞ control | 13-24–13-28, 13-30 | out-of-scope | H-infinity control: advanced robust-control synthesis |
| H ∞ control, disturbance weighting | 13-30 | out-of-scope | H-infinity control: advanced robust-control synthesis |
| Hall chart | 13-22 | out-of-scope | graphical design chart (Hall chart) |
| hardware-in-the-loop simulation (HIL) | 15-3 | out-of-scope | systems-engineering test practice (HIL) |
| Harrier AV-8B aircraft | 3-31, 3-32 | out-of-scope | application example (aircraft) |
| heat propagation | 9-11, 10-29 | out-of-scope | heat equation (PDE), different field |
| Heaviside, O. | 6-35 | index-noise | person |
| Heaviside step function | 6-20, 6-35 | taught | Note 118 (step input) |
| Hellerstein, J. L. | 1-28, 4-17 | index-noise | person |
| Hewlett’s oscillator | 2-24 | out-of-scope | history (electronic oscillator) |
| Hewlett-Packard | 2-24 | index-noise | company |
| hidden technology | 15-37 | out-of-scope | essay topic (hidden technology) |
| high-frequency roll-off | 11-20, 12-11, 12-14, 13-17, 13-20, 14-28 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. high-frequency roll-off |
| high-pass filter | 9-35 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. high-pass filter |
| Hill function | 3-40 | out-of-scope | biology (Hill function) |
| Hoagland, M. B. | 1-1 | index-noise | person |
| Hodgkin-Huxley equations | 3-41–3-43, 3-48 (see also FitzHugh-Nagumo equations) | out-of-scope | neuroscience models, different field |
| homeostasis | 1-3, 3-40 | out-of-scope | biology (homeostasis) |
| homogeneous equation | 2-6, 9-23 | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). homogeneous equation / system (initial-condition response) |
| homogeneous system | 6-3, 6-6, 6-7 | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). homogeneous equation / system (initial-condition response) |
| Horowitz, I. M. | 2-28, 8-32, 12-30, 13-22, 13-28, 14-30 | index-noise | person |
| human-machine interface | 1-21, 4-1, 4-5 | out-of-scope | human-machine interface, FBS ch.1 discussion |
| hybrid system | 1-28, 3-8, 3-19, 3-43, 15-12 | taught | Note 289 (hybrid systems) |
| hyper state | 15-33 | out-of-scope | adaptive-control theory (hyper state) |
| hysteresis | 1-18, 1-19, 2-4, 2-26, 2-27, 10-26, 10-27 | out-of-scope | on-off control detail (hysteresis), FBS ch.1 |
| I-PD controller | 11-20 | add | **pidtune** → RO-06, extend Note 117 (PD and PID control) or a new Note after Note 119. I-PD controller (setpoint weighting) |
| identification |  (see system identification) | index-noise | cross-reference |
| impedance | 9-8, 9-9, 11-21 | out-of-scope | electrical impedance (FBS §9.2 circuits); impedance control of robots is Note 287 |
| implementation, controllers |  (see analog implementation; computer implementation) | index-noise | cross-reference |
| impulse function | 6-16, 7-4 | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). impulse function and impulse response |
| impulse response | 6-5, 6-16, 6-17, 6-35, 7-3, 9-16 | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). impulse function and impulse response |
| inductor, transfer function for | 9-9 | out-of-scope | electrical circuit example |
| inertia matrix | 3-12, 6-34 | taught | Note 220, Note 281 (inertia matrix) |
| inferential control |  (see internal model control) | index-noise | cross-reference |
| infinity norm | 10-23, 13-25 | out-of-scope | system norms, beyond course level |
| information systems | 1-10, 3-34–3-39 (see also congestion control; web server control) | out-of-scope | application domain (information systems) |
| initial condition | 5-2, 5-5, 5-8, 6-3, 6-7, 6-14, 8-17 | taught | plan §4 new maths: ODEs and vector fields (initial condition) |
| initial condition response | 6-3, 6-4, 6-6–6-9, 6-13, 6-14, 6-17, 9-3–9-5 | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). initial-condition response |
| initial value problem | 5-2 | taught | plan §4 new maths: ODEs and vector fields |
| initial value theorem | 9-16 | add | **laplace** → MA 06-calculus, new Note after the planned ODEs and State-space models Notes (plan §4). initial value theorem |
| inner loop control | 12-27, 12-29 | taught | Note 119 (inner loop) |
| input sensitivity function |  (see load sensitivity function) | index-noise | cross-reference |
| input signal |  (see control signal) | index-noise | cross-reference |
| input/output models | 1-5, 2-5, 3-4, 3-5, 6-3, 6-15–6-28, 9-1, 9-4, 10-22 (see also frequency response; steadystate response; step response) | add | **tf** → RO-06 Feedback control, new Note after Note 118. input/output models and transfer functions |
| input/output models, and transfer functions | 9-16 | add | **tf** → RO-06 Feedback control, new Note after Note 118. input/output models and transfer functions |
| input/output models, from experiments | 9-37 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. input/output models from experiments |
| input/output models, relationship to state space models | 3-6, 5-1, 6-16 | add | **tf** → RO-06 Feedback control, new Note after Note 118. input/output vs state-space models |
| input/output models, steady-state response | 6-19 | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). steady-state response |
| input/output models, transfer function for | 9-8 | add | **tf** → RO-06 Feedback control, new Note after Note 118. transfer function of an input/output model |
| input/output stability | 10-24 | out-of-scope | input/output stability (system norms), beyond course level |
| inputs | 3-3, 3-6 | taught | plan §4 new maths: State-space models (inputs) |
| insect flight control | 3-23–3-26 | out-of-scope | biology (insect flight) |
| instrumentation | 1-8–1-9, 4-8 | out-of-scope | application domain (instrumentation) |
| insulin-glucose dynamics | 1-2, 4-24–4-26, 4-30 | out-of-scope | application example from medicine |
| insulin-glucose dynamics, minimal model | 4-25 | out-of-scope | application example from medicine |
| integral action | 1-19, 1-20, 1-29, 2-17, 2-25, 7-24–7-27, 7-35, 8-27, 11-2, 11-4–11-5, 11-7 | taught | Note 119 (integral action) |
| integral action, by positive feedback | 2-25 | out-of-scope | implementation detail (integral action by positive feedback) |
| integral action, setpoint weighting | 11-20, 11-23 | add | **pidtune** → RO-06, extend Note 117 (PD and PID control) or a new Note after Note 119. setpoint weighting; integral time constant |
| integral action, time constant | 11-3 | add | **pidtune** → RO-06, extend Note 117 (PD and PID control) or a new Note after Note 119. setpoint weighting; integral time constant |
| integral gain | 1-19, 11-2, 11-5, 11-7 | taught | Note 117 (integral gain) |
| integrated error | 11-5 | taught | Note 117 (integral of the error) |
| integrator | 3-23, 3-24, 7-24–7-26, 8-5, 9-11, 9-30, 10-18 (see also double integrator) | taught | Note 119 (integrator) |
| integrator windup | 1-19, 8-31, 11-15–11-17 | taught | Note 119 (integrator windup) |
| integrator windup, conditional integration | 11-26 | taught | Note 119 (anti-windup by conditional integration) |
| intelligent machines |  (see robotics) | index-noise | cross-reference |
| interaction | 15-24 | out-of-scope | loop interaction in MIMO process control |
| internal model control | 15-21 | out-of-scope | internal model control: process-control design method |
| internal model principle | 8-13, 8-30, 15-42 | out-of-scope | internal model principle: theory result; its common case, integral action against constant disturbances, is Note 119 |
| internal stability | 12-5 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. internal stability |
| Internet | 1-10, 4-12, 4-14, 4-17 (see also congestion control) | out-of-scope | networking, different field |
| Internet of Things (IoT) | 15-41 | out-of-scope | networking, different field |
| Internet Protocol (IP) | 4-14 | out-of-scope | networking, different field |
| invariant set | 5-27, 5-30 | add | **lasalle** → MA 06-calculus, short section in the planned Stability of dynamical systems Note (plan §4). invariant set |
| inverse model | 6-33, 6-34, 12-19, 12-20 | taught | Note 124 (inverting the model = feedback linearisation); Note 119 feedforward |
| inverse model, approximate | 12-22 | out-of-scope | approximate inverses for feedforward (FBS §12.4 detail) |
| inverse response | 3-34, 10-21, 12-21 | add | **tf** → RO-06 Feedback control, new Note after Note 118. inverse response (right-half-plane zero) |
| inverted pendulum | 3-14, 4-6, 5-6–5-7, 5-14–5-15, 5-27–5-30, 5-36, 5-37, 10-13, 14-7 (see also balance systems) | taught | Note 296 (inverted pendulum) |
| Jacobian linearization | 6-29–6-33 | taught | plan §5 recap Taylor linearisation (MA-064); Note 206 |
| Janert, P. K. | 1-28 | index-noise | person |
| Jordan block | 6-9 | add | **eigmult** → MA 05-linear-algebra, extend MA-056 (eigenvectors and eigenvalues). Jordan block / form |
| Jordan form | 6-9–6-12, 6-36, 7-21 | add | **eigmult** → MA 05-linear-algebra, extend MA-056 (eigenvectors and eigenvalues). Jordan block / form |
| Kalman, R. E. | 7-1, 7-33, 8-1, 8-16, 8-32 | index-noise | person |
| Kalman decomposition | 8-15–8-17, 9-40, 9-43 | out-of-scope | Kalman decomposition: structure theory |
| Kalman filter | 8-11, 8-17–8-21, 8-32, 13-23 | taught | Note 80 (Kalman filter) |
| Kalman filter, extended | 8-30 | taught | Note 81 (EKF) |
| Kalman’s inequality | 10-29 | out-of-scope | Kalman's inequality: LQR robustness theory, advanced |
| Kalman-Bucy filter | 8-20 | out-of-scope | continuous-time Kalman-Bucy filter; the plan teaches the discrete filter (Note 80) |
| Kelly, F. P. | 4-17 | index-noise | person |
| Kepler, J. | 3-2 | index-noise | person |
| Keynesian economic model | 3-45, 6-37 | out-of-scope | economics model |
| Krasovski-Lasalle principle | 5-26–5-27 | add | **lasalle** → MA 06-calculus, short section in the planned Stability of dynamical systems Note (plan §4). Krasovskii-LaSalle principle |
| LabVIEW | 5-31, 6-35 | index-noise | software / industrial language |
| ladder diagrams, LD | 15-39 | index-noise | software / industrial language |
| lag |  (see phase lag) | index-noise | cross-reference |
| lag compensation | 12-15 | add | **loopshape** → RO-06 Feedback control, new Note after the sensitivity Note. lag compensation |
| lag-dominated dynamics | 11-13, 11-14 | add | **pidtune** → RO-06, extend Note 117 (PD and PID control) or a new Note after Note 119. lag-dominated dynamics (FOTD classes) |
| Laplace transforms | xi, 9-14–9-16 | add | **laplace** → MA 06-calculus, new Note after the planned ODEs and State-space models Notes (plan §4). Laplace transform |
| Laplacian matrix | 3-39 | add | **graphlap** → MA 05-linear-algebra (new Note after MA-056 eigenvectors), first used by the consensus Note in RO-23. Laplacian matrix (FBS §3.4 consensus) |
| Lasalle’s invariance principle |  (see Krasovski-Lasalle principle) | index-noise | cross-reference |
| lead |  (see phase lead) | index-noise | cross-reference |
| lead compensation | 12-15, 12-17, 12-28, 12-34 | add | **loopshape** → RO-06 Feedback control, new Note after the sensitivity Note. lead and lead-lag compensation |
| lead-lag compensation | 12-33 | add | **loopshape** → RO-06 Feedback control, new Note after the sensitivity Note. lead and lead-lag compensation |
| learning | 15-29 | taught | Note 1 (learning) |
| limit cycle | 4-28, 5-7, 5-17–5-18, 5-31, 10-25, 10-26 | taught | Note 299 (limit cycles) |
| linear quadratic control | 7-28–7-32, 8-18, 8-22–8-23, 8-32, 13-23–13-24 | taught | Note 205 (LQR) |
| linear quadratic control, proof of optimality | 7-36 | out-of-scope | proof of LQR optimality |
| linear quadratic control, using optimal estimator | 8-22 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). LQ control with an optimal estimator (LQG) |
| linear range | 1-19, 2-2–2-5 | out-of-scope | linear operating range of a nonlinear element (FBS ch.2) |
| linear systems | 2-5–2-9, 3-4, 3-10, 4-10, 5-11, 6-1–6-35, 8-15, 9-3, 9-8, 9-40, 10-23 | taught | plan §4 new maths: State-space models (linear systems) |
| linear temporal logic | 15-13 | out-of-scope | formal methods (temporal logic) |
| linear time-invariant systems | 2-6, 3-4, 3-5, 3-10, 6-4 | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). linear time-invariant systems |
| linearity | 6-3, 9-29 | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). linearity |
| linearization | 5-16, 5-26, 6-2, 6-28–6-34, 8-28, 13-2 | taught | plan §5 recap Taylor linearisation (MA-064); Notes 81, 206 |
| Lipschitz continuity | 5-4 | out-of-scope | Lipschitz continuity: ODE existence proof condition |
| load disturbances | 2-2, 2-4, 12-2, 13-16 (see also disturbances, disturbance attentuation) | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. load disturbances |
| load sensitivity function | 12-3 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. load sensitivity function |
| local behavior | 5-10, 5-16, 5-26, 5-29, 6-30 | taught | plan §4 new maths: Stability of dynamical systems (local asymptotic stability) |
| locally asymptotically stable | 5-10 | taught | plan §4 new maths: Stability of dynamical systems (local asymptotic stability) |
| logic, combining feedback with | 1-20–1-25, 1-27, 1-28, 3-6, 3-8, 15-11, 15-39, 15-40 (see also finite state machine; supervisory control) | out-of-scope | logic combined with feedback (FBS ch.1 survey) |
| logistic growth model | 4-26, 4-27 | out-of-scope | population models, biology |
| loop analysis | 10-1, 12-1 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. loop analysis |
| loop shaping | 10-4, 12-13–12-17, 12-30, 13-22 | add | **loopshape** → RO-06 Feedback control, new Note after the sensitivity Note. loop shaping |
| loop shaping, design rules | 12-14 (see also Bode’s loop transfer function) | add | **loopshape** → RO-06 Feedback control, new Note after the sensitivity Note. loop shaping |
| loop transfer function | 10-1–10-4, 10-16, 10-24, 12-1, 12-5, 12-13, 12-14, 12-30, 14-6 (see also Bode’s loop transfer function) | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. loop transfer function |
| Lotus Notes server |  (see e-mail server) | index-noise | cross-reference |
| low-order models | 11-7 | out-of-scope | model-order discussion (FBS §11.2) |
| low-pass filter | 9-35, 11-19 (see also highfrequency roll-off) | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. low-pass filter |
| LQ control |  (see linear quadratic control) | index-noise | cross-reference |
| LTI systems |  (see linear time-invariant systems) | index-noise | cross-reference |
| Lyapunov equation | 5-22, 5-36 | add | **lyapeq** → MA 06-calculus, extend the planned Stability of dynamical systems Note (plan §4). Lyapunov equation |
| Lyapunov functions | 5-19, 5-21–5-23, 5-29, 6-36 | taught | plan §4 new maths: Lyapunov functions; Note 199 |
| Lyapunov functions, design of controllers using | 5-27, 5-32 | taught | Note 124 (Kanayama controller proved stable with a Lyapunov function) |
| Lyapunov functions, existence of | 5-21 | out-of-scope | converse Lyapunov theorems: proof-level |
| Lyapunov stability analysis | 3-22, 5-18–5-28, 5-34 | taught | plan §4 new maths: Lyapunov functions / Stability of dynamical systems |
| Lyapunov stability analysis, discrete time | 5-37 | add | **dtstab** → MA 06-calculus, extend the planned Stability of dynamical systems Note (plan §4). discrete-time Lyapunov analysis |
| magnitude, of frequency response |  (see gain) | index-noise | cross-reference |
| manifold | 5-28 | out-of-scope | stable manifolds: nonlinear-dynamics theory |
| manual control | 11-18 | add | **pidtune** → RO-06, extend Note 117 (PD and PID control) or a new Note after Note 119. manual / automatic mode switching |
| margins |  (see stability margins) | index-noise | cross-reference |
| Markov parameters | 9-42 | out-of-scope | Markov parameters: realization theory |
| materials science | 1-8 | out-of-scope | application domain (materials science) |
| Mathematica | 3-20, 5-31, 6-35 | index-noise | software (Mathematica) |
| MATLAB | 2-11, 3-20, 5-31, 6-35, 6-37, 13-23, 15-25 | index-noise | software command (MATLAB) |
| MATLAB, acker | 7-15, 8-11 | index-noise | software command (MATLAB) |
| MATLAB, dlqe | 8-18 | index-noise | software command (MATLAB) |
| MATLAB, dlqr | 7-32 | index-noise | software command (MATLAB) |
| MATLAB, feedback | 2-11 | index-noise | software command (MATLAB) |
| MATLAB, gapmetric | 13-7 | index-noise | software command (MATLAB) |
| MATLAB, hinfsyn | 13-25 | index-noise | software command (MATLAB) |
| MATLAB, jordan | 6-10 | index-noise | software command (MATLAB) |
| MATLAB, kalman | 8-20 | index-noise | software command (MATLAB) |
| MATLAB, linmod | 6-31 | index-noise | software command (MATLAB) |
| MATLAB, lqr | 7-29 | index-noise | software command (MATLAB) |
| MATLAB, lsim | 2-12 | index-noise | software command (MATLAB) |
| MATLAB, parallel | 2-11 | index-noise | software command (MATLAB) |
| MATLAB, place | 7-15, 7-23, 8-11 | index-noise | software command (MATLAB) |
| MATLAB, series | 2-11 | index-noise | software command (MATLAB) |
| MATLAB, step | 2-12 | index-noise | software command (MATLAB) |
| MATLAB, trim | 6-31 | index-noise | software command (MATLAB) |
| matrix exponential | 6-6–6-15, 6-34, 6-35 | taught | plan §4 new maths: Matrix exponential and logarithm |
| matrix exponential, coordinate transformations | 6-18 | taught | plan §4 Matrix exponential; MA-056 (change of basis) |
| matrix exponential, Jordan form | 6-10 | add | **eigmult** → MA 05-linear-algebra, extend MA-056 (eigenvectors and eigenvalues). matrix exponential with Jordan form |
| matrix exponential, second-order systems | 6-35 | taught | plan §4 Matrix exponential; Second-order linear systems |
| maximum complementary sensitivity | 12-6, 13-11, 14-25 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. maximum complementary sensitivity |
| maximum modulus principle | 14-15 | out-of-scope | maximum modulus principle: complex-analysis proof tool |
| maximum selector | 1-23, 15-20 | out-of-scope | process-control selectors |
| maximum sensitivity | 12-6, 12-10, 13-9, 13-13, 14-25 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. maximum sensitivity |
| measured signals | 3-6, 3-10, 5-1, 8-1, 8-2, 8-14, 8-31, 12-2, 12-5, 13-24 | taught | plan §4 new maths: State-space models (outputs y = Cx) |
| measurement noise | 1-5, 1-17, 8-2, 8-3, 8-17, 8-19, 9-18, 11-19, 12-2, 12-14, 13-16, 14-28 | taught | Note 80, Note 83 (measurement noise) |
| measurement noise, response to | 12-10–12-12, 13-16–13-17 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. response to measurement noise |
| mechanical systems | 3-6, 3-12, 3-21, 3-30, 3-44, 6-34 | taught | plan §4 Newtonian and rigid-body mechanics; Note 281 |
| mechanics | 3-2–3-5, 5-34, 6-1 | taught | plan §4 Newtonian and rigid-body mechanics; Note 281 |
| median selectors | 15-20 | out-of-scope | process-control selectors |
| mid-range control | 15-19 | out-of-scope | process-control selectors |
| minimal model (insulin-glucose) | 4-25 (see also insulin-glucose dynamics) | out-of-scope | medical model |
| minimum phase | 10-19, 10-27, 14-10 | add | **tf** → RO-06 Feedback control, new Note after Note 118. minimum phase |
| minimum selector | 1-23, 15-20 | out-of-scope | process-control selectors |
| mixed integer solvers | 15-14 | out-of-scope | hybrid / formal-methods optimisation (mixed-integer) |
| mixed logical dynamical | 15-14 | out-of-scope | hybrid / formal-methods optimisation (mixed-integer) |
| modal form |  (see diagonal systems) | index-noise | cross-reference |
| model checking | 15-15 | out-of-scope | formal methods (model checking) |
| model predictive control | 4-26 | taught | Note 207 (MPC) |
| model reference | 12-2 | taught | Note 206 (tracking a reference model) |
| Modelica | 3-7, 3-26, 6-34, 9-23 | index-noise | software (Modelica) |
| modeling | 1-5, 3-1–3-10, 3-44, 4-1 | taught | plan §4 State-space models; Note 139 |
| modeling, control perspective | 3-5 | out-of-scope | modelling discussion (FBS §3.1) |
| modeling, discrete control | 3-37 | out-of-scope | modelling discussion (FBS §3.1) |
| modeling, discrete-time | 3-14–3-15, 6-27–6-28 | taught | plan §4 State-space models (discrete time) |
| modeling, frequency domain | 9-1–9-3 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. frequency-domain modelling |
| modeling, from experiments | 3-27–3-28 | taught | Note 139 (system identification) |
| modeling, model reduction | 1-6 | out-of-scope | model reduction, beyond course level |
| modeling, multidomain | 3-6 | out-of-scope | modelling-software paradigm |
| modeling, normalization and scaling | 3-28 | out-of-scope | modelling technique (scaling) |
| modeling, simplified models, use of | 3-6, 11-7, 13-2, 13-10, 13-12 | taught | Note 296 (simplified models) |
| modeling, software for | 3-7, 6-31, 6-34 | index-noise | software pointer |
| modeling, state space | 3-10–3-22 | taught | plan §4 State-space models |
| modeling, uncertainty |  (see uncertainty) | index-noise | cross-reference |
| modes | 6-12–6-14, 9-23 | add | **modes** → MA 06-calculus, inside the planned Matrix exponential Note (plan §4). modes and their relation to poles |
| modes, relationship to poles | 9-25 | add | **modes** → MA 06-calculus, inside the planned Matrix exponential Note (plan §4). modes and their relation to poles |
| modularity | 1-16–1-17, 15-8, 15-10, 15-39 | out-of-scope | systems-engineering discussion |
| motion control systems | 3-30–3-32, 8-32 | out-of-scope | application domain pointer |
| motors, electric | 3-46, 10-3, 14-26 | taught | Note 283 (motors) |
| multi-input, multi-output systems | 5-1, 10-23, 12-6, 12-14 (see also input/output models) | taught | plan §4 State-space models (vector inputs and outputs) |
| multiplicative uncertainty | 13-3, 13-4, 13-12, 13-13 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. multiplicative uncertainty |
| nanopositioner (AFM) | 10-17, 13-19 | out-of-scope | application example (AFM) |
| natural frequency | 2-15, 7-18, 11-9 | taught | Note 118 (natural frequency) |
| natural frequency, damped | 2-15, 7-18 | taught | Note 118 (natural frequency) |
| negative definite function | 5-19 | taught | plan §4 new maths: Lyapunov functions (sign-definite functions) |
| negative feedback | 1-2, 1-15, 2-2, 4-9, 7-10, 10-1, 11-6 | taught | Note 117 (negative feedback) |
| Nernst’s law | 3-43 | out-of-scope | neuroscience |
| networking | 1-10, 3-24, 4-17 (see also congestion control) | out-of-scope | application domain (networking) |
| neural systems | 1-9, 2-23, 3-25, 3-41–3-43, 11-6 | out-of-scope | application domain (neuroscience) |
| neutral stability | 5-8–5-10 | taught | plan §4 Stability of dynamical systems (marginal / neutral stability) |
| Newton, I. | 3-2 | index-noise | person |
| Nichols, N. B. | 6-34, 11-11, 12-30, 13-28 | index-noise | person |
| Nichols chart | 13-22, 13-23 | out-of-scope | graphical design chart (Nichols chart) |
| Nobel Prize | 1-9, 3-43, 4-17 | index-noise | prize |
| noise |  (see disturbances; measurement noise) | index-noise | cross-reference |
| noise attenuation | 9-37, 12-10–12-12 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. noise attenuation |
| noise cancellation | 5-33 | out-of-scope | worked example |
| noise sensitivity function | 12-3 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. noise sensitivity function |
| non-minimum phase | 10-20, 14-10, 14-12 (see also inverse response) | add | **tf** → RO-06 Feedback control, new Note after Note 118. non-minimum phase |
| nonlinear systems | 2-1–2-2, 2-22, 3-6, 5-1, 5-4, 5-7, 5-15, 5-18, 5-23, 5-29–5-34, 8-2, 8-24, 8-30, 10-23–10-25, 13-12, 14-26–14-30 | taught | plan §4 State-space models (nonlinear systems) |
| nonlinear systems, linear approximation | 5-26, 6-30, 13-2 | taught | plan §5 recap Taylor linearisation (MA-064) |
| nonlinear systems, system identification | 3-45 | taught | Note 139 (system identification) |
| nonunique solutions (ODEs) | 5-3 | out-of-scope | ODE uniqueness theory |
| normalized coordinates | 3-28–3-29, 3-45, 6-32 | out-of-scope | modelling technique (normalised coordinates) |
| norms | 10-22–10-23 | out-of-scope | system norms, beyond course level |
| Nyquist, H. | 1-8, 10-1, 10-27 | index-noise | person |
| Nyquist contour | 10-5, 14-8 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. Nyquist contour and criterion |
| Nyquist criterion | 10-4–10-13, 10-25, 11-12 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. Nyquist contour and criterion |
| Nyquist criterion, extension to nonlinear systems | 10-24–10-25 | out-of-scope | Nyquist for nonlinear systems (circle criterion), advanced |
| Nyquist criterion, for robust stability | 13-9 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. robust stability via Nyquist |
| Nyquist criterion, general | 10-10 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. general Nyquist criterion; Nyquist plot |
| Nyquist plot | 10-5–10-6, 10-15, 11-12, 12-9, 12-10, 13-23 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. general Nyquist criterion; Nyquist plot |
| observability | 8-1–8-2, 8-15, 8-32 | taught | Note 80 (observability, concept) |
| observability, rank condition | 8-3 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). observability rank test, observability matrix, unobservable systems |
| observability, tests for | 8-2–8-3 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). observability rank test, observability matrix, unobservable systems |
| observability, unobservable systems | 8-4, 8-15–8-17, 9-44 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). observability rank test, observability matrix, unobservable systems |
| observability matrix | 8-3, 8-5 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). observability rank test, observability matrix, unobservable systems |
| observable canonical form | 8-5, 8-32 | out-of-scope | observable canonical form (derivation device) |
| observer gain | 8-7, 8-9–8-11, 8-13, 8-18, 8-20 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). observer gain and observers |
| observers | 8-1, 8-6–8-9, 8-13, 8-20, 8-30 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). observer gain and observers |
| observers, block diagram | 8-2, 8-9 (see also Kalman filter) | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). observer gain and observers |
| ODEs |  (see differential equations) | index-noise | cross-reference |
| Ohm’s law | 3-42, 4-9, 9-9 | out-of-scope | electrical engineering |
| on-off control | 1-18, 1-19 | out-of-scope | on-off control: motivating example before proportional control (FBS §1.5) |
| open loop | 1-1, 1-2, 2-2, 4-8, 7-2, 9-20, 10-1, 11-15, 12-1, 12-9, 13-4 | taught | Note 9 (open-loop vs feedback plans) |
| operational amplifier | 2-24, 2-25, 4-8–4-11, 9-6–9-8, 10-28, 11-20, 13-13 | out-of-scope | electronics (operational amplifiers) |
| operational amplifier, circuits | 4-28, 6-23, 13-18–13-19 | out-of-scope | electronics (operational amplifiers) |
| operational amplifier, dynamical model | 4-10, 9-6 | out-of-scope | electronics (operational amplifiers) |
| operational amplifier, input/output characteristics | 4-9 | out-of-scope | electronics (operational amplifiers) |
| operational amplifier, oscillator using | 4-29, 5-37 | out-of-scope | electronics (operational amplifiers) |
| operational amplifier, static model | 4-8, 9-6 | out-of-scope | electronics (operational amplifiers) |
| optimal control | 7-28, 8-17, 8-20, 13-23 | taught | Note 205 (optimal control); Note 116 |
| order, of a model | 3-10, 3-11 | taught | plan §4 State-space models (model order) |
| ordinary differential equations |  (see differential equations) | index-noise | cross-reference |
| oscillator dynamics | 2-24–2-25, 4-29, 5-2, 5-3, 5-17–5-18, 5-37, 6-8, 7-18, 9-5, 9-11 | out-of-scope | oscillator examples (electronics, biology) |
| oscillator dynamics, normal form | 3-45 | out-of-scope | oscillator examples (electronics, biology) |
| oscillator dynamics, repressilator (biological circuit) | 3-41 (see also nanopositioner (AFM); springmass system) | out-of-scope | oscillator examples (electronics, biology) |
| outer loop control | 12-27–12-29 | taught | Note 119 (outer loop) |
| output feedback | 8-11, 8-13, 8-32 (see also control: using estimated state; loop shaping; PID control) | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). output feedback |
| output sensitivity function |  (see noise sensitivity function) | index-noise | cross-reference |
| outputs |  (see measured signals) | index-noise | cross-reference |
| overdamped oscillator | 7-18 | taught | plan §4 Second-order linear systems (overdamped) |
| overshoot | 2-12, 6-21, 7-10, 7-19, 12-6 | taught | Note 118 (overshoot) |
| overshoot, for second-order systems | 7-20 | taught | Note 118 (overshoot) |
| Padé approximation | 10-30, 14-5 | add | **tf** → RO-06 Feedback control, new Note after Note 118. Padé approximation of a delay |
| pairing problem (relative gain array) | 15-25, 15-26 | out-of-scope | process-control MIMO pairing |
| parallel connection | 2-10, 2-11, 9-17 | add | **tf** → RO-06 Feedback control, new Note after Note 118. parallel connection |
| parallel systems | 15-27–15-29 | out-of-scope | application example (parallel systems) |
| parametric stability diagram | 5-30–5-32 | out-of-scope | parameter stability diagrams (bifurcation analysis) |
| parametric uncertainty | 2-20, 3-9, 13-1–13-2 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. parametric uncertainty |
| partial differential equation |  (see heat propagation) | index-noise | cross-reference |
| particular solution | 2-6, 6-3, 6-22, 9-5 (see also forced response) | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). particular solution (forced response) |
| particular solution, transfer function | 2-7 | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). particular solution (forced response) |
| passive systems | 10-24, 10-30 | out-of-scope | passivity theory: beyond course level |
| passivity theorem | 10-24 | out-of-scope | passivity theory: beyond course level |
| patch clamp | 1-9 | out-of-scope | neuroscience lab method |
| PD control | 11-5, 12-15 | taught | Note 117 (PD control) |
| peak frequency | 6-25, 12-6, 12-7 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. peak frequency, peak value and their products |
| peak frequency-peak time product | 12-32 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. peak frequency, peak value and their products |
| peak value | 12-6, 12-7 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. peak frequency, peak value and their products |
| pendulum dynamics | 5-21 (see also inverted pendulum) | taught | Note 296 (pendulum models) |
| perfect adaptation | 11-6 | out-of-scope | biology (perfect adaptation) |
| performance limits | 13-27, 14-6, 14-10, 14-25 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. performance limits (named) |
| performance limits, due to right half-plane poles and zeros | 10-20 (see also control: fundamental limits) | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. performance limits (named) |
| performance specifications | 2-12, 4-12, 6-21, 7-10, 12-1, 12-6–12-12, 12-14, 12-33, 13-15 (see also overshoot; maximum sensitivity; resonant peak; rise time; settling time) | add | **ssresp** → RO-06, extend Note 118 (step response and second-order systems). performance specifications |
| performance specifications, test points | 12-12, 15-5 | out-of-scope | test points: lab practice |
| performance specifications, time domain versus frequency domain | 12-6 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. time vs frequency domain specifications |
| periodic solutions |  (see differential equations; limit cycles) | index-noise | cross-reference |
| persistence, of a web connection | 4-12, 4-13 | out-of-scope | networking example |
| persistent excitation | 15-32 | out-of-scope | adaptive-control theory (persistent excitation) |
| Petri net | 3-24 | out-of-scope | discrete-event modelling (Petri nets) |
| pharmacokinetics | 4-21–4-24 (see also drug administration) | index-noise | cross-reference |
| phase | 2-8, 3-22, 6-23, 6-24, 7-21, 9-3, 9-6, 9-29, 10-22–10-25 (see also minimum phase; non-minimum phase) | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. phase of a frequency response |
| phase area formula |  (see Bode’s phase area formula) | index-noise | cross-reference |
| phase crossover frequency | 10-15, 10-16 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. phase crossover frequency |
| phase curve (Bode plot) | 9-29–9-31, 9-33 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. Bode phase curve |
| phase curve (Bode plot), relationship to gain curve | 10-18, 12-14 | out-of-scope | gain-phase relation theory (Bode's relations) |
| phase lag | 6-23, 6-24, 9-36, 10-19, 10-20, 14-11, 14-13 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. phase lag and lead |
| phase lead | 6-23, 9-36, 12-15, 12-34 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. phase lag and lead |
| phase margin | 10-15, 10-16, 12-14, 12-34, 13-29, 14-11 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. phase margin |
| phase margin, for Bode’s ideal transfer function | 13-30 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. phase margin |
| phase margin, from Bode plot | 10-16 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. phase margin |
| phase margin, reasonable values | 10-17 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. phase margin |
| phase margin, relationship to stability margin | 13-26 | out-of-scope | advanced robust-control margin relation |
| phase portrait | 3-3, 5-4–5-5, 5-29 | taught | plan §4 new maths: ODEs and vector fields (phase portraits) |
| Philbrick, G. A. | 4-11 | index-noise | person |
| photoreceptors | 11-6 | out-of-scope | biology |
| physics, relationship to control | 1-5 | index-noise | discussion pointer |
| PI control | 1-14, 1-20, 2-14–2-16, 3-17, 4-1, 4-4, 11-5, 11-10, 12-15 | taught | Note 117 (PI control) |
| PI control, first-order system | 11-8, 14-21 | taught | Note 117 (PI on a first-order plant) |
| PID control | 1-19–1-20, 2-29, 9-11, 11-1–11-24 | taught | Note 117 (PID) |
| PID control, block diagram | 2-2, 11-2, 11-5, 11-17 | taught | Note 117 (PID) |
| PID control, computer implementation | 11-22 | add | **sampling** → RO-08, extend Note 136 (Delays and control rate), or RO-06 after the PID Notes. computer implementation of PID |
| PID control, ideal form | 11-2 | add | **pidtune** → RO-06, extend Note 117 (PD and PID control) or a new Note after Note 119. ideal form and implementation |
| PID control, implementation | 11-5, 11-19–11-23 | add | **pidtune** → RO-06, extend Note 117 (PD and PID control) or a new Note after Note 119. ideal form and implementation |
| PID control, in biological systems | 11-6 | out-of-scope | PID in biology / op-amp implementation, different fields |
| PID control, op amp implementation | 11-20–11-22 | out-of-scope | PID in biology / op-amp implementation, different fields |
| PID control, proportional action | 11-3 | taught | Note 117 (proportional action) |
| PID control, tuning | 11-11–11-15 (see also derivative action; integral action) | add | **pidtune** → RO-06, extend Note 117 (PD and PID control) or a new Note after Note 119. PID tuning |
| planar dynamical systems | 5-5, 5-10 (see also second-order systems) | add | **eqtypes** → MA 06-calculus, extend the planned Stability of dynamical systems Note (plan §4). planar systems |
| pole excess | 9-24, 12-20, 12-24 | add | **tf** → RO-06 Feedback control, new Note after Note 118. pole excess (relative degree) |
| pole placement | 7-11, 14-25 (see also eigenvalue assignment) | taught | Note 204 (pole placement) |
| pole zero diagram | 9-24 | add | **tf** → RO-06 Feedback control, new Note after Note 118. pole-zero diagram |
| pole/zero cancellations | 9-13, 9-26–9-28, 9-40, 9-44, 14-25, 15-28 | add | **tf** → RO-06 Feedback control, new Note after Note 118. pole/zero cancellations |
| pole/zero cancellations, unstable | 9-27, 12-5 | add | **tf** → RO-06 Feedback control, new Note after Note 118. pole/zero cancellations |
| pole/zero pair, right half-plane | 14-3, 14-13–14-14, 14-17, 14-18, 14-20, 14-31, 14-32 | out-of-scope | right-half-plane pole/zero pairs: fundamental-limits theory |
| poles | 2-8, 9-9, 9-23, 9-25, 14-4 | add | **tf** → RO-06 Feedback control, new Note after Note 118. poles |
| poles, dominant |  (see dominant eigenvalues (poles)) | index-noise | cross-reference |
| poles, fast stable | 14-21, 14-25 | out-of-scope | fundamental-limits detail |
| poles, pure imaginary | 10-5, 10-13 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. pure imaginary poles on the Nyquist contour |
| poles, relationship to eigenvalues | 9-24 | add | **tf** → RO-06 Feedback control, new Note after Note 118. poles are eigenvalues |
| poles, right half-plane (unstable) | 9-25, 9-34, 10-20, 14-3, 14-6, 14-10, 14-12–14-14, 14-17, 14-20, 14-21, 14-25, 14-31, 14-32 | add | **tf** → RO-06 Feedback control, new Note after Note 118. right-half-plane (unstable) poles |
| Popov-Belevitch-Hautus (PBH) test | 14-3 | out-of-scope | PBH test: structure theory |
| population dynamics | 4-26–4-27, 4-31 (see also predator-prey system) | out-of-scope | population dynamics, biology |
| positive definite function | 5-19, 5-22, 5-26 | taught | plan §4 new maths: Lyapunov functions (positive definite V) |
| positive definite matrix | 5-22, 7-28 | taught | MA-068 (positive definite matrix) |
| positive feedback | 1-2, 1-17, 2-4, 2-23–2-27, 11-4 | out-of-scope | positive feedback discussion (FBS ch.1-2) |
| power of a matrix | 6-6 | taught | MA-056 (A^k = P D^k P^-1) |
| power systems (electric) | 1-7, 3-47, 5-7, 5-36 | out-of-scope | electric power systems, different field |
| predator-prey system | 3-15–3-16, 4-26–4-27, 5-30–5-31, 7-15–7-16 | out-of-scope | predator-prey, biology |
| prediction, in controllers | 1-20, 8-30, 11-5 (see also derivative action) | taught | Note 117 (derivative action as prediction) |
| prediction time | 11-5 | taught | Note 117 (derivative action as prediction) |
| principle of the argument |  (see variation of the argument, principle of) | index-noise | cross-reference |
| process control | 1-8, 1-25, 3-24, 3-32, 15-9, 15-39–15-40 | out-of-scope | process control, different field |
| program synthesis | 15-16 | out-of-scope | formal methods (program synthesis) |
| programmable logic controller | 11-23 | out-of-scope | industrial automation hardware (PLC) |
| programmable logic controller (PLC) | 15-39, 15-40 | out-of-scope | industrial automation hardware (PLC) |
| proper transfer function | 9-24 | add | **tf** → RO-06 Feedback control, new Note after Note 118. proper transfer function |
| proportional band | 11-3 | out-of-scope | process-industry name for controller gain |
| proportional control | 1-19, 2-13, 2-14, 11-2–11-4 (see also PID control) | taught | Note 117 (proportional control) |
| proportional-derivative control |  (see PD control) | index-noise | cross-reference |
| proportional-integral control |  (see PI control) | index-noise | cross-reference |
| proportional-integral-derivative control |  (see PID control) | index-noise | cross-reference |
| protocol |  (see congestion control; consensus) | index-noise | cross-reference |
| pulse signal | 6-16, 6-17, 7-22 (see also impulse function) | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). pulse signal |
| pupil response | 2-29, 9-39, 11-6 | out-of-scope | biology (pupil response) |
| pure exponential response |  (see exponential response) | index-noise | cross-reference |
| Q-value | 3-46, 7-20, 9-32 | out-of-scope | quality factor Q = 1/(2 zeta): alternative damping parameter; damping ratio is Note 118 |
| quantitative feedback theory (QFT) | 13-22 | out-of-scope | quantitative feedback theory: advanced robust design |
| quantization | 14-28 | out-of-scope | quantization effects in feedback (FBS §14.5), advanced |
| quarter car model | 9-43 | out-of-scope | vehicle suspension example |
| queuing systems | 3-35–3-36, 3-47 | out-of-scope | queuing systems |
| ramp input | 12-8 | add | **ssresp** → RO-06, extend Note 118 (step response and second-order systems). ramp input |
| random process | 3-35, 8-17, 8-18 | out-of-scope | stochastic-process theory (FBS §8.4 gives a sketch) |
| reachability | 7-1–7-9, 7-33, 8-15, 14-2, 14-3 | taught | Note 204 (reachability = controllability, rank test) |
| reachability, rank condition | 7-4 | taught | Note 204 (reachability = controllability, rank test) |
| reachability, tests for | 7-3 | taught | Note 204 (reachability = controllability, rank test) |
| reachability, unreachable systems | 7-6, 7-33, 7-34, 8-15–8-17, 9-44 | out-of-scope | structure of unreachable systems (theory) |
| reachability, with integral action | 7-27 | taught | Note 119 (integral action in state feedback) |
| reachability matrix | 7-4, 7-8 | taught | plan §4 new maths: Controllability rank test (reachability matrix) |
| reachable canonical form | 3-11, 7-7–7-9, 7-13, 7-14, 7-34, 9-13 | out-of-scope | reachable canonical form (derivation device) |
| reachable set | 7-2 | taught | Note 112 (reachable sets) |
| real-time systems | 1-6 | out-of-scope | computing topic (real-time systems) |
| realization | 9-12 | out-of-scope | realization theory (minimal realizations) |
| realization, minimal | 9-13 | out-of-scope | realization theory (minimal realizations) |
| reasoning | 15-29 | out-of-scope | AI reasoning, FBS ch.15 survey |
| receding horizon control | 15-10 | taught | Note 207 (receding horizon) |
| rectified linear unit (ReLu) | 15-36 | taught | DL-028 (ReLU) |
| reference signal | 1-18, 2-1, 7-9, 7-10, 8-24, 9-2, 9-18, 11-2, 11-20 (see also command signal; setpoint) | taught | Note 117 (reference / setpoint) |
| reference signal, effect on observer error | 8-12, 8-17, 8-24 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). reference and observer error |
| reference signal, response to | 2-19, 12-7, 13-29 | taught | Note 206 (tracking a reference) |
| reference signal, tracking | 2-2, 2-17, 7-10, 8-23, 8-28, 12-13, 13-17–13-18 | taught | Note 206 (tracking a reference) |
| reference weighting |  (see setpoint weighting) | index-noise | cross-reference |
| region of attraction |  (see equilibrium points: regions of attraction) | index-noise | cross-reference |
| regression analysis | 15-3 | taught | ML-049 (regression) |
| regulation problem | 2-12 | taught | Note 205 (regulation = LQR regulator) |
| regulator |  (see control law) | index-noise | cross-reference |
| reinforcement learning | 15-33 | taught | Note 1 (reinforcement learning) |
| relative degree | 9-24 | add | **tf** → RO-06 Feedback control, new Note after Note 118. relative degree |
| relative gain array (RGA) | 15-25–15-26 | out-of-scope | relative gain array: process-control MIMO design |
| relay feedback | 10-26, 11-14 | add | **pidtune** → RO-06, extend Note 117 (PD and PID control) or a new Note after Note 119. relay feedback |
| Reno (protocol) |  (see Internet; congestion control) | index-noise | cross-reference |
| repressilator | 3-41 | out-of-scope | biology |
| repressor | 1-13, 3-41, 3-47, 5-23, 6-38, 9-37 (see also biological circuits) | out-of-scope | biology |
| requirements |  (see performance specifications) | index-noise | cross-reference |
| reset logic | 3-8 | out-of-scope | hybrid-system reset logic (FBS §3.4) |
| reset, in PID control | 11-4, 11-5 | taught | Note 119 (reset = integral action) |
| resonant frequency | 10-23 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. resonant frequency and peak |
| resonant frequency, for second-order systems | 7-20 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. resonant frequency and peak |
| resonant peak | 6-25, 13-12 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. resonant frequency and peak |
| resonant peak, for second-order systems | 7-20 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. resonant frequency and peak |
| resource usage, in computing systems | 3-36, 3-38, 4-11, 4-12 | out-of-scope | computing systems |
| response |  (see input/output models) | index-noise | cross-reference |
| retina | 11-6 (see also pupil response) | out-of-scope | biology |
| Riccati differential equation | 7-28 | taught | Note 205 (Riccati equation; continuous form of the recursion) |
| Riccati equation | 7-28, 8-20, 13-25, 13-28 | taught | Note 205 (Riccati equation) |
| Riemann sphere | 13-6 | out-of-scope | advanced robust-control geometry (Riemann sphere) |
| right half-plane poles and zeros |  (see poles: right half-plane; zeros: right half-plane) | index-noise | cross-reference |
| rise time | 2-12, 6-21, 6-36, 7-10, 7-19, 12-6, 12-32 | add | **ssresp** → RO-06, extend Note 118 (step response and second-order systems). rise time |
| rise time, for second-order systems | 7-20 | add | **ssresp** → RO-06, extend Note 118 (step response and second-order systems). rise time |
| rise time-bandwidth product | 12-9, 12-32 | add | **ssresp** → RO-06, extend Note 118 (step response and second-order systems). rise time - bandwidth product |
| robotics | 1-9, 6-34 | index-noise | pointer to robotics applications |
| robust stability | 13-3 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. robust stability |
| robustness | 1-12, 1-14–1-15, 2-3, 2-20–2-23, 11-20, 12-6, 13-4, 13-28 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. robustness |
| robustness, nonlinear gain variations | 2-20, 13-12 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. robustness |
| robustness, performance | 13-15–13-28 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. robustness |
| robustness, stability | 13-9–13-15, 13-26 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. robustness |
| robustness, using gain and phase margin | 10-17, 12-13 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. robustness via gain and phase margins |
| robustness, using maximum sensitivity | 12-10, 12-13, 13-9, 13-29 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. robustness via maximum sensitivity |
| robustness, using Vinnicombe metric | 13-26 | out-of-scope | Vinnicombe metric: advanced robust control |
| robustness, via gain and phase margin | 10-16 (see also uncertainty) | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. robustness via margins |
| roll-off |  (see high-frequency roll-off) | index-noise | cross-reference |
| root locus diagram | 5-31, 5-32, 12-24–12-27 | add | **rootlocus** → RO-06 Feedback control, short section in the transfer-function Note. root locus |
| root locus diagram, asymptotes | 12-33 | add | **rootlocus** → RO-06 Feedback control, short section in the transfer-function Note. root locus |
| root locus diagram, initial direction | 12-34 | add | **rootlocus** → RO-06 Feedback control, short section in the transfer-function Note. root locus |
| root locus diagram, real line segments | 12-34 | add | **rootlocus** → RO-06 Feedback control, short section in the transfer-function Note. root locus |
| Routh-Hurwitz criterion | 2-9 | add | **tf** → RO-06 Feedback control, new Note after Note 118. Routh-Hurwitz criterion (named) |
| routing matrix | 4-15 | out-of-scope | networking |
| rush-hour effect | 3-36 | out-of-scope | queuing |
| saddle (equilibrium point) | 5-10 | add | **eqtypes** → MA 06-calculus, extend the planned Stability of dynamical systems Note (plan §4). saddle |
| safety | 15-20 | taught | Note 197 (safety filters); RO-14 |
| sampling | 6-27–6-28, 8-30, 8-31, 11-22 | add | **sampling** → RO-08, extend Note 136 (Delays and control rate), or RO-06 after the PID Notes. sampling |
| saturation function | 2-2, 2-26, 3-24, 4-8, 11-22 (see also actuators: saturation) | taught | Note 119 (saturation) |
| scaling |  (see normalized coordinates) | index-noise | cross-reference |
| scanning tunneling microscope | 4-17 | out-of-scope | application example (microscopy) |
| schematic diagrams | 3-23, 3-24, 4-8 | out-of-scope | electrical schematics |
| Schitter, G. | 4-20, 4-21 | index-noise | person |
| Schmitt trigger | 2-27 | out-of-scope | electronics (Schmitt trigger) |
| second-order systems | 2-29, 3-3, 6-35, 7-17–7-21, 7-35, 9-31, 9-32, 11-10, 12-32 | taught | Note 118 (second-order systems) |
| sector-bounded nonlinearities | 10-24, 11-17, 11-19, 13-12–13-13, 14-27 | out-of-scope | sector-bounded nonlinearities: nonlinear analysis, advanced |
| Segway Personal Transporter | 3-12, 7-5 | out-of-scope | application example (Segway); balance models are Note 296 |
| selector control | 1-23, 15-20–15-21 | out-of-scope | process-control selectors |
| self-activation | 5-38 | out-of-scope | biology |
| self-optimizing controllers | 15-24 | out-of-scope | process-control optimisation |
| self-repression | 6-38, 9-36 | out-of-scope | biology |
| semidefinite function | 5-19 | taught | plan §4 new maths: Lyapunov functions |
| sensitivity crossover frequency | 12-6, 12-9, 12-10 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. sensitivity crossover frequency |
| sensitivity function | 2-3, 12-3, 12-13, 12-34, 13-9, 13-17, 13-29, 14-25 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. sensitivity function |
| sensitivity function, and disturbance attenuation | 12-9, 12-32, 14-6 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. sensitivity function |
| sensor fusion | 15-23 | taught | Note 86 (sensor fusion) |
| sensor matrix | 3-10, 3-14 | taught | plan §4 State-space models (C matrix) |
| sensor networks | 3-38 | out-of-scope | sensor networks (FBS §3.4 consensus example) |
| sensors | 1-5, 8-2, 8-30, 10-20, 11-22, 12-2, 12-5, 14-4, 14-13 | taught | Notes 74, 83 (robot sensors) |
| sensors, effect on zeros | 10-20, 14-4 | out-of-scope | design insight on sensor placement and zeros, advanced |
| sensors, in computing systems | 4-11 (see also measured signals) | out-of-scope | computing systems |
| separation principle | 8-13, 8-22, 8-32 | add | **observer** → RO-15, new Note after Note 204 (state feedback and pole placement). separation principle |
| series connection | 2-10, 2-11, 9-17 | add | **tf** → RO-06 Feedback control, new Note after Note 118. series connection |
| service rate (queuing systems) | 3-36 | out-of-scope | queuing |
| servo problem | 2-17 | taught | Note 206 (tracking = servo problem) |
| setpoint | 1-16, 11-2 | taught | Note 117 (setpoint) |
| setpoint weighting | 11-20, 11-23 | add | **pidtune** → RO-06, extend Note 117 (PD and PID control) or a new Note after Note 119. setpoint weighting |
| settling time | 2-12, 6-21, 6-36, 7-10, 12-6 | taught | Note 118 (settling time) |
| settling time, for second-order systems | 7-20 | taught | Note 118 (settling time) |
| sgn (function) | 4-3 | out-of-scope | notation (sign function) |
| ship dynamics | 5-16, 15-31 | out-of-scope | ship example |
| signal blocking |  (see zeros: signal blocking property) | index-noise | cross-reference |
| similarity of two systems | 13-4–13-9 | out-of-scope | Vinnicombe similarity, advanced robust control |
| simulation | 3-9, 3-19–3-20 | taught | plan §4 new maths: Numerical integration of ODEs |
| SIMULINK | 6-31 | index-noise | software |
| single-input, single-output (SISO) systems | 5-1, 6-2, 6-3, 6-29, 8-4, 10-23 | add | **tf** → RO-06 Feedback control, new Note after Note 118. single-input single-output systems |
| singular values | 10-22, 10-23 | out-of-scope | MIMO system gains (singular values), beyond course level |
| sink (equilibrium point) | 5-10 | add | **eqtypes** → MA 06-calculus, extend the planned Stability of dynamical systems Note (plan §4). sink |
| small gain theorem | 10-24, 13-12 | out-of-scope | small-gain theorem, advanced |
| Smith predictor | 15-22 | out-of-scope | Smith predictor: process-control delay compensation |
| smoothness | 15-3 | out-of-scope | generic requirement word (FBS ch.15) |
| software tools for control | x | index-noise | software pointer |
| solution (ODE) |  (see differential equations: solutions) | index-noise | cross-reference |
| source (equilibrium point) | 5-10 | add | **eqtypes** → MA 06-calculus, extend the planned Stability of dynamical systems Note (plan §4). source |
| specifications |  (see performance specifications) | index-noise | cross-reference |
| spectrum analyzer | 9-38 | out-of-scope | lab instrument |
| Sperry autopilot | 1-16 | out-of-scope | history of control (FBS ch.1) |
| spring-mass system | 3-2, 3-11–3-12, 3-19–3-22, 3-45, 4-18, 5-22, 5-36, 6-12, 9-36 | taught | plan §4 new maths: Second-order linear systems (mass-spring-damper) |
| spring-mass system, generalized | 3-12, 4-7 | out-of-scope | generalized mechanical model, beyond course level |
| spring-mass system, identification | 3-27 | taught | Note 139 (system identification) |
| spring-mass system, normalization | 3-28, 3-45 (see also atomic force microscopes; coupled spring-mass system; oscillator dynamics; vehicle suspension; vibration damper) | out-of-scope | modelling technique (normalisation) |
| stability | 1-5, 1-15, 2-9, 3-21, 5-4, 5-8–5-28 | taught | plan §4 Stability of dynamical systems |
| stability, asymptotic stability | 5-8, 5-13, 5-18 | taught | plan §4 Stability of dynamical systems |
| stability, conditional | 10-13–10-14 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. conditional stability |
| stability, in the sense of Lyapunov | 5-8 | taught | plan §4 Stability of dynamical systems (Lyapunov stability) |
| stability, internal | 12-5 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. internal stability |
| stability, local versus global | 5-10, 5-29 | add | **eqtypes** → MA 06-calculus, extend the planned Stability of dynamical systems Note (plan §4). local vs global stability |
| stability, Lyapunov analysis |  (see Lyapunov stability analysis) | index-noise | cross-reference |
| stability, neutral | 5-8, 5-10 | taught | plan §4 Stability of dynamical systems (neutral / marginal) |
| stability, of a system | 5-12 | taught | plan §4 Stability of dynamical systems |
| stability, of equilibrium points | 3-21, 5-8, 5-10, 5-19, 5-26, 5-27 | taught | plan §4 Stability of dynamical systems |
| stability, of feedback loop |  (see Nyquist criterion) | index-noise | cross-reference |
| stability, of limit cycles | 5-17–5-18 | taught | Note 299 (limit cycles, Poincaré maps) |
| stability, of linear systems | 5-11–5-14, 5-21, 6-10 | taught | plan §4 Stability of dynamical systems |
| stability, of solutions | 5-8, 5-9, 5-18 | taught | plan §4 Stability of dynamical systems |
| stability, of transfer functions | 9-24 | add | **tf** → RO-06 Feedback control, new Note after Note 118. stability of transfer functions |
| stability, robust |  (see robust stability) | index-noise | cross-reference |
| stability, Routh-Hurwitz criterion | 2-9 | add | **tf** → RO-06 Feedback control, new Note after Note 118. Routh-Hurwitz criterion |
| stability, unstable solutions | 5-10 | taught | plan §4 Stability of dynamical systems; plan §5 recap Taylor linearisation |
| stability, using eigenvalues | 5-26, 6-10, 6-11 | taught | plan §4 Stability of dynamical systems; plan §5 recap Taylor linearisation |
| stability, using linear approximation | 5-14, 5-26, 6-30 | taught | plan §4 Stability of dynamical systems; plan §5 recap Taylor linearisation |
| stability, using state feedback | 7-9–7-32 (see also bifurcations; equilibrium points) | taught | Note 204 (stabilising by state feedback) |
| stability diagram |  (see parametric stability diagram) | index-noise | cross-reference |
| stability margin (quantity) | 10-15, 10-17, 12-10, 13-9, 13-29, 14-31 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. stability margins |
| stability margin (quantity), for Bode’s ideal transfer function | 13-30 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. stability margins |
| stability margin (quantity), generalized | 13-25, 13-26 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. stability margins |
| stability margin (quantity), reasonable values | 10-17 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. stability margins |
| stability margins (concept) | 10-14–10-18, 12-14, 13-30 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. stability margins |
| stabilizability | 14-2–14-3 | out-of-scope | stabilizability: refinement of controllability (FBS §14.1) |
| Stark, L. | 9-39 | index-noise | person |
| state, of a dynamical system | 3-2, 3-6, 3-10 | taught | plan §4 State-space models; Note 63 |
| state estimators |  (see observers) | index-noise | cross-reference |
| state feedback | 7-1–7-32, 8-7, 8-13, 13-24, 15-19 (see also eigenvalue assignment; linear quadratic control) | taught | Note 204 (state feedback) |
| state space | 3-2, 3-10–3-22, 7-9 | taught | plan §4 State-space models |
| state vector | 3-3, 3-10 | taught | plan §4 State-space models |
| state, of a dynamical system | 7-1 | taught | plan §4 State-space models |
| static gain |  (see gain, zero frequency) | index-noise | cross-reference |
| steady-state gain |  (see zero frequency gain) | index-noise | cross-reference |
| steady-state response | 1-29, 2-12, 3-20, 6-19–6-21, 6-23, 6-27, 7-11, 9-2, 9-38, 9-40 | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). steady-state response |
| steady-state response, for second-order systems | 7-20 | add | **ssresp** → RO-06, extend Note 118 (step response and second-order systems). steady state of second-order systems |
| steady-state solution | 9-5 | add | **tf** → RO-06 Feedback control, new Note after Note 118. steady-state solution for exponential inputs |
| steam engines | 1-2, 1-3, 1-14 | out-of-scope | history (steam engines) |
| steering |  (see vehicle steering) | index-noise | cross-reference |
| Stein, G. | xii, 12-1, 14-6, 14-7 | index-noise | person |
| step input | 3-5, 6-5, 6-20, 9-23 | taught | Note 118 (step input and response) |
| step response | 2-11, 2-12, 3-5, 3-27, 3-28, 6-5, 6-17, 6-20, 6-21, 7-10, 7-18–7-20, 11-11, 12-32 | taught | Note 118 (step input and response) |
| step response, relationship to frequency response | 10-21, 12-8, 12-9, 12-12, 12-32 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. step response vs frequency response |
| stereographic projection | 13-6 | out-of-scope | advanced robust-control geometry |
| stochastic systems | 8-17, 8-19 | taught | Note 80 (stochastic linear systems) |
| strictly proper | 9-24 | add | **tf** → RO-06 Feedback control, new Note after Note 118. strictly proper |
| strong stabilizability | 14-2, 14-3 | out-of-scope | strong stabilizability, advanced |
| summing junction | 3-24 | add | **tf** → RO-06 Feedback control, new Note after Note 118. summing junction |
| superposition | 3-4, 6-3, 6-4, 6-17, 6-27, 6-35, 9-2, 9-17 | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). superposition |
| superregenerative amplifier | 2-4 | out-of-scope | history (electronics) |
| supervised learning | 15-33 | taught | ML-003 (supervised learning) |
| supervisory control | 1-23, 1-25, 1-27, 15-9, 15-12–15-14 (see also decision making: higher levels of) | taught | Note 126 (supervisory layers); Note 130 |
| supply chains | 1-11, 1-12, 1-25 | out-of-scope | supply chains, different field |
| supremum (sup) | 10-23 | out-of-scope | notation (supremum) |
| switching behavior | 5-25, 5-26, 13-27 | out-of-scope | switching behaviour in biology / gain switching, FBS examples |
| system design | 14-1, 15-2 | out-of-scope | systems-engineering design |
| system identification | 3-27, 3-28, 3-45, 9-38 | taught | Note 139 (system identification) |
| system inversion |  (see inverse model) | index-noise | cross-reference |
| tapping mode |  (see atomic force microscopes) | index-noise | cross-reference |
| task description | 8-23 | taught | Note 201 (trajectory generation as the task description) |
| TCP/IP |  (see Internet; congestion control) | index-noise | cross-reference |
| temporal logic | 15-13 | out-of-scope | formal methods (temporal logic) |
| Teorell, T. | 4-21, 4-23 | index-noise | person |
| test points | 12-12, 15-5 | out-of-scope | lab practice (test points) |
| thermofluid systems | 3-32–3-34, 5-35, 9-11, 10-29 | out-of-scope | thermofluid examples, different field |
| thermofluid systems, drum boiler | 3-34 | out-of-scope | thermofluid examples, different field |
| thermofluid systems, water heater | 3-33 | out-of-scope | thermofluid examples, different field |
| three-term controllers | 11-2 (see also PID control) | taught | Note 117 (three-term = PID) |
| thrust vectored aircraft |  (see vectored thrust aircraft) | index-noise | cross-reference |
| time constant | 2-6, 6-36 | add | **ssresp** → RO-06, extend Note 118 (step response and second-order systems). time constant |
| time delay | 1-10, 9-10, 9-11, 10-3, 10-17, 10-20, 11-12, 11-13, 11-22, 12-20, 14-5, 14-13, 14-14, 14-20, 14-32 | add | **tf** → RO-06 Feedback control, new Note after Note 118. time delay |
| time delay, Padé approximation | 10-30, 14-5 | add | **tf** → RO-06 Feedback control, new Note after Note 118. Padé approximation |
| time plot | 3-3 | out-of-scope | generic plot word |
| time-invariant systems | 2-6, 3-4, 3-10, 5-35, 6-4–6-6 | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). time-invariant systems |
| tracking |  (see reference signal: tracking) | index-noise | cross-reference |
| tracking mode | 11-18 | add | **pidtune** → RO-06, extend Note 117 (PD and PID control) or a new Note after Note 119. tracking mode (bumpless transfer) |
| traffic light controller | 3-18 | out-of-scope | example (traffic-light state machine); state machines are Note 130 |
| trail (bicycle dynamics) | 4-6, 4-7 | out-of-scope | bicycle geometry detail |
| transcription factors | 3-40 | out-of-scope | biology |
| transcriptional regulation |  (see gene regulation) | index-noise | cross-reference |
| transfer functions | 2-6–2-9, 9-1–9-40 | add | **tf** → RO-06 Feedback control, new Note after Note 118. transfer functions |
| transfer functions, and frequency response | 9-2, 9-29 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. transfer function and frequency response |
| transfer functions, and impulse response | 9-16 | add | **laplace** → MA 06-calculus, new Note after the planned ODEs and State-space models Notes (plan §4). transfer function = transform of the impulse response |
| transfer functions, by inspection | 9-9, 9-20 | add | **tf** → RO-06 Feedback control, new Note after Note 118. transfer functions: by inspection, for control systems, derivation, differentiator |
| transfer functions, derivation using exponential signals | 9-3 | add | **tf** → RO-06 Feedback control, new Note after Note 118. transfer functions: by inspection, for control systems, derivation, differentiator |
| transfer functions, for control systems | 9-18, 9-43 | add | **tf** → RO-06 Feedback control, new Note after Note 118. transfer functions: by inspection, for control systems, derivation, differentiator |
| transfer functions, for differentiator | 9-11 | add | **tf** → RO-06 Feedback control, new Note after Note 118. transfer functions: by inspection, for control systems, derivation, differentiator |
| transfer functions, for electrical circuits | 9-9 | out-of-scope | electrical circuits |
| transfer functions, for integrator | 9-11 | add | **tf** → RO-06 Feedback control, new Note after Note 118. transfer functions: integrator, linear I/O systems, state space, time delay |
| transfer functions, for linear input/output systems | 2-8, 9-8, 9-10, 9-11, 9-43 | add | **tf** → RO-06 Feedback control, new Note after Note 118. transfer functions: integrator, linear I/O systems, state space, time delay |
| transfer functions, for state space systems | 9-3, 9-11, 9-15, 9-42 | add | **tf** → RO-06 Feedback control, new Note after Note 118. transfer functions: integrator, linear I/O systems, state space, time delay |
| transfer functions, for time delay | 9-10, 9-11 | add | **tf** → RO-06 Feedback control, new Note after Note 118. transfer functions: integrator, linear I/O systems, state space, time delay |
| transfer functions, from experiments | 9-37 | add | **freqresp** → RO-06 Feedback control, new Note after the transfer-function Note. transfer functions from experiments |
| transfer functions, irrational | 9-11, 9-12 | out-of-scope | irrational transfer functions (heat equation), advanced |
| transfer functions, qualitative insight | 9-36 | add | **tf** → RO-06 Feedback control, new Note after Note 118. qualitative insight from transfer functions |
| transient response | 3-20, 6-19, 6-20, 6-23, 6-27, 7-2, 7-22, 9-4–9-5 | add | **linresp** → MA 06-calculus, new Note after the planned Matrix exponential Note (plan §4). transient response |
| Transmission Control Protocol (TCP) | 4-14 | out-of-scope | networking |
| transmission zero |  (see zeros, blocking property) | index-noise | cross-reference |
| transportation systems | 1-24–1-25 | out-of-scope | application domain (transportation) |
| Tsien, H. S. | 1-9 | index-noise | person |
| tuning rules |  (see Ziegler-Nichols tuning) | index-noise | cross-reference |
| Tustin, A. | 2-1 | index-noise | person |
| two degree-of-freedom control | 2-2, 2-18–2-20, 8-23, 8-24, 11-2, 11-20, 12-1, 12-18, 12-30, 12-31, 13-30 | taught | Note 119 (feedforward plus feedback) |
| two-out-of-three selectors | 15-20 | out-of-scope | process-control selectors |
| uncertainty | 1-5, 1-14–1-15, 3-6, 3-8–3-10, 7-24, 13-1–13-9 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. uncertainty (parameter variation, disturbances, noise) |
| uncertainty, component or parameter variation | 1-5, 2-3, 13-1 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. uncertainty (parameter variation, disturbances, noise) |
| uncertainty, disturbances and noise | 1-5, 3-6, 7-9, 9-18, 12-2 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. uncertainty (parameter variation, disturbances, noise) |
| uncertainty, static uncertainty | 3-9 | out-of-scope | static uncertainty illustration (FBS §3.1) |
| uncertainty, unmodeled dynamics | 1-5, 2-16–2-17, 3-9, 13-3, 13-10 (see also additive uncertainty; feedback uncertainty; multiplicative uncertainty; parametric uncertainty) | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. unmodeled dynamics |
| uncertainty band | 3-9 | out-of-scope | FBS illustrations of uncertainty (uncertainty band / lemon) |
| uncertainty lemon | 3-9, 4-4, 4-10, 4-20 | out-of-scope | FBS illustrations of uncertainty (uncertainty band / lemon) |
| underdamped oscillator | 5-3, 7-18, 7-19 | taught | plan §4 Second-order linear systems (underdamped) |
| unit step | 6-20 | taught | Note 118 (unit step) |
| unmodeled dynamics |  (see uncertainty: unmodeled dynamics) | index-noise | cross-reference |
| unstable pole |  (see poles: right half-plane) | index-noise | cross-reference |
| unstable solution, for a dynamical system | 5-10, 5-13, 6-11, 9-25 | taught | plan §4 Stability of dynamical systems |
| unstable zero |  (see zeros: right half-plane) | index-noise | cross-reference |
| V-model | 15-2 | out-of-scope | systems-engineering V-model |
| variation of the argument, principle of | 10-10, 10-27 | out-of-scope | principle of the argument: complex-analysis proof behind Nyquist |
| vector field | 3-3, 5-5 | taught | plan §4 new maths: ODEs and vector fields |
| vectored thrust aircraft | 3-31–3-32, 6-11–6-12, 7-29–7-30, 8-20–8-21, 9-43, 12-17, 12-27–12-30 | out-of-scope | FBS running example (planar VTOL aircraft); aerial robots are RO-17 |
| vehicle steering | 3-30–3-31, 3-46, 6-32–6-33, 7-11–7-13, 8-10, 8-13–8-14, 8-25–8-26, 8-28–8-29, 9-21–9-22, 10-20–10-22, 12-19–12-20, 14-4–14-5, 14-22–14-24 (see also ship dynamics) | taught | Note 67, Note 253 (vehicle steering) |
| vehicle suspension | 9-43 (see also coupled spring-mass system) | out-of-scope | vehicle suspension example |
| vertical takeoff and landing |  (see vectored thrust aircraft) | index-noise | cross-reference |
| vibration damper | 9-9–9-10 | out-of-scope | mechanical example (vibration damper) |
| Vidyasagar, M. | 13-28 | index-noise | person |
| Vinnicombe, G. | 12-30, 13-6, 13-7, 13-28 | index-noise | person |
| Vinnicombe metric | 13-6–13-9, 13-26 | out-of-scope | Vinnicombe metric: advanced robust control |
| Vinnicombe metric, numerical computation | 13-7 | out-of-scope | Vinnicombe metric: advanced robust control |
| voltage clamp | 1-9, 3-43 | out-of-scope | neuroscience lab method |
| Volterra equations |  (see Lotka-Volterra equations) | index-noise | cross-reference |
| water heater | 3-33 | out-of-scope | thermofluid example |
| waterbed effect | 14-6 | add | **sens** → RO-06 Feedback control, new Note after the Nyquist Note. waterbed effect (named) |
| Watt governor |  (see centrifugal governor) | index-noise | history cross-reference |
| Watt steam engine | 1-2, 1-14 | index-noise | history cross-reference |
| web server control | 4-12–4-13, 7-30–7-32, 11-25 | out-of-scope | computing systems |
| web site, companion | x | index-noise | book web site |
| Whipple, F. J. W. | 4-8 | index-noise | person |
| Wiener, N. | 1-9 | index-noise | person |
| winding number | 10-6, 10-10, 10-12, 13-6, 13-7 | add | **nyquist** → RO-06 Feedback control, new Note after the frequency-response Note. winding number (counting encirclements) |
| window size (TCP) | 4-15–4-17, 5-11 | out-of-scope | networking |
| windup |  (see integrator windup) | index-noise | cross-reference |
| windup, selector control | 15-21 | out-of-scope | process-control selectors |
| Wright, F. L. | 15-1 | index-noise | person |
| Wright, W. | 1-15 | index-noise | person |
| Wright Flyer | 1-8, 1-15 | out-of-scope | history of control (FBS ch.1) |
| X-29 aircraft | 14-7–14-8 | out-of-scope | application example (X-29) |
| Youla parameterization | 13-13–13-15 | out-of-scope | Youla parameterization: advanced |
| zero frequency gain | 2-8, 6-24, 7-11, 7-14, 9-23, 11-13 | add | **ssresp** → RO-06, extend Note 118 (step response and second-order systems). zero-frequency gain |
| zero frequency gain, for second-order systems | 7-20 | add | **ssresp** → RO-06, extend Note 118 (step response and second-order systems). zero-frequency gain |
| zeros | 2-8, 9-9, 9-23, 9-24 | add | **tf** → RO-06 Feedback control, new Note after Note 118. zeros and their blocking property |
| zeros, blocking property | 2-9 | add | **tf** → RO-06 Feedback control, new Note after Note 118. zeros and their blocking property |
| zeros, effect of sensors and actuators on | 10-20, 10-21, 14-4 | out-of-scope | design insight on sensor/actuator placement and zeros |
| zeros, for a state space system | 9-24 | add | **tf** → RO-06 Feedback control, new Note after Note 118. zeros of state-space systems; right-half-plane zeros; signal blocking |
| zeros, right half-plane | 9-25, 9-34, 10-20, 12-20, 14-7, 14-10, 14-12–14-14, 14-16, 14-17, 14-20, 14-25, 14-31 | add | **tf** → RO-06 Feedback control, new Note after Note 118. zeros of state-space systems; right-half-plane zeros; signal blocking |
| zeros, signal-blocking property | 9-24 | add | **tf** → RO-06 Feedback control, new Note after Note 118. zeros of state-space systems; right-half-plane zeros; signal blocking |
| zeros, slow | 14-22, 14-24, 14-25 | out-of-scope | slow zeros: fundamental-limits detail |
| zeros, stable/unstable | 14-22 | add | **tf** → RO-06 Feedback control, new Note after Note 118. stable / unstable zeros |
| Ziegler, J. G. | 11-11, 11-24 | index-noise | person |
| Ziegler-Nichols tuning | 11-11–11-14, 11-24 | add | **pidtune** → RO-06, extend Note 117 (PD and PID control) or a new Note after Note 119. Ziegler-Nichols tuning |

## Bullo, Lectures on Network Systems, ed. 1.7 (2024)

Index pages parsed: 300 terms. Pages are the book's own page labels.

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| algebraic connectivity | 112 | add | **graphlap** → MA 05-linear-algebra (new Note after MA-056 eigenvectors), first used by the consensus Note in RO-23. algebraic connectivity = 2nd-smallest Laplacian eigenvalue (LNS p.112) |
| algorithm |  (see system) | index-noise | cross-reference to "system" |
| arc |  | out-of-scope | circle arcs for phase oscillators (LNS ch.17); coupled-oscillator theory is a different field (physics/biology) |
| arc, clockwise arc length | 281 | out-of-scope | circle arcs for phase oscillators (LNS ch.17); coupled-oscillator theory is a different field (physics/biology) |
| arc, subset | 282 | out-of-scope | circle arcs for phase oscillators (LNS ch.17); coupled-oscillator theory is a different field (physics/biology) |
| basic graphs | 45 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. example graphs (path, cycle, star, complete) used to teach graph basics |
| basic graphs, adjacency matrices | 58 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. adjacency matrix |
| basic graphs, adjacency spectrum | 58 | out-of-scope | adjacency spectra of example graphs: spectral graph theory beyond course level |
| basic graphs, algebraic connectivity | 113 | add | **graphlap** → MA 05-linear-algebra (new Note after MA-056 eigenvectors), first used by the consensus Note in RO-23. algebraic connectivity of example graphs |
| behavior |  | index-noise | parent heading, no page |
| behavior, phase balancing | 287 | out-of-scope | phase balancing of oscillators (LNS ch.17), different field |
| behavior, synchronization |  | index-noise | parent heading, no page |
| behavior, synchronization, among double integrators | 155 | add | **consensus** → RO-23 Planning in depth, new Note before Note 271 (Planning with time and many robots). second-order (double-integrator) consensus |
| behavior, synchronization, in a network of clocks | 117 | out-of-scope | distributed clock sync in sensor networks; robot sensor time sync is Note 93 |
| behavior, synchronization, in inductors/capacitors circuits | 162 | out-of-scope | electrical circuits example, different field |
| behavior, synchronization, in Kuramoto oscillators | 282 | out-of-scope | Kuramoto oscillators, physics/biology field |
| centrality scores | 90 | out-of-scope | network centrality scores (LNS ch.5): social-network analysis, different field |
| centrality scores, betweenness | 93 | out-of-scope | network centrality scores (LNS ch.5): social-network analysis, different field |
| centrality scores, closeness | 93 | out-of-scope | network centrality scores (LNS ch.5): social-network analysis, different field |
| centrality scores, degree | 90 | out-of-scope | network centrality scores (LNS ch.5): social-network analysis, different field |
| centrality scores, eigenvector | 91 | out-of-scope | network centrality scores (LNS ch.5): social-network analysis, different field |
| centrality scores, Katz | 91 | out-of-scope | network centrality scores (LNS ch.5): social-network analysis, different field |
| centrality scores, PageRank | 92 | out-of-scope | network centrality scores (LNS ch.5): social-network analysis, different field |
| Collatz–Wielandt formula | 39 | out-of-scope | proof tool for Perron-Frobenius |
| compartmental digraph | 188 | out-of-scope | compartmental systems (LNS ch.9-10): pharmacokinetics/ecology models, different field |
| compartmental digraph, inflow connected | 191 | out-of-scope | compartmental systems (LNS ch.9-10): pharmacokinetics/ecology models, different field |
| compartmental digraph, outflow connected | 191 | out-of-scope | compartmental systems (LNS ch.9-10): pharmacokinetics/ecology models, different field |
| compartmental digraph, simple trap | 191 | out-of-scope | compartmental systems (LNS ch.9-10): pharmacokinetics/ecology models, different field |
| compartmental digraph, trap | 191 | out-of-scope | compartmental systems (LNS ch.9-10): pharmacokinetics/ecology models, different field |
| control law |  | index-noise | parent heading, no page |
| control law, averaging-based integral | 293 | out-of-scope | distributed averaging-based PI/PID control for power networks and clocks (LNS ch.6-7 exercises/advanced): research-level |
| control law, averaging-based proportional (discrete-time) | 119 | out-of-scope | distributed averaging-based PI/PID control for power networks and clocks (LNS ch.6-7 exercises/advanced): research-level |
| control law, averaging-based proportional, integral, derivative | 126 | out-of-scope | distributed averaging-based PI/PID control for power networks and clocks (LNS ch.6-7 exercises/advanced): research-level |
| control law, averaging-based proportional, integral (discretetime) | 119 | out-of-scope | distributed averaging-based PI/PID control for power networks and clocks (LNS ch.6-7 exercises/advanced): research-level |
| control law, complex affine averaging | 145 | out-of-scope | complex-weight formation laws: research-level |
| control law, diffusive coupling | 156 | add | **consensus** → RO-23 Planning in depth, new Note before Note 271 (Planning with time and many robots). diffusive coupling / position-velocity averaging = consensus laws |
| control law, diffusive coupling | 147 | add | **consensus** → RO-23 Planning in depth, new Note before Note 271 (Planning with time and many robots). diffusive coupling / position-velocity averaging = consensus laws |
| control law, proportional, derivative, position- and velocityaveraging | 148 | add | **consensus** → RO-23 Planning in depth, new Note before Note 271 (Planning with time and many robots). diffusive coupling / position-velocity averaging = consensus laws |
| control law, robotic coordination |  | index-noise | parent heading, no page |
| control law, robotic coordination, rendezvous | 40 | add | **multirobot** → RO-23, new Note after the consensus Note, before Note 273 (Coverage planning). rendezvous |
| control law, robotic coordination |  | index-noise | parent heading (repeat), no page |
| control law, robotic coordination, affine gradient | 251 | add | **multirobot** → RO-23, new Note after the consensus Note, before Note 273 (Coverage planning). robotic coordination laws: affine formation gradient, centering, cyclic balancing/pursuit, deployment, rendezvous |
| control law, robotic coordination, centering | 142 | add | **multirobot** → RO-23, new Note after the consensus Note, before Note 273 (Coverage planning). robotic coordination laws: affine formation gradient, centering, cyclic balancing/pursuit, deployment, rendezvous |
| control law, robotic coordination, cyclic balancing | 12 | add | **multirobot** → RO-23, new Note after the consensus Note, before Note 273 (Coverage planning). robotic coordination laws: affine formation gradient, centering, cyclic balancing/pursuit, deployment, rendezvous |
| control law, robotic coordination, cyclic pursuit | 11 | add | **multirobot** → RO-23, new Note after the consensus Note, before Note 273 (Coverage planning). robotic coordination laws: affine formation gradient, centering, cyclic balancing/pursuit, deployment, rendezvous |
| control law, robotic coordination, deployment | 141 | add | **multirobot** → RO-23, new Note after the consensus Note, before Note 273 (Coverage planning). robotic coordination laws: affine formation gradient, centering, cyclic balancing/pursuit, deployment, rendezvous |
| control law, robotic coordination, rendezvous | 99, 141 | add | **multirobot** → RO-23, new Note after the consensus Note, before Note 273 (Coverage planning). robotic coordination laws: affine formation gradient, centering, cyclic balancing/pursuit, deployment, rendezvous |
| convergence factor |  | index-noise | parent heading, no page |
| convergence factor, asymptotic | 213 | add | **consensus** → RO-23 Planning in depth, new Note before Note 271 (Planning with time and many robots). convergence rate of averaging |
| convergence factor, mean-square | 239 | out-of-scope | mean-square convergence of randomized (gossip) averaging, LNS ch.14: research-level |
| convergence factor, per-step | 213 | add | **consensus** → RO-23 Planning in depth, new Note before Note 271 (Planning with time and many robots). per-step convergence factor of averaging |
| convex combination | 28 | taught | MA-067 (convex sets: convex combination, glossary entry) |
| convex combination, coefficients | 29 | taught | MA-067 (convex sets: convex combination, glossary entry) |
| cycle |  (see graph, cycle and digraph, cycle) | index-noise | cross-reference |
| digraph |  | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. directed graph (digraph) |
| digraph, acyclic | 47 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. acyclic (DAG) |
| digraph, aperiodic | 48 | add | **markovconv** → MA 02-probability, extend the planned Markov chains Note (plan §4). aperiodic digraph = aperiodic chain condition |
| digraph, binary adjacency matrix of | 57 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. binary adjacency matrix |
| digraph, condensation digraph | 49 | out-of-scope | condensation digraph: graph-theory proof device (LNS §3) |
| digraph, cycle | 47 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. cycle, directed walk (path) |
| digraph, directed walk | 47 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. cycle, directed walk (path) |
| digraph, node |  | index-noise | parent heading, no page |
| digraph, node, in-degree | 46 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. in/out-degree, in/out-neighbours, sink, source |
| digraph, node, in-neighbor of | 46 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. in/out-degree, in/out-neighbours, sink, source |
| digraph, node, out-degree | 46 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. in/out-degree, in/out-neighbours, sink, source |
| digraph, node, out-neighbor of | 46 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. in/out-degree, in/out-neighbours, sink, source |
| digraph, node, sink | 47 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. in/out-degree, in/out-neighbours, sink, source |
| digraph, node, source | 47 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. in/out-degree, in/out-neighbours, sink, source |
| digraph, periodic | 48 | add | **markovconv** → MA 02-probability, extend the planned Markov chains Note (plan §4). periodic digraph |
| digraph, reverse | 48 | out-of-scope | reverse digraph: book-specific operation used in LNS proofs |
| digraph, strongly connected | 48 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. strong connectivity and strongly connected components |
| digraph, strongly connected component | 49 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. strong connectivity and strongly connected components |
| digraph, subgraph of | 46 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. subgraph |
| digraph, subgraph of, induced | 46 | out-of-scope | induced subgraph: graph-theory detail not used by robotics Notes |
| digraph, subgraph of, spanning | 46 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. spanning subgraph (leads to spanning tree) |
| digraph, topological sort | 54 | out-of-scope | topological sort: CS algorithm; LNS uses it only to order acyclic digraphs (p.54) |
| digraph, topologically balanced | 46 | out-of-scope | LNS-specific balance condition |
| digraph, undirected | 45 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. undirected graph as a special digraph |
| digraph, walk |  | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. walk |
| digraph, walk, directed |  (see digraph, directed walk) | index-noise | cross-reference |
| digraph, weakly connected | 48 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. weak connectivity |
| digraph, weighted |  (see weighted digraph) | index-noise | cross-reference |
| Dini derivatives | 263 | out-of-scope | Dini derivatives: non-smooth analysis, research-level |
| disagreement |  | index-noise | parent heading, no page |
| disagreement, cumulative quadratic | 215 | out-of-scope | LNS-specific disagreement functions used in convergence proofs |
| disagreement, max-min | 86 | out-of-scope | LNS-specific disagreement functions used in convergence proofs |
| disagreement, quadratic | 85 | add | **graphlap** → MA 05-linear-algebra (new Note after MA-056 eigenvectors), first used by the consensus Note in RO-23. quadratic disagreement x^T L x |
| disagreement, relative | 175 | out-of-scope | LNS-specific disagreement measure |
| disagreement, vector | 84, 137, 214 | add | **consensus** → RO-23 Planning in depth, new Note before Note 271 (Planning with time and many robots). disagreement vector (distance from agreement) |
| dynamical flow system | 188 | out-of-scope | dynamical flow (compartmental) systems: different field |
| dynamical flow system, compartmental matrix | 190 | out-of-scope | dynamical flow (compartmental) systems: different field |
| dynamical flow system, flow rate matrix | 190 | out-of-scope | dynamical flow (compartmental) systems: different field |
| dynamical flow system, linear | 190 | out-of-scope | dynamical flow (compartmental) systems: different field |
| dynamical flow system, reduced | 193 | out-of-scope | dynamical flow (compartmental) systems: different field |
| effective resistence | 115 | out-of-scope | effective resistance: electrical-network theory, different field |
| eigenpair | 23 | taught | MA-056 (eigenvectors and eigenvalues) |
| eigenvalue | 23 | taught | MA-056 (eigenvectors and eigenvalues) |
| eigenvalue, algebraic multiplicity of | 25 | add | **eigmult** → MA 05-linear-algebra, extend MA-056 (eigenvectors and eigenvalues). algebraic multiplicity |
| eigenvalue, dominant | 32 | add | **perron** → MA 02-probability, inside the planned Markov chains Note (plan §4). dominant eigenvalue |
| eigenvalue, geometric multiplicity of | 25 | add | **eigmult** → MA 05-linear-algebra, extend MA-056 (eigenvectors and eigenvalues). geometric multiplicity, semisimple, simple eigenvalue |
| eigenvalue, semisimple | 25 | add | **eigmult** → MA 05-linear-algebra, extend MA-056 (eigenvectors and eigenvalues). geometric multiplicity, semisimple, simple eigenvalue |
| eigenvalue, simple | 25 | add | **eigmult** → MA 05-linear-algebra, extend MA-056 (eigenvectors and eigenvalues). geometric multiplicity, semisimple, simple eigenvalue |
| eigenvector | 23 | taught | MA-056 |
| eigenvector, dominant | 32 | add | **perron** → MA 02-probability, inside the planned Markov chains Note (plan §4). dominant eigenvector |
| equal-neighbor matrix | 87 | add | **consensus** → RO-23 Planning in depth, new Note before Note 271 (Planning with time and many robots). equal-neighbour averaging weights |
| Fiedler eigenpair | 112 | add | **graphlap** → MA 05-linear-algebra (new Note after MA-056 eigenvectors), first used by the consensus Note in RO-23. Fiedler eigenpair |
| function |  | index-noise | parent heading, no page |
| function, convex and strictly convex | 269 | taught | MA-065, MA-067 (convex functions) |
| function, critical point of | 254 | taught | MA-064, MA-065 (critical/stationary points) |
| function, Dini derivative of | 263 | out-of-scope | Dini derivative: non-smooth analysis, research-level |
| function, global minimum point of | 254 | taught | MA-065 (global minimum) |
| function, Hessian matrix of | 262 | taught | MA-064 (Hessian) |
| function, level and sublevel set of | 254 | taught | MA-062 (level sets read as contours) |
| function, Lie derivative of | 256 | out-of-scope | notation: name for dV/dt along solutions; beginner texts (FBS ch.5) just write dV/dt |
| function, local minimum point of | 254 | taught | MA-065 (local minimum) |
| function, positive definite or semidefinite, locally or globally | 254 | taught | plan §4 new maths: Lyapunov functions (positive definite V is part of the definition) |
| function, proper | 255 | out-of-scope | technical conditions for global Lyapunov results (proof technique) |
| function, radially unbounded | 255 | out-of-scope | technical conditions for global Lyapunov results (proof technique) |
| Gelfand’s formula | 73 | out-of-scope | Gelfand's formula: proof tool for spectral radius |
| geodesic distance | 281 | out-of-scope | geodesic distance on the circle for oscillators (LNS ch.17), different field |
| graph |  | taught | Note 103 (graph as a model of a state space) |
| graph, acyclic | 47 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. acyclic graph |
| graph, adjacency spectrum | 58 | out-of-scope | adjacency spectrum: spectral graph theory beyond course level |
| graph, connected | 47 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. connected, connected component, cycle |
| graph, connected component of | 47 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. connected, connected component, cycle |
| graph, cycle | 47 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. connected, connected component, cycle |
| graph, edge | 45 | taught | Note 103 (edges of a graph) |
| graph, edge set of | 45 | taught | Note 103 (edges of a graph) |
| graph, edge space | 168 | out-of-scope | edge space: algebraic graph theory (cycle/cut spaces), LNS ch.9 |
| graph, incidence matrix | 165 | add | **graphlap** → MA 05-linear-algebra (new Note after MA-056 eigenvectors), first used by the consensus Note in RO-23. incidence matrix |
| graph, neighbor | 45 | taught | Note 103 (nodes and neighbours in graph search) |
| graph, node | 45 | taught | Note 103 (nodes and neighbours in graph search) |
| graph, node, degree | 45 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. node degree |
| graph, node set of | 45 | taught | Note 103 |
| graph, undirected | 45 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. undirected graph |
| graph, union | 228 | out-of-scope | union of time-varying graphs: research-level consensus (LNS ch.12) |
| graph, walk | 47 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. walk / simple walk (path) |
| graph, walk, simple | 47 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. walk / simple walk (path) |
| group | 37 | out-of-scope | group theory: plan §7 drops PA 4.6 on purpose (SE(2)/SE(3) taught as matrices) |
| Hicksian stability condition | 198 | out-of-scope | Hicksian stability: economics, different field |
| Kron reduction | 125 | out-of-scope | Kron reduction: electrical-network reduction, different field |
| Kronecker product | 149 | out-of-scope | Kronecker product: notation for stacking multi-dimensional agent states; each coordinate can be treated separately |
| Laplacian |  | add | **graphlap** → MA 05-linear-algebra (new Note after MA-056 eigenvectors), first used by the consensus Note in RO-23. Laplacian (graph) |
| Laplacian, flow | 6, 134 | add | **consensus** → RO-23 Planning in depth, new Note before Note 271 (Planning with time and many robots). Laplacian flow x' = -Lx |
| Laplacian, matrix | 110 | add | **graphlap** → MA 05-linear-algebra (new Note after MA-056 eigenvectors), first used by the consensus Note in RO-23. Laplacian matrix and Laplacian potential x^T L x |
| Laplacian, potential function | 109 | add | **graphlap** → MA 05-linear-algebra (new Note after MA-056 eigenvectors), first used by the consensus Note in RO-23. Laplacian matrix and Laplacian potential x^T L x |
| Laplacian, pseudoinverse | 114 | out-of-scope | Laplacian pseudoinverse: used for effective resistance (electrical networks) |
| Laplacian, second-order flow | 148 | add | **consensus** → RO-23 Planning in depth, new Note before Note 271 (Planning with time and many robots). second-order Laplacian flow |
| Laplacian, system | 114 | out-of-scope | Laplacian linear system L x = b for electrical networks (LNS §6), different field |
| leading principal minors | 198 | out-of-scope | alternative test of positive definiteness (Sylvester's criterion); the eigenvalue test is in MA-064 |
| linear matrix inequality (LMI) | 123 | out-of-scope | linear matrix inequalities: convex-optimisation research tool |
| linear matrix inequality (LMI) | 123, 157 | out-of-scope | linear matrix inequalities: convex-optimisation research tool |
| logarithmic-linear function | 258 | out-of-scope | book-specific function class |
| Lyapunov function | 86 | taught | plan §4 new maths: Lyapunov functions (short section in Note 117); Note 199 |
| Lyapunov equalities and inequalities | 260 | add | **lyapeq** → MA 06-calculus, extend the planned Stability of dynamical systems Note (plan §4). Lyapunov equation and inequality |
| Lyapunov equalities and inequalities | 123, 140, 157 | add | **lyapeq** → MA 06-calculus, extend the planned Stability of dynamical systems Note (plan §4). Lyapunov equation and inequality |
| Lyapunov function |  | taught | plan §4 new maths: Lyapunov functions and Stability of dynamical systems |
| Lyapunov function, candidate | 257 | taught | plan §4 new maths: Lyapunov functions and Stability of dynamical systems |
| Lyapunov function, global | 257 | taught | plan §4 new maths: Lyapunov functions and Stability of dynamical systems |
| Lyapunov function, local | 257 | taught | plan §4 new maths: Lyapunov functions and Stability of dynamical systems |
| Lyapunov function, quadratic | 85, 260 | add | **lyapeq** → MA 06-calculus, extend the planned Stability of dynamical systems Note (plan §4). quadratic Lyapunov function |
| Lyapunov function, weak | 257 | add | **lasalle** → MA 06-calculus, short section in the planned Stability of dynamical systems Note (plan §4). weak Lyapunov function (V' <= 0) |
| matrix |  | taught | MA-053 (matrices) |
| matrix, adjacency |  (see weighted digraph, adjacency matrix of) | index-noise | cross-reference |
| matrix, block triangular | 60 | out-of-scope | block triangular form: device in reducibility proofs |
| matrix, circulant | 70 | out-of-scope | circulant matrices: special structure for cycle-graph examples |
| matrix, continuous-time convergent or Hurwitz | 134 | taught | plan §4 new maths: Stability of dynamical systems (all eigenvalues in the left half-plane = Hurwitz) |
| matrix, continuous-time semi-convergent | 134 | out-of-scope | semi-convergent matrix: LNS term for matrices whose powers have a limit, used in averaging proofs |
| matrix, convergent | 24 | add | **dtstab** → MA 06-calculus, extend the planned Stability of dynamical systems Note (plan §4). convergent matrix (powers go to 0) |
| matrix, diagonally dominant |  | out-of-scope | diagonal dominance: sufficient eigenvalue-location test (Gersgorin), proof tool |
| matrix, diagonally dominant, quasi | 194 | out-of-scope | diagonal dominance: sufficient eigenvalue-location test (Gersgorin), proof tool |
| matrix, diagonally dominant, strictly row | 38 | out-of-scope | diagonal dominance: sufficient eigenvalue-location test (Gersgorin), proof tool |
| matrix, diagonally dominant, weakly column | 190 | out-of-scope | diagonal dominance: sufficient eigenvalue-location test (Gersgorin), proof tool |
| matrix, exponential | 134 | taught | plan §4 new maths: Matrix exponential and logarithm |
| matrix, image of | 23 | taught | MA-053, MA-058 (column space / image) |
| matrix, incidence | 165 | add | **graphlap** → MA 05-linear-algebra (new Note after MA-056 eigenvectors), first used by the consensus Note in RO-23. incidence matrix |
| matrix, Jordan normal form of | 25 | add | **eigmult** → MA 05-linear-algebra, extend MA-056 (eigenvectors and eigenvalues). Jordan normal form (named only) |
| matrix, kernel of | 23 | taught | MA-058 (null space) |
| matrix, Laplacian | 110 | add | **graphlap** → MA 05-linear-algebra (new Note after MA-056 eigenvectors), first used by the consensus Note in RO-23. Laplacian matrix |
| matrix, Laplacian, irreducible | 108 | out-of-scope | irreducible Laplacian: Perron-Frobenius proof class |
| matrix, Metzler | 184 | out-of-scope | Metzler matrices: positive-systems theory (LNS ch.10), research-level |
| matrix, non-negative | 28 | add | **perron** → MA 02-probability, inside the planned Markov chains Note (plan §4). non-negative matrix |
| matrix, non-negative, column-stochastic | 28 | taught | plan §4 new maths: Markov chains (transition matrix; column convention) |
| matrix, non-negative, doubly-stochastic | 28 | add | **consensus** → RO-23 Planning in depth, new Note before Note 271 (Planning with time and many robots). doubly-stochastic weights reach the average |
| matrix, non-negative, indecomposable | 79 | add | **markovconv** → MA 02-probability, extend the planned Markov chains Note (plan §4). indecomposable matrix |
| matrix, non-negative, irreducible | 31 | add | **markovconv** → MA 02-probability, extend the planned Markov chains Note (plan §4). irreducible, primitive, reducible |
| matrix, non-negative, primitive | 31 | add | **markovconv** → MA 02-probability, extend the planned Markov chains Note (plan §4). irreducible, primitive, reducible |
| matrix, non-negative, reducible | 31 | add | **markovconv** → MA 02-probability, extend the planned Markov chains Note (plan §4). irreducible, primitive, reducible |
| matrix, non-negative, row-stochastic | 4, 28 | taught | plan §4 new maths: Markov chains (transition matrix rows sum to 1) |
| matrix, non-negative, row-substochastic | 7, 65 | out-of-scope | substochastic matrices: absorbing chains / opinion dynamics, LNS ch.5 |
| matrix, permutation | 37, 60 | out-of-scope | permutation matrices: used for relabelling nodes in LNS proofs |
| matrix, projection | 98 | taught | MA-052, ML-053 (projection) |
| matrix, rank of | 23 | taught | MA-052 (rank) |
| matrix, rotation | 37 | taught | MA-053; plan §4 Rigid-body transforms (rotation by any angle) |
| matrix, semi-convergent | 24 | out-of-scope | semi-convergent matrix (as 167) |
| matrix, spectral abscissa of | 134 | out-of-scope | spectral abscissa: book-specific name for the largest real part; the eigenvalue test is planned in the stability Note |
| matrix, spectral radius of | 28 | add | **dtstab** → MA 06-calculus, extend the planned Stability of dynamical systems Note (plan §4). spectral radius |
| matrix, spectrum of | 27 | taught | MA-056 (spectrum = set of eigenvalues) |
| matrix, Toeplitz | 58 | out-of-scope | Toeplitz matrices: structure of path-graph examples |
| matrix, tridiagonal Toeplitz | 70 | out-of-scope | Toeplitz matrices: structure of path-graph examples |
| Metropolis–Hastings matrix | 89, 106 | out-of-scope | Metropolis-Hastings weights for averaging in sensor networks: different field |
| modal decomposition | 24 | add | **modes** → MA 06-calculus, inside the planned Matrix exponential Note (plan §4). modal decomposition |
| model |  (see system) | index-noise | cross-reference |
| monotonicity property |  | index-noise | parent heading, no page |
| monotonicity property, algebraic connectivity | 113 | out-of-scope | LNS-specific monotonicity results (proofs) |
| monotonicity property, effective resistence (Rayleigh monotonicity property) | 115 | out-of-scope | LNS-specific monotonicity results (proofs) |
| monotonicity property, Laplacian definiteness | 177 | out-of-scope | LNS-specific monotonicity results (proofs) |
| monotonicity property, solutions of positive systems | 202 | out-of-scope | LNS-specific monotonicity results (proofs) |
| monotonicity property, spectral abscissa of Metzler matrix | 202 | out-of-scope | LNS-specific monotonicity results (proofs) |
| monotonicity property, spectral radius of non-negative matrix | 74 | out-of-scope | LNS-specific monotonicity results (proofs) |
| monotonicity property, spectral radius of non-negative matrix | 64 | out-of-scope | LNS-specific monotonicity results (proofs) |
| negative gradient flow | 261 | taught | ML-056 (gradient descent; LNS's continuous-time form) |
| network system |  | index-noise | parent heading, no page |
| network system, electrical network | 109, 203 | out-of-scope | electrical networks: different field |
| network system, Noy-Meir water flow model | 7 | out-of-scope | water-flow ecology model: different field |
| network system |  | index-noise | parent heading (repeat), no page |
| network system, electrical network | 114, 132, 167 | out-of-scope | electrical networks: different field |
| network system, Krackhardt’s advice network | 80 | out-of-scope | named social-network datasets (examples) |
| network system, Sampson monastery network | 81 | out-of-scope | named social-network datasets (examples) |
| network system, spring network | 109, 114, 125, 248 | out-of-scope | spring networks: LNS mechanics example for Laplacians (electrical/mechanical analogy) |
| network system, Western North American power grid | 249 | out-of-scope | power-grid dataset example |
| Neumann series | 37 | add | **neumann** → MA 06-calculus, extend the planned Geometric series Note (plan §4). Neumann series |
| order parameter | 284 | out-of-scope | Kuramoto order parameter / phase balancing: oscillator theory, different field |
| phase balancing | 287 | out-of-scope | Kuramoto order parameter / phase balancing: oscillator theory, different field |
| pseudoinverse | 42 | taught | MA-060 (pseudo-inverse); plan §4 weighted pseudo-inverse |
| pseudoinverse, incidence matrix | 177 | out-of-scope | pseudoinverses for electrical-network resistance |
| pseudoinverse, Laplacian | 114 | out-of-scope | pseudoinverses for electrical-network resistance |
| push sum algorithm | 99 | out-of-scope | push-sum: distributed averaging on digraphs, research-level |
| set |  | index-noise | parent heading, no page |
| set, bounded, closed, compact | 254 | out-of-scope | real-analysis terms used in proofs |
| set, invariant | 259 | add | **lasalle** → MA 06-calculus, short section in the planned Stability of dynamical systems Note (plan §4). invariant set |
| set, level and sublevel of a function | 254 | taught | MA-062 (level sets as contours) |
| singular value decomposition | 42 | taught | MA-057, MA-058 (SVD) |
| sink |  (see digraph, node, sink) | index-noise | cross-reference |
| source |  (see digraph, node, source) | index-noise | cross-reference |
| spectral abscissa | 134 | out-of-scope | spectral abscissa (as 195) |
| spectral gap | 218 | add | **consensus** → RO-23 Planning in depth, new Note before Note 271 (Planning with time and many robots). spectral gap sets averaging speed |
| spectral radius | 28 | add | **dtstab** → MA 06-calculus, extend the planned Stability of dynamical systems Note (plan §4). spectral radius |
| spectral radius, essential | 211 | add | **consensus** → RO-23 Planning in depth, new Note before Note 271 (Planning with time and many robots). essential spectral radius = rate of averaging |
| subgraph |  (see digraph, subgraph of) | index-noise | cross-reference |
| Sylvester equation | 161 | out-of-scope | Sylvester equation: matrix-equation research tool |
| synchronization |  | out-of-scope | oscillator synchronization (Kuramoto): different field |
| synchronization, frequency | 282 | out-of-scope | oscillator synchronization (Kuramoto): different field |
| synchronization, phase | 282 | out-of-scope | oscillator synchronization (Kuramoto): different field |
| system |  | index-noise | parent heading, no page |
| system, n-bugs | 11 | add | **multirobot** → RO-23, new Note after the consensus Note, before Note 273 (Coverage planning). n-bugs (cyclic pursuit) |
| system, averaging | 5 | add | **consensus** → RO-23 Planning in depth, new Note before Note 271 (Planning with time and many robots). averaging system |
| system, averaging, accelerated | 218 | out-of-scope | accelerated averaging: research-level |
| system, averaging, affine | 39 | out-of-scope | affine averaging (with inputs/stubborn agents): opinion-dynamics research |
| system, averaging, parallel | 98 | out-of-scope | parallel averaging (Jacobi-type solvers): numerical-analysis detail |
| system, averaging, randomized | 238 | out-of-scope | randomized (gossip) averaging: research-level |
| system, averaging, time-varying | 228 | out-of-scope | averaging over switching graphs: research-level (LNS ch.12) |
| system, coupled oscillators | 247 | out-of-scope | coupled oscillators: different field |
| system, double integrators | 148 | add | **consensus** → RO-23 Planning in depth, new Note before Note 271 (Planning with time and many robots). double-integrator consensus |
| system, dynamical flow | 188 | out-of-scope | dynamical flow (compartmental) systems: different field |
| system, dynamical flow, linear | 190 | out-of-scope | dynamical flow (compartmental) systems: different field |
| system, dynamical flow system | 7, 8 | out-of-scope | dynamical flow (compartmental) systems: different field |
| system, French-Harary-DeGroot opinion dynamics | 4 | out-of-scope | opinion-dynamics models: social science, different field |
| system, Friedkin-Johnsen opinion dynamics | 103 | out-of-scope | opinion-dynamics models: social science, different field |
| system, heterogeneous clocks | 117 | out-of-scope | clock networks: distributed timekeeping, different field |
| system, Kuramoto coupled oscillators | 247 | out-of-scope | Kuramoto oscillators: different field |
| system, Laplacian flow | 6, 134 | add | **consensus** → RO-23 Planning in depth, new Note before Note 271 (Planning with time and many robots). Laplacian flow |
| system, Leslie population | 74 | out-of-scope | Leslie population model: biology |
| system, linear |  | taught | plan §4 new maths: State-space models (continuous and discrete time, x' = Ax + Bu); Note 204 |
| system, linear, continuous-time | 134 | taught | plan §4 new maths: State-space models (continuous and discrete time, x' = Ax + Bu); Note 204 |
| system, linear, discrete-time | 24 | taught | plan §4 new maths: State-space models (continuous and discrete time, x' = Ax + Bu); Note 204 |
| system, linear control | 157 | taught | plan §4 new maths: State-space models (continuous and discrete time, x' = Ax + Bu); Note 204 |
| system, logistic | 245 | out-of-scope | logistic and Lotka-Volterra population models: biology |
| system, Lotka-Volterra | 246 | out-of-scope | logistic and Lotka-Volterra population models: biology |
| system, mechanical system, conservative and dissipative | 253 | out-of-scope | worked example of Lyapunov analysis (LNS ch.15); Lyapunov functions themselves are taught (plan §4) |
| system, negative gradient | 253 | taught | ML-056 (gradient descent; continuous-time gradient system) |
| system, positive | 187 | out-of-scope | positive systems: LNS ch.10, research-level |
| Theorem |  | index-noise | parent heading, no page |
| Theorem, Krasovskiı̆-LaSalle Invariance | 259 | add | **lasalle** → MA 06-calculus, short section in the planned Stability of dynamical systems Note (plan §4). Krasovskii-LaSalle invariance principle |
| Theorem, Geršgorin Disks | 29 | out-of-scope | Gersgorin disks: eigenvalue-location proof tool |
| Theorem, Jordan Normal Form | 25 | add | **eigmult** → MA 05-linear-algebra, extend MA-056 (eigenvectors and eigenvalues). Jordan normal form (named only) |
| Theorem, Lyapunov Stability Criteria | 257 | taught | plan §4 new maths: Lyapunov functions / Stability of dynamical systems |
| Theorem, Metzler Hurwitz | 186, 194 | out-of-scope | Metzler-Hurwitz theorem: positive-systems theory |
| Theorem, Negative gradient flow | 262 | out-of-scope | proof result on gradient flows |
| Theorem, Perron–Frobenius | 32 | add | **perron** → MA 02-probability, inside the planned Markov chains Note (plan §4). Perron-Frobenius theorem (statement) |
| Theorem, Perron–Frobenius for Metzler matrices | 185 | out-of-scope | Perron-Frobenius for Metzler matrices: positive-systems theory |
| Theorem, Strongly connected and aperiodic digraphs and primitive adjacency matrices | 62 | out-of-scope | graph/matrix theorems used only in LNS proofs |
| Theorem, Strongly connected digraphs and irreducible adjacency matrices | 60 | out-of-scope | graph/matrix theorems used only in LNS proofs |
| tree | 47 | taught | Note 110 (RRT), Note 48 (MCTS): trees |
| tree, directed | 47 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. directed (rooted) tree |
| tree, directed, spanning |  (see tree, spanning) | index-noise | cross-reference |
| tree, root of | 47 | taught | Note 48, Note 110 (root of a search tree) |
| tree, rooted |  (see tree, directed) | index-noise | cross-reference |
| tree, spanning | 47 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. spanning tree |
| weighted digraph | 50 | taught | Note 104 (Dijkstra on a weighted directed graph) |
| weighted digraph, adjacency matrix of | 57 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. adjacency matrix of a weighted digraph |
| weighted digraph, binary adjacency matrix of | 57 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. adjacency matrix of a weighted digraph |
| weighted digraph, in-degree matrix of | 57 | add | **graphlap** → MA 05-linear-algebra (new Note after MA-056 eigenvectors), first used by the consensus Note in RO-23. degree matrix |
| weighted digraph, Laplacian matrix of | 107 | add | **graphlap** → MA 05-linear-algebra (new Note after MA-056 eigenvectors), first used by the consensus Note in RO-23. Laplacian of a weighted digraph |
| weighted digraph, node |  | index-noise | parent heading, no page |
| weighted digraph, node, in-degree | 52 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. in/out-degree |
| weighted digraph, node, out-degree | 52 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. in/out-degree |
| weighted digraph, out-degree matrix of | 57 | add | **graphlap** → MA 05-linear-algebra (new Note after MA-056 eigenvectors), first used by the consensus Note in RO-23. out-degree matrix |
| weighted digraph, undirected | 50 | add | **graphs** → RO-05, extend Note 103 (Graphs and uninformed search) or a new MA 05-linear-algebra Note just before the graph Laplacian. undirected weighted graph |
| weighted digraph, weight-balanced | 52 | add | **consensus** → RO-23 Planning in depth, new Note before Note 271 (Planning with time and many robots). weight-balanced digraphs give average consensus |

## Deisenroth, Faisal & Ong, Mathematics for Machine Learning (2020; PDF ©2024)

Index pages parsed: 460 terms. Pages are the book's own page labels.

| Term | Pages | Verdict | Where / why |
|---|---|---|---|
| 1-of-K representation | 364 | taught | ML-026 (one-hot encoding) |
| ℓ 1 norm | 71 | taught | MA-049 (L1 and L2 norms) |
| ℓ 2 norm | 72 | taught | MA-049 (L1 and L2 norms) |
| abduction | 258 | out-of-scope | philosophy-of-science term (MML p.258) |
| Abel-Ruffini theorem | 334 | out-of-scope | theorem on polynomial roots (history/proof) |
| Abelian group | 36 | out-of-scope | group theory: plan §7 drops PA 4.6 on purpose (SE(2)/SE(3) taught as matrices) |
| absolutely homogeneous | 71 | out-of-scope | norm axiom used in proofs; MA-049 teaches norms by example |
| activation function | 315 | taught | DL-004, DL-027 (activation functions) |
| affine mapping | 63 | taught | MA-053 (affine transformation, G-178); plan §4 Rigid-body transforms |
| affine subspace | 61 | add | **paramline** → MA 05-linear-algebra, extend MA-051 (equation of a hyperplane). affine subspace |
| Akaike information criterion | 288 | out-of-scope | information-criterion model selection; no plan Note uses it |
| algebra | 17 | index-noise | generic word; p.17 is the linear-algebra chapter opening |
| algebraic multiplicity | 106 | add | **eigmult** → MA 05-linear-algebra, extend MA-056 (eigenvectors and eigenvalues). algebraic multiplicity |
| analytic | 143 | taught | MA-061 (analytic function, G-197) |
| ancestral sampling | 340, 364 | out-of-scope | sampling a directed graphical model (MML §8.4); the planned sampling-recipes Note (plan §4) covers drawing samples |
| angle | 76 | taught | MA-050 (angle via cosine similarity) |
| associativity | 24, 26, 36 | taught | MA-054 (associativity) |
| attribute | 253 | taught | ML-002 (feature = attribute) |
| augmented matrix | 29 | add | **linsolve** → MA 05-linear-algebra, new Note after MA-053 (before MA-058 four subspaces). augmented matrix |
| auto-encoder | 343 | taught | plan §4 DL new chapter "Generative models" (VAE); DL-003 |
| automatic differentiation | 161 | taught | MA-063 (automatic differentiation, G-232) |
| automorphism | 49 | out-of-scope | abstract algebra (map from a space to itself), proof vocabulary |
| backpropagation | 159 | taught | DL-015 to DL-017 (backpropagation) |
| basic variable | 30 | add | **linsolve** → MA 05-linear-algebra, new Note after MA-053 (before MA-058 four subspaces). basic variable |
| basis | 44 | taught | MA-052 (basis) |
| basis vector | 45 | taught | MA-052 (basis) |
| Bayes factor | 287 | taught | MA-019 (Bayes factor, G-2215) |
| Bayes’ law | 185 | taught | MA-018 (Bayes' theorem) |
| Bayes’ rule | 185 | taught | MA-018 (Bayes' theorem) |
| Bayes’ theorem | 185 | taught | MA-018 (Bayes' theorem) |
| Bayesian GP-LVM | 347 | out-of-scope | Bayesian GP-LVM: ML research method; no plan Note uses it |
| Bayesian inference | 274 | taught | MA-072 (prior and posterior) |
| Bayesian information criterion | 288 | out-of-scope | information-criterion model selection; no plan Note uses it |
| Bayesian linear regression | 303 | out-of-scope | ML-theory route to predictive uncertainty (MML ch.9); the planned GP Note (plan §4) gives mean and uncertainty directly |
| Bayesian model selection | 286 | out-of-scope | Bayesian model comparison; no plan Note uses it |
| Bayesian network | 278, 283 | taught | Note 77 (hidden Markov model / dynamic Bayes network) |
| Bayesian PCA | 346 | out-of-scope | Bayesian PCA: ML method not used by any plan Note |
| Bernoulli distribution | 205 | taught | MA-021, MA-031 (Bernoulli) |
| Beta distribution | 206 | out-of-scope | Beta distribution: used in MML for conjugate priors; no plan Note uses it |
| bilinear mapping | 72 | out-of-scope | abstract definition of inner products (proof vocabulary) |
| bijective | 48 | out-of-scope | function-theory vocabulary used in MML proofs |
| binary classification | 370 | taught | ML-003, ML-069 (binary classification) |
| Binomial distribution | 206 | taught | MA-031 (binomial) |
| blind-source separation | 346 | out-of-scope | blind-source separation (ICA): ML method not used by any plan Note |
| Borel σ-algebra | 180 | out-of-scope | measure theory, beyond course level |
| canonical basis | 45 | taught | MA-052 (standard basis) |
| canonical feature map | 389 | out-of-scope | kernel-method notation |
| canonical link function | 315 | out-of-scope | generalized-linear-model framework; logistic regression itself is ML-069 |
| categorical variable | 180 | taught | MA-004, ML-025 (categorical variables) |
| Cauchy-Schwarz inequality | 75 | out-of-scope | inequality used as a proof tool |
| change-of-variable technique | 219 | taught | MA-063 (Jacobian determinant / change of variables) |
| characteristic polynomial | 104 | taught | MA-056 (characteristic polynomial) |
| Cholesky decomposition | 114 | taught | plan §4 new maths: Cholesky factor |
| Cholesky factor | 114 | taught | plan §4 new maths: Cholesky factor |
| Cholesky factorization | 114 | taught | plan §4 new maths: Cholesky factor |
| class | 370 | taught | ML-003 (classification, classes) |
| classification | 315 | taught | ML-003 (classification, classes) |
| closure | 36 | out-of-scope | group axiom (abstract algebra) |
| code | 343 | taught | plan §4 DL new chapter (VAE latent code) |
| codirected | 105 | out-of-scope | MML term for vectors pointing the same way (book-specific) |
| codomain | 58, 139 | taught | MA-061 (codomain) |
| collinear | 105 | taught | MA-052 (linearly dependent vectors lie on one line) |
| column | 22 | taught | MA-048 (rows and columns) |
| column space | 59 | taught | MA-053 (column space) |
| column vector | 22, 38 | taught | MA-048 (column vector) |
| completing the squares | 307 | taught | plan §4 new maths: Product of two Gaussians (completing the square) |
| concave function | 236 | taught | MA-067 (concave function) |
| condition number | 230 | taught | MA-058 (condition number) |
| conditional probability | 179 | taught | MA-015 (conditional probability) |
| conditionally independent | 195 | taught | MA-016; plan §5 recap "Independence and conditional independence" |
| conjugate | 208 | out-of-scope | conjugate priors: Bayesian statistics; no plan Note uses them |
| conjugate prior | 208 | out-of-scope | conjugate priors: Bayesian statistics; no plan Note uses them |
| convex conjugate | 242 | out-of-scope | convex conjugate: convex-analysis tool beyond course level |
| convex function | 236 | taught | MA-065, ML-056 (convex function) |
| convex hull | 386 | taught | plan §4 new maths: Convex hull; DL-076 (glossary) |
| convex optimization problem | 236, 239 | taught | MA-067 (convex optimisation problem, convex set) |
| convex set | 236 | taught | MA-067 (convex optimisation problem, convex set) |
| coordinate | 50 | taught | MA-048 (coordinates) |
| coordinate representation | 50 | taught | MA-056 (coordinates in a basis, change-of-basis matrix) |
| coordinate vector | 50 | taught | MA-056 (coordinates in a basis, change-of-basis matrix) |
| correlation | 191 | taught | MA-009 (correlation, covariance) |
| covariance | 190 | taught | MA-009 (correlation, covariance) |
| covariance matrix | 190, 198 | taught | ML-047 (covariance matrix) |
| covariate | 253 | taught | DL-031 (covariate) |
| CP decomposition | 136 | out-of-scope | tensor (CP) decomposition: ML research method |
| cross-covariance | 191 | add | **gausscond** → MA 08-likelihood, in the planned "Linear transforms of a Gaussian" Note (plan §4). cross-covariance |
| cross-validation | 258, 263 | taught | ML-028 (cross-validation) |
| cumulative distribution function | 178, 181 | taught | MA-021 (CDF) |
| d-separation | 281 | out-of-scope | graphical-model inference theory; no plan Note uses it |
| data covariance matrix | 318 | taught | ML-047 (covariance matrix of the data) |
| data point | 253 | taught | ML-002 (data points) |
| data-fit term | 302 | taught | ML-062 (loss + penalty) |
| decoder | 343 | taught | DL-068 (encoder-decoder); plan §4 VAE |
| deep auto-encoder | 347 | taught | plan §4 DL new chapter (VAE) |
| defective | 111 | add | **eigmult** → MA 05-linear-algebra, extend MA-056 (eigenvectors and eigenvalues). defective matrix |
| denominator layout | 151 | taught | MA-063 (layout conventions) |
| derivative | 141 | taught | MA-061 (derivative) |
| design matrix | 294, 296 | taught | ML-053 (design matrix) |
| determinant | 99 | taught | MA-056 (determinant) |
| diagonal matrix | 115 | taught | MA-053 (diagonal matrix) |
| diagonalizable | 116 | add | **eigmult** → MA 05-linear-algebra, extend MA-056 (eigenvectors and eigenvalues). diagonalizable |
| diagonalization | 116 | taught | MA-056 (P^-1 A P = D) |
| difference quotient | 141 | taught | MA-061 (difference quotient) |
| dimension | 45 | taught | MA-048 (dimension) |
| dimensionality reduction | 317 | taught | ML-045 (dimensionality reduction) |
| directed graphical model | 278, 283 | taught | Note 77 (dynamic Bayes network) |
| direction | 61 | taught | MA-049 (vector direction) |
| direction space | 61 | add | **paramline** → MA 05-linear-algebra, extend MA-051 (equation of a hyperplane). direction space of an affine subspace |
| distance | 75 | taught | MA-049 (distance) |
| distribution | 177 | taught | MA-020 (distributions) |
| distributivity | 24, 26 | taught | MA-050 (distributive law, G-627) |
| domain | 58, 139 | taught | MA-061 (domain) |
| dot product | 72 | taught | MA-050 (dot product) |
| dual SVM | 385 | taught | MA-066 §7.2 (the SVM dual) |
| Eckart-Young theorem | 131, 334 | taught | MA-059 (Eckart-Young) |
| eigendecomposition | 116 | taught | MA-056 (eigendecomposition) |
| eigenspace | 106 | add | **eigmult** → MA 05-linear-algebra, extend MA-056 (eigenvectors and eigenvalues). eigenspace (its dimension is the geometric multiplicity) |
| eigenspectrum | 106 | taught | MA-056 (set of eigenvalues) |
| eigenvalue | 105 | taught | MA-056, ML-047 (eigenvalues, eigenvectors) |
| eigenvalue equation | 105 | taught | MA-056, ML-047 (eigenvalues, eigenvectors) |
| eigenvector | 105 | taught | MA-056, ML-047 (eigenvalues, eigenvectors) |
| elementary transformations | 28 | add | **linsolve** → MA 05-linear-algebra, new Note after MA-053 (before MA-058 four subspaces). elementary row operations |
| EM algorithm | 360 | taught | MA-074 (EM) |
| embarrassingly parallel | 264 | out-of-scope | computing term (parallel jobs), not maths |
| empirical covariance | 192 | taught | MA-009 (sample covariance) |
| empirical mean | 192 | taught | MA-005 (sample mean) |
| empirical risk | 260 | out-of-scope | statistical-learning-theory name for average training loss; ML-050 teaches minimising it |
| empirical risk minimization | 257, 260 | out-of-scope | statistical-learning-theory name for average training loss; ML-050 teaches minimising it |
| encoder | 343 | taught | DL-068 (encoder) |
| endomorphism | 49 | out-of-scope | abstract algebra (proof vocabulary) |
| epigraph | 236 | taught | MA-067 (epigraph) |
| equivalent | 56 | out-of-scope | MML term for matrices related by basis changes on both sides (book-specific) |
| error function | 294 | taught | ML-050 (loss / error function, G-706) |
| error term | 382 | taught | ML-050 (error term in a loss) |
| Euclidean distance | 72, 75 | taught | MA-049 (Euclidean distance and norm) |
| Euclidean norm | 72 | taught | MA-049 (Euclidean distance and norm) |
| Euclidean vector space | 73 | taught | MA-048 (vectors in R^n) |
| event space | 175 | taught | MA-010 (events) |
| evidence | 186, 285, 306 | taught | MA-018 (evidence) |
| example | 253 | taught | ML-003 (examples = data points) |
| expected risk | 261 | out-of-scope | statistical-learning-theory term (as empirical risk) |
| expected value | 187 | taught | MA-012 (expected value) |
| exponential family | 205, 211 | out-of-scope | exponential family: statistical theory; no plan Note uses it |
| extended Kalman filter | 170 | taught | Note 81 (extended Kalman filter) |
| factor analysis | 346 | out-of-scope | factor analysis: ML method not used by any plan Note |
| factor graph | 283 | taught | Note 263 (factor graphs) |
| feature | 253 | taught | ML-002, ML-089 (features, feature map) |
| feature map | 254 | taught | ML-002, ML-089 (features, feature map) |
| feature matrix | 296 | taught | ML-053 (design / feature matrix) |
| feature vector | 295 | taught | MA-048 (feature vector) |
| Fisher discriminant analysis | 136 | out-of-scope | Fisher discriminant / Fisher-Neyman: statistical theory not used by any plan Note |
| Fisher-Neyman theorem | 210 | out-of-scope | Fisher discriminant / Fisher-Neyman: statistical theory not used by any plan Note |
| forward mode | 161 | out-of-scope | forward-mode autodiff: alternative mode; backprop (DL-015) is reverse mode |
| free variable | 30 | add | **linsolve** → MA 05-linear-algebra, new Note after MA-053 (before MA-058 four subspaces). free variable |
| full rank | 47 | taught | MA-058 (rank, full rank) |
| full SVD | 128 | taught | MA-057 (full SVD) |
| fundamental theorem of linear mappings | 60 | taught | MA-058 (dimensions of the four subspaces: rank r and null space n - r) |
| Gaussian elimination | 31 | add | **linsolve** → MA 05-linear-algebra, new Note after MA-053 (before MA-058 four subspaces). Gaussian elimination |
| Gaussian mixture model | 349 | taught | MA-073 (GMM) |
| Gaussian process | 316 | taught | plan §4 new ML Note: Gaussian processes |
| Gaussian process latent-variable model | 347 | out-of-scope | GP-LVM: ML research method |
| general linear group | 37 | out-of-scope | group theory (plan §7 drops PA 4.6) |
| general solution | 28, 30 | add | **linsolve** → MA 05-linear-algebra, new Note after MA-053 (before MA-058 four subspaces). general solution |
| generalized linear model | 272, 315 | out-of-scope | generalized-linear-model framework (statistics) |
| generating set | 44 | taught | MA-052 (spanning set) |
| generative process | 272, 286 | taught | MA-073 (generative process) |
| generator | 344 | taught | plan §4 DL new chapter (VAE decoder / GAN generator) |
| geometric multiplicity | 108 | add | **eigmult** → MA 05-linear-algebra, extend MA-056 (eigenvectors and eigenvalues). geometric multiplicity |
| Givens rotation | 94 | out-of-scope | Givens rotations: numerical-linear-algebra algorithm (QR) |
| global minimum | 225 | taught | ML-056 (global minimum) |
| GP-LVM | 347 | out-of-scope | GP-LVM: ML research method |
| gradient | 146 | taught | MA-062 (gradient) |
| Gram matrix | 389 | taught | MA-058 (A^T A, G-22) |
| Gram-Schmidt orthogonalization | 89 | out-of-scope | Gram-Schmidt: numerical algorithm; orthonormal bases come from the SVD (MA-057) in these Notes |
| graphical model | 278 | taught | Note 77 (dynamic Bayes network) |
| group | 36 | out-of-scope | group theory (plan §7 drops PA 4.6) |
| Hadamard product | 23 | taught | DL-048 (element-wise product) |
| hard margin SVM | 377 | taught | ML-087 (hard-margin SVM) |
| Hessian | 164 | taught | MA-064 (Hessian) |
| Hessian eigenmaps | 136 | out-of-scope | Hessian eigenmaps: ML embedding method named only (MML p.136) |
| Hessian matrix | 165 | taught | MA-064 (Hessian matrix) |
| hinge loss | 381 | taught | ML-088 (hinge loss) |
| histogram | 369 | taught | ML-019 (histogram) |
| hyperparameter | 258 | taught | ML-028 (hyperparameter) |
| hyperplane | 61, 62 | taught | MA-051 (hyperplane) |
| hyperprior | 281 | out-of-scope | hierarchical Bayesian modelling; no plan Note uses it |
| i.i.d. | 195 | taught | MA-033 (i.i.d.) |
| ICA | 346 | out-of-scope | ICA: ML method not used by any plan Note |
| identity automorphism | 49 | out-of-scope | abstract algebra (proof vocabulary) |
| identity mapping | 49 | taught | MA-053 (identity transformation) |
| identity matrix | 23 | taught | ML-047 (identity matrix) |
| image | 58, 139 | taught | MA-053 (image = column space) |
| independent and identically distributed | 195, 260, 266 | taught | MA-033 (i.i.d.) |
| independent component analysis | 346 | out-of-scope | ICA: ML method not used by any plan Note |
| inference network | 344 | taught | plan §4 DL new chapter (VAE encoder) |
| injective | 48 | out-of-scope | function-theory vocabulary used in MML proofs |
| inner product | 73 | taught | MA-050 (dot product as the standard inner product) |
| inner product space | 73 | out-of-scope | abstract inner-product spaces; the weighted case x^T A y appears in the planned Mahalanobis Note (plan §4) |
| intermediate variables | 162 | taught | MA-063 (chain rule with intermediate variables) |
| inverse | 24 | taught | ML-053 (inverse matrix) |
| inverse element | 36 | out-of-scope | group axiom (abstract algebra) |
| invertible | 24 | taught | ML-053 (invertible matrix) |
| Isomap | 136 | out-of-scope | Isomap: ML embedding method named only (MML p.136) |
| isomorphism | 49 | out-of-scope | abstract algebra (proof vocabulary) |
| Jacobian | 146, 150 | taught | MA-063 (Jacobian, Jacobian determinant) |
| Jacobian determinant | 152 | taught | MA-063 (Jacobian, Jacobian determinant) |
| Jeffreys-Lindley paradox | 287 | out-of-scope | Bayesian-statistics paradox |
| Jensen’s inequality | 239 | taught | MA-067 (Jensen's inequality) |
| joint probability | 178 | taught | MA-014 (joint probability) |
| Karhunen-Loève transform | 318 | taught | ML-046 (Karhunen-Loeve transform = PCA) |
| kernel | 33, 47, 58, 254, 388 | taught | MA-058 (kernel = null space) |
| kernel density estimation | 369 | taught | MA-023 (KDE) |
| kernel matrix | 389 | out-of-scope | kernel-method detail (MML §12.4); no plan Note uses it |
| kernel PCA | 347 | out-of-scope | kernel PCA: ML method not used by any plan Note |
| kernel trick | 316, 347, 389 | taught | ML-089 (kernel trick) |
| label | 253 | taught | ML-003 (label) |
| Lagrange multiplier | 234 | taught | MA-066 (Lagrange multipliers) |
| Lagrangian | 234 | taught | MA-066 (Lagrange multipliers) |
| Lagrangian dual problem | 234 | taught | MA-066 (primal and dual problems) |
| Laplace approximation | 170 | taught | MA-064 (Laplace approximation, G-1043) |
| Laplace expansion | 102 | out-of-scope | cofactor expansion: hand method for determinants; MA-056 computes small determinants directly |
| Laplacian eigenmaps | 136 | out-of-scope | ML embedding method named only (MML p.136); the graph Laplacian itself is an add (graphlap) |
| LASSO | 303, 316 | taught | ML-066 (lasso) |
| latent variable | 275 | taught | MA-073 (latent variable) |
| law | 177, 181 | out-of-scope | probability-theory word for a distribution (notation) |
| law of total variance | 203 | out-of-scope | identity not used by any plan Note |
| leading coefficient | 30 | add | **linsolve** → MA 05-linear-algebra, new Note after MA-053 (before MA-058 four subspaces). leading coefficient (pivot) in row-echelon form |
| least-squares loss | 154 | taught | MA-063 (least-squares loss) |
| least-squares problem | 261 | taught | ML-053 (least squares, normal equation) |
| least-squares solution | 88 | taught | ML-053 (least squares, normal equation) |
| left-singular vectors | 119 | taught | MA-057 (left singular vectors) |
| Legendre transform | 242 | out-of-scope | Legendre transform: convex-analysis tool beyond course level |
| Legendre-Fenchel transform | 242 | out-of-scope | Legendre transform: convex-analysis tool beyond course level |
| length | 71 | taught | MA-049 (length = norm) |
| likelihood | 185, 265, 269, 291 | taught | MA-069 (likelihood) |
| line | 61, 82 | taught | MA-051 (lines) |
| linear combination | 40 | taught | MA-052 (linear combination) |
| linear manifold | 61 | add | **paramline** → MA 05-linear-algebra, extend MA-051 (equation of a hyperplane). linear manifold (affine subspace) |
| linear mapping | 48 | taught | MA-053 (linear map) |
| linear program | 239 | taught | MA-068 (linear program) |
| linear subspace | 39 | taught | MA-052 (subspace = span) |
| linear transformation | 48 | taught | MA-053 (linear transformation) |
| linearly dependent | 40 | taught | MA-052 (linear dependence) |
| linearly independent | 40 | taught | MA-052 (linear dependence) |
| link function | 272 | out-of-scope | generalized-linear-model framework (statistics) |
| loading | 322 | taught | ML-047 (loadings) |
| local minimum | 225 | taught | ML-056 (local minimum) |
| log-partition function | 211 | out-of-scope | exponential-family theory |
| logistic regression | 315 | taught | ML-069 (logistic regression) |
| logistic sigmoid | 315 | taught | ML-071 (sigmoid) |
| loss function | 260, 381 | taught | ML-050 (loss function) |
| loss term | 382 | taught | DL-026 (loss + penalty terms) |
| lower-triangular matrix | 101 | taught | plan §4 new maths: Cholesky factor (lower-triangular factor) |
| Maclaurin series | 143 | taught | MA-061 (Maclaurin series) |
| Manhattan norm | 71 | taught | MA-049 (Manhattan / L1 norm) |
| MAP | 300 | taught | MA-072 (MAP estimation) |
| MAP estimation | 269 | taught | MA-072 (MAP estimation) |
| margin | 374 | taught | ML-086 (margin) |
| marginal | 190 | taught | MA-014 (marginal) |
| marginal likelihood | 186, 286, 306 | taught | MA-018 (evidence = marginal likelihood) |
| marginal probability | 179 | taught | MA-014 (marginal probability; sum rule) |
| marginalization property | 184 | taught | MA-014 (marginal probability; sum rule) |
| Markov random field | 283 | out-of-scope | Markov random fields: graphical-model theory; no plan Note uses them |
| matrix | 22 | taught | MA-053 (matrices) |
| matrix factorization | 98 | taught | MA-047 (matrix factorisation) |
| maximum a posteriori | 300 | taught | MA-072 (MAP) |
| maximum a posteriori estimation | 269 | taught | MA-072 (MAP) |
| maximum likelihood | 257 | taught | MA-070 (MLE) |
| maximum likelihood estimate | 296 | taught | MA-070 (MLE) |
| maximum likelihood estimation | 265, 293 | taught | MA-070 (MLE) |
| mean | 187 | taught | MA-005 (mean) |
| mean function | 309 | taught | plan §4 new ML Note: Gaussian processes |
| mean vector | 198 | taught | MA-073 (multivariate normal mean vector) |
| measure | 180 | out-of-scope | measure theory, beyond course level |
| median | 188 | taught | MA-005 (median) |
| metric | 76 | taught | Note 108 (metric: rules a distance must follow) |
| minimal | 44 | taught | MA-052 (basis = minimal spanning set) |
| minimax inequality | 234 | taught | MA-066 (minimax inequality) |
| misfit term | 302 | taught | ML-062 (data-fit + penalty) |
| mixture model | 349 | taught | MA-073 (mixture models) |
| mixture weight | 349 | taught | MA-073 (mixture models) |
| mode | 188 | taught | MA-005 (mode) |
| model | 251 | taught | ML-001 (model) |
| model evidence | 286 | out-of-scope | Bayesian model comparison; no plan Note uses it |
| model selection | 258 | taught | ML-009 (model selection) |
| Moore-Penrose pseudo-inverse | 35 | taught | MA-060 (pseudo-inverse) |
| multidimensional scaling | 136 | out-of-scope | multidimensional scaling: ML method named only (MML p.136) |
| multiplication by scalars | 37 | taught | MA-049 (scalar multiplication) |
| multivariate | 178 | taught | MA-073 (multivariate normal) |
| multivariate Gaussian distribution | 198 | taught | MA-073 (multivariate normal) |
| multivariate Taylor series | 166 | taught | MA-064 (multivariate Taylor) |
| natural parameters | 212 | out-of-scope | exponential-family theory |
| negative log-likelihood | 265 | taught | MA-070 (negative log-likelihood) |
| nested cross-validation | 258, 284 | taught | ML-106 (nested cross-validation) |
| neutral element | 36 | out-of-scope | group axiom (abstract algebra) |
| noninvertible | 24 | taught | MA-053 (determinant 0 = not invertible) |
| nonsingular | 24 | taught | ML-053 (invertible matrix) |
| norm | 71 | taught | MA-049 (norm) |
| normal distribution | 197 | taught | MA-024 (normal distribution) |
| normal equation | 86 | taught | ML-053 (normal equation) |
| normal vector | 80 | taught | MA-051 (normal vector) |
| null space | 33, 47, 58 | taught | MA-058 (null space) |
| numerator layout | 150 | taught | MA-063 (numerator layout) |
| Occam’s razor | 285 | out-of-scope | philosophy-of-science principle |
| ONB | 79 | taught | MA-057 (orthonormal basis) |
| one-hot encoding | 364 | taught | ML-026 (one-hot) |
| ordered basis | 50 | taught | MA-052 (basis) |
| orthogonal | 77 | taught | MA-050 (orthogonal) |
| orthogonal basis | 79 | taught | MA-057 (orthogonal / orthonormal bases) |
| orthogonal complement | 79 | taught | MA-058 (four fundamental subspaces: row space and null space are orthogonal complements) |
| orthogonal matrix | 78 | taught | MA-057 (orthogonal matrix, orthonormal) |
| orthonormal | 77 | taught | MA-057 (orthogonal matrix, orthonormal) |
| orthonormal basis | 79 | taught | MA-057 (orthogonal matrix, orthonormal) |
| outer product | 38 | taught | MA-064 (outer product) |
| overfitting | 262, 271, 299 | taught | ML-007 (overfitting) |
| PageRank | 114 | taught | MA-056 (power iteration, PageRank example) |
| parameters | 61 | taught | MA-020 (parameters) |
| parametric equation | 61 | add | **paramline** → MA 05-linear-algebra, extend MA-051 (equation of a hyperplane). parametric equation of a line/plane |
| partial derivative | 146 | taught | MA-062, ML-050 (partial derivative) |
| particular solution | 27, 30 | add | **linsolve** → MA 05-linear-algebra, new Note after MA-053 (before MA-058 four subspaces). particular solution |
| PCA | 317 | taught | ML-046 (PCA) |
| pdf | 181 | taught | MA-022 (PDF) |
| penalty term | 263 | taught | DL-026 (penalty term) |
| pivot | 30 | add | **linsolve** → MA 05-linear-algebra, new Note after MA-053 (before MA-058 four subspaces). pivot |
| plane | 62 | taught | MA-051, ML-052 (plane) |
| plate | 281 | index-noise | graphical-model notation (plates) |
| population mean and covariance | 191 | taught | MA-009 (population covariance) |
| positive definite | 71, 73, 74, 76 | taught | MA-068 (positive definite matrix) |
| posterior | 185, 269 | taught | MA-018 (posterior) |
| posterior odds | 287 | taught | MA-019 (odds form with the Bayes factor) |
| power iteration | 334 | taught | MA-056 (power iteration) |
| power series representation | 145 | taught | MA-061 (Taylor/Maclaurin series) |
| PPCA | 340 | out-of-scope | probabilistic PCA: ML method not used by any plan Note |
| preconditioner | 230 | out-of-scope | optimisation numerics; no plan Note uses it |
| predictor | 12, 255 | taught | ML-001 (model as predictor) |
| primal problem | 234 | taught | MA-066 (primal problem) |
| principal component | 322 | taught | ML-046 (principal components, subspace) |
| principal component analysis | 136, 317 | taught | ML-046 (principal components, subspace) |
| principal subspace | 327 | taught | ML-046 (principal components, subspace) |
| prior | 185, 269 | taught | MA-018 (prior) |
| prior odds | 287 | taught | MA-019 (odds form) |
| probabilistic inverse | 186 | out-of-scope | MML name for Bayes' theorem as an inverse (notation) |
| probabilistic PCA | 340 | out-of-scope | probabilistic PCA: ML method not used by any plan Note |
| probabilistic programming | 278 | out-of-scope | software paradigm (probabilistic programming) |
| probability | 175 | taught | MA-011 (probability) |
| probability density function | 181 | taught | MA-022 (PDF) |
| probability distribution | 172 | taught | MA-020 (distributions) |
| probability integral transform | 217 | taught | plan §4 new maths: Drawing samples from distributions (inverse-CDF sampling) |
| probability mass function | 178 | taught | MA-021 (PMF) |
| product rule | 184 | taught | MA-015 (p(x,y) = p(y/x) p(x)) |
| projection | 82 | taught | MA-055, ML-046 (projection) |
| projection error | 88 | taught | ML-053 (residual of the least-squares projection) |
| projection matrix | 82 | taught | MA-052 (projection matrix) |
| pseudo-inverse | 86 | taught | MA-060 (pseudo-inverse) |
| random variable | 172, 175 | taught | MA-020 (random variable) |
| range | 58 | taught | MA-053 (range = column space) |
| rank | 47 | taught | MA-058 (rank) |
| rank deficient | 47 | taught | MA-058 (rank) |
| rank-k approximation | 130 | taught | MA-059 (rank-k approximation) |
| rank-nullity theorem | 60 | taught | MA-058 (dimensions r and n - r) |
| raw-score formula for variance | 193 | taught | MA-012 (Var = E[X^2] - E[X]^2) |
| recognition network | 344 | taught | plan §4 DL new chapter (VAE encoder) |
| reconstruction error | 88, 327 | taught | MA-059 (low-rank reconstruction error) |
| reduced hull | 388 | out-of-scope | SVM geometry detail (MML §12.3) |
| reduced row-echelon form | 31 | add | **linsolve** → MA 05-linear-algebra, new Note after MA-053 (before MA-058 four subspaces). reduced row-echelon form |
| reduced SVD | 129 | taught | MA-057 (reduced SVD) |
| REF | 30 | add | **linsolve** → MA 05-linear-algebra, new Note after MA-053 (before MA-058 four subspaces). row-echelon form |
| regression | 289 | taught | ML-049 (regression) |
| regular | 24 | taught | ML-053 (invertible = regular) |
| regularization | 262, 302, 382 | taught | ML-062, DL-026 (regularisation) |
| regularization parameter | 263, 302, 380 | taught | ML-062, DL-026 (regularisation) |
| regularized least squares | 302 | taught | ML-062, DL-026 (regularisation) |
| regularizer | 263, 302, 380, 382 | taught | ML-062, DL-026 (regularisation) |
| representer theorem | 384 | out-of-scope | representer theorem: kernel-method theory |
| responsibility | 352 | taught | MA-073 (responsibilities) |
| reverse mode | 161 | taught | DL-015, DL-019 (backprop = reverse mode) |
| right-singular vectors | 119 | taught | MA-057 (right singular vectors) |
| RMSE | 298 | taught | ML-051 (RMSE) |
| root mean square error | 298 | taught | ML-051 (RMSE) |
| rotation | 91 | taught | MA-053; plan §4 Rigid-body transforms |
| rotation matrix | 92 | taught | MA-053; plan §4 Rigid-body transforms and 3D rotations |
| row | 22 | taught | MA-048 (rows, row vectors) |
| row vector | 22, 38 | taught | MA-048 (rows, row vectors) |
| row-echelon form | 30 | add | **linsolve** → MA 05-linear-algebra, new Note after MA-053 (before MA-058 four subspaces). row-echelon form |
| sample mean | 192 | taught | MA-005 (sample mean) |
| sample space | 175 | taught | MA-010 (sample space) |
| scalar | 37 | taught | MA-049 (scalars) |
| scalar product | 72 | taught | MA-050 (scalar product) |
| sigmoid | 213 | taught | ML-071 (sigmoid) |
| similar | 56 | taught | MA-056 (P^-1 A P: similar matrices) |
| singular | 24 | taught | MA-053 (singular matrix squashes space) |
| singular value decomposition | 119 | taught | MA-057 (SVD) |
| singular value equation | 124 | taught | MA-057 (SVD) |
| singular value matrix | 119 | taught | MA-057 (SVD) |
| singular values | 119 | taught | MA-057 (SVD) |
| slack variable | 379 | taught | ML-088 (soft margin, slack) |
| soft margin SVM | 379, 380 | taught | ML-088 (soft margin, slack) |
| solution | 20 | add | **linsolve** → MA 05-linear-algebra, new Note after MA-053 (before MA-058 four subspaces). solution of a linear system |
| span | 44 | taught | MA-052 (span) |
| special solution | 27 | add | **linsolve** → MA 05-linear-algebra, new Note after MA-053 (before MA-058 four subspaces). special solution |
| spectral clustering | 136 | out-of-scope | spectral clustering: ML method not used by any plan Note; the graph Laplacian itself is an add (graphlap) |
| spectral norm | 131 | taught | MA-059 (spectral norm) |
| spectral theorem | 111 | taught | MA-056 (spectral theorem) |
| spectrum | 106 | taught | MA-056 (set of eigenvalues) |
| square matrix | 25 | taught | MA-053 (square matrices) |
| standard basis | 45 | taught | MA-052 (standard basis) |
| standard deviation | 190 | taught | MA-006, MA-012 (standard deviation) |
| standard normal distribution | 198 | taught | MA-025 (standard normal) |
| standardization | 336 | taught | ML-023 (standardization) |
| statistical independence | 194 | taught | MA-016 (independence) |
| statistical learning theory | 265 | out-of-scope | statistical learning theory: beyond course level |
| stochastic gradient descent | 231 | taught | ML-058 (SGD) |
| strong duality | 236 | taught | MA-066 (strong duality) |
| sufficient statistics | 210 | out-of-scope | sufficient statistics: statistical theory; no plan Note uses it |
| sum rule | 184 | taught | MA-014 (marginalising = sum rule) |
| support point | 61 | add | **paramline** → MA 05-linear-algebra, extend MA-051 (equation of a hyperplane). support point of an affine subspace |
| support vector | 384 | taught | ML-086 (support vectors) |
| supporting hyperplane | 242 | out-of-scope | convex-analysis tool (MML §7.3) |
| surjective | 48 | out-of-scope | function-theory vocabulary used in MML proofs |
| SVD | 119 | taught | MA-057 (SVD) |
| SVD theorem | 119 | taught | MA-057 (SVD) |
| symmetric | 73, 76 | taught | MA-057, MA-068 (symmetric, positive definite) |
| symmetric matrix | 25 | taught | MA-057, MA-068 (symmetric, positive definite) |
| symmetric, positive definite | 74 | taught | MA-057, MA-068 (symmetric, positive definite) |
| symmetric, positive semidefinite | 74 | taught | MA-068 (positive semidefinite) |
| system of linear equations | 20 | add | **linsolve** → MA 05-linear-algebra, new Note after MA-053 (before MA-058 four subspaces). system of linear equations |
| target space | 175 | taught | MA-020 (values a random variable takes) |
| Taylor polynomial | 142, 166 | taught | MA-061, MA-064 (Taylor) |
| Taylor series | 142 | taught | MA-061, MA-064 (Taylor) |
| test error | 300 | taught | ML-012 (test set and error) |
| test set | 262, 284 | taught | ML-012 (test set and error) |
| Tikhonov regularization | 265 | taught | ML-062 (L2 / Tikhonov regularisation) |
| trace | 103 | add | **trace** → MA 05-linear-algebra, short section in MA-056 (eigenvalues). trace |
| training | 12 | taught | ML-001 (training) |
| training error | 300 | taught | ML-061 (training error) |
| training set | 260, 292 | taught | ML-012 (training set) |
| transfer function | 315 | taught | DL-027 (MML uses "transfer function" for an activation function, G-2004); the control-theory transfer function is a separate add (see FBS) |
| transformation matrix | 51 | taught | MA-053 (transformation matrix) |
| translation vector | 63 | taught | MA-053 (affine shift); plan §4 Rigid-body transforms |
| transpose | 25, 38 | taught | ML-053 (transpose) |
| triangle inequality | 71, 76 | taught | Note 108 (rules a distance must follow) |
| truncated SVD | 129 | taught | MA-059 (truncated SVD) |
| Tucker decomposition | 136 | out-of-scope | tensor (Tucker) decomposition: ML research method |
| underfitting | 271 | taught | ML-007 (underfitting) |
| undirected graphical model | 283 | out-of-scope | undirected graphical models: no plan Note uses them |
| uniform distribution | 182 | taught | MA-029 (uniform) |
| univariate | 178 | taught | ML-019 (univariate) |
| unscented transform | 170 | taught | Note 256 (unscented Kalman filter) |
| upper-triangular matrix | 101 | add | **linsolve** → MA 05-linear-algebra, new Note after MA-053 (before MA-058 four subspaces). upper-triangular (echelon) form and back substitution |
| validation set | 263, 284 | taught | ML-012, DL-011 (validation set) |
| variable selection | 316 | taught | ML-066 (lasso selects variables) |
| variance | 190 | taught | MA-012 (variance) |
| vector | 37 | taught | MA-048 (vectors) |
| vector addition | 37 | taught | MA-052 (vector addition) |
| vector space | 37 | taught | MA-052 (vector spaces as spans) |
| vector space homomorphism | 48 | out-of-scope | abstract-algebra name for a linear map (taught as linear transformation, MA-053) |
| vector space with inner product | 73 | out-of-scope | abstract inner-product spaces (as 197) |
| vector subspace | 39 | taught | MA-052 (subspace) |
| weak duality | 235 | taught | MA-066 (weak duality) |
| zero-one loss | 381 | taught | ML-075 (accuracy = share of 0-1 losses that are 0) |
