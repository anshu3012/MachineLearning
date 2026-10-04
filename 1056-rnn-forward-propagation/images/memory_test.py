"""Section 6.3 test, animated: "movie was good" and "movie not good" go through the hand-picked weights of
section 5.3, first with the feedback W_h, then with W_h = 0. With W_h the middle word changes h_3; without it the
two h_3 are identical. Weights copied from the Notebook; checked against data/worked_example.csv.
Run: python memory_test.py  -> memory_test.gif, memory_test_frames.png (Manim)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MarkupText.set_default(color=BLACK, font="Latin Modern Roman")

vocab = ["movie", "was", "good", "bad", "not"]
W_i = np.array([[0.2, -0.1, 0.0], [0.0, 0.1, 0.1], [0.8, 0.3, -0.5], [-0.8, -0.3, 0.5], [-0.6, 0.2, 0.4]])
W_h = np.array([[0.5, 0.0, 0.1], [0.2, 0.4, 0.0], [0.0, -0.3, 0.5]])


def forward(sentence, Wh):
    h, out = np.zeros(3), []
    for w in sentence.split():
        h = np.tanh(W_i[vocab.index(w)] + h @ Wh)
        out.append(h)
    return out


REVIEWS = ("movie was good", "movie not good")
RUNS = {"on": [forward(r, W_h) for r in REVIEWS], "off": [forward(r, np.zeros((3, 3))) for r in REVIEWS]}
ref = pd.read_csv(HERE.parent / "data" / "worked_example.csv")
assert np.allclose(np.array(RUNS["on"][0]), ref[["h1", "h2", "h3"]].values, atol=1e-4)
assert np.allclose(RUNS["on"][1][-1], [0.532, 0.240, -0.336], atol=1e-3)         # table of section 6.3
assert np.allclose(RUNS["off"][0][-1], RUNS["off"][1][-1])
XS, YS = (-3.9, 0.0, 3.9), (1.0, -1.9)


def state(values):
    cells = VGroup()
    for v in values:
        colour = ManimColor(BLUE_C if v >= 0 else RED_C).interpolate(WHITE, 1 - min(abs(v) / 0.8, 1) * 0.85)
        sq = Rectangle(width=0.95, height=0.7, stroke_color=GREY_C, stroke_width=2, fill_color=colour, fill_opacity=1)
        cells.add(VGroup(sq, Text(f"{v:.2f}", font_size=28).move_to(sq)))
    return cells.arrange(RIGHT, buff=0)


class MemoryTest(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        title = Text("Does the last state remember the middle word?", font_size=34).to_edge(UP, buff=0.3)
        self.add(title)
        for r, y in zip(REVIEWS, YS):                                   # row labels and the words
            for k, (w, x) in enumerate(zip(r.split(), XS)):
                col = ORANGE_C if w in ("was", "not") else BLUE_C
                self.add(Text(w, font_size=30, color=col).move_to([x, y - 0.7, 0]))
            for k, x in enumerate(XS):
                self.add(MarkupText(f"h<sub>{k + 1}</sub>", font_size=26, color=GREY_C).move_to([x, y + 0.6, 0]))
        for mode, label, colour in (("on", "feedback on: h<sub>t</sub> uses h<sub>t-1</sub> W<sub>h</sub>", RED_C),
                                    ("off", "feedback cut: W<sub>h</sub> = 0", GREY_C)):
            head = MarkupText(label, font_size=30, color=colour).next_to(title, DOWN, buff=0.25)
            arrows = VGroup(*[Arrow([XS[k] + 1.5, y, 0], [XS[k + 1] - 1.5, y, 0], buff=0.05, stroke_width=5,
                                    color=colour) for y in YS for k in range(2)])
            if mode == "off":
                arrows.set_opacity(0.25)
                arrows.add(*[Cross(a, stroke_width=4, scale_factor=0.5) for a in arrows.copy()])
            self.play(FadeIn(head), FadeIn(arrows), run_time=0.8)
            boxes = VGroup()
            for k in range(3):
                new = VGroup(*[state(RUNS[mode][i][k]).move_to([XS[k], y, 0]) for i, y in enumerate(YS)])
                self.play(FadeIn(new, shift=RIGHT * 0.3), run_time=0.9)
                boxes.add(new)
                self.wait(0.4)
                if k == 1:
                    self.snap()
            last = boxes[2]
            same = np.allclose(RUNS[mode][0][2], RUNS[mode][1][2])
            frame = SurroundingRectangle(last, color=GREEN_C if same else ORANGE_C, buff=0.12, stroke_width=6)
            verdict = Text("identical: only \"good\" counts" if same else "different: the middle word got through",
                           font_size=30, color=GREEN_C if same else ORANGE_C).to_edge(DOWN, buff=0.25)
            self.play(Create(frame), FadeIn(verdict), run_time=0.9)
            self.wait(2.0)
            self.snap()
            if mode == "on":
                self.play(FadeOut(VGroup(head, arrows, boxes, frame, verdict)), run_time=0.7)
        self.wait(1.0)


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim_memory"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "memory_test", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = MemoryTest()
        scene.render()
    mp4 = next(media.rglob("memory_test.mp4"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "memory_test.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "memory_test_frames.png")
    shutil.rmtree(media)
