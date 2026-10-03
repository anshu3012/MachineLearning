"""Flights: the same month x year pivot table as a clustermap (months and years with similar traffic grouped)."""
from common import load, save_px, clustermap, MONTHS

f = load("flights")
table = f.pivot_table(values="passengers", index="month", columns="year").reindex(MONTHS)
table.index.name, table.columns.name = "Month", "Year"
fig = clustermap(table, "Months and years grouped by similar traffic", "Passengers<br>(thousands)",
                 width=1100, height=700)
fig.update_traces(textfont_size=11, selector=dict(type="heatmap"))
save_px(fig, "flights_clustermap")
