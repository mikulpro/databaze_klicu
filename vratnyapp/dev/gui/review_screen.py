from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp


class ReviewScreen(Screen):

    def __init__(self, **kwargs):
        super(ReviewScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        MDApp.get_running_app().update_review_information()
        MDApp.get_running_app().on_resize()
        return super().on_enter(*args)

    def on_leave(self, *args):
        MDApp.get_running_app().on_resize()
        return super().on_leave(*args)