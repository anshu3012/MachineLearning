"""The three paths from the loss back to the shared input weight, on the unrolled 3-step RNN: each path lights up
in its own colour and writes its term (one-node example of section 6.3: -0.196, 0, -0.086); the terms then add
up to the gradient -0.282. Manim: paths are traced one after another.
Run: python three_paths.py -> three_paths.gif, three_paths_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
import manimpango

for _f in Path("/usr/share/texmf/fonts/opentype/public/lm").glob("lmroman10-*.otf"):
    manimpango.register_font(str(_f))

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MarkupText.set_default(color=BLACK, font="Latin Modern Roman")


class Snap(Scene):
    """A scene that keeps key frames for the PDF grid."""
    def snap(self):
        if not hasattr(self, "snaps"):
            self.snaps = []
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))


def render(scene_cls, name, fps=10, width=760):
    """Render to <name>.gif and a 2 x 2 grid of the scene's first four key frames, <name>_frames.png."""
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = scene_cls()
        scene.render()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(next(media.rglob(f"{name}.mp4"))), "-vf",
                    f"fps={fps},scale={width}:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    w, h = scene.snaps[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, f in enumerate(scene.snaps[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / f"{name}_frames.png")
    shutil.rmtree(media)

# one-node example of the Note: w_i = 0.5, w_h = 0.8, w_o = 1, x = (1, 0, 1), y = 1
wi, wh, wo, xs, y = 0.5, 0.8, 1.0, (1.0, 0.0, 1.0), 1.0
h = [0.0]
for x in xs:
    h.append(np.tanh(wi * x + wh * h[-1]))
yhat = 1 / (1 + np.exp(-wo * h[3]))
d = [1 - v ** 2 for v in h]
err = (yhat - y) * wo
TERMS = [err * d[3] * xs[2], err * d[3] * wh * d[2] * xs[1], err * d[3] * wh * d[2] * wh * d[1] * xs[0]]
assert [round(t, 3) for t in TERMS] == [-0.196, 0.0, -0.086] and round(sum(TERMS), 3) == -0.282
COLS = [GREEN_C, ORANGE_C, PURPLE_C]
VIA = ["L → ŷ → h<sub>3</sub> → w<sub>i</sub>", "L → ŷ → h<sub>3</sub> → h<sub>2</sub> → w<sub>i</sub>",
       "L → ŷ → h<sub>3</sub> → h<sub>2</sub> → h<sub>1</sub> → w<sub>i</sub>"]


def box(label, colour, at):
    b = VGroup(RoundedRectangle(corner_radius=0.1, width=1.0, height=0.7, stroke_color=colour, stroke_width=4,
                                fill_color=WHITE, fill_opacity=1), MarkupText(label, font_size=30))
    return b.move_to(at)


class Paths(Snap):
    def construct(self):
        title = MarkupText("w<sub>i</sub> is used at every time step: three paths from the loss", font_size=34).to_edge(UP, buff=0.3)
        Y, X = 2.0, [-6.0, -3.6, -1.2, 1.2, 3.6, 5.8]
        hs = [box("h<sub>0</sub>", GREY_C, [X[0], Y, 0])] + [box(f"h<sub>{t}</sub>", PURPLE_C, [X[t], Y, 0]) for t in (1, 2, 3)]
        yh, L = box("ŷ", GREEN_C, [X[4], Y, 0]), box("L", RED_C, [X[5], Y, 0])
        xin = [box(f"x<sub>{t}</sub>", BLUE_C, [X[t], Y - 1.9, 0]) for t in (1, 2, 3)]
        fwd = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.05, stroke_width=3, color=GREY_C,
                             max_tip_length_to_length_ratio=0.2) for a, b in zip(hs + [yh], hs[1:] + [yh, L])],
                     *[Arrow(xin[t].get_top(), hs[t + 1].get_bottom(), buff=0.05, stroke_width=3, color=BLUE_C,
                             max_tip_length_to_length_ratio=0.2) for t in range(3)])
        wl = VGroup(*[MarkupText("w<sub>i</sub>", font_size=28, color=BLUE_C).move_to([X[t + 1] + 0.4, Y - 0.95, 0])
                      for t in range(3)],
                    *[MarkupText("w<sub>h</sub>", font_size=24, color=GREY_C).move_to([(X[t] + X[t + 1]) / 2, Y + 0.3, 0])
                      for t in range(3)])
        self.play(FadeIn(title), FadeIn(VGroup(*hs, yh, L, *xin)), FadeIn(fwd), FadeIn(wl), run_time=1.0)
        self.wait(0.8)

        rows = VGroup()
        for k in range(3):
            t = 3 - k                                            # the time step whose use of w_i this path reaches
            off = (k - 1) * 0.13
            pts = [L.get_center() + UP * off] + [[X[j], Y + off, 0] for j in range(4, t - 1, -1)]
            pts.append([X[t] - 0.12 + 0.12 * k, Y - 0.95, 0])
            path = VMobject(stroke_color=COLS[k], stroke_width=12, stroke_opacity=0.55).set_points_as_corners(pts)
            tip = Dot(pts[-1], radius=0.13, color=COLS[k])
            val = f"{TERMS[k]:.3f}".replace("-", "−") if abs(TERMS[k]) > 1e-9 else "0   (x<sub>2</sub> = 0)"
            row = MarkupText(f"path {k + 1}:  {VIA[k]}   =   <b>{val}</b>", font_size=30, color=COLS[k])
            row.move_to([-5.8, -1.0 - 0.62 * k, 0], aligned_edge=LEFT)
            self.play(Create(path), run_time=1.0 + 0.4 * k)
            self.play(FadeIn(tip, scale=2), Indicate(wl[t - 1], color=COLS[k], scale_factor=1.5), FadeIn(row), run_time=0.7)
            self.wait(0.9)
            self.snap()
            rows.add(row)
        total = MarkupText("∂L/∂w<sub>i</sub>  =  −0.196 + 0 − 0.086  =  <b>−0.282</b>", font_size=36, color=RED_C)
        total.move_to([-5.8, -3.2, 0], aligned_edge=LEFT)
        line = Line([-5.8, -2.72, 0], [2.5, -2.72, 0], stroke_color=GREY_C, stroke_width=2)
        self.play(Create(line), FadeIn(total, shift=UP * 0.2), run_time=0.8)
        self.wait(2.5)
        self.snap()


if __name__ == "__main__":
    render(Paths, "three_paths")
