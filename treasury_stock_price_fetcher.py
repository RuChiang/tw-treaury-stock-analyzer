#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import csv
import time
import sys
import datetime
import numpy as np
import requests
import logging
import urllib
import random
from time import sleep
import traceback

from datetime import datetime
from utils.file_reader import FileReader

logging.basicConfig()
logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger('stock price fetcher')


req = requests.Session()
req.get('https://www.twse.com.tw/')


class Recorder(object):
    '''Record data to csv'''

    def __init__(self, path='data'):
        self.folder_path = '{}'.format('data')
        if not os.path.isdir(self.folder_path):
            os.makedirs(self.folder_path)

    def record_to_csv(self, filename, header, data):
        try:
            file_path = '{}/{}.csv'.format(self.folder_path, filename)
            with open(file_path, 'w') as output_file:
                writer = csv.writer(output_file, delimiter=',')
                writer.writerow(header)
                for day in data:
                    writer.writerow(day)

        except Exception as err:
            print(err)
            traceback.print_exc()


def get_stock_info(idx, date, data_type):
    sleep(0.5)
    return json.loads(req.get(f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={date}&stockNo={idx}&_=1592225418511",
                              headers={'Accept-Language': 'zh-TW'}).text)[data_type]


def get_index_info(date, data_type):
    sleep(0.5)
    return json.loads(req.get(f"https://www.twse.com.tw/indicesReport/MI_5MINS_HIST?response=json&date={date}&_=1592225418511",
                              headers={'Accept-Language': 'zh-TW'}).text)[data_type]


def main():

    # get src file
    src_data = sys.argv[1]
    # get list of stock indices
    target = sys.argv[2]
    file_reader = FileReader(src_data, target)
    date_ranges = file_reader.get_date_range()

    logger.debug(f"date_ranges: {date_ranges}")

    for date_range in date_ranges:

        logger.info(f"getting price range of {date_range}")
        start, end = [''.join(date.split('/')) for date in date_range]
        #  if start and end are in the same month

        start_yr = start[0:4]
        start_month = start[4:6]
        start_date = start[6:8]

        end_yr = end[0:4]
        end_month = end[4:6]
        end_date = end[6:8]

        logger.debug(f"start_yr {start_yr}")
        logger.debug(f"start_month {start_month}")
        logger.debug(f"start_date {start_date}")

        logger.debug(f"end_yr {end_yr}")
        logger.debug(f"end_month {end_month}")
        logger.debug(f"end_date {end_date}")

        [curr_year, curr_month, curr_date] = datetime.today().strftime(
            '%Y/%m/%d').split('/')
        logger.info(f"current time: {curr_year}/{curr_month}/{curr_date}")
        logger.info(f"end time: {end_yr}/{end_month}/{end_date}")

        if curr_year < end_yr or (curr_year == end_yr and curr_month < end_month) or (curr_year == end_yr and curr_month == end_month and curr_date < end_date):
            logger.warning('庫藏股回購尚未結束')
            continue

        headers = [f"股票{title}" for title in get_stock_info(target, start, "fields")] \
            + [f"發行量加權股價指數{title}" for title in get_index_info(start, "fields")
               ][1:]

        data = []

        if start_yr == end_yr and start_month == end_month:
            stock_entries = get_stock_info(target, start, "data")
            index_entries = get_index_info(start, "data")
            rows = []
            for i, row in enumerate(stock_entries):
                rows.append(row + index_entries[i][1:])
            data = data + rows
        # get months price
        elif start_yr == end_yr and start_month != end_month:
            for month in range(int(start_month), int(end_month) + 1):
                stock_entries = get_stock_info(
                    target, f"{start_yr}{str(month).rjust(2, '0')}01", "data")
                index_entries = get_index_info(
                    f"{start_yr}{str(month).rjust(2, '0')}01", "data")
                logger.debug(f"stock_entries {len(stock_entries)}")

                logger.debug(f"stock_entries {stock_entries}")
                logger.debug(f"index_entries {len(index_entries)}")

                logger.debug(f"index_entries {index_entries}")

                rows = []
                for i, row in enumerate(stock_entries):
                    rows.append(row + index_entries[i][1:])
                data = data + rows
        else:
            if int(end_yr) - int(start_yr) == 1:
                for month in range(int(start_month), 13):
                    stock_entries = get_stock_info(
                        target, f"{start_yr}{str(month).rjust(2, '0')}01", "data")
                    index_entries = get_index_info(
                        f"{start_yr}{str(month).rjust(2, '0')}01", "data")
                    rows = []
                    for i, row in enumerate(stock_entries):
                        rows.append(row + index_entries[i][1:])
                    data = data + rows

                for month in range(1, int(end_month) + 1):
                    stock_entries = get_stock_info(
                        target, f"{end_yr}{str(month).rjust(2, '0')}01", "data")
                    index_entries = get_index_info(
                        f"{end_yr}{str(month).rjust(2, '0')}01", "data")
                    rows = []
                    for i, row in enumerate(stock_entries):
                        rows.append(row + index_entries[i][1:])
                    data = data + rows
            else:
                for month in range(int(start_month), 13):
                    stock_entries = get_stock_info(
                        target, f"{start_yr}{str(month).rjust(2, '0')}01", "data")
                    index_entries = get_index_info(
                        f"{start_yr}{str(month).rjust(2, '0')}01", "data")
                    rows = []
                    for i, row in enumerate(stock_entries):
                        rows.append(row + index_entries[i][1:])
                    data = data + rows
                for year in range(int(start_yr), int(end_yr) + 1):
                    for month in range(1, 13):
                        stock_entries = get_stock_info(
                            target, f"{year}{str(month).rjust(2, '0')}01", "data")
                        index_entries = get_index_info(
                            f"{year}{str(month).rjust(2, '0')}01", "data")
                        rows = []
                        for i, row in enumerate(stock_entries):
                            rows.append(row + index_entries[i][1:])
                        data = data + rows
                for month in range(1, int(end_month) + 1):
                    stock_entries = get_stock_info(
                        target, f"{end_yr}{str(month).rjust(2, '0')}01", "data")
                    index_entries = get_index_info(
                        f"{end_yr}{str(month).rjust(2, '0')}01", "data")
                    rows = []
                    for i, row in enumerate(stock_entries):
                        rows.append(row + index_entries[i][1:])
                    data = data + rows
        # data = np.array(data)
        logger.debug(f"headers\n{headers}")
        logger.debug(f"data\n{data}")

        # sanitize the data
        sanitize_data = []
        for point in data:
            logger.debug(f"point {point}")
            yr, mon, day = point[0].split('/')
            logger.debug(f"yr {yr}")
            logger.debug(f"mon {mon}")
            logger.debug(f"day {day}")

            if int(yr) + 1911 == int(start_yr) and int(mon) == int(start_month) and int(day) < int(start_date):
                continue
            elif int(yr) + 1911 == int(end_yr) and int(mon) == int(end_month) and int(day) > int(end_date):
                continue
            else:
                sanitize_data.append(point)
        #  write to files
        recoder = Recorder()
        recoder.record_to_csv(f"{target}-{start}-{end}",
                              headers, sanitize_data)


if __name__ == '__main__':
    main()
