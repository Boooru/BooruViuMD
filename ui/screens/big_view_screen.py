from kivy import Logger
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.screen import MDScreen

from core import caches
from core.structures.Entry import Entry
from ui.widgets import MetaDataImage


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

        headers = caches.provider_cache['home screen'].get_active_provider().get_headers()
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
            root_scroll_screen = App.get_running_app().root.ids.screen_manager.get_screen('home screen')
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