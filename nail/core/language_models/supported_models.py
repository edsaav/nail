"""
Supported LLM classes are registered here in SUPPORTED_MODELS.
"""
from nail.core.language_models.open_ai import GPT_3_5, GPT_4


SUPPORTED_MODELS = {
    "gpt-3.5-turbo": GPT_3_5,
    "gpt-4": GPT_4,
}

DEFAULT_MODEL = "gpt-3.5-turbo"
