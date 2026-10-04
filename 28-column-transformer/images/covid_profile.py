"""The COVID toy data at a glance: the categories of cough and city, and the missing values per column (fever has
10). Each panel shows the problem a transformer must fix."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "covid_toy.csv")
cough, city, miss = df.cough.value_counts(), df.city.value_counts(), df.isnull().sum()
assert cough.to_dict() == {"Mild": 62, "Strong": 38} and city.to_dict() == {"Kolkata": 32, "Bangalore": 30, "Delhi": 22, "Mumbai": 16}
assert miss["fever"] == 10 and miss.drop("fever").sum() == 0
fig = make_subplots(rows=1, cols=3, column_widths=[0.25, 0.35, 0.4], horizontal_spacing=0.08, subplot_titles=[
    "cough: ordinal (Mild < Strong)<br>→ ordinal encoding", "city: nominal, 4 categories<br>→ one-hot encoding",
    "missing values per column<br>fever → simple imputation"])
fig.add_bar(x=cough.index, y=cough.values, text=cough.values, textposition="outside", marker_color="#B279A2", row=1, col=1)
fig.add_bar(x=city.index, y=city.values, text=city.values, textposition="outside", marker_color="#54A24B", row=1, col=2)
fig.add_bar(x=miss.index, y=miss.values, text=miss.values, textposition="outside",
            marker_color=["#E45756" if v else "#cccccc" for v in miss.values], row=1, col=3)
fig.update_yaxes(title_text="patients", range=[0, 72], row=1, col=1)
fig.update_yaxes(range=[0, 38], row=1, col=2)
fig.update_yaxes(range=[0, 12], row=1, col=3)
fig.update_xaxes(tickangle=-30, row=1, col=3)
fig.update_annotations(font_size=19)
fig.update_layout(template="simple_white", width=1400, height=500, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=90, b=90))
fig.write_image(here / "covid_profile.png", scale=2)
fig.write_image(here / "covid_profile.pdf")
