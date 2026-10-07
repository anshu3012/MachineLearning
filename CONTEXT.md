# CampusX ML Study Notes

Ground-zero study notes for the CampusX "100 Days of Machine Learning" playlist, written for a visual learner with no prior ML or Python knowledge.

## Language

**Source**:
Material a Note is built from: a playlist video (with its subtitles), a book chapter or section, or a paper. A Note may draw on several Sources and lists them in its Sources section.
_Avoid_: Video (as the unit of the project), lecture, episode

**Note**:
One lesson on one main idea, built from one or more Sources and complete enough to learn from without them. Identified by its Note number (e.g. Note ML-037).
_Avoid_: Chapter, page, summary

**Subject**:
One of the top-level parts of the project, each with a two-letter prefix: MA (Mathematical foundations: linear algebra, calculus, optimisation, probability, statistics), ML (Machine learning), DL (Deep learning) and, later, RO (Robotics).
_Avoid_: Playlist, course, section

**Chapter**:
A group of Notes inside a Subject that is read in order and matches one mind map (e.g. DL chapter "optimizers").
_Avoid_: Module, unit, part

**Note number**:
A Note's Subject prefix and its position in that Subject, three digits, in reading order with no gaps (e.g. DL-038). Numbers run on across Chapters and are reassigned by script when Notes are added.
_Avoid_: Video number, ID

**Teacher's flow**:
The order, examples and analogies the teacher uses in a video Source, taken from its subtitles. Shapes a Note's sections but is never named or narrated in it.
_Avoid_: Script, outline

**Extra box**:
A clearly marked section in a Note with material the teacher did not cover (formulas, common mistakes, deeper intuition).
_Avoid_: Bonus, aside

**Key point**:
A one-line box opening every section of a Note, stating the section's main idea before it is explained.
_Avoid_: TL;DR, summary box

**Key terms**:
The closing list of a Note, generated from the glossary: the terms whose Home is this Note, then the terms it only recaps, each linking to its Home.
_Avoid_: Vocabulary, definitions

**Notebook**:
A Jupyter notebook that goes with a Note, holding interactive demos and the Source's code rebuilt by us for current library versions. Never a copy of the teacher's notebook.
_Avoid_: Code file, script, lab

**Course map**:
The one overview that ties all Notes together. It has four views: the Pipeline map, the Concept map, the Learning path and the Algorithm chooser. It lives in `00-course-map/`, outside the Subjects.
_Avoid_: Index, syllabus, roadmap, architecture

**Pipeline map**:
The Course map view that places every topic at its step in an ML project (14 steps, from Foundations and Frame the problem to Test and Monitor and maintain).
_Avoid_: Workflow diagram, lifecycle

**Concept map**:
The Course map view showing how ideas relate across Notes (e.g. overfitting is fixed by regularisation).
_Avoid_: Mind map, knowledge graph

**Learning path**:
The Course map view showing which Notes must be read before which, as one Course order.
_Avoid_: Prerequisite graph, curriculum

**Note order**:
The order of Notes inside a Subject, given by Note number. Subjects are organised MA, then ML, then DL. Keeps the folders tidy; it is not the order a reader must follow.
_Avoid_: Reading order (ambiguous)

**Course order**:
The one order a reader follows through the whole course, shown in the site's sidebar and on the Learning path, and recorded as its Stages in one file (agreed by review, 2026-10-07). ML and DL keep their Note order; each maths topic comes, whole, just before the first Note that needs it. Every Note comes after all the Notes it builds on. "Earlier" always means earlier in the Course order.
_Avoid_: Syllabus, sequence

**Home**:
The one section of one Note that teaches a Concept or a Glossary term. Every other Note that uses it recaps briefly and links to the Home.
_Avoid_: Owner, first Note, "first explained"

**Glossary term**:
A word or symbol with a one-line meaning in the glossary. Has its own Home and belongs to exactly one Concept (e.g. "learning rate" belongs to "gradient descent"); a term with no natural Concept belongs to the main Concept of its Home Note.
_Avoid_: Keyword, definition

**Builds on**:
The Notes whose ideas a Note needs directly and that come earlier in the Course order; the same list as the Note's prerequisites. Direct only: their own prerequisites are not repeated.
_Avoid_: Depends on, requires

**Leads to**:
The exact reverse of Builds on: Note A leads to Note B when B builds on A.
_Avoid_: Next, see also

**Preview**:
An idea a Note uses before its Home in the same Subject (Note numbers follow the CampusX order and are not changed for it). The Note explains it in one plain sentence where used and links to the Home; the Where this fits box lists it as "Used here, taught in full later".
_Avoid_: Forward reference, spoiler

**Concept**:
One idea on the Course map (e.g. overfitting, Naive Bayes). Has exactly one Home; other Notes may use it. One Note can be the Home of several Concepts.
_Avoid_: Topic, node, idea

**Link**:
A labelled connection between two Concepts. Exactly five kinds: *needs*, *is a kind of*, *fixes*, *compared with*, *used in*.
_Avoid_: Edge, relation, dependency

**Where this fits**:
The box at the start of every Note showing its place on the Pipeline map, the Notes it builds on, and the Notes it leads to.
_Avoid_: Context box, breadcrumbs

**Algorithm chooser**:
The Course map view that leads from a problem's properties to suitable algorithms.
_Avoid_: Cheat sheet, decision tree (that name belongs to the algorithm)

**Python box**:
A clearly marked section teaching just the Python needed at that point in the playlist, for a reader with no Python.
_Avoid_: Python primer, prerequisite

**Stage**:
A short run of consecutive Notes in the Course order (10 to 20), named for what it covers, used to show the Course order on the Learning path.
_Avoid_: Phase, level
