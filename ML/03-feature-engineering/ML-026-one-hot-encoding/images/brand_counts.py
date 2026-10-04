"""Cars per brand in the car data: brands with 100 cars or fewer become 'uncommon' (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
THRESHOLD = 100
counts = pd.read_csv(here.parent / "data" / "cars.csv")["brand"].value_counts()
colours = ["#4C78A8" if c > THRESHOLD else "#E45756" for c in counts]
fig = go.Figure(go.Bar(x=counts.index, y=counts.values, marker_color=colours, text=counts.values,
                       textposition="outside", textfont=dict(size=12), cliponaxis=False))
fig.add_hline(y=THRESHOLD, line=dict(color="#6B6B6B", dash="dash"),
              annotation_text="100 cars", annotation_position="top right")
fig.update_layout(template="simple_white", width=1100, height=520, font=dict(family="Latin Modern Roman", size=16),
                  title=dict(text=f"{len(counts)} brands: blue kept (more than 100 cars), red grouped as uncommon", x=0.5),
                  xaxis=dict(tickangle=-60), yaxis=dict(title="Number of cars", range=[0, counts.max() * 1.1]),
                  margin=dict(l=70, r=20, t=60, b=120))
fig.write_image(here / "brand_counts.png", scale=2)
fig.write_image(here / "brand_counts.pdf")
