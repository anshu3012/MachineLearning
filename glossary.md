# Glossary

Every ML term in the notes, in plain English, with the Note that first explains it.

| Term | Meaning | First explained |
|---|---|---|
| `find`, `find_all` | Return the first matching tag, or a list of all matching tags. | [Video 18](18-web-scraping/note.md) |
| `ignore_index` | Setting of `pd.concat` that renumbers the joined rows from 0. | [Video 17](17-fetching-data-from-api/note.md) |
| `json_normalize` | pandas function that turns nested JSON into flat columns. | [Video 17](17-fetching-data-from-api/note.md) |
| `pd.concat` | pandas function that joins several DataFrames into one. | [Video 17](17-fetching-data-from-api/note.md) |
| `read_json` | pandas function that reads JSON from a file or a URL into a DataFrame. | [Video 16](16-working-with-json-and-sql/note.md) |
| `read_sql_query` | pandas function that runs an SQL query and returns a DataFrame. | [Video 16](16-working-with-json-and-sql/note.md) |
| Accuracy | The fraction of predictions that are correct. | [Video 13](13-toy-project/note.md) |
| Agent | The learner in reinforcement learning. | [Video 3](03-types-of-ml/note.md) |
| AGI (artificial general intelligence) | A machine with all the abilities of human intelligence. Does not exist yet. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Anomaly detection | Finding rows that do not fit the pattern of the rest. | [Video 3](03-types-of-ml/note.md) |
| API (Application Programming Interface) | A way for two programs to talk; a website's API hands out its data on request. | [Video 17](17-fetching-data-from-api/note.md) |
| API key | A secret code that tells the API who is asking. | [Video 17](17-fetching-data-from-api/note.md) |
| API | A service that returns data when our code asks for it. | [Video 7](07-challenges-in-ml/note.md) |
| Array | The programming name for a tensor (as in NumPy). | [Video 11](11-tensors/note.md) |
| Artificial Intelligence (AI) | The field of building machines that show intelligence. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Association rule learning | Finding items that tend to occur together. | [Video 3](03-types-of-ml/note.md) |
| Attribute | A `name="value"` setting inside an opening tag. | [Video 18](18-web-scraping/note.md) |
| Axis | One direction along which a tensor's items are arranged. | [Video 11](11-tensors/note.md) |
| Backward elimination | Feature selection that starts with all columns and removes the worst at a time. | [Video 46](46-curse-of-dimensionality/note.md) |
| Bar plot | One bar per category, its height the mean of a numerical column. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Batch learning | Training on the whole dataset at once, offline, then deploying. | [Video 4](04-batch-learning/note.md) |
| BeautifulSoup | Python library that parses HTML into a searchable tree. | [Video 18](18-web-scraping/note.md) |
| Biased model | A model pushed towards wrong answers, e.g. by bad data. | [Video 5](05-online-learning/note.md) |
| Bin | One of the equal ranges a histogram splits the data into. | [Video 20](20-univariate-analysis/note.md) |
| Bivariate analysis | Studying two variables together. | [Video 20](20-univariate-analysis/note.md) |
| BMI | Body mass index: weight (kg) divided by height (m) squared. | [Video 7](07-challenges-in-ml/note.md) |
| Bot | A program that visits websites automatically. | [Video 18](18-web-scraping/note.md) |
| Box plot | A graph of the five-number summary, with outliers drawn as dots. | [Video 20](20-univariate-analysis/note.md) |
| Categorical data | Data made of categories. | [Video 3](03-types-of-ml/note.md) |
| Category | One of the fixed groups of a categorical column. | [Video 20](20-univariate-analysis/note.md) |
| Channel | One colour layer of an image (red, green or blue). | [Video 11](11-tensors/note.md) |
| Chunk | A piece of a file, read as a small DataFrame. | [Video 15](15-working-with-csv/note.md) |
| Class | An attribute that labels tags; used to select the right ones. | [Video 18](18-web-scraping/note.md) |
| Classification | Supervised learning with a categorical output. | [Video 3](03-types-of-ml/note.md) |
| Client, server | The program that asks, and the computer that answers. | [Video 17](17-fetching-data-from-api/note.md) |
| Cluster | One group found by clustering. | [Video 3](03-types-of-ml/note.md) |
| Clustering | Splitting data into groups of similar rows. | [Video 3](03-types-of-ml/note.md) |
| Clustermap | A heatmap with rows and columns reordered so similar ones sit together. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Compression | Storing data in less space. | [Video 11](11-tensors/note.md) |
| Confidence interval | A range in which the true mean most likely lies. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Connection object | The open link to a database (`conn`) that queries go through. | [Video 16](16-working-with-json-and-sql/note.md) |
| Connector | A library that lets Python talk to a database. | [Video 16](16-working-with-json-and-sql/note.md) |
| Container | A tag (often a `div`) that holds everything about one item, such as one company. | [Video 18](18-web-scraping/note.md) |
| Correlation | How two columns move together, from -1 to +1. | [Video 19](19-understanding-your-data/note.md) |
| Count plot | A bar chart with one bar per category, as tall as its frequency. | [Video 20](20-univariate-analysis/note.md) |
| Crosstab | A table counting the rows for every pair of categories of two columns. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| CSV file | A text file holding a table, with commas between values. | [Video 13](13-toy-project/note.md) |
| Curse of dimensionality | The problems that appear when data has too many dimensions: lower performance and more computation. | [Video 46](46-curse-of-dimensionality/note.md) |
| Data cleaning | Fixing errors, gaps and inconsistencies in data. | [Video 7](07-challenges-in-ml/note.md) |
| Data leakage | Information from the test set leaking into training. | [Video 13](13-toy-project/note.md) |
| Data pipeline | A channel that carries data from one point to another. | [Video 17](17-fetching-data-from-api/note.md) |
| Data type (dtype) | The kind of values a column holds, such as `int64`, `float64` or `str`. | [Video 19](19-understanding-your-data/note.md) |
| Database server | A program that holds databases and answers queries, such as MySQL. | [Video 16](16-working-with-json-and-sql/note.md) |
| Database | A program that stores data as tables and answers queries. | [Video 16](16-working-with-json-and-sql/note.md) |
| Decision boundary | A line or curve that separates the classes in classification. | [Video 6](06-instance-vs-model-based/note.md) |
| Deep Learning (DL) | Machine Learning that uses neural networks with many layers; finds features by itself. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Dendrogram | A tree showing which rows (or columns) were joined as similar, and in what order. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Density plot | A histogram with a smooth KDE curve on top. | [Video 20](20-univariate-analysis/note.md) |
| Dependent variable | The output column (y). | [Video 13](13-toy-project/note.md) |
| Deploy | Move a model from development to production. | [Video 4](04-batch-learning/note.md) |
| Deployment | Putting a model on a server so users can reach it. | [Video 7](07-challenges-in-ml/note.md) |
| Descriptive statistics | Numbers that summarise data, such as count, mean, spread and percentiles. | [Video 19](19-understanding-your-data/note.md) |
| Development environment | Our own machine, where we build and train a model. | [Video 4](04-batch-learning/note.md) |
| Dimension | One input column. | [Video 3](03-types-of-ml/note.md) |
| Dimensionality reduction | Reducing the number of input columns while keeping the information. | [Video 3](03-types-of-ml/note.md) |
| Distance | A number measuring how far apart two points are; small distance = similar. | [Video 6](06-instance-vs-model-based/note.md) |
| Distribution | How a column's values spread over their range. | [Video 20](20-univariate-analysis/note.md) |
| dtype | The data type of a column, such as `int64`, `float64` or `str`. | [Video 15](15-working-with-csv/note.md) |
| Duplicate row | A row identical to another row in every column. | [Video 19](19-understanding-your-data/note.md) |
| Eager learning | Another name for model-based learning: all the work done up front. | [Video 6](06-instance-vs-model-based/note.md) |
| Encoding | The rulebook that maps text characters to stored bytes. | [Video 15](15-working-with-csv/note.md) |
| Endpoint | One address of an API that returns one kind of data. | [Video 17](17-fetching-data-from-api/note.md) |
| Environment variable | A named value stored on the computer, outside the code, read with `os.environ`. | [Video 17](17-fetching-data-from-api/note.md) |
| Environment | The world the agent acts in. | [Video 3](03-types-of-ml/note.md) |
| Expert system | Early AI: a human expert's knowledge written as rules, plus a program that applies them. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Explicit programming | A human writing out every rule the computer follows. ML avoids it. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Exploratory data analysis (EDA) | Exploring data with summaries and plots to find patterns. | [Video 13](13-toy-project/note.md) |
| f-string | Text starting with `f` in which `{name}` is replaced by a value. | [Video 17](17-fetching-data-from-api/note.md) |
| Feature engineering | Choosing, removing and creating features. | [Video 7](07-challenges-in-ml/note.md) |
| Feature extraction | Creating a new column from existing ones. | [Video 3](03-types-of-ml/note.md) |
| Feature scaling | Putting columns on the same scale, so no column dominates distances. | [Video 6](06-instance-vs-model-based/note.md) |
| Feature selection | Choosing which input columns to use. | [Video 13](13-toy-project/note.md) |
| Feature | One piece of information about each example that a model uses (e.g. a student's CGPA). | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Fence | A limit 1.5 IQR beyond the box; values past it are possible outliers. | [Video 20](20-univariate-analysis/note.md) |
| Five-number summary | Minimum, Q1, median, Q3 and maximum. | [Video 20](20-univariate-analysis/note.md) |
| For loop | Code that repeats once for each item of a collection. | [Video 15](15-working-with-csv/note.md) |
| Forward selection | Feature selection that starts empty and adds the best column at a time. | [Video 46](46-curse-of-dimensionality/note.md) |
| Frame | One image in a video. | [Video 11](11-tensors/note.md) |
| Frequency | How many times a value or category occurs. | [Video 20](20-univariate-analysis/note.md) |
| Function, lambda | A named reusable piece of code (`def`), and a one-line unnamed one. | [Video 15](15-working-with-csv/note.md) |
| Garbage in, garbage out | Bad input data always gives bad results. | [Video 7](07-challenges-in-ml/note.md) |
| Good fit | Capturing the pattern while ignoring the noise. | [Video 7](07-challenges-in-ml/note.md) |
| Header | The line of a file that holds the column names. | [Video 15](15-working-with-csv/note.md) |
| Headers | Extra information sent with a request, such as the User-Agent. | [Video 18](18-web-scraping/note.md) |
| Heatmap | A table drawn as coloured cells, darker for larger values. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| High-dimensional data | Data with a very large number of columns. | [Video 46](46-curse-of-dimensionality/note.md) |
| Histogram | A bar chart of how many values fall in each equal range (bin) of a numerical column. | [Video 20](20-univariate-analysis/note.md) |
| HTML | The language web pages are written in: a tree of nested tags. | [Video 18](18-web-scraping/note.md) |
| Hue, style, size | Plot settings that show an extra column by colour, marker shape or dot size. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Incremental learning | Training on small pieces of data over time (the opposite of batch). | [Video 4](04-batch-learning/note.md) |
| Incremental training | Training in small steps, keeping what was learned before. | [Video 5](05-online-learning/note.md) |
| Independent variables | The input columns (X). | [Video 13](13-toy-project/note.md) |
| Index | The row labels of a DataFrame. | [Video 15](15-working-with-csv/note.md) |
| Inference engine | The part of an expert system that applies the rules to answer a question. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Input / output | The columns we know / the column we want to predict. | [Video 3](03-types-of-ml/note.md) |
| Inspect | Browser tool that shows which tag draws each part of a page. | [Video 18](18-web-scraping/note.md) |
| Instance-based learning | Learning by storing the training data and comparing new points with it. | [Video 6](06-instance-vs-model-based/note.md) |
| Interquartile range (IQR) | Q3 - Q1: the width of the middle half of the data. | [Video 20](20-univariate-analysis/note.md) |
| JSON (JavaScript Object Notation) | A plain-text data format of objects and arrays that almost every language can read. | [Video 16](16-working-with-json-and-sql/note.md) |
| JSON Lines | A JSON file with one object per line, read with `lines=True`. | [Video 16](16-working-with-json-and-sql/note.md) |
| JSON viewer | A tool that lays out JSON text as a tree to show its structure. | [Video 17](17-fetching-data-from-api/note.md) |
| K-nearest neighbours (KNN) | Predicting from the answers of the k closest stored points. | [Video 6](06-instance-vs-model-based/note.md) |
| Kaggle | A website for sharing datasets and notebooks and for ML competitions. | [Video 17](17-fetching-data-from-api/note.md) |
| KDE plot | A smooth estimate of a column's PDF, built from the data. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Kernel density estimate (KDE) | A smooth curve that estimates a column's distribution from its values. | [Video 20](20-univariate-analysis/note.md) |
| Knowledge base | The collection of rules inside an expert system. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Labelled data | Data that includes the output column. | [Video 3](03-types-of-ml/note.md) |
| Layer | One step in a neural network; each layer builds on what the previous one found. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Lazy learning | Another name for instance-based learning: no work until a question arrives. | [Video 6](06-instance-vs-model-based/note.md) |
| Learning rate | How strongly each new piece of data changes the model. | [Video 5](05-online-learning/note.md) |
| Learning | Finding rules (patterns) from examples. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Line plot | A scatter plot with the dots joined in order, used when x is time. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Linear relationship | A relationship between two columns that follows a straight line. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| List, dictionary | Python's ordered collection `[...]`, and its `key: value` pairs `{...}`. | [Video 15](15-working-with-csv/note.md) |
| Logistic regression | A classification algorithm that finds a separating boundary. | [Video 13](13-toy-project/note.md) |
| Machine Learning (ML) | Using statistics to let a machine find patterns (rules) in data by itself. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Matrix | A table of numbers: a 2D tensor. | [Video 11](11-tensors/note.md) |
| Mean absolute deviation | The average absolute distance of the points from their mean. | [Video 47](47-pca-geometric-intuition/note.md) |
| Mean | The average of the values; the centre of the data. | [Video 47](47-pca-geometric-intuition/note.md) |
| Median | The middle value of sorted data; the 50% percentile. | [Video 19](19-understanding-your-data/note.md) |
| Mini-batch | A small group of data points used for one training step. | [Video 5](05-online-learning/note.md) |
| Missing value | An empty entry, shown by pandas as `NaN`. | [Video 15](15-working-with-csv/note.md) |
| Missing values | Empty cells in the data. | [Video 7](07-challenges-in-ml/note.md) |
| MLOps | Running and maintaining ML models in production. | [Video 7](07-challenges-in-ml/note.md) |
| Model drift / concept drift | A model's accuracy dropping as the real world changes. | [Video 4](04-batch-learning/note.md) |
| Model selection | Training several algorithms and keeping the best. | [Video 13](13-toy-project/note.md) |
| Model-based learning | Learning a mathematical function from the data and predicting with it. | [Video 6](06-instance-vs-model-based/note.md) |
| Multivariate analysis | Studying more than two variables together. | [Video 20](20-univariate-analysis/note.md) |
| Narrow AI | AI that does one specific task. All AI today is narrow. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Neural network | The model DL uses, loosely inspired by neurons in the brain. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Non-null | Not missing. | [Video 19](19-understanding-your-data/note.md) |
| Normal distribution | A symmetric, bell-shaped distribution. | [Video 20](20-univariate-analysis/note.md) |
| Numerical data | Data made of numbers. | [Video 3](03-types-of-ml/note.md) |
| Offline learning | Another name for batch learning. | [Video 4](04-batch-learning/note.md) |
| One-hot encoding | Representing each word or category by a vector with a single 1. | [Video 11](11-tensors/note.md) |
| Online learning | Training incrementally on mini-batches while the model is live in production. | [Video 5](05-online-learning/note.md) |
| Optimal number of features | The number of columns at which a model performs best. | [Video 46](46-curse-of-dimensionality/note.md) |
| Out-of-core learning | Training on data too big for memory by feeding it in chunks, offline. | [Video 5](05-online-learning/note.md) |
| Outlier | A value far from the rest of the data. | [Video 20](20-univariate-analysis/note.md) |
| Outliers | Values far from the rest, often mistakes. | [Video 7](07-challenges-in-ml/note.md) |
| Overfitting | Learning the training data too closely, noise included; fails on new data. | [Video 7](07-challenges-in-ml/note.md) |
| Pair plot | A grid of scatter plots of every pair of numerical columns, with histograms on the diagonal. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| pandas, DataFrame | Python's main table library, and its name for a table. | [Video 13](13-toy-project/note.md) |
| Parameter | A named setting passed to a function, like `sep=";"`. | [Video 15](15-working-with-csv/note.md) |
| Parameters | The numbers that describe a learned model, e.g. slope and intercept. | [Video 6](06-instance-vs-model-based/note.md) |
| Parse, parser | Read text and build a structure from it; the part that does this. | [Video 18](18-web-scraping/note.md) |
| Parser | The part of a program that reads text and splits it into pieces. | [Video 15](15-working-with-csv/note.md) |
| partial_fit | A scikit-learn method that continues training from where the model left off. | [Video 5](05-online-learning/note.md) |
| PCA | Principal component analysis, a dimensionality reduction technique. | [Video 3](03-types-of-ml/note.md) |
| Pearson correlation coefficient | The usual measure of correlation, written $r$; the one `df.corr()` computes. | [Video 19](19-understanding-your-data/note.md) |
| Percentile | The value below which a given share of the data lies. | [Video 19](19-understanding-your-data/note.md) |
| Perceptron | The smallest building block of a neural network; one artificial neuron. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| phpMyAdmin | A web page for creating and managing MySQL databases. | [Video 16](16-working-with-json-and-sql/note.md) |
| pickle | A Python module that saves objects to a file and loads them back. | [Video 13](13-toy-project/note.md) |
| Pie chart | A circle split into slices sized by each category's share. | [Video 20](20-univariate-analysis/note.md) |
| Pipeline | One object that bundles several processing steps and a model. | [Video 13](13-toy-project/note.md) |
| Pivot table | A grid with one column's values as rows, another's as columns, and a third in the cells. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Pixel | One dot of an image, stored as one or more numbers. | [Video 11](11-tensors/note.md) |
| Policy | The agent's rules for which action to take. | [Video 3](03-types-of-ml/note.md) |
| Predict | Use a trained model to give an answer for new data it has not seen. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Preprocessing | Cleaning and preparing data before training. | [Video 13](13-toy-project/note.md) |
| Principal component analysis (PCA) | An unsupervised feature extraction technique that builds new columns along the directions of greatest variance. | [Video 47](47-pca-geometric-intuition/note.md) |
| Principal component | A new axis found by PCA; PC1 holds the most variance, PC2 the next most. | [Video 47](47-pca-geometric-intuition/note.md) |
| Probability density function (PDF) | A curve showing how likely each value is; areas under it are probabilities. | [Video 20](20-univariate-analysis/note.md) |
| Production environment | The server where a model serves real users. | [Video 4](04-batch-learning/note.md) |
| Projection | Dropping each point onto an axis or line, like casting a shadow. | [Video 47](47-pca-geometric-intuition/note.md) |
| Quartiles | The 25%, 50% and 75% percentiles, which cut the data into four equal groups. | [Video 19](19-understanding-your-data/note.md) |
| Query parameters | Settings after the `?` in a URL, joined by `&`, such as `page=1`. | [Video 17](17-fetching-data-from-api/note.md) |
| Query | A request for data, written in SQL. | [Video 16](16-working-with-json-and-sql/note.md) |
| Rank | The number of axes of a tensor (ndim in NumPy). | [Video 11](11-tensors/note.md) |
| RapidAPI | A website listing many APIs, including free ones. | [Video 17](17-fetching-data-from-api/note.md) |
| Rate limit | The most requests an API accepts in a given time. | [Video 17](17-fetching-data-from-api/note.md) |
| Reader | What `read_csv` returns with `chunksize`: it hands out one chunk at a time. | [Video 15](15-working-with-csv/note.md) |
| Recommendation engine | A model that suggests items, such as movies, to users. | [Video 4](04-batch-learning/note.md) |
| Regression | Supervised learning with a numerical output. | [Video 3](03-types-of-ml/note.md) |
| Reinforcement learning | Learning by acting and receiving rewards or punishments. | [Video 3](03-types-of-ml/note.md) |
| Relative path | A file's location, starting from the folder the code runs in. | [Video 15](15-working-with-csv/note.md) |
| Representative sample | A sample that reflects the whole situation fairly. | [Video 7](07-challenges-in-ml/note.md) |
| Request, response | What we send to a server, and what it sends back. | [Video 18](18-web-scraping/note.md) |
| requests | Python library that sends web requests. | [Video 17](17-fetching-data-from-api/note.md) |
| Response | What `requests.get` returns: the status code plus the reply. | [Video 17](17-fetching-data-from-api/note.md) |
| Retrain | Train a model again, here from scratch on old + new data. | [Video 4](04-batch-learning/note.md) |
| Reward / punishment | Good / bad feedback after an action. | [Video 3](03-types-of-ml/note.md) |
| River | A Python library for online machine learning. | [Video 5](05-online-learning/note.md) |
| robots.txt | A file at a site's root listing what bots are asked not to visit. | [Video 18](18-web-scraping/note.md) |
| Rollback | Restoring a model to an earlier, good version. | [Video 5](05-online-learning/note.md) |
| Sample | The part of the real world that our data covers. | [Video 7](07-challenges-in-ml/note.md) |
| Sampling bias | An unrepresentative sample caused by how the data was collected. | [Video 7](07-challenges-in-ml/note.md) |
| Sampling noise | An unrepresentative sample caused by being too small. | [Video 7](07-challenges-in-ml/note.md) |
| Scalar | A single number: a 0D tensor. | [Video 11](11-tensors/note.md) |
| Scaling | Bringing input columns to similar ranges. | [Video 13](13-toy-project/note.md) |
| Scatter plot | One dot per row, with one numerical column on each axis. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| scikit-learn | Python's main library for classical ML. | [Video 13](13-toy-project/note.md) |
| Semi-supervised learning | Learning from a few labelled rows and many unlabelled ones. | [Video 3](03-types-of-ml/note.md) |
| Separator | The character between values on a line, such as `,` or a tab. | [Video 15](15-working-with-csv/note.md) |
| Sequential data | Data fed one piece after another, in order. | [Video 5](05-online-learning/note.md) |
| Series | pandas' one-column structure: values with an index. | [Video 15](15-working-with-csv/note.md) |
| Server | A computer that is always on and that users reach over the internet. | [Video 4](04-batch-learning/note.md) |
| SGDRegressor | A scikit-learn model that does linear regression step by step. | [Video 5](05-online-learning/note.md) |
| Shape | The number of items along each axis. | [Video 11](11-tensors/note.md) |
| Similarity | How alike two data points are. | [Video 6](06-instance-vs-model-based/note.md) |
| Size | The total number of items: the product of the shape. | [Video 11](11-tensors/note.md) |
| Skewness | A number for how lopsided a distribution is: 0 symmetric, positive right tail, negative left tail. | [Video 20](20-univariate-analysis/note.md) |
| Software integration | Building a model into the software that users use. | [Video 7](07-challenges-in-ml/note.md) |
| Sparse data | Data where most of the space holds no points. | [Video 46](46-curse-of-dimensionality/note.md) |
| SQL (Structured Query Language) | The language for asking a database for data. | [Video 16](16-working-with-json-and-sql/note.md) |
| SQLAlchemy | A Python library that connects to many kinds of database; pandas supports it fully. | [Video 16](16-working-with-json-and-sql/note.md) |
| SQLite | A database stored in a single file, built into Python, needing no server. | [Video 16](16-working-with-json-and-sql/note.md) |
| Standard deviation | A measure of how spread out a column's values are. | [Video 13](13-toy-project/note.md) |
| Standardization | Scaling a column to mean 0 and standard deviation 1. | [Video 13](13-toy-project/note.md) |
| Static model | A model that learns nothing new after deployment. | [Video 4](04-batch-learning/note.md) |
| Status code | A number saying how a request went: 200 OK, 401, 404, 500. | [Video 17](17-fetching-data-from-api/note.md) |
| Supervised learning | Learning from data with inputs and outputs, to predict outputs. | [Video 3](03-types-of-ml/note.md) |
| Supervision | Correct answers that guide an algorithm while it learns. | [Video 3](03-types-of-ml/note.md) |
| Symbolic AI | Early AI where humans write the knowledge as rules. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Tag | One element of HTML, such as `<h2>TCS</h2>`. | [Video 18](18-web-scraping/note.md) |
| Target, label | Other names for the output column. | [Video 3](03-types-of-ml/note.md) |
| Tensor | A container of numbers arranged along one or more axes. | [Video 11](11-tensors/note.md) |
| Test set | The part hidden during training, used to check the model. | [Video 13](13-toy-project/note.md) |
| Time series | Data recorded at regular time intervals. | [Video 11](11-tensors/note.md) |
| Train | Let a model learn by making predictions, measuring its errors and adjusting to reduce them. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Train-test split | Dividing the data into training and test sets. | [Video 13](13-toy-project/note.md) |
| Training set | The part of the data the model learns from. | [Video 13](13-toy-project/note.md) |
| TSV file | Like a CSV file, with tabs between values. | [Video 15](15-working-with-csv/note.md) |
| Underfitting | Being too simple to capture the pattern; fails on all data. | [Video 7](07-challenges-in-ml/note.md) |
| Understanding the data | The project stage where we learn what is in the data before cleaning or modelling. | [Video 19](19-understanding-your-data/note.md) |
| Univariate analysis | Studying one variable on its own. | [Video 20](20-univariate-analysis/note.md) |
| Unreasonable effectiveness of data | With enough data, different algorithms perform about the same. | [Video 7](07-challenges-in-ml/note.md) |
| Unsupervised learning | Learning from inputs only, to find structure. | [Video 3](03-types-of-ml/note.md) |
| User-Agent | A short text a browser sends to say what it is. | [Video 15](15-working-with-csv/note.md) |
| UTF-8 | The most common encoding, and `read_csv`'s default. | [Video 15](15-working-with-csv/note.md) |
| Variable | One column of a dataset. | [Video 20](20-univariate-analysis/note.md) |
| Variance | The average squared distance of the points from their mean. | [Video 47](47-pca-geometric-intuition/note.md) |
| Vector | A list of numbers: a 1D tensor. | [Video 11](11-tensors/note.md) |
| Vectorization | Converting data such as text into vectors of numbers. | [Video 11](11-tensors/note.md) |
| View Page Source | Browser option that shows a page's raw HTML. | [Video 18](18-web-scraping/note.md) |
| Vocabulary | The list of unique words in a set of texts. | [Video 11](11-tensors/note.md) |
| Vowpal Wabbit | A fast learning library that supports online learning. | [Video 5](05-online-learning/note.md) |
| Wayback Machine | A web archive that keeps copies of web pages as they were. | [Video 18](18-web-scraping/note.md) |
| Web scraping | Writing code that extracts data from web pages. | [Video 7](07-challenges-in-ml/note.md) |
| X, y | Usual names for the input table and the output column. | [Video 11](11-tensors/note.md) |
| XAMPP | A free package that runs a web server and a MySQL server on one computer. | [Video 16](16-working-with-json-and-sql/note.md) |
