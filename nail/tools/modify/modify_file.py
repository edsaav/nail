from nail.core.file_editor import FileEditor
from nail.core.chat import Chat
from nail.core.prompt.prompt import ModifyPrompt


def modify_file(file_path, request, context_file_paths=None, model=None):
    prompt = ModifyPrompt(file_path, context_file_paths,
                          details={'request': request}).text()
    modified_contents = Chat(model).predict_code(prompt)
    FileEditor(file_path).apply_changes(modified_contents)
