"""From one equation per student to y_hat = X beta, on the four students of Section 6.1 (CGPA 6.89, 5.12, 7.82, 7.42).
1. four prediction equations, one per student; 2. the left sides stack into the vector y_hat; 3. the numbers stack
into the matrix X and the coefficients, the same in every equation, are written once as the vector beta; 4. the
first column of X is the 1s that multiply beta_0; 5. y_hat = X beta. Our own design; no source to credit.
Manim (symbols move from the equations into the matrices). Run: python stack_equations.py -> .mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MathTex.set_default(color=BLACK)
CGPA = ["6.89", "5.12", "7.82", "7.42"]


class Stack(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def say(self, old, text):
        new = Text(text, font_size=34).to_edge(UP, buff=0.5)
        self.play(FadeOut(old), FadeIn(new), run_time=0.6) if old else self.play(FadeIn(new), run_time=0.6)
        return new

    def construct(self):
        self.snaps = []
        title = self.say(None, "1. one prediction equation per student")
        eqs = VGroup(*[MathTex(rf"\hat y_{i + 1}", "=", r"\beta_0", r"\cdot", "1", "+", r"\beta_1", r"\cdot", c,
                               font_size=52) for i, c in enumerate(CGPA)]).arrange(DOWN, buff=0.45).shift(0.3 * DOWN)
        for e in eqs:
            e[2].set_color(ORANGE_C), e[6].set_color(ORANGE_C), e[4].set_color(BLUE_C), e[8].set_color(BLUE_C)
            self.play(Write(e), run_time=0.7)
        self.wait(1)
        self.snap()

        yv = Matrix([[rf"\hat y_{i + 1}"] for i in range(4)], element_to_mobject_config=dict(font_size=52))
        xm = Matrix([["1", c] for c in CGPA], h_buff=1.6, element_to_mobject_config=dict(font_size=52)).set_color(BLUE_C)
        bv = Matrix([[r"\beta_0"], [r"\beta_1"]], element_to_mobject_config=dict(font_size=52)).set_color(ORANGE_C)
        eq = MathTex("=", font_size=52)
        row = VGroup(yv, eq, xm, bv).arrange(RIGHT, buff=0.35).shift(0.3 * DOWN)
        for m in (yv, xm, bv):
            m.get_brackets().set_color(BLACK)

        title = self.say(title, "2. the left sides stack into one vector")
        self.play(*[ReplacementTransform(eqs[i][0], yv.get_entries()[i]) for i in range(4)],
                  ReplacementTransform(VGroup(*[e[1] for e in eqs]), eq), FadeIn(yv.get_brackets()), run_time=1.5)
        self.wait(0.8)
        title = self.say(title, "3. the numbers stack into X; the coefficients are written once")
        self.play(*[ReplacementTransform(eqs[i][4], xm.get_entries()[2 * i]) for i in range(4)],
                  *[ReplacementTransform(eqs[i][8], xm.get_entries()[2 * i + 1]) for i in range(4)],
                  FadeIn(xm.get_brackets()), *[FadeOut(VGroup(e[3], e[5], e[7])) for e in eqs],
                  ReplacementTransform(VGroup(*[e[2] for e in eqs]), bv.get_entries()[0]),
                  ReplacementTransform(VGroup(*[e[6] for e in eqs]), bv.get_entries()[1]),
                  FadeIn(bv.get_brackets()), run_time=2.5)
        self.wait(1.2)
        self.snap()
        title = self.say(title, "4. the first column of X is all 1s")
        ones = SurroundingRectangle(xm.get_columns()[0], color=GREEN_C, buff=0.12)
        note = Text("the column of 1s multiplies the intercept", font_size=28, color=GREEN_C).next_to(row, DOWN, buff=0.5)
        self.play(Create(ones), FadeIn(note))
        self.wait(1.5)
        self.snap()
        self.play(FadeOut(ones), FadeOut(note))
        title = self.say(title, "5. all four predictions in one line")
        labels = VGroup(MathTex(r"\hat y", font_size=60).next_to(yv, DOWN, buff=0.4),
                        MathTex("X", font_size=60, color=BLUE_C).next_to(xm, DOWN, buff=0.4),
                        MathTex(r"\beta", font_size=60, color=ORANGE_C).next_to(bv, DOWN, buff=0.4))
        labels[2].align_to(labels[1], DOWN), labels[0].align_to(labels[1], DOWN)
        eq2 = MathTex("=", font_size=60).move_to([eq.get_x(), labels[1].get_y(), 0])
        self.play(FadeIn(labels), FadeIn(eq2))
        self.wait(2.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    name = "stack_equations"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = Stack()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=48:stats_mode=diff[p];"
                    "[b][p]paletteuse=dither=none:diff_mode=rectangle", str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
