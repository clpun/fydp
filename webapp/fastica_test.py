#print(__doc__)

import sys
import csv
import gevent
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from py.lib import emotiv

from sklearn.decomposition import FastICA, PCA

###############################################################################
# Test application
limit = 128 * 5
F3Buffer = []
FC5Buffer = []
AF3Buffer = []
F7Buffer = []
T7Buffer = []
P7Buffer = []
O1Buffer = []
O2Buffer = []
P8Buffer = []
T8Buffer = []
F8Buffer = []
AF4Buffer = []
FC6Buffer = []
F4Buffer = []
headset = emotiv.Emotiv()
gevent.spawn(headset.setup)
gevent.sleep(1)

try:
    sample_counter = 0

    print '~~~~~~~~~~~'
    while sample_counter < limit:
        # Retrieve emotiv packet
        packet = headset.dequeue()
        # print str(packet)
        # print str(type(packet))
        # for key in packet.sensors.keys():
        #     print str(key) + " = " + str(packet.sensors[key])
        # Get sensor data
        battery = packet.battery
        gyroX = packet.sensors['X']['value']
        gyroY = packet.sensors['Y']['value']
        F3 = packet.sensors['F3']['value']
        FC5 = packet.sensors['FC5']['value']
        AF3 = packet.sensors['AF3']['value']
        F7 = packet.sensors['F7']['value']
        T7 = packet.sensors['T7']['value']
        P7 = packet.sensors['P7']['value']
        O1 = packet.sensors['O1']['value']
        O2 = packet.sensors['O2']['value']
        P8 = packet.sensors['P8']['value']
        T8 = packet.sensors['T8']['value']
        F8 = packet.sensors['F8']['value']
        AF4 = packet.sensors['AF4']['value']
        FC6 = packet.sensors['FC6']['value']
        F4 = packet.sensors['F4']['value']

        # Build buffers for FFT
        F3Buffer = np.append(F3Buffer,F3)
        FC5Buffer = np.append(FC5Buffer,FC5)
        AF3Buffer = np.append(AF3Buffer,AF3)
        F7Buffer = np.append(F7Buffer,F7)
        T7Buffer = np.append(T7Buffer,T7)
        P7Buffer = np.append(P7Buffer,P7)
        O1Buffer = np.append(O1Buffer,O1)
        O2Buffer = np.append(O2Buffer,O2)
        P8Buffer = np.append(P8Buffer,P8)
        T8Buffer = np.append(T8Buffer,T8)
        F8Buffer = np.append(F8Buffer,F8)
        AF4Buffer = np.append(AF4Buffer,AF4)
        FC6Buffer = np.append(FC6Buffer,FC6)
        F4Buffer = np.append(F4Buffer,F4)

        gevent.sleep(0)

        sample_counter += 1
        if sample_counter%50 == 0:
        	print str(battery)
        	print "Acquiring data {0} seconds : {1}%".format(str(float(sample_counter)/128.0),str(float(sample_counter)*100/float(limit)))

except KeyboardInterrupt:
    headset.close()
finally:
    headset.close()


observation = []
# O2 = []
# O1 = []
# with open('6mins_post5sitting.csv','rU') as csvfile:
# 	reader = csv.reader(csvfile,delimiter=',',quotechar='|')
# 	i = 0
# 	for row in reader:
# 		i += 1
# 		if row[8] != 'O2(gamma)':
# 			O2 = np.append(O2,float(row[8]))
# 			if float(row[8]) == float('Inf') or float(row[8]) == float('NaN'):
# 				print 'Found {0} at {1}'.format(str(float(row[8])),str(i))
# 			#print len(observation)
# 		if row[7] != 'O1(gamma)':
# 			O1 = np.append(O1,float(row[7]))
# 			if float(row[7]) == float('Inf') or float(row[7]) == float('NaN'):
# 				print 'Found {0} at {1}'.format(str(float(row[7])),str(i))
# tempO1 = O1Buffer + (0.2 * np.random.normal(size=O1Buffer.shape))
observation = np.c_[O1Buffer.T,O2Buffer.T,T7Buffer.T,T8Buffer.T]
# print str(O1Buffer)
# print "observ"
# print str(observation.T[0])
# for i in range(1,len(line)-1):
# 	#stringlist = line[i].split(',')
# 	observation = np.c_[observation,float(stringlist[8])]
# 	line = test_file.readline()
# 	print str(i)

# while line != '':
# 	stringlist = line.split(',')
# 	observation = np.c_[observation,float(stringlist[8])]
# 	line = test_file.readline()
#test_file.close()
#print str(observation)
observation /= observation.std(axis=0)
ica = FastICA(n_components=4,max_iter=400)
source = ica.fit_transform(observation)
# Plot results

plt.figure()

models = [observation, source]
names = ['Observation O1',
         'Observation O2',
         'Observation T7',
         'Observation T8',
         'ICA recovered signal O1',
         'ICA recovered signal O2',
         'ICA recovered signal T7',
         'ICA recovered signal T8']
colors = ['red', 'steelblue','orange','green']
print 'fastICA mixing matrix = ' + str(ica.mixing_)
for ii in range(1,9):
	plt.subplot(8, 1, ii)
	plt.title(names[ii-1])
	#print "plotting subplot {0} = {1}".format(str(ii),names[ii-1])
	if (ii == 1):
		plt.plot(models[0].T[0], color='red')
	elif (ii == 2):
		plt.plot(models[0].T[1], color='steelblue')
	elif (ii == 3):
		plt.plot(models[0].T[2], color='orange')
	elif (ii == 4):
		plt.plot(models[0].T[3], color='green')
	elif (ii == 5):
		plt.plot(models[1].T[0], color='red')
	elif (ii == 6):
		plt.plot(models[1].T[1], color='steelblue')
	elif (ii == 7):
		plt.plot(models[1].T[2], color='orange')
	elif (ii == 8):
		plt.plot(models[1].T[3], color='green')
	# for sig, color in zip(model.T, colors):
	# 	plt.plot(sig, color=color)

plt.subplots_adjust(0.09, 0.04, 0.94, 0.94, 0.26, 0.46)
plt.show()


# ###############################################################################
# # Generate sample data
# np.random.seed(0)
# n_samples = 2000
# time = np.linspace(0, 8, n_samples)

# s1 = np.sin(2 * time)  # Signal 1 : sinusoidal signal
# s2 = np.sign(np.sin(3 * time))  # Signal 2 : square signal
# s3 = signal.sawtooth(2 * np.pi * time)  # Signal 3: saw tooth signal

# S = np.c_[s1, s2, s3]
# S += 0.2 * np.random.normal(size=S.shape)  # Add noise

# S /= S.std(axis=0)  # Standardize data
# # Mix data
# A = np.array([[1, 1, 1], [0.5, 2, 1.0], [1.5, 1.0, 2.0]])  # Mixing matrix
# X = np.dot(S, A.T)  # Generate observations

# # Compute ICA
# ica = FastICA(n_components=3)
# S_ = ica.fit_transform(X)  # Reconstruct signals
# A_ = ica.mixing_  # Get estimated mixing matrix

# # We can `prove` that the ICA model applies by reverting the unmixing.
# assert np.allclose(X, np.dot(S_, A_.T) + ica.mean_)

# # For comparison, compute PCA
# pca = PCA(n_components=3)
# H = pca.fit_transform(X)  # Reconstruct signals based on orthogonal components

# ###############################################################################
# # Plot results

# plt.figure()

# models = [X, S, S_, H]
# names = ['Observations (mixed signal)',
#          'True Sources',
#          'ICA recovered signals', 
#          'PCA recovered signals']
# colors = ['red', 'steelblue', 'orange']

# for ii, (model, name) in enumerate(zip(models, names), 1):
#     plt.subplot(4, 1, ii)
#     plt.title(name)
#     for sig, color in zip(model.T, colors):
#         plt.plot(sig, color=color)

# plt.subplots_adjust(0.09, 0.04, 0.94, 0.94, 0.26, 0.46)
# plt.show()

