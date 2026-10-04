"""One arrow, two bases. x = [3, -2] is 3 i-hat - 2 j-hat on the standard grid, and 0.5 v + 2.5 w on the grid
built from v = [1, 1] and w = [1, -1]. The arrow never moves; only the grid we measure it with changes.
Run: python change_basis.py  -> change_basis.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C, PURPLE_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B", "#B279A2"
Text.set_default(color=BLACK, font="Latin Modern Roman")
X, V, W = np.array([3.0, -2.0]), np.array([1.0, 1.0]), np.array([1.0, -1.0])
O = np.array([-2.2, 0.9, 0])                                # screen position of the origin
K = 1.0                                                     # screen units per data unit
P = lambda xy: O + K * np.array([xy[0], xy[1], 0.0])


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


def arrow(a, b, colour, width=7):
    return Arrow(P(a), P(b), buff=0, color=colour, stroke_width=width, max_tip_length_to_length_ratio=0.2)


def grid(M, colour, opacity):
    """Grid lines of the basis given by the columns of M (the camera clips them to the frame)."""
    lines = VGroup()
    for k in range(-14, 15):
        for d, e in ((M[:, 0], M[:, 1]), (M[:, 1], M[:, 0])):
            a, b = k * e - 14 * d, k * e + 14 * d
            lines.add(Line(P(a), P(b), stroke_color=colour, stroke_width=1.6, stroke_opacity=opacity))
    return lines


class ChangeBasis(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        std = grid(np.eye(2), GREY_C, 0.35)
        new = grid(np.column_stack([V, W]), PURPLE_C, 0.5)
        x = arrow([0, 0], X, ORANGE_C, 9)
        dot = Dot(P([0, 0]), color=BLACK, radius=0.06)
        name = boxed(MathTex(r"\mathbf x", color=ORANGE_C, font_size=50), 0.06).move_to(P(X) + RIGHT * 0.45)
        self.add(std, x, dot, name)
        self.wait(0.6)
        # 1. standard basis: 3 i-hat then -2 j-hat
        i3, j2 = arrow([0, 0], [3, 0], GREEN_C), arrow([3, 0], X, RED_C)
        head = boxed(MathTex(r"\mathbf x = 3\,\hat\imath - 2\,\hat\jmath", r"\;\to\; [3, -2]", color=BLACK,
                             font_size=46), 0.12).to_corner(UR, buff=0.3)
        self.play(GrowArrow(i3), run_time=0.8)
        self.play(GrowArrow(j2), FadeIn(head), run_time=0.8)
        self.wait(1)
        self.snap()
        # 2. swap the grid for the one built from v and w
        vw = VGroup(arrow([0, 0], V, BLUE_C, 9), arrow([0, 0], W, BLUE_C, 9))
        vw_lab = VGroup(boxed(MathTex(r"\mathbf v", color=BLUE_C, font_size=44), 0.05).move_to(P(V) + UL * 0.35),
                        boxed(MathTex(r"\mathbf w", color=BLUE_C, font_size=44), 0.05).move_to(P(W) + DL * 0.35))
        cap = boxed(Text("new basis v = [1, 1], w = [1, -1]", font_size=30, weight=BOLD, color=BLUE_C), 0.12)
        cap.to_edge(DOWN, buff=0.3)
        self.play(FadeOut(i3, j2, head), FadeOut(std), FadeIn(new), GrowArrow(vw[0]), GrowArrow(vw[1]),
                  FadeIn(vw_lab), FadeIn(cap), run_time=1.5)
        self.bring_to_front(x, dot, name)
        self.wait(0.8)
        self.snap()
        # 3. the same arrow as 0.5 v + 2.5 w
        a_part, b_part = arrow([0, 0], 0.5 * V, BLUE_C, 9), arrow(0.5 * V, X, BLUE_C, 9)
        head2 = boxed(MathTex(r"\mathbf x = 0.5\,\mathbf v + 2.5\,\mathbf w", r"\;\to\; [0.5, 2.5]", color=BLACK,
                              font_size=46), 0.12).to_corner(UR, buff=0.3)
        self.play(FadeOut(vw, vw_lab), GrowArrow(a_part), run_time=0.8)
        parts = VGroup(boxed(MathTex(r"0.5\,\mathbf v", color=BLUE_C, font_size=40), 0.05).next_to(P(0.5 * V), UP, 0.1),
                       boxed(MathTex(r"2.5\,\mathbf w", color=BLUE_C, font_size=40), 0.05).move_to(P(0.5 * V + 1.25 * W) + UR * 0.4))
        self.play(GrowArrow(b_part), FadeIn(head2), FadeIn(parts), run_time=1)
        self.bring_to_front(x, dot, name)
        self.wait(0.8)
        self.snap()
        cap2 = boxed(Text("same arrow, different numbers: coordinates depend on the basis", font_size=28,
                          weight=BOLD), 0.12).to_edge(DOWN, buff=0.3)
        self.play(FadeTransform(cap, cap2))
        self.wait(2)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    assert np.allclose(np.linalg.solve(np.column_stack([V, W]), X), [0.5, 2.5])
    name = "change_basis"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = ChangeBasis()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=48:stats_mode=diff[p];[b][p]paletteuse=dither=none:diff_mode=rectangle",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
