"""Switching views on the die example (A = at least 4, B = even): each Venn region lights up together with its cell
of the contingency table, then a whole circle with its row or column total. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from anim import save_gif, FONT, ORANGE

here = Path(__file__).parent
A, B, S = {4, 5, 6}, {2, 4, 6}, set(range(1, 7))
REG = {"both": A & B, "A only": A - B, "B only": B - A, "neither": S - A - B}
assert REG == {"both": {4, 6}, "A only": {5}, "B only": {2}, "neither": {1, 3}}
POS = {5: (-1.3, 0), 4: (-0.2, 0.35), 6: (-0.2, -0.35), 2: (1.0, 0), 1: (-2.6, 1.2), 3: (2.3, -1.2)}
# table cells: (row, col) with rows = at least 4 / below 4 and cols = even / odd; totals in row/col index 2
CELL = {"both": [(0, 0)], "A only": [(0, 1)], "B only": [(1, 0)], "neither": [(1, 1)],
        "circle A": [(0, 2)], "circle B": [(2, 0)]}
COUNT = [[2, 1, 3], [1, 2, 3], [3, 3, 6]]
STEPS = [("both", "overlap ↔ cell (at least 4, even): {4, 6}"), ("A only", "A only ↔ cell (at least 4, odd): {5}"),
         ("B only", "B only ↔ cell (below 4, even): {2}"), ("neither", "outside both ↔ cell (below 4, odd): {1, 3}"),
         ("circle A", "whole circle A ↔ row total 3: {4, 5, 6}"), ("circle B", "whole circle B ↔ column total 3: {2, 4, 6}")]


def frame(key, text):
    lit = (A if key == "circle A" else B if key == "circle B" else REG[key])
    fig = go.Figure()
    fig.add_shape(type="rect", x0=-3.2, x1=3.0, y0=-1.7, y1=1.7, fillcolor="rgba(0,0,0,0)", layer="below", line=dict(color="black", width=2))
    for cx, name in ((-0.75, "A: at least 4"), (0.35, "B: even")):
        fig.add_shape(type="circle", x0=cx - 1.2, x1=cx + 1.2, y0=-1.2, y1=1.2, fillcolor="rgba(76,120,168,0.08)", layer="below", line=dict(color="#4C78A8", width=3))
        fig.add_annotation(x=cx, y=1.45, text=name, showarrow=False, font=dict(size=20, color="#4C78A8"))
    for f, (x, y) in POS.items():
        fig.add_scatter(x=[x], y=[y], mode="markers+text", text=[f"<b>{f}</b>"], textfont=dict(size=24, color="white" if f in lit else "black"),
                        marker=dict(size=46, color=ORANGE if f in lit else "#eeeeee"), showlegend=False)
    # the table, drawn at x 4..8
    rows, cols = ["at least 4", "below 4", "total"], ["even", "odd", "total"]
    for j, c in enumerate(cols):
        fig.add_annotation(x=4.9 + 1.1 * j, y=1.45, text=f"<b>{c}</b>", showarrow=False, font=dict(size=19))
    for i, r in enumerate(rows):
        fig.add_annotation(x=3.6, y=0.8 - 0.9 * i, text=f"<b>{r}</b>", showarrow=False, xanchor="right", font=dict(size=19))
        for j in range(3):
            on = (i, j) in CELL[key]
            fig.add_shape(type="rect", x0=4.4 + 1.1 * j, x1=5.4 + 1.1 * j, y0=0.4 - 0.9 * i, y1=1.2 - 0.9 * i,
                          fillcolor=ORANGE if on else "white", opacity=1, line=dict(color="#888", width=1))
            fig.add_annotation(x=4.9 + 1.1 * j, y=0.8 - 0.9 * i, text=str(COUNT[i][j]), showarrow=False,
                               font=dict(size=22, color="white" if on else "black"))
    fig.update_layout(template="simple_white", width=1400, height=520, font=FONT, title=dict(text=text, x=0.5),
                      xaxis=dict(visible=False, range=[-3.4, 7.9]), yaxis=dict(visible=False, range=[-1.9, 1.8], scaleanchor="x"),
                      margin=dict(l=10, r=10, t=70, b=10))
    return fig


if __name__ == "__main__":
    save_gif([frame(*s) for s in STEPS], "venn_table_link", here, keys=[0, 4], fps=1, holds=[3] * 5 + [5], cols=1, width=1000)
