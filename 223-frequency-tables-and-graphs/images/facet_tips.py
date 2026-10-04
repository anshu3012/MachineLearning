"""A facet grid: one scatter plot of bill vs tip per meal time, smokers by colour: four features in one figure.
Plotly."""
from pathlib import Path
import pandas as pd
import plotly.express as px

here = Path(__file__).parent
tips = pd.read_csv(here.parent / "data" / "tips.csv")
fig = px.scatter(tips, x="total_bill", y="tip", color="smoker", facet_col="time",
                 category_orders={"time": ["Lunch", "Dinner"], "smoker": ["No", "Yes"]},
                 color_discrete_map={"No": "#4C78A8", "Yes": "#F58518"}, opacity=0.8,
                 labels={"total_bill": "total bill", "tip": "tip", "smoker": "smoker"})
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1], font_size=20))
fig.update_traces(marker=dict(size=8))
fig.update_xaxes(showgrid=True)
fig.update_yaxes(showgrid=True)
fig.update_layout(template="simple_white", width=1000, height=450, font=dict(family="Latin Modern Roman", size=18),
                  margin=dict(l=60, r=20, t=40, b=60))
fig.write_image(here / "facet_tips.png", scale=2)
fig.write_image(here / "facet_tips.pdf")
