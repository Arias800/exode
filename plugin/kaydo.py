#-*- coding: utf-8 -*-
from lib.comaddon import EXlog

SITE_IDENTIFIER = 'kaydo'
SITE_NAME = 'Kaydo'
SITE_DESC = 'Kaydo : Films et serie en HD et en streaming'

URL_MAIN = 'https://hdss.to/'
URL_LISTE = URL_MAIN

#URL_SEARCH = ('', 'sHowResultSearch')
#URL_SEARCH_MOVIES = ('', 'sHowResultSearch')
FUNCTION_SEARCH = 'sHowResultSearch'

sPattern1 = '<a href="([^"]+)".+?src="([^"]+)" alt.*?="(.+?)".*?>'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'

def ShowPlugin():
    EXlog('Kaydo Load')

