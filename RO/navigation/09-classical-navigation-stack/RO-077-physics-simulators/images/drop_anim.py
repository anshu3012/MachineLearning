"""The running example at three time steps, one frame per 0.02 s of simulated time, all three drawn at the same
scale: a 1 kg box (0.2 m cube, seen from the side) falls from 0.1 m with a sideways speed of 2.0 m/s onto the soft
floor (friction coefficient 0.4) and slides. Top, 0.002 s (MuJoCo's default step): stable, stops at 0.549 m after
0.51 s, against the exact 0.550 m. Middle, 0.015 s: jittery, bounces 0.088 m off the floor before settling. Bottom,
0.03 s: unstable, thrown 1.36 m into the air (an arrow shows it above the frame). Grey dashes: where the exact
answer stops. Run -> drop_anim.gif, drop_anim_frames.png"""
import numpy as np
import plotly.graph_objects as go
import simkit as s
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from plotly.subplots import make_subplots

REF = s.reference()
RUNS = [s.simulate(dt, T=1.0) for dt in s.DTS]
assert round(RUNS[0][-1, 1], 3) == 0.549 and round(REF["x_stop"], 3) == 0.550
z1 = RUNS[1][:, 2]
assert round(z1[RUNS[1][:, 0] > REF["t_land"] + 0.05].max(), 3) == 0.088
assert round(RUNS[2][:, 2].max(), 2) == 1.36
NAMES = [("Δt = 0.002 s (MuJoCo's default): stable", BLUE), ("Δt = 0.015 s: jittery", ORANGE),
         ("Δt = 0.03 s: unstable", RED)]
ZTOP = 0.5


def state(r, t):
    k = int(np.searchsorted(r[:, 0], t + 1e-9, side="right") - 1)
    return k, r[k]


def frame(t):
    fig = make_subplots(rows=3, cols=1, vertical_spacing=0.06)
    for i, (r, (name, col)) in enumerate(zip(RUNS, NAMES)):
        row = i + 1
        fig.add_hrect(y0=-0.06, y1=0, fillcolor="rgba(150,150,150,0.3)", line_width=0, row=row, col=1)
        fig.add_trace(go.Scatter(x=[REF["x_stop"]] * 2, y=[-0.06, ZTOP - 0.1], mode="lines",
                                 line=dict(color=GREY, dash="dash", width=2)), row=row, col=1)
        k, (tt, x, z, vx, vz, N, f, d) = state(r, t)
        tr = r[:k + 1]
        fig.add_trace(go.Scatter(x=tr[:, 1], y=np.minimum(tr[:, 2], ZTOP), mode="lines",
                                 line=dict(color=col, width=2)), row=row, col=1)
        zb = min(z, ZTOP + 0.3)
        fig.add_shape(type="rect", x0=x - s.SIZE / 2, x1=x + s.SIZE / 2, y0=zb, y1=zb + s.SIZE,
                      line=dict(color=col, width=4), fillcolor="rgba(0,0,0,0)", layer="above", opacity=1, row=row, col=1)
        if z > ZTOP - s.SIZE:
            fig.add_annotation(x=x + 0.03, y=ZTOP - 0.12, xref=f"x{row}", yref=f"y{row}", text=f"box at {z:.2f} m ↑",
                               showarrow=False, xanchor="left", font=dict(size=18, color=col),
                               bgcolor="rgba(255,255,255,0.9)")
        fig.add_annotation(x=0.0, y=ZTOP + 0.03, xref=f"x{row}", yref=f"y{row}", text=f"<b>{name}</b>",
                           showarrow=False, xanchor="left", yanchor="top", font=dict(size=18, color=col))
        fig.add_annotation(x=0.98, y=ZTOP + 0.03, xref=f"x{row}", yref=f"y{row}",
                           text=f"x = {x:.3f} m<br>height {z * 1000:.0f} mm", showarrow=False, xanchor="right",
                           yanchor="top", align="right", font=dict(size=17))
        fig.update_xaxes(range=[-0.12, 1.0], row=row, col=1, showgrid=False,
                         title_text="along the floor (m)" if row == 3 else None)
        fig.update_yaxes(range=[-0.06, ZTOP + 0.05], row=row, col=1, showgrid=False, scaleanchor=f"x{row}")
    fig.add_annotation(x=REF["x_stop"], y=-0.05, xref="x3", yref="y3", text="exact stop", showarrow=False,
                       yanchor="bottom", xanchor="left", font=dict(size=15, color=GREY))
    fig.add_annotation(x=0.5, y=1.0, xref="paper", yref="paper", text=f"<b>t = {t:.2f} s</b>", showarrow=False,
                       yanchor="bottom", font=dict(size=20))
    fig.update_layout(template="simple_white", font=FONT, width=820, height=1300, showlegend=False,
                      margin=dict(l=60, r=20, t=40, b=60))
    return fig


ts = [round(v, 2) for v in np.arange(0, 1.0 + 1e-9, 0.02)]
figs = [frame(t) for t in ts]
holds = [5] + [1] * (len(ts) - 2) + [16]
make_gif(figs, "drop_anim", fps=8, holds=holds, keys=[ts.index(0.16), ts.index(0.3), ts.index(0.68),
                                                      len(ts) - 1], cols=2)
