"""Test BLEU after each epoch: trained with teacher forcing vs trained on the model's own predictions, 3 seeds each,
mean in bold (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import GREEN, RED, FONT

here = Path(__file__).parent
a = pd.read_csv(here.parent / "data" / "teacher_forcing.csv")
fig = go.Figure()
for teacher, name, c in ((True, "teacher forcing (gold previous word)", GREEN), (False, "own prediction as next input", RED)):
    s = a[a.teacher == teacher]
    for _, g in s.groupby("seed"):
        fig.add_trace(go.Scatter(x=g.epoch, y=g.test_bleu, showlegend=False, opacity=0.35, line=dict(color=c, width=1.5)))
    m = s.groupby("epoch").test_bleu.mean()
    fig.add_trace(go.Scatter(x=m.index, y=m.values, name=name + " (mean of 3)", mode="lines+markers", line=dict(color=c, width=5)))
fig.update_layout(template="simple_white", width=950, height=450, font=FONT, xaxis=dict(title="epoch", dtick=1),
                  yaxis=dict(title="test BLEU (greedy decoding)", rangemode="tozero"),
                  legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.8)"), margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "teacher_forcing.png", scale=2)
fig.write_image(here / "teacher_forcing.pdf")
