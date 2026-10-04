"""Sequential against parallel. Top: an LSTM reads a 6-word sentence one word per step, each step waiting for the one
before. Bottom: self-attention computes all 6 positions in one step, every word looking at every word. Then the
measured times of one training step at 256 words grow as bars (data/timing.csv, Notebook).
Run: python race.py -> race.mp4, race.gif, race_frames.png (Manim)"""
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
T = pd.read_csv(HERE.parent / "data" / "timing.csv").set_index("length")
WORDS = "the transformer reads all words together".split()
X0, DX = -4.4, 1.75


def cell(x, y, col):
    return RoundedRectangle(corner_radius=0.1, width=1.2, height=0.6, color=col, fill_color=col, fill_opacity=0.1,
                            stroke_width=3).move_to([x, y, 0])


class Race(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        title = Text("Sequential against parallel", font_size=32).to_edge(UP, buff=0.25)
        self.play(FadeIn(title), run_time=0.5)
        yl, ya = 1.5, -1.9
        lab_l = Text("LSTM", font_size=28, color=BLUE_C).move_to([X0 - 0.6, yl + 0.75, 0], aligned_edge=LEFT)
        lab_a = Text("self-attention", font_size=28, color=ORANGE_C).move_to([X0 - 0.6, ya + 1.25, 0], aligned_edge=LEFT)
        lstm = VGroup(*[cell(X0 + DX * k, yl, BLUE_C) for k in range(6)])
        att = VGroup(*[cell(X0 + DX * k, ya, ORANGE_C) for k in range(6)])
        wl = VGroup(*[Text(w, font_size=20).next_to(c, DOWN, buff=0.12) for w, c in zip(WORDS, lstm)])
        wa = VGroup(*[Text(w, font_size=20).next_to(c, DOWN, buff=0.12) for w, c in zip(WORDS, att)])
        arrows = VGroup(*[Arrow(lstm[k].get_right(), lstm[k + 1].get_left(), buff=0.02, color=BLUE_C, stroke_width=3)
                          for k in range(5)])
        self.play(FadeIn(lab_l), FadeIn(lab_a), FadeIn(lstm), FadeIn(att), FadeIn(wl), FadeIn(wa), FadeIn(arrows))
        clock_l = Text("steps: 0", font_size=24, color=BLUE_C).move_to([5.9, yl + 0.8, 0])
        clock_a = Text("steps: 0", font_size=24, color=ORANGE_C).move_to([5.9, ya + 1.25, 0])
        self.play(FadeIn(clock_l), FadeIn(clock_a), run_time=0.4)
        links = VGroup(*[ArcBetweenPoints(att[i].get_top(), att[j].get_top(), angle=-PI / 4, color=ORANGE_C,
                                          stroke_width=1.5) for i in range(6) for j in range(6) if i < j])
        for k in range(6):
            anims = [lstm[k].animate.set_fill(BLUE_C, opacity=0.8),
                     Transform(clock_l, Text(f"steps: {k + 1}", font_size=24, color=BLUE_C).move_to(clock_l))]
            if k == 0:
                anims += [att.animate.set_fill(ORANGE_C, opacity=0.8), Create(links),
                          Transform(clock_a, Text("steps: 1 (done)", font_size=24, color=ORANGE_C).move_to(clock_a))]
            self.play(*anims, run_time=0.7)
            if k == 0:
                self.snap()
        done = Text("each LSTM step waits for the one before", font_size=22, color=BLUE_C).next_to(wl, DOWN, buff=0.2)
        self.play(FadeIn(done))
        self.wait(0.8)
        self.snap()
        # measured times
        self.play(*[FadeOut(m) for m in self.mobjects if m is not title], run_time=0.6)
        n = 256
        sub = Text(f"measured: one training step on a GPU, {n} words, batch of 16", font_size=24).move_to([0, 2.4, 0])
        self.play(FadeIn(sub))
        scale = 1.25                                         # units per millisecond
        rows = []
        for k, (name, col) in enumerate((("LSTM", BLUE_C), ("self-attention", ORANGE_C))):
            y = 1.0 - 1.4 * k
            lab = Text(name, font_size=26, color=col).move_to([-4.4, y, 0], aligned_edge=RIGHT)
            ms = T.loc[n, name]
            bar = Rectangle(width=scale * ms, height=0.6, stroke_width=0, fill_color=col, fill_opacity=0.85)
            bar.move_to([-4.1, y, 0], aligned_edge=LEFT)
            val = Text(f"{ms:.2f} ms", font_size=24).next_to(bar, RIGHT, buff=0.15)
            rows.append((lab, bar, val))
        self.play(*[FadeIn(r[0]) for r in rows], run_time=0.4)
        self.play(*[GrowFromEdge(r[1], LEFT) for r in rows], run_time=2.0, rate_func=linear)
        self.play(*[FadeIn(r[2]) for r in rows], run_time=0.4)
        ratio = Text(f"the LSTM is {T.loc[n, 'LSTM / attention']:.1f} times slower here", font_size=26).move_to([0, -2.4, 0])
        self.play(FadeIn(ratio))
        self.wait(1.0)
        self.snap()
        foot = Text("at 1,024 words the n × n comparisons catch up: 34.5 against 16.6 ms", font_size=22,
                    color=GREY_C).move_to([0, -3.2, 0])
        self.play(FadeIn(foot))
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
                     "output_file": "race", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = Race()
        scene.render()
    mp4 = HERE / "race.mp4"
    shutil.copy(next(media.rglob("race.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "race.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "race_frames.png")
    shutil.rmtree(media)
