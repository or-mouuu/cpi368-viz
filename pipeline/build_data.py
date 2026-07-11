"""Parse the raw CPI item-group XML into public/data/items.json for the frontend.

Source: dataset 9158 (消費者物價基本分類暨項目群指數), item level = "項目群" (368 items),
coded 1-368 with fixed category code ranges (see CATEGORY_RANGES below), confirmed by
inspecting the official item listing boundaries.
"""
import json
import re
import statistics
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

RAW_XML = Path(__file__).parent / "raw" / "cpi_items.xml"
OUT_JSON = Path(__file__).parent.parent / "public" / "data" / "items.json"

SUFFIX_RE = re.compile(r"\(指數基期：民國\d+年=100\)$")
LEAF_CODE_RE = re.compile(r"^(\d{1,3})(?=[^\d.])(.+)$")

# Three item-group rows come back malformed in the source XML: the item code (246)
# is glued to an octane-grade suffix with no separator (e.g. "24692無鉛汽油" instead
# of "246無鉛汽油(92)"). Codes 247/248 never separately exist upstream either -
# 246-248 are all folded into this one gasoline item split by octane grade.
MALFORMED_FIXES = {
    "24692無鉛汽油": (246, "無鉛汽油(92)"),
    "24795無鉛汽油": (247, "無鉛汽油(95)"),
    "24898無鉛汽油": (248, "無鉛汽油(98)"),
}

CATEGORY_RANGES = [
    (1, 171, "食物類"),
    (172, 194, "衣著類"),
    (195, 240, "居住類"),
    (241, 270, "交通及通訊類"),
    (271, 291, "醫藥保健類"),
    (292, 339, "教養娛樂類"),
    (340, 368, "雜項類"),
]

MONTHS_PER_YEAR = 12
# Rebase every series to the earliest year the source actually has (2013) rather
# than a rolling N-year window. Items first tracked later than this (e.g. 鯖魚/
# 南瓜, only surveyed since 2022) are excluded - they can't be compared "since
# 2013" at all. A handful of items that DO start in 2013 but have sparse early
# coverage (some seasonal fruits) still start within BASE_YEAR itself, just not
# on January - only the year is checked, not the month.
BASE_YEAR = 2013
# still need enough data points for the trend/shape math: a 12mo rolling
# mean eats the first 11 months, and late3/momentum look back 37/13 months
# into the resulting trend line
MIN_MONTHS_FOR_TREND = MONTHS_PER_YEAR - 1 + 37

# Classification thresholds (v3 2026-07-11; v3.1 steady split 2026-07-11) - see docs/METHODOLOGY.md.
VOLATILITY_THRESHOLD = 15.0  # % deviation around trend that separates年年震盪 from多年一次行情
RISING_THRESHOLD = 10.0      # trend change % above which an item counts as 上漲
FALLING_THRESHOLD = -5.0     # trend change % below which an item counts as 越來越俗
SURGE_LATE_SHARE = 0.55      # share of the rise in the last 3 years -> 近期急漲
PLATEAU_LATE_SHARE = 0.15    # rise essentially finished before the last 3 years -> 漲後不跌
PLATEAU_MAX_MOMENTUM = 1.5   # % trend growth over the last 12 months still counts as flat
# v3.1: the old 持續上漲 blob (47% of items) is split by comparing the trend's
# first-half vs second-half slope, following the shape-clustering analysis in
# analysis/cluster_increasing.py + compare_classifications.py
ACCEL_SLOPE_RATIO = 2.5   # second-half slope > 2.5x first-half -> 越漲越快
ACCEL_MIN_SLOPE2 = 0.5    # ...and the late slope must be meaningful on its own
DECEL_SLOPE_RATIO = 2.0   # first-half slope > 2x second-half -> merged into 漲後不跌


def shape_metrics(series: list[float]) -> dict:
    """Trajectory-shape metrics on a 12-month rolling-mean trend line.

    The rolling mean strips seasonal oscillation so that trend direction and
    the volatility *around* the trend can be measured independently."""
    trend = [
        statistics.mean(series[i - MONTHS_PER_YEAR + 1 : i + 1])
        for i in range(MONTHS_PER_YEAR - 1, len(series))
    ]
    t0, tn = trend[0], trend[-1]
    total_change = (tn / t0 - 1) * 100 if t0 else 0.0

    deviations = [series[MONTHS_PER_YEAR - 1 + j] / trend[j] - 1 for j in range(len(trend)) if trend[j]]
    volatility = statistics.pstdev(deviations) * 100 if len(deviations) > 1 else 0.0

    total_gain = tn - t0
    late3 = (tn - trend[-37]) / total_gain if abs(total_gain) > 1e-9 and len(trend) >= 37 else 0.0
    momentum = (tn / trend[-13] - 1) * 100 if len(trend) >= 13 and trend[-13] else 0.0

    peak = max(trend)
    gain_at_peak = (peak / t0 - 1) * 100 if t0 else 0.0
    retrace = (peak - tn) / (peak - t0) if peak > t0 * 1.001 else 0.0

    # first-half vs second-half trend slope, normalized by the trend's mean
    # level (x1000) so items of different price levels are comparable
    half = len(trend) // 2
    mean_level = statistics.mean(trend)
    slope1 = _ls_slope(trend[:half]) / mean_level * 1000 if mean_level else 0.0
    slope2 = _ls_slope(trend[half:]) / mean_level * 1000 if mean_level else 0.0

    return {
        "total_change": total_change,
        "volatility": volatility,
        "late3": late3,
        "momentum": momentum,
        "gain_at_peak": gain_at_peak,
        "retrace": retrace,
        "slope1": slope1,
        "slope2": slope2,
    }


def _ls_slope(values: list[float]) -> float:
    """Least-squares slope of values against their 0..n-1 index."""
    n = len(values)
    if n < 2:
        return 0.0
    x_mean = (n - 1) / 2
    y_mean = statistics.mean(values)
    num = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(values))
    den = sum((i - x_mean) ** 2 for i in range(n))
    return num / den if den else 0.0


def classify(m: dict) -> str:
    """v3.1 漲相 classification: macro 上漲/持平/下跌, with the rising tier
    subdivided by HOW it rose rather than how much. The former catch-all
    持續上漲 is further split by slope shape (accelerating vs linear), with
    clearly decelerating items folded into 漲後不跌."""
    if m["total_change"] > RISING_THRESHOLD:
        if m["volatility"] > VOLATILITY_THRESHOLD:
            return "wavy"  # 波動上漲
        if m["late3"] >= SURGE_LATE_SHARE:
            return "surge"  # 近期急漲
        if m["late3"] <= PLATEAU_LATE_SHARE and m["momentum"] < PLATEAU_MAX_MOMENTUM:
            return "plateau"  # 漲後不跌
        if m["slope1"] > DECEL_SLOPE_RATIO * max(m["slope2"], 0.01):
            return "plateau"  # 早期漲完、近年明顯趨緩 -> 性格上就是漲後不跌
        if m["slope2"] > ACCEL_SLOPE_RATIO * max(m["slope1"], 0.01) and m["slope2"] > ACCEL_MIN_SLOPE2:
            return "accel"  # 越漲越快
        return "steady"  # 穩定上漲
    if m["total_change"] < FALLING_THRESHOLD:
        return "cheaper"  # 越來越俗
    return "flat"  # 價格持平


def is_price_event(m: dict) -> bool:
    """One-off boom-then-bust price events (egg shortage, garlic spike...):
    rose >20% at peak, gave back >40% of the rise, and is not a seasonal oscillator."""
    return m["gain_at_peak"] > 20 and m["retrace"] > 0.4 and m["volatility"] <= VOLATILITY_THRESHOLD


def category_for_code(code: int) -> str:
    for lo, hi, name in CATEGORY_RANGES:
        if lo <= code <= hi:
            return name
    raise ValueError(f"code {code} out of known category ranges")


def period_key(period: str) -> tuple[int, int]:
    # "2013M01" -> (2013, 1)
    year, month = period.split("M")
    return int(year), int(month)


def parse_leaf(raw_name: str) -> tuple[int, str] | None:
    clean = SUFFIX_RE.sub("", raw_name).strip()
    if clean in MALFORMED_FIXES:
        return MALFORMED_FIXES[clean]
    m = LEAF_CODE_RE.match(clean)
    if not m:
        return None
    code = int(m.group(1))
    if not (1 <= code <= 368):
        return None
    return code, m.group(2).strip()


def load_series() -> dict[str, dict[tuple[int, int], float]]:
    tree = ET.parse(RAW_XML)
    root = tree.getroot()
    series: dict[str, dict[tuple[int, int], float]] = {}
    for obs in root.findall("Obs"):
        item = obs.findtext("Item", "").strip()
        freq = obs.findtext("FREQ", "").strip()
        type_ = obs.findtext("TYPE", "").strip()
        period = obs.findtext("TIME_PERIOD", "").strip()
        value_text = (obs.findtext("Item_VALUE") or "").strip()
        if freq != "M" or type_ != "原始值" or not value_text:
            continue
        try:
            value = float(value_text)
        except ValueError:
            continue
        series.setdefault(item, {})[period_key(period)] = value
    return series


def build_items(series: dict[str, dict[tuple[int, int], float]]) -> list[dict]:
    items = []
    for raw_name, points in series.items():
        parsed = parse_leaf(raw_name)
        if parsed is None:
            continue  # top-level total / mid-level rollup rows, not a leaf item
        code, name = parsed
        category = category_for_code(code)

        sorted_periods = sorted(points.keys())
        if not sorted_periods or sorted_periods[0][0] > BASE_YEAR:
            print(
                f"[build] skip {code} {name}: first tracked {sorted_periods[0] if sorted_periods else 'never'}, "
                f"not available since {BASE_YEAR}",
                file=sys.stderr,
            )
            continue
        if len(sorted_periods) < MIN_MONTHS_FOR_TREND:
            print(f"[build] skip {code} {name}: only {len(sorted_periods)} months of data", file=sys.stderr)
            continue

        # use the item's full history from its first tracked month (all in
        # BASE_YEAR or later, per the check above) through the latest release
        window_periods = sorted_periods
        series_values = [points[p] for p in window_periods]

        metrics = shape_metrics(series_values)
        price_type = classify(metrics)

        items.append(
            {
                "id": code,
                "name": name,
                "category": category,
                "type": price_type,
                "change10y": round(metrics["total_change"], 2),
                "volatility": round(metrics["volatility"], 2),
                "volatile": metrics["volatility"] > VOLATILITY_THRESHOLD and price_type != "wavy",
                "event": is_price_event(metrics),
                "series": [round(v, 2) for v in series_values],
                "periods": [f"{y}-{m:02d}" for y, m in window_periods],
            }
        )
    items.sort(key=lambda it: it["id"])
    return items


def sanity_check(items: list[dict]) -> None:
    if not (300 <= len(items) <= 400):
        raise RuntimeError(f"item count out of expected range: {len(items)}")
    types_present = {it["type"] for it in items}
    missing = {"steady", "accel", "plateau", "surge", "wavy", "flat", "cheaper"} - types_present
    if missing:
        raise RuntimeError(f"no items found for type(s): {missing}")
    for it in items:
        if not it["series"] or all(v == 0 for v in it["series"]):
            raise RuntimeError(f"item {it['id']} {it['name']} has an empty/zero series")
    categories_present = {it["category"] for it in items}
    expected_categories = {c for _, _, c in CATEGORY_RANGES}
    if categories_present != expected_categories:
        raise RuntimeError(f"category mismatch: {categories_present} vs {expected_categories}")


def main() -> None:
    if not RAW_XML.exists():
        raise SystemExit(f"raw XML not found at {RAW_XML}, run fetch.py first")
    series = load_series()
    items = build_items(series)
    sanity_check(items)

    all_periods = sorted({p for it in items for p in it["periods"]})
    meta = {
        "itemCount": len(items),
        "dataStart": all_periods[0] if all_periods else None,
        "dataEnd": all_periods[-1] if all_periods else None,
        "baseYear": BASE_YEAR,
        "basePeriod": "民國110年=100 (2021=100)",
        "source": "行政院主計總處 - 消費者物價基本分類暨項目群指數 (data.gov.tw dataset 9158)",
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps({"meta": meta, "items": items}, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"[build] wrote {len(items)} items to {OUT_JSON}")
    print(f"[build] data range: {meta['dataStart']} .. {meta['dataEnd']}")


if __name__ == "__main__":
    main()
