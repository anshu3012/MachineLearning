"""Plotly figures for the Optuna Note: grid against random search on the 5 x 5 placement grid (section 2),
the TPE study's max_depth trial by trial (section 5.2), and the algorithm study filling in trial by trial
(section 8, GIF + frame grid). Studies are read from data/optuna.db, which the Notebook wrote."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import optuna
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
STORAGE = f"sqlite:///{here.parent / 'data' / 'optuna.db'}"
FONT = dict(family="Latin Modern Roman", size=20)
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
LAY = dict(template="simple_white", font=FONT)
optuna.logging.set_verbosity(optuna.logging.WARNING)


def save(fig, name):
    fig.write_image(here / f"{name}.png", scale=2); fig.write_image(here / f"{name}.pdf")


# Section 2: the 5 x 5 grid; grid search trains all 25, random search 5 of them
D, M = np.meshgrid(np.arange(1, 6), np.arange(50, 251, 50))
D, M = D.ravel(), M.ravel()
assert len(D) == 25
pick = np.random.default_rng(0).choice(25, size=5, replace=False)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=["grid search: all 25 models trained", "random search: 5 models, 20 never seen"])
fig.add_trace(go.Scatter(x=D, y=M, mode="markers", marker=dict(size=24, color=GREY), showlegend=False), 1, 1)
fig.add_trace(go.Scatter(x=D, y=M, mode="markers", marker=dict(size=24, color="white", line=dict(color="#BBBBBB",
                         width=2)), showlegend=False), 1, 2)
fig.add_trace(go.Scatter(x=D[pick], y=M[pick], mode="markers", marker=dict(size=24, color=ORANGE),
                         showlegend=False), 1, 2)
fig.update_xaxes(title="max_depth", dtick=1, range=[0.4, 5.6])
fig.update_yaxes(title="n_estimators", tickvals=[50, 100, 150, 200, 250], range=[20, 280])
fig.update_layout(**LAY, width=1100, height=500, margin=dict(l=80, r=20, t=60, b=60))
fig.update_annotations(font=dict(family="Latin Modern Roman", size=21))
save(fig, "search_blind")

# Section 5.2: TPE's max_depth per trial; random for 10 trials, then it returns to depth 8 and 9
tpe = optuna.load_study(study_name="tpe", storage=STORAGE).trials_dataframe()
best = tpe.loc[tpe.value.idxmax()]
assert round(best.value, 3) == 0.790 and (best.params_n_estimators, best.params_max_depth) == (115, 8)
good = tpe.params_max_depth.isin([8, 9])
n_start, n_late = int(good[:10].sum()), int(good[10:].sum())
assert (n_start, n_late) == (1, 12)
fig = go.Figure()
fig.add_hrect(y0=7.5, y1=9.5, fillcolor=GREEN, opacity=0.12, line_width=0)
fig.add_vrect(x0=-0.5, x1=9.5, fillcolor=GREY, opacity=0.08, line_width=0)
fig.add_trace(go.Scatter(x=tpe.number, y=tpe.params_max_depth, mode="markers", showlegend=False,
                         marker=dict(size=13, color=tpe.value, colorscale="Blues", cmin=0.75, cmax=0.79,
                                     line=dict(color=GREY, width=1),
                                     colorbar=dict(title="CV<br>accuracy", tickformat=".2f", dtick=0.01))))
fig.add_annotation(x=0, y=21.3, xanchor="left", text="10 random starts", showarrow=False, font=dict(color=GREY))
fig.add_annotation(x=30, y=21.3, text=f"TPE: depth 8 or 9 in {n_late} of 40 trials", showarrow=False,
                   font=dict(color=GREEN))
fig.update_layout(**LAY, width=1000, height=500, margin=dict(l=80, r=20, t=30, b=60),
                  xaxis=dict(title="trial", range=[-1, 50]), yaxis=dict(title="max_depth", range=[2, 22.5]))
save(fig, "tpe_gathers")

# Section 8: the algorithm study, trial by trial
alg = optuna.load_study(study_name="algorithm", storage=STORAGE).trials_dataframe()
NAMES = {"RandomForest": ("random forest", BLUE), "GradientBoosting": ("gradient boosting", ORANGE),
         "SVC": ("SVC", GREEN)}
blocks = [(0, 20), (20, 40), (40, 60), (60, 100)]
counts = [alg.params_classifier[a:b].value_counts().reindex(NAMES).fillna(0).astype(int).tolist() for a, b in blocks]
assert counts == [[8, 8, 4], [1, 17, 2], [2, 11, 7], [40, 0, 0]], counts
assert round(alg.value.max(), 3) == 0.788


def frame(n):
    seen = alg[:n]
    fig = go.Figure()
    for key, (label, c) in NAMES.items():
        s = seen[seen.params_classifier == key]
        fig.add_trace(go.Scatter(x=s.number, y=s.value, mode="markers", name=f"{label}: {len(s)}",
                                 marker=dict(size=12, color=c, line=dict(color="white", width=1))))
    for a, b in blocks[1:]:
        fig.add_vline(x=a - 0.5, line=dict(color="#CCCCCC", width=1))
    fig.update_layout(**LAY, width=950, height=580, margin=dict(l=80, r=20, t=110, b=60),
                      title=dict(text=f"{n} trials", x=0.5),
                      xaxis=dict(title="trial", range=[-2, 101]), yaxis=dict(title="3-fold CV accuracy",
                                                                             range=[0.6, 0.81]),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=1.02, yanchor="bottom"))
    return fig


if __name__ == "__main__":
    tmp = here / ".alg"
    tmp.mkdir(exist_ok=True)
    stops = list(range(5, 101, 5))
    for i, n in enumerate(stops):
        frame(n).write_image(tmp / f"{i:03d}.png")
    for i in range(len(stops), len(stops) + 9):
        shutil.copy(tmp / f"{len(stops) - 1:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(here / "algorithm_race.gif")], check=True)
    # the last frame holds the whole story (all 100 trials and the counts), and stays readable in the PDF
    shutil.copy(tmp / f"{len(stops) - 1:03d}.png", here / "algorithm_race_frames.png")
    shutil.rmtree(tmp)
