"""Cosine similarity of the Note's toy summaries A, B, C and B written twice (B2), from their word-count vectors.
B and C share one word: 0.29; A shares none with the others: 0; B and B2 point the same way: 1."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

here = Path(__file__).parent
texts = ["hi how are you", "my name is riya", "this is 2023", "my name is riya my name is riya"]
X = CountVectorizer().fit_transform(texts)
S = cosine_similarity(X)
assert round(S[1, 2], 2) == 0.29 and S[0, 1] == 0 and np.isclose(S[1, 3], 1)
lab = ["A: hi how are you", "B: my name is riya", "C: this is 2023", "B2: B written twice"]
fig = go.Figure(go.Heatmap(z=S, x=lab, y=lab, colorscale="Blues", zmin=0, zmax=1, text=np.round(S, 2), texttemplate="%{text}",
                           textfont=dict(size=22), colorbar=dict(title="cos θ")))
fig.update_layout(template="simple_white", width=1000, height=720, font=dict(family="Latin Modern Roman", size=18),
                  title=dict(text="Cosine similarity of word-count vectors", x=0.5),
                  yaxis=dict(autorange="reversed"), margin=dict(l=210, r=20, t=70, b=170))
fig.update_xaxes(tickangle=-30)
fig.write_image(here / "text_cosine.png", scale=2)
fig.write_image(here / "text_cosine.pdf")
