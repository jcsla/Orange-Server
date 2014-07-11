import urllib2
import json

from django.http import HttpResponse
from bs4 import BeautifulSoup

from Orange_Server.models import MelonObject

#from Orange_Server.yongjun import get_billboard_chart

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
    url = 'http://www.m.billboard.com/v/ChartSingles/Hot2255'

    handle = urllib2.urlopen(url)
    data = handle.read()
    beautifulSoup = BeautifulSoup(data)
    title = beautifulSoup.find_all('h1')
    
    return HttpResponse(title)
