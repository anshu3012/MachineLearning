"""Lasso vs Ridge as geometry, on two diabetes features (bmi and bp, training split of the Lasso Note,
each scaled to standard deviation 1). The loss is a bowl whose level curves are ellipses around the
least-squares point. With the same budget t = 15, the Lasso region |b1| + |b2| <= t is a diamond and the
Ridge region b1^2 + b2^2 <= t^2 a circle. Growing the ellipse until it first touches each region gives the
constrained answer: a corner of the diamond (bp coefficient exactly 0) versus a point off the axes on the circle.
Picture after ESL Figure 3.11 and StatQuest "Ridge vs Lasso Regression, Visualized"; our own data and code.
Run: python constraint_touch.py  -> constraint_touch.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MathTex.set_default(color=BLACK)
T = 15.0                                              # the same budget for both penalties
XR, YR = (-20, 60), (-20, 40)                         # coefficient window shown in each panel


def data():
    d = load_diabetes(as_frame=True)
    Xtr, _, ytr, _ = train_test_split(d.data, d.target, test_size=0.2, random_state=2)
    A = Xtr[["bmi", "bp"]]
    A = ((A - A.mean()) / A.std()).values
    yc = (ytr - ytr.mean()).values
    Q = A.T @ A / len(A)
    return Q, np.linalg.solve(Q, A.T @ yc / len(A))


Q, BETA = data()
W, V = np.linalg.eigh(Q)
TH = np.linspace(0, 2 * np.pi, 4001)
U = np.c_[np.cos(TH), np.sin(TH)]


def loss(B):
    """Extra mean squared error over least squares: (b - beta)^T Q (b - beta)."""
    R = np.atleast_2d(B) - BETA
    return np.einsum("ij,jk,ik->i", R, Q, R)


def touch(boundary):
    i = loss(boundary).argmin()
    return boundary[i], loss(boundary)[i]


DIAMOND = U / np.abs(U).sum(1, keepdims=True) * T
CIRCLE = U * T
(L_PT, L_LEVEL), (R_PT, R_LEVEL) = touch(DIAMOND), touch(CIRCLE)


def ellipse_points(level):
    return BETA + (U * np.sqrt(level / W)) @ V.T


def boxed(mob, buff=0.1):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


class Panel(VGroup):
    def __init__(self, title, region, colour, centre):
        super().__init__()
        self.ax = Axes(x_range=[*XR, 10], y_range=[*YR, 10], x_length=6.2, y_length=6.2 * 60 / 80, tips=False,
                       axis_config={"color": GREY_C, "stroke_width": 2, "include_numbers": False}).move_to(centre)
        self.region = Polygon(*[self.ax.c2p(*p) for p in region[::40]], color=colour, fill_opacity=0.3,
                              stroke_width=4)
        self.title = Text(title, font_size=34, color=colour, weight=BOLD).next_to(self.ax, UP, buff=0.15)
        self.xl = Text("bmi", font_size=26, color=GREY_C).next_to(self.ax.c2p(XR[1], 0), DOWN, buff=0.12).shift(LEFT * 0.3)
        self.yl = Text("bp", font_size=26, color=GREY_C).next_to(self.ax.c2p(0, YR[1]), RIGHT, buff=0.12).shift(DOWN * 0.2)
        self.ols = Dot(self.ax.c2p(*BETA), color=BLACK, radius=0.07)
        self.add(self.ax, self.region, self.title, self.xl, self.yl, self.ols)

    def ring(self, level, colour=ORANGE_C, width=4):
        """The loss ellipse at this level, cut to the panel window."""
        pts = ellipse_points(max(level, 1e-3))
        inside = (pts[:, 0] >= XR[0]) & (pts[:, 0] <= XR[1]) & (pts[:, 1] >= YR[0]) & (pts[:, 1] <= YR[1])
        g = VGroup()
        run = []
        for p, ok in zip(pts, inside):
            if ok:
                run.append(self.ax.c2p(*p))
            elif len(run) > 1:
                g.add(VMobject(color=colour, stroke_width=width).set_points_as_corners(run))
                run = []
            else:
                run = []
        if len(run) > 1:
            g.add(VMobject(color=colour, stroke_width=width).set_points_as_corners(run))
        return g


class ConstraintTouch(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, text, colour=BLACK):
        return boxed(Text(text, font_size=32, color=colour, weight=BOLD)).to_edge(DOWN, buff=0.25)

    def construct(self):
        self.snaps = []
        left = Panel("Lasso: diamond", DIAMOND, RED_C, [-3.45, 0.25, 0])
        right = Panel("Ridge: circle", CIRCLE, BLUE_C, [3.45, 0.25, 0])
        self.add(left, right)
        ols_tags = VGroup(*[boxed(Text("least squares", font_size=24), 0.05).next_to(p.ols, UP, buff=0.12)
                            for p in (left, right)])
        cap = boxed(VGroup(Text("Same budget:", font_size=32, weight=BOLD),
                           MathTex(r"|b_1| + |b_2| \le 15 \quad\text{vs}\quad b_1^2 + b_2^2 \le 15^2", font_size=40))
                    .arrange(RIGHT, buff=0.25)).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(ols_tags), FadeIn(cap))
        self.wait(1.2)
        self.snap()

        # Grow the loss ellipse from the least-squares point; each panel stops at its first touch.
        lev = ValueTracker(1.0)
        ring_l = always_redraw(lambda: left.ring(min(lev.get_value(), L_LEVEL)))
        ring_r = always_redraw(lambda: right.ring(min(lev.get_value(), R_LEVEL)))
        cap2 = self.caption("Loss grows in rings around the least-squares point")
        faint = VGroup(*[p.ring(f * R_LEVEL, "#F5B87A", 2) for p in (left, right) for f in (0.04, 0.15, 0.35, 0.65)])
        self.play(FadeOut(ols_tags), FadeTransform(cap, cap2), Create(faint), run_time=1.5)
        self.add(ring_l, ring_r)
        self.play(lev.animate.set_value(0.35 * R_LEVEL), run_time=2, rate_func=linear)
        self.snap()
        self.play(lev.animate.set_value(R_LEVEL), run_time=2, rate_func=linear)
        hit_r = Dot(right.ax.c2p(*R_PT), color=BLUE_C, radius=0.13)
        self.play(FadeIn(hit_r, scale=2))
        self.play(lev.animate.set_value(L_LEVEL), run_time=1.2, rate_func=linear)
        hit_l = Dot(left.ax.c2p(*L_PT), color=RED_C, radius=0.13)
        self.play(FadeIn(hit_l, scale=2))
        tag_l = boxed(MathTex(r"b_{\text{bp}} = 0", font_size=40, color=RED_C), 0.06).next_to(hit_l, DOWN + RIGHT, buff=0.1)
        tag_r = boxed(MathTex(rf"b_{{\text{{bp}}}} = {R_PT[1]:.1f}", font_size=40, color=BLUE_C), 0.06)
        tag_r.next_to(hit_r, DOWN + LEFT, buff=0.1)
        cap3 = self.caption("First touch: a corner for Lasso, off the axis for Ridge")
        self.play(FadeIn(tag_l), FadeIn(tag_r), FadeTransform(cap2, cap3))
        self.wait(2.5)
        self.snap()
        cap4 = self.caption("Corners stick out, so the rings often hit them first", RED_C)
        corners = VGroup(*[Circle(radius=0.2, color=RED_C, stroke_width=5).move_to(left.ax.c2p(*c))
                           for c in ((T, 0), (0, T), (-T, 0), (0, -T))])
        self.play(FadeTransform(cap3, cap4), Create(corners))
        self.wait(2.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    print("least squares", BETA.round(2), "lasso touch", L_PT.round(2), "ridge touch", R_PT.round(2))
    assert abs(L_PT[1]) < 1e-6 and abs(L_PT[0] - T) < 1e-6        # Lasso: corner (15, 0)
    assert R_PT.min() > 1                                         # Ridge: both coefficients clearly non-zero
    assert R_LEVEL < L_LEVEL                                      # the ring reaches the circle first
    name = "constraint_touch"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = ConstraintTouch()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=48:stats_mode=diff[p];"
                    "[b][p]paletteuse=dither=none:diff_mode=rectangle", str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
