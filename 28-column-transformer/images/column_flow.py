"""ColumnTransformer as a flow: each column goes to its own transformer, the outputs are stitched into one array.
Uses three real training rows of covid_toy.csv (split with random_state=0).
Run: python column_flow.py  -> column_flow.mp4, column_flow.gif, column_flow_frames.png"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MONO = "Latin Modern Mono"

W, HEAD_H, CELL_H, GAP = 1.75, 0.5, 0.42, 0.3   # column width, header height, cell height, gap between groups
TOP_Y, BOX_Y, OUT_Y = 3.55, 0.95, 0.05           # top of input columns, centre of transformer boxes, top of outputs

# three training rows: (age, gender, fever, cough, city); the second has a missing fever
AGE, GENDER, FEVER = ["22", "71", "75"], ["Female", "Male", "Female"], ["99", "NaN", "104"]
COUGH, CITY = ["Mild", "Strong", "Strong"], ["Bangalore", "Kolkata", "Delhi"]


def fit(t, width):
    return t.scale_to_fit_width(width) if t.width > width else t


def column(header, values, colour, red_rows=()):
    """One table column: coloured header on top of three white cells. Top-left corner at the origin."""
    head = Rectangle(width=W, height=HEAD_H, stroke_color=colour, fill_color=colour, fill_opacity=0.25, stroke_width=2)
    # names with "_" in mono: the serif underscore is so wide it reads as "__"
    head_t = Text(header, font_size=18, font=MONO) if "_" in header else Text(header, font_size=19, weight=BOLD)
    head_t = fit(head_t, W - 0.12).move_to(head)
    parts = [VGroup(head, head_t)]
    for i, v in enumerate(values):
        cell = Rectangle(width=W, height=CELL_H, stroke_color=colour, stroke_width=2)
        cell.next_to(parts[-1], DOWN, buff=0)
        txt = fit(Text(v, font_size=19, color=RED_C if i in red_rows else BLACK), W - 0.12).move_to(cell)
        parts.append(VGroup(cell, txt))
    return VGroup(*parts)


def place(cols, left_x, top_y):
    """Lay columns side by side starting at left_x, tops at top_y."""
    for i, c in enumerate(cols):
        c.move_to([left_x + W / 2 + i * W, top_y - c.height / 2, 0])
    return cols


class ColumnFlow(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, title, sub):
        return VGroup(Text(title, font_size=30, weight=BOLD), Text(sub, font_size=22, color=GREY_C)
                      ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.25)

    def construct(self):
        self.snaps = []
        age = column("age", AGE, GREY_C)
        gender = column("gender", GENDER, ORANGE_C)
        fever = column("fever", FEVER, PURPLE_C, red_rows=(1,))
        cough = column("cough", COUGH, BLUE_C)
        city = column("city", CITY, ORANGE_C)
        inputs = [age, gender, fever, cough, city]

        # group layout of the output: imputer (1 col) | ordinal (1) | one-hot (4) | passthrough (1)
        widths = [1, 1, 4, 1]
        lefts, x = [], -(7 * W + 3 * GAP) / 2
        for n in widths:
            lefts.append(x)
            x += n * W + GAP
        names = ["SimpleImputer", "OrdinalEncoder", "OneHotEncoder", "passthrough"]
        colours = [PURPLE_C, BLUE_C, ORANGE_C, GREY_C]
        boxes = VGroup()
        for left, n, name, c in zip(lefts, widths, names, colours):
            r = RoundedRectangle(corner_radius=0.12, width=n * W - 0.1, height=0.62, stroke_color=c,
                                 fill_color=WHITE, fill_opacity=1, stroke_width=3)
            r.move_to([left + n * W / 2, BOX_Y, 0])
            boxes.add(VGroup(r, fit(Text(name, font_size=20, color=c, font=MONO), n * W - 0.2).move_to(r)))

        # Step 0: the input table and the transformers waiting below it
        place(inputs, -5 * W / 2, TOP_Y)
        cap = self.caption("Training inputs: five columns, four different jobs",
                           "fever has missing values; cough is ordinal; gender and city are nominal; age is ready")
        self.play(FadeIn(VGroup(*inputs)), FadeIn(boxes), FadeIn(cap))
        self.wait(0.6)
        self.snap()

        # Step 1: route every column to the transformer that handles it
        targets = {fever: lefts[0], cough: lefts[1], age: lefts[3]}
        anims = [c.animate.move_to([l + W / 2, TOP_Y - c.height / 2, 0]) for c, l in targets.items()]
        oh_left = lefts[2] + (4 * W - 2 * W) / 2
        anims += [gender.animate.move_to([oh_left + W / 2, TOP_Y - gender.height / 2, 0]),
                  city.animate.move_to([oh_left + 3 * W / 2, TOP_Y - city.height / 2, 0])]
        self.play(*anims, Transform(cap, self.caption("1. Route each column to its transformer",
                                                      "age has no transformer: remainder='passthrough' keeps it as it is")),
                  run_time=1.6)
        arrows = VGroup(*[Arrow([b.get_center()[0], TOP_Y - age.height - 0.02, 0], b.get_top(), buff=0.05,
                                color=GREY_C, stroke_width=4, max_tip_length_to_length_ratio=0.35) for b in boxes])
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), GrowArrow(arrows[2]), GrowArrow(arrows[3]))
        self.wait(0.6)
        self.snap()

        # Step 2: each transformer produces its own output block below it
        outs = [
            [column("fever", ["99", "100.9", "104"], PURPLE_C, red_rows=(1,))],
            [column("cough", ["0", "1", "1"], BLUE_C)],
            [column("gender_Male", ["0", "1", "0"], ORANGE_C), column("city_Delhi", ["0", "0", "1"], ORANGE_C),
             column("city_Kolkata", ["0", "1", "0"], ORANGE_C), column("city_Mumbai", ["0", "0", "0"], ORANGE_C)],
            [column("age", AGE, GREY_C)],
        ]
        out_groups = VGroup(*[place(VGroup(*o), l, OUT_Y) for o, l in zip(outs, lefts)])
        down = VGroup(*[Arrow(b.get_bottom(), [b.get_center()[0], OUT_Y + 0.02, 0], buff=0.05, color=GREY_C,
                              stroke_width=4, max_tip_length_to_length_ratio=0.5) for b in boxes])
        self.play(*[GrowArrow(a) for a in down],
                  *[TransformFromCopy(VGroup(*src), dst) for src, dst in
                    zip([[fever], [cough], [gender, city], [age]], out_groups)],
                  Transform(cap, self.caption("2. Each transformer works only on its own columns",
                                              "missing fever filled with the training mean 100.9; Mild = 0, Strong = 1; "
                                              "2 nominal columns become 4")),
                  run_time=2.0)
        self.wait(0.8)
        self.snap()

        # Step 3: close the gaps: one array with 7 columns
        packed = [g.animate.shift(RIGHT * (-(7 * W) / 2 + sum(widths[:i]) * W - lefts[i])) for i, g in enumerate(out_groups)]
        self.play(*packed, FadeOut(down), FadeOut(arrows), FadeOut(VGroup(*inputs)), FadeOut(boxes),
                  Transform(cap, self.caption("3. Stitch the outputs side by side",
                                              "the result is one array: 80 rows, 7 columns (age moves to the end)")),
                  run_time=1.6)
        frame = SurroundingRectangle(out_groups, color=BLACK, buff=0.08, stroke_width=3)
        title = Text("transformed training data", font_size=26, weight=BOLD).next_to(frame, UP, buff=0.25)
        self.play(Create(frame), FadeIn(title))
        self.wait(1.5)
        self.snap()


def key_frames_grid(frames, out, gap=16, pad=20):
    # crop every frame to the area any frame uses, so the PDF grid is not mostly white space
    from PIL import ImageOps
    boxes = [ImageOps.invert(f.convert("RGB")).getbbox() for f in frames[:4]]
    l, t = min(b[0] for b in boxes) - pad, min(b[1] for b in boxes) - pad
    r, b_ = max(b[2] for b in boxes) + pad, max(b[3] for b in boxes) + pad
    frames = [f.crop((max(l, 0), max(t, 0), r, b_)) for f in frames]
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "column_flow", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = ColumnFlow()
        scene.render()
    mp4 = HERE / "column_flow.mp4"
    shutil.copy(next(media.rglob("column_flow.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "column_flow.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "column_flow_frames.png")
    shutil.rmtree(media)
