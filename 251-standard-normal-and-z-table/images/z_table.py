"""Reading the z-table: the area under the standard normal curve to the left of z = 1.33 (left), and the part of the
positive z-table that holds it, row 1.3 and column 0.03 (right)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#6B6B6B"
fig = make_subplots(rows=1, cols=2, column_widths=[0.45, 0.55], horizontal_spacing=0.06,
                    specs=[[{"type": "xy"}, {"type": "table"}]],
                    subplot_titles=["Φ(1.33) = area to the left of 1.33", "Positive z-table (excerpt)"])
z = np.linspace(-3.5, 3.5, 600)
fig.add_scatter(x=z, y=stats.norm.pdf(z), mode="lines", line=dict(color=BLUE, width=4), row=1, col=1)
s = np.linspace(-3.5, 1.33, 400)
fig.add_scatter(x=np.r_[s, 1.33], y=np.r_[stats.norm.pdf(s), 0], fill="tozeroy", fillcolor="rgba(76,120,168,0.35)",
                mode="lines", line=dict(width=0), row=1, col=1)
fig.add_annotation(x=0, y=0.15, text="0.90824", showarrow=False, font=dict(size=22), row=1, col=1)
fig.add_annotation(x=2.1, y=0.07, text="1 − 0.90824<br>= 0.09176", ax=40, ay=-50, font=dict(size=17), row=1, col=1)
rows = [1.1, 1.2, 1.3, 1.4, 1.5]
cols = [0.00, 0.01, 0.02, 0.03, 0.04, 0.05]
cells = [[f"<b>{r:.1f}</b>" for r in rows]] + [[f"{stats.norm.cdf(r + c):.5f}" for r in rows] for c in cols]
fill = [["#EEEEEE"] * len(rows)] + [["#FBE3CC" if (r == 1.3 and c == 0.03) else
                                     ("#EAF0F7" if (r == 1.3 or c == 0.03) else "white") for r in rows] for c in cols]
fig.add_trace(go.Table(header=dict(values=["<b>z</b>"] + [f"<b>{c:.2f}</b>" for c in cols], fill_color="#EEEEEE",
                                   font=dict(size=17, family="Latin Modern Roman"), height=36),
                       cells=dict(values=cells, fill_color=fill, font=dict(size=17, family="Latin Modern Roman"),
                                  height=36)), row=1, col=2)
fig.update_xaxes(title_text="z", dtick=1, row=1, col=1)
fig.update_yaxes(title_text="density", row=1, col=1)
fig.update_annotations(selector=dict(xref="paper"), font_size=19)
fig.update_layout(template="simple_white", width=1250, height=430, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=50, b=50))
fig.write_image(here / "z_table.png", scale=2)
fig.write_image(here / "z_table.pdf")
