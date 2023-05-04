from nail.core.file_editor import FileEditor
from nail.core.chat import Chat
from nail.core.prompt.prompt import BuildReadmePrompt


def build_readme(readme_file_path, model=None):
    """
    Gathers context from all files in the current directory, builds a prompt for OpenAI to generate
    a README file for the application, calls the predict_readme method, and writes the generated file
    to the specified path.

    :param readme_file_path: Path to save the generated README file
    """
    prompt = BuildReadmePrompt().text()
    readme_contents = Chat(model).predict(prompt)
    FileEditor(readme_file_path).apply_changes(readme_contents)
