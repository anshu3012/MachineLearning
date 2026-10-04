"""The four RNN types on one time axis, with the Note's own examples. Each frame is one time step: a blue word
enters a cell from below, a green output leaves above, the red arrow carries the hidden state to the next step.
Many-to-one: outputs only at the last step. One-to-many: input only at the first step. Same length: an output at
every input. Different lengths: the encoder reads all 4 words before the decoder writes 5.
Our own design. Tool: Plotly frames (a fixed diagram filling in step by step). -> GIF + key-frame grid."""
from pathlib import Path

import plotly.graph_objects as go
from gifkit import save_gif

HERE = Path(__file__).parent
BLUE, RED, GREEN, PURPLE, GREY = "#4C78A8", "#E45756", "#54A24B", "#B279A2", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=20)
# (name, inputs per step, outputs per step); None = nothing at that step
TYPES = [
    ("many-to-one", ["movie", "was", "not", "good"], [None, None, None, "negative"]),
    ("one-to-many", ["image", None, None, None], ["a", "man", "plays", "cricket"]),
    ("many-to-many,<br>same length", ["my", "name", "is", "Riya"], ["pronoun", "noun", "verb", "proper<br>noun"]),
    ("many-to-many,<br>different lengths", ["I", "am", "going", "home"] + [None] * 5,
     [None] * 4 + ["main", "ghar", "ja", "raha", "hoon"]),
]
T = 9
ROW_H = 3.0


def frame(t):
    fig = go.Figure()
    for r, (name, ins, outs) in enumerate(TYPES):
        y = (len(TYPES) - 1 - r) * ROW_H + 1.3
        fig.add_annotation(x=0.35, y=y, text=f"<b>{name}</b>", showarrow=False, xanchor="right", font=dict(size=22))
        for k in range(min(t, len(ins))):
            x = k + 1
            now = k == t - 1
            fig.add_shape(type="rect", x0=x - 0.3, x1=x + 0.3, y0=y - 0.35, y1=y + 0.35, opacity=1,
                          line=dict(color=PURPLE, width=4 if now else 2), fillcolor="#E3CFE0" if now else "#F1E8EF")
            if k > 0:
                fig.add_annotation(x=x - 0.32, y=y, ax=x - 0.68, ay=y, xref="x", yref="y", axref="x", ayref="y",
                                   arrowhead=2, arrowwidth=2.5, arrowcolor=RED, text="")
            if ins[k]:
                fig.add_annotation(x=x, y=y - 0.37, ax=x, ay=y - 0.8, xref="x", yref="y", axref="x", ayref="y",
                                   arrowhead=2, arrowwidth=2.5, arrowcolor=BLUE, text="")
                fig.add_annotation(x=x, y=y - 1.05, text=ins[k], showarrow=False, font=dict(size=23, color=BLUE))
            if outs[k]:
                fig.add_annotation(x=x, y=y + 0.8, ax=x, ay=y + 0.37, xref="x", yref="y", axref="x", ayref="y",
                                   arrowhead=2, arrowwidth=2.5, arrowcolor=GREEN, text="")
                fig.add_annotation(x=x, y=y + 1.05, text=outs[k], showarrow=False, font=dict(size=23, color=GREEN), yanchor="bottom", yshift=-14)
        if r == 3 and t >= 5:
            fig.add_annotation(x=2.5, y=y + 0.75, text="encoder: reads", showarrow=False, font=dict(size=21, color=GREY))
            fig.add_annotation(x=7, y=y - 0.75, text="decoder: writes", showarrow=False, font=dict(size=21, color=GREY))
    fig.update_layout(template="simple_white", width=1100, height=820, font=FONT, showlegend=False,
                      title=dict(text=f"time step <b>{t}</b>: <span style='color:{BLUE}'>input in</span>, "
                                      f"<span style='color:{GREEN}'>output out</span>, "
                                      f"<span style='color:{RED}'>hidden state on</span>", x=0.5, y=0.97),
                      xaxis=dict(visible=False, range=[-2.2, T + 0.6]), yaxis=dict(visible=False, range=[-0.1, 4 * ROW_H]),
                      margin=dict(l=10, r=10, t=60, b=10))
    return fig


if __name__ == "__main__":
    save_gif([frame(t) for t in range(1, T + 1)], "types_timeline", HERE, keys=[0, 3, 4, 8], fps=1.0, cols=2,
             holds=[1, 1, 1, 3, 1, 1, 1, 1, 5], width=820)
