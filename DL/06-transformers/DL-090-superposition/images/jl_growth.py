"""Section 6: the dimension k that the Johnson-Lindenstrauss bound (Dasgupta and Gupta 2003, epsilon = 0.1) needs to
guarantee n directions with every cosine below 0.222. k grows with log n, so n grows exponentially with k
(data/jl_table.csv, Notebook). Plotly."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, GREY, FONT

here = Path(__file__).parent
J = pd.read_csv(here.parent / "data" / "jl_table.csv")
eps = 0.1
k = lambda n: 4 * np.log(n + 1) / (eps ** 2 / 2 - eps ** 3 / 3)             # n directions plus the origin
assert np.allclose(np.ceil(k(J.directions.values)), J.k_needed.values)
nn = np.logspace(2, 13, 200)
fig = go.Figure()
fig.add_scatter(x=k(nn), y=nn, mode="lines", line=dict(color=GREY, width=3), showlegend=False)
fig.add_scatter(x=J.k_needed, y=J.directions, mode="markers+text", marker=dict(size=13, color=BLUE), showlegend=False,
                text=[f"{n:,} directions<br>k = {k:,}" for n, k in zip(J.directions, J.k_needed)], textposition="top left",
                textfont=dict(size=15))
fig.update_layout(template="simple_white", width=1000, height=470, font=dict(FONT, size=18),
                  xaxis=dict(title="dimension k", range=[0, 26000]),
                  yaxis=dict(type="log", title="directions n that fit (every cosine < 0.222)", exponentformat="power", dtick=3),
                  margin=dict(l=90, r=30, t=20, b=70))
fig.write_image(here / "jl_growth.png", scale=2)
fig.write_image(here / "jl_growth.pdf")
