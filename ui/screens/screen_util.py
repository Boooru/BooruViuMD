from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDTextButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

import assets.strings
from core import caches
from core.structures.Entry import Entry
from ui.widgets import SwitchArray


class ProviderSetupScreen(MDScreen):

    def __init__(self, **kwargs):
        super(ProviderSetupScreen, self).__init__(**kwargs)

        self.layout = GridLayout(cols=3, pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(1, 1))
        self.left_col = MDBoxLayout(orientation='vertical')
        self.center_col = MDBoxLayout(orientation='vertical')
        self.right_col = MDBoxLayout(orientation='vertical')

        self.left_col.pos_hint = self.right_col.pos_hint = self.center_col.pos_hint = {'center_y': 0.5}
        self.left_col.adaptive_size = self.left_col.adaptive_height = self.left_col.adaptive_width = True
        self.right_col.adaptive_size = self.right_col.adaptive_height = self.right_col.adaptive_width = True
        self.center_col.adaptive_size = self.center_col.adaptive_height = self.center_col.adaptive_width = True

        self.center_col.add_widget(
            MDLabel(text="Provider", adaptive_height=True, adaptive_size=True, adaptive_width=True))

        self.switch_array = SwitchArray(labels=assets.strings.ALL_PROVIDERS,
                                        active_func=lambda arg: caches.provider_cache[
                                            'home screen'].set_provider(arg),
                                        adaptive_size=True,
                                        adaptive_height=True,
                                        adaptive_width=True)

        self.center_col.add_widget(self.switch_array)

        b = MDTextButton(text='Ready!')
        b.adaptive_width = b.adaptive_height = b.adaptive_size = True
        b.on_release = lambda a=None: set_screen('home screen')

        self.right_col.add_widget(b)

        self.layout.add_widget(self.left_col)
        self.layout.add_widget(self.center_col)
        self.layout.add_widget(self.right_col)
        self.add_widget(self.layout)


def set_screen(val):
    app = App.get_running_app()
    app.root.ids.screen_manager.current = val


def set_big_screen_metadata(caller: MDScreen, meta_data: Entry, also=None):
    print("Setting screen..")
    caller.parent.get_screen('big view screen').update_metadata(meta_data)

    if also:
        print("Running also...")
        also()
