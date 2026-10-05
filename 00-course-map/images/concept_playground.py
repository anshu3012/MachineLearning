"""Serverless twin of ../../course_map/app.py: the Concept map with one precomputed frame per Concept. The dropdown
picks a Concept; its frame brightens the Concept and its direct links, zooms to that neighbourhood and lists its
links by relation with the Notes that teach it (the app's side panel). No Dash, no callbacks.

Run: python concept_playground.py -> concept_playground.html   (positions come from app.py, so Graphviz is needed)
"""
import sys
import textwrap
from pathlib import Path

import plotly.graph_objects as go
from sitecustomize import plotlyjs_src

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "course_map"))
from app import AREA_NAME, AREA_OF, CONCEPTS, LINK_COLOUR, LINKS, POS, RELATION, STEP_COLOUR, STEPS, TITLES, \
    relations  # noqa: E402

TYPES = list(LINK_COLOUR)
ANIM = dict(mode="immediate", frame=dict(duration=0, redraw=True), transition=dict(duration=0))
# ponytail: one frame per Concept (335) is fine because a frame holds only that Concept's links and neighbours.
ORDER = sorted(CONCEPTS, key=lambda c: (list(AREA_NAME).index(AREA_OF[c]), CONCEPTS[c]["name"].lower()))


def xy(cid):
    return POS[cid]["x"], POS[cid]["y"]


def edge_xy(links):
    """x and y for a line trace drawing every link, None between links."""
    x, y = [], []
    for l in links:
        (xa, ya), (xb, yb) = xy(l["a"]), xy(l["b"])
        x += [xa, xb, None]
        y += [ya, yb, None]
    return dict(x=x, y=y)


def notes(cid):
    c = CONCEPTS[cid]
    return "; ".join(TITLES[v] for v in c["videos"]) or "No Note yet."


def hover(cid):
    c = CONCEPTS[cid]
    return (f"<b>{c['name']}</b><br>{AREA_NAME[AREA_OF[cid]]} · step {c['step']} ({STEPS[c['step']]}) · {c['status']}"
            f"<br>Taught in: {notes(cid)}")


def bounds(cids, pad=0.15):
    xs, ys = [xy(c)[0] for c in cids], [xy(c)[1] for c in cids]
    w, h = max(max(xs) - min(xs), 1200), max(max(ys) - min(ys), 600)
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    return dict(xaxis=dict(range=[cx - w * (0.5 + pad), cx + w * (0.5 + pad)]),
                yaxis=dict(range=[cy - h * (0.5 + pad), cy + h * (0.5 + pad)]))


def panel(cid):
    """The app's side panel as one annotation: Notes, then every relation with its neighbours."""
    lines = [f"<b>{CONCEPTS[cid]['name']}</b>", f"Taught in: {notes(cid)}", ""]
    for rel, others in relations(cid).items():
        colour = LINK_COLOUR[next(t for t, pair in RELATION.items() if rel in pair)]
        body = "; ".join(CONCEPTS[o]["name"] for o in others)
        lines += [f"<span style='color:{colour}'><b>{rel} ({len(others)})</b></span>: {body}", ""]
    text = "<br>".join("<br>".join(textwrap.wrap(line, 28)) if not line.startswith("<b>") else line
                       for line in lines)
    return [dict(text=text, x=0.705, xref="paper", y=1, yref="paper", xanchor="left", yanchor="top", align="left",
                 showarrow=False, font=dict(size=11))]


def frame(cid):
    """Bright traces for the Concept's links (per type), their type labels, its neighbours and itself."""
    mine = [l for l in LINKS if cid in (l["a"], l["b"])]
    near = sorted({l["a"] for l in mine} | {l["b"] for l in mine} - {cid})
    data = [go.Scatter(**edge_xy([l for l in mine if l["type"] == t])) for t in TYPES]
    data.append(go.Scatter(x=[(xy(l["a"])[0] + xy(l["b"])[0]) / 2 for l in mine],
                           y=[(xy(l["a"])[1] + xy(l["b"])[1]) / 2 for l in mine], text=[l["type"] for l in mine],
                           textfont=dict(color=[LINK_COLOUR[l["type"]] for l in mine])))
    data.append(go.Scatter(x=[xy(c)[0] for c in near], y=[xy(c)[1] for c in near],
                           text=[CONCEPTS[c]["name"] for c in near], hovertext=[hover(c) for c in near],
                           marker=dict(color=[STEP_COLOUR[CONCEPTS[c]["step"]] for c in near])))
    data.append(go.Scatter(x=[xy(cid)[0]], y=[xy(cid)[1]], text=[f"<b>{CONCEPTS[cid]['name']}</b>"],
                           hovertext=[hover(cid)], marker=dict(color=STEP_COLOUR[CONCEPTS[cid]["step"]])))
    data.append(go.Scatter(**AREA_TITLES))
    c = CONCEPTS[cid]
    title = (f"<b>{c['name']}</b><br><span style='font-size:12px'>{AREA_NAME[AREA_OF[cid]]} · step {c['step']} "
             f"({STEPS[c['step']]}) · {c['status']}</span>")   # two lines: fits a phone-width iframe
    return go.Frame(name=cid, data=data, traces=FILLED, layout=dict(title=title, annotations=panel(cid),
                                                                   **bounds(near + [cid])))


# Area boxes: a rectangle round each area's Concepts (static shapes); their titles are a text trace that only the
# Concept frames fill, because at the whole-map zoom the 18 titles would pile up.
SHAPES, AREA_TITLES = [], dict(x=[], y=[], text=[])
for a, title in AREA_NAME.items():
    pts = [xy(c) for c in CONCEPTS if AREA_OF[c] == a]
    x0, x1 = min(p[0] for p in pts) - 90, max(p[0] for p in pts) + 90
    y0, y1 = min(p[1] for p in pts) - 60, max(p[1] for p in pts) + 60
    SHAPES.append(dict(type="rect", x0=x0, x1=x1, y0=y0, y1=y1, fillcolor="#F3F1EC", opacity=0.5, layer="below",
                       line=dict(color="#B8B2A6", width=1)))
    AREA_TITLES["x"].append((x0 + x1) / 2), AREA_TITLES["y"].append(y1), AREA_TITLES["text"].append(f"<b>{title}</b>")

FILLED = list(range(len(TYPES) + 1, len(TYPES) + 10))     # the nine traces every frame replaces
HINT = "Pick a Concept in the dropdown to see how it is connected"
full = bounds(CONCEPTS, pad=0.03)
frames = [go.Frame(name="all", data=[go.Scatter(x=[], y=[])] * len(FILLED), traces=FILLED,
                   layout=dict(title=HINT, annotations=[], **full))] + [frame(c) for c in ORDER]

# Base traces: every link per type (faint; the legend), every Concept (dots, hover for the name and Notes),
# then the nine traces the frames fill: 5 link types, link labels, neighbours, the chosen Concept, area titles.
fig = go.Figure(frames=frames)
for t in TYPES:
    fig.add_trace(go.Scatter(**edge_xy([l for l in LINKS if l["type"] == t]), mode="lines", name=t,
                             line=dict(color=LINK_COLOUR[t], width=1), opacity=0.3, hoverinfo="skip"))
fig.add_trace(go.Scatter(x=[xy(c)[0] for c in CONCEPTS], y=[xy(c)[1] for c in CONCEPTS], mode="markers",
                         hovertext=[hover(c) for c in CONCEPTS], hoverinfo="text", showlegend=False,
                         marker=dict(size=6, color=[STEP_COLOUR[c["step"]] for c in CONCEPTS.values()],
                                     opacity=[1 if c["status"] == "confirmed" else 0.4 for c in CONCEPTS.values()],
                                     line=dict(color="black", width=[1 if c["status"] == "confirmed" else 0
                                                                     for c in CONCEPTS.values()]))))
for t in TYPES:
    fig.add_trace(go.Scatter(x=[], y=[], mode="lines", line=dict(color=LINK_COLOUR[t], width=3), hoverinfo="skip",
                             showlegend=False))
fig.add_trace(go.Scatter(x=[], y=[], mode="text", textfont=dict(size=10), hoverinfo="skip", showlegend=False))
fig.add_trace(go.Scatter(x=[], y=[], mode="markers+text", textposition="top center", textfont=dict(size=11),
                         hoverinfo="text", showlegend=False, marker=dict(size=11, line=dict(color="black", width=1))))
fig.add_trace(go.Scatter(x=[], y=[], mode="markers+text", textposition="top center", textfont=dict(size=13),
                         hoverinfo="text", showlegend=False, marker=dict(size=18, line=dict(color="#E45756", width=4))))
fig.add_trace(go.Scatter(x=[], y=[], mode="text", textposition="top center", hoverinfo="skip", showlegend=False,
                         textfont=dict(size=12, color="#5A5246")))

buttons = [dict(label="(whole map)", method="animate", args=[["all"], ANIM])]
buttons += [dict(label=f"{AREA_NAME[AREA_OF[c]]} › {CONCEPTS[c]['name']}", method="animate", args=[[c], ANIM])
            for c in ORDER]
fig.update_layout(
    template="simple_white", height=850, margin=dict(l=10, r=10, t=130, b=90), shapes=SHAPES,
    title=dict(text=HINT, y=0.975, yanchor="top", font=dict(size=15)),                      # title, then dropdown; legend at the bottom
    xaxis=dict(domain=[0, 0.69], visible=False, **full["xaxis"]),
    yaxis=dict(visible=False, **full["yaxis"]),
    # legend below the map: on a phone it wraps onto several rows and would cover the dropdown above
    legend=dict(orientation="h", x=0, xanchor="left", y=-0.01, yanchor="top", title="link type: "),
    updatemenus=[dict(type="dropdown", x=0, xanchor="left", y=1.06, yanchor="bottom", active=0, buttons=buttons,
                      font=dict(size=12))])
out = HERE / "concept_playground.html"
fig.write_html(out, include_plotlyjs=plotlyjs_src(out), full_html=True, auto_play=False,
               config={"responsive": True, "displaylogo": False, "scrollZoom": True,
                       "displayModeBar": False})
print(f"{len(frames)} frames, {out.stat().st_size / 1e6:.1f} MB")
