"""Tree-level column sampling (bagging) against node-level column sampling (random forest), 2 of 5 columns.
Run: python column_sampling.py  -> column_sampling.mp4, column_sampling.gif, column_sampling_frames.png"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")

# tree shape: three split nodes and four leaves; positions relative to the panel centre
NODES = {"a": (0, 0.9), "b": (-1.5, -0.6), "c": (1.5, -0.6)}
LEAVES = [(-2.3, -2.0), (-0.7, -2.0), (0.7, -2.0), (2.3, -2.0)]
EDGES = [("a", "b"), ("a", "c")]
LEAF_EDGES = [("b", 0), ("b", 1), ("c", 2), ("c", 3)]
# bagging: one draw for the whole tree; random forest: one draw per node (the column chosen is the first of the pair)
BAG_DRAW, BAG_SPLITS = (1, 3), {"a": 3, "b": 1, "c": 3}
RF_DRAWS = {"a": (2, 3), "b": (4, 5), "c": (2, 1)}
RF_SPLITS = {"a": 3, "b": 4, "c": 1}


def chips(centre):
    """Five column cards: col1 ... col5."""
    g = VGroup(*[VGroup(RoundedRectangle(width=0.95, height=0.5, corner_radius=0.08, color=GREY_C, stroke_width=2),
                        Text(f"col{i}", font_size=20)) for i in range(1, 6)]).arrange(RIGHT, buff=0.12)
    return g.move_to(centre)


def split_node(label, pos):
    box = RoundedRectangle(width=1.25, height=0.6, corner_radius=0.1, color=GREEN_C, fill_color="#E5F1E3",
                           fill_opacity=1, stroke_width=3)
    return VGroup(box, Text(label, font_size=22)).move_to(pos).set_z_index(2)


def leaf(pos):
    return Circle(radius=0.16, color=GREY_C, fill_color=WHITE, fill_opacity=1, stroke_width=3).move_to(pos).set_z_index(2)


def light(chip_group, idx, colour):
    return [chip_group[i - 1][0].animate.set_fill(colour, opacity=0.35).set_stroke(colour) for i in idx]


def reset(chip_group):
    return [c[0].animate.set_fill(WHITE, opacity=0).set_stroke(GREY_C) for c in chip_group]


class ColumnSampling(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def tree_skeleton(self, centre):
        pts = {k: centre + np.array([x, y, 0]) for k, (x, y) in NODES.items()}
        lv = [centre + np.array([x, y, 0]) for x, y in LEAVES]
        return pts, lv

    def construct(self):
        self.snaps = []
        left, right = np.array([-3.6, -0.9, 0]), np.array([3.6, -0.9, 0])
        t1 = Text("bagging: columns drawn once per tree", font_size=24).move_to([-3.6, 3.5, 0])
        t2 = Text("random forest: drawn again at every node", font_size=24).move_to([3.6, 3.5, 0])
        divider = DashedLine([0, 3.8, 0], [0, -3.6, 0], color=GREY_C)
        c1, c2 = chips([-3.6, 2.6, 0]), chips([3.6, 2.6, 0])
        self.add(t1, t2, divider, c1, c2)

        # ---- bagging: one draw, then every node uses those two columns ----
        pts, lv = self.tree_skeleton(left)
        draw_note = Text("this tree may only use col1 and col3", font_size=22, color=BLUE_C).move_to([-3.6, 1.95, 0])
        self.play(*light(c1, BAG_DRAW, BLUE_C), FadeIn(draw_note), run_time=0.8)
        self.wait(0.4)
        self.snap()
        for k in ["a", "b", "c"]:
            node = split_node(f"col{BAG_SPLITS[k]}", pts[k])
            edges = [Line(pts[p], pts[q], color=GREY_C, stroke_width=3).set_z_index(-1) for p, q in EDGES if q == k]
            self.play(*[Create(e) for e in edges], FadeIn(node), run_time=0.5)
        self.play(*[Create(Line(pts[p], lv[i], color=GREY_C, stroke_width=3).set_z_index(-1)) for p, i in LEAF_EDGES],
                  *[FadeIn(leaf(p)) for p in lv], run_time=0.5)
        self.wait(0.5)
        self.snap()

        # ---- random forest: a fresh draw at each node ----
        pts, lv = self.tree_skeleton(right)
        note = None
        for k in ["a", "b", "c"]:
            draw = RF_DRAWS[k]
            new_note = Text(f"this node: col{draw[0]} or col{draw[1]}", font_size=22, color=ORANGE_C).move_to([3.6, 1.95, 0])
            anims = reset(c2) if note is not None else []
            self.play(*anims, run_time=0.25) if anims else None
            self.play(*light(c2, draw, ORANGE_C), FadeIn(new_note) if note is None else Transform(note, new_note),
                      run_time=0.6)
            if note is None:
                note = new_note
            node = split_node(f"col{RF_SPLITS[k]}", pts[k])
            edges = [Line(pts[p], pts[q], color=GREY_C, stroke_width=3).set_z_index(-1) for p, q in EDGES if q == k]
            self.play(*[Create(e) for e in edges], FadeIn(node), run_time=0.5)
            self.wait(0.3)
            if k == "b":
                self.snap()
        self.play(*[Create(Line(pts[p], lv[i], color=GREY_C, stroke_width=3).set_z_index(-1)) for p, i in LEAF_EDGES],
                  *[FadeIn(leaf(p)) for p in lv], *reset(c2), FadeOut(note), run_time=0.6)
        s1 = Text("every split: col1 or col3", font_size=24, color=BLUE_C).move_to([-3.6, -3.4, 0])
        s2 = Text("splits use col3, col4, col1", font_size=24, color=ORANGE_C).move_to([3.6, -3.4, 0])
        self.play(FadeIn(s1), FadeIn(s2), run_time=0.6)
        self.wait(1.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, hgt = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * hgt + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (hgt + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "column_sampling", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = ColumnSampling()
        scene.render()
    mp4 = HERE / "column_sampling.mp4"
    shutil.copy(next(media.rglob("column_sampling.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "column_sampling.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "column_sampling_frames.png")
    shutil.rmtree(media)
