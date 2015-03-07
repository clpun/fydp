import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# # Generate sample data
np.random.seed(0)
n_samples = 804
(time, step) = np.linspace(0, 2*np.pi, n_samples, retstep=True)
print step

s1 = np.sin(time)  # Signal 1 : sinusoidal signal
# s2 = np.sign(np.sin(3 * time))  # Signal 2 : square signal
# s3 = signal.sawtooth(2 * np.pi * time)  # Signal 3: saw tooth signal

normalization_factor = 2/np.sqrt(26.0)
f1 = np.absolute((np.fft.fft(s1[778:],128)*normalization_factor)[0:((128/2)+1)])
print f1

plt.figure()
colors = ['red', 'steelblue']
# models = [X, S, S_, H]
# names = ['Observations (mixed signal)',
#          'True Sources',
#          'ICA recovered signals', 
#          'PCA recovered signals']
plt.subplot(2, 1, 1)
plt.title('True Sources')
plt.plot(s1, color='red')
plt.subplot(2, 1, 2)
plt.title('DFT')
plt.plot(np.linspace(0,64,65),f1, color='steelblue')
# for ii, (model, name) in enumerate(zip(models, names), 1):
#     plt.subplot(4, 1, ii)
#     plt.title(name)
#     for sig, color in zip(model.T, colors):
#         plt.plot(sig, color=color)

plt.subplots_adjust(0.09, 0.04, 0.94, 0.94, 0.26, 0.46)
plt.show()
