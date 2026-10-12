"""Scoring a possible end pose with the odometry model (Section 4.4), played. Odometry reported turn 0.500 rad, drive
0.479 m, turn 0.500 rad (Section 4.2). Stage 1: the robot drives the turn, drive, turn that would take the start
(2, 1, 30 deg) to the pose (2.27, 1.38, 1.50): 0.4294 rad, 0.4662 m, 0.5470 rad, drawn against odometry's (grey).
Stage 2: each part against its Gaussian, centred on odometry's value with the standard deviations of Section 4.3
(0.0979 rad, 0.0579 m, 0.0979 rad); the gap is marked and the density read off: 3.142, 6.724, 3.631; their product is
76.7. Stage 3: the far pose (2.10, 1.60, 1.50) for contrast: 0.8820 rad, 0.6083 m, 0.0944 rad; densities 0.0020,
0.57, 0.00076; product 8.7e-7. The last frame holds both scores.
Run: python pose_score_anim.py -> pose_score_anim.gif, pose_score_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from motion import ODO_END, START, odo_deltas, odo_sds
from plotly.subplots import make_subplots
from robotdraw import robot

here = Path(__file__).parent
X0, Y0, TH0 = START
U = (0.500, 0.479, 0.500)                                  # odometry's report, Section 4.2
SD = odo_sds(U)                                             # Section 4.3
NEAR, FAR = (2.27, 1.38, 1.50), (2.10, 1.60, 1.50)
HN = [round(v, 4) for v in odo_deltas(START, NEAR)]         # this pose's turn, drive, turn (the hatted values)
HF = [round(v, 4) for v in odo_deltas(START, FAR)]
dens = lambda a, s: np.exp(-a * a / (2 * s * s)) / np.sqrt(2 * np.pi * s * s)
GN = [round(U[i] - HN[i], 4) for i in range(3)]             # gaps a, odometry's value minus the hatted value
GF = [round(U[i] - HF[i], 4) for i in range(3)]
PN = [dens(GN[i], SD[i]) for i in range(3)]
PF = [dens(GF[i], SD[i]) for i in range(3)]
PN_S = [f"{p:.3f}" for p in PN]
PF_S = [f"{PF[0]:.4f}", f"{PF[1]:.2f}", f"{PF[2]:.5f}"]     # two significant figures each
assert [round(s, 4) for s in SD] == [0.0979, 0.0579, 0.0979]
assert HN == [0.4294, 0.4662, 0.5470] and GN == [0.0706, 0.0128, -0.047]
assert PN_S == ["3.142", "6.724", "3.631"] and round(np.prod(PN), 1) == 76.7 and round(3.142 * 6.724 * 3.631, 1) == 76.7
assert HF == [0.8820, 0.6083, 0.0944] and GF == [-0.382, -0.1293, 0.4056]
assert PF_S == ["0.0020", "0.57", "0.00076"] and round(0.0020 * 0.57 * 0.00076 * 1e7, 1) == 8.7
FULL_F = [dens(U[i] - h, SD[i]) for i, h in enumerate(odo_deltas(START, FAR))]
assert round(np.prod(FULL_F) * 1e7, 1) == 8.7                # the Note's 8.7e-7 (notebook, full precision)
CN, CF, CO = TH0 + HN[0], TH0 + HF[0], TH0 + U[0]            # directions of the three straight drives
UNIT = ("rad", "m", "rad")
PART = ("first turn", "drive", "second turn")
SC = 0.2                                                     # robots drawn at 0.2 of RO-001's size (said in frame)
H_ODO = "odometry: first turn 0.500 rad, drive 0.479 m, second turn 0.500 rad"


def line_this(n, who, h, col):
    """Header line listing the first n parts of a pose's turn, drive, turn."""
    parts = [f"{PART[i]} {h[i]:.4f} {UNIT[i]}" for i in range(n)]
    return f"<span style='font-size:20px;color:{col}'>{who}: {', '.join(parts) if parts else '…'}</span>"


def header(title, n_near, n_far=None):
    s = f"{title}<br><span style='font-size:20px;color:{GREY}'>{H_ODO}</span><br>{line_this(n_near, 'this pose', HN, BLUE)}"
    if n_far is not None:
        s += f"<br>{line_this(n_far, 'far pose', HF, RED)}"
    return s


def label(fig, x, y, s, col, anchor="center", size=20, **kw):
    fig.add_annotation(x=x, y=y, text=s, showarrow=False, xanchor=anchor, font=dict(color=col, size=size), **kw)


def arrow(fig, x, y, th, n, col, width=4):
    fig.add_trace(go.Scatter(x=[x, x + n * np.cos(th)], y=[y, y + n * np.sin(th)], mode="lines+markers",
                             line=dict(color=col, width=width),
                             marker=dict(symbol="arrow", size=[0, 14], angleref="previous", color=col)))


def wedge(fig, cx, cy, a0, a1, r, col):
    t = np.linspace(a0, a1, 30)
    fig.add_trace(go.Scatter(x=cx + r * np.cos(t), y=cy + r * np.sin(t), mode="lines+markers",
                             line=dict(color=col, width=3),
                             marker=dict(symbol="arrow", size=[0] * 29 + [12], angleref="previous", color=col)))


def path(fig, h, chord, end, prog, col, r_wedge):
    """Draw how far a pose's turn, drive, turn has got: prog = (r1, d, r2) done so far."""
    r1, d, r2 = prog
    if r1 > 0:
        wedge(fig, X0, Y0, TH0, TH0 + r1, r_wedge, col)
    if d > 0:
        fig.add_trace(go.Scatter(x=[X0, X0 + d * np.cos(chord)], y=[Y0, Y0 + d * np.sin(chord)], mode="lines",
                                 line=dict(color=col, width=5)))
    if r2 > 0:
        wedge(fig, end[0], end[1], chord, chord + r2, 0.055, col)


def map_frame(title, near, far=None, n_near=0, n_far=None, near_faded=False):
    """near, far: progress (r1, d, r2) of this pose's and the far pose's turn, drive, turn (far None: not shown)."""
    fig = go.Figure()
    # odometry's report, grey: first turn, straight drive, end pose with its heading
    wedge(fig, X0, Y0, TH0, CO, 0.11, GREY)
    fig.add_trace(go.Scatter(x=[X0, ODO_END[0]], y=[Y0, ODO_END[1]], mode="lines",
                             line=dict(color=GREY, dash="dash", width=3)))
    arrow(fig, ODO_END[0], ODO_END[1], ODO_END[2], 0.1, GREY, 3)
    fig.add_trace(go.Scatter(x=[ODO_END[0]], y=[ODO_END[1]], mode="markers", marker=dict(size=12, color=GREY)))
    label(fig, 2.30, 1.49, "odometry's end<br>(2.249, 1.409)", GREY, "left", align="left")
    arrow(fig, X0, Y0, TH0, 0.14, ORANGE)
    label(fig, 2.13, 1.04, "start heading 30°", ORANGE, "left", 19)
    label(fig, 1.975, 0.945, "start (2, 1)", "black", "right")
    # this pose, blue
    fig.add_trace(go.Scatter(x=[NEAR[0]], y=[NEAR[1]], mode="markers", marker=dict(size=12, color=BLUE)))
    arrow(fig, NEAR[0], NEAR[1], NEAR[2], 0.1, BLUE, 3)
    label(fig, 2.31, 1.33, "this pose<br>(2.27, 1.38)", BLUE, "left", align="left")
    path(fig, HN, CN, NEAR, near, BLUE, 0.08)
    if far is not None:
        fig.add_trace(go.Scatter(x=[FAR[0]], y=[FAR[1]], mode="markers", marker=dict(size=12, color=RED)))
        arrow(fig, FAR[0], FAR[1], FAR[2], 0.1, RED, 3)
        label(fig, 2.14, 1.62, "far pose (2.10, 1.60)", RED, "left")
        path(fig, HF, CF, FAR, far, RED, 0.15)
    r1, d, r2 = near
    q = (X0 + d * np.cos(CN), Y0 + d * np.sin(CN), TH0 + r1 + r2)
    for tr in robot(q, scale=SC, opacity=0.35 if near_faded else 1.0, arrow=not near_faded):
        fig.add_trace(tr)
    if far is not None:
        r1, d, r2 = far
        q = (X0 + d * np.cos(CF), Y0 + d * np.sin(CF), TH0 + r1 + r2)
        for tr in robot(q, scale=SC, color=RED, fill="rgba(228,87,86,0.18)"):
            fig.add_trace(tr)
    fig.add_trace(go.Scatter(x=[X0], y=[Y0], mode="markers", marker=dict(size=12, color="black")))
    label(fig, 2.49, 0.925, "robots drawn at 1/5 of their size", GREY, "right", 17)
    fig.update_xaxes(range=[1.82, 2.50], dtick=0.1, showgrid=True, gridcolor="#e4e4e4", title="x (m)")
    fig.update_yaxes(range=[0.90, 1.76], dtick=0.1, showgrid=True, gridcolor="#e4e4e4", title="y (m)",
                     scaleanchor="x")
    fig.update_layout(template="simple_white", width=900, height=1200, font=FONT, showlegend=False,
                      margin=dict(l=80, r=30, t=200, b=70),
                      title=dict(x=0.5, y=0.975, yanchor="top", font=dict(size=23),
                                 text=header(title, n_near, n_far)))
    return fig


XR = [(0.05, 0.95), (0.29, 0.67), (0.05, 0.95)]
PEAK = [dens(0, s) for s in SD]
SIDE_N, SIDE_F = ("left", "left", "right"), ("right", "right", "left")   # corner for each label, clear of the bell


def mark(fig, i, h, g, p, p_s, who, col, side, stage, y_bar):
    """Mark one pose's value h on panel i: stage 1 = the gap g from odometry's value; stage 2 = also the density p."""
    row, unit, pk = i + 1, UNIT[i], PEAK[i]
    # the gap a = odometry's value minus h, drawn from h towards odometry's value (points right when a > 0)
    fig.add_trace(go.Scatter(x=[h, U[i]], y=[y_bar * pk] * 2, mode="lines+markers", line=dict(color=col, width=5),
                             marker=dict(symbol="arrow", size=[0, 13], angleref="previous", color=col)), row, 1)
    if stage == 2:                                       # read the density off the curve at h
        fig.add_trace(go.Scatter(x=[h, h], y=[0, p], mode="lines", line=dict(color=col, width=2, dash="dot")),
                      row, 1)
    lines = [f"{who} {h:.4f} {unit}", f"gap a = {g:+.4f} {unit}".replace("-", "−")]
    lo, hi = XR[i]
    span = hi - lo
    lx = lo + 0.01 * span if side == "left" else hi - 0.01 * span
    if stage == 2:
        lines.append(f"p<sub>{i + 1}</sub> = {p_s} per {unit}")
        fig.add_trace(go.Scatter(x=[h], y=[p], mode="markers", marker=dict(size=13, color=col)), row, 1)
        tx = lo + 0.12 * span if side == "left" else hi - 0.12 * span
        fig.add_annotation(x=h, y=p, ax=tx, ay=0.83 * pk, axref=f"x{row if row > 1 else ''}",
                           ayref=f"y{row if row > 1 else ''}", text="", showarrow=True, arrowhead=2, arrowwidth=2,
                           arrowcolor=col, standoff=6, row=row, col=1)
    fig.add_annotation(x=lx, y=1.33 * pk, text="<br>".join(lines), showarrow=False, xanchor=side, yanchor="top",
                       align=side, font=dict(color=col, size=19), row=row, col=1)


def gauss_frame(title, n_marks, near_stage=None, far=False, products=0, n_far=None):
    """n_marks: panels with this pose marked (the last of them at near_stage, earlier ones at stage 2);
    far: mark the far pose on all panels; products: 0 none, 1 this pose's, 2 both."""
    titles = [f"{PART[i]}: Gaussian around odometry's {U[i]:.3f} {UNIT[i]}, σ = {SD[i]:.4f} {UNIT[i]}"
              for i in range(3)]
    fig = make_subplots(rows=3, cols=1, vertical_spacing=0.1, subplot_titles=titles)
    for i in range(3):
        lo, hi = XR[i]
        xs = np.linspace(lo, hi, 400)
        fig.add_trace(go.Scatter(x=xs, y=dens(xs - U[i], SD[i]), mode="lines", line=dict(color=GREY, width=3),
                                 fill="tozeroy", fillcolor="rgba(107,107,107,0.12)"), i + 1, 1)
        fig.add_trace(go.Scatter(x=[U[i], U[i]], y=[0, PEAK[i]], mode="lines",
                                 line=dict(color=GREY, width=2, dash="dash")), i + 1, 1)
        fig.update_xaxes(range=[lo, hi], row=i + 1, col=1, ticks="outside")
        fig.update_yaxes(range=[0, 1.36 * PEAK[i]], title=f"per {UNIT[i]}", row=i + 1, col=1)
        if i < n_marks:
            st = near_stage if i == n_marks - 1 and near_stage else 2
            mark(fig, i, HN[i], GN[i], PN[i], PN_S[i], "this pose", BLUE, SIDE_N[i], st, 0.13)
        if far:
            mark(fig, i, HF[i], GF[i], PF[i], PF_S[i], "far pose", RED, SIDE_F[i], 2, 0.05)
    if products >= 1:
        label(fig, 0.5, -0.095, f"this pose: p<sub>1</sub> p<sub>2</sub> p<sub>3</sub> = {PN_S[0]} × {PN_S[1]} × "
              f"{PN_S[2]} = 76.7", BLUE, size=22, xref="paper", yref="paper")
    if products >= 2:
        label(fig, 0.5, -0.14, f"far pose: p<sub>1</sub> p<sub>2</sub> p<sub>3</sub> = {PF_S[0]} × {PF_S[1]} × "
              f"{PF_S[2]} = 8.7 × 10<sup>−7</sup>", RED, size=22, xref="paper", yref="paper")
    for t in titles:
        fig.update_annotations(selector=dict(text=t), font_size=20)
    fig.update_layout(template="simple_white", width=900, height=1200, font=FONT, showlegend=False,
                      margin=dict(l=80, r=30, t=200, b=150),
                      title=dict(x=0.5, y=0.975, yanchor="top", font=dict(size=23),
                                 text=header(title, 3, n_far)))
    return fig


T1 = "1. how likely is the pose (2.27, 1.38, 1.50)? its turn, drive, turn"
T2 = "2. each part against its Gaussian; the densities multiply"
T3 = "3. for contrast, the far pose (2.10, 1.60, 1.50)"
figs, holds = [], []
add = lambda f, h: (figs.append(f), holds.append(h))
add(map_frame(T1, (0, 0, 0)), 10)
for k in (1, 2, 3):
    add(map_frame(T1, (HN[0] * k / 3, 0, 0), n_near=1 if k == 3 else 0), 2 if k < 3 else 4)
for k in (1, 2, 3):
    add(map_frame(T1, (HN[0], HN[1] * k / 3, 0), n_near=1 if k < 3 else 2), 2 if k < 3 else 4)
for k in (1, 2, 3):
    add(map_frame(T1, (HN[0], HN[1], HN[2] * k / 3), n_near=2 if k < 3 else 3), 2 if k < 3 else 8)
keys = [len(figs) - 1]
add(gauss_frame(T2, 0), 6)
for i in (1, 2, 3):
    add(gauss_frame(T2, i, near_stage=1), 4)
    add(gauss_frame(T2, i, near_stage=2), 6)
add(gauss_frame(T2, 3, products=1), 12)
keys.append(len(figs) - 1)
DONE = (HN[0], HN[1], HN[2])
add(map_frame(T3, DONE, far=(0, 0, 0), n_near=3, n_far=0, near_faded=True), 6)
for k in (1, 2, 3):
    add(map_frame(T3, DONE, far=(HF[0] * k / 3, 0, 0), n_near=3, n_far=1 if k == 3 else 0, near_faded=True),
        2 if k < 3 else 3)
for k in (1, 2, 3):
    add(map_frame(T3, DONE, far=(HF[0], HF[1] * k / 3, 0), n_near=3, n_far=1 if k < 3 else 2, near_faded=True),
        2 if k < 3 else 3)
add(map_frame(T3, DONE, far=(HF[0], HF[1], HF[2]), n_near=3, n_far=3, near_faded=True), 8)
keys.append(len(figs) - 1)
add(gauss_frame("this pose scores 76.7; the far pose 8.7 × 10<sup>−7</sup>", 3, far=True, products=2, n_far=3), 28)
keys.append(len(figs) - 1)
make_gif(figs, here / "pose_score_anim", fps=4, holds=holds, keys=keys, cols=2, width=850)
