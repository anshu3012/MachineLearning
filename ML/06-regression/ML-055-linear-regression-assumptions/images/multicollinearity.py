"""Assumption 2: correlations between the inputs and their VIF values (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools import add_constant
from common import df, X_train, BLUE, ORANGE, GREY, FONT

here = Path(__file__).parent
cols = ["feature1", "feature2", "feature3"]
corr = df[cols].corr().to_numpy()
Xc = add_constant(X_train)
vif = [variance_inflation_factor(Xc, i) for i in range(1, 4)]
fig = make_subplots(1, 2, column_widths=[0.55, 0.45], horizontal_spacing=0.15,
                    subplot_titles=("Correlation between inputs", "VIF of each input (problem above 5)"))
fig.add_trace(go.Heatmap(z=corr, x=cols, y=cols, zmin=-1, zmax=1, colorscale="RdBu", reversescale=True,
                         text=np.round(corr, 2), texttemplate="%{text}", textfont=dict(size=16), showscale=False), 1, 1)
fig.add_trace(go.Bar(x=cols, y=vif, marker_color=BLUE, text=[f"{v:.2f}" for v in vif], textposition="outside"), 1, 2)
fig.add_trace(go.Scatter(x=cols, y=[5] * 3, mode="lines", line=dict(color=ORANGE, dash="dash")), 1, 2)
fig.update_yaxes(autorange="reversed", row=1, col=1)
fig.update_yaxes(range=[0, 6], title="VIF", row=1, col=2)
fig.update_layout(template="simple_white", width=1000, height=420, showlegend=False, font=FONT,
                  margin=dict(l=80, r=20, t=50, b=50))
fig.update_annotations(font_size=16)
print([round(v, 3) for v in vif])
fig.write_image(here / "multicollinearity.png", scale=2)
fig.write_image(here / "multicollinearity.pdf")
