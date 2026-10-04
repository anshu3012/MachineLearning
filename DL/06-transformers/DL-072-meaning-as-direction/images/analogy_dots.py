"""Sections 5 and 7: each analogy question, with the cosine of the closest word among all candidates (grey) and of the
expected word (green if it ranks first once the question words are removed, red otherwise, with its rank).
One chart for GloVe, one for GPT-2's token-embedding table (data/analogies.csv, Notebook). Plotly."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import GREEN, RED, GREY, FONT

here = Path(__file__).parent
A = pd.read_csv(here.parent / "data" / "analogies.csv")
g = A[A.model == "GloVe"]
assert g.loc[g.target == "queen", "cos_target"].item() == 0.783 and g.loc[g.target == "sister", "rank_excl"].item() == 6
for model, name in (("GloVe", "analogy_glove"), ("GPT-2", "analogy_gpt2")):
    D = A[A.model == model].iloc[::-1]
    fig = go.Figure()
    for _, r in D.iterrows():
        fig.add_scatter(x=[r.cos_target, r.cos_top_all], y=[r.question] * 2, mode="lines",
                        line=dict(color="#C9C9C9", width=3), showlegend=False)
    fig.add_scatter(x=D.cos_top_all, y=D.question, mode="markers+text", marker=dict(size=13, color=GREY),
                    text=D.top_all.str.strip(), textposition="middle right", name="closest word, all candidates",
                    textfont=dict(size=15, color=GREY))
    ok = D.rank_excl == 1
    fig.add_scatter(x=D.cos_target, y=D.question, mode="markers", marker=dict(size=15, color=[GREEN if o else RED for o in ok]),
                    name="expected word (green: first once the question words are removed)")
    for _, r in D[~ok].iterrows():
        fig.add_annotation(x=r.cos_target, y=r.question, text=f"{r.target}: rank {r.rank_excl}", showarrow=False,
                           xanchor="right", xshift=-12, font=dict(size=15, color=RED))
    fig.update_layout(template="simple_white", width=1000, height=60 * len(D) + 140, font=dict(FONT, size=17),
                      title=dict(text=f"{model}: cosine of each result point with two words", x=0.5),
                      xaxis=dict(title="cosine similarity", range=[0.2, 1.02]),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.18), margin=dict(l=20, r=20, t=50, b=110))
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")
