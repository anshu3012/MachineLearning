"""The chain of the small CNN, then the backward pass over it: gradients appear from right to left, each with the
shape of its tensor. Green: the ANN part (this Note). Red: the CNN part (the part 2 Note).
Manim: boxes and arrows drawn one after another. Run: python chain_backward.py -> chain_backward.gif, _frames.png"""
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

NODES = [("X", "6 × 6"), ("Z<sub>1</sub>", "4 × 4"), ("A<sub>1</sub>", "4 × 4"), ("P<sub>1</sub>", "2 × 2"),
         ("F", "4 × 1"), ("Z<sub>2</sub>", "1 × 1"), ("A<sub>2</sub>", "1 × 1"), ("L", "loss")]
OPS = ["conv", "ReLU", "max pool", "flatten", "dense", "σ", "log loss"]
# backward steps, right to left: (index of the tensor that receives the gradient, local rule, colour)
BACK = [(6, "log loss", GREEN_C), (5, "a<sub>2</sub> − y", GREEN_C), (4, "× W<sub>2</sub><sup>T</sup>", RED_C),
        (3, "reshape", RED_C), (2, "route to max", RED_C), (1, "ReLU mask", RED_C)]


class Chain(Snap):
    def construct(self):
        title = Text("Forward: one operation per arrow", font_size=38).to_edge(UP, buff=0.35)
        xs = np.linspace(-6.1, 6.1, 8)
        boxes, shapes = VGroup(), VGroup()
        for x, (name, shape) in zip(xs, NODES):
            b = VGroup(RoundedRectangle(corner_radius=0.12, width=1.05, height=0.8, stroke_color=BLUE_C, stroke_width=4,
                                        fill_color=WHITE, fill_opacity=1), MarkupText(name, font_size=32))
            b.move_to([x, 1.5, 0])
            boxes.add(b)
            shapes.add(Text(shape, font_size=24, color=GREY_C).next_to(b, UP, buff=0.12))
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.05, stroke_width=4, color=GREY_C,
                                max_tip_length_to_length_ratio=0.3) for i in range(7)])
        ops = VGroup(*[Text(o, font_size=22, color=GREY_C).move_to([arrows[i].get_center()[0], 0.85, 0]) for i, o in enumerate(OPS)])
        self.play(FadeIn(title), FadeIn(boxes[0]), FadeIn(shapes[0]), run_time=0.6)
        for i in range(7):
            self.play(GrowArrow(arrows[i]), FadeIn(ops[i]), FadeIn(boxes[i + 1]), FadeIn(shapes[i + 1]), run_time=0.45)
        self.wait(0.6)
        self.snap()

        self.play(Transform(title, Text("Backward: one gradient per tensor, right to left", font_size=38
                                        ).to_edge(UP, buff=0.35)), run_time=0.6)
        grads = {}
        prev = boxes[7]
        for k, (i, rule, col) in enumerate(BACK):
            name, shape = NODES[i]
            g = VGroup(RoundedRectangle(corner_radius=0.12, width=1.25, height=1.0, stroke_color=col, stroke_width=4,
                                        fill_color=WHITE, fill_opacity=1),
                       VGroup(MarkupText(f"∂L/∂{name}", font_size=22, color=col),
                              Text(shape, font_size=22, color=col)).arrange(DOWN, buff=0.06))
            g[1].move_to(g[0])
            g.move_to([xs[i], -0.7, 0])
            start = prev.get_bottom() if k == 0 else prev.get_left()
            end = g.get_right() if k else g.get_top() + RIGHT * 0.3
            a = (CurvedArrow(boxes[7].get_bottom(), g.get_right() + UP * 0.1, angle=-0.9, color=col, stroke_width=4,
                             tip_length=0.2) if k == 0
                 else Arrow(start, end, buff=0.05, stroke_width=4, color=col, max_tip_length_to_length_ratio=0.3))
            lab = MarkupText(rule, font_size=20, color=col).next_to(g, DOWN, buff=0.12)
            self.play(Create(a) if k == 0 else GrowArrow(a), run_time=0.45)
            self.play(FadeIn(g, shift=LEFT * 0.2), FadeIn(lab), Indicate(boxes[i], color=col, scale_factor=1.1), run_time=0.6)
            grads[i], prev = g, g
            if k == 1:
                self.wait(0.3)
                self.snap()
        self.wait(0.4)
        self.snap()

        # the parameters hang off Z2 (W2, b2) and Z1 (W1, b1)
        def param(i, text, shape, col, dx):
            p = VGroup(MarkupText(text, font_size=24, color=col), Text(shape, font_size=22, color=col)).arrange(DOWN, buff=0.06)
            p.move_to([xs[i] + dx, -2.9, 0])
            return p, Arrow(grads[i].get_bottom() + DOWN * 0.45, p.get_top(), buff=0.08, stroke_width=4, color=col,
                            max_tip_length_to_length_ratio=0.3)
        p2, a2 = param(5, "∂L/∂W<sub>2</sub> = (a<sub>2</sub> − y) F<sup>T</sup>", "1 × 4, the shape of the output weights", GREEN_C, 0.2)
        p1, a1 = param(1, "∂L/∂W<sub>1</sub> = X ∗ ∂L/∂Z<sub>1</sub>", "3 × 3, the shape of the filter", RED_C, 0.4)
        self.play(GrowArrow(a2), FadeIn(p2), run_time=0.8)
        self.wait(0.5)
        self.play(GrowArrow(a1), FadeIn(p1), run_time=0.8)
        key = VGroup(Text("green: ANN part (this Note)", font_size=24, color=GREEN_C),
                     Text("red: CNN part (part 2)", font_size=24, color=RED_C)).arrange(RIGHT, buff=0.8).move_to([0, -3.7, 0])
        self.play(FadeIn(key), run_time=0.5)
        self.wait(2.5)
        self.snap()


if __name__ == "__main__":
    render(Chain, "chain_backward")
