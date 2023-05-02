from nail.core.file_editor import FileEditor
from nail.core.chat_utils import predict
from nail.core.prompt.context_compiler import ContextCompiler

README_SYSTEM_MESSAGE = "You are a README generating assistant."
README_REQUEST = "Generate a README file for the application."


def build_readme(readme_file_path, model=None):
    """
    Gathers context from all files in the current directory, builds a prompt for OpenAI to generate
    a README file for the application, calls the predict_readme method, and writes the generated file
    to the specified path.

    :param readme_file_path: Path to save the generated README file
    :param context_directory_path: Optional path to the directory containing the application files.
                                    If not provided, uses the current path.
    """
    context_prefix = ContextCompiler().compile_all_minus_ignored()
    prompt = f"{context_prefix}{README_REQUEST}"
    readme_contents = predict(
        prompt, system_message_content=README_SYSTEM_MESSAGE, model=model)
    file = FileEditor(readme_file_path)
    file.apply_changes(readme_contents)
