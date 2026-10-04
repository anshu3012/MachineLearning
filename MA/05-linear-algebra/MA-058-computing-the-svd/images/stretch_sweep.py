"""Where the recipe's numbers live. A unit vector v sweeps the unit circle (left); A v sweeps an ellipse (middle);
the length |A v| is plotted against the angle of v (right). The length peaks at v1 = [1, 1]/sqrt2 with
|A v1| = sqrt45 = 6.71 = sigma1 and bottoms out at v2 = [-1, 1]/sqrt2 with |A v2| = sqrt5 = 2.24 = sigma2:
the eigenvectors of A^T A, since |A v|^2 = v^T A^T A v. Dividing A v_i by sigma_i gives the unit vectors u_i.
Run: python stretch_sweep.py  -> stretch_sweep.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C, PURPLE_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B", "#B279A2"
Text.set_default(color=BLACK, font="Latin Modern Roman")
A = np.array([[3.0, 0.0], [4.0, 5.0]])
OL, KL = np.array([-5.0, -0.4, 0]), 1.3                    # left panel: origin, screen units per unit
OM, KM = np.array([-1.2, -0.4, 0]), 0.42                   # middle panel
unit = lambda deg: np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg))])
L = lambda xy: OL + KL * np.array([xy[0], xy[1], 0.0])
M = lambda xy: OM + KM * np.array([xy[0], xy[1], 0.0])


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


def arrow(a, b, colour, width=7):
    return Arrow(a, b, buff=0, color=colour, stroke_width=width, max_tip_length_to_length_ratio=0.2)


class StretchSweep(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        th = ValueTracker(0.0)
        circle = Circle(radius=KL, color=GREY_C, stroke_width=3).move_to(OL)
        ellipse = ParametricFunction(lambda t: M(A @ unit(np.degrees(t))), t_range=[0, TAU], color=GREY_C,
                                     stroke_width=3)
        axes_l = VGroup(Line(L([-1.4, 0]), L([1.4, 0])), Line(L([0, -1.4]), L([0, 1.4]))).set_stroke(GREY_C, 1.5, 0.6)
        axes_m = VGroup(Line(M([-4, 0]), M([4, 0])), Line(M([0, -7.2]), M([0, 7.2]))).set_stroke(GREY_C, 1.5, 0.6)
        heads = VGroup(boxed(MathTex(r"\mathbf v", color=BLUE_C, font_size=44)).move_to(OL + UP * 2.4),
                       boxed(MathTex(r"A\mathbf v", color=ORANGE_C, font_size=44)).move_to(OM + UP * 3.4 + LEFT * 1.6))
        graph = Axes(x_range=[0, 180, 45], y_range=[0, 7, 1], x_length=4.2, y_length=3.6, tips=False,
                     axis_config={"color": GREY_C, "include_numbers": True, "font_size": 26,
                                  "decimal_number_config": {"color": BLACK, "num_decimal_places": 0}}).move_to([4.6, -0.3, 0])
        g_lab = VGroup(MathTex(r"\lVert A\mathbf v \rVert", color=ORANGE_C, font_size=40).next_to(graph, UP, buff=0.2),
                       Text("angle of v (degrees)", font_size=24).next_to(graph, DOWN, buff=0.45))
        length = lambda deg: np.linalg.norm(A @ unit(deg))
        curve = always_redraw(lambda: graph.plot(length, x_range=[0, max(th.get_value(), 0.5)], color=ORANGE_C,
                                                 stroke_width=5))
        v = always_redraw(lambda: arrow(OL, L(unit(th.get_value())), BLUE_C))
        av = always_redraw(lambda: arrow(OM, M(A @ unit(th.get_value())), ORANGE_C))
        dot = always_redraw(lambda: Dot(graph.c2p(th.get_value(), length(th.get_value())), color=ORANGE_C, radius=0.08))
        title = boxed(MathTex(r"A = \begin{bmatrix} 3 & 0 \\ 4 & 5 \end{bmatrix}", color=BLACK, font_size=40), 0.1)
        title.to_corner(UL, buff=0.2)
        self.add(axes_l, axes_m, circle, ellipse, heads, graph, g_lab, title, v, av, curve, dot)
        cap = boxed(Text("v goes round the unit circle; A v goes round an ellipse", font_size=28, weight=BOLD), 0.1)
        cap.to_edge(DOWN, buff=0.2)
        self.play(FadeIn(cap))
        self.play(th.animate.set_value(20.0), run_time=1)
        self.snap()
        # 1. sweep half a turn (the other half repeats it with signs flipped)
        self.play(th.animate.set_value(180.0), run_time=6, rate_func=linear)
        self.snap()
        # 2. the longest and shortest stretch: v1 and v2
        self.remove(curve)
        self.add(graph.plot(length, x_range=[0, 180], color=ORANGE_C, stroke_width=5))
        self.bring_to_front(dot)
        marks = VGroup()
        for deg, sig, name, col in ((45, r"\sigma_1 = \sqrt{45} = 6.71", "1", GREEN_C),
                                    (135, r"\sigma_2 = \sqrt{5} = 2.24", "2", RED_C)):
            self.play(th.animate.set_value(float(deg)), run_time=1.2)
            v_i = arrow(OL, L(unit(deg)), col, 9)
            av_i = arrow(OM, M(A @ unit(deg)), col, 9)
            pk = DashedLine(graph.c2p(deg, 0), graph.c2p(deg, length(deg)), color=col)
            lab = boxed(MathTex(sig, color=col, font_size=34), 0.06)
            lab.move_to(graph.c2p(112, 6.3) if name == "1" else graph.c2p(85, 1.0))
            vl = boxed(MathTex(rf"\mathbf v_{name}", color=col, font_size=40), 0.05)
            vl.next_to(L(1.25 * unit(deg)), UP if name == "1" else LEFT, buff=0.05)
            marks.add(v_i, av_i, pk, lab, vl)
            self.play(FadeIn(v_i, av_i, pk, lab, vl))
            self.wait(0.4)
        cap2 = boxed(Text("longest and shortest stretch: v1 and v2, at 90 degrees", font_size=28, weight=BOLD), 0.1)
        cap2.to_edge(DOWN, buff=0.2)
        self.play(FadeTransform(cap, cap2), FadeOut(v, av, dot))
        self.wait(1)
        self.snap()
        # 3. the recipe in one line
        cap3 = boxed(MathTex(r"\lVert A\mathbf v\rVert^2 = \mathbf v^{\mathsf T}A^{\mathsf T}\!A\,\mathbf v"
                             r"\;\Rightarrow\; \mathbf v_i \text{ eigenvectors of } A^{\mathsf T}\!A,\ "
                             r"\sigma_i = \sqrt{\lambda_i},\ \mathbf u_i = A\mathbf v_i/\sigma_i",
                             color=BLACK, font_size=36), 0.1).to_edge(DOWN, buff=0.2)
        self.play(FadeTransform(cap2, cap3))
        self.wait(2.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    lam, V = np.linalg.eigh(A.T @ A)
    assert np.allclose(lam, [5, 45])
    degs = np.arange(0, 180, 0.5)
    lens = [np.linalg.norm(A @ unit(d)) for d in degs]
    assert degs[np.argmax(lens)] == 45 and degs[np.argmin(lens)] == 135          # peaks sit at v1 and v2
    assert np.isclose(max(lens), np.sqrt(45)) and np.isclose(min(lens), np.sqrt(5))
    name = "stretch_sweep"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = StretchSweep()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=48:stats_mode=diff[p];"
                    "[b][p]paletteuse=dither=none:diff_mode=rectangle", str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
