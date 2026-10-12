---
title: "Grid Filters: Histogram Filter and Binary Bayes Filter"
tags: [subject/robotics, area/localization, concept/histogram-filter, concept/binary-bayes-filter, concept/hidden-markov-model]
---

## 1. Overview

> **Key point:** Chop the robot's space into cells and keep one probability per cell: the Bayes filter then becomes plain arithmetic on a list of numbers. The same list of numbers also answers two questions about the past: where the robot most likely was, and which whole path it most likely took.

![A hallway of 10 cells, numbered 0 to 9 and joined into a loop, with doors in front of cells 1, 3 and 7; a robot stands in cell 1 and does not know it](images/hallway.png)

The robot can now update its belief from the newest command and reading alone, with the [**Bayes filter**](../RO-014-bayes-filter/RO-014-bayes-filter.md#44-the-algorithm) (G-2446). What still breaks is its prediction step, a sum over **every** possible previous state. In the [door world](../RO-014-bayes-filter/RO-014-bayes-filter.md#2-the-door-world) that sum had 2 terms; a position along the hallway can be any number of metres, so the sum has infinitely many terms and cannot be done as written. This Note adds one number per cell, and answers: **how does a computer run the Bayes filter, and what else can the same numbers tell us?**

We go back to the hallway (Figure 1) on which the robot's [**belief**](../RO-013-belief/RO-013-belief.md#42-the-definition) (G-2433), its probability for every cell, was defined, with the same numbers:

- 10 cells of 1 m in a loop, with doors at cells 1, 3 and 7;
- a door sensor that reads "door" with probability 0.6 at a door and 0.2 at a wall;
- a command "move 2" that moves the robot 1, 2 or 3 cells with probability 0.1, 0.8 and 0.1.

The Note covers:

- the **histogram filter** (G-2461): one probability per cell, updated by multiplying (sensing) and sliding (moving) ([Section 2](#2-the-histogram-filter));
- how to cut a real, continuous space into cells: fixed cells or cells that adapt to the belief ([Section 3](#3-cutting-a-real-space-into-cells));
- the binary Bayes filter for a yes-or-no state that does not change, run in [**log odds**](../../../../ML/08-trees-and-ensembles/ML-116-gradient-boosting-classification/ML-116-gradient-boosting-classification.md#4-stage-1-the-log-odds-of-class-1) (G-1116), the logarithm of the yes-to-no odds ([Section 4](#4-the-binary-bayes-filter));
- looking back: the smoothed belief at an earlier time, and the most likely whole path ([Section 5](#5-looking-back-smoothing-and-the-most-likely-path)).

## 2. The histogram filter

> **Key point:** Keep one probability per cell: sensing multiplies every cell by how well it explains the reading, then rescales. Moving slides the list along and blurs it with the motion probabilities.

### 2.1 Why cells

A continuous position, such as "3.42 m along the hallway", can take infinitely many values, and a computer can only store a finite list. So we cut the hallway into cells, here 10 cells of 1 m, and keep one probability for each: the probability that the robot is somewhere in that cell. Cutting a range into cells is the same move as [discretization](../../../../ML/03-feature-engineering/ML-031-binning-binarization/ML-031-binning-binarization.md#3-discretization) (G-619) of a feature into bins, and the list of probabilities, drawn as bars, is a [histogram](../../../../ML/02-getting-data/ML-019-univariate-analysis/ML-019-univariate-analysis.md#6-histogram) (G-899) of the **belief** (G-2433).

The **Bayes filter** (G-2446) run on such a list of cells is the **histogram filter** (G-2461) (PR §4.1). When the states are finite to begin with, as in the door world, the same algorithm is called the discrete Bayes filter (Labbe ch.2). The sum of the prediction step now has only 10 terms, so it can be done exactly.

### 2.2 Sense: multiply, then rescale

The robot has no idea where it is, so each cell starts at 0.1. It reads "door". Figure 2 runs the four stages in turn: watch each bar shrink as it is multiplied by its cell's chance of a "door" reading, the 10 products stack up to 0.32, and the division by 0.32 grow them back until they add to 1, with each door cell now three times as tall as a wall cell.

![The hallway's 10 cells, with the doors at cells 1, 3 and 7 shaded. The bars start at 0.1, the prior. Each bar is multiplied by p(door | cell), the chance of reading door in that cell (0.6 at a door, 0.2 at a wall), and shrinks to 0.06 or 0.02. The 10 products stack one by one into the sum column, which reaches 0.32. Dividing every product by 0.32 grows them to 0.1875 at the doors and 0.0625 at the walls. Last frame: the new belief, with the prior 0.1 as a dashed line](images/sense_anim.gif)

**Multiply** each cell by the probability of the reading in that cell:

$$\text{door cell: } 0.1 \times 0.6 = 0.06$$

$$\text{wall cell: } 0.1 \times 0.2 = 0.02$$

**Add** the 10 products, 3 door cells and 7 wall cells:

$$3 \times 0.06 + 7 \times 0.02 = 0.32$$

**Rescale** by dividing every product by 0.32, so the cells add to 1 again:

$$\text{door cell: } 0.06 / 0.32 = 0.1875$$

$$\text{wall cell: } 0.02 / 0.32 = 0.0625$$

Multiplying and rescaling is the correction step of the Bayes filter, done cell by cell (Labbe ch.2). The robot reads "door" three times as often at a door as at a wall, and after the update each door cell holds three times the **belief** (G-2433) of a wall cell.

### 2.3 Move: shift, then blur

Next the robot moves 2 cells. If the move were exact, every probability would simply travel 2 cells to the right, wrapping round the loop (Figure 3, middle). But the move is 1 cell with probability 0.1 and 3 cells with probability 0.1, so some **belief** (G-2433) also lands one cell short or one cell too far (Figure 3, right).

![Left: the belief after reading door, 0.1875 at cells 1, 3 and 7. Middle: shifted exactly 2 cells, 0.1875 at cells 3, 5 and 9. Right: shifted and blurred by the 0.1/0.8/0.1 move, 0.1625 at cells 3, 5 and 9 and 0.0875 at cell 4](images/move_step.png)

Which old cells can end in cell 3? Cell 2 (by moving 1), cell 1 (by moving 2) and cell 0 (by moving 3). Each contributes its old belief times the probability of that move:

$$\text{new cell 3} = 0.1 \times 0.0625$$

$$+\ 0.8 \times 0.1875$$

$$+\ 0.1 \times 0.0625$$

$$= 0.1625$$

Adding up the weighted old cells is the prediction step of the **Bayes filter** (G-2446): the [law of total probability](../../../../MA/02-probability/MA-019-bayes-problem/MA-019-bayes-problem.md#4-the-evidence-total-probability) (G-1053) with three terms instead of ten, because only three old cells can reach each new one.

Every new cell is built the same way, with the same three weights, slid along the hallway. Figure 4 builds the whole predicted belief this way, one cell at a time.

![Top: the old belief with the three cells that can reach the new cell highlighted and weighted 0.1, 0.8 and 0.1. Bottom: the new belief filled in cell by cell; new cell 3 = 0.1 x 0.0625 + 0.8 x 0.1875 + 0.1 x 0.0625 = 0.1625](images/convolution.gif)

The list of weights, here (0.1, 0.8, 0.1), is the **motion kernel** (G-2462). Sliding a small list of weights along a longer list and adding the products at each position is a [convolution](../../../../DL/04-cnn/DL-042-convolution-operation/DL-042-convolution-operation.md#41-a-moving-average) (G-481), the same operation a CNN filter performs on an image (Labbe ch.2). Convolution is valid here because the move's error does not depend on where the robot is: the same kernel applies in every cell.

### 2.4 Moving without looking loses everything

What if the robot keeps moving and never reads its sensor? Figure 5 starts it sure that it is in cell 1 and repeats "move 2".

![After 1 move the highest cell holds 0.80, after 3 moves 0.56, after 10 moves 0.29, after 80 moves 0.11: the belief flattens towards 0.1 in every cell](images/lose_info.gif)

Each move spreads the **belief** (G-2433) of every cell over three cells, so the highest cell's belief shrinks:

| Moves without a reading | 0 | 1 | 3 | 10 | 80 |
|---|---|---|---|---|---|
| Highest cell | 1.00 | 0.80 | 0.56 | 0.29 | 0.11 |

The belief tends to 0.1 in every cell, where the robot started before it knew anything. A prediction can only lose information; only readings bring it back (Labbe ch.2).

### 2.5 Sense and move together

A real robot alternates: move, read, move, read. Figure 6 runs seven steps; $t$ counts them from 1 to 7. The true robot starts in cell 1 and really moves 2 cells each time (cells 1, 3, 5, 7, 9, 1, 3). Every reading is correct except at $t = 5$, where the sensor says "door" in front of the wall of cell 9.

![Seven steps of the histogram filter: orange frames show the predicted belief after each move, blue frames the belief after each reading; the tallest bar follows the true cell except at t = 5, after the wrong reading, when it jumps to cell 3; at t = 6 and t = 7 it is back on the true cell](images/hist_filter.gif)

The tallest bar at each step:

| $t$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| True cell | 1 | 3 | 5 | 7 | 9 | 1 | 3 |
| Tallest bar | 1, 3, 7 (tied) | 3 | 5 | 7 | 3 | 1 | 3 |
| Its belief | 0.19 | 0.31 | 0.30 | 0.42 | 0.32 | 0.37 | 0.47 |

The wrong reading at $t = 5$ moves the tallest bar to cell 3, a door. But the true cell 9 keeps a **belief** (G-2433) of 0.24, because one reading never sets a cell to zero. Two correct readings later the filter is back on the true cell with 0.47. A filter that kept only one best guess would have been lost at $t = 5$ (Labbe ch.2).

### 2.6 The formal version

With the cells numbered 0 to 9, at time step $t$:

- $k$ is the number of a cell after the move, 0 to 9;
- $i$ is the number of a cell before the move, 0 to 9;
- $p_{i,t-1}$ is the **belief** (G-2433) in cell $i$ one step earlier, a number from 0 to 1 (0.1875 for cell 1 after the first reading);
- $p(x_k \mid u_t,\ x_i)$ is the chance that the command $u_t$ takes the robot from cell $i$ to cell $k$ (0.8 for "move 2" from cell 1 to cell 3);
- $\bar p_{k,t}$ is the predicted belief in cell $k$, after the move and before the reading (0.1625 for cell 3 at $t = 2$);
- $p(z_t \mid x_k)$ is the chance of the reading $z_t$ when the robot is in cell $k$ (0.6 for "door" at a door, 0.2 at a wall);
- $\eta$ is the factor that rescales the cells so they add to 1, one over the sum of the products (the sum is 0.32 after the first reading, [Section 2.2](#22-sense-multiply-then-rescale));
- $p_{k,t}$ is the belief in cell $k$ at time $t$, a number from 0 to 1 (0.3095 for cell 3 at $t = 2$).

The **histogram filter** (G-2461) is (PR §4.1.1):

$$\bar p_{k,t} = \sum_{i} p(x_k \mid u_t,\ x_i)\ p_{i,t-1}$$

$$p_{k,t} = \eta\ p(z_t \mid x_k)\ \bar p_{k,t}$$

The first line is the prediction step with the sum over the old cells $i$; the second is the correction step. Both lines visit every cell, so one step costs a fixed amount of work per cell.

> **Python:** the hallway filter, using `np.roll` to shift a list round the loop.
> ```python
> import numpy as np
> door = np.isin(np.arange(10), [1, 3, 7])
> def sense(bel, z):           # z = True: reads "door"
>     p = np.where(door, 0.6, 0.2)
>     if not z:
>         p = 1 - p
>     return p * bel / (p * bel).sum()
> def move(bel):               # 1, 2 or 3 cells
>     return (0.1 * np.roll(bel, 1)
>             + 0.8 * np.roll(bel, 2)
>             + 0.1 * np.roll(bel, 3))
> bel = sense(np.full(10, 0.1), True)   # 0.1875 at doors
> bel = sense(move(bel), True)          # 0.3095 at cell 3
> ```

The notebook `RO-015-grid-filters.ipynb` runs every example in this Note. Ten cells of 1 m make the sum exact on the hallway, but they place the robot only to the nearest metre.

## 3. Cutting a real space into cells

> **Key point:** Fine cells give an accurate **belief** (G-2433), the robot's probability for each cell, but their number explodes with the size of the space and the number of state variables. A static decomposition fixes the cells in advance; an adaptive one makes cells small only where the belief needs them.

### 3.1 Why the number of cells explodes

Cells turned the sum over infinitely many positions into 10 terms, at a price: with cells of 1 m, the robot's position is never known better than "somewhere in this metre". Smaller cells give a sharper answer, but every cell costs memory and time, because both steps visit every cell. A real floor robot has a pose, its position and heading (see [**pose**](../../../control/01-robot-models/RO-001-pose-and-differential-drive/RO-001-pose-and-differential-drive.md#22-why-position-is-not-enough-the-heading) (G-2280)), so the grid has three directions. On a 30 m by 30 m floor (Fox 1999):

- the position along the floor runs from 0 to 30 m in cells of 15 cm;
- the position across the floor runs from 0 to 30 m in cells of 15 cm;
- the heading, the direction the robot faces, runs from 0° to 360° in steps of 2°.

Counting the cells:

$$\frac{30}{0.15} = 200 \text{ cells along the floor}$$

$$\frac{30}{0.15} = 200 \text{ cells across the floor}$$

$$\frac{360}{2} = 180 \text{ headings}$$

$$200 \times 200 \times 180 = 7{,}200{,}000 \text{ cells}$$

Halving the cell size multiplies the count by 4 for the position alone, and each extra state variable, such as speed, multiplies it again by the number of its values (Labbe ch.2). Fox, Burgard and Thrun found that updating 7.2 million cells at every reading was too slow for the computers of 1999 (Fox 1999).

### 3.2 Static and adaptive decomposition

Most of those millions of cells hold a **belief** (G-2433) close to zero: the robot is not inside a wall or at the far end of the building. Two ways of cutting the space follow from that (PR §4.1.4):

- A **static decomposition** (G-2464) fixes the cells before the robot starts, whatever the belief turns out to be. A regular grid of equal cells is the usual choice (Fox 1999). A fixed grid is simple, and every cell is updated the same way, but it spends as much work on empty regions as on the region where the robot is.
- An **adaptive decomposition** (G-2465), also called a dynamic decomposition, changes the cells as the belief changes: small cells where the belief is high, large cells where it is near zero. A common way is a quadtree, which splits a square into four only where more detail is needed (ShanghaiTech slides; Fox 1999, §6).

![Left: an 8 m by 8 m floor cut into 64 fixed 1 m cells, with the belief concentrated in one spot. Right: the same floor cut adaptively into 19 cells: 4 m cells where the belief is near zero, down to 0.5 m cells at the peak](images/decomposition.png)

Figure 7 compares the two on an 8 m by 8 m floor. The fixed grid uses 64 cells of 1 m. The adaptive one uses 19 cells, yet its smallest cells (0.5 m) are finer than the fixed grid's where the belief peaks. The price is bookkeeping: cells must be split and merged as the belief moves. The smallest grid of all has just 2 cells.

## 4. The binary Bayes filter

> **Key point:** For a yes-or-no state that never changes, each reading multiplies the odds by a fixed factor. In **log odds** (G-1116), the logarithm of the odds, that becomes adding a fixed number, which is fast and does not round to 0 or 1.

### 4.1 A state that does not change

The smallest grid has 2 cells, open and closed. Go back to the [door world](../RO-014-bayes-filter/RO-014-bayes-filter.md#2-the-door-world), but now nobody touches the door: it is open or closed, and it stays that way while the robot reads its sensor again and again. A state that the robot's commands do not change is a **static state** (G-2467) (PR §4.2). With a static state the prediction step does nothing (the **belief** (G-2433), the robot's probability for each door state, before a step equals the belief after it), so only the correction step is left.

The same situation appears in mapping: whether one small square of the floor is occupied by an obstacle is a yes-or-no question about something that does not move. A map built this way keeps one such filter per square (PR §4.2; Freiburg mapping slides).

### 4.2 Each reading multiplies the odds

The [odds](../../../../ML/08-trees-and-ensembles/ML-116-gradient-boosting-classification/ML-116-gradient-boosting-classification.md#4-stage-1-the-log-odds-of-class-1) (G-1376) of the door being open compare the two possibilities. In symbols:

- $p(\text{open})$ is the probability that the door is open, 0.5 at the start;
- $p(\text{closed})$ is the probability that it is closed, 0.5 at the start.

The odds are their ratio:

$$\text{odds} = \frac{p(\text{open})}{p(\text{closed})}$$

Why does a reading multiply the odds? [**Bayes' theorem**](../../../../MA/02-probability/MA-018-bayes-theorem/MA-018-bayes-theorem.md#4-the-formula-and-its-proof) (G-269) gives each door state's probability after a reading, with the same denominator for both: the overall chance of the reading. For one "sense open" from 0.5, the sensor reads it with chance 0.6 at an open door, 0.2 at a closed one and [0.4 overall](../RO-014-bayes-filter/RO-014-bayes-filter.md#31-why-the-robot-needs-bayes-theorem):

$$\text{open: } \frac{0.6 \times 0.5}{0.4} = 0.75$$

$$\text{closed: } \frac{0.2 \times 0.5}{0.4} = 0.25$$

$$\text{new odds} = \frac{0.75}{0.25}$$

$$= \frac{0.6 \times 0.5}{0.4} \div \frac{0.2 \times 0.5}{0.4}$$

$$= \frac{0.6 \times 0.5}{0.2 \times 0.5}$$

$$= \frac{0.6}{0.2} \times \frac{0.5}{0.5}$$

$$= 3 \times 1 = 3$$

The same steps for any reading:

- $z$ is the reading, "sense open" or "sense closed";
- $p(z \mid \text{open})$ is the chance of that reading when the door is open (0.6 for "sense open");
- $p(z \mid \text{closed})$ is the chance of that reading when the door is closed (0.2 for "sense open");
- $p(z)$ is the overall chance of the reading, the same denominator in both lines (0.4 for "sense open");
- $p(\text{open} \mid z)$ is the probability that the door is open after the reading (0.75 after one "sense open" from 0.5);
- $p(\text{closed} \mid z)$ is the probability that it is closed after the reading (0.25 after one "sense open" from 0.5).

$$p(\text{open} \mid z) = \frac{p(z \mid \text{open})\ p(\text{open})}{p(z)}$$

$$p(\text{closed} \mid z) = \frac{p(z \mid \text{closed})\ p(\text{closed})}{p(z)}$$

$$\text{new odds} = \frac{p(\text{open} \mid z)}{p(\text{closed} \mid z)}$$

$$= \frac{p(z \mid \text{open})\ p(\text{open})}{p(z)}$$

$$\div\ \frac{p(z \mid \text{closed})\ p(\text{closed})}{p(z)}$$

$$= \frac{p(z \mid \text{open})\ p(\text{open})}{p(z \mid \text{closed})\ p(\text{closed})}$$

$$= \frac{p(z \mid \text{open})}{p(z \mid \text{closed})} \times \frac{p(\text{open})}{p(\text{closed})}$$

The first fraction, the ratio of the two measurement probabilities, is the [Bayes factor](../../../../MA/02-probability/MA-019-bayes-problem/MA-019-bayes-problem.md#61-the-size-of-the-update-the-bayes-factor) (G-2215); the second is the old odds:

$$\text{new odds} = \text{old odds} \times \frac{p(z \mid \text{open})}{p(z \mid \text{closed})}$$

We never need $p(z)$, whose inverse is the normaliser $\eta$ of the correction step, which is why odds are convenient.

The factor is 3 for "sense open", as above. For "sense closed" it is:

$$0.4 / 0.8 = 0.5$$

Starting from odds of 1 (that is, 0.5 against 0.5), two readings of "open" give:

$$1 \times 3 \times 3 = 9$$

Odds of 9 mean 9 parts open to 1 part closed:

$$p(\text{open}) = \frac{9}{9 + 1} = 0.9$$

the same 0.9 as in the [**Bayes filter**](../RO-014-bayes-filter/RO-014-bayes-filter.md#32-a-second-reading-bayes-theorem-with-background-knowledge) (G-2446).

### 4.3 Log odds turn the products into sums

Taking the logarithm turns a product into a sum. The natural log of the **odds** (G-1376) is the [log odds](../../../../ML/08-trees-and-ensembles/ML-116-gradient-boosting-classification/ML-116-gradient-boosting-classification.md#4-stage-1-the-log-odds-of-class-1) (G-1116). In symbols:

- $p$ is the probability that the door is open, a number from 0 to 1 (0.5 at the start);
- $1 - p$ is the probability that it is closed;
- $\ln$ is the natural logarithm;
- $l$ is the log odds, a number with no unit that can be any size (0 at the start).

Written out:

$$l = \ln \frac{p}{1 - p}$$

Figure 8 shows how probabilities map to log odds: 0.5 goes to 0, probabilities above 0.5 to positive numbers, below 0.5 to negative ones, and 0 and 1 are never reached.

![The curve from log odds to probability: p = 0.5 at l = 0, p = 0.75 at l = 1.10, p = 0.9 at l = 2.20, p = 0.33 at l = -0.69; the curve flattens towards 0 and 1 but never reaches them](images/logodds.png)

Each reading now **adds** a fixed amount:

$$\text{sense open: } \ln 3 = +1.0986$$

$$\text{sense closed: } \ln 0.5 = -0.6931$$

Figure 9 runs five readings: open, open, closed, open, open.

![Left: the log odds as a stack of blocks, +1.0986 for each sense open and -0.6931 for the sense closed, reaching 1.0986, 2.1972, 1.5041, 2.6027 and 3.7013. Right: the matching probability that the door is open, 0.75, 0.90, 0.818, 0.931 and 0.976](images/binary_door.gif)

Step by step, the log odds $l$ after each reading:

$$\text{open: } l = 0 + 1.0986 = 1.0986$$

$$\text{open: } l = 1.0986 + 1.0986 = 2.1972$$

$$\text{closed: } l = 2.1972 - 0.6931 = 1.5041$$

$$\text{open: } l = 1.5041 + 1.0986 = 2.6027$$

$$\text{open: } l = 2.6027 + 1.0986 = 3.7013$$

To read a probability back out, undo the log, which is the [sigmoid function](../../../../ML/07-classification/ML-071-sigmoid-function/ML-071-sigmoid-function.md#4-the-sigmoid-function) (G-1798); $e$, about 2.718, is the base of the natural log:

$$p = 1 - \frac{1}{1 + e^{l}}$$

$$l = 3.7013: \quad p = 0.976$$

The notebook checks that Bayes' theorem applied five times gives the same 0.976.

This filter, a static binary state updated in log odds, is the **binary Bayes filter** (G-2466) (PR §4.2).

### 4.4 Why work in log odds

Two reasons:

1. **Adding is cheaper than multiplying and rescaling.** A map can hold millions of cells, each updated at every scan; one addition per cell is the cheapest update possible, and every cell can be updated at the same time (Freiburg mapping slides: the **log odds** (G-1116) update "only requires to compute sums").
2. **Probabilities near 0 or 1 round off.** Run 40 readings of "open" in ordinary probabilities. The **odds** (G-1376) become 3 to the power 40, about 12 billion billion, and the computer stores $p(\text{open})$ as exactly 1.0. After that, a reading of "closed" changes nothing, because 1.0 times anything, divided by itself, is still 1.0. In log odds the same run reaches 43.94, and a "closed" reading moves it to 43.25, as it should. The notebook shows both.

Figure 10 runs both, one reading at a time. Watch the stored probability creep towards 1 until, at reading 34, it is stored as exactly 1.0 and stops moving; the log odds keep climbing to 43.94 and still drop to 43.25 at the "closed" reading.

![Left: the probability that the door is open, updated by Bayes' theorem in ordinary probabilities after each of 40 readings of open, with every digit the computer keeps; from reading 34 on it is stored as exactly 1.0 (orange dots), and a 41st reading, closed, leaves it at 1.0. Right: the log odds l, the natural log of the odds, which climb by ln 3 = 1.0986 per reading to 43.94 and drop by 0.69 to 43.25 at the closed reading](images/round_off.gif)

Every filter so far answers where the robot is now; the same numbers can also say where it was.

## 5. Looking back: smoothing and the most likely path

> **Key point:** Later readings also say where the robot was earlier. The forward-backward algorithm combines readings from before and after a time step into the smoothed **belief** (G-2433), the probability of each cell at that earlier time; the Viterbi algorithm finds the single most likely path.

### 5.1 Three questions about a run

Now the second half of the opening question: what else the same cell probabilities tell us. Take the hallway robot's [run of three steps](../RO-013-belief/RO-013-belief.md#21-why-the-true-cell-is-out-of-reach), the run that first built its **belief** (G-2433), its probability for every cell: at time step $t = 1$ it stays and reads "door"; at $t = 2$ it moves 2 and reads "door"; at $t = 3$ it moves 2 and reads "wall". Its true cells are 1, 3 and 5. The [**hidden Markov model**](../RO-013-belief/RO-013-belief.md#63-hidden-markov-model) (G-2439) of the robot, hidden cells that each produce a reading we can see, can answer three different questions (CS188 §8.2–8.3; J&M App. A):

1. **Where is the robot now, given the readings so far?** This is **filtering** (G-2469); the **histogram filter** (G-2461) of [Section 2](#2-the-histogram-filter) does it.
2. **Where was the robot at an earlier time, given all readings, including later ones?** This is **smoothing** (G-2470).
3. **Which whole path of cells is most likely, given all readings?** This is the **most likely path** (G-2476), found by the **Viterbi algorithm** (G-2474).

Filtering is what a robot needs while it drives. Smoothing and the most likely path are for looking back over a recorded run, for example to draw the path it took.

### 5.2 Smoothing with the forward-backward algorithm

At $t = 1$ the filter knew only the first reading, so cells 1, 3 and 7 were equally likely (Figure 11, blue bars). Later readings settle it. A robot at cell 3 at $t = 1$ would be at cell 5 at $t = 2$, a wall, and would have read "door" there only 20 percent of the time. A robot at cell 1 would be at cell 3, a door. So the reading at $t = 2$ points back to cell 1.

The **forward-backward algorithm** (G-2471) makes this exact. The algorithm combines two quantities for every cell $x$ and time $t$ (J&M App. A):

- the **forward probability** (G-2472) $\alpha_t(x)$: the probability of the readings up to $t$ and of being in cell $x$ at $t$. It is the **histogram filter** (G-2461) before rescaling; at $t = 1$ it is 0.06 at the doors and 0.02 at the walls ([Section 2.2](#22-sense-multiply-then-rescale));
- the **backward probability** (G-2473) $\beta_t(x)$: the probability of the readings **after** $t$, given cell $x$ at $t$. It is computed from the end backwards, starting from 1 at the last step; for cell 1 at $t = 1$ it is 0.4144 (worked below).

Figure 11 computes both for the run, with one column of the 10 cells for each time step. Watch $\alpha$ fill in from left to right and $\beta$ from right to left, then the column $t = 1$ being multiplied and rescaled: the belief in cell 1 rises from 0.19 to 0.36.

![Left: the three time steps as columns of the 10 cells; each box holds alpha, the forward probability (orange, left), and beta, the backward probability (purple, right). Alpha fills in from left to right: 0.06 at the doors and 0.02 at the walls at t = 1, 0.0312 for cell 3 at t = 2. Beta fills in from right to left: 1 at t = 3, 0.8 for cell 3 at t = 2, 0.4144 for cell 1 and 0.1072 for cell 3 at t = 1; coloured lines show the moves used. Then alpha times beta in each cell of t = 1 is divided by their total, 0.06896. Right: the belief at t = 1, filtered from the first reading only (blue, 0.19 at cells 1, 3 and 7) and, in the last frame, smoothed from all three readings (purple, 0.36 at cell 1, 0.09 at cells 3 and 7)](images/fwd_bwd_anim.gif)

So $\alpha$ carries the evidence from the past, $\beta$ from the future. Their product, rescaled to add to 1, is the smoothed **belief** (G-2433). In symbols:

- $\eta$ is the factor that rescales the products so they add to 1, one over their total over all cells (the total is 0.06896);
- $\gamma_t(x)$ is the smoothed belief in cell $x$ at time $t$, a number from 0 to 1 (0.36 for cell 1 at $t = 1$).

Written out:

$$\gamma_t(x) = \eta\ \alpha_t(x)\ \beta_t(x)$$

**$\beta$ for cell 1 at $t = 1$**, worked backwards. At $t = 3$ there are no later readings, so $\beta_3 = 1$ everywhere. One step back, from cell 3 at $t = 2$ the robot reaches cell 4, 5 or 6 (all walls), and each reads "wall" with probability 0.8:

$$\beta_2(3) = 0.1 \times 0.8 + 0.8 \times 0.8$$

$$+\ 0.1 \times 0.8 = 0.8$$

Another step back, from cell 1 at $t = 1$ the robot reaches cell 2 (a wall), 3 (a door) or 4 (a wall), and must then read "door" and continue. $\beta_2(2)$ is worked like $\beta_2(3)$: from cell 2 the robot reaches cell 3 (a door, reads "wall" with probability 0.4), 4 or 5 (walls):

$$\beta_2(2) = 0.1 \times 0.4 + 0.8 \times 0.8$$

$$+\ 0.1 \times 0.8 = 0.76$$

$\beta_2(4) = 0.76$ the same way (notebook). Then:

$$\beta_1(1) = 0.1 \times 0.2 \times 0.76$$

$$+\ 0.8 \times 0.6 \times 0.8$$

$$+\ 0.1 \times 0.2 \times 0.76$$

$$= 0.4144$$

The same calculation for cell 3 gives only 0.1072, because a robot there would read "door" at a wall.

Why does a plain product work? The steps use two facts:

- the [**Markov property**](../RO-007-why-a-robot-is-never-sure/RO-007-why-a-robot-is-never-sure.md#43-complete-state-and-the-markov-property) (G-2316): once the cell at a time step is known, the earlier readings tell nothing more about the later ones;
- the [**multiplication rule**](../../../../MA/02-probability/MA-015-conditional-probability/MA-015-conditional-probability.md#5-the-multiplication-rule) (G-2212): the chance of one event times the chance of a second event given the first is the chance of both.

For cell 1 at $t = 1$:

$$\alpha_1(1)\ \beta_1(1) = 0.06 \times 0.4144$$

$$= 0.0249$$

The same steps for any cell and time step:

- $t$ is the time step, 1 above;
- $x$ is the cell, 1 above;
- $T$ is the last time step, 3 in our run;
- $z_{1:t}$ is the readings from time 1 to $t$, only "door" at $t = 1$;
- $z_{t+1:T}$ is the readings after $t$, ("door", "wall") at $t = 1$;
- $z_{1:T}$ is all readings of the run, ("door", "door", "wall");
- $x_t = x$ means that the robot is in cell $x$ at time $t$;
- a comma inside $p(\ldots)$ means "and".

$$\alpha_t(x)\ \beta_t(x)$$

$$= p(z_{1:t},\ x_t = x)$$

$$\quad \times\ p(z_{t+1:T} \mid x_t = x)$$

$$= p(z_{1:t},\ x_t = x)$$

$$\quad \times\ p(z_{t+1:T} \mid x_t = x,\ z_{1:t})$$

$$= p(z_{1:T},\ x_t = x)$$

Cell 3 the same way:

$$\alpha_1(3)\ \beta_1(3) = 0.06 \times 0.1072 = 0.0064$$

The products over all 10 cells add to 0.06896, the probability of the three readings; it is the same at every $t$, which the notebook checks. Dividing each product by it gives the probability of its cell given all three readings, the smoothed belief (J&M App. A):

$$\gamma_1(1) = 0.0249 / 0.06896 = 0.36$$

$$\gamma_1(3) = 0.0064 / 0.06896 = 0.09$$

The last frame of Figure 11 compares the two: the blue bars are the filtered belief, the purple bars the smoothed one. Using the later readings nearly doubles the belief in the true starting cell, from 0.19 to 0.36.

### 5.3 The most likely path: the Viterbi algorithm

**Smoothing** (G-2470) gives a probability for each cell at each time. Sometimes we want one answer instead: the single path of cells that best explains all readings. Trying every path is hopeless for long runs: with 10 cells and $T$ steps there are 10 to the power $T$ paths, 1000 for our 3 steps but a 1 followed by 100 zeros for 100 steps (J&M App. A).

The **Viterbi algorithm** (G-2474) avoids this with one observation: the best path to a cell at time $t$ must continue the best path to some cell at time $t - 1$. So for each cell it keeps only the probability of the best path ending there, and which cell that path came from, the **back-pointer** (G-2477) (CS188 §8.3). For each cell $x$ at time $t$:

- $x'$ is a cell at time $t - 1$, where the path may come from;
- $m_{t-1}(x')$ is the probability of the best path ending in cell $x'$ at time $t - 1$ (0.06 at a door and 0.02 at a wall at $t = 1$);
- $p(x \mid u_t, x')$ is the chance that the command $u_t$ takes the robot from cell $x'$ to cell $x$ (0.8 for "move 2" from cell 1 to cell 3);
- $\max_{x'}$ keeps the largest value over all cells $x'$;
- $p(z_t \mid x)$ is the chance of the reading $z_t$ in cell $x$ (0.6 for "door" at cell 3);
- $m_t(x)$ is the probability of the best path ending in cell $x$ at time $t$ (0.0288 for cell 3 at $t = 2$).

The update is the **histogram filter** (G-2461) of [Section 2.6](#26-the-formal-version) without the rescaling, with the sum replaced by a maximum:

$$m_t(x) = p(z_t \mid x)$$

$$\times \max_{x'} p(x \mid u_t, x')\ m_{t-1}(x')$$

Storing each sub-answer once and reusing it is [dynamic programming](../../../../DL/01-basics/DL-019-mlp-memoization/DL-019-mlp-memoization.md#33-the-memoized-version) (G-652).

**At $t = 2$, cell 3.** The best path into cell 3 comes from cell 1, cell 2 or cell 0, and $m_1$ is 0.06 at a door and 0.02 at a wall:

$$\text{from cell 1: } 0.8 \times 0.06 = 0.048$$

$$\text{from cell 2: } 0.1 \times 0.02 = 0.002$$

$$\text{from cell 0: } 0.1 \times 0.02 = 0.002$$

The best is from cell 1, so the back-pointer of cell 3 at $t = 2$ is cell 1, and:

$$m_2(3) = 0.6 \times 0.048 = 0.0288$$

This 0.0288 is the probability of the best path into cell 3, which is the robot's true path: cell 1, then cell 3.

**At $t = 3$, cell 5.** The best way in is from cell 3 at $t = 2$:

$$m_3(5) = 0.8 \times 0.8 \times 0.0288 = 0.0184$$

![A trellis: time t = 1, 2, 3 across, cells 0 to 9 down. Each node shows the probability of the best path ending there and a grey line to its best predecessor. The largest value at t = 3 is 0.0184 at cell 5; following the back-pointers gives the red path 1, 3, 5](images/viterbi.gif)

Figure 12 draws all 30 values on a **trellis** (G-2475): one column of cells per time step, with lines for the possible moves between columns. Cell 5 has the largest value at $t = 3$. Following its back-pointer gives cell 3 at $t = 2$, and cell 3's back-pointer gives cell 1 at $t = 1$:

$$\text{most likely path: } 1 \rightarrow 3 \rightarrow 5$$

These are the true cells. The notebook checks all 1000 paths by brute force and finds the same path with the same probability, 0.0184. The Viterbi algorithm needed only 100 comparisons (10 possible earlier cells for each of the 10 cells) for each of the two steps after the first:

$$2 \times 10 \times 10 = 200$$

against 1000 paths; for 100 steps it needs 10,000 against 10 to the power 100 (J&M App. A).

## 6. Summary

| Method | Answers | One step | Cost |
|---|---|---|---|
| Histogram filter | where the robot is now | slide and blur (predict), multiply and rescale (correct) | every cell, every step |
| Static or adaptive cells | how to cut a continuous space | fixed grid, or fine cells only where the belief is high | adaptive saves cells, costs bookkeeping |
| Binary Bayes filter | a fixed yes-or-no state | add the log of the Bayes factor for each reading | one addition per reading |
| Forward-backward | where the robot was at an earlier time | multiply forward $\alpha$ and backward $\beta$, rescale | two passes over the run |
| Viterbi | the single most likely path | maximum instead of sum, then follow back-pointers | 10 × 10 per step, not 10 to the power $T$ for $T$ steps |

- The histogram filter runs the **Bayes filter** (G-2446) exactly on a list of cells, because the sum over previous states has only as many terms as there are cells: 10 on the hallway instead of infinitely many, and only 3 of them count for each new cell.
- Sensing multiplies each cell by the measurement probability $p(z \mid x)$ and rescales, so cells that explain the reading gain **belief** (G-2433); moving convolves the belief with the motion kernel, because the same move error applies in every cell.
- Moving without reading flattens the belief, so a robot must keep reading its sensors to stay localized.
- A wrong reading moves the tallest bar but never removes the true cell, so the filter recovers after a few correct readings.
- Fine cells explode in number with the space size and the number of state variables (7.2 million for a 30 m floor), so **adaptive decompositions** (G-2465) put small cells only where the belief is high.
- For a static yes-or-no state each reading multiplies the odds by the Bayes factor, so in **log odds** (G-1116) it adds a fixed number; this is fast and does not round to 0 or 1.
- Later readings tell where the robot was earlier, because each earlier cell predicts what the later readings should be: forward-backward raised the true starting cell from 0.19 to 0.36, and the **Viterbi algorithm** (G-2474) recovered the true path 1, 3, 5 with 200 comparisons instead of 1000 path products.

The robot can now run the Bayes filter on a computer, one number per cell, and look back over a recorded run. Still missing: cells multiply with every extra state variable, 7.2 million for one 30 m floor; the [**particle filter**](../RO-016-particle-filter/RO-016-particle-filter.md#1-overview) (G-2492) keeps samples only where the belief is, and the [**Kalman filter**](../RO-017-kalman-filter/RO-017-kalman-filter.md#1-overview) (G-2506) keeps a belief shaped like a single bell-shaped curve, a [**Gaussian**](../../../../MA/03-distributions/MA-024-normal-distribution/MA-024-normal-distribution.md#2-what-the-normal-distribution-is) (G-827), as two numbers.

## 7. Sources

**Built from**

- Udacity, Artificial Intelligence for Robotics, lesson 1 "Localization" (clips "Probability After Sense" to "Sense and Move"; some titles in Korean, English audio), YouTube playlist, https://www.youtube.com/playlist?list=PLJTqwKOfxtSjwWlu3Gth0m6mcQ9awWONg
- Udacity, Artificial Intelligence for Robotics, lesson 1, programming assignment (2-D localization), YouTube, https://www.youtube.com/watch?v=9a42_zEeeA0
- RoboJackets, "Log Odds Derivation | Robotics 5-3", YouTube, https://www.youtube.com/watch?v=bNoWvj0klAo
- NPTEL IIT Madras, "Introduction to Robotics: Binary Bayes" (#36), YouTube, https://www.youtube.com/watch?v=odk5ZfSStag
- DataMListic, "The Viterbi Algorithm | HMM Part 2", YouTube, https://www.youtube.com/watch?v=LGY4yMWUjL4
- DataMListic, "Forward-Backward Algorithm | HMM Part 3", YouTube, https://www.youtube.com/watch?v=QBDvFVmpgd0 (used for the idea of alpha, beta and gamma only)
- Carlotta A. Berry, PhD, "Advanced Mobile Robotics: Lecture 5-1 Discrete Bayes Filters" (grid size and tree-based cells), YouTube, https://www.youtube.com/watch?v=m-a8WRKv7nM
- Labbe, R. *Kalman and Bayesian Filters in Python*, ch.2 "Discrete Bayes Filter" (sensing, prediction as convolution, loss of information, bad sensor data, drawbacks and limitations). https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python/blob/master/02-Discrete-Bayes.ipynb (Labbe ch.2)
- Fox, D., Burgard, W. and Thrun, S. (1999). Markov localization for mobile robots in dynamic environments. *Journal of Artificial Intelligence Research* 11, 391–427. §3.4 grid sizes, §6 the need for variable-resolution grids. https://jair.org/index.php/jair/article/view/10246 (Fox 1999)
- Luft, L., Burgard, W. et al. (Uni Freiburg), *Introduction to Mobile Robotics*, "Grid Maps and Mapping with Known Poses" slides (binary Bayes filter per cell, log odds update "only requires to compute sums"). http://ais.informatik.uni-freiburg.de/teaching/ss23/robotics/slides/12-occupancy-mapping.pdf (Freiburg mapping slides)
- DeNero, J., Klein, D. et al. *CS 188: Introduction to Artificial Intelligence*, online textbook, UC Berkeley. §8.1 Markov models, §8.2 hidden Markov models, §8.3 the Viterbi algorithm. https://inst.eecs.berkeley.edu/~cs188/textbook/hmms/viterbi.html (CS188)
- Jurafsky, D. and Martin, J. H. *Speech and Language Processing*, 3rd ed. draft, Appendix A "Hidden Markov Models" (the count of possible paths, forward, backward and smoothed probabilities, Viterbi). https://web.stanford.edu/~jurafsky/slp3/A.pdf (J&M App. A)

**Other references**

- ShanghaiTech University, Robotics (2024), "Mapping" slides, slide "Adaptive cell decomposition" (quadtrees and octrees). https://robotics.shanghaitech.edu.cn/sites/default/files/2024-03/robotics_2024_05-Mapping.pdf (ShanghaiTech slides)
- Thrun, S., Burgard, W. and Fox, D. (2005). *Probabilistic Robotics*. MIT Press. §4.1 the histogram filter, §4.1.4 decomposition techniques, §4.2 binary Bayes filters with static state. Cited only where the free sources above say the same (PR)

## 8. Key terms

Terms taught in this Note come first; linked terms are recaps, taught in the Note the link opens.

| Term | Meaning |
|---|---|
| Histogram filter (discrete Bayes filter) (G-2461) | The Bayes filter run on a space cut into cells, keeping one probability per cell; sensing multiplies each cell by $p(z \mid x)$ and rescales, moving slides and blurs the list. It makes the Bayes filter computable for a continuous position. |
| Motion kernel (G-2462) | The short list of move probabilities, such as (0.1, 0.8, 0.1) for one cell short, exact, one cell too far, slid along the belief in the prediction step; it spreads each cell's belief over the cells the robot may have reached. |
| Static decomposition (G-2464) | Cutting the state space into cells fixed before the robot starts, usually a regular grid such as 15 cm cells and 2° headings; simple, but it spends as much work on empty regions as where the robot is. |
| Adaptive (dynamic) decomposition (G-2465) | Cutting the state space into cells that change with the belief: small cells where the belief is high, large cells where it is near zero, as in a quadtree; it gives fine detail with far fewer cells. |
| Static state (G-2467) | A state that the robot's commands do not change while it is being estimated, such as a door nobody touches; the prediction step then does nothing and only readings update the belief. |
| Binary Bayes filter (G-2466) | The Bayes filter for a yes-or-no state that does not change, such as "door open" or "this map cell is occupied", run in log odds: each reading adds the log of its Bayes factor. It is fast and does not round to 0 or 1. |
| Filtering (state estimation) (G-2469) | Estimating the current state from the readings so far, $p(x_t \mid z_{1:t})$; what a robot needs while it drives, and what the Bayes filter computes. |
| Smoothing (G-2470) | Estimating the state at an earlier time using all readings, including later ones, $p(x_t \mid z_{1:T})$; later readings often settle where the robot was, such as raising the true starting cell from 0.19 to 0.36. |
| Most likely path (G-2476) | The one sequence of hidden states with the highest probability given all readings, such as cells 1, 3, 5; one consistent answer for a whole run, found by the Viterbi algorithm. |
| Viterbi algorithm (G-2474) | The method that finds the single most likely sequence of hidden states in an HMM by keeping, for each state and time, only the best path ending there and where it came from, then tracing back; it costs states squared times steps instead of trying every path. |
| Forward-backward algorithm (G-2471) | The method that computes smoothed beliefs in an HMM by multiplying a forward pass (evidence up to $t$) by a backward pass (evidence after $t$) and rescaling; it uses every reading of a recorded run for each time step. |
| Forward probability $\alpha_t$ (G-2472) | The probability of the readings up to time $t$ together with being in state $x$ at $t$; the histogram filter before rescaling, carrying the evidence from the past. |
| Backward probability $\beta_t$ (G-2473) | The probability of the readings after time $t$, given state $x$ at $t$, computed from the last step backwards starting at 1; it carries the evidence from the future. |
| Back-pointer (G-2477) | The note the Viterbi algorithm keeps for each state and time of which earlier state the best path came from; following them backwards from the best end recovers the most likely path. |
| Trellis (G-2475) | A grid drawing of an HMM run with one column of states per time step and lines for the possible moves between columns; every path through it is one guess at the hidden states. |
| [Bayes filter](../../../../RO/localization/02-bayes-filters/RO-014-bayes-filter/RO-014-bayes-filter.md#44-the-algorithm) (G-2446) | The algorithm that keeps a robot's belief up to date one step at a time: a prediction step after each command and a correction step after each reading; it gives the exact belief without storing the history, under the Markov assumption. |
| [Belief](../../../../RO/localization/02-bayes-filters/RO-013-belief/RO-013-belief.md#42-the-definition) (G-2433) | The robot's probability for each possible state given all its commands and readings, $\text{bel}(x_t) = p(x_t \mid z_{1:t}, u_{1:t})$; a short summary of the history that says how strongly the evidence points to each state. |
| [Log-odds](../../../../ML/08-trees-and-ensembles/ML-116-gradient-boosting-classification/ML-116-gradient-boosting-classification.md#4-stage-1-the-log-odds-of-class-1) (G-1116) | The natural log of the odds, $\ln(p/(1-p))$: it turns a probability between 0 and 1 into any number (0 at $p = 0.5$), so a model such as logistic regression can predict it with a straight line, and the sigmoid turns it back into a probability. |
| [Discretization](../../../../ML/03-feature-engineering/ML-031-binning-binarization/ML-031-binning-binarization.md#1-overview) (G-619) | Turning a continuous column into a discrete one by cutting its range into intervals (bins), such as ages 0–18, 18–60 and 60+; it turns endless values into a few groups that a model or a table can handle. |
| [Histogram](../../../../ML/02-getting-data/ML-019-univariate-analysis/ML-019-univariate-analysis.md#6-histogram) (G-899) | A bar chart of how many values fall in each equal range (bin) of a numerical column; it shows the shape of a distribution at a glance: where values pile up, how far they spread and whether there are several peaks. |
| [Law of total probability](../../../../MA/02-probability/MA-019-bayes-problem/MA-019-bayes-problem.md#1-overview) (G-1053) | The rule for the overall probability of an event: add its probability under each case, weighted by how likely that case is, $P(B) = \sum_i P(B \mid A_i) P(A_i)$, when the cases $A_i$ are mutually exclusive and cover every possibility. |
| [Convolution operation](../../../../DL/04-cnn/DL-042-convolution-operation/DL-042-convolution-operation.md#6-the-convolution-operation) (G-481) | Sliding a small filter over an input and, at each position, multiplying cell by cell and adding up, so the output (a feature map) is large where the input contains the filter's pattern, such as an edge. |
| [Pose](../../../../RO/control/01-robot-models/RO-001-pose-and-differential-drive/RO-001-pose-and-differential-drive.md#22-why-position-is-not-enough-the-heading) (G-2280) | Where a robot is and which way it faces: on a floor, its position $(x, y)$ and heading $\theta$, such as (2 m, 1 m, 30°); needed because a robot at one spot drives off differently depending on its heading. |
| [Odds](../../../../ML/08-trees-and-ensembles/ML-116-gradient-boosting-classification/ML-116-gradient-boosting-classification.md#4-stage-1-the-log-odds-of-class-1) (G-1376) | How often an event happens divided by how often it does not, e.g. 5 placed to 3 not placed is $5/3$; unlike a probability, odds have no upper limit, so evidence updates them by one multiplication, and their log can be predicted with a straight line. |
| [Bayes factor](../../../../MA/02-probability/MA-019-bayes-problem/MA-019-bayes-problem.md#61-the-size-of-the-update-the-bayes-factor) (G-2215) | A number that says how strongly the evidence favours yes over no: how many times more likely the evidence is if the answer is yes than if it is no, $P(\text{evidence} \mid \text{yes}) / P(\text{evidence} \mid \text{no})$. Multiplying the prior odds by it gives the posterior odds. |
| [Sigmoid function](../../../../ML/07-classification/ML-071-sigmoid-function/ML-071-sigmoid-function.md#4-the-sigmoid-function) (G-1798) | An S-shaped function that squashes any number into the range 0 to 1, $\sigma(z) = 1/(1 + e^{-z})$; it turns a score into a probability, as in logistic regression. |
| [Hidden Markov model (HMM)](../../../../RO/localization/02-bayes-filters/RO-013-belief/RO-013-belief.md#63-hidden-markov-model) (G-2439) | A Markov chain whose states cannot be seen, where each state produces an observation that can, such as hidden robot cells producing "door" or "wall" readings; it is the model behind robot state estimation, speech recognition and many trackers. |
| [Markov property](../../../../RO/localization/02-bayes-filters/RO-007-why-a-robot-is-never-sure/RO-007-why-a-robot-is-never-sure.md#43-complete-state-and-the-markov-property) (G-2316) | The property of a sequence of states that the future depends on the past only through the present state; it lets a filter forget the history and work from the latest state alone. |
| [Dynamic programming](../../../../DL/01-basics/DL-019-mlp-memoization/DL-019-mlp-memoization.md#33-the-memoized-version) (G-652) | Solving a problem by storing the answer to each overlapping sub-problem the first time it is computed and looking it up afterwards, so no work is repeated; memoization is one form of it. |
| [Particle filter](../../../../RO/localization/02-bayes-filters/RO-016-particle-filter/RO-016-particle-filter.md#4-the-particle-filter-step-by-step) (G-2492) | A Bayes filter that stores the belief as a set of weighted samples (particles) and runs each round as move, weigh, resample; it can hold beliefs of any shape, such as a belief with three modes, one at each of three doors. |
| [Kalman filter](../../../../RO/localization/02-bayes-filters/RO-017-kalman-filter/RO-017-kalman-filter.md#25-the-linear-gaussian-system) (G-2506) | The Bayes filter for a linear Gaussian system: it keeps the belief as a mean and a (co)variance and updates them with a predict step and an update step, blending a model's prediction with a sensor reading so the result is as certain as possible. |
| [Gaussian distribution](../../../../MA/03-distributions/MA-024-normal-distribution/MA-024-normal-distribution.md#2-what-the-normal-distribution-is) (G-827) | Another name for the normal distribution: the symmetric, bell-shaped continuous distribution set by its mean and standard deviation, used to model many measurements. |
