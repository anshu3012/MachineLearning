"""Six shapes a histogram can take, from synthetic data with a fixed seed."""
from pathlib import Path
import numpy as np
import pandas as pd
import seaborn as sns
import seaborn.objects as so

here = Path(__file__).parent
rng = np.random.default_rng(1)
n = 5000
shapes = {
    "symmetric": rng.normal(50, 10, n),
    "bimodal": np.concatenate([rng.normal(35, 6, n // 2), rng.normal(68, 6, n // 2)]),
    "right skew (long tail right)": 20 + rng.gamma(2, 9, n),
    "left skew (long tail left)": 100 - rng.gamma(2, 9, n),
    "uniform": rng.uniform(10, 90, n),
    "no pattern (too many bins)": rng.normal(50, 15, 60),
}
df = pd.concat([pd.DataFrame({"value": v, "shape": k}) for k, v in shapes.items()])
plot = (
    so.Plot(df, x="value")
    .facet(col="shape", wrap=3, order=list(shapes))
    .add(so.Bars(color="#4C78A8"), so.Hist(stat="proportion", bins=30, common_bins=False, common_norm=False))
    .share(x=False, y=False)
    .label(x="", y="share of values", title="{}".format)
    .layout(size=(11, 6))
    .theme({**sns.axes_style("white"), "font.family": "Latin Modern Roman", "font.size": 13,
            "axes.titlesize": 15, "axes.labelsize": 14})
)
plot.save(here / "hist_shapes.png", dpi=200, bbox_inches="tight")
plot.save(here / "hist_shapes.pdf", bbox_inches="tight")
