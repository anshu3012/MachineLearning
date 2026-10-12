# Path-finding on a grid

Twelve search algorithms find a route across a warehouse floor drawn as a grid, all with the same start and goal, so we can watch how each one explores, cell by cell.

## The maps

![The warehouse floor: shelves and walls dark, floor white, start S, goal G, three blue charging pads](maps/warehouse_preview.png)

- **The floor:** 40 × 25 cells, each 1 m × 1 m. Dark cells are shelves and walls (blocked); white cells are floor (free).
- **Moves:** the robot moves to any of the 8 cells around it. A straight move costs 1 m, a diagonal move 1.41 m. A diagonal move must not cut the corner of a shelf.
- **The graph:** every free cell is a node (623 of them); every move between two free cells is an edge.
- **The trip:** from S (green, the loading dock, bottom left) to G (red, in the corridor behind the shelves at the top). The shelf rows are closed at the top, so the corridor can be entered only at its two ends.
- **Blue cells:** three charging pads, the goals of the multi-goal search.

The map is a picture, `maps/warehouse.png`, one pixel per cell. A second map, a maze, runs with the same code:

![The maze: 31 × 21 cells of 1 m, start top left, goal bottom right](maps/maze_preview.png)

**Reading the animations:** pale green cells are the **frontier** (reached, waiting to be expanded); pale blue cells are **visited** (taken off the frontier and expanded). The yellow line is the route. The counts are above the map.

## Breadth-first search

Breadth-first search (BFS) takes cells from a first-in, first-out queue, so the blue area grows in rings: every cell 1 move away, then 2 moves, and so on. It counts moves and ignores that a diagonal move is longer, so its route has the fewest moves (41), not necessarily the fewest metres. On this floor the fewest-move route is also a shortest one.

![Breadth-first search on the warehouse floor](images/warehouse/bfs.gif)

- Visited: 597 cells · Route: 44.7 m · 100 % of Dijkstra's

Taught in: [breadth-first search](../../RO/navigation/04-graph-search-and-configuration-space/RO-032-graphs-and-uninformed-search/RO-032-graphs-and-uninformed-search.md#5-breadth-first-search-ring-by-ring)

## Depth-first search

Depth-first search (DFS) takes the newest cell from a stack, so it runs one way until it is stuck, then backs up. The orange line is the branch it is on. It reaches the goal after fewer visits than BFS, but along a 308 m zigzag, 6.9 times the shortest route.

![Depth-first search on the warehouse floor](images/warehouse/dfs.gif)

- Visited: 299 cells · Route: 307.9 m · 688 % of Dijkstra's

Taught in: [depth-first search](../../RO/navigation/04-graph-search-and-configuration-space/RO-032-graphs-and-uninformed-search/RO-032-graphs-and-uninformed-search.md#6-depth-first-search-dive-then-back-up)

## Dijkstra

Dijkstra always expands the frontier cell with the smallest distance from the start, g. The blue area grows in bands of equal metres, the same way in every direction, also away from the goal. It stops when the goal is expanded; by then it has visited 596 of the 623 floor cells.

![Dijkstra on the warehouse floor](images/warehouse/dijkstra.gif)

- Visited: 596 cells · Route: 44.7 m (the shortest) · 100 %

Taught in: [Dijkstra's algorithm](../../RO/navigation/04-graph-search-and-configuration-space/RO-033-dijkstra-and-priority-queues/RO-033-dijkstra-and-priority-queues.md#32-the-algorithm-settle-the-nearest-update-its-neighbours)

## A*

A* expands the cell with the smallest f = g + h, where h is the straight-line distance to the goal. A cell that leads away from the goal has a large h and waits. A* visits 376 cells instead of Dijkstra's 596, and its route is still the shortest, because the straight line is never longer than a real route.

![A* on the warehouse floor](images/warehouse/a_star.gif)

- Visited: 376 cells · Route: 44.7 m · 100 % of Dijkstra's

Taught in: [A* search](../../RO/navigation/04-graph-search-and-configuration-space/RO-034-a-star-and-heuristics/RO-034-a-star-and-heuristics.md#45-the-algorithm)

## Choosing the heuristic

The guess h decides how much A* explores. Four guesses race side by side; each tick, every search expands one cell.

- **h = 0:** no guess, so A* is Dijkstra: 596 cells.
- **Straight line:** never too big: 376 cells.
- **Octile:** the length of the best 8-way route if no shelf were in the way. Never too big, and closer to the truth: 350 cells.
- **Manhattan:** metres east-west plus metres north-south. It counts a diagonal move as 2 m where it costs 1.41 m, so it can **overestimate**: at the start it guesses 50.0 m, but the shortest route is 44.7 m. It visits only 42 cells. Here its route is still the shortest, but once h can overestimate, A* no longer promises that.

![A* with four heuristics: h = 0, Manhattan, straight line, octile](images/warehouse/heuristics.gif)

- h = 0: 596 cells · Straight line: 376 · Octile: 350 · Manhattan: 42; all four routes 44.7 m

Taught in: [heuristics](../../RO/navigation/04-graph-search-and-configuration-space/RO-034-a-star-and-heuristics/RO-034-a-star-and-heuristics.md#53-a-closer-guess-takes-fewer-cells)

## Greedy best-first search

Greedy best-first search expands the cell with the smallest h only, and ignores the metres already driven. It heads for the goal, runs up the shelf rows that are closed at the top, one after another, and finally goes round the right end. It visits few cells, but its route is a quarter longer than the shortest.

![Greedy best-first search on the warehouse floor](images/warehouse/greedy.gif)

- Visited: 134 cells · Route: 56.1 m · 126 % of Dijkstra's

Taught in: [best-first search](../../RO/navigation/04-graph-search-and-configuration-space/RO-034-a-star-and-heuristics/RO-034-a-star-and-heuristics.md#3-following-the-guess-alone-greedy-best-first-search)

## Iterative deepening A* (IDA*)

IDA* is depth-first search with a bound on f = g + h: a branch is cut as soon as its f goes over the bound. If the goal is not reached, the bound rises to the smallest f that went over it, and the search starts again. It stores only the branch it is on (orange), but it visits the same cells again in every round.

On the whole trip, IDA* had not finished after 1,000,000 visits (193 rounds), and not on the trip to a point halfway along the route either. So the animation shows a nearer goal, 14.3 m from the start.

![IDA* on the warehouse floor, to a goal 14.3 m away](images/warehouse/ida_star.gif)

- Visits: 1,560 in 31 rounds (A* to the same goal: 29) · Route: 14.3 m, the shortest to that goal

Taught in: [iterative deepening](../../RO/navigation/04-graph-search-and-configuration-space/RO-034-a-star-and-heuristics/RO-034-a-star-and-heuristics.md#7-saving-memory-iterative-deepening-and-ida)

## Bidirectional search

Two Dijkstra searches run at once, one from the start (blue) and one from the goal (purple); each step expands whichever side's next cell is nearer its own end. The route is complete where they meet. Together they visit 354 cells, against 596 for one Dijkstra.

![Bidirectional search on the warehouse floor](images/warehouse/bidirectional.gif)

- Visited: 354 cells · Route: 44.7 m · 100 % of Dijkstra's

Taught in: [bidirectional search](../../RO/navigation/04-graph-search-and-configuration-space/RO-034-a-star-and-heuristics/RO-034-a-star-and-heuristics.md#82-bidirectional-search)

## Weighted A*

Weighted A* uses f = g + ε h with ε = 2: it trusts the guess twice as much. It visits 206 cells, about half of A*'s, and its route is 56.1 m. The promise is a route at most ε times the shortest (89.5 m).

![Weighted A* with ε = 2 on the warehouse floor](images/warehouse/weighted_a_star.gif)

- Visited: 206 cells · Route: 56.1 m · 126 % of Dijkstra's

Taught in: [weighted A*](../../RO/navigation/04-graph-search-and-configuration-space/RO-034-a-star-and-heuristics/RO-034-a-star-and-heuristics.md#101-weighted-a)

## Anytime A*

Weighted A* runs three times, with ε = 2.5, then 1.5, then 1. Each round starts afresh and gives a better route; the dotted lines are the earlier routes. The first route arrives after 169 visits; the shortest after 948 visits in all.

![Anytime A* on the warehouse floor](images/warehouse/anytime_a_star.gif)

- Rounds: ε = 2.5: 56.1 m after 169 visits · ε = 1.5: 46.5 m after 403 · ε = 1: 44.7 m after 376
- Route: 44.7 m · 100 % of Dijkstra's

Taught in: [anytime A*](../../RO/navigation/04-graph-search-and-configuration-space/RO-034-a-star-and-heuristics/RO-034-a-star-and-heuristics.md#102-anytime-a-and-ara)

## Theta*

Theta* is A* whose route may run at any angle. When it reaches a cell, it checks whether the cell can be seen in a straight line from the parent of the cell it came from; if so, it links to that parent and cuts the corner. The route is 4 straight pieces, shorter than the 8-way route, which can only run along the 8 grid directions.

![Theta* on the warehouse floor](images/warehouse/theta_star.gif)

- Visited: 381 cells · Route: 43.6 m · 98 % of Dijkstra's (Dijkstra may only make 8-way moves)

Taught in: [any-angle search (Theta*)](../../RO/navigation/04-graph-search-and-configuration-space/RO-034-a-star-and-heuristics/RO-034-a-star-and-heuristics.md#12-routes-at-any-angle-theta)

## Multi-goal A*

Which of the three charging pads (blue) is nearest by route? One A* run answers it: we add a virtual goal joined to each pad by a 0 m move, and h is the straight line to the nearest pad.

- **The pad in the office** (top left) is the nearest in a straight line, 21.0 m. The office has one door, in its right wall, so the route to it is 32.0 m.
- **The pad in the middle aisle** is 21.1 m away in a straight line and 24.3 m by route: the nearest by route.
- **The pad in the bottom-right corner** is 35.0 m away in a straight line and 35.4 m by route.

![Multi-goal A* to the nearest of three charging pads](images/warehouse/multi_goal.gif)

- Visited: 148 cells · Route: 24.3 m to the pad in the middle aisle

**Separate runs or one run:** the plain way is one A* run per pad, keeping the shortest route. The two ways race below; each tick, each expands one cell. One A* per pad visits 169 + 107 + 36 = 312 cells; the one multi-goal run visits 148, less than half, and finds the same 24.3 m route.

![One A* run per pad against one multi-goal A* run](images/warehouse/multi_goal_race.gif)

- One A* per pad: 312 cells visited · Multi-goal A*: 148 · Both: 24.3 m to the pad in the middle aisle

Taught in: [multi-goal A*](../../RO/navigation/04-graph-search-and-configuration-space/RO-034-a-star-and-heuristics/RO-034-a-star-and-heuristics.md#91-the-virtual-goal)

## Jump point search

Jump point search (JPS) is A* that skips cells. From a cell it scans straight or diagonally across open floor (pale yellow) and stops only at the goal or beside a shelf corner, where a shortest route might turn. Only these jump points go on the frontier. It visits 67 cells against A*'s 376, with the same route; its scans step over cells 1,696 times.

![Jump point search on the warehouse floor](images/warehouse/jps.gif)

- Visited: 67 jump points · Route: 44.7 m · 100 % of Dijkstra's

Taught in: [jump point search](../../RO/navigation/04-graph-search-and-configuration-space/RO-034-a-star-and-heuristics/RO-034-a-star-and-heuristics.md#11-skipping-equal-routes-jump-point-search)

## The race

Six searches on one clock: each tick, every search expands one cell. Each map shows its cells visited and, once done, its route length.

![Race on the warehouse floor: BFS, DFS, Dijkstra, greedy, A*, bidirectional](images/warehouse/race.gif)

The same race on the maze, run by changing one argument (`--map maze`):

![Race on the maze](images/maze/race.gif)

The same functions also run on the streets of Chicago: [Path-finding on real streets](../real-map-pathfinding/real-map-pathfinding.md).

## Run it yourself

In the `campusx` environment, from `projects/grid-pathfinding/`:

```bash
python check_algorithms.py                  # every search against networkx, on every map in maps/
python run.py                               # the warehouse: numbers, preview, all animations
python run.py --map maze                    # another map in maps/
python run.py --map path/to/my_floor.png    # a map you drew
python run.py --only a_star race            # only some animations
jupyter nbconvert --to notebook --execute grid-pathfinding.ipynb
```

**A new map** is a PNG drawn in any paint program with these colours:

- black: blocked (shelf, wall);
- white: free floor;
- pure green (0, 255, 0): the start, one pixel;
- pure red (255, 0, 0): the goal, one pixel;
- pure blue (0, 0, 255), optional: goals for the multi-goal search.

One pixel is one cell. A JSON file with the same name gives the cell size: `{"label": "My floor", "cell_m": 1.0, "pixels_per_cell": 1}` (set `pixels_per_cell` if each cell is drawn as a block of pixels).

**Files:** `algorithms.py` (every search), `map_interface.py` (what a map gives the searches), `grid.py` (PNG maps), `render.py` (the drawings), `run.py`, `check_algorithms.py`, `gifkit.py` (frames to GIF).

## Sources

Built from:

- The video [A* (A-Star) Pathfinding Algorithm Visualization on a Real Map](https://www.youtube.com/watch?v=CgW0HPHqFE8) by ones and zeros, as the inspiration.
- S. M. LaValle, *Planning Algorithms*, Cambridge University Press, 2006, chapter 2 (BFS, DFS, Dijkstra, A*, best-first, iterative deepening, bidirectional search).
- R. E. Korf, "Depth-first iterative-deepening: an optimal admissible tree search", *Artificial Intelligence* 27, 1985 (IDA*).
- I. Pohl, "Heuristic search viewed as path finding in a graph", *Artificial Intelligence* 1, 1970 (weighted A*); M. Likhachev, G. Gordon, S. Thrun, "ARA*: Anytime A* with provable bounds on sub-optimality", NIPS 2003 (anytime A*).
- D. Harabor, A. Grastien, "Online graph pruning for pathfinding on grid maps", AAAI 2011 (jump point search); the no-corner-cutting jump rules follow [PathFinding.js](https://github.com/qiao/PathFinding.js) by Xueqiao Xu, whose look the animations borrow.
- A. Nash, K. Daniel, S. Koenig, A. Felner, "Theta*: any-angle path planning on grids", AAAI 2007.
