"""The same two transformations in both orders, side by side. Left: shear S first, then rotation R (product RS):
i-hat ends at (0, 1), j-hat at (-1, 1). Right: rotation first, then shear (SR): i-hat at (1, 1), j-hat at (-1, 0).
Run: python order_matters.py  -> order_matters.mp4, .gif, _frames.png (Manim)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
R = np.array([[0, -1], [1, 0]])
S = np.array([[1, 1], [0, 1]])
U = 0.85
CL, CR = np.array([-3.5, 0.0, 0]), np.array([3.5, 0.0, 0])


def boxed(mob, buff=0.1):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


def vec(c, xy, colour):
    return Arrow(c, c + U * np.array([*xy, 0]), buff=0, color=colour, stroke_width=7, max_tip_length_to_length_ratio=0.25)


def plane(c, ghost=False):
    style = {"stroke_color": "#E3E3E3"} if ghost else {"stroke_color": BLUE_C, "stroke_opacity": 0.35}
    return NumberPlane(x_range=[-2, 2], y_range=[-2, 2], x_length=4 * U, y_length=4 * U, background_line_style=style,
                       axis_config={"stroke_color": "#BBBBBB" if ghost else BLUE_C}).move_to(c)


class OrderMatters(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        self.add(plane(CL, True), plane(CR, True))
        pl, pr = plane(CL), plane(CR)
        il, jl, ir, jr = vec(CL, [1, 0], GREEN_C), vec(CL, [0, 1], RED_C), vec(CR, [1, 0], GREEN_C), vec(CR, [0, 1], RED_C)
        tl = boxed(Text("shear first, then rotate", font_size=34)).move_to(CL + np.array([0, 3.4, 0]))
        tr = boxed(Text("rotate first, then shear", font_size=34)).move_to(CR + np.array([0, 3.4, 0]))
        self.add(pl, pr, il, jl, ir, jr, tl, tr)
        self.wait(0.8)
        self.snap()
        Ml, Mr = np.eye(2), np.eye(2)
        for step, (A, B) in enumerate([(S, R), (R, S)]):          # left gets A, right gets B
            Ml, Mr = A @ Ml, B @ Mr
            self.play(ApplyMatrix(A, pl, about_point=CL), ApplyMatrix(B, pr, about_point=CR),
                      Transform(il, vec(CL, Ml[:, 0], GREEN_C)), Transform(jl, vec(CL, Ml[:, 1], RED_C)),
                      Transform(ir, vec(CR, Mr[:, 0], GREEN_C)), Transform(jr, vec(CR, Mr[:, 1], RED_C)), run_time=2.2)
            self.wait(0.6)
            self.snap()
        fmt = lambda v: f"[{int(v[0])}, {int(v[1])}]"
        ll = VGroup(boxed(MathTex(r"\hat{\imath} \to " + fmt(Ml[:, 0]), color=GREEN_C, font_size=38)),
                    boxed(MathTex(r"\hat{\jmath} \to " + fmt(Ml[:, 1]), color=RED_C, font_size=38)),
                    boxed(MathTex(r"RS = \begin{bmatrix} 0 & -1 \\ 1 & 1 \end{bmatrix}", color=BLACK, font_size=38))
                    )
        ll = VGroup(VGroup(ll[0], ll[1]).arrange(RIGHT, buff=0.3), ll[2]).arrange(DOWN, buff=0.2).move_to(CL + np.array([0, -2.9, 0]))
        lr = VGroup(boxed(MathTex(r"\hat{\imath} \to " + fmt(Mr[:, 0]), color=GREEN_C, font_size=38)),
                    boxed(MathTex(r"\hat{\jmath} \to " + fmt(Mr[:, 1]), color=RED_C, font_size=38)),
                    boxed(MathTex(r"SR = \begin{bmatrix} 1 & -1 \\ 1 & 0 \end{bmatrix}", color=BLACK, font_size=38))
                    )
        lr = VGroup(VGroup(lr[0], lr[1]).arrange(RIGHT, buff=0.3), lr[2]).arrange(DOWN, buff=0.2).move_to(CR + np.array([0, -2.9, 0]))
        self.play(FadeIn(ll), FadeIn(lr))
        self.wait(2.2)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    assert (R @ S == [[0, -1], [1, 1]]).all() and (S @ R == [[1, -1], [1, 0]]).all()
    name = "order_matters"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = OrderMatters()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
