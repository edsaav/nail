from unittest.mock import patch
from nail.core.context_utils import (
    build_context_prefix,
    format_file_label,
    format_file_block,
    list_all_files,
    build_context_prefix_from_directory,
)

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


@patch("nail.core.context_utils.format_file_block", return_value=test_file_content)
def test_build_context_prefix_with_files(_, tmp_path):
    # Create a test file
    file_path = tmp_path / test_file_path
    file_path.write_text(test_file_content)

    context_file_paths = [file_path]
    expected_output = "Existing files for context:\n\nThis is a test file." \
        + "Given the above context, draft a new file using the " \
        + "following request:\n\n"
    assert build_context_prefix(context_file_paths) == expected_output


@patch("os.walk")
def test_list_all_files(mock_os_walk):
    # Mock the os.walk generator to return a single file
    mock_os_walk.return_value = [("root", [], ["test_file.txt"])]

    file_paths = list_all_files()
    assert len(file_paths) == 1
    assert file_paths[0] == "root/test_file.txt"


@patch("nail.core.context_utils.list_all_files")
@patch("nail.core.context_utils.build_context_prefix")
def test_build_context_prefix_from_directory(
        mock_build_context_prefix, mock_list_all_files):
    # Mock list_all_files to return a single file path
    mock_list_all_files.return_value = [test_file_path]

    # Mock build_context_prefix to return a string
    mock_build_context_prefix.return_value = "Mocked context prefix"

    context_prefix = build_context_prefix_from_directory()
    mock_list_all_files.assert_called_once()
    mock_build_context_prefix.assert_called_once_with([test_file_path])
    assert context_prefix == "Mocked context prefix"
