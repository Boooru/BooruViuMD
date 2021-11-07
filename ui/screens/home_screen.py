import copy
import gc
from datetime import datetime
from typing import Union

from kivy.uix.gridlayout import GridLayout
from kivy.uix.video import Video
from kivymd.uix.chip import MDChip
from kivymd.uix.list import OneLineListItem
from kivymd.uix.screen import MDScreen

from core.caches import provider_cache as providers
from core.structures.ImageProvider import ImageProvider
from ui.effects import ImageOverscroll
from ui.screens.screen_util import set_big_screen_metadata, set_screen
from ui.widgets import MetaDataImage
from util import provider_util


class HomeScreen(MDScreen):

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

    def search(self):
        self.ids.image_scroll_view.clear_widgets()

        gc.collect(generation=2)
        self.set_scroller_func()

        self.set_title(providers['home screen'].get_active_provider())

        composition = providers['home screen'].get_active_provider().compose()
        urls = providers['home screen'].get_active_provider().search()

        pane = self.generate_image_pane(urls)

        # Adding GridLayout to ScrollView
        self.ids.image_scroll_view.add_widget(pane)

        if len(pane.children) > 0:
            self.ids.image_scroll_view.scroll_to(pane.children[-1])

    def get_next_page(self, caller=None):
        debug_timer = datetime.now()
        results = providers['home screen'].get_active_provider().more()
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
                                            'home screen'].get_active_provider().get_headers(),
                                        meta_data=entry)
                else:
                    img = MetaDataImage(source=entry.image_small, keep_ratio=True, allow_stretch=True,
                                        extra_headers=providers[
                                            'home screen'].get_active_provider().get_headers(),
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
                providers['home screen'].get_active_provider().add_tag(part)

        elif type(tag) == OneLineListItem:
            text = tag.text
            chip = MDChip(text=text)
            chip.icon_right = "close-circle-outline"
            chip.pos_hint = {'center_y': 0.5}
            chip.bind(on_press=self.remove_tag_chip)
            self.ids.tag_container.add_widget(chip)
            providers['home screen'].get_active_provider().add_tag(text)

    def remove_tag_chip(self, chip: Union[str, MDChip]):
        if type(chip) == MDChip:
            self.ids.tag_container.remove_widget(chip)
            providers['home screen'].get_active_provider().remove_tag(chip.text)
        elif type(chip) == str:
            for child in self.ids.tag_container.children:
                if child.text == chip:
                    self.ids.tag_container.remove_widget(child)
                    providers['home screen'].get_active_provider().remove_tag(chip)

    def clear_chips(self):
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