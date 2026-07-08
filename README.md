# 368種物價漲相大調查

台灣消費者物價指數 368 個查價項目的互動視覺化網站。資料來自行政院主計總處「消費者物價基本分類暨項目群指數」（[data.gov.tw dataset 9158](https://data.gov.tw/dataset/9158)），每月自動更新。

## 開發

```bash
npm install
npm run dev
```

## 資料 Pipeline

```bash
python3 -m venv .venv && ./.venv/bin/pip install -r pipeline/requirements.txt
./.venv/bin/python pipeline/fetch.py     # 下載最新 XML
./.venv/bin/python pipeline/build_data.py  # 產出 public/data/items.json
```

`pipeline/fetch.py` 透過 data.gov.tw 的穩定 REST API 解析目前的 XML 下載連結（該連結每月會換路徑），並用 `pipeline/certs/twca-extra.pem` 補足 Python 對 TWCA/ePKI 憑證鏈的信任（curl／macOS 系統信任庫本來就有，但 Python 的 certifi 套件沒有）。

## 建置與部署

```bash
npm run build
```

`.github/workflows/update.yml` 每月自動重新抓資料、重建、部署到 GitHub Pages；也可用 workflow_dispatch 手動觸發。
