# Maths Notes: video sources and animation plan

Covers the 69 maths Notes (200–999). Source order: StatQuest, then Khan Academy (YouTube channel), then 3Blue1Brown, then free CampusX videos. A textbook is used only when none of these covers the topic. Every video ID, title, channel and length was checked with yt-dlp. English captions (`.vtt` and `.txt` with ~30 s timestamps) are in `transcripts/maths-video/<NoteID>-<short>.*`. CampusX Hindi sessions were not re-downloaded; their entries point to the existing `transcripts/Mxx.whisper-en.txt` files.

Each Note block below has:

- **Sources**, with timestamps.
- **Teaching path**: the order the video builds the idea, its visuals, and its exact numbers. This is the beginner path the rewrite should follow.
- **What the video adds** that the Note lacks.
- **Animation ideas**: each to be redrawn with our own code and data.
- **Textbook-only parts**.
- **Contradictions**.

## Summary

### Primary video series per block

| Block | Notes | Primary series |
|---|---|---|
| Descriptive statistics | 220–231 | StatQuest *Statistics Fundamentals*; Khan for frequency tables, box plots, mean/median |
| Distributions | 240–262 | StatQuest + Khan; 3Blue1Brown for density and the normal formula (ZA4JkHKZM50, zeJD6dqJ5lo, cy8r7WSuT1I) |
| Binomial and CLT | 270–272 | StatQuest (J8jNoF-K8E8, YAlJCEDH2uY, XNgt7F6FqDU); 3Blue1Brown CLT (zeJD6dqJ5lo); Khan sampling distributions |
| Confidence intervals, t | 280–282 | Khan (hlM7zdf7zwU, bGALoCckICI, gLE6y_NwmhQ, hV4pdjHCKuA); StatQuest bootstrap CI |
| Hypothesis tests | 290–302 | StatQuest null/alternative, p-values, power; Khan z-test, t-tests, errors, power |
| Probability | 330–341 | Khan basics; StatQuest expected value, conditional probability, Bayes; 3Blue1Brown Bayes area picture |
| Linear algebra | 350–363, 490–530 | 3Blue1Brown *Essence of Linear Algebra* ch. 1–4, 6, 9, 14; Khan worked numbers; StatQuest *Essential Matrix Algebra for NNs* |
| Poisson and tests | 560–572 | Khan Poisson process, chi-square series, ANOVA 1–3; StatQuest null hypothesis, binomial test, linear models |
| Convexity, derivatives | 590, 600 | StatQuest *Gradient Descent* and *Chain Rule*; 3Blue1Brown *Essence of Calculus* ch. 2–4, 10, 11; CampusX convex video |
| Multivariable calculus | 601–603 | Khan Academy multivariable calculus (Grant Sanderson): partials, gradient, directional derivative, Jacobian, tangent plane, quadratic approximation, Hessian, second-partial test |
| SVD | 610–613 | No SVD video in any priority channel (CampusX SVD session is members-only). Supporting pieces from 3Blue1Brown ch. 3, 7, 8, 13, Khan orthogonal matrices / least squares, StatQuest PCA-with-SVD |
| Lagrange, convex, LP/QP | 620–622 | Khan Lagrange multiplier series; Khan concavity; StatQuest *Linear Programming / Simplex* |
| Likelihood | 630–633 | StatQuest MLE series, logistic MLE, cross entropy, ridge |
| GMM / EM | 640–641 | None; StatQuest k-means only as a bridge |

### Coverage

- **57 of the 69 Notes now have a StatQuest, Khan or 3Blue1Brown source.**
- **12 do not:**
  - **Textbook core, no video** (8): 243 KDE, 253 PDF/CDF in practice, 262 Pareto, 610 SVD geometry, 611 computing the SVD, 612 low-rank approximation, 640 GMM, 641 EM. Notes MA-057 and MA-058 have supporting videos for their pieces, but none teaches the SVD itself.
  - **CampusX only** (3): 440 role of maths, 580 learning maths for ML (3Blue1Brown preview only), 210 roadmap (no source needed).
  - **Partly textbook** (1): 260 is half video-sourced (Q-Q plots) and half textbook (kurtosis, Westfall 2014).
- Textbook sections still used for parts of video-sourced Notes are listed in each block (for example MML §5.8 for higher-order Taylor tensors, Boyd & Vandenberghe ch. 5 for KKT and duality).

### Top 15 animation ideas (Hessian and curvature first)

1. **Slider p in f = x² + y² + p·xy, from 0 to 4.** The x- and y-slices stay concave up while a diagonal slice flattens and flips at p = 2, so the bowl becomes a saddle. Live readouts: Hessian eigenvalues 2 ± p and det = 4 − p². Manim 3-D. Source KA m1FhUjMMv30@04:07–05:07, numbers @08:10–10:42.
2. **Tangent plane, then quadratic "ghost" surface** hugging f = x³ + xy + y² at (1, 1). Walk the touch point away and colour the error. Plotly 3-D with a slider. Source KA 80bJA_tSbo4@00:30–02:01.
3. **Saddle x² − y² sliced by the planes x = 0 and y = 0.** The two traced curves lift out side by side, one opening up and one opening down. Manim. Source KA 8aAU4r_pUUU@02:02–04:02.
4. **f = xy with a rotating vertical slicing plane.** Plot the slice's curvature against the angle: 0 on the axes, ± on the diagonals. This shows what the mixed partial measures. Manim. Source KA sJo7D74PAak@06:06–08:42.
5. **f, f′, f″ stacked with one moving cursor.** Shade the convex (f″ > 0) and concave parts. Add 3b1b's "two dx steps, ddf ∝ dx²" picture of the second derivative. Manim. Sources KA LcEqOzNov4E@00:00–05:49; 3b1b BLkz5LGWihw@02:12–03:43.
6. **Taylor polynomial of cos x built term by term.** Match value, then slope, then bend; check cos 0.1 ≈ 0.995; then add the x⁴/24 term. Manim/Plotly. Source 3b1b 3d6DsjIBzJ4@02:05–08:17.
7. **Jacobian zoom box.** A grid under (x + sin y, y + sin x) or polar coordinates, with a tracking inset. Two tiny steps become the Jacobian's columns. Insets at (−2, 1) and (0, 1) show the area growing ×1.23 at one and shrinking ×0.46 at the other. Manim. Sources KA Vnga_psnCAo@03:06, bohL918kXQk@01:00, p46QWyHQE6M@06:37–08:08.
8. **Zoom on a contour map** until the contours f = 2 and f = 2.1 look parallel. The shortest step between them is perpendicular, which is the gradient. Manim. Source KA ZTbTYEMvo10@03:38–06:09.
9. **Lagrange.** First the unit circle lifted onto the surface x²y, then the top view with one contour growing until it is tangent. Plus a budget slider plotting the best revenue M*(b), whose slope is λ. Manim + Plotly. Sources KA vwUV2IDLP8Q@01:00–05:34, m-G3K2GPmEQ@07:41–09:11.
10. **Eigenvectors stay on their own line** as the grid morphs under [[3,1],[0,2]]. Then a λ knob shrinks det(A − λI) to 0. Manim. Sources 3b1b PFDu9oVAE-g@01:06–03:12, @07:29–08:02.
11. **Bayes unit square.** A prior strip; shade the share of each part that matches the evidence; zoom to the posterior fraction; add sliders. Manim. Source 3b1b HZGCoVF3YvM@08:53–09:55.
12. **CLT.** Four different dice distributions; their standardised sums for n = 2 → 50 converge on N(0, 1). Manim. Source 3b1b zeJD6dqJ5lo@22:02 (√n spread @13:39).
13. **Power.** H₀ and H₁ sampling curves with α, β and power shaded, and sliders for n, α and effect size. Plotly. Source StatQuest 6_Cuz0QqRWc@03:34–09:13.
14. **Likelihood.** A fixed data dot (34 g) while the normal curve slides. A second panel traces height against μ, and that trace is the likelihood function. Then the same idea for many points and their product. Manim/Plotly. Sources StatQuest pYxNSUDSFH4@03:07–03:39, XepXtl9YKwc@02:06–03:39.
15. **PCA through the SVD.** A line through the origin rotates over centred data. A live sum of squared projected distances peaks at PC1, and σ₁ = √SS. Manim. Source StatQuest FgakZw6K1QQ@04:20–09:02, @12:23.

Runners-up:

- Covariance quadrant rectangles (qtaqvPAeEJY@07:38).
- Histogram bins refining into a density (ZA4JkHKZM50@03:39–04:13).
- 100 confidence intervals dropping past the true value (bGALoCckICI@02:03).
- Simplex walk on the feasible polygon (h5o1n1QMcmM@09:49–16:29).
- Grid morph and composition order (kYB8IZa5AuE@04:08, XkY2DOUCWMU@07:12).
- Chi-square from squared normals (dXB3cUGnaxQ@01:34–06:51).
- ANOVA split SST 30 = SSB 24 + SSW 6 (j9ZPMlVHJVs@00:30–11:27).

### Contradictions found

In every case below, the Note is right or the difference is only a convention. No Note needs a correction; some should add one line so learners are not confused.

- **630:** StatQuest pYxNSUDSFH4@03:39 gives the likelihood of N(34, 2.5²) at 34 g as 0.21. The correct value is 1/(2.5√(2π)) = 0.160, which is what the Note says (MML eq. 6.62).
- **281:** three videos read a computed interval as "95% probability μ is inside": Khan hlM7zdf7zwU@05:14, StatQuest TqOeMYtOc1w@04:36, Khan hV4pdjHCKuA@11:08. The Note is right (Wasserman §6.3.2).
- **260:** Khan FXZ2O1Lv-KE@07:08 says kurtosis is "peakedness". The Note is right that it measures tails (Westfall 2014).
- **271:** StatQuest YAlJCEDH2uY@06:12 says the CLT needs only a mean. The Note is right that finite variance is also required (Feller Vol. II §VIII.4).
- **231:** StatQuest qtaqvPAeEJY@16:27 says cov = 0 means "no relationship". The Note's "no straight-line relationship" is right (Wasserman §3.3). The caption at @19:08 reads "48" where 408 is meant.
- **270:** Khan NF0lrkqXIkQ@07:45 says the normal arises from a "product" of random processes. It arises from a sum; products give the log-normal.
- **300:** StatQuest vemZtEM63GY@04:08 calls the p-value a confidence that A differs. The Note is right (Greenland et al. 2016).
- **251:** Khan mvye6X_0upA@05:25 gives the area beyond −3 as 0.15%; it is 0.135%.
- **602:** Khan CGbBbH1e7Yw@02:02 gives cos(−2) as +0.42; it is −0.416. Khan's own p46QWyHQE6M@06:07 uses −0.42.
- **620:** Khan vwUV2IDLP8Q@02:00 says "contours of x² + y²" but means x²y.
- **571:** Khan hpWdDmgsIRE@04:44 says "80 did not get sick" where 80 is the number who did get sick.
- **363 (a gap in the Note, not a contradiction):** §6.1 proves that w is normal to the hyperplane only when w₀ = 0. The Khan argument n·(x − x₀) = 0 closes the gap (UJxgcVaNTqY@06:13–09:34).
- **Conventions, not errors** (the Notes should say so):
  - **362:** StatQuest gives cosine similarity a 0–1 range, which holds for non-negative counts (Manning et al. §6.3.1).
  - **510:** StatQuest writes points as rows (x·W); the Note uses columns.
  - **530:** det(λI − A) and det(A − λI) have the same roots.
  - **570:** StatQuest uses an exact binomial test, the Note a z-test.
  - **230:** Khan's whiskers run to min/max; the Note uses 1.5·IQR fences.
  - **302:** Khan uses df = min(n) − 1; the Note uses Welch's df.
  - **291/292:** StatQuest says always use two tails; the Note allows one tail if chosen in advance.
  - **601:** the gradient is a column in Khan and a row in the Note (MML).
  - **620:** the sign of the Lagrangian differs between Khan and the Note.
  - **590/621:** Khan's "concave up" means what the Note calls convex.

---

## Per-Note sources

### 210 Statistics roadmap
- **Sources:** none added. This is a roadmap/overview Note; its own CampusX roadmap video (2GV_ouHBw30) is the right source. StatQuest's "Statistics Fundamentals" playlist order (histograms → distributions → population parameters → mean/variance → p-values → CI) is a useful beginner reading order to cite.
- **Teaching path:** n/a.
- **What the video adds / Animation ideas:** n/a.
- **Textbook-only parts:** ISLR ch. 3, §4.3, §4.4.4 (as now).
- **Contradictions:** none.

### 220 What is statistics: population, sample and types of data
- **Sources:** `StatQuest — "Population and Estimated Parameters, Clearly Explained!!!" (vikkiwjQqfU, 14:31)` → §4 Population and sample (00:32–08:50), §5 tools of inference (09:48–12:51).
- **Teaching path** (StatQuest, the only priority-channel video that teaches population vs sample with a picture):
  1. 00:32 — Starts from a concrete measurement: count mRNA in 5 liver cells; "if that means nothing to you, imagine green apples in 5 grocery stores". Five green dots on a number line at 3, 13, 19, 24, 29.
  2. 01:35 — "Imagine 240 billion green dots" = every cell in a liver. Draws a histogram of all of them (most between 20–30).
  3. 02:38 — Uses the histogram to get a probability: cells with ≥30 transcripts = 38 billion / 240 billion = 0.16.
  4. 03:09 — Overlays a normal curve (mean 20, SD 10) on the histogram; shades area ≥30 = 0.16, same as the histogram → "the curve is a good approximation".
  5. 05:11 — Only now names the term ("terminology alert"): the whole histogram = **population**; mean and SD of that curve = **population parameters**. Side note: exponential (rate 0.1) and gamma (shape, rate) curves also have population parameters.
  6. 07:15 — Back to the 5 dots = **sample**; we estimate parameters from it. ML link at 08:16: "the 5 measurements are the training set, the population curve is what we want to predict".
  7. 08:47 — Numbers: 5 points give mean 17.6, SD 10.1; a repeat experiment gives 19.2, 12.7 → estimates move.
  8. 09:48 — Builds "more data = better estimate" one point at a time: 2 points → mean 11, SD 11.3; 3 points → 15.3, 11; 5 points → 17.6, 10.1 (true 20, 10).
  9. 11:21 — Names the goal of inference: p-values and confidence intervals quantify confidence in the estimates.
- **What the video adds:** the Note defines population/sample in words; the video shows a sample's estimates converging to the population parameters as n grows (09:48–11:21) and the "sample = training data" link.
- **Animation ideas:** Manim: 240 B-dot histogram fades to a normal curve; 2→3→5 sample dots appear one at a time and a purple estimated curve snaps toward the true curve (vikkiwjQqfU@09:48).
- **Textbook-only parts:** §6 Types of data (nominal/ordinal/interval/ratio) — no StatQuest/Khan/3b1b video teaches Stevens' four scales; keep Stevens (1946) Table 1.
- **Contradictions:** none.

### 221 Measures of central tendency
- **Sources:** `Khan Academy — "Average or Central Tendency: Arithmetic Mean, Median, and Mode" (GrynkZB3E7M, 9:01)` → §3 Mean (00:31–02:04), §4 Median (02:35–04:37), §5 Mode (06:40–08:00), §8 Choosing (05:09–06:40, 08:25). `Khan Academy — "Exploring the mean and median" (n6xCyzOP900, 5:26)` → §3.1/§8 outlier effect (01:00–02:00). Also `StatQuest — SzZ6GpcfoQY` 02:01–03:35 for μ vs x̄ notation (see 222).
- **Teaching path** (Khan GrynkZB3E7M is the most beginner-friendly: one small dataset reused for all three measures):
  1. 00:00 — One list: 2, 3, 3, 3, 4, 4, 10. Goal stated in plain words: "one number for where these numbers roughly are" → named "average / central tendency".
  2. 00:31 — Arithmetic mean = sum ÷ count: 29/7 = 4 1/7. Notices it sits right of most numbers, "what caused that? the 10".
  3. 02:35 — Median = middle number after sorting: count 3 in from each side → 3. Even case at 03:37: 2, 3, 4, 5 → two middles → (3+4)/2 = 3.5, and here mean = median = 3.5.
  4. 05:09 — Contrast: first set median 3 vs mean 4.14 → the outlier 10 pulls the mean. 06:09 thought experiment: add 1,000,000 → mean explodes, median ≈ 3.5. Term "less sensitive to extremes".
  5. 06:40 — Mode = most frequent (three 3's → 3); 07:49 weakness: 2, 3, 4, 5 has no meaningful mode.
  6. 08:25 — Why summarise at all: "7 billion numbers, you don't show someone all of them".
  - n6xCyzOP900 01:00 — interactive number line: Sal drags the largest dot right; mean label moves, median label stays fixed. Best visual for "median is robust".
- **What the video adds:** the drag-an-outlier interaction (n6xCyzOP900 01:00–02:00); the 1,000,000 thought experiment.
- **Animation ideas:** Plotly slider: 5 dots on a number line, slider moves the top value from 10 to 1,000; mean and median markers update live (n6xCyzOP900@01:00).
- **Textbook-only parts:** §6 Weighted mean, §7 Trimmed mean — no priority-channel video; keep Wilcox (2012) ch. 3.
- **Contradictions:** none.

### 222 Measures of dispersion
- **Sources:** `StatQuest — "Calculating the Mean, Variance and Standard Deviation, Clearly Explained!!!" (SzZ6GpcfoQY, 14:22)` → §4 Variance (03:35–09:47), §6 SD (05:39–06:41). `StatQuest — "Why Dividing By N Underestimates the Variance" (sHRBg6BhKjI, 17:15)` → §4.3 n−1 (03:07–14:37), §4.2/§5 squares vs absolute value (15:09–15:40). `Khan Academy — "Simulation showing bias in sample variance" (Cn0skMJ2F3c, 6:24)` → §4.3 Figure 4 (04:03–06:06).
- **Teaching path:**
  - SzZ6GpcfoQY (first):
    1. 01:01 — Same 5 liver-cell dots (3, 13, 19, 24, 29) and the full-population histogram from the population video.
    2. 02:01 — Population mean = average of all 240 B = 20; centre the curve there. 03:04 sample mean = 17.6; terminology alert x̄ vs μ.
    3. 04:06 — Population variance formula built term by term: "x − μ: subtract the mean from each point (boop boop)", square, Σ, divide by N. 05:08 why square: left-side differences are negative and would cancel the right side.
    4. 05:39 — Result 100 "transcripts squared" → can't draw squared units on the x-axis → take √ → SD = 10, drawn as 20 ± 10 on the graph.
    5. 07:44 — Sample version: swap μ for x̄ and N for n−1. Reason in words: distances to x̄ are smaller than distances to μ, so dividing by n would underestimate. Numbers: 101.8 → SD 10.1; purple estimated curve (17.6, 10.1) vs true (20, 10).
    6. 13:29 — Practical tip: Excel VAR.P vs VAR.S.
  - sHRBg6BhKjI (the "why"):
    1. 03:38 — Replace x̄ by 0, compute mean squared distance = 391; plot point (0, 391). Move the line to 5 → 240. Keep moving → points trace a U-shaped curve "variance around a point v".
    2. 04:39 — Mark x̄ and μ on that U: the bottom is at x̄, μ is a little up the wall → dividing by n around x̄ always gives the smaller value.
    3. 05:41 — New sample of 5 → new U, bottom again at its own x̄.
    4. 07:15 — Proof: f(v) = (1/n)Σ(x−v)²; chain rule → derivative −(2/n)Σ(x−v); set 0 → v = x̄. Done three times: with the data, with x₁…x₅, with n points.
    5. 15:09 — Absolute value instead of square gives a V with a sharp corner, no derivative → why squares are used.
  - Cn0skMJ2F3c 04:03 — Simulation bar chart: average biased variance / σ² → 1/2 at n=2, 2/3 at n=3, 3/4 at n=4 → pattern (n−1)/n → multiply by n/(n−1).
- **What the video adds:** the U-curve "variance around v" with x̄ at its minimum (sHRBg6BhKjI 03:38–05:10) — a visual reason for n−1 the Note lacks (the Note gives the 1,2,3,4 enumeration and Titanic simulation only); the (n−1)/n pattern (Cn0skMJ2F3c 04:03); square vs absolute value (sharp corner) at 15:09.
- **Animation ideas:** Manim: vertical line slides along the number line under the 5 dots; squared-distance bars grow/shrink; a dot traces the U-curve; label x̄ at the bottom and μ above it (sHRBg6BhKjI@03:38). Plotly: bar chart of mean biased variance / σ² vs n with the (n−1)/n curve (Cn0skMJ2F3c@04:03).
- **Textbook-only parts:** §7 Coefficient of variation — NIST Dataplot (as now). §5 MAD — no video; keep current source.
- **Contradictions:** none. (Video says why n−1 exactly is deferred to the expected-values video; Note's enumeration proof agrees.)

### 223 Frequency tables and graphs
- **Sources:** `StatQuest — "StatQuest: Histograms, Clearly Explained" (qBigTkBLU6g, 3:42)` → §3 Histograms (00:35–03:16). `Khan Academy — "Frequency tables and dot plots" (gdE46YSedvE, 7:18)` → §2 Frequency tables (00:00–02:34), dot plot (02:34–04:37). `Khan Academy — "Comparing dot plots, histograms, and box plots" (s_w3EJ2Jzw0, 5:25)` → §3 what a histogram can/cannot answer (01:31–02:32, 04:06–05:08).
- **Teaching path:**
  - qBigTkBLU6g (best for "why a histogram exists"):
    1. 00:35 — Measure one person's height = one dot on a line; then many; dots overlap and hide each other.
    2. 00:50 — Fix attempt 1: stack identical values → fails, exact repeats are rare.
    3. 01:06 — Fix attempt 2: cut the range into bins and stack dots per bin → "this, my friends, is a histogram". Taller stack = more measurements.
    4. 01:39 — Use it to predict: "I'd bet the next measurement lands here"; rare out in the tails. Bridge to fitting a normal or exponential curve.
    5. 02:12 — Bin width: too narrow → every dot its own bin (no insight); 02:44 too wide → 2 bins, 50/50 split (only "above/below average"). "Don't trust the default bin setting."
  - gdE46YSedvE: raw list of class ages → frequency table built by counting each age (5:2, 6:1, 7:4, 8:0, 9:4, 10:1, 11:0, 12:2) → same counts as a dot plot (02:34) → answer questions from it: mode (7 and 9 tie), range 12−5 = 7, "how many older than 9?" = 3.
  - s_w3EJ2Jzw0: Pixar film lengths: median readable from dot plot and box plot, not from the histogram (01:31 "I know one film is 80–85 but not its exact length"); car odometers: count >200,000 km readable only from the histogram (03:04).
- **What the video adds:** the dots → stacked dots → bins build-up (qBigTkBLU6g 00:35–01:06) that motivates bins; the too-narrow / too-wide pair; Khan's "which chart answers which question" (histogram loses the exact values).
- **Animation ideas:** Manim: dots rain onto a number line, overlap, then slide into bins and stack into bars; then bin width animates from very narrow to two bins (qBigTkBLU6g@00:35, @02:12).
- **Textbook-only parts:** §4–5 graphs for two or more features — no priority-channel video; keep current sources (NIST handbook for bimodal histogram).
- **Contradictions:** none.

### 230 Percentiles and box plots
- **Sources:** `StatQuest — "Quantiles and Percentiles, Clearly Explained!!!" (IFKQLDmRK0Y, 6:30)` → §2 Quantiles (01:02–03:35), §3 Percentiles (03:35–05:10). `StatQuest — "Boxplots are Awesome!!!" (fHLhBnmwUM0, 2:33)` → §6 Reading box plots (00:30–02:03). `Khan Academy — "Constructing a box and whisker plot" (09Cx7xuIXig, 8:18)` → §4 five-number summary, §5 building by hand (whole video).
- **Teaching path:**
  - IFKQLDmRK0Y:
    1. 00:30 — Admits the mess up front: R's quantile() has 9 methods; "strict definition vs how it's used".
    2. 01:02 — 15 gene-expression dots on a line; one vertical line at the median (4.5) with 7 dots each side → "the median is a quantile because it splits data into equal groups"; labelled both 0.5 and 50%.
    3. 02:35 — Two more lines → 4 equal groups: 0.25 quantile = 2.5, 0.75 quantile = 7.3.
    4. 03:35 — Percentile = quantile with 100 groups; in practice used loosely ("50th percentile" on 15 points).
    5. 04:09 — Per-point percentile = fraction of points below it: lowest = 0th, next = 1/15 = 7th, 4th point = 3/15 = 20th.
    6. 05:10 — Small data → methods disagree; large data → they agree.
  - 09Cx7xuIXig: 17 restaurant commute distances; sort them (00:00), median = 9th value = 6; remove the median, take medians of the halves → Q1 = (2+3)/2 = 2.5, Q3 = (11+14)/2 = 12.5; draw number line 0–35, box 2.5–12.5, line at 6, whiskers to min 1 and max 22.
  - fHLhBnmwUM0 00:30 — labels box, whiskers, median line; "50% of data inside the box"; 01:31 outliers as dots beyond whiskers; overlay raw points on the box (sample size visible); 02:03 box plot vs bar plot of same data.
- **What the video adds:** the "lines that cut the dots into equal groups" picture (IFKQLDmRK0Y 01:02–03:05); overlaying raw data on a box plot (fHLhBnmwUM0 01:31).
- **Animation ideas:** Manim: 15 dots on a line; vertical lines drop in one at a time (median, then Q1/Q3), each region coloured with its count (IFKQLDmRK0Y@01:02); then the box rises out of the Q1–Q3 region and whiskers extend (09Cx7xuIXig whole).
- **Textbook-only parts:** 1.5 IQR fences and the "why 1.5" derivation — not in these videos; keep Note ML-042 / current sources (Tukey's rule).
- **Contradictions:** convention difference, not an error. Khan (09Cx7xuIXig) excludes the median when splitting halves and draws whiskers to the min/max (1 and 22); the Note uses the (n+1)/linear percentile rules and 1.5 IQR fences (Tukey's box plot). Both are valid conventions; the Note's 1.5 IQR version matches seaborn/matplotlib defaults. The Note should say "some textbooks draw whiskers to min/max" so a learner watching Khan is not confused.

### 231 Covariance and correlation
- **Sources:** `StatQuest — "Covariance, Clearly Explained!!!" (qtaqvPAeEJY, 22:23)` → §2 mean→variance→covariance (00:30–02:34), §3 Covariance (02:34–17:00), §3.2 scale flaw (17:00–20:12). `StatQuest — "Pearson's Correlation, Clearly Explained!!!" (xZ_z8KWkhXE, 19:13)` → §4 Correlation (04:07–15:32), §5 not causation (03:34–04:07).
- **Teaching path:**
  - qtaqvPAeEJY:
    1. 00:30 — Recap: 5 cells, gene X on a number line, x̄ and variance. 01:03 add gene Y counted in the same 5 cells, drawn on a **perpendicular** axis ("don't sweat why it's perpendicular").
    2. 02:03 — Look at pairs: one cell is below both means, another above both → "do pairs tell us something single values don't?" → plot each pair as one dot (scatter).
    3. 03:05 — Trend line: positive slope; 04:05 negative-slope data; 04:35 flat data (same y for every x) → no trend. Main idea stated twice: covariance classifies + / − / none.
    4. 07:06 — Formula appears only now. Draws the vertical x̄ line and horizontal ȳ line across the scatter → 4 quadrants. Leftmost point: (x−x̄) < 0, (y−ȳ) < 0 → product positive. Does each point. 10:45 "points in these two quadrants add positive values". Σ/(n−1) → cov = 116 → positive trend.
    5. 11:15 — What covariance does NOT tell: steepness, closeness to the line.
    6. 12:49 — Second dataset: points in the other two quadrants → negative products → cov negative. 14:53 flat data: every (y−ȳ) = 0 → cov = 0; also a symmetric up-down pattern where + and − cancel → 0.
    7. 17:00 — Why it's hard to read: cov(X, X) = variance (102); multiply data by 2 → same picture, covariance ×4 (408; captions mis-transcribe "48"). Data far from line can give larger or smaller cov depending on units (381 vs smaller after rescale).
    8. 20:12 — "Wish there was a scale-free version" → correlation.
  - xZ_z8KWkhXE:
    1. 01:30 — Same scatter; use the line to predict: x = 20 → y ≈ 27. Points close to the line → narrow range of guesses (strong); far → wide range (weak).
    2. 03:34 — Not causation: "something else could cause the trend".
    3. 04:07 — Correlation = number for strength; 1 when a straight positive-slope line passes through every point, regardless of slope steepness or axis scale (axis numbers deliberately removed).
    4. 05:43 — Two random dots always give r = 1 → why small samples mislead; 3 points on a line is unlikely by chance → p-value enters (08:18). r = 0.3 with n growing: p 0.8 → 0.08 → 0.008 but guesses stay bad (12:27).
    5. 13:27 — Formula last: cov / (√var_x √var_y); denominator "squeezes" cov into [−1, 1]. Numbers: 116 / √(101.8 × 160.3) ≈ 0.9, p = 0.03.
- **What the video adds:** the quadrant picture (mean lines splitting the scatter into +/− product regions) at qtaqvPAeEJY 07:38–10:45 — the clearest visual for the sign of covariance; "2 random dots always give r = 1" (xZ_z8KWkhXE 05:43–07:48); r vs confidence (p-value) separation (12:27).
- **Animation ideas:** Manim: scatter with x̄ and ȳ lines; each point draws a rectangle to the mean-crossing, shaded green (positive product) or red (negative); running sum ticker gives the covariance (qtaqvPAeEJY@07:38). Plotly slider: scale X by k and show cov changing by k while r stays fixed (qtaqvPAeEJY@18:38).
- **Textbook-only parts:** rule-of-thumb strength bands — Akoglu (2018) Table 1, as now.
- **Contradictions:** video (qtaqvPAeEJY 16:27 and 21:13 summary) says "covariance = 0 means no relationship". The Note's wording "no straight-line relationship" is right: zero covariance rules out only a linear trend (e.g. y = x² on symmetric x has cov 0). Wasserman, *All of Statistics* §3.3 (independence ⇒ cov 0, not the converse). Keep the Note's wording; add the y = x² example.

### 240 Random variables and probability distributions
- **Sources:** `StatQuest — "The Main Ideas behind Probability Distributions" (oI3hZJqXJuc, 5:15)` → §3–5 table → function → graph (00:38–04:34). `Khan Academy — "Random variables" (3v9w79NhsfI, 5:32)` → §2 Random variables (00:00–05:18).
- **Teaching path:**
  - Khan 3v9w79NhsfI first (defines the object):
    1. 00:00 — Warns: not an algebra variable. "A random variable maps outcomes of a random process to numbers."
    2. 00:34 — X = 1 if heads, 0 if tails; "could have been 100 and 703, still a random variable" → the mapping is a choice.
    3. 01:38 — Y = sum of 7 dice. 02:41 why bother: P(Y ≤ 30), P(Y is even) instead of writing the sentence out.
    4. 04:17 — Contrast with x + 5 = 6 (solve for x): a random variable has no single value, only probabilities of values.
  - StatQuest oI3hZJqXJuc:
    1. 00:38 — Measure heights one at a time (5.2, 5.8, 5.6, 5.9, 5.1, 6.3 ft) and drop each into a 0.5-ft bin → histogram. 01:42 most between 5–6 ft, both tails rare.
    2. 02:16 — Halve the bin width → more precise ("half the people between 5.25 and 5.75").
    3. 02:49 — Smooth curve over the histogram. Three advantages: an empty bin still gets a probability (03:23); any range like 5.021–5.317 without rounding to bins (04:00); a curve from mean and SD works with few data.
    4. 04:34 — Names it: histogram and curve are both "distributions".
- **What the video adds:** histogram → narrower bins → smooth curve sequence (StatQuest 00:38–02:49); the "100 and 703" point that the number assignment is arbitrary (Khan 01:05).
- **Animation ideas:** Manim: height dots fall into bins; bins split in half twice; a smooth curve fades in over the bars, then an empty bin gets shaded under the curve (oI3hZJqXJuc@02:16–03:23).
- **Textbook-only parts:** §8 Parameters of a distribution — partly covered by StatQuest vikkiwjQqfU 05:42–06:44 (see 220); keep MML §6.1.2 for the formal "random variable as a function".
- **Contradictions:** none.

### 241 PMF and discrete CDF
- **Sources:** `Khan Academy — "Constructing a probability distribution for random variable" (cqK3uRoPtk0, 6:47)` → §2 PMF (00:00–06:40), the bar plot of a PMF (03:05–05:40).
- **Teaching path:**
  1. 00:00 — X = number of heads in 3 fair flips. 00:31 writes all 8 outcomes HHH … TTT.
  2. 01:03 — Groups outcomes by X: X=0 → 1/8, X=1 → 3/8 (circles the 3 outcomes), X=2 → 3/8, X=3 → 1/8.
  3. 03:05 — Draws axes: probability (0–1, ticks in eighths) vs value of X; draws bars 1/8, 3/8, 3/8, 1/8.
  4. 06:10 — Names it: a discrete probability distribution; X can't be 1/2 or π.
- **What the video adds:** the outcome-list → grouping → bar chart sequence on a smaller example than the Note's two dice; good warm-up before the 36-outcome dice table.
- **Animation ideas:** Manim: 8 coin-triplet tiles slide into 4 columns by number of heads, then each column collapses into a bar of height count/8 (cqK3uRoPtk0@01:03–05:40).
- **Textbook-only parts:** §7 discrete CDF (step function) — no priority-channel video found for the discrete CDF staircase; keep MML §6.2 / current sources. §6 Bernoulli example — MML Example 6.8 (and see 270 for StatQuest/Khan).
- **Contradictions:** none.

### 242 PDF and continuous CDF
- **Sources:** `3Blue1Brown — "Why 'probability of 0' does not mean 'impossible' | Probabilities of probabilities, part 2" (ZA4JkHKZM50, 10:01)` → §3 y-axis is not probability (01:02–02:08), §4 area (02:39–05:51), §5 density (04:13–05:20). `Khan Academy — "Probability density functions" (Fvi9A_tEmXQ, 10:02)` → §3 (02:09–04:11), §4 (04:11–08:28).
- **Teaching path:**
  - Khan Fvi9A_tEmXQ (easier first contact):
    1. 00:34 — Y = exact amount of rain tomorrow; draws a hump-shaped curve, x-axis 0–4 inches, peak ≈ 0.5.
    2. 02:09 — Asks P(Y = 2) — tempting to read 0.5 off the curve → "no". 03:10 "exactly 2, not one extra water molecule" → 0.
    3. 04:11 — Fix: ask P(|Y − 2| < 0.1) = P(1.9 < Y < 2.1) → shade the strip → "area is key" → ∫ from 1.9 to 2.1.
    4. 06:21 — Area of a line = base 0 → probability 0.
    5. 07:25 — More areas: 1–3 inches, < 0.1, > 4 inches ("10% chance"); 07:58 total area = 1, same rule as PMF bars summing to 1 (coin 0.5 + 0.5).
  - 3b1b ZA4JkHKZM50 (the "why density"):
    1. 00:02 — Weighted coin, 7 heads in 10; "what's the probability the true weight h is exactly 0.7?"
    2. 01:02 — Paradox: if every value in [0,1] had a non-zero probability, the sum blows up; if all are 0, the sum is 0 ≠ 1.
    3. 02:39 — Buckets of width 0.05 (e.g. 0.8–0.85); "let the AREA of each bar be the probability, not the height".
    4. 03:39 — Animation: buckets get finer and finer; bar areas shrink but heights stay ≈ the same → a smooth curve emerges. Counterfactual at 04:13: if heights were probabilities, all bars sink to a flat line at 0.
    5. 04:13 — Units of the y-axis: probability per unit x = "probability density" → PDF named at 05:20.
    6. 05:20 — Read any PDF: area between a and b. Thin slice at 0.7 = 0; whole curve = 1 → paradox sidestepped.
    7. 06:53 — Mixed case (0 with 50%, else half-bell) → measure theory (optional).
- **What the video adds:** the finer-bucket limit where heights stay fixed and areas shrink (3b1b 03:39–04:46) — the Note's shrinking-strip GIF shows one strip; the video shows the whole histogram refining into a curve, and the "heights → flat zero line" counterfactual.
- **Animation ideas:** Manim: histogram of h on [0,1] with bins halving 5 times, total area label fixed at 1, heights stable; second panel where height = probability and bars collapse to 0 (ZA4JkHKZM50@03:39–04:13).
- **Textbook-only parts:** §7–8 continuous CDF and PDF = derivative of CDF — no priority-channel video found for the CDF curve itself; keep current sources (SciPy docs; MML §6.2.2).
- **Contradictions:** none.

### 243 Density estimation and KDE
- **Sources:** none in StatQuest, Khan Academy or 3Blue1Brown (searched "kernel density estimation" — top hits are DataMListic 6sGOMbC5xdE, ritvikmath t1PEhjyzxLA, not priority channels). CampusX session M04 (C_QAURbgBqY) stays the video source.
- **Teaching path:** n/a (non-priority option if wanted: ritvikmath "Kernel Density Estimation: Data Science Concepts" t1PEhjyzxLA, 25:52 — not downloaded).
- **What the video adds:** n/a. StatQuest oI3hZJqXJuc 02:49 ("curve approximating the histogram") is a 1-line motivation for §2.
- **Animation ideas:** Manim: each data point drops a small Gaussian bump; bumps sum into the KDE curve; bandwidth slider widens all bumps (own design, no video source).
- **Textbook-only parts:** §3–5 parametric vs non-parametric, KDE, bandwidth — textbook: MML §11.1/§11.5 currently cited; for KDE itself Wasserman *All of Statistics* §20.3 (kernel density estimation) is the better textbook reference.
- **Contradictions:** none checked against video (none exists).

### 250 Normal distribution
- **Sources:** `StatQuest — "The Normal Distribution, Clearly Explained!!!" (rzFX5NWojp0, 5:13)` → §2 what it is (00:30–01:32), §3 parameters (01:32–03:35), §4 why it matters (04:06). `3Blue1Brown — "But what is the Central Limit Theorem?" (zeJD6dqJ5lo, 31:15)` → §5 the PDF built piece by piece (15:43–19:23). `3Blue1Brown — "Why π is in the normal distribution (beyond integral tricks)" (cy8r7WSuT1I, 24:46)` → §5 where √(2π) comes from (02:07–11:58), optional depth.
- **Teaching path:**
  - StatQuest rzFX5NWojp0 (first, 5 min):
    1. 00:30 — Bell curve of human heights; y-axis = "relative probability"; low at very short, tall near average, low at very tall.
    2. 01:32 — Two curves side by side: newborn boys (mean 20 in, SD 0.6) and adult men (mean 70 in, SD 4). "Always centred on the average."
    3. 02:04 — Why the baby curve is much taller: fewer possible heights → each is more likely ("the wider the curve, the shorter").
    4. 02:35 — SD sets width; 95% within ±2 SD: babies 20 ± 1.2, adults 70 ± 8.
    5. 03:35 — Recipe: to draw a normal you need only mean (centre) and SD (width; width sets height). 04:37 teaser: CLT is why it's everywhere.
  - 3b1b zeJD6dqJ5lo 15:43–19:23 (the formula, layer by layer — best beginner path to the formula):
    1. 15:43 — e^x = growth; e^(−x) flips it = decay; e^(−|x|) decays both ways but has a sharp point; e^(−x²) = smooth bell.
    2. 16:15 — Constant c in e^(−cx²) stretches/squeezes; changing base (2, 3, e) gives the same family.
    3. 17:20 — Rewrite exponent as −½(x/σ)² so σ = SD.
    4. 17:50 — Area must be 1; area under e^(−x²) is √π → divide by √π; stretching by σ√2 → divide by that too → 1/(σ√(2π)).
    5. 19:23 — σ = 1 → standard normal; subtract μ to slide.
  - 3b1b cy8r7WSuT1I (optional, for "why π"): 05:15 bump to 2D surface e^(−(x²+y²)); 06:46 volume via cylindrical shells (soup-can label 2πr · e^(−r²) · dr) = π; 09:22 same volume via parallel slices = C² → C = √π. 13:03 Herschel's dartboard: radial symmetry + independent x, y force f = e^(−cr²).
- **What the video adds:** baby-vs-adult curves showing "narrower ⇒ taller" (rzFX5NWojp0 01:32–03:35); building the formula from e^x step by step (zeJD6dqJ5lo 15:43–19:23) — the Note states the formula and evaluates it but does not build its shape from e^x; the √π origin.
- **Animation ideas:** Manim: morph e^x → e^(−x) → e^(−|x|) → e^(−x²), then slide a c slider, then show area label going from √π to 1 after dividing (zeJD6dqJ5lo@15:43). Manim 3D: rotate the bell surface e^(−(x²+y²)), peel one cylindrical shell into a rectangle 2πr × e^(−r²) (cy8r7WSuT1I@06:46).
- **Textbook-only parts:** §6 properties beyond the 68-95-99.7 rule (linear transformation, sum of normals) — no priority video; keep Taylor (1997) ch. 5.
- **Contradictions:** none.

### 251 Standard normal and the z-table
- **Sources:** `Khan Academy — "Z-score introduction" (5S-Zfa-vOXs, 5:05)` → §3 standardizing (00:00–04:34). `Khan Academy — "Standard normal table for proportion below" (Fo4kitkFB3I, 4:20)` → §4 the z-table (02:35–04:05), §5 problems. `Khan Academy — "ck12.org exercise: Standard normal distribution and the empirical rule" (2fzYE-Emar0, 8:16)` → §2 standard normal (00:31–01:34), §6 68-95-99.7 (02:07–06:16).
- **Teaching path:**
  1. 5S-Zfa-vOXs 00:00 — Defines z in words first: "number of standard deviations from the mean". 00:31 a population of 7 winged turtles, lengths 2, 2, 3, 2, 5, 1, 6 cm; μ = 3, σ ≈ 1.69. z for 2 = (2−3)/1.69 = −0.59 ("a bit more than half an SD below"); z for 6 = 1.77. 04:04 why care: "how unusual is a point".
  2. Fo4kitkFB3I 00:00 — Heights N(150, 20); Darnell 161.4 cm; sketch the bell, mark 150 and 161.4; z = 11.4/20 = 0.57. 03:05 how to read the table: row 0.5, column 0.07 → 0.7157 → 71.57% are shorter.
  3. 2fzYE-Emar0 00:31 — Draws the standard normal (mean 0, SD 1), ticks −3…3. 02:40 shades the middle 68%; tails share 32% → 16% each → P(Z < 1) = 68 + 16 = 84%, P(Z < −1) = 16%. 05:15 middle 95% → each tail 2.5% → P(Z > 2) = 2.5%.
- **What the video adds:** the "split the 32% leftover into two 16% tails" reasoning by symmetry (2fzYE-Emar0 02:40–03:42) — lets beginners get areas without a table; reading the table row/column on screen (Fo4kitkFB3I 03:05).
- **Animation ideas:** Manim: shade ±1σ (68%), then colour the two leftover tails 16% each, then merge middle + left tail = 84% (2fzYE-Emar0@02:40). Manim: a N(150, 20) curve slides to 0 and squeezes to SD 1 while Darnell's marker moves from 161.4 to z = 0.57 (Fo4kitkFB3I@01:30).
- **Textbook-only parts:** none beyond current (Bradman example from Davis 2000 is an illustration, not a method).
- **Contradictions:** none. (Note gives exact 68.27/95.45/99.73; videos use rounded 68/95/99.7 — consistent.)

### 252 Skewness
- **Sources:** `Khan Academy — "Median, mean and skew from density curves" (JFesFhraX2M, 6:05)` → §4 order of mode/median/mean (00:00–05:38), §2 tail direction (05:08). `Khan Academy — "Classifying shapes of distributions" (Y53_8WRrPzg, 4:28)` → §2–3 shape names, tails (00:00–04:06).
- **Teaching path:**
  1. Y53_8WRrPzg 00:00 — Six real histograms: housefly lengths (symmetric, mirror line drawn), penny dates (left skew, long left tail), state representatives (right skew), coffee cups (left), daily highs (bimodal), die rolls (≈ uniform). Named by "which side the long tail is on".
  2. JFesFhraX2M 00:32 — Median on a density curve = point with equal area left and right; for symmetric shapes it's on the mirror line. 02:05 for a lopsided curve: "you might be tempted to put it at the peak, but the right area is bigger" → move it toward the tail.
  3. 03:07 — Mean = balance point: "put a fulcrum where the shape balances". 04:08 long right tail pulls the fulcrum right of the median → named "right skewed" at 05:08.
- **What the video adds:** mean as the fulcrum / balance point of the curve (JFesFhraX2M 03:37–04:38) — a physical picture for why the mean runs into the tail; median as the equal-area line.
- **Animation ideas:** Manim: a right-skewed density on a seesaw; fulcrum slides from the mode to the balance point (mean) while a vertical line at the median splits area 50/50 (JFesFhraX2M@03:37).
- **Textbook-only parts:** §5 sample skewness formula and §6 the three bands — no priority video; keep Bulmer (1979).
- **Contradictions:** none. Khan's "mean is to the right of the median ⇒ right skew" is a rule of thumb; the Note already cites von Hippel (2005) for exceptions.

### 253 PDF and CDF in practice
- **Sources:** none in priority channels for "PDF/CDF for feature selection" or "CDF to score a decision rule" (these are CampusX-specific uses). CampusX M05 (ADqYqSdtyW8) stays the source. For §4 2D density plots, see 243 (no video either).
- **Teaching path:** n/a.
- **What the video adds:** n/a.
- **Animation ideas:** Plotly: two class-conditional PDFs (e.g. Iris petal length per species) with a draggable threshold; shaded CDF areas show each class's error rate (own design, from the Note's §3).
- **Textbook-only parts:** whole Note — Wasserman *All of Statistics* ch. 7 (empirical CDF), as now.
- **Contradictions:** n/a.

### 260 Kurtosis and Q-Q plots
- **Sources:** `StatQuest — "Quantile-Quantile Plots (QQ plots), Clearly Explained!!!" (okjYjClSjOg, 6:56)` → §6 is a feature normal (00:31), §7 building a Q-Q plot (00:31–04:04), §9 other distributions (04:04–05:06), two-sample Q-Q (05:06–06:37).
- **Teaching path:**
  1. 00:31 — 15 gene-expression values; question: "is this normal?"
  2. 00:45 — Step 1 give each point its own quantile; step 2 "get any normal curve"; step 3 cut the curve into 15 equal-probability pieces → slices at the edges are WIDE, in the middle NARROW (01:01–01:32) — key visual.
  3. 01:32 — Step 4 plot: smallest data quantile 0.6 (horizontal dotted line) vs smallest normal quantile −1.5 (vertical dotted line) → dot at the crossing. 2nd: 1.1 vs −1.2. 3rd: 1.9 vs −0.89. Repeat for all 15.
  4. 03:34 — Draw a straight line; "fit not awesome" → try a uniform distribution, same four steps → points hug the line → uniform fits better (04:35).
  5. 05:06 — Q-Q of two datasets using 4 quartiles each.
- **What the video adds:** equal-probability slices of the normal curve that get wider in the tails (01:01–01:32); the dotted-line crossing construction of each point; comparing against a uniform, not only a normal.
- **Animation ideas:** Manim: normal curve sliced into 15 equal-area strips (wide at edges); for each i, a horizontal line from the data value and a vertical line from the i-th normal quantile meet and leave a dot (okjYjClSjOg@01:01–03:34).
- **Textbook-only parts:** §3–5 kurtosis, excess kurtosis, "not peakedness", kurtosis risk — no StatQuest/Khan/3b1b video on kurtosis; keep Westfall (2014) and current sources. (Non-priority: zedstatistics TM033GCU-SY discusses the peakedness controversy, not downloaded.)
- **Contradictions:** Khan "Sampling distribution of the sample mean" (FXZ2O1Lv-KE 07:08–07:39) says positive kurtosis means "fatter tails and a more pointy peak". The Note (§3.1) is right: kurtosis measures tail extremity only, not peakedness (Westfall 2014, *The American Statistician* 68(3)). Do not use that Khan segment. Q-Q axes match StatQuest (theoretical on x, data on y).

### 261 Uniform and log-normal distributions
- **Sources:** `Khan Academy — "Continuous probability distribution intro" (j8XLYFzTJzE, 9:58)` → §2 uniform PDF height 1/(b−a) (00:31–03:41), areas (03:41–09:53). `StatQuest — "Logs (logarithms), Clearly Explained!!!" (VSi0Z04fWj0, 15:37)` → §3 background for log-normal: log scale makes ×8 and ÷8 symmetric (04:37–06:09), geometric mean (08:13–09:49).
- **Teaching path:**
  - j8XLYFzTJzE (uniform):
    1. 00:31 — X uniform on 0–5, density 0 outside; draws a flat line, asks "at what height?"
    2. 02:04 — Total probability 1 → area of the rectangle = 1 → base 5 → height 1/5.
    3. 03:41 — P(1 ≤ X ≤ 2) = 1 × 1/5 = 1/5; P(4 ≤ X ≤ 4⅓) = 1/15.
    4. 05:45 — Shrinking window around 3: [2.9, 3.1] → 1/25; [2.99, 3.01] → 1/250; [2.999, 3.001] → 1/2500 → exactly 3 → a line with no width → 0.
  - VSi0Z04fWj0 (log idea for log-normal): 00:30 number line 0–8 rewritten as powers of 2; 05:08 on a normal axis 1→8 is far, 1→1/8 is cramped; on log₂ axis both are 3 steps → symmetric. 08:13 qPCR runs 1, 2, 8: mean 3.7 vs geometric mean 2^1.3 = 2.5, less swayed by the outlier.
- **What the video adds:** the height-from-area argument with numbers (1/5) and the shrinking-window sequence 1/25 → 1/250 → 1/2500 (j8XLYFzTJzE 05:45–09:23); log axis symmetry for multiplicative data (VSi0Z04fWj0 05:08) — the intuition for why taking logs of a right-skewed log-normal gives a symmetric bell.
- **Animation ideas:** Manim: rectangle on [0,5] whose height adjusts to 1/5 as area → 1; then a window around 3 shrinks with the probability ticker 1/25, 1/250, 1/2500, 0 (j8XLYFzTJzE@05:45). Manim: number line 1/8…8 morphs to a log₂ axis, then a right-skewed log-normal histogram morphs into a bell (VSi0Z04fWj0@05:08).
- **Textbook-only parts:** §3 log-normal distribution itself (PDF, parameters, why products of factors give it) — no priority video; keep current sources.
- **Contradictions:** none.

### 262 Pareto and power law
- **Sources:** none in StatQuest, Khan Academy or 3Blue1Brown (searched; hits are Shaw Talebi Wcqt49dXtm8 "Pareto, Power Laws, and Fat Tails", 26:34 — not a priority channel, not downloaded). CampusX M06 (U6QCc_3zgUk) stays the video source.
- **Teaching path:** n/a. StatQuest VSi0Z04fWj0 (logs) 00:30–05:39 supports §4 "check on log–log axes" (log turns powers into straight lines).
- **What the video adds:** n/a.
- **Animation ideas:** Manim: Pareto PDF on linear axes morphs to log–log axes where it becomes a straight line of slope −(α+1) (own design).
- **Textbook-only parts:** whole Note — Pareto (1896–97), Clementi and Gallegati (2005), as now; Newman (2005) "Power laws, Pareto distributions and Zipf's law" would be a standard textbook-level reference for §4.
- **Contradictions:** n/a.

### 270 Bernoulli and binomial
- **Sources:** `StatQuest — "The Binomial Distribution and Test, Clearly Explained!!!" (J8jNoF-K8E8, 15:47)` → §3–5 counting by hand and the formula (02:37–10:27), §6 independence condition (14:34). `Khan Academy — "Visualizing a binomial distribution" (NF0lrkqXIkQ, 9:26)` → §3 PMF plot for 5 flips (01:01–05:40), link to the normal (06:11–09:16). `3Blue1Brown — "Binomial distributions | Probabilities of probabilities, part 1" (8idr1WZ1A7Q, 12:34)` → §5 formula with 50 choose 48 (05:51–07:56), §7 simulation (03:42, 06:21). `3Blue1Brown — zeJD6dqJ5lo` 01:36–03:45 Galton board (already credited in the Note).
- **Teaching path:**
  - StatQuest J8jNoF-K8E8 (most beginner-friendly: the formula is reverse-engineered from a hand count):
    1. 00:31 — Hook: do people prefer orange or grape Fanta? 4 vs 3 in 7 people — real preference or chance?
    2. 02:37 — Tiny case: 3 people, answers orange, orange, grape. With no preference p = 0.5: 0.5 × 0.5 × 0.5 = 0.125.
    3. 04:13 — "That's one ORDER." Grape could be 1st, 2nd or 3rd → 3 orders, each 0.125 → 0.375.
    4. 05:15 — Only now the formula; each piece mapped back: n!/(x!(n−x)!) = 3 = "the number of orders we listed"; p^x = 0.5²; (1−p)^(n−x) = 0.5¹. Plug in → 0.375 again. 3 of 3 → 0.125.
    5. 10:27 — 4 of 7: 0.273. 11:30 binomial test p-value: add equally-or-less likely outcomes: 0.273 + 0.164 + 0.055 + 0.008 = 0.5 for orange side, same for grape → p = 1 → can't reject "equally loved".
    6. 14:34 — Condition: one person's answer must not change the next person's probability (independence).
  - Khan NF0lrkqXIkQ: X = heads in 5 fair flips; bars 1/32, 5/32, 10/32, 10/32, 5/32, 1/32 drawn by hand; 06:11 with 5 million flips the bars narrow and the hump approaches a bell curve.
  - 3b1b 8idr1WZ1A7Q: seller with true success rate 0.95; 03:42 simulate batches of 10 reviews (≈60% give 10/10); 06:21 simulate 50-review batches → 26.1% give 48/50; 06:52 exact formula C(50,48) = 1225 × 0.95^48 × 0.05² = 0.261 matches simulation; 08:58 slider on s: the binomial pile slides, highlighted 48th bar's height traced in a lower plot (peaks at s = 0.96) — preview of likelihood (Notes MA-069+).
- **What the video adds:** "count the orders by hand, then show the formula is just that count" (StatQuest 04:13–08:54); simulation-matches-formula (3b1b 06:21–07:56); the binomial-test p-value worked to the end (StatQuest 11:30–14:02).
- **Animation ideas:** Manim: three Fanta cups O-O-G permute into 3 rows, each row labelled 0.125, sum 0.375; then formula pieces light up over the matching parts (J8jNoF-K8E8@04:13–08:54). Plotly: slider on s with the binomial(50, s) bars and the 48-bar highlighted, lower panel tracing P(48 | s) (8idr1WZ1A7Q@08:58).
- **Textbook-only parts:** none beyond current.
- **Contradictions:** Khan NF0lrkqXIkQ 07:45 says the normal arises from "the product of an almost infinite number of random processes"; it is the SUM of many independent pieces that tends to normal (CLT; Feller Vol. II §VIII.4; 3b1b zeJD6dqJ5lo 04:45). Products tend to log-normal (Note MA-029). The Note does not repeat Khan's slip.

### 271 Sampling distribution and the CLT
- **Sources:** `StatQuest — "The Central Limit Theorem, Clearly Explained!!!" (YAlJCEDH2uY, 7:35)` → §4 CLT (01:01–05:09), §7 why it matters (05:09–06:12), §4.1 conditions (06:12–07:12). `Khan Academy — "Sampling distribution of the sample mean" (FXZ2O1Lv-KE, 10:52)` → §3 sampling distributions (01:00–02:31), §5 simulation (03:01–10:40). `3Blue1Brown — "But what is the Central Limit Theorem?" (zeJD6dqJ5lo, 31:15)` → §4 (03:45–05:15), §6 mean nμ, SD √n σ (11:03–15:12), §4.1 assumptions (28:15–30:18).
- **Teaching path:**
  - StatQuest YAlJCEDH2uY first (7 min, one picture repeated):
    1. 01:01 — Uniform(0,1); draw 20 values, take their mean, drop it into a histogram on the right.
    2. 01:33 — Repeat: 10, 20, … 100 means; at 100 overlay a normal curve → "means are normally distributed" (bold).
    3. 03:06 — Same with an exponential population → means again normal.
    4. 05:09 — Why we care: we needn't know the data's distribution to build CIs, t-tests, ANOVA on means.
    5. 06:12 — n ≥ 30 is a rule of thumb (he used n = 20).
  - Khan FXZ2O1Lv-KE: 01:30 names "sampling distribution of the sample mean" and dissects the phrase; 03:33 draws a weird bimodal 32-value population in the onlinestatbook applet; 04:04 animated: 5 draws → mean → dot; 05:04 10,000 trials → bell, mean 14.42 vs population 14.45; 08:39 n = 5 vs n = 25 side by side: n = 25 narrower, less skew.
  - 3b1b zeJD6dqJ5lo (for the √n and assumptions):
    1. 01:36 — Simplified Galton board: each peg ±1, 5 rows → ball position = sum of 5 random ±1.
    2. 06:20 — Weighted die skewed low; sums of 10 → bell. 07:24 four panels: sums of 2, 5, 10, 15 dice — 2 still looks like the die, 15 a clean bell.
    3. 08:59 — Exact distributions (convolutions) replace noisy simulation; 11:03 they drift right and spread out.
    4. 13:06 — Mean of sum = nμ; variances add → SD of sum = √n σ ("it's the variance that adds, not the SD").
    5. 15:12 — Recentre and rescale every sum to mean 0, SD 1 → all approach one universal shape. 22:02 with sum of 50, changing the die's distribution no longer changes the bottom plot.
    6. 25:07 — Worked: 100 fair dice: μ = 3.5, σ = 1.71 → sum mean 350, SD 17.1 → 95% range 316–384; 27:14 divide by 100 → range for the average.
    7. 28:15 — Three assumptions: independent, identically distributed, finite variance; the real Galton board breaks the first two.
- **What the video adds:** recentre-and-rescale animation where every starting distribution converges to one shape (3b1b 15:12, 22:02–23:34); "variance adds, SD grows as √n" (13:39–14:41); n = 5 vs n = 25 side by side (Khan 08:39).
- **Animation ideas:** Manim: top row 4 different die distributions; bottom row standardized sum-of-n distributions; slider n = 2 → 50, the bottom panels converge to N(0,1) (zeJD6dqJ5lo@22:02). Plotly: two histograms of means (n = 5, n = 25) filling up live from the same weird population (FXZ2O1Lv-KE@08:39).
- **Textbook-only parts:** cumulant rate of convergence (skewness γ₁/√n) and infinite-variance failure — keep Feller (1971) §VI.1 and the Notebook.
- **Contradictions:** StatQuest YAlJCEDH2uY 06:12–07:12 says the only fine print is "you must be able to compute a mean (e.g. not Cauchy)". The Note (§4.1, Pareto α = 1.5 Extra) is right that a finite VARIANCE is also needed: Pareto α = 1.5 has a mean but no CLT. Lindeberg–Lévy CLT requires finite variance (Feller Vol. II §VIII.4; 3b1b zeJD6dqJ5lo 29:46 agrees with the Note).

### 272 Estimating a mean with the CLT
- **Sources:** `StatQuest — "The standard error, Clearly Explained!!!" (XNgt7F6FqDU, 11:44)` → §3 sampling distribution of the mean (02:01–06:40), §5–6 σ/√n (08:13). `StatQuest — "Standard Deviation vs Standard Error, Clearly Explained!!!" (A82brFpdr9g, 2:52)` → §6 common mistake / SD vs SE (00:00–02:35).
- **Teaching path:**
  - XNgt7F6FqDU:
    1. 00:00 — Starts from what readers see: scatter of 3 groups, mean bars, red SD error bars, "dynamite plot". Three error-bar types: SD, SE, CI.
    2. 02:01 — Population: normal curve of mouse-weight differences from the mean. Sample 5 mice → mean −0.2, SD 1.923, drawn as mean ± SD.
    3. 03:32 — Rule of thumb 68%/95%.
    4. 04:03 — Second and third samples overlaid; one sample has an extreme point but its mean barely moves — "for a mean to be far out, most points must be far out together, which is rare".
    5. 05:06 — SD of the three means = much narrower bar → named "standard error" (0.86 here).
    6. 06:40 — Any statistic has a standard error (median, SD…). 08:13 formula only for the mean: s/√n. 08:43 bootstrap for everything else: resample 5 values with replacement (1.43, −1.38, −3.11, 1.43, −0.10), mean, repeat, SD of means.
  - A82brFpdr9g: 5 mice × 5 experiments → 5 means on one line; SD of those = SE. Summary: SD = spread within one set; SE = spread of means across sets; plot SD in figures.
- **What the video adds:** overlaying several samples' means to see the SE as a narrower bar than the data SD (XNgt7F6FqDU 04:03–05:37); bootstrap as the "no-formula" route (08:43–10:47).
- **Animation ideas:** Manim: population curve; 5-dot samples drop one after another, each leaving a mean tick; a second axis collects the ticks; final SE bar vs a sample SD bar (XNgt7F6FqDU@04:03).
- **Textbook-only parts:** §8 template (country income) is applied; none textbook-only.
- **Contradictions:** none.

### 280 Confidence intervals: the z-procedure
- **Sources:** `Khan Academy — "Confidence intervals and margin of error" (hlM7zdf7zwU, 11:45)` → §3 why a point estimate is not enough (00:00–01:34), §4 CI and level (04:10–08:52), §8 where the formula comes from (04:10–06:19), margin of error (09:22). `StatQuest — "Confidence Intervals, Clearly Explained!!!" (TqOeMYtOc1w, 6:42)` → §5 two ways to compute (bootstrap way, 01:02–03:36), CI as a visual test (03:36–06:09).
- **Teaching path:**
  - Khan hlM7zdf7zwU (the formula route, matches the Note's z-procedure):
    1. 00:00 — Election runoff, 100,000 voters; asking all is unrealistic → sample n = 100 → p̂ = 0.54; another sample might give 0.58.
    2. 01:34 — Sampling distribution of p̂ drawn as a bell centred on the unknown p, with ±1, 2, 3 SD ticks; SD = √(p(1−p)/n).
    3. 04:10 — "What's the probability p̂ lands within 2 SD of p?" → ≈ 95% (shade). 05:14 flip the statement: p is within 2 SD of p̂.
    4. 06:19 — Problem: SD needs p → replace by p̂ → standard error √(0.54 × 0.46/100) ≈ 0.05.
    5. 08:21 — Interval 0.54 ± 2 × 0.05 = 0.44 to 0.64 → named "confidence interval"; 09:22 margin of error = 2 SE = 0.10.
    6. 10:23 — Correct reading: the METHOD captures p 95% of the time. 10:55 larger n → smaller margin.
  - StatQuest TqOeMYtOc1w (the bootstrap route, for "two ways"): 01:02 weigh 12 female mice → sample mean; 01:32 resample 12 with replacement (one mouse picked twice, one left out), mean, repeat ~10,000 times; 02:33 "a 95% CI is just the interval that covers 95% of the bootstrapped means"; 03:36 values outside the CI have p < 0.05 (visual test); 05:07 female vs male mice: CIs don't overlap → significant; overlap → still need a t-test.
- **What the video adds:** flip from "p̂ within 2 SD of p" to "p within 2 SD of p̂" drawn on the sampling distribution (Khan 04:10–05:47); bootstrap CI as a no-formula alternative (StatQuest 01:32–03:05); non-overlap rule (05:38–06:09).
- **Animation ideas:** Manim: sampling-distribution bell centred at p with a ±2 SD band; a p̂ dot lands; a bracket of the same width is drawn around p̂ and reaches back to p (hlM7zdf7zwU@04:10–05:47). Manim: bootstrap — 12 mouse dots, resampled copies flash, means stack into a histogram, 2.5%/97.5% cut lines drop (TqOeMYtOc1w@01:32–03:05).
- **Textbook-only parts:** none (assumptions §6 are in both videos in brief; keep current sources).
- **Contradictions:** Khan hlM7zdf7zwU 05:14–05:47 says "there is a 95% probability that the population proportion p is within two standard deviations of p̂ = 0.54", and StatQuest TqOeMYtOc1w 04:36 says "the probability that the true mean is in this area has to be less than 0.05". Both read a computed interval as a probability statement about the fixed parameter. The Note (281 §3, Misreading 1) is right for a frequentist interval: the 95% belongs to the procedure (Wasserman *All of Statistics* §6.3.2; Pishro-Nik §9.1.9 cited in the Note). Khan itself gives the correct reading at 10:23.

### 281 Interpreting confidence intervals
- **Sources:** `Khan Academy — "Confidence interval simulation" (bGALoCckICI, 4:25)` → §2 what "95% confident" means (00:31–03:38), §4 width vs n (03:38–04:10). `Khan Academy — "Interpreting confidence level example" (XZAGtQt-lQo, 5:00)` → §3 misreadings (02:36–04:41).
- **Teaching path:**
  1. bGALoCckICI 00:00 — Gumball machine, true share green = 60% (known to us, not to the sampler); samples of 50 → p̂ = 0.60, then 0.52.
  2. 01:01 — Each sample gets a ±2 SE bar; bars move and change length.
  3. 02:03 — Draw 25 samples at a time; counter shows % of intervals containing 0.6: 93% → creeping toward 95%. Misses are drawn in a different colour.
  4. 03:38 — n = 200 → intervals narrower, still ≈ 95% capture.
  5. XZAGtQt-lQo 00:00 — Elephant food, n = 30 days, x̄ = 350 kg, s = 25, 90% CI 341–359. Draws the fixed true mean and stacked intervals from repeated samples (01:01–02:36).
  6. 02:36 — Four multiple-choice readings: (A) "ate 341–359 on 90% of days" — wrong, about days not the mean; (B) "0.9 probability μ is in 341–359" — "tempting, makes μ sound random" (left uneasy); (C) "in repeated sampling, this method captures μ in 90% of samples" — correct; (D) "90% of sample means fall in 341–359" — wrong.
- **What the video adds:** the live capture-rate counter (bGALoCckICI 02:03–03:06); the 4-choice quiz maps exactly onto the Note's three misreadings (XZAGtQt-lQo 02:36–04:41).
- **Animation ideas:** Plotly/Manim: vertical line at the true p; 100 interval bars drop in one by one, green if they cross the line, red if not; running "% captured" counter; then a toggle for n = 50 vs 200 (bGALoCckICI@02:03).
- **Textbook-only parts:** §5 why 95% is the usual level (Fisher's convention) — no video; keep current source. §3 "83% of new means" Extra — own derivation, keep.
- **Contradictions:** Khan XZAGtQt-lQo treats choice B as "uncomfortable" rather than wrong; the Note calls it wrong (frequentist). Note is right under the frequentist definition (Wasserman §6.3.2); the Note's Extra on Bayesian credible intervals already explains the other school.

### 282 The t-procedure
- **Sources:** `Khan Academy — "Introduction to t statistics" (a2rd4Qy8yNI, 4:26)` → §2 σ rarely known (01:02–02:34), §7 why "z with s" fails (02:34–03:34), §6 formula (03:34). `Khan Academy — "Simulation showing value of t statistic" (gLE6y_NwmhQ, 3:14)` → §7 (01:00–03:00). `Khan Academy — "T-statistic confidence interval" (hV4pdjHCKuA, 11:47)` → §5 t-distribution (01:03–02:37), §6 worked interval (03:40–10:27).
- **Teaching path:**
  1. a2rd4Qy8yNI 00:31 — Recap CI = statistic ± z* × SD of its sampling distribution. 02:03 for a mean that SD is σ/√n — but σ is unknown → tempting fix: use s with z*. 03:04 "this underestimates the margin you need" → statisticians invented t: x̄ ± t* s/√n, read from a t-table.
  2. gLE6y_NwmhQ 01:00 — Simulation: μ = 2.0 apples/day, σ = 0.5, n = 12, 95% target. z + σ: ≈ 95% capture. 02:00 z + s: only 92.2% after 625 intervals. 02:30 t + s: back near 95%.
  3. hV4pdjHCKuA 01:03 — Draws a t-distribution: "like a normal but fatter tails"; 95% in the middle; 10 data points → 9 degrees of freedom → t-table two-sided 95% → ±2.262.
  4. 03:40 — Engine emissions: x̄ = 17.17, s = 2.98, n = 10; SE = 2.98/√10 = 0.942; 2.262 × 0.942 = 2.13; algebra on the inequality → 15.04 < μ < 19.30.
- **What the video adds:** the 3-way capture-rate simulation (z+σ / z+s / t+s) showing z+s undercovers (gLE6y_NwmhQ 01:30–03:00) — direct evidence for the Note's §7.
- **Animation ideas:** Plotly: three panels of 100 intervals each (z+σ, z+s, t+s) from the same samples, n = 12, with running capture % 95 / 92 / 95 (gLE6y_NwmhQ@01:30). Manim: normal vs t(df) overlay, df slider 1 → 30, tails thin toward the normal (hV4pdjHCKuA@01:03, own animation).
- **Textbook-only parts:** §5 why s/√n gives a t (Student 1908, Gosset) and degrees of freedom derivation — no priority video; keep current sources.
- **Contradictions:** hV4pdjHCKuA 11:08 ends with "there's a 95% chance that the true population mean will fall in this interval" — same Misreading 1 as above; Note MA-036 is right (frequentist; Wasserman §6.3.2).

### 290 Null and alternative hypotheses
- **Sources:** `StatQuest — "Hypothesis Testing and The Null Hypothesis, Clearly Explained!!!" (0oc49DyA3hU, 14:41)` → §2 the problem (00:31–04:40), §3 null hypothesis (08:48–12:57), §5.3 fail to reject ≠ prove (05:11–08:48). `StatQuest — "Alternative Hypotheses: Main Ideas!!!" (5koKb5B_YWo, 9:50)` → §4 alternative (02:05–08:46).
- **Teaching path:**
  - 0oc49DyA3hU:
    1. 00:31 — Virus, drug A to 3 people: recovery times differ (one eats healthy, one has a stressful job) → random stuff we can't control.
    2. 02:03 — Drug B on 3 others; means differ by 15 h → a hypothesis "A needs 15 h fewer".
    3. 02:36 — Repeat: now A needs 35 h MORE; repeat again (check labels), again → always opposite → confidently reject. Named "reject".
    4. 04:40 — Drugs C vs D: first 13 h, repeats give 12 h and 13.5 h → can't reject 13, but can't confirm it either (12 or 13.5 just as good) → "fail to reject" (08:17).
    5. 08:48 — Which of the infinitely many hypotheses (12, 12.25, 13.1 …) to test? Test "no difference" → named **null hypothesis** at 09:48. Drugs E vs F: 0.5 h then 0.25 h the other way → fail to reject; many people → small random shifts → reject.
    6. 11:55 — Bonus: the null needs no preliminary data, since "no difference" is always 0.
  - 5koKb5B_YWo:
    1. 02:05 — A statistical test needs data, a null, and an alternative.
    2. 03:05 — Hand-wavy picture: distances of all points to ONE overall mean (null) vs to TWO group means (alternative); two-mean distances much shorter → reject (04:08); about the same → fail to reject.
    3. 05:09 — With 3 groups, alternatives differ ("all different" vs "C = D ≠ E") and can change the decision → state the alternative clearly.
    4. 07:13 — Even after rejecting, we don't "accept" the alternative — other alternatives may fit better.
- **What the video adds:** reject vs fail-to-reject built from repeated experiments before any formula (0oc49DyA3hU 02:36–08:17); why the null is "no difference" (there are too many specific hypotheses, 08:48–09:48); one-mean vs two-means distance picture (5koKb5B_YWo 03:05–04:38) — a visual bridge to ANOVA (Note MA-046).
- **Animation ideas:** Manim: two groups of dots; draw residual lines to the pooled mean, then morph them to residuals around two group means; bars of total squared length shrink a lot (reject) or barely (fail) (5koKb5B_YWo@03:05).
- **Textbook-only parts:** §6 the eight steps — CampusX-specific procedure; no video. Keep current sources.
- **Contradictions:** none of substance. StatQuest (07:13) says we never "accept" H₁ because with 3+ groups many alternatives exist; the Note (§5.2) says "we reject H₀, and H₁ is what remains". For the two-hypothesis case the Note's wording is standard (Casella & Berger §8.1); for multi-group tests StatQuest's caution applies — worth one sentence in Note MA-046.

### 291 Rejection region and the z-test
- **Sources:** `Khan Academy — "Hypothesis testing and p-values" (-FtlH4svqx4, 11:27)` → full z-test worked example (00:00–10:56). `Khan Academy — "One-tailed and two-tailed tests" (mvye6X_0upA, 6:34)` → one-tailed vs two-tailed regions (00:31–06:28).
- **Teaching path:**
  1. -FtlH4svqx4 00:00 — 100 rats injected; untreated mean response 1.2 s; sample x̄ = 1.05 s, s = 0.5 s. "Does the drug have an effect?"
  2. 00:31 — H₀: no effect, μ = 1.2 (status quo); H₁: μ ≠ 1.2.
  3. 02:10 — Logic: assume H₀; if getting a result this extreme is very unlikely, reject.
  4. 03:13 — Sampling distribution of x̄ under H₀: normal, mean 1.2, SD ≈ s/√n = 0.5/10 = 0.05.
  5. 05:48 — z = (1.2 − 1.05)/0.05 = 3 → mark −3 SD on the bell.
  6. 07:54 — Both tails beyond ±3: 99.7% inside → 0.3% outside → named p-value = 0.003 (10:26) → below 5% → reject.
  7. mvye6X_0upA 01:01 — Same data, H₁: μ < 1.2 → only the left tail → 0.15% (half of 0.3%).
- **What the video adds:** a complete one-sample z-test with the empirical rule instead of a table (−FtlH4svqx4 05:48–09:26); same data run as two-tailed then one-tailed (mvye6X_0upA).
- **Animation ideas:** Manim: bell at μ₀ = 1.2 with SD 0.05; dot at 1.05 slides to z = −3; both tails shade red (0.3%), then one tail fades (0.15%) when H₁ switches to "<" (−FtlH4svqx4@07:22, mvye6X_0upA@03:18).
- **Textbook-only parts:** the rejection-region (critical value) framing — Khan goes straight to p-values; keep current sources for z_α tables.
- **Contradictions:** minor slip in mvye6X_0upA 05:25: says "0.13%" then "0.15% / 0.0015" for one tail beyond −3. Exact value is Φ(−3) = 0.00135 (any z-table). Khan also uses s in place of σ and still calls it a z-test (fine for n = 100, but the Note's z-test assumes known σ; the t-test is the exact procedure, Note MA-042).

### 292 Errors, power and tails
- **Sources:** `Khan Academy — "Introduction to Type I and Type II errors" (Hdbbx7DIweQ, 5:03)` → §2 the 2×2 error table (02:34–04:39). `StatQuest — "Statistical Power, Clearly Explained!!!" (Rsc5znwR5FA, 8:19)` → §3 power (00:31–07:16). `Khan Academy — "Introduction to power in significance tests" (6_Cuz0QqRWc, 9:45)` → §3–4 what raises power (02:03–09:13). `StatQuest — "StatQuest: One or Two Tailed P-Values" (bsZGt-caXO4, 7:06)` → §5 tails and choosing after looking (02:36–06:12).
- **Teaching path:**
  1. Hdbbx7DIweQ 02:34 — Draws the grid: columns "H₀ true / H₀ false", rows "reject / fail to reject"; fills Type I (reject a true H₀) with P = α (03:37), two "correct" cells, Type II (fail to reject a false H₀).
  2. Rsc5znwR5FA 00:31 — Two mouse-weight curves (special vs normal diet) barely overlapping; small samples → p = 0.0004 → reject; repeated → almost always reject; occasional overlap sample → p > 0.05. Power named at 03:05 = probability of correctly rejecting. 04:08 if both curves are the same, power doesn't apply. 04:39 heavily overlapping curves + 3 mice each → p = 0.34 mostly → low power. 06:14 more measurements → more power.
  3. 6_Cuz0QqRWc 02:03 — Two sampling distributions on one axis: blue under H₀ (μ₁) with α tails shaded orange; red under truth (μ₂). Area of red inside the "don't reject" zone = β (Type II); rest = power (05:39–06:09). Levers: raise α (shifts boundary, but more Type I) 06:39; raise n (both curves narrow) 07:40; less variability 08:11; true μ further from μ₁ 08:41.
  4. bsZGt-caXO4 01:03 — Cancer trial: one-tailed p = 0.03, two-tailed p = 0.06 — tempting to pick one-tailed. 03:09 simulation: 10,000 two-tailed t-tests on identical populations → ~500 false positives (5%). 05:11 rule "switch to one-tailed when it looks good" → ~800 (8%). 06:12 advice: choose before data; prefer two-tailed.
- **What the video adds:** the two-curve power picture with α, β and power as areas, and the four levers (6_Cuz0QqRWc 03:34–09:13) — the Note's §3 likely needs this as its main figure; the 5% → 8% simulation for choosing tails after looking (bsZGt-caXO4 03:09–05:42), matching the Note's 10% Extra.
- **Animation ideas:** Manim: H₀ curve and H₁ curve on one axis; critical line; shade α (orange), β (grey), power (green); sliders animate n (curves narrow, β shrinks), α (line moves) and effect size (H₁ curve slides) (6_Cuz0QqRWc@03:34–09:13). Plotly: histogram of 10,000 null p-values, flat at ~500 per bin, then the "peek-then-one-tail" version with a taller first bin (bsZGt-caXO4@04:10).
- **Textbook-only parts:** exact power computation formula — videos say "fairly difficult to calculate"; keep the Note's derivation and current sources.
- **Contradictions:** none in maths. Advice differs: StatQuest says "when you have a choice, always use two-tailed"; the Note (§5) allows one-tailed for a strong directional reason chosen in advance. Both agree it must be chosen before the data (the Note's Extra shows 10% Type I when chosen after; StatQuest's milder rule gives 8%).

### 300 p-values
- **Sources:** `StatQuest — "p-values: What they are and how to interpret them" (vemZtEM63GY, 11:21)` → §2 definition by intuition (00:32–04:40), §5 threshold α (04:40–08:46), effect size (09:18–10:53). `StatQuest — "How to calculate p-values" (JQc3yx0-Q9E, 25:15)` → §3 coin p-values by counting (01:01–11:53), continuous p-value as tail area (12:24–19:38), §6 one-sided danger (20:09–24:15).
- **Teaching path:**
  - vemZtEM63GY:
    1. 00:32 — 1 person each on drug A (cured) and B (not) → can't conclude (allergy, missed dose, placebo).
    2. 01:35 — 2 each → still can't. 02:06 1,043/1,046 vs 2/1,434 → obvious. 03:37 37% vs 31% → not obvious → "that's where the p-value comes in".
    3. 04:40 — Threshold 0.05; then the key thought experiment at 05:42: give the SAME drug to two groups; usually p = 0.9, but sometimes allergies cluster → p = 0.01 → false positive; 0.05 means 5% false positives when there's no difference.
    4. 07:45 — Choose threshold by stakes: 0.00001 vs 0.2 (ice-cream truck).
    5. 09:49 — Small p ≠ big effect: 6-point difference p = 0.24 vs 1-point difference with more people p = 0.04.
  - JQc3yx0-Q9E:
    1. 01:01 — 2 heads in a row: "is my coin special?" → null: normal coin.
    2. 02:03 — 4 outcomes tree; P(HH) = 0.25. p-value = 3 parts: P(observed) + P(equally rare) + P(rarer) = 0.25 + 0.25 + 0 = 0.5.
    3. 06:42 — Why add equally rare/rarer: "rarest flower" analogy (07:13–08:46).
    4. 09:17 — 4H1T in 5 flips: 32 outcomes (1, 5, 10, 10, 5, 1) → 5/32 + 5/32 + 2/32 = 0.375.
    5. 12:24 — Continuous: Brazilian women's heights, 95% between 142 and 169 cm; observed 142 → p = 0.025 + 0.025 = 0.05; 141 → 0.03; 155.4–156 → p = 1 (adds both sides beyond).
    6. 20:09 — One-sided danger: "super drug" worse (15.5 days) → two-sided p = 0.03 catches it, one-sided p = 0.98 misses it.
- **What the video adds:** same-drug-twice false-positive thought experiment (vemZtEM63GY 05:42–07:13); the three-part p-value recipe on coins, with exact counts (JQc3yx0-Q9E 05:10–11:53); "p-value of a near-average value is 1" (18:06–19:38).
- **Animation ideas:** Manim: 5-flip outcome bars (1, 5, 10, 10, 5, 1)/32; highlight observed 4H1T, then the equally-rare 1H4T, then the rarer 5H and 5T; running sum to 0.375 (JQc3yx0-Q9E@09:49). Plotly: 1,000 same-drug experiments; histogram of p-values with the <0.05 bar marked "false positives ≈ 5%" (vemZtEM63GY@05:42).
- **Textbook-only parts:** none.
- **Contradictions:** vemZtEM63GY 04:08 calls the p-value a number that "quantifies how confident we should be that drug A is different from drug B" — loose; the Note (§4.2) is right that p is P(data this extreme | H₀), not the probability H₀ or H₁ is true (Greenland et al. 2016, cited in the Note). Also note: StatQuest's discrete two-sided p-value adds "equally rare or rarer" outcomes, while the Note's coin example (53 heads, p = 0.309) is the one-sided tail P(X ≥ 53); both are valid definitions for their H₁ — the Note should state which H₁ it uses so the numbers don't seem to clash.

### 301 One-sample t-test
- **Sources:** `Khan Academy — "Example calculating t statistic for a test about a mean" (BJl9WA787-Q, 5:02)` → §4 worked t statistic (00:00–04:35). `Khan Academy — "Conditions for a t test about a mean" (GtokpL4f32s, 5:48)` → §3 assumptions (02:05–05:36).
- **Teaching path:**
  1. BJl9WA787-Q 00:00 — Rory: teachers' mean experience; H₀: μ = 5, H₁: μ < 5; n = 25, x̄ = 4, s = 2.
  2. 01:31 — z would need σ/√n, unknown → replace with s/√n → t.
  3. 03:03 — t = (4 − 5)/(2/5) = −2.5; sketch t-curve, shade the left tail beyond −2.5 = p-value; compare with α.
  4. GtokpL4f32s 00:00 — Sunil: messages/day, n = 7 days, x̄ = 125, s = 44, data strongly right-skewed. Checks 3 conditions: random (02:05), independence (with replacement or n ≤ 10% of population: 7 ≤ 36.5, 02:35), normal (04:05: population normal? n ≥ 30? sample symmetric, no outliers?) → fails all three → t-test not appropriate.
- **What the video adds:** a "conditions fail" example (GtokpL4f32s) — the Note shows a case where we assume normality; the video shows when to refuse the test. The 10% condition for independence.
- **Animation ideas:** Manim: checklist of 3 conditions with the skewed 7-point dot plot; each normal sub-condition ticks red (GtokpL4f32s@04:05). Manim: t(24) curve with left-tail shading at −2.5 (BJl9WA787-Q@03:33).
- **Textbook-only parts:** Shapiro–Wilk test — no priority video; keep current source.
- **Contradictions:** none.

### 302 Two-sample and paired t-tests
- **Sources:** `StatQuest — "StatQuickie: Which t test to use" (nnBJeb_I-q8, 5:10)` → §2 types (00:02–02:39), Welch default (02:07). `Khan Academy — "Two-sample t test for difference of means" (NkGvw18zlGQ, 6:56)` → §3–4 worked two-sample test (00:00–06:47). `Khan Academy — "Example of hypotheses for paired and two-sample t tests" (X0gIJUXz6jc, 3:49)` → §5 paired vs two-sample (00:32–03:39).
- **Teaching path:**
  1. nnBJeb_I-q8 00:02 — Paired = before/after on the same person (blood pressure drug); unpaired = two separate groups (heights A vs B). 01:04 two unpaired kinds: equal variance vs not; recommends the one that doesn't assume equal variance (Welch) — "more conservative".
  2. NkGvw18zlGQ 00:00 — Kaito's tomato fields: H₀ μ_A = μ_B, H₁ ≠. 01:32 t = (x̄_A − x̄_B)/√(s_A²/n_A + s_B²/n_B) = (1.3 − 1.6)/√(0.25/22 + 0.09/24) ≈ −2.44. 05:14 conservative df = min(22, 24) − 1 = 21 → two-tailed p ≈ 0.024 < 0.05 → reject.
  3. X0gIJUXz6jc 00:32 — Two-sample = two populations, two independent samples, estimate μ₁ − μ₂; paired = ONE population, two measurements per subject, take each subject's difference, then the mean difference (01:35). Shoes example: 6 runners, each runs once in each brand → paired; H₁: mean (Zeppo − Harpo) > 0.
- **What the video adds:** the "one population of differences" framing of the paired test (X0gIJUXz6jc 01:35–02:35); a full two-sample example with numbers.
- **Animation ideas:** Manim: 6 runners with two times each; lines connect each pair; the pairs collapse into 6 difference dots on one axis → one-sample t-test on differences (X0gIJUXz6jc@01:35).
- **Textbook-only parts:** Levene's test, pooled SD and the Welch–Satterthwaite df formula, the cross-validation caveat (Dietterich 1998; Nadeau and Bengio 2003) — no priority video; keep current sources.
- **Contradictions:** convention only. Khan uses the conservative df = min(n₁, n₂) − 1 (AP Statistics rule) → df 21; the Note uses Welch–Satterthwaite df (e.g. 54.5, 68.1) as scipy does. Both are valid; Welch–Satterthwaite is exact-er and is what `ttest_ind(equal_var=False)` returns (Welch 1947). Say so in the Note to avoid confusion.

### 330 Events and types of events
- **Sources** (priority order):
  - `Khan Academy — "Probability explained | Independent and dependent events | Probability and Statistics | Khan Academy" (uzkc-qNVoOk, 8:18)` → Note §2 five terms (00:31–03:07 experiment, equally likely outcomes), §4 mutually exclusive and impossible event (06:47–07:23), compound event "even number" (07:23–08:18)
  - `Khan Academy — "Addition rule for probability | Probability and Statistics | Khan Academy" (QE2uR6Z-NcU, 10:43)` → Note §4 mutually exclusive events (09:18–10:43); also feeds Note MA-011 §6 addition rule
  - CampusX — "Master Probability in Data Science ... Part 1" (DUT4WEUngt0, 1:34:05) stays the base source (Hindi; no English captions; Whisper text in transcripts/M13.whisper-en.txt, no timestamps)
- **Teaching path:**
  - uzkc-qNVoOk (the more beginner-friendly of the two for this Note; it starts from zero):
    1. 00:31 draws a fair coin (a quarter, heads side, tails side). Asks P(heads). Names the flip an "experiment" (03:07: "I know this isn't the kind of experiment you're used to").
    2. 01:33 first definition, in words before symbols: "number of equally likely possibilities that meet my conditions / number of equally likely possibilities". Coin: 1/2 = 50%.
    3. 03:07 second view of the same number: run the experiment a million times, what share is heads. Suggests shaking 100–200 coins in a box and counting (04:12). This plants the empirical view used in Note MA-011.
    4. 04:43 die drawn with faces 1, 2, 3 visible. P(1) = 1/6; P(1 or 6) = 2/6 = 1/3 (06:16, first compound event).
    5. 06:47 trick question: P(2 and 3) on one roll = 0, then names this "mutually exclusive" (07:23) and crosses it out. The term arrives only after the impossible case is felt.
    6. 07:53 P(even) = 3/6 = 1/2: an event made of three outcomes.
  - QE2uR6Z-NcU, last part only (09:18): draws the sample space as a box with two separate blobs A and B; "nothing is a member of both sets", so P(A and B) = 0, named mutually exclusive (09:48).
- **What the video adds:**
  - The two meanings of probability (count of outcomes vs long-run share) side by side in the first 4 minutes; the Note splits them across 330 and 331.
  - The "impossible joint event" (2 and 3 on one roll) as the entry point to mutual exclusivity: concrete and memorable.
- **Animation ideas:**
  - Die faces as six tiles; highlight the tiles of an event ("1 or 6", "even", "2 and 3" = nothing lit). Manim. Source uzkc-qNVoOk@05:13–07:53.
  - Sample-space box with two disjoint blobs vs two overlapping blobs, the overlap flashing to 0 area. Manim. Source QE2uR6Z-NcU@09:18.
- **Textbook-only parts:** exhaustive events and the sure event have no short video here; they stay on the CampusX session and Blitzstein & Hwang §2.3 (law of total probability, as currently cited).
- **Contradictions:** none.

### 331 Empirical and theoretical probability
- **Sources** (priority order):
  - `StatQuest with Josh Starmer — "The Main Ideas behind Probability Distributions" (oI3hZJqXJuc, 5:15)` → Note §3 empirical probability from data (00:38–02:49), §5 from empirical to theoretical (02:49–04:34)
  - `Khan Academy — "Experimental versus theoretical probability simulation | Probability | AP Statistics | Khan Academy" (Nos-xOCpQqg, 4:57)` → Note §5 law of large numbers (00:00–04:39)
  - `Khan Academy — "Addition rule for probability" (QE2uR6Z-NcU, 10:43)` → Note §6 addition rule (00:00–09:18)
- **Teaching path:**
  - Nos-xOCpQqg (best for §5; it is a live simulation):
    1. 00:00 states the claim first: experimental probability should get closer to theoretical as trials grow; names it the law of large numbers.
    2. 01:02 opens a coin-flip simulator (fair coin, 50%). Plots "proportion of heads" against "number of tosses".
    3. 01:32 walks the first 10 flips one by one: H → 100%, T → 50%, T → 33%, H → 50%, H → 60%. The line jumps wildly.
    4. 02:35 adds 200 tosses: a long run of heads pushes the line up, then a run of tails pulls it down; after 215 tosses it is "still reasonably different" from 50%.
    5. 03:35 keeps going: ~800 tosses, then past 1,000: 51%, 50.6%, near 50% at 1,210.
    6. 04:08 caveat: divergence is still possible, only less and less likely.
  - oI3hZJqXJuc (best for linking data counts to a curve):
    1. 00:38 "Imagine we measured the height of a lot of people": 5.2 ft goes into the 5–5.5 bin, then 5.8, 5.6, 5.9, 5.1, 6.3 ft, each dropped into a bin. The stack is named a histogram (01:08).
    2. 01:42 reads probability off the stack: most between 5 and 6 ft, very short or tall is rare.
    3. 02:16 halves the bin width: more precise ("half the people are between 5.25 and 5.75 ft").
    4. 02:49 lays a smooth curve over the histogram. Three advantages: a bin with no data still gets a probability (03:23); any interval, e.g. 5.021–5.317 ft, without rounding to bins (03:23–04:00); a curve from mean and sd is cheap when data is scarce (04:00).
    5. 04:34 names both the histogram and the curve "distributions".
  - QE2uR6Z-NcU (addition rule):
    1. 00:00 a bag: 8 green cubes, 9 green spheres, 5 yellow cubes, 7 yellow spheres = 29 objects.
    2. 01:32 P(cube) = 13/29, drawn as a blob inside a box of area 29; P(yellow) = 12/29 (02:35).
    3. 03:07 P(yellow cube) = 5/29, shown as the overlap of the two blobs (04:07).
    4. 04:37 P(yellow or cube): 12 + 13 would count the 5 yellow cubes twice, so 12 + 13 − 5 = 20, 20/29.
    5. 07:12 rewrites 20/29 as 12/29 + 13/29 − 5/29 and only then names the addition rule P(A or B) = P(A) + P(B) − P(A and B) (08:16).
- **What the video adds:**
  - A live picture of the running proportion settling to 0.5 (the Note has the idea; the video shows the early wild swings and the long runs).
  - Histogram → smaller bins → smooth curve: the bridge from empirical counts to a theoretical model.
  - The addition rule derived from counts first, formula last.
- **Animation ideas:**
  - Running proportion of heads vs number of tosses, log x axis, dashed line at 0.5, several seeds. Plotly. Source Nos-xOCpQqg@01:32–04:08.
  - Heights dropping one by one into bins, bins halving, smooth curve fading in. Manim. Source oI3hZJqXJuc@00:38–02:49.
  - Bag of 29 objects sorted into a Venn picture; overlap of 5 counted twice then removed. Manim. Source QE2uR6Z-NcU@04:37–07:12.
- **Textbook-only parts:** the three axioms (§6) have no beginner video; keep MML §6.1.2 as cited.
- **Contradictions:** none.

### 332 Random variables as functions, expected value and variance
- **Sources** (priority order):
  - `StatQuest with Josh Starmer — "Expected Values, Main Ideas!!!" (KLs_7b7SKi4, 13:39)` → Note §3 expected value (01:02–12:19)
  - `Khan Academy — "Variance and standard deviation of a discrete random variable | AP Statistics | Khan Academy" (2egl_5c8i-g, 6:26)` → Note §4 variance (00:30–06:18)
  - Note §2 (random variable as a function) has no matching video; see below.
- **Teaching path:**
  - KLs_7b7SKi4 (primary; builds E[X] from a bet, not from a formula):
    1. 00:31 story: Statsquatch bets $1 that the next person has heard of the movie Troll 2.
    2. 01:02 the data: 37 of 213 people in StatLand have heard of it, 176 have not. 02:33 turns counts into probabilities: 37/213 = 0.17, 0.83.
    3. 03:35 puts outcomes under the probabilities: lose $1 (−1) with 0.17, win $1 (+1) with 0.83.
    4. 04:36 "Can we make this bet 100 times?" 0.17 × 100 = 17 losses → −$17; 0.83 × 100 = 83 wins → +$83; total +$66 (07:12).
    5. 07:12 divide by 100 bets: 0.66 per bet. Only now named "expected value", E(bet) = 0.66, then E(X) = 0.66 (08:12).
    6. 08:44 shows the 100s cancel, leaving Σ x·P(x). Sigma notation explained term by term (09:14).
    7. 10:15 second example: win $10 if heard, lose $1 if not: 10 × 0.17 + (−1) × 0.83 = 0.87.
  - 2egl_5c8i-g:
    1. 00:00 recap: X = workouts per week, values 0–4 with P = 0.1, 0.15, 0.4, 0.25, 0.1; mean 2.1.
    2. 01:01 variance = Σ (x − μ)² P(x), term by term: (0−2.1)²·0.1 + (1−2.1)²·0.15 + (2−2.1)²·0.4 + (3−2.1)²·0.25 + (4−2.1)²·0.1 = 1.19 (03:45).
    3. 03:45 σ = √1.19 ≈ 1.09.
    4. 04:16 draws the bar chart (heights 0.1, 0.15, 0.4, 0.25, 0.1), marks the mean at 2.1 and ±1.09 (≈1 to ≈3.2) to check it "feels reasonable" (05:48).
- **What the video adds:**
  - Expected value as "average gain per bet if repeated many times", derived from 100 bets then divided by 100. The Note goes from the sample mean with repeats; the bet story gives a reason to care.
  - A visual sanity check of σ on the bar chart.
- **Animation ideas:**
  - 100 bets as 100 coins: 17 red (−1), 83 green (+1), sum to +66, then divide to 0.66; then hide the 100s to reveal Σ x P(x). Manim. Source KLs_7b7SKi4@04:36–08:44.
  - PMF bar chart with a vertical line at μ = 2.1 and a bracket ±σ; each bar's squared distance shown as a square whose area is weighted by P. Manim. Source 2egl_5c8i-g@01:01–05:48.
- **Textbook-only parts:** §2 (random variable as a function from outcomes to numbers, dice difference D) and the variance shortcut theorems stay on Grinstead & Snell §6.1–6.2 as cited.
- **Contradictions:** none.

### 340 Venn diagrams and contingency tables
- **Sources** (priority order):
  - `Khan Academy — "Two-way frequency tables and Venn diagrams | Data and modeling | 8th grade | Khan Academy" (l5MrtV7ZN88, 6:22)` → Note §2 Venn (00:31–03:37), §3 contingency table (03:37–06:11), §4 switching views (whole video)
  - `Khan Academy — "Probability with playing cards and Venn diagrams | Probability and Statistics | Khan Academy" (obZzOq_wSCg, 10:02)` → Note §2 overlap and union (04:43–09:55)
- **Teaching path:**
  - l5MrtV7ZN88 (primary; the exact Note topic):
    1. 00:00 12 candies drawn on screen: brown = chocolate outside, "C" = coconut inside.
    2. 00:31 rectangle = "the universe we care about" (all 12); two circles, chocolate and coconut, "not drawn to scale".
    3. 01:32 fills regions by counting: chocolate only 6, both 3 (in the overlap, 02:35), coconut only 1, neither 2 (outside both circles, 03:06). Checks 6+3+1+2 = 12.
    4. 03:37 "Another way": two-way table, rows chocolate / no chocolate, columns coconut / no coconut. Each cell copied from a Venn region: 3, 6, 1, 2.
    5. 05:09 adds totals: column totals 4 and 8, row totals 9 and 3. Says what each total means (9 = all chocolate = 6 + 3).
  - obZzOq_wSCg:
    1. 00:00 52-card deck: 4 suits × 13 ranks.
    2. 01:33 P(Jack) = 4/52 = 1/13; P(heart) = 13/52 = 1/4; P(Jack and heart) = 1/52 (03:42).
    3. 04:43 rectangle of area 52, Jack circle (area 4) overlapping heart circle (area 13); overlap = Jack of hearts.
    4. 07:20 "why not add 4 + 13?" The Jack of hearts is counted twice; general picture of two overlapping areas A + B − C (08:23).
    5. 09:23 answer 16/52 = 4/13.
- **What the video adds:** the one-to-one map "Venn region ↔ table cell" built live with the same 12 objects; the Note states it, the video performs it.
- **Animation ideas:**
  - 12 candy icons fly from the Venn regions into the four table cells, then totals appear. Manim. Source l5MrtV7ZN88@01:32–05:41.
  - Deck of 52 tiles: highlight 4 Jacks and 13 hearts; the shared tile pulses when counted twice. Manim. Source obZzOq_wSCg@07:20–09:23.
- **Textbook-only parts:** none (the base CampusX session ndHDsvqmbuI remains the primary build source).
- **Contradictions:** none.

### 341 Joint, marginal and conditional probability
- **Sources** (priority order):
  - `StatQuest with Josh Starmer — "Conditional Probabilities, Clearly Explained!!!" (_IgyaD7vOOA, 10:56)` → Note §2–§4 (joint table, margins, conditional). Its only English track is a garbled auto-caption (wrong-language speech recognition, unusable; deleted); its content is recapped in the Bayes video below at 00:30–03:05.
  - `StatQuest with Josh Starmer — "Bayes' Theorem, Clearly Explained!!!!" (9wCnvr7Xw4E, 14:00)` → Note §4 conditional (00:30–04:37), §6 Bayes (05:08–11:15)
  - `3Blue1Brown — "Bayes theorem, the geometry of changing beliefs" (HZGCoVF3YvM, 15:11)` → Note §6 Bayes intuition (03:06–09:55)
- **Teaching path:**
  - 9wCnvr7Xw4E (primary for §2–§4 and the algebra of §6):
    1. 00:30 StatLand people as coloured dots, asked if they love candy and/or soda: both 2, candy only 4, soda only 5, neither 3, total 14. Same counts go into a contingency table.
    2. 01:01 each cell / 14 = joint probability; row and column totals = marginal probabilities.
    3. 01:31 P(no candy and soda | soda) = 5/7 = 0.71. Then divides top and bottom by 14 (02:02): same 0.71, now joint / marginal. This is how the conditional formula appears, from counts.
    4. 03:05 keeps the "redundant" form P(no candy and soda | soda) on purpose so the numerator is visibly the same event.
    5. 04:07 changes the condition to "does not love candy": 5/8 = 0.63. Same numerator, different denominator (05:08).
    6. 05:39 Statsquatch bet: solve without the joint. Multiply each conditional by its marginal, set the two equal, divide: Bayes' theorem (08:10). Letters A, B only at 08:41.
    7. 09:11 why it matters: when we only have 0.71, a guess P(soda) ≈ 0.6 and P(no candy) = 0.57, Bayes gives ≈ 0.75 (09:42), different from the full-table 0.63 because the 0.6 was a guess (10:15).
  - HZGCoVF3YvM (best for intuition; use for §6):
    1. 01:01 Steve: "shy, withdrawn, meek and tidy soul". Librarian or farmer?
    2. 02:35 the forgotten fact: about 20 farmers per librarian.
    3. 03:06 representative sample: 10 librarians, 200 farmers drawn as figures. 40% of librarians fit → 4; 10% of farmers fit → 20. P(librarian | description) = 4/24 ≈ 16.7%.
    4. 04:09 mantra: evidence updates prior beliefs, it does not replace them.
    5. 04:39 generalise: hypothesis H, evidence E; names prior (1/21, 05:10), likelihood P(E|H) (05:42), P(E|¬H) (06:14), posterior (07:20).
    6. 08:53 the key diagram: 1×1 square of all possibilities; left strip width P(H); inside it, height P(E|H) shaded; right strip shaded to height P(E|¬H). Evidence "restricts the space" to the shaded parts; the posterior is the left shaded area over all shaded area (09:24). If both heights are equal, nothing changes (irrelevant evidence).
    7. 10:28 aside: Linda problem; "40 out of 100" works better on intuition than "40%".
  - Choice: StatQuest for the table mechanics (it uses the same table as §2–§4); 3Blue1Brown for why Bayes matters and the area diagram (more beginner-friendly for §6 than the algebra).
- **What the video adds:**
  - The 1×1 probability square with shaded strips: a picture of P(H|E) the Note does not have.
  - Bayes derived in 3 lines from two conditionals of the same table cell.
  - The base-rate trap (Steve) as the motivation.
- **Animation ideas:**
  - 3b1b Bayes square: unit square split at P(H) = 1/21; shade 40% of left strip and 10% of right; zoom to the shaded union, show 4/24. Animate sliders for prior and likelihoods. Manim (or Plotly with sliders). Source HZGCoVF3YvM@08:53–09:55.
  - 14 dots in a 2×2 grid (candy × soda); conditioning dims everything outside the given row/column and shows the fraction. Manim. Source 9wCnvr7Xw4E@00:30–05:08.
- **Textbook-only parts:** §5 independence in formulas has partial video cover (KA uzkc-qNVoOk); the Titanic one-feature classifier is the Note's own data. No textbook needed.
- **Contradictions:** none. Note on wording only: 3b1b calls P(E|H) the "likelihood" (05:42); this matches Bayes usage in Note MA-069.

### 350 Linear algebra roadmap
- **Sources** (priority order):
  - `3Blue1Brown — "Essence of linear algebra preview" (kjBOesZCoqc, 5:09)` → Note §2 why ML needs linear algebra (00:42–03:46), §5 resources
  - `StatQuest with Josh Starmer — "Essential Matrix Algebra for Neural Networks, Clearly Explained!!!" (ZTt9gsGcdDo, 30:01)` → Note §2 (18:56–26:40 a neural network written as matrix maths)
  - CampusX — "Linear Algebra Roadmap ..." (rIsCKVyh4dI, 15:48) stays the base source (Hindi; no English captions; Whisper text in transcripts/M15.whisper-en.txt, no timestamps)
- **Teaching path:**
  - kjBOesZCoqc: 00:11 students can compute (matrix product, determinant, eigenvalues) without seeing why; 00:42 geometric vs numeric understanding; 01:42 analogy: learning sine only as an infinite polynomial, never as triangles, then facing physics; 03:14 most courses over-weight the numeric half, computers do that half now; 03:46 plan: short visual series. No worked numbers.
  - ZTt9gsGcdDo (used in full under Note MA-054; here only 18:56–26:40): iris flower, petal and sepal width → weights → ReLU → second weights → species. Shows every step is "row times matrix, add bias".
- **What the video adds:** the "geometric half vs numeric half" framing for why the roadmap goes visual first; a concrete neural network that is only matrix maths.
- **Animation ideas:** none needed for a roadmap Note beyond a module map.
- **Textbook-only parts:** the least-squares remark (Trefethen & Bau Lecture 11) stays textbook.
- **Contradictions:** none.

### 360 Vectors and feature vectors
- **Sources** (priority order):
  - `Khan Academy — "Vector intro for linear algebra | Vectors and spaces | Linear Algebra | Khan Academy" (br7tS1t2SFE, 5:49)` → Note §4 what a vector is (00:00–05:42), §7 column form (03:36)
  - `3Blue1Brown — "Vectors | Chapter 1, Essence of linear algebra" (fNk_zzaMoSs, 9:52)` → Note §4 (00:30–04:36), §5 feature vectors (01:03 house example), §7 (03:36)
  - CampusX — "Supercharge Your ML Journey: Mastering Vectors ... Part 1" (mQewAJb8oJ8, 1:31:57) stays the base source (Whisper text with timestamps: transcripts/M16.whisper-en.timestamped.txt)
- **Teaching path:**
  - fNk_zzaMoSs (more beginner-friendly for an ML reader because it starts from data):
    1. 00:00 three views: physics (arrow), computer science (ordered list), mathematician (anything you can add and scale).
    2. 01:03 house example: [square footage, price] is a 2D vector; "order matters". This is the feature-vector idea.
    3. 02:04 "think of an arrow inside a coordinate system with its tail at the origin".
    4. 02:34 builds the plane: x-axis, y-axis, origin, tick marks; coordinates as walking instructions (right/left, then up/down).
    5. 03:36 convention: write the pair vertically in square brackets to tell vectors from points.
    6. 04:06 adds the z-axis; triplets ↔ 3D arrows, one to one.
  - br7tS1t2SFE: 00:00 "magnitude and direction"; 5 mph is speed (scalar), 5 mph east is velocity (vector, 01:01); arrow of length 5 pointing east; moved arrows are the same vector (02:36); written [5, 0] then [3, 4] (04:39); length 5 by the 3-4-5 triangle (05:11).
- **What the video adds:** the arrow-from-origin habit; walking-instruction reading of coordinates; the same vector seen as arrow, point and list.
- **Animation ideas:**
  - A house as a dot in (sq ft, price) space; an arrow grows from the origin to it; the list [x, y] written vertically beside it. Manim. Source fNk_zzaMoSs@01:03–03:36.
- **Textbook-only parts:** GPU remark (Goodfellow et al. §12.1.2) stays textbook. Bag-of-words recommender is covered by StatQuest e9U0QAFbfLI (see 362).
- **Contradictions:** none of substance. The Note's key point says "a vector is a point"; KA says vectors have no fixed start (02:36) and 3b1b says "arrow with tail at the origin" (02:04), points for collections (see 490-ka at 04:55 in 3b1b ch2). Not a conflict; the Note may add one line that the point is the tip of the arrow from the origin.

### 361 Magnitude, distance and scalar operations
- **Sources** (priority order):
  - `Khan Academy — "Vector dot product and vector length | Vectors and spaces | Linear Algebra | Khan Academy" (WNuIhXo39_k, 9:10)` → Note §2 magnitude (04:13–08:20)
  - `Khan Academy — "Multiplying a vector by a scalar | Vectors and spaces | Linear Algebra | Khan Academy" (ZN7YaSbY3-w, 5:44)` → Note §6 scaling (00:00–05:15)
  - `3Blue1Brown — "Vectors | Chapter 1" (fNk_zzaMoSs, 9:52)` → Note §6 (06:49–08:22)
- **Teaching path:**
  - WNuIhXo39_k §2 part: 04:46 "why define length if I already know it?" Because vectors can have 50 components. 05:17 definition ‖a‖ = √(a1² + … + an²). 05:47 example b = [2, 5]: √(4 + 25) = √29. 06:17 draws b (2 right, 5 up) and shows it is Pythagoras. 07:20 links to dot product: ‖a‖² = a·a (08:20).
  - ZN7YaSbY3-w (primary for §6): 00:00 a = [2, 1] drawn. 00:31 3a = [6, 3], plotted; same direction, 3 times longer (02:05); "the scalar scales" is where the word comes from (02:35). 03:08 −1·a = [−2, −1]: flipped, same length; links to −5 on a number line (03:39). 04:11 −2·a = [−4, −2]: flipped and doubled.
  - fNk_zzaMoSs 06:49: 2× stretches, 1/3 squishes, −1.8 flips then stretches; "scalar" named at 07:21.
- **What the video adds:** number-line analogy for negative scalars; the reason for the word "scalar".
- **Animation ideas:**
  - One arrow [2, 1] morphing through k = 3, 1, 1/3, −1, −2 with a slider; ghost of the original stays. Manim. Source ZN7YaSbY3-w@00:31–05:15 and fNk_zzaMoSs@06:49.
- **Textbook-only parts:** Euclidean distance (§3) and mean centring (§5) have no clean beginner video in the priority channels; they stay on the CampusX session. Scalar addition stays on MML Definition 2.9 + NumPy broadcasting (already flagged in the Note).
- **Contradictions:** none (the Note already says scalar addition is broadcasting, not a vector-space operation).

### 362 Dot product and cosine similarity
- **Sources** (priority order):
  - `StatQuest with Josh Starmer — "Cosine Similarity, Clearly Explained!!!" (e9U0QAFbfLI, 10:14)` → Note §6 cosine similarity (01:32–08:47)
  - `Khan Academy — "Vector dot product and vector length" (WNuIhXo39_k, 9:10)` → Note §3 computing (02:07–04:13)
  - `3Blue1Brown — "Dot products and duality | Chapter 9" (LyGKycYT2v0, 14:11)` → Note §5 geometric meaning (01:24–03:58)
- **Teaching path:**
  - e9U0QAFbfLI (primary for §6):
    1. 00:30 sentences about Troll 2: three positive, one negative; easy by eye, impossible for a month of tweets.
    2. 01:32 tiny example: "Hello World" vs "Hello". Word-count table (02:04).
    3. 02:36 plot: x = count of "hello", y = count of "world". "Hello World" at (1, 1), "Hello" at (1, 0). Lines from the origin; angle 45°; cos 45° = 0.71 (03:06).
    4. 03:37 "Hello Hello Hello" → (3, 0): point moves out, angle unchanged, still 0.71. Length does not matter.
    5. 04:38 same phrase → angle 0, cos = 1; no shared words ("Hello" vs "World") → 90°, cos = 0 (05:11).
    6. 06:15 formula Σ AiBi / (√ΣAi² √ΣBi²) introduced after the picture, plugged in to get 0.71 again (07:15).
    7. 07:46 five words → five dimensions, cannot draw; "I love Troll 2" vs "I love Gymkata" = 0.58 by formula (08:47).
  - WNuIhXo39_k: [2, 5]·[7, 1] = 14 + 5 = 19 (03:40); [1, 2, 3]·[−2, 0, 5] = 13 (04:13).
  - LyGKycYT2v0 §5: 01:24 project w onto the line through v; length of shadow × length of v; negative when the shadow points backwards; 01:55 positive / zero / negative by direction.
- **What the video adds:** the word-count plane picture (cosine = angle between phrase arrows); "repeat the words, angle stays" shows why cosine ignores length.
- **Animation ideas:**
  - Two phrases as arrows in the hello/world plane; drag "Hello" → "Hello Hello Hello"; angle and cos readout stay fixed. Manim. Source e9U0QAFbfLI@02:36–04:38.
  - Shadow (projection) of w on v with sign colour as w rotates around. Manim. Source LyGKycYT2v0@01:24–01:55.
- **Textbook-only parts:** cross product mention (Massey 1983) stays textbook.
- **Contradictions:** apparent only. StatQuest (05:43) says cosine similarity is "between 0 and 1"; the Note (§6) says −1 to 1. Both are right: word counts are never negative, so their angle is at most 90° and the cosine is in [0, 1]; for general vectors the range is [−1, 1] (Manning, Raghavan & Schütze, *Introduction to Information Retrieval*, §6.3.1). Suggest the Note add this one line.

### 363 Equation of a hyperplane
- **Sources** (priority order):
  - `Khan Academy — "Defining a plane in R3 with a point and normal vector | Linear Algebra | Khan Academy" (UJxgcVaNTqY, 13:53)` → Note §4 vector form, §6 normal vector (02:05–13:23)
  - `Khan Academy — "Normal vector from plane equation | Vectors and spaces | Linear Algebra | Khan Academy" (gw-4wltP5tY, 9:58)` → Note §5 what w0 means, §6 (06:57–09:32)
  - `CampusX — "Equation of a Hyper-plane in N dimensions" (10e-b8AgdVA, 15:17)` → whole Note (Hindi, no English captions; Whisper text transcripts/M27.whisper-en.txt, no timestamps)
- **Teaching path:**
  - UJxgcVaNTqY (primary):
    1. 00:31 "the surface of your computer monitor is a plane, whatever angle you hold it". Draws x, y, z axes and a tilted plane. Plane equation ax + by + cz = d (01:01).
    2. 01:34 a point alone does not fix a plane: "you could pivot the plane around that point". Adds a normal vector n (02:05).
    3. 02:36 "imagine the plane as a piece of cardboard"; a yellow arrow drawn on the cardboard; n·a = 0 for every such arrow (03:07).
    4. 04:11 position vectors x0 and x go from the origin to the plane; they do not lie in the plane (04:41). Coffee-table side view (05:11).
    5. 06:13 x − x0 lies in the plane, so n·(x − x0) = 0 (08:30); expands to n1(x − x0) + n2(y − y0) + n3(z − z0) = 0, the form ax + by + cz = d (09:34).
    6. 10:05 example: n = (1, 3, −2), point (1, 2, 3) → x + 3y − 2z = 1 (12:44).
  - gw-4wltP5tY: 06:57 reverse direction: given ax + by + cz = d, the normal is (a, b, c). Example −3x + √2 y + 7z = π → n = (−3, √2, 7) (08:29). 08:59 d only shifts the plane; all planes with the same a, b, c are parallel and share the normal (09:32). This is exactly the Note's "w0 moves it, w tilts it".
- **What the video adds:** the x − x0 argument, which proves w is normal even when the plane does not pass through the origin.
- **Animation ideas:**
  - Tilted plane with normal n; a point x0 on it; a second point x slides around; arrow x − x0 stays in the plane and at 90° to n. Then change d: plane slides along n, normal unchanged. Manim 3D. Source UJxgcVaNTqY@06:13–09:34, gw-4wltP5tY@08:59.
- **Textbook-only parts:** none.
- **Contradictions:** a gap, not an error. Note §6.1 proves w is normal only for w0 = 0 and relies on the "add x0 = 1" trick to cover w0 ≠ 0. That trick puts [w0, w] normal to a hyperplane in n+1 dimensions; it does not by itself show w is normal to the original hyperplane. The KA argument (n·(x − x0) = 0, UJxgcVaNTqY@06:13–09:34) closes it; standard statement in MML §2.8 (affine subspaces) / §12.2 (SVM: w is orthogonal to any vector on the hyperplane, from w·(xa − xb) = 0).

### 440 Role of maths in ML
- **Sources** (priority order):
  - `CampusX — "Role of Mathematics in Machine Learning" (hIMzczMO_Yc, 7:53)` → whole Note (Hindi, no English captions; Whisper text transcripts/M24.whisper-en.txt, no timestamps)
  - No StatQuest, Khan Academy or 3Blue1Brown video covers "what each branch of maths does in ML" as one overview; the per-branch videos are listed under 350 (3b1b preview), 362 (cosine similarity) and 570 (hypothesis testing).
- **Teaching path:** the CampusX video is the only one; its order (linear algebra → calculus → probability → statistics) is the Note's order.
- **What the video adds:** n/a.
- **Animation ideas:** none.
- **Textbook-only parts:** reducible vs irreducible error (ISLR §2.1.1) stays textbook.
- **Contradictions:** none.

### 490 Linear combinations, span and basis
- **Sources** (priority order):
  - `Khan Academy — "Introduction to linear independence | Vectors and spaces | Linear Algebra | Khan Academy" (CrV1xCWdY-g, 15:46)` → Note §7 dependence (00:00–15:31), §6 span of collinear vectors (00:00–04:09)
  - `3Blue1Brown — "Linear combinations, span, and basis vectors | Chapter 2" (k7RM-ot2NWY, 9:59)` → Note §4–§8 (00:45–09:06)
  - `3Blue1Brown — "Vectors | Chapter 1" (fNk_zzaMoSs, 9:52)` → Note §2–§3 (00:00–06:49)
- **Teaching path:**
  - k7RM-ot2NWY (primary; the Note is built from it):
    1. 00:45 i-hat and j-hat; coordinates (3, −2) read as "3 times i-hat plus −2 times j-hat"; named basis (01:17).
    2. 01:47 a different pair of basis vectors (one up-right, one down-right) gives a different but valid coordinate system.
    3. 02:49 "linear combination" named; 03:22 fix one scalar, vary the other: the tip traces a straight line (origin of the word "linear").
    4. 03:22 both scalars free: tips fill the plane; if the two vectors line up, only a line; both zero, only the origin. 03:52 named "span".
    5. 04:55 trick: one vector = arrow, many vectors = points (tips). Span becomes a line or the whole sheet.
    6. 05:58 3D: two vectors' span is a flat sheet through the origin (06:28). Third vector: on the sheet → nothing new; off it → all of 3D ("it unlocks access", 07:30).
    7. 08:35 "linearly dependent" / "independent" named. 09:06 basis = independent set that spans, left as a puzzle.
  - CrV1xCWdY-g (worked numbers, use for §7 examples): [2, 3] and [4, 6] → span is one line (00:00–03:39), named linearly dependent (04:40); [2, 3], [7, 2], [9, 5]: v1 + v2 = v3, so dependent (07:15–08:25); [7, 0], [0, −1] independent, span R² (10:10–11:44); [2,0,0], [0,1,0], [0,0,7] independent in R³ (13:19–14:56).
- **What the video adds:** "fix one scalar → tip draws a line" (why "linear"); arrows for one vector, points for many; 3D third vector leaving the sheet.
- **Animation ideas:**
  - Two vectors v, w with scalar sliders a, b; the tip of av + bw leaves a trail that fills the plane; snap w onto v's line and the trail collapses to a line. Manim. Source k7RM-ot2NWY@03:22–04:22.
  - 3D: sheet spanned by two vectors; third vector lifted off the sheet sweeps out space. Manim 3D. Source k7RM-ot2NWY@05:58–07:30.
- **Textbook-only parts:** none.
- **Contradictions:** none.

### 500 Linear transformations and matrices
- **Sources** (priority order):
  - `Khan Academy — "Matrix vector products as linear transformations | Linear Algebra | Khan Academy" (ondmopWLiEg, 17:04)` → Note §3 linearity algebraically (06:25–15:03)
  - `3Blue1Brown — "Linear transformations and matrices | Chapter 3" (kYB8IZa5AuE, 10:59)` → Note §2–§6 (00:30–10:02)
  - `StatQuest with Josh Starmer — "Essential Matrix Algebra for Neural Networks" (ZTt9gsGcdDo, 30:01)` → Note §7 ML use (18:56–26:40)
- **Teaching path:**
  - kYB8IZa5AuE (primary; much more beginner-friendly than the KA proof, which is all symbols):
    1. 00:30 "transformation" = function; chosen word suggests movement (01:02). Each input vector moves to its output.
    2. 01:32 too many arrows, so vectors become points; every point of an infinite grid moves, a faint copy of the old grid stays behind (02:02).
    3. 02:34 linear = lines stay lines and origin fixed; counter-examples: curvy lines; straight grid but diagonal line bends (03:05). Rule of thumb: grid lines parallel and evenly spaced.
    4. 03:35 "what formula do you give the computer?" Only where i-hat and j-hat land. Example v = −1·i-hat + 2·j-hat; i-hat → (1, −2), j-hat → (3, 0); v lands at −1(1, −2) + 2(3, 0) = (5, 2) (04:41–05:14).
    5. 05:47 general: (x, y) → x(1, −2) + y(3, 0) = (1x + 3y, −2x + 0y). Four numbers fix the map.
    6. 06:17 pack them as columns of a 2×2 matrix; [a b; c d][x; y] = x(a, c) + y(b, d) (06:48–07:22).
    7. 07:54 examples: 90° rotation, columns (0, 1), (−1, 0); shear, columns (1, 0), (1, 1) (08:26); "imagine" matrix with columns (1, 2), (3, 1) (08:59); dependent columns squash the plane onto a line (09:31).
  - ondmopWLiEg: proves A(a + b) = Aa + Ab and A(ca) = c(Aa) column by column (06:25–14:27); 3D games remark (15:34).
- **What the video adds:** the moving grid with a ghost grid; the i-hat/j-hat recipe with the (5, 2) worked example.
- **Animation ideas:**
  - Grid morph for [[1, 3], [−2, 0]] with ghost grid; v = (−1, 2) tracked to (5, 2); then rotation, shear and a rank-1 squash. Manim (LinearTransformationScene). Source kYB8IZa5AuE@04:08–05:14, 07:54–09:31.
- **Textbook-only parts:** formal linearity (MML Definition 2.15) as cited; KA ondmopWLiEg now covers it by video too.
- **Contradictions:** none.

### 510 Matrix multiplication as composition
- **Sources** (priority order):
  - `StatQuest with Josh Starmer — "Essential Matrix Algebra for Neural Networks, Clearly Explained!!!" (ZTt9gsGcdDo, 30:01)` → Note §2 composition (09:15–13:28), §4 computing a product (07:08–11:50), §7 inner sizes and ML (13:28–26:40)
  - `3Blue1Brown — "Matrix multiplication as composition | Chapter 4" (XkY2DOUCWMU, 10:04)` → Note §2–§6 (02:04–09:47)
- **Teaching path:**
  - XkY2DOUCWMU (primary for §2–§6):
    1. 00:00 recap: matrix = landing spots of i-hat, j-hat.
    2. 02:04 rotate 90° then shear: track i-hat → (1, 1), j-hat → (−1, 0); these become the columns of the composition (02:36).
    3. 03:09 long way: rotation then shear applied to a vector; short way: one composition matrix; call it the product (03:39).
    4. 04:10 read right to left, like f(g(x)).
    5. 04:40 numbers only: M1 columns (1, 1), (−2, 0); M2 columns (0, 1), (2, 0). i-hat: M2·(1, 1) = (2, 1); j-hat: M2·(−2, 0) = (0, −2) (05:12–05:42).
    6. 05:42 same with letters: "first column of the composition = left matrix times first column of the right matrix".
    7. 07:12 order: shear then rotate gives i-hat (0, 1), j-hat (−1, 1); rotate then shear gives (1, 1), (−1, 0): different (07:43).
    8. 08:14 associativity "trivial": both mean apply C, then B, then A.
  - ZTt9gsGcdDo (best for ML readers; real-world story):
    1. 02:42 'Squatch's seat at a Taylor Swift concert in Stockholm; axes on the stage.
    2. 03:14 the stage rotates; equations move seat (2, 1) → (−2, −1). 03:46 terminology alert: linear transformation, constant change in → constant change out (04:23–05:28), contrast 2^x nonlinear.
    3. 06:01 coordinates as a 1×2 row matrix, coefficients as a 2×2 matrix; row-times-column (07:41–08:41).
    4. 09:15 she rotates the stage again: (−2, −1) → (−1, 2). 10:49 "why multiply this strange way?" Multiply the two transformation matrices row by column: one combined matrix that sends (2, 1) straight to (−1, 2) (12:21–12:56).
    5. 13:28 sizes must match: columns of the first = rows of the second; transpose flips rows to columns (14:31–16:07).
    6. 18:56 iris neural network: petal and sepal width → weights → +bias → ReLU → weights → +bias → species, all as matrix products (19:31–24:01); PyTorch nn.Linear docs decoded (24:34); attention formula with tiny numbers (27:11–28:46).
  - Choice: 3b1b for the geometry of composition (§2–§6); StatQuest for "why the strange row-by-column rule" with numbers and for §7 (ML).
- **What the video adds:** a story reason for composition (the stage turning twice); reading PyTorch shapes.
- **Animation ideas:**
  - Grid: rotate 90° then shear vs shear then rotate, side by side, final i-hat/j-hat compared. Manim. Source XkY2DOUCWMU@07:12–07:43.
  - Concert seat dot on a rotating stage, two turns, then the single combined turn. Manim. Source ZTt9gsGcdDo@03:14–12:56.
- **Textbook-only parts:** XOR example (Goodfellow et al. §6.1) stays textbook.
- **Contradictions:** convention only. StatQuest writes points as row vectors and multiplies x·W (06:01–08:41), so the matrix applied first is on the left; the Note (§3, from 3b1b) uses columns and reads right to left. Both are right: (W2W1x)ᵀ = xᵀW1ᵀW2ᵀ (MML §2.2.1, transpose of a product). The Note should say this once, since PyTorch nn.Linear uses the row form (ZTt9gsGcdDo@24:34).

### 520 Dot product and duality
- **Sources** (priority order):
  - `3Blue1Brown — "Dot products and duality | Chapter 9, Essence of linear algebra" (LyGKycYT2v0, 14:11)` → whole Note (§2 01:24–01:55, §3 01:55–03:58, §4 04:29–06:30, §5 07:01–11:07, §6 11:37–12:40)
  - No StatQuest or Khan Academy video teaches duality; KA WNuIhXo39_k covers only the numeric dot product (see 362).
- **Teaching path:**
  1. 00:50 numeric rule: [1, 2]·[3, 4] = 1·3 + 2·4; [6, 2, 8, 3]·[1, 8, 5, 3].
  2. 01:24 projection picture: shadow of w on the line through v, times ‖v‖; negative when the shadow points away; sign = same / perpendicular / opposite (01:55).
  3. 02:25 puzzle: why does order not matter? Equal lengths → mirror symmetry; scale v by 2 → both readings double (02:57–03:27).
  4. 03:58 second puzzle: why does "multiply and add" equal projection? Needs linear maps to the number line.
  5. 04:59 visual test of linearity: evenly spaced dots on a line stay evenly spaced on the number line.
  6. 05:29 example map: i-hat → 1, j-hat → −2; vector (4, 3) → 4·1 + 3·(−2) = −2. A 1×2 matrix "looks like a vector tipped on its side" (06:30).
  7. 07:01 "Unlearn what you have learned": a copy of the number line laid diagonally; unit vector u-hat at its 1.
  8. 08:34 projecting onto it is linear; where does i-hat land? By symmetry, at u_x (09:04); j-hat at u_y (09:35). So the matrix is [u_x u_y] and projecting = dotting with u-hat (10:05).
  9. 10:36 scale u-hat by 3: everything triples, so dot with a non-unit vector = project then scale.
  10. 11:37 duality named: every linear map to numbers is a dot product with one unique vector (12:09).
- **What the video adds:** the symmetry argument (i-hat projected on u-hat mirrors u-hat projected on the x-axis); the evenly-spaced-dots test.
- **Animation ideas:**
  - Diagonal number line through the origin; whole plane of dots collapses onto it; i-hat and u-hat mirror projections highlighted. Manim. Source LyGKycYT2v0@07:01–10:05.
- **Textbook-only parts:** matrix factorisation recommender (Koren et al. 2009) stays a paper.
- **Contradictions:** none.

### 530 Eigenvectors and eigenvalues
- **Sources** (priority order):
  - `Khan Academy — "Introduction to eigenvalues and eigenvectors | Linear Algebra | Khan Academy" (PhfbEr2btGQ, 7:43)` → Note §2 (00:33–05:47)
  - `Khan Academy — "Example solving for the eigenvalues of a 2x2 matrix | Linear Algebra | Khan Academy" (pZ6mMVEE89g, 5:39)` → Note §3 (00:31–05:15)
  - `3Blue1Brown — "Eigenvectors and eigenvalues | Chapter 14" (PFDu9oVAE-g, 17:16)` → Note §2–§6 (01:06–16:29)
  - `3Blue1Brown — "The determinant | Chapter 6" (Ip3X9LOh2dk, 10:03)` → Note §3 prerequisite: det = area factor, det 0 = squish (00:31–03:14)
- **Teaching path:**
  - PFDu9oVAE-g (primary; KA is symbol-first and never animates the grid):
    1. 01:06 matrix with columns (3, 0), (1, 2). Follow one vector and its span (the line through it). Most vectors get knocked off their span (01:36).
    2. 02:09 i-hat stays on the x-axis, stretched by 3; every x-axis vector does too.
    3. 02:41 (−1, 1) stays on its diagonal, stretched by 2. Only now named eigenvector and eigenvalue (03:12). Eigenvalue −1/2 would flip and squish (03:43).
    4. 04:14 why care: a 3D rotation's eigenvector is its axis (eigenvalue 1).
    5. 05:18 Av = λv; rewrite λv = (λI)v; (A − λI)v = 0 (06:21–06:54); non-zero v only if A − λI squishes space, det = 0 (07:29).
    6. 07:29 knob picture: matrix columns (2, 1), (2, 3); subtract a variable λ from the diagonal and "turn a knob"; the determinant hits 0 at λ = 1 (08:02).
    7. 09:39 back to (3, 0), (1, 2): det = (3 − λ)(2 − λ) → λ = 2, 3; for λ = 2, solutions on the line through (−1, 1) (10:09).
    8. 10:39 rotation 90°: λ² + 1 = 0, no real eigenvectors; shear (1, 0), (1, 1): (1 − λ)² → only λ = 1, x-axis only (11:44); scale by 2: every vector (12:14).
    9. 12:44 eigenbasis: if i-hat → −1·i-hat, j-hat → 2·j-hat, the matrix is diagonal (13:17); powers are easy (13:50–14:22); change to the eigenbasis to make any such matrix diagonal (14:54–15:59); shear cannot.
  - Ip3X9LOh2dk (prerequisite, needed for step 5): columns (3, 0), (0, 2) turn the unit square into a 3×2 rectangle, area ×6 (00:31–01:02); shear keeps area 1 (01:35); det 0 = squished to a line (03:14); negative det = flipped orientation (03:45).
  - pZ6mMVEE89g (extra numeric practice): A = [1 2; 4 3] → (λ − 1)(λ − 3) − 8 = λ² − 4λ − 5 → λ = 5, −1 (00:31–04:39); names "characteristic polynomial" (04:09).
  - PhfbEr2btGQ: reflection across the line through (1, 2): (1, 2) has λ = 1, (2, −1) has λ = −1 (00:33–05:47). Good second example of a non-stretch eigenvector.
- **What the video adds:** vectors "staying on their span" during the animation; the λ-knob shrinking the determinant to 0; rotation and shear as edge cases.
- **Animation ideas:**
  - Grid morph for [[3, 1], [0, 2]] with many arrows; the ones that stay on their span light up (x-axis yellow ×3, diagonal (−1, 1) pink ×2). Manim. Source PFDu9oVAE-g@01:06–03:12.
  - λ slider on A − λI for [[2, 2], [1, 3]]: the unit square's area shrinks to 0 at λ = 1 (and 4); plot det(λ) beside it. Manim + Plotly. Source PFDu9oVAE-g@07:29–08:02, Ip3X9LOh2dk@00:31–03:14.
- **Textbook-only parts:** spectral theorem (MML Theorem 4.15) and PCA link stay textbook.
- **Contradictions:** none. Sign convention: KA uses det(λI − A) = 0 (pZ6mMVEE89g@00:00), 3b1b and the Note use det(A − λI) = 0. Same roots (they differ by (−1)ⁿ; MML §4.2, Definition 4.5 uses A − λI).

### 560 Poisson distribution
- **Sources** (priority order):
  - `Khan Academy — "Poisson process 1 | Probability and Statistics | Khan Academy" (3z-M6sbGIZ0, 11:01)` → Note §2 what Poisson describes (00:00–02:34), §7 binomial limit setup (02:34–06:43)
  - `Khan Academy — "Poisson process 2 | Probability and Statistics | Khan Academy" (Jkr4FSrNEVY, 12:42)` → Note §3 PMF and §7 limit derivation (00:00–11:12), worked example (11:42–12:14)
  - 365 Data Science BbLfV0wOeyc stays the base source. No StatQuest or 3Blue1Brown video on Poisson exists (searched).
- **Teaching path:**
  - 3z-M6sbGIZ0:
    1. 00:00 a traffic engineer counts cars passing a point; X = cars per hour.
    2. 00:31 two assumptions: every hour is like every other (no rush hour), and hours are independent (01:32).
    3. 02:03 sit and average many hours: λ = 9.3 cars per hour is the expected value.
    4. 02:34 try the binomial: λ = n·p. Make each minute a trial: n = 60, p = λ/60 (03:37). P(X = 3) = C(60, 3)(λ/60)³(1 − λ/60)⁵⁷ (04:10).
    5. 04:41 the flaw: two cars in one minute count as one success. 05:11 use seconds: n = 3,600, p = λ/3600. Still two cars can come within half a second (06:13). So let n → ∞.
    6. 06:43–10:55 two tools: lim (1 + a/x)^x = e^a (07:15–08:52); x!/(x − k)! = x(x − 1)…(x − k + 1), k terms, e.g. 7!/5! = 7·6 (09:22–10:24).
  - Jkr4FSrNEVY:
    1. 00:00 recap; p = λ/n (02:41).
    2. 03:47 expand C(n, k)(λ/n)^k(1 − λ/n)^(n−k), regroup (04:21–05:55).
    3. 06:26 take three limits: n(n−1)…/n^k → 1 (08:28–09:01); (1 − λ/n)^n → e^(−λ) (09:01–09:34); (1 − λ/n)^(−k) → 1 (09:34–10:06).
    4. 10:06 result P(X = k) = λ^k e^(−λ)/k!; "you wouldn't guess it came from the binomial" (10:41).
    5. 11:42 example: λ = 9 cars/hour, P(2 cars) = 9²/2!·e^(−9) = 81/2·e^(−9) (≈ 0.005, left as exercise).
- **What the video adds:** the "slice the hour finer" story behind the binomial limit (minutes → seconds → moments), which the Note states as a result in §7.
- **Animation ideas:**
  - One hour as a strip; car ticks on it; slice into 60 then 3,600 cells; binomial bars for each n converging to the Poisson bars (λ = 9.3). Manim strip + Plotly bars. Source 3z-M6sbGIZ0@02:34–06:13, Jkr4FSrNEVY@06:26–10:41.
- **Textbook-only parts:** football-scores application (Maher 1982) stays a paper; mean = variance = λ (§5) has no video derivation here, keep the current derivation/simulation.
- **Contradictions:** none.

### 570 Choosing a hypothesis test
- **Sources** (priority order):
  - `StatQuest with Josh Starmer — "Hypothesis Testing and The Null Hypothesis, Clearly Explained!!!" (0oc49DyA3hU, 14:41)` → Note §2 one logic for every test (00:00–13:30)
  - `StatQuest with Josh Starmer — "The Binomial Distribution and Test, Clearly Explained!!!" (J8jNoF-K8E8, 15:47)` → Note §4 one categorical feature (10:27–14:34)
  - `StatQuest with Josh Starmer — "Using Linear Models for t tests and ANOVA, Clearly Explained!!!" (R7xd624pR1A, 11:38)` → Note §6, §8 t-test and ANOVA as one method (01:01–10:46)
  - Krish Naik YrhlQB3mQFI stays the base source (outside the priority channels).
- **Teaching path:**
  - 0oc49DyA3hU:
    1. 00:31 drug A to 3 people: recovery times differ (diet, exercise, stress). Drug B to 3 others (01:33). Means differ by 15 h → hypothesis "A needs 15 fewer hours" (02:03).
    2. 02:36 repeat: now A needs 35 more hours; repeat again and again, always opposite → reject the hypothesis (04:09).
    3. 04:40 drugs C and D: 13 h, then 12 h, then 13.5 h (05:44–06:45). Not different enough to reject, not proof either → "fail to reject" (07:46).
    4. 09:18 which of 12, 12.25, 13.1, 13.5 to test? Test "no difference" instead; named the null hypothesis (09:48).
    5. 10:20 drugs E and F: 0.5 h difference that random luck could flip → fail to reject (11:24); with many people → reject (11:55).
    6. 12:26 the null needs no preliminary data: "no difference" is always 0.
  - J8jNoF-K8E8 (§4):
    1. 00:31 orange vs grape Fanta; 4 of 7 prefer orange — real preference or chance?
    2. 02:37 3 people (O, O, G): 0.5³ = 0.125 for that order; three orders → 0.375 (04:13–05:15). Then the binomial formula, term by term (05:49–08:54).
    3. 10:27 4 of 7: 0.273. 11:30 p-value = observed + equally rare + rarer outcomes, both directions; 0.273 + 0.164 + 0.055 + 0.008 = 0.5 for orange, same for grape → p = 1 (13:00–14:02). Cannot reject "equally loved".
  - R7xd624pR1A (§6, §8): 01:01 recap of regression F; 02:04 step 1 overall mean ignoring x; 03:05 control mean 2.2, mutant mean 3.6 are least-squares lines; 04:39 one equation with 1/0 switches = design matrix (06:12); F from SS(mean), SS(fit), p_mean = 1, p_fit = 2 (07:43–08:43); ANOVA with five groups = same steps, p_fit = 5 (09:14–10:16).
- **What the video adds:** "fail to reject" felt through repeated experiments; the binomial (exact) test as the small-sample version of the proportion z-test in §4; t-test and ANOVA as one linear-model recipe.
- **Animation ideas:**
  - Repeated experiments as rows of 3 + 3 dots; their mean differences stacking on a number line around 13 h vs flipping sign. Manim. Source 0oc49DyA3hU@04:40–07:46.
  - Binomial bars for n = 7, p = 0.5; colour the observed bar and all bars as rare or rarer; sum = p-value. Plotly. Source J8jNoF-K8E8@11:30–14:02.
- **Textbook-only parts:** correlation t-test (§7) has no priority-channel video; keep Montgomery and the Note's derivation.
- **Contradictions:** none. Note §4 uses the normal-approximation z-test; StatQuest uses the exact binomial test. Both valid; the exact test is preferred for small n (Agresti, *Categorical Data Analysis*, §1.4).

### 571 Chi-square tests
- **Sources** (priority order):
  - `Khan Academy — "Chi-square distribution introduction | Probability and Statistics | Khan Academy" (dXB3cUGnaxQ, 10:23)` → Note §3 (00:31–10:03)
  - `Khan Academy — "Pearson's chi square test (goodness of fit) | Probability and Statistics | Khan Academy" (2QeDRsxSF9M, 11:48)` → Note §2 statistic, §4 goodness of fit (00:00–11:41)
  - `Khan Academy — "Contingency table chi-square test | Probability and Statistics | Khan Academy" (hpWdDmgsIRE, 17:37)` → Note §5 test of independence (00:00–17:04)
  - No StatQuest or 3Blue1Brown chi-square video exists (searched).
- **Teaching path:**
  - dXB3cUGnaxQ (do first; it defines the curve):
    1. 00:31 X ~ N(0, 1). Q1 = X² (01:34): square a standard normal draw. Q1 is chi-square with 1 df (02:37).
    2. 03:09 Q2 = X1² + X2², 2 df; Q3 adds X3² (06:19).
    3. 04:16 Wikipedia plot of the densities: k = 1 spikes at 0 because a standard normal is usually small and squaring makes it smaller (04:47–05:17); to get 4 you need to draw a 2, which is rare. k = 2 moderates (05:49); larger k shifts right (06:51). Always ≥ 0 (07:21).
    4. 07:52 reading a table: P(Q2 > 2.41) = 0.30 (08:27–09:32), shown as 30% of the area right of 2.41 on the k = 2 curve (10:03).
  - 2QeDRsxSF9M (§4):
    1. 00:00 buying a restaurant; owner claims a weekday customer distribution (10%, 10%, 15%, 20%, 30%, 15%).
    2. 00:30 observed counts 30, 14, 34, 45, 57, 20 (total 200, 03:08). H0: owner is right; α = 5%.
    3. 03:38 expected = 200 × share: 20, 20, 30, 40, 60, 30.
    4. 04:45 χ² = Σ (O − E)²/E, "normalising the error by the expected" (05:16). 100/20 + 36/20 + 16/30 + 25/40 + 9/60 + 100/30 = 11.44 (06:24–08:02).
    5. 09:03 df: six terms, but the last is fixed by the total → 5 (09:34). Critical value 11.07 (10:05). 11.44 > 11.07 → reject (11:07).
  - hpWdDmgsIRE (§5):
    1. 00:00 herb 1, herb 2, placebo (sugar pill, placebo effect 00:31); table sick / not sick: 20/100, 30/110, 30/90; totals 120, 140, 120; 80 sick, 300 not, 380 total (01:01–01:34).
    2. 02:04 H0: herbs do nothing; α = 10% (03:10).
    3. 04:44 pooled rate 80/380 = 21% sick, 79% not (05:14). Expected: 25.3/94.7, 29.4/110.6, 25.3/94.7 (06:15–08:20).
    4. 09:23 χ² over all six cells = 2.53 (12:09).
    5. 12:42 df = (rows − 1)(cols − 1) = 1 × 2 = 2; why: given totals, the last cell in each row/column is not new information (13:47–14:54).
    6. 15:25 critical 4.60 at 10%, 2 df; drawn on the k = 2 curve with the rejection region shaded (16:00); 2.53 sits left of it → cannot reject (17:04).
- **What the video adds:** the chi-square curve built from squared normals (the Note gives it as an "Extra"); expected counts from the pooled rate as a story.
- **Animation ideas:**
  - Draw z ~ N(0,1) repeatedly, square it, drop into a histogram (k = 1); then sum of 2, 3, 5 squares; histograms morph into the chi-square densities. Manim + Plotly. Source dXB3cUGnaxQ@01:34–06:51.
  - Bar pairs observed vs expected for the restaurant; each (O − E)²/E term grows as a block that stacks to 11.44 against a line at 11.07. Plotly. Source 2QeDRsxSF9M@04:45–11:07.
- **Textbook-only parts:** Cochran's expected-count rule (§7) stays on Cochran (1954) as cited.
- **Contradictions:** one slip in the video, the Note is right. hpWdDmgsIRE@04:44–05:14 says "80 out of 380 did not get sick … 21% did not get sick", then uses 21% as the share that got sick (05:45 onward). 80 is the number who got sick (01:34); the computed expected counts and χ² = 2.53 use the correct reading. If the Note borrows this example, label 21% as "sick" (expected count = row total × column total / grand total, NIST e-Handbook §7.4.5.1 / any standard text).

### 572 One-way ANOVA
- **Sources** (priority order):
  - `StatQuest with Josh Starmer — "Using Linear Models for t tests and ANOVA, Clearly Explained!!!" (R7xd624pR1A, 11:38)` → Note §4 splitting variation, §9 ANOVA in ML (09:14–10:46)
  - `Khan Academy — "ANOVA 1: Calculating SST (total sum of squares) | Probability and Statistics | Khan Academy" (EFdlFoHI_0I, 7:39)` → Note §4 SST (00:00–07:23)
  - `Khan Academy — "ANOVA 2: Calculating SSW and SSB (total sum of squares within and between) | Khan Academy" (j9ZPMlVHJVs, 13:20)` → Note §4 SSW, SSB, SST = SSB + SSW (00:00–13:03)
  - `Khan Academy — "ANOVA 3: Hypothesis test with F-statistic | Probability and Statistics | Khan Academy" (Xg8_iSkJpAE, 10:14)` → Note §3 hypotheses (02:03–03:40), §5 F (04:11–06:49), §6 decision (07:19–10:01)
- **Teaching path:**
  - KA 1–3 (primary; one tiny dataset carried through, the most beginner-friendly path):
    1. EFdlFoHI_0I 00:00 nine numbers in three groups: (3, 2, 1), (5, 3, 4), (5, 6, 7). Grand mean 36/9 = 4 = mean of the group means 2, 4, 6 (01:09–02:13).
    2. 02:43 SST = Σ(x − 4)² = 14 + 2 + 14 = 30 (04:50). df = mn − 1 = 8 (05:21–06:22), with the "if you know 8 and the mean, the 9th is fixed" argument.
    3. j9ZPMlVHJVs 00:30 SSW: distance to own group mean: 2 + 2 + 2 = 6 (02:32); df = m(n − 1) = 6 (03:38–04:09).
    4. 05:16 SSB: each point replaced by its group mean, distance to 4: 3·4 + 3·0 + 3·4 = 24 (06:18–09:51); df = m − 1 = 2 (08:51).
    5. 11:27 30 = 24 + 6 and 8 = 2 + 6: the split.
    6. Xg8_iSkJpAE 01:03 story: three foods, test scores. H0: population means equal (02:35). F = (SSB/2)/(SSW/6) = 12/1 = 12 (04:41–06:49). Big numerator = differences come from the means (05:12). α = 10%, F table (2, 6) → critical 3.46 (08:56–09:30); 12 ≫ 3.46 → reject (10:01). F = ratio of two chi-square variables (08:24).
  - R7xd624pR1A (bridge to ML, §9): ANOVA as fitting one mean vs one mean per group, with a design matrix of 1s and 0s (09:14–10:16).
- **What the video adds:** SST = SSB + SSW shown with one 9-point dataset where the numbers are small enough to do by hand; the df add up too.
- **Animation ideas:**
  - Nine dots in three columns; grand-mean line at 4; residual sticks to the grand mean (SST), then to group means (SSW), then group means to grand mean (SSB); squares of the sticks stack into bars 30 = 24 + 6. Manim. Source j9ZPMlVHJVs@00:30–11:27.
  - F(2, 6) density with the 10% tail shaded beyond 3.46 and a marker at 12. Plotly. Source Xg8_iSkJpAE@08:56–10:01.
- **Textbook-only parts:** Kruskal–Wallis (§7 alternative) and Tukey's test stay on the cited papers; the Titanic case is the Note's own data.
- **Contradictions:** none.

### 580 Learning maths for ML
- **Sources** (priority order):
  - `CampusX — "How to Overcome the Fear of Maths in Data Science? | Maths Roadmap for Machine Learning" (o4g4OTyCyDM, 25:58)` → whole Note (Hindi, no English captions; Whisper text transcripts/M38.whisper-en.txt, no timestamps)
  - `3Blue1Brown — "Essence of linear algebra preview" (kjBOesZCoqc, 5:09)` → Note §5 habit 4, learn visually first (00:42–03:14: geometric vs numeric understanding, the sine-as-polynomial analogy)
- **Teaching path:** see 350 for kjBOesZCoqc; the CampusX video is the base.
- **What the video adds:** an outside voice for "visual first" with a concrete analogy (sine taught only as a polynomial, 01:42–02:43).
- **Animation ideas:** none.
- **Textbook-only parts:** none.
- **Contradictions:** none.

---
Captions written (transcripts/maths-video/, .vtt + 30 s .txt): 330-ka-probability-explained, 330-ka-addition-rule, 331-ka-exp-vs-theo-sim, 331-sq-probability-distributions, 332-sq-expected-values, 332-ka-variance-discrete-rv, 340-ka-two-way-tables-venn, 340-ka-cards-venn, 341-sq-bayes, 341-3b1b-bayes-geometry, 350-3b1b-ela-preview, 350-sq-matrix-algebra-nn, 360-ka-vector-intro, 360-3b1b-ch1-vectors, 361-ka-dot-and-length, 361-ka-scalar-mult, 362-sq-cosine-similarity, 362-3b1b-ch9-dot-duality, 363-ka-plane-point-normal, 363-ka-normal-from-plane, 490-ka-linear-independence, 490-3b1b-ch2-span, 500-ka-matvec-as-lt, 500-3b1b-ch3-lin-transf, 510-3b1b-ch4-composition, 530-ka-eigen-intro, 530-ka-eigen-2x2-example, 530-3b1b-ch14-eigen, 530-3b1b-ch6-determinant, 560-ka-poisson-process-1, 560-ka-poisson-process-2, 570-sq-hypothesis-testing, 570-sq-binomial-test, 570-sq-linear-models-ttest-anova, 571-ka-chi-square-distribution, 571-ka-pearson-gof, 571-ka-contingency-chi-square, 572-ka-anova1-sst, 572-ka-anova2-ssw-ssb, 572-ka-anova3-f-test.
Not available: 341-sq-conditional-probability (_IgyaD7vOOA; auto-captions are garbage, deleted; Whisper would need audio, not done); CampusX videos have no English captions (existing Whisper text used).

### 590 Convex and non-convex cost functions
- **Sources:**
  - `StatQuest — "Gradient Descent, Step-by-Step" (sDv4f4s2SB8, 23:54)` → §2 (02:42–05:22: the loss plotted against the intercept), §3.2 background (09:08–13:30)
  - `3Blue1Brown — "Gradient descent, how neural networks learn | Deep Learning Chapter 2" (IHZwWFHWa-w, 20:33)` → §4 (05:44–06:47: several valleys, start point decides), §5.2 (14:47, 19:28)
  - `CampusX — "Difference between convex & non-convex cost function…" (TXVtbgaEyms, 10:00)` → current base; whisper transcript `transcripts/M39.whisper-en.txt` (no timestamps; Hindi-English, not re-downloaded)
  - Files: `transcripts/maths-video/590-*.txt`
- **Teaching path:**
  1. **Loss is a curve over the parameter** (StatQuest): 01:32 three people (weight, height) = (0.5, 1.4), (2.3, 1.9), (2.9, 3.2); slope fixed at 0.64, intercept free. 02:42 intercept 0 → residuals 1.1, 0.4, 1.3 → SSR 3.1. 03:47 **plot SSR (y) against intercept (x)**; 04:19 add points for intercept 0.25, 0.5, … → a U-shaped curve. This is the beginner's first picture of "cost as a function of the parameters".
  2. **Walk down it** (StatQuest 09:39–13:30): slope −5.7 at 0, learning rate 0.1 → step −0.57 → intercept 0.57; then slope −2.3 → 0.8; −0.9 → 0.89; 0.92, 0.94, 0.95 = least-squares answer. Big steps far away, baby steps near the bottom. 15:40 the 3-D bowl over (intercept, slope).
  3. **Convex = chord never below the curve** (CampusX M39): pick two points on the graph, join them, check whether any part of the curve rises above the segment; a wavy curve breaks the rule twice. Strictly convex → one minimum. Linear-regression loss surface: one minimum; neural-network surface: many minima.
  4. **Why non-convex hurts** (3b1b DL2 05:44–06:47): one-input cost curve with several dips; "ball rolling down a hill"; which valley you land in depends on the random start; no guarantee it is the lowest. 06:47 two inputs: surface over the plane, step along −∇. 14:47 the trained digit network found "a happy little local minimum". 19:28 (interview segment) local minima of big networks tend to be of similar quality on structured data.
  - **Which to follow:** StatQuest step 1–2 to make "loss over parameters" concrete with three data points; then CampusX's chord test; then 3b1b's ball-in-valleys picture.
- **What the videos add that the Note lacks:** building the loss curve point by point from three real data points (the Note shows finished surfaces); the "ball rolling into one of several valleys" image; the remark that in large networks local minima are often equally good (3b1b 19:28, a guest quoting a paper — treat as a pointer, not a citable claim).
- **Animation ideas:**
  - SSR-vs-intercept curve drawn dot by dot (intercept 0, 0.25, 0.5 …) next to the data plot whose line moves up; then gradient-descent dots with shrinking steps 0 → 0.57 → 0.8 → … → 0.95. Plotly with frames. Source sDv4f4s2SB8@03:47 and @11:16.
  - Several balls dropped at random starts on a 1-D wavy cost curve, each rolling into a different valley; colour by final loss. Manim. Source IHZwWFHWa-w@06:15.
- **Textbook-only parts:** §3.1 the formal chord inequality with λ, §3.2 "local = global" proof (Boyd & Vandenberghe §4.2.2). The chord idea itself has a CampusX video.
- **Contradictions:** none. Vocabulary trap for the rewrite: Khan Academy's single-variable videos say "concave upward" for what the Note (and Boyd §3.1) call **convex**; "concave" in the Note means curving down.

### 600 Derivatives of one variable
- **Sources** (StatQuest, then 3Blue1Brown *Essence of Calculus*):
  - `StatQuest — "The Chain Rule, Clearly Explained!!!" (wl1myxrtQHQ, 18:24)` → §5.3 (01:34–17:35)
  - `3Blue1Brown — "The paradox of the derivative | Chapter 2" (9vKqVkMQHKk, 16:50)` → §3, §4.1 (00:46–16:33)
  - `3Blue1Brown — "Derivative formulas through geometry | Chapter 3" (S0_qX4VJhMQ, 17:34)` → §4.2, §5.1 (01:43–16:33)
  - `3Blue1Brown — "Visualizing the chain rule and product rule | Chapter 4" (YG15m2VwSjA, 15:56)` → §5.2–5.3 (01:50–14:23)
  - `3Blue1Brown — "Taylor series | Chapter 11" (3d6DsjIBzJ4, 22:20)` → §6 (01:35–14:26)
  - Files: `transcripts/maths-video/600-*.txt`
- **Teaching path:**
  1. **The car** (3b1b ch2): 00:46 car from A to B, 100 m in 10 s, speeds up then slows. 01:20 distance–time curve s(t): shallow, steep, shallow. 02:20 velocity curve = a bump. 03:21 **paradox**: a photo of a car can't tell its speed — you need two moments. 04:25 the speedometer compares t = 3 and 3.01 s → ds/dt with dt = 0.01. 05:31 zoom on the graph: rise over run between two close points. 06:03 how the computer drew the velocity curve: (s(t + 0.01) − s(t))/0.01 for many t. 07:38 the true derivative = what that ratio *approaches* as dt → 0 → secant becomes tangent. 09:12 better phrase: "best constant approximation for the rate of change near a point".
  2. **Worked limit** (ch2 10:16–13:22): s(t) = t³ at t = 2: ((2 + dt)³ − 8)/dt = 12 + 6dt + dt² → 12; generally 3t². 14:25 paradox: is the car moving at t = 0 (derivative 0)? Between 0 and 0.1 s it moves 0.001 m, average 0.01 m/s.
  3. **Power rule from shapes** (ch3): 02:15 graph of x² with tangent slopes 0, steeper at 1, steeper at 2. 02:47 **square of side x grows by dx**: two thin strips x·dx + tiny corner dx²; numbers x = 3, dx = 0.01 → strips 0.06, corner 0.0001 → ignore. 04:51 **cube**: three thin square slabs x²·dx → 3x². 07:58 xⁿ: n ways to pick one dx → n·xⁿ⁻¹. 10:42 **1/x as a puddle of area 1** (width x, height 1/x; width 2 → height ½, width 3 → ⅓). 12:48–16:01 **sin**: walk 0.8 around the unit circle; zoom on a tiny step dθ; the tiny triangle is similar to the big one → d(sin θ)/dθ = cos θ.
  4. **Sum, product, chain** (ch4): 02:22 sin x + x² as two stacked bars at x = 0.5. 04:33 **product as a box** with sides sin x and x², adjustable by a slider x; nudge → bottom strip + side strip ("left d right, right d left"). 08:53 **three number lines** x → x² → sin(x²); x = 1.5 nudged; the nudge is passed down and rescaled at each line → chain rule; 14:23 "the dh's cancel" is a real reflection of the nudges.
  5. **Chain rule with data** (StatQuest): 02:05 weight→height line (slope 2), height→shoe size line (slope ¼); 05:40 d(shoe)/d(weight) = ¼ × 2 = ½ ("beep boop beep"). 06:11 hunger = time² + ½ (exponential-looking curve), craving = √hunger; 07:43 derivative by chain rule = time/√(time² + ½). 09:46 "stuff inside" trick for nested formulas. 11:19 **ML link**: squared residual of a line with only the intercept free; chain rule gives d(residual²)/d(intercept) = −2(observed − intercept − weight); set 0 → intercept = 1.
  6. **Taylor polynomials** (ch11): 00:33 pendulum height ∝ 1 − cos θ; cos θ ≈ 1 − θ²/2 makes it simple. 02:05 find c₀ + c₁x + c₂x² that "spoons" cos x at 0: match value → c₀ = 1; match slope → c₁ = 0; match bending → 2c₂ = −1, c₂ = −½. 05:11 check: cos 0.1 ≈ 0.995. 06:13 add c₃x³ (= 0) and c₄x⁴ = x⁴/24; factorials appear from the cascading power rule (1·2·3·4 = 24). 09:20 each derivative at 0 is controlled by one coefficient. 13:24 eˣ → 1 + x + x²/2! + x³/3! … 14:26 **geometric second-order term**: area under a graph, the extra piece is a triangle ½·f″(a)(x − a)². 17:33–20:36 series, convergence for eˣ at x = 1, 2; ln x around 1 converges only on (0, 2) (radius of convergence).
  - **Which to follow:** 3b1b ch2–ch4 for the derivative, power and product rules (best visuals); StatQuest for the chain rule (simpler numbers, and it ends on the squared residual, which links to ML).
- **What the videos add that the Note lacks:** the car/speedometer story and the "instantaneous rate is an oxymoron" paradox; the cube, the 1/x puddle and the unit-circle triangle for sin; the three-number-line chain rule; StatQuest's weight → height → shoe-size chain with slopes 2 × ¼ = ½; Taylor built term by term by matching value, slope, bending (cos x), with the 0.995 check. The Note already has the secant→tangent GIF, the growing-square GIF and the product-as-rectangle GIF.
- **Animation ideas:**
  - Three stacked number lines x → x² → sin(x²); a nudge at the top propagates down, each arrow rescaled by the local derivative. Manim. Source YG15m2VwSjA@08:53.
  - Taylor polynomials of cos x appearing one term at a time with the "value / slope / bend" labels lighting up; slider for degree. Plotly or Manim. Source 3d6DsjIBzJ4@02:05–08:17.
  - Weight → height → shoe-size: two fitted lines side by side; a dot dragged on the first moves the dot on the second; slopes multiply. Plotly with a slider. Source wl1myxrtQHQ@02:05.
- **Textbook-only parts:** §5.1 table of basic derivatives (exp, log), §6.3 "a polynomial is its own Taylor polynomial" (MML §5.1). Both are simple; no video needed.
- **Contradictions:** none.

### 601 Partial derivatives and gradients
- **Sources** (all Khan Academy, Grant Sanderson):
  - `"Partial derivatives, introduction" (AXqhWeUEtQU, 10:56)` → §3.1–3.2 (00:00–10:52)
  - `"Partial derivatives and graphs" (dfvnCHqzK54, 6:54)` → §3.3 (00:32–06:49)
  - `"Gradient" (tIpKfDc295M, 5:31)` → §4.1 (00:31–05:09)
  - `"Gradient and graphs" (_-02ze7tf08, 6:11)` → §4.2 uphill + length (01:31–05:39)
  - `"Gradient and contour maps" (ZTbTYEMvo10, 6:17)` → §4.2 perpendicular to contours (02:34–06:09)
  - `"Directional derivative" (N_ZRcLheNv0, 7:14)` → §4.2 slope along **u** (01:05–06:42)
  - `"Why the gradient is the direction of steepest ascent" (TEB2z7ZlRAw, 10:32)` → §4.2, Figure 3 (02:02–10:09)
  - `"Multivariable chain rule" (NO3AqAaAE6o, 9:33)` and `"Multivariable chain rule intuition" (hFvBZf-Jx28, 7:47)` → §6.1
  - Files: `transcripts/maths-video/601-*.txt`
- **Teaching path:**
  1. **Nudge picture for an ordinary derivative** (AXqhWeUEtQU 00:31–02:02): f = x² graph at x = 2; dx = "a little nudge", df = resulting change, ratio = slope. Then the same idea **without a graph**: input number line mapped onto output number line; a nudge that comes out 4× bigger means derivative 4.
  2. **Partial derivative as a nudge in one direction** (02:02–04:36): input space drawn as the xy-plane, output as a separate number line; nudge (1, 2) in x only → df; nudge in y only → a different df. Named "partial" because each tells only "part of the story". The curly ∂ introduced.
  3. **Worked example** f = x²y + sin y at (1, 2) (05:07–07:11): plug y = 2 in first, then differentiate: ∂f/∂x = 4x → 4; ∂f/∂y = 1 + cos 2. Then general formulas by "pretending y is a constant" (07:42–09:52): 2xy and x² + cos y.
  4. **Slice picture** (dfvnCHqzK54): same f, point (−1, 1). 01:38 a vertical plane y = 1 cuts the surface; the red curve is traced; 02:38 tangent line slope ≈ −2, matching ∂f/∂x = 2xy = −2. 03:39 slice x = −1 instead; slope = 1 + cos 1, "a bit more than one". 05:14 warning: graphs only work for 2 inputs; the nudge view works for 100.
  5. **Gradient = partials stacked** (tIpKfDc295M): f = x² sin y → ∇f = [2x sin y, x² cos y] (00:31–02:04). It is a vector-valued function (point in, arrow out). 03:06 "the full derivative"; ∇ as "a vector of partial-derivative operators" (memory trick). Grant says he dislikes showing computation first but the link to geometry needs the directional derivative.
  6. **Gradient field on a graph** (_-02ze7tf08): f = x² + y² → ∇f = (2x, 2y). 01:31 pause-and-guess prompt; 02:01 **vector field of arrows pointing away from the origin**, arrows scaled down, colour = length (red long, blue short). 03:03 **hiker on a mountain**: which way to walk to climb fastest? Seen from below the bowl, straight away from the origin = the arrows. 04:06 second example: a surface below the xy-plane with two peaks; arrows point towards the peaks; red (long) arrows where the graph is very steep. Length = steepness.
  7. **Gradient on a contour map** (ZTbTYEMvo10): f = xy, contour lines xy = 2 etc. 02:02 at (2, 1) the gradient is (1, 2). 02:34 field drawn over contours: every arrow crosses a contour line at right angles. 03:38 **zoom in**: contour f = 2 and neighbour f = 2.1 look like parallel straight lines; the shortest step from one to the other is perpendicular.
  8. **Directional derivative** (N_ZRcLheNv0): **v** = (−1, 2) drawn from the point; 02:06 step h**v** with h → 0 (h = 0.001); 03:07 "−1 step in x, 2 steps in y" → ∇_v f = −1·f_x + 2·f_y; general (a, b) → a f_x + b f_y = **w**·∇f (05:10–06:11).
  9. **Why steepest ascent** (TEB2z7ZlRAw): 02:32 unit vector **v** at the point; directional derivative = ∇f·**v**. 04:37 "maximise ∇f·**v** over all unit vectors". 05:07–06:38 **dot product as projection**: project **v** onto ∇f; example projection length 0.7, gradient length 2 → 1.4; swing **v** round → projection grows (0.75 …) until **v** lines up with ∇f. 07:38 "the gradient is a vector that loves to be dotted with other things". 08:08–10:09 slope along ∇f/|∇f| = |∇f| → length = rate of steepest climb.
  10. **Multivariable chain rule** (NO3AqAaAE6o): f = x²y with x = cos t, y = sin t. 00:31 picture: t on a number line → point in the xy-plane → number line. 02:04–04:43 does it the long way (product rule) then 05:14–07:46 spots the pattern f_x·dx/dt + f_y·dy/dt. Intuition video (hFvBZf-Jx28) 01:31–07:09: nudge dt → small move (dx, dy) in the plane → two contributions to df, added.
- **What the videos add that the Note lacks:** the "nudge the input, watch the output number line" picture that works without a graph; the hiker-on-a-mountain story; the zoomed-in parallel contour lines argument for "perpendicular"; the pause-and-guess vector field; the long-way-first chain-rule example where the pattern "pops out". The Note already has the slice figure, the contour+arrows figure and the direction sweep (Figure 3, built from TEB2z7ZlRAw).
- **Animation ideas:**
  - **(top)** Zoom into one point of the contour map until two neighbouring contour lines (f = 2, f = 2.1) look like parallel lines; draw several step arrows from one line to the next; the shortest is perpendicular and matches the gradient. Manim (camera zoom). Source ZTbTYEMvo10@03:38.
  - Hiker: a dot on the 3-D bowl, its shadow on the floor, and the gradient arrow under it; the dot climbs along the arrows. Plotly 3-D with a slider for the step. Source _-02ze7tf08@03:03.
  - Two-number-line nudge picture: a small square of input points in the plane mapped to a short interval on the output line; nudge in x vs in y gives different stretches. Manim. Source AXqhWeUEtQU@02:33.
- **Textbook-only parts:** §5 rules for gradients (MML §5.2.2), §6.2 the 2×2 case, §7 numerical gradient check (MML §5.2 remark). No video.
- **Contradictions:** convention only. KA writes the gradient as a column; the Note (following MML §5.2) uses a row and explains the choice in §4.1 ("Row or column?"). Both give the same numbers. No error.

### 602 Jacobian and matrix gradients
- **Sources** (Khan Academy, Grant Sanderson; then 3Blue1Brown):
  - `Khan Academy — "Jacobian prerequisite knowledge" (VmfTXVG9S0U, 9:22)` → recap for §4.2 (00:31–08:36)
  - `Khan Academy — "Local linearity for a multivariable function" (Vnga_psnCAo, 5:23)` → §1, §4.1 (01:02–05:09)
  - `Khan Academy — "The Jacobian matrix" (bohL918kXQk, 6:22)` → §3.1, §4.1 (01:00–06:10)
  - `Khan Academy — "Computing a Jacobian matrix" (CGbBbH1e7Yw, 3:53)` → §3.1 example (00:30–03:35)
  - `Khan Academy — "The Jacobian Determinant" (p46QWyHQE6M, 8:53)` → §5 (00:00–08:38)
  - `3Blue1Brown — "The determinant | Chapter 6, Essence of linear algebra" (Ip3X9LOh2dk, 10:03)` → §5 background (00:31–09:18)
  - `Khan Academy — "Vector form of the multivariable chain rule" (qZlBjnC3iro, 5:25)` → §6 (00:31–04:42)
  - Files: `transcripts/maths-video/602-*.txt`
- **Teaching path** (KA's 4-video arc is the beginner path; the Note uses polar coordinates, KA uses f(x, y) = (x + sin y, y + sin x)):
  1. **Matrix as a grid move** (VmfTXVG9S0U): matrix [[2, −3], [1, 1]]. 01:32 every point of a blue grid moves to its image; 02:02 grid lines stay straight, parallel, evenly spaced = "linear". 02:32 green **î** lands on (2, 1) = column 1, red **ĵ** on (−3, 1) = column 2; 04:03 multiplication by (1, 0) shows why. 07:36 point (2, 1) lands at (1, 3) = 2·green + 1·red.
  2. **A non-linear map** (Vnga_psnCAo): 01:02 the same grid under (x + sin y, y + sin x) goes "wavy and curly". 01:34 follow one point (π/2, 0) → (π/2, 1): moves straight up 1. 03:06 **zoom box**: a yellow box follows the point while the map plays; inside, with denser grid lines, the grid stays almost straight. 04:09 smaller box → looks exactly linear. Named "locally linear". Question: which 2×2 matrix?
  3. **Build the Jacobian from two tiny steps** (bohL918kXQk): point (−2, 1). 01:00 tiny step right (∂x) → its image has a right component and a down component = (∂f₁/∂x, ∂f₂/∂x) → column 1. 02:32 dividing by the step size "scales it up to a normal-sized vector that doesn't shrink as we zoom". 03:36 tiny step up (∂y) → column 2. 05:09 named "the Jacobian matrix".
  4. **Compute it** (CGbBbH1e7Yw): J = [[1, cos y], [cos x, 1]]; at (−2, 1): [[1, 0.54], [cos(−2), 1]]. 03:03 gut check: image of the first basis vector has a right component ≈ 1 and a downward component ≈ 0.42.
  5. **Determinant = area factor** (p46QWyHQE6M; 3b1b Ip3X9LOh2dk): 3b1b 00:31 diag(3, 2) turns the unit square into a 3×2 rectangle, area 6; 01:02 shear [[1, 1], [0, 1]] keeps area 1; 01:35 any blob ≈ many grid squares, all scaled alike; 02:39 det = ½, det = 0 (squash to a line); 03:45 negative det = flipped paper; 04:45 i-hat swung towards j-hat, det slides through 0 into negatives. KA 00:30 [[3, 1], [0, 2]] → det 6, parallelogram base 3 × height 2. KA 05:37–06:37 det J = 1 − cos x cos y; at (−2, 1): 1 − (−0.42)(0.54) ≈ 1.227 ("stretched a little"); 07:07–08:08 at (0, 1): 1 − 0.54 = 0.46, and the zoomed animation visibly shrinks.
  6. **Chain rule in vector form** (qZlBjnC3iro): 01:02 v(t) = (x(t), y(t)), v′(t) = (dx/dt, dy/dt); 01:33 the sum f_x x′ + f_y y′ is a dot product ∇f(v(t))·v′(t); 03:08 compared to f′(g(t))g′(t); 04:11 works for 100 variables.
  - **Which to follow:** use KA steps 1–5; take 3b1b's area/orientation visuals (step 5) because they explain negative determinants, which KA skips.
- **What the videos add that the Note lacks:** the "follow one point while a zoom box tracks it" visual; the two-tiny-steps construction of each column (the Note states "column j is where a step along input j lands" but never animates the two steps separately); a second point (0, 1) where area *shrinks* (det 0.46 < 1), so the beginner sees both stretch and squash; orientation flip for negative determinants.
- **Animation ideas:**
  - **(top)** Grid under f(x, y) = (x + sin y, y + sin x) or under polar coordinates, with a tracking zoom inset; two tiny arrows (along x, along y) drawn in the inset grow into the Jacobian's columns; readout det J. Manim (ApplyPointwiseFunction + zoomed inset). Source Vnga_psnCAo@03:06, bohL918kXQk@01:00.
  - Same map, two inset boxes side by side at (−2, 1) and (0, 1): one unit square grows to area 1.23, the other shrinks to 0.46. Manim. Source p46QWyHQE6M@06:37–08:08.
  - i-hat rotating towards j-hat and past it; the parallelogram area and the det readout pass 0 and turn negative (paper flips colour). Manim. Source Ip3X9LOh2dk@04:45.
- **Textbook-only parts:** §7 least-squares gradient, §8 gradients of matrices (tensors), §9 identities, §10 autodiff preview (MML §5.3–5.6). No video in the priority channels; 3b1b DL ch. 4 "Backpropagation calculus" (tIeHLnjs5U8) is used by the DL Notes, not here.
- **Contradictions:** none in the Note. Video slip to avoid copying: KA CGbBbH1e7Yw@02:02 says cos(−2) ≈ 0.42; it is −0.416 (cos is even, cos 2 < 0). KA's own determinant video (p46QWyHQE6M@06:07) uses −0.42 correctly.

### 603 Hessian and multivariate Taylor
- **Sources** (priority order; all Khan Academy, Grant Sanderson's multivariable calculus):
  - `Khan Academy — "What is a tangent plane" (cHNT7_F8m1Y, 3:20)` → §4 (00:31–03:06)
  - `Khan Academy — "Local linearization" (o7_zS7Bx2VA, 9:13)` → §4 vector form (01:32–07:40)
  - `Khan Academy — "Symmetry of second partial derivatives" (J08-L2buigM, 7:02)` → §2 (00:01–06:39)
  - `Khan Academy — "What do quadratic approximations look like" (80bJA_tSbo4, 4:42)` → §1 Figure 1, §5.1 (00:00–04:35)
  - `Khan Academy — "Quadratic approximation formula, part 1" (UV5yj5A3QIM, 7:09)` and `"part 2" (szHMvVXxp-g, 9:50)` → §5.1 derivation of the ½ coefficients
  - `Khan Academy — "The Hessian matrix" (LbBcuZukCAw, 6:10)` → §3.1 (00:32–05:39)
  - `Khan Academy — "Vector form of multivariable quadratic approximation" (ClFrIg0PpnM, 8:35)` → §5.1 vector form (03:05–08:08)
  - `Khan Academy — "Multivariable maxima and minima" (ux7EQ3ip2DU, 8:04)`, `"Saddle points" (8aAU4r_pUUU, 5:50)`, `"Second partial derivative test" (m1FhUjMMv30, 11:52)`, `"Second partial derivative test intuition" (sJo7D74PAak, 10:43)` → §3.3 curvature/shape
  - `3Blue1Brown — "Higher order derivatives | Chapter 10, Essence of calculus" (BLkz5LGWihw, 5:39)` → §2 one-variable meaning of a second derivative (00:34–03:43)
  - Files: `transcripts/maths-video/603-*.txt` (13 files)
- **Teaching path** (KA order; the Note currently teaches Hessian (§3) before the tangent plane (§4) and Taylor (§5) — KA goes the other way and is easier for a beginner, because each step adds one term to the last):
  1. **Second derivative in 1-D first (3b1b ch10).** 00:34 graph of f with tangent slope; 01:08 "where it curves upward the slope is increasing → f'' > 0"; two graphs compared at x = 4, both f'' > 0 but one bends more sharply (bigger f''). 02:12–03:43 the notation d²f/dx² read off a picture: two small steps dx to the right give changes df₁, df₂; their difference ddf ~ dx² (with dx = 0.01, ddf ~ 0.0001). 03:43–04:47 acceleration: distance-time graph, velocity bump, "pushed back into your seat" = positive f''. Third derivative = jerk.
  2. **Tangent plane (KA cHNT7_F8m1Y).** 00:31 recall the 1-D tangent line "kissing" a curve; 01:02 3-D surface with a plane "barely kissing" it; the red input dot (x₀, y₀) can be dragged and the plane follows. Goal stated: find a function L(x, y) whose graph is that plane.
  3. **Local linearization formula (KA o7_zS7Bx2VA).** 01:32 L = f(x₀,y₀) + f_x(x₀,y₀)(x−x₀) + f_y(x₀,y₀)(y−y₀); 02:02 why "x − x₀": plugging in x₀ kills the term so L(x₀) = f(x₀). 03:03 "linear" just means each variable times a constant. 03:34–07:40 packs it into vectors: bold **x**, bold **x₀**, dot product → L = f(**x₀**) + ∇f(**x₀**)·(**x** − **x₀**); "works for 100 inputs".
  4. **What a quadratic approximation looks like (KA 80bJA_tSbo4).** 00:00 recap: flat tangent plane on a graph. 00:30–01:31 **key visual:** a "ghostly white" curved surface that hugs the graph near the point; slice it in any direction and you get a parabola; seen from one side it is concave up, from another concave down. 01:31–02:01 move a few steps away and it still matches; only far away does it peel off. 02:33–03:34 the form: a + bx + cy (linear) plus dx² + exy + fy² (quadratic = "two variables multiplied in"). Six constants to tune.
  5. **Fitting the six constants (KA UV5yj5A3QIM, szHMvVXxp-g).** Part 1 01:31–04:08: the three facts that define L (same value, same f_x, same f_y at the point). 04:38–06:12: copy L, add a(x−x₀)² + b(x−x₀)(y−y₀) + c(y−y₀)² so the new terms vanish at the point. Part 2 01:01–03:05 goal: all second partials of Q match f's at the point. 03:35–06:11 differentiate Q twice in x → 2a, so a = ½ f_xx; 06:41–07:42 mixed → b = f_xy; 07:42–08:13 c = ½ f_yy. 09:15 back to the hugging-surface picture.
  6. **Symmetry of mixed partials (KA J08-L2buigM).** Worked example f = sin(x)·y²: 00:31–02:32 tree of derivatives: f_x = cos(x)y², f_y = 2y sin(x); then f_xy = 2y cos(x) by both paths (02:32–04:34). 05:08 Schwarz's theorem (continuous second partials). 06:09 notation order trap: ∂²f/∂y∂x reads right-to-left, f_xy reads left-to-right.
  7. **The Hessian (KA LbBcuZukCAw).** 00:32 "a way to package all the second derivatives". Worked example f = e^{x/2} sin(y): 01:34 f_x = ½e^{x/2} sin y, f_y = e^{x/2} cos y; 02:05–03:37 fills the 2×2 grid: ¼e^{x/2} sin y, ½e^{x/2} cos y (twice), −e^{x/2} sin y. 03:37 a matrix-valued function: plug in (x, y), get a matrix. 04:07–05:39 extend the pattern to 3×3, then n×n ("100 variables → 100×100").
  8. **Vector form (KA ClFrIg0PpnM).** 00:30 colour-codes constant / linear / quadratic terms; 02:02 linear term = ∇f·(**x**−**x₀**); 03:05–04:36 the quadratic term as a quadratic form, with ½f_xy split across both off-diagonal corners; 05:07 "this matrix is almost the Hessian — pull out the ½"; 06:37 final Q(**x**) = f(**x₀**) + ∇f(**x₀**)·(**x**−**x₀**) + ½(**x**−**x₀**)ᵀH(**x₀**)(**x**−**x₀**); 07:38 compares to 1-D Taylor f(a) + f'(a)(x−a) + ½f''(a)(x−a)².
  9. **Why it matters: max/min (KA ux7EQ3ip2DU).** 00:30 motivation: profits of a company; 01:01 machine-learning cost function ("tell the computer to minimize"). 02:02 surface with tallest peak = "Mount Everest" vs smaller peaks; 02:33 tangent plane at the peak is flat; 03:03 tilted plane elsewhere → can walk uphill. 06:39 ∇f = **0** means "tangent plane flat". Not enough: local maxima, minima, saddles also flat.
  10. **Saddle point (KA 8aAU4r_pUUU).** 00:00 visual: a horizontal plane slid up and down until it just touches the peak. 01:00 f = x² − y²: tangent plane at the origin is flat (f_x = 2x, f_y = −2y both 0). 02:02–03:32 slice with constant x → upside-down parabola (looks like a max); slice with constant y → parabola (looks like a min). 04:02 "the x and y directions disagree". 04:34 named after a horse saddle. Cannot happen in 1-D.
  11. **Second partial derivative test (KA m1FhUjMMv30).** 00:00 recap f = x⁴ − 4x² + y²: critical points (0,0), (±√2, 0); origin saddle, others minima. 01:01 counter-example **f = x² + y² + p·xy**: f_xx = f_yy = 2 (both say "minimum") yet at p = 4 it is a saddle. 04:07–05:07 **key animation: slider p from 0 to 4**; the bowl flattens along a diagonal and flips into a saddle at p = 2. 05:37 the test: H = f_xx·f_yy − (f_xy)²; H > 0 → max or min (check f_xx sign), H < 0 → saddle, H = 0 → test fails. 08:10–10:42 numbers: p = 0 → H = 4 (min); p = 4 → 2·2 − 16 = −12 (saddle); crossover p = 2 (flat in one direction).
  12. **Why the test works (KA sJo7D74PAak).** 02:33 slice with a constant-y plane → f_xx is "x concavity"; same for y. 04:04 if x and y disagree (+ × −) the first term is negative → saddle (example x² − y², 04:34). 05:36 if they agree, it becomes "a battle" with the mixed term. 06:06–08:42 **f = xy**: f_xx = f_yy = 0, f_xy = 1; flat along both axes, but a diagonal slice is concave down and the other diagonal concave up → the mixed partial measures "disagreement in the diagonal directions". 09:12 three numbers cover infinitely many directions (the rigorous proof is in KA's article).
- **What the videos add that the Note lacks:**
  - The build-up tangent plane → "ghost surface that hugs the graph" → six constants → Hessian falls out as "the matrix in the quadratic term". The Note defines H first, as a bare grid of numbers, before showing why we need it.
  - The second partial derivative test fxx·fyy − fxy² with the slider animation; the Note goes straight to eigenvalues (§3.3). For a beginner, "x-concavity, y-concavity, diagonal disagreement" comes before eigenvalues; then eigenvalues can be shown as "the slice directions where bending is largest and smallest".
  - Slicing a surface with a vertical plane and reading the curve's concavity — the Note never slices.
  - Second derivative as "change in the change" with two dx steps, and as acceleration (3b1b).
- **Animation ideas:**
  - **(top 1)** Slider p in f = x² + y² + p·xy, p: 0 → 4; show the surface, the x-slice and y-slice parabolas (unchanged, both curving up), a diagonal slice that flattens then turns down at p = 2, and live readouts of H's eigenvalues 2 ± p and det = 4 − p². Manim 3-D (ThreeDScene + ValueTracker). Source m1FhUjMMv30@04:07.
  - **(top 2)** Tangent plane vs quadratic "ghost" surface on our running f = x³ + xy + y² at (1, 1): plane fades in, then curved surface; walk the touching point away and back; error colour-mapped. Plotly 3-D with a slider for the step size. Source 80bJA_tSbo4@00:30.
  - **(top 3)** Saddle x² − y²: two slicing planes (x = 0, y = 0) sweep in, the intersecting curves are traced and lifted out as 2-D parabolas side by side (one up, one down). Manim. Source 8aAU4r_pUUU@02:02.
  - f = xy with a rotating vertical slicing plane; the slice's curvature plotted against angle θ (0 on the axes, ±1 on diagonals). Manim. Source sJo7D74PAak@06:06.
  - Hessian grid filling cell by cell from a derivative tree (∂/∂x, ∂/∂y branches), with the two mixed paths meeting in the same cell. Manim. Sources J08-L2buigM@00:31, LbBcuZukCAw@02:05.
- **Textbook-only parts:** §5.2 higher-order Taylor terms as tensors/outer products (MML §5.8); §6 Newton/BFGS/Laplace approximation (MML ch. 5, Bishop §4.4). No KA/3b1b/StatQuest/CampusX video covers these.
- **Contradictions:** none. Note's §2 notation (∂²f/∂y∂x = "first x then y, read right to left") agrees with KA J08-L2buigM@06:09. Note §3.3's "all eigenvalues positive → bowl" agrees with the KA test, since for 2×2, det H = f_xx f_yy − f_xy² = λ₁λ₂ (MML §4.2, det = product of eigenvalues).

### 610 SVD geometry
- **Sources:** no StatQuest, Khan Academy, 3Blue1Brown or free CampusX video teaches the SVD itself (3b1b has no SVD chapter; KA's linear algebra stops before it; CampusX "Session on Singular Value Decomposition" NPkMoUNkEtQ is members-only). Videos that teach the *pieces* the Note uses:
  - `3Blue1Brown — "Linear transformations and matrices | Chapter 3" (kYB8IZa5AuE, 10:59)` → §2 background, matrix as a grid move (01:32–07:54)
  - `Khan Academy — "Orthogonal matrices preserve angles and lengths" (yDwIfYjKEeo, 11:16)` → §3.2 (02:00–10:54)
  - `3Blue1Brown — "Nonsquare matrices as transformations between dimensions | Chapter 8" (v8VSDg_WQlA, 4:27)` → §6 (00:41–04:15)
  - `3Blue1Brown — "Change of basis | Chapter 13" (P2LTAUO1TdA, 12:51)` → §7 eigen-decomposition as "translate, transform, translate back" (09:06–12:16)
  - Files: `transcripts/maths-video/610-*.txt`
- **Teaching path** (pieces, in the order the Note needs them):
  1. 3b1b ch3 01:32 vectors as points on an infinite grid; 02:34 linear = lines stay lines, origin fixed; 04:41 example: î lands on (1, −2), ĵ on (3, 0) → v = (−1, 2) lands at −1·(1, −2) + 2·(3, 0) = (5, 2); 06:17 columns = landing spots; 07:54 rotation 90°; 08:26 shear (1, 0), (1, 1); 08:59 pause-and-imagine (1, 2), (3, 1).
  2. KA yDwIfYjKEeo 02:00 two arrows with an angle between them, transformed by an orthogonal C: same lengths, same angle ("no distortion"); 03:33 contrast with a non-orthogonal map that stretches and bends the angle; 04:39–07:18 proof ‖Cx‖² = xᵀCᵀCx = xᵀx; 08:18–10:54 cos θ preserved.
  3. 3b1b ch8 00:41 a 3×2 matrix sends the 2-D grid onto a plane inside 3-D (columns (2, 0, −1)-style landing spots); 02:43 a 2×3 matrix squashes 3-D to 2-D; 03:13 1×2 matrix = 2-D to a number line.
  4. 3b1b ch13 01:35 Jennifer's basis b₁, b₂; 04:18 her (−1, 2) is our (−4, 1); 09:06–11:42 rotation in her language = A⁻¹MA, read right to left: "translate to our language, rotate, translate back".
- **What the videos add:** grid-moving animations for orthogonal matrices and for non-square matrices; the "translate–transform–translate back" reading, which is the template for "rotate–stretch–rotate". The circle→ellipse, perpendicular-pair sweep and rotate-stretch-rotate GIF in the Note have no video source and are the Note's own (built from Strang §7.4).
- **Animation ideas:** non-square SVD: a 3×2 matrix taking the unit circle in the plane to an ellipse lying on a tilted plane in 3-D, shown as Vᵀ (rotate in 2-D) → Σ (stretch and lift into 3-D) → U (rotate in 3-D). Manim 3-D. Built on 3b1b v8VSDg_WQlA@00:41 (no SVD source).
- **Textbook-only parts:** §2 circle→ellipse and the perpendicular pair, §4 A = UΣVᵀ, §5 singular values/vectors, §7 SVD vs eigen-decomposition (Strang *Introduction to Linear Algebra* §7.2, §7.4; MML §4.5–4.6). Keep textbook-based.
- **Contradictions:** none.

### 611 Computing the SVD
- **Sources:** no SVD-computation video in the priority channels (CampusX SVD session is members-only). Supporting videos:
  - `3Blue1Brown — "Inverse matrices, column space and null space | Chapter 7" (uQhTuRlWMxw, 12:09)` → §5 rank 1, §6 four subspaces (07:43–11:32)
  - `Khan Academy — "Column space of a matrix" (st6D5OdFV9M, 10:40)` → §6
  - `Khan Academy — "Rowspace and left nullspace" (qBfc57x_RSg, 23:19)` → §6 (14:51 row space, 18:33 left null space)
  - Current non-priority source kept: MIT OCW 18.06 Lecture 29 (Strang).
  - Files: `transcripts/maths-video/611-*.txt`
- **Teaching path:** 3b1b ch7 07:43 two zero-determinant 3×3 cases: squash to a line vs to a plane; 08:15 **rank = number of dimensions of the output**; 08:47 column space = span of the columns = all possible outputs; 09:23 full rank; 09:56 when space squashes onto a line, a whole other line of vectors lands on 0; 10:32 that set = null space (kernel). KA adds the row space and left null space with algebra.
- **What the videos add:** the squash picture for rank 1 (the Note's Figure "C flattens the unit circle onto a segment" is the same idea) and a visual definition of null space ("the line of vectors that land on the origin").
- **Animation ideas:** rank-1 matrix C acting on a grid: the whole plane collapses onto the line through (1, 2) while one direction (the null space) collapses to the origin; highlight v₁ (lands at length 5) and v₂ (lands on 0). Manim. Source uQhTuRlWMxw@09:56.
- **Textbook-only parts:** §2–4 the AᵀA recipe, the sign trap, §7 non-square example, §8 numerical algorithms (Strang §7.2; MML §4.5.2; MIT 18.06 L29). Keep.
- **Contradictions:** none.

### 612 Low-rank approximation
- **Sources:** none in the priority channels (searched StatQuest, KA, 3b1b channel lists and CampusX free videos for "SVD", "singular", "low rank", "image compression"). Stays textbook-based: MML §4.6 and Theorem 4.25 (Eckart–Young).
- **Teaching path / visuals:** none to borrow. Closest beginner bridge is StatQuest PCA (FgakZw6K1QQ, see 613) at 18:41: "a 2-D graph using PC1 and PC2 is a good approximation of the 3-D graph since it accounts for 94% of the variation" — the same idea as keeping k singular values.
- **Animation ideas:** image rebuilt layer by layer (rank 1, 2, 5, 20 …) with a running "% of Σσ² kept" bar; Plotly frames (the Note's §5 already compresses an image; animate it). Source: own (MML §4.6).
- **Contradictions:** n/a.

### 613 SVD in machine learning
- **Sources:**
  - `StatQuest — "Principal Component Analysis (PCA), Step-by-Step" (FgakZw6K1QQ, 21:58)` → §2 PCA through the SVD (00:00–15:55)
  - `Khan Academy — "Least squares approximation" (MC7l96tW8V8, 15:32)` → §5 pseudo-inverse and least squares (01:39–14:59)
  - Files: `transcripts/maths-video/613-*.txt`
- **Teaching path:**
  1. **PCA with SVD** (StatQuest): 00:00 states it does PCA "using SVD". 03:47 average of each gene → centre of the data; shift the cloud so the centre sits on the origin (relative positions unchanged). 04:20 random line through the origin, rotate it. 05:22 two equivalent scores: minimise distances to the line, or maximise distances of projected points from the origin; 05:53–07:25 one point, right triangle a² = b² + c² (fixed hypotenuse), so making c bigger makes b smaller. 07:55 distances d₁…d₆, squared and summed (SS). 09:02 best line = PC1, slope 0.25 ("4 parts gene 1, 1 part gene 2"). 11:11 hypotenuse 4.12 → divide by 4.12 → unit vector = **singular vector**, entries = loading scores. 12:23 **singular value = √(SS)**; eigenvalue = SS averaged. 12:57 PC2 ⟂ PC1: (−0.242, 0.97). 14:15 rotate so PC1 is horizontal → PCA plot. 15:24 variation 15 and 3 → 83% and 17% → scree plot. 16:28 3 genes: 79/15/6%, 2-D plot keeps 94%.
  2. **Least squares as projection** (KA): 01:39 column space of A drawn as a plane, b pokes out of it; 02:39 want x* with Ax* as close to b as possible; 05:21 minimise ‖b − Ax*‖² → name "least squares"; 06:23 closest point = projection of b onto the plane; 09:05 the error vector is perpendicular to the column space → lies in the null space of Aᵀ; 11:42 AᵀAx* = Aᵀb (normal equations).
- **What the videos add:** the rotating-line search for PC1 with the right-triangle argument, and the plain statement "singular value = √(sum of squared projected distances)"; least squares as dropping a perpendicular onto a plane.
- **Animation ideas:**
  - Centred 2-D cloud, a line through the origin rotates; each point's projection foot slides along it; live bar of SS(projected distances) peaking at PC1; then σ₁ = √SS shown. Manim. Source FgakZw6K1QQ@04:20–09:02.
  - Column space as a plane in 3-D, vector b above it, its shadow Ax* and the perpendicular error; drag b. Plotly 3-D. Source MC7l96tW8V8@01:39–09:05.
- **Textbook-only parts:** §3 latent semantic analysis, §4 recommenders (MML Examples 4.14–4.15; Deerwester et al. 1990), the pseudo-inverse via SVD in §5 (MML §4.5). No priority-channel video.
- **Contradictions:** none of substance. StatQuest calls the eigenvalue the "average" of the squared distances without saying n or n − 1; the Note uses σᵢ²/n and notes scikit-learn divides by n − 1 (§2.2). Both are consistent.

### 620 Lagrange multipliers
- **Sources** (all Khan Academy, Grant Sanderson):
  - `"Constrained optimization introduction" (vwUV2IDLP8Q, 6:29)` → §2, §3.1 (00:00–06:06)
  - `"Lagrange multipliers, using tangency to solve constrained optimization" (yuqB-d5MjZA, 8:43)` → §3.2 (00:31–08:22)
  - `"Lagrange multiplier example, part 1" (BSKtQcLQLWU, 7:50)` → §3 worked example (00:00–07:44)
  - `"The Lagrangian" (hQ4UNu1P2kw, 12:28)` → §4.1 (03:33–12:14)
  - `"Meaning of Lagrange multiplier" (m-G3K2GPmEQ, 10:08)` → §4.2 (05:39–09:42)
  - Files: `transcripts/maths-video/620-*.txt`
- **Teaching path:**
  1. **The problem on the 3-D graph** (vwUV2IDLP8Q): maximise f = x²y on the unit circle x² + y² = 1. 01:00 surface of x²y with the circle **lifted onto the surface** as a wiggly loop; 01:30 look for its highest points. 02:00 switch to the flat input plane — contour lines are easier to solve with.
  2. **Slide one contour** (03:01–05:34): one contour of f, value c adjustable: c = 0.1 cuts the circle at 4 points (achievable); c = 1 misses it (impossible); raise c (0.2, 0.3 …) while it still touches. 05:34 the best c is where the contour is **tangent** to the circle. Pause-and-think: how can the gradient help?
  3. **Tangency → parallel gradients** (yuqB-d5MjZA): 01:34 many contours of f with the gradient field (arrows perpendicular to contours); 02:36 name g = x² + y², the circle is a contour of g; 03:07 ∇g also perpendicular there → ∇f = λ∇g, λ named the Lagrange multiplier (04:10). 05:13–07:52 ∇g = (2x, 2y), ∇f = (2xy, x²) → 2xy = 2λx, x² = 2λy, plus x² + y² = 1: three equations, three unknowns.
  4. **Business example** (BSKtQcLQLWU): widgets; labour $20/h, steel $2000/ton; revenue R(h, s) = 100·h^{2/3}·s^{1/3}; budget 20h + 2000s = 20 000. 02:35 the budget is a straight line in the (h, s) plane; revenue contours bend towards it; 06:14 ∇R = λ∇B gives two equations with the same λ.
  5. **Lagrangian** (hQ4UNu1P2kw): 04:04 ℒ(x, y, λ) = R − λ(B − b); 05:35–10:43 ∂ℒ/∂x = 0 and ∂ℒ/∂y = 0 are the tangency equations, ∂ℒ/∂λ = 0 is the constraint. 10:43 "it doesn't help by hand; it's for computers": turns a constrained problem into "gradient = 0".
  6. **Meaning of λ** (m-G3K2GPmEQ): 07:41 λ* = dM*/db, the derivative of the best revenue with respect to the budget. 08:11 example λ* = 2.3: one more dollar of budget → about $2.30 more revenue; 09:11 if λ* > 1, raise the budget.
- **What the videos add that the Note lacks:** the constraint drawn *on the 3-D surface* first (why we want the maximum of a curve on a surface), then the flat contour picture; an everyday money example where λ is a price you can act on ($2.30 per extra $1). The Note already animates the growing level curve and the slide-along gradient for f = x² + 2y² on x + y = 3.
- **Animation ideas:**
  - Surface x²y with the unit circle lifted onto it as a glowing loop; camera rotates down to the top view, the loop flattens to the circle and contours appear. Manim 3-D. Source vwUV2IDLP8Q@01:00.
  - Budget line in the (labour, steel) plane, revenue contours; drag the budget b with a slider and plot best revenue M*(b) beside it with its tangent slope = λ*. Plotly with a slider. Source m-G3K2GPmEQ@07:41, BSKtQcLQLWU@02:35.
- **Textbook-only parts:** §5 inequality constraints/KKT, §6 Lagrangian duality, §7 ridge/lasso constraint view and SVM dual (MML §7.2, §12.3; Boyd & Vandenberghe §5). No KA/StatQuest/3b1b/CampusX free video covers KKT or duality.
- **Contradictions:** none. Sign convention differs but both are right: KA writes ℒ = R − λ(B − b) (maximising), the Note writes ℒ = f + λh with h = 3 − x − y (minimising); both give λ = d(best value)/d(constraint level) (MML §7.2; Boyd & Vandenberghe §5.6). Slip in KA vwUV2IDLP8Q@02:00: says "contour lines for x² + y²" but means x²y.

### 621 Convex sets and functions
- **Sources:**
  - `Khan Academy — "Concavity introduction" (LcEqOzNov4E, 9:54)` → §4.2 in 1-D (02:38–09:26)
  - `Khan Academy — "Second derivative test" (-cW5hCsc9Yc, 6:12)` → §4.2 / §6.2 1-D (00:00–05:43)
  - `Khan Academy — "Second partial derivative test intuition" (sJo7D74PAak)` and `"Saddle points" (8aAU4r_pUUU)` → §4.2 in 2-D (see Note MA-064)
  - `CampusX — convex vs non-convex (TXVtbgaEyms)` → §3 chord test (see Note MA-065)
  - Files: `transcripts/maths-video/621-*.txt`
- **Teaching path:**
  1. **Curving up = slope increasing** (KA LcEqOzNov4E): 00:00 three stacked graphs: f (yellow), f′ (mauve), f″ (blue). 02:38 on the "upside-down U" part the slope goes very positive → less positive → 0 → negative, so f′ falls and f″ < 0; 04:43 on the "U" part f′ rises, f″ > 0. 05:49 names: concave down / concave up. 08:26 critical point + concave down → maximum; + concave up → minimum.
  2. **Second derivative test** (KA -cW5hCsc9Yc): 00:30 sketch of a hump at x = c with flat tangent; 01:31 f′(c) = 0 and f″(c) < 0 → max; 02:05 cup → min; 04:10 quiz: h(8) = 5, h′(8) = 0, h″(8) < 0 → relative max; f″ = 0 → inconclusive.
  3. **Chord test** — CampusX (see 590 step 3).
  4. **2-D: bowl vs saddle via second partials** — KA (see 603 steps 10–12).
- **What the videos add:** the three-stacked-graphs picture (f, f′, f″) that shows "convex ⇔ f′ increasing ⇔ f″ ≥ 0" in one glance. The Note already has animated chord test, tangent-below test and Hessian contour figures.
- **Animation ideas:** f, f′, f″ stacked and sharing one moving vertical cursor; shade green where f″ > 0 (convex part) and red where f″ < 0; the tangent line on f rotates faster/slower to match. Manim. Source LcEqOzNov4E@00:00–05:49.
- **Textbook-only parts:** §2 convex sets (definition, intersections), §5 operations that keep convexity, §6 convex optimisation problems, Slater's condition, duality (MML §7.3; Boyd & Vandenberghe §3.1–3.2, §5.2.3). No StatQuest/KA/3b1b/CampusX video covers convex sets.
- **Contradictions:** none; same "concave up = convex" vocabulary trap as 590.

### 622 Linear and quadratic programming
- **Sources:**
  - `StatQuest — "Optimization with Linear Programming (and the Simplex Algorithm), Main Ideas!!!" (h5o1n1QMcmM, 24:02)` → §2.1–2.2 (01:30–18:31), corner idea in 3-D (19:31–22:37)
  - File: `transcripts/maths-video/622-sq-linear-programming.txt`
- **Teaching path** (StatQuest):
  1. 01:30 factory: cookie mix $3/kg, donut mix $2/kg → revenue 3c + 2d. 02:00 Squatch: "just make loads" — no: only 10 kg flour; cookie uses 0.4 kg/kg, donut 0.5 kg/kg → 0.4c + 0.5d ≤ 10.
  2. 03:02 intercepts: only cookie → 25 kg (dot at (0, 25)); only donut → 20 kg; join → line; 04:07 **yellow feasible triangle** with c, d ≥ 0. 04:37 "vertices" named.
  3. 05:09 revenue at vertices: 0, 75, 40. 06:09–08:15 along each edge revenue changes linearly, so the best on an edge is an end; 08:15 an interior point can always make more → never best. Conclusion: check only vertices → 25 kg cookie, $75.
  4. 09:49 add sugar (≤ 5 kg) and chocolate (≤ 1 kg) lines → more vertices; 10:19 three products → 3-D solid; 11:21 brute force over all vertices is too slow → simplex.
  5. 13:23 simplex from the origin: step along the axis with the biggest revenue per kg (cookie, $3); 14:26 vertex (0, 10), revenue 30 (chocolate used up); 15:58 move to (10, 10), revenue 50; 16:29 next vertex (7.1, 14.3) gives 49 → stop. 17:31 starting along donut instead ends at the same vertex.
  6. 19:31 3-D example (donut, cookie, brownie; 5 constraint planes, 12 vertices): (0,0,0) → (8,0,0) rev 8 → (12,3,0) rev 15 (vs (8,0,4) rev 12) → … → (9,9,4).
- **What the video adds:** a full beginner story for "the answer is at a corner" with an edge-by-edge argument (the Note states it and shows a sliding profit line); the simplex walk vertex-to-vertex; the 3-D polytope.
- **Animation ideas:** feasible polygon built one constraint line at a time (flour, sugar, chocolate), then a dot hopping vertex to vertex with revenue labels 0 → 30 → 50, the rejected neighbour 49 flashing red. Manim. Source h5o1n1QMcmM@09:49–16:29.
- **Textbook-only parts:** §2.3–2.4 LP duality and reading multipliers, §3 quadratic programming, KKT, QP dual, SVM as a QP (MML ch. 7; Boyd & Vandenberghe ch. 5, ch. 11). No priority-channel video.
- **Contradictions:** none.

### 630 Probability vs likelihood
- **Sources:**
  - `StatQuest — "In Statistics, Probability is not Likelihood." (pYxNSUDSFH4, 5:01)` → §4, §5 (00:31–04:11)
  - `CampusX — "Probability vs Likelihood | Machine Learning Interview Question" (QBFVcBXRzu4, 28:48)` → §2–3 (current base; `transcripts/M43.whisper-en.txt`)
  - File: `transcripts/maths-video/630-sq-prob-not-likelihood.txt`
- **Teaching path** (StatQuest, whole video is one picture):
  1. 00:31 normal curve of mouse weights, μ = 32 g, σ = 2.5, range 24–40 g. 01:01 **probability = area**: shaded strip 32–34 g, area 0.29. 01:34 notation P(32 < w < 34 | μ = 32, σ = 2.5) = 0.29; 02:04 change the left side (e.g. > 34 g) to ask new questions; the right side (the curve) stays fixed.
  2. 02:35 **likelihood**: the mouse is already weighed, 34 g. 03:07 likelihood = **height of the curve** at 34 → 0.12; written L(μ = 32, σ = 2.5 | w = 34). 03:39 slide the curve so μ = 34 → new height. Data fixed, curve moves.
  3. 04:11 summary: probabilities are areas under a fixed distribution; likelihoods are y-values at fixed data under a movable distribution.
- **What the video adds:** the slide-the-curve-under-a-fixed-dot motion (the Note's Figure 4 shows two static curves).
- **Animation ideas:** fixed dot at 34 g; the normal curve slides from μ = 28 to 38; a vertical bar at 34 shows the height; a second panel traces height vs μ (the likelihood function, peaking at μ = 34 with 0.160). Manim or Plotly slider. Source pYxNSUDSFH4@03:07–03:39.
- **Textbook-only parts:** §6 "a likelihood is not a probability" (integrates to 0.167, not 1) — MML §8.3.1; no video states it.
- **Contradictions:** **yes, small; the Note is right.** StatQuest @03:39 says shifting the mean to 34 gives likelihood 0.21. For N(34, 2.5²) the height at 34 is 1/(2.5√(2π)) = 0.160 (and the 0.12 at μ = 32 checks out: 0.1159). The Note §4 already says 0.16. Normal pdf formula: MML §6.5, eq. 6.62. Do not copy 0.21.

### 631 Maximum likelihood estimation
- **Sources:**
  - `StatQuest — "Maximum Likelihood, clearly explained!!!" (XepXtl9YKwc, 6:12)` → §2, §4, §5 (00:32–05:41)
  - `StatQuest — "Maximum Likelihood For the Normal Distribution, step-by-step!!!" (Dn6b9fCIUpM, 19:50)` → §3 (06:31–07:35, product of likelihoods), §6 (09:17–11:29, why log), §8 (13:03–18:50)
  - File: `transcripts/maths-video/631-sq-mle.txt` (+ `632-sq-mle-normal.txt`)
- **Teaching path:**
  1. (XepXtl9YKwc) 00:32 weighed mice on a number line; normal, exponential, gamma shapes shown; 01:02 why fit a distribution (easier, more general). 01:33 data look normal: most near the average, roughly symmetric. 02:06 pick any normal curve: centred far away → likelihood of the data low; 02:36 slide it over the data → high; keep sliding → low again. 03:08 **plot likelihood against the centre's location** → a hump; 03:39 its peak = MLE of the mean (here equal to the data mean). 04:10 then repeat for σ with μ fixed. 05:10 terminology: in stats, likelihood = "the distribution given the data".
  2. (Dn6b9fCIUpM) 01:36 one measurement x = 32, σ = 2: μ = 28 → 0.03; 02:46 μ = 30 → 0.12; 03:20 plot likelihood over μ, slope 0 at μ = 32 (04:20). 05:58 two mice (32 g, 34 g): 06:31 independent → multiply the two likelihoods. 09:17 log likelihood peaks at the same place; log turns × into +.
- **What the videos add:** the "slide the curve across the data and record the likelihood" hump; one-point example with real numbers (0.03 → 0.12) before many points.
- **Animation ideas:** data dots on an axis; a normal curve slides left→right; each dot's height drawn as a bar; their product (log-sum) traced on a second axis; the peak marked. Manim. Source XepXtl9YKwc@02:06–03:39.
- **Textbook-only parts:** §9 how good the MLE is (consistency, 1/N variance, Fisher information) — MML §8.3.2, §8.3.4. No video.
- **Contradictions:** none.

### 632 MLE for common distributions
- **Sources:**
  - `StatQuest — "Maximum Likelihood for the Binomial Distribution, Clearly Explained!!!" (4KKV9yZCoM4, 11:24)` → §2 (01:00–10:44)
  - `StatQuest — "Maximum Likelihood for the Exponential Distribution, Clearly Explained!!!" (p3T-_LMrvBc, 9:39)` → §3 (00:32–09:12)
  - `StatQuest — "Maximum Likelihood For the Normal Distribution, step-by-step!!!" (Dn6b9fCIUpM, 19:50)` → §4 (08:08–18:50)
  - Files: `transcripts/maths-video/632-*.txt`
- **Teaching path:**
  1. **Binomial** (4KKV9yZCoM4): 01:00 4 of 7 people prefer orange Fanta over grape. 01:31 probability of 4/7 given p = 0.5 → 0.273; 02:01 flip sides → likelihood of p = 0.5 given 4/7 = 0.273. 03:02 try p = 0.25 → 0.058; p = 0.57 → 0.294. 04:34 likelihood curve over p ∈ (0, 1), peak where slope = 0. 05:04 take log (same peak; × → +, powers → ×). 06:05–07:38 differentiate, set to 0 → p = 4/7. 08:09–10:12 general x, n → p̂ = x/n. 10:44 "Duh?" — but now it's proved.
  2. **Exponential** (p3T-_LMrvBc): 00:32 time between views of a video / text messages; 01:33 λ = 1 vs λ = 0.5 curves (rate). 03:03 likelihood of λ given x₁ = height of the curve at x₁; 04:05 two points → multiply; 05:06 n points → λⁿ e^{−λΣx}. 06:08 log, derivative, solve → λ̂ = n/Σx. 08:11 example x = 2, 2.5, 1.5 → λ̂ = 3/6 = 0.5.
  3. **Normal** (Dn6b9fCIUpM): 08:08 "brace yourself": product of n normal densities; 09:52–11:29 log of one density in 7 small steps; 12:31 combine n terms; 13:03–14:39 ∂/∂μ with the chain rule → Σ(xᵢ − μ)/σ²; 15:11–16:43 ∂/∂σ; 17:16–17:47 μ̂ = mean; 18:19 σ̂ = √(Σ(xᵢ − μ̂)²/n).
- **What the videos add:** the plug-and-chug likelihood table before calculus (0.058, 0.273, 0.294), a familiar story per distribution (Fanta, video views, mice), and the log algebra done one line at a time.
- **Animation ideas:** likelihood curve over p for 4/7 drawn as a dot moves along p with live value; then the log-likelihood curve overlaid with the same peak at 4/7. Plotly slider. Source 4KKV9yZCoM4@03:02–05:35.
- **Textbook-only parts:** §5 dividing by n vs n − 1 (bias of σ̂²) — MML §8.3.2 remark. StatQuest says "the standard deviation of the measurements" without stating the divisor; its formula divides by n.
- **Contradictions:** none (all StatQuest numbers checked: C(7,4)·0.5⁷ = 0.273, C(7,4)·0.25⁴·0.75³ = 0.058, C(7,4)·0.57⁴·0.43³ = 0.294; N(32; 28, 2) = 0.027 ≈ 0.03, N(32; 30, 2) = 0.121).

### 633 MLE in machine learning
- **Sources:**
  - `StatQuest — "The Main Ideas of Fitting a Line to Data (Least Squares…)" (PaFPbb66DxQ, 9:22)` → §3.3 (00:34–05:56)
  - `StatQuest — "Logistic Regression Details Pt 2: Maximum Likelihood" (BfKanl1aSG0, 10:23)` → §4 (02:05–08:54)
  - `StatQuest — "Neural Networks Part 6: Cross Entropy" (6ArSys5qHAU, 9:31)` → §5 (01:31–08:13)
  - `StatQuest — "Regularization Part 1: Ridge (L2) Regression" (Q81RR3yKn30, 20:27)` → §6, §7.2 motivation (03:05–09:51)
  - `CampusX — "Logistic Regression Part 4 | Loss Function | Maximum Likelihood | Binary Cross Entropy" (6bXOo0sxY5c, 29:03)` → §4 (Hindi; captions not downloaded — English-only rule)
  - Files: `transcripts/maths-video/633-*.txt`
- **Teaching path:**
  1. **Least squares** (PaFPbb66DxQ): 01:09 horizontal line at the mean (b = 3.5); 01:41–03:51 residuals, why square them (absolute values made the maths tricky); 04:24 rotate the line, SSR falls (14.05) then rises; 05:56 SSR vs rotation curve, minimum = least squares.
  2. **Logistic by likelihood** (BfKanl1aSG0): 02:05 obese / not-obese mice vs weight; 02:36 log-odds axis pushes points to ±∞ → residuals infinite → can't use least squares. 03:06 project points onto a candidate straight line in log-odds (e.g. 2.1, 1.4); 03:36–04:39 convert log-odds −2.1 → p = 0.1 on the S-curve. 05:11 likelihood of an obese mouse = its y on the squiggle (0.9 …); 06:47 not obese → 1 − p (1 − 0.3, 1 − 0.01). 07:52 log-likelihood −3.77; 08:23 rotate the line → −4.15 (worse); keep the best.
  3. **Cross entropy** (6ArSys5qHAU): 02:02 iris network, softmax 0.57 for the true class setosa → −ln 0.57 = 0.56; 04:36 0.58 → 0.54; 05:06 0.52 → 0.65; total 1.75. 06:08 why not squared residuals: 07:10 plot loss vs predicted probability — cross entropy explodes near 0, squared error stays ≤ 1; steeper slope → bigger backprop step for bad predictions.
  4. **Overfitting and the penalty** (Q81RR3yKn30): 03:05 two training points → least squares line passes through both (SSR 0) but misses the test points (high variance). 04:36 ridge minimises SSR + λ·slope²; 05:38 numbers: least squares 0 + 1·1.3² = 1.69 vs ridge 0.3² + 0.1² + 1·0.8² = 0.74. 08:49 λ = 0 → least squares; larger λ → slope → 0; 09:51 choose λ by cross-validation.
  - **Which to follow:** StatQuest for every section (concrete numbers); none of them says "Gaussian noise ⇒ least squares" or "Gaussian prior ⇒ ridge" — that link stays textbook (MML §8.3, §9.2).
- **What the videos add:** why logistic regression cannot use least squares (infinite residuals on the log-odds axis); the loss-vs-probability plot showing why cross entropy beats squared error for probabilities; the 1.69 vs 0.74 ridge comparison.
- **Animation ideas:** loss vs predicted probability for the true class: −ln p and (1 − p)² on one axis, with tangent lines at p = 0.05 showing the very different slopes. Plotly. Source 6ArSys5qHAU@07:10.
- **Textbook-only parts:** §3.1–3.2 Gaussian NLL → squared error, §3.4 noise variance, §7 MAP, Gaussian prior → ridge, Laplace prior → lasso (MML §8.3.1–8.3.2, §9.2.1–9.2.4, §9.5; Murphy §7.4). No priority-channel video derives these.
- **Contradictions:** none (cross-entropy numbers check: −ln 0.57 = 0.562, −ln 0.58 = 0.545, −ln 0.52 = 0.654).

### 640 Gaussian mixture models
- **Sources:** no StatQuest, Khan Academy, 3Blue1Brown or free CampusX video on GMMs (searched channel lists for "mixture", "GMM", "expectation maximization"). Stays textbook-based: MML ch. 11 (§11.1–11.2, §11.4–11.5) and §6.5.
  - Partial bridge: `StatQuest — "StatQuest: K-means clustering" (4b5d3muPQmA, 8:30)` → §9 mixtures vs k-means (00:31–06:40). File `transcripts/maths-video/640-sq-kmeans.txt`.
- **Teaching path (k-means part only):** 00:31 data on a line, need 3 clusters (e.g. tumour types); 01:01 step 1 pick K = 3; 01:32 step 2 pick 3 random points as centres; 02:03 steps 3–4 assign each point to the nearest centre; 02:33 step 5 move each centre to its cluster mean; 03:03 result can be poor → total within-cluster variation; 03:34 restart from new random centres, keep the best (04:05). 04:37–05:39 elbow plot of variation vs K. 06:40 2-D with Euclidean distance.
- **Animation ideas:** same 1-D data clustered two ways side by side: k-means hard colours vs GMM soft colours (each point a pie of responsibilities), plus the three weighted normal curves summing to the mixture density. Manim/Plotly. Source for the k-means half 4b5d3muPQmA@01:32–02:33; GMM half own (MML §11.2).
- **Contradictions:** n/a.

### 641 Expectation–maximisation
- **Sources:** none in the priority channels. Stays textbook-based: MML §7.3 (Jensen), §11.3–11.5; Hunter & Lange 2004; Nguyen 2016. Bridge: StatQuest k-means (4b5d3muPQmA) for §8 "k-means as hard EM": its steps 4–5 (02:03 assign to nearest, 02:33 recompute means) are exactly the hard E-step and M-step.
- **Animation ideas:** 2-D EM on a two-cluster dataset: ellipses (covariances) and point colours (responsibilities) update frame by frame, with the log-likelihood curve rising monotonically beside it. Manim or Plotly frames. Source own (MML §11.3 running example).
- **Contradictions:** n/a.
