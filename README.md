# 安裝
```
pip install -r requirements.txt
```

# 執行抓取股價
```
python3 treasury_stock_price_fetcher.py src_data/treasury_stock_records.csv <股票代碼>

for example
python3 treasury_stock_price_fetcher.py src_data/treasury_stock_records.csv 2303

```

# 執行指定格式分析
```
python3 easury_stock_analyzer.py src_data/treasury_stock_records.csv <股票代碼>

for example
python3 teasury_stock_analyzer.py src_data/treasury_stock_records.csv 2303

```

# 輸出資料
在 `/data` 資料夾