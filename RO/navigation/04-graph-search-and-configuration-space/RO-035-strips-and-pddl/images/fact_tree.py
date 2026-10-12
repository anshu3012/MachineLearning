"""Why the number of states doubles with every fact: a tree of true/false choices for the three robot-at facts,
one fact per frame (1, 2, 4, 8 sets), then the three sets that can happen (the robot at exactly one place), then
the count for all 8 facts of the Note: 2 to the power 8 = 256. Run: python fact_tree.py -> fact_tree.gif"""
from itertools import product
from pathlib import Path

import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, RED, make_gif
from taskplan import FACTS

here = Path(__file__).parent
NAMES = ["robot-at start", "robot-at table", "robot-at door"]
SHORT = ["start", "table", "door"]
assert NAMES == FACTS[:3] and len(FACTS) == 8 and 2 ** 8 == 256
COUNTS = [(n, 2 ** n) for n in range(9)]
assert [c for _, c in COUNTS] == [1, 2, 4, 8, 16, 32, 64, 128, 256]
YL = [9.0, 6.6, 4.2, 1.8]                                   # height of each level of the tree
LEAVES = list(product([True, False], repeat=3))
POSSIBLE = [sum(leaf) == 1 for leaf in LEAVES]              # the robot is at exactly one place
assert sum(POSSIBLE) == 3 and len(LEAVES) == 8


def xpos(level, k):
    """Across position of node k (0 .. 2^level - 1) of a level, leaves spread over 0..14."""
    w = 16 / 2 ** level
    return w * (k + 0.5) - 1


def frame(level, title, mark=False, all_counts=False):
    fig = go.Figure()
    for lv in range(level + 1):
        for k in range(2 ** lv):
            x, y = xpos(lv, k), YL[lv]
            if lv < level:                                   # two branches to the next level: true (left), false
                for side, val in ((0, True), (1, False)):
                    cx, cy = xpos(lv + 1, 2 * k + side), YL[lv + 1]
                    fig.add_trace(go.Scatter(x=[x, cx], y=[y - 0.35, cy + 0.35], mode="lines",
                                             line=dict(color=GREEN if val else RED, width=3)))
                    fig.add_annotation(x=(x + cx) / 2 + (-0.25 if side == 0 else 0.25), y=(y + cy) / 2,
                                       text="true" if val else "false", showarrow=False,
                                       font=dict(size=17, color=GREEN if val else RED),
                                       xanchor="right" if side == 0 else "left")
            if lv == 3:
                leaf = LEAVES[k]
                txt = "{" + ", ".join(s for s, v in zip(SHORT, leaf) if v) + "}"
                col = "black"
                if mark:
                    col = BLUE if POSSIBLE[k] else "#BBBBBB"
                fig.add_annotation(x=x, y=y - 0.15, text=txt.replace(", ", ",<br>") if sum(leaf) > 1 else txt,
                                   showarrow=False, yanchor="top", font=dict(size=16, color=col))
                fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(
                    size=16, color=(BLUE if POSSIBLE[k] else "#DDDDDD") if mark else GREY)))
                if mark and not POSSIBLE[k]:
                    fig.add_annotation(x=x + 0.42, y=y, text="×", showarrow=False, font=dict(size=26, color=RED))
            else:
                fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(size=16, color=GREY)))
        if 0 < lv:
            fig.add_annotation(x=-1.2, y=(YL[lv - 1] + YL[lv]) / 2, text=f"<b>{NAMES[lv - 1]}</b>?", showarrow=False,
                               xanchor="right", font=dict(size=17))
    # the running count on the right
    rows = COUNTS if all_counts else COUNTS[:level + 1]
    lines = ["<b>facts decided → sets</b>"] + [f"{n} → {c}" for n, c in rows]
    fig.add_annotation(x=17.6, y=9.6, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                       align="left", font=dict(size=19))
    if level == 3:
        fig.add_annotation(x=-1.2, y=YL[3] - 0.5, text="robot-at<br>true at:", showarrow=False, xanchor="right",
                           font=dict(size=16, color=GREY))
    if mark and not all_counts:
        fig.add_annotation(x=7, y=-0.9, text="blue: the robot at exactly one place, the 3 sets that can happen",
                           showarrow=False, font=dict(size=17, color=BLUE))
    if all_counts:
        fig.add_annotation(x=7, y=-0.9, text="5 more facts, each true or false: 8 × 2 × 2 × 2 × 2 × 2 = 256 sets",
                           showarrow=False, font=dict(size=18))
    fig.update_layout(template="simple_white", font=FONT, width=1150, height=640, showlegend=False,
                      margin=dict(l=20, r=20, t=70, b=20), title=dict(x=0.5, text=title),
                      xaxis=dict(visible=False, range=[-6.6, 24]), yaxis=dict(visible=False, range=[-1.4, 9.9]))
    return fig


figs = [frame(0, "no fact decided yet: 1 set"),
        frame(1, "robot-at start, true or false: 2 sets"),
        frame(2, "add robot-at table: each set splits in two, 4 sets"),
        frame(3, "add robot-at door: 8 sets"),
        frame(3, "only 3 of the 8 sets can happen", mark=True),
        frame(3, "all 8 facts of the task: 256 sets", mark=True, all_counts=True)]
make_gif(figs, here / "fact_tree", fps=1, holds=[2, 3, 3, 4, 5, 10], keys=[1, 3, 4, 5], cols=2, width=900)
