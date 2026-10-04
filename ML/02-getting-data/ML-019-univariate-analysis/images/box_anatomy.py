"""Box plot of Titanic ages with every part labelled: whiskers, quartiles, median, outliers."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
age = pd.read_csv(here.parent / "data" / "titanic_train.csv")["Age"].dropna()
q1, med, q3 = age.quantile([0.25, 0.5, 0.75])
iqr = q3 - q1
lo, hi = age[age >= q1 - 1.5 * iqr].min(), age[age <= q3 + 1.5 * iqr].max()
# pass pandas' own quartiles and Tukey fences (1.5 x IQR), so the plot matches describe() exactly
q1, med, q3 = age.quantile([0.25, 0.5, 0.75])
iqr = q3 - q1
inside = age[(age >= q1 - 1.5 * iqr) & (age <= q3 + 1.5 * iqr)]
out = age[(age < q1 - 1.5 * iqr) | (age > q3 + 1.5 * iqr)]
fig = go.Figure(go.Box(y=[0], q1=[q1], median=[med], q3=[q3], lowerfence=[inside.min()], upperfence=[inside.max()],
                       orientation="h", line=dict(color="#4C78A8", width=3), fillcolor="rgba(76,120,168,0.18)"))
fig.add_trace(go.Scatter(x=out, y=[0] * len(out), mode="markers",
                         marker=dict(color="#E45756", size=9, opacity=1)))
# labels: above the box for the box parts, below for whiskers and outliers
for x, text, ay, *axs in [(q1, f"Q1 = {q1:.1f}", -95), (med, f"median = {med:.0f}", -150), (q3, f"Q3 = {q3:.0f}", -95),
                    (lo, f"lower whisker = {lo:.2f}", 85, 70), (hi, f"upper whisker = {hi:.0f}", 85, 0),
                    (74, "outliers: above 64.8", -95)]:
    fig.add_annotation(x=x, y=0, text=text, ax=(axs or [0])[0], ay=ay, arrowhead=2, arrowwidth=1.6, arrowcolor="#6B6B6B",
                       font=dict(size=17))
fig.add_shape(type="line", x0=q1, x1=q3, y0=-0.42, y1=-0.42, line=dict(color="#F58518", width=3))
fig.add_annotation(x=(q1 + q3) / 2, y=-0.42, text=f"IQR = Q3 - Q1 = {iqr:.2f}", showarrow=False, yshift=-16,
                   font=dict(size=17, color="#F58518"))
fig.update_xaxes(title="Age (years)", range=[-3, 84])
fig.update_yaxes(visible=False, range=[-0.6, 0.85])
fig.update_layout(template="simple_white", width=1000, height=440, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=30, r=30, t=20, b=60))
fig.write_image(here / "box_anatomy.png", scale=2)
fig.write_image(here / "box_anatomy.pdf")
