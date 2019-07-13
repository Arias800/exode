#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from lib.handler.requestHandler import cRequestHandler
from lib.parser import cParser

import re

def getMediaLinkForGuest(sUrl):

    api_call = sUrl
    #full moviz lien direct final nowvideo
    if 'zerocdn.to' in api_call:
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
        api_call = api_call + '|User-Agent=' + UA

    #Special pour mangacity
    if 'pixsil' in api_call:
        api_call = api_call.split('|')[0] + '|Referer=http://www.mangacity.org/jwplayer/player.swf'

    #Modif pr aliez
    if 'aplayer1.me' in api_call:
        UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
        api_call = api_call + '|User-Agent=' + UA

    if 'sport7' in api_call:
        UA= 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
        api_call = api_call + '|User-Agent=' + UA + '&referer=' + sUrl

    #Special pour hd-stream.in et film-streaming.co
    if 'playlist.m3u8' in api_call:
        base = re.sub(r'(playlist.m3u8*.+)', '', api_call)
        oRequest = cRequestHandler(api_call)
        sHtmlContent = oRequest.request()
        sPattern =  ',NAME="([^"]+)".+?(chunklist.+?.m3u8)'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=[]
            api_call = ''
            #Remplissage des tableaux
            for i in aResult[1]:
                url.append(str(i[1]))
                qua.append(str(i[0]))


    if (api_call):
        return True, api_call

    return False, False
