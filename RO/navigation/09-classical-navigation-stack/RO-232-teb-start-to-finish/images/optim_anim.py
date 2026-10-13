"""Steps 4 to 6 on numbers, with the person 0.25 m further left, in the cycle at 2.5 s: the three candidate bands,
one per homotopy class, optimised side by side, one solver step per frame. Orange: last cycle's band (left of the
person); purple: the band built from the global plan (right); green: the band from the roadmap's new path (right).
Each of the 4 passes first resizes the bands, then takes 5 Levenberg-Marquardt steps; the obstacle weight starts at
50 and doubles after each pass. The text gives each band's cost with the set weights. The last frame gives the
selection costs (obstacle terms x 100; the plan's band x 0.95) and the band TEB picks.
Run -> optim_anim.gif, optim_anim_frames.png"""
from pathlib import Path

import bandkit as bk
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
import tebkit as tk
from gifkit import FONT, GREEN, ORANGE, PURPLE, make_gif

here = Path(__file__).parent
c = tk.results()["left"][25]
pl = c["planner"]
ob = c["obst"]
COL = (ORANGE, PURPLE, GREEN)
NAME = ("last cycle's band", "band from the plan", "band from the roadmap")
assert pl["best"] == 0 and pl["init_idx"] == 1 and len(pl["hist"]) == 3 and all(len(h) == 24 for h in pl["hist"])
assert [round(v, 2) for v in pl["costs"]] == [59.02, 314.23, 348.88]


def cost(i, h):
    b = pl["candidates"][i].copy()
    b.P, b.DT = h["P"], h["DT"]
    return sum(tk.band_cost(b, ob).values())


def frame(k, final=False):
    fig = go.Figure()
    rd.room(fig)
    rd.person(fig, bk.PERSON_LEFT, bk.PERSON_R)
    x = c["x"]
    lines = ["<b>t = 2.5 s</b>, person 0.25 m further left"]
    if final:
        lines.append("selection costs:")
    else:
        p, s = divmod(k, 6)
        lines.append(f"<b>pass {p + 1} of 4</b>, " + ("bands resized" if s == 0 else f"step {s} of 5") +
                     f"; obstacle weight {50 * 2 ** p}")
    for i, (hst, col) in enumerate(zip(pl["hist"], COL)):
        h = hst[min(k, 23)]
        if final and i != pl["best"]:
            rd.band(fig, h["P"], col, size=5, width=1.5, ticks=False)
        else:
            rd.band(fig, h["P"], col, size=7, width=2.5)
        if final and i == pl["init_idx"]:
            txt = f"{pl['candidates'][i].cost:.3f} × 0.95 = {pl['costs'][i]:.3f}"
        else:
            txt = f"{pl['costs'][i]:.3f}" if final else f"{cost(i, h):.1f}"
        tag = "  <b>picked</b>" if final and i == pl["best"] else ""
        lines.append(f"<span style='color:{col}'>{NAME[i]}: {txt}{tag}</span>")
    rd.robot(fig, *x, "#4C78A8")
    g = c["goal"]
    fig.add_trace(go.Scatter(x=[g[0]], y=[g[1]], mode="markers", marker=dict(symbol="x", size=16, color="#333333")))
    fig.add_annotation(x=1.37, y=3.93, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                       align="left", font=dict(size=18), bgcolor="rgba(255,255,255,0.92)")
    rd.zoom(fig, (1.35, 4.1), (1.45, 4.05))
    fig.update_layout(template="simple_white", font=FONT, width=800, height=760, showlegend=False,
                      margin=dict(l=10, r=10, t=10, b=10))
    return fig


figs = [frame(k) for k in range(24)] + [frame(23, final=True)]
make_gif(figs, here / "optim_anim", fps=3, holds=[5] + [1] * 22 + [3, 14], keys=[0, 6, 12, 24], cols=2, width=600)
print("costs with the set weights, first -> last:", [(round(cost(i, h[0]), 2), round(cost(i, h[-1]), 2)) for i, h in enumerate(pl["hist"])])
