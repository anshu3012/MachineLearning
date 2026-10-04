"""Next-word accuracy on the test stories: two simple baselines and the LSTM (mean of 5 seeds, error bar = 1 std) (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import GREY, GREEN, FONT

here = Path(__file__).parent
b = pd.read_csv(here.parent / "data" / "baselines.csv")
fig = go.Figure(go.Bar(y=b.method, x=b.test_accuracy, orientation="h", marker_color=[GREY, GREY, GREEN],
                       error_x=dict(type="data", array=b.test_accuracy_std, visible=True, thickness=2, width=8),
                       text=[f"{v:.3f}" for v in b.test_accuracy], textposition="inside", insidetextanchor="start",
                       textfont=dict(color="white", family=FONT["family"], size=18)))
fig.update_layout(template="simple_white", width=950, height=320, font=FONT, showlegend=False,
                  xaxis=dict(title="next-word accuracy on the test stories", range=[0, max(b.test_accuracy) * 1.15]),
                  yaxis=dict(autorange="reversed"), margin=dict(l=260, r=20, t=20, b=60))
fig.write_image(here / "baselines.png", scale=2)
fig.write_image(here / "baselines.pdf")
