import os
import random
import numpy as np
from scipy.stats import norm

class Particle:
	"""Particle for hillclimbing_search"""
	def __init__(self, pos):
		# super(Particle, self).__init__()
		self.pos = pos
	def search_neighbour(self, space):
		new_pos = self.pos
		overall_prob = 1.0
		bound = []
		decision_pos = []
		if self.pos == 0:
			if self.pos == len(space)-1:
				return self.pos
			overall_prob = float(space[new_pos] + space[new_pos+1])
			bound.append(space[new_pos]/overall_prob)
			bound.append(1.0)
			decision_pos.append(new_pos)
			decision_pos.append(new_pos+1)
		elif self.pos == len(space)-1:
			overall_prob = float(space[new_pos-1] + space[new_pos])
			bound.append(space[new_pos-1]/overall_prob)
			bound.append(1.0)
			decision_pos.append(new_pos-1)
			decision_pos.append(new_pos)
		else:
			overall_prob = float(space[new_pos-1] + space[new_pos] + space[new_pos+1])
			firstbound = space[new_pos-1]/overall_prob
			bound.append(firstbound)
			bound.append(firstbound+(space[new_pos]/overall_prob))
			bound.append(1.0)
			decision_pos.append(new_pos-1)
			decision_pos.append(new_pos)
			decision_pos.append(new_pos+1)
		decision = random.random()
		for ii in range(0,len(bound)):
			if decision < bound[ii]:
				self.pos = decision_pos[ii]
				break
		return self.pos
	def get_pos(self):
		return self.pos

def find_bands(data):
	bands = []
	max_freq = len(data)
	boundaries = []
	# print str((data))
	# for ii in range(0,len(data)):
	# 	if ii == 0:
	# 		if data[ii+1] - data[ii] > 0:
	# 			boundaries.append(-1)
	# 		else:
	# 			boundaries.append(1)
	# 	elif ii == len(data)-1:
	# 		if data[ii] - data[ii-1] > 0:
	# 			boundaries.append(1)
	# 		else:
	# 			boundaries.append(-1)
	# 	else:
	# 		backdiff = data[ii] - data[ii-1]
	# 		forwarddiff = data[ii+1] - data[ii]
	# 		if backdiff < 0 and forwarddiff > 0:
	# 			boundaries.append(-1)
	# 		elif backdiff > 0 and forwarddiff < 0:
	# 			boundaries.append(1)
	# 		else:
	# 			boundaries.append(0)
	# print str(boundaries)
	# numBoundaries = 0
	# for ii in range(1,len(boundaries)-1):
	# 	if boundaries[ii] == -1:
	# 		numBoundaries += 1
	# print str(numBoundaries)
	# index = 1
	boundaries = minimax_locator(data)
	prevBound = 0
	bands.append(0)
	for ii in range(1,len(boundaries)-1):
		if boundaries[ii] == -1:
			# print (str(index) + " band : " + str(prevBound+1) + " ~ " + str(ii) + " Hz ("+str(ii-prevBound-1)+")")
			# bands.append([prevBound,ii])
			bands.append(ii)
			prevBound = ii
			# index += 1
			# if index == numBoundaries+1:
			# 	bands.append([prevBound,max_freq-1])
			# 	bands.append(max_freq-1)
			# 	print (str(index) + " band : " + str(prevBound+1) + " ~ "+str(max_freq)+" Hz ("+str(max_freq-prevBound-1)+")")
			# 	break
	bands.append(max_freq-1)
	# print str(bands)
	return np.array(bands)

def minimax_locator(data):
	boundaries = []
	for ii in range(0,len(data)):
		if ii == 0:
			if data[ii+1] - data[ii] > 0:
				boundaries.append(-1)
			else:
				boundaries.append(1)
		elif ii == len(data)-1:
			if data[ii] - data[ii-1] > 0:
				boundaries.append(1)
			else:
				boundaries.append(-1)
		else:
			backdiff = data[ii] - data[ii-1]
			forwarddiff = data[ii+1] - data[ii]
			if backdiff < 0 and forwarddiff > 0:
				boundaries.append(-1)
			elif backdiff > 0 and forwarddiff < 0:
				boundaries.append(1)
			else:
				boundaries.append(0)
	return boundaries

def find_multimodes(data):
	minimax = minimax_locator(data)
	modes = []
	for ii in range(0,len(minimax)):
		if minimax[ii] == 1:
			modes.append(ii)
	modes = hillclimbing_search(data,modes,400,1000)
	return modes

def hillclimbing_search(data,initial_soln,num_particles,iteration):
	soln = initial_soln
	gbest_soln = []
	for ii in range(0,len(initial_soln)):
		gbest_soln.append(initial_soln[ii])
	gbest = len(gbest_soln)
	searchspace = data
	if not isinstance(data,np.ndarray):
		searchspace = np.array(data)

	# Initialize particles
	all_particles = []
	for ii in range(0,len(soln)):
		for jj in range(0,num_particles):
			particle = Particle(soln[ii])
			all_particles.append(particle)
	# Search the clusters
	for ii in range(0,iteration):
		for jj in range(0,len(all_particles)):
			all_particles[jj].search_neighbour(searchspace)
		# check bands and update global best
		soln = []
		for jj in range(0,len(all_particles)):
			soln.append(all_particles[jj].get_pos())
		hist,edges = np.histogram(np.array(soln),bins=range(0,65),density=False)
		minimax = minimax_locator(hist)
		soln = []
		for jj in range(0,len(minimax)):
			if minimax[jj] == 1:
				soln.append(jj)
		if len(soln) < gbest:
			gbest_soln = []
			for jj in range(0,len(soln)):
				gbest_soln.append(soln[jj])
			gbest = len(gbest_soln)
	# Final values
	# soln = []
	# for ii in range(0,len(all_particles)):
	# 	soln.append(all_particles[ii].get_pos())
	print "best particles position after hillclimbing = " + str(gbest_soln)
	# Get histogram
	# hist,edges = np.histogram(np.array(soln),bins=range(0,65),density=False)
	print "number of bands after hillclimbing = " + str(gbest)
	# minimax = minimax_locator(hist)
	# soln = []
	# for ii in range(0,len(minimax)):
	# 	if minimax[ii] == 1:
	# 		soln.append(ii)
	return gbest_soln

def plot_histogram(data):
	if not isinstance(data,np.ndarray):
		data = np.array(data)
	val = 0
	valarray = []
	for ii in data.flat:
		for jj in ii.flat:
			valarray.append((jj))
			# print str(type(jj))
			val += 1
	# print "all particles before hillclimbing = " + str((val))
	hist,edges = np.histogram(np.array(valarray),bins=range(0,65),density=False)
	print "histogram before hillclimbing = " + str((hist))
	return hist

if __name__ == "__main__":
	# data = [1,2,3,4,5,4,3,2,1,3,4,7,8,5,3,2]
	# bands = [0, 5, 10, 14, 19, 24, 28, 33, 38, 43, 45, 47, 50, 52, 54, 57, 59, 63] = 18 bands
	# ideal = [0, 5, 10, 14, 19, 24, 28, 33, 38, 43, 47, 52, 57, 63] = 14 bands
	data = [111.041538462,103.604203526,83.0736417498,54.29163879,23.8438369909,3.9172397809,19.1807802615,24.7116791561,20.5592905101,10.3042221115,1.9701817383,10.8260347067,14.8111779672,13.2002572053,7.4503064192,0.6155759194,6.2273559076,9.6146914048,9.6110242047,6.9456740361,3.1351595437,0.8485088117,2.6945089569,3.4587771511,3.650769542,3.8532153988,3.6587522547,2.5136423254,0.7054726315,2.1627483686,4.0336013115,4.8393183786,4.453042574,3.3293873578,2.2635344665,1.650151503,1.0638298162,1.4511213728,3.0960067146,4.5260477938,4.9790552947,4.2015441666,2.6075691888,1.8800609846,2.9543288696,3.5750012901,3.0260779061,1.5838810655,0.9726097679,2.1389735234,2.5522947195,1.9049423418,0.8144771737,1.5291793769,2.4508453672,2.4258480551,1.4264832209,0.5618846404,1.8597685094,2.6185146845,2.3324405507,1.1297238222,0.6831685462,2.007636653]
	find_bands(data)