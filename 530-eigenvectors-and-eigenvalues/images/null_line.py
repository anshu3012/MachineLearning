"""Finding the eigenvectors: A - lambda I squishes the plane flat, and the eigenvectors are the line it crushes to
the origin. For A = [[3, 1], [0, 2]]: A - 2I = [[1, 1], [0, 0]] squishes the plane onto the x-axis and sends every
vector on the line through (-1, 1) to 0 (green); then A - 3I = [[0, 1], [0, -1]] sends the whole x-axis to 0.
A vector off the line, (1, 1), survives (red). Our own design. Manim: the grid and the vectors move smoothly from
the identity to A - lambda I.
Run: python null_line.py  -> null_line.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
A = np.array([[3.0, 1.0], [0.0, 2.0]])
K, O = 0.75, np.array([0.0, -0.6, 0])                   # screen units per grid unit, screen position of the origin
CASES = [(2, [[-1, 1], [-2, 2], [1, -1], [2, -2]], r"\lambda = 2:\ A - 2I = \begin{bmatrix} 1 & 1 \\ 0 & 0 \end{bmatrix}",
          r"the line through $[-1, 1]$ is crushed to $\mathbf{0}$"),
         (3, [[1, 0], [2, 0], [-1, 0], [-2, 0]], r"\lambda = 3:\ A - 3I = \begin{bmatrix} 0 & 1 \\ 0 & -1 \end{bmatrix}",
          r"the x-axis is crushed to $\mathbf{0}$")]
OTHER = np.array([1.0, 1.0])


def boxed(mob, buff=0.1):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


def S(v):
    return O + K * np.array([v[0], v[1], 0.0])


class NullLine(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        t = ValueTracker(0.0)
        state = {"M": np.eye(2)}

        def Mt():
            return (1 - t.get_value()) * np.eye(2) + t.get_value() * state["M"]

        def grid():
            M, g = Mt(), VGroup()
            for c in range(-10, 11):
                for a, b in (([c, -10], [c, 10]), ([-10, c], [10, c])):
                    pa, pb = M @ np.array(a, float), M @ np.array(b, float)
                    g.add(Line(S(pa), S(pb), stroke_width=4 if c == 0 else 1.5,
                               color=GREY_C if c == 0 else "#C9D7E8"))
            return g

        def arrows():
            M, g = Mt(), VGroup()
            for v in state["eig"]:
                w = M @ np.array(v, float)
                if np.linalg.norm(w) > 0.08:
                    g.add(Arrow(S([0, 0]), S(w), buff=0, color=GREEN_C, stroke_width=6, max_tip_length_to_length_ratio=0.2))
            w = M @ OTHER
            g.add(Arrow(S([0, 0]), S(w), buff=0, color=RED_C, stroke_width=7, max_tip_length_to_length_ratio=0.2))
            g.add(Dot(S([0, 0]), color=BLACK, radius=0.09))
            return g

        for lam, eig, head_tex, note in CASES:
            state["M"], state["eig"] = A - lam * np.eye(2), eig
            t.set_value(0.0)
            g, ar = always_redraw(grid), always_redraw(arrows)
            head = boxed(MathTex(head_tex, color=BLACK, font_size=42), 0.12).to_edge(UP, buff=0.25)
            self.add(g, ar, head)
            self.wait(0.8)
            self.snap()
            self.play(t.animate.set_value(1.0), run_time=3, rate_func=smooth)
            msg = boxed(Tex(note, font_size=40, color=GREEN_C), 0.1).to_edge(DOWN, buff=0.3)
            red = boxed(Tex(r"$[1, 1]$ is not an eigenvector: it survives", font_size=32, color=RED_C), 0.08)
            red.next_to(msg, UP, buff=0.15)
            self.play(FadeIn(msg), FadeIn(red))
            self.wait(1.6)
            self.snap()
            self.play(FadeOut(VGroup(g, ar, head, msg, red)))
            self.remove(g, ar)


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    for lam, eig, _, _ in CASES:                         # every green vector really is sent to 0; [1, 1] is not
        M = A - lam * np.eye(2)
        assert all(np.allclose(M @ np.array(v, float), 0) for v in eig) and np.linalg.norm(M @ OTHER) > 1
    name = "null_line"
    media = HERE / ".manim_nl"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = NullLine()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=8,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=32[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
