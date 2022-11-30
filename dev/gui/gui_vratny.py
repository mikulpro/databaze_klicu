# python modules
import time
from datetime import datetime
from dev.sqlite.db_interface import Db

# kivy builder and builder configuration
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.config import Config
from kivy.resources import resource_find
from kivy.clock import Clock

# kivy material design library
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivy.uix.scrollview import ScrollView

# kivy basic objects
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

# auxiliary kivy functions
from kivy.properties import ObjectProperty
from kivy.metrics import dp

# custom widget fot ppl and keys
class SearchResultWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(SearchResultWidget, self).__init__(**kwargs)
        self.label_pointer = None
        self.data = None


# first screen
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
        if username == "" and password == "":
            MDApp.get_running_app().set_lender(username)
            return True
        elif username == "admin" and password == "admin":
            MDApp.get_running_app().set_lender("admin")
            sc_mngr.current = "admin"
            return False
        else:
            return False

    def PrihasitSeButtonFunction(self):

        # some function to authenticate
        usr = self.ids.user.text
        pswd = self.ids.password.text

        if self._authenticate(usr, pswd):
            # some function to select next screen
            self.manager.current = "actionselection"
            MDApp.get_running_app().on_resize()


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
        sc_mngr.current = "floorselection"
        sc_mngr.get_screen("floorselection").SearchFloorTextInputFunction(initial=True)
        MDApp.get_running_app().on_resize()

    def vratit(self):
        sc_mngr.current = "borrowingselection"
        sc_mngr.get_screen("borrowingselection").SearchBorrowingTextInputFunction()
        MDApp.get_running_app().on_resize()


class BorrowingSelectionScreen(Screen):

    def __init__(self, **kwargs):
        super(BorrowingSelectionScreen, self).__init__(**kwargs)
        self.SearchBorrowingTextInputFunction()  # initial search

    def on_enter(self, *args):
        MDApp.get_running_app().on_resize()
        return super().on_enter(*args)

    def on_leave(self, *args):
        MDApp.get_running_app().on_resize()
        return super().on_leave(*args)

    def SearchBorrowingTextInputFunction(self):
        borrowings = MDApp.get_running_app().get_ongoing_borrowings()

        # undisplaying old
        self.ids.borrowings_widget_scrollview.clear_widgets()

        # displaying new
        number_of_displayed_borrowings = 0
        for b in borrowings:
            if number_of_displayed_borrowings >= 500:
                break
            if self.ids.borrowingsearch.text in (str(b.authorization.person.get_full_name()) + "   " + str(b.key.room.name) + "   " +  str(b.borrowed)):
                number_of_displayed_borrowings += 1
                self._add_borrowingwidget(b)

    def _add_borrowingwidget(self, data):
        borrowing_widget = SearchResultWidget()
        borrowing_widget.ids.searchresultwidget_label_content.text = str(data.authorization.person.get_full_name()) + "   " + str(data.key.room.name) + "   " +  str(data.borrowed)
        borrowing_widget.label_pointer = borrowing_widget.ids.searchresultwidget_label_content
        borrowing_widget.data = data
        self.ids.borrowings_widget_scrollview.add_widget(borrowing_widget)


class FloorSelectionScreen(Screen):

    def __init__(self, **kwargs):
        super(FloorSelectionScreen, self).__init__(**kwargs)
        self.SearchFloorTextInputFunction(initial=True)  # initial search

    def on_enter(self, *args):
        MDApp.get_running_app().on_resize()
        return super().on_enter(*args)

    def on_leave(self, *args):
        MDApp.get_running_app().on_resize()
        return super().on_leave(*args)

    def SearchFloorTextInputFunction(self, initial=False):
        floors = MDApp.get_running_app().get_all_floors()
        floors.reverse()

        # undisplaying old floors
        self.ids.floor_widget_scrollview.clear_widgets()

        # displaying new floors
        number_of_displayed_floors = 0
        for floor in floors:
            if number_of_displayed_floors >= 500:
                break
            if initial or str(self.ids.floorsearch.text) in str(floor):
                number_of_displayed_floors += 1
                self._add_floorwidget(floor)

    def _add_floorwidget(self, data):
        floor_widget = SearchResultWidget()
        floor_widget.data = data
        floor_widget.ids.searchresultwidget_label_content.text = str(data)
        floor_widget.label_pointer = floor_widget.ids.searchresultwidget_label_content
        self.ids.floor_widget_scrollview.add_widget(floor_widget)


class RoomSelectionScreen(Screen):

    def __init__(self, **kwargs):
        super(RoomSelectionScreen, self).__init__(**kwargs)
        self.SearchRoomTextInputFunction()  # initial search

    def on_enter(self, *args):
        MDApp.get_running_app().on_resize()
        return super().on_enter(*args)

    def on_leave(self, *args):
        MDApp.get_running_app().on_resize()
        return super().on_leave(*args)

    def SearchRoomTextInputFunction(self):

        # find all relevant examples
        selected_floor = MDApp.get_running_app().get_selected_floor()
        searched_expression = str(self.ids.roomsearch.text)
        if len(searched_expression) >= 1:
            list_of_matches_rooms = MDApp.get_running_app().get_room_by_name_fraction(fraction=searched_expression,
                                                                                      floor=selected_floor)
        else:
            list_of_matches_rooms = MDApp.get_running_app().get_room_by_name_fraction(fraction="", floor=selected_floor)

        # undisplay old rooms
        self.ids.room_widget_scrollview.clear_widgets()

        # some function, that adds widget for each match
        number_of_displayed_rooms = 0
        for item in list_of_matches_rooms:
            if number_of_displayed_rooms >= 500:
                break
            number_of_displayed_rooms += 1
            self._add_keywidget(item)

    def _add_keywidget(self, data):
        key_widget = SearchResultWidget()
        key_widget.data = data
        key_widget.ids.searchresultwidget_label_content.text = str(data.name)
        key_widget.label_pointer = key_widget.ids.searchresultwidget_label_content
        self.ids.room_widget_scrollview.add_widget(key_widget)

class PersonSelectionScreen(Screen):

    def __init__(self, **kwargs):
        super(PersonSelectionScreen, self).__init__(**kwargs)
        self.PersonSearchTextInputFunction()  # initial search

    def on_enter(self, *args):
        MDApp.get_running_app().on_resize()
        return super().on_enter(*args)

    def on_leave(self, *args):
        MDApp.get_running_app().on_resize()
        return super().on_leave(*args)

    def PersonSearchTextInputFunction(self):

        # find all relevant examples
        searched_expression = str(self.ids.personsearch.text)
        if len(searched_expression) >= 1:
            list_of_matches_ppl = MDApp.get_running_app().get_person_by_name_fraction(fraction=searched_expression)
        else:
            list_of_matches_ppl = MDApp.get_running_app().get_person_by_name_fraction(fraction="")

        # undisplay old rooms
        self.ids.person_widget_scrollview.clear_widgets()

        # some function, that adds widget for each match
        number_of_displayed_ppl = 0
        for item in list_of_matches_ppl:
            if number_of_displayed_ppl >= 500:
                break
            else:
                number_of_displayed_ppl += 1
                self._add_personwidget(item)

    def _add_personwidget(self, data):
        person_widget = SearchResultWidget()
        person_widget.data = data
        person_widget.ids.searchresultwidget_label_content.text = (f"{str(data.firstname)} {str(data.surname)} (id: {str(data.id)})")
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

    def on_enter(self, *args):
        MDApp.get_running_app().update_review_information()
        MDApp.get_running_app().on_resize()
        return super().on_enter(*args)

    def on_leave(self, *args):
        MDApp.get_running_app().on_resize()
        return super().on_leave(*args)

class AdminScreen(Screen):

    def __init__(self, **kwargs):
        super(AdminScreen, self).__init__(**kwargs)

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

    def on_start(self):
        Clock.schedule_interval(self.update_label, 1)

    def update_label(self, *args):
        try:
            sc_mngr.current_screen.ids.clock.text = f"{datetime.now().hour}:{datetime.now().minute:02d}"
        except:
            pass

        self.on_resize()


    def on_resize(self, *args):
        current_screen = sc_mngr.current_screen
        current = sc_mngr.current

        commands = ["current_screen.ids.user.width=(current_screen.ids.bgcard.width * 0.8)", 
                    "current_screen.ids.user.height=(current_screen.ids.bgcard.height * 0.2)",
                    "current_screen.ids.password.width=(current_screen.ids.bgcard.width * 0.8)", 
                    "current_screen.ids.password.height=(current_screen.ids.bgcard.height * 0.2)",                    
                    "current_screen.ids.login_button.width=(current_screen.ids.bgcard.width * 0.8)", 
                    "current_screen.ids.login_button.height=(current_screen.ids.bgcard.height * 0.2)",
                    "current_screen.ids.pujcit_button.width=(current_screen.ids.bgcard.width * 0.8)", 
                    "current_screen.ids.pujcit_button.height=(current_screen.ids.bgcard.height * 0.35)",
                    "current_screen.ids.vrait_button.width=current_screen.ids.pujcit_button.width", 
                    "current_screen.ids.vrait_button.height=current_screen.ids.pujcit_button.height",
                    "current_screen.ids.borrowingsearch.width=(current_screen.ids.bgcard.width * 0.8)",
                    "current_screen.ids.borrowingsearch.height=(current_screen.ids.bgcard.height * 0.1)",
                    "current_screen.ids.borrowings_widget_scrollview.width=(current_screen.ids.bgcard.width * 0.8)",
                    "current_screen.ids.borrowings_widget_scrollview.height=(current_screen.ids.bgcard.height * 0.7)",
                    "current_screen.ids.storno_button.width=(current_screen.ids.background.width * 0.05)",
                    "current_screen.ids.storno_button.height=(current_screen.ids.background.height * 0.05)",
                    "current_screen.ids.rev_lab_borrower.width=(current_screen.ids.bgcard.width * 0.8)",
                    "current_screen.ids.rev_lab_borrower.height=(current_screen.ids.bgcard.height * 0.175)",
                    "current_screen.ids.rev_lab_key.width=(current_screen.ids.bgcard.width * 0.8)",
                    "current_screen.ids.rev_lab_key.height=(current_screen.ids.bgcard.height * 0.175)",
                    "current_screen.ids.rev_lab_room.width=(current_screen.ids.bgcard.width * 0.8)",
                    "current_screen.ids.rev_lab_room.height=(current_screen.ids.bgcard.height * 0.175)",
                    "current_screen.ids.rev_lab_starttime.width=(current_screen.ids.bgcard.width * 0.8)",
                    "current_screen.ids.rev_lab_starttime.height=(current_screen.ids.bgcard.height * 0.175)",
                    "current_screen.ids.rev_refresh_button.width=(current_screen.ids.bgcard.width * 0.4)",
                    "current_screen.ids.rev_refresh_button.height=(current_screen.ids.bgcard.height * 0.2)",
                    "current_screen.ids.rev_confirm_button.width=(current_screen.ids.bgcard.width * 0.4)",
                    "current_screen.ids.rev_confirm_button.height=(current_screen.ids.bgcard.height * 0.2)"]

        for line in commands:
            try:
                exec(line)
            except:
                pass

 
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
        return self.db.get_person_by_name_fraction(fraction)

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
            self.selected_borrowing = pressed_button_instance.data
            self.return_key(self.selected_borrowing.id)
            sc_mngr.current = "actionselection"
        if sc_mngr.current == "floorselection":
            self.selected_floor = pressed_button_instance.data
            sc_mngr.get_screen("roomselection").SearchRoomTextInputFunction()
            sc_mngr.current = "roomselection"
        elif sc_mngr.current == "roomselection":
            self.selected_room = pressed_button_instance.data
            self.selected_key = pressed_button_instance.data.get_ordinary_key()
            sc_mngr.current = "personselection"
        elif sc_mngr.current == "keyselection":
            self.selected_key = pressed_button_instance.data
            sc_mngr.current = "personselection"
        elif sc_mngr.current == "personselection":
            self.selected_person = pressed_button_instance.data
            sc_mngr.current = "review"
            self.update_review_information()

    def StornoButton(self, *args):
        if sc_mngr.current == "actionselection":
            sc_mngr.current = "login"
        elif sc_mngr.current in [""]:
            sc_mngr.current = "admin"
        elif sc_mngr.current == "admin":
            sc_mngr.current = "login"
        else:
            self.selected_lender = ""
            self.selected_floor = None
            self.selected_room = None
            self.selected_key = None
            self.selected_person = None
            self.selected_starttime = None
            self.selected_endtime_time = None
            self.selected_endtime_date = None
            sc_mngr.current = "actionselection"

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

        global sc_mngr
        sc_mngr = ScreenManager(transition=NoTransition())

        Window.fullscreen = False
        #Window.size = (1920, 1000)
        Window.maximize()
        Window.bind(on_resize=self.on_resize)

        #Config.set('graphics', 'width', '1920')
        #Config.set('graphics', 'height', '1080')

        filename = 'style_vratny.kv'
        filename = resource_find(filename) or filename
        if filename in Builder.files:
            Builder.unload_file(filename)
        Builder.load_file('dev/gui/style_vratny.kv')

        sc_mngr.add_widget(LoginScreen(name="login"))
        sc_mngr.add_widget(ActionSelectionScreen(name="actionselection"))
        sc_mngr.add_widget(BorrowingSelectionScreen(name="borrowingselection"))
        sc_mngr.add_widget(FloorSelectionScreen(name="floorselection"))
        sc_mngr.add_widget(RoomSelectionScreen(name="roomselection"))
        sc_mngr.add_widget(PersonSelectionScreen(name="personselection"))
        sc_mngr.add_widget(ReviewScreen(name="review"))
        sc_mngr.add_widget(AdminScreen(name="admin"))

        self.on_resize()
        return sc_mngr

    def update_review_information(self):
        if sc_mngr.current == "review":
            try:
                ready = True

                self.update_starttime()

                if self.selected_person is None:
                    ready = False
                else:
                    sc_mngr.get_screen("review").ids.rev_lab_borrower.text = f"Komu půjčuje: {self.selected_person.get_full_name()}"
                
                
                if self.selected_key is not None:
                    sc_mngr.get_screen("review").ids.rev_lab_key.text = f"Klíč: {self.selected_key.registration_number}"
                else:
                    ready = False
                    sc_mngr.get_screen("review").ids.rev_lab_key.text = f"Klíč: NEBYL NALEZEN ŽÁDNÝ DOSTUPNÝ KLÍČ"
                
                if self.selected_room is not None:
                    sc_mngr.get_screen("review").ids.rev_lab_room.text = f"Místnost: {self.selected_room.name}"
                else:
                    ready = False
                
                sc_mngr.get_screen("review").ids.rev_lab_starttime.text = str(
                    f"Kdy: {self.selected_starttime.hour}:{self.selected_starttime.minute:02d} "
                    f"{self.selected_starttime.day}. {self.selected_starttime.month}. {self.selected_starttime.year}")
                                 
                if ready:
                    sc_mngr.get_screen("review").ids.rev_confirm_button.disabled = False
                else:
                    sc_mngr.get_screen("review").ids.rev_confirm_button.disabled = True

            except:
                pass

    def complete_borrowing_session(self):
        self.add_borrowing(self.selected_key.id, self.selected_person.id)

        self.selected_lender = ""
        self.selected_floor = None
        self.selected_room = None
        self.selected_key = None
        self.selected_person = None
        self.selected_starttime = None
        self.selected_endtime_time = None
        self.selected_endtime_date = None
        sc_mngr.current = "actionselection"
