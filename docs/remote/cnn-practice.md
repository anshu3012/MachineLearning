# Task: write DL Notes 1049–1054 (CNN in practice)

You are working in `~/campusx` on the machine topgro. It holds a copy of a study-Notes project: beginner ML, maths and DL Notes, one folder per Note. Another machine owns the git repository. **Do not run git, and do not push anything.** Your finished folders will be copied back and reviewed there.

Write six Notes from Videos 49–54 of the "100 Days of Deep Learning" playlist (titles in `dl_map/playlist.txt`):

| Note | Video | Topic |
|---|---|---|
| 1049 | 49 | cat vs dog image classification project |
| 1050 | 50 | data augmentation |
| 1051 | 51 | pretrained models, ImageNet / ILSVRC, Keras code |
| 1052 | 52 | what a CNN sees: visualising filters and feature maps |
| 1053 | 53 | transfer learning: feature extraction vs fine-tuning |
| 1054 | 54 | the Keras functional API for non-linear networks |

Name the folders `1049-cat-vs-dog-cnn`, `1050-data-augmentation`, `1051-pretrained-models`, `1052-visualizing-cnn`, `1053-transfer-learning` and `1054-keras-functional-api`.

## Read first
1. `docs/NOTE-RULES.md`: every rule the user set (style, evidence, experiments, presentation, the house rules). Follow it exactly.
2. `docs/STYLE-naming.md`.
3. Style models: `1031-batch-normalization/note.md`, `1055-why-rnn/note.md` and `1067-history-of-llms/note.md`. Copy their structure:
   - title front matter;
   - Overview with a Key point box;
   - Prerequisites as bullets that start with the link;
   - numbered sections, each opening with a Key point box;
   - "In words / Formula / Example";
   - Extra boxes;
   - Python boxes;
   - Summary;
   - `## N. Sources`;
   - `## N. Key terms` table.

## Sources
- **Transcripts:** `transcripts/D049.whisper-en.txt` … `D054.whisper-en.txt`. Hindi originals are in `dl_map/transcripts/0NN.hi-orig.txt`.
- **Books and papers** (download arXiv PDFs with curl and check the text):
  - Goodfellow et al., *Deep Learning*, ch. 9 and §7.4 (augmentation);
  - Chollet, *Deep Learning with Python*, 2nd ed., ch. 8–9;
  - Russakovsky et al. 2015 (ILSVRC);
  - Krizhevsky et al. 2012 (AlexNet);
  - Simonyan and Zisserman 2015 (VGG);
  - He et al. 2016 (ResNet);
  - Zeiler and Fergus 2014 (visualising CNNs);
  - Yosinski et al. 2014 (how transferable are features);
  - Shorten and Khoshgoftaar 2019 (augmentation survey);
  - the Keras docs.

## Links
- **Already written:** `1002-what-is-deep-learning` (§5.4, transfer learning in general), `1067-history-of-llms` (transfer learning in NLP), `1024-dropout`, `1026-regularization-in-dl`, `1031-batch-normalization`, `1011-customer-churn-ann` (Keras basics), `1022-early-stopping`.
- **Being written right now on another machine: the CNN theory Notes 1040–1048.** Their folders already exist with these names (the text may still be changing), so link to them:
  - `../1040-cnn-intuition/note.md`
  - `../1042-convolution-operation/note.md`
  - `../1043-padding-and-strides/note.md`
  - `../1044-pooling/note.md`
  - `../1045-lenet-5/note.md`

  List every placeholder in your report. Do not re-teach convolution or pooling; a one-line recap with a link is enough.

## Data and compute
- This machine has an RTX 4060 GPU with 8 GB. Use it: `TF_FORCE_GPU_ALLOW_GROWTH=true`.
- Python: `~/miniforge3/envs/campusx/bin/python`, with `PYTHONNOUSERSITE=1`.
- Real data: the Kaggle/Microsoft cats-vs-dogs images via `tensorflow_datasets` ("cats_vs_dogs"), or `keras.utils.image_dataset_from_directory` on the Microsoft download. Use ImageNet weights from `keras.applications`.
- Keep `data/` under about 1 MB per Note. Never commit images of the dataset; save only small CSVs of results and a few example thumbnails.
- Notebooks must run end to end, seeded:
  `PYTHONNOUSERSITE=1 ~/miniforge3/envs/campusx/bin/python -m nbconvert --to notebook --execute --output-dir .logs --output notebook notebook.ipynb`
- Store the notebook without outputs; the executed copy goes in `.logs/`.
- Build each Note with `CAMPUSX_ENV=~/miniforge3/envs/campusx tools/build.sh <folder>`, which must print "Built". If LaTeX is missing a package, say so in your report instead of working around it.

## Experiments must show each principle on real data
For example:
- **1049:** a small CNN overfits cats vs dogs (training accuracy rises while validation stalls).
- **1050:** augmentation closes that gap.
- **1051:** a pretrained ResNet50 or VGG16 classifies real photos correctly out of the box.
- **1052:** early-layer filters look like edges and later feature maps respond to parts (Zeiler and Fergus).
- **1053:** feature extraction beats training from scratch on a small subset, and fine-tuning the top block helps a little more.
- **1054:** a functional model with two inputs or a skip connection.

Average over seeds where results are noisy. Prefer clear, simple demos.

## Figures
Use Plotly, TikZ or Manim, never matplotlib. Animations become Plotly frames, then an ffmpeg GIF plus a `_frames.png` grid for the PDF; see `603-hessian-and-multivariate-taylor/images/optimizer_race.py`. Check every figure PNG yourself.

## Do not touch
Anything outside your six folders: no glossary, course_map, dl_map, tools, docs or other Notes. Do not write a "Where this fits" box.

## Final report
Write it to `~/campusx/docs/remote/cnn-practice-report.md`. Per Note, include:
- figures, with the tool and the reason for each;
- concepts, with their pipeline step;
- map suggestions (Concept ids and links: needs / is a kind of / fixes / compared with / used in);
- key terms;
- corrections to the transcript, with sources;
- what was linked instead of repeated;
- the placeholder links;
- every Extra box and beyond-transcript claim with its backing;
- an UNRESOLVED list;
- build status.
