import json
import os

CONFIG_FILE_NAME = ".nail.json"


def load_local_config():
    if os.path.exists(CONFIG_FILE_NAME):
        with open(CONFIG_FILE_NAME, "r") as file:
            config = json.load(file)
    return config
