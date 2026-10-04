"""A 3x3 filter slides over a 7x7 image with stride 2: it jumps 2 pixels each time and the feature map is 3x3.
Run: python stride_slide.py -> stride_slide.gif, stride_slide_frames.png"""
from pathlib import Path
import numpy as np
from anim import animate

rng = np.random.default_rng(3)
X = rng.integers(0, 10, size=(7, 7))
K = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
Z = animate("stride_slide", X, 3, kernel=K, stride=2, here=Path(__file__).parent, keys=(0, 1, 3, -1), height=560)
assert Z.shape == (3, 3)
