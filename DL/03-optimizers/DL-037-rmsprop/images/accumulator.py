"""The accumulator v of the bias b over 300 steps: AdaGrad's sum of squared gradients only grows; RMSProp's EWMA
follows the recent gradients and shrinks again (left). The resulting step size eta/sqrt(v) of b (right) (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import GREEN, PURPLE, FONT
from shared import ETA, run

here = Path(__file__).parent
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=("accumulator v of b", "effective learning rate η / √v of b"))
steps = np.arange(1, 301)
for kind, name, c in (("adagrad", "AdaGrad: sum of squares", GREEN), ("rmsprop", "RMSProp: EWMA of squares", PURPLE)):
    _, V = run(kind)
    fig.add_trace(go.Scatter(x=steps, y=V[:, 1], name=name, line=dict(color=c, width=3)), 1, 1)
    fig.add_trace(go.Scatter(x=steps, y=ETA / np.sqrt(V[:, 1]), showlegend=False, line=dict(color=c, width=3)), 1, 2)
fig.update_yaxes(type="log")
fig.update_yaxes(title_text="v (log scale)", col=1)
fig.update_yaxes(title_text="η / √v (log scale)", col=2)
fig.update_xaxes(title_text="step")
fig.update_layout(template="simple_white", width=1050, height=440, font=FONT,
                  legend=dict(orientation="h", x=0, y=-0.25), margin=dict(l=80, r=20, t=40, b=110))
fig.write_image(here / "accumulator.png", scale=2)
fig.write_image(here / "accumulator.pdf")
