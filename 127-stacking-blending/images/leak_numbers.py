"""Section 5's measurement on the heart data (Notebook, section 7). Left: the mean gap between predicted probability
and true class for the random forest and gradient boosting, on their own training patients and on patients they did
not see. Right: the weights the meta-model gives each base model when it learns from in-sample predictions. Plotly."""
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=18)
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#6B6B6B"
GAP = {"random forest": (0.09, 0.30), "gradient boosting": (0.07, 0.25)}     # the Note's numbers
W = {"random forest": 3.5, "gradient boosting": 3.8, "KNN": 1.0}
fig = make_subplots(rows=1, cols=2, column_widths=[0.55, 0.45], horizontal_spacing=0.12,
                    subplot_titles=("mean error: seen against unseen patients", "meta-model weight (in-sample)"))
fig.add_bar(x=list(GAP), y=[v[0] for v in GAP.values()], name="on its own training patients", marker_color=BLUE,
            text=[f"{v[0]:.2f}" for v in GAP.values()], textposition="outside", row=1, col=1)
fig.add_bar(x=list(GAP), y=[v[1] for v in GAP.values()], name="on patients it did not see", marker_color=ORANGE,
            text=[f"{v[1]:.2f}" for v in GAP.values()], textposition="outside", row=1, col=1)
fig.add_bar(x=list(W), y=list(W.values()), marker_color=GREY, showlegend=False, text=[f"{v:.1f}" for v in W.values()],
            textposition="outside", row=1, col=2)
fig.update_yaxes(range=[0, 0.36], title="|probability - true class|", row=1, col=1)
fig.update_yaxes(range=[0, 4.5], row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=440, font=FONT, barmode="group",
                  legend=dict(orientation="h", x=0.27, xanchor="center", y=-0.15), margin=dict(l=70, r=20, t=50, b=90))
fig.write_image(here / "leak_numbers.png", scale=2)
fig.write_image(here / "leak_numbers.pdf")
