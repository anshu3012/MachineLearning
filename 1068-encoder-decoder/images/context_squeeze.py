"""The encoder squeezes a sentence into one context vector of fixed size. The LSTM reads one word per step; each word
gets a share of the fixed-size state (drawn as a coloured slice). A 3-word sentence and a 7-word sentence end in the
same number of slots, so with more words each word gets a thinner share. The decoder sees only that vector.
Sentences from the Note's test set (data/translations.csv). A picture of the idea, not of the LSTM's numbers.
Run: python context_squeeze.py -> context_squeeze.mp4, context_squeeze.gif, context_squeeze_frames.png (Manim)"""
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
tr = pd.read_csv(HERE.parent / "data" / "translations.csv")
SHORT = "i like your house ."
LONG = "she accompanied her friend to the concert ."
assert SHORT in set(tr.english) and LONG in set(tr.english)
PALETTE = [BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, "#9D755D", "#72B7B2", "#EECA3B"]
VW, VH = 1.2, 3.0                                      # size of the context vector drawing


def context(n_words):
    """The fixed-size vector, split into one equal slice per word read so far."""
    box = Rectangle(width=VW, height=VH, stroke_color=BLACK, stroke_width=3)
    slices = VGroup(*[Rectangle(width=VW, height=VH / n_words, stroke_width=0, fill_color=PALETTE[k % 8],
                                fill_opacity=0.85) for k in range(n_words)]).arrange(DOWN, buff=0)
    return VGroup(slices, box)


class ContextSqueeze(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def run_sentence(self, sentence, y_words):
        words = sentence.split()
        chips = VGroup(*[Text(w, font_size=26, color=PALETTE[k % 8]) for k, w in enumerate(words)])
        chips.arrange(RIGHT, buff=0.25).move_to([-2.6, y_words, 0])
        if chips.width > 8.2:
            chips.scale_to_fit_width(8.2)
        enc = RoundedRectangle(corner_radius=0.15, width=2.5, height=1.0, color=BLUE_C, fill_color=BLUE_C,
                               fill_opacity=0.12).move_to([-2.6, 0.3, 0])
        enc_l = Text("encoder LSTM", font_size=22, color=BLUE_C).move_to(enc)
        ctx_pos = [1.4, 0.3, 0]
        self.play(FadeIn(chips), FadeIn(enc), FadeIn(enc_l), run_time=0.7)
        ctx = context(1).move_to(ctx_pos)
        for k, chip in enumerate(chips):
            moving = chip.copy()
            self.play(moving.animate.move_to(enc.get_center()).scale(0.6).set_opacity(0), Indicate(chip, scale_factor=1.1),
                      run_time=0.5)
            new = context(k + 1).move_to(ctx_pos)
            if k == 0:
                self.play(FadeIn(new), run_time=0.4)
            else:
                self.play(Transform(ctx, new), run_time=0.4)
            ctx = new if k == 0 else ctx
            if sentence == LONG and k == 3:
                self.snap()
        return VGroup(chips, enc, enc_l), ctx

    def construct(self):
        self.snaps = []
        title = Text("The encoder squeezes the sentence into one vector", font_size=32).to_edge(UP, buff=0.3)
        self.play(FadeIn(title))
        lab = Text("context vector:\nthe same size\nfor every sentence", font_size=24).move_to([4.6, 0.3, 0])
        group, ctx = self.run_sentence(SHORT, 2.2)
        self.play(FadeIn(lab))
        dec = RoundedRectangle(corner_radius=0.15, width=2.5, height=1.0, color=ORANGE_C, fill_color=ORANGE_C,
                               fill_opacity=0.12).move_to([1.4, -2.6, 0])
        dec_l = Text("decoder LSTM", font_size=22, color=ORANGE_C).move_to(dec)
        arr = Arrow(ctx.get_bottom(), dec.get_top(), buff=0.1, color=GREY_C)
        out = Text(tr.set_index("english").predicted[SHORT], font_size=24, color=ORANGE_C).next_to(dec, RIGHT, buff=0.4)
        self.play(FadeIn(dec), FadeIn(dec_l), GrowArrow(arr), run_time=0.7)
        self.play(FadeIn(out), run_time=0.6)
        note = Text("the decoder sees only this vector", font_size=22, color=GREY_C).next_to(dec, LEFT, buff=0.4)
        self.play(FadeIn(note))
        self.wait(1.0)
        self.snap()
        self.play(FadeOut(VGroup(group, ctx, dec, dec_l, arr, out, note)), run_time=0.6)
        group, ctx = self.run_sentence(LONG, 2.2)
        self.wait(0.6)
        self.snap()
        msg = VGroup(Text("5 tokens or 8 tokens: the same space", font_size=26),
                     Text("with more words, each word gets a thinner share", font_size=24, color=RED_C)
                     ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(msg))
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
                     "output_file": "context_squeeze", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = ContextSqueeze()
        scene.render()
    mp4 = HERE / "context_squeeze.mp4"
    shutil.copy(next(media.rglob("context_squeeze.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "context_squeeze.gif")], check=True)
    key_frames_grid([scene.snaps[i] for i in (0, 1, 2, 3)], HERE / "context_squeeze_frames.png")
    shutil.rmtree(media)
