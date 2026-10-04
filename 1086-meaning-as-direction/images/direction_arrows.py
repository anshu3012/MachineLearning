"""king - man + woman drawn on real GloVe vectors (100-d), in the plane through man, woman and king.
The plane holds man, woman, king and king - man + woman exactly; queen is projected onto it (the Notebook gives
how far off the plane it sits). Numbers: data/analogy_plane.csv and data/analogies.csv (from the Notebook).
Idea credited to Sanderson (3Blue1Brown), Ch 5; our own data and code.
Run: python direction_arrows.py -> direction_arrows.gif, direction_arrows_frames.png (Manim CE)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
P = pd.read_csv(HERE.parent / "data" / "analogy_plane.csv").set_index("word")
A = pd.read_csv(HERE.parent / "data" / "analogies.csv")
K = A[(A.model == "GloVe") & (A.target == "queen")].iloc[0]
SCALE, SHIFT = 0.82, np.array([-4.9, -3.3, 0])


def pt(word):
    return np.array([P.loc[word, "x"], P.loc[word, "y"], 0]) * SCALE + SHIFT


class Directions(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def dot(self, word, color, label, direction):
        d = Dot(pt(word), radius=0.11, color=color)
        t = Text(label, font_size=30, color=color).next_to(d, direction, buff=0.15)
        return VGroup(d, t)

    def construct(self):
        self.snaps = []
        title = Text("Directions carry meaning", font_size=38, weight=BOLD).to_edge(UP, buff=0.25)
        sub = Text("real GloVe vectors, 100 numbers per word, seen in one flat slice", font_size=24,
                   color=GREY_C).next_to(title, DOWN, buff=0.12)
        self.add(title, sub)
        man, woman = self.dot("man", GREY_C, "man", DOWN), self.dot("woman", GREY_C, "woman", DOWN)
        self.play(FadeIn(man), FadeIn(woman), run_time=0.8)
        g = Arrow(pt("man"), pt("woman"), buff=0.12, color=ORANGE_C, stroke_width=7, max_tip_length_to_length_ratio=0.12)
        gl = Text("woman − man", font_size=28, color=ORANGE_C).next_to(g, UP, buff=0.12)
        self.play(GrowArrow(g), FadeIn(gl), run_time=1.2)
        note = Text("one direction:\n\"more female\"", font_size=26, color=ORANGE_C, line_spacing=0.8).move_to([4.3, -2.2, 0])
        self.play(FadeIn(note))
        self.wait(1.0)
        self.snap()

        king = self.dot("king", BLUE_C, "king", LEFT)
        self.play(FadeIn(king), FadeOut(note))
        g2 = g.copy()
        self.play(g2.animate.shift(pt("king") - pt("man")), run_time=1.8)
        tgt = Star(n=5, outer_radius=0.2, color=RED_C, fill_opacity=1).move_to(pt("king − man + woman"))
        tl = Text("king − man + woman", font_size=28, color=RED_C).next_to(tgt, RIGHT, buff=0.15)
        self.play(FadeIn(tgt, scale=1.5), FadeIn(tl))
        step = Text("add the same arrow\nto king", font_size=26, color=ORANGE_C, line_spacing=0.8).move_to([4.6, -0.6, 0])
        self.play(FadeIn(step))
        self.wait(1.2)
        self.snap()

        queen = self.dot("queen", PURPLE_C, "queen", DOWN)
        line = DashedLine(pt("king − man + woman"), pt("queen"), color=PURPLE_C, stroke_width=4)
        self.play(FadeOut(step), FadeIn(queen), Create(line), run_time=1.2)
        off = Text(f"queen is really {P.loc['queen', 'off_plane']:.1f} units\noff this slice", font_size=24,
                   color=PURPLE_C, line_spacing=0.8).next_to(queen, DOWN, buff=0.15).shift(0.2 * RIGHT)
        self.play(FadeIn(off))
        self.wait(0.8)
        board = VGroup(
            Text("closest words in all 100 dimensions", font_size=24, weight=BOLD),
            Text(f"1. {K.top_all}   cosine {K.cos_top_all:.3f}", font_size=26, color=BLUE_C),
            Text(f"2. {K.second_all}   cosine {K.cos_target:.3f}", font_size=26, color=PURPLE_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.1, 0.0, 0])
        self.play(FadeIn(board, shift=0.2 * LEFT), run_time=1.0)
        self.wait(1.6)
        self.snap()

        verdict = VGroup(
            Text("drop king, man, woman", font_size=26),
            Text("from the candidates:", font_size=26),
            Text("queen comes first", font_size=28, color=PURPLE_C, weight=BOLD),
            Text("a near miss, not a hit", font_size=24, color=GREY_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(board, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(FadeIn(verdict), run_time=1.0)
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
                     "output_file": "direction_arrows", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = Directions()
        scene.render()
    mp4 = next(media.rglob("direction_arrows.mp4"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "direction_arrows.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "direction_arrows_frames.png")
    shutil.rmtree(media)
