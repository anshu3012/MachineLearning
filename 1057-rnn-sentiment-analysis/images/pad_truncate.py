"""What pad_sequences(maxlen=50) does to real IMDB training reviews: long reviews lose their start
(truncating="pre", the default) and keep their last 50 words; a short review gets zeros in front (padding="pre").
Lengths from data/pad_examples.csv (keras.datasets.imdb.load_data order). Plotly."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, RED, FONT

here = Path(__file__).parent
P = pd.read_csv(here.parent / "data" / "pad_examples.csv")
assert P.length.tolist() == [218, 189, 141, 11]          # the Note's numbers
M = 50
fig = make_subplots(rows=1, cols=2, column_widths=[0.72, 0.28], horizontal_spacing=0.06,
                    subplot_titles=("the review as loaded (words)", "after pad_sequences(maxlen=50)"))
labels = [f"{r.review}: {r.length} words" for r in P.itertuples()]
cut = [max(n - M, 0) for n in P.length]
kept = [min(n, M) for n in P.length]
pad = [max(M - n, 0) for n in P.length]
fig.add_bar(y=labels, x=cut, orientation="h", marker_color=RED, name="cut off (the start)", row=1, col=1,
            text=[f"{c} cut" if c else "" for c in cut], textposition="inside", insidetextanchor="middle")
fig.add_bar(y=labels, x=kept, orientation="h", marker_color=BLUE, name="kept (the last 50 words)", row=1, col=1,
            showlegend=False)
fig.add_bar(y=labels, x=pad, orientation="h", marker_color="#C9C9C9", name="zeros added in front", row=1, col=2,
            text=[f"{p} zeros" if p else "" for p in pad], textposition="inside", insidetextanchor="middle")
fig.add_bar(y=labels, x=kept, orientation="h", marker_color=BLUE, name="words kept", row=1, col=2,
            text=[f"{k}" for k in kept], textposition="inside", insidetextanchor="middle")
fig.update_yaxes(autorange="reversed")
fig.update_yaxes(showticklabels=False, row=1, col=2)
fig.update_xaxes(range=[0, 230], row=1, col=1)
fig.update_xaxes(range=[0, 50], tickvals=[0, 25, 50], row=1, col=2)
fig.update_layout(barmode="stack", template="simple_white", width=1100, height=420, font=dict(FONT, size=19),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.12), margin=dict(l=20, r=20, t=50, b=80))
fig.write_image(here / "pad_truncate.png", scale=2)
fig.write_image(here / "pad_truncate.pdf")
