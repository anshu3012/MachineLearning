"""The dot product as a projection: v = [3, 1] stays fixed while w (length sqrt 5) turns around the origin.
The purple shadow of w on the line of v, times |v|, is v.w: +5 at w = [1, 2], 0 when perpendicular,
-5 at w = [-2, 1], about -7.07 when w points straight against v.
Run: python projection_sweep.py  -> projection_sweep.mp4, .gif, _frames.png (Manim)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C, PURPLE_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B", "#B279A2"
Text.set_default(color=BLACK, font="Latin Modern Roman")
V = np.array([3.0, 1.0])
R = np.sqrt(5)
U = 1.0
C = np.array([-3.0, -0.4, 0])
A0 = np.degrees(np.arctan2(2, 1))                    # w = [1, 2]
STOPS = [A0, A0 + 45, A0 + 90, A0 + 135]             # +5, 0, -5, straight against v


def pt(xy):
    return C + U * np.array([xy[0], xy[1], 0])


def boxed(mob, buff=0.12):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


class ProjectionSweep(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        plane = NumberPlane(x_range=[-4, 4], y_range=[-3.5, 3.5], x_length=8 * U, y_length=7 * U,
                            background_line_style={"stroke_color": "#E3E3E3"}, axis_config={"stroke_color": "#BBBBBB"}).move_to(C)
        vhat = V / np.linalg.norm(V)
        line = DashedLine(pt(-4 * vhat), pt(4 * vhat), color=GREY_C, stroke_width=3)
        v = Arrow(pt([0, 0]), pt(V), buff=0, color=BLUE_C, stroke_width=8, max_tip_length_to_length_ratio=0.12)
        vlab = boxed(MathTex(r"\mathbf{v} = [3, 1]", color=BLUE_C, font_size=40)).next_to(pt(V), UP, buff=0.15)
        self.add(plane, line, v, vlab)
        ang = ValueTracker(A0)

        def w_xy():
            a = np.radians(ang.get_value())
            return R * np.array([np.cos(a), np.sin(a)])

        def shadow():
            return (w_xy() @ vhat)

        w = always_redraw(lambda: Arrow(pt([0, 0]), pt(w_xy()), buff=0, color=ORANGE_C, stroke_width=8,
                                        max_tip_length_to_length_ratio=0.15))
        drop = always_redraw(lambda: DashedLine(pt(w_xy()), pt(shadow() * vhat), color=GREY_C, stroke_width=3))
        bar = always_redraw(lambda: Line(pt([0, 0]), pt(shadow() * vhat), color=PURPLE_C, stroke_width=14, stroke_opacity=0.7))

        def readout():
            s = shadow()
            s = 0.0 if abs(s) < 0.005 else s
            dot = s * np.linalg.norm(V)
            col = GREEN_C if dot > 0.05 else (RED_C if dot < -0.05 else GREY_C)
            word = "same general direction" if dot > 0.05 else ("opposite general direction" if dot < -0.05 else "perpendicular")
            wx, wy = w_xy()
            g = VGroup(MathTex(rf"\mathbf{{w}} = [{wx:.2f}, {wy:.2f}]", color=ORANGE_C, font_size=40),
                       MathTex(r"\text{shadow} = " + f"{s:+.2f}", color=PURPLE_C, font_size=40),
                       MathTex(r"\mathbf{v} \cdot \mathbf{w} = " + f"{s:+.2f}" + r" \times 3.16 = " + f"{dot:+.2f}", color=col, font_size=40),
                       Text(word, font_size=32, color=col)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            return boxed(g).to_edge(RIGHT, buff=0.3)

        info = always_redraw(readout)
        self.add(bar, drop, w, info)
        self.wait(1.2)
        self.snap()
        for a in STOPS[1:]:
            self.play(ang.animate.set_value(a), run_time=2.2, rate_func=smooth)
            self.wait(1.2)
            self.snap()
        self.play(ang.animate.set_value(A0 + 360), run_time=4, rate_func=linear)
        self.wait(1)


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    assert np.isclose(V @ [1, 2], 5) and np.isclose(V @ [-2, 1], -5)
    name = "projection_sweep"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = ProjectionSweep()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
