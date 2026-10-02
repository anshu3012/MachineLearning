"""Reinforcement learning in one picture: try, get punished, update the policy, get rewarded.
Run: python rl_fire_water.py  -> rl_fire_water.mp4, rl_fire_water.gif, rl_fire_water_frames.png"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")


class FireWater(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        floor = Line(LEFT * 6, RIGHT * 6, color=GREY_C, stroke_width=4).shift(DOWN * 1.75)
        fire = VGroup(Triangle(color=RED_C, fill_color=ORANGE_C, fill_opacity=1).scale(0.7),
                      Text("Fire", font_size=30, weight=BOLD)).arrange(DOWN, buff=0.25).move_to([-4.8, -0.5, 0])
        water = VGroup(Circle(0.6, color=BLUE_C, fill_color=BLUE_C, fill_opacity=0.6),
                       Text("Water", font_size=30, weight=BOLD)).arrange(DOWN, buff=0.25).move_to([4.8, -0.5, 0])
        agent = VGroup(Circle(0.62, color=RED_C, fill_color=RED_C, fill_opacity=0.25, stroke_width=5),
                       Text("Agent", font_size=28, weight=BOLD)).move_to([0, -0.5, 0])
        agent[1].move_to(agent[0])
        policy_box = RoundedRectangle(width=6.4, height=1.0, corner_radius=0.15, color=GREY_C).move_to([0, 2.6, 0])
        policy = Text("Policy: go to the fire", font_size=30).move_to(policy_box)
        self.play(Create(floor), FadeIn(fire), FadeIn(water), FadeIn(agent), Create(policy_box), Write(policy))
        self.wait(0.5)
        self.snap()

        # Try 1: follows the policy, gets punished
        self.play(agent.animate.move_to([-3.4, -0.5, 0]), run_time=1.2)
        punish = Text("-10  punishment", font_size=34, color=RED_C, weight=BOLD).move_to([-3.4, 0.8, 0])
        self.play(FadeIn(punish, shift=UP * 0.3), agent[0].animate.set_fill(RED_C, 0.7))
        self.wait(0.6)
        self.snap()

        # Update the policy
        new_policy = Text("Policy: go to the water", font_size=30, color=GREEN_C).move_to(policy_box)
        self.play(FadeOut(punish), Transform(policy, new_policy), policy_box.animate.set_color(GREEN_C),
                  agent[0].animate.set_fill(RED_C, 0.25))
        self.play(agent.animate.move_to([0, -0.5, 0]), run_time=0.8)
        self.wait(0.4)
        self.snap()

        # Try 2: follows the new policy, gets rewarded
        self.play(agent.animate.move_to([3.4, -0.5, 0]), run_time=1.2)
        reward = Text("+10  reward", font_size=34, color=GREEN_C, weight=BOLD).move_to([3.4, 0.8, 0])
        self.play(FadeIn(reward, shift=UP * 0.3))
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
                     "output_file": "rl_fire_water", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = FireWater()
        scene.render()
    mp4 = HERE / "rl_fire_water.mp4"
    shutil.copy(next(media.rglob("rl_fire_water.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "rl_fire_water.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "rl_fire_water_frames.png")
    shutil.rmtree(media)
