"""One-hot encoding of the Note's colour column, built step by step: one new column per category, the 1s filled in
row by row, then the first column dropped (0, 0 now means Yellow). Rows as in onehot_colors.tex.
Table build-up after StatQuest, "One-Hot, Label, Target and K-Fold Target Encoding" (01:30-02:30). Plotly frames -> GIF."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from anim import save_gif, FONT

here = Path(__file__).parent
ROWS = ["Yellow", "Blue", "Red", "Blue"]
CATS = ["Yellow", "Blue", "Red"]
NAMES = {"Yellow": "color_Y", "Blue": "color_B", "Red": "color_R"}
TINT = {"Yellow": "#fff2b3", "Blue": "#cfe0f3", "Red": "#f7c9c9"}
want = pd.get_dummies(pd.Series(ROWS), dtype=int)[CATS]
assert want.values.tolist() == [[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 1, 0]]


def frame(n_cols, n_rows, head, dropped=False):
    """n_cols: how many new columns exist; n_rows: how many rows are filled in."""
    cats = CATS[1:] if dropped else CATS[:n_cols]
    values = [ROWS] + [[str(want[c][i]) if i < n_rows else "" for i in range(4)] for c in cats]
    fill = [[TINT[r] for r in ROWS]] + [[("#f9b36b" if want[c][i] else "#f2f2f2") if i < n_rows else "white"
                                         for i in range(4)] for c in cats]
    fig = go.Figure(go.Table(columnwidth=[90] * (1 + len(cats)),
                             header=dict(values=["color"] + [NAMES[c] for c in cats], fill_color="#4C78A8",
                                         font=dict(color="white", size=24), height=48),
                             cells=dict(values=values, fill_color=fill, height=48, font=dict(size=24, color="black"))))
    fig.update_layout(width=1000, height=400, font=FONT, margin=dict(l=20, r=20, t=110, b=0),
                      title=dict(text=head, x=0.5, y=0.93))
    return fig


if __name__ == "__main__":
    figs = [frame(0, 0, "<b>A nominal column:</b> three colours, no order")]
    figs += [frame(k, 0, f"<b>One new column per category</b> ({k} of 3)") for k in (1, 2, 3)]
    figs += [frame(3, k, f"<b>Row {k} is {ROWS[k - 1]}:</b> 1 in {NAMES[ROWS[k - 1]]}, 0 elsewhere") for k in (1, 2, 3, 4)]
    figs += [frame(3, 4, "<b>Drop the first column:</b> 0, 0 now means Yellow", dropped=True)]
    save_gif(figs, "onehot_fill", here, keys=[0, 5, 7, 8], fps=1, holds=[3, 1, 1, 2, 2, 2, 2, 4, 6], cols=2)
