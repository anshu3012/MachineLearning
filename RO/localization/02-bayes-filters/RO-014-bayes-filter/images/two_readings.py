"""A door that nobody touches, read twice. Before any reading 0.5/0.5; after 'sense open' 0.75/0.25; after a second
'sense open' 0.9/0.1. Run: python two_readings.py -> two_readings.png"""
from pathlib import Path

from plotly.subplots import make_subplots

from doorplot import door_bars, update
from gifkit import BLUE, FONT

here = Path(__file__).parent
b0 = {"open": 0.5, "closed": 0.5}
b1 = update(b0, "open")
b2 = update(b1, "open")
assert abs(b1["open"] - 0.75) < 1e-12 and abs(b2["open"] - 0.9) < 1e-12
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.07,
                    subplot_titles=["before any reading", "after z<sub>1</sub> = sense open",
                                    "after z<sub>2</sub> = sense open"])
for c, b in enumerate((b0, b1, b2), start=1):
    door_bars(fig, b, BLUE, row=1, col=c, fmt="{:.2f}")
fig.update_yaxes(title="probability", row=1, col=1)
fig.update_layout(template="simple_white", width=1200, height=430, font=FONT, showlegend=False,
                  margin=dict(l=70, r=20, t=70, b=50))
fig.update_annotations(font_size=22)
fig.write_image(here / "two_readings.png", scale=1.5)
