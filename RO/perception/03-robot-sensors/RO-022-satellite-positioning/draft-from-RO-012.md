# Moved from RO-012 on 2026-10-10: where two range circles cross

From RO-012 Section 5.2 (Two and three landmarks: rings meet). Setting: the pink pole at (4.4, 3.8) read at range 3.10 m and the green pole at (0.4, 3.2) read at range 1.95 m; the robot is truly at (2, 2). No figures. Notebook cell: notebook-cells-from-RO-012.json. No glossary rows moved (trilateration, G-2406, stays in RO-012).

With the first pole at the origin and the second at distance $a$ along the x-axis, the crossing points of circles of radius $d_1$ and $d_2$ are (Freiburg sensor-model slides, "Distances only"):

$$x = \frac{a^2 + d_1^2 - d_2^2}{2a}$$

$$y = \pm\sqrt{d_1^2 - x^2}$$

The formula comes from the two circle equations:

$$x^2 + y^2 = d_1^2$$

$$(x - a)^2 + y^2 = d_2^2$$

Subtract the second equation from the first. The $y^2$ terms cancel:

$$x^2 - (x - a)^2 = d_1^2 - d_2^2$$

Multiply out the bracket:

$$2ax - a^2 = d_1^2 - d_2^2$$

Solve for $x$:

$$x = \frac{a^2 + d_1^2 - d_2^2}{2a}$$

Putting that $x$ back into the first circle gives $y$. For pink and green, 4.04 m apart:

$$x = \frac{16.36 + 9.61 - 3.80}{8.09} = 2.74$$

$$y = \pm\sqrt{9.61 - 7.51} = \pm 1.45$$

Turned back into room coordinates, the two crossing points are (1.91, 1.96), close to the true (2, 2), and (1.48, 4.83), which lies outside the room. The map rules the second one out.
