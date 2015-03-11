#!/usr/bin/env python
import pyglet
song = pyglet.media.load('test.mp3', streaming=False)
song.play()
pyglet.app.run()

# Install pyglet and AVBin before running
