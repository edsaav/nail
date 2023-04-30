from unittest.mock import patch
from nail.tools.modify.modify_file import modify_file


@patch("nail.tools.modify.modify_file.predict_code")
@patch("nail.tools.modify.modify_file.build_context_prefix")
@patch('nail.tools.modify.modify_file.FileEditor')
def test_modify_file(MockFileEditor, mock_build_context_prefix, mock_predict_code):
    # Create a mock instance of FileEditor
    mock_file_editor = MockFileEditor.return_value

    # Set the return values and side effects for the mock_file_editor instance
    mock_file_editor.content.return_value = 'original content'
    mock_predict_code.return_value = 'expected modified content'
    mock_build_context_prefix.return_value = 'context prefix'

    # Call the modify_file function with the mocked instance
    modify_file('path/to/file', 'request', context_file_paths=None, model=None)

    # Assert the expected behavior
    mock_file_editor.apply_changes.assert_called_once_with(
        'expected modified content')
