"""The test of independence on gender by age group, as three tables (Plotly heatmaps): the observed counts, the
counts expected if the two features were independent (row total x column total / 60), and each cell's contribution
(O - E)^2 / E, which add up to chi-square = 2.50."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from gifkit import FONT

here = Path(__file__).parent
O = np.array([[12, 12, 10], [8, 14, 4]])
res = stats.chi2_contingency(O)
E = res.expected_freq
C = (O - E) ** 2 / E
assert round(E[0, 0], 2) == 11.33 and round(res.statistic, 2) == 2.50 and round(res.pvalue, 2) == 0.29 and res.dof == 2
assert [round(c, 3) for c in C.ravel()] == [0.039, 0.507, 0.538, 0.051, 0.663, 0.704]
cols, rows = ["child", "adult", "elderly"], ["female", "male"]
fig = make_subplots(1, 3, horizontal_spacing=0.07, subplot_titles=["observed O", "expected E if independent",
                                                                   f"(O − E)² / E: total {C.sum():.2f}"])
fig.update_annotations(font_size=22)
for col, (M, fmt, scale) in enumerate([(O, "{:.0f}", "Blues"), (E, "{:.2f}", "Greys"), (C, "{:.3f}", "Oranges")], 1):
    fig.add_trace(go.Heatmap(z=M[::-1], x=cols, y=rows[::-1], colorscale=scale, showscale=False,
                             zmin=0, zmax=M.max() * 1.6, text=[[fmt.format(v) for v in r] for r in M[::-1]],
                             texttemplate="%{text}", textfont=dict(size=24)), 1, col)
fig.update_layout(template="simple_white", width=1300, height=380, font=FONT, margin=dict(l=90, r=20, t=60, b=40))
fig.write_image(here / "independence_table.png", scale=2)
