from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp


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
            MDApp.get_running_app().sc_mngr.current = "review"