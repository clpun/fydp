from _csv import reader
import numpy


class TestCaseTable(object):
    def __init__(self, filename, time_range, correlation_table):
        self.filename = filename
        self.time_range = time_range
        self.correlation_table = correlation_table
        self.table = {}

        self.parse_data()

    def parse_data(self):
        with open(self.filename, 'rb') as csv_file:
            data_reader = reader(csv_file)
            first_row = True
            header = None

            for row in data_reader:
                if first_row:
                    first_row = False
                    header = row
                    continue
                time = float(row[0])
                for correlation in self.correlation_table.correlation_generator():
                    if self.is_time_part_of_correlation(time, (correlation[2], correlation[3])):
                        channel_name = correlation[0]
                        frequency = correlation[1]
                        correlation_frequency_index = self.index_for(header, channel_name, frequency)
                        if correlation_frequency_index is -1:
                            raise Exception('Could not find index for the correlation frequency %s' % channel_name)

                        self.update_table_for_time(channel_name, frequency, time, float(row[correlation_frequency_index]))
            
            self.convert_table_to_means()

    def update_table_for_time(self, channel_name, frequency, time, power):
        if not self.table.has_key(channel_name):
            self.table[channel_name] = {}
        if not self.table[channel_name].has_key(frequency):
            self.table[channel_name][frequency] = {1: [], 2: [], 3: []}

        if time <= self.time_range[0]:
            self.table[channel_name][frequency][1].append(power)
        elif time <= self.time_range[1]:
            self.table[channel_name][frequency][2].append(power)
        else:
            self.table[channel_name][frequency][3].append(power)

    @staticmethod
    def index_for(header, channel_name, frequency):
        i = 1
        while i < len(header):
            if header[i].startswith(channel_name):
                return i + frequency - 1
            else:
                i += 64
        return -1

    def is_time_part_of_correlation(self, time, correlation):
        first = correlation[0]
        second = correlation[1]
        if first == 1 and time < self.time_range[0]:
            return True
        elif first == 2 and self.time_range[0] <= time < self.time_range[1]:
            return True
        if (second == 3 and time >= self.time_range[1]) or (second == 2 and self.time_range[0] <= time < self.time_range[1]):
            return True
        return False

    def convert_table_to_means(self):
        num_segments = len(self.time_range)+1
        for channel_name in self.table:
            for channel_frequency in self.table[channel_name]:
                for segment in range(1, num_segments+1):
                    self.table[channel_name][channel_frequency][segment] = \
                        numpy.mean(self.table[channel_name][channel_frequency][segment])