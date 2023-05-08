import pytest
import os
from unittest.mock import patch
from nail.tools.build.build_readme import build_readme

# Test data
TEST_CONTEXT_DIRECTORY = "test_directory"
TEST_PROMPT = "This is the content of the app files. Generate a README file."
TEST_README_FILE = "README.md"
TEST_README_CONTENTS = "This is a generated README file."


@pytest.fixture
def MockFileEditor():
    with patch("nail.tools.build.build_readme.FileEditor", autospec=True) as mock:
        yield mock


@pytest.fixture
def MockChat():
    with patch("nail.tools.build.build_readme.Chat", autospec=True) as mock:
        mock_chat = mock.return_value
        mock_chat.predict.return_value = TEST_README_CONTENTS
        yield mock


@pytest.fixture
def MockBuildReadmePrompt():
    with patch("nail.tools.build.build_readme.BuildReadmePrompt", autospec=True) as mock:
        mock_prompt = mock.return_value
        mock_prompt.text.return_value = TEST_PROMPT
        yield mock


def test_build_readme(MockBuildReadmePrompt, MockChat, MockFileEditor):
    readme_file_path = os.path.join(TEST_CONTEXT_DIRECTORY, TEST_README_FILE)
    mock_file_editor = MockFileEditor.return_value

    build_readme(readme_file_path)

    mock_file_editor.apply_changes.assert_called_once_with(
        TEST_README_CONTENTS)
