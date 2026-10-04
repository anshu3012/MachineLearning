"""Why we scale: CGPA and IQ live on very different ranges; after StandardScaler both centre on 0."""
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from toy_model import load

here = Path(__file__).parent
df, X_train, _, _, _, scaler, _ = load()
scaled = scaler.transform(X_train)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=("<b>Before scaling</b>: very different ranges", "<b>After scaling</b>: same range"))
for i, (name, colour) in enumerate([("CGPA", "#4C78A8"), ("IQ", "#F58518")]):
    fig.add_trace(go.Box(x=X_train.iloc[:, i], name=name, marker_color=colour, boxpoints="all", jitter=0.4,
                         pointpos=0, showlegend=False), 1, 1)
    fig.add_trace(go.Box(x=scaled[:, i], name=name, marker_color=colour, boxpoints="all", jitter=0.4,
                         pointpos=0, showlegend=False), 1, 2)
fig.update_xaxes(title_text="value", row=1, col=1)
fig.update_xaxes(title_text="value after scaling", zeroline=True, zerolinecolor="#6B6B6B", row=1, col=2)
fig.update_layout(template="simple_white", width=1200, height=420, font=dict(family="Latin Modern Roman", size=17),
                  margin=dict(l=60, r=20, t=70, b=60))
fig.update_annotations(font_size=19)
fig.write_image(here / "scaling.png", scale=2)
fig.write_image(here / "scaling.pdf")
