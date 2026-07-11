import json
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import warnings

warnings.filterwarnings("ignore")

with open("public/data/items.json", "r") as f:
    data = json.load(f)

# Filter items that have 10-year change > 10% (i.e. 上漲)
increasing_items = [item for item in data["items"] if item.get("change10y", 0) > 10]
print(f"Total increasing items: {len(increasing_items)}")

# We will extract shape features for clustering. 
# Another approach is to cluster the normalized time series directly. Let's do both or pick the better one.
# Normalizing the 12-month moving average to [0, 1] captures the shape perfectly.
normalized_series = []
item_names = []
item_objs = []

for item in increasing_items:
    series = np.array(item["series"])
    if len(series) < 12:
        continue
    ma12 = np.convolve(series, np.ones(12)/12, mode='valid')
    # Normalize to 0-1
    min_val = np.min(ma12)
    max_val = np.max(ma12)
    if max_val - min_val == 0:
        norm = np.zeros_like(ma12)
    else:
        norm = (ma12 - min_val) / (max_val - min_val)
    normalized_series.append(norm)
    item_names.append(item["name"])
    item_objs.append(item)

X = np.array(normalized_series)

# Let's find the best k using Silhouette Score on K-Means or Agglomerative
best_k = 2
best_score = -1
best_labels = None
best_model = None

for k in range(3, 9):
    model = AgglomerativeClustering(n_clusters=k, metric='euclidean', linkage='ward')
    labels = model.fit_predict(X)
    score = silhouette_score(X, labels)
    print(f"k={k}, silhouette={score:.4f}")
    if score > best_score:
        best_score = score
        best_k = k
        best_labels = labels

print(f"\nBest K: {best_k} with silhouette score: {best_score:.4f}")

# Analyze the clusters found
clusters = {i: [] for i in range(best_k)}
for i, label in enumerate(best_labels):
    clusters[label].append((item_names[i], item_objs[i], X[i]))

# For each cluster, we can summarize the mean curve shape to name them
print("\nCluster Summaries:")
summary = {}
for k in range(best_k):
    items_in_cluster = clusters[k]
    names = [x[0] for x in items_in_cluster]
    mean_curve = np.mean([x[2] for x in items_in_cluster], axis=0)
    
    # Calculate simple metrics on the mean curve to describe it
    x_axis = np.arange(len(mean_curve))
    slope, _ = np.polyfit(x_axis, mean_curve, 1)
    
    half = len(mean_curve) // 2
    s1, _ = np.polyfit(x_axis[:half], mean_curve[:half], 1)
    s2, _ = np.polyfit(x_axis[half:], mean_curve[half:], 1)
    
    # late3 contribution: last 36 months change vs total change
    # mean_curve is 0 to 1, so total change is 1
    # ma12 reduces 132 to 121 points. Last 36 months in ma12 corresponds to roughly last 36 points.
    late3_start = len(mean_curve) - 36
    late3_change = mean_curve[-1] - mean_curve[late3_start]
    
    early_change = mean_curve[half] - mean_curve[0]
    
    desc = f"Count: {len(names)}\n"
    desc += f"  Slope1: {s1*1000:.2f}, Slope2: {s2*1000:.2f}\n"
    desc += f"  Late3 Change % of normalized: {late3_change*100:.1f}%\n"
    desc += f"  Examples: {', '.join(names[:7])}\n"
    print(f"Cluster {k}:\n{desc}")
    summary[k] = {"count": len(names), "mean_curve": mean_curve.tolist(), "names": names, "s1": s1, "s2": s2}

# Write summary to a JSON file for further inspection if needed
with open("analysis/cluster_results.json", "w") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

