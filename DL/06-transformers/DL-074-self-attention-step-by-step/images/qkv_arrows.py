"""One embedding e = (1, 2) becomes three vectors: e W_Q = q, e W_K = k, e W_V = v (the Note's example of
section 8.1). Each matrix moves the arrow to a new place.
Run: python qkv_arrows.py -> qkv_arrows.mp4, qkv_arrows.gif, qkv_arrows_frames.png (Manim)"""
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
E = np.array([1.0, 2.0])
MATS = [("Q", np.array([[1, 0], [1, 1]]), BLUE_C, "query"),
        ("K", np.array([[0, 1], [1, 0]]), ORANGE_C, "key"),
        ("V", np.array([[2, 0], [0, 0.5]]), GREEN_C, "value")]


def fmt(v):
    return f"{v:g}"


class QKVArrows(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 3, 1], x_length=6.4, y_length=4.8, tips=False,
                  axis_config=dict(color=GREY_C, stroke_width=2, include_numbers=True, font_size=28,
                                   decimal_number_config=dict(color=GREY_C, num_decimal_places=0)))
        ax.to_edge(LEFT, buff=0.8).shift(DOWN * 0.4)
        P = lambda v: ax.c2p(v[0], v[1])
        title = Text("One embedding, three roles: three matrices", font_size=32).to_edge(UP, buff=0.3)
        self.play(FadeIn(title), Create(ax))
        e = Arrow(P([0, 0]), P(E), buff=0, color=GREY_C, stroke_width=8, max_tip_length_to_length_ratio=0.15)
        e_l = MarkupText("e = (1, 2)", font_size=30, color=GREY_C).next_to(P(E), UP, buff=0.12)
        self.play(GrowArrow(e), FadeIn(e_l))
        self.wait(0.5)
        self.snap()
        rows = VGroup()
        for k, (name, W, col, role) in enumerate(MATS):
            out = E @ W
            mat = MathTex(r"W_" + name + r"=\begin{pmatrix}" + fmt(W[0, 0]) + "&" + fmt(W[0, 1]) + r"\\" +
                          fmt(W[1, 0]) + "&" + fmt(W[1, 1]) + r"\end{pmatrix}", color=col, font_size=34)
            res = MarkupText(f"e W<sub>{name}</sub> = ({fmt(out[0])}, {fmt(out[1])}): {role}", font_size=26, color=col)
            row = VGroup(mat, res).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            row.move_to([3.9, 1.6 - 1.7 * k, 0], aligned_edge=LEFT).shift(LEFT * 1.0)
            a = Arrow(P([0, 0]), P(out), buff=0, color=col, stroke_width=7, max_tip_length_to_length_ratio=0.15)
            if name == "V":                                   # k and v are the same arrow here: draw v slightly thinner
                a = Arrow(P([0, 0]), P(out), buff=0, color=col, stroke_width=3, max_tip_length_to_length_ratio=0.1)
            lab = MarkupText(name.lower(), font_size=30, color=col)
            lab.next_to(P(out), {"Q": UR, "K": DOWN, "V": RIGHT}[name], buff=0.12)
            self.play(FadeIn(row), TransformFromCopy(e, a), FadeIn(lab), run_time=1.3)
            rows.add(row)
            self.wait(0.7)
            if name in ("Q", "V"):
                self.snap()
        note = VGroup(Text("one e, three vectors", font_size=26),
                      Text("(here k and v happen to coincide)", font_size=22, color=GREY_C)
                      ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(rows, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(FadeIn(note))
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
                     "output_file": "qkv_arrows", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = QKVArrows()
        scene.render()
    mp4 = HERE / "qkv_arrows.mp4"
    shutil.copy(next(media.rglob("qkv_arrows.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "qkv_arrows.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "qkv_arrows_frames.png")
    shutil.rmtree(media)
