from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.core.window import Window

from kivy.garden.navigationdrawer import NavigationDrawer

class ExampleApp(App):

    def build(self):
        navigationdrawer = NavigationDrawer()

        side_panel = BoxLayout(orientation='vertical')
        
        side_panel.add_widget(Label(text='XCHANGE'))
        side_panel.add_widget(Button(text='Files'))
        side_panel.add_widget(Button(text='About'))
        
        navigationdrawer.add_widget(side_panel)
        
        main_panel = BoxLayout(orientation='vertical')
        
        #
        #
        #
        # MAIN PANEL WIDGETS ARE HERE
        #
        #
        #
        
        navigationdrawer.add_widget(main_panel)

        button = Button(text='toggle NavigationDrawer state (animate)',size_hint_y=0.2)
        button.bind(on_press=lambda j: navigationdrawer.toggle_state())
        
        main_panel.add_widget(button)

        return navigationdrawer


if __name__ == "__main__":
    ExampleApp().run()