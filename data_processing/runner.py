import sys
from correlation_table import CorrelationTable
from test_case_table import TestCaseTable

filename = sys.argv[1]

correlation_table = CorrelationTable(filename)
test_case_1 = TestCaseTable('lhchung_ctn_600_5~0s4-7~5_30s.csv', (5, 7.8), correlation_table)
print 'done'