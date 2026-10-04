"""Reading a file in chunks: only one chunk is in memory at a time.
Run: python chunks.py  -> chunks.mp4, chunks.gif, chunks_frames.png"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
SIZES = [300, 300, 300, 100]
UNIT = 5.2 / 1000          # height of one row on screen


def block(rows, colour):
    light = ManimColor(colour).interpolate(WHITE, 0.8)
    rect = Rectangle(width=2.4, height=rows * UNIT, stroke_color=colour, stroke_width=2,
                     fill_color=light, fill_opacity=1)
    return VGroup(rect, Text(f"{rows} rows", font_size=24).move_to(rect))


class Chunks(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, text):
        return Text(text, font_size=28).to_edge(DOWN, buff=0.45)

    def construct(self):
        self.snaps = []
        # the file on disk: 1,000 rows, cut into chunks of 300
        blocks = VGroup(*[block(n, BLUE_C) for n in SIZES]).arrange(DOWN, buff=0.06).move_to(LEFT * 4 + UP * 0.25)
        file_label = Text("file on disk: 1,000 rows", font_size=26, color=GREY_C).next_to(blocks, UP, buff=0.25)
        # memory: room for one chunk only
        memory = Rectangle(width=3.0, height=300 * UNIT + 0.5, stroke_color=GREEN_C, stroke_width=3).move_to(UP * 0.25)
        mem_label = Text("memory (RAM)", font_size=26, color=GREEN_C).next_to(memory, UP, buff=0.25)
        total_label = Text("rows counted so far", font_size=26, color=GREY_C).move_to(RIGHT * 4.3 + UP * 1.2)
        total = Text("0", font_size=60, weight=BOLD).next_to(total_label, DOWN, buff=0.4)
        cap = self.caption("chunksize=300 cuts the file into 4 chunks")
        self.play(FadeIn(*blocks, file_label, memory, mem_label, total_label, total, cap))
        self.wait(0.5)

        done = 0
        for i, n in enumerate(SIZES):
            chunk = blocks[i]
            # load one chunk into memory
            chunk[0].set_stroke(ORANGE_C)
            self.play(chunk.animate.move_to(memory),
                      Transform(cap, self.caption(f"chunk {i + 1} of 4: only these {n} rows are in memory")),
                      run_time=1.0)
            # process it: add its rows to the running total
            done += n
            self.play(Transform(total, Text(f"{done:,}", font_size=60, weight=BOLD).move_to(total)), run_time=0.6)
            self.wait(0.4)
            self.snap()
            # free the memory before the next chunk
            self.play(FadeOut(chunk), run_time=0.5)

        self.play(Transform(cap, self.caption("all 1,000 rows processed, never more than 300 at once")))
        self.wait(1.5)


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "chunks", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = Chunks()
        scene.render()
    mp4 = HERE / "chunks.mp4"
    shutil.copy(next(media.rglob("chunks.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "chunks.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "chunks_frames.png")
    shutil.rmtree(media)
