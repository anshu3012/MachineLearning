"""Sections 9 and 10.3: the hand-made network and the tuned winner, each retrained with 5 seeds; one dot per run,
validation and test accuracy (Plotly)."""
from pathlib import Path
import pandas as pd
from plotly.subplots import make_subplots
from common import BLUE, GREEN, RED, FONT

here = Path(__file__).parent
cases = {"retrain_dots": ("retrain.csv", "baseline", {("baseline", "val"): 0.751, ("tuned", "val"): 0.723,
                                                       ("baseline", "test"): 0.740, ("tuned", "test"): 0.734}),
         "mnist_retrain_dots": ("mnist_retrain.csv", "hand-made guess", {("baseline", "val"): 0.928,
                                ("tuned", "val"): 0.953, ("baseline", "test"): 0.926, ("tuned", "test"): 0.948})}
for out, (csv, base_name, means) in cases.items():
    r = pd.read_csv(here.parent / "data" / csv)
    assert sorted(r.model.unique()) == ["baseline", "tuned"] and (r.model == "tuned").sum() == 5
    for (m, s), v in means.items():
        assert round(r[r.model == m][f"{'val' if s == 'val' else 'test'}_accuracy"].mean(), 3) == v, (out, m, s)
    fig = make_subplots(1, 2, shared_yaxes=True, horizontal_spacing=0.06,
                        subplot_titles=["validation accuracy", "test accuracy"])
    for col, metric in ((1, "val_accuracy"), (2, "test_accuracy")):
        for m, label, c in (("baseline", base_name, RED), ("tuned", "tuned winner", GREEN)):
            v = r[r.model == m][metric]
            off = {"baseline": 0, "tuned": 1}[m]
            fig.add_scatter(x=[off - 0.18 + 0.05 * (i - 2) for i in range(len(v))], y=v, mode="markers", marker=dict(size=16, color=c, opacity=0.75),
                            showlegend=False, row=1, col=col)
            fig.add_scatter(x=[off], y=[v.mean()], mode="markers+text", text=[f"mean {v.mean():.3f}"],
                            textposition="middle right", marker=dict(symbol="line-ew-open", size=40, color="black",
                                                                     line=dict(width=3)),
                            textfont=dict(size=17), showlegend=False, row=1, col=col)
    fig.update_layout(template="simple_white", width=950, height=460, font=dict(FONT, size=18),
                      margin=dict(l=80, r=20, t=50, b=50))
    fig.update_yaxes(title="accuracy (one dot per seed)", row=1, col=1)
    fig.update_xaxes(tickvals=[0, 1], ticktext=[base_name, "tuned winner"], range=[-0.55, 1.75])
    fig.update_annotations(font_size=19)
    fig.write_image(here / f"{out}.png", scale=2)
    fig.write_image(here / f"{out}.pdf")
