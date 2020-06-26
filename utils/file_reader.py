import csv


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

    def get_full_data(self):
        rows = []
        with open(f"{self.file_name}", newline='', encoding='utf-8', errors='replace') as csvfile:
            for cols in csv.reader(csvfile):
                if cols[1] in self.indices:
                    rows.append(cols)
        return rows
