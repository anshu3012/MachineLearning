"""Interactive Course map (Dash + Dash Cytoscape). Reads the same concepts.yaml as the PDF.

Run:  python course_map/app.py   then open http://127.0.0.1:8050
- Filter by pipeline step, link type, or show confirmed Concepts only.
- Click a Concept to highlight its Links and list the Notes that teach it."""
from pathlib import Path

import dash_cytoscape as cyto
import yaml
from dash import Dash, Input, Output, dcc, html

ROOT = Path(__file__).resolve().parent.parent
DATA = yaml.safe_load(open(ROOT / "course_map" / "concepts.yaml"))
STEPS, NOTES = DATA["steps"], DATA["notes"]
CONCEPTS = {c["id"]: c for c in DATA["concepts"]}
LINKS = [dict(zip(("a", "type", "b", "status"), link)) for link in DATA["links"]]
STEP_COLOUR = {0: "#6B6B6B", 1: "#B279A2", 2: "#4C78A8", 3: "#4C78A8", 4: "#4C78A8", 5: "#54A24B", 6: "#54A24B",
               7: "#54A24B", 8: "#F58518", 9: "#E45756", 10: "#E45756", 11: "#72B7B2", 12: "#72B7B2", 13: "#72B7B2"}
LINK_COLOUR = {"needs": "#4C78A8", "is a kind of": "#6B6B6B", "fixes": "#54A24B", "compared with": "#B279A2",
               "used in": "#F58518"}


def elements(steps, types, confirmed_only):
    keep = {cid for cid, c in CONCEPTS.items()
            if c["step"] in steps and (c["status"] == "confirmed" or not confirmed_only)}
    nodes = [{"data": {"id": cid, "label": c["name"], "colour": STEP_COLOUR[c["step"]]},
              "classes": c["status"]} for cid, c in CONCEPTS.items() if cid in keep]
    edges = [{"data": {"source": l["a"], "target": l["b"], "label": l["type"], "colour": LINK_COLOUR[l["type"]]},
              "classes": l["status"] + (" undirected" if l["type"] == "compared with" else "")}
             for l in LINKS if l["a"] in keep and l["b"] in keep and l["type"] in types
             and (l["status"] == "confirmed" or not confirmed_only)]
    return nodes + edges


STYLE = [
    {"selector": "node", "style": {"label": "data(label)", "background-color": "data(colour)", "font-size": 13,
                                   "text-valign": "top", "text-margin-y": -4, "width": 22, "height": 22,
                                   "font-family": "Latin Modern Roman, serif"}},
    {"selector": "node.draft", "style": {"opacity": 0.4}},
    {"selector": "node.confirmed", "style": {"border-width": 2, "border-color": "black"}},
    {"selector": "edge", "style": {"line-color": "data(colour)", "target-arrow-color": "data(colour)",
                                   "target-arrow-shape": "triangle", "curve-style": "bezier", "width": 2,
                                   "label": "data(label)", "font-size": 9, "text-rotation": "autorotate",
                                   "color": "#555", "text-background-color": "white", "text-background-opacity": 0.8}},
    {"selector": "edge.draft", "style": {"line-style": "dashed", "opacity": 0.6}},
    {"selector": "edge.undirected", "style": {"target-arrow-shape": "none"}},
    {"selector": ".faded", "style": {"opacity": 0.08}},
    {"selector": "node:selected", "style": {"border-width": 4, "border-color": "#E45756", "width": 30, "height": 30}},
]

app = Dash(__name__, title="Course map")
app.layout = html.Div(style={"fontFamily": "serif", "margin": "12px"}, children=[
    html.H2("Course map"),
    html.Div(style={"display": "flex", "gap": "28px", "flexWrap": "wrap"}, children=[
        html.Div([html.B("Pipeline steps"),
                  dcc.Checklist(id="steps", options=[{"label": f" {k} {v}", "value": k} for k, v in STEPS.items()],
                                value=list(STEPS), style={"columnCount": 2})]),
        html.Div([html.B("Link types"),
                  dcc.Checklist(id="types", options=list(LINK_COLOUR), value=list(LINK_COLOUR))]),
        html.Div([html.B("Show"),
                  dcc.RadioItems(id="confirmed", options=[{"label": " all Concepts", "value": False},
                                                         {"label": " confirmed only", "value": True}], value=False),
                  dcc.Dropdown(id="layout", options=["cose", "breadthfirst", "circle", "concentric"], value="cose",
                               clearable=False, style={"width": "180px", "marginTop": "8px"})]),
        html.Div(id="info", style={"maxWidth": "420px"}),
    ]),
    cyto.Cytoscape(id="map", stylesheet=STYLE, style={"width": "100%", "height": "78vh", "border": "1px solid #ccc"},
                   layout={"name": "cose", "nodeRepulsion": 9000, "idealEdgeLength": 90}),
])


@app.callback(Output("map", "elements"), Output("map", "layout"),
              Input("steps", "value"), Input("types", "value"), Input("confirmed", "value"), Input("layout", "value"))
def update(steps, types, confirmed_only, layout):
    return elements(set(steps), set(types), confirmed_only), {"name": layout, "nodeRepulsion": 9000,
                                                              "idealEdgeLength": 90, "animate": False}


@app.callback(Output("info", "children"), Output("map", "stylesheet"), Input("map", "tapNodeData"))
def show(node):
    if not node:
        return html.I("Click a Concept to see its links and Notes."), STYLE
    c = CONCEPTS[node["id"]]
    notes = [f"Note {v}" + ("" if v in NOTES else " (coming)") for v in c["videos"]]
    links = [f"{CONCEPTS[l['a']]['name']} {l['type']} {CONCEPTS[l['b']]['name']}"
             for l in LINKS if node["id"] in (l["a"], l["b"])]
    near = {node["id"]} | {l["a"] for l in LINKS if l["b"] == node["id"]} | {l["b"] for l in LINKS if l["a"] == node["id"]}
    highlight = STYLE + [{"selector": "node", "style": {"opacity": 0.12}}] + \
        [{"selector": f"node[id = '{n}']", "style": {"opacity": 1}} for n in near] + \
        [{"selector": "edge", "style": {"opacity": 0.05}},
         {"selector": f"edge[source = '{node['id']}'], edge[target = '{node['id']}']", "style": {"opacity": 1}}]
    return html.Div([html.B(c["name"]), f"  (step {c['step']}: {STEPS[c['step']]}, {c['status']})",
                     html.Div("Taught in: " + ", ".join(notes)),
                     html.Ul([html.Li(t) for t in links])]), highlight


if __name__ == "__main__":
    app.run(debug=False)
