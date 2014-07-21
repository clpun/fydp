import sys
sys.path.append("..")
import emotiv
import gevent
import numpy as np
import csv
import time

import fft
import signal_preprocessing as sp


def create_e_matrix(channel_map, width):
	e_matrix = np.zeros(shape=(14,width))

	for idx, key in enumerate(channel_map):
		e_matrix[idx] = channel_map[key]

	return np.matrix(e_matrix)

def generate_sigma_matrix(e_matrix_array, width):
	""" channelMaps should contain all the training sets for a specific cognitive function
	return : sigma matrix for the specific cognitive function
	"""
	matrix_sum = np.zeros(shape=(14,width))

	for e_matrix in e_matrix_array:
		current_matrix = np.divide(np.dot(e_matrix, e_matrix.T), np.matrix.trace(np.dot(e_matrix, e_matrix)))
		matrix_sum = np.matrix.sum(current_matrix, matrix_sum)

	return np.divide(matrix_sum, len(e_matrix_array))

def find_omega_matrix(sigmaMatrices) :
	""" sigmaMatrices should contain all the sigma matrices for the specific cognitive functions to be compared
	return : omega matrix
	"""
	pass