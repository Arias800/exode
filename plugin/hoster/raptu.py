#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from lib.handler.requestHandler import cRequestHandler
from lib.parser import cParser
from lib.comaddon import EXlog

def getMediaLinkForGuest(sUrl):
    oParser = cParser()
    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0')
    oRequest.addHeaderEntry('Referer',sUrl)
    sHtmlContent = oRequest.request()

    sPattern = '<source src="([^"]+)" type="video/.+?" label="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        url=[]
        qua=[]
        for i in aResult[1]:
            url.append(str(i[0]))
            qua.append(str(i[1]))

        return qua, url

    return False, False
