"""Fit PCA on the 70,000 MNIST images (Keras copy, ~/.keras/datasets/mnist.npz) and store small CSVs for the figures:
one example image and the first 6 eigenvectors (components_) with their explained variance ratios. Run once; the CSVs
are kept in data/ so the figures build without the 11 MB MNIST file."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

here = Path(__file__).parent
if __name__ == "__main__" and not (here.parent / "data" / "mnist_components.csv").exists():
    z = np.load(Path.home() / ".keras" / "datasets" / "mnist.npz")
    X = np.concatenate([z["x_train"], z["x_test"]]).reshape(-1, 784).astype(float)
    pca = PCA(n_components=6, random_state=0).fit(X)
    df = pd.DataFrame(pca.components_)
    df.insert(0, "ratio", pca.explained_variance_ratio_)
    df.round(6).to_csv(here.parent / "data" / "mnist_components.csv", index=False)
    pd.DataFrame(z["x_train"][0].reshape(1, -1)).to_csv(here.parent / "data" / "mnist_example.csv", index=False)
