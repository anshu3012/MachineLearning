"""Flights: total passengers per year (groupby year, sum), drawn as a line plot."""
import seaborn.objects as so
from common import load, save_so, THEME, BLUE

yearly = load("flights").groupby("year", as_index=False)["passengers"].sum()
plot = (
    so.Plot(yearly, x="year", y="passengers")
    .add(so.Line(color=BLUE, linewidth=3))
    .add(so.Dot(color=BLUE, pointsize=8))
    .scale(x=so.Continuous().tick(every=1))
    .label(x="Year", y="Passengers (thousands)", title="Air passengers per year, 1949 to 1960")
    .layout(size=(8, 4.6))
    .theme(THEME)
)
save_so(plot, "line_flights")
