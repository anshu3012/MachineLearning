"""Flights: total passengers per year (groupby year, sum), drawn as a line plot."""
import plotly.graph_objects as go
from common import load, layout, save_px, BLUE

yearly = load("flights").groupby("year", as_index=False)["passengers"].sum()
fig = go.Figure(go.Scatter(x=yearly.year, y=yearly.passengers, mode="lines+markers", line=dict(color=BLUE, width=4), marker=dict(size=10)))
layout(fig, "Air passengers per year, 1949 to 1960", "Year", "Passengers (thousands)")
fig.update_xaxes(dtick=1, showgrid=True)
fig.update_yaxes(showgrid=True, rangemode="tozero")
save_px(fig, "line_flights")
