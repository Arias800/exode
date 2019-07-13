#-*- coding: utf-8 -*-
import importlib

def getHoster(sHosterFileName, sHosterUrl):
    module = importlib.import_module("plugin.hoster."+sHosterFileName, package=None)
    qual, url = module.getMediaLinkForGuest(sHosterUrl)
    return qual, url

def checkHoster(sHosterUrl):

    #securitee
    if (not sHosterUrl):
        return False

    #Petit nettoyage
    sHosterUrl = sHosterUrl.split('|')[0]

    #Recuperation du host
    try:
        sHostName = sHosterUrl.split('/')[2]
    except:
        sHostName = sHosterUrl

    #Gestion classique
    if ('livestream' in sHostName):
        return getHoster('lien_direct',sHosterUrl)
    if ('gounlimited' in sHostName):
        return getHoster('gounlimited',sHosterUrl)
    if ('xdrive' in sHostName):
        return getHoster('xdrive',sHosterUrl)
    if ('facebook' in sHostName):
        return getHoster('facebook',sHosterUrl)
    if ('cloudcartel' in sHostName):
        return getHoster('cloudcartel',sHosterUrl)
    if (('raptu.com' in sHostName) or ('rapidvideo' in sHostName)):
        return getHoster('raptu',sHosterUrl)
    if ('mixloads' in sHostName):
        return getHoster('mixloads',sHosterUrl)
    if ('vidoza.' in sHostName):
        return getHoster('vidoza',sHosterUrl)
    if (('youtube' in sHostName) or ('youtu.be' in sHostName)):
        return getHoster('youtube',sHosterUrl)
    if ('rutube' in sHostName):
        return getHoster('rutube',sHosterUrl)
    if ('vk.com' in sHostName):
        return getHoster('vk',sHosterUrl)
    if (('vkontakte' in sHostName) or ('vkcom' in sHostName)):
        return getHoster('vk',sHosterUrl)
    if ('megawatch' in sHostName):
        return getHoster('megawatch',sHosterUrl)
    if ('vidto.me' in sHostName):
        return getHoster('vidto',sHosterUrl)
    if (('vidtodo.' in sHostName) or ('vidstodo.' in sHostName)):
        return getHoster('vidtodo',sHosterUrl)
    if ('vidzi' in sHostName):
        return getHoster('vidzi',sHosterUrl)
    if ('vcstream' in sHostName):
        return getHoster('vidcloud',sHosterUrl)
    if ('filetrip' in sHostName):
        return getHoster('filetrip',sHosterUrl)
    if ('uptostream' in sHostName):
        return getHoster('uptostream',sHosterUrl)
    if (('dailymotion' in sHostName) or ('dai.ly' in sHostName)):
        if 'stream' in sHosterUrl:
            return getHoster('lien_direct')
        else:
            return getHoster('dailymotion')
    if ('filez.' in sHostName):
        return getHoster('flashx', sHosterUrl)
    if ('mystream' in sHostName) or ('mstream' in sHostName):
        return getHoster('mystream', sHosterUrl)
    if (('streamingentiercom/videophp?type=speed' in sHosterUrl) or ('speedvideo' in sHostName)):
        return getHoster('speedvideo', sHosterUrl)
    if (('netu' in sHostName) or ('hqq' in sHostName) or ('waaw' in sHostName)):
        return getHoster('netu', sHosterUrl)
    if ('mail.ru' in sHostName):
        return getHoster('mailru', sHosterUrl)
    if ('onevideo' in sHostName):
        return getHoster('onevideo',sHosterUrl)
    if (('picasaweb' in sHostName) or ('googlevideo' in sHostName)):
        return getHoster('googlevideo',sHosterUrl)
    if ('googleusercontent' in sHostName):
        return getHoster('googlevideo',sHosterUrl)
    if ('playreplay' in sHostName):
        return getHoster('playreplay',sHosterUrl)
    if ('flashx' in sHostName):
        return getHoster('flashx',sHosterUrl)
    if (('ok.ru' in sHostName) or ('odnoklassniki' in sHostName)):
        return getHoster('ok_ru',sHosterUrl)
    if ('vimeo.com' in sHostName):
        return getHoster('vimeo',sHosterUrl)
    if (('openload' in sHostName) or ('oload.' in sHostName) or ('oladblock.' in sHostName)):
        return getHoster('openload',sHosterUrl)
    if (('thevideo.' in sHostName) or ('video.tt' in sHostName) or ('vev.io' in sHostName)):
        return getHoster('thevideo_me',sHosterUrl)
    if ('uqload.' in sHostName):
        return getHoster('uqload',sHosterUrl)
    if ('letwatch' in sHostName):
        return getHoster('letwatch',sHosterUrl)
    if ('www.amazon' in sHostName):
        return getHoster('amazon',sHosterUrl)
    if ('filepup' in sHostName):
        return getHoster('filepup',sHosterUrl)
    if ('vimple.ru' in sHostName):
        return getHoster('vimple',sHosterUrl)
    if ('wstream.' in sHostName):
        return getHoster('wstream',sHosterUrl)
    if ('watchvideo' in sHostName):
         return getHoster('watchvideo',sHosterUrl)
    if (('drive.google.com' in sHostName) or ('docs.google.com' in sHostName)):
        return getHoster('googledrive',sHosterUrl)
    if ('vidwatch' in sHostName):
        return getHoster('vidwatch',sHosterUrl)
    if ('up2stream' in sHostName):
        return getHoster('up2stream',sHosterUrl)
    if ('stream.moe' in sHostName):
        return getHoster('streammoe',sHosterUrl)
    if ('tune' in sHostName):
        return getHoster('tune',sHosterUrl)
    if ('sendvid' in sHostName):
        return getHoster('sendvid',sHosterUrl)
    if ('vidup' in sHostName):
        return getHoster('vidup',sHosterUrl)
    if ('vidbull' in sHostName):
        return getHoster('vidbull',sHosterUrl)
    if ('vidlox' in sHostName):
        return getHoster('vidlox',sHosterUrl)
    if ('stagevu' in sHostName):
        return getHoster('stagevu',sHosterUrl)
    if (('movshare' in sHostName) or ('wholecloud' in sHostName)):
        return getHoster('wholecloud',sHosterUrl)
    if ('gorillavid' in sHostName):
        return getHoster('gorillavid',sHosterUrl)
    if ('daclips' in sHostName):
        return getHoster('daclips',sHosterUrl)
    if ('estream' in sHostName) and not ('widestream' in sHostName):
        return getHoster('estream',sHosterUrl)
    if ('hdvid' in sHostName):
        return getHoster('hdvid',sHosterUrl)
    if (('streamango' in sHostName) or ('streamcherry' in sHostName)):
        return getHoster('streamango',sHosterUrl)
    if ('vshare' in sHostName):
        return getHoster('vshare',sHosterUrl)
    if ('giga' in sHostName):
        return getHoster('giga',sHosterUrl)
    if ('vidbom' in sHostName):
        return getHoster('vidbom',sHosterUrl)
    if ('upvid.' in sHostName):
        return getHoster('upvid',sHosterUrl)
    if (('cloudvid' in sHostName ) or ('clipwatching.' in sHostName)):#meme code
        return getHoster('cloudvid',sHosterUrl)
    if ('megadrive' in sHostName):
        return getHoster('megadrive',sHosterUrl)
    if ('downace' in sHostName):
        return getHoster('downace',sHosterUrl)
    if ('clickopen' in sHostName):
        return getHoster('clickopen',sHosterUrl)
    if (('iframe-secured' in sHostName) or ('iframe-secure' in sHostName)):
        return getHoster('iframe_secured',sHosterUrl)
    if ('goo.gl' in sHostName or 'bit.ly' in sHostName or 'streamcrypt.net' in sHostName or 'opsktp.com' in sHosterUrl):
        return getHoster('allow_redirects',sHosterUrl)
    if ('jawcloud' in sHostName):
        return getHoster('jawcloud',sHosterUrl)
    if ('kvid' in sHostName):
        return getHoster('kvid',sHosterUrl)
    if ('soundcloud' in sHostName):
        return getHoster('soundcloud',sHosterUrl)
    if ('mixcloud' in sHostName):
        return getHoster('mixcloud',sHosterUrl)
    if ('ddlfr' in sHostName):
        return getHoster('ddlfr',sHosterUrl)
    if ('pdj' in sHostName):
        return getHoster('pdj',sHosterUrl)
    if ('vidzstore' in sHostName):
        return getHoster('vidzstore',sHosterUrl)
    if ('hd-stream' in sHostName):
        return getHoster('hd_stream',sHosterUrl)
    if ('rapidstream' in sHostName):
        return getHoster('rapidstream',sHosterUrl)
    if ('beeload' in sHostName):
        return getHoster('beeload',sHosterUrl)
    if ('verystream.' in sHostName):
        return getHoster('verystream',sHosterUrl)
    if ('archive.' in sHostName):
        return getHoster('archive',sHosterUrl)
    if ('freshstream' in sHostName):
        return getHoster('freshstream',sHosterUrl)
    if ('jetload' in sHostName):
        return getHoster('jetload',sHosterUrl)

    #Lien telechargeable a convertir en stream
    if ('1fichier' in sHostName):
        return getHoster('onefichier',sHosterUrl)
    if ('uptobox' in sHostName):
        return getHoster('uptobox',sHosterUrl)
    if ('uplea.com' in sHostName):
        return getHoster('uplea',sHosterUrl)
    if ('uploaded' in sHostName or 'ul.to' in sHostName):
        return getHoster('uploaded',sHosterUrl)

    if ('kaydo.ws' in sHostName):
        return getHoster('lien_direct',sHosterUrl)
    if ('fembed' in sHostName):
        return getHoster('lien_direct',sHosterUrl)

    #Si aucun hebergeur connu on teste les liens directs
    if (sHosterUrl[-4:] in '.mp4.avi.flv.m3u8.webm'):
        return getHoster('lien_direct',sHosterUrl)
    #Cas special si parametre apres le lien_direct
    if (sHosterUrl.split('?')[0][-4:] in '.mp4.avi.flv.m3u8.webm'):
        return getHoster('lien_direct',sHosterUrl)

    return False
