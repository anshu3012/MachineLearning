"""The joint test of independence on the Titanic table: for each class, the actual joint probability
P(class, died) against the product P(class) P(died) that independence would require (0.616 x P(class))."""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic_train.csv")
J = pd.crosstab(df["Pclass"], df["Survived"], normalize="all")
actual = J[0].values
product = J.sum(axis=1).values * J[0].sum()
assert actual.round(3).tolist() == [0.090, 0.109, 0.418] and round(product[0], 3) == 0.149
x = ["class 1", "class 2", "class 3"]
fig = go.Figure()
fig.add_bar(x=x, y=product, name="if independent: P(class) × P(died)", marker_color="#BAB0AC",
            text=[f"{v:.3f}" for v in product], textposition="outside")
fig.add_bar(x=x, y=actual, name="actual: P(class, died)", marker_color="#E45756", text=[f"{v:.3f}" for v in actual],
            textposition="outside")
fig.update_yaxes(title_text="joint probability", range=[0, 0.48])
fig.update_layout(template="simple_white", width=900, height=480, barmode="group",
                  font=dict(family="Latin Modern Roman", size=22), legend=dict(x=0.01, y=1.0),
                  margin=dict(l=80, r=20, t=20, b=50))
fig.write_image(here / "independence_check.png", scale=2)
fig.write_image(here / "independence_check.pdf")
