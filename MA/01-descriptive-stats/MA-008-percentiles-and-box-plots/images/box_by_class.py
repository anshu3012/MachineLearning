"""Side-by-side box plots: Titanic ages for each ticket class."""
from pathlib import Path
import pandas as pd
import plotly.express as px

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic_train.csv")
df["class"] = df.Pclass.map({1: "1st class", 2: "2nd class", 3: "3rd class"})
fig = px.box(df.dropna(subset=["Age"]), x="class", y="Age", color="class", points="outliers",
             category_orders={"class": ["1st class", "2nd class", "3rd class"]},
             color_discrete_sequence=["#4C78A8", "#F58518", "#54A24B"])
fig.update_layout(template="simple_white", width=900, height=480, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), xaxis_title="", yaxis_title="age (years)",
                  margin=dict(l=70, r=20, t=20, b=50))
fig.write_image(here / "box_by_class.png", scale=2)
fig.write_image(here / "box_by_class.pdf")
