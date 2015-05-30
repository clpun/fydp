import sys
import os
import csv
from csv import reader
output_root = "/home/aaron/Documents/MindCraft/fydp/data_processing/data_analysis/"
sensor_names = ['F3', 'FC5', 'AF3', 'F7', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'F8', 'AF4', 'FC6', 'F4']

def process_csv(files):
	data = {}
	for f in files:
		# print "Processing file : " + str(f)
		F3 = []
		FC5 = []
		AF3 = []
		F7 = []
		T7 = []
		P7 = []
		O1 = []
		O2 = []
		P8 = []
		T8 = []
		F8 = []
		AF4 = []
		FC6 = []
		F4 = []
		with open(f, 'rU') as csv_file:
			data_reader = reader(csv_file)
			first_row = True
			for row in csv_file.readlines():
				if first_row:
					first_row = False
					continue
				tmp_array = row.split(',')
				F3.append(tmp_array[0])
				FC5.append(tmp_array[1])
				AF3.append(tmp_array[2])
				F7.append(tmp_array[3])
				T7.append(tmp_array[4])
				P7.append(tmp_array[5])
				O1.append(tmp_array[6])
				O2.append(tmp_array[7])
				P8.append(tmp_array[8])
				T8.append(tmp_array[9])
				F8.append(tmp_array[10])
				AF4.append(tmp_array[11])
				FC6.append(tmp_array[12])
				F4.append(tmp_array[13])
		data[f] = {"F3" : F3,"FC5" : FC5,"AF3" : AF3,"F7" : F7,"T7" : T7,"P7" : P7,"O1" : O1,"O2" : O2,"P8" : P8,"T8" : T8,"F8" : F8,"AF4" : AF4,"FC6" : FC6,"F4" : F4}
		# print "output : " + str(data[f])
	return data

if __name__ == "__main__":
	# print "current working dir : " + str(os.getcwd())
	files = sys.argv
	files.pop(0)
	process_csv(files)