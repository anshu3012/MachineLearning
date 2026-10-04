"""Section 5: why next-word prediction is classification. (a) A regression output such as 2.7 falls between the
indices of "the" (2) and "and" (3) and names no word. (b) For the prefix "but", the one-hot target (the real next
word "the") against the model's softmax probabilities for its five most likely words (data/typing.csv, seed 0). Plotly."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, RED, GREEN, GREY, FONT

here = Path(__file__).parent
T = pd.read_csv(here.parent / "data" / "typing.csv").query("step == 1").sort_values("rank")
assert T.prefix.iloc[0] == "but" and T.next_word.iloc[0] == "the" and round(T.p.iloc[0], 3) == 0.232
fig = make_subplots(rows=1, cols=2, column_widths=[0.42, 0.58], horizontal_spacing=0.1,
                    subplot_titles=("(a) regression: one number", '(b) classification: after "but"'))
words = {2: "the", 3: "and"}                          # the indices given in section 4.2
fig.add_scatter(x=list(words), y=[0] * 2, mode="markers+text", text=[f"{i}: {w}" for i, w in words.items()],
                textposition="top center", marker=dict(size=14, color=GREY), textfont=dict(size=19), showlegend=False,
                row=1, col=1)
fig.add_scatter(x=[2.7], y=[0], mode="markers+text", text=["2.7: no word"], textposition="bottom center",
                marker=dict(size=18, color=RED, symbol="x"), textfont=dict(size=19, color=RED), showlegend=False,
                row=1, col=1)
fig.update_xaxes(range=[1.2, 3.8], dtick=1, title="word index", row=1, col=1)
fig.update_yaxes(visible=False, range=[-1, 1], row=1, col=1)
fig.add_bar(x=T.word, y=(T.word == "the").astype(int), name="one-hot target (the real next word)",
            marker_color="rgba(84,162,75,0.35)", marker_line=dict(color=GREEN, width=2), row=1, col=2)
fig.add_bar(x=T.word, y=T.p, name="softmax output (probabilities)", marker_color=BLUE, row=1, col=2,
            text=[f"{p:.2f}" for p in T.p], textposition="outside")
fig.update_yaxes(range=[0, 1.1], title="value", row=1, col=2)
fig.update_xaxes(title="the five most likely words of 3,000", row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=440, font=dict(FONT, size=19), barmode="overlay",
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.25), margin=dict(l=40, r=20, t=50, b=110))
fig.write_image(here / "onehot_softmax.png", scale=2)
fig.write_image(here / "onehot_softmax.pdf")
