"""Section 1: the five stages from the encoder-decoder to ChatGPT, appearing one at a time. Each stage is followed
by the problem it left (red), which the next stage fixes.
Run: python timeline.py  -> timeline.gif, timeline_frames.png (the last frame: the whole timeline)
Tool: TikZ frames (a still diagram revealed stage by stage) + ffmpeg. Our own design."""
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
STYLE = (HERE / "../../../../tools/tikz-style.tex").resolve()

TEX = r"""\documentclass[tikz,border=8pt]{standalone}
\input{STYLE}
\tikzset{stage/.style={box=#1, text width=3.3cm, minimum height=2.3cm, font=\sffamily},
  prob/.style={font=\sffamily\small, text=cred, align=center, text width=3.1cm},
cell/.style={circle, draw=#1, fill=#1!20, minimum size=4.5mm, inner sep=0pt, line width=1pt},
           blk/.style={rectangle, draw=#1, fill=#1!20, minimum width=7mm, minimum height=4mm, inner sep=0pt, line width=1pt}}
\begin{document}
\foreach \k in {1,...,9} {
\begin{tikzpicture}
  \useasboundingbox (2.6,-3.6) rectangle (25.6,3.7);
  \foreach \i/\c/\yr/\name/\idea/\who in {
    1/cblue/2014/{Encoder--decoder}/{an LSTM reads the input; a second LSTM writes the output}/{Sutskever et al.},
    2/cpurple/2014--15/{Attention}/{the decoder looks back at every input word}/{Bahdanau et al.},
    3/corange/2017/{Transformer}/{attention only, no RNN: all words in parallel}/{Vaswani et al.},
    4/cgreen/2018/{Transfer learning}/{pre-train a language model, then fine-tune}/{Howard and Ruder},
    5/cred/2018--22/{LLMs and ChatGPT}/{huge transformers; RLHF for dialogue}/{GPT, BERT, InstructGPT}} {
    \pgfmathtruncatemacro{\need}{2*\i-1}
    \ifnum\k<\need \node[stage=\c, opacity=0] (s\i) at (4.7*\i, 0) {\textbf{\yr}\\[2pt]\textbf{\name}\\[3pt]{\small \idea}\\[2pt]{\small\itshape \who}};
    \else \node[stage=\c] (s\i) at (4.7*\i, 0) {\textbf{\yr}\\[2pt]\textbf{\name}\\[3pt]{\small \idea}\\[2pt]{\small\itshape \who}}; \fi
  }
  \foreach \i/\j in {1/2, 2/3, 3/4, 4/5} {\pgfmathtruncatemacro{\need}{2*\j-1} \ifnum\k<\need \else \draw[arrow] (s\i.east) -- (s\j.west); \fi}
  % architecture icons above the stages
  % 1: LSTM chain -> one context vector -> LSTM chain
  \ifnum\k<1 \else \begin{scope}[shift={(4.7,2.45)}]
    \foreach \k in {0,1,2} \node[cell=cblue] (e\k) at (-1.55+0.55*\k, 0) {};
    \node[rectangle, fill=cblue, minimum size=3mm, inner sep=0pt] (c) at (0, 0) {};
    \foreach \k in {0,1,2} \node[cell=corange] (d\k) at (0.45+0.55*\k, 0) {};
    \draw[cgrey, line width=0.8pt, ->] (e0) -- (e1); \draw[cgrey, line width=0.8pt, ->] (e1) -- (e2);
    \draw[cgrey, line width=0.8pt, ->] (e2) -- (c); \draw[cgrey, line width=0.8pt, ->] (c) -- (d0);
    \draw[cgrey, line width=0.8pt, ->] (d0) -- (d1); \draw[cgrey, line width=0.8pt, ->] (d1) -- (d2);
  \end{scope} \fi
  % 2: every encoder state feeds the decoder step
  \ifnum\k<3 \else \begin{scope}[shift={(9.4,2.45)}]
    \foreach \k in {0,1,2} \node[cell=cblue] (a\k) at (-1.1+0.55*\k, -0.25) {};
    \node[cell=corange] (b) at (1.0, 0.3) {};
    \draw[cpurple, line width=2pt] (a0) -- (b); \draw[cpurple, line width=0.6pt] (a1) -- (b); \draw[cpurple, line width=1.2pt] (a2) -- (b);
  \end{scope} \fi
  % 3: all words attend to all words at once
  \ifnum\k<5 \else \begin{scope}[shift={(14.1,2.45)}]
    \foreach \k in {0,1,2,3} {\node[blk=corange] (t\k) at (-1.2+0.8*\k, -0.3) {}; \node[blk=corange] (u\k) at (-1.2+0.8*\k, 0.4) {};}
    \foreach \k in {0,1,2,3} \foreach \m in {0,1,2,3} \draw[corange, line width=0.4pt] (t\k.north) -- (u\m.south);
  \end{scope} \fi
  % 4: big pre-training block, then a small fine-tuning step
  \ifnum\k<7 \else \begin{scope}[shift={(18.8,2.45)}]
    \node[rectangle, draw=cgreen, fill=cgreen!20, minimum width=1.5cm, minimum height=0.8cm, font=\sffamily\scriptsize, align=center] (pt) at (-0.6, 0) {pre-train\\lots of text};
    \node[rectangle, draw=cgreen, fill=cgreen!45, minimum width=0.8cm, minimum height=0.5cm, font=\sffamily\scriptsize] (ft) at (1.0, 0) {tune};
    \draw[arrow, line width=1pt] (pt) -- (ft);
  \end{scope} \fi
  % 5: a tall stack of transformer blocks and a chat bubble
  \ifnum\k<9 \else \begin{scope}[shift={(23.5,2.75)}]
    \foreach \k in {0,...,5} \node[blk=cred, minimum width=11mm, minimum height=1.6mm] at (-0.5, -0.45+0.18*\k) {};
    \node[draw=cred, fill=white, rounded corners=3pt, font=\sffamily\scriptsize, inner sep=2pt] (q) at (0.85, 0.15) {Hi!};
    \draw[cred, line width=0.8pt] (q.south west) -- ++(-0.2,-0.2);
  \end{scope} \fi

  \foreach \x/\txt [count=\i] in {7.05/{one context vector forgets long sentences}, 11.75/{still one word at a time: slow to train}, 16.45/{training from scratch needs huge data}, 21.15/{still an LSTM, not yet a transformer}}
    {\pgfmathtruncatemacro{\need}{2*\i} \ifnum\k<\need \else \node[prob, anchor=north] at (\x, -1.75) {\txt}; \fi}
  \node[note] at (14.1, -3.25) {red: the problem each stage left, which the next stage fixed};
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
        subprocess.run(["pdftoppm", "-png", "-r", "110", "f.pdf", "p"], cwd=tmp, check=True)
        pngs = sorted(tmp.glob("p-*.png"))
        assert len(pngs) == 9
        n = 0
        for k, p in enumerate(pngs):
            for _ in range(6 if k == 8 else 2):                 # 2 s per step, hold the end 6 s
                shutil.copy(p, tmp / f"{n:03d}.png")
                n += 1
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                        "scale=1200:-2:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                        str(HERE / "timeline.gif")], check=True)
        Image.open(pngs[-1]).convert("RGB").save(HERE / "timeline_frames.png")
