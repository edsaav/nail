import pytest
from unittest.mock import MagicMock, patch
from nail.core.language_models.open_ai import (
    OpenAIAPIError,
    GPT_3_5,
    GPT_4,
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
)

from nail.core.language_models.language_model import DEFAULT_SYSTEM_MESSAGE, CODE_SYSTEM_MESSAGE

PROMPT = "Create a python class that builds widgets."
RESPONSE = "This is an answer from OpenAI."


@pytest.fixture
def mock_openai_chat_response():
    mock_choice = MagicMock()
    mock_choice.message = {"content": RESPONSE}
    response = MagicMock()
    response.choices = [mock_choice]
    return response


@pytest.fixture
def MockChatCompletion():
    with patch("openai.ChatCompletion") as MockChatCompletion:
        yield MockChatCompletion


def test_gpt_3_5_respond(mock_openai_chat_response, MockChatCompletion):
    model = GPT_3_5('gpt-3.5-turbo')
    MockChatCompletion.create.return_value = mock_openai_chat_response

    response = model.respond(PROMPT)

    MockChatCompletion.create.assert_called_once_with(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "user", "content": f"{DEFAULT_SYSTEM_MESSAGE}\n{PROMPT}"}
        ],
        temperature=DEFAULT_TEMPERATURE,
        max_tokens=DEFAULT_MAX_TOKENS,
    )
    assert response == RESPONSE


def test_gpt_3_5_respond_with_code(mock_openai_chat_response, MockChatCompletion):
    model = GPT_3_5('gpt-3.5-turbo')
    MockChatCompletion.create.return_value = mock_openai_chat_response

    response = model.respond_with_code(PROMPT)

    MockChatCompletion.create.assert_called_once_with(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "user", "content": f"{CODE_SYSTEM_MESSAGE}\n{PROMPT}"}
        ],
        temperature=DEFAULT_TEMPERATURE,
        max_tokens=DEFAULT_MAX_TOKENS,
    )
    assert response == RESPONSE


def test_gpt_3_5_error_response(MockChatCompletion):
    model = GPT_3_5('gpt-3.5-turbo')
    MockChatCompletion.create.return_value = MagicMock()
    MockChatCompletion.create.return_value.choices = []

    with pytest.raises(OpenAIAPIError, match="OpenAI API response is invalid."):
        model.respond(PROMPT)


def test_gpt_4_respond(mock_openai_chat_response, MockChatCompletion):
    model = GPT_4('gpt-4')
    MockChatCompletion.create.return_value = mock_openai_chat_response

    response = model.respond(PROMPT)

    MockChatCompletion.create.assert_called_once_with(
        model='gpt-4',
        messages=[
            {"role": "system", "content": DEFAULT_SYSTEM_MESSAGE},
            {"role": "user", "content": PROMPT}
        ],
        temperature=DEFAULT_TEMPERATURE,
        max_tokens=DEFAULT_MAX_TOKENS,
    )
    assert response == RESPONSE


def test_gpt_4_respond_with_code(mock_openai_chat_response, MockChatCompletion):
    model = GPT_4('gpt-4')
    MockChatCompletion.create.return_value = mock_openai_chat_response

    response = model.respond_with_code(PROMPT)

    MockChatCompletion.create.assert_called_once_with(
        model='gpt-4',
        messages=[
            {"role": "system", "content": CODE_SYSTEM_MESSAGE},
            {"role": "user", "content": PROMPT}
        ],
        temperature=DEFAULT_TEMPERATURE,
        max_tokens=DEFAULT_MAX_TOKENS,
    )
    assert response == RESPONSE


def test_gpt_4_error_response(MockChatCompletion):
    model = GPT_4('gpt-4')
    MockChatCompletion.create.return_value = MagicMock()
    MockChatCompletion.create.return_value.choices = []

    with pytest.raises(OpenAIAPIError, match="OpenAI API response is invalid."):
        model.respond(PROMPT)
