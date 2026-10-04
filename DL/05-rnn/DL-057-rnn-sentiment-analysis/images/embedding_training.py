"""The 2-number embedding of the IMDB model (seed 0) while it trains: the 24 words of embedding_words.png before
training (epoch 0) and after each of the 5 epochs, from data/embedding_epochs.csv (Notebook). Before training the
words sit in one random cloud; training pulls positive and negative words apart.
Idea after StatQuest, "Word Embedding and Word2Vec, Clearly Explained!!!" (words plotted on the plane of their
embedding weights, before and after training); our own model and data.
Tool: Plotly frames (points moving between epochs). -> GIF + key-frame grid."""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from common import GREEN, RED, GREY, FONT
from gifkit import save_gif

HERE = Path(__file__).parent
D = pd.read_csv(HERE.parent / "data" / "embedding_epochs.csv")
final = pd.read_csv(HERE.parent / "data" / "embedding_words.csv").set_index("word")
last = D[D.epoch == 5].set_index("word")
assert (abs(last.e1 - final.e1) < 1e-3).all() and (abs(last.e2 - final.e2) < 1e-3).all()   # ends at Figure 6
LABELS = {"great": "top center", "excellent": "bottom center", "worst": "top center",
          "waste": "bottom center", "bad": "bottom center", "movie": "top center"}


def frame(ep):
    d = D[D.epoch == ep]
    fig = go.Figure()
    for g, col in (("positive", GREEN), ("negative", RED), ("neutral", GREY)):
        q = d[d.group == g]
        show = ep > 0
        fig.add_scatter(x=q.e1, y=q.e2, mode="markers+text" if show else "markers", name=g,
                        text=[w if w in LABELS else "" for w in q.word],
                        textposition=[LABELS.get(w, "top center") for w in q.word],
                        marker=dict(size=14, color=col), textfont=dict(color=col, size=20))
    title = "before training: random numbers, the groups are mixed" if ep == 0 else \
        f"after epoch <b>{ep}</b>: positive and negative words move apart"
    fig.update_layout(template="simple_white", width=1000, height=620, font=dict(FONT, size=20),
                      title=dict(text=title, x=0.5, y=0.96),
                      xaxis=dict(title="embedding number 1", range=[-0.62, 0.4], zeroline=True, zerolinecolor="#DDDDDD"),
                      yaxis=dict(title="embedding number 2", range=[-0.25, 0.36], zeroline=True, zerolinecolor="#DDDDDD"),
                      legend=dict(x=1.0, y=1.0, xanchor="right", bgcolor="rgba(255,255,255,0.8)"),
                      margin=dict(l=80, r=20, t=70, b=70))
    return fig


if __name__ == "__main__":
    save_gif([frame(e) for e in range(6)], "embedding_training", HERE, keys=[0, 1, 3, 5], fps=0.8, cols=2,
             holds=[2, 1, 1, 1, 1, 5])
