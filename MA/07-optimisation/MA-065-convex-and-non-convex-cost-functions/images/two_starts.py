"""Gradient descent on the non-convex g(w) = w^4 - 4w^2 + w from two starting points (learning rate 0.02).
Started at w = -2 it reaches the global minimum w = -1.47 (g = -5.44); started at w = 2 it stops in the
local minimum w = 1.35 (g = -2.62), where the slope is also 0.
Run: python two_starts.py  -> two_starts.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
g = lambda w: w ** 4 - 4 * w ** 2 + w
dg = lambda w: 4 * w ** 3 - 8 * w + 1
LR, STEPS = 0.02, 30


def path(w0):
    ws = [w0]
    for _ in range(STEPS):
        ws.append(ws[-1] - LR * dg(ws[-1]))
    return ws


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


class TwoStarts(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        ax = Axes(x_range=[-2.2, 2.2, 1], y_range=[-6, 6, 2], x_length=10, y_length=5.6, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 26,
                               "decimal_number_config": {"color": BLACK, "num_decimal_places": 0}})
        ax.shift(DOWN * 0.4)
        curve = ax.plot(g, x_range=[-2.05, 2.05], color=BLUE_C, stroke_width=5)
        lab = MathTex(r"g(w) = w^4 - 4w^2 + w", color=BLUE_C, font_size=38).to_corner(UL, buff=0.4)
        wl = MathTex("w", color=BLACK, font_size=34).next_to(ax.x_axis, RIGHT, buff=0.15)
        pa, pb = path(-2.0), path(2.0)
        ball_a = Dot(ax.c2p(pa[0], g(pa[0])), color=GREEN_C, radius=0.14)
        ball_b = Dot(ax.c2p(pb[0], g(pb[0])), color=ORANGE_C, radius=0.14)
        sa = boxed(Tex(r"start $w = -2$", color=GREEN_C, font_size=34)).next_to(ball_a, RIGHT, buff=0.2)
        sb = boxed(Tex(r"start $w = 2$", color=ORANGE_C, font_size=34)).next_to(ball_b, LEFT, buff=0.2)
        self.add(ax, curve, lab, wl, ball_a, ball_b, sa, sb)
        self.wait(0.6)
        self.snap()
        self.play(FadeOut(sa), FadeOut(sb), run_time=0.3)
        for i in range(1, STEPS + 1):
            self.play(ball_a.animate.move_to(ax.c2p(pa[i], g(pa[i]))),
                      ball_b.animate.move_to(ax.c2p(pb[i], g(pb[i]))), run_time=0.22 if i < 6 else 0.08,
                      rate_func=linear)
            if i == 2:
                self.snap()
        self.wait(0.3)
        self.snap()
        ga = boxed(Tex(r"global minimum\\ $w = -1.47$, $g = -5.44$", color=GREEN_C, font_size=32))
        ga.move_to(ax.c2p(-1.45, 3.2))
        arr = Arrow(ga.get_bottom(), ball_a.get_top(), buff=0.12, color=GREEN_C, stroke_width=4)
        gb = boxed(Tex(r"local minimum\\ $w = 1.35$, $g = -2.62$", color=ORANGE_C, font_size=32))
        gb.next_to(ball_b, DOWN, buff=0.25)
        note = boxed(Tex(r"slope 0 at both: gradient descent\\ stops wherever it lands first",
                         color=BLACK, font_size=34)).to_corner(UR, buff=0.4)
        self.play(FadeIn(ga), FadeIn(arr), FadeIn(gb), FadeIn(note))
        self.wait(1.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, hgt = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * hgt + gap), "white")
    for i, fr in enumerate(frames[:4]):
        sheet.paste(fr.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (hgt + gap)))
    sheet.save(out)


if __name__ == "__main__":
    assert abs(path(-2.0)[-1] + 1.473) < 1e-3 and abs(path(2.0)[-1] - 1.347) < 1e-3
    name = "two_starts"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = TwoStarts()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
