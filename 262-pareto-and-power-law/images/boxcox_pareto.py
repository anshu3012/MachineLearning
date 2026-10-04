"""Making Pareto data closer to normal: 1,000 values from a Pareto distribution (alpha = 3, the scipy sample of
section 3.5), raw (skewness 7.68), after the log (1.87) and after Box-Cox (lambda = -2.17, skewness 0.30)."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
d = stats.pareto(b=3, scale=1).rvs(size=1000, random_state=42)
bc, lam = stats.boxcox(d)
sets = [("raw", d), ("log", np.log(d)), (f"Box-Cox, λ = {lam:.2f}", bc)]
sk = [pd.Series(v).skew() for _, v in sets]
assert [round(s, 2) for s in sk] == [7.68, 1.87, 0.30] and round(lam, 2) == -2.17
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.06,
                    subplot_titles=[f"{n}: skewness {s:.2f}" for (n, _), s in zip(sets, sk)])
for j, (_, v) in enumerate(sets, start=1):
    fig.add_histogram(x=v, nbinsx=40, marker_color="#4C78A8" if j < 3 else "#54A24B", row=1, col=j)
fig.update_annotations(font_size=21)
fig.update_layout(template="simple_white", width=1400, height=440, showlegend=False, bargap=0.05,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=50, r=20, t=60, b=40))
fig.write_image(here / "boxcox_pareto.png", scale=2)
fig.write_image(here / "boxcox_pareto.pdf")
