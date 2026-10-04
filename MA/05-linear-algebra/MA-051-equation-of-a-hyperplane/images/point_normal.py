"""A plane from one point and a normal vector. Plane: x1 + 2 x2 + 2 x3 = 5, normal w = [1, 2, 2], point x0 = (1, 1, 1).
1. One point does not fix a plane: the sheet can pivot about x0.  2. The normal vector w fixes it.
3. For every point x on the plane, the arrow x - x0 lies in the plane, at 90 degrees to w: w . (x - x0) = 0.
4. Changing w0 slides the plane along w; w does not turn.
Tool: Manim 3D (a moving plane and arrows in space). Idea after Khan Academy, "Defining a plane in R3 with a point and
normal vector". Run: python point_normal.py  -> point_normal.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
W, X0 = np.array([1.0, 2, 2]), np.array([1.0, 1, 1])
U1 = np.array([2.0, -1, 0]) / np.sqrt(5)                   # two unit directions inside the plane
U2 = np.cross(W, U1) / np.linalg.norm(np.cross(W, U1))
K = 0.8                                                    # screen units per data unit
R = 1.7                                                    # x circles x0 at this distance


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


def arrow3(a, b, colour):
    return Arrow3D(K * np.asarray(a, float), K * np.asarray(b, float), color=colour, thickness=0.035, height=0.25,
                   base_radius=0.09)


def sheet(centre, opacity=0.35, colour=BLUE_C):
    corners = [K * (centre + s * U1 + t * U2) for s, t in ((-2.4, -2.4), (2.4, -2.4), (2.4, 2.4), (-2.4, 2.4))]
    return Polygon(*corners, color=colour, fill_color=colour, fill_opacity=opacity, stroke_width=1.5)


def on_plane(t):
    return X0 + R * (np.cos(t) * U1 + np.sin(t) * U2)


class PointNormal(ThreeDScene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, *lines, colour=BLACK):
        group = VGroup(*[Text(t, font_size=30, color=colour, weight=BOLD) for t in lines]).arrange(DOWN, buff=0.12)
        out = boxed(group, 0.12).to_edge(DOWN, buff=0.25)
        self.add_fixed_in_frame_mobjects(out)
        return out

    def tag(self, tex, colour, below=None):
        out = boxed(MathTex(tex, color=colour, font_size=40), 0.1)
        out.to_corner(UL, buff=0.3) if below is None else out.next_to(below, DOWN, aligned_edge=LEFT, buff=0.15)
        self.add_fixed_in_frame_mobjects(out)
        return out

    def construct(self):
        self.snaps = []
        self.set_camera_orientation(phi=60 * DEGREES, theta=-5 * DEGREES, zoom=0.95)
        axes = ThreeDAxes(x_range=[-4, 4], y_range=[-4, 4], z_range=[-3, 4], x_length=8 * K, y_length=8 * K,
                          z_length=7 * K, axis_config={"stroke_color": GREY_C, "stroke_width": 2})
        plane = sheet(X0)
        p0 = Dot3D(K * X0, color=BLACK, radius=0.09)
        t0 = self.tag(r"x_0 = (1, 1, 1)", BLACK)
        self.add(axes, plane, p0)
        # 1. one point is not enough
        cap = self.caption("one point does not fix a plane:", "the sheet can pivot about it")
        for ang in (0.6, -1.0, 0.4):
            self.play(Rotate(plane, ang, axis=U1, about_point=K * X0), run_time=1.1)
        self.snap()
        # 2. the normal vector fixes it
        normal = arrow3(X0, X0 + 0.7 * W, ORANGE_C)
        t1 = self.tag(r"w = [1, 2, 2]", ORANGE_C, t0)
        self.remove(cap)
        cap = self.caption("a normal vector w fixes the plane:", "w stands at 90° to the sheet", colour=ORANGE_C)
        self.play(FadeIn(normal), run_time=0.8)
        self.wait(1.2)
        self.snap()
        # 3. x - x0 lies in the plane
        t = ValueTracker(0.3)
        px = always_redraw(lambda: Dot3D(K * on_plane(t.get_value()), color=GREEN_C, radius=0.09))
        diff = always_redraw(lambda: arrow3(X0, on_plane(t.get_value()), GREEN_C))
        t2 = self.tag(r"w \cdot (x - x_0) = 0", GREEN_C, t1)
        self.remove(cap)
        cap = self.caption("x moves on the plane: the arrow x − x0", "stays in the sheet, at 90° to w", colour=GREEN_C)
        self.add(px, diff)
        self.play(t.animate.set_value(2.6), run_time=2, rate_func=linear)
        self.snap()
        self.play(t.animate.set_value(0.3 + TAU), run_time=3.5, rate_func=linear)
        # 4. w0 slides the plane along w
        self.remove(px, diff, t2, cap)
        d = ValueTracker(5.0)                              # the plane is w . x = d, so w0 = -d

        def centre():
            return X0 + (d.get_value() - 5) / (W @ W) * W

        self.remove(plane, normal, p0)
        moving = always_redraw(lambda: sheet(centre()))
        mnormal = always_redraw(lambda: arrow3(centre(), centre() + 0.7 * W, ORANGE_C))
        self.add(moving, mnormal)
        cap = self.caption("change w0: the plane slides along w;", "w does not turn", colour=ORANGE_C)
        t2 = self.tag(r"x_1 + 2x_2 + 2x_3 + w_0 = 0", BLACK, t1)
        self.remove(t0)
        for target in (0.0, 9.0, 5.0):
            self.add(sheet(centre(), 0.08))
            self.play(d.animate.set_value(target), run_time=1.6)
            self.wait(0.4)
            if target == 0.0:
                self.snap()
        self.wait(1.5)


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet_img = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet_img.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet_img.save(out)


if __name__ == "__main__":
    assert np.isclose(W @ X0, 5) and np.isclose(W @ U1, 0) and np.isclose(W @ U2, 0)
    assert all(np.isclose(W @ (on_plane(a) - X0), 0) for a in np.linspace(0, 6, 7))
    name = "point_normal"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = PointNormal()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=48:stats_mode=diff[p];[b][p]paletteuse=dither=none:diff_mode=rectangle",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
