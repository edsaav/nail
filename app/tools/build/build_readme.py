from app.core.file_utils import write_file
from app.core.chat_utils import predict_code
from app.core.context_utils import build_context_prefix_from_directory


def generate_readme(readme_file_path, context_directory_path=None):
    """
    Gathers context from all files in the current directory, builds a prompt for OpenAI to generate
    a README file for the application, calls the predict_code method, and writes the generated file
    to the specified path.

    :param readme_file_path: Path to save the generated README file
    :param context_directory_path: Optional path to the directory containing the application files.
                                    If not provided, uses the current path.
    """
    context_prefix = build_context_prefix_from_directory(
        context_directory_path)
    prompt = f"{context_prefix}Generate a README file for the application."
    readme_contents = predict_code(prompt)
    write_file(readme_file_path, readme_contents)