# Draft for the wheel types and unicycle Note (moved from RO-001, 2026-10-10)

RO-001 keeps only what it needs; this text, the kinematic model as one matrix, was cut from it and belongs in this Note. Figure and section numbers are RO-001's and must be renumbered when this Note is built. Figures: none.

## Glossary rows to restore (IDs kept)

(none)

The three lines can be written as one matrix times the input vector:

$$\dot{q} = G(q)\thinspace u$$

$$\dot{q} = \begin{bmatrix} \dot{x} \cr\dot{y} \cr\dot{\theta} \end{bmatrix}$$

$$G(q) = \begin{bmatrix} \cos\theta & 0 \cr\sin\theta & 0 \cr0 & 1 \end{bmatrix}$$

$$u = \begin{bmatrix} v \cr\omega \end{bmatrix}$$

The matrix form shows something the three lines hide. Each column of $G(q)$ is one direction the robot can move in: the first column is "drive forward", the second is "turn on the spot" (MR §13.3.1). Every motion is a mix of these two. A third direction, sliding sideways, is missing, and Section 6 is about that gap.

At our pose, with the input $u = (0.5, 1)$, the matrix product gives back the speeds of Section 5.1:

$$\dot{x} = 0.866 \times 0.5 + 0 \times 1 = 0.433$$

$$\dot{y} = 0.5 \times 0.5 + 0 \times 1 = 0.25$$

$$\dot{\theta} = 0 \times 0.5 + 1 \times 1 = 1$$

The same three equations describe a single rolling wheel, the unicycle (MR §13.3.1); a later Note in this chapter compares wheel types.
