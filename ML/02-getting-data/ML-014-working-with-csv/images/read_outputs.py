"""What three read_csv options give back, on the Note's own files (Plotly):
dtype_memory.png - memory of the target column as float64 vs int8;
ipl_weekdays.png - matches per weekday, only possible once parse_dates made `date` a real date;
na_values.png    - gender counts before and after na_values=["Male"]."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
LAYOUT = dict(template="simple_white", font=dict(family="Latin Modern Roman", size=24), showlegend=False,
              margin=dict(l=110, r=30, t=40, b=80))

# bytes drawn in encoding_bytes.tex: the UnicodeDecodeError is at position 7044, inside "Bras\xed_lia"
assert (DATA / "zomato.csv").read_bytes()[7040:7049] == b"Bras\xed_lia"

# 1. dtype: bytes for the 1,000 target values
raw = pd.read_csv(DATA / "aug_train.csv")
small = pd.read_csv(DATA / "aug_train.csv", dtype={"target": "int8"})
mem = [raw["target"].memory_usage(index=False), small["target"].memory_usage(index=False)]
assert (str(raw["target"].dtype), mem) == ("float64", [8000, 1000])
fig = go.Figure(go.Bar(x=["float64 (default)", 'dtype={"target": "int8"}'], y=mem, marker_color=[GREY, GREEN],
                       text=[f"{m:,} bytes" for m in mem], textposition="outside", cliponaxis=False, width=0.55))
fig.update_layout(width=900, height=500, yaxis=dict(title="memory of target", range=[0, 9500]), **LAYOUT)
fig.write_image(HERE / "dtype_memory.png", scale=1.5)

# 2. parse_dates: weekday of every match
ipl = pd.read_csv(DATA / "ipl_matches_2008_2020.csv", parse_dates=["date"])
assert len(ipl) == 816 and (ipl["date"].max() - ipl["date"].min()).days == 4589
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
n = ipl["date"].dt.day_name().value_counts()[days]
assert n.sum() == 816 and n.idxmax() == "Sunday"
fig = go.Figure(go.Bar(x=[d[:3] for d in days], y=n.values, text=n.values, textposition="outside", cliponaxis=False,
                       marker_color=[ORANGE if d in ("Saturday", "Sunday") else BLUE for d in days]))
fig.update_layout(width=1000, height=500, yaxis=dict(title="IPL matches, 2008-2020", range=[0, 200]),
                  xaxis=dict(title='ipl["date"].dt.day_name()'), **LAYOUT)
fig.write_image(HERE / "ipl_weekdays.png", scale=1.5)

# 3. na_values: counts of gender before and after
before = raw["gender"].value_counts(dropna=False)
after = pd.read_csv(DATA / "aug_train.csv", na_values=["Male"])["gender"].value_counts(dropna=False)
cats = ["Male", "missing (NaN)", "Female", "Other"]
get = lambda s: [s.get(c, 0) if c != "missing (NaN)" else s[s.index.isna()].sum() for c in cats]
b, a = get(before), get(after)
assert b == [689, 231, 67, 13] and a == [0, 920, 67, 13]
fig = go.Figure([go.Bar(x=cats, y=v, name=nm, marker_color=c, text=v, textposition="outside", cliponaxis=False)
                 for v, nm, c in ((b, "before", GREY), (a, 'after na_values=["Male"]', RED))])
fig.update_layout(width=1000, height=520, barmode="group", yaxis=dict(title="rows", range=[0, 1050]),
                  **{**LAYOUT, "showlegend": True}, legend=dict(x=0.55, y=0.98))
fig.write_image(HERE / "na_values.png", scale=1.5)
