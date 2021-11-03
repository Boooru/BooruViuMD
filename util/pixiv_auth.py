# This is a modified version of the original Pixiv OAuth Flow (with Selenium) Python script created by upbit.
# Find the original here: https://gist.github.com/upbit/6edda27cb1644e94183291109b8a5fde

import os
import time
import json
import re
from configparser import ConfigParser

import pixivpy3
import requests

from argparse import ArgumentParser
from base64 import urlsafe_b64encode
from hashlib import sha256
from pprint import pprint
from secrets import token_urlsafe
from sys import exit
from urllib.parse import urlencode

from kivy import Logger
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Latest app version can be found using GET /v1/application-info/android
from core.caches import api_cache
import util

USER_AGENT = "PixivIOSApp/7.13.3 (iOS 14.6; iPhone13,2)"
REDIRECT_URI = "https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback"
LOGIN_URL = "https://app-api.pixiv.net/web/v1/login"
AUTH_TOKEN_URL = "https://oauth.secure.pixiv.net/auth/token"
CLIENT_ID = "MOBrBDS8blbauoSck0ZfDbtuzpyT"
CLIENT_SECRET = "lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj"
REQUESTS_KWARGS = {
    # 'proxies': {
    #     'https': 'http://127.0.0.1:1087',
    # },
    # 'verify': False
}


def s256(data):
    """S256 transformation method."""

    return urlsafe_b64encode(sha256(data).digest()).rstrip(b"=").decode("ascii")


def oauth_pkce(transform):
    """Proof Key for Code Exchange by OAuth Public Clients (RFC7636)."""

    code_verifier = token_urlsafe(32)
    code_challenge = transform(code_verifier.encode("ascii"))

    return code_verifier, code_challenge


def print_auth_token_response(response):
    data = response.json()

    try:
        access_token = data["access_token"]
        refresh_token = data["refresh_token"]
    except KeyError:
        print("error:")
        pprint(data)
        exit(1)

    print("access_token:", access_token)
    print("refresh_token:", refresh_token)
    print("expires_in:", data.get("expires_in", 0))


def auth_tokens(response) -> dict:
    data = response.json()

    try:
        access_token = data["access_token"]
        refresh_token = data["refresh_token"]
    except KeyError:
        print("error:")
        pprint(data)
        exit(1)

    return {
        "access_token": data["access_token"],
        "refresh_token": data["refresh_token"]
    }


def login() -> dict:
    caps = DesiredCapabilities.CHROME.copy()
    caps["goog:loggingPrefs"] = {"performance": "ALL"}  # enable performance logs

    driver = None
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=caps)
    except:
        Logger.warn("Couldn't locate Chrome, trying Firefox")
    if not driver:
        try:
            driver = webdriver.Firefox(GeckoDriverManager().install(), desired_capabilities=caps)
        except:
            Logger.warn("Couldn't locate Firefox, trying Edge")
    if not driver:
        driver = webdriver.ChromiumEdge(EdgeChromiumDriverManager().install())

    code_verifier, code_challenge = oauth_pkce(s256)
    login_params = {
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "client": "pixiv-android",
    }
    print("[INFO] Gen code_verifier:", code_verifier)

    driver.get(f"{LOGIN_URL}?{urlencode(login_params)}")

    while True:
        # wait for login
        if driver.current_url[:40] == "https://accounts.pixiv.net/post-redirect":
            break
        time.sleep(1)

    # filter code url from performance logs
    code = None
    for row in driver.get_log('performance'):
        data = json.loads(row.get("message", {}))
        message = data.get("message", {})
        if message.get("method") == "Network.requestWillBeSent":
            url = message.get("params", {}).get("documentURL")
            if url[:8] == "pixiv://":
                code = re.search(r'code=([^&]*)', url).groups()[0]
                break

    driver.close()

    print("[INFO] Get code:", code)

    response = requests.post(
        AUTH_TOKEN_URL,
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "code_verifier": code_verifier,
            "grant_type": "authorization_code",
            "include_policy": "true",
            "redirect_uri": REDIRECT_URI,
        },
        headers={
            "user-agent": USER_AGENT,
            "app-os-version": "14.6",
            "app-os": "ios",
        },
        **REQUESTS_KWARGS
    )

    # print_auth_token_response(response)
    return auth_tokens(response)


def refresh(refresh_token):
    response = requests.post(
        AUTH_TOKEN_URL,
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "refresh_token",
            "include_policy": "true",
            "refresh_token": refresh_token,
        },
        headers={
            "user-agent": USER_AGENT,
            "app-os-version": "14.6",
            "app-os": "ios",
        },
        **REQUESTS_KWARGS
    )
    print_auth_token_response(response)


def read_tokens():
    import assets
    parser = ConfigParser()
    parser.read(assets.strings.PIXIV_TOKEN_PATH)
    return parser['tokens']


def write_tokens(tokens):
    import assets
    if os.path.isfile(assets.strings.PIXIV_TOKEN_PATH):
        os.remove(assets.strings.PIXIV_TOKEN_PATH)

    parser = ConfigParser()
    parser.add_section("tokens")
    parser["tokens"] = tokens
    with open(assets.strings.PIXIV_TOKEN_PATH, 'w') as configfile:
        parser.write(configfile)


# For internal use only. Manages IO/API calls to create an authenticated AppPixivAPI object.
def try_aapi_auth():
    import util, assets
    aapi = pixivpy3.AppPixivAPI()
    tokens = None

    if not os.path.isdir("tokens"):
        os.mkdir("tokens")

    need_refresh = False
    if need_refresh or not os.path.isfile(assets.strings.PIXIV_TOKEN_PATH):
        tokens = util.pixiv_auth.login()
        write_tokens(tokens)
    else:
        tokens = read_tokens()

    aapi.access_token = tokens['access_token']
    aapi.auth(refresh_token=tokens['refresh_token'])

    return aapi


# If the pixiv api has not already been authed, auth and store the api in the cache
def aapi_auth():
    if "pixiv-aapi" not in api_cache or not api_cache['pixiv-aapi']:
        api_cache['pixiv-aapi'] = util.pixiv_auth.try_aapi_auth()


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()
    parser.set_defaults(func=lambda _: parser.print_usage())
    login_parser = subparsers.add_parser("login")
    login_parser.set_defaults(func=lambda _: login())
    refresh_parser = subparsers.add_parser("refresh")
    refresh_parser.add_argument("refresh_token")
    refresh_parser.set_defaults(func=lambda ns: refresh(ns.refresh_token))
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
