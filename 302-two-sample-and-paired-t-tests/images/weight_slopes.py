"""Weight-loss program: each line is one participant's weight before and after (data/weight_loss.csv);
green = lost weight, red = gained."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
w = pd.read_csv(here.parent / "data" / "weight_loss.csv")
fig = go.Figure()
for _, r in w.iterrows():
    colour = "#54A24B" if r.after < r.before else ("#E45756" if r.after > r.before else "#6B6B6B")
    fig.add_scatter(x=["before", "after"], y=[r.before, r.after], mode="lines+markers",
                    line=dict(color=colour, width=2.5), marker=dict(size=9))
fig.add_annotation(x=1.02, y=w.after.max(), xref="paper", text="gained", showarrow=False,
                   font=dict(color="#E45756", size=17), xanchor="left")
fig.add_annotation(x=1.02, y=w.after.max() - 3, xref="paper", text="lost", showarrow=False,
                   font=dict(color="#54A24B", size=17), xanchor="left")
fig.update_yaxes(title_text="weight (kg)")
fig.update_layout(template="simple_white", width=620, height=460, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=60, r=90, t=20, b=40))
fig.write_image(here / "weight_slopes.png", scale=2)
fig.write_image(here / "weight_slopes.pdf")
