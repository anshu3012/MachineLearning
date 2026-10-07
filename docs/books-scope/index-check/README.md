# Index check: is the robotics plan complete?

This folder holds the evidence that [robotics.md](../robotics.md) is complete against standard sources. Every term in each source got a written verdict:

| Verdict | Meaning |
|---|---|
| taught | The cited Note lists the concept in its own title or "Teaches" column. A nearby topic does not count. |
| add | Missing. The verdict says where it goes. |
| out-of-scope | Left out, with a reason that can be checked: research-only, a different field, proof vocabulary and the like. |
| index-noise | Names, symbols and pointers. |

**How to look up a term:** search the ledgers, for example `grep -i "laplacian" *.md`.

## Ledgers

| File | Sources |
|---|---|
| robo_ledger.md | Lynch & Park, *Modern Robotics*; LaValle, *Planning Algorithms*; Correll et al., *Introduction to Autonomous Robots* |
| ctrl_ledger.md | Åström & Murray, *Feedback Systems*; Bullo, *Lectures on Network Systems*; Deisenroth et al., *Mathematics for ML* |
| vis_ledger.md | Barfoot, *State Estimation for Robotics*; Szeliski, *Computer Vision* (2010); Prince, *Computer Vision: Models, Learning, and Inference* |
| dec_ledger.md | Sutton & Barto; Kochenderfer et al., *Algorithms for Decision Making*; Kochenderfer & Wheeler, *Algorithms for Optimization* |
| adv_ledger.md | Rawlings, Mayne & Diehl, *Model Predictive Control*; Murray, Li & Sastry (contents); Tedrake, *Underactuated Robotics* (contents) |
| uniA_ledger.md | 12 university courses: mobile robotics, estimation, planning |
| uniB_ledger.md | 12 university courses: control, arms, vision, robot learning |
| yt_ledger.md | 14 official lecture playlists |
| web_ledger.md | Online outlines and glossaries: robotics, control, computer vision, ML |

Each ledger gives the source URL of every book, course and playlist it used.

**Note numbers in the ledgers** ("N117", "RO 235") refer to the 359-Note draft the check was run against, not to today's numbering. The concept names still match.

## Checks on the verdicts

- **verify_flags.md.** A script tested every "taught" verdict against the cited Note's concept list. This file holds the 774 that failed, each judged by hand.
- **merged_adds.md.** All adds merged into unique concepts, each checked against the existing MA/ML/DL Notes. 224 concepts are placed in the plan; in robotics.md their rows read `idx:<concept>`.

## Totals

13,470 terms: 5,696 taught, 1,698 add, 4,163 out of scope, 1,896 noise, 17 mentioned only.

## Limit

This proves completeness against these sources only. A topic none of them teaches can still be missing. To widen the check, add a book or course and judge its terms the same way.
