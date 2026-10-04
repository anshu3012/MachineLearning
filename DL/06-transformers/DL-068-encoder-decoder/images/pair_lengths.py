"""Section 3: input and output lengths are not tied. The 40,000 English-French training pairs of the Notebook
(English up to 8 tokens, French up to 10, punctuation counted) as a heatmap of English length against French
length. Only 30% of the pairs lie on the diagonal (same length). Data: data/pair_lengths.csv. Plotly."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from common import FONT

here = Path(__file__).parent
D = pd.read_csv(here.parent / "data" / "pair_lengths.csv")
assert D.pairs.sum() == 40000
same = D.loc[D.en_tokens == D.fr_tokens, "pairs"].sum() / 40000
assert round(same, 2) == 0.30
Z = D.pivot(index="fr_tokens", columns="en_tokens", values="pairs").reindex(index=range(2, 11), columns=range(2, 9))
fig = go.Figure(go.Heatmap(z=Z.values, x=Z.columns, y=Z.index, colorscale="Blues", colorbar=dict(title="pairs"),
                           text=np.where(np.isnan(Z.values), "", Z.fillna(0).astype(int).astype(str)),
                           texttemplate="%{text}", textfont=dict(size=13), xgap=2, ygap=2))
fig.add_scatter(x=[1.5, 8.5], y=[1.5, 8.5], mode="lines", line=dict(color="#E45756", width=3, dash="dash"),
                name=f"same length: {same:.0%} of the pairs")
fig.update_layout(template="simple_white", width=900, height=640, font=dict(FONT, size=19),
                  xaxis=dict(title="English sentence length (tokens)", dtick=1, range=[1.5, 8.5]),
                  yaxis=dict(title="French translation length (tokens)", dtick=1, range=[1.5, 10.5]),
                  legend=dict(x=0.02, y=0.98), margin=dict(l=80, r=20, t=20, b=70))
fig.write_image(here / "pair_lengths.png", scale=2)
fig.write_image(here / "pair_lengths.pdf")
