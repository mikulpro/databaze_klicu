# from tkinter import Grid
# # from ...db_interface import Db as db
# from pomocne_gui_funkce import *

# kivy builder and builder configuration
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.config import Config

# kivy material design library
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDRoundFlatIconButton

# kivy basic objects
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

# auxiliary kivy functions
from kivy.properties import ObjectProperty
from kivy.metrics import dp


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

# custom widget fot ppl and keys
class SearchResultWidget(BoxLayout):
    

    def __init__(self, **kwargs):
        super(SearchResultWidget, self).__init__(**kwargs)
        self.label_pointer = None


# first screen
class LoginScreen(Screen):


    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

    def _authenticate(self, username, password):
        if username == "" and password == "":
            return True
        else:
            return False


    def PrihasitSeButtonFunction(self):

        # some function to authenticate
        usr = self.ids.user.text
        pswd = self.ids.password.text
        
        if self._authenticate(usr, pswd):
            # some function to select next screen
            self.manager.current = "keyselection"
        
# second screen
class KeySelectionScreen(Screen):


    def __init__(self, **kwargs):
        super(KeySelectionScreen, self).__init__(**kwargs)
        self._list_of_current_keywidgets = []
        self.SearchKeyTextInputFunction() # initial search


    def SearchKeyTextInputFunction(self):
        
        # some function, that finds all relevant examples
        searched_expression = self.ids.keysearch.text
        list_of_matches = self._find_relevant_matches(searched_expression)

        # some function, that removes all existing widgets
        self._remove_current_keywidgets()

        # some function, that adds widget for each match
        for item in list_of_matches:
            self._add_keywidget(item)

        # bugfix for duplicit buttons
        self._remove_error_labels()


    def _remove_error_labels(self):
        for item in self.ids.key_widget_scrollview.children:
            if item is not None and hasattr(item, 'text') and item.text == 'ERROR':
                self.ids.key_widget_scrollview.remove_widget(item)  


    def _find_relevant_matches(self, input_text):
        output = []
        #return ["testing_result"]
        
        try:
            with open("dev/sqlite/old/data/data_Rooms.csv", "r") as f:
                for line in f:
                    if input_text in line:
                        output.append(line)          
        except:
            pass

        if len(output) > 8:
            return output[:8]

        return output


    def _remove_current_keywidgets(self):
        for item in self._list_of_current_keywidgets:
            if item is not None:
                self.ids.key_widget_scrollview.remove_widget(item)


    def _add_keywidget(self, data):
        key_widget = SearchResultWidget()
        key_widget.ids.searchresultwidget_label_content.text = data
        key_widget.label_pointer = key_widget.ids.searchresultwidget_label_content
        self._list_of_current_keywidgets.append(key_widget)
        self.ids.key_widget_scrollview.add_widget(key_widget)


class PersonSelectionScreen(Screen):


    def __init__(self, **kwargs):
        super(PersonSelectionScreen, self).__init__(**kwargs)


class VratnyApp(MDApp):


    def __init__(self, **kwargs):
        super(VratnyApp, self).__init__(**kwargs)
        self.selected_key = None


    def SearchResultWidgetClickFunction(self, pressed_button_instance):
        self.selected_key = pressed_button_instance.text
        sc_mngr.current = "personselection"
        sc_mngr.get_screen("personselection").ids.debugging_label.text = self.selected_key


    def get_selected_key(self):
        return self.selected_key


    def build(self):
        Builder.load_file('vratny.kv')

        global sc_mngr
        sc_mngr = ScreenManager(transition = NoTransition())
        sc_mngr.add_widget(LoginScreen(name = "login"))
        sc_mngr.add_widget(KeySelectionScreen(name = "keyselection"))
        sc_mngr.add_widget(PersonSelectionScreen(name = "personselection"))

        return sc_mngr


if __name__ == "__main__":
    
    Window.size = (1080, 720)
    Config.set('graphics', 'width', '1080')
    Config.set('graphics', 'height', '720')

    VratnyApp().run()