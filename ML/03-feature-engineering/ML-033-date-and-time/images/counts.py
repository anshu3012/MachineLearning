"""Plotly chart for Note ML-033: orders rows per weekday, and messages per hour of the day."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
BLUE, ORANGE = "#4C78A8", "#F58518"
orders = pd.read_csv(here.parent / "data" / "orders.csv", parse_dates=["date"])
messages = pd.read_csv(here.parent / "data" / "messages.csv", parse_dates=["date"])

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dow = orders["date"].dt.day_name().value_counts().reindex(days)
hour = messages["date"].dt.hour.value_counts().reindex(range(24), fill_value=0)

fig = make_subplots(1, 2, horizontal_spacing=0.1, column_widths=[0.42, 0.58],
                    subplot_titles=["orders.csv: rows per day of week", "messages.csv: messages per hour"])
fig.add_trace(go.Bar(x=[d[:3] for d in days], y=dow.values, text=dow.values, textposition="outside",
                     marker_color=[ORANGE if d in ("Saturday", "Sunday") else BLUE for d in days]), 1, 1)
fig.add_trace(go.Bar(x=hour.index, y=hour.values, text=[v if v else "" for v in hour.values],
                     textposition="outside", marker_color=BLUE), 1, 2)
fig.update_yaxes(title="rows", range=[0, 210], row=1, col=1)
fig.update_yaxes(title="messages", range=[0, 450], row=1, col=2)
fig.update_xaxes(title="day of week (weekend in orange)", row=1, col=1)
fig.update_xaxes(title="hour (0 = midnight to 1 am)", dtick=2, range=[-0.6, 23.6], row=1, col=2)
fig.update_layout(template="simple_white", width=1200, height=480, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=70, r=20, t=60, b=70))
fig.update_annotations(font_size=22)
fig.update_traces(cliponaxis=False, textfont_size=18)
fig.update_layout(uniformtext_minsize=18, uniformtext_mode="show")
fig.write_image(here / "counts.png", scale=2)
fig.write_image(here / "counts.pdf")
