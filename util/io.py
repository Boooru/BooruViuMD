# Util functions related to general IO
import os
import subprocess
from configparser import ConfigParser
from os import path

from kivy import Logger

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
                    user_rules[section.title()][value] = parser[section.title()][value]

            elif section.title() == "Main":
                for value in parser[section.title()].keys():
                    general[value] = parser[section.title()][value]

        caches.general_config = general
        caches.user_rules = user_rules
    else:
        cf = open(strings.CONFIG_FILE_NAME, 'x')
        cf.close()


def run_executable(path_to_file, args: str = "", is_async: bool = False):
    p = subprocess.Popen(path_to_file, cwd=os.getcwd())
    if not is_async:
        return_code = p.wait()
        Logger.info(path_to_file + " exited with code " + return_code)
