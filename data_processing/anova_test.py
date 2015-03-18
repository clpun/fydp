from csv import reader
import sys
import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd


file = sys.argv[1]
first_row = 1
start_test = 1
end_test = 0
start_control = 0
end_control = 0
with open(file, 'rb') as csvfile:
	data_reader = reader(csvfile)
	for row in data_reader:
		if first_row:
			end_control = len(row)-1
			for index, col in enumerate(row[1:]):
				# print index
				if float(col)<15:
					end_test = index
					# print col
			start_control = end_test + 1
			first_row = 0
			print start_test
			print end_test 
			print start_control
			print end_control
			continue
		else:
			# print row[start_test]
			# print row[start_test:end_test+1]
			# print row[start_control:end_control+1]
			# print row[end_control]
			# print end_control
			i = 1
			tuples = []
			while i<=end_control:
				if i<start_control:
					tuples.append(( i, 'test', row[i]))
				else:
					tuples.append(( i, 'control', row[i]))
				i+=1
			x = np.rec.array(tuples, dtype=[('idx', '<i4'), ('type', '|S8'), ('power', 'float')])
			# print x
			# print x.power[0:end_test]
			# print x.power[end_test:end_control]
			f_value, p_value = stats.f_oneway(x.power[0:end_test], x.power[end_test:end_control])
			print '%s \t p-value: %.7f \t %s significantly different' % (row[0], p_value, 'is' if p_value<0.05 else 'is NOT')
			break
