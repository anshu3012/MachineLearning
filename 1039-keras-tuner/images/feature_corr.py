"""Correlation of each of the 8 Pima features with the target Outcome (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, FONT

here = Path(__file__).parent
d = pd.read_csv(here.parent / "data" / "diabetes.csv")
c = d.corr()["Outcome"].drop("Outcome").sort_values()
assert len(d) == 768 and len(c) == 8
assert round(c.Glucose, 2) == 0.47 and round(c.BMI, 2) == 0.29 and round(c.Age, 2) == 0.24
assert round(c.BloodPressure, 2) == 0.07 and round(c.SkinThickness, 2) == 0.07
fig = go.Figure(go.Bar(x=c.values, y=c.index, orientation="h", marker_color=BLUE,
                       text=[f"{v:.2f}" for v in c.values], textposition="outside", textfont=dict(size=18)))
fig.update_layout(template="simple_white", width=850, height=480, font=dict(FONT, size=18),
                  xaxis=dict(title="correlation with Outcome (diabetes)", range=[0, 0.55]),
                  margin=dict(l=20, r=20, t=20, b=60))
fig.write_image(here / "feature_corr.png", scale=2)
fig.write_image(here / "feature_corr.pdf")
