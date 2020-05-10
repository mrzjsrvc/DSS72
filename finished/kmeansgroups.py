from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

# Takes data as Nx2 matrix & array of acceptable group sizes to test(must be <= to N in matrix)
# Returns best group size, and the assignment of the points to the groups as array
def get_groups(X, range_n_clusters=[2, 3, 4]):

    best_score = 0
    best_score_group_amount = range_n_clusters[0]
    best_assignment = None

    for n_clusters in range_n_clusters:
        clusterer = KMeans(n_clusters=n_clusters, random_state=10)
        cluster_labels = clusterer.fit_predict(X)

        silhouette_label_score = silhouette_score(X, cluster_labels)
        print("For n_clusters =", n_clusters, "The average silhouette_score is :", silhouette_label_score)
        sample_silhouette_values = silhouette_samples(X, cluster_labels)

        if best_score <= silhouette_label_score:
            best_score = silhouette_label_score
            best_score_group_amount = n_clusters
            best_assignment = cluster_labels

    return best_assignment.tolist(), best_score_group_amount
