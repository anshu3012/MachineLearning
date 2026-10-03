"""Bayesian optimisation in one dimension: accuracy as an unknown function of max_depth. After three trials, a
Gaussian process guesses the curve (line) and its uncertainty (band); the next trial goes where the expected
improvement is highest; the guess is updated; repeat. At the end the hidden curve is revealed.
Run: python bayes_search.py  -> bayes_search.mp4, bayes_search.gif, bayes_search_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image, ImageOps
from scipy.interpolate import CubicSpline
from scipy.stats import norm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, GREY_C, RED_C = "#4C78A8", "#F58518", "#54A24B", "#6B6B6B", "#E45756"
Text.set_default(color=BLACK, font="Latin Modern Roman")

TRUE = CubicSpline([1, 5, 10, 15, 19, 25], [70, 85, 65, 84, 89, 76])      # the hidden curve (unknown to the search)
D = np.linspace(1, 25, 241)


def fit(xs):
    gp = GaussianProcessRegressor(RBF(3.0), optimizer=None, normalize_y=True, alpha=1e-6)
    gp.fit(np.array(xs)[:, None], TRUE(xs))
    mu, sd = gp.predict(D[:, None], return_std=True)
    best = TRUE(xs).max()
    z = (mu - best) / np.maximum(sd, 1e-9)
    ei = (mu - best) * norm.cdf(z) + sd * norm.pdf(z)
    return mu, sd, D[ei.argmax()]


class BayesSearch(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, title, sub):
        return VGroup(Text(title, font_size=26, weight=BOLD), Text(sub, font_size=20, color=GREY_C)
                      ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).to_corner(UR, buff=0.4).shift(DOWN * 0.7)

    def construct(self):
        self.snaps = []
        ax = Axes(x_range=[0, 26, 5], y_range=[50, 100, 10], x_length=7.2, y_length=5.2, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 22,
                               "decimal_number_config": {"num_decimal_places": 0, "color": BLACK}}
                  ).to_edge(LEFT, buff=0.8).shift(UP * 0.1)
        xl = Text("max_depth", font_size=22).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = Text("accuracy (%)", font_size=22).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.5)
        heading = Text("Bayesian search", font_size=34, weight=BOLD).to_corner(UR, buff=0.4)
        self.add(ax, xl, yl, heading)

        def pts(xs, colour=BLACK):
            return VGroup(*[Dot(ax.c2p(x, float(TRUE(x))), radius=0.09, color=colour) for x in xs])

        def guess(mu, sd):
            upper = [ax.c2p(x, min(m + 2 * s, 100)) for x, m, s in zip(D, mu, sd)]
            lower = [ax.c2p(x, max(m - 2 * s, 50)) for x, m, s in zip(D, mu, sd)]
            band = Polygon(*upper, *lower[::-1], stroke_width=0, fill_color=BLUE_C, fill_opacity=0.18)
            line = VMobject(color=BLUE_C, stroke_width=4).set_points_smoothly(
                [ax.c2p(x, m) for x, m in zip(D, mu)])
            return VGroup(band, line)

        xs = [5.0, 10.0, 15.0]
        cap = self.caption("1. Three trials", "max_depth 5, 10, 15: three points on the hidden curve")
        dots = pts(xs)
        self.play(FadeIn(cap), LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.4))
        self.wait(0.6)
        self.snap()

        mu, sd, nxt = fit(xs)
        g = guess(mu, sd)
        self.play(FadeIn(g), Transform(cap, self.caption("2. Guess the curve",
                                                         "line: best guess; band: how unsure we are")))
        self.wait(0.6)
        for k in range(4):
            arrow = Arrow(ax.c2p(nxt, 99), ax.c2p(nxt, 93), color=ORANGE_C, buff=0, stroke_width=6)
            sub = "high guess or wide band: most expected improvement"
            self.play(GrowArrow(arrow), Transform(cap, self.caption(f"3. Next trial: max_depth {nxt:.0f}", sub)))
            self.wait(0.5)
            if k == 0:
                self.snap()
            xs.append(round(float(nxt)))
            new = Dot(ax.c2p(xs[-1], float(TRUE(xs[-1]))), radius=0.09, color=ORANGE_C)
            self.play(GrowFromCenter(new), FadeOut(arrow))
            dots.add(new)
            mu, sd, nxt = fit(xs)
            self.play(Transform(g, guess(mu, sd)), new.animate.set_color(BLACK), Transform(cap, self.caption(
                "4. Update the guess", f"{len(xs)} trials so far")))
            self.wait(0.4)
            if k == 2:
                self.snap()
        truth = ax.plot(lambda x: float(TRUE(x)), x_range=[1, 25], color=GREEN_C, stroke_width=4)
        best = max(xs, key=lambda x: TRUE(x))
        ring = Circle(radius=0.2, color=RED_C, stroke_width=5).move_to(ax.c2p(best, float(TRUE(best))))
        self.play(Create(truth), Create(ring), Transform(cap, self.caption(
            f"Best after {len(xs)} trials: max_depth {best}", "green: the hidden curve, revealed")))
        self.wait(1.5)
        self.snap()


def key_frames_grid(frames, out, gap=16, pad=20):
    boxes = [ImageOps.invert(f.convert("RGB")).getbbox() for f in frames[:4]]
    l, t = min(b[0] for b in boxes) - pad, min(b[1] for b in boxes) - pad
    r, b_ = max(b[2] for b in boxes) + pad, max(b[3] for b in boxes) + pad
    W, H = frames[0].size
    frames = [f.crop((max(l, 0), max(t, 0), min(r, W), min(b_, H))) for f in frames]
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "bayes_search", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = BayesSearch()
        scene.render()
    mp4 = HERE / "bayes_search.mp4"
    shutil.copy(next(media.rglob("bayes_search.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "bayes_search.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "bayes_search_frames.png")
    shutil.rmtree(media)
