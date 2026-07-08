"""Fetch the CPI basic-classification + item-group index XML from data.gov.tw dataset 9158.

The dataset page (https://data.gov.tw/dataset/9158) republishes a fresh XML file
under ws.dgbas.gov.tw every month with a rotating path, so we resolve the current
download URL through the stable data.gov.tw REST API instead of hardcoding a path.
"""
import sys
import tempfile
from pathlib import Path

import certifi
import requests

DATASET_API = "https://data.gov.tw/api/v2/rest/dataset/9158"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; cpi368-viz/1.0)"}
RAW_DIR = Path(__file__).parent / "raw"
RAW_XML = RAW_DIR / "cpi_items.xml"
TWCA_EXTRA_CA = Path(__file__).parent / "certs" / "twca-extra.pem"


def trust_bundle() -> str:
    """ws.dgbas.gov.tw's TLS chain is signed by TWCA/ePKI roots that Mozilla's
    (and therefore certifi's) bundle doesn't include. Build a combined bundle
    of certifi's roots plus the TWCA chain so both data.gov.tw and
    ws.dgbas.gov.tw verify cleanly."""
    combined = certifi.contents() + "\n" + TWCA_EXTRA_CA.read_text()
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".pem", delete=False)
    tmp.write(combined)
    tmp.close()
    return tmp.name


VERIFY = trust_bundle()


def resolve_download_url() -> str:
    resp = requests.get(DATASET_API, headers=HEADERS, timeout=30, verify=VERIFY)
    resp.raise_for_status()
    payload = resp.json()
    distribution = payload["result"]["distribution"]
    if not distribution:
        raise RuntimeError("dataset 9158 回應沒有 distribution，資料源可能異動")
    url = distribution[0]["resourceDownloadUrl"]
    if not url.startswith("https://ws.dgbas.gov.tw/"):
        raise RuntimeError(f"resourceDownloadUrl 網域不是預期的 ws.dgbas.gov.tw：{url}")
    return url


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    url = resolve_download_url()
    print(f"[fetch] downloading {url}")
    resp = requests.get(url, headers=HEADERS, timeout=60, verify=VERIFY)
    resp.raise_for_status()
    if len(resp.content) < 100_000:
        raise RuntimeError(f"下載內容過小（{len(resp.content)} bytes），可能是錯誤頁面")
    RAW_XML.write_bytes(resp.content)
    print(f"[fetch] saved {len(resp.content)} bytes to {RAW_XML}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"[fetch] FAILED: {exc}", file=sys.stderr)
        sys.exit(1)
