"""Why features on different scales must be standardised before PCA. Two features of scikit-learn's wine data
(178 wines): proline (278 to 1680) and hue (0.48 to 1.71). Left: PCA on the raw values, PC1 is almost pure proline.
Right: after standardising, PC1 mixes both in equal parts. Both panels are drawn in standardised units so the
PC1 arrows can be compared. Plotly (a chart)."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

here = Path(__file__).parent
BLUE, ORANGE = "#4C78A8", "#F58518"
w = load_wine(as_frame=True).data[["proline", "hue"]]
raw = w.values
std = StandardScaler().fit_transform(raw)


def pc1(X):
    p = PCA(n_components=1).fit(X)
    u = p.components_[0]
    return u * np.sign(u[0]), p.explained_variance_ratio_[0]


u_raw, r_raw = pc1(raw)
u_std, r_std = pc1(std)
print("raw PC1", u_raw.round(4), round(r_raw, 4), "| standardised PC1", u_std.round(3), round(r_std, 3),
      "| std devs", raw.std(axis=0).round(2))
assert abs(u_raw[0]) > 0.999 and abs(abs(u_std[0]) - 0.707) < 0.001
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12, subplot_titles=[
    f"raw values: PC1 = {u_raw[0]:.2f} × proline + {u_raw[1]:.2f} × hue",
    f"standardised: PC1 = {u_std[0]:.2f} × proline + {u_std[1]:.2f} × hue"])
fig.add_scatter(x=raw[:, 0], y=raw[:, 1], mode="markers", marker=dict(size=8, color=BLUE, opacity=0.7), row=1, col=1)
fig.add_scatter(x=std[:, 0], y=std[:, 1], mode="markers", marker=dict(size=8, color=BLUE, opacity=0.7), row=1, col=2)
m = raw.mean(axis=0)
for col, (c, u, L) in enumerate([(m, u_raw, 620), ((0, 0), u_std, 2.6)], start=1):
    fig.add_annotation(x=c[0] + L * u[0], y=c[1] + L * u[1], ax=c[0] - L * u[0], ay=c[1] - L * u[1], xref=f"x{col if col > 1 else ''}",
                       yref=f"y{col if col > 1 else ''}", axref=f"x{col if col > 1 else ''}", ayref=f"y{col if col > 1 else ''}",
                       arrowhead=3, arrowwidth=5, arrowcolor=ORANGE, text="")
fig.add_annotation(x=1500, y=1.12, text="<b>PC1</b>", showarrow=False, font=dict(color=ORANGE, size=22), row=1, col=1)
fig.add_annotation(x=2.2, y=1.4, text="<b>PC1</b>", showarrow=False, font=dict(color=ORANGE, size=22), row=1, col=2)
fig.update_xaxes(title_text="proline (278 to 1680)", range=[0, 1900], row=1, col=1)
fig.update_yaxes(title_text="hue (0.48 to 1.71)", range=[0, 2.2], row=1, col=1)
fig.update_xaxes(title_text="proline, standardised", range=[-3.4, 3.4], row=1, col=2)
fig.update_yaxes(title_text="hue, standardised", range=[-3.4, 3.4], scaleanchor="x2", row=1, col=2)
for a in fig.layout.annotations[:2]:
    a.font.size = 20
fig.update_layout(template="simple_white", width=1400, height=640, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=18), margin=dict(l=70, r=20, t=60, b=70))
fig.write_image(here / "scale_matters.png", scale=2)
fig.write_image(here / "scale_matters.pdf")
