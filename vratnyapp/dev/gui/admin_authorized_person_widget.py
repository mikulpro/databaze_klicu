from kivy.uix.gridlayout import GridLayout
from kivymd.app import MDApp


class AdminAuthorizedPersonWidget(GridLayout):

    def __init__(self, **kwargs):
        super(AdminAuthorizedPersonWidget, self).__init__(**kwargs)
        self.data = None

    def edit(self, instance):
        pass

    def delete(self, instance):
        MDApp.get_running_app().db.invalidate_authorization_obj(instance.data)
        instance.parent.remove_widget(instance)