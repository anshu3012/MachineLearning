"""Type I error, Type II error and power for the training-program z-test (right-tailed) if the true mean is 52:
alpha = 0.05 (left) and alpha = 0.01 (right). The z statistic follows N(0, 1) under H0 and N(2.19, 1) if mu = 52."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE, ORANGE = "#4C78A8", "#F58518"
shift = (52 - 50) / (5 / np.sqrt(30))           # 2.19
z = np.linspace(-3.5, 6, 900)
h0, h1 = stats.norm.pdf(z), stats.norm.pdf(z, loc=shift)
alphas = [0.05, 0.01]
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.06,
                    subplot_titles=[f"α = {a:.2f}: critical value {stats.norm.ppf(1 - a):.3f}" for a in alphas])
for i, a in enumerate(alphas, start=1):
    c = stats.norm.ppf(1 - a)
    beta = stats.norm.cdf(c - shift)
    left, right = z <= c, z >= c
    fig.add_scatter(x=z[right], y=h1[right], fill="tozeroy", fillcolor="rgba(84,162,75,0.35)", line_width=0,
                    row=1, col=i)                                         # power
    fig.add_scatter(x=z[left], y=h1[left], fill="tozeroy", fillcolor="rgba(245,133,24,0.45)", line_width=0,
                    row=1, col=i)                                         # beta
    fig.add_scatter(x=z[right], y=h0[right], fill="tozeroy", fillcolor="rgba(228,87,86,0.75)", line_width=0,
                    row=1, col=i)                                         # alpha
    fig.add_scatter(x=z, y=h0, mode="lines", line=dict(color=BLUE, width=3), row=1, col=i)
    fig.add_scatter(x=z, y=h1, mode="lines", line=dict(color="black", width=3, dash="dash"), row=1, col=i)
    fig.add_vline(x=c, line=dict(color="black", width=2), opacity=1, row=1, col=i)
    fig.add_annotation(x=-1.6, y=0.37, text="H₀ true: μ = 50", showarrow=False, font=dict(size=17, color=BLUE),
                       row=1, col=i)
    fig.add_annotation(x=4.4, y=0.37, text="H₀ false: μ = 52", showarrow=False, font=dict(size=17), row=1, col=i)
    fig.add_annotation(x=c - 0.3, y=0.05, ax=-150, ay=-60, text=f"β = {beta:.2f}", font_size=18,
                       arrowcolor=ORANGE, arrowwidth=2, row=1, col=i)
    fig.add_annotation(x=shift + 0.6, y=0.2, ax=110, ay=-30, text=f"power = {1 - beta:.2f}", font_size=18, bgcolor="white",
                       arrowcolor="#54A24B", arrowwidth=2, row=1, col=i)
    fig.add_annotation(x=c + 0.25, y=0.012, ax=5.0, ay=0.12, axref=f"x{i if i > 1 else ''}", ayref=f"y{i if i > 1 else ''}", text=f"α = {a:.2f}",
                       font_size=18, arrowcolor="#E45756", arrowwidth=2,
                       row=1, col=i)
    fig.update_xaxes(title_text="z", tickvals=[0, round(shift, 2)], range=[-3.5, 6], row=1, col=i)
fig.update_yaxes(showticklabels=False, range=[0, 0.45])
fig.update_annotations(font_family="Latin Modern Roman")
fig.layout.annotations[0].font.size = fig.layout.annotations[1].font.size = 19
fig.update_layout(template="simple_white", width=1150, height=430, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=20, r=20, t=45, b=50))
fig.write_image(here / "power.png", scale=2)
fig.write_image(here / "power.pdf")
