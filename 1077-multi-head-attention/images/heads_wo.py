"""Two heads on "money bank", followed for the word "money": each head's weights and output, the concatenation,
and W_O cut into one block of rows per head. Concatenating and multiplying by W_O equals adding one change per
head. Numbers from the Notebook (section 1 and data/wo_split.csv).
Intuition after Sanderson (3Blue1Brown), "Attention in transformers, step-by-step", 2024 (20:31-23:08).
Run: python heads_wo.py -> heads_wo.mp4, heads_wo.gif, heads_wo_frames.png (Manim)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MarkupText.set_default(color=BLACK, font="Latin Modern Roman")
split = pd.read_csv(HERE.parent / "data" / "wo_split.csv")
# the Notebook's section 1, row of "money"
WEIGHTS = {1: (0.269, 0.731), 2: (0.5, 0.5)}
Z = {1: [-2.46, -0.73, -0.54, -0.27], 2: [1.50, -0.50, -0.50, 0.00]}
WO = np.array([[-1, -1, 0, 1], [0, 1, -1, -1], [1, 1, -1, -1], [1, 0, 0, -1],
               [1, 0, 1, 1], [1, -1, 1, -1], [0, 0, 1, -1], [1, -1, 0, 0]])
assert np.allclose(np.array(Z[1]) @ WO[:4], split["head 1"], atol=0.02)
assert np.allclose(np.array(Z[2]) @ WO[4:], split["head 2"], atol=0.02)
HC = {1: BLUE_C, 2: ORANGE_C}


def cells(values, colour, w=0.78, h=0.5, fs=22):
    row = VGroup()
    for v in values:
        sq = Rectangle(width=w, height=h, stroke_color=colour, stroke_width=3,
                       fill_color=ManimColor(colour).interpolate(WHITE, 0.82), fill_opacity=1)
        row.add(VGroup(sq, Text(f"{v:.2f}" if isinstance(v, float) else f"{v}", font_size=fs).move_to(sq)))
    return row.arrange(RIGHT, buff=0)


class HeadsWO(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        title = MarkupText('Two heads, then W<sub>O</sub>: each head adds its own change', font_size=32).to_edge(UP, buff=0.3)
        sub = Text('the word "money" in "money bank"', font_size=24, color=GREY_C).next_to(title, DOWN, buff=0.12)
        self.play(FadeIn(title), FadeIn(sub))
        heads, zs = {}, {}
        for i, x in ((1, -3.4), (2, 3.4)):
            lab = Text(f"head {i}", font_size=30, color=HC[i]).move_to([x, 2.1, 0])
            w = VGroup(*[Text(f"{a:.2f} on {wd}", font_size=24) for a, wd in zip(WEIGHTS[i], ("money", "bank"))]
                       ).arrange(RIGHT, buff=0.4).next_to(lab, DOWN, buff=0.2)
            heads[i] = VGroup(lab, w)
        self.play(*[FadeIn(h, shift=DOWN * 0.2) for h in heads.values()], run_time=1.0)
        for i in (1, 2):
            zs[i] = cells(Z[i], HC[i]).next_to(heads[i], DOWN, buff=0.3)
            zl = MarkupText(f"z<sup>{i}</sup>", font_size=26, color=HC[i]).next_to(zs[i], LEFT, buff=0.15)
            zs[i] = VGroup(zs[i], zl)
        self.play(*[FadeIn(z) for z in zs.values()], run_time=1.0)
        self.wait(0.6)
        self.snap()
        # concatenate
        cat = VGroup(zs[1][0].copy(), zs[2][0].copy()).arrange(RIGHT, buff=0).move_to([-2.6, -1.4, 0])
        cat_l = Text("concatenate: 8 numbers", font_size=24).next_to(cat, UP, buff=0.15)
        self.play(TransformFromCopy(zs[1][0], cat[0]), TransformFromCopy(zs[2][0], cat[1]), FadeIn(cat_l), run_time=1.2)
        wo = VGroup(*[cells([int(v) for v in WO[r]], HC[1 if r < 4 else 2], w=0.55, h=0.38, fs=20) for r in range(8)]
                    ).arrange(DOWN, buff=0).next_to(cat, RIGHT, buff=0.6).shift(DOWN * 0.3)
        wo_l = MarkupText("W<sub>O</sub> (8 x 4)", font_size=24).next_to(wo, UP, buff=0.1)
        times = Text("×", font_size=36).next_to(cat, RIGHT, buff=0.15)
        self.play(FadeIn(times), FadeIn(wo), FadeIn(wo_l), run_time=0.9)
        brace1 = Brace(wo[:4], RIGHT, color=BLUE_C)
        brace2 = Brace(wo[4:], RIGHT, color=ORANGE_C)
        b1 = Text("head 1", font_size=24, color=BLUE_C).next_to(brace1, RIGHT, buff=0.08)
        b2 = Text("head 2", font_size=24, color=ORANGE_C).next_to(brace2, RIGHT, buff=0.08)
        self.play(GrowFromCenter(brace1), GrowFromCenter(brace2), FadeIn(b1), FadeIn(b2))
        self.wait(0.8)
        self.snap()
        # one change per head, summed
        self.play(FadeOut(VGroup(cat, cat_l, times, wo, wo_l, brace1, brace2, b1, b2)), run_time=0.6)
        y0 = -0.4
        ch = {}
        for k, i in enumerate((1, 2)):
            vals = [float(v) for v in split[f"head {i}"]]
            ch[i] = cells(vals, HC[i]).move_to([1.3, y0 - 0.7 * k, 0])
            lab = MarkupText(f"z<sup>{i}</sup> × rows of head {i}", font_size=24, color=HC[i]).next_to(ch[i], LEFT, buff=0.25)
            self.play(TransformFromCopy(zs[i][0], ch[i]), FadeIn(lab), run_time=1.0)
            ch[i] = VGroup(ch[i], lab)
        plus = Text("+", font_size=36).next_to(ch[2][0], RIGHT, buff=0.2)
        line = Line(ch[2][0].get_corner(DL) + DOWN * 0.1, ch[2][0].get_corner(DR) + DOWN * 0.1, color=BLACK)
        out = cells([float(v) for v in split["sum"]], PURPLE_C).next_to(ch[2][0], DOWN, buff=0.25)
        out_l = Text("output for money", font_size=24, color=PURPLE_C).next_to(out, LEFT, buff=0.25)
        self.play(FadeIn(plus), Create(line), TransformFromCopy(VGroup(ch[1][0], ch[2][0]), out), FadeIn(out_l), run_time=1.2)
        self.wait(0.6)
        self.snap()
        end = VGroup(MarkupText("concatenate, then multiply by W<sub>O</sub>", font_size=26),
                     Text("= add one change per head", font_size=26, color=PURPLE_C)
                     ).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(end))
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
                     "output_file": "heads_wo", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = HeadsWO()
        scene.render()
    mp4 = HERE / "heads_wo.mp4"
    shutil.copy(next(media.rglob("heads_wo.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "heads_wo.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "heads_wo_frames.png")
    shutil.rmtree(media)
