from nail.core.file_editor import FileEditor
from nail.core.chat import Chat, ModelCodeGenerationError
from nail.core.prompt.prompt import DebugPrompt

NO_BUGS_MESSAGE = 'No bugs were found in the file.'


def debug_file(file_path, error_message, model=None):
    file = FileEditor(file_path)
    prompt = DebugPrompt(file_path, details={
                         "error_message": error_message}).text()
    try:
        modified_contents = Chat(model).predict_code(prompt)
    except ModelCodeGenerationError:
        print(NO_BUGS_MESSAGE)
        return
    file.apply_changes(modified_contents)
