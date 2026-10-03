"""A matrix as a transformation of the whole grid. Most vectors turn; the eigenvectors only stretch.
Matrix [[3, 1], [0, 2]]: (1, 0) -> (3, 0), eigenvalue 3; (-1, 1) -> (-2, 2), eigenvalue 2; (1, 1) -> (4, 2) turns.
Run: python eigen_transform.py  -> eigen_transform.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
A = [[3, 1], [0, 2]]


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.9, buff=buff), mob)


class EigenTransform(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def label(self, text, colour, pos):
        return boxed(Text(text, font_size=26, color=colour, weight=BOLD).move_to(pos))

    def construct(self):
        self.snaps = []
        ghost = NumberPlane(x_range=[-8, 8], y_range=[-5, 5], background_line_style={"stroke_color": "#E3E3E3"},
                            axis_config={"stroke_color": "#BBBBBB"})
        plane = NumberPlane(x_range=[-8, 8], y_range=[-5, 5], faded_line_ratio=0,
                            background_line_style={"stroke_color": BLUE_C, "stroke_opacity": 0.35},
                            axis_config={"stroke_color": BLUE_C})
        vec = lambda xy, c: Arrow(ORIGIN, [*xy, 0], buff=0, color=c, stroke_width=7,
                                  max_tip_length_to_length_ratio=0.2)
        v1, v2, v3 = vec([1, 0], GREEN_C), vec([-1, 1], GREEN_C), vec([1, 1], RED_C)
        title = boxed(Text("Matrix [[3, 1], [0, 2]] applied to every vector", font_size=30, weight=BOLD), 0.1)
        title.to_edge(UP, buff=0.25)
        self.add(ghost, plane, v1, v2, v3, title)
        labels = VGroup(self.label("(1, 0)", GREEN_C, [1.2, -0.45, 0]), self.label("(-1, 1)", GREEN_C, [-1.6, 1.3, 0]),
                        self.label("(1, 1)", RED_C, [1.45, 1.35, 0]))
        self.play(FadeIn(labels))
        self.wait(0.6)
        self.snap()
        self.play(FadeOut(labels))
        self.play(ApplyMatrix(A, plane), Transform(v1, vec([3, 0], GREEN_C)), Transform(v2, vec([-2, 2], GREEN_C)),
                  Transform(v3, vec([4, 2], RED_C)), run_time=3)
        self.bring_to_front(title)
        after = VGroup(self.label("(3, 0): same line, 3 times longer", GREEN_C, [3.3, -0.5, 0]),
                       self.label("(-2, 2): same line, 2 times longer", GREEN_C, [-3.4, 2.5, 0]),
                       self.label("(4, 2): direction changed", RED_C, [4.4, 2.6, 0]))
        self.play(FadeIn(after))
        self.wait(0.8)
        self.snap()
        lines = VGroup(DashedLine([-7, 0, 0], [7, 0, 0], color=GREEN_C, stroke_width=5, dash_length=0.15),
                       DashedLine([3.6, -3.6, 0], [-3.6, 3.6, 0], color=GREEN_C, stroke_width=5, dash_length=0.15))
        note = VGroup(Text("eigenvectors stay on their own line", font_size=28, color=GREEN_C, weight=BOLD),
                      Text("eigenvalues: how much they stretch (3 and 2)", font_size=26, color=GREEN_C))
        note = boxed(note.arrange(DOWN, buff=0.15), 0.1).to_edge(DOWN, buff=0.35)
        self.play(Create(lines), FadeIn(note))
        self.bring_to_front(after)
        self.wait(1)
        self.snap()
        formula = boxed(MathTex(r"A v = \lambda v", font_size=60, color=BLACK), 0.12).to_corner(DL, buff=0.5)
        self.play(FadeIn(formula))
        self.wait(1.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    w, v = np.linalg.eig(np.array(A, float))
    print("eigenvalues", w, "eigenvectors (columns)\n", v.round(3))
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "eigen_transform", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = EigenTransform()
        scene.render()
    mp4 = HERE / "eigen_transform.mp4"
    shutil.copy(next(media.rglob("eigen_transform.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "eigen_transform.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "eigen_transform_frames.png")
    shutil.rmtree(media)
