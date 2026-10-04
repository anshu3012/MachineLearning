"""The loop visits one company box at a time and turns it into one table row.
Run: python container_loop.py  -> container_loop.mp4, container_loop.gif, container_loop_frames.png"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
# real values from page 1 of the saved list (August 2022)
COMPANIES = [("TCS", "3.9", "44.9k", "Public"),
             ("Accenture", "4.2", "30.3k", "Public"),
             ("Cognizant", "4.0", "27.4k", "Private")]
COLS = ["name", "rating", "reviews", "type"]
COL_W = [2.0, 1.2, 1.4, 1.4]


def company_box(values):
    """A card like the web page's: name on top, then the details."""
    name, rating, reviews, ctype = values
    lines = VGroup(Text(name, font_size=26, weight=BOLD),
                   Text(f"{rating}   ({reviews} Reviews)", font_size=20),
                   Text(f"{ctype}  ...", font_size=20)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    frame = RoundedRectangle(corner_radius=0.12, width=3.6, height=1.45, stroke_color=GREY_C, stroke_width=2)
    lines.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.25)
    return VGroup(frame, lines)


def cell(text, width, bold=False, fill=WHITE):
    rect = Rectangle(width=width, height=0.55, stroke_color=GREY_C, stroke_width=1.5,
                     fill_color=fill, fill_opacity=1)
    return VGroup(rect, Text(text, font_size=22, weight=BOLD if bold else NORMAL).move_to(rect))


def table_row(texts, y, bold=False, fill=WHITE):
    row, x = VGroup(), 0.0
    for t, w in zip(texts, COL_W):
        c = cell(t, w, bold, fill)
        c.move_to([x + w / 2, y, 0])
        row.add(c)
        x += w
    return row


class ContainerLoop(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, text):
        return Text(text, font_size=28).to_edge(DOWN, buff=0.4)

    def construct(self):
        self.snaps = []
        boxes = VGroup(*[company_box(v) for v in COMPANIES]).arrange(DOWN, buff=0.3).move_to(LEFT * 4.3 + UP * 0.35)
        page_label = Text("company boxes on the page", font_size=24, color=GREY_C).next_to(boxes, UP, buff=0.25)
        header = table_row(COLS, 0, bold=True, fill=ManimColor(BLUE_C).interpolate(WHITE, 0.75))
        table = VGroup(header).move_to(RIGHT * 2.6 + UP * 1.9)
        df_label = Text("DataFrame", font_size=24, color=BLUE_C).next_to(table, UP, buff=0.25)
        cap = self.caption("company = soup.find_all('div', class_='company-content-wrapper')")
        self.play(FadeIn(boxes, page_label, table, df_label, cap))
        self.wait(0.6)

        for k, values in enumerate(COMPANIES):
            box = boxes[k]
            # the loop variable i is this one box: search only inside it
            self.play(box[0].animate.set_stroke(ORANGE_C, width=5),
                      Transform(cap, self.caption(f"for i in company:   box {k + 1} of 30")), run_time=0.6)
            row = table_row(values, 0).next_to(table, DOWN, buff=0)
            sources = [box[1][0], box[1][1], box[1][1], box[1][2]]
            self.play(*[TransformFromCopy(src, cl) for src, cl in zip(sources, row)], run_time=1.1)
            table.add(row)
            self.wait(0.3)
            self.snap()
            self.play(box[0].animate.set_stroke(GREEN_C, width=3), run_time=0.3)

        dots = Text("...", font_size=36).next_to(table, DOWN, buff=0.15)
        self.play(FadeIn(dots), Transform(cap, self.caption("30 boxes on the page  =  30 rows in the table")))
        self.wait(0.8)
        self.snap()
        self.wait(1.0)


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "container_loop", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = ContainerLoop()
        scene.render()
    mp4 = HERE / "container_loop.mp4"
    shutil.copy(next(media.rglob("container_loop.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "container_loop.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "container_loop_frames.png")
    shutil.rmtree(media)
