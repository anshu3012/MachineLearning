"""Table 2 of Vaswani et al. (2017): BLEU against training cost, English-to-German and English-to-French (Plotly scatter)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
POS = {(1, "Transformer (base model)"): "top right", (1, "Transformer (big)"): "top center",
       (1, "ConvS2S Ensemble"): "top center", (1, "GNMT + RL Ensemble"): "bottom center",
       (2, "Transformer (base model)"): "top right", (2, "Transformer (big)"): "top center",
       (2, "ConvS2S Ensemble"): "top center", (2, "GNMT + RL Ensemble"): "middle left",
       (2, "MoE"): "top left", (2, "ConvS2S"): "top right", (2, "Deep-Att + PosUnk Ensemble"): "bottom center"}
t = pd.read_csv(here.parent / "data" / "table2.csv")
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=("English → German", "English → French"))
for k, (b, c) in enumerate((("bleu_en_de", "cost_en_de"), ("bleu_en_fr", "cost_en_fr")), start=1):
    d = t.dropna(subset=[b, c])
    for _, r in d.iterrows():
        tr = r.model.startswith("Transformer")
        fig.add_trace(go.Scatter(x=[r[c]], y=[r[b]], mode="markers+text", showlegend=False,
                                 marker=dict(size=13, color=ORANGE if tr else BLUE,
                                             symbol="circle-open" if r.ensemble else "circle",
                                             line=dict(width=3, color=ORANGE if tr else BLUE)),
                                 text=[r.model.replace("(base model)", "base").replace("(big)", "big")
                                       .replace(" Ensemble", " ensemble")],
                                 textposition=POS.get((k, r.model), "bottom center"),
                                 textfont=dict(size=13, color=ORANGE if tr else BLUE)), row=1, col=k)
    fig.update_xaxes(type="log", title_text="training cost (FLOPs, log scale)", dtick=1, exponentformat="power", row=1, col=k)
    fig.update_yaxes(title_text="BLEU (test, newstest2014)", row=1, col=k)
fig.update_yaxes(range=[24.0, 29.0], row=1, col=1)
fig.update_yaxes(range=[37.6, 42.4], row=1, col=2)
fig.update_xaxes(range=[18.3, 20.7], row=1, col=1)
fig.update_xaxes(range=[18.3, 21.6], row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=480, font=FONT, margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(font=FONT)
fig.write_image(here / "table2.png", scale=2)
fig.write_image(here / "table2.pdf")
