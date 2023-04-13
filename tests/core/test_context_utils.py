from unittest.mock import patch
from app.core.context_utils import build_context_prefix, format_file_label, format_file_block

# Test data
test_file_path = "test_file.txt"
test_file_content = "This is a test file."


def test_format_file_label():
    expected_output = "[[test_file.txt]]"
    assert format_file_label(test_file_path) == expected_output


def test_format_file_block():
    expected_output = "[[test_file.txt]]\n```\nThis is a test file.\n```\n\n"
    assert format_file_block(
        test_file_path, test_file_content) == expected_output


def test_build_context_prefix_empty_list():
    assert build_context_prefix([]) == ""


@patch("app.core.context_utils.read_file", return_value=test_file_content)
@patch("app.core.context_utils.format_file_block", return_value=test_file_content)
def test_build_context_prefix_with_files(mock_format_file_block, mock_read_file):
    context_file_paths = [test_file_path]
    expected_output = "Existing files for context:\n\nThis is a test file.Given the above context, draft a new file using the following request:\n\n"
    assert build_context_prefix(context_file_paths) == expected_output
