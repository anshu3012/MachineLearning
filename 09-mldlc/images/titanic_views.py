"""Two previews on the Titanic training file (891 passengers, also used in the pipelines Note):
dirty_data.png   - what preprocessing must fix: missing values, an outlier, very different scales;
eda_views.png    - EDA in miniature: one feature alone, a feature against the target, class balance. Plotly."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
df = pd.read_csv(HERE.parent / "data" / "titanic_train.csv")
miss = df.isnull().sum()
assert len(df) == 891 and miss[["Cabin", "Age", "Embarked"]].tolist() == [687, 177, 2]
assert round(df.Fare.max(), 2) == 512.33 and round(df.Fare.median(), 2) == 14.45 and df.Age.max() == 80
surv = df.groupby("Sex").Survived.mean()
counts = df.Survived.value_counts()
assert counts.tolist() == [549, 342] and round(surv["female"], 2) == 0.74 and round(surv["male"], 2) == 0.19
LAYOUT = dict(template="simple_white", font=dict(family="Latin Modern Roman", size=22), showlegend=False,
              margin=dict(l=70, r=20, t=80, b=70))

# 1. dirty data
fig = make_subplots(1, 3, horizontal_spacing=0.09, subplot_titles=(
    "Missing values", "Outliers: Fare", "Different scales"))
m = miss[miss > 0].sort_values()
fig.add_trace(go.Bar(x=m.values, y=m.index, orientation="h", marker_color=RED, text=m.values,
                     textposition="outside", cliponaxis=False), 1, 1)
fig.update_xaxes(range=[0, 850], title="empty cells (of 891)", row=1, col=1)
fig.add_trace(go.Box(y=df.Fare, marker_color=BLUE, boxpoints="outliers", name="Fare"), 1, 2)
fig.add_annotation(x=0, y=512.33, text="512 (median 14)", showarrow=True, ax=70, ay=30, font=dict(color=RED),
                   row=1, col=2)
fig.update_yaxes(title="fare", row=1, col=2)
for name, s, c in (("Age", df.Age, GREEN), ("Fare", df.Fare, ORANGE)):
    fig.add_trace(go.Scatter(x=[name, name], y=[s.min(), s.max()], mode="lines+markers+text", line=dict(color=c, width=14),
                             text=[f"{s.min():g}", f"{s.max():.0f}"], textposition=["bottom center", "top center"],
                             marker=dict(size=4, color=c), cliponaxis=False), 1, 3)
fig.update_yaxes(range=[-70, 580], title="range of values", row=1, col=3)
fig.update_layout(width=1300, height=520, **LAYOUT)
fig.update_annotations(font_size=24)
fig.write_image(HERE / "dirty_data.png", scale=1.5)

# 2. EDA views
fig = make_subplots(1, 3, horizontal_spacing=0.09, subplot_titles=(
    "Univariate: Age", "Bivariate: Sex vs survival", "Balance of the target"))
fig.add_trace(go.Histogram(x=df.Age, xbins=dict(start=0, end=80, size=5), marker_color=BLUE), 1, 1)
fig.update_xaxes(title="age (years)", row=1, col=1)
fig.update_yaxes(title="passengers", row=1, col=1)
fig.add_trace(go.Bar(x=["female", "male"], y=surv[["female", "male"]] * 100, marker_color=[ORANGE, BLUE],
                     text=[f"{v:.0%}" for v in surv[["female", "male"]]], textposition="outside", cliponaxis=False), 1, 2)
fig.update_yaxes(title="survived (percent)", range=[0, 90], row=1, col=2)
fig.add_trace(go.Bar(x=["died (0)", "survived (1)"], y=[counts[0], counts[1]], marker_color=[GREY, GREEN],
                     text=[counts[0], counts[1]], textposition="outside", cliponaxis=False), 1, 3)
fig.update_yaxes(title="passengers", range=[0, 650], row=1, col=3)
fig.update_layout(width=1300, height=520, bargap=0.25, **LAYOUT)
fig.update_annotations(font_size=24)
fig.write_image(HERE / "eda_views.png", scale=1.5)
