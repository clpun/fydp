from csv import reader
import numpy


class CorrelationTable(object):
    def __init__(self, filename):
        self.filename = filename
        self.table = {}
        self.parse_data()

    def parse_data(self):
        with open(self.filename, 'rU') as csv_file:
            data_reader = reader(csv_file)
            parsed_rows = []
            first_row = True
            for row in data_reader:
                if first_row:
                    first_row = False
                    continue
                parsed_rows.append(tuple(row))
            self.table = numpy.rec.array(parsed_rows,
                                         dtype=[('CH', '|S8'), ('frequency', '<i4'), ('C1', '<i4'), ('C2', '<i4')])

    def correlation_generator(self):
        for correlation in self.table:
            yield correlation