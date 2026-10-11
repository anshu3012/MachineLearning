# Moved from RO-017 on 2026-10-10: the rank test for observability

From RO-017 §6.5 (Observability), after the definition of observable (G-2517). It uses the constant-velocity model of RO-017 §6.2: $F = [[1, 1], [0, 1]]$, position sensor $H = [1, 0]$. Notebook lines: notebook-cells-from-RO-017.json.

The test: stack the measurement matrix and what it sees one step later,

$$\mathcal{O} = \begin{bmatrix} H \cr HF \end{bmatrix}$$

and check that its [rank](../../../../MA/05-linear-algebra/MA-052-linear-combinations-span-and-basis/MA-052-linear-combinations-span-and-basis.md#7-linear-dependence-and-independence) (G-1627) equals the number of state variables, here 2 (FBS Theorem 8.1). For the position sensor:

$$H = \begin{bmatrix} 1 & 0 \end{bmatrix}$$

$$HF = \begin{bmatrix} 1 & 1 \end{bmatrix}$$

The two rows point in different directions: rank 2, observable. Two position readings one second apart give the position and, from their difference, the speed. For a speed sensor:

$$H = \begin{bmatrix} 0 & 1 \end{bmatrix}$$

$$HF = \begin{bmatrix} 0 & 1 \end{bmatrix}$$

The rows are the same: rank 1, not observable. 

## Glossary rows to restore

| <span id="G-1627">G-1627</span> | Rank (of a matrix) | The number of linearly independent columns of a matrix, that is, how many directions its columns really span; a column that is a combination of others does not add to it. | [Note MA-058](MA/05-linear-algebra/MA-058-computing-the-svd/MA-058-computing-the-svd.md#5-a-matrix-of-rank-1) | Linear combinations, span and basis |
