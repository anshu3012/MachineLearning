"""The sizes of all 23,410 photos (data/sizes.csv.gz, from experiments/peek.py): width against height, one dot per
photo, and the single size every photo is resized to, 256 x 256. Plotly."""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

HERE = Path(__file__).parent
S = pd.read_csv(HERE.parent / "data" / "sizes.csv.gz")
assert len(S) == 23410 and S.cls.value_counts().to_dict() == {"Cat": 11741, "Dog": 11669}
n_sizes = S[["width", "height"]].drop_duplicates().shape[0]
common = S.groupby(["width", "height"]).size().idxmax()
share = (S.width.eq(common[0]) & S.height.eq(common[1])).mean()
fig = go.Figure()
for cls, col in (("Cat", "#F58518"), ("Dog", "#4C78A8")):
    q = S[S.cls == cls]
    fig.add_scattergl(x=q.width, y=q.height, mode="markers", name=f"{cls.lower()}s",
                      marker=dict(size=4, color=col, opacity=0.25))
fig.add_scatter(x=[256], y=[256], mode="markers", marker=dict(size=18, symbol="x", color="black"),
                name="resized size")
fig.add_annotation(x=256, y=256, ax=120, ay=420, axref="x", ayref="y", text="every photo becomes 256 × 256",
                   showarrow=True, arrowwidth=2, font=dict(size=18), bgcolor="rgba(255,255,255,0.9)")
fig.update_layout(template="simple_white", width=1000, height=700, font=dict(family="Latin Modern Roman", size=20),
                  title=dict(text=f"23,410 photos in {n_sizes:,} different sizes "
                                  f"(the most common, {common[0]} × {common[1]}, is {100 * share:.0f}% of them)",
                             x=0.5, font=dict(size=20)),
                  xaxis=dict(title="width (pixels)", range=[0, 520], constrain="domain"), yaxis=dict(title="height (pixels)", range=[0, 520],
                                                                                 scaleanchor="x"),
                  legend=dict(x=0.02, y=0.98, itemsizing="constant"), margin=dict(l=80, r=30, t=70, b=70))
fig.write_image(HERE / "sizes.png", scale=2)
print(n_sizes, common, round(share, 3), S.width.min(), S.width.max(), S.height.min(), S.height.max())
