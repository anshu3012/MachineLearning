"""Section 6.3: for the ambiguous words "that", "about" and "as", the share of each tag of the NEXT word, per tag of the
word itself, in the CoNLL-2000 training sentences (same counting as the Notebook: lower-cased word, not first or
last in its sentence). Different tags of the same word are followed by different next tags.
Run: python next_tags.py  -> next_tags.png (Plotly stacked horizontal bars)"""
import gzip
from collections import Counter, defaultdict
from pathlib import Path

import plotly.graph_objects as go

from common import BLUE, GREEN, GREY, ORANGE, PURPLE, RED

HERE = Path(__file__).parent
sents, cur = [], []
for line in gzip.open(HERE.parent / "data" / "train.wordpos.gz", "rt"):
    p = line.split()
    if p:
        cur.append((p[0], p[1]))
    elif cur:
        sents.append(cur)
        cur = []
sents += [cur] if cur else []
nxt = defaultdict(Counter)
for s in sents:
    for j, (w, t) in enumerate(s):
        if w.lower() in ("that", "about", "as") and 0 < j < len(s) - 1:
            nxt[w.lower(), t][s[j + 1][1]] += 1
uses = {k: sum(v.values()) for k, v in nxt.items()}
assert [uses[k] for k in [("that", "WDT"), ("that", "DT"), ("that", "IN"), ("about", "RB"), ("about", "IN"),
                          ("as", "RB"), ("as", "IN")]] == [476, 272, 1053, 70, 371, 117, 789]        # the Note's table
assert nxt["about", "RB"]["$"] == 70 and nxt["that", "DT"]["NN"] == 166 and nxt["as", "IN"]["DT"] == 233

ROWS = [("that", "WDT", "relative pronoun"), ("that", "DT", "determiner"), ("that", "IN", "conjunction"),
        ("about", "RB", "adverb"), ("about", "IN", "preposition"), ("as", "RB", "adverb"), ("as", "IN", "preposition")]
COL = {"VBD": RED, "VBZ": RED, "VBP": RED, "MD": RED, "NN": BLUE, "DT": GREEN, "PRP": GREEN, "$": ORANGE,
       "CD": PURPLE, "JJ": BLUE, "RB": PURPLE}
fig = go.Figure()
labels = [f'"{w}" as {t} ({name})' for w, t, name in ROWS]
for rank in range(4):
    xs, texts, colours = [], [], []
    for w, t, _ in ROWS:
        top = nxt[w, t].most_common(4)
        tag, n = top[rank] if rank < len(top) else ("", 0)
        share = n / uses[w, t]
        xs.append(share)
        texts.append(tag if share >= 0.08 else "")
        colours.append(COL.get(tag, GREY))
    fig.add_trace(go.Bar(y=labels, x=xs, orientation="h", text=texts, textposition="inside", insidetextanchor="middle",
                         marker=dict(color=colours, line=dict(color="white", width=2)), textfont=dict(size=20, color="white"),
                         showlegend=False))
rest = [1 - sum(n for _, n in nxt[w, t].most_common(4)) / uses[w, t] for w, t, _ in ROWS]
fig.add_trace(go.Bar(y=labels, x=rest, orientation="h", marker=dict(color="#DDDDDD", line=dict(color="white", width=2)),
                     text=["other" if r > 0.12 else "" for r in rest], textposition="inside", showlegend=False))
fig.update_yaxes(autorange="reversed")
fig.update_layout(template="simple_white", barmode="stack", width=1150, height=560,
                  font=dict(family="Latin Modern Roman", size=20),
                  title=dict(text="tag of the NEXT word, share of uses (training sentences)", x=0.5),
                  xaxis=dict(title="share", tickformat=".0%", range=[0, 1]), margin=dict(l=20, r=20, t=70, b=60))

if __name__ == "__main__":
    fig.write_image(HERE / "next_tags.png", scale=2)
