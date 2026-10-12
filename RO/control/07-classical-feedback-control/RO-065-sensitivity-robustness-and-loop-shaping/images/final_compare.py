"""Our first-try PD (Kp 0.4, Kd 0.08, blue), RO-060's tuned PD (Kp 0.2, Kd 0.283, orange) and the lead-lag (green)
compared in the frequency domain. Top: |S| in dB; peaks 2.55, 1.00 and 1.35. Middle: the noise gain |CS| from heading
noise to motor torque; at 100 rad/s 8.0, 28.3 and 1.87, because the lead's pole stops the controller's gain rising.
Bottom: the real robot's model error |delta| (grey, dotted) against the bound 1/|T| of each loop; the bounds of RO-060's
tuned PD and of the lead-lag stay above it at every frequency, so their stability is guaranteed. Run: python final_compare.py ->
final_compare.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE
from loopkit import I, KP, C_leadlag, C_pd, db
from shapekit import I_PAY, TAU_REAL, gang_of_four

here = Path(__file__).parent
w = np.logspace(-1, np.log10(300), 2000)
TUNED = "RO-060's tuned PD, Kp 0.2, Kd 0.283"
loops = [("our PD, Kp 0.4, Kd 0.08", lambda s: C_pd(s), BLUE), (TUNED, lambda s: C_pd(s, 0.2, 0.283), ORANGE),
         ("lead-lag", C_leadlag, GREEN)]
g = {name: gang_of_four(C, w) for name, C, _ in loops}
delta = np.abs((I / I_PAY) * np.exp(-1j * w * TAU_REAL) - 1)
at100 = {name: abs(gang_of_four(C, np.array([100.0]))["CS"][0]) for name, C, _ in loops}
assert abs(at100["our PD, Kp 0.4, Kd 0.08"] - 8.0) < 0.05 and abs(at100[TUNED] - 28.3) < 0.05
assert abs(at100["lead-lag"] - 1.87) < 0.01 and np.abs(g[TUNED]["S"]).max() <= 1.0
assert np.all(delta < 1 / np.abs(g["lead-lag"]["T"])) and np.all(delta < 1 / np.abs(g[TUNED]["T"]))
assert np.any(delta > 1 / np.abs(g["our PD, Kp 0.4, Kd 0.08"]["T"]))

fig = make_subplots(rows=3, cols=1, vertical_spacing=0.1, subplot_titles=(
    "sensitivity |S|: disturbances", "noise gain |CS|: heading noise → motor torque",
    "model error |δ| against the bound 1/|T|"))
for a in fig.layout.annotations:
    a.font = dict(size=20)
for name, _, col in loops:
    fig.add_trace(go.Scatter(x=w, y=db(g[name]["S"]), line=dict(color=col, width=4), name=name), 1, 1)
    fig.add_trace(go.Scatter(x=w, y=np.abs(g[name]["CS"]), line=dict(color=col, width=4), showlegend=False), 2, 1)
    fig.add_trace(go.Scatter(x=w, y=1 / np.abs(g[name]["T"]), line=dict(color=col, width=4, dash="dash"),
                             showlegend=False), 3, 1)
    fig.add_trace(go.Scatter(x=[100], y=[at100[name]], mode="markers+text", marker=dict(color=col, size=11),
                             text=[f"{at100[name]:.1f}" if at100[name] > 5 else f"{at100[name]:.2f}"],
                             textposition="top left", textfont=dict(size=18, color=col), showlegend=False), 2, 1)
fig.add_trace(go.Scatter(x=w, y=delta, line=dict(color=GREY, width=4, dash="dot"), name="|δ|: the real robot's model error"),
              3, 1)
fig.add_hline(y=0, line=dict(color=GREY, width=1.5, dash="dash"), row=1, col=1)
for r in (1, 2):
    fig.update_xaxes(type="log", range=[-1, np.log10(300)], title_text="ω (rad/s)", row=r, col=1)
fig.update_xaxes(type="log", range=[-1, 1], title_text="ω (rad/s)", tickvals=[0.1, 0.2, 0.5, 1, 2, 5, 10], row=3, col=1)
fig.update_yaxes(title_text="|S| (dB)", range=[-40, 12], row=1, col=1)
fig.update_yaxes(type="log", title_text="N·m per rad", range=[-2, 2], row=2, col=1)
fig.update_yaxes(title_text="relative size", range=[0, 2.5], row=3, col=1)
fig.update_layout(template="simple_white", font=FONT, width=1000, height=1450, margin=dict(l=100, r=30, t=230, b=70),
                  legend=dict(x=0.0, y=1.035, yanchor="bottom", font=dict(size=18)),
                  title=dict(x=0.5, y=0.985, text="first-try PD, tuned PD, or lead-lag"))
fig.write_image(here / "final_compare.png", scale=1)
