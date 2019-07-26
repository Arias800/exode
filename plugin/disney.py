#-*- coding: utf-8 -*-
from kivymd.bottomsheet import MDListBottomSheet
from lib.handler.requestHandler import cRequestHandler
from lib.comaddon import EXlog
from lib.hoster import checkHoster
from lib.parser import cParser

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

def getJson(title):
    oRequest = cRequestHandler('https://disneyhd.tk/movies_list.php')
    oRequest.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequest.request()

    oParser = cParser()
    sPattern = 'href="([^"]+)" title="([^"]+)"><img src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern) 

    d1 = {"plugin":SITE_NAME}
    dest = []
    
    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sTitle = aEntry[1]
            if title.lower() in sTitle.lower():
                sUrl = URL_MAIN + aEntry[0]

                sQual,url = getFinalUrl(sUrl)

                for qual,sUrl1 in zip(sQual,url):

                    extra = {"source":{'title' : sTitle,"url":sUrl1,"qual":qual}}
                    dest.append((d1))
                    dest.append((extra))

    JSON = json.dumps(dest)

    return JSON

def getFinalUrl(sUrl):
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

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
