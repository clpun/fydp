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
	left_freq = 395
	right_freq = 405

	pygame.init()

	# Load audio tracks
	sound1 = Tone(left_freq)
	sound2 = Tone(right_freq)

	# Find the left and right channels
	chan1 = Channel(0)
	chan2 = Channel(1)

	# Play audio tracks
	chan1.play(sound1, -1)
	chan1.set_volume(0.5, 0)
	chan2.play(sound2, -1)
	chan2.set_volume(0, 0.5)

	time.sleep(10)

	# Simulate the situation when beta is high
	# Osillate beat frequency around 5 ~ 15Hz
	# Change frequency every 1s
	beta_high = True
	beat_freq = 10
	mid_freq = 400
	while beta_high:
		left_freq = randint(mid_freq-7, mid_freq-2)
		right_freq = randint(mid_freq+3, mid_freq+8)
		beat_freq = right_freq - left_freq
		print beat_freq

		chan1 = Channel(0)
		chan2 = Channel(1)
		sound1 = Tone(left_freq)
		sound2 = Tone(right_freq)
		chan1.play(sound1, -1)
		chan1.set_volume(0.5, 0)
		time.sleep(1)
		chan2.play(sound2, -1)
		chan2.set_volume(0, 0.5)
		time.sleep(1)
