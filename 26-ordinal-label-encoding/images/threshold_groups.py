"""Why numbering nominal categories misleads a model: three states coded 0, 1, 2 sit on a number line, and a model that
cuts the line at one threshold (a decision tree) can only form two of the three possible groupings.
No dataset: the three states are the Note's own nominal example. Idea after StatQuest, "One-Hot, Label, Target and
K-Fold Target Encoding" (04:00-04:30: a tree is forced to group by the arbitrary numbers). Plotly frames -> GIF."""
from pathlib import Path
import plotly.graph_objects as go
from anim import save_gif, FONT, BLUE, ORANGE, GREEN, RED, GREY

here = Path(__file__).parent
STATES = ["Karnataka", "Maharashtra", "West Bengal"]  # alphabetical, as OrdinalEncoder would number them
COL = [BLUE, ORANGE, GREEN]


def frame(head, cut=None, left=None, right=None, impossible=False):
    fig = go.Figure()
    fig.add_scatter(x=[0, 1, 2], y=[0] * 3, mode="markers+text", marker=dict(size=46, color=COL),
                    text=[f"<b>{s}</b><br>code {i}" for i, s in enumerate(STATES)], textposition="top center",
                    textfont=dict(size=22))
    if cut is not None:
        fig.add_shape(type="line", x0=cut, x1=cut, y0=-0.75, y1=1.05, line=dict(color=RED, width=5, dash="dash"), opacity=1)
        fig.add_annotation(x=cut, y=1.0, text=f"is the code below {cut}?", showarrow=False, xanchor="left", xshift=10,
                           font=dict(size=22, color=RED))
        fig.add_annotation(x=(cut - 0.5) / 2, y=-1.0, text="<b>yes:</b> " + left, showarrow=False, font=dict(size=21))
        fig.add_annotation(x=(cut + 2.5) / 2, y=-1.0, text="<b>no:</b> " + right, showarrow=False, font=dict(size=21))
    if impossible:
        fig.add_shape(type="path", path="M 0,-0.3 Q 1,-1.3 2,-0.3", line=dict(color=RED, width=4, dash="dot"),
                      fillcolor="rgba(0,0,0,0)", opacity=1)
        fig.add_annotation(x=1, y=-1.05, showarrow=False, font=dict(size=21, color=RED),
                           text="Karnataka with West Bengal, Maharashtra alone:<br>no single cut can do it, because 1 lies between 0 and 2")
    fig.update_layout(template="simple_white", width=1100, height=520, font=FONT, showlegend=False,
                      title=dict(text=f"<b>{head}</b>", x=0.5), margin=dict(l=30, r=30, t=80, b=40),
                      xaxis=dict(range=[-0.5, 2.5], tickvals=[0, 1, 2], title="code given to the state"),
                      yaxis=dict(visible=False, range=[-1.4, 1.1]))
    return fig


if __name__ == "__main__":
    figs = [frame("Three states with no order, numbered 0, 1, 2"),
            frame("Cut 1 groups Maharashtra with West Bengal", 0.5, "Karnataka", "Maharashtra, West Bengal"),
            frame("Cut 2 groups Karnataka with Maharashtra", 1.5, "Karnataka, Maharashtra", "West Bengal"),
            frame("The third grouping is impossible", impossible=True)]
    save_gif(figs, "threshold_groups", here, keys=[1, 2, 3], fps=1, holds=[3, 3, 3, 6], cols=1, width=860)
