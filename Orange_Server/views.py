# -*- coding: cp949 -*-

import urllib
import urllib2
import json
import re
import datetime
import os

from django.http import HttpResponse
from bs4 import BeautifulSoup

from datetime import timedelta, date

from Orange_Server.models import MelonObject
from Orange_Server.models import YouTubeObject


import thread
import time    

def get_melon_chart(request):
    """
    url = 'http://www.melon.com/chart/index.htm'

    handle = urllib2.urlopen(url)
    data = handle.read()
    beautifulSoup = BeautifulSoup(data)
    title = beautifulSoup.find_all('div', {'class':'ellipsis rank01'})
    singer = beautifulSoup.find_all('div', {'class':'ellipsis rank02'})
    """
    melonChart = []
    f = open("/home/jcsla/Orange_Server/Orange_Server/MelonChart.dat", 'r')
    for i in range(1, 101):
        melonObject = MelonObject()
        melonObject.title = f.readline().strip()#title[i].text.strip()
        melonObject.singer = f.readline().strip()#singer[i].find('span').text.strip()
	melonObject.url = f.readline().strip()
	melonObject.time = f.readline().strip()
	
        melonChart.append(melonObject)
    f.close()
    melonChartForJSON = []
    for i in range(len(melonChart)):
        melonChartForJSON.append({"singer": melonChart[i].singer, "title": melonChart[i].title, "url": melonChart[i].url, "time": melonChart[i].time})

    #return HttpResponse(singer)
    return HttpResponse(json.dumps(melonChartForJSON, ensure_ascii=False))

def get_billboard_chart(request):
    url = 'http://www.billboard.com/charts/hot-100?page=%d'

    melonChart = []
    for i in range(0, 10):
        handle = urllib2.urlopen(url % i)
        data = handle.read()
        bs = BeautifulSoup(data)
	title = bs.find_all('h1')
	singer = bs.find_all('p', {'class':'chart_info'})

	for j in range(0, 10):
	    melonObject = MelonObject()
	    melonObject.title = title[j+1].text.strip()
	    melonObject.singer = singer[j].find('a').text.strip()
	    melonChart.append(melonObject)

    melonChartForJSON = []
    for i in range(len(melonChart)):
	melonChartForJSON.append({"singer": melonChart[i].singer, "title": melonChart[i].title})

    return HttpResponse(json.dumps(melonChartForJSON, ensure_ascii=False))

def get_oricon_chart(request):
    url = 'http://www.oricon.co.jp/rank/js/w/%s/more/%d/'

    d = datetime.date.today()
    td = timedelta(days=0-d.weekday())
    d = d + td

    melonChart = []
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
	    melonObject = MelonObject()
	    melonObject.title = title[j].text.strip()
	    melonObject.singer = singer[j].text.strip()
	    melonChart.append(melonObject)

    melonChartForJSON = []
    for i in range(len(melonChart)):
	melonChartForJSON.append({"singer": melonChart[i].singer, "title": melonChart[i].title})

    return HttpResponse(json.dumps(melonChartForJSON, ensure_ascii=False))

def get_music_video_information(request):
    singer = request.GET['singer'].encode('utf8')
    title = request.GET['title'].encode('utf8')

    url = 'http://www.youtube.com/results?search_query=' + urllib.quote(singer) + '+' + urllib.quote(title)
    handle = urllib2.urlopen(url)
    data = handle.read()
    beautifulSoup = BeautifulSoup(data)
    title = beautifulSoup.find_all('a', {'class':'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link ' })
    url = beautifulSoup.find_all('ol', {'class':'item-section'})

    resultTitle = title[0].text
    resultURl = 'http://www.youtube.com' + url[0].find('a')['href']

    youtubeObject = YouTubeObject()
    youtubeObject.title = resultTitle
    youtubeObject.url = resultURl

    musicVideoInformationForJson = { "title" : youtubeObject.title,
                                     "url" : youtubeObject.url}

    return HttpResponse(json.dumps(musicVideoInformationForJson, ensure_ascii=False))

def search_music_video_information(request):
    query = request.GET['query'].encode('utf8')

    url = 'http://www.youtube.com/results?search_query=' + urllib.quote(query)
    print (url)
    handle = urllib2.urlopen(url)
    data = handle.read()
    beautifulSoup = BeautifulSoup(data)

    contents = beautifulSoup.find_all('div', {'class':'yt-lockup yt-lockup-tile yt-lockup-video yt-uix-tile clearfix'})

    musicVideoInformationForJson = []

    for i in range(len(contents)):
        resultTitle = contents[i].find('h3', {'class':'yt-lockup-title'}).text
        resultUrl = 'http://www.youtube.com' + contents[i].find('h3', {'class':'yt-lockup-title'}).find('a')['href']
        resultTime = contents[i].find('span', {'class':'video-time'}).text
        
        musicVideoInformationForJson.append({"title" : resultTitle, "url" : resultUrl, "time" : resultTime})

    return HttpResponse(json.dumps(musicVideoInformationForJson, ensure_ascii=False))
