"""
=========================
Repeated Edited nearest-neighbours
=========================

An illustration of the edited nearest-neighbours and repeated 
edited nearest-neighbours method combined in a pipeline object.

"""

print(__doc__)

import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# Define some color for the plotting
almost_black = '#262626'
palette = sns.color_palette()

from sklearn.datasets import make_classification
from sklearn.decomposition import PCA

from unbalanced_dataset.under_sampling import EditedNearestNeighbours, \
    RepeatedEditedNearestNeighbours
from unbalanced_dataset.pipeline import make_pipeline

# Generate the dataset
X, y = make_classification(n_classes=2, class_sep=1.25, weights=[0.3, 0.7],
                           n_informative=3, n_redundant=1, flip_y=0,
                           n_features=5, n_clusters_per_class=1,
                           n_samples=5000, random_state=10)


# Fit and transform x to visualise inside a 2D feature space
pca = PCA(n_components=2)
X_vis = pca.fit_transform(X)

# Three subplots, unpack the axes array immediately
f, (ax1, ax3) = plt.subplots(1, 2)

ax1.scatter(X_vis[y == 0, 0], X_vis[y == 0, 1], label="Class #0", alpha=.5,
            edgecolor=almost_black, facecolor=palette[0], linewidth=0.15)
ax1.scatter(X_vis[y == 1, 0], X_vis[y == 1, 1], label="Class #1", alpha=.5,
            edgecolor=almost_black, facecolor=palette[2], linewidth=0.15)
ax1.set_title('Original set')

# Create the samplers
enn = EditedNearestNeighbours()
renn = RepeatedEditedNearestNeighbours()

# Add the samplers in the pipeline
pipeline = make_pipeline(enn, renn)
X_resampled, y_resampled = pipeline.fit_sample(X, y)
X_res_vis = pca.transform(X_resampled)

ax3.scatter(X_res_vis[y_resampled == 0, 0], X_res_vis[y_resampled == 0, 1],
            label="Class #0", alpha=.5, edgecolor=almost_black,
            facecolor=palette[0], linewidth=0.15)
ax3.scatter(X_res_vis[y_resampled == 1, 0], X_res_vis[y_resampled == 1, 1],
            label="Class #1", alpha=.5, edgecolor=almost_black,
            facecolor=palette[2], linewidth=0.15)
ax3.set_title('RENN + ENN ')

plt.show()