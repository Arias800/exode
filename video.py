#! usr/bin/env python
#! -*- coding:utf-8 -*-

#Au cas ou la personne ait mit la lib dans le meme dossier au lieu de l'installer.
import sys
try:
    sys.path.append('kivymd')
except:
    pass

import kivy
kivy.require("1.10.1")

#Reste des import kivy
from kivy.core.window import Window
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.config import Config
from kivy.clock import Clock
from kivy.graphics import *
from kivy.metrics import sp
from kivy.app import App

#Uix import
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

#Button import
from kivy.uix.button import Button

#Label import
from kivy.uix.label import Label

#Reste des import kivymd
from kivymd.theming import ThemeManager
from kivymd.bottomsheet import MDListBottomSheet
from kivymd.toast import toast
from kivymd.dialog import MDDialog
from kivymd.elevation import RectangularElevationBehavior, CircularElevationBehavior
from kivymd.cards import MDCardPost

#Custom Lib import
from lib.comaddon import EXlog, ImageButton, BlackHole
from lib.utils import CleanName
from tmdb import tmdb

#Autre import
from functools import partial
import json, importlib, re, os

sous_menu = {
    "trending": {
    "Quotidien": "day",
    "Hebdomadaire": "week" },
    "movie": {
    "Populaires": "popular",
    "Mieux notes": "top_rated",
    "En salles": "now_playing",
    "A venir" : "upcoming" },
    "tv": {
    "Populaires": "popular",
    "Mieux notes" : "top_rated",
    "Diffusees 7 jours" : "on_the_air",
    "Diffusees ce jour": "airing_today" },
    "player": {
    "Nop": "Nop" },
    "pref": {
    "Nop": "Nop" }
}

menu = {
    "Tendance": 'trending',
    "Films": 'movie',
    "Series tv": 'tv',
    "Lecteur": 'player',
    'Parametre': 'pref'}

#Commande pour lancer l'application sous linux: 
#   KIVY_VIDEO=ffpyplayer python3 video.py

#pk ça utiliser les nom anglais pour apelle au function
#pouvoir modifier quand y a auras un fichier lang.

#test lang
in_file = open("lang.json","r",encoding="utf-8")
lang = json.load(in_file)

class VideoAlan(Screen, BlackHole):
    fullscreen = BooleanProperty(False)
    f = ObjectProperty()
    Config.get('kivy', 'exit_on_escape')

    def __init__(self,**kwargs):
        self.picktypes = menu.keys()
        super(VideoAlan,self).__init__(**kwargs)
        Window.bind(on_dropfile = self.calistir)
        Window.bind(mouse_pos = self.on_motion)
        self.video.bind(position = self.slider)
        self.keyboard = Window.request_keyboard(self.keyboard_closed,self,"text")
        self.keyboard.bind(on_key_down = self.on_keyboard_down)
        self.keyboard.bind(on_key_up = self.on_keyboard_up)
        self.ses_ayari.value = self.video.volume
        self.duration = str(self.video.duration)
        self.position = str(self.video.position)

    def keyboard_closed(self):
        self.keyboard.unbind(on_key_down = self.on_keyboard_down)
        self.keyboard = None

    def on_keyboard_down(self,keyboard,keycode,text,modifiers):
        if keycode[1] == "right":
            self.video.unbind(position = self.slider)
            self.video.seek(float(self.video.position)/float(self.video.duration) + 5.0/self.video.duration)

        elif keycode[1] == "left":
            self.video.unbind(position = self.slider)
            self.video.seek(float(self.video.position)/float(self.video.duration) - 5.0/self.video.duration)

            if float(self.video.position)/float(self.video.duration) < 5.0/self.video.duration:
                self.video.seek(0)

        elif keycode[1] == "spacebar":
            if self.video.state == "play":
                self.video.state = "pause"
            elif self.video.state == "pause" or  self.video.state == "stop":
                self.video.state = "play"

        elif keycode[1] == "enter":
            if self.fullscreen:
                self.video.pos_hint = {"x":0,"y":0.1}
                Window.fullscreen = False
                self.durumcubugu.pos_hint = {"center_x":0.5,"y":0}
                self.fullscreen = not self.fullscreen
            else:
                self.video.pos_hint = {"x":0,"y":0}
                Window.fullscreen = True
                self.size_hint = (1,1)
                Window.size = (1366,768)
                self.durumcubugu.pos_hint = {"center_x":0.5,"top":0}
                self.fullscreen = not self.fullscreen

        elif keycode[1] == "escape":
            if self.fullscreen:
                self.video.pos_hint = {"x":0,"y":0.1}
                Window.fullscreen = False
                self.durumcubugu.pos_hint = {"x":0,"y":0}
                self.fullscreen = not self.fullscreen
            else:
                pass

        if len(modifiers) > 0:
            if modifiers[-1] == "ctrl" and keycode[1] == "up":
                self.durumcubugu.pos_hint = {"center_x":0.5,"y":0}
            elif modifiers[-1] == "ctrl" and keycode[1] == "down":
                self.durumcubugu.pos_hint = {"center_x":0.5,"top":0}
            elif modifiers[-1] == "alt" and keycode[1] == "up":
                self.menu.pos_hint = {"x":0,"y":1}
            elif modifiers[-1] == "alt" and keycode[1] == "down":
                self.menu.pos_hint = {"x":0,"top":1}

    def on_keyboard_up(self,keyboard,keycode):
        self.video.bind(position = self.slider)

    #slider et position en temp reel
    #affichage 2.3.42 a revoire pour 2.30.42 -> Normalement corriger avec la fonction format
    #divmod est inutile car meme resultat avec les operation de base

    def slider(self,ins,val):
        m , s = (self.video.position // 60, self.video.position % 60)
        h , m = (m // 60, m % 60)

        dur_m , dur_s = (self.video.duration // 60, self.video.duration % 60)
        dur_h , dur_m = (dur_m // 60, dur_m % 60)

        self.position  = str(int(h)) + ":" + format(int(m), '02d') + ":" + format(int(s), '02d')
        self.duration = str(int(dur_h)) + ":" + format(int(dur_m), '02d') + ":" + format(int(dur_s), '02d')
        
        self.progression.value = float(val)/ float(ins.duration)

        if self.f:
            if self.position in list(self.sub_list.keys()):
                self.altyazi.text = self.sub_list[self.position]
            if self.position in self.sub_list_e:
                self.altyazi.text = ""

    def Play(self):
        self.video.state = "play"

    def Pause(self):
        self.video.state = "pause"

    def Stop(self):
        self.video.state = "stop"
        self.progression.value = 0,0

    def volume(self):
        toast(str(round(self.ses_ayari.value, 2)))

    def seek(self):
        toast(str(round(self.progression.value, 2)))

    def calistir(self,path):
        self.sub_list = {}
        self.sub_list_e = []
        self.altyazi.text = ""

        self.video.size_hint = (1,1)

        if isinstance(path, list):
            if len(path) > 0:
                path = path[0]
            else:
                return

        if path.endswith(".srt"):
            for i in self.f:
                self.sub_list[str(i.start.hours) + ":" + str(i.start.minutes) +":" + str(i.start.seconds)] = "[b]" + (i.text.replace("<","[")).replace(">","]") + "[/b]"

            for i in self.f:
                if str(i.end.hours) + ":" + str(i.end.minutes) +":" + str(i.end.seconds) not in self.sub_list:
                    self.sub_list_e.append(str(i.end.hours) + ":" + str(i.end.minutes) +":" + str(i.end.seconds))
        else:
            self.video.source = path
            print('lecture')
        self.video.state == "play"
            # self.triggerUpdate = Clock.create_trigger(self.checkUpdate)
            # Clock.schedule_interval(self.triggerUpdate, 0.01)

    def checkUpdate(self, *args):
        self.position = str(self.video.position)
        self.duration = str(self.video.duration)

    def on_touch_down(self,touch):
        if "button" in touch.profile:
            if touch.button == "scrolldown" and self.durumcubugu.collide_point(*touch.pos) == False and self.ses.pos_hint != {"right":0.9,"top":0.9}:
                self.ses.pos_hint = {"right":0.9,"top":0.9}
                Clock.schedule_once(self.ses_gizle, 5)

            if touch.button == "scrollup" and self.durumcubugu.collide_point(*touch.pos) == False and self.ses.pos_hint != {"right":0.9,"top":0.9}:
                self.ses.pos_hint = {"right":0.9,"top":0.9}
                Clock.schedule_once(self.ses_gizle, 5)

            if touch.button == "scrolldown":
                self.video.volume += 0.05
                if self.durumcubugu.collide_point(*touch.pos) == False:
                    self.ses_ayari.value += 0.05
                if self.video.volume > 2:
                    self.video.volume = 2
                if self.ses_ayari.value > 2:
                    self.ses_ayari.value = 2

            if touch.button == "scrollup":
                self.video.volume -= 0.05
                if self.durumcubugu.collide_point(*touch.pos) == False:
                    self.ses_ayari.value -= 0.05
                if self.video.volume < 0:
                    self.video.volume = 0
                if self.ses_ayari.value < 0:
                    self.ses_ayari.value = 0

            if self.video.collide_point(*touch.pos):
                if touch.is_double_tap:
                    if self.fullscreen:
                        self.hide_widget(False)
                        self.video.pos_hint = {"x":0,"y":0.1}
                        Window.fullscreen = False
                        self.durumcubugu.pos_hint = {"center_x":0.5,"y":0}
                        self.fullscreen = not self.fullscreen
                    else:
                        self.video.pos_hint = {"x":0,"y":0}
                        Window.fullscreen = True
                        self.size_hint = (1,1)
                        Window.size = (1366,768)
                        self.hide_widget(True)
                        self.fullscreen = not self.fullscreen

            if self.progression.collide_point(*touch.pos):
                self.video.unbind(position = self.slider)
            super(VideoAlan,self).on_touch_down(touch)

        else:
            pass

    def on_touch_up(self,touch):
        if self.video.loaded:
            if self.progression.collide_point(*touch.pos):

                self.video.seek(self.progression.value)
                self.video.bind(position = self.slider)

            self.video.volume = self.ses_ayari.value
            super(VideoAlan,self).on_touch_up(touch)

        else:
            pass

    def ses_gizle(self,dt):
        self.ses.pos_hint = {"left":2,"top":2}

    def hide_widget(self, hide, *largs):
        app = App.get_running_app()
        #Conserve la couleurs d'origine
        try:
            trueColor = self.defaultColor
        except AttributeError:
            self.defaultColor = Window.clearcolor

        #Simule le fait de cacher les widget pendant le plein ecran
        #alors que je les mets juste en dehors de l'écran
        if hide:
            #Change la couleur du fond pour du noir plus agreable pour le visionage
            Window.clearcolor = (0, 0, 0, 0)
            self.durumcubugu.pos_hint = {"x":-1,"y":-1}
            self.ses.pos_hint = {"x":-1,"y":-1}
            self.progression.pos_hint = {"x":-50000,"y":-50000}
            self.menu.pos_hint = {"x":-1,"y":-1} 
            app.root.toolbar.pos_hint = {"x":-1,"y":-1}  

        else:
            #Retour a la couleurs choisit par l'utilisateur
            Window.clearcolor = self.defaultColor
            self.durumcubugu.pos_hint = {"center_x":0.5,"y":0}
            self.ses.pos_hint = {"right":0.9,"top":0.9}
            self.progression.pos_hint = {"center_x":0.5,"y":0}
            self.menu.pos_hint = {"x":0,"top":1}
            app.root.toolbar.pos_hint = {"x":0,"y":0} 

    def on_motion(self, reste, pos):
        app = App.get_running_app()
        if app.root.manager.current == "player" and self.video.state == "play":
            self.hide_widget(False)
            Clock.schedule_once(partial(self.hide_widget, True), 5)
        elif self.video.state == "pause" or self.video.state == "stop":
            self.hide_widget(False)
        elif app.root.manager.current != "player":
            self.hide_widget(False)
        else:
            return                       

class ListDiscover(Screen, BlackHole):
    #init les object du fichier KV
    grid_l = ObjectProperty(None)
    scroll_l = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.pageNumber = 1
        self.picktypes = menu.keys()
        #self.soustypes = sous_menu.get(kwargs['types']).keys()

        super(ListDiscover, self).__init__(**kwargs)

        #grille de poster
        #self.grid = self.grid_l
        self.menu = kwargs['menu']
        self.types = kwargs['types']

        app = App.get_running_app()

        self.ids.discover_label.text = app._(kwargs['menu'])


        EXlog((self.menu, self.types))

        #poster
        self.ids.grid_id.clear_widgets()
        self.add()

    def add(self):
        json = _jsonload(self.types, self.menu,NextPage=self.pageNumber)

        for data in json:
            btn = ImageButton(types=self.types,
            tmdbid=data['tmdbid'],
            img=data['backdrop_path'],
            size=(Window.width , Window.width / 1.777),
            functionName = ListInfo)

            self.ids.grid_id.add_widget(btn)
            label = discover_layout(data)
            self.ids.grid_id.add_widget(label)

    def scroll_direction(self, scroll_y):
        if scroll_y < 0:
            self.pageNumber = self.pageNumber + 1
            self.add()
            self.ids.scroll_id.scroll_y = float(1) / (self.pageNumber)

    #changement de vue grid or list
    def show_view(self):
        self.ids.grid_id.clear_widgets()
        self.ids.grid_id.cols = 3
        self.add()

class discover_layout(BoxLayout):
    bar_l = ObjectProperty(None)

    def __init__(self, data, **kwargs):
        super(discover_layout, self).__init__(**kwargs)

        self.title = data['title']
        self.overview = data['overview'][0:140]
        self.release_date = data['release_date']
        self.vote_average = str(data['vote_average'])

    pass

#screen information
class ListInfo(Screen, BlackHole):

    grid_l = ObjectProperty(None)
    scroll_l = ObjectProperty(None)
    circle_l = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ListInfo, self).__init__(**kwargs)

        json = tmdb().getByid(kwargs['types'], kwargs['tmdbid'])

        #introduit le dict dans self
        #a revoir c'est moche
        for value in json[0]:
            setattr(self, value, json[0][value])

        #self.ids.cicle_l.add_widget(MyCircle(num = self.vote_average))
        
        self.ids.list_label.text = self.title

    def show_synopsis(self):
        self.synopsis = Label(text=self.overview,
        bold = True,
        text_size=(self.width,self.height),
        font_size="20sp",
        pos_hint={'center_x': 0.5, 'center_y': .50},
        size_hint_y=None,
        size = self.size,
        halign="center",
        valign = "bottom")

        self.add_widget(self.synopsis)
        self.synopsis.bind(size=self.setting_function)

    #setting_function et update_rect sont utilise pour bloquer la synopsis en bas de l'ecran
    def setting_function(self, *args):
        """FUNCTION TO UPDATE THE LABEL TO ADJUST ITSELF ACCORDING TO SCREEN SIZE CHANGES"""
        self.synopsis.pos_hint = {'center_x': 0.5, 'center_y': .50}
        self.synopsis.text_size=self.size

    def update_rect(self, *args):
        """FUNCTION TO UPDATE THE RECATANGLE OF CANVAS TO FIT THE WHOLE SCREEN OF MAINSCREEN ALWAYS"""
        self.rect.pos = self.pos
        self.rect.size = self.size

    def show_source(self):
        app.root.manager.add_widget(ListSource(name = "source", title=self.title))
        app.root.manager.current =  "source"

    def show_bottom(self):
        self.ids.spinner.active = True

        from iplugin import plugin

        print(self.title, 'getfoldr')
        print(CleanName(self.title), 'getfoldr')

        _plugin = plugin().getFolder(CleanName(self.title.replace(' ','+'))).replace('\\','').replace('["','').replace('"]','')
        sv = ScrollView()
        bs = MDListBottomSheet()
        #sv.add_widget(bs)

        #json valider pas besoin de retest
        #main = re.findall('plugin": "(.+?)".+?{"title": "(.+?)", "url": "(.+?)", "qual": "(.+?)"}',str(_plugin))
        #for sub in main:
        #    text = ("%s - %s [%s]") % (sub[0], sub[1] ,sub[3])
        #    bs.add_item(text, lambda x, url=sub[2], title=sub[1]: self.plays(url=url, title=title))            
        #bs.open()

        for main in json.loads(_plugin):

            if main.get('source'):
                for sub in main.get('source'):
                    text = ("%s - %s [%s]") % (main['plugin'], sub['title'] ,sub['qual'])
                    bs.add_item(text, lambda x, url=sub['url'], title=sub['title']: self.plays(url=url, title=title))
            else:
                text = ("%s - Aucune réponse") % (main['plugin'])
                bs.add_item(text, lambda x:x)

        bs.open()

        #loading stop en time mais a voir pour le mettre en vrais temp de chargement
        Clock.schedule_once(self.spinner_stop, 8)

    def spinner_stop(self, *args):
        self.ids.spinner.active = False

    def plays(self, *args, **kwargs):
        app = App.get_running_app()
        EXlog (kwargs)
        #gstreamer n'accepter pas les m3u8 ni les connections securiser https
        #ffpyplayer les support uniquement si il est compiler manuellement

        url = kwargs['url'].replace('https', 'http') 

        if app.root.manager.current == "discover":
            app.root.manager.clear_widgets(screens=[app.root.manager.get_screen('discover')])
        app.root.manager.add_widget(VideoAlan(name = "player"))
        app.root.manager.get_screen("player").calistir(url)
        app.root.manager.current =  "player"

class ListSource(Screen, BlackHole):

    grid_id = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ListSource, self).__init__(**kwargs)

        EXlog(kwargs)
        self.ids.bar_label.text = kwargs['title']

        from iplugin import getAllPlugins

        _plugin = getAllPlugins()

        for main in _plugin:
            text = ("%s - %s \n %s") % (main[0] , main[1] ,  main[2])
            self.ids.grid_id.add_widget(Button(text=text, font_size=14, on_press=partial(self.plays, sName=main[1])))

    def plays(self, *args, **kwargs):
        module = importlib.import_module("plugin."+str(kwargs['sName']), package=None)
        content = module.ShowPlugin()

        if app.root.manager.current == "discover":
            app.root.manager.clear_widgets(screens=[app.root.manager.get_screen('source')])

class MyCircle(GridLayout, BlackHole):
    def __init__(self, **kwargs):
        super(MyCircle, self).__init__(**kwargs)

        num = round(float(kwargs['num']) * 36, 2)

        with self.canvas:
            pts = [(Window.width/1.17), (Window.height/2.45), min(80, 80) / 2, 0, num]
            self.line = Line(circle=pts, width=5)

class ListParam(Screen, BlackHole):

    grid_id = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ListParam, self).__init__(**kwargs)

        from kivy.uix.settings import Settings, SettingsWithSpinner, SettingsPanel
        from kivy.config import ConfigParser

        print("parammmmmmmm")

        #json param
        #graphics
        conf_graphics = [
        #{"type": "title", "title": "Windows"},
        {"type": "bool", "title": "Fullscreen", "desc": "Set the window in windowed or fullscreen", "section": "graphics", "key": "fullscreen"}
        ]

        #theme
        conf_theme = [
        {"type": "options", "title": "Style", "desc": "Style des fenêtres", "section": "theme", "key": "Style", 'options': ['Light', 'Dark']},
        {"type": "options", "title": "Palette", "desc": "Couleurs des fenêtres", "section": "theme", "key": "Palette", 'options': 
        ["Red", "Pink", "Purple", "DeepPurple", "Indigo", "Blue", "LightBlue", "Cyan", "Teal", "Green", "LightGreen", "Lime", "Yellow", "Amber",
        "Orange", "DeepOrange", "Brown", "Gray", "BlueGray"]}
        ]

        config = ConfigParser()
        config.read('config.ini')

        s = Settings()
        #s.add_json_panel('My custom panel', config, 'settings_custom.json')
        #s.add_json_panel('Another panel', config, 'settings_test2.json')
        s.add_json_panel('Graphics', config, data=json.dumps(conf_graphics))
        s.add_json_panel('Theme', config, data=json.dumps(conf_theme))
        self.ids.grid_id.add_widget(s)

class MyRectangularBox(BoxLayout, RectangularElevationBehavior):
    pass

class MyCircularBox(BoxLayout, CircularElevationBehavior):
    pass

class ListTmdb(Screen, BlackHole):

    grid_id = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ListTmdb, self).__init__(**kwargs)

    def connect(self):
        dialog = MDDialog(
            title='Connexion', size_hint=(.8, .3), text_button_ok='Yes',
            text="Votre navigateur va s'ouvrir pour autoriser la connexion",
            text_button_cancel='Cancel',
            events_callback=self.callback)
        dialog.open()

    def callback(self, *args):
        if args[0] == 'Yes':
            tmdb_account = tmdb().getToken()
            print(tmdb_account)

    def setconnect(self):
        pass
        
    def deco(self):
        pass

        #self.ids.grid_id.add_widget(s)

class OpenFolder(Screen, BlackHole):
    def __init__(self, **kwargs):
        super(OpenFolder, self).__init__(**kwargs)

    def openPlayer(self,path):
        app = App.get_running_app()
        if app.root.manager.current == "discover":
            app.root.manager.clear_widgets(screens=[app.root.manager.get_screen('discover')])
        app.root.manager.add_widget(VideoAlan(name = "player"))
        app.root.manager.get_screen("player").calistir(path)
        app.root.manager.current =  "player"

def _jsonload(types, menu,NextPage):

    EXlog(("json", types, menu))
    return tmdb().getTmdb(types, menu, NextPage)

class ScreenSwitcher(ScreenManager, BlackHole):
     #The screens can be added on the __init__ method like this or on the .kv file
    def __init__(self, **kwargs):
        super(ScreenSwitcher, self).__init__(**kwargs)
        try:
            self.add_widget(ListDiscover(name = "discover", types=types, menu=text))
        except NameError:
            self.add_widget(ListDiscover(name = "discover", types="movie", menu='trending'))

    #Fonction pour retourner a l'ecran precedent
    def set_previous_screen(self):
        app = App.get_running_app()
        previousName = app.root.manager.previous()

        if app.root.manager.current == "source":
            app.root.manager.clear_widgets(screens=[app.root.manager.get_screen('source')])
        elif app.root.manager.current == "info":
            app.root.manager.clear_widgets(screens=[app.root.manager.get_screen('info')])
        else: pass
        app.root.manager.current = previousName

class MainScreen(GridLayout,BlackHole):
    manager = ObjectProperty(None)
    toolbar = ObjectProperty(None)
    nav_drawer = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        EXlog(menu.keys())
        self.picktypes = menu.keys()
        super(MainScreen, self).__init__(**kwargs)
        #connecter ou pas
        self.tmdb_username = Config.get('user', 'tmdb_username')
        print(self.tmdb_username)

    def onChange(self, types, menu, text):
        EXlog('types %s / menu %s / Text %s'% (types, menu, text))

        if menu == "discover":
            if "discover" in self.manager.screen_names:
                self.manager.clear_widgets(screens=[self.manager.get_screen('discover')])
            self.manager.add_widget(ListDiscover(name = "discover", types=types, menu=text))
            self.manager.current = 'discover'

        if menu == "info":
            if "info" in self.manager.screen_names:
                self.manager.clear_widgets(screens=[self.manager.get_screen('info')])
            self.manager.add_widget(ListInfo(name = "info"))
            self.manager.current = 'info'

        if menu == "list":
            if "list" in self.manager.screen_names:
                self.manager.clear_widgets(screens=[self.manager.get_screen('list')])
            self.manager.add_widget(ListDiscover(name ="list", types=types, menu=text))
            self.manager.current = "list"

        if menu == "player":
            if "player" in self.manager.screen_names:
                self.manager.clear_widgets(screens=[self.manager.get_screen('player')])
            self.manager.add_widget(VideoAlan(name = "player", path=url))
            self.manager.current = "player"
            
        if menu == "param":
            if "param" in self.manager.screen_names:
                self.manager.clear_widgets(screens=[self.manager.get_screen('param')])
            self.manager.add_widget(ListParam(name = "param"))
            self.manager.current = 'param'

        if menu == "tmdb":
            if text == 'account':
                return tmdb().connect()
            if text == 'decount':
                return tmdb().deconnect()

            if self.tmdb_username:
                if "list" in self.manager.screen_names:
                    self.manager.clear_widgets(screens=[self.manager.get_screen('list')])
                self.manager.add_widget(ListDiscover(name = "list", types=types, menu=text))
                self.manager.current = 'list'
            else: return tmdb().connect()

        self.ids.nav_layout.toggle_nav_drawer()

    def onRoot(self):
        self.manager.add_widget(OpenFolder(name = "folder"))
        self.manager.current = 'folder'

class Video(App):

    theme_cls = ThemeManager()

    def build(self):

        Config.read('config.ini')
        Config.get('kivy', 'keyboard_mode')
        Config.get('graphics', 'width')
        Config.get('graphics', 'height')
        Config.get('graphics', 'resizable')
        Config.get('graphics', 'fullscreen')

        self.theme_cls.theme_style = Config.get('theme', 'style')
        self.theme_cls.primary_palette = Config.get('theme', 'palette')
        Config.write()

        #self.theme_cls.theme_style = 'Light'
        #self.theme_cls.primary_palette = 'Blue'
        self.screen = MainScreen()

        #Permets de definir le nom de la fenetre
        self.title = 'eXode'

        return self.screen

    def _(self, text):
        #print(lang[text]['fr'], 'iciiiiiiiiii')
        if lang[text]['fr']:
            return str(lang[text]['fr'])
        else : return 'Erreur'


if __name__ in ('__main__', '__android__'):
    Video().run()
