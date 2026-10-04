"""One sentence through a whole trained transformer: "we're friends ." is embedded, passes the 2 encoder blocks
(each word's 128 numbers drawn as a coloured strip; the blocks' self-attention weights as dots), then the decoder
writes the French one word per step: masked self-attention over the words written so far, cross-attention to the
English words (line width = weight), the 5 most likely next words, and the chosen word appended to the input.
Data: data/capstone.json, exported by the transformer inference Note's Notebook (section 8): its 2 + 2 block model,
d_model = 128, 4 heads; weights are means over the 4 heads.
Run: python capstone.py -> capstone.mp4, capstone.gif, capstone_frames.png (Manim)"""
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MarkupText.set_default(color=BLACK, font="Latin Modern Roman")
C = json.load(open(HERE.parent / "data" / "capstone.json"))
EN = C["english"]
STEPS = C["steps"]
SW = 0.026                                                   # width of one number in a strip


def strip(vec, scale):
    g = VGroup()
    for v in vec:
        col = ManimColor(BLUE_C if v >= 0 else RED_C).interpolate(WHITE, 1 - min(abs(v) / scale, 1) * 0.9)
        g.add(Rectangle(width=SW, height=0.42, stroke_width=0, fill_color=col, fill_opacity=1))
    return g.arrange(RIGHT, buff=0)


def enc_rows(stage):
    vecs = np.array(C["enc_vectors"][stage])
    scale = np.percentile(np.abs(vecs), 95)
    return VGroup(*[strip(v, scale) for v in vecs])


def esc(w):
    return w.replace("<", "&lt;").replace(">", "&gt;")


class Capstone(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        title = Text("One sentence through the trained transformer", font_size=30).to_edge(UP, buff=0.2)
        self.play(FadeIn(title), run_time=0.6)
        # ---- encoder (left half)
        ex, ys = -3.85, [1.7, 0.9, 0.1]
        words = VGroup(*[Text(w, font_size=26, color=BLUE_C).move_to([-6.0, y, 0], aligned_edge=RIGHT) for w, y in zip(EN, ys)])
        stage_lab = Text("embedding × √128 + position", font_size=22, color=GREY_C).move_to([ex, 2.45, 0])
        rows = enc_rows(0)
        for r, y in zip(rows, ys):
            r.move_to([ex, y, 0])
        self.play(FadeIn(words), run_time=0.6)
        self.play(FadeIn(stage_lab), *[TransformFromCopy(w, r) for w, r in zip(words, rows)], run_time=1.2)
        self.wait(0.5)
        self.snap()
        for b in range(2):
            Wt = np.array(C["enc_weights"][b])
            dots = VGroup()
            for i, y in enumerate(ys):
                for j in range(3):
                    dots.add(Circle(radius=0.05 + 0.25 * np.sqrt(Wt[i, j]), color=PURPLE_C, fill_opacity=0.8,
                                    stroke_width=0).move_to([-1.55 + 0.55 * j, y, 0]))
            att_lab = Text(f"encoder block {b + 1}: self-attention", font_size=22, color=PURPLE_C).move_to([-1.3, 2.45, 0])
            new = enc_rows(b + 1)
            for r, y in zip(new, ys):
                r.move_to([ex, y, 0])
            self.play(FadeIn(dots), FadeIn(att_lab), run_time=0.8)
            lab = Text(f"after encoder block {b + 1}", font_size=22, color=GREY_C).move_to(stage_lab)
            self.play(Transform(rows, new), Transform(stage_lab, lab), run_time=1.2)
            self.play(FadeOut(dots), FadeOut(att_lab), run_time=0.5)
        henc = MarkupText("H<sub>enc</sub>: computed once, read at every step", font_size=22, color=BLUE_C).move_to([ex - 0.6, -0.55, 0])
        self.play(FadeIn(henc))
        self.snap()
        # ---- decoder (right half), one step per word
        dx0, dy = -0.2, -2.3
        dec_title = Text("decoder: one run per word", font_size=24, color=ORANGE_C).move_to([4.4, 2.55, 0])
        self.play(FadeIn(dec_title), run_time=0.5)
        inp = VGroup()
        for t, s in enumerate(STEPS):
            words_in = s["input"]
            if t == 0:
                tok = Text(esc(words_in[0]).replace("&lt;", "<").replace("&gt;", ">"), font_size=24, color=ORANGE_C)
                tok.move_to([dx0 + 0.6, dy, 0])
                inp.add(tok)
                self.play(FadeIn(tok), run_time=0.5)
            newest = inp[-1]
            selfw = s["self_last"][0]
            sd = VGroup(*[Circle(radius=0.05 + 0.22 * np.sqrt(w), color=PURPLE_C, fill_opacity=0.8, stroke_width=0)
                          .next_to(inp[k], DOWN, buff=0.18) for k, w in enumerate(selfw)])
            sd_lab = Text("masked self-attention of the newest word", font_size=20, color=PURPLE_C).move_to([2.3, dy - 1.0, 0])
            crossw = s["cross_last"][-1]
            lines = VGroup(*[Line(newest.get_top(), rows[j].get_right(), color=GREEN_C, stroke_width=1 + 14 * w,
                                  stroke_opacity=0.25 + 0.75 * w) for j, w in enumerate(crossw)])
            c_lab = Text("cross-attention:\nreads the English", font_size=20, color=GREEN_C).move_to([5.6, -0.9, 0])
            self.play(FadeIn(sd), FadeIn(sd_lab), run_time=0.7)
            self.play(Create(lines), FadeIn(c_lab), run_time=0.8)
            top = s["top"]
            bars = VGroup()
            for k, (w, p) in enumerate(top):
                y = 1.75 - 0.42 * k
                bar = Rectangle(width=max(2.0 * p, 0.02), height=0.3, stroke_width=0,
                                fill_color=ORANGE_C if k == 0 else GREY_C, fill_opacity=1)
                bar.move_to([3.75, y, 0], aligned_edge=LEFT)
                lab = Text(w, font_size=20).move_to([3.65, y, 0], aligned_edge=RIGHT)
                val = Text(f"{p:.3f}", font_size=17, color=GREY_C).next_to(bar, RIGHT, buff=0.08)
                bars.add(VGroup(bar, lab, val))
            b_lab = Text(f"step {t + 1}: 5 most likely next words", font_size=20).move_to([4.4, 2.1, 0])
            self.play(FadeIn(bars), FadeIn(b_lab), run_time=0.8)
            self.wait(0.6)
            if t in (0, 2):
                self.snap()
            chosen = top[0][0]
            if chosen == "<end>":
                done = Text("<end>: stop", font_size=24, color=RED_C).move_to([5.6, -0.1, 0])
                self.play(Indicate(bars[0], color=RED_C), FadeIn(done), run_time=0.8)
                break
            new_tok = Text(chosen, font_size=24, color=ORANGE_C).next_to(inp[-1], RIGHT, buff=0.3)
            self.play(TransformFromCopy(bars[0][1], new_tok), run_time=0.8)
            inp.add(new_tok)
            self.play(FadeOut(VGroup(sd, sd_lab, lines, c_lab, bars, b_lab)), run_time=0.4)
        out = Text("French: " + " ".join(s["top"][0][0] for s in STEPS[:-1]), font_size=28, color=ORANGE_C)
        out.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(out))
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
                     "output_file": "capstone", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = Capstone()
        scene.render()
    snaps = scene.snaps
    snaps = [snaps[0], snaps[2], snaps[3], snaps[-1]]          # embeddings, steps 1 and 3, final
    mp4 = HERE / "capstone.mp4"
    shutil.copy(next(media.rglob("capstone.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "capstone.gif")], check=True)
    key_frames_grid(snaps, HERE / "capstone_frames.png")
    shutil.rmtree(media)
