import json
from datetime import datetime
from typing import Union

import requests
from kivy import Logger

from core.structures import Entry


class ImageProvider:

    def __init__(self):
        self.user_id = ""
        self.user_api = ""

        self.provider_url = ""

        self.__tags = []
        self.__blacklisted_tags = []
        self.__image_limit = 0
        self.__score_limit = -1

        self.__replace_spaces = False
        self.__replacement = '_'

        self.__always_safe = False

        self.__headers = None

        self.sorting_modes = []
        self.sort_mode = None

        self.page_number = 0

    def make_entry(self, data: str) -> Entry:
        print("Default entry factory")

    def compose(self) -> str:
        return ""

    def search(self, reset_page: bool = True) -> list[Entry]:
        Logger.warn("Default ImageProvider.search used!")
        if reset_page:
            self.page_number = 0
        result = requests.get(self.compose())
        json_array = json.loads(result.text)
        entries = []
        for obj in json_array:
            entries.append(self.make_entry(obj))

        return entries

    def more(self) -> list[Entry]:
        print("Getting more from: " + self.provider_url)
        self.page_number = self.page_number + 1
        return self.search(reset_page=False)

    def add_tag(self, tag: str) -> None:
        if self.__replace_spaces:
            self.__tags.append(tag.replace(' ', self.__replacement))
        else:
            self.__tags.append(tag)

    def add_tags_from_string(self, tags: str) -> None:
        split_tags = tags.split(" ")
        self.add_tags(split_tags)

    def add_tags(self, tags: list[str]) -> None:
        for tag in tags:
            if self.__replace_spaces:
                self.__tags.append(tag.replace(' ', self.__replacement))
            else:
                self.__tags.append(tag)

    def blacklist_tag(self, tag: str):
        if self.__replace_spaces:
            self.__blacklisted_tags.append(tag.replace(' ', self.__replacement))
        else:
            self.__blacklisted_tags.append(tag)

    def blacklist_tags(self, tags: list[str]):
        for tag in tags:
            if self.__replace_spaces:
                self.__blacklisted_tags.append(tag.replace(' ', self.__replacement))
            else:
                self.__blacklisted_tags.append(tag)

    def blacklist_tags_from_string(self, tags: str) -> None:
        split_tags = tags.split(" ")
        self.blacklist_tags(split_tags)

    def sort_by(self, mode:Union[str, int]):
        if type(mode) == str:
            if mode in self.sorting_modes:
                self.sort_mode = mode

        elif type(mode) == int:
            if mode in range(len(self.sorting_modes)):
                self.sort_mode = self.sorting_modes[mode]

    def set_score_limit(self, limit: int):
        self.__score_limit = limit

    def get_score_limit(self) -> int:
        return self.__score_limit

    def set_limit(self, limit: int):
        self.__image_limit = limit

    def get_tags(self) -> list[str]:
        return self.__tags

    def clear_tags(self):
        self.__tags = []

    def clear_blacklist(self):
        self.__blacklisted_tags = []

    def get_blacklisted_tags(self) -> list[str]:
        return self.__blacklisted_tags

    def get_image_limit(self) -> int:
        return self.__image_limit

    def is_always_safe(self) -> bool:
        return self.__always_safe

    def set_always_safe(self, safe: bool):
        self.__always_safe = safe

    def replace_spaces_with(self, sep: str):
        self.__replacement = sep
        self.__replace_spaces = True

    def dont_replace_spaces(self):
        self.__replace_spaces = False

    def get_headers(self):
        return self.__headers

    def set_headers(self, headers: dict):
        self.__headers = headers
