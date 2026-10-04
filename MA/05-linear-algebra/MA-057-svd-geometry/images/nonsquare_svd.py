"""The SVD of a tall matrix, as three moves in 3D (built on 3Blue1Brown's picture of a 3 x 2 matrix taking the
plane into 3D, "Nonsquare matrices as transformations between dimensions"; the SVD sequence is our own, after
Strang section 7.4). B = [[1, 1], [0, 1], [1, 0]]. The unit circle lies on the floor (third coordinate 0).
V^T rotates it on the floor, Sigma stretches it to an ellipse (1.73 by 1) still on the floor, U turns it up onto the
tilted plane of B's outputs. The dashed curve is B applied in one step.
Run: python nonsquare_svd.py  -> nonsquare_svd.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
from scipy.spatial.transform import Rotation, Slerp

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, PURPLE_C, GREY_C, RED_C = "#4C78A8", "#F58518", "#B279A2", "#9A9A9A", "#E45756"
Text.set_default(color=BLACK, font="Latin Modern Roman")
B = np.array([[1.0, 1.0], [0.0, 1.0], [1.0, 0.0]])
U, S, Vt = np.linalg.svd(B)
if np.linalg.det(Vt) < 0:                         # make both factors proper rotations (flip a matching pair)
    Vt[1] *= -1
    U[:, 1] *= -1
if np.linalg.det(U) < 0:
    U[:, 2] *= -1                                 # the third column only multiplies zeros
SCALE = 1.6
PHI = np.linspace(0, 2 * np.pi, 121)
CIRCLE = np.c_[np.cos(PHI), np.sin(PHI)]
VS = Vt.T                                          # columns v1, v2
ROT_V = np.arctan2(Vt[1, 0], Vt[0, 0])             # V^T as an angle in the floor
SLERP = Slerp([0, 1], Rotation.from_matrix([np.eye(3), U]))


def stage(points2, a, b, c):
    """points2: n x 2 inputs; a, b, c in [0, 1] for the V^T, Sigma and U moves."""
    th = a * ROT_V
    R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    p = points2 @ R.T
    p = p * (1 + b * (S - 1))
    p3 = np.c_[p, np.zeros(len(p))]
    return p3 @ SLERP([c]).as_matrix()[0].T


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


class NonSquare(ThreeDScene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, text):
        new = boxed(Text(text, font_size=34), 0.08).to_corner(UL, buff=0.25)
        self.add_fixed_in_frame_mobjects(new)
        if self.cap is not None:
            self.remove(self.cap)
        self.cap = new
        self.add(new)

    def construct(self):
        self.snaps, self.cap = [], None
        self.set_camera_orientation(phi=68 * DEGREES, theta=-50 * DEGREES, zoom=1.0)
        axes = ThreeDAxes(x_range=[-2.5, 2.5], y_range=[-2.5, 2.5], z_range=[-1.6, 1.6], x_length=5 * SCALE,
                          y_length=5 * SCALE, z_length=3.2 * SCALE, axis_config={"color": GREY_C})
        floor = Surface(lambda u, v: np.array([u, v, 0]) * SCALE, u_range=[-2.2, 2.2], v_range=[-2.2, 2.2],
                        resolution=(4, 4), fill_opacity=0.08, checkerboard_colors=[GREY_C, GREY_C], stroke_width=0.5)
        self.add(axes, floor)
        a, b, c = ValueTracker(0), ValueTracker(0), ValueTracker(0)
        cur = lambda pts: stage(pts, a.get_value(), b.get_value(), c.get_value()) * SCALE

        def curve():
            return VMobject(stroke_color=BLUE_C, stroke_width=5).set_points_as_corners(list(cur(CIRCLE)))

        def arrows():
            p = cur(VS.T)
            return VGroup(Arrow3D(ORIGIN, p[0], color=ORANGE_C, thickness=0.03),
                          Arrow3D(ORIGIN, p[1], color=PURPLE_C, thickness=0.03))

        self.add(always_redraw(curve), always_redraw(arrows))
        self.caption("unit circle on the floor; arrows: v₁, v₂")
        self.begin_ambient_camera_rotation(rate=0.06)
        self.wait(1.2)
        self.snap()
        self.caption("Vᵀ: rotate v₁, v₂ onto the axes")
        self.play(a.animate.set_value(1), run_time=2.0)
        self.wait(0.5)
        self.caption("Σ (3 × 2): stretch by 1.73 and 1, still on the floor")
        self.play(b.animate.set_value(1), run_time=2.0)
        self.wait(0.6)
        self.snap()
        self.caption("U (3 × 3): turn the ellipse up into 3D")
        self.play(c.animate.set_value(1), run_time=3.0)
        n = np.cross(B[:, 0], B[:, 1])
        n = n / np.linalg.norm(n)
        e1 = B[:, 0] / np.linalg.norm(B[:, 0])
        e2 = np.cross(n, e1)
        plane = Surface(lambda u, v: (u * e1 + v * e2) * SCALE, u_range=[-2.2, 2.2], v_range=[-1.6, 1.6],
                        resolution=(4, 4), fill_opacity=0.18, checkerboard_colors=[RED_C, RED_C], stroke_width=0)
        direct = DashedVMobject(VMobject(stroke_color=RED_C, stroke_width=4).set_points_as_corners(
            list((CIRCLE @ B.T) * SCALE)), num_dashes=40)
        self.caption("the outputs of B fill only this tilted plane")
        self.play(FadeIn(plane), Create(direct), run_time=1.5)
        self.wait(3.0)
        self.snap()
        self.stop_ambient_camera_rotation()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (w, len(frames) * h + (len(frames) - 1) * gap), "white")
    for i, fr in enumerate(frames):
        sheet.paste(fr.convert("RGB"), (0, i * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    assert np.allclose(S, [np.sqrt(3), 1.0])                                  # the Note's singular values
    assert np.allclose(stage(CIRCLE, 1, 1, 1), CIRCLE @ B.T, atol=1e-9)        # three moves = B in one step
    name = "nonsquare_svd"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = NonSquare()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64:stats_mode=diff[p];"
                    "[b][p]paletteuse=dither=none", str(HERE / f"{name}.gif")], check=True)
    key_frames_grid([scene.snaps[0], scene.snaps[1], scene.snaps[2]], HERE / f"{name}_frames.png")
    shutil.rmtree(media)
