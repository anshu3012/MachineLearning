"""Validation accuracy per epoch on raw vs standardized inputs, and the size of the first-layer gradients (Plotly)."""
from pathlib import Path
import pandas as pd
from plotly.subplots import make_subplots
from common import BLUE, RED, FONT

here = Path(__file__).parent
h = pd.read_csv(here.parent / "data" / "histories.csv")
g = pd.read_csv(here.parent / "data" / "gradients.csv").set_index("inputs")
fig = make_subplots(1, 2, column_widths=[0.62, 0.38], horizontal_spacing=0.12,
                    subplot_titles=["Validation accuracy per epoch", "Mean |gradient| of first-layer weights"])
fig.add_scatter(x=h.epoch, y=h.raw_val_accuracy, name="raw inputs", line=dict(color=RED, width=3), row=1, col=1)
fig.add_scatter(x=h.epoch, y=h.scaled_val_accuracy, name="standardized inputs", line=dict(color=BLUE, width=3),
                row=1, col=1)
for name, c in (("raw", RED), ("standardized", BLUE)):
    fig.add_bar(x=["age weights", "salary weights"], y=g.loc[name, ["age", "salary"]], marker_color=c,
                showlegend=False, text=[f"{v:,.0f}" if v >= 10 else f"{v:.3g}" for v in g.loc[name, ["age", "salary"]]], textposition="outside",
                row=1, col=2)
fig.update_xaxes(title="epoch", row=1, col=1)
fig.update_yaxes(range=[0.25, 1.0], tickformat=".0%", row=1, col=1)
fig.update_yaxes(type="log", range=[-2.6, 4.2], title="log scale", row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=470, font=FONT, barmode="group",
                  legend=dict(orientation="h", x=0.0, y=-0.2), margin=dict(l=60, r=20, t=50, b=60))
fig.update_annotations(font=dict(size=18))
fig.write_image(here / "scaling_effect.png", scale=2)
fig.write_image(here / "scaling_effect.pdf")
