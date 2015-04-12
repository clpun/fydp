import os
import numpy as np
from scipy.stats import norm

def find_mode():
	data = [111.041538462,103.604203526,83.0736417498,54.29163879,23.8438369909,3.9172397809,19.1807802615,24.7116791561,20.5592905101,10.3042221115,1.9701817383,10.8260347067,14.8111779672,13.2002572053,7.4503064192,0.6155759194,6.2273559076,9.6146914048,9.6110242047,6.9456740361,3.1351595437,0.8485088117,2.6945089569,3.4587771511,3.650769542,3.8532153988,3.6587522547,2.5136423254,0.7054726315,2.1627483686,4.0336013115,4.8393183786,4.453042574,3.3293873578,2.2635344665,1.650151503,1.0638298162,1.4511213728,3.0960067146,4.5260477938,4.9790552947,4.2015441666,2.6075691888,1.8800609846,2.9543288696,3.5750012901,3.0260779061,1.5838810655,0.9726097679,2.1389735234,2.5522947195,1.9049423418,0.8144771737,1.5291793769,2.4508453672,2.4258480551,1.4264832209,0.5618846404,1.8597685094,2.6185146845,2.3324405507,1.1297238222,0.6831685462,2.007636653]
	# data = [1,2,3,4,5,4,3,2,1,3,4,7,8,5,3,2]
	max_freq = len(data)
	boundaries = []
	print str((data))
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
	print str(boundaries)
	numBoundaries = 0
	for ii in range(0,len(boundaries)):
		if boundaries[ii] == -1:
			numBoundaries += 1
	print str(numBoundaries)
	index = 1
	prevBound = 0
	for ii in range(0,len(boundaries)):
		if ii != 0 or ii != len(boundaries)-1:
			if boundaries[ii] == -1:
				print (str(index) + " band : " + str(prevBound+1) + " ~ " + str(ii) + " Hz ("+str(ii-prevBound-1)+")")
				prevBound = ii
				index += 1
				if index == numBoundaries+1:
					print (str(index) + " band : " + str(prevBound+1) + " ~ "+str(max_freq)+" Hz ("+str(max_freq-prevBound-1)+")")
					break

if __name__ == "__main__":
	find_mode()