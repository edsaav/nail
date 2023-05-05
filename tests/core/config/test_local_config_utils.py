from unittest.mock import mock_open, patch
from nail.core.config import local_config_utils


def test_load_local_config_file_exists():
    # Mock the existence of the config file and its content
    config_content = """
    key: value
    """
    m = mock_open(read_data=config_content)
    with patch("builtins.open", m):
        with patch("os.path.exists", return_value=True):
            # Call the function and check if the content is loaded correctly
            config = local_config_utils.load_local_config()
            assert config == {"key": "value"}


def test_load_local_config_file_not_exists():
    # Mock the non-existence of the config file
    with patch("os.path.exists", return_value=False):
        # Call the function and check if an empty dictionary is returned
        config = local_config_utils.load_local_config()
        assert config == {}
