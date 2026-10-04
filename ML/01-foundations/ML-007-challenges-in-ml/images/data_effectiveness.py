"""With enough data, different algorithms end up performing about the same. Concept curves, not measurements."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
GREY = "#6B6B6B"
size = np.logspace(0, 3, 200)                    # 1 to 1000 (millions of words, say)
fig = go.Figure()
for name, colour, start, speed in [("Algorithm A", "#4C78A8", 0.78, 0.9), ("Algorithm B", "#F58518", 0.72, 1.1),
                                   ("Algorithm C", "#54A24B", 0.66, 1.3), ("Algorithm D", "#E45756", 0.60, 1.5)]:
    acc = 0.97 - (0.97 - start) * size ** (-0.35 * speed)
    fig.add_trace(go.Scatter(x=size, y=acc, mode="lines", name=name, line=dict(color=colour, width=4)))
fig.add_annotation(x=np.log10(3), y=0.69, text="little data:<br>big differences", showarrow=False, font=dict(size=16, color=GREY))
fig.add_annotation(x=np.log10(400), y=0.90, text="lots of data:<br>all about the same", showarrow=False, font=dict(size=16, color=GREY))
fig.update_layout(template="simple_white", width=950, height=500, font=dict(family="Latin Modern Roman", size=17),
                  title=dict(text="With enough data, the choice of algorithm matters less", x=0.5),
                  xaxis=dict(title="Amount of training data (log scale)", type="log", showticklabels=False, ticks=""),
                  yaxis=dict(title="Accuracy", showticklabels=False, ticks="", range=[0.55, 1.0]),
                  legend=dict(x=0.02, y=0.98), margin=dict(l=70, r=30, t=70, b=60))
fig.add_annotation(x=3, y=0.58, xanchor="right", showarrow=False, text="illustration, not real measurements",
                   font=dict(size=13, color=GREY))
fig.write_image(here / "data_effectiveness.png", scale=2)
fig.write_image(here / "data_effectiveness.pdf")
