"""Section 3: a guided tour of the whole transformer on the Note's sentence "turn off the lights" -> "light band karo".
Each frame lights up one block, says what it does in one line, and names the Note that teaches it.
Run: python tour.py  -> tour.gif, tour_frames.png (the last frame: the whole map)
Tool: TikZ frames (a still block diagram lit up block by block) + ffmpeg. Our own sentence and drawing; the idea of
walking one short sentence through every block before any detail is after StatQuest, "Transformer Neural Networks,
ChatGPT's foundation, Clearly Explained!!!" (01:00 onwards)."""
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
STYLE = (HERE / "../../tools/tikz-style.tex").resolve()
CAPTIONS = [
    ("The input sentence", "all four words go in together"),
    ("Embedding", "each word becomes a vector of numbers"),
    ("Positional encoding", "adds each word's position to its vector"),
    ("Self-attention, in several heads", "every word looks at every other word"),
    ("Add and norm", "keeps the original vector and steadies the numbers"),
    ("Feed-forward network", "works on each word's vector separately"),
    ("Masked self-attention", "the decoder looks only at the words written so far"),
    ("Cross-attention", "the decoder looks at the encoder's output"),
    ("Linear layer and softmax", "one probability per word of the vocabulary: pick ``light''"),
    ("Repeat", "the new word goes back in, until the end token"),
]
N = len(CAPTIONS)

TEX = r"""\documentclass[tikz,border=8pt]{standalone}
\input{STYLE}
\tikzset{blk/.style={box=#1, minimum width=4.6cm, minimum height=0.8cm, inner sep=3pt, font=\sffamily},
  tag/.style={font=\sffamily\small\bfseries, text=cgrey, anchor=west},
  flow/.style={arrow, line width=1.2pt}}
% \B{name}{x}{y}{colour}{text}{first frame}{Note tag}{tag anchor x}
\newcommand{\B}[7]{%
  \pgfmathsetmacro{\o}{\k>=#6 ? 1 : 0.15}
  \pgfmathsetmacro{\lw}{\k==#6 ? 2.6 : 1.2}
  \node[blk=#4, opacity=\o, line width=\lw pt] (#1) at (#2,#3) {#5};
  \ifnum\k<#6 \else \node[tag] at ($(#1.east)+(0.1,0)$) {#7}; \fi}
\begin{document}
\foreach \k/\ttl/\sub in {PAGES} {
\begin{tikzpicture}
  \useasboundingbox (-3.4,-2.9) rectangle (14.4,8.2);
  \node[font=\sffamily\bfseries\LARGE] at (5.5,-1.7) {\k. \ttl};
  \node[font=\sffamily\Large, text=cgrey] at (5.5,-2.45) {\sub};
  \node[font=\sffamily\bfseries\large, text=cblue] at (0,7.7) {encoder};
  \node[font=\sffamily\bfseries\large, text=corange] at (8.8,7.7) {decoder};
  % encoder
  \node[font=\sffamily\large] (in) at (0,-0.3) {turn\quad off\quad the\quad lights};
  \B{e1}{0}{1.0}{cblue}{embedding}{2}{Note 1072}
  \B{e2}{0}{2.2}{cblue}{positional encoding}{3}{Note 1078}
  \B{e3}{0}{3.4}{cblue}{multi-head self-attention}{4}{Notes 1072--1077}
  \B{e4}{0}{4.6}{cblue}{add and norm}{5}{Notes 1079, 1080}
  \B{e5}{0}{5.8}{cblue}{feed-forward network}{6}{Note 1080}
  \foreach \a/\b/\s in {in/e1/2, e1/e2/3, e2/e3/4, e3/e4/5, e4/e5/6} {
    \pgfmathsetmacro{\o}{\k>=\s ? 1 : 0.15} \draw[flow, opacity=\o] (\a) -- (\b); }
  % decoder
  \pgfmathsetmacro{\od}{\k>=7 ? 1 : 0.15}
  \node[font=\sffamily\large, opacity=\od] (din) at (8.8,-0.3) {\ifnum\k>9 \texttt{<start>}\quad light \else \texttt{<start>} \fi};
  \B{d1}{8.8}{1.0}{corange}{embedding + positional encoding}{7}{}
  \B{d2}{8.8}{2.2}{corange}{masked self-attention}{7}{Note 1081}
  \B{d3}{8.8}{3.4}{corange}{cross-attention}{8}{Note 1082}
  \B{d4}{8.8}{4.6}{corange}{feed-forward network}{9}{}
  \B{d5}{8.8}{5.8}{corange}{linear layer + softmax}{9}{Note 1083}
  \foreach \a/\b/\s in {din/d1/7, d1/d2/7, d2/d3/8, d3/d4/9, d4/d5/9} {
    \pgfmathsetmacro{\o}{\k>=\s ? 1 : 0.15} \draw[flow, opacity=\o] (\a) -- (\b); }
  % encoder output into cross-attention
  \pgfmathsetmacro{\o}{\k>=8 ? 1 : 0.15}
  \draw[flow, draw=cblue, opacity=\o] (e5.north) -- (0,6.7) -- (5.6,6.7) -- (5.6,3.4) -- (d3.west);
  \ifnum\k>7 \node[font=\sffamily\small, text=cblue, anchor=south] at (2.3,6.7) {encoder output}; \fi
  % output word and the loop
  \ifnum\k>8 \node[font=\sffamily\bfseries\Large, text=cgreen] (out) at (8.8,7.0) {light}; \draw[flow, draw=cgreen] (d5) -- (out); \fi
  \ifnum\k>9 \draw[flow, draw=cgreen, dashed] (out.east) -- (13.7,7.0) -- (13.7,-0.3) -- (din.east);
    \node[tag, text=cgreen, anchor=east] at (13.6,0.3) {Note 1084}; \fi
\end{tikzpicture}
}
\end{document}
"""

if __name__ == "__main__":
    pages = ", ".join(f"{k + 1}/{{{t}}}/{{{s}}}" for k, (t, s) in enumerate(CAPTIONS))
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "f.tex").write_text(TEX.replace("STYLE", str(STYLE)).replace("PAGES", pages))
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "f.tex"], cwd=tmp, check=True,
                       stdout=subprocess.DEVNULL)
        subprocess.run(["pdftoppm", "-png", "-r", "120", "f.pdf", "p"], cwd=tmp, check=True)
        pngs = sorted(tmp.glob("p-*.png"))
        assert len(pngs) == N
        n = 0
        for k, p in enumerate(pngs):
            for _ in range(6 if k == N - 1 else 3):             # 3 s per block, hold the end 6 s
                shutil.copy(p, tmp / f"{n:03d}.png")
                n += 1
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                        "scale=1000:-2:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                        str(HERE / "tour.gif")], check=True)
        Image.open(pngs[-1]).convert("RGB").save(HERE / "tour_frames.png")
        Image.open(pngs[3]).convert("RGB").save("/tmp/tour4.png")
