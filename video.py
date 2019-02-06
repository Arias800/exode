#! usr/bin/env python
#! -*- coding:utf-8 -*-
import kivy
kivy.require("1.9.1")

from kivy.app import App
from functools import partial
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty, BooleanProperty,ObjectProperty, ListProperty
from kivy.uix.label import Label
from kivy.modules import inspector
from kivy.config import Config
from kivy.clock import Clock
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image, AsyncImage
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.graphics import *
from kivy.metrics import dp, sp
from tmdb import tmdb

import json

#import pysrt

sm = ScreenManager()

class VideoAlan(Screen):

    fullscreen = BooleanProperty(False)
    f = ObjectProperty()
    Config.set('kivy', 'exit_on_escape', '0')

    def __init__(self,**kwargs):

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

            if self.zaman in self.sub_list.keys():
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
                path = path[0].encode("utf-8")
            else:
                return

        if path.decode("utf-8").endswith(".srt"):
            #self.f = pysrt.open(path,encoding='iso-8859-9')

            for i in self.f:
                self.sub_list[str(i.start.hours) + ":" + str(i.start.minutes) +":" + str(i.start.seconds)] = "[b]" + (i.text.replace("<","[")).replace(">","]") + "[/b]"

            for i in self.f:
                if str(i.end.hours) + ":" + str(i.end.minutes) +":" + str(i.end.seconds) not in self.sub_list:
                    self.sub_list_e.append(str(i.end.hours) + ":" + str(i.end.minutes) +":" + str(i.end.seconds))
        else:
            self.video.source = path.decode("utf-8")

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

class OpenFolder(Screen):
    pass

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
    "Diffusees ce jour": "airing_today" }
}

menu = {
    "Films": 'movie',
    "Series tv": 'tv',
    "test2": 'Autre',
    'Parametre': 'pref'}

#pk ça utiliser les nom anglais pour apelle au function
#pouvoir modifier quand y a auras un fichier lang.

class ListFolder(Screen):
    #a = StringProperty('a')
    #b = StringProperty('b')
    #init les object du fichier KV
    grid_l = ObjectProperty(None)
    scroll_l = ObjectProperty(None)

    #pickType = ['Movies','Series','Autres']

    #sousType = {'pop' : 'populaire', 'note' : 'grande note', 'pro' : 'prochainement'}

    def __init__(self, **kwargs):
        self.pageNumber = 1
        self.pickType = menu.viewkeys()
        self.sousType = sous_menu.get(kwargs['type']).viewkeys()

        #self.sousType = ['Populaire','Mieux notes','Prochainement', 'latest']

        super(ListFolder, self).__init__(**kwargs)

        #grille de poster
        self.grid = self.grid_l

        self.menu = kwargs['menu']
        self.type = kwargs['type']

        print self.menu
        #poster
        self.on_sub_Change()
        #self.add_widget(Button(text="NextPage", on_press=lambda a:self.on_change_Page(text='Populaires')))

        #scroll.add_widget(grid)
        #scroll.add_widget(grid)

        #self.root_widget = DataLayout(orientation='vertical')
        #self.ids.box_id.add_widget(self.root_widget)

        #self.ids.boxlayout_id.add_widget(newLabel)
        #self.add_widget(_item2(self))
        #return ListScreen()
    pass

    def onChange(self, text):
        #sm.clear_widgets(screens=[sm.get_screen('discover')])
        sm.clear_widgets(screens=[self])

        print 'list folder onchange',  menu.get(text)

        discover = menu.get(text)

        sm.add_widget(ListDiscover(name = "discover", menu=discover))
        #sm.remove_widget('info')
        sm.current = 'discover'

#trouver un moyen de load populaire peux importe les lang utiliser
    def on_sub_Change(self, text='Populaires'):
        #pas trouver d'autre solution
        try:
            sm.clear_widgets(screens=[sm.get_screen('discover')])
        except: pass

        self.ids.grid_id.clear_widgets()

        #self.remove_widget(self.grid_l)

        menu = sous_menu.get(self.type).get(text)

        try:
            json = _jsonload(self.type, menu,NextPage=self.pageNumber)
            for data in json:
                #btn = AsyncImage(subtext=data['name'], source="https://cdn2.iconfinder.com/data/icons/flat-ui-icons-24-px/24/eye-24-256.png", size_hint=(None, None), size=(160, 160))
                #size = (width, height)
                #aspect ratio 2/3 = 0.666

                btn = ImageButton(type=self.type,
                tmdbid=data['tmdbid'],
                img=data['poster_path'],
                size=(Window.width / 2 , (Window.width / 2) / 0.666 ))

                #btn = Button(text=data['name'], size_hint=(None, None), size=(220,300), background_normal='image.jpg', subtext=data['name'])
                self.grid.add_widget(btn)
            #change(self,text)
        except: pass

    #Pour afficher plus d'une page
    def on_change_Page(self, text='Populaires'):
        self.pageNumber = self.pageNumber + 1
        print 'page number ' ,self.pageNumber

        try:
            sm.clear_widgets(screens=[sm.get_screen('discover')])
        except: pass

        self.ids.grid_id.clear_widgets()

        print "change page ", text

        #self.remove_widget(self.grid_l)

        menu = sous_menu.get(self.type).get(text)

        try:
            json = _jsonload(self.type, menu,NextPage=self.pageNumber)
            for data in json:
                #btn = AsyncImage(subtext=data['name'], source="https://cdn2.iconfinder.com/data/icons/flat-ui-icons-24-px/24/eye-24-256.png", size_hint=(None, None), size=(160, 160))
                btn = ImageButton(type=self.type,
                tmdbid=data['tmdbid'],
                img=data['poster_path'],
                size=(Window.width / 2 , (Window.width / 2) / 0.666 ))

                #btn = Button(text=data['name'], size_hint=(None, None), size=(220,300), background_normal='image.jpg', subtext=data['name'])
                self.grid.add_widget(btn)
            #change(self,text)
        except: pass

class ImageButton(ButtonBehavior, AsyncImage):

    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)

        #icon = AsyncImage(source='https://cdn2.iconfinder.com/data/icons/flat-ui-icons-24-px/24/eye-24-256.png')
        self.background_normal = kwargs['img']
        #print "ratio", self.root.width
        self.tmdb = kwargs['tmdbid']
        self.type = kwargs['type']

    def on_press(self):
        def on_stop(*l):
            self.animation = Animation(size =(self.size[0] - 10, self.size[1] - 10), t='in_quad', duration=0.5)
            self.animation.start(self)

        self.animation = Animation(size =(self.size[0] + 10, self.size[1] + 10), t='in_quad', duration=0.5)
        self.animation.bind(on_complete=on_stop)
        self.animation.start(self)

        #App.get_running_app().root.manager.current = 'menu'
        # screen_manager = App.get_running_app().root
        # screen_manager.transition.direction = 'left'
        # screen_manager.current = 'info'
        sm.transition.direction = 'left'

        sm.add_widget(ListInfo(name = "info", type=self.type, tmdbid=self.tmdb))
        #sm.remove_widget('info')
        sm.current = 'info'

        #self.box_share2.clear_widgets()

        #sm.get_screen('first_screen').first_screen.text = "Hi I'm The Fifth Screen"

#screen information
class ListInfo(Screen):

    #box_share2 = ObjectProperty(None)
    grid_l = ObjectProperty(None)
    scroll_l = ObjectProperty(None)
    circle_l = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ListInfo, self).__init__(**kwargs)

        #json = _jsonload(self)
        json = tmdb().getByid(kwargs['type'], kwargs['tmdbid'])

        #introduit le dict dans self
        #a revoir c'est moche
        for value in json[0]:
            setattr(self, value, json[0][value])

        # img = AsyncImage(source=self.backdrop_path,
        # size=(1920, 1280),
        # keep_ratio=False,
        # allow_stretch=True,
        # pos=(-150, 150))

        # self.add_widget(img)

        self.ids.cicle_l.add_widget(MyCircle(num = self.vote_average))

        # self.vote_circle = str(round(float(self.vote_average) * 36, 2))

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

    def onChange(self, label):
        #self.box_share2.clear_widgets()
        sm.clear_widgets(screens=[sm.get_screen('info')])
        #sm.remove_widget('info')
        sm.current = 'list'
        #sm.clear_widgets('info')

    def show_source(self):

        #self.ids.spinner_source.values = ['A', 'B'] 

        sm.transition.direction = 'left'

        sm.add_widget(ListSource(name = "source"))
        sm.current = 'source'

    pass

class ListSource(Screen):

    grid_id = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ListSource, self).__init__(**kwargs)

        from iplugin import plugin

        _plugin = plugin().getFolder()

        for main in json.loads(_plugin):

            for sub in main.get('source'):
                text = ("%s - %s [%s]") % (main['plugin'], sub['title'] ,sub['qual'])
                self.ids.grid_id.add_widget(Button(text=text, font_size=14, on_press=partial(self.plays, url=sub['url'])))

    def onChange(self, text):
        #sm.clear_widgets(screens=[sm.get_screen('discover')])
        sm.clear_widgets(screens=[self])
        sm.transition.direction = 'left'
        #sm.remove_widget('info')
        sm.current = 'info'
    pass

    def plays(self, *args, **kwargs):
        print kwargs['url']
        #VideoAlan().calistir(kwargs['url'],'Nop')

        #root.parent.get_screen("main").calistir(filechooser.path,filechooser.selection)
        sm.get_screen("main").calistir(kwargs['url'],kwargs['url'])
        sm.current = "main"

class MyCircle(GridLayout):
    def __init__(self, **kwargs):
        #circle: self.center_x, self.center_y, min(50, 50) / 2, 210, 360
        super(MyCircle, self).__init__(**kwargs)

        num = round(float(kwargs['num']) * 36, 2)

        #self.size_hint = (None, None)
        with self.canvas:
            #pts = [self.center_x, self.center_y, min(50, 50) / 2, 0, num]
            pts = [(Window.width/1.17), (Window.height/2.45), min(80, 80) / 2, 0, num]
            self.line = Line(circle=pts, width=5)

class ListDiscover(Screen):

    def __init__(self, **kwargs):
        self.pickType = menu.viewkeys()

        self.sousType = sous_menu.get(kwargs['menu']).viewkeys()

        super(ListDiscover, self).__init__(**kwargs)

        #self.grid = self.grid_l

        self.menu = kwargs['menu']
        #auplus simple

        #poster

        json = tmdb().getDiscover(kwargs['menu'])
        for data in json:
            #btn = ImageButton(data)
            btn = ImageButton(type=self.menu,
            tmdbid=data['tmdbid'],
            img=data['backdrop_path_780'],
            size=(Window.width , Window.width / 1.777))
            self.discover_grid.add_widget(btn)
            label = discover_layout(data)
            self.discover_grid.add_widget(label)

        #self.grid_id.add_widget(self.grid_id2)

    def onChange(self, text):

        sm.clear_widgets(screens=[self])
        #sm.clear_widgets(screens=[sm.get_screen('list')])
        discover = menu.get(text)

        sm.add_widget(ListDiscover(name ="discover", menu=discover))
        #sm.remove_widget('info')
        sm.current = "discover"

    def on_sub_Change(self, text=None):
        menu = sous_menu.get(self.menu).get(text)

        sm.add_widget(ListFolder(name ="list", type=self.menu, menu=menu))
        sm.current = "list"

        #self.remove_widget(self.grid_l)
        #self.ids.grid_id.clear_widgets()

        #change(self,text)

class discover_layout(BoxLayout):

    def __init__(self, data, **kwargs):
        super(discover_layout, self).__init__(**kwargs)
        self.title = data['title']
        self.overview = data['overview'][0:140]
        self.release_date = data['release_date']
        self.vote_average = str(data['vote_average'])
    pass

class ListParam(Screen):
    pass

#change screen
# def change(self, text):
#     print text
#     if text == "popular":
#         print "passe popular"
#         sm.add_widget(ListFolder(name = "list", menu='movie', sous_menu='popular'))
#         sm.current = 'list'
#     if text == "Mieux notes":
#         print "passe notes"
#         sm.add_widget(ListFolder(name = "list", menu='movie', sous_menu='rated'))
#         sm.current = 'list'

#     if text == "Movies":
#         self.manager.current = 'files'
#     elif text == "Series":
#         self.manager.current = 'files'
#     elif text == "Autres":
#         self.manager.current = 'files'

def _jsonload(type, menu,NextPage):

    print "json", type, menu
    if menu == 'popular':
        return tmdb().getPopular(NextPage)
    elif menu == "top_rated":
        return tmdb().getRated(NextPage)

class Video(App):

    def build(self):

        Config.set('kivy', 'keyboard_mode', 'system')
        Config.set('graphics', 'width', '480')
        Config.set('graphics', 'height', '800')
        Config.set('graphics', 'resizable', 0)
        Config.write()

        sm.add_widget(VideoAlan(name = "main"))
        sm.add_widget(OpenFolder(name = "files"))
        #list de film
        sm.add_widget(ListFolder(name = "list", type="movie", menu='popular'))
        #decouvrir par default
        #sm.add_widget(ListDiscover(name = "movie", menu='movie'))
        #paramettre
        sm.add_widget(ListParam(name = "param"))
        #sm.add_widget(ListInfo(name = "info"))

        return sm

if __name__ in ('__main__', '__android__'):
    Window.clearcolor = (0,0,0,0)
    #print 'list' , _plugin.getList()

    #print 'Name' , _plugin.getPluginName()

    #print 'nameee', vars(_plugin)

    Video().run()
