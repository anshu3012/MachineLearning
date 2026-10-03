"""One new passenger flowing through the fitted Titanic pipeline, step by step.
Values are the real outputs of the Notebook's fitted pipe for [2, male, 31.0, 0, 0, 10.5, S].
Run: python pipe_flow.py  -> pipe_flow.mp4, pipe_flow.gif, pipe_flow_frames.png"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image, ImageOps

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MONO = "Latin Modern Mono"
W, HEAD_H, CELL_H, ROW_Y = 1.34, 0.5, 0.5, 1.2

STEPS = [("trf1", "impute", PURPLE_C), ("trf2", "one-hot", ORANGE_C), ("trf3", "scale", GREEN_C),
         ("trf4", "select 8", RED_C), ("trf5", "tree", BLUE_C)]

# each stage: list of (key, header, value, colour, source key)
S0 = [("Pclass", "Pclass", "2", GREY_C, None), ("Sex", "Sex", "male", GREY_C, None),
      ("Age", "Age", "31.0", GREY_C, None), ("SibSp", "SibSp", "0", GREY_C, None),
      ("Parch", "Parch", "0", GREY_C, None), ("Fare", "Fare", "10.5", GREY_C, None),
      ("Embarked", "Embarked", "S", GREY_C, None)]
S1 = [("Age", "Age", "31.0", PURPLE_C, "Age"), ("Embarked", "Embarked", "S", PURPLE_C, "Embarked"),
      ("Pclass", "Pclass", "2", GREY_C, "Pclass"), ("Sex", "Sex", "male", GREY_C, "Sex"),
      ("SibSp", "SibSp", "0", GREY_C, "SibSp"), ("Parch", "Parch", "0", GREY_C, "Parch"),
      ("Fare", "Fare", "10.5", GREY_C, "Fare")]
S2 = [("eC", "Emb_C", "0", ORANGE_C, "Embarked"), ("eQ", "Emb_Q", "0", ORANGE_C, "Embarked"),
      ("eS", "Emb_S", "1", ORANGE_C, "Embarked"), ("sF", "Sex_f", "0", ORANGE_C, "Sex"),
      ("sM", "Sex_m", "1", ORANGE_C, "Sex"), ("Age", "Age", "31.0", GREY_C, "Age"),
      ("Pclass", "Pclass", "2", GREY_C, "Pclass"), ("SibSp", "SibSp", "0", GREY_C, "SibSp"),
      ("Parch", "Parch", "0", GREY_C, "Parch"), ("Fare", "Fare", "10.5", GREY_C, "Fare")]
SCALED = {"Age": "0.38", "Pclass": "0.5", "Fare": "0.02"}
S3 = [(k, h, SCALED.get(k, v), GREEN_C, k) for k, h, v, _, _ in S2]
S4 = [(k, h, v, RED_C, k) for k, h, v, _, _ in S3 if k not in ("eQ", "Age")]


def fit(t, width):
    return t.scale_to_fit_width(width) if t.width > width else t


def cell(header, value, colour):
    head = Rectangle(width=W, height=HEAD_H, stroke_color=colour, fill_color=colour, fill_opacity=0.25, stroke_width=2)
    ht = fit(Text(header, font_size=18, font=MONO) if "_" in header else Text(header, font_size=19, weight=BOLD),
             W - 0.12).move_to(head)
    body = Rectangle(width=W, height=CELL_H, stroke_color=colour, stroke_width=2).next_to(head, DOWN, buff=0)
    vt = fit(Text(value, font_size=21), W - 0.12).move_to(body)
    return VGroup(head, ht, body, vt)


def row(specs):
    n = len(specs)
    cells = {}
    for i, (k, h, v, c, _) in enumerate(specs):
        cells[k] = cell(h, v, c).move_to([(i - (n - 1) / 2) * W, ROW_Y, 0])
    return cells


class PipeFlow(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, title, sub):
        return VGroup(Text(title, font_size=30, weight=BOLD), Text(sub, font_size=22, color=GREY_C)
                      ).arrange(DOWN, buff=0.12).move_to([0, -2.4, 0])

    def shape_label(self, n):
        return Text(f"1 row × {n} columns", font_size=22, color=GREY_C).move_to([0, ROW_Y + 0.95, 0])

    def morph(self, old, specs, cap, extra=()):
        new = row(specs)
        anims = []
        for ok, om in old.items():
            targets = [new[k] for k, _, _, _, s in specs if s == ok]
            if len(targets) == 1:
                anims.append(ReplacementTransform(om, targets[0]))
            elif targets:
                anims.append(ReplacementTransform(om, VGroup(*targets)))
            else:
                anims.append(FadeOut(om, shift=DOWN * 0.6))
        self.play(*anims, *extra, Transform(self.cap, cap), Transform(self.size, self.shape_label(len(specs))),
                  run_time=1.8)
        # replace the temporary groups with the plain cells
        for m in list(self.mobjects):
            if m not in (self.bar, self.cap, self.size, *self.keep):
                self.remove(m)
        self.add(*new.values())
        self.wait(0.9)
        self.snap()
        return new

    def construct(self):
        self.snaps, self.keep = [], []
        boxes = VGroup()
        for name, job, c in STEPS:
            r = RoundedRectangle(corner_radius=0.12, width=2.0, height=0.85, stroke_color=c, stroke_width=3,
                                 fill_color=c, fill_opacity=0.08)
            t = VGroup(Text(name, font_size=22, weight=BOLD, color=c), Text(job, font_size=18)).arrange(DOWN, buff=0.06)
            boxes.add(VGroup(r, t.move_to(r)))
        boxes.arrange(RIGHT, buff=0.55).move_to([0, 3.2, 0])
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.05, color=GREY_C,
                                stroke_width=4, max_tip_length_to_length_ratio=0.4) for i in range(4)])
        frame = SurroundingRectangle(boxes, color=GREY_C, buff=0.15, stroke_width=2)
        label = Text("fitted pipe", font_size=20, color=GREY_C, font=MONO).next_to(frame, LEFT, buff=0.15)
        self.bar = VGroup(boxes, arrows, frame, label)

        cells = row(S0)
        self.size = self.shape_label(7)
        self.cap = self.caption("A new passenger: one row, 7 columns",
                                "pipe.predict(new) sends it through the steps fitted on the 712 training rows")
        self.play(FadeIn(self.bar), FadeIn(VGroup(*cells.values())), FadeIn(self.size), FadeIn(self.cap))
        self.wait(0.8)
        self.snap()

        def light(i):
            return [b[0].animate.set_fill(opacity=0.3 if j == i else 0.08) for j, b in enumerate(boxes)]

        cells = self.morph(cells, S1, self.caption("trf1: impute Age and Embarked",
                           "nothing is missing here; the two imputed columns move to the front"), light(0))
        cells = self.morph(cells, S2, self.caption("trf2: one-hot encode positions 1 and 3",
                           "Embarked becomes 3 columns and Sex 2: now 10 columns"), light(1))
        cells = self.morph(cells, S3, self.caption("trf3: scale every column to 0 to 1",
                           "with the training min and max: Age 31 is 0.38, Pclass 2 is 0.5, Fare 10.5 is 0.02"),
                           light(2))
        cells = self.morph(cells, S4, self.caption("trf4: keep the 8 best columns",
                           "the chi-squared test chose them on the training set; Emb_Q and Age are dropped"),
                           light(3))

        result = VGroup(RoundedRectangle(corner_radius=0.12, width=4.4, height=0.8, stroke_color=BLUE_C,
                                         stroke_width=3, fill_color=WHITE, fill_opacity=1),
                        Text("prediction: 0", font_size=28, weight=BOLD, color=BLUE_C)).move_to([0, -0.85, 0])
        result[1].move_to(result[0])
        down = Arrow([0, ROW_Y - 0.55, 0], result.get_top(), buff=0.05, color=GREY_C, stroke_width=4,
                     max_tip_length_to_length_ratio=0.35)
        self.keep = [result, down]
        self.play(*light(4), GrowArrow(down), FadeIn(result),
                  Transform(self.cap, self.caption("trf5: the decision tree predicts",
                                                   "0 = does not survive; no preprocessing code was written by hand")),
                  run_time=1.6)
        self.wait(1.5)
        self.snap()


def key_frames_grid(frames, out, cols=2, gap=16, pad=20):
    # crop every frame to the area any frame uses, so the PDF grid is not mostly white space
    boxes = [ImageOps.invert(f.convert("RGB")).getbbox() for f in frames]
    l, t = min(b[0] for b in boxes) - pad, min(b[1] for b in boxes) - pad
    r, b_ = max(b[2] for b in boxes) + pad, max(b[3] for b in boxes) + pad
    frames = [f.crop((max(l, 0), max(t, 0), r, b_)) for f in frames]
    w, h = frames[0].size
    rows = (len(frames) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w + (cols - 1) * gap, rows * h + (rows - 1) * gap), "white")
    for i, f in enumerate(frames):
        sheet.paste(f.convert("RGB"), ((i % cols) * (w + gap), (i // cols) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "pipe_flow", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = PipeFlow()
        scene.render()
    mp4 = HERE / "pipe_flow.mp4"
    shutil.copy(next(media.rglob("pipe_flow.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "pipe_flow.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "pipe_flow_frames.png")
    shutil.rmtree(media)
