"""Breaking the independence condition: 10 students each say "good" with probability 0.5. Independent answers give
Binomial(10, 0.5). Linked answers (in half of the workshops the students talk first and all copy one student) pile
up at 0 and 10, and the count is no longer binomial. 10,000 simulated workshops each."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
rng = np.random.default_rng(0)
N = 10_000
indep = rng.binomial(10, 0.5, N)
talk = rng.random(N) < 0.5
first = rng.random(N) < 0.5
linked = np.where(talk, 10 * first, rng.binomial(10, 0.5, N))
share = lambda v: np.bincount(v, minlength=11) / N
assert share(linked)[[0, 10]].min() > 0.2 and share(indep)[[0, 10]].max() < 0.005
k = np.arange(11)
fig = go.Figure()
fig.add_bar(x=k - 0.2, y=share(indep), width=0.38, marker_color="#4C78A8", name="independent answers")
fig.add_bar(x=k + 0.2, y=share(linked), width=0.38, marker_color="#E45756", name="linked answers (students talk first)")
fig.add_scatter(x=k, y=stats.binom(10, 0.5).pmf(k), mode="markers", marker=dict(color="black", size=11, symbol="diamond"),
                name="Binomial(10, 0.5) formula")
fig.update_layout(template="simple_white", width=1100, height=620, font=dict(family="Latin Modern Roman", size=19),
                  title=dict(text="10 students rate a workshop: only independent answers follow the binomial formula", x=0.5,
                             font=dict(size=21)),
                  xaxis=dict(title="students who said good", dtick=1), yaxis=dict(title="share of 10,000 workshops"),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2), margin=dict(l=90, r=30, t=70, b=120))
fig.write_image(here / "not_independent.png", scale=2)
fig.write_image(here / "not_independent.pdf")
