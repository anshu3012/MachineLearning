"""Plotly figures for the test chooser, all computed from data/people.csv:
dataset_counts, proportion_null, chi_square_shares, groups."""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
people = pd.read_csv(here.parent / "data" / "people.csv")
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=20)
ages = ["child", "adult", "elderly"]


def save(fig, name, w, h):
    fig.update_layout(template="simple_white", width=w, height=h, font=FONT, showlegend=False)
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


# ---- the six tests of the Note ----
n = len(people)
men = (people.gender == "male").sum()
z = (men / n - 0.5) / np.sqrt(0.25 / n)
p_prop = 2 * stats.norm.sf(abs(z))
table = pd.crosstab(people.gender, people.age_group)[ages]
chi2, p_chi, _, _ = stats.chi2_contingency(table)
p_t1 = stats.ttest_1samp(people.height, 1.55).pvalue
p_r = stats.pearsonr(people.height, people.weight).pvalue
adults = people[people.age_group == "adult"]
p_t2 = stats.ttest_ind(adults[adults.gender == "male"].height, adults[adults.gender == "female"].height).pvalue
p_anova = stats.f_oneway(*[people[people.age_group == a].weight for a in ages]).pvalue
print(f"z={z:.2f} p={p_prop:.2f}; chi2={chi2:.2f} p={p_chi:.2f}; t1 p={p_t1:.2f}; r p={p_r:.1e}; t2 p={p_t2:.1e}; anova p={p_anova:.1e}")

# dataset_counts: the two categorical features
fig = make_subplots(rows=1, cols=2, subplot_titles=("gender", "age group"), horizontal_spacing=0.12)
fig.update_annotations(font_size=24)
g = people.gender.value_counts()[["female", "male"]]
a = people.age_group.value_counts()[ages]
fig.add_trace(go.Bar(x=g.index, y=g.values, marker_color=[ORANGE, BLUE], text=g.values, textposition="outside"), 1, 1)
fig.add_trace(go.Bar(x=a.index, y=a.values, marker_color=GREEN, text=a.values, textposition="outside"), 1, 2)
fig.update_traces(textfont=dict(size=22), width=0.6)
fig.update_yaxes(range=[0, 40], title_text="people", row=1, col=1)
fig.update_yaxes(range=[0, 40], row=1, col=2)
fig.update_layout(margin=dict(l=80, r=20, t=50, b=50))
save(fig, "dataset_counts", 900, 420)

# proportion_null: sampling distribution of p-hat if H0 (pi = 0.5) were true
se = np.sqrt(0.25 / n); ph = men / n
x = np.linspace(0.25, 0.75, 400); y = stats.norm.pdf(x, 0.5, se)
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color=GREY, width=3)))
for lo, hi in ((0.25, ph), (1 - ph, 0.75)):
    m = (x <= hi) & (x >= lo)
    fig.add_trace(go.Scatter(x=np.r_[x[m], x[m][::-1]], y=np.r_[y[m], np.zeros(m.sum())], fill="toself",
                             fillcolor="rgba(228,87,86,0.35)", line=dict(width=0)))
fig.add_vline(x=ph, line=dict(color=BLUE, width=3), opacity=1, layer="above")
fig.add_annotation(x=ph, y=y.max() * 1.02, text=f"our sample: {men}/60 = {ph:.3f}", showarrow=False, xanchor="right",
                   font=dict(size=20, color=BLUE))
fig.add_annotation(x=0.5, y=y.max() * 0.45, text=f"shaded: p = {p_prop:.2f}", showarrow=False, font=dict(size=22, color=RED))
fig.update_xaxes(title="share of men in a sample of 60, if the population is 50/50", range=[0.25, 0.75])
fig.update_yaxes(visible=False)
fig.update_layout(margin=dict(l=20, r=20, t=40, b=70))
save(fig, "proportion_null", 900, 420)

# chi_square_shares: share of men in each age group against the overall share
share = (table.loc["male"] / table.sum()).reindex(ages)
fig = go.Figure()
fig.add_trace(go.Bar(x=ages, y=share.values, marker_color=BLUE, width=0.55,
                     text=[f"{table.loc['male', a]}/{table[a].sum()}" for a in ages], textposition="inside", insidetextanchor="end", textfont_color="white"))
fig.add_hline(y=men / n, line=dict(color=GREY, dash="dash", width=3), layer="above", opacity=1)
fig.add_annotation(xref="paper", x=1.0, y=men / n, text=f"all: {men}/60", xanchor="left", xshift=8, showarrow=False,
                   font=dict(size=20, color=GREY))
fig.update_traces(textfont=dict(size=22))
fig.update_yaxes(title="share of men", range=[0, 0.7])
fig.update_layout(title=dict(text=f"χ² = {chi2:.2f}, p = {p_chi:.2f}", x=0.5), margin=dict(l=90, r=130, t=60, b=50))
save(fig, "chi_square_shares", 800, 440)

# groups: two groups (t-test) vs three groups (ANOVA)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.14,
                    subplot_titles=("2 groups: t-test", "3 groups: ANOVA"))
fig.update_annotations(font_size=24)
for gname, c in (("female", ORANGE), ("male", BLUE)):
    v = adults[adults.gender == gname].height
    fig.add_trace(go.Box(y=v, name=f"adult {gname}", marker_color=c, boxpoints="all", jitter=0.4, pointpos=0), 1, 1)
for aname, c in zip(ages, (ORANGE, BLUE, GREEN)):
    v = people[people.age_group == aname].weight
    fig.add_trace(go.Box(y=v, name=aname, marker_color=c, boxpoints="all", jitter=0.4, pointpos=0), 1, 2)
fig.update_yaxes(title_text="height (m)", row=1, col=1)
fig.update_yaxes(title_text="weight (kg)", row=1, col=2)
fig.update_layout(margin=dict(l=80, r=20, t=50, b=50))
save(fig, "groups", 1000, 460)
