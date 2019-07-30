#-*- coding: utf-8 -*-
from lib.comaddon import EXlog
from lib.utils import CleanName
import os, sys, importlib, json

class plugin(object):

    def __init__(self):

        self.__FullJson = []

    def getFolder(self,title):

        app_path = os.path.dirname(os.path.abspath(__file__))
        plugin_path = os.path.join(app_path, 'plugin')

        for name in os.listdir(plugin_path):
            if name.startswith('__init__.'):
                continue
            if not name.endswith(".py"):
                continue

            name = name.replace('.py', '')

            module = importlib.import_module("plugin."+name, package=None)
            _class = getattr(module, name)
            module = _class()

            EXlog("Recherche en cours sur " + name)
            module.search(tmdbid="58425", title=title) 

            _json = module.getJson()
            self.__FullJson.append(_json)

        return json.dumps(self.__FullJson)

class iplugin(object):

    def __init__(self):

        self.__list = []
        self.__Plugin = ''
        self.__Thumb = ''
        self.__Json = {}
        self.__Source = []
            

# {
#     "plugin" : "disney",
#     "source" : {
#         "title" : "Avatar",
#         "url" : "http://",
#         "qual" : "HD"
#     }
# }

    #valid le json evite les erreurs
    def is_valid(self, json):

        if not json:
            return False
        try:
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
        except AttributeError:
            # counters is not a dictionary, ignore and move on
            pass    
                        
        return True

#nom du plugin
    def getPlugin(self):
        return self.__Plugin

    def setPlugin(self, Plugin):
        self.__Plugin = Plugin

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
        json["plugin"] =  self.getPlugin()
        json["thumb"] = self.getThumb()
        json["source"] =  self.getSource()
        return json
    
    #full json
    def getJson(self):
        if self.is_valid(self.__Json):
            return self.__Json
        else:
            return self.getList()
            
        return False

    def setJson(self, json):
        self.__Json = json

    # def serial(self):
    #     print json.dumps(self.getParams())

    def similar(self, w1, w2):
        w1 = w1.replace('+',' ').lower() + ' ' * (len(w2) - len(w1))
        w2 = CleanName(w2).lower() + ' ' * (len(w1) - len(w2))
        cal = sum(1 if i == j else 0 for i, j in zip(w1, w2)) / float(len(w1))
        #similaire a 70%
        if cal > 0.70 : 
            return True 
        else : return False


#La fonction json.dumps() permet de transformer mon dictionnaire (type dict) en une chaine de caractères (type str):
#La fonction json.loads() permet de reconvertir ma str en dict:

# playlist = {}
# playlist["nom"] = "MeshowRandom"
# playlist["musiques"] = []
# playlist["musiques"].append("Best Improvisation Ever 2")
# playlist["musiques"].append("My Theory (Bonus)")
