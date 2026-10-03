"""Three curves with mean 0 and standard deviation 1 that differ only in their tails (generalised normal family):
leptokurtic (excess kurtosis +3), mesokurtic (normal, 0) and platykurtic (-1.08). Right: zoom on the right tail."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
curves = [  # (shape beta, name, colour, dash)
    (1, "leptokurtic", "#F58518", "dash"),
    (2, "mesokurtic (normal)", "#6B6B6B", "solid"),
    (8, "platykurtic", "#4C78A8", "dot"),
]
fig = make_subplots(rows=1, cols=2, column_widths=[0.6, 0.4], horizontal_spacing=0.1,
                    subplot_titles=["Same mean (0) and standard deviation (1)", "Zoom on the right tail"])
x = np.linspace(-4.5, 4.5, 900)
tail = np.linspace(2, 4.5, 300)
for beta, name, colour, dash in curves:
    g = stats.gennorm(beta)
    s = g.std()
    f = lambda v: g.pdf(v * s) * s                  # rescaled so the standard deviation is 1
    ex = float(g.stats(moments="k"))
    label = f"{name}, excess kurtosis {ex:+.2f}".replace("+0.00", "0").replace("-0.00", "0")
    fig.add_scatter(x=x, y=f(x), mode="lines", name=label, line=dict(color=colour, width=3.5, dash=dash), row=1, col=1)
    fig.add_scatter(x=tail, y=f(tail), mode="lines", showlegend=False, line=dict(color=colour, width=3.5, dash=dash),
                    row=1, col=2)
fig.update_xaxes(title_text="value (in standard deviations)", dtick=1, row=1, col=1)
fig.update_xaxes(title_text="value (in standard deviations)", dtick=0.5, row=1, col=2)
fig.update_yaxes(title_text="density", row=1, col=1)
fig.update_yaxes(range=[0, 0.06], row=1, col=2)
fig.update_annotations(font_size=19)
fig.update_layout(template="simple_white", width=1200, height=560,
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2, font=dict(size=16)),
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=60, r=20, t=50, b=40))
fig.write_image(here / "kurtosis_types.png", scale=2)
fig.write_image(here / "kurtosis_types.pdf")
