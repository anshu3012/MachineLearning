"""Average loss per epoch: our backpropagation code and Keras, regression and classification (from the Notebook)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREY, FONT

here = Path(__file__).parent
reg = pd.read_csv(here.parent / "data" / "regression_loss.csv")
cls = pd.read_csv(here.parent / "data" / "classification_loss.csv")
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=("Regression: MSE, learning rate 0.001", "Classification: BCE, learning rate 0.001"))
for col, d in ((1, reg), (2, cls)):
    fig.add_trace(go.Scatter(x=d.epoch, y=d.ours, name="our code", line=dict(color=BLUE, width=7),
                             showlegend=col == 1), row=1, col=col)
    fig.add_trace(go.Scatter(x=d.epoch, y=d.keras, name="Keras", line=dict(color=ORANGE, width=3, dash="dash"),
                             showlegend=col == 1), row=1, col=col)
    fig.update_xaxes(title_text="epoch", row=1, col=col)
fig.update_yaxes(title_text="average loss (log scale)", type="log", tickvals=[0.2, 0.5, 1, 2, 5, 10, 20],
                 row=1, col=1)
fig.update_yaxes(title_text="average loss", range=[0.68, 0.70], row=1, col=2)
fig.add_trace(go.Scatter(x=[1, 50], y=[0.6931, 0.6931], mode="lines", line=dict(color=GREY, width=2, dash="dot"),
                         showlegend=False), row=1, col=2)
fig.add_annotation(x=50, y=0.6931, text="log 2 = 0.693: always predicting 0.5", showarrow=False, xanchor="right",
                   yshift=-14, row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=460, font=FONT, legend=dict(x=0.3, y=0.98),
                  margin=dict(l=80, r=30, t=60, b=60))
fig.update_annotations(font=dict(family="Latin Modern Roman", size=17))
fig.write_image(here / "loss_curves.png", scale=2)
fig.write_image(here / "loss_curves.pdf")
