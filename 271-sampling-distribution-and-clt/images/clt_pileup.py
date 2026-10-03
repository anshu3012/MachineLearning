"""Sample means pile up into a bell: samples of n = 30 from a skewed exponential(1) population; each sample's
mean drops into a histogram, which approaches the normal curve N(1, 1/30) of the central limit theorem.
Run: python clt_pileup.py  -> clt_pileup.mp4, clt_pileup.gif, clt_pileup_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
N, TOTAL = 30, 2000
rng = np.random.default_rng(42)
SAMPLES = rng.exponential(1, (TOTAL, N))
MEANS = SAMPLES.mean(axis=1)
EDGES = np.arange(0.35, 1.70, 0.05)
UNIT = 3.6 / 240                                      # bar height per mean (peak count is about 225)


class CLTPileup(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def bars(self, k):
        counts, _ = np.histogram(MEANS[:k], EDGES)
        group = VGroup()
        for left, c in zip(EDGES[:-1], counts):
            x0, x1 = self.right.c2p(left, 0), self.right.c2p(left + 0.05, 0)
            h = max(c * UNIT, 0.001)
            group.add(Rectangle(width=x1[0] - x0[0], height=h, stroke_color=GREEN_C, stroke_width=1.5,
                                fill_color=GREEN_C, fill_opacity=0.45).move_to(x0, aligned_edge=DL))
        return group

    def caption(self, text):
        return Text(text, font_size=28).to_edge(DOWN, buff=0.35)

    def construct(self):
        self.snaps = []
        # left: the population, an exponential curve
        self.left = Axes(x_range=[0, 4, 1], y_range=[0, 1.1, 0.5], x_length=5, y_length=3.6, tips=False,
                         axis_config={"color": GREY_C}
                         ).to_edge(LEFT, buff=0.6).shift(UP * 0.3)
        curve = self.left.plot(lambda x: np.exp(-x), x_range=[0, 4], color=ORANGE_C, stroke_width=5)
        area = self.left.get_area(curve, x_range=[0, 4], color=ORANGE_C, opacity=0.15)
        ltitle = Text("population: exponential, skewed", font_size=26).next_to(self.left, UP, buff=0.3)
        # right: the histogram of sample means
        self.right = Axes(x_range=[0.25, 1.75, 0.25], y_range=[0, 3.6, 1], x_length=5.6, y_length=3.6, tips=False,
                          y_axis_config={"stroke_opacity": 0},
                          x_axis_config={"color": GREY_C}
                          ).to_edge(RIGHT, buff=0.6).shift(UP * 0.3)
        ticks = VGroup(*[Text(str(v), font_size=22).next_to(self.left.c2p(v, 0), DOWN, buff=0.15) for v in range(5)],
                       *[Text(str(v), font_size=22).next_to(self.right.c2p(v, 0), DOWN, buff=0.15) for v in [0.5, 1, 1.5]])
        self.add(ticks)
        rtitle = Text("means of samples, n = 30", font_size=26).next_to(self.right, UP, buff=0.3)
        cap = self.caption("draw 30 values at random from the population")
        self.play(FadeIn(self.left), Create(curve), FadeIn(area), FadeIn(ltitle), FadeIn(self.right),
                  FadeIn(rtitle), FadeIn(cap))
        hist = self.bars(0)
        self.add(hist)

        # the first three samples, one at a time
        for i in range(3):
            xs = np.clip(SAMPLES[i], 0, 3.95)
            dots = VGroup(*[Dot(self.left.c2p(x, 0.04 + 0.05 * (j % 3)), radius=0.06, color=BLUE_C)
                            for j, x in enumerate(xs)])
            self.play(FadeIn(dots, lag_ratio=0.03), run_time=0.9)
            m = MEANS[i]
            line = DashedLine(self.left.c2p(min(m, 3.95), 0), self.left.c2p(min(m, 3.95), 0.95), color=GREEN_C)
            label = Text(f"mean {m:.2f}", font_size=24, color=GREEN_C).next_to(line, UP, buff=0.1)
            new_cap = self.caption(f"sample {i + 1}: its mean drops into the histogram")
            self.play(Create(line), FadeIn(label), Transform(cap, new_cap), run_time=0.7)
            token = Dot(line.get_end(), radius=0.09, color=GREEN_C)
            new_hist = self.bars(i + 1)
            self.play(token.animate.move_to(self.right.c2p(m, 0)), run_time=0.8)
            self.play(Transform(hist, new_hist), FadeOut(token), run_time=0.3)
            if i == 0:
                self.snap()
            self.play(FadeOut(dots), FadeOut(line), FadeOut(label), run_time=0.4)

        # many more samples, faster
        self.play(Transform(cap, self.caption("repeat: 50, then 300, then 2000 sample means")), run_time=0.5)
        for k in [50, 300]:
            self.play(Transform(hist, self.bars(k)), run_time=1.0)
            self.wait(0.3)
        self.snap()
        self.play(Transform(hist, self.bars(TOTAL)), run_time=1.2)
        self.wait(0.3)
        self.snap()

        # the normal curve predicted by the CLT
        sd = 1 / np.sqrt(N)
        scale = TOTAL * 0.05 * UNIT                     # density -> bar height
        bell = self.right.plot(lambda x: scale * np.exp(-0.5 * ((x - 1) / sd) ** 2) / (sd * np.sqrt(2 * np.pi)),
                               x_range=[0.25, 1.75], color=BLACK, stroke_width=4)
        self.play(Create(bell), Transform(cap, self.caption("skewed population, yet the means are close to normal: N(1, 1/30)")),
                  run_time=1.5)
        self.wait(2)
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
                     "output_file": "clt_pileup", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = CLTPileup()
        scene.render()
    mp4 = HERE / "clt_pileup.mp4"
    shutil.copy(next(media.rglob("clt_pileup.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "clt_pileup.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "clt_pileup_frames.png")
    shutil.rmtree(media)
