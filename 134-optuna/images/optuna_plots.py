"""Optuna's own Plotly plots of the studies the Notebook saved in data/optuna.db, restyled in Latin Modern:
optimisation history (grid, random, TPE), parallel coordinates, contour and hyperparameter importances (TPE)."""
from pathlib import Path

import optuna
from optuna.visualization import (plot_contour, plot_optimization_history, plot_parallel_coordinate,
                                  plot_param_importances)

here = Path(__file__).parent
STORAGE = f"sqlite:///{here.parent / 'data' / 'optuna.db'}"
FONT = dict(family="Latin Modern Roman", size=20)
optuna.logging.set_verbosity(optuna.logging.WARNING)
grid, rand, tpe = (optuna.load_study(study_name=n, storage=STORAGE) for n in ["grid", "random", "tpe"])


def save(fig, name, title, w=1000, h=560, **layout):
    fig.update_layout(template="simple_white", font=FONT, width=w, height=h,
                      title=dict(text=title, x=0.5, font=dict(family=FONT["family"], size=20)), **layout)
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


fig = plot_optimization_history([grid, rand, tpe])
colours = {"grid": "#6B6B6B", "random": "#F58518", "tpe": "#4C78A8"}
labels = {"grid": "grid", "random": "random", "tpe": "TPE"}
for tr in fig.data:                       # traces: "Objective Value of <study>", "Best Value of <study>", "Infeasible Trial"
    study = tr.name.split()[-1]
    if study not in colours:
        tr.showlegend = False
        continue
    c = colours[study]
    if tr.name.startswith("Best"):
        tr.update(line=dict(color=c, width=3), mode="lines", name=f"{labels[study]}: best so far")
    else:
        tr.update(marker=dict(color=c, size=7, opacity=0.5), name=f"{labels[study]}: each trial")
save(fig, "history", "Optimisation history: grid, random and TPE", w=900,
     yaxis=dict(title="3-fold CV accuracy", tickformat=".3f"), xaxis=dict(title="trial"),
     legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2), margin=dict(l=70, r=20, t=60, b=130))

fig = plot_parallel_coordinate(tpe)
# Optuna draws this plot with scatter lines; the axis numbers are annotations in a small grey font
fig.update_annotations(font=dict(family=FONT["family"], size=17, color="#333333"))
save(fig, "parallel", "Parallel coordinates of the TPE study", w=900, h=520, margin=dict(l=90, r=40, t=60, b=40))

fig = plot_contour(tpe)
save(fig, "contour", "Contour plot of the TPE study", w=760, h=560, margin=dict(l=80, r=40, t=70, b=70))

fig = plot_param_importances(tpe)
fig.update_traces(marker_color="#4C78A8")
save(fig, "importances", "Hyperparameter importances (TPE study)", w=800, h=340,
     margin=dict(l=140, r=40, t=70, b=60))
