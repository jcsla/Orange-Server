# -*- coding: cp949 -*-

import urllib
import urllib2
import json
import re
import datetime

from django.http import HttpResponse
from bs4 import BeautifulSoup

from datetime import timedelta, date

from Orange_Server.models import MelonObject
from Orange_Server.models import YouTubeObject

def get_melon_chart(request):
    url = 'http://www.melon.com/chart/index.htm'

    handle = urllib2.urlopen(url)
    data = handle.read()
    beautifulSoup = BeautifulSoup(data)
    title = beautifulSoup.find_all('div', {'class':'ellipsis rank01'})
    singer = beautifulSoup.find_all('div', {'class':'ellipsis rank02'})

    melonChart = []
    for i in range(1, 101):
        melonObject = MelonObject()
        melonObject.title = title[i].text.strip()
        melonObject.singer = singer[i].find('span').text.strip()
        melonChart.append(melonObject)

    melonChartForJSON = []
    for i in range(len(melonChart)):
        melonChartForJSON.append({"singer": melonChart[i].singer, "title": melonChart[i].title})

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
    td = timedelta(days=7-d.weekday())
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

#    infoListForJSON = []
#    for i in range(len(title)):
    resultTitle = title[0].text
    resultURl = 'http://www.youtube.com' + url[0].find('a')['href']

    youtubeObject = YouTubeObject()
    youtubeObject.title = resultTitle
    youtubeObject.url = resultURl
#    musicVideoInformationForJson = { "title" : youtubeObject.title,
#      				     "url" : youtubeObject.url}
#	infoListForJSON.append(youtubeObject)

    musicVideoInformationForJson = { "title" : youtubeObject.title,
                                     "url" : youtubeObject.url}

    return HttpResponse(json.dumps(musicVideoInformationForJson, ensure_ascii=False))

def search_music_video_information(request):
    query = request.GET['query'].encode('utf8')

    url = 'http://www.youtube.com/results?search_query=' + urllib.quote(query)
    handle = urllib2.urlopen(url)
    data = handle.read()
    beautifulSoup = BeautifulSoup(data)
    title = beautifulSoup.find_all('a', {'class':'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link ' })
    url = beautifulSoup.find_all('h3', {'class':'yt-lockup-title'})

    musicVideoInformationForJson = []
    for i in range(len(title)):
        resultTitle = title[i].text
	resultUrl = 'http://www.youtube.com' + url[i].find('a')['href']
        musicVideoInformationForJson.append({"title" : resultTitle, "url" : resultUrl})

    return HttpResponse(json.dumps(musicVideoInformationForJson, ensure_ascii=False))
