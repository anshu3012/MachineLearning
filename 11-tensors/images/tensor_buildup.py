"""Each tensor is a collection of tensors one dimension lower: scalars -> vector -> matrix -> 3D -> 4D.
Run: python tensor_buildup.py  -> tensor_buildup.mp4, tensor_buildup.gif, tensor_buildup_frames.png"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
CELL = 0.75


def cell(colour, value=None):
    light = ManimColor(colour).interpolate(WHITE, 0.82)      # solid pale fill hides the layers behind
    sq = Square(CELL, stroke_color=colour, stroke_width=2, fill_color=light, fill_opacity=1)
    if value is None:
        return sq
    return VGroup(sq, Text(str(value), font_size=26).move_to(sq))


def row(colour, values, numbers=True):
    return VGroup(*[cell(colour, v if numbers else None) for v in values]).arrange(RIGHT, buff=0)


def matrix(colour, rows=3, cols=4, start=1, numbers=True):
    return VGroup(*[row(colour, range(start + r * cols, start + (r + 1) * cols), numbers)
                    for r in range(rows)]).arrange(DOWN, buff=0)


def stack(colour, depth=3):
    layers = VGroup(*[matrix(colour, numbers=(d == 0)) for d in range(depth)])   # numbers on the front layer only
    for d, layer in enumerate(layers):
        layer.shift(UR * 0.3 * d)
        layer.set_z_index(depth - d)                   # front layer always drawn on top
    return VGroup(*reversed(layers))          # draw the back layer first


class TensorBuildup(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, title, shape):
        return VGroup(Text(title, font_size=34, weight=BOLD), Text(shape, font_size=26, color=GREY_C)
                      ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)

    def construct(self):
        self.snaps = []
        # Step 1: four scalars line up into a vector
        scalars = VGroup(*[cell(BLUE_C, v) for v in [1, 2, 3, 4]]).arrange(RIGHT, buff=0.6)
        cap = self.caption("4 scalars (0D)", "each has shape ()")
        self.play(FadeIn(scalars, lag_ratio=0.2), FadeIn(cap))
        vector = row(BLUE_C, [1, 2, 3, 4])
        new_cap = self.caption("lined up: a vector (1D)", "shape (4,)")
        self.play(Transform(scalars, vector), Transform(cap, new_cap), run_time=1.2)
        self.wait(0.6)
        self.snap()

        # Step 2: three vectors stack into a matrix
        mat = matrix(BLUE_C)
        self.play(Transform(scalars, mat[0]), FadeIn(mat[1:], shift=DOWN * 0.3),
                  Transform(cap, self.caption("3 vectors stacked: a matrix (2D)", "shape (3, 4)")), run_time=1.2)
        self.remove(scalars)
        self.add(mat)
        self.wait(0.6)
        self.snap()

        # Step 3: three matrices stack into a 3D tensor
        cube = stack(GREEN_C)
        self.play(ReplacementTransform(mat, cube[-1]), FadeIn(cube[:-1], shift=UR * 0.3),
                  Transform(cap, self.caption("3 matrices stacked: a 3D tensor", "shape (3, 3, 4)")), run_time=1.4)
        self.wait(0.6)
        self.snap()

        # Step 4: 3D tensors line up into a 4D tensor
        cubes = VGroup(*[stack(ORANGE_C) for _ in range(3)]).arrange(RIGHT, buff=0.6).scale(0.62).shift(UP * 0.4)
        self.play(ReplacementTransform(cube, cubes[0]), FadeIn(cubes[1:], shift=LEFT * 0.4),
                  Transform(cap, self.caption("3 of those lined up: a 4D tensor", "shape (3, 3, 3, 4)")), run_time=1.4)
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
                     "output_file": "tensor_buildup", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = TensorBuildup()
        scene.render()
    mp4 = HERE / "tensor_buildup.mp4"
    shutil.copy(next(media.rglob("tensor_buildup.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "tensor_buildup.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "tensor_buildup_frames.png")
    shutil.rmtree(media)
