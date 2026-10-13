"""Drawing helpers for this Note's message animations (no output when run on its own): node boxes, arrows and
message dots, all placed in paper coordinates (0 to 1 across and up the figure)."""
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE

W, H, MARGIN = 1300, 900, 10
FILL = {BLUE: "rgba(76,120,168,0.25)", ORANGE: "rgba(245,133,24,0.25)", GREY: "rgba(107,107,107,0.18)",
        "#B279A2": "rgba(178,121,162,0.25)", "#54A24B": "rgba(84,162,75,0.25)", "#E45756": "rgba(228,87,86,0.25)"}


def blank(width=W, height=H):
    fig = go.Figure()
    fig.update_xaxes(visible=False, range=[0, 1])
    fig.update_yaxes(visible=False, range=[0, 1])
    fig.update_layout(template="simple_white", font=FONT, width=width, height=height, showlegend=False,
                      margin=dict(l=MARGIN, r=MARGIN, t=MARGIN, b=MARGIN))
    return fig


def box(fig, x, y, text, color=BLUE, lit=False, w=0.2, h=0.09, size=20, sub=None):
    fig.add_shape(type="rect", opacity=1, xref="paper", yref="paper", x0=x - w / 2, x1=x + w / 2, y0=y - h / 2,
                  y1=y + h / 2, line=dict(color=color, width=5 if lit else 2),
                  fillcolor=FILL.get(color, "white") if lit else "white", layer="below")
    txt = f"<b>{text}</b>" + (f"<br><span style='font-size:{size - 4}px'>{sub}</span>" if sub else "")
    fig.add_annotation(x=x, y=y, xref="paper", yref="paper", showarrow=False, xanchor="center", yanchor="middle",
                       text=txt, font=dict(size=size, color="black"))


def arrow(fig, p0, p1, color=GREY, width=3, dash=False, width_px=W, height_px=H):
    """An arrow from p0 to p1 in paper coordinates, head at p1."""
    pw, ph = width_px - 2 * MARGIN, height_px - 2 * MARGIN
    if dash:
        fig.add_shape(type="line", opacity=1, xref="paper", yref="paper", x0=p0[0], y0=p0[1], x1=p1[0], y1=p1[1],
                      line=dict(color=color, width=width, dash="dash"))
    fig.add_annotation(x=p1[0], y=p1[1], xref="paper", yref="paper", ax=(p0[0] - p1[0]) * pw,
                       ay=-(p0[1] - p1[1]) * ph, showarrow=True, arrowhead=2, arrowsize=1.2,
                       arrowwidth=0.1 if dash else width, arrowcolor=color, text="")


def dot(fig, p, color, label=None, size=22, label_side="right", font=17):
    fig.add_shape(type="circle", opacity=1, xref="paper", yref="paper", x0=p[0] - 0.012, x1=p[0] + 0.012,
                  y0=p[1] - 0.012 * W / H, y1=p[1] + 0.012 * W / H, line=dict(color=color, width=2), fillcolor=color)
    if label:
        fig.add_annotation(x=p[0] + (0.02 if label_side == "right" else -0.02), y=p[1], xref="paper", yref="paper",
                           showarrow=False, xanchor="left" if label_side == "right" else "right", text=label,
                           font=dict(size=font, color=color), bgcolor="rgba(255,255,255,0.85)")


def text(fig, x, y, s, size=19, color="black", anchor="left", valign="top"):
    fig.add_annotation(x=x, y=y, xref="paper", yref="paper", showarrow=False, xanchor=anchor, yanchor=valign,
                       align=anchor if anchor != "center" else "center", text=s, font=dict(size=size, color=color))


def lerp(p0, p1, f):
    return (p0[0] + (p1[0] - p0[0]) * f, p0[1] + (p1[1] - p0[1]) * f)
