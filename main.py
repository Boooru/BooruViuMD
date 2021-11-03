import os

from kivy import platform
from kivy.config import Config
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp

import core.caches
from core.structures.ImageProviderManager import ProviderManager

from flow.preprocessing.download import AsyncDownloader
from util import io

async_downloader = AsyncDownloader()

class BooruApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Booru Viu"
        self.provider_manager = ProviderManager()

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"

        core.caches.provider_cache['root scroll screen'] = ProviderManager()


if __name__ == "__main__":
    Window.size = (1600, 1080)

    if platform == 'win':
        # Dispose of that nasty red dot on Windows
        Config.set('input', 'mouse', 'mouse, disable_multitouch')

    Config.set('graphics', 'resizable', True)
    Config.set('kivy', 'exit_on_escape', 0)

    io.load_api_keys()
    io.load_settings()

    for kv_file in os.listdir("kv"):
        with open(os.path.join("kv", kv_file), encoding="utf-8") as kv:
            Builder.load_string(kv.read())

    print("Running app")
    BooruApp().run()
