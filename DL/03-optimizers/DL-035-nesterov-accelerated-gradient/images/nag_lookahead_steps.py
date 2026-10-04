"""Momentum (top) and NAG (bottom) step by step on the valley L = (w1^2 + 100 w2^2)/2 from (-10, 0.4), eta = 0.01,
beta = 0.9 (the run of Figure 1). Orange: the momentum jump beta*v; blue: minus eta times the gradient; the purple
dot marks where the gradient is measured. Momentum measures it at the current point, NAG at the look-ahead point.
Run: python nag_lookahead_steps.py -> nag_lookahead_steps.gif, nag_lookahead_steps_frames.png (Manim; render on topgro)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
K, START, ETA, BETA = 100, np.array([-10.0, 0.4]), 0.01, 0.9
SX, SY, X0 = 1.05, 1.9, -6.2
CY = {False: 1.25, True: -2.2}                       # screen y of w2 = 0: momentum panel, NAG panel
grad = lambda w: np.array([w[0], K * w[1]])
loss = lambda w: 0.5 * (w[0] ** 2 + K * w[1] ** 2)


def run(nag, steps=80):
    """Points w_t, jumps beta*v_{t-1}, gradient points and gradient steps, so w_{t+1} = w_t - jump - gstep."""
    w, v, W, jump, at, gstep = START.copy(), np.zeros(2), [START.copy()], [], [], []
    for _ in range(steps):
        p = w - BETA * v if nag else w.copy()       # NAG: measure the slope after the jump
        jump.append(BETA * v)
        at.append(p)
        gstep.append(ETA * grad(p))
        v = BETA * v + ETA * grad(p)
        w = w - v
        W.append(w.copy())
    return np.array(W), np.array(jump), np.array(at), np.array(gstep)


RUNS = {nag: run(nag) for nag in (False, True)}
DONE = {nag: int(np.argmax([loss(p) < 0.01 for p in R[0]])) for nag, R in RUNS.items()}
assert DONE == {False: 59, True: 25}                # as in Figure 1
for W, J, A, G in RUNS.values():
    assert np.allclose(W[1:], W[:-1] - J - G)


def pt(w, nag):
    return np.array([X0 + SX * (w[0] + 10.5), CY[nag] + SY * w[1], 0])


def arrow(a, b, nag, colour, width=7):
    return Arrow(pt(a, nag), pt(b, nag), buff=0, color=colour, stroke_width=width,
                 max_tip_length_to_length_ratio=0.25, max_stroke_width_to_length_ratio=12)


class NagLookahead(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        title = Text("where is the slope measured?", font_size=34).to_edge(UP, buff=0.2)
        key = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.6, color=ORANGE_C, stroke_width=8),
                            Text("momentum jump β·v", font_size=24, color=ORANGE_C)).arrange(RIGHT, buff=0.15),
                     VGroup(Line(ORIGIN, RIGHT * 0.6, color=BLUE_C, stroke_width=8),
                            Text("− η × gradient", font_size=24, color=BLUE_C)).arrange(RIGHT, buff=0.15),
                     VGroup(Dot(radius=0.12, color=PURPLE_C),
                            Text("gradient measured here", font_size=24, color=PURPLE_C)).arrange(RIGHT, buff=0.15))
        key.arrange(RIGHT, buff=0.6).next_to(title, DOWN, buff=0.15)
        self.add(title, key)
        dots, trails, counters = {}, {}, {}
        for nag in (False, True):
            centre = pt([0, 0], nag)
            self.add(*[Ellipse(width=2 * SX * np.sqrt(2 * c), height=2 * SY * np.sqrt(2 * c) / 10, color=GREY_C,
                               stroke_width=1.5, stroke_opacity=0.5).move_to(centre) for c in (0.5, 3, 10, 22)])
            self.add(Star(5, outer_radius=0.17, color=RED_C, fill_opacity=1).move_to(centre))
            name = "NAG: slope at the look-ahead point" if nag else "momentum: slope at the current point"
            self.add(Text(name, font_size=28, color=PURPLE_C if nag else ORANGE_C)
                     .move_to([X0 + 0.1, CY[nag] + 1.25, 0], aligned_edge=LEFT))
            dots[nag] = Dot(pt(START, nag), radius=0.08, color=BLACK)
            trails[nag] = VGroup()
            self.add(dots[nag], trails[nag])
        line = DashedLine([-7, -0.45, 0], [7, -0.45, 0], color=GREY_C, stroke_width=2)
        self.add(line)
        counter = Text("step 1", font_size=28).to_corner(DR, buff=0.25)
        self.add(counter)
        self.wait(0.4)
        for t in range(DONE[False]):
            slow = t < 4
            shown = []
            self.remove(counter)
            counter = Text(f"step {t + 1}", font_size=28).to_corner(DR, buff=0.25)
            self.add(counter)
            stage = {1: [], 2: [], 3: []}
            for nag in (False, True):
                W, J, A, G = RUNS[nag]
                if t >= DONE[nag]:
                    continue
                a, b = W[t], W[t + 1]
                if np.linalg.norm(J[t]) > 1e-9:
                    stage[1].append(arrow(a, a - J[t], nag, ORANGE_C))
                stage[2].append(Dot(pt(A[t], nag), radius=0.12, color=PURPLE_C))
                stage[3].append(arrow(a - J[t], b, nag, BLUE_C))
            notes = []
            if t == 1:
                notes = [Text(s, font_size=26, color=GREY_C).move_to([-3.4, CY[nag] - 0.75, 0], aligned_edge=LEFT)
                         for nag, s in ((False, "no slope across here: the jump swings it past"),
                                        (True, "slope after the jump points back: the swing cancels"))]
            if slow:
                for k in (1, 2, 3):
                    if stage[k]:
                        self.play(*[GrowArrow(m) if isinstance(m, Arrow) else FadeIn(m, scale=1.6)
                                    for m in stage[k]], run_time=0.6)
                if notes:
                    self.play(*[FadeIn(n) for n in notes], run_time=0.5)
                    self.wait(1.5)
                self.wait(0.8)
            else:
                self.add(*stage[1], *stage[2], *stage[3])
                self.wait(0.3 if t < 15 else 0.12)
            if t in (1, 9):
                self.snap()
            self.remove(*stage[1], *stage[2], *stage[3], *notes)
            for nag in (False, True):
                W = RUNS[nag][0]
                if t < DONE[nag]:
                    trails[nag].add(Line(pt(W[t], nag), pt(W[t + 1], nag), color=PURPLE_C if nag else ORANGE_C,
                                         stroke_width=3, stroke_opacity=0.7))
                    dots[nag].move_to(pt(W[t + 1], nag))
                if t + 1 == DONE[nag]:
                    self.add(Text(f"loss < 0.01 after {DONE[nag]} steps", font_size=26, color=GREEN_C)
                             .move_to([X0 + 0.1, CY[nag] - 1.05, 0], aligned_edge=LEFT))
            if t + 1 == DONE[True]:
                self.wait(1.0)
                self.snap()
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
                     "output_file": "nag_lookahead_steps", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = NagLookahead()
        scene.render()
    mp4 = next(media.rglob("nag_lookahead_steps.mp4"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "nag_lookahead_steps.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "nag_lookahead_steps_frames.png")
    shutil.rmtree(media)
