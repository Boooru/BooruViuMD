from kivy.app import App
from kivymd.uix.screen import MDScreen

from core.structures.Entry import Entry


def set_screen(val):
    app = App.get_running_app()
    app.root.ids.screen_manager.current = val


def set_big_screen_metadata(caller: MDScreen, meta_data: Entry, also=None):
    print("Setting screen..")
    caller.parent.get_screen('big view screen').update_metadata(meta_data)

    if also:
        print("Running also...")
        also()
