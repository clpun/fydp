#!/usr/bin/env python
import pygame
import time

pygame.init()

# Load audio tracks
track_length = 60 # 60s
sound1 = pygame.mixer.Sound('left_channel.wav')
sound2 = pygame.mixer.Sound('right_channel.wav')

# Find the left and right channels
chan1 = pygame.mixer.Channel(0)
chan2 = pygame.mixer.Channel(1)

# Play audio tracks
chan1.play(sound1)
chan1.set_volume(1, 0)
chan2.play(sound2)
chan2.set_volume(0, 1)

time.sleep(track_length)