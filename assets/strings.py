# File Names
CONFIG_FILE_NAME = "preferences.cfg"

# Paths
SAVE_PATH = './downloads'
PIXIV_TOKEN_PATH = "./tokens/pixiv"
API_KEY_STORE_PATH = "./tokens/keystore"

MODULE_UPSCALE_BIN_PATH = "bin/upscaleprovider/"

# Provider Names
PROVIDER_GELBOORU_NAME = "Gelbooru"
PROVIDER_R34_NAME = 'Rule34'
PROVIDER_TWITTER_NAME = 'Twitter'
PROVIDER_PIXIV_NAME = "Pixiv"
PROVIDER_SAFEBOORU_NAME = "Safebooru"
PROVIDER_REDDIT_NAME = "Reddit"
PROVIDER_DANBOORU_NAME = "Danbooru"

# Provider list
ALL_PROVIDERS = [PROVIDER_GELBOORU_NAME, PROVIDER_R34_NAME, PROVIDER_TWITTER_NAME, PROVIDER_PIXIV_NAME,
                 PROVIDER_SAFEBOORU_NAME, PROVIDER_REDDIT_NAME, PROVIDER_DANBOORU_NAME]

# Regex
TWITTER_USER_REGEX = r'twitter\.com\/[a-zA-Z0-9_-]+'
PIXIV_USER_REGEX = r'users\/[0-9]+'
PIXIV_ARTWORK_REGEX = "artworks\\/[0-9]+"
PIXIV_OLD_ILLUS_REGEX = "illust_id=[0-9]+"

# URLs
MODULE_UPSCALE_OSX_URL = "https://github.com/nihui/waifu2x-ncnn-vulkan/releases/download/20210521/waifu2x-ncnn-vulkan-20210521-macos.zip"
MODULE_UPSCALE_LINUX_URL = "https://github.com/nihui/waifu2x-ncnn-vulkan/releases/download/20210521/waifu2x-ncnn-vulkan-20210521-ubuntu.zip"
MODULE_UPSCALE_WINDOWS_URL = "https://github.com/nihui/waifu2x-ncnn-vulkan/releases/download/20210521/waifu2x-ncnn-vulkan-20210521-windows.zip"
