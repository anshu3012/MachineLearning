"""A filter is a node that looks at 9 pixels at a time. First an ANN node with one weight per pixel of an 8 x 8 digit
(scikit-learn digits, image 0); then a 3 x 3 filter with 9 weights; then the filter slides, using the same 9 weights
at all 36 positions (parameter sharing) and filling the feature map (vertical-edge filter + ReLU).
Manim: lines collapse and a window moves. Run: python filter_as_node.py -> filter_as_node.gif, _frames.png"""
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
from sklearn.datasets import load_digits

IMG = load_digits().images[0] / 16.0                       # 8 x 8, values 0..1
K = np.array([[1, 0, -1]] * 3, float)
FMAP = np.array([[max((IMG[i:i + 3, j:j + 3] * K).sum(), 0) for j in range(6)] for i in range(6)])
assert FMAP.shape == (6, 6) and FMAP.max() > 0
C = 0.42                                                   # cell size


def grid(vals, at, colour, top):
    g = VGroup()
    for r in range(vals.shape[0]):
        for c in range(vals.shape[1]):
            sq = Square(C, stroke_color=GREY_C, stroke_width=1,
                        fill_color=ManimColor(WHITE).interpolate(ManimColor(colour), min(vals[r, c] / top, 1)),
                        fill_opacity=1).move_to([c * C, -r * C, 0])
            g.add(sq)
    return g.move_to(at)


class FilterNode(Snap):
    def construct(self):
        title = Text("An ANN node: one weight for every pixel", font_size=38).to_edge(UP, buff=0.35)
        gx = grid(IMG, [-4.6, -0.3, 0], "#222222", 1.0)
        lx = Text("image, 8 × 8", font_size=28, color=GREY_C).next_to(gx, DOWN, buff=0.25)
        node = Circle(0.62, stroke_color=BLUE_C, stroke_width=5, fill_color=WHITE, fill_opacity=1).move_to([0, -0.3, 0])
        ntxt = VGroup(Text("Σ + b", font_size=26), Text("ReLU", font_size=24, color=GREY_C)).arrange(DOWN, buff=0.05).move_to(node)
        self.play(FadeIn(title), FadeIn(gx), FadeIn(lx), FadeIn(node), FadeIn(ntxt), run_time=0.8)
        all_lines = VGroup(*[Line(sq.get_center(), node.get_left(), stroke_color=BLUE_C, stroke_width=1.2, stroke_opacity=0.6)
                             for sq in gx])
        count = Text("64 pixels → 64 weights + 1 bias", font_size=32, color=BLUE_C).to_edge(DOWN, buff=0.5)
        self.play(LaggedStart(*[Create(l) for l in all_lines], lag_ratio=0.01), run_time=1.6)
        self.play(FadeIn(count), run_time=0.5)
        self.wait(1.2)
        self.snap()

        # the filter: the same kind of node, on 9 pixels
        win = Square(3 * C, stroke_color=ORANGE_C, stroke_width=6).move_to(gx[9].get_center())   # centre cell of the first window

        def nine():
            c0 = win.get_center()
            return VGroup(*[Line(c0 + np.array([dx * C, dy * C, 0]), node.get_left(), stroke_color=ORANGE_C, stroke_width=2.5)
                            for dy in (1, 0, -1) for dx in (-1, 0, 1)])
        lines9 = always_redraw(nine)
        self.play(FadeOut(all_lines), Transform(title, Text("A filter: the same node, on 9 pixels at a time", font_size=38
                                                             ).to_edge(UP, buff=0.35)),
                  Transform(count, Text("9 pixels → 9 weights + 1 bias", font_size=32, color=ORANGE_C).to_edge(DOWN, buff=0.5)),
                  node.animate.set_stroke(color=ORANGE_C), run_time=0.9)
        self.play(Create(win), run_time=0.5)
        self.add(lines9)
        gf = grid(FMAP, [4.6, -0.3, 0], GREEN_C, FMAP.max())
        blank = VGroup(*[sq.copy().set_fill(WHITE) for sq in gf])
        lf = Text("feature map, 6 × 6", font_size=28, color=GREY_C).next_to(gf, DOWN, buff=0.25)
        mark = Square(C, stroke_color=ORANGE_C, stroke_width=5).move_to(gf[0])
        out = always_redraw(lambda: Line(node.get_right(), mark.get_center(), stroke_color=ORANGE_C, stroke_width=2.5))
        self.play(FadeIn(blank), FadeIn(lf), FadeIn(mark), run_time=0.6)
        self.add(out)
        self.play(FadeIn(gf[0]), run_time=0.4)
        self.wait(1.0)
        self.snap()

        self.play(Transform(title, Text("Slide: the same 9 weights at every position", font_size=38).to_edge(UP, buff=0.35)),
                  run_time=0.6)
        for k in range(1, 36):
            i, j = divmod(k, 6)
            rt = 0.35 if k < 7 else 0.12
            self.play(win.animate.move_to(gx[(i + 1) * 8 + j + 1].get_center()), mark.animate.move_to(gf[k]), run_time=rt)
            self.add(gf[k])
            self.bring_to_front(mark)
            if k == 14:
                self.snap()
        self.play(Transform(count, Text("36 outputs, still 9 weights + 1 bias: parameter sharing", font_size=32,
                                        color=ORANGE_C).to_edge(DOWN, buff=0.5)), run_time=0.6)
        self.wait(2.5)
        self.snap()


if __name__ == "__main__":
    render(FilterNode, "filter_as_node")
