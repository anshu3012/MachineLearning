"""Animation: one trip round the speed loop's block diagram, one stage per frame, with the closed-loop ramp run's
numbers (no sensor noise in this run). Cycle at t = 4.00 s, the first on the ramp: the sensor reads 0.500 m/s, the error
is 0, the controller asks for 1 N, the motors push 1 N, the ramp pulls 0.785 N back, so the speed falls by 0.00098 m/s
in 10 ms. The next cycle starts from the lower reading; then the loop 50 cycles later (t = 4.50 s) and settled
(t = 10.00 s: error 0.0357 m/s, force 1.713 N, net force 0). Frames are TikZ, drawn like block_diagram.tex.
Run -> loop_anim.gif, loop_anim_frames.png"""
import shutil
import subprocess
import sys
from pathlib import Path

import speedkit as s
from gifkit import gif_from_pngs

here = Path(__file__).resolve().parent
style = next(p / "tools" / "tikz-style.tex" for p in here.parents if (p / "tools" / "tikz-style.tex").exists())
CL = s.run(30, closed=True)


def at(t):
    k = int(round(t / s.DT))
    v, ym, e, u, d, b = (float(CL[n][k]) for n in ("v", "y_m", "e", "u", "d", "b"))
    net = u - b * v - d
    return dict(t=t, v=v, ym=ym, e=e, u=u, d=d, drag=b * v, net=net, dv=net * s.DT / s.M, vnext=float(CL["v"][k + 1]))


A, B2, C, D = at(4.00), at(4.01), at(4.50), at(10.00)
assert A["e"] == 0 and A["u"] == 1.0 and abs(A["d"] - 0.7848) < 1e-12
assert abs(A["dv"] + 0.000981) < 1e-6 and abs(B2["ym"] - A["vnext"]) < 1e-12
assert abs(D["net"]) < 1e-6 and round(D["e"], 4) == 0.0357 and round(D["u"], 3) == 1.713
# the arithmetic printed in the frames must come out of the printed numbers
assert f"{1 + 20 * float(f'{C['e']:.6f}'):.4f}" == f"{C['u']:.4f}"
assert f"{1 + 20 * float(f'{D['e']:.6f}'):.4f}" == f"{D['u']:.4f}"

ON = "draw=black, line width=3pt, -{Stealth[length=4.5mm]}"
OFF = "arrow"
TEMPLATE = r"""\documentclass[tikz,border=8pt]{standalone}
\input{STYLE}
\begin{document}
\begin{tikzpicture}[every node/.append style={font=\large},
    sum/.style={circle, draw=cgrey, fill=white, minimum size=0.95cm, inner sep=0pt, line width=1.4pt},
    sumon/.style={circle, draw=black, fill=cred!15, minimum size=0.95cm, inner sep=0pt, line width=3pt},
    val/.style={font=\normalsize, text=cgrey, align=center},
    valon/.style={font=\normalsize\bfseries, text=black, align=center}]
  \node[@S1] (s1) at (2.6,0) {};
  \node[box=cblue, text width=3.3cm, @CTRL] (ctrl) at (7.4,0) {\textbf{controller}\\ computer\\[2pt] $u = 1 + 20\,e$};
  \node[box=corange, text width=3.0cm, @ACT] (act) at (13.2,0) {\textbf{actuator}\\ motors\\[2pt] at most 4 N};
  \node[@S2] (s2) at (17.6,0) {};
  \node[box=cpurple, text width=3.6cm, @PLANT] (plant) at (21.2,0) {\textbf{plant}\\ robot, 8 kg\\[2pt] drag 2 N per m/s};
  \node[box=cgreen, text width=3.3cm, @SENS] (sens) at (21.2,-4.4) {\textbf{sensor}\\ wheel encoders};
  \node[sum] (s3) at (13.2,-4.4) {};
  \draw[@AREF] (-1.0,0) -- node[above] {reference $r$} node[below, @VREF] {VREF} (s1.west);
  \node[font=\Large] at ($(s1.north west)+(-0.12,0.22)$) {$+$};
  \node[font=\Large] at ($(s1.south west)+(-0.14,-0.25)$) {$-$};
  \draw[@AERR] (s1.east) -- node[above] {error $e$} node[below, @VERR] {VERR} (ctrl.west);
  \draw[@AU] (ctrl.east) -- node[above] {$u$} node[below, @VU] {VU} (act.west);
  \draw[@AF] (act.east) -- node[above] {force} node[below, @VF] {VF} (s2.west);
  \node[font=\Large] at ($(s2.south west)+(-0.12,-0.22)$) {$+$};
  \node[font=\Large] at ($(s2.north east)+(0.18,0.22)$) {$-$};
  \draw[@AD] (17.6,2.7) node[above, align=center] {\textbf{disturbance} $d$\\[-1pt] \normalsize\textcolor{cgrey}{ramp's pull 0.785 N}}
     -- (s2.north);
  \draw[@AP] (s2.east) -- (plant.west);
  \draw[@AY] (plant.east) -- node[pos=0.3, above] {output $y$} node[pos=0.3, below, @VY] {VY} (27.0,0);
  \draw[@AFB] (25.6,0) -- (25.6,-4.4) -- (sens.east);
  \draw[@AFB] (sens.west) -- (s3.east);
  \node[font=\Large] at ($(s3.north east)+(0.14,0.22)$) {$+$};
  \node[font=\Large] at ($(s3.south east)+(0.2,-0.22)$) {$+$};
  \draw[arrow] (13.2,-7.0) node[below, align=center] {\textbf{sensor noise} $n$\\[-1pt] \normalsize\textcolor{cgrey}{0 in this run}}
     -- (s3.south);
  \draw[@AM] (s3.west) -- node[above] {measured $y_m$} node[below, @VM] {VM} (2.6,-4.4) -- (s1.south);
  \useasboundingbox (-1.3,4.3) rectangle (27.3,-12.4);
  \node[font=\Large\bfseries, anchor=west] at (-1.0,3.6) {CLOCK};
  \node[draw=cgrey, rounded corners=4pt, fill=white, text width=27.2cm, align=left, inner sep=10pt, anchor=north west,
        font=\Large] at (-1.0,-9.2) {CAPTION};
\end{tikzpicture}
\end{document}
"""
ELEMENTS = {"S1": ("sum", "sumon"), "S2": ("sum", "sumon"), "CTRL": ("", "line width=3pt, draw=black"),
            "ACT": ("", "line width=3pt, draw=black"), "PLANT": ("", "line width=3pt, draw=black"),
            "SENS": ("", "line width=3pt, draw=black")}
ARROWS = ["AREF", "AERR", "AU", "AF", "AD", "AP", "AY", "AFB", "AM"]
VALUES = ["VREF", "VERR", "VU", "VF", "VY", "VM"]


def tex(lit, vals, clock, caption):
    """lit: names drawn thick; vals: value text per V-name (shown bold when the matching arrow is lit)."""
    src = TEMPLATE.replace("STYLE", str(style))
    for name, (off, on) in ELEMENTS.items():
        src = src.replace(f"@{name}", on if name in lit else off)
    for name in ARROWS:
        src = src.replace(f"[@{name}]", f"[{ON}]" if name in lit else f"[{OFF}]")
    for name in VALUES:
        src = src.replace(f"@{name}", "valon" if name in lit else "val")
        src = src.replace("{" + name + "}", "{" + vals.get(name, "") + "}")
    return src.replace("CLOCK", clock).replace("CAPTION", caption).replace(", ]", "]")


def f4(x):
    return f"{x:.4f}"


def cycle_vals(c, upto):
    """Value labels of a cycle, shown only for the stages reached so far."""
    full = {"VREF": "0.5 m/s", "VM": f"{c['ym']:.6f} m/s", "VERR": f"{c['e']:.6f}\\\\ m/s",
            "VU": f"{f4(c['u'])}\\\\ N", "VF": f"{f4(c['u'])}\\\\ N", "VY": f"{c['vnext']:.5f}\\\\ m/s"}
    order = ["VREF", "VM", "VERR", "VU", "VF", "VY"]
    return {k: full[k] for k in order[:upto]}


frames = []
a = A
clock = r"cycle at $t = 4.00$ s: the robot has just reached the ramp"
frames.append(([], {}, clock, "Every 10 ms the computer runs once round this loop. Follow one cycle, stage by stage."))
frames.append((["AREF", "VREF"], cycle_vals(a, 1), clock,
               r"1. \textbf{Reference.} The plan asks for $r = 0.5$ m/s."))
frames.append((["SENS", "AFB", "AM", "VM"], cycle_vals(a, 2), clock,
               rf"2. \textbf{{Sensor.}} The wheel encoders measure the speed: $y_m = {a['ym']:.3f}$ m/s."))
frames.append((["S1", "AERR", "VERR"], cycle_vals(a, 3), clock,
               rf"3. \textbf{{Summing junction.}} Error $e = r - y_m = 0.5 - {a['ym']:.3f} = {a['e']:.3f}$ m/s: "
               r"not too slow yet."))
frames.append((["CTRL", "AU", "VU"], cycle_vals(a, 4), clock,
               rf"4. \textbf{{Controller.}} $u = 1 + 20 \times {a['e']:.3f} = {a['u']:.3f}$ N, the flat-floor force."))
frames.append((["ACT", "AF", "VF"], cycle_vals(a, 5), clock,
               rf"5. \textbf{{Actuator.}} The motors push {a['u']:.3f} N (they can give up to 4 N)."))
frames.append((["S2", "AD", "AP", "PLANT", "AY", "VY"], cycle_vals(a, 6), clock,
               rf"6. \textbf{{Plant.}} Net force $= 1.000 - 1.000 - 0.785 = {a['net']:.3f}$ N (push $-$ drag $-$ "
               rf"ramp), so in 10 ms the speed changes by ${a['net']:.3f} \times 0.01 / 8 = {a['dv']:.5f}$ m/s, "
               rf"to {a['vnext']:.5f} m/s."))
frames.append((["AY", "AFB", "SENS"], cycle_vals(a, 6), clock,
               r"7. \textbf{Back round.} The new speed goes back to the sensor: the next cycle starts from it."))
b = B2
frames.append((ARROWS + VALUES + ["S1", "S2", "CTRL", "ACT", "PLANT", "SENS"], cycle_vals(b, 6),
               r"next cycle, $t = 4.01$ s",
               rf"Now $y_m = {b['ym']:.6f}$, so $e = {b['e']:.6f}$ m/s and $u = 1 + 20 \times {b['e']:.6f} = "
               rf"{f4(b['u'])}$ N: the correction has started."))
c = C
frames.append((ARROWS + VALUES + ["S1", "S2", "CTRL", "ACT", "PLANT", "SENS"], cycle_vals(c, 6),
               r"50 cycles later, $t = 4.50$ s",
               rf"$e = {c['e']:.6f}$ m/s, $u = 1 + 20 \times {c['e']:.6f} = {f4(c['u'])}$ N; drag "
               rf"{c['drag']:.4f} N and ramp 0.7848 N leave a net force of {c['net']:.4f} N: still slowing, more gently."))
d = D
frames.append((ARROWS + VALUES + ["S1", "S2", "CTRL", "ACT", "PLANT", "SENS"], cycle_vals(d, 6),
               r"settled, $t = 10.00$ s",
               rf"$e = {d['e']:.6f}$ m/s, $u = 1 + 20 \times {d['e']:.6f} = {f4(d['u'])}$ N $=$ drag "
               rf"{d['drag']:.4f} N $+$ ramp 0.7848 N. The net force is 0, so the speed stays at {d['vnext']:.4f} m/s."))

PDFTOPPM = str(Path(sys.executable).parent / "pdftoppm") if (Path(sys.executable).parent / "pdftoppm").exists() \
    else "pdftoppm"
tmp = here / ".loop_anim_tex"
tmp.mkdir(exist_ok=True)
pngs = []
for i, (lit, vals, clock, cap) in enumerate(frames):
    f = tmp / f"loop{i:02d}.tex"
    f.write_text(tex(lit, vals, clock, cap))
    subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f.name], cwd=tmp, check=True,
                   stdout=subprocess.DEVNULL)
    subprocess.run([PDFTOPPM, "-png", "-r", "110", "-singlefile", f.with_suffix(".pdf").name, f.stem], cwd=tmp,
                   check=True)
    pngs.append(tmp / f"{f.stem}.png")
gif_from_pngs(pngs, here / "loop_anim", fps=1, holds=[4] + [5] * 7 + [5, 6, 12], keys=[1, 3, 6, len(pngs) - 1],
              cols=2, width=1000)
shutil.rmtree(tmp)
