"""One MNIST image (the first training image, a 5) rebuilt from its first k principal components, k = 1 ... 300.
PCA is fitted on all 70,000 images (Keras copy, ~/.keras/datasets/mnist.npz); the rebuilt images are stored in
data/mnist_reconstruct.csv so the figure builds without the 11 MB MNIST file. Plotly heatmap frames -> GIF."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from anim import save_gif, FONT

here = Path(__file__).parent
CSV = here.parent / "data" / "mnist_reconstruct.csv"
KS = [1, 5, 20, 50, 100, 300]
if not CSV.exists():
    from sklearn.decomposition import PCA
    z = np.load(Path.home() / ".keras" / "datasets" / "mnist.npz")
    X = np.concatenate([z["x_train"], z["x_test"]]).reshape(-1, 784).astype(float)
    pca = PCA(n_components=300, svd_solver="randomized", random_state=0).fit(X)
    s = pca.transform(X[:1])[0]                                   # the image's 300 scores
    rec = [pca.mean_ + s[:k] @ pca.components_[:k] for k in KS]   # mean image + the first k components
    cum = np.cumsum(pca.explained_variance_ratio_)
    df = pd.DataFrame(np.vstack([X[0]] + rec).round(1))
    df.insert(0, "kept", [1.0] + [cum[k - 1] for k in KS])
    df.insert(0, "k", [784] + KS)
    df.to_csv(CSV, index=False)
d = pd.read_csv(CSV)
orig = d.iloc[0, 2:].values.reshape(28, 28)


def frame(i):
    row = d.iloc[i]
    img = row.iloc[2:].values.astype(float).reshape(28, 28)
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.06,
                        subplot_titles=["the original: 784 pixels", f"rebuilt from {int(row.k)} number{'s' if row.k > 1 else ''}"])
    for c, im in enumerate([orig, img], start=1):
        fig.add_heatmap(z=im[::-1], colorscale="Greys", zmin=0, zmax=255, showscale=False, row=1, col=c)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_xaxes(scaleanchor="y", row=1, col=1)
    fig.update_xaxes(scaleanchor="y2", row=1, col=2)
    for a in fig.layout.annotations:
        a.font.size = 24
    fig.update_layout(template="simple_white", width=1000, height=600, font=FONT, margin=dict(l=20, r=20, t=110, b=20),
                      title=dict(x=0.5, text=f"{int(row.k)} principal component{'s' if row.k > 1 else ''}: "
                                                f"{100 * row.kept:.0f} percent of the variance kept"))
    return fig


if __name__ == "__main__":
    print(d[["k", "kept"]].round(3).to_string())
    save_gif([frame(i) for i in range(1, len(d))], "reconstruct", here, keys=[0, 1, 2, 3, 4, 5],
             fps=1, holds=[2] * 5 + [5], cols=3, width=800)
