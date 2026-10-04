"""DBSCAN step by step on 14 points (eps = 1, min_samples = 4): label the points, grow a cluster from each
unclustered core point through density-connected core points, attach border points, leave noise alone.
Run: python dbscan_steps.py  -> dbscan_steps.mp4, dbscan_steps.gif, dbscan_steps_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image, ImageOps
from sklearn.cluster import DBSCAN
from sklearn.metrics import pairwise_distances

from toy_points import EPS, MIN_SAMPLES, X

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREY_C, DARK = "#4C78A8", "#F58518", "#6B6B6B", "#333333"
COLOURS = [BLUE_C, ORANGE_C]
Text.set_default(color=BLACK, font="Latin Modern Roman")

db = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES).fit(X)
CORE = np.zeros(len(X), bool); CORE[db.core_sample_indices_] = True
D = pairwise_distances(X)


class DBSCANSteps(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, title, sub):
        return VGroup(Text(title, font_size=28, weight=BOLD), Text(sub, font_size=21, color=GREY_C)
                      ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)

    def construct(self):
        self.snaps = []
        heading = Text(f"DBSCAN, eps = {EPS:g}, MinPts = {MIN_SAMPLES}", font_size=32,
                       weight=BOLD).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[-0.2, 7.2, 1], y_range=[0.3, 4.1, 1], x_length=10.4, y_length=5.3, tips=False,
                  axis_config={"stroke_opacity": 0}).shift(UP * 0.3)
        pos = [ax.c2p(*p) for p in X]
        dots = [Dot(p, radius=0.11, color=GREY_C) for p in pos]
        cap = self.caption("Step 0: choose eps and MinPts", "here eps = 1 and MinPts = 4")
        self.play(FadeIn(heading), *[FadeIn(d) for d in dots], FadeIn(cap))
        self.wait(0.6)

        # Step 1: label every point
        unit = ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]
        ring = Circle(radius=EPS * unit, color=BLUE_C, stroke_width=3).move_to(pos[2])
        self.play(Create(ring), Transform(cap, self.caption("Step 1: label every point",
                                                            "count the points within eps of each point")))
        anims, marks = [], VGroup()
        for i, d in enumerate(dots):
            if CORE[i]:
                anims.append(d.animate.set_color(DARK).scale(1.15))
            elif db.labels_[i] == -1:
                cross = Cross(scale_factor=0.13, stroke_color=GREY_C, stroke_width=6).move_to(pos[i])
                marks.add(cross)
                anims.append(FadeOut(d))
            else:
                anims.append(d.animate.set_fill(WHITE, opacity=1).set_stroke(DARK, width=4))
        legend = VGroup(
            VGroup(Dot(color=DARK, radius=0.11), Text("core", font_size=22)).arrange(RIGHT, buff=0.15),
            VGroup(Dot(radius=0.11, fill_color=WHITE, fill_opacity=1, stroke_color=DARK, stroke_width=4),
                   Text("border", font_size=22)).arrange(RIGHT, buff=0.15),
            VGroup(Cross(scale_factor=0.13, stroke_color=GREY_C, stroke_width=6), Text("noise", font_size=22)
                   ).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.4
                                                                                                    ).shift(DOWN * 0.6)
        self.play(*anims, FadeIn(marks), FadeIn(legend), FadeOut(ring), Transform(cap, self.caption(
            "Step 1: core, border or noise", "core: at least 4 points within eps (itself included)")))
        self.wait(0.8)
        self.snap()

        # Step 2: grow a cluster from each unclustered core point
        label = -np.ones(len(X), int)
        for c in range(2):
            seed = next(i for i in range(len(X)) if CORE[i] and label[i] == -1)
            label[seed] = c
            frontier, edges = [seed], VGroup()
            while frontier:
                i = frontier.pop()
                for j in np.where((D[i] <= EPS) & CORE & (label == -1))[0]:
                    label[j] = c
                    frontier.append(j)
                    edges.add(Line(pos[i], pos[j], color=COLOURS[c], stroke_width=5))
            members = [dots[i] for i in range(len(X)) if CORE[i] and label[i] == c]
            self.play(Create(edges), *[m.animate.set_color(COLOURS[c]) for m in members],
                      Transform(cap, self.caption(f"Step 2: cluster {c + 1} grows from a core point",
                                                  "add every core point linked by steps of at most eps")),
                      run_time=1.6)
            self.wait(0.7)
            if c == 1:
                self.snap()

        # Step 3: border points join the cluster of their nearest core point
        anims, links = [], VGroup()
        for i in range(len(X)):
            if not CORE[i] and db.labels_[i] != -1:
                cores = np.where(CORE)[0]
                j = cores[np.argmin(D[i, cores])]
                links.add(DashedLine(pos[i], pos[j], color=COLOURS[label[j]], stroke_width=4))
                anims.append(dots[i].animate.set_stroke(COLOURS[label[j]], width=5))
        self.play(Create(links), *anims, Transform(cap, self.caption(
            "Step 3: each border point joins its nearest core point's cluster", "dashed: border to nearest core")))
        self.wait(0.8)
        self.snap()

        # Step 4: noise stays out
        self.play(Indicate(marks, color=BLACK, scale_factor=1.6), Transform(cap, self.caption(
            "Step 4: noise points stay unclustered", "result: 2 clusters and 2 noise points (label -1)")))
        self.wait(1.5)
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
                     "output_file": "dbscan_steps", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = DBSCANSteps()
        scene.render()
    mp4 = HERE / "dbscan_steps.mp4"
    shutil.copy(next(media.rglob("dbscan_steps.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "dbscan_steps.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "dbscan_steps_frames.png")
    shutil.rmtree(media)
