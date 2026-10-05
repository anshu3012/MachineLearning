"""MICE on the 5-row table: mean fill -> iteration 1 column by column -> change -> iteration 2 -> settled values.
Run: python mice_steps.py  -> mice_steps.mp4, mice_steps.gif, mice_steps_frames.png"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
W, H = 2.3, 0.62
DATA = [["8", "15", "30"], ["NaN", "5", "20"], ["15", "10", "41"], ["12", "NaN", "26"], ["2", "15", "NaN"]]
GAPS = [(1, 0), (3, 1), (4, 2)]                       # (row, column) of the three gaps
MEANS = ["9.25", "11.25", "29.25"]
IT1, CH1 = ["23.14", "11.06", "31.56"], ["+13.89", "-0.19", "+2.31"]
IT2, CH2 = ["23.78", "11.22", "38.87"], ["+0.64", "+0.16", "+7.31"]
ITN, CHN = ["26.72", "13.02", "70.69"], ["0.00", "0.00", "0.00"]
COLS = ["R&D", "Administration", "Marketing"]


def pale(c, t=0.82):
    return ManimColor(c).interpolate(WHITE, t)


def cell(text, colour=BLACK, fill=WHITE, stroke=GREY_C, sw=2, z=0):
    # z keeps texts above boxes, and gap cells above the table, while boxes are recoloured
    box = Rectangle(width=W, height=H, stroke_color=stroke, stroke_width=sw, fill_color=fill, fill_opacity=1)
    return VGroup(box.set_z_index(z), Text(text, font_size=26, color=colour).move_to(box).set_z_index(z + 1))


class MiceSteps(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, line1, line2=""):
        parts = [Text(line1, font_size=30, weight=BOLD)]
        if line2:
            parts.append(Text(line2, font_size=24, color=GREY_C))
        return VGroup(*parts).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)

    def set_gap(self, r, c, text, colour, run_time=0.8):
        new = cell(text, colour, pale(colour), colour, 4, z=2).move_to(self.cells[r][c])
        self.play(FadeTransform(self.gap[(r, c)], new), run_time=run_time)
        self.gap[(r, c)] = new

    def show_changes(self, values, title):
        new = VGroup(Text(title, font_size=24, weight=BOLD),
                     *[Text(f"{COLS[c]}: {v}", font_size=24, color=GREY_C) for (_, c), v in zip(GAPS, values)]
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(self.board, RIGHT, buff=0.6)
        if self.panel is None:
            self.play(FadeIn(new))
        else:
            self.play(Transform(self.panel, new))
            return
        self.panel = new

    def construct(self):
        self.snaps, self.panel = [], None
        self.cells = [VGroup(*[cell(v) for v in row]).arrange(RIGHT, buff=0) for row in DATA]
        table = VGroup(*self.cells).arrange(DOWN, buff=0)
        heads = VGroup(*[Text(h, font_size=24, weight=BOLD).move_to(self.cells[0][j].get_top() + UP * 0.35)
                         for j, h in enumerate(COLS)])
        labels = VGroup(*[Text(f"row {i + 1}", font_size=22, color=GREY_C).next_to(r, LEFT, buff=0.25)
                          for i, r in enumerate(self.cells)])
        self.board = VGroup(table, heads, labels).move_to(LEFT * 2.3 + UP * 0.9)
        self.gap = {}
        for r, c in GAPS:
            self.gap[(r, c)] = cell("NaN", RED_C, pale(RED_C), RED_C, 4, z=2).move_to(self.cells[r][c])

        # Step 0: the gaps, then the column means
        cap = self.caption("Three gaps, one in each column")
        self.play(FadeIn(self.board), *[FadeIn(g) for g in self.gap.values()], FadeIn(cap))
        self.wait(0.6)
        self.play(Transform(cap, self.caption("Step 0: fill each gap with its column mean",
                                              "(8 + 15 + 12 + 2) / 4 = 9.25,  11.25,  29.25")))
        for (r, c), m in zip(GAPS, MEANS):
            self.set_gap(r, c, m, ORANGE_C, 0.6)
        self.wait(0.8)
        self.snap()

        # Iteration 1, column by column
        lines = ["Administration, Marketing", "R&D, Marketing", "R&D, Administration"]
        for (r, c), value, inputs in zip(GAPS, IT1, lines):
            self.play(Transform(cap, self.caption(f"Iteration 1, {COLS[c]}: put the gap back to NaN",
                                                  f"train on the other 4 rows: {COLS[c]} from {inputs}")))
            self.set_gap(r, c, "NaN", RED_C, 0.5)
            train = [row for i, row in enumerate(self.cells) if i != r]
            target = VGroup(*[row[c][0] for row in train])
            inputs_ = VGroup(*[row[k][0] for row in train for k in range(3) if k != c])
            self.play(target.animate.set_fill(pale(GREEN_C, 0.7), 1), inputs_.animate.set_fill(pale(BLUE_C, 0.75), 1))
            self.wait(0.6)
            if c == 0:
                self.snap()
            self.play(Transform(cap, self.caption(f"Linear regression predicts {COLS[c]} for row {r + 1}: {value}",
                                                  "the gap keeps this value for the next columns")), run_time=0.6)
            self.set_gap(r, c, value, GREEN_C, 0.6)
            self.play(target.animate.set_fill(WHITE, 1), inputs_.animate.set_fill(WHITE, 1), run_time=0.4)
        self.play(Transform(cap, self.caption("End of iteration 1: compare with iteration 0",
                                              "large changes, so we run another iteration")))
        self.show_changes(CH1, "change since iteration 0")
        self.wait(1.0)
        self.snap()

        # Iteration 2
        self.play(Transform(cap, self.caption("Iteration 2: same steps, starting from iteration 1's table")))
        for (r, c), v in zip(GAPS, IT2):
            self.set_gap(r, c, v, GREEN_C, 0.5)
        self.show_changes(CH2, "change since iteration 1")
        self.wait(1.0)

        # Settled
        self.play(Transform(cap, self.caption("After about 5 iterations nothing changes any more",
                                              "the changes are 0: stop, the table is filled")))
        for (r, c), v in zip(GAPS, ITN):
            self.set_gap(r, c, v, GREEN_C, 0.5)
        self.show_changes(CHN, "change, iteration 10")
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
                     "output_file": "mice_steps", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = MiceSteps()
        scene.render()
    mp4 = HERE / "mice_steps.mp4"
    shutil.copy(next(media.rglob("mice_steps.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "mice_steps.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "mice_steps_frames.png")
    shutil.rmtree(media)
