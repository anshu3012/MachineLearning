"""Complete case analysis as a process on the job data's experience column: rows are hidden step by step, at random
(MCAR, left) or only among people with under 5 years (MNAR, right), and CCA keeps the rest. At random, every bar shrinks
by the same share and the mean stays; under MNAR only the left bars shrink and the mean rises. Same random numbers and
final shares as the still mechanisms figure (charts.py). Our own design. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from anim import save_gif, FONT, GREEN, GREY

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "data_science_job.csv.gz")
full = df.dropna(subset=["experience"])
exp = full["experience"].to_numpy()
u = np.random.default_rng(0).random(len(full))
BINS = dict(start=-0.5, end=20.5, size=1)
STEPS = np.linspace(0, 1, 6)


def kept(kind, s):
    hide = (u < 0.25 * s) if kind == "MCAR" else (exp < 5) & (u < 0.8 * s)
    return exp[~hide]


assert round(exp.mean(), 1) == 9.9 and round(kept("MCAR", 1).mean(), 1) == 9.9 and round(kept("MNAR", 1).mean(), 1) == 11.9


def frame(s):
    names = {"MCAR": "MCAR: rows hidden at random", "MNAR": "MNAR: hidden only if under 5 years"}
    titles = []
    for kind in names:
        k = kept(kind, s)
        titles.append(f"{names[kind]}<br>{100 * (1 - len(k) / len(exp)):.0f}% removed, mean {k.mean():.1f} years")
    fig = make_subplots(1, 2, horizontal_spacing=0.08, subplot_titles=titles, shared_yaxes=True)
    for j, kind in enumerate(names, start=1):
        fig.add_histogram(x=exp, xbins=BINS, marker_color=GREY, opacity=0.35, name="all rows", showlegend=j == 1, row=1, col=j)
        fig.add_histogram(x=kept(kind, s), xbins=BINS, marker_color=GREEN, opacity=0.8, name="rows CCA keeps",
                          showlegend=j == 1, row=1, col=j)
        fig.add_vline(x=exp.mean(), line=dict(color="black", width=2, dash="dot"), opacity=1, row=1, col=j)
        fig.add_vline(x=kept(kind, s).mean(), line=dict(color=GREEN, width=4), opacity=1, row=1, col=j)
        fig.update_xaxes(title="experience (years)", row=1, col=j)
    fig.update_yaxes(title="rows", range=[0, 3600], row=1, col=1)
    fig.update_annotations(font_size=21)
    fig.update_layout(template="simple_white", barmode="overlay", bargap=0.05, width=1300, height=600, font=FONT,
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2), margin=dict(l=80, r=20, t=110, b=110))
    return fig


if __name__ == "__main__":
    save_gif([frame(s) for s in STEPS], "rows_vanish", here, keys=[0, 5], fps=1, holds=[3, 1, 1, 1, 1, 6], cols=1, width=900)
