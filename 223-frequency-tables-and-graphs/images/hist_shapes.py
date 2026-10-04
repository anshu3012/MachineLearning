"""Six shapes a histogram can take, from synthetic data with a fixed seed. Plotly."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots

here = Path(__file__).parent
rng = np.random.default_rng(1)
n = 5000
shapes = {
    "symmetric": rng.normal(50, 10, n),
    "bimodal": np.concatenate([rng.normal(35, 6, n // 2), rng.normal(68, 6, n // 2)]),
    "right skew (long tail right)": 20 + rng.gamma(2, 9, n),
    "left skew (long tail left)": 100 - rng.gamma(2, 9, n),
    "uniform": rng.uniform(10, 90, n),
    "no pattern (too many bins)": rng.normal(50, 15, 60),
}
fig = make_subplots(rows=2, cols=3, subplot_titles=list(shapes), horizontal_spacing=0.08, vertical_spacing=0.16)
for i, v in enumerate(shapes.values()):
    c, e = np.histogram(v, bins=30)
    fig.add_bar(x=(e[:-1] + e[1:]) / 2, y=c / c.sum(), width=np.diff(e), marker_color="#4C78A8",
                marker_line=dict(color="white", width=0.5), row=i // 3 + 1, col=i % 3 + 1)
fig.update_yaxes(title_text="share of values", col=1)
fig.update_annotations(font_size=20)
fig.update_layout(template="simple_white", width=1100, height=620, showlegend=False, bargap=0,
                  font=dict(family="Latin Modern Roman", size=16), margin=dict(l=70, r=20, t=40, b=40))
fig.write_image(here / "hist_shapes.png", scale=2)
fig.write_image(here / "hist_shapes.pdf")
