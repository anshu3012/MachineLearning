"""Titanic: crosstab of class vs survival, shown as a heatmap."""
import pandas as pd
import plotly.express as px
from common import load, save_px, FONT

t = load("titanic_train")
ct = pd.crosstab(t.Pclass, t.Survived)
fig = px.imshow(ct, text_auto=True, color_continuous_scale="Blues", aspect="auto",
                labels=dict(x="Survived (0 = died, 1 = survived)", y="Ticket class", color="Passengers"))
fig.update_traces(textfont_size=20)
fig.update_xaxes(tickvals=[0, 1], side="bottom")
fig.update_yaxes(tickvals=[1, 2, 3])
fig.update_layout(template="simple_white", width=800, height=520, font=FONT,
                  title=dict(text="Passengers per class and outcome", x=0.5), margin=dict(l=70, r=20, t=70, b=60))
save_px(fig, "heatmap_class")
