"""The normal equation as a projection, on the first three students of the placement data.
X has columns 1 = (1, 1, 1) and cgpa = (6.89, 5.12, 7.82); y = (3.26, 1.98, 3.25) (packages).
Every prediction X beta lies in the plane spanned by the two columns (the column space of X). y sticks out of it.
The closest point of the plane, y_hat = X beta_hat, is where the residual y - y_hat is perpendicular to the
plane, i.e. to both columns: X^T (y - X beta_hat) = 0, the normal equations.
Picture after ESL Figure 3.2 (geometry of least squares); our own data and code.
The scene is drawn in a rotated frame (lengths and angles kept) with the plane as the floor.
Run: python projection.py  -> projection.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C, PURPLE_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B", "#9D5BA8"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MathTex.set_default(color=BLACK)

X = np.array([[1, 6.89], [1, 5.12], [1, 7.82]])
Y = np.array([3.26, 1.98, 3.25])
BETA = np.linalg.solve(X.T @ X, X.T @ Y)
YHAT = X @ BETA
S = 1.6                                                  # screen units per data unit
K = 0.25                                                 # the 1 direction is drawn 4 times shorter (see below)
# drawing frame: f1 along the column of 1s, f2 along cgpa minus its mean, f3 the plane's normal (y on the + side).
# f1, f2, f3 are orthonormal, so the plane is the floor and the residual is vertical. Shrinking only the in-plane
# f1 axis keeps the residual perpendicular to the floor and its foot the closest point, so the picture stays true.
F1 = X[:, 0] / np.linalg.norm(X[:, 0])
F2 = X[:, 1] - X[:, 1].mean()
F2 /= np.linalg.norm(F2)
F3 = np.cross(F1, F2)
F3 *= np.sign(F3 @ Y)
R = np.vstack([K * F1, F2, F3])
SHIFT = np.array([-2.8, -1.6, 0])


def P(v):
    return S * (R @ np.asarray(v, float)) + SHIFT


def err(b):
    return np.linalg.norm(Y - X @ b)


def boxed(mob, buff=0.1):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


class Projection(ThreeDScene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def say(self, old, text, colour=BLACK):
        new = boxed(Text(text, font_size=34, color=colour, weight=BOLD)).to_edge(UP, buff=0.3)
        self.add_fixed_in_frame_mobjects(new)
        self.remove(new)
        self.play(FadeOut(old), FadeIn(new))
        return new

    def construct(self):
        self.snaps = []
        self.set_camera_orientation(phi=64 * DEGREES, theta=-100 * DEGREES, zoom=1.0)
        corners = [S * np.array([u, v, 0]) + SHIFT for u, v in ((-0.4, -0.8), (3.4, -0.8), (3.4, 2.3), (-0.4, 2.3))]
        plane = Polygon(*corners, color=BLUE_C, fill_opacity=0.18, stroke_width=1.5, stroke_opacity=0.5)
        ones = Arrow3D(P([0, 0, 0]), P(X[:, 0]), color=BLUE_C, thickness=0.02)
        cgpa = Arrow3D(P([0, 0, 0]), P(X[:, 1]), color=BLUE_C, thickness=0.02)
        cap = boxed(Text("Every prediction Xβ lies in this plane", font_size=34, weight=BOLD)).to_edge(UP, buff=0.3)
        lab = boxed(VGroup(VGroup(Text("columns of X:", font_size=28, color=BLUE_C),
                                  MathTex(r"\mathbf 1,\ \text{cgpa}", font_size=40, color=BLUE_C)).arrange(RIGHT),
                           Text("(1 direction drawn 4x shorter)", font_size=22, color=GREY_C))
                    .arrange(DOWN, aligned_edge=LEFT, buff=0.1)).to_corner(DL, buff=0.4)
        self.add_fixed_in_frame_mobjects(cap, lab)
        self.add(plane, ones, cgpa)
        self.wait(1.2)
        self.snap()

        yv = Arrow3D(P([0, 0, 0]), P(Y), color=ORANGE_C, thickness=0.025)
        ylab = boxed(MathTex(r"\mathbf y = \text{packages}", font_size=40, color=ORANGE_C)).to_corner(DR, buff=0.4)
        self.add_fixed_in_frame_mobjects(ylab)
        self.remove(ylab)
        cap = self.say(cap, "y sticks out of the plane: no β fits exactly")
        self.play(Create(yv), FadeIn(ylab))
        self.wait(0.6)

        # try points X beta in the plane; the dashed line to y is the error
        path = [np.array([0.0, 0.3]), np.array([1.2, 0.18]), np.array([-1.5, 0.62]), BETA]
        t = ValueTracker(0.0)

        def beta_now():
            s = t.get_value()
            i = min(int(s), len(path) - 2)
            return path[i] + (s - i) * (path[i + 1] - path[i])

        dot = always_redraw(lambda: Dot3D(P(X @ beta_now()), color=GREEN_C, radius=0.07))
        gap = always_redraw(lambda: DashedLine(P(X @ beta_now()), P(Y), color=RED_C, stroke_width=4, dash_length=0.06))
        num = DecimalNumber(err(path[0]), num_decimal_places=2, font_size=40, color=RED_C)
        def upd(m):
            m.set_value(err(beta_now()))
            self.renderer.camera.add_fixed_in_frame_mobjects(m)      # set_value makes new digits: keep them flat
        num.add_updater(upd)
        readout = boxed(VGroup(Text("error length", font_size=30, color=RED_C), num).arrange(RIGHT, buff=0.25))
        readout.next_to(ylab, UP, buff=0.25).align_to(ylab, RIGHT)
        self.add_fixed_in_frame_mobjects(readout)
        self.remove(readout)
        cap = self.say(cap, "Try points Xβ in the plane")
        self.add(dot, gap)
        self.play(FadeIn(readout))
        self.play(t.animate.set_value(1.0), run_time=2, rate_func=smooth)
        self.snap()
        self.play(t.animate.set_value(2.0), run_time=1.5, rate_func=smooth)
        cap = self.say(cap, "Closest point: the least-squares fit, error 0.36")
        self.play(t.animate.set_value(3.0), run_time=2)
        self.wait(0.8)

        # zoom on the foot: the residual is perpendicular to the plane
        u = -YHAT / np.linalg.norm(YHAT)
        z = (Y - YHAT) / np.linalg.norm(Y - YHAT)
        a = 0.12
        mark = VMobject(color=BLACK, stroke_width=3).set_points_as_corners(
            [P(YHAT + a * u), P(YHAT + a * u + a * z), P(YHAT + a * z)])
        res = Line(P(YHAT), P(Y), color=RED_C, stroke_width=6)
        cap = self.say(cap, "The residual meets the plane at a right angle", RED_C)
        self.play(FadeOut(gap), Create(res), Create(mark))
        self.move_camera(zoom=2.0, frame_center=P(YHAT), run_time=2.5)
        self.wait(0.8)
        self.snap()
        eq = boxed(MathTex(r"X^{\mathsf T}(\mathbf y - X\hat\beta) = 0", r"\ \Longrightarrow\ ",
                           r"X^{\mathsf T}X\hat\beta = X^{\mathsf T}\mathbf y", font_size=46), 0.15).to_edge(DOWN, buff=0.35)
        self.add_fixed_in_frame_mobjects(eq)
        self.remove(eq)
        self.play(FadeOut(lab), FadeOut(ylab), FadeOut(readout), FadeIn(eq))
        self.move_camera(theta=-65 * DEGREES, run_time=2.5)
        self.wait(2)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    print("beta", BETA.round(3), "y_hat", YHAT.round(3), "error", round(err(BETA), 3))
    assert np.allclose(X.T @ (Y - YHAT), 0, atol=1e-9)                  # residual perpendicular to both columns
    assert all(err(b) > err(BETA) for b in [np.array([0, 0.3]), np.array([1.2, 0.18]), np.array([-1.5, 0.62])])
    assert np.allclose(np.vstack([F1, F2, F3]) @ np.vstack([F1, F2, F3]).T, np.eye(3))   # orthonormal frame
    name = "projection"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = Projection()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=48:stats_mode=diff[p];"
                    "[b][p]paletteuse=dither=none:diff_mode=rectangle", str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
