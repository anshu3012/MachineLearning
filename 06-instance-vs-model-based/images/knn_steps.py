"""Instance-based learning step by step (KNN, k = 3): store, measure distances, pick the nearest, vote.
Run: python knn_steps.py  -> knn_steps.mp4, knn_steps.gif, knn_steps_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
from sklearn.preprocessing import StandardScaler

from placement_data import placement_data

HERE = Path(__file__).parent
BLUE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
QUERY = np.array([94.5, 8.3])


class KnnSteps(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        X, y = placement_data()
        scaler = StandardScaler().fit(X)
        dist = np.linalg.norm(scaler.transform(X) - scaler.transform([QUERY]), axis=1)
        nearest = np.argsort(dist)[:3]

        axes = Axes(x_range=[75, 136, 10], y_range=[5, 10, 1], x_length=7.6, y_length=5.4, tips=False,
                    axis_config={"color": GREY_C, "include_numbers": True, "font_size": 22,
                                 "decimal_number_config": {"color": BLACK, "num_decimal_places": 0}}).shift(LEFT * 2.4)
        labels = VGroup(Text("IQ", font_size=24).next_to(axes.x_axis, DOWN, buff=0.45),
                        Text("CGPA", font_size=24).next_to(axes.y_axis, UP, buff=0.15))
        dots = VGroup(*[Dot(axes.c2p(*p), radius=0.07, color=GREEN_C if c else RED_C) for p, c in zip(X, y)])
        side = VGroup(Text("Training: just store the data", font_size=26, weight=BOLD),
                      VGroup(Dot(color=GREEN_C), Text("placed", font_size=22)).arrange(RIGHT),
                      VGroup(Dot(color=RED_C), Text("not placed", font_size=22)).arrange(RIGHT)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(UP * 1.8)
        self.play(Create(axes), FadeIn(labels), FadeIn(dots, lag_ratio=0.02), FadeIn(side), run_time=2)
        self.wait(0.4)
        self.snap()

        # A new student arrives: measure the distance to every stored point
        q = axes.c2p(*QUERY)
        star = Star(n=5, outer_radius=0.2, color=BLUE_C, fill_opacity=1, stroke_color=BLACK, stroke_width=1).move_to(q)
        step2 = Text("New student: measure distance\nto every stored student", font_size=24, weight=BOLD,
                     line_spacing=0.8).next_to(side, DOWN, buff=0.6, aligned_edge=LEFT)
        lines = VGroup(*[Line(q, d.get_center(), stroke_width=1, color=GREY_C, stroke_opacity=0.5) for d in dots])
        self.play(FadeIn(star, scale=2), FadeIn(step2))
        self.play(Create(lines, lag_ratio=0.01), run_time=1.5)
        self.wait(0.3)
        self.snap()

        # Keep only the 3 nearest
        step3 = Text("Keep the 3 nearest", font_size=24, weight=BOLD).next_to(step2, DOWN, buff=0.4, aligned_edge=LEFT)
        rings = VGroup(*[Circle(0.17, color=BLUE_C, stroke_width=4).move_to(dots[i]) for i in nearest])
        near_lines = VGroup(*[Line(q, dots[i].get_center(), stroke_width=4, color=BLUE_C) for i in nearest])
        self.play(FadeOut(lines), FadeIn(step3))
        self.play(Create(near_lines), Create(rings))
        self.wait(0.3)
        self.snap()

        # Vote
        n_placed = int(y[nearest].sum())
        verdict = "Placed" if n_placed >= 2 else "Not placed"
        vote = Text(f"Vote: {n_placed} placed, {3 - n_placed} not placed", font_size=24).next_to(
            step3, DOWN, buff=0.4, aligned_edge=LEFT)
        result = Text(f"Prediction: {verdict}", font_size=30, weight=BOLD,
                      color=GREEN_C if n_placed >= 2 else RED_C).next_to(vote, DOWN, buff=0.35, aligned_edge=LEFT)
        self.play(FadeIn(vote))
        self.play(FadeIn(result, scale=1.2), star.animate.set_color(GREEN_C if n_placed >= 2 else RED_C))
        self.wait(1.5)
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
                     "output_file": "knn_steps", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = KnnSteps()
        scene.render()
    mp4 = HERE / "knn_steps.mp4"
    shutil.copy(next(media.rglob("knn_steps.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "knn_steps.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "knn_steps_frames.png")
    shutil.rmtree(media)
