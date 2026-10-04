"""Section 5: a list of 3 numbers is a point (an arrow from the origin) in 3D space. Each number is a walk along one axis:
CGPA first, then IQ, then state. Two example students, the Note's [8.1, 91, 0] and a second one with state 1.
Plotly frames (real axes with tick values in 3D) -> GIF, plus a key-frame grid for the PDF."""
from pathlib import Path
import plotly.graph_objects as go
from gifkit import save_gif

HERE = Path(__file__).parent
RED, BLUE, GREY = "#E45756", "#4C78A8", "#9A9A9A"
GRID = dict(showgrid=True, gridcolor="#DDDDDD", showbackground=True, backgroundcolor="#FAFAFA")
A, B = (8.1, 91, 0), (6.2, 120, 1)


def walk(fig, p, colour, steps):
    """Draw the first `steps` legs of the walk origin -> p (one leg per axis); with all 3 legs, add the arrow and the point."""
    corners = [(0, 0, 0), (p[0], 0, 0), (p[0], p[1], 0), p][:steps + 1]
    x, y, z = zip(*corners)
    fig.add_scatter3d(x=x, y=y, z=z, mode="lines+markers", line=dict(color=GREY, width=7, dash="dash"),
                      marker=dict(size=3, color=GREY), showlegend=False)
    if steps == 3:
        fig.add_scatter3d(x=[0, p[0]], y=[0, p[1]], z=[0, p[2]], mode="lines", line=dict(color=colour, width=9), showlegend=False)
        fig.add_scatter3d(x=[p[0]], y=[p[1]], z=[p[2]], mode="markers+text", marker=dict(size=8, color=colour, symbol="diamond"),
                          text=[f"[{p[0]}, {p[1]}, {p[2]}]  "], textposition="middle left" if p[2] else "top left", textfont=dict(size=20, color=colour),
                          showlegend=False)


def frame(title, a_steps, b_steps=None):
    fig = go.Figure()
    walk(fig, A, RED, a_steps)
    if b_steps is not None:
        walk(fig, B, BLUE, b_steps)
    fig.update_layout(template="simple_white", width=900, height=680, font=dict(family="Latin Modern Roman", size=17),
                      title=dict(text=title, x=0.5, font=dict(size=23)),
                      scene=dict(xaxis=dict(title="CGPA", range=[0, 10], **GRID), yaxis=dict(title="IQ", range=[0, 140], **GRID),
                                 zaxis=dict(title="State (0 or 1)", range=[0, 1.3], tickvals=[0, 1], **GRID),
                                 camera=dict(eye=dict(x=1.35, y=-1.75, z=0.8), center=dict(x=0, y=0, z=-0.08)), aspectmode="cube"),
                      margin=dict(l=0, r=0, t=70, b=0))
    return fig


if __name__ == "__main__":
    figs = [frame("The list [8.1, 91, 0]: start at the origin", 0),
            frame("First number: walk 8.1 along the CGPA axis", 1),
            frame("Second number: walk 91 along the IQ axis", 2),
            frame("Third number: walk 0 along the State axis.<br>The list is now a point, with an arrow from the origin", 3),
            frame("A second list [6.2, 120, 1]: walk 6.2, then 120 ...", 3, 2),
            frame("... then 1 up the State axis.<br>One list of 3 numbers = one point in 3D space", 3, 3)]
    save_gif(figs, "list_to_point", HERE, keys=[1, 2, 3, 5], fps=0.8)
