import pytest

from unittest.mock import patch
from nail.tools.explain_file import explain_file


@pytest.fixture
def MockExplainPrompt():
    with patch("nail.tools.explain_file.ExplainPrompt", autospec=True) as mock:
        mock_prompt = mock.return_value
        mock_prompt.text.return_value = "Explain the following: code"
        yield mock


@pytest.fixture
def MockChat():
    with patch("nail.tools.explain_file.Chat", autospec=True) as mock:
        mock_chat = mock.return_value
        mock_chat.predict_code.return_value = "Here is the explanation"
        yield mock


@pytest.fixture
def MockConsole():
    with patch("nail.tools.explain_file.Console", autospec=True) as mock:
        yield mock


@pytest.fixture
def MockMarkdown():
    with patch("nail.tools.explain_file.Markdown", autospec=True) as mock:
        mock.return_value = "Here is the explanation"
        yield mock


def test_explain_file(MockExplainPrompt, MockChat, MockConsole, MockMarkdown):
    mock_console = MockConsole.return_value

    explain_file("initial_file.py")

    mock_console.print.assert_called_once_with("Here is the explanation")
