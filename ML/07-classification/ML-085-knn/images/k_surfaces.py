"""Decision surfaces for k = 1, 5, 20 and k = n (every training point): overfitting to underfitting (Plotly)."""
import sys
from pathlib import Path

from plotly.subplots import make_subplots

here = Path(__file__).parent
sys.path.insert(0, str(here.parent))
from app import X_train, traces, xs, ys

ks = [1, 5, 20, len(X_train)]
results = [traces(k, show_legend=(i == 0)) for i, k in enumerate(ks)]
titles = [f"k = {k}{' (= n)' if k == len(X_train) else ''}: test accuracy {acc:.2f}" for k, (_, acc) in zip(ks, results)]
fig = make_subplots(rows=2, cols=2, subplot_titles=titles, horizontal_spacing=0.08, vertical_spacing=0.12)
for i, (tr, acc) in enumerate(results):
    print(titles[i])
    for t in tr:
        fig.add_trace(t, i // 2 + 1, i % 2 + 1)
fig.update_xaxes(range=[xs[0], xs[-1]], title="mean radius", row=2)
fig.update_xaxes(range=[xs[0], xs[-1]])
fig.update_yaxes(range=[ys[0], ys[-1]])
fig.update_yaxes(title="mean texture", col=1)
fig.update_annotations(font_size=19)
fig.update_layout(template="simple_white", width=1100, height=950, font=dict(family="Latin Modern Roman", size=16),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.08), margin=dict(l=70, r=20, t=50, b=90))
fig.write_image(here / "k_surfaces.png", scale=2); fig.write_image(here / "k_surfaces.pdf")
