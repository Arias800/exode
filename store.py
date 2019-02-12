from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty

class ScreenSwitcher(ScreenManager):
     #The screens can be added on the __init__ method like this or on the .kv file
    def __init__(self, **kwargs):
        super(ScreenSwitcher, self).__init__(**kwargs)
        self.add_widget(ScreenOne(name='sone'))
        self.add_widget(ScreenTwo(name='stwo'))

    def newscreen(self, screen):
        self.add_widget(screen)



class ScreenOne(Screen):
    pass


class ScreenTwo(Screen):
    pass

class ScreenTest(Screen):
    pass


class MainScreen(GridLayout):
    manager = ObjectProperty(None)

    def onChange(self):
        self.manager.add_widget(ScreenTest(name='test'))
        print vars(self.manager)
        self.manager.current = "test"


class StoreApp(App):
    def build(self):
        return MainScreen()


if __name__ == "__main__":
    StoreApp().run()