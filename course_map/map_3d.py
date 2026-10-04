"""3D Concept map: every Concept and every link from concepts.yaml, as a network you can rotate and zoom.

Usage: python course_map/map_3d.py      writes course_map/concept_map_3d.html (opens offline in any browser)
Each area is a cluster; hover a Concept for its Notes, click it to light up its links (click it again to reset)."""
import json
import math
import random
from pathlib import Path

import networkx as nx
import plotly.graph_objects as go

from build_map import AREAS, CONCEPTS, LINK_COLOUR, LINKS, note_title

OUT = Path(__file__).resolve().parent / "concept_map_3d.html"
PALETTE = ["#4C78A8", "#F58518", "#54A24B", "#E45756", "#72B7B2", "#B279A2", "#FF9DA6", "#9D755D", "#BAB0AC",
           "#EECA3B", "#2F6B9A", "#C2410C", "#3F7F3A", "#A3333D", "#3E8F8A", "#7A4E78", "#8C6D31", "#5A5A5A"]

area_of = {cid: next(a for a, _, member in AREAS if member(c)) for cid, c in CONCEPTS.items()}
areas = [(a, t) for a, t, _ in AREAS if a in area_of.values()]
colour = {a: PALETTE[k % len(PALETTE)] for k, (a, _) in enumerate(areas)}

# Layout: area centres spread evenly on a sphere; an invisible hub per area holds its Concepts together,
# then a 3D spring layout settles everything so linked Concepts sit close.
g = nx.Graph()
start = {}
for k, (a, _) in enumerate(areas):                     # Fibonacci sphere: even spacing for any number of areas
    y = 1 - 2 * (k + 0.5) / len(areas)
    r, phi = math.sqrt(1 - y * y), k * math.pi * (3 - math.sqrt(5))
    start["hub:" + a] = (3 * r * math.cos(phi), 3 * y, 3 * r * math.sin(phi))
for cid in CONCEPTS:
    g.add_edge(cid, "hub:" + area_of[cid], weight=2.0)
for i, (a, _) in enumerate(areas):                       # weak ties between hubs keep small areas from drifting off
    for b, _ in areas[i + 1:]:
        g.add_edge("hub:" + a, "hub:" + b, weight=0.04)
for l in LINKS:
    g.add_edge(l["a"], l["b"], weight=0.6 if area_of[l["a"]] == area_of[l["b"]] else 0.15)
rng = random.Random(7)                                  # Concepts start scattered around their area's hub
init = {n: start[n] if n in start else tuple(c + rng.uniform(-0.5, 0.5) for c in start["hub:" + area_of[n]])
        for n in g.nodes}
pos = nx.spring_layout(g, dim=3, seed=7, weight="weight", k=1.3, iterations=600, pos=init)

nodes = list(CONCEPTS)
centre = {a: [sum(pos[n][d] for n in nodes if area_of[n] == a) / sum(area_of[n] == a for n in nodes) for d in range(3)]
          for a, _ in areas}                             # area name sits at the middle of its Concepts
index = {cid: i for i, cid in enumerate(nodes)}
neighbours = {cid: set() for cid in nodes}
for l in LINKS:
    neighbours[l["a"]].add(l["b"])
    neighbours[l["b"]].add(l["a"])


def notes_text(c):
    return "<br>".join(note_title(v) for v in c["videos"][:4]) + ("<br>…" if len(c["videos"]) > 4 else "")


fig = go.Figure()
for t in LINK_COLOUR:                                   # one trace per relation, so the legend can toggle it
    xs, ys, zs = [], [], []
    for l in LINKS:
        if l["type"] == t:
            for n in (l["a"], l["b"]):
                xs.append(pos[n][0]); ys.append(pos[n][1]); zs.append(pos[n][2])
            xs.append(None); ys.append(None); zs.append(None)
    fig.add_trace(go.Scatter3d(x=xs, y=ys, z=zs, mode="lines", name=t, hoverinfo="skip",
                               line=dict(color=LINK_COLOUR[t], width=2), opacity=0.45))
degree = {cid: len(neighbours[cid]) for cid in nodes}
fig.add_trace(go.Scatter3d(
    x=[pos[n][0] for n in nodes], y=[pos[n][1] for n in nodes], z=[pos[n][2] for n in nodes],
    mode="markers", name="Concepts", showlegend=False,
    marker=dict(size=[4 + 1.2 * min(degree[n], 12) for n in nodes], color=[colour[area_of[n]] for n in nodes],
                line=dict(color="#333333", width=0.5), opacity=1.0),
    text=[CONCEPTS[n]["name"] for n in nodes],
    customdata=[[dict(areas)[area_of[n]], notes_text(CONCEPTS[n])] for n in nodes],
    hovertemplate="<b>%{text}</b><br>%{customdata[0]}<br><br>%{customdata[1]}<extra></extra>"))
fig.add_trace(go.Scatter3d(                             # area names, floating above each cluster
    x=[centre[a][0] for a, _ in areas], y=[centre[a][1] for a, _ in areas],
    z=[centre[a][2] for a, _ in areas], mode="text", name="Area names",
    text=[f"<b>{t}</b>" for _, t in areas], textfont=dict(size=12, color=[colour[a] for a, _ in areas]),
    hoverinfo="skip"))
fig.add_trace(go.Scatter3d(                             # every Concept name; off until switched on
    x=[pos[n][0] for n in nodes], y=[pos[n][1] for n in nodes], z=[pos[n][2] for n in nodes],
    mode="text", text=[CONCEPTS[n]["name"] for n in nodes], name="Concept names", visible="legendonly",
    textfont=dict(size=10, color="#222222"), hoverinfo="skip"))
fig.add_trace(go.Scatter3d(x=[], y=[], z=[], mode="lines", name="selected links", showlegend=False,
                           hoverinfo="skip", line=dict(color="#111111", width=6)))
fig.add_trace(go.Scatter3d(x=[], y=[], z=[], mode="markers+text", name="selected", showlegend=False,
                           hoverinfo="skip", textposition="top center", textfont=dict(size=13, color="#111111"),
                           marker=dict(size=9, color="#111111")))
axis = dict(visible=False, showbackground=False)
fig.update_layout(title=dict(text="Course map in 3D: drag to rotate, scroll to zoom, click a Concept to see its links",
                             x=0.5, font=dict(size=16)),
                  template="simple_white", height=900, margin=dict(l=0, r=0, t=50, b=0),
                  scene=dict(xaxis=axis, yaxis=axis, zaxis=axis, aspectmode="data",
                             camera=dict(eye=dict(x=0.9, y=0.9, z=0.6))),
                  legend=dict(title_text="Links (click to hide)", x=0.01, y=0.98),
                  font=dict(family="Latin Modern Roman, serif"))

# Click a Concept: draw its links in black and name it and its neighbours; click it again to clear.
graph = {"pos": {n: pos[n].tolist() for n in nodes}, "names": {n: CONCEPTS[n]["name"] for n in nodes},
         "nodes": nodes, "nb": {n: sorted(neighbours[n]) for n in nodes}}
concept_trace, sel_links, sel_nodes = len(LINK_COLOUR), len(fig.data) - 2, len(fig.data) - 1
post_script = f"""
const G = {json.dumps(graph)};
const gd = document.getElementById('{{plot_id}}');
let current = null;
gd.on('plotly_click', ev => {{
  const p = ev.points.find(q => q.curveNumber === {concept_trace});
  if (!p) return;
  const id = G.nodes[p.pointNumber];
  const clear = id === current;
  current = clear ? null : id;
  const lx = [], ly = [], lz = [], nx = [], ny = [], nz = [], nt = [];
  if (!clear) {{
    const a = G.pos[id];
    for (const b of G.nb[id]) {{
      const q = G.pos[b];
      lx.push(a[0], q[0], null); ly.push(a[1], q[1], null); lz.push(a[2], q[2], null);
      nx.push(q[0]); ny.push(q[1]); nz.push(q[2]); nt.push(G.names[b]);
    }}
    nx.push(a[0]); ny.push(a[1]); nz.push(a[2]); nt.push('<b>' + G.names[id] + '</b>');
  }}
  Plotly.restyle(gd, {{x: [lx, nx], y: [ly, ny], z: [lz, nz], text: [[], nt]}}, [{sel_links}, {sel_nodes}]);
  Plotly.restyle(gd, {{opacity: clear ? 0.45 : 0.12}}, [...Array({len(LINK_COLOUR)}).keys()]);
}});
"""
fig.write_html(OUT, include_plotlyjs=True, post_script=post_script, config={"displaylogo": False})
print(f"Wrote {OUT} ({len(nodes)} Concepts, {len(LINKS)} links, {len(areas)} areas)")
