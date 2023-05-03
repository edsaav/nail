from nail.core.chat import Chat
from nail.core.file_editor import FileEditor


def build_spec_file(file_path, target_file_path, model=None):
    # Read the content of the initial file
    initial_file = FileEditor(file_path)
    initial_file_content = initial_file.content()

    # Send the content to the predict_code function with a request to build a unit test file
    prompt = f"Create a unit test file for the following code, using pytest:\n\n```\n{initial_file_content}\n```"
    test_file_content = Chat(model).predict_code(prompt)

    # Write the contents of the test file to the target file path
    test_file = FileEditor(target_file_path)
    test_file.apply_changes(test_file_content)
