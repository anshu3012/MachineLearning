"""Frequency, relative frequency and cumulative frequency of a 200-person vacation survey: bar, pie and line."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
t = pd.DataFrame({"vacation": ["Beach", "City", "Adventure", "Nature", "Cruise", "Other"],
                  "frequency": [60, 40, 30, 35, 20, 15]})
t["relative"] = t.frequency / t.frequency.sum()
t["cumulative"] = t.frequency.cumsum()
colours = ["#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#9D755D"]
fig = make_subplots(rows=1, cols=3, specs=[[{"type": "xy"}, {"type": "domain"}, {"type": "xy"}]],
                    subplot_titles=["Frequency: bar chart", "Relative frequency: pie chart",
                                    "Cumulative frequency: line chart"], horizontal_spacing=0.09)
fig.add_bar(x=t.vacation, y=t.frequency, marker_color=colours, text=t.frequency, textposition="outside",
            row=1, col=1)
fig.add_pie(labels=t.vacation, values=t.relative, marker=dict(colors=colours), sort=False, direction="clockwise",
            textinfo="label+percent", textfont=dict(size=15), row=1, col=2)
fig.add_scatter(x=t.vacation, y=t.cumulative, mode="lines+markers+text", text=t.cumulative,
                textposition="top left", line=dict(color="#4C78A8", width=3), marker=dict(size=9), row=1, col=3)
fig.update_yaxes(title_text="people", range=[0, 72], row=1, col=1)
fig.update_yaxes(title_text="people so far", range=[0, 225], row=1, col=3)
fig.update_xaxes(tickangle=-40)
fig.update_annotations(font_size=18)
fig.update_layout(template="simple_white", width=1500, height=520, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=16), margin=dict(l=60, r=20, t=60, b=90))
fig.write_image(here / "freq_charts.png", scale=2)
fig.write_image(here / "freq_charts.pdf")
