import praw
from kivy import Logger
from praw.models import Subreddit

import core.caches
import util.utils
from core.structures.Entry import Entry
from core.structures.ImageProvider import ImageProvider
import assets


class RedditProvider(ImageProvider):

    def __init__(self):
        super().__init__()

        self.internal_index = 0
        self.__reddit_api: praw.Reddit = self.__auth()
        self.__subreddt_generator: Subreddit = None
        self.sorting_modes = ['top', 'hot', 'new']
        self.sort_mode = self.sorting_modes[1]
        super().set_limit(10)

    def __auth(self):
        if assets.strings.PROVIDER_REDDIT_NAME in core.caches.api_cache and \
                core.caches.api_cache[assets.strings.PROVIDER_REDDIT_NAME]:

            return core.caches.api_cache[assets.strings.PROVIDER_REDDIT_NAME]
        else:
            core.caches.api_cache[assets.strings.PROVIDER_REDDIT_NAME] = \
                praw.Reddit(client_id=core.caches.api_keys["reddit_app"],
                            user_agent="BooruViu",
                            client_secret=core.caches.api_keys['reddit_secret'],
                            username=core.caches.api_keys['reddit_username'],
                            password=core.caches.api_keys['reddit_password'])

            return core.caches.api_cache[assets.strings.PROVIDER_REDDIT_NAME]

    def __test(self) -> bool:
        try:
            askreddit = self.__reddit_api.subreddit('askreddit').hot()
            return True
        except:
            return False

    def compose(self) -> str:
        c = ""
        for tag in self.get_tags():
            c = c + tag

        return c

    def search(self, reset_page: bool = True) -> list[Entry]:
        entries = []
        self.internal_index = 0

        if self.get_tags() is None or self.get_tags() == [] or self.get_tags()[0] == "":
            return entries

        if reset_page:
            limit = self.get_image_limit()
            if self.sort_mode == 'hot':
                Logger.info("Sorting by hot")
                self.__subreddt_generator = self.__reddit_api.subreddit(self.compose()).hot()
            elif self.sort_mode == 'top':
                Logger.info("Sorting by top")
                self.__subreddt_generator = self.__reddit_api.subreddit(self.compose()).top()
            else:
                Logger.info("Sorting by new")
                Logger.info("Sort mode was: " + str(self.sort_by))
                self.__subreddt_generator = self.__reddit_api.subreddit(self.compose()).new()

        for submission in self.__subreddt_generator:
            if self.internal_index > self.get_image_limit():
                break

            if submission.selftext != "":
                Logger.info("Skipping self-post: " + submission.url)
                continue

            self.internal_index = self.internal_index + 1

            entries.append(self.make_entry(submission))

        return entries

    def make_entry(self, data: praw.models.Submission) -> Entry:
        e = Entry()

        if util.utils.contains_domain(data.url, "redgifs" or util.utils.contains_domain(data.url, 'gyfcat')):
            e.image_full = util.utils.transform_redgif(data.url)
            e.image_small = util.utils.transform_redgif(data.url, "mobile")
        elif util.utils.contains_domain(data.url, "gify"):
            pass
        else:
            e.image_full = data.url
            e.image_small = data.url
        e.source = data.permalink
        e.score = data.score
        e.tile = data.title
        return e

    def more(self) -> list[Entry]:
        return self.search(reset_page=False)
