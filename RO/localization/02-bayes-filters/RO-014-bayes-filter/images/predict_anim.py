"""Figure 4 as an animation: the prediction step at t = 2 (command: push), path by path. Left: the probability tree;
the first branch is the belief after t = 1 (open 0.75, closed 0.25), the second what a
push does (an open door stays open; a closed one opens with 0.8). Right: the belief as bars. Path 1 keeps 0.75 on
open; path 2 moves nothing; path 3 lifts 0.2 off the closed bar and stacks it on open; path 4 leaves 0.05 on closed.
Blue: belief after t = 1; orange: predicted belief. The last frame is the still: 0.75 + 0.2 = 0.95 open, 0.05 closed.
Run -> predict_anim.gif, predict_anim_frames.png"""
from pathlib import Path

import plotly.graph_objects as go

from doorplot import P_X, predict, update
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
b1 = update(predict({"open": 0.5, "closed": 0.5}, "do nothing"), "open")      # belief after t = 1: 0.75 / 0.25
bb2 = predict(b1, "push")                                                     # predicted belief at t = 2
PO, PC = round(b1["open"], 12), round(b1["closed"], 12)
PUSH = P_X["push"]
# (was, now, edge probability, product); top to bottom as in the still
PATHS = [(w, n, PUSH[w][n], round((PO if w == "open" else PC) * PUSH[w][n], 12))
         for w in ("open", "closed") for n in ("open", "closed")]
assert [p[3] for p in PATHS] == [0.75, 0.0, 0.2, 0.05]
assert abs(bb2["open"] - 0.95) < 1e-12 and abs(bb2["closed"] - 0.05) < 1e-12

NODE = {"start": (0.7, 0.0, 1.3), "was open": (3.6, 1.6, 2.1), "was closed": (3.6, -1.6, 2.1)}
LEAF_Y = [2.4, 0.8, -0.8, -2.4]
COL = {"open": GREEN, "closed": RED}
LIGHT = {GREEN: "#E8F3E7", RED: "#FCE9E9", GREY: "#EEEEEE"}
W = 0.55                                                                       # bar width


def box(fig, x, y, w, text, col):
    fig.add_shape(type="rect", x0=x - w / 2, x1=x + w / 2, y0=y - 0.42, y1=y + 0.42, line=dict(color=col, width=2),
                  fillcolor=LIGHT[col], opacity=1, xref="x", yref="y")
    fig.add_annotation(x=x, y=y, text=text, showarrow=False, font=dict(size=21), xref="x", yref="y")


def edge(fig, a, b, label, lx, ly, active):
    fig.add_annotation(x=b[0], y=b[1], ax=a[0], ay=a[1], xref="x", yref="y", axref="x", ayref="y", text="",
                       showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=3.5 if active else 2,
                       arrowcolor="black" if active else GREY)
    fig.add_annotation(x=lx, y=ly, text=label, showarrow=False, font=dict(size=21), xref="x", yref="y")


def tree(fig, done, active):
    """done: paths drawn so far (0-3); active: the path being explained (None for the first and last frame)."""
    box(fig, *NODE["start"][:2], NODE["start"][2], "start", GREY)
    for name, lab, ly in (("was open", "0.75", 1.15), ("was closed", "0.25", -1.15)):
        x, y, w = NODE[name]
        box(fig, x, y, w, name, COL[name.split()[1]])
        edge(fig, (1.35, 0.0), (x - w / 2 - 0.05, y), lab, 1.62, ly,
             active is not None and PATHS[active][0] == name.split()[1])
    for i in done:
        was, now, p, prod = PATHS[i]
        x0, y0, w0 = NODE[f"was {was}"]
        y = LEAF_Y[i]
        box(fig, 7.3, y, 2.1, f"now {now}", COL[now])
        edge(fig, (x0 + w0 / 2, y0), (6.2, y), f"{p:g}", 5.4, (y + y0) / 2 + (0.32 if y > y0 else -0.32), i == active)
        fig.add_annotation(x=8.55, y=y, text=f"{PO if was == 'open' else PC:g} × {p:g} = {prod:g}", showarrow=False,
                           xanchor="left", font=dict(size=21, color="black" if i == active or active is None else GREY),
                           xref="x", yref="y")
    fig.add_annotation(x=1.9, y=-3.35, text="first branch: belief after t = 1", showarrow=False,
                       font=dict(size=17, color=GREY), xref="x", yref="y")
    if done:
        fig.add_annotation(x=7.3, y=-3.35, text="second branch: what a push does", showarrow=False,
                           font=dict(size=17, color=GREY), xref="x", yref="y")


def piece(fig, x, y0, h, col, label=None, inside=True):
    fig.add_shape(type="rect", x0=x - W / 2, x1=x + W / 2, y0=y0, y1=y0 + h, fillcolor=col, line=dict(color="white", width=2),
                  opacity=1, xref="x2", yref="y2")
    if label:
        fig.add_annotation(x=x, y=y0 + h / 2 if inside else y0 + h + 0.045, text=label, showarrow=False, xref="x2",
                           yref="y2", font=dict(size=20, color="white" if inside else "black"))


def frame(title, sub, done, active, bars, totals=None, sums=False):
    """bars: list of (x, y0, h, colour, label, inside) rectangles; totals: labels above the two bars."""
    fig = go.Figure()
    tree(fig, done, active)
    for b in bars:
        piece(fig, *b)
    for x, (y, s) in (totals or {}).items():
        fig.add_annotation(x=x, y=y + 0.045, text=s, showarrow=False, xref="x2", yref="y2", font=dict(size=20))
    if sums:
        fig.add_annotation(x=5.9, y=-4.15, text="now open: 0.75 + 0.2 = 0.95", showarrow=False, xanchor="left",
                           font=dict(size=24, color=GREEN), xref="x", yref="y")
        fig.add_annotation(x=5.9, y=-4.85, text="now closed: 0 + 0.05 = 0.05", showarrow=False, xanchor="left",
                           font=dict(size=24, color=RED), xref="x", yref="y")
    fig.add_annotation(x=0.855, y=1.0, xref="paper", yref="paper", showarrow=False, yanchor="bottom",
                       text=f"<span style='color:{BLUE}'>blue: belief after t = 1</span><br>"
                            f"<span style='color:{ORANGE}'>orange: predicted belief</span>", font=dict(size=19))
    fig.update_layout(template="simple_white", width=1250, height=700, font=FONT, showlegend=False,
                      margin=dict(l=20, r=20, t=140, b=50),
                      xaxis=dict(domain=[0, 0.66], range=[-0.1, 12.4], visible=False),
                      yaxis=dict(domain=[0, 1], range=[-5.3, 3.0], visible=False),
                      xaxis2=dict(domain=[0.75, 1.0], range=[-0.6, 1.6], anchor="y2", tickvals=[0, 1],
                                  ticktext=["open", "closed"]),
                      yaxis2=dict(domain=[0.08, 0.86], range=[0, 1.12], anchor="x2", title="probability"),
                      title=dict(text=f"{title}<br><span style='font-size:19px'>{sub}</span>", x=0.5, y=0.96,
                                 yanchor="top", font=dict(size=24)))
    return fig


T = "t = 2, predict: u<sub>2</sub> = push"
A = (0, 0.0, PO)                           # the open bar, path 1
C = (1, 0.0, 0.05)                         # what stays on closed, path 4
B = 0.2                                    # what moves from closed to open, path 3
figs, holds, keys = [], [], []


def add(f, hold, key=False):
    if key:
        keys.append(len(figs))
    figs.append(f)
    holds.append(hold)


add(frame(T, "before the push: belief after t = 1, 0.75 open and 0.25 closed", [], None,
          [(*A, BLUE), (1, 0.0, PC, BLUE)], {0: (PO, "0.75"), 1: (PC, "0.25")}), 9, key=True)
add(frame("path 1: was open, the push keeps it open (1)", "0.75 × 1 = 0.75 stays on open", [0], 0,
          [(*A, ORANGE, "0.75"), (1, 0.0, PC, BLUE)], {1: (PC, "0.25")}), 9, key=True)
add(frame("path 2: was open, the push never closes it (0)", "0.75 × 0 = 0 goes to closed: nothing moves", [0, 1], 1,
          [(*A, ORANGE, "0.75"), (1, 0.0, PC, BLUE)], {1: (PC, "0.25")}), 8)
P3 = ("path 3: was closed, the push opens it (0.8)", "0.25 × 0.8 = 0.2 moves from closed to open")
add(frame(*P3, [0, 1, 2], 2, [(*A, ORANGE, "0.75"), (*C, BLUE), (1, 0.05, B, BLUE, "0.2")]), 7, key=True)
for x, y0 in ((1, 0.75), (0.5, 0.75)):                           # lift 0.2 above the bars, then slide it across
    add(frame(*P3, [0, 1, 2], 2, [(*A, ORANGE, "0.75"), (*C, BLUE, "0.05", False), (x, y0, B, BLUE, "0.2")]), 2,
        key=x == 0.5)
add(frame(*P3, [0, 1, 2], 2, [(*A, ORANGE, "0.75"), (*C, BLUE, "0.05", False), (0, PO, B, ORANGE, "0.2")]), 8)
add(frame("path 4: was closed, the push fails (0.2)", "0.25 × 0.2 = 0.05 stays on closed", [0, 1, 2, 3], 3,
          [(*A, ORANGE, "0.75"), (*C, ORANGE, "0.05", False), (0, PO, B, ORANGE, "0.2")]), 9, key=True)
add(frame("predicted belief: add the paths that end in each state", "open: 0.75 + 0.2 = 0.95     closed: 0 + 0.05 = 0.05",
          [0, 1, 2, 3], None, [(*A, ORANGE, "0.75"), (*C, ORANGE), (0, PO, B, ORANGE, "0.2")],
          {0: (PO + B, "0.95"), 1: (0.05, "0.05")}, sums=True), 24, key=True)
make_gif(figs, here / "predict_anim", fps=4, holds=holds, keys=keys, cols=2, width=950)
assert abs(PO + B - bb2["open"]) < 1e-12 and abs(C[2] - bb2["closed"]) < 1e-12        # the bars are 0.95 and 0.05
