# This class contains the BooruProvider base class and all of its direct children.
# Note that providers that significantly modify BooruProvider's functionality, or inherit deeply from it, may
# be located in a different class.

from core.structures.Entry import Entry
from core.structures.ImageProvider import ImageProvider


class BooruProvider(ImageProvider):
    provider_url = ""
    page_tag = "pid"

    use_json_marker = True

    def __init__(self):
        super().__init__()
        self.user_id = ""
        self.user_api = ""

    def compose(self) -> str:
        req = self.provider_url

        # handle tags
        if self.get_tags() and len(self.get_tags()) > 0:
            req = req + "&tags="
            for tag in self.get_tags():
                req = req + "+" + tag

        # insert blacklisted tags
        if self.get_blacklisted_tags() and len(self.get_blacklisted_tags()) > 0:
            for tag in self.get_blacklisted_tags():
                req = req + "+-" + tag

        # handle safety
        if self.is_always_safe():
            req = req + "+rating:safe"

        # handle limit
        if int(self.get_image_limit()) > 0:
            req = req + "&limit=" + str(self.get_image_limit())

        if self.get_score_limit() >= 0:
            req = req + "&score:>=" + str(self.get_score_limit())

        if self.sort_mode is not None:
            if self.sort_mode == self.SCORE_SORT:
                req = req + "&sort:score:desc"
            elif self.sort_mode == self.RANDOM_SORT:
                req = req + "&sort:random"

        req = req + "&{t}=".format(t=self.page_tag) + str(self.page_number)

        if self.use_json_marker:
            req = req + "&json=1"

        print(req)
        return req

    def make_entry(self, data: dict) -> Entry:
        try:
            en = Entry()
            en.image_full = data["file_url"].replace("\\", "")
            en.image_small = en.image_full
            en.source = data["source"].replace("\\", "")
            en.tags = data["tags"].split(" ")
            en.headers = self.get_headers()
            return en
        except:
            print("Failed to make entry: ")
            print(data)


class GelbooruProvider(BooruProvider):

    def __init__(self):
        super().__init__()
        self.provider_url = "http://gelbooru.com/index.php?page=dapi&s=post&q=index"


class SafebooruProvider(BooruProvider):

    def __init__(self):
        super().__init__()
        self.provider_url = "http://safebooru.org/index.php?page=dapi&s=post&q=index"

    def make_entry(self, data: dict) -> Entry:
        try:
            en = Entry()
            image_url = "https://safebooru.org//images/{directory}/{image}".format(directory=data['directory'],
                                                                                   image=data['image'])
            en.image_full = image_url
            en.image_small = en.image_full
            en.source = ""
            en.tags = data["tags"].split(" ")
            en.headers = self.get_headers()
            return en
        except:
            print("Failed to make entry: ")
            print(data)


class Rule34Provider(BooruProvider):

    def __init__(self):
        super().__init__()
        self.provider_url = "https://rule34.xxx/index.php?page=dapi&s=post&q=index"

    def make_entry(self, data: dict) -> Entry:
        en = Entry()
        en.image_full = data["file_url"].replace("\\", "")
        en.image_small = data["sample_url"].replace("\\", "")
        en.source = None
        en.tags = data["tags"].split(" ")
        en.headers = self.get_headers()
        return en


class DanbooruProvider(BooruProvider):

    def __init__(self):
        super(DanbooruProvider, self).__init__()
        self.provider_url = "https://danbooru.donmai.us/posts.json?"
        self.page_tag = "page"
        self.use_json_marker = False

    def compose(self) -> str:
        first_append = True
        req = self.provider_url

        # handle tags
        if self.get_tags() and len(self.get_tags()) > 0:
            if first_append:
                first_append = False
            else:
                req = req + '&'
            req = req + "tags="
            for tag in self.get_tags():
                req = req + "+" + tag

        # insert blacklisted tags
        if self.get_blacklisted_tags() and len(self.get_blacklisted_tags()) > 0:
            for tag in self.get_blacklisted_tags():
                req = req + "+-" + tag

        # handle safety
        if self.is_always_safe():
            if first_append:
                first_append = False
            else:
                req = req + '&'
            req = req + "+rating:safe"

        # handle limit
        if int(self.get_image_limit()) > 0:
            if first_append:
                first_append = False
            else:
                req = req + '&'
            req = req + "limit=" + str(self.get_image_limit())

        if self.get_score_limit() >= 0:
            if first_append:
                first_append = False
            else:
                req = req + '&'
            req = req + "score:>=" + str(self.get_score_limit())

        if self.sort_mode is not None:
            if first_append:
                first_append = False
            else:
                req = req + '&'
            if self.sort_mode == self.SCORE_SORT:
                req = req + "sort:score:desc"
            elif self.sort_mode == self.RANDOM_SORT:
                req = req + "sort:random"

        if first_append:
            first_append = False
        else:
            req = req + '&'
        req = req + "{t}=".format(t=self.page_tag) + str(self.page_number)

        print(req)
        return req

    def make_entry(self, data: dict) -> Entry:
        try:
            en = Entry()
            en.image_full = data["file_url"].replace("\\", "")
            en.image_small = data['large_file_url']
            en.source = data["source"].replace("\\", "")
            en.tags = data["tag_string"].split(" ")
            en.headers = self.get_headers()
            en.title = "Art by " + data['tag_string_artist']
            return en
        except:
            print("Failed to make entry: ")
            print(data)
