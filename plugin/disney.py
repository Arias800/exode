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
        #self.setJson(json)

        #ou

        
        self.setPlugin("Disney")
        self.setThumb("http://")
        self.setSource("title","http", "1080")
        self.setSource("avatar","http", "1080")

