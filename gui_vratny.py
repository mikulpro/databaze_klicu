from pomocne_gui_funkce import *

from kivy.app import App
from kivy.uix.widget import Widget

# ZATIM NEPOTREBNE IMPORTY
# from kivy.properties import NumericProperty, ReferenceListProperty
# from kivy.vector import Vector
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.label import Label
# from kivy.uix.image import Image
# from kivy.uix.button import Button
# from kivy.uix.textinput import TextInput

class PrihlaseniSe(Widget):
    pass

class VyberOsoby(Widget):
    pass

class GUIVratnyApp(App):    # !!! NEPREJMENOVAVAT, KRITICKE POJMENOVANI PRO SPOJENI S .kv SOUBOREM
    def build(self):
        self.title = "Zapůjčení klíče"
        return VyberOsoby()



if __name__ == "__main__":
    GUIVratnyApp().run()