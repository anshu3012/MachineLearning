# Claims audit, group 0

34 Notes checked (folders in `docs/audit/audit_00`).

## Findings

| Note | Quote (short) | Verdict | Action |
|---|---|---|---|
| 01-course-map | Algorithm chooser figure: "Deep learning (not in this course; see Note 2)" | WRONG FACT | not fixed: text lives in course_map/algorithm_chooser.tex, which this audit may not touch; DL Notes 1001+ exist |
| 01-course-map | Algorithm chooser picks ("best accuracy on tables: random forest, XGBoost", "small dataset: KNN, SVM") | UNSUPPORTED | not fixed: same file; the figure is labelled DRAFT and the Note says it is a starting point |
| 01-what-is-ml | "'without being explicitly programmed' is usually credited to Arthur Samuel" | UNSUPPORTED | sourced: Samuel 1959, IBM J. Res. Dev. 3(3); reworded to say the phrase is a later paraphrase of his sentence |
| 01-what-is-ml | "Tom Mitchell (1997)" definition | UNSUPPORTED | sourced: Mitchell, Machine Learning, McGraw-Hill 1997, Ch. 1 |
| 01-what-is-ml | "Paul Graham ... outperformed hand-written rules" | UNSUPPORTED | sourced: Graham, A Plan for Spam (Aug 2002); now states his reported numbers |
| 01-what-is-ml | "data mining ... also called KDD" + "difference is mainly how hidden the patterns are" | UNSUPPORTED | sourced: Han, Kamber and Pei 2011, Sec. 1.2; second sentence now tied to the Note's own Section 4.3 (transcript) |
| 01-what-is-ml | "Rosenblatt ... 1957 ... AlexNet won ... by a wide margin" | UNSUPPORTED | sourced: Rosenblatt 1957 Cornell report 85-460-1; Krizhevsky et al. NeurIPS 2012 (15.3% vs 26.2% top-5) |
| 01-what-is-ml | "IBM estimate from 2013 ... internet users passed 5 billion in 2022" | UNSUPPORTED | sourced: IBM Smarter Computing Big Data brochure (2013); internet users sourced: ITU Facts and Figures 2022 (5.3 bn), 2024 (5.5 bn) |
| 02-ai-vs-ml-vs-dl | "The start of AI is usually dated to Alan Turing's 1950 paper" | WRONG FACT | sourced: Turing 1950, Mind 59(236); Russell and Norvig 4th ed. 2020, Sec. 1.3.1 (the name comes from the 1956 Dartmouth workshop); reworded to give both dates |
| 02-ai-vs-ml-vs-dl | "researchers inspected trained networks ... early layers respond to edges" | UNSUPPORTED | sourced: Zeiler and Fergus, ECCV 2014, Fig. 2 |
| 03-types-of-ml | "MNIST uses 28 x 28 pixel images, 784 columns" | UNSUPPORTED | sourced: LeCun et al., Proc. IEEE 1998, Sec. III.A |
| 03-types-of-ml | "Placing the two side by side increased sales" / "most likely comes from a 1992 analysis for Osco" | WRONG FACT | sourced: D. Power, DSS News, 10 Nov 2002 (Osco did not move the products); Extra now says the sales gain is legend |
| 04-batch-learning | "usually called model drift ... or concept drift" | UNSUPPORTED | sourced: Gama et al., ACM Computing Surveys 46(4), 2014, Sec. 2.1 |
| 04-batch-learning | "Figure 3 shows the effect" (figure is a made-up curve) | UNSUPPORTED | reworded: now labelled a sketch, not measured data |
| 06-instance-vs-model-based | "Measured raw, distances would depend almost only on IQ" | UNSUPPORTED | derived: distance formula with the notebook's ranges (60 and 5 give squared terms up to 3600 vs 25) |
| 06-instance-vs-model-based | "sometimes called eager learning" | UNSUPPORTED | sourced: Mitchell, Machine Learning, 1997, Sec. 8.6 |
| 06-instance-vs-model-based | "This is why it is also called lazy learning" (term not in the lecture) | UNSUPPORTED | sourced: Mitchell 1997, Sec. 8.6 |
| 07-challenges-in-ml | "published by Michele Banko and Eric Brill (Microsoft) in 2001 ... 2009 article ... three Google researchers" | UNSUPPORTED | sourced: Banko and Brill, ACL 2001; Halevy, Norvig and Pereira, IEEE Intelligent Systems 24(2), 2009 (full references added) |
| 07-challenges-in-ml | "Sculley and others, Google, 2015. Its main figure" | UNSUPPORTED | sourced: Sculley et al., NeurIPS 2015, Fig. 1 |
| 08-applications-of-ml | "Twitter earns money by licensing its data ... In 2014 it bought Gnip" | UNSUPPORTED | sourced: Twitter Form 10-K FY2018 (data licensing revenue); Gnip deal April 2014 |
| 08-applications-of-ml | "A 2011 study by Bollen, Mao and Zeng" | UNSUPPORTED | sourced: J. Computational Science 2(1), 2011 (journal added) |
| 08-applications-of-ml | "Twitter was founded in 2006 and made its first full-year profit only in 2018" | UNSUPPORTED | sourced: Twitter Form 10-K FY2018 (net income about 1.2 bn USD vs 2017 loss) |
| 08-applications-of-ml | "In banking it is called credit scoring ... probability of default" | UNSUPPORTED | sourced: Thomas, Edelman and Crook, Credit Scoring and Its Applications, SIAM 2002, Ch. 1 |
| 09-mldlc | "Apache Spark is a widely used tool for ... data too big for one computer" | UNSUPPORTED | sourced: Zaharia et al., CACM 59(11), 2016 |
| 09-mldlc | "A model trained on such data tends to favour the large class" | UNSUPPORTED | sourced: He and Garcia, IEEE TKDE 21(9), 2009, Sec. 2 |
| 09-mldlc | "Handling imbalance usually means ... oversampling ... undersampling" | UNSUPPORTED | sourced: He and Garcia 2009, Sec. 3.1 |
| 09-mldlc | "Dunn index is higher when clusters are tight and far apart" | UNSUPPORTED | sourced: Dunn, J. Cybernetics 4(1), 1974; formula stated |
| 09-mldlc | "settings we choose before training are hyperparameters" | UNSUPPORTED | sourced: Goodfellow, Bengio and Courville, Deep Learning, 2016, Sec. 5.3 |
| 09-mldlc | "Using an ensemble usually improves performance, so it is a step we almost always take" | UNSUPPORTED | sourced: Dietterich, MCS 2000, Sec. 1; short citation added; original wording kept |
| 09-mldlc | "free options for small demos today include Render and Hugging Face Spaces" | WRONG FACT | sourced: HF Spaces docs now require a paid plan for Gradio/Docker Spaces, so HF removed; Render "Deploy for Free" docs; Heroku changelog (28 Nov 2022) |
| 09-mldlc | "loading a pickle can run code" | UNSUPPORTED | sourced: Python docs, pickle module warning |
| 09-mldlc | "Because the groups are random, a clear difference can be put down to the new version" | UNSUPPORTED | sourced: Kohavi, Tang and Xu, Trustworthy Online Controlled Experiments, 2020, Ch. 1 |
| 09-mldlc | "running and maintaining live models is called MLOps" | UNSUPPORTED | sourced: Kreuzberger, Kühl and Hirschl, IEEE Access 11, 2023 |
| 11-tensors | "MPEG and MP4 compress ... without a visible loss in quality. A one-minute MP4 ... typically only about 10 to 50 MB" | UNSUPPORTED | sourced: Le Gall, CACM 34(4), 1991 (how MPEG compresses); YouTube Help bitrate 2.5 Mbps for 480p; derived 19 MB vs 7.5 GB raw, about 400 times |
| 11-tensors | "In NumPy ... every tensor is an array" | UNSUPPORTED | sourced: NumPy docs, ndarray page |
| 11-tensors | "table of all inputs is usually called X, and the output column y" | UNSUPPORTED | sourced: scikit-learn Glossary, X and y |
| 11-tensors | "TensorFlow usually puts the channels last ... PyTorch puts them first" | UNSUPPORTED | sourced: tf.keras.layers.Conv2D data_format docs; torch.nn.Conv2d docs |
| 12-setup-anaconda-jupyter-colab | "We use conda ... pip only for packages that conda does not have" (pip vs conda facts) | UNSUPPORTED | sourced: Helmus, Understanding Conda and Pip, Anaconda blog 2018 |
| 12-setup-anaconda-jupyter-colab | "paid licence ... in organisations with 200 or more people" | UNSUPPORTED | sourced: Anaconda Terms of Service FAQs 2024 (also covers contractors; university exemption added) |
| 12-setup-anaconda-jupyter-colab | "installer of about 450 MB ... about twice that size" | UNSUPPORTED | sourced: repo.anaconda.com/archive listing (477 MB in 2021.05, 1.0 GB in 2026.07) |
| 12-setup-anaconda-jupyter-colab | "`notebook` ... which our environment does not include" / "ipywidgets ... not in our environment" | UNSUPPORTED | tested: `import notebook` and `import ipywidgets` both fail in the campusx env; environment.yml lists only jupyterlab |
| 12-setup-anaconda-jupyter-colab | "Because Markdown cells accept HTML" | UNSUPPORTED | sourced: Jupyter Notebook docs, Markdown Cells |
| 12-setup-anaconda-jupyter-colab | "A TPU is Google's chip built only for that maths" | UNSUPPORTED | sourced: Jouppi et al., ISCA 2017 |
| 12-setup-anaconda-jupyter-colab | "Classic ML code (scikit-learn) does not use a GPU" | UNSUPPORTED | sourced: scikit-learn FAQ, "Will you add GPU support?" |
| 12-setup-anaconda-jupyter-colab | "Kaggle ... limited number of free hours per week" | UNSUPPORTED | sourced: Kaggle docs, TPUs page (30 GPU h, 20 TPU h per week) |
| 12-setup-anaconda-jupyter-colab | "at most about 12 hours ... the machine is wiped" | UNSUPPORTED | sourced: Google Colab FAQ (12-hour limit; VMs deleted when idle or at max lifetime) |
| 12-setup-anaconda-jupyter-colab | "kaggle.json is a password" | UNSUPPORTED | sourced: Kaggle API README, API credentials |
| 12-setup-anaconda-jupyter-colab | "pandas 3 stores text columns in ... Arrow arrays that the library cannot add up" | UNSUPPORTED | tested: full ProfileReport on titanic_train.csv fails with AttributeError 'ArrowExtensionArray' has no attribute 'sum' under default storage, succeeds with string_storage='python'; result added |
| 13-toy-project | "This mistake is called data leakage" | UNSUPPORTED | sourced: scikit-learn User Guide, Common pitfalls, Data leakage; Kaufman, Rosset and Perlich, ACM TKDD 6(4), 2012 |
| 13-toy-project | "a website that passes it raw CGPA and IQ values would get wrong answers" | UNSUPPORTED | tested: new Notebook cell; raw test rows give "placed" for all 10, accuracy 40% vs 90% scaled; result added to Note |
| 13-toy-project | "AWS and Google Cloud still offer limited free tiers" / Heroku free plan ended Nov 2022 | UNSUPPORTED | sourced: Heroku Dev Center changelog 2022; aws.amazon.com/free; cloud.google.com/free |
| 14-framing-ml-problem | "Netflix does not publish its churn rate ... Outside estimates exist" | UNSUPPORTED | sourced: E. Shapiro, Media War & Peace, "Churn, Baby, Churn" 2023; Antenna estimates (5.1% Nov 2022, 6.3% Nov 2023) via Shapiro |
| 14-framing-ml-problem | "Most classifiers ... can output a probability for each class" | UNSUPPORTED | sourced: Hastie, Tibshirani and Friedman, ESL 2nd ed. 2009, Sec. 4.4; scikit-learn predict_proba |
| 15-working-with-csv | "The official pandas documentation lists about fifty" (parameters) | WRONG FACT | tested: inspect.signature(pd.read_csv) has 44 parameters in pandas 3.0.6; corrected |
| 15-working-with-csv | "shows up as Cafí©... because the file's text was already garbled before it was saved" | UNSUPPORTED | tested: the file holds bytes ED A9 (neither latin-1 E9 nor UTF-8 C3 A9); cp1252 also fails; evidence added; latin-1 fact sourced to Python codecs docs |
| 15-working-with-csv | "replaced by on_bad_lines in pandas 1.3 and removed in pandas 2" | UNSUPPORTED | sourced: pandas What's new 1.3.0 and 2.0.0; tested: TypeError in 3.0.6 |
| 15-working-with-csv | "So was the date_parser parameter" (deprecated in 2.2) | WRONG FACT | sourced: pandas What's new 2.0.0 (date_parser deprecated in 2.0), 2.2.0, 3.0.0; corrected |
| 16-working-with-json-and-sql | "Current pandas (3.0) treats any text as a file name and fails" | UNSUPPORTED | sourced: pandas What's new 2.1.0 (deprecation); tested: FileNotFoundError in 3.0.6 |
| 16-working-with-json-and-sql | "mysql-connector 2.2.9, an old version from 2019 that is no longer maintained" | UNSUPPORTED | sourced: PyPI (2.2.9 released 2019-04-01); "no longer maintained" dropped |
| 16-working-with-json-and-sql | "pandas shows a warning that it only fully supports SQLite and SQLAlchemy" | UNSUPPORTED | sourced: pandas docs, read_sql (DBAPI2: only sqlite3 supported) |
| 17-fetching-data-from-api | "pandas 2.0 removed DataFrame.append" | UNSUPPORTED | sourced: pandas What's new 2.0.0 |
| 17-fetching-data-from-api | "TVmaze allows about 20 requests every 10 seconds ... about 380 pages" | UNSUPPORTED | sourced: TVmaze API docs ("at least 20 calls every 10 seconds"); tested: page 378 returns 200, page 380 returns 404 |
| 17-fetching-data-from-api | "Each page holds up to 250 shows (page 0 has 240)" | UNSUPPORTED | sourced: TVmaze API docs; tested: saved page 0 has 240 shows |
| 17-fetching-data-from-api | "TMDB ... asks to be credited as the data source" | UNSUPPORTED | sourced: TMDB API FAQ |
| 18-web-scraping | "robots.txt cannot block anyone; it is a request that polite bots ... follow" | UNSUPPORTED | sourced: RFC 9309 (2022), "not a form of access authorization" |
| 18-web-scraping | "lxml is faster ... in a plain Python setup it needs pip install lxml" | UNSUPPORTED | sourced: Beautiful Soup docs, Installing a parser; tested: `import lxml` fails in the campusx env |
| 18-web-scraping | "DataFrame.append was removed in pandas 2.0" | UNSUPPORTED | sourced: pandas What's new 2.0.0 |
| 19-understanding-your-data | "divides by n - 1 ... corrects for the fact that a sample tends to look a little less spread out" | UNSUPPORTED | sourced: linked to Note 222, Sec. 4.3, which derives it (MATH) |
| 19-understanding-your-data | "From pandas 2 on, [df.corr()] raises ValueError" | UNSUPPORTED | sourced: pandas What's new 2.0.0 (numeric_only defaults to False); tested: ValueError on titanic_train.csv |
| 20-univariate-analysis | "our eyes compare bar heights much better than angles" | UNSUPPORTED | sourced: Cleveland and McGill, JASA 79(387), 1984 |
| 21-bivariate-multivariate-analysis | "They were probably helped into the lifeboats first" | UNSUPPORTED | sourced: Frey, Savage and Torgler, J. Econ. Perspectives 25(1), 2011 ("women and children first") |
| 21-bivariate-multivariate-analysis | "The port itself probably did not save anyone: it stands in for class and sex" | UNSUPPORTED | tested: survival by port within class and sex; gap mostly shrinks (1st-class women 98% vs 96%, men 40% vs 35%) but not for 3rd-class women (65% vs 38%); numbers added |
| 21-bivariate-multivariate-analysis | "by default, with 95% confidence ... seaborn draws these lines by default" | UNSUPPORTED | sourced: seaborn barplot docs, errorbar=("ci", 95) |
| 21-bivariate-multivariate-analysis | "distplot has been deprecated since seaborn 0.11 and is being removed" | UNSUPPORTED | sourced: seaborn v0.11.0 release notes; "is being removed" dropped |
| 21-bivariate-multivariate-analysis | "A KDE curve is built by placing a small bell-shaped bump on every data value" | UNSUPPORTED | sourced: Silverman 1986, Ch. 2 |
| 21-bivariate-multivariate-analysis | "groupby(...).mean() ... In pandas 2 and later this raises an error" | UNSUPPORTED | sourced: pandas What's new 2.0.0; tested: TypeError in 3.0.6 |
| 21-bivariate-multivariate-analysis | "seaborn ... stores month as an ordered category" | WRONG FACT | sourced: seaborn load_dataset source (pd.Categorical in calendar order, not ordered=True); corrected |
| 22-pandas-profiling | "began as pandas-profiling ... 2023 ydata-profiling ... 2026 fg-data-profiling ... import ydata_profiling warns" | UNSUPPORTED | sourced: PyPI project pages (ydata 4.0.0 Jan 2023, fg 4.19.0 Apr 2026, pandas-profiling 3.6.6 "Deprecated"); tested: ydata_profiling/__init__.py warning text |
| 22-pandas-profiling | "Spearman's and Kendall's coefficients ... compare the ranks" | UNSUPPORTED | sourced: Spearman 1904; Kendall 1938 |
| 22-pandas-profiling | "Cramér's V ... from 0 to 1" | UNSUPPORTED | sourced: Cramér 1946 |
| 22-pandas-profiling | "Phik works for any mix of numerical and categorical columns" | UNSUPPORTED | sourced: Baak et al., CSDA 152, 2020 |
| 22-pandas-profiling | "Auto heatmap picks Spearman ... Cramér's V ... every pair above 0.5 gets an alert" | UNSUPPORTED | tested: library source (correlations_pandas.py uses Spearman/Cramér; config.py default threshold 0.5); saved report has the alerts |
| 24-standardization | "sag ... gives up after 100 steps; on the raw data it has not reached the best answer by then, which gives the 65.8%" | WRONG FACT | tested: with max_iter=100,000, sag stops at about 9,800 steps, weights stay near 0, every user predicted "not purchased", accuracy = 65.8% = share of non-buyers; sourced: scikit-learn LogisticRegression docs (sag fast only with similarly scaled features); Notebook cell added, Extra rewritten |
| 24-standardization | "StandardScaler divides by n" | UNSUPPORTED | sourced: scikit-learn StandardScaler docs (ddof=0) |
| 25-normalization | "wine dataset ... from the UCI repository ... built into scikit-learn as load_wine" | UNSUPPORTED | sourced: scikit-learn load_wine docs |
| 25-normalization | "Max-abs scaling ... keeps sparse data sparse; min-max or standardization would destroy that" | UNSUPPORTED | sourced: scikit-learn User Guide, Scaling sparse data |
| 27-one-hot-encoding | "Tree-based models ... and K-nearest neighbours work fine with all n columns" | UNSUPPORTED | sourced: Kuhn and Johnson 2019, Feature Engineering and Selection, Sec. 5.1 |
| 27-one-hot-encoding | "renamed sparse_output in version 1.2, and the old name no longer works" | UNSUPPORTED | sourced: scikit-learn 1.2 release notes (removal in 1.4); tested: TypeError in 1.9.1 |
| 27-one-hot-encoding | "the unknown car is silently treated as CNG" | WRONG FACT | tested: scikit-learn 1.9.1 emits a UserWarning; "silently" corrected |
| 29-pipelines | "The diagram has been the default since version 1.1" | UNSUPPORTED | sourced: scikit-learn 1.1 release notes |
| 29-pipelines | "chi2 ... only works on values of 0 or more" | UNSUPPORTED | sourced: scikit-learn chi2 docs |
| 29-pipelines | "Preprocessing the whole training set first ... would let the test part leak" | UNSUPPORTED | sourced: scikit-learn User Guide, Common pitfalls |
| 29-pipelines | "joblib ... handles large NumPy arrays better ... same scikit-learn version" | UNSUPPORTED | sourced: scikit-learn User Guide, Model persistence |
| 30-function-transformer | "The decision tree changed by about one point, which is within its usual run-to-run noise" | UNSUPPORTED | tested: 20 tree seeds on the same split give 64.8% to 68.7%; range added |
| 31-power-transformer | "published it in 1964, George Box and David Cox" | UNSUPPORTED | sourced: Box and Cox, JRSS B 26(2), 1964 |
| 31-power-transformer | "published by In-Kwon Yeo and Richard Johnson in 2000" | UNSUPPORTED | sourced: Yeo and Johnson, Biometrika 87(4), 2000 |
| 31-power-transformer | "scikit-learn uses maximum likelihood" | UNSUPPORTED | sourced: scikit-learn PowerTransformer docs |
| 31-power-transformer | "Concrete Compressive Strength dataset by I-Cheng Yeh" | UNSUPPORTED | sourced: Yeh, Cement and Concrete Research 28(12), 1998 |
| 32-binning-binarization | "Binning still changes where those cuts can go ... Linear models can gain more" (why binning helped the tree) | UNSUPPORTED | sourced: scikit-learn example "Using KBinsDiscretizer to discretize continuous features" (linear model more flexible, tree less flexible) |
| 32-binning-binarization | KBinsDiscretizer details (quantile_method 1.7/1.9, subsample, kmeans init) | UNSUPPORTED | sourced: scikit-learn KBinsDiscretizer docs; tested: kmeans init from uniform-edge midpoints in sklearn source |
| 34-date-and-time | "Since pandas 3, text is parsed at microsecond resolution" | UNSUPPORTED | sourced: pandas What's new 3.0.0; tested: dtype datetime64[us] |
| 34-date-and-time | "Since pandas 2 it guesses one format from the first value" | UNSUPPORTED | sourced: pandas What's new 2.0.0; tested: "10/12/2019" read as 12 Oct, mixed list raises ValueError |
| 34-date-and-time | "ISO calendar: week 1 contains the year's first Thursday" | UNSUPPORTED | sourced: ISO 8601; tested: 29 Dec 2019 week 52, 30 Dec 2019 week 1 of 2020 |

## UNRESOLVED (removed from Note)

| Note | Removed text | Why |
|---|---|---|
| 21-bivariate-multivariate-analysis | "Older people were more likely to afford the expensive tickets." | removed: no source; in the Note data Age and Fare correlate only 0.10, so the data does not back it |

## Counts per Note

| Note | UNSUPPORTED | WRONG CITATION | WRONG FACT | Total |
|---|---|---|---|---|
| 01-course-map | 1 | 0 | 1 | 2 |
| 01-what-is-ml | 6 | 0 | 0 | 6 |
| 02-ai-vs-ml-vs-dl | 1 | 0 | 1 | 2 |
| 03-types-of-ml | 1 | 0 | 1 | 2 |
| 04-batch-learning | 2 | 0 | 0 | 2 |
| 05-online-learning | 0 | 0 | 0 | 0 |
| 06-instance-vs-model-based | 3 | 0 | 0 | 3 |
| 07-challenges-in-ml | 2 | 0 | 0 | 2 |
| 08-applications-of-ml | 4 | 0 | 0 | 4 |
| 09-mldlc | 9 | 0 | 1 | 10 |
| 11-tensors | 4 | 0 | 0 | 4 |
| 12-setup-anaconda-jupyter-colab | 11 | 0 | 0 | 11 |
| 13-toy-project | 3 | 0 | 0 | 3 |
| 14-framing-ml-problem | 2 | 0 | 0 | 2 |
| 15-working-with-csv | 2 | 0 | 2 | 4 |
| 16-working-with-json-and-sql | 3 | 0 | 0 | 3 |
| 17-fetching-data-from-api | 4 | 0 | 0 | 4 |
| 18-web-scraping | 3 | 0 | 0 | 3 |
| 19-understanding-your-data | 2 | 0 | 0 | 2 |
| 20-univariate-analysis | 1 | 0 | 0 | 1 |
| 21-bivariate-multivariate-analysis | 6 | 0 | 1 | 7 |
| 22-pandas-profiling | 5 | 0 | 0 | 5 |
| 23-what-is-feature-engineering | 0 | 0 | 0 | 0 |
| 24-standardization | 1 | 0 | 1 | 2 |
| 25-normalization | 2 | 0 | 0 | 2 |
| 26-ordinal-label-encoding | 0 | 0 | 0 | 0 |
| 27-one-hot-encoding | 2 | 0 | 1 | 3 |
| 28-column-transformer | 0 | 0 | 0 | 0 |
| 29-pipelines | 4 | 0 | 0 | 4 |
| 30-function-transformer | 1 | 0 | 0 | 1 |
| 31-power-transformer | 4 | 0 | 0 | 4 |
| 32-binning-binarization | 2 | 0 | 0 | 2 |
| 33-mixed-variables | 0 | 0 | 0 | 0 |
| 34-date-and-time | 3 | 0 | 0 | 3 |
| **Total** | 94 | 0 | 9 | 103 |

## Notes

- Notes with 0 findings were read against their transcripts; their extra claims (mostly library behaviour) were checked by running the code in the campusx env, so no edit was needed: 05, 23, 26, 28, 33.
- Every edited Note now uses short citation tags in the text and a `## Sources` list before Key terms, and was rebuilt with `tools/build.sh` ("Built").
- Notebooks changed: 13-toy-project (new cell: model on unscaled inputs), 24-standardization (new cell: sag with 100,000 allowed steps). Both re-executed on CPU.
- 17-fetching-data-from-api: one f-string sentence reworded only so the PDF text check passes (not a claim finding).
- 01-course-map: two findings are in `course_map/algorithm_chooser.tex`, which this audit may not touch; they are left for the course-map owner.
- 19-understanding-your-data: "every algorithm ... gets faster" after shrinking dtypes is said in the lecture, so left as is (TRANSCRIPT), although scikit-learn converts most inputs to float64 anyway.
