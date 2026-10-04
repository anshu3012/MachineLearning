"""Self-attention on "money bank" drawn in 2-D, step by step: embeddings, their query/key/value projections,
the scores of bank's query, the value vectors scaled by the weights, their sum y_bank, and finally y_bank for
"river bank" for comparison. Numbers from the Notebook (data/vectors.csv).
Run: python attention_2d.py -> attention_2d.gif, attention_2d_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from common import BLUE, ORANGE, GREEN, RED, PURPLE, GREY, FONT

HERE = Path(__file__).parent
d = pd.read_csv(HERE.parent / "data" / "vectors.csv")


def vec(sentence, word, kind):
    r = d[(d.sentence == sentence) & (d.word == word) & (d.kind == kind)].iloc[0]
    return np.array([r.x, r.y])


MB, RB = "money bank", "river bank"
e_m, e_b, e_r = vec(MB, "money", "e"), vec(MB, "bank", "e"), vec(RB, "river", "e")
P = {k: {w: vec(MB, w, k) for w in ("money", "bank")} for k in "qkv"}
w_m = d[(d.sentence == MB) & (d.word == "bank") & (d.kind == "weight_money")].iloc[0]
w_b = d[(d.sentence == MB) & (d.word == "bank") & (d.kind == "weight_bank")].iloc[0]
v_r, y_b, y_rb = vec(RB, "river", "v"), vec(MB, "bank", "y"), vec(RB, "bank", "y")
w_r = d[(d.sentence == RB) & (d.word == "bank") & (d.kind == "weight_river")].iloc[0].x
COL = {"q": BLUE, "k": ORANGE, "v": GREEN}


def arrow(fig, a, b, color, label, width=3, dash=False):
    if np.allclose(a, b):
        return
    fig.add_annotation(x=b[0], y=b[1], ax=a[0], ay=a[1], xref="x", yref="y", axref="x", ayref="y", showarrow=True,
                       arrowhead=2, arrowsize=1.2, arrowwidth=width, arrowcolor=color, opacity=0.55 if dash else 1)
    if label:
        below = label.startswith("k<") or label.startswith("e<sub>bank")       # keys: label under the tip
        fig.add_annotation(x=b[0], y=b[1], text=label, showarrow=False, xshift=22 if below else -12 if label.startswith("q<sub>m") else 14,
                           yshift=-14 if below else 12,
                           font=dict(color=color, size=19))


def frame(arrows, title, note="", segments=()):
    fig = go.Figure(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(color="black", size=6), showlegend=False))
    for a, b, c in segments:                       # dotted line between two value vectors
        fig.add_trace(go.Scatter(x=[a[0], b[0]], y=[a[1], b[1]], mode="lines", showlegend=False,
                                 line=dict(color=c, width=2, dash="dot")))
    for a in arrows:
        arrow(fig, *a)
    if note:
        fig.add_annotation(x=0.99, y=0.02, xref="paper", yref="paper", text=note, showarrow=False, align="right",
                           xanchor="right", yanchor="bottom", font=dict(size=17), bgcolor="rgba(255,255,255,0.85)")
    fig.update_layout(template="simple_white", width=820, height=700, font=FONT, title=dict(text=title, x=0.5),
                      xaxis=dict(range=[-0.6, 9.2], title="dimension 1", zeroline=True),
                      yaxis=dict(range=[-2.8, 7.8], title="dimension 2", zeroline=True, scaleanchor="x"),
                      margin=dict(l=60, r=20, t=60, b=55))
    return fig


O = np.zeros(2)
lerp = lambda a, b, t: a + (b - a) * t
EMB = [(O, e_m, GREY, "e<sub>money</sub>"), (O, e_b, GREY, "e<sub>bank</sub>")]
frames = []
frames += [frame(EMB, "1. Embeddings of \"money\" and \"bank\"")] * 4
for t in np.linspace(0.15, 1, 6):                                          # 2. projections grow
    arr = [a[:3] + (a[3] if t == 1 else "", 3, True) for a in EMB]
    arr += [(O, lerp(O, P[k][w], t), COL[k], f"{k}<sub>{w}</sub>" if t == 1 else "") for k in "qkv"
            for w in ("money", "bank")]
    frames.append(frame(arr, "2. Each embedding × W<sub>Q</sub>, W<sub>K</sub>, W<sub>V</sub> → query, key, value"))
frames += [frames[-1]] * 3
SC = (f"q<sub>bank</sub>·k<sub>money</sub> = 4.45, ÷√2 = 3.15<br>q<sub>bank</sub>·k<sub>bank</sub> = 5.04, ÷√2 = 3.56"
      f"<br>softmax → weights {w_m.x:.3f} and {w_b.x:.3f}")
frames += [frame([(O, P["q"]["bank"], BLUE, "q<sub>bank</sub>"), (O, P["k"]["money"], ORANGE, "k<sub>money</sub>"),
                  (O, P["k"]["bank"], ORANGE, "k<sub>bank</sub>")], "3. Compare bank's query with every key", SC)] * 6
for t in np.linspace(0, 1, 7):                                             # 4. scale the values by the weights
    sm, sb = lerp(1, w_m.x, t), lerp(1, w_b.x, t)
    frames.append(frame([(O, P["v"]["money"], GREEN, "v<sub>money</sub>", 2, True),
                         (O, P["v"]["bank"], GREEN, "v<sub>bank</sub>", 2, True),
                         (O, sm * P["v"]["money"], RED, f"{sm:.2f} v<sub>money</sub>"),
                         (O, sb * P["v"]["bank"], RED, f"{sb:.2f} v<sub>bank</sub>")],
                        "4. Scale each value vector by its weight"))
frames += [frames[-1]] * 3
a_m, a_b = w_m.x * P["v"]["money"], w_b.x * P["v"]["bank"]
for t in np.linspace(0, 1, 7):                                             # 5. add them tip to tail
    frames.append(frame([(O, P["v"]["money"], GREEN, "v<sub>money</sub>", 2, True),
                         (O, P["v"]["bank"], GREEN, "v<sub>bank</sub>", 2, True),
                         (O, a_b, RED, ""), (lerp(O, a_b, t), lerp(O, a_b, t) + a_m, RED, "")]
                        + ([(O, y_b, PURPLE, "y<sub>bank</sub>", 4)] if t == 1 else []),
                        "5. Add them: y<sub>bank</sub> = 0.397 v<sub>money</sub> + 0.603 v<sub>bank</sub>",
                        segments=[(P["v"]["money"], P["v"]["bank"], PURPLE)] if t == 1 else []))
frames += [frames[-1]] * 5
final = [(O, P["v"]["money"], GREEN, "v<sub>money</sub>", 2, True), (O, P["v"]["bank"], GREEN, "v<sub>bank</sub>", 2, True),
         (O, v_r, GREEN, "v<sub>river</sub>", 2, True), (O, y_b, PURPLE, "y<sub>bank</sub> (money bank)", 4),
         (O, y_rb, BLUE, "y<sub>bank</sub> (river bank)", 4)]
frames += [frame(final, "6. Same word, different context, different output",
                 f"money bank: weight {w_m.x:.2f} on money<br>river bank: weight {w_r:.2f} on river",
                 [(P["v"]["money"], P["v"]["bank"], PURPLE), (v_r, P["v"]["bank"], BLUE)])] * 10

if __name__ == "__main__":
    tmp = HERE / ".attn_frames"
    tmp.mkdir(exist_ok=True)
    for i, f in enumerate(frames):
        f.write_image(tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "attention_2d.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (9, 15, 38, len(frames) - 1)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "attention_2d_frames.png")
    shutil.rmtree(tmp)
    print(len(frames), "frames")
