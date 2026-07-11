import json
import numpy as np
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt

with open("public/data/items.json", "r") as f:
    data = json.load(f)

increasing_items = [item for item in data["items"] if item.get("change10y", 0) > 10]
normalized_series = []
for item in increasing_items:
    series = np.array(item["series"])
    if len(series) < 12:
        continue
    ma12 = np.convolve(series, np.ones(12)/12, mode='valid')
    min_val, max_val = np.min(ma12), np.max(ma12)
    norm = np.zeros_like(ma12) if max_val == min_val else (ma12 - min_val) / (max_val - min_val)
    normalized_series.append(norm)

X = np.array(normalized_series)
model = AgglomerativeClustering(n_clusters=4, metric='euclidean', linkage='ward')
labels = model.fit_predict(X)

plt.figure(figsize=(12, 8))
cluster_names = ["Cluster 0", "Cluster 1", "Cluster 2", "Cluster 3"]
# We will just plot the mean and std dev of each cluster
for k in range(4):
    cluster_data = X[labels == k]
    mean_curve = np.mean(cluster_data, axis=0)
    plt.plot(mean_curve, label=f'Cluster {k} (n={len(cluster_data)})', linewidth=2)

plt.title('Normalized Mean Shapes of 4 Clusters (Increasing Items)')
plt.legend()
plt.savefig('analysis/clusters.png')
