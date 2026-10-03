"""Made-up flat data shared by the figures and the Notebook (no output when run)."""
import numpy as np

rng = np.random.default_rng(7)
N = 30
rooms = rng.uniform(1, 5, N)                                  # number of rooms (continuous for a clear picture)
shops = 3 + rng.normal(0, 0.35, N)                            # grocery shops nearby: hardly varies
washrooms = 0.8 * rooms + rng.normal(0, 0.35, N) + 0.4        # washrooms: rise with rooms
washrooms = washrooms * rooms.std() / washrooms.std()         # same spread as rooms, so selection cannot choose
washrooms += 3 - washrooms.mean()
