"""Three stills for the Note's sections: the training curve of the model (section 4), step 1 of translating
"we're friends ." (section 5), and test BLEU with and without the mask at inference for 3 trained models (section 7).
Data: data/training_history.csv, data/decode_steps.csv, data/decode_cross.csv, data/mask_at_inference.csv (Notebook).
Run: python inference_stills.py -> training_curve.png, step1.png, mask_bleu.png (Plotly)"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREY, FONT

HERE = Path(__file__).parent
D = HERE.parent / "data"
F = dict(FONT, size=19)

h = pd.read_csv(D / "training_history.csv")
fig = go.Figure()
fig.add_trace(go.Scatter(x=h.epoch + 1, y=h.loss, name="training loss", line=dict(color=BLUE, width=3)))
fig.add_trace(go.Scatter(x=h.epoch + 1, y=h.val_loss, name="validation loss", line=dict(color=ORANGE, width=3)))
fig.update_layout(template="simple_white", width=850, height=450, font=F, xaxis_title="epoch",
                  yaxis_title="cross-entropy loss", legend=dict(x=0.55, y=0.95), margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(HERE / "training_curve.png", scale=2)

SENT = "we're friends ."
s = pd.read_csv(D / "decode_steps.csv")
s = s[(s.sentence == SENT) & (s.step == 1)].sort_values("rank", ascending=False)
c = pd.read_csv(D / "decode_cross.csv")
c = c[(c.sentence == SENT) & (c.step == 1)]
fig = make_subplots(1, 2, horizontal_spacing=0.18, subplot_titles=("5 most likely first words",
                                                                   "cross-attention of &lt;start&gt;"))
fig.add_trace(go.Bar(x=s.prob, y=s.word, orientation="h", marker_color=[ORANGE if r == 1 else GREY for r in s["rank"]],
                     text=[f"{p:.3f}" for p in s.prob], textposition="outside"), 1, 1)
fig.add_trace(go.Bar(x=c.english, y=c.weight, marker_color=BLUE, text=[f"{w:.2f}" for w in c.weight],
                     textposition="outside"), 1, 2)
fig.update_xaxes(range=[0, 1.3], title="probability", row=1, col=1)
fig.update_yaxes(range=[0, 1.1], title="weight", row=1, col=2)
fig.update_layout(template="simple_white", width=1000, height=440, font=F, showlegend=False,
                  margin=dict(l=80, r=20, t=50, b=60))
fig.write_image(HERE / "step1.png", scale=2)

m = pd.read_csv(D / "mask_at_inference.csv")
lab = [f"model {k + 1}" for k in range(len(m))]
fig = go.Figure()
fig.add_trace(go.Bar(x=lab, y=m.bleu_with, name="mask on (as in training)", marker_color=BLUE,
                     text=[f"{v:.1f}" for v in m.bleu_with], textposition="outside"))
fig.add_trace(go.Bar(x=lab, y=m.bleu_without, name="mask off", marker_color=GREY,
                     text=[f"{v:.1f}" for v in m.bleu_without], textposition="outside"))
fig.update_layout(template="simple_white", width=800, height=450, font=F, barmode="group", yaxis=dict(title="test BLEU", range=[0, 50]),
                  legend=dict(orientation="h", x=0, y=1.12), margin=dict(l=70, r=20, t=50, b=50))
fig.write_image(HERE / "mask_bleu.png", scale=2)
