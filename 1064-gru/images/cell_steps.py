"""Section 8: the four steps of one GRU time step, lit up in order on the cell of Figure 1, with the numbers of
sentence 4 of the story written on each wire. Same numbers as gru_step.py and the Notebook.
Run: python cell_steps.py  -> cell_steps.gif, cell_steps_frames.png
Tool: TikZ frames (the same still diagram as gru_cell.tex, one page per step) + ffmpeg. Our own design."""
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).parent
h_prev, r = np.array([0.6, 0.6, 0.7, 0.1]), np.array([0.8, 0.2, 0.1, 0.9])
h_cand, z = np.array([0.7, 0.2, 0.1, 0.2]), np.array([0.1, 0.7, 0.8, 0.2])
old, new = (1 - z) * h_prev, z * h_cand
h = old + new
assert np.allclose(np.round(h, 2), [0.61, 0.32, 0.22, 0.12])                    # section 8.4
v = lambda a: "[" + ",\\ ".join(f"{x:.2f}".rstrip("0").rstrip(".") for x in a) + "]"

TITLES = ["Step 1: the reset gate $r_t$", "Step 2: the candidate $\\tilde h_t$",
          "Step 3: the update gate $z_t$", "Step 4: the new hidden state $h_t$"]
SUBS = ["how much of each entry of the old memory to use", "a tanh layer on the reset memory and the input",
        "how much of the candidate to take in", "share $1 - z$ of the old memory plus share $z$ of the candidate"]

TEX = r"""\documentclass[tikz,border=8pt]{standalone}
\input{%(style)s}
\begin{document}
\foreach \k/\ttl/\sub in {%(pages)s} {
\begin{tikzpicture}[x=1.7cm, y=1.35cm,
  layer/.style={draw=##1, fill=##1!15, rounded corners=3pt, minimum width=1.15cm, minimum height=0.75cm, font=\sffamily},
  op/.style={circle, draw=cgrey, fill=white, minimum size=0.62cm, inner sep=0pt, font=\sffamily\large},
  line/.style={-{Stealth[length=2.6mm]}, line width=1.3pt},
  num/.style={font=\sffamily\normalsize, fill=white, inner sep=1.5pt, text=##1}]
  \useasboundingbox (-1.9,-2.3) rectangle (13.4,6.6);
  \pgfmathsetmacro{\oa}{\k>=1 ? 1 : 0.16} \pgfmathsetmacro{\ob}{\k>=2 ? 1 : 0.16}
  \pgfmathsetmacro{\oc}{\k>=3 ? 1 : 0.16} \pgfmathsetmacro{\od}{\k>=4 ? 1 : 0.16}
  \node[font=\sffamily\bfseries\LARGE] at (5.75,6.25) {\ttl};
  \node[font=\sffamily\large, text=cgrey] at (5.75,5.65) {\sub};
  % always on: the old memory, the input and the bus [h_{t-1}, x_t]
  \draw[line width=1.3pt, draw=cred] (-0.6,4.2) node[left, text=cred] {$h_{t-1}$} -- (0.3,4.2) -- (0.3,-0.6);
  \node[num=cred, anchor=south west] at (-1.75,4.4) {$%(hprev)s$};
  \draw[line width=1.3pt, draw=cblue] (0.3,-1.6) node[below, text=cblue] {$x_t$ (sentence 4)} -- (0.3,-0.6);
  \draw[line width=1.3pt, draw=cgrey] (0.3,-0.6) -- (4.6,-0.6);
  \node[note, anchor=north] at (2.5,-0.65) {$[h_{t-1}, x_t]$};
  % step 1: reset gate
  \begin{scope}[opacity=\oa]
    \node[layer=cpurple] (r) at (1.9,1.3) {$\sigma$};
    \draw[line, draw=cgrey] (1.9,-0.6) -- (r);
    \node[font=\sffamily\bfseries, text=cpurple] at (1.9,0.45) {reset gate};
    \draw[line width=1.3pt, draw=cpurple] (r) -- (1.9,2.1);
    \ifnum\k>0 \node[num=cpurple, anchor=south] at (1.9,2.2) {$r_t = %(r)s$}; \fi
  \end{scope}
  % step 2: candidate
  \begin{scope}[opacity=\ob]
    \node[op] (rx) at (3.3,2.1) {$\times$};
    \draw[line, draw=cred] (0.3,4.2) -- (3.3,4.2) -- (rx);
    \draw[line, draw=cpurple] (1.9,2.1) -- (rx);
    \node[layer=cblue] (c) at (8.0,1.3) {tanh};
    \draw[line, draw=cpurple] (rx) -| (7.75,1.68);
    \draw[line width=1.3pt, draw=cblue] (0.3,-1.2) -- (8.0,-1.2);
    \draw[line, draw=cblue] (8.0,-1.2) -- (c);
    \node[font=\sffamily\bfseries, text=cblue] at (8.0,0.45) {candidate};
    \ifnum\k>1 \node[num=cpurple, anchor=west] at (5.1,1.75) {$r_t \odot h_{t-1}$};
      \node[num=cpurple, anchor=west] at (5.1,1.35) {$= %(rh)s$};
      \node[num=cblue, anchor=west] at (8.55,0.9) {$\tilde h_t = %(cand)s$}; \fi
  \end{scope}
  % step 3: update gate
  \begin{scope}[opacity=\oc]
    \node[layer=corange] (z) at (4.6,1.3) {$\sigma$};
    \draw[line, draw=cgrey] (4.6,-0.6) -- (z);
    \node[font=\sffamily\bfseries, text=corange] at (4.6,0.45) {update gate};
    \node[layer=corange, minimum width=0.8cm, minimum height=0.55cm] (om) at (4.6,3.45) {$1-$};
    \draw[line, draw=corange] (z) -- (4.6,2.85) -- (om);
    \ifnum\k>2 \node[num=corange, anchor=west] at (5.0,2.6) {$z_t = %(z)s$};
      \node[num=corange, anchor=west] at (5.0,3.45) {$1 - z_t = %(omz)s$}; \fi
  \end{scope}
  % step 4: balance old memory and candidate
  \begin{scope}[opacity=\od]
    \node[op] (keep) at (4.6,4.2) {$\times$};
    \node[op] (plus) at (10.6,4.2) {$+$};
    \node[op] (zx) at (10.6,2.85) {$\times$};
    \draw[line, draw=cred] (3.3,4.2) -- (keep);
    \draw[line, draw=corange] (4.6,3.67) -- (keep);
    \draw[line, draw=cred] (keep) -- (plus);
    \draw[line, draw=corange] (4.6,2.85) -- (zx);
    \draw[line, draw=cblue] (8.55,1.3) -| (zx);
    \draw[line, draw=corange] (zx) -- (plus);
    \draw[line, draw=cred] (plus) -- (12.2,4.2) node[right, text=cred] {$h_t$};
    \ifnum\k>3 \node[num=cred, anchor=south] at (7.6,4.3) {$(1 - z_t) \odot h_{t-1} = %(old)s$};
      \node[num=cblue, anchor=west] at (10.8,3.55) {$z_t \odot \tilde h_t$};
      \node[num=cblue, anchor=west] at (10.8,3.15) {$= %(new)s$};
      \node[num=cred, anchor=south, font=\sffamily\bfseries] at (11.4,4.75) {$h_t = %(h)s$}; \fi
  \end{scope}
\end{tikzpicture}
}
\end{document}
"""


def tikz_gif(tex, name, pages, seconds=3, hold=6, width=1000):
    """Compile a multi-page TikZ file; pages -> name.gif (each page shown `seconds`) and name_frames.png (the last page)."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "f.tex").write_text(tex)
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "f.tex"], cwd=tmp, check=True,
                       stdout=subprocess.DEVNULL)
        subprocess.run(["pdftoppm", "-png", "-r", "130", "f.pdf", "p"], cwd=tmp, check=True)
        pngs = sorted(tmp.glob("p-*.png"))
        assert len(pngs) == pages, (len(pngs), pages)
        n = 0
        for k, p in enumerate(pngs):
            for _ in range(hold if k == pages - 1 else seconds):
                shutil.copy(p, tmp / f"{n:03d}.png")
                n += 1
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                        f"scale={width}:-2:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                        str(HERE / f"{name}.gif")], check=True)
        # the last page shows every step and every number, so it alone is the PDF figure
        Image.open(pngs[-1]).convert("RGB").save(HERE / f"{name}_frames.png")


if __name__ == "__main__":
    pages = ", ".join(f"{k + 1}/{{{t}}}/{{{s}}}" for k, (t, s) in enumerate(zip(TITLES, SUBS)))
    tex = TEX
    for key, val in dict(style=(HERE / "../../tools/tikz-style.tex").resolve(), pages=pages, hprev=v(h_prev), r=v(r),
                         rh=v(r * h_prev), cand=v(h_cand), z=v(z), omz=v(1 - z), old=v(old), new=v(new),
                         h=v(h)).items():
        tex = tex.replace(f"%({key})s", str(val))
    tikz_gif(tex, "cell_steps", pages=4)
