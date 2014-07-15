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
    melonChart = []
#    f = open("/home/jcsla/Orange_Server/Orange_Server/MelonChart.dat", 'r')
    f = open("Orange_Server/MelonChart.dat", 'r')
    for i in range(1, 101):
        melonObject = MelonObject()
        melonObject.title = f.readline().strip()
        melonObject.singer = f.readline().strip()
	melonObject.url = f.readline().strip()
	melonObject.time = f.readline().strip()
        melonChart.append(melonObject)

    f.close()
    melonChartForJSON = []
    for i in range(len(melonChart)):
        melonChartForJSON.append({"singer": melonChart[i].singer, "title": melonChart[i].title, "url": melonChart[i].url, "time": melonChart[i].time})

    return HttpResponse(json.dumps(melonChartForJSON, ensure_ascii=False))

def get_billboard_chart(request):
    billboardChart = []
    
#    f = open("/home/jcsla/Orange_Server/Orange_Server/MelonChart.dat", 'r')
    f = open("Orange_Server/BillboardChart.dat", 'r')
    for i in range(1, 101):
        billboardObject = MelonObject()
        billboardObject.title = f.readline().strip()
        billboardObject.singer = f.readline().strip()
        billboardObject.url = f.readline().strip()
        billboardObject.time = f.readline().strip()
        billboardChart.append(billboardObject)

    f.close()

    billboardChartForJSON = []
    for i in range(len(billboardChart)):
	billboardChartForJSON.append({"singer": billboardChart[i].singer, "title": billboardChart[i].title, "url": billboardChart[i].url, "time": billboardChart[i].time})

    return HttpResponse(json.dumps(billboardChartForJSON, ensure_ascii=False))

def get_oricon_chart(request):
    oriconChart = []

#    f = open("/home/jcsla/Orange_Server/Orange_Server/MelonChart.dat", 'r')
    f = open("Orange_Server/OriconChart.dat", 'r')
    for i in range(0, 50):
        oriconObject = MelonObject()
        oriconObject.title = f.readline().strip()
        oriconObject.singer = f.readline().strip()
        oriconObject.url = f.readline().strip()
        oriconObject.time = f.readline().strip()
        oriconChart.append(oriconObject)

    f.close()
    oriconChartForJSON = []
    for i in range(len(oriconChart)):
        oriconChartForJSON.append({"singer": oriconChart[i].singer, "title": oriconChart[i].title, "url": oriconChart[i].url, "time": oriconChart[i].time})

    return HttpResponse(json.dumps(oriconChartForJSON, ensure_ascii=False))

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
