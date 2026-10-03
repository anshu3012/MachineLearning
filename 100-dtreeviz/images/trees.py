"""Tree diagrams drawn with Graphviz `dot` from scikit-learn trees (no matplotlib):
plain_tree   - what sklearn's own export gives (features as x[i]), iris, depth 2
path_tree    - the fully grown iris tree, left to right, node numbers, one flower's prediction path highlighted"""
import subprocess
from pathlib import Path

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, export_graphviz

HERE = Path(__file__).parent
FONT = "Latin Modern Roman,LM Roman 10"   # this spelling makes Graphviz (Pango) find the font
CLASS_FILL = ["#DCE6F2", "#FDE5CC", "#DDEFD9"]           # setosa, versicolor, virginica (light)
CLASS_LINE = ["#4C78A8", "#F58518", "#54A24B"]
SHORT = ["sepal length", "sepal width", "petal length", "petal width"]

iris = load_iris()
X, y = iris.data, iris.target
QUERY = 70                                                 # one versicolor flower, used in the Note and the Notebook


def render(dot_text, name):
    for fmt, extra in (("pdf", []), ("png", ["-Gdpi=200"])):
        subprocess.run(["dot", f"-T{fmt}", *extra, "-o", str(HERE / f"{name}.{fmt}")], input=dot_text.encode(), check=True)


# 1. The plain export: feature indexes, Gini, samples and value lists in every box
small = DecisionTreeClassifier(max_depth=2, random_state=0).fit(X, y)
render(export_graphviz(small, out_file=None, fontname=FONT, rounded=True, special_characters=True), "plain_tree")

# 2. The fully grown tree with node numbers and the prediction path of one flower
full = DecisionTreeClassifier(random_state=0).fit(X, y)
t = full.tree_
path = set(full.decision_path(X[QUERY:QUERY + 1]).indices)
lines = ["digraph tree {", "rankdir=LR; nodesep=0.12; ranksep=0.35;",
         f'node [shape=box, style="rounded,filled", fontname="{FONT}", fontsize=13, penwidth=1.2];',
         f'edge [fontname="{FONT}", fontsize=11, color="#6B6B6B", arrowsize=0.6];']
for n in range(t.node_count):
    counts = [int(round(v * t.n_node_samples[n])) for v in t.value[n][0]]
    cls = max(range(3), key=lambda k: counts[k])
    on = n in path
    if t.children_left[n] == -1:
        label = f"#{n}\\n{iris.target_names[cls]}\\n{counts[0]}/{counts[1]}/{counts[2]}"
        style = f'fillcolor="{CLASS_FILL[cls]}", color="{CLASS_LINE[cls]}"'
    else:
        label = f"#{n}\\n{SHORT[t.feature[n]]}\\n≤ {t.threshold[n]:.2f}?"
        style = 'fillcolor="white", color="#6B6B6B"'
    if on:
        style += ', penwidth=3.5, color="#E45756"'
    lines.append(f'n{n} [label="{label}", {style}];')
for n in range(t.node_count):
    for child, word in ((t.children_left[n], "yes"), (t.children_right[n], "no")):
        if child != -1:
            hot = ', color="#E45756", penwidth=3' if (n in path and child in path) else ""
            lines.append(f'n{n} -> n{child} [label="{word}"{hot}];')
lines.append("}")
render("\n".join(lines), "path_tree")
print("query flower", X[QUERY], iris.target_names[y[QUERY]], "path", sorted(path), "nodes", t.node_count)
