"""OrdinalEncoder at work on the Note's customer data: fit learns the two category lists from the 40 training rows,
then transform fills in the codes row by row (first six training rows, then two test rows with the same lists).
Plotly table frames -> GIF."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from anim import save_gif, FONT

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "customer.csv").iloc[:, 2:]
Xtr, Xte, _, _ = train_test_split(df.iloc[:, 0:2], df.iloc[:, -1], test_size=0.2, random_state=0)
oe = OrdinalEncoder(categories=[["Poor", "Average", "Good"], ["School", "UG", "PG"]]).fit(Xtr)
A, B = oe.transform(Xtr), oe.transform(Xte)
assert len(Xtr) == 40 and Xtr.iloc[:4].values.tolist() == [["Good", "PG"], ["Poor", "School"], ["Poor", "PG"], ["Average", "School"]]
assert A[:4].tolist() == [[2, 2], [0, 0], [0, 2], [1, 0]]
rows = [("train", *Xtr.iloc[i], *A[i]) for i in range(6)] + [("test", *Xte.iloc[i], *B[i]) for i in range(2)]
DARK = {"#e8710a", "#3a6ea5"}
CODE = {"Poor": "#fde0c5", "Average": "#f9b36b", "Good": "#e8710a", "School": "#d6e4f0", "UG": "#8fb3d9", "PG": "#3a6ea5"}


def frame(k, head):
    cells = [[r[0] for r in rows], [r[1] for r in rows], [r[2] for r in rows],
             [f"{int(r[3])}" if i < k else "" for i, r in enumerate(rows)],
             [f"{int(r[4])}" if i < k else "" for i, r in enumerate(rows)]]
    fill = [["#f2f2f2" if r[0] == "train" else "#e8e8e8" for r in rows],
            [CODE[r[1]] for r in rows], [CODE[r[2]] for r in rows],
            [CODE[r[1]] if i < k else "white" for i, r in enumerate(rows)],
            [CODE[r[2]] if i < k else "white" for i, r in enumerate(rows)]]
    fig = go.Figure(go.Table(columnwidth=[60, 90, 90, 90, 90],
                             header=dict(values=["set", "review", "education", "review code", "education code"],
                                         fill_color="#4C78A8", font=dict(color="white", size=22), height=44),
                             cells=dict(values=cells, fill_color=fill, height=42,
                                        font=dict(size=22, color=[[("white" if c in DARK else "black") for c in col] for col in fill]))))
    fig.update_layout(width=1000, height=540, font=FONT, margin=dict(l=20, r=20, t=130, b=0),
                      title=dict(text=head, x=0.5, y=0.95))
    return fig


LISTS = "review: Poor → 0, Average → 1, Good → 2<br>education: School → 0, UG → 1, PG → 2"
if __name__ == "__main__":
    figs = [frame(0, "<b>fit</b> on the 40 training rows learns, in our order:<br>" + LISTS)]
    figs += [frame(k, f"<b>transform</b>: row {k} replaced by its positions<br>" + LISTS) for k in range(1, 9)]
    save_gif(figs, "encode_rows", here, keys=[0, 8], fps=1, holds=[4] + [2] * 7 + [6], cols=2)
