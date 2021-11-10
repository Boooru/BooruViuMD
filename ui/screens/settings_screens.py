from kivy.app import App
from kivymd.uix.list import OneLineListItem
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

    # Sets the home screen's provider and takes care of misc GUI calls
    def set_provider(self, caller: MDSwitch, provider: str):
        if caller.active:  # If the trigger comes from a switch being activated
            self.reset_other_switches(exception=provider)  # Reset the other switches
            util.provider_util.set_provider(provider)  # Set the provider
            App.get_running_app().root.ids.screen_manager.get_screen('home screen').set_title(provider)  # Set the title

    # Sets switches to false
    def reset_other_switches(self, exception: str = None):

        for element in self.__switch_elements:
            if exception and element == (exception.lower() + "_switch"):
                continue

            weak_ref = getattr(self.ids, element)  # Translate the element variable to a reference to the switch
            setattr(weak_ref, "active", False)  # Turn the switch off


def open_booru_config_screen(provider: str):
    config_screen = App.get_running_app().root.ids.screen_manager.get_screen('settings booru config screen')
    config_screen.prepare(provider)
    App.get_running_app().root.ids.screen_manager.current = 'settings booru config screen'



class SettingsBooruConfigScreen(MDScreen):

    def __init__(self, **kwargs):
        super(SettingsBooruConfigScreen, self).__init__(**kwargs)
        self.provider = None

    def set_target(self, provider: str):
        self.provider = provider

    def get_tags(self):
        if 'tags' in core.caches.user_rules[self.provider]:
            return core.caches.user_rules[self.provider]['tags']

        return ""

    def get_blacklist(self):
        if 'blacklist' in core.caches.user_rules[self.provider]:
            return core.caches.user_rules[self.provider]['blacklist']

        return ""

    def get_limit(self):
        if 'limit' in core.caches.user_rules[self.provider]:
            return core.caches.user_rules[self.provider]['limit']

        return 10

    def __generate_tag_list_item(self, tag: str):
        l_i = OneLineListItem(text=tag)
        l_i.bind(on_press=self.remove_tag)
        return l_i

    def __generate_blacklist_item(self, tag: str):
        l_i = OneLineListItem(text=tag)
        l_i.bind(on_press=self.remove_blacklist_tag)
        return l_i

    def prepare(self, provider: str):
        self.set_target(provider)

        if provider not in core.caches.user_rules:
            core.caches.user_rules[provider] = {}

        tags_list = self.ids.tag_list
        blacklist_list = self.ids.blacklist_list

        tags_list.clear_widgets()
        blacklist_list.clear_widgets()

        for tag in self.get_tags().split(" "):
            tags_list.add_widget(self.__generate_tag_list_item(tag))

        for tag in self.get_blacklist().split(" "):
            print("Adding tag to blacklist: " + tag)
            blacklist_list.add_widget(self.__generate_blacklist_item(tag))

    def add_tag(self, tag: str):
        if 'tags' not in core.caches.user_rules[self.provider]:
            core.caches.user_rules[self.provider]['tags'] = ""

        old_tags = core.caches.user_rules[self.provider]['tags']
        core.caches.user_rules[self.provider]['tags'] = old_tags + " " + tag

        tag_list = self.ids.tag_list
        tag_list.add_widget(self.__generate_tag_list_item(tag))

    def add_blacklist_tag(self, tag: str):
        if 'blacklist' not in core.caches.user_rules[self.provider]:
            core.caches.user_rules[self.provider]['blacklist'] = ""

        old_tags = core.caches.user_rules[self.provider]['blacklist']
        core.caches.user_rules[self.provider]['blacklist'] = old_tags + " " + tag

        blacklist_list = self.ids.blacklist_list
        blacklist_list.add_widget(self.__generate_blacklist_item(tag))

    def remove_tag(self, list_item):
        old_b_list = core.caches.user_rules[self.provider]['tags'].split(" ")
        old_b_list.remove(list_item.text)
        core.caches.user_rules[self.provider]['tags'] = " ".join(old_b_list)
        self.ids.tag_list.remove_widget(list_item)

    def remove_blacklist_tag(self, list_item):
        old_b_list = core.caches.user_rules[self.provider]['blacklist'].split(" ")
        old_b_list.remove(list_item.text)
        core.caches.user_rules[self.provider]['blacklist'] = " ".join(old_b_list)
        self.ids.blacklist_list.remove_widget(list_item)

    def pack_tag(self, caller):
        self.add_tag(caller.text)
        caller.text = ""

    def pack_blacklist(self, caller):
        self.add_blacklist_tag(caller.text)
        caller.text = ""