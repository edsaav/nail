import pytest

from unittest.mock import patch
from nail.tools.spec.build_spec_file import build_spec_file


@pytest.fixture
def MockSpecPrompt():
    with patch("nail.tools.spec.build_spec_file.SpecPrompt", autospec=True) as mock:
        mock_prompt = mock.return_value
        mock_prompt.text.return_value = 'Create unit tests for the following: code'
        yield mock


@pytest.fixture
def MockFileEditor():
    with patch("nail.tools.spec.build_spec_file.FileEditor", autospec=True) as mock:
        yield mock


@pytest.fixture
def MockChat():
    with patch("nail.tools.spec.build_spec_file.Chat", autospec=True) as mock:
        mock_chat = mock.return_value
        mock_chat.predict_code.return_value = (
            "def test_add():\n"
            "    assert add(1, 2) == 3\n"
        )
        yield mock


def test_build_spec_file(MockSpecPrompt, MockFileEditor, MockChat):
    mock_file_editor = MockFileEditor.return_value

    build_spec_file("initial_file.py", "test_initial_file.py")

    mock_file_editor.apply_changes.assert_called_once_with(
        "def test_add():\n    assert add(1, 2) == 3\n")
