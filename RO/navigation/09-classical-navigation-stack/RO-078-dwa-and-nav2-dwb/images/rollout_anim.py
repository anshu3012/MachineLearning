"""Two rollouts of the person's cycle (t = 2.4 s), one step per frame. First, keep going: (0.568 m/s, 0.263 rad/s),
20 steps of 0.085 s; the obstacle critic checks pose by pose and rejects it at the first pose inside the dotted
band of the person. Then the chosen pair, brake: (0.158 m/s, 0.263 rad/s), 18 steps of 0.0944 s; its speed falls
by 0.5 m/s^2 from 0.568 m/s and reaches 0.158 m/s after 9 steps (0.85 s). Top: the poses in the room. Bottom: the
speed of each step against time. Our Python version of DWB's rollout. Run -> rollout_anim.gif,
rollout_anim_frames.png"""
import math

import dwbkit as d
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from plotly.subplots import make_subplots

R = d.results()
o = [c for c in R["replan"]["cycles"] if abs(c["t"] - d.T_PERSON) < 1e-9][0]
rec = o["rec"]
x, v0, w0 = o["x"], o["v"], o["w"]
pairs = [tuple(p) for p in rec["pairs"]]
i_keep = [i for i, p in enumerate(pairs) if abs(p[0] - v0) < 1e-9 and abs(p[1] - w0) < 1e-9][0]
i_best = pairs.index(tuple(rec["cmd"]))
cm = o["cm"]


def info(i):
    cmd = pairs[i]
    n, dt = d.time_steps(*cmd)
    T = rec["trajs"][i]
    vv = np.where(cmd[0] < v0, np.maximum(cmd[0], v0 - 0.5 * dt * np.arange(1, n + 1)),
                  np.minimum(cmd[0], v0 + 0.5 * dt * np.arange(1, n + 1)))
    ii, jj, _ = cm.world_to_map(T[:, 0], T[:, 1])
    c = cm.cost[jj, ii]
    bad = np.where(c >= d.INSCRIBED)[0]
    return dict(cmd=cmd, n=n, dt=dt, T=T, vv=vv, first_bad=int(bad[0]) if len(bad) else None)


K, B = info(i_keep), info(i_best)
print("keep going: steps", K["n"], "dt", K["dt"], "first pose in a band", K["first_bad"])
assert K["n"] == 20 and round(K["dt"], 3) == 0.085 and K["first_bad"] is not None
assert B["n"] == 18 and round(B["dt"], 4) == 0.0944 and B["first_bad"] is None
assert int(np.argmax(np.isclose(B["vv"], B["cmd"][0]))) + 1 == 9
TT = np.linspace(0, 2 * math.pi, 80)


def frame(stage, k):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.64, 0.36], vertical_spacing=0.08)
    rd.room(fig, rc=(1, 1))
    rd.person(fig, d.PERSON, d.PERSON_R, rc=(1, 1))
    fig.add_trace(go.Scatter(x=d.PERSON[0] + 0.45 * np.cos(TT), y=d.PERSON[1] + 0.45 * np.sin(TT), mode="lines",
                             line=dict(color="#C2185B", width=1.5, dash="dot")), row=1, col=1)
    rd.robot(fig, x[0], x[1], x[2], BLUE, rc=(1, 1), fill="rgba(0,0,0,0)")
    lines = []
    for name, I, col, kk in (("keep going", K, RED, k if stage == 0 else K["first_bad"]),
                             ("brake", B, ORANGE, k if stage == 1 else -1)):
        if kk < 0:
            continue
        T = I["T"][:kk + 1]
        hit = I["first_bad"] is not None and kk >= I["first_bad"]
        fig.add_trace(go.Scatter(x=T[:, 0], y=T[:, 1], mode="lines+markers", line=dict(color=col, width=2.5),
                                 marker=dict(size=7, color=col)), row=1, col=1)
        if hit:
            fig.add_trace(go.Scatter(x=[T[-1, 0]], y=[T[-1, 1]], mode="markers",
                                     marker=dict(size=20, color=RED, symbol="x")), row=1, col=1)
        t = np.arange(0, kk + 1) * I["dt"]                # the speed held during each step, as the rollout uses it
        y = np.r_[I["vv"][:kk], I["vv"][kk - 1]] if kk > 0 else np.array([v0])
        fig.add_trace(go.Scatter(x=t, y=y, mode="lines+markers",
                                 line=dict(color=col, width=3, shape="hv"), marker=dict(size=6, color=col)),
                      row=2, col=1)
        msg = (f"{name} ({I['cmd'][0]:.3f} m/s, {I['cmd'][1]:.3f} rad/s): step {kk} of {I['n']}, "
               f"{I['dt']:.3f} s each")
        if hit:
            msg = (f"<b>{name}</b>: pose {kk} is in the person's band:<br>illegal, the critic stops checking")
        lines.append(f"<span style='color:{col}'>{msg}</span>")
    if stage == 1 and k == B["n"]:
        lines.append(f"<span style='color:{ORANGE}'><b>brake: all 19 poses clear</b></span>")
    fig.add_annotation(x=1.88, y=3.43, xref="x", yref="y", text="<br>".join(lines), showarrow=False,
                       xanchor="left", yanchor="top", align="left", font=dict(size=18),
                       bgcolor="rgba(255,255,255,0.9)")
    fig.add_hline(y=v0, line=dict(color=GREY, dash="dot", width=1.5), row=2, col=1)
    fig.add_annotation(x=1.65, y=v0, xref="x2", yref="y2", text="speed now 0.568", showarrow=False,
                       yanchor="bottom", xanchor="right", font=dict(size=16, color=GREY))
    rd.zoom(fig, (1.85, 3.65), (1.35, 3.45), rc=(1, 1))
    fig.update_xaxes(title_text="time ahead (s)", range=[-0.02, 1.75], row=2, col=1, showgrid=False)
    fig.update_yaxes(title_text="speed (m/s)", range=[0, 0.65], row=2, col=1, showgrid=False)
    fig.update_layout(template="simple_white", font=FONT, width=800, height=1250, showlegend=False,
                      margin=dict(l=90, r=20, t=10, b=70))
    return fig


figs = [frame(0, k) for k in range(K["first_bad"] + 1)] + [frame(1, k) for k in range(B["n"] + 1)]
holds = [3] + [1] * (K["first_bad"] - 1) + [8] + [2] + [1] * (B["n"] - 1) + [14]
make_gif(figs, "rollout_anim", fps=4, holds=holds, keys=[K["first_bad"] // 2, K["first_bad"],
                                                        K["first_bad"] + 1 + 9, len(figs) - 1], cols=2)
