"""Group ablations on GPT-2 small, "<athlete> plays the sport of", for the 18 athletes whose sport it ranks first:
zero the outputs of a group of MLPs at the name tokens or at the other tokens, and count the athletes whose true
sport is still ranked first among 10 sports. Data: data/ablation_summary.csv (Notebook).
Run: python ablation_groups.py -> ablation_groups.png"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

from common import BLUE, GREY, ORANGE, FONT, DATA

HERE = Path(__file__).parent
d = pd.read_csv(DATA / "ablation_summary.csv")
col = [GREY if "nothing" in c else (ORANGE if "name" in c else BLUE) for c in d.condition]
fig = go.Figure(go.Bar(x=d.condition.str.replace(", ", "<br>"), y=d.still_first, marker_color=col,
                       text=[f"{v} of {n}" for v, n in zip(d.still_first, d.athletes)], textposition="outside"))
fig.update_layout(template="simple_white", width=900, height=500, font=FONT, showlegend=False,
                  yaxis=dict(title="athletes whose true sport<br>is still ranked first", range=[0, 20.5]),
                  xaxis=dict(tickfont=dict(size=17)), margin=dict(l=90, r=20, t=20, b=90))
fig.write_image(HERE / "ablation_groups.png", scale=2)
