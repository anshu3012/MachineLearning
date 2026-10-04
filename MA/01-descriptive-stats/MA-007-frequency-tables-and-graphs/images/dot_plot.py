"""A dot plot: the frequency table of a discrete feature, one dot per observation. Data: the party size of the 76
Sunday parties in the tips data. Plotly. Idea after Khan Academy, "Frequency tables and dot plots"."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
tips = pd.read_csv(here.parent / "data" / "tips.csv")
freq = tips.loc[tips.day == "Sun", "size"].value_counts().reindex(range(1, 7), fill_value=0)
assert freq.tolist() == [0, 39, 15, 18, 3, 1]
x = np.repeat(freq.index, freq.values)
y = np.concatenate([np.arange(1, f + 1) for f in freq.values])
fig = go.Figure(go.Scatter(x=x, y=y, mode="markers", marker=dict(size=11, color="#4C78A8")))
for size, f in freq.items():
    fig.add_annotation(x=size, y=f + 2.2, text=f"<b>{f}</b>", showarrow=False, font=dict(size=20))
fig.update_layout(template="simple_white", width=900, height=620, font=dict(family="Latin Modern Roman", size=20),
                  xaxis=dict(title="party size (people)", dtick=1, range=[0.4, 6.6]),
                  yaxis=dict(title="number of parties (frequency)", range=[0, 44]),
                  margin=dict(l=80, r=20, t=20, b=70))
fig.write_image(here / "dot_plot.png", scale=2)
fig.write_image(here / "dot_plot.pdf")
print(freq.to_dict())
