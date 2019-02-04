#-*- coding: utf-8 -*-

import os, sys


class iplugin(object):

    def __init__(self):

        self.__list = []
        self.__PluginName = ''


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
            #self.setList(plugin.getJson())

            print plugin.getPluginName()
            print "listttttttttt", plugin.getList()
            

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


    def is_valid(json):

        if json.get('plugin') is None:
            return False
        if json.get('thumb') is None:
            return False
        if json.get('source').get('title') is None:
            return False
        if json.get('source').get('url') is None:
            return False
        if json.get('source').get('qual') is None:
            return False

        return True

    def getPluginName(self):
        return self.__PluginName

    def setPluginName(self, PluginName):

        print "plugin name", PluginName
        self.__PluginName = PluginName
    
    def getTitle(self):
        return "titleeeeeee"

    def addParams(self, Key, Value):
        test = self.__Params[Key] = Value
        self.__list.append(test)

    def getParams(self):
        return self.__Params
    
    def getList(self):
        print "list", self.__list
        return self.__list

#envoie un json full
    def setList(self, list):
        self.__list.append(list)

    def serial(self):
        import json
        print json.dumps(self.getParams())


#La fonction json.dumps() permet de transformer mon dictionnaire (type dict) en une chaine de caractères (type str):
#La fonction json.loads() permet de reconvertir ma str en dict:


# playlist = {}
# playlist["nom"] = "MeshowRandom"
# playlist["musiques"] = []
# playlist["musiques"].append("Best Improvisation Ever 2")
# playlist["musiques"].append("My Theory (Bonus)")