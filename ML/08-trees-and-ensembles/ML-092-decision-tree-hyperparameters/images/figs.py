"""Plotly figures for the hyperparameters Note: max_depth on the ads data, and four ways to stop a tree on the moons data."""
import sys
from pathlib import Path

from plotly.subplots import make_subplots

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import fit, grid, traces          # same data and surface code as the app


def panel_figure(name, settings, titles, out, rows, cols, height):
    fig = make_subplots(rows=rows, cols=cols, subplot_titles=titles, horizontal_spacing=0.07, vertical_spacing=0.13)
    for i, params in enumerate(settings):
        tree, X_train, X_test, y_train, y_test, axes, classes = fit(name, **params)
        fig.layout.annotations[i].text += (f"<br>{tree.get_n_leaves()} leaves, train {tree.score(X_train, y_train):.2f},"
                                           f" test {tree.score(X_test, y_test):.2f}")
        print(out, fig.layout.annotations[i].text.replace("<br>", " | "))
        for t in traces(tree, X_train, y_train, classes, show_legend=(i == 0)):
            fig.add_trace(t, i // cols + 1, i % cols + 1)
    xs, ys = grid(X_train)
    fig.update_xaxes(range=[xs[0], xs[-1]])
    fig.update_yaxes(range=[ys[0], ys[-1]])
    fig.update_xaxes(title=axes[0], row=rows)
    fig.update_yaxes(title=axes[1], col=1)
    fig.update_annotations(font_size=19)
    fig.update_layout(template="simple_white", width=1100 if cols == 2 else 1400, height=height,
                      font=dict(family="Latin Modern Roman", size=16),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.1), margin=dict(l=80, r=20, t=80, b=100))
    fig.write_image(HERE / f"{out}.png", scale=2)
    fig.write_image(HERE / f"{out}.pdf")


depths = [None, 1, 2, 3, 4, 5]
panel_figure("ads", [dict(max_depth=d) for d in depths], [f"max_depth = {d}" for d in depths], "depth_surfaces", 2, 3, 950)

stops = [dict(), dict(min_samples_split=100), dict(min_samples_leaf=20), dict(max_leaf_nodes=5)]
panel_figure("moons", stops, ["no limits (fully grown)", "min_samples_split = 100", "min_samples_leaf = 20",
                              "max_leaf_nodes = 5"], "stopping_rules", 2, 2, 1000)
