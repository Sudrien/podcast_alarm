#!/bin/python3

import RPi.GPIO
import time
import os.path
import pygame
import datetime
import yaml
import random

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setwarnings(False)
RPi.GPIO.setup(23, RPi.GPIO.IN, pull_up_down = RPi.GPIO.PUD_DOWN)
RPi.GPIO.setup(25, RPi.GPIO.OUT, initial = RPi.GPIO.HIGH)

target_volume = 0.03

pygame.init()
pygame.mixer.init()
# pygame.mixer.music.load(mp3_local)
pygame.mixer.music.set_volume(target_volume)

stop_time = datetime.datetime.now() + datetime.timedelta(hours=1)
mp3_dir = '/home/dietpi/podcast_alarm/mp3/'
mp3_metadata_path = mp3_dir + 'mp3.yaml'

print('start at %s' % (datetime.datetime.now()))

print('stop at %s' % (stop_time))

try:

	if os.path.exists(mp3_metadata_path):
        	with open(mp3_metadata_path, 'r') as file:
                	mp3_metadata = yaml.safe_load(file)
	else:
		print('bad')
		raise FileNotFoundError('No Downloads')

	# get first random music
	random_timestamp, random_mp3 = random.choice(list(mp3_metadata.items()))
	pygame.mixer.music.load(mp3_dir + random_mp3)
	pygame.mixer.music.play()

#	while pygame.mixer.music.get_busy():
	while datetime.datetime.now() <= stop_time:
		if RPi.GPIO.input(23) == RPi.GPIO.LOW:
			break
		if target_volume < 0.08:
			target_volume += 0.0001
			pygame.mixer.music.set_volume( target_volume )
			print('volume: %1.6F %1.6F' % (target_volume, pygame.mixer.music.get_volume()))
		if not pygame.mixer.music.get_busy():
			random_timestamp, random_mp3 = random.choice(list(mp3_metadata.items()))
			pygame.mixer.music.load(mp3_dir + random_mp3)
		time.sleep(1)
except KeyboardInterrupt:
	print('Ctrl+C\'d?')
	pass
except FileNotFoundError:
	print('yaml empty?')
	pass
pygame.mixer.music.stop()
RPi.GPIO.output(25,RPi.GPIO.LOW)
RPi.GPIO.cleanup()
