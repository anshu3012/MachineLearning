"""One word, "how", through one encoder block of the Notebook's tiny model (d_model = 4, 2 heads, hidden layer 8):
attention computes a change z that is added to x (the residual connection), layer normalisation rescales the sum,
the feed-forward network computes a second change y that is added, and a second normalisation gives the output.
The values are the Notebook's (section 5 of the Note quotes them).
Run: python block_values.py -> block_values.mp4, block_values.gif, block_values_frames.png (Manim)"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MarkupText.set_default(color=BLACK, font="Latin Modern Roman")
# the Notebook's numbers for "how" (Note, sections 5.1 to 5.4)
X = [0.5, 2.0, -0.5, 1.2]
Z = [1.08, 0.77, 0.39, -1.21]
Z1 = [1.58, 2.77, -0.11, -0.01]
ZN = [0.44, 1.43, -0.98, -0.89]
H = [0.20, 0, 0.83, 0.09, 0.21, 1.36, 0, 0.47]
Y = [-0.78, 0.67, -0.14, -0.31]
Y1 = [-0.34, 2.10, -1.12, -1.20]
YN = [-0.15, 1.68, -0.73, -0.79]


def cells(values, label, colour=BLACK, w=1.05):
    """A vector as a row of cells: blue for positive, red for negative, paler near 0."""
    row = VGroup()
    for v in values:
        c = ManimColor(BLUE_C if v >= 0 else RED_C).interpolate(WHITE, 1 - min(abs(v) / 2.0, 1) * 0.8)
        sq = Rectangle(width=w, height=0.55, stroke_color=GREY_C, stroke_width=2, fill_color=c, fill_opacity=1)
        row.add(VGroup(sq, Text(f"{v:.2f}", font_size=26).move_to(sq)))
    row.arrange(RIGHT, buff=0)
    return VGroup(row, MarkupText(label, font_size=27, color=colour).next_to(row, LEFT, buff=0.25))


class BlockValues(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        title = Text('The word "how" through one encoder block', font_size=32).to_edge(UP, buff=0.3)
        x = cells(X, "x  (input)", GREY_C).move_to([0.6, 2.4, 0])
        self.play(FadeIn(title), FadeIn(x))
        # sub-layer 1: attention, a change added to x
        z = cells(Z, "z  (attention's change)", PURPLE_C).move_to([0.6, 1.6, 0])
        z.shift(RIGHT * (x[0].get_left()[0] - z[0].get_left()[0]))
        plus = Text("+", font_size=40).next_to(z[0], RIGHT, buff=0.3)
        self.play(FadeIn(z, shift=DOWN * 0.2), FadeIn(plus))
        z1 = cells(Z1, "x + z", BLACK).move_to([0.6, 0.8, 0])
        z1.shift(RIGHT * (x[0].get_left()[0] - z1[0].get_left()[0]))
        line = Line(z[0].get_corner(DL) + DOWN * 0.08, z[0].get_corner(DR) + DOWN * 0.08, color=BLACK)
        self.play(Create(line), TransformFromCopy(VGroup(x[0], z[0]), z1[0]), FadeIn(z1[1]), run_time=1.2)
        note1 = Text("residual connection: the input skips attention and is added back", font_size=22,
                     color=RED_C).next_to(z1, DOWN, buff=0.25)
        self.play(FadeIn(note1))
        self.wait(0.8)
        self.snap()
        zn = cells(ZN, "LayerNorm(x + z)", BLUE_C).move_to(z1)
        zn.shift(RIGHT * (z1[0].get_left()[0] - zn[0].get_left()[0]))
        stat = Text("mean 1.06, standard deviation 1.20 → mean 0, standard deviation 1", font_size=22,
                    color=GREY_C).move_to(note1)
        self.play(ReplacementTransform(z1, zn), ReplacementTransform(note1, stat), run_time=1.2)
        self.wait(1.0)
        self.snap()
        # sub-layer 2: feed-forward network, a second change
        self.play(FadeOut(x), FadeOut(z), FadeOut(plus), FadeOut(line), FadeOut(stat),
                  zn.animate.move_to([0.6, 2.4, 0]), run_time=1.0)
        h = cells(H, "hidden layer, ReLU", GREEN_C, w=0.85).move_to([0.2, 1.4, 0])
        zero = VGroup(*[SurroundingRectangle(h[0][i], color=RED_C, buff=0.02, stroke_width=4) for i in (1, 6)])
        self.play(FadeIn(h, shift=DOWN * 0.2), run_time=0.9)
        self.play(Create(zero), FadeIn(Text("ReLU set 2 of 8 values to 0", font_size=22, color=RED_C)
                                       .next_to(h, DOWN, buff=0.15)), run_time=0.8)
        y = cells(Y, "y  (the network's change)", PURPLE_C).move_to([0.6, 0.0, 0])
        y.shift(RIGHT * (zn[0].get_left()[0] - y[0].get_left()[0]))
        self.play(FadeIn(y, shift=DOWN * 0.2))
        y1 = cells(Y1, "LayerNorm(x + z) + y", BLACK).move_to([0.6, -0.9, 0])
        y1.shift(RIGHT * (zn[0].get_left()[0] - y1[0].get_left()[0]))
        line2 = Line(y[0].get_corner(DL) + DOWN * 0.08, y[0].get_corner(DR) + DOWN * 0.08, color=BLACK)
        self.play(Create(line2), TransformFromCopy(VGroup(zn[0], y[0]), y1[0]), FadeIn(y1[1]), run_time=1.2)
        self.wait(0.6)
        self.snap()
        yn = cells(YN, "block output", BLUE_C).move_to(y1)
        yn.shift(RIGHT * (y1[0].get_left()[0] - yn[0].get_left()[0]))
        self.play(ReplacementTransform(y1, yn), run_time=1.2)
        end = VGroup(Text("each sub-layer adds a change; the sum is normalised", font_size=24),
                     Text("still 4 numbers (512 in the paper): ready for the next block", font_size=22, color=GREY_C)
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
                     "output_file": "block_values", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = BlockValues()
        scene.render()
    mp4 = HERE / "block_values.mp4"
    shutil.copy(next(media.rglob("block_values.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "block_values.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "block_values_frames.png")
    shutil.rmtree(media)
