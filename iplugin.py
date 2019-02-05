#-*- coding: utf-8 -*-

import os, sys
import json


class iplugin(object):

    def __init__(self):

        self.__list = []
        self.__Plugin = ''
        self.__Thumb = ''
        self.__Json = {}
        self.__Source = []


    def getFolder(self):

        app_path = os.path.dirname(os.path.abspath(__file__))
        plugin_path = os.path.join(app_path, 'plugin')

        for name in os.listdir(plugin_path):
            if name.startswith('__init__.'):
                continue
            if not name.endswith(".py"):
                continue

            name = name.replace('.py', '')

            plugin = __import__('plugin.%s' % name, fromlist=[name])
            _class = getattr(plugin, name)
            plugin = _class(get_tmdbid="testt", get_title="avatar")

        #json ou list
            if self.is_valid(plugin.getJson()):
                return plugin.getJson()
            elif self.is_valid(plugin.getList()): 
                return plugin.getList()
            else:
                print "erreur Json"
            

# {
#     "plugin" : "disney",
#     "source" : {
#         "title" : "Avatar",
#         "url" : "http://",
#         "qual" : "HD"
#     }
# }

    def getTmdbID(self):
        return self.__Tmdbid

    def setTmdbID(self, tmdbid):
        self.__Tmdbid = tmdbid

#valid le json evite les erreurs
    def is_valid(self, json):

        if not json:
            return False

        if json.get('plugin') is None:
            return False
        if json.get('thumb') is None:
            return False
        for e in json.get('source'):
            if e.get('title') is None:
                return False
            if e.get('url') is None:
                return False
            if e.get('qual') is None:
                return False
        return True

#nom du plugin
    def getPlugin(self):
        return self.__Plugin

    def setPlugin(self, Plugin):
        self.__PluginName = Plugin

#image plugin
    def getThumb(self):
        return self.__Thumb

    def setThumb(self, Thumb):
        self.__Thumb = Thumb
    
#source plugin
    def getSource(self):
        return self.__Source

    def setSource(self, Title, Url, Qual):
        self.__Source.append({"title": Title, "url": Url, "qual": Qual})

    def getList(self):
        json = {}
        json['plugin'] =  self.getPlugin()
        json['thumb'] = self.getThumb()
        json['source'] =  self.getSource()
        return json
    
#full json
    def getJson(self):
        return self.__Json

    def setJson(self, json):
        self.__Json = json

    # def serial(self):
    #     print json.dumps(self.getParams())


#La fonction json.dumps() permet de transformer mon dictionnaire (type dict) en une chaine de caractères (type str):
#La fonction json.loads() permet de reconvertir ma str en dict:


# playlist = {}
# playlist["nom"] = "MeshowRandom"
# playlist["musiques"] = []
# playlist["musiques"].append("Best Improvisation Ever 2")
# playlist["musiques"].append("My Theory (Bonus)")