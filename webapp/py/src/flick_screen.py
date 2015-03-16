import time
import numpy as np
from PIL import Image
import sys
import threading
import matplotlib
matplotlib.use('TkAgg') # do this before importing pylab

import matplotlib.pyplot as plt
import matplotlib.patches as patches
fig = plt.figure(figsize=(14, 14),frameon=False)
fig.patch.set_facecolor('black')
ax = fig.add_axes([0, 0, 1, 1])
#ax.axis('off')
IsBlack = True
GammaIsHigh = True
prev_time = time.time()
#image = np.random.randn(10,10)
#im=plt.imshow(image)

def use_timer (interval, worker_func, iterations = 0):
	if iterations != 1:
		threading.Timer (
		interval,
		use_timer, [interval, worker_func, 0 if iterations == 0 else iterations-1]
		).start ();

	worker_func ();

def show_image():
	global IsBlack
	global GammaIsHigh
	global prev_time
	global ax
	print time.time() - prev_time
	prev_time = time.time()
	if IsBlack:
		ax.set_axis_bgcolor((0, 0, 0))
	elif GammaIsHigh:
		ax.set_axis_bgcolor((0, 1, 0))
	else:
		ax.set_axis_bgcolor((1, 1, 1))
	fig.canvas.draw()
	IsBlack = not IsBlack
	#print "Hello, World!"

def change_GammaIsHigh():
	global GammaIsHigh
	GammaIsHigh = not GammaIsHigh

interval = 0.09090909
use_timer (interval, show_image, 200);
use_timer (5, change_GammaIsHigh, 5)

mng = plt.get_current_fig_manager()                                   # you get normal size
mng.window.wm_geometry("2000x1500+20+40")
plt.show()
