# Moved from RO-015 on 2026-10-10: the inverse measurement model

From RO-015 (Grid Filters) §4.5, with its Extra box (a 0.2 prior). The sentence naming the binary Bayes filter stayed in RO-015, now at the end of §4.3 (RO-015-grid-filters.md#43-log-odds-turn-the-products-into-sums). Notebook cells: notebook-cells-from-RO-015.json. Glossary row to restore:

| <span id="G-2468">G-2468</span> | Inverse measurement model | The probability of the state given one reading on its own, $p(x \mid z)$, such as 0.75 for "door open" after one "sense open"; used when the state is a simple yes or no but the reading is complex, such as a camera image. | [Note RO-015](RO/localization/02-bayes-filters/RO-015-grid-filters/RO-015-grid-filters.md#45-the-inverse-measurement-model) | Binary Bayes filter |

### 4.5 The inverse measurement model

So far the robot used $p(z \mid x)$: how likely the reading is for each state. In the binary Bayes filter it is usual to use the other direction, $p(x \mid z)$: how likely the state is, given one reading on its own. This is the **inverse measurement model** (G-2468) (PR §4.2). For the door, with an even prior:

$$p(\text{open} \mid \text{sense open}) = 0.75$$

$$p(\text{open} \mid \text{sense closed}) = 0.33$$

Why turn the model round? Because the state is a single yes or no, while the reading can be large, such as a whole camera image. Writing down how likely every possible image is for an open door is very hard; learning to say "open" or "closed" from one image is much easier (PR §4.2).

The update in log odds is then (PR §4.2; UW CSE 571):

$$l_t = l_{t-1} + \ln \frac{p(x \mid z_t)}{1 - p(x \mid z_t)} - l_0$$

where $l_0$ is the log odds of the prior, before any reading:

$$l_0 = \ln \frac{p(x)}{1 - p(x)}$$

Why subtract $l_0$? The inverse model already includes the prior once, because it answers "how likely is open after this one reading, starting from the prior". Section 4.2 gives the same fact as a formula. Applied to one reading on its own, starting from the prior, it says:

$$\text{odds of } p(x \mid z)$$

$$= \text{Bayes factor} \times \text{prior odds}$$

Take the log of both sides:

$$\ln \frac{p(x \mid z)}{1 - p(x \mid z)}$$

$$= \ln(\text{Bayes factor}) + l_0$$

So the log of the Bayes factor, the amount each reading should add, is:

$$\ln(\text{Bayes factor}) = \ln \frac{p(x \mid z)}{1 - p(x \mid z)} - l_0$$

Put this into "new log odds = old log odds + log of the Bayes factor" and we get the update above. Without the $-l_0$, the prior would be counted again at every reading. With an even prior, $l_0 = 0$, and each "sense open" adds:

$$\ln \frac{0.75}{0.25} = \ln 3 = 1.10$$

the same step as in Section 4.3.

> **Extra:** With an uneven prior the subtraction matters. Suppose doors in this building are usually closed, with a prior of 0.2 for open. The inverse model for "sense open" is then:
>
> $$\frac{0.6 \times 0.2}{0.6 \times 0.2 + 0.2 \times 0.8} = 0.43$$
>
> With the $-l_0$ term the filter gives 0.43 after one reading, which matches Bayes' theorem. Without it the filter gives 0.16, because it counted the prior of 0.2 twice.
