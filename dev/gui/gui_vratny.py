# python modules
import time
import logging
from datetime import datetime
from dev.sqlite.db_interface import Db

# kivy builder and builder configuration
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.config import Config
from kivy.resources import resource_find
from kivy.clock import Clock
from kivy.logger import Logger

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

class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        MDApp.get_running_app().on_resize()
        return super().on_enter(*args)

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
        
        user = MDApp.get_running_app().db.get_user_by_username(username)
        if user is not None and user.check_password(password):
            MDApp.get_running_app().set_lender(username)
            if user.is_superuser:
                sc_mngr.current = "admin"
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

    def on_enter(self, *args):
        self.SearchBorrowingTextInputFunction()
        MDApp.get_running_app().on_resize()
        return super().on_enter(*args)

    def on_leave(self, *args):
        MDApp.get_running_app().on_resize()
        return super().on_leave(*args)

    def SearchBorrowingTextInputFunction(self):
        borrowings = MDApp.get_running_app().db.get_ongoing_borrowings()

        # undisplaying old
        self.ids.borrowings_widget_scrollview.clear_widgets()

        if borrowings is not []:
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

    def on_enter(self, *args):
        self.SearchFloorTextInputFunction(initial=True)
        MDApp.get_running_app().on_resize()
        return super().on_enter(*args)

    def on_leave(self, *args):
        MDApp.get_running_app().on_resize()
        return super().on_leave(*args)

    def SearchFloorTextInputFunction(self, initial=False):
        floors = MDApp.get_running_app().db.get_all_floors()
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

    def on_enter(self, *args):
        self.SearchRoomTextInputFunction()
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
            list_of_matches_rooms = MDApp.get_running_app().\
                db.search_rooms_availability_dict_by_floor(expression=searched_expression, floor=selected_floor)
        else:
            list_of_matches_rooms = MDApp.get_running_app().db.get_rooms_availability_dict_by_floor(floor=selected_floor)

        available_rooms = list_of_matches_rooms["available"]
        unavailable_rooms = list_of_matches_rooms["unavailable"]

        # undisplay old rooms
        self.ids.room_widget_scrollview.clear_widgets()

        # some function, that adds widget for each match
        number_of_displayed_rooms = 0
        for item in available_rooms:
            if number_of_displayed_rooms >= 500:
                break
            number_of_displayed_rooms += 1
            self._add_keywidget(item, False)

        for item in unavailable_rooms:
            if number_of_displayed_rooms >= 500:
                break
            number_of_displayed_rooms += 1
            self._add_keywidget(item, True)

    def _add_keywidget(self, data, disabled):
        key_widget = SearchResultWidget()
        key_widget.data = data
        key_widget.ids.searchresultwidget_label_content.text = str(data.name)
        key_widget.label_pointer = key_widget.ids.searchresultwidget_label_content
        self.ids.room_widget_scrollview.add_widget(key_widget)
        key_widget.disabled = disabled
        # if data.get_borrowable_key() is None:
        #     key_widget.disabled = True

class PersonSelectionScreen(Screen):

    def __init__(self, **kwargs):
        super(PersonSelectionScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        MDApp.get_running_app().on_resize()
        self.PersonSearchTextInputFunction()
        return super().on_enter(*args)

    def on_leave(self, *args):
        MDApp.get_running_app().on_resize()
        return super().on_leave(*args)

    def PersonSearchTextInputFunction(self):

        list_of_matches = []
        if MDApp.get_running_app().selected_room is not None:
            authorizations = MDApp.get_running_app().db.get_prioritized_authorizations_for_room(MDApp.get_running_app().selected_room.id)

            # find all relevant examples
            searched_expression = str(self.ids.personsearch.text)

            for authorization in authorizations:
                if searched_expression in str(authorization.person.get_full_name()):
                    list_of_matches.append(authorization)

        # undisplay old rooms
        self.ids.person_widget_scrollview.clear_widgets()

        # some function, that adds widget for each match
        number_of_displayed_ppl = 0
        for item in list_of_matches:
            if number_of_displayed_ppl >= 500:
                break
            else:
                number_of_displayed_ppl += 1
                self._add_personwidget(item)

    def _add_personwidget(self, data):
        person_widget = SearchResultWidget()
        person_widget.data = data
        person_widget.ids.searchresultwidget_label_content.text = (f"{str(data.person.firstname)} {str(data.person.surname)} (pracoviště: {str(data.person.workplace) if data.person.workplace else ''})")
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

class AdminAuthorizedPersonWidget(GridLayout):

    def __init__(self, **kwargs):
        super(AdminAuthorizedPersonWidget, self).__init__(**kwargs)
        self.data = None

    def edit(self, instance):
        pass

    def delete(self, instance):
        MDApp.get_running_app().db.invalidate_authorization_obj(instance.data)
        instance.parent.remove_widget(instance)


class AdminScreen(Screen):

    def __init__(self, **kwargs):
        super(AdminScreen, self).__init__(**kwargs)

    def admin_func_1(self):
        sc_mngr.current = "admin_authorized_ppl"
    
    def admin_func_2(self):
        pass

    def admin_func_3(self):
        sc_mngr.get_screen("admin_authorized_ppl").admin_authorise_new_person()

class AdminAuthorizedPplScreen(Screen):

    def __init__(self, **kwargs):
        super(AdminAuthorizedPplScreen, self).__init__(**kwargs)

    def change_to_loading(self):
        sc_mngr.current = "loading"

    def on_enter(self, *args):
        self.display_authorizations()
        return super().on_enter(*args)

    def display_authorizations(self):
        searched_expression = ""
        
        searched_expression = str(sc_mngr.get_screen("admin_authorized_ppl").ids.admin_auth_ppl_search.text)
        
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

class VratnyApp(MDApp):

    def __init__(self, database_object=Db(), **kwargs):
        super(VratnyApp, self).__init__(**kwargs)
        self.selected_lender = ""
        self.selected_floor = None
        self.selected_room = None
        self.selected_key = None
        self.selected_authorization = None
        self.selected_starttime = None
        self.selected_endtime_time = None
        self.selected_endtime_date = None
        self.selected_borrowing = None
        self.db = database_object
        self.preloaded_auths = []
        self.return_screen = "login"
        self.number_of_auths_to_load = 1

        # Load config file
        Config.read('kivy.config')
        Logger.warning('Vratny app: Log level nastaven na debug')


    def on_start(self):
        Clock.schedule_interval(self.update_label, 2)

    def update_label(self, *args):
        try:
            sc_mngr.current_screen.ids.clock.text = f"{datetime.now().hour}:{datetime.now().minute:02d}"
        except:
            pass
        
        self.on_resize()
        
        if self.preloaded_auths == []:
            self.preload_auths(return_screen=self.return_screen, number_of_auths=self.number_of_auths_to_load)
            self.return_screen = "login"
            self.number_of_auths_to_load = 300

    def preload_auths_again(self):
        sc_mngr.current = "loading"
        self.return_screen = "admin_authorized_ppl"
        self.number_of_auths_to_load = 600
        self.preloaded_auths = []

    def preload_auths(self, return_screen="login", number_of_auths=1):
        Logger.info("Admin app: Nacitani auths zacalo")
        sc_mngr.current_screen = sc_mngr.get_screen("loading")
        self.preloaded_auths = []
        instructions = self.db.get_all_authorizations_screen()
        counter = 0
        for item in instructions:
            if counter >= number_of_auths:
                break
            widget = AdminAuthorizedPersonWidget()
            widget.data = item
            # (1746, 'Jan', 'Novák', 'admin', datetime.datetime(2022, 12, 9, 13, 51, 59, 762329), datetime.datetime(2023, 3, 19, 13, 51, 59, 430651), 'CP-5.24')
            widget.ids.name.text = item[1] + " " + item[2]
            widget.ids.authorized_by.text = item[3]

            widget.ids.time.text = item[4].strftime("%d.%m.%Y %H:%M")
            widget.ids.time2.text = item[5].strftime("%d.%m.%Y %H:%M")
            widget.ids.room.text = str(item[6])
            # widget.ids.name.text = str(item.person.get_full_name())
            # if item.origin_id == "1" or item.origin_id == 1:
            #     widget.ids.authorized_by.text = "admin"
            # else:
            #     widget.ids.authorized_by.text = "systém"
            # widget.ids.time.text = str(item.created)
            # widget.ids.time2.text = str(item.expiration)
            # widget.ids.room.text = str(item.room.name)
            self.preloaded_auths.append(widget)
            counter += 1
        Logger.info('Admin app: Nacteni auths dokonceno')
        sc_mngr.current = return_screen

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
            self.db.return_key(self.selected_borrowing.id)
            key = self.selected_borrowing.key
            Logger.info(f"Vratny app: "
                        f"[{datetime.utcnow().strftime('%d.%m.%Y %H:%M')}] "
                        f"Vrácen klíč {key.registration_number} "
                        f"od místnosti {key.room.name} "
                        f"osobou {self.selected_borrowing.authorization.person.get_full_name()}")
            sc_mngr.current = "actionselection"
        if sc_mngr.current == "floorselection":
            self.selected_floor = pressed_button_instance.data
            sc_mngr.get_screen("roomselection").SearchRoomTextInputFunction()
            sc_mngr.current = "roomselection"
        elif sc_mngr.current == "roomselection":
            self.selected_room = pressed_button_instance.data
            self.selected_key = pressed_button_instance.data.get_borrowable_key()
            sc_mngr.current = "personselection"
        elif sc_mngr.current == "keyselection":
            self.selected_key = pressed_button_instance.data
            sc_mngr.current = "personselection"
        elif sc_mngr.current == "personselection":
            self.selected_authorization = pressed_button_instance.data
            sc_mngr.current = "review"
            self.update_review_information()

    def StornoButton(self, *args):
        if sc_mngr.current == "actionselection":
            sc_mngr.current = "login"
        elif sc_mngr.current in ["admin_authorized_ppl"]:
            sc_mngr.current = "admin"
        elif sc_mngr.current == "admin":
            sc_mngr.current = "login"
        else:
            self.selected_lender = ""
            self.selected_floor = None
            self.selected_room = None
            self.selected_key = None
            self.selected_authorization = None
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
        Window.size = (1920, 1000)
        #Window.maximize()
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
        sc_mngr.add_widget(AdminAuthorizedPplScreen(name="admin_authorized_ppl"))

        # !!! LoadingScreen has to be added last
        sc_mngr.add_widget(LoadingScreen(name="loading"))
        sc_mngr.current = "loading"
        self.on_resize()
        return sc_mngr

    def update_review_information(self):
        if sc_mngr.current == "review":
            try:
                ready = True

                self.update_starttime()

                if self.selected_authorization is None:
                    ready = False
                else:
                    sc_mngr.get_screen("review").ids.rev_lab_borrower.text = f"Komu půjčuje: {self.selected_authorization.person.get_full_name()}"
                
                
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
        self.db.add_borrowing(self.selected_key.id, self.selected_authorization.id)
        Logger.info(f"Vratny app: "
                    f"[{datetime.utcnow().strftime('%d.%m.%Y %H:%M')}] "
                    f"Vypůjčen klíč {self.selected_key.registration_number} "
                    f"od místnosti {self.selected_key.room.name} "
                    f"osobě {self.selected_authorization.person.get_full_name()}")

        self.selected_lender = ""
        self.selected_floor = None
        self.selected_room = None
        self.selected_key = None
        self.selected_authorization = None
        self.selected_starttime = None
        self.selected_endtime_time = None
        self.selected_endtime_date = None
        sc_mngr.current = "actionselection"
