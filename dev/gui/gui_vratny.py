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

# kivy basic objects
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

# auxiliary kivy functions
from kivy.properties import ObjectProperty
from kivy.metrics import dp

# # for MDDataTable override
# from kivymd.uix.dialog import BaseDialog
# from kivy.clock import Clock
# from functools import partial


# # MDDataTable override
# class MyDataTable(MDDataTable):
#         def __init__(self, **kwargs):
#             # skip the MDDataTable.__init__() and call its superclass __init__()
#             super(ThemableBehavior, self).__init__(**kwargs)
    
#             # schedule call to MDDataTable.__init__() contents after ids are populated
#             Clock.schedule_once(partial(self.delayed_init, **kwargs))
    
#         def delayed_init(self, dt, **kwargs):
#             # this is copied from MDDataTable.__init__() with super() call deleted
#             self.header = TableHeader(
#                 column_data=self.column_data,
#                 sorted_on=self.sorted_on,
#                 sorted_order=self.sorted_order,
#             )
#             self.table_data = TableData(
#                 self.header,
#                 row_data=self.row_data,
#                 check=self.check,
#                 rows_num=self.rows_num,
#                 _parent=self,
#             )
#             self.register_event_type("on_row_press")
#             self.register_event_type("on_check_press")
#             self.pagination = TablePagination(table_data=self.table_data)
#             self.table_data.pagination = self.pagination
#             self.header.table_data = self.table_data
#             self.table_data.fbind("scroll_x", self._scroll_with_header)
#             self.ids.container.add_widget(self.header)
#             self.ids.container.add_widget(self.table_data)
#             if self.use_pagination:
#                 self.ids.container.add_widget(self.pagination)
#             Clock.schedule_once(self.create_pagination_menu, 0.5)
#             self.bind(row_data=self.update_row_data)


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
    # sem funkce ohledne klikani na widget samotny
    ...

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
    
    def SearchKeyTextInputFunction(self):
        
        # some function, that finds all relevant examples
        searched_expression = self.ids.keysearch.text
        list_of_matches = self._find_relevant_matches(searched_expression)

        # some function, that removes all existing widgets
        self._remove_current_keywidgets()

        # some function, that adds widget for each match
        for item in list_of_matches:
            self._add_keywidget(item)

    def _find_relevant_matches(self, input_text):
        output = []
        
        try:
            with open("dev/sqlite/old/data/data_Rooms.csv", "r") as f:
                for line in f:
                    if input_text in line:
                        output.append(line)          
        except:
            pass

        if len(output) > 15:
            output = output[:14]

        return output

    def _remove_current_keywidgets(self):
        for item in self._list_of_current_keywidgets:
            if item is not None:
                self.ids.key_widget_scrollview.remove_widget(item)

    def _add_keywidget(self, data):
        key_widget = SearchResultWidget()
        key_widget.ids.searchresultwidget_label_content.text = data
        self._list_of_current_keywidgets.append(key_widget)
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


if __name__ == "__main__":
    
    Window.size = (1080, 720)
    Config.set('graphics', 'width', '1080')
    Config.set('graphics', 'height', '720')

    VratnyApp().run()