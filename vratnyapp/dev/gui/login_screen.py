from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp


class LoginScreen(Screen):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        MDApp.get_running_app().on_resize()
        return super().on_enter(*args)

    def on_leave(self, *args):
        MDApp.get_running_app().on_resize()
        return super().on_leave(*args)

    def _authenticate(self, username, password):
        
        user = MDApp.get_running_app().db.get_user_by_username(username)
        if user is not None and user.check_password(password):
            MDApp.get_running_app().set_lender(username)
            if user.is_superuser:
                MDApp.get_running_app().sc_mngr.current = "admin"
                return False
            else:
                return True

    def PrihasitSeButtonFunction(self):

        # some function to authenticate
        usr = self.ids.user.text
        pswd = self.ids.password.text

        if self._authenticate(usr, pswd):
            # some function to select next screen
            self.manager.current = "actionselection"
            MDApp.get_running_app().on_resize()