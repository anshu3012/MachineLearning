"""Section 6: the transformer's multi-head attention built up step by step, with the shapes of every array and a
running count of the weights. The count ends at 1,050,624: the same as one head of 512 (section 6.1).
Run: python shape_count.py  -> shape_count.gif, shape_count_frames.png (the last frame)
Tool: TikZ frames (the block diagram of mha_flow.tex, one stage per page) + ffmpeg. Our own design."""
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
STYLE = (HERE / "../../../../tools/tikz-style.tex").resolve()
d, h = 512, 8
qkv = 3 * h * d * (d // h)                     # W_Q, W_K, W_V of all heads
wo = d * d
bias = 3 * h * (d // h) + d
assert (qkv, qkv + wo, qkv + wo + bias) == (786_432, 1_048_576, 1_050_624)          # section 6.1
STEPS = [
    ("the embeddings: one row of 512 numbers per word", "weights so far: 0"),
    ("8 heads, each with three matrices of 512 $\\times$ 64", f"weights so far: $8 \\times 3 \\times 512 \\times 64$ = {qkv:,}"),
    ("each head runs its own attention: 64 numbers per word", f"weights so far: {qkv:,} (attention itself has none)"),
    ("the 8 outputs side by side: $8 \\times 64 = 512$ numbers per word", f"weights so far: {qkv:,}"),
    ("$W_O$ mixes the heads", f"weights so far: {qkv:,} + $512 \\times 512$ = {qkv + wo:,}"),
    ("the output has the input's shape", f"with {bias:,} biases: {qkv + wo + bias:,}, the same as one head of 512"),
]
N = len(STEPS)

TEX = r"""\documentclass[tikz,border=8pt]{standalone}
\input{STYLE}
\begin{document}
\foreach \k/\ttl/\cnt in {PAGES} {
\begin{tikzpicture}[every node/.append style={font=\sffamily}]
  \useasboundingbox (-1.7,-5.6) rectangle (21.6,4.6);
  \node[font=\sffamily\bfseries\Large] at (9.9,4.0) {\ttl};
  \node[font=\sffamily\Large, text=cred] at (9.9,-4.9) {\cnt};
  \pgfmathsetmacro{\oa}{\k>=2 ? 1 : 0.13} \pgfmathsetmacro{\ob}{\k>=3 ? 1 : 0.13}
  \pgfmathsetmacro{\oc}{\k>=4 ? 1 : 0.13} \pgfmathsetmacro{\od}{\k>=5 ? 1 : 0.13} \pgfmathsetmacro{\oe}{\k>=6 ? 1 : 0.13}
  \node[box=cgrey, text width=2.4cm, minimum height=4.6cm] (x) {$X$\\[3pt]embeddings\\[3pt]\small $n \times 512$};
  \foreach \i/\y/\lab in {1/2.1/1, 2/0.7/2, 8/-2.1/8} {
    \node[box=cblue, text width=4.6cm, opacity=\oa] (h\i) at (5.2,\y) {\textbf{head \lab}: $W_Q^{\lab}, W_K^{\lab}, W_V^{\lab}$\\\small $512 \times 64$ each};
    \node[box=cpurple, text width=2.6cm, right=0.6cm of h\i, opacity=\ob] (a\i) {attention\\\small $Z_{\lab}$: $n \times 64$};
    \draw[arrow, opacity=\oa] (x.east |- h\i) -- (h\i);
    \draw[arrow, opacity=\ob] (h\i) -- (a\i);
  }
  \node[font=\Large, opacity=\oa] at (5.2,-0.7) {$\vdots$};
  \node[font=\Large, opacity=\ob] at ($(a2)!0.5!(a8)$) {$\vdots$};
  \node[box=corange, text width=2.3cm, minimum height=4.6cm, right=0.8cm of a2.east |- x, opacity=\oc] (c) {concatenate\\[3pt]$Z'$\\[3pt]\small $n \times (8 \cdot 64)$\\\small $= n \times 512$};
  \foreach \i in {1,2,8} \draw[arrow, opacity=\oc] (a\i) -- (a\i -| c.west);
  \node[box=cgreen, text width=2.2cm, right=0.7cm of c, opacity=\od] (o) {$\times\, W_O$\\\small $512 \times 512$};
  \node[box=cred, text width=2.0cm, right=0.7cm of o, opacity=\oe] (z) {$Z$\\\small $n \times 512$};
  \draw[arrow, opacity=\od] (c) -- (o);
  \draw[arrow, opacity=\oe] (o) -- (z);
\end{tikzpicture}
}
\end{document}
"""

if __name__ == "__main__":
    pages = ", ".join(f"{k + 1}/{{{t}}}/{{{c}}}" for k, (t, c) in enumerate(STEPS))
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "f.tex").write_text(TEX.replace("STYLE", str(STYLE)).replace("PAGES", pages))
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "f.tex"], cwd=tmp, check=True,
                       stdout=subprocess.DEVNULL)
        subprocess.run(["pdftoppm", "-png", "-r", "110", "f.pdf", "p"], cwd=tmp, check=True)
        pngs = sorted(tmp.glob("p-*.png"))
        assert len(pngs) == N
        n = 0
        for k, p in enumerate(pngs):
            for _ in range(6 if k == N - 1 else 3):             # 3 s per stage, hold the end 6 s
                shutil.copy(p, tmp / f"{n:03d}.png")
                n += 1
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                        "scale=1100:-2:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                        str(HERE / "shape_count.gif")], check=True)
        Image.open(pngs[-1]).convert("RGB").save(HERE / "shape_count_frames.png")
        Image.open(pngs[1]).convert("RGB").save("/tmp/sc2.png")
