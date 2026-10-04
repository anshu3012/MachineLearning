"""Model simple cell (one filter position) and model complex cell (max over a neighbourhood):
left, response against the bar's angle; right, response against a sideways shift of a vertical bar (Plotly).
Insets show example bar images."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
t = pd.read_csv(here.parent / "data" / "tuning.csv")
p = pd.read_csv(here.parent / "data" / "position.csv")
bars = np.load(here.parent / "data" / "bars.npy")
fig = make_subplots(2, 6, row_heights=[0.25, 0.75], vertical_spacing=0.1, horizontal_spacing=0.03,
                    specs=[[{}, {}, {}, {}, {}, {}], [{"colspan": 3}, None, None, {"colspan": 3}, None, None]],
                    subplot_titles=("bar at 0°", "45°", "90° (vertical)", "", "90°, shifted 5 px", "",
                                    "orientation: rotate the bar", "position: shift a vertical bar"))
for k, (img, col) in enumerate(zip(bars, (1, 2, 3, 5))):
    fig.add_trace(go.Heatmap(z=img, colorscale="gray", showscale=False), 1, col)
for name, c, dash in (("simple", BLUE, "solid"), ("complex", ORANGE, "dash")):
    label = "model simple cell (one filter position)" if name == "simple" else "model complex cell (max over a neighbourhood)"
    fig.add_trace(go.Scatter(x=t.angle, y=t[name], name=label, line=dict(color=c, width=4, dash=dash)), 2, 1)
    fig.add_trace(go.Scatter(x=p["shift"], y=p[name], showlegend=False, line=dict(color=c, width=4, dash=dash),
                             mode="lines+markers"), 2, 4)
for col in range(1, 7):
    fig.update_xaxes(visible=False, row=1, col=col)
    fig.update_yaxes(visible=False, autorange="reversed", row=1, col=col)
for k in (1, 2, 3, 5):
    fig.layout[f"yaxis{'' if k == 1 else k}"].scaleanchor = f"x{'' if k == 1 else k}"
for col in (4, 6):
    fig.update_xaxes(visible=False, row=1, col=col); fig.update_yaxes(visible=False, row=1, col=col)
fig.update_xaxes(title="angle of the bar (degrees; 90 = vertical)", tickvals=[0, 45, 90, 135, 180], row=2, col=1)
fig.update_xaxes(title="sideways shift of the bar (pixels)", row=2, col=4)
fig.update_yaxes(title="response (1 = largest)", range=[-0.03, 1.08], row=2, col=1)
fig.update_yaxes(range=[-0.03, 1.08], row=2, col=4)
fig.update_layout(template="simple_white", width=1200, height=640, font=FONT,
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.18), margin=dict(l=70, r=20, t=40, b=110))
fig.write_image(here / "cell_models.png", scale=2)
fig.write_image(here / "cell_models.pdf")
