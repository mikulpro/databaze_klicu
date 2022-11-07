# from tkinter import Grid
# # from ...db_interface import Db as db
# from pomocne_gui_funkce import *

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.config import Config
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

# colors = {
#     "Cyan": {
#         "200": "#005963",
#         "500": "#005963",
#         "700": "#005963",
#     },
#     "Gray": {
#         "200": "#ededed",
#         "500": "#ededed",
#         "700": "#ededed",
#     },
#     "Red": {
#         "200": "#ff0000",
#         "500": "#ff0000",
#         "A700": "#ff0000",
#     },
#     "Light": {
#         "StatusBar": "E0E0E0",
#         "AppBar": "#202020",
#         "Background": "#ededed",
#         "CardsDialogs": "#FFFFFF",
#         "FlatButtonDown": "#CCCCCC",
#     },
# }


class SearchResultWidget(BoxLayout):
    # sem funkce ohledne klikani na widget samotny
    ...


class LoginScreen(Screen):
    ...


class KeySelectionScreen(Screen):
    
    def __init__(self, **kwargs):
        super(KeySelectionScreen, self).__init__(**kwargs)
    
    def add_key_widget(self):
        key_widget = SearchResultWidget()
        self.ids.key_widget_scrollview.add_widget(key_widget)


class PersonSelectionScreen(Screen):
    ...


class VratnyApp(MDApp):
    def build(self):
        # self.theme_cls.colors = colors
        # self.theme_cls.primary_palette = "Gray"
        # self.theme_cls.accent_palette = "Cyan"
        # self.theme_cls.theme_style = "Light"
        
        Builder.load_file('vratny.kv')

        sc_mngr = ScreenManager(transition = NoTransition())
        sc_mngr.add_widget(LoginScreen(name = "login"))
        sc_mngr.add_widget(KeySelectionScreen(name = "keyselection"))

        return sc_mngr


def PrihasitSeButtonFunction(username=None, password=None):

    # some function to authenticate

    # some function to select next screen

    ...


if __name__ == "__main__":
    
    Window.size = (1080, 720)
    Config.set('graphics', 'width', '1080')
    Config.set('graphics', 'height', '720')

    VratnyApp().run()