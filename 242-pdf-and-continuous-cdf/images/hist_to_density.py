"""Density histograms of 100,000 CGPAs with ever narrower bins settle onto the smooth PDF curve.
Run: python hist_to_density.py -> hist_to_density.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREY_C = "#4C78A8", "#F58518", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
CGPA = stats.beta(7, 3, scale=10)
SAMPLE = CGPA.rvs(100_000, random_state=np.random.default_rng(42))
WIDTHS = [2, 1, 0.5, 0.1]


class HistToDensity(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, title, detail):
        return VGroup(Text(title, font_size=34, weight=BOLD), Text(detail, font_size=26, color=GREY_C)
                      ).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.3)

    def bars(self, ax, width):
        edges = np.arange(0, 10 + width / 2, width)
        dens, _ = np.histogram(SAMPLE, bins=edges, density=True)     # bar area = share of the data
        out = VGroup()
        for lo, d in zip(edges[:-1], dens):
            p0, p1 = ax.c2p(lo, 0), ax.c2p(lo + width, max(d, 1e-4))
            out.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=BLUE_C, fill_opacity=0.75,
                              stroke_color=WHITE, stroke_width=1 if width >= 0.25 else 0.3)
                    .move_to((p0 + p1) / 2))
        return out

    def construct(self):
        self.snaps = []
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 0.35, 0.1], x_length=11, y_length=4.8,
                  axis_config={"color": GREY_C, "include_tip": False, "font_size": 30},
                  x_axis_config={"numbers_to_include": range(0, 11)},
                  y_axis_config={"numbers_to_include": [0, 0.1, 0.2, 0.3],
                                 "decimal_number_config": {"num_decimal_places": 1}}).shift(DOWN * 0.8)
        for n in list(ax.x_axis.numbers) + list(ax.y_axis.numbers):
            n.set_color(GREY_C)
        xl = Text("CGPA", font_size=26, color=GREY_C).next_to(ax.x_axis, DOWN, buff=0.55)
        yl = Text("density", font_size=26, color=GREY_C).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.55)
        hist = self.bars(ax, WIDTHS[0])
        cap = self.caption("Density histogram, bin width 2", "bar height = share of students in the bin / bin width")
        self.play(Create(ax), FadeIn(xl, yl), FadeIn(hist, lag_ratio=0.1), FadeIn(cap), run_time=1.5)
        self.wait(0.6)
        self.snap()
        for w in WIDTHS[1:]:
            new = self.bars(ax, w)
            detail = "the bars hug a smooth curve" if w == WIDTHS[-1] else "the total area of the bars is still 1"
            self.play(Transform(hist, new), Transform(cap, self.caption(f"Bin width {w}", detail)), run_time=1.4)
            self.wait(0.5)
            if w != 0.5:
                self.snap()
        curve = ax.plot(lambda x: CGPA.pdf(x), x_range=[0, 10, 0.02], color=ORANGE_C, stroke_width=7)
        self.play(Create(curve), Transform(cap, self.caption("The limit is the PDF f(x)",
                                                              "height = probability density, area = probability")),
                  run_time=1.6)
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
                     "output_file": "hist_to_density", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = HistToDensity()
        scene.render()
    mp4 = HERE / "hist_to_density.mp4"
    shutil.copy(next(media.rglob("hist_to_density.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "hist_to_density.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "hist_to_density_frames.png")
    shutil.rmtree(media)
