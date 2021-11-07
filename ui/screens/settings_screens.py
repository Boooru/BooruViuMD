from kivy.app import App
from kivymd.uix.screen import MDScreen
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.toolbar import MDToolbar

import assets.strings
import core.caches


class SettingsToolbar(MDToolbar):
    pass


class SettingsAppearanceScreen(MDScreen):
    pass


class SettingsProviderScreen(MDScreen):

    def __init__(self, **kwargs):
        super(SettingsProviderScreen, self).__init__(**kwargs)
        self.__switch_elements = [s.lower() + "_switch" for s in assets.strings.ALL_PROVIDERS]

    # Sets the home screen's provider and takes care of misc GUI calls
    def set_provider(self, caller: MDSwitch, provider: str):
        if caller.active: # If the trigger comes from a switch being activated
            self.reset_other_switches(exception=provider)  # Reset the other switches
            core.caches.provider_cache['home screen'].set_provider(provider)  # Set the provider
            App.get_running_app().root.ids.screen_manager.get_screen('home screen').set_title(provider)  # Set the title

    # Sets switches to false
    def reset_other_switches(self, exception: str = None):

        for element in self.__switch_elements:
            if exception and element == (exception.lower() + "_switch"):
                continue

            weak_ref = getattr(self.ids, element)  # Translate the element variable to a reference to the switch
            setattr(weak_ref, "active", False)  # Turn the switch off
