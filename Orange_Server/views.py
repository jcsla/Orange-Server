# -*- coding: cp949 -*-

import urllib
import urllib2
import json
import re
import datetime
import os
import django.db

from django.http import HttpResponse
from bs4 import BeautifulSoup

from datetime import timedelta, date

from Orange_Server.models import MelonObject
from Orange_Server.models import YouTubeObject

import thread
import time    
from PlayLists.models import PlayList

def get_melon_chart(request):
    melonChart = []
    f = open("/home/jcsla/Orange_Server/Orange_Server/MelonChart.dat", 'r')
#    f = open("Orange_Server/MelonChart.dat", 'r')
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
    
    f = open("/home/jcsla/Orange_Server/Orange_Server/BillboardChart.dat", 'r')
#    f = open("Orange_Server/BillboardChart.dat", 'r')
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

    f = open("/home/jcsla/Orange_Server/Orange_Server/OriconChart.dat", 'r')
#    f = open("Orange_Server/OriconChart.dat", 'r')
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
    handle.close()

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

def Test():
    """
    p1 = PlayList(name='Melon_Chart_140727', cnt='0')
    p1.save()
    p2 = PlayList(name='Billboard_Chart_140727', cnt='0')
    p2.save()
    p3 = PlayList(name='Oricon_Chart_140727', cnt='0')
    p3.save()

    p4 = PlayList(name='Third', cnt='0')
    p4.save()
    p5 = PlayList(name='4th', cnt='0')
    p5.save()
    """
    #list = PlayList.objects.filter(name='Second')

    #if len(list) == 0:
        #print (len(list))
    #PlayList.objects.filter(id=2).update(name='Second')

    list = PlayList.objects.order_by("-id")[0:5]
    for i in range(len(list)):
        print (list[i])

def search_music_video_information(request):
    Test()

    query = request.GET['query'].encode('utf8')

    url = 'http://www.youtube.com/results?search_query=' + urllib.quote(query)
    
    handle = urllib2.urlopen(url)
    data = handle.read()
    handle.close()

    beautifulSoup = BeautifulSoup(data, from_encoding='utf-8')

    contents = beautifulSoup.find_all('div', {'class':'yt-lockup yt-lockup-tile yt-lockup-video yt-uix-tile clearfix'})

    musicVideoInformationForJson = []

    for i in range(len(contents)):
        resultTitle = contents[i].find('h3', {'class':'yt-lockup-title'}).text
        resultUrl = 'http://www.youtube.com' + contents[i].find('h3', {'class':'yt-lockup-title'}).find('a')['href']
        resultTime = contents[i].find('span', {'class':'video-time'}).text
        
        musicVideoInformationForJson.append({"title" : resultTitle, "url" : resultUrl, "time" : resultTime})

    return HttpResponse(json.dumps(musicVideoInformationForJson, ensure_ascii=False))

def search_music_video_information_for_page(request):
    query = request.GET['query'].encode('utf8')
    page = request.GET['page'].encode('utf8')

    url = 'http://www.youtube.com/results?search_query=' + urllib.quote(query) + '&page=' + urllib.quote(page)
    
    handle = urllib2.urlopen(url)
    data = handle.read()
    handle.close()
    
    bs = BeautifulSoup(data, from_encoding='utf-8')

    contents = bs.find_all('div', {'class':'yt-lockup yt-lockup-tile yt-lockup-video yt-uix-tile clearfix'})

    musicVideoInformationForJson = []

    next = bs.find_all('a', {'class':'yt-uix-button  yt-uix-pager-button yt-uix-sessionlink yt-uix-button-default yt-uix-button-size-default'})

    for i in range(len(contents)):
        resultTitle = contents[i].find('h3', {'class':'yt-lockup-title'}).text
        resultUrl = 'http://www.youtube.com' + contents[i].find('h3', {'class':'yt-lockup-title'}).find('a')['href']
        resultTime = contents[i].find('span', {'class':'video-time'}).text
        
        musicVideoInformationForJson.append({"title" : resultTitle, "url" : resultUrl, "time" : resultTime})

    return HttpResponse(json.dumps(musicVideoInformationForJson, ensure_ascii=False))

def search_play_list(request):
    query = request.GET['query'].encode('utf8')

    # select db
    lists = PlayList.objects.filter(name__contains=query)

    resultPlayListForJSON = []
    for i in range(len(lists)):
        resultPlayList = lists[i]
        
        resultPlayListForJSON.append({"title" : resultPlayList.name, "hits_count" : resultPlayList.cnt})
    
    return HttpResponse(json.dumps(resultPlayListForJSON, ensure_ascii=False))

def get_recent_play_list(request):
    lists = PlayList.objects.order_by("-id")[0:5]

    resultPlayListForJSON = []
    for i in range(len(lists)):
        resultPlayList = lists[i]
        
        resultPlayListForJSON.append({"title" : resultPlayList.name, "hits_count" : resultPlayList.cnt})
    
    return HttpResponse(json.dumps(resultPlayListForJSON, ensure_ascii=False))

def upload_play_list(request):
    if request.method == "POST":
        return HttpResponse("POST")

    #else if request.method == "GET":
    else
        return HttpResponse("GET")


def get_high_cnt_play_list(request):
    lists = PlayList.objects.order_by("-cnt")[0:5]

    resultPlayListForJSON = []
    for i in range(len(lists)):
        resultPlayList = lists[i]
        
        resultPlayListForJSON.append({"title" : resultPlayList.name, "hits_count" : resultPlayList.cnt})
    
    return HttpResponse(json.dumps(resultPlayListForJSON, ensure_ascii=False))


def get_play_list(request):
    title = request.GET['title'].encode('utf8')

    try:
        resultPlayList = PlayList.objects.get(name=title)
        
        resultPlayList.cnt = resultPlayList.cnt + 1
        resultPlayList.save()

        path = "/home/jcsla/Orange_Server/Orange_Server/PlayLists/%s.dat" % title
        #path = "Orange_Server/PlayLists/%s.dat" % title
        
        f = open(path, 'r')

        playList = []
        while 1:
            playListObject = MelonObject()
            title = f.readline().strip()
            if not title: break

            playListObject.title = title
            playListObject.singer = f.readline().strip()
            playListObject.url = f.readline().strip()
            playListObject.time = f.readline().strip()
            playList.append(playListObject)

        f.close()

        playListForJSON = []
        for i in range(len(playList)):
            playListForJSON.append({
                "singer": playList[i].singer, 
                "title": playList[i].title, 
                "url": playList[i].url, 
                "time": playList[i].time})

        return HttpResponse(json.dumps(playListForJSON, ensure_ascii=False))

    except PlayList.DoesNotExist:
        return HttpResponse()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       


    