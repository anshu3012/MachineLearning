"""Cosine similarity of two phrases drawn as arrows. Axes: how often the phrase says "good" and "movie".
Repeating the words makes an arrow longer but does not turn it, so the angle and its cosine stay the same.
Tool: Plotly frames -> GIF (a few 2D arrows with number readouts). Idea after StatQuest, "Cosine Similarity"."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from anim import save_gif, FONT, BLUE, ORANGE, GREEN

here = Path(__file__).parent
WORDS = ("good", "movie")


def count(phrase):
    return np.array([phrase.split().count(w) for w in WORDS], float)


def cos(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


PAIRS = [("good movie", "good", "two phrases, two arrows"),
         ("good movie", "good good", "say “good” twice: the arrow grows, the angle stays"),
         ("good movie", "good good good", "three times: still the same angle"),
         ("good movie", "good movie good movie", "same words, repeated: angle 0"),
         ("movie", "good", "no shared word: a right angle")]
assert [round(cos(count(p), count(q)), 2) for p, q, _ in PAIRS] == [0.71, 0.71, 0.71, 1.0, 0.0]


def frame(p, q, head):
    a, b = count(p), count(q)
    c = cos(a, b)
    ang = np.degrees(np.arccos(np.clip(c, -1, 1)))
    fig = go.Figure()
    for v, col, wid in ((a, BLUE, 6), (b, ORANGE, 4)):          # thinner orange on top, so both show when they overlap
        fig.add_annotation(x=v[0], y=v[1], ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", arrowhead=3,
                           arrowwidth=wid, arrowcolor=col, text="")
    fig.add_annotation(x=a[0], y=a[1], text=f"“{p}”", showarrow=False, yshift=14, xshift=-80 if a[0] else 60,
                       font=dict(size=22, color=BLUE))
    fig.add_annotation(x=b[0], y=b[1], text=f"“{q}”", showarrow=False, yshift=-26 if b[1] == 0 else 24,
                       xshift=0 if b[1] == 0 else 150, font=dict(size=22, color="#c55a00"))
    t0, t1 = np.arctan2(b[1], b[0]), np.arctan2(a[1], a[0])
    if ang > 1:
        t = np.linspace(t0, t1, 30)
        fig.add_scatter(x=0.55 * np.cos(t), y=0.55 * np.sin(t), mode="lines", line=dict(color=GREEN, width=4))
    fig.add_annotation(x=2.2, y=2.75, showarrow=False, font=dict(size=28, color="#2e7d32"),
                       text=f"angle = {ang:.0f}°<br>cosine similarity = <b>{c:.2f}</b>")
    fig.update_layout(template="simple_white", width=900, height=760, font=FONT, showlegend=False,
                      title=dict(text=head, x=0.5),
                      xaxis=dict(title="count of “good”", range=[-0.3, 3.6], dtick=1, zeroline=True, zerolinewidth=2),
                      yaxis=dict(title="count of “movie”", range=[-0.5, 3.2], dtick=1, zeroline=True, zerolinewidth=2,
                                 scaleanchor="x"),
                      margin=dict(l=80, r=30, t=80, b=70))
    return fig


if __name__ == "__main__":
    save_gif([frame(*p) for p in PAIRS], "phrase_angle", here, keys=[0, 2, 3, 4], fps=1, holds=[3, 3, 3, 4, 6])
