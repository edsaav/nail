from rich.console import Console
from rich.markdown import Markdown
from nail.core.chat import Chat
from nail.core.prompt.prompt import ExplainPrompt


def explain_file(file_path, context_file_paths=None, verbose=False, model=None):
    prompt = ExplainPrompt(file_path, context_file_paths, {"verbose": verbose}).text()
    explanation = Chat(model).predict(prompt)
    Console().print(Markdown(explanation))
