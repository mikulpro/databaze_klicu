# from tkinter import Grid
# # from ...db_interface import Db as db
# from pomocne_gui_funkce import *

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.config import Config
from kivymd.app import MDApp

colors = {
    "Cyan": {
        "200": "#005963",
        "500": "#005963",
        "700": "#005963",
    },
    "Gray": {
        "200": "#ededed",
        "500": "#ededed",
        "700": "#ededed",
    },
    "Red": {
        "200": "#ff0000",
        "500": "#ff0000",
        "A700": "#ff0000",
    },
    "Light": {
        "StatusBar": "E0E0E0",
        "AppBar": "#202020",
        "Background": "#ededed",
        "CardsDialogs": "#FFFFFF",
        "FlatButtonDown": "#CCCCCC",
    },
}

class LoginApp(MDApp):
    def build(self):
        self.theme_cls.colors = colors
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.accent_palette = "Cyan"
        self.theme_cls.theme_style = "Light"
        return Builder.load_file('login.kv')


if __name__ == "__main__":
    
    Window.size = (1080, 720)
    Config.set('graphics', 'width', '1080')
    Config.set('graphics', 'height', '720')

    login = LoginApp()
    login.run()

    login_uspesny = False
    if login_uspesny:
        pass