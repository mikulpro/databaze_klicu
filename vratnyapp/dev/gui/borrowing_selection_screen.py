from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

try:
    import search_result_widget
except:
    import os
    from pathlib import Path
    import importlib.util
    main_folder_path = Path(__file__).resolve().parent
    project_folder_path = main_folder_path.parent
    module_path = os.path.join(project_folder_path, 'gui', 'search_result_widget.py')
    spec = importlib.util.spec_from_file_location('search_result_widget', module_path)
    search_result_widget = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(search_result_widget)  


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
        borrowing_widget = search_result_widget.SearchResultWidget()
        borrowing_widget.change_text(str(data.authorization.person.get_full_name()) + "   " + str(data.key.room.name) + "   " +  str(data.borrowed))
        borrowing_widget.label_pointer = borrowing_widget.ids.searchresultwidget_label_content
        borrowing_widget.data = data
        self.ids.borrowings_widget_scrollview.add_widget(borrowing_widget)