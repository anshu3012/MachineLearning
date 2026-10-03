"""Pie charts of three categorical Titanic columns: the share of each group in percent."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic_train.csv")
BLUE, ORANGE, GREEN, RED = "#4C78A8", "#F58518", "#54A24B", "#E45756"
pies = [("Survived", {0: "died (0)", 1: "survived (1)"}, [RED, GREEN]),
        ("Pclass", {1: "class 1", 2: "class 2", 3: "class 3"}, [BLUE, ORANGE, GREEN]),
        ("Sex", {"male": "male", "female": "female"}, [BLUE, ORANGE])]
fig = make_subplots(1, 3, specs=[[{"type": "domain"}] * 3], subplot_titles=[p[0] for p in pies])
for i, (col, names, colours) in enumerate(pies, start=1):
    vc = df[col].value_counts().sort_index()
    fig.add_trace(go.Pie(labels=[names[k] for k in vc.index], values=vc.values, sort=False,
                         marker=dict(colors=colours, line=dict(color="white", width=2)),
                         textinfo="label+percent", texttemplate="%{label}<br>%{percent:.1%}",
                         textfont_size=20, insidetextorientation="horizontal"), 1, i)
fig.update_layout(template="simple_white", width=1050, height=420, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=21), margin=dict(l=20, r=20, t=60, b=20))
fig.update_annotations(font_size=23, yshift=10)
fig.write_image(here / "pies.png", scale=2)
fig.write_image(here / "pies.pdf")
