#-*- coding: utf-8 -*-
from kivy.app import App
from kivy.core.window import Window

from kivy.uix.image import Image, AsyncImage
from kivy.uix.behaviors import ButtonBehavior

from kivy.animation import Animation

import os

class BlackHole(object):
    def __init__(self, **kw):
        super(BlackHole, self).__init__()

def EXlog(message):
    return print('[APPLICATION] EXODE: '+str(message))

class ImageButton(ButtonBehavior, AsyncImage, BlackHole):
    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.source = kwargs['img']

        ##alert : normal que quand ont agrandit la genetre ça bug il faut recharger les images pour prendre en compte Window.size
        #calcul backdrop
        #Backdrops should have an aspect ratio of 1.78:1 (16x9).
        #calcul poster
        #An aspect ratio of 1:1.5 (2:3) is usually preferred.
        #Window.size (width, height)
        self.size = Window.size[0] , Window.size[0] / 1.78
        self.types = kwargs['types']
        self.tmdb = kwargs['tmdbid']
        self.function = kwargs['functionName']
        self.keep_ratio = False
        self.allow_stretch = True
        print(Window.size[0] / 1.78)
        #EXlog("ratio", self.root.width)

    def on_press(self):
        def on_stop(*l):
            self.animation = Animation(size =(self.size[0] - 10, self.size[1] - 10), t='in_quad', duration=0.5)
            self.animation.start(self)

        self.animation = Animation(size =(self.size[0] + 10, self.size[1] + 10), t='in_quad', duration=0.5)
        self.animation.bind(on_complete=on_stop)
        self.animation.start(self)

        app = App.get_running_app()
        EXlog((self.parent.parent.parent.parent.manager))

        app.root.manager.add_widget(self.function(name = "info", types=self.types, tmdbid=self.tmdb))
        app.root.manager.current = "info"
