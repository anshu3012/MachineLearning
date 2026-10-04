"""Why mean imputation weakens a relationship: Age against Family in the training set before and after filling the
148 missing ages with the mean. The filled points form a flat line at the mean, which carries no trend, so the
correlation falls from -0.299 to -0.245 (the Note's numbers)."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.model_selection import train_test_split

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic_toy.csv")
Xtr, _, _, _ = train_test_split(df.drop(columns="Survived"), df["Survived"], test_size=0.2, random_state=2)
miss = Xtr.Age.isna()
filled = Xtr.Age.fillna(Xtr.Age.mean())
r0, r1 = Xtr.Age.corr(Xtr.Family), filled.corr(Xtr.Family)
assert len(Xtr) == 712 and round(r0, 3) == -0.299 and round(r1, 3) == -0.245
jit = np.random.default_rng(0).uniform(-0.25, 0.25, len(Xtr))
fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.05,
                    subplot_titles=[f"before: {(~miss).sum()} known ages, correlation {r0:.3f}",
                                    f"after mean imputation: correlation {r1:.3f}"])
fig.add_scatter(x=Xtr.Family[~miss] + jit[~miss], y=Xtr.Age[~miss], mode="markers",
                marker=dict(size=6, color="#4C78A8", opacity=0.5), row=1, col=1)
fig.add_scatter(x=Xtr.Family[~miss] + jit[~miss], y=Xtr.Age[~miss], mode="markers",
                marker=dict(size=6, color="#4C78A8", opacity=0.5), row=1, col=2)
fig.add_scatter(x=Xtr.Family[miss] + jit[miss], y=filled[miss], mode="markers",
                marker=dict(size=7, color="#E45756", opacity=0.8), name=f"{miss.sum()} filled ages", row=1, col=2)
fig.add_annotation(x=8, y=Xtr.Age.mean(), text=f"{miss.sum()} filled ages, all {Xtr.Age.mean():.1f}", ax=0, ay=-50,
                   font=dict(size=17, color="#E45756"), row=1, col=2)
for c in (1, 2):
    fig.update_xaxes(title_text="Family (relatives aboard)", row=1, col=c)
fig.update_yaxes(title_text="Age", row=1, col=1)
for a in fig.layout.annotations[:2]:
    a.font.size = 19
fig.update_layout(template="simple_white", width=1400, height=520, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=60, b=60))
fig.write_image(here / "age_family_scatter.png", scale=2)
fig.write_image(here / "age_family_scatter.pdf")
