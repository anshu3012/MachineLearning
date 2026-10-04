"""The two passes of a bidirectional tagger on a real CoNLL-2000 test sentence (from the Notebook, seed 1).
The forward pass sweeps left to right and the unidirectional LSTM's tags appear: it tags "about" IN (preposition).
The backward pass then sweeps right to left; once it has read the "$" after "about", the BiLSTM tags "about" RB
(adverb), the true tag. Run: python birnn_sweep.py  -> birnn_sweep.gif, birnn_sweep_frames.png (Manim + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import pandas as pd
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
ex = pd.read_csv(HERE.parent / "data" / "pos_example.csv", keep_default_na=False)
START = ex.index[ex.word == "that"][0]                     # earlier words shown as "..."
ex = ex.iloc[START:].reset_index(drop=True)
ABOUT = ex.index[ex.word == "about"][0]
assert ex.unidirectional[ABOUT] == "IN" and ex.bidirectional[ABOUT] == ex.true[ABOUT] == "RB"
X0, DX = -3.5, 1.42                                        # x of "that", gap between words
xs = [X0 + k * DX for k in range(len(ex))]
Y_BACK, Y_WORD, Y_FWD, Y_UNI, Y_BI, Y_TRUE = 1.75, 0.65, -0.45, -1.6, -2.45, -3.3


def cell(x, y, colour):
    return RoundedRectangle(corner_radius=0.1, width=1.0, height=0.6, stroke_color=colour, stroke_width=3,
                            fill_color=colour, fill_opacity=0.25).move_to([x, y, 0])


def tag(text, x, y, ok):
    return Text(text, font_size=30, color=GREEN_C if ok else RED_C, weight=BOLD).move_to([x, y, 0])


class BiSweep(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        title = Text("tagging each word: one pass or two?", font_size=34).to_edge(UP, buff=0.3)
        words = VGroup(Text("...", font_size=32, color=GREY_C).move_to([X0 - 1.2, Y_WORD, 0]),
                       *[Text(w, font_size=32, weight=BOLD if k == ABOUT else NORMAL).move_to([xs[k], Y_WORD, 0])
                         for k, w in enumerate(ex.word)])
        lab = dict(font_size=24, color=GREY_C)
        labels = VGroup(Text("backward", **lab, ).move_to([-6.1, Y_BACK, 0]),
                        Text("forward", **lab).move_to([-6.1, Y_FWD, 0]),
                        Text("LSTM", **lab).move_to([-6.1, Y_UNI, 0]),
                        Text("BiLSTM", **lab).move_to([-6.1, Y_BI, 0]),
                        Text("true tag", **lab).move_to([-6.1, Y_TRUE, 0]))
        labels[0].set_color(GREEN_C)
        labels[1].set_color(BLUE_C)
        self.play(FadeIn(title), FadeIn(words), FadeIn(labels[1]), FadeIn(labels[2]))

        # forward pass: left to right, the LSTM's tag appears as soon as its state reaches the word
        prev = cell(X0 - 1.2, Y_FWD, BLUE_C)
        self.add(prev)
        for k in range(len(ex)):
            c = cell(xs[k], Y_FWD, BLUE_C)
            self.play(GrowArrow(Arrow(prev.get_right(), c.get_left(), buff=0.02, color=BLUE_C, stroke_width=4,
                                      max_tip_length_to_length_ratio=0.5)), FadeIn(c), run_time=0.35)
            t = tag(ex.unidirectional[k], xs[k], Y_UNI, ex.unidirectional[k] == ex.true[k])
            self.play(FadeIn(t, shift=DOWN * 0.2), run_time=0.25)
            prev = c
            if k == ABOUT:
                seen = SurroundingRectangle(VGroup(words[0], words[ABOUT + 1]), color=BLUE_C, buff=0.12)
                note = Text('read so far: "... that totaled about"  ->  IN (preposition)', font_size=26,
                            color=BLUE_C).next_to(title, DOWN, buff=0.2)
                self.play(Create(seen), FadeIn(note), run_time=0.6)
                self.wait(1.4)
                self.snap()
                self.play(FadeOut(seen), FadeOut(note), run_time=0.4)
        self.wait(0.8)
        self.snap()

        # backward pass: right to left from the end of the sentence
        self.play(FadeIn(labels[0]), run_time=0.4)
        prev = cell(xs[-1], Y_BACK, GREEN_C)                # starts at the last word, from zeros
        self.play(FadeIn(prev), run_time=0.35)
        for k in range(len(ex) - 2, ABOUT - 1, -1):
            c = cell(xs[k], Y_BACK, GREEN_C)
            self.play(GrowArrow(Arrow(prev.get_left(), c.get_right(), buff=0.02, color=GREEN_C, stroke_width=4,
                                      max_tip_length_to_length_ratio=0.5)), FadeIn(c), run_time=0.35)
            prev = c
        seen = SurroundingRectangle(VGroup(words[ABOUT + 1], words[-1]), color=GREEN_C, buff=0.12)
        note = Text('backward state at "about" has read "about $ 76.7 million ."', font_size=26,
                    color=GREEN_C).next_to(title, DOWN, buff=0.2)
        self.play(Create(seen), FadeIn(note), run_time=0.6)
        self.wait(1.2)
        self.snap()
        self.play(FadeOut(seen), run_time=0.3)
        for k in range(ABOUT - 1, -1, -1):
            c = cell(xs[k], Y_BACK, GREEN_C)
            self.play(GrowArrow(Arrow(prev.get_left(), c.get_right(), buff=0.02, color=GREEN_C, stroke_width=4,
                                      max_tip_length_to_length_ratio=0.5)), FadeIn(c), run_time=0.3)
            prev = c

        # both states joined at every word: the BiLSTM's tags, then the true tags
        self.play(FadeOut(note), FadeIn(labels[3]), run_time=0.4)
        bi = VGroup(*[tag(ex.bidirectional[k], xs[k], Y_BI, ex.bidirectional[k] == ex.true[k]) for k in range(len(ex))])
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in bi], lag_ratio=0.15), run_time=1.6)
        true = VGroup(*[Text(t, font_size=28, color=GREY_C).move_to([xs[k], Y_TRUE, 0]) for k, t in enumerate(ex.true)])
        self.play(FadeIn(labels[4]), FadeIn(true), run_time=0.6)
        col = SurroundingRectangle(VGroup(words[ABOUT + 1], true[ABOUT]), color=BLACK, buff=0.12)
        end = Text('"about $ 76.7 million": about is an adverb (RB)', font_size=26).next_to(title, DOWN, buff=0.2)
        self.play(Create(col), FadeIn(end), run_time=0.7)
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
                     "output_file": "birnn_sweep", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = BiSweep()
        scene.render()
    mp4 = HERE / ".birnn_sweep.mp4"
    shutil.copy(next(media.rglob("birnn_sweep.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "birnn_sweep.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "birnn_sweep_frames.png")
    shutil.rmtree(media)
    mp4.unlink()
