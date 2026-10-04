"""Sections 3 and 6: the self-attention output vector of "rahul" and of "lion" in "rahul killed the lion" (order 1)
and "the lion killed rahul" (order 2). Top row: no positions, the two bars of every pair are equal. Bottom row:
positional encodings added to the embeddings, the bars differ. Data: data/order_outputs.csv (Notebook, section 1).
Plotly (a bar chart). Idea of swapping the words after StatQuest, "Transformer Neural Networks, ChatGPT's
foundation, Clearly Explained!!!" (11:30); sentences, layer and numbers are the Note's own."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
d = pd.read_csv(here.parent / "data" / "order_outputs.csv")
WORDS = {"rahul": "\"rahul\": word 1, then word 4", "lion": "\"lion\": word 4, then word 2"}
ROWS = {"plain": "no positions", "pe": "positions added"}
fig = make_subplots(rows=2, cols=2, shared_yaxes=True, vertical_spacing=0.2, horizontal_spacing=0.06,
                    subplot_titles=[f"{t}<br><span style='font-size:17px'>{r}: largest gap "
                                    f"{(d[d.word == w][k + '_order1'] - d[d.word == w][k + '_order2']).abs().max():.2f}</span>"
                                    for k, r in ROWS.items() for w, t in WORDS.items()])
for i, k in enumerate(ROWS):
    for j, w in enumerate(WORDS):
        part = d[d.word == w]
        for col, name, colour in ((f"{k}_order1", "rahul killed the lion", BLUE), (f"{k}_order2", "the lion killed rahul", ORANGE)):
            fig.add_bar(x=part.dim + 1, y=part[col], name=name, marker_color=colour, legendgroup=name,
                        showlegend=(i == 0 and j == 0), row=i + 1, col=j + 1)
        fig.update_xaxes(title_text="number of the output vector" if i == 1 else None, dtick=1, row=i + 1, col=j + 1)
fig.update_yaxes(title_text="value", col=1)
fig.update_layout(template="simple_white", width=1100, height=760, font=dict(FONT, size=18), barmode="group",
                  legend=dict(orientation="h", y=1.14, x=0.5, xanchor="center"), margin=dict(l=70, r=20, t=110, b=60))
fig.update_annotations(font_size=19)
fig.write_image(here / "order_with_pe.png", scale=2)
fig.write_image(here / "order_with_pe.pdf")
