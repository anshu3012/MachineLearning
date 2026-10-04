"""Splitting the Type 1 column `Cabin`, one row at a time: the first character goes to cabin_cat (the deck), the first
run of digits to cabin_num. Rows 0, 1, 3, 27, 75, 292 of the Note's data, as in the table of section 5.
Our own design. Plotly table frames -> GIF."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from anim import save_gif, FONT

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic.csv").loc[[0, 1, 3, 27, 75, 292]]
num = pd.to_numeric(df["Cabin"].str.extract(r"(\d+)")[0]).astype("Int64")
cat = df["Cabin"].str[0]
assert df["Cabin"].tolist()[1:] == ["C85", "C123", "C23 C25 C27", "F G73", "D"] and num.tolist()[1:5] == [85, 123, 23, 73]
NUM, CAT, NOW = "#d6e4f0", "#fde0c5", "#ffe08a"
N = len(df)
show = lambda v: "NaN" if pd.isna(v) else str(v)
WHY = ["no cabin: both new columns stay empty", "letter C, digits 85", "letter C, digits 123",
       "three cabins: only the first letter and the first number are kept", "deck F is kept, although the cabin is G73",
       "a letter but no digits: cabin_num stays empty"]


def frame(k):
    """rows 0..k-1 split; row k-1 highlighted."""
    r = range(N)
    catc = [show(cat.iloc[i]) if i < k else "" for i in r]
    numc = [show(num.iloc[i]).replace("<NA>", "NaN") if i < k else "" for i in r]
    fig = go.Figure(go.Table(columnwidth=[0.5, 1.4, 1, 1],
                             header=dict(values=["row", "Cabin", "cabin_cat", "cabin_num"], fill_color="#4C78A8",
                                         font=dict(color="white", size=21), height=44),
                             cells=dict(values=[df.index, df["Cabin"].map(show), catc, numc], height=42, font=dict(size=22),
                                        fill_color=[["white"] * N, [NOW if i == k - 1 else "white" for i in r],
                                                    [CAT if i < k and catc[i] != "NaN" else "white" for i in r],
                                                    [NUM if i < k and numc[i] != "NaN" else "white" for i in r]])))
    head = ("The mixed column <b>Cabin</b>: a deck letter and a cabin number in one cell" if k == 0 else
            f"<b>{show(df['Cabin'].iloc[k - 1])}</b>: {WHY[k - 1]}")
    fig.update_layout(width=1100, height=430, font=FONT, title=dict(text=head, x=0.5, y=0.93),
                      margin=dict(l=10, r=10, t=80, b=0))
    return fig


if __name__ == "__main__":
    save_gif([frame(k) for k in range(N + 1)], "cabin_rows", here, keys=[2, 6], fps=1, holds=[3, 2, 2, 2, 3, 3, 6], cols=1,
             width=900)
