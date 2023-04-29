import configparser
from unittest import mock
from unittest.mock import patch
import pytest
from nail.core.config_utils import get_api_key, save_api_key


@pytest.fixture
def temp_config_file(tmp_path):
    temp_file = tmp_path / ".nailrc"
    temp_file.touch()
    return temp_file


def test_get_api_key_with_env_var(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test_key")
    assert get_api_key() == "test_key"


def test_get_api_key_with_config_file(monkeypatch, temp_config_file):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    config = configparser.ConfigParser()
    config["openai"] = {"api_key": "test_key"}
    with temp_config_file.open("w") as f:
        config.write(f)

    with mock.patch("nail.core.config_utils.CONFIG_FILE", temp_config_file):
        assert get_api_key() == "test_key"


def test_get_api_key_with_no_key(monkeypatch, temp_config_file):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with mock.patch("nail.core.config_utils.CONFIG_FILE", temp_config_file):
        assert get_api_key() is None


def test_save_api_key(tmp_path):
    api_key = "test_api_key"
    temp_config_file = tmp_path / ".nailrc"

    with patch("nail.core.config_utils.CONFIG_FILE", temp_config_file):
        save_api_key(api_key)
        config = configparser.ConfigParser()
        config.read(temp_config_file)
        assert config["openai"]["api_key"] == api_key
