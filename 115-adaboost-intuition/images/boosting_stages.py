"""AdaBoost on 10 students, stage by stage: each stump's split, its mistakes, its say (alpha), the mistakes growing
(heavier weights) before the next stage, and the final weighted vote of the three stumps.
Run: python boosting_stages.py  -> boosting_stages.mp4, boosting_stages.gif, boosting_stages_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, RED_C, GREY_C, GREEN_C = "#4C78A8", "#F58518", "#E45756", "#6B6B6B", "#54A24B"
LIGHT = {1: "#DCE6F2", -1: "#FDE5CC"}
Text.set_default(color=BLACK, font="Latin Modern Roman")

# 10 students: CGPA and IQ; +1 placed, -1 not placed
CGPA = np.array([2, 3, 1.5, 7, 8.5, 3.5, 6, 8, 8.5, 5.5])
IQ = np.array([120, 90, 78, 125, 120, 55, 90, 70, 100, 62])
Y = np.array([1, 1, 1, 1, 1, -1, -1, -1, -1, -1])
X = np.c_[CGPA, IQ]


def adaboost(rounds=3):
    """Stumps trained on weighted rows; alpha = 1/2 ln((1 - error) / error); w * e^(-alpha y h)."""
    w = np.full(len(Y), 1 / len(Y))
    out = []
    for _ in range(rounds):
        stump = DecisionTreeClassifier(max_depth=1, random_state=0).fit(X, Y, sample_weight=w)
        pred = stump.predict(X)
        err = w[pred != Y].sum()
        alpha = 0.5 * np.log((1 - err) / err)
        out.append(dict(stump=stump, pred=pred, err=err, alpha=alpha, w_before=w.copy()))
        w = w * np.exp(-alpha * Y * pred)
        w = w / w.sum()
        out[-1]["w_after"] = w.copy()
    return out


STAGES = adaboost()


def score(cg, iq):
    return sum(s["alpha"] * s["stump"].predict([[cg, iq]])[0] for s in STAGES)


class BoostingStages(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def region(self, x0, x1, y0, y1, cls, opacity=0.55):
        p0, p1 = self.ax.c2p(x0, y0), self.ax.c2p(x1, y1)
        return Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=LIGHT[cls],
                         fill_opacity=opacity).move_to((p0 + p1) / 2).set_z_index(-2)

    def stump_regions(self, stump):
        t = stump.tree_
        f, thr = t.feature[0], t.threshold[0]
        left = stump.classes_[t.value[1].argmax()]
        right = stump.classes_[t.value[2].argmax()]
        if f == 0:
            regs = [self.region(0, thr, 40, 140, left), self.region(thr, 10, 40, 140, right)]
            line = DashedLine(self.ax.c2p(thr, 40), self.ax.c2p(thr, 140), color=BLACK, stroke_width=4)
            name = f"CGPA {'<' if left == 1 else '>'} {thr:.2f}: placed"
        else:
            regs = [self.region(0, 10, 40, thr, left), self.region(0, 10, thr, 140, right)]
            line = DashedLine(self.ax.c2p(0, thr), self.ax.c2p(10, thr), color=BLACK, stroke_width=4)
            name = f"IQ {'<' if left == 1 else '>'} {thr:.0f}: placed"
        return VGroup(*regs), line, name

    def construct(self):
        self.snaps = []
        self.ax = Axes(x_range=[0, 10, 2], y_range=[40, 140, 20], x_length=6.4, y_length=5.0, tips=False,
                       axis_config=dict(color=GREY_C, include_numbers=True, font_size=24,
                                        decimal_number_config=dict(num_decimal_places=0, color=GREY_C)))
        self.ax.to_edge(LEFT, buff=0.7).shift(DOWN * 0.15)
        labels = VGroup(Text("CGPA", font_size=24).next_to(self.ax.x_axis, DOWN, buff=0.45),
                        Text("IQ", font_size=24).next_to(self.ax.y_axis, UP, buff=0.15))
        title = Text("AdaBoost: three stumps, one after another", font_size=32).to_edge(UP, buff=0.3)
        r0 = 0.13
        dots = VGroup(*[Dot(self.ax.c2p(c, q), radius=r0, color=BLUE_C if y == 1 else ORANGE_C,
                            stroke_color=WHITE, stroke_width=1.5) for c, q, y in zip(CGPA, IQ, Y)])
        legend = VGroup(Dot(color=BLUE_C), Text("placed (+1)", font_size=22), Dot(color=ORANGE_C),
                        Text("not placed (-1)", font_size=22)).arrange(RIGHT, buff=0.15)
        legend[2].shift(RIGHT * 0.25); legend[3].shift(RIGHT * 0.25)
        legend.next_to(title, DOWN, buff=0.15)
        panel = VGroup().move_to(RIGHT * 3.6 + UP * 0.6)
        self.add(title, self.ax, labels, dots, legend)
        self.wait(0.6)
        rows = []
        lines = []
        for k, s in enumerate(STAGES, start=1):
            regs, line, name = self.stump_regions(s["stump"])
            head = Text(f"stage {k}: stump h{k}", font_size=28, weight=BOLD)
            rule = Text(name, font_size=24)
            wrong = np.where(s["pred"] != Y)[0]
            info = Text(f"{len(wrong)} mistakes, error = {s['err']:.3f}", font_size=24, color=RED_C)
            say = MathTex(rf"\alpha_{k} = \tfrac{{1}}{{2}}\ln\tfrac{{1-{s['err']:.3f}}}{{{s['err']:.3f}}} = {s['alpha']:.2f}",
                          font_size=34, color=BLACK)
            box = VGroup(head, rule, info, say).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
            box.move_to(RIGHT * 3.9 + UP * 0.9)
            self.play(FadeIn(regs), Create(line), FadeIn(head), FadeIn(rule), run_time=1.0)
            rings = VGroup(*[Circle(radius=dots[i].radius + 0.1, color=RED_C, stroke_width=5).move_to(dots[i])
                             for i in wrong])
            self.play(Create(rings), FadeIn(info), run_time=0.8)
            self.play(Write(say), run_time=0.8)
            self.wait(0.5)
            # reweight: area of each dot follows its new weight
            grow = Text("mistakes weigh more, the rest less", font_size=24, color=GREY_C).next_to(box, DOWN, buff=0.35)
            ratio = s["w_after"] / s["w_before"]
            anims = [d.animate.scale(np.sqrt(r)) for d, r in zip(dots, ratio)]
            if k < len(STAGES):
                self.play(*anims, FadeIn(grow), FadeOut(rings), run_time=1.2)
            else:
                self.play(FadeOut(rings), run_time=0.4)
            self.wait(0.6)
            if k == 1:
                self.snap()
            rows.append(MathTex(rf"\alpha_{k} = {s['alpha']:.2f}", font_size=32, color=BLACK))
            lines.append(line.copy().set_stroke(color=GREY_C, width=2.5))
            if k in (2, 3):
                self.snap()
            self.play(FadeOut(regs), FadeOut(line), FadeOut(box), FadeOut(grow), run_time=0.5)
        # final: combined regions from the weighted vote
        xs = sorted({0, 10} | {s["stump"].tree_.threshold[0] for s in STAGES if s["stump"].tree_.feature[0] == 0})
        ys = sorted({40, 140} | {s["stump"].tree_.threshold[0] for s in STAGES if s["stump"].tree_.feature[0] == 1})
        cells = VGroup()
        for x0, x1 in zip(xs, xs[1:]):
            for y0, y1 in zip(ys, ys[1:]):
                cells.add(self.region(x0, x1, y0, y1, int(np.sign(score((x0 + x1) / 2, (y0 + y1) / 2))), 0.8))
        a = [s["alpha"] for s in STAGES]
        formula = MathTex(r"H(x) = \operatorname{sign}\big(", f"{a[0]:.2f}", r"\,h_1 + ", f"{a[1]:.2f}", r"\,h_2 + ",
                          f"{a[2]:.2f}", r"\,h_3\big)", font_size=30, color=BLACK)
        head = Text("weighted vote\nof the three stumps", font_size=26, weight=BOLD)
        acc = Text("all 10 students classified correctly", font_size=24, color=GREEN_C)
        fin = VGroup(head, formula, acc).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        fin.next_to(self.ax, RIGHT, buff=0.4).shift(UP * 0.8)
        for d in dots:
            d.generate_target()
            d.target.scale(r0 / d.width * 2)
        self.play(*[MoveToTarget(d) for d in dots], FadeIn(VGroup(*lines)), run_time=0.8)
        self.play(FadeIn(cells), FadeIn(head), Write(formula), run_time=1.4)
        self.play(FadeIn(acc))
        self.wait(2)
        self.snap()

    def setup(self):
        pass


def key_frames_grid(frames, out, gap=16):
    w, hgt = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * hgt + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (hgt + gap)))
    sheet.save(out)


if __name__ == "__main__":
    for k, s in enumerate(STAGES, 1):
        t = s["stump"].tree_
        print(k, "feature", t.feature[0], "thr", t.threshold[0], "err", round(s["err"], 4), "alpha",
              round(s["alpha"], 4), "wrong", np.where(s["pred"] != Y)[0])
    print("all correct:", all(np.sign(score(c, q)) == y for c, q, y in zip(CGPA, IQ, Y)))
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "boosting_stages", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = BoostingStages()
        scene.render()
    mp4 = HERE / "boosting_stages.mp4"
    shutil.copy(next(media.rglob("boosting_stages.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "boosting_stages.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "boosting_stages_frames.png")
    shutil.rmtree(media)
