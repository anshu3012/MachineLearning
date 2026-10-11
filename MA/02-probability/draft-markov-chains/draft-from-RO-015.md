# Moved from RO-015 on 2026-10-10: the stationary distribution

From RO-015 (Grid Filters) §2.4 "Moving without looking loses everything": a robot in a 10-cell looped hallway that moves 2 cells (1, 2 or 3 with probability 0.1, 0.8, 0.1) without reading its sensor; its belief flattens towards 0.1 in every cell. Glossary row to restore:

| <span id="G-2463">G-2463</span> | Stationary distribution | The belief that repeated moves without readings settle into and that one more move leaves unchanged, such as 0.1 in every cell of a looped hallway; it shows that prediction alone loses all knowledge. | [Note RO-015](RO/localization/02-bayes-filters/RO-015-grid-filters/RO-015-grid-filters.md#24-moving-without-looking-loses-everything) | Histogram filter |

The belief that repeated moves settle into, and that one more move leaves unchanged, is the **stationary distribution** (G-2463) of the motion (CS188 §8.1). Here it is flat, because the hallway is a loop and every cell looks the same to the motion.
