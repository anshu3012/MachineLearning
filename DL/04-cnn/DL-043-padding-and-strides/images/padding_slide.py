"""A 3x3 filter slides over a 5x5 image with one ring of zero padding: the feature map stays 5x5.
Run: python padding_slide.py -> padding_slide.gif, padding_slide_frames.png"""
from pathlib import Path
import numpy as np
from anim import animate

X = np.array([[3, 0, 1, 2, 7], [1, 5, 8, 9, 3], [2, 7, 2, 5, 1], [0, 1, 3, 1, 7], [4, 2, 1, 6, 2]])
K = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
Z = animate("padding_slide", X, 3, kernel=K, pad=1, here=Path(__file__).parent, keys=(0, 1, 12, -1), fps=2.5, height=560)
assert Z.shape == (5, 5)
