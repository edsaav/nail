import pytest

from unittest.mock import MagicMock, patch

from nail.core.language_models.supported_models import SUPPORTED_MODELS, DEFAULT_MODEL
from nail.core.chat import Chat, InvalidModelError, ModelCodeGenerationError


def test_init_with_default_model():
    chat = Chat()
    assert chat.model_name == DEFAULT_MODEL
    assert type(chat.model) == SUPPORTED_MODELS[DEFAULT_MODEL]


def test_init_with_custom_model():
    custom_model_name = "custom_model"
    SUPPORTED_MODELS[custom_model_name] = MagicMock(
        return_value="custom_model_instance"
    )

    chat = Chat(custom_model_name)
    assert chat.model_name == custom_model_name
    assert chat.model == "custom_model_instance"

    del SUPPORTED_MODELS[custom_model_name]


def test_init_with_invalid_model():
    with pytest.raises(InvalidModelError):
        Chat("invalid_model")


def test_predict():
    chat = Chat()
    chat.model.respond = MagicMock(return_value="response")
    prompt = "test_prompt"

    with patch(
        "nail.core.loading_decorator.loadable",
        MagicMock(return_value=chat.model.respond),
    ):
        response = chat.predict(prompt)

    chat.model.respond.assert_called_once_with(prompt)
    assert response == "response"


def test_predict_code():
    chat = Chat()
    chat.model.respond_with_code = MagicMock(return_value="```\ncode\n```")
    prompt = "test_prompt"

    with patch(
        "nail.core.loading_decorator.loadable",
        MagicMock(return_value=chat.model.respond_with_code),
    ):
        code = chat.predict_code(prompt)

    chat.model.respond_with_code.assert_called_once_with(prompt)
    assert code == "code"


def test_predict_code_with_invalid_response():
    chat = Chat()
    chat.model.respond_with_code = MagicMock(return_value="no code block")
    prompt = "test_prompt"

    with patch(
        "nail.core.loading_decorator.loadable",
        MagicMock(return_value=chat.model.respond_with_code),
    ):
        with pytest.raises(ModelCodeGenerationError):
            chat.predict_code(prompt)
