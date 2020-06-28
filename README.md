### 安裝
```
pip install -r requirements.txt
```
### extract 所有股票代碼
所有代碼會被寫入在 `data/indices.txt`
```
python3 treasury_stock_parser.py src_data/treasury_stock_records.csv
```

### 執行抓取股價
```
python3 treasury_stock_price_fetcher.py src_data/treasury_stock_records.csv 股票代碼...

for example
python3 treasury_stock_price_fetcher.py src_data/treasury_stock_records.csv 2303

```

### 執行指定格式分析
將所有指定庫藏股資訊寫進 `data/final.csv`
```
python3 easury_stock_analyzer.py src_data/treasury_stock_records.csv 股票代碼...

for example
python3 teasury_stock_analyzer.py src_data/treasury_stock_records.csv 2303

```

### 輸出資料
在 `data` 資料夾

[庫藏股原始資料來源](https://mops.twse.com.tw/mops/web/t35sc09)