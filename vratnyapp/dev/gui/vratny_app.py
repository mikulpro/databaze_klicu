# python modules
from datetime import datetime

# db api
import os
from pathlib import Path
import importlib.util
# main_folder_path = Path(__file__).resolve().parent
# project_folder_path = main_folder_path.parent
# module_path = os.path.join(project_folder_path, 'sqlite', 'db_interface.py')
# spec = importlib.util.spec_from_file_location('db_interface', module_path)
# module_to_import = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(module_to_import)
# Db = module_to_import.Db

# kivy builder and builder configuration
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.config import Config
from kivy.resources import resource_find
from kivy.clock import Clock
from kivy.logger import Logger

# kivy material design library
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker, MDTimePicker

# kivy basic objects
from kivy.uix.screenmanager import ScreenManager, NoTransition

# kivy import custom screens
# try:
from .admin_screen import AdminScreen
from .admin_authorized_ppl_screen import AdminAuthorizedPplScreen
from .action_selection_screen import ActionSelectionScreen
from .review_screen import ReviewScreen
from .borrowing_selection_screen import BorrowingSelectionScreen
from .floor_selection_screen import FloorSelectionScreen
from .room_selection_screen import RoomSelectionScreen
from .person_selection_screen import PersonSelectionScreen
from .search_result_widget import SearchResultWidget
# except:
#     screens_to_load = [ 'action_selection_screen',
#                     'borrowing_selection_screen',
#                     'floor_selection_screen',
#                     'room_selection_screen',
#                     'person_selection_screen',
#                     'review_screen',
#                     'admin_screen',
#                     'admin_authorized_ppl_screen',
#                     'search_result_widget']
#
#     classes_to_load = ["AdminScreen",
#                        "AdminAuthorizedPplScreen",
#                        "ActionSelectionScreen",
#                        "ReviewScreen",
#                        "BorrowingSelectionScreen",
#                        "FloorSelectionScreen",
#                        "RoomSelectionScreen",
#                        "PersonSelectionScreen",
#                        "SearchResultWidget"]
#
#     for _screen in screens_to_load:
#         main_folder_path = Path(__file__).resolve().parent
#         project_folder_path = main_folder_path.parent
#         module_path = os.path.join(project_folder_path, 'gui', f"{_screen}.py")
#         spec = importlib.util.spec_from_file_location(_screen, module_path)
#         module_to_import = importlib.util.module_from_spec(spec)
#         spec.loader.exec_module(module_to_import)
#         for _class in classes_to_load:
#             try:
#                 exec(f"{_class} = module_to_import.{_class}")
#             except:
#                 pass




class VratnyApp(MDApp):

    def __init__(self, database_object, **kwargs):
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
        self.sc_mngr = None

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
        self.sc_mngr = sc_mngr

        Window.fullscreen = False
        Window.size = (1920, 1000)
        Window.bind(on_resize=self.on_resize)

        filenames = ['action_selection_screen.kv', 
                     'borrowing_selection_screen.kv', 
                     'floor_selection_screen.kv', 
                     'room_selection_screen.kv', 
                     'person_selection_screen.kv', 
                     'review_screen.kv', 
                     'admin_screen.kv', 
                     'admin_authorized_ppl_screen.kv',
                     'search_result_widget.kv']
        
        for _filename in filenames:
            if _filename in Builder.files:
                Builder.unload_file(_filename)
            main_folder_path = Path(__file__).resolve().parent
            project_folder_path = main_folder_path.parent
            module_path = os.path.join(project_folder_path, 'gui', _filename)
            Builder.load_file(module_path)

        sc_mngr.add_widget(ActionSelectionScreen(name="actionselection"))
        sc_mngr.add_widget(BorrowingSelectionScreen(name="borrowingselection"))
        sc_mngr.add_widget(FloorSelectionScreen(name="floorselection"))
        sc_mngr.add_widget(RoomSelectionScreen(name="roomselection"))
        sc_mngr.add_widget(PersonSelectionScreen(name="personselection"))
        sc_mngr.add_widget(ReviewScreen(name="review"))
        sc_mngr.add_widget(AdminScreen(name="admin"))
        sc_mngr.add_widget(AdminAuthorizedPplScreen(name="admin_authorized_ppl"))
        
        sc_mngr.current = "actionselection"
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
