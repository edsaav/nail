import re
import openai

DEFAULT_SYSTEM_MESSAGE = "You are a helpful assistant."
CODE_SYSTEM_MESSAGE = """You are a code generating assistant.
You obey the following rules:
- You only respond only in code.
- You respond only in complete files.
- Any explanation should be included only as inline comments.
- You do not include usage examples."""

DEFAULT_TEMPERATURE = 0.3
DEFAULT_MAX_TOKENS = 2048
DEFAULT_MODEL = "gpt-3.5-turbo"

SUPPORTED_MODELS = [
    "gpt-3.5-turbo",
    "gpt-4",
]


def predict(prompt, system_message_content=DEFAULT_SYSTEM_MESSAGE, model=DEFAULT_MODEL):
    if model == None:
        model = DEFAULT_MODEL
    if model not in SUPPORTED_MODELS:
        raise ValueError("Unsupported LLM model requested.")

    messages = [
        system_message(system_message_content),
        user_message(prompt)
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=DEFAULT_TEMPERATURE,
        max_tokens=DEFAULT_MAX_TOKENS,
    )

    return response.choices[0].message["content"]


def predict_code(prompt, model=DEFAULT_MODEL):
    prediction = predict(
        prompt, system_message_content=CODE_SYSTEM_MESSAGE, model=model)

    return extract_code(prediction)


def extract_code(text):
    # Regular expression pattern to detect code wrapped with triple backticks and optional language identifier
    pattern = r"^```(?:\w+)?\n([\s\S]*?)\n```"
    matches = re.findall(pattern, text, re.MULTILINE)

    # Return only the first found match, considering there is only one code block
    return matches[0] if matches else ""


def user_message(message):
    return {"role": "user", "content": message}


def system_message(message):
    return {"role": "system", "content": message}
