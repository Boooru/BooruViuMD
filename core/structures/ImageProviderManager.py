from kivy.app import App

from core import caches
from core.structures import ImageProvider
import assets.strings
from util import provider_util


class ProviderManager:
    DEFAULT_PROVIDER = assets.strings.PROVIDER_GELBOORU_NAME

    def __init__(self):
        self.__provider = None
        self.__user_rules = caches.user_rules

        if caches.general_config and 'default_provider' in caches.general_config:
            self.DEFAULT_PROVIDER = caches.general_config['default_provider']
        self.set_provider(self.DEFAULT_PROVIDER)

    def clear(self) -> None:
        self.__provider = None

    def get_active_provider(self) -> ImageProvider:
        return self.__provider

    def set_provider(self, provider_name: str):
        self.__provider = (provider_util.translate(provider_name))()
        self.__provider.set_limit(10)
        if provider_name not in caches.user_rules:
            return

        if "tags" in self.__user_rules[provider_name] and self.__user_rules[provider_name]["tags"]:
            self.__provider.add_tags_from_string(tags=self.__user_rules[provider_name]["tags"])

        if "blacklist" in self.__user_rules[provider_name] and self.__user_rules[provider_name]["blacklist"]:
            self.__provider.blacklist_tags_from_string(tags=self.__user_rules[provider_name]["blacklist"])

        if "limit" in self.__user_rules[provider_name] and self.__user_rules[provider_name]["limit"]:
            self.__provider.set_limit(limit=int(self.__user_rules[provider_name]["limit"]))
        else:
            self.__provider.set_limit(10)

        if "always_safe" in self.__user_rules[provider_name] and self.__user_rules[provider_name]["always_safe"]:
            self.__provider.set_always_safe(bool(self.__user_rules[provider_name]['always_safe']))
