"""PCA as rotating the axes: project the flats onto a line through the centre, turn the line, watch the variance.
The line with the largest variance is PC1; the one at right angles is PC2.
Run: python rotate_axes.py  -> rotate_axes.mp4, rotate_axes.gif, rotate_axes_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
from flats import rooms, washrooms

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
P = np.c_[rooms, washrooms]
C = P.mean(axis=0)
var_at = lambda deg: float(((P - C) @ [np.cos(np.radians(deg)), np.sin(np.radians(deg))]).var())
ANGLES = np.arange(0, 180, 0.5)
BEST = float(ANGLES[np.argmax([var_at(a) for a in ANGLES])])


class RotateAxes(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        axes = Axes(x_range=[0, 6, 1], y_range=[0, 6, 1], x_length=5.2, y_length=5.2, tips=False,
                    axis_config={"color": GREY_C, "include_numbers": True,
                                 "decimal_number_config": {"num_decimal_places": 0, "color": GREY_C}}
                    ).to_edge(LEFT, buff=0.8).shift(DOWN * 0.05)
        xl = Text("rooms", font_size=22, color=GREY_C).next_to(axes.x_axis, DOWN, buff=0.4)
        yl = Text("washrooms", font_size=22, color=GREY_C).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.45)
        dots = VGroup(*[Dot(axes.c2p(*p), radius=0.07, color=BLUE_C) for p in P])
        angle = ValueTracker(0)

        def direction():
            a = np.radians(angle.get_value())
            return np.array([np.cos(a), np.sin(a)])

        def line():
            d = direction()
            return Line(axes.c2p(*(C - 3.2 * d)), axes.c2p(*(C + 3.2 * d)), color=ORANGE_C, stroke_width=5)

        def shadows():
            d = direction()
            return VGroup(*[Dot(axes.c2p(*(C + ((p - C) @ d) * d)), radius=0.055, color=ORANGE_C) for p in P])

        def drops():
            d = direction()
            return VGroup(*[DashedLine(axes.c2p(*p), axes.c2p(*(C + ((p - C) @ d) * d)), color=GREY_C,
                                       stroke_width=1.5, dash_length=0.05) for p in P])

        rot_line, shadow, drop = always_redraw(line), always_redraw(shadows), always_redraw(drops)
        title = Text("Turn the line, measure the spread of the shadows", font_size=28, weight=BOLD).to_edge(UP, buff=0.3)
        panel_x = 3.6
        angle_txt = always_redraw(lambda: Text(f"angle: {angle.get_value():.0f}°", font_size=28)
                                  .move_to([panel_x, 1.6, 0]))
        var_txt = always_redraw(lambda: Text(f"variance of shadows: {var_at(angle.get_value()):.2f}", font_size=28,
                                             color=ORANGE_C).move_to([panel_x, 0.9, 0]))
        self.play(Create(axes), FadeIn(xl, yl, dots, title))
        self.add(drop, rot_line, shadow, angle_txt, var_txt)
        self.wait(0.6)
        note = Text("along rooms", font_size=24, color=GREY_C).move_to([panel_x, 0.2, 0])
        self.play(FadeIn(note))
        self.snap()
        self.play(FadeOut(note), angle.animate.set_value(90), run_time=3)
        note = Text("along washrooms: same spread", font_size=24, color=GREY_C).move_to([panel_x, 0.2, 0])
        self.play(FadeIn(note))
        self.snap()
        self.play(FadeOut(note), angle.animate.set_value(BEST), run_time=2.5)
        note = Text("largest spread: this line is PC1", font_size=24, color=ORANGE_C, weight=BOLD).move_to([panel_x, 0.2, 0])
        self.play(FadeIn(note))
        self.snap()
        # PC2 at right angles
        d2 = np.array([np.cos(np.radians(BEST + 90)), np.sin(np.radians(BEST + 90))])
        pc2 = Line(axes.c2p(*(C - 1.6 * d2)), axes.c2p(*(C + 1.6 * d2)), color=GREEN_C, stroke_width=5)
        pc1_lab = Text("PC1", font_size=24, color=ORANGE_C, weight=BOLD).move_to(axes.c2p(*(C + 3.5 * direction())))
        pc2_lab = Text("PC2", font_size=24, color=GREEN_C, weight=BOLD).next_to(pc2.get_end(), UP, buff=0.1)
        summary = VGroup(
            Text(f"PC1 variance: {var_at(BEST):.2f}", font_size=26, color=ORANGE_C),
            Text(f"PC2 variance: {var_at(BEST + 90):.2f}", font_size=26, color=GREEN_C),
            Text("keep PC1, drop PC2:", font_size=24),
            Text("2 columns become 1", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([panel_x, -1.3, 0])
        self.play(Create(pc2), FadeIn(pc1_lab, pc2_lab), FadeIn(summary, lag_ratio=0.2))
        self.wait(1.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    print(f"rooms axis {var_at(0):.2f}, washrooms axis {var_at(90):.2f}, PC1 at {BEST}° {var_at(BEST):.2f}, "
          f"PC2 {var_at(BEST + 90):.2f}")
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "rotate_axes", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = RotateAxes()
        scene.render()
    mp4 = HERE / "rotate_axes.mp4"
    shutil.copy(next(media.rglob("rotate_axes.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "rotate_axes.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "rotate_axes_frames.png")
    shutil.rmtree(media)
