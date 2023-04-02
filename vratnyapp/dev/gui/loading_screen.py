from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp


class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        MDApp.get_running_app().on_resize()
        return super().on_enter(*args)