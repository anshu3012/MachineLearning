"""Poisson PMF with lambda = 4 (questions per day). Left: the bar for exactly 7 questions. Right: the bars for
7 or more, whose total height is P(Y >= 7)."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE, RED = "#4C78A8", "#E45756"
y = np.arange(0, 15)
pmf = stats.poisson.pmf(y, 4)
fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.06,
                    subplot_titles=["exactly 7: P(Y = 7) = 0.060", "7 or more: P(Y ≥ 7) = 0.111"])
for col, red in [(1, y == 7), (2, y >= 7)]:
    fig.add_bar(x=y, y=pmf, marker_color=np.where(red, RED, BLUE), showlegend=False, row=1, col=col)
    fig.update_xaxes(tickvals=list(range(0, 15, 2)), title_text="questions in one day, y", row=1, col=col)
fig.update_yaxes(title_text="P(Y = y)", row=1, col=1)
fig.update_annotations(font_size=20)
fig.update_layout(template="simple_white", width=1100, height=420, bargap=0.15,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=40, b=40))
fig.write_image(here / "questions_pmf.png", scale=2)
fig.write_image(here / "questions_pmf.pdf")
