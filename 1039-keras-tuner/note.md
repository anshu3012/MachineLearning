---
title: "Hyperparameter Tuning a Neural Network with Keras Tuner"
---

## 1. Overview

> **Key point:** Keras Tuner automates the choices we make by hand when we build a network. We write one function that builds a model and marks each choice as a hyperparameter; a tuner then builds, trains and scores many versions and returns the best.

Every network we have built so far rested on guesses: how many hidden layers, how many nodes in each, which activation, which optimizer, which batch size. We cannot know the best answers without trying them. **Keras Tuner** (the Python package `keras_tuner`) is a library that tries them for us.

![The Keras Tuner workflow. The search repeats step 3 for every trial; the test set is used once, at the end](images/workflow.png){width=100%}

Figure 1 shows the whole workflow. We follow it four times on the same data, each time tuning more: first the optimizer, then the number of nodes, then the number of layers, and finally everything at once.

## 2. Prerequisites

- The [how to improve a neural network Note](../1021-improving-a-neural-network/note.md): the hyperparameters of a network.
- The [Optuna Note](../134-optuna/note.md): grid, random and Bayesian search, and the diabetes data.
- The [customer churn ANN Note](../1011-customer-churn-ann/note.md): building, compiling and fitting a Keras model, and the validation set.
- The [dropout Note](../1024-dropout/note.md) and the [activation functions Note](../1027-activation-functions/note.md).

## 3. The problem: too many choices

> **Key point:** A network has many hyperparameters, and the right values depend on the data. Trying them by hand is slow trial and error; Keras Tuner turns it into a search.

A **hyperparameter** is a setting chosen before training that the network does not learn (see the [pipelines Note](../29-pipelines/note.md)). For a network, the main ones are:

- number of hidden layers;
- number of nodes in each hidden layer;
- activation function of each layer;
- optimizer (see the [optimizers Note](../1032-optimizers-in-deep-learning/note.md));
- batch size, the number of epochs and the dropout rate.

Until now we picked these from intuition. **Hyperparameter tuning** tries several values and keeps the ones that score best (the [Optuna Note](../134-optuna/note.md), section 2). For scikit-learn models we used `GridSearchCV` and `RandomizedSearchCV` (the [random forest tuning Note](../112-random-forest-tuning/note.md)). Keras Tuner does the same job for Keras networks.

## 4. The data and a hand-made baseline

> **Key point:** 768 patients, 8 medical measurements, diabetes yes or no. A one-layer network chosen by hand reaches a validation accuracy of 0.760; that is the number to beat.

### 4.1 The Pima diabetes data

> **Key point:** A small, well-known binary classification dataset; every feature is numeric.

We use the Pima diabetes data of the [ROC Note](../78-roc-auc/note.md) and the [Optuna Note](../134-optuna/note.md). Each **observation** (one record, a row of the table) is a woman. Each has 8 **features** (input variables, one column each), such as the number of pregnancies, glucose, blood pressure, insulin, BMI and age. The **target** (the output we predict) is `Outcome`: 1 for diabetes, 0 for none.

The correlation of each feature with the target shows that all of them carry some signal. Glucose is the strongest (0.47), then BMI (0.29) and age (0.24); blood pressure and skin thickness are the weakest (0.07 each). We keep all 8, since the goal here is tuning, not feature selection.

### 4.2 Three sets: train, validation, test

> **Key point:** The tuner chooses by the validation score, so the validation set takes part in the choice. A separate test set, used once at the end, gives the honest score.

We split the 768 observations three ways, keeping the share of diabetes the same in each:

| Set | Observations | Used for |
|---|---|---|
| training | 460 (60%) | fitting the weights |
| validation | 154 (20%) | scoring each trial, choosing the best |
| test | 154 (20%) | one final, honest score |

A standard scaler is fitted on the training set only and applied to all three (the [toy project Note](../13-toy-project/note.md) explains why).

Why three sets? The tuner picks the model with the highest validation score. After many trials, the winner's validation score is partly luck: it is the best of many noisy numbers. If we also reported that same set as the final score, information from it would have leaked into the choice of the model (see data leakage in the [toy project Note](../13-toy-project/note.md)). The test set has played no part in any choice, so its score is honest.

### 4.3 The baseline network

> **Key point:** One hidden layer of 32 ReLU nodes, a sigmoid output, Adam, batch size 32, 100 epochs: validation accuracy 0.760.

> **Python:** The hand-made baseline.
>
> ```python
> model = keras.Sequential([
>     keras.Input(shape=(8,)),
>     keras.layers.Dense(32, activation="relu"),
>     keras.layers.Dense(1, activation="sigmoid")])
> model.compile(optimizer="adam",
>               loss="binary_crossentropy", metrics=["accuracy"])
> model.fit(X_train, y_train, batch_size=32, epochs=100,
>           validation_data=(X_val, y_val))
> ```

After 100 epochs the validation accuracy is 0.760. Every number in that model (1 layer, 32 nodes, ReLU, Adam) was a guess. The rest of this Note asks whether a search finds better ones.

## 5. The Keras Tuner workflow: choosing the optimizer

> **Key point:** Three steps: a function `build_model(hp)` that marks the choices, a tuner object, and `tuner.search(...)`. Then we read off the best hyperparameters and the best model.

### 5.1 Step 1: the model-building function

> **Key point:** `build_model(hp)` builds and compiles one network. Wherever a value should be tuned, we ask `hp` for it instead of writing a number.

Keras Tuner calls our function again and again, once per **trial** (one model built, trained and scored with one set of hyperparameter values). It passes in `hp`, a `HyperParameters` object. Calling `hp.Choice(name, values=[...])` both declares a hyperparameter and returns the value to use in this trial (Keras Tuner guide).

> **Python:** Only the optimizer is tuned; the rest is fixed.
>
> ```python
> import keras_tuner as kt
>
> def build_model(hp):
>     model = keras.Sequential([
>         keras.Input(shape=(8,)),
>         keras.layers.Dense(32, activation="relu"),
>         keras.layers.Dense(1, activation="sigmoid")])
>     optimizer = hp.Choice("optimizer",
>         values=["adam", "sgd", "rmsprop", "adadelta"])
>     model.compile(optimizer=optimizer,
>         loss="binary_crossentropy", metrics=["accuracy"])
>     return model
> ```

Every hyperparameter has a name, here `"optimizer"`; the results are reported under that name. The four optimizers are taught in their own Notes: SGD with [momentum](../1034-sgd-with-momentum/note.md) or without, [RMSProp](../1037-rmsprop/note.md) and [Adam](../1038-adam/note.md); Adadelta is a relative of RMSProp (Ruder 2016, section 4.4).

### 5.2 Step 2: the tuner object

> **Key point:** `kt.RandomSearch` draws random combinations of the hyperparameter values, up to `max_trials` of them, and keeps the one with the best `objective`.

> **Python:** A random-search tuner.
>
> ```python
> tuner = kt.RandomSearch(
>     build_model,                  # the function above
>     objective="val_accuracy",     # what to maximise
>     max_trials=5,                 # at most 5 models
>     seed=0,                       # same draws every run
>     directory="my_dir",           # where results are saved
>     project_name="optimizer",     # sub-folder of directory
>     overwrite=True)               # start afresh
> ```

`RandomSearch` is the counterpart of scikit-learn's `RandomizedSearchCV`, not of `GridSearchCV`: it draws random combinations instead of trying every one (Keras Tuner guide). Keras Tuner also has `BayesianOptimization` and `Hyperband` tuners (Keras Tuner guide); the idea behind Bayesian search is in the [Optuna Note](../134-optuna/note.md).

`objective` names the metric to optimise. For built-in metrics such as `"val_accuracy"`, the tuner infers on its own whether higher or lower is better (Keras Tuner guide).

### 5.3 Step 3: the search

> **Key point:** `tuner.search` takes the same arguments as `model.fit`. RMSProp scored best, 0.747; Adadelta failed, 0.338.

> **Python:** Run the trials. Each trial trains for 10 epochs.
>
> ```python
> tuner.search(X_train, y_train, epochs=10,
>              validation_data=(X_val, y_val))
> ```

Every argument of `search` is passed on to `model.fit` in each trial (Keras Tuner guide). The tuner builds a model, trains it, records its validation accuracy, and moves on. Ten epochs are enough to compare the candidates roughly; the winner can train longer afterwards.

| Trial | Optimizer | Validation accuracy |
|---|---|---|
| 3 | `rmsprop` | 0.747 |
| 1 | `sgd` | 0.740 |
| 0 | `adam` | 0.727 |
| 2 | `adadelta` | 0.338 |

We asked for 5 trials but got 4. The optimizer has only 4 values, so after 4 trials every combination has been tried. The random search then keeps drawing repeats; after 20 repeats in a row it stops (Keras Tuner source, `oracle.py`).

> **Extra:** Adadelta's 0.338 is almost exactly the share of diabetes in the validation set, 0.351: after 10 epochs that model still called nearly every patient diabetic. Keras gives Adadelta a default learning rate of 0.001 (Keras source, `adadelta.py`), so in 10 epochs its weights moved little from their random start. A poor score after a short search can mean "not trained enough" as well as "bad choice".

### 5.4 The best hyperparameters and the best model

> **Key point:** `get_best_hyperparameters()[0].values` gives the winning values as a dictionary; `get_best_models(num_models=1)[0]` gives the winning model, already trained.

> **Python:** Read off the winner and keep training it.
>
> ```python
> tuner.get_best_hyperparameters()[0].values
> # {'optimizer': 'rmsprop'}
>
> model = tuner.get_best_models(num_models=1)[0]
> model.fit(X_train, y_train, batch_size=32, epochs=100,
>           initial_epoch=10,
>           validation_data=(X_val, y_val))
> ```

Both methods return lists sorted from best to worst, hence the `[0]`. The returned model is not a fresh one: it holds the weights from the best epoch of its trial (Keras Tuner guide). So we can continue training it rather than start again.

`initial_epoch` tells `fit` where to continue the epoch count. Epochs are numbered from 0, so after 10 epochs (numbers 0 to 9) the next one is number 10, and `initial_epoch=10, epochs=100` runs the remaining 90. Setting `initial_epoch` to one more than the epochs already run would skip an epoch.

After the 90 further epochs, the RMSProp model reaches a validation accuracy of 0.753, against the baseline's 0.760. Choosing the optimizer alone did not beat the baseline here.

## 6. Tuning the number of nodes

> **Key point:** `hp.Int(name, min_value, max_value, step)` tries whole numbers in a range. With 8 to 128 in steps of 8, the best of 5 trials was 56 nodes, at 0.773.

> **Python:** The hidden layer's size becomes a hyperparameter; the optimizer is the winner of section 5.
>
> ```python
> def build_model(hp):
>     units = hp.Int("units", min_value=8,
>                    max_value=128, step=8)
>     model = keras.Sequential([
>         keras.Input(shape=(8,)),
>         keras.layers.Dense(units, activation="relu"),
>         keras.layers.Dense(1, activation="sigmoid")])
>     model.compile(optimizer="rmsprop",
>         loss="binary_crossentropy", metrics=["accuracy"])
>     return model
> ```

`hp.Int` declares an integer hyperparameter. With `step=8` the possible values are 8, 16, 24, …, 128: 16 values. The random search draws 5 of them:

| Nodes | 56 | 104 | 64 | 32 | 8 |
|---|---|---|---|---|---|
| Validation accuracy | 0.773 | 0.766 | 0.753 | 0.734 | 0.636 |

Without `step`, every whole number from 8 to 128 can be drawn; Keras Tuner then stores the step as 1 (Notebook).

## 7. Tuning the number of layers

> **Key point:** A `for` loop over `range(hp.Int("num_layers", 1, 10))` adds that many hidden layers. Of 5 trials, 3 layers scored best, 0.766, tied with 5 layers.

> **Python:** The number of hidden layers is the hyperparameter; each layer has the 56 nodes found in section 6.
>
> ```python
> def build_model(hp):
>     model = keras.Sequential([keras.Input(shape=(8,))])
>     n = hp.Int("num_layers", min_value=1, max_value=10)
>     for i in range(n):
>         model.add(keras.layers.Dense(56, activation="relu"))
>     model.add(keras.layers.Dense(1, activation="sigmoid"))
>     model.compile(optimizer="rmsprop",
>         loss="binary_crossentropy", metrics=["accuracy"])
>     return model
> ```

The loop runs once per trial with the drawn number: one trial builds 3 hidden layers, another 8. With `keras.Input` as the first element, the first hidden layer needs no special case.

| Hidden layers | 3 | 5 | 10 | 1 | 8 |
|---|---|---|---|---|---|
| Validation accuracy | 0.766 | 0.766 | 0.753 | 0.740 | 0.734 |

The scores are close together: on 154 validation patients, one patient more or less changes the accuracy by $1/154 = 0.0065$.

## 8. Tuning everything at once

> **Key point:** Inside the layer loop, each layer gets its own hyperparameters, named with the layer number: `units_0`, `units_1`, …. The number of hyperparameters then changes from trial to trial.

### 8.1 One name per layer

> **Key point:** Two hyperparameters with the same name are the same hyperparameter. To tune each layer separately, put the layer number in the name.

Each hyperparameter is identified by its name (Keras Tuner guide). If every layer asked for `hp.Int("units", ...)`, all layers would share one value. Writing `f"units_{i}"` gives layer 0 the hyperparameter `units_0`, layer 1 `units_1`, and so on.

These are **conditional hyperparameters**: `units_3` exists only in trials with at least 4 layers (Keras Tuner guide). We also add a dropout layer after each hidden layer, with its own rate, and let the tuner pick the optimizer.

> **Python:** The all-in-one model-building function.
>
> ```python
> def build_model(hp):
>     model = keras.Sequential([keras.Input(shape=(8,))])
>     for i in range(hp.Int("num_layers", 1, 4)):
>         model.add(keras.layers.Dense(
>             hp.Int(f"units_{i}", 8, 128, step=8),
>             activation=hp.Choice(f"activation_{i}",
>                                  values=["relu", "tanh"])))
>         model.add(keras.layers.Dropout(
>             hp.Choice(f"dropout_{i}",
>                 values=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5])))
>     model.add(keras.layers.Dense(1, activation="sigmoid"))
>     optimizer = hp.Choice("optimizer",
>         values=["adam", "rmsprop", "nadam", "sgd"])
>     model.compile(optimizer=optimizer,
>         loss="binary_crossentropy", metrics=["accuracy"])
>     return model
> ```

Each added value multiplies the number of combinations (the [Optuna Note](../134-optuna/note.md), section 2), and random search with 20 trials sees only a few of them. So the ranges are kept to values that suit a network this small: at most 4 layers and dropout rates up to 0.5. Every trial trains for the same 100 epochs as the baseline, so the scores can be compared with it.

### 8.2 The results

> **Key point:** The best of 20 trials, 2 layers with RMSProp, scored 0.779. But 11 of the 20 trials scored within the range that the baseline itself covers when only its random start changes.

![Validation accuracy of the 20 trials (best epoch of 100), ranked, each labelled with its number of layers and optimizer. Red band and dashed line: the baseline after 100 epochs, 5 seeds](images/trials.png){width=100%}

Figure 2 ranks the 20 trials. The winner, trial 2, has two hidden layers: 40 tanh nodes without dropout, then 104 ReLU nodes with dropout 0.3, trained with RMSProp. Its score is 0.779; the weakest trial scored 0.740.

The red band in Figure 2 is the baseline trained 5 times, changing only the seed: its validation accuracy ranges from 0.734 to 0.760. Eleven of the 20 trials fall inside that band. On 154 validation patients, the differences between most sensible networks are no bigger than the differences between two random starts of the same network.

The dictionary of best values also lists `units_2`, `units_3` and their partners, left over from other trials, even though the winner has only 2 layers (Notebook). Only the values of layers that exist are used when the model is built.

### 8.3 Where the results are stored

> **Key point:** Everything goes to the folder `directory/project_name`: one sub-folder per trial, each with a `trial.json` file holding the values and the score.

The tuner saves its state as it goes: an `oracle.json` file for the search, and for every trial a folder `trial_00`, `trial_01`, … with a `trial.json` (values, score) and the weights of its best epoch (Notebook). We can open these files later to analyse the trials.

> **Extra:** By default, `directory` is the current folder, `project_name` is `"untitled_project"` and `overwrite` is `False` (Keras Tuner source, `base_tuner.py`). A second tuner created with the defaults therefore reloads the first one's finished project instead of starting a new search. Its trials are already used up, so the search ends at once with the message "Oracle triggered exit". Giving each search its own `project_name`, or passing `overwrite=True`, avoids this.

## 9. Is the tuned network really better?

> **Key point:** Retrained 5 times, the tuned network averages 0.723 on validation against the baseline's 0.751, and 0.735 on the test set against 0.740. On this small dataset, tuning did not beat a sensible hand-made network.

A trial's score is the best of its 100 epochs, from one random start, on 154 patients. For a fair comparison we rebuild the baseline and the winning configuration from scratch, train each 5 times with different seeds for 100 epochs, and compare the mean validation accuracy. Only then do we look at the test set, once.

| | Baseline (5 runs) | Tuned (5 runs) |
|---|---|---|
| Validation accuracy, mean (std) | 0.751 (0.010) | 0.723 (0.011) |
| Test accuracy, mean (std) | 0.740 (0.011) | 0.735 (0.008) |

The tuned network's 0.779 shrinks to 0.723 once it is retrained. Two things inflated it:

1. **The best epoch.** A trial is scored at the best of its epochs, and its saved model is that epoch's (Keras Tuner guide; Keras Tuner source, `tuner.py`). The retrained runs are scored after the last epoch.
2. **The best of 20.** The winner is the highest of 20 scores that each carry seed-to-seed noise of about 0.01 (the baseline's standard deviation). Picking the highest favours the trial whose noise happened to be largest.

On the test set the two networks are level: 0.740 and 0.735, a gap smaller than either standard deviation. The honest result is that Keras Tuner works as designed, but on 460 training patients a one-layer network with sensible defaults is already about as good as any network in the search space. The search did rule out bad choices: Adadelta after 10 epochs (0.338) and 8 nodes (0.636) scored far below the rest in sections 5 and 6.

> **Extra:** Keras Tuner can reduce this noise inside the search itself: `executions_per_trial=2` trains every configuration twice and averages the scores, at twice the cost (Keras Tuner guide).

## 10. Summary

| Step | Code | What it does |
|------|------------------|----------|
| Mark a choice | `hp.Choice(...)` | one value from a list |
| | `hp.Int(...)` | a whole number in a range, with a step |
| Build | `build_model(hp)` | builds and compiles one network per trial |
| Tuner | `kt.RandomSearch(...)` | random combinations, best by `objective` |
| Search | `tuner.search(...)` | its arguments go to `fit` |
| Results | `get_best_hyperparameters()` | winning values, best first |
| | `get_best_models()` | winning models, best first |
| Continue | `fit(initial_epoch=k)` | resumes the epoch count after epochs 0 to $k-1$ have run |

- Keras Tuner replaces hand-picked layers, nodes, activations and optimizers with a search.
- `build_model(hp)` marks each choice; per-layer hyperparameters need per-layer names such as `f"units_{i}"`.
- `RandomSearch` draws random combinations; it stops early if no new combination is left.
- Tune on a validation set, and report the test set once at the end.
- A trial's score is noisy on a small dataset: retrain the winner with several seeds before trusting it.

## 11. Sources

- Keras Tuner guide: Invernizzi, L., Long, J., Chollet, F., O'Malley, T. and Jin, H. "Getting started with KerasTuner." keras.io/keras_tuner/getting_started (last modified 2021-10-27).
- Keras Tuner source code, version 1.4.8: `engine/base_tuner.py` (default directory and project name), `engine/oracle.py` (repeated draws, stopping), `engine/tuner.py` (best-epoch checkpoint).
- Keras source code, version 3.15.1: `optimizers/adadelta.py` (default learning rate).
- Ruder, S. (2016). An overview of gradient descent optimization algorithms. arXiv:1609.04747.

## 12. Key terms

| Term | Meaning |
|---|---|
| Hyperparameter | A setting chosen before training that the network does not learn, such as the number of layers |
| Hyperparameter tuning | Trying several hyperparameter values and keeping those that score best |
| Keras Tuner | A Python library (`keras_tuner`) that searches for good hyperparameters of a Keras model |
| Trial | One model built, trained and scored with one set of hyperparameter values |
| `build_model(hp)` | The function that builds and compiles one network, asking `hp` for each tuned value |
| `hp.Choice` | Declares a hyperparameter that takes one value from a list |
| `hp.Int` | Declares a whole-number hyperparameter between a minimum and a maximum, with an optional step |
| Conditional hyperparameter | A hyperparameter that exists only for some values of another, such as `units_3` |
| `RandomSearch` | A tuner that tries random combinations of the hyperparameter values |
| Objective | The metric the tuner maximises or minimises, such as `val_accuracy` |
| Validation set | Observations held out from training and used to choose between models |
| Test set | Observations used once, at the end, for an honest score |
| Observation | One record of the data: one row of the data table |
| Feature | An input variable, such as glucose: one column of the data table |
| Target | The output we predict, here diabetes yes or no |
