"""Why we standardize: the 11 churn features of the 8,000 training customers on their raw scales and after
StandardScaler (the Notebook's split, random_state=1). Each box spans the middle half of a feature's values. Plotly."""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).parent
df = pd.read_csv(HERE.parent / "data" / "Churn_Modelling.csv").drop(columns=["RowNumber", "CustomerId", "Surname"])
df = pd.get_dummies(df, columns=["Geography", "Gender"], drop_first=True, dtype=int)
X = df.drop(columns="Exited")
X_train, _, _, _ = train_test_split(X, df["Exited"], test_size=0.2, random_state=1)
S = pd.DataFrame(StandardScaler().fit_transform(X_train), columns=X.columns)
assert X_train.shape == (8000, 11) and abs(S.mean().abs().max()) < 1e-9
order = X_train.max().sort_values().index.tolist()
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.2,
                    subplot_titles=("Raw values", "After standardizing: mean 0, standard deviation 1"))
for col, data in ((1, X_train), (2, S)):
    for c in order:
        fig.add_box(x=data[c], name=c, orientation="h", marker_color="#4C78A8", boxpoints=False, showlegend=False,
                    line=dict(width=1.5), row=1, col=col)
fig.update_xaxes(title_text="value", row=1, col=1, tickvals=[0, 50e3, 100e3, 150e3, 200e3, 250e3],
                 ticktext=["0", "50k", "100k", "150k", "200k", "250k"])
fig.update_xaxes(title_text="standardized value", range=[-4, 4], row=1, col=2)
fig.update_yaxes(showticklabels=False, row=1, col=2)
fig.update_layout(template="simple_white", width=1300, height=620, font=dict(family="Latin Modern Roman", size=19),
                  margin=dict(l=170, r=30, t=70, b=70))
for a in fig.layout.annotations:
    a.font.size = 21
fig.write_image(HERE / "scales.png", scale=2)
print(X_train.max().round(1).to_dict())
