#-*- coding: utf-8 -*-
from kivymd.bottomsheet import MDListBottomSheet
from lib.handler.requestHandler import cRequestHandler
from lib.comaddon import EXlog

import re,json

SITE_IDENTIFIER = 'disneyhd_tk'
SITE_NAME = 'Disney HD'
SITE_DESC = 'Disney HD: Tous les films Disney en streaming'

URL_MAIN = 'https://disneyhd.tk/'
URL_LISTE = URL_MAIN + '?page=liste.php'
ANIM_ENFANTS = ('http://', 'load')

#URL_SEARCH = ('', 'sHowResultSearch')
#URL_SEARCH_MOVIES = ('', 'sHowResultSearch')
FUNCTION_SEARCH = 'sHowResultSearch'

sPattern1 = '<a href="([^"]+)".+?src="([^"]+)" alt.*?="(.+?)".*?>'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'

def getJson():
    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'
    oRequest = cRequestHandler('https://disneyhd.tk/movies_list.php')
    oRequest.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequest.request()

    aResult = re.findall('<img src="([^"]+)"><div class="title">([^>]+)<\/div><\/a><a class="item" href="([^"]+)"',str(sHtmlContent))
    d1 = {"plugin":SITE_NAME}

    i = 0
    for aEntry in aResult:
        if i >= 2:
            break
        sUrl = URL_MAIN + aEntry[2]
        sQual,url = getFinalUrl(sUrl)

        for qual,sUrl in zip(sQual,url):
            sTitle = aEntry[1]
            extra = ({"source":{'title' : sTitle,"url":sUrl,"qual":qual}})
            d1.update(extra)
        i = i+1

    JSON = json.dumps(d1)

    return JSON

def getFinalUrl(sUrl):

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #film
    if '<ol id="playlist">' in str(sHtmlContent):
        aResult = re.findall('<li data-trackurl="([^"]+)">(.+?)<\/li>',str(sHtmlContent))
        
    elif 'data-ws=' in str(sHtmlContent):
        aResult = re.findall('data-ws="([^"]+)">(.+?)</span>',str(sHtmlContent))
    else:
        aResult = re.findall('<span class="qualiteversion" data-qualurl="([^"]+)">([^"]+)</span>',str(sHtmlContent))

    url = []
    sQual = []
    for aEntry in aResult:
        url.append(aEntry[0])
        sQual.append(aEntry[1])

    return sQual,url
