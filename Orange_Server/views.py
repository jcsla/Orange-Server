# -*- coding: cp949 -*-

import urllib
import urllib2
import json
import re
import datetime
import os
import django.db

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from bs4 import BeautifulSoup

from datetime import timedelta, date

from Orange_Server.models import MelonObject
from Orange_Server.models import YouTubeObject
from Orange_Server.Security import DES

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

@method_decorator(csrf_exempt)
def Test(request):
    if request.method == 'POST':
        data = request.body

        key = 'b0d9b872'
        iv = 'b0d9b872'

        des = DES(iv, key)
        decr_data = des.decrypt(file_data)

        return HttpResponse(decr_data)	

    else:
        return HttpResponse("")

def search_music_video_information(request):
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

@method_decorator(csrf_exempt)
def upload_play_list(request):
    if request.method == 'POST':
	data = request.body
	contents = json.loads(data)

	chart_name = contents['chart_name']
	chart_name = chart_name.lower()
	chart_list = contents['chart_list']
	
	lists = PlayList.objects.filter(name=chart_name)
	
	if len(lists):
#	    p = PlayList.objects.get(name=chart_name)
#	    p.delete()
	    return HttpResponse("False")
	
	url = "/home/jcsla/Orange_Server/Orange_Server/PlayLists/%s.dat" % chart_name
	
	file_data = ""
	for i in range(0, len(chart_list)):
	    tmp_title = chart_list[i]['title']
	    tmp_singer = chart_list[i]['singer']
	    tmp_url = chart_list[i]['url']
	    tmp_time = chart_list[i]['time']

	    file_data = file_data + tmp_title + "\n" + tmp_singer + "\n" + tmp_url + "\n" + tmp_time + "\n"
	
	file_data = file_data.encode('utf-8')
	f = open(url, 'w')
	f.write(file_data)
	f.close()

	play_list = PlayList(name=chart_name, cnt='0')
	play_list.save()
	
        return HttpResponse(file_data)

    elif request.method == 'GET':
        return HttpResponse('')

    else: 
	return Http404

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


    
