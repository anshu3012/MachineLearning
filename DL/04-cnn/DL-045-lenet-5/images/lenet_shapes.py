"""The shape arithmetic of LeNet-5, one layer per step: each block is drawn to scale (side = height of the maps,
one square per map) while its calculation appears: 32 - 5 + 1 = 28, 28 / 2 = 14, 14 - 5 + 1 = 10, 10 / 2 = 5,
5 x 5 x 16 = 400, then the dense layers 120, 84 and 10.
Manim: blocks are drawn one after another. Run: python lenet_shapes.py -> lenet_shapes.gif, lenet_shapes_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
import manimpango

for _f in Path("/usr/share/texmf/fonts/opentype/public/lm").glob("lmroman10-*.otf"):
    manimpango.register_font(str(_f))

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MarkupText.set_default(color=BLACK, font="Latin Modern Roman")


class Snap(Scene):
    """A scene that keeps key frames for the PDF grid."""
    def snap(self):
        if not hasattr(self, "snaps"):
            self.snaps = []
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))


def render(scene_cls, name, fps=10, width=760):
    """Render to <name>.gif and a 2 x 2 grid of the scene's first four key frames, <name>_frames.png."""
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = scene_cls()
        scene.render()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(next(media.rglob(f"{name}.mp4"))), "-vf",
                    f"fps={fps},scale={width}:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    w, h = scene.snaps[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, f in enumerate(scene.snaps[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / f"{name}_frames.png")
    shutil.rmtree(media)

S = 0.055                      # screen units per pixel of map side
# (side, maps, colour, shape label, layer name, calculation)
STAGES = [(32, 1, GREY_C, "32 × 32 × 1", "input", "a 32 × 32 image"),
          (28, 6, BLUE_C, "28 × 28 × 6", "conv 5 × 5, 6 filters", "32 − 5 + 1 = 28"),
          (14, 6, ORANGE_C, "14 × 14 × 6", "avg pool 2 × 2", "28 ÷ 2 = 14"),
          (10, 16, BLUE_C, "10 × 10 × 16", "conv 5 × 5, 16 filters", "14 − 5 + 1 = 10"),
          (5, 16, ORANGE_C, "5 × 5 × 16", "avg pool 2 × 2", "10 ÷ 2 = 5")]
DENSE = [(400, 2.6, RED_C, "flatten", "5 × 5 × 16 = 400"), (120, 1.7, GREEN_C, "dense", "400 → 120 nodes"),
         (84, 1.3, GREEN_C, "dense", "120 → 84 nodes"), (10, 0.6, GREEN_C, "softmax", "84 → 10 digits")]


def stack(side, maps, colour):
    g = VGroup()
    for k in range(maps):
        g.add(Square(side * S, stroke_color=colour, stroke_width=2, fill_color=WHITE, fill_opacity=1
                     ).shift((maps - 1 - k) * 0.04 * (RIGHT + UP)))
    return g


class Shapes(Snap):
    def construct(self):
        title = Text("LeNet-5: the shape after every layer", font_size=38).to_edge(UP, buff=0.3)
        self.play(FadeIn(title), run_time=0.5)
        x, prev, Y = -6.5, None, 0.3
        calc = Text(" ", font_size=40).move_to([0, -2.6, 0])
        self.add(calc)
        items = []
        for side, maps, col, shape, layer, eq in STAGES:
            b = stack(side, maps, col)
            b.move_to([x + b.width / 2, Y, 0])
            x += b.width + 0.5
            items.append((b, col, shape, layer, eq))
        for n, h, col, layer, eq in DENSE:
            b = Rectangle(width=0.28, height=h, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.25)
            b.move_to([x + 0.14, Y, 0])
            x += 0.28 + 0.5
            items.append((b, col, str(n), layer, eq))
        for k, (b, col, shape, layer, eq) in enumerate(items):
            lab = Text(shape, font_size=22, color=col).next_to(b, UP if k % 2 else DOWN, buff=0.15)
            new_calc = VGroup(Text(layer, font_size=30, color=col), Text(eq, font_size=44)).arrange(DOWN, buff=0.15
                                                                                               ).move_to([0, -2.6, 0])
            anims = [FadeIn(b, shift=RIGHT * 0.2), FadeIn(lab), Transform(calc, new_calc)]
            if prev is not None:
                anims.append(GrowArrow(Arrow(prev.get_right(), b.get_left(), buff=0.08, stroke_width=3, color=GREY_C,
                                             max_tip_length_to_length_ratio=0.35)))
            self.play(*anims, run_time=0.8)
            self.wait(1.0)
            if k in (1, 4, 5):
                self.snap()
            prev = b
        self.play(Transform(calc, VGroup(Text("the maps shrink 32 → 28 → 14 → 10 → 5", font_size=34),
                                         Text("while their number grows 1 → 6 → 16", font_size=34)
                                         ).arrange(DOWN, buff=0.15).move_to([0, -2.6, 0])), run_time=0.6)
        self.wait(2.5)
        self.snap()


if __name__ == "__main__":
    render(Shapes, "lenet_shapes")
