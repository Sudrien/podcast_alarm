#!/bin/ruby

require 'nokogiri'
require 'open-uri'

doc = Nokogiri::HTML(URI.open('https://feeds.twit.tv/sn.xml'))

mp3 = doc.at_xpath('//enclosure').attr('url')
uri = URI.parse(mp3)
w = 'youtube-dl -w  \'%s\' -o /home/dietpi/podcast_alarm/%s' % [mp3, File.basename(uri.path)]
p = 'ffplay -nodisp -volume 7 \'/home/dietpi/podcast_alarm/%s\'' % [File.basename(uri.path)]

begin
system 'gpioset pinctrl-bcm2835 25=1'
puts
puts w
puts
system w

puts
puts p
puts
system p

system 'gpioset pinctrl-bcm2835 25=0'

rescue Interrupt => e
system 'gpioset pinctrl-bcm2835 25=0'
end
