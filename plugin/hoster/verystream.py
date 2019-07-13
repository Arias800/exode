#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from lib.handler.requestHandler import cRequestHandler

import re

def getMediaLinkForGuest(sUrl):
    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    api_call = ''

    sPattern =  'id="videolink">([^<>]+)<\/p>'
    aResult = re.findall(sPattern, str(sHtmlContent))
    
    if (aResult):
        
        api_call = 'https://verystream.com/gettoken/' + aResult[0] + '?mime=true'

    if (api_call):
        return True, api_call

    return False, False
