---
title: "Range Sensors: the Beam Model"
tags: [subject/robotics, area/localization, concept/measurement-model, concept/beam-model, concept/mixture-density]
---

## 1. Overview

> **Key point:** A robot judges a guess about its **pose** (G-2280), where it stands and which way it faces, by asking how likely its laser readings would be from there. The beam model gives that number for one reading as a mix of four causes, so that a person walking past does not make the right pose look impossible.

So far the robot has a [grid map](../RO-009-maps-and-landmarks/RO-009-maps-and-landmarks.md#3-feature-based-and-grid-maps) (G-2335) of its room: the room split into small cells, each marked free or occupied. The map does not say where the robot is on it; the robot can only guess poses and test each guess against what its sensors report. Figure 1 shows where that test breaks: watch the four beams leave the robot one by one, and see which one stops short of the wall.

![Animation: a 5 m by 4 m room seen from above. The robot at (2, 2), facing along x, fires four laser beams one by one, at 0°, 90°, 180° and 270° from its heading. Each beam travels out and stops at the first surface it meets: the forward beam at a person 1.00 m ahead, although the wall is 3 m away (dashed blue line); the other three at the walls, after 1.97, 2.04 and 1.99 m. The readings fill in beside the room, and the last frame holds the whole scan](images/scan_anim.gif)

The robot stands at pose (2, 2, 0) in a 5 m by 4 m room; its laser measures the distance to the nearest surface in four directions. A person stands 1 m in front of it, so the forward beam reads 1.00 m, although the map says the wall is 3 m away. Is the robot at (2, 2, 0), or one metre further along at (3, 2, 0)? This Note adds the rule that answers it.

The room is smaller and emptier than the [7 m by 4 m room with poles and furniture](../RO-009-maps-and-landmarks/RO-009-maps-and-landmarks.md#1-overview) used for maps: a laser needs only walls, and bare walls keep every **expected range** (G-2375), the distance a beam should read according to the map, a round number we can check by hand.

A sensor reading is a [measurement](../RO-007-why-a-robot-is-never-sure/RO-007-why-a-robot-is-never-sure.md#51-measurements-and-controls) (G-2317): what the sensors report about the world at one moment. To test a guessed pose we need a rule that answers one question: how likely are these four readings if the robot stood at that pose? This Note builds the standard rule for range sensors:

- what a range sensor reports, and why the question above is the one to ask ([Section 2](#2-what-a-range-sensor-measures));
- why a Gaussian around the expected range is not enough ([Section 3](#3-why-a-gaussian-alone-fails));
- the four causes of a reading and the shape each one gives, with the reason for every shape ([Section 4](#4-the-four-causes-of-a-reading));
- how the four shapes combine into one model, and what the model says about Figure 1 ([Section 5](#5-the-beam-model-one-mixture-of-four-shapes));
- how to learn the model's numbers from recorded readings, by maximum likelihood and the [**EM algorithm**](../../../../MA/08-likelihood/MA-074-expectation-maximization/MA-074-expectation-maximization.md#3-the-two-steps-and-the-algorithm) (G-675) ([Section 6](#6-learning-the-models-numbers-from-data));
- the other kinds of sensor models a robot uses ([Section 7](#7-a-catalogue-of-sensor-models)).

## 2. What a range sensor measures

> **Key point:** A range sensor reports, for each direction, the distance to the first surface the beam meets. A measurement model scores a guessed **pose** (G-2280), a position and heading, by how likely those distances are from there.

### 2.1 Range finders and scans

The four numbers of Figure 1 come from a **range finder** (G-2371), which measures the distance to the nearest surface in one direction. A laser range finder, or [LiDAR](../../../../DL/01-basics/DL-003-nn-types-history-applications/DL-003-nn-types-history-applications.md#41-mainstream-applications) (G-1083), sends a short pulse of light and times its return. The pulse travels to the surface and back, so the time of flight multiplied by the speed of light is twice the distance; halved, it is the distance. A sonar does the same with a sound pulse (LaValle §11.5.1).

A scanning laser turns, so one sweep gives many readings, for example one every half degree. The list of readings from one sweep is a **range scan** (G-2372). Figure 2 plays both steps in our room: first watch one pulse of the forward beam go out to the person and back while a clock runs, and the round trip turn into the reading 1.00 m; then watch the head turn and the readings outline the room.

![Animation in the room of Figure 1. First, one reading: the forward beam's pulse travels out to the person and back while a clock runs; the echo is back after 6.67 nanoseconds (ns, billionths of a second). Light covers about 0.3 m per ns, so in 6.67 ns the pulse travelled 2.00 m, out and back, and the reading is half of that, 1.00 m. Then the laser head turns and fires one beam every 0.5°; each red dot marks where a beam stopped, and after a full turn 720 dots outline the walls and the person, scattered by a few centimetres of sensor noise. Beams that leave through the glass pane in the top wall meet nothing within 5 m, no echo comes back in time, and each reports 5 m (purple dots)](images/pulse_scan.gif)

For one scan:

- $z^k$ is the reading of beam $k$, in m (1.00 m for the forward beam of Figure 1);
- $K$ is the number of beams, 4 in Figure 1;
- $z$ is the whole scan, the list of all $K$ readings.

$$z = (z^1, z^2, \dots, z^K)$$

Figure 1's four beams point at 0°, 90°, 180° and 270° from the robot's heading:

$$z = (1.00,\ 1.97,\ 2.04,\ 1.99)$$

Every sensor has a longest distance it can report. When no surface returns the pulse in time, as for the beams through the glass in Figure 2, the sensor reports that longest distance itself. That longest distance is the **maximum range** (G-2373) $z_{\max}$; our laser has:

$$z_{\max} = 5 \text{ m}$$

### 2.2 Why we need a measurement model

Suppose the robot is unsure whether it is at pose A, (2, 2, 0), or at pose B, (3, 2, 0): one metre further along the room. To decide, it compares its readings with what each pose would predict. The map predicts, for each pose and each beam, the distance the beam should travel before it meets a wall: the **expected range** (G-2375), written $z^{\ast}$.

We find it by **ray casting** (G-2376): start at the robot, walk along the beam's direction in small steps, and stop at the first occupied cell of the grid map (Figure 3). The distance walked is $z^{\ast}$. For the forward beam:

- $z_{A}^{\ast}$ is its expected range from pose A, in m;
- $z_{B}^{\ast}$ is its expected range from pose B, in m.

$$z_{A}^{\ast} = 3.0 \text{ m}$$

$$z_{B}^{\ast} = 2.0 \text{ m}$$

In Figure 3, watch the counter as each ray checks one cell after another: the walk ends when the ray enters a wall cell, after 3.0 m from pose A and after 2.0 m from pose B.

![Animation of ray casting in the grid map of the room, drawn with 0.5 m cells (the notebook walks in 1 mm steps); the dark ring of cells is the wall. From pose A at (2, 2) the forward ray checks one cell at a time (orange box): six free cells, then it enters a wall cell and stops after 3.0 m. Then from pose B at (3, 2): four free cells, then a wall cell, stop after 2.0 m. The counter shows the distance walked; both rays start at y = 2 and are drawn in different rows so both show](images/raycast_anim.gif)

The reading was 1.00 m, which matches neither 3.0 nor 2.0. We need a number for "how well does a reading of 1.00 m fit an expected range of 3.0 m?", one that tolerates small sensor errors and an odd reading now and then. That number is the **measurement model** (G-2374), also called the sensor model or observation model (Thrun §6.1). For one scan and one guessed pose:

- $z$ is the scan, the four readings (1.00, 1.97, 2.04, 1.99) m;
- $x$ is the guessed pose, such as A;
- $m$ is the map, the grid map of the room;
- the bar $\mid$ reads "given".

$$p(z \mid x, m)$$

In words: the density of getting the readings $z$, given that the robot is at pose $x$ and the world looks like map $m$. The pose $x$ is the [pose](../../../control/01-robot-models/RO-001-pose-and-differential-drive/RO-001-pose-and-differential-drive.md#22-why-position-is-not-enough-the-heading) (G-2280) of a floor robot, position and heading:

- its first entry $x$ is the position along the room, in m (2 m at pose A);
- $y$ is the position across the room, in m (2 m at pose A);
- $\theta$ is the heading, in degrees (0° at pose A, facing along x).

$$x = (x,\ y,\ \theta)$$

For a fixed set of readings, $p(z \mid x, m)$ read as a function of the pose is the [likelihood](../../../../MA/08-likelihood/MA-069-probability-vs-likelihood/MA-069-probability-vs-likelihood.md#22-likelihood-from-the-event-back-to-the-parameter) (G-1086) of that pose: the poses under which the readings are more likely score higher. A localization filter uses the model this way: the [**Bayes filter**](../RO-014-bayes-filter/RO-014-bayes-filter.md#43-the-correction-step) (G-2446) multiplies its belief by this likelihood in its correction step.

A range reading is a continuous quantity, so $p(z \mid x, m)$ is a [probability density](../../../../MA/03-distributions/MA-022-pdf-and-continuous-cdf/MA-022-pdf-and-continuous-cdf.md#5-what-the-density-at-a-point-means) (G-1569), not a probability: per metre for one reading, per m⁴ for our scan of four readings. A density can be larger than 1; only areas under it are probabilities.

### 2.3 Why a whole scan is a product of beams

A scan has many beams, and writing one density for all of them at once is hard. We split it into one density per beam and multiply. With the symbols of [Section 2.1](#21-range-finders-and-scans) and [Section 2.2](#22-why-we-need-a-measurement-model):

- $z^k$ is the reading of beam $k$, in m;
- $K$ is the number of beams, 4;
- $x$ is the guessed pose, such as A;
- $m$ is the map;
- $\prod$ means "multiply the terms for $k = 1$ to $K$".

$$p(z \mid x, m) = \prod_{k=1}^{K} p(z^k \mid x, m)$$

Multiplying is allowed when the beams are independent: knowing one beam's error tells us nothing about another's. Independence does not hold in general, but it nearly holds once the **pose** (G-2280) and the map are known (Thrun §6.3.1):

- **Without a map**, beams are linked: if one beam hits something at 2 m, the beam half a degree away probably hits the same object at about 2 m.
- **With the map and the pose given**, that shared object is already in the map, so each beam's remaining error is its own sensor noise, and the beams are close to independent.

Independence that holds only once a third thing is known is [conditional independence](../../../../ML/07-classification/ML-082-naive-bayes-maths/ML-082-naive-bayes-maths.md#5-step-3-the-naive-assumption) (G-443), the same assumption Naive Bayes makes for features given the class.

> **Extra:** The assumption is not exact. A person blocks several neighbouring beams at once, and their errors are then linked. The product then counts that one person several times, which makes the model overconfident (Freiburg sensor-model slides, "Summary beam-based model"). Implementations therefore use only a subset of the beams of each scan: the ROS localization package AMCL uses 30 evenly spaced beams per scan by default (ROS amcl, `laser_max_beams`).

So scoring a pose comes down to one density per beam; what is still missing is the shape of that density.

## 3. Why a Gaussian alone fails

> **Key point:** A narrow Gaussian around the expected range gives a reading caused by a passer-by a density of practically zero, and the product then rejects the true **pose** (G-2280), the robot's real position and heading, outright.

The first rule that comes to mind fails on the person's 1.00 m reading of Figure 1. The rule says the reading should be the **expected range** (G-2375), the distance the map predicts, plus a small sensor error, and small errors follow a [Gaussian distribution](../../../../MA/03-distributions/MA-024-normal-distribution/MA-024-normal-distribution.md#2-what-the-normal-distribution-is) (G-827). A good laser's readings typically lie about 0.05 m from the true distance: its [**standard deviation**](../../../../MA/02-probability/MA-012-expected-value-and-variance/MA-012-expected-value-and-variance.md#41-variance-term-by-term) (G-1870) is $\sigma = 0.05$ m. For one beam:

- $z$ is the beam's reading, in m (1.00 m for the forward beam);
- $z^{\ast}$ is its expected range, 3 m for the forward beam at pose A;
- $\sigma$ is the sensor's standard deviation, 0.05 m;
- $\mathcal{N}(z;\ z^{\ast}, \sigma^2)$ is the Gaussian density of the reading, with mean $z^{\ast}$ and variance $\sigma^2$, in per m.

$$\mathcal{N}(z;\ z^{\ast}, \sigma^2) = \frac{1}{\sigma\sqrt{2\pi}}\ e^{-\frac{1}{2}\left(\frac{z - z^{\ast}}{\sigma}\right)^2}$$

Figure 4 draws it for the forward beam at the true pose A, where $z^{\ast} = 3$ m. Now put the person's reading, 1.00 m, into it. The distance from the expected range, in units of $\sigma$:

$$\frac{1.00 - 3.00}{0.05} = -40$$

The exponent:

$$-\tfrac{1}{2} \times 40^2 = -800$$

The factor in front of the exponential:

$$\frac{1}{0.05 \times \sqrt{2\pi}} = 7.98$$

The density:

$$7.98 \times e^{-800}$$

$$\approx 0$$

The number $e^{-800}$ is so small that a computer stores it as exactly 0 (the notebook checks). In Figure 4, the reading of 1.00 m sits 40 standard deviations left of the peak, where the curve lies flat on the axis.

![A Gaussian with standard deviation 0.05 m around the expected range 3 m. The reading 1.00 m, caused by a person, sits far out in the tail, where the density is about e to the minus 800, effectively 0](images/gaussian_fails.png)

Because the scan density is a product, one zero beam makes the whole scan density zero, whatever the other beams say. So the true pose A gets 0. The wrong pose B fits the backward beam far worse but escapes the zero: its forward beam expects 2 m, and its backward beam expects 3 m but reads 2.04 m. Those two densities are tiny but not zero, and B ends up with a scan density of about $4 \times 10^{-164}$. A Gaussian alone would prefer the wrong pose, only because a person stepped in front of the robot.

The cure is not a wider Gaussian: that would make every reading near the wall less informative too. Instead we list the other ways a reading can come about, and give each its own shape.

## 4. The four causes of a reading

> **Key point:** A reading is one of four things: a correct hit with small noise; a hit on something not in the map; a failure, which reports the sensor's longest distance, its **maximum range** (G-2373); or a random reading with no modelled cause. Each cause has its own density shape, and each shape follows from how that cause works.

The person's reading is one of four ways a beam can come back. Figure 5 shows the shape each gives for the forward beam at **pose** (G-2280) A, the robot at (2, 2) facing along x (expected range $z^{\ast} = 3$ m, maximum range $z_{\max} = 5$ m). They come from Thrun §6.3.1 and the Freiburg sensor-model slides; the reason for each shape follows below. In Figure 5, look at where each panel puts its density: a narrow peak at the wall, a pile that falls off before it, a spike at 5 m, and a flat floor everywhere.

![The four densities of the beam model for an expected range of 3 m: a narrow Gaussian at 3 m (measurement noise), a curve that starts high at 0 and falls off until it stops at 3 m (unexpected objects), a spike at 5 m (failures), and a flat line at height 0.2 from 0 to 5 m (random readings)](images/four_parts.png)

### 4.1 Measurement noise: a Gaussian around the expected range

When the beam does reach the mapped wall, the reading still differs a little from $z^{\ast}$: limited resolution, temperature, the surface. In Figure 6, watch the forward beam hit the wall 3 m away again and again: its readings land almost all within 0.1 m of 3 m, and their histogram settles onto a narrow Gaussian around 3 m.

![Animation: with nobody in the way, the forward beam of pose A hits the wall 3 m away again and again (simulated readings, reported in 1 cm steps; the first is the 3.02 m of the worked example below). Left: the room and the current reading. Right: the histogram of the readings so far as density per metre, one bar per 1 cm step, zoomed to 2.75 to 3.25 m; the black curve is the Gaussian around 3 m with standard deviation 0.05 m, whose peak is 7.98 per m. As the readings pile up, the bars settle onto the curve; the last frame holds 2000 readings, 97% of them within 0.1 m of 3 m](images/noise_anim.gif)

This **measurement noise** (G-2378) is the Gaussian of [Section 3](#3-why-a-gaussian-alone-fails), with one change. Readings below 0 or above $z_{\max}$ cannot occur, so the Gaussian is cut to the range from 0 to $z_{\max}$ and scaled up so its area is 1 again. For one beam:

- $z$ is the reading, in m;
- $z^{\ast}$ is the expected range, 3 m for the forward beam at pose A;
- $z_{\max}$ is the maximum range, 5 m;
- $\sigma_{\text{hit}}$ is the standard deviation of the hits, the $\sigma$ of [Section 3](#3-why-a-gaussian-alone-fails), 0.05 m;
- $\eta$ (eta) is the **normalizer** (G-2382): one over the area of the Gaussian that lies inside the range, so that the whole density again has area 1 (Thrun §6.3.1); 1.000 for our wall at 3 m;
- $p_{\text{hit}}(z)$ is the density of the reading when the beam hits the mapped wall, in per m.

$$p_{\text{hit}}(z) = \eta\ \mathcal{N}(z;\ z^{\ast}, \sigma_{\text{hit}}^2)$$

for $0 \le z \le z_{\max}$, and 0 outside. A Gaussian cut to a range and rescaled is a [truncated normal](../../../../DL/02-training/DL-030-xavier-he-initialization/DL-030-xavier-he-initialization.md#62-with-keras-initialisers) (G-2023).

For our wall at 3 m, the Gaussian lies far inside the range (at least 40 $\sigma$ from 0 and from 5 m), so $\eta = 1.000$. The normalizer matters near the edge. If the wall were 4.98 m away, about a third of the Gaussian would lie beyond 5 m:

$$\text{area inside} = 0.655$$

$$\eta = 1 / 0.655 = 1.53$$

**Worked example.** At **pose** (G-2280) A the forward beam expects 3 m. For a reading of 3.02 m, the distance from the expected range, in units of $\sigma_{\text{hit}}$:

$$\frac{3.02 - 3.00}{0.05} = 0.4$$

The exponent:

$$-\tfrac{1}{2} \times 0.4^2 = -0.08$$

The density, with the factor 7.98 in front as in [Section 3](#3-why-a-gaussian-alone-fails) and $\eta = 1.000$:

$$p_{\text{hit}}(3.02) = 7.98 \times e^{-0.08}$$

$$= 7.37 \text{ per m}$$

The hit part explains readings near the wall, such as 3.02 m; the person's 1.00 m still gets a density of practically 0 from it.

### 4.2 Unexpected objects: why the curve falls off, and why it stops

A person, a chair or an open door that is not in the map can block the beam first. The reading is then shorter than $z^{\ast}$. Such a blocker is an **unexpected object** (G-2379), and its reading a short reading. Figure 5 shows its shape: high at 0, falling off, and zero after $z^{\ast}$. Both features have a reason.

**Why it stops at the expected range.** An object behind the wall cannot block the beam: the wall is hit first. So a short reading is always shorter than $z^{\ast}$, and the density is 0 beyond it.

**Why it falls off.** Only the first object along the beam matters; anything behind it is hidden. Cut the beam into 4 equal cells and let each cell be either blocked (1) or free (0), all 16 patterns equally likely. Figure 7 sorts the 16 patterns by the first blocked cell:

| First blocked cell | Patterns |
|---|---|
| 1 | 8 |
| 2 | 4 |
| 3 | 2 |
| 4 | 1 |
| none | 1 |

![The 16 ways to fill 4 cells along a beam, grouped by the first blocked cell: 8 patterns stop at cell 1, 4 at cell 2, 2 at cell 3, 1 at cell 4 and 1 pattern is never blocked](images/bitstrings.png)

The first cell is blocked in 8 of the 16 patterns, more than all the patterns that first stop further out:

$$1 + 2 + 4 = 7$$

The count halves with each cell, because each extra free cell in front is one more condition the pattern must meet.

The same holds for any blocking chance. Let each cell be blocked independently of the others:

- $b$ is the chance that one cell is blocked, a number from 0 to 1 (0.2 below);
- $j$ is a cell's number along the beam, counted from the robot (1, 2, 3, …);
- $P(\text{first stop at cell } j)$ is the probability that the beam stops at cell $j$ and not before.

For the beam to stop at cell $j$, the $j - 1$ cells before it must be free and cell $j$ blocked:

$$P(\text{first stop at cell } j) = (1 - b)^{j - 1}\ b$$

Each further cell multiplies the chance by the same factor $1 - b$. With cells of 0.1 m and $b = 0.2$:

$$P(\text{cell } 1) = 0.2$$

$$P(\text{cell } 2) = 0.8 \times 0.2 = 0.16$$

$$P(\text{cell } 3) = 0.8^2 \times 0.2 = 0.128$$

Figure 8 runs this as an experiment: in each trial, cells of a 3 m beam are blocked at random, and we record where the beam stops. After 5000 trials the shares match the formula.

![Animation: in each trial, 0.1 m cells along a 3 m beam are blocked with probability 0.2; the beam stops at the first blocked cell. The histogram of where it stopped builds up trial by trial and settles on the curve 0.2 times 0.8 to the power j minus 1](images/first_hit.gif)

A curve that falls by the same factor at every step is exponential. Make the cells shorter and keep the blocking chance per metre fixed:

- $\Delta$ is the cell length, in m (0.1 m, then shorter);
- $\lambda$ is the blocking chance per metre, 2 per m;
- $z$ is the distance along the beam, in m (1 m in the table).

The chance per cell is then:

$$b = \lambda\Delta$$

The share per metre at 1 m approaches $\lambda e^{-\lambda z}$:

| Cell length $\Delta$ | Share per metre at 1 m |
|---|---|
| 0.1 m | 0.215 |
| 0.01 m | 0.265 |
| 0.001 m | 0.270 |
| limit: $2 e^{-2}$ | 0.271 |

So the short-reading density is an [exponential distribution](../../../../MA/08-likelihood/MA-071-mle-for-common-distributions/MA-071-mle-for-common-distributions.md#31-the-distribution-of-waiting-times) (G-733), cut at $z^{\ast}$. The exponential holds under the assumption made above: objects are spread evenly and block the beam with the same chance per metre at every distance (De Laet et al. 2008, §3.6). Its rate $\lambda_{\text{short}}$ is large in a crowded hall and small in an empty one. For one beam:

- $z$ is the reading, in m;
- $z^{\ast}$ is the expected range, 3 m for the forward beam at pose A;
- $\lambda_{\text{short}}$ is the rate of unexpected objects, the $\lambda$ above: the chance per metre that one blocks the beam, 2 per m;
- $\eta$ is again the normalizer, now one over the area of the exponential between 0 and $z^{\ast}$ (1.0025, worked out below);
- $p_{\text{short}}(z)$ is the density of a short reading, in per m.

$$p_{\text{short}}(z) = \eta\ \lambda_{\text{short}}\ e^{-\lambda_{\text{short}} z}$$

for $0 \le z \le z^{\ast}$, and 0 otherwise (Thrun §6.3.1).

**The normalizer.** The exponential's area from 0 to $z^{\ast}$ is:

$$\int_0^{z^{\ast}} \lambda e^{-\lambda z}\thinspace dz = 1 - e^{-\lambda z^{\ast}}$$

So $\eta$ is one over that area. With $\lambda_{\text{short}} = 2$ per metre and $z^{\ast} = 3$ m:

$$1 - e^{-6} = 0.9975$$

$$\eta = 1.0025$$

**Worked example.** The person's reading, 1.00 m:

$$p_{\text{short}}(1.00) = 1.0025 \times 2 e^{-2}$$

$$= 1.0025 \times 0.2707$$

$$= 0.2714 \text{ per m}$$

The person's 1.00 m now has a cause with a density above 0; a reading of exactly 5 m, which no blocker in front of the wall can give, still has none.

### 4.3 Failures: a spike at the maximum range

Sometimes no pulse comes back: the beam hits glass or a black, light-absorbing surface, bounces off a shiny surface at a slant, or the wall is out of range (Thrun §6.3.1). The sensor then reports $z_{\max}$. Figure 9 shows one failure and then many: watch the clock run past the time a 5 m echo needs, and every failure reading land in the same bar at 5 m, although the wall is at 3 m.

![Animation of failures on the forward beam of pose A, whose wall is 3 m away. The pulse is lost at the wall (for example on a black or shiny spot) and no echo comes back. The clock passes 20.0 ns, when an echo from the wall would be back, and reaches 33.4 ns, the time light needs to go 5 m and back; with no echo by then, the sensor reports its maximum range, 5 m (purple dot). Right: the histogram of the failure readings, as counts per 0.05 m bin, grows a single bar at 5 m; the last frame holds 50 failures, all at exactly 5 m](images/failure_anim.gif)

Such a **max-range reading** (G-2380) lands on exactly one value, 5 m, however far the wall is. So its density is a single spike at $z_{\max}$:

- $z$ is the reading, in m;
- $z_{\max}$ is the maximum range, 5 m;
- $p_{\max}(z)$ is the failure part of the model.

$$p_{\max}(z) = 1 \text{ if } z = z_{\max}, \text{ else } 0$$

A distribution that puts all its probability on one value is a **point mass** (G-2383). A point mass has no height, only a probability, so it cannot be added to densities as it stands. In code we draw it as a narrow box one sensor step wide (1 cm), of height 100 per metre, so its area is 1 (Figure 5, third panel).

Readings of exactly 5 m now have a cause; a stray reading such as 4 m, behind the wall at 3 m, still has none.

### 4.4 Random readings: the uniform part

Some readings have no cause we can model: cross-talk between sonars, reflections that come back by a strange path, electronic glitches (Thrun §6.3.1; Freiburg slides). In Figure 10, watch such stray readings of the forward beam land anywhere from 0 to 5 m, even beyond the wall at 3 m, and their histogram fill in evenly into a flat floor.

![Animation of random readings on the forward beam of pose A, whose wall is 3 m away. Each stray echo gives a reading drawn at random, evenly, from 0 to 5 m (simulated, as the uniform part below assumes); the big green dot is the newest reading, the small dots the ones before it. Right: the histogram of the readings so far, as density per metre in 0.25 m bins; the black line is the uniform part, 0.2 per m. The last frame holds 5000 readings, spread evenly along the line](images/random_anim.gif)

We know nothing about where such a **random measurement** (G-2381) lands, so we give every value from 0 to $z_{\max}$ the same density, a [uniform distribution](../../../../MA/03-distributions/MA-029-uniform-and-log-normal/MA-029-uniform-and-log-normal.md#2-the-uniform-distribution) (G-2043):

- $z$ is the reading, in m, anywhere from 0 to $z_{\max}$;
- $z_{\max}$ is the maximum range, 5 m;
- $p_{\text{rand}}(z)$ is the density of a random reading, in per m.

$$p_{\text{rand}}(z) = \frac{1}{z_{\max}}$$

$$= \frac{1}{5} = 0.2 \text{ per m}$$

The uniform part $p_{\text{rand}}$ has a job: no reading between 0 and 5 m ever gets a density of exactly 0, so one strange reading can never wipe out a whole scan.

## 5. The beam model: one mixture of four shapes

> **Key point:** The beam model adds the four densities with weights that sum to 1. With it, the person's reading costs **pose** (G-2280) A, the robot's true position and heading, a factor, not everything, and A wins.

### 5.1 The mixture

We do not know whether the forward beam's 1.00 m came from the person or from a random reading, only how often each cause happens. So the density of a reading is the weighted sum of the four densities, a [mixture density](../../../../MA/08-likelihood/MA-073-gaussian-mixture-models/MA-073-gaussian-mixture-models.md#61-the-formula) like a Gaussian mixture, but with parts of different shapes. For one beam $k$:

- $p(z^k \mid x, m)$ is the density of beam $k$'s reading $z^k$, given the pose $x$ and the map $m$, in per m;
- $p_{\text{hit}}$ is the Gaussian around the expected range ([Section 4.1](#41-measurement-noise-a-gaussian-around-the-expected-range));
- $p_{\text{short}}$ is the falling exponential of unexpected objects ([Section 4.2](#42-unexpected-objects-why-the-curve-falls-off-and-why-it-stops));
- $p_{\max}$ is the failure spike at 5 m ([Section 4.3](#43-failures-a-spike-at-the-maximum-range));
- $p_{\text{rand}}$ is the uniform part, 0.2 per m ([Section 4.4](#44-random-readings-the-uniform-part));
- $w_{\text{hit}}$ is the share of readings that are hits, 0.75;
- $w_{\text{short}}$ is the share caused by unexpected objects, 0.12;
- $w_{\max}$ is the share of failures, 0.05;
- $w_{\text{rand}}$ is the share of random readings, 0.08.

$$p(z^k \mid x, m) = w_{\text{hit}}\ p_{\text{hit}} + w_{\text{short}}\ p_{\text{short}}$$

$$\qquad + w_{\max}\ p_{\max} + w_{\text{rand}}\ p_{\text{rand}}$$

The [mixture weights](../../../../MA/08-likelihood/MA-073-gaussian-mixture-models/MA-073-gaussian-mixture-models.md#62-why-the-weights-must-add-up-to-1) (G-1238) are the shares of readings each cause produces. They are not negative and add up to 1, so the mixture's area is 1 too. Thrun writes them $z_{\text{hit}}, \dots$; we write $w$ so that $z$ always means a reading. This weighted mixture of four densities is the **beam model** (G-2377) of a **range finder** (G-2371), a distance sensor such as our laser; it is also called the beam-based proximity model (Thrun §6.3; Freiburg slides). We use these weights in Sections [5](#5-the-beam-model-one-mixture-of-four-shapes) and [6](#6-learning-the-models-numbers-from-data):

| Cause | Weight | Shape |
|---|---|---|
| hit, measurement noise | $w_{\text{hit}} = 0.75$ | Gaussian, $\sigma_{\text{hit}} = 0.05$ m |
| unexpected object | $w_{\text{short}} = 0.12$ | exponential, $\lambda_{\text{short}} = 2$ per m |
| failure | $w_{\max} = 0.05$ | spike at 5 m |
| random | $w_{\text{rand}} = 0.08$ | uniform, 0.2 per m |

Figure 11 adds the four weighted parts one at a time, each on top of the ones before; watch the top edge change with each part, and in the last frame the black top edge is the mixture. Its odd shape, with the falling start, the dip just before the wall, the Gaussian, the uniform part and the spike at the end, is the sum of four simple shapes.

![Animation: the beam model for an expected range of 3 m, built by stacking the weighted parts one at a time: a green uniform layer (random readings, weight 0.08, height 0.016 per m), an orange falling curve up to 3 m (unexpected objects, weight 0.12), the blue Gaussian at 3 m (measurement noise, weight 0.75; its peak, 6.00 per m, is cut off at the top) and the purple spike at 5 m (failures, weight 0.05). The last frame draws the top edge in black: the mixture, 0.049 per m at 1.00 m and 0.016 per m at 4.00 m](images/mixture_anim.gif)

**Worked example: the person's reading, 1.00 m, at pose A.** The Gaussian and the spike give 0 there. The other two parts:

$$0.12 \times 0.2714 = 0.0326$$

$$0.08 \times 0.2 = 0.016$$

$$p(1.00 \mid A) = 0.0326 + 0.016$$

$$= 0.0486 \text{ per m}$$

Small, because a short reading is less common than a hit, but not zero.

### 5.2 Back to the opening scan

Now score both **poses** (G-2280) with the beam model. Ray casting gives the expected ranges $z^{\ast}$ of the four beams:

| Beam | Reading (m) | $z^{\ast}$ at A (m) | $z^{\ast}$ at B (m) |
|---|---|---|---|
| 0° | 1.00 | 3.0 | 2.0 |
| 90° | 1.97 | 2.0 | 2.0 |
| 180° | 2.04 | 2.0 | 3.0 |
| 270° | 1.99 | 2.0 | 2.0 |

Figure 12 scores the scan beam by beam, first for pose A, then for pose B. For each beam, watch where its reading lands on the beam model drawn around that beam's expected range: the height of the curve there is the beam's density, and it is multiplied into a running product.

![Animation of scoring the opening scan. Left: the beam model of the current beam, drawn around its expected range z* (dashed line), and the reading (dotted red line); the dot on the curve is the density read off. Right: the room with the guessed pose, each beam drawn from that pose with the length it read (red) and to where the map says it should end (dashed), and the table of densities with the running product. Pose A ends at 6.26 per m⁴, pose B at 0.0291 per m⁴. The last frame shows the backward beam that decides: its reading, 2.04 m, sits near the peak of A's curve (4.361 per m) but in the flat tail of B's (0.02007 per m); the ratio of the two scan densities is 215](images/score_anim.gif)

The beam densities (per m), from the notebook:

| Beam | Pose A | Pose B |
|---|---|---|
| 0° | 0.04856 | 0.04909 |
| 90° | 5.019 | 5.019 |
| 180° | 4.361 | 0.02007 |
| 270° | 5.886 | 5.886 |
| product (per m⁴) | 6.26 | 0.0291 |

The forward beam costs both poses about the same, because both explain 1.00 m only as a short reading. The backward beam decides: it fits A's expected 2 m well and B's expected 3 m badly. The ratio of the two scan densities:

$$\frac{6.26}{0.0291} = 215$$

So the scan is about 215 times more likely from pose A than from pose B, and the beam model picks the right pose. The Gaussian alone gave A exactly 0.

> **Python:** the **beam model** (G-2377) for a whole scan, as in the UChicago class 05 algorithm.
> ```python
> def beam_model(readings, expected):  # metres
>     q = 1.0
>     for z, zs in zip(readings, expected):
>         q *= mixture(z, zs)  # four weighted parts
>     return q
> beam_model([1.00, 1.97, 2.04, 1.99], [3, 2, 2, 2])   # 6.26 (pose A)
> beam_model([1.00, 1.97, 2.04, 1.99], [2, 2, 3, 2])   # 0.0291 (pose B)
> ```
> `mixture` is defined in the notebook `RO-010-range-sensors-beam-model.ipynb`.

## 6. Learning the model's numbers from data

> **Key point:** Record many readings of a wall at a known distance and choose the weights and widths that make those readings most likely. The causes are hidden, so EM finds them by alternating "which cause made each reading?" with "refit each cause".

### 6.1 Why the numbers must be learned

The answer of [Section 5.2](#52-back-to-the-opening-scan), the scan about 215 times more likely from **pose** (G-2280) A (the robot's true position and heading) than from pose B, rests on six numbers we chose: the four weights, the standard deviation of the hits $\sigma_{\text{hit}}$ (0.05 m) and the rate of short readings $\lambda_{\text{short}}$ (2 per m). The six numbers are the model's **intrinsic parameters** (G-2384): they belong to the sensor and its surroundings, not to the pose (Thrun §6.3.4). A sonar is noisier than a laser, and a busy hall has more short readings than an empty lab, so no textbook value fits every robot. We measure them.

The experiment: place the robot 3 m from a wall and record 1000 readings of the beam that faces it while people walk past (Freiburg slides, "Raw sensor data" for an expected distance of 300 cm). Figure 13 shows the result as counts per 0.05 m bin. Look for the four causes in it: the tall peak at the wall, the falling pile of short readings near 0, the thin even layer of random readings, and the bar at 5 m. We built these readings in the notebook from the model of [Section 5](#5-the-beam-model-one-mixture-of-four-shapes), so that we can check the fit against known values; real recordings look the same (Freiburg slides, "Raw sensor data").

![1000 readings of a wall 3 m away as counts per 0.05 m bin. Left: a tall peak at 3 m. Right, zoomed to counts up to 25: a falling pile of short readings near 0, a thin uniform layer of random readings, and a bar of 47 readings at the maximum range of 5 m](images/wall_data.png)

Some numbers are easy. With nobody around, the readings scatter only by **measurement noise** (G-2378), and $\sigma_{\text{hit}}$ is their **standard deviation** (G-1870), their typical distance from 3 m, as given by the [MLE of a normal distribution](../../../../MA/08-likelihood/MA-071-mle-for-common-distributions/MA-071-mle-for-common-distributions.md#44-the-mle-of-the-standard-deviation) (G-1242). The weights cannot be read off like that: a reading of 2.95 m could be a hit or a short reading, and nothing in the reading says which.

### 6.2 Maximum likelihood, and why it needs a search

The principle is [maximum likelihood estimation](../../../../MA/08-likelihood/MA-070-maximum-likelihood-estimation/MA-070-maximum-likelihood-estimation.md#72-the-maximum-likelihood-estimate) (G-1191): choose the six numbers that make the 1000 recorded readings most likely. With the [log-likelihood](../../../../MA/08-likelihood/MA-070-maximum-likelihood-estimation/MA-070-maximum-likelihood-estimation.md#8-why-we-take-the-log) (G-1113), we maximise a sum over the readings:

- $z_i$ is recorded reading number $i$, in m;
- $n$ is the number of readings, 1000;
- $z^{\ast}$ is the expected range, the wall's distance, 3 m;
- $p(z_i \mid z^{\ast})$ is the mixture of [Section 5](#5-the-beam-model-one-mixture-of-four-shapes) at reading $z_i$, in per m;
- $\ell$ is the log-likelihood, the sum of the logs of those densities.

$$\ell = \sum_{i=1}^{n} \log p(z_i \mid z^{\ast})$$

The log of a sum of four parts does not split into simple pieces, so setting the derivative to zero gives no closed formula, exactly as for a [Gaussian mixture](../../../../MA/08-likelihood/MA-073-gaussian-mixture-models/MA-073-gaussian-mixture-models.md#9-why-maximum-likelihood-has-no-closed-form). The standard way out for mixtures is EM, which guesses which cause made each reading, refits each cause to its readings, and repeats; each of its steps has a simple formula (UW CSE 571 slides; Thrun §6.3.4; De Laet et al. 2008, Algorithm 1).

### 6.3 EM for the beam model

The hidden piece of information is the cause of each reading, a [latent variable](../../../../MA/08-likelihood/MA-073-gaussian-mixture-models/MA-073-gaussian-mixture-models.md#52-the-latent-variable) (G-1050). The [EM algorithm](../../../../MA/08-likelihood/MA-074-expectation-maximization/MA-074-expectation-maximization.md#3-the-two-steps-and-the-algorithm) (G-675) repeats two steps from a starting guess. We start from equal weights 0.25, a standard deviation of the hits $\sigma_{\text{hit}}$ of 0.3 m and a rate of short readings $\lambda_{\text{short}}$ of 0.5 per m.

**E-step: share each reading among the causes.** For each reading, compute each weighted part and divide by their sum. The shares are the [responsibilities](../../../../MA/08-likelihood/MA-073-gaussian-mixture-models/MA-073-gaussian-mixture-models.md#32-the-standard-terms) (G-1687) $e_{i,c}$ of cause $c$ for reading $i$; they add up to 1 over the four causes ([**E-step**](../../../../MA/08-likelihood/MA-074-expectation-maximization/MA-074-expectation-maximization.md#31-the-two-steps) (G-654)). With the starting guess, the weighted parts (per m) for three readings:

| Reading | hit | short | max | rand | sum |
|---|---|---|---|---|---|
| 3.02 m | 0.332 | 0 | 0 | 0.05 | 0.382 |
| 1.00 m | 0 | 0.098 | 0 | 0.05 | 0.148 |
| 5.00 m | 0 | 0 | 25 | 0.05 | 25.05 |

Dividing each row by its sum gives the responsibilities:

| Reading | hit | short | max | rand |
|---|---|---|---|---|
| 3.02 m | 0.869 | 0 | 0 | 0.131 |
| 1.00 m | 0 | 0.661 | 0 | 0.339 |
| 5.00 m | 0 | 0 | 0.998 | 0.002 |

The 3.02 m reading is mostly a hit, the 1.00 m reading mostly a short reading, the 5.00 m reading almost surely a failure.

**M-step: refit each cause to its share of the readings.** Each cause is now fitted like a single distribution, with each reading counted by its responsibility (the [**M-step**](../../../../MA/08-likelihood/MA-074-expectation-maximization/MA-074-expectation-maximization.md#21-one-round-recalled) (G-1139)). With our numbers:

- $e_{i,c}$ is the responsibility of cause $c$ for reading $i$, a number from 0 to 1 (0.869 of the hit cause for the 3.02 m reading above);
- $n$ is the number of readings, 1000;
- $z_i$ is reading number $i$, in m;
- $z^{\ast}$ is the wall's distance, 3 m;
- $w_c$ is the new weight of cause $c$, its share of the readings.

The three refits (Thrun §6.3.4; De Laet et al. 2008, Eq. 65–66):

- **Weights:** a cause's weight is its average responsibility, its share of the readings.

  $$
  w_c = \frac{1}{n} \sum_i e_{i,c}
  $$

- **Standard deviation of the hits:** the responsibility-weighted variance around $z^{\ast}$, the same formula as the MLE of a normal with weighted readings.

  $$
  \sigma_{\text{hit}}^2 = \frac{\sum_i e_{i,\text{hit}}\ (z_i - z^{\ast})^2}{\sum_i e_{i,\text{hit}}}
  $$

- **Rate of the short readings:** the [MLE of an exponential rate](../../../../MA/08-likelihood/MA-071-mle-for-common-distributions/MA-071-mle-for-common-distributions.md#33-the-derivation) (G-1243) is the number of waits over their sum. With weighted readings, the count becomes the sum of responsibilities:

  $$
  \lambda_{\text{short}} = \frac{\sum_i e_{i,\text{short}}}{\sum_i e_{i,\text{short}}\ z_i}
  $$

This last formula ignores the cut at $z^{\ast}$. Ignoring the cut is safe when the curve has nearly died out before $z^{\ast}$, as here: with $\lambda_{\text{short}} = 2$ per m, the share of the exponential beyond 3 m is only

$$e^{-6} = 0.0025$$

Figure 14 plays the rounds. After round 1 the Gaussian has already narrowed onto the wall; after a few rounds the curve follows the bars, and the **log-likelihood** (G-1113) has stopped rising. EM never lowers the log-likelihood from one round to the next ([why the log-likelihood never decreases](../../../../MA/08-likelihood/MA-074-expectation-maximization/MA-074-expectation-maximization.md#6-why-the-log-likelihood-never-decreases)).

![Animation of EM fitting the beam model. Each frame is one round: blue bars are the 1000 readings, the black line is how many readings the current model expects per bin, the right panel is the log-likelihood. Round 0 is a flat, wide guess with log-likelihood −932; by round 60 the weights are hit 0.733, short 0.150, max 0.047, rand 0.070, sigma 0.051 m, lambda 1.75 per m, log-likelihood 448](images/em_fit.gif)

| Round | $w_{\text{hit}}$ | $w_{\text{short}}$ | $w_{\max}$ | $w_{\text{rand}}$ | $\sigma_{\text{hit}}$ (m) | $\lambda_{\text{short}}$ | log-likelihood |
|---|---|---|---|---|---|---|---|
| 0 | 0.250 | 0.250 | 0.250 | 0.250 | 0.300 | 0.50 | −932 |
| 1 | 0.621 | 0.163 | 0.047 | 0.169 | 0.081 | 0.88 | 280 |
| 2 | 0.727 | 0.135 | 0.047 | 0.092 | 0.052 | 1.53 | 445 |
| 60 | 0.733 | 0.150 | 0.047 | 0.070 | 0.051 | 1.75 | 448 |

Random readings below 3 m look exactly like short ones, because there the two shapes overlap, so EM moves some weight between those two causes.

With its numbers learned, the beam model is complete for a laser; other sensors report other kinds of numbers and need models of their own.

## 7. A catalogue of sensor models

> **Key point:** Every sensor needs its own measurement model $p(z \mid x, m)$, the density of its reading $z$ given the pose $x$ and the map $m$, because each reports a different kind of number. Four kinds cover most mobile robots: landmark, range, boundary and odometry sensors.

The **beam model** (G-2377) answers the question of Figure 1 for a laser; it is one entry in a family. A model is needed for every sensor the robot uses, and its shape follows from what the sensor reports. LaValle collects the common kinds (LaValle §11.5.1); Figure 15 draws four of them in our room.

![Four kinds of sensors in the 5 m by 4 m room: a landmark sensor measures range or bearing to a known point; a depth sensor measures distances to the nearest surface along many beams; a boundary sensor says whether the robot touches or is near a wall; an odometry sensor reports how far the wheels say the robot moved](images/catalogue.png)

| Kind | What it reports | Example | Where we model it |
|---|---|---|---|
| **Landmark sensor** (G-2385) | the direction or distance to a known point | a camera sees a coloured pole 3 m away at 37° to the left | [**landmark measurement model**](../RO-012-landmark-measurement-model/RO-012-landmark-measurement-model.md#4-the-landmark-measurement-model) (G-2401) |
| **Depth-mapping sensor** (G-2386) | the distance to the nearest surface along each beam | the laser scan of Figure 1 | this Note and the [**likelihood field**](../RO-011-likelihood-fields-and-scan-matching/RO-011-likelihood-fields-and-scan-matching.md#3-the-likelihood-field-model) (G-2393) |
| **Boundary sensor** (G-2387) | whether the robot touches, or is close to, an obstacle | a bumper, or "within 0.5 m of a wall" | yes/no readings |
| **Odometry sensor** (G-2388) | how far the robot has moved, from its wheel turns | "1.02 m since the last step" | the [**odometry motion model**](../RO-008-probabilistic-motion-models/RO-008-probabilistic-motion-models.md#4-the-odometry-motion-model) (G-2323) |

## 8. Summary

| Part | Density | Why this shape |
|---|---|---|
| measurement noise | Gaussian around the expected range $z^{\ast}$, cut at 0 and at the maximum range $z_{\max}$ (5 m) | small errors scatter symmetrically around the true distance |
| unexpected object | exponential, from 0 up to $z^{\ast}$ | only the first blocker counts, and each extra free stretch is one more condition; nothing behind the wall can block |
| failure | spike at $z_{\max}$ | a lost pulse is reported as the maximum range |
| random | uniform at height $1 / z_{\max}$, 0.2 per m | no reading may ever have density 0 |

- The four readings of Figure 1 are about 215 times more likely from **pose** (G-2280) A than from pose B, even though a person blocks the forward beam, because the beam model lets a short reading cost a pose a factor instead of everything; the six numbers behind that answer can be learned from a thousand readings of one wall.
- A **range finder** (G-2371) reports the distance to the first surface along each beam, so a guessed pose can be tested by ray casting the map to get the expected ranges and comparing.
- The **measurement model** (G-2374) $p(z \mid x, m)$, the density of the readings $z$ given the pose $x$ and the map $m$, scores a pose by how likely the readings are from there; read over poses it is the **likelihood** (G-1086) that a localization filter multiplies into its belief.
- A scan's density is the product of its beams' densities, because once the pose and map are known the beams are nearly independent; the leftover dependence makes the product overconfident, so implementations use a subset of beams.
- A Gaussian alone fails, because one reading caused by a passer-by gets density 0 and the product then rejects the true pose.
- The **beam model** (G-2377) mixes four causes with weights that add up to 1, so a short reading costs a pose a factor instead of everything; in our scan the readings are 215 times more likely from the true pose than from the wrong one.
- The short-reading curve is exponential because the beam stops at the first of many evenly spread blockers, which halves (or shrinks by a fixed factor) the chance with every extra stretch of beam.
- The weights and widths are learned by maximum likelihood from recorded readings; the causes are hidden, so EM alternates responsibilities and weighted refits, and it never lowers the **log-likelihood** (G-1113).
- Each sensor kind (landmark, range, boundary, odometry) needs its own model, because each reports a different kind of number.

Now the robot can score a guessed pose from a laser scan on a grid map, even with a person in the way. Still missing is speed: every guessed pose needs a ray cast per beam, and a filter tries hundreds of poses per scan, so the next step is a [score that looks only at where each beam ends](../RO-011-likelihood-fields-and-scan-matching/RO-011-likelihood-fields-and-scan-matching.md#1-overview).

## 9. Sources

**Built from**

- Cyrill Stachniss, "Observation Models", YouTube, https://www.youtube.com/watch?v=SfwxLpdFB-o (Stachniss, observation models)
- Carlotta A. Berry, PhD, "Advanced Mobile Robotics: Lecture 4-1b - Probabilistic Sensor Models", YouTube, https://www.youtube.com/watch?v=l6Xk37fpQHg (Berry, lecture 4-1b)
- NPTEL - IIT Madras, "#40 Range Finder Measurement Model", *Introduction to Robotics*, YouTube, https://www.youtube.com/watch?v=SwzKOMm1X_I (NPTEL #40)
- Burgard, W. et al., *Introduction to Mobile Robotics*, "Probabilistic Sensor Models" slides, University of Freiburg, http://ais.informatik.uni-freiburg.de/teaching/ss23/robotics/slides/07-sensor-models.pdf (Freiburg slides)
- University of Chicago, CMSC 20600 *Introduction to Robotics*, "Class Meeting 05: Measurement Models for Range Finders", https://classes.cs.uchicago.edu/archive/2025/fall/20600-1/class_meeting_05.html (the beam-model algorithm and the four formulas)
- University of Washington, CSE 571 *Robotics*, "Motion and sensor models" slides, https://courses.cs.washington.edu/courses/cse571/26wi/slides/03-motion-sensor-models.pdf (UW CSE 571 slides: EM for the mixture parameters)
- De Laet, T., De Schutter, J. and Bruyninckx, H. (2008). "A Rigorously Bayesian Beam Model and an Adaptive Full Scan Model for Range Finders in Dynamic Environments". *Journal of Artificial Intelligence Research* 33, 179–222. https://arxiv.org/abs/1401.3432 (§3.6: the assumptions behind the exponential; §4.1 and Algorithm 1: EM for the beam model)
- LaValle, S. M. (2006). *Planning Algorithms*. Cambridge University Press. §11.5.1 "Sensor models". Free online: https://lavalle.pl/planning/node570.html (LaValle)
- Thrun, S., Burgard, W. and Fox, D. (2005). *Probabilistic Robotics*. MIT Press. §6.1–6.3 (measurement models, the beam model, learning its parameters). Cited only for what the free sources above confirm. (Thrun)

**Other references**

- ROS `amcl` package, parameter definitions `AMCL.cfg`, https://github.com/ros-planning/navigation/blob/noetic-devel/amcl/cfg/AMCL.cfg (ROS amcl)
- Cyrill Stachniss's lecture is part of his course on state estimation; the same slides appear in "MSR Course 05: Motion and Sensor Models", YouTube, https://www.youtube.com/watch?v=rjpbE-X23wc

## 10. Key terms

Terms taught in this Note come first; linked terms are recaps, taught in the Note the link opens.

| Term | Meaning |
|---|---|
| Expected range $z^{\ast}$ (G-2375) | The distance a beam would read with a perfect sensor, if the robot were at a given pose in the map; the measurement model compares each real reading with it. |
| Range finder (G-2371) | A sensor that measures the distance to the nearest surface in one direction, for example by timing a laser or sound pulse; robots use it to compare what they see with a map. |
| Range scan (G-2372) | The list of readings from one sweep of a scanning range finder, one distance per beam direction, such as $z = (1.00, 1.97, 2.04, 1.99)$; it is the measurement a laser-based robot tests poses against. |
| Maximum range $z_{\max}$ (G-2373) | The longest distance a range sensor can report, such as 5 m; when no pulse returns, the sensor reports this value, so a reading of $z_{\max}$ usually means a failure, not a wall. |
| Ray casting (G-2376) | Finding the expected range by walking along a beam's direction through the map until the first occupied cell; it turns a guessed pose and a map into the readings the robot should see. |
| Measurement model $p(z \mid x, m)$ (G-2374) | The density of getting sensor readings $z$ if the robot were at pose $x$ in map $m$ (also sensor or observation model); read over poses it is a likelihood that tells a filter which poses fit the readings. |
| Hit part $p_{\text{hit}}$ (measurement noise in the beam model) (G-2378) | The small scatter of a reading around the true distance when the beam does hit the mapped surface; modelled as a Gaussian around $z^{\ast}$ cut to $[0, z_{\max}]$. |
| Normalizer $\eta$ (G-2382) | The factor that rescales a set of numbers, or a density, so that they add up (or integrate) to 1; it is always one over the current total: the sum of the products in the Bayes filter (1/0.4 = 2.5 after a reading in the door world), the area under the cut curve in the beam model (1/0.655 = 1.53). |
| Unexpected object ($p_{\text{short}}$) (G-2379) | Something not in the map, such as a person, that blocks the beam before the mapped surface and gives a short reading; modelled as an exponential from 0 up to $z^{\ast}$, because only the first blocker counts. |
| Max-range reading ($p_{\max}$) (G-2380) | A reading of exactly $z_{\max}$ that a sensor gives when its pulse never returns (glass, black or shiny surfaces, nothing in range); modelled as a spike at $z_{\max}$. |
| Point mass (G-2383) | A distribution that puts all its probability on one value, such as a reading of exactly $z_{\max}$; it has no density height, so code draws it as a very narrow box of area 1. |
| Random measurement ($p_{\text{rand}}$) (G-2381) | A reading with no modelled cause, such as cross-talk or a stray reflection; modelled as a uniform density $1/z_{\max}$ (the uniform part $p_{\text{rand}}$) so that no reading ever has density 0. |
| Beam model (G-2377) | The measurement model of a range finder that mixes four densities for one reading (measurement noise, unexpected objects, failures, random readings) with weights that add up to 1, so no single odd reading can rule out the true pose. |
| Intrinsic parameters (of a sensor model) (G-2384) | The numbers that describe a sensor and its surroundings rather than the pose, such as the beam model's four weights, $\sigma_{\text{hit}}$ and $\lambda_{\text{short}}$; they are learned from recorded readings. |
| Landmark sensor (G-2385) | A sensor that reports the direction or distance to a known point in the world, such as a camera that sees a coloured pole; each kind of report needs its own measurement model. |
| Depth-mapping sensor (G-2386) | A sensor that reports the distance to the nearest surface along each of many directions, such as a laser scanner or a ring of sonars; the beam model describes its readings. |
| Boundary sensor (G-2387) | A sensor that reports whether the robot touches, or is close to, an obstacle, such as a bumper or a proximity sensor; it gives yes/no readings. |
| Odometry sensor (G-2388) | A sensor that reports how far the robot has moved, from counting wheel turns; robots usually feed it into the motion model rather than the measurement model. |
| [Pose](../../../../RO/control/01-robot-models/RO-001-pose-and-differential-drive/RO-001-pose-and-differential-drive.md#22-why-position-is-not-enough-the-heading) (G-2280) | Where a robot is and which way it faces: on a floor, its position $(x, y)$ and heading $\theta$, such as (2 m, 1 m, 30°); needed because a robot at one spot drives off differently depending on its heading. |
| [Location-based map (grid map)](../../../../RO/localization/02-bayes-filters/RO-009-maps-and-landmarks/RO-009-maps-and-landmarks.md#3-feature-based-and-grid-maps) (G-2335) | A map that splits space into cells and stores a value for every cell, occupied or free, free space included (2800 cells for a 7 m by 4 m room at 0.1 m); larger, but it answers at once whether a pose is free. |
| [Measurement $z_t$](../../../../RO/localization/02-bayes-filters/RO-007-why-a-robot-is-never-sure/RO-007-why-a-robot-is-never-sure.md#51-measurements-and-controls) (G-2317) | What a robot's sensors report about the world at time $t$, such as "door", a laser scan or a camera image; it does not change the state but tells the robot something about it, which narrows its distribution. |
| [EM algorithm (expectation maximization)](../../../../MA/08-likelihood/MA-074-expectation-maximization/MA-074-expectation-maximization.md#3-the-two-steps-and-the-algorithm) (G-675) | A method for finding the maximum likelihood when some variables are hidden (latent): it repeats two steps, an E-step and an M-step, until the fit settles. |
| [LiDAR](../../../../DL/01-basics/DL-003-nn-types-history-applications/DL-003-nn-types-history-applications.md#41-mainstream-applications) (G-1083) | A sensor that measures distances to nearby objects with laser light. |
| [Likelihood](../../../../MA/08-likelihood/MA-069-probability-vs-likelihood/MA-069-probability-vs-likelihood.md#22-likelihood-from-the-event-back-to-the-parameter) (G-1086) | How probable the observed data is under given parameter values; read as a function of the parameters with the data fixed. |
| [Bayes filter](../../../../RO/localization/02-bayes-filters/RO-014-bayes-filter/RO-014-bayes-filter.md#44-the-algorithm) (G-2446) | The algorithm that keeps a robot's belief up to date one step at a time: a prediction step after each command and a correction step after each reading; it gives the exact belief without storing the history, under the Markov assumption. |
| [Probability density](../../../../MA/03-distributions/MA-022-pdf-and-continuous-cdf/MA-022-pdf-and-continuous-cdf.md#5-what-the-density-at-a-point-means) (G-1569) | The height of a continuous distribution's curve; compares how likely nearby values are. |
| [Conditional independence](../../../../ML/07-classification/ML-082-naive-bayes-maths/ML-082-naive-bayes-maths.md#5-step-3-the-naive-assumption) (G-443) | Independence that holds once a third variable is known: given the class, knowing one feature tells nothing more about another. Naive Bayes assumes it so it can multiply one probability per feature. |
| [Gaussian distribution](../../../../MA/03-distributions/MA-024-normal-distribution/MA-024-normal-distribution.md#2-what-the-normal-distribution-is) (G-827) | Another name for the normal distribution: the symmetric, bell-shaped continuous distribution set by its mean and standard deviation, used to model many measurements. |
| [Standard deviation of a random variable](../../../../MA/02-probability/MA-012-expected-value-and-variance/MA-012-expected-value-and-variance.md#41-variance-term-by-term) (G-1870) | The square root of a random variable's variance, in the units of $X$; it says how far values typically fall from the expected value. |
| [Truncated normal](../../../../DL/02-training/DL-030-xavier-he-initialization/DL-030-xavier-he-initialization.md#62-with-keras-initialisers) (G-2023) | A normal distribution restricted to a range and rescaled so its area is 1; it keeps its bell shape inside the range. Keras' normal initialisers cut at two standard deviations: values beyond are redrawn. |
| [Exponential distribution](../../../../MA/08-likelihood/MA-071-mle-for-common-distributions/MA-071-mle-for-common-distributions.md#31-the-distribution-of-waiting-times) (G-733) | The pattern of waiting times between random events: short waits are common and long waits rare (a right-skewed continuous distribution). |
| [Uniform distribution](../../../../MA/03-distributions/MA-029-uniform-and-log-normal/MA-029-uniform-and-log-normal.md#2-the-uniform-distribution) (G-2043) | A distribution in which every outcome in a range is equally likely. |
| [Mixture weight $\pi_k$](../../../../MA/08-likelihood/MA-073-gaussian-mixture-models/MA-073-gaussian-mixture-models.md#61-the-formula) (G-1238) | How big a share of a mixture one component $k$ gets; the weights are non-negative and add up to 1. |
| [MLE of a normal distribution](../../../../MA/08-likelihood/MA-071-mle-for-common-distributions/MA-071-mle-for-common-distributions.md#44-the-mle-of-the-standard-deviation) (G-1242) | The normal curve that makes the data most likely: its mean is the sample mean and its variance the average squared distance from that mean (dividing by $n$), $\hat\mu = \bar{x}$ and $\hat\sigma^2 = \sum(x_i - \bar{x})^2/n$. |
| [Maximum likelihood estimation (MLE)](../../../../MA/08-likelihood/MA-070-maximum-likelihood-estimation/MA-070-maximum-likelihood-estimation.md#72-the-maximum-likelihood-estimate) (G-1191) | Fitting parameters by making the likelihood of the observed data as large as possible. |
| [Log-likelihood](../../../../ML/07-classification/ML-072-log-loss/ML-072-log-loss.md#42-taking-logs) (G-1113) | The logarithm of the likelihood, which turns the product of probabilities into a sum of log probabilities; it peaks at the same parameters as the likelihood and is easier to compute and maximise. |
| [Latent variable](../../../../MA/08-likelihood/MA-073-gaussian-mixture-models/MA-073-gaussian-mixture-models.md#52-the-latent-variable) (G-1050) | A variable in a model that is never observed, such as the component that produced a point. |
| [Responsibility $r_{nk}$](../../../../MA/08-likelihood/MA-073-gaussian-mixture-models/MA-073-gaussian-mixture-models.md#32-the-standard-terms) (G-1687) | In a mixture model, how likely it is that component $k$ produced point $n$, given that point (the posterior probability). |
| [E-step](../../../../MA/08-likelihood/MA-074-expectation-maximization/MA-074-expectation-maximization.md#31-the-two-steps) (G-654) | The expectation step of the EM algorithm: using the current parameters, give every point its responsibilities (the probability that it came from each component), a soft assignment that the M-step then uses. |
| [M-step](../../../../MA/08-likelihood/MA-074-expectation-maximization/MA-074-expectation-maximization.md#21-one-round-recalled) (G-1139) | The second step of each EM round (maximisation): with the responsibilities held fixed, re-estimate each component's mean, covariance and weight as responsibility-weighted averages, so the fit to the data improves. |
| [MLE of an exponential rate](../../../../MA/08-likelihood/MA-071-mle-for-common-distributions/MA-071-mle-for-common-distributions.md#33-the-derivation) (G-1243) | The rate of an exponential distribution that makes the observed waiting times most likely: one over their mean, $\hat\lambda = n/\sum x_i = 1/\bar{x}$. |
| [Landmark measurement model](../../../../RO/localization/02-bayes-filters/RO-012-landmark-measurement-model/RO-012-landmark-measurement-model.md#41-two-gaussians-multiplied) (G-2401) | The density of a landmark reading (range, bearing) given a pose and the map: a Gaussian of the range error times a Gaussian of the bearing error, with the errors taken as independent; it scores how well a guessed pose explains what the robot saw. |
| [Likelihood field](../../../../RO/localization/02-bayes-filters/RO-011-likelihood-fields-and-scan-matching/RO-011-likelihood-fields-and-scan-matching.md#42-from-distances-to-the-likelihood-field) (G-2393) | A grid over the map that stores, for each cell, the density of a beam endpoint landing there; computed once from the distance transform, so scoring a pose becomes one look-up per beam. |
| [Odometry motion model](../../../../RO/localization/02-bayes-filters/RO-008-probabilistic-motion-models/RO-008-probabilistic-motion-models.md#4-the-odometry-motion-model) (G-2323) | A motion model that splits the pose change reported by odometry into a first turn, a straight drive and a second turn, and adds independent noise to each, with a standard deviation that grows with the motion; used when wheel encoders exist. |
