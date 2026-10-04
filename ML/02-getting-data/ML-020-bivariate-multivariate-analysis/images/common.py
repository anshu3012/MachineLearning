"""Shared data, colours and theme for this Note's figures (imported by the other scripts)."""
from pathlib import Path
import pandas as pd

here = Path(__file__).parent
data = here.parent / "data"
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
FONT = dict(family="Latin Modern Roman", size=17)


def load(name):
    return pd.read_csv(data / f"{name}.csv")


def layout(fig, title, x, y, width=900, height=540, **kw):
    """The house style for a simple chart: white background, grid on the value axis, centred title."""
    fig.update_layout(template="simple_white", width=width, height=height, font=FONT, title=dict(text=title, x=0.5),
                      xaxis_title=x, yaxis_title=y, margin=dict(l=80, r=20, t=70, b=70), **kw)
    return fig


def save_px(fig, name):
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


def clustermap(table, title, colorbar_title, width=900, height=620):
    """Plotly version of seaborn's clustermap: average-linkage dendrograms on rows and columns, heatmap reordered to match."""
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    from scipy.cluster.hierarchy import dendrogram, linkage

    def tree(values):
        return dendrogram(linkage(values, method="average"), no_plot=True) if len(values) > 1 else None

    rows, cols = tree(table.values), tree(table.values.T)
    r_order = rows["leaves"] if rows else [0]
    c_order = cols["leaves"] if cols else [0]
    t = table.iloc[r_order, c_order]
    fig = make_subplots(rows=2, cols=2, column_widths=[0.18, 0.82], row_heights=[0.16, 0.84],
                        horizontal_spacing=0.01, vertical_spacing=0.01)
    # scipy places leaf i at 5 + 10 i; the heatmap places it at i, so map with (x - 5) / 10
    line = dict(color=GREY, width=2)
    if rows:  # row tree on the left, leaves facing the heatmap
        for xs, ys in zip(rows["icoord"], rows["dcoord"]):
            fig.add_trace(go.Scatter(x=[-y for y in ys], y=[(x - 5) / 10 for x in xs], mode="lines", line=line,
                                     hoverinfo="skip", showlegend=False), 2, 1)
    if cols:  # column tree on top
        for xs, ys in zip(cols["icoord"], cols["dcoord"]):
            fig.add_trace(go.Scatter(x=[(x - 5) / 10 for x in xs], y=ys, mode="lines", line=line,
                                     hoverinfo="skip", showlegend=False), 1, 2)
    fig.add_trace(go.Heatmap(z=t.values, x=list(range(t.shape[1])), y=list(range(t.shape[0])), colorscale="Blues",
                             text=t.values.round(0).astype(int), texttemplate="%{text}", textfont=dict(size=14),
                             colorbar=dict(title=colorbar_title, len=0.7, y=0.42, x=1.1)), 2, 2)
    fig.update_xaxes(tickvals=list(range(t.shape[1])), ticktext=[str(c) for c in t.columns], title=table.columns.name,
                     range=[-0.5, t.shape[1] - 0.5], row=2, col=2)
    fig.update_yaxes(tickvals=list(range(t.shape[0])), ticktext=[str(i) for i in t.index], side="right",
                     title=table.index.name, range=[-0.5, t.shape[0] - 0.5], row=2, col=2)
    fig.update_yaxes(range=[-0.5, t.shape[0] - 0.5], row=2, col=1)
    fig.update_xaxes(range=[-0.5, t.shape[1] - 0.5], row=1, col=2)
    for r, c in [(1, 1), (1, 2), (2, 1)]:
        fig.update_xaxes(visible=False, row=r, col=c)
        fig.update_yaxes(visible=False, row=r, col=c)
    fig.update_layout(template="simple_white", width=width, height=height, font=FONT, title=dict(text=title, x=0.5),
                      margin=dict(l=20, r=150, t=70, b=60))
    return fig
