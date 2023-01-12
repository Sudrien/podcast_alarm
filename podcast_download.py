#!/bin/python3

import time
import xml.etree.ElementTree
import urllib.request
import shutil
import os.path
import yaml
import re
import email.utils

feed_urls = []
feed_urls.append('https://feeds.twit.tv/sn.xml') # security now
feed_urls.append('https://feeds.npr.org/510351/podcast.xml') # shortwave

mp3_dir = '/home/dietpi/podcast_alarm/mp3/'
mp3_metadata_path = mp3_dir + 'mp3.yaml'

if os.path.exists(mp3_metadata_path):
	with open(mp3_metadata_path, 'r') as file:
		mp3_metadata = yaml.safe_load(file)
else:
	mp3_metadata = dict()


for feed_url in feed_urls:
	feed_site = urllib.request.urlopen(feed_url)
	feed_body = feed_site.read().decode('utf-8')
	feed_dom = xml.etree.ElementTree.fromstring(feed_body)
	mp3_urls = feed_dom.findall('.//item')
	for mp3_url in mp3_urls:
		mp3_basename = re.sub("\.mp3\?.*", ".mp3", os.path.basename(mp3_url.find('./enclosure').attrib['url']))
		mp3_local = mp3_dir + mp3_basename
		print(mp3_url)
		print(mp3_basename)

		if not os.path.exists(mp3_dir):
			os.makedirs(mp3_dir)

		if os.path.exists(mp3_local):
			print(mp3_local + ' already exists')
		else:
			with urllib.request.urlopen(mp3_url.find('./enclosure').attrib['url']) as response, open(mp3_local, 'wb') as out_file:
				print(response.status)
				shutil.copyfileobj(response, out_file)

			print(mp3_local + ' downloaded')
		mp3_metadata[time.mktime(email.utils.parsedate_to_datetime(mp3_url.find('./pubDate').text).timetuple())] = mp3_basename

		with open(mp3_metadata_path, 'w') as file:
			yaml.dump(mp3_metadata, file)

