import sys
import csv
from utils.file_reader import FileReader
import logging
import os.path
import numpy as np

logging.basicConfig()
logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger('stock price fetcher')


# first use the give stock_idx to get list of dateranges in the downloaded treasury stock file
# then get the interested figures from the files under /data
# write to a new file, one file for each stock
def main():

    # get src file
    src_data = sys.argv[1]
    indices = []
    with open(src_data, newline='', encoding='utf-8', errors='replace') as csvfile:
        for cols in csv.reader(csvfile):
            indices.append(cols[1])
    indices = list(set(indices[1:]))
    logger.info(f"indices {indices}")
    with open('data/indices.txt', 'w') as output:
        for index in indices:
            output.write(f"{index} ")


if __name__ == '__main__':
    main()
