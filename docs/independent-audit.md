# Task: independent read-only audit of randomly chosen Notes

You are a fresh reviewer. Change nothing. Read `docs/NOTE-RULES.md` in full first. Then read each Note on your list in full, as a beginner with ADHD reading on a phone, one line at a time, who has never seen the topic.

For every line ask:
- Do I already know everything this line uses (each word, symbol, picture, idea)? If not, was it shown earlier in this Note or one tap away through a link to the exact section that explains it?
- Is anything here false, or easy to read as false (wrong word for the object, a label sitting on the wrong thing, a shape or count that does not match, a hidden condition)?
- Is any calculation inside a sentence, or a step skipped?
- Does each figure say what kind of picture it is, what each axis, colour and mark means, and what to look at? Open the image (`images/<name>.png`, or `<name>_frames.png` for a GIF) and check the text matches it.
- Does each abstract statement have a concrete example right there?
- Is a technical term used without its plain meaning at its first use in this section?
- Does any link point at a whole Note instead of a section, or say "the X Note"? (Ignore the generated "Where this fits" block at the top.)
- Anything else that would stop a beginner, even if no rule names it.

Report findings as a table: Note | line | kind | what is wrong | suggested fix. Group them by kind at the end with counts, and name any **new kind of problem** that the rules do not cover yet. Be strict; report everything you find, and nothing you did not verify.
