"""The winning top-5 error of the ImageNet challenge, one year per frame, 2010 to 2015, with the depth of the
winning CNN where the Note cites it (8, 22, 152 layers) and one trained human's 5.1 percent.
Data: data/ilsvrc_winners.csv. Plotly frames: bars appear year by year.
Run: python ilsvrc_race.py -> ilsvrc_race.gif, ilsvrc_race_frames.png"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from common import BLUE, GREY, RED
from frames import save

HERE = Path(__file__).parent
w = pd.read_csv(HERE.parent / "data" / "ilsvrc_winners.csv")
DEPTH = {2012: "8 layers", 2014: "22 layers", 2015: "152 layers"}        # Krizhevsky 2012, Szegedy 2015, He 2016
NOTE = {2010: "2010: hand-made features win, 28.2%", 2011: "2011: hand-made features again, 25.8%",
        2012: "2012: a CNN, AlexNet, wins by almost 10 points", 2013: "2013: another CNN, 11.7%",
        2014: "2014: GoogLeNet, 22 layers, 6.7%", 2015: "2015: ResNet, 152 layers, below the human's 5.1%"}
FONT = dict(family="Latin Modern Roman", size=22)
w["name"] = w.entry.str.replace("SuperVision (AlexNet)", "AlexNet", regex=False)
assert list(w.year) == list(range(2010, 2016)) and w.top5_error.iloc[-1] < 5.1


def frame(k):
    """The first k winners shown."""
    d = w.iloc[:k]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=d.year, y=d.top5_error, width=0.62, cliponaxis=False,
                         marker_color=[GREY if kind != "CNN" else BLUE for kind in d.kind],
                         text=[f"{e:g}%<br>{n}" + (f"<br>{DEPTH[y]}" if y in DEPTH else "")
                               for e, n, y in zip(d.top5_error, d.name, d.year)],
                         textposition="outside", textfont=dict(size=19), constraintext="none"))
    fig.add_shape(type="line", x0=2009.5, x1=2015.5, y0=5.1, y1=5.1, layer="below", line=dict(color=RED, width=3, dash="dash"))
    fig.add_annotation(x=2015.45, y=33.5, xanchor="right", showarrow=False, font=dict(color=RED, size=20),
                       text="dashed: one trained human, 5.1%")
    fig.add_annotation(x=2015.45, y=30.5, xanchor="right", showarrow=False, font=dict(color=GREY, size=20),
                       text="grey: hand-made features;  <span style='color:#4C78A8'>blue: CNNs</span>")
    fig.update_layout(template="simple_white", width=1000, height=600, font=FONT, showlegend=False,
                      title=dict(text=NOTE[int(d.year.iloc[-1])] if k else "ImageNet challenge: the winner's top-5 error",
                                 x=0.5, font=dict(size=24)),
                      xaxis=dict(title="year", tickmode="array", tickvals=list(w.year), range=[2009.5, 2015.5]),
                      yaxis=dict(title="top-5 error of the winner (%)", range=[0, 38]),
                      margin=dict(l=80, r=20, t=70, b=70))
    return fig


if __name__ == "__main__":
    figs = [frame(k) for k in range(7)]
    seq = [0] * 2 + [k for k in range(1, 7) for _ in range(3)] + [6] * 6
    save("ilsvrc_race", figs, seq, [2, 3, 5, 6], HERE, fps=2)
