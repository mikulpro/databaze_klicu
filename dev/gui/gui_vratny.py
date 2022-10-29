from tkinter import Grid
# from ...db_interface import Db as db
from pomocne_gui_funkce import *

from kivy.app import App
from kivy.uix.widget import Widget
# from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

class LoginWindow(GridLayout):
    pass

class LoginApp(App):
    def build(self):
        self.title = "Přihlášení se"
        return LoginWindow()


if __name__ == "__main__":
    Window.clearcolor = (1, 1, 1, 1)
    Window.size = (1280, 720)

    login = LoginApp()
    login.run()

    login_uspesny = False
    if login_uspesny:
        pass