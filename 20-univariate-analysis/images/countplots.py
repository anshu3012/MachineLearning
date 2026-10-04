"""Count plots of four categorical Titanic columns: how many passengers fall in each group."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic_train.csv")
cols = ["Survived", "Pclass", "Sex", "Embarked"]
fig = make_subplots(2, 2, subplot_titles=cols, vertical_spacing=0.16, horizontal_spacing=0.12)
for i, c in enumerate(cols):
    counts = df[c].astype(str).value_counts().sort_index()
    row, col = i // 2 + 1, i % 2 + 1
    fig.add_trace(go.Bar(x=counts.index, y=counts.values, text=counts.values, textposition="outside",
                         marker=dict(color="#4C78A8", opacity=0.85)), row, col)
    fig.update_xaxes(type="category", row=row, col=col)
    fig.update_yaxes(range=[0, 730], showgrid=True, title="Passengers" if col == 1 else None, row=row, col=col)
fig.update_layout(template="simple_white", width=900, height=760, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=18), margin=dict(l=80, r=20, t=50, b=40))
fig.update_annotations(font_size=20)
fig.write_image(here / "countplots.png", scale=2)
fig.write_image(here / "countplots.pdf")
