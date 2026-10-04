"""Build the Jacobian's columns from two tiny steps (idea after Khan Academy, "The Jacobian matrix"; our own code
and example). Polar coordinates f(r, theta) = (r cos theta, r sin theta) at the Note's point (2, pi/6).
Left: a step of size h along r, then along theta, in the input plane. Right: its image step under f (thin), and the
image step divided by h (thick). As h shrinks, the thick arrow settles on a column of J.
Run: python two_steps.py  -> two_steps.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#B279A2", "#9A9A9A"
Text.set_default(color=BLACK, font="Latin Modern Roman")
R0, T0 = 2.0, np.pi / 6
J = np.array([[np.cos(T0), -R0 * np.sin(T0)], [np.sin(T0), R0 * np.cos(T0)]])
KI, ORG_I = 1.9, np.array([-8.1, -3.0])            # input panel: screen units per unit, screen spot of (0, 0)
KO, ORG_O = 1.55, np.array([0.2, -3.3])            # output panel


def f(p):
    return np.array([p[0] * np.cos(p[1]), p[0] * np.sin(p[1])])


def si(p):
    return np.array([ORG_I[0] + KI * p[0], ORG_I[1] + KI * p[1], 0])


def so(p):
    return np.array([ORG_O[0] + KO * p[0], ORG_O[1] + KO * p[1], 0])


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


def quotient(e, h):
    p = np.array([R0, T0])
    return (f(p + h * e) - f(p)) / h


class TwoSteps(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        rs, ts = np.arange(1.0, 3.01, 0.5), np.linspace(0, np.pi / 2, 7)
        s = np.linspace(0, 1, 40)
        grid_in, grid_out = VGroup(), VGroup()
        for r in rs:
            grid_in.add(Line(si([r, ts[0]]), si([r, ts[-1]]), color=BLUE_C, stroke_width=2))
            grid_out.add(VMobject(stroke_color=BLUE_C, stroke_width=2).set_points_smoothly(
                [so(f([r, ts[0] + u * (ts[-1] - ts[0])])) for u in s]))
        for t in ts:
            grid_in.add(Line(si([rs[0], t]), si([rs[-1], t]), color=BLUE_C, stroke_width=2))
            grid_out.add(Line(so(f([rs[0], t])), so(f([rs[-1], t])), color=BLUE_C, stroke_width=2))
        lab_in = Text("input (r, θ)", font_size=30, color=BLUE_C).move_to(si([2.0, -0.28]))
        lab_out = Text("output (x, y) = f(r, θ)", font_size=30, color=BLUE_C).move_to(so([2.4, -0.2]))
        p_in, p_out = si([R0, T0]), so(f([R0, T0]))
        dots = VGroup(Dot(p_in, color=BLACK, radius=0.07), Dot(p_out, color=BLACK, radius=0.07))
        title = boxed(Text("Where does a tiny step land?", font_size=40), 0.1).to_edge(UP, buff=0.15)
        self.add(grid_in, grid_out, lab_in, lab_out, dots, title)
        self.wait(0.8)

        cols = []
        for k, (e, name, colour) in enumerate([(np.array([1.0, 0.0]), "r", ORANGE_C),
                                                (np.array([0.0, 1.0]), "θ", PURPLE_C)]):
            h = ValueTracker(0.6)
            step_in = always_redraw(lambda e=e, colour=colour: Arrow(
                p_in, si(np.array([R0, T0]) + h.get_value() * e), buff=0, color=colour, stroke_width=6,
                max_tip_length_to_length_ratio=0.35))
            step_out = always_redraw(lambda e=e, colour=colour: Arrow(
                p_out, so(f(np.array([R0, T0]) + h.get_value() * e)), buff=0, color=colour, stroke_width=6,
                max_tip_length_to_length_ratio=0.35))
            q_arrow = always_redraw(lambda e=e: Arrow(
                p_out, p_out + KO * np.r_[quotient(e, h.get_value()), 0], buff=0, color=GREEN_C, stroke_width=8,
                max_tip_length_to_length_ratio=0.15))

            def readout(e=e, name=name, colour=colour):
                q = quotient(e, h.get_value())
                g = VGroup(Text(f"step along {name}:  h = {h.get_value():.2f}", font_size=30, color=colour),
                           Text(f"image step ÷ h = ({q[0]:.3f}, {q[1]:.3f})", font_size=30, color=GREEN_C)
                           ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
                return boxed(g, 0.08).move_to([-4.0, 1.55, 0])
            ro = always_redraw(readout)
            self.play(GrowArrow(step_in), FadeIn(ro))
            self.play(TransformFromCopy(step_in, step_out), run_time=1.2)
            self.play(GrowArrow(q_arrow))
            self.wait(0.8)
            if k == 1:
                self.snap()                            # theta step, h = 0.6: the quotient is still off
            self.play(h.animate.set_value(0.01), run_time=4, rate_func=lambda u: 1 - (1 - u) ** 2)
            self.wait(0.8)
            if k == 0:
                self.snap()                            # r step, h small: column 1
            col = Arrow(p_out, p_out + KO * np.r_[J[:, k], 0], buff=0, color=GREEN_C, stroke_width=8,
                        max_tip_length_to_length_ratio=0.15)
            col_lab = boxed(Text(f"column {k + 1}", font_size=32, color=GREEN_C), 0.05)
            col_lab.next_to(col.get_end(), RIGHT if k == 0 else UP, buff=0.12)
            self.remove(q_arrow)
            self.add(col)
            self.play(FadeOut(step_in), FadeOut(step_out), FadeOut(ro), FadeIn(col_lab))
            cols.append(VGroup(col, col_lab))

        jm = boxed(MathTex(r"J\left(2, \tfrac{\pi}{6}\right) = \begin{bmatrix} 0.866 & -1 \\ 0.5 & 1.732 \end{bmatrix}",
                           color=GREEN_C, font_size=44), 0.12).move_to([-4.0, 1.55, 0])
        msg = boxed(Text("the two image steps ÷ h are the Jacobian's columns", font_size=34), 0.1).to_edge(UP, buff=0.15)
        self.play(FadeIn(jm), FadeOut(title), FadeIn(msg))
        self.wait(2.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, fr in enumerate(frames[:4]):
        sheet.paste(fr.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    # the Note's numbers: the r-quotient is exactly column 1; the theta-quotient tends to column 2
    assert np.allclose(quotient(np.array([1.0, 0.0]), 0.6), J[:, 0])
    assert np.abs(quotient(np.array([0.0, 1.0]), 0.01) - J[:, 1]).max() < 0.01
    assert np.allclose(quotient(np.array([0.0, 1.0]), 0.6), [-1.445, 1.339], atol=2e-3)
    name = "two_steps"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = TwoSteps()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
