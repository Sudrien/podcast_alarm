#!/bin/python3

import RPi.GPIO
import time
import xml.etree.ElementTree
import urllib.request
import shutil
import os.path
import pygame

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setwarnings(False)
RPi.GPIO.setup(23, RPi.GPIO.IN, pull_up_down = RPi.GPIO.PUD_DOWN)
RPi.GPIO.setup(25, RPi.GPIO.OUT, initial = RPi.GPIO.HIGH)

feed_url = 'https://feeds.twit.tv/sn.xml'
feed_site = urllib.request.urlopen(feed_url)
feed_body = feed_site.read().decode('utf-8')
feed_dom = xml.etree.ElementTree.fromstring(feed_body)
mp3_url = feed_dom.find('.//enclosure').attrib['url']

mp3_basename = os.path.basename(mp3_url)
mp3_local = '/home/dietpi/podcast_alarm/' + mp3_basename

print(mp3_url)
print(mp3_basename)

if os.path.exists(mp3_local):
        print(mp3_local + ' already exists')
else:
        with urllib.request.urlopen(mp3_url) as response, open(mp3_local, 'wb') as out_file:
                print(response.status)
                shutil.copyfileobj(response, out_file)

        print(mp3_local + ' downloaded')

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(mp3_local)
pygame.mixer.music.set_volume(0.03)
pygame.mixer.music.play()

try:
        while pygame.mixer.music.get_busy():
                if RPi.GPIO.input(23) == RPi.GPIO.LOW:
                        pygame.mixer.music.stop()
                        RPi.GPIO.output(25, RPi.GPIO.LOW)
                time.sleep(0.5)
except KeyboardInterrupt:
        RPi.GPIO.output(25,RPi.GPIO.LOW)
        RPi.GPIO.cleanup()
