from unittest.mock import patch, ANY
import pytest
from click.testing import CliRunner

from main import configure, build, readme, modify, debug, spec


@pytest.fixture
def runner():
    return CliRunner()


def test_configure(runner):
    with patch("main.save_api_key") as mock_save_api_key:
        result = runner.invoke(configure, input="test_api_key\n")
        assert result.exit_code == 0
        mock_save_api_key.assert_called_once_with("test_api_key")


def test_build(runner):
    with patch("main.build_file") as mock_build_file:
        result = runner.invoke(build, ["test_file"])
        assert result.exit_code == 0
        mock_build_file.assert_called_once_with("test_file", ANY, None)


def test_readme(runner):
    with patch("main.build_readme") as mock_build_readme:
        result = runner.invoke(readme)
        assert result.exit_code == 0
        mock_build_readme.assert_called_once_with("README.md", None)


def test_modify(runner):
    with patch("main.modify_file") as mock_modify_file:
        result = runner.invoke(modify, ["test_file", "-r", "test_request"])
        assert result.exit_code == 0
        mock_modify_file.assert_called_once_with(
            "test_file", "test_request", ANY, None)


def test_debug(runner):
    with patch("main.debug_file") as mock_debug_file:
        result = runner.invoke(debug, ["test_file"])
        assert result.exit_code == 0
        mock_debug_file.assert_called_once_with("test_file", None, None)


def test_spec(runner):
    with patch("main.build_spec_file") as mock_build_spec_file:
        result = runner.invoke(spec, ["test_file", "test_target_path"])
        assert result.exit_code == 0
        mock_build_spec_file.assert_called_once_with(
            "test_file", "test_target_path", None)
