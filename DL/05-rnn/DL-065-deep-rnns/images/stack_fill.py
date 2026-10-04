"""The two-layer toy stack of section 4.2 (layer 1: 3 nodes, layer 2: 2 nodes) reading "cat mat rat". The grid fills
cell by cell: each hidden state h_t^(l) is computed from the cell below and the cell to its left. Values are the
Notebook's hand forward pass (untrained Keras weights, seed 42). Run: python stack_fill.py -> stack_fill.gif,
stack_fill_frames.png (Manim + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import pandas as pd
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MarkupText.set_default(color=BLACK, font="Latin Modern Roman")
g = pd.read_csv(HERE.parent / "data" / "toy_states.csv")
ONE_HOT = {"cat": "[1, 0, 0]", "mat": "[0, 1, 0]", "rat": "[0, 0, 1]"}
XS, X_H0 = [-2.4, 0.9, 4.0], -5.2                       # x of the time steps and of the zero start states
Y_WORD, Y = -2.75, {1: -0.9, 2: 1.35}                    # y of the words and of each layer
COLOUR = {1: BLUE_C, 2: ORANGE_C}


def state(values, label, layer):
    """Hidden state as cells: blue for positive, red for negative, paler when near 0."""
    cells = VGroup()
    for v in values:
        colour = ManimColor(BLUE_C if v >= 0 else RED_C).interpolate(WHITE, 1 - min(abs(v) / 0.8, 1) * 0.85)
        sq = Rectangle(width=0.7, height=0.48, stroke_color=COLOUR[layer], stroke_width=3, fill_color=colour,
                       fill_opacity=1)
        cells.add(VGroup(sq, Text(f"{v:.2f}", font_size=20).move_to(sq)))
    cells.arrange(RIGHT, buff=0)
    return VGroup(cells, MarkupText(label, font_size=24, color=COLOUR[layer]).next_to(cells, UP, buff=0.1))


def arrow(a, b, colour):
    return Arrow(a, b, buff=0.08, color=colour, stroke_width=5, max_tip_length_to_length_ratio=0.3)


class StackFill(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        title = Text('"cat mat rat" through two stacked layers', font_size=32).to_edge(UP, buff=0.3)
        rows = VGroup(*[Text(f"layer {l}", font_size=24, color=COLOUR[l]).rotate(PI / 2).move_to([-6.6, Y[l], 0])
                        for l in (1, 2)])
        prev = {1: state([0, 0, 0], "zeros", 1).move_to([X_H0, Y[1], 0]),
                2: state([0, 0], "zeros", 2).move_to([X_H0, Y[2], 0])}
        self.play(FadeIn(title), FadeIn(rows), FadeIn(prev[1]), FadeIn(prev[2]))
        for k, r in g.iterrows():
            x = XS[k]
            word = VGroup(Text(r.word, font_size=30, color=GREEN_C, weight=BOLD),
                          Text(ONE_HOT[r.word], font_size=18, color=GREY_C)).arrange(DOWN, buff=0.06).move_to([x, Y_WORD, 0])
            self.play(FadeIn(word, shift=UP * 0.2), run_time=0.4)
            below = word
            for l, vals in ((1, [r.h1_1, r.h1_2, r.h1_3]), (2, [r.h2_1, r.h2_2])):
                h = state(vals, f"h<sub>{r.t}</sub><sup>({l})</sup>", l).move_to([x, Y[l], 0])
                up = arrow(below.get_top(), h[0].get_bottom(), COLOUR[l])
                left = arrow(prev[l][0].get_right(), h[0].get_left(), RED_C)
                self.play(GrowArrow(up), GrowArrow(left), run_time=0.6)
                self.play(FadeIn(h, scale=0.8), run_time=0.5)
                prev[l], below = h, h
            self.wait(0.6)
            self.snap()
        y = MarkupText(f"ŷ = {r.y_hat:.2f}", font_size=26, color=PURPLE_C).move_to([5.95, Y[2], 0])
        self.play(GrowArrow(arrow(prev[2][0].get_right(), y.get_left(), PURPLE_C)), FadeIn(y), run_time=0.8)
        note = Text("each cell reads the cell below and the cell to its left", font_size=24,
                    color=GREY_C).next_to(title, DOWN, buff=0.2)
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
                     "output_file": "stack_fill", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = StackFill()
        scene.render()
    mp4 = HERE / ".stack_fill.mp4"
    shutil.copy(next(media.rglob("stack_fill.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "stack_fill.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "stack_fill_frames.png")
    shutil.rmtree(media)
    mp4.unlink()
