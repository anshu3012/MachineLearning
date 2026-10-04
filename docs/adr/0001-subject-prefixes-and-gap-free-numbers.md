# Subject prefixes, chapters and gap-free Note numbers

The flat layout of 270+ Note folders numbered by source (1–134, 210–641, 1001–1084) hid the project's structure and would get worse with the robotics books. We group Notes into Subjects with a prefix (MA, ML, DL, later RO), split large Subjects into Chapters that match the mind maps, and number Notes per Subject with three digits in reading order and no gaps (DL-038). Statistics, probability, calculus and linear algebra share one Subject (MA), because their boundaries blur (likelihood, covariance, expected value) and they play one role: the background the other Subjects build on.

## Consequences

Adding a Note shifts the numbers after it in its Subject. A script rewrites folders, links and tags, but references outside the repo (personal notes, printed PDFs) can go stale, so we renumber only at milestones such as the end of a book. Per-chapter numbers (MA-1.07) were considered and rejected for being less tidy.
