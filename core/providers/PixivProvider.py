import os

import util.pixiv_auth
from core.caches import api_cache
from core.structures.Entry import Entry
from core.structures.ImageProvider import ImageProvider
from util import utils


class PixivProvider(ImageProvider):
    __tokens = None
    __target = None

    def __init__(self):
        super(PixivProvider, self).__init__()

        util.pixiv_auth.aapi_auth()

        self.set_headers({"Referer": 'https://app-api.pixiv.net/'})

        self.__tokens = None
        self.__target = None

        self.modes_std = ['day', 'week', 'month', 'day_male', 'day_female', 'week_original', 'week_rookie', 'day_manga']
        self.modes_r18 = ['day_r18', 'day_male_r18', 'day_female_r18', 'week_r18', 'week_r18g']
        self.modes = (self.modes_std + self.modes_r18 + ['user', 'following'])
        self.mode = [self.modes[0]]

    def compose(self) -> str:
        if len(self.get_tags()) > 0:
            self.__target = self.get_tags()[0]

            return self.get_tags()[0]

        return ""

    def search(self, reset_page: bool = True, next_page=None) -> list[Entry]:
        if not os.path.isdir("./temp"):
            os.mkdir("./temp")

        if reset_page:
            self.page_number = 0

        entries = []
        response = None

        if self.mode == 'user':
            if not self.__target or self.__target == "":
                return []
            else:
                response = self.__search_user(reset_page, next_page)

        elif self.mode == 'following':
            response = self.__search_followed(reset_page, next_page)
        else:
            response = self.__search_rankings(reset_page, next_page)

        if not response:
            return entries

        for illus in response.illusts:
            if len(illus.meta_pages) > 0:
                for page in illus.meta_pages:
                    e = Entry()
                    e.image_full = page.image_urls.original
                    e.image_small = page.image_urls.medium
                    e.source = "https://www.pixiv.net/en/users/" + str(illus.user.id)
                    e.tags = [str(t['translated_name']) for t in illus.tags]
                    e.headers = self.get_headers()
                    entries.append(e)
            else:
                e = Entry()
                if illus.image_urls.original:
                    e.image_full = illus.image_urls.original
                elif illus.image_urls.large:
                    e.image_full = illus.image_urls.large
                elif illus.image_urls.medium:
                    print("Can't find larger image, check JSON")
                    print(illus)
                    e.image_full = illus.image_urls.medium
                else:
                    print("skipped")
                    print(illus.image_urls)
                    continue

                e.image_small = illus.image_urls.medium
                e.source = "https://www.pixiv.net/en/users/" + str(illus.user.id)
                e.tags = [t['name'] for t in illus.tags]
                e.headers = self.get_headers()
                entries.append(e)

        return entries

    def more(self):
        print("Getting more from pixiv")
        return self.search(reset_page=False, next_page=self.page_number)

    def __search_user(self, reset_page: bool, next_page):
        response = None
        if reset_page and next_page is None:  # Check if we are making a fresh request
            try:
                artist_id = int(self.__target)  # If so, parse the user's ID we are visiting
            except ValueError:
                user_id = utils.get_user_from_url(self.__target)
                if user_id:
                    artist_id = user_id
                else:
                    return []
            response = api_cache['pixiv-aapi'].user_illusts(user_id=artist_id)  # Get the user's works

            # If we have more than one page worth of works, set the page_number var to the url of the next page
            self.page_number = response.next_url
        elif next_page:  # The user wants to get the next page
            response = api_cache['pixiv-aapi'].parse_qs(next_page)  # Get the works from the next page
            response = api_cache['pixiv-aapi'].user_illusts(**response)
            self.page_number = response.next_url  # Update the page_number var to have the url of the next page
        else:
            print("Something went wrong, can't fetch any results!")

        return response

    def __search_followed(self, reset_page: bool, next_page):
        response = None
        if reset_page and next_page is None:  # Check if we are making a fresh request

            response = api_cache['pixiv-aapi'].illust_follow(req_auth=True)  # Get the user's works

            # If we have more than one page worth of works, set the page_number var to the url of the next page
            self.page_number = response.next_url
        elif next_page:  # The user wants to get the next page
            response = api_cache['pixiv-aapi'].parse_qs(next_page)  # Get the works from the next page
            response = api_cache['pixiv-aapi'].illust_follow(req_auth=True, **response)
            self.page_number = response.next_url  # Update the page_number var to have the url of the next page
        else:
            print("Something went wrong, can't fetch any results!")

        return response

    def __search_rankings(self, reset_page: bool, next_page):
        response = None
        if reset_page and next_page is None:  # Check if we are making a fresh request

            response = api_cache['pixiv-aapi'].illust_ranking(self.mode)  # Get the user's works

            # If we have more than one page worth of works, set the page_number var to the url of the next page
            self.page_number = response.next_url
        elif next_page:  # The user wants to get the next page
            response = api_cache['pixiv-aapi'].parse_qs(next_page)  # Get the works from the next page
            response = api_cache['pixiv-aapi'].illust_ranking(**response)
            self.page_number = response.next_url  # Update the page_number var to have the url of the next page
        else:
            print("Something went wrong, can't fetch any results!")

        return response
