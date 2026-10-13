"""Map-consistent sampling, played; the scene and the seeded samples of map_reject.py. Left: one big step of 0.48 m.
The 500 samples fly out from the start along their noisy drive; only where they end is checked: 95 end inside the wall
(8 cm thick, y from 1.45 to 1.53 m) and are rejected (red), 14 end beyond it in free space and are kept (purple),
though no robot can drive through a wall. Right: the same motion in twenty small steps of about 2.4 cm, the noise per
step raised so the final spread matches; after every step, samples that land in the wall flash red and are redrawn
from their last pose. None gets beyond the wall.
Run: python map_reject_anim.py -> map_reject_anim.gif, map_reject_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, PURPLE, RED, make_gif
from map_reject import WALL, beyond, big_step, inside, small_steps
from motion import A_ODO, START, sample_odometry
from plotly.subplots import make_subplots

here = Path(__file__).parent
X0, Y0, _ = START
BX, BY, _ = big_step(np.random.default_rng(5))
IN, OUT = inside(BX, BY), beyond(BX, BY)
OK = ~IN & ~OUT
assert IN.sum() == 95 and OUT.sum() == 14 and len(BX) == 500


def small_steps_history(rng, n=500, k=20):
    """map_reject.small_steps, keeping the cloud after each sub-step and the positions rejected at each sub-step."""
    x, y, th = (np.full(n, v) for v in START)
    u = (0.5 / k, 0.479 / k, 0.5 / k)
    a = tuple(np.sqrt(k) * v for v in A_ODO)
    clouds, rejected = [], []
    for _ in range(k):
        nx, ny, nth = sample_odometry(u, (x, y, th), rng, n, a)
        bad = inside(nx, ny)
        rej = [(nx[bad].copy(), ny[bad].copy())]
        while bad.any():
            rx, ry, rth = sample_odometry(u, (x[bad], y[bad], th[bad]), rng, bad.sum(), a)
            nx[bad], ny[bad], nth[bad] = rx, ry, rth
            bad = inside(nx, ny)
            rej.append((nx[bad].copy(), ny[bad].copy()))
        x, y, th = nx, ny, nth
        clouds.append((x.copy(), y.copy()))
        rejected.append((np.concatenate([r[0] for r in rej]), np.concatenate([r[1] for r in rej])))
    return clouds, rejected


CLOUDS, REJ = small_steps_history(np.random.default_rng(5))
SX, SY, _ = small_steps(np.random.default_rng(5))
assert np.allclose(CLOUDS[-1][0], SX) and np.allclose(CLOUDS[-1][1], SY)      # the same run as map_reject.small_steps
assert beyond(SX, SY).sum() == 0 and round(0.479 / 20 * 100, 1) == 2.4
assert round((WALL[3] - WALL[2]) * 100) == 8
LEGEND = "blue: kept   red: inside the wall, rejected   purple: free but unreachable"


def frame(head, left, right, titles=("one big step", "twenty small steps")):
    """left: ('fly', f) samples a fraction f of the way out, or ('checked', flash);
    right: None, or (j, show_rejected) the cloud after sub-step j."""
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08, subplot_titles=titles)
    for c in (1, 2):
        fig.add_shape(type="rect", x0=WALL[0], x1=WALL[1], y0=WALL[2], y1=WALL[3], fillcolor="#8c8c8c", line_width=0, layer="below",
                      opacity=1, row=1, col=c)
        fig.add_annotation(x=2.6, y=1.49, text="wall", showarrow=False, font=dict(size=18, color="white"), row=1,
                           col=c)
        fig.add_trace(go.Scatter(x=[X0], y=[Y0], mode="markers", marker=dict(size=12, color="black")), 1, c)
        fig.update_xaxes(range=[1.7, 2.8], dtick=0.2, title="x (m)", row=1, col=c)
        fig.update_yaxes(range=[0.95, 1.7], dtick=0.1, row=1, col=c)
    kind, v = left
    if kind == "fly":
        if v > 0:
            fig.add_trace(go.Scatter(x=X0 + v * (BX - X0), y=Y0 + v * (BY - Y0), mode="markers",
                                     marker=dict(size=4, color=BLUE, opacity=0.6)), 1, 1)
    else:
        fig.add_trace(go.Scatter(x=BX[OK], y=BY[OK], mode="markers", marker=dict(size=4, color=BLUE, opacity=0.6)),
                      1, 1)
        fig.add_trace(go.Scatter(x=BX[IN], y=BY[IN], mode="markers",
                                 marker=dict(size=12 if v else 7, color=RED, symbol="x")), 1, 1)
        fig.add_trace(go.Scatter(x=BX[OUT], y=BY[OUT], mode="markers",
                                 marker=dict(size=6, color=PURPLE if not v else BLUE, opacity=1 if not v else 0.6)),
                      1, 1)
    if right is not None:
        j, show = right
        fig.add_trace(go.Scatter(x=CLOUDS[j - 1][0], y=CLOUDS[j - 1][1], mode="markers",
                                 marker=dict(size=4, color=BLUE, opacity=0.6)), 1, 2)
        if show and len(REJ[j - 1][0]):
            fig.add_trace(go.Scatter(x=REJ[j - 1][0], y=REJ[j - 1][1], mode="markers",
                                     marker=dict(size=10, color=RED, symbol="x")), 1, 2)
    fig.update_yaxes(title="y (m)", row=1, col=1)
    fig.update_layout(template="simple_white", width=1100, height=620, font=FONT, showlegend=False,
                      margin=dict(l=80, r=30, t=150, b=70),
                      title=dict(x=0.5, y=0.96, font=dict(size=22),
                                 text=f"{head}<br><span style='font-size:19px;color:{GREY}'>{LEGEND}</span>"))
    fig.update_annotations(selector=dict(text="wall"), font_size=18)
    fig.update_annotations(selector=dict(yref="paper"), font_size=19)
    return fig


T_DONE = (f"one big step: {IN.sum()} rejected, {OUT.sum()} beyond the wall", "twenty small steps")
figs, holds = [], []
add = lambda f, h: (figs.append(f), holds.append(h))
add(frame("a wall 8 cm thick lies across the cloud of our 0.48 m step", ("fly", 0), None), 8)
for f in (0.25, 0.5, 0.75, 1.0):
    add(frame("one big step: 500 samples, each checked only where it ends", ("fly", f), None), 2 if f < 1 else 4)
add(frame(f"{IN.sum()} samples end inside the wall: rejected", ("checked", True), None), 6)
add(frame(f"{OUT.sum()} end beyond the wall, in free space: kept, though no robot drives through a wall",
          ("checked", False), None, T_DONE), 12)
key = [len(figs) - 1]
for j in range(1, 21):
    n = len(REJ[j - 1][0])
    head = f"twenty small steps of 2.4 cm: step {j}, {n} draws landed in the wall and were drawn again"
    add(frame(head, ("checked", False), (j, True), T_DONE), 3 if n else 1)
add(frame("a small step cannot cross the wall: no sample gets beyond it", ("checked", False), (20, False),
          (T_DONE[0], f"twenty small steps: {beyond(SX, SY).sum()} beyond the wall")), 24)
key.append(len(figs) - 1)
make_gif(figs, here / "map_reject_anim", fps=4, holds=holds, keys=key, cols=2, width=950)
print("rejections per small step:", [len(r[0]) for r in REJ])
