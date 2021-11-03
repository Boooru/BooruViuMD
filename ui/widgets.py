from kivy import Logger
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage, Image
from kivy.uix.label import Label
from kivymd.material_resources import dp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList
from kivymd.uix.selectioncontrol import MDSwitch

import main
from ui.common_gestures.commongestures import CommonGestures

from core.structures.Entry import Entry


class ClickableAsyncImage(CommonGestures, AsyncImage):
    pass


class MetaDataImage(CommonGestures, AsyncImage):
    def __init__(self, meta_data=Entry(), func=None, **kwargs):
        super().__init__(**kwargs)

        print("Got metadata! " + str(meta_data.image_full))
        self.meta_data = meta_data
        self.func = func

    def cg_tap(self, touch, x, y):
        if self.func:
            self.func(self.meta_data)

    def cg_long_press(self, touch, x, y):
        if self.meta_data and self.meta_data.image_full:
            main.async_downloader.submit_url(self.meta_data.image_full, headers=self.meta_data.headers)
        else:
            Logger.warn("Can't save image with url: " + str(self.meta_data.image_full))


class FuncButton(CommonGestures, Label):
    pass


class FuncImageButton(CommonGestures, Image):
    pass


# A CheckBox that contains an internal text field.
class LabeledCheckBox(CheckBox):
    text: str = ""


# An array of checkboxes. When exclusive is set to true, only one may be selected at a time
class CheckBoxArray(GridLayout):

    def __init__(self, labels: list[str], title: str = None, exclusive: bool = True, on_select=None, **kwargs):

        super().__init__(**kwargs)
        self.cols = 1

        self.__exclusive = exclusive
        self.__label_map = {}

        self.on_select = on_select  # An auxiliary function that can be called whenever any box gets checked
        self.__grid = GridLayout(cols=2, size_hint=(1, 1))  # Main grid layout

        if title:
            self.add_widget(Label(text=title))

        for label in labels:
            self.create_child(label)

        self.add_widget(self.__grid)

    # Add a new checkbox/label pair
    def create_child(self, text: str):
        label = Label(text=text)  # Generate label
        check = LabeledCheckBox()  # Generate check box
        check.text = label.text  # Set the check box's internal text field to the label's text field
        check.bind(active=self.activate)  # Bind the activation function

        # Add box widgets to the outer layout
        self.__grid.add_widget(label)
        self.__grid.add_widget(check)

        self.__label_map[label.text] = check

    # Run each time a box gets checked
    def activate(self, caller: LabeledCheckBox, _):
        if self.__exclusive:
            for child in self.__label_map.values():
                if child is not caller:
                    child.active = False

        if self.on_select is not None and len(self.all_active()) > 0:  # If on_select was set, run it
            print("Running on_select!")
            self.on_select(self.all_active())

    def set_active(self, label_text: str):
        if label_text in self.__label_map:
            self.__label_map[label_text].active = True
        else:
            print("check_array couldn't find " + label_text + " in " + str(self.__label_map))

    # Get the text associated with all checked boxes
    def all_active(self) -> list[str]:
        labels = []
        for child in self.children[0].children:
            if type(child) == LabeledCheckBox and child.active:
                labels.append(child.text)
        print("All active: " + str(labels))
        return labels


class LabeledSwitch(MDGridLayout):
    def __init__(self, text: str = "", active_func=None, inactive_func=None, callback=None, **kwargs):
        super(LabeledSwitch, self).__init__(**kwargs)

        self.cols = 2
        self.padding = dp(5)
        self.spacing = dp(5)

        self.text = text

        self.active_func = active_func
        self.inactive_func = inactive_func
        self.callback = callback

        self.label = MDLabel(text=self.text)
        self.label.adaptive_width = self.label.adaptive_height = self.label.adaptive_size = True

        self.switch = MDSwitch()
        self.switch.on_release = lambda a=None: self.delegate(self.switch.active, self.text)

        self.add_widget(self.label)
        self.add_widget(self.switch)

    def delegate(self, switch_status, arg):
        if switch_status:
            if self.active_func:
                self.active_func(arg)
                if self.callback:
                    self.callback(self)
        else:
            if self.inactive_func:
                self.inactive_func(arg)


class SwitchArray(MDList):
    def __init__(self, labels: list[str], active_func=None, inactive_func=None, **kwargs):
        super(SwitchArray, self).__init__(**kwargs)

        self.adaptive_width = True

        for label in labels:
            print(f"Adding label {label}")
            self.add_widget(LabeledSwitch(text=label, active_func=active_func,
                                          inactive_func=inactive_func,
                                          callback=self.disable_all,
                                          adaptive_width=True,
                                          adaptive_height=True,
                                          adaptive_size=True))

    def disable_all(self, other_than):
        for child in self.children:
            for sub_child in child.children:
                if type(sub_child) == MDSwitch:
                    if other_than and sub_child == other_than.switch:
                        continue

                    sub_child.active = False
