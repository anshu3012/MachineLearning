"""The categorical features of the car data at a glance: fuel (4 categories) and owner (5 categories), with the
number of cars in each; each category becomes one one-hot column."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "cars.csv")
fuel, owner = df.fuel.value_counts(), df.owner.value_counts()
assert len(df) == 8128 and fuel.to_dict() == {"Diesel": 4402, "Petrol": 3631, "CNG": 57, "LPG": 38} and len(owner) == 5
fig = make_subplots(rows=1, cols=2, column_widths=[0.42, 0.58], horizontal_spacing=0.1,
                    subplot_titles=["fuel: 4 categories → 4 columns", "owner: 5 categories → 5 columns"])
for j, c in enumerate((fuel, owner), start=1):
    fig.add_bar(x=c.index, y=c.values, text=c.values, textposition="outside", marker_color="#4C78A8",
                cliponaxis=False, row=1, col=j)
    fig.update_yaxes(title_text="cars" if j == 1 else None, range=[0, 6000], row=1, col=j)
fig.update_xaxes(tickangle=-25)
fig.update_annotations(font_size=20)
fig.update_layout(template="simple_white", width=1300, height=500, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=60, b=110))
fig.write_image(here / "car_categories.png", scale=2)
fig.write_image(here / "car_categories.pdf")
