# Task: map ML and DL Notes to their teaching path and best visual sources

The user is a beginner with ADHD: "the whole project depends on animations and figures" and "what's also important is the images, videos, animations etc they used and the intuition they build. Like I said this is for a beginner." Rule NOTE-RULES §12: every fix applies to every Note. This map is the input for later rewrite agents. It is a research document: change no Note.

## Per Note in your range, write a block `### <number> <title>` with:
1. **Sources**, in priority order:
   - the Note's own CampusX video: ML transcripts in `transcripts/NNN.*.txt` (titles and IDs in `transcripts/playlist.txt`); DL transcripts in `dl_map/transcripts/` (IDs in `dl_map/playlist.txt`);
   - StatQuest, 3Blue1Brown and Khan Academy videos on the same concept. Search with the newer yt-dlp: `/home/anshu/miniforge3/bin/python3 -m yt_dlp "ytsearch5:StatQuest <topic>" --flat-playlist --print "%(id)s %(title)s %(duration)s"`.
   - For each one you use, fetch the English captions (`--skip-download --write-auto-subs --sub-langs en --sub-format vtt`) into `transcripts/teaching-video/<number>-<channel>-<slug>.vtt`, plus a `.txt` with one line per about 30 s, `[mm:ss] text`. Never download video or audio, never use cookies.
   - Confirm each video's ID, title, channel and length with yt-dlp. List only videos you opened.
2. **Teaching path:** the order of beats that teaches the idea best to a beginner, from the clearest source. For each beat: timestamp, the analogy or worked example with its exact numbers, and every visual (what is drawn or animated, and why it makes the idea click).
3. **What the Note lacks** compared with the path: missing beats, missing visuals, wrong order, a term used before it is explained.
4. **Animation ideas:** 1–4 concrete animations, each with a tool (Manim for geometry and vectors, Plotly frames for data and curves) and the data to use (the Note's own data where possible).
5. **CampusX vs the others (NOTE-RULES §13):** per concept, which explanation is clearer for a beginner and why; any angle CampusX adds that the others lack (or the reverse); any clash between them, with which is right and the evidence.
6. **Contradictions:** a video and the Note disagree. Say which is right, with the evidence.

Check every beat against the transcript text; never write from memory.

## Output
- Write to `docs/teaching-paths/<your range>.md`. If writing under `docs/` is blocked, write to `/home/anshu/.claude/jobs/8c1c0992/tmp/` and say so.
- Start the file with a summary: coverage, the top 10 animation ideas, and the contradictions.
- Touch no Note, glossary, course map, tool or git. Start no background agents.
- Report as text: the file path, coverage, the Notes that have no outside video, and the worst gaps.
