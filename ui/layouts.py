from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget


class DataGridLayout(GridLayout, ButtonBehavior):
    def __init__(self, **kwargs):
        super(DataGridLayout, self).__init__(**kwargs)
        self.data = {}


class ClickableBoxLayout(Widget, ButtonBehavior):

    def __init__(self, orientation="vertical", **kwargs):
        super().__init__(**kwargs)
        self.data = {}

        self.root = BoxLayout(size_hint=(1, 1))
        super().add_widget(self.root)
        self.root.orientation = orientation

    def add_widget(self, widget, index=0, canvas=None):
        self.root.add_widget(widget, index, canvas)

    def get_root(self):
        return self.root

    def remove_widget(self, widget):
        self.root.remove_widget(widget)
