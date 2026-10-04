"""Section 5.3: words exchange information only in attention. In the Notebook's tiny encoder block (d_model 4,
2 heads, feed-forward hidden layer 8, Keras' seeded starting weights) we add 5 to every number of "you" and measure
how much each word's output changes (largest change over its numbers), in the attention sub-layer and in the
feed-forward sub-layer. Same construction and seeds as the Notebook, run on the CPU.
Run: python who_changes.py  -> who_changes.png (Plotly grouped bars)"""
import os
from pathlib import Path

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["CUDA_VISIBLE_DEVICES"] = ""
import keras
import numpy as np
import plotly.graph_objects as go

from common import BLUE, ORANGE

HERE = Path(__file__).parent


def positional_encoding(n_pos, d_model):
    pos, i = np.arange(n_pos)[:, None], np.arange(d_model // 2)[None, :]
    angle = pos / 10000 ** (2 * i / d_model)
    pe = np.zeros((n_pos, d_model))
    pe[:, 0::2], pe[:, 1::2] = np.sin(angle), np.cos(angle)
    return pe.astype("float32")


class EncoderBlock(keras.layers.Layer):                     # as in the Notebook
    def __init__(self, d_model, heads, d_ff, **kw):
        super().__init__(**kw)
        self.mha = keras.layers.MultiHeadAttention(num_heads=heads, key_dim=d_model // heads)
        self.norm1 = keras.layers.LayerNormalization()
        self.ffn1 = keras.layers.Dense(d_ff, activation="relu")
        self.ffn2 = keras.layers.Dense(d_model)
        self.norm2 = keras.layers.LayerNormalization()

    def call(self, x):
        z_norm = self.norm1(x + self.mha(x, x))
        return self.norm2(z_norm + self.ffn2(self.ffn1(z_norm)))


words = ["how", "are", "you"]
E = np.array([[0.5, 1.0, -0.5, 0.2], [-1.0, 0.3, 0.8, 0.4], [0.7, -0.6, 0.1, 0.9]], dtype="float32")
X4 = E + positional_encoding(3, 4)
keras.utils.set_random_seed(1)
tiny = EncoderBlock(4, 2, 8)
tiny(X4[None])
Z = tiny.mha(X4[None], X4[None])[0].numpy()
Z_norm = tiny.norm1(X4[None] + Z[None])[0].numpy()
ffn = lambda M: tiny.ffn2(tiny.ffn1(M[None]))[0].numpy()
changed = Z_norm.copy(); changed[2] += 5.0
d_ffn = np.abs(ffn(changed) - ffn(Z_norm)).max(axis=1)
Xc = X4.copy(); Xc[2] += 5.0
d_att = np.abs(tiny.mha(Xc[None], Xc[None])[0].numpy() - Z).max(axis=1)
assert np.allclose(Z[0].round(2), [1.08, 0.77, 0.39, -1.21]), Z[0]           # z_how of section 5.1
assert np.allclose(d_att.round(2), [1.59, 4.12, 5.75]) and np.allclose(d_ffn.round(2), [0, 0, 7.13]), (d_att, d_ffn)

fig = go.Figure()
for vals, name, c in ((d_att, "attention output", BLUE), (d_ffn, "feed-forward output", ORANGE)):
    fig.add_trace(go.Bar(x=words, y=vals, name=name, marker_color=c, text=[f"{v:.2f}" for v in vals],
                         textposition="outside"))
fig.update_layout(template="simple_white", barmode="group", width=1000, height=500,
                  font=dict(family="Latin Modern Roman", size=22),
                  title=dict(text='change in each word\'s output when only "you" changes', x=0.5, y=0.97),
                  yaxis=dict(title="largest change", range=[0, 8.5]),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=1.0, yanchor="bottom"),
                  margin=dict(l=80, r=20, t=110, b=50))

if __name__ == "__main__":
    fig.write_image(HERE / "who_changes.png", scale=2)
