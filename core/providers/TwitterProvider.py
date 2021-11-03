from kivy import Logger
from twitter import Twitter, OAuth2, TwitterStream
from twitter.api import TwitterListResponse

import core.caches
from core.structures.Entry import Entry
from core.structures.ImageProvider import ImageProvider
from util import utils


class TwitterProvider(ImageProvider):
    __bearer_token = None

    def __init__(self, **kwargs):
        super().__init__()
        if "bearer_token" in kwargs:
            self.__bearer_token = kwargs["bearer_token"]
        else:
            self.__bearer_token = core.caches.api_keys['twitter']
        self.__twitter = Twitter(auth=OAuth2(bearer_token=self.__bearer_token))
        self.__stream = TwitterStream(auth=OAuth2(bearer_token=self.__bearer_token))
        self.__target = ""
        self.set_limit(200)  # Not true image limit, actually

    def compose(self) -> str:
        if len(self.get_tags()) > 0:
            self.__target = self.get_tags()[0]
        return ""

    # TODO: Test this on a tweet containing multiple videos
    # TODO: Add GIF support
    def search(self, reset_page: bool = True) -> list[Entry]:
        results: TwitterListResponse = None
        entries: list[Entry] = []

        if reset_page:
            self.page_number = None
            self.__stream = None

        if self.__target:
            if self.page_number and self.page_number > -1:
                results = self.__twitter.statuses.user_timeline(screen_name=self.__target, count=200,
                                                                max_id=self.page_number)
                print("Searched with count or max")
            else:
                results = self.__twitter.statuses.user_timeline(screen_name=self.__target)
                print("Searched without count or max")

            if results:
                self.page_number = results[-1]['id']
            else:
                self.page_number = -1
                print("No results found")
            for r in results:  # For each result
                if "extended_entities" in r:
                    for em in r['extended_entities']['media']:  # For each individual media on that tweet
                        if em['type'] == 'video':
                            print('Found a video: ')
                            e = Entry()
                            e.image_full = utils.best_video_variant(em['video_info']['variants']).removesuffix(
                                "mp4*+") + ".mp4"
                            print(e.image_full)
                            e.image_small = e.image_full
                            e.tags = ['twitter_video']
                            e.score = 0
                            entries.append(e)
                        else:
                            Logger.warn("Found extended media of type: " + em['type'])
                            e = Entry()
                            e.image_full = em['media_url_https']
                            e.source = em['expanded_url']
                            e.image_small = em['media_url_https']
                            e.tags = []
                            e.score = 0
                            e.headers = self.get_headers()
                            entries.append(e)
                elif "media" in r["entities"]:  # That has some media in it
                    for m in r['entities']['media']:  # For each individual media on that tweet
                        e = Entry()
                        e.image_full = m['media_url_https']
                        e.source = m['expanded_url']
                        e.image_small = m['media_url_https']
                        e.tags = []
                        e.score = 0
                        e.headers = self.get_headers()
                        entries.append(e)


            else:
                print("No media found")
        return entries

    def more(self) -> list[Entry]:
        print("Getting more from: " + self.provider_url)
        results = self.search(reset_page=False)
        print("Got " + str(len(results)) + " results!")
        return results
