"""Section 4: the two counting ideas. Left: the raw index grows without limit (a 100,000-word book). Right: index
divided by the sentence length stays between 0 and 1, but the second word gets 1.0 in "thank you" and 0.5 in
"Rahul killed the lion". Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import RED, BLUE, GREEN, FONT

here = Path(__file__).parent
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.14,
                    subplot_titles=("count: 1, 2, 3, ... grows without limit", "count / length: position 2 changes value"))
p = np.array([1, 10, 100, 1000, 10000, 100000])
fig.add_scatter(x=p, y=p, mode="lines+markers", line=dict(color=RED, width=4), showlegend=False, row=1, col=1)
fig.add_hrect(y0=-1, y1=1, fillcolor="rgba(84,162,75,0.25)", line_width=0, row=1, col=1)
fig.add_annotation(x=np.log10(20), y=np.log10(1.6), text="inputs a network likes: about -1 to 1", showarrow=False,
                   xanchor="left", font=dict(size=17, color=GREEN), row=1, col=1)
fig.add_annotation(x=5, y=5, text="last word of a<br>100,000-word book", showarrow=True, ax=-110, ay=10,
                   font=dict(size=17), row=1, col=1)
fig.update_xaxes(type="log", title="position", row=1, col=1)
fig.update_yaxes(type="log", title="value", range=[-0.3, 5.6], row=1, col=1)
for n, words, col in ((2, ["thank", "you"], BLUE), (4, ["Rahul", "killed", "the", "lion"], RED)):
    pos = np.arange(1, n + 1)
    assert (pos / n)[1] == {2: 1.0, 4: 0.5}[n]
    fig.add_scatter(x=pos, y=pos / n, mode="lines+markers+text", text=words, textposition="top left", name=f"{n}-word sentence",
                    line=dict(color=col, width=3), marker=dict(size=12), row=1, col=2)
fig.add_annotation(x=2, y=1.0, text="position 2 → 1.0", showarrow=True, ax=60, ay=30, font=dict(size=17, color=BLUE), row=1, col=2)
fig.add_annotation(x=2, y=0.5, text="position 2 → 0.5", showarrow=True, ax=60, ay=30, font=dict(size=17, color=RED), row=1, col=2)
fig.update_xaxes(title="position", dtick=1, range=[0.2, 4.6], row=1, col=2)
fig.update_yaxes(title="position / length", range=[0, 1.2], row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=440, font=dict(FONT, size=18),
                  legend=dict(x=0.86, y=0.12), margin=dict(l=60, r=20, t=50, b=60))
fig.write_image(here / "count_problems.png", scale=2)
fig.write_image(here / "count_problems.pdf")
