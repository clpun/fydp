import csv
from csv import reader
import os
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def load_csv(filename):
	with open(filename,'rU') as csv_file:
		data_reader = reader(csv_file)
		master = []
		#matrix = []
		for row in data_reader:
			matrix = np.asarray(row)
			# master.append(matrix)
	matrix = [float(i) for i in matrix]
	print str(type(matrix[0]))
	mu, std = norm.fit(matrix)
	print "mu = " + str(mu)
	print "std = " + str(std)

if __name__ == "__main__":
	load_csv("testing_scipy_normfit.csv")
