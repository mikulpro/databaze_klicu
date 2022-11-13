# python modules
from datetime import datetime
from dev.sqlite.db_interface import Db

# kivy builder and builder configuration
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.config import Config
from kivy.resources import resource_find

# kivy material design library
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.pickers import MDDatePicker, MDTimePicker

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
        #if username == "Pavel Pyšný" and password == "123456":
        if username == "" and password == "":
            MDApp.get_running_app().set_lender(username)
            return True
        else:
            return False


    def PrihasitSeButtonFunction(self):

        # some function to authenticate
        usr = self.ids.user.text
        pswd = self.ids.password.text
        
        if self._authenticate(usr, pswd):
            # some function to select next screen
            self.manager.current = "actionselection"


class ActionSelectionScreen(Screen):


    def __init__(self, **kwargs):
        super(ActionSelectionScreen, self).__init__(**kwargs)


    def pujcit(self):
        sc_mngr.current = "floorselection"


    def vratit(self):
        pass


class FloorSelectionScreen(Screen):


    def __init__(self, **kwargs):
        super(FloorSelectionScreen, self).__init__(**kwargs)
        #self._list_of_current_keywidgets = []
        self.SearchFloorTextInputFunction(initial=True) # initial search


    def SearchFloorTextInputFunction(self, initial=False):
        floors = MDApp.get_running_app().get_all_floors()
        
        # undisplaying old floors
        self.ids.floor_widget_scrollview.clear_widgets()
        
        # displaying new floors
        number_of_displayed_floors = 0
        for floor in floors:
            if number_of_displayed_floors == 9:
                break
            if initial or str(self.ids.floorsearch.text) in str(floor):
                number_of_displayed_floors += 1
                self._add_floorwidget(floor)


    def _add_floorwidget(self, data):
        floor_widget = SearchResultWidget()
        floor_widget.ids.searchresultwidget_label_content.text = str(data)
        floor_widget.label_pointer = floor_widget.ids.searchresultwidget_label_content
        self.ids.floor_widget_scrollview.add_widget(floor_widget)


class KeySelectionScreen(Screen):


    def __init__(self, **kwargs):
        super(KeySelectionScreen, self).__init__(**kwargs)
        self.SearchKeyTextInputFunction() # initial search


    def SearchKeyTextInputFunction(self):
        
        # find all relevant examples
        selected_floor = MDApp.get_running_app().get_selected_floor()
        searched_expression = str(self.ids.keysearch.text)
        if len(searched_expression) >= 1:
            list_of_matches_keys = MDApp.get_running_app().get_room_by_name_fraction(fraction=searched_expression, floor=selected_floor)
        else:
            list_of_matches_keys = MDApp.get_running_app().get_rooms_by_floor(floor=selected_floor)

        # undisplay old rooms
        self.ids.key_widget_scrollview.clear_widgets()

        # some function, that adds widget for each match
        number_of_displayed_rooms = 0
        for item in list_of_matches_keys:
            if number_of_displayed_rooms == 9:
                break
            self._add_keywidget(item)


    def _add_keywidget(self, data):
        key_widget = SearchResultWidget()
        key_widget.ids.searchresultwidget_label_content.text = str(data)
        key_widget.label_pointer = key_widget.ids.searchresultwidget_label_content
        self.ids.key_widget_scrollview.add_widget(key_widget)


class PersonSelectionScreen(Screen):


    def __init__(self, **kwargs):
        super(PersonSelectionScreen, self).__init__(**kwargs)
        self._list_of_current_personwidgets = []
        self.PersonSearchTextInputFunction() # initial search


    def PersonSearchTextInputFunction(self):
        
        # some function, that finds all relevant examples
        searched_expression = self.ids.personsearch.text
        list_of_matches_ppl = MDApp.get_running_app().find_relevant_matches(searched_expression, "dev/sqlite/old/data/data_Borrowers.csv")

        # some function, that removes all existing widgets
        self._remove_current_personwidgets()

        # some function, that adds widget for each match
        for item in list_of_matches_ppl:
            self._add_personwidget(item)


    def _remove_current_personwidgets(self):
        for item in self._list_of_current_personwidgets:
            if item is not None:
                self.ids.person_widget_scrollview.remove_widget(item)


    def _add_personwidget(self, data):
        person_widget = SearchResultWidget()
        person_widget.ids.searchresultwidget_label_content.text = data
        person_widget.label_pointer = person_widget.ids.searchresultwidget_label_content
        self._list_of_current_personwidgets.append(person_widget)
        self.ids.person_widget_scrollview.add_widget(person_widget)


class TimeSelectionScreen(Screen):


    def __init__(self, **kwargs):
        super(TimeSelectionScreen, self).__init__(**kwargs)

    
    def confirm_timestamps(self):
        if self.ids.datepicker_label.text not in ["CANCELED", "Nebylo vybráno žádné datum"] and self.ids.timepicker_label.text not in ["None", "Nebyl vybrán žádný čas"]:
            sc_mngr.current = "review"


class ReviewScreen(Screen):


    def __init__(self, **kwargs):
        super(ReviewScreen, self).__init__(**kwargs)


class VratnyApp(MDApp):


    def __init__(self, database_object=Db(), **kwargs):
        super(VratnyApp, self).__init__(**kwargs)
        self.selected_lender = ""
        self.selected_floor = 1
        self.selected_key = None
        self.selected_person = None
        self.selected_starttime = datetime.now()
        self.selected_endtime_time = None
        self.selected_endtime_date = None
        self.db = database_object

    def get_all_floors(self):
        return self.db.get_all_floors()

    def get_rooms_by_floor(self, floor):
        return self.db.get_rooms_by_floor(floor)

    def get_authorizations_for_room(self, room_id):
        return self.db.get_authorizations_for_room(room_id)

    def get_primary_authorizations_for_room(self, room_id):
        return self.db.get_primary_authorizations_for_room(room_id)

    def get_borrowers_by_name_fraction(self, fraction):
        return self.db.get_borrowers_by_name_fraction(fraction)
    
    def get_room_by_name_fraction(self, fraction, floor=None):
        return self.db.get_room_by_name_fraction(fraction, floor)

    def add_borrowing(self, key_id, borrower_id):
        self.add_borrowing(key_id, borrower_id)

    def return_key(self, borrowing_id):
        self.db.return_key(borrowing_id)

    def get_ongoing_borrowings(self):
        return self.db.get_ongoing_borrowings()

    def excel_dump(self):
        return self.db.excel_dump()

    def set_lender(self, input):
        self.selected_lender = input


    def show_time_picker(self):
		# Define default time
        default_time = datetime.strptime("23:59:59", '%H:%M:%S').time()

        time_dialog = MDTimePicker()
		# Set default Time
        time_dialog.set_time(default_time)
        time_dialog.bind(on_cancel=self._on_timepicker_cancel, time=self._on_timepicker_confirm)
        time_dialog.open()


    def _on_timepicker_confirm(self, instance, time):
        self.selected_endtime_time = str(time)
        sc_mngr.get_screen("timeselection").ids.timepicker_label.text = str(time)


    def _on_timepicker_cancel(self, instance, time):
        self.selected_endtime_time = self.selected_endtime_time
        if self.selected_endtime_time is None or self.selected_endtime_time == "None":
            sc_mngr.get_screen("timeselection").ids.timepicker_label.text = "Nebyl vybrán žádný čas"
        else:
            sc_mngr.get_screen("timeselection").ids.timepicker_label.text = str(time)


    def show_date_picker(self):
		#date_dialog = MDDatePicker(year=2000, month=2, day=14)
        date_dialog = MDDatePicker(mode="range")
        date_dialog.bind(on_save=self._on_datepicker_confirm, on_cancel=self._on_datepicker_cancel)
        date_dialog.open()


    def _on_datepicker_confirm(self, instance, value, date_range):
        self.selected_endtime_date = date_range[-1]
        sc_mngr.get_screen("timeselection").ids.datepicker_label.text = str(date_range[-1])


    def _on_datepicker_cancel(self, instance, value):
        sc_mngr.get_screen("timeselection").ids.datepicker_label.text = "CANCELED"


    def SearchResultWidgetClickFunction(self, pressed_button_instance):
        if sc_mngr.current == "floorselection":
            self.selected_floor = pressed_button_instance.text
            sc_mngr.current = "keyselection"
        elif sc_mngr.current == "keyselection":
            self.selected_key = pressed_button_instance.text
            sc_mngr.current = "personselection"
        elif sc_mngr.current == "personselection":
            self.selected_person = pressed_button_instance.text
            sc_mngr.current = "timeselection"        

    def get_selected_floor(self):
        return self.selected_floor

    def get_selected_key(self):
        return self.selected_key


    def find_relevant_matches(self, input_text, where_to_search):
        output = []
        #return ["testing_result"]
        
        try:
            with open(where_to_search, "r", encoding="utf8") as f:
                for line in f:
                    if input_text in line:
                        output.append(line)
            f.close()          
        except:
            pass

        if len(output) > 8:
            return output[:8]

        return output


    def build(self):

        Window.size = (1080, 720)
        Config.set('graphics', 'width', '1080')
        Config.set('graphics', 'height', '720')

        filename = 'style_vratny.kv'
        filename = resource_find(filename) or filename
        if filename in Builder.files:
            Builder.unload_file(filename)
        Builder.load_file('dev/gui/style_vratny.kv')

        global sc_mngr
        sc_mngr = ScreenManager(transition = NoTransition())
        sc_mngr.add_widget(LoginScreen(name = "login"))
        sc_mngr.add_widget(ActionSelectionScreen(name = "actionselection"))
        sc_mngr.add_widget(FloorSelectionScreen(name = "floorselection"))
        sc_mngr.add_widget(KeySelectionScreen(name = "keyselection"))
        sc_mngr.add_widget(PersonSelectionScreen(name = "personselection"))
        sc_mngr.add_widget(TimeSelectionScreen(name = "timeselection"))
        sc_mngr.add_widget(ReviewScreen(name = "review"))

        return sc_mngr


    def update_review_information(self):
        sc_mngr.get_screen("review").ids.rev_lab_lender.text = str("Oprávněná osoba: " + self.selected_lender)
        sc_mngr.get_screen("review").ids.rev_lab_borrower.text = str("Komu půjčuje: " + self.selected_person)
        sc_mngr.get_screen("review").ids.rev_lab_key.text = str("Klíč: " + self.selected_key)
        sc_mngr.get_screen("review").ids.rev_lab_starttime.text = str("Od: " + str(self.selected_starttime))
        sc_mngr.get_screen("review").ids.rev_lab_endtime.text = str("Do: " + str(self.selected_endtime_time) + str(self.selected_endtime_date))


if __name__ == "__main__":
    VratnyApp().run()
