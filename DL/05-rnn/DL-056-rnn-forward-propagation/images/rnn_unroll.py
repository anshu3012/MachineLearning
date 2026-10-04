"""The same recurrent layer applied at t = 1, 2, 3 to "movie was good". The hidden state h_t (3 numbers, from the
Notebook's worked example) is passed to the next time step; the last one gives the prediction.
Run: python rnn_unroll.py  -> rnn_unroll.mp4, rnn_unroll.gif, rnn_unroll_frames.png"""
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
steps = pd.read_csv(HERE.parent / "data" / "worked_example.csv")
X0, DX = -3.4, 3.2                                         # x of the first box, gap between time steps


def state(values, label):
    """Hidden state as 3 cells: blue for positive, red for negative, paler when near 0."""
    cells = VGroup()
    for v in values:
        colour = ManimColor(BLUE_C if v >= 0 else RED_C).interpolate(WHITE, 1 - min(abs(v) / 0.8, 1) * 0.85)
        sq = Rectangle(width=0.78, height=0.5, stroke_color=GREY_C, stroke_width=2, fill_color=colour, fill_opacity=1)
        cells.add(VGroup(sq, Text(f"{v:.2f}", font_size=20).move_to(sq)))
    cells.arrange(RIGHT, buff=0)
    return VGroup(cells, MarkupText(label, font_size=24, color=RED_C).next_to(cells, UP, buff=0.12))


def rnn_box(x):
    box = RoundedRectangle(corner_radius=0.15, width=2.2, height=1.1, stroke_color=PURPLE_C,
                           fill_color=ManimColor(PURPLE_C).interpolate(WHITE, 0.85), fill_opacity=1)
    label = VGroup(Text("recurrent layer", font_size=22), MarkupText("same W<sub>i</sub>, W<sub>h</sub>", font_size=18, color=GREY_C)
                   ).arrange(DOWN, buff=0.06).move_to(box)
    return VGroup(box, label).move_to([x, 0, 0])


class RNNUnroll(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        title = Text('"movie was good", one word per time step', font_size=30).to_edge(UP, buff=0.35)
        h_prev = state([0, 0, 0], "h<sub>0</sub> = zeros").scale(0.9).move_to([X0 - 2.0, 1.6, 0])
        self.play(FadeIn(title), FadeIn(h_prev))
        for k, r in steps.iterrows():
            x = X0 + k * DX
            box = rnn_box(x)
            word = VGroup(Text(r.word, font_size=28, color=BLUE_C), Text(f"t = {r.t}", font_size=20, color=GREY_C)
                          ).arrange(DOWN, buff=0.08).move_to([x, -2.2, 0])
            up = Arrow(word.get_top(), box.get_bottom(), buff=0.1, color=BLUE_C, stroke_width=4)
            self.play(FadeIn(box), FadeIn(word, shift=UP * 0.3), GrowArrow(up), run_time=0.8)
            carry = Arrow(h_prev.get_bottom(), box.get_left(), buff=0.1, color=RED_C, stroke_width=4)
            self.play(GrowArrow(carry), Indicate(h_prev, color=RED_C, scale_factor=1.08), run_time=0.8)
            h_new = state([r.h1, r.h2, r.h3], f"h<sub>{r.t}</sub>").scale(0.9).move_to([x + 1.1, 1.6, 0])
            out = Arrow(box.get_top(), h_new.get_bottom(), buff=0.1, color=PURPLE_C, stroke_width=4)
            self.play(GrowArrow(out), FadeIn(h_new, shift=UP * 0.2), run_time=0.8)
            self.wait(0.5)
            h_prev = h_new
            self.snap()
        y = VGroup(MarkupText("ŷ = sigmoid(h<sub>3</sub> W<sub>o</sub>)", font_size=24, color=GREEN_C),
                   Text(f"= {steps.y_hat.iloc[0]:.2f}", font_size=24, color=GREEN_C)).arrange(DOWN, buff=0.12)
        y.move_to([h_prev.get_right()[0] + 0.3, -1.2, 0])
        self.play(GrowArrow(Arrow(h_prev.get_bottom() + RIGHT * 0.9, y.get_top(), buff=0.1, color=GREEN_C,
                                  stroke_width=4)), FadeIn(y), run_time=1.0)
        note = Text("the last hidden state holds information from all three words", font_size=24, color=GREY_C).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note))
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
                     "output_file": "rnn_unroll", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = RNNUnroll()
        scene.render()
    mp4 = HERE / "rnn_unroll.mp4"
    shutil.copy(next(media.rglob("rnn_unroll.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "rnn_unroll.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "rnn_unroll_frames.png")
    shutil.rmtree(media)
