from kivy.app import App
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

import assets.strings
import core.caches
import util.utils
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


def build_provider_menu(caller):
    menu_items = []
    for provider in assets.strings.ALL_PROVIDERS:
        item = {"text": provider, "viewclass": "OneLineListItem",
                "on_release": lambda prov=provider: util.utils.set_provider(prov)}

        menu_items.append(item)

    return MDDropdownMenu(caller=caller, items=menu_items, width_mult=2)


def build_mode_menu(caller):
    menu_items = []
    for mode in core.caches.provider_cache['home screen'].get_active_provider().modes:
        item = {"text": mode,
                "viewclass": "OneLineListItem",
                "on_release": lambda m=mode: core.caches.provider_cache['home screen'].set_provider_mode(m)
        }

        menu_items.append(item)

    return MDDropdownMenu(caller=caller, items=menu_items, width_mult=2)
