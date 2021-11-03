from typing import Union, Optional
import assets
from core.providers.PixivProvider import PixivProvider
from core.providers.RedditProvider import RedditProvider
from core.providers.TwitterProvider import TwitterProvider
from core.providers.BooruProvider import GelbooruProvider, Rule34Provider, SafebooruProvider, DanbooruProvider
from core.structures.ImageProvider import ImageProvider


def translate(provider: Union[str, ImageProvider]) -> Optional[Union[str, ImageProvider]]:
    name_class_map = {assets.strings.PROVIDER_GELBOORU_NAME: GelbooruProvider,
                      assets.strings.PROVIDER_SAFEBOORU_NAME: SafebooruProvider,
                      assets.strings.PROVIDER_R34_NAME: Rule34Provider,
                      assets.strings.PROVIDER_PIXIV_NAME: PixivProvider,
                      assets.strings.PROVIDER_TWITTER_NAME: TwitterProvider,
                      assets.strings.PROVIDER_REDDIT_NAME: RedditProvider,
                      assets.strings.PROVIDER_DANBOORU_NAME: DanbooruProvider}
    class_name_map = {v: k for k, v in name_class_map.items()}
    if type(provider) == str:
        if provider in name_class_map.keys():
            return name_class_map[provider]
        else:
            print("Couldn't translate " + str(provider))
            print(name_class_map.keys())
    elif isinstance(provider, ImageProvider):
        if provider.__class__ in class_name_map:
            return class_name_map[provider.__class__]
        else:
            print("Couldn't translate " + str(provider))
    else:
        print("Couldn't translate " + str(type(provider)))
