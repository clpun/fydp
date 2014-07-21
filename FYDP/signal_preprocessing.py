from scipy import signal
import numpy as np

def moving_avg_filter(data):
	window_size = 5
	moving_avg = np.ones(int(window_size))/float(window_size)
	y3 = np.convolve(data, moving_avg, 'same')
	return y3

def average_subtraction(data, mean):
	# Subtract mean from data
	y2 = np.subtract(data, mean)
	return y2

def low_pass_filter(data):
	# Design a low pass butterworth filter
	fs = 128.0
	fmax = 0.5*fs
	cutoff = 64.0/fmax
	b, a = signal.butter(4, cutoff, btype='low')

	# Use the butterworth filter to filter the data
	y1 = signal.lfilter(b, a, data)

	# Return the filtered data
	return y1

def preprocess(data, mean):
	# Convert data to numpy array
	numpy_array = np.array(data)

	y1 = low_pass_filter(numpy_array)
	y2 = average_subtraction(y1, mean)
	y3 = moving_avg_filter(y2)
	return y3