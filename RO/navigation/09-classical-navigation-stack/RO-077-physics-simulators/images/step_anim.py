"""How one simulator step works, on the box falling from 0.1 m, with a coarse step of 0.025 s so that each step can
be seen. Bottom: the four parts of a step, lit in turn (find contacts, forces to acceleration, new velocity, new
position). Top: the height of the box's bottom against time: the exact fall (grey), semi-implicit Euler (blue,
position from the new velocity, as MuJoCo) and explicit Euler (purple, position from the old velocity). Step 6
takes the blue box 0.029 m into the floor. Run -> step_anim.gif, step_anim_frames.png"""
import numpy as np
import plotly.graph_objects as go
import simkit as s
from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE, make_gif
from plotly.subplots import make_subplots

DT, NSTEP = 0.025, 6
SEMI = s.free_fall(DT, NSTEP, "semi")
EXPL = s.free_fall(DT, NSTEP, "explicit")
assert [round(v, 5) for v in SEMI[:2, 1]] == [0.1, 0.09387] and round(EXPL[1, 1], 5) == 0.1
assert round(SEMI[6, 1], 3) == -0.029 and round(SEMI[1, 2], 3) == -0.245
tt = np.linspace(0, s.reference()["t_land"], 200)              # the exact fall ends on the floor
PARTS = ["1  find contacts", "2  forces → acceleration", "3  new velocity", "4  new position"]


def texts(n):
    """The values of step n (1-based) for each part."""
    z0, v0 = SEMI[n - 1, 1], SEMI[n - 1, 2]
    v1, z1 = SEMI[n, 2], SEMI[n, 1]
    return [f"bottom at {z0:.4f} m: above the floor, no contact",
            "gravity only: a = −9.81 m/s²",
            f"v = {v0:.3f} + (−9.81)(0.025) = {v1:.3f} m/s",
            f"z = {z0:.4f} + ({v1:.3f})(0.025) = {z1:.4f} m"]


def frame(n, part):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.6, 0.4], vertical_spacing=0.08)
    fig.add_hrect(y0=-0.04, y1=0, fillcolor="rgba(150,150,150,0.25)", line_width=0, row=1, col=1)
    fig.add_trace(go.Scatter(x=tt, y=s.H0 - 0.5 * s.G * tt ** 2, mode="lines", line=dict(color=GREY, width=3)),
                  row=1, col=1)
    done = n if part == 3 else n - 1
    fig.add_trace(go.Scatter(x=SEMI[:done + 1, 0], y=SEMI[:done + 1, 1], mode="lines+markers",
                             line=dict(color=BLUE, width=2.5), marker=dict(size=10, color=BLUE)), row=1, col=1)
    fig.add_trace(go.Scatter(x=EXPL[:done + 1, 0], y=EXPL[:done + 1, 1], mode="lines+markers",
                             line=dict(color=PURPLE, width=2.5, dash="dot"), marker=dict(size=9, color=PURPLE,
                                                                                       symbol="square")),
                  row=1, col=1)
    lab = [("exact fall", GREY, 0.115, 0.075), ("semi-implicit Euler (MuJoCo)", BLUE, 0.01, -0.015),
           ("explicit Euler", PURPLE, 0.01, -0.03)]
    for txt, col, x, y in lab:
        fig.add_annotation(x=x, y=y, xref="x", yref="y", text=txt, showarrow=False, xanchor="left",
                           font=dict(size=17, color=col))
    fig.add_annotation(x=0.148, y=-0.033, xref="x", yref="y", text="inside the floor", showarrow=False,
                       xanchor="right", font=dict(size=15, color=GREY))
    for i, name in enumerate(PARTS):
        y0 = 3 - i
        on = i == part
        fig.add_shape(type="rect", x0=0, x1=10, y0=y0, y1=y0 + 0.85, xref="x2", yref="y2",
                      line=dict(color=ORANGE if on else "#BBBBBB", width=3 if on else 1.5),
                      fillcolor="rgba(245,133,24,0.18)" if on else "rgba(0,0,0,0)")
        fig.add_annotation(x=0.2, y=y0 + 0.6, xref="x2", yref="y2", text=f"<b>{name}</b>", showarrow=False,
                           xanchor="left", font=dict(size=18, color="black" if on else GREY))
        if i <= part:
            fig.add_annotation(x=0.2, y=y0 + 0.25, xref="x2", yref="y2", text=texts(n)[i], showarrow=False,
                               xanchor="left", font=dict(size=17, color=ORANGE if on else BLUE))
    fig.add_annotation(x=5, y=4.15, xref="x2", yref="y2", text=f"<b>step {n} of the time step Δt = 0.025 s</b>",
                       showarrow=False, font=dict(size=19))
    fig.update_xaxes(title_text="time (s)", range=[-0.005, 0.16], row=1, col=1, showgrid=False)
    fig.update_yaxes(title_text="height of the bottom (m)", range=[-0.04, 0.11], row=1, col=1, showgrid=False)
    fig.update_xaxes(range=[-0.1, 10.1], visible=False, row=2, col=1)
    fig.update_yaxes(range=[-0.1, 4.4], visible=False, row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=820, height=1150, showlegend=False,
                      margin=dict(l=90, r=20, t=20, b=20))
    return fig


figs, holds, keys = [], [], []
for n in range(1, NSTEP + 1):
    for p in range(4):
        figs.append(frame(n, p))
        holds.append(4 if n == 1 else 2)
holds[-1] = 14
make_gif(figs, "step_anim", fps=3, holds=holds, keys=[3, 7, len(figs) - 1], cols=3)
