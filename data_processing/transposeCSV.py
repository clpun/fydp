import csv
import sys
from itertools import izip
input_file = sys.argv[1]
a = izip(*csv.reader(open(input_file, "rU")))
output_file = 'transpose_' + input_file
csv.writer(open(output_file, "wb")).writerows(a)