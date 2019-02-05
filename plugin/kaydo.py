#coding: utf-8

import re
import base64

from iplugin import iplugin
##class nom de fichier
class kaydo(iplugin):

    def __init__(self, **kwargs):
        #Kwargs get_tmdbid, get_title
        iplugin.__init__(self)

        print "Kaydo"

        print kwargs['get_title']

        json = { 
            "plugin" : "kaydo",
            "thumb" : "http://kaydo",
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

        
        self.setPlugin("kaydo")
        self.setThumb("http://kaydo")
        self.setSource("title","http", "1080")
        self.setSource("avatar","http", "1080")

