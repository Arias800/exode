#-*- coding: utf-8 -*-
from kivy.properties import ObjectProperty

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

def ListMenu():
    Menu = [('Liste Film',URL_LISTE),('Liste Film',URL_LISTE),('Liste Film',URL_LISTE),('Liste Film',URL_LISTE)]
    EXlog('Menu '+str(Menu))
    return Menu

def getHtml(sUrl):
    import urllib.parse
    import urllib.request

    headers = {'User-Agent': UA}

    req = urllib.request.Request(sUrl, None, headers)
    with urllib.request.urlopen(req) as response:
       return response.read()

def showMovies(sUrl):
    html = getHtml(sUrl)

    result = re.findall('<a href="([^"]+)".+?src="([^"]+)" alt.*?="(.+?)".*?>',str(html))
    sTitle = []
    sUrl = []

    for res in result:
        sUrl.append(URL_MAIN + res[0])
        sTitle.append(res[2].replace('streaming', '').replace(' 1080p', '').replace('_', ' '))
    content = dict(zip(sTitle,sUrl))
    return content
