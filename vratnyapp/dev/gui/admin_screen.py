from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp


class AdminScreen(Screen):

    def __init__(self, **kwargs):
        super(AdminScreen, self).__init__(**kwargs)

    def admin_func_1(self):
        MDApp.get_running_app().sc_mngr.current = "admin_authorized_ppl"
    
    def admin_func_2(self):
        pass

    def admin_func_3(self):
        MDApp.get_running_app().sc_mngr.get_screen("admin_authorized_ppl").admin_authorise_new_person()