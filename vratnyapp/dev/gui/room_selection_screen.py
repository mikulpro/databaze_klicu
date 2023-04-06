from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from .search_result_widget import SearchResultWidget


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