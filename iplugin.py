#-*- coding: utf-8 -*-
#from resources.lib.config import cConfig
from lib.comaddon import EXlog
from lib.xbmcvfs import exists, translatePath

import sys, os, importlib

def getPluginHandle():
    try:
        return int( sys.argv[ 1 ] )
    except:
        return 0

def getPluginPath():
    try:
        return sys.argv[0]
    except:
        return ''

def __getFileNamesFromFolder(sFolder):
    aNameList = []
    sFolder = translatePath(sFolder)
    items = os.listdir(sFolder)
    items.sort()
    for sItemName in items:
        if not sItemName.endswith(".py"):
            continue

        sFilePath = "/".join([sFolder, sItemName])

        # xbox hack
        sFilePath = sFilePath.replace('\\', '/')

        EXlog("Load Plugin %s" % (sItemName))

        if (sFilePath.lower().endswith('py')):
            sItemName = sItemName.replace('.py', '')
            aNameList.append(sItemName)
    return aNameList

def __importPlugin(sName):
    module = importlib.import_module("plugin."+sName, package=None)
    sSiteName = module.SITE_NAME
    sSiteDesc = module.SITE_DESC
    sSiteIdentifer = sName
    return sSiteName, sSiteIdentifer, sSiteDesc

def getAvailablePlugins(force = False):
    sFolder = "special://plugin"

    # xbox hack
    sFolder = sFolder.replace('\\', '/')
    EXlog("Sites Folder " + sFolder)

    aFileNames = __getFileNamesFromFolder(sFolder)

    aPlugins = []
    for sFileName in aFileNames:
        aPlugin = __importPlugin(sFileName)
        if (aPlugin[0] != False):
            sSiteName = aPlugin[0]
            sPluginSettingsName = aPlugin[1]
            sSiteDesc = aPlugin[2]

    return aPlugins

def getAllPlugins():
    sFolder = "special://plugin"

    # xbox hack
    sFolder = sFolder.replace('\\', '/')
    EXlog("Sites Folder " + sFolder)

    aFileNames = __getFileNamesFromFolder(sFolder)

    aPlugins = []
    for sFileName in aFileNames:
        if not '__init__' in sFileName:
            aPlugin = __importPlugin(sFileName)
            if (aPlugin[0] != False):
                sSiteName = aPlugin[0]
                sPluginSettingsName = aPlugin[1]
                sSiteDesc = aPlugin[2]

                aPlugins.append(__createAvailablePluginsItem(sSiteName, sFileName, sSiteDesc))

    return aPlugins

def __createAvailablePluginsItem(sPluginName, sPluginIdentifier, sPluginDesc):
    aPluginEntry = []
    aPluginEntry.append(sPluginName)
    aPluginEntry.append(sPluginIdentifier)
    aPluginEntry.append(sPluginDesc)
    return aPluginEntry
