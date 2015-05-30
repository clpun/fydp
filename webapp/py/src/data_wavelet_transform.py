import sys
import numpy as np
import pywt
import import_experiment as imexp
import matplotlib.pyplot as plt
from scipy import signal

files = sys.argv
files.pop(0)
if len(files) >= 1:
	data = imexp.process_csv(files)
	print str(pywt.families())
	wavelet = pywt.Wavelet('db3')
	(phi, psi, x) = wavelet.wavefun(level=5)
	# data format : data[file_name][channel]
	# plot signals
	plt.figure()
	plt.subplot(4, 1, 1)
	plt.title('O1')
	plt.plot(data[files[0]]["O1"], color='black')
	plt.subplot(4, 1, 2)
	plt.title('O2')
	plt.plot(data[files[0]]["O2"], color='black')
	plt.subplot(4, 1, 3)
	plt.title('P7')
	plt.plot(data[files[0]]["P7"], color='black')
	plt.subplot(4, 1, 4)
	plt.title('P8')
	plt.plot(data[files[0]]["P8"], color='black')
	plt.subplot(5, 1, 5)
	plt.title('Wavelet')
	# plt.plot(x,color='black')
	# plt.plot(phi,color='green')
	plt.plot(psi,color='red')

	plt.subplots_adjust(0.09, 0.04, 0.94, 0.94, 0.26, 0.46)
	plt.show()