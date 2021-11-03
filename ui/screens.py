import copy
import gc

from kivy.uix.gridlayout import GridLayout
from kivy.uix.video import Video
from kivymd.material_resources import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDTextButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList
from kivymd.uix.screen import MDScreen

import assets.strings
import core.caches
from core import caches
from ui.widgets import SwitchArray

from ui.widgets import MetaDataImage
from core.caches import provider_cache as providers


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


        self.center_col.add_widget(MDLabel(text="Provider", adaptive_height=True, adaptive_size=True, adaptive_width=True))

        self.switch_array = SwitchArray(labels=assets.strings.ALL_PROVIDERS,
                                        active_func=lambda arg: caches.provider_cache[
                                            'root scroll screen'].set_provider(arg),
                                        adaptive_size=True,
                                        adaptive_height=True,
                                        adaptive_width=True)

        self.center_col.add_widget(self.switch_array)

        b = MDTextButton(text='Ready!')
        b.adaptive_width = b.adaptive_height = b.adaptive_size = True
        b.on_release = lambda a=None: set_val(self, 'root scroll screen')

        self.right_col.add_widget(b)

        self.layout.add_widget(self.left_col)
        self.layout.add_widget(self.center_col)
        self.layout.add_widget(self.right_col)
        self.add_widget(self.layout)

def set_val(target, val):
    target.parent.current = val


class RootScrollScreen(MDScreen):

    def __init__(self, **kwargs):
        super(RootScrollScreen, self).__init__(**kwargs)

    def search(self):
        self.ids.image_scroll_view.clear_widgets()
        gc.collect(generation=2)

        providers['root scroll screen'].get_active_provider().clear_tags()

        if self.ids.tags.text != "":
            providers['root scroll screen'].get_active_provider().add_tags_from_string(
                self.ids.tags.text)

        composition = providers['root scroll screen'].get_active_provider().compose()
        urls = providers['root scroll screen'].get_active_provider().search()

        pane = self.generate_image_pane(urls)

        # Adding GridLayout to ScrollView
        self.ids.image_scroll_view.add_widget(pane)
        self.ids.image_scroll_view.scroll_to(pane.children[-1])

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
                #img.func = self.launch_big_viewer
                image_pane.add_widget(img)
        return image_pane
