"""The one-dimensional Kalman filter as a loop, run for steps 1 and 2, one stage per frame. The box or arrow in use is
drawn thick and dark; the numbers of each stage appear in its box. Step 1: predict 0 -> 0.5 m, variance 1 -> 1.01 m²;
update with the reading 0.82 m: K = 0.863, estimate 0.776 m, variance 0.138 m². Step 2 starts from those: predict
1.276 m, 0.148 m²; update with 1.85 m: K = 0.481, estimate 1.552 m, variance 0.077 m². The first frame is the plain
loop; the last frame hands step 2's estimate on to step 3.
Run: python kf_cycle_anim.py -> kf_cycle_anim.gif, kf_cycle_anim_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE, make_gif
from kfsim import P0, Q, R, U, X0, Z, kf1d

here = Path(__file__).parent
r1, r2 = kf1d()[:2]
# every number a frame shows, as printed, and the arithmetic between them as printed
assert (X0, P0, U, Q, R) == (0.0, 1.0, 0.5, 0.01, 0.16) and tuple(Z[:2]) == (0.82, 1.85)
assert round(r1["x_pred"], 3) == 0.5 and round(r1["p_pred"], 3) == 1.01
assert round(r1["K"], 3) == 0.863 and round(1.01 / 1.17, 3) == 0.863
assert round(r1["x"], 3) == 0.776 and round(0.5 + 0.863 * 0.32, 3) == 0.776
assert round(r1["p"], 3) == 0.138 and round(0.137 * 1.01, 3) == 0.138
assert round(r2["x_pred"], 3) == 1.276 and round(r2["p_pred"], 3) == 0.148
assert round(r2["K"], 3) == 0.481 and round(0.148 / 0.308, 3) == 0.481
assert round(r2["x"], 3) == 1.552 and round(1.276 + 0.481 * 0.574, 3) == 1.552
assert round(r2["p"], 3) == 0.077 and round(0.519 * 0.148, 3) == 0.077

xb, pb, xh = "<i>x̄</i>", "<i>p̄</i>", "<i>x̂</i>"
PRED = {1: [f"{xb}<sub>1</sub> = 0 + 0.5 = 0.5 m", f"{pb}<sub>1</sub> = 1 + 0.01 = 1.01 m²"],
        2: [f"{xb}<sub>2</sub> = 0.776 + 0.5 = 1.276 m", f"{pb}<sub>2</sub> = 0.138 + 0.01 = 0.148 m²"]}
UPD = {1: ["<i>z</i><sub>1</sub> = 0.82 m", "<i>K</i><sub>1</sub> = 1.01 / 1.17 = 0.863",
           f"{xh}<sub>1</sub> = 0.5 + 0.863 × 0.32 = 0.776 m", "<i>p</i><sub>1</sub> = 0.137 × 1.01 = 0.138 m²"],
       2: ["<i>z</i><sub>2</sub> = 1.85 m", "<i>K</i><sub>2</sub> = 0.148 / 0.308 = 0.481",
           f"{xh}<sub>2</sub> = 1.276 + 0.481 × 0.574 = 1.552 m", "<i>p</i><sub>2</sub> = 0.519 × 0.148 = 0.077 m²"]}
HAND = {1: f"{xb}<sub>1</sub> = 0.5 m<br>{pb}<sub>1</sub> = 1.01 m²", 2: f"{xb}<sub>2</sub> = 1.276 m<br>{pb}<sub>2</sub> = 0.148 m²"}
BACK = {1: f"{xh}<sub>1</sub> = 0.776 m, <i>p</i><sub>1</sub> = 0.138 m²: the start of step 2",
        2: f"{xh}<sub>2</sub> = 1.552 m, <i>p</i><sub>2</sub> = 0.077 m²: the start of step 3"}
# box corners in plot units (x 0..100, y 0..60)
PB, UB = (1, 40, 23, 47), (60, 99, 18, 52)
PC, UC = (PB[0] + PB[1]) / 2, (UB[0] + UB[1]) / 2       # box centres across


def rgba(hexc, a):
    return f"rgba({int(hexc[1:3], 16)},{int(hexc[3:5], 16)},{int(hexc[5:7], 16)},{a})"


def frame(title, on=None, pred=None, upd=None, hand=None, back=None):
    """on: the element in use ('start', 'predict', 'hand', 'update', 'back'); pred/upd: the step whose numbers each box
    shows; hand/back: the step whose numbers the two arrows carry."""
    fig = go.Figure()

    def box(c, col, name, lines, nums, now):
        x0, x1, y0, y1 = c
        fig.add_shape(type="rect", x0=x0, x1=x1, y0=y0, y1=y1, line=dict(color=col, width=6 if now else 2.5),
                      fillcolor=rgba(col, 0.28 if now else 0.08), layer="below", opacity=1)
        txt = "<br>".join([f"<b>{name}</b>"] + lines)
        fig.add_annotation(x=(x0 + x1) / 2, y=y1 - 1.5, text=txt, showarrow=False, yanchor="top",
                           font=dict(size=23, color="black" if now or on is None else GREY))
        if nums:
            fig.add_annotation(x=(x0 + x1) / 2, y=y0 + 1.5, text="<br>".join(nums), showarrow=False, yanchor="bottom",
                               font=dict(size=20, color="black" if now else GREY))

    box(PB, BLUE, "predict (motion)", [f"{xb} = {xh} + <i>u</i>", f"{pb} = <i>p</i> + <i>Q</i>",
                                       "<span style='font-size:18px'>the Gaussian moves and widens</span>"],
        PRED.get(pred), on == "predict")
    box(UB, ORANGE, "update (reading <i>z</i>)",
        [f"<i>K</i> = {pb} / ({pb} + <i>R</i>)", f"{xh} = {xb} + <i>K</i> (<i>z</i> − {xb})",
         f"<i>p</i> = (1 − <i>K</i>) {pb}", "<span style='font-size:18px'>the Gaussian moves towards <i>z</i>"
         " and narrows</span>"], UPD.get(upd), on == "update")

    def arrow(x0, y0, x1, y1, now, head=True):
        col, w = ("black", 5) if now else ("#BBBBBB" if on else GREY, 3)
        if head:
            fig.add_annotation(x=x1, y=y1, ax=x0, ay=y0, xref="x", yref="y", axref="x", ayref="y", text="",
                               showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=w, arrowcolor=col)
        else:
            fig.add_shape(type="line", x0=x0, y0=y0, x1=x1, y1=y1, line=dict(color=col, width=w), opacity=1)

    def label(x, y, txt, now, **kw):
        col = "black" if now else ("#999999" if on else GREY)
        fig.add_annotation(x=x, y=y, text=txt, showarrow=False, font=dict(size=20, color=col), **kw)

    # start note and its arrow into predict
    label(1, 57, f"start: a first guess {xh}<sub>0</sub> = 0 m with variance <i>p</i><sub>0</sub> = 1 m²",
          on == "start", xanchor="left")
    arrow(PC, 55, PC, PB[3] + 0.4, on == "start")
    # predict -> update
    arrow(PB[1], 35, UB[0] - 0.4, 35, on == "hand")
    label(50, 36.5, HAND[hand] if hand else f"{xb}, {pb}", on == "hand", yanchor="bottom")
    # update -> back to predict, round the bottom
    arrow(UC, UB[2], UC, 8, on == "back", head=False)
    arrow(UC, 8, PC, 8, on == "back", head=False)
    arrow(PC, 8, PC, PB[2] - 0.4, on == "back")
    label(50, 6.5, BACK[back] if back else f"{xh}, <i>p</i>: next step", on == "back", yanchor="top")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=720, margin=dict(l=20, r=20, t=80, b=20),
                      title=dict(x=0.5, y=0.975, yanchor="top", text=title), showlegend=False,
                      xaxis=dict(visible=False, range=[0, 100]), yaxis=dict(visible=False, range=[0, 60]))
    return fig


figs = [frame("the loop: predict, then update, every step"),
        frame("step 1: start from the first guess", on="start"),
        frame("step 1: predict with the command <i>u</i> = 0.5 m", on="predict", pred=1),
        frame("step 1: the prediction goes to the update", on="hand", pred=1, hand=1),
        frame("step 1: update with the reading <i>z</i><sub>1</sub> = 0.82 m", on="update", pred=1, upd=1, hand=1),
        frame("step 1 done: its estimate goes round to step 2", on="back", pred=1, upd=1, hand=1, back=1),
        frame("step 2: predict from step 1's estimate", on="predict", pred=2, upd=1, back=1),
        frame("step 2: the prediction goes to the update", on="hand", pred=2, upd=1, hand=2, back=1),
        frame("step 2: update with the reading <i>z</i><sub>2</sub> = 1.85 m", on="update", pred=2, upd=2, hand=2,
              back=1),
        frame("step 2 done: its estimate goes round to step 3", on="back", pred=2, upd=2, hand=2, back=2)]
make_gif(figs, here / "kf_cycle_anim", fps=1, holds=[4, 3, 5, 3, 6, 4, 5, 3, 6, 12], keys=[0, 2, 4, 9], cols=2,
         width=850)
