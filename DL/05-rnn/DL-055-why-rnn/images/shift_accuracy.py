"""Section 5.4's experiment as a chart: a small ANN trained on the first 50 words of IMDB reviews, tested on the
same test reviews pushed 0 to 20 positions to the right. Numbers from the Notebook (mean of 3 seeds). Plotly."""
from pathlib import Path
import plotly.graph_objects as go
from common import BLUE, GREY, FONT

here = Path(__file__).parent
SHIFT = [0, 1, 5, 10, 20]
ACC = [67.9, 67.2, 65.9, 63.6, 57.4]                      # the Note's table (Notebook section 5)
fig = go.Figure(go.Scatter(x=SHIFT, y=ACC, mode="lines+markers+text", text=[f"{a}%" for a in ACC],
                           textposition=["top center", "bottom right", "top right", "top right", "top right"], line=dict(color=BLUE, width=4), marker=dict(size=13),
                           textfont=dict(size=20)))
fig.add_hline(y=50, line=dict(color=GREY, width=2, dash="dash"), annotation_text="guessing: 50%",
              annotation_position="bottom right", annotation_font_size=18)
fig.update_layout(template="simple_white", width=1000, height=420, font=dict(FONT, size=20), showlegend=False,
                  xaxis=dict(title="shift: blank positions added at the start (every word still there)", range=[-1, 23]),
                  yaxis=dict(title="test accuracy (%)", range=[45, 72]), margin=dict(l=80, r=20, t=20, b=70))
fig.write_image(here / "shift_accuracy.png", scale=2)
fig.write_image(here / "shift_accuracy.pdf")
