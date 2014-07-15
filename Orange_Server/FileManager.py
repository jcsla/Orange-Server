#-*- coding: cp949 -*-
import urllib
import urllib2
import re

from bs4 import BeautifulSoup

from datetime import timedelta, date

import thread, time
import datetime

def set_file_info(id):
	t = time.localtime()

	while True:
		now = time.localtime()

#		if now.tm_mday != t.tm_mday:
#		if now.tm_hour != t.tm_hour
		if now.tm_min != t.tm_min:
			# write melon_chart file
			url = 'http://www.melon.com/chart/index.htm'

			handle = urllib2.urlopen(url)
			data = handle.read()
			beautifulSoup = BeautifulSoup(data)
			title = beautifulSoup.find_all('div', {'class':'ellipsis rank01'})
			singer = beautifulSoup.find_all('div', {'class':'ellipsis rank02'})
			
			f = open("MelonChart.dat", 'w')
			for i in range(1, 101):
				tmp_title = title[i].text.strip().encode('utf-8')
				tmp_singer = singer[i].find('span').text.strip().encode('utf-8')
				
				search_url = 'http://www.youtube.com/results?search_query=' + urllib.quote(tmp_title) + '+' + urllib.quote(tmp_singer)
				handle = urllib2.urlopen(search_url)
				data = handle.read()
				beautifulSoup = BeautifulSoup(data)
				bs_url = beautifulSoup.find_all('h3', {'class':'yt-lockup-title'})
				bs_time = beautifulSoup.find_all('span', {'class':'video-time'})

				tmp_url = "http://www.youtube.com" + bs_url[0].find('a')['href'].encode('utf-8')
				tmp_time = bs_time[0].text.encode('utf-8')
				data = tmp_title + '\n' + tmp_singer + '\n' + tmp_url + "\n" + tmp_time + "\n"
				f.write(data)
			
			f.close()
			t = time.localtime()
			print ("Update: %s" % datetime.date.today())



if __name__ == '__main__':
#	set_file_info(0)	
	thread.start_new_thread(set_file_info, (0,))
	while True:
		time.sleep(30) 
