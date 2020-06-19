#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import csv
import time
import sys
from datetime import date
import numpy as np
import requests
import logging

from datetime import datetime


logging.basicConfig()
logging.root.setLevel(logging.INFO)

# class CrawlerController(object):
#     '''Split targets into several Crawler, avoid request url too long'''

#     def __init__(self, targets, max_stock_per_crawler=50):
#         self.crawlers = []

#         for index in range(0, len(targets), max_stock_per_crawler):
#             crawler = Crawler(targets[index:index + max_stock_per_crawler])
#             self.crawlers.append(crawler)

#     def run(self):
#         data = []
#         header = []
#         for crawler in self.crawlers:
#             header, data = crawler.get_data()
#         return header, data

# https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20200501&stockNo=2303&_=1592225418511


# class Crawler(object):
#     '''Request to Market Information System'''
#     '''For now only support one stock'''

#     def __init__(self, targets):
#         endpoint = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY'
#         # Add 1000 seconds for prevent time inaccuracy
#         # timestamp = int(time.time() * 1000 + 1000000)
#         # channels = '|'.join('tse_{}.tw'.format(target) for target in targets)
#         # self.query_url = '{}?_={}&ex_ch={}'.format(endpoint, timestamp, channels)
#         self.query_url = '{}?reponse=json&date={}&stockNo={}&_{}'.format(
#             endpoint, '20200501', '2303', int(time.time() * 1000))

#     def get_data(self):
#         try:
#             # Get original page to get session
#             req = requests.session()
#             req.get('http://mis.twse.com.tw/stock/index.jsp',
#                     headers={'Accept-Language': 'zh-TW'})

#             response = req.get(self.query_url)
#             content = json.loads(response.text)
#         except Exception as err:
#             print(err)
#             data = []
#             header = []
#         else:
#             data = content["data"]
#             header = content["fields"]

#         return header, data


class FileReader(object):
    def __init__(self, file_name, indices):
        self.file_name = file_name
        self.indices = indices

    def get_date_range(self):
        rows = []
        with open(self.file_name, newline='', encoding='utf-8', errors='replace') as csvfile:
            for cols in csv.reader(csvfile):
                if cols[1] in self.indices:
                    rows.append([cols[9], cols[10]])
        return rows


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


def main():

    logger = logging.getLogger('stock price fetcher')

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

        #  get headers
        response = requests.get(f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={start}&stockNo={target}&_=1592225418511",
                                headers={'Accept-Language': 'zh-TW'})
        content = json.loads(response.text)
        headers = content["fields"]

        data = []

        if start_yr == end_yr and start_month == end_month:
            response = requests.get(f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={start}&stockNo={target}&_=1592225418511",
                                    headers={'Accept-Language': 'zh-TW'})
            content = json.loads(response.text)
            data = data + content["data"]
        # get months price
        elif start_yr == end_yr and start_month != end_month:
            for month in range(int(start_month), int(end_month) + 1):
                response = requests.get(f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={start_yr}{str(month).rjust(2, '0')}01&stockNo={target}&_=1592225418511",
                                        headers={'Accept-Language': 'zh-TW'})
                content = json.loads(response.text)
                data = data + content["data"]
        else:
            if int(end_yr) - int(start_yr) == 1:
                for month in range(int(start_month), 13):
                    response = requests.get(f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={start_yr}{str(month).rjust(2, '0')}01&stockNo={target}&_=1592225418511",
                                            headers={'Accept-Language': 'zh-TW'})
                    content = json.loads(response.text)
                    data = data + content["data"]
                for month in range(1, int(end_month) + 1):
                    response = requests.get(f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={end_yr}{str(month).rjust(2, '0')}01&stockNo={target}&_=1592225418511",
                                            headers={'Accept-Language': 'zh-TW'})
                    content = json.loads(response.text)
                    data = data + content["data"]
            else:
                for month in range(int(start_month), 13):
                    response = requests.get(f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={start_yr}{str(month).rjust(2, '0')}01&stockNo={target}&_=1592225418511",
                                            headers={'Accept-Language': 'zh-TW'})
                    content = json.loads(response.text)
                    data = data + content["data"]
                for year in range(int(start_yr), int(end_yr) + 1):
                    for month in range(1, 13):
                        response = requests.get(f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={year}{str(month).rjust(2, '0')}01&stockNo={target}&_=1592225418511",
                                                headers={'Accept-Language': 'zh-TW'})
                    content = json.loads(response.text)
                    data = data + content["data"]
                for month in range(1, int(end_month) + 1):
                    response = requests.get(f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={start_yr}{str(month).rjust(2, '0')}01&stockNo={target}&_=1592225418511",
                                            headers={'Accept-Language': 'zh-TW'})
                    content = json.loads(response.text)
                    data = data + content["data"]
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
