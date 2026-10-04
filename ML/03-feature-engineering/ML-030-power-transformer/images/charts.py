"""Plotly charts for Note ML-030: the Box-Cox family of curves, and the concrete columns before and after PowerTransformer.
Q-Q plots are scipy.stats.probplot data drawn in Plotly."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PowerTransformer

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, PURPLE, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=20)


def qq(fig, x, row, col, colour=BLUE):
    """Q-Q plot: probplot gives (normal quantiles, sorted data) and the best straight line through them."""
    (osm, osr), (slope, intercept, _) = stats.probplot(x, dist="norm")
    fig.add_trace(go.Scatter(x=osm, y=osr, mode="markers", marker=dict(color=colour, size=4, opacity=0.6)), row, col)
    fig.add_trace(go.Scatter(x=osm[[0, -1]], y=slope * osm[[0, -1]] + intercept, mode="lines",
                             line=dict(color=RED, width=2.5)), row, col)


def hist(fig, x, row, col, colour=BLUE):
    """Histogram scaled to density, with a KDE curve on top."""
    fig.add_trace(go.Histogram(x=x, histnorm="probability density", nbinsx=30, marker_color=colour, opacity=0.45), row, col)
    grid = np.linspace(x.min(), x.max(), 300)
    fig.add_trace(go.Scatter(x=grid, y=stats.gaussian_kde(x)(grid), mode="lines", line=dict(color=colour, width=2.5)), row, col)


def save(fig, name, width, height, title_size=19, font_size=20):
    fig.update_layout(template="simple_white", width=width, height=height, showlegend=False, font={**FONT, "size": font_size},
                      bargap=0.02, margin=dict(l=60, r=20, t=60, b=40))
    fig.update_annotations(font_size=title_size)
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


# 1. the Box-Cox family: one curve per lambda; log, square root, reciprocal and square are members
x = np.linspace(0.08, 4, 300)
fig = go.Figure()
curves = [(2, "λ = 2: like x²", ORANGE, 7.5), (1, "λ = 1: no change", GREY, 3.7),
          (0.5, "λ = 0.5: like √x", GREEN, 2.3), (0, "λ = 0: log x", BLUE, 0.9), (-1, "λ = −1: like 1/x", PURPLE, -0.5)]
for lam, label, colour, label_y in curves:
    y = stats.boxcox(x, lam)
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color=colour, width=3.5)))
    fig.add_annotation(x=4.05, y=label_y, text=label, showarrow=False, xanchor="left", font=dict(color=colour, size=30))
fig.update_xaxes(title="original value x", range=[0, 6.1], tickvals=[0, 1, 2, 3, 4])
fig.update_yaxes(title="transformed value", range=[-4, 8])
save(fig, "lambda_family", 900, 520, title_size=28, font_size=24)

# concrete training set, exactly as in the Notebook
df = pd.read_csv(here.parent / "data" / "concrete_data.csv")
X, y = df.drop(columns=["Strength"]), df["Strength"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
cols = list(X.columns)

# 2. every raw column: histogram on top, Q-Q plot below (two blocks of four columns)
fig = make_subplots(4, 4, vertical_spacing=0.09, horizontal_spacing=0.06,
                    subplot_titles=[f"{c} ({X_train[c].skew():.2f})" if r in (0, 2) else "Q-Q plot"
                                    for r in range(4) for c in cols[(r // 2) * 4:(r // 2) * 4 + 4]])
for i, c in enumerate(cols):
    block, col = i // 4, i % 4 + 1
    hist(fig, X_train[c].values, 2 * block + 1, col)
    qq(fig, X_train[c].values.astype(float), 2 * block + 2, col)
fig.update_yaxes(showticklabels=False)
fig.update_xaxes(tickfont_size=17)
save(fig, "raw_columns", 1300, 1050, title_size=22)

# 3. Age: raw, after Box-Cox, after Yeo-Johnson (histogram and Q-Q plot)
bc = PowerTransformer(method="box-cox").fit(X_train + 0.000001)
yj = PowerTransformer(method="yeo-johnson").fit(X_train)
Xbc = pd.DataFrame(bc.transform(X_train + 0.000001), columns=cols)
Xyj = pd.DataFrame(yj.transform(X_train), columns=cols)
lam_bc, lam_yj = dict(zip(cols, bc.lambdas_)), dict(zip(cols, yj.lambdas_))
age = [("Age, raw", X_train["Age"].values.astype(float), BLUE),
       (f"Box-Cox, λ = {lam_bc['Age']:.3f}", Xbc["Age"].values, GREEN),
       (f"Yeo-Johnson, λ = {lam_yj['Age']:.3f}", Xyj["Age"].values, GREEN)]
fig = make_subplots(2, 3, vertical_spacing=0.16, horizontal_spacing=0.07,
                    subplot_titles=[f"{t}: skew {pd.Series(v).skew():.2f}" for t, v, _ in age] + ["Q-Q plot"] * 3)
for i, (_, v, colour) in enumerate(age, start=1):
    hist(fig, v, 1, i, colour)
    qq(fig, v, 2, i, colour)
fig.update_yaxes(showticklabels=False)
save(fig, "age_power", 1200, 650, title_size=23)

# 4. every column after each method: histograms with lambda and skewness in the titles
for name, data, lams in [("boxcox_after", Xbc, lam_bc), ("yeojohnson_after", Xyj, lam_yj)]:
    fig = make_subplots(2, 4, vertical_spacing=0.2, horizontal_spacing=0.05,
                        subplot_titles=[f"{c}<br>λ = {lams[c]:.2f}, skew {data[c].skew():.2f}" for c in cols])
    for i, c in enumerate(cols):
        hist(fig, data[c].values, i // 4 + 1, i % 4 + 1, GREEN)
    fig.update_yaxes(showticklabels=False)
    fig.update_xaxes(tickfont_size=14)
    save(fig, name, 1300, 660, title_size=22)

# 5. Yeo-Johnson next to Box-Cox, lambda = 0.5: Box-Cox stops at 0, Yeo-Johnson carries on smoothly into negatives
lam = 0.5
pts = np.array([-3.0, 0.0, 3.0])
yj_pts = stats.yeojohnson(pts, lam)
assert np.allclose(yj_pts, [-4.67, 0, 2], atol=0.005)          # the worked example of Section 4
xs = np.linspace(-4, 4, 400)
fig = go.Figure()
fig.add_trace(go.Scatter(x=xs, y=stats.yeojohnson(xs, lam), mode="lines", line=dict(color=GREEN, width=4)))
xp = xs[xs > 0]
fig.add_trace(go.Scatter(x=xp, y=stats.boxcox(xp, lam), mode="lines", line=dict(color=BLUE, width=4, dash="dash")))
fig.add_trace(go.Scatter(x=pts, y=yj_pts, mode="markers+text", marker=dict(color=RED, size=14),
                         text=[f"({p:g}, {v:.2f})" for p, v in zip(pts, yj_pts)],
                         textposition=["middle right", "top left", "top left"], textfont=dict(size=24, color=RED)))
fig.add_vrect(x0=-4, x1=0, fillcolor=GREY, opacity=0.08, line_width=0)
fig.add_annotation(x=-2, y=3, text="x ≤ 0: Box-Cox<br>has no value here", showarrow=False, font=dict(size=24, color=BLUE))
fig.add_annotation(x=3.9, y=2.9, text="Yeo-Johnson", showarrow=False, xanchor="right", font=dict(size=26, color=GREEN))
fig.add_annotation(x=3.9, y=1.0, text="Box-Cox", showarrow=False, xanchor="right", font=dict(size=26, color=BLUE))
fig.update_xaxes(title="original value x", range=[-4, 4], zeroline=True)
fig.update_yaxes(title="transformed value (λ = 0.5)", range=[-6.5, 4], zeroline=True)
save(fig, "yeojohnson_vs_boxcox", 900, 560, font_size=24)

# 6. FunctionTransformer(log1p) vs PowerTransformer on the same training columns: skewness after each
from sklearn.preprocessing import FunctionTransformer
logged = pd.DataFrame(FunctionTransformer(np.log1p).fit_transform(X_train), columns=cols)
sk = pd.DataFrame({"raw": X_train.skew(), "log": logged.skew(), "yj": Xyj.skew()})
assert round(sk.loc["Age", "raw"], 2) == 3.34 and round(sk.loc["Age", "yj"], 2) == 0.00
assert (sk["yj"].abs() <= sk["log"].abs() + 1e-9).all()       # the learned power is never further from 0 here
short = [c.replace("Blast Furnace ", "").replace(" Aggregate", " Agg.").replace("Superplasticizer", "Superplast.")
         for c in cols]
fig = go.Figure()
for key, colour, name in [("raw", GREY, "raw"), ("log", ORANGE, "log(1 + x) for every feature"),
                          ("yj", GREEN, "Yeo-Johnson, own λ per feature")]:
    fig.add_trace(go.Bar(x=short, y=sk[key], marker_color=colour, name=name))
fig.add_annotation(x="Age", y=1.55, text="Age raw: 3.34 (bar cut off)", showarrow=False, xanchor="right", xshift=-45, font=dict(size=20, color=GREY))
fig.update_yaxes(title="skewness (0 = symmetric)", range=[-0.7, 1.7], zeroline=True)
fig.update_layout(barmode="group", showlegend=True, legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.22))
fig.update_layout(template="simple_white", width=1300, height=600, font=FONT, margin=dict(l=80, r=20, t=30, b=150))
fig.write_image(here / "function_vs_power.png", scale=2)
fig.write_image(here / "function_vs_power.pdf")
print(sk.round(2))
