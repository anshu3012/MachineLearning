"""Run chosen code cells of notebook.ipynb in order: python run_cells.py 1 3 9 22"""
import json, sys
nb = json.load(open("notebook.ipynb"))
g = {}
for i in map(int, sys.argv[1:]):
    src = "".join(nb["cells"][i]["source"])
    src = "\n".join(l for l in src.splitlines() if not l.lstrip().startswith(("%", "!")))
    exec(compile(src, f"cell{i}", "exec"), g)
