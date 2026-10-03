"""Charts for Note 42 (placement data): column shapes, the mean +- 3 std limits, and trimming vs capping."""
from pathlib import Path
import numpy as np
import pandas as pd
import seaborn as sns
import seaborn.objects as so
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
df = pd.read_csv(here.parent / "data" / "placement.csv")
mean, std = df["cgpa"].mean(), df["cgpa"].std()
lo, hi = mean - 3 * std, mean + 3 * std
out = (df["cgpa"] < lo) | (df["cgpa"] > hi)

# 1. Seaborn objects: cgpa is bell-shaped, the exam marks are right-skewed
names = {"cgpa": f"cgpa (skew {df['cgpa'].skew():.2f})",
         "placement_exam_marks": f"placement_exam_marks (skew {df['placement_exam_marks'].skew():.2f})"}
long = df[list(names)].rename(columns=names).melt(var_name="column", value_name="value")
THEME = {**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
         "axes.titlesize": 15, "axes.labelsize": 15}
plot = (so.Plot(long, x="value").facet(col="column", order=list(names.values())).share(x=False, y=False)
        .add(so.Bars(color=BLUE, alpha=0.5, edgewidth=0), so.Hist(stat="density", bins=30, common_bins=False))
        .add(so.Line(color=BLUE, linewidth=2.5), so.KDE(common_grid=False, common_norm=False))
        .label(col="", x="value", y="density").layout(size=(10, 4)).theme(THEME))
plot.save(here / "distributions.png", dpi=200, bbox_inches="tight")
plot.save(here / "distributions.pdf", bbox_inches="tight")

# Plotly helpers
FONT = dict(family="Latin Modern Roman", size=20)
BINS = dict(start=4.8, end=9.2, size=0.1)


def save(fig, name, width, height):
    fig.update_layout(template="simple_white", width=width, height=height, showlegend=False, font=FONT,
                      barmode="overlay", bargap=0.05, margin=dict(l=90, r=30, t=70, b=70))
    fig.update_annotations(font_size=19)
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


def limits(fig, **rc):
    for v in (lo, hi):
        fig.add_vline(x=v, line=dict(color=GREY, width=2, dash="dash"), **rc)


# 2. the limits on cgpa and the 5 outliers
fig = go.Figure()
fig.add_trace(go.Histogram(x=df.loc[~out, "cgpa"], xbins=BINS, marker_color=BLUE))
fig.add_trace(go.Histogram(x=df.loc[out, "cgpa"], xbins=BINS, marker_color=RED))
limits(fig)
fig.add_annotation(x=lo, y=1.0, yref="paper", yanchor="bottom", showarrow=False, text=f"lower {lo:.2f}")
fig.add_annotation(x=hi, y=1.0, yref="paper", yanchor="bottom", showarrow=False, text=f"upper {hi:.2f}")
fig.add_annotation(x=lo - 0.12, y=12, showarrow=False, font_color=RED, xanchor="right",
                   text="4.89, 4.90, 4.92")
fig.add_annotation(x=hi + 0.12, y=12, showarrow=False, font_color=RED, xanchor="left", text="8.87, 9.12")
fig.add_annotation(x=5.25, y=55, showarrow=False, font_color=BLUE, xanchor="left", align="left",
                   text=f"995 inside<br>mean {mean:.2f}, std {std:.2f}")
fig.update_xaxes(title="cgpa", range=[4.0, 10.0], dtick=0.5)
fig.update_yaxes(title="students")
save(fig, "limits", 1000, 460)

# 3. before and after: original, trimmed, capped
capped = df["cgpa"].clip(lo, hi)
rows = [("original: 1000 rows", df["cgpa"], out),
        ("trimmed: 995 rows", df.loc[~out, "cgpa"], None),
        ("capped: 1000 rows, min 5.11, max 8.81", capped, out)]
fig = make_subplots(3, 1, shared_xaxes=True, vertical_spacing=0.1, subplot_titles=[r[0] for r in rows])
for i, (_, x, flag) in enumerate(rows, start=1):
    keep = x if flag is None else x[~flag]
    fig.add_trace(go.Histogram(x=keep, xbins=BINS, marker_color=BLUE), i, 1)
    if flag is not None:
        fig.add_trace(go.Histogram(x=x[flag], xbins=BINS, marker_color=RED if i == 1 else ORANGE), i, 1)
    limits(fig, row=i, col=1)
fig.add_annotation(x=lo + 0.05, y=3, xref="x3", yref="y3", ax=-30, ay=-60, arrowcolor=ORANGE, font_color=ORANGE,
                   text="3 values set to 5.11", xanchor="right")
fig.add_annotation(x=hi + 0.05, y=2, xref="x3", yref="y3", ax=30, ay=-60, arrowcolor=ORANGE, font_color=ORANGE,
                   text="2 values set to 8.81", xanchor="left")
fig.update_xaxes(range=[4.0, 10.0], dtick=0.5)
fig.update_xaxes(title="cgpa", row=3, col=1)
fig.update_yaxes(title="students", row=2, col=1)
save(fig, "before_after", 1000, 760)
