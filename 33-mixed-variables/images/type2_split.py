"""Splitting the Type 2 column `number`, one row at a time: pd.to_numeric(errors="coerce") reads each value; a number
goes to number_numerical, a value it cannot read (A) goes to number_categorical, and the other cell stays empty.
First six rows of the Note's data. Plotly table frames -> GIF."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from anim import save_gif, FONT

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic.csv").head(6)
num = pd.to_numeric(df["number"], errors="coerce")
cat = df["number"].where(num.isna())
assert df["number"].tolist() == ["5", "3", "6", "3", "A", "2"] and num.isna().tolist() == [False] * 4 + [True, False]
NUM, CAT, NOW = "#d6e4f0", "#fde0c5", "#ffe08a"


def frame(k):
    """rows 0..k-1 split; row k-1 highlighted."""
    rows = list(range(6))
    numc = [f"{int(num[i])}" if i < k and not pd.isna(num[i]) else ("NaN" if i < k else "") for i in rows]
    catc = [cat[i] if i < k and isinstance(cat[i], str) else ("NaN" if i < k else "") for i in rows]
    fill_src = [NOW if i == k - 1 else "white" for i in rows]
    fill_num = [NUM if i < k and not pd.isna(num[i]) else "white" for i in rows]
    fill_cat = [CAT if i < k and isinstance(cat[i], str) else "white" for i in rows]
    fig = go.Figure(go.Table(columnwidth=[0.5, 1, 1.4, 1.4],
                             header=dict(values=["row", "number", "number_numerical", "number_categorical"],
                                         fill_color="#4C78A8", font=dict(color="white", size=21), height=44),
                             cells=dict(values=[rows, df["number"], numc, catc], height=42, font=dict(size=22),
                                        fill_color=[["white"] * 6, fill_src, fill_num, fill_cat])))
    if k == 0:
        head = "The mixed column <b>number</b>: digits, and A for alone"
    else:
        v = df["number"][k - 1]
        head = (f"row {k - 1}: <b>{v}</b> is a number → number_numerical" if not pd.isna(num[k - 1])
                else f"row {k - 1}: <b>{v}</b> is not a number → NaN, so it goes to number_categorical")
    fig.update_layout(width=1100, height=430, font=FONT, title=dict(text=head, x=0.5, y=0.93),
                      margin=dict(l=10, r=10, t=80, b=0))
    return fig


if __name__ == "__main__":
    save_gif([frame(k) for k in range(7)], "type2_split", here, keys=[4, 5], fps=1, holds=[3, 2, 2, 2, 2, 4, 6], cols=1,
             width=900)
