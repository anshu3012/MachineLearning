# Recorded Homes and a generated Course order

Every Concept and every Glossary term now has one recorded Home (a Note and a section) in the data files, and the Course order is generated from Builds on. Until now the teaching Note was guessed three different ways (first Note in a mention list, a Note-name match, and a text search behind the glossary), and the guesses disagreed on about 50 Concepts; boxes pointed at overview Notes, Builds on pointed forward, and the site's glossary boxes said "Explained in this Note" in Notes that only mention a term. Recording the Home once and deriving everything (Where this fits, Course map, glossary links, Key terms tables, tags, prerequisites, chapter pages) from it removes the disagreement at the source.

Folders and Note numbers keep the Subject order MA, ML, DL and the CampusX video order; the reader's path is the separate, generated Course order, which places each Note right after the last Note it builds on. A Note that needs a later Note of its own Subject is not renumbered: it carries a Preview (one plain sentence and a link to the Home).

## Consequences

Homes for 335 Concepts and 2,138 terms must be filled once (agents propose, a script rejects Homes whose section does not exist, does not mention the term, or only points elsewhere). A structure check runs on every build and fails on a forward Builds on, a missing Home, Leads to that is not the reverse of Builds on, prerequisites that differ from the box, or a Preview without its sentence. The hand-drawn mind maps stay hand-drawn and are checked against the Homes.
