"""A 3D scatter plot: three numerical columns of the tips data at once, coloured by a fourth (time)."""
from pathlib import Path
import pandas as pd
import plotly.express as px

here = Path(__file__).parent
tips = pd.read_csv(here.parent / "data" / "tips.csv")
fig = px.scatter_3d(tips, x="total_bill", y="size", z="tip", color="time",
                    color_discrete_map={"Lunch": "#F58518", "Dinner": "#4C78A8"})
fig.update_traces(marker=dict(size=4, opacity=0.85))
fig.update_layout(width=900, height=560, font=dict(family="Latin Modern Roman", size=15),
                  scene=dict(xaxis_title="total bill", yaxis_title="party size", zaxis_title="tip",
                             camera=dict(eye=dict(x=1.6, y=-1.6, z=0.6))),
                  legend=dict(title="", x=0.8, y=0.85), margin=dict(l=0, r=0, t=0, b=0))
fig.write_image(here / "scatter_3d.png", scale=2)
fig.write_image(here / "scatter_3d.pdf")
