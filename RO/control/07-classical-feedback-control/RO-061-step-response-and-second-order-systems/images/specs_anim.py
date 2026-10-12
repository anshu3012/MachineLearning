"""The four numbers of a step response, read off one at a time. Left: the speed under P control (Kv = 6 N per m/s)
after the command steps from 0 to 0.5 m/s. Right: the heading under PD control (Kp = 0.4, Kd = 0.08) after the command
steps from 0 to 0.5 rad. First both curves are drawn over time; then each stage marks one number on both:
rise time (10 to 90 percent of the final value), overshoot, settling time (2 percent band), steady-state error.
Run: python specs_anim.py -> specs_anim.gif, specs_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE, RED, make_gif
from stepkit import KD_OLD, TH_REF, V_REF, heading_pd, speed_p, step_info

here = Path(__file__).parent
ts, th_t = np.linspace(0, 8, 8001), np.linspace(0, 12, 12001)
v = speed_p(ts)
th, _, _ = heading_pd(th_t, kd=KD_OLD)
S = step_info(ts, v, 0.375, V_REF)
H = step_info(th_t, th, TH_REF, TH_REF)
assert abs(S["rise"] - 2.20) < 5e-3 and abs(S["settle"] - 3.91) < 5e-3 and abs(S["sse"] - 0.125) < 1e-9
assert abs(H["rise"] - 0.60) < 5e-3 and abs(H["overshoot"] - 0.527) < 5e-4 and abs(H["settle"] - 9.80) < 5e-3
STAGES = ["1. rise time: 10 % to 90 % of the final value", "2. overshoot: how far past the final value",
          "3. settling time: stays inside the 2 % band", "4. steady-state error: command minus final value"]


def seg(fig, x, y, col, color, width=3, dash=None):
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color=color, width=width, dash=dash)), 1, col)


def text(fig, x, y, s, col, color, xa="left", ya="middle"):
    fig.add_annotation(x=x, y=y, text=s, showarrow=False, xanchor=xa, yanchor=ya, font=dict(color=color, size=19),
                       bgcolor="rgba(255,255,255,0.85)", row=1, col=col)


def frame(frac, stage):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.11,
                        subplot_titles=["speed step 0 → 0.5 m/s (P, Kv = 6)",
                                        "heading step 0 → 0.5 rad (PD, Kp = 0.4, Kd = 0.08)"])
    ks, kh = int(frac * (len(ts) - 1)), int(frac * (len(th_t) - 1))
    if stage >= 3:   # the 2 percent bands go under the curves
        for col, f, xmax in ((1, 0.375, 8), (2, TH_REF, 12)):
            fig.add_trace(go.Scatter(x=[0, xmax, xmax, 0, 0], y=[0.98 * f, 0.98 * f, 1.02 * f, 1.02 * f, 0.98 * f],
                                     fill="toself", mode="lines", line=dict(width=0),
                                     fillcolor="rgba(84,162,75,0.3)"), 1, col)
    seg(fig, [0, 8], [V_REF, V_REF], 1, GREY, 2, "dash")
    seg(fig, [0, 12], [TH_REF, TH_REF], 2, GREY, 2, "dash")
    text(fig, 0.15, V_REF, "command 0.5", 1, GREY, ya="bottom")
    fig.add_trace(go.Scatter(x=ts[:ks + 1], y=v[:ks + 1], mode="lines", line=dict(color=BLUE, width=4)), 1, 1)
    fig.add_trace(go.Scatter(x=th_t[:kh + 1], y=th[:kh + 1], mode="lines", line=dict(color=BLUE, width=4)), 1, 2)
    if stage >= 1:
        for col, I_, f in ((1, S, 0.375), (2, H, TH_REF)):
            for lv, tt in ((0.1 * f, I_["t10"]), (0.9 * f, I_["t90"])):
                seg(fig, [0, tt], [lv, lv], col, ORANGE, 2, "dot")
                seg(fig, [tt, tt], [0, lv], col, ORANGE, 2, "dot")
            seg(fig, [I_["t10"], I_["t90"]], [0.02, 0.02] if col == 1 else [0.03, 0.03], col, ORANGE, 5)
        text(fig, S["t90"] + 0.15, 0.03, "rise 2.20 s", 1, ORANGE)
        text(fig, H["t90"] + 0.2, 0.04, "rise 0.60 s", 2, ORANGE)
    if stage >= 2:
        text(fig, 7.9, 0.2, "overshoot 0 %:<br>never passes 0.375", 1, RED, xa="right")
        seg(fig, [H["t_peak"], H["t_peak"]], [TH_REF, H["peak"]], 2, RED, 5)
        fig.add_annotation(x=H["t_peak"], y=H["peak"], text="overshoot 52.7 %:<br>peak 0.763 rad", ax=70, ay=-6,
                           xanchor="left", arrowcolor=RED, font=dict(color=RED, size=19), row=1, col=2)
    if stage >= 3:
        seg(fig, [S["settle"]] * 2, [0, 0.6], 1, GREEN, 3, "dot")
        seg(fig, [H["settle"]] * 2, [0, 0.85], 2, GREEN, 3, "dot")
        text(fig, S["settle"] + 0.12, 0.27, "settled<br>3.91 s", 1, GREEN)
        text(fig, H["settle"] - 0.15, 0.25, "settled<br>9.80 s", 2, GREEN, xa="right")
    if stage >= 4:
        seg(fig, [6.5, 6.5], [0.375, V_REF], 1, PURPLE, 5)
        text(fig, 6.4, 0.44, "error<br>0.125 m/s", 1, PURPLE, xa="right")
        text(fig, 11.8, 0.585, "error 0", 2, PURPLE, xa="right")
    fig.update_xaxes(title="time t (s)")
    fig.update_xaxes(range=[0, 8], row=1, col=1)
    fig.update_xaxes(range=[0, 12], row=1, col=2)
    fig.update_yaxes(title="speed v (m/s)", range=[0, 0.6], row=1, col=1)
    fig.update_yaxes(title="heading θ (rad)", range=[0, 0.85], row=1, col=2)
    title = STAGES[stage - 1] if stage else f"both commands step at t = 0: the responses ({frac * 100:.0f} % drawn)"
    fig.update_layout(template="simple_white", font=FONT, width=1250, height=620, showlegend=False,
                      margin=dict(l=80, r=30, t=130, b=70), title=dict(x=0.5, y=0.95, text=title))
    fig.update_annotations(selector=dict(showarrow=False, xref="paper"), font_size=20)
    return fig


fr = np.linspace(0, 1, 21)
figs = [frame(f, 0) for f in fr] + [frame(1, s) for s in (1, 2, 3, 4)]
make_gif(figs, here / "specs_anim", fps=6, holds=[6] + [1] * 19 + [6, 14, 14, 14, 30],
         keys=[10, 21, 22, 24], cols=2, width=950)
