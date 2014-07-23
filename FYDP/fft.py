import numpy as np
import csv
import time

def write_to_file(data_set, start_time):
	# Write results to a csv file
	F3 = data_set['F3']
	FC5 = data_set['FC5']
	AF3 = data_set['AF3']
	F7 = data_set['F7']
	T7 = data_set['T7']
	P7 = data_set['P7']
	O1 = data_set['O1']
	O2 = data_set['O2']
	P8 = data_set['P8']
	T8 = data_set['T8']
	F8 = data_set['F8']
	AF4 = data_set['AF4']
	FC6 = data_set['FC6']
	F4 = data_set['F4']

	cur_time = time.time()-start_time

	f = open('fft_mag_spectrum_formatted.csv', 'a')
        writer = csv.writer(f)
        data = [str(cur_time)]
        
        for i in range(0, len(F3)):
            data.append(str(F3[i]))
        for i in range(0, len(FC5)):
            data.append(str(FC5[i]))
        for i in range(0, len(AF3)):
            data.append(str(AF3[i]))
        for i in range(0, len(F7)):
            data.append(str(F7[i]))
        for i in range(0, len(T7)):
            data.append(str(T7[i]))
        for i in range(0, len(P7)):
            data.append(str(P7[i]))
        for i in range(0, len(O1)):
            data.append(str(O1[i]))
        for i in range(0, len(O2)):
            data.append(str(O2[i]))
        for i in range(0, len(P8)):
            data.append(str(P8[i]))
        for i in range(0, len(T8)):
            data.append(str(T8[i]))
        for i in range(0, len(F8)):
            data.append(str(F8[i]))
        for i in range(0, len(AF4)):
            data.append(str(AF4[i]))
        for i in range(0, len(FC6)):
            data.append(str(FC6[i]))
        for i in range(0, len(F4)):
            data.append(str(F4[i]))

        writer.writerow(data)

        f.close()

def compute_fft(data):
	#Check frequencies
	timestep = 1/128.0
	freq = np.fft.fftfreq(data.size, d=timestep)
	print "Frequencies: "+str(freq)

	# Comput fft amplitude spectrum
	y = np.fft.fft(data)
	length_y = len(y)

	# Return the positive frequency components
	return np.absolute(y[0:(length_y/2)+1])