#coding: utf-8

import re
import base64

from iplugin import iplugin

##class nom de fichier
class disney(iplugin):

    def __init__(self, **kwargs):
        #Kwargs get_tmdbid, get_title
        iplugin.__init__(self)
        #print "DIsneyyyyyy"
        #print kwargs['get_title']

        json = { 
            "plugin" : "disney",
            "thumb" : "http://disney",
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
        self.setThumb("http://disney")
        self.setSource("1001 pattes","http://disneyhdsource.ml/mp4/1001_pattes.mp4", "1080")
        self.setSource("Aladdin","http://disneyhdsource.ml/mp4/aladdin.mp4", "1080")

