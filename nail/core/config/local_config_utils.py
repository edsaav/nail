import os
import yaml

CONFIG_FILE_NAME = ".nail.yaml"


def load_local_config():
    config = {}
    if os.path.exists(CONFIG_FILE_NAME):
        with open(CONFIG_FILE_NAME, "r") as file:
            config = yaml.safe_load(file)
    return config
