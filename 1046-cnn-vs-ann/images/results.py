"""CNN (12,810 parameters) against ANN (101,770 parameters): test accuracy and train-test gap on MNIST and
Fashion-MNIST, mean of 3 seeds, each seed as a dot (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREY, FONT

here = Path(__file__).parent
r = pd.read_csv(here.parent / "data" / "cnn_vs_ann.csv")
r["gap"] = r.train_acc - r.test_acc
fig = make_subplots(1, 2, horizontal_spacing=0.12,
                    subplot_titles=("test accuracy (%)", "training minus test accuracy (points)"))
for name, color, label in (("ANN", GREY, "ANN, 101,770 parameters"), ("CNN", BLUE, "CNN, 12,810 parameters")):
    s = r[r.model == name]
    m = s.groupby("data")[["test_acc", "gap"]].mean().reindex(["MNIST", "Fashion-MNIST"])
    for col, key in ((1, "test_acc"), (2, "gap")):
        fig.add_trace(go.Bar(x=m.index, y=100 * m[key], name=label, marker_color=color, showlegend=col == 1,
                             text=(100 * m[key]).round(2), textposition="outside", offsetgroup=name), 1, col)
fig.update_yaxes(range=[85, 100.5], row=1, col=1)
fig.update_yaxes(range=[0, 4.6], row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=460, font=FONT, barmode="group",
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.15), margin=dict(l=60, r=20, t=40, b=80))
fig.write_image(here / "results.png", scale=2)
fig.write_image(here / "results.pdf")
