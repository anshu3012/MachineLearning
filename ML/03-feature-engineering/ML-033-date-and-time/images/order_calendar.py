"""Week of the year and quarter on a calendar: rows of orders.csv per date in 2019, laid out by ISO week (columns) and
weekday (rows). The dashed lines mark the start of each quarter."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
d = pd.to_datetime(pd.read_csv(here.parent / "data" / "orders.csv")["date"])
assert (d.dt.year == 2019).sum() == 645
days = pd.date_range("2019-01-01", "2019-12-31")
cnt = d[d.dt.year == 2019].value_counts().reindex(days, fill_value=0)
iso = days.isocalendar()
week = np.where((days.month == 12) & (iso.week == 1), 53, iso.week)   # 30-31 Dec 2019 belong to ISO week 1 of 2020
grid = np.full((7, 54), np.nan)
grid[days.dayofweek, week] = cnt.values
fig = go.Figure(go.Heatmap(z=grid, x=list(range(54)), y=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], xgap=2, ygap=2,
                           colorscale="Blues", colorbar=dict(title="order rows")))
for q, start in ((2, "2019-04-01"), (3, "2019-07-01"), (4, "2019-10-01")):
    w = pd.Timestamp(start).isocalendar().week
    fig.add_vline(x=w - 0.5, line=dict(color="#E45756", width=3, dash="dash"))
    fig.add_annotation(x=w + 4, y=7.1, text=f"Q{q}", showarrow=False, font=dict(size=20, color="#E45756"))
fig.add_annotation(x=4, y=7.1, text="Q1", showarrow=False, font=dict(size=20, color="#E45756"))
fig.update_layout(template="simple_white", width=1500, height=420, font=dict(family="Latin Modern Roman", size=18),
                  title=dict(text="orders.csv in 2019: one cell per day, column = week of the year, row = weekday", x=0.5),
                  xaxis=dict(title="ISO week of the year", range=[0.5, 53.5], dtick=4),
                  yaxis=dict(autorange="reversed", range=[-0.5, 7.6]), margin=dict(l=60, r=20, t=80, b=60))
fig.write_image(here / "order_calendar.png", scale=2)
fig.write_image(here / "order_calendar.pdf")
