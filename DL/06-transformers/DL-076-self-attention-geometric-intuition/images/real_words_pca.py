"""Section 3: real word vectors as points. 17 words: four groups of 4 and "bank", their 100-number GloVe vectors projected onto
their first 2 principal components (the Notebook's last section). Data: data/word_pca.csv. Plotly (a scatter chart)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, ORANGE, GREEN, PURPLE, RED, FONT

here = Path(__file__).parent
d = pd.read_csv(here.parent / "data" / "word_pca.csv")
COL = {"chemistry": PURPLE, "formal": ORANGE, "money": GREEN, "river": BLUE, "bank": RED}
NAME = {"chemistry": "chemistry words", "formal": "formal linking words", "money": "money words",
        "river": "river words", "bank": "bank"}
POS = {"chloride": "top right", "sodium": "middle left", "oxide": "middle right", "magnesium": "bottom center",
       "therefore": "top center", "consequently": "middle left", "indeed": "top right", "although": "bottom right",
       "loan": "top left", "credit": "top right", "cash": "middle left", "money": "bottom left", "bank": "bottom right",
       "stream": "middle right", "lake": "middle left", "valley": "middle right", "river": "bottom center"}
fig = go.Figure()
for g, part in d.groupby("group", sort=False):
    fig.add_scatter(x=part.pc1, y=part.pc2, mode="markers+text", text=part.word, name=NAME[g],
                    textposition=[POS[w] for w in part.word],
                    marker=dict(size=16 if g == "bank" else 11, color=COL[g], symbol="star" if g == "bank" else "circle"),
                    textfont=dict(size=17, color=COL[g]))
fig.update_layout(template="simple_white", width=1000, height=720, font=dict(FONT, size=18),
                  xaxis=dict(title="principal component 1", zeroline=False, range=[-7, 5]),
                  yaxis=dict(title="principal component 2", zeroline=False),
                  legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center"), margin=dict(l=70, r=20, t=50, b=60))
fig.write_image(here / "real_words_pca.png", scale=2)
fig.write_image(here / "real_words_pca.pdf")
