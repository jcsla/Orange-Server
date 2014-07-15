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
	newDay = True
	newHour = True	

	while True:
		now = time.localtime()

		if(now.tm_year > t.tm_year):
			newDay = True
			newHour = True
			t = time.localtime()

		elif(now.tm_mon > t.tm_mon):
			newDay = True
			newHour = True
			t = time.localtime()

		elif(now.tm_mday > t.tm_mday):
			newDay = True
			newHour = True
			t = time.localtime()
		
		elif(now.tm_hour > t.tm_hour):
			newHour = True
			t = time.localtime()

		if newHour:			
			# update melon_chart file
			print("melon chart updating...")
			url = 'http://www.melon.com/chart/index.htm'

			handle = urllib2.urlopen(url)
			data = handle.read()
			beautifulSoup = BeautifulSoup(data)
			title = beautifulSoup.find_all('div', {'class':'ellipsis rank01'})
			singer = beautifulSoup.find_all('div', {'class':'ellipsis rank02'})
			
			info_data = ""
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
				data = tmp_title + "\n" + tmp_singer + "\n" + tmp_url + "\n" + tmp_time + "\n"
				
				info_data = info_data + data
				if (i % 10) == 0:
					print ('   %3d%% ing...' % i)
			
			f = open("MelonChart.dat", 'w')
			f.write(info_data)
			f.close()
			print ("Update Complete Melon Chart!")

		if newDay:
			# write billboard_chart file
			print ("billboard chart updating...")
			url = 'http://www.billboard.com/charts/hot-100?page=%d'

			info_data = ""
			for i in range(0, 10):
        			handle = urllib2.urlopen(url % i)
        			data = handle.read()
        			bs = BeautifulSoup(data)
        			title = bs.find_all('h1')
        			singer = bs.find_all('p', {'class':'chart_info'})

        			for j in range(0, 10):
            				tmp_title = title[j+1].text.strip()
            				tmp_singer = singer[j].find('a').text.strip()
            									
					search_url = 'http://www.youtube.com/results?search_query=' + urllib.quote(tmp_title) + '+' + urllib.quote(tmp_singer)
                                	handle = urllib2.urlopen(search_url)
                                	data = handle.read()
                                	beautifulSoup = BeautifulSoup(data)
                                	bs_url = beautifulSoup.find_all('h3', {'class':'yt-lockup-title'})
                                	bs_time = beautifulSoup.find_all('span', {'class':'video-time'})

                                	tmp_url = "http://www.youtube.com" + bs_url[0].find('a')['href'].encode('utf-8')
                                	tmp_time = bs_time[0].text.encode('utf-8')
                                
					data = tmp_title + "\n" + tmp_singer + "\n" + tmp_url + "\n" + tmp_time + "\n"
                                
                                	info_data = info_data + data
				
				print ('   %3d%% ing...' % ((i+1)*10) )
			
			f = open("BillboardChart.dat", 'w')
			f.write(info_data)
			f.close()
			
			print("Update Complete Billboard Chart")
			
			# update oricon_chart file
			print("oricon chart updaing...")
			url = 'http://www.oricon.co.jp/rank/js/w/%s/more/%d/'

    			d = datetime.date.today()
    			td = timedelta(days=0-d.weekday())
    			d = d + td

			info_data = ""
			proceed = 0
    			for i in range(1, 7):
        			handle = urllib2.urlopen(url % (d, i))
        			data = handle.read()
        			bs = BeautifulSoup(data)

        			title = bs.find_all('h2')
        			singer = bs.find_all('h3')

				
        			j_max = 10
        			if i < 3:
            				j_max = 5

        			for j in range(0, j_max):
            				tmp_title = title[j].text.strip().encode('utf-8')
            				tmp_singer = singer[j].text.strip().encode('utf-8')	
				
					search_url = 'http://www.youtube.com/results?search_query=' + urllib.quote(tmp_title) + '+' + urllib.quote(tmp_singer)
					
                                        handle = urllib2.urlopen(search_url)
                                        data = handle.read()
                                        beautifulSoup = BeautifulSoup(data)
                                        bs_url = beautifulSoup.find_all('h3', {'class':'yt-lockup-title'})
                                        bs_time = beautifulSoup.find_all('span', {'class':'video-time'})

                                        tmp_url = "http://www.youtube.com" + bs_url[0].find('a')['href'].encode('utf-8')
                                        tmp_time = bs_time[0].text.encode('utf-8')

                                        data = tmp_title + "\n" + tmp_singer + "\n" + tmp_url + "\n" + tmp_time + "\n"

                                        info_data = info_data + data

				proceed = proceed + (j_max * 2)
				print('   %3d%% ing...' % proceed)

			f = open("OriconChart.dat", 'w')
			f.write(info_data)
			f.close()

			print("Update Complete Oricon Chart")

		newDay = False
		newHour = False					

if __name__ == '__main__':
#	set_file_info(0)	
	thread.start_new_thread(set_file_info, (0,))
	while True:
		time.sleep(30) 
