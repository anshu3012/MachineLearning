"""Run: python3 site/test_glossary_terms.py  (checks the boxes link to the recorded Home sections)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glossary_terms as g
repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
e = g.load(repo)
assert e["G-1469"][2][:3:2] == ("ML-046-pca-geometric-intuition", "1-what-pca-is"), e["G-1469"][2]
assert e["G-596"][2][0].startswith("MA-004"), e["G-596"][2]
assert e["G-172"][2][2] == "52-add-and-norm", e["G-172"][2]
print("ok")
# a Note link gets the glossary meaning of the term its text names in that Note, and links its own section
ctx = dict(entries=e, notes=g.notes(repo), homes={}, by_note={})
for c, (_, _, (n, _, a, _, _)) in e.items():
    ctx["homes"].setdefault((n, a or ""), []).append(c)
    ctx["by_note"].setdefault(n, []).append(c)
b = g.link_box("particle filter", "RO-016-particle-filter#46-the-algorithm", "RO-016-particle-filter", "46-the-algorithm", ctx)
assert b.startswith('<span class="gloss-def" data-link hidden>**Particle filter:**'), b
assert b.endswith("Explained in: [Particle Filter, §4.6 The algorithm](RO-016-particle-filter#46-the-algorithm)</span>"), b
text, boxes = g.add_link_boxes("the [belief](RO-013-belief#42-the-definition) (G-2433) and [door world](RO-014-bayes-filter)", ctx)
assert text.count("\x01") == 2 and len(boxes) == 1 and "The Bayes Filter" in boxes[0], (text, boxes)
print("links ok")
