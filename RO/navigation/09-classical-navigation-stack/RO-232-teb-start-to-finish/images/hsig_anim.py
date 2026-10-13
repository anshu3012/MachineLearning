"""How TEB tells two bands apart (the H-signature), with the person 0.25 m further left, in the cycle at 2.5 s. Two of
its optimised candidate bands: orange passes the person on the left, purple on the right. A dot runs along each band;
a line joins it to the person's centre. The text adds up the angle each line has turned through so far (anticlockwise
positive) and the H-signature of the band so far for the person's centre, the code's number (HSignature3d, divided
by 4 pi): its sign is the side. The last frame holds the whole bands. Run -> hsig_anim.gif, hsig_anim_frames.png"""
import math
from pathlib import Path

import bandkit as bk
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
import tebkit as tk
from gifkit import FONT, ORANGE, PURPLE, make_gif

here = Path(__file__).parent
c = tk.results()["left"][25]
pl = c["planner"]
C0 = bk.PERSON_LEFT
bands = [pl["candidates"][0], pl["candidates"][2]]           # left (picked), right (new from the roadmap)
assert round(c["t"], 1) == 2.5 and pl["best"] == 0


def sweep(P):
    a = np.arctan2(P[:, 1] - C0[1], P[:, 0] - C0[0])
    return np.concatenate([[0], np.cumsum(tk.wrap(np.diff(a)))])


SW = [sweep(b.P) for b in bands]
H = [[0.0] + [float(tk.h_signature(b.P[:k + 1], b.DT[:k], C0[None])[0]) for k in range(1, len(b.P))] for b in bands]
final = [(math.degrees(s[-1]), h[-1]) for s, h in zip(SW, H)]
assert final[0][1] < 0 < final[1][1]
N = 24


def frame(f):
    fig = go.Figure()
    rd.room(fig)
    rd.person(fig, C0, bk.PERSON_R)
    lines = [f"<b>t = 2.5 s</b>, person at ({C0[0]:.2f}, {C0[1]:.2f})"]
    for b, s, h, col, name in zip(bands, SW, H, (ORANGE, PURPLE), ("left band", "right band")):
        rd.band(fig, b.P, col, size=6, width=2, ticks=False)
        k = min(int(round(f / N * (len(b.P) - 1))), len(b.P) - 1)
        p = b.P[k]
        fig.add_trace(go.Scatter(x=[C0[0], p[0]], y=[C0[1], p[1]], mode="lines", line=dict(color=col, width=2, dash="dot")))
        fig.add_trace(go.Scatter(x=[p[0]], y=[p[1]], mode="markers", marker=dict(size=16, color=col)))
        lines.append(f"<span style='color:{col}'>{name}: turned {math.degrees(s[k]):+.0f}°, H {h[k]:+.3f}</span>")
    g = c["goal"]
    fig.add_trace(go.Scatter(x=[g[0]], y=[g[1]], mode="markers", marker=dict(symbol="x", size=16, color="#333333")))
    if f == N:
        lines.append("person on the band's left: H > 0; on its right: H < 0")
    fig.add_annotation(x=1.4, y=3.9, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                       align="left", font=dict(size=19), bgcolor="rgba(255,255,255,0.92)")
    rd.zoom(fig, (1.35, 4.0), (1.45, 4.0))
    fig.update_layout(template="simple_white", font=FONT, width=800, height=780, showlegend=False,
                      margin=dict(l=10, r=10, t=10, b=10))
    return fig


figs = [frame(f) for f in range(N + 1)]
make_gif(figs, here / "hsig_anim", fps=4, holds=[4] + [1] * (N - 1) + [14], keys=[0, N // 3, 2 * N // 3, N], cols=2,
         width=600)
print("left band: turned %.1f deg, H %.4f; right band: turned %.1f deg, H %.4f" % (*final[0], *final[1]))
