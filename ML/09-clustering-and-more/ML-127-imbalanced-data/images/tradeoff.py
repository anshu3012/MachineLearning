"""Section 10's table as a picture: minority precision against minority recall for every technique on the
mammography data (mean of 15 cross-validation folds, numbers from the Notebook). Every fix moves a model to the right
(more calcifications found) and down (more false alarms). Plotly."""
from pathlib import Path
import plotly.graph_objects as go

here = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=17)
ROWS = [("logistic regression", 0.79, 0.40, "#4C78A8"), ("LR + any of the 4 fixes", 0.17, 0.85, "#4C78A8"),
        ("random forest", 0.88, 0.54, "#54A24B"), ("balanced random forest", 0.31, 0.85, "#54A24B"),
        ("XGBoost", 0.83, 0.54, "#F58518"), ("XGBoost, custom loss", 0.56, 0.77, "#F58518")]
POS = {"logistic regression": "middle left", "LR + any of the 4 fixes": "middle left", "random forest": "top center",
       "balanced random forest": "middle left", "XGBoost": "middle left", "XGBoost, custom loss": "top center"}
fig = go.Figure()
for i in range(0, 6, 2):
    a, b = ROWS[i], ROWS[i + 1]
    fig.add_annotation(x=b[2], y=b[1], ax=a[2], ay=a[1], xref="x", yref="y", axref="x", ayref="y", showarrow=True,
                       arrowhead=2, arrowwidth=2.5, arrowcolor=a[3], text="")
for name, p, r, col in ROWS:
    fig.add_scatter(x=[r], y=[p], mode="markers+text", marker=dict(size=14, color=col), text=[name],
                    textposition=POS[name], showlegend=False)
fig.update_layout(template="simple_white", width=1000, height=520, font=FONT,
                  xaxis=dict(title="recall of the minority class", range=[0, 1]),
                  yaxis=dict(title="precision of the minority class", range=[0, 1]), margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "tradeoff.png", scale=2)
fig.write_image(here / "tradeoff.pdf")
