"""Charts for Note ML-043 (weight-height data): percentile limits on Height, trimming vs capping, three rules compared."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, PURPLE, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=20)
BINS = dict(start=54, end=79.5, size=0.5)
h = pd.read_csv(here.parent / "data" / "weight-height.csv")["Height"]
lo, hi = h.quantile([0.01, 0.99])
out = (h < lo) | (h > hi)


def save(fig, name, width, height):
    fig.update_layout(template="simple_white", width=width, height=height, showlegend=False, font=FONT,
                      barmode="overlay", bargap=0.05, margin=dict(l=90, r=30, t=70, b=70))
    fig.update_annotations(font_size=19)
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


def box(values):
    # quartilemethod="linear" gives the same quartiles as pandas
    return go.Box(x=values, boxpoints="outliers", quartilemethod="linear", marker=dict(color=RED, size=7),
                  line=dict(color=BLUE, width=2.5), fillcolor="rgba(76,120,168,0.25)", name="")


def limits(fig, **rc):
    for v in (lo, hi):
        fig.add_vline(x=v, line=dict(color=GREY, width=2, dash="dash"), **rc)


# 1. box plot and histogram of Height with the 1st and 99th percentiles
fig = make_subplots(2, 1, shared_xaxes=True, vertical_spacing=0.06, row_heights=[0.3, 0.7])
fig.add_trace(box(h), 1, 1)
fig.add_trace(go.Histogram(x=h[~out], xbins=BINS, marker_color=BLUE), 2, 1)
fig.add_trace(go.Histogram(x=h[out], xbins=BINS, marker_color=RED), 2, 1)
limits(fig, row="all", col=1)
fig.add_annotation(x=lo, y=1.0, xref="x", yref="paper", yanchor="bottom", showarrow=False,
                   text=f"1st percentile {lo:.2f}")
fig.add_annotation(x=hi, y=1.0, xref="x", yref="paper", yanchor="bottom", showarrow=False,
                   text=f"99th percentile {hi:.2f}")
fig.add_annotation(x=lo - 0.3, y=170, xref="x2", yref="y2", xanchor="right", showarrow=False, font_color=RED,
                   align="right", text="100 heights<br>below")
fig.add_annotation(x=hi + 0.3, y=170, xref="x2", yref="y2", xanchor="left", showarrow=False, font_color=RED,
                   align="left", text="100 heights<br>above")
fig.update_xaxes(range=[53.5, 80], dtick=2)
fig.update_xaxes(title="Height (inches)", row=2, col=1)
fig.update_yaxes(showticklabels=False, showline=False, ticks="", row=1, col=1)
fig.update_yaxes(title="people", row=2, col=1)
save(fig, "limits", 1000, 600)

# 2. before and after: original, trimmed, capped (histogram left, box plot right)
capped = h.clip(lo, hi)
trimmed = h[~out]
rows = [("original: 10,000 rows, 200 outliers", h, out, RED),
        (f"trimmed: {len(trimmed):,} rows", trimmed, None, None),
        ("capped (winsorized): 10,000 rows, 200 values moved", capped, out, ORANGE)]
titles = [t for r in rows for t in (r[0], "")]
fig = make_subplots(3, 2, shared_xaxes=True, vertical_spacing=0.11, horizontal_spacing=0.06,
                    column_widths=[0.6, 0.4], subplot_titles=titles)
for i, (_, v, flag, colour) in enumerate(rows, start=1):
    keep = v if flag is None else v[~flag]
    fig.add_trace(go.Histogram(x=keep, xbins=BINS, marker_color=BLUE), i, 1)
    if flag is not None:
        fig.add_trace(go.Histogram(x=v[flag], xbins=BINS, marker_color=colour), i, 1)
    fig.add_trace(box(v), i, 2)
    limits(fig, row=i, col=1)
    limits(fig, row=i, col=2)
fig.add_annotation(x=lo, y=100, xref="x5", yref="y5", ax=0, ay=-110, arrowcolor=ORANGE, font_color=ORANGE,
                   text="100 at 58.13", xanchor="center")
fig.add_annotation(x=hi, y=100, xref="x5", yref="y5", ax=0, ay=-110, arrowcolor=ORANGE, font_color=ORANGE,
                   text="100 at 74.79", xanchor="center")
fig.update_xaxes(range=[53.5, 80], dtick=4)
fig.update_xaxes(title="Height (inches)", row=3)
fig.update_yaxes(showticklabels=False, showline=False, ticks="", col=2)
fig.update_yaxes(title="people", row=2, col=1)
fig.update_yaxes(range=[0, 520], col=1)
save(fig, "before_after", 1100, 820)

# 3. the three detection rules on the same column
mean, std = h.mean(), h.std()
q1, q3 = h.quantile([0.25, 0.75])
iqr = q3 - q1
rules = [("percentiles 1 and 99", lo, hi, GREEN),
         ("IQR fences", q1 - 1.5 * iqr, q3 + 1.5 * iqr, PURPLE),
         ("z-score: mean ± 3 std", mean - 3 * std, mean + 3 * std, BLUE)]
fig = make_subplots(2, 1, shared_xaxes=True, vertical_spacing=0.08, row_heights=[0.55, 0.45])
fig.add_trace(go.Histogram(x=h, xbins=BINS, marker_color="rgba(107,107,107,0.45)"), 1, 1)
for name, a, b, colour in rules:
    n = int(((h < a) | (h > b)).sum())
    fig.add_trace(go.Scatter(x=[a, b], y=[name, name], mode="lines+markers",
                             line=dict(color=colour, width=5), marker=dict(size=13, color=colour)), 2, 1)
    fig.add_annotation(x=b + 0.4, y=name, xref="x2", yref="y2", xanchor="left", showarrow=False,
                       font_color=colour, text=f"{n} outliers")
    for v in (a, b):
        fig.add_vline(x=v, line=dict(color=colour, width=3, dash="dash"), opacity=1, row=1, col=1)
fig.update_xaxes(range=[53.5, 83], dtick=2)
fig.update_xaxes(title="Height (inches)", row=2, col=1)
fig.update_yaxes(title="people", row=1, col=1)
fig.update_yaxes(range=[-0.6, 2.6], row=2, col=1)
save(fig, "three_rules", 1100, 640)

# 4. a percentile is a value at a rank: the 10,000 heights sorted, the 100 shortest and 100 tallest in red (Section 2)
s = h.sort_values().to_numpy()
rank = range(1, len(s) + 1)
assert (s[:100] < lo).all() and (s[100] >= lo) and (s[-100:] > hi).all() and (s[-101] <= hi)
fig = go.Figure()
fig.add_trace(go.Scatter(x=list(rank)[100:-100], y=s[100:-100], mode="lines", line=dict(color=BLUE, width=4)))
for sl in (slice(0, 100), slice(-100, None)):
    fig.add_trace(go.Scatter(x=list(rank)[sl], y=s[sl], mode="lines", line=dict(color=RED, width=6)))
for v, t in ((lo, f"1st percentile {lo:.2f}"), (hi, f"99th percentile {hi:.2f}")):
    fig.add_hline(y=v, line=dict(color=GREY, width=2, dash="dash"))
    fig.add_annotation(x=5000, y=v, yshift=14 if v == hi else -14, showarrow=False, text=t)
fig.add_annotation(x=60, y=56, ax=90, ay=0, xanchor="left", font_color=RED, arrowcolor=RED,
                   text="the 100 shortest")
fig.add_annotation(x=9900, y=s[-1], ax=-60, ay=-10, xanchor="right", font_color=RED, arrowcolor=RED,
                   text="the 100 tallest")
fig.update_xaxes(title="rank (shortest = 1)", range=[-200, 10200], tickformat=",")
fig.update_yaxes(title="Height (inches)", range=[53, 80])
save(fig, "sorted_heights", 1000, 500)

# 5. the fixed share on Weight: the box-plot fences flag 1 value, the 1st and 99th percentiles flag 200 (Section 10)
w = pd.read_csv(here.parent / "data" / "weight-height.csv")["Weight"]
wq1, wq3 = w.quantile([0.25, 0.75])
flo, fhi = wq1 - 1.5 * (wq3 - wq1), wq3 + 1.5 * (wq3 - wq1)
plo, phi = w.quantile([0.01, 0.99])
pout = (w < plo) | (w > phi)
assert ((w < flo) | (w > fhi)).sum() == 1 and pout.sum() == 200
WB = dict(start=60, end=275, size=5)
fig = go.Figure()
fig.add_trace(go.Histogram(x=w[~pout], xbins=WB, marker_color=BLUE))
fig.add_trace(go.Histogram(x=w[pout], xbins=WB, marker_color=RED))
for v, s_ in ((flo, "left"), (fhi, "right")):
    fig.add_vline(x=v, line=dict(color=GREEN, width=4, dash="dot"), opacity=1)
for v in (plo, phi):
    fig.add_vline(x=v, line=dict(color=RED, width=3, dash="dash"), opacity=1)
fig.add_annotation(x=w.max(), y=2, ax=-10, ay=-200, arrowcolor=GREEN, font_color=GREEN, xanchor="right",
                   text=f"the 1 box-plot outlier: {w.max():.0f}")
fig.add_annotation(x=0.5, y=1.0, xref="paper", yref="paper", yanchor="bottom", showarrow=False,
                   text="<span style='color:#54A24B'>dotted: box-plot fences, 1 outlier</span>"
                        "     <span style='color:#E45756'>dashed: 1st and 99th percentiles, 200 flagged</span>")
fig.update_xaxes(title="Weight (pounds)", range=[50, 280], dtick=20)
fig.update_yaxes(title="people")
save(fig, "weight_share", 1100, 480)
