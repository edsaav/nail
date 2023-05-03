from unittest.mock import patch
from nail.tools.modify.modify_file import modify_file


@patch("nail.tools.modify.modify_file.Chat")
@patch('nail.tools.modify.modify_file.FileEditor')
@patch("nail.tools.modify.modify_file.ContextCompiler")
def test_modify_file(MockContextCompiler, MockFileEditor, MockChat):
    mock_file_editor = MockFileEditor.return_value
    mock_context_compiler = MockContextCompiler.return_value
    mock_chat = MockChat.return_value

    # Set the return values for mock functions
    mock_file_editor.content.return_value = 'original content'
    mock_chat.predict_code.return_value = 'expected modified content'
    mock_context_compiler.compile_all.return_value = 'context prefix'

    # Call the modify_file function with the mocked instance
    modify_file('path/to/file', 'request', context_file_paths=None, model=None)

    # Assert the expected behavior
    mock_file_editor.apply_changes.assert_called_once_with(
        'expected modified content')
