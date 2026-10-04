"""Local linearity (idea: Sanderson's Khan Academy lessons on the Jacobian; our own code and example).
Polar coordinates f(r, theta) = (r cos theta, r sin theta) bend a straight (r, theta) grid into rays and arcs.
Then we zoom on the cell at (r, theta) = (2, pi/6): as the cell shrinks (magnified to a fixed screen size),
its curved image (orange) becomes the parallelogram spanned by J times the cell's sides (green).
Run: python local_linear.py  -> local_linear.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
R0, T0, DR, DT = 2.0, np.pi / 6, 0.4, 0.2           # the Note's cell (Figure 1)
J = np.array([[np.cos(T0), -R0 * np.sin(T0)], [np.sin(T0), R0 * np.cos(T0)]])
K, ORG = 1.75, np.array([-6.4, -3.3])              # screen units per unit, screen position of (0, 0)
INSET_C, INSET_W = np.array([4.0, 0.0]), 2.4       # centre of the magnified view, screen length of J's first column times dr


def f(r, t):
    return np.array([r * np.cos(t), r * np.sin(t)])


def scr(p):
    return np.array([ORG[0] + K * p[0], ORG[1] + K * p[1], 0])


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


def cell_outline(r0, t0, dr, dt, n=30):
    s = np.linspace(0, 1, n)
    rr = np.r_[r0 + dr * s, np.full(n, r0 + dr), r0 + dr * s[::-1], np.full(n, r0)]
    tt = np.r_[np.full(n, t0), t0 + dt * s, np.full(n, t0 + dt), t0 + dt * s[::-1]]
    return rr, tt


class LocalLinear(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        w = ValueTracker(0.0)                          # 0 = input grid, 1 = output of f
        warp = lambda r, t: (1 - w.get_value()) * np.array([r, t]) + w.get_value() * f(r, t)
        rs, ts = np.arange(1.0, 3.01, 0.4), np.arange(0, np.pi / 2 + 1e-9, np.pi / 12)
        s = np.linspace(0, 1, 40)

        def grid():
            g = VGroup()
            for r in rs:
                g.add(VMobject(stroke_color=BLUE_C, stroke_width=2.5).set_points_smoothly(
                    [scr(warp(r, ts[0] + u * (ts[-1] - ts[0]))) for u in s]))
            for t in ts:
                g.add(VMobject(stroke_color=BLUE_C, stroke_width=2.5).set_points_smoothly(
                    [scr(warp(1 + 2 * u, t)) for u in s]))
            rr, tt = cell_outline(R0, T0, DR, DT)
            g.add(Polygon(*[scr(warp(a, b)) for a, b in zip(rr, tt)], stroke_color=ORANGE_C, stroke_width=4,
                          fill_color=ORANGE_C, fill_opacity=0.6))
            return g

        title = boxed(MathTex(r"\mathbf f(r, \theta) = (r\cos\theta,\ r\sin\theta)", color=BLACK, font_size=44), 0.1)
        title.to_edge(UP, buff=0.15)
        stage = boxed(Tex(r"straight $(r, \theta)$ grid", font_size=40, color=BLUE_C), 0.08).move_to([-3.6, 2.6, 0])
        self.add(always_redraw(grid), title, stage)
        self.wait(1.0)
        self.snap()                                    # straight grid, orange cell
        self.play(FadeOut(stage))
        self.play(w.animate.set_value(1.0), run_time=3.5)
        stage2 = boxed(Text("f bends the grid", font_size=32, color=BLUE_C), 0.08).move_to([-1.2, 2.6, 0])
        self.play(FadeIn(stage2))
        self.wait(1.0)
        self.snap()                                    # bent grid

        # zoom: the cell shrinks by d, the inset magnifies by 1/d so it keeps its screen size
        d = ValueTracker(1.0)
        mag = INSET_W / (DR * np.linalg.norm(J[:, 0]))  # screen units per unit when d = 1
        p0 = f(R0, T0)

        def inset():
            dd = d.get_value()
            m = mag / dd
            rr, tt = cell_outline(R0, T0, DR * dd, DT * dd)
            mid = p0 + J @ [DR * dd, DT * dd] / 2           # keep the cell centred in the frame
            to = lambda q: np.array([INSET_C[0] + m * (q[0] - mid[0]), INSET_C[1] + m * (q[1] - mid[1]), 0])
            true_cell = Polygon(*[to(f(a, b)) for a, b in zip(rr, tt)], stroke_color=ORANGE_C, stroke_width=5,
                                fill_color=ORANGE_C, fill_opacity=0.5)
            c1, c2 = J[:, 0] * DR * dd, J[:, 1] * DT * dd
            para = Polygon(to(p0), to(p0 + c1), to(p0 + c1 + c2), to(p0 + c2), stroke_color=GREEN_C,
                           stroke_width=5, fill_opacity=0)
            return VGroup(true_cell, para)

        frame = Square(side_length=5.2, color=GREY_C, stroke_width=2).move_to([*INSET_C, 0])
        link = DashedLine(scr(p0), frame.get_left(), color=GREY_C, stroke_width=2)
        legend = VGroup(Text("orange: f of the cell", font_size=26, color=ORANGE_C),
                        Text("green: J times the cell's sides", font_size=26, color=GREEN_C)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        legend = boxed(legend, 0.08).next_to(frame, DOWN, buff=0.12)
        zoom = always_redraw(lambda: boxed(MathTex(rf"\text{{cell sides}} \div {1 / d.get_value():.0f},\ \text{{zoom}} \times {1 / d.get_value():.0f}", color=BLACK,
                                                   font_size=36), 0.06).next_to(frame, UP, buff=0.1))
        self.play(FadeOut(stage2), Create(frame), Create(link), FadeIn(legend))
        self.add(always_redraw(inset), zoom)
        self.wait(1.2)
        self.snap()                                    # zoom x1: the curved cell is visibly not a parallelogram
        self.play(d.animate.set_value(0.05), run_time=4, rate_func=lambda u: 1 - (1 - u) ** 3)
        jm = boxed(MathTex(r"J(2, \tfrac{\pi}{6}) = \begin{bmatrix} 0.866 & -1 \\ 0.5 & 1.732 \end{bmatrix}",
                           color=GREEN_C, font_size=38), 0.1).move_to([-3.9, 2.65, 0])
        msg = boxed(Text("zoomed in, f acts like the matrix J", font_size=34, color=BLACK), 0.08).to_edge(UP, buff=0.15)
        self.play(FadeIn(jm), FadeOut(title), FadeIn(msg))
        self.wait(2.0)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, fr in enumerate(frames[:4]):
        sheet.paste(fr.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    # the Note's numbers: det J = r, and the linear step (0.1, 0.05) lands within 0.005 of the true point
    assert abs(np.linalg.det(J) - R0) < 1e-12
    assert np.abs(f(R0, T0) + J @ [0.1, 0.05] - f(R0 + 0.1, T0 + 0.05)).max() < 0.006
    name = "local_linear"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = LocalLinear()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
