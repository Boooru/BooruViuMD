from kivymd.uix.screen import MDScreen
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.toolbar import MDToolbar

import assets.strings
import core.caches
import util.provider_util


class SettingsToolbar(MDToolbar):
    pass


class SettingsAppearanceScreen(MDScreen):
    pass


class SettingsProviderScreen(MDScreen):

    def __init__(self, **kwargs):
        super(SettingsProviderScreen, self).__init__(**kwargs)

        self.__switch_elements = [s.lower() + "_switch" for s in assets.strings.ALL_PROVIDERS]

    def set_provider(self, caller: MDSwitch, provider: str):
        if caller.active:
            self.reset_other_switches(exception=provider)
            core.caches.provider_cache['root scroller provider'] = util.provider_util.translate(provider)()

    def reset_other_switches(self, exception: str = None):

        for element in self.__switch_elements:
            if exception and element == (exception.lower() + "_switch"):
                continue

            weak_ref = getattr(self.ids, element)
            setattr(weak_ref, "active", False)
