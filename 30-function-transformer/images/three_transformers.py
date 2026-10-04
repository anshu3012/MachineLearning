"""The three scikit-learn classes on the same feature, the 891 Titanic fares: FunctionTransformer(np.log1p),
PowerTransformer (Yeo-Johnson, the default) and QuantileTransformer(output_distribution="normal"), with the
skewness of each result."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import FunctionTransformer, PowerTransformer, QuantileTransformer

here = Path(__file__).parent
fare = pd.read_csv(here.parent / "data" / "titanic_train.csv")[["Fare"]]
out = {"raw fare": fare.values.ravel(),
       "FunctionTransformer(np.log1p)": FunctionTransformer(np.log1p).fit_transform(fare).values.ravel(),
       "PowerTransformer()": PowerTransformer().fit_transform(fare).ravel(),
       "QuantileTransformer(normal)": QuantileTransformer(output_distribution="normal", n_quantiles=891,
                                                          random_state=0).fit_transform(fare).ravel()}
sk = {k: pd.Series(v).skew() for k, v in out.items()}
assert round(sk["raw fare"], 2) == 4.79 and all(abs(v) < 1 for k, v in sk.items() if k != "raw fare")
fig = make_subplots(rows=1, cols=4, horizontal_spacing=0.05, subplot_titles=[f"{k}<br>skewness {v:.2f}" for k, v in sk.items()])
for j, v in enumerate(out.values(), start=1):
    fig.add_histogram(x=v, nbinsx=40, marker_color="#4C78A8" if j == 1 else "#54A24B", row=1, col=j)
fig.update_annotations(font_size=17)
fig.update_layout(template="simple_white", width=1600, height=440, showlegend=False, bargap=0.03,
                  font=dict(family="Latin Modern Roman", size=15), margin=dict(l=40, r=20, t=80, b=40))
fig.write_image(here / "three_transformers.png", scale=2)
fig.write_image(here / "three_transformers.pdf")
