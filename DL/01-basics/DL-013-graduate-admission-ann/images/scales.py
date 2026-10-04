"""Min-max scaling on the admission data: the 7 features of the 400 training students on their raw scales and after
MinMaxScaler (the Notebook's split, random_state=1). Each box spans the middle half of a feature's values. Plotly."""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

HERE = Path(__file__).parent
df = pd.read_csv(HERE.parent / "data" / "Admission_Predict_Ver1.1.csv")
df.columns = df.columns.str.strip()
df = df.drop(columns="Serial No.")
X, y = df.iloc[:, 0:-1], df.iloc[:, -1]
X_train, _, _, _ = train_test_split(X, y, test_size=0.2, random_state=1)
S = pd.DataFrame(MinMaxScaler().fit_transform(X_train), columns=X.columns)
assert X_train.shape == (400, 7) and S.min().min() == 0 and S.max().max() == 1
order = X_train.max().sort_values().index.tolist()
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.18,
                    subplot_titles=("Raw values", "After min-max scaling: every feature from 0 to 1"))
for col, data in ((1, X_train), (2, S)):
    for c in order:
        fig.add_box(x=data[c], name=c, orientation="h", marker_color="#4C78A8", boxpoints=False, showlegend=False,
                    line=dict(width=1.5), row=1, col=col)
fig.update_xaxes(title_text="value", row=1, col=1)
fig.update_xaxes(title_text="scaled value", range=[-0.05, 1.05], row=1, col=2)
fig.update_yaxes(showticklabels=False, row=1, col=2)
fig.update_layout(template="simple_white", width=1300, height=520, font=dict(family="Latin Modern Roman", size=19),
                  margin=dict(l=170, r=30, t=70, b=70))
for a in fig.layout.annotations:
    a.font.size = 21
fig.write_image(HERE / "scales.png", scale=2)
print(X_train.agg(["min", "max"]).to_dict())
