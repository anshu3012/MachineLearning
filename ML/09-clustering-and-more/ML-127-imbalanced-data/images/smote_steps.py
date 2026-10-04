"""SMOTE step by step on 10 minority points: find each point's 5 nearest minority neighbours, pick a random point,
pick one of its neighbours, place a new point at a random fraction of the way between them, repeat.
Run: python smote_steps.py  -> smote_steps.mp4, smote_steps.gif, smote_steps_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image, ImageOps

HERE = Path(__file__).parent
BLUE_C, RED_C, ORANGE_C, GREY_C = "#4C78A8", "#E45756", "#F58518", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")

MINO = np.array([[1.0, 1.2], [1.6, 0.8], [2.1, 1.5], [1.3, 2.0], [2.6, 0.9], [0.7, 0.6], [2.0, 2.4],
                 [3.0, 1.7], [1.5, 1.4], [2.5, 2.0]])
MAJO = np.random.default_rng(3).uniform([0.2, 2.7], [4.2, 3.9], size=(14, 2))
MAJO = np.vstack([MAJO, np.random.default_rng(4).uniform([3.4, 0.2], [4.3, 2.6], size=(8, 2))])
K = 5
NBRS = np.argsort(((MINO[:, None] - MINO) ** 2).sum(2), axis=1)[:, 1:K + 1]     # 5 nearest minority neighbours
rng = np.random.default_rng(7)
PICKS = [(i, NBRS[i, rng.integers(K)], round(float(rng.uniform(0.15, 0.85)), 2))
         for i in rng.integers(len(MINO), size=7)]


class Smote(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, title, sub):
        return VGroup(Text(title, font_size=26, weight=BOLD), Text(sub, font_size=20, color=GREY_C)
                      ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).to_corner(UR, buff=0.4).shift(DOWN * 0.7)

    def construct(self):
        self.snaps = []
        ax = Axes(x_range=[0, 4.5, 1], y_range=[0, 4.2, 1], x_length=6.2, y_length=5.8, tips=False,
                  axis_config={"color": GREY_C, "include_ticks": False}).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        p = lambda xy: ax.c2p(*xy)
        heading = Text("SMOTE, k = 5", font_size=34, weight=BOLD).to_corner(UR, buff=0.4)
        majo = VGroup(*[Dot(p(q), radius=0.07, color=BLUE_C, fill_opacity=0.5) for q in MAJO])
        mino = VGroup(*[Dot(p(q), radius=0.1, color=RED_C, stroke_color=BLACK, stroke_width=1.5) for q in MINO])
        cap = self.caption("Imbalanced data", "22 majority points (blue), 10 minority (red)")
        self.play(Create(ax), FadeIn(majo, mino, heading, cap))
        self.wait(0.6)
        self.play(majo.animate.set_opacity(0.12), Transform(cap, self.caption(
            "1. Look at the minority class only", "SMOTE works on the red points")))
        self.wait(0.4)

        for step, (i, j, lam) in enumerate(PICKS):
            fast = step > 0
            ring = Circle(radius=0.2, color=BLACK, stroke_width=4).move_to(p(MINO[i]))
            if not fast:
                self.play(Create(ring), Transform(cap, self.caption("2. Pick a minority point at random",
                                                                     "its 5 nearest minority neighbours")))
                lines = VGroup(*[DashedLine(p(MINO[i]), p(MINO[n]), color=GREY_C, stroke_width=3) for n in NBRS[i]])
                self.play(Create(lines))
                self.wait(0.4)
                self.snap()
                chosen = Line(p(MINO[i]), p(MINO[j]), color=ORANGE_C, stroke_width=6)
                self.play(FadeOut(lines), Create(chosen), Transform(cap, self.caption(
                    "3. Pick one of the 5 neighbours at random", "the orange segment")))
                self.wait(0.4)
                self.snap()
                new = MINO[i] + lam * (MINO[j] - MINO[i])
                dot = Dot(p(MINO[i]), radius=0.1, color=ORANGE_C)
                self.add(dot)
                self.play(dot.animate.move_to(p(new)), Transform(cap, self.caption(
                    f"4. New point = x + {lam} * (neighbour - x)", "random factor between 0 and 1")), run_time=1.4)
                self.wait(0.6)
                self.snap()
                self.play(FadeOut(ring, chosen))
            else:
                chosen = Line(p(MINO[i]), p(MINO[j]), color=ORANGE_C, stroke_width=6)
                new = MINO[i] + lam * (MINO[j] - MINO[i])
                dot = Dot(p(MINO[i]), radius=0.1, color=ORANGE_C)
                self.play(Create(ring), Create(chosen), run_time=0.4)
                self.add(dot)
                self.play(dot.animate.move_to(p(new)), run_time=0.5)
                self.play(FadeOut(ring, chosen), run_time=0.3)
                if step == 1:
                    self.play(Transform(cap, self.caption("5. Repeat", "until both classes have the same size")))
        self.play(majo.animate.set_opacity(0.5))
        self.wait(1.2)
        self.snap()


def key_frames_grid(frames, out, gap=16, pad=20):
    boxes = [ImageOps.invert(f.convert("RGB")).getbbox() for f in frames[:4]]
    l, t = min(b[0] for b in boxes) - pad, min(b[1] for b in boxes) - pad
    r, b_ = max(b[2] for b in boxes) + pad, max(b[3] for b in boxes) + pad
    frames = [f.crop((max(l, 0), max(t, 0), r, b_)) for f in frames]
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "smote_steps", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = Smote()
        scene.render()
    mp4 = HERE / "smote_steps.mp4"
    shutil.copy(next(media.rglob("smote_steps.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "smote_steps.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "smote_steps_frames.png")
    shutil.rmtree(media)
