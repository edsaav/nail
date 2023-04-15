import os
from unittest.mock import patch
from app.tools.build.build_readme import generate_readme, README_REQUEST, README_SYSTEM_MESSAGE, IGNORE_LIST

# Test data
TEST_CONTEXT_DIRECTORY = "test_directory"
TEST_README_FILE = "README.md"
TEST_README_CONTENTS = "This is a generated README file."


@patch("app.tools.build.build_readme.build_context_prefix_from_directory")
@patch("app.tools.build.build_readme.predict")
@patch("app.tools.build.build_readme.write_file")
def test_generate_readme(mock_write_file, mock_predict, mock_build_context):
    # Prepare the test environment
    readme_file_path = os.path.join(TEST_CONTEXT_DIRECTORY, TEST_README_FILE)

    # Set the return values for the mocked functions
    mock_build_context.return_value = TEST_CONTEXT_DIRECTORY
    mock_predict.return_value = TEST_README_CONTENTS

    # Call the generate_readme function
    generate_readme(readme_file_path, TEST_CONTEXT_DIRECTORY)

    # Check if the build_context_prefix_from_directory function was called with the correct arguments
    mock_build_context.assert_called_once_with(TEST_CONTEXT_DIRECTORY, ignore_list=IGNORE_LIST)

    # Check if the predict function was called with the correct arguments
    expected_prompt = f"{TEST_CONTEXT_DIRECTORY}{README_REQUEST}"
    mock_predict.assert_called_once_with(
        expected_prompt, system_message_content=README_SYSTEM_MESSAGE)

    # Check if the write_file function was called with the correct arguments
    mock_write_file.assert_called_once_with(
        readme_file_path, TEST_README_CONTENTS)
