from csv import reader
import numpy as np
import sys

file = sys.argv[1]

with open(file, 'rb') as csvfile:
	data_reader = reader(csvfile)
	for channel_frequency_power in data_reader[1:]:
		channel_name = channel_frequency_power[0]
		
		power_array = np.zeros(shape=(146, 1))
		for i, power in enumerate(channel_frequency_power[1:]):
			power_array[i] = power
		print power_array
		break

