"""Batch against layer normalisation on the Note's padded batch ("hi rahul" + 2 padding rows, "how are you today";
3 numbers per position, section 5.1). Batch normalisation sweeps down each column: its mean and standard deviation
include the padding zeros. Layer normalisation sweeps along each row: every word is standardised on its own, and the
padding rows do not touch the words. Values computed here as Keras does (epsilon = 0.001, gamma = 1, beta = 0).
Run: python norm_axes.py -> norm_axes.mp4, norm_axes.gif, norm_axes_frames.png (Manim)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MarkupText.set_default(color=BLACK, font="Latin Modern Roman")
WORDS = ["hi", "rahul", "(pad)", "(pad)", "how", "are", "you", "today"]
Z = np.array([[6.1, 3.2, 1.3], [1.1, 7.5, 8.3], [0, 0, 0], [0, 0, 0],
              [5.9, 6.8, 5.3], [8.5, 7.5, 1.0], [7.9, 1.3, 6.8], [2.4, 7.9, 5.3]])
EPS = 1e-3
BN = (Z - Z.mean(0)) / np.sqrt(Z.var(0) + EPS)
LN = (Z - Z.mean(1, keepdims=True)) / np.sqrt(Z.var(1, keepdims=True) + EPS)
CW, RH = 1.15, 0.52


def table(values, origin):
    g = VGroup()
    for i, row in enumerate(values):
        for j, v in enumerate(row):
            pad = WORDS[i] == "(pad)"
            sq = Rectangle(width=CW, height=RH, stroke_color=GREY_C, stroke_width=1.5,
                           fill_color=RED_C if pad else WHITE, fill_opacity=0.12 if pad else 1)
            sq.move_to(origin + np.array([j * CW, -i * RH, 0]))
            g.add(VGroup(sq, Text(f"{v:.2f}", font_size=22).move_to(sq)))
    return g


class NormAxes(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        title = Text("Batch norm averages columns; layer norm averages rows", font_size=30).to_edge(UP, buff=0.25)
        org = np.array([-3.6, 2.0, 0])
        tab = table(Z, org)
        heads = VGroup(*[Text(f"dim {j + 1}", font_size=22, color=GREY_C).move_to(org + np.array([j * CW, RH * 0.95, 0]))
                         for j in range(3)])
        rows = VGroup(*[Text(w, font_size=22, color=RED_C if w == "(pad)" else BLACK)
                        .move_to(org + np.array([-1.15, -i * RH, 0])) for i, w in enumerate(WORDS)])
        self.play(FadeIn(title), FadeIn(tab), FadeIn(heads), FadeIn(rows))
        px = 1.2
        # batch normalisation: column by column
        bn_t = Text("batch normalisation", font_size=28, color=BLUE_C).move_to([px, 2.2, 0], aligned_edge=LEFT)
        self.play(FadeIn(bn_t), run_time=0.5)
        info = VGroup()
        for j in range(3):
            box = SurroundingRectangle(VGroup(*[tab[i * 3 + j] for i in range(8)]), color=BLUE_C, buff=0.03, stroke_width=5)
            txt = Text(f"dim {j + 1}: mean {Z[:, j].mean():.2f}, with the zeros", font_size=22, color=BLUE_C)
            txt.move_to([px, 1.5 - 0.45 * j, 0], aligned_edge=LEFT)
            self.play(Create(box), FadeIn(txt), run_time=0.7)
            self.wait(0.3)
            if j == 2:
                self.snap()
            self.play(FadeOut(box), run_time=0.3)
            info.add(txt)
        real = Text(f"over the 6 real words: {Z[[0, 1, 4, 5, 6, 7], 0].mean():.2f}, "
                    f"{Z[[0, 1, 4, 5, 6, 7], 1].mean():.2f}, {Z[[0, 1, 4, 5, 6, 7], 2].mean():.2f}",
                    font_size=22, color=RED_C).move_to([px, 0.1, 0], aligned_edge=LEFT)
        self.play(FadeIn(real))
        bn_tab = table(BN, org)
        self.play(Transform(tab, bn_tab), run_time=1.2)
        note = Text("padding changed the words' numbers", font_size=22, color=RED_C).move_to([px, -0.4, 0], aligned_edge=LEFT)
        self.play(FadeIn(note))
        self.wait(1.2)
        self.snap()
        # layer normalisation: row by row
        self.play(Transform(tab, table(Z, org)), FadeOut(VGroup(bn_t, info, real, note)), run_time=0.9)
        ln_t = Text("layer normalisation", font_size=28, color=ORANGE_C).move_to([px, 2.2, 0], aligned_edge=LEFT)
        self.play(FadeIn(ln_t), run_time=0.5)
        for i in (0, 1, 2, 4):
            box = SurroundingRectangle(VGroup(*[tab[i * 3 + j] for j in range(3)]), color=ORANGE_C, buff=0.03,
                                       stroke_width=5)
            msg = (f"{WORDS[i]}: mean {Z[i].mean():.2f}, its own numbers only" if WORDS[i] != "(pad)"
                   else "padding row: stays 0, touches no word")
            txt = Text(msg, font_size=22, color=ORANGE_C).move_to([px, 1.5, 0], aligned_edge=LEFT)
            self.play(Create(box), FadeIn(txt), run_time=0.6)
            self.wait(0.5)
            if i == 1:
                self.snap()
            self.play(FadeOut(box), FadeOut(txt), run_time=0.3)
        self.play(Transform(tab, table(LN, org)), run_time=1.2)
        end = VGroup(Text("each word standardised on its own:", font_size=24),
                     Text("adding padding cannot change it", font_size=24, color=ORANGE_C)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([px, 0.6, 0], aligned_edge=LEFT)
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
                     "output_file": "norm_axes", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = NormAxes()
        scene.render()
    mp4 = HERE / "norm_axes.mp4"
    shutil.copy(next(media.rglob("norm_axes.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "norm_axes.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "norm_axes_frames.png")
    shutil.rmtree(media)
