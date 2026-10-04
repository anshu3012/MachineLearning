"""The standardized perceptron of Section 8 (z = 5.82 x1 + 1.48 x2 + 1 on scaled CGPA and resume score) applied to
three students of data/placement.csv: inputs flow in, the weighted sum z fills a bar, the step fires, and the student
lands on the plane in the predicted colour. Then all 100 students and the line z = 0 with its two regions.
Run: python perceptron_fire.py  -> perceptron_fire.gif, perceptron_fire_frames.png"""
import glob
import shutil
import subprocess
from pathlib import Path

import manimpango
import numpy as np
import pandas as pd
from manim import *
from PIL import Image
from sklearn.linear_model import Perceptron
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).parent
# topgro: ~/.fonts links are broken, so register the TeX copy of Latin Modern for Pango
for f in glob.glob("/usr/share/texmf/fonts/opentype/public/lm/lmroman*.otf"):
    manimpango.register_font(f)
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MarkupText.set_default(color=BLACK, font="Latin Modern Roman")

df = pd.read_csv(HERE.parent / "data" / "placement.csv")
X, y = df[["cgpa", "resume_score"]], df["placed"].to_numpy()
model = make_pipeline(StandardScaler(), Perceptron(random_state=0)).fit(X, y)
S = model[0].transform(X)
(W1, W2), B = model[-1].coef_[0], model[-1].intercept_[0]
Z = S @ np.array([W1, W2]) + B
SHOW = [0, 1, 3]                     # z = 6.63 (placed), -5.70 (not), 1.19 (close to the line)

IN_X, SUM_X, STEP_X = -5.0, -2.9, -0.9
IN_Y = [1.4, 0.0, -1.4]
SUM_P = np.array([SUM_X, 0, 0])
ZSCALE = 0.17                        # bar length per unit of z


class PerceptronFire(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        # left: the perceptron
        ins = [Circle(0.48, stroke_color=c, stroke_width=4, fill_color=WHITE, fill_opacity=1).move_to([IN_X, yy, 0])
               for c, yy in zip([BLUE_C, BLUE_C, GREY_C], IN_Y)]
        in_lab = [Text(t, font_size=28, color=GREY_C).next_to(c, LEFT, buff=0.12) for t, c in
                  zip(["CGPA", "resume", "bias"], ins)]
        summ = Circle(0.45, stroke_color=ORANGE_C, stroke_width=5, fill_color=WHITE, fill_opacity=1).move_to(SUM_P)
        sig = Text("Σ", color=ORANGE_C, font_size=40).move_to(summ)
        edges = [Line(c.get_center(), SUM_P, buff=0.4, stroke_color=GREY_C, stroke_width=3) for c in ins]
        wlab = [Text(t, font_size=30, color=PURPLE_C).move_to(e.point_from_proportion(0.5) + UP * 0.3)
                for t, e in zip([f"{W1:.2f}", f"{W2:.2f}", f"{B:.0f}"], edges)]
        step_ax = Axes(x_range=[-12, 12, 12], y_range=[0, 1, 1], x_length=1.6, y_length=1.2, tips=False,
                       axis_config={"color": GREY_C, "stroke_width": 2}).move_to([STEP_X, 0, 0])
        step = VGroup(Line(step_ax.c2p(-12, 0), step_ax.c2p(0, 0)), Line(step_ax.c2p(0, 1), step_ax.c2p(12, 1))
                      ).set_stroke(GREEN_C, 5)
        step_box = SurroundingRectangle(step_ax, color=GREEN_C, buff=0.15, corner_radius=0.1)
        step_lab = Text("step", font_size=30, color=GREEN_C).next_to(step_box, UP, buff=0.08)
        to_step = Arrow(summ.get_right(), step_box.get_left(), buff=0.08, color=ORANGE_C, stroke_width=4)
        bar_base = DashedLine(SUM_P + DOWN * 2.3 + LEFT * 2.0, SUM_P + DOWN * 2.3 + RIGHT * 2.0, color=GREY_C,
                              stroke_width=2)
        zero_tick = VGroup(Line(SUM_P + DOWN * 2.1, SUM_P + DOWN * 2.5, color=BLACK, stroke_width=3),
                           Text("z = 0", font_size=24, color=GREY_C).move_to(SUM_P + DOWN * 2.8))
        net = VGroup(*edges, *ins, *in_lab, summ, sig, *wlab, step_ax, step, step_box, step_lab, to_step,
                     bar_base, zero_tick)

        # right: the plane of scaled inputs
        ax = Axes(x_range=[-2, 2.5, 1], y_range=[-2.5, 2.5, 1], x_length=4.6, y_length=5.0, tips=False,
                  axis_config={"color": GREY_C, "stroke_width": 2, }
                  ).move_to([4.3, -0.4, 0])
        ax_lab = VGroup(Text("CGPA (scaled)", font_size=28, color=GREY_C).next_to(ax, DOWN, buff=0.1),
                        Text("resume (scaled)", font_size=28, color=GREY_C).rotate(PI / 2).next_to(ax, LEFT, buff=0.1))
        title = MarkupText(f"z = {W1:.2f} x<sub>1</sub> + {W2:.2f} x<sub>2</sub> + {B:.0f}, then step",
                           font_size=36).to_edge(UP, buff=0.25)
        self.play(FadeIn(title), FadeIn(net), Create(ax), FadeIn(ax_lab), run_time=1.2)

        dots = VGroup()
        for k, i in enumerate(SHOW):
            s1, s2, z = S[i, 0], S[i, 1], Z[i]
            out = int(z >= 0)
            colour = GREEN_C if out else RED_C
            card = Text(f"student {i + 1}: CGPA {X.cgpa[i]:.2f}, resume {X.resume_score[i]:.2f}", font_size=28,
                        color=BLUE_C).move_to([-3.4, 2.5, 0])
            vals = [Text(f"{v:.2f}", font_size=26).move_to(c) for v, c in zip([s1, s2, 1.0], ins)]
            self.play(FadeIn(card), *[FadeIn(v, scale=0.6) for v in vals], run_time=0.7)
            pulses = [Dot(c.get_center(), radius=0.09, color=ORANGE_C) for c in ins]
            self.play(*[MoveAlongPath(p, e) for p, e in zip(pulses, edges)], run_time=0.8)
            bar = Rectangle(width=max(abs(z) * ZSCALE, 0.02), height=0.35, stroke_width=0, fill_color=colour,
                            fill_opacity=0.85)
            bar.move_to(SUM_P + DOWN * 2.3, aligned_edge=LEFT if z >= 0 else RIGHT)
            zt = Text(f"z = {z:.2f}", font_size=34, color=colour).move_to(SUM_P + DOWN * 1.65)
            bar0 = bar.copy().stretch(0.01, 0, about_edge=LEFT if z >= 0 else RIGHT)
            self.add(bar0)
            self.play(FadeOut(*pulses), Transform(bar0, bar), FadeIn(zt), run_time=0.9)
            fire = Dot(step_ax.c2p(np.clip(z, -11.5, 11.5), out), radius=0.12, color=colour)
            out_t = Text(f"output {out}", font_size=32, color=colour).next_to(step_box, DOWN, buff=0.15)
            self.play(GrowArrow(to_step.copy().set_color(colour)), FadeIn(fire, scale=2), FadeIn(out_t), run_time=0.7)
            d = Dot(ax.c2p(s1, s2), radius=0.12, color=colour)
            ring = Circle(0.26, color=colour, stroke_width=4).move_to(d)
            self.play(TransformFromCopy(fire, d), Create(ring), run_time=0.8)
            dots.add(d)
            self.wait(0.6)
            self.snap()
            self.play(FadeOut(card), *[FadeOut(v) for v in vals], FadeOut(bar0), FadeOut(zt), FadeOut(fire),
                      FadeOut(out_t), FadeOut(ring), run_time=0.5)

        # all 100 students, then the line z = 0 and its regions
        rest = VGroup(*[Dot(ax.c2p(*S[i]), radius=0.07, color=GREEN_C if Z[i] >= 0 else RED_C)
                        for i in range(len(S)) if i not in SHOW])
        msg = Text("all 100 students, coloured by output", font_size=28, color=GREY_C).move_to([-3.4, 2.5, 0])
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in rest], lag_ratio=0.02), FadeIn(msg), run_time=1.8)
        xa, xb = (-B - W2 * 2.5) / W1, (-B + W2 * 2.5) / W1          # where the line meets y = 2.5 and y = -2.5
        line = Line(ax.c2p(xa, 2.5), ax.c2p(xb, -2.5), color=BLACK, stroke_width=5)
        corners_pos = [ax.c2p(xa, 2.5), ax.c2p(2.5, 2.5), ax.c2p(2.5, -2.5), ax.c2p(xb, -2.5)]
        corners_neg = [ax.c2p(-2, 2.5), ax.c2p(xa, 2.5), ax.c2p(xb, -2.5), ax.c2p(-2, -2.5)]
        reg = VGroup(Polygon(*corners_pos, stroke_width=0, fill_color=GREEN_C, fill_opacity=0.15),
                     Polygon(*corners_neg, stroke_width=0, fill_color=RED_C, fill_opacity=0.15))
        reg_lab = VGroup(Text("z < 0", font_size=28, color=RED_C).next_to(ax.c2p(-1.2, 2.5), UP, buff=0.1),
                         Text("z ≥ 0", font_size=28, color=GREEN_C).next_to(ax.c2p(1.5, 2.5), UP, buff=0.1))
        # true labels: the 3 students the line gets wrong change colour
        truth = [d.animate.set_color(GREEN_C if y[i] else RED_C) for i, d in
                 zip([j for j in range(len(S)) if j not in SHOW], rest)]
        wrong = [j for j in range(len(S)) if int(Z[j] >= 0) != y[j]]
        rings = VGroup(*[Circle(0.2, color=BLACK, stroke_width=3).move_to(ax.c2p(*S[j])) for j in wrong])
        msg2 = Text(f"true labels: {len(S) - len(wrong)} of 100 correct", font_size=28,
                    color=BLACK).move_to([-3.4, 2.5, 0])
        self.add(reg)
        self.bring_to_back(reg)
        self.play(Create(line), FadeIn(reg), FadeIn(reg_lab), run_time=1.2)
        self.play(*truth, Create(rings), FadeOut(msg), FadeIn(msg2), run_time=1.0)
        self.wait(2.5)
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
                     "output_file": "perceptron_fire", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = PerceptronFire()
        scene.render()
    mp4 = next(media.rglob("perceptron_fire.mp4"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "perceptron_fire.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "perceptron_fire_frames.png")
    shutil.rmtree(media)
