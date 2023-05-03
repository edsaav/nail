from unittest.mock import patch
from nail.tools.spec.build_spec_file import build_spec_file, SPEC_PREFIX


@patch("nail.tools.spec.build_spec_file.Chat")
@patch("nail.tools.spec.build_spec_file.FileEditor")
@patch("nail.tools.spec.build_spec_file.file_block")
def test_build_spec_file(mock_file_block, MockFileEditor, MockChat):
    mock_file_editor = MockFileEditor.return_value
    target_code_block = "```\ndef add(a, b):\n    return a + b\n```"

    mock_file_block.return_value = target_code_block

    mock_chat = MockChat.return_value
    mock_chat.predict_code.return_value = (
        "def test_add():\n"
        "    assert add(1, 2) == 3\n"
    )

    build_spec_file("initial_file.py", "test_initial_file.py")

    # Assertions
    mock_chat.predict_code.assert_called_once_with(
        f"{SPEC_PREFIX}\n\n{target_code_block}",
    )
    mock_file_editor.apply_changes.assert_called_once_with(
        "def test_add():\n    assert add(1, 2) == 3\n")
