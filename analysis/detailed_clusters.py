import json
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

with open("public/data/items.json", "r") as f:
    data = json.load(f)

increasing_items = []
normalized_series = []

for item in data["items"]:
    if item.get("change10y", 0) > 10:
        series = np.array(item["series"])
        if len(series) < 12: continue
        ma12 = np.convolve(series, np.ones(12)/12, mode='valid')
        min_val, max_val = np.min(ma12), np.max(ma12)
        norm = np.zeros_like(ma12) if max_val == min_val else (ma12 - min_val) / (max_val - min_val)
        
        x_old = np.linspace(0, 1, len(norm))
        x_new = np.linspace(0, 1, 100)
        norm_resampled = interp1d(x_old, norm, kind='linear')(x_new)
        
        increasing_items.append(item)
        normalized_series.append(norm_resampled)

X = np.array(normalized_series)

def analyze_k(k, filename):
    model = AgglomerativeClustering(n_clusters=k, metric='euclidean', linkage='ward')
    labels = model.fit_predict(X)
    
    plt.figure(figsize=(14, 8))
    print(f"\n--- Analysis for k={k} ---")
    for c in range(k):
        cluster_data = X[labels == c]
        mean_curve = np.mean(cluster_data, axis=0)
        n = len(cluster_data)
        
        # Plot
        plt.plot(mean_curve, label=f'Cluster {c} (n={n})', linewidth=2)
        
        # Summary
        v0, v33, v66, v100 = mean_curve[0], mean_curve[33], mean_curve[66], mean_curve[-1]
        
        # get example names
        examples = [increasing_items[i]["name"] for i in range(len(increasing_items)) if labels[i] == c][:5]
        print(f"Cluster {c} (n={n}):")
        print(f"  Shape: 0%={v0:.2f}, 33%={v33:.2f}, 66%={v66:.2f}, 100%={v100:.2f}")
        print(f"  Examples: {', '.join(examples)}")
        
    plt.legend()
    plt.title(f'Mean Curves for k={k}')
    plt.savefig(filename)
    plt.close()

analyze_k(6, 'analysis/clusters_k6.png')
analyze_k(8, 'analysis/clusters_k8.png')

