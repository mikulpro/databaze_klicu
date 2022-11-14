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
        self.borrowing = None


# first screen
class LoginScreen(Screen):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

    def _authenticate(self, username, password):
        # if username == "Pavel Pyšný" and password == "123456":
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
        sc_mngr.current = "borrowingselection"


class BorrowingSelectionScreen(Screen):

    def __init__(self, **kwargs):
        super(BorrowingSelectionScreen, self).__init__(**kwargs)
        self.SearchBorrowingTextInputFunction()  # initial search

    def SearchBorrowingTextInputFunction(self):
        borrowings = MDApp.get_running_app().get_ongoing_borrowings()

        # undisplaying old floors
        self.ids.borrowings_widget_scrollview.clear_widgets()

        # displaying new floors
        number_of_displayed_borrowings = 0
        for b in borrowings:
            if number_of_displayed_borrowings == 9:
                break
            number_of_displayed_borrowings += 1
            self._add_borrowingwidget(b)

    def _add_borrowingwidget(self, data):
        borrowing_widget = SearchResultWidget()
        borrowing_widget.ids.searchresultwidget_label_content.text = str(data.authorization.person.get_full_name())
        borrowing_widget.label_pointer = borrowing_widget.ids.searchresultwidget_label_content
        borrowing_widget.borrowing = data
        self.ids.borrowings_widget_scrollview.add_widget(borrowing_widget)


class FloorSelectionScreen(Screen):

    def __init__(self, **kwargs):
        super(FloorSelectionScreen, self).__init__(**kwargs)
        self.SearchFloorTextInputFunction(initial=True)  # initial search

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


class RoomSelectionScreen(Screen):

    def __init__(self, **kwargs):
        super(RoomSelectionScreen, self).__init__(**kwargs)
        self.SearchRoomTextInputFunction()  # initial search

    def SearchRoomTextInputFunction(self):

        # find all relevant examples
        selected_floor = MDApp.get_running_app().get_selected_floor()
        searched_expression = str(self.ids.roomsearch.text)
        if len(searched_expression) >= 1:
            list_of_matches_rooms = MDApp.get_running_app().get_room_by_name_fraction(fraction=searched_expression,
                                                                                      floor=selected_floor)
        else:
            list_of_matches_rooms = MDApp.get_running_app().get_room_by_name_fraction(fraction="", floor=selected_floor)
            # list_of_matches_keys = MDApp.get_running_app().get_rooms_by_floor(floor=selected_floor)

        # undisplay old rooms
        self.ids.room_widget_scrollview.clear_widgets()

        # some function, that adds widget for each match
        number_of_displayed_rooms = 0
        for item in list_of_matches_rooms:
            if number_of_displayed_rooms == 9:
                break
            number_of_displayed_rooms += 1
            self._add_keywidget(item.name)

    def _add_keywidget(self, data):
        key_widget = SearchResultWidget()
        key_widget.ids.searchresultwidget_label_content.text = str(data)
        key_widget.label_pointer = key_widget.ids.searchresultwidget_label_content
        self.ids.room_widget_scrollview.add_widget(key_widget)


class KeySelectionScreen(Screen):

    def __init__(self, **kwargs):
        super(KeySelectionScreen, self).__init__(**kwargs)
        self.SearchKeyTextInputFunction()  # initial search

    def SearchKeyTextInputFunction(self):

        # find all relevant examples
        selected_room = MDApp.get_running_app().get_selected_room()
        selected_room = MDApp.get_running_app().get_room_by_name_fraction(fraction=selected_room)
        searched_expression = str(self.ids.keysearch.text)
        available_keys = []
        if selected_room is not None and len(selected_room) >= 1:
            available_keys = selected_room[-1].keys

        # undisplay old rooms
        self.ids.key_widget_scrollview.clear_widgets()

        # some function, that adds widget for each match
        number_of_displayed_rooms = 0
        for item in available_keys:
            if number_of_displayed_rooms >= 9:
                break
            number_of_displayed_rooms += 1
            self._add_keywidget(item.registration_number)

    def _add_keywidget(self, data):
        key_widget = SearchResultWidget()
        key_widget.ids.searchresultwidget_label_content.text = str(data)
        key_widget.label_pointer = key_widget.ids.searchresultwidget_label_content
        self.ids.key_widget_scrollview.add_widget(key_widget)


class PersonSelectionScreen(Screen):

    def __init__(self, **kwargs):
        super(PersonSelectionScreen, self).__init__(**kwargs)
        self.PersonSearchTextInputFunction()  # initial search

    def PersonSearchTextInputFunction(self):

        # find all relevant examples
        searched_expression = str(self.ids.personsearch.text)
        if len(searched_expression) >= 1:
            list_of_matches_ppl = MDApp.get_running_app().get_borrowers_by_name_fraction(fraction=searched_expression)
        else:
            list_of_matches_ppl = MDApp.get_running_app().get_borrowers_by_name_fraction(fraction="")

        # undisplay old rooms
        self.ids.person_widget_scrollview.clear_widgets()

        # some function, that adds widget for each match
        number_of_displayed_ppl = 0
        for item in list_of_matches_ppl:
            if number_of_displayed_ppl >= 9:
                break
            else:
                number_of_displayed_ppl += 1
                self._add_personwidget((str(item.firstname) + " " + str(item.surname)))

    def _add_personwidget(self, data):
        person_widget = SearchResultWidget()
        person_widget.ids.searchresultwidget_label_content.text = data
        person_widget.label_pointer = person_widget.ids.searchresultwidget_label_content
        self.ids.person_widget_scrollview.add_widget(person_widget)


class TimeSelectionScreen(Screen):

    def __init__(self, **kwargs):
        super(TimeSelectionScreen, self).__init__(**kwargs)

    def confirm_timestamps(self):
        if self.ids.datepicker_label.text not in [
            "CANCELED",
            "Nebylo vybráno žádné datum"
        ] and self.ids.timepicker_label.text not in [
            "None",
            "Nebyl vybrán žádný čas"
        ]:
            sc_mngr.current = "review"


class ReviewScreen(Screen):

    def __init__(self, **kwargs):
        super(ReviewScreen, self).__init__(**kwargs)


class VratnyApp(MDApp):

    def __init__(self, database_object=Db(), logger=None, **kwargs):
        super(VratnyApp, self).__init__(**kwargs)
        self.selected_lender = ""
        self.selected_floor = None
        self.selected_room = None
        self.selected_key = None
        self.selected_person = None
        self.selected_starttime = None
        self.selected_endtime_time = None
        self.selected_endtime_date = None
        self.selected_borrowing = None
        self.db = database_object
        self.logger = logger

    def update_starttime(self):
        self.selected_starttime = datetime.now()

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
        self.db.add_borrowing(key_id, borrower_id)

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
        # date_dialog = MDDatePicker(year=2000, month=2, day=14)
        date_dialog = MDDatePicker(mode="range")
        date_dialog.bind(on_save=self._on_datepicker_confirm, on_cancel=self._on_datepicker_cancel)
        date_dialog.open()

    def _on_datepicker_confirm(self, instance, value, date_range):
        self.selected_endtime_date = date_range[-1]
        sc_mngr.get_screen("timeselection").ids.datepicker_label.text = str(date_range[-1])

    def _on_datepicker_cancel(self, instance, value):
        sc_mngr.get_screen("timeselection").ids.datepicker_label.text = "CANCELED"

    def SearchResultWidgetClickFunction(self, pressed_button_instance):
        if sc_mngr.current == "borrowingselection":
            self.selected_borrowing = pressed_button_instance.borrowing
            self.return_key(self.selected_borrowing.id)
            #self.logger.warning(str(dir(pressed_button_instance)))
            sc_mngr.current = "actionselection"
        if sc_mngr.current == "floorselection":
            self.selected_floor = pressed_button_instance.text
            sc_mngr.current = "roomselection"
        elif sc_mngr.current == "roomselection":
            self.selected_room = pressed_button_instance.text
            sc_mngr.current = "keyselection"
        elif sc_mngr.current == "keyselection":
            self.selected_key = pressed_button_instance.text
            sc_mngr.current = "personselection"
        elif sc_mngr.current == "personselection":
            self.selected_person = pressed_button_instance.text
            sc_mngr.current = "review"

    def get_selected_floor(self):
        return self.selected_floor

    def get_selected_key(self):
        return self.selected_key

    def get_selected_room(self):
        return self.selected_room

    def find_relevant_matches(self, input_text, where_to_search):
        output = []
        # return ["testing_result"]

        try:
            with open(where_to_search, "r", encoding="utf8") as f:
                for line in f:
                    if input_text in line:
                        output.append(line)
            f.close()
        except Exception as e:
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
        sc_mngr = ScreenManager(transition=NoTransition())
        sc_mngr.add_widget(LoginScreen(name="login"))
        sc_mngr.add_widget(ActionSelectionScreen(name="actionselection"))
        sc_mngr.add_widget(BorrowingSelectionScreen(name="borrowingselection"))
        sc_mngr.add_widget(FloorSelectionScreen(name="floorselection"))
        sc_mngr.add_widget(RoomSelectionScreen(name="roomselection"))
        sc_mngr.add_widget(KeySelectionScreen(name="keyselection"))
        sc_mngr.add_widget(PersonSelectionScreen(name="personselection"))
        sc_mngr.add_widget(TimeSelectionScreen(name="timeselection"))
        sc_mngr.add_widget(ReviewScreen(name="review"))

        return sc_mngr

    def update_review_information(self):
        self.update_starttime()
        # sc_mngr.get_screen("review").ids.rev_lab_lender.text = str("Oprávněná osoba: " + self.selected_lender)
        sc_mngr.get_screen("review").ids.rev_lab_borrower.text = str("Komu půjčuje: " + self.selected_person)
        sc_mngr.get_screen("review").ids.rev_lab_key.text = str(f"Klíč: {self.selected_key}")
        sc_mngr.get_screen("review").ids.rev_lab_room.text = str(f"Místnost: {self.selected_room}")
        sc_mngr.get_screen("review").ids.rev_lab_starttime.text = str(
            f"Kdy: {self.selected_starttime.hour}:{self.selected_starttime.minute:02d} "
            f"{self.selected_starttime.day}. {self.selected_starttime.month}. {self.selected_starttime.year}")
        # sc_mngr.get_screen("review").ids.rev_lab_endtime.text = str("Do: " + str(self.selected_endtime_time) +
        #                                                             str(self.selected_endtime_date))

    def complete_borrowing_session(self):
        room = self.get_selected_room()
        room = self.get_room_by_name_fraction(fraction=room)[-1]

        room_keys = room.keys
        key_id = None
        for item in room_keys:
            if str(item.registration_number) == str(self.selected_key):
                key_id = item.id
                break

        borrower = self.get_borrowers_by_name_fraction(fraction=self.selected_person)[-1]
        borrower_id = borrower.id

        self.add_borrowing(key_id, borrower_id)

        self.selected_lender = ""
        self.selected_floor = None
        self.selected_room = None
        self.selected_key = None
        self.selected_person = None
        self.selected_starttime = None
        self.selected_endtime_time = None
        self.selected_endtime_date = None
        sc_mngr.current = "actionselection"
