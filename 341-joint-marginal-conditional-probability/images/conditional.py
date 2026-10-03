"""P(died | class) against P(class | died) on the Titanic data (Plotly): the two directions differ."""
from pathlib import Path
import pandas as pd
from plotly.subplots import make_subplots

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic_train.csv")
died_given_class = pd.crosstab(df["Pclass"], df["Survived"], normalize="index")[0]
class_given_died = pd.crosstab(df["Pclass"], df["Survived"], normalize="columns")[0]
p_died = (df["Survived"] == 0).mean()
print(died_given_class.round(3).tolist(), class_given_died.round(3).tolist(), round(p_died, 3))
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=["P(died | class): each bar is a row share", "P(class | died): bars sum to 1"])
x = ["class 1", "class 2", "class 3"]
fig.add_bar(x=x, y=died_given_class.values, marker_color="#E45756", text=died_given_class.round(3).values,
            textposition="outside", showlegend=False, row=1, col=1)
fig.add_shape(type="line", xref="x domain", yref="y", x0=0, x1=1, y0=p_died, y1=p_died,
              line=dict(color="#333333", dash="dash", width=2.5), layer="above")
fig.add_annotation(xref="x domain", yref="y", x=0.01, y=p_died + 0.05, text=f"P(died) = {p_died:.3f}",
                   xanchor="left", showarrow=False, font=dict(size=20, color="#6B6B6B"))
fig.add_bar(x=x, y=class_given_died.values, marker_color="#4C78A8", text=class_given_died.round(3).values,
            textposition="outside", showlegend=False, row=1, col=2)
fig.update_yaxes(range=[0, 1], title_text="probability", row=1, col=1)
fig.update_yaxes(range=[0, 1], row=1, col=2)
fig.update_layout(template="simple_white", width=1000, height=470, font=dict(family="Latin Modern Roman", size=22),
                  margin=dict(l=70, r=20, t=60, b=40))
for a in fig.layout.annotations[:2]:
    a.font.size = 22
fig.write_image(here / "conditional.png", scale=2)
fig.write_image(here / "conditional.pdf")
