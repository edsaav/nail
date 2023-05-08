import re

from nail.core.loading_decorator import loadable
from nail.core.language_models.supported_models import SUPPORTED_MODELS, DEFAULT_MODEL


class InvalidModelError(Exception):
    pass


class ModelCodeGenerationError(Exception):
    pass


class Chat:
    def __init__(self, model_name=None):
        self._set_llm_model(model_name)

    def predict(self, prompt):
        create_completion = loadable(self.model.respond, "Loading response...")
        return create_completion(prompt)

    def predict_code(self, prompt):
        create_completion = loadable(self.model.respond_with_code, "Generating code...")
        completion = create_completion(prompt)
        return self._extract_code(completion)

    def _extract_code(self, text):
        # regex for text wrapped in triple backticks
        # and optional language identifier
        code_block_pattern = r"^```(?:\w+)?\n([\s\S]*?)\n```"
        code_blocks = re.findall(code_block_pattern, text, re.MULTILINE)
        try:
            return code_blocks[0]
        except IndexError:
            err_msg = f"Model ({self.model_name}) failed to respond with code"
            raise ModelCodeGenerationError(err_msg)

    def _set_llm_model(self, model_name):
        self.model_name = DEFAULT_MODEL if model_name is None else model_name
        try:
            self.model = SUPPORTED_MODELS[self.model_name](self.model_name)
        except KeyError:
            raise InvalidModelError(f"Unsupported model: {model_name}")
