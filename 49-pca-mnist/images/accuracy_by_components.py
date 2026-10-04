"""KNN accuracy on MNIST test images as the number of principal components grows, against all 784 columns (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
r = pd.read_csv(here.parent / "data" / "knn_results.csv")
pca = r[r.setup.str.startswith("PCA ")]
full = r[r.setup == "raw pixels"].iloc[0]
fig = go.Figure()
fig.add_trace(go.Scatter(x=[1, 300], y=[full.accuracy] * 2, mode="lines", line=dict(color=GREY, dash="dash", width=2)))
fig.add_annotation(x=2.4, y=full.accuracy, yshift=-14, xref="x", text=f"all 784 columns: {full.accuracy:.1%}",
                   showarrow=False, font=dict(color=GREY, size=15))
fig.add_trace(go.Scatter(x=pca["columns"], y=pca.accuracy, mode="lines+markers+text", line=dict(color=BLUE, width=4),
                         marker=dict(size=9), text=[f"{a:.0%}" for a in pca.accuracy], textposition="top left",
                         textfont=dict(size=13)))
fig.update_layout(template="simple_white", width=950, height=500, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=80, r=30, t=60, b=60),
                  title=dict(text="KNN on MNIST: accuracy with k principal components", x=0.5),
                  xaxis=dict(title="Number of principal components k (log scale)", type="log",
                             tickvals=pca["columns"].tolist()),
                  yaxis=dict(title="Test accuracy", tickformat=".0%", range=[0, 1.02]))
fig.write_image(here / "accuracy_by_components.png", scale=2)
fig.write_image(here / "accuracy_by_components.pdf")
