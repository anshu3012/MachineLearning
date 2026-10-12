"""Download a street map from OpenStreetMap with OSMnx and save it for run.py. Needs the internet once; everything
else runs offline from data/. Map data © OpenStreetMap contributors (ODbL).

    python get_map.py                       # central Chicago, the default map (the exact command is below)
    python get_map.py --place "Rome, Italy" --name rome --label Rome --dist 2500
    python get_map.py --cut-from chicago --point 41.8820 -87.6395 --dist 550 --name chicago-west-loop \
        --label "Chicago, West Loop"         # a small part of a saved map, no download

--place finds the place's centre and takes the streets within --dist metres of it (a square about 2 x dist across);
--point gives the centre directly; --cut-from takes the square from a map already in data/ instead of downloading.
Saves data/<name>.graphml.gz (the drivable streets, as OSMnx gives them), data/<name>.json (the label, the start
and goal, the goals of the multi-goal search) and the preview data/<name>.png.
Without --start/--goal, the start and goal are the intersections nearest two opposite corners of the map.
--goals-tag picks the multi-goal goals from OpenStreetMap: every KEY=VALUE must match (default: hospitals)."""
import argparse
import gzip
import json
import sys
from pathlib import Path

import osmnx as ox

DATA = Path(__file__).resolve().parent / "data"
CHICAGO = ["--point", "41.8819", "-87.6300", "--dist", "2500", "--name", "chicago", "--label", "Chicago",
           "--start", "41.8648", "-87.6559", "--goal", "41.8975", "-87.6075",
           "--goals-tag", "railway=station", "train=yes"]


def snap(G, lat, lon):
    node = int(ox.distance.nearest_nodes(G, X=lon, Y=lat))
    return {"lat": G.nodes[node]["y"], "lon": G.nodes[node]["x"], "node": node}


def goals_from_osm(G, centre, dist, goals_tag):
    """The places with every KEY=VALUE tag within dist of centre, each snapped to its nearest intersection."""
    tags = dict(t.split("=", 1) for t in goals_tag)
    key, value = next(iter(tags.items()))
    try:
        feats = ox.features_from_point(centre, tags={key: value}, dist=dist)
    except ox._errors.InsufficientResponseError:
        return []                          # nothing with that tag here: no multi-goal search on this map
    goals = []
    for _, f in feats.iterrows():
        if all(str(f.get(k)) == v for k, v in tags.items()):
            c = f.geometry.centroid
            name = f.get("name")
            goals.append({"name": name if isinstance(name, str) else "", **snap(G, c.y, c.x)})
    return list({g["node"]: g for g in goals}.values())   # one per intersection


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--place", help='a place name OpenStreetMap knows, e.g. "Rome, Italy"')
    ap.add_argument("--point", nargs=2, type=float, metavar=("LAT", "LON"), help="the centre of the map")
    ap.add_argument("--dist", type=float, default=2500, help="metres from the centre to each edge of the map")
    ap.add_argument("--name", required=True, help="file name under data/")
    ap.add_argument("--label", help="the name written in the corner of the pictures")
    ap.add_argument("--start", nargs=2, type=float, metavar=("LAT", "LON"))
    ap.add_argument("--goal", nargs=2, type=float, metavar=("LAT", "LON"))
    ap.add_argument("--goals-tag", nargs="+", default=["amenity=hospital"], metavar="KEY=VALUE")
    ap.add_argument("--cut-from", metavar="NAME", help="cut the square from data/NAME.graphml.gz (no download)")
    args = ap.parse_args(argv or CHICAGO)

    ox.settings.use_cache = False          # no cache folder; OSMnx's default user agent, no personal data
    centre = tuple(args.point) if args.point else ox.geocoder.geocode(args.place)
    if args.cut_from:
        with gzip.open(DATA / f"{args.cut_from}.graphml.gz", "rt", encoding="utf-8") as f:
            G = ox.load_graphml(graphml_str=f.read())
        G = ox.truncate.truncate_graph_bbox(G, ox.utils_geo.bbox_from_point(centre, args.dist))
    else:
        G = ox.graph_from_point(centre, dist=args.dist, network_type="drive")
    G = ox.truncate.largest_component(G)   # keep only streets connected to each other

    lats = [d["y"] for _, d in G.nodes(data=True)]
    lons = [d["x"] for _, d in G.nodes(data=True)]
    corner = lambda f: (min(lats) + f * (max(lats) - min(lats)), min(lons) + f * (max(lons) - min(lons)))
    start = args.start or corner(0.1)      # near the south-west corner
    goal = args.goal or corner(0.9)        # near the north-east corner

    if args.cut_from:                      # the source map's goals that are inside the cut
        source = json.loads((DATA / f"{args.cut_from}.json").read_text())
        goals, args.goals_tag = [g for g in source["goals"] if g["node"] in G], source["goals_tag"]
    else:
        goals = goals_from_osm(G, centre, args.dist, args.goals_tag)

    DATA.mkdir(exist_ok=True)
    tmp = DATA / f"{args.name}.graphml"
    ox.save_graphml(G, tmp)
    with open(tmp, "rb") as src, gzip.open(DATA / f"{args.name}.graphml.gz", "wb") as dst:
        dst.write(src.read())
    tmp.unlink()
    info = {"label": args.label or args.place or args.name,
            "source": f"OpenStreetMap via OSMnx {ox.__version__}, network_type='drive', "
                      f"{args.dist:g} m around {centre[0]:.5f}, {centre[1]:.5f}"
                      + (f", cut from data/{args.cut_from}" if args.cut_from else ""),
            "credit": "Map data © OpenStreetMap contributors (ODbL)",
            "start": snap(G, *start), "goal": snap(G, *goal),
            "goals_tag": args.goals_tag, "goals": goals}
    (DATA / f"{args.name}.json").write_text(json.dumps(info, indent=1, ensure_ascii=False))
    print(f"{args.name}: {len(G)} intersections, {len(goals)} goals for the multi-goal search")

    import render, streets                 # the preview picture
    render.preview(streets.load_map(args.name), DATA / f"{args.name}.png")


if __name__ == "__main__":
    main(sys.argv[1:])
