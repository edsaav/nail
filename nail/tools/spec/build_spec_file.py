from nail.core.chat import Chat
from nail.core.file_editor import FileEditor
from nail.core.prompt.formatting_utils import file_block

SPEC_PREFIX = "Create a unit test file for the following code:"


def build_spec_file(file_path, target_file_path, model=None):

    # Send the contents of the target file along with the
    # request to build a spec to the model
    prompt = f"{SPEC_PREFIX}\n\n{file_block(file_path)}"
    test_file_content = Chat(model).predict_code(prompt)

    # Write the contents of the test file to the target file path
    test_file = FileEditor(target_file_path)
    test_file.apply_changes(test_file_content)
