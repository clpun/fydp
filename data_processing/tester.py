from collections import Counter
import unittest
import numpy
from correlation_table import CorrelationTable
from test_case_table import TestCaseTable


class TestCaseTableTester(unittest.TestCase):
    def setUp(self):
        self.correlation_table = CorrelationTable('p_values_test.csv')
        self.test_case_table = TestCaseTable('test_case_test_data.csv', (5, 7.8), self.correlation_table)

    def test_correlation_table(self):
        i = 0
        expected_freq_values = [1, 2, 3, 4, 5, 7, 10, 13, 14, 15, 15, 25, 26, 27, 28, 29, 30, 33, 40, 41, 42, 43, 44, 45, 48, 53, 58, 62, 63, 10, 11, 11, 12, 25, 53, 58]
        expected_c1_values = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 2, 2, 2]
        expected_c2_values = [3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3]
        for correlation in self.correlation_table.correlation_generator():
            expected_channel_name = 'F3'
            if i >= 29:
                expected_channel_name = 'AF3'
            self.assertEqual(correlation[0], expected_channel_name)
            self.assertEqual(correlation[1], expected_freq_values[i])
            self.assertEqual(correlation[2], expected_c1_values[i])
            self.assertEqual(correlation[3], expected_c2_values[i])

            i += 1

    def test_test_case_table(self):
        expected_channels = ['F3', 'AF3']
        channels = self.test_case_table.table.keys()
        F3_frequencies = [1, 2, 3, 4, 5, 7, 10, 13, 14, 15, 25, 26, 27, 28, 29, 30, 33, 40, 41, 42, 43, 44, 45, 48, 53, 58, 62, 63]
        AF3_frequencies = [10, 11, 12, 25, 53, 58]
        F3_c1_1_powers = [249.4385385, 231.9000769, 259.1308462, 278.977, 231.2077692, 189.2846923, 122.5923846, 146.9000769,
                 208.977, 77.51546154, 104.8231538, 137.0539231, 124.4385385, 133.2846923, 109.2846923, 132.2846923,
                 161.5154615, 97.05392308, 147.1308462, 209.6693077, 178.9000769, 189.4385385, 231.6693077, 223.977,
                 204.7462308]
        AF3_c2_11_powers = [10.22229075, 7.203163395, 7.58745171, 5.175852544, 17.95534987, 10.51706006, 1.834857653,
                            4.837017527, 4.672391692, 15.31231381, 7.496309305, 4.904158822, 19.22180625, 16.72057177]
        self.assertEqual(expected_channels, channels)
        self.assertEqual(Counter(self.test_case_table.table['F3'].keys()), Counter(F3_frequencies))
        self.assertEqual(Counter(self.test_case_table.table['AF3'].keys()), Counter(AF3_frequencies))
        self.assertEqual(self.test_case_table.table['F3'][1][1], numpy.mean(F3_c1_1_powers))
        self.assertEqual(self.test_case_table.table['AF3'][11][2], numpy.mean(AF3_c2_11_powers), 'AF3 mean value for frequency 11 is wrong')
        # TODO: possibly more testing


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestCaseTableTester('test_test_case_table'))
    unittest.TextTestRunner().run(suite)