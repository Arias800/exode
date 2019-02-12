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

import json

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

    #utilise un json pour le moment
    def getPopular(self,NextPage):
        if NextPage == 2:
            in_file = open("popular2.json","r")
        else:
            in_file = open("popular.json","r")
        self.results = json.load(in_file)
        in_file.close()
        if self.results:
            return self._format_light()
        return

    def getByid(self, type, id):

        print "get id", type , id
        in_file = open("film.json","r")
        results = json.load(in_file)
        in_file.close()
        if results:
            self.results = {"results" : [results]}
            return self._format_light()
        return

    def getRated(self,NextPage):
        in_file = open("rated.json","r")
        self.results = json.load(in_file)
        in_file.close()
        if self.results:
            return self._format_light()
        return

    def getDiscover(self, type="movie"):
        if type == "movie":
            file = "discover_movie.json"
        elif type == "tv":
            file = "discover_tv.json"

        in_file = open(file,"r")
        self.results = json.load(in_file)
        in_file.close()
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

            if 'release_date' in i:
                tub.update({"release_date" : i["release_date"]})
            elif 'first_air_date' in i:
                tub.update({"release_date" : i["first_air_date"]})

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
