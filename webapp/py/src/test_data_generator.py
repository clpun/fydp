from random import randrange
from gevent import sleep


class TestDataGenerator(object):
    def __init__(self):
        self.signal_types = ['delta', 'theta', 'alpha', 'beta', 'gamma']
        self.sensor_names = ['F3', 'FC5', 'AF3', 'F7', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'F8', 'AF4', 'FC6', 'F4']
        self.keep_generating = False

    def generate_data(self):
        self.keep_generating = True
        while self.keep_generating:
            sleep(0.25)
            dict_to_yield = {}
            for signal_type in self.signal_types:
                dict_to_yield[signal_type] = {}
                for sensor_name in self.sensor_names:
                    dict_to_yield[signal_type][sensor_name] = randrange(1, 8000, 1)
            yield dict_to_yield

    def stop_generation(self):
        self.keep_generating = False