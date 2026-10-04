"""Four matrices read as moving grids: rotation by 90 degrees, shear, the matrix with columns [1, 2] and [3, 1],
and dependent columns [2, 1], [-1, -0.5] that squash the plane onto one line. Green = where i-hat lands (column 1),
red = where j-hat lands (column 2), grey = the grid before.
Run: python gallery_morph.py  -> gallery_morph.mp4, .gif, _frames.png (Manim)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
CASES = [("Rotation by 90°", [[0, -1], [1, 0]]),
         ("Shear", [[1, 1], [0, 1]]),
         ("From matrix to picture", [[1, 3], [2, 1]]),
         ("Dependent columns: squashed onto a line", [[2, -1], [1, -0.5]])]


def boxed(mob, buff=0.12):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


def vec(xy, colour):
    return Arrow(ORIGIN, [*xy, 0], buff=0, color=colour, stroke_width=8, max_tip_length_to_length_ratio=0.2)


def fmt(x):
    return f"{x:g}"


class GalleryMorph(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        ghost = NumberPlane(x_range=[-8, 8], y_range=[-5, 5], background_line_style={"stroke_color": "#E3E3E3"},
                            axis_config={"stroke_color": "#BBBBBB"})
        self.add(ghost)
        for title, A in CASES:
            plane = NumberPlane(x_range=[-14, 14], y_range=[-14, 14], faded_line_ratio=0,
                                background_line_style={"stroke_color": BLUE_C, "stroke_opacity": 0.35},
                                axis_config={"stroke_color": BLUE_C})
            i_hat, j_hat = vec([1, 0], GREEN_C), vec([0, 1], RED_C)
            m = Matrix([[fmt(A[0][0]), fmt(A[0][1])], [fmt(A[1][0]), fmt(A[1][1])]],
                       element_to_mobject_config={"color": BLACK}, bracket_config={"color": BLACK}, h_buff=1.1)
            m.get_columns()[0].set_color(GREEN_C)
            m.get_columns()[1].set_color(RED_C)
            head = boxed(VGroup(Text(title, font_size=36), m.scale(0.8)).arrange(RIGHT, buff=0.35)).to_edge(UP, buff=0.25)
            self.play(FadeIn(plane), FadeIn(i_hat), FadeIn(j_hat), FadeIn(head), run_time=0.8)
            self.wait(0.4)
            c1, c2 = np.array(A)[:, 0], np.array(A)[:, 1]
            self.play(ApplyMatrix(A, plane), Transform(i_hat, vec(c1, GREEN_C)), Transform(j_hat, vec(c2, RED_C)),
                      run_time=2.5)
            lab = VGroup(boxed(MathTex(rf"\hat{{\imath}} \to [{fmt(c1[0])}, {fmt(c1[1])}]", color=GREEN_C, font_size=40)),
                         boxed(MathTex(rf"\hat{{\jmath}} \to [{fmt(c2[0])}, {fmt(c2[1])}]", color=RED_C, font_size=40))
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DL, buff=0.35)
            extra = VGroup()
            if title.startswith("Dependent"):
                extra = boxed(Text("every point lands on the line through [2, 1]", font_size=30, color=RED_C)).to_corner(DR, buff=0.35)
            self.play(FadeIn(lab), FadeIn(extra))
            self.wait(1.6)
            self.snap()
            self.play(FadeOut(VGroup(plane, i_hat, j_hat, head, lab, extra)), run_time=0.6)


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    assert np.allclose(np.array(CASES[0][1]) @ [3, 1], [-1, 3])          # rotation: [3, 1] -> [-1, 3]
    assert np.allclose(np.array(CASES[1][1]) @ [2, 3], [5, 3])           # shear: [2, 3] -> [5, 3]
    assert np.allclose(np.array(CASES[2][1]) @ [1, 1], [4, 3])           # [1, 1] -> [4, 3]
    assert np.allclose(np.array(CASES[3][1]) @ [3, -1], [7, 3.5])        # squash: [3, -1] -> [7, 3.5]
    name = "gallery_morph"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = GalleryMorph()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=8,scale=560:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=24:stats_mode=diff[p];"
                    "[b][p]paletteuse=dither=none:diff_mode=rectangle",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
