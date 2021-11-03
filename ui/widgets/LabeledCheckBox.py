from abc import ABCMeta, ABC

from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivymd.uix import MDAdaptiveWidget
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDCheckbox, MDSwitch


class LabeledCheckBox(MDGridLayout):

    def __init__(self, text: str = "", on_select=None, on_deselect=None, **kwargs):
        super().__init__(**kwargs)

        self.on_select = on_select
        self.on_deselect = on_deselect
        self.text = text

        self.cols = 2
        self.adaptive_height = True
        self.adaptive_width = True
        self.adaptive_size = True

        self.lb = MDLabel(adaptive_size=True, text=text)
        self.switch = MDSwitch()

        self.switch.on_press = lambda a=None, b=None: delegate(self.switch.active, self.text)
        self.switch.adaptive_size = True
        self.switch.adaptive_width = self.switch.adaptive_height = False

        self.add_widget(self.lb)
        self.add_widget(self.switch)

        def delegate(switch_state, args):
            if not switch_state:
                on_select(args)
            else:
                on_deselect(args)
