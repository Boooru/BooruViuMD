# Util functions related to general IO
import os
import subprocess
from configparser import ConfigParser
from os import path

from kivy import Logger

import assets.strings
from assets import strings
from core import caches


def load_api_keys():
    if not path.exists(strings.API_KEY_STORE_PATH):
        print("No keystore found!")
        if not os.path.isdir("./tokens"):
            os.mkdir("./tokens")
        with open(strings.API_KEY_STORE_PATH, 'w') as keystore:
            s = """
            [Keys]
            Saucenao = None
            Twitter = None
            Reddit_app = None
            Reddit_secret = None
            Reddit_username = None
            Reddit_password = None
            """

            keystore.write(s)
            keystore.close()
    else:
        print("Loading keystore...")
        parser = ConfigParser()
        cfg = parser.read(strings.API_KEY_STORE_PATH)

        keys = {}
        for key in parser['Keys']:
            keys[key] = parser['Keys'][key]

        print(keys)
        caches.api_keys = keys


def load_settings():
    if os.path.exists(strings.CONFIG_FILE_NAME):
        parser = ConfigParser()
        parser.read(strings.CONFIG_FILE_NAME)

        user_rules = {}
        general = {}

        for section in parser.sections():
            if section.title() in strings.ALL_PROVIDERS:
                user_rules[section.title()] = {}
                for value in parser[section.title()].keys():
                    user_rules[section.title()][value] = parser[section.title()][value].replace('"', '')

            elif section.title() == "Main":
                for value in parser[section.title()].keys():
                    general[value] = parser[section.title()][value]

        caches.general_config = general
        caches.user_rules = user_rules
    else:
        cf = open(strings.CONFIG_FILE_NAME, 'x')
        cf.close()


def save_settings():
    Logger.info("Writing config data...")

    parser = ConfigParser()
    parser.add_section("Main")

    print("Main:")
    for key in caches.general_config:
        print(str(key) + ": " + str(caches.general_config[key]))
        parser["Main"][key] = caches.general_config[key]

    for provider in caches.user_rules:
        print(str(provider))
        parser.add_section(provider)
        for key in caches.user_rules[provider]:
            print(str(key) + ": " + str(caches.user_rules[provider][key]))
            parser[provider][key] = caches.user_rules[provider][key]

    if os.path.exists(assets.strings.CONFIG_FILE_NAME):
        os.remove(assets.strings.CONFIG_FILE_NAME)

    with open(assets.strings.CONFIG_FILE_NAME, 'w') as configfile:
        parser.write(configfile)


def run_executable(path_to_file, args: str = "", is_async: bool = False):
    p = subprocess.Popen(path_to_file, cwd=os.getcwd())
    if not is_async:
        return_code = p.wait()
        Logger.info(path_to_file + " exited with code " + return_code)
