from abc import ABC, abstractmethod

DEFAULT_SYSTEM_MESSAGE = "You are a helpful assistant."
CODE_SYSTEM_MESSAGE = """You are a code generating assistant.
You obey the following rules:
- You only respond only in code.
- You respond only in complete files.
- Any explanation should be included only as inline comments.
- You do not include usage examples."""


class LanguageModel(ABC):
    """
    Abstract base class representing a large language model. Delegates
    chat response logic out to implementations in model specific subclasses.

    Concrete language model classes must implement _respond_from_prompt to
    take a prompt string as a param and return a string as an answer.
    """

    def __init__(self, model_name: str):
        self.model_name = model_name

    def respond(self, prompt: str) -> str:
        """
        Respond to a prompt with a general instruction message prepended.

        :param prompt: The prompt to respond to.
        :return: The response string.
        """
        return self._respond_from_prompt(prompt, DEFAULT_SYSTEM_MESSAGE)

    def respond_with_code(self, prompt: str) -> str:
        """
        Respond to a prompt with a code generation instruction message prepended.

        :param prompt: The prompt to respond to.
        :return: The response string.
        """
        return self._respond_from_prompt(prompt, CODE_SYSTEM_MESSAGE)

    @abstractmethod
    def _respond_from_prompt(self, prompt: str, system_message: str) -> str:
        pass
