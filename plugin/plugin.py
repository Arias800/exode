#-*- coding: utf-8 -*-

class iplugin(object):

    def __init__(self):

        self.__Name = ''
        self.__Params = {}
        self.__aItemValues = {}

    def getPluginName(self):
        return self.__Name

    def setPluginName(self, Name):
        self.__Name = Name

    def addParams(self, Key, Value):
        self.__Params[Key] = Value

    def getParams(self):
        return self.__Params