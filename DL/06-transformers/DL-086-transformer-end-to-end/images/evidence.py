"""Section 6: the measured effect of five parts of the transformer, each from the Note that measured it (values as in
the Note's table): the metric without the part, then with it. Similarity between words is better when lower.
Run: python evidence.py  -> evidence.png (Plotly dumbbell chart, one row per part)"""
from pathlib import Path

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from common import GREEN, GREY, RED

HERE = Path(__file__).parent
rows = [  # part, metric, without, with, Note
    ("attention", "test BLEU", 9.8, 25.7, "DL-069"),
    ("dot-product score", "test BLEU (vs additive)", 25.1, 31.6, "DL-070"),
    ("learned W<sub>Q</sub>, W<sub>K</sub>, W<sub>V</sub>", "IMDB accuracy", 0.69, 0.84, "DL-074"),
    ("residual connections", "similarity between words (lower is better)", 1.00, 0.09, "DL-081"),
    ("mask at inference", "BLEU", 38.9, 41.5, "DL-085")]
fig = make_subplots(1, len(rows), horizontal_spacing=0.06,
                    subplot_titles=[f"{p}<br>(Note {n})" for p, m, _, _, n in rows])
for i, (p, m, a, b, n) in enumerate(rows, start=1):
    fig.add_trace(go.Bar(x=["without", "with"], y=[a, b], marker_color=[RED, GREEN], text=[f"{a:g}", f"{b:g}"],
                         textposition="outside", showlegend=False), 1, i)
    fig.update_yaxes(range=[0, max(a, b) * 1.2], title_text=m, title_font_size=18, row=1, col=i)
fig.update_layout(template="simple_white", width=1400, height=520, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=70, r=20, t=90, b=50))
fig.update_annotations(font_size=19)

if __name__ == "__main__":
    fig.write_image(HERE / "evidence.png", scale=2)
