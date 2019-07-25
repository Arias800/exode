#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
import os
import sys
import unicodedata
from lib.xbmcvfs import translatePath

from lib.comaddon import EXlog

#-----------------------
#     Cookies gestion
#------------------------
class GestionCookie():
    #PathCache = xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getAddonInfo("profile")).decode("utf-8")
    PathCache = translatePath("special://userdata")
    if not os.path.isdir(PathCache):
        os.mkdir(PathCache)
    EXlog(PathCache)

    def DeleteCookie(self,Domain):
        #file = os.path.join(self.PathCache,'Cookie_'+ str(Domain) +'.txt')
        Name = "/".join([self.PathCache, "cookie_%s.txt"]) % (Domain)
        #os.remove(os.path.join(self.PathCache,file))
        os.delete(Name)

    def SaveCookie(self,Domain,data):
        #Name = os.path.join(self.PathCache,'Cookie_'+ str(Domain) +'.txt')
        Name = "/".join([self.PathCache, "cookie_%s.txt"]) % (Domain)

        #save it
        #file = open(Name,'w')
        #file.write(data)
        #file.close()

        f = open(Name, 'w')
        f.write(data)
        f.close()

    def Readcookie(self,Domain):
        #Name = os.path.join(self.PathCache,'Cookie_'+ str(Domain) +'.txt')
        Name = "/".join([self.PathCache, "cookie_%s.txt"]) % (Domain)

        # try:
        #     file = open(Name,'r')
        #     data = file.read()
        #     file.close()
        # except:
        #     return ''

        try:
            f = open(Name)
            data = f.read()
            f.close()
        except:
            return ''

        return data

    def AddCookies(self):
        cookies = self.Readcookie(self.__sHosterIdentifier)
        return 'Cookie=' + cookies

def CleanName(name):
    #vire accent et '\'
    try:
        name = unicode(name, 'utf-8')#converti en unicode pour aider aux convertions
    except:
        pass
    name = unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode("unicode_escape").replace(' ','+')
    name = ''.join([i for i in name if i.isalpha() or i == '+']) #<- Supprime tout les caractere non alphanumeric sauf les +
    return name
