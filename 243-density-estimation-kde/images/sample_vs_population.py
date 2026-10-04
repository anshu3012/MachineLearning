"""A histogram describes the sample, a density estimate aims at the population: four samples of 200 values from the
same two-peaked population (300:700 mixture of normals at 20 and 40, sd 5). The histogram changes from sample to
sample; the KDE (bandwidth 3) stays close to the true population PDF (dashed). Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats
from sklearn.neighbors import KernelDensity
from anim import save_gif, FONT, ORANGE

here = Path(__file__).parent
x = np.linspace(0, 60, 300)
true = 0.3 * stats.norm(20, 5).pdf(x) + 0.7 * stats.norm(40, 5).pdf(x)
rng = np.random.default_rng(1)


def frame(k):
    n1 = rng.binomial(200, 0.3)
    s = np.concatenate([rng.normal(20, 5, n1), rng.normal(40, 5, 200 - n1)])
    kde = np.exp(KernelDensity(bandwidth=3).fit(s.reshape(-1, 1)).score_samples(x.reshape(-1, 1)))
    err = np.trapezoid(np.abs(kde - true), x)
    fig = go.Figure()
    fig.add_histogram(x=s, histnorm="probability density", xbins=dict(start=0, end=60, size=2),
                      marker_color="rgba(76,120,168,0.4)", name="this sample's histogram")
    fig.add_scatter(x=x, y=true, mode="lines", line=dict(color="black", dash="dash", width=3), name="population PDF")
    fig.add_scatter(x=x, y=kde, mode="lines", line=dict(color=ORANGE, width=4), name="KDE of this sample")
    fig.update_layout(template="simple_white", width=1000, height=620, font=FONT, bargap=0.05,
                      title=dict(text=f"<b>Sample {k}</b> of 200 values from the same population", x=0.5),
                      xaxis=dict(title="value", range=[0, 60]), yaxis=dict(title="density", range=[0, 0.1]),
                      legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.8)"), margin=dict(l=90, r=30, t=80, b=80))
    return fig, err


if __name__ == "__main__":
    out = [frame(k) for k in range(1, 5)]
    assert all(e < 0.25 for _, e in out), [e for _, e in out]    # every KDE stays close to the population PDF
    save_gif([f for f, _ in out], "sample_vs_population", here, keys=[0, 1, 2, 3], fps=1, holds=[3, 3, 3, 5])
