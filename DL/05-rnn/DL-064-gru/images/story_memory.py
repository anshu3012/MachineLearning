"""Section 6: the hidden state of the King Vikram story as a heat map, one row per sentence, one column per aspect.
Values are the Note's teaching table; row 4 is the one computed in section 8.4.
Run: python story_memory.py  -> story_memory.png (Plotly heat map: a table of numbers read as colour)"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
ASPECTS = ["power", "conflict", "tragedy", "revenge"]
SENT = ["1 Vikram, strong king", "2 enemy king Kali", "3 Kali kills Vikram", "4 son grows up strong",
        "5 son attacks, is killed", "6 grandson fights Kali", "7 grandson kills Kali"]
H = np.array([[0.9, 0.0, 0.0, 0.0], [1.0, 0.5, 0.0, 0.0], [0.6, 0.6, 0.7, 0.1], [0.61, 0.32, 0.22, 0.12],
              [0.8, 0.8, 0.9, 0.3], [1.0, 0.9, 0.7, 0.7], [0.7, 0.8, 0.3, 1.0]])
h3, h4 = H[2], H[3]
z, cand = np.array([0.1, 0.7, 0.8, 0.2]), np.array([0.7, 0.2, 0.1, 0.2])
assert np.allclose(np.round((1 - z) * h3 + z * cand, 2), h4)                 # row 4 = section 8.4

fig = go.Figure(go.Heatmap(z=H, x=ASPECTS, y=SENT, colorscale=[[0, "#FFFFFF"], [1, "#4C78A8"]], zmin=0, zmax=1,
                           text=[[f"{v:g}" for v in row] for row in H], texttemplate="%{text}",
                           textfont=dict(size=22), xgap=3, ygap=3, colorbar=dict(title="value")))
fig.update_yaxes(autorange="reversed")
fig.update_xaxes(side="top")
fig.update_layout(template="simple_white", width=1000, height=600, font=dict(family="Latin Modern Roman", size=22),
                  title=dict(text="h<sub>t</sub> after each sentence (h<sub>0</sub> = 0)", x=0.5, y=0.98),
                  margin=dict(l=20, r=20, t=110, b=20))

if __name__ == "__main__":
    fig.write_image(HERE / "story_memory.png", scale=2)
