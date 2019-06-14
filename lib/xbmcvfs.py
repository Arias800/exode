#-*- coding: utf-8 -*-
#Portage de la lib xbmcvfs de kodi en python
from lib.comaddon import EXlog
import os

def translatePath(path):
    path = os.getcwd().replace('\\','/').split('exode')[0] + 'exode/' + path.split('special://')[1]
    EXlog(path)
    return path

def exists(path):
    path = translatePath(path)
    exists = os.path.isfile(path)
    if exists:
        return True
    else:
        return False
