"""Download a street map from OpenStreetMap with OSMnx and save it for run.py. Needs the internet once; everything
else runs offline from data/. Map data © OpenStreetMap contributors (ODbL).

    python get_map.py                       # central Chicago, the default map (the exact command is below)
    python get_map.py --place "Rome, Italy" --name rome --label Rome --dist 2500
    python get_map.py --cut-from chicago --point 41.8820 -87.6395 --dist 550 --name chicago-west-loop \
        --label "Chicago, West Loop"         # a small part of a saved map, no download
    python get_map.py --keep-streets --keep-places   # Chicago again from data/, e.g. after changing the goal rules

--place finds the place's centre and takes the streets within --dist metres of it (a square about 2 x dist across);
--point gives the centre directly; --cut-from takes the square from a map already in data/ instead of downloading.
Saves data/<name>.graphml.gz (the drivable streets, as OSMnx gives them), data/<name>-places.json (the places with
the --goals-tag tag), data/<name>.json (the label, the start and goal, the goals of the multi-goal search) and the
preview data/<name>.png. Without --start/--goal, the start and goal are the intersections nearest two opposite
corners of the map.

The multi-goal goals: the places whose tags match every KEY=VALUE of --goals-tag (the first one is asked from
OpenStreetMap; default: hospitals), whose straight-line distance from the start is within --goals-dist, and of
those --goals-count spread out (the farthest from the start first, then each time the one farthest from those
already chosen), each snapped to its nearest intersection.
"""
import argparse
import gzip
import json
import sys
from pathlib import Path

import osmnx as ox

DATA = Path(__file__).resolve().parent / "data"
CHICAGO = ["--point", "41.8819", "-87.6300", "--dist", "2500", "--name", "chicago", "--label", "Chicago",
           "--start", "41.8648", "-87.6559", "--goal", "41.8975", "-87.6075",
           "--goals-tag", "railway=station", "--goals-dist", "3000", "5000", "--goals-count", "4"]


def snap(G, lat, lon):
    node = int(ox.distance.nearest_nodes(G, X=lon, Y=lat))
    return {"lat": G.nodes[node]["y"], "lon": G.nodes[node]["x"], "node": node}


def fetch_places(centre, dist, goals_tag):
    """The places within dist of centre with the first KEY=VALUE of goals_tag (one OpenStreetMap request): their
    name, position and the tags named in goals_tag."""
    key, value = goals_tag[0].split("=", 1)
    try:
        feats = ox.features_from_point(centre, tags={key: value}, dist=dist)
    except ox._errors.InsufficientResponseError:
        return []                          # nothing with that tag here: no multi-goal search on this map
    keys = ["name"] + [t.split("=", 1)[0] for t in goals_tag]
    places = []
    for (kind, osm_id), f in feats.iterrows():
        c = f.geometry.centroid
        tags = {k: f[k] for k in keys if k in f.index and isinstance(f[k], str)}
        places.append({"osm": f"{kind}/{osm_id}", "lat": round(c.y, 7), "lon": round(c.x, 7), **tags})
    return places


def choose_goals(G, places, goals_tag, start, near=0.0, far=float("inf"), count=None):
    """The places that match every KEY=VALUE and lie near..far metres (straight line) from start, spread out:
    the farthest from start first, then each time the one farthest from those chosen. Snapped to intersections."""
    tags = dict(t.split("=", 1) for t in goals_tag)
    dist = lambda a, b: ox.distance.great_circle(a["lat"], a["lon"], b["lat"], b["lon"])
    pool = [p for p in places if all(p.get(k) == v for k, v in tags.items()) and near <= dist(p, start) <= far]
    chosen = []
    while pool and len(chosen) < (count or len(pool) + len(chosen)):
        best = max(pool, key=lambda p: min((dist(p, c) for c in chosen), default=dist(p, start)))
        chosen.append(best)
        pool.remove(best)
    goals = [{"name": p.get("name", ""), "osm": p["osm"], **snap(G, p["lat"], p["lon"])} for p in chosen]
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
    ap.add_argument("--goals-dist", nargs=2, type=float, metavar=("NEAR", "FAR"),
                    help="keep goals this many metres from the start, in a straight line")
    ap.add_argument("--goals-count", type=int, help="keep this many goals, spread out")
    ap.add_argument("--cut-from", metavar="NAME", help="cut the square from data/NAME.* (no download)")
    ap.add_argument("--keep-streets", action="store_true", help="use the streets already in data/ (no download)")
    ap.add_argument("--keep-places", action="store_true", help="use the places already in data/ (no download)")
    args = ap.parse_args(argv if "--name" in argv else CHICAGO + argv)

    ox.settings.use_cache = False          # no cache folder; OSMnx's default user agent, no personal data
    centre = tuple(args.point) if args.point else ox.geocoder.geocode(args.place)
    streets_from = args.cut_from or (args.name if args.keep_streets else None)
    if streets_from:
        with gzip.open(DATA / f"{streets_from}.graphml.gz", "rt", encoding="utf-8") as f:
            G = ox.load_graphml(graphml_str=f.read())
        if args.cut_from:
            G = ox.truncate.truncate_graph_bbox(G, ox.utils_geo.bbox_from_point(centre, args.dist))
    else:
        G = ox.graph_from_point(centre, dist=args.dist, network_type="drive")
    G = ox.truncate.largest_component(G)   # keep only streets connected to each other

    lats = [d["y"] for _, d in G.nodes(data=True)]
    lons = [d["x"] for _, d in G.nodes(data=True)]
    corner = lambda f: (min(lats) + f * (max(lats) - min(lats)), min(lons) + f * (max(lons) - min(lons)))
    start = args.start or corner(0.1)      # near the south-west corner
    goal = args.goal or corner(0.9)        # near the north-east corner

    if args.cut_from:                      # the source map's places that are inside the cut
        source = json.loads((DATA / f"{args.cut_from}.json").read_text())
        args.goals_tag = source["goals_tag"]
        west, south, east, north = ox.utils_geo.bbox_from_point(centre, args.dist)
        places = [p for p in json.loads((DATA / f"{args.cut_from}-places.json").read_text())
                  if west <= p["lon"] <= east and south <= p["lat"] <= north]
    elif args.keep_places:
        places = json.loads((DATA / f"{args.name}-places.json").read_text())
    else:
        places = fetch_places(centre, args.dist, args.goals_tag)
    start, goal = snap(G, *start), snap(G, *goal)
    goals = choose_goals(G, places, args.goals_tag, start, *(args.goals_dist or (0, float("inf"))), args.goals_count)

    DATA.mkdir(exist_ok=True)
    if not args.keep_streets:
        tmp = DATA / f"{args.name}.graphml"
        ox.save_graphml(G, tmp)
        with open(tmp, "rb") as src, gzip.open(DATA / f"{args.name}.graphml.gz", "wb") as dst:
            dst.write(src.read())
        tmp.unlink()
    if not args.keep_places:
        (DATA / f"{args.name}-places.json").write_text(json.dumps(places, indent=1, ensure_ascii=False))
    info = {"label": args.label or args.place or args.name,
            "source": f"OpenStreetMap via OSMnx {ox.__version__}, network_type='drive', "
                      f"{args.dist:g} m around {centre[0]:.5f}, {centre[1]:.5f}"
                      + (f", cut from data/{args.cut_from}" if args.cut_from else ""),
            "credit": "Map data © OpenStreetMap contributors (ODbL)",
            "start": start, "goal": goal,
            "goals_tag": args.goals_tag, "goals_dist": args.goals_dist, "goals_count": args.goals_count,
            "goals": goals}
    (DATA / f"{args.name}.json").write_text(json.dumps(info, indent=1, ensure_ascii=False))
    print(f"{args.name}: {len(G)} intersections, {len(goals)} goals for the multi-goal search")

    import render, streets                 # the preview picture
    render.preview(streets.load_map(args.name), DATA / f"{args.name}.png")


if __name__ == "__main__":
    main(sys.argv[1:])
