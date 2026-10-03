"""Plotly charts for Note 35: missing shares, before/after complete case analysis, and the three missingness mechanisms."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import gaussian_kde

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=20)


def save(fig, name, width, height, top=80, legend=False):
    fig.update_layout(template="simple_white", width=width, height=height, showlegend=legend, font=FONT,
                      bargap=0.05, margin=dict(l=80, r=20, t=top, b=70))
    fig.update_annotations(font_size=21)
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


# the job-applicant data, exactly as in the Notebook
df = pd.read_csv(here.parent / "data" / "data_science_job.csv.gz")
share = df.isnull().mean() * 100
cols = [c for c in df.columns if 0 < share[c] < 5]
cca = df.dropna(subset=cols)

# 1. percentage missing per column, with the 5% line
s = share.sort_values()
colour = [GREY if v == 0 else GREEN if v < 5 else RED for v in s]
fig = go.Figure(go.Bar(x=s.values, y=s.index, orientation="h", marker_color=colour,
                       text=[f"{v:.1f}%" for v in s], textposition="outside", textfont=dict(size=17)))
fig.add_vline(x=5, line=dict(color=GREY, width=2, dash="dash"))
fig.add_annotation(x=5, y=1.02, yref="paper", text="5%", showarrow=False, yanchor="bottom")
fig.update_xaxes(title="missing values (% of 19,158 rows)", range=[0, 38])
save(fig, "missing_share", 1000, 560, top=40)

# 2. the three numerical columns: histogram (top) and KDE (bottom), before and after CCA
num = [("training_hours", "training_hours"), ("city_development_index", "city_development_index"),
       ("experience", "experience")]
fig = make_subplots(2, 3, vertical_spacing=0.17, horizontal_spacing=0.07, subplot_titles=[c for c, _ in num] + [""] * 3)
for j, (c, _) in enumerate(num, start=1):
    lo, hi = df[c].min(), df[c].max()
    size = (hi - lo) / 50 if c != "experience" else 1
    for data, col, name in [(df[c], RED, "before CCA"), (cca[c], GREEN, "after CCA")]:
        fig.add_trace(go.Histogram(x=data, histnorm="probability density", marker_color=col, opacity=0.55,
                                   xbins=dict(start=lo, end=hi + size, size=size), name=name,
                                   legendgroup=name, showlegend=(j == 1)), 1, j)
        grid = np.linspace(lo, hi, 300)
        fig.add_trace(go.Scatter(x=grid, y=gaussian_kde(data.dropna())(grid), mode="lines",
                                 line=dict(color=col, width=3, dash="solid" if col == RED else "dash"),
                                 name=name, legendgroup=name, showlegend=False), 2, j)
    fig.update_xaxes(title=c, row=2, col=j)
fig.update_layout(barmode="overlay", legend=dict(orientation="h", x=0.5, xanchor="center", y=1.13))
fig.update_yaxes(title="density", col=1)
save(fig, "numeric_before_after", 1300, 720, top=110, legend=True)

# 3. category shares before and after CCA (share among the non-missing values)
fig = make_subplots(1, 2, horizontal_spacing=0.1, column_widths=[0.4, 0.6],
                    subplot_titles=["enrolled_university", "education_level"])
for j, c in enumerate(["enrolled_university", "education_level"], start=1):
    before = df[c].value_counts(normalize=True)
    after = cca[c].value_counts(normalize=True)[before.index]
    for data, col, name in [(before, RED, "before CCA"), (after, GREEN, "after CCA")]:
        fig.add_trace(go.Bar(x=[i.replace(" ", "<br>").replace("_", "<br>") for i in data.index], y=data.values * 100,
                             marker_color=col, name=name, legendgroup=name, showlegend=(j == 1),
                             text=[f"{v:.1f}" for v in data * 100], textposition="outside", textfont=dict(size=15)), 1, j)
fig.update_layout(barmode="group", bargroupgap=0.05, legend=dict(orientation="h", x=0.5, xanchor="center", y=1.2))
fig.update_yaxes(title="share of rows (%)", range=[0, 85], col=1)
fig.update_yaxes(range=[0, 70], col=2)
save(fig, "category_shares", 1300, 560, top=120, legend=True)

# 4. the same column made incomplete three ways; keep only the rows still complete
full = df.dropna(subset=["experience"])
rng = np.random.default_rng(0)
u = rng.random(len(full))
hide = {"MCAR: 25% hidden at random": u < 0.25,
        "MAR: 80% hidden if no relevant<br>experience": (full["relevent_experience"] == "No relevent experience") & (u < 0.8),
        "MNAR: 80% hidden if under 5 years": (full["experience"] < 5) & (u < 0.8)}
titles = []
for name, h in hide.items():
    titles.append(f"{name}<br><span style='font-size:17px'>mean {full['experience'].mean():.1f} "
                  f"to {full.loc[~h, 'experience'].mean():.1f} years, {h.mean() * 100:.0f}% removed</span>")
fig = make_subplots(1, 3, horizontal_spacing=0.06, subplot_titles=titles, shared_yaxes=True)
for j, h in enumerate(hide.values(), start=1):
    for data, col, name in [(full["experience"], RED, "all values"), (full.loc[~h, "experience"], GREEN, "complete cases")]:
        fig.add_trace(go.Histogram(x=data, histnorm="probability density", xbins=dict(start=-0.5, end=20.5, size=1),
                                   marker_color=col, opacity=0.55, name=name, legendgroup=name,
                                   showlegend=(j == 1)), 1, j)
    fig.update_xaxes(title="experience (years)", row=1, col=j)
fig.update_layout(barmode="overlay", legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.22))
fig.update_yaxes(title="density", col=1)
save(fig, "mechanisms", 1300, 560, top=120, legend=True)
