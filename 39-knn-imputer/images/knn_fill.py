"""KNN imputation of one gap, step by step: gap -> distances -> k = 2 nearest rows -> average fills the gap.
Run: python knn_fill.py  -> knn_fill.mp4, knn_fill.gif, knn_fill_frames.png"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
W, H = 1.3, 0.62
ROWS = [(1, ["30", "60", "NaN"], "8.66"), (2, ["NaN", "55", "20"], ""), (3, ["40", "52", "25"], "7.14"),
        (4, ["25", "NaN", "22"], "3.46"), (5, ["50", "70", "40"], "30.62")]


def cell(text, colour=GREY_C, fill=WHITE):
    box = Rectangle(width=W, height=H, stroke_color=GREY_C, stroke_width=2, fill_color=fill, fill_opacity=1)
    return VGroup(box, Text(text, font_size=26, color=colour).move_to(box))


class KnnFill(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, line1, line2=""):
        parts = [Text(line1, font_size=30, weight=BOLD)]
        if line2:
            parts.append(Text(line2, font_size=24, color=GREY_C))
        return VGroup(*parts).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.45)

    def construct(self):
        self.snaps = []
        pale_grey = ManimColor(GREY_C).interpolate(WHITE, 0.85)
        pale_red = ManimColor(RED_C).interpolate(WHITE, 0.82)
        table, labels, rows = VGroup(), VGroup(), {}
        for i, (r, vals, _) in enumerate(ROWS):
            cells = VGroup(*[cell(v, GREY_C if v == "NaN" else BLACK, pale_grey if v == "NaN" else WHITE)
                             for v in vals]).arrange(RIGHT, buff=0).shift(DOWN * H * i)
            rows[r] = cells
            table.add(cells)
            labels.add(Text(f"row {r}", font_size=24, color=GREY_C).next_to(cells, LEFT, buff=0.3))
        heads = VGroup(*[Text(h, font_size=26, weight=BOLD).next_to(rows[1][j], UP, buff=0.2)
                         for j, h in enumerate(["f1", "f2", "f3"])])
        board = VGroup(table, labels, heads).move_to(LEFT * 2.2 + UP * 1.0)
        gap = cell("NaN", RED_C, pale_red).move_to(rows[2][0])
        gap[0].set_stroke(RED_C, width=4)

        # Step 1: the gap
        cap = self.caption("Step 1: row 2 has a gap in f1", "f2 and f3 of row 2 are known: 55 and 20")
        self.play(FadeIn(board), FadeIn(cap))
        self.play(FadeIn(gap))
        self.wait(0.8)
        self.snap()

        # Step 2: the distance from row 2 to every other row
        dist_head = Text("distance to row 2", font_size=24, weight=BOLD).next_to(heads, RIGHT, buff=1.0)
        dists = VGroup(*[Text(d, font_size=26, color=GREY_C).move_to([dist_head.get_center()[0], rows[r].get_center()[1], 0])
                         for r, _, d in ROWS if d])
        self.play(FadeIn(dist_head), FadeIn(dists, lag_ratio=0.25),
                  Transform(cap, self.caption("Step 2: measure the distance to every other row",
                                              "nan-Euclidean: skip pairs with a NaN, scale up by a weight")), run_time=1.5)
        self.wait(0.8)
        self.snap()

        # Step 3: keep the k = 2 nearest rows
        near = {3: dists[1], 4: dists[2]}
        anims = [d.animate.set_color(GREEN_C) for d in near.values()]
        anims += [rows[r].animate.set_opacity(0.25) for r in (1, 5)] + [dists[i].animate.set_opacity(0.25) for i in (0, 3)]
        anims += [rows[r][0][0].animate.set_stroke(GREEN_C, width=5) for r in near]
        self.play(*anims, Transform(cap, self.caption("Step 3: keep the k = 2 nearest rows",
                                                      "row 4 (3.46) and row 3 (7.14)")), run_time=1.3)
        self.wait(0.8)
        self.snap()

        # Step 4: their f1 values fill the gap
        copies = VGroup(rows[4][0][1].copy(), rows[3][0][1].copy())
        filled = cell("32.5", GREEN_C, ManimColor(GREEN_C).interpolate(WHITE, 0.82)).move_to(gap)
        filled[0].set_stroke(GREEN_C, width=4)
        self.play(copies.animate.move_to(gap).set_opacity(0), FadeTransform(gap, filled),
                  Transform(cap, self.caption("Step 4: fill the gap with their f1 mean: (25 + 40) / 2 = 32.5",
                                              "with weights=\"distance\" the nearer row counts more: 29.90")), run_time=1.6)
        self.wait(1.8)
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
                     "output_file": "knn_fill", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = KnnFill()
        scene.render()
    mp4 = HERE / "knn_fill.mp4"
    shutil.copy(next(media.rglob("knn_fill.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "knn_fill.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "knn_fill_frames.png")
    shutil.rmtree(media)
