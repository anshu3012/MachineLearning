"""Chart: how often a roadmap of n uniform milestones (10 nearest neighbours) finds each of the four trips, over 200
runs per n (seeds 1000 to 1199), for n = 5, 10, 20, 50, 100. Every trip has a route, so each curve is the chance of
a correct answer; it rises towards 1 as n grows. Run -> success.png"""
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import prm
from gifkit import BLUE, FONT, GREEN, ORANGE, PURPLE

here = Path(__file__).parent
NS = (5, 10, 20, 50, 100)


def success(args):
    n, seed = args
    w = prm.World()
    V, E = prm.build(w, np.random.default_rng(1000 + seed), n)
    return [prm.query(w, V, E, s, g)[0] is not None for _, s, _, g in prm.TRIPS]


if __name__ == "__main__":
    with Pool(10) as pool:
        R = np.array([np.array(pool.map(success, [(n, s) for s in range(200)]), float).mean(0) for n in NS])
    assert np.allclose(R[:, 1], [0.14, 0.375, 0.715, 0.97, 0.995]) and np.allclose(R[:, 0], [0.965, 1, 1, 1, 1])
    fig = go.Figure()
    for k, (a, _, b, _) in enumerate(prm.TRIPS):
        fig.add_trace(go.Scatter(x=list(NS), y=100 * R[:, k], mode="lines+markers", name=f"trip {k + 1}: {a} to {b}",
                                 line=dict(color=[BLUE, ORANGE, GREEN, PURPLE][k], width=3), marker=dict(size=10)))
    fig.update_xaxes(type="log", tickvals=list(NS), title="milestones n (log scale)")
    fig.update_yaxes(range=[0, 104], title="trips found (percent of 200 runs)")
    fig.update_layout(template="simple_white", width=1100, height=560, font=FONT,
                      legend=dict(x=0.52, y=0.08, xanchor="left", yanchor="bottom", font=dict(size=19)),
                      title=dict(text="Every trip has a route; the chance of finding it rises with n", x=0.5),
                      margin=dict(l=90, r=30, t=70, b=70))
    fig.write_image(here / "success.png")
