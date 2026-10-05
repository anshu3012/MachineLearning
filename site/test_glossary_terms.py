"""Run: python3 site/test_glossary_terms.py  (checks the box links follow a Note's own pointer to the teaching Note)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glossary_terms as g
repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
e = g.load(repo)
assert e["G-1469"][2][:3:2] == ("ML-046-pca-geometric-intuition", "1-what-pca-is"), e["G-1469"][2]   # ML-003 only points to it
assert e["G-596"][2][0].startswith("MA-004"), e["G-596"][2]          # its own section teaches it; the "see" is an example
assert e["G-172"][2][2] == "52-add-and-norm", e["G-172"][2]
print("ok")
