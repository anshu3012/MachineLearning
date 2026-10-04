"""What a test compares, as a picture. Left: the Note's five new-style lessons (7, 9, 5, 11, 13 minutes).
Right: five steadier lessons with the same mean 9 (8, 9, 8, 10, 10), made up for contrast. A horizontal line
starts at the null value 6 and moves to the sample mean 9; the bars are each lesson's distance to the line.
Left the total distance falls only from 17 to 12; right it falls from 15 to 4.
Plotly frames (points fixed, a line and bars changing) -> mean_fit.gif, _frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from anim import save_gif, FONT, BLUE, ORANGE, RED, GREY

here = Path(__file__).parent
REAL = np.array([7, 9, 5, 11, 13.0])
STEADY = np.array([8, 9, 8, 10, 10.0])
dist = lambda s, b: np.abs(s - b).sum()
assert REAL.mean() == STEADY.mean() == 9 and (dist(REAL, 6), dist(REAL, 9), dist(STEADY, 6), dist(STEADY, 9)) == (17, 12, 15, 4)
P_REAL = stats.ttest_1samp(REAL, 6, alternative="greater").pvalue        # 0.051, as in the Note
P_STEADY = stats.ttest_1samp(STEADY, 6, alternative="greater").pvalue    # 0.001


def frame(b):
    name = "H0: mean 6" if b == 6 else ("the lessons' own mean 9" if b == 9 else "moving the line")
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08, subplot_titles=[
        f"our five lessons<br>total distance <b>{dist(REAL, b):g}</b>",
        f"five steadier lessons<br>total distance <b>{dist(STEADY, b):g}</b>"])
    for j, s in enumerate((REAL, STEADY), start=1):
        for i, v in enumerate(s):
            fig.add_scatter(x=[i + 1, i + 1], y=[b, v], mode="lines", line=dict(color=ORANGE, width=8), row=1, col=j)
        fig.add_scatter(x=np.arange(1, 6), y=s, mode="markers", marker=dict(color=BLUE, size=20), row=1, col=j)
        fig.add_scatter(x=[0.4, 5.6], y=[b, b], mode="lines", line=dict(color=RED if b == 6 else GREY, width=4), row=1, col=j)
        fig.update_xaxes(title_text="lesson", range=[0.4, 5.6], dtick=1, row=1, col=j)
        fig.update_yaxes(range=[3.5, 14], row=1, col=j)
    fig.update_yaxes(title_text="view duration (minutes)", row=1, col=1)
    fig.update_annotations(font_size=24)
    fig.update_layout(template="simple_white", width=1300, height=680, font=FONT, showlegend=False,
                      title=dict(text=f"<b>Line at {b:g}</b>: {name}", x=0.5), margin=dict(l=80, r=30, t=170, b=80))
    return fig


if __name__ == "__main__":
    save_gif([frame(b) for b in (6, 7, 8, 9)], "mean_fit", here, keys=[0, 3], fps=1, holds=[4, 2, 2, 6], cols=1, width=900)
    print(P_REAL, P_STEADY, stats.ttest_1samp(STEADY, 6).statistic)
