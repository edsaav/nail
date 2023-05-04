import os
import configparser
from pathlib import Path

USER_CONFIG_FILE = Path.home() / ".nailrc"


def get_api_key():
    if "OPENAI_API_KEY" in os.environ:
        return os.environ["OPENAI_API_KEY"]

    if USER_CONFIG_FILE.is_file():
        config = configparser.ConfigParser()
        config.read(USER_CONFIG_FILE)
        if "openai" in config and "api_key" in config["openai"]:
            return config["openai"]["api_key"]

    return None


def save_api_key(api_key):
    config = configparser.ConfigParser()
    if USER_CONFIG_FILE.is_file():
        config.read(USER_CONFIG_FILE)

    if "openai" not in config:
        config["openai"] = {}

    config["openai"]["api_key"] = api_key

    with USER_CONFIG_FILE.open("w") as config_file:
        config.write(config_file)
