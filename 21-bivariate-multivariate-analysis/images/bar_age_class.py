"""Titanic: mean age per class, split by sex, with 95% confidence intervals (bootstrap, as seaborn's barplot draws by default)."""
import numpy as np
import plotly.graph_objects as go
from common import load, layout, save_px, BLUE, ORANGE

t = load("titanic_train").dropna(subset=["Age"])
rng = np.random.default_rng(0)
classes = {1: "1st", 2: "2nd", 3: "3rd"}
fig = go.Figure()
for sex, colour in [("male", BLUE), ("female", ORANGE)]:
    means, lo, hi = [], [], []
    for c in classes:
        age = t.Age[(t.Sex == sex) & (t.Pclass == c)].to_numpy()
        boot = rng.choice(age, (1000, len(age))).mean(axis=1)        # 1,000 resamples of the group, mean of each
        m = age.mean()
        means.append(m), lo.append(m - np.percentile(boot, 2.5)), hi.append(np.percentile(boot, 97.5) - m)
    fig.add_bar(x=list(classes.values()), y=means, name=sex, marker=dict(color=colour, opacity=0.8),
                error_y=dict(type="data", symmetric=False, array=hi, arrayminus=lo, color="black", thickness=2, width=6))
layout(fig, "Older passengers travelled in higher classes", "Ticket class", "Mean age (years)", barmode="group",
       legend=dict(title="Sex", x=0.88, y=0.98))
fig.update_yaxes(showgrid=True)
save_px(fig, "bar_age_class")
