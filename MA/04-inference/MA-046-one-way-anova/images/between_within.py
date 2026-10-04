"""Two sets of three groups with the same group means (5, 7, 9). Left: values close to their group mean, so the
gaps between means stand out (F = 12). Right: values spread widely, so the same gaps drown in the noise (F = 0.75)."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
COLOURS = ["#4C78A8", "#F58518", "#54A24B"]
SETS = {"tight groups: F = 12, p = 0.008": [[4, 5, 6], [6, 7, 8], [8, 9, 10]],
        "spread-out groups: F = 0.75, p = 0.51": [[1, 5, 9], [3, 7, 11], [5, 9, 13]]}
fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.06, subplot_titles=list(SETS))
for col, (title, groups) in enumerate(SETS.items(), start=1):
    assert abs(stats.f_oneway(*groups).statistic - (12 if col == 1 else 0.75)) < 1e-9
    for i, (vals, colour, name) in enumerate(zip(groups, COLOURS, "ABC")):
        fig.add_scatter(x=[i] * 3, y=vals, mode="markers", marker=dict(color=colour, size=16), showlegend=False,
                        row=1, col=col)
        fig.add_scatter(x=[i - 0.3, i + 0.3], y=[np.mean(vals)] * 2, mode="lines", line=dict(color=colour, width=4),
                        showlegend=False, row=1, col=col)
    fig.add_scatter(x=[-0.5, 2.5], y=[7, 7], mode="lines", line=dict(color="black", dash="dash", width=2),
                    name="grand mean 7", showlegend=(col == 1), row=1, col=col)
    fig.update_xaxes(tickvals=[0, 1, 2], ticktext=["section A", "section B", "section C"], range=[-0.6, 2.6],
                     row=1, col=col)
fig.update_yaxes(title_text="marks", row=1, col=1)
fig.update_annotations(font_size=20)
fig.update_layout(template="simple_white", width=1100, height=430,
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.15),
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=40, b=40))
fig.write_image(here / "between_within.png", scale=2)
fig.write_image(here / "between_within.pdf")
