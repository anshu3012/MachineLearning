"""Particle deprivation, as an animation. Two particle filters get the same three readings: 5 particles (seed 9) and
100 particles (seed 2, the run of pf_loop.gif). The 5 particles start with none at door 1, where the robot is; the
one at door 3 takes the weight of reading 1, its copies move to plain wall where reading 2 cannot tell them apart,
and they end tight at door 1, the wrong door (0.99 of the weight). The 100 particles end at door 3 (0.96).
Last frame: the share of 1000 runs per particle count that end at the right door.
Run: python deprivation_anim.py -> deprivation_anim.gif, deprivation_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from pfsim import DOORS, LOOP, X_TRUE, run

here = Path(__file__).parent
RUNS = {5: run(5, np.random.default_rng(9)), 100: run(100, np.random.default_rng(2))}
NAMES = [s[0] for s in RUNS[5]][:-1]                       # start ... weigh 3 (the table of Section 4.5 stops there)


def shares(x, w):
    return [float(np.sum(w[(x >= a) & (x <= b)])) for a, b in DOORS]


S = {M: [shares(x, w) for _, x, w in RUNS[M]] for M in RUNS}
x5 = {n: x for n, x, _ in RUNS[5]}
assert np.sum((x5["start"] >= 1.5) & (x5["start"] <= 2.5)) == 0               # no particle at door 1, the robot's
assert np.isclose(S[5][1][2], 0.964, atol=5e-4) and np.ptp(x5["resample 1"]) == 0   # one door particle, 5 copies
assert np.all((x5["move 1"] > 7.5) & (x5["move 1"] < 10)) and np.ptp(RUNS[5][4][2]) < 1e-12   # wall, equal weights
assert round(S[5][7][0], 2) == 0.99 and round(S[100][7][2], 2) == 0.96          # weigh 3: door 1 vs door 3

TITLES = {"start": "1. same three readings, two filters: 5 particles and 100 particles",
          "weigh 1": "reading 1 says door: of the 5, only one is at a door (door 3)",
          "resample 1": "resample: the 5 particles become 5 copies of that one",
          "move 1": "move 2.5 m: the 5 copies land beside plain wall",
          "weigh 2": "reading 2 says door: none of the 5 fits, so all keep equal weight",
          "resample 2": "resample: nothing to choose between, the 5 stay together",
          "move 2": "move 2.5 m: the 5 go round the loop to door 1",
          "weigh 3": "reading 3 says door: the 5 end in one cluster at door 1, the wrong door"}
jitter = np.random.default_rng(7).uniform(0.12, 0.72, 100)


def truth(name):
    return X_TRUE[0 if name in ("start", "weigh 1", "resample 1") else 1 if name in ("move 1", "weigh 2",
                                                                                      "resample 2") else 2]


def frame(i, name):
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.2, subplot_titles=["<b>5 particles</b>",
                                                                               "<b>100 particles</b>"])
    for r, M in enumerate(RUNS, start=1):
        ax = "" if r == 1 else "2"
        for a, b in DOORS:
            fig.add_shape(type="rect", x0=a, x1=b, y0=0, y1=1, xref=f"x{ax}", yref=f"y{ax} domain", fillcolor=ORANGE,
                          opacity=0.18, line_width=0, layer="below")
        _, x, w = RUNS[M][i]
        fig.add_trace(go.Scatter(x=x, y=jitter[:M], mode="markers", marker=dict(size=np.clip(4 + 16 * np.sqrt(w * M),
                                 3, 60), color=BLUE, opacity=0.55, line=dict(width=0))), row=r, col=1)
        fig.add_trace(go.Scatter(x=[truth(name)], y=[0.97], mode="markers+text", text=["robot"],
                                 marker=dict(symbol="triangle-down", size=22, color=RED), textposition="middle right",
                                 textfont=dict(size=17, color=RED)), row=r, col=1)
        d = S[M][i]
        fig.add_annotation(x=1, y=1.04, xref=f"x{ax} domain", yref=f"y{ax} domain", xanchor="right", yanchor="bottom",
                           showarrow=False, font=dict(size=19),
                           text=f"share of weight at doors 1, 2, 3:  {d[0]:.2f},  {d[1]:.2f},  {d[2]:.2f}")
    fig.update_xaxes(range=[0, LOOP], dtick=1)
    fig.update_xaxes(title="position x (m)", row=2, col=1)
    fig.update_yaxes(visible=False, range=[0, 1.08])
    fig.update_annotations(selector=dict(text="<b>5 particles</b>"), x=0, xanchor="left", font_size=21)
    fig.update_annotations(selector=dict(text="<b>100 particles</b>"), x=0, xanchor="left", font_size=21)
    fig.add_annotation(xref="paper", yref="paper", x=0.5, y=-0.2, yanchor="top", showarrow=False,
                       font=dict(size=16, color=GREY),
                       text="orange: doors; marker size grows with a particle's weight; red triangle: the true robot")
    fig.update_layout(template="simple_white", font=FONT, width=1100, height=760, showlegend=False,
                      margin=dict(l=40, r=40, t=100, b=130), title=dict(x=0.5, y=0.97, font=dict(size=23),
                                                                         text=f"{i + 1}. {TITLES[name]}"
                                                                         if i else TITLES[name]))
    return fig


def tally():
    """The last frame: 1000 runs per particle count; the asserted shares are the notebook's."""
    rng = np.random.default_rng(1)
    Ms = [5, 10, 20, 50, 100]
    rate = [100 * np.mean([np.mean(np.abs(run(M, rng)[-1][1] - 7.0) < 0.8) > 0.5 for _ in range(1000)]) for M in Ms]
    assert np.allclose(np.round(rate, 1), [43.9, 63.0, 87.8, 99.6, 100.0])
    fig = go.Figure(go.Bar(x=[str(m) for m in Ms], y=rate, marker_color=BLUE, text=[f"{r:.1f} percent" for r in rate],
                           textposition="outside", textfont=dict(size=19)))
    fig.update_layout(template="simple_white", font=FONT, width=1100, height=760, margin=dict(l=90, r=40, t=110, b=90),
                      title=dict(x=0.5, y=0.97, font=dict(size=23),
                                 text="9. not by chance: share of 1000 runs that end at the right door, for each M"),
                      xaxis=dict(title="number of particles M"), yaxis=dict(title="percent of runs", range=[0, 115]))
    return fig


figs = [frame(i, n) for i, n in enumerate(NAMES)]
figs[-1].update_layout(title_text="8. reading 3: 5 particles end in one cluster at door 1, the wrong door; 100 end at door 3")
figs.append(tally())
holds = [5] + [4] * (len(NAMES) - 2) + [10, 16]
make_gif(figs, here / "deprivation_anim", fps=2, holds=holds,
         keys=[0, NAMES.index("weigh 1"), NAMES.index("weigh 2"), NAMES.index("move 2"), len(NAMES) - 1, len(NAMES)],
         cols=2, width=900)
