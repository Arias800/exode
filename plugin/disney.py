#-*- coding: utf-8 -*-
from kivymd.bottomsheet import MDListBottomSheet

from lib.comaddon import EXlog

import re 

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

def ListMenu(self, kwargs):
    bs = MDListBottomSheet()
    Menu = [('Liste Film',URL_LISTE)]
    for txt in Menu:
        text = ("%s") % (txt[0])
        bs.add_item(text, lambda x: self.PluginMenu(sName=str(kwargs['sName']),sCat=str(int(kwargs['sCat'])+1),sUrl=str(txt[1])))
    bs.open()
    return kwargs['sCat']

def getHtml(sUrl):
    import urllib.parse
    import urllib.request

    headers = {'User-Agent': UA}

    req = urllib.request.Request(sUrl, None, headers)
    with urllib.request.urlopen(req) as response:
       return response.read()

def showMovies(self, kwargs):
    bs = MDListBottomSheet()
    html = getHtml(kwargs['sUrl'])

    result = re.findall('<a href="([^"]+)".+?src="([^"]+)" alt.*?="(.+?)".*?>',str(html))
    sTitle = []
    sUrl = []

    for res in result:
        sUrl.append(URL_MAIN + res[0])
        sTitle.append(res[2].replace('streaming', '').replace(' 1080p', '').replace('_', ' '))
    content = dict(zip(sTitle,sUrl))

    for aEntry in content.items():
        text = ("%s") % (aEntry[0])
        bs.add_item(text, lambda x: self.PluginMenu(sName=str(kwargs['sName']), sCat=str(int(kwargs['sCat'])+1)))
    bs.open()
    return kwargs['sCat']
