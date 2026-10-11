"""Figure 3 as an animation: the set of cells the robot could be in, step by step.
Part 1, a sensor that is never wrong: before any reading, all 10 cells; the reading 'door' keeps {1, 3, 7}; the move
'2 cells' (really 1, 2 or 3) fans each door cell out, one at a time, to {2,3,4} u {4,5,6} u {8,9,0}
= {0, 2, 3, 4, 5, 6, 8, 9}; the second 'door' keeps only cell 3. Part 2, the real sensor, which
reads 'door' at a wall 20 percent of the time: 'door' can be read in all 10 cells, so the second reading removes
nothing; the next move fills all 10 cells, and no reading can empty them: the set never shrinks.
Run: python sets_anim.py -> sets_anim.gif, sets_anim_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE, make_gif
from hallplot import BROWN, DOORS, KERNEL, N

here = Path(__file__).parent
ROWS = (4.4, 2.2, 0.0)                     # y of the three hallway rows: before, after the move, after the reading
FANS = {1: PURPLE, 3: GREEN, 7: ORANGE}
ALL = set(range(N))


def reach(cells):
    """Every cell the move '2' can take each cell to (1, 2 or 3 cells right, round the loop)."""
    return {(c + k) % N for c in cells for k in KERNEL}


S1 = set(DOORS)
S2 = reach(S1)
S3 = S2 & set(DOORS)
assert sorted(S2) == [0, 2, 3, 4, 5, 6, 8, 9] and S3 == {3}
assert [sorted((c + k) % N for k in KERNEL) for c in DOORS] == [[2, 3, 4], [4, 5, 6], [0, 8, 9]]
assert S2 & ALL == S2 and reach(S2) == ALL          # noisy sensor: nothing removed; the next move fills the hallway


def frame(title, rows, fans=(), wrap=False):
    """rows: per hallway row, (cells in the set, cells crossed out, label lines, fill colour or None)."""
    fig = go.Figure()
    for y, (cells, crossed, lines, fill) in zip(ROWS, rows):
        if lines is None:
            continue
        for i in range(N):
            fig.add_shape(type="rect", x0=i, x1=i + 1, y0=y, y1=y + 0.8, line=dict(color=GREY, width=2),
                          fillcolor="rgba(0,0,0,0)")
            if i in cells or i in crossed:
                fig.add_shape(type="rect", x0=i + 0.08, x1=i + 0.92, y0=y + 0.08, y1=y + 0.72, line=dict(width=0),
                              fillcolor=fill or BLUE, opacity=0.15 if i in crossed else 0.55)
            if i in crossed:
                fig.add_annotation(x=i + 0.5, y=y + 0.4, text="×", showarrow=False, font=dict(size=30, color=GREY))
        for d in DOORS:
            fig.add_shape(type="rect", x0=d + 0.15, x1=d + 0.85, y0=y + 0.8, y1=y + 0.95, line=dict(width=0),
                          fillcolor=BROWN, opacity=0.7)
        fig.add_annotation(x=10.4, y=y + 0.4, xanchor="left", showarrow=False, align="left", text="<br>".join(lines),
                           font=dict(size=20))
    for s in fans:                                                  # arrows from a door cell to the cells it reaches
        for k in KERNEL:
            t = s + k
            if t < N:
                fig.add_annotation(x=t + 0.5, y=ROWS[1] + 0.85, ax=s + 0.5, ay=ROWS[0], xref="x", yref="y", axref="x",
                                   ayref="y", text="", showarrow=True, arrowhead=2, arrowwidth=2.5, arrowcolor=FANS[s])
    if wrap:                                                        # 7 + 3 = cell 0: the hallway is a loop
        fig.add_annotation(x=10.25, y=3.6, ax=7.5, ay=ROWS[0], xref="x", yref="y", axref="x", ayref="y", text="",
                           showarrow=True, arrowhead=2, arrowwidth=2.5, arrowcolor=ORANGE)
        fig.add_annotation(x=10.35, y=3.6, xanchor="left", text="to cell 0", showarrow=False,
                           font=dict(size=18, color=ORANGE))
        fig.add_annotation(x=0.5, y=ROWS[1] + 0.85, ax=-0.35, ay=3.6, xref="x", yref="y", axref="x", ayref="y",
                           text="", showarrow=True, arrowhead=2, arrowwidth=2.5, arrowcolor=ORANGE)
    low = min(y for y, row in zip(ROWS, rows) if row[2] is not None)        # cell numbers under the lowest row
    for i in range(N):
        fig.add_annotation(x=i + 0.5, y=low - 0.3, text=str(i), showarrow=False, font=dict(size=20, color=GREY))
    for y, row in ((4.1, rows[1]), (1.9, rows[2])):                    # a dashed line above every row after the first
        if row[2] is None:
            continue
        fig.add_shape(type="line", x0=-0.4, x1=15.9, y0=y, y1=y, line=dict(color=GREY, width=1, dash="dash"))
    fig.update_xaxes(range=[-0.5, 16], visible=False)
    fig.update_yaxes(range=[-0.7, 5.4], visible=False, scaleanchor="x")
    fig.update_layout(template="simple_white", width=1100, height=560, font=FONT, showlegend=False,
                      margin=dict(l=10, r=10, t=80, b=10), title=dict(text=title, x=0.5, font=dict(size=22)))
    return fig


def fmt(cells):
    return "{" + ", ".join(str(c) for c in sorted(cells)) + "}"


figs, holds, keys = [], [], []


def add(fig, hold, key=False):
    figs.append(fig)
    holds.append(hold)
    if key:
        keys.append(len(figs) - 1)


R1 = (S1, set(), ['read "door": {1, 3, 7}'], None)
U = ["{2, 3, 4}", "∪ {4, 5, 6}", "∪ {8, 9, 0}"]
NONE = (set(), set(), None, None)
add(frame("the cells the robot could be in, with a sensor that is never wrong",
          [(ALL, set(), ["no reading yet:", "any of the 10 cells"], None), NONE, NONE]), 8)
add(frame('read "door": a wall cell cannot give it, so it is crossed out',
          [(S1, ALL - S1, ['read "door":', "only the doors (brown) stay"], None), NONE, NONE]), 6)
add(frame('after the reading: {1, 3, 7}', [R1, NONE, NONE]), 5)
done = set()
for j, s in enumerate(DOORS):
    done |= reach({s})
    add(frame(f"move 2 (really 1, 2 or 3 cells): cell {s} can reach {U[j].lstrip('∪ ')}"
              + ("; the hallway is a loop" if s == 7 else ""),
              [R1, (done, set(), ["move 2 (1, 2 or 3 cells):", " ".join(U[:j + 1])], None), NONE],
              fans=DOORS[:j + 1], wrap=s == 7), 5 if s < 7 else 7)
R2 = (S2, set(), ["move 2 (1, 2 or 3 cells):", " ".join(U), f"= {fmt(S2)}"], None)
add(frame("the union: every cell that one of the doors can reach", [R1, R2, NONE], fans=DOORS, wrap=True), 7)
add(frame('read "door" again: keep only the cells that are also doors',
          [R1, R2, (S3, S2 - S3, [f"∩ {fmt(S1)}:", "the walls are crossed out"], None)], fans=DOORS, wrap=True), 6)
add(frame("the robot knows its cell: 3",
          [R1, R2, (S3, set(), ['read "door" again: only cell 3', "is both reachable and a door"], None)],
          fans=DOORS, wrap=True), 16, key=True)
add(frame('the real sensor reads "door" at a wall 20 percent of the time',
          [R1, R2, (ALL, set(), ['"door" can now be read', "in all 10 cells"], BROWN)], fans=DOORS, wrap=True), 8)
add(frame('so the second "door" crosses out nothing',
          [R1, R2, (S2, set(), ["S (the set after the move) ∩ {0, 1, …, 9}", "= S: nothing removed, 8 cells stay"], None)],
          fans=DOORS, wrap=True), 10, key=True)
add(frame("the next move fills the hallway, and no reading can empty it",
          [(S2, set(), ["after the noisy reading:", "8 cells"], None),
           (ALL, set(), ["move 2: all 10 cells"], None),
           (ALL, set(), ['read "door" (or "wall"):', "all 10 stay: the set never shrinks"], None)]), 24, key=True)
make_gif(figs, here / "sets_anim", fps=4, holds=holds, keys=keys, cols=1, width=950)
