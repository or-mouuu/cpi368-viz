import json
import numpy as np

with open("public/data/items.json", "r") as f:
    data = json.load(f)

steady_items = [item for item in data["items"] if item["type"] == "steady"]

classifications = {"linear": 0, "accelerating": 0, "decelerating": 0, "steplike": 0, "other": 0}
sub_cats = []

for item in steady_items:
    series = np.array(item["series"])
    if len(series) < 12:
        continue
    ma12 = np.convolve(series, np.ones(12)/12, mode='valid')
    
    x = np.arange(len(ma12))
    slope, intercept = np.polyfit(x, ma12, 1)
    y_pred = slope * x + intercept
    ss_res = np.sum((ma12 - y_pred)**2)
    ss_tot = np.sum((ma12 - np.mean(ma12))**2)
    r2 = 1 - (ss_res / ss_tot)
    
    half = len(ma12) // 2
    slope1, _ = np.polyfit(x[:half], ma12[:half], 1)
    slope2, _ = np.polyfit(x[half:], ma12[half:], 1)
    accel_ratio = slope2 / (slope1 + 1e-5)
    
    diffs = np.diff(ma12)
    max_jump = np.max(diffs)
    avg_jump = np.mean(np.abs(diffs))
    jumpiness = max_jump / (avg_jump + 1e-5)
    
    # Simple rule-based classification for the steady items
    cat = "other"
    if jumpiness > 5.0 and r2 < 0.9: 
        cat = "steplike" # 階梯式上漲 (Long flats, sudden jumps)
    elif accel_ratio > 2.0 and slope2 > 0:
        cat = "accelerating" # 加速上漲 (Steeper recently)
    elif accel_ratio < 0.5 and slope1 > 0:
        cat = "decelerating" # 減速上漲 (Early steep, now flattening)
    elif r2 > 0.8:
        cat = "linear" # 平穩上漲 (Highly linear trend)
    
    classifications[cat] += 1
    sub_cats.append((cat, item["name"]))

print("Distribution:")
for k, v in classifications.items():
    print(f"{k}: {v}")
    examples = [name for c, name in sub_cats if c == k][:5]
    print(f"  Examples: {', '.join(examples)}")

