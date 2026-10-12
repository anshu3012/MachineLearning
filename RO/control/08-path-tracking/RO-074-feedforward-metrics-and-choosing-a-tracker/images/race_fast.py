"""The same race at 5 m/s with steering that follows its command with a lag of 0.4 s (RO-071's steering motor,
Hoffmann et al. 2007), one frame per 0.2 s. Rear-wheel feedback swings the steering back and forth: steering travel
203 deg against 50 (pure pursuit), 55 (Stanley) and 75 (line rule plus the curve's turn). Metrics (RMS / peak):
pure pursuit 0.080 / 0.180 m, Stanley 0.170 / 0.312 m, rear-wheel feedback 0.235 / 0.595 m, line rule plus the
curve's turn 0.203 / 0.414 m.
Run: python race_fast.py -> race_fast.gif, race_fast_frames.png"""
from pathlib import Path

from racedraw import make, race

here = Path(__file__).parent
runs, sc = race(5.0, tau=0.4)
want = [(0.080, 0.180, 49.6), (0.170, 0.312, 55.1), (0.235, 0.595, 202.6), (0.203, 0.414, 74.8)]
for m, (r, p, t) in zip(sc, want):
    assert abs(m["rms"] - r) < 5e-4 and abs(m["peak"] - p) < 5e-4 and abs(m["travel"] - t) < 0.05, m
make(runs, sc, here / "race_fast", "the same at 5 m/s, steering lagging 0.4 s", [-0.7, 0.7], [-27, 27], every=0.2)
