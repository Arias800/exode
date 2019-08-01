# -*- coding: utf-8 -*-
# Code de depart par vStream
#https://github.com/Kodi-vStream/venom-xbmc-addons/
# Modif pour app

# "backdrop_sizes": [
#   "w300",
#   "w780",
#   "w1280",
#   "original"
# ],
# "poster_sizes": [
#   "w92",
#   "w154",
#   "w185",
#   "w342",
#   "w500",
#   "w780",
#   "original"
# ],

from kivy.config import Config
from kivymd.dialog import MDInputDialog, MDDialog
from kivymd.toast import toast

import json
import requests

class tmdb:
    URL = "http://api.themoviedb.org/3/"
    CACHE = "special://userdata/addon_data/plugin.video.vstream/video_cache.db"


    def __init__(self, api_key='', debug=False, lang='fr'):

        self.api_key = "92ab39516970ab9d86396866456ec9b6"
        self.debug = debug
        self.lang = lang
        self.poster = 'https://image.tmdb.org/t/p/w342'
        self.fanart = 'https://image.tmdb.org/t/p/original'
        self.fanart_780 = 'https://image.tmdb.org/t/p/w780'
        self.request_token = ''
        self.session_id = ''
        self.username = ''
        self.id = ''

    def connect(self):
            dialog = MDDialog(
                title='Connexion', size_hint=(.8, .3), text_button_ok='Yes',
                text="Votre navigateur va s'ouvrir pour autoriser la connexion",
                text_button_cancel='Cancel',
                events_callback=self.getToken)
            dialog.open()

    def getToken(self, *args):
        if args[0] == 'Yes':
            import webbrowser

            url = 'https://api.themoviedb.org/3/authentication/token/new?api_key=%s' % (self.api_key)

            req = requests.get(url)
            results = req.json()
            if results['request_token']:
                self.request_token = results['request_token']
                url = 'https://www.themoviedb.org/authenticate/'+self.request_token
                webbrowser.open(url)

                dialog = MDDialog(
                title='Connexion', size_hint=(.8, .3), text_button_ok='Yes',
                text="Ete vous connecter ?",
                text_button_cancel='Cancel',
                events_callback=self.callback)
                dialog.open()

    def callback(self, *args):
        if args[0] == 'Yes':
            data = {"request_token": self.request_token}
            url = 'https://api.themoviedb.org/3/authentication/session/new?api_key=%s' % (self.api_key)
            req = requests.post(url, data = data)
            results = req.json()
            #sauv results['session_id']
            if results['session_id']:
                self.session_id = results['session_id']

                url = 'https://api.themoviedb.org/3/account?api_key=%s&session_id=%s' % (self.api_key, self.session_id)
                req = requests.get(url)
                results = req.json()
                if results['username']:
                    self.username = results['username']
                    self.id = results['id']
                    toast('Connexion Reussis %s' % self.username)
                    #print(results)
                    #sauv config
                    Config.set('user', 'tmdb_id', self.id)
                    Config.set('user', 'tmdb_username', self.username)
                    Config.set('user', 'tmdb_session_id', self.session_id)
                    Config.write()
                    return




    #utilise un json pour le moment
    def getPopular(self,NextPage):
        if NextPage == 2:
            in_file = open("popular2.json","r",encoding="utf-8")
        else:
            in_file = open("popular.json","r",encoding="utf-8")
        self.results = json.load(in_file)
        in_file.close()
        if self.results:
            return self._format_light()
        return

    def getByid(self, types, id):

        print(("get id", types , id))
        #news code
        rqst = requests.get('https://api.themoviedb.org/3/%s/%s?api_key=%s&language=fr-FR' % (types, id, self.api_key))
        results = rqst.json()

        #in_file = open("film.json","r",encoding="utf-8")
        #results = json.load(in_file)
        #in_file.close()
        if results:
            self.results = {"results" : [results]}
            return self._format_light()
        return

    def getTmdb(self, types, menu, page):
        #types movie/tv
        #menu discover, top_rated
        tmdb_id = Config.get('user', 'tmdb_id')
        tmdb_session_id = Config.get('user', 'tmdb_session_id')

        #touts faire avec discovers et c'est tris
        #popularity.asc, popularity.desc, release_date.asc, release_date.desc, revenue.asc, revenue.desc, 
        #primary_release_date.asc, primary_release_date.desc, original_title.asc, original_title.desc, 
        # vote_average.asc, vote_average.desc, vote_count.asc, vote_count.desc
        #default: popularity.desc
        #tendance 
        #Media Type :  all, movie, tv, person
        #time window : day, week
        #/trending/{media_type}/{time_window}
        
        if menu == "trending":
            #url = "discover/"+types
            url = "trending/"+types+"/week"
            rqst = requests.get('https://api.themoviedb.org/3/%s?api_key=%s&language=fr-FR&page=%s' % (url, self.api_key, page))
        elif menu == "favorite" or menu == "rated" or menu == "watchlist":
            url = "account/%s/%s/%s" % (tmdb_id, menu, types)
            rqst = requests.get('https://api.themoviedb.org/3/%s?api_key=%s&session_id=%s&language=fr-FR&page=%s' % (url, self.api_key, tmdb_session_id, page))
        else :
            url = types+"/"+menu
            rqst = requests.get('https://api.themoviedb.org/3/%s?api_key=%s&language=fr-FR&page=%s' % (url, self.api_key, page))

        
        self.results = rqst.json()
        

        if self.results:
            #self.results = {"results" : [results]}
            return self._format_light()
        return

    def getRated(self,NextPage):
        in_file = open("rated.json","r",encoding="utf-8")
        self.results = json.load(in_file)
        in_file.close()
        if self.results:
            return self._format_light()
        return

    def getDiscover(self, types,menu, NextPage):
        #Ca ouvre popular2 juste pour pas avoir un autre json pour rien
        #types movie / tv
        #menu popular, top_rated
        rqst = requests.get('https://api.themoviedb.org/3/%s/%s?api_key=%s&language=fr-FR' % (types, menu, self.api_key))
        self.results = rqst.json()


        if self.results:
            return self._format_light()
        return

    #format fiche poster
    def _format_light(self):

        videos = []

        for i in self.results.get("results", []):

            tub = {'tmdbid' : i["id"],
            "vote_average" : str(i["vote_average"]) }

            if 'poster_path' in i and i.get('poster_path'):
                tub.update({"poster_path" : self.poster+i["poster_path"]})
            else :
                tub.update({"poster_path" : "http://gowatchit.com/assets/movie_imgs/noposter.png"})

            if 'backdrop_path' in i and i.get('backdrop_path'):
                tub.update({"backdrop_path" : self.fanart+i["backdrop_path"]})
                tub.update({"backdrop_path_780" : self.fanart_780+i["backdrop_path"]})
            else :
                tub.update({"backdrop_path" : "http://gowatchit.com/assets/movie_imgs/noposter.png"})
                tub.update({"backdrop_path_780" : "http://gowatchit.com/assets/movie_imgs/noposter.png"})

            if 'title' in i:
                tub.update({"title" : i["title"]})
            elif "name" in i:
                tub.update({"title" : i["name"]})
            else:
                tub.update({"title" : "NC"})

            if 'tagline' in i:
                tub.update({"tagline" : i["tagline"]})

            if 'release_date' in i:
                tub.update({"release_date" : i["release_date"]})
                tub.update({"year" : i["release_date"][0:4]})
            elif 'first_air_date' in i:
                tub.update({"release_date" : i["first_air_date"]})
                tub.update({"year" : i["first_air_date"][0:4]})

            if 'overview' in i:
                tub.update({"overview" : i["overview"]})

            if 'genres' in i:
                #genres = ""
                #affiche 1 seul
                for genre in i['genres']:
                    #genres = genre['name'] + ' '
                    genres = genre['name']
                tub.update({"genres" : genres})

            videos.append(tub)

        return videos

    #format fiche description
    def _format(self, results):

        result = []
        for i in self.results.get("results", []):
            videos.append({'id' : i["id"],
            "vote_average" : i["vote_average"],
            "title" : i["title"],
            "poster_path" : self.poster+i["poster_path"],
            "backdrop_path" : self.fanart+i["backdrop_path"],
            "release_date" : i["release_date"] })
