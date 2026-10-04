"""A 3x3 horizontal-edge filter slides over a 6x6 image (black top, white bottom) and fills the 4x4 feature map.
Run: python conv_slide.py -> conv_slide.gif, conv_slide_frames.png"""
from pathlib import Path
import numpy as np
from anim import animate

X = np.vstack([np.zeros((3, 6)), np.full((3, 6), 255)])
K = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
Z = animate("conv_slide", X, 3, kernel=K, here=Path(__file__).parent, keys=(0, 4, 8, -1))
assert (Z == np.array([[0] * 4, [765] * 4, [765] * 4, [0] * 4])).all()
