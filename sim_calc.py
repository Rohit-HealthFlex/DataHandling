import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw


def compute_euclidean_distance_matrix(x, y) -> np.array:
    """Calculate distance matrix
    This method calcualtes the pairwise Euclidean distance between two sequences.
    The sequences can have different lengths.
    """
    dist = np.zeros((len(y), len(x)))
    for i in range(len(y)):
        for j in range(len(x)):
            dist[i, j] = (x[j]-y[i])**2
    return dist


def compute_accumulated_cost_matrix(x, y) -> np.array:
    """Compute accumulated cost matrix for warp path using Euclidean distance
    """
    distances = compute_euclidean_distance_matrix(x, y)

    # Initialization
    cost = np.zeros((len(y), len(x)))
    cost[0, 0] = distances[0, 0]

    for i in range(1, len(y)):
        cost[i, 0] = distances[i, 0] + cost[i-1, 0]

    for j in range(1, len(x)):
        cost[0, j] = distances[0, j] + cost[0, j-1]

    # Accumulated warp path cost
    for i in range(1, len(y)):
        for j in range(1, len(x)):
            cost[i, j] = min(
                cost[i-1, j],    # insertion
                cost[i, j-1],    # deletion
                cost[i-1, j-1]   # match
            ) + distances[i, j]

    return cost


def compute_dtw(x, y):
    dtw_distance, warp_path = fastdtw(x, y, dist=euclidean)
    return dtw_distance, warp_path


if __name__ == "__main__":
    x = np.array([2, 2, 1, 3, 1, 2, 2, 4, 56, 6, 45, 4]).reshape(-1, 1)
    y = np.array([2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 2, 2, 2,
                  2, 4, 56, 6, 45, 4]).reshape(-1, 1)
    print(x.shape, y.shape)

    dist, warp = compute_dtw(x, y)
    print(dist)
    print(warp)
