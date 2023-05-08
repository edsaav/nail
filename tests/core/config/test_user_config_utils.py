import configparser
import pytest
from nail.core.config.user_config_utils import (
    get_api_key,
    save_api_key,
    USER_CONFIG_FILE,
)


def test_get_api_key_from_env(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test_key_from_env")
    assert get_api_key() == "test_key_from_env"


def test_get_api_key_from_file(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    config = configparser.ConfigParser()
    config["openai"] = {"api_key": "test_key_from_file"}
    with USER_CONFIG_FILE.open("w") as config_file:
        config.write(config_file)
    assert get_api_key() == "test_key_from_file"


def test_get_api_key_not_found(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    if USER_CONFIG_FILE.is_file():
        USER_CONFIG_FILE.unlink()
    assert get_api_key() is None


def test_save_api_key():
    save_api_key("test_key_to_save")
    config = configparser.ConfigParser()
    config.read(USER_CONFIG_FILE)
    assert config["openai"]["api_key"] == "test_key_to_save"


@pytest.fixture(autouse=True)
def cleanup():
    # Remove the config file before and after each test
    if USER_CONFIG_FILE.is_file():
        USER_CONFIG_FILE.unlink()
    yield
    if USER_CONFIG_FILE.is_file():
        USER_CONFIG_FILE.unlink()
