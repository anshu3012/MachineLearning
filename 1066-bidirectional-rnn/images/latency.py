"""Section 8: latency. Four words of a spoken command arrive one by one. The unidirectional RNN gives each output as
its word arrives; the bidirectional RNN gives no output until the last word, where its backward pass starts.
Run: python latency.py  -> latency.gif, latency_frames.png (the last frame)
Tool: TikZ frames (a still timeline, one page per arriving word) + ffmpeg. Our own design."""
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
STYLE = (HERE / "../../tools/tikz-style.tex").resolve()

TEX = r"""\documentclass[tikz,border=10pt]{standalone}
\input{STYLE}
\begin{document}
\foreach \k in {1,...,5} {
\begin{tikzpicture}[w/.style={box=cblue, inner sep=4pt, minimum height=0.8cm, minimum width=1.5cm, font=\sffamily},
  o/.style={box=##1, inner sep=3pt, minimum height=0.7cm, minimum width=1.2cm, font=\sffamily\small}]
  \useasboundingbox (-3.6,-1.7) rectangle (14.6,4.3);
  \draw[arrow] (-0.9,-0.9) -- (12.6,-0.9) node[right, note] {time};
  \foreach \t/\x [count=\i] in {turn/0, on/2.6, the/5.2, lights/7.8} {
    \ifnum\i>\k \else
      \node[w] (w\i) at (\x,0) {\t};
      \node[note] at (\x,-1.3) {word \i\ arrives};
      \node[o=cblue] (u\i) at (\x,1.6) {$\hat y_\i$};
      \draw[arrow, draw=cblue] (w\i) -- (u\i);
    \fi
  }
  \node[anchor=east, font=\sffamily\bfseries, text=cblue] at (-1.0,1.6) {unidirectional};
  \node[anchor=east, font=\sffamily\bfseries, text=cgreen] at (-1.0,3.4) {bidirectional};
  \node[note, text=cblue, anchor=west] at (-0.7,2.3) {each output as soon as its word arrives};
  \node[note, text=cgreen, anchor=west] at (-0.7,3.85) {no output yet: the backward RNN can start only at the last word};
  \ifnum\k<5
    \draw[cgreen, dashed] (-0.7,3.4) -- ({2.6*(\k-1)+0.8},3.4);
    \node[text=cgreen, font=\sffamily\bfseries, anchor=west] at ({2.6*(\k-1)+0.9},3.4) {waiting \dots};
  \else
    \node[o=cgreen, minimum width=3.6cm] (bo) at (10.8,3.4) {$\hat y_1, \hat y_2, \hat y_3, \hat y_4$};
    \draw[arrow, draw=cgreen, line width=2pt] (w4.east) to[bend right=30] (bo.south);
    \draw[cgreen, dashed] (-0.7,3.4) -- (bo.west);
    \node[note, text=cgreen, anchor=west] at (11.2,2.3) {all at once, after\\the last word (latency)};
  \fi
\end{tikzpicture}
}
\end{document}
"""

if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "f.tex").write_text(TEX.replace("STYLE", str(STYLE)))
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "f.tex"], cwd=tmp, check=True,
                       stdout=subprocess.DEVNULL)
        subprocess.run(["pdftoppm", "-png", "-r", "140", "f.pdf", "p"], cwd=tmp, check=True)
        pngs = sorted(tmp.glob("p-*.png"))
        assert len(pngs) == 5
        n = 0
        for k, p in enumerate(pngs):
            for _ in range(5 if k == 4 else 2):                 # 2 s per word, hold the end 5 s
                shutil.copy(p, tmp / f"{n:03d}.png")
                n += 1
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                        "scale=1000:-2:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                        str(HERE / "latency.gif")], check=True)
        Image.open(pngs[-1]).convert("RGB").save(HERE / "latency_frames.png")
