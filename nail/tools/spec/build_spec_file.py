from nail.core.chat import Chat
from nail.core.file_editor import FileEditor
from nail.core.prompt.prompt import SpecPrompt


def build_spec_file(file_path, target_file_path, model=None):
    prompt = SpecPrompt(file_path).text()
    test_file_content = Chat(model).predict_code(prompt)
    FileEditor(target_file_path).apply_changes(test_file_content)
