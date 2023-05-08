import openai

from nail.core.config.user_config_utils import get_api_key
from nail.core.language_models.language_model import LanguageModel


DEFAULT_TEMPERATURE = 0.3
DEFAULT_MAX_TOKENS = 2048


class OpenAIAPIError(Exception):
    pass


class OpenAIChat(LanguageModel):
    """
    Implementation for the OpenAI chat (*not completion*) API.
    Reference: https://platform.openai.com/docs/guides/chat/introduction
    """

    def _user_message(self, message):
        return {"role": "user", "content": message}

    def _fetch_response(self, messages):
        openai.api_key = get_api_key()
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=messages,
            temperature=DEFAULT_TEMPERATURE,
            max_tokens=DEFAULT_MAX_TOKENS,
        )
        return response

    def _parse_response(self, response):
        try:
            return response.choices[0].message["content"]
        except (AttributeError, IndexError):
            raise OpenAIAPIError("OpenAI API response is invalid.")


class GPT_3_5(OpenAIChat):
    """
    This implementation instead prefixes the initial user message with the
    system message content. This should result in more accurate instruction
    following.

    From the OpenAI docs:
    "gpt-3.5-turbo-0301 does not always pay strong attention to system messages.
    Future models will be trained to pay stronger attention to system messages."
    """

    def _respond_from_prompt(self, prompt, system_message):
        full_prompt = f"{system_message}\n{prompt}"
        messages = [self._user_message(full_prompt)]
        return self._parse_response(self._fetch_response(messages))


class GPT_4(OpenAIChat):
    """
    The GPT-4 model makes full use of the concept of system messages, so
    this implementation uses them as intended.
    """

    def _system_message(self, message):
        return {"role": "system", "content": message}

    def _respond_from_prompt(self, prompt, system_message):
        messages = [self._system_message(system_message), self._user_message(prompt)]
        return self._parse_response(self._fetch_response(messages))
