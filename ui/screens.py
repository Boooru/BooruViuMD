import copy
import gc

from kivy import Logger
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.video import Video
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDTextButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

import assets.strings
from core import caches
from core.caches import provider_cache as providers
from core.structures.Entry import Entry
from ui.widgets import MetaDataImage
from ui.widgets import SwitchArray


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
                img.func = lambda a=None: set_big_screen_metadata(self, a,
                                                                  lambda: set_screen('big view screen'))
                image_pane.add_widget(img)
        return image_pane


class BigViewScreen(MDScreen):

    def __init__(self, **kwargs):
        super(BigViewScreen, self).__init__(**kwargs)

        self.meta_data: Entry = None

    def update_metadata(self, meta_data: Entry):
        if not meta_data:
            Logger.warn("Cannot update screen with null metadata!")
            return

        print("Updating...")
        print("Metadata: " + str(meta_data.as_dict()))
        headers = caches.provider_cache['root scroll screen'].get_active_provider().get_headers()
        new_image = MetaDataImage(source=meta_data.image_full, keep_ratio=True, allow_stretch=True,
                                  extra_headers=headers, meta_data=meta_data)

        print("Metadata: " + str(new_image.meta_data.as_dict()))

        app = App.get_running_app()  # get a reference to the running App
        big_view_screen = app.root.ids.screen_manager.get_screen('big view screen')  # get a reference to the MainScreen
        big_view_screen.ids.main_image_container.update_image(new_image)


def set_screen(val):
    app = App.get_running_app()
    app.root.ids.screen_manager.current = val


def set_big_screen_metadata(caller: MDScreen, meta_data: Entry, also=None):
    print("Setting screen..")
    caller.parent.get_screen('big view screen').update_metadata(meta_data)

    if also:
        print("Running also...")
        also()
