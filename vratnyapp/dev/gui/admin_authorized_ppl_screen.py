from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from .admin_authorized_person_widget import AdminAuthorizedPersonWidget


class AdminAuthorizedPplScreen(Screen):

    def __init__(self, **kwargs):
        super(AdminAuthorizedPplScreen, self).__init__(**kwargs)

    def change_to_loading(self):
        MDApp.get_running_app().sc_mngr.current = "loading"

    def on_enter(self, *args):
        self.display_authorizations()
        return super().on_enter(*args)

    def display_authorizations(self):
        searched_expression = ""
        
        searched_expression = str(MDApp.get_running_app().sc_mngr.get_screen("admin_authorized_ppl").ids.admin_auth_ppl_search.text)
        
        found_ppl = []
        if searched_expression is None or searched_expression == "":
            number_of_displayed_auths = 0
            for widget in MDApp.get_running_app().preloaded_auths:
                number_of_displayed_auths += 1
                self.ids.admin_person_widget_scrollview.add_widget(widget)
                if number_of_displayed_auths >= 2000:
                    break
            return
        else:
            found_ppl = MDApp.get_running_app().db.search_authorizations(searched_expression)

        self.ids.admin_person_widget_scrollview.clear_widgets()

        number_of_displayed_auths = 0
        for person in found_ppl:
            number_of_displayed_auths += 1
            if number_of_displayed_auths < 40:
                self._admin_add_authorised_person_widget(person)
        

    def _admin_add_authorised_person_widget(self, data):
        widget = AdminAuthorizedPersonWidget()
        widget.data = data
        widget.ids.name.text = str(data.person.get_full_name())
        if data.origin_id == "1" or data.origin_id == 1:
            widget.ids.authorized_by.text = "admin"
        else:
            widget.ids.authorized_by.text = "neznámý"
        widget.ids.time.text = str(data.created)
        widget.ids.time2.text = str(data.expiration)
        widget.ids.room.text = str(data.room.name)
        self.ids.admin_person_widget_scrollview.add_widget(widget)


    def admin_authorise_new_person(self):
        pass