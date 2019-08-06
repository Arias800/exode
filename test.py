# process = subprocess.run (
#      ' python "chemin / vers / collect_widet.py" module.nom " ,
#      cwd = ' <chemin de l'espace de travail> ' ,
#      stdout = sous-processus. PIPE , env = os.environ,
#      shell = True , encoding = ' utf8 '
# )
# si process.returncode ==  0 :
#     data = json.loads (process.stdout)

import kivy
kivy.require("1.10.1")

from kivy.app import App

from kivy.lang import Builder
from kivy.factory import Factory

from kivymd.theming import ThemeManager


#fichier avec test.kv qui permet de faire des test d'emplacement de desing
#pour eviter de recharger le lecteur tout le temp

class TestApp(App):
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Blue'
    pass


if __name__ == '__main__':
    TestApp().run()