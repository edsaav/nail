import os
from unittest.mock import patch
from nail.tools.build.build_readme import build_readme

# Test data
TEST_CONTEXT_DIRECTORY = "test_directory"
TEST_PROMPT = "This is the content of the app files. Generate a README file."
TEST_README_FILE = "README.md"
TEST_README_CONTENTS = "This is a generated README file."


@patch("nail.tools.build.build_readme.FileEditor")
@patch("nail.tools.build.build_readme.Chat")
@patch("nail.tools.build.build_readme.BuildReadmePrompt")
def test_build_readme(MockBuildReadmePrompt, MockChat, MockFileEditor):
    # Prepare the test environment
    readme_file_path = os.path.join(TEST_CONTEXT_DIRECTORY, TEST_README_FILE)

    # Set the return values for the mocked functions
    mock_chat = MockChat()
    mock_chat.predict.return_value = TEST_README_CONTENTS
    mock_prompt = MockBuildReadmePrompt.return_value
    mock_prompt.text.return_value = TEST_PROMPT
    mock_file_editor = MockFileEditor()
    mock_file_editor.apply_changes.return_value = True

    # Call the build_readme function
    build_readme(readme_file_path)

    # Check if the apply_changes function was called with the correct arguments
    mock_file_editor.apply_changes.assert_called_once_with(
        TEST_README_CONTENTS)
