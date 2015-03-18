from csv import reader
import sys

file = sys.argv[1]

with open(file, 'rb') as csvfile:
	data_reader = reader(csvfile)
	for row in data_reader:
		print row[1], row[2]
		break