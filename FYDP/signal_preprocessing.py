from scipy import signal
import numpy as np

def moving_avg_filter(data):
	window_size = 5
	moving_avg = np.ones(int(window_size))/float(window_size)
	y = np.convolve(data, moving_avg, 'same')
	return y

def average_subtraction(data, mean):
	# Subtract mean from data
	y = np.subtract(data, mean)
	return y

def low_pass_filter(data):
	# Design a low pass butterworth filter
	fmax = 64.0
	low_cutoff = 0.5/fmax # To better remove dc components
	high_cutoff = 45.0/fmax
	b, a = signal.butter(4, [low_cutoff, high_cutoff], btype='band')

	# Use the butterworth filter to filter the data
	y = signal.lfilter(b, a, data)

	# Return the filtered data
	return y

def preprocess(data, mean):
	# Convert data to numpy array
	numpy_array = np.array(data)

	y1 = average_subtraction(numpy_array, mean)
	y2 = low_pass_filter(y1)
	y3 = moving_avg_filter(y2)
	return y3