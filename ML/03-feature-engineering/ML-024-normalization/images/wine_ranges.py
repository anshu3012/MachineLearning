"""What MinMaxScaler learns and what it guarantees, on the wine training set: the range of each feature before
(11.03 to 14.75 and 0.89 to 5.65) and after scaling (0 to 1), with the test set's malic acid overshooting to
-0.03 and 1.03 because it is scaled with the training minimum and maximum."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "wine_data.csv", header=None, usecols=[0, 1, 2])
df.columns = ["Class", "Alcohol", "Malic acid"]
Xtr, Xte, _, _ = train_test_split(df.drop(columns="Class"), df["Class"], test_size=0.3, random_state=0)
sc = MinMaxScaler().fit(Xtr)
tr, te = sc.transform(Xtr), sc.transform(Xte)
assert list(sc.data_min_.round(2)) == [11.03, 0.89] and list(sc.data_max_.round(2)) == [14.75, 5.65]
assert round(te[:, 1].min(), 2) == -0.03 and round(te[:, 1].max(), 2) == 1.03
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#9a9a9a"
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=["Before: each feature has its own range", "After: training ranges are exactly 0 to 1"])
for j, (data_tr, data_te) in enumerate(((Xtr.values, Xte.values), (tr, te)), start=1):
    for k, (name, c) in enumerate((("Alcohol", BLUE), ("Malic acid", ORANGE))):
        y = 1 - k
        fig.add_scatter(x=data_tr[:, k], y=[y + 0.12] * len(data_tr), mode="markers", showlegend=False,
                        marker=dict(color=c, size=9, opacity=0.5, symbol="line-ns-open", line=dict(width=2)), row=1, col=j)
        fig.add_scatter(x=data_te[:, k], y=[y - 0.12] * len(data_te), mode="markers", showlegend=False,
                        marker=dict(color=GREY, size=9, opacity=0.7, symbol="line-ns-open", line=dict(width=2)), row=1, col=j)
        lo, hi = data_tr[:, k].min(), data_tr[:, k].max()
        fig.add_annotation(x=(lo + hi) / 2, y=y + 0.36, text=f"{name}: train {lo:.2f} to {hi:.2f}", showarrow=False,
                           font=dict(size=17, color=c), row=1, col=j)
        if j == 2 and k == 1:
            fig.add_annotation(x=0.5, y=y - 0.36, text=f"test: {data_te[:, k].min():.2f} to {data_te[:, k].max():.2f}",
                               showarrow=False, font=dict(size=17, color="#555"), row=1, col=j)
    fig.update_yaxes(visible=False, range=[-0.6, 1.6], row=1, col=j)
fig.update_xaxes(title_text="value", range=[0, 16], row=1, col=1)
fig.update_xaxes(title_text="scaled value", range=[-0.15, 1.15], row=1, col=2)
fig.add_vline(x=0, line=dict(dash="dash", color="black"), row=1, col=2)
fig.add_vline(x=1, line=dict(dash="dash", color="black"), row=1, col=2)
fig.update_annotations(selector=dict(xref="paper"), font_size=19)
fig.update_layout(template="simple_white", width=1400, height=460, font=dict(family="Latin Modern Roman", size=17),
                  margin=dict(l=30, r=30, t=60, b=70))
fig.write_image(here / "wine_ranges.png", scale=2)
fig.write_image(here / "wine_ranges.pdf")
