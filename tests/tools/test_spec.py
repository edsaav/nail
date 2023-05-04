from unittest.mock import patch
from nail.tools.spec.build_spec_file import build_spec_file


@patch("nail.tools.spec.build_spec_file.Chat")
@patch("nail.tools.spec.build_spec_file.FileEditor")
@patch("nail.tools.spec.build_spec_file.SpecPrompt")
def test_build_spec_file(MockSpecPrompt, MockFileEditor, MockChat):
    mock_file_editor = MockFileEditor.return_value
    mock_prompt = MockSpecPrompt.return_value
    mock_prompt.text.return_value = 'Create unit tests for the following: code'

    mock_chat = MockChat.return_value
    mock_chat.predict_code.return_value = (
        "def test_add():\n"
        "    assert add(1, 2) == 3\n"
    )

    build_spec_file("initial_file.py", "test_initial_file.py")

    # Assertions
    mock_file_editor.apply_changes.assert_called_once_with(
        "def test_add():\n    assert add(1, 2) == 3\n")
