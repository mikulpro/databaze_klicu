from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from .search_result_widget import SearchResultWidget


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
        #person_widget.ids.searchresultwidget_label_content.text = (f"{str(data.person.firstname)} {str(data.person.surname)} (pracoviště: {str(data.person.workplace) if data.person.workplace else ''})")
        person_widget.ids.searchresultwidget_label_content.text = (f"{str(data.person.firstname)} {str(data.person.surname)} | {str(data.person.workplace.abbreviation) if data.person.workplace else ''}")
        person_widget.label_pointer = person_widget.ids.searchresultwidget_label_content
        self.ids.person_widget_scrollview.add_widget(person_widget)