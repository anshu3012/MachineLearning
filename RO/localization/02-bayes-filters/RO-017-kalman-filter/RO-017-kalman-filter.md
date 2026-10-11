---
title: "Kalman Filter"
tags: [subject/robotics, area/localization, concept/kalman-filter, concept/kalman-gain, concept/observability]
---

## 1. Overview

> **Key point:** A robot has two noisy ways to know where it is: its commands, which drift, and its sensor, which jumps. The Kalman filter blends them with the weight that makes the result as certain as possible, and it does so one step at a time from two numbers.

![Ten steps of a robot in a corridor: the true position, the jumpy beacon readings, the drifting estimate from the commands alone, and the Kalman filter estimate that follows the truth](images/problem.png)

The [**particle filter**](../RO-016-particle-filter/RO-016-particle-filter.md#46-the-algorithm) (G-2492) lets the robot's [**belief**](../RO-013-belief/RO-013-belief.md#42-the-definition) (G-2433), its probability for each possible position, take any shape, but every particle must be moved and weighed every round. When the belief is a single bell-shaped curve, a [**Gaussian**](../../../../MA/03-distributions/MA-024-normal-distribution/MA-024-normal-distribution.md#2-what-the-normal-distribution-is) (G-827), two numbers carry all of it; this Note builds that filter, the **Kalman filter** (G-2506). It needs a new world. The three doors of the looped corridor give a belief with a peak at each door: three [**modes**](../../../../MA/01-descriptive-stats/MA-005-measures-of-central-tendency/MA-005-measures-of-central-tendency.md#5-mode) (G-1251), so the belief is [**multimodal**](../../../../MA/01-descriptive-stats/MA-005-measures-of-central-tendency/MA-005-measures-of-central-tendency.md#5-mode) (G-1275), and one Gaussian cannot hold it. Here a ceiling beacon reports the position itself, so the belief has a single mode: it is **unimodal** (G-2528).

A delivery robot drives along a straight corridor. Every second it is commanded to move 0.5 m. A ceiling beacon system also reports its position once a second. Neither source is good enough on its own (Figure 1):

- **The commands** give a smooth path, but they **drift**: each step's error is the last step's error plus a new wheel slip, so the error carries over and piles up. Over the ten steps of Figure 1, the commands alone miss the true position by 0.27 m on average (root mean square).
- **The beacon** **jumps**: each reading's error is new, with no memory of the last one, so it never piles up, but it can swing from one side to the other between two seconds. Its readings miss by 0.51 m on average.

Figure 2 runs both sources for 60 steps from a known start. The commands' error moves only a little each step, but the moves add up, and its band of two standard deviations widens like this ([Section 2.4](#24-adding-independent-errors-adds-variances)):

$$2 \times 0.1 \times \sqrt{t}$$

The beacon's error lands somewhere new each step, but its band stays at ±0.8 m. After about 16 steps the commands are the worse source.

![One simulated run of 60 steps from a known start, one frame per step. Top: the errors now, with an arrow from each last value; the commands' error moves a little each step and wanders off, the beacon's lands somewhere new each step, the Kalman filter's stays near zero. Bottom: the errors so far; the commands' band of two standard deviations widens, the beacon's stays at ±0.8 m, the Kalman filter's settles at ±0.38 m](images/drift_jump.gif)

The Kalman filter's estimate misses by 0.17 m, better than either (notebook). In Figure 2 (blue), its error stays near zero, and its band settles at ±0.38 m, half the beacon's, and does not widen. It gets there by asking, at every step, how far to trust each source, and the answer is a number we derive: the Kalman gain. The Note builds the filter on this corridor, one step at a time, in the order of kalmanfilter.net and Becker's book:

- why a Gaussian belief stays Gaussian, so two numbers are enough ([Section 2](#2-why-two-numbers-are-enough-the-linear-gaussian-system));
- the predict step, which carries the drift: the Gaussian moves and widens ([Section 3](#3-predict-the-gaussian-moves-and-widens));
- the update step, which uses the beacon: the gain derived as the weight that makes the variance smallest ([Section 4](#4-update-the-gain-that-makes-the-estimate-most-certain));
- the ten steps of Figure 1 by hand ([Section 5](#5-ten-steps-on-the-corridor));
- the matrix form, which estimates a speed that is never measured, observability, and the filter as the source of the state a controller needs ([Section 6](#6-the-matrix-form-more-than-one-number));
- how to choose the two noise settings, Q and R ([Section 7](#7-choosing-q-and-r)).

## 2. Why two numbers are enough: the linear Gaussian system

> **Key point:** To weigh the drifting commands against the jumping beacon at every step, the filter must carry its belief in a few numbers. If the motion and the sensor are **linear** functions (G-2527) of the state (a fixed multiple of the state plus a constant, $y = ax + b$, whose graph is a straight line) with added Gaussian noise, a Gaussian belief stays Gaussian, so a mean and a variance carry the whole belief.

### 2.1 The Bayes filter in brief

The robot's belief $\text{bel}(x_t)$ is a probability distribution over its position $x_t$ at step $t$. The [**Bayes filter**](../RO-014-bayes-filter/RO-014-bayes-filter.md#44-the-algorithm) (G-2446) updates it in two steps per round:

- **predict** with the command $u_t$, spreading the belief by the motion model $p(x_t \mid u_t, x_{t-1})$;
- **update** with the reading $z_t$, multiplying by the sensor model $p(z_t \mid x_t)$ and rescaling to a total of 1.

For a general belief these steps act on whole curves, which is costly: the [**particle filter**](../RO-016-particle-filter/RO-016-particle-filter.md#3-a-belief-as-a-cloud-of-samples) (G-2492) needs hundreds of samples to store one. The Kalman filter instead uses the case in which the belief is always a Gaussian, which needs no samples at all.

### 2.2 A Gaussian is two numbers

A Gaussian, also called a [normal distribution](../../../../MA/03-distributions/MA-024-normal-distribution/MA-024-normal-distribution.md#3-parameters-and-notation) (G-827), is fixed by its mean (where the peak is) and its variance (how wide it is). If the belief is normal, it is enough to store:

- the estimate $\hat{x}$, the mean, our best single guess;
- its variance $p$, how unsure we are, in m².

The robot's first guess is that it starts at the dock, give or take about 1 m:

$$\hat x_0 = 0 \text{ m}$$

$$p_0 = 1 \text{ m}^2$$

The true start is 0.3 m; the filter does not know that, and this start error is part of the commands' drift. Two numbers are enough only if the predict and update steps keep the belief Gaussian, which the rest of this section checks.

### 2.3 A linear function keeps a Gaussian a Gaussian

> **Key point:** Passing a normal variable through a linear function $y = ax + b$, whose graph is a straight line, gives another normal variable: the mean goes through the line and the variance is multiplied by $a^2$.

The predict step shifts the belief by the command, so we first check what a linear function does to a Gaussian. Take a normal variable $x$ with mean 1 and [**standard deviation**](../../../../MA/01-descriptive-stats/MA-006-measures-of-dispersion/MA-006-measures-of-dispersion.md#5-standard-deviation) (G-1871) 0.5, and the linear function

$$y = 2x + 1$$

Every value of $x$ is stretched by 2 and shifted by 1, so the whole curve is stretched by 2 and shifted by 1. Its shape stays a Gaussian (Figure 3). The mean goes through the line:

$$2 \times 1 + 1 = 3$$

The standard deviation is stretched by the slope:

$$2 \times 0.5 = 1$$

![x with mean 1 and standard deviation 0.5 (top) is passed through the line y = 2x + 1; the result y (right) is a Gaussian with mean 3 and standard deviation 1. Both axes and both density panels use the same scale, so the line rises 2 for every 1 across and the curve of y is twice as wide and half as tall. Histograms of 5000 samples sit on the formula curves](images/linear_gaussian.png)

**Why the mean goes through the line and the variance gets $a^2$.** The mean of $y$ is the average of all the $y$ values, and every $y$ is $2x + 1$. Two samples of $x$, 0.5 and 1.5, have mean 1 and variance 0.25, like $x$ in Figure 3. Through the line they become 2 and 4:

$$\text{mean of } y = \frac{2 + 4}{2}$$

$$= \frac{(2 \times 0.5 + 1) + (2 \times 1.5 + 1)}{2}$$

$$= \frac{2 \times 0.5 + 2 \times 1.5 + 1 + 1}{2}$$

$$= \frac{2 \times (0.5 + 1.5) + 2 \times 1}{2}$$

$$= 2 \times \frac{0.5 + 1.5}{2} + 1$$

$$= 2 \times 1 + 1$$

$$= 3$$

The same steps for any $n$ samples $x_i$ with mean $\mu$, through $y = ax + b$, where $\sum$ means [add up](../../../../MA/01-descriptive-stats/MA-005-measures-of-central-tendency/MA-005-measures-of-central-tendency.md#3-mean):

$$\text{mean of } y = \frac{1}{n}\sum_{i=1}^{n} y_i$$

$$= \frac{1}{n}\sum_{i=1}^{n} (a x_i + b)$$

$$= \frac{1}{n}\Big(\sum_{i=1}^{n} a x_i + \sum_{i=1}^{n} b\Big)$$

$$= \frac{1}{n}\Big(a\sum_{i=1}^{n} x_i + n b\Big)$$

$$= a\thinspace\frac{1}{n}\sum_{i=1}^{n} x_i + b$$

$$= a\mu + b$$

The [variance](../../../../MA/02-probability/MA-012-expected-value-and-variance/MA-012-expected-value-and-variance.md#4-variance-of-a-random-variable) (G-2076) of $y$ is the average squared distance of the $y$ values from their mean, $a\mu + b$:

$$\text{Var}(y) = \frac{1}{n}\sum_{i=1}^{n} \big(y_i - (a\mu + b)\big)^2$$

$$= \frac{1}{n}\sum_{i=1}^{n} (a x_i + b - a\mu - b)^2$$

$$= \frac{1}{n}\sum_{i=1}^{n} (a x_i - a\mu)^2$$

$$= \frac{1}{n}\sum_{i=1}^{n} \big(a\thinspace(x_i - \mu)\big)^2$$

$$= \frac{1}{n}\sum_{i=1}^{n} a^2\thinspace(x_i - \mu)^2$$

$$= a^2\thinspace\frac{1}{n}\sum_{i=1}^{n} (x_i - \mu)^2$$

$$= a^2\thinspace\text{Var}(x)$$

With our numbers:

$$\text{Var}(y) = 4 \times 0.25 = 1$$

The shift $b$ moves the Gaussian without widening it. That the result is still a Gaussian, not some other shape, is a property of the normal distribution (Freiburg KF slides; Labbe ch.4). The command is such a shift, but each step also adds a wheel slip, a second error.

### 2.4 Adding independent errors adds variances

The robot's next position is its present position $x$ plus the commanded 0.5 m plus a random slip $w$. The estimate $\hat{x}$ moves by the same 0.5 m. The error is the true position minus the estimate; call the present one $e$. The next error:

$$(x + 0.5 + w) - (\hat{x} + 0.5)$$

$$= x - \hat{x} + w$$

$$= e + w$$

The present error has mean 0, because the estimate is the mean, and variance $p$ ([Section 2.2](#22-a-gaussian-is-two-numbers)). The slip has mean 0 and does not depend on $e$, so the two errors are independent. Their variances add:

$$\text{Var}(e + w) = \text{Var}(e) + \text{Var}(w)$$

**Why.** Take a present error of 1 m or −1 m and a slip of 0.1 m or −0.1 m, all four pairs equally likely. Square each next error:

$$(1 + 0.1)^2 = 1 + 0.2 + 0.01$$

$$(1 - 0.1)^2 = 1 - 0.2 + 0.01$$

$$(-1 + 0.1)^2 = 1 - 0.2 + 0.01$$

$$(-1 - 0.1)^2 = 1 + 0.2 + 0.01$$

Average the four squares; each +0.2 cancels a −0.2:

$$\text{Var}(e + w) = 1 + 0.01$$

The same in symbols:

$$(e + w)^2 = e^2 + 2ew + w^2$$

Averaged, the $2ew$ parts cancel the same way: whatever $e$ is, the slip is as often negative as positive.

$$\text{Var}(e + w) = \text{Var}(e) + \text{Var}(w)$$

So every slip adds its variance, and the commands' drift grows step by step.

### 2.5 The linear Gaussian system

Sections [2.3](#23-a-linear-function-keeps-a-gaussian-a-gaussian) and [2.4](#24-adding-independent-errors-adds-variances) give the two facts the Kalman filter needs: a linear function keeps a Gaussian a Gaussian, and independent errors add their variances. Both apply to a **linear Gaussian system** (G-2507), a system that meets three conditions (Freiburg KF slides; Thrun §3.2):

1. the next state is a linear function of the state and the command, plus normal noise;
2. the reading is a linear function of the state, plus normal noise;
3. the first [**belief**](../RO-013-belief/RO-013-belief.md#42-the-definition) (G-2433), before any command or reading, is normal.

Our robot meets all three. At step $t$:

- $x_t$ is the robot's true position, in m;
- $u_t$ is the command, 0.5 m forward;
- $w_t$ is the wheel slip, the source of the commands' drift, normal with mean 0 and variance $Q = 0.01$ m² (a standard deviation of 0.1 m);
- $z_t$ is the beacon's reading, in m;
- $v_t$ is the beacon's error, the source of its jumps, normal with mean 0 and variance $R = 0.16$ m² (a standard deviation of 0.4 m).

The next position is the last position plus the command plus the slip:

$$x_t = x_{t-1} + u_t + w_t$$

The reading is the position plus the beacon's error:

$$z_t = x_t + v_t$$

Both are linear with normal noise, which meets conditions 1 and 2. The first belief, mean 0 m and variance 1 m² ([Section 2.2](#22-a-gaussian-is-two-numbers)), is normal, which meets condition 3. So the belief stays Gaussian at every step, and the Kalman filter computes its mean and variance exactly. It is the Bayes filter with nothing approximated (Freiburg KF slides). Its first step, predict, is where the drift enters.

## 3. Predict: the Gaussian moves and widens

> **Key point:** The command moves the estimate; the slip widens it. The predicted variance is the old variance plus the slip's variance $Q$, 0.01 m².

**The idea.** First the drift of Figure 1: why do the commands alone miss by 0.27 m? The robot is commanded 0.5 m, so our best guess moves 0.5 m. But each command adds a slip we cannot see, so we are less sure than before, and the doubt piles up.

**The standard terms.** The random slip the motion adds at each step is the **process noise** (G-2509) (kalmanfilter.net). The estimate before the step's reading is the **predicted estimate** (G-2512), also called the prior or a priori estimate.

**The formulas.** At each step:

- $\hat{x}$ is the estimate after the last step, in m (0 m at the start);
- $p$ is its variance, in m² (1 m² at the start);
- $u$ is the command, 0.5 m;
- $Q$ is the slip's variance, 0.01 m²;
- $\bar{x}$ is the predicted estimate, in m;
- $\bar{p}$ is its variance, in m².

The mean goes through the motion; the variances add ([Section 2.4](#24-adding-independent-errors-adds-variances)):

$$\bar{x} = \hat{x} + u$$

$$\bar{p} = p + Q$$

**Step 1 on the corridor.** From the first guess:

$$\bar x_1 = 0 + 0.5 = 0.5 \text{ m}$$

$$\bar p_1 = 1 + 0.01 = 1.01 \text{ m}^2$$

Frame "step 1: predict" of Figure 7 ([Section 5](#5-ten-steps-on-the-corridor)) shows the Gaussian moving 0.5 m and widening a little.

If the robot drove with no readings at all, the variance would grow by $Q$ every step. After 100 steps:

$$p = 1 + 100 \times 0.01 = 2 \text{ m}^2$$

$$\sqrt{2} = 1.4 \text{ m standard deviation}$$

This is the drift of Figure 1: the commands alone only ever widen the Gaussian, so a beacon reading is needed to pull the variance down.

## 4. Update: the gain that makes the estimate most certain

> **Key point:** The new estimate is a weighted average of the prediction and the reading. The weight on the reading that gives the smallest variance is the Kalman gain $K = \bar{p}/(\bar{p} + R)$, where $\bar{p}$ is the prediction's variance and $R$ the reading's: large when the prediction is unsure, small when the reading is.

### 4.1 Two estimates of one position

The beacon stops the drift but jumps. The update decides how far to follow each reading. After the predict step of step 1, we have two estimates of the same position:

| Source | Value | Variance |
|---|---|---|
| prediction | $\bar x_1 = 0.5$ m | $\bar p_1 = 1.01$ m² |
| beacon reading | $z_1 = 0.82$ m | $R = 0.16$ m² |

The reading's error has a variance $R$, the **measurement noise** (G-2510) variance, which comes from the sensor's datasheet or from a calibration ([Section 7.1](#71-r-measure-the-sensor)).

Neither should be thrown away. A natural blend is a weighted average:

- $z$ is the beacon's reading, in m (0.82 m at step 1);
- $\bar{x}$ is the predicted estimate, in m (0.5 m at step 1);
- $k$ is the weight on the reading, a number from 0 to 1; the prediction gets $1 - k$;
- $\hat{x}$ is the blended estimate, in m.

$$\hat{x} = k\thinspace z + (1 - k)\thinspace\bar{x}$$

Which $k$? Taking $k = 0$ keeps the prediction, $k = 1$ takes the reading, and anything in between mixes them. We want the $k$ that makes the blended estimate as certain as possible: the smallest variance.

### 4.2 The variance of the blend

To find that $k$, we write the blend's variance as a function of $k$. The prediction's error and the reading's error are independent. By [Section 2.3](#23-a-linear-function-keeps-a-gaussian-a-gaussian), scaling an error by $k$ scales its variance by $k^2$; by [Section 2.4](#24-adding-independent-errors-adds-variances), independent variances add:

- $p(k)$ is the variance of the blend for weight $k$, in m²;
- $R$ is the reading's variance, 0.16 m²;
- $\bar{p}$ is the prediction's variance, 1.01 m² at step 1.

$$p(k) = k^2 R + (1 - k)^2\thinspace\bar{p}$$

With our numbers:

$$p(k) = 0.16\thinspace k^2 + 1.01\thinspace(1 - k)^2$$

Figure 4 plots it. At the ends:

$$p(0) = 1.01 \quad \text{(prediction only)}$$

$$p(1) = 0.16 \quad \text{(reading only)}$$

In between, the curve dips below both: mixing two independent estimates beats either one. What is left is to find where the dip is lowest.

![The variance of the blended estimate against the weight on the reading, for the first step: 1.01 at k = 0, 0.16 at k = 1, lowest at k = 0.863 with variance 0.138](images/var_vs_weight.png)

### 4.3 The best weight: the Kalman gain

The lowest point of a smooth curve is where its slope is zero. The [**derivative**](../../../../MA/06-calculus/MA-061-derivatives-of-one-variable/MA-061-derivatives-of-one-variable.md#41-from-secant-to-tangent) (G-595) of $p(k)$, term by term:

$$\frac{dp}{dk} = 2kR - 2(1 - k)\thinspace\bar{p}$$

Set it to zero and divide by 2:

$$kR = (1 - k)\thinspace\bar{p}$$

$$kR + k\bar{p} = \bar{p}$$

$$k = \frac{\bar{p}}{\bar{p} + R}$$

This best weight is the **Kalman gain** (G-2508), written $K$ (kalmanfilter.net; Becker ch.4). For step 1:

$$K_1 = \frac{1.01}{1.01 + 0.16}$$

$$= 1.01 / 1.17 = 0.863$$

The reading gets 86 percent of the say, because our first guess (variance 1.01) was far less certain than the beacon (0.16).

**Checks at easy values** (kalmanfilter.net):

- A perfect sensor, $R = 0$: the top and bottom of the gain are equal, so $K = 1$, and the estimate is the reading.
- A perfect prediction, $\bar{p} = 0$: $K = 0$, and the reading is ignored.
- Equal variances: $K = 0.5$, a plain average.

So $K$ always lies between 0 and 1, and the update always lands between the prediction and the reading.

### 4.4 The updated estimate and its variance

Put $k = K$ into the weighted average and regroup:

$$\hat{x} = Kz + (1 - K)\thinspace\bar{x}$$

$$\hat{x} = \bar{x} + K\thinspace(z - \bar{x})$$

The second form reads: start from the prediction and move a fraction $K$ of the way towards the reading. The gap between the reading and the prediction, $z - \bar{x}$, is the **innovation** (G-2511): the part of the reading the prediction did not expect.

For step 1, the innovation is:

$$z_1 - \bar x_1 = 0.82 - 0.5 = 0.32$$

The updated estimate:

$$\hat x_1 = 0.5 + 0.863 \times 0.32$$

$$= 0.5 + 0.276 = 0.776 \text{ m}$$

The true position is 0.73 m.

**The variance.** Put $k = K$ into $p(k)$. The two weights are:

$$K = \frac{\bar{p}}{\bar{p} + R}$$

$$1 - K = \frac{R}{\bar{p} + R}$$

So the two terms of $p(k)$ are:

$$K^2 R = \frac{\bar{p}^2 R}{(\bar{p} + R)^2}$$

$$(1 - K)^2\thinspace\bar{p} = \frac{R^2\thinspace\bar{p}}{(\bar{p} + R)^2}$$

Add them and take out the shared $\bar{p} R$:

$$p = \frac{\bar{p} R\thinspace(\bar{p} + R)}{(\bar{p} + R)^2}$$

$$= \frac{R}{\bar{p} + R}\thinspace\bar{p}$$

$$= (1 - K)\thinspace\bar{p}$$

(kalmanfilter.net).

For step 1:

$$p_1 = 0.137 \times 1.01 = 0.138 \text{ m}^2$$

the lowest point of Figure 4. The estimate after the reading is the **updated estimate** (G-2513), also called the posterior or a posteriori estimate. Because $1 - K$ is at most 1, an update never makes the filter less sure: one beacon reading has cut the standard deviation from 1 m to 0.37 m.

### 4.5 The same answer from multiplying Gaussians

The gain came from making the variance smallest, not from the Bayes filter. The Bayes filter's update multiplies the predicted belief by the sensor model and rescales, as the [continuous Bayes filter](../RO-014-bayes-filter/RO-014-bayes-filter.md#6-the-same-two-steps-on-a-continuous-position) does. Both are Gaussians here, and the product of two Gaussians is again a Gaussian (Labbe ch.4; Freiburg KF slides), with mean and variance:

$$\text{mean} = \frac{R\thinspace\bar{x} + \bar{p}\thinspace z}{\bar{p} + R}$$

$$\text{variance} = \frac{\bar{p}\thinspace R}{\bar{p} + R}$$

For step 1:

$$\frac{0.16 \times 0.5 + 1.01 \times 0.82}{1.17}$$

$$= 0.908 / 1.17 = 0.776$$

$$\frac{1.01 \times 0.16}{1.17} = 0.138$$

The same numbers as [Section 4.4](#44-the-updated-estimate-and-its-variance): the variance-minimising blend and the Bayes update are one and the same. Figure 5 multiplies the step-1 prediction by readings of different quality. A vague reading ($R = 4$) gives $K = 0.202$ and barely moves the Gaussian; the real beacon ($R = 0.16$) gives $K = 0.863$; a sharp reading ($R = 0.01$) gives $K = 0.990$ and the product sits on the reading. So the measurement noise $R$ sets how far one update follows a reading.

![The step-1 prediction (mean 0.5, variance 1.01) multiplied by a reading at 0.82 whose variance R falls from 4 to 0.01: the product moves from the prediction to the reading and narrows; at R = 0.16 the product has mean 0.776 and variance 0.138](images/combine.gif)

## 5. Ten steps on the corridor

> **Key point:** Predict, then update, every step. The gain starts high, while the first guess is vague, and settles to a fixed value once the variance stops changing.

One step has cut the variance from 1.01 to 0.138 m². The ten steps of Figure 1 are this loop run ten times: predict with the drifting command, update with the jumping reading (Figure 6). The filter keeps only $\hat{x}$ and $p$ from one step to the next: it never stores the past readings, yet its estimate uses all of them (kalmanfilter.net; Labbe ch.4).

![The one-dimensional Kalman filter as a loop: predict moves the mean by u and adds Q to the variance; update computes K, moves the mean a fraction K towards the reading and multiplies the variance by 1 − K](images/kf_cycle.png)

**Step 1** is Sections [3](#3-predict-the-gaussian-moves-and-widens) and [4](#4-update-the-gain-that-makes-the-estimate-most-certain): prediction 0.5 m (variance 1.01), reading 0.82 m, gain 0.863, estimate 0.776 m (variance 0.138).

**Step 2.** Predict from step 1's estimate:

$$\bar x_2 = 0.776 + 0.5 = 1.276$$

$$\bar p_2 = 0.138 + 0.01 = 0.148$$

The reading is $z_2 = 1.85$ m. The gain:

$$K_2 = 0.148 / (0.148 + 0.16)$$

$$= 0.148 / 0.308 = 0.481$$

The prediction is now about as certain as the reading, so the gain is near one half. The innovation:

$$z_2 - \bar x_2 = 1.85 - 1.276 = 0.574$$

The update:

$$\hat x_2 = 1.276 + 0.481 \times 0.574$$

$$= 1.276 + 0.276 = 1.552 \text{ m}$$

$$p_2 = 0.519 \times 0.148 = 0.077 \text{ m}^2$$

The true position is 1.22 m. The reading 1.85 m was 0.63 m too high, and the filter followed it only halfway.

**Steps 3 to 10** (notebook):

| Step | $\bar{x}$ | $\bar{p}$ | $K$ | $z$ | $\hat{x}$ | $p$ | True |
|---|---|---|---|---|---|---|---|
| 1 | 0.500 | 1.010 | 0.863 | 0.82 | 0.776 | 0.138 | 0.73 |
| 2 | 1.276 | 0.148 | 0.481 | 1.85 | 1.552 | 0.077 | 1.22 |
| 3 | 2.052 | 0.087 | 0.352 | 2.01 | 2.037 | 0.056 | 1.88 |
| 4 | 2.537 | 0.066 | 0.293 | 2.65 | 2.570 | 0.047 | 2.45 |
| 5 | 3.070 | 0.057 | 0.262 | 2.19 | 2.839 | 0.042 | 2.79 |
| 6 | 3.339 | 0.052 | 0.245 | 4.18 | 3.545 | 0.039 | 3.28 |
| 7 | 4.045 | 0.049 | 0.235 | 2.95 | 3.788 | 0.038 | 3.72 |
| 8 | 4.288 | 0.048 | 0.230 | 4.68 | 4.378 | 0.037 | 4.24 |
| 9 | 4.878 | 0.047 | 0.226 | 4.45 | 4.781 | 0.036 | 4.58 |
| 10 | 5.281 | 0.046 | 0.224 | 4.75 | 5.162 | 0.036 | 5.10 |

Variances are in m², positions in m.

![The first five steps, one stage per frame: the predicted Gaussian moves 0.5 m and widens, the reading's Gaussian arrives, and the updated Gaussian lies between them and is narrower; the dotted line is the true position](images/kf_iterations.gif)

What to see in Figures 6 and 7:

- **The gain falls, then settles.** Each update shrinks the variance, and each prediction adds back only $Q = 0.01$. After a few steps the two balance: the variance before each reading settles near 0.046 and the gain near 0.22 (0.2207 in the long run, notebook). The filter has stopped learning about its start and now trusts each reading about a fifth. The fixed value the gain approaches is the **steady-state gain** (G-2518).
- **The jumps are damped.** The beacon's step-6 reading jumped 0.9 m too high; the estimate moved only 0.21 m towards it, because the gain was 0.245.
- **The band is consistent.** The shaded band in Figure 8 is the estimate plus and minus two standard deviations; the true position stays inside it at every step, a first sign that the filter's variance matches its real errors, which is what makes a [**consistent** filter](../RO-018-extended-kalman-filter/RO-018-extended-kalman-filter.md#51-why-we-need-a-check) (G-2524).

![Top: true position, readings and the estimate with a band of two standard deviations. Bottom: the gain falls from 0.86 at step 1 to 0.22 at step 10](images/kf_run.png)

Over the ten steps, the commands alone miss by 0.27 m, the beacon by 0.51 m, the filter by 0.17 m (notebook). That solves the opening problem for a state of one number, the position, moved by a known command.

## 6. The matrix form: more than one number

> **Key point:** With a state of several numbers, the variance becomes a covariance matrix and the same five lines become matrix lines. The covariance between position and speed lets a position reading correct a speed that is never measured.

### 6.1 Why a vector state: the hidden speed

So far the commands told the filter how far the robot moved, 0.5 m per step, drift and all. Suppose instead we do not know the robot's speed, only that it drives roughly steadily: a person is pushing a trolley, or the odometry is unreliable. We still want the speed, for example because a speed controller needs it ([Section 6.6](#66-the-state-a-controller-needs-the-filter-as-an-observer)), but nothing measures it.

We put the speed into the state. The state is now a vector (a list of numbers) with two entries:

$$\mathbf{x} = \begin{bmatrix} \text{position} \cr\text{speed} \end{bmatrix}$$

Its uncertainty is a 2 × 2 [covariance matrix](../../../../ML/05-dimensionality/ML-047-pca-step-by-step/ML-047-pca-step-by-step.md#33-the-covariance-matrix) (G-495) $P$: the variances of position and speed on the diagonal, and their covariance off it. The belief is a [multivariate normal distribution](../../../../MA/08-likelihood/MA-073-gaussian-mixture-models/MA-073-gaussian-mixture-models.md#71-the-multivariate-normal) (G-1283), the Gaussian for several numbers at once, with mean $\hat{\mathbf{x}}$ and covariance $P$. The motion and the reading must now act on this vector, as matrices.

### 6.2 The model as matrices

**Motion.** With steps of 1 s, the position grows by the speed and the speed stays as it is, plus noise. As a matrix times the state:

$$\mathbf x_t = F\thinspace\mathbf x_{t-1} + \mathbf w_t$$

$$F = \begin{bmatrix} 1 & 1 \cr0 & 1 \end{bmatrix}$$

The first row gives position plus speed; the second gives speed. $F$ is the **state transition matrix** (G-2514); this choice of $F$ is the constant-velocity model (Labbe ch.6). The noise $\mathbf w_t$ has covariance

$$Q = \begin{bmatrix} 0.01 & 0 \cr0 & 0.001 \end{bmatrix}$$

a position slip of 0.1 m and a speed change of about 0.03 m/s per step.

**Reading.** The beacon reads position, not speed:

$$z_t = H\thinspace\mathbf x_t + v_t$$

$$H = \begin{bmatrix} 1 & 0 \end{bmatrix}$$

$H$ is the **measurement matrix** (G-2515): it picks out of the state what the sensor sees. The measurement noise is the same, $R = 0.16$. With $F$ and $H$ in hand, the filter's lines can be rewritten for matrices.

### 6.3 The five lines in matrix form

Each line is the one-dimensional line with numbers replaced by matrices (Labbe ch.6; kalmanfilter.net; Freiburg KF slides); the gain's denominator gets its own row and name, $S$. The [transpose](../../../../ML/05-dimensionality/ML-047-pca-step-by-step/ML-047-pca-step-by-step.md#21-projecting-one-point) (G-2012) $F^{\mathsf T}$ flips a matrix over its diagonal, and $S^{-1}$ is the [inverse](../../../../ML/06-regression/ML-053-multiple-lr-maths/ML-053-multiple-lr-maths.md#6-the-normal-equation) (G-968), here simply 1 divided by the number $S$.

| Step | One number | Matrix form |
|---|---|---|
| predict mean | $\bar{x} = \hat{x} + u$ | $\bar{\mathbf{x}} = F\thinspace\hat{\mathbf{x}}$ |
| predict variance | $\bar{p} = p + Q$ | $\bar{P} = F P F^{\mathsf T} + Q$ |
| innovation variance | $\bar{p} + R$ | $S = H \bar{P} H^{\mathsf T} + R$ |
| gain | $K = \bar{p} / (\bar{p} + R)$ | $K = \bar{P} H^{\mathsf T} S^{-1}$ |
| update mean | $\hat{x} = \bar{x} + K(z - \bar{x})$ | $\hat{\mathbf{x}} = \bar{\mathbf{x}} + K(z - H\bar{\mathbf{x}})$ |
| update variance | $p = (1 - K)\thinspace\bar{p}$ | $P = (I - KH)\thinspace\bar{P}$ |

The only new piece is $F P F^{\mathsf T}$. It is the matrix version of [Section 2.3](#23-a-linear-function-keeps-a-gaussian-a-gaussian)'s rule "variance times slope squared": a linear map $F$ turns a covariance $P$ into $F P F^{\mathsf T}$ (Labbe ch.6). The matrix gain is derived the same way as in [Section 4.3](#43-the-best-weight-the-kalman-gain), by making the updated variances as small as possible (Labbe ch.7, "Deriving the Kalman gain equation").

### 6.4 One step in matrix form, and the speed nobody measured

We run one step of these lines on the corridor's first reading. Start at position 0, speed 0, both with variance 1 and no covariance:

$$\hat{\mathbf x_0} = \begin{bmatrix} 0 \cr0 \end{bmatrix}$$

$$P_0 = \begin{bmatrix} 1 & 0 \cr0 & 1 \end{bmatrix}$$

**Predict.** The mean stays at zero. $P_0$ is the identity matrix, so $F P_0 F^{\mathsf T}$ is $F F^{\mathsf T}$. Each entry is a row of $F$ times a row of $F$:

$$\text{top left: } 1 \times 1 + 1 \times 1 = 2$$

$$\text{off-diagonal: } 1 \times 0 + 1 \times 1 = 1$$

$$\text{bottom right: } 0 \times 0 + 1 \times 1 = 1$$

$$F P_0 F^{\mathsf T} = \begin{bmatrix} 2 & 1 \cr1 & 1 \end{bmatrix}$$

$$\bar P_1 = \begin{bmatrix} 2.01 & 1 \cr1 & 1.001 \end{bmatrix}$$

The position variance has grown from 1 to 2.01, because an unknown speed adds an unknown distance. The off-diagonal 1 is new: the prediction now links the two errors. If the robot is further along than predicted, it was probably faster.

**Update** with the first reading $z_1 = 0.82$:

$$S = 2.01 + 0.16 = 2.17$$

$H = [1, 0]$ picks the first column of $\bar P_1$, so $\bar P_1 H^{\mathsf T} = (2.01, 1)$, and dividing by $S$ gives the gain:

$$K = \begin{bmatrix} 2.01 / 2.17 \cr1 / 2.17 \end{bmatrix}$$

$$= \begin{bmatrix} 0.926 \cr0.461 \end{bmatrix}$$

The prediction was 0, so the innovation is the whole reading, 0.82. The new state:

$$0.926 \times 0.82 = 0.760$$

$$0.461 \times 0.82 = 0.378$$

$$\hat{\mathbf x_1} = \begin{bmatrix} 0.760 \cr0.378 \end{bmatrix}$$

One position reading has given a speed estimate of 0.378 m/s. The gain's second entry is the covariance divided by $S$: through the link in $\bar{P}$, a position innovation becomes a speed correction.

Figure 9 runs the same ten jumping beacon readings. The speed estimate swings at first, then settles: after step 10 it is 0.421 m/s with a standard deviation of 0.081 m/s, against the robot's true average speed of 0.48 m/s, inside one standard deviation (notebook). A quantity that no sensor measures has been estimated from how the measured one changes, which kalmanfilter.net and Labbe ch.6 call the strength of the multivariate filter.

![The two-variable filter fed only position readings. Left: position estimate, readings and truth with a band of two standard deviations. Right: the speed estimate, never measured, settles near the true average of 0.48 m/s while its band narrows](images/cv_speed.png)

### 6.5 Observability: can the readings pin down the state?

Could we do the same with a speed sensor and no position sensor? No. Every position, shifted by the same amount, gives exactly the same speed readings, so no number of speed readings can tell where the robot is.

A system is **observable** (G-2517) if its whole state can be worked out from its readings (and commands) over time (FBS §8.1). Figure 10 shows what a speed sensor alone does to the filter: with the speed sensor, the variance of the position estimate grows every step, to 2.68 m² after ten steps; with the position sensor it falls to 0.066 m² (notebook). A Kalman filter on an unobservable system runs without error messages but cannot shrink the uncertainty in the hidden direction, so checking observability comes before building the filter.

![Variance of the position estimate over ten steps: with a position sensor it stays small and ends at 0.066; with only a speed sensor it grows steadily to 2.68](images/observability.png)

### 6.6 The state a controller needs: the filter as an observer

The speed estimate of [Section 6.4](#64-one-step-in-matrix-form-and-the-speed-nobody-measured) is what a controller needs. A controller that holds the robot at 0.5 m/s must know the speed; one that stops it at a door must know the position. Many controllers need the whole state, but sensors give only part of it (FBS §8.1). Something must rebuild the missing parts.

The obvious attempt is to run the model alone, with no readings: each step, multiply the last estimate by $F$. That is dead reckoning: any error in the start or in the model is never corrected. The fix is feedback: compare the reading with what the estimate predicts, and correct the estimate by a gain times the gap,

$$\hat{\mathbf{x}} = \bar{\mathbf{x}} + L\thinspace(z - H\bar{\mathbf{x}})$$

A model run alongside the real system and corrected this way is a **state observer** (G-2516) (FBS §8.2). The size of the gain $L$ is a trade-off: a large gain corrects errors fast but passes the sensor's noise straight into the estimate (FBS §8.2). The Kalman filter is the observer whose gain, $L = K$, is the best compromise for the given noises (FBS §8.2). The controller then uses $\hat{\mathbf{x}}$ in place of the true state (FBS §8.3), which is why the Kalman filter sits between the sensors and the controller in most robots. Every gain so far rested on two noise settings we were simply given, $Q$ and $R$.

## 7. Choosing Q and R

> **Key point:** The measurement noise $R$ is the variance of the beacon's jumps and is measured; the process noise $Q$ is how far each command can drift from the model and is tuned. Only their ratio changes the estimates.

### 7.1 R: measure the sensor

The measurement noise $R$ is the variance of the beacon's error, the jumps of Figure 1, so it can be measured: put the robot on a mark at a known position and record many readings (kalmanfilter.net). We parked the robot at exactly 2.00 m and took 100 readings (`data/beacon_calibration.csv`):

$$\text{mean} = 2.018 \text{ m}$$

$$\text{sample variance} = 0.134 \text{ m}^2$$

The datasheet value is 0.16 m². Sensor datasheets are the other source of $R$ (kalmanfilter.net). The mean, 2.018 m, also shows no sizeable bias, which matters because the Kalman filter assumes the noise has mean zero.

### 7.2 Q: tune the motion noise

$Q$ is harder: it covers everything the motion model leaves out (slips, pushes, a wheel radius slightly wrong), so there is no datasheet for it, and it is set by tuning against data (Labbe ch.8). Each wrong choice fails in its own way. We simulated 2000 runs of 50 steps in which the true slip variance is 0.01, and ran three filters on them (Figure 11):

| Filter's $Q$ | Gain it settles to | Error (RMSE, steps 11–50) | What goes wrong |
|---|---|---|---|
| 0.0001 (too small) | 0.10 at step 10, falling | 0.305 m | trusts the commands, ignores readings, drifts with the slips |
| 0.01 (right) | 0.22 | 0.187 m | none |
| 1 (too big) | 0.88 | 0.353 m | trusts each reading, copies its noise |

The readings alone give 0.399 m. Too small a $Q$ trusts the commands and drifts like them; too large a $Q$ follows every jump of the beacon (Labbe ch.4, "Incorrect process variance"; kalmanfilter.net, where a too-small $Q$ causes a lag error).

![Error of three filters on one 50-step run; the legend gives each filter's RMSE over all 2000 runs. Q = 0.0001 lags below the truth for long stretches; Q = 1 jumps with every reading; Q = 0.01 stays closest to zero](images/tuning.png)

**Only the ratio matters.** Multiply $Q$, $R$ and the first variance all by 10: every gain $\bar{p}/(\bar{p} + R)$ has a 10 on top and below, so the gains and the estimates are the same; the notebook finds a largest difference of exactly 0. What a filter designer really chooses is how much the model is trusted relative to the sensor.

**How to tell when it is wrong without knowing the truth.** On a real robot the truth is unknown, but the innovations are not: a well-tuned filter's innovations look like random noise of the size its own $S$ predicts. Testing them is the [consistency check](../RO-018-extended-kalman-filter/RO-018-extended-kalman-filter.md#5-consistency-is-the-filter-telling-the-truth-about-itself) on the innovations.

## 8. Summary

| Line | Formula | Why |
|---|---|---|
| predict mean | $\bar{x} = \hat{x} + u$ | the command moves the robot |
| predict variance | $\bar{p} = p + Q$ | independent slip variances add |
| gain | $K = \bar{p}/(\bar{p} + R)$ | the weight that makes the blended variance smallest |
| update mean | $\hat{x} = \bar{x} + K(z - \bar{x})$ | move a fraction $K$ of the way to the reading |
| update variance | $p = (1 - K)\thinspace\bar{p}$ | blending two independent estimates beats either |

- The corridor robot's two poor sources make one good one: the filter misses by 0.17 m against 0.27 m for the drifting commands and 0.51 m for the jumping beacon, because at every step the gain gives each source the trust its variance earns.
- In a linear Gaussian system the belief stays Gaussian, because a linear function keeps a Gaussian a Gaussian and independent variances add, so a mean and a variance carry the whole belief.
- The predict step widens the Gaussian by $Q$, so the commands alone always drift: after 100 steps the standard deviation would be 1.4 m.
- The Kalman gain is derived, not chosen: it is the weight on the reading that minimises the updated variance, and it equals the Bayes update of two multiplied Gaussians (0.776 m and 0.138 m² at step 1 either way).
- The gain is high while the estimate is vague (0.863 at step 1) and settles near 0.22 once prediction and reading balance, so the beacon's jumps are damped.
- In matrix form the covariance links position and speed, so position readings estimate a speed nobody measures (0.421 m/s against a true 0.48 m/s).
- Observability decides what readings can pin down: position readings give both variables, speed readings never give the position, whose variance grows to 2.68 m².
- The Kalman filter is the observer with the best gain for the given noises, so it supplies the full state a controller needs from partial sensors.
- $R$ is measured from the sensor, $Q$ is tuned; too small a $Q$ drifts like the commands, too large a $Q$ follows every jump, and only the ratio matters.

The robot can now blend drifting commands and jumping readings with two numbers per step. Still missing: the filter needs linear models, and a range beacon's reading is a nonlinear function of the position (its graph is a curve), which the [**extended Kalman filter**](../RO-018-extended-kalman-filter/RO-018-extended-kalman-filter.md#1-overview) (G-2520) straightens.

## 9. Sources

**Built from**

- MATLAB, "Understanding Kalman Filters, Part 2: State Observers", YouTube, https://www.youtube.com/watch?v=4OerJmPpkRg
- MATLAB, "Understanding Kalman Filters, Part 3: Optimal State Estimator", YouTube, https://www.youtube.com/watch?v=ul3u2yLPwU0
- MATLAB, "Understanding Kalman Filters, Part 4: Optimal State Estimator Algorithm", YouTube, https://www.youtube.com/watch?v=VFXf1lIZ3p8
- Lars Hammarstrand (Chalmers), "4.3.3 Kalman filter tuning and consistency: motion and measurement models", YouTube, https://www.youtube.com/watch?v=WroIS3pPfjM
- Steve Brunton, "Control Bootcamp: Observability", YouTube, https://www.youtube.com/watch?v=iRZmJBcg1ZA
- Becker, A. *Kalman Filter from the Ground Up*, and its free tutorial pages: "Kalman Filter in one dimension" https://www.kalmanfilter.net/kalman1d.html, "Adding process noise" https://www.kalmanfilter.net/kalman1d_pn.html, "Multivariate Kalman Filter" https://www.kalmanfilter.net/kalmanmulti.html (kalmanfilter.net 1D, process noise, multivariate; Becker ch.4)
- Labbe, R. *Kalman and Bayesian Filters in Python*, ch.4 "One Dimensional Kalman Filters", ch.6 "Multivariate Kalman Filters", ch.7 "Kalman Filter Math", ch.8 "Designing Kalman Filters", https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python (Labbe ch.4, ch.6, ch.7, ch.8)
- Åström, K. J. and Murray, R. M. (2021). *Feedback Systems*, 2nd ed., ch.8 "Output Feedback", §8.1 Observability, §8.2 State estimation, §8.3 Control using estimated state. Free: https://fbswiki.org (FBS)
- Burgard, W. et al. (Uni Freiburg), *Introduction to Mobile Robotics*, "Bayes Filter – Kalman Filter" slides, http://ais.informatik.uni-freiburg.de/teaching/ss23/robotics/slides/10-kalman.pdf (Freiburg KF slides)

**Other references**

- NPTEL-NOC IITM, "Introduction to Robotics, #33 Kalman Filter", YouTube, https://www.youtube.com/watch?v=E9QL8XWJIh8
- Thrun, S., Burgard, W. and Fox, D. (2005). *Probabilistic Robotics*. MIT Press. §3.2 "The Kalman Filter"; cited for what the Freiburg slides confirm (Thrun)

## 10. Key terms

Terms taught in this Note come first; linked terms are recaps, taught in the Note the link opens.

| Term | Meaning |
|---|---|
| Kalman filter (G-2506) | The Bayes filter for a linear Gaussian system: it keeps the belief as a mean and a (co)variance and updates them with a predict step and an update step, blending a model's prediction with a sensor reading so the result is as certain as possible. |
| Unimodal (G-2528) | Having a single mode (one peak); a unimodal belief can be held by one Gaussian, so the Kalman filter needs only its mean and variance. |
| Linear function (G-2527) | A function $y = ax + b$: a fixed multiple of the input plus a constant, whose graph is a straight line; passing a normal variable through it gives another normal variable, which is why the Kalman filter is exact for linear models. |
| Linear Gaussian system (G-2507) | A system whose next state and whose readings are linear functions of the state plus normal noise, starting from a normal belief; in it the belief stays normal, so the Kalman filter is exact. |
| Process noise $Q$ (G-2509) | The random part of the motion the model leaves out (wheel slip, pushes), given as its variance or covariance $Q$; it widens the belief at every predict step and is usually set by tuning. |
| Predicted estimate (a priori) (G-2512) | The estimate and its variance after the predict step and before the step's reading, $\bar{x}$ and $\bar{p}$; it says what the model alone expects. |
| Measurement noise $R$ (G-2510) | The random error of a sensor reading, given as its variance or covariance $R$; it sets how much the filter trusts each reading and is taken from the datasheet or measured in a calibration. |
| Kalman gain $K$ (G-2508) | The weight the update gives to the reading, $K = \bar{p}/(\bar{p} + R)$ in one dimension: the weight that makes the updated variance smallest, near 1 when the prediction is vague and near 0 when the reading is. |
| Innovation (G-2511) | The gap between a reading and the reading the prediction expected, $z - H\bar{x}$; the update moves the estimate by the gain times this gap, and its size is used to check the filter. |
| Updated estimate (a posteriori) (G-2513) | The estimate and its variance after the reading has been blended in, $\hat{x}$ and $p$; it is the filter's output for the step and the start of the next. |
| Steady-state gain (G-2518) | The fixed value the Kalman gain settles to once the variance added by each prediction balances the variance removed by each update, such as 0.22 for $Q = 0.01$ and $R = 0.16$. |
| State transition matrix $F$ (G-2514) | The matrix that carries the state one step forward in a linear model, such as $F = [[1, 1], [0, 1]]$ for position and speed with 1 s steps (position plus speed, speed unchanged). |
| Measurement matrix $H$ (G-2515) | The matrix that turns the state into the reading the sensor should give, such as $H = [1, 0]$ for a sensor that sees position but not speed. |
| Observability (G-2517) | Whether a system's whole state can be worked out from its readings and commands over time; a filter needs it before it can pin down every state variable. |
| State observer (G-2516) | A model run alongside the real system and corrected by a gain times the gap between the measured and the predicted reading, so it rebuilds states no sensor measures for a controller to use; the Kalman filter is the observer with the best gain for the given noises. |
| [Particle filter](../../../../RO/localization/02-bayes-filters/RO-016-particle-filter/RO-016-particle-filter.md#4-the-particle-filter-step-by-step) (G-2492) | A Bayes filter that stores the belief as a set of weighted samples (particles) and runs each round as move, weigh, resample; it can hold beliefs of any shape, such as a belief with three modes, one at each of three doors. |
| [Belief](../../../../RO/localization/02-bayes-filters/RO-013-belief/RO-013-belief.md#42-the-definition) (G-2433) | The robot's probability for each possible state given all its commands and readings, $\text{bel}(x_t) = p(x_t \mid z_{1:t}, u_{1:t})$; a short summary of the history that says how strongly the evidence points to each state. |
| [Gaussian distribution](../../../../MA/03-distributions/MA-024-normal-distribution/MA-024-normal-distribution.md#2-what-the-normal-distribution-is) (G-827) | Another name for the normal distribution: the symmetric, bell-shaped continuous distribution set by its mean and standard deviation, used to model many measurements. |
| [Mode](../../../../MA/01-descriptive-stats/MA-005-measures-of-central-tendency/MA-005-measures-of-central-tendency.md#5-mode) (G-1251) | The value that appears most often in the data, so it sits under the highest peak of a histogram or a distribution curve; it gives a centre for data that are not numbers, and a belief with several peaks has several modes. |
| [Multimodal](../../../../MA/01-descriptive-stats/MA-005-measures-of-central-tendency/MA-005-measures-of-central-tendency.md#5-mode) (G-1275) | Having more than one mode (two modes: bimodal). |
| [Bayes filter](../../../../RO/localization/02-bayes-filters/RO-014-bayes-filter/RO-014-bayes-filter.md#44-the-algorithm) (G-2446) | The algorithm that keeps a robot's belief up to date one step at a time: a prediction step after each command and a correction step after each reading; it gives the exact belief without storing the history, under the Markov assumption. |
| [Standard deviation](../../../../ML/02-getting-data/ML-018-understanding-your-data/ML-018-understanding-your-data.md#71-count-mean-standard-deviation-minimum-and-maximum) (G-1871) | How far values typically lie from the mean; divide by $n - 1$ for a sample (pandas default) or by $n$ for a population (NumPy default). |
| [Variance of a random variable](../../../../MA/02-probability/MA-012-expected-value-and-variance/MA-012-expected-value-and-variance.md#4-variance-of-a-random-variable) (G-2076) | How spread out a random variable's values are: the expected squared distance from its expected value, $\mathrm{Var}(X) = E[(X - E[X])^2]$. |
| [Derivative](../../../../MA/06-calculus/MA-061-derivatives-of-one-variable/MA-061-derivatives-of-one-variable.md#41-from-secant-to-tangent) (G-595) | The slope of a function at a point: how fast the output changes as the input changes there. It is zero at the lowest point of a smooth curve, which is how training finds a minimum. |
| [Consistent filter](../../../../RO/localization/02-bayes-filters/RO-018-extended-kalman-filter/RO-018-extended-kalman-filter.md#51-why-we-need-a-check) (G-2524) | A filter whose real errors are as large as its own reported covariance says, on average; only then can its uncertainty be trusted by a controller or planner. |
| [Covariance matrix](../../../../ML/05-dimensionality/ML-047-pca-step-by-step/ML-047-pca-step-by-step.md#33-the-covariance-matrix) (G-495) | A square table with every feature's variance on the diagonal and every pair's covariance off it, so it sums up how the data spreads and which features move together; PCA takes its eigenvectors. |
| [Multivariate normal distribution](../../../../MA/08-likelihood/MA-073-gaussian-mixture-models/MA-073-gaussian-mixture-models.md#71-the-multivariate-normal) (G-1283) | The bell-shaped (normal) distribution for several numbers at once, a vector; it is set by a mean vector (its centre) and a covariance matrix (its spread and how the numbers vary together). |
| [Transpose](../../../../ML/06-regression/ML-053-multiple-lr-maths/ML-053-multiple-lr-maths.md#41-two-rules-about-transposes) (G-2012) | A matrix or vector with rows and columns swapped; it turns a column vector $u$ into a row $u^{\mathsf T}$, so $u^{\mathsf T}x$ is the dot product. |
| [Inverse matrix](../../../../ML/06-regression/ML-053-multiple-lr-maths/ML-053-multiple-lr-maths.md#6-the-normal-equation) (G-968) | The matrix that undoes another: their product is the identity matrix. |
| [Extended Kalman filter (EKF)](../../../../RO/localization/02-bayes-filters/RO-018-extended-kalman-filter/RO-018-extended-kalman-filter.md#41-the-algorithm) (G-2520) | The Kalman filter for nonlinear motion and sensor models: it moves the mean through the nonlinear functions and uses their Jacobians at the latest estimate in place of $F$ and $H$, so it can track unimodal beliefs through nonlinear models. |
