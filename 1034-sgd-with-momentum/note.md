---
title: "SGD with Momentum"
tags: [subject/deep-learning, area/dl-optimizers, step/model, concept/momentum, concept/saddle-point]
---

## 1. Overview

> **Key point:** Momentum keeps an exponentially weighted average of past gradients, the velocity $v$, and moves by it: $v_t = \beta v_{t-1} + \eta\thinspace \nabla L(w_t)$, then $w_{t+1} = w_t - v_t$. When many gradients agree, the steps grow and training speeds up; the price is overshooting the minimum.

**Momentum** (Polyak 1964) is the first improved optimizer. Plain gradient descent forgets every gradient as soon as it has used it. Momentum remembers them: if the last few gradients all point the same way, it becomes confident and moves faster in that direction, like a ball gathering speed as it rolls downhill.

![Plain gradient descent and momentum along a narrow valley, same learning rate 0.01. Gradient descent zigzags across and crawls along; momentum builds speed along the valley](images/momentum_valley.gif){width=95%}

Figure 1 shows the main benefit. On a narrow valley, gradient descent needs 424 steps to get close to the minimum; momentum needs 59. The idea of momentum returns in NAG and Adam, which makes it one of the most important optimizers to understand.

## 2. Prerequisites

- The [optimizers Note](../1032-optimizers-in-deep-learning/note.md): the weak spots of plain gradient descent.
- The [EWMA Note](../1033-exponentially-weighted-moving-average/note.md): $V_t = \beta V_{t-1} + (1-\beta)\theta_t$ and the role of $\beta$.
- The [gradient descent Note](../57-gradient-descent/note.md): the contour plot of a loss surface.

## 3. Three ways to draw a loss

> **Key point:** One parameter: a curve. Two parameters: a surface in 3D. The same surface seen from above: a contour plot, where colour or rings show the height.

The loss is a function of the weights and biases, so we can draw it against them, just as we draw $y = f(x)$. We can only see up to 3 dimensions, so the pictures in this Note use one or two parameters:

- **One parameter, a 2D graph.** A single node with one weight $w$ and no bias: the loss is a curve over $w$.
- **Two parameters, a 3D graph.** Add a bias $b$: the loss is a surface over the $(w, b)$ plane, with the loss as height.
- **A contour plot.** The same surface seen from above (see section 6 of the [gradient descent Note](../57-gradient-descent/note.md)). Each ring joins points of equal loss, and colour or shading shows the height that the top view loses.

Reading a contour plot takes practice. Where the surface is flat, the height changes slowly, so the rings lie far apart. Where it is steep, they crowd together.

## 4. Why plain gradient descent struggles

> **Key point:** Deep learning losses are non-convex. Local minima, saddle points with their flat surroundings, and high curvature all slow plain gradient descent down or trap it.

The losses of neural networks are non-convex (see the [convex and non-convex cost functions Note](../590-convex-and-non-convex-cost-functions/note.md)), which makes the minimum hard to reach for three reasons:

1. **Local minima:** a dip where the slope is zero. Starting from an unlucky point, gradient descent stops there and returns a sub-optimal solution.
2. **Saddle points:** the surface rises in one direction and falls in another, and the slope changes very slowly over a wide flat region. Updates are proportional to the slope, so they become tiny there and training slows down.
3. **High curvature:** a bend with a small radius, such as the steep sides of a narrow valley. Gradient descent zigzags across the bend instead of following it.

Batch, stochastic and mini-batch gradient descent handle these poorly (see section 8 of the [gradient descent in neural networks Note](../1020-gradient-descent-in-neural-networks/note.md) for their paths). Momentum was designed for exactly these situations: high curvature, small but consistent gradients, and noisy gradients (Goodfellow et al. 2016, §8.3.2).

## 5. The idea: confidence builds speed

> **Key point:** If the past gradients keep pointing the same way, move faster that way. Like a ball rolling downhill, the parameters gather speed.

**An everyday picture.** We drive from A to B and do not know the way, so we ask people. If four people in four places all point in the same direction, we become confident and drive faster that way. If two point forward and two point back, we still go forward, but slowly.

**A physics picture.** A ball rolling down a hill gathers speed as it goes. Momentum in physics is mass times velocity; with a unit mass, momentum is simply the velocity (Goodfellow et al. 2016, §8.3.2). The optimizer keeps a **velocity** $v$: the direction and speed with which the parameters move, built from the history of past updates.

The single most important benefit of momentum is speed: it usually reaches a good solution faster than plain gradient descent.

## 6. The update rule

> **Key point:** The velocity is an EWMA of past gradients: $v_t = \beta v_{t-1} + \eta\thinspace \nabla L(w_t)$. The weight moves by the velocity: $w_{t+1} = w_t - v_t$.

Plain gradient descent moves by the current gradient only: $w_{t+1} = w_t - \eta\thinspace \nabla L(w_t)$. Momentum replaces that step by the velocity.

1. **In words:** the new velocity is a fraction $\beta$ of the old velocity plus the current gradient step. The weight then moves by the whole velocity.
2. **Formula:**
   $$v_t = \beta\thinspace v_{t-1} + \eta\thinspace \nabla L(w_t), \qquad w_{t+1} = w_t - v_t$$
   with $v_0 = 0$ and $\beta$ between 0 and 1, usually 0.9.
3. **Example:** the loss $L(w) = w^2/2$, whose gradient is $w$, starting at $w_0 = -10$, with $\eta = 0.1$ and $\beta = 0.9$:
   $$v_1 = 0.9 \times 0 + 0.1 \times (-10) = -1, \qquad w_1 = -10 - (-1) = -9$$
   $$v_2 = 0.9 \times (-1) + 0.1 \times (-9) = -1.8, \qquad w_2 = -9 - (-1.8) = -7.2$$
   Plain gradient descent would be at $w_2 = -9 - 0.1 \times (-9) = -8.1$. Momentum's second step is almost twice as long, because the first step's push is still there (Notebook).

The term $\beta v_{t-1}$ is the momentum. To compute $v_{t-1}$ we needed $v_{t-2}$, which needed $v_{t-3}$, and so on: the velocity carries the whole history of past gradients. Momentum accumulates an exponentially decaying moving average of past gradients and continues to move in their direction (Goodfellow et al. 2016, §8.3.2).

> **Extra:** If every gradient is the same, $g$, the velocity grows until it settles at a **terminal velocity** of $\eta g/(1-\beta)$ (Goodfellow et al. 2016, eq. 8.17). With $\beta = 0.9$, momentum's steps become $1/(1 - 0.9) = 10$ times longer than plain gradient descent's; the Notebook's steps grow from 0.1 to 1.0. This is the $1/(1-\beta)$ of the [EWMA Note](../1033-exponentially-weighted-moving-average/note.md) again. Our velocity adds $\eta\thinspace \nabla L$ rather than the EWMA's $(1-\beta)\thinspace \nabla L$; that only rescales the learning rate.

Each step now has two parts: the push of the past velocity, and the current gradient. When both point the same way, the step is long.

### 6.1 Why the zigzag fades and speed builds

> **Key point:** Across a narrow valley the gradients flip sign at every step, so they cancel in the velocity. Along the valley they agree, so they add up.

In a narrow valley (Figure 1), plain gradient descent spends its steps bouncing between the steep walls, because each step follows the current slope, which points mostly across the valley. With momentum:

- **Across the valley,** the gradient changes sign at every step. In the velocity, those up-and-down components largely cancel, so the zigzag shrinks.
- **Along the valley,** every gradient points the same way. Those components add up, so the velocity grows and the steps lengthen.

Momentum increases the step for directions whose gradients point the same way and reduces it for directions whose gradients change sign (Ruder 2016, §4.1). On the valley $L = (w_1^2 + 100w_2^2)/2$ from $(-10, 0.4)$, with $\eta = 0.01$ for both, after 20 steps gradient descent has moved $w_1$ from $-10$ to $-8.18$, while momentum is already at $-1.18$, close to the minimum at 0 (Notebook). To bring the loss below 0.01:

| Optimizer | Steps |
|---|---|
| Gradient descent, $\eta = 0.01$ | 424 |
| Gradient descent, $\eta = 0.019$ (its largest safe value) | 223 |
| Momentum, $\eta = 0.01$, $\beta = 0.9$ | 59 |

## 7. The role of $\beta$

> **Key point:** $\beta = 0$ is plain gradient descent. $\beta$ close to 1 remembers the past for long: more speed, more overshooting. $\beta = 1$ never forgets and never settles. Usual values: 0.5, 0.9, 0.99.

$\beta$ is the **decay factor**: it decides how fast the influence of past velocities dies away. An old gradient's contribution is multiplied by $\beta$ at every step, so recent gradients count most, exactly as in an EWMA. With $\beta = 0.9$ the velocity behaves roughly like an average of the last $1/(1-0.9) = 10$ gradients.

- **$\beta = 0$:** the momentum term disappears, $v_t = \eta\thinspace \nabla L(w_t)$, and the update is plain gradient descent.
- **$\beta = 1$:** nothing decays. Like a ball on a frictionless surface, the parameters keep swinging back and forth forever without settling.
- **In practice:** 0.5, 0.9 or 0.99 (Goodfellow et al. 2016, §8.3.2).

![The weight over 100 steps on $L = w^2/2$ from $w = -10$, $\eta = 0.1$. $\beta = 0$ creeps in; $\beta = 0.5$ arrives quickly; $\beta = 0.9$ overshoots and swings before settling; $\beta = 1$ swings between $-10$ and 10 forever](images/beta_effect.png){width=95%}

Figure 2 shows all four. With $\beta = 1$, the weight is still swinging between about $-10$ and 10 after 100 steps (Notebook).

> **Extra:** Goodfellow et al. (2016, §8.3.2) explain the decay as friction. The velocity's decay acts like viscous drag, a force proportional to $-v$, as if the particle moved through syrup. Without it ($\beta = 1$) the particle would slide down one side of the valley and up the other forever, like a hockey puck on frictionless ice.

## 8. Escaping a local minimum, and the cost: overshooting

> **Key point:** The speed that carries momentum through a small dip also carries it past the true minimum. Momentum swings back and forth before settling, and those swings waste time.

![Two balls roll down a curve with a small dip (local minimum) and a deeper one (global minimum), $\eta = 0.05$. Plain gradient descent (blue) stops in the small dip. Momentum (orange, $\beta = 0.9$) rolls over the bump, overshoots the global minimum and swings before settling](images/momentum_ball.gif){width=95%}

Figure 3 shows two effects on the curve $L(w) = (w^2 - 4)^2/8 - 0.6w$, starting at $w = -3$:

1. **Faster.** The orange ball gains speed as it rolls; the blue ball moves at the pace of the slope.
2. **Out of a local minimum.** The blue ball stops in the small dip near $w = -1.83$ (loss 1.15). The orange ball has enough speed to climb out, crosses the bump, and ends in the global minimum near $w = 2.14$ (loss $-1.24$) (Notebook).

The same speed has a price. The orange ball does not stop at the global minimum: it shoots past to $w = 2.85$, comes back, and swings with shrinking amplitude before settling. In Figure 2, $\beta = 0.9$ crosses the minimum again and again for the same reason. As the decay factor makes the old velocities fade, the swings die out, but the time spent swinging is wasted.

Momentum is still faster than plain gradient descent, but these oscillations make it slower than optimizers that damp them. The biggest problem of momentum is its momentum. The next optimizer, Nesterov accelerated gradient, reduces the swings.

> **Extra:** Escaping a dip is not guaranteed. On this curve it depends on the settings: with $\beta = 0.5$, momentum also stops in the small dip (Notebook). A ball escapes only if it has gathered enough speed before reaching the bump.

## 9. Momentum on real data: MNIST

> **Key point:** On handwritten digits, adding momentum 0.9 to SGD with the same learning rate reached plain SGD's 20-epoch loss by epoch 4.

The data is the MNIST handwritten digits (see the [MNIST Note](../1012-mnist-ann/note.md)): 10,000 training images, each with 784 pixel **features** (input variables) and the digit as **target** (the output we predict), and the 10,000 test images for validation. The network has hidden layers of 128 and 64 ReLU nodes and a softmax output. Both runs use mini-batch SGD with learning rate 0.01, batch size 64 and 20 epochs; only the momentum changes, 0 or 0.9. Each is trained with 3 seeds and the curves are averaged.

![Training loss on MNIST per epoch, mean of 3 seeds. Same learning rate 0.01; momentum 0.9 (orange) against plain SGD (blue)](images/mnist_momentum.png){width=90%}

Figure 4 and the Notebook give:

| | Plain SGD | SGD with momentum 0.9 |
|---|---|---|
| Training loss, epoch 1 | 1.94 | 0.85 |
| Training loss, epoch 5 | 0.48 | 0.18 |
| Training loss, epoch 20 | 0.24 | 0.021 |
| Validation accuracy, epoch 20 | 0.917 | 0.950 |

Momentum gets to plain SGD's final loss of 0.24 by epoch 4. Its terminal steps are up to $1/(1-0.9) = 10$ times longer when the gradients agree (section 6), so it covers the same ground in far fewer epochs.

### 9.1 Momentum in Keras

> **Key point:** Pass `momentum` to Keras' `SGD`: 0 is plain SGD, 0.9 is SGD with momentum.

> **Python:** SGD with momentum in Keras.
>
> ```python
> import keras
> opt = keras.optimizers.SGD(learning_rate=0.01, momentum=0.9)
> model.compile(optimizer=opt, loss="sparse_categorical_crossentropy",
>               metrics=["accuracy"])
> ```

`momentum` is $\beta$, and its default is 0. With `momentum=0.9` and `nesterov=False` (the default) Keras uses the update of section 6.

> **Extra:** Keras writes the same update with the sign of $v$ flipped: $v \leftarrow \beta v - \eta g$, then $w \leftarrow w + v$ (Keras `SGD` documentation). Both give the same weights. Some books, such as Goodfellow et al. (2016, §8.3.2), use this form too.

## 10. Summary

| | Plain gradient descent | SGD with momentum |
|---|---|---|
| Step | $\eta\thinspace \nabla L(w_t)$ | $v_t = \beta v_{t-1} + \eta\thinspace \nabla L(w_t)$ |
| Memory of past gradients | none | EWMA, about $1/(1-\beta)$ steps |
| Narrow valley (our example) | 424 steps | 59 steps |
| Small local dip | stops in it | can roll through |
| Near the minimum | arrives directly | overshoots and swings |

- Momentum adds a velocity, an exponentially decaying average of past gradients, to gradient descent.
- Gradients that agree add up (speed); gradients that flip sign cancel (less zigzag).
- $\beta = 0$ is plain gradient descent; $\beta = 1$ never settles; 0.9 is the usual value.
- The speed can carry it out of a small local minimum, and also past the global minimum: overshooting is its main weakness.
- In Keras: `SGD(learning_rate=..., momentum=0.9)`.

## 11. Sources

- Goodfellow, I., Bengio, Y. and Courville, A. (2016). *Deep Learning*. MIT Press. §8.3.2 Momentum (algorithm 8.2, eq. 8.17, the physical analogy).
- Polyak, B. T. (1964). Some methods of speeding up the convergence of iteration methods. *USSR Computational Mathematics and Mathematical Physics* 4(5), 1–17.
- Ruder, S. (2016). An overview of gradient descent optimization algorithms. arXiv:1609.04747. §4.1 Momentum.
- Keras API documentation: `SGD` optimizer, keras.io/api/optimizers/sgd.

## 12. Key terms

| Term | Meaning |
|---|---|
| Momentum (optimizer) | Gradient descent that moves by a velocity, an exponentially decaying average of past gradients |
| Velocity $v$ | The direction and size of the current move, built from past gradients: $v_t = \beta v_{t-1} + \eta\thinspace \nabla L(w_t)$ |
| Decay factor $\beta$ | How much of the old velocity is kept each step; 0 gives plain gradient descent, usually 0.9 |
| Terminal velocity | The step size momentum reaches when every gradient is the same: $\eta g/(1-\beta)$ |
| Overshooting | Moving past the minimum because of the built-up velocity, then swinging back |
| Contour plot | A loss surface seen from above, with rings joining points of equal loss |
| Feature | An input variable, such as one pixel of an image |
| Target | The output we predict, such as the digit |
