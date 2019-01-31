#coding: utf-8
from plugin import iplugin

import re
import base64


class disney(iplugin):

    def __init__(self):
        iplugin.__init__(self)

        #self.__Name = 'Disney'
        #self.__sDisplayName = 'ClickOpen'
        #self.setPluginName('Disney')

        self.setPluginName('Disney')
        self.addParams('TmdbId', '365855')
        self.addParams('testinou', 'moreee')

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'clickopen'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self):
        return ''

    def __modifyUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        api_call = ''

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern = 'JuicyCodes\.Run\("(.+?)"\);'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):

            media =  aResult[1][0].replace('+', '')
            media = base64.b64decode(media)

            #cPacker decode
            from resources.lib.packer import cPacker
            media = cPacker().unpack(media)

            if (media):

                sPattern = '{"file":"(.+?)","label":"(.+?)"'
                aResult = oParser.parse(media, sPattern)

                if (aResult[0] == True):
                #initialisation des tableaux
                    url=[]
                    qua=[]
                #Remplissage des tableaux
                    for i in aResult[1]:
                        url.append(str(i[0]))
                        qua.append(str(i[1]))
                #Si une seule url
                    api_call = dialog().VSselectqual(qua, url)

        if (api_call):
            return True, api_call

        return False, False
