"""Figure 6: the speed loop's cycles on the ramp. The block diagram of loop_cycle.tex (Figure 5) with each signal's value
updated, one frame every 5 cycles (0.05 s) from t = 4.00 to 6.00 s, then the settled loop at t = 10.00 s, held. Under
the diagram, the same closed-loop ramp run (speedkit.py, no sensor noise): the speed against time, and the push u
against the force that holding the current speed requires, drag b v plus the ramp's pull d. Their gap, the shortfall,
is the net force that slows the robot; it shrinks to 0 as the speed settles at 0.464 m/s. Frames are TikZ (pgfplots).
The notebook prints every value through cycle(). Run -> loop_cycles.gif, loop_cycles_frames.png"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

import speedkit as s

here = Path(__file__).resolve().parent
CL = s.run(30, closed=True)
STEP = 5                                                         # cycles per frame: 0.05 s
TIMES = [round(4 + STEP * s.DT * i, 2) for i in range(41)] + [10.0]


def cycle(t):
    """The cycle at time t as Figure 6 prints it, rounded to 4 decimals; the needed force, the shortfall and the net
    force are worked out from the rounded parts, so every printed sum adds up."""
    k = int(round(t / s.DT))
    v, e, u = (float(CL[n][k]) for n in ("v", "e", "u"))
    c = dict(t=t, ym=round(v, 4), e=round(e, 4), u=round(u, 4), drag=round(s.B * v, 4), ramp=round(s.D_RAMP, 4),
             vnext=round(float(CL["v"][k + 1]), 4))
    c["need"] = round(c["drag"] + c["ramp"], 4)
    c["short"] = round(c["need"] - c["u"], 4) + 0.0                # + 0.0 turns -0.0 into 0.0
    true_short = s.B * v + s.D_RAMP - u
    assert abs(c["short"] - true_short) < 2e-4 and round(c["ym"] + c["e"], 4) == s.V_REF
    return c


# Figure 5's values (typed into loop_cycle.tex) are this run's first cycle on the ramp
first = cycle(4.00)
assert (first["ym"], first["e"], first["u"], first["drag"], first["short"]) == (0.5, 0.0, 1.0, 1.0, 0.7848)
assert f"{CL['v'][401]:.5f}" == "0.49902" and "0.49902 m/s" in (here / "loop_cycle.tex").read_text()
end = cycle(10.00)
assert (end["e"], end["u"], end["drag"], end["need"], end["short"], end["ym"]) == (0.0357, 1.7135, 0.9287, 1.7135, 0, 0.4643)


def num(x):
    """A value for TeX: a true minus sign, and a plain 0 for zero."""
    return "0" if x == 0 else f"${x:.4f}$"


def pts(xs, ys):
    return " ".join(f"({x:.2f},{y:.5f})" for x, y in zip(xs, ys))


def frame_tex(c, settled):
    k0, k = int(round(3.5 / s.DT)), int(round(c["t"] / s.DT))
    t, v, u = CL["t"][k0:k + 1], CL["v"][k0:k + 1], CL["u"][k0:k + 1]
    need = s.B * v + CL["d"][k0:k + 1]
    r0 = int(round(4.0 / s.DT)) - k0                                # first sample on the ramp
    gap = pts(list(t[r0:]) + list(t[r0:][::-1]), list(u[r0:]) + list(need[r0:][::-1]))
    title = (r"settled, $t = 10.00$ s {\mdseries\color{cgrey}\quad (the previous frame is $t = 6.00$ s)}" if settled
             else rf"$t = {c['t']:.2f}$ s {{\mdseries\color{{cgrey}}\quad one frame every 5 cycles (0.05 s)}}")
    readout = (rf"push $u$ = {c['u']:.4f} N, \quad needed = drag {c['drag']:.4f} N $+$ ramp {c['ramp']:.4f} N "
               rf"= {c['need']:.4f} N, \quad shortfall {num(c['short'])} N")
    vals = {"vTitle": title, "vM": f"{c['ym']:.4f} m/s", "vE": f"{c['e']:.4f}\\\\ m/s", "vU": f"{c['u']:.4f}\\\\ N",
            "vF": f"{c['u']:.4f}\\\\ N", "vPlant": f"drag {c['drag']:.4f} N\\\\ net force {num(-c['short'])} N",
            "vY": f"new speed\\\\ {c['vnext']:.4f} m/s"}
    plots = rf"""
  \pgfplotsset{{every axis/.append style={{scale only axis, width=26.6cm, height=5.6cm, xmin=3.5, xmax=10.2,
      xtick={{4,5,6,7,8,9,10}}, axis lines=left, tick label style={{font=\LARGE}}, label style={{font=\LARGE}},
      title style={{font=\LARGE, align=center}}, clip=false}}}}
  \begin{{axis}}[at={{(1.4cm,-10.2cm)}}, anchor=north west, ymin=0.45, ymax=0.51, ytick={{0.45,0.46,0.47,0.48,0.49,0.5,0.51}},
      yticklabel style={{/pgf/number format/fixed, /pgf/number format/precision=2}}, ylabel={{speed (m/s)}},
      title={{\textbf{{speed of the robot}}}}]
    \addplot[cgrey, dashed, line width=2pt] coordinates {{(3.5,0.5) (10.2,0.5)}};
    \node[anchor=south east, text=cgrey, font=\LARGE] at (axis cs:10.15,0.5) {{wanted 0.5 m/s}};
    \addplot[cblue, densely dotted, line width=2pt] coordinates {{(3.5,{s.steady_closed(d=s.D_RAMP):.4f}) (10.2,{s.steady_closed(d=s.D_RAMP):.4f})}};
    \node[anchor=north east, text=cblue, font=\LARGE] at (axis cs:9.7,0.4643) {{settles at 0.464 m/s}};
    \draw[cgrey, dashed, line width=1.4pt] (axis cs:4,0.45) -- (axis cs:4,0.51);
    \node[anchor=south west, text=cgrey, font=\LARGE] at (axis cs:4.03,0.451) {{the ramp starts, $t = 4.00$ s}};
    \addplot[cblue, line width=3pt] coordinates {{{pts(t, v)}}};
    \addplot[only marks, mark=*, mark size=7pt, cblue] coordinates {{({c['t']:.2f},{CL['v'][k]:.5f})}};
  \end{{axis}}
  \begin{{axis}}[at={{(1.4cm,-19.4cm)}}, anchor=north west, ymin=0.9, ymax=1.9, ytick={{1.0,1.2,1.4,1.6,1.8}},
      yticklabel style={{/pgf/number format/fixed, /pgf/number format/precision=1, /pgf/number format/fixed zerofill}},
      xlabel={{time (s)}}, ylabel={{force (N)}}, title={{{readout}}},
      legend cell align=left, legend style={{at={{(0.99,0.04)}}, anchor=south east, nodes={{font=\LARGE}}, draw=none,
      fill=white, row sep=3pt}}]
    \addplot[fill=cred!22, draw=cred!22, area legend] coordinates {{{gap}}};
    \addlegendentry{{shortfall = needed $-$ push: it slows the robot}}
    \addplot[cred, line width=3pt] coordinates {{{pts(t, need)}}};
    \addlegendentry{{needed to hold the speed: drag $+$ ramp's pull}}
    \addplot[cblue, line width=3pt] coordinates {{{pts(t, u)}}};
    \addlegendentry{{push $u$ from the controller}}
    \addplot[only marks, mark=*, mark size=7pt, cred, forget plot] coordinates {{({c['t']:.2f},{need[-1]:.5f})}};
    \addplot[only marks, mark=*, mark size=7pt, cblue, forget plot] coordinates {{({c['t']:.2f},{u[-1]:.5f})}};
  \end{{axis}}
  \useasboundingbox (-1.3,4.5) rectangle (28.7,-27.3);"""
    src = (here / "loop_cycle.tex").read_text()
    style = next(p / "tools" / "tikz-style.tex" for p in here.parents if (p / "tools" / "tikz-style.tex").exists())
    src = src.replace("../../../../../tools/tikz-style.tex", str(style))
    src = src.replace(r"\begin{document}", "\\usepackage{pgfplots}\n\\pgfplotsset{compat=1.18}\n\\begin{document}")
    src = src.replace(r"\stagestrue", r"\stagesfalse").replace("% FRAME", plots)
    for name, val in vals.items():
        src, n = re.subn(rf"\\newcommand{{\\{name}}}{{.*}}\n", lambda m: f"\\newcommand{{\\{name}}}{{{val}}}\n", src)
        assert n == 1, name
    return src


if __name__ == "__main__":
    from gifkit import gif_from_pngs

    pdftoppm = Path(sys.executable).parent / "pdftoppm"
    tmp = here / ".loop_cycles_tex"
    tmp.mkdir(exist_ok=True)
    pngs = []
    for i, t in enumerate(TIMES):
        f = tmp / f"cyc{i:02d}.tex"
        f.write_text(frame_tex(cycle(t), settled=t == 10.0))
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f.name], cwd=tmp, check=True,
                       stdout=subprocess.DEVNULL)
        subprocess.run([str(pdftoppm) if pdftoppm.exists() else "pdftoppm", "-png", "-r", "100", "-singlefile",
                        f.with_suffix(".pdf").name, f.stem], cwd=tmp, check=True)
        pngs.append(tmp / f"{f.stem}.png")
    keys = [TIMES.index(x) for x in (4.0, 4.25, 5.0, 10.0)]
    gif_from_pngs(pngs, here / "loop_cycles", fps=5, holds=[10] + [1] * (len(pngs) - 2) + [30], keys=keys, cols=2,
                  width=1000)
    shutil.rmtree(tmp)
