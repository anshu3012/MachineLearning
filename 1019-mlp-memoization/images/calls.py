"""Function calls with and without memoization: Fibonacci, and dL/dO for every node of a network with hidden
layers of 10 nodes (counts from the Notebook) (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import RED, GREEN, FONT

here = Path(__file__).parent
fib = pd.read_csv(here.parent / "data" / "fib_calls.csv")
net = pd.read_csv(here.parent / "data" / "network_calls.csv")
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=("Fibonacci: fib(n)", "Backpropagation: hidden layers of 10 nodes"))
for col, d, xcol in ((1, fib, "n"), (2, net, "hidden_layers")):
    fig.add_trace(go.Scatter(x=d[xcol], y=d.plain, mode="lines+markers", name="plain recursion",
                             line=dict(color=RED, width=3), marker=dict(size=8), showlegend=col == 1), row=1, col=col)
    fig.add_trace(go.Scatter(x=d[xcol], y=d.memo, mode="lines+markers", name="with memoization",
                             line=dict(color=GREEN, width=3), marker=dict(size=8), showlegend=col == 1), row=1, col=col)
    fig.update_yaxes(title_text="function calls (log scale)", type="log", dtick=1, exponentformat="power", row=1, col=col)
fig.update_xaxes(title_text="n", row=1, col=1)
fig.update_xaxes(title_text="number of hidden layers", dtick=1, row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=470, font=FONT, legend=dict(x=0.02, y=0.98),
                  margin=dict(l=80, r=30, t=60, b=60))
fig.update_annotations(font=dict(family="Latin Modern Roman", size=17))
fig.write_image(here / "calls.png", scale=2)
fig.write_image(here / "calls.pdf")
