"""Interactive Course map (Dash + Dash Cytoscape). Reads the same concepts.yaml as the PDF, via build_map.py.

Run:  python course_map/app.py   then open http://127.0.0.1:8050
- Concepts sit in boxes, one per area of the Concept map; link colours show the link type (legend at the top).
- Click a Concept (or pick one in the search box): it and its direct links stay bright, the rest fades, and the
  side panel lists its links by relation with the Notes that teach each one. Click the background to reset.
- Filter by area, link type, or show confirmed Concepts only."""
import subprocess
import sys
from pathlib import Path

import dash_cytoscape as cyto
from dash import Dash, Input, Output, ctx, dcc, html

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_map import AREAS, CONCEPTS, LINK_COLOUR, LINKS, STEP_COLOUR, STEPS, note_title  # noqa: E402

AREA_OF = {cid: next(a for a, _, member in AREAS if member(c)) for cid, c in CONCEPTS.items()}
AREA_NAME = {a: title for a, title, _ in AREAS if a in AREA_OF.values()}
TITLES = {v: note_title(v) for v in {v for c in CONCEPTS.values() for v in c["videos"]}}
# How a link reads from the clicked Concept's side: (when it is the link's first end, when it is the second end).
RELATION = {"needs": ("builds on", "leads to"), "is a kind of": ("is a kind of", "has kinds"),
            "fixes": ("fixes", "fixed by"), "compared with": ("compared with", "compared with"),
            "used in": ("used in", "uses")}


def neato(nodes, edges, extra="", sep=14):
    """Graphviz neato (Graphviz is already used by build_map.py). nodes {id: (width, height) in px}, edges
    [(a, b, weight)]. Boxes never overlap. Returns node centres in px."""
    dot = ["graph G {", f'graph [overlap=false, sep="+{sep}", splines=false{extra}]; node [shape=box, fixedsize=true];']
    dot += [f'"{n}" [width={w / 72:.2f}, height={h / 72:.2f}];' for n, (w, h) in nodes.items()]
    dot += [f'"{u}" -- "{v}" [weight={wt}];' for u, v, wt in edges] + ["}"]
    out = subprocess.run(["neato", "-Tplain"], input="\n".join(dot), capture_output=True, text=True, check=True).stdout
    return {p[1].strip('"'): (float(p[2]) * 72, -float(p[3]) * 72)
            for p in (line.split() for line in out.splitlines()) if p[0] == "node"}


def positions():
    """Two levels: lay out each area on its own (Concepts sized like their labels so labels do not overlap), then
    lay out the areas as big boxes, pulled together by how many links run between them."""
    local, size = {}, {}
    for a in AREA_NAME:
        inside = {cid: (min(len(CONCEPTS[cid]["name"]) * 8, 150) + 10, 20 * (len(CONCEPTS[cid]["name"]) * 8 // 150 + 1) + 30)
                  for cid in CONCEPTS if AREA_OF[cid] == a}
        pos = neato(inside, [(l["a"], l["b"], 1) for l in LINKS if l["a"] in inside and l["b"] in inside])
        xs = [pos[c][0] + sx * inside[c][0] / 2 for c in pos for sx in (-1, 1)]
        ys = [pos[c][1] + sy * inside[c][1] / 2 for c in pos for sy in (-1, 1)]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        local.update({c: (x - cx, y - cy) for c, (x, y) in pos.items()})
        size[a] = (max(xs) - min(xs) + 120, max(ys) - min(ys) + 400)     # room for the padding and a 3-line title
    between = {}
    for l in LINKS:
        pair = tuple(sorted((AREA_OF[l["a"]], AREA_OF[l["b"]])))
        if pair[0] != pair[1]:
            between[pair] = between.get(pair, 0) + 1
    centre = neato(size, [(u, v, n) for (u, v), n in between.items()], ", mode=major, overlap=vpsc, pack=true, start=3", sep=60)
    return {c: {"x": centre[AREA_OF[c]][0] + x, "y": centre[AREA_OF[c]][1] + y} for c, (x, y) in local.items()}


POS = positions()
LAYOUT = {"name": "preset", "fit": True, "padding": 20}


def elements(areas, types, confirmed_only):
    keep = {cid for cid, c in CONCEPTS.items()
            if AREA_OF[cid] in areas and (c["status"] == "confirmed" or not confirmed_only)}
    boxes = [{"data": {"id": f"area:{a}", "label": AREA_NAME[a]}, "classes": "area", "selectable": False}
             for a in AREA_NAME if a in {AREA_OF[cid] for cid in keep}]
    nodes = [{"data": {"id": cid, "label": c["name"], "colour": STEP_COLOUR[c["step"]], "parent": f"area:{AREA_OF[cid]}"},
              "position": POS[cid], "classes": c["status"]} for cid, c in CONCEPTS.items() if cid in keep]
    edges = [{"data": {"source": l["a"], "target": l["b"], "label": l["type"], "colour": LINK_COLOUR[l["type"]]},
              "classes": l["status"] + (" undirected" if l["type"] == "compared with" else "")}
             for l in LINKS if l["a"] in keep and l["b"] in keep and l["type"] in types
             and (l["status"] == "confirmed" or not confirmed_only)]
    return boxes + nodes + edges


STYLE = [
    {"selector": "node", "style": {"label": "data(label)", "background-color": "data(colour)", "font-size": 16,
                                   "text-valign": "top", "text-margin-y": -4, "width": 20, "height": 20,
                                   "font-family": "Latin Modern Roman, serif", "min-zoomed-font-size": 7,
                                   "text-wrap": "wrap", "text-max-width": 150,
                                   "text-background-color": "white", "text-background-opacity": 0.7}},
    {"selector": "node.draft", "style": {"background-opacity": 0.4, "color": "#777"}},
    {"selector": "node.confirmed", "style": {"border-width": 2, "border-color": "black"}},
    {"selector": "node.area", "style": {"background-color": "#F3F1EC", "background-opacity": 1, "border-width": 1,
                                        "border-color": "#B8B2A6", "shape": "round-rectangle", "padding": 18,
                                        "font-size": 110, "font-weight": "bold", "color": "#5A5246",
                                        "text-valign": "top", "text-margin-y": -6, "min-zoomed-font-size": 3,
                                        "text-background-opacity": 0, "text-max-width": 1400}},
    {"selector": "edge", "style": {"line-color": "data(colour)", "target-arrow-color": "data(colour)",
                                   "target-arrow-shape": "triangle", "curve-style": "bezier", "width": 1.6,
                                   "opacity": 0.3, "arrow-scale": 0.9}},
    {"selector": "edge.draft", "style": {"line-style": "dashed"}},
    {"selector": "edge.undirected", "style": {"target-arrow-shape": "none"}},
]


def focus_style(cid):
    """Stylesheet with the Concept, its direct neighbours and their links bright and everything else faded."""
    near = {cid} | {l["a"] for l in LINKS if l["b"] == cid} | {l["b"] for l in LINKS if l["a"] == cid}
    return STYLE + [
        {"selector": "node:childless", "style": {"opacity": 0.1}},
        {"selector": "node.area", "style": {"text-opacity": 0.3}},
        {"selector": "edge", "style": {"opacity": 0.04}},
        {"selector": ", ".join(f"node[id = '{n}']" for n in near), "style": {"opacity": 1, "z-index": 9, "min-zoomed-font-size": 0, "font-size": 24}},
        {"selector": f"node[id = '{cid}']", "style": {"width": 34, "height": 34, "border-width": 4,
                                                      "border-color": "#E45756", "font-size": 30, "font-weight": "bold"}},
        {"selector": f"edge[source = '{cid}'], edge[target = '{cid}']",
         "style": {"opacity": 1, "width": 3.5, "z-index": 9, "label": "data(label)", "font-size": 12,
                   "text-rotation": "autorotate", "color": "#333", "text-background-color": "white",
                   "text-background-opacity": 0.9}},
    ]


def relations(cid):
    """{relation: [neighbour id, ...]} for every link of the Concept, read from its side."""
    groups = {}
    for l in LINKS:
        for mine, other, side in ((l["a"], l["b"], 0), (l["b"], l["a"], 1)):
            if mine == cid:
                groups.setdefault(RELATION[l["type"]][side], []).append(other)
    order = [r for pair in RELATION.values() for r in pair]
    return {r: groups[r] for r in dict.fromkeys(order) if r in groups}


def panel(cid):
    c = CONCEPTS[cid]
    body = [html.H3(c["name"], style={"margin": "0"}),
            html.Div(f"{AREA_NAME[AREA_OF[cid]]} · step {c['step']} ({STEPS[c['step']]}) · {c['status']}",
                     style={"color": "#666"}),
            html.Div("Taught in: " + "; ".join(TITLES[v] for v in c["videos"]) if c["videos"] else "No Note yet.",
                     style={"margin": "6px 0 10px"})]
    for rel, others in relations(cid).items():
        colour = LINK_COLOUR[next(t for t, pair in RELATION.items() if rel in pair)]
        body.append(html.H4(f"{rel} ({len(others)})", style={"color": colour, "margin": "12px 0 4px"}))
        body.append(html.Ul([html.Li([html.B(CONCEPTS[o]["name"]),
                                      html.Div("; ".join(TITLES[v] for v in CONCEPTS[o]["videos"]) or "No Note yet.",
                                               style={"fontSize": "13px", "color": "#555"})])
                             for o in others], style={"margin": "0", "paddingLeft": "18px"}))
    return body


HINT = html.I("Click a Concept, or pick one in the search box, to see how it is connected. "
              "Click the background to reset.")
legend = html.Div([html.Span([html.Span(style={"display": "inline-block", "width": "26px", "height": "4px",
                                               "background": colour, "verticalAlign": "middle", "marginRight": "5px"}),
                              rel], style={"marginRight": "14px"}) for rel, colour in LINK_COLOUR.items()]
                  + [html.Span("dashed = draft · faint node = draft · black ring = confirmed", style={"color": "#666"})])

app = Dash(__name__, title="Course map")
app.layout = html.Div(style={"fontFamily": "serif", "margin": "10px"}, children=[
    html.Div(style={"display": "flex", "gap": "24px", "alignItems": "flex-start", "flexWrap": "wrap"}, children=[
        html.H2("Course map", style={"margin": "0"}),
        dcc.Dropdown(id="search", options=sorted(({"label": c["name"], "value": cid} for cid, c in CONCEPTS.items()),
                                                 key=lambda o: o["label"].lower()),
                     placeholder="Search a Concept...", style={"width": "320px"}),
        html.Details([html.Summary("Filters"), html.Div(style={"display": "flex", "gap": "24px"}, children=[
            html.Div([html.B("Areas"), dcc.Checklist(id="areas", options=[{"label": f" {t}", "value": a}
                                                                          for a, t in AREA_NAME.items()],
                                                     value=list(AREA_NAME), style={"columnCount": 2})]),
            html.Div([html.B("Link types"), dcc.Checklist(id="types", options=list(LINK_COLOUR), value=list(LINK_COLOUR)),
                      html.Br(), dcc.Checklist(id="confirmed", options=[{"label": " confirmed only", "value": "yes"}],
                                               value=[])])])]),
    ]),
    html.Div(legend, style={"margin": "6px 0", "fontSize": "14px"}),
    html.Div(style={"display": "flex", "gap": "10px"}, children=[
        cyto.Cytoscape(id="map", stylesheet=STYLE, layout=LAYOUT, elements=elements(set(AREA_NAME), set(LINK_COLOUR), False),
                       minZoom=0.05, maxZoom=3, style={"flex": "1", "height": "84vh", "border": "1px solid #ccc"}),
        html.Div(HINT, id="info", style={"width": "360px", "height": "84vh", "overflowY": "auto", "fontSize": "15px"}),
    ]),
])


@app.callback(Output("map", "elements"), Output("map", "layout"),
              Input("areas", "value"), Input("types", "value"), Input("confirmed", "value"), prevent_initial_call=True)
def update(areas, types, confirmed):
    return elements(set(areas), set(types), bool(confirmed)), LAYOUT


@app.callback(Output("info", "children"), Output("map", "stylesheet"),
              Input("map", "selectedNodeData"), Input("search", "value"))
def show(selected, search):
    cid = search if ctx.triggered_id == "search" else (selected[-1]["id"] if selected else None)
    if cid not in CONCEPTS:
        return HINT, STYLE
    return panel(cid), focus_style(cid)


# Search: select the Concept in the graph and zoom to it and its neighbours (cytoscape keeps its instance on the container's _cyreg).
app.clientside_callback(
    """function(cid) {
        const el = document.getElementById('map'); const cy = el && el._cyreg && el._cyreg.cy;
        if (!cy || !cid) return window.dash_clientside.no_update;
        const n = cy.getElementById(cid); if (n.empty()) return window.dash_clientside.no_update;
        cy.nodes().unselect(); n.select();
        const near = n.closedNeighborhood(), bb = near.boundingBox();
        const zoom = Math.min(1.2, Math.max(0.5, Math.min(cy.width() / bb.w, cy.height() / bb.h) * 0.9));
        cy.animate({zoom: zoom, center: {eles: n}}, {duration: 400});
        return window.dash_clientside.no_update;
    }""", Output("search", "className"), Input("search", "value"))


if __name__ == "__main__":
    app.run(debug=False)
