import os
from unittest.mock import patch
from nail.tools.build.build_readme import build_readme, README_REQUEST, README_SYSTEM_MESSAGE, IGNORE_LIST, FileEditor

# Test data
TEST_CONTEXT_DIRECTORY = "test_directory"
TEST_CONTEXT = "This is the content of the app files."
TEST_README_FILE = "README.md"
TEST_README_CONTENTS = "This is a generated README file."


@patch("nail.tools.build.build_readme.build_context_prefix_from_directory")
@patch("nail.tools.build.build_readme.predict")
@patch("nail.tools.build.build_readme.FileEditor")
def test_build_readme(MockFileEditor, mock_predict, mock_build_context):
    # Prepare the test environment
    readme_file_path = os.path.join(TEST_CONTEXT_DIRECTORY, TEST_README_FILE)

    # Set the return values for the mocked functions
    mock_build_context.return_value = TEST_CONTEXT
    mock_predict.return_value = TEST_README_CONTENTS
    mock_file_editor = MockFileEditor()
    mock_file_editor.apply_changes.return_value = True

    # Call the build_readme function
    build_readme(readme_file_path)

    # Check if the build_context_prefix_from_directory function was
    # called with the correct arguments
    mock_build_context.assert_called_once_with(ignore_list=IGNORE_LIST)

    # Check if the predict function was called with the correct arguments
    expected_prompt = f"{TEST_CONTEXT}{README_REQUEST}"
    mock_predict.assert_called_once_with(
        expected_prompt, system_message_content=README_SYSTEM_MESSAGE, model=None)

    # Check if the apply_changes function was called with the correct arguments
    mock_file_editor.apply_changes.assert_called_once_with(
        TEST_README_CONTENTS)
