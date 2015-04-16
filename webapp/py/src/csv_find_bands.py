import csv
import os
import numpy as np
import multimodal_clustering as mmc
from scipy.stats import norm
from csv import reader
test_data_root = "/home/aaron/Documents/MindCraft/fydp/data_processing/test_data/"
output_root = "/home/aaron/Documents/MindCraft/fydp/data_processing/data_analysis/"
# output_file = "lhchung_bands.csv"
sensor_names = ['F3', 'FC5', 'AF3', 'F7', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'F8', 'AF4', 'FC6', 'F4']
num_channel = len(sensor_names)
num_freq = 64

def load_test_file_control(filename,channel):
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

def load_test_file_encode(filename,channel):
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
            if float(tmp_array[0]) > 5 and float(tmp_array[0]) <= 7.5:
            	data_array.append(np.array(list(float(tmp_array[ii]) for ii in cols)))
            else:
            	continue
    # print str((type(data_array[0])))
    return np.array(data_array)

def output_csv_file(data,header,output_file):
	output = open(output_root+output_file,'w')
	if header != "":
		output.writelines(header + "\n")
	for ii in data:
		tmp = ""
		for jj in ii:
			tmp += str(jj) + ","
		tmp += "\n"
		output.writelines(tmp)
	output.close()

def find_clusters_for_control(prefix,suffix,test_number,test_range,target_channel):
	result = []
	indices = []
	for ii in range(0,test_range):
		file_name = prefix + str(test_number+ii) + suffix
		print "Computing clusters on " + file_name + " for controls..."
		test_case = (load_test_file_control(file_name,target_channel))
		for jj in range(0,len(test_case)):
			clusters = mmc.find_clusters(test_case[jj])
			result.append(clusters)
			for kk in range(0,len(clusters)):
				if clusters[kk] > 0:
					indices.append(kk)
	output_file = "lhchung_clusters_control.csv"
	output_csv_file(result,"",output_file)
	print "Finish printing csv at " + output_root + output_file
	
	hist = mmc.plot_histogram(indices)
	maximas = mmc.find_multimodes(hist)
	output_file = "lhchung_clusters_control_summary.csv"
	output_csv_file(result,"",output_file)
	print "Finish printing csv at " + output_root + output_file
	print "maximas for control = " + str(maximas)
	
	return (result)

def find_clusters_for_encode(prefix,suffix,test_number,test_range,target_channel):
	result = []
	indices = []
	for ii in range(0,test_range):
		file_name = prefix + str(test_number+ii) + suffix
		print "Computing clusters on " + file_name + " for encode..."
		test_case = (load_test_file_encode(file_name,target_channel))
		for jj in range(0,len(test_case)):
			clusters = mmc.find_clusters(test_case[jj])
			result.append(clusters)
			for kk in range(0,len(clusters)):
				if clusters[kk] > 0:
					indices.append(kk)
	output_file = "lhchung_clusters_encode.csv"
	output_csv_file(result,"",output_file)
	print "Finish printing csv at " + output_root + output_file

	hist = mmc.plot_histogram(indices)
	maximas = mmc.find_multimodes(hist)
	output_file = "lhchung_clusters_encode_summary.csv"
	output_csv_file(result,"",output_file)
	print "Finish printing csv at " + output_root + output_file
	print "maximas for encode = " + str(maximas)

	return (result)

'''find_bands_for_control returns the bands for each test case and each sample (time slice) of a specific channel'''
def find_bands_for_control(prefix,suffix,test_number,test_range,target_channel):
	# test = load_test_file_control(prefix+str(601)+suffix,target_channel)
	# print str(test[10])
	# print str(mmc.find_bands(test[10]))
	result = []
	for ii in range(0,test_range):
		file_name = prefix + str(test_number+ii) + suffix
		# test_case = []
		test_case = (load_test_file_control(file_name,target_channel))
		for jj in range(0,len(test_case)):
			# bands = []
			bands = mmc.find_bands(test_case[jj])
			result.append(bands)
			# print "bands = " + str(bands)
	# print "result = " + str(len(result))
	# output_csv_file(result,"","lhchung_bands.csv")
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
	output_file = "lhchung_bands.csv"
	output_csv_file(bands_print,"",output_file)
	print "Finish printing csv at " + output_root + output_file
	return bands_print

if __name__ == "__main__":
	test_data_file_prefix = "lhchung_ctn_"
	test_data_file_suffix = "_5~0s4-7~5_30s.csv"
	test_data_number = 600

	# array = find_bands_for_control(test_data_file_prefix,test_data_file_suffix,test_data_number,27,"T7")
	# hist = mmc.plot_histogram(array)
	# bands = mmc.find_multimodes(hist)
	# print "bands = " + str(bands)
	# print "len(bands) = " + str(len(bands))

	# find_bands_for_all_channels(test_data_file_prefix,test_data_file_suffix,test_data_number,27)

	find_clusters_for_control(test_data_file_prefix,test_data_file_suffix,test_data_number,27,"T7")
	find_clusters_for_encode(test_data_file_prefix,test_data_file_suffix,test_data_number,27,"T7")