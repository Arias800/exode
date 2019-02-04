#coding: utf-8

import re
import base64

from iplugin import iplugin
##class nom de fichier
class disney(iplugin):

    def __init__(self, **kwargs):
        #Kwargs get_tmdbid, get_title
        iplugin.__init__(self)

        print kwargs['get_title']

        json = { 
            "plugin" : "disney",
            "thumb" : "http://",
        "source" :[{
            "title" : "Avatar",
            "url" : "http://",
            "qual" : "HD"
            },
            {"title" : "Avatar",
            "url" : "http://",
            "qual" : "HD"
            }]
        }

        print "paseeeeeeeeeeeeee"

        self.__json = json

        self.setList(json)
        self.setPluginName("Disney")
        
    #obligatoire
    def getJson(self):
        return self.__json

