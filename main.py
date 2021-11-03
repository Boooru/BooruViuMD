import os

from kivy.config import Config
from kivy.lang import Builder
from kivymd.app import MDApp

import core.caches
from core.structures.ImageProviderManager import ProviderManager

from flow.preprocessing.download import AsyncDownloader

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
    Config.set('graphics', 'width', '1600')
    Config.set('graphics', 'height', '1080')
    for kv_file in os.listdir("kv"):
        with open(os.path.join("kv", kv_file), encoding="utf-8") as kv:
            Builder.load_string(kv.read())

    print("Running app")
    BooruApp().run()
