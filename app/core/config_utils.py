import os
import configparser
from pathlib import Path

CONFIG_FILE = Path.home() / ".nailrc"


def get_api_key():
    if "OPENAI_API_KEY" in os.environ:
        return os.environ["OPENAI_API_KEY"]

    if CONFIG_FILE.is_file():
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        if "openai" in config and "api_key" in config["openai"]:
            return config["openai"]["api_key"]

    return None


def save_api_key(api_key):
    config = configparser.ConfigParser()
    if CONFIG_FILE.is_file():
        config.read(CONFIG_FILE)

    if "openai" not in config:
        config["openai"] = {}

    config["openai"]["api_key"] = api_key

    with CONFIG_FILE.open("w") as config_file:
        config.write(config_file)
