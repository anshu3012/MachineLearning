"""How a regression tree finds its first split: slide a threshold, predict each side's mean, add up the squared errors.
Run: python sse_sweep.py  -> sse_sweep.mp4, sse_sweep.gif, sse_sweep_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C = "#4C78A8", "#F58518", "#54A24B", "#E45756"
Text.set_default(color=BLACK, font="Latin Modern Roman")

df = pd.read_csv(HERE.parent / "data" / "exam_day.csv")
h, m = df["hours"].to_numpy(), df["marks"].to_numpy()
xs = np.unique(h)
CANDS = (xs[:-1] + xs[1:]) / 2                       # midpoints between neighbouring hours


def sse(t):
    left, right = m[h <= t], m[h > t]
    return ((left - left.mean()) ** 2).sum() + ((right - right.mean()) ** 2).sum()


SSE = np.array([sse(t) for t in CANDS])
BEST = int(SSE.argmin())


class SSESweep(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 100, 20], x_length=6.2, y_length=4.6, tips=False,
                  axis_config=dict(color=GREY_D, include_numbers=True, font_size=26,
                                   decimal_number_config=dict(num_decimal_places=0, color=BLACK))).to_corner(DL, buff=0.7).shift(UP * 0.45)
        ax2 = Axes(x_range=[0, 10, 2], y_range=[0, 10000, 2000], x_length=4.6, y_length=4.2, tips=False,
                   axis_config=dict(color=GREY_D, include_numbers=True, font_size=22,
                                    decimal_number_config=dict(num_decimal_places=0, color=BLACK))).to_corner(DR, buff=0.5).shift(UP * 0.45)
        labels = VGroup(Text("hours", font_size=24).next_to(ax.x_axis, DOWN, buff=0.4),
                        Text("marks", font_size=24).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.5),
                        Text("threshold", font_size=24).next_to(ax2.x_axis, DOWN, buff=0.4),
                        Text("SSE", font_size=24).next_to(ax2.y_axis.get_top(), RIGHT, buff=0.45))
        pts = VGroup(*[Cross(scale_factor=0.09, stroke_color=BLUE_C, stroke_width=4).move_to(ax.c2p(a, b))
                       for a, b in zip(h, m)])
        self.add(ax, ax2, labels, pts)
        title = Text("Try every threshold: each side predicts its mean;", font_size=28).to_edge(UP, buff=0.3)
        title2 = Text("score = sum of squared errors (SSE)", font_size=28).next_to(title, DOWN, buff=0.12)
        self.add(title, title2)

        k = ValueTracker(0)

        def idx():
            return int(round(k.get_value()))

        def split_lines():
            t = CANDS[idx()]
            left, right = m[h <= t], m[h > t]
            g = VGroup(DashedLine(ax.c2p(t, 0), ax.c2p(t, 100), color=BLACK, stroke_width=3),
                       Line(ax.c2p(0, left.mean()), ax.c2p(t, left.mean()), color=ORANGE_C, stroke_width=6),
                       Line(ax.c2p(t, right.mean()), ax.c2p(10, right.mean()), color=GREEN_C, stroke_width=6))
            for a, b in zip(h, m):                   # residuals: distance from each point to its side's mean
                mean = left.mean() if a <= t else right.mean()
                g.add(Line(ax.c2p(a, b), ax.c2p(a, mean), color=RED_C, stroke_width=2))
            return g

        def curve():
            i = idx()
            dots = VGroup(*[Dot(ax2.c2p(CANDS[j], SSE[j]), radius=0.05, color=BLACK) for j in range(i + 1)])
            if i > 0:
                dots.add(VMobject(color=BLACK, stroke_width=3).set_points_as_corners(
                    [ax2.c2p(CANDS[j], SSE[j]) for j in range(i + 1)]))
            return dots

        def readout():
            return Text(f"threshold {CANDS[idx()]:.2f}:  SSE = {SSE[idx()]:,.0f}", font_size=26) \
                .next_to(ax2, UP, buff=0.3).align_to(ax2, LEFT).shift(LEFT * 0.6)

        lines, sse_curve, text = always_redraw(split_lines), always_redraw(curve), always_redraw(readout)
        self.add(lines, sse_curve, text)
        self.wait(0.8)
        self.snap()
        self.play(k.animate.set_value(BEST - 3), run_time=3, rate_func=linear)
        self.wait(0.4)
        self.snap()
        self.play(k.animate.set_value(len(CANDS) - 1), run_time=4, rate_func=linear)
        self.wait(0.3)
        self.play(k.animate.set_value(BEST), run_time=2)
        lines.clear_updaters()
        sse_curve.clear_updaters()
        text.clear_updaters()
        ring = Circle(radius=0.16, color=RED_C, stroke_width=5).move_to(ax2.c2p(CANDS[BEST], SSE[BEST]))
        best = Text(f"minimum: split at hours ≤ {CANDS[BEST]:.2f}", font_size=26, color=RED_C) \
            .next_to(ax2, UP, buff=0.3).align_to(ax2, LEFT).shift(LEFT * 0.6)
        self.play(Create(ring), FadeOut(text), FadeIn(best))
        self.wait(1.2)
        self.snap()
        # The full curve for reference in the last key frame
        full = VMobject(color=GREY_D, stroke_width=3).set_points_as_corners([ax2.c2p(c, s) for c, s in zip(CANDS, SSE)])
        self.play(Create(full))
        self.wait(1)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, hgt = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * hgt + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (hgt + gap)))
    sheet.save(out)


if __name__ == "__main__":
    print("candidates", len(CANDS), "best", CANDS[BEST], "SSE", round(SSE[BEST], 1))
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "sse_sweep", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = SSESweep()
        scene.render()
    mp4 = HERE / "sse_sweep.mp4"
    shutil.copy(next(media.rglob("sse_sweep.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "sse_sweep.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "sse_sweep_frames.png")
    shutil.rmtree(media)
