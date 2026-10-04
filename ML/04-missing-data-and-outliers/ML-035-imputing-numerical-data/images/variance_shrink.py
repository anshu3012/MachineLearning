"""Why the variance shrinks: the 712 training ages before and after mean imputation, with a band of one standard
deviation either side of the mean. The 148 filled values all sit at the mean and add no distance, so the standard
deviation falls from 14.30 (variance 204.35) to 12.72 (161.81). Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from anim import save_gif, FONT, BLUE, RED

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic_toy.csv")
Xtr, _, _, _ = train_test_split(df.drop(columns="Survived"), df["Survived"], test_size=0.2, random_state=2)
age = Xtr.Age
filled = age.fillna(age.mean())
assert round(age.var(), 2) == 204.35 and round(filled.var(), 2) == 161.81


def frame(after):
    v = filled if after else age.dropna()
    m, s = v.mean(), v.std()
    fig = go.Figure()
    fig.add_vrect(x0=m - s, x1=m + s, fillcolor="rgba(84,162,75,0.25)", opacity=1, layer="below", line_width=0)
    fig.add_histogram(x=age.dropna(), xbins=dict(start=0, end=82, size=2), marker_color=BLUE, name="known ages")
    if after:
        fig.add_histogram(x=filled[age.isna()], xbins=dict(start=0, end=82, size=2), marker_color=RED, name="148 filled ages")
    fig.add_annotation(x=60, y=150, text=f"green band: mean ± 1 SD<br>{m - s:.1f} to {m + s:.1f}<br>SD {s:.2f}, variance {s * s:.2f}",
                       showarrow=False, font=dict(size=20, color="#2e7d32"))
    fig.update_layout(template="simple_white", width=1100, height=540, font=FONT, barmode="stack", bargap=0.05,
                      title=dict(text="<b>after mean imputation</b>: 148 values pile up at the mean" if after else
                                 "<b>before</b>: the 564 known training ages", x=0.5),
                      xaxis=dict(title="Age", range=[0, 82]), yaxis=dict(title="passengers", range=[0, 185]),
                      legend=dict(x=0.62, y=0.6), margin=dict(l=80, r=30, t=80, b=70))
    return fig


if __name__ == "__main__":
    save_gif([frame(False), frame(True)], "variance_shrink", here, keys=[0, 1], fps=1, holds=[4, 6])
