"""Section 5.2: memory of the four small-number Titanic columns (Survived, Pclass, SibSp, Parch) stored as int64 and
as int8, measured with pandas on data/titanic_train.csv. Plotly."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=19)
df = pd.read_csv(here.parent / "data" / "titanic_train.csv")
cols = ["Survived", "Pclass", "SibSp", "Parch"]
before = int(df[cols].memory_usage(index=False).sum())
after = int(df[cols].astype("int8").memory_usage(index=False).sum())
assert (before, after) == (28512, 3564)
fig = go.Figure(go.Bar(x=["int64: 8 bytes per value", "int8: 1 byte per value"], y=[before, after],
                       marker_color=["#E45756", "#54A24B"], text=[f"{before:,} bytes", f"{after:,} bytes"], textposition="outside"))
fig.update_layout(template="simple_white", width=900, height=420, font=FONT, showlegend=False,
                  title=dict(text="4 columns × 891 rows: 8 times less memory", x=0.5),
                  yaxis=dict(title="memory (bytes)", range=[0, 33000]), margin=dict(l=80, r=20, t=60, b=60))
fig.write_image(here / "dtype_memory.png", scale=2)
fig.write_image(here / "dtype_memory.pdf")
