"""Matrix shapes of the three layers of the 4-3-2-1 network, then the nested formula (Manim).
Each layer: (rows x cols of W transposed)(previous activation) + bias -> this layer's activation. The inner sizes must
match and drop out; the outer sizes give the result. Then the three layers nest into one formula.
Run: python shapes.py -> shapes.mp4, .gif, _frames.png"""
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
LAYERS = [(1, 3, 4, BLUE_C), (2, 2, 3, ORANGE_C), (3, 1, 2, GREEN_C)]        # layer, nodes out, nodes in
C = 0.3                                                                       # cell size


def block(rows, cols, color):
    return VGroup(*[Square(side_length=C, stroke_width=2, stroke_color=color, fill_color=color, fill_opacity=0.2)
                    .move_to([c * C, -r * C, 0]) for r in range(rows) for c in range(cols)])


class Shapes(Scene):
    def construct(self):
        snaps = []
        title = Text("Each layer: one matrix product, one added bias", font_size=34, weight=BOLD).to_edge(UP, buff=0.25)
        self.add(title)
        ys = [1.6, -0.3, -2.2]
        for (k, out, inn, col), y in zip(LAYERS, ys):
            name = Text(f"layer {k}", font_size=30, color=col).move_to([-6.0, y, 0])
            Wt, a, b, res = block(out, inn, col), block(inn, 1, GREY_C), block(out, 1, col), block(out, 1, col)
            Wt.move_to([-3.9, y, 0]); a.move_to([-2.3, y, 0]); b.move_to([-1.0, y, 0]); res.move_to([0.6, y, 0])
            plus = MathTex("+", font_size=40).move_to([-1.65, y, 0]); arr = MathTex(r"\rightarrow", font_size=40).move_to([-0.2, y, 0])
            tex = MathTex(f"({out}", r"\times", f"{inn})", f"({inn}", r"\times", "1)", "+", f"({out}", r"\times", "1)", r"\rightarrow",
                          f"({out}", r"\times", "1)", font_size=34).move_to([3.9, y, 0])
            lab = MathTex(rf"W^{{{k}\mathsf T}}", rf"a^{{{k-1}}}", rf"b^{{{k}}}", rf"a^{{{k}}}", font_size=32)
            for m, t in zip(lab, (Wt, a, b, res)):
                m.next_to(t, DOWN, buff=0.12)
            self.play(FadeIn(name, Wt, a, lab[0], lab[1]), FadeIn(tex[:6]), run_time=0.7)
            inner = VGroup(tex[2], tex[3])
            self.play(inner.animate.set_color(RED_C), Indicate(Wt[:inn], color=RED_C), Indicate(a, color=RED_C), run_time=0.9)
            self.play(inner.animate.set_color("#BBBBBB"), VGroup(tex[0], tex[5]).animate.set_color(GREEN_C), run_time=0.5)
            self.play(FadeIn(plus, b, lab[2], tex[6:10]), run_time=0.5)
            self.play(FadeIn(arr, res, lab[3], tex[10:]), run_time=0.5)
            self.wait(0.6)
            snaps.append(Image.fromarray(self.renderer.get_frame()))
        note = Text("inner sizes match and drop out; outer sizes give the result", font_size=28, color=GREY_C).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(1.5)
        snaps[-1] = Image.fromarray(self.renderer.get_frame())
        # the nested formula
        self.play(FadeOut(*[m for m in self.mobjects if m is not title]), run_time=0.5)
        title2 = Text("The three layers nest into one formula", font_size=34, weight=BOLD).to_edge(UP, buff=0.25)
        self.play(Transform(title, title2), run_time=0.4)
        f1 = MathTex(r"\sigma(W^{1\mathsf T} a^{0} + b^{1})", font_size=44, color=BLUE_C)
        cap = Text("layer 1 gives a¹", font_size=30, color=BLUE_C).move_to([0, -1.6, 0])
        self.play(Write(f1), FadeIn(cap), run_time=1.0)
        self.wait(0.8)
        f2 = MathTex(r"\sigma\big(W^{2\mathsf T}\,", r"\sigma(W^{1\mathsf T} a^{0} + b^{1})", r"+ b^{2}\big)", font_size=44)
        f2[0].set_color(ORANGE_C); f2[1].set_color(BLUE_C); f2[2].set_color(ORANGE_C)
        cap2 = Text("layer 2 wraps around it and gives a²", font_size=30, color=ORANGE_C).move_to(cap)
        self.play(ReplacementTransform(f1, f2[1]), FadeIn(f2[0], f2[2]), FadeOut(cap), FadeIn(cap2), run_time=1.0)
        self.wait(0.8)
        f3 = MathTex(r"\hat y =", r"\sigma\Big(W^{3\mathsf T}\,", r"\sigma\big(W^{2\mathsf T}\,", r"\sigma(W^{1\mathsf T} a^{0} + b^{1})", r"+ b^{2}\big)",
                     r"+ b^{3}\Big)", font_size=40)
        for i, c in zip(range(6), (BLACK, GREEN_C, ORANGE_C, BLUE_C, ORANGE_C, GREEN_C)):
            f3[i].set_color(c)
        cap3 = Text("layer 3 wraps around both and gives the prediction", font_size=30, color=GREEN_C).move_to(cap)
        self.play(ReplacementTransform(f2[0], f3[2]), ReplacementTransform(f2[1], f3[3]), ReplacementTransform(f2[2], f3[4]),
                  FadeIn(f3[0], f3[1], f3[5]), FadeOut(cap2), FadeIn(cap3), run_time=1.0)
        self.wait(2.2)
        snaps.append(Image.fromarray(self.renderer.get_frame()))
        self.snaps = snaps


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "frame_rate": 15, "background_color": WHITE, "media_dir": str(media),
                     "output_file": "shapes", "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = Shapes()
        scene.render()
    mp4 = HERE / "shapes.mp4"
    shutil.copy(next(media.rglob("shapes.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse", str(HERE / "shapes.gif")], check=True)
    w, h = scene.snaps[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, f in enumerate(scene.snaps[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "shapes_frames.png")
    shutil.rmtree(media)
