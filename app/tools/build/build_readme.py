from app.core.file_utils import apply_changes
from app.core.chat_utils import predict
from app.core.context_utils import build_context_prefix_from_directory

README_SYSTEM_MESSAGE = "You are a README generating assistant."
README_REQUEST = "Generate a README file for the application."
# TODO: Make this list configurable
IGNORE_LIST = ["README.md", "LICENSE", "tests",
               "test", "specs", "__pycache__", "nail.egg-info"]


def build_readme(readme_file_path, model=None):
    """
    Gathers context from all files in the current directory, builds a prompt for OpenAI to generate
    a README file for the application, calls the predict_readme method, and writes the generated file
    to the specified path.

    :param readme_file_path: Path to save the generated README file
    :param context_directory_path: Optional path to the directory containing the application files.
                                    If not provided, uses the current path.
    """
    context_prefix = build_context_prefix_from_directory(
        ignore_list=IGNORE_LIST)
    prompt = f"{context_prefix}{README_REQUEST}"
    readme_contents = predict(
        prompt, system_message_content=README_SYSTEM_MESSAGE, model=model)
    apply_changes(readme_file_path, readme_contents)
