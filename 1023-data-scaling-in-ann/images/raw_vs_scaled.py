"""The 320 training users before and after StandardScaler: the same picture, only the axis numbers change
(Plotly; split and scaler as in the Notebook)."""
from pathlib import Path
import pandas as pd
from plotly.subplots import make_subplots
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from common import BLUE, RED, FONT

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "Social_Network_Ads.csv")
X, y = df[["Age", "EstimatedSalary"]].to_numpy(), df["Purchased"].to_numpy()
X_tr, _, y_tr, _ = train_test_split(X, y, test_size=0.2, random_state=42)
Z = StandardScaler().fit_transform(X_tr)
assert len(X_tr) == 320
assert [round(v, 2) for v in (*Z.min(0), *Z.max(0))] == [-1.95, -1.61, 2.17, 2.32]        # the Extra box
fig = make_subplots(1, 2, horizontal_spacing=0.12, subplot_titles=["Raw: age in years, salary in rupees",
                                                                   "Standardized: both mean 0, std 1"])
for col, D in ((1, X_tr), (2, Z)):
    for v, name, c, s in ((0, "did not buy", BLUE, "circle"), (1, "bought", RED, "x")):
        m = y_tr == v
        fig.add_scatter(x=D[m, 0], y=D[m, 1], mode="markers", name=name, showlegend=col == 1,
                        marker=dict(color=c, symbol=s, size=7, opacity=0.8), row=1, col=col)
fig.update_xaxes(title="age")
fig.update_yaxes(title="salary", row=1, col=1)
fig.update_layout(template="simple_white", width=1150, height=480, font=FONT,
                  legend=dict(orientation="h", x=0.35, y=-0.2), margin=dict(l=80, r=20, t=50, b=60))
fig.update_annotations(font_size=18)
fig.write_image(here / "raw_vs_scaled.png", scale=2)
fig.write_image(here / "raw_vs_scaled.pdf")
