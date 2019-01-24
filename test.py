from kivy.app import App
from kivy.lang import Builder

kv = '''
BoxLayout:
    Slider:
        id: start
        orientation: 'vertical'
        size_hint_x: None
        width: 20
        max: 360
    Slider:
        id: end
        orientation: 'vertical'
        size_hint_x: None
        width: 20
        max: 360
    GridLayout:
        cols: 2
        Widget:
            canvas:
                Line:
                    width: 10
                    circle: self.center_x, self.center_y, min(self.width, 50) / 2, 0, 180
        Widget:
            canvas:
                Line:
                    width: 2
                    ellipse: self.x, self.y,\
                             self.width, self.height,\
                             start.value, end.value
        Widget:
            canvas:
                Ellipse:
                    pos: self.x, self.y
                    size: self.width, self.height
                    angle_start: start.value
                    angle_end: end.value

'''


class MyApp(App):
    def build(self):
        return Builder.load_string(kv)


MyApp().run()