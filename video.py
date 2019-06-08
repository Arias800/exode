#! usr/bin/env python
#! -*- coding:utf-8 -*-
import kivy
kivy.require("1.10.1")

#Reste des import kivy
from kivy.core.window import Window
from kivy.properties import StringProperty, BooleanProperty,ObjectProperty, ListProperty
from kivy.modules import inspector
from kivy.config import Config
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.graphics import *
from kivy.metrics import dp, sp
from kivy.app import App

#Uix import
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image, AsyncImage
from kivy.uix.behaviors import ButtonBehavior

#Button import
from kivy.uix.button import Button
from kivymd.button import MDRaisedButton

#Label import
from kivy.uix.label import Label
from kivymd.label import MDLabel

#Reste des import kivy
from kivy.core.window import Window
from kivy.properties import StringProperty, BooleanProperty,ObjectProperty, ListProperty
from kivy.modules import inspector
from kivy.config import Config
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.graphics import *
from kivy.metrics import dp, sp

#Reste des import kivymd
from kivymd.theming import ThemeManager
from kivymd.accordion import MDAccordionSubItem, MDAccordionItem
from kivymd.button import MDRaisedButton
from kivymd.list import TwoLineListItem
from kivymd.textfields import MDTextField

#Autre import
from functools import partial
from tmdb import tmdb
import json

app = App.get_running_app()

sous_menu = {
    "movie": {
    "Populaires": "popular",
    "Mieux notes": "top_rated",
    "En salles": "now_playing",
    "Recemment" : "latest",
    "A venir" : "upcoming" },
    "tv": {
    "Populaires": "popular",
    "Mieux notes" : "top_rated",
    "Diffusees 7 jours" : "on_the_air",
    "Recemment" : "latest",
    "Diffusees ce jour": "airing_today" },
    "player": {
    "Nop": "Nop" },
    "pref": {
    "Nop": "Nop" }
}

menu = {
    "Films": 'movie',
    "Series tv": 'tv',
    "Lecteur": 'player',
    'Parametre': 'pref'}

#pk ça utiliser les nom anglais pour apelle au function
#pouvoir modifier quand y a auras un fichier lang.

#Evite l'erreur :
# __init__ don't take arguments
class BlackHole(object):
    def __init__(self, **kw):
        super(BlackHole, self).__init__()

class VideoAlan(Screen, BlackHole):

    fullscreen = BooleanProperty(False)
    f = ObjectProperty()
    Config.set('kivy', 'exit_on_escape', '0')

    def __init__(self,**kwargs):

        self.picktypes = menu.keys()

        Window.bind(on_dropfile=self.calistir)
        super(VideoAlan,self).__init__(**kwargs)
        self.video.bind(position = self.slider)
        self.keyboard = Window.request_keyboard(self.keyboard_closed,self,"text")
        self.keyboard.bind(on_key_down = self.on_keyboard_down)
        self.keyboard.bind(on_key_up = self.on_keyboard_up)
        self.ses_ayari.value = self.video.volume

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

    def slider(self,ins,val):

        m , s = divmod(self.video.position,60)
        h , m = divmod(m,60)

        self.zaman = str(int(h)) + ":" + str(int(m)) + ":" + str(int(s))

        self.ilerleme.value = float(val)/ float(ins.duration)

        if self.f:

            if self.zaman in list(self.sub_list.keys()):
                self.altyazi.text = self.sub_list[self.zaman]

            if self.zaman in self.sub_list_e:
                self.altyazi.text = ""

    def oynat(self):

        self.video.state = "play"

    def duraklat(self):

        self.video.state = "pause"

    def durdur(self):

        self.video.state = "stop"
        self.ilerleme.value = 0,0

    def calistir(self,window,path):

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
                        self.video.pos_hint = {"x":0,"y":0.1}
                        Window.fullscreen = False
                        self.durumcubugu.pos_hint = {"center_x":0.5,"y":0}
                        Config.set('graphics', 'show_cursor', "1")
                        self.fullscreen = not self.fullscreen
                    else:
                        self.video.pos_hint = {"x":0,"y":0}
                        Window.fullscreen = True
                        self.size_hint = (1,1)
                        Window.size = (1366,768)
                        self.durumcubugu.pos_hint = {"x":0,"top":0}
                        self.fullscreen = not self.fullscreen

            if self.ilerleme.collide_point(*touch.pos):
                self.video.unbind(position = self.slider)
            super(VideoAlan,self).on_touch_down(touch)

        else:
            pass

    def on_touch_up(self,touch):

        if self.video.loaded:

            if self.ilerleme.collide_point(*touch.pos):

                self.video.seek(self.ilerleme.value)
                self.video.bind(position = self.slider)

            self.video.volume = self.ses_ayari.value
            super(VideoAlan,self).on_touch_up(touch)

        else:
            pass

    def ses_gizle(self,dt):
        self.ses.pos_hint = {"left":2,"top":2}

class OpenFolder(Screen, BlackHole):
    pass

def onChange(self, text):
    print(('onchange',  text))
    if text == "movie" or text =="tv":
        sm.clear_widgets(screens=[self])
        sm.add_widget(ListDiscover(name = "discover", menu=text))
        sm.current = 'discover'
    if text == "main":
        sm.current = 'main'
    if text == "pref":
        sm.add_widget(ListParam(name = "param"))
        sm.current = 'param'

class ImageButton(ButtonBehavior, AsyncImage, BlackHole):

    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)

        #icon = AsyncImage(source='https://cdn2.iconfinder.com/data/icons/flat-ui-icons-24-px/24/eye-24-256.png')
        self.background_normal = kwargs['img']
        self.types = kwargs['types']
        self.tmdb = kwargs['tmdbid']
        #print("ratio", self.root.width)

    def on_press(self):

        def on_stop(*l):
            self.animation = Animation(size =(self.size[0] - 10, self.size[1] - 10), t='in_quad', duration=0.5)
            self.animation.start(self)

        self.animation = Animation(size =(self.size[0] + 10, self.size[1] + 10), t='in_quad', duration=0.5)
        self.animation.bind(on_complete=on_stop)
        self.animation.start(self)

        app = App.get_running_app()
        print((self.parent.parent.parent.parent.manager))

        app.root.manager.add_widget(ListInfo(name = "info", types=self.types, tmdbid=self.tmdb))
        app.root.manager.current = "info"

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

        self.ids.cicle_l.add_widget(MyCircle(num = self.vote_average))
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

    def onChange(self):
        app = App.get_running_app()
        if app.root.manager.current == "source":
            print("paseeeeeeeeeee")
            app.root.manager.current = 'info'
            app.root.manager.clear_widgets(screens=[app.root.manager.get_screen('source')])
        elif app.root.manager.current == "info":
            app.root.manager.current = app.root.manager.previous()
            app.root.manager.clear_widgets(screens=[app.root.manager.get_screen('info')])

    def show_source(self):
        app = App.get_running_app()
        app.root.manager.add_widget(ListSource(name = "source", title=self.title))
        app.root.manager.current =  "source"

    pass

class ListSource(Screen, BlackHole):

    grid_id = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ListSource, self).__init__(**kwargs)

        print(kwargs)
        self.ids.bar_label.text = kwargs['title']

        from iplugin import plugin

        _plugin = plugin().getFolder()

        for main in json.loads(_plugin):

            for sub in main.get('source'):
                text = ("%s - %s [%s]") % (main['plugin'], sub['title'] ,sub['qual'])
                self.ids.grid_id.add_widget(Button(text=text, font_size=14, on_press=partial(self.plays, url=sub['url'])))

    def plays(self, *args, **kwargs):
        print((kwargs['url']))
        app = App.get_running_app()

        app.root.manager.get_screen("main").calistir(kwargs['url'],kwargs['url'])
        app.root.manager.current =  "main"

class MyCircle(GridLayout, BlackHole):
    def __init__(self, **kwargs):
        super(MyCircle, self).__init__(**kwargs)

        num = round(float(kwargs['num']) * 36, 2)

        with self.canvas:
            pts = [(Window.width/1.17), (Window.height/2.45), min(80, 80) / 2, 0, num]
            self.line = Line(circle=pts, width=5)

class ListDiscover(Screen, BlackHole):
    #init les object du fichier KV
    grid_l = ObjectProperty(None)
    scroll_l = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.pageNumber = 1
        self.picktypes = menu.keys()
        self.soustypes = sous_menu.get(kwargs['types']).keys()

        super(ListDiscover, self).__init__(**kwargs)

        #grille de poster
        self.grid = self.grid_l

        self.menu = kwargs['menu']
        self.types = kwargs['types']

        print((self.menu, self.types))

        #poster
        self.ids.grid_id.clear_widgets()
        self.add()

    def add(self):
        json = _jsonload(self.types, self.menu,NextPage=self.pageNumber)
        for data in json:
            btn = ImageButton(types=self.menu,
            tmdbid=data['tmdbid'],
            img=data['backdrop_path_780'],
            size=(Window.width , Window.width / 1.777))

            self.ids.grid_id.add_widget(btn)
            label = discover_layout(data)
            self.ids.grid_id.add_widget(label)

    def scroll_direction(self, scroll_y):
        if scroll_y < 0:
            self.pageNumber = self.pageNumber + 1
            self.add()
            self.ids.scroll_id.scroll_y = float(1) / (self.pageNumber)

    def onChange(self, text):
        discover = menu.get(text)
        onChange(self, discover)

    def on_sub_Change(self, text=None):
        menu = sous_menu.get(self.menu).get(text)
        sm.add_widget(ListDiscover(name ="list", types=self.menu, menu=menu))
        sm.current = "list"

class discover_layout(BoxLayout):

    def __init__(self, data, **kwargs):
        super(discover_layout, self).__init__(**kwargs)
        self.title = data['title']
        self.overview = data['overview'][0:140]
        self.release_date = data['release_date']
        self.vote_average = str(data['vote_average'])
    pass

class ListParam(Screen, BlackHole):
    pass

def _jsonload(types, menu,NextPage):

    print(("json", types, menu))
    if menu == 'popular':
        return tmdb().getPopular(NextPage)
    elif menu == "top_rated":
        return tmdb().getRated(NextPage)
    elif menu == "discover":
        return tmdb().getDiscover(types,NextPage)

class ScreenSwitcher(ScreenManager, BlackHole):
     #The screens can be added on the __init__ method like this or on the .kv file
    def __init__(self, **kwargs):
        super(ScreenSwitcher, self).__init__(**kwargs)
        try:
            self.add_widget(ListDiscover(name = "discover", types=types, menu=text))
        except NameError:
            self.add_widget(ListDiscover(name = "discover", types="movie", menu='discover'))
        self.add_widget(VideoAlan(name = "main"))

    #Fonction pour retourner a l'ecran precedent
    def set_previous_screen(self):
        app = App.get_running_app()
        previousName = app.root.manager.previous()
        print((app.root.manager.current))
        if app.root.manager.current == "source":
            app.root.manager.clear_widgets(screens=[app.root.manager.get_screen('source')])
        elif app.root.manager.current == "info":
            app.root.manager.clear_widgets(screens=[app.root.manager.get_screen('info')])
        else: pass
        app.root.manager.current = previousName

class MainScreen(GridLayout,BlackHole):
    manager = ObjectProperty(None)
    nav_drawer = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        print((menu.keys()))
        self.picktypes = menu.keys()
        super(MainScreen, self).__init__(**kwargs)

    def onChange(self, types, menu, text):
        print(('types %s / menu %s / Text %s'% (types, menu, text)))

        if menu == "discover":
            if "discover" in self.manager.screen_names:
                self.manager.clear_widgets(screens=[self.manager.get_screen('discover')])
            self.manager.add_widget(ListDiscover(name = "discover", types=types, menu=text))
            self.manager.current = 'discover'

        if menu == "list":
            if "list" in self.manager.screen_names:
                self.manager.clear_widgets(screens=[self.manager.get_screen('list')])
            self.manager.add_widget(ListDiscover(name ="list", types=types, menu=text))
            self.manager.current = "list"

        if menu == "main":
            self.manager.current = 'main'
        if menu == "pref":
            sm.add_widget(ListParam(name = "param"))
            sm.current = 'param'

        self.ids.nav_layout.toggle_nav_drawer()

class Video(App):

    theme_cls = ThemeManager()

    def build(self):

        Config.set('kivy', 'keyboard_mode', 'system')
        Config.set('graphics', 'width', '480')
        Config.set('graphics', 'height', '800')
        Config.set('graphics', 'resizable', 0)
        Config.set('graphics', 'fullscreen', 0)
        Config.write()

        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Blue'
        self.screen = MainScreen()

        return self.screen

if __name__ in ('__main__', '__android__'):
    Window.clearcolor = (0,0,0,0)
    Video().run()
