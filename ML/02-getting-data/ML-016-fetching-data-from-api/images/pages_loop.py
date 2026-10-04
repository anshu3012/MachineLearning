"""Fetching page after page and joining the pages into one DataFrame.
Run: python pages_loop.py  -> pages_loop.mp4, pages_loop.gif, pages_loop_frames.png"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
ROWS = [240, 245, 242, 243, 238]   # shows on pages 0-4 of api.tvmaze.com/shows (October 2026)


def light(colour):
    return ManimColor(colour).interpolate(WHITE, 0.82)


def block(page, rows, start, colour):
    rect = Rectangle(width=5.6, height=0.72, stroke_color=colour, stroke_width=2,
                     fill_color=light(colour), fill_opacity=1)
    label = Text(f"page {page}: {rows} rows, index {start}-{start + rows - 1}", font_size=24).move_to(rect)
    return VGroup(rect, label)


class PagesLoop(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, text):
        return Text(text, font_size=28).to_edge(DOWN, buff=0.4)

    def construct(self):
        self.snaps = []
        server = VGroup(RoundedRectangle(corner_radius=0.15, width=2.6, height=1.3, stroke_color=PURPLE_C,
                                         fill_color=light(PURPLE_C), fill_opacity=1),
                        Text("TVmaze API", font_size=28)).move_to(LEFT * 5.2 + UP * 1.0)
        server[1].move_to(server[0])
        title = Text("frames (a list of DataFrames)", font_size=26, color=GREY_C).move_to(RIGHT * 0.9 + UP * 3.3)
        counter_label = Text("rows so far", font_size=26, color=GREY_C).move_to(RIGHT * 5.4 + UP * 1.6)
        counter = Text("0", font_size=56, weight=BOLD).next_to(counter_label, DOWN, buff=0.3)
        cap = self.caption("for page in range(0, 5): fetch, convert, append")
        self.play(FadeIn(server, title, counter_label, counter, cap))

        blocks, total = [], 0
        for page, rows in enumerate(ROWS):
            b = block(page, rows, 0, BLUE_C).move_to(server)
            b.scale(0.4)
            target = RIGHT * 0.9 + UP * (2.6 - 0.85 * page)
            self.play(FadeIn(b), Transform(cap, self.caption(f"page {page}: requests.get, then a DataFrame of {rows} rows")),
                      run_time=0.5)
            self.play(b.animate.scale(2.5).move_to(target), run_time=0.8)
            total += rows
            self.play(Transform(counter, Text(f"{total:,}", font_size=56, weight=BOLD).move_to(counter)),
                      run_time=0.4)
            blocks.append(b)
            if page in (0, 2, 4):
                self.wait(0.4)
                self.snap()

        # join: ignore_index=True gives every row a new number, counting on from the page above
        self.play(Transform(cap, self.caption("every page starts at index 0: labels repeat")), run_time=0.6)
        self.wait(0.8)
        new, start = [], 0
        for page, (b, rows) in enumerate(zip(blocks, ROWS)):
            new.append(block(page, rows, start, GREEN_C).move_to(b))
            start += rows
        self.play(*[Transform(b, n) for b, n in zip(blocks, new)],
                  Transform(title, Text("df (one DataFrame)", font_size=26, color=GREEN_C).move_to(title)),
                  Transform(cap, self.caption("pd.concat(frames, ignore_index=True): one table, index 0-1207")),
                  run_time=1.2)
        self.wait(0.6)
        self.snap()
        self.wait(1.2)


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "pages_loop", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = PagesLoop()
        scene.render()
    mp4 = HERE / "pages_loop.mp4"
    shutil.copy(next(media.rglob("pages_loop.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "pages_loop.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "pages_loop_frames.png")
    shutil.rmtree(media)
