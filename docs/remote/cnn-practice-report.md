# Report: DL Notes 1049–1054 (CNN in practice)

Written on topgro, 2026-10-03. No git was run. All six folders hold `note.md`, `notebook.ipynb` (stored without outputs), `data/`, `images/` and the executed notebook in `.logs/notebook.ipynb`. Every Note builds with `tools/build.sh` and prints "Built".

## General notes

**Environment and data**

- **Data.** The data came from four places, none of it stored in the repo except small thumbnails:
  - Cats vs dogs: the Microsoft download `kagglecatsanddogs_5340.zip`, unpacked to `~/datasets/PetImages`. Every notebook downloads it if it is missing, and deletes files without "JFIF" in their header, exactly as the official Keras example does (1,590 files).
  - The small subset (1,000 + 1,000 training, 500 + 500 validation, 500 + 500 test, seed 0) is a folder of symbolic links, `~/datasets/cats_vs_dogs_small`, built by the notebooks.
  - UTKFace (1054) came from the Hugging Face copy `py97/UTKFace-Cropped`, because the official download link no longer works.
  - Photos for prediction came from Wikimedia Commons. All are under licences that allow reuse, and each author and licence is listed in the Note's Sources.
- **No dataset images stored.** `data/` holds only CSVs, small arrays and small JPEG thumbnails. The largest `data/` folders are 1052 (332 KB) and 1050 (316 KB).
- **The GPU was shared.** Kernels from another session used 1 to 6 GB of the 8 GB card throughout. Because of that:
  - 1049 uses mixed precision (`mixed_float16`, with a float32 output layer) and caps cuDNN's workspace at 256 MB. The notebook says why. The model and hyperparameters are unchanged.
  - 1050 and 1054 were executed on the CPU (`CUDA_VISIBLE_DEVICES=""`), while 1049 and 1053 ran on the GPU.
  - On another machine the GPU will be used and the numbers will differ slightly, but the conclusions should not.
- **Op determinism is off.** `enable_op_determinism()` is not used, because its extra cuDNN workspace ran out of memory on the shared GPU. Seeds are fixed, but GPU runs are not bit-for-bit reproducible. Every number in the Notes matches the executed copy in `.logs/`.
- **Chrome for Plotly.** Kaleido found no Chrome on this machine. I set `BROWSER_PATH` to the existing Puppeteer Chrome (`~/.cache/puppeteer/chrome/linux-147.0.7727.57/chrome-linux64/chrome`) when calling `tools/build.sh`. Nothing was installed. The build machine needs Chrome, or the same variable.
- **LaTeX.** No package was missing.
- **The build writes outside my folders.** `tools/build.sh` writes `pdf/<folder>.pdf` and `images/.built_*` stamps as designed. Nothing else outside the six folders was changed.

**Incidents in the previous run**

- **Your email went to an outside service.** A fact-checking subagent passed the user's email address to the Unpaywall API in a single lookup, to find an open copy of the Shorten and Khoshgoftaar paper. I did not ask for this. No subagent was used in the second run, and no personal data was sent anywhere.
- **Stray folder, removed.** A bug of mine briefly wrote data files to `~/campusx/data/`. That folder did not exist before and held only my files. I deleted it.

**Sources**

- **Fact-checking.** Papers were read as arXiv PDFs or official proceedings PDFs. The other sources were the Keras guides and API pages, the Goodfellow book chapters on deeplearningbook.org, and the Chollet notebooks.
- **Chollet editions.** The printed 2nd edition (2021) was not available. For code facts I cite its companion notebooks (augmentation layers, `layers[:-4]`, `RMSprop(1e-5)`). For prose quotes I cite the 1st edition (2017, §5.3–5.4 companion notebooks with prose) or the free 3rd edition (Chollet and Watson 2025, deeplearningwithpython.io), whichever I actually read.
- **Teacher's name.** No Note mentions the teacher, the videos or the course. I grepped all six Notes.

**Placeholder links (CNN theory Notes still being written)**

| Linked from | Placeholder |
|---|---|
| 1049 | `../1043-padding-and-strides/note.md`, `../1044-pooling/note.md`, `../1045-lenet-5/note.md` |
| 1051 | `../1043-padding-and-strides/note.md`, `../1045-lenet-5/note.md` |
| 1052 | `../1040-cnn-intuition/note.md`, `../1042-convolution-operation/note.md`, `../1044-pooling/note.md` |

1040 has no `note.md` yet. Where 1052 says "The CNN intuition Note claimed that early layers find simple features", that claim must survive in 1040's final text; if it does not, rephrase the sentence. The Notes also link to each other (1049 to 1054) and to existing Notes: 1002, 1003, 1011, 1014, 1018, 1022, 1023, 1024, 1026, 1027, 1031 and 1055.

---

## 1049 Cat vs dog CNN

**Figures**

| Figure | Tool | Why |
|---|---|---|
| 1 `samples.png` | Plotly image grid | Six dataset thumbnails with label and original size; the only dataset images kept (`data/samples.npz`, 254 KB) |
| 2 `cnn.tex` | TikZ diagram | Still architecture, with output sizes and parameters per layer |
| 3 `curves.png` | Plotly chart | Training vs validation accuracy and loss, 3 seeds |
| 4 `compare.png` | Plotly chart | Plain vs batch normalisation + dropout: validation accuracy and the gap |

**Experiment.** 23,410 photos (after deleting 1,590 damaged files), split 18,728 for training and 4,682 for validation. The transcript's CNN (3 × Conv/Pool with 32, 64, 128 filters; Dense 128, 64, 1) at 256 × 256, Adam, 10 epochs, 3 seeds. Mixed precision was used because of the shared GPU.

| | Plain CNN | + batch normalisation (after each conv) and dropout 0.1 (after each hidden dense) |
|---|---|---|
| Training accuracy, epoch 10 | 99.1% | 97.4% |
| Validation accuracy, epoch 10 | 78.9% | 80.3% |
| Gap | 0.20 | 0.17 |
| Validation loss | lowest at epoch 3 (0.44), then 1.34 | lowest at epoch 5 (0.46), then 0.76 |

- The overfitting principle shows clearly in the plain model.
- The remedy helps only a little, matching the transcript ("gap reduced a little"). The Note says so plainly and points to augmentation and early stopping as stronger remedies.
- **New photos.** Two Wikimedia photos were labelled correctly by both models: the kitten gave P(dog) = 0.000, the golden retriever 0.999 and 1.000.

**Concepts and pipeline steps**

| Concept | Step |
|---|---|
| Loading images from class folders in batches | 2 Get data |
| Resizing images to one shape | 4 Clean (or 5) |
| Pixel scaling | 5 |
| A CNN for binary image classification | 8 |
| Parameter count of conv and dense layers | 8 |
| Overfitting diagnosis from learning curves | 9 |
| Remedies | 8 / 10 |
| Predicting a new image | 11 Deploy |

**Map suggestions**

- `cnn_project` needs `cnn_architecture` (1045), `keras` and `input_scaling`; used in nothing yet.
- `image_loading` used in `cnn_project`, `data_augmentation` and `transfer_learning`.
- `cnn_project` compared with `ann_classification`.
- `dropout` fixes `overfitting`, and `batch_norm` fixes `overfitting` (both already in the map; this Note is evidence for a mild effect).

**Key terms.** Binary image classification, observation, target, batch, generator, `image_dataset_from_directory`, epoch, overfitting, validation set.

**Corrections to the transcript**

- **Parameter count.** The model has 14,847,297 parameters, about 14.8 million; the transcript's "148,000,000" is a slip. Of these, 99.3% are in the first dense layer (Notebook).
- **Dataset size.** The transcript's dataset is the Kaggle version with 20,000/5,000 photos. We use the Microsoft download (23,410 usable), so the counts differ.
- **Colab, Kaggle API and `kaggle.json` steps** are not taught; only "a GPU helps; Colab offers one" is kept.
- **OpenCV is not used.** The transcript reads photos with OpenCV (BGR order, hence "weird" colours). The Note uses `keras.utils.load_img` (RGB) and does not make the BGR claim, because I did not open the OpenCV docs.
- **The transcript's 80–81% after batch normalisation and dropout** is replaced by our measured 80.3%.

**Linked instead of repeated.** Output-size formula (1043), pooling (1044), CNN architecture (1045), Keras basics (1011), data scaling (1023), regularisation (1026), dropout (1024), batch normalisation (1031), early stopping (1022), loss functions (1014), GPUs (1002 §5.2), augmentation (1050).

**Extra boxes and beyond-transcript claims, with backing**

- No Extra boxes.
- Deleting files without "JFIF" (1,590 files) and the name "Kaggle Cats vs Dogs dataset": the Keras example "Image classification from scratch" (checked).
- The readme pointing to Microsoft Research's Asirra project: the readme in the download.
- `image_dataset_from_directory` defaults: Keras docs.
- Memory of 3.7 and 14.7 GB, output sizes and parameter counts: maths derivations, matched by the Notebook.

**UNRESOLVED.** None.

**Build:** Built.

---

## 1050 Data augmentation

**Figures**

| Figure | Tool | Why |
|---|---|---|
| 1 `aug_animation.gif` (+ `_frames.png`) | Plotly frames, then an ffmpeg GIF | Shows that each epoch sees a new random version; motion is the point |
| 2 `transforms.png` | Plotly image grid | The five transformations side by side, two random draws each |
| 3 `fill_modes.png` | Plotly image grid | The four `fill_mode` options on the same shifted photo |
| 4 `curves.png` | Plotly chart | Training vs validation accuracy, without and with augmentation, 3 seeds |

**Experiment.** 2,000 training photos, the small CNN of the Keras blog, 60 epochs, 3 seeds:

| | Without augmentation | With augmentation |
|---|---|---|
| Gap between training and validation accuracy, epoch 60 | 0.276 | 0.023 |
| Validation loss | rises from 0.57 to 3.78 | stays near 0.55 |
| Test accuracy | 72.4% | 78.2% |

The principle (augmentation closes the gap) shows clearly. The text also reports honestly that augmentation is behind at epoch 5 (62.5% vs 69.4% validation accuracy).

**Concepts and pipeline steps**

| Concept | Step |
|---|---|
| Data augmentation | 5 Engineer features (or 8 Model, as a regulariser) |
| Augmentation safety | 5 |
| Random preprocessing layers | 8 |
| `fill_mode` | 5 |

**Map suggestions**

- `data_augmentation` fixes `overfitting`; fixes `data_quantity`.
- `data_augmentation` is a kind of `regularisation`.
- `data_augmentation` needs `labelled_data`.
- `data_augmentation` used in `cnn_project` (1049) and `transfer_learning` (1053).
- `data_augmentation` compared with `dropout`.

**Key terms.** Data augmentation, generalise, horizontal flip, rotation/shift/zoom/shear, safety of an augmentation, `fill_mode`, random preprocessing layer, `ImageDataGenerator`.

**Corrections to the transcript**

- **`ImageDataGenerator` no longer works as taught.** It is deprecated (TensorFlow docs). In Keras 3 it cannot be imported from `keras.preprocessing.image` (the Notebook checked), so the Note teaches the random layers and mentions `ImageDataGenerator` in an Extra box. `fit_generator` is likewise gone; `fit` takes datasets.
- **Small numbers from the transcript are not repeated.** The transcript's results (57% without vs 69% with augmentation after 5 epochs; 74% after 25) are replaced by our own measured numbers.
- **The shear setting is in degrees, not percent.** In `ImageDataGenerator`, `shear_range=0.2` means 0.2 degrees, not "distorting 0.2 on a scale of 1" (tf-keras source docstring: "Shear angle in counter-clockwise direction in degrees"; checked). The Note states this in the Extra box.

**Linked instead of repeated.** Overfitting and regularisation (1026), the dataset and loading (1049), transfer learning (1053), AlexNet (1051).

**Extra boxes and beyond-transcript claims, with backing**

- **Extra box (5.1), `ImageDataGenerator` deprecated.** Backed by the TensorFlow documentation and the Notebook's import test.
- "The best way to make a ML model generalize better..." and "particularly effective technique for ... object recognition": Goodfellow §7.4, p. 236.
- Medical image analysis lacks big data: Shorten and Khoshgoftaar 2019, abstract.
- Augmentation safety, with the 6 vs 9 example: Shorten and Khoshgoftaar p. 7. The "b" and "d" example: Goodfellow p. 237.
- AlexNet used shifts and flips and overfits without them: Krizhevsky et al. 2012, §4.1.
- Layers are inactive at inference: Keras `RandomFlip` docs, plus the Notebook test (`training=False` returns the image unchanged).
- `reflect` is the default fill mode and `constant` fills with 0: the Keras layer signatures (checked in code).
- The small CNN and the 1,000 photos per class: Keras blog 2016. The augmentation layer settings: Chollet 2021, ch. 8 notebook.

**UNRESOLVED**

- The malaria-detection example comes from the transcript. No source checks its cost figures, and the Note gives none.

**Build:** Built.

---

## 1051 Pretrained models

**Figures**

| Figure | Tool | Why |
|---|---|---|
| 1 `predictions.png` | Plotly image grid | The 11 photos with ResNet50's top answer |
| 2 `ilsvrc_errors.png` | Plotly bar chart | Winning error by year, with the human line |
| 3 `alexnet.tex` | TikZ diagram | Still architecture, with output sizes |

**Experiment.** ResNet50 with ImageNet weights, no training, 11 Wikimedia photos. It was correct on all 10 photos whose class exists in ImageNet; probabilities were 0.40 to 1.00, and 7 of the 10 were above 0.9. The tomato was answered "hip" (0.43) and "strawberry" (0.22); the Notebook confirms that "tomato" is not among the 1,000 classes.

**Concepts and pipeline steps**

| Concept | Step |
|---|---|
| Pretrained model | 8 |
| ImageNet | 2 Get data |
| ILSVRC and top-1/top-5 error | 9 Evaluate |
| AlexNet | 8 |
| `keras.applications` | 8 |
| `preprocess_input` | 5 |

**Map suggestions**

- `pretrained_model` fixes `data_quantity`; needs `imagenet`; used in `transfer_learning`.
- `alexnet` is a kind of `cnn_architecture`; `alexnet` needs `relu`.
- `imagenet` needs `labelled_data`.
- `top5_error` compared with `accuracy`.
- `resnet` needs `skip_connection` (1054) and fixes `vanishing_gradient`.

**Key terms.** Pretrained model, labelled data, ImageNet, WordNet, bounding box, crowdsourcing, ILSVRC, top-1 error, top-5 error, AlexNet, `keras.applications`, `preprocess_input`, `decode_predictions`.

**Corrections to the transcript**

- **ImageNet's size.** ImageNet has 14,197,122 images in 21,841 categories, not "1.4 million / 20,000" (Russakovsky §1.1). The transcript's "1.4 crore" is right in Indian units.
- **The 2013 winner.** The winner was Clarifai with 11.7%, not ZFNet. ZF's entry scored 13.5% (Russakovsky Table 6).
- **2014.** GoogLeNet won with 6.7%; VGG was second with 7.3%. The transcript has VGG in 2014 and Google in 2015.
- **2015.** ResNet won in 2015 (3.57%), not 2016 (He et al., abstract and Table 5).
- **AlexNet's team.** AlexNet is by Krizhevsky, Sutskever and Hinton. The transcript's "Geoffrey Hinton's ... LXNet" is a transcription slip.
- **ReLU was not AlexNet's invention.** The paper says it follows Nair and Hinton 2010 and is "not the first to consider alternatives" (§3.1).
- **GPUs were not new either.** AlexNet "used a GPU instead of a CPU for the first time" is not claimed in the Note. The Note says only that it trained on two GTX 580s (§1). Earlier GPU training (Raina et al. 2009) is mentioned in Note 1002.
- **AlexNet's input size.** The paper says 224 × 224; 227 is needed for its own 55 × 55 output. The Note shows the derivation.
- **Human error.** The human estimate is 5.1% for one trained annotator on 1,500 images (Russakovsky §6.4.1), not "humans 5%".
- **Top-5 wording.** "Top 1% / top 5% accuracy" is a slip for top-1 / top-5 accuracy.

**Linked instead of repeated.** The output-size formula (1043), CNN architecture (1045), history and AlexNet's impact (1003), GPUs (1002), ReLU (1027), dropout (1024), augmentation (1050), skip connections (1018), transfer learning (1053).

**Extra boxes and beyond-transcript claims, with backing**

- **Extra box: AlexNet's 227 vs 224.** Backed by a maths derivation in the Note, and Krizhevsky §3.5.
- **Extra box: ReLU not first; 15.3% vs 16.4%.** Backed by Krizhevsky §3.1 and §6, and Russakovsky Table 6.
- ImageNet built on WordNet, verified by several Turk workers: Deng et al. 2009, §3.2.
- 1,034,908 bounding-box images: the ImageNet summary statistics page (archived). Found by the subagent in the first run; I did not reopen it this run.
- 120 dog breeds: Russakovsky Figure 2.
- 1,281,167 / 50,000 / 100,000 photos: Russakovsky Table 2.
- SIFT and LBP features in 2010: Russakovsky §5.1.
- GoogLeNet has 22 layers: Szegedy et al. 2015.
- The Keras applications table: keras.io.
- What `preprocess_input` "caffe" mode does: Keras source and docs.
- File size ≈ 4 bytes × parameters: maths derivation (528 MB for VGG16, matching the table).

**UNRESOLVED**

- The 1,034,908 figure rests on an archived page that I have not reopened myself in this run.

**Build:** Built.

---

## 1052 What a CNN sees

**Figures**

| Figure | Tool | Why |
|---|---|---|
| 1 `top_patches.png` | Plotly image grid | The main evidence (Zeiler–Fergus style) |
| 2 `vgg16_layers.tex` | TikZ diagram | Layer positions as Keras lists them |
| 3 `first_filters.png` | Plotly image grid | VGG16's 3 × 3 and ResNet50's 7 × 7 first-layer filters |
| 4 `feature_maps.png` | Plotly image grid | One photo through six layers |
| 5 `sparsity.png` | Plotly chart | Zero values and blank maps by layer, over 500 photos |

**Experiments**

- **Filters.** ResNet50's 7 × 7 first-layer filters are clearly oriented edge detectors and colour blobs. VGG16's 3 × 3 filters are too small to read.
- **Feature maps.** They go from edge drawings (layers 1 to 2) to sparse spots (layers 13 to 17). Two of the eight layer-17 maps of the kitten photo are blank.
- **Sparsity, over 500 photos.** The share of zero values grows from 47% (block1_conv1) to 92% (block5_conv3). Blank maps appear almost only in block5_conv3 (12.8%).
- **Top patches over 1,000 photos.** Channels were chosen by a fixed rule: the two maps the kitten excites most per layer.

  | Layer | What the top patches show |
  |---|---|
  | Block 3 (40-pixel receptive field) | Dark spots with a bright highlight: mostly eyes, also a button and a printed letter |
  | Block 4 (92 pixels) | Cat eyes (all 6 photos are cats); dog snouts (all 6 are dogs) |
  | Block 5 (196 pixels) | Whole cats and cat heads (all 12 are cats) |

  This is the Zeiler and Fergus progression. The receptive-field sizes come from a maths derivation shown in the Note.

**Concepts and pipeline steps**

| Concept | Step |
|---|---|
| CNN visualisation (filters, feature maps) | 9 Evaluate |
| Sparsity of activations | 9 |
| Receptive field growth | 8 |
| Top activations | 9 |

**Map suggestions**

- `cnn_visualisation` needs `convolution` and `pretrained_model`.
- `cnn_visualisation` compared with `representation_learning`.
- `feature_hierarchy` used in `transfer_learning`.
- `receptive_field` needs `pooling`.

**Key terms.** Black box, filter, feature map, edge detector, colour blob, VGG16, sparse, blank map, receptive field, top activations.

**Corrections to the transcript**

- **No "human being" class.** The transcript says VGG16's classes include one; none of the 1,000 class names is a person, human or face (Notebook; "face_powder" only). Given in an Extra box.
- **The transcript's "layer 17".** It is block5_conv3 at Keras position 17; the transcript's counting matches positions in `vgg.layers`. No change was needed.
- **The kitten replaces the cricketer's photo.** The transcript uses a photo of a named cricketer. The Note uses a CC BY kitten photo instead, and never names a person.

**Linked instead of repeated.** Convolution, filters and feature maps (1042), pooling and receptive field (1044), ReLU (1027), VGG16 (1051), the "early layers simple" idea (1040, 1002 §2.4), `keras.Model` (1054).

**Extra boxes and beyond-transcript claims, with backing**

- **Extra box: no person class.** Backed by the Notebook's class search.
- First layers as edge detectors and colour blobs: Krizhevsky §6.1 and Figure 3; Yosinski abstract; Goodfellow §9.10 pp. 364–365 (also the line "we can just display an image of the convolution kernel"); Chollet 2017 §5.4; Chollet and Watson 2025 ch. 10.
- Sparsity and abstraction with depth: Chollet and Watson 2025, ch. 10 (quoted), plus the Notebook's measurement.
- Zeiler and Fergus "top 9 activations" and layers 4 and 5: Zeiler and Fergus §4 (quoted).
- ResNet50's first layer is 7 × 7: He et al. 2016, Table 1.
- Receptive fields of 40, 92 and 196 pixels: maths derivation.

**UNRESOLVED.** None.

**Build:** Built.

---

## 1053 Transfer learning

**Figures**

| Figure | Tool | Why |
|---|---|---|
| 1 `strategies.tex` | TikZ diagram | What is frozen in each strategy |
| 2 `results.png` | Plotly chart | Validation curves per method, plus test-accuracy bars with seed range |

**Experiment.** 2,000 training, 1,000 validation and 1,000 test photos; 3 seeds per method.

| Method | Test accuracy | Seed range |
|---|---|---|
| From scratch (augmented small CNN, 60 epochs, batch 32) | 76.5% | 74.3–79.7% |
| Feature extraction (frozen VGG16 base, new Dense 256 head, Adam, 20 epochs) | 94.9% | 94.3–95.9% |
| Fine-tuning (same first 10 epochs, then block 5 unfrozen, RMSprop 1e-5, 10 epochs) | 95.7% | 95.5–95.9% |

- Both principles show: feature extraction beats scratch by 18 points, and fine-tuning adds 0.8 points, with tighter seeds and a lower validation loss (0.73 vs 1.37).
- **Speed shortcut.** Blocks 1 to 4 were run once and their output stored, because they are frozen in both transfer methods and there is no augmentation. The Notebook checks that the split model equals VGG16's base on real photos (`allclose`: True). The Note explains this in an Extra box.

**Concepts and pipeline steps**

| Concept | Step |
|---|---|
| Transfer learning | 8 |
| Convolutional base and top | 8 |
| Freezing (`trainable`) | 8 |
| Feature extraction | 8 |
| Fine-tuning | 10 Tune (or 8) |

**Map suggestions**

- `transfer_learning` needs `pretrained_model`; fixes `data_quantity`; fixes `overfitting`.
- `feature_extraction_tl` is a kind of `transfer_learning`; `fine_tuning` is a kind of `transfer_learning`.
- `fine_tuning` compared with `feature_extraction_tl`.
- `transfer_learning` compared with `cnn_from_scratch`; used in `functional_api` (1054).
- Note 1067's "transfer learning in NLP" compared with this computer-vision use.

**Key terms.** Transfer learning, convolutional base, top, freeze, feature extraction, fine-tuning, `include_top=False`, `trainable`.

**Corrections to the transcript**

- **Pixel scaling.** The transcript divides pixels by 255 for VGG16. Keras documents `preprocess_input` (BGR, mean subtraction) for VGG16; the Note uses it and explains the difference in an Extra box.
- **`fit_generator`** no longer exists; `fit` is used.
- **"16.8 million parameters" is right.** The transcript's "1.6 crore" is consistent with 16,812,353.
- **Unchecked claims left out.** The "Andrew Ng chart" and the Wikipedia definition are not used. I could not open a source for the chart; the definition is taken from the Keras guide instead.
- **Training order.** The transcript fine-tunes in one stage. The Note trains the top first and then unfreezes block 5, as Chollet (§5.3) and the Keras guide recommend.

**Linked instead of repeated.** ImageNet and VGG16 (1051), feature hierarchy (1052), augmentation and the scratch model (1050), 1002 §5.4. Note 1067 is not linked from 1053; its NLP transfer learning is a different setting, and 1067 already links back to 1002.

**Extra boxes and beyond-transcript claims, with backing**

- **Extra box (7.1), `preprocess_input`.** Backed by the Keras docs.
- **Extra box (8.1), the stored-output shortcut.** Backed by the Notebook's equivalence check.
- Definition and workflow: the Keras transfer learning guide (quoted).
- General vs specific features; transferability falls with task distance: Yosinski 2014 abstract (quoted).
- Train the top first; very low learning rate; fine-tune the specialised layers: Chollet 2017 §5.3 (quoted).
- RMSprop 1e-5 and the last block: Chollet 2021 ch. 8 notebook.
- ImageNet includes cat and dog classes: Russakovsky (120 dog breeds), plus the cat classes found in the 1051 Notebook.

**UNRESOLVED.** None.

**Build:** Built.

---

## 1054 Keras functional API

**Figures**

| Figure | Tool | Why |
|---|---|---|
| 1 `topologies.tex` | TikZ diagram | Sequential vs two outputs vs three inputs |
| 2 `toy_two_outputs.tex` | TikZ diagram | The toy model with parameter counts |
| 3 `two_inputs_and_skip.tex` | TikZ diagram | Concatenate and Add |
| 4 `age_gender_model.tex` | TikZ diagram | The real model |
| 5 `two_output_curves.png` | Plotly chart | Both test metrics per epoch, with guessing baselines |

**Experiment.** UTKFace: 23,705 photos, split 18,964 for training and 4,741 for testing. Frozen VGG16 base at 128 × 128, two Dense 256 branches, losses MAE and binary cross-entropy with weights 0.1 and 1.0, 15 epochs, 3 seeds.

| Model | Age MAE | Gender accuracy |
|---|---|---|
| One model, two outputs | 9.15 years (8.60–9.78) | 86.3% |
| Separate models | 8.65 years (8.33–9.06) | 85.9% (84.4–86.8%) |
| Guessing | 15.03 years | 52.5% |

The seed ranges overlap. The single model needs 18.9 million parameters against 33.6 million for two separate full models. Training used the same stored-base-output shortcut as 1053, explained in an Extra box. The toy models were built and summarised: 8,898 parameters, 10,789, and the skip block 4,640.

**Concepts and pipeline steps**

| Concept | Step |
|---|---|
| Functional API | 8 |
| Multi-output model | 8 |
| Multi-input model | 8 |
| `Concatenate` | 8 |
| Skip (residual) connection | 8 |
| Loss weights | 8 |

**Map suggestions**

- `functional_api` compared with `keras` (Sequential); needs `keras`.
- `multi_output_model` and `multi_input_model` are each a kind of `functional_api` model.
- `skip_connection` fixes `vanishing_gradient`; used in `resnet`.
- `multi_output_model` used in an age and gender project; needs `transfer_learning`.
- `loss_weights` used in `multi_output_model`.

**Key terms.** Feature, target, observation, Sequential model, functional API, topology, multi-output model, multi-input model, `Input`, `Concatenate`, skip (residual) connection, `Add`, loss weight.

**Corrections to the transcript**

- **Which layer the age output reads.** In the toy example the transcript first says the age output connects to `hidden1`, then draws both outputs from `hidden2`. The Note follows the diagram (both from `hidden2`).
- **No emotion labels.** The face example mentions emotion; UTKFace has age, gender and race but no emotion. The Note uses age and gender, as the transcript's own Kaggle example does.
- **`class_mode="multi_output"`** belongs to the old `flow_from_dataframe`; it is not used.
- **The UTKFace numbers.** The transcript gives no results; ours are new.

**Linked instead of repeated.** Sequential and Keras basics (1011), losses (1014), transfer learning (1053), residual blocks (1018), ResNet (1051), RNN (1055, used only as an example input).

**Extra boxes and beyond-transcript claims, with backing**

- **Extra box (4.1), `plot_model`.** Backed by the Keras functional API guide. The `pydot`/Graphviz requirement was observed here: neither is installed, so `plot_model` is not run.
- **Extra box (5.3), stored base output.** Backed by the same reasoning as 1053, and the frozen base.
- Sequential is "appropriate for a plain stack of layers..." and the list of when it is not appropriate: the Keras Sequential guide (quoted).
- "The functional API can handle models with non-linear topology...", "This cannot be handled with the Sequential API", loss weights "modulate their contribution", residual connections: the Keras functional API guide (quoted).
- Chollet's "basically a Python list ... limited to simple stacks of layers": Chollet and Watson 2025, ch. 7.
- UTKFace facts (over 20,000 photos, ages 0–116, file-name labels, gender codes, non-commercial licence): the official dataset page.
- Parameter counts: maths derivations, matched by the Notebook.

**UNRESOLVED**

- The UTKFace copy comes from an unofficial Hugging Face mirror (the official link is dead). The licence is non-commercial research only. The Note stores no faces, but the reviewer should confirm this use is acceptable.

**Build:** Built.

---

## Run log (second session)

- **Runs restarted.** The first session's runs for 1049, 1050, 1053 and 1054 were killed when it ended. All four were re-executed end to end with `nbconvert` into `.logs/`, and the Notes' numbers come from those executed copies.
- **No subagents, no outside personal data.** No subagents were used in the second session, and no personal data was sent to any service.
- **1053 scratch model batch size.** It uses batches of 32 (the same as the transfer methods), not 1050's 16. Its 76.5% therefore differs slightly from 1050's 78.2%; the 1053 Note says so.
- **Final pass.** I shortened long code lines in all Python boxes so that they do not wrap in the PDF, and replaced three vague "It" sentence openings in 1051.
