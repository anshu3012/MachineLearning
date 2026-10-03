"""A decision tree cuts the plane step by step with lines parallel to the axes (iris petals, depth 3).
Run: python splitting.py  -> splitting.mp4, splitting.gif, splitting_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
COLS = ["#4C78A8", "#F58518", "#54A24B"]            # setosa, versicolor, virginica
NAMES = ["setosa", "versicolor", "virginica"]
FEAT = ["petal length", "petal width"]
Text.set_default(color=BLACK, font="Latin Modern Roman")

iris = load_iris()
X, y = iris.data[:, 2:], iris.target
tree = DecisionTreeClassifier(max_depth=3, random_state=2).fit(X, y).tree_
BOX = (0.5, 7.5, 0.0, 2.7)                          # x0, x1, y0, y1 of the plotting area


def splits():
    """Internal nodes in breadth-first order, each with the rectangle it cuts."""
    out, queue = [], [(0, BOX)]
    while queue:
        node, (x0, x1, y0, y1) = queue.pop(0)
        if tree.children_left[node] == -1:
            continue
        f, t = tree.feature[node], tree.threshold[node]
        left = (x0, t, y0, y1) if f == 0 else (x0, x1, y0, t)
        right = (t, x1, y0, y1) if f == 0 else (x0, x1, t, y1)
        out.append((node, f, t, (x0, x1, y0, y1), tree.children_left[node], left, tree.children_right[node], right))
        queue += [(tree.children_left[node], left), (tree.children_right[node], right)]
    return out


class Splitting(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def rect(self, box, node):
        x0, x1, y0, y1 = box
        cls = int(np.argmax(tree.value[node][0]))
        r = Polygon(*[self.ax.c2p(a, b) for a, b in [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]],
                    stroke_width=0, fill_color=COLS[cls], fill_opacity=0.18)
        return r

    def caption(self, *lines):
        return VGroup(*[Text(t, font_size=28) for t in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.16) \
            .move_to(ORIGIN, aligned_edge=UL).shift(RIGHT * 1.6 + UP * 2.6)

    def construct(self):
        self.snaps = []
        self.ax = Axes(x_range=[BOX[0], BOX[1], 1], y_range=[BOX[2], BOX[3], 0.5], x_length=6.6, y_length=5.6, tips=False,
                       axis_config=dict(color=GREY_D, include_numbers=True, font_size=30,
                                        decimal_number_config=dict(num_decimal_places=1, color=BLACK))
                       ).to_edge(LEFT, buff=0.7).shift(UP * 0.2)
        labels = VGroup(Text(FEAT[0], font_size=24).next_to(self.ax.x_axis, DOWN, buff=0.45),
                        Text(FEAT[1], font_size=24).rotate(PI / 2).next_to(self.ax.y_axis, LEFT, buff=0.45))
        dots = VGroup(*[Dot(self.ax.c2p(*p), radius=0.06, color=COLS[c], fill_opacity=0.85) for p, c in zip(X, y)])
        legend = VGroup(*[VGroup(Dot(color=COLS[i], radius=0.09), Text(NAMES[i], font_size=24)).arrange(RIGHT, buff=0.15)
                          for i in range(3)]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        legend.move_to(ORIGIN, aligned_edge=DL).shift(RIGHT * 1.6 + DOWN * 3.2)
        self.add(self.ax, labels, dots, legend)
        cap = self.caption("Start: one region,", "all 150 flowers")
        self.add(cap)
        self.wait(0.6)
        self.snap()
        regions = {}
        for i, (node, f, t, box, nl, lbox, nr, rbox) in enumerate(splits(), start=1):
            x0, x1, y0, y1 = box
            a, b = ((t, y0), (t, y1)) if f == 0 else ((x0, t), (x1, t))
            line = Line(self.ax.c2p(*a), self.ax.c2p(*b), color=BLACK, stroke_width=5)
            new_cap = self.caption(f"Split {i}: {FEAT[f]} ≤ {t:.2f}",
                                   "a line parallel to the " + ("y axis" if f == 0 else "x axis"),
                                   "inside the region it splits")
            old = regions.pop(node, None)
            fades = [FadeOut(old)] if old is not None else []
            self.play(Create(line), Transform(cap, new_cap), *fades, run_time=1.2)
            regions[nl], regions[nr] = self.rect(lbox, nl), self.rect(rbox, nr)
            self.play(FadeIn(regions[nl]), FadeIn(regions[nr]), run_time=0.6)
            self.bring_to_front(dots)
            self.wait(0.6)
            if i in (1, 2):
                self.snap()
        self.play(Transform(cap, self.caption("Done: 5 boxes, each", "coloured by its majority class")))
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
                     "output_file": "splitting", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = Splitting()
        scene.render()
    mp4 = HERE / "splitting.mp4"
    shutil.copy(next(media.rglob("splitting.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "splitting.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "splitting_frames.png")
    shutil.rmtree(media)
