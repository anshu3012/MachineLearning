"""The four trackers raced on the chapter's car at 2 m/s, every car starting on the line, one frame per 0.5 s. Top: the
course and the cars (front wheel drawn at its steering angle). Middle: lateral error at the rear axle. Bottom: steering
angle. The last frame fills the legend with the metrics: RMS lateral error, peak lateral error and steering travel.
Pure pursuit 0.086 / 0.167 m / 30 deg; Stanley 0.189 / 0.316 m / 29 deg (its front axle holds the line, its rear axle
runs inside the arc); rear-wheel feedback 0.002 / 0.007 m / 34 deg; RO-070's line rule plus the curve's turn
0.003 / 0.007 m / 33 deg.
Run: python race.py -> race.gif, race_frames.png"""
from pathlib import Path

import numpy as np

from racedraw import make, race

here = Path(__file__).parent
runs, sc = race(2.0)
want = [(0.086, 0.167, 30.1), (0.189, 0.316, 28.8), (0.002, 0.007, 33.8), (0.003, 0.007, 33.5)]
for m, (r, p, t) in zip(sc, want):
    assert abs(m["rms"] - r) < 5e-4 and abs(m["peak"] - p) < 5e-4 and abs(m["travel"] - t) < 0.05, m
make(runs, sc, here / "race", "four trackers on the chapter's car at 2 m/s, from on the line", [-0.4, 0.45], [-2, 20])
