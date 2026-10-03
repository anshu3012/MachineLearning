"""Box-Cox on the concrete Age column: as lambda moves, the histogram changes shape; the learned lambda gives the most normal one.
Run: python lambda_sweep.py  -> lambda_sweep.mp4, lambda_sweep.gif, lambda_sweep_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
from manim import *
from PIL import Image
from scipy import stats
from sklearn.model_selection import train_test_split

HERE = Path(__file__).parent
BLUE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")

# the Age column of the training set, exactly as in the Notebook
df = pd.read_csv(HERE.parent / "data" / "concrete_data.csv")
X_train, *_ = train_test_split(df.drop(columns=["Strength"]), df["Strength"], test_size=0.2, random_state=42)
AGE = X_train["Age"].values.astype(float)
LEARNED = stats.boxcox(AGE)[1]          # the lambda PowerTransformer(method="box-cox") learns: 0.067
EDGES = np.arange(-5, 5.51, 0.5)        # histogram bins on the standardised scale
WIDTH = EDGES[1] - EDGES[0]


def standardised(lam):
    t = stats.boxcox(AGE, lam)
    return (t - t.mean()) / t.std()


class LambdaSweep(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, text):
        return Text(text, font_size=30, color=GREY_C).to_edge(DOWN, buff=0.35)

    def construct(self):
        self.snaps = []
        ax = Axes(x_range=[-5, 5.5, 1], y_range=[0, 0.5, 0.1], x_length=11, y_length=4.6,
                  axis_config={"color": GREY_C, "include_ticks": True}).shift(UP * 0.3)
        ticks = VGroup(*[Text(f"{v}".replace("-", "−"), font_size=24, color=GREY_C).next_to(ax.c2p(v, 0), DOWN, buff=0.15)
                         for v in range(-4, 6, 2)])
        xlabel = Text("standardised value", font_size=24, color=GREY_C).next_to(ticks, DOWN, buff=0.12)
        normal = ax.plot(lambda z: WIDTH * stats.norm.pdf(z), x_range=[-4, 4], color=RED_C, stroke_width=4)
        lam = ValueTracker(1.0)

        def bars():
            z = standardised(lam.get_value())
            share = np.histogram(np.clip(z, -4.99, 5.49), EDGES)[0] / len(z)
            colour = GREEN_C if abs(lam.get_value() - LEARNED) < 0.01 else BLUE_C
            return VGroup(*[Rectangle(width=ax.x_axis.unit_size * WIDTH * 0.92,
                                      height=max(ax.y_axis.unit_size * min(s, 0.5), 0.001),
                                      stroke_width=0, fill_color=colour, fill_opacity=0.6)
                            .move_to(ax.c2p(e + WIDTH / 2, 0), aligned_edge=DOWN)
                            for e, s in zip(EDGES[:-1], share)])

        hist = always_redraw(bars)
        lam_text = always_redraw(lambda: Text(f"λ = {lam.get_value():.2f}".replace("-", "−"), font_size=40, weight=BOLD)
                                 .to_corner(UL, buff=0.4))
        skew_text = always_redraw(lambda: Text(f"skewness {pd.Series(stats.boxcox(AGE, lam.get_value())).skew():.2f}".replace("-", "−"),
                                               font_size=32, color=GREY_C).next_to(lam_text, DOWN, aligned_edge=LEFT))
        title = Text("Box-Cox on Age", font_size=34).to_corner(UR, buff=0.4)
        legend = Text("red: normal curve", font_size=24, color=RED_C).next_to(title, DOWN, aligned_edge=RIGHT)

        cap = self.caption("λ = 1: shape unchanged, long right tail")
        self.add(ax, ticks, xlabel, hist, normal, lam_text, skew_text, title, legend, cap)
        self.wait(1.2)
        self.snap()
        steps = [(0.5, "λ = 0.5: like a square root, tail shorter"),
                 (-0.5, "λ = −0.5: too far, now a left tail"),
                 (LEARNED, f"λ = {LEARNED:.3f}: the value PowerTransformer learns")]
        for value, text in steps:
            self.play(lam.animate.set_value(value), Transform(cap, self.caption(text)), run_time=2.5, rate_func=smooth)
            self.wait(1.2)
            self.snap()
        self.wait(1)


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "lambda_sweep", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = LambdaSweep()
        scene.render()
    mp4 = HERE / "lambda_sweep.mp4"
    shutil.copy(next(media.rglob("lambda_sweep.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "lambda_sweep.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "lambda_sweep_frames.png")
    shutil.rmtree(media)
