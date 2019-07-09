#-*- coding: utf-8 -*-
from kivymd.bottomsheet import MDListBottomSheet
from lib.handler.requestHandler import cRequestHandler
from lib.comaddon import EXlog

import re 

SITE_IDENTIFIER = 'kaydo'
SITE_NAME = 'Kaydo'
SITE_DESC = 'Kaydo : Films et serie en HD et en streaming'

URL_MAIN = 'https://hdss.to/'
URL_LISTE = URL_MAIN + 'films/'
ANIM_ENFANTS = ('http://', 'load')

#URL_SEARCH = ('', 'sHowResultSearch')
#URL_SEARCH_MOVIES = ('', 'sHowResultSearch')
FUNCTION_SEARCH = 'sHowResultSearch'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'

def ListMenu(self, kwargs):
    bs = MDListBottomSheet()
    Menu = [('Liste Film',URL_LISTE)]
    for txt in Menu:
        text = ("%s") % (txt[0])
        bs.add_item(text, lambda x: self.PluginMenu(sName=str(kwargs['sName']),sCat=str(int(kwargs['sCat'])+1),sUrl=str(txt[1])))
    bs.open()
    return kwargs['sCat']

def showMovies(self, kwargs):
    bs = MDListBottomSheet()

    oRequest = cRequestHandler(kwargs['sUrl'])
    oRequest.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequest.request()

    result = re.findall('class="TPost C">.+?href="([^"]+)">.+?<img.+?src="([^"]+)".+?<h3 class="Title">([^<]+)</h3> .+?class="Qlty">([^<]+)<.+?<p>.+?streaming,([^<]+)',str(sHtmlContent), re.MULTILINE|re.DOTALL)
    sTitle = []
    sUrl = []

    for res in result:
        sUrl.append(URL_MAIN + res[0])
        sTitle.append(res[2])
    content = dict(zip(sTitle,sUrl))

    for aEntry in content.items():
        EXlog(content)
        text = ("%s") % (aEntry[0])
        bs.add_item(text, lambda x: self.PluginMenu(sName=str(kwargs['sName']), sCat=str(int(kwargs['sCat'])+1)))
    bs.open()
    return kwargs['sCat']
