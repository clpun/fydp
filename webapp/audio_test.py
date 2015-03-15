#!/usr/bin/env python
import time
import math
import pygame

from array import array
from pygame.mixer import Sound, Channel, pre_init, get_init
from random import randint

SAMPLE_RATE = 44100

class Tone(Sound):
	frequency = 0

	def __init__(self, frequency):
		self.frequency = frequency
		Tone.frequency = frequency
		Sound.__init__(self, self.build_samples())

	def build_samples(self):
		amplitude = 2**(abs(get_init()[1])-1)-1
		samples = array("h", [int(math.sin(n*Tone.frequency*(2*math.pi/SAMPLE_RATE))*amplitude) for n in xrange(0, SAMPLE_RATE)])
		return samples

if __name__ == "__main__":
	pygame.init()
	pygame.mixer.set_num_channels(30)

	# Initialize channels
	channels = []
	for i in range(0, 30):
		channels.append(Channel(i))

	left_freq = 398
	right_freq = 403
	counter = 0
	for i in xrange(0, 30, 2):
		print "Left frequency: "+str(left_freq)
		print "Right frequency: "+str(right_freq)
		channels[i].play(Tone(left_freq), -1)
		channels[i].set_volume(0, 0)
		channels[i+1].play(Tone(right_freq), -1)
		channels[i+1].set_volume(0, 0)

		counter = counter + 1
		if (counter % 2) == 1:
			left_freq = left_freq - 1
		else:
			right_freq = right_freq + 1


	# Play the 10Hz pair
	channels[10].set_volume(0.5, 0)
	channels[11].set_volume(0, 0.5)
	current_left_chan = channels[10]
	current_right_chan = channels[11]

	time.sleep(5)

	# Simulate the situation when beta is high
	# Osillate beat frequency around 5 ~ 15Hz
	# Change frequency every 1s
	beta_high = True
	beat_freq = 10
	left_chan_index = 10
	right_chan_index = 11
	should_increase = True

	while beta_high:
		print "Beat frequency: "+str(beat_freq)

		if beat_freq == 20:
			should_increase = False
		elif beat_freq == 5:
			should_increase = True

		if should_increase == True:
			beat_freq = beat_freq + 1
		else:
			beat_freq = beat_freq - 1

		# Mute current channels
		current_left_chan.set_volume(0, 0)
		current_right_chan.set_volume(0, 0)

		if beat_freq == 5:
			left_chan_index = 0
			right_chan_index = 1
		elif beat_freq == 6:
			left_chan_index = 2
			right_chan_index = 3
		elif beat_freq == 8:
			left_chan_index = 4
			right_chan_index = 5
		elif beat_freq == 9:
			left_chan_index = 6
			right_chan_index = 7
		elif beat_freq == 10:
			left_chan_index = 8
			right_chan_index = 9
		elif beat_freq == 11:
			left_chan_index = 10
			right_chan_index = 11
		elif beat_freq == 12:
			left_chan_index = 12
			right_chan_index = 13
		elif beat_freq == 13:
			left_chan_index = 14
			right_chan_index = 15
		elif beat_freq == 14:
			left_chan_index = 16
			right_chan_index = 17
		elif beat_freq == 15:
			left_chan_index = 18
			right_chan_index = 19
		elif beat_freq == 16:
			left_chan_index = 20
			right_chan_index = 21
		elif beat_freq == 17:
			left_chan_index = 22
			right_chan_index = 23
		elif beat_freq == 18:
			left_chan_index = 24
			right_chan_index = 25
		elif beat_freq == 19:
			left_chan_index = 26
			right_chan_index = 27
		elif beat_freq == 20:
			left_chan_index = 28
			right_chan_index = 29

		channels[left_chan_index].set_volume(0.5, 0)
		channels[right_chan_index].set_volume(0, 0.5)
		current_left_chan = channels[left_chan_index]
		current_right_chan = channels[right_chan_index]

		time.sleep(0.25)