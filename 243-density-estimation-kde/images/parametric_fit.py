"""Parametric density estimation: 1000 values, a density histogram, the fitted normal and a badly chosen normal."""
from pathlib import Path
import numpy as np
import pandas as pd
import seaborn as sns
import seaborn.objects as so
from scipy import stats

here = Path(__file__).parent
rng = np.random.default_rng(42)                     # same draws as the Notebook
sample = rng.normal(50, 5, 1000)
mu, sigma = sample.mean(), sample.std()
x = np.linspace(sample.min(), sample.max(), 100)
curves = pd.concat([
    pd.DataFrame({"x": x, "density": stats.norm(mu, sigma).pdf(x), "curve": rf"fitted: $\mu$ = {mu:.2f}, $\sigma$ = {sigma:.2f}"}),
    pd.DataFrame({"x": x, "density": stats.norm(60, 12).pdf(x), "curve": r"badly chosen: $\mu$ = 60, $\sigma$ = 12"}),
], ignore_index=True)
plot = (
    so.Plot()
    .add(so.Bars(color="#4C78A8", alpha=0.4), so.Hist(stat="density", bins=10), data=pd.DataFrame({"v": sample}), x="v")
    .add(so.Line(linewidth=3.5), data=curves, x="x", y="density", color="curve")
    .scale(color=so.Nominal(["#F58518", "#E45756"]))
    .label(x="value", y="density", color="", title="1000 values: density histogram and two normal PDFs")
    .layout(size=(8.5, 4.6))
    .theme({**sns.axes_style("whitegrid"), "font.family": "Latin Modern Roman", "font.size": 14,
            "axes.titlesize": 15, "axes.labelsize": 15, "legend.fontsize": 13, "mathtext.fontset": "cm"})
)
plot.save(here / "parametric_fit.png", dpi=200, bbox_inches="tight")
plot.save(here / "parametric_fit.pdf", bbox_inches="tight")
