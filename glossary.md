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
| Absolute value | A number's size without its sign. | [Video 25](25-normalization/note.md) |
| Accuracy | The fraction of predictions that are correct. | [Video 13](13-toy-project/note.md) |
| Agent | The learner in reinforcement learning. | [Video 3](03-types-of-ml/note.md) |
| AGI (artificial general intelligence) | A machine with all the abilities of human intelligence. Does not exist yet. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Alert | A warning in the report about a column that may need attention. | [Video 22](22-pandas-profiling/note.md) |
| Anomaly detection | Finding rows that do not fit the pattern of the rest. | [Video 3](03-types-of-ml/note.md) |
| API (Application Programming Interface) | A way for two programs to talk; a website's API hands out its data on request. | [Video 17](17-fetching-data-from-api/note.md) |
| API key | A secret code that tells the API who is asking. | [Video 17](17-fetching-data-from-api/note.md) |
| API | A service that returns data when our code asks for it. | [Video 7](07-challenges-in-ml/note.md) |
| Array | The programming name for a tensor (as in NumPy). | [Video 11](11-tensors/note.md) |
| Artificial Intelligence (AI) | The field of building machines that show intelligence. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Association rule learning | Finding items that tend to occur together. | [Video 3](03-types-of-ml/note.md) |
| Attribute | A `name="value"` setting inside an opening tag. | [Video 18](18-web-scraping/note.md) |
| Average record size | The memory one row takes, on average. | [Video 22](22-pandas-profiling/note.md) |
| Axis | One direction along which a tensor's items are arranged. | [Video 11](11-tensors/note.md) |
| Backward elimination | Feature selection that starts with all columns and removes the worst at a time. | [Video 46](46-curse-of-dimensionality/note.md) |
| Bar plot | One bar per category, its height the mean of a numerical column. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Batch learning | Training on the whole dataset at once, offline, then deploying. | [Video 4](04-batch-learning/note.md) |
| BeautifulSoup | Python library that parses HTML into a searchable tree. | [Video 18](18-web-scraping/note.md) |
| Biased model | A model pushed towards wrong answers, e.g. by bad data. | [Video 5](05-online-learning/note.md) |
| Bin | One of the equal ranges a histogram splits the data into. | [Video 20](20-univariate-analysis/note.md) |
| Binning | Grouping a numerical column into ranges that act as categories. | [Video 23](23-what-is-feature-engineering/note.md) |
| Bivariate analysis | Studying two variables together. | [Video 20](20-univariate-analysis/note.md) |
| BMI | Body mass index: weight (kg) divided by height (m) squared. | [Video 7](07-challenges-in-ml/note.md) |
| Bot | A program that visits websites automatically. | [Video 18](18-web-scraping/note.md) |
| Box plot | A graph of the five-number summary, with outliers drawn as dots. | [Video 20](20-univariate-analysis/note.md) |
| Categorical column | A column whose values are labels rather than numbers. | [Video 23](23-what-is-feature-engineering/note.md) |
| Categorical data | Data made of categories. | [Video 3](03-types-of-ml/note.md) |
| categories_ | The attribute holding the categories `OrdinalEncoder` learned, in order. | [Video 26](26-ordinal-label-encoding/note.md) |
| Category | One of the fixed groups of a categorical column. | [Video 20](20-univariate-analysis/note.md) |
| Centred data | Data whose mean is 0. | [Video 25](25-normalization/note.md) |
| Channel | One colour layer of an image (red, green or blue). | [Video 11](11-tensors/note.md) |
| Chi-squared test (chi2) | A test scoring how strongly a column is linked to the target; needs values of 0 or more. | [Video 29](29-pipelines/note.md) |
| Chunk | A piece of a file, read as a small DataFrame. | [Video 15](15-working-with-csv/note.md) |
| Class | An attribute that labels tags; used to select the right ones. | [Video 18](18-web-scraping/note.md) |
| classes_ | The attribute holding the classes `LabelEncoder` learned, in order. | [Video 26](26-ordinal-label-encoding/note.md) |
| Classification | Supervised learning with a categorical output. | [Video 3](03-types-of-ml/note.md) |
| Client, server | The program that asks, and the computer that answers. | [Video 17](17-fetching-data-from-api/note.md) |
| Cluster | One group found by clustering. | [Video 3](03-types-of-ml/note.md) |
| Clustering | Splitting data into groups of similar rows. | [Video 3](03-types-of-ml/note.md) |
| Clustermap | A heatmap with rows and columns reordered so similar ones sit together. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Coefficient of variation (CV) | Standard deviation divided by mean: spread relative to the average. | [Video 22](22-pandas-profiling/note.md) |
| Column transformer | A scikit-learn class that applies different transformations to different columns at once (covered two Notes later). | [Video 26](26-ordinal-label-encoding/note.md) |
| ColumnTransformer | The scikit-learn class (in `sklearn.compose`) that implements the column transformer. | [Video 28](28-column-transformer/note.md) |
| components_ | The eigenvectors of the fitted PCA, one per row. | [Video 49](49-pca-mnist/note.md) |
| Compression | Storing data in less space. | [Video 11](11-tensors/note.md) |
| Confidence interval | A range in which the true mean most likely lies. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Connection object | The open link to a database (`conn`) that queries go through. | [Video 16](16-working-with-json-and-sql/note.md) |
| Connector | A library that lets Python talk to a database. | [Video 16](16-working-with-json-and-sql/note.md) |
| Container | A tag (often a `div`) that holds everything about one item, such as one company. | [Video 18](18-web-scraping/note.md) |
| Correlation | How two columns move together, from -1 to +1. | [Video 19](19-understanding-your-data/note.md) |
| Count plot | A bar chart with one bar per category, as tall as its frequency. | [Video 20](20-univariate-analysis/note.md) |
| Covariance matrix | A square table of all variances (diagonal) and covariances (off-diagonal) of the columns. | [Video 48](48-pca-step-by-step/note.md) |
| Covariance | How two columns move together: positive if they rise together, negative if not. | [Video 48](48-pca-step-by-step/note.md) |
| Cramér's V | A measure of the link between two categorical columns, from 0 to 1. | [Video 22](22-pandas-profiling/note.md) |
| Cross-validation | Testing a model by training and testing it several times on different parts of the training data. | [Video 29](29-pipelines/note.md) |
| Crosstab | A table counting the rows for every pair of categories of two columns. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| CSV file | A text file holding a table, with commas between values. | [Video 13](13-toy-project/note.md) |
| Cumulative explained variance | The share of the variance kept by the first k components together. | [Video 49](49-pca-mnist/note.md) |
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
| Dimensionality | The number of columns (features) in the data. | [Video 27](27-one-hot-encoding/note.md) |
| Distance | A number measuring how far apart two points are; small distance = similar. | [Video 6](06-instance-vs-model-based/note.md) |
| Distribution | How a column's values spread over their range. | [Video 20](20-univariate-analysis/note.md) |
| Domain knowledge | Knowledge of the field the data comes from. | [Video 23](23-what-is-feature-engineering/note.md) |
| Dot product | Multiply matching components of two vectors and add; $u^{\mathsf T}x$. | [Video 48](48-pca-step-by-step/note.md) |
| dtype | The data type of a column, such as `int64`, `float64` or `str`. | [Video 15](15-working-with-csv/note.md) |
| Dummy variable trap | The multicollinearity caused by keeping all $n$ dummy columns, which always add up to 1. | [Video 27](27-one-hot-encoding/note.md) |
| Dummy variable | One of the 0/1 columns created by one-hot encoding. | [Video 27](27-one-hot-encoding/note.md) |
| Duplicate row | A row identical to another row in every column. | [Video 19](19-understanding-your-data/note.md) |
| Eager learning | Another name for model-based learning: all the work done up front. | [Video 6](06-instance-vs-model-based/note.md) |
| Eigen-decomposition | Finding all the eigenvalues and eigenvectors of a matrix. | [Video 48](48-pca-step-by-step/note.md) |
| Eigenvalue | The factor by which a matrix stretches its eigenvector. | [Video 48](48-pca-step-by-step/note.md) |
| Eigenvector | A vector that a matrix only stretches or shrinks, without turning it. | [Video 48](48-pca-step-by-step/note.md) |
| Encoding | The rulebook that maps text characters to stored bytes. | [Video 15](15-working-with-csv/note.md) |
| Endpoint | One address of an API that returns one kind of data. | [Video 17](17-fetching-data-from-api/note.md) |
| Environment variable | A named value stored on the computer, outside the code, read with `os.environ`. | [Video 17](17-fetching-data-from-api/note.md) |
| Environment | The world the agent acts in. | [Video 3](03-types-of-ml/note.md) |
| Euclidean distance | The straight-line distance between two points. | [Video 23](23-what-is-feature-engineering/note.md) |
| Expert system | Early AI: a human expert's knowledge written as rules, plus a program that applies them. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Explained variance ratio | One component's share of the total variance: its eigenvalue divided by the sum of all. | [Video 49](49-pca-mnist/note.md) |
| Explained variance | The variance along a principal component; its eigenvalue. | [Video 48](48-pca-step-by-step/note.md) |
| explained_variance_ | The eigenvalues of the fitted PCA, largest first. | [Video 49](49-pca-mnist/note.md) |
| Explicit programming | A human writing out every rule the computer follows. ML avoids it. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Exploratory data analysis (EDA) | Exploring data with summaries and plots to find patterns. | [Video 13](13-toy-project/note.md) |
| f-string | Text starting with `f` in which `{name}` is replaced by a value. | [Video 17](17-fetching-data-from-api/note.md) |
| Feature construction | Creating a new column by hand from existing ones. | [Video 23](23-what-is-feature-engineering/note.md) |
| Feature engineering | Choosing, removing and creating features. | [Video 7](07-challenges-in-ml/note.md) |
| Feature extraction | Creating a new column from existing ones. | [Video 3](03-types-of-ml/note.md) |
| Feature scaling | Putting columns on the same scale, so no column dominates distances. | [Video 6](06-instance-vs-model-based/note.md) |
| Feature selection | Choosing which input columns to use. | [Video 13](13-toy-project/note.md) |
| Feature transformation | Changing a column into a form the model can use better. | [Video 23](23-what-is-feature-engineering/note.md) |
| Feature | One piece of information about each example that a model uses (e.g. a student's CGPA). | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Fence | A limit 1.5 IQR beyond the box; values past it are possible outliers. | [Video 20](20-univariate-analysis/note.md) |
| fit / transform | Learn the scaler's numbers from the training set / apply them to any data. | [Video 24](24-standardization/note.md) |
| fit_transform | Fit and transform in one call; used on the training set only. | [Video 28](28-column-transformer/note.md) |
| Five-number summary | Minimum, Q1, median, Q3 and maximum. | [Video 20](20-univariate-analysis/note.md) |
| For loop | Code that repeats once for each item of a collection. | [Video 15](15-working-with-csv/note.md) |
| Forward selection | Feature selection that starts empty and adds the best column at a time. | [Video 46](46-curse-of-dimensionality/note.md) |
| Frame | One image in a video. | [Video 11](11-tensors/note.md) |
| Frequency | How many times a value or category occurs. | [Video 20](20-univariate-analysis/note.md) |
| func | The `FunctionTransformer` parameter that holds the function to apply. | [Video 30](30-function-transformer/note.md) |
| Function, lambda | A named reusable piece of code (`def`), and a one-line unnamed one. | [Video 15](15-working-with-csv/note.md) |
| FunctionTransformer | scikit-learn's class that applies any function we give it to the data. | [Video 30](30-function-transformer/note.md) |
| Garbage in, garbage out | Bad input data always gives bad results. | [Video 7](07-challenges-in-ml/note.md) |
| get_dummies | pandas function that one-hot encodes columns; `drop_first=True` keeps $n - 1$. | [Video 27](27-one-hot-encoding/note.md) |
| get_feature_names_out | `OneHotEncoder` method that returns the names of the new columns. | [Video 27](27-one-hot-encoding/note.md) |
| Good fit | Capturing the pattern while ignoring the noise. | [Video 7](07-challenges-in-ml/note.md) |
| Gradient descent | Finding the lowest point of a function by repeated small steps downhill. | [Video 24](24-standardization/note.md) |
| GridSearchCV | scikit-learn class that cross-validates every value in a grid and keeps the best. | [Video 29](29-pipelines/note.md) |
| handle_unknown | `OneHotEncoder` parameter that decides what happens to categories never seen in training. | [Video 27](27-one-hot-encoding/note.md) |
| handle_unknown="ignore" | `OneHotEncoder` setting that outputs all zeros for a category not seen in training. | [Video 29](29-pipelines/note.md) |
| Header | The line of a file that holds the column names. | [Video 15](15-working-with-csv/note.md) |
| Headers | Extra information sent with a request, such as the User-Agent. | [Video 18](18-web-scraping/note.md) |
| Heatmap | A table drawn as coloured cells, darker for larger values. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| High cardinality | A categorical column with very many different categories. | [Video 22](22-pandas-profiling/note.md) |
| High-dimensional data | Data with a very large number of columns. | [Video 46](46-curse-of-dimensionality/note.md) |
| Histogram | A bar chart of how many values fall in each equal range (bin) of a numerical column. | [Video 20](20-univariate-analysis/note.md) |
| HTML | The language web pages are written in: a tree of nested tags. | [Video 18](18-web-scraping/note.md) |
| Hue, style, size | Plot settings that show an extra column by colour, marker shape or dot size. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Hyperparameter tuning | Trying several hyperparameter values and keeping the best. | [Video 29](29-pipelines/note.md) |
| Hyperparameter | A setting of an algorithm chosen before training, such as a tree's `max_depth`. | [Video 29](29-pipelines/note.md) |
| Identity matrix | The matrix that leaves every vector unchanged. | [Video 48](48-pca-step-by-step/note.md) |
| Imputation | Filling in missing values, for example with the mean, median or mode. | [Video 23](23-what-is-feature-engineering/note.md) |
| Incremental learning | Training on small pieces of data over time (the opposite of batch). | [Video 4](04-batch-learning/note.md) |
| Incremental training | Training in small steps, keeping what was learned before. | [Video 5](05-online-learning/note.md) |
| Independent variables | The input columns (X). | [Video 13](13-toy-project/note.md) |
| Index | The row labels of a DataFrame. | [Video 15](15-working-with-csv/note.md) |
| Inference engine | The part of an expert system that applies the rules to answer a question. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Input / output | The columns we know / the column we want to predict. | [Video 3](03-types-of-ml/note.md) |
| Inspect | Browser tool that shows which tag draws each part of a page. | [Video 18](18-web-scraping/note.md) |
| Instance-based learning | Learning by storing the training data and comparing new points with it. | [Video 6](06-instance-vs-model-based/note.md) |
| Interquartile range (IQR) | Q3 - Q1: the width of the middle half of the data. | [Video 20](20-univariate-analysis/note.md) |
| joblib | A library that saves and loads Python objects like pickle, better suited to large arrays. | [Video 29](29-pipelines/note.md) |
| JSON (JavaScript Object Notation) | A plain-text data format of objects and arrays that almost every language can read. | [Video 16](16-working-with-json-and-sql/note.md) |
| JSON Lines | A JSON file with one object per line, read with `lines=True`. | [Video 16](16-working-with-json-and-sql/note.md) |
| JSON viewer | A tool that lays out JSON text as a tree to show its structure. | [Video 17](17-fetching-data-from-api/note.md) |
| K-nearest neighbours (KNN) | Predicting from the answers of the k closest stored points. | [Video 6](06-instance-vs-model-based/note.md) |
| Kaggle | A website for sharing datasets and notebooks and for ML competitions. | [Video 17](17-fetching-data-from-api/note.md) |
| KDE plot | A smooth estimate of a column's PDF, built from the data. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Kernel density estimate (KDE) | A smooth curve that estimates a column's distribution from its values. | [Video 20](20-univariate-analysis/note.md) |
| Knowledge base | The collection of rules inside an expert system. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Kurtosis | How heavy the tails of a distribution are compared with a normal curve. | [Video 22](22-pandas-profiling/note.md) |
| Label encoding | Replacing the classes of the target by 0, 1, 2, ...; for the output column only. | [Video 26](26-ordinal-label-encoding/note.md) |
| LabelEncoder | scikit-learn's class for label encoding the target. | [Video 26](26-ordinal-label-encoding/note.md) |
| Labelled data | Data that includes the output column. | [Video 3](03-types-of-ml/note.md) |
| Lambda | A one-line Python function without a name, such as `lambda x: x**2`. | [Video 30](30-function-transformer/note.md) |
| Layer | One step in a neural network; each layer builds on what the previous one found. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Lazy learning | Another name for instance-based learning: no work until a question arrives. | [Video 6](06-instance-vs-model-based/note.md) |
| LDA | Linear discriminant analysis: a supervised method that finds the directions that best separate the classes. | [Video 49](49-pca-mnist/note.md) |
| Learning rate | How strongly each new piece of data changes the model. | [Video 5](05-online-learning/note.md) |
| Learning | Finding rules (patterns) from examples. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Line plot | A scatter plot with the dots joined in order, used when x is time. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Linear regression | An algorithm that fits the straight line closest to all the points. | [Video 23](23-what-is-feature-engineering/note.md) |
| Linear relationship | A relationship between two columns that follows a straight line. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Linear transformation | A change of the whole plane by a matrix that keeps grid lines straight and evenly spaced. | [Video 48](48-pca-step-by-step/note.md) |
| List, dictionary | Python's ordered collection `[...]`, and its `key: value` pairs `{...}`. | [Video 15](15-working-with-csv/note.md) |
| Log transform | Replacing each value with its logarithm; pulls in a long right tail. | [Video 30](30-function-transformer/note.md) |
| log1p | NumPy's $\log(1 + x)$, a log transform that also works when a value is 0. | [Video 30](30-function-transformer/note.md) |
| Logistic regression | A classification algorithm that finds a separating boundary. | [Video 13](13-toy-project/note.md) |
| Machine Learning (ML) | Using statistics to let a machine find patterns (rules) in data by itself. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Magnitude | The number part of a quantity, as opposed to its unit. | [Video 25](25-normalization/note.md) |
| make_column_transformer | Function that builds a column transformer from (transformer, columns) pairs, without names. | [Video 29](29-pipelines/note.md) |
| make_pipeline | Function that builds a pipeline from objects alone, naming each step after its class. | [Video 29](29-pipelines/note.md) |
| Mathematical transformation | Applying one mathematical formula to every value of a column. | [Video 30](30-function-transformer/note.md) |
| Matrix | A table of numbers: a 2D tensor. | [Video 11](11-tensors/note.md) |
| Max-abs scaling | Divide by the largest absolute value in the column, giving values from -1 to 1. | [Video 25](25-normalization/note.md) |
| MaxAbsScaler | scikit-learn's class for max-abs scaling. | [Video 25](25-normalization/note.md) |
| Mean absolute deviation | The average absolute distance of the points from their mean. | [Video 47](47-pca-geometric-intuition/note.md) |
| Mean centring | Subtracting the mean from every value, so the column's mean becomes 0. | [Video 24](24-standardization/note.md) |
| Mean normalization | Subtract the mean and divide by the range, giving values from -1 to 1 centred on 0. | [Video 25](25-normalization/note.md) |
| Mean | The average of the values; the centre of the data. | [Video 47](47-pca-geometric-intuition/note.md) |
| Median absolute deviation (MAD) | The median distance of the values from their median. | [Video 22](22-pandas-profiling/note.md) |
| Median | The middle value of sorted data; the 50% percentile. | [Video 19](19-understanding-your-data/note.md) |
| Min-max scaling | The main normalization technique. | [Video 24](24-standardization/note.md) |
| min_frequency | `OneHotEncoder` parameter that merges rare categories into one column. | [Video 27](27-one-hot-encoding/note.md) |
| Mini-batch | A small group of data points used for one training step. | [Video 5](05-online-learning/note.md) |
| MinMaxScaler | scikit-learn's class for min-max scaling. | [Video 25](25-normalization/note.md) |
| Missing value | An empty entry, shown by pandas as `NaN`. | [Video 15](15-working-with-csv/note.md) |
| Missing values | Empty cells in the data. | [Video 7](07-challenges-in-ml/note.md) |
| MLOps | Running and maintaining ML models in production. | [Video 7](07-challenges-in-ml/note.md) |
| MNIST | A dataset of about 70,000 handwritten-digit images of 28 × 28 pixels. | [Video 23](23-what-is-feature-engineering/note.md) |
| Mode | The most common value of a column. | [Video 23](23-what-is-feature-engineering/note.md) |
| Model drift / concept drift | A model's accuracy dropping as the real world changes. | [Video 4](04-batch-learning/note.md) |
| Model selection | Training several algorithms and keeping the best. | [Video 13](13-toy-project/note.md) |
| Model-based learning | Learning a mathematical function from the data and predicting with it. | [Video 6](06-instance-vs-model-based/note.md) |
| Monotonicity | Whether a column's values only go up, or only go down, from row to row. | [Video 22](22-pandas-profiling/note.md) |
| Multicollinearity | A mathematical relationship between input columns, so that one can be calculated from the others. | [Video 27](27-one-hot-encoding/note.md) |
| Multivariate analysis | Studying more than two variables together. | [Video 20](20-univariate-analysis/note.md) |
| n_components | The number of principal components PCA keeps; a number between 0 and 1 means a share of the variance. | [Video 49](49-pca-mnist/note.md) |
| named_steps | Dictionary of a pipeline's steps, from each name to its object. | [Video 29](29-pipelines/note.md) |
| Narrow AI | AI that does one specific task. All AI today is narrow. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Neural network | The model DL uses, loosely inspired by neurons in the brain. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Nominal data | Categorical data whose categories have no order, such as states. | [Video 26](26-ordinal-label-encoding/note.md) |
| Non-null | Not missing. | [Video 19](19-understanding-your-data/note.md) |
| Normal distribution | A symmetric, bell-shaped distribution. | [Video 20](20-univariate-analysis/note.md) |
| Normalization | The other type of feature scaling, which squeezes values into a fixed range (next Note). | [Video 24](24-standardization/note.md) |
| np.concatenate | NumPy function that joins arrays; with `axis=1` it puts them side by side. | [Video 28](28-column-transformer/note.md) |
| Nullity matrix | A picture of the whole table with missing values drawn as white lines. | [Video 22](22-pandas-profiling/note.md) |
| Numerical data | Data made of numbers. | [Video 3](03-types-of-ml/note.md) |
| Objective function | The quantity an algorithm tries to make as large or as small as possible. | [Video 48](48-pca-step-by-step/note.md) |
| Observation | The report's word for a row. | [Video 22](22-pandas-profiling/note.md) |
| Offline learning | Another name for batch learning. | [Video 4](04-batch-learning/note.md) |
| One-hot encoding | Representing each word or category by a vector with a single 1. | [Video 11](11-tensors/note.md) |
| OneHotEncoder | scikit-learn's class for one-hot encoding; remembers the categories it learned. | [Video 27](27-one-hot-encoding/note.md) |
| Online learning | Training incrementally on mini-batches while the model is live in production. | [Video 5](05-online-learning/note.md) |
| Optimal number of features | The number of columns at which a model performs best. | [Video 46](46-curse-of-dimensionality/note.md) |
| Ordinal data | Categorical data whose categories have a natural order, such as Poor < Average < Good. | [Video 26](26-ordinal-label-encoding/note.md) |
| Ordinal encoding | Replacing ordered categories by 0, 1, 2, ... in their order; for input columns. | [Video 26](26-ordinal-label-encoding/note.md) |
| OrdinalEncoder | scikit-learn's class for ordinal encoding; takes the order through `categories`. | [Video 26](26-ordinal-label-encoding/note.md) |
| Out-of-core learning | Training on data too big for memory by feeding it in chunks, offline. | [Video 5](05-online-learning/note.md) |
| Outlier | A value far from the rest of the data. | [Video 20](20-univariate-analysis/note.md) |
| Outliers | Values far from the rest, often mistakes. | [Video 7](07-challenges-in-ml/note.md) |
| Overfitting | Learning the training data too closely, noise included; fails on new data. | [Video 7](07-challenges-in-ml/note.md) |
| Pair plot | A grid of scatter plots of every pair of numerical columns, with histograms on the diagonal. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Pandas Profiling | The library that builds a profiling report from a DataFrame, now named `fg-data-profiling`. | [Video 22](22-pandas-profiling/note.md) |
| pandas, DataFrame | Python's main table library, and its name for a table. | [Video 13](13-toy-project/note.md) |
| Parameter | A named setting passed to a function, like `sep=";"`. | [Video 15](15-working-with-csv/note.md) |
| Parameters | The numbers that describe a learned model, e.g. slope and intercept. | [Video 6](06-instance-vs-model-based/note.md) |
| Parse, parser | Read text and build a structure from it; the part that does this. | [Video 18](18-web-scraping/note.md) |
| Parser | The part of a program that reads text and splits it into pieces. | [Video 15](15-working-with-csv/note.md) |
| partial_fit | A scikit-learn method that continues training from where the model left off. | [Video 5](05-online-learning/note.md) |
| passthrough | The `remainder` option that keeps untouched columns unchanged. | [Video 28](28-column-transformer/note.md) |
| PCA | Principal component analysis, a dimensionality reduction technique. | [Video 3](03-types-of-ml/note.md) |
| Pearson correlation coefficient | The usual measure of correlation, written $r$; the one `df.corr()` computes. | [Video 19](19-understanding-your-data/note.md) |
| Pearson's r | The correlation coefficient for straight-line relationships between two numerical columns. | [Video 22](22-pandas-profiling/note.md) |
| Percentile | The value below which a given share of the data lies. | [Video 19](19-understanding-your-data/note.md) |
| Perceptron | The smallest building block of a neural network; one artificial neuron. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| phpMyAdmin | A web page for creating and managing MySQL databases. | [Video 16](16-working-with-json-and-sql/note.md) |
| pickle | A Python module that saves objects to a file and loads them back. | [Video 13](13-toy-project/note.md) |
| Pie chart | A circle split into slices sized by each category's share. | [Video 20](20-univariate-analysis/note.md) |
| Pipeline (class) | The scikit-learn class (in `sklearn.pipeline`) that builds a pipeline from a list of (name, object) tuples. | [Video 29](29-pipelines/note.md) |
| Pipeline | One object that bundles several processing steps and a model. | [Video 13](13-toy-project/note.md) |
| Pivot table | A grid with one column's values as rows, another's as columns, and a third in the cells. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Pixel | One dot of an image, stored as one or more numbers. | [Video 11](11-tensors/note.md) |
| Policy | The agent's rules for which action to take. | [Video 3](03-types-of-ml/note.md) |
| PowerTransformer | scikit-learn's class for the Box-Cox and Yeo-Johnson transforms (next Note). | [Video 30](30-function-transformer/note.md) |
| Predict | Use a trained model to give an answer for new data it has not seen. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Preprocessing | Cleaning and preparing data before training. | [Video 13](13-toy-project/note.md) |
| Principal component analysis (PCA) | An unsupervised feature extraction technique that builds new columns along the directions of greatest variance. | [Video 47](47-pca-geometric-intuition/note.md) |
| Principal component | A new axis found by PCA; PC1 holds the most variance, PC2 the next most. | [Video 47](47-pca-geometric-intuition/note.md) |
| Probability density function (PDF) | A curve showing how likely each value is; areas under it are probabilities. | [Video 20](20-univariate-analysis/note.md) |
| Production code | The code that runs the deployed model on a server, for example behind a website. | [Video 29](29-pipelines/note.md) |
| Production environment | The server where a model serves real users. | [Video 4](04-batch-learning/note.md) |
| Profiling report | An automatic EDA report describing every column and pair of columns of a dataset. | [Video 22](22-pandas-profiling/note.md) |
| Projection | Dropping each point onto an axis or line, like casting a shadow. | [Video 47](47-pca-geometric-intuition/note.md) |
| Q-Q plot | A plot of a column's sorted values against the values a normal distribution would have; points on the line mean normal. | [Video 30](30-function-transformer/note.md) |
| QuantileTransformer | scikit-learn's third mathematical transformer, not covered in these Notes. | [Video 30](30-function-transformer/note.md) |
| Quartiles | The 25%, 50% and 75% percentiles, which cut the data into four equal groups. | [Video 19](19-understanding-your-data/note.md) |
| Query parameters | Settings after the `?` in a URL, joined by `&`, such as `page=1`. | [Video 17](17-fetching-data-from-api/note.md) |
| Query | A request for data, written in SQL. | [Video 16](16-working-with-json-and-sql/note.md) |
| Rank | The number of axes of a tensor (ndim in NumPy). | [Video 11](11-tensors/note.md) |
| RapidAPI | A website listing many APIs, including free ones. | [Video 17](17-fetching-data-from-api/note.md) |
| Rate limit | The most requests an API accepts in a given time. | [Video 17](17-fetching-data-from-api/note.md) |
| Raw data | Data as it arrives, before any preparation. | [Video 23](23-what-is-feature-engineering/note.md) |
| Reader | What `read_csv` returns with `chunksize`: it hands out one chunk at a time. | [Video 15](15-working-with-csv/note.md) |
| Reciprocal transform | Replacing each value with $1/x$; reverses the order of the values. | [Video 30](30-function-transformer/note.md) |
| Recommendation engine | A model that suggests items, such as movies, to users. | [Video 4](04-batch-learning/note.md) |
| Reference category | The category whose dummy column is dropped; it is shown by all zeros. | [Video 27](27-one-hot-encoding/note.md) |
| Regression | Supervised learning with a numerical output. | [Video 3](03-types-of-ml/note.md) |
| Reinforcement learning | Learning by acting and receiving rewards or punishments. | [Video 3](03-types-of-ml/note.md) |
| Relative path | A file's location, starting from the folder the code runs in. | [Video 15](15-working-with-csv/note.md) |
| remainder | The `ColumnTransformer` parameter for untouched columns: `"drop"` (default) or `"passthrough"`. | [Video 28](28-column-transformer/note.md) |
| Representative sample | A sample that reflects the whole situation fairly. | [Video 7](07-challenges-in-ml/note.md) |
| Request, response | What we send to a server, and what it sends back. | [Video 18](18-web-scraping/note.md) |
| requests | Python library that sends web requests. | [Video 17](17-fetching-data-from-api/note.md) |
| Response | What `requests.get` returns: the status code plus the reply. | [Video 17](17-fetching-data-from-api/note.md) |
| Retrain | Train a model again, here from scratch on old + new data. | [Video 4](04-batch-learning/note.md) |
| Reward / punishment | Good / bad feedback after an action. | [Video 3](03-types-of-ml/note.md) |
| River | A Python library for online machine learning. | [Video 5](05-online-learning/note.md) |
| robots.txt | A file at a site's root listing what bots are asked not to visit. | [Video 18](18-web-scraping/note.md) |
| Robust scaler | A normalization technique that copes well with outliers. | [Video 24](24-standardization/note.md) |
| Robust scaling | Subtract the median and divide by the interquartile range; copes well with outliers. | [Video 25](25-normalization/note.md) |
| RobustScaler | scikit-learn's class for robust scaling. | [Video 25](25-normalization/note.md) |
| Rollback | Restoring a model to an earlier, good version. | [Video 5](05-online-learning/note.md) |
| Sample | The part of the real world that our data covers. | [Video 7](07-challenges-in-ml/note.md) |
| Sampling bias | An unrepresentative sample caused by how the data was collected. | [Video 7](07-challenges-in-ml/note.md) |
| Sampling noise | An unrepresentative sample caused by being too small. | [Video 7](07-challenges-in-ml/note.md) |
| Scalar | A single number: a 0D tensor. | [Video 11](11-tensors/note.md) |
| Scaling | Bringing input columns to similar ranges. | [Video 13](13-toy-project/note.md) |
| Scatter plot | One dot per row, with one numerical column on each axis. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| scikit-learn | Python's main library for classical ML. | [Video 13](13-toy-project/note.md) |
| SelectKBest | scikit-learn class that scores every column and keeps the `k` best. | [Video 29](29-pipelines/note.md) |
| Semi-supervised learning | Learning from a few labelled rows and many unlabelled ones. | [Video 3](03-types-of-ml/note.md) |
| Separator | The character between values on a line, such as `,` or a tab. | [Video 15](15-working-with-csv/note.md) |
| Sequential data | Data fed one piece after another, in order. | [Video 5](05-online-learning/note.md) |
| Series | pandas' one-column structure: values with an index. | [Video 15](15-working-with-csv/note.md) |
| Server | A computer that is always on and that users reach over the internet. | [Video 4](04-batch-learning/note.md) |
| set_output | Method that makes a transformer return a pandas DataFrame with `transform="pandas"`. | [Video 28](28-column-transformer/note.md) |
| SGDRegressor | A scikit-learn model that does linear regression step by step. | [Video 5](05-online-learning/note.md) |
| Shape | The number of items along each axis. | [Video 11](11-tensors/note.md) |
| Similarity | How alike two data points are. | [Video 6](06-instance-vs-model-based/note.md) |
| SimpleImputer | scikit-learn's class that fills missing values, by default with the column's mean. | [Video 28](28-column-transformer/note.md) |
| Size | The total number of items: the product of the shape. | [Video 11](11-tensors/note.md) |
| Skewness | A number for how lopsided a distribution is: 0 symmetric, positive right tail, negative left tail. | [Video 20](20-univariate-analysis/note.md) |
| slice(0, 10) | Python object meaning positions 0 up to, not including, 10. | [Video 29](29-pipelines/note.md) |
| Software integration | Building a model into the software that users use. | [Video 7](07-challenges-in-ml/note.md) |
| Solver | The method a model uses to find its best settings during training. | [Video 24](24-standardization/note.md) |
| Sparse data | Data where most of the space holds no points. | [Video 46](46-curse-of-dimensionality/note.md) |
| Sparse matrix | A table stored as only its non-zero entries, to save memory. | [Video 27](27-one-hot-encoding/note.md) |
| sparse_output | `OneHotEncoder` parameter; `False` returns a normal NumPy array. | [Video 27](27-one-hot-encoding/note.md) |
| SQL (Structured Query Language) | The language for asking a database for data. | [Video 16](16-working-with-json-and-sql/note.md) |
| SQLAlchemy | A Python library that connects to many kinds of database; pandas supports it fully. | [Video 16](16-working-with-json-and-sql/note.md) |
| SQLite | A database stored in a single file, built into Python, needing no server. | [Video 16](16-working-with-json-and-sql/note.md) |
| Square root transform | Replacing each value with $\sqrt{x}$; a milder version of the log. | [Video 30](30-function-transformer/note.md) |
| Square transform | Replacing each value with $x^2$; used for left-skewed data. | [Video 30](30-function-transformer/note.md) |
| Standard deviation | A measure of how spread out a column's values are. | [Video 13](13-toy-project/note.md) |
| Standardization | Scaling a column to mean 0 and standard deviation 1. | [Video 13](13-toy-project/note.md) |
| StandardScaler | scikit-learn's class that standardizes columns with `fit` and `transform`. | [Video 24](24-standardization/note.md) |
| Static model | A model that learns nothing new after deployment. | [Video 4](04-batch-learning/note.md) |
| Status code | A number saying how a request went: 200 OK, 401, 404, 500. | [Video 17](17-fetching-data-from-api/note.md) |
| step__parameter | How a pipeline step's parameter is named: step name, two underscores, parameter name. | [Video 29](29-pipelines/note.md) |
| Supervised learning | Learning from data with inputs and outputs, to predict outputs. | [Video 3](03-types-of-ml/note.md) |
| Supervision | Correct answers that guide an algorithm while it learns. | [Video 3](03-types-of-ml/note.md) |
| Symbolic AI | Early AI where humans write the knowledge as rules. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Tag | One element of HTML, such as `<h2>TCS</h2>`. | [Video 18](18-web-scraping/note.md) |
| Target, label | Other names for the output column. | [Video 3](03-types-of-ml/note.md) |
| Tensor | A container of numbers arranged along one or more axes. | [Video 11](11-tensors/note.md) |
| Test set | The part hidden during training, used to check the model. | [Video 13](13-toy-project/note.md) |
| Theoretical quantile | Where a value would sit if the data were perfectly normal (the horizontal axis of a Q-Q plot). | [Video 30](30-function-transformer/note.md) |
| Time series | Data recorded at regular time intervals. | [Video 11](11-tensors/note.md) |
| Top categories | Keeping only the most frequent categories and merging the rest into one "uncommon" category. | [Video 27](27-one-hot-encoding/note.md) |
| Train | Let a model learn by making predictions, measuring its errors and adjusting to reduce them. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Train-test split | Dividing the data into training and test sets. | [Video 13](13-toy-project/note.md) |
| Training set | The part of the data the model learns from. | [Video 13](13-toy-project/note.md) |
| transformers | The `ColumnTransformer` parameter: a list of (name, transformer, columns) tuples. | [Video 28](28-column-transformer/note.md) |
| transformers_ | List of a fitted column transformer's (name, transformer, columns) tuples. | [Video 29](29-pipelines/note.md) |
| Transpose | A matrix or vector with rows and columns swapped. | [Video 48](48-pca-step-by-step/note.md) |
| TSV file | Like a CSV file, with tabs between values. | [Video 15](15-working-with-csv/note.md) |
| Underfitting | Being too simple to capture the pattern; fails on all data. | [Video 7](07-challenges-in-ml/note.md) |
| Understanding the data | The project stage where we learn what is in the data before cleaning or modelling. | [Video 19](19-understanding-your-data/note.md) |
| Unit hypercube | The same box in three or more dimensions (a unit cube in three). | [Video 25](25-normalization/note.md) |
| Unit square | The square from (0, 0) to (1, 1), into which min-max scaling presses two columns. | [Video 25](25-normalization/note.md) |
| Unit vector | A vector of length 1, used to describe a direction. | [Video 48](48-pca-step-by-step/note.md) |
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
| Z-score normalization | Another name for standardization. | [Video 24](24-standardization/note.md) |
| Z-score | A value after standardization: how many standard deviations it lies from the mean. | [Video 24](24-standardization/note.md) |
