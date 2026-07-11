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
model = AgglomerativeClustering(n_clusters=4, metric='euclidean', linkage='ward')
labels = model.fit_predict(X)

plt.figure(figsize=(12, 8))
# The labels are 0(A), 1(B), 2(C), 3(D) in order of the crosstab
names = ["A", "B", "C", "D"]
for k in range(4):
    mean_curve = np.mean(X[labels == k], axis=0)
    plt.plot(mean_curve, label=f'統計-{names[k]} (n={sum(labels==k)})', linewidth=2)

plt.legend()
plt.savefig('analysis/clusters_resampled.png')
