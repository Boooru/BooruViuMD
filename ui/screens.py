import copy
import gc
from datetime import datetime
from typing import Union

from kivy import Logger
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.video import Video
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDTextButton
from kivymd.uix.chip import MDChip
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.screen import MDScreen

import assets.strings
from core import caches
from core.caches import provider_cache as providers
from core.structures.Entry import Entry
from core.structures.ImageProvider import ImageProvider
from ui.effects import ImageOverscroll
from ui.widgets import MetaDataImage
from ui.widgets import SwitchArray
from util import provider_util


class ProviderSetupScreen(MDScreen):

    def __init__(self, **kwargs):
        super(ProviderSetupScreen, self).__init__(**kwargs)

        self.layout = MDGridLayout(cols=3, pos_hint={'center_x': 0.5, 'center_y': 0.5})
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
                                            'root scroll screen'].set_provider(arg),
                                        adaptive_size=True,
                                        adaptive_height=True,
                                        adaptive_width=True)

        self.center_col.add_widget(self.switch_array)

        b = MDTextButton(text='Ready!')
        b.adaptive_width = b.adaptive_height = b.adaptive_size = True
        b.on_release = lambda a=None: set_screen('root scroll screen')

        self.right_col.add_widget(b)

        self.layout.add_widget(self.left_col)
        self.layout.add_widget(self.center_col)
        self.layout.add_widget(self.right_col)
        self.add_widget(self.layout)


class RootScrollScreen(MDScreen):

    def __init__(self, **kwargs):
        super(RootScrollScreen, self).__init__(**kwargs)

    def search(self):
        self.ids.image_scroll_view.clear_widgets()

        gc.collect(generation=2)
        self.set_scroller_func()

        self.set_title(providers['root scroll screen'].get_active_provider())

        composition = providers['root scroll screen'].get_active_provider().compose()
        urls = providers['root scroll screen'].get_active_provider().search()

        pane = self.generate_image_pane(urls)

        # Adding GridLayout to ScrollView
        self.ids.image_scroll_view.add_widget(pane)

        if len(pane.children) > 0:
            self.ids.image_scroll_view.scroll_to(pane.children[-1])

    def get_next_page(self, caller=None):
        debug_timer = datetime.now()
        results = providers['root scroll screen'].get_active_provider().more()
        print("get_next_page done with more in " + str(datetime.now() - debug_timer))
        if not results:
            print("No results found!")

        self.generate_image_pane(results, self.ids.image_scroll_view.children[0])

        print("get_next_page done in " + str(datetime.now() - debug_timer))

    def generate_image_pane(self, entries: list, existing_pane=None) -> GridLayout:
        image_pane = GridLayout(cols=3, spacing=0, size_hint=(1, None), pos=(0, 0))
        image_pane.bind(minimum_height=image_pane.setter('height'))
        image_pane.col_default_width = 500
        image_pane.row_default_height = 500

        if existing_pane:
            image_pane = existing_pane
        for entry in entries:
            if entry is None or entry.image_small is None:
                continue
            img = None
            if entry.image_small[-3:] == "mp4":
                print(entry.image_small)
                img = Video(source=entry.image_small)
                pass
            else:
                if entry.image_path and entry.image_path != "":
                    img = MetaDataImage(source=entry.image_path, keep_ratio=True, allow_stretch=True,
                                        extra_headers=providers[
                                            'root scroll screen'].get_active_provider().get_headers(),
                                        meta_data=entry)
                else:
                    img = MetaDataImage(source=entry.image_small, keep_ratio=True, allow_stretch=True,
                                        extra_headers=providers[
                                            'root scroll screen'].get_active_provider().get_headers(),
                                        meta_data=entry)
                img.size_hint = (1, 1)
                meta_data = copy.deepcopy(img.meta_data)
                img.func = lambda a=None: set_big_screen_metadata(self, a,
                                                                  lambda: set_screen('big view screen'))
                image_pane.add_widget(img)
        return image_pane

    def add_tag(self, tag: Union[str, OneLineListItem]):
        text = None
        if type(tag) == str:
            for part in tag.split(" "):
                text = part

                chip = MDChip(text=part)
                chip.icon_right = "close-circle-outline"
                chip.pos_hint = {'center_y': 0.5}
                chip.bind(on_press=self.remove_tag_chip)
                self.ids.tag_container.add_widget(chip)
                providers['root scroll screen'].get_active_provider().add_tag(part)

        elif type(tag) == OneLineListItem:
            text = tag.text
            chip = MDChip(text=text)
            chip.icon_right = "close-circle-outline"
            chip.pos_hint = {'center_y': 0.5}
            chip.bind(on_press=self.remove_tag_chip)
            self.ids.tag_container.add_widget(chip)
            providers['root scroll screen'].get_active_provider().add_tag(text)

    def remove_tag_chip(self, chip: Union[str, MDChip]):
        if type(chip) == MDChip:
            self.ids.tag_container.remove_widget(chip)
            providers['root scroll screen'].get_active_provider().remove_tag(chip.text)
        elif type(chip) == str:
            for child in self.ids.tag_container.children:
                if child.text == chip:
                    self.ids.tag_container.remove_widget(child)
                    providers['root scroll screen'].get_active_provider().remove_tag(chip)

    def clear_chips(self):
        print(str(len(self.ids.tag_container.children)) + " tag chips!")
        while len(self.ids.tag_container.children) > 0:
            self.remove_tag_chip(self.ids.tag_container.children[0])

    def set_scroller_func(self, _=None):
        if self.ids.image_scroll_view.effect_cls != ImageOverscroll:
            self.ids.image_scroll_view.effect_cls = ImageOverscroll
        self.ids.image_scroll_view.effect_cls.func = self.get_next_page

    def set_text_field(self, text: str = ""):
        self.ids.tags.text = text

    def set_title(self, title):

        if type(title) == str:
            self.ids.tool_bar.title = title
        elif isinstance(title, ImageProvider):
            self.ids.tool_bar.title = provider_util.translate(title)

class BigViewScreen(MDScreen):

    def __init__(self, **kwargs):
        super(BigViewScreen, self).__init__(**kwargs)

        self.meta_data: Entry = None
        self.big_image: MetaDataImage = None
        self.tag_scroll: ScrollView = None

    def update_metadata(self, meta_data: Entry):
        if not meta_data:
            Logger.warn("Cannot update screen with null metadata!")
            return

        headers = caches.provider_cache['root scroll screen'].get_active_provider().get_headers()
        new_image = MetaDataImage(source=meta_data.image_full, keep_ratio=True, allow_stretch=True,
                                  extra_headers=headers, meta_data=meta_data)

        self.big_image = new_image
        self.meta_data = meta_data

        app = App.get_running_app()  # get a reference to the running App
        big_view_screen = app.root.ids.screen_manager.get_screen('big view screen')  # get a reference to the MainScreen
        big_view_screen.ids.main_image_container.update_image(new_image)

        container = self.ids.main_image_container
        if self.tag_scroll in container.children:
            container.remove_widget(self.tag_scroll)
        self.generate_tag_scroll()

    def generate_tag_scroll(self):
        container = self.ids.main_image_container

        tag_scroll = ScrollView()
        tag_list = MDList()

        for tag in self.meta_data.tags:
            line_item = OneLineListItem(text=tag)
            root_scroll_screen = App.get_running_app().root.ids.screen_manager.get_screen('root scroll screen')
            line_item.bind(on_press=root_scroll_screen.add_tag)
            tag_list.add_widget(line_item)

        tag_scroll.add_widget(tag_list)
        tag_scroll.do_scroll_x = False
        tag_scroll.do_scroll_y = True
        self.tag_scroll = tag_scroll

    def toggle_tags(self):
        container = self.ids.main_image_container

        if self.tag_scroll in container.children:
            container.remove_widget(self.tag_scroll)

        else:
            container.add_widget(self.tag_scroll)


def set_screen(val):
    app = App.get_running_app()
    app.root.ids.screen_manager.current = val


def set_big_screen_metadata(caller: MDScreen, meta_data: Entry, also=None):
    print("Setting screen..")
    caller.parent.get_screen('big view screen').update_metadata(meta_data)

    if also:
        print("Running also...")
        also()
