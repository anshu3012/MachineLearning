"""Remove or impute, on four real rows of the job data (rows 0 to 3; row 3 has no enrolled_university value):
removing the row drops its three good values too; imputing fills the gap with the column's mode, no_enrollment."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "data_science_job.csv.gz")
cols = ["city_development_index", "enrolled_university", "experience", "training_hours"]
t = df[cols].head(4)
mode = df["enrolled_university"].mode()[0]
assert t["enrolled_university"].isna().tolist() == [False, False, False, True] and mode == "no_enrollment"
fmt = lambda v: "NaN" if pd.isna(v) else (f"{v:g}" if isinstance(v, float) else str(v))
short = ["city_dev_index", "enrolled_univ", "experience", "training_hours"]
fig = make_subplots(rows=1, cols=3, specs=[[{"type": "table"}] * 3], horizontal_spacing=0.03,
                    subplot_titles=["the data: row 3 has a gap", "remove: row 3 is gone, with its 3 good values",
                                    "impute: the gap gets the mode, no_enrollment"])
views = [(t, None), (t.iloc[:3], None), (t.fillna({"enrolled_university": mode}), (3, 1))]
for j, (v, hot) in enumerate(views, start=1):
    vals = [[fmt(x) for x in v[c]] for c in cols]
    fill = [["#ffe2c4" if (hot and r == hot[0] and ci == hot[1]) or (j == 1 and r == 3 and ci == 1) else
             ("#fbe3e3" if j == 1 and r == 3 else "white") for r in range(len(v))] for ci in range(4)]
    fig.add_trace(go.Table(header=dict(values=short, fill_color="#4C78A8", font=dict(color="white", size=15), height=32),
                           cells=dict(values=vals, fill_color=fill, font=dict(size=16), height=32)), row=1, col=j)
for a in fig.layout.annotations:
    a.font.size = 18
fig.update_layout(width=1600, height=300, font=dict(family="Latin Modern Roman", size=16), margin=dict(l=10, r=10, t=50, b=0))
fig.write_image(here / "remove_vs_impute.png", scale=2)
fig.write_image(here / "remove_vs_impute.pdf")
