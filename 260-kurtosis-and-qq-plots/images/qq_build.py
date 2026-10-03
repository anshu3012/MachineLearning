"""Building a Q-Q plot from percentiles: the 150 iris sepal lengths and 1,000 values from a standard normal
distribution are sorted, their deciles are matched in pairs, and each pair becomes one point; then all 99 percentiles.
Run: python qq_build.py -> qq_build.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
from sklearn.datasets import load_iris

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
DATA = np.sort(load_iris().data[:, 0])                          # sepal length (cm), 150 flowers
THEO = np.sort(np.random.default_rng(42).normal(0, 1, 1000))    # theoretical sample: standard normal
DEC = np.arange(10, 100, 10)
PCT = np.arange(1, 100)


class QQBuild(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, title, detail):
        return VGroup(Text(title, font_size=32, weight=BOLD), Text(detail, font_size=24, color=GREY_C)
                      ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.25)

    def strip(self, values, lo, hi, step, colour, label, y):
        line = NumberLine(x_range=[lo, hi, step], length=5.6, color=GREY_C, include_numbers=True, font_size=22,
                          include_tip=False).move_to([-3.6, y, 0])
        for n in line.numbers:
            n.set_color(GREY_C)
        values = values[(values >= lo) & (values <= hi)]          # keep the dots on the drawn line
        jitter = np.random.default_rng(1).uniform(0.12, 0.55, len(values))
        dots = VGroup(*[Dot(line.n2p(v) + UP * j, radius=0.03, color=colour, fill_opacity=0.55)
                        for v, j in zip(values, jitter)])
        name = Text(label, font_size=22, color=colour).next_to(line, UP, buff=0.75)
        return line, dots, name

    def construct(self):
        self.snaps = []
        dline, ddots, dname = self.strip(DATA, 4, 8, 1, BLUE_C, "our data: 150 sepal lengths (cm)", 0.9)
        tline, tdots, tname = self.strip(THEO, -3, 3, 1, ORANGE_C, "theoretical: 1,000 standard normal values", -2.3)
        # x runs 0..6 internally (shown as -3..3) so the y axis sits at the left edge, not in the middle
        ax0 = Axes(x_range=[0, 6, 1], y_range=[4, 8, 1], x_length=5.2, y_length=4.5,
                   axis_config={"color": GREY_C, "include_tip": False, "font_size": 22},
                   y_axis_config={"numbers_to_include": range(4, 9)}).move_to([3.7, -0.55, 0])
        ax0.x_axis.add_labels({i: Text(str(i - 3).replace("-", "−"), font_size=20, color=GREY_C) for i in range(7)})
        ax = ax0
        c2p = ax0.c2p
        ax.c2p = lambda t, d: c2p(t + 3, d)
        for n in list(ax.y_axis.numbers):
            n.set_color(GREY_C)
        xl = Text("theoretical quantiles", font_size=22, color=ORANGE_C).next_to(ax.x_axis, DOWN, buff=0.45)
        yl = Text("data quantiles", font_size=22, color=BLUE_C).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.45)

        cap = self.caption("Step 1: two sorted sets of values", "our data, and data from the distribution we compare with")
        self.play(FadeIn(cap), Create(dline), Create(tline), FadeIn(dname, tname),
                  FadeIn(ddots, lag_ratio=0.01), FadeIn(tdots, lag_ratio=0.002), run_time=2)
        self.play(Create(ax), FadeIn(xl, yl), run_time=1)
        self.wait(0.5)
        self.snap()

        dq, tq = np.percentile(DATA, DEC), np.percentile(THEO, DEC)
        dticks = VGroup(*[Line(dline.n2p(v) + DOWN * 0.15, dline.n2p(v) + UP * 0.65, color=BLUE_C, stroke_width=4)
                          for v in dq])
        tticks = VGroup(*[Line(tline.n2p(v) + DOWN * 0.15, tline.n2p(v) + UP * 0.65, color=ORANGE_C, stroke_width=4)
                          for v in tq])
        self.play(Transform(cap, self.caption("Step 2: the same percentiles of both",
                                              "10th, 20th, ..., 90th percentile (deciles)")),
                  Create(dticks, lag_ratio=0.15), Create(tticks, lag_ratio=0.15), run_time=2)
        self.wait(0.5)
        self.snap()

        self.play(Transform(cap, self.caption("Step 3: pair them up, one point per pair",
                                              "x = theoretical percentile, y = data percentile")), run_time=0.8)
        pts = VGroup()
        for i, (t, d) in enumerate(zip(tq, dq)):
            p = Dot(ax.c2p(t, d), radius=0.08, color=BLUE_C)
            self.play(TransformFromCopy(VGroup(dticks[i], tticks[i]), p), run_time=0.45)
            pts.add(p)
        self.wait(0.5)
        self.snap()

        all_pts = VGroup(*[Dot(ax.c2p(t, d), radius=0.045, color=BLUE_C, fill_opacity=0.8)
                           for t, d in zip(np.percentile(THEO, PCT), np.percentile(DATA, PCT))])
        slope, icpt = np.polyfit(np.percentile(THEO, PCT), np.percentile(DATA, PCT), 1)
        fit = Line(ax.c2p((4.1 - icpt) / slope, 4.1), ax.c2p((7.9 - icpt) / slope, 7.9), color=RED_C, stroke_width=5)
        self.play(Transform(cap, self.caption("Step 4: all 99 percentiles, and a straight line",
                                              "points near the line: the shapes match")),
                  FadeOut(pts), FadeIn(all_pts, lag_ratio=0.02), run_time=2)
        self.play(Create(fit), run_time=1)
        self.wait(1.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "qq_build", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = QQBuild()
        scene.render()
    mp4 = HERE / "qq_build.mp4"
    shutil.copy(next(media.rglob("qq_build.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "qq_build.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "qq_build_frames.png")
    shutil.rmtree(media)
