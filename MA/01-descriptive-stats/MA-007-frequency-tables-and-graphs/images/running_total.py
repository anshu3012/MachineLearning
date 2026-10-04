"""Building the three tables of the vacation survey step by step: walk down the categories, add each frequency to
the running total (cumulative frequency) and divide by 200 (relative frequency). Plotly frames -> GIF."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from anim import save_gif, FONT, BLUE, ORANGE, GREY

here = Path(__file__).parent
t = pd.DataFrame({"vacation": ["Beach", "City", "Adventure", "Nature", "Cruise", "Other"],
                  "f": [60, 40, 30, 35, 20, 15]})
t["cum"] = t.f.cumsum()
assert t.f.sum() == 200 and t.cum.tolist() == [60, 100, 130, 165, 185, 200]   # the Note's table


def frame(k):
    """k categories counted so far (0..6)."""
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                        subplot_titles=["Frequency f", "Cumulative frequency F"])
    col = [ORANGE if i == k - 1 else (BLUE if i < k else "#e6e6e6") for i in range(6)]
    fig.add_bar(x=t.vacation, y=t.f, marker_color=col, row=1, col=1,
                text=[str(v) if i < k else "" for i, v in enumerate(t.f)], textposition="outside")
    fig.add_scatter(x=t.vacation[:k], y=t.cum[:k], mode="lines+markers+text", text=t.cum[:k],
                    textposition="top center", line=dict(color=BLUE, width=4), marker=dict(size=12), row=1, col=2)
    if k:
        r = t.iloc[k - 1]
        prev = 0 if k == 1 else t.cum[k - 2]
        fig.add_scatter(x=[r.vacation], y=[r.cum], mode="markers", marker=dict(size=22, color=ORANGE), row=1, col=2)
        head = (f"<b>{r.vacation}</b>: f = {r.f}   relative f = {r.f}/200 = {r.f / 200:.3f}"
                f"<br>F = {prev} + {r.f} = <b>{r.cum}</b>")
    else:
        head = "<b>200 answers, six categories</b><br>count them one category at a time"
    fig.update_yaxes(range=[0, 75], title_text="people", row=1, col=1)
    fig.update_yaxes(range=[0, 240], title_text="people so far", row=1, col=2)
    fig.update_xaxes(tickangle=-35, range=[-0.7, 5.7])
    fig.update_annotations(font_size=22)
    fig.update_layout(template="simple_white", width=1300, height=600, font=FONT, showlegend=False,
                      title=dict(text=head, x=0.5, y=0.96), margin=dict(l=80, r=30, t=150, b=110))
    return fig


if __name__ == "__main__":
    save_gif([frame(k) for k in range(7)], "running_total", here, keys=[1, 2, 4, 6], fps=1,
             holds=[2, 2, 2, 2, 2, 2, 5], width=900)
