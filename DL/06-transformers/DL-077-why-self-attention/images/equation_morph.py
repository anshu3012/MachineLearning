"""Luong attention turning into self-attention. Top: the French decoder states ask the English encoder states
(decoder step 2, "la"); then the French row leaves and the English sentence asks itself. Bottom: the three
equations, in which the decoder state becomes a query (blue), the encoder state that is compared becomes a key
(orange) and the encoder state that is mixed becomes a value (green). Sentence pair: the Note's own
("Turn off the light." / "Éteins la lumière."). Our own design.
Run: python equation_morph.py -> equation_morph.gif, equation_morph_frames.png (Manim)"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image
import manimpango

for f in Path("/usr/share/texmf/fonts/opentype/public/lm").glob("lmroman10-*.otf"):   # pango on topgro misses LM
    manimpango.register_font(str(f))

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MathTex.set_default(color=BLACK)
FR, EN = ["Éteins", "la", "lumière"], ["turn", "off", "the", "light"]
ROW_ASK, ROW_ANS = 2.05, 0.5          # y of the row that asks and of the row that is asked


def word_row(words, y, colour):
    boxes = VGroup()
    for w in words:
        t = Text(w, font_size=30)
        box = RoundedRectangle(width=1.75, height=0.62, corner_radius=0.1, color=colour, stroke_width=3)
        boxes.add(VGroup(box, t))
    boxes.arrange(RIGHT, buff=0.35).move_to([0, y, 0])
    return boxes


def tags(row, symbols, colours, direction):
    out = VGroup()
    for k, cell in enumerate(row):
        parts = [MathTex(s.format(k + 1), font_size=38, color=c) for s, c in zip(symbols, colours)]
        out.add(VGroup(*parts).arrange(RIGHT, buff=0.18).next_to(cell, direction, buff=0.12))
    return out


class EquationMorph(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        title = Text("The same three equations", font_size=36, weight=BOLD).to_edge(UP, buff=0.25)
        head = Text("Luong attention: the French output asks the English input", font_size=28, color=GREY_C)
        head.next_to(title, DOWN, buff=0.15)
        fr, en = word_row(FR, ROW_ASK, BLUE_C), word_row(EN, ROW_ANS, ORANGE_C)
        fr_tag = tags(fr, ["s_{}"], [BLUE_C], UP)
        en_tag = tags(en, ["h_{}"], [ORANGE_C], DOWN)
        side_a = Text("decoder", font_size=24, color=GREY_C).next_to(fr, LEFT, buff=0.4)
        side_b = Text("encoder", font_size=24, color=GREY_C).next_to(en, LEFT, buff=0.4)
        links = VGroup(*[Line(fr[1].get_bottom(), c.get_top(), color=GREY_C, stroke_width=3) for c in en])
        self.play(FadeIn(title), FadeIn(head))
        self.play(FadeIn(fr), FadeIn(fr_tag), FadeIn(en), FadeIn(en_tag), FadeIn(side_a), FadeIn(side_b))
        self.play(Create(links), run_time=0.8)

        def equations(rows):
            eqs = VGroup(*[MathTex(*r, font_size=44) for r in rows])
            for k, e in enumerate(eqs):
                e.move_to([-0.8, -0.95 - 0.85 * k, 0])
            return eqs

        luong = equations([["e_{ij}", "=", "s_i", r"\cdot", "h_j"],
                           [r"\alpha_{ij}", "=", r"\mathrm{softmax}_j(", "e_{ij}", ")"],
                           ["c_i", "=", r"\sum_j", r"\alpha_{ij}", "h_j"]])
        selfa = equations([["s_{ij}", "=", "q_i", r"\cdot", "k_j"],
                           ["w_{ij}", "=", r"\mathrm{softmax}_j(", "s_{ij}", ")"],
                           ["y_i", "=", r"\sum_j", "w_{ij}", "v_j"]])
        for eqs in (luong, selfa):
            eqs[0][2].set_color(BLUE_C), eqs[0][4].set_color(ORANGE_C), eqs[2][4].set_color(GREEN_C)
        steps = VGroup(*[Text(s, font_size=26, color=GREY_C).move_to([-5.6, -0.95 - 0.85 * k, 0], aligned_edge=LEFT)
                         for k, s in enumerate(["1. scores", "2. weights", "3. output"])])
        for k in range(3):
            self.play(FadeIn(steps[k]), Write(luong[k]), run_time=0.9)
        self.wait(1.0)
        self.snap()

        roles = VGroup(Text("query: the one asking", font_size=26, color=BLUE_C),
                       Text("key: compared with the query", font_size=26, color=ORANGE_C),
                       Text("value: mixed into the output", font_size=26, color=GREEN_C))
        roles[0].move_to([1.7, -0.7, 0], aligned_edge=LEFT)
        roles[1].move_to([1.7, -1.2, 0], aligned_edge=LEFT)
        roles[2].move_to([1.7, -2.65, 0], aligned_edge=LEFT)
        for r, target in zip(roles, (luong[0][2], luong[0][4], luong[2][4])):
            self.play(FadeIn(r), Indicate(target, color=r.get_color(), scale_factor=1.5), run_time=0.9)
        self.wait(1.2)
        self.snap()

        # the French row leaves; the English sentence takes its place and asks itself
        head2 = Text("Self-attention: the sentence asks itself", font_size=28, color=GREY_C).move_to(head)
        en_top = word_row(EN, ROW_ASK, BLUE_C)
        q_tag = tags(en_top, ["q_{}"], [BLUE_C], UP)
        kv_tag = tags(en, ["k_{}", "v_{}"], [ORANGE_C, GREEN_C], DOWN)
        links2 = VGroup(*[Line(en_top[1].get_bottom(), c.get_top(), color=GREY_C, stroke_width=3) for c in en])
        self.play(FadeOut(fr), FadeOut(fr_tag), FadeOut(links), FadeOut(side_a), FadeOut(side_b),
                  Transform(head, head2), run_time=0.9)
        self.play(TransformFromCopy(en, en_top), run_time=1.2)
        self.play(FadeIn(q_tag), ReplacementTransform(en_tag, kv_tag), Create(links2), run_time=1.0)
        self.wait(0.8)
        self.snap()
        for k in range(3):
            self.play(*[ReplacementTransform(a, b) for a, b in zip(luong[k], selfa[k])], run_time=1.1)
        self.wait(1.0)

        note = Text("queries, keys and values all come from one sentence: \"self\"", font_size=27)
        note.to_edge(DOWN, buff=0.12)
        self.play(FadeIn(note))
        self.wait(3.0)
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
                     "output_file": "equation_morph", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = EquationMorph()
        scene.render()
    mp4 = next(media.rglob("equation_morph.mp4"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "equation_morph.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "equation_morph_frames.png")
    shutil.rmtree(media)
