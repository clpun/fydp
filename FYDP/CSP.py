import sys
sys.path.append("..")
import emotiv
import gevent
import numpy as np
import csv
import time

import fft
import signal_preprocessing as sp


def create_e_matrix(channelMap):
	pass


def generate_sigma_matrix(channelMaps) :
	""" channelMaps should contain all the training sets for a specific cognitive function
	return : sigma matrix for the specific cognitive function
	"""
	pass

def find_omega_matrix(sigmaMatrices) :
	""" sigmaMatrices should contain all the sigma matrices for the specific cognitive functions to be compared
	return : omega matrix
	"""
	pass

