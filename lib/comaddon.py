#-*- coding: utf-8 -*-
from kivy.app import App

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

        #icon = AsyncImage(source='https://cdn2.iconfinder.com/data/icons/flat-ui-icons-24-px/24/eye-24-256.png')
        self.background_normal = kwargs['img']
        self.types = kwargs['types']
        self.tmdb = kwargs['tmdbid']
        self.function = kwargs['functionName']
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
