"""Constructing Family_size = SibSp + Parch + 1, row by row, on six Titanic passengers (rows 0, 2, 7, 13, 25, 27).
Then each size is grouped into Family_type (alone 1, small 2 to 4, large 5 or more). Plotly table frames -> GIF."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from anim import save_gif, FONT

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic.csv").iloc[[0, 2, 7, 13, 25, 27]]
df["Name"] = df.Name.str.split(",").str[0]
F = df.SibSp + df.Parch + 1
assert F.iloc[0] == 2


TYPE = ["alone" if f == 1 else "small" if f <= 4 else "large" for f in F]      # the grouping of section 3.3
CODE = {"alone": 0, "small": 1, "large": 2}


def frame(k):
    """k = 0: empty; 1..6: Family_size row by row; 7..12: Family_type row by row."""
    n, t = min(k, 6), max(k - 6, 0)
    vals = [df.Name, df.SibSp, df.Parch,
            [f"{a} + {b} + 1 = <b>{f}</b>" if i < n else "" for i, (a, b, f) in enumerate(zip(df.SibSp, df.Parch, F))],
            [f"{ty} (<b>{CODE[ty]}</b>)" if i < t else "" for i, ty in enumerate(TYPE)]]
    hot = lambda j: ["#ffe2c4" if i == j else "white" for i in range(6)]
    fill = [["white"] * 6, ["#eef3f9"] * 6, ["#eef3f9"] * 6, hot(k - 1 if k <= 6 else -1), hot(t - 1)]
    fig = go.Figure(go.Table(columnwidth=[1.1, 0.6, 0.6, 1.5, 1.1],
                             header=dict(values=["passenger (surname)", "SibSp", "Parch", "Family_size = SibSp + Parch + 1",
                                                 "Family_type"],
                                         fill_color="#4C78A8", font=dict(color="white", size=19), height=40),
                             cells=dict(values=vals, fill_color=fill, font=dict(size=19), height=38)))
    title = ("Constructing a new feature from two old ones" if k == 0 else f"row {k}: family size {F.iloc[k - 1]}" if k <= 6
             else f"row {t}: size {F.iloc[t - 1]} is {'1' if TYPE[t - 1] == 'alone' else '2 to 4' if TYPE[t - 1] == 'small' else '5 or more'}, so {TYPE[t - 1]}")
    fig.update_layout(width=1300, height=360, font=FONT, margin=dict(l=10, r=10, t=60, b=0), title=dict(text=title, x=0.5))
    return fig


if __name__ == "__main__":
    save_gif([frame(k) for k in range(13)], "family_build", here, keys=[6, 12], fps=1, holds=[3] + [2] * 11 + [6], cols=1, width=900)
