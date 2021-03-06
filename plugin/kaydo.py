#-*- coding: utf-8 -*-
from kivymd.bottomsheet import MDListBottomSheet
from lib.handler.requestHandler import cRequestHandler
from lib.comaddon import EXlog
from lib.hoster import checkHoster
from lib.parser import cParser

import re, json

SITE_IDENTIFIER = 'kaydo'
SITE_NAME = 'Kaydo'
SITE_DESC = 'Kaydo : Films et serie en HD et en streaming'

URL_MAIN = 'https://hdss.to/'

URL_SEARCH = (URL_MAIN + 'search/avengers', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'sHowResultSearch'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'

from iplugin import iplugin

##class nom de fichier
class kaydo(iplugin):

    def __init__(self, **kwargs):
        #Kwargs tmdbid, title
        iplugin.__init__(self)
        self.setPlugin("Kaydo") #nom du site
        self.setThumb("http://kaydo") #thumb du site non utiliser pour le moment

    def search(self, **kwargs):
            
        oRequest = cRequestHandler(URL_MAIN + 'search/'+kwargs['title'])
        oRequest.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern = 'class="TPost C">.+?href="([^"]+)">.+?<img.+?src="([^"]+)".+?<h3 class="Title">([^<]+)</h3> .+?class="Qlty">([^<]+)<'
        aResult = oParser.parse(sHtmlContent, sPattern) 

        if (aResult[0] == True):
            url=[]
            qua=[]
            for aEntry in aResult[1]:

                sUrl = aEntry[0]
                qual = aEntry[3]
                sTitle = aEntry[2]

                if self.similar(kwargs['title'], sTitle):

                    sQual,url = getFinalUrl(sUrl,qual)

                    for qual,sUrl in zip(sQual,url):
                        qua, Url = checkHoster(sUrl)

                        if qua == True:
                            qua = sQual  

                        if Url == False:
                            continue
                        else:
                            #Si plus d'un url
                            if type(Url) is list:
                                for qua1 , Url1 in zip(qua, Url):
                                    self.setSource(sTitle,Url1,qua1)
                            else:
                                self.setSource(sTitle,Url,qua[0])


def getJson2(title):
    oRequest = cRequestHandler(URL_MAIN + 'search/'+title)
    oRequest.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequest.request()

    oParser = cParser()
    sPattern = 'class="TPost C">.+?href="([^"]+)">.+?<img.+?src="([^"]+)".+?<h3 class="Title">([^<]+)</h3> .+?class="Qlty">([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern) 

    d1 = {"plugin":SITE_NAME}

    dest = []

    if (aResult[0] == True):
        url=[]
        qua=[]
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            qual = aEntry[3]
            sTitle = aEntry[2]
            sQual,url = getFinalUrl(sUrl,qual)

            for qual,sUrl in zip(sQual,url):
                qua, Url = checkHoster(sUrl)

                if qua == True:
                    qua = sQual  

                if Url == False:
                    continue
                else:
                    #Si plus d'un url
                    if type(Url) is list:
                        for qua1 , Url1 in zip(qua, Url):
                            extra = ({"source":{'title' : sTitle,"url":Url1,"qual":qua1}})
                            dest.append((d1))
                            dest.append((extra))
                    else:
                        extra = ({"source":{'title' : sTitle,"url":Url,"qual":qua[0]}})
                        dest.append((d1))
                        dest.append((extra))                       

        JSON = json.dumps(dest)
        return JSON

def getFinalUrl(sUrl,qual=''):

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #Recuperer variable pour url de base
    aResult1 = re.findall('id=.+?trembed=([^"]+)(?:"|&quot;) frameborder',str(sHtmlContent))

    url = []
    sQual = []

    for aEntry in aResult1:
        site = URL_MAIN + "?trembed=" + aEntry.replace('#038;','').replace('amp;','')

        oRequestHandler = cRequestHandler(site)
        sHtmlContent = oRequestHandler.request()

        #Recuperation de l'url suivante
        aResult2 = re.search('<div class="Video"><iframe.+?src="([^"]+)"',str(sHtmlContent)).group(1)

        Url = ''.join(aResult2)
        oRequestHandler = cRequestHandler(Url)
        sHtmlContent = oRequestHandler.request()

        #Recuperation de l'id
        aResult3 = re.search("var id.+?'(.+?)'",str(sHtmlContent)).group(1).replace('\\','')
        sPost = ''.join(aResult3)[::-1]
        sUrl1 = URL_MAIN + '?trhidee=1&trfex=' + sPost

        oRequestHandler = cRequestHandler(sUrl1)
        oRequestHandler.addHeaderEntry('Referer', Url)
        sHtmlContent = oRequestHandler.request()
        sHosterUrl = oRequestHandler.getRealUrl()

        if 'public/dist' in sHosterUrl:
            sHosterUrl = 'https://' + sHosterUrl.split('/')[2] + '/hls/'+sHosterUrl.split('id=')[1] + '/'+sHosterUrl.split('id=')[1] + '.playlist.m3u8'

        url.append(sHosterUrl)
        sQual.append(qual)

    return sQual,url
