from kivy.uix.boxlayout import BoxLayout


class SearchResultWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(SearchResultWidget, self).__init__(**kwargs)
        self.label_pointer = None
        self.data = None

    def change_text(self, text):
        self.ids.searchresultwidget_label_content.text = text