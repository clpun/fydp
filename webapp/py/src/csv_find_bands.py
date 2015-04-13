import csv
import os
import numpy as np
import multimodal_clustering as mmc
from scipy.stats import norm
from csv import reader
test_data_root = "/home/aaron/Documents/MindCraft/fydp/data_processing/test_data/"
output_root = "/home/aaron/Documents/MindCraft/fydp/data_processing/data_analysis/"
output_file = "band_range.csv"
sensor_names = ['F3', 'FC5', 'AF3', 'F7', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'F8', 'AF4', 'FC6', 'F4']
num_channel = len(sensor_names)
num_freq = 64

def load_test_file(filename,channel):
    index = 0
    data_array = []
    cols = []
    for ii in range(0,len(sensor_names)):
    	if(channel == sensor_names[ii]):
    		index = ii
    # print "index for channel " + channel + " = " + str(index)
    for ii in range(0,num_freq):
    	cols.append(index*num_freq+ii+1)
    # print "cols = " + str(cols)
    with open(test_data_root+filename, 'rU') as csv_file:
        data_reader = reader(csv_file)
        first_row = True
        for row in csv_file.readlines():
            if first_row:
                first_row = False
                continue
            tmp_array = row.split(',')
            if float(tmp_array[0]) <= 5:
            	data_array.append(np.array(list(float(tmp_array[ii]) for ii in cols)))
            else:
            	continue
    # print str((type(data_array[0])))
    return np.array(data_array)

def output_csv_file(data):
	output = open(output_root+output_file,'w')
	for ii in data:
		tmp = ""
		for jj in ii:
			tmp += str(jj) + ","
		tmp += "\n"
		output.writelines(tmp)
	output.close()

'''find_bands_for_control returns the bands of a number of test cases of a specific channel'''
def find_bands_for_control(prefix,suffix,test_number,test_range,target_channel):
	# test = load_test_file(prefix+str(601)+suffix,target_channel)
	# print str(test[10])
	# print str(mmc.find_bands(test[10]))
	result = []
	for ii in range(0,test_range):
		file_name = prefix + str(test_number+ii) + suffix
		# test_case = []
		test_case = (load_test_file(file_name,target_channel))
		for jj in range(0,len(test_case)):
			# bands = []
			bands = mmc.find_bands(test_case[jj])
			result.append(bands)
			# print "bands = " + str(bands)
	# print "result = " + str(len(result))
	# output_csv_file(result)
	return (result)

def find_bands_for_all_channels(prefix,suffix,test_number,test_range):
	bands_print = []
	for ii in range(0,len(sensor_names)):
		print "Finding bands for channel " + sensor_names[ii] + "..."
		array = find_bands_for_control(prefix,suffix,test_number,test_range,sensor_names[ii])
		hist = mmc.plot_histogram(array)
		bands = mmc.find_multimodes(hist)
		tmp_array = []
		tmp_array.append(sensor_names[ii])
		for jj in range(0,len(bands)):
			tmp_array.append(bands[jj])
		bands_print.append(tmp_array)
	output_csv_file(bands_print)
	print "Finish printing csv at " + output_root+output_file

if __name__ == "__main__":
	test_data_file_prefix = "lhchung_ctn_"
	test_data_file_suffix = "_5~0s4-7~5_30s.csv"
	test_data_number = 600

	# array = find_bands_for_control(test_data_file_prefix,test_data_file_suffix,test_data_number,27,"T7")
	# hist = mmc.plot_histogram(array)
	# bands = mmc.find_multimodes(hist)
	# print "bands = " + str(bands)
	# print "len(bands) = " + str(len(bands))

	find_bands_for_all_channels(test_data_file_prefix,test_data_file_suffix,test_data_number,27)