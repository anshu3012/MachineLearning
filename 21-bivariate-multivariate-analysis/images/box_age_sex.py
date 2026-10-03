"""Titanic: age by sex (box plot), split by survival (hue)."""
import plotly.express as px
from common import load, save_px, FONT, RED, GREEN

t = load("titanic_train").dropna(subset=["Age"])
t["Outcome"] = t.Survived.map({0: "died", 1: "survived"})
fig = px.box(t, x="Sex", y="Age", color="Outcome", color_discrete_map={"died": RED, "survived": GREEN},
             category_orders={"Sex": ["male", "female"], "Outcome": ["died", "survived"]})
fig.update_layout(template="simple_white", width=900, height=540, font=FONT, legend_title_text="",
                  title=dict(text="Age by sex and survival", x=0.5), yaxis_title="Age (years)",
                  margin=dict(l=70, r=20, t=70, b=60))
save_px(fig, "box_age_sex")
