"""Section 2's Extra as a chart: 10-fold cross-validated accuracy on the noisy circles of the AdaBoost
hyperparameters Note, for a stump and a fully grown tree alone, bagged and boosted (100 base models each).
Numbers from the Notebook (asserted against the Note's table). Plotly."""
from pathlib import Path
import plotly.graph_objects as go

here = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=19)
GREY, BLUE, ORANGE = "#6B6B6B", "#4C78A8", "#F58518"
ACC = {"stump": (0.566, 0.738, 0.814), "fully grown tree": (0.746, 0.808, 0.750)}
fig = go.Figure()
for i, (name, col) in enumerate((("alone", GREY), ("bagging", BLUE), ("AdaBoost", ORANGE))):
    vals = [ACC[b][i] for b in ACC]
    fig.add_bar(x=list(ACC), y=vals, name=name, marker_color=col, text=[f"{v:.3f}" for v in vals], textposition="outside")
fig.add_annotation(x=1.45, y=0.505, text="axis starts at 0.5, guessing", showarrow=False, font=dict(size=15, color=GREY), xanchor="right", yanchor="bottom")
fig.update_layout(template="simple_white", width=1000, height=430, font=FONT, barmode="group",
                  xaxis=dict(title="base model"), yaxis=dict(title="cross-validated accuracy", range=[0.5, 0.88]),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=1.12), margin=dict(l=80, r=20, t=50, b=70))
fig.write_image(here / "swap_bars.png", scale=2)
fig.write_image(here / "swap_bars.pdf")
