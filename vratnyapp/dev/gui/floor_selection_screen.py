from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

# try:
from dev.gui.search_result_widget import SearchResultWidget
# except:
#     import os
#     from pathlib import Path
#     import importlib.util
#     main_folder_path = Path(__file__).resolve().parent
#     project_folder_path = main_folder_path.parent
#     module_path = os.path.join(project_folder_path, 'gui', 'search_result_widget.py')
#     spec = importlib.util.spec_from_file_location('search_result_widget', module_path)
#     module_to_import = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module_to_import)
#     SearchResultWidget = module_to_import.SearchResultWidget
    

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