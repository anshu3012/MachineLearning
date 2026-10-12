"""Shared drawing helpers for this Note's figures of the room grid and the waypoint graph (no output when run on its
own). Colours keep one meaning in every figure: grey = blocked cell, light blue = visited, light orange = frontier,
red outline = the vertex being expanded, green = the route found."""
import plotly.graph_objects as go
from gifkit import FONT, GREEN, GREY, ORANGE, RED
from roommap import CAB, DOOR, H, TABLE, W
from roomsearch import BLOCKED, C, GOAL, NX, NY, START, WP

LBLUE, LORANGE, BGREY = "#c6dbef", "#fdd0a2", "#a8a8a8"
CODES = {"free": 0, "blocked": 1, "visited": 2, "frontier": 3}
_SCALE = [[0, "white"], [0.25, "white"], [0.25, BGREY], [0.5, BGREY], [0.5, LBLUE], [0.75, LBLUE],
          [0.75, LORANGE], [1, LORANGE]]


def grid_trace(visited=(), frontier=(), text=None, size=15):
    """One heatmap of all 112 cells: blocked grey, visited light blue, frontier light orange, free white.
    text: dict cell -> string written in that cell."""
    z = [[CODES["blocked"] if BLOCKED[j, i] else CODES["free"] for i in range(NX)] for j in range(NY)]
    for i, j in visited:
        z[j][i] = CODES["visited"]
    for i, j in frontier:
        z[j][i] = CODES["frontier"]
    txt = [["" for _ in range(NX)] for _ in range(NY)]
    for (i, j), s in (text or {}).items():
        txt[j][i] = s
    return go.Heatmap(z=z, x0=C / 2, dx=C, y0=C / 2, dy=C, zmin=-0.5, zmax=3.5, colorscale=_SCALE, showscale=False,
                      text=txt, texttemplate="%{text}", textfont=dict(size=size, color="black"),
                      hoverinfo="skip")


def grid_lines(color="#b8b8b8"):
    """The 0.5 m cell borders as thin lines (drawn over the heatmap)."""
    xs, ys = [], []
    for k in range(1, NX):
        xs += [k * C, k * C, None]
        ys += [0, NY * C, None]
    for k in range(1, NY):
        xs += [0, NX * C, None]
        ys += [k * C, k * C, None]
    return go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=color, width=1), hoverinfo="skip")


def room_lines(color="#333", width=4):
    """Walls with the door gap, and the table and cabinet outlines (thin)."""
    out = []
    for seg in [[(DOOR[1], H), (W, H), (W, 0), (0, 0), (0, H), (DOOR[0], H)]]:
        sx, sy = zip(*seg)
        out.append(go.Scatter(x=sx, y=sy, mode="lines", line=dict(color=color, width=width), hoverinfo="skip"))
    px, py = zip(*(TABLE + [TABLE[0]]))
    out.append(go.Scatter(x=px, y=py, mode="lines", line=dict(color="#555", width=1.5), hoverinfo="skip"))
    out.append(go.Scatter(x=[5.6, 7, 7, 6.4, 6.4, 5.6, 5.6], y=[4, 4, 2.4, 2.4, 3.4, 3.4, 4], mode="lines",
                          line=dict(color="#555", width=1.5), hoverinfo="skip"))
    return out


def cell_box(c, color=RED, width=4, dash=None):
    i, j = c
    x0, y0 = i * C, j * C
    return go.Scatter(x=[x0, x0 + C, x0 + C, x0, x0], y=[y0, y0, y0 + C, y0 + C, y0], mode="lines",
                      line=dict(color=color, width=width, dash=dash), hoverinfo="skip")


def route(path, color=GREEN, width=6, dash=None):
    xs = [(i + 0.5) * C for i, _ in path]
    ys = [(j + 0.5) * C for _, j in path]
    return go.Scatter(x=xs, y=ys, mode="lines+markers", line=dict(color=color, width=width, dash=dash),
                      marker=dict(size=7, color=color), hoverinfo="skip")


def start_goal(fig, row=None, col=None, size=17):
    """Labels S and G on the start and goal cells, and the word door above the gap."""
    kw = dict(row=row, col=col) if row else {}
    for c, s in ((START, "S"), (GOAL, "G")):
        fig.add_annotation(x=c[0] * C + 0.04, y=(c[1] + 1) * C - 0.03, text=f"<b>{s}</b>", showarrow=False,
                           xanchor="left", yanchor="top", font=dict(size=size, color=GREEN), **kw)
        fig.add_trace(cell_box(c, GREEN, 3), **kw)
    fig.add_annotation(x=sum(DOOR) / 2, y=H + 0.17, text="door", showarrow=False, font=dict(size=18, color=GREY), **kw)


def axes(fig, row=None, col=None, ytitle=True, top=4.35):
    kw = dict(row=row, col=col) if row else {}
    fig.update_xaxes(range=[-0.06, W + 0.06], dtick=1, title="x (m)", showgrid=False, **kw)
    fig.update_yaxes(range=[-0.06, top], dtick=1, title="y (m)" if ytitle else None, showgrid=False,
                     scaleanchor=f"x{'' if not col or col == 1 else col}", **kw)


def wp_traces(edge_color="#999", highlight=(), hl_color=ORANGE):
    """The waypoint graph: edges as grey lines with their length, vertices as circles with their letter.
    highlight: a list of vertices whose joining edges are drawn thick in hl_color (a path)."""
    from roomsearch import WP_EDGES
    out = []
    for a, b in WP_EDGES:
        (x0, y0), (x1, y1) = WP[a], WP[b]
        out.append(go.Scatter(x=[x0, x1], y=[y0, y1], mode="lines", line=dict(color=edge_color, width=2),
                              hoverinfo="skip"))
    for a, b in zip(highlight, highlight[1:]):
        (x0, y0), (x1, y1) = WP[a], WP[b]
        out.append(go.Scatter(x=[x0, x1], y=[y0, y1], mode="lines", line=dict(color=hl_color, width=7),
                              hoverinfo="skip"))
    return out


def wp_nodes(fill=None, edge=None, size=34, font=18):
    """Vertex circles: fill[v] = fill colour (default white), edge[v] = outline colour (default dark grey)."""
    fill, edge = fill or {}, edge or {}
    out = []
    for v, (x, y) in WP.items():
        out.append(go.Scatter(x=[x], y=[y], mode="markers+text", text=[f"<b>{v}</b>"], textposition="middle center",
                              marker=dict(size=size, color=fill.get(v, "white"),
                                          line=dict(color=edge.get(v, "#444"), width=4 if v in edge else 2)),
                              textfont=dict(size=font, color="black"), hoverinfo="skip"))
    return out


def layout(fig, width=1000, height=700, title=None, b=30, t=70, l=70, r=20, grid=False):
    fig.update_layout(template="simple_white", width=width, height=height, font=FONT, showlegend=False,
                      plot_bgcolor="white",
                      margin=dict(l=l, r=r, t=t, b=b),
                      title=dict(text=title, x=0.5, font=dict(size=22)) if title else None)
    return fig


def lines_below(fig, lines, y0=-0.12, dy=0.055, size=19):
    """Text lines under the plot area, as (text, colour) pairs, in paper coordinates."""
    for k, (s, col) in enumerate(lines):
        fig.add_annotation(x=0.0, y=y0 - dy * k, xref="paper", yref="paper", xanchor="left", yanchor="top",
                           showarrow=False, text=s, font=dict(size=size, color=col))


# where each edge's length label sits, as a fraction of the way from the first vertex to the second (clear of others)
_LABEL_AT = {("D", "G"): 0.45, ("C", "G"): 0.5, ("D", "S"): 0.4, ("A", "D"): 0.55}


def wp_labels(fig, row=None, col=None, size=15):
    """Each edge's length in m, on a white box at the middle of the edge."""
    from roomsearch import WP_EDGES, wp_dist
    kw = dict(row=row, col=col) if row else {}
    for a, b in WP_EDGES:
        f = _LABEL_AT.get((a, b), 0.5)
        (x0, y0), (x1, y1) = WP[a], WP[b]
        fig.add_annotation(x=x0 + f * (x1 - x0), y=y0 + f * (y1 - y0), text=f"{wp_dist(a, b):.3f}", showarrow=False,
                           bgcolor="white", font=dict(size=size, color=GREY), borderpad=1, **kw)


def furniture_fill(color="#e4e4e4"):
    """The table and the cabinet as light grey shapes (for figures of the waypoint graph)."""
    px, py = zip(*(TABLE + [TABLE[0]]))
    return [go.Scatter(x=px, y=py, mode="lines", fill="toself", fillcolor=color, line=dict(width=0), hoverinfo="skip"),
            go.Scatter(x=[5.6, 7, 7, 6.4, 6.4, 5.6, 5.6], y=[4, 4, 2.4, 2.4, 3.4, 3.4, 4], mode="lines", fill="toself",
                       fillcolor=color, line=dict(width=0), hoverinfo="skip")]


def route_cells(path, color=GREEN, width=4):
    """The route as thick outlines of its cells, so the numbers written in the cells stay readable."""
    return [cell_box(c, color, width) for c in path]
