"""The 256 first-layer weights without regularisation and with L2: box plots and density curves (Plotly)."""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
w = pd.read_csv(here.parent / "data" / "first_layer_weights.csv")
fig = make_subplots(1, 2, horizontal_spacing=0.1, column_widths=[0.4, 0.6],
                    subplot_titles=["Box plots", "Density of the weights"])
grid = np.linspace(-3, 3, 1201)
top = 0
for n, c, label in (("none", BLUE, "no regularisation"), ("L2", ORANGE, "L2, λ = 0.03")):
    fig.add_box(y=w[n], name=label, marker_color=c, boxpoints="outliers", showlegend=False, row=1, col=1)
    dens = gaussian_kde(w[n])(grid)
    top = max(top, dens.max())
    fig.add_scatter(x=grid, y=dens, name=label, line=dict(color=c, width=3), fill="tozeroy",
                    row=1, col=2)
fig.update_yaxes(title="weight", row=1, col=1)
fig.update_xaxes(title="weight", row=1, col=2)
fig.update_yaxes(title="density", range=[0, top * 1.05], row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=460, font=FONT,
                  legend=dict(x=0.75, y=0.95), margin=dict(l=60, r=20, t=50, b=60))
fig.update_annotations(font=dict(size=18))
fig.write_image(here / "weights.png", scale=2)
fig.write_image(here / "weights.pdf")
