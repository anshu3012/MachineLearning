"""Elastic Net between Lasso and Ridge, as geometry. Two diabetes features (bmi and s1, training split of the
Lasso Note, each scaled to standard deviation 1) and a budget t = 15. The allowed region
    r (|b1| + |b2|) / t + (1 - r) (b1^2 + b2^2) / t^2 <= 1
is Lasso's diamond at l1_ratio r = 1 and Ridge's circle at r = 0; every shape in between keeps the corners at
(+-t, 0) and (0, +-t). As r falls, the loss ellipse's first touch stays on the corner (s1 coefficient exactly 0)
until the shape is round enough, then slides off the axis.
Picture after ESL Figure 3.11 and Zou and Hastie (2005) Figure 1; our own data and code.
Run: python shape_morph.py  -> shape_morph.mp4, .gif, _frames.png"""
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
T = 15.0
XR, YR = (-20, 60), (-20, 25)


def data():
    d = load_diabetes(as_frame=True)
    Xtr, _, ytr, _ = train_test_split(d.data, d.target, test_size=0.2, random_state=2)
    A = Xtr[["bmi", "s1"]]
    A = ((A - A.mean()) / A.std()).values
    yc = (ytr - ytr.mean()).values
    Q = A.T @ A / len(A)
    return Q, np.linalg.solve(Q, A.T @ yc / len(A))


Q, BETA = data()
W, V = np.linalg.eigh(Q)
TH = np.linspace(0, 2 * np.pi, 8000, endpoint=False)
U = np.c_[np.cos(TH), np.sin(TH)]
L1 = np.abs(U).sum(1)


def region(r):
    """Boundary points of the Elastic Net region for l1_ratio r (radius along each direction)."""
    a2, b2 = (1 - r) / T ** 2, r * L1 / T
    s = 1 / b2 if a2 == 0 else (-b2 + np.sqrt(b2 ** 2 + 4 * a2)) / (2 * a2)
    return U * s[:, None]


def loss(B):
    R = B - BETA
    return np.einsum("ij,jk,ik->i", R, Q, R)


def solve(r):
    pts = region(r)
    ls = loss(pts)
    i = ls.argmin()
    return pts[i], ls[i]


def ellipse(level):
    return BETA + (U * np.sqrt(level / W)) @ V.T


def boxed(mob, buff=0.1):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


R_GRID = np.linspace(1, 0, 101)
PATH = np.array([solve(r)[0][1] for r in R_GRID])                 # s1 coefficient along the sweep
R_LAST_ZERO = R_GRID[np.abs(PATH) < 0.05].min()


class ShapeMorph(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        ax = Axes(x_range=[*XR, 10], y_range=[*YR, 10], x_length=7.0, y_length=7.0 * 45 / 80, tips=False,
                  axis_config={"color": GREY_C, "stroke_width": 2}).move_to([-3.2, 0.6, 0])
        xl = Text("bmi", font_size=26, color=GREY_C).next_to(ax.c2p(XR[1], 0), DOWN, buff=0.12).shift(LEFT * 0.3)
        yl = Text("s1", font_size=26, color=GREY_C).next_to(ax.c2p(0, YR[1]), RIGHT, buff=0.12).shift(DOWN * 0.2)
        ols = Dot(ax.c2p(*BETA), color=BLACK, radius=0.07)
        ols_t = boxed(Text("least squares", font_size=24), 0.05).next_to(ols, UP, buff=0.12)
        plot = Axes(x_range=[0, 1, 0.5], y_range=[0, 5, 1], x_length=4.6, y_length=3.4, tips=False,
                    axis_config={"color": GREY_C, "include_numbers": True, "font_size": 26,
                                 "decimal_number_config": {"color": BLACK, "num_decimal_places": 1}}).move_to([4.3, 0.2, 0])
        px = Tex(r"\texttt{l1\_ratio}", font_size=34).next_to(plot.x_axis, DOWN, buff=0.45)
        py = MathTex(r"b_{\text{s1}}", font_size=36).next_to(plot.y_axis, UP, buff=0.15)
        r = ValueTracker(1.0)

        def shape():
            c = interpolate_color(ManimColor(BLUE_C), ManimColor(RED_C), r.get_value())
            return Polygon(*[ax.c2p(*p) for p in region(r.get_value())[::40]], color=c, fill_opacity=0.3, stroke_width=4)

        def ring():
            pt, lev = solve(r.get_value())
            pts = ellipse(lev)
            ok = (pts[:, 0] >= XR[0]) & (pts[:, 0] <= XR[1]) & (pts[:, 1] >= YR[0]) & (pts[:, 1] <= YR[1])
            pts = np.roll(pts, -int(np.argmin(ok)), axis=0)            # start the loop at a point outside the window
            ok = np.roll(ok, -int(np.argmin(ok)))
            g, run = VGroup(), []
            for p, inside in zip(pts, ok):
                if inside:
                    run.append(ax.c2p(*p))
                elif len(run) > 1:
                    g.add(VMobject(color=ORANGE_C, stroke_width=4).set_points_as_corners(run))
                    run = []
                else:
                    run = []
            if len(run) > 1:
                g.add(VMobject(color=ORANGE_C, stroke_width=4).set_points_as_corners(run))
            zero = abs(pt[1]) < 0.05
            g.add(Dot(ax.c2p(*pt), color=RED_C if zero else BLUE_C, radius=0.11))
            return g

        def trace():
            k = int(round((1 - r.get_value()) * 100)) + 1
            pts = [plot.c2p(rr, b) for rr, b in zip(R_GRID[:k], PATH[:k])]
            line = VMobject(color=GREEN_C, stroke_width=5).set_points_as_corners(pts) if k > 1 else VGroup()
            b = np.interp(r.get_value(), R_GRID[::-1], PATH[::-1])
            return VGroup(line, Dot(plot.c2p(r.get_value(), b), color=GREEN_C, radius=0.1))

        def readout():
            b = np.interp(r.get_value(), R_GRID[::-1], PATH[::-1])
            b = 0.0 if abs(b) < 0.05 else b
            return boxed(MathTex(rf"\text{{l1\_ratio}} = {r.get_value():.2f}\qquad b_{{\text{{s1}}}} = {b:.2f}",
                                 font_size=40)).to_edge(DOWN, buff=0.3)

        title = boxed(Tex(r"\textbf{\texttt{l1\_ratio} from 1 (Lasso) to 0 (Ridge)}", font_size=44)).to_edge(UP, buff=0.25)
        self.add(ax, xl, yl, plot, px, py, always_redraw(shape), always_redraw(ring), ols, ols_t,
                 always_redraw(trace), always_redraw(readout), title)
        self.wait(1.5)
        self.snap()
        self.play(r.animate.set_value(R_LAST_ZERO), run_time=3, rate_func=linear)
        note = boxed(Text("still a corner: exactly 0", font_size=28, color=RED_C, weight=BOLD)).move_to(plot.c2p(0.55, 4.6))
        self.play(FadeIn(note))
        self.wait(1.2)
        self.snap()
        self.play(FadeOut(note))
        self.play(r.animate.set_value(0.25), run_time=3, rate_func=linear)
        self.wait(0.5)
        self.snap()
        self.play(r.animate.set_value(0.0), run_time=1.5, rate_func=linear)
        note2 = boxed(Text("circle: never exactly 0", font_size=28, color=BLUE_C, weight=BOLD)).move_to(plot.c2p(0.55, 4.6))
        self.play(FadeIn(note2))
        self.wait(2.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    print("least squares", BETA.round(2), "s1 stays 0 down to l1_ratio", R_LAST_ZERO.round(2),
          "ridge s1", PATH[-1].round(2))
    assert abs(PATH[0]) < 0.05 and PATH[-1] > 1                    # Lasso zero, Ridge clearly not
    assert 0.3 < R_LAST_ZERO < 0.9                                  # the zero survives a real range of mixes
    assert np.all(np.diff(PATH) >= -0.05)                           # the coefficient only grows as r falls
    name = "shape_morph"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = ShapeMorph()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=48:stats_mode=diff[p];"
                    "[b][p]paletteuse=dither=none:diff_mode=rectangle", str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
