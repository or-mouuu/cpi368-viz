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

ROLLING_YEARS = 10
MONTHS_PER_YEAR = 12
# 10 years of comparison window + the 12 months being compared = need at least this many months
MIN_MONTHS_FOR_10Y = ROLLING_YEARS * MONTHS_PER_YEAR + MONTHS_PER_YEAR


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
        if len(sorted_periods) < MIN_MONTHS_FOR_10Y:
            print(f"[build] skip {code} {name}: only {len(sorted_periods)} months of data", file=sys.stderr)
            continue

        # keep a rolling ~10-year window (plus a little headroom) for the sparkline
        window_periods = sorted_periods[-(ROLLING_YEARS * MONTHS_PER_YEAR + MONTHS_PER_YEAR):]
        series_values = [points[p] for p in window_periods]

        recent_12 = [points[p] for p in sorted_periods[-MONTHS_PER_YEAR:]]
        decade_ago_12 = [points[p] for p in sorted_periods[-(MIN_MONTHS_FOR_10Y):-(MIN_MONTHS_FOR_10Y - MONTHS_PER_YEAR)]]

        recent_avg = statistics.mean(recent_12)
        decade_avg = statistics.mean(decade_ago_12)
        change10y = (recent_avg / decade_avg - 1) * 100 if decade_avg else 0.0
        seasonal_var = statistics.variance(recent_12) if len(recent_12) > 1 else 0.0

        if seasonal_var > 100:
            price_type = "seasonal"
        elif change10y > 15:
            price_type = "hot"
        elif change10y >= 0:
            price_type = "normal"
        else:
            price_type = "falling"

        items.append(
            {
                "id": code,
                "name": name,
                "category": category,
                "type": price_type,
                "change10y": round(change10y, 2),
                "seasonalVar": round(seasonal_var, 2),
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
    missing = {"hot", "normal", "falling", "seasonal"} - types_present
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
