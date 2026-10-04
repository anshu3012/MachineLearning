"""Section 5 worked example: the one-node forward pass with its numbers, and the single backward path from L to w_o.
Numbers come from data/worked_example.csv (the Notebook) and are checked against the Note's rounded values.
Run: python wo_path.py  -> wo_path.pdf, wo_path.png (TikZ written from Python so the numbers cannot drift)"""
import shutil
import subprocess
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
v = pd.read_csv(HERE.parent / "data" / "worked_example.csv").set_index("quantity")["value"]
r3 = lambda k: round(float(v[k]), 3)
assert [r3("h_1"), r3("h_2"), r3("h_3"), r3("y_hat"), r3("loss")] == [0.462, 0.354, 0.654, 0.658, 0.419]
assert r3("dL/dz") == -0.342 and r3("dL/dw_o") == -0.224

TEX = r"""\documentclass[tikz,border=8pt]{standalone}
\input{../../../../../tools/tikz-style.tex}
\begin{document}
\begin{tikzpicture}[st/.style={box=cpurple, minimum width=1.7cm}, inp/.style={box=cblue, minimum width=1.3cm}]
  \node[box=cgrey, minimum width=1.3cm] (h0) at (0,0) {$h_0$\\ 0};
  \foreach \t/\x/\h in {1/1/H1, 2/0/H2, 3/1/H3} {
    \node[st] (h\t) at (2.9*\t,0) {$h_\t$\\ \h};
    \node[inp] (x\t) at (2.9*\t,-2.3) {$x_\t = \x$};
    \draw[arrow, draw=cblue] (x\t) -- node[right, text=cblue] {$w_i{=}0.5$} (h\t);
  }
  \foreach \a/\b in {h0/h1, h1/h2, h2/h3} \draw[arrow] (\a) -- node[above, text=cgrey, font=\small] {$w_h{=}0.8$} (\b);
  \node[box=cgreen, minimum width=1.7cm] (y) at (12.3,0) {$\hat{y}$\\ YH};
  \node[box=cred, minimum width=1.7cm] (L) at (15.3,0) {$L$\\ LOSS};
  \draw[arrow, draw=cgreen] (h3) -- node[above, text=cgreen] {$w_o{=}1$} (y);
  \draw[arrow] (y) -- node[above, text=cgrey] {$y{=}1$} (L);
  \draw[line width=3.2pt, opacity=0.6, cred, -{Stealth[length=4mm]}, rounded corners=6pt]
    (L.north) -- ++(0,1.0) -| node[pos=0.25, above, opacity=1, text=cred] {one path: $\hat{y} - y = $ DZ} ([xshift=-0.9cm]y.north west |- y.north);
  \node[box=cred, align=center] at (12.3,-2.6) {$\partial L/\partial w_o = h_3\,(\hat{y} - y)$\\ $= $ H3 $\times$ (DZ) $=$ GO};
\end{tikzpicture}
\end{document}
"""
for k, s in {"H1": "h_1", "H2": "h_2", "H3": "h_3", "YH": "y_hat", "LOSS": "loss", "DZ": "dL/dz", "GO": "dL/dw_o"}.items():
    TEX = TEX.replace(k, f"{r3(s):.3f}")

if __name__ == "__main__":
    gen = HERE / ".gen"
    gen.mkdir(exist_ok=True)
    (gen / "wo_path.tex").write_text(TEX)
    subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "wo_path.tex"], cwd=gen, check=True,
                   stdout=subprocess.DEVNULL)
    shutil.copy(gen / "wo_path.pdf", HERE / "wo_path.pdf")
    subprocess.run(["pdftoppm", "-png", "-r", "200", "-singlefile", str(HERE / "wo_path.pdf"), str(HERE / "wo_path")],
                   check=True)
    shutil.rmtree(gen)
