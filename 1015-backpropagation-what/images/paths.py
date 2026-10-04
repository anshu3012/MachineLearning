"""The dependency tree of the loss, grown from L backwards with the local derivative on every edge (student 1's
numbers), then four paths lit up: the product of the numbers along a path is that parameter's gradient (Manim).
Run: python paths.py -> paths.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image
import manimpango

for f in Path("/usr/share/texmf/fonts/opentype/public/lm").glob("lmroman10-*.otf"):   # pango on topgro misses LM
    manimpango.register_font(str(f))

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MathTex.set_default(color=BLACK)
assert round(-7.36 * 1.6, 2) == -11.78 and round(-7.36 * 0.1 * 8, 2) == -5.89 and round(-7.36 * 0.1, 3) == -0.736

# node: (tex, position, kind)   kind: v = value, w = weight, b = bias
N = {"L": ("L", [1.2, 2.6], "v"), "y": (r"\hat y", [1.2, 1.1], "v"),
     "W2a": ("W^2_{11}", [-5.9, -0.6], "w"), "W2b": ("W^2_{21}", [-4.1, -0.6], "w"), "b2": ("b_{21}", [-2.3, -0.6], "b"),
     "O1": ("O_{11}", [1.0, -0.6], "v"), "O2": ("O_{12}", [5.0, -0.6], "v"),
     "W1a": ("W^1_{11}", [-0.3, -2.9], "w"), "W1b": ("W^1_{21}", [1.0, -2.9], "w"), "b1a": ("b_{11}", [2.3, -2.9], "b"),
     "W1c": ("W^1_{12}", [3.7, -2.9], "w"), "W1d": ("W^1_{22}", [5.0, -2.9], "w"), "b1b": ("b_{12}", [6.3, -2.9], "b")}
# edge: (parent, child, local derivative as text)
E = [("L", "y", "−7.36"), ("y", "W2a", "1.6"), ("y", "W2b", "1.6"), ("y", "b2", "1"), ("y", "O1", "0.1"), ("y", "O2", "0.1"),
     ("O1", "W1a", "8"), ("O1", "W1b", "8"), ("O1", "b1a", "1"), ("O2", "W1c", "8"), ("O2", "W1d", "8"), ("O2", "b1b", "1")]
COL = {"v": GREY_C, "w": BLUE_C, "b": GREEN_C}
PATHS = [(["L", "y", "W2a"], r"\frac{\partial L}{\partial W^2_{11}} = -7.36 \times 1.6 = -11.78"),
         (["L", "y", "b2"], r"\frac{\partial L}{\partial b_{21}} = -7.36 \times 1 = -7.36"),
         (["L", "y", "O1", "W1a"], r"\frac{\partial L}{\partial W^1_{11}} = -7.36 \times 0.1 \times 8 = -5.89"),
         (["L", "y", "O1", "b1a"], r"\frac{\partial L}{\partial b_{11}} = -7.36 \times 0.1 \times 1 = -0.736")]


class Paths(Scene):
    def construct(self):
        snaps = []
        title = Text("Each gradient is a product along a path back from L", font_size=32, weight=BOLD).to_edge(UP, buff=0.2)
        self.add(title)
        nodes = {}
        for k, (tex, p, kind) in N.items():
            m = MathTex(tex, font_size=34)
            box = RoundedRectangle(corner_radius=0.15, width=max(m.width + 0.35, 0.8), height=0.7, color=COL[kind], stroke_width=4,
                                   fill_color=WHITE, fill_opacity=1)
            nodes[k] = VGroup(box, m).move_to([p[0], p[1], 0])
        edges, labs = {}, {}
        for a, b, t in E:
            ln = Line(nodes[a].get_bottom(), nodes[b].get_top(), color=GREY_C, stroke_width=3).set_z_index(-1)
            lab = Text(t, font_size=24, color=RED_C).move_to(ln.point_from_proportion(0.55))
            lab.add_background_rectangle(color=WHITE, opacity=0.9, buff=0.04)
            edges[(a, b)], labs[(a, b)] = ln, lab
        legend = VGroup(Text("blue: weight", font_size=24, color=BLUE_C), Text("green: bias", font_size=24, color=GREEN_C),
                        Text("red: how much the upper box changes", font_size=24, color=RED_C),
                        Text("per unit change of the lower box", font_size=24, color=RED_C)).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to([-4.3, 2.2, 0])
        self.play(FadeIn(nodes["L"], legend), run_time=0.5)
        for group in (E[:1], E[1:6], E[6:]):
            self.play(*[Create(edges[(a, b)]) for a, b, _ in group], *[FadeIn(nodes[b]) for _, b, _ in group],
                      *[FadeIn(labs[(a, b)]) for a, b, _ in group], run_time=1.0)
            self.wait(0.8)
        snaps.append(Image.fromarray(self.renderer.get_frame()))
        formula = None
        for path, tex in PATHS:
            segs = list(zip(path, path[1:]))
            new = MathTex(tex, font_size=32).move_to([-4.0, -2.6, 0])
            anims = [edges[s].animate.set_stroke(RED_C, 8) for s in segs]
            if formula is not None:
                self.remove(formula)
            self.play(*anims, FadeIn(new), run_time=0.8)
            formula = new
            self.wait(1.8)
            snaps.append(Image.fromarray(self.renderer.get_frame()))
            self.play(*[edges[s].animate.set_stroke(GREY_C, 3) for s in segs], run_time=0.3)
        self.snaps = [snaps[0], snaps[1], snaps[3], snaps[4]]


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "frame_rate": 15, "background_color": WHITE, "media_dir": str(media),
                     "output_file": "paths", "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = Paths()
        scene.render()
    mp4 = HERE / "paths.mp4"
    shutil.copy(next(media.rglob("paths.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=8,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse", str(HERE / "paths.gif")], check=True)
    w, h = scene.snaps[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, f in enumerate(scene.snaps[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "paths_frames.png")
    shutil.rmtree(media)
