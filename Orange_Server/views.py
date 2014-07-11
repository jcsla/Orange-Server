import urllib2
import json

from django.http import HttpResponse
from bs4 import BeautifulSoup

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
    return HttpResponse("")

def get_music_video_information(request):
    singer = request.GET['singer'].encode('utf8')
    title = request.GET['title'].encode('utf8')

    url = 'http://www.youtube.com/results?search_query=' + singer + title
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