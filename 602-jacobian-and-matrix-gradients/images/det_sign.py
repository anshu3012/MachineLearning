"""The determinant as an area factor, with a sign (idea after 3Blue1Brown, "The determinant | Chapter 6, Essence of
linear algebra"; our own code). Part 1: the Note's matrix A = [[1, 3], [-2, 0]] takes the unit square to a
parallelogram of area 6. Part 2: i-hat swings towards j-hat and past it; the area shrinks to 0 and the determinant
turns negative as the square flips over.  Run: python det_sign.py  -> det_sign.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, GREEN_C, RED_C, GREY_C, POS_C, NEG_C = "#4C78A8", "#54A24B", "#E45756", "#BBBBBB", "#4C78A8", "#E45756"
Text.set_default(color=BLACK, font="Latin Modern Roman")
A = np.array([[1.0, 3.0], [-2.0, 0.0]])
K, ORG = 0.85, np.array([-2.8, 0.0])


def sc(p):
    return np.array([ORG[0] + K * p[0], ORG[1] + K * p[1], 0])


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


class DetSign(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        M = [np.eye(2)]                                  # the current matrix, changed by the updaters below

        def picture():
            m = M[0]
            out = VGroup()
            for i in range(-30, 31):
                out.add(Line(sc(m @ [i, -40]), sc(m @ [i, 40]), color=GREY_C, stroke_width=1.5))
                out.add(Line(sc(m @ [-40, i]), sc(m @ [40, i]), color=GREY_C, stroke_width=1.5))
            d = np.linalg.det(m)
            out.add(Polygon(sc([0, 0]), sc(m[:, 0]), sc(m[:, 0] + m[:, 1]), sc(m[:, 1]), stroke_width=0,
                            fill_color=POS_C if d >= 0 else NEG_C, fill_opacity=0.45))
            out.add(Arrow(sc([0, 0]), sc(m[:, 0]), buff=0, color=GREEN_C, stroke_width=7))
            out.add(Arrow(sc([0, 0]), sc(m[:, 1]), buff=0, color=RED_C, stroke_width=7))
            out.add(MathTex(r"\hat\imath", color=GREEN_C, font_size=44).next_to(sc(m[:, 0]), DR, buff=0.05))
            out.add(MathTex(r"\hat\jmath", color=RED_C, font_size=44).next_to(sc(m[:, 1]), UL, buff=0.05))
            word = "area" if d >= -1e-9 else "flipped, area"
            out.add(boxed(Text(f"det = {d:+.2f}   ({word} × {abs(d):.2f})", font_size=30,
                               color=POS_C if d >= 0 else NEG_C), 0.08).move_to([3.3, 2.5, 0]))
            return out

        self.add(always_redraw(picture))
        title = boxed(Text("the unit square: area 1", font_size=32), 0.08).move_to([3.3, 3.4, 0])
        self.add(title)
        self.wait(1.0)
        self.snap()
        t = ValueTracker(0.0)
        upd = lambda mob: M.__setitem__(0, (1 - t.get_value()) * np.eye(2) + t.get_value() * A)
        holder = Mobject().add_updater(upd)
        self.add(holder)
        self.play(t.animate.set_value(1.0), run_time=3.0)
        mat = boxed(MathTex(r"A = \begin{bmatrix} 1 & 3 \\ -2 & 0 \end{bmatrix}", color=BLACK, font_size=40), 0.1)
        mat.move_to([3.3, 1.2, 0])
        self.play(FadeIn(mat), Transform(title, boxed(Text("A makes every area 6 times larger", font_size=32),
                                                         0.08).move_to([3.3, 3.4, 0])))
        self.wait(1.5)
        self.snap()
        holder.clear_updaters()
        self.play(FadeOut(mat))
        M[0] = np.eye(2)
        a = ValueTracker(0.0)
        holder.add_updater(lambda mob: M.__setitem__(0, np.array([[np.cos(a.get_value()), 0.0],
                                                                   [np.sin(a.get_value()), 1.0]])))
        self.play(Transform(title, boxed(Text("î swings towards ĵ ...", font_size=32), 0.08).move_to([3.3, 3.4, 0])))
        self.play(a.animate.set_value(np.pi / 2), run_time=3.0, rate_func=linear)
        self.wait(0.6)
        self.snap()                                      # i-hat on top of j-hat: det = 0
        self.play(Transform(title, boxed(Text("... and past it: the square flips over", font_size=32), 0.08)
                            .move_to([3.3, 3.4, 0])))
        self.play(a.animate.set_value(5 * np.pi / 6), run_time=2.0, rate_func=linear)
        self.wait(2.0)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, fr in enumerate(frames[:4]):
        sheet.paste(fr.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    assert abs(np.linalg.det(A) - 6) < 1e-12                       # the Note's Section 4 matrix
    name = "det_sign"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = DetSign()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=8,scale=600:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=32:stats_mode=diff[p];[b][p]paletteuse=dither=none:diff_mode=rectangle",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
