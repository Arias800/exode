#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#A corriger plus tard je le mets juste pour pas bloquer Kaydo
from lib.handler.requestHandler import cRequestHandler
from lib.parser import cParser

def getMediaLinkForGuest(sUrl):
    api_call = False

    oParser = cParser()
    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    sPattern = '<source src="([^"]+)" type="video/.+?"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        url=[]
        qua=[]
        for i in aResult[1]:
            url.append(str(i[0]))
            qua.append(str(i[1]))

    if (api_call):
        return qua, url

    return False, False
