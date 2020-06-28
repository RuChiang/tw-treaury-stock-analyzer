import sys
import csv
from utils.file_reader import FileReader
import logging
import os.path
import numpy as np

logging.basicConfig()
logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger('stock price analyzer')


# first use the give stock_idx to get list of dateranges in the downloaded treasury stock file
# then get the interested figures from the files under /data
# write to a new file, one file for each stock
def main():
    # get src file
    src_data = sys.argv[1]
    # get list of stock indices
    targets = sys.argv[2:]
    final_data = []
    headers = ['序號',	'公司代號',	'公司名稱',	'董事會決議日期', '買回目的',	'買回股份總金額上限(依最新財報計算之法定上限)',	'預定買回股數',	'買回價格區間-最低',	'買回價格區間-最高',	'預定買回期間-起',	'預定買回期間-迄',	'是否執行完畢',	'買回達一定標準資料',	'本次已買回股數(空白為尚在執行中)',	'本次執行完畢已註銷或轉讓股數',
               '本次已買回股數佔預定買回股數比例(%)(空白為尚<br>在執行中)',	'本次已買回總金額(空白為尚在執行中)',	'本次平均每股買回價格(空白為尚在執行中)',	'本次買回股數佔公司已發行股份總數比例(%)(空白為尚在執行中)',	'執行日開盤價',	'執行期間最高價',	'執行期間最低價',	'執行終止日收盤價',	'執行日大盤開盤價',	'執行期間大盤最高價',	'執行期間大盤最低價',	'執行終止日大盤收盤價']
    for target in targets:
        file_reader = FileReader(src_data, target)
        data = file_reader.get_full_data()
        date_ranges = file_reader.get_date_range()

        logger.debug(f"date_ranges: {date_ranges}")

        # one date_range will be one entry in the resulting file
        for cnt, date_range in enumerate(date_ranges):
            start, end = [''.join(date.split('/')) for date in date_range]
            fname = f"data/{target}-{start}-{end}.csv"
            if os.path.isfile(fname) == True:
                stock_duration_highest = stock_duration_lowest = stock_duration_open = stock_duration_close = None
                index_duration_highest = index_duration_lowest = index_duration_open = index_duration_close = None

                price_data = []
                open_close_price = []
                with open(fname, newline='', encoding='utf-8', errors='replace') as csvfile:
                    for row_cnt, cols in enumerate(csv.reader(csvfile)):
                        logger.debug(f"cols {cols}")
                        # ignore the first row header
                        if row_cnt >= 1:
                            # get the open and close values

                            # stock_h, stock_l, index_h, index_l
                            price_data.append([float(''.join(col.split(',')))
                                               for col in (cols[4:6] + cols[10:12])])
                            open_close_price.append([float(''.join(col.split(',')))
                                                     for col in [cols[3], cols[6], cols[9], cols[12]]])
                    stock_duration_open = open_close_price[0][0]
                    stock_duration_close = open_close_price[-1][1]
                    index_duration_open = open_close_price[0][2]
                    index_duration_close = open_close_price[-1][3]
                price_data = np.array(price_data)
                logger.debug(f" {price_data}")

                stock_duration_highest, index_duration_highest = np.amax(
                    price_data[:, [0, 2]], axis=0)
                stock_duration_lowest, index_duration_lowest = np.amin(
                    price_data[:, [1, 3]], axis=0)
                final_data.append(data[cnt][:-1]+[str(stock_duration_open), str(stock_duration_highest), str(stock_duration_lowest), str(stock_duration_close),
                                                  str(index_duration_open), str(index_duration_highest), str(index_duration_lowest), str(index_duration_close)])
                logger.debug(f"open_close_price {open_close_price}")
                logger.debug(f"final_data {final_data}")
            else:
                logger.error(fname)

    with open(f"data/final.csv", 'w') as output_file:
        writer = csv.writer(output_file, delimiter=',')
        logger.debug(f"headers.length {len(headers)}")
        writer.writerow(headers)
        for row in final_data:
            logger.debug(f"row.length {len(row)}")
            writer.writerow(row)
        logger.info('finished compiling final file')


if __name__ == '__main__':
    main()
