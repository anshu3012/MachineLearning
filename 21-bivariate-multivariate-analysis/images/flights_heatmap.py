"""Flights: passengers per month and year (pivot table), shown as a heatmap."""
import plotly.express as px
from common import load, save_px, FONT, MONTHS

f = load("flights")
table = f.pivot_table(values="passengers", index="month", columns="year").reindex(MONTHS)
fig = px.imshow(table, color_continuous_scale="Blues", aspect="auto",
                labels=dict(x="Year", y="Month", color="Passengers<br>(thousands)"))
fig.update_xaxes(tickvals=list(table.columns), side="bottom")
fig.update_layout(template="simple_white", width=950, height=560, font=FONT,
                  title=dict(text="More passengers every year, and most in July and August", x=0.5),
                  margin=dict(l=70, r=20, t=70, b=60))
save_px(fig, "flights_heatmap")
