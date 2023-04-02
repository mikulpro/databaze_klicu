from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp


class ActionSelectionScreen(Screen):

    def __init__(self, **kwargs):
        super(ActionSelectionScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        MDApp.get_running_app().on_resize()
        return super().on_enter(*args)

    def on_leave(self, *args):
        MDApp.get_running_app().on_resize()
        return super().on_leave(*args)

    def pujcit(self):
        MDApp.get_running_app().sc_mngr.current = "floorselection"
        MDApp.get_running_app().sc_mngr.get_screen("floorselection").SearchFloorTextInputFunction(initial=True)
        MDApp.get_running_app().on_resize()

    def vratit(self):
        MDApp.get_running_app().sc_mngr.current = "borrowingselection"
        MDApp.get_running_app().sc_mngr.get_screen("borrowingselection").SearchBorrowingTextInputFunction()
        MDApp.get_running_app().on_resize()